"""Core simulation loop."""

from __future__ import annotations

import json
import random
from sim.models import Agent, Environment, Action
from sim.prompts import build_turn_prompt, build_memory_prompt
from sim.llm import call_llm
from sim.market import validate_trade, execute_trade
from sim.governance import create_proposal, cast_vote, process_pending_votes


def parse_action(raw_text: str) -> dict:
    """Parse LLM response into an action dict. Falls back to 'nothing' on failure."""
    text = raw_text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"action": "nothing", "_parse_error": raw_text[:200]}


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

    elif action_type == "propose_rule":
        rule = action_dict.get("rule", "")
        proposal = create_proposal(env, agent.name, rule)
        log_entry["summary"] = f"[proposal #{proposal.id}] \"{rule}\""
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

    else:
        log_entry["summary"] = "[nothing] Chose to do nothing."
        env.public_log.append(log_entry)

    return log_entry


def agent_turn(agent: Agent, env: Environment) -> tuple[dict, dict]:
    """Execute one agent's turn. Returns (action_log_entry, usage_stats)."""
    usage = {"input_tokens": 0, "output_tokens": 0}

    # LLM call 1: Choose action
    turn_prompt = build_turn_prompt(agent, env)
    action_response = call_llm(agent.persona, turn_prompt)
    usage["input_tokens"] += action_response["input_tokens"]
    usage["output_tokens"] += action_response["output_tokens"]

    action_dict = parse_action(action_response["text"])
    log_entry = apply_action(agent, env, action_dict)

    # LLM call 2: Update memory
    memory_prompt = build_memory_prompt(agent, env, action_dict)
    memory_response = call_llm(agent.persona, memory_prompt)
    usage["input_tokens"] += memory_response["input_tokens"]
    usage["output_tokens"] += memory_response["output_tokens"]

    agent.memory = memory_response["text"][:2000]  # Hard cap

    return log_entry, usage


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

    env = Environment(agents=agents)
    num_rounds = config["simulation"]["rounds"]
    total_usage = {"input_tokens": 0, "output_tokens": 0}
    round_snapshots = []

    print(f"Starting simulation: {len(agents)} agents, {num_rounds} rounds")

    for round_num in range(num_rounds):
        env.round_num = round_num
        order = list(agents)
        random.shuffle(order)

        round_log = []
        for agent in order:
            log_entry, usage = agent_turn(agent, env)
            round_log.append(log_entry)
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

        # Save round snapshot
        snapshot = {
            "round": round_num,
            "agent_order": [a.name for a in order],
            "balances": {a.name: a.tokens for a in agents},
            "actions": round_log,
            "rules_enacted": enacted,
            "pending_proposals": [
                {"id": p.id, "rule": p.rule, "proposed_by": p.proposed_by,
                 "votes": p.votes, "status": p.status}
                for p in env.pending_proposals
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
