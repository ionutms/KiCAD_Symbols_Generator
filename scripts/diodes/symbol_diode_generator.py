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
    """Generate a KiCad symbol file from CSV data for inductors.

    Args:
        input_csv_file (str): Path to the input CSV file with component data.
        output_symbol_file (str): Path for the output .kicad_sym file.
        encoding (str, optional):
            Character encoding to use. Defaults to 'utf-8'.

    Raises:
        FileNotFoundError: If the input CSV file is not found.
        csv.Error: If there's an error reading the CSV file.
        IOError: If there's an error writing to the output file.

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


def write_component(  # noqa: C901, PLR0912
    symbol_file: TextIO,
    component_data: dict[str, str],
    property_order: list[str],
) -> None:
    """Write a single component to the KiCad symbol file.

    Args:
        symbol_file (TextIO): File handle for the output symbol file.
        component_data (dict): Dictionary of component properties.
        property_order (list): List of property names in desired order

    Returns:
        None

    """
    symbol_name = component_data.get("Symbol Name", "")
    symbol_utils.write_symbol_header(symbol_file, symbol_name)

    if symbol_name in ("D_SP4020-01FTG-C", "D_SP4020-01FTG"):
        symbol_utils.write_properties(
            symbol_file,
            component_data,
            property_order,
            text_y_offset=3,
        )
    else:
        symbol_utils.write_properties(
            symbol_file,
            component_data,
            property_order,
            text_y_offset=2,
        )

    if component_data.get("Diode Type") == "Schottky":
        symbol_utils.write_schottky_symbol_drawing(symbol_file, symbol_name)
    if component_data.get("Diode Type") == "Zener":
        symbol_utils.write_zener_symbol_drawing(symbol_file, symbol_name)
    if component_data.get("Diode Type") == "Rectifier":
        symbol_utils.write_rectifier_symbol_drawing(symbol_file, symbol_name)
    if component_data.get("Diode Type") == "Unidirectional TVS":
        if symbol_name == "D_SP4020-01FTG":
            symbol_utils.write_unidirectional_tvs_symbol_drawing_v2(
                symbol_file,
                symbol_name,
            )
        else:
            symbol_utils.write_unidirectional_tvs_symbol_drawing(
                symbol_file,
                symbol_name,
            )
    if component_data.get("Diode Type") == "Bidirectional TVS":
        if symbol_name == "D_SP4020-01FTG-C":
            symbol_utils.write_bidirectional_tvs_symbol_drawing_v2(
                symbol_file,
                symbol_name,
            )
        else:
            symbol_utils.write_bidirectional_tvs_symbol_drawing(
                symbol_file,
                symbol_name,
            )
    if (
        component_data.get("Diode Type")
        == "Dual Small Signal Switching Diodes"
    ):
        symbol_utils.write_dual_small_signal_diodes_symbol_drawing_v1(
            symbol_file,
            symbol_name,
        )
    if component_data.get("Diode Type") == "Small Signal Schottky Diodes":
        symbol_utils.write_small_signal_schottky_diodes_symbol_drawing(
            symbol_file,
            symbol_name,
        )
    if component_data.get("Diode Type") == "Red LED":
        symbol_utils.write_red_led_symbol_drawing(symbol_file, symbol_name)
    if component_data.get("Diode Type") == "Green LED":
        symbol_utils.write_green_led_symbol_drawing(symbol_file, symbol_name)
    symbol_file.write(")")
