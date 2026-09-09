"""Plotting utilities for benchmark results."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_plots(results: pd.DataFrame, output_dir: str | Path = "results") -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    qaoa = results[results["method"].str.startswith("qaoa")].copy()

    # Approximation-ratio plot
    fig, ax = plt.subplots(figsize=(8, 5))
    for method, group in qaoa.groupby("method"):
        grouped = group.groupby("n_nodes", as_index=False)["approximation_ratio"].mean()
        ax.plot(
            grouped["n_nodes"],
            grouped["approximation_ratio"],
            marker="o",
            label=method,
        )

    ax.axhline(1.0, linestyle="--", linewidth=1, label="optimal")
    ax.set_xlabel("Number of graph vertices")
    ax.set_ylabel("Mean approximation ratio")
    ax.set_title("QAOA solution quality vs. problem size")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "approximation_ratio.png", dpi=180)
    plt.close(fig)

    # Runtime plot
    fig, ax = plt.subplots(figsize=(8, 5))
    for method, group in results.groupby("method"):
        grouped = group.groupby("n_nodes", as_index=False)["runtime_seconds"].mean()
        ax.plot(
            grouped["n_nodes"],
            grouped["runtime_seconds"],
            marker="o",
            label=method,
        )

    ax.set_xlabel("Number of graph vertices")
    ax.set_ylabel("Mean runtime (seconds)")
    ax.set_yscale("log")
    ax.set_title("Solver runtime vs. problem size")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "runtime.png", dpi=180)
    plt.close(fig)
