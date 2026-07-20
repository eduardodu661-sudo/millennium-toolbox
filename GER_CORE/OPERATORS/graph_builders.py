"""
============================================================
GER CORE
Operator Graph Builders
============================================================

Library of relational operators used by the GER
experimental laboratory.

Each constructor returns a standardized operator
dictionary.

No spectral analysis is performed here.

Author
------
Eduardo Batista de Freitas

Version
-------
2.0
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


# ============================================================
# Operator Container
# ============================================================

@dataclass
class GraphOperator:

    name: str
    adjacency: np.ndarray

    @property
    def size(self):

        return self.adjacency.shape[0]

    @property
    def laplacian(self):

        degree = np.diag(self.adjacency.sum(axis=1))
        return degree - self.adjacency


# ============================================================
# Cycle
# ============================================================

def build_cycle_graph(
    n: int,
) -> GraphOperator:

    A = np.zeros((n, n), dtype=float)

    for i in range(n):

        A[i, (i - 1) % n] = 1.0
        A[i, (i + 1) % n] = 1.0

    return GraphOperator(
        name="Cycle",
        adjacency=A,
    )


# ============================================================
# Cycle + Extra Edge
# ============================================================

def build_cycle_plus_edge(
    n: int,
    i: int,
    j: int,
) -> GraphOperator:

    op = build_cycle_graph(n)

    A = op.adjacency.copy()

    A[i, j] = 1.0
    A[j, i] = 1.0

    return GraphOperator(
        name="Cycle+Edge",
        adjacency=A,
    )


# ============================================================
# Broken Cycle
# ============================================================

def build_broken_cycle(
    n: int,
    edge: int,
) -> GraphOperator:

    op = build_cycle_graph(n)

    A = op.adjacency.copy()

    j = (edge + 1) % n

    A[edge, j] = 0.0
    A[j, edge] = 0.0

    return GraphOperator(
        name="BrokenCycle",
        adjacency=A,
    )


# ============================================================
# Weighted Cycle
# ============================================================

def build_weighted_cycle(
    n: int,
    weight: float = 2.0,
) -> GraphOperator:

    op = build_cycle_graph(n)

    A = op.adjacency.copy()

    A[0,1] = weight
    A[1,0] = weight

    return GraphOperator(
        name="WeightedCycle",
        adjacency=A,
    )


# ============================================================
# Random Perturbed Cycle
# ============================================================

def build_random_cycle(
    n: int,
    probability: float = 0.02,
    seed: int = 42,
) -> GraphOperator:

    rng = np.random.default_rng(seed)

    op = build_cycle_graph(n)

    A = op.adjacency.copy()

    for i in range(n):

        for j in range(i + 2, n):

            if rng.random() < probability:

                A[i, j] = 1.0
                A[j, i] = 1.0

    return GraphOperator(
        name="RandomCycle",
        adjacency=A,
    )
