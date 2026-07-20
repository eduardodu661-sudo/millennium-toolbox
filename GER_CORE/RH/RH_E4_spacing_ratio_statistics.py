"""
============================================================
GER RH-E4
Spacing Ratio Statistics
============================================================

Objective
---------
Compute consecutive spacing-ratio statistics for all
registered graph operators.

Definition
----------
Given consecutive spacings

s_n = λ_{n+1} − λ_n

define

r_n = min(s_n,s_{n+1}) / max(s_n,s_{n+1})

which satisfies

0 ≤ r ≤ 1

and is independent of any unfolding procedure.

Output
------
RH_E4_summary.csv
RH_E4_summary.json
RH_E4_execution.txt
<operator>_spacing_ratio.csv
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

EPS = 1e-12


# ============================================================
# Spectrum
# ============================================================

def laplacian_spectrum(graph):

    L = nx.laplacian_matrix(
        graph
    ).astype(float).toarray()

    eigenvalues = np.linalg.eigvalsh(L)

    eigenvalues = np.real_if_close(
        eigenvalues
    )

    eigenvalues = np.sort(
        eigenvalues
    )

    return eigenvalues


def positive_spectrum(eigenvalues):

    return eigenvalues[
        eigenvalues > EPS
    ]


# ============================================================
# Ratio statistics
# ============================================================

def spacing_ratio_statistics(
    eigenvalues,
):

    eig = positive_spectrum(
        eigenvalues
    )

    if len(eig) < 3:

        raise RuntimeError(
            "Spectrum too small."
        )

    spacings = np.diff(eig)

    ratios = []

    rows = []

    for i in range(
        len(spacings) - 1
    ):

        s1 = spacings[i]

        s2 = spacings[i + 1]

        r = min(
            s1,
            s2,
        ) / max(
            s1,
            s2,
        )

        ratios.append(r)

        rows.append({

            "index": i,

            "spacing_left":
                float(s1),

            "spacing_right":
                float(s2),

            "ratio":
                float(r),

        })

    ratios = np.asarray(
        ratios
    )

    stats = {

        "count":
            len(ratios),

        "mean":
            float(
                np.mean(ratios)
            ),

        "median":
            float(
                np.median(ratios)
            ),

        "variance":
            float(
                np.var(ratios)
            ),

        "std":
            float(
                np.std(ratios)
            ),

        "coefficient_variation":
            float(
                np.std(ratios)
                /
                np.mean(ratios)
            ),

        "minimum":
            float(
                np.min(ratios)
            ),

        "maximum":
            float(
                np.max(ratios)
            ),

        "p05":
            float(
                np.percentile(
                    ratios,
                    5,
                )
            ),

        "p25":
            float(
                np.percentile(
                    ratios,
                    25,
                )
            ),

        "p50":
            float(
                np.percentile(
                    ratios,
                    50,
                )
            ),

        "p75":
            float(
                np.percentile(
                    ratios,
                    75,
                )
            ),

        "p95":
            float(
                np.percentile(
                    ratios,
                    95,
                )
            ),

    }

    return stats, rows


# ============================================================
# Main
# ============================================================

def main():

    results = ResultManager(

        category="RH",

        experiment="RH_E4",

    )

    print(

        results.header(

            "GER RH-E4\n"
            "Spacing Ratio Statistics"

        )

    )

    summary = []

    operators = get_registered_operators()

    for name, builder in operators.items():

        print("=" * 60)

        print(name)

        print("-" * 60)

        graph = builder(
            GRAPH_SIZE
        )

        spectrum = laplacian_spectrum(
            graph
        )

        stats, rows = spacing_ratio_statistics(
            spectrum
        )

        results.save_csv(

            f"{name}_spacing_ratio.csv",

            rows,

            header=[

                "index",

                "spacing_left",

                "spacing_right",

                "ratio",

            ],

        )

        entry = {

            "operator":
                name,

        }

        entry.update(
            stats
        )

        summary.append(
            entry
        )

        for key, value in stats.items():

            print(
                f"{key:25s}: {value}"
            )

        print()

    results.save_dict_csv(

        "RH_E4_summary.csv",

        summary,

    )

    results.save_json(

        "RH_E4_summary.json",

        summary,

    )

    report = []

    report.append(

        results.header(

            "GER RH-E4\n"
            "Spacing Ratio Statistics"

        )

    )

    report.append(

        f"Operators analysed : {len(summary)}"

    )

    report.append(

        f"Graph size          : {GRAPH_SIZE}"

    )

    report.append("")

    report.append(
        results.footer()
    )

    results.save_txt(

        "RH_E4_execution.txt",

        "\n".join(report),

    )

    print(
        results.footer()
    )


if __name__ == "__main__":

    main()
