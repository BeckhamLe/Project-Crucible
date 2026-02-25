"""CLI entry point for Project Crucible simulations."""

import argparse
import json
import os
import sys
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

from sim.engine import run_simulation
from sim.agents import get_agent_configs


def main():
    parser = argparse.ArgumentParser(description="Run a Project Crucible simulation")
    parser.add_argument("--config", default="configs/templates/baseline.json", help="Path to run config JSON")
    parser.add_argument("--run-id", default=None, help="Run ID (auto-generated if not provided)")
    args = parser.parse_args()

    # Load config
    with open(args.config) as f:
        config = json.load(f)

    # Generate run ID
    run_id = args.run_id or f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    config["run_id"] = run_id

    # Resolve persona references to full configs
    if "persona_names" in config and "personas" not in config:
        token_overrides = config.get("token_overrides")
        config["personas"] = get_agent_configs(config["persona_names"], token_overrides)

    # Validate
    if "personas" not in config or not config["personas"]:
        print("Error: Config must have 'personas' (list of agent configs) or 'persona_names' (list of names).")
        sys.exit(1)

    if "simulation" not in config:
        print("Error: Config must have 'simulation' with at least 'rounds'.")
        sys.exit(1)

    # Create output directory
    output_dir = os.path.join("results", run_id)
    os.makedirs(output_dir, exist_ok=True)

    # Save config snapshot
    with open(os.path.join(output_dir, "config_snapshot.json"), "w") as f:
        json.dump(config, f, indent=2)

    print(f"Run ID: {run_id}")
    print(f"Config: {args.config}")
    print(f"Output: {output_dir}/")
    print()

    # Run simulation
    results = run_simulation(config, output_dir)

    print(f"\nResults saved to {output_dir}/")
    return results


if __name__ == "__main__":
    main()
