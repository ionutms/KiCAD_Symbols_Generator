"""KiCad Diode Symbol Generator.

This module provides functionality to generate KiCad symbol files from CSV
data for diodes. It creates symbol files with proper diode properties
and graphical representation in both horizontal and vertical layouts.

The main function, generate_kicad_symbol, reads data from a CSV file and
produces a .kicad_sym file with the symbol definition, including properties
and graphical representation.

Usage:
    python kicad_diode_symbol_generator.py

Or import and use the generate_kicad_symbol function in your own script.

Dependencies:
    - csv (Python standard library)
"""

from pathlib import Path
from typing import TextIO

from utilities import file_handler_utilities, symbol_utils


def generate_kicad_symbol(
    input_csv_file: str,
    output_symbol_file: str,
) -> None:
    """Generate a KiCad symbol file for diodes.

    Reads diode data from a CSV file and generates a KiCad symbol file
    with the appropriate properties and graphical representation.

    Args:
        input_csv_file (str): Path to the input CSV file with diode data.
        output_symbol_file (str): Path to the output KiCad symbol file.

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
    """Write a diode component to a KiCad symbol file.

    Args:
        symbol_file (TextIO): The file handle for the KiCad symbol file.
        component_data (dict): A dictionary of diode properties.
        property_order (list): The order of properties to write.

    Returns:
        None

    """
    symbol_name = component_data.get("Symbol Name", "")
    symbol_utils.write_symbol_header(symbol_file, symbol_name)
    symbol_utils.write_properties(
        symbol_file,
        component_data,
        property_order,
        3,
    )
    if component_data.get("Transistor Type") == "P-Channel":
        if component_data.get("Series") == "ZXMP6A17E6TA":
            symbol_utils.write_p_mos_transistor_symbol_drawing_2(
                symbol_file,
                symbol_name,
            )
        else:
            symbol_utils.write_p_mos_transistor_symbol_drawing(
                symbol_file,
                symbol_name,
            )
    if component_data.get("Transistor Type") == "N-Channel":
        if component_data.get("Series") == "BSS123WQ-7-F":
            symbol_utils.write_n_mos_basic_transistor_symbol_drawing(
                symbol_file,
                symbol_name,
            )
        else:
            symbol_utils.write_n_mos_transistor_symbol_drawing(
                symbol_file,
                symbol_name,
            )
    if component_data.get("Transistor Type") == "N-Channel Dual":
        symbol_utils.write_n_mos_dual_transistor_symbol_drawing(
            symbol_file,
            symbol_name,
        )
    if component_data.get("Transistor Type") == "P-Channel Dual":
        symbol_utils.write_p_mos_dual_transistor_symbol_drawing(
            symbol_file,
            symbol_name,
        )
    symbol_file.write(")")
