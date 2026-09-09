"""Run reproducible Quantum-vs-Classical Max-Cut experiments."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.classical import solve_brute_force
from src.problem import cut_value, generate_graph, graph_to_quadratic_program
from src.quantum import solve_qaoa
from src.visualization import save_plots


OUTPUT_DIR = Path("results")

# Keep the baseline deliberately small so it can run on a laptop.
#GRAPH_SIZES = [4, 5, 6]
GRAPH_SIZES = [6, 8, 10]
GRAPH_SEEDS = [11, 23, 37]
EDGE_PROBABILITY = 0.5
#QAOA_DEPTHS = [1, 2]
QAOA_DEPTHS = [1, 2, 3]


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    records = []

    for n_nodes in GRAPH_SIZES:
        for seed in GRAPH_SEEDS:
            print(f"\nGraph: n={n_nodes}, seed={seed}")

            graph = generate_graph(
                n_nodes=n_nodes,
                edge_probability=EDGE_PROBABILITY,
                seed=seed,
            )
            qp = graph_to_quadratic_program(graph)

            classical = solve_brute_force(graph)
            optimum = classical["objective"]

            print(
                f"  Classical exact: cut={optimum:.3f}, "
                f"time={classical['runtime_seconds']:.6f}s"
            )

            records.append(
                {
                    "n_nodes": n_nodes,
                    "seed": seed,
                    "edge_probability": EDGE_PROBABILITY,
                    "method": classical["method"],
                    "cut_value": optimum,
                    "optimal_cut": optimum,
                    "approximation_ratio": 1.0,
                    "runtime_seconds": classical["runtime_seconds"],
                }
            )

            for reps in QAOA_DEPTHS:
                qaoa = solve_qaoa(
                    quadratic_program=qp,
                    reps=reps,
                    seed=seed,
                    maxiter=100,
                )

                # Evaluate the returned assignment ourselves so both methods
                # use exactly the same graph-based objective calculation.
                qaoa_cut = cut_value(graph, qaoa["x"])
                ratio = qaoa_cut / optimum if optimum != 0 else 1.0

                print(
                    f"  QAOA p={reps}: cut={qaoa_cut:.3f}, "
                    f"ratio={ratio:.3f}, "
                    f"time={qaoa['runtime_seconds']:.6f}s"
                )

                records.append(
                    {
                        "n_nodes": n_nodes,
                        "seed": seed,
                        "edge_probability": EDGE_PROBABILITY,
                        "method": qaoa["method"],
                        "cut_value": qaoa_cut,
                        "optimal_cut": optimum,
                        "approximation_ratio": ratio,
                        "runtime_seconds": qaoa["runtime_seconds"],
                    }
                )

    results = pd.DataFrame(records)
    csv_path = OUTPUT_DIR / "benchmark_results.csv"
    results.to_csv(csv_path, index=False)
    save_plots(results, OUTPUT_DIR)

    print("\nSaved:")
    print(f"  {csv_path}")
    print(f"  {OUTPUT_DIR / 'approximation_ratio.png'}")
    print(f"  {OUTPUT_DIR / 'runtime.png'}")

    print("\nMean results:")
    print(
        results.groupby(["n_nodes", "method"])[
            ["approximation_ratio", "runtime_seconds"]
        ]
        .mean()
        .round(4)
    )


if __name__ == "__main__":
    main()
