"""Specifications for transformer footprint generation."""

from typing import NamedTuple


class BodyDimensions(NamedTuple):
    """Defines rectangular dimensions for transformer body outlines.

    All measurements are in millimeters relative to the origin point (0,0).

    """

    width: float   # Total width of transformer body
    height: float  # Total height of transformer body


class PadDimensions(NamedTuple):
    """Defines dimensions for transformer pads.

    All measurements are in millimeters.

    """

    width: float        # Width of each pad
    height: float       # Height of each pad
    center_x: float     # Distance from origin to pad center on X axis
    pitch_y: float      # Vertical distance between adjacent pads
    pin_count: int      # Total number of pins (must be even)


class FootprintSpecs(NamedTuple):
    """Complete specifications for generating a transformer footprint."""

    body_dimensions: BodyDimensions  # Basic rectangle dimensions
    pad_dimensions: PadDimensions   # Pad size and positioning
    ref_offset_y: float            # Y offset for reference designator


FOOTPRINTS_SPECS: dict[str, FootprintSpecs] = {
    "ZA9384": FootprintSpecs(
        body_dimensions=BodyDimensions(width=18.5, height=15.5),
        pad_dimensions=PadDimensions(
            width=2.5, height=1.75, center_x=7.75, pitch_y=2.5, pin_count=10),
        ref_offset_y=-8.89),
    "ZA9644": FootprintSpecs(
        body_dimensions=BodyDimensions(width=10.5, height=10.5),
        pad_dimensions=PadDimensions(
            width=2.45, height=1.6, center_x=3.675, pitch_y=2.5, pin_count=8),
        ref_offset_y=-6.096),
    "750315836": FootprintSpecs(
        body_dimensions=BodyDimensions(width=18.8, height=13.46),
        pad_dimensions=PadDimensions(
            width=1.88, height=1.17,
            center_x=8.18, pitch_y=2.5, pin_count=10),
        ref_offset_y=-7.62),
    "YA8779": FootprintSpecs(
        body_dimensions=BodyDimensions(width=10.5, height=10.2),
        pad_dimensions=PadDimensions(
            width=1.9, height=1.6,
            center_x=4.05, pitch_y=2.49, pin_count=8),
        ref_offset_y=-7.62),
}
