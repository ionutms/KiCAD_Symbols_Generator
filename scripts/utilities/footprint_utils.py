"""Utility functions for generating KiCad PCB footprint components.

This module provides helper functions to generate various sections and
elements of KiCad footprints, including headers, 3D models, courtyards,
silkscreen lines, and component properties.
"""

from __future__ import annotations

from uuid import uuid4


def generate_header(model_name: str) -> str:
    """Generate the standard KiCad footprint header section.

    Args:
        model_name (str): Name of the footprint model.

    Returns:
        str: Formatted KiCad footprint header with version and generator
             information.

    """
    return f"""(footprint "{model_name}"
    (version 20240108)
    (generator "pcbnew")
    (generator_version "8.0")
    (layer "F.Cu")
    """


def associate_3d_model(
    file_path: str,
    file_name: str,
    hide: bool = False,  # noqa: FBT001, FBT002
) -> str:
    """Generate the 3D model section for a KiCad footprint.

    Args:
        file_path (str): Relative path to the 3D model file.
        file_name (str): Name of the 3D model file without extension.
        hide (bool): TODO

    Returns:
        str: Formatted KiCad 3D model association with default
             offset, scale, and rotation.

    """
    hide_option = "(hide yes)" if hide else ""

    return f"""
        (model "{file_path}/{file_name}.step"
            {hide_option}
            (offset (xyz 0 0 0))
            (scale (xyz 1 1 1))
            (rotate (xyz 0 0 0))
        )
        """


def generate_courtyard(width: float, height: float) -> str:
    """Generate KiCad courtyard outline for rectangular components.

    Creates a rectangular courtyard outline defining the minimum
    clearance zone around a component.

    Args:
        width (float): Component body width in millimeters.
        height (float): Component body height in millimeters.

    Returns:
        str: KiCad format courtyard outline specification.

    """
    half_width = width / 2
    half_height = height / 2

    return f"""
        (fp_rect
            (start -{half_width} -{half_height})
            (end {half_width} {half_height})
            (stroke (width 0.00635) (type solid))
            (fill none)
            (layer "F.CrtYd")
            (uuid "{uuid4()}")
        )
        """


def generate_chamfered_shape(
    width: float,
    height: float,
    layer: str,
    stroke_width: float = 0.00635,
) -> str:
    """Generate a chamfered shape for a KiCad footprint.

    Creates a chamfered shape to represent a component's physical body

    Args:
        width (float): Component body width in millimeters.
        height (float): Component body height in millimeters.
        layer (str): Layer to draw the chamfered shape on.
        stroke_width (float): Width of the stroke line.

    Returns:
        str: KiCad formatted chamfered shape definition.

    """
    half_width = width / 2
    half_height = height / 2

    return f"""
        (fp_poly
            (pts
                (xy -{width / 4} -{half_height})
                (xy -{half_width} -{height / 5})
                (xy -{half_width} {height / 5})
                (xy -{width / 4} {half_height})
                (xy {half_width} {half_height})
                (xy {half_width} -{half_height})
            )
            (stroke (width {stroke_width}) (type solid))
            (fill none)
            (layer "{layer}")
            (uuid "{uuid4()}"))
        """


def generate_courtyard_2(
    width_left: float,
    width_right: float,
    height_top: float,
    height_bottom: float,
) -> str:
    """Generate KiCad courtyard outline for rectangular components.

    Creates a rectangular courtyard outline defining the minimum
    clearance zone around a component.

    Args:
        width_left (float): Component body width in millimeters.
        width_right (float): Component body width in millimeters.
        height_top (float): Component body height in millimeters.
        height_bottom (float): Component body height in millimeters.

    Returns:
        str: KiCad format courtyard outline specification.

    """
    return f"""
        (fp_rect
            (start -{width_left} {height_bottom})
            (end {width_right} -{height_top})
            (stroke (width 0.00635) (type solid))
            (fill none)
            (layer "F.CrtYd")
            (uuid "{uuid4()}")
        )
        """


