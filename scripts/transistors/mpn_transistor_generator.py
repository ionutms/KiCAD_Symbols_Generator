"""Diode Component File Generator.

This module automates the generation of electronic component documentation
and KiCad library files for diodes.

Key Features:
- Generates CSV files with detailed component specifications
- Creates KiCad symbol files for electronic design automation (EDA)
- Produces KiCad footprint files for PCB layout
- Builds a unified component database

Primary Workflow:
1. Reads diode series specifications from symbol_diode_specs
2. Generates individual part numbers for each series
3. Creates CSV files with component details
4. Generates KiCad symbol files
5. Produces footprint files
6. Assembles a unified component database

Typical Use Cases:
- Automated electronic component library management
- Standardizing component documentation
- Facilitating KiCad library development

Dependencies:
- symbol_diode_specs: Provides series and part specifications
- file_handler_utilities: Handles file operations
- print_message_utilities: Manages logging and error reporting
- footprint_diode_generator: Generates component footprints
- symbol_diode_generator: Creates KiCad symbol files

Note:
Requires predefined series specifications in symbol_diode_specs.SYMBOLS_SPECS

"""

import csv
import os
import sys
from typing import Final

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import footprint_transistor_generator
import symbol_transistor_generator
import symbol_transistor_specs
from utilities import file_handler_utilities, print_message_utilities

# Global header to attribute mapping
HEADER_MAPPING: Final[dict] = {
    "Symbol Name": lambda part: part.symbol_name,
    "Reference": lambda part: part.reference,
    "Value": lambda part: f"{part.value} V",
    "Footprint": lambda part: part.footprint,
    "Datasheet": lambda part: part.datasheet,
    "Description": lambda part: part.description,
    "Manufacturer": lambda part: part.manufacturer,
    "MPN": lambda part: part.mpn,
    "Series": lambda part: part.series,
    "Trustedparts Search": lambda part: part.trustedparts_link,
    "Drain Current (A)": lambda part: f"{part.drain_current:.1f}",
    "Transistor Type": lambda part: part.transistor_type,
}


def generate_files_for_series(
    series_name: str,
    unified_parts_list: list[symbol_transistor_specs.PartInfo],
) -> None:
    """Generate component files for a specific transistor series.

    Generates part numbers, CSV files, KiCad symbol files, and footprint files
    for a given transistor series based on manufacturer specifications.

    Args:
        series_name: Name of the transistor series to generate files for
        unified_parts_list: List to store all part numbers for unified files

    Raises:
        ValueError: If the series name is not found in the specifications

    Returns:
        None

    """
    if series_name not in symbol_transistor_specs.SYMBOLS_SPECS:
        msg = f"Unknown series: {series_name}"
        raise ValueError(msg)

    specs = symbol_transistor_specs.SYMBOLS_SPECS[series_name]

    # Ensure required directories exist
    file_handler_utilities.ensure_directory_exists("app/data")
    file_handler_utilities.ensure_directory_exists("series_kicad_sym")
    file_handler_utilities.ensure_directory_exists("symbols")
    file_handler_utilities.ensure_directory_exists("footprints")
    footprint_dir = "footprints/transistor_footprints.pretty"
    file_handler_utilities.ensure_directory_exists(footprint_dir)

    csv_filename = f"{specs.base_series}_part_numbers.csv"
    symbol_filename = f"TRANSISTORS_{specs.base_series}_DATA_BASE.kicad_sym"

    # Generate part numbers and write to CSV
    try:
        parts_list = symbol_transistor_specs.PartInfo.generate_part_numbers(
            specs,
        )
        file_handler_utilities.write_to_csv(
            parts_list,
            f"app/data/{csv_filename}",
            HEADER_MAPPING,
        )
        print_message_utilities.print_success(
            f"Generated {len(parts_list)} part numbers in "
            f"'app/data/{csv_filename}'",
        )

        # Generate KiCad symbol file
        symbol_transistor_generator.generate_kicad_symbol(
            f"app/data/{csv_filename}",
            f"series_kicad_sym/{symbol_filename}",
        )
        print_message_utilities.print_success(
            f"KiCad symbol file '{symbol_filename}' generated successfully.",
        )

        # Generate KiCad footprint files
        try:
            for part in parts_list:
                footprint_transistor_generator.generate_footprint_file(
                    part,
                    footprint_dir,
                )
                print_message_utilities.print_success(
                    f"Generated footprint file for {part.mpn}",
                )
        except ValueError as footprint_error:
            print_message_utilities.print_error(
                f"Error generating footprint: {footprint_error}",
            )
        except OSError as io_error:
            print_message_utilities.print_error(
                f"I/O error generating footprint: {io_error}",
            )

        # Add parts to unified list
        unified_parts_list.extend(parts_list)

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
            f"I/O error when generating files: {io_error}",
        )
    except ValueError as val_error:
        print_message_utilities.print_error(
            f"Error generating part numbers: {val_error}",
        )


def generate_unified_files(
    all_parts: list[symbol_transistor_specs.PartInfo],
    unified_csv: str,
    unified_symbol: str,
) -> None:
    """Generate unified component database files containing all series.

    Creates:
    1. A unified CSV file containing all component specifications
    2. A unified KiCad symbol file containing all components

    Args:
        all_parts: List of all part numbers from different series
        unified_csv: Filename for the unified CSV file
        unified_symbol: Filename for the unified KiCad symbol file

    Raises:
        FileNotFoundError: If CSV file creation fails
        csv.Error: If CSV processing fails or data formatting is invalid
        IOError: If file operations fail due to permissions or disk space

    Returns:
        None

    """
    # Write unified CSV file
    file_handler_utilities.write_to_csv(
        all_parts,
        f"app/data/{unified_csv}",
        HEADER_MAPPING,
    )
    print_message_utilities.print_success(
        f"Generated unified CSV file with {len(all_parts)} "
        f"part numbers in 'app/data/{unified_csv}'",
    )

    # Generate unified KiCad symbol file
    try:
        symbol_transistor_generator.generate_kicad_symbol(
            f"app/data/{unified_csv}",
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
        unified_parts: list[symbol_transistor_specs.PartInfo] = []

        for series in symbol_transistor_specs.SYMBOLS_SPECS:
            print_message_utilities.print_info(
                f"\nGenerating files for {series} series:",
            )
            generate_files_for_series(series, unified_parts)

        # Generate unified files after all series are processed
        UNIFIED_CSV = "UNITED_TRANSISTORS_DATA_BASE.csv"
        UNIFIED_SYMBOL = "UNITED_TRANSISTORS_DATA_BASE.kicad_sym"
        print_message_utilities.print_info("\nGenerating unified files:")
        generate_unified_files(unified_parts, UNIFIED_CSV, UNIFIED_SYMBOL)

    except (OSError, ValueError, csv.Error) as error:
        print_message_utilities.print_error(
            f"Error generating files: {error}",
        )
