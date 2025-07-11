"""KiCad Connector Symbol Generator.

Generates KiCad symbol files for tactile switches from CSV data.
Modified to match specific pin and field positioning requirements.
"""

from pathlib import Path
from typing import TextIO, List, Tuple

from utilities import file_handler_utilities, symbol_utils
from symbol_tactile_switches_specs import SeriesSpec


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
        write_tactile_switch_with_led_symbol_drawing(
            symbol_file,
            symbol_name,
            component_data,
            number_of_rows,
            led_color=ts29_series_led_colors.get(series),
        )

    elif ts28_series_led_colors.get(series):
        write_tactile_switch_with_led_symbol_drawing_v2(
            symbol_file,
            symbol_name,
            component_data,
            number_of_rows,
            led_color=ts28_series_led_colors.get(series),
        )

    else:
        write_tactile_switch_symbol_drawing(
            symbol_file,
            symbol_name,
            component_data,
            number_of_rows,
        )
    symbol_file.write(")")


def write_tactile_switch_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
    component_data: dict[str, str],
    number_of_rows: int,
) -> None:
    """Write the drawing for a tactile switch symbol.

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

    # Check for override pin specs
    override_pins = get_override_pins_specs(component_data.get("Series", ""))

    if override_pins:
        for pin_num, x_pos, y_pos, angle in override_pins:
            symbol_utils.write_pin(symbol_file, x_pos, y_pos, angle, pin_num)
    else:
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
                symbol_utils.write_pin(
                    symbol_file, -5.08, y_pos, 0, str(pin_num)
                )

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


def write_tactile_switch_with_led_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
    component_data: dict[str, str],
    number_of_rows: int,
    led_color: dict[str, int],
) -> None:
    """Write the drawing for a tactile switch symbol.

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

    # Check for override pin specs
    override_pins = get_override_pins_specs(component_data.get("Series", ""))

    if override_pins:
        for pin_num, x_pos, y_pos, angle in override_pins:
            symbol_utils.write_pin(symbol_file, x_pos, y_pos, angle, pin_num)
    else:
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
                symbol_utils.write_pin(
                    symbol_file, -5.08, y_pos, 0, str(pin_num)
                )

    symbol_file.write(f"""
			(polyline
				(pts
					(xy -2.286 1.27) (xy -2.286 -1.27)
                    (xy -2.286 0) (xy -3.81 0)
				)
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(circle
				(center -1.27 1.27)
				(radius 0.254)
				(stroke (width 0) (type solid))
				(fill (type outline))
			)
			(circle
				(center -1.27 -1.27)
				(radius 0.254)
				(stroke (width 0) (type solid))
				(fill (type outline))
			)
			(polyline
				(pts
					(xy 0 2.54) (xy -2.54 2.54)
                    (xy -1.27 2.54) (xy -1.27 1.27)
				)
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(polyline
				(pts
					(xy 0 -2.54) (xy -2.54 -2.54)
                    (xy -1.27 -2.54) (xy -1.27 -1.27)
				)
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(polyline
				(pts
					(xy 2.54 -2.54) (xy 2.54 -1.27) (xy 3.81 -1.27)
                    (xy 2.54 -1.27) (xy 3.81 1.27) (xy 2.54 1.27)
                    (xy 2.54 2.54) (xy 2.54 1.27) (xy 1.27 1.27)
                    (xy 2.54 -1.27) (xy 1.27 -1.27) (xy 2.54 -1.27)
                    (xy 2.54 -2.54)
				)
				(stroke (width 0.2032) (type solid))
				(fill
                    (type color)
                    (color
                        {led_color["R"]} {led_color["G"]} {led_color["B"]} 1)
                )
			)
			(polyline
				(pts
					(xy 4.445 -0.508) (xy 5.969 -2.032) (xy 5.969 -1.27)
                    (xy 5.969 -2.032) (xy 5.207 -2.032)
				)
				(stroke (width 0.2032) (type default))
				(fill (type none))
			)
			(polyline
				(pts
					(xy 4.445 -1.778) (xy 5.969 -3.302) (xy 5.969 -2.54)
                    (xy 5.969 -3.302) (xy 5.207 -3.302)
				)
				(stroke (width 0.2032) (type default))
				(fill (type none))
			)
    """)

    symbol_file.write("\t\t)\n")

    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')
    symbol_file.write("\t\t)\n")


