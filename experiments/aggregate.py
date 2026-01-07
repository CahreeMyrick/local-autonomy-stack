# experiments/aggregate.py
import numpy as np
from collections import defaultdict

def aggregate(results):
    grouped = defaultdict(list)
    for r in results:
        grouped[r["planner"]].append(r)

    summary = {}

    for planner, runs in grouped.items():
        successes = [r for r in runs if r["success"]]
        failures = [r for r in runs if not r["success"]]
        collisions = [r for r in runs if r["min_clearance"] < 0]

        summary[planner] = {
            "num_trials": len(runs),
            "success_rate": len(successes) / len(runs),
            "collision_rate": len(collisions) / len(runs),
            "mean_steps": np.mean([r["steps"] for r in successes]) if successes else None,
            "std_steps": np.std([r["steps"] for r in successes]) if successes else None,
            "mean_path_length": np.mean([r["path_length"] for r in successes]) if successes else None,
            "std_path_length": np.std([r["path_length"] for r in successes]) if successes else None,
            "mean_clearance": np.mean([r["min_clearance"] for r in successes]) if successes else None,
        }

    return summary

