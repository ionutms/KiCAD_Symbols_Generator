"""Compare part numbers across multiple series."""

import csv
from pathlib import Path

SERIES_CONFIG = {
    "WE-XHMI": {
        "extracted_file": "we_xhmi_parts.csv",
        "display_name": "WE-XHMI",
    },
    "WE-LHMI": {
        "extracted_file": "we_lhmi_parts.csv",
        "display_name": "WE-LHMI",
    },
}

REFERENCE_DB = {
    "file": "../../app/data/UNITED_INDUCTORS_DATA_BASE.csv",
    "name": "UNITED_INDUCTORS",
}


def load_part_numbers_from_extracted_csv(file_path):
    """Load part numbers and their parameters from extracted CSV file.

    Assumes CSV format:
        Part Number, Inductance (uH), IRP,40K (A), RDC Max (mOhm)
    """
    parts_data = {}
    with open(file_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if row:
                part_number = row[0].strip()
                inductance = row[1].strip() if len(row) > 1 else "N/A"
                current_rating = row[2].strip() if len(row) > 2 else "N/A"
                dc_resistance = row[3].strip() if len(row) > 3 else "N/A"
                parts_data[part_number] = {
                    "inductance": inductance,
                    "current_rating": current_rating,
                    "dc_resistance": dc_resistance,
                }
    return parts_data


def load_part_numbers_from_reference_db(file_path):
    """Load part numbers and their parameters from reference CSV file."""
    parts_data = {}
    with open(file_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mpn = row.get("MPN", "").strip()
            if mpn:
                inductance = row.get("Value", "").strip()
                current_rating = row.get("Maximum DC Current (A)", "").strip()
                dc_resistance = row.get(
                    "Maximum DC Resistance (Ω)", ""
                ).strip()
                parts_data[mpn] = {
                    "inductance": inductance,
                    "current_rating": current_rating,
                    "dc_resistance": dc_resistance,
                }
    return parts_data


def compare_part_numbers(extracted_file, reference_file):
    """Compare part numbers between two files."""
    extracted_parts = load_part_numbers_from_extracted_csv(extracted_file)
    reference_parts = load_part_numbers_from_reference_db(reference_file)

    extracted_set = set(extracted_parts.keys())
    reference_set = set(reference_parts.keys())
    common_parts = extracted_set.intersection(reference_set)

    only_in_extracted = extracted_set.difference(reference_set)
    only_in_reference = reference_set.difference(extracted_set)

    return (
        common_parts,
        only_in_extracted,
        only_in_reference,
        extracted_parts,
        reference_parts,
    )


def normalize_numeric_value(value):
    """Normalize numeric values for comparison."""
    if not value or value.upper() in ["N/A", "N/A%"]:
        return value

    original_value = value
    unit = ""

    if value.endswith("mΩ"):
        value = value[:-2]
        unit = "mΩ"
    elif value.endswith("Ω"):
        value = value[:-1]
        unit = "Ω"
    elif value.endswith("A"):
        value = value[:-1]
        unit = "A"
    elif value.endswith(" µH"):
        value = value[:-3]
        unit = "µH"
    elif value.endswith("nH"):
        value = value[:-2]
        unit = "nH"
    elif value.endswith("µH"):
        value = value[:-2]
        unit = "µH"

    try:
        float_val = float(value)

        if unit == "nH":
            float_val = float_val / 1000.0
            unit = "µH"
        elif unit == "mH":
            float_val = float_val * 1000.0
            unit = "µH"

        normalized_val = f"{float_val:.10f}".rstrip("0").rstrip(".")
        return normalized_val + unit if unit else normalized_val
    except ValueError:
        return original_value


def extract_numeric_value(value):
    """Extract the numeric value for comparison purposes."""
    if not value or value.upper() in ["N/A", "N/A%"]:
        return value

    unit = ""
    temp_value = value

    if value.endswith("mΩ"):
        temp_value = value[:-2]
        unit = "mΩ"
    elif value.endswith("Ω"):
        temp_value = value[:-1]
        unit = "Ω"
    elif value.endswith("A"):
        temp_value = value[:-1]
        unit = "A"
    elif value.endswith(" µH"):
        temp_value = value[:-3]
        unit = "µH"
    elif value.endswith("nH"):
        temp_value = value[:-2]
        unit = "nH"
    elif value.endswith("µH"):
        temp_value = value[:-2]
        unit = "µH"

    try:
        float_val = float(temp_value)

        if unit == "nH":
            float_val = float_val / 1000.0
        elif unit == "mH":
            float_val = float_val * 1000.0

        normalized_val = f"{float_val:.10f}".rstrip("0").rstrip(".")
        return normalized_val
    except ValueError:
        return value


def compare_parameters_for_common_parts(
    common_parts, extracted_parts, reference_parts
):
    """Compare parameters for common parts and return mismatches."""
    mismatches = []

    for part in common_parts:
        extracted_params = extracted_parts[part]
        reference_params = reference_parts[part]

        extracted_inductance_raw = extracted_params["inductance"]
        reference_inductance_raw = reference_params["inductance"]
        extracted_inductance = extract_numeric_value(extracted_inductance_raw)
        reference_inductance = extract_numeric_value(reference_inductance_raw)

        extracted_current_raw = extracted_params["current_rating"]
        reference_current_raw = reference_params["current_rating"]
        extracted_current = extract_numeric_value(extracted_current_raw)
        reference_current = extract_numeric_value(reference_current_raw)

        extracted_resistance_raw = extracted_params["dc_resistance"]
        reference_resistance_raw = reference_params["dc_resistance"]
        extracted_resistance = extract_numeric_value(extracted_resistance_raw)
        reference_resistance = extract_numeric_value(reference_resistance_raw)

        if (
            extracted_inductance != reference_inductance
            or extracted_current != reference_current
            or extracted_resistance != reference_resistance
        ):
            mismatches.append({
                "part_number": part,
                "inductance": {
                    "extracted": extracted_inductance_raw,
                    "reference": reference_inductance_raw,
                },
                "current_rating": {
                    "extracted": extracted_current_raw,
                    "reference": reference_current_raw,
                },
                "dc_resistance": {
                    "extracted": extracted_resistance_raw,
                    "reference": reference_resistance_raw,
                },
            })

    return mismatches


def print_comparison_results(
    series_name,
    common,
    only_extracted,
    only_reference,
    extracted_parts,
    reference_parts,
    reference_name,
):
    """Print comparison results for a series."""
    print(f"\n{'=' * 80}")
    print(f"Comparison Results for {series_name}")
    print(f"{'=' * 80}")

    print(f"Total {series_name} parts: {len(extracted_parts)}")
    print(f"Total {reference_name} parts: {len(reference_parts)}")
    print(f"Common parts: {len(common)}")
    print(f"Only in {series_name}: {len(only_extracted)}")
    print(f"Only in {reference_name}: {len(only_reference)}")

    mismatches = compare_parameters_for_common_parts(
        common, extracted_parts, reference_parts
    )

    print(f"\nParameter mismatches found: {len(mismatches)}")

    if mismatches:
        print("\nDetailed parameter mismatches:")
        for mismatch in mismatches:
            print(f"\nPart Number: {mismatch['part_number']}")

            extracted_inductance_num = extract_numeric_value(
                mismatch["inductance"]["extracted"]
            )
            reference_inductance_num = extract_numeric_value(
                mismatch["inductance"]["reference"]
            )

            extracted_current_num = extract_numeric_value(
                mismatch["current_rating"]["extracted"]
            )
            reference_current_num = extract_numeric_value(
                mismatch["current_rating"]["reference"]
            )

            extracted_resistance_num = extract_numeric_value(
                mismatch["dc_resistance"]["extracted"]
            )
            reference_resistance_num = extract_numeric_value(
                mismatch["dc_resistance"]["reference"]
            )

            if extracted_inductance_num != reference_inductance_num:
                print(
                    f"  Inductance - {series_name}: "
                    f"{mismatch['inductance']['extracted']}, "
                    f"{reference_name}: {mismatch['inductance']['reference']}"
                )

            if extracted_current_num != reference_current_num:
                print(
                    f"  Current Rating - {series_name}: "
                    f"{mismatch['current_rating']['extracted']}, "
                    f"{reference_name}: "
                    f"{mismatch['current_rating']['reference']}"
                )

            if extracted_resistance_num != reference_resistance_num:
                print(
                    f"  DC Resistance - {series_name}: "
                    f"{mismatch['dc_resistance']['extracted']}, "
                    f"{reference_name}: "
                    f"{mismatch['dc_resistance']['reference']}"
                )
    else:
        print("\nAll parameter values match for common parts!")

    if only_extracted:
        print(
            f"\n{min(10, len(only_extracted))} "
            f"sample parts only in {series_name}:"
        )
        for part in sorted(only_extracted)[:10]:
            print(f"  {part}")


def compare_series(series_name, script_dir, reference_db_path):
    """Compare a specific series against the reference database."""
    if series_name not in SERIES_CONFIG:
        print(f"Unknown series: {series_name}")
        print(f"Available series: {', '.join(SERIES_CONFIG.keys())}")
        return

    config = SERIES_CONFIG[series_name]
    extracted_file = script_dir / config["extracted_file"]

    if not extracted_file.exists():
        print(
            f"Error: {extracted_file} not found. Run extraction script first."
        )
        return

    if not reference_db_path.exists():
        print(f"Error: {reference_db_path} not found")
        return

    (
        common,
        only_extracted,
        only_reference,
        extracted_parts,
        reference_parts,
    ) = compare_part_numbers(extracted_file, reference_db_path)

    print_comparison_results(
        config["display_name"],
        common,
        only_extracted,
        only_reference,
        extracted_parts,
        reference_parts,
        REFERENCE_DB["name"],
    )


def compare_all_series(script_dir, reference_db_path):
    """Compare all configured series against the reference database."""
    for series_name in SERIES_CONFIG.keys():
        compare_series(series_name, script_dir, reference_db_path)


def generate_summary_report(script_dir, reference_db_path):
    """Generate a summary report for all series."""
    print(f"\n{'=' * 80}")
    print("SUMMARY REPORT - All Series")
    print(f"{'=' * 80}\n")

    summary_data = []

    for series_name in SERIES_CONFIG.keys():
        config = SERIES_CONFIG[series_name]
        extracted_file = script_dir / config["extracted_file"]

        if not extracted_file.exists():
            continue

        try:
            extracted_parts = load_part_numbers_from_extracted_csv(
                extracted_file
            )
            reference_parts = load_part_numbers_from_reference_db(
                reference_db_path
            )

            extracted_set = set(extracted_parts.keys())
            reference_set = set(reference_parts.keys())
            common = extracted_set.intersection(reference_set)
            only_extracted = extracted_set.difference(reference_set)

            mismatches = compare_parameters_for_common_parts(
                common, extracted_parts, reference_parts
            )

            summary_data.append({
                "series": config["display_name"],
                "total": len(extracted_parts),
                "common": len(common),
                "only_in_series": len(only_extracted),
                "mismatches": len(mismatches),
            })
        except Exception as e:
            print(f"Error processing {series_name}: {e}")
            continue

    if summary_data:
        print(
            f"{'Series':<15} {'Total':<8} {'Common':<8} {'New':<8} "
            f"{'Mismatches':<12}"
        )
        print("-" * 60)
        for data in summary_data:
            print(
                f"{data['series']:<15} {data['total']:<8} "
                f"{data['common']:<8} "
                f"{data['only_in_series']:<8} {data['mismatches']:<12}"
            )
    else:
        print("No data available for summary report.")


if __name__ == "__main__":
    script_dir = Path(__file__).parent
    reference_db_path = script_dir / REFERENCE_DB["file"]

    compare_all_series(script_dir, reference_db_path)
