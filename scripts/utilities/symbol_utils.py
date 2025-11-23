"""Utilities for generating KiCad symbol files.

This module provides functions for creating KiCad symbol files, including
writing headers, properties, and drawing various electronic components like
capacitors, resistors, inductors, transformers, and transistors.
Key features:
- Write headers for symbol and symbol library files.
- Write properties for a single symbol.
- Write graphical representation of electronic components.
- Write pins for electronic components.

"""

from typing import List, TextIO, Tuple


def write_header(
    symbol_file: TextIO,
) -> None:
    """Write the header of the KiCad symbol file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.

    Returns:
        None

    """
    symbol_file.write("""
        (kicad_symbol_lib
            (version 20231120)
            (generator kicad_symbol_editor)
            (generator_version 8.0)
        """)


def write_symbol_header(
    symbol_file: TextIO,
    symbol_name: str,
) -> None:
    """Write the header for a single symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    Returns:
        None

    """
    symbol_file.write(f"""
        (symbol "{symbol_name}"
            (pin_names(offset 0.254))
            (exclude_from_sim no)
            (in_bom yes)
            (on_board yes)
        """)


def get_all_properties(
    component_data_list: list[dict[str, str]],
) -> list[str]:
    """Get all properties from the component data in a consistent order.

    Args:
        component_data_list (List[Dict[str, str]]): List of component data.

    Returns:
        list[str]:
            List of all unique property names with priority properties first,
            then remaining properties in alphabetical order.

    """
    all_properties = set()

    # Priority properties that should always come first
    priority_properties = [
        "Reference",
        "Value",
        "Footprint",
        "Datasheet",
    ]

    # Collect all unique properties
    for component in component_data_list:
        all_properties.update(component.keys())

    # Create final sorted list:
    # 1. Start with priority properties (if they exist in the data)
    result = [prop for prop in priority_properties if prop in all_properties]

    # 2. Add remaining properties in alphabetical order
    remaining_props = sorted(
        prop for prop in all_properties if prop not in priority_properties
    )
    result.extend(remaining_props)

    return result


def write_property(  # noqa: PLR0913
    symbol_file: TextIO,
    property_name: str,
    property_value: str,
    x_offset: float,
    y_offset: float,
    font_size: float,
    show_name: bool,  # noqa: FBT001
    hide: bool,  # noqa: FBT001
) -> None:
    """Write a single property for a symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        property_name (str): Name of the property.
        property_value (str): Value of the property.
        x_offset (float): Horizontal offset for property placement.
        y_offset (float): Vertical offset for property placement.
        font_size (float): Size of the font.
        show_name (bool): Whether to show the property name.
        hide (bool): Whether to hide the property.

    Returns:
        None

    """
    symbol_file.write(f"""
        (property "{property_name}" "{property_value}"
            (at {x_offset} {y_offset} 0)
            {("(show_name)" if show_name else "")}
            (effects
                (font(size {font_size} {font_size}))
                (justify left)
                {("(hide yes)" if hide else "")}
            )
        )
        """)


def write_properties(
    symbol_file: TextIO,
    component_data: dict[str, str],
    property_order: list[str],
    text_y_offset: int,
    text_x_offset: int = 0,
) -> None:
    """Write properties for a single symbol in the KiCad symbol file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        component_data (Dict[str, str]): Dictionary containing component data.
        property_order (List[str]):
            List of property names in the desired order.
        text_y_offset (int): Vertical offset for text placement.
        text_x_offset (int): Horizontal offset for text placement.

    Returns:
        None

    """
    property_configs = {
        "Reference": (
            text_x_offset,
            2.54 * text_y_offset,
            1.27,
            False,
            False,
            component_data.get("Reference", "-"),
        ),
        "Value": (
            text_x_offset,
            -2.54 * text_y_offset,
            1.27,
            False,
            False,
            component_data.get("Value", "-"),
        ),
        "Footprint": (
            text_x_offset,
            -2.54 * (text_y_offset + 1),
            1.27,
            True,
            True,
            None,
        ),
        "Datasheet": (
            text_x_offset,
            -2.54 * (text_y_offset + 2),
            1.27,
            True,
            True,
            None,
        ),
        "Description": (
            text_x_offset,
            -2.54 * (text_y_offset + 3),
            1.27,
            True,
            True,
            None,
        ),
    }

    y_offset = -2.54 * (text_y_offset + 4)
    for prop_name in property_order:
        if prop_name in component_data:
            config = property_configs.get(
                prop_name,
                (text_x_offset, y_offset, 1.27, True, True, None),
            )
            value = config[5] or component_data[prop_name]
            write_property(symbol_file, prop_name, value, *config[:5])
            if prop_name not in property_configs:
                y_offset -= 2.54


def write_pin(  # noqa: PLR0913
    symbol_file: TextIO,
    x_pos: float,
    y_pos: float,
    angle: int,
    number: str,
    name: str = "",
    pin_type: str = "unspecified",
    hide: bool = False,  # noqa: FBT001, FBT002
    length: float = 2.54,
) -> None:
    """Write a single pin for a symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        x_pos (float): X-coordinate of the pin.
        y_pos (float): Y-coordinate of the pin.
        angle (int): Angle of the pin.
        number (str): Number of the pin.
        name (str): Name of the pin.
        pin_type (str): Type of the pin.
        hide (bool): Whether to hide the pin.
        length (float): Length of the pin.

    Returns:
        None

    """
    symbol_file.write(f"""
        (pin {pin_type} line
            (at {x_pos} {y_pos} {angle})
            (length {length})
            (name "{name}"(effects(font(size 1.27 1.27))))
            (number "{number}"(effects(font(size 1.27 1.27))))
            {("hide" if hide else "")}
        )
        """)


def write_capacitor_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
) -> None:
    """Write the graphical representation of a symbol in the KiCad symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    Returns:
        None

    """
    symbol_file.write(f"""
        (symbol "{symbol_name}_0_1"
            (polyline
                (pts (xy -0.762 -2.032) (xy -0.762 2.032))
                (stroke (width 0.508) (type default))
                (fill (type none))
            )
            (polyline
                (pts (xy 0.762 -2.032) (xy 0.762 2.032))
                (stroke (width 0.508) (type default))
                (fill (type none))
            )
        )
    """)

    # Write pins
    write_pin(symbol_file, -3.81, 0, 0, "1", length=2.8, pin_type="passive")
    write_pin(symbol_file, 3.81, 0, 180, "2", length=2.8, pin_type="passive")


def write_polarised_capacitor_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
) -> None:
    """Write the graphical representation of a symbol in the KiCad symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    Returns:
        None

    """
    symbol_file.write(f"""
        (symbol "{symbol_name}_0_1"
            (polyline
                (pts (xy -0.762 -2.032) (xy -0.762 2.032))
                (stroke (width 0.508) (type default))
                (fill (type none))
            )
			(polyline
				(pts (xy -2.54 -1.016) (xy -2.54 -2.032))
				(stroke (width 0.508) (type default))
				(fill (type none))
			)
			(polyline
				(pts (xy -2.032 -1.524) (xy -3.048 -1.524))
				(stroke (width 0.508) (type default))
				(fill (type none))
			)
			(arc
				(start 1.524 2.032)
				(mid 0.9088 0)
				(end 1.524 -2.032)
				(stroke (width 0.508) (type default))
				(fill (type none))
			)
        )
    """)

    # Write pins
    write_pin(symbol_file, -3.81, 0, 0, "1", length=2.8, pin_type="passive")
    write_pin(symbol_file, 3.81, 0, 180, "2", length=2.8, pin_type="passive")


def write_resistor_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
) -> None:
    """Write the graphical representation of a symbol in the KiCad file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    Returns:
        None

    """
    symbol_file.write(f"""
        (symbol "{symbol_name}_0_1"
            (polyline
                (pts (xy 2.286 0) (xy 2.54 0))
                (stroke (width 0) (type default))
                (fill (type none))
            )
            (polyline
                (pts (xy -2.286 0) (xy -2.54 0))
                (stroke (width 0) (type default))
                (fill (type none))
            )
            (polyline
                (pts
                    (xy 0.762 0) (xy 1.143 1.016) (xy 1.524 0)
                    (xy 1.905 -1.016) (xy 2.286 0)
                )
                (stroke (width 0) (type default))
                (fill (type none))
            )
            (polyline
                (pts
                    (xy -0.762 0) (xy -0.381 1.016) (xy 0 0)
                    (xy 0.381 -1.016) (xy 0.762 0)
                )
                (stroke (width 0) (type default))
                (fill (type none))
            )
            (polyline
                (pts
                    (xy -2.286 0) (xy -1.905 1.016) (xy -1.524 0)
                    (xy -1.143 -1.016) (xy -0.762 0)
                )
                (stroke (width 0) (type default))
                (fill (type none))
            )
        )
        """)

    # Write pins
    write_pin(symbol_file, -5.08, 0, 0, "1", pin_type="passive")
    write_pin(symbol_file, 5.08, 0, 180, "2", pin_type="passive")


def write_thermistor_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
) -> None:
    """Write the graphical representation of a symbol in the KiCad file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    Returns:
        None

    """
    symbol_file.write(f"""
        (symbol "{symbol_name}_0_1"
			(polyline
				(pts
					(xy -2.286 0) (xy -2.54 0)
				)
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(polyline
				(pts
					(xy 2.286 0) (xy 2.54 0)
				)
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(polyline
				(pts
					(xy 2.54 1.778) (xy 1.524 1.778)
                    (xy -1.524 -1.778) (xy -2.54 -1.778)
				)
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(polyline
				(pts
					(xy -2.286 0) (xy -1.905 1.016) (xy -1.524 0)
                    (xy -1.143 -1.016) (xy -0.762 0)
				)
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(polyline
				(pts
					(xy -0.762 0) (xy -0.381 1.016) (xy 0 0)
                    (xy 0.381 -1.016) (xy 0.762 0)
				)
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(polyline
				(pts
					(xy 0.762 0) (xy 1.143 1.016) (xy 1.524 0)
                    (xy 1.905 -1.016) (xy 2.286 0)
				)
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(polyline
				(pts
					(xy -3.302 2.54) (xy -1.016 2.54) (xy -1.778 2.794)
                    (xy -1.778 2.286) (xy -1.016 2.54) (xy -1.27 2.54)
				)
				(stroke (width 0) (type default))
				(fill (type outline))
			)
			(polyline
				(pts
					(xy -1.016 1.778) (xy -3.302 1.778) (xy -2.54 2.032)
                    (xy -2.54 1.524) (xy -3.302 1.778) (xy -3.048 1.778)
				)
				(stroke (width 0) (type default))
				(fill (type outline))
			)
        )
        """)

    # Write pins
    write_pin(symbol_file, -5.08, 0, 0, "1", pin_type="passive")
    write_pin(symbol_file, 5.08, 0, 180, "2", pin_type="passive")


