"""
============================================================
GER
RH-E2

Operator Family Scan

============================================================

Scans every registered graph operator,
computes its Laplacian spectrum,
computes global spectral statistics
and automatically saves every result
to Google Drive.

Outputs
-------

Google Drive

GER_RESULTS/
    RH/
        RH_E2/
            YYYYMMDD_HHMMSS/
                RH_E2_summary.csv
                RH_E2_summary.json
                RH_E2_execution.txt
                *_spectrum.csv

Author
------
Eduardo Batista de Freitas

Version
-------
1.1
"""

from __future__ import annotations

import csv
import json
import os
from datetime import datetime

import numpy as np

from GER_CORE.OPERATORS.operator_registry import (
    build_default_family,
)

# ============================================================
# Configuration
# ============================================================

BASE_RESULT_PATH = (
    "/content/drive/MyDrive/"
    "GER_RESULTS/RH/RH_E2"
)

VERSION = "1.1"

# ============================================================
# Output Folder
# ============================================================

def create_output_folder():

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_folder = os.path.join(
        BASE_RESULT_PATH,
        timestamp,
    )

    os.makedirs(
        output_folder,
        exist_ok=True,
    )

    return output_folder, timestamp


# ============================================================
# Spectrum
# ============================================================

def compute_spectrum(operator):

    return np.linalg.eigvalsh(
        operator.laplacian
    )


# ============================================================
# Spectral Statistics
# ============================================================

def spectral_statistics(eigenvalues):

    eigenvalues = np.asarray(
        eigenvalues,
        dtype=float,
    )

    eigenvalues = np.sort(eigenvalues)

    gaps = np.diff(eigenvalues)

    if len(gaps):

        spectral_gap = float(gaps[0])

        mean_gap = float(np.mean(gaps))

    else:

        spectral_gap = 0.0
        mean_gap = 0.0

    if len(eigenvalues) > 1:

        positive = eigenvalues[1:]

        minimum_positive = max(
            np.min(positive),
            1e-12,
        )

        condition = (
            np.max(eigenvalues)
            /
            minimum_positive
        )

    else:

        condition = 0.0

    return {

        "dimension":
            int(len(eigenvalues)),

        "trace":
            float(np.sum(eigenvalues)),

        "minimum":
            float(np.min(eigenvalues)),

        "maximum":
            float(np.max(eigenvalues)),

        "mean":
            float(np.mean(eigenvalues)),

        "variance":
            float(np.var(eigenvalues)),

        "spectral_gap":
            spectral_gap,

        "mean_gap":
            mean_gap,

        "condition":
            float(condition),

    }


# ============================================================
# CSV
# ============================================================

def save_spectrum_csv(
    folder,
    operator_name,
    eigenvalues,
):

    filename = os.path.join(

        folder,

        f"{operator_name}_spectrum.csv",

    )

    with open(

        filename,

        "w",

        newline="",

    ) as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow(

            [

                "index",

                "eigenvalue",

            ]

        )

        for i, value in enumerate(eigenvalues):

            writer.writerow(

                [

                    i,

                    float(value),

                ]

            )
          # ============================================================
# Summary CSV
# ============================================================

def save_summary_csv(
    folder,
    summary,
):

    filename = os.path.join(

        folder,

        "RH_E2_summary.csv",

    )

    if not summary:

        return

    fieldnames = list(summary[0].keys())

    with open(

        filename,

        "w",

        newline="",

    ) as csvfile:

        writer = csv.DictWriter(

            csvfile,

            fieldnames=fieldnames,

        )

        writer.writeheader()

        writer.writerows(summary)


# ============================================================
# Summary JSON
# ============================================================

def save_summary_json(
    folder,
    summary,
    timestamp,
    n,
):

    filename = os.path.join(

        folder,

        "RH_E2_summary.json",

    )

    payload = {

        "experiment":
            "RH_E2",

        "version":
            VERSION,

        "timestamp":
            timestamp,

        "graph_dimension":
            n,

        "number_of_operators":
            len(summary),

        "results":
            summary,

    }

    with open(

        filename,

        "w",

    ) as file:

        json.dump(

            payload,

            file,

            indent=4,

        )


# ============================================================
# TXT Report
# ============================================================

def build_execution_report(
    summary,
    timestamp,
    n,
):

    lines = []

    lines.append("=" * 60)
    lines.append("GER RH-E2")
    lines.append("Operator Family Scan")
    lines.append("=" * 60)
    lines.append("")

    lines.append(f"Version   : {VERSION}")
    lines.append(f"Timestamp : {timestamp}")
    lines.append(f"Dimension : {n}")
    lines.append(f"Operators : {len(summary)}")

    lines.append("")

    for result in summary:

        lines.append("-" * 60)

        lines.append(

            result["operator"]

        )

        lines.append("-" * 60)

        for key, value in result.items():

            if key == "operator":

                continue

            lines.append(

                f"{key:18s}: {value}"

            )

        lines.append("")

    return "\n".join(lines)


def save_execution_report(
    folder,
    report,
):

    filename = os.path.join(

        folder,

        "RH_E2_execution.txt",

    )

    with open(

        filename,

        "w",

    ) as file:

        file.write(report)


# ============================================================
# Terminal
# ============================================================

def print_statistics(
    operator_name,
    stats,
):

    print("=" * 60)

    print(operator_name)

    print("-" * 60)

    for key, value in stats.items():

        print(

            f"{key:18s}: {value}"

        )

    print()
  # ============================================================
# Experiment
# ============================================================

def run_experiment(n=128):

    output_folder, timestamp = create_output_folder()

    print("=" * 60)
    print("GER RH-E2")
    print("Operator Family Scan")
    print("=" * 60)
    print()

    print(f"Output folder:")
    print(output_folder)
    print()

    operators = build_default_family(n)

    summary = []

    for operator in operators:

        eigenvalues = compute_spectrum(operator)

        stats = spectral_statistics(
            eigenvalues
        )

        result = {

            "operator":
                operator.name,

            **stats,

        }

        summary.append(result)

        print_statistics(
            operator.name,
            stats,
        )

        save_spectrum_csv(
            output_folder,
            operator.name,
            eigenvalues,
        )

    save_summary_csv(
        output_folder,
        summary,
    )

    save_summary_json(
        output_folder,
        summary,
        timestamp,
        n,
    )

    report = build_execution_report(
        summary,
        timestamp,
        n,
    )

    save_execution_report(
        output_folder,
        report,
    )

    print("=" * 60)
    print("Experiment completed.")
    print("=" * 60)
    print()

    print("Files generated:")

    print("  RH_E2_summary.csv")
    print("  RH_E2_summary.json")
    print("  RH_E2_execution.txt")
    print("  *_spectrum.csv")
    print()

    print(f"Saved to:")
    print(output_folder)
    print()

    return summary


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    run_experiment()
