"""Generate a KiCad symbol file from CSV data for inductors.

This module provides functions to generate a KiCad symbol file from CSV data
for inductors. The CSV data should contain the following columns:
- Symbol Name
- Manufacturer
- Manufacturer Part Number
- Description
- Value
- Tolerance
- Power Rating
- Series
- Datasheet
- TrustedParts Link
- Maximum DC Current
- Maximum DC Resistance

The generated symbol file will contain a symbol for each inductor in the CSV
data. The symbol will include the inductor's properties and a graphical
representation of the inductor.
"""

from pathlib import Path
from typing import TextIO

from utilities import file_handler_utilities, symbol_utils


def generate_kicad_symbol(
    input_csv_file: str,
    output_symbol_file: str,
) -> None:
    """Generate a KiCad symbol file from CSV data for inductors.

    Args:
        input_csv_file (str): Path to the input CSV file.
        output_symbol_file (str): Path to the output symbol file.

    Returns:
        None

    """
    component_data_list = file_handler_utilities.read_csv_data(input_csv_file)
    all_properties = symbol_utils.get_all_properties(component_data_list)

    with Path.open(output_symbol_file, "w", encoding="utf-8") as symbol_file:
        symbol_utils.write_header(symbol_file)
        for component_data in component_data_list:
            write_component(symbol_file, component_data, all_properties)
        symbol_file.write(")")


def write_component(
    symbol_file: TextIO,
    component_data: dict[str, str],
    property_order: list[str],
) -> None:
    """Write a single component to the KiCad symbol file.

    Args:
        symbol_file (TextIO): File handle for the symbol file.
        component_data (dict): Component data from the CSV file.
        property_order (list): Order of properties to write.

    Returns:
        None

    """
    symbol_name = component_data.get("Symbol Name", "")
    symbol_utils.write_symbol_header(symbol_file, symbol_name)
    if component_data.get("Reference") == "E":
        symbol_utils.write_properties(
            symbol_file,
            component_data,
            property_order,
            text_y_offset=2,
        )
        symbol_utils.write_ferrite_bead_symbol_drawing(
            symbol_file,
            symbol_name,
        )
    else:
        symbol_utils.write_properties(
            symbol_file,
            component_data,
            property_order,
            text_y_offset=1,
        )
        symbol_utils.write_inductor_symbol_drawing(symbol_file, symbol_name)
    symbol_file.write(")")
