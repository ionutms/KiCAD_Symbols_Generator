"""Capacitor footprint specifications using structured data types.

This module defines named tuples for specifying physical dimensions of
capacitor footprints. Each named tuple represents a different capacitor
footprint size, with specific dimensions for the body and pads.

The FOOTPRINTS_SPECS dictionary maps capacitor sizes to their respective
footprint specifications. Each entry contains a FootprintSpecs named tuple
with all necessary dimensions and offsets for generating a KiCad footprint.

"""

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


class RadialBodyDimensions(NamedTuple):
    """Defines circular dimensions for radial component footprint body.

    All measurements are in millimeters.

    Attributes:
        diameter: Total diameter of the component body

    """

    diameter: float


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


class AdditionalPad(NamedTuple):
    """Defines dimensions and position for additional pads.

    All measurements are in millimeters.

    Attributes:
        x: X coordinate of the pad center
        y: Y coordinate of the pad center
        pad_diameter: Diameter of the pad
        drill_size: Size of drill hole for through hole
        name: Pad name/number

    """

    x: float
    y: float
    pad_diameter: float
    drill_size: float
    name: str = "3"


class RadialPadDimensions(NamedTuple):
    """Defines dimensions for radial component pads.

    All measurements are in millimeters.

    Attributes:
        pad_diameter: Diameter of each pad
        drill_size: Size of drill hole for through hole
        pad_distance: Distance from center to pad center
        pad_width: Width of the pad (for oval pads)
        pad_height: Height of the pad (for oval pads)
        additional_pads: List of additional pads

    """

    pad_diameter: float
    drill_size: float
    pad_distance: float
    pad_width: float = 0.0
    pad_height: float = 0.0
    additional_pads: list[AdditionalPad] | None = None