def write_inductor_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
    pin_config: dict = None,
) -> None:
    """Write the horizontal graphical representation of an inductor symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
        pin_config (dict, optional): Dictionary defining pin configuration.

    Returns:
        None

    """

    def write_arc(
        symbol_file: TextIO,
        start_x: float,
        mid_x: float,
        end_x: float,
    ) -> None:
        """Write an arc to the symbol file.

        Args:
            symbol_file (TextIO): File object for writing the symbol file.
            start_x (float): X-coordinate of the start of the arc.
            mid_x (float): X-coordinate of the middle of the arc.
            end_x (float): X-coordinate of the end of the arc.

        Returns:
            None

        """
        symbol_file.write(f"""
            (arc
                (start {start_x} 0.0056)
                (mid {mid_x} 1.27)
                (end {end_x} 0.0056)
                (stroke (width 0.2032) (type default))
                (fill (type none))
            )
            """)

    # Write symbol drawing section
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_1"\n')

    # Write arcs
    arc_params = [
        (-2.54, -3.81, -5.08),
        (0, -1.27, -2.54),
        (2.54, 1.27, 0),
        (5.08, 3.81, 2.54),
    ]
    for start_x, mid_x, end_x in arc_params:
        write_arc(symbol_file, start_x, mid_x, end_x)

    # Write standard pins
    write_pin(symbol_file, -7.62, 0, 0, "1", pin_type="passive")
    write_pin(symbol_file, 7.62, 0, 180, "2", pin_type="passive")

    # Write additional pins if they exist
    if pin_config and "additional_pins" in pin_config:
        for pin in pin_config["additional_pins"]:
            write_pin(
                symbol_file=symbol_file,
                x_pos=pin["x_pos"],
                y_pos=pin["y_pos"],
                angle=0,
                number=pin["number"],
                name="",
                pin_type=pin["pin_type"],
                hide=pin.get("hide", False),
                length=pin["length"],
            )

    symbol_file.write("\t\t)\n")


def write_ferrite_bead_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
) -> None:
    """Write the horizontal graphical representation of an inductor symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    Returns:
        None

    """
    symbol_file.write(f"""
        (symbol "{symbol_name}_0_1"
            (polyline
				(pts (xy -1.27 0) (xy -2.54 0))
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(polyline
				(pts (xy 1.27 0) (xy 2.54 0))
				(stroke (width 0) (type default))
				(fill (type none))
			)
            (polyline
				(pts
					(xy 0 2.54) (xy 2.54 2.54) (xy 0 -2.54)
                    (xy -2.54 -2.54) (xy 0 2.54)
				)
				(stroke (width 0.2032) (type default))
				(fill (type none))
			)
        )
        """)
    # Write pins
    write_pin(symbol_file, -5.08, 0, 0, "1", pin_type="passive")
    write_pin(symbol_file, 5.08, 0, 180, "2", pin_type="passive")

    symbol_file.write("\t\t)\n")


def get_symbol_bounds(pin_config: dict) -> tuple:
    """Get the minimum and maximum y-coordinates of the symbol.

    Args:
        pin_config (dict): Dictionary defining pin configuration.

    Returns:
        tuple: Minimum and maximum y-coordinates of the symbol.

    """
    y_positions = [pin["y_pos"] for pin in pin_config["left"]] + [
        pin["y_pos"] for pin in pin_config["right"]
    ]
    max_y = max(y_positions)
    min_y = min(y_positions)
    return min_y, max_y


def write_arcs(
    symbol_file: TextIO,
    start_x: float,
    offset: list[float],
    num_arcs: int = 4,
) -> None:
    """Write a set of inductor arcs for transformer symbol.

    Args:
        symbol_file: File to write to
        start_x: X coordinate to start arcs from
        offset: [x_offset, y_offset] for positioning the arcs
        num_arcs: Number of arcs to draw (default 4)

    Returns:
        None

    """
    x_offset, y_offset = offset
    for y_start in range(num_arcs):
        y_pos = y_start * 2.54
        symbol_file.write(f"""
            (arc
                (start {start_x + x_offset} {y_offset + y_pos})
                (mid
                    {start_x + x_offset + (-1.27 if start_x > 0 else 1.27)}
                    {y_offset + y_pos + 1.27})
                (end {start_x + x_offset} {y_offset + y_pos + 2.54})
                (stroke (width 0) (type default))
                (fill (type none))
            )
            """)


def write_transformer_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
    pin_config: dict,
) -> None:
    """Write the horizontal graphical representation of a transformer symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
        pin_config (dict, optional): Dictionary defining pin configuration.

    Returns:
        None

    """
    # Calculate symbol bounds
    min_y, max_y = get_symbol_bounds(pin_config)

    # Write symbol drawing section - split into two units
    symbol_file.write(f'        (symbol "{symbol_name}_0_1"\n')

    # Write left and right inductor arcs
    write_arcs(symbol_file, -2.54, [0.0, -5.08])
    write_arcs(symbol_file, 2.54, [0.0, -5.08])

    # Write polarity dots
    for x, y in [(-2.54, 3.81), (2.54, -3.81)]:
        symbol_file.write(f"""
            (circle
                (center {x} {y})
                (radius 0.508)
                (stroke (width 0) (type default))
                (fill (type none))
            )
            """)

    # Write coupling lines
    for x in [-0.254, 0.254]:
        symbol_file.write(f"""
            (polyline
                (pts (xy {x} {max_y}) (xy {x} {min_y}))
                (stroke (width 0) (type default))
                (fill (type none))
            )
            """)

    # Write left side pins
    for pin in pin_config["left"]:
        write_pin(
            symbol_file=symbol_file,
            x_pos=-7.62,
            y_pos=pin["y_pos"],
            angle=0,
            number=pin["number"],
            pin_type=pin["pin_type"],
            hide=pin.get("hide", False),
            length=pin["lenght"],
        )

    # Write right side pins
    for pin in pin_config["right"]:
        write_pin(
            symbol_file=symbol_file,
            x_pos=7.62,
            y_pos=pin["y_pos"],
            angle=180,
            number=pin["number"],
            pin_type=pin["pin_type"],
            hide=pin.get("hide", False),
            length=pin["lenght"],
        )

    symbol_file.write("        )\n")


def write_transformer_symbol_drawing_v2(
    symbol_file: TextIO,
    symbol_name: str,
    pin_config: dict,
) -> None:
    """Write the horizontal graphical representation of a transformer symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
        pin_config (dict, optional): Dictionary defining pin configuration.

    Returns:
        None

    """
    for symbol_number in range(1, 3):
        # Write symbol drawing section
        symbol_file.write(
            f'        (symbol "{symbol_name}_1_{symbol_number}"\n',
        )

        # Write left inductor arcs
        write_arcs(symbol_file, -2.54, [0.0, -10.16], num_arcs=8)

        # Write right inductor arcs
        write_arcs(symbol_file, 2.54, [0.0, -5.08])

        secondary_dot_y = -1 if symbol_number == 1 else 1

        # Write polarity dots
        for x, y in [
            (-2.54, 8.89),
            (-2.54, -1.27),
            (2.54, secondary_dot_y * 3.81),
        ]:
            symbol_file.write(f"""
                (circle
                    (center {x} {y})
                    (radius 0.508)
                    (stroke (width 0) (type default))
                    (fill (type none))
                )
                """)

        # Write coupling lines
        for x in [-0.254, 0.254]:
            symbol_file.write(f"""
                (polyline
                    (pts (xy {x} -10.16) (xy {x} 10.16))
                    (stroke (width 0) (type default))
                    (fill (type none))
                )
                """)

        # Write left side pins
        for pin in pin_config["left"]:
            write_pin(
                symbol_file=symbol_file,
                x_pos=-7.62,
                y_pos=pin["y_pos"],
                angle=0,
                number=pin["number"],
                pin_type=pin["pin_type"],
                hide=pin.get("hide", False),
                length=pin["lenght"],
            )

        # Write right side pins
        for pin in (
            pin_config["right"]
            if symbol_number == 1
            else pin_config["right_alternative"]
        ):
            write_pin(
                symbol_file=symbol_file,
                x_pos=7.62,
                y_pos=pin["y_pos"],
                angle=180,
                number=pin["number"],
                pin_type=pin["pin_type"],
                hide=pin.get("hide", False),
                length=pin["lenght"],
            )

        symbol_file.write("        )\n")


def write_transformer_symbol_drawing_v3(
    symbol_file: TextIO,
    symbol_name: str,
    pin_config: dict,
) -> None:
    """Write the horizontal graphical representation of a transformer symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
        pin_config (dict, optional): Dictionary defining pin configuration.

    Returns:
        None

    """
    # Calculate symbol bounds
    min_y, max_y = get_symbol_bounds(pin_config)

    # Write symbol drawing section - split into two units
    symbol_file.write(f'        (symbol "{symbol_name}_0_1"\n')

    # Write left inductor arcs
    write_arcs(symbol_file, -2.54, [0.0, -5.08])

    # Write first right inductor arcs
    write_arcs(symbol_file, 2.54, [0.0, -5.08])

    # Write second right inductor arcs
    write_arcs(symbol_file, 5.08, [0.0, -5.08])

    for symbol in ["-", ""]:
        symbol_file.write(f"""
            (polyline
                (pts
                    (xy 2.54 {symbol}5.08)
                    (xy 2.54 {symbol}7.62)
                    (xy 5.08 {symbol}7.62)
                )
                (stroke (width 0) (type default))
                (fill (type none))
            )
        """)

    # Write polarity dots
    for x, y in [(-2.54, -3.81), (2.54, 3.81), (5.08, 3.81)]:
        symbol_file.write(f"""
            (circle
                (center {x} {y})
                (radius 0.508)
                (stroke (width 0) (type default))
                (fill (type none))
            )
            """)

    # Write coupling lines
    for x in [-0.254, 0.254]:
        symbol_file.write(f"""
            (polyline
                (pts (xy {x} {max_y}) (xy {x} {min_y}))
                (stroke (width 0) (type default))
                (fill (type none))
            )
            """)

    # Write left side pins
    for pin in pin_config["left"]:
        write_pin(
            symbol_file=symbol_file,
            x_pos=-7.62,
            y_pos=pin["y_pos"],
            angle=0,
            number=pin["number"],
            pin_type=pin["pin_type"],
            hide=pin.get("hide", False),
            length=pin["lenght"],
        )

    # Write right side pins
    for pin in pin_config["right"]:
        write_pin(
            symbol_file=symbol_file,
            x_pos=7.62,
            y_pos=pin["y_pos"],
            angle=180,
            number=pin["number"],
            pin_type=pin["pin_type"],
            hide=pin.get("hide", False),
            length=pin["lenght"],
        )

    symbol_file.write("        )\n")


