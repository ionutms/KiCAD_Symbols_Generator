"""Specifications for tactile switches footprints.

This module defines the physical dimensions and parameters needed to generate
KiCad footprints for various terminal block tactile switches.
It provides structured data types to represent connector specifications
and a dictionary of pre-defined specifications for common connector models.

The coordinate system uses millimeters with the origin (0,0) at the center
of the component. Positive coordinates extend right/up, negative coordinates
extend left/down.
"""

from __future__ import annotations

from typing import NamedTuple


class NonPlatedRoundMountingHoles(NamedTuple):
    """Defines the position and size of mounting holes for a connector.

    Attributes:
        footprint_specs:
            List of mounting hole specifications,
            where each spec is [x, y, diameter]:
                - x: X position relative to the connector origin
                - y: Y position relative to the connector origin
                - diameter: Diameter of the mounting hole
    """

    footprint_specs: list[list[float]]


class PlatedOvalMountingHoles(NamedTuple):
    """Defines the position and size of mounting holes for a connector.

    Attributes:
        footprint_specs:
            List of mounting hole specifications,
            where each spec is [x, y, diameter]:
                - x: X position relative to the connector origin
                - y: Y position relative to the connector origin
                - pad_oval_size: Size of the oval pad
                - drill_oval_size: Size of the oval drill hole
    """

    footprint_specs: list[list[float]]


class MountingPads(NamedTuple):
    """TODO"""

    dimensions: list[list[float]]


class NonPlatedMountingHoles(NamedTuple):
    """TODO"""

    dimensions: list[list[float]]


class BodyDimensions(NamedTuple):
    """Defines rectangular dimensions for component footprint outlines.

    All measurements are in millimeters relative to the origin point (0,0).
    Positive values extend right/up, negative values extend left/down.

    Attributes:
        width_left: Distance from origin to left edge
        width_right: Distance from origin to right edge
        height_top: Distance from origin to top edge
        height_bottom: Distance from origin to bottom edge
    """

    width_left: float
    width_right: float
    height_top: float
    height_bottom: float


class InternalCourtyard(NamedTuple):
    """Defines the internal courtyard dimensions for a connector footprint.

    Attributes:
        width_left: Distance from origin to left edge
        width_right: Distance from origin to right edge
        height_top: Distance from origin to top edge
        height_bottom: Distance from origin to bottom edge
    """

    width_left: float
    width_right: float
    height_top: float
    height_bottom: float


class FootprintSpecs(NamedTuple):
    """Complete specifications for generating a connector footprint.

    Defines all physical dimensions, pad properties, reference designator
    positions, and 3D model alignment parameters needed to generate a complete
    KiCad footprint file.

    Attributes:
        model_name: Name of the 3D model file (without extension)
        pad_pitch: Additional width needed per pin
        body_dimensions: Basic rectangle dimensions
        pad_size: Diameter/size of through-hole pads
        mpn_y: Y position for manufacturer part number
        ref_y: Y position for reference designator
        drill_size: Diameter of drill holes
        row_pitch: Additional height needed per row
        number_of_rows: Number of rows of pins
        non_plated_pad_size: Diameter of non-plated pads
        non_plated_drill_size: Diameter of non-plated drill holes
        non_plated_row_pitch: Additional height per row of non-plated pads
        miror_zig_zag: Mirror the zig-zag pattern
        mirror_x_pin_numbering: Mirror pin numbering along X-axis
        non_plated_round_mounting_holes: Non-plated mounting holes
        plated_oval_mounting_holes: Plated oval mounting holes
        internal_courtyard: Internal courtyard dimensions
        mounting_pads: TODO
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


CONNECTOR_SPECS: dict[str, FootprintSpecs] = {
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
    "TS29-R": FootprintSpecs(
        model_name="TS29-R",
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
    ),
}
