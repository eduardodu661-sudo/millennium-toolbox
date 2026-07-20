"""
============================================================
GER RH-E3
Normalized Spacing Statistics
============================================================

Objective
---------
Compute normalized nearest-neighbor spacing statistics for all
registered graph operators.

This experiment intentionally uses mean-normalized spacings instead
of a full spectral unfolding. A genuine unfolding procedure requires
estimating the smooth spectral density and will be introduced in a
later experiment.

Output
------
summary.csv
summary.json
execution.txt
<operator>_spacing.csv
"""

from __future__ import annotations

import numpy as np
import networkx as nx

from GER_CORE.OPERATORS.operator_registry import (
    get_registered_operators,
)

from GER_CORE.OPERATORS.result_manager import (
    ResultManager,
)


# ============================================================
# Configuration
# ============================================================

GRAPH_SIZE = 128


# ============================================================
# Utilities
# ============================================================

def laplacian_spectrum(graph):

    L = nx.laplacian_matrix(graph).astype(float).toarray()

    eigenvalues = np.linalg.eigvalsh(L)

    eigenvalues = np.sort(
        np.real_if_close(eigenvalues)
    )

    return eigenvalues


def positive_spectrum(eigenvalues):

    eps = 1e-12

    return eigenvalues[eigenvalues > eps]


def spacing_statistics(eigenvalues):

    eig = positive_spectrum(eigenvalues)

    if len(eig) < 2:

        raise RuntimeError(
            "Spectrum too small."
        )

    spacings = np.diff(eig)

    mean_spacing = np.mean(spacings)

    normalized = spacings / mean_spacing

    stats = {

        "count":
            len(normalized),

        "mean":
            float(np.mean(normalized)),

        "median":
            float(np.median(normalized)),

        "variance":
            float(np.var(normalized)),

        "std":
            float(np.std(normalized)),

        "coefficient_variation":
            float(
                np.std(normalized)
                /
                np.mean(normalized)
            ),

        "minimum":
            float(np.min(normalized)),

        "maximum":
            float(np.max(normalized)),

        "p05":
            float(
                np.percentile(
                    normalized,
                    5,
                )
            ),

        "p25":
            float(
                np.percentile(
                    normalized,
                    25,
                )
            ),

        "p50":
            float(
                np.percentile(
                    normalized,
                    50,
                )
            ),

        "p75":
            float(
                np.percentile(
                    normalized,
                    75,
                )
            ),

        "p95":
            float(
                np.percentile(
                    normalized,
                    95,
                )
            ),

    }

    rows = []

    for i, value in enumerate(normalized):

        rows.append({

            "index": i,

            "spacing": float(spacings[i]),

            "normalized_spacing":
                float(value),

        })

    return stats, rows


# ============================================================
# Main
# ============================================================

def main():

    results = ResultManager(

        category="RH",

        experiment="RH_E3",

    )

    print(

        results.header(

            "GER RH-E3\n"
            "Normalized Spacing Statistics"

        )

    )

    summary = []

    operators = get_registered_operators()

    for name, builder in operators.items():

        print("=" * 60)

        print(name)

        print("-" * 60)

        graph = builder(GRAPH_SIZE)

        spectrum = laplacian_spectrum(graph)

        stats, spacing_rows = spacing_statistics(
            spectrum
        )

        results.save_csv(

            f"{name}_spacing.csv",

            spacing_rows,

            header=[
                "index",
                "spacing",
                "normalized_spacing",
            ],

        )

        row = {

            "operator": name,

        }

        row.update(stats)

        summary.append(row)

        for key, value in stats.items():

            print(f"{key:25s}: {value}")

        print()

    results.save_dict_csv(

        "RH_E3_summary.csv",

        summary,

    )

    results.save_json(

        "RH_E3_summary.json",

        summary,

    )

    report = []

    report.append(

        results.header(

            "GER RH-E3\n"
            "Normalized Spacing Statistics"

        )

    )

    report.append(

        f"Operators analysed : {len(summary)}"

    )

    report.append(

        f"Graph size          : {GRAPH_SIZE}"

    )

    report.append("")

    report.append(results.footer())

    results.save_txt(

        "RH_E3_execution.txt",

        "\n".join(report),

    )

    print(results.footer())


if __name__ == "__main__":

    main()
