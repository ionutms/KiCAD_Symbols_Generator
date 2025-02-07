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

    # Ensure the output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

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
    input_files = [
        "UNITED_IC_ADI.kicad_sym",
        "UNITED_SOLDER_JUMPERS.kicad_sym",
        "UNITED_TEST_POINTS.kicad_sym",
        "UNITED_MODULES_DATA_BASE.kicad_sym",
        "UNITED_CRYSTALS_DATA_BASE.kicad_sym",
        "UNITED_MOUSE_BITES_DATA_BASE.kicad_sym",
    ]

    # Get script location
    script_dir = Path(__file__).parent

    # Navigate to project root from script location
    project_root = script_dir.parent

    for input_file in input_files:
        # Construct paths for input and output
        input_path = project_root / "symbols" / input_file
        output_path = (
            project_root / "data" / input_file.replace(".kicad_sym", ".csv")
        )

        print(f"Script directory: {script_dir}")
        print(f"Project root directory: {project_root}")
        print(f"Looking for input file at: {input_path}")
        print(f"Attempting to write output to: {output_path}")
        print(f"Output directory exists: {output_path.parent.exists()}")

        # Check if file exists
        if not input_path.exists():
            print(f"Error: Input file not found: {input_path}")
            sys.exit(1)

        # Read the file
        with input_path.open() as file:
            content = file.read()

        # Parse and write results to CSV
        symbols = parse_kicad_symbol_file(content)

        # Create data directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Created/verified output directory: {output_path.parent}")

        write_symbols_to_csv(symbols, output_path)
        print(f"Symbol information has been written to: {output_path}")
