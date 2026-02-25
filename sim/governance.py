"""Rule formation, voting mechanics, and enforcement."""

from __future__ import annotations

from sim.models import Environment, Proposal, EnforceableRule


VALID_ENFORCEMENT_TYPES = {"tax", "sanction", "repeal"}


def validate_enforcement(enforcement: dict, env: Environment) -> bool:
    """Validate enforcement params. Returns True if valid and enforceable."""
    if not isinstance(enforcement, dict):
        return False
    etype = enforcement.get("type")
    if etype not in VALID_ENFORCEMENT_TYPES:
        return False

    agent_names = [a.name for a in env.agents]

    if etype == "tax":
        threshold = enforcement.get("threshold")
        amount = enforcement.get("amount")
        if not isinstance(threshold, (int, float)) or threshold <= 0:
            return False
        if not isinstance(amount, (int, float)) or amount < 1 or amount > 5:
            return False
        return True

    if etype == "sanction":
        target = enforcement.get("target")
        amount = enforcement.get("amount")
        if target not in agent_names:
            return False
        if not isinstance(amount, (int, float)) or amount < 1 or amount > 3:
            return False
        return True

    if etype == "repeal":
        rule_id = enforcement.get("rule_id")
        if not isinstance(rule_id, int):
            return False
        # Must reference an existing active enforceable rule
        if not any(r.id == rule_id for r in env.enforceable_rules):
            return False
        return True

    return False


def create_proposal(env: Environment, proposed_by: str, rule: str, enforcement: dict | None = None) -> Proposal:
    """Create a new rule proposal. Auto-adds proposer's yes vote."""
    # Validate enforcement — invalid params become advisory-only
    valid_enforcement = None
    if enforcement and validate_enforcement(enforcement, env):
        valid_enforcement = enforcement

    proposal = Proposal(
        id=env.proposal_counter,
        proposed_by=proposed_by,
        rule=rule,
        round_proposed=env.round_num,
        enforcement=valid_enforcement,
    )
    # Auto-yes: proposing implies support
    proposal.votes[proposed_by] = "yes"
    env.pending_proposals.append(proposal)
    env.proposal_counter += 1
    return proposal


def cast_vote(env: Environment, voter: str, proposal_id: int, vote: str) -> bool:
    """Cast a vote on a pending proposal. Returns True if valid."""
    proposal = next((p for p in env.pending_proposals if p.id == proposal_id), None)
    if proposal is None or proposal.status != "pending":
        return False
    if vote not in ("yes", "no"):
        return False
    proposal.votes[voter] = vote
    return True


def repeal_rule(env: Environment, rule_id: int) -> str | None:
    """Remove an enforceable rule. Returns the rule text if found, None otherwise."""
    for i, rule in enumerate(env.enforceable_rules):
        if rule.id == rule_id:
            removed = env.enforceable_rules.pop(i)
            return removed.text
    return None


def process_pending_votes(env: Environment) -> list[str]:
    """Check all pending proposals. Majority yes = passed. Returns list of newly enacted rules."""
    num_agents = len(env.agents)
    threshold = num_agents / 2  # Simple majority
    enacted = []

    for proposal in env.pending_proposals:
        if proposal.status != "pending":
            continue
        # Only resolve if all agents have voted OR proposal is 3+ rounds old
        all_voted = len(proposal.votes) >= num_agents
        expired = (env.round_num - proposal.round_proposed) >= 3

        if all_voted or expired:
            yes_votes = sum(1 for v in proposal.votes.values() if v == "yes")
            if yes_votes > threshold:
                proposal.status = "passed"
                env.rules.append(proposal.rule)
                enacted.append(proposal.rule)

                # Handle enforcement
                if proposal.enforcement:
                    etype = proposal.enforcement.get("type")
                    if etype == "repeal":
                        # Repeal removes an existing enforceable rule
                        target_id = proposal.enforcement["rule_id"]
                        repealed_text = repeal_rule(env, target_id)
                        if repealed_text:
                            env.public_log.append({
                                "round": env.round_num,
                                "agent": "SYSTEM",
                                "action": {"action": "rule_repealed"},
                                "summary": f"[RULE REPEALED] Rule #{target_id}: \"{repealed_text}\"",
                            })
                    else:
                        # Tax or sanction — add to enforceable rules
                        enforceable = EnforceableRule(
                            id=proposal.id,
                            text=proposal.rule,
                            enforcement=proposal.enforcement,
                            enacted_round=env.round_num,
                        )
                        env.enforceable_rules.append(enforceable)
            else:
                proposal.status = "failed"

    return enacted


def enforce_rules(env: Environment) -> list[dict]:
    """Apply all active enforceable rules. Returns log of enforcement events."""
    events = []
    agent_map = {a.name: a for a in env.agents}

    for rule in env.enforceable_rules:
        etype = rule.enforcement.get("type")

        if etype == "tax":
            threshold = rule.enforcement["threshold"]
            amount = rule.enforcement["amount"]

            # Find payers (above threshold) and recipients (below threshold)
            payers = [a for a in env.agents if a.tokens > threshold]
            recipients = [a for a in env.agents if a.tokens < threshold]

            if not recipients:
                # Nobody below threshold — tax doesn't trigger
                continue

            total_collected = 0
            for payer in payers:
                payment = min(amount, payer.tokens)
                if payment > 0:
                    payer.tokens -= payment
                    total_collected += payment

            if total_collected > 0:
                # Give to poorest agent below threshold
                recipients.sort(key=lambda a: (a.tokens, a.name))
                poorest = recipients[0]
                poorest.tokens += total_collected
                events.append({
                    "round": env.round_num,
                    "agent": "SYSTEM",
                    "action": {"action": "tax_enforced", "rule_id": rule.id},
                    "summary": f"[TAX] Rule #{rule.id}: collected {total_collected} from agents above {threshold} credits → {poorest.name} (balance: {poorest.tokens})",
                })

        elif etype == "sanction":
            target_name = rule.enforcement["target"]
            amount = rule.enforcement["amount"]
            target = agent_map.get(target_name)

            if not target or target.tokens == 0:
                continue

            payment = min(amount, target.tokens)
            target.tokens -= payment

            # Split among all OTHER agents
            others = [a for a in env.agents if a.name != target_name]
            if others and payment > 0:
                per_agent = payment // len(others)
                remainder = payment % len(others)
                for other in others:
                    other.tokens += per_agent
                # Give remainder to first alphabetically
                if remainder > 0:
                    others_sorted = sorted(others, key=lambda a: a.name)
                    others_sorted[0].tokens += remainder

                events.append({
                    "round": env.round_num,
                    "agent": "SYSTEM",
                    "action": {"action": "sanction_enforced", "rule_id": rule.id},
                    "summary": f"[SANCTION] Rule #{rule.id}: {target_name} paid {payment} credits, split among others",
                })

    return events
