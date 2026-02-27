"""Rule formation, voting mechanics, and enforcement."""

from __future__ import annotations

from sim.models import Environment, Proposal, EnforceableRule, Challenge


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


def _poorest_agent(agents: list, exclude: str | None = None):
    """Return the poorest agent (lowest tokens, ties broken alphabetically). Optionally exclude one agent by name."""
    candidates = [a for a in agents if a.name != exclude] if exclude else list(agents)
    if not candidates:
        return None
    candidates.sort(key=lambda a: (a.tokens, a.name))
    return candidates[0]


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
                            origin="proposal",
                        )
                        env.enforceable_rules.append(enforceable)
            else:
                proposal.status = "failed"

    return enacted


def _enforce_single_rule(rule: EnforceableRule, env: Environment) -> list[dict]:
    """Apply a single enforceable rule. Returns log events."""
    events = []
    etype = rule.enforcement.get("type")

    if etype == "tax":
        threshold = rule.enforcement["threshold"]
        amount = rule.enforcement["amount"]

        # Find payers (above threshold) and recipients (below threshold)
        payers = [a for a in env.agents if a.tokens > threshold]
        recipients = [a for a in env.agents if a.tokens < threshold]

        if not recipients:
            return events

        total_collected = 0
        for payer in payers:
            payment = min(amount, payer.tokens)
            if payment > 0:
                payer.tokens -= payment
                total_collected += payment

        if total_collected > 0:
            poorest = _poorest_agent(recipients)
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
        target = next((a for a in env.agents if a.name == target_name), None)

        if not target or target.tokens == 0:
            return events

        payment = min(amount, target.tokens)
        target.tokens -= payment

        # Split among all OTHER agents
        others = [a for a in env.agents if a.name != target_name]
        if others and payment > 0:
            per_agent = payment // len(others)
            remainder = payment % len(others)
            for other in others:
                other.tokens += per_agent
            # Give remainder to poorest (ties broken alphabetically)
            if remainder > 0:
                poorest = _poorest_agent(others)
                poorest.tokens += remainder

            events.append({
                "round": env.round_num,
                "agent": "SYSTEM",
                "action": {"action": "sanction_enforced", "rule_id": rule.id},
                "summary": f"[SANCTION] Rule #{rule.id}: {target_name} paid {payment} credits, split among others",
            })

    return events


def enforce_rules(env: Environment) -> list[dict]:
    """Apply all active enforceable rules. Returns log of enforcement events."""
    events = []
    for rule in env.enforceable_rules:
        events.extend(_enforce_single_rule(rule, env))
    return events


# ---------------------------------------------------------------------------
# Decree mechanics
# ---------------------------------------------------------------------------

def enact_decree(env: Environment, agent_name: str, rule_text: str, enforcement: dict) -> tuple[EnforceableRule | None, list[dict]]:
    """Enact a decree: immediately create an enforceable rule without voting.

    Cost is deducted from the agent and redistributed to others (poorest gets remainder).
    Returns (rule_or_None, log_entries).
    """
    logs = []
    agent = next((a for a in env.agents if a.name == agent_name), None)
    if not agent:
        return None, [{"error": f"Agent {agent_name} not found"}]

    cost = env.decree_cost
    if cost <= 0:
        return None, [{"error": "Decrees are disabled (decree_cost=0)"}]

    if agent.tokens < cost:
        return None, [{"error": f"{agent_name} cannot afford decree (needs {cost}, has {agent.tokens})"}]

    if not validate_enforcement(enforcement, env):
        return None, [{"error": f"Invalid enforcement params for decree"}]

    # Deduct cost
    agent.tokens -= cost

    # Redistribute cost to others (poorest gets remainder)
    others = [a for a in env.agents if a.name != agent_name]
    if others and cost > 0:
        per_agent = cost // len(others)
        remainder = cost % len(others)
        for other in others:
            other.tokens += per_agent
        if remainder > 0:
            poorest = _poorest_agent(others)
            poorest.tokens += remainder

    # Create enforceable rule with decree origin
    rule = EnforceableRule(
        id=env.proposal_counter,
        text=rule_text,
        enforcement=enforcement,
        enacted_round=env.round_num,
        origin="decree",
        decreed_by=agent_name,
    )
    env.proposal_counter += 1  # Shared counter with proposals

    # Handle repeal type immediately
    if enforcement.get("type") == "repeal":
        target_id = enforcement["rule_id"]
        repealed_text = repeal_rule(env, target_id)
        if repealed_text:
            logs.append({
                "round": env.round_num,
                "agent": "SYSTEM",
                "action": {"action": "rule_repealed"},
                "summary": f"[DECREE REPEAL] Rule #{target_id}: \"{repealed_text}\" — repealed by decree from {agent_name}",
            })
        return rule, logs

    # Add to enforceable rules
    env.enforceable_rules.append(rule)
    env.rules.append(rule_text)

    # Immediately enforce
    enforcement_logs = _enforce_single_rule(rule, env)
    logs.extend(enforcement_logs)

    return rule, logs


