"""KiCad Footprint Generator for Surface Mount and Radial Capacitors.

Generates standardized KiCad footprint files (.kicad_mod) for both surface
mount and radial capacitors. Uses manufacturer specifications to create
accurate footprints with appropriate pad dimensions and clearances.
"""

from pathlib import Path

from footprint_capacitor_specs import (
    AdditionalPad,
    FOOTPRINTS_SPECS,
    FootprintSpecs,
    RadialFootprintSpecs,
)
from symbol_capacitors_specs import SERIES_SPECS, SeriesSpec
from utilities import footprint_utils


def generate_radial_footprint(
    series_spec: SeriesSpec,
    capacitor_specs: RadialFootprintSpecs,
    case_code_in: str | None = None,
    case_code_mm: str | None = None,
    step_file_name: str | None = None,
) -> str:
    """Generate complete KiCad footprint file content for a radial capacitor.

    Args:
        series_spec: Series specifications from SERIES_SPECS
        capacitor_specs: Physical specifications from RADIAL_FOOTPRINTS_SPECS
        case_code_in: Optional case code to override the series default
        case_code_mm: Optional case code mm to override the series default
        step_file_name: Optional 3D model name to override the default

    Returns:
        Complete .kicad_mod file content as formatted string

    """
    case_in: str = case_code_in if case_code_in else series_spec.case_code_in
    case_mm: str = case_code_mm if case_code_mm else series_spec.case_code_mm
    footprint_name: str = f"C_{case_in}_{case_mm}Metric"
    step_file_name_final: str = (
        step_file_name if step_file_name else f"C_{case_in}"
    )

    body_diameter: float = capacitor_specs.body_dimensions.diameter

    pad_diameter: float = capacitor_specs.pad_dimensions.pad_diameter
    drill_size: float = capacitor_specs.pad_dimensions.drill_size
    pad_distance: float = capacitor_specs.pad_dimensions.pad_distance
    additional_pads: list = capacitor_specs.pad_dimensions.additional_pads or []

    # Calculate position for plus sign outside the circular body
    plus_pos_x = -body_diameter / 2 - 0.75

    # Generate radial footprint sections
    sections: list[str] = [
        footprint_utils.generate_header(footprint_name),
        footprint_utils.generate_properties(
            capacitor_specs.ref_offset_y,
            footprint_name,
        ),
        # Generate circular courtyard
        footprint_utils.generate_circular_courtyard(body_diameter),
        # Generate circular fabrication layer
        footprint_utils.generate_circular_fab(body_diameter),
        # Generate circular silkscreen
        footprint_utils.generate_circular_silkscreen(body_diameter),
        # Add plus sign for pad 1 on silkscreen (outside courtyard)
        footprint_utils.generate_plus_sign_silkscreen(plus_pos_x, 0),
        # Add plus sign for pad 1 on fab layer (outside courtyard)
        footprint_utils.generate_plus_sign_fab(plus_pos_x, 0),
        # Generate through-hole pads for radial capacitor
        footprint_utils.generate_thru_hole_pads(
            pin_count=2,
            pad_pitch=pad_distance * 2,
            pad_size=pad_diameter,
            drill_size=drill_size,
            start_pos=-pad_distance,
            row_pitch=0,
            row_count=1,
            pin_numbers=["1", "2"],
        ),
    ]

    # Add additional pads if specified
    if additional_pads:
        # Import here to avoid circular imports
        from typing import NamedTuple

        # Create a temporary NamedTuple class to match the expected format
        class PadProperty(NamedTuple):
            name: str
            x: float
            y: float
            pad_size: float
            drill_size: float

        # Convert additional pads to the format expected by generate_custom_thru_hole_pads
        pad_properties = [
            PadProperty(
                name=pad.name,
                x=pad.x,
                y=pad.y,
                pad_size=pad.pad_diameter,
                drill_size=pad.drill_size
            )
            for pad in additional_pads
        ]

        additional_pads_section = footprint_utils.generate_custom_thru_hole_pads(pad_properties)
        sections.insert(-2, additional_pads_section)  # Insert before the 3D model section

    sections.extend([
        footprint_utils.associate_3d_model(
            "${KICAD9_3D_MODELS_VAULT}/3D_models/capacitors",
            step_file_name_final,
        ),
        ")",  # Close the footprint
    ])

    return "\n".join(sections)


