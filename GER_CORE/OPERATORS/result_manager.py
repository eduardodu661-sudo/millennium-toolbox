"""
============================================================
GER CORE

Result Manager

============================================================

Utility module responsible for storing experiment results.

Automatically creates folders inside Google Drive and
provides simple methods for saving CSV, JSON and TXT files.

Author
------
Eduardo Batista de Freitas

Version
-------
1.0
"""

from __future__ import annotations

import csv
import json
import os
from datetime import datetime


# ============================================================
# Result Manager
# ============================================================

class ResultManager:

    BASE_PATH = (
        "/content/drive/MyDrive/"
        "GER_RESULTS"
    )

    def __init__(

        self,

        category,

        experiment,

    ):

        self.category = category
        self.experiment = experiment

        self.timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        self.output_folder = os.path.join(

            self.BASE_PATH,

            category,

            experiment,

            self.timestamp,

        )

        os.makedirs(

            self.output_folder,

            exist_ok=True,

        )

    # ========================================================

    @property
    def folder(self):

        return self.output_folder

    # ========================================================

    def path(

        self,

        filename,

    ):

        return os.path.join(

            self.output_folder,

            filename,

        )
          # ========================================================
    # CSV
    # ========================================================

    def save_csv(

        self,

        filename,

        rows,

        header=None,

    ):

        filepath = self.path(filename)

        with open(

            filepath,

            "w",

            newline="",

        ) as file:

            writer = csv.writer(file)

            if header is not None:

                writer.writerow(header)

            writer.writerows(rows)

        return filepath

    # ========================================================
    # Dictionary CSV
    # ========================================================

    def save_dict_csv(

        self,

        filename,

        data,

    ):

        filepath = self.path(filename)

        if not data:

            return filepath

        fieldnames = list(data[0].keys())

        with open(

            filepath,

            "w",

            newline="",

        ) as file:

            writer = csv.DictWriter(

                file,

                fieldnames=fieldnames,

            )

            writer.writeheader()

            writer.writerows(data)

        return filepath

    # ========================================================
    # JSON
    # ========================================================

    def save_json(

        self,

        filename,

        data,

    ):

        filepath = self.path(filename)

        with open(

            filepath,

            "w",

        ) as file:

            json.dump(

                data,

                file,

                indent=4,

            )

        return filepath

    # ========================================================
    # TXT
    # ========================================================

    def save_txt(

        self,

        filename,

        text,

    ):

        filepath = self.path(filename)

        with open(

            filepath,

            "w",

        ) as file:

            file.write(text)

        return filepath
          # ========================================================
    # Metadata
    # ========================================================

    def metadata(

        self,

    ):

        return {

            "category":
                self.category,

            "experiment":
                self.experiment,

            "timestamp":
                self.timestamp,

            "output_folder":
                self.output_folder,

        }

    # ========================================================
    # Header
    # ========================================================

    def header(

        self,

        title,

        version="1.0",

    ):

        lines = [

            "=" * 60,

            "GER",

            title,

            "=" * 60,

            "",

            f"Version   : {version}",

            f"Timestamp : {self.timestamp}",

            f"Folder    : {self.output_folder}",

            "",

        ]

        return "\n".join(lines)

    # ========================================================
    # Footer
    # ========================================================

    def footer(

        self,

    ):

        lines = [

            "",

            "=" * 60,

            "Experiment completed.",

            "=" * 60,

            "",

            f"Results saved to:",

            self.output_folder,

            "",

        ]

        return "\n".join(lines)

    # ========================================================
    # Console
    # ========================================================

    def print_location(

        self,

    ):

        print("=" * 60)

        print("Results Folder")

        print("=" * 60)

        print(self.output_folder)

        print()

    # ========================================================
    # String Representation
    # ========================================================

    def __str__(self):

        return self.output_folder

    def __repr__(self):

        return (

            f"ResultManager("

            f"folder='{self.output_folder}')"

        )