# ---------------------------------------------------------------------------
# Challenge mechanics
# ---------------------------------------------------------------------------

def create_challenge(env: Environment, challenger_name: str, target_rule_id: int) -> tuple[Challenge | None, list[dict]]:
    """Create a challenge against an active enforceable rule.

    Cost is deducted and redistributed. Challenger auto-votes "repeal".
    Returns (challenge_or_None, log_entries).
    """
    logs = []
    challenger = next((a for a in env.agents if a.name == challenger_name), None)
    if not challenger:
        return None, [{"error": f"Agent {challenger_name} not found"}]

    cost = env.challenge_cost
    if cost <= 0:
        return None, [{"error": "Challenges are disabled (challenge_cost=0)"}]

    if challenger.tokens < cost:
        return None, [{"error": f"{challenger_name} cannot afford challenge (needs {cost}, has {challenger.tokens})"}]

    # Target rule must exist and be active
    target_rule = next((r for r in env.enforceable_rules if r.id == target_rule_id), None)
    if not target_rule:
        return None, [{"error": f"Rule #{target_rule_id} not found or not active"}]

    # Cannot challenge a rule enacted this round
    if target_rule.enacted_round == env.round_num:
        return None, [{"error": f"Rule #{target_rule_id} was enacted this round — wait until next round to challenge"}]

    # No duplicate pending challenges on same rule
    existing = any(c for c in env.pending_challenges if c.target_rule_id == target_rule_id and c.status == "pending")
    if existing:
        return None, [{"error": f"Rule #{target_rule_id} already has a pending challenge"}]

    # Deduct cost and redistribute
    challenger.tokens -= cost
    others = [a for a in env.agents if a.name != challenger_name]
    if others and cost > 0:
        per_agent = cost // len(others)
        remainder = cost % len(others)
        for other in others:
            other.tokens += per_agent
        if remainder > 0:
            poorest = _poorest_agent(others)
            poorest.tokens += remainder

    # Create challenge
    challenge = Challenge(
        id=env.proposal_counter,
        target_rule_id=target_rule_id,
        challenged_by=challenger_name,
        round_created=env.round_num,
    )
    env.proposal_counter += 1  # Shared counter
    challenge.votes[challenger_name] = "repeal"  # Auto-vote

    env.pending_challenges.append(challenge)

    return challenge, logs


def cast_challenge_vote(env: Environment, voter: str, challenge_id: int, vote: str) -> bool:
    """Cast a vote on a pending challenge. Valid votes: 'repeal' or 'keep'. Returns True if valid."""
    challenge = next((c for c in env.pending_challenges if c.id == challenge_id), None)
    if challenge is None or challenge.status != "pending":
        return False
    if vote not in ("repeal", "keep"):
        return False
    challenge.votes[voter] = vote
    return True


def process_pending_challenges(env: Environment) -> list[dict]:
    """Resolve pending challenges. Returns log events."""
    num_agents = len(env.agents)
    threshold = num_agents / 2  # Simple majority
    events = []

    for challenge in env.pending_challenges:
        if challenge.status != "pending":
            continue

        all_voted = len(challenge.votes) >= num_agents
        expired = (env.round_num - challenge.round_created) >= 3

        if all_voted or expired:
            repeal_votes = sum(1 for v in challenge.votes.values() if v == "repeal")

            if repeal_votes > threshold:
                # Majority repeal — remove the rule
                challenge.status = "repealed"
                repealed_text = repeal_rule(env, challenge.target_rule_id)
                events.append({
                    "round": env.round_num,
                    "agent": "SYSTEM",
                    "action": {"action": "challenge_succeeded", "challenge_id": challenge.id,
                               "rule_id": challenge.target_rule_id},
                    "summary": f"[CHALLENGE WON] Challenge #{challenge.id}: Rule #{challenge.target_rule_id} repealed "
                               f"(\"{repealed_text or '?'}\")",
                })
            else:
                # Majority keep — challenger drops to 1 credit, lost credits redistributed
                challenge.status = "sustained"
                challenger = next((a for a in env.agents if a.name == challenge.challenged_by), None)
                if challenger and challenger.tokens > 1:
                    lost = challenger.tokens - 1
                    challenger.tokens = 1
                    # Redistribute lost credits
                    others = [a for a in env.agents if a.name != challenge.challenged_by]
                    if others and lost > 0:
                        per_agent = lost // len(others)
                        remainder = lost % len(others)
                        for other in others:
                            other.tokens += per_agent
                        if remainder > 0:
                            poorest = _poorest_agent(others)
                            poorest.tokens += remainder

                events.append({
                    "round": env.round_num,
                    "agent": "SYSTEM",
                    "action": {"action": "challenge_failed", "challenge_id": challenge.id,
                               "rule_id": challenge.target_rule_id},
                    "summary": f"[CHALLENGE LOST] Challenge #{challenge.id}: Rule #{challenge.target_rule_id} sustained. "
                               f"{challenge.challenged_by} drops to 1 credit.",
                })

    return events
