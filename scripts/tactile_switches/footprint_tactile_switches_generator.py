"""KiCad Footprint Generator Module.

Generates standardized KiCad footprint files (.kicad_mod) for various
tactile switches series.
It handles pad placement, silkscreen generation, and 3D model alignment
based on manufacturer specifications.

The module supports multiple tactile switches series with different pin counts and
pitches, generating complete footprint definitions including:
- Through-hole pad layouts
- Silkscreen outlines
- Component identifiers
- 3D model references
"""

from pathlib import Path

import symbol_tactile_switches_specs as symbol_tactile_switches_specs
from footprint_tactile_switches_specs import (
    CONNECTOR_SPECS,
    FootprintSpecs,
)
from utilities import footprint_utils


def generate_footprint(  # noqa: C901
    part_info: symbol_tactile_switches_specs.PartInfo,
    footprint_specs: FootprintSpecs,
) -> str:
    """Generate complete KiCad footprint file content for a tactile switch.

    Creates all required sections of a .kicad_mod file including component
    outline, pad definitions, text elements, and 3D model references.

    Args:
        part_info: Component specifications (MPN, pin count, pitch)
        footprint_specs: Physical specifications for the tactile switches series

    Returns:
        Complete .kicad_mod file content as formatted string
    """
    dimensions = footprint_utils.calculate_dimensions(
        part_info.pin_count,
        footprint_specs.pad_pitch,
        footprint_specs.body_dimensions.width_left,
        footprint_specs.body_dimensions.width_right,
    )
    width_left = dimensions["width_left"]
    width_right = dimensions["width_right"]
    height_top = footprint_specs.body_dimensions.height_top
    height_bottom = footprint_specs.body_dimensions.height_bottom

    model_file_name = footprint_specs.model_name
    footprint_value = part_info.series

    if part_info.mounting_style == "Through Hole":
        pads = footprint_utils.generate_thru_hole_pads(
            part_info.pin_count,
            footprint_specs.pad_pitch,
            footprint_specs.pad_size,
            footprint_specs.drill_size,
            dimensions["start_pos"],
            row_pitch=footprint_specs.row_pitch,
            row_count=footprint_specs.number_of_rows,
        )

    if (
        part_info.mounting_style == "Surface Mount"
        and footprint_specs.number_of_rows == 1
    ):
        pads = [
            footprint_utils.generate_zig_zag_surface_mount_pads(
                part_info.pin_count,
                footprint_specs.pad_pitch,
                footprint_specs.pad_size,
                dimensions["start_pos"],
                row_pitch=footprint_specs.row_pitch,
                mirror_y_position=footprint_specs.miror_zig_zag,
            ),
        ]
        pads = "".join(pads)

    if (
        part_info.mounting_style == "Surface Mount"
        and footprint_specs.number_of_rows == 2
    ):
        pads = [
            footprint_utils.generate_surface_mount_pads(
                part_info.pin_count,
                footprint_specs.pad_pitch,
                footprint_specs.pad_size,
                dimensions["start_pos"],
                row_pitch=footprint_specs.row_pitch,
                row_count=footprint_specs.number_of_rows,
                mirror_x_pin_numbering=footprint_specs.mirror_x_pin_numbering,
            ),
        ]
        pads = "".join(pads)

    if footprint_specs.non_plated_round_mounting_holes is not None:
        for _, mounting_holes_specs in enumerate(
            footprint_specs.non_plated_round_mounting_holes.footprint_specs,
        ):
            pads += footprint_utils.generate_non_plated_through_hole(
                mounting_holes_specs,
            )

    if footprint_specs.plated_oval_mounting_holes is not None:
        for _, mounting_holes_specs in enumerate(
            footprint_specs.plated_oval_mounting_holes.footprint_specs,
        ):
            pads += footprint_utils.generate_oval_plated_through_hole(
                mounting_holes_specs,
            )

    if footprint_specs.mounting_pads is not None:
        for _, mounting_pads in enumerate(footprint_specs.mounting_pads):
            print(mounting_pads)
            pads += footprint_utils.generate_mounting_pads(mounting_pads)

    second_courtyard = ""
    if footprint_specs.internal_courtyard is not None:
        second_courtyard = footprint_utils.generate_courtyard_2(
            footprint_specs.internal_courtyard.width_left,
            footprint_specs.internal_courtyard.width_right,
            footprint_specs.internal_courtyard.height_top,
            footprint_specs.internal_courtyard.height_bottom,
        )

    if footprint_specs.non_plated_drill_size is not None:
        pads += footprint_utils.generate_non_plated_through_holes(
            part_info.pin_count,
            footprint_specs.pad_pitch,
            footprint_specs.non_plated_pad_size,
            footprint_specs.non_plated_drill_size,
            dimensions["start_pos"],
            row_pitch=footprint_specs.non_plated_row_pitch,
            row_count=footprint_specs.number_of_rows,
        )

    sections = [
        footprint_utils.generate_header(part_info.footprint.split(":")[-1]),
        footprint_utils.generate_properties(
            footprint_specs.ref_y,
            footprint_value,
            footprint_specs.mpn_y,
        ),
        footprint_utils.generate_courtyard_2(
            width_left,
            width_right,
            height_top,
            height_bottom,
        ),
        second_courtyard,
        footprint_utils.generate_silkscreen_rectangle(
            width_left,
            width_right,
            height_top,
            height_bottom,
        ),
        footprint_utils.generate_fabrication_rectangle(
            width_left,
            width_right,
            height_top,
            height_bottom,
        ),
        pads,
        footprint_utils.associate_3d_model(
            "${KICAD9_3D_MODELS_VAULT}/3D_models/tactile_switches",
            model_file_name,
        ),
        ")",  # Close the footprint
    ]
    return "\n".join(sections)


def generate_footprint_file(
    part_info: symbol_tactile_switches_specs.PartInfo,
    output_path: str,
) -> None:
    """Generate and save a complete .kicad_mod file for a tactile switch.

    Creates a KiCad footprint file in the connector_footprints.pretty
    directory using the specified part information and
    corresponding series specifications.

    Args:
        part_info: Component specifications (MPN, pin count, pitch)
        output_path: Directory path for saving the .kicad_mod file

    Returns:
        None
    """
    footprint_name = part_info.footprint.split(":")[-1]
    footprint_specs = CONNECTOR_SPECS.get(footprint_name)
    if not footprint_specs:
        raise ValueError(f"No footprint specs found for {footprint_name}")

    footprint_content = generate_footprint(part_info, footprint_specs)
    filename = f"{footprint_name}.kicad_mod"
    file_path = f"{output_path}/{filename}"

    with Path.open(file_path, "w", encoding="utf-8") as file_handle:
        file_handle.write(footprint_content)