def generate_silkscreen_rectangle(
    width_left: float,
    width_right: float,
    height_top: float,
    height_bottom: float,
) -> str:
    """Generate KiCad courtyard outline for rectangular components.

    Creates a rectangular courtyard outline defining the minimum
    clearance zone around a component.

    Args:
        width_left (float): Component body width in millimeters.
        width_right (float): Component body width in millimeters.
        height_top (float): Component body height in millimeters.
        height_bottom (float): Component body height in millimeters.

    Returns:
        str: KiCad format courtyard outline specification.

    """
    return f"""
        (fp_rect
            (start -{width_left} {height_bottom})
            (end {width_right} -{height_top})
            (stroke (width 0.1524) (type solid))
            (fill none)
            (layer "F.SilkS")
            (uuid "{uuid4()}")
        )
        """


def generate_fabrication_rectangle(
    width_left: float,
    width_right: float,
    height_top: float,
    height_bottom: float,
) -> str:
    """Generate KiCad courtyard outline for rectangular components.

    Creates a rectangular courtyard outline defining the minimum
    clearance zone around a component.

    Args:
        width_left (float): Component body width in millimeters.
        width_right (float): Component body width in millimeters.
        height_top (float): Component body height in millimeters.
        height_bottom (float): Component body height in millimeters.

    Returns:
        str: KiCad format courtyard outline specification.

    """
    return f"""
        (fp_rect
            (start -{width_left} {height_bottom})
            (end {width_right} -{height_top})
            (stroke (width 0.1524) (type solid))
            (fill none)
            (layer "F.Fab")
            (uuid "{uuid4()}")
        )
        """


def generate_silkscreen_lines(
    height: float,
    center_x: float,
    pad_width: float,
) -> str:
    """Generate silkscreen reference lines for a component.

    Creates horizontal silkscreen lines to help with component
    orientation and placement.

    Args:
        height (float): Total height of the component.
        center_x (float): X-coordinate of the component center.
        pad_width (float): Width of the component's pad.

    Returns:
        str: KiCad formatted silkscreen line definitions.

    """
    half_height = height / 2
    silkscreen_x = center_x - pad_width / 2

    shapes: str = ""

    for symbol in ["-", ""]:
        shapes += f"""
            (fp_line
                (start {silkscreen_x} {symbol}{half_height})
                (end -{silkscreen_x} {symbol}{half_height})
                (stroke (width 0.1524) (type solid))
                (layer "F.SilkS")
                (uuid "{uuid4()}")
            )
            """
    return shapes


def generate_fab_rectangle(width: float, height: float) -> str:
    """Generate fabrication layer rectangular outline.

    Creates a rectangle defining the component's physical
    dimensions on the fabrication layer.

    Args:
        width (float): Width of the rectangle.
        height (float): Height of the rectangle.

    Returns:
        str: KiCad formatted fabrication layer rectangle.

    """
    half_width = width / 2
    half_height = height / 2

    return f"""
        (fp_rect
            (start -{half_width} -{half_height})
            (end {half_width} {half_height})
            (stroke (width 0.0254) (type default))
            (fill none)
            (layer "F.Fab")
            (uuid "{uuid4()}")
        )
        """


def generate_fab_diode(
    width: float,
    height: float,
    anode_center_x: float,
    cathode_center_x: float,
) -> str:
    """Generate fabrication layer polygon for diode representation.

    Creates a polygon on the fabrication layer depicting a diode's
    physical shape and orientation.

    Args:
        width (float): Total width of the diode.
        height (float): Total height of the diode.
        anode_center_x (float): X-coordinate of the anode center.
        cathode_center_x (float): X-coordinate of the cathode center.

    Returns:
        str: KiCad formatted fabrication layer diode polygon.

    """
    return f"""
        (fp_poly
            (pts
            (xy {width} 0)
            (xy {anode_center_x} 0)
            (xy {width} 0)
            (xy {width} {height / 2})
            (xy 0 0)
            (xy 0 {height / 2})
            (xy 0 0)
            (xy -{cathode_center_x} 0)
            (xy 0 0)
            (xy 0 -{height / 2})
            (xy 0 0)
            (xy {width} -{height / 2})
            )
            (stroke (width 0.1) (type solid))
            (fill solid)
            (layer "F.Fab")
            (uuid "{uuid4()}")
        )
        """


