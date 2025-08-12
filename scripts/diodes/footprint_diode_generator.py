"""KiCad Footprint Generator for Diodes.

Generates standardized KiCad footprint files (.kicad_mod) for diodes
based on manufacturer specifications. Creates accurate footprints with
appropriate pad dimensions, clearances, and silkscreen markings for surface
mount diodes.
"""

from pathlib import Path
from uuid import uuid4

import symbol_diode_specs
from footprint_diode_specs import FOOTPRINTS_SPECS, FootprintSpecs
from utilities import footprint_utils


def generate_footprint(
    part_info: symbol_diode_specs.PartInfo,
    specs: FootprintSpecs,
) -> str:
    """Generate complete KiCad footprint file content for a diode.

    Args:
        part_info: Component specifications including MPN and package type
        specs: FootprintSpecs containing all dimensions for the footprint

    Returns:
        String containing KiCad footprint content for a diode

    """
    body_width = specs.body_dimensions.width
    body_height = specs.body_dimensions.height

    if part_info.package in ("SC_70", "SOT-323"):
        anode_center_x = specs.pad_dimensions.center_x
        cathode_center_x = specs.pad_dimensions.center_x
        anode_width = specs.pad_dimensions.width
        anode_height = specs.pad_dimensions.height

        sections = [
            footprint_utils.generate_header(part_info.package),
            footprint_utils.generate_properties(
                specs.ref_offset_y,
                part_info.package,
            ),
            footprint_utils.generate_courtyard(body_width, body_height),
            footprint_utils.generate_silkscreen_rectangle(
                body_width / 2,
                body_width / 2,
                body_height / 2,
                body_height / 2,
            ),
            generate_zig_zag_pads(specs),
            footprint_utils.associate_3d_model(
                "${KICAD9_3D_MODELS_VAULT}/3D_models/diodes",
                part_info.package,
            ),
            ")",  # Close the footprint
        ]
    elif part_info.package in ("DO-214AA", "SOD323", "SOD_923"):
        anode_center_x = specs.pad_dimensions.anode_center_x
        cathode_center_x = specs.pad_dimensions.cathode_center_x
        anode_width = specs.pad_dimensions.anode_width
        anode_height = specs.pad_dimensions.anode_height

        sections = [
            footprint_utils.generate_header(part_info.package),
            footprint_utils.generate_properties(
                specs.ref_offset_y,
                part_info.package,
            ),
            footprint_utils.generate_courtyard(body_width, body_height),
            footprint_utils.generate_fab_rectangle(body_width, body_height),
            footprint_utils.generate_silkscreen_lines(
                body_height,
                anode_center_x,
                anode_width,
            ),
            generate_pads(specs),
            footprint_utils.associate_3d_model(
                "${KICAD9_3D_MODELS_VAULT}/3D_models/diodes",
                part_info.package,
            ),
            ")",  # Close the footprint
        ]
    else:
        anode_center_x = specs.pad_dimensions.anode_center_x
        cathode_center_x = specs.pad_dimensions.cathode_center_x
        anode_width = specs.pad_dimensions.anode_width
        anode_height = specs.pad_dimensions.anode_height

        sections = [
            footprint_utils.generate_header(part_info.package),
            footprint_utils.generate_properties(
                specs.ref_offset_y,
                part_info.package,
            ),
            footprint_utils.generate_courtyard(body_width, body_height),
            footprint_utils.generate_fab_rectangle(body_width, body_height),
            footprint_utils.generate_fab_diode(
                anode_width,
                anode_height,
                anode_center_x,
                cathode_center_x,
            ),
            footprint_utils.generate_silkscreen_lines(
                body_height,
                anode_center_x,
                anode_width,
            ),
            generate_pads(specs),
            footprint_utils.associate_3d_model(
                "${KICAD9_3D_MODELS_VAULT}/3D_models/diodes",
                part_info.package,
            ),
            ")",  # Close the footprint
        ]

    return "\n".join(sections)


