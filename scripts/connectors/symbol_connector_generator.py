"""KiCad Connector Symbol Generator.

Generates KiCad symbol files for connectors from CSV data.
Modified to match specific pin and field positioning requirements.
"""

from pathlib import Path
from typing import TextIO

from utilities import file_handler_utilities, symbol_utils


def generate_kicad_symbol(
    input_csv_file: str,
    output_symbol_file: str,
) -> None:
    """Generate a KiCad symbol file from CSV data for connectors.

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
    write_symbol_drawing(
        symbol_file,
        symbol_name,
        component_data,
        number_of_rows,
    )
    symbol_file.write(")")


def write_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
    component_data: dict[str, str],
    number_of_rows: int,
) -> None:
    """Write the drawing for a connector symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
        component_data (Dict[str, str]): Data for the component.
        number_of_rows (int): Number of rows of the symbol.

    Returns:
        None

    """
    pin_count = int(component_data.get("Pin Count", "2"))
    pin_spacing = 2.54

    min_height = 7.62
    calculated_height = (pin_count * pin_spacing) + 2.54
    rectangle_height = max(min_height, calculated_height)

    symbol_file.write(f'\t\t(symbol "{symbol_name}_0_0"\n')

    start_y = (pin_count - 1) * pin_spacing / 2

    if number_of_rows == 2:  # noqa: PLR2004
        for pin_num in range(1, pin_count * 2, 2):
            y_pos = start_y - (pin_num - 1) * pin_spacing / 2
            symbol_utils.write_pin(symbol_file, -5.08, y_pos, 0, str(pin_num))
            symbol_utils.write_pin(
                symbol_file,
                5.08,
                y_pos,
                180,
                str(pin_num + 1),
            )
    else:
        for pin_num in range(1, pin_count + 1):
            y_pos = start_y - (pin_num - 1) * pin_spacing
            symbol_utils.write_pin(symbol_file, -5.08, y_pos, 0, str(pin_num))

    symbol_file.write("\t\t)\n")

    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')
    write_rectangle(
        symbol_file,
        -2.54,
        rectangle_height / 2,
        2.54,
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