def generate_properties(
    ref_y: float,
    value: str,
    mpn_y: float | None = None,
) -> str:
    """Generate properties section for KiCad footprint.

    Creates text properties including reference, value, and
    footprint description with consistent formatting.

    Args:
        ref_y (float): Vertical offset for reference text.
        value (str): Component value/description.
        mpn_y (float): Vertical offset for reference text.

    Returns:
        str: KiCad formatted properties and text elements.

    """
    font_props = """
        (effects
            (font (size 0.762 0.762) (thickness 0.1524))
            (justify left)
        )
        """

    ref = -ref_y if mpn_y is None else mpn_y

    return f"""
        (property "Reference" "REF**"
            (at 0 {ref_y} 0)
            (unlocked yes)
            (layer "F.SilkS")
            (uuid "{uuid4()}")
            {font_props}
        )
        (property "Value" "{value}"
            (at 0 {ref} 0)
            (unlocked yes)
            (layer "F.Fab")
            (uuid "{uuid4()}")
            {font_props}
        )
        (property "Footprint" ""
            (at 0 0 0)
            (layer "F.Fab")
            (hide yes)
            (uuid "{uuid4()}")
            {font_props}
        )
        (fp_text user "${{REFERENCE}}"
            (at 0 {ref + 1.27} 0)
            (unlocked yes)
            (layer "F.Fab")
            (uuid "{uuid4()}")
            {font_props}
        )
        """


def generate_pin_1_indicator(  # noqa: PLR0913
    body_width: float,  # Width of the component body
    pins_per_side: float = 1,
    pitch_y: float = 0,
    layer: str = "F.SilkS",
    mirror_y_coordonate: bool = False,  # noqa: FBT001, FBT002
    mirror_x_coordonate: bool = False,  # noqa: FBT001, FBT002
    margin_offset: float = 0.6,  # Distance from body edge
) -> str:
    """Generate the pin 1 indicator for a component.

    Args:
        body_width: Width of the component body
        pins_per_side: Number of pins on each side
        pitch_y: Distance between adjacent pads
        layer: Layer to draw the pin 1 indicator on
        mirror_y_coordonate: Mirror the Y-coordinate of the pin 1 indicator
        mirror_x_coordonate: Mirror the X-coordinate of the pin 1 indicator
        margin_offset: Distance from body edge to place the indicator

    Returns:
        str: KiCad formatted pin 1 indicator

    """
    shapes = []

    total_height = pitch_y * (pins_per_side - 1)

    circle_x = (
        -(body_width / 2 + margin_offset)
        if not mirror_x_coordonate
        else (body_width / 2 + margin_offset)
    )

    circle_y = (
        -total_height / 2 if not mirror_y_coordonate else total_height / 2
    )

    radius = 0.3

    shapes.append(f"""
        (fp_circle
            (center {circle_x} {circle_y})
            (end {circle_x - radius} {circle_y})
            (stroke (width 0.1524) (type solid))
            (fill solid)
            (layer {layer})
            (uuid "{uuid4()}")
        )
        """)

    return "\n".join(shapes)


def calculate_pad_positions(
    pad_center_x: float,
    pad_pitch_y: float,
    pins_per_side: float,
) -> list[tuple[float, float]]:
    """Calculate the positions of the pads on the footprint.

    Args:
        pad_center_x: X-coordinate of the pad center
        pad_pitch_y: Distance between adjacent pads
        pins_per_side: Number of pins on each side

    Returns:
        List of pad positions as (x, y) tuples

    """
    total_height = pad_pitch_y * (pins_per_side - 1)

    positions = []

    # Left side pads (top to bottom)
    for pin_index in range(pins_per_side):
        y_pos = -total_height / 2 + pin_index * pad_pitch_y
        positions.append((-pad_center_x, y_pos))

    # Right side pads (bottom to top)
    for pin_index in range(pins_per_side):
        y_pos = total_height / 2 - pin_index * pad_pitch_y
        positions.append((pad_center_x, y_pos))

    return positions


