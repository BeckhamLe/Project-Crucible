"""Post-run narrative generation for Project Crucible.

Generates two observability outputs from rounds.jsonl:
1. Per-agent narrative summaries (agent_summaries.md)
2. Rule proposal & enactment log (rule_log.md)
"""

from __future__ import annotations

import json
import os
import sys
from collections import defaultdict


def load_rounds(results_dir: str) -> list[dict]:
    """Load all round snapshots from rounds.jsonl."""
    rounds = []
    rounds_file = os.path.join(results_dir, "raw", "rounds.jsonl")
    with open(rounds_file) as f:
        for line in f:
            if line.strip():
                rounds.append(json.loads(line))
    return rounds


def _truncate(text: str, max_len: int = 120) -> str:
    """Truncate text with ellipsis."""
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."


def _action_type(action_dict: dict) -> str:
    """Extract the action type from an action's inner dict."""
    return action_dict.get("action", {}).get("action", "unknown")


# ---------------------------------------------------------------------------
# Agent Summaries
# ---------------------------------------------------------------------------

def _extract_agent_actions(rounds: list[dict]) -> dict[str, list[dict]]:
    """Group actions by agent across all rounds. Each entry has round number."""
    by_agent = defaultdict(list)
    for rd in rounds:
        for act in rd.get("actions", []):
            agent = act["agent"]
            by_agent[agent].append({
                "round": rd["round"],
                "action": act["action"],
                "summary": act.get("summary", ""),
            })
    return dict(by_agent)


def _extract_votes(rounds: list[dict]) -> dict[str, list[dict]]:
    """Track when each agent's vote first appears on each proposal."""
    # For each proposal, track which round each agent's vote was first seen
    seen_votes: dict[int, dict[str, int]] = {}  # proposal_id -> {agent: first_round}
    agent_votes: dict[str, list[dict]] = defaultdict(list)

    for rd in rounds:
        for prop in rd.get("pending_proposals", []):
            pid = prop["id"]
            if pid not in seen_votes:
                seen_votes[pid] = {}
            for agent, vote in prop.get("votes", {}).items():
                if agent not in seen_votes[pid]:
                    seen_votes[pid][agent] = rd["round"]
                    agent_votes[agent].append({
                        "round": rd["round"],
                        "proposal_id": pid,
                        "vote": vote,
                        "proposer": prop["proposed_by"],
                        "rule_text": _truncate(prop["rule"], 80),
                    })
    return dict(agent_votes)


def _balance_trajectory(rounds: list[dict], agent: str) -> list[tuple[int, int]]:
    """Return (round, balance) pairs for an agent."""
    trajectory = []
    for rd in rounds:
        bal = rd.get("balances", {}).get(agent)
        if bal is not None:
            trajectory.append((rd["round"], bal))
    return trajectory


