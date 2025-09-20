"""KiCad Footprint Generator for Power Transformers.

Generates standardized KiCad footprint files (.kicad_mod) for power
transformers based on manufacturer specifications.
Creates accurate footprints with appropriate pad dimensions, clearances, and
silkscreen markings for surface mount power transformers with multiple pins.
"""

from pathlib import Path

import symbol_transformer_specs
from footprint_transformer_specs import (
    FOOTPRINTS_SPECS,
    FootprintSpecs,
)
from utilities import footprint_utils


def generate_footprint(
    part_info: symbol_transformer_specs.PartInfo,
    specs: FootprintSpecs,
) -> str:
    """Generate the content of a .kicad_mod file for a power transformer.

    Args:
        part_info: Information about the part
        specs: Footprint specifications for the part

    Returns:
        The content of the .kicad_mod file as a string

    """
    body_width = specs.body_dimensions.width
    body_height = specs.body_dimensions.height

    if isinstance(specs.pad_dimensions, list):
        # Use custom SMD pad positions and properties
        pads = []
        for pad_property in specs.pad_dimensions:
            pad = f"""
            (pad "{pad_property.name}" smd circle
                (at {pad_property.x} {pad_property.y})
                (size {pad_property.pad_size} {pad_property.pad_size})
                (layers "F.Cu" "F.Paste" "F.Mask")
                (uuid "{footprint_utils.uuid4()}")
            )
            """
            pads.append(pad)
        pads = "\n".join(pads)

        # Extract pin 1 y coordinate for pin 1 indicator
        pin_1_y = None
        # Extract x coordinates for silkscreen lines
        pad_x_coords = []
        for pad_property in specs.pad_dimensions:
            pad_x_coords.append(pad_property.x)
            if pad_property.name == "1":
                pin_1_y = pad_property.y

        pad_center_x = 0
        pad_width = 0
        pad_height = 0
        pad_pitch_y = 0
        pins_per_side = 0
        reverse_pin_numbering = False
    else:
        pad_center_x = specs.pad_dimensions.center_x
        pad_width = specs.pad_dimensions.width
        pad_height = specs.pad_dimensions.height
        pad_pitch_y = specs.pad_dimensions.pitch_y
        pins_per_side = specs.pad_dimensions.pin_count // 2
        reverse_pin_numbering = specs.pad_dimensions.reverse_pin_numbering
        pin_1_y = None  # Not needed for standard pads
        pad_x_coords = None  # Not needed for standard pads

        pads = footprint_utils.generate_pads(
            pad_width,
            pad_height,
            pad_center_x,
            pad_pitch_y,
            pins_per_side,
            reverse_pin_numbering=reverse_pin_numbering,
        )

    sections = [
        footprint_utils.generate_header(part_info.series),
        footprint_utils.generate_properties(
            specs.ref_offset_y,
            part_info.series,
        ),
        footprint_utils.generate_courtyard(body_width, body_height),
        footprint_utils.generate_fab_rectangle(body_width, body_height),
        footprint_utils.generate_silkscreen_lines(
            body_height,
            pad_center_x,
            pad_width,
            pad_x_coords,  # Pass custom pad x coordinates
        ),
        footprint_utils.generate_pin_1_indicator(
            body_width=body_width,
            pins_per_side=pins_per_side,
            pitch_y=pad_pitch_y,
            mirror_x_coordonate=reverse_pin_numbering,
            custom_pin_1_y=pin_1_y,  # Pass the custom pin 1 y coordinate
        ),
        pads,
        footprint_utils.associate_3d_model(
            "${KICAD9_3D_MODELS_VAULT}/3D_models/transformers",
            part_info.series,
        ),
        ")",  # Close the footprint
    ]
    return "\n".join(sections)


def generate_footprint_file(
    part_info: symbol_transformer_specs.PartInfo,
    output_path: str,
) -> None:
    """Generate and save a complete .kicad_mod file.

    Args:
        part_info: Information about the part
        output_path: The directory to save the file in

    Returns:
        None

    """
    specs = FOOTPRINTS_SPECS[part_info.series]

    footprint_content = generate_footprint(part_info, specs)
    filename = f"{part_info.series}.kicad_mod"
    file_path = f"{output_path}/{filename}"

    with Path.open(file_path, "w", encoding="utf-8") as file_handle:
        file_handle.write(footprint_content)
