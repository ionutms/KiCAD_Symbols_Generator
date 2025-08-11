"""Specifications for PCB terminal block connector footprints.

This module defines the physical dimensions and parameters needed to generate
KiCad footprints for various terminal block connectors.
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
        pad_pitch: Additional width needed per pin
        body_dimensions: Basic rectangle dimensions
        pad_size:
            Diameter/size of through-hole pads.
            Can be either a single float for circular pads
            or a list of [width, height] for rectangular pads
        drill_size: Diameter of drill holes
        mpn_y: Y position for manufacturer part number
        ref_y: Y position for reference designator
        row_pitch: Additional height needed per row
        number_of_rows: Number of rows of pins
        non_plated_pad_size: Diameter of non-plated pads
        non_plated_drill_size: Diameter of non-plated drill holes
        non_plated_row_pitch: Additional height per row of non-plated pads
        miror_zig_zag: Mirror the zig-zag pattern
        non_plated_round_mounting_holes: Non-plated mounting holes
        plated_oval_mounting_holes: Plated oval mounting holes
        internal_courtyard: Internal courtyard dimensions

    """

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


CONNECTOR_SPECS: dict[str, FootprintSpecs] = {
    "TB004-508": FootprintSpecs(
        pad_pitch=5.08,
        body_dimensions=BodyDimensions(
            width_left=5.8,
            width_right=5.2,
            height_top=5.2,
            height_bottom=5.2,
        ),
        pad_size=2.55,
        drill_size=1.7,
        mpn_y=6.096,
        ref_y=-6.096,
    ),
    "TB006-508": FootprintSpecs(
        pad_pitch=5.08,
        body_dimensions=BodyDimensions(
            width_left=5.8,
            width_right=5.2,
            height_top=4.2,
            height_bottom=4.2,
        ),
        pad_size=2.55,
        drill_size=1.7,
        mpn_y=5.334,
        ref_y=-5.334,
    ),
    "TBP02R1-381": FootprintSpecs(
        pad_pitch=3.81,
        body_dimensions=BodyDimensions(
            width_left=4.4,
            width_right=4.4,
            height_top=7.9,
            height_bottom=1.4,
        ),
        pad_size=2.1,
        drill_size=1.4,
        mpn_y=-10.2,
        ref_y=2.4,
    ),
    "TBP02R2-381": FootprintSpecs(
        pad_pitch=3.81,
        body_dimensions=BodyDimensions(
            width_left=4.445,
            width_right=4.445,
            height_top=4.445,
            height_bottom=3.2512,
        ),
        pad_size=2.1,
        drill_size=1.4,
        mpn_y=-6.8,
        ref_y=4.2,
    ),
    "TBP04R1-500": FootprintSpecs(
        pad_pitch=5.0,
        body_dimensions=BodyDimensions(
            width_left=5.2,
            width_right=5.2,
            height_top=2.2,
            height_bottom=9.9,
        ),
        pad_size=2.55,
        drill_size=1.7,
        mpn_y=10.8,
        ref_y=-3.0,
    ),
    "TBP04R2-500": FootprintSpecs(
        pad_pitch=5.0,
        body_dimensions=BodyDimensions(
            width_left=5.8,
            width_right=5.8,
            height_top=4.0,
            height_bottom=4.8,
        ),
        pad_size=2.55,
        drill_size=1.7,
        mpn_y=-6.6,
        ref_y=5.8,
    ),
    "TBP04R3-500": FootprintSpecs(
        pad_pitch=5.0,
        body_dimensions=BodyDimensions(
            width_left=5.2,
            width_right=5.2,
            height_top=4.0,
            height_bottom=4.8,
        ),
        pad_size=2.55,
        drill_size=1.7,
        mpn_y=-6.6,
        ref_y=5.8,
    ),
    "TBP04R12-500": FootprintSpecs(
        pad_pitch=5.0,
        body_dimensions=BodyDimensions(
            width_left=5.8,
            width_right=5.8,
            height_top=2.2,
            height_bottom=9.9,
        ),
        pad_size=2.55,
        drill_size=1.7,
        mpn_y=10.8,
        ref_y=-3.0,
    ),
    "SLM-1xx-01-G-S": FootprintSpecs(
        pad_pitch=1.27,
        body_dimensions=BodyDimensions(
            width_left=1.45,
            width_right=1.45,
            height_top=1.35,
            height_bottom=1.35,
        ),
        pad_size=1.0874,
        drill_size=0.787,
        mpn_y=2.032,
        ref_y=-2.032,
    ),
    "HMTSW-1xx-10-G-S-530-RA": FootprintSpecs(
        pad_pitch=2.54,
        body_dimensions=BodyDimensions(
            width_left=2.7,
            width_right=2.7,
            height_top=18,
            height_bottom=1.35,
        ),
        pad_size=1.7,
        drill_size=1,
        mpn_y=2.286,
        ref_y=-19.05,
    ),
    "TSW-1xx-14-G-S": FootprintSpecs(
        pad_pitch=2.54,
        body_dimensions=BodyDimensions(
            width_left=2.7,
            width_right=2.7,
            height_top=1.35,
            height_bottom=1.35,
        ),
        pad_size=1.7,
        drill_size=1,
        mpn_y=2.286,
        ref_y=-2.286,
    ),
    "MTSW-1xx-10-L-D-530-RA": FootprintSpecs(
        pad_pitch=2.54,
        row_pitch=2.54,
        number_of_rows=2,
        body_dimensions=BodyDimensions(
            width_left=2.7,
            width_right=2.7,
            height_top=19,
            height_bottom=2.7,
        ),
        pad_size=1.7,
        drill_size=1,
        mpn_y=3.81,
        ref_y=-19.812,
    ),
    "MTMM-1xx-04-L-D-196": FootprintSpecs(
        pad_pitch=2.00,
        row_pitch=2.00,
        number_of_rows=2,
        body_dimensions=BodyDimensions(
            width_left=2.1,
            width_right=2.1,
            height_top=2.1,
            height_bottom=2.1,
        ),
        pad_size=1.5,
        drill_size=0.9,
        mpn_y=2.794,
        ref_y=-2.794,
    ),
    "TMS-1xx-02-G-S": FootprintSpecs(
        pad_pitch=1.27,
        body_dimensions=BodyDimensions(
            width_left=1.45,
            width_right=1.45,
            height_top=1.35,
            height_bottom=1.35,
        ),
        pad_size=1.0874,
        drill_size=0.787,
        mpn_y=2.032,
        ref_y=-2.032,
    ),
    "TMS-1xx-02-G-D": FootprintSpecs(
        pad_pitch=1.27,
        row_pitch=2.54,
        number_of_rows=2,
        body_dimensions=BodyDimensions(
            width_left=1.45,
            width_right=1.45,
            height_top=2.7,
            height_bottom=2.6,
        ),
        pad_size=1.0874,
        drill_size=0.787,
        mpn_y=3.302,
        ref_y=-3.302,
    ),
    "SL-1xx-G-11": FootprintSpecs(
        pad_pitch=2.54,
        body_dimensions=BodyDimensions(
            width_left=2.65,
            width_right=2.65,
            height_top=1.35,
            height_bottom=1.35,
        ),
        pad_size=1.264,
        drill_size=0.914,
        mpn_y=2.032,
        ref_y=-2.032,
    ),
    "BBS-1xx-G-A": FootprintSpecs(
        pad_pitch=2.54,
        body_dimensions=BodyDimensions(
            width_left=2.65,
            width_right=2.65,
            height_top=1.35,
            height_bottom=1.35,
        ),
        pad_size=1.264,
        drill_size=0.914,
        mpn_y=2.032,
        ref_y=-2.032,
    ),
    "BSW-1xx-04-G-S": FootprintSpecs(
        pad_pitch=2.54,
        body_dimensions=BodyDimensions(
            width_left=2.9,
            width_right=2.9,
            height_top=1.4,
            height_bottom=3.9,
        ),
        pad_size=1.264,
        non_plated_drill_size=0.74,
        non_plated_pad_size=0.74,
        non_plated_row_pitch=2.54,
        drill_size=0.914,
        mpn_y=4.572,
        ref_y=-2.032,
    ),
    "CLP-1xx-02-G-D-BE": FootprintSpecs(
        pad_pitch=1.27,
        row_pitch=3.734,
        number_of_rows=2,
        body_dimensions=BodyDimensions(
            width_left=1.7,
            width_right=1.7,
            height_top=2.9,
            height_bottom=2.9,
        ),
        pad_size=[0.74, 1.47],
        non_plated_drill_size=0.74,
        non_plated_pad_size=0.74,
        non_plated_row_pitch=1.27,
        drill_size=0.787,
        mpn_y=3.556,
        ref_y=-3.556,
    ),
    "TSM-1xx-03-L-DH-TR": FootprintSpecs(
        pad_pitch=2.54,
        row_pitch=4.19,
        number_of_rows=2,
        mirror_x_pin_numbering=True,
        body_dimensions=BodyDimensions(
            width_left=2.7,
            width_right=2.7,
            height_top=18.5,
            height_bottom=4.5,
        ),
        pad_size=[1.27, 3.18],
        mpn_y=5.588,
        ref_y=-19.558,
    ),
    "TSM-1xx-03-L-SH-TR": FootprintSpecs(
        pad_pitch=2.54,
        body_dimensions=BodyDimensions(
            width_left=2.7,
            width_right=2.7,
            height_top=17.5,
            height_bottom=2.5,
        ),
        pad_size=[1.27, 3.18],
        mpn_y=3.556,
        ref_y=-18.542,
    ),
    "FW-xx-04-G-D-070-315": FootprintSpecs(
        pad_pitch=1.27,
        row_pitch=1.27,
        number_of_rows=2,
        body_dimensions=BodyDimensions(
            width_left=1.5,
            width_right=1.5,
            height_top=2.0,
            height_bottom=2.0,
        ),
        pad_size=1.0874,
        drill_size=0.787,
        mpn_y=3.302,
        ref_y=-3.302,
    ),
    "FW-xx-03-G-D-085-315": FootprintSpecs(
        pad_pitch=1.27,
        row_pitch=4.07,
        number_of_rows=2,
        body_dimensions=BodyDimensions(
            width_left=1.5,
            width_right=1.5,
            height_top=3.8,
            height_bottom=3.8,
        ),
        pad_size=[0.74, 2.79],
        mpn_y=4.572,
        ref_y=-4.572,
    ),
    "FW-xx-03-G-D-085-155": FootprintSpecs(
        pad_pitch=1.27,
        row_pitch=4.07,
        number_of_rows=2,
        body_dimensions=BodyDimensions(
            width_left=1.5,
            width_right=1.5,
            height_top=3.8,
            height_bottom=3.8,
        ),
        pad_size=[0.74, 2.79],
        mpn_y=4.572,
        ref_y=-4.572,
    ),
    "FTSH-1xx-01-L-DV": FootprintSpecs(
        pad_pitch=1.27,
        row_pitch=3.734,
        number_of_rows=2,
        body_dimensions=BodyDimensions(
            width_left=1.4,
            width_right=1.4,
            height_top=3.5,
            height_bottom=3.5,
        ),
        pad_size=[0.74, 2.79],
        drill_size=0.787,
        mpn_y=4.318,
        ref_y=-4.318,
    ),
    "FTSH-1xx-01-L-DV-K": FootprintSpecs(
        pad_pitch=1.27,
        row_pitch=3.734,
        number_of_rows=2,
        body_dimensions=BodyDimensions(
            width_left=1.4,
            width_right=1.4,
            height_top=3.5,
            height_bottom=3.5,
        ),
        pad_size=[0.74, 2.79],
        drill_size=0.787,
        mpn_y=4.318,
        ref_y=-4.318,
    ),
    "FTSH-1xx-04-L-D": FootprintSpecs(
        pad_pitch=1.27,
        row_pitch=1.27,
        number_of_rows=2,
        body_dimensions=BodyDimensions(
            width_left=1.4,
            width_right=1.4,
            height_top=1.8,
            height_bottom=1.8,
        ),
        pad_size=1.0874,
        drill_size=0.787,
        mpn_y=4.318,
        ref_y=-4.318,
    ),
    "TSM-1xx-01-S-SV-P-TR": FootprintSpecs(
        pad_pitch=2.54,
        row_pitch=2.92,
        miror_zig_zag=False,
        body_dimensions=BodyDimensions(
            width_left=2.7,
            width_right=2.7,
            height_top=3.5,
            height_bottom=3.5,
        ),
        pad_size=[1.27, 3.43],
        mpn_y=4.318,
        ref_y=-4.318,
    ),
    "RSM-1xx-02-STL-S": FootprintSpecs(
        pad_pitch=1.27,
        row_pitch=2.985,
        miror_zig_zag=True,
        body_dimensions=BodyDimensions(
            width_left=1.5,
            width_right=1.5,
            height_top=2.6,
            height_bottom=2.6,
        ),
        pad_size=[0.91, 1.715],
        mpn_y=4.318,
        ref_y=-4.318,
    ),
    "FTR-1xx-03-L-S": FootprintSpecs(
        pad_pitch=1.27,
        row_pitch=2.985,
        miror_zig_zag=False,
        body_dimensions=BodyDimensions(
            width_left=1.5,
            width_right=1.5,
            height_top=3.6,
            height_bottom=3.6,
        ),
        pad_size=[0.74, 3.73],
        mpn_y=4.318,
        ref_y=-4.318,
    ),
    "1043": FootprintSpecs(
        pad_pitch=71.6,
        body_dimensions=BodyDimensions(
            width_left=39,
            width_right=39,
            height_top=11,
            height_bottom=11,
        ),
        internal_courtyard=InternalCourtyard(
            width_left=30,
            width_right=30,
            height_top=3.5,
            height_bottom=3.5,
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [27.6, -8, 3.45],
            [-27.6, 8, 3.45],
            [35.8, 8, 2.39],
        ]),
        pad_size=2.0828,
        drill_size=1.5748,
        mpn_y=12.7,
        ref_y=-12.7,
    ),
    "1042P": FootprintSpecs(
        pad_pitch=79.34,
        body_dimensions=BodyDimensions(
            width_left=44,
            width_right=44,
            height_top=11,
            height_bottom=11,
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [27.6, -8, 3.45],
            [-27.6, 8, 3.45],
            [35.82, 8, 2.39],
        ]),
        pad_size=[7.46, 6.47],
        mpn_y=12.7,
        ref_y=-12.7,
    ),
    "UJ32-C-V-G-TH-8-P24-TR": FootprintSpecs(
        pad_pitch=0.5,
        row_pitch=3.3,
        number_of_rows=2,
        body_dimensions=BodyDimensions(
            width_left=3.6,
            width_right=3.6,
            height_top=2.6,
            height_bottom=2.6,
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [5.5, -1.3, 0.6],
            [-5.5, -1.3, 0.6],
        ]),
        plated_oval_mounting_holes=PlatedOvalMountingHoles([
            [-4.1, -1.47, 1.7, 1.2, 1.3, 0.8],
            [-4.1, 1.47, 1.7, 1.2, 1.3, 0.8],
            [4.1, -1.47, 1.7, 1.2, 1.3, 0.8],
            [4.1, 1.47, 1.7, 1.2, 1.3, 0.8],
        ]),
        pad_size=[0.27, 1.3],
        mpn_y=3.302,
        ref_y=-3.302,
    ),
}
