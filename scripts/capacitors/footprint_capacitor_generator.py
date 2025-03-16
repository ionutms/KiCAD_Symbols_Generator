"""KiCad Footprint Generator for Surface Mount Capacitors.

Generates standardized KiCad footprint files (.kicad_mod) for surface mount
capacitors. Uses manufacturer specifications to create accurate footprints
with appropriate pad dimensions and clearances.
"""

from pathlib import Path

from footprint_capacitor_specs import FOOTPRINTS_SPECS, FootprintSpecs
from symbol_capacitors_specs import SERIES_SPECS, SeriesSpec
from utilities import footprint_utils


def generate_footprint(
    series_spec: SeriesSpec,
    capacitor_specs: FootprintSpecs,
) -> str:
    """Generate complete KiCad footprint file content for a capacitor.

    Args:
        series_spec: Series specifications from SERIES_SPECS
        capacitor_specs: Physical specifications from FOOTPRINTS_SPECS

    Returns:
        Complete .kicad_mod file content as formatted string

    """
    case_in: str = series_spec.case_code_in
    case_mm: str = series_spec.case_code_mm
    footprint_name: str = f"C_{case_in}_{case_mm}Metric"
    step_file_name: str = f"C_{case_in}"

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
                "${KIPRJMOD}/KiCAD_Symbol_Generator/3D_models",
                step_file_name,
                hide=True,
            ),
            footprint_utils.associate_3d_model(
                "${3D_MODELS_VAULT}/3D_models/capacitors",
                step_file_name,
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
                "${KIPRJMOD}/KiCAD_Symbol_Generator/3D_models",
                step_file_name,
                hide=True,
            ),
            footprint_utils.associate_3d_model(
                "${3D_MODELS_VAULT}/3D_models/capacitors",
                step_file_name,
            ),
            ")",  # Close the footprint
        ]

    return "\n".join(sections)


def generate_footprint_file(
    series_name: str,
    output_path: str,
) -> None:
    """Generate and save a complete .kicad_mod file for a capacitor.

    Args:
        series_name: Name of the capacitor series
        output_path: Directory to save the generated footprint file

    Returns:
        None

    """
    series_spec: SeriesSpec = SERIES_SPECS[series_name]
    capacitor_specs: FootprintSpecs = FOOTPRINTS_SPECS[
        series_spec.case_code_in
    ]

    footprint_content: str = generate_footprint(series_spec, capacitor_specs)

    filename: str = (
        f"C_{series_spec.case_code_in}_{series_spec.case_code_mm}"
        "Metric.kicad_mod"
    )
    file_path: str = f"{output_path}/{filename}"

    with Path.open(file_path, "w", encoding="utf-8") as file_handle:
        file_handle.write(footprint_content)