class FootprintSpecs(NamedTuple):
    """Complete specifications for generating a capacitor footprint.

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


class RadialFootprintSpecs(NamedTuple):
    """Complete specifications for generating a radial capacitor footprint.

    Defines all physical dimensions, pad properties, and text positions
    needed to generate a complete KiCad footprint file for radial components.

    Attributes:
        body_dimensions: Dimensions of the component body (circular)
        pad_dimensions: Dimensions of the component pads (through hole)
        ref_offset_y: Y offset for reference designator text
        is_radial: Flag indicating this is a radial component

    """

    body_dimensions: RadialBodyDimensions
    pad_dimensions: RadialPadDimensions
    ref_offset_y: float
    is_radial: bool = True


FOOTPRINTS_SPECS: dict[str, FootprintSpecs | RadialFootprintSpecs] = {
    "0402": FootprintSpecs(
        body_dimensions=BodyDimensions(width=1.82, height=0.92),
        pad_dimensions=PadDimensions(width=0.56, height=0.62, center_x=0.48),
        ref_offset_y=-1.27,
    ),
    "0603": FootprintSpecs(
        body_dimensions=BodyDimensions(width=2.96, height=1.46),
        pad_dimensions=PadDimensions(width=0.9, height=0.95, center_x=0.775),
        ref_offset_y=-1.524,
    ),
    "0805": FootprintSpecs(
        body_dimensions=BodyDimensions(width=3.4, height=1.96),
        pad_dimensions=PadDimensions(width=1.0, height=1.45, center_x=0.95),
        ref_offset_y=-1.778,
    ),
    "0805_060": FootprintSpecs(
        body_dimensions=BodyDimensions(width=3.4, height=1.96),
        pad_dimensions=PadDimensions(width=1.0, height=1.45, center_x=0.95),
        ref_offset_y=-1.778,
    ),
    "0805_125": FootprintSpecs(
        body_dimensions=BodyDimensions(width=3.4, height=1.96),
        pad_dimensions=PadDimensions(width=1.0, height=1.45, center_x=0.95),
        ref_offset_y=-1.778,
    ),
    "1206": FootprintSpecs(
        body_dimensions=BodyDimensions(width=4.6, height=2.3),
        pad_dimensions=PadDimensions(width=1.15, height=1.8, center_x=1.475),
        ref_offset_y=-2.032,
    ),
    "1210": FootprintSpecs(
        body_dimensions=BodyDimensions(width=4.6, height=3.2),
        pad_dimensions=PadDimensions(width=1.15, height=2.7, center_x=1.475),
        ref_offset_y=-2.286,
    ),
    "1210_140": FootprintSpecs(
        body_dimensions=BodyDimensions(width=4.6, height=3.2),
        pad_dimensions=PadDimensions(width=1.15, height=2.7, center_x=1.475),
        ref_offset_y=-2.286,
    ),
    "1210_200": FootprintSpecs(
        body_dimensions=BodyDimensions(width=4.6, height=3.2),
        pad_dimensions=PadDimensions(width=1.15, height=2.7, center_x=1.475),
        ref_offset_y=-2.286,
    ),
    "1210_250": FootprintSpecs(
        body_dimensions=BodyDimensions(width=4.6, height=3.2),
        pad_dimensions=PadDimensions(width=1.15, height=2.7, center_x=1.475),
        ref_offset_y=-2.286,
    ),
    "1812": FootprintSpecs(
        body_dimensions=BodyDimensions(width=6, height=3.9),
        pad_dimensions=PadDimensions(width=1.4, height=3.5, center_x=2.05),
        ref_offset_y=-2.794,
    ),
    "023x0196": FootprintSpecs(
        body_dimensions=BodyDimensions(width=8, height=5.5),
        pad_dimensions=PadDimensions(width=3.0, height=1.6, center_x=2.2),
        ref_offset_y=-3.556,
    ),
    "023x0248": FootprintSpecs(
        body_dimensions=BodyDimensions(width=9.8, height=7),
        pad_dimensions=PadDimensions(width=3.5, height=1.6, center_x=2.8),
        ref_offset_y=-4.318,
    ),
    "027x0314": FootprintSpecs(
        body_dimensions=BodyDimensions(width=12, height=8.5),
        pad_dimensions=PadDimensions(width=4.15, height=1.9, center_x=3.475),
        ref_offset_y=-5.08,
    ),
    "031x0468": FootprintSpecs(
        body_dimensions=BodyDimensions(width=12, height=8.5),
        pad_dimensions=PadDimensions(width=4.15, height=1.9, center_x=3.475),
        ref_offset_y=-5.08,
    ),
    "039x0496": FootprintSpecs(
        body_dimensions=BodyDimensions(width=14, height=10.5),
        pad_dimensions=PadDimensions(width=4.4, height=1.9, center_x=4.35),
        ref_offset_y=-6.096,
    ),
    "034x0263": FootprintSpecs(
        body_dimensions=BodyDimensions(width=12.5, height=9),
        pad_dimensions=PadDimensions(width=4.2, height=2.2, center_x=3.65),
        ref_offset_y=-6.096,
    ),
    "3025_400": FootprintSpecs(
        body_dimensions=BodyDimensions(width=8.71, height=7.12),
        pad_dimensions=PadDimensions(width=1.89, height=6.81, center_x=3.26),
        ref_offset_y=-4.318,
    ),
    "197x394": RadialFootprintSpecs(
        body_dimensions=RadialBodyDimensions(diameter=10.0),
        pad_dimensions=RadialPadDimensions(
            pad_diameter=2.0,
            drill_size=1.0,
            pad_distance=2.5,
        ),
        ref_offset_y=-6.096,
    ),
    "138x315": RadialFootprintSpecs(
        body_dimensions=RadialBodyDimensions(diameter=8.0),
        pad_dimensions=RadialPadDimensions(
            pad_diameter=2.0,
            drill_size=1.0,
            pad_distance=1.75,
        ),
        ref_offset_y=-6.096,
    ),
    "138x315_H21": RadialFootprintSpecs(
        body_dimensions=RadialBodyDimensions(diameter=8.0),
        pad_dimensions=RadialPadDimensions(
            pad_diameter=2.0,
            drill_size=1.0,
            pad_distance=1.75,
        ),
        ref_offset_y=-6.096,
    ),
    "197x512": RadialFootprintSpecs(
        body_dimensions=RadialBodyDimensions(diameter=13.0),
        pad_dimensions=RadialPadDimensions(
            pad_diameter=2.0,
            drill_size=1.0,
            pad_distance=2.5,
        ),
        ref_offset_y=-7.366,
    ),
    "295x630": RadialFootprintSpecs(
        body_dimensions=RadialBodyDimensions(diameter=16.0),
        pad_dimensions=RadialPadDimensions(
            pad_diameter=2.0,
            drill_size=1.0,
            pad_distance=3.75,
        ),
        ref_offset_y=-8.89,
    ),
    "197x492": RadialFootprintSpecs(
        body_dimensions=RadialBodyDimensions(diameter=12.5),
        pad_dimensions=RadialPadDimensions(
            pad_diameter=2.0,
            drill_size=1.0,
            pad_distance=2.5,
        ),
        ref_offset_y=-7.112,
    ),
    "295x709": RadialFootprintSpecs(
        body_dimensions=RadialBodyDimensions(diameter=18.0),
        pad_dimensions=RadialPadDimensions(
            pad_diameter=2.0,
            drill_size=1.0,
            pad_distance=3.75,
        ),
        ref_offset_y=-9.906,
    ),
    "22x45": RadialFootprintSpecs(
        body_dimensions=RadialBodyDimensions(diameter=22.0),
        pad_dimensions=RadialPadDimensions(
            pad_diameter=4.0,
            drill_size=2.0,
            pad_distance=5,
        ),
        ref_offset_y=-11.938,
    ),
    "35X61": RadialFootprintSpecs(
        body_dimensions=RadialBodyDimensions(diameter=35.0),
        pad_dimensions=RadialPadDimensions(
            pad_diameter=4.0,
            drill_size=2.0,
            pad_distance=12.15,
            # TODO: Fix additional pads possitions
            additional_pads=[
                AdditionalPad(
                    x=-6,
                    y=11.5,
                    pad_diameter=4.0,
                    drill_size=2.0,
                    name="1",
                ),
                AdditionalPad(
                    x=-6,
                    y=-11.5,
                    pad_diameter=4.0,
                    drill_size=2.0,
                    name="1",
                ),
            ],
        ),
        ref_offset_y=-18.542,
    ),
}