def generate_pads(specs: FootprintSpecs) -> str:
    """Generate the pads section of the footprint with pad dimensions.

    Args:
        specs: FootprintSpecs containing asymmetric pad dimensions

    Returns:
        String containing KiCad footprint pad definitions

    """
    pad_props = specs.pad_dimensions

    # Cathode pad (1)
    cathode = f"""
        (pad "1" smd roundrect
            (at -{pad_props.cathode_center_x} 0)
            (size {pad_props.cathode_width} {pad_props.cathode_height})
            (layers "F.Cu" "F.Paste" "F.Mask")
            (roundrect_rratio {pad_props.roundrect_ratio})
            (uuid "{uuid4()}")
        )
        """

    # Anode pad (2)
    anode = f"""
        (pad "2" smd roundrect
            (at {pad_props.anode_center_x} 0)
            (size {pad_props.anode_width} {pad_props.anode_height})
            (layers "F.Cu" "F.Paste" "F.Mask")
            (roundrect_rratio {pad_props.roundrect_ratio})
            (uuid "{uuid4()}")
        )
        """

    return f"{cathode}\n{anode}"


def generate_x_positions_list(
    center_x: float,
    pin_count: int,
) -> list[float]:
    """Generate a list of X-coordinates for the pads.

    Args:
        center_x: X-coordinate of the center of the pads
        pin_count: Number of pins to generate positions for (odd or even)

    Returns:
        List of X-coordinates for the pads

    """
    half_number = center_x / 2
    if pin_count % 2 == 1:  # Odd pin_count
        return [
            -half_number
            if pin_index < pin_count // 2
            else 0
            if pin_index == pin_count // 2
            else half_number
            for pin_index in range(pin_count)
        ]
    # Even pin_count
    return [
        -half_number if pin_index < pin_count // 2 else half_number
        for pin_index in range(pin_count)
    ]


def generate_y_positions_list(
    center_x: float,
    pin_count: int,
) -> list[float]:
    """Generate a list of Y-coordinates for the pads.

    Args:
        center_x: X-coordinate of the center of the pads
        pin_count: Number of pins to generate positions for (odd or even)

    Returns:
        List of Y-coordinates for the pads

    """
    half_number = center_x / 2
    return [
        (1 if pin_index % 2 == 0 else -1) * half_number
        for pin_index in range(pin_count)
    ]


def generate_pin_numbers(start: int, end: int) -> list[int]:
    """Generate a list of pin numbers in a zig-zag pattern.

    Args:
        start: Starting pin number
        end: Ending pin number

    Returns:
        List of pin numbers in a zig-zag pattern

    """
    original_list = list(range(start, end + 1))
    result = []

    while original_list:
        result.append(original_list.pop(0))
        if original_list:
            result.append(original_list.pop(-1))

    return result


def generate_zig_zag_pads(specs: FootprintSpecs) -> str:
    """Generate the pads section of the footprint with pad dimensions.

    Args:
        specs: FootprintSpecs containing asymmetric pad dimensions

    Returns:
        String containing KiCad footprint pad definitions

    """
    pad_props = specs.pad_dimensions

    pads = []

    x_pos = generate_x_positions_list(pad_props.center_x, specs.pin_count)
    y_pos = generate_y_positions_list(pad_props.center_y, specs.pin_count)
    pin_numbers = generate_pin_numbers(1, specs.pin_count)

    for pin_index, pin_number in enumerate(pin_numbers):
        pad = f"""
            (pad "{pin_number}" smd roundrect
                (at {x_pos[pin_index]} {y_pos[pin_index]})
                (size {pad_props.width} {pad_props.height})
                (layers "F.Cu" "F.Paste" "F.Mask")
                (roundrect_rratio {pad_props.roundrect_ratio})
                (uuid "{uuid4()}")
            )
            """
        pads.append(pad)

    return "\n".join(pads)


def generate_footprint_file(
    part_info: symbol_diode_specs.PartInfo,
    output_path: str,
) -> None:
    """Generate and save a complete .kicad_mod file for a diode.

    Args:
        part_info: Component specifications including MPN and package type
        output_path: Directory to save the generated footprint file

    Returns:
        None

    """
    specs = FOOTPRINTS_SPECS[part_info.package]
    footprint_content = generate_footprint(part_info, specs)
    filename = f"{part_info.package}.kicad_mod"
    file_path = f"{output_path}/{filename}"

    with Path.open(file_path, "w", encoding="utf-8") as file_handle:
        file_handle.write(footprint_content)