def generate_pads(  # noqa: D417, PLR0913
    pad_width: float,
    pad_height: float,
    pad_center_x: float,
    pad_pitch_y: float = 0,
    pins_per_side: int = 1,
    pin_numbers: list = None,  # noqa: RUF013
    reverse_pin_numbering: bool = False,  # noqa: FBT001, FBT002
) -> str:
    """Generate the pads section of the footprint.

    Args:
        pad_width: Width of the pad
        pad_height: Height of the pad
        pad_center_x: X-coordinate of the pad center
        pad_pitch_y: Distance between adjacent pads
        pins_per_side: Number of pins on each side
        pin_numbers: List of custom pin numbers

    Returns:
        str: KiCad formatted pad definitions

    """
    pads = []
    pad_positions = calculate_pad_positions(
        pad_center_x,
        pad_pitch_y,
        pins_per_side,
    )

    # Determine pin numbering
    if pin_numbers is None:
        # Default: use sequential numbering from 1
        pin_numbers = list(range(1, len(pad_positions) + 1))
        if reverse_pin_numbering:
            pin_numbers = list(reversed(pin_numbers))

    # Validate that we have enough custom pin numbers
    if len(pin_numbers) != len(pad_positions):
        msg = (
            f"Number of pin numbers ({len(pin_numbers)}) "
            f"must match number of pad positions ({len(pad_positions)})"
        )
        raise ValueError(msg)

    for (x_pos, y_pos), pad_number in zip(pad_positions, pin_numbers):
        pads.append(f"""
            (pad "{pad_number}" smd roundrect
                (at {x_pos} {y_pos})
                (size {pad_width} {pad_height})
                (layers "F.Cu" "F.Paste" "F.Mask")
                (roundrect_rratio 0.25)
                (uuid "{uuid4()}")
            )
            """)

    return "\n".join(pads)


def generate_thermal_pad(
    pad_width: float,
    pad_heigh: float,
    pad_x: float,
    pad_y: list[float],
    thermal_pad_numbers: list[int],
) -> str:
    """Generate the thermal pads section of the footprint.

    Args:
        pad_width: Width of the thermal pad
        pad_heigh: Height of the thermal pad
        pad_x: X-coordinate of the thermal pad
        pad_y: List of Y-coordinates of the thermal pads
        thermal_pad_numbers: List of thermal pad numbers

    Returns:
        str: KiCad formatted thermal pad definitions

    """
    pads = [
        f"""
        (pad "{pad_number}" smd roundrect
            (at {pad_x} {pad_y[index]})
            (size {pad_width} {pad_heigh})
            (layers "F.Cu" "F.Paste" "F.Mask")
            (roundrect_rratio 0.05)
            (uuid "{uuid4()}")
        )
        """
        for index, pad_number in enumerate(thermal_pad_numbers)
    ]

    return "\n".join(pads)


