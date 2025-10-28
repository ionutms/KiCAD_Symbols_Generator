"""KiCad Terminal Block Symbol Generator.

Generates KiCad symbol files for terminal blocks from CSV data.
Modified to match specific pin and field positioning requirements.
"""

from pathlib import Path
from typing import TextIO

import symbol_terminal_block_specs
from utilities import file_handler_utilities, symbol_utils


def generate_kicad_symbol(
    input_csv_file: str,
    output_symbol_file: str,
) -> None:
    """Generate a KiCad symbol file from CSV data for terminal blocks.

    Args:
        input_csv_file (str): Path to the input CSV file with component data.
        output_symbol_file (str): Path for the output .kicad_sym file.

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
        symbol_file (TextIO): File object for writing the symbol file.
        component_data (Dict[str, str]): Data for a single component.
        property_order (List[str]): Ordered list of property names.

    Returns:
        None

    """
    symbol_name = component_data.get("Symbol Name", "")
    symbol_utils.write_symbol_header(symbol_file, symbol_name)
    pin_count = int(component_data.get("Pin Count", "1"))
    row_count = int(component_data.get("Number of Rows", "1"))

    series_name = component_data.get("Series", "")
    rectangle_width = symbol_terminal_block_specs.SYMBOLS_SPECS[
        series_name
    ].rectangle_width

    rect_half_width = rectangle_width / 2

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
        rect_half_width + 2.54,
    )

    write_symbol_drawing(
        symbol_file,
        symbol_name,
        component_data,
    )
    symbol_file.write(")")


def write_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
    component_data: dict[str, str],
) -> None:
    """Write the drawing for a terminal block symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
        component_data (Dict[str, str]): Data for the component.

    Returns:
        None

    """
    pin_count = int(component_data.get("Pin Count", "2"))
    pin_spacing = 2.54

    series_name = component_data.get("Series", "")
    series_spec = symbol_terminal_block_specs.SYMBOLS_SPECS[series_name]
    rectangle_width = series_spec.rectangle_width
    rect_half_width = rectangle_width / 2

    min_height = 7.62
    calculated_height = (pin_count * pin_spacing) + 2.54
    rectangle_height = max(min_height, calculated_height)

    symbol_file.write(f'\t\t(symbol "{symbol_name}_0_0"\n')

    start_y = (pin_count - 1) * pin_spacing / 2

    if series_spec.pin_names:
        pin_numbers = list(series_spec.pin_names.keys())
    else:
        pin_numbers = list(range(1, pin_count + 1))

    for index, _ in enumerate(pin_numbers):
        y_pos = start_y - index * pin_spacing
        write_screw_symbol(symbol_file, 0, y_pos)

    symbol_file.write("\t\t)\n")

    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')
    write_rectangle(
        symbol_file,
        -rect_half_width,
        rectangle_height / 2,
        rect_half_width,
        -rectangle_height / 2,
    )
    symbol_file.write("\t\t)\n")


def write_rectangle(
    symbol_file: TextIO,
    start_x: float,
    start_y: float,
    end_x: float,
    end_y: float,
) -> None:
    """Write a rectangle to the KiCad symbol file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        start_x (float): X-coordinate of the start point.
        start_y (float): Y-coordinate of the start point.
        end_x (float): X-coordinate of the end point.
        end_y (float): Y-coordinate of the end point.

    Returns:
        None

    """
    symbol_file.write(f"""
        (rectangle
            (start {start_x} {start_y})
            (end {end_x} {end_y})
            (stroke (width 0.254) (type solid) )
            (fill (type none) )
        )
        """)


def write_screw_symbol(
    symbol_file: TextIO,
    start_x: float,
    start_y: float,
) -> None:
    """Write a rectangle to the KiCad symbol file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        start_x (float): X-coordinate of the start point.
        start_y (float): Y-coordinate of the start point.

    Returns:
        None

    """
    symbol_file.write(f"""
        (circle
            (center {start_x} {start_y})
            (radius 0.762)
            (stroke (width 0) (type default) )
            (fill (type none) )
        )
        (polyline
            (pts
                (xy 0.508 {start_y + 1.778 - 1.27})
                (xy -0.508 {start_y + 0.762 - 1.27})
            )
            (stroke (width 0) (type default) )
            (fill (type none) )
        )
        """)
