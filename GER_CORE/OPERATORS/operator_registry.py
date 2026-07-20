"""
============================================================
GER CORE
Operator Registry
============================================================

Central registry of graph operators.

Experiments should obtain operator families through this
module instead of instantiating builders directly.

Author
------
Eduardo Batista de Freitas

Version
-------
1.0
"""

from __future__ import annotations

from typing import Callable, Dict, List

from .graph_builders import (
    GraphOperator,
    build_cycle_graph,
    build_cycle_plus_edge,
    build_broken_cycle,
    build_weighted_cycle,
    build_random_cycle,
)


# ============================================================
# Registry
# ============================================================

_OPERATOR_BUILDERS: Dict[str, Callable[..., GraphOperator]] = {}


def register_operator(
    name: str,
    builder: Callable[..., GraphOperator],
) -> None:

    _OPERATOR_BUILDERS[name] = builder


def available_operators() -> List[str]:

    return sorted(_OPERATOR_BUILDERS.keys())


def build_operator(
    name: str,
    **kwargs,
) -> GraphOperator:

    if name not in _OPERATOR_BUILDERS:

        raise ValueError(f"Unknown operator: {name}")

    return _OPERATOR_BUILDERS[name](**kwargs)


# ============================================================
# Default Family
# ============================================================

register_operator(
    "Cycle",
    build_cycle_graph,
)

register_operator(
    "CyclePlusEdge",
    lambda n: build_cycle_plus_edge(
        n=n,
        i=0,
        j=n // 2,
    ),
)

register_operator(
    "BrokenCycle",
    lambda n: build_broken_cycle(
        n=n,
        edge=0,
    ),
)

register_operator(
    "WeightedCycle",
    build_weighted_cycle,
)

register_operator(
    "RandomCycle",
    build_random_cycle,
)


# ============================================================
# Convenience
# ============================================================

def build_default_family(
    n: int,
) -> List[GraphOperator]:

    return [

        build_operator(
            name,
            n=n,
        )

        for name in available_operators()

    ]
