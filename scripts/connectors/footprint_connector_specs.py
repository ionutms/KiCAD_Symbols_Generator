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


class PadPosition(NamedTuple):
    """Defines the position of a single pad.

    Attributes:
        pad_number: Pad number or name (string)
        x: X position relative to the connector origin
        y: Y position relative to the connector origin
        pad_size: Optional pad size (diameter). If None, uses default pad_size
            from FootprintSpecs. Can be float for circular pads or
            list[float] for oval pads [width, height].
        drill_size: Optional drill size (diameter). If None, uses default
            drill_size from FootprintSpecs.

    """

    pad_number: str
    x: float
    y: float
    pad_size: float | list[float] | None = None
    drill_size: float | None = None


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
        zig_zag: Use zig-zag pattern for through-hole pads
        non_plated_round_mounting_holes: Non-plated mounting holes
        plated_oval_mounting_holes: Plated oval mounting holes
        internal_courtyard: Internal courtyard dimensions
        pad_positions_override:
            Optional list of custom pad positions to override
            automatic pad placement. When provided, these positions
            are used instead of calculating positions from pad_pitch.
        pad1_square:
            Whether pad 1 should be square (rect) to indicate pin 1.
            Set to False to make pad 1 circular like all other pads.

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
    zig_zag: bool = False
    mirror_x_pin_numbering: bool = False
    non_plated_round_mounting_holes: None | NonPlatedRoundMountingHoles = None
    plated_oval_mounting_holes: None | PlatedOvalMountingHoles = None
    internal_courtyard: None | InternalCourtyard = None
    show_pin1_indicator: bool = True
    pad_positions_override: None | list[PadPosition] = None
    pad1_square: bool = True


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
        pad_size=1.06,
        drill_size=0.71,
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
    "FW-xx-05-F-D-248-160": FootprintSpecs(
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
    "FW-xx-03-G-D-120-160": FootprintSpecs(
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
    "FW-xx-03-G-D-150-160": FootprintSpecs(
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
    "FW-xx-05-G-D-470-160": FootprintSpecs(
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
    "FTSH-1xx-04-L-DH": FootprintSpecs(
        pad_pitch=1.27,
        row_pitch=3.05,
        number_of_rows=2,
        body_dimensions=BodyDimensions(
            width_left=1.4,
            width_right=1.4,
            height_top=5.6,
            height_bottom=3,
        ),
        pad_size=[0.76, 2.03],
        mpn_y=3.81,
        ref_y=-6.35,
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
        show_pin1_indicator=False,
        mirror_x_pin_numbering=True,
    ),
    "FW-xx-04-G-D-370-160": FootprintSpecs(
        pad_pitch=1.27,
        row_pitch=1.27,
        number_of_rows=2,
        body_dimensions=BodyDimensions(
            width_left=1.5,
            width_right=1.5,
            height_top=2.0,
            height_bottom=2.0,
        ),
        pad_size=1.06,
        drill_size=0.71,
        mpn_y=3.302,
        ref_y=-3.302,
    ),
    "FW-xx-01-G-D-160-160": FootprintSpecs(
        pad_pitch=1.27,
        row_pitch=1.27,
        number_of_rows=2,
        body_dimensions=BodyDimensions(
            width_left=1.5,
            width_right=1.5,
            height_top=2.0,
            height_bottom=2.0,
        ),
        pad_size=1.06,
        drill_size=0.71,
        mpn_y=3.302,
        ref_y=-3.302,
    ),
    "68000-2xxHLF": FootprintSpecs(
        pad_pitch=2.54,
        body_dimensions=BodyDimensions(
            width_left=2.7,
            width_right=2.7,
            height_top=1.35,
            height_bottom=1.35,
        ),
        pad_size=1.7,
        drill_size=1,
        mpn_y=2.032,
        ref_y=-2.032,
    ),
    "OQ": FootprintSpecs(
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
    "SL 11 139 xx G": FootprintSpecs(
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
    "T4145015051-001": FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=10,
            width_right=10,
            height_top=3.3,
            height_bottom=8.6,
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-7.5, 0, 2.35],
            [7.5, 0, 2.35],
            [-7.5, 4, 2.8],
            [7.5, 4, 2.8],
        ]),
        pad_size=2,
        drill_size=1.3,
        mpn_y=9.652,
        ref_y=-4.064,
        pad_positions_override=[
            PadPosition(pad_number="1", x=-1.77, y=-1.77),
            PadPosition(pad_number="2", x=1.77, y=-1.77),
            PadPosition(pad_number="5", x=0, y=0),
            PadPosition(pad_number="3", x=1.77, y=1.77),
            PadPosition(pad_number="4", x=-1.77, y=1.77),
        ],
        pad1_square=False,
    ),
    "2496699-2": FootprintSpecs(
        pad_pitch=1.02,
        row_pitch=1.78,
        number_of_rows=1,
        zig_zag=True,
        body_dimensions=BodyDimensions(
            width_left=10,
            width_right=10,
            height_top=7.1,
            height_bottom=8.9,
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-6.35, 3.43, 3.15],
            [6.35, 3.43, 3.15],
        ]),
        pad_positions_override=[
            PadPosition(pad_number="8", x=-3.57, y=-0.89),
            PadPosition(pad_number="7", x=-2.55, y=0.89),
            PadPosition(pad_number="6", x=-1.53, y=-0.89),
            PadPosition(pad_number="5", x=-0.51, y=0.89),
            PadPosition(pad_number="4", x=0.51, y=-0.89),
            PadPosition(pad_number="3", x=1.53, y=0.89),
            PadPosition(pad_number="2", x=2.55, y=-0.89),
            PadPosition(pad_number="1", x=3.57, y=0.89),
            PadPosition(pad_number="12", x=-6.86, y=-5.7),
            PadPosition(pad_number="9", x=6.86, y=-5.7),
            PadPosition(pad_number="11", x=-4.57, y=-5.7),
            PadPosition(pad_number="10", x=4.57, y=-5.7),
            PadPosition(
                pad_number="SH1", x=-8.1, y=0, pad_size=2.2, drill_size=1.7
            ),
            PadPosition(
                pad_number="SH2", x=8.1, y=0, pad_size=2.2, drill_size=1.7
            ),
        ],
        pad_size=1.2,
        drill_size=0.9,
        mpn_y=9.906,
        ref_y=-8.128,
        show_pin1_indicator=False,
        pad1_square=True,
    ),
}
CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=21, width_right=21, height_top=25, height_bottom=15
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-14.925, -13.3, 3.75],
            [14.925, -13.3, 3.75],
        ]),
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-27.94,
        ref_y=16.002,
        pad_positions_override=[
            # Rows 1–3
            *[
                PadPosition(
                    pad_number=str(row * 14 + col + 1),
                    x=xpos,
                    y=row * 3,
                )
                for row in range(3)
                for col, xpos in enumerate([
                    -15.74,
                    -13.74,
                    -11.74,
                    -9.74,
                    -7.74,
                    -5.74,
                    -3.74,
                    3.74,
                    5.74,
                    7.74,
                    9.74,
                    11.74,
                    13.74,
                    15.74,
                ])
            ],
            # Row 4
            *[
                PadPosition(
                    pad_number=str(num),
                    x=xpos,
                    y=9,
                    pad_size=1.7,
                    drill_size=1.3,
                )
                for num, xpos in zip(
                    range(43, 49),
                    [-15.74, -7.74, -3.74, 3.74, 11.74, 15.74],
                )
            ],
            # Row 5
            *[
                PadPosition(
                    pad_number=str(num),
                    x=xpos,
                    y=12,
                    pad_size=1.7,
                    drill_size=1.3,
                )
                for num, xpos in zip(
                    range(49, 57),
                    [-15.74, -11.74, -7.74, -3.74, 3.74, 7.74, 11.74, 15.74],
                )
            ],
        ],
        pad1_square=False,
    )
    for mpn in [
        "1600130623",
        "1600130641",
        "1600132623",
        "1600132641",
        "1600133623",
        "1600133641",
        "1600133724",
        "1600133741",
        "1600133841",
        "1600133941",
        "1600134141",
        "1600134623",
        "1600134641",
    ]
}

