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
        part_info.pitch,
        specs.body_dimensions.width_left,
        specs.body_dimensions.width_right,
    )
    width_left = dimensions["width_left"]
    width_right = dimensions["width_right"]
    height_top = specs.body_dimensions.height_top
    height_bottom = specs.body_dimensions.height_bottom

    sections = [
        footprint_utils.generate_header(part_info.mpn),
        footprint_utils.generate_properties(
            specs.ref_y,
            part_info.series,
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
        footprint_utils.generate_pin_1_indicator(width_left, specs.pad_size),
        footprint_utils.generate_pin_1_indicator(
            width_left,
            specs.pad_size,
            layer="F.Fab",
        ),
        footprint_utils.generate_thru_hole_pads(
            part_info.pin_count,
            part_info.pitch,
            specs.pad_size,
            specs.drill_size,
            dimensions["start_pos"],
        ),
        footprint_utils.associate_3d_model(
            "KiCAD_Symbol_Generator/3D_models",
            f"CUI_DEVICES_{part_info.mpn}",
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
