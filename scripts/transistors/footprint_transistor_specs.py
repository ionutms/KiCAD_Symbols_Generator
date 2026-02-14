"""Defines physical dimensions and pad properties for various diode packages.

This module defines a dictionary of FootprintSpecs objects, each of which
contains all the information needed to generate a complete KiCad footprint
file for a specific diode package. The dictionary keys are the package names
as they appear in the MPN field of the transistor symbol.

The FootprintSpecs object contains the following fields:

- body_dimensions:
    A BodyDimensions object with the width and height of the
    diode body outline in millimeters.
"""

from __future__ import annotations

from typing import NamedTuple


class BodyDimensions(NamedTuple):
    """Defines rectangular dimensions for diode body outlines.

    All measurements are in millimeters relative to the origin point (0,0).

    Attributes:
        width: The width of the diode body outline.
        height: The height of the diode body outline.

    """

    width: float
    height: float


class PadDimensions(NamedTuple):
    """Defines dimensions for asymmetric transistor pads.

    All measurements are in millimeters.

    Attributes:
        width: Width of the pad
        height: Height of the pad
        pad_center_x: X-coordinate of the pad center
        pad_pitch_y: Y-coordinate of the pad center

    """

    width: float
    height: float
    pad_center_x: float
    pad_pitch_y: float


class PadDimensionsAsymmetric(NamedTuple):
    """Defines pad dimensions and positions for diode footprints.

    All measurements are in millimeters relative to the origin point (0,0).

    Attributes:
        width: The width of the diode pad.
        height: The height of the diode pad.
        pad_center_x: The x-coordinate of the center of the first pad.
        pad_pitch_y: The distance between the centers of adjacent pads.
        pins_per_side: The number of pads on each side of the diode.
        thermal_width: The width of the thermal pad(s).
        thermal_height: The height of the thermal pad(s).
        thermal_pad_center_x:
            The x-coordinates of the centers of the thermal pads.
        thermal_pad_center_y:
            The y-coordinates of the centers of the thermal pads.
        thermal_pad_numbers: The pad numbers for the thermal pads.
        pad_numbers: The pad numbers for the regular pads.
        solid_pad_numbers:
            The pad numbers that should have solid connection to zones.


    """

    width: float
    height: float
    pad_center_x: float
    pad_pitch_y: float
    pins_per_side: float
    pad_numbers: list[int]
    thermal_width: list[float] | None = None
    thermal_height: list[float] | None = None
    thermal_pad_center_x: list[float] | None = None
    thermal_pad_center_y: list[float] | None = None
    thermal_pad_numbers: list[int] | None = None
    solid_pad_numbers: list[int] | None = None


class FootprintSpecs(NamedTuple):
    """Defines physical dimensions and pad properties for a diode package.

    Attributes:
        body_dimensions:
            A BodyDimensions object with the width and height of the diode
            body outline in millimeters.
        pad_dimensions:
            A PadDimensionsAsymmetric object with the pad dimensions and
            positions for the diode footprint.
        ref_offset_y: The y-coordinate of the reference designator text.

    """

    body_dimensions: BodyDimensions
    pad_dimensions: PadDimensionsAsymmetric
    ref_offset_y: float
    pin_count: int | None = None


