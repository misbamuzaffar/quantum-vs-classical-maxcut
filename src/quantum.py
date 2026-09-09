"""QAOA solver for Max-Cut using modern Qiskit Optimization primitives."""

from __future__ import annotations

from time import perf_counter

import numpy as np
from qiskit.primitives import StatevectorSampler
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.minimum_eigensolvers import QAOA
from qiskit_optimization.optimizers import COBYLA
from qiskit_optimization.utils import algorithm_globals


def solve_qaoa(
    quadratic_program,
    reps: int = 1,
    seed: int = 123,
    maxiter: int = 100,
) -> dict:
    """Solve a binary optimization problem using simulator-based QAOA."""
    if reps < 1:
        raise ValueError("reps must be at least 1.")

    algorithm_globals.random_seed = seed

    sampler = StatevectorSampler(seed=seed)
    optimizer = COBYLA(maxiter=maxiter)

    # QAOA has 2 * reps variational parameters.
    rng = np.random.default_rng(seed)
    initial_point = rng.uniform(0.0, np.pi, size=2 * reps)

    qaoa_mes = QAOA(
        sampler=sampler,
        optimizer=optimizer,
        reps=reps,
        initial_point=initial_point,
    )

    solver = MinimumEigenOptimizer(qaoa_mes)

    start = perf_counter()
    result = solver.solve(quadratic_program)
    elapsed = perf_counter() - start

    return {
        "method": f"qaoa_p{reps}",
        "x": np.rint(result.x).astype(int),
        "objective": float(result.fval),
        "runtime_seconds": elapsed,
        "raw_result": result,
    }