def _compute_agent_profile(agent: str, actions: list[dict], votes: list[dict],
                            all_votes: dict[str, list[dict]], rounds: list[dict],
                            all_agents: list[str]) -> dict:
    """Compute behavioral signals for one agent."""
    total_rounds = len(rounds)

    # Action type counts
    type_counts = defaultdict(int)
    for act in actions:
        atype = act["action"].get("action", "unknown")
        type_counts[atype] += 1

    # Primary strategy (what they spent most turns on)
    governance_turns = type_counts.get("propose_rule", 0) + type_counts.get("public_message", 0) + type_counts.get("private_message", 0)
    work_turns = type_counts.get("work", 0)
    nothing_turns = type_counts.get("nothing", 0)

    # Proposal stats
    proposals_made = [a for a in actions if a["action"].get("action") == "propose_rule"]
    proposals_by_agent = _track_proposals_for_agent(agent, rounds)
    passed_own = sum(1 for p in proposals_by_agent if p["status"] == "passed")
    failed_own = sum(1 for p in proposals_by_agent if p["status"] == "failed")

    # Voting alignment — who do they agree with?
    alignment = defaultdict(lambda: {"agree": 0, "disagree": 0})
    all_proposals = {}
    for rd in rounds:
        for prop in rd.get("pending_proposals", []):
            if prop["id"] not in all_proposals:
                all_proposals[prop["id"]] = {}
            for a, v in prop.get("votes", {}).items():
                if a not in all_proposals[prop["id"]]:
                    all_proposals[prop["id"]][a] = v

    for pid, vote_map in all_proposals.items():
        if agent not in vote_map:
            continue
        my_vote = vote_map[agent]
        for other, their_vote in vote_map.items():
            if other == agent:
                continue
            if my_vote == their_vote:
                alignment[other]["agree"] += 1
            else:
                alignment[other]["disagree"] += 1

    # How often did they block others' proposals (voted no on proposals by others)?
    blocked_others = defaultdict(int)
    supported_others = defaultdict(int)
    for v in votes:
        if v["proposer"] != agent:
            if v["vote"] == "no":
                blocked_others[v["proposer"]] += 1
            else:
                supported_others[v["proposer"]] += 1

    # Private messaging targets
    private_targets = defaultdict(int)
    for act in actions:
        if act["action"].get("action") == "private_message":
            private_targets[act["action"].get("to", "?")] += 1

    # Enforcement types proposed
    enf_types = defaultdict(int)
    for act in actions:
        if act["action"].get("action") == "propose_rule":
            enf = act["action"].get("enforcement")
            if enf:
                enf_types[enf["type"]] += 1
            else:
                enf_types["advisory"] += 1

    # Parse errors (failed to produce valid JSON)
    parse_errors = sum(1 for act in actions if act["action"].get("_parse_error"))

    return {
        "type_counts": dict(type_counts),
        "governance_turns": governance_turns,
        "work_turns": work_turns,
        "nothing_turns": nothing_turns,
        "proposals_made": len(proposals_made),
        "proposals_passed": passed_own,
        "proposals_failed": failed_own,
        "alignment": dict(alignment),
        "blocked_others": dict(blocked_others),
        "supported_others": dict(supported_others),
        "private_targets": dict(private_targets),
        "enf_types": dict(enf_types),
        "parse_errors": parse_errors,
        "total_rounds": total_rounds,
    }


def _track_proposals_for_agent(agent: str, rounds: list[dict]) -> list[dict]:
    """Get all proposals made by a specific agent."""
    seen = {}
    for rd in rounds:
        for prop in rd.get("pending_proposals", []):
            if prop["proposed_by"] == agent and prop["id"] not in seen:
                seen[prop["id"]] = {"status": prop["status"]}
            if prop["id"] in seen:
                seen[prop["id"]]["status"] = prop["status"]
    return list(seen.values())


