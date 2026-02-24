"""Visualization for Project Crucible runs."""

import json
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import networkx as nx
from analysis.metrics import build_communication_graph, gini_over_time


def plot_token_distribution(results_dir: str):
    """Plot token balances over time for each agent."""
    rounds_file = os.path.join(results_dir, "raw", "rounds.jsonl")
    snapshots = []
    with open(rounds_file) as f:
        for line in f:
            snapshots.append(json.loads(line))

    if not snapshots:
        return

    agents = list(snapshots[0]["balances"].keys())
    rounds = [s["round"] for s in snapshots]

    fig, ax = plt.subplots(figsize=(10, 5))
    for agent in agents:
        balances = [s["balances"][agent] for s in snapshots]
        ax.plot(rounds, balances, marker="o", markersize=3, label=agent, linewidth=2)

    ax.set_xlabel("Round")
    ax.set_ylabel("Credits")
    ax.set_title("Credit Distribution Over Time")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "token_distribution.png"), dpi=150)
    plt.close()
    print(f"  Saved: {results_dir}/token_distribution.png")


def plot_gini_over_time(results_dir: str):
    """Plot Gini coefficient over time."""
    rounds_file = os.path.join(results_dir, "raw", "rounds.jsonl")
    snapshots = []
    with open(rounds_file) as f:
        for line in f:
            snapshots.append(json.loads(line))

    ginis = gini_over_time(snapshots)
    rounds = list(range(len(ginis)))

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(rounds, ginis, color="red", linewidth=2)
    ax.fill_between(rounds, ginis, alpha=0.2, color="red")
    ax.set_xlabel("Round")
    ax.set_ylabel("Gini Coefficient")
    ax.set_title("Wealth Inequality Over Time (0 = equal, 1 = one agent has everything)")
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "gini_over_time.png"), dpi=150)
    plt.close()
    print(f"  Saved: {results_dir}/gini_over_time.png")


def plot_network_graph(results_dir: str):
    """Plot the communication/interaction network."""
    with open(os.path.join(results_dir, "results.json")) as f:
        results = json.load(f)

    interactions = results["interactions"]
    G = build_communication_graph(interactions)

    if len(G.nodes) == 0:
        print("  No interactions to plot.")
        return

    fig, ax = plt.subplots(figsize=(8, 8))
    pos = nx.spring_layout(G, seed=42)

    # Edge widths based on weight
    weights = [G[u][v]["weight"] for u, v in G.edges()]
    max_weight = max(weights) if weights else 1

    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="#4ECDC4", ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold", ax=ax)
    nx.draw_networkx_edges(
        G, pos, width=[w / max_weight * 5 for w in weights],
        alpha=0.6, edge_color="#555", arrows=True, arrowsize=20, ax=ax,
    )

    # Edge labels
    edge_labels = {(u, v): str(G[u][v]["weight"]) for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=9, ax=ax)

    ax.set_title("Agent Interaction Network (edge weight = # interactions)")
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "network_graph.png"), dpi=150)
    plt.close()
    print(f"  Saved: {results_dir}/network_graph.png")


def generate_all_plots(results_dir: str):
    """Generate all visualizations for a run."""
    print(f"Generating plots for {results_dir}...")
    plot_token_distribution(results_dir)
    plot_gini_over_time(results_dir)
    plot_network_graph(results_dir)
    print("All plots generated.")
