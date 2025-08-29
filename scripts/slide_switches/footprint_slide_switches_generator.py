"""KiCad Footprint Generator Module.

Generates standardized KiCad footprint files (.kicad_mod) for various
slide switch series. Handles pad placement, silkscreen generation, and 3D
model alignment based on manufacturer specifications.

The module supports multiple slide switch series with different pin counts
and pitches, generating complete footprint definitions including:
- Through-hole and surface mount pad layouts
- Silkscreen and fabrication outlines
- Component identifiers and references
- Mounting holes and pads
"""

from pathlib import Path

import symbol_slide_switches_specs as symbol_slide_switches_specs
from footprint_slide_switches_specs import SLIDE_SWITCHES_SPECS
from utilities import footprint_utils


def generate_footprint(part_info, footprint_specs):
    """Generate complete KiCad footprint file content for a slide switch."""
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

    pads = ""

    if part_info.mounting_style == "Through Hole":
        if footprint_specs.pad_properties is not None:
            pads = footprint_utils.generate_custom_thru_hole_pads(
                footprint_specs.pad_properties,
            )
        else:
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
        pads = footprint_utils.generate_zig_zag_surface_mount_pads(
            part_info.pin_count,
            footprint_specs.pad_pitch,
            footprint_specs.pad_size,
            dimensions["start_pos"],
            row_pitch=footprint_specs.row_pitch,
            mirror_y_position=footprint_specs.miror_zig_zag,
        )

    if (
        part_info.mounting_style == "Surface Mount"
        and footprint_specs.number_of_rows == 2
    ):
        pads = footprint_utils.generate_surface_mount_pads(
            part_info.pin_count,
            footprint_specs.pad_pitch,
            footprint_specs.pad_size,
            dimensions["start_pos"],
            row_pitch=footprint_specs.row_pitch,
            row_count=footprint_specs.number_of_rows,
            mirror_x_pin_numbering=footprint_specs.mirror_x_pin_numbering,
            anti_clockwise_numbering=True,
        )

    if footprint_specs.non_plated_round_mounting_holes is not None:
        for (
            mounting_holes_specs
        ) in footprint_specs.non_plated_round_mounting_holes.footprint_specs:
            pads += footprint_utils.generate_non_plated_through_hole(
                mounting_holes_specs,
            )

    if footprint_specs.plated_oval_mounting_holes is not None:
        for (
            mounting_holes_specs
        ) in footprint_specs.plated_oval_mounting_holes.footprint_specs:
            pads += footprint_utils.generate_oval_plated_through_hole(
                mounting_holes_specs,
            )

    if footprint_specs.mounting_pads is not None:
        for mounting_pads in footprint_specs.mounting_pads:
            pads += footprint_utils.generate_mounting_pads(mounting_pads)

    if footprint_specs.non_plated_mounting_holes is not None:
        for mounting_holes in footprint_specs.non_plated_mounting_holes:
            pads += footprint_utils.generate_non_plated_through_hole(
                mounting_holes
            )

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
            "${KICAD9_3D_MODELS_VAULT}/3D_models/slide_switches",
            model_file_name,
        ),
        ")",  # Close the footprint
    ]
    return "\n".join(sections)


def generate_footprint_file(part_info, output_path):
    """Generate and save a complete .kicad_mod file for a slide switch."""
    footprint_name = part_info.footprint.split(":")[-1]
    footprint_specs = SLIDE_SWITCHES_SPECS.get(footprint_name)
    if not footprint_specs:
        raise ValueError(f"No footprint specs found for {footprint_name}")

    footprint_content = generate_footprint(part_info, footprint_specs)
    filename = f"{footprint_name}.kicad_mod"
    file_path = f"{output_path}/{filename}"

    with Path.open(file_path, "w", encoding="utf-8") as file_handle:
        file_handle.write(footprint_content)