FOOTPRINTS_SPECS: dict[str, FootprintSpecs] = {
    "PowerPAK 1212-8": FootprintSpecs(
        body_dimensions=BodyDimensions(width=4.0, height=3.9),
        pad_dimensions=PadDimensionsAsymmetric(
            width=0.99,
            height=0.405,
            pad_center_x=1.435,
            pad_pitch_y=0.66,
            pins_per_side=4,
            thermal_width=[1.725],
            thermal_height=[2.385],
            thermal_pad_center_x=[0.558],
            thermal_pad_center_y=[0],
            thermal_pad_numbers=[5],
            pad_numbers=[1, 2, 3, 4, 5, 5, 5, 5],
            solid_pad_numbers=[1, 2, 3, 5],
        ),
        ref_offset_y=-2.5,
    ),
    "LFPAK33-8": FootprintSpecs(
        body_dimensions=BodyDimensions(width=4.1, height=3.6),
        pad_dimensions=PadDimensionsAsymmetric(
            width=0.83,
            height=0.4,
            pad_center_x=1.535,
            pad_pitch_y=0.65,
            pins_per_side=4,
            thermal_width=[1.85],
            thermal_height=[2.35],
            thermal_pad_center_x=[0.405],
            thermal_pad_center_y=[0],
            thermal_pad_numbers=[5],
            pad_numbers=[1, 2, 3, 4, 5, 5, 5, 5],
            solid_pad_numbers=[5],
        ),
        ref_offset_y=-2.5,
    ),
    "LFPAK56D-8": FootprintSpecs(
        body_dimensions=BodyDimensions(width=7.3, height=5.85),
        pad_dimensions=PadDimensionsAsymmetric(
            width=1.15,
            height=0.7,
            pad_center_x=2.95,
            pad_pitch_y=1.27,
            pins_per_side=4,
            thermal_width=[4.4, 4.4],
            thermal_height=[1.97, 1.97],
            thermal_pad_center_x=[0.425, 0.425],
            thermal_pad_center_y=[1.27, -1.27],
            thermal_pad_numbers=[5, 6],
            pad_numbers=[1, 2, 3, 4, 5, 5, 6, 6],
        ),
        ref_offset_y=-3.6,
    ),
    "PowerPAK SO-8 Dual": FootprintSpecs(
        body_dimensions=BodyDimensions(width=7.0, height=5.0),
        pad_dimensions=PadDimensionsAsymmetric(
            width=1.27,
            height=0.66,
            pad_center_x=2.67,
            pad_pitch_y=1.27,
            pins_per_side=4,
            thermal_width=[3.81, 3.81],
            thermal_height=[1.93, 1.93],
            thermal_pad_center_x=[0.69, 0.69],
            thermal_pad_center_y=[1.27, -1.27],
            thermal_pad_numbers=[5, 6],
            pad_numbers=[1, 2, 3, 4, 5, 5, 6, 6],
        ),
        ref_offset_y=-3.2,
    ),
    "SOT-26": FootprintSpecs(
        body_dimensions=BodyDimensions(width=3.4, height=3.2),
        pad_dimensions=PadDimensionsAsymmetric(
            width=0.8,
            height=0.55,
            pad_center_x=1.2,
            pad_pitch_y=0.95,
            pins_per_side=3,
            pad_numbers=[1, 2, 3, 4, 5, 6],
        ),
        ref_offset_y=-3.2,
    ),
    "SOT-323": FootprintSpecs(
        pin_count=3,
        body_dimensions=BodyDimensions(width=2.2, height=2.9),
        pad_dimensions=PadDimensions(
            width=0.47,
            height=0.6,
            pad_center_x=1.3,
            pad_pitch_y=1.9,
        ),
        ref_offset_y=-2.286,
    ),
    "SO-8FL": FootprintSpecs(
        body_dimensions=BodyDimensions(width=7.0, height=5.2),
        pad_dimensions=PadDimensionsAsymmetric(
            width=1,
            height=0.75,
            pad_center_x=2.8,
            pad_pitch_y=1.27,
            pins_per_side=4,
            thermal_width=[4.53],
            thermal_height=[4.56],
            thermal_pad_center_x=[0.935],
            thermal_pad_center_y=[0],
            thermal_pad_numbers=[5],
            pad_numbers=[1, 2, 3, 4, 5, 5, 5, 5],
        ),
        ref_offset_y=-3.302,
    ),
    "SOT23-3": FootprintSpecs(
        pin_count=3,
        body_dimensions=BodyDimensions(width=3, height=3.2),
        pad_dimensions=PadDimensions(
            width=0.8,
            height=0.9,
            pad_center_x=1.9,
            pad_pitch_y=2,
        ),
        ref_offset_y=-2.286,
    ),
    "PowerPAK SO-8 Single": FootprintSpecs(
        body_dimensions=BodyDimensions(width=7.0, height=5.0),
        pad_dimensions=PadDimensionsAsymmetric(
            width=1.27,
            height=0.66,
            pad_center_x=2.67,
            pad_pitch_y=1.27,
            pins_per_side=4,
            thermal_width=[3.81],
            thermal_height=[4.47],
            thermal_pad_center_x=[0.69],
            thermal_pad_center_y=[0],
            thermal_pad_numbers=[5],
            pad_numbers=[1, 2, 3, 4, 5, 5, 5, 5],
        ),
        ref_offset_y=-3.2,
    ),
    "TDSON-8 FL": FootprintSpecs(
        body_dimensions=BodyDimensions(width=7.0, height=5.0),
        pad_dimensions=PadDimensionsAsymmetric(
            width=1.1,
            height=0.5,
            pad_center_x=2.775,
            pad_pitch_y=1.27,
            pins_per_side=4,
            thermal_width=[4.55, 1.1],
            thermal_height=[4.41, 3.04],
            thermal_pad_center_x=[1.05, -2.775],
            thermal_pad_center_y=[0, -0.635],
            thermal_pad_numbers=[5, 1],
            pad_numbers=[1, 2, 3, 4, 5, 5, 5, 5],
        ),
        ref_offset_y=-3.2,
    ),
    "TSDSON-8FL": FootprintSpecs(
        body_dimensions=BodyDimensions(width=4.2, height=3.4),
        pad_dimensions=PadDimensionsAsymmetric(
            width=0.9,
            height=0.34,
            pad_center_x=1.575 - 0.125,
            pad_pitch_y=0.65,
            pins_per_side=4,
            thermal_width=[2.36, 0.9],
            thermal_height=[2.29, 1.64],
            thermal_pad_center_x=[1.18 - 0.46, -2.775 + 1.325],
            thermal_pad_center_y=[0, -0.325],
            thermal_pad_numbers=[5, 1],
            pad_numbers=[1, 2, 3, 4, 5, 5, 5, 5],
            solid_pad_numbers=[1, 2, 3, 5],
        ),
        ref_offset_y=-3.2,
    ),
    "SOT23": FootprintSpecs(
        pin_count=3,
        body_dimensions=BodyDimensions(width=3, height=3.2),
        pad_dimensions=PadDimensions(
            width=0.8,
            height=0.9,
            pad_center_x=1.9,
            pad_pitch_y=2,
        ),
        ref_offset_y=-2.286,
    ),
    "PowerPAK SC-70": FootprintSpecs(
        body_dimensions=BodyDimensions(width=2.5, height=2.3),
        pad_dimensions=PadDimensionsAsymmetric(
            width=0.35,
            height=0.3,
            pad_center_x=0.925,
            pad_pitch_y=0.65,
            pins_per_side=3,
            thermal_width=[1.7, 0.87],
            thermal_height=[0.95, 0.235],
            thermal_pad_center_x=[0, 0],
            thermal_pad_center_y=[-0.325, 0.668],
            thermal_pad_numbers=[6, 7],
            pad_numbers=[1, 2, 3, 4, 5, 6],
            solid_pad_numbers=[1, 2, 4, 5, 6, 7],
        ),
        ref_offset_y=-2.032,
    ),
}
