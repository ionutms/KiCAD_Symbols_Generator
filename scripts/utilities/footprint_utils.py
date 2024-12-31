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


def associate_3d_model(file_path: str, file_name: str) -> str:
    """Generate the 3D model section for a KiCad footprint.

    Args:
        file_path (str): Relative path to the 3D model file.
        file_name (str): Name of the 3D model file without extension.

    Returns:
        str: Formatted KiCad 3D model association with default
             offset, scale, and rotation.

    """
    return f"""
        (model "${{KIPRJMOD}}/{file_path}/{file_name}.step"
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
            (start -{width_left} -{height_bottom})
            (end {width_right} {height_top})
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
            (start -{width_left} -{height_bottom})
            (end {width_right} {height_top})
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
            (start -{width_left} -{height_bottom})
            (end {width_right} {height_top})
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

    ref = ref_y if mpn_y is None else mpn_y

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


def generate_pin_1_indicator(
    pad_center_x: float,
    pad_width: float,
    pins_per_side: float = 1,
    pitch_y: float = 0,
) -> str:
    """Generate the shapes section of the footprint."""
    shapes = []

    # Pin 1 indicator position
    total_height = pitch_y * (pins_per_side - 1)
    circle_x = -(pad_center_x + pad_width)
    circle_y = -total_height / 2
    radius = pad_width / 4

    # Pin 1 indicator on silkscreen
    shapes.append(f"""
        (fp_circle
            (center {circle_x} {circle_y})
            (end {circle_x - radius} {circle_y})
            (stroke (width 0.1524) (type solid))
            (fill solid)
            (layer "F.SilkS")
            (uuid "{uuid4()}")
        )
        """)

    return "\n".join(shapes)


def calculate_pad_positions(
    pad_center_x: float,
    pad_pitch_y: float,
    pins_per_side: float,
) -> list[tuple[float, float]]:
    """Calculate positions for all pads based on pin count."""
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


def generate_pads(  # noqa: PLR0913
    pad_width: float,
    pad_height: float,
    pad_center_x: float,
    pad_pitch_y: float = 0,
    pins_per_side: float = 1,
    pin_numbers: list = None,  # noqa: RUF013
) -> str:
    """Generate the pads section of the footprint."""
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
    """Generate the pads section of the footprint."""
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
