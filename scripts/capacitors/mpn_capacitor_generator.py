"""Murata GCM Series Capacitor Part Number Generator.

A module for generating standardized part numbers for Murata GCM series
capacitors. Supports multiple series types and specifications, producing both
individual series files and unified output in CSV and KiCad symbol formats.

Features:
    - Generates part numbers for GCM155, GCM188, GCM216, GCM31M,
        and GCM31C series
    - Supports X7R dielectric type
    - Creates individual series and unified output files
    - Produces both CSV and KiCad symbol format outputs
    - Handles standard E12 series values with exclusions
    - Generates KiCad footprint files for each series
"""

import csv
import os
import sys
from typing import Final

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import footprint_capacitor_generator
import symbol_capacitor_generator
import symbol_capacitors_specs
from utilities import file_handler_utilities, print_message_utilities

# Global header to attribute mapping
HEADER_MAPPING: Final[dict] = {
    "Symbol Name": lambda part: part.symbol_name,
    "Reference": lambda part: part.reference,
    "Value": lambda part: symbol_capacitors_specs.PartInfo.format_value(
        part.value,
    ),
    "Footprint": lambda part: part.footprint,
    "Datasheet": lambda part: part.datasheet,
    "Description": lambda part: part.description,
    "Manufacturer": lambda part: part.manufacturer,
    "MPN": lambda part: part.mpn,
    "Dielectric": lambda part: part.dielectric,
    "Tolerance": lambda part: part.tolerance,
    "Voltage Rating": lambda part: part.voltage_rating,
    "Case Code - in": lambda part: part.case_code_in,
    "Case Code - mm": lambda part: part.case_code_mm,
    "Series": lambda part: part.series,
    "Trustedparts Search": lambda part: part.trustedparts_link,
    "Capacitor Type": lambda part: part.capacitor_type,
    "3dviewer Link": lambda part: part.step_file_viewer_link,
}


def generate_files_for_series(
    series_name: str,
    unified_parts_list: list[symbol_capacitors_specs.PartInfo],
) -> None:
    """Generate CSV, KiCad symbol, and footprint files for a specific series.

    Args:
        series_name: Series identifier (must exist in SERIES_SPECS)
        unified_parts_list: List to append generated parts to

    Raises:
        ValueError: If series_name is not found in SERIES_SPECS
        FileNotFoundError: If CSV file creation fails
        csv.Error: If CSV processing fails or data formatting is invalid
        IOError: If file operations fail due to permissions or disk space

    Note:
        Generated files are saved in 'app/data/', 'series_kicad_sym/', and
        'capacitor_footprints.pretty/' directories.

    """
    if series_name not in symbol_capacitors_specs.SERIES_SPECS:
        msg = f"Unknown series: {series_name}"
        raise ValueError(msg)

    specs = symbol_capacitors_specs.SERIES_SPECS[series_name]
    series_code = series_name.replace("-", "")

    # Ensure required directories exist
    file_handler_utilities.ensure_directory_exists("app/data")
    file_handler_utilities.ensure_directory_exists("series_kicad_sym")
    file_handler_utilities.ensure_directory_exists("symbols")
    file_handler_utilities.ensure_directory_exists("footprints")
    footprint_dir = "footprints/capacitor_footprints.pretty"
    file_handler_utilities.ensure_directory_exists(footprint_dir)

    csv_filename = f"{series_code}_part_numbers.csv"
    csv_filepath = f"app/data/{csv_filename}"
    symbol_filename = f"CAPACITORS_{series_code}_DATA_BASE.kicad_sym"

    # Generate part numbers and sort by value
    parts_list = symbol_capacitors_specs.PartInfo.generate_part_numbers(specs)
    parts_list.sort(key=lambda part: part.value)

    file_handler_utilities.write_to_csv(
        parts_list,
        csv_filepath,
        HEADER_MAPPING,
    )
    print_message_utilities.print_success(
        f"Generated {len(parts_list)} part numbers in '{csv_filepath}'",
    )

    # Generate KiCad symbol file
    try:
        symbol_capacitor_generator.generate_kicad_symbol(
            csv_filepath,
            f"series_kicad_sym/{symbol_filename}",
        )
        print_message_utilities.print_success(
            f"KiCad symbol file '{symbol_filename}' generated successfully.",
        )
    except FileNotFoundError as file_error:
        print_message_utilities.print_error(
            f"CSV file not found: {file_error}",
        )
    except csv.Error as csv_error:
        print_message_utilities.print_error(
            f"CSV processing error: {csv_error}",
        )
    except OSError as io_error:
        print_message_utilities.print_error(
            f"I/O error when generating KiCad symbol file: {io_error}",
        )

    # Generate KiCad footprint file
    try:
        footprint_capacitor_generator.generate_footprint_file(
            series_name,
            footprint_dir,
        )
        footprint_name = f"{series_name}_{specs.case_code_in}.kicad_mod"
        print_message_utilities.print_success(
            "KiCad footprint file "
            f"'{footprint_name}' generated successfully.",
        )
    except KeyError as key_error:
        print_message_utilities.print_error(
            f"Invalid series specification: {key_error}",
        )
    except OSError as io_error:
        print_message_utilities.print_error(
            f"I/O error when generating footprint file: {io_error}",
        )

    # Add parts to unified list
    unified_parts_list.extend(parts_list)


