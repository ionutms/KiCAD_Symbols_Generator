"""KiCad Tactile Switch Symbol Generator.

Generates KiCad symbol files for tactile switches from CSV data.
Creates symbols with standard switch graphics and optional LED indicators
for specific series with color-coded LED support.
"""

from pathlib import Path
from typing import TextIO

from utilities import file_handler_utilities, symbol_utils
from symbol_tactile_switches_specs import SYMBOLS_SPECS


def generate_kicad_symbol(
    input_csv_file: str,
    output_symbol_file: str,
) -> None:
    """Generate a KiCad symbol file from CSV data for tactile switches.

    Reads component data from CSV file and generates corresponding KiCad
    symbol definitions with appropriate pin configurations and graphical
    representations.

    Args:
        input_csv_file: Path to the input CSV file containing component data.
        output_symbol_file: Path for the output .kicad_sym file to be created.
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
    """Write a single component symbol to the KiCad symbol file.

    Determines the appropriate symbol type based on component series and
    generates the corresponding symbol definition with pins, properties,
    and graphical elements.

    Args:
        symbol_file: File object for writing the symbol file.
        component_data: Dictionary containing component specifications.
        property_order: Ordered list of property names for consistent
            output formatting.
    """
    symbol_name = component_data.get("Symbol Name", "")
    number_of_rows = int(component_data.get("Number of Rows", "1"))
    symbol_utils.write_symbol_header(symbol_file, symbol_name)
    pin_count = int(component_data.get("Pin Count", "1"))
    row_count = int(component_data.get("Number of Rows", "1"))
    extra_offset = (
        ((pin_count / row_count) / 2)
        if row_count == 1
        else (pin_count / row_count)
    )

    symbol_utils.write_properties(
        symbol_file,
        component_data,
        property_order,
        1 + extra_offset,
        2,
    )
    # Define the LED color mapping
    ts28_series_led_colors = {
        "TS28-63-63-BL-260-RA-D": {"R": 0, "G": 0, "B": 255},
        "TS28-63-63-R-260-RA-D": {"R": 255, "G": 0, "B": 0},
        "TS28-63-63-G-260-RA-D": {"R": 0, "G": 255, "B": 0},
        "TS28-63-63-Y-260-RA-D": {"R": 255, "G": 255, "B": 0},
    }
    ts29_series_led_colors = {
        "TS29-1212-1-R-300-D": {"R": 255, "G": 0, "B": 0},
        "TS29-1212-1-G-300-D": {"R": 0, "G": 255, "B": 0},
        "TS29-1212-1-BL-300-D": {"R": 0, "G": 0, "B": 255},
        "TS29-1212-1-WT-300-D": {"R": 255, "G": 255, "B": 255},
        "TS29-1212-1-Y-300-D": {"R": 255, "G": 255, "B": 0},
    }

    series = component_data.get("Series", "")

    if ts29_series_led_colors.get(series):
        symbol_utils.write_tactile_switch_with_led_symbol_drawing(
            symbol_file=symbol_file,
            symbol_name=symbol_name,
            component_data=component_data,
            number_of_rows=number_of_rows,
            led_color=ts29_series_led_colors.get(series),
            specs_dict=SYMBOLS_SPECS,
        )

    elif ts28_series_led_colors.get(series):
        symbol_utils.write_tactile_switch_with_led_symbol_drawing_v2(
            symbol_file=symbol_file,
            symbol_name=symbol_name,
            component_data=component_data,
            number_of_rows=number_of_rows,
            led_color=ts28_series_led_colors.get(series),
            specs_dict=SYMBOLS_SPECS,
        )

    else:
        symbol_utils.write_tactile_switch_symbol_drawing(
            symbol_file=symbol_file,
            symbol_name=symbol_name,
            component_data=component_data,
            number_of_rows=number_of_rows,
            specs_dict=SYMBOLS_SPECS,
        )
    symbol_file.write(")")
