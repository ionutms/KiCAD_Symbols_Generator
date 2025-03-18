"""KiCad Footprint Generator for Diodes.

Generates standardized KiCad footprint files (.kicad_mod) for diodes
based on manufacturer specifications. Creates accurate footprints with
appropriate pad dimensions, clearances, and silkscreen markings for surface
mount diodes.
"""

from pathlib import Path
from uuid import uuid4

import symbol_transistor_specs
from footprint_transistor_specs import FOOTPRINTS_SPECS, FootprintSpecs
from utilities import footprint_utils


def generate_footprint(
    part_info: symbol_transistor_specs.PartInfo,
    specs: FootprintSpecs,
) -> str:
    """Generate a complete .kicad_mod file for a diode.

    Args:
        part_info: Component specifications including MPN and package type
        specs: Footprint specifications for the diode package

    Returns:
        A string with the content of the .kicad_mod file for the diode

    """
    body_width = specs.body_dimensions.width
    body_height = specs.body_dimensions.height
    pad_width = specs.pad_dimensions.width
    pad_height = specs.pad_dimensions.height
    pad_center_x = specs.pad_dimensions.pad_center_x
    pad_pitch_y = specs.pad_dimensions.pad_pitch_y

    if part_info.package in ("SOT-323"):
        sections = [
            footprint_utils.generate_header(part_info.package),
            footprint_utils.generate_properties(
                specs.ref_offset_y,
                part_info.package,
            ),
            footprint_utils.generate_courtyard(body_width, body_height),
            footprint_utils.generate_fab_rectangle(body_width, body_height),
            generate_zig_zag_pads(specs),
            footprint_utils.associate_3d_model(
                "${3D_MODELS_VAULT}/3D_models/transistors",
                part_info.package,
            ),
            ")",  # Close the footprint
        ]
    else:
        pins_per_side = specs.pad_dimensions.pins_per_side
        thermal_pad_width = specs.pad_dimensions.thermal_width
        thermal_pad_height = specs.pad_dimensions.thermal_height
        thermal_pad_center_x = specs.pad_dimensions.thermal_pad_center_x
        thermal_pad_center_y = specs.pad_dimensions.thermal_pad_center_y
        thermal_pad_numbers = specs.pad_dimensions.thermal_pad_numbers
        pad_numbers = specs.pad_dimensions.pad_numbers

        thermal_pad = (
            footprint_utils.generate_thermal_pad(
                thermal_pad_width,
                thermal_pad_height,
                thermal_pad_center_x,
                thermal_pad_center_y,
                thermal_pad_numbers,
            )
            if part_info.package not in ("SOT-26")
            else ""
        )
        sections = [
            footprint_utils.generate_header(part_info.package),
            footprint_utils.generate_properties(
                specs.ref_offset_y,
                part_info.package,
            ),
            footprint_utils.generate_courtyard(body_width, body_height),
            footprint_utils.generate_fab_rectangle(body_width, body_height),
            footprint_utils.generate_pads(
                pad_width,
                pad_height,
                pad_center_x,
                pad_pitch_y,
                pins_per_side,
                pad_numbers,
            ),
            thermal_pad,
            footprint_utils.associate_3d_model(
                "${3D_MODELS_VAULT}/3D_models/transistors",
                part_info.package,
            ),
            ")",  # Close the footprint
        ]
    return "\n".join(sections)


def generate_footprint_file(
    part_info: symbol_transistor_specs.PartInfo,
    output_path: str,
) -> None:
    """Generate and save a complete .kicad_mod file for a diode.

    Args:
        part_info: Component specifications including MPN and package type
        output_path: Directory where the .kicad_mod file will be saved

    Returns:
        None

    """
    specs = FOOTPRINTS_SPECS[part_info.package]
    footprint_content = generate_footprint(part_info, specs)
    filename = f"{part_info.package}.kicad_mod"
    file_path = f"{output_path}/{filename}"

    with Path.open(file_path, "w", encoding="utf-8") as file_handle:
        file_handle.write(footprint_content)


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

    x_pos = generate_x_positions_list(pad_props.pad_center_x, specs.pin_count)
    y_pos = generate_y_positions_list(pad_props.pad_pitch_y, specs.pin_count)
    pin_numbers = generate_pin_numbers(1, specs.pin_count)

    for pin_index, pin_number in enumerate(pin_numbers):
        pad = f"""
            (pad "{pin_number}" smd roundrect
                (at {x_pos[pin_index]} {y_pos[pin_index]})
                (size {pad_props.width} {pad_props.height})
                (layers "F.Cu" "F.Paste" "F.Mask")
                (roundrect_rratio 0.25)
                (uuid "{uuid4()}")
            )
            """
        pads.append(pad)

    return "\n".join(pads)
