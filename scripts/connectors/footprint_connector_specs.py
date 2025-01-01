"""Specifications for PCB terminal block connector footprints.

This module defines the physical dimensions and parameters needed to generate
KiCad footprints for various terminal block connectors.
It provides structured data types to represent connector specifications
and a dictionary of pre-defined specifications for common connector models.

The coordinate system uses millimeters with the origin (0,0) at the center
of the component. Positive coordinates extend right/up, negative coordinates
extend left/down.
"""

from typing import NamedTuple


class BodyDimensions(NamedTuple):
    """Defines rectangular dimensions for component footprint outlines.

    All measurements are in millimeters relative to the origin point (0,0).
    Positive values extend right/up, negative values extend left/down.
    """

    width_left: float  # Distance from origin to left edge
    width_right: float  # Distance from origin to right edge
    height_top: float  # Distance from origin to top edge
    height_bottom: float  # Distance from origin to bottom edge


class FootprintSpecs(NamedTuple):
    """Complete specifications for generating a connector footprint.

    Defines all physical dimensions, pad properties, reference designator
    positions, and 3D model alignment parameters needed to generate a complete
    KiCad footprint file.
    """

    pitch: float  # Additional width needed per pin
    body_dimensions: BodyDimensions  # Basic rectangle dimensions
    pad_size: float  # Diameter/size of through-hole pads
    drill_size: float  # Diameter of drill holes
    silk_margin: float  # Clearance for silkscreen outlines
    mask_margin: float  # Solder mask clearance around pads
    mpn_y: float  # Y position for manufacturer part number
    ref_y: float  # Y position for reference designator


CONNECTOR_SPECS: dict[str, FootprintSpecs] = {
    "TB004-508": FootprintSpecs(
        pitch=5.08,
        body_dimensions=BodyDimensions(
            width_left=5.8,
            width_right=5.2,
            height_top=5.2,
            height_bottom=5.2,
        ),
        pad_size=2.55,
        drill_size=1.7,
        silk_margin=0.1524,
        mask_margin=0.102,
        mpn_y=6.096,
        ref_y=-6.096,
    ),
    "TB006-508": FootprintSpecs(
        pitch=5.08,
        body_dimensions=BodyDimensions(
            width_left=5.8,
            width_right=5.2,
            height_top=4.2,
            height_bottom=4.2,
        ),
        pad_size=2.55,
        drill_size=1.7,
        silk_margin=0.1524,
        mask_margin=0.102,
        mpn_y=5.334,
        ref_y=-5.334,
    ),
    "TBP02R1-381": FootprintSpecs(
        pitch=3.81,
        body_dimensions=BodyDimensions(
            width_left=4.4,
            width_right=4.4,
            height_top=7.9,
            height_bottom=1.4,
        ),
        pad_size=2.1,
        drill_size=1.4,
        silk_margin=0.1524,
        mask_margin=0.102,
        mpn_y=-10.2,
        ref_y=2.4,
    ),
    "TBP02R2-381": FootprintSpecs(
        pitch=3.81,
        body_dimensions=BodyDimensions(
            width_left=4.445,
            width_right=4.445,
            height_top=4.445,
            height_bottom=3.2512,
        ),
        pad_size=2.1,
        drill_size=1.4,
        silk_margin=0.1524,
        mask_margin=0.102,
        mpn_y=-6.8,
        ref_y=4.2,
    ),
    "TBP04R1-500": FootprintSpecs(
        pitch=5.0,
        body_dimensions=BodyDimensions(
            width_left=5.2,
            width_right=5.2,
            height_top=2.2,
            height_bottom=9.9,
        ),
        pad_size=2.55,
        drill_size=1.7,
        silk_margin=0.1524,
        mask_margin=0.102,
        mpn_y=10.8,
        ref_y=-3.0,
    ),
    "TBP04R2-500": FootprintSpecs(
        pitch=5.0,
        body_dimensions=BodyDimensions(
            width_left=5.8,
            width_right=5.8,
            height_top=4.0,
            height_bottom=4.8,
        ),
        pad_size=2.55,
        drill_size=1.7,
        silk_margin=0.1524,
        mask_margin=0.102,
        mpn_y=-6.6,
        ref_y=5.8,
    ),
    "TBP04R3-500": FootprintSpecs(
        pitch=5.0,
        body_dimensions=BodyDimensions(
            width_left=5.2,
            width_right=5.2,
            height_top=4.0,
            height_bottom=4.8,
        ),
        pad_size=2.55,
        drill_size=1.7,
        silk_margin=0.1524,
        mask_margin=0.102,
        mpn_y=-6.6,
        ref_y=5.8,
    ),
    "TBP04R12-500": FootprintSpecs(
        pitch=5.0,
        body_dimensions=BodyDimensions(
            width_left=5.8,
            width_right=5.8,
            height_top=2.2,
            height_bottom=9.9,
        ),
        pad_size=2.55,
        drill_size=1.7,
        silk_margin=0.1524,
        mask_margin=0.102,
        mpn_y=10.8,
        ref_y=-3.0,
    ),
}
