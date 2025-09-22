"""KiCad Footprint Generator for Power Inductors.

Generates standardized KiCad footprint files (.kicad_mod) for power inductors
based on manufacturer specifications. Creates accurate footprints with
appropriate pad dimensions, clearances, and silkscreen markings for surface
mount power inductors.
"""

from pathlib import Path

import symbol_inductors_specs
from footprint_inductor_specs import FOOTPRINTS_SPECS, FootprintSpecs
from utilities import footprint_utils


def generate_footprint(
    part_info: symbol_inductors_specs.PartInfo,
    specs: FootprintSpecs,
) -> str:
    """Generate complete KiCad footprint file content for an inductor.

    Args:
        part_info: Component specifications
        specs: Footprint specifications for the component series

    Returns:
        str: Complete content of the .kicad_mod file for the inductor

    """
    body_width = specs.body_dimensions.width
    body_height = specs.body_dimensions.height

    pad_center_x = specs.pad_dimensions.center_x
    pad_width = specs.pad_dimensions.width
    pad_height = specs.pad_dimensions.height

    add_pin_1_indicator = (
        footprint_utils.generate_pin_1_indicator(
            body_width,
            pad_width,
        )
        if specs.enable_pin_1_indicator
        else ""
    )

    footprint_name = part_info.footprint.split(":")[1]

    sections = [
        footprint_utils.generate_header(footprint_name),
        footprint_utils.generate_properties(
            specs.ref_offset_y,
            footprint_name,
        ),
        footprint_utils.generate_courtyard(body_width, body_height),
        footprint_utils.generate_fab_rectangle(body_width, body_height),
        footprint_utils.generate_silkscreen_lines(
            body_height,
            pad_center_x,
            pad_width,
        ),
        add_pin_1_indicator,
        footprint_utils.generate_pads(pad_width, pad_height, pad_center_x),
        footprint_utils.associate_3d_model(
            "${KICAD9_3D_MODELS_VAULT}/3D_models/inductors",
            footprint_name,
        ),
        ")",  # Close the footprint
    ]
    return "\n".join(sections)


def generate_footprint_file(
    part_info: symbol_inductors_specs.PartInfo,
    output_path: str,
) -> None:
    """Generate and save a complete .kicad_mod file for an inductor.

    Args:
        part_info: Component specifications
        output_path: Directory path to save the generated file

    Returns:
        None

    """
    footprint_name = part_info.footprint.split(":")[1]
    specs = FOOTPRINTS_SPECS[footprint_name]
    footprint_content = generate_footprint(part_info, specs)

    filename = f"{footprint_name}.kicad_mod"
    file_path = f"{output_path}/{filename}"

    with Path.open(file_path, "w", encoding="utf-8") as file_handle:
        file_handle.write(footprint_content)
