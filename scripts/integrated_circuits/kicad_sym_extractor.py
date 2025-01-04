"""Extracts symbol information from a KiCad symbol library file (.kicad_sym).

This script reads a KiCad symbol library file and extracts all symbol names
and properties defined in the file. It writes the extracted information to a
CSV file with headers determined from the properties found in the symbols.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path


def parse_kicad_symbol_file(content: str) -> dict[str, dict[str, str]]:
    """Parse a KiCad symbol file and extract symbol names and properties.

    Args:
        content (str): The content of the KiCad symbol file

    Returns:
        dict[str, dict[str, str]]:
            A dictionary where keys are symbol names and values are
            dictionaries of properties for each symbol.

    """
    symbols = {}

    # Regular expression to find all symbols
    symbol_pattern = r'\(symbol\s+"([^"]+)"(.*?)\)\s*(?=\(symbol|$)'
    property_pattern = r'\(property\s+"([^"]+)"\s+"([^"]+)"(?:\s+[^\)]*)?\)'

    # Extract symbols and their properties
    for symbol_match in re.finditer(symbol_pattern, content, re.DOTALL):
        symbol_name = symbol_match.group(1)

        # Exclude symbols ending with _0_1
        if any(symbol_name.endswith(pattern) for pattern in ("_0_1")):
            continue

        symbol_body = symbol_match.group(2)
        properties = {}

        # Extract properties for the current symbol
        for property_match in re.finditer(property_pattern, symbol_body):
            name = property_match.group(1)
            value = property_match.group(2)
            properties[name] = value

        symbols[symbol_name] = properties

    return symbols


def get_all_property_names(symbols: dict[str, dict[str, str]]) -> list[str]:
    """Get a sorted list of all unique property names found in the symbols.

    Args:
        symbols (dict[str, dict[str, str]]):
            A dictionary of symbols and their properties

    Returns:
        list[str]: A sorted list of all unique property names

    """
    property_names = set()
    for properties in symbols.values():
        property_names.update(properties.keys())
    return sorted(property_names)


def write_symbols_to_csv(
    symbols: dict[str, dict[str, str]],
    output_file: Path,
) -> None:
    """Write symbols and their properties to a CSV file.

    Args:
        symbols (dict[str, dict[str, str]]):
            A dictionary of symbols and their properties
        output_file (Path):
            Path to the output CSV file

    Returns:
        None

    """
    # Get all unique property names to use as headers
    headers = ["Symbol Name", *get_all_property_names(symbols)]

    with output_file.open("w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

        for symbol_name, properties in symbols.items():
            # Create a row with empty strings for missing properties
            row = [symbol_name] + [
                properties.get(header, "") for header in headers[1:]
            ]
            writer.writerow(row)


if __name__ == "__main__":
    filename = "UNITED_IC_ADI.kicad_sym"
    # Get the directory where the script is located
    script_dir = Path(__file__).parent

    # Construct the full path to the kicad file
    file_path = script_dir / filename
    output_file = script_dir / "symbols.csv"

    print(f"Looking for file at: {file_path}")

    # Check if file exists
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    # Read the file
    with file_path.open() as file:
        content = file.read()

    # Parse and write results to CSV
    symbols = parse_kicad_symbol_file(content)
    write_symbols_to_csv(symbols, output_file)
    print(f"Symbol information has been written to: {output_file}")
