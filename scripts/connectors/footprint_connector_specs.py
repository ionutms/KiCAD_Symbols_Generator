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


def make_pad_group(
    rows: list[tuple],
    pad_base: int,
    x_offset: float = 0.0,
) -> list[PadPosition]:
    """Generate a list of PadPositions for a single connector group.

    Each row in `rows` describes one horizontal band of pads.
    Rows with exactly 2 pad offsets are expanded so that each offset maps
    to 2 x-positions (i.e. each logical pin occupies two physical pads);
    rows with more offsets are mapped one-to-one.

    Args:
        rows: List of (pad_offsets, row_y, xpositions, extra) tuples where:
            - pad_offsets: pad numbers relative to pad_base for this row.
            - row_y: Y coordinate shared by all pads in the row.
            - xpositions: X coordinates, one per pad after offset expansion.
            - extra:
                additional kwargs forwarded to PadPosition
                (e.g. pad_size, drill_size);
                pass {} to use footprint defaults.
        pad_base:
            Added to every pad_offset to produce the absolute pad number.
        x_offset: Shifts all pads horizontally, used to position the group
            (left, center, or right) within the footprint.

    Returns:
        Flat list of PadPosition instances for all pads in the group.

    """
    return [
        PadPosition(
            pad_number=str(pad_base + pad_offset),
            x=pad_x + x_offset,
            y=row_y,
            **extra,
        )
        for pad_offsets, row_y, xpositions, extra in rows
        for pad_offset, pad_x in zip(
            [num for num in pad_offsets for _ in range(2)]
            if len(pad_offsets) == 2
            else pad_offsets,
            xpositions,
        )
    ]


PADS_25_4PWR = [
    ([1, 2], 0, [-4.6, -0.6, 2.6, 6.6], {"pad_size": 2.1, "drill_size": 1.5}),
    ([3, 4], 3, [-6.6, -2.6, 0.6, 4.6], {"pad_size": 2.1, "drill_size": 1.5}),
    ([5, 6, 7, 8, 9, 10, 11], 6, [-6.6, -4.6, -2.6, 0.6, 2.6, 4.5, 6.6], {}),
    (
        [12, 13, 14, 15, 16, 17, 18],
        9,
        [-6.6, -4.6, -2.6, 0.6, 2.6, 4.5, 6.6],
        {},
    ),
    (
        [19, 20, 21, 22, 23, 24, 25],
        12,
        [-6.6, -4.6, -2.6, 0.6, 2.6, 4.5, 6.6],
        {},
    ),
]