def write_transformer_symbol_drawing_v4(
    symbol_file: TextIO,
    symbol_name: str,
    pin_config: dict,
) -> None:
    """Write the horizontal graphical representation of a transformer symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
        pin_config (dict, optional): Dictionary defining pin configuration.

    Returns:
        None

    """
    # Calculate symbol bounds
    min_y, max_y = get_symbol_bounds(pin_config)

    # Write symbol drawing section - split into two units
    symbol_file.write(f'        (symbol "{symbol_name}_0_1"\n')

    # Write left inductor arcs
    write_arcs(symbol_file, -2.54, [0.0, -5.08])

    # Write top right inductor arcs
    write_arcs(symbol_file, 2.54, [0.0, 2.54])

    # Write bottom right inductor arcs
    write_arcs(symbol_file, 2.54, [0.0, -12.7])

    # Write polarity dots
    for x, y in [(-2.54, -3.81), (2.54, -3.81), (2.54, 11.43)]:
        symbol_file.write(f"""
            (circle
                (center {x} {y})
                (radius 0.508)
                (stroke (width 0) (type default))
                (fill (type none))
            )
            """)

    # Write coupling lines
    for x in [-0.254, 0.254]:
        symbol_file.write(f"""
            (polyline
                (pts (xy {x} {max_y}) (xy {x} {min_y}))
                (stroke (width 0) (type default))
                (fill (type none))
            )
            """)

    # Write left side pins
    for pin in pin_config["left"]:
        write_pin(
            symbol_file=symbol_file,
            x_pos=-7.62,
            y_pos=pin["y_pos"],
            angle=0,
            number=pin["number"],
            pin_type=pin["pin_type"],
            hide=pin.get("hide", False),
            length=pin["lenght"],
        )

    # Write right side pins
    for pin in pin_config["right"]:
        write_pin(
            symbol_file=symbol_file,
            x_pos=7.62,
            y_pos=pin["y_pos"],
            angle=180,
            number=pin["number"],
            pin_type=pin["pin_type"],
            hide=pin.get("hide", False),
            length=pin["lenght"],
        )

    symbol_file.write("        )\n")


def write_transformer_symbol_drawing_v5(
    symbol_file: TextIO,
    symbol_name: str,
    pin_config: dict,
) -> None:
    """Write the horizontal graphical representation of a transformer symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
        pin_config (dict, optional): Dictionary defining pin configuration.

    Returns:
        None

    """
    # Calculate symbol bounds
    min_y, max_y = get_symbol_bounds(pin_config)

    # Write symbol drawing section - split into two units
    symbol_file.write(f'        (symbol "{symbol_name}_0_1"\n')

    # Write left inductor arcs
    write_arcs(symbol_file, -2.54, [0.0, 2.54 * 3])
    write_arcs(symbol_file, -2.54, [0.0, -2.54 * 2])
    write_arcs(symbol_file, -2.54, [0.0, -2.54 * 7])

    # Write right inductor arcs
    write_arcs(symbol_file, 2.54, [0.0, 10.16])
    write_arcs(symbol_file, 2.54, [0.0, 0.0])
    write_arcs(symbol_file, 2.54, [0.0, -10.16])
    write_arcs(symbol_file, 2.54, [0.0, -20.32])

    # Write bottom right inductor arcs
    # write_arcs(symbol_file, 2.54, [0.0, -5.08])

    # write_arcs(symbol_file, 2.54, [0.0, -12.7])

    # Write polarity dots
    for x, y in [
        (-2.54, 1.27 * 13),
        (-2.54, 1.27 * 3),
        (-2.54, -1.27 * 7),
        (2.54, 1.27 * 15),
        (2.54, 1.27 * 7),
        (2.54, -1.27 * 1),
        (2.54, -1.27 * 9),
    ]:
        symbol_file.write(f"""
            (circle
                (center {x} {y})
                (radius 0.508)
                (stroke (width 0) (type default))
                (fill (type none))
            )
            """)

    # Write coupling lines
    for x in [-0.254, 0.254]:
        symbol_file.write(f"""
            (polyline
                (pts (xy {x} {max_y}) (xy {x} {min_y}))
                (stroke (width 0) (type default))
                (fill (type none))
            )
            """)

    # Write left side pins
    for pin in pin_config["left"]:
        write_pin(
            symbol_file=symbol_file,
            x_pos=-7.62,
            y_pos=pin["y_pos"],
            angle=0,
            number=pin["number"],
            pin_type=pin["pin_type"],
            hide=pin.get("hide", False),
            length=pin["lenght"],
        )

    # Write right side pins
    for pin in pin_config["right"]:
        write_pin(
            symbol_file=symbol_file,
            x_pos=7.62,
            y_pos=pin["y_pos"],
            angle=180,
            number=pin["number"],
            pin_type=pin["pin_type"],
            hide=pin.get("hide", False),
            length=pin["lenght"],
        )

    symbol_file.write("        )\n")


def write_coupled_inductor_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
    pin_config: dict,
) -> None:
    """Write the horizontal graphical representation of an inductor symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
        pin_config (dict): Pin config.

    Returns:
        None

    """
    for symbol_number in range(1, 3):
        # Write symbol drawing section
        symbol_file.write(
            f'        (symbol "{symbol_name}_1_{symbol_number}"\n',
        )

        # Write left inductor arcs
        write_arcs(symbol_file, -2.54, [0.0, -5.08])

        # Write right inductor arcs
        write_arcs(symbol_file, 2.54, [0.0, -5.08])

        secondary_dot_y = -1 if symbol_number == 1 else 1
        # Write polarity dots
        for x, y in [(-2.54, 3.81), (2.54, secondary_dot_y * 3.81)]:
            symbol_file.write(f"""
                (circle
                    (center {x} {y})
                    (radius 0.508)
                    (stroke (width 0) (type default))
                    (fill (type none))
                )""")

        # Write coupling lines
        for x in [-0.254, 0.254]:
            symbol_file.write(f"""
                (polyline
                    (pts (xy {x} 5.08) (xy {x} -5.08))
                    (stroke (width 0) (type default))
                    (fill (type none))
                )""")

        # Write left side pins
        for pin in pin_config["left"]:
            write_pin(
                symbol_file=symbol_file,
                x_pos=-7.62,
                y_pos=pin["y_pos"],
                angle=0,
                number=pin["number"],
                pin_type=pin["pin_type"],
                hide=pin.get("hide", False),
                length=pin["lenght"],
            )

        # Write right side pins
        for pin in (
            pin_config["right"]
            if symbol_number == 1
            else pin_config["right_alternative"]
        ):
            write_pin(
                symbol_file=symbol_file,
                x_pos=7.62,
                y_pos=pin["y_pos"],
                angle=180,
                number=pin["number"],
                pin_type=pin["pin_type"],
                hide=pin.get("hide", False),
                length=pin["lenght"],
            )

        symbol_file.write("        )\n")


def write_schottky_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
) -> None:
    """Write the horizontal graphical representation of a diode symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    Returns:
        None

    """
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')

    symbol_file.write("""
        (polyline
            (pts
                (xy 0.635 1.27) (xy 0.635 1.905) (xy 1.27 1.905) (xy 1.27 0)
                (xy -1.27 1.905) (xy -1.27 -1.905) (xy 1.27 0)
                (xy 1.27 -1.905) (xy 1.905 -1.905) (xy 1.905 -1.27)
            )
            (stroke (width 0.2032) (type default))
            (fill (type none))
        )
        """)

    # Write pins
    write_pin(symbol_file, 5.08, 0, 180, "1", length=3.81, pin_type="passive")
    write_pin(symbol_file, -5.08, 0, 0, "2", length=3.81, pin_type="passive")

    symbol_file.write("\t\t)\n")


def write_zener_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
) -> None:
    """Write the horizontal graphical representation of a diode symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    Returns:
        None

    """
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')

    symbol_file.write("""
        (polyline
            (pts
                (xy 0.635 1.905) (xy 1.27 1.27) (xy 1.27 0)
                (xy -1.27 1.905) (xy -1.27 -1.905) (xy 1.27 0)
                (xy 1.27 -1.27) (xy 1.905 -1.905)
            )
            (stroke (width 0.2032) (type default))
            (fill (type none))
        )
        """)

    # Write pins
    write_pin(symbol_file, 5.08, 0, 180, "1", length=3.81, pin_type="passive")
    write_pin(symbol_file, -5.08, 0, 0, "2", length=3.81, pin_type="passive")

    symbol_file.write("\t\t)\n")


def write_rectifier_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
) -> None:
    """Write the horizontal graphical representation of a diode symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    Returns:
        None

    """
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')

    symbol_file.write("""
        (polyline
            (pts
                (xy 1.27 1.905) (xy 1.27 0) (xy -1.27 1.905)
                (xy -1.27 -1.905) (xy 1.27 0) (xy 1.27 -1.905)
            )
            (stroke (width 0.2032) (type default))
            (fill (type none))
        )
        """)

    # Write pins
    write_pin(symbol_file, 5.08, 0, 180, "1", length=3.81, pin_type="passive")
    write_pin(symbol_file, -5.08, 0, 0, "2", length=3.81, pin_type="passive")

    symbol_file.write("\t\t)\n")


def write_unidirectional_tvs_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
) -> None:
    """Write the horizontal graphical representation of a diode symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    Returns:
        None

    """
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')

    symbol_file.write("""
        (polyline
            (pts
                (xy 1.27 1.905) (xy 1.27 0) (xy -1.27 1.905)
                (xy -1.27 -1.905) (xy 1.27 0) (xy 1.27 -1.905)
                (xy 0.635 -1.905)
            )
            (stroke (width 0.2032) (type default))
            (fill (type none))
        )
        """)

    # Write pins
    write_pin(symbol_file, 5.08, 0, 180, "1", length=3.81, pin_type="passive")
    write_pin(symbol_file, -5.08, 0, 0, "2", length=3.81, pin_type="passive")

    symbol_file.write("\t\t)\n")


def write_unidirectional_tvs_symbol_drawing_v2(
    symbol_file: TextIO,
    symbol_name: str,
) -> None:
    """Write the horizontal graphical representation of a diode symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    Returns:
        None

    """
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')

    symbol_file.write("""
        (polyline
            (pts
                (xy 6.35 0) (xy 6.35 -3.81) (xy 1.27 -3.81) (xy 1.27 -5.715)
                (xy 1.27 -3.81) (xy -1.27 -5.715) (xy -1.27 -3.81)
                (xy -6.35 -3.81) (xy -6.35 0) (xy -6.35 0) (xy -6.35 -3.81)
                (xy -1.27 -3.81) (xy -1.27 -1.905) (xy 1.27 -3.81)
                (xy 1.27 -1.905) (xy 1.27 -3.81) (xy 6.35 -3.81)
            )
            (stroke
                (width 0.2032)
                (type default)
            )
            (fill
                (type none)
            )
        )
        (polyline
            (pts
                (xy -6.35 0) (xy -6.35 3.81) (xy -3.81 3.81) (xy -3.81 5.715)
                (xy -3.81 3.81) (xy -1.27 5.715) (xy -1.27 3.81)
                (xy 1.27 3.81) (xy 1.27 5.715) (xy 3.81 3.81) (xy 3.81 5.08)
                (xy 3.175 5.715) (xy 3.81 5.08) (xy 3.81 3.81) (xy 6.35 3.81)
                (xy 6.35 0) (xy 6.35 0) (xy 6.35 3.81) (xy 3.81 3.81)
                (xy 3.81 2.54) (xy 4.445 1.905) (xy 3.81 2.54) (xy 3.81 3.81)
                (xy 1.27 1.905) (xy 1.27 3.81) (xy -1.27 3.81)
                (xy -1.27 1.905) (xy -3.81 3.81) (xy -3.81 1.905)
                (xy -3.81 3.81) (xy -6.35 3.81)
            )
            (stroke
                (width 0.2032)
                (type default)
            )
            (fill
                (type none)
            )
        )
        (circle
            (center -6.35 0)
            (radius 0.284)
            (stroke (width 0) (type default))
            (fill (type outline))
        )
        (circle
            (center 6.35 0)
            (radius 0.284)
            (stroke (width 0) (type default))
            (fill (type outline))
        )
        """)

    # Write pins
    write_pin(
        symbol_file, 10.16, 0, 180, "1", length=3.81, pin_type="passive"
    )
    write_pin(symbol_file, -10.16, 0, 0, "2", length=3.81, pin_type="passive")

    symbol_file.write("\t\t)\n")


