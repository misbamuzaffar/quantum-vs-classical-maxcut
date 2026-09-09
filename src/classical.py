"""Classical baselines for Max-Cut."""

from __future__ import annotations

from itertools import product
from time import perf_counter

import networkx as nx
import numpy as np

from .problem import cut_value


def solve_brute_force(graph: nx.Graph) -> dict:
    """Find the exact Max-Cut solution by enumerating all binary assignments.

    This is intentionally simple and exact. Its exponential scaling makes it
    useful as a small-instance ground-truth baseline, not a scalable solver.
    """
    n = graph.number_of_nodes()

    start = perf_counter()
    best_value = float("-inf")
    best_assignment = None

    # Fix vertex 0 to 0 because a cut and its complement have the same value.
    # This reduces the search space from 2^n to 2^(n-1).
    for tail in product([0, 1], repeat=n - 1):
        assignment = np.array((0, *tail), dtype=int)
        value = cut_value(graph, assignment)

        if value > best_value:
            best_value = value
            best_assignment = assignment

    elapsed = perf_counter() - start

    return {
        "method": "classical_exact",
        "x": best_assignment,
        "objective": best_value,
        "runtime_seconds": elapsed,
    }
