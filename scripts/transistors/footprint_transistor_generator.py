"""KiCad Footprint Generator for Diodes.

Generates standardized KiCad footprint files (.kicad_mod) for diodes
based on manufacturer specifications. Creates accurate footprints with
appropriate pad dimensions, clearances, and silkscreen markings for surface
mount diodes.
"""

from pathlib import Path

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
    pins_per_side = specs.pad_dimensions.pins_per_side
    thermal_pad_width = specs.pad_dimensions.thermal_width
    thermal_pad_height = specs.pad_dimensions.thermal_height
    thermal_pad_center_x = specs.pad_dimensions.thermal_pad_center_x
    thermal_pad_center_y = specs.pad_dimensions.thermal_pad_center_y
    thermal_pad_numbers = specs.pad_dimensions.thermal_pad_numbers
    pad_numbers = specs.pad_dimensions.pad_numbers

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
        footprint_utils.generate_thermal_pad(
            thermal_pad_width,
            thermal_pad_height,
            thermal_pad_center_x,
            thermal_pad_center_y,
            thermal_pad_numbers,
        ),
        footprint_utils.associate_3d_model(
            "KiCAD_Symbol_Generator/3D_models",
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