def write_bidirectional_tvs_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
) -> None:
    """Write the horizontal graphical representation of a diode symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    Returns:
        None

    """
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')

    symbol_file.write("""
        (polyline
            (pts
                (xy 3.81 0) (xy 2.54 0) (xy 2.54 1.905) (xy 0 0) (xy 0 1.27)
                (xy -0.635 1.905) (xy 0 1.27) (xy 0 0) (xy -2.54 1.905)
                (xy -2.54 0) (xy -3.81 0) (xy -2.54 0) (xy -2.54 -1.905)
                (xy 0 0) (xy 0 -1.27) (xy 0.635 -1.905) (xy 0 -1.27) (xy 0 0)
                (xy 2.54 -1.905) (xy 2.54 0)
            )
            (stroke (width 0.2032) (type default))
            (fill (type none))
        )
        """)

    # Write pins
    write_pin(symbol_file, 5.08, 0, 180, "1", length=1.27, pin_type="passive")
    write_pin(symbol_file, -5.08, 0, 0, "2", length=1.27, pin_type="passive")

    symbol_file.write("\t\t)\n")


def write_bidirectional_tvs_symbol_drawing_v2(
    symbol_file: TextIO,
    symbol_name: str,
) -> None:
    """Write the horizontal graphical representation of a diode symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    Returns:
        None

    """
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')

    symbol_file.write("""
        (polyline
            (pts
                (xy -6.35 0) (xy -6.35 -3.81) (xy -3.81 -3.81)
                (xy -3.81 -5.715) (xy -3.81 -3.81) (xy -1.27 -5.715)
                (xy -1.27 -3.81) (xy 1.27 -3.81) (xy 1.27 -5.715)
                (xy 3.81 -3.81) (xy 3.81 -5.08) (xy 3.175 -5.715)
                (xy 3.81 -5.08) (xy 3.81 -3.81) (xy 6.35 -3.81) (xy 6.35 0)
                (xy 6.35 0) (xy 6.35 -3.81) (xy 3.81 -3.81) (xy 3.81 -2.54)
                (xy 4.445 -1.905) (xy 3.81 -2.54) (xy 3.81 -3.81)
                (xy 1.27 -1.905) (xy 1.27 -3.81) (xy -1.27 -3.81)
                (xy -1.27 -1.905) (xy -3.81 -3.81) (xy -3.81 -1.905)
                (xy -3.81 -3.81) (xy -6.35 -3.81)
            )
            (stroke
                (width 0.2032)
                (type default)
            )
            (fill
                (type none)
            )
        )
        (polyline
            (pts
                (xy 6.35 0) (xy 6.35 3.81) (xy 3.81 3.81) (xy 3.81 5.715)
                (xy 3.81 3.81) (xy 1.27 5.715) (xy 1.27 3.81) (xy -1.27 3.81)
                (xy -1.27 5.715) (xy -3.81 3.81) (xy -3.81 5.08)
                (xy -3.175 5.715) (xy -3.81 5.08) (xy -3.81 3.81)
                (xy -6.35 3.81) (xy -6.35 0) (xy -6.35 0) (xy -6.35 3.81)
                (xy -3.81 3.81) (xy -3.81 2.54) (xy -4.445 1.905)
                (xy -3.81 2.54) (xy -3.81 3.81) (xy -1.27 1.905)
                (xy -1.27 3.81) (xy 1.27 3.81) (xy 1.27 1.905) (xy 3.81 3.81)
                (xy 3.81 1.905) (xy 3.81 3.81) (xy 6.35 3.81)
            )
            (stroke
                (width 0.2032)
                (type default)
            )
            (fill
                (type none)
            )
        )
        (circle
            (center -6.35 0)
            (radius 0.284)
            (stroke (width 0) (type default))
            (fill (type outline))
        )
        (circle
            (center 6.35 0)
            (radius 0.284)
            (stroke (width 0) (type default))
            (fill (type outline))
        )
        """)

    # Write pins
    write_pin(
        symbol_file, 10.16, 0, 180, "1", length=3.81, pin_type="passive"
    )
    write_pin(symbol_file, -10.16, 0, 0, "2", length=3.81, pin_type="passive")

    symbol_file.write("\t\t)\n")


def write_dual_small_signal_diodes_symbol_drawing_v1(
    symbol_file: TextIO,
    symbol_name: str,
) -> None:
    """Write the horizontal graphical representation of a diode symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    Returns:
        None

    """
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')

    symbol_file.write("""
        (polyline
            (pts
                (xy 6.35 1.905) (xy 6.35 0) (xy 3.81 1.905) (xy 3.81 0)
                (xy 0 0) (xy 0 1.27) (xy 0 0) (xy -3.81 0) (xy -3.81 1.905)
                (xy -3.81 0) (xy -6.35 1.905) (xy -6.35 -1.905) (xy -3.81 0)
                (xy -3.81 -1.905) (xy -3.81 0) (xy 3.81 0) (xy 3.81 -1.905)
                (xy 6.35 0) (xy 6.35 -1.905)
            )
            (stroke (width 0.2032) (type default))
            (fill (type none))
        )
        (circle
            (center 0 0)
            (radius 0.254)
            (stroke (width 0) (type default))
            (fill (type outline))
        )
        """)

    # Write pins
    write_pin(symbol_file, -10.16, 0, 0, "1", length=3.81, pin_type="passive")
    write_pin(
        symbol_file, 10.16, 0, 180, "2", length=3.81, pin_type="passive"
    )
    write_pin(symbol_file, 0, 5.08, 270, "3", length=3.81, pin_type="passive")

    symbol_file.write("\t\t)\n")


def write_small_signal_schottky_diodes_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
) -> None:
    """Write the horizontal graphical representation of a diode symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    Returns:
        None

    """
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')

    symbol_file.write("""
        (polyline
            (pts
                (xy 6.35 1.905) (xy 6.35 0) (xy 3.81 1.905) (xy 3.81 0)
                (xy 0 0) (xy 0 1.27) (xy 0 0) (xy -3.81 0) (xy -3.81 1.905)
                (xy -6.35 0) (xy -6.35 1.905) (xy -6.35 -1.905) (xy -6.35 0)
                (xy -3.81 -1.905) (xy -3.81 0) (xy 3.81 0) (xy 3.81 -1.905)
                (xy 6.35 0) (xy 6.35 -1.905)
            )
            (stroke (width 0.2032) (type default))
            (fill (type none))
        )
        (circle
            (center 0 0)
            (radius 0.254)
            (stroke (width 0) (type default))
            (fill (type outline))
        )
        """)

    # Write pins
    write_pin(symbol_file, -10.16, 0, 0, "1", length=3.81, pin_type="passive")
    write_pin(
        symbol_file, 10.16, 0, 180, "2", length=3.81, pin_type="passive"
    )
    write_pin(symbol_file, 0, 5.08, 270, "3", length=3.81, pin_type="passive")

    symbol_file.write("\t\t)\n")


def write_red_led_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
) -> None:
    """Write the horizontal graphical representation of a diode symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    Returns:
        None

    """
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')

    symbol_file.write("""
        (polyline
				(pts
					(xy 1.27 1.905) (xy 1.27 0) (xy -1.27 1.905)
                    (xy -1.27 -1.905) (xy 1.27 0) (xy 1.27 -1.905)
				)
				(stroke (width 0.2032) (type default))
				(fill (type color) (color 255 0 0 1))
			)
        (polyline
            (pts
                (xy 1.778 2.54) (xy 3.302 4.064) (xy 2.54 4.064)
                (xy 3.302 4.064) (xy 3.302 3.302)
            )
            (stroke (width 0.2032) (type default))
            (fill (type none))
        )
        (polyline
            (pts
                (xy 3.048 2.54) (xy 4.572 4.064) (xy 3.81 4.064)
                (xy 4.572 4.064) (xy 4.572 3.302)
            )
            (stroke (width 0.2032) (type default))
            (fill (type none))
        )
        """)

    # Write pins
    write_pin(symbol_file, 5.08, 0, 180, "1", length=3.81, pin_type="passive")
    write_pin(symbol_file, -5.08, 0, 0, "2", length=3.81, pin_type="passive")

    symbol_file.write("\t\t)\n")


def write_green_led_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
) -> None:
    """Write the horizontal graphical representation of a diode symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    Returns:
        None

    """
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')

    symbol_file.write("""
        (polyline
				(pts
					(xy 1.27 1.905) (xy 1.27 0) (xy -1.27 1.905)
                    (xy -1.27 -1.905) (xy 1.27 0) (xy 1.27 -1.905)
				)
				(stroke (width 0.2032) (type default))
				(fill (type color) (color 204 255 0 1))
			)
        (polyline
            (pts
                (xy 1.778 2.54) (xy 3.302 4.064) (xy 2.54 4.064)
                (xy 3.302 4.064) (xy 3.302 3.302)
            )
            (stroke (width 0.2032) (type default))
            (fill (type none))
        )
        (polyline
            (pts
                (xy 3.048 2.54) (xy 4.572 4.064) (xy 3.81 4.064)
                (xy 4.572 4.064) (xy 4.572 3.302)
            )
            (stroke (width 0.2032) (type default))
            (fill (type none))
        )
        """)

    # Write pins
    write_pin(symbol_file, 5.08, 0, 180, "1", length=3.81, pin_type="passive")
    write_pin(symbol_file, -5.08, 0, 0, "2", length=3.81, pin_type="passive")

    symbol_file.write("\t\t)\n")


def write_circle(
    symbol_file: TextIO,
    x_pos: float,
    y_pos: float,
) -> None:
    """Write a circle to the symbol file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        x_pos (float): X-coordinate of the circle.
        y_pos (float): Y-coordinate of the circle.

    Returns:
        None

    """
    symbol_file.write(f"""
        (circle
            (center {x_pos} {y_pos})
            (radius 0.0254)
            (stroke (width 0.381) (type default))
            (fill (type none))
        )
    """)


