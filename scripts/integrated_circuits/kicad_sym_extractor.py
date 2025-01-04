"""Extracts symbol information from a KiCad symbol library file (.kicad_sym).

This script reads a KiCad symbol library file and extracts all symbol names
and properties defined in the file. It assumes that the symbol library file
is in the same directory as the script.
"""

from __future__ import annotations

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


def print_symbol_info(symbols: dict[str, dict[str, str]]) -> None:
    """Print all symbols and their properties.

    Args:
        symbols (dict[str, dict[str, str]]):
            A dictionary of symbols and their properties

    Returns:
        None

    """
    for symbol_name, properties in symbols.items():
        print("Symbol Name:", symbol_name)
        print("\nProperties:")
        print("-" * 50)
        for name, value in properties.items():
            print(f"{name}: {value}")
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    filename = "IC_ADI.kicad_sym"
    # Get the directory where the script is located
    script_dir = Path(__file__).parent

    # Construct the full path to the kicad file
    file_path = script_dir / filename

    print(f"Looking for file at: {file_path}")

    # Check if file exists
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    # Read the file
    with file_path.open() as file:
        content = file.read()

    # Parse and print results
    symbols = parse_kicad_symbol_file(content)
    print_symbol_info(symbols)
