"""Panasonic ERJ Series Part Number Generator.

This script generates part numbers for Panasonic ERJ resistor series including
ERJ-2RK, ERJ-3EK, ERJ-6EN, ERJ-P08, ERJ-P06, and ERJ-P03. It supports both E96
and E24 standard values and handles component specifications like size, power
rating, resistance range, and packaging options.

The script generates:
- Part numbers following Panasonic's naming conventions
- CSV files containing component specifications and parameters
- KiCad symbol files for electronic design automation

Features:
- Supports E96 and E24 resistance value series
- Handles resistance values from 10Ω to 2.2MΩ depending on series
- Generates both individual series files and unified component database
- Includes vendor links and detailed component specifications
- Exports in industry-standard formats (CSV, KiCad)
"""

import csv
import os
import sys
from typing import Final

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import footprint_resistor_generator
import symbol_resistor_generator
import symbol_resistors_specs
from utilities import file_handler_utilities, print_message_utilities

# Global header to attribute mapping
HEADER_MAPPING: Final[dict] = {
    "Symbol Name": lambda part: part.symbol_name,
    "Reference": lambda part: part.reference,
    "Value": lambda part: symbol_resistors_specs.PartInfo.format_value(
        part.value,
    ),
    "Footprint": lambda part: part.footprint,
    "Datasheet": lambda part: part.datasheet,
    "Description": lambda part: part.description,
    "Manufacturer": lambda part: part.manufacturer,
    "MPN": lambda part: part.mpn,
    "Tolerance": lambda part: part.tolerance,
    "Temperature Coefficient": lambda part: part.temperature_coefficient,
    "Voltage Rating": lambda part: part.voltage_rating,
    "Case Code - in": lambda part: part.case_code_in,
    "Case Code - mm": lambda part: part.case_code_mm,
    "Series": lambda part: part.series,
    "Trustedparts Search": lambda part: part.trustedparts_link,
    "3dviewer Link": lambda part: part.step_file_viewer_link,
    "Component Type": lambda part: part.component_type,
}

# Define the data directory
DATA_DIR = "app/data"


def generate_files_for_series(
    series_name: str,
    unified_parts_list: list[symbol_resistors_specs.PartInfo],
) -> None:
    """Generate CSV, KiCad symbol, and footprint files for a resistor series.

    Creates:
    1. A CSV file containing all component specifications
    2. A KiCad symbol file for use in electronic design
    3. A KiCad footprint file for PCB layout
    4. Adds generated parts to the unified parts list

    Args:
        series_name: Name of the resistor series to generate files for
        unified_parts_list: List of all PartInfo instances across all series

    Raises:
        ValueError: If the series name is not found in the specs dictionary
        FileNotFoundError: If CSV file cannot be found
        csv.Error: If CSV processing fails
        OSError: If file operations fail

    Returns:
        None

    """
    if series_name not in symbol_resistors_specs.SYMBOLS_SPECS:
        msg = f"Unknown series: {series_name}"
        raise ValueError(msg)

    specs = symbol_resistors_specs.SYMBOLS_SPECS[series_name]

    # Ensure required directories exist
    file_handler_utilities.ensure_directory_exists(DATA_DIR)
    file_handler_utilities.ensure_directory_exists("series_kicad_sym")
    file_handler_utilities.ensure_directory_exists("symbols")
    file_handler_utilities.ensure_directory_exists("footprints")
    footprint_dir = "footprints/resistor_footprints.pretty"
    file_handler_utilities.ensure_directory_exists(footprint_dir)

    csv_filename = f"{series_name}_part_numbers.csv"
    symbol_filename = f"RESISTORS_{series_name}_DATA_BASE.kicad_sym"
    csv_file_path = f"{DATA_DIR}/{csv_filename}"

    # Generate part numbers and sort by value
    parts_list = symbol_resistors_specs.PartInfo.generate_part_numbers(specs)
    # Remove duplicates
    unique_parts_dict = {part.mpn: part for part in parts_list}
    parts_list = list(unique_parts_dict.values())
    parts_list.sort(key=lambda part: part.value)

    file_handler_utilities.write_to_csv(
        parts_list,
        csv_file_path,
        HEADER_MAPPING,
    )
    print_message_utilities.print_success(
        f"Generated {len(parts_list)} part numbers in '{csv_file_path}'",
    )

    # Generate KiCad symbol file
    try:
        symbol_resistor_generator.generate_kicad_symbol(
            csv_file_path,
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
        footprint_resistor_generator.generate_footprint_file(
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
    all_parts: list[symbol_resistors_specs.PartInfo],
    unified_csv: str,
    unified_symbol: str,
) -> None:
    """Generate unified component database files containing all series.

    Creates:
    1. A unified CSV file containing all component specifications
    2. A unified KiCad symbol file containing all components
    3. A complete footprint library for all series

    Args:
        all_parts: List of all PartInfo instances across all series
        unified_csv: Name of the unified CSV file to generate
        unified_symbol: Name of the unified KiCad symbol file to generate

    Raises:
        csv.Error: If CSV processing fails
        OSError: If file operations fail

    Returns:
        None

    """
    # Sort all parts by value before writing
    all_parts.sort(key=lambda part: part.value)

    # Write unified CSV file
    unified_csv_path = f"{DATA_DIR}/{unified_csv}"
    file_handler_utilities.write_to_csv(
        all_parts,
        unified_csv_path,
        HEADER_MAPPING,
    )
    print_message_utilities.print_success(
        f"Generated unified CSV file with {len(all_parts)} "
        f"part numbers at {unified_csv_path}",
    )

    # Generate unified KiCad symbol file
    try:
        symbol_resistor_generator.generate_kicad_symbol(
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
        unified_parts: list[symbol_resistors_specs.PartInfo] = []

        for series in symbol_resistors_specs.SYMBOLS_SPECS:
            print_message_utilities.print_info(
                f"\nGenerating files for {series} series:",
            )
            generate_files_for_series(series, unified_parts)

        # Generate unified files after all series are processed
        UNIFIED_CSV = "UNITED_RESISTORS_DATA_BASE.csv"
        UNIFIED_SYMBOL = "UNITED_RESISTORS_DATA_BASE.kicad_sym"
        print_message_utilities.print_info("\nGenerating unified files:")
        generate_unified_files(unified_parts, UNIFIED_CSV, UNIFIED_SYMBOL)

    except (OSError, csv.Error) as file_error:
        print_message_utilities.print_error(
            f"Error generating files: {file_error}",
        )
