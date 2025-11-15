"""KiCad Seven Segment Display Symbol Generator."""

from pathlib import Path
from typing import TextIO

import symbol_seven_segm_displays_specs
from utilities import file_handler_utilities, symbol_utils


def generate_kicad_symbol(
    input_csv_file: str,
    output_symbol_file: str,
) -> None:
    """Generate a KiCad symbol file from CSV data."""
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
    """Write a single component to the KiCad symbol file."""
    symbol_name = component_data.get("Symbol Name", "")
    symbol_utils.write_symbol_header(symbol_file, symbol_name)
    pin_count = int(component_data.get("Pin Count", "14"))

    pins_per_side = pin_count // 2
    pin_spacing = 2.54
    rectangle_height = max(5.08, pins_per_side * pin_spacing + 2.54)

    extra_offset = round((rectangle_height / 2.54) / 2)

    symbol_utils.write_properties(
        symbol_file, component_data, property_order, extra_offset + 1
    )

    write_symbol_drawing(symbol_file, symbol_name, component_data)
    symbol_file.write(")")


def write_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
    component_data: dict[str, str],
) -> None:
    """Write the drawing for a seven segment display symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
        component_data (dict[str, str]): Data for the component.

    Returns:
        None

    """
    pin_count = int(component_data.get("Pin Count", "14"))
    pin_spacing = 2.54

    series_name = component_data.get("Series", "")
    series_spec = symbol_seven_segm_displays_specs.SYMBOLS_SPECS[series_name]
    rectangle_width = series_spec.rectangle_width
    rect_half_width = rectangle_width / 2

    # Use per-series symbol pin length if provided
    pin_length = getattr(series_spec, "symbol_pin_length", 2.54)

    # Compute X positions for pin anchors
    left_pin_x_default = -rect_half_width - pin_length
    right_pin_x_default = rect_half_width + pin_length
    left_pin_x = left_pin_x_default
    right_pin_x = right_pin_x_default

    pins_per_side = pin_count // 2
    rectangle_height = max(5.08, pins_per_side * pin_spacing + 2.54)

    symbol_file.write(f'\t\t(symbol "{symbol_name}_0_0"\n')

    # For symmetrical layout, we'll divide pins equally on left and right
    if series_spec.pin_names:
        all_pin_ids = list(series_spec.pin_names.keys())
    else:
        all_pin_ids = [str(i) for i in range(1, pin_count + 1)]

    # Split pins equally between left and right sides based on mounting style
    if component_data.get("Mounting Style", "") == "Surface Mount":
        left_pins = all_pin_ids[:pins_per_side]
        right_pins = all_pin_ids[pins_per_side:pin_count]
    else:  # Through hole
        left_pins = all_pin_ids[:pins_per_side]
        right_pins = all_pin_ids[pins_per_side:pin_count]

    # Calculate starting Y position to center the pins
    total_pins_for_centering = max(len(left_pins), len(right_pins))
    start_y = (total_pins_for_centering - 1) * pin_spacing / 2

    # Place pins on left side (top to bottom)
    for index, pin_id in enumerate(left_pins):
        y_pos = start_y - index * pin_spacing
        pin_name = (
            series_spec.pin_names.get(pin_id, "")
            if series_spec.pin_names
            else ""
        )
        symbol_utils.write_pin(
            symbol_file,
            left_pin_x,
            y_pos,
            0,
            pin_id,
            pin_name,
            length=pin_length,
        )

    # Place pins on right side (top to bottom to maintain symmetry)
    for index, pin_id in enumerate(right_pins):
        y_pos = start_y - index * pin_spacing
        pin_name = (
            series_spec.pin_names.get(pin_id, "")
            if series_spec.pin_names
            else ""
        )
        symbol_utils.write_pin(
            symbol_file,
            right_pin_x,
            y_pos,
            180,
            pin_id,
            pin_name,
            length=pin_length,
        )

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
    """Write a rectangle to the KiCad symbol file."""
    symbol_file.write(f"""
        (rectangle
            (start {start_x} {start_y})
            (end {end_x} {end_y})
            (stroke (width 0.254) (type solid) )
            (fill (type none) )
        )
        """)