def generate_unified_files(
    all_parts: list[symbol_capacitors_specs.PartInfo],
    unified_csv: str,
    unified_symbol: str,
) -> None:
    """Generate unified component database files containing all series.

    Args:
        all_parts: Complete list of parts to include in unified files
        unified_csv: Name of the unified CSV file
        unified_symbol: Name of the unified symbol file

    Raises:
        FileNotFoundError: If unified CSV file creation fails
        csv.Error: If CSV processing fails or data formatting is invalid
        IOError: If file operations fail due to permissions or disk space

    Note:
        Creates:
        1. A unified CSV file containing all component specifications
        2. A unified KiCad symbol file containing all components
        3. A complete footprint library for all series

    """
    # Sort all parts by value before writing
    all_parts.sort(key=lambda part: part.value)

    # Write unified CSV file with new app/data path
    unified_csv_path = f"app/data/{unified_csv}"
    file_handler_utilities.write_to_csv(
        all_parts,
        unified_csv_path,
        HEADER_MAPPING,
    )
    print_message_utilities.print_success(
        f"Generated unified CSV file with {len(all_parts)} part numbers",
    )

    # Generate unified KiCad symbol file
    try:
        symbol_capacitor_generator.generate_kicad_symbol(
            unified_csv_path,
            f"symbols/{unified_symbol}",
        )
        print_message_utilities.print_success(
            "Unified KiCad symbol file generated successfully.",
        )
    except FileNotFoundError as file_error:
        print_message_utilities.print_error(
            f"Unified CSV file not found: {file_error}",
        )
    except csv.Error as csv_error:
        print_message_utilities.print_error(
            f"CSV processing error for unified file: {csv_error}",
        )
    except OSError as io_error:
        print_message_utilities.print_error(
            f"Error when generating unified KiCad symbol file: {io_error}",
        )


if __name__ == "__main__":
    try:
        unified_parts: list[symbol_capacitors_specs.PartInfo] = []

        for series in symbol_capacitors_specs.SERIES_SPECS:
            print_message_utilities.print_info(
                f"\nGenerating files for {series} series:",
            )
            generate_files_for_series(series, unified_parts)

        # Generate unified files after all series are processed
        UNIFIED_CSV = "UNITED_CAPACITORS_DATA_BASE.csv"
        UNIFIED_SYMBOL = "UNITED_CAPACITORS_DATA_BASE.kicad_sym"
        print_message_utilities.print_info("\nGenerating unified files:")
        generate_unified_files(unified_parts, UNIFIED_CSV, UNIFIED_SYMBOL)

    except (OSError, csv.Error) as file_error:
        print_message_utilities.print_error(
            f"Error generating unified files: {file_error}",
        )
