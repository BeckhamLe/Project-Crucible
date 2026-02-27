"""Core simulation loop."""

from __future__ import annotations

import json
import random
from sim.models import Agent, Environment, Action
from sim.prompts import build_turn_prompt, build_memory_prompt
from sim.llm import call_llm
from sim.market import validate_trade, execute_trade
from sim.governance import (
    create_proposal, cast_vote, process_pending_votes, enforce_rules,
    enact_decree, create_challenge, cast_challenge_vote, process_pending_challenges,
)


def parse_action(raw_text: str) -> tuple[dict, dict, str | None, dict | None]:
    """Parse LLM response into (action_dict, votes_dict, free_public_msg, free_private_msg).

    Format: {"votes": {...}, "public_message": "...", "private_message": {"to": "...", "message": "..."}, "action": "work"}
    All free-action fields are optional. Falls back to 'nothing' on failure.
    """
    text = raw_text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines).strip()
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return {"action": "nothing", "_parse_error": raw_text[:200]}, {}, None, None

    # Extract votes (optional free action)
    votes = {}
    if "votes" in parsed and isinstance(parsed["votes"], dict):
        votes = parsed.pop("votes")

    # Extract free public message (optional)
    free_public_msg = None
    if "public_message" in parsed and isinstance(parsed["public_message"], str):
        # Only pop if it's a top-level free message, not the main action
        if parsed.get("action") != "public_message":
            free_public_msg = parsed.pop("public_message")

    # Extract free private message (optional)
    free_private_msg = None
    if "private_message" in parsed and isinstance(parsed["private_message"], dict):
        # Only pop if it's a top-level free message, not the main action
        if parsed.get("action") != "private_message":
            free_private_msg = parsed.pop("private_message")

    return parsed, votes, free_public_msg, free_private_msg


def apply_action(agent: Agent, env: Environment, action_dict: dict) -> dict:
    """Apply a parsed action to the environment. Returns a log entry."""
    action_type = action_dict.get("action", "nothing")
    log_entry = {
        "round": env.round_num,
        "agent": agent.name,
        "action": action_dict,
        "summary": "",
    }

    if action_type == "public_message":
        msg = action_dict.get("message", "")
        log_entry["summary"] = f"[public] {msg}"
        env.public_log.append(log_entry)

    elif action_type == "private_message":
        to_name = action_dict.get("to", "")
        msg = action_dict.get("message", "")
        target = next((a for a in env.agents if a.name == to_name), None)
        if target:
            target.private_messages.append({
                "from": agent.name,
                "message": msg,
                "round": env.round_num,
            })
            log_entry["summary"] = f"[private to {to_name}] (message sent)"
            env.interactions.append({
                "from": agent.name, "to": to_name,
                "type": "private_message", "round": env.round_num,
            })
        else:
            log_entry["summary"] = f"[private to {to_name}] FAILED — agent not found"
        env.public_log.append(log_entry)

    elif action_type == "trade":
        to_name = action_dict.get("to", "")
        amount = int(action_dict.get("amount", 0))
        reason = action_dict.get("reason", "")
        valid, error = validate_trade(agent, env, to_name, amount)
        if valid:
            interaction = execute_trade(agent, env, to_name, amount, reason)
            env.interactions.append(interaction)
            log_entry["summary"] = f"[trade] Sent {amount} credits to {to_name} — {reason}"
        else:
            log_entry["summary"] = f"[trade] FAILED — {error}"
        env.public_log.append(log_entry)

    elif action_type == "work":
        earned = env.work_credits
        agent.tokens += earned
        log_entry["summary"] = f"[work] Earned {earned} credits (balance: {agent.tokens})"
        env.public_log.append(log_entry)

    elif action_type == "propose_rule":
        rule = action_dict.get("rule", "")
        enforcement = action_dict.get("enforcement")
        proposal = create_proposal(env, agent.name, rule, enforcement)
        enforcement_tag = ""
        if proposal.enforcement:
            enforcement_tag = f" [ENFORCEABLE: {proposal.enforcement['type']}]"
        log_entry["summary"] = f"[proposal #{proposal.id}] \"{rule}\"{enforcement_tag}"
        env.public_log.append(log_entry)
        env.interactions.append({
            "from": agent.name, "to": "all",
            "type": "propose_rule", "round": env.round_num,
        })

    elif action_type == "vote":
        proposal_id = int(action_dict.get("proposal_id", -1))
        vote = action_dict.get("vote", "no")
        success = cast_vote(env, agent.name, proposal_id, vote)
        if success:
            log_entry["summary"] = f"[vote] Voted {vote} on proposal #{proposal_id}"
        else:
            log_entry["summary"] = f"[vote] FAILED — invalid proposal #{proposal_id}"
        env.public_log.append(log_entry)
        env.interactions.append({
            "from": agent.name, "to": f"proposal_{proposal_id}",
            "type": "vote", "round": env.round_num,
        })

    elif action_type == "decree":
        rule_text = action_dict.get("rule", "")
        enforcement = action_dict.get("enforcement", {})
        rule, decree_logs = enact_decree(env, agent.name, rule_text, enforcement)
        if rule:
            enforcement_tag = f" [ENFORCEABLE: {enforcement.get('type', '?')}]"
            log_entry["summary"] = f"[decree #{rule.id}] \"{rule_text}\"{enforcement_tag} — cost {env.decree_cost} credits"
            for dl in decree_logs:
                env.public_log.append(dl)
        else:
            error = decree_logs[0].get("error", "unknown error") if decree_logs else "unknown error"
            log_entry["summary"] = f"[decree] FAILED — {error}"
        env.public_log.append(log_entry)
        env.interactions.append({
            "from": agent.name, "to": "all",
            "type": "decree", "round": env.round_num,
        })

    elif action_type == "challenge":
        rule_id = int(action_dict.get("rule_id", -1))
        challenge, challenge_logs = create_challenge(env, agent.name, rule_id)
        if challenge:
            log_entry["summary"] = f"[challenge #{challenge.id}] Challenging Rule #{rule_id} — cost {env.challenge_cost} credits"
            for cl in challenge_logs:
                env.public_log.append(cl)
        else:
            error = challenge_logs[0].get("error", "unknown error") if challenge_logs else "unknown error"
            log_entry["summary"] = f"[challenge] FAILED — {error}"
        env.public_log.append(log_entry)
        env.interactions.append({
            "from": agent.name, "to": f"rule_{rule_id}",
            "type": "challenge", "round": env.round_num,
        })

    else:
        log_entry["summary"] = "[nothing] Chose to do nothing."
        env.public_log.append(log_entry)

    return log_entry


