"""Slide Switches Series Part Number Generator.

Generates part numbers and specifications for slide switches series.
Generates both individual series files and unified component database.
"""

import csv
import os
import sys
from typing import Final

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import footprint_slide_switches_generator
import symbol_slide_switches_generator as symbol_slide_switches_generator
import symbol_slide_switches_specs as symbol_slide_switches_specs
from utilities import file_handler_utilities, print_message_utilities

# Global header to attribute mapping
HEADER_MAPPING: Final[dict] = {
    "Symbol Name": lambda part: part.symbol_name,
    "Reference": lambda part: part.reference,
    "Value": lambda part: part.value,
    "Footprint": lambda part: part.footprint,
    "Datasheet": lambda part: part.datasheet,
    "Description": lambda part: part.description,
    "Manufacturer": lambda part: part.manufacturer,
    "MPN": lambda part: part.mpn,
    "Series": lambda part: part.series,
    "Trustedparts Search": lambda part: part.trustedparts_link,
    "Pin Count": lambda part: part.pin_count,
    "Mounting Angle": lambda part: part.mounting_angle,
    "Mounting Style": lambda part: part.mounting_style,
    "Number of Rows": lambda part: part.number_of_rows,
}


def generate_files_for_series(
    series_name: str,
    unified_parts_list: list[symbol_slide_switches_specs.PartInfo],
    generated_footprints: set[str],
) -> None:
    """Generate CSV, KiCad symbol, and footprint files for a specific series.

    Generates all required files for a single slide switch series including
    part number CSV, KiCad symbol library, and footprint files. Appends
    generated parts to the unified parts list for later processing.

    Args:
        series_name: Series identifier that must exist in SYMBOLS_SPECS
        unified_parts_list: List to append generated parts to
        generated_footprints: Set of footprint names already generated to
            avoid duplicates

    Raises:
        ValueError: If series_name is not found in SYMBOLS_SPECS
        FileNotFoundError: If CSV file creation fails
        csv.Error: If CSV processing fails or data formatting is invalid
        IOError: If file operations fail due to permissions or disk space

    Returns:
        None

    Note:
        Generated files are saved in 'app/data/', 'series_kicad_sym/', and
        'slide_switches_footprints.pretty/' directories.

    """
    if series_name not in symbol_slide_switches_specs.SYMBOLS_SPECS:
        msg = f"Unknown series: {series_name}"
        raise ValueError(msg)

    specs = symbol_slide_switches_specs.SYMBOLS_SPECS[series_name]
    series_code = specs.base_series

    # Ensure required directories exist
    file_handler_utilities.ensure_directory_exists("app/data")
    file_handler_utilities.ensure_directory_exists("series_kicad_sym")
    file_handler_utilities.ensure_directory_exists("symbols")
    file_handler_utilities.ensure_directory_exists("footprints")
    footprint_dir = "footprints/slide_switches_footprints.pretty"
    file_handler_utilities.ensure_directory_exists(footprint_dir)

    csv_filename = f"{series_code}_part_numbers.csv"
    csv_path = f"app/data/{csv_filename}"
    symbol_filename = f"SLIDE_SWITCHES_{series_code}_DATA_BASE.kicad_sym"

    # Generate part numbers and write to CSV
    parts_list = symbol_slide_switches_specs.PartInfo.generate_part_numbers(
        specs
    )
    file_handler_utilities.write_to_csv(
        parts_list,
        csv_path,
        HEADER_MAPPING,
    )
    print_message_utilities.print_success(
        f"Generated {len(parts_list)} part numbers in '{csv_path}'",
    )

    # Generate KiCad symbol file
    try:
        symbol_slide_switches_generator.generate_kicad_symbol(
            csv_path,
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

    # Generate KiCad footprint file (only if not already generated)
    try:
        if parts_list:  # Check if parts_list is not empty
            footprint_name = parts_list[0].footprint.split(":")[-1]
            if footprint_name not in generated_footprints:
                footprint_slide_switches_generator.generate_footprint_file(
                    parts_list[0],  # Use first part for footprint generation
                    footprint_dir,
                )
                generated_footprints.add(footprint_name)
                print_message_utilities.print_success(
                    f"KiCad footprint file '{footprint_name}.kicad_mod' "
                    "generated successfully.",
                )
    except ValueError as val_error:
        print_message_utilities.print_error(
            f"Invalid connector specification: {val_error}",
        )
    except OSError as io_error:
        print_message_utilities.print_error(
            f"I/O error when generating footprint file: {io_error}",
        )

    # Add parts to unified list
    unified_parts_list.extend(parts_list)


def generate_unified_files(
    all_parts: list[symbol_slide_switches_specs.PartInfo],
    unified_csv: str,
    unified_symbol: str,
) -> None:
    """Generate unified component database files containing all series.

    Creates a unified CSV file and KiCad symbol file containing all component
    specifications from all processed series. These files serve as a complete
    database for all slide switch components.

    Args:
        all_parts: List of all PartInfo instances across all series
        unified_csv: Name of the unified CSV file to generate
        unified_symbol: Name of the unified KiCad symbol file to generate

    Raises:
        csv.Error: If CSV processing fails or data formatting is invalid
        OSError: If file operations fail due to permissions or disk space

    Returns:
        None

    """
    # Write unified CSV file with full path
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
        symbol_slide_switches_generator.generate_kicad_symbol(
            unified_csv_path,
            f"symbols/{unified_symbol}",
        )
        print_message_utilities.print_success(
            "Unified KiCad symbol file generated successfully.",
        )
    except FileNotFoundError as e:
        print_message_utilities.print_error(
            f"Unified CSV file not found: {e}",
        )
    except csv.Error as e:
        print_message_utilities.print_error(
            f"CSV processing error for unified file: {e}",
        )
    except OSError as e:
        print_message_utilities.print_error(
            f"I/O error when generating unified KiCad symbol file: {e}",
        )


if __name__ == "__main__":
    try:
        unified_parts: list[symbol_slide_switches_specs.PartInfo] = []
        generated_footprints: set[str] = set()  # Track generated footprints

        for series in symbol_slide_switches_specs.SYMBOLS_SPECS:
            print_message_utilities.print_info(
                f"\nGenerating files for {series} series:",
            )
            generate_files_for_series(
                series, unified_parts, generated_footprints
            )

        # Generate unified files after all series are processed
        UNIFIED_CSV = "UNITED_SLIDE_SWITCHES_DATA_BASE.csv"
        UNIFIED_SYMBOL = "UNITED_SLIDE_SWITCHES_DATA_BASE.kicad_sym"
        print_message_utilities.print_info("\nGenerating unified files:")
        generate_unified_files(unified_parts, UNIFIED_CSV, UNIFIED_SYMBOL)

    except (OSError, ValueError, csv.Error) as error:
        print_message_utilities.print_error(
            f"Error generating files: {error}",
        )
