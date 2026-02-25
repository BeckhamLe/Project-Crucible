"""Prompt construction for agent turns."""

import json
from sim.models import Agent, Environment


def build_turn_prompt(agent: Agent, env: Environment) -> str:
    """Build the user prompt for an agent's turn."""
    other_agents = [a for a in env.agents if a.name != agent.name]
    agent_balances = ", ".join(
        f"{a.name}: {a.tokens} credits{'  [BANKRUPT]' if a.tokens == 0 else ''}"
        for a in env.agents
    )

    recent_public = env.public_log[-20:] if len(env.public_log) > 20 else env.public_log
    public_log_text = "\n".join(
        f"  [Round {e['round']}] {e['agent']}: {e['summary']}"
        for e in recent_public
    ) if recent_public else "  (no public events yet)"

    private_text = "\n".join(
        f"  From {m['from']} (Round {m['round']}): {m['message']}"
        for m in agent.private_messages[-10:]
    ) if agent.private_messages else "  (none)"

    rules_text = "\n".join(f"  - {r}" for r in env.rules) if env.rules else "  (no rules enacted yet)"

    # Active enforcement rules
    enforcement_text = ""
    if env.enforceable_rules:
        enforcement_lines = []
        for r in env.enforceable_rules:
            etype = r.enforcement.get("type", "unknown")
            if etype == "tax":
                desc = f"Agents above {r.enforcement['threshold']} credits pay {r.enforcement['amount']}/round to poorest"
            elif etype == "sanction":
                desc = f"{r.enforcement['target']} pays {r.enforcement['amount']}/round, split among others"
            else:
                desc = json.dumps(r.enforcement)
            enforcement_lines.append(f"  [Rule #{r.id}] {etype.upper()}: {desc} — \"{r.text}\"")
        enforcement_text = "\n\nACTIVE ENFORCEMENTS (these execute automatically each round):\n" + "\n".join(enforcement_lines)
    else:
        enforcement_text = "\n\nACTIVE ENFORCEMENTS:\n  (none — no enforceable rules have been enacted yet)"

    # Pending proposals for free voting
    pending = [p for p in env.pending_proposals if p.status == "pending"]
    if pending:
        pending_lines = []
        for p in pending:
            enforcement_tag = ""
            if p.enforcement:
                enforcement_tag = f" [ENFORCEABLE: {p.enforcement['type']}]"
            pending_lines.append(
                f"  [{p.id}] Proposed by {p.proposed_by}: \"{p.rule}\"{enforcement_tag} — Votes so far: {json.dumps(p.votes)}"
            )
        pending_text = "\n".join(pending_lines)
    else:
        pending_text = "  (no pending proposals)"

    memory_text = agent.memory if agent.memory else "(no memories yet — this is the beginning)"

    maintenance_text = ""
    if env.maintenance_cost > 0:
        maintenance_text = f"\n  Maintenance cost: {env.maintenance_cost} credits/round (deducted at start of each round)"
        maintenance_text += f"\n  WARNING: If your credits hit 0, you are BANKRUPT. You can still act but you cannot trade."

    work_text = ""
    if env.work_credits > 0:
        work_text = f"\n  Work income: {env.work_credits} credits/round (only if you choose the work action)"

    return f"""ROUND {env.round_num + 1} — It is your turn.

YOUR STATUS:
  Name: {agent.name}
  Credits: {agent.tokens}{'  [BANKRUPT]' if agent.tokens == 0 else ''}{maintenance_text}{work_text}

ALL AGENT BALANCES:
  {agent_balances}

CURRENT RULES:
{rules_text}
{enforcement_text}

VOTE ON PENDING PROPOSALS (free — does NOT cost your action):
{pending_text}

RECENT PUBLIC EVENTS:
{public_log_text}

YOUR PRIVATE MESSAGES:
{private_text}

YOUR MEMORY:
{memory_text}

---

Respond with valid JSON only, no other text.

RESPONSE FORMAT:
{{
  "votes": {{"PROPOSAL_ID": "yes" or "no", ...}},
  "action": "ACTION_TYPE",
  ...action params...
}}

"votes" is OPTIONAL. Include it to vote on any pending proposals above. You may vote on multiple proposals at once. Voting is FREE — it does not use your action.

Available actions (choose ONE for your main action):
1. {{"action": "work"}} — Earn {env.work_credits} credit(s). Uses your action but keeps you financially stable.
2. {{"action": "public_message", "message": "your message"}}
3. {{"action": "private_message", "to": "AgentName", "message": "your message"}}
4. {{"action": "trade", "to": "AgentName", "amount": NUMBER, "reason": "why"}}
5. {{"action": "propose_rule", "rule": "the rule text", "enforcement": {{"type": "TYPE", ...params}}}}
6. {{"action": "vote", "proposal_id": NUMBER, "vote": "yes" or "no"}} — Use ONLY if you want voting to be your main action instead of doing something else.
7. {{"action": "nothing"}}

ENFORCEMENT TYPES for propose_rule:
- TAX: {{"type": "tax", "threshold": NUMBER, "amount": 1-5}} — Agents above threshold pay amount/round to the poorest agent below threshold.
- SANCTION: {{"type": "sanction", "target": "AgentName", "amount": 1-3}} — Named agent pays amount/round, split among everyone else. Requires majority vote.
- REPEAL: {{"type": "repeal", "rule_id": NUMBER}} — Remove an active enforcement rule.
- Omit "enforcement" to propose an advisory-only rule (no automatic enforcement).

Rules:
- You can only trade credits you have (max: {agent.tokens}).
- Trade amounts must be positive integers.
- The other agents are: {', '.join(a.name for a in other_agents)}.

Respond with ONLY the JSON object."""


def build_memory_prompt(agent: Agent, env: Environment, action_taken: dict) -> str:
    """Build prompt for updating agent's memory after their turn."""
    recent_public = env.public_log[-10:] if len(env.public_log) > 10 else env.public_log
    recent_text = "\n".join(
        f"  [Round {e['round']}] {e['agent']}: {e['summary']}"
        for e in recent_public
    ) if recent_public else "  (nothing happened)"

    return f"""You just took an action in Round {env.round_num + 1}.

Your action: {json.dumps(action_taken)}

Recent events:
{recent_text}

Your current memory:
{agent.memory if agent.memory else "(empty)"}

---

Update your memory. Summarize what matters: alliances forming, threats, your strategy, who you trust/distrust, what rules are being proposed, what enforcements are active and how they affect you. Drop old details that no longer matter. Max 200 words. Respond with ONLY your updated memory text, nothing else."""