def write_tactile_switch_with_led_symbol_drawing_v2(
    symbol_file: TextIO,
    symbol_name: str,
    component_data: dict[str, str],
    number_of_rows: int,
    led_color: dict[str, int],
) -> None:
    """Write the drawing for a tactile switch symbol.

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

    # Check for override pin specs
    override_pins = get_override_pins_specs(component_data.get("Series", ""))

    if override_pins:
        for pin_num, x_pos, y_pos, angle in override_pins:
            symbol_utils.write_pin(symbol_file, x_pos, y_pos, angle, pin_num)
    else:
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
                symbol_utils.write_pin(
                    symbol_file, -5.08, y_pos, 0, str(pin_num)
                )

    symbol_file.write(f"""
			(polyline
				(pts
					(xy -4.826 1.27) (xy -4.826 -1.27)
                    (xy -4.826 0) (xy -6.35 0)
				)
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(circle
				(center -3.81 1.27)
				(radius 0.254)
				(stroke (width 0) (type solid))
				(fill (type outline))
			)
			(circle
				(center -3.81 -1.27)
				(radius 0.254)
				(stroke (width 0) (type solid))
				(fill (type outline))
			)
			(polyline
				(pts
					(xy -2.54 2.54) (xy -5.08 2.54)
                    (xy -3.81 2.54) (xy -3.81 1.27)
				)
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(polyline
				(pts
					(xy -2.54 -2.54) (xy -5.08 -2.54)
                    (xy -3.81 -2.54) (xy -3.81 -1.27)
				)
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(polyline
				(pts
					(xy 5.08 -2.54) (xy 5.08 -1.27) (xy 6.35 -1.27)
                    (xy 5.08 -1.27) (xy 6.35 1.27) (xy 5.08 1.27)
                    (xy 5.08 2.54) (xy 5.08 1.27) (xy 3.81 1.27)
                    (xy 5.08 -1.27) (xy 3.81 -1.27) (xy 5.08 -1.27)
                    (xy 5.08 -2.54)
				)
				(stroke (width 0.2032) (type solid))
				(fill
					(type color)
                    (color
                        {led_color["R"]} {led_color["G"]} {led_color["B"]} 1)
				)
			)
			(polyline
				(pts
					(xy 6.985 -0.508) (xy 8.509 -2.032) (xy 8.509 -1.27)
                    (xy 8.509 -2.032) (xy 7.747 -2.032)
				)
				(stroke (width 0.2032) (type default))
				(fill (type none))
			)
			(polyline
				(pts
					(xy 6.985 -1.778) (xy 8.509 -3.302) (xy 8.509 -2.54)
                    (xy 8.509 -3.302) (xy 7.747 -3.302)
				)
				(stroke (width 0.2032) (type default))
				(fill (type none))
			)			
            (polyline
				(pts
					(xy 0 2.54) (xy 0 -2.54) (xy 0 0) (xy 1.27 0)
                    (xy 1.27 1.27) (xy 1.27 -1.27)
				)
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(polyline
				(pts
					(xy 1.778 -0.762) (xy 1.778 0.762)
				)
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(polyline
				(pts
					(xy 2.286 -0.254) (xy 2.286 0.254)
				)
				(stroke (width 0) (type default))
				(fill (type none))
			)
    """)

    symbol_file.write("\t\t)\n")

    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')
    symbol_file.write("\t\t)\n")


def get_override_pins_specs(
    series: str,
) -> List[Tuple[str, float, float, int]]:
    """Retrieve override pin specifications for a given series.

    Args:
        series (str): The series identifier for the tactile switch.

    Returns:
        List[Tuple[str, float, float, int]]:
            List of tuples containing pin number, x, y, and angle.
        Returns empty list if no override specs are found.
    """
    from symbol_tactile_switches_specs import SYMBOLS_SPECS

    specs = SYMBOLS_SPECS.get(series)
    if specs and specs.override_pins_specs:
        return specs.override_pins_specs
    return []