def write_p_mos_transistor_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
    vertical_offset: float = 0.0,
) -> None:
    """Write the graphical representation of a P-MOS transistor symbol.

    Args:
        symbol_file: File object for writing the symbol file.
        symbol_name: Name of the symbol.
        vertical_offset:
            Vertical translation in units.
            Positive moves up, negative moves down. Defaults to 0.0.

    Returns:
        None

    """
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')

    def offset_y(y: float) -> float:
        """Offset y-coordinate by vertical translation."""
        return y + vertical_offset

    symbol_file.write(f"""
        (polyline
            (pts
                (xy 0 {offset_y(-6.35)}) (xy 0 {offset_y(-2.54)})
                (xy -2.54 {offset_y(-2.54)}) (xy 2.54 {offset_y(-2.54)})
                (xy 0 {offset_y(-2.54)}) (xy 0 {offset_y(-6.35)})
            )
            (stroke (width 0) (type default))
            (fill (type outline))
        )
        (polyline
            (pts
                (xy -5.08 {offset_y(1.27)}) (xy -5.08 {offset_y(0)})
                (xy -2.54 {offset_y(0)}) (xy -2.032 {offset_y(0)})
                (xy -2.032 {offset_y(-2.032)}) (xy -2.54 {offset_y(-2.032)})
                (xy -1.524 {offset_y(-2.032)}) (xy -2.032 {offset_y(-2.032)})
                (xy -2.032 {offset_y(0)}) (xy -2.54 {offset_y(0)})
                (xy -2.54 {offset_y(1.27)}) (xy -0.508 {offset_y(1.27)})
                (xy -0.508 {offset_y(0.762)}) (xy 0.508 {offset_y(1.27)})
                (xy 0.508 {offset_y(0.762)}) (xy 0.508 {offset_y(1.27)})
                (xy 2.54 {offset_y(1.27)}) (xy 2.54 {offset_y(0)})
                (xy 0 {offset_y(0)}) (xy -0.508 {offset_y(-1.016)})
                (xy 0 {offset_y(-1.016)}) (xy 0 {offset_y(-2.032)})
                (xy -0.508 {offset_y(-2.032)}) (xy 0.508 {offset_y(-2.032)})
                (xy 0 {offset_y(-2.032)}) (xy 0 {offset_y(-1.016)})
                (xy 0.508 {offset_y(-1.016)}) (xy 0 {offset_y(0)})
                (xy 2.032 {offset_y(0)}) (xy 2.032 {offset_y(-2.032)})
                (xy 1.524 {offset_y(-2.032)}) (xy 2.54 {offset_y(-2.032)})
                (xy 2.032 {offset_y(-2.032)}) (xy 2.032 {offset_y(0)})
                (xy 2.54 {offset_y(0)}) (xy 5.08 {offset_y(0)})
                (xy 5.08 {offset_y(-3.81)}) (xy 5.08 {offset_y(1.27)})
                (xy 5.08 {offset_y(0)}) (xy 2.54 {offset_y(0)})
                (xy 2.54 {offset_y(1.27)}) (xy 0.508 {offset_y(1.27)})
                (xy 0.508 {offset_y(1.778)}) (xy 0.508 {offset_y(1.27)})
                (xy -0.508 {offset_y(1.778)}) (xy -0.508 {offset_y(1.27)})
                (xy -2.54 {offset_y(1.27)}) (xy -2.54 {offset_y(0)})
                (xy -5.08 {offset_y(0)}) (xy -5.08 {offset_y(1.27)})
            )
            (stroke (width 0) (type default))
            (fill (type outline))
        )
        """)

    # Write symbol circles with vertical offset
    write_circle(symbol_file, -2.54, offset_y(0))
    write_circle(symbol_file, 2.032, offset_y(0))
    write_circle(symbol_file, 2.54, offset_y(0))

    # Write pins with vertical offset
    write_pin(symbol_file, -7.62, offset_y(1.27), 0, "5", "D", length=2.54)
    write_pin(symbol_file, 7.62, offset_y(1.27), 180, "1", "S", length=2.54)
    write_pin(symbol_file, 7.62, offset_y(-1.27), 180, "2", "S", length=2.54)
    write_pin(symbol_file, 7.62, offset_y(-3.81), 180, "3", "S", length=2.54)
    write_pin(symbol_file, 2.54, offset_y(-6.35), 180, "4", "G", length=2.54)

    symbol_file.write("\t\t)\n")


def write_p_mos_transistor_symbol_drawing_2(
    symbol_file: TextIO,
    symbol_name: str,
    vertical_offset: float = 0.0,
) -> None:
    """Write the graphical representation of a P-MOS transistor symbol.

    Args:
        symbol_file: File object for writing the symbol file.
        symbol_name: Name of the symbol.
        vertical_offset:
            Vertical translation in units.
            Positive moves up, negative moves down. Defaults to 0.0.

    Returns:
        None

    """
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')

    def offset_y(y: float) -> float:
        """Offset y-coordinate by vertical translation."""
        return y + vertical_offset

    symbol_file.write(f"""
        (polyline
            (pts
                (xy 0 {offset_y(-6.35)}) (xy 0 {offset_y(-2.54)})
                (xy -2.54 {offset_y(-2.54)}) (xy 2.54 {offset_y(-2.54)})
                (xy 0 {offset_y(-2.54)}) (xy 0 {offset_y(-6.35)})
            )
            (stroke (width 0) (type default))
            (fill (type outline))
        )
        (polyline
            (pts
                (xy -5.08 {offset_y(1.27)}) (xy -5.08 {offset_y(-6.35)})
                (xy -5.08 {offset_y(0)}) (xy -2.54 {offset_y(0)})
                (xy -2.032 {offset_y(0)}) (xy -2.032 {offset_y(-2.032)})
                (xy -2.54 {offset_y(-2.032)}) (xy -1.524 {offset_y(-2.032)})
                (xy -2.032 {offset_y(-2.032)}) (xy -2.032 {offset_y(0)})
                (xy -2.54 {offset_y(0)}) (xy -2.54 {offset_y(1.27)})
                (xy -0.508 {offset_y(1.27)}) (xy -0.508 {offset_y(0.762)})
                (xy 0.508 {offset_y(1.27)}) (xy 0.508 {offset_y(0.762)})
                (xy 0.508 {offset_y(1.27)}) (xy 2.54 {offset_y(1.27)})
                (xy 2.54 {offset_y(0)}) (xy 0 {offset_y(0)})
                (xy -0.508 {offset_y(-1.016)}) (xy 0 {offset_y(-1.016)})
                (xy 0 {offset_y(-2.032)}) (xy -0.508 {offset_y(-2.032)})
                (xy 0.508 {offset_y(-2.032)}) (xy 0 {offset_y(-2.032)})
                (xy 0 {offset_y(-1.016)}) (xy 0.508 {offset_y(-1.016)})
                (xy 0 {offset_y(0)}) (xy 2.032 {offset_y(0)})
                (xy 2.032 {offset_y(-2.032)}) (xy 1.524 {offset_y(-2.032)})
                (xy 2.54 {offset_y(-2.032)})
                (xy 2.032 {offset_y(-2.032)})
                (xy 2.032 {offset_y(0)}) (xy 2.54 {offset_y(0)})
                (xy 5.08 {offset_y(0)}) (xy 5.08 {offset_y(1.27)})
                (xy 5.08 {offset_y(0)}) (xy 2.54 {offset_y(0)})
                (xy 2.54 {offset_y(1.27)}) (xy 0.508 {offset_y(1.27)})
                (xy 0.508 {offset_y(1.778)}) (xy 0.508 {offset_y(1.27)})
                (xy -0.508 {offset_y(1.778)}) (xy -0.508 {offset_y(1.27)})
                (xy -2.54 {offset_y(1.27)}) (xy -2.54 {offset_y(0)})
                (xy -5.08 {offset_y(0)})
            )
            (stroke (width 0) (type default))
            (fill (type outline))
        )
        """)

    # Write symbol circles with vertical offset
    write_circle(symbol_file, -2.54, offset_y(0))
    write_circle(symbol_file, 2.032, offset_y(0))
    write_circle(symbol_file, 2.54, offset_y(0))

    # Write pins with vertical offset
    write_pin(symbol_file, -7.62, offset_y(1.27), 0, "1", "D", length=2.54)
    write_pin(symbol_file, -7.62, offset_y(-1.27), 0, "2", "D", length=2.54)
    write_pin(symbol_file, -7.62, offset_y(-3.81), 0, "5", "D", length=2.54)
    write_pin(symbol_file, -7.62, offset_y(-6.35), 0, "6", "D", length=2.54)
    write_pin(symbol_file, 7.62, offset_y(1.27), 180, "4", "S", length=2.54)
    write_pin(symbol_file, 2.54, offset_y(-6.35), 180, "3", "G", length=2.54)

    symbol_file.write("\t\t)\n")


def write_n_mos_transistor_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
    vertical_offset: float = 0.0,
) -> None:
    """Write the graphical representation of an N-MOS transistor symbol.

    Args:
        symbol_file: File object for writing the symbol file.
        symbol_name: Name of the symbol.
        vertical_offset:
            Vertical translation in units.
            Positive moves up, negative moves down. Defaults to 0.0.

    Returns:
        None

    """
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')

    def offset_y(y: float) -> float:
        """Offset y-coordinate by vertical translation.

        Args:
            y: Y-coordinate to offset.

        Returns:
            float: Offset y-coordinate.

        """
        return y + vertical_offset

    symbol_file.write(f"""
        (polyline
            (pts
                (xy 0 {offset_y(-6.35)}) (xy 0 {offset_y(-2.54)})
                (xy -2.54 {offset_y(-2.54)}) (xy 2.54 {offset_y(-2.54)})
                (xy 0 {offset_y(-2.54)}) (xy 0 {offset_y(-6.35)})
            )
            (stroke (width 0) (type default))
            (fill (type none))
        )
        (polyline
            (pts
                (xy 5.08 {offset_y(1.27)}) (xy 5.08 {offset_y(0)})
                (xy 2.54 {offset_y(0)}) (xy 2.54 {offset_y(1.27)})
                (xy 0.508 {offset_y(1.27)}) (xy 0.508 {offset_y(1.778)})
                (xy -0.508 {offset_y(1.27)}) (xy -0.508 {offset_y(1.778)})
                (xy -0.508 {offset_y(1.27)}) (xy -2.54 {offset_y(1.27)})
                (xy -2.54 {offset_y(0)}) (xy -5.08 {offset_y(0)})
                (xy -5.08 {offset_y(1.27)}) (xy -5.08 {offset_y(0)})
                (xy -2.032 {offset_y(0)}) (xy -2.032 {offset_y(-2.032)})
                (xy -2.54 {offset_y(-2.032)}) (xy -1.524 {offset_y(-2.032)})
                (xy -2.032 {offset_y(-2.032)}) (xy -2.032 {offset_y(0)})
                (xy -2.54 {offset_y(0)}) (xy -2.54 {offset_y(1.27)})
                (xy -0.508 {offset_y(1.27)}) (xy -0.508 {offset_y(0.762)})
                (xy -0.508 {offset_y(1.27)}) (xy 0.508 {offset_y(0.762)})
                (xy 0.508 {offset_y(1.27)}) (xy 2.54 {offset_y(1.27)})
                (xy 2.54 {offset_y(0)}) (xy 0 {offset_y(0)})
                (xy 0 {offset_y(-1.016)}) (xy -0.508 {offset_y(-1.016)})
                (xy 0 {offset_y(-2.032)}) (xy -0.508 {offset_y(-2.032)})
                (xy 0.508 {offset_y(-2.032)}) (xy 0 {offset_y(-2.032)})
                (xy 0.508 {offset_y(-1.016)}) (xy 0 {offset_y(-1.016)})
                (xy 0 {offset_y(0)}) (xy 2.032 {offset_y(0)})
                (xy 2.032 {offset_y(-2.032)}) (xy 1.524 {offset_y(-2.032)})
                (xy 2.54 {offset_y(-2.032)}) (xy 2.032 {offset_y(-2.032)})
                (xy 2.032 {offset_y(0)}) (xy 5.08 {offset_y(0)})
                (xy 5.08 {offset_y(-3.81)})
            )
            (stroke (width 0) (type default))
            (fill (type outline))
        )
        """)

    # Write symbol circles with vertical offset
    write_circle(symbol_file, -2.54, offset_y(0))
    write_circle(symbol_file, 2.032, offset_y(0))
    write_circle(symbol_file, 2.54, offset_y(0))

    # Write pins with vertical offset
    write_pin(symbol_file, -7.62, offset_y(1.27), 0, "5", "D", length=2.54)
    write_pin(symbol_file, 7.62, offset_y(1.27), 180, "1", "S", length=2.54)
    write_pin(symbol_file, 7.62, offset_y(-1.27), 180, "2", "S", length=2.54)
    write_pin(symbol_file, 7.62, offset_y(-3.81), 180, "3", "S", length=2.54)
    write_pin(symbol_file, 2.54, offset_y(-6.35), 180, "4", "G", length=2.54)

    symbol_file.write("\t\t)\n")


