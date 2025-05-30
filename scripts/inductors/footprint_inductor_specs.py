"""Defines physical dimensions and pad properties for inductor footprints.

This module contains a dictionary of FootprintSpecs objects that define the
physical dimensions, pad properties, and reference designator positions for
various series of surface mount power inductors. These specs are used to
generate accurate KiCad footprint files for each inductor series.
"""

from typing import NamedTuple


class BodyDimensions(NamedTuple):
    """Defines rectangular dimensions for inductor body outlines.

    All measurements are in millimeters relative to the origin point (0,0).

    Attributes:
        width: Total width of inductor body
        height: Total height of inductor body

    """

    width: float  # Total width of inductor body
    height: float  # Total height of inductor body


class PadDimensions(NamedTuple):
    """Defines dimensions for inductor pads.

    All measurements are in millimeters.

    Attributes:
        width: Width of each pad
        height: Height of each pad
        center_x: Distance from origin to pad center on X axis

    """

    width: float  # Width of each pad
    height: float  # Height of each pad
    center_x: float  # Distance from origin to pad center on X axis


class FootprintSpecs(NamedTuple):
    """Complete specifications for generating an inductor footprint.

    Defines all physical dimensions, pad properties, and reference designator
    positions needed to generate a complete KiCad footprint file.

    Attributes:
        body_dimensions: BodyDimensions object with inductor body dimensions
        pad_dimensions: PadDimensions object with pad dimensions and positions
        ref_offset_y: Y offset for reference designator
        enable_pin_1_indicator: Flag to enable pin 1 indicator (default: True)

    """

    body_dimensions: BodyDimensions  # Basic rectangle dimensions
    pad_dimensions: PadDimensions  # Pad size and positioning
    ref_offset_y: float  # Y offset for reference designator
    enable_pin_1_indicator: bool = True  # Enable pin 1 indicator


