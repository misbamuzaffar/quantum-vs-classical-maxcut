"""Utilities for generating and evaluating Max-Cut instances."""

from __future__ import annotations

import networkx as nx
import numpy as np
from qiskit_optimization.applications import Maxcut


def generate_graph(
    n_nodes: int,
    edge_probability: float = 0.5,
    seed: int | None = None,
) -> nx.Graph:
    """Generate a connected random unweighted graph.

    We retry with deterministic seed offsets until the graph is connected.
    This keeps benchmark instances easy to interpret.
    """
    if n_nodes < 2:
        raise ValueError("n_nodes must be at least 2.")

    attempt = 0
    while True:
        graph_seed = None if seed is None else seed + attempt
        graph = nx.gnp_random_graph(n_nodes, edge_probability, seed=graph_seed)

        if nx.is_connected(graph):
            for u, v in graph.edges:
                graph[u][v]["weight"] = 1.0
            return graph

        attempt += 1


def graph_to_quadratic_program(graph: nx.Graph):
    """Convert a NetworkX graph to Qiskit's Max-Cut QuadraticProgram."""
    weight_matrix = nx.to_numpy_array(graph, weight="weight", dtype=float)
    maxcut = Maxcut(weight_matrix)
    return maxcut.to_quadratic_program()


def cut_value(graph: nx.Graph, bitstring: np.ndarray | list[int]) -> float:
    """Compute the cut value represented by a 0/1 assignment."""
    assignment = np.asarray(bitstring, dtype=int)
    value = 0.0

    for u, v, data in graph.edges(data=True):
        if assignment[u] != assignment[v]:
            value += float(data.get("weight", 1.0))

    return value
