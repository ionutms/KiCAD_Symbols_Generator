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

from symbol_transformer_specs import SYMBOLS_SPECS, SidePinConfig
from utilities import file_handler_utilities, symbol_utils


def generate_kicad_symbol(
    input_csv_file: str,
    output_symbol_file: str,
) -> None:
    """Generate a KiCad symbol file from CSV data for inductors.

    Args:
        input_csv_file (str): Path to the input CSV file.
        output_symbol_file (str): Path to the output symbol file.

    Raises:
        FileNotFoundError: If the input CSV file is not found.
        csv.Error: If there is an error processing the CSV file.
        OSError: If there is an I/O error when generating the symbol file.

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


def convert_pin_config(
    spec_config: SidePinConfig,
) -> dict[str, list[dict[str, float | bool]]]:  # noqa: FA102
    """Convert pin configuration data to dictionary format.

    Args:
        spec_config (SidePinConfig): Pin configuration from

    Returns:
        dict[str, list[dict[str, float | bool]]]: Pin configuration data

    """
    config = {
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
    }

    # Only add right_alternative if it exists and is not None
    if spec_config.right_alternative is not None:
        config["right_alternative"] = [
            {
                "number": pin.number,
                "y_pos": pin.y_pos,
                "pin_type": pin.pin_type,
                "lenght": pin.lenght,
                "hide": pin.hide,
            }
            for pin in spec_config.right_alternative
        ]
    else:
        config["right_alternative"] = []

    return config


def write_component(
    symbol_file: TextIO,
    component_data: dict[str, str],
    property_order: list[str],
) -> None:
    """Write a single component to the KiCad symbol file.

    Args:
        symbol_file (TextIO): File handle for the symbol file.
        component_data (dict[str, str]): Data for the component.
        property_order (list[str]): Order of properties to write.

    Returns:
        None

    """
    symbol_name = component_data.get("Symbol Name", "")
    series = component_data.get("Series", "")

    # Get pin configuration from SYMBOLS_SPECS if available
    series_spec = SYMBOLS_SPECS.get(series)
    pin_config = convert_pin_config(series_spec.pin_config)

    symbol_utils.write_symbol_header(symbol_file, symbol_name)
    if component_data.get("Series") in ("ZA9384", "ZA9644"):
        symbol_utils.write_properties(
            symbol_file,
            component_data,
            property_order,
            3,
        )
        symbol_utils.write_transformer_symbol_drawing(
            symbol_file,
            symbol_name,
            pin_config,
        )
    if component_data.get("Series") in ("750315836"):
        symbol_utils.write_properties(
            symbol_file,
            component_data,
            property_order,
            5,
        )
        symbol_utils.write_transformer_symbol_drawing_v2(
            symbol_file,
            symbol_name,
            pin_config,
        )
    if component_data.get("Series") in ("YA8779"):
        symbol_utils.write_properties(
            symbol_file,
            component_data,
            property_order,
            4,
        )
        symbol_utils.write_transformer_symbol_drawing_v3(
            symbol_file,
            symbol_name,
            pin_config,
        )
    if component_data.get("Series") in ("YA8916", "YA8864"):
        symbol_utils.write_properties(
            symbol_file,
            component_data,
            property_order,
            6,
        )
        symbol_utils.write_transformer_symbol_drawing_v4(
            symbol_file,
            symbol_name,
            pin_config,
        )
    if component_data.get("Series") in ("PL160X9-102L"):
        symbol_utils.write_properties(
            symbol_file,
            component_data,
            property_order,
            9,
        )
        symbol_utils.write_transformer_symbol_drawing_v5(
            symbol_file,
            symbol_name,
            pin_config,
        )
    symbol_file.write(")")