def _generate_behavioral_narrative(agent: str, profile: dict, traj: list[tuple[int, int]],
                                    all_agents: list[str]) -> list[str]:
    """Generate a readable behavioral analysis paragraph from computed signals."""
    lines = []
    p = profile
    total = p["total_rounds"]

    # --- Strategy characterization ---
    work_pct = round(100 * p["work_turns"] / total)
    gov_pct = round(100 * p["governance_turns"] / total)

    if work_pct >= 50:
        strategy = f"Primarily a **worker** — spent {work_pct}% of turns on work and {gov_pct}% on governance (messaging + proposals)."
    elif gov_pct >= 50:
        strategy = f"Primarily a **politician** — spent {gov_pct}% of turns on governance (messaging + proposals) and only {work_pct}% working."
    else:
        strategy = f"**Mixed strategy** — {work_pct}% work, {gov_pct}% governance, {round(100 * p['nothing_turns'] / total)}% idle/parse errors."
    lines.append(strategy)

    # --- Proposal effectiveness ---
    if p["proposals_made"] > 0:
        win_rate = round(100 * p["proposals_passed"] / p["proposals_made"])
        enf_summary = ", ".join(f"{c} {t}" for t, c in sorted(p["enf_types"].items(), key=lambda x: -x[1]))
        lines.append(f"Proposed {p['proposals_made']} rules ({enf_summary}), {p['proposals_passed']} passed, "
                      f"{p['proposals_failed']} failed ({win_rate}% success rate).")

    # --- Coalition / alignment ---
    if p["alignment"]:
        ally = max(p["alignment"], key=lambda a: p["alignment"][a]["agree"])
        rival = max(p["alignment"], key=lambda a: p["alignment"][a]["disagree"])
        ally_agree = p["alignment"][ally]["agree"]
        ally_disagree = p["alignment"][ally]["disagree"]
        rival_agree = p["alignment"][rival]["agree"]
        rival_disagree = p["alignment"][rival]["disagree"]

        if ally == rival:
            # Only one other agent, or same person is both
            lines.append(f"Voted with {ally} {ally_agree} times and against them {ally_disagree} times.")
        else:
            lines.append(f"**Closest ally**: {ally} (agreed {ally_agree} times, disagreed {ally_disagree}). "
                          f"**Main rival**: {rival} (disagreed {rival_disagree} times, agreed {rival_agree}).")

    # --- Blocking behavior ---
    if p["blocked_others"]:
        blocks = ", ".join(f"{target} ({count}x)" for target, count in
                           sorted(p["blocked_others"].items(), key=lambda x: -x[1]))
        lines.append(f"Voted NO against proposals by: {blocks}.")

    if p["supported_others"]:
        supports = ", ".join(f"{target} ({count}x)" for target, count in
                              sorted(p["supported_others"].items(), key=lambda x: -x[1]))
        lines.append(f"Voted YES on proposals by: {supports}.")

    # --- Private coordination ---
    if p["private_targets"]:
        targets = ", ".join(f"{t} ({c}x)" for t, c in p["private_targets"].items())
        lines.append(f"Sent private messages to: {targets} — indicates behind-the-scenes coordination.")

    # --- Parse errors ---
    if p["parse_errors"] > 0:
        lines.append(f"Had {p['parse_errors']} parse errors (turns lost to malformed JSON output).")

    # --- Economic arc ---
    if traj:
        start = traj[0][1]
        end = traj[-1][1]
        peak = max(b for _, b in traj)
        trough = min(b for _, b in traj)
        peak_round = next(r for r, b in traj if b == peak)
        trough_round = next(r for r, b in traj if b == trough)

        if end < start:
            delta = start - end
            lines.append(f"Lost {delta} credits over the game (peak: {peak} at round {peak_round}, "
                          f"low: {trough} at round {trough_round}).")
        elif end > start:
            delta = end - start
            lines.append(f"Gained {delta} credits over the game (peak: {peak} at round {peak_round}, "
                          f"low: {trough} at round {trough_round}).")
        else:
            lines.append(f"Ended where they started. Peak: {peak} at round {peak_round}, "
                          f"low: {trough} at round {trough_round}.")

    return lines