FOOTPRINTS_SPECS: dict[str, FootprintSpecs] = {
    "XAL1010": FootprintSpecs(
        body_dimensions=BodyDimensions(width=10.922, height=12.192),
        pad_dimensions=PadDimensions(
            width=2.3876,
            height=8.9916,
            center_x=3.3274,
        ),
        ref_offset_y=-6.858,
    ),
    "XAL1030": FootprintSpecs(
        body_dimensions=BodyDimensions(width=10.922, height=12.192),
        pad_dimensions=PadDimensions(
            width=2.3876,
            height=8.9916,
            center_x=3.3274,
        ),
        ref_offset_y=-6.858,
    ),
    "XAL1060": FootprintSpecs(
        body_dimensions=BodyDimensions(width=10.922, height=12.192),
        pad_dimensions=PadDimensions(
            width=2.3876,
            height=8.9916,
            center_x=3.3274,
        ),
        ref_offset_y=-6.858,
    ),
    "XAL1080": FootprintSpecs(
        body_dimensions=BodyDimensions(width=10.922, height=12.192),
        pad_dimensions=PadDimensions(
            width=2.3876,
            height=8.9916,
            center_x=3.3274,
        ),
        ref_offset_y=-6.858,
    ),
    "XAL1350": FootprintSpecs(
        body_dimensions=BodyDimensions(width=13.716, height=14.732),
        pad_dimensions=PadDimensions(
            width=2.9718,
            height=11.9888,
            center_x=4.3053,
        ),
        ref_offset_y=-8.128,
    ),
    "XAL1510": FootprintSpecs(
        body_dimensions=BodyDimensions(width=15.748, height=16.764),
        pad_dimensions=PadDimensions(
            width=3.175,
            height=13.208,
            center_x=5.2959,
        ),
        ref_offset_y=-9.144,
    ),
    "XAL1513": FootprintSpecs(
        body_dimensions=BodyDimensions(width=15.748, height=16.764),
        pad_dimensions=PadDimensions(
            width=3.175,
            height=13.208,
            center_x=5.2959,
        ),
        ref_offset_y=-9.144,
    ),
    "XAL1580": FootprintSpecs(
        body_dimensions=BodyDimensions(width=15.748, height=16.764),
        pad_dimensions=PadDimensions(
            width=3.175,
            height=13.208,
            center_x=5.2959,
        ),
        ref_offset_y=-9.144,
    ),
    "XAL4020": FootprintSpecs(
        body_dimensions=BodyDimensions(width=4.4704, height=4.4704),
        pad_dimensions=PadDimensions(
            width=0.9652,
            height=3.4036,
            center_x=1.1811,
        ),
        ref_offset_y=-3.048,
    ),
    "XAL4030": FootprintSpecs(
        body_dimensions=BodyDimensions(width=4.4704, height=4.4704),
        pad_dimensions=PadDimensions(
            width=0.9652,
            height=3.4036,
            center_x=1.1811,
        ),
        ref_offset_y=-3.048,
    ),
    "XAL4040": FootprintSpecs(
        body_dimensions=BodyDimensions(width=4.4704, height=4.4704),
        pad_dimensions=PadDimensions(
            width=0.9652,
            height=3.4036,
            center_x=1.1811,
        ),
        ref_offset_y=-3.048,
    ),
    "XAL5020": FootprintSpecs(
        body_dimensions=BodyDimensions(width=5.6896, height=5.9436),
        pad_dimensions=PadDimensions(
            width=1.1684,
            height=4.699,
            center_x=1.651,
        ),
        ref_offset_y=-3.81,
    ),
    "XAL5030": FootprintSpecs(
        body_dimensions=BodyDimensions(width=5.6896, height=5.9436),
        pad_dimensions=PadDimensions(
            width=1.1684,
            height=4.699,
            center_x=1.651,
        ),
        ref_offset_y=-3.81,
    ),
    "XAL5050": FootprintSpecs(
        body_dimensions=BodyDimensions(width=5.6896, height=5.9436),
        pad_dimensions=PadDimensions(
            width=1.1684,
            height=4.699,
            center_x=1.651,
        ),
        ref_offset_y=-3.81,
    ),
    "XAL6020": FootprintSpecs(
        body_dimensions=BodyDimensions(width=6.858, height=7.112),
        pad_dimensions=PadDimensions(
            width=1.4224,
            height=5.4864,
            center_x=2.0193,
        ),
        ref_offset_y=-4.572,
    ),
    "XAL6030": FootprintSpecs(
        body_dimensions=BodyDimensions(width=6.858, height=7.112),
        pad_dimensions=PadDimensions(
            width=1.4224,
            height=5.4864,
            center_x=2.0193,
        ),
        ref_offset_y=-4.572,
    ),
    "XAL6060": FootprintSpecs(
        body_dimensions=BodyDimensions(width=6.858, height=7.112),
        pad_dimensions=PadDimensions(
            width=1.4224,
            height=5.4864,
            center_x=2.0193,
        ),
        ref_offset_y=-4.572,
    ),
    "XAL7020": FootprintSpecs(
        body_dimensions=BodyDimensions(width=8.382, height=8.382),
        pad_dimensions=PadDimensions(
            width=1.778,
            height=6.5024,
            center_x=2.3622,
        ),
        ref_offset_y=-5.08,
    ),
    "XAL7030": FootprintSpecs(
        body_dimensions=BodyDimensions(width=8.382, height=8.382),
        pad_dimensions=PadDimensions(
            width=1.778,
            height=6.5024,
            center_x=2.3622,
        ),
        ref_offset_y=-5.08,
    ),
    "XAL7050": FootprintSpecs(
        body_dimensions=BodyDimensions(width=8.382, height=8.382),
        pad_dimensions=PadDimensions(
            width=1.778,
            height=6.5024,
            center_x=2.3622,
        ),
        ref_offset_y=-5.08,
    ),
    "XAL7070": FootprintSpecs(
        body_dimensions=BodyDimensions(width=8.0264, height=8.382),
        pad_dimensions=PadDimensions(
            width=1.9304,
            height=6.5024,
            center_x=2.413,
        ),
        ref_offset_y=-5.08,
    ),
    "XAL8050": FootprintSpecs(
        body_dimensions=BodyDimensions(width=8.636, height=9.144),
        pad_dimensions=PadDimensions(
            width=1.778,
            height=7.0104,
            center_x=2.5781,
        ),
        ref_offset_y=-5.588,
    ),
    "XAL8080": FootprintSpecs(
        body_dimensions=BodyDimensions(width=8.636, height=9.144),
        pad_dimensions=PadDimensions(
            width=1.778,
            height=7.0104,
            center_x=2.5781,
        ),
        ref_offset_y=-5.588,
    ),
    "XFL2005": FootprintSpecs(
        body_dimensions=BodyDimensions(width=2.6924, height=2.3876),
        pad_dimensions=PadDimensions(
            width=1.0414,
            height=2.2098,
            center_x=0.7239,
        ),
        ref_offset_y=-2.032,
    ),
    "XFL2006": FootprintSpecs(
        body_dimensions=BodyDimensions(width=2.286, height=2.3876),
        pad_dimensions=PadDimensions(
            width=0.6096,
            height=1.8034,
            center_x=0.6731,
        ),
        ref_offset_y=-2.032,
    ),
    "XFL2010": FootprintSpecs(
        body_dimensions=BodyDimensions(width=2.286, height=2.3876),
        pad_dimensions=PadDimensions(
            width=0.6096,
            height=1.8034,
            center_x=0.6731,
        ),
        ref_offset_y=-2.032,
    ),
    "XFL3010": FootprintSpecs(
        body_dimensions=BodyDimensions(width=3.3528, height=3.3528),
        pad_dimensions=PadDimensions(
            width=0.9906,
            height=2.8956,
            center_x=1.016,
        ),
        ref_offset_y=-2.54,
    ),
    "XFL3012": FootprintSpecs(
        body_dimensions=BodyDimensions(width=3.3528, height=3.3528),
        pad_dimensions=PadDimensions(
            width=0.9906,
            height=2.8956,
            center_x=1.016,
        ),
        ref_offset_y=-2.54,
    ),
    "XFL4012": FootprintSpecs(
        body_dimensions=BodyDimensions(width=4.4704, height=4.4704),
        pad_dimensions=PadDimensions(
            width=0.9652,
            height=3.4036,
            center_x=1.1811,
        ),
        ref_offset_y=-3.048,
    ),
    "XFL4015": FootprintSpecs(
        body_dimensions=BodyDimensions(width=4.4704, height=4.4704),
        pad_dimensions=PadDimensions(
            width=0.9652,
            height=3.4036,
            center_x=1.1811,
        ),
        ref_offset_y=-3.048,
    ),
    "XFL4020": FootprintSpecs(
        body_dimensions=BodyDimensions(width=4.4704, height=4.4704),
        pad_dimensions=PadDimensions(
            width=0.9652,
            height=3.4036,
            center_x=1.1811,
        ),
        ref_offset_y=-3.048,
    ),
    "XFL4030": FootprintSpecs(
        body_dimensions=BodyDimensions(width=4.4704, height=4.4704),
        pad_dimensions=PadDimensions(
            width=0.9652,
            height=3.4036,
            center_x=1.1811,
        ),
        ref_offset_y=-3.048,
    ),
    "XFL5015": FootprintSpecs(
        body_dimensions=BodyDimensions(width=5.6896, height=5.9436),
        pad_dimensions=PadDimensions(
            width=1.1684,
            height=4.699,
            center_x=1.651,
        ),
        ref_offset_y=-3.81,
    ),
    "XFL5018": FootprintSpecs(
        body_dimensions=BodyDimensions(width=5.6896, height=5.9436),
        pad_dimensions=PadDimensions(
            width=1.1684,
            height=4.699,
            center_x=1.651,
        ),
        ref_offset_y=-3.81,
    ),
    "XFL5030": FootprintSpecs(
        body_dimensions=BodyDimensions(width=5.6896, height=5.9436),
        pad_dimensions=PadDimensions(
            width=1.1684,
            height=4.699,
            center_x=1.651,
        ),
        ref_offset_y=-3.81,
    ),
    "XFL6012": FootprintSpecs(
        body_dimensions=BodyDimensions(width=6.858, height=7.112),
        pad_dimensions=PadDimensions(
            width=1.4224,
            height=5.4864,
            center_x=2.0193,
        ),
        ref_offset_y=-4.572,
    ),
    "XFL6060": FootprintSpecs(
        body_dimensions=BodyDimensions(width=6.858, height=7.112),
        pad_dimensions=PadDimensions(
            width=1.4224,
            height=5.4864,
            center_x=2.0193,
        ),
        ref_offset_y=-4.572,
    ),
    "XFL7015": FootprintSpecs(
        body_dimensions=BodyDimensions(width=8.382, height=8.382),
        pad_dimensions=PadDimensions(
            width=1.778,
            height=6.223,
            center_x=2.286,
        ),
        ref_offset_y=-5.08,
    ),
    "742792731": FootprintSpecs(
        body_dimensions=BodyDimensions(width=1.7, height=1.0),
        pad_dimensions=PadDimensions(
            width=0.5,
            height=0.6,
            center_x=0.5,
        ),
        ref_offset_y=-1.27,
        enable_pin_1_indicator=False,
    ),
    "LCENA2016MKTR47M0NK": FootprintSpecs(
        body_dimensions=BodyDimensions(width=2.7, height=2.2),
        pad_dimensions=PadDimensions(
            width=0.8,
            height=1.8,
            center_x=0.8,
        ),
        ref_offset_y=-1.778,
    ),
    "DFE21CCN1R0MELL": FootprintSpecs(
        body_dimensions=BodyDimensions(width=2.7, height=1.8),
        pad_dimensions=PadDimensions(
            width=0.8,
            height=1.4,
            center_x=0.8,
        ),
        ref_offset_y=-1.778,
    ),
    "LQG15HS47NJ02D": FootprintSpecs(
        body_dimensions=BodyDimensions(width=1.86, height=0.94),
        pad_dimensions=PadDimensions(width=0.54, height=0.64, center_x=0.51),
        ref_offset_y=-1.27,
    ),
}
