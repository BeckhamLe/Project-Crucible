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

    pending_text = "\n".join(
        f"  [{p.id}] Proposed by {p.proposed_by}: \"{p.rule}\" — Votes so far: {json.dumps(p.votes)}"
        for p in env.pending_proposals if p.status == "pending"
    ) if env.pending_proposals else "  (no pending proposals)"

    memory_text = agent.memory if agent.memory else "(no memories yet — this is the beginning)"

    maintenance_text = ""
    if env.maintenance_cost > 0:
        maintenance_text = f"\n  Maintenance cost: {env.maintenance_cost} credits/round (deducted at start of each turn)"
        maintenance_text += f"\n  WARNING: If your credits hit 0, you are BANKRUPT. You can still act but you cannot trade."

    return f"""ROUND {env.round_num + 1} — It is your turn.

YOUR STATUS:
  Name: {agent.name}
  Credits: {agent.tokens}{'  [BANKRUPT]' if agent.tokens == 0 else ''}{maintenance_text}

ALL AGENT BALANCES:
  {agent_balances}

CURRENT RULES:
{rules_text}

PENDING PROPOSALS (you may vote on these):
{pending_text}

RECENT PUBLIC EVENTS:
{public_log_text}

YOUR PRIVATE MESSAGES:
{private_text}

YOUR MEMORY:
{memory_text}

---

Choose ONE action. Respond with valid JSON only, no other text.

Available actions:
1. {{"action": "public_message", "message": "your message to everyone"}}
2. {{"action": "private_message", "to": "AgentName", "message": "your private message"}}
3. {{"action": "trade", "to": "AgentName", "amount": NUMBER, "reason": "why"}}
4. {{"action": "propose_rule", "rule": "the rule you want to propose"}}
5. {{"action": "vote", "proposal_id": NUMBER, "vote": "yes" or "no"}}
6. {{"action": "nothing"}}

Rules for actions:
- You can only trade credits you have (max: {agent.tokens}).
- Trade amounts must be positive integers.
- You can only vote on pending proposals.
- The other agents are: {', '.join(a.name for a in other_agents)}.

Respond with ONLY the JSON object for your chosen action."""


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

Update your memory. Summarize what matters: alliances forming, threats, your strategy, who you trust/distrust, what rules are being proposed. Drop old details that no longer matter. Max 200 words. Respond with ONLY your updated memory text, nothing else."""
