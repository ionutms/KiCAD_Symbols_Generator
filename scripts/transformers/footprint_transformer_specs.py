"""Specifications module for transformer footprint generation in KiCAD.

This module defines the data structures and specifications needed to generate
transformer footprints in KiCAD format. It provides classes for defining body
dimensions, pad specifications, and complete footprint parameters.
Classes:
    BodyDimensions:
        Defines rectangular dimensions for transformer body outlines
    Pad: Defines properties for individual pads in a transformer footprint
    PadDimensions: Defines dimensions and positioning for transformer pads
    FootprintSpecs:
        Combines body and pad specs for complete footprint definition
Constants:
    FOOTPRINTS_SPECS:
        Dictionary mapping transformer models to their footprint
        specifications
"""

from typing import NamedTuple, Union


class BodyDimensions(NamedTuple):
    """Defines rectangular dimensions for transformer body outlines.

    All measurements are in millimeters relative to the origin point (0,0).

    Attributes:
        width: Total width of transformer body
        height: Total height of transformer body

    """

    width: float
    height: float


class Pad(NamedTuple):
    """Defines properties for individual pads in a transformer footprint.

    Attributes:
        name: Identifier for the pad (e.g., '1', '2', etc.)
        x: X coordinate of the pad center relative to the origin
        y: Y coordinate of the pad center relative to the origin
        pad_size: Diameter of the pad

    """

    name: str
    x: float
    y: float
    pad_size: float


class PadDimensions(NamedTuple):
    """Defines dimensions for transformer pads.

    All measurements are in millimeters.

    Attributes:
        width: Width of each pad
        height: Height of each pad
        center_x: Distance from origin to pad center on X axis
        pitch_y: Vertical distance between adjacent pads
        pin_count: Total number of pins (must be even)
        reverse_pin_numbering: Flag to reverse pin numbering

    """

    width: float
    height: float
    center_x: float
    pitch_y: float
    pin_count: int
    reverse_pin_numbering: bool = False


class FootprintSpecs(NamedTuple):
    """Complete specifications for generating a transformer footprint."""

    body_dimensions: BodyDimensions
    pad_dimensions: Union[PadDimensions, list[Pad]]
    ref_offset_y: float


FOOTPRINTS_SPECS: dict[str, FootprintSpecs] = {
    "ZA9384": FootprintSpecs(
        body_dimensions=BodyDimensions(width=18.5, height=15.5),
        pad_dimensions=PadDimensions(
            width=2.5,
            height=1.75,
            center_x=7.75,
            pitch_y=2.5,
            pin_count=10,
        ),
        ref_offset_y=-8.89,
    ),
    "ZA9644": FootprintSpecs(
        body_dimensions=BodyDimensions(width=10.5, height=10.5),
        pad_dimensions=PadDimensions(
            width=2.45,
            height=1.6,
            center_x=3.675,
            pitch_y=2.5,
            pin_count=8,
        ),
        ref_offset_y=-6.096,
    ),
    "750315836": FootprintSpecs(
        body_dimensions=BodyDimensions(width=18.8, height=13.46),
        pad_dimensions=PadDimensions(
            width=1.88,
            height=1.17,
            center_x=8.18,
            pitch_y=2.5,
            pin_count=10,
            reverse_pin_numbering=True,
        ),
        ref_offset_y=-7.62,
    ),
    "YA8779": FootprintSpecs(
        body_dimensions=BodyDimensions(width=10.5, height=10.2),
        pad_dimensions=PadDimensions(
            width=1.9,
            height=1.6,
            center_x=4.05,
            pitch_y=2.49,
            pin_count=8,
        ),
        ref_offset_y=-7.62,
    ),
    "YA8916": FootprintSpecs(
        body_dimensions=BodyDimensions(width=10.5, height=10.2),
        pad_dimensions=PadDimensions(
            width=1.9,
            height=1.6,
            center_x=4.05,
            pitch_y=2.49,
            pin_count=8,
        ),
        ref_offset_y=-7.62,
    ),
    "YA8864": FootprintSpecs(
        body_dimensions=BodyDimensions(width=10.5, height=10.2),
        pad_dimensions=PadDimensions(
            width=1.9,
            height=1.6,
            center_x=4.05,
            pitch_y=2.49,
            pin_count=8,
        ),
        ref_offset_y=-7.62,
    ),
    "PL160X9-102L": FootprintSpecs(
        body_dimensions=BodyDimensions(width=24, height=21.5),
        pad_dimensions=[
            Pad("1", -10.41, -7.875, 2.03),
            Pad("2", -10.41, -5.08, 2.03),
            Pad("3", -10.41, -2.285, 2.03),
            Pad("4", -10.41, 2.285, 2.03),
            Pad("5", -10.41, 5.08, 2.03),
            Pad("6", -10.41, 7.875, 2.03),
            Pad("7", 9.91, 3.175 * 2, 2.79),
            Pad("8", 9.91, 3.175, 2.79),
            Pad("9", 9.91, 0, 2.79),
            Pad("10", 9.91, -3.175, 2.79),
            Pad("11", 9.91, -3.175 * 2, 2.79),
        ],
        ref_offset_y=-11.684,
    ),
}
