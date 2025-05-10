"""Utility functions for file handling.

This module contains utility functions for file handling, such as writing
to CSV files and creating directories.
"""

import csv
from pathlib import Path
from typing import Final, NamedTuple

from .print_message_utilities import print_info


def write_to_csv(
    parts_list: list[NamedTuple],
    output_file: str,
    header_mapping: list[str],
    encoding: str = "utf-8",
) -> None:
    """Write specifications to CSV file using global header mapping.

    Args:
        parts_list: List of parts to write
        output_file: Output filename
        header_mapping: todo
        encoding: Character encoding

    Returns:
        None

    """
    # Prepare all rows before opening file
    headers: Final[list[str]] = list(header_mapping.keys())
    rows = [headers]
    rows.extend([
        [header_mapping[header](part) for header in headers]
        for part in parts_list
    ])

    # Write all rows at once
    with Path.open(
        f"{output_file}",
        "w",
        newline="",
        encoding=encoding,
    ) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)


def ensure_directory_exists(directory: str) -> None:
    """Create a directory and all necessary parent directories.

    Args:
        directory: Path of the directory to create.
            Can be either absolute or relative path.

    Returns:
        None

    Note:
        If the directory already exists, this function will silently succeed.
        Parent directories will be created automatically if they don't exist.

    """
    Path(directory).mkdir(parents=True, exist_ok=True)
    print_info(f"Created directory: {directory}")


def read_csv_data(input_csv_file: str) -> list[dict[str, str]]:
    """Read component data from a CSV file.

    Args:
        input_csv_file (str): Path to the input CSV file.
        encoding (str): Character encoding of the CSV file.

    Returns:
        List[Dict[str, str]]: List of dictionaries containing component data.

    """
    with Path.open(input_csv_file, "r", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))
