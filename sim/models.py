from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Action:
    type: str  # "public_message" | "private_message" | "trade" | "propose_rule" | "vote" | "nothing"
    payload: dict = field(default_factory=dict)
    # payload examples:
    #   public_message:  {"message": "..."}
    #   private_message: {"to": "Judge", "message": "..."}
    #   trade:           {"to": "Builder", "amount": 3, "reason": "..."}
    #   propose_rule:    {"rule": "Each agent must contribute 1 credit per round to a shared pool"}
    #   vote:            {"proposal_id": 0, "vote": "yes" | "no"}
    #   nothing:         {}


@dataclass
class EnforceableRule:
    id: int  # Same as the proposal ID that created it
    text: str  # Human-readable rule text
    enforcement: dict  # {"type": "tax"|"sanction"|"repeal", ...params}
    enacted_round: int
    origin: str = "proposal"  # "proposal" | "decree"
    decreed_by: str | None = None  # agent name if decree


@dataclass
class Challenge:
    id: int  # Shares proposal_counter for unique IDs
    target_rule_id: int
    challenged_by: str
    round_created: int
    votes: dict = field(default_factory=dict)  # {name: "repeal"/"keep"}
    status: str = "pending"  # "pending" | "repealed" | "sustained"


@dataclass
class Proposal:
    id: int
    proposed_by: str
    rule: str
    round_proposed: int
    votes: dict = field(default_factory=dict)  # {agent_name: "yes"/"no"}
    status: str = "pending"  # "pending" | "passed" | "failed"
    enforcement: Optional[dict] = None  # Structured enforcement params, or None for advisory


@dataclass
class Agent:
    name: str
    persona: str  # System prompt defining personality/ideology
    tokens: int = 10
    memory: str = ""  # Rolling summary of recent events (max 500 words)
    private_messages: list = field(default_factory=list)  # Messages only this agent sees


@dataclass
class Environment:
    agents: list = field(default_factory=list)
    public_log: list = field(default_factory=list)  # All public events
    rules: list = field(default_factory=list)  # Enacted rules (strings) — advisory + backward compat
    enforceable_rules: list = field(default_factory=list)  # List of EnforceableRule objects
    pending_proposals: list = field(default_factory=list)  # List of Proposal objects
    proposal_counter: int = 0
    round_num: int = 0
    interactions: list = field(default_factory=list)  # [{from, to, type, round}] for network analysis
    maintenance_cost: int = 0  # Credits deducted per agent per round
    work_credits: int = 0  # Credits earned per work action
    pending_challenges: list = field(default_factory=list)  # List of Challenge objects
    decree_cost: int = 0  # 0 = disabled
    challenge_cost: int = 0  # 0 = disabled
