"""Resistor footprint specifications using structured data types."""

from typing import NamedTuple


class BodyDimensions(NamedTuple):
    """Defines rectangular dimensions for component footprint body.

    All measurements are in millimeters.

    Attributes:
        width: Total width of the component body
        height: Total height of the component body

    """

    width: float
    height: float


class PadDimensions(NamedTuple):
    """Defines dimensions for component pads.

    All measurements are in millimeters.

    Attributes:
        width: Width of each pad
        height: Height of each pad
        center_x: Distance from origin to pad center

    """

    width: float
    height: float
    center_x: float


class FootprintSpecs(NamedTuple):
    """Complete specifications for generating a resistor footprint.

    Defines all physical dimensions, pad properties, and text positions
    needed to generate a complete KiCad footprint file.

    Attributes:
        body_dimensions: Dimensions of the component body
        pad_dimensions: Dimensions of the component pads
        ref_offset_y: Y offset for reference designator text

    """

    body_dimensions: BodyDimensions
    pad_dimensions: PadDimensions
    ref_offset_y: float


FOOTPRINTS_SPECS: dict[str, FootprintSpecs] = {
    "0402": FootprintSpecs(
        body_dimensions=BodyDimensions(width=1.86, height=0.94),
        pad_dimensions=PadDimensions(width=0.54, height=0.64, center_x=0.51),
        ref_offset_y=-1.27,
    ),
    "0402_RT": FootprintSpecs(
        body_dimensions=BodyDimensions(width=1.86, height=0.94),
        pad_dimensions=PadDimensions(width=0.54, height=0.64, center_x=0.51),
        ref_offset_y=-1.27,
    ),
    "0603": FootprintSpecs(
        body_dimensions=BodyDimensions(width=2.96, height=1.46),
        pad_dimensions=PadDimensions(width=0.8, height=0.95, center_x=0.825),
        ref_offset_y=-1.524,
    ),
    "0805": FootprintSpecs(
        body_dimensions=BodyDimensions(width=3.36, height=1.9),
        pad_dimensions=PadDimensions(width=1.025, height=1.4, center_x=0.912),
        ref_offset_y=-1.778,
    ),
    "0805_RT": FootprintSpecs(
        body_dimensions=BodyDimensions(width=3.36, height=1.9),
        pad_dimensions=PadDimensions(width=1.025, height=1.4, center_x=0.912),
        ref_offset_y=-1.778,
    ),
    "1206": FootprintSpecs(
        body_dimensions=BodyDimensions(width=4.56, height=2.24),
        pad_dimensions=PadDimensions(
            width=1.125, height=1.75, center_x=1.462
        ),
        ref_offset_y=-2.032,
    ),
    "1210": FootprintSpecs(
        body_dimensions=BodyDimensions(width=4.56, height=3.16),
        pad_dimensions=PadDimensions(
            width=1.125, height=2.65, center_x=1.462
        ),
        ref_offset_y=-2.286,
    ),
    "2010": FootprintSpecs(
        body_dimensions=BodyDimensions(width=6.36, height=3.16),
        pad_dimensions=PadDimensions(
            width=1.225, height=2.65, center_x=2.312
        ),
        ref_offset_y=-2.286,
    ),
    "2512": FootprintSpecs(
        body_dimensions=BodyDimensions(width=7.64, height=3.84),
        pad_dimensions=PadDimensions(
            width=1.225, height=3.35, center_x=2.962
        ),
        ref_offset_y=-2.794,
    ),
}
