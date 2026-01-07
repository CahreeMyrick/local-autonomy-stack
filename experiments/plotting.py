import matplotlib.pyplot as plt
from collections import defaultdict
import os

def plot_results(results, out_dir="experiments/plots"):
    out_dir = "experiments/plots"
    os.makedirs(out_dir, exist_ok=True)

    grouped = defaultdict(list)
    for r in results:
        grouped[r["planner"]].append(r)

    # --- Success rate ---
    planners = list(grouped.keys())
    success_rates = [
        sum(r["success"] for r in grouped[p]) / len(grouped[p])
        for p in planners
    ]

    plt.figure()
    plt.bar(planners, success_rates)
    plt.ylabel("Success Rate")
    plt.title("Success Rate by Planner")
    plt.savefig(f"{out_dir}/success_rate.png")

    # --- Path length boxplot ---
    plt.figure()
    data = [
        [r["path_length"] for r in grouped[p] if r["success"]]
        for p in planners
    ]
    plt.boxplot(data, labels=planners)
    plt.ylabel("Path Length")
    plt.title("Path Length Distribution (Successful Runs)")
    plt.savefig(f"{out_dir}/path_length_boxplot.png")

    # --- Clearance histogram ---
    plt.figure()
    for p in planners:
        clearances = [r["min_clearance"] for r in grouped[p]]
        plt.hist(clearances, bins=30, alpha=0.5, label=p)

    plt.xlabel("Minimum Clearance")
    plt.ylabel("Frequency")
    plt.legend()
    plt.title("Minimum Clearance Distribution")
    plt.savefig(f"{out_dir}/clearance_hist.png")

    plt.close("all")

