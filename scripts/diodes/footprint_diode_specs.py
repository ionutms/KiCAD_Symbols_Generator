"""Specifications for diode footprint generation."""

from __future__ import annotations

from typing import NamedTuple


class BodyDimensions(NamedTuple):
    """Defines rectangular dimensions for diode body outlines.

    All measurements are in millimeters relative to the origin point (0,0).
    A diode body is defined by its width and height.

    Attributes:
        width: Width of the diode body
        height: Height of the diode body

    """

    width: float
    height: float


class PadDimensionsAsymmetric(NamedTuple):
    """Defines dimensions for asymmetric diode pads.

    All measurements are in millimeters. For PowerDI-123 package,
    cathode_pad is pad 1, anode_pad is pad 2.

    Attributes:
        cathode_width: Width of the cathode pad
        cathode_height: Height of the cathode pad
        cathode_center_x: X-coordinate of the cathode pad center
        anode_width: Width of the anode pad
        anode_height: Height of the anode pad
        anode_center_x: X-coordinate of the anode pad center
        roundrect_ratio: Roundness ratio of the pad corners (default 0.25)

    """

    cathode_width: float
    cathode_height: float
    cathode_center_x: float
    anode_width: float
    anode_height: float
    anode_center_x: float
    roundrect_ratio: float = 0.25


class PadDimensions(NamedTuple):
    """Defines dimensions for asymmetric diode pads.

    All measurements are in millimeters. For PowerDI-123 package,
    cathode_pad is pad 1, anode_pad is pad 2.

    Attributes:
        width: Width of the pad
        height: Height of the pad
        center_x: X-coordinate of the pad center
        center_y: Y-coordinate of the pad center
        roundrect_ratio: Roundness ratio of the pad corners (default 0.25)

    """

    width: float
    height: float
    center_x: float
    center_y: float
    roundrect_ratio: float = 0.25


class FootprintSpecs(NamedTuple):
    """Complete specifications for generating a diode footprint.

    Defines all physical dimensions, pad properties, and reference designator
    positions needed to generate a complete KiCad footprint file.

    Attributes:
        body_dimensions: BodyDimensions for the diode body
        pad_dimensions: PadDimensionsAsymmetric for the diode pads
        ref_offset_y: Y-coordinate offset for the reference designator
        pin_count: Number of pins on the diode (default None)

    """

    body_dimensions: BodyDimensions
    pad_dimensions: PadDimensionsAsymmetric | PadDimensions
    ref_offset_y: float
    pin_count: int | None = None


