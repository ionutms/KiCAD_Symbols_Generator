"""Specifications for tactile switches footprints.

This module defines the physical dimensions and parameters needed to generate
KiCad footprints for various tactile switches. It provides structured data
types to represent switch specifications and a dictionary of pre-defined
specifications for common switch models.

The coordinate system uses millimeters with the origin (0,0) at the center
of the component. Positive coordinates extend right/up, negative coordinates
extend left/down.
"""

from __future__ import annotations

from typing import NamedTuple, Optional


class NonPlatedRoundMountingHoles(NamedTuple):
    """Defines the position and size of non-plated round mounting holes.

    Attributes:
        footprint_specs:
            List of mounting hole specifications,
            where each spec is [x, y, diameter]:
                - x: X position relative to the component origin
                - y: Y position relative to the component origin
                - diameter: Diameter of the mounting hole
    """

    footprint_specs: list[list[float]]


class PlatedOvalMountingHoles(NamedTuple):
    """Defines the position and size of plated oval mounting holes.

    Attributes:
        footprint_specs:
            List of mounting hole specifications,
            where each spec is [x, y, pad_oval_size, drill_oval_size]:
                - x: X position relative to the component origin
                - y: Y position relative to the component origin
                - pad_oval_size: Size of the oval pad
                - drill_oval_size: Size of the oval drill hole
    """

    footprint_specs: list[list[float]]


class MountingPads(NamedTuple):
    """Defines mounting pad specifications for mechanical attachment.

    Attributes:
        dimensions:
            List of mounting pad specifications,
            where each spec is [x, y, width, height]:
                - x: X position relative to the component origin
                - y: Y position relative to the component origin
                - width: Width of the mounting pad
                - height: Height of the mounting pad
    """

    dimensions: list[list[float]]


class NonPlatedMountingHoles(NamedTuple):
    """Defines non-plated mounting holes for mechanical attachment.

    Attributes:
        dimensions:
            List of mounting hole specifications,
            where each spec is [x, y, diameter]:
                - x: X position relative to the component origin
                - y: Y position relative to the component origin
                - diameter: Diameter of the mounting hole
    """

    dimensions: list[list[float]]


class BodyDimensions(NamedTuple):
    """Defines rectangular dimensions for component footprint outlines.

    All measurements are in millimeters relative to the origin point (0,0).
    Positive values extend right/up, negative values extend left/down.

    Attributes:
        width_left: Distance from origin to left edge (negative value)
        width_right: Distance from origin to right edge (positive value)
        height_top: Distance from origin to top edge (positive value)
        height_bottom: Distance from origin to bottom edge (negative value)
    """

    width_left: float
    width_right: float
    height_top: float
    height_bottom: float


class InternalCourtyard(NamedTuple):
    """Defines the internal courtyard dimensions for a component footprint.

    The courtyard defines the minimum space required around the component
    to prevent interference with adjacent components.

    Attributes:
        width_left: Distance from origin to left courtyard edge
        width_right: Distance from origin to right courtyard edge
        height_top: Distance from origin to top courtyard edge
        height_bottom: Distance from origin to bottom courtyard edge
    """

    width_left: float
    width_right: float
    height_top: float
    height_bottom: float


class Pad(NamedTuple):
    """Defines properties for individual pads in a component footprint.

    Attributes:
        name: Identifier for the pad (e.g., '1', '2', 'A1', etc.)
        x: X coordinate of the pad center relative to the origin
        y: Y coordinate of the pad center relative to the origin
        pad_size: Diameter or size of the pad
        drill_size: Diameter of the drill hole for through-hole pads
    """

    name: str
    x: float
    y: float
    pad_size: float
    drill_size: float


class FootprintSpecs(NamedTuple):
    """Complete specifications for generating a tactile switch footprint.

    Defines all physical dimensions, pad properties, reference designator
    positions, and 3D model alignment parameters needed to generate a complete
    KiCad footprint file.

    Attributes:
        model_name: Name of the 3D model file (without extension)
        pad_pitch: Spacing between pads in the same row
        body_dimensions: Physical outline dimensions of the component
        pad_size: Diameter/size of through-hole pads (single value or list)
        mpn_y: Y position for manufacturer part number text
        ref_y: Y position for reference designator text
        drill_size: Diameter of drill holes for through-hole pads
        row_pitch: Spacing between rows of pads
        number_of_rows: Number of rows of pads
        non_plated_pad_size: Diameter of non-plated pads
        non_plated_drill_size: Diameter of non-plated drill holes
        non_plated_row_pitch: Spacing between rows of non-plated pads
        miror_zig_zag: Mirror the zig-zag pattern for pin numbering
        mirror_x_pin_numbering: Mirror pin numbering along X-axis
        non_plated_round_mounting_holes: Non-plated mounting holes
        plated_oval_mounting_holes: Plated oval mounting holes
        internal_courtyard: Internal courtyard dimensions
        mounting_pads: Mounting pad specifications
        non_plated_mounting_holes: Non-plated mounting hole specifications
        pad_properties: List of individual pad properties and positions
    """

    model_name: str
    pad_pitch: float
    body_dimensions: BodyDimensions
    pad_size: float | list[float]
    mpn_y: float
    ref_y: float
    drill_size: float | None = None
    row_pitch: float = 0
    number_of_rows: int = 1
    non_plated_pad_size: None | float = None
    non_plated_drill_size: None | float = None
    non_plated_row_pitch: float = 0
    miror_zig_zag: None | bool = None
    mirror_x_pin_numbering: bool = False
    non_plated_round_mounting_holes: None | NonPlatedRoundMountingHoles = None
    plated_oval_mounting_holes: None | PlatedOvalMountingHoles = None
    internal_courtyard: None | InternalCourtyard = None
    mounting_pads: None | MountingPads = None
    non_plated_mounting_holes: None | NonPlatedMountingHoles = None
    pad_properties: Optional[list[Pad]] = None


