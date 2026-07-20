"""
============================================================
GER CORE
Graph Transforms
============================================================

Operator transformation library.

Transforms existing operators without rebuilding them.

Author
------
Eduardo Batista de Freitas

Version
-------
1.0
"""

from __future__ import annotations

import numpy as np

from .graph_builders import GraphOperator


# ============================================================
# Internal helper
# ============================================================

def _copy(operator: GraphOperator, name: str) -> GraphOperator:

    return GraphOperator(
        name=name,
        adjacency=operator.adjacency.copy(),
    )


# ============================================================
# Add Edge
# ============================================================

def add_edge(
    operator: GraphOperator,
    i: int,
    j: int,
    weight: float = 1.0,
) -> GraphOperator:

    op = _copy(operator, operator.name + "_AddEdge")

    op.adjacency[i, j] = weight
    op.adjacency[j, i] = weight

    return op


# ============================================================
# Remove Edge
# ============================================================

def remove_edge(
    operator: GraphOperator,
    i: int,
    j: int,
) -> GraphOperator:

    op = _copy(operator, operator.name + "_RemoveEdge")

    op.adjacency[i, j] = 0.0
    op.adjacency[j, i] = 0.0

    return op


# ============================================================
# Change Weight
# ============================================================

def set_edge_weight(
    operator: GraphOperator,
    i: int,
    j: int,
    weight: float,
) -> GraphOperator:

    op = _copy(operator, operator.name + "_Weighted")

    op.adjacency[i, j] = weight
    op.adjacency[j, i] = weight

    return op


# ============================================================
# Gaussian Perturbation
# ============================================================

def perturb_weights(
    operator: GraphOperator,
    sigma: float = 0.05,
    seed: int = 42,
) -> GraphOperator:

    rng = np.random.default_rng(seed)

    op = _copy(operator, operator.name + "_Perturbed")

    mask = op.adjacency > 0

    noise = rng.normal(
        loc=0.0,
        scale=sigma,
        size=op.adjacency.shape,
    )

    op.adjacency[mask] += noise[mask]

    op.adjacency = (op.adjacency + op.adjacency.T) / 2

    op.adjacency[op.adjacency < 0] = 0.0

    return op


# ============================================================
# Random Edge Injection
# ============================================================

def add_random_edges(
    operator: GraphOperator,
    probability: float = 0.02,
    seed: int = 42,
) -> GraphOperator:

    rng = np.random.default_rng(seed)

    op = _copy(operator, operator.name + "_RandomEdges")

    n = op.size

    for i in range(n):

        for j in range(i + 1, n):

            if op.adjacency[i, j] == 0:

                if rng.random() < probability:

                    op.adjacency[i, j] = 1.0
                    op.adjacency[j, i] = 1.0

    return op


# ============================================================
# Threshold
# ============================================================

def threshold(
    operator: GraphOperator,
    minimum_weight: float,
) -> GraphOperator:

    op = _copy(operator, operator.name + "_Threshold")

    mask = op.adjacency < minimum_weight

    op.adjacency[mask] = 0.0

    return op


# ============================================================
# Normalize
# ============================================================

def normalize_weights(
    operator: GraphOperator,
) -> GraphOperator:

    op = _copy(operator, operator.name + "_Normalized")

    maximum = op.adjacency.max()

    if maximum > 0:

        op.adjacency /= maximum

    return op
