"""KiCad Footprint Generator Module for Terminal Blocks.

Generates standardized KiCad footprint files (.kicad_mod) for various
terminal block series.
It handles pad placement, silkscreen generation, and 3D model alignment
based on manufacturer specifications.

The module supports multiple terminal block series with different pin counts
and pitches, generating complete footprint definitions including:
- Through-hole pad layouts
- Silkscreen outlines
- Component identifiers
- 3D model references
"""

from pathlib import Path

import symbol_terminal_block_specs
from footprint_terminal_block_specs import CONNECTOR_SPECS, FootprintSpecs
from utilities import footprint_utils


def generate_footprint(
    part_info: symbol_terminal_block_specs.PartInfo,
    footprint_specs: FootprintSpecs,
) -> str:
    """Generate complete KiCad footprint file content for a terminal block.

    Creates all required sections of a .kicad_mod file including component
    outline, pad definitions, text elements, and 3D model references.

    Args:
        part_info: Component specifications (MPN, pin count, pitch)
        footprint_specs: Physical specifications for the terminal block series

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

    model_file_name = f"{part_info.mpn}"
    footprint_value = part_info.series.replace(
        "xx",
        f"{part_info.pin_count:02d}",
    )

    if part_info.manufacturer == "Same Sky":
        footprint_value = part_info.series

    if part_info.manufacturer == "Amphenol Anytek":
        footprint_value = part_info.series

    # Prepare custom pin numbering from pin_names if provided
    series_spec = symbol_terminal_block_specs.SYMBOLS_SPECS[part_info.series]
    custom_pin_numbers: list[int] | None = None
    if series_spec.pin_names:
        keys = list(series_spec.pin_names.keys())
        total_pins = part_info.pin_count * footprint_specs.number_of_rows
        # Use provided order whenever possible
        if len(keys) == total_pins:
            if footprint_specs.number_of_rows == 1:
                custom_pin_numbers = keys
            else:
                pins_per_side = part_info.pin_count
                left_group = keys[:pins_per_side]
                right_group = keys[pins_per_side:]
                custom_pin_numbers = []
                for index in range(pins_per_side):
                    custom_pin_numbers.append(left_group[index])
                    custom_pin_numbers.append(right_group[-1 - index])
        else:
            # Fallback to sequential numbering logic if counts don't align
            custom_pin_numbers = None

    sections = [
        footprint_utils.generate_header(part_info.mpn),
        footprint_utils.generate_properties(
            footprint_specs.ref_y,
            footprint_value,
            footprint_specs.mpn_y,
        ),
        footprint_utils.generate_user_comment_courtyard(
            width_left,
            width_right,
            height_top,
            height_bottom,
        ),
        footprint_utils.associate_3d_model(
            "${KICAD9_3D_MODELS_VAULT}/3D_models/terminal_blocks",
            model_file_name,
        ),
        ")",  # Close the footprint
    ]
    return "\n".join(sections)


def generate_footprint_file(
    part_info: symbol_terminal_block_specs.PartInfo,
    output_path: str,
) -> None:
    """Generate and save a complete .kicad_mod file for a terminal block.

    Creates a KiCad footprint file in the terminal_block_footprints.pretty
    directory using the specified part information and
    corresponding series specifications.

    Args:
        part_info: Component specifications (MPN, pin count, pitch)
        output_path: Directory path for saving the .kicad_mod file

    Returns:
        None

    """
    footprint_specs = CONNECTOR_SPECS[part_info.series]
    footprint_content = generate_footprint(part_info, footprint_specs)
    filename = f"{part_info.mpn}.kicad_mod"
    file_path = f"{output_path}/{filename}"

    with Path.open(file_path, "w", encoding="utf-8") as file_handle:
        file_handle.write(footprint_content)
