"""Transformer Part Number Generator and File Generator Module.

This module provides functionality to generate part numbers and corresponding
files for electronic transformers, including CSV databases, KiCad symbols,
and footprints.
It supports both individual series generation and unified database creation.
The module handles:
- Generation of part numbers based on series specifications
- Creation of CSV files containing component specifications
- Generation of KiCad symbol files
- Generation of KiCad footprint files
- Creation of unified component databases across all series
Key Functions:
    generate_files_for_series():
        Generates files for a specific transformer series
    generate_unified_files(): Creates unified component database files
Global Variables:
    HEADER_MAPPING (Final[dict]):
        Maps CSV headers to PartInfo attribute getters
Dependencies:
    - csv: For CSV file handling
    - os: For file path operations
    - sys: For path manipulation
    - footprint_transformer_generator: For footprint file generation
    - symbol_transformer_generator: For symbol file generation
    - symbol_transformer_specs: For component specifications
    - utilities: For file handling and message printing
    The module expects specific directory structure for file generation:
    - 'app/data/': For CSV files
    - 'series_kicad_sym/': For individual series symbol files
    - 'symbols/': For unified symbol files
    - 'footprints/transformer_footprints.pretty/': For footprint files

"""

import csv
import os
import sys
from typing import Final

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import footprint_transformer_generator
import symbol_transformer_generator
import symbol_transformer_specs
from utilities import file_handler_utilities, print_message_utilities

# Global header to attribute mapping
HEADER_MAPPING: Final[dict] = {
    "Symbol Name": lambda part: part.symbol_name,
    "Reference": lambda part: part.reference,
    "Value": lambda part: part.mpn,
    "Footprint": lambda part: part.footprint,
    "Datasheet": lambda part: part.datasheet,
    "Trustedparts Search": lambda part: part.trustedparts_link,
    "Description": lambda part: part.description,
    "Manufacturer": lambda part: part.manufacturer,
    "MPN": lambda part: part.mpn,
    "Primary Inductance (µH)": lambda part: part.primary_inductance,
    "Tolerance": lambda part: part.tolerance,
    "Series": lambda part: part.series,
    "Maximum DC Resistance (Ω)": lambda part: "; ".join(
        f"{name} = {value}" for name, value in part.max_dc_resistance.items()
    ),
    "Turns Ratio": lambda part: "; ".join(
        f"{name} = {value}" for name, value in part.turns_ratio.items()
    ),
}


def generate_files_for_series(
    series_name: str,
    unified_parts_list: list[symbol_transformer_specs.PartInfo],
) -> None:
    """Generate CSV, KiCad symbol, and footprint files for a specific series.

    Args:
        series_name: Name of the transformer series to generate files for
        unified_parts_list: List to store all generated PartInfo instances

    Raises:
        ValueError: If the series name is not found in the specs

    Returns:
        None

    Note:
        Generated files are saved in 'app/data/', 'series_kicad_sym/', and
        'transformer_footprints.pretty/' directories.

    """
    if series_name not in symbol_transformer_specs.SYMBOLS_SPECS:
        msg = f"Unknown series: {series_name}"
        raise ValueError(msg)

    specs = symbol_transformer_specs.SYMBOLS_SPECS[series_name]

    # Ensure required directories exist
    file_handler_utilities.ensure_directory_exists("app/data")
    file_handler_utilities.ensure_directory_exists("series_kicad_sym")
    file_handler_utilities.ensure_directory_exists("symbols")
    file_handler_utilities.ensure_directory_exists("footprints")
    footprint_dir = "footprints/transformer_footprints.pretty"
    file_handler_utilities.ensure_directory_exists(footprint_dir)

    csv_filename = f"{specs.base_series}_part_numbers.csv"
    symbol_filename = f"TRANSFORMERS_{specs.base_series}_DATA_BASE.kicad_sym"

    # Generate part numbers and write to CSV
    try:
        parts_list = symbol_transformer_specs.PartInfo.generate_part_numbers(
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
        symbol_transformer_generator.generate_kicad_symbol(
            f"app/data/{csv_filename}",
            f"series_kicad_sym/{symbol_filename}",
        )
        print_message_utilities.print_success(
            f"KiCad symbol file '{symbol_filename}' generated successfully.",
        )

        # Generate KiCad footprint files
        try:
            for part in parts_list:
                footprint_transformer_generator.generate_footprint_file(
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
    all_parts: list[symbol_transformer_specs.PartInfo],
    unified_csv: str,
    unified_symbol: str,
) -> None:
    """Generate unified component database files containing all series.

    Creates:
    1. A unified CSV file containing all component specifications
    2. A unified KiCad symbol file containing all components

    Args:
        all_parts: List of all PartInfo instances from all series
        unified_csv: Filename for the unified CSV file
        unified_symbol: Filename for the unified KiCad symbol file

    Raises:
        csv.Error: If there is an error processing the CSV file
        OSError: If there is an I/O error when generating the files

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
        f"Generated unified CSV file with {len(all_parts)} part numbers",
    )

    # Generate unified KiCad symbol file
    try:
        symbol_transformer_generator.generate_kicad_symbol(
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
        unified_parts: list[symbol_transformer_specs.PartInfo] = []

        for series in symbol_transformer_specs.SYMBOLS_SPECS:
            print_message_utilities.print_info(
                f"\nGenerating files for {series} series:",
            )
            generate_files_for_series(series, unified_parts)

        # Generate unified files after all series are processed
        UNIFIED_CSV = "UNITED_TRANSFORMERS_DATA_BASE.csv"
        UNIFIED_SYMBOL = "UNITED_TRANSFORMERS_DATA_BASE.kicad_sym"
        print_message_utilities.print_info("\nGenerating unified files:")
        generate_unified_files(unified_parts, UNIFIED_CSV, UNIFIED_SYMBOL)

    except (OSError, ValueError, csv.Error) as error:
        print_message_utilities.print_error(
            f"Error generating files: {error}",
        )
