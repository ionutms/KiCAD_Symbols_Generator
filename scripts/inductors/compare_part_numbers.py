"""Compare part numbers."""

import csv
from pathlib import Path


def load_part_numbers_from_we_xhmi(file_path):
    """Load part numbers and their parameters from WE-XHMI CSV file."""
    parts_data = {}
    with open(file_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip header row
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


def load_part_numbers_from_united_inductors(file_path):
    """Load part numbers and their parameters from a CSV file."""
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


def compare_part_numbers(we_xhmi_file, united_inductors_file):
    """Compare part numbers between two files."""
    we_xhmi_parts = load_part_numbers_from_we_xhmi(we_xhmi_file)
    united_inductor_parts = load_part_numbers_from_united_inductors(
        united_inductors_file
    )

    we_xhmi_set = set(we_xhmi_parts.keys())
    united_inductor_set = set(united_inductor_parts.keys())
    common_parts = we_xhmi_set.intersection(united_inductor_set)

    only_in_we_xhmi = we_xhmi_set.difference(united_inductor_set)

    only_in_united = united_inductor_set.difference(we_xhmi_set)

    return (
        common_parts,
        only_in_we_xhmi,
        only_in_united,
        we_xhmi_parts,
        united_inductor_parts,
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
    common_parts, we_xhmi_parts, united_inductor_parts
):
    """Compare parameters for common parts and return mismatches."""
    mismatches = []

    for part in common_parts:
        we_xhmi_params = we_xhmi_parts[part]
        united_params = united_inductor_parts[part]

        we_xhmi_inductance_raw = we_xhmi_params["inductance"]
        united_inductance_raw = united_params["inductance"]
        we_xhmi_inductance = extract_numeric_value(we_xhmi_inductance_raw)
        united_inductance = extract_numeric_value(united_inductance_raw)

        we_xhmi_current_raw = we_xhmi_params["current_rating"]
        united_current_raw = united_params["current_rating"]
        we_xhmi_current = extract_numeric_value(we_xhmi_current_raw)
        united_current = extract_numeric_value(united_current_raw)

        we_xhmi_resistance_raw = we_xhmi_params["dc_resistance"]
        united_resistance_raw = united_params["dc_resistance"]
        we_xhmi_resistance = extract_numeric_value(we_xhmi_resistance_raw)
        united_resistance = extract_numeric_value(united_resistance_raw)

        if (
            we_xhmi_inductance != united_inductance
            or we_xhmi_current != united_current
            or we_xhmi_resistance != united_resistance
        ):
            mismatches.append({
                "part_number": part,
                "inductance": {
                    "we_xhmi": we_xhmi_inductance_raw,
                    "united": united_inductance_raw,
                },
                "current_rating": {
                    "we_xhmi": we_xhmi_current_raw,
                    "united": united_current_raw,
                },
                "dc_resistance": {
                    "we_xhmi": we_xhmi_resistance_raw,
                    "united": united_resistance_raw,
                },
            })

    return mismatches


def print_detailed_comparison(
    common_parts, we_xhmi_parts, united_inductor_parts
):
    """Print detailed parameter comparison for common parts."""
    print("\nDetailed parameter comparison for common parts:")
    print("Format: Part Number | Inductance | Current Rating | DC Resistance")
    print("-" * 80)

    for part in sorted(common_parts):
        we_xhmi_params = we_xhmi_parts[part]
        united_params = united_inductor_parts[part]

        print(
            f"{part} | WE-XHMI: {we_xhmi_params['inductance']}, "
            f"{we_xhmi_params['current_rating']}A, "
            f"{we_xhmi_params['dc_resistance']}mΩ | "
            f"UNITED: {united_params['inductance']}, "
            f"{united_params['current_rating']}A, "
            f"{united_params['dc_resistance']}Ω"
        )


if __name__ == "__main__":
    script_dir = Path(__file__).parent

    we_xhmi_file = script_dir / "we_xhmi_parts.csv"
    united_inductors_file = (
        script_dir
        / ".."
        / ".."
        / "app"
        / "data"
        / "UNITED_INDUCTORS_DATA_BASE.csv"
    )

    if not we_xhmi_file.exists():
        print(f"Error: {we_xhmi_file} not found")
        exit(1)

    if not united_inductors_file.exists():
        print(f"Error: {united_inductors_file} not found")
        exit(1)

    (
        common,
        only_we_xhmi,
        only_united,
        we_xhmi_parts,
        united_inductor_parts,
    ) = compare_part_numbers(we_xhmi_file, united_inductors_file)

    print(f"Total WE-XHMI parts: {len(we_xhmi_parts)}")
    print(f"Total UNITED INDUCTORS parts: {len(united_inductor_parts)}")
    print(f"Common parts: {len(common)}")
    print(f"Only in WE-XHMI: {len(only_we_xhmi)}")
    print(f"Only in UNITED_INDUCTORS: {len(only_united)}")

    mismatches = compare_parameters_for_common_parts(
        common, we_xhmi_parts, united_inductor_parts
    )

    print(f"\nParameter mismatches found: {len(mismatches)}")

    if mismatches:
        print("\nDetailed parameter mismatches:")
        for mismatch in mismatches:
            print(f"\nPart Number: {mismatch['part_number']}")

            we_xhmi_inductance_num = extract_numeric_value(
                mismatch["inductance"]["we_xhmi"]
            )
            united_inductance_num = extract_numeric_value(
                mismatch["inductance"]["united"]
            )

            we_xhmi_current_num = extract_numeric_value(
                mismatch["current_rating"]["we_xhmi"]
            )
            united_current_num = extract_numeric_value(
                mismatch["current_rating"]["united"]
            )

            we_xhmi_resistance_num = extract_numeric_value(
                mismatch["dc_resistance"]["we_xhmi"]
            )
            united_resistance_num = extract_numeric_value(
                mismatch["dc_resistance"]["united"]
            )

            if we_xhmi_inductance_num != united_inductance_num:
                print(
                    f"  Inductance - WE-XHMI: "
                    f"{mismatch['inductance']['we_xhmi']}, "
                    f"UNITED: {mismatch['inductance']['united']}"
                )

            if we_xhmi_current_num != united_current_num:
                print(
                    f"  Current Rating - WE-XHMI: "
                    f"{mismatch['current_rating']['we_xhmi']}, "
                    f"UNITED: {mismatch['current_rating']['united']}"
                )

            if we_xhmi_resistance_num != united_resistance_num:
                print(
                    f"  DC Resistance - WE-XHMI: "
                    f"{mismatch['dc_resistance']['we_xhmi']}, "
                    f"UNITED: {mismatch['dc_resistance']['united']}"
                )
    else:
        print("\nAll parameter values match for common parts!")

    if only_we_xhmi:
        print(f"\n{min(10, len(only_we_xhmi))} sample parts only in WE-XHMI:")
        for part in sorted(only_we_xhmi)[:10]:
            print(f"  {part}")

    if only_united:
        print(
            f"\n{min(10, len(only_united))} "
            "sample parts only in UNITED_INDUCTORS:"
        )
        for part in sorted(only_united)[:10]:
            print(f"  {part}")