FOOTPRINTS_SPECS: dict[str, FootprintSpecs] = {
    "PowerDI_123": FootprintSpecs(
        body_dimensions=BodyDimensions(width=5.0, height=2.6),
        pad_dimensions=PadDimensionsAsymmetric(
            cathode_width=2.4,
            cathode_height=1.5,
            cathode_center_x=0.85,
            anode_width=1.05,
            anode_height=1.5,
            anode_center_x=1.525,
        ),
        ref_offset_y=-2.5,
    ),
    "SOD_123": FootprintSpecs(
        body_dimensions=BodyDimensions(width=4.8, height=2.0),
        pad_dimensions=PadDimensionsAsymmetric(
            cathode_width=0.91,
            cathode_height=1.22,
            cathode_center_x=1.635,
            anode_width=0.91,
            anode_height=1.22,
            anode_center_x=1.635,
        ),
        ref_offset_y=-1.778,
    ),
    "SOD_523": FootprintSpecs(
        body_dimensions=BodyDimensions(width=2.2, height=1),
        pad_dimensions=PadDimensionsAsymmetric(
            cathode_width=0.65,
            cathode_height=0.3,
            cathode_center_x=0.675,
            anode_width=0.65,
            anode_height=0.3,
            anode_center_x=0.675,
        ),
        ref_offset_y=-1.27,
    ),
    "SOD_123F": FootprintSpecs(
        body_dimensions=BodyDimensions(width=4.6, height=2.2),
        pad_dimensions=PadDimensionsAsymmetric(
            cathode_width=1.34,
            cathode_height=1.8,
            cathode_center_x=1.43,
            anode_width=1.34,
            anode_height=1.8,
            anode_center_x=1.43,
        ),
        ref_offset_y=-1.778,
    ),
    "LED_RED_0402_1005Metric": FootprintSpecs(
        body_dimensions=BodyDimensions(width=2, height=0.9),
        pad_dimensions=PadDimensionsAsymmetric(
            cathode_width=0.7,
            cathode_height=0.5,
            cathode_center_x=0.45,
            anode_width=0.7,
            anode_height=0.5,
            anode_center_x=0.45,
        ),
        ref_offset_y=-1.27,
    ),
    "LED_GREEN_0402_1005Metric": FootprintSpecs(
        body_dimensions=BodyDimensions(width=2, height=0.9),
        pad_dimensions=PadDimensionsAsymmetric(
            cathode_width=0.7,
            cathode_height=0.5,
            cathode_center_x=0.45,
            anode_width=0.7,
            anode_height=0.5,
            anode_center_x=0.45,
        ),
        ref_offset_y=-1.27,
    ),
    "SC_70": FootprintSpecs(
        pin_count=3,
        body_dimensions=BodyDimensions(width=2.6, height=3.4),
        pad_dimensions=PadDimensions(
            width=0.7,
            height=0.9,
            center_x=1.3,
            center_y=1.9,
        ),
        ref_offset_y=-2.54,
    ),
    "SOT-323": FootprintSpecs(
        pin_count=3,
        body_dimensions=BodyDimensions(width=2.6, height=3.4),
        pad_dimensions=PadDimensions(
            width=0.5,
            height=0.95,
            center_x=1.3,
            center_y=1.95,
        ),
        ref_offset_y=-2.54,
    ),
    "SOD123W": FootprintSpecs(
        body_dimensions=BodyDimensions(width=4.4, height=2.1),
        pad_dimensions=PadDimensionsAsymmetric(
            cathode_width=1.1,
            cathode_height=1.1,
            cathode_center_x=1.4,
            anode_width=1.1,
            anode_height=1.1,
            anode_center_x=1.4,
        ),
        ref_offset_y=-1.778,
    ),
    "SOD128": FootprintSpecs(
        body_dimensions=BodyDimensions(width=6.2, height=3.4),
        pad_dimensions=PadDimensionsAsymmetric(
            cathode_width=1.2,
            cathode_height=1.9,
            cathode_center_x=2.2,
            anode_width=1.2,
            anode_height=1.9,
            anode_center_x=2.2,
        ),
        ref_offset_y=-2.54,
    ),
    "DO-214AA": FootprintSpecs(
        body_dimensions=BodyDimensions(width=7.75, height=4),
        pad_dimensions=PadDimensionsAsymmetric(
            cathode_width=2.16,
            cathode_height=2.26,
            cathode_center_x=2.45,
            anode_width=2.16,
            anode_height=2.26,
            anode_center_x=2.45,
        ),
        ref_offset_y=-2.794,
    ),
    "SOD323": FootprintSpecs(
        body_dimensions=BodyDimensions(width=3, height=1.5),
        pad_dimensions=PadDimensionsAsymmetric(
            cathode_width=0.49,
            cathode_height=0.45,
            cathode_center_x=1.14,
            anode_width=0.49,
            anode_height=0.45,
            anode_center_x=1.14,
        ),
        ref_offset_y=-1.524,
    ),
    "DO-214AB-2": FootprintSpecs(
        body_dimensions=BodyDimensions(width=8.6, height=6.2),
        pad_dimensions=PadDimensionsAsymmetric(
            cathode_width=1.54,
            cathode_height=3.14,
            cathode_center_x=3.325,
            anode_width=1.54,
            anode_height=3.14,
            anode_center_x=3.325,
        ),
        ref_offset_y=-4.064,
    ),
    "SOD_923": FootprintSpecs(
        body_dimensions=BodyDimensions(width=1.3, height=0.8),
        pad_dimensions=PadDimensionsAsymmetric(
            cathode_width=0.36,
            cathode_height=0.25,
            cathode_center_x=0.42,
            anode_width=0.36,
            anode_height=0.25,
            anode_center_x=0.42,
        ),
        ref_offset_y=-1.016,
    ),
    "DO-219AD": FootprintSpecs(
        body_dimensions=BodyDimensions(width=3.8, height=1.7),
        pad_dimensions=PadDimensionsAsymmetric(
            cathode_width=2,
            cathode_height=1.1,
            cathode_center_x=0.65,
            anode_width=0.8,
            anode_height=0.8,
            anode_center_x=1.25,
        ),
        ref_offset_y=-1.524,
    ),
    "SMA": FootprintSpecs(
        body_dimensions=BodyDimensions(width=7, height=2.9),
        pad_dimensions=PadDimensionsAsymmetric(
            cathode_width=2.5,
            cathode_height=1.7,
            cathode_center_x=2,
            anode_width=2.5,
            anode_height=1.7,
            anode_center_x=2,
        ),
        ref_offset_y=-2.286,
    ),
}