def generate_footprint(
    series_spec: SeriesSpec,
    capacitor_specs: FootprintSpecs | RadialFootprintSpecs,
    case_code_in: str | None = None,
    case_code_mm: str | None = None,
    step_file_name: str | None = None,
) -> str:
    """Generate complete KiCad footprint file content for a capacitor.

    Args:
        series_spec: Series specifications from SERIES_SPECS
        capacitor_specs:
            Physical specifications from FOOTPRINTS_SPECS or
            RADIAL_FOOTPRINTS_SPECS
        case_code_in: Optional case code to override the series default
        case_code_mm: Optional case code mm to override the series default
        step_file_name: Optional 3D model name to override the default

    Returns:
        Complete .kicad_mod file content as formatted string

    """
    case_in: str = case_code_in if case_code_in else series_spec.case_code_in
    case_mm: str = case_code_mm if case_code_mm else series_spec.case_code_mm
    footprint_name: str = f"C_{case_in}_{case_mm}Metric"
    step_file_name_final: str = (
        step_file_name if step_file_name else f"C_{case_in}"
    )

    if hasattr(capacitor_specs, "is_radial") and capacitor_specs.is_radial:
        return generate_radial_footprint(
            series_spec,
            capacitor_specs,
            case_code_in,
            case_code_mm,
            step_file_name,
        )

    # Regular SMD capacitor
    body_width: float = capacitor_specs.body_dimensions.width
    body_height: float = capacitor_specs.body_dimensions.height

    pad_center_x: float = capacitor_specs.pad_dimensions.center_x
    pad_width: float = capacitor_specs.pad_dimensions.width
    pad_height: float = capacitor_specs.pad_dimensions.height

    if series_spec.capacitor_type == "Ceramic":
        sections: list[str] = [
            footprint_utils.generate_header(footprint_name),
            footprint_utils.generate_properties(
                capacitor_specs.ref_offset_y,
                footprint_name,
            ),
            footprint_utils.generate_courtyard(body_width, body_height),
            footprint_utils.generate_fab_rectangle(body_width, body_height),
            footprint_utils.generate_silkscreen_lines(
                body_height,
                pad_center_x,
                pad_width,
            ),
            footprint_utils.generate_pads(
                pad_width,
                pad_height,
                pad_center_x,
            ),
            footprint_utils.associate_3d_model(
                "${KICAD9_3D_MODELS_VAULT}/3D_models/capacitors",
                step_file_name_final,
            ),
            ")",  # Close the footprint
        ]
    else:
        sections: list[str] = [
            footprint_utils.generate_header(footprint_name),
            footprint_utils.generate_properties(
                capacitor_specs.ref_offset_y,
                footprint_name,
            ),
            footprint_utils.generate_chamfered_shape(
                body_width,
                body_height,
                layer="F.SilkS",
                stroke_width=0.1524,
            ),
            footprint_utils.generate_chamfered_shape(
                body_width,
                body_height,
                layer="F.CrtYd",
            ),
            footprint_utils.generate_chamfered_shape(
                body_width,
                body_height,
                layer="F.Fab",
            ),
            footprint_utils.generate_pads(
                pad_width,
                pad_height,
                pad_center_x,
            ),
            footprint_utils.associate_3d_model(
                "${KICAD9_3D_MODELS_VAULT}/3D_models/capacitors",
                step_file_name_final,
            ),
            ")",  # Close the footprint
        ]

    return "\n".join(sections)


def generate_footprint_file(
    series_name: str,
    output_path: str,
) -> None:
    """Generate and save complete .kicad_mod files for a capacitor series.

    Args:
        series_name: Name of the capacitor series
        output_path: Directory to save the generated footprint files

    Returns:
        None

    """
    series_spec: SeriesSpec = SERIES_SPECS[series_name]

    # Generate the default footprint based on the series specification
    default_case_code_in = series_spec.case_code_in
    capacitor_specs = FOOTPRINTS_SPECS[default_case_code_in]

    default_footprint_content: str = generate_footprint(
        series_spec, capacitor_specs
    )

    default_filename: str = (
        f"C_{series_spec.case_code_in}_{series_spec.case_code_mm}"
        "Metric.kicad_mod"
    )
    default_file_path: str = f"{output_path}/{default_filename}"

    with Path.open(default_file_path, "w", encoding="utf-8") as file_handle:
        file_handle.write(default_footprint_content)

    # If the series has value_footprints, generate additional footprints
    if series_spec.value_footprints:
        for (
            capacitance_value,
            footprint_name,
        ) in series_spec.value_footprints.items():
            if ":" in footprint_name:
                footprint_part = footprint_name.split(":")[1]
                parts = footprint_part.replace("C_", "").split("_")
                if len(parts) >= 2:
                    case_code_in = parts[0]
                    case_code_mm = parts[1].replace("Metric", "")

                    step_file_name = None
                    if (
                        series_spec.value_3d_models
                        and capacitance_value in series_spec.value_3d_models
                    ):
                        # Extract the model name from the full path if needed
                        model_path = series_spec.value_3d_models[
                            capacitance_value
                        ]
                        if ":" in model_path:
                            step_file_name = model_path.split(":")[1]
                        else:
                            step_file_name = model_path

                    if case_code_in in FOOTPRINTS_SPECS:
                        specific_capacitor_specs = FOOTPRINTS_SPECS[
                            case_code_in
                        ]
                        specific_footprint_content: str = generate_footprint(
                            series_spec,
                            specific_capacitor_specs,
                            case_code_in,
                            case_code_mm,
                            step_file_name,
                        )

                        specific_filename: str = f"{footprint_part}.kicad_mod"
                        specific_file_path: str = (
                            f"{output_path}/{specific_filename}"
                        )

                        with Path.open(
                            specific_file_path, "w", encoding="utf-8"
                        ) as file_handle:
                            file_handle.write(specific_footprint_content)