def generate_agent_summaries(results_dir: str) -> str:
    """Generate per-agent behavioral summaries. Returns path to output file."""
    rounds = load_rounds(results_dir)
    if not rounds:
        raise ValueError(f"No rounds found in {results_dir}")

    actions_by_agent = _extract_agent_actions(rounds)
    votes_by_agent = _extract_votes(rounds)
    agents = sorted(actions_by_agent.keys())

    total_rounds = len(rounds)

    lines = ["# Agent Summaries\n"]

    # Load config for starting credits if available
    config_path = os.path.join(results_dir, "config_snapshot.json")
    starting_credits = {}
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = json.load(f)
        for a in config.get("agents", []):
            starting_credits[a["name"]] = a.get("credits", "?")

    for agent in agents:
        traj = _balance_trajectory(rounds, agent)
        start_bal = starting_credits.get(agent, traj[0][1] if traj else "?")
        end_bal = traj[-1][1] if traj else "?"

        lines.append(f"## {agent}")
        lines.append(f"**Credits**: {start_bal} → {end_bal}")
        lines.append("")

        # Action type counts
        type_counts = defaultdict(int)
        for act in actions_by_agent[agent]:
            atype = act["action"].get("action", "unknown")
            type_counts[atype] += 1
        count_str = ", ".join(f"{t}: {c}" for t, c in sorted(type_counts.items(), key=lambda x: -x[1]))
        lines.append(f"**Action breakdown**: {count_str}")
        lines.append("")

        # Compute behavioral profile
        profile = _compute_agent_profile(
            agent, actions_by_agent[agent], votes_by_agent.get(agent, []),
            votes_by_agent, rounds, agents,
        )

        # Generate narrative
        lines.append("### Behavioral Profile")
        narrative = _generate_behavioral_narrative(agent, profile, traj, agents)
        for line in narrative:
            lines.append(line)
        lines.append("")

        # Compact phase timeline (just balance arc + counts, not every action)
        phase_bounds = [
            ("Early", 0, 9),
            ("Mid", 10, 19),
            ("Late", 20, total_rounds - 1),
        ]
        lines.append("### Phase Timeline")
        lines.append("| Phase | Balance | Work | Governance | Proposals |")
        lines.append("|-------|---------|------|------------|-----------|")
        for phase_name, lo, hi in phase_bounds:
            phase_traj = [(r, b) for r, b in traj if lo <= r <= hi]
            if not phase_traj:
                continue
            bal_str = f"{phase_traj[0][1]} → {phase_traj[-1][1]}"
            phase_acts = [a for a in actions_by_agent[agent] if lo <= a["round"] <= hi]
            work_c = sum(1 for a in phase_acts if a["action"].get("action") == "work")
            gov_c = sum(1 for a in phase_acts if a["action"].get("action") in
                        ("public_message", "private_message", "propose_rule"))
            prop_c = sum(1 for a in phase_acts if a["action"].get("action") == "propose_rule")
            lines.append(f"| {phase_name} (r{lo}-{hi}) | {bal_str} | {work_c} | {gov_c} | {prop_c} |")
        lines.append("")

    output = "\n".join(lines)
    out_path = os.path.join(results_dir, "agent_summaries.md")
    with open(out_path, "w") as f:
        f.write(output)

    print(f"Agent summaries written to {out_path}")
    return out_path


# ---------------------------------------------------------------------------
# Rule Proposal & Enactment Log
# ---------------------------------------------------------------------------

def _track_proposals(rounds: list[dict]) -> list[dict]:
    """Build a chronological list of proposals with full lifecycle info."""
    proposals = {}  # id -> proposal dict with extra tracking

    for rd in rounds:
        for prop in rd.get("pending_proposals", []):
            pid = prop["id"]
            if pid not in proposals:
                # First appearance — record the round it was proposed
                proposals[pid] = {
                    "id": pid,
                    "proposed_round": rd["round"],
                    "proposed_by": prop["proposed_by"],
                    "rule_text": prop["rule"],
                    "enforcement": prop.get("enforcement"),
                    "votes": {},
                    "status": prop["status"],
                    "resolved_round": None,
                }

            # Update votes and status
            for agent, vote in prop.get("votes", {}).items():
                if agent not in proposals[pid]["votes"]:
                    proposals[pid]["votes"][agent] = vote
            proposals[pid]["status"] = prop["status"]

            # Track when it resolved
            if prop["status"] in ("passed", "failed") and proposals[pid]["resolved_round"] is None:
                proposals[pid]["resolved_round"] = rd["round"]

    return sorted(proposals.values(), key=lambda p: (p["proposed_round"], p["id"]))


def _track_enforcement_activity(rounds: list[dict]) -> dict[int, list[int]]:
    """Track which rounds each enforceable rule was active."""
    active_rounds: dict[int, list[int]] = defaultdict(list)
    for rd in rounds:
        for rule in rd.get("enforceable_rules", []):
            active_rounds[rule["id"]].append(rd["round"])
    return dict(active_rounds)