CONNECTOR_SPECS["1600131624"] = FootprintSpecs(
    show_pin1_indicator=False,
    pad_pitch=3.54,
    body_dimensions=BodyDimensions(
        width_left=21, width_right=21, height_top=25, height_bottom=15
    ),
    non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
        [-14.925, -13.3, 3.75],
        [14.925, -13.3, 3.75],
    ]),
    pad_size=1.5,
    drill_size=1.1,
    mpn_y=-27.94,
    ref_y=16.002,
    pad_positions_override=[
        # Row 1
        *[
            PadPosition(pad_number=str(col + 1), x=xpos, y=0)
            for col, xpos in enumerate([
                -15.74,
                -13.74,
                -11.74,
                -9.74,
                -7.74,
                -5.74,
                -3.74,
                3.74,
                5.74,
                7.74,
                9.74,
                11.74,
                13.74,
                15.74,
            ])
        ],
        # Row 2
        *[
            PadPosition(pad_number=str(14 + col + 1), x=xpos, y=6)
            for col, xpos in enumerate([
                -15.74,
                -13.74,
                -11.74,
                -9.74,
                -7.74,
                -5.74,
                -3.74,
            ])
        ],
        # Row 3
        *[
            PadPosition(
                pad_number=str(num),
                x=xpos,
                y=9,
                pad_size=1.7,
                drill_size=1.3,
            )
            for num, xpos in zip(range(22, 25), [3.74, 11.74, 15.74])
        ],
        # Row 4
        *[
            PadPosition(
                pad_number=str(num),
                x=xpos,
                y=12,
                pad_size=1.7,
                drill_size=1.3,
            )
            for num, xpos in zip(
                range(25, 33),
                [-15.74, -11.74, -7.74, -3.74, 3.74, 7.74, 11.74, 15.74],
            )
        ],
    ],
    pad1_square=False,
)

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=11, width_right=11, height_top=25, height_bottom=15
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-7.05, -13.3, 3.75],
            [7.05, -13.3, 3.75],
        ]),
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-27.94,
        ref_y=16.002,
        pad_positions_override=[
            # Rows 1–3
            *[
                PadPosition(
                    pad_number=str(row * 7 + col + 1),
                    x=xpos,
                    y=row * 3,
                )
                for row in range(3)
                for col, xpos in enumerate([-6, -4, -2, 0, 2, 4, 6])
            ],
            # Row 4
            *[
                PadPosition(
                    pad_number=str(num),
                    x=xpos,
                    y=9,
                    pad_size=1.7,
                    drill_size=1.3,
                )
                for num, xpos in zip(range(22, 25), [-6, 2, 6])
            ],
            # Row 5
            *[
                PadPosition(
                    pad_number=str(num),
                    x=xpos,
                    y=12,
                    pad_size=1.7,
                    drill_size=1.3,
                )
                for num, xpos in zip(range(25, 29), [-6, -2, 2, 6])
            ],
        ],
        pad1_square=False,
    )
    for mpn in ["1600136601", "1600136602", "1600136603", "1600136604"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=14, width_right=14, height_top=28, height_bottom=14
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-11.7, -3.8, 2.9],
            [11.7, -3.8, 2.9],
        ]),
        pad_size=2.1,
        drill_size=1.5,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            # Row 1
            *[
                PadPosition(pad_number=str(num), x=xpos, y=0)
                for num, xpos in zip(
                    [1, 1, 2, 2],
                    [-4.6, -0.6, 2.6, 6.6],
                )
            ],
            # Row 2
            *[
                PadPosition(pad_number=str(num), x=xpos, y=3)
                for num, xpos in zip(
                    [3, 3, 4, 4],
                    [-6.6, -2.6, 0.6, 4.6],
                )
            ],
            # Rows 3–4 (pad_size and drill_size vary per group)
            *[
                PadPosition(
                    pad_number=str(num),
                    x=xpos,
                    y=ypos,
                    pad_size=pad_size,
                    drill_size=drill_size,
                )
                for ypos, num_range, xpositions, pad_size, drill_size in [
                    (6, range(5, 9), [-6.6, -2.6, 2.6, 6.6], 1.9, 1.3),
                    (9, range(9, 13), [-6.6, -2.6, 2.6, 6.6], 1.9, 1.3),
                ]
                for num, xpos in zip(num_range, xpositions)
            ],
        ],
        pad1_square=False,
    )
    for mpn in ["2005020121", "2005020122", "2005020123", "2005020124"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=14, width_right=14, height_top=28, height_bottom=14
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-11.7, -3.8, 2.9],
            [11.7, -3.8, 2.9],
        ]),
        pad_size=2.1,
        drill_size=1.5,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            # Row 1
            *[
                PadPosition(pad_number=str(num), x=xpos, y=0)
                for num, xpos in zip(
                    [1, 1, 2, 2],
                    [-4.6, -0.6, 2.6, 6.6],
                )
            ],
            # Row 2
            *[
                PadPosition(pad_number=str(num), x=xpos, y=3)
                for num, xpos in zip(
                    [3, 3, 4, 4],
                    [-6.6, -2.6, 0.6, 4.6],
                )
            ],
            # Rows 3–5
            *[
                PadPosition(
                    pad_number=str(num),
                    x=xpos,
                    y=ypos,
                    pad_size=1.5,
                    drill_size=1.1,
                )
                for ypos, num_range in [
                    (6, range(5, 12)),
                    (9, range(12, 20)),
                    (12, range(19, 26)),
                ]
                for num, xpos in zip(
                    num_range,
                    [-6.6, -4.6, -2.6, 0.6, 2.6, 4.6, 6.6],
                )
            ],
        ],
        pad1_square=False,
    )
    for mpn in ["2005020251", "2005020252", "2005020253", "2005020254"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=14, width_right=14, height_top=28, height_bottom=14
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-11.7, -3.8, 2.9],
            [11.7, -3.8, 2.9],
        ]),
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            # Row 1
            *[
                PadPosition(pad_number=str(num), x=xpos, y=0)
                for num, xpos in zip(range(1, 8), [-6, -4, -2, 0, 2, 4, 6])
            ],
            # Rows 2–3
            *[
                PadPosition(pad_number=str(num), x=xpos, y=ypos)
                for ypos, num_range in [(3, range(8, 14)), (6, range(14, 20))]
                for num, xpos in zip(num_range, [-6, -4, -2, 2, 4, 6])
            ],
            # Rows 4–5
            *[
                PadPosition(
                    pad_number=str(num),
                    x=xpos,
                    y=ypos,
                    pad_size=1.7,
                    drill_size=1.3,
                )
                for ypos, num_range in [
                    (9, range(20, 24)),
                    (12, range(24, 28)),
                ]
                for num, xpos in zip(num_range, [-6, -2, 2, 6])
            ],
        ],
        pad1_square=False,
    )
    for mpn in ["2005020271", "2005020272", "2005020273", "2005020274"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=14, width_right=14, height_top=28, height_bottom=14
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-11.7, -3.8, 2.9],
            [11.7, -3.8, 2.9],
        ]),
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            # Rows 1–3
            *[
                PadPosition(pad_number=str(num), x=xpos, y=ypos)
                for ypos, num_range in [
                    (0, range(1, 8)),
                    (3, range(8, 15)),
                    (6, range(15, 22)),
                ]
                for num, xpos in zip(num_range, [-6, -4, -2, 0, 2, 4, 6])
            ],
            # Rows 4
            *[
                PadPosition(
                    pad_number=str(num),
                    x=xpos,
                    y=ypos,
                    pad_size=1.7,
                    drill_size=1.3,
                )
                for ypos, num_range in [(9, range(22, 25))]
                for num, xpos in zip(num_range, [-6, 2, 6])
            ],
            # Rows 5
            *[
                PadPosition(
                    pad_number=str(num),
                    x=xpos,
                    y=ypos,
                    pad_size=1.7,
                    drill_size=1.3,
                )
                for ypos, num_range in [(12, range(25, 29))]
                for num, xpos in zip(num_range, [-6, -2, 2, 6])
            ],
        ],
        pad1_square=False,
    )
    for mpn in ["2005020281", "2005020282", "2005020283", "2005020284"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=14, width_right=14, height_top=28, height_bottom=14
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-11.7, -3.8, 2.9],
            [11.7, -3.8, 2.9],
        ]),
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            # Rows 1–4
            *[
                PadPosition(pad_number=str(num), x=xpos, y=ypos)
                for ypos, num_range in [
                    (0, range(1, 8)),
                    (3, range(8, 15)),
                    (6, range(15, 22)),
                    (9, range(22, 29)),
                ]
                for num, xpos in zip(
                    num_range, [-6.6, -4.6, -2.6, 0.6, 2.6, 4.6, 6.6]
                )
            ],
            # Rows 5
            *[
                PadPosition(
                    pad_number=str(num),
                    x=xpos,
                    y=ypos,
                    pad_size=1.7,
                    drill_size=1.3,
                )
                for ypos, num_range in [(12, range(29, 33))]
                for num, xpos in zip(num_range, [-6.6, -2.6, 2.6, 6.6])
            ],
        ],
        pad1_square=False,
    )
    for mpn in ["2005020321", "2005020322", "2005020323", "2005020324"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=14, width_right=14, height_top=28, height_bottom=14
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-11.7, -3.8, 2.9],
            [11.7, -3.8, 2.9],
        ]),
        pad_size=2.1,
        drill_size=1.5,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            # Row 1
            *[
                PadPosition(pad_number=str(num), x=xpos, y=0)
                for num, xpos in zip(
                    [1, 1, 2, 2],
                    [-4.6, -0.6, 2.6, 6.6],
                )
            ],
            # Row 2
            *[
                PadPosition(pad_number=str(num), x=xpos, y=3)
                for num, xpos in zip(
                    [3, 3, 4, 4],
                    [-6.6, -2.6, 0.6, 4.6],
                )
            ],
            # Rows 3–4
            *[
                PadPosition(
                    pad_number=str(num),
                    x=xpos,
                    y=ypos,
                    pad_size=1.5,
                    drill_size=1.1,
                )
                for ypos, num_range in [(6, range(5, 9)), (9, range(9, 13))]
                for num, xpos in zip(num_range, [-6.6, -2.6, 2.6, 6.6])
            ],
        ],
        pad1_square=False,
    )
    for mpn in ["2005021121", "2005021122", "2005021123", "2005021124"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=14, width_right=14, height_top=28, height_bottom=14
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-11.7, -3.8, 2.9],
            [11.7, -3.8, 2.9],
        ]),
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            # Rows 1–3
            *[
                PadPosition(pad_number=str(num), x=xpos, y=ypos)
                for ypos, num_range in [
                    (0, range(1, 8)),
                    (3, range(8, 15)),
                    (6, range(15, 22)),
                ]
                for num, xpos in zip(num_range, [-6, -4, -2, 0, 2, 4, 6])
            ],
            # Rows 4
            *[
                PadPosition(
                    pad_number=str(num),
                    x=xpos,
                    y=ypos,
                    pad_size=2.1,
                    drill_size=1.5,
                )
                for ypos, num_range in [(9.67, [22, 22, 22, 23, 23, 23])]
                for num, xpos in zip(
                    num_range, [-7.08, -4.54, -2, 0.92, 3.46, 6]
                )
            ],
        ],
        pad1_square=False,
    )
    for mpn in ["2005021231", "2005021232", "2005021233", "2005021234"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=14, width_right=14, height_top=28, height_bottom=14
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-11.7, -3.8, 2.9],
            [11.7, -3.8, 2.9],
        ]),
        pad_size=2.1,
        drill_size=1.5,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            # Row 1
            *[
                PadPosition(pad_number=str(num), x=xpos, y=0)
                for num, xpos in zip(
                    [1, 1, 2, 2],
                    [-4.6, -0.6, 2.6, 6.6],
                )
            ],
            # Row 2
            *[
                PadPosition(pad_number=str(num), x=xpos, y=3)
                for num, xpos in zip(
                    [3, 3, 4, 4],
                    [-6.6, -2.6, 0.6, 4.6],
                )
            ],
            # Rows 3–5
            *[
                PadPosition(
                    pad_number=str(num),
                    x=xpos,
                    y=ypos,
                    pad_size=1.5,
                    drill_size=1.1,
                )
                for ypos, num_range in [
                    (6, range(5, 12)),
                    (9, range(12, 19)),
                    (12, range(19, 26)),
                ]
                for num, xpos in zip(
                    num_range, [-6.6, -4.6, -2.6, 0.6, 2.6, 4.6, 6.6]
                )
            ],
        ],
        pad1_square=False,
    )
    for mpn in ["2005021251", "2005021252", "2005021253", "2005021254"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=14, width_right=14, height_top=28, height_bottom=14
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-11.7, -3.8, 2.9],
            [11.7, -3.8, 2.9],
        ]),
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            # Row 1
            *[
                PadPosition(pad_number=str(num), x=xpos, y=0)
                for num, xpos in zip(range(1, 8), [-6, -4, -2, 0, 2, 4, 6])
            ],
            # Rows 2–3
            *[
                PadPosition(pad_number=str(num), x=xpos, y=ypos)
                for ypos, num_range in [(3, range(8, 14)), (6, range(14, 20))]
                for num, xpos in zip(num_range, [-6, -4, -2, 2, 4, 6])
            ],
            # Rows 4–5
            *[
                PadPosition(
                    pad_number=str(num),
                    x=xpos,
                    y=ypos,
                    pad_size=1.7,
                    drill_size=1.3,
                )
                for ypos, num_range in [
                    (9, range(20, 24)),
                    (12, range(24, 28)),
                ]
                for num, xpos in zip(num_range, [-6, -2, 2, 6])
            ],
        ],
        pad1_square=False,
    )
    for mpn in ["2005021271", "2005021272", "2005021273", "2005021274"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=14, width_right=14, height_top=28, height_bottom=14
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-11.7, -3.8, 2.9],
            [11.7, -3.8, 2.9],
        ]),
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            # Rows 1–3
            *[
                PadPosition(pad_number=str(num), x=xpos, y=ypos)
                for ypos, num_range in [
                    (0, range(1, 8)),
                    (3, range(8, 15)),
                    (6, range(15, 22)),
                ]
                for num, xpos in zip(num_range, [-6, -4, -2, 0, 2, 4, 6])
            ],
            # Rows 4
            *[
                PadPosition(
                    pad_number=str(num),
                    x=xpos,
                    y=ypos,
                    pad_size=1.7,
                    drill_size=1.3,
                )
                for ypos, num_range in [(9, range(22, 25))]
                for num, xpos in zip(num_range, [-6, 2, 6])
            ],
            # Rows 5
            *[
                PadPosition(
                    pad_number=str(num),
                    x=xpos,
                    y=ypos,
                    pad_size=1.7,
                    drill_size=1.3,
                )
                for ypos, num_range in [(12, range(25, 29))]
                for num, xpos in zip(num_range, [-6, -2, 2, 6])
            ],
        ],
        pad1_square=False,
    )
    for mpn in ["2005021281", "2005021282", "2005021283", "2005021284"]
}
CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=14, width_right=14, height_top=28, height_bottom=14
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-11.7, -3.8, 2.9],
            [11.7, -3.8, 2.9],
        ]),
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            # Rows 1–4
            *[
                PadPosition(pad_number=str(num), x=xpos, y=ypos)
                for ypos, num_range in [
                    (0, range(1, 8)),
                    (3, range(8, 15)),
                    (6, range(15, 22)),
                    (9, range(22, 29)),
                ]
                for num, xpos in zip(
                    num_range, [-6.6, -4.6, -2.6, 0.6, 2.6, 4.6, 6.6]
                )
            ],
            # Rows 5
            *[
                PadPosition(
                    pad_number=str(num),
                    x=xpos,
                    y=ypos,
                    pad_size=1.7,
                    drill_size=1.3,
                )
                for ypos, num_range in [(12, range(29, 33))]
                for num, xpos in zip(num_range, [-6.6, -2.6, 2.6, 6.6])
            ],
        ],
        pad1_square=False,
    )
    for mpn in ["2005021321", "2005021322", "2005021323", "2005021324"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=25.5, width_right=25.5, height_top=28, height_bottom=14
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-23.4, -3.8, 2.9],
            [0, -3.8, 2.9],
            [23.4, -3.8, 2.9],
        ]),
        pad_size=2.1,
        drill_size=1.5,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            PadPosition(
                pad_number=str(pad_base + pad_offset),
                x=pad_x + group_x_shift,
                y=row_y,
                **extra,
            )
            for group_x_shift, pad_base in zip([-11.7, 11.7], [0, 12])
            for offsets, row_y, x_positions, extra in [
                ([1, 2], 0, [-4.6, -0.6, 2.6, 6.6], {}),
                ([3, 4], 3, [-6.6, -2.6, 0.6, 4.6], {}),
                (
                    [5, 6, 7, 8],
                    6,
                    [-6.6, -2.6, 2.6, 6.6],
                    {"pad_size": 1.5, "drill_size": 1.1},
                ),
                (
                    [9, 10, 11, 12],
                    9,
                    [-6.6, -2.6, 2.6, 6.6],
                    {"pad_size": 1.5, "drill_size": 1.1},
                ),
            ]
            for pad_offset, pad_x in zip(
                [num for num in offsets for _ in range(2)]
                if len(offsets) == 2
                else offsets,
                x_positions,
            )
        ],
        pad1_square=False,
    )
    for mpn in ["2005062007", "2005062507"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=25.5, width_right=25.5, height_top=28, height_bottom=14
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-23.4, -3.8, 2.9],
            [0, -3.8, 2.9],
            [23.4, -3.8, 2.9],
        ]),
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            # Left side
            PadPosition(
                pad_number=str(pad_base + pad_offset),
                x=pad_x - 11.7,
                y=row_y,
                **extra,
            )
            for offsets, row_y, x_positions, extra in [
                (
                    [1, 2],
                    0,
                    [-4.6, -0.6, 2.6, 6.6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
                (
                    [3, 4],
                    3,
                    [-6.6, -2.6, 0.6, 4.6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
                ([5, 6, 7, 8], 6, [-6.6, -2.6, 2.6, 6.6], {}),
                ([9, 10, 11, 12], 9, [-6.6, -2.6, 2.6, 6.6], {}),
            ]
            for pad_offset, pad_x in zip(
                [num for num in offsets for _ in range(2)]
                if len(offsets) == 2
                else offsets,
                x_positions,
            )
            for pad_base in [
                0
            ]  # keeps left side self-contained in one comprehension
        ]
        + [
            # Right side — asymmetric, listed explicitly per row
            PadPosition(
                pad_number=str(pad_num),
                x=pad_x + 11.7,
                y=row_y,
                **extra,
            )
            for pad_nums, row_y, x_positions, extra in [
                (
                    [13, 14, 15, 16, 17, 18, 19],
                    0,
                    [-6, -4, -2, 0, 2, 4, 6],
                    {},
                ),
                (
                    [20, 21, 22, 23, 24, 25, 26],
                    3,
                    [-6, -4, -2, 0, 2, 4, 6],
                    {},
                ),
                (
                    [27, 28, 29, 30, 31, 32, 33],
                    6,
                    [-6, -4, -2, 0, 2, 4, 6],
                    {},
                ),
                (
                    [34, 34, 34, 35, 35, 35],
                    9.67,
                    [-7.08, -4.54, -2, 0.92, 3.46, 6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
            ]
            for pad_num, pad_x in zip(pad_nums, x_positions)
        ],
        pad1_square=False,
    )
    for mpn in ["2005062031", "2005062531"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=36.5, width_right=36.5, height_top=28, height_bottom=14
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-35.1, -3.8, 2.9],
            [-11.7, -3.8, 2.9],
            [11.7, -3.8, 2.9],
            [35.1, -3.8, 2.9],
        ]),
        pad_size=2.1,
        drill_size=1.5,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            PadPosition(
                pad_number=str(pad_base + pad_offset),
                x=pad_x + group_x_shift,
                y=row_y,
                **extra,
            )
            for group_x_shift, pad_base in zip(
                [-23.4, 0.0, 23.4],
                [0, 12, 24],
            )
            for offsets, row_y, x_positions, extra in [
                ([1, 2], 0, [-4.6, -0.6, 2.6, 6.6], {}),
                ([3, 4], 3, [-6.6, -2.6, 0.6, 4.6], {}),
                (
                    [5, 6, 7, 8],
                    6,
                    [-6.6, -2.6, 2.6, 6.6],
                    {"pad_size": 1.5, "drill_size": 1.1},
                ),
                (
                    [9, 10, 11, 12],
                    9,
                    [-6.6, -2.6, 2.6, 6.6],
                    {"pad_size": 1.5, "drill_size": 1.1},
                ),
            ]
            for pad_offset, pad_x in zip(
                [num for num in offsets for _ in range(2)]
                if len(offsets) == 2
                else offsets,
                x_positions,
            )
        ],
        pad1_square=False,
    )
    for mpn in ["2005063010", "2005063510"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=25.5, width_right=25.5, height_top=28, height_bottom=14
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-23.4, -3.8, 2.9],
            [0, -3.8, 2.9],
            [23.4, -3.8, 2.9],
        ]),
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            # Left side
            PadPosition(
                pad_number=str(pad_base + pad_offset),
                x=pad_x - 11.7,
                y=row_y,
                **extra,
            )
            for offsets, row_y, x_positions, extra in [
                (
                    [1, 2],
                    0,
                    [-4.6, -0.6, 2.6, 6.6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
                (
                    [3, 4],
                    3,
                    [-6.6, -2.6, 0.6, 4.6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
                ([5, 6, 7, 8], 6, [-6.6, -2.6, 2.6, 6.6], {}),
                ([9, 10, 11, 12], 9, [-6.6, -2.6, 2.6, 6.6], {}),
            ]
            for pad_offset, pad_x in zip(
                [num for num in offsets for _ in range(2)]
                if len(offsets) == 2
                else offsets,
                x_positions,
            )
            for pad_base in [
                0
            ]  # keeps left side self-contained in one comprehension
        ]
        + [
            # Right side — asymmetric, listed explicitly per row
            PadPosition(
                pad_number=str(pad_num),
                x=pad_x + 11.7,
                y=row_y,
                **extra,
            )
            for pad_nums, row_y, x_positions, extra in [
                (
                    [13, 13, 14, 14],
                    0,
                    [-4.6, -0.6, 2.6, 6.6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
                (
                    [15, 15, 16, 16],
                    3,
                    [-6.6, -2.6, 0.6, 4.6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
                (
                    [17, 18, 19, 20, 21, 22, 23],
                    6,
                    [-6.6, -4.6, -2.6, 0.6, 2.6, 4.6, 6.6],
                    {},
                ),
                (
                    [24, 25, 26, 27, 28, 29, 30],
                    9,
                    [-6.6, -4.6, -2.6, 0.6, 2.6, 4.6, 6.6],
                    {},
                ),
                (
                    [31, 32, 33, 34, 35, 36, 37],
                    12,
                    [-6.6, -4.6, -2.6, 0.6, 2.6, 4.6, 6.6],
                    {},
                ),
            ]
            for pad_num, pad_x in zip(pad_nums, x_positions)
        ],
        pad1_square=False,
    )
    for mpn in ["2005062030", "2005062530"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=25.5, width_right=25.5, height_top=28, height_bottom=14
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-23.4, -3.8, 2.9],
            [0, -3.8, 2.9],
            [23.4, -3.8, 2.9],
        ]),
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            # Left side — asymmetric, listed explicitly per row
            PadPosition(
                pad_number=str(pad_num),
                x=pad_x - 11.7,
                y=row_y,
                **extra,
            )
            for pad_nums, row_y, x_positions, extra in [
                ([1, 2, 3, 4, 5, 6, 7], 0, [-6, -4, -2, 0, 2, 4, 6], {}),
                ([8, 9, 10, 11, 12, 13], 3, [-6, -4, -2, 2, 4, 6], {}),
                ([14, 15, 16, 17, 18, 19], 6, [-6, -4, -2, 2, 4, 6], {}),
                (
                    [20, 21, 22, 23],
                    9,
                    [-6, -2, 2, 6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
                (
                    [24, 25, 26, 27],
                    12,
                    [-6, -2, 2, 6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
            ]
            for pad_num, pad_x in zip(pad_nums, x_positions)
        ]
        + [
            # Right side — generic doubling comprehension
            PadPosition(
                pad_number=str(pad_base + pad_offset),
                x=pad_x + 11.7,
                y=row_y,
                **extra,
            )
            for offsets, row_y, x_positions, extra in [
                (
                    [1, 2],
                    0,
                    [-4.6, -0.6, 2.6, 6.6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
                (
                    [3, 4],
                    3,
                    [-6.6, -2.6, 0.6, 4.6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
                ([5, 6, 7, 8], 6, [-6.6, -2.6, 2.6, 6.6], {}),
                ([9, 10, 11, 12], 9, [-6.6, -2.6, 2.6, 6.6], {}),
            ]
            for pad_offset, pad_x in zip(
                [num for num in offsets for _ in range(2)]
                if len(offsets) == 2
                else offsets,
                x_positions,
            )
            for pad_base in [27]
        ],
        pad1_square=False,
    )
    for mpn in ["2005062005", "2005062105"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=25.5, width_right=25.5, height_top=28, height_bottom=14
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-23.4, -3.8, 2.9],
            [0, -3.8, 2.9],
            [23.4, -3.8, 2.9],
        ]),
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            # Left side — generic doubling comprehension
            PadPosition(
                pad_number=str(pad_base + pad_offset),
                x=pad_x - 11.7,
                y=row_y,
                **extra,
            )
            for offsets, row_y, x_positions, extra in [
                (
                    [1, 2],
                    0,
                    [-4.6, -0.6, 2.6, 6.6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
                (
                    [3, 4],
                    3,
                    [-6.6, -2.6, 0.6, 4.6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
                ([5, 6, 7, 8], 6, [-6.6, -2.6, 2.6, 6.6], {}),
                ([9, 10, 11, 12], 9, [-6.6, -2.6, 2.6, 6.6], {}),
            ]
            for pad_offset, pad_x in zip(
                [num for num in offsets for _ in range(2)]
                if len(offsets) == 2
                else offsets,
                x_positions,
            )
            for pad_base in [0]
        ]
        + [
            # Right side — asymmetric, listed explicitly per row
            PadPosition(
                pad_number=str(pad_num),
                x=pad_x + 11.7,
                y=row_y,
                **extra,
            )
            for pad_nums, row_y, x_positions, extra in [
                (
                    [13, 14, 15, 16, 17, 18, 19],
                    0,
                    [-6, -4, -2, 0, 2, 4, 6],
                    {},
                ),
                ([20, 21, 22, 23, 24, 25], 3, [-6, -4, -2, 2, 4, 6], {}),
                ([26, 27, 28, 29, 30, 31], 6, [-6, -4, -2, 2, 4, 6], {}),
                (
                    [32, 33, 34, 35],
                    9,
                    [-6, -2, 2, 6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
                (
                    [36, 37, 38, 39],
                    12,
                    [-6, -2, 2, 6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
            ]
            for pad_num, pad_x in zip(pad_nums, x_positions)
        ],
        pad1_square=False,
    )
    for mpn in ["2005062015", "2005062515"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=25.5, width_right=25.5, height_top=28, height_bottom=14
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-23.4, -3.8, 2.9],
            [0, -3.8, 2.9],
            [23.4, -3.8, 2.9],
        ]),
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            # Left side — generic doubling comprehension
            PadPosition(
                pad_number=str(pad_base + pad_offset),
                x=pad_x - 11.7,
                y=row_y,
                **extra,
            )
            for offsets, row_y, x_positions, extra in [
                (
                    [1, 2],
                    0,
                    [-4.6, -0.6, 2.6, 6.6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
                (
                    [3, 4],
                    3,
                    [-6.6, -2.6, 0.6, 4.6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
                ([5, 6, 7, 8], 6, [-6.6, -2.6, 2.6, 6.6], {}),
                ([9, 10, 11, 12], 9, [-6.6, -2.6, 2.6, 6.6], {}),
            ]
            for pad_offset, pad_x in zip(
                [num for num in offsets for _ in range(2)]
                if len(offsets) == 2
                else offsets,
                x_positions,
            )
            for pad_base in [0]
        ]
        + [
            # Right side — asymmetric, listed explicitly per row
            PadPosition(
                pad_number=str(pad_num),
                x=pad_x + 11.7,
                y=row_y,
                **extra,
            )
            for pad_nums, row_y, x_positions, extra in [
                (
                    [13, 14, 15, 16, 17, 18, 19],
                    0,
                    [-6.6, -4.6, -2.6, 0.6, 2.6, 4.6, 6.6],
                    {},
                ),
                (
                    [20, 21, 22, 23, 24, 25, 26],
                    3,
                    [-6.6, -4.6, -2.6, 0.6, 2.6, 4.6, 6.6],
                    {},
                ),
                (
                    [27, 28, 29, 30, 31, 32, 33],
                    6,
                    [-6.6, -4.6, -2.6, 0.6, 2.6, 4.6, 6.6],
                    {},
                ),
                (
                    [34, 35, 36, 37, 38, 39, 40],
                    9,
                    [-6.6, -4.6, -2.6, 0.6, 2.6, 4.6, 6.6],
                    {},
                ),
                (
                    [41, 42, 43, 44],
                    12,
                    [-6.6, -2.6, 2.6, 6.6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
            ]
            for pad_num, pad_x in zip(pad_nums, x_positions)
        ],
        pad1_square=False,
    )
    for mpn in ["2005062012", "2005062023", "2005062025", "2005062525"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=25.5, width_right=25.5, height_top=28, height_bottom=14
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-23.4, -3.8, 2.9],
            [0, -3.8, 2.9],
            [23.4, -3.8, 2.9],
        ]),
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            # Left side — asymmetric, listed explicitly per row
            PadPosition(
                pad_number=str(pad_num),
                x=pad_x - 11.7,
                y=row_y,
                **extra,
            )
            for pad_nums, row_y, x_positions, extra in [
                (
                    [1, 2, 3, 4, 5, 6, 7],
                    0,
                    [-6.6, -4.6, -2.6, 0.6, 2.6, 4.6, 6.6],
                    {},
                ),
                (
                    [8, 9, 10, 11, 12, 13, 14],
                    3,
                    [-6.6, -4.6, -2.6, 0.6, 2.6, 4.6, 6.6],
                    {},
                ),
                (
                    [15, 16, 17, 18, 19, 20, 21],
                    6,
                    [-6.6, -4.6, -2.6, 0.6, 2.6, 4.6, 6.6],
                    {},
                ),
                (
                    [22, 23, 24, 25, 26, 27, 28],
                    9,
                    [-6.6, -4.6, -2.6, 0.6, 2.6, 4.6, 6.6],
                    {},
                ),
                (
                    [29, 30, 31, 32],
                    12,
                    [-6.6, -2.6, 2.6, 6.6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
            ]
            for pad_num, pad_x in zip(pad_nums, x_positions)
        ]
        + [
            # Right side — generic doubling comprehension
            PadPosition(
                pad_number=str(pad_base + pad_offset),
                x=pad_x + 11.7,
                y=row_y,
                **extra,
            )
            for offsets, row_y, x_positions, extra in [
                (
                    [1, 2],
                    0,
                    [-4.6, -0.6, 2.6, 6.6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
                (
                    [3, 4],
                    3,
                    [-6.6, -2.6, 0.6, 4.6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
                ([5, 6, 7, 8], 6, [-6.6, -2.6, 2.6, 6.6], {}),
                ([9, 10, 11, 12], 9, [-6.6, -2.6, 2.6, 6.6], {}),
            ]
            for pad_offset, pad_x in zip(
                [num for num in offsets for _ in range(2)]
                if len(offsets) == 2
                else offsets,
                x_positions,
            )
            for pad_base in [32]
        ],
        pad1_square=False,
    )
    for mpn in ["2005062029", "2005062529", "2005062032", "2005062532"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=25.5, width_right=25.5, height_top=28, height_bottom=14
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-23.4, -3.8, 2.9],
            [0, -3.8, 2.9],
            [23.4, -3.8, 2.9],
        ]),
        pad_size=2.1,
        drill_size=1.5,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            PadPosition(
                pad_number=str(pad_base + pad_offset),
                x=pad_x + group_x_shift,
                y=row_y,
                **extra,
            )
            for group_x_shift, pad_base in zip([-11.7, 11.7], [0, 25])
            for offsets, row_y, x_positions, extra in [
                ([1, 2], 0, [-4.6, -0.6, 2.6, 6.6], {}),
                ([3, 4], 3, [-6.6, -2.6, 0.6, 4.6], {}),
                (
                    [5, 6, 7, 8, 9, 10, 11],
                    6,
                    [-6.6, -4.6, -2.6, 0.6, 2.6, 4.6, 6.6],
                    {"pad_size": 1.5, "drill_size": 1.1},
                ),
                (
                    [12, 13, 14, 15, 16, 17, 18],
                    9,
                    [-6.6, -4.6, -2.6, 0.6, 2.6, 4.6, 6.6],
                    {"pad_size": 1.5, "drill_size": 1.1},
                ),
                (
                    [19, 20, 21, 22, 23, 24, 25],
                    12,
                    [-6.6, -4.6, -2.6, 0.6, 2.6, 4.6, 6.6],
                    {"pad_size": 1.5, "drill_size": 1.1},
                ),
            ]
            for pad_offset, pad_x in zip(
                [num for num in offsets for _ in range(2)]
                if len(offsets) == 2
                else offsets,
                x_positions,
            )
        ],
        pad1_square=False,
    )
    for mpn in ["2005062019", "2005062519"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=25.5, width_right=25.5, height_top=28, height_bottom=14
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-23.4, -3.8, 2.9],
            [0, -3.8, 2.9],
            [23.4, -3.8, 2.9],
        ]),
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            # Left side
            PadPosition(
                pad_number=str(pad_num),
                x=pad_x - 11.7,
                y=row_y,
                **extra,
            )
            for pad_nums, row_y, x_positions, extra in [
                (
                    [1, 2],
                    0,
                    [-4.6, -0.6, 2.6, 6.6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
                (
                    [3, 4],
                    3,
                    [-6.6, -2.6, 0.6, 4.6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
                (
                    [5, 6, 7, 8, 9, 10, 11],
                    6,
                    [-6.6, -4.6, -2.6, 0.6, 2.6, 4.6, 6.6],
                    {},
                ),
                (
                    [12, 13, 14, 15, 16, 17, 18],
                    9,
                    [-6.6, -4.6, -2.6, 0.6, 2.6, 4.6, 6.6],
                    {},
                ),
                (
                    [19, 20, 21, 22, 23, 24, 25],
                    12,
                    [-6.6, -4.6, -2.6, 0.6, 2.6, 4.6, 6.6],
                    {},
                ),
            ]
            for pad_num, pad_x in zip(
                [num for num in pad_nums for _ in range(2)]
                if len(pad_nums) == 2
                else pad_nums,
                x_positions,
            )
        ]
        + [
            # Right side
            PadPosition(
                pad_number=str(pad_base + pad_offset),
                x=pad_x + 11.7,
                y=row_y,
                **extra,
            )
            for offsets, row_y, x_positions, extra in [
                ([1, 2, 3, 4, 5, 6, 7], 0, [-6, -4, -2, 0, 2, 4, 6], {}),
                ([8, 9, 10, 11, 12, 13], 3, [-6, -4, -2, 2, 4, 6], {}),
                ([14, 15, 16, 17, 18, 19], 6, [-6, -4, -2, 2, 4, 6], {}),
                (
                    [20, 21, 22, 23],
                    9,
                    [-6, -2, 2, 6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
                (
                    [24, 25, 26, 27],
                    12,
                    [-6, -2, 2, 6],
                    {"pad_size": 2.1, "drill_size": 1.5},
                ),
            ]
            for pad_offset, pad_x in zip(
                [num for num in offsets for _ in range(2)]
                if len(offsets) == 2
                else offsets,
                x_positions,
            )
            for pad_base in [25]
        ],
        pad1_square=False,
    )
    for mpn in ["2005062018", "2005062518"]
}
