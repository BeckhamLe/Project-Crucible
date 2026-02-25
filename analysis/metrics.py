"""Post-run analysis metrics for Project Crucible."""

from __future__ import annotations

import json
import numpy as np
import networkx as nx
from collections import defaultdict


def gini_coefficient(values: list[int]) -> float:
    """Compute Gini coefficient. 0 = perfect equality, 1 = perfect inequality."""
    values = sorted(values)
    n = len(values)
    if n == 0 or sum(values) == 0:
        return 0.0
    cumulative = np.cumsum(values)
    return (2 * np.sum((np.arange(1, n + 1) * values)) - (n + 1) * np.sum(values)) / (n * np.sum(values))


def build_communication_graph(interactions: list[dict]) -> nx.DiGraph:
    """Build a directed graph from interaction records."""
    G = nx.DiGraph()
    edge_weights = defaultdict(int)
    # Solo action types that don't represent agent-to-agent interactions
    solo_types = {"work"}
    for interaction in interactions:
        if interaction.get("type") in solo_types:
            continue
        frm = interaction["from"]
        to = interaction["to"]
        if to == "all":
            continue  # Skip broadcasts for direct graph
        edge_weights[(frm, to)] += 1

    for (frm, to), weight in edge_weights.items():
        G.add_edge(frm, to, weight=weight)

    return G


def network_metrics(G: nx.DiGraph) -> dict:
    """Compute network analysis metrics."""
    if len(G.nodes) == 0:
        return {"betweenness": {}, "clustering": {}, "density": 0}

    return {
        "betweenness_centrality": nx.betweenness_centrality(G),
        "clustering_coefficient": nx.clustering(G.to_undirected()),
        "density": nx.density(G),
        "in_degree": dict(G.in_degree(weight="weight")),
        "out_degree": dict(G.out_degree(weight="weight")),
    }


def classify_governance(rules: list[str], proposals_total: int, balances: dict) -> str:
    """Rough classification of what governance emerged."""
    if len(rules) == 0 and proposals_total == 0:
        return "anarchy"
    if len(rules) == 0 and proposals_total > 0:
        return "failed_state"  # Tried but couldn't agree
    # Check if rules favor redistribution
    redistribution_keywords = ["share", "redistribute", "equal", "tax", "contribute", "pool"]
    has_redistribution = any(
        any(kw in rule.lower() for kw in redistribution_keywords)
        for rule in rules
    )
    if has_redistribution:
        return "welfare_state"
    # Check if rules favor order/structure
    order_keywords = ["must", "required", "penalty", "enforce", "forbidden"]
    has_order = any(
        any(kw in rule.lower() for kw in order_keywords)
        for rule in rules
    )
    if has_order:
        return "authoritarian"
    return "cooperative"  # Rules exist but are voluntary/loose


def gini_over_time(round_snapshots: list[dict]) -> list[float]:
    """Compute Gini coefficient at each round."""
    ginis = []
    for snapshot in round_snapshots:
        balances = list(snapshot["balances"].values())
        ginis.append(gini_coefficient(balances))
    return ginis


def analyze_run(results_dir: str) -> dict:
    """Full analysis of a completed run. Reads from results_dir, writes metrics.json."""
    import os

    # Load results
    with open(os.path.join(results_dir, "results.json")) as f:
        results = json.load(f)

    # Load round snapshots
    round_snapshots = []
    rounds_file = os.path.join(results_dir, "raw", "rounds.jsonl")
    with open(rounds_file) as f:
        for line in f:
            round_snapshots.append(json.loads(line))

    # Compute metrics
    final_balances = results["final_balances"]
    interactions = results["interactions"]
    rules = results["rules_enacted"]

    G = build_communication_graph(interactions)
    net_metrics = network_metrics(G)
    gini_history = gini_over_time(round_snapshots)

    # Count interactions by type
    interaction_counts = defaultdict(int)
    for i in interactions:
        interaction_counts[i["type"]] += 1

    metrics = {
        "run_id": results["config"].get("run_id", "unknown"),
        "final_gini": gini_coefficient(list(final_balances.values())),
        "gini_over_time": gini_history,
        "final_balances": final_balances,
        "governance_type": classify_governance(rules, results["total_proposals"], final_balances),
        "rules_enacted": rules,
        "total_proposals": results["total_proposals"],
        "network": net_metrics,
        "interaction_counts": dict(interaction_counts),
        "api_cost": results["api_cost"],
    }

    # Write metrics
    with open(os.path.join(results_dir, "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2, default=str)

    print(f"Analysis complete for {results_dir}")
    print(f"  Gini: {metrics['final_gini']:.3f}")
    print(f"  Governance: {metrics['governance_type']}")
    print(f"  Rules enacted: {len(rules)}")
    print(f"  Network density: {net_metrics.get('density', 0):.3f}")

    return metrics