def write_n_mos_basic_transistor_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
    vertical_offset: float = 0.0,
) -> None:
    """Write the graphical representation of an N-MOS transistor symbol.

    Args:
        symbol_file: File object for writing the symbol file.
        symbol_name: Name of the symbol.
        vertical_offset:
            Vertical translation in units.
            Positive moves up, negative moves down. Defaults to 0.0.

    Returns:
        None

    """
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')

    def offset_y(y: float) -> float:
        """Offset y-coordinate by vertical translation.

        Args:
            y: Y-coordinate to offset.

        Returns:
            float: Offset y-coordinate.

        """
        return y + vertical_offset

    symbol_file.write(f"""
        (polyline
            (pts
                (xy 0 {offset_y(-6.35)}) (xy 0 {offset_y(-2.54)})
                (xy -2.54 {offset_y(-2.54)}) (xy 2.54 {offset_y(-2.54)})
                (xy 0 {offset_y(-2.54)}) (xy 0 {offset_y(-6.35)})
            )
            (stroke (width 0) (type default))
            (fill (type none))
        )
        (polyline
            (pts
                (xy 5.08 {offset_y(1.27)}) (xy 5.08 {offset_y(0)})
                (xy 2.54 {offset_y(0)}) (xy 2.54 {offset_y(1.27)})
                (xy 0.508 {offset_y(1.27)}) (xy 0.508 {offset_y(1.778)})
                (xy -0.508 {offset_y(1.27)}) (xy -0.508 {offset_y(1.778)})
                (xy -0.508 {offset_y(1.27)}) (xy -2.54 {offset_y(1.27)})
                (xy -2.54 {offset_y(0)}) (xy -5.08 {offset_y(0)})
                (xy -5.08 {offset_y(1.27)}) (xy -5.08 {offset_y(0)})
                (xy -2.032 {offset_y(0)}) (xy -2.032 {offset_y(-2.032)})
                (xy -2.54 {offset_y(-2.032)}) (xy -1.524 {offset_y(-2.032)})
                (xy -2.032 {offset_y(-2.032)}) (xy -2.032 {offset_y(0)})
                (xy -2.54 {offset_y(0)}) (xy -2.54 {offset_y(1.27)})
                (xy -0.508 {offset_y(1.27)}) (xy -0.508 {offset_y(0.762)})
                (xy -0.508 {offset_y(1.27)}) (xy 0.508 {offset_y(0.762)})
                (xy 0.508 {offset_y(1.27)}) (xy 2.54 {offset_y(1.27)})
                (xy 2.54 {offset_y(0)}) (xy 0 {offset_y(0)})
                (xy 0 {offset_y(-1.016)}) (xy -0.508 {offset_y(-1.016)})
                (xy 0 {offset_y(-2.032)}) (xy -0.508 {offset_y(-2.032)})
                (xy 0.508 {offset_y(-2.032)}) (xy 0 {offset_y(-2.032)})
                (xy 0.508 {offset_y(-1.016)}) (xy 0 {offset_y(-1.016)})
                (xy 0 {offset_y(0)}) (xy 2.032 {offset_y(0)})
                (xy 2.032 {offset_y(-2.032)}) (xy 1.524 {offset_y(-2.032)})
                (xy 2.54 {offset_y(-2.032)}) (xy 2.032 {offset_y(-2.032)})
                (xy 2.032 {offset_y(0)}) (xy 5.08 {offset_y(0)})
            )
            (stroke (width 0) (type default))
            (fill (type outline))
        )
        """)

    # Write symbol circles with vertical offset
    write_circle(symbol_file, -2.54, offset_y(0))
    write_circle(symbol_file, 2.032, offset_y(0))
    write_circle(symbol_file, 2.54, offset_y(0))

    # Write pins with vertical offset
    write_pin(symbol_file, 2.54, offset_y(-6.35), 180, "1", "G", length=2.54)
    write_pin(symbol_file, 7.62, offset_y(1.27), 180, "2", "S", length=2.54)
    write_pin(symbol_file, -7.62, offset_y(1.27), 0, "3", "D", length=2.54)

    symbol_file.write("\t\t)\n")


def write_n_mos_dual_transistor_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
    vertical_offset: float = 1.27,
) -> None:
    """Write the horizontal graphical representation of a diode symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
        vertical_offset:
            Vertical translation in units.
            Positive moves up, negative moves down. Defaults to 0.0.

    Returns:
        None

    """

    def offset_y(y: float) -> float:
        """Offset y-coordinate by vertical translation.

        Args:
            y: Y-coordinate to offset.

        Returns:
            float: Offset y-coordinate.

        """
        return y + vertical_offset

    pin_specs = (
        {"1": "S1", "2": "G1", "6": "D1"},
        {"3": "S2", "4": "G2", "5": "D2"},
    )

    number = [list(pin_spec.keys()) for pin_spec in pin_specs]
    name = [list(pin_spec.values()) for pin_spec in pin_specs]

    for index in range(1, 3):
        symbol_file.write(f"""
            (symbol "{symbol_name}_{index}_0"
                (polyline
                    (pts
                        (xy 0 {offset_y(-5.08)})
                        (xy 0 {offset_y(-1.27)})
                        (xy -2.54 {offset_y(-1.27)})
                        (xy 2.54 {offset_y(-1.27)})
                        (xy 0 {offset_y(-1.27)})
                        (xy 0 {offset_y(-5.08)})
                    )
                    (stroke (width 0) (type default))
                    (fill (type none))
                )
                (polyline
                    (pts
                        (xy 7.62 {offset_y(2.54)})
                        (xy 7.62 {offset_y(1.27)})
                        (xy 2.54 {offset_y(1.27)})
                        (xy 2.54 {offset_y(2.54)})
                        (xy 0.508 {offset_y(2.54)})
                        (xy 0.508 {offset_y(3.048)})
                        (xy -0.508 {offset_y(2.54)})
                        (xy -0.508 {offset_y(3.048)})
                        (xy -0.508 {offset_y(2.54)})
                        (xy -2.54 {offset_y(2.54)})
                        (xy -2.54 {offset_y(1.27)})
                        (xy -7.62 {offset_y(1.27)})
                        (xy -7.62 {offset_y(2.54)})
                        (xy -7.62 {offset_y(1.27)})
                        (xy -2.032 {offset_y(1.27)})
                        (xy -2.032 {offset_y(-0.762)})
                        (xy -2.54 {offset_y(-0.762)})
                        (xy -1.524 {offset_y(-0.762)})
                        (xy -2.032 {offset_y(-0.762)})
                        (xy -2.032 {offset_y(1.27)})
                        (xy -2.54 {offset_y(1.27)})
                        (xy -2.54 {offset_y(2.54)})
                        (xy -0.508 {offset_y(2.54)})
                        (xy -0.508 {offset_y(2.032)})
                        (xy -0.508 {offset_y(2.54)})
                        (xy 0.508 {offset_y(2.032)})
                        (xy 0.508 {offset_y(2.54)})
                        (xy 2.54 {offset_y(2.54)})
                        (xy 2.54 {offset_y(1.27)})
                        (xy 0 {offset_y(1.27)})
                        (xy 0 {offset_y(0.254)})
                        (xy -0.508 {offset_y(0.254)})
                        (xy 0 {offset_y(-0.762)})
                        (xy -0.508 {offset_y(-0.762)})
                        (xy 0.508 {offset_y(-0.762)})
                        (xy 0 {offset_y(-0.762)})
                        (xy 0.508 {offset_y(0.254)})
                        (xy 0 {offset_y(0.254)})
                        (xy 0 {offset_y(1.27)})
                        (xy 2.032 {offset_y(1.27)})
                        (xy 2.032 {offset_y(-0.762)})
                        (xy 1.524 {offset_y(-0.762)})
                        (xy 2.54 {offset_y(-0.762)})
                        (xy 2.032 {offset_y(-0.762)})
                        (xy 2.032 {offset_y(1.27)})
                        (xy 7.62 {offset_y(1.27)})
                        (xy 7.62 {offset_y(2.54)})
                    )
                    (stroke (width 0) (type default))
                    (fill (type outline))
                )
            """)

        # Write symbol circles with vertical offset
        write_circle(symbol_file, -2.54, offset_y(1.27))
        write_circle(symbol_file, 2.032, offset_y(1.27))
        write_circle(symbol_file, 2.54, offset_y(1.27))

        # Write pins with vertical offset
        write_pin(
            symbol_file,
            10.16,
            offset_y(2.54),
            180,
            number[index - 1][0],
            name[index - 1][0],
        )
        write_pin(
            symbol_file,
            2.54,
            offset_y(-5.08),
            180,
            number[index - 1][1],
            name[index - 1][1],
        )
        write_pin(
            symbol_file,
            -10.16,
            offset_y(2.54),
            0,
            number[index - 1][2],
            name[index - 1][2],
        )

        symbol_file.write(")")