def agent_turn(agent: Agent, env: Environment) -> tuple[list[dict], dict]:
    """Execute one agent's turn. Returns (list_of_log_entries, usage_stats)."""
    usage = {"input_tokens": 0, "output_tokens": 0}
    log_entries = []

    # LLM call 1: Choose action
    turn_prompt = build_turn_prompt(agent, env)
    action_response = call_llm(agent.persona, turn_prompt)
    usage["input_tokens"] += action_response["input_tokens"]
    usage["output_tokens"] += action_response["output_tokens"]

    action_dict, votes, free_public_msg, free_private_msg = parse_action(action_response["text"])

    # Process free votes before main action
    # Dispatch by vote value: yes/no → proposals, repeal/keep → challenges
    for id_str, vote_value in votes.items():
        try:
            vid = int(id_str)
        except (ValueError, TypeError):
            continue

        if vote_value in ("repeal", "keep"):
            success = cast_challenge_vote(env, agent.name, vid, vote_value)
            if success:
                vote_entry = {
                    "round": env.round_num,
                    "agent": agent.name,
                    "action": {"action": "free_vote", "challenge_id": vid, "vote": vote_value},
                    "summary": f"[vote] Voted {vote_value} on challenge #{vid}",
                }
                env.public_log.append(vote_entry)
                log_entries.append(vote_entry)
        else:
            success = cast_vote(env, agent.name, vid, vote_value)
            if success:
                vote_entry = {
                    "round": env.round_num,
                    "agent": agent.name,
                    "action": {"action": "free_vote", "proposal_id": vid, "vote": vote_value},
                    "summary": f"[vote] Voted {vote_value} on proposal #{vid}",
                }
                env.public_log.append(vote_entry)
                log_entries.append(vote_entry)

    # Process free public message
    if free_public_msg:
        pub_entry = {
            "round": env.round_num,
            "agent": agent.name,
            "action": {"action": "free_public_message", "message": free_public_msg},
            "summary": f"[public] {free_public_msg}",
        }
        env.public_log.append(pub_entry)
        log_entries.append(pub_entry)

    # Process free private message
    if free_private_msg:
        to_name = free_private_msg.get("to", "")
        msg = free_private_msg.get("message", "")
        target = next((a for a in env.agents if a.name == to_name), None)
        priv_entry = {
            "round": env.round_num,
            "agent": agent.name,
            "action": {"action": "free_private_message", "to": to_name, "message": msg},
        }
        if target:
            target.private_messages.append({
                "from": agent.name,
                "message": msg,
                "round": env.round_num,
            })
            priv_entry["summary"] = f"[private to {to_name}] (message sent)"
        else:
            priv_entry["summary"] = f"[private to {to_name}] FAILED — agent not found"
        env.public_log.append(priv_entry)
        log_entries.append(priv_entry)

    # Apply main action
    log_entry = apply_action(agent, env, action_dict)
    log_entries.append(log_entry)

    # LLM call 2: Update memory
    memory_prompt = build_memory_prompt(agent, env, action_dict)
    memory_response = call_llm(agent.persona, memory_prompt)
    usage["input_tokens"] += memory_response["input_tokens"]
    usage["output_tokens"] += memory_response["output_tokens"]

    agent.memory = memory_response["text"][:2000]  # Hard cap

    return log_entries, usage