# Define the TS28 color variants
_TS28_COLORS = ["BL", "R", "G", "Y"]

# Define the TS29 color variants
_TS29_COLORS = ["R", "G", "BL", "WT", "Y"]

TACTILE_SWITCHES_SPECS: dict[str, FootprintSpecs] = {
    "TS21": FootprintSpecs(
        model_name="TS21",
        pad_pitch=2,
        row_pitch=3.25,
        number_of_rows=2,
        body_dimensions=BodyDimensions(
            width_left=2.1,
            width_right=2.1,
            height_top=2.5,
            height_bottom=2.5,
        ),
        pad_size=[0.6, 1.25],
        drill_size=0.787,
        mpn_y=3.556,
        ref_y=-3.556,
        mirror_x_pin_numbering=True,
        mounting_pads=[[-1.65, 0, 0.5, 1], [1.65, 0, 0.5, 1]],
    ),
    "TS24-BL": FootprintSpecs(
        model_name="TS24-BL",
        pad_pitch=4.5,
        row_pitch=8.4,
        number_of_rows=2,
        body_dimensions=BodyDimensions(
            width_left=3.2,
            width_right=3.2,
            height_top=5.3,
            height_bottom=5.3,
        ),
        pad_size=[1.4, 1.6],
        drill_size=0.787,
        mpn_y=6.096,
        ref_y=-6.096,
        mirror_x_pin_numbering=True,
    ),
    "TS24-CL": FootprintSpecs(
        model_name="TS24-CL",
        pad_pitch=4.5,
        row_pitch=8.4,
        number_of_rows=2,
        body_dimensions=BodyDimensions(
            width_left=3.2,
            width_right=3.2,
            height_top=5.3,
            height_bottom=5.3,
        ),
        pad_size=[1.4, 1.6],
        drill_size=0.787,
        mpn_y=6.096,
        ref_y=-6.096,
        mirror_x_pin_numbering=True,
    ),
    **{
        f"TS28-{color}": FootprintSpecs(
            model_name=f"TS28-{color}",
            pad_pitch=6.2,
            row_pitch=5,
            number_of_rows=2,
            body_dimensions=BodyDimensions(
                width_left=-2.2,
                width_right=1.2,
                height_top=4.6,
                height_bottom=4.6,
            ),
            pad_size=2.8,
            drill_size=1.4,
            mpn_y=5.588,
            ref_y=-5.588,
            mirror_x_pin_numbering=True,
            pad_properties=[
                Pad(name="1", x=2.54, y=2.25, pad_size=2, drill_size=1.2),
                Pad(name="2", x=-2.54, y=2.25, pad_size=2, drill_size=1.2),
                Pad(name="3", x=2.54, y=-2.25, pad_size=2, drill_size=1.2),
                Pad(name="4", x=-2.54, y=-2.25, pad_size=2, drill_size=1.2),
                Pad(name="5", x=0, y=3.15, pad_size=2, drill_size=1.2),
                Pad(name="6", x=0, y=-3.15, pad_size=2, drill_size=1.2),
                Pad(name="7", x=5.84, y=2.54, pad_size=2, drill_size=1.2),
                Pad(name="8", x=5.84, y=-2.54, pad_size=2, drill_size=1.2),
            ],
        )
        for color in _TS28_COLORS
    },
    **{
        f"TS29-{color}": FootprintSpecs(
            model_name=f"TS29-{color}",
            pad_pitch=6.2,
            row_pitch=5,
            number_of_rows=2,
            body_dimensions=BodyDimensions(
                width_left=5,
                width_right=5,
                height_top=8.2,
                height_bottom=8.2,
            ),
            pad_size=2.8,
            drill_size=1.4,
            mpn_y=9.144,
            ref_y=-9.144,
            mirror_x_pin_numbering=True,
            non_plated_mounting_holes=[[0, 4.4, 1.8], [0, -4.4, 1.8]],
            pad_properties=[
                Pad(name="1", x=6.2, y=2.5, pad_size=2.4, drill_size=1.4),
                Pad(name="2", x=-6.2, y=2.5, pad_size=2.4, drill_size=1.4),
                Pad(name="3", x=6.2, y=-2.5, pad_size=2.4, drill_size=1.4),
                Pad(name="4", x=-6.2, y=-2.5, pad_size=2.4, drill_size=1.4),
                Pad(name="5", x=0, y=6.6, pad_size=2.3, drill_size=1.3),
                Pad(name="6", x=0, y=-6.6, pad_size=2.3, drill_size=1.3),
            ],
        )
        for color in _TS29_COLORS
    },
}