def generate_thru_hole_pads(  # noqa: PLR0913
    pin_count: int,
    pad_pitch: float,
    pad_size: float,
    drill_size: float,
    start_pos: float,
    row_pitch: float,
    row_count: int,
) -> str:
    """Generate the pads section of the footprint.

    Args:
        pin_count: Number of pins in the connector
        pad_pitch: Distance between adjacent pins
        pad_size: Diameter of the pad
        drill_size: Diameter of the drill hole
        start_pos: X-coordinate of the first pad
        row_pitch: Pitch between connector rows
        row_count: Number of connector rows

    Returns:
        str: KiCad formatted pad definitions

    """
    xpos = [
        start_pos + (pin_num * pad_pitch)
        for pin_num in range(pin_count * row_count)
    ]

    final_xpos = xpos
    if row_count == 2:  # noqa: PLR2004
        # duplicate each position
        final_xpos = [x_position for x_position in xpos for _ in range(2)]

    pads = []
    for pin_index, pin_num in enumerate(range(pin_count * row_count)):
        ypos = (
            (-1 if pin_num % 2 == 0 else 1)
            * (row_pitch / 2)
            * (row_count - 1)
        )

        pad_type = "rect" if pin_num == 0 else "circle"
        pad = f"""
            (pad "{pin_num + 1}" thru_hole {pad_type}
                (at {final_xpos[pin_index]:.3f} {ypos:.3f})
                (size {pad_size} {pad_size})
                (drill {drill_size})
                (layers "*.Cu" "*.Mask")
                (remove_unused_layers no)
                (solder_mask_margin 0.102)
                (uuid "{uuid4()}")
            )
            """
        pads.append(pad)
    return "\n".join(pads)


def generate_surface_mount_pads(  # noqa: PLR0913
    pin_count: int,
    pad_pitch: float,
    pad_size: list[float],
    start_pos: float,
    row_pitch: float,
    row_count: int,
    mirror_x_pin_numbering: bool,  # noqa: FBT001
) -> str:
    """Generate the pads section of the footprint.

    Args:
        pin_count: Number of pins in the connector
        pad_pitch: Distance between adjacent pins
        pad_size: Diameter of the pad
        start_pos: X-coordinate of the first pad
        row_pitch: Pitch between connector rows
        row_count: Number of connector rows
        mirror_x_pin_numbering: change pin numbering direction

    Returns:
        str: KiCad formatted pad definitions

    """
    xpos = [
        start_pos + (pin_num * pad_pitch)
        for pin_num in range(pin_count * row_count)
    ]

    final_xpos = xpos
    if row_count == 2:  # noqa: PLR2004
        # duplicate each position
        final_xpos = [x_position for x_position in xpos for _ in range(2)]

    pads = []
    for pin_index, pin_num in enumerate(range(pin_count * row_count)):
        ypos = (
            (-1 if pin_num % 2 == 0 else 1)
            * (row_pitch / 2)
            * (row_count - 1)
        )
        ypos = ypos if not mirror_x_pin_numbering else -ypos

        pad = f"""
            (pad "{pin_num + 1}" smd roundrect
                (at {final_xpos[pin_index]:.3f} {ypos:.3f})
                (size {pad_size[0]} {pad_size[1]})
                (layers "F.Cu" "F.Paste")
                (roundrect_rratio 0.25)
                (uuid "{uuid4()}")
            )
            """
        pads.append(pad)
    return "\n".join(pads)


def generate_zig_zag_surface_mount_pads(  # noqa: PLR0913
    pin_count: int,
    pad_pitch: float,
    pad_size: list[float],
    start_pos: float,
    row_pitch: float,
    mirror_y_position: bool = False,  # noqa: FBT001, FBT002
) -> str:
    """Generate the pads section of the footprint.

    Args:
        pin_count: Number of pins in the connector
        pad_pitch: Distance between adjacent pins
        pad_size: Diameter of the pad
        start_pos: X-coordinate of the first pad
        row_pitch: Pitch between connector rows
        mirror_y_position: Mirror the Y-coordinate of the pads

    Returns:
        str: KiCad formatted pad definitions

    """
    xpos = [start_pos + (pin_num * pad_pitch) for pin_num in range(pin_count)]

    pads = []
    for pin_index, pin_num in enumerate(range(pin_count)):
        mirror_coefficient = -1 if mirror_y_position else 1
        ypos = (
            -1 * mirror_coefficient
            if pin_num % 2 == 0
            else 1 * mirror_coefficient
        ) * (row_pitch / 2)

        pad = f"""
            (pad "{pin_num + 1}" smd roundrect
                (at {xpos[pin_index]:.3f} {ypos:.3f})
                (size {pad_size[0]} {pad_size[1]})
                (layers "F.Cu" "F.Paste")
                (roundrect_rratio 0.25)
                (uuid "{uuid4()}")
            )
            """
        pads.append(pad)
    return "\n".join(pads)


