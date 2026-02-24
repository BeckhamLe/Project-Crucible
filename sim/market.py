"""Token trading mechanics."""

from __future__ import annotations

from sim.models import Agent, Environment


def validate_trade(agent: Agent, env: Environment, to_name: str, amount: int) -> tuple[bool, str]:
    """Validate a trade. Returns (is_valid, error_message)."""
    if amount <= 0:
        return False, "Trade amount must be positive."
    if amount > agent.tokens:
        return False, f"{agent.name} has {agent.tokens} credits but tried to trade {amount}."
    target = next((a for a in env.agents if a.name == to_name), None)
    if target is None:
        return False, f"Agent '{to_name}' does not exist."
    if target.name == agent.name:
        return False, "Cannot trade with yourself."
    return True, ""


def execute_trade(agent: Agent, env: Environment, to_name: str, amount: int, reason: str) -> dict:
    """Execute a validated trade. Returns interaction record."""
    target = next(a for a in env.agents if a.name == to_name)
    agent.tokens -= amount
    target.tokens += amount
    return {
        "from": agent.name,
        "to": to_name,
        "type": "trade",
        "amount": amount,
        "reason": reason,
        "round": env.round_num,
    }