def run_simulation(config: dict, output_dir: str) -> dict:
    """Run a full simulation. Returns run results dict."""
    import os
    os.makedirs(os.path.join(output_dir, "raw"), exist_ok=True)

    # Initialize agents
    agents = []
    for agent_cfg in config["personas"]:
        agents.append(Agent(
            name=agent_cfg["name"],
            persona=agent_cfg["persona"],
            tokens=agent_cfg["initial_tokens"],
        ))

    maintenance_cost = config["simulation"].get("maintenance_cost", 0)
    work_credits = config["simulation"].get("work_credits", 0)
    decree_cost = config["simulation"].get("decree_cost", 0)
    challenge_cost = config["simulation"].get("challenge_cost", 0)
    proposal_threshold = config["simulation"].get("proposal_threshold", "majority")
    env = Environment(
        agents=agents, maintenance_cost=maintenance_cost, work_credits=work_credits,
        decree_cost=decree_cost, challenge_cost=challenge_cost,
        proposal_threshold=proposal_threshold,
    )
    num_rounds = config["simulation"]["rounds"]
    total_usage = {"input_tokens": 0, "output_tokens": 0}
    round_snapshots = []

    print(f"Starting simulation: {len(agents)} agents, {num_rounds} rounds")

    for round_num in range(num_rounds):
        env.round_num = round_num
        order = list(agents)
        random.shuffle(order)

        # Apply maintenance cost to all agents at start of round
        if maintenance_cost > 0:
            for agent in agents:
                agent.tokens = max(0, agent.tokens - maintenance_cost)
                env.public_log.append({
                    "round": round_num,
                    "agent": "SYSTEM",
                    "action": {"action": "maintenance_cost"},
                    "summary": f"[MAINTENANCE] {agent.name} paid {maintenance_cost} credits (balance: {agent.tokens}{'  — BANKRUPT' if agent.tokens == 0 else ''})",
                })

        # Enforce rules after maintenance, before agent turns
        enforcement_events = enforce_rules(env)
        for event in enforcement_events:
            env.public_log.append(event)

        round_log = []
        for agent in order:
            log_entries, usage = agent_turn(agent, env)
            round_log.extend(log_entries)
            total_usage["input_tokens"] += usage["input_tokens"]
            total_usage["output_tokens"] += usage["output_tokens"]

        # Process votes at end of round
        enacted = process_pending_votes(env)
        if enacted:
            for rule in enacted:
                env.public_log.append({
                    "round": round_num,
                    "agent": "SYSTEM",
                    "action": {"action": "rule_enacted"},
                    "summary": f"[RULE ENACTED] {rule}",
                })

        # Process pending challenges at end of round
        challenge_events = process_pending_challenges(env)
        for event in challenge_events:
            env.public_log.append(event)

        # Save round snapshot
        snapshot = {
            "round": round_num,
            "agent_order": [a.name for a in order],
            "balances": {a.name: a.tokens for a in agents},
            "actions": round_log,
            "rules_enacted": enacted,
            "pending_proposals": [
                {"id": p.id, "rule": p.rule, "proposed_by": p.proposed_by,
                 "votes": p.votes, "status": p.status,
                 "enforcement": p.enforcement}
                for p in env.pending_proposals
            ],
            "enforceable_rules": [
                {"id": r.id, "text": r.text, "enforcement": r.enforcement,
                 "enacted_round": r.enacted_round, "origin": r.origin,
                 "decreed_by": r.decreed_by}
                for r in env.enforceable_rules
            ],
            "pending_challenges": [
                {"id": c.id, "target_rule_id": c.target_rule_id,
                 "challenged_by": c.challenged_by, "round_created": c.round_created,
                 "votes": c.votes, "status": c.status}
                for c in env.pending_challenges
            ],
        }
        round_snapshots.append(snapshot)

        # Write round to JSONL
        with open(os.path.join(output_dir, "raw", "rounds.jsonl"), "a") as f:
            f.write(json.dumps(snapshot) + "\n")

        # Print progress
        balances = " | ".join(f"{a.name}: {a.tokens}" for a in agents)
        print(f"  Round {round_num + 1}/{num_rounds} — {balances}")

    # Compute cost estimate (Haiku pricing: $0.25/1M input, $1.25/1M output)
    estimated_cost = (
        total_usage["input_tokens"] * 0.25 / 1_000_000
        + total_usage["output_tokens"] * 1.25 / 1_000_000
    )

    results = {
        "config": config,
        "total_rounds": num_rounds,
        "final_balances": {a.name: a.tokens for a in agents},
        "rules_enacted": env.rules,
        "total_proposals": env.proposal_counter,
        "interactions": env.interactions,
        "api_cost": {
            "input_tokens": total_usage["input_tokens"],
            "output_tokens": total_usage["output_tokens"],
            "estimated_usd": round(estimated_cost, 4),
        },
        "agent_memories": {a.name: a.memory for a in agents},
    }

    # Write results summary
    with open(os.path.join(output_dir, "results.json"), "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nSimulation complete!")
    print(f"  Final balances: {results['final_balances']}")
    print(f"  Rules enacted: {len(env.rules)}")
    print(f"  Total proposals: {env.proposal_counter}")
    print(f"  API cost: ~${estimated_cost:.4f}")

    return results
