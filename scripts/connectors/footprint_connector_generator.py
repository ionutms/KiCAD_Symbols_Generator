"""KiCad Footprint Generator Module.

Generates standardized KiCad footprint files (.kicad_mod) for various
connector series.
It handles pad placement, silkscreen generation, and 3D model alignment
based on manufacturer specifications.

The module supports multiple connector series with different pin counts and
pitches, generating complete footprint definitions including:
- Through-hole pad layouts
- Silkscreen outlines
- Component identifiers
- 3D model references
"""

from pathlib import Path

import symbol_connectors_specs
from footprint_connector_specs import CONNECTOR_SPECS, FootprintSpecs
from utilities import footprint_utils


def generate_footprint(
    part_info: symbol_connectors_specs.PartInfo,
    specs: FootprintSpecs,
) -> str:
    """Generate complete KiCad footprint file content for a connector.

    Creates all required sections of a .kicad_mod file including component
    outline, pad definitions, text elements, and 3D model references.

    Args:
        part_info: Component specifications (MPN, pin count, pitch)
        specs: Physical specifications for the connector series

    Returns:
        Complete .kicad_mod file content as formatted string

    """
    dimensions = footprint_utils.calculate_dimensions(
        part_info.pin_count,
        specs.pad_pitch,
        specs.body_dimensions.width_left,
        specs.body_dimensions.width_right,
    )
    width_left = dimensions["width_left"]
    width_right = dimensions["width_right"]
    height_top = specs.body_dimensions.height_top
    height_bottom = specs.body_dimensions.height_bottom

    model_file_name = f"{part_info.mpn}"
    footprint_value = part_info.series.replace(
        "xx",
        f"{part_info.pin_count:02d}",
    )

    if part_info.manufacturer == "Same Sky":
        model_file_name = f"CUI_DEVICES_{part_info.mpn}"
        footprint_value = part_info.series

    if part_info.manufacturer == "Keystone Electronics":
        model_file_name = f"{part_info.mpn}"
        footprint_value = part_info.series

    pads = footprint_utils.generate_thru_hole_pads(
        part_info.pin_count,
        specs.pad_pitch,
        specs.pad_size,
        specs.drill_size,
        dimensions["start_pos"],
        row_pitch=specs.row_pitch,
        row_count=specs.number_of_rows,
    )

    f_silk_pin_1_indicator = footprint_utils.generate_pin_1_indicator(
        pad_center_x=width_left,
        pad_width=specs.pad_size,
        pins_per_side=specs.number_of_rows,
        pitch_y=2.54,
        layer="F.SilkS",
    )

    f_fab_pin_1_indicator = footprint_utils.generate_pin_1_indicator(
        pad_center_x=width_left,
        pad_width=specs.pad_size,
        pins_per_side=specs.number_of_rows,
        pitch_y=2.54,
        layer="F.Fab",
    )

    if part_info.series == "CLP-1xx-02-G-D-BE":
        pads = [
            footprint_utils.generate_surface_mount_pads(
                part_info.pin_count,
                specs.pad_pitch,
                specs.pad_size,
                dimensions["start_pos"],
                row_pitch=specs.row_pitch,
                row_count=specs.number_of_rows,
            ),
            footprint_utils.generate_non_plated_through_holes(
                part_info.pin_count,
                specs.pad_pitch,
                specs.non_plated_pad_size,
                specs.non_plated_drill_size,
                dimensions["start_pos"],
                row_pitch=specs.non_plated_row_pitch,
                row_count=specs.number_of_rows,
            ),
        ]
        pads = "".join(pads)

    if specs.mounting_holes is not None:
        for _, mounting_holes_specs in enumerate(specs.mounting_holes.specs):
            pads += footprint_utils.generate_non_plated_through_hole(
                mounting_holes_specs,
            )

    if part_info.series in ("FTSH-1xx-01-L-DV", "FTSH-1xx-01-L-DV-K"):
        pads = [
            footprint_utils.generate_surface_mount_pads(
                part_info.pin_count,
                specs.pad_pitch,
                specs.pad_size,
                dimensions["start_pos"],
                row_pitch=specs.row_pitch,
                row_count=specs.number_of_rows,
                mirror_x_pin_numbering=True,
            ),
        ]
        pads = "".join(pads)
        f_silk_pin_1_indicator = footprint_utils.generate_pin_1_indicator(
            pad_center_x=width_left,
            pad_width=specs.pad_size,
            pins_per_side=specs.number_of_rows,
            pitch_y=2.54,
            layer="F.SilkS",
            mirror_y_coordonate=True,
        )

        f_fab_pin_1_indicator = footprint_utils.generate_pin_1_indicator(
            pad_center_x=width_left,
            pad_width=specs.pad_size,
            pins_per_side=specs.number_of_rows,
            pitch_y=2.54,
            layer="F.Fab",
            mirror_y_coordonate=True,
        )

    if part_info.mounting_style == "Surface Mount":
        pads = [
            footprint_utils.generate_zig_zag_surface_mount_pads(
                part_info.pin_count,
                specs.pad_pitch,
                specs.pad_size,
                dimensions["start_pos"],
                row_pitch=specs.row_pitch,
                row_count=specs.number_of_rows,
                mirror_y_position=specs.miror_zig_zag,
            ),
        ]
        pads = "".join(pads)

    if part_info.series in ("FW-xx-03-G-D-085-315", "FW-xx-03-G-D-085-155"):
        pads = [
            footprint_utils.generate_surface_mount_pads(
                part_info.pin_count,
                specs.pad_pitch,
                specs.pad_size,
                dimensions["start_pos"],
                row_pitch=specs.row_pitch,
                row_count=specs.number_of_rows,
            ),
        ]
        pads = "".join(pads)

    sections = [
        footprint_utils.generate_header(part_info.mpn),
        footprint_utils.generate_properties(
            specs.ref_y,
            footprint_value,
            specs.mpn_y,
        ),
        footprint_utils.generate_courtyard_2(
            width_left,
            width_right,
            height_top,
            height_bottom,
        ),
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
        f_silk_pin_1_indicator,
        f_fab_pin_1_indicator,
        pads,
        footprint_utils.associate_3d_model(
            "KiCAD_Symbol_Generator/3D_models",
            model_file_name,
        ),
        ")",  # Close the footprint
    ]
    return "\n".join(sections)


def generate_footprint_file(
    part_info: symbol_connectors_specs.PartInfo,
    output_path: str,
) -> None:
    """Generate and save a complete .kicad_mod file for a connector.

    Creates a KiCad footprint file in the connector_footprints.pretty
    directory using the specified part information and
    corresponding series specifications.

    Args:
        part_info: Component specifications (MPN, pin count, pitch)
        output_path: Directory path for saving the .kicad_mod file

    Returns:
        None

    """
    specs = CONNECTOR_SPECS[part_info.series]
    footprint_content = generate_footprint(part_info, specs)
    filename = f"{part_info.mpn}.kicad_mod"
    file_path = f"{output_path}/{filename}"

    with Path.open(file_path, "w", encoding="utf-8") as file_handle:
        file_handle.write(footprint_content)
