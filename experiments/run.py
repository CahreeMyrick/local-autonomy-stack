# experiments/run.py
from experiments.scenarios import generate_scenario
from experiments.evaluate import run_trial
from experiments.logging import write_csv
from experiments.aggregate import aggregate
from experiments.plotting import plot_results
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--planner", nargs="+", required=True)
    parser.add_argument("--num-trials", type=int, default=50)
    parser.add_argument("--num-obstacles", type=int, default=5)
    args = parser.parse_args()

    results = []

    for planner in args.planner:
        for i in range(args.num_trials):
            scenario = generate_scenario(
                num_obstacles=args.num_obstacles,
                seed=i
            )
            result = run_trial(planner, scenario, seed=i)
            results.append(result)

    write_csv(results, "experiments/results/results.csv")

    summary = aggregate(results)
    for planner, stats in summary.items():
        print(f"\nPlanner: {planner}")
        for k, v in stats.items():
            print(f"  {k}: {v}")

    plot_results(results)

if __name__ == "__main__":
    main()

