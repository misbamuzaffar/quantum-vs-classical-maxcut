# Quantum vs. Classical Optimization: Max-Cut with QAOA

A research-style benchmark comparing a classical exact solver with the Quantum Approximate Optimization Algorithm (QAOA) on small Max-Cut problems.

## Research Question

How does QAOA compare with a classical exact method on small combinatorial optimization problems as graph size and QAOA circuit depth change?

This project focuses on:

- formulating Max-Cut as a binary optimization problem,
- solving the same instances with a classical brute-force method and QAOA,
- comparing objective value, approximation ratio, and runtime,
- studying how QAOA depth (`reps`) changes solution quality,
- producing reproducible numerical experiments and plots.

> This is a learning/benchmark project using quantum simulation. It does **not** claim quantum advantage.

## Why Max-Cut?

For a graph \(G=(V,E)\), Max-Cut divides vertices into two sets so that as many edges as possible cross between them. It is a standard combinatorial optimization problem and can be represented as a QUBO/Ising Hamiltonian, which makes it a natural introductory problem for QAOA.

## Project Structure

```text
quantum-vs-classical-maxcut/
├── README.md
├── environment.yml
├── requirements.txt
├── run_experiment.py
├── src/
│   ├── classical.py
│   ├── problem.py
│   ├── quantum.py
│   └── visualization.py
└── results/
```

## Setup with Anaconda

```bash
conda env create -f environment.yml
conda activate quantum-maxcut
```

Or, inside an existing environment:

```bash
pip install -r requirements.txt
```

## Run

Open the folder in VS Code, select the `quantum-maxcut` Python interpreter, then run:

```bash
python run_experiment.py
```

The script creates several random graph instances, solves each one classically and with QAOA, and saves:

- `results/benchmark_results.csv`
- `results/approximation_ratio.png`
- `results/runtime.png`

## Metrics

**Cut value:** Number (or total weight) of edges crossing between the two selected vertex sets.

**Approximation ratio:**

\[
\text{Approximation Ratio} =
\frac{\text{QAOA Cut Value}}{\text{Optimal Classical Cut Value}}
\]

A value of `1.0` means QAOA found the known optimum for that instance.

**Runtime:** Wall-clock time taken by each solver. Because QAOA is simulated on a classical computer here, runtime comparisons should be interpreted as implementation/experimental comparisons—not evidence of quantum speedup.

## Experiments to Add

Once the baseline works, extend the project one experiment at a time:

1. Increase graph size from 4–6 vertices to larger instances.
2. Compare QAOA depth `reps = 1, 2, 3`.
3. Run multiple random seeds per graph size.
4. Compare sparse vs. dense graphs.
5. Add weighted Max-Cut.
6. Compare noiseless simulation against an Aer noise model.
7. Compare QAOA against a scalable classical heuristic rather than only brute force.
8. Report mean approximation ratio and variability over repeated trials.

## Resume Version

**Quantum vs. Classical Optimization Benchmark | Python, Qiskit**

- Implemented a reproducible Max-Cut benchmark comparing QAOA with a classical exact solver across randomly generated graph instances.
- Formulated combinatorial optimization problems as binary quadratic programs and evaluated quantum solutions using approximation ratio and runtime.
- Designed numerical experiments to study how graph size and QAOA circuit depth affect optimization performance.
- Built automated visualization and reporting tools for comparing classical and quantum results.

Only use these bullets after you have run, understood, and validated the corresponding experiments.

## Responsible Interpretation

This repository is intended to demonstrate quantum-algorithm development, scientific computing, and experimental reasoning. Small simulator benchmarks do not demonstrate practical quantum advantage. Results should be presented as evidence about algorithm behavior under the tested conditions.