def generate_rule_log(results_dir: str) -> str:
    """Generate rule proposal & enactment log. Returns path to output file."""
    rounds = load_rounds(results_dir)
    if not rounds:
        raise ValueError(f"No rounds found in {results_dir}")

    proposals = _track_proposals(rounds)
    enforcement_activity = _track_enforcement_activity(rounds)

    lines = ["# Rule Proposal & Enactment Log\n"]

    # Summary stats
    total = len(proposals)
    passed = sum(1 for p in proposals if p["status"] == "passed")
    failed = sum(1 for p in proposals if p["status"] == "failed")
    enforceable = sum(1 for p in proposals if p["status"] == "passed" and p["enforcement"])
    lines.append(f"**Total proposals**: {total} | **Passed**: {passed} | **Failed**: {failed} | "
                 f"**Enforceable**: {enforceable}")
    lines.append("")

    # Table header
    lines.append("| # | Round | Proposer | Rule | Enforcement | Votes | Status | Active Rounds |")
    lines.append("|---|-------|----------|------|-------------|-------|--------|---------------|")

    for prop in proposals:
        pid = prop["id"]
        rd = prop["proposed_round"]
        proposer = prop["proposed_by"]
        rule = _truncate(prop["rule_text"], 60)
        enf = prop["enforcement"]

        # Format enforcement
        if enf:
            etype = enf["type"]
            if etype == "tax":
                enf_str = f"tax (>{enf['threshold']}, -{enf['amount']})"
            elif etype == "sanction":
                enf_str = f"sanction ({enf.get('target', '?')}, -{enf.get('amount', '?')})"
            elif etype == "repeal":
                enf_str = f"repeal (rule #{enf.get('rule_id', '?')})"
            else:
                enf_str = etype
        else:
            enf_str = "advisory"

        # Format votes
        yes_agents = [a for a, v in prop["votes"].items() if v == "yes"]
        no_agents = [a for a, v in prop["votes"].items() if v == "no"]
        vote_str = f"Y: {','.join(yes_agents)} / N: {','.join(no_agents)}"

        # Status
        status = prop["status"].upper()

        # Active rounds for enforcement
        if pid in enforcement_activity and prop["status"] == "passed":
            active = enforcement_activity[pid]
            active_str = f"rounds {min(active)}-{max(active)} ({len(active)} rounds)"
        else:
            active_str = "—"

        lines.append(f"| {pid} | {rd} | {proposer} | {rule} | {enf_str} | {vote_str} | {status} | {active_str} |")

    # Detailed entries below the table
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Proposal Details\n")

    for prop in proposals:
        pid = prop["id"]
        status_emoji = "PASSED" if prop["status"] == "passed" else "FAILED"
        lines.append(f"### Proposal #{pid} [{status_emoji}]")
        lines.append(f"**Proposed by**: {prop['proposed_by']} (round {prop['proposed_round']})")
        if prop["resolved_round"] is not None:
            lines.append(f"**Resolved**: round {prop['resolved_round']}")

        # Full rule text
        lines.append(f"\n> {prop['rule_text']}\n")

        # Enforcement details
        enf = prop["enforcement"]
        if enf:
            lines.append(f"**Enforcement**: `{json.dumps(enf)}`")
        else:
            lines.append("**Enforcement**: None (advisory)")

        # Vote breakdown
        lines.append("")
        lines.append("| Agent | Vote |")
        lines.append("|-------|------|")
        for agent, vote in sorted(prop["votes"].items()):
            marker = "auto" if agent == prop["proposed_by"] else ""
            lines.append(f"| {agent} | {vote} {marker} |")

        # Enforcement activity
        if pid in enforcement_activity and prop["status"] == "passed":
            active = enforcement_activity[pid]
            lines.append(f"\n**Enforcement active**: rounds {min(active)}-{max(active)} ({len(active)} rounds)")
        elif prop["status"] == "passed" and not enf:
            lines.append("\n**Enforcement**: Advisory only — no automatic execution")

        lines.append("")

    output = "\n".join(lines)
    out_path = os.path.join(results_dir, "rule_log.md")
    with open(out_path, "w") as f:
        f.write(output)

    print(f"Rule log written to {out_path}")
    return out_path


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def generate_all(results_dir: str) -> None:
    """Generate both narrative outputs for a run."""
    generate_agent_summaries(results_dir)
    generate_rule_log(results_dir)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m analysis.narrative <results_dir>")
        print("Example: python -m analysis.narrative results/poc_003")
        sys.exit(1)
    generate_all(sys.argv[1])
