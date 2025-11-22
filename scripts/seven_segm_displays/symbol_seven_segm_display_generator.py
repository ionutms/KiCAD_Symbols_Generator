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

    # Get series name and spec to use rectangle height from spec
    series_name = component_data.get("Series", "")
    if series_name in symbol_seven_segm_displays_specs.SYMBOLS_SPECS:
        series_spec = symbol_seven_segm_displays_specs.SYMBOLS_SPECS[
            series_name
        ]
        rectangle_height = series_spec.rectangle_height
    else:
        rectangle_height = max(5.08, pins_per_side * pin_spacing + 2.54)

    extra_offset = round((rectangle_height / 2.54) / 2)

    symbol_utils.write_properties(
        symbol_file, component_data, property_order, extra_offset + 1, 13
    )

    write_symbol_drawing(symbol_file, symbol_name, component_data)
    symbol_file.write(")")


def convert_pin_config(
    spec_config: symbol_seven_segm_displays_specs.SidePinConfig,
) -> list[dict[str, float | bool | str | int]]:
    """Convert pin configuration data to dictionary format.

    Args:
        spec_config: Pin configuration from series spec

    Returns:
        list: Pin configuration data in dictionary format

    """
    pin_list = [
        {
            "number": pin.number,
            "x_pos": pin.x_pos,
            "y_pos": pin.y_pos,
            "rotation": pin.rotation,
            "pin_type": pin.pin_type,
            "length": pin.length,
            "hide": pin.hide,
        }
        for pin in spec_config.pins
    ]
    return pin_list


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
    rectangle_height = series_spec.rectangle_height
    rect_half_width = rectangle_width / 2

    # Use per-series symbol pin length if provided
    pin_length = getattr(series_spec, "symbol_pin_length", 2.54)

    symbol_file.write(f'\t\t(symbol "{symbol_name}_0_0"\n')

    # Use custom pin configuration if available, otherwise use default
    if series_spec.pin_config:
        # Use custom pin configuration
        pin_config = convert_pin_config(series_spec.pin_config)

        # Write all pins from the configuration
        for pin in pin_config:
            symbol_utils.write_pin(
                symbol_file,
                pin["x_pos"],
                pin["y_pos"],
                pin["rotation"],
                pin["number"],
                series_spec.pin_names.get(pin["number"], "")
                if series_spec.pin_names
                else "",
                pin_type=pin["pin_type"],
                hide=pin.get("hide", False),
                length=pin["length"],
            )
    else:
        # For symmetrical layout, we'll divide pins equally on left and right
        if series_spec.pin_names:
            all_pin_ids = list(series_spec.pin_names.keys())
        else:
            all_pin_ids = [str(i) for i in range(1, pin_count + 1)]

        pins_per_side = pin_count // 2

        # Compute default X positions for pin anchors
        left_pin_x = -rect_half_width - pin_length
        right_pin_x = rect_half_width + pin_length

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
    write_segments(symbol_file)
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


def write_segments(
    symbol_file: TextIO,
) -> None:
    """Write a rectangle to the KiCad symbol file."""
    symbol_file.write("""
        (polyline
            (pts
                (xy -7.8994 -11.938) (xy -5.7404 -10.033) (xy -4.6482 -2.413)
                (xy -6.2992 -0.508) (xy -8.4582 -2.413) (xy -9.5504 -10.033)
                (xy -7.8994 -11.938)
            )
            (stroke
                (width 0)
                (type default)
            )
            (fill
                (type none)
            )
        )
        (polyline
            (pts
                (xy -7.4676 -12.446) (xy -5.2832 -10.541) (xy 2.3368 -10.541)
                (xy 3.9624 -12.446) (xy 1.8034 -14.351) (xy -5.8166 -14.351)
                (xy -7.4676 -12.446)
            )
            (stroke
                (width 0)
                (type default)
            )
            (fill
                (type none)
            )
        )
        (polyline
            (pts
                (xy -6.1468 0.508) (xy -3.9878 2.413) (xy -2.8956 10.033)
                (xy -4.5466 11.938) (xy -6.7056 10.033)
                (xy -7.7978 2.413) (xy -6.1468 0.508)
            )
            (stroke
                (width 0)
                (type default)
            )
            (fill
                (type none)
            )
        )
        (polyline
            (pts
                (xy -5.715 0) (xy -3.5306 1.905) (xy 4.0894 1.905)
                (xy 5.715 0) (xy 3.5306 -1.905) (xy -4.0894 -1.905)
                (xy -5.715 0)
            )
            (stroke
                (width 0)
                (type default)
            )
            (fill
                (type none)
            )
        )
        (polyline
            (pts
                (xy -3.9624 12.446) (xy -1.8034 14.351) (xy 5.8166 14.351)
                (xy 7.4676 12.446) (xy 5.2832 10.541) (xy -2.3368 10.541)
                (xy -3.9624 12.446)
            )
            (stroke
                (width 0)
                (type default)
            )
            (fill
                (type none)
            )
        )
        (polyline
            (pts
                (xy 4.5466 -11.938) (xy 6.7056 -10.033) (xy 7.7978 -2.413)
                (xy 6.1468 -0.508) (xy 3.9878 -2.413) (xy 2.8956 -10.033)
                (xy 4.5466 -11.938)
            )
            (stroke
                (width 0)
                (type default)
            )
            (fill
                (type none)
            )
        )
        (polyline
            (pts
                (xy 6.2992 0.508) (xy 8.4582 2.413) (xy 9.5504 10.033)
                (xy 7.8994 11.938) (xy 5.7404 10.033) (xy 4.6482 2.413)
                (xy 6.2992 0.508)
            )
            (stroke
                (width 0)
                (type default)
            )
            (fill
                (type none)
            )
        )
        (circle
            (center 8.128 -12.446)
            (radius 1.651)
            (stroke
                (width 0)
                (type default)
            )
            (fill
                (type none)
            )
        )
        (text "e"
            (at -7.0866 -6.223 0)
            (effects
                (font
                    (size 1.905 1.905)
                )
            )
        )
        (text "f"
            (at -5.3594 6.223 0)
            (effects
                (font
                    (size 1.905 1.905)
                )
            )
        )
        (text "d"
            (at -1.7526 -12.446 0)
            (effects
                (font
                    (size 1.905 1.905)
                )
            )
        )
        (text "g"
            (at 0 0 0)
            (effects
                (font
                    (size 1.905 1.905)
                )
            )
        )
        (text "a"
            (at 1.7526 12.446 0)
            (effects
                (font
                    (size 1.905 1.905)
                )
            )
        )
        (text "c"
            (at 5.3594 -6.223 0)
            (effects
                (font
                    (size 1.905 1.905)
                )
            )
        )
        (text "b"
            (at 7.0866 6.223 0)
            (effects
                (font
                    (size 1.905 1.905)
                )
            )
        )
        """)