def write_p_mos_dual_transistor_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
    vertical_offset: float = 1.27,
) -> None:
    """Write the horizontal graphical representation of a diode symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
        vertical_offset:
            Vertical translation in units.
            Positive moves up, negative moves down. Defaults to 0.0.

    Returns:
        None

    """

    def offset_y(y: float) -> float:
        """Offset y-coordinate by vertical translation.

        Args:
            y (float): Y-coordinate.

        Returns:
            float: Y-coordinate with vertical offset.

        """
        return y + vertical_offset

    pin_specs = (
        {"1": "S1", "2": "G1", "6": "D1"},
        {"3": "S2", "4": "G2", "5": "D2"},
    )

    number = [list(pin_spec.keys()) for pin_spec in pin_specs]
    name = [list(pin_spec.values()) for pin_spec in pin_specs]

    for index in range(1, 3):
        symbol_file.write(f"""
            (symbol "{symbol_name}_{index}_0"
                (polyline
                    (pts
                        (xy 0 {offset_y(-5.08)})
                        (xy 0 {offset_y(-1.27)})
                        (xy -2.54 {offset_y(-1.27)})
                        (xy 2.54 {offset_y(-1.27)})
                        (xy 0 {offset_y(-1.27)})
                        (xy 0 {offset_y(-5.08)})
                    )
                    (stroke (width 0) (type default))
                    (fill (type outline))
                )
                (polyline
                    (pts
                        (xy -7.62 {offset_y(2.54)})
                        (xy -7.62 {offset_y(1.27)})
                        (xy -2.54 {offset_y(1.27)})
                        (xy -2.032 {offset_y(1.27)})
                        (xy -2.032 {offset_y(-0.762)})
                        (xy -2.54 {offset_y(-0.762)})
                        (xy -1.524 {offset_y(-0.762)})
                        (xy -2.032 {offset_y(-0.762)})
                        (xy -2.032 {offset_y(1.27)})
                        (xy -2.54 {offset_y(1.27)})
                        (xy -2.54 {offset_y(2.54)})
                        (xy -0.508 {offset_y(2.54)})
                        (xy -0.508 {offset_y(2.032)})
                        (xy 0.508 {offset_y(2.54)})
                        (xy 0.508 {offset_y(2.032)})
                        (xy 0.508 {offset_y(2.54)})
                        (xy 2.54 {offset_y(2.54)})
                        (xy 2.54 {offset_y(1.27)})
                        (xy 0 {offset_y(1.27)})
                        (xy -0.508 {offset_y(0.254)})
                        (xy 0 {offset_y(0.254)})
                        (xy 0 {offset_y(-0.762)})
                        (xy -0.508 {offset_y(-0.762)})
                        (xy 0.508 {offset_y(-0.762)})
                        (xy 0 {offset_y(-0.762)})
                        (xy 0 {offset_y(0.254)})
                        (xy 0.508 {offset_y(0.254)})
                        (xy 0 {offset_y(1.27)})
                        (xy 2.032 {offset_y(1.27)})
                        (xy 2.032 {offset_y(-0.762)})
                        (xy 1.524 {offset_y(-0.762)})
                        (xy 2.54 {offset_y(-0.762)})
                        (xy 2.032 {offset_y(-0.762)})
                        (xy 2.032 {offset_y(1.27)})
                        (xy 2.54 {offset_y(1.27)})
                        (xy 7.62 {offset_y(1.27)})
                        (xy 7.62 {offset_y(2.54)})
                        (xy 7.62 {offset_y(2.54)})
                        (xy 7.62 {offset_y(1.27)})
                        (xy 2.54 {offset_y(1.27)})
                        (xy 2.54 {offset_y(2.54)})
                        (xy 0.508 {offset_y(2.54)})
                        (xy 0.508 {offset_y(3.048)})
                        (xy 0.508 {offset_y(2.54)})
                        (xy -0.508 {offset_y(3.048)})
                        (xy -0.508 {offset_y(2.54)})
                        (xy -2.54 {offset_y(2.54)})
                        (xy -2.54 {offset_y(1.27)})
                        (xy -7.62 {offset_y(1.27)})
                        (xy -7.62 {offset_y(2.54)})
                    )
                    (stroke (width 0) (type default))
                    (fill (type outline))
                )
            """)

        # Write symbol circles with vertical offset
        write_circle(symbol_file, -2.54, offset_y(1.27))
        write_circle(symbol_file, 2.032, offset_y(1.27))
        write_circle(symbol_file, 2.54, offset_y(1.27))

        # Write pins with vertical offset
        write_pin(
            symbol_file,
            10.16,
            offset_y(2.54),
            180,
            number[index - 1][0],
            name[index - 1][0],
        )
        write_pin(
            symbol_file,
            2.54,
            offset_y(-5.08),
            180,
            number[index - 1][1],
            name[index - 1][1],
        )
        write_pin(
            symbol_file,
            -10.16,
            offset_y(2.54),
            0,
            number[index - 1][2],
            name[index - 1][2],
        )

        symbol_file.write(")")


