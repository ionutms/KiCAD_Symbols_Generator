"""KiCad Inductor Symbol Generator.

This module provides functionality to generate KiCad symbol files from CSV
data for inductors. It creates symbol files with proper inductor properties
and graphical representation in horizontal layout.

The main function, generate_kicad_symbol, reads data from a CSV file and
produces a .kicad_sym file with the symbol definition, including properties
and graphical representation.

Usage:
    python kicad_inductor_symbol_generator.py

Or import and use the generate_kicad_symbol function in your own script.

Dependencies:
    - csv (Python standard library)
"""

from pathlib import Path
from typing import TextIO

from symbol_coupled_inductors_specs import SYMBOLS_SPECS, SidePinConfig
from utilities import file_handler_utilities, symbol_utils


def generate_kicad_symbol(
    input_csv_file: str,
    output_symbol_file: str,
) -> None:
    """Generate a KiCad symbol file from CSV data for inductors.

    Args:
        input_csv_file (str): Path to the input CSV file with component data.
        output_symbol_file (str): Path for the output .kicad_sym file.

    Raises:
        FileNotFoundError: If the input CSV file is not found.
        csv.Error: If there's an error reading the CSV file.
        IOError: If there's an error writing to the output file.

    """
    component_data_list = file_handler_utilities.read_csv_data(input_csv_file)
    all_properties = symbol_utils.get_all_properties(component_data_list)

    with Path.open(output_symbol_file, "w", encoding="utf-8") as symbol_file:
        symbol_utils.write_header(symbol_file)
        for component_data in component_data_list:
            write_component(symbol_file, component_data, all_properties)
        symbol_file.write(")")


def convert_pin_config(spec_config: SidePinConfig) -> dict[str, list]:
    """Convert a SidePinConfig from specs.

    Args:
        spec_config: Optional[SidePinConfig] from SYMBOLS_SPECS

    Returns:
        dict[str, list]: Dictionary with left and right pin configurations.

    """
    return {
        "left": [
            {
                "number": pin.number,
                "y_pos": pin.y_pos,
                "pin_type": pin.pin_type,
                "lenght": pin.lenght,
                "hide": pin.hide,
            }
            for pin in spec_config.left
        ],
        "right": [
            {
                "number": pin.number,
                "y_pos": pin.y_pos,
                "pin_type": pin.pin_type,
                "lenght": pin.lenght,
                "hide": pin.hide,
            }
            for pin in spec_config.right
        ],
        "right_alternative": [
            {
                "number": pin.number,
                "y_pos": pin.y_pos,
                "pin_type": pin.pin_type,
                "lenght": pin.lenght,
                "hide": pin.hide,
            }
            for pin in spec_config.right_alternative
        ],
    }


def write_component(
    symbol_file: TextIO,
    component_data: dict[str, str],
    property_order: list[str],
) -> None:
    """Write a single component to the KiCad symbol file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        component_data (Dict[str, str]): Data for a single component.
        property_order (List[str]): Ordered list of property names.

    Returns:
        None

    """
    symbol_name = component_data.get("Symbol Name", "")
    series = component_data.get("Series", "")

    # Get pin configuration from SYMBOLS_SPECS if available
    series_spec = SYMBOLS_SPECS.get(series)
    pin_config = convert_pin_config(series_spec.pin_config)

    symbol_utils.write_symbol_header(symbol_file, symbol_name)
    symbol_utils.write_properties(
        symbol_file,
        component_data,
        property_order,
        3,
    )
    symbol_utils.write_coupled_inductor_symbol_drawing(
        symbol_file,
        symbol_name,
        pin_config,
    )
    symbol_file.write(")")
