"""KiCad Connector Symbol Generator.

Generates KiCad symbol files for tactile switches from CSV data.
Modified to match specific pin and field positioning requirements.
"""

from pathlib import Path
from typing import TextIO

from utilities import file_handler_utilities, symbol_utils


def generate_kicad_symbol(
    input_csv_file: str,
    output_symbol_file: str,
) -> None:
    """Generate a KiCad symbol file from CSV data for tactile switches.

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
    pin_spacing = 5.08 * 2

    symbol_file.write(f'\t\t(symbol "{symbol_name}_0_0"\n')

    start_y = (pin_count - 1) * pin_spacing / 2

    def toggle_angle(current):
        return 90 if current == 270 else 270

    if number_of_rows == 2:  # noqa: PLR2004
        angle = 270  # Start with 270
        for pin_num in range(1, pin_count * 2, 2):
            y_pos = start_y - (pin_num - 1) * pin_spacing / 2

            # Both pins in this row use the same angle
            symbol_utils.write_pin(
                symbol_file, -2.54 / 2, y_pos, angle, str(pin_num)
            )
            symbol_utils.write_pin(
                symbol_file, 2.54 / 2, y_pos, angle, str(pin_num + 1)
            )

            # Toggle angle for next row
            angle = toggle_angle(angle)
    else:
        for pin_num in range(1, pin_count + 1):
            y_pos = start_y - (pin_num - 1) * pin_spacing
            symbol_utils.write_pin(symbol_file, -5.08, y_pos, 0, str(pin_num))

    symbol_file.write(f"""
			(circle
				(center 0 1.27)
				(radius 0.254)
				(stroke (width 0) (type solid))
				(fill (type outline))
			)
			(circle
				(center 0 -1.27)
				(radius 0.254)
				(stroke (width 0) (type solid))
				(fill (type outline))
			)
			(polyline
				(pts
					(xy 1.27 2.54) (xy -1.27 2.54) (xy 0 2.54)
                    (xy 0 1.27) (xy 1.27 -1.27)
				)
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(polyline
				(pts
					(xy 1.27 -2.54) (xy -1.27 -2.54)
                    (xy 0 -2.54) (xy 0 -1.27)
				)
				(stroke (width 0) (type default))
				(fill (type none))
			)
    """)

    symbol_file.write("\t\t)\n")

    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')
    symbol_file.write("\t\t)\n")