def write_connector_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
    component_data: dict[str, str],
) -> None:
    """Write the horizontal graphical representation of a connector symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
        component_data (dict[str, str]): Component data.

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
    for pin_num in range(1, pin_count + 1):
        y_pos = start_y - (pin_num - 1) * pin_spacing
        write_pin(symbol_file, -5.08, y_pos, 0, str(pin_num))

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
    """Write a rectangle definition with specific formatting."""
    symbol_file.write(f"""
        (rectangle
            (start {start_x} {start_y})
            (end {end_x} {end_y})
            (stroke (width 0.254) (type solid))
            (fill (type none))
        )
        """)


def write_npn_transistor_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
    vertical_offset: float = 0.0,
) -> None:
    """Write the graphical representation of a P-MOS transistor symbol.

    Args:
        symbol_file: File object for writing the symbol file.
        symbol_name: Name of the symbol.
        vertical_offset:
            Vertical translation in units.
            Positive moves up, negative moves down. Defaults to 0.0.

    Returns:
        None

    """
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')

    symbol_file.write("""
			(polyline
				(pts (xy -2.54 0) (xy 0.635 0))
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(polyline
				(pts (xy 0.635 1.905) (xy 0.635 -1.905))
				(stroke (width 0.508) (type default))
				(fill (type none))
			)
			(polyline
				(pts (xy 0.635 0.635) (xy 2.54 2.54))
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(polyline
				(pts (xy 0.635 -0.635) (xy 2.54 -2.54))
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(circle
				(center 1.27 0)
				(radius 2.8194)
				(stroke (width 0.254) (type default))
				(fill (type none))
			)
			(polyline
				(pts
					(xy 1.27 -1.778) (xy 1.778 -1.27)
                    (xy 2.286 -2.286) (xy 1.27 -1.778)
				)
				(stroke (width 0) (type default))
				(fill (type outline))
			)
        """)

    write_pin(symbol_file, -5.08, 0, 0, "1", "B", length=2.54)
    write_pin(symbol_file, 2.54, 5.08, 270, "3", "C", length=2.54)
    write_pin(symbol_file, 2.54, -5.08, 90, "2", "E", length=2.54)

    symbol_file.write("\t\t)\n")


def write_pnp_transistor_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
    vertical_offset: float = 0.0,
) -> None:
    """Write the graphical representation of a P-MOS transistor symbol.

    Args:
        symbol_file: File object for writing the symbol file.
        symbol_name: Name of the symbol.
        vertical_offset:
            Vertical translation in units.
            Positive moves up, negative moves down. Defaults to 0.0.

    Returns:
        None

    """
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')

    symbol_file.write("""
			(polyline
				(pts (xy -2.54 0) (xy 0.635 0))
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(polyline
				(pts (xy 0.635 1.905) (xy 0.635 -1.905))
				(stroke (width 0.508) (type default))
				(fill (type none))
			)
			(polyline
				(pts (xy 0.635 0.635) (xy 2.54 2.54))
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(polyline
				(pts (xy 0.635 -0.635) (xy 2.54 -2.54))
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(polyline
				(pts
					(xy 1.27 1.778) (xy 1.778 1.27)
                    (xy 0.762 0.762) (xy 1.27 1.778)
				)
				(stroke (width 0) (type default))
				(fill (type outline))
			)
			(circle
				(center 1.27 0)
				(radius 2.8194)
				(stroke (width 0.254) (type default))
				(fill (type none))
			)
        """)

    write_pin(symbol_file, -5.08, 0, 0, "1", "B", length=2.54)
    write_pin(symbol_file, 2.54, 5.08, 270, "2", "E", length=2.54)
    write_pin(symbol_file, 2.54, -5.08, 90, "3", "C", length=2.54)

    symbol_file.write("\t\t)\n")


def write_dip_switch_symbol_drawing(
    *,
    symbol_file: TextIO,
    symbol_name: str,
    component_data: dict[str, str],
    number_of_rows: int,
    specs_dict: dict,
    anti_clockwise_numbering: bool = False,
) -> None:
    """Write the drawing for a standard dip switch symbol.

    Creates KiCad symbol definition with appropriate pin layout and
    standard dip switch graphical representation including switch
    contacts and actuator mechanism.

    Args:
        symbol_file: File object for writing the symbol file.
        symbol_name: Name identifier for the symbol.
        component_data: Dictionary containing component specifications.
        number_of_rows: Number of pin rows in the component layout.
        specs_dict: Dictionary containing component specifications.
        anti_clockwise_numbering: Use anti-clockwise pin numbering scheme.

    """
    pin_count = int(component_data.get("Pin Count", "2"))
    pin_spacing = 2.54

    symbol_file.write(f'\t\t(symbol "{symbol_name}_0_0"\n')

    override_pins = get_override_pins_specs(
        component_data.get("Series", ""),
        specs_dict,
    )

    if override_pins:
        for pin_num, x_pos, y_pos, angle in override_pins:
            write_pin(
                symbol_file, x_pos, y_pos, angle, pin_num, pin_type="passive"
            )
    else:
        total_pins = pin_count * 2
        pins_per_side = total_pins // 2

        start_y = (pins_per_side - 1) * pin_spacing / 2

        if number_of_rows == 2:
            if anti_clockwise_numbering:
                for i in range(pins_per_side):
                    pin_num = (i * 2) + 1
                    y_pos = start_y - i * pin_spacing
                    write_pin(
                        symbol_file,
                        -5.08,
                        y_pos,
                        0,
                        str(pin_num),
                        pin_type="passive",
                    )

                for i in range(pins_per_side):
                    pin_num = (i * 2) + 2
                    y_pos = start_y - i * pin_spacing
                    write_pin(
                        symbol_file,
                        5.08,
                        y_pos,
                        180,
                        str(pin_num),
                        pin_type="passive",
                    )
            else:
                for i in range(pins_per_side):
                    pin_num = i + 1
                    y_pos = start_y - i * pin_spacing
                    write_pin(
                        symbol_file,
                        -5.08,
                        y_pos,
                        0,
                        str(pin_num),
                        pin_type="passive",
                    )

                for i in range(pins_per_side):
                    pin_num = total_pins - i
                    y_pos = start_y - i * pin_spacing
                    write_pin(
                        symbol_file,
                        5.08,
                        y_pos,
                        180,
                        str(pin_num),
                        pin_type="passive",
                    )

        else:
            for pin_num in range(1, pin_count + 1):
                if anti_clockwise_numbering:
                    actual_pin_num = pin_count - pin_num + 1
                else:
                    actual_pin_num = pin_num
                y_pos = start_y - (pin_num - 1) * pin_spacing
                write_pin(
                    symbol_file,
                    -5.08,
                    y_pos,
                    0,
                    str(actual_pin_num),
                    pin_type="passive",
                )

    for switch_idx in range(pin_count):
        if number_of_rows == 2:
            y_offset = start_y - switch_idx * pin_spacing
        else:
            y_offset = start_y - switch_idx * pin_spacing

        symbol_file.write(f"""
			(polyline
				(pts
					(xy -2.54 {y_offset}) (xy -1.27 {y_offset})
                    (xy 1.27 {y_offset + 1.27})
				)
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(circle
				(center -1.27 {y_offset})
				(radius 0.254)
				(stroke (width 0) (type solid))
				(fill (type outline))
			)
			(circle
				(center 1.27 {y_offset})
				(radius 0.254)
				(stroke (width 0) (type solid))
				(fill (type outline))
			)
			(polyline
				(pts (xy 2.54 {y_offset}) (xy 1.27 {y_offset}))
				(stroke (width 0) (type default))
				(fill (type none))
			)""")

    symbol_file.write("\t\t)\n")

    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')
    symbol_file.write("\t\t)\n")


def write_slide_switch_symbol_drawing(
    *,
    symbol_file: TextIO,
    symbol_name: str,
    component_data: dict[str, str],
    number_of_rows: int,
    specs_dict: dict,
) -> None:
    """Write the drawing for a standard tactile switch symbol.

    Creates KiCad symbol definition with appropriate pin layout and
    standard tactile switch graphical representation including switch
    contacts and actuator mechanism.

    Args:
        symbol_file: File object for writing the symbol file.
        symbol_name: Name identifier for the symbol.
        component_data: Dictionary containing component specifications.
        number_of_rows: Number of pin rows in the component layout.
        specs_dict: Dictionary containing component specifications.

    """
    pin_count = int(component_data.get("Pin Count", "2"))
    pin_spacing = 5.08 * 2

    symbol_file.write(f'\t\t(symbol "{symbol_name}_0_0"\n')

    # Check for override pin specs
    override_pins = get_override_pins_specs(
        component_data.get("Series", ""),
        specs_dict,
    )

    if override_pins:
        for pin_num, x_pos, y_pos, angle in override_pins:
            write_pin(
                symbol_file, x_pos, y_pos, angle, pin_num, pin_type="passive"
            )
    else:
        start_y = (pin_count - 1) * pin_spacing / 2

        def toggle_angle(current):
            return 90 if current == 270 else 270

        if number_of_rows == 2:  # noqa: PLR2004
            angle = 270  # Start with 270
            for pin_num in range(1, pin_count * 2, 2):
                y_pos = start_y - (pin_num - 1) * pin_spacing / 2

                # Both pins in this row use the same angle
                write_pin(
                    symbol_file,
                    -2.54 / 2,
                    y_pos,
                    angle,
                    str(pin_num),
                    pin_type="passive",
                )
                write_pin(
                    symbol_file,
                    2.54 / 2,
                    y_pos,
                    angle,
                    str(pin_num + 1),
                    pin_type="passive",
                )

                # Toggle angle for next row
                angle = toggle_angle(angle)
        else:
            for pin_num in range(1, pin_count + 1):
                y_pos = start_y - (pin_num - 1) * pin_spacing
                write_pin(
                    symbol_file,
                    -5.08,
                    y_pos,
                    0,
                    str(pin_num),
                    pin_type="passive",
                )

    symbol_file.write("""
			(polyline
				(pts (xy -2.54 0) (xy 0 0) (xy 2.032 2.286))
				(stroke (width 0.2032) (type solid))
				(fill (type none))
			)
			(circle
				(center 2.286 2.54)
				(radius 0.254)
				(stroke (width 0.2032) (type solid))
				(fill (type none))
			)
			(circle
				(center 2.286 -2.54)
				(radius 0.254)
				(stroke (width 0.2032) (type solid))
				(fill (type none))
			)
    """)

    symbol_file.write("\t\t)\n")

    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')
    symbol_file.write("\t\t)\n")


def write_tactile_switch_symbol_drawing(
    *,
    symbol_file: TextIO,
    symbol_name: str,
    component_data: dict[str, str],
    number_of_rows: int,
    specs_dict: dict,
) -> None:
    """Write the drawing for a standard tactile switch symbol.

    Creates KiCad symbol definition with appropriate pin layout and
    standard tactile switch graphical representation including switch
    contacts and actuator mechanism.

    Args:
        symbol_file: File object for writing the symbol file.
        symbol_name: Name identifier for the symbol.
        component_data: Dictionary containing component specifications.
        number_of_rows: Number of pin rows in the component layout.
        specs_dict: Dictionary containing component specifications.

    """
    pin_count = int(component_data.get("Pin Count", "2"))
    pin_spacing = 5.08 * 2

    symbol_file.write(f'\t\t(symbol "{symbol_name}_0_0"\n')

    # Check for override pin specs
    override_pins = get_override_pins_specs(
        component_data.get("Series", ""),
        specs_dict,
    )

    if override_pins:
        for pin_num, x_pos, y_pos, angle in override_pins:
            write_pin(
                symbol_file, x_pos, y_pos, angle, pin_num, pin_type="passive"
            )
    else:
        start_y = (pin_count - 1) * pin_spacing / 2

        def toggle_angle(current):
            return 90 if current == 270 else 270

        if number_of_rows == 2:  # noqa: PLR2004
            angle = 270  # Start with 270
            for pin_num in range(1, pin_count * 2, 2):
                y_pos = start_y - (pin_num - 1) * pin_spacing / 2

                # Both pins in this row use the same angle
                write_pin(
                    symbol_file,
                    -2.54 / 2,
                    y_pos,
                    angle,
                    str(pin_num),
                    pin_type="passive",
                )
                write_pin(
                    symbol_file,
                    2.54 / 2,
                    y_pos,
                    angle,
                    str(pin_num + 1),
                    pin_type="passive",
                )

                # Toggle angle for next row
                angle = toggle_angle(angle)
        else:
            for pin_num in range(1, pin_count + 1):
                y_pos = start_y - (pin_num - 1) * pin_spacing
                write_pin(
                    symbol_file,
                    -5.08,
                    y_pos,
                    0,
                    str(pin_num),
                    pin_type="passive",
                )

    symbol_file.write("""
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
    *,
    symbol_file: TextIO,
    symbol_name: str,
    component_data: dict[str, str],
    number_of_rows: int,
    led_color: dict[str, int],
    specs_dict: dict,
) -> None:
    """Write the drawing for a tactile switch symbol with LED indicator.

    Creates KiCad symbol definition for TS29 series tactile switches that
    include integrated LED indicators. Renders both switch mechanism and
    LED with appropriate color coding.

    Args:
        symbol_file: File object for writing the symbol file.
        symbol_name: Name identifier for the symbol.
        component_data: Dictionary containing component specifications.
        number_of_rows: Number of pin rows in the component layout.
        led_color: Dictionary with RGB color values for LED representation.
        specs_dict: Dictionary containing component specifications.

    """
    pin_count = int(component_data.get("Pin Count", "2"))
    pin_spacing = 5.08 * 2

    symbol_file.write(f'\t\t(symbol "{symbol_name}_0_0"\n')

    # Check for override pin specs
    override_pins = get_override_pins_specs(
        component_data.get("Series", ""),
        specs_dict,
    )

    if override_pins:
        for pin_num, x_pos, y_pos, angle in override_pins:
            write_pin(
                symbol_file, x_pos, y_pos, angle, pin_num, pin_type="passive"
            )
    else:
        start_y = (pin_count - 1) * pin_spacing / 2

        def toggle_angle(current):
            return 90 if current == 270 else 270

        if number_of_rows == 2:  # noqa: PLR2004
            angle = 270  # Start with 270
            for pin_num in range(1, pin_count * 2, 2):
                y_pos = start_y - (pin_num - 1) * pin_spacing / 2

                # Both pins in this row use the same angle
                write_pin(
                    symbol_file,
                    -2.54 / 2,
                    y_pos,
                    angle,
                    str(pin_num),
                    pin_type="passive",
                )
                write_pin(
                    symbol_file,
                    2.54 / 2,
                    y_pos,
                    angle,
                    str(pin_num + 1),
                    pin_type="passive",
                )

                # Toggle angle for next row
                angle = toggle_angle(angle)
        else:
            for pin_num in range(1, pin_count + 1):
                y_pos = start_y - (pin_num - 1) * pin_spacing
                write_pin(
                    symbol_file,
                    -5.08,
                    y_pos,
                    0,
                    str(pin_num),
                    pin_type="passive",
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
    *,
    symbol_file: TextIO,
    symbol_name: str,
    component_data: dict[str, str],
    number_of_rows: int,
    led_color: dict[str, int],
    specs_dict: dict,
) -> None:
    """Write the drawing for a tactile switch symbol with LED indicator v2.

    Creates KiCad symbol definition for TS28 series tactile switches that
    include integrated LED indicators. Uses alternative layout with
    modified positioning for different component geometry.

    Args:
        symbol_file: File object for writing the symbol file.
        symbol_name: Name identifier for the symbol.
        component_data: Dictionary containing component specifications.
        number_of_rows: Number of pin rows in the component layout.
        led_color: Dictionary with RGB color values for LED representation.
        specs_dict: Dictionary containing component specifications.

    """
    pin_count = int(component_data.get("Pin Count", "2"))
    pin_spacing = 5.08 * 2

    symbol_file.write(f'\t\t(symbol "{symbol_name}_0_0"\n')

    # Check for override pin specs
    override_pins = get_override_pins_specs(
        component_data.get("Series", ""),
        specs_dict,
    )

    if override_pins:
        for pin_num, x_pos, y_pos, angle in override_pins:
            write_pin(
                symbol_file, x_pos, y_pos, angle, pin_num, pin_type="passive"
            )
    else:
        start_y = (pin_count - 1) * pin_spacing / 2

        def toggle_angle(current):
            return 90 if current == 270 else 270

        if number_of_rows == 2:  # noqa: PLR2004
            angle = 270  # Start with 270
            for pin_num in range(1, pin_count * 2, 2):
                y_pos = start_y - (pin_num - 1) * pin_spacing / 2

                # Both pins in this row use the same angle
                write_pin(
                    symbol_file,
                    -2.54 / 2,
                    y_pos,
                    angle,
                    str(pin_num),
                    pin_type="passive",
                )
                write_pin(
                    symbol_file,
                    2.54 / 2,
                    y_pos,
                    angle,
                    str(pin_num + 1),
                    pin_type="passive",
                )

                # Toggle angle for next row
                angle = toggle_angle(angle)
        else:
            for pin_num in range(1, pin_count + 1):
                y_pos = start_y - (pin_num - 1) * pin_spacing
                write_pin(
                    symbol_file,
                    -5.08,
                    y_pos,
                    0,
                    str(pin_num),
                    pin_type="passive",
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
    specs_dict: dict,
) -> List[Tuple[str, float, float, int]]:
    """Retrieve override pin specifications for a given component series.

    Args:
        series: The series identifier for the tactile switch component.
        specs_dict: Dictionary containing SYMBOLS_SPECS.

    Returns:
        List of tuples containing pin specifications in format
        (pin_number, x_position, y_position, angle). Returns empty list
        if no override specifications are found.

    """
    specs = specs_dict.get(series)
    if (
        specs
        and hasattr(specs, "override_pins_specs")
        and specs.override_pins_specs
    ):
        return specs.override_pins_specs

    return []
