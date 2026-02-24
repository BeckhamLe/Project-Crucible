"""Rule formation and voting mechanics."""

from __future__ import annotations

from sim.models import Environment, Proposal


def create_proposal(env: Environment, proposed_by: str, rule: str) -> Proposal:
    """Create a new rule proposal."""
    proposal = Proposal(
        id=env.proposal_counter,
        proposed_by=proposed_by,
        rule=rule,
        round_proposed=env.round_num,
    )
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


def process_pending_votes(env: Environment) -> list[str]:
    """Check all pending proposals. Majority yes = passed. Returns list of newly enacted rules."""
    num_agents = len(env.agents)
    threshold = num_agents / 2  # Simple majority
    enacted = []

    for proposal in env.pending_proposals:
        if proposal.status != "pending":
            continue
        # Only resolve if all agents have voted OR proposal is 2+ rounds old
        all_voted = len(proposal.votes) >= num_agents
        expired = (env.round_num - proposal.round_proposed) >= 2

        if all_voted or expired:
            yes_votes = sum(1 for v in proposal.votes.values() if v == "yes")
            if yes_votes > threshold:
                proposal.status = "passed"
                env.rules.append(proposal.rule)
                enacted.append(proposal.rule)
            else:
                proposal.status = "failed"

    return enacted