PADS_32_4PWR = [
    ([1, 2, 3, 4, 5, 6, 7], 0, [-6.6, -4.6, -2.6, 0.6, 2.6, 4.6, 6.6], {}),
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

PADS_28_7PWR = [
    ([1, 2, 3, 4, 5, 6, 7], 0, [-6, -4, -2, 0, 2, 4, 6], {}),
    ([8, 9, 10, 11, 12, 13, 14], 3, [-6, -4, -2, 0, 2, 4, 6], {}),
    ([15, 16, 17, 18, 19, 20, 21], 6, [-6, -4, -2, 0, 2, 4, 6], {}),
    ([22, 23, 24], 9, [-6, 2, 6], {"pad_size": 2.1, "drill_size": 1.5}),
    (
        [25, 26, 27, 28],
        12,
        [-6, -2, 2, 6],
        {"pad_size": 2.1, "drill_size": 1.5},
    ),
]

PADS_12_4PWR = [
    ([1, 2], 0, [-4.6, -0.6, 2.6, 6.6], {"pad_size": 2.1, "drill_size": 1.5}),
    ([3, 4], 3, [-6.6, -2.6, 0.6, 4.6], {"pad_size": 2.1, "drill_size": 1.5}),
    ([5, 6, 7, 8], 6, [-6.6, -2.6, 2.6, 6.6], {}),
    ([9, 10, 11, 12], 9, [-6.6, -2.6, 2.6, 6.6], {}),
]


PADS_27_8PWR = [
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


PADS_23_2PWR = [
    ([1, 2, 3, 4, 5, 6, 7], 0, [-6, -4, -2, 0, 2, 4, 6], {}),
    ([8, 9, 10, 11, 12, 13, 14], 3, [-6, -4, -2, 0, 2, 4, 6], {}),
    ([15, 16, 17, 18, 19, 20, 21], 6, [-6, -4, -2, 0, 2, 4, 6], {}),
    (
        [22, 22, 22, 23, 23, 23],
        9.67,
        [-7.08, -4.54, -2, 0.92, 3.46, 6],
        {"pad_size": 2.1, "drill_size": 1.5},
    ),
]


PADS_18_4PWR = [
    (
        [1, 2, 3, 4, 5, 6, 7],
        0,
        [-15.74, -13.74, -11.74, -9.74, -7.74, -5.74, -3.74],
        {},
    ),
    (
        [8, 9, 10, 11, 12, 13, 14],
        6,
        [-15.74, -13.74, -11.74, -9.74, -7.74, -5.74, -3.74],
        {},
    ),
    (
        [15, 16, 17, 18],
        12,
        [-15.74, -11.74, -7.74, -3.74],
        {"pad_size": 2.1, "drill_size": 1.5},
    ),
]


PADS_14_7PWR = [
    (
        [1, 2, 3, 4, 5, 6, 7],
        0,
        [3.74, 5.74, 7.74, 9.74, 11.74, 13.74, 15.74],
        {},
    ),
    (
        [8, 9, 10],
        9,
        [3.74, 11.74, 15.74],
        {"pad_size": 2.1, "drill_size": 1.5},
    ),
    (
        [11, 12, 13, 14],
        12,
        [3.74, 7.74, 11.74, 15.74],
        {"pad_size": 2.1, "drill_size": 1.5},
    ),
]


PADS_28_7PWR_S_L = [
    (
        [1, 2, 3, 4, 5, 6, 7],
        0,
        [-15.74, -13.74, -11.74, -9.74, -7.74, -5.74, -3.74],
        {},
    ),
    (
        [8, 9, 10, 11, 12, 13, 14],
        3,
        [-15.74, -13.74, -11.74, -9.74, -7.74, -5.74, -3.74],
        {},
    ),
    (
        [15, 16, 17, 18, 19, 20, 21],
        6,
        [-15.74, -13.74, -11.74, -9.74, -7.74, -5.74, -3.74],
        {},
    ),
    (
        [22, 23, 24],
        9,
        [-15.74, -7.74, -3.74],
        {"pad_size": 2.1, "drill_size": 1.5},
    ),
    (
        [25, 26, 27, 28],
        12,
        [-15.74, -11.74, -7.74, -3.74],
        {"pad_size": 2.1, "drill_size": 1.5},
    ),
]

PADS_28_7PWR_S_R = [
    (
        [1, 2, 3, 4, 5, 6, 7],
        0,
        [3.74, 5.74, 7.74, 9.74, 11.74, 13.74, 15.74],
        {},
    ),
    (
        [8, 9, 10, 11, 12, 13, 14],
        3,
        [3.74, 5.74, 7.74, 9.74, 11.74, 13.74, 15.74],
        {},
    ),
    (
        [15, 16, 17, 18, 19, 20, 21],
        6,
        [3.74, 5.74, 7.74, 9.74, 11.74, 13.74, 15.74],
        {},
    ),
    (
        [22, 23, 24],
        9,
        [3.74, 11.74, 15.74],
        {"pad_size": 2.1, "drill_size": 1.5},
    ),
    (
        [25, 26, 27, 28],
        12,
        [3.74, 7.74, 11.74, 15.74],
        {"pad_size": 2.1, "drill_size": 1.5},
    ),
]


PADS_8 = [
    ([1, 2, 3, 4], 0, [-1.27 * 3, -1.27, 1.27, 1.27 * 3], {}),
    ([5, 6, 7, 8], 2.54, [-1.27 * 3, -1.27, 1.27, 1.27 * 3], {}),
]


PADS_10_4PWR = [
    (
        [7, 7, 8, 8, 9, 9, 10, 10],
        0,
        [-9.025, -6.725, -3.775, -1.475, 1.475, 3.775, 6.725, 9.025],
        {},
    ),
    (
        [1, 2, 3, 4, 5, 6],
        3.2,
        [-8.75, -5.25, -1.75, 1.75, 5.25, 8.75],
        {},
    ),
]


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
            *make_pad_group(PADS_28_7PWR_S_L, pad_base=0, x_offset=0.0),
            *make_pad_group(PADS_28_7PWR_S_R, pad_base=28, x_offset=0.0),
        ],
        pad1_square=False,
    )
    for mpn in [
        *["1600130623", "1600130641", "1600132623", "1600132641"],
        *["1600133623", "1600133641", "1600133724", "1600133741"],
        *["1600133841", "1600133941", "1600134141", "1600134623"],
        *["1600134641"],
    ]
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
            *make_pad_group(PADS_18_4PWR, pad_base=0, x_offset=0.0),
            *make_pad_group(PADS_14_7PWR, pad_base=18, x_offset=0.0),
        ],
        pad1_square=False,
    )
    for mpn in ["1600131624"]
}

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
            *make_pad_group(PADS_28_7PWR, pad_base=0, x_offset=0.0),
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
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            *make_pad_group(PADS_12_4PWR, pad_base=0, x_offset=0.0),
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
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            *make_pad_group(PADS_25_4PWR, pad_base=0, x_offset=0.0),
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
            *make_pad_group(PADS_27_8PWR, pad_base=0, x_offset=0.0),
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
            *make_pad_group(PADS_28_7PWR, pad_base=0, x_offset=0.0),
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
            *make_pad_group(PADS_32_4PWR, pad_base=0, x_offset=0.0),
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
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            *make_pad_group(PADS_12_4PWR, pad_base=0, x_offset=0.0),
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
            *make_pad_group(PADS_23_2PWR, pad_base=0, x_offset=0.0),
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
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            *make_pad_group(PADS_25_4PWR, pad_base=0, x_offset=0.0),
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
            *make_pad_group(PADS_27_8PWR, pad_base=0, x_offset=0.0),
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
            *make_pad_group(PADS_28_7PWR, pad_base=0, x_offset=0.0),
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
            *make_pad_group(PADS_32_4PWR, pad_base=0, x_offset=0.0),
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
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            *make_pad_group(PADS_12_4PWR, pad_base=0, x_offset=-11.7),
            *make_pad_group(PADS_12_4PWR, pad_base=12, x_offset=11.7),
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
            *make_pad_group(PADS_12_4PWR, pad_base=0, x_offset=-11.7),
            *make_pad_group(PADS_23_2PWR, pad_base=12, x_offset=11.7),
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
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            *make_pad_group(PADS_12_4PWR, pad_base=0, x_offset=-23.4),
            *make_pad_group(PADS_12_4PWR, pad_base=12, x_offset=0.0),
            *make_pad_group(PADS_12_4PWR, pad_base=24, x_offset=23.4),
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
            *make_pad_group(PADS_12_4PWR, pad_base=0, x_offset=-11.7),
            *make_pad_group(PADS_25_4PWR, pad_base=12, x_offset=11.7),
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
            *make_pad_group(PADS_27_8PWR, pad_base=0, x_offset=-11.7),
            *make_pad_group(PADS_12_4PWR, pad_base=27, x_offset=11.7),
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
            *make_pad_group(PADS_12_4PWR, pad_base=0, x_offset=-11.7),
            *make_pad_group(PADS_27_8PWR, pad_base=12, x_offset=11.7),
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
            *make_pad_group(PADS_12_4PWR, pad_base=0, x_offset=-11.7),
            *make_pad_group(PADS_32_4PWR, pad_base=12, x_offset=11.7),
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
            *make_pad_group(PADS_32_4PWR, pad_base=0, x_offset=-11.7),
            *make_pad_group(PADS_12_4PWR, pad_base=32, x_offset=11.7),
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
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            *make_pad_group(PADS_25_4PWR, pad_base=0, x_offset=-11.7),
            *make_pad_group(PADS_25_4PWR, pad_base=25, x_offset=11.7),
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
            *make_pad_group(PADS_25_4PWR, pad_base=0, x_offset=-11.7),
            *make_pad_group(PADS_27_8PWR, pad_base=25, x_offset=11.7),
        ],
        pad1_square=False,
    )
    for mpn in ["2005062018", "2005062518"]
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
            *make_pad_group(PADS_25_4PWR, pad_base=0, x_offset=-11.7),
            *make_pad_group(PADS_28_7PWR, pad_base=25, x_offset=11.7),
        ],
        pad1_square=False,
    )
    for mpn in ["2005062004", "2005062504", "2005062027", "2005062527"]
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
            *make_pad_group(PADS_27_8PWR, pad_base=0, x_offset=-11.7),
            *make_pad_group(PADS_27_8PWR, pad_base=27, x_offset=11.7),
        ],
        pad1_square=False,
    )
    for mpn in ["2005062011", "2005062511"]
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
            *make_pad_group(PADS_28_7PWR, pad_base=0, x_offset=-11.7),
            *make_pad_group(PADS_28_7PWR, pad_base=28, x_offset=11.7),
        ],
        pad1_square=False,
    )
    for mpn in ["2005062009", "2005062509", "2005062034", "2005062534"]
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
            *make_pad_group(PADS_32_4PWR, pad_base=0, x_offset=-11.7),
            *make_pad_group(PADS_25_4PWR, pad_base=32, x_offset=11.7),
        ],
        pad1_square=False,
    )
    for mpn in ["2005062017", "2005062517", "2005062021", "2005062024"]
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
            *make_pad_group(PADS_25_4PWR, pad_base=0, x_offset=-11.7),
            *make_pad_group(PADS_32_4PWR, pad_base=25, x_offset=11.7),
        ],
        pad1_square=False,
    )
    for mpn in ["2005062022", "2005062522"]
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
            *make_pad_group(PADS_28_7PWR, pad_base=0, x_offset=-11.7),
            *make_pad_group(PADS_32_4PWR, pad_base=28, x_offset=11.7),
        ],
        pad1_square=False,
    )
    for mpn in ["2005062020", "2005062520"]
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
            *make_pad_group(PADS_32_4PWR, pad_base=0, x_offset=-11.7),
            *make_pad_group(PADS_28_7PWR, pad_base=32, x_offset=11.7),
        ],
        pad1_square=False,
    )
    for mpn in ["2005062028", "2005062528"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=36.5,
            width_right=36.5,
            height_top=28,
            height_bottom=14,
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-35.1, -3.8, 2.9],
            [-11.7, -3.8, 2.9],
            [11.7, -3.8, 2.9],
            [35.1, -3.8, 2.9],
        ]),
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            *make_pad_group(PADS_25_4PWR, pad_base=0, x_offset=-23.4),
            *make_pad_group(PADS_25_4PWR, pad_base=25, x_offset=0.0),
            *make_pad_group(PADS_12_4PWR, pad_base=50, x_offset=23.4),
        ],
        pad1_square=False,
    )
    for mpn in ["2005063017", "2005063517"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=36.5,
            width_right=36.5,
            height_top=28,
            height_bottom=14,
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-35.1, -3.8, 2.9],
            [-11.7, -3.8, 2.9],
            [11.7, -3.8, 2.9],
            [35.1, -3.8, 2.9],
        ]),
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            *make_pad_group(PADS_12_4PWR, pad_base=0, x_offset=-23.4),
            *make_pad_group(PADS_25_4PWR, pad_base=12, x_offset=0.0),
            *make_pad_group(PADS_25_4PWR, pad_base=37, x_offset=23.4),
        ],
        pad1_square=False,
    )
    for mpn in ["2005063018", "2005063518"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=25.5,
            width_right=25.5,
            height_top=28,
            height_bottom=14,
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
            *make_pad_group(PADS_32_4PWR, pad_base=0, x_offset=-11.7),
            *make_pad_group(PADS_32_4PWR, pad_base=32, x_offset=11.7),
        ],
        pad1_square=False,
    )
    for mpn in [
        *["2005062008", "2005062026", "2005062013", "2005062513"],
        *["2005062014", "2005062514", "2005062033", "2005062533"],
    ]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=36.5,
            width_right=36.5,
            height_top=28,
            height_bottom=14,
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-35.1, -3.8, 2.9],
            [-11.7, -3.8, 2.9],
            [11.7, -3.8, 2.9],
            [35.1, -3.8, 2.9],
        ]),
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            *make_pad_group(PADS_32_4PWR, pad_base=0, x_offset=-23.4),
            *make_pad_group(PADS_25_4PWR, pad_base=32, x_offset=0.0),
            *make_pad_group(PADS_12_4PWR, pad_base=57, x_offset=23.4),
        ],
        pad1_square=False,
    )
    for mpn in ["2005063009", "2005063509"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=36.5,
            width_right=36.5,
            height_top=28,
            height_bottom=14,
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-35.1, -3.8, 2.9],
            [-11.7, -3.8, 2.9],
            [11.7, -3.8, 2.9],
            [35.1, -3.8, 2.9],
        ]),
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            *make_pad_group(PADS_12_4PWR, pad_base=0, x_offset=-23.4),
            *make_pad_group(PADS_27_8PWR, pad_base=12, x_offset=0.0),
            *make_pad_group(PADS_32_4PWR, pad_base=39, x_offset=23.4),
        ],
        pad1_square=False,
    )
    for mpn in ["2005063015", "2005063515"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=36.5,
            width_right=36.5,
            height_top=28,
            height_bottom=14,
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-35.1, -3.8, 2.9],
            [-11.7, -3.8, 2.9],
            [11.7, -3.8, 2.9],
            [35.1, -3.8, 2.9],
        ]),
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            *make_pad_group(PADS_32_4PWR, pad_base=0, x_offset=-23.4),
            *make_pad_group(PADS_28_7PWR, pad_base=32, x_offset=0.0),
            *make_pad_group(PADS_12_4PWR, pad_base=60, x_offset=23.4),
        ],
        pad1_square=False,
    )
    for mpn in ["2005063020", "2005063520"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=36.5,
            width_right=36.5,
            height_top=28,
            height_bottom=14,
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-35.1, -3.8, 2.9],
            [-11.7, -3.8, 2.9],
            [11.7, -3.8, 2.9],
            [35.1, -3.8, 2.9],
        ]),
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            *make_pad_group(PADS_32_4PWR, pad_base=0, x_offset=-23.4),
            *make_pad_group(PADS_25_4PWR, pad_base=32, x_offset=0),
            *make_pad_group(PADS_25_4PWR, pad_base=57, x_offset=23.4),
        ],
        pad1_square=False,
    )
    for mpn in ["2005063003", "2005063503"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=36.5,
            width_right=36.5,
            height_top=28,
            height_bottom=14,
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-35.1, -3.8, 2.9],
            [-11.7, -3.8, 2.9],
            [11.7, -3.8, 2.9],
            [35.1, -3.8, 2.9],
        ]),
        pad_size=1.5,
        drill_size=1.1,
        mpn_y=-30.48,
        ref_y=14.986,
        pad_positions_override=[
            *make_pad_group(PADS_25_4PWR, pad_base=0, x_offset=-23.4),
            *make_pad_group(PADS_25_4PWR, pad_base=25, x_offset=0.0),
            *make_pad_group(PADS_32_4PWR, pad_base=50, x_offset=23.4),
        ],
        pad1_square=False,
    )
    for mpn in ["2005063011", "2005063511"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=9.6,
            width_right=9.6,
            height_top=31,
            height_bottom=5,
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-1.27 * 5, 1.27, 3.05],
            [1.27 * 5, 1.27, 3.05],
        ]),
        pad_size=1.6,
        drill_size=1.2,
        mpn_y=-33.274,
        ref_y=5.842,
        pad_positions_override=[
            *make_pad_group(PADS_8, pad_base=0, x_offset=0.0),
        ],
        pad1_square=False,
    )
    for mpn in ["346910080"]
}

CONNECTOR_SPECS |= {
    mpn: FootprintSpecs(
        show_pin1_indicator=False,
        pad_pitch=3.54,
        body_dimensions=BodyDimensions(
            width_left=17.1,
            width_right=17.1,
            height_top=31,
            height_bottom=5,
        ),
        non_plated_round_mounting_holes=NonPlatedRoundMountingHoles([
            [-13.97, 1.27, 3.05],
            [13.97, 1.27, 3.05],
        ]),
        pad_size=1.9,
        drill_size=1.48,
        mpn_y=-33.274,
        ref_y=5.842,
        pad_positions_override=[
            *make_pad_group(PADS_10_4PWR, pad_base=0, x_offset=0.0),
        ],
        pad1_square=False,
    )
    for mpn in ["346960100"]
}