def generate_non_plated_through_holes(  # noqa: PLR0913
    pin_count: int,
    pad_pitch: float,
    pad_size: float,
    drill_size: float,
    start_pos: float,
    row_pitch: float,
    row_count: int,
) -> str:
    """Generate the pads section of the footprint.

    Args:
        pin_count: Number of pins in the connector
        pad_pitch: Distance between adjacent pins
        pad_size: Diameter of the pad
        drill_size: Diameter of the drill hole
        start_pos: X-coordinate of the first pad
        row_pitch: Pitch between connector rows
        row_count: Number of connector rows

    Returns:
        str: KiCad formatted pad definitions

    """
    xpos = [
        start_pos + (pin_num * pad_pitch)
        for pin_num in range(pin_count * row_count)
    ]

    final_xpos = xpos
    if row_count == 2:  # noqa: PLR2004
        # duplicate each position
        final_xpos = [x_position for x_position in xpos for _ in range(2)]

    pads = []
    for pin_index, pin_num in enumerate(range(pin_count * row_count)):
        ypos = (
            (-1 if pin_num % 2 == 0 else 1)
            * (row_pitch / 2)
            * (row_count - 1)
        )
        if row_count == 1:
            ypos = row_pitch

        pad = f"""
            (pad None np_thru_hole circle
                (at {final_xpos[pin_index]:.3f} {ypos:.3f})
                (size {pad_size} {pad_size})
                (drill {drill_size})
                (layers "F&B.Cu" "*.Mask")
                (uuid "{uuid4()}")
            )
            """
        pads.append(pad)
    return "\n".join(pads)


def generate_non_plated_through_hole(
    mounting_holes_specs: list[float],
) -> str:
    """Generate the pads section of the footprint.

    Args:
        mounting_holes_specs: List of mounting hole specifications

    Returns:
        str: KiCad formatted pad definitions

    """
    pads = []

    x, y, diameter = mounting_holes_specs

    pad = f"""
        (pad None np_thru_hole circle
            (at {x} {y})
            (size {diameter} {diameter})
            (drill {diameter})
            (layers "F&B.Cu" "*.Mask")
            (uuid "{uuid4()}")
        )
        """
    pads.append(pad)
    return "\n".join(pads)


def generate_oval_plated_through_hole(
    mounting_holes_specs: list[float],
) -> str:
    """Generate the pads section of the footprint.

    Args:
        mounting_holes_specs: List of mounting hole specifications

    Returns:
        str: KiCad formatted pad definitions

    """
    pads = []

    x, y, pad_size_x, pad_size_y, dril_size_x, dril_size_y = (
        mounting_holes_specs
    )

    pad = f"""
        (pad "" thru_hole oval
            (at {x} {y})
            (size {pad_size_x} {pad_size_y})
            (drill oval {dril_size_x} {dril_size_y})
            (layers "F&B.Cu" "*.Mask")
            (uuid "{uuid4()}")
        )
        """
    pads.append(pad)
    return "\n".join(pads)


def calculate_dimensions(
    pin_count: int,
    pad_pitch: float,
    width_left: float,
    width_right: float,
) -> dict:
    """Calculate key dimensions for footprint generation.

    Determines total width, length, and starting positions based on the
    connector's pin count and physical specifications.

    Args:
        pin_count: Number of pins on the connector
        pad_pitch: Distance between adjacent pins
        width_left: Initial width of the connector body on the left side
        width_right: Initial width of the connector body on the right side

    Returns:
        Dictionary containing calculated dimensions and positions

    """
    extra_width_per_side = (pin_count - 2) * pad_pitch / 2
    total_length = (pin_count - 1) * pad_pitch
    start_position = -total_length / 2

    return {
        "width_left": width_left + extra_width_per_side,
        "width_right": width_right + extra_width_per_side,
        "total_length": total_length,
        "start_pos": start_position,
    }
