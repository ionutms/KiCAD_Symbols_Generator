#!/usr/bin/env python3
"""Compare pin alternate and additional functions between a CSV and a symbol.

Reads a datasheet pin-definition CSV and a KiCad ``.kicad_sym`` file,
then reports discrepancies between the functions listed in the CSV and
those stored as ``(alternate ...)`` entries in the symbol.
"""

import csv
import re

CSV_FILE = (
    "scripts/extract_pdf_tables/tables/stm32h562ag/"
    "Table 14 STM32H562xx and STM32H563xx pin_ball definition LQFP144.csv"
)
KICAD_FILE = "symbols/UNITED_IC_ST.kicad_sym"


def normalize(text):
    """Return text lowercased with underscores, dashes, and spaces removed.

    Args:
        text: String to normalise.

    Returns:
        Normalised string used for fuzzy comparisons.

    """
    return text.lower().replace("_", "").replace("-", "").replace(" ", "")


def split_function_list(raw):
    """Split a comma-separated cell value into a list of strings.

    Discards empty entries and bare dash placeholders.

    Args:
        raw: Raw cell text, may be an en-dash or empty string.

    Returns:
        List of stripped strings.

    """
    if raw in ("-", "", "\u2013"):
        return []
    return [
        part.strip()
        for part in re.split(r",\s*", raw)
        if part.strip() and part.strip() != "-"
    ]


def expand_slash_names(function_set):
    """Expand slash-separated compound names into individual tokens.

    Slash notation is used for signals that share a pin, e.g.
    ``TAMP_IN2/TAMP_OUT1``.  Each component is added individually so
    comparisons work regardless of which form is used.

    Args:
        function_set: Iterable of strings, some of which may contain
            ``/`` separators.

    Returns:
        New set containing each slash-split component.

    """
    expanded = set()
    for func in function_set:
        for part in func.split("/"):
            expanded.add(part.strip())
    return expanded


def parse_csv(csv_path):
    """Parse a pin-definition CSV into a dict keyed by primary pin name.

    The primary name is extracted from column 2 by stripping any
    dash-suffix or parenthetical annotation, e.g.
    ``PC14-OSC32_IN (OSC32_IN)`` becomes ``PC14``.  Rows whose name
    cell is empty, matches a known column header, or is a package
    section divider are skipped.

    Args:
        csv_path: Path to the CSV file.

    Returns:
        Dict keyed by primary pin name.  Each value is a dict with
        ``pin_numbers`` (list of pin numbers seen for that name),
        ``alternate_functions`` (list of strings from column 3),
        ``additional_functions`` (list of strings from column 4), and
        ``all_functions`` (set union of the two lists).

    """
    pins = {}

    with open(csv_path, encoding="utf-8-sig") as csv_file:
        raw_content = csv_file.read()

    raw_content = raw_content.replace("\r\n", "\n").replace("\r", "\n")

    for row in csv.reader(raw_content.splitlines()):
        if len(row) < 2:
            continue

        pin_number_raw = row[0].strip()
        pin_name_raw = row[1].strip() if len(row) > 1 else ""
        alt_func_raw = row[2].strip() if len(row) > 2 else ""
        add_func_raw = row[3].strip() if len(row) > 3 else ""

        if not pin_name_raw:
            continue

        if (
            "function after reset" in pin_name_raw.lower()
            or pin_name_raw.startswith("Pin name")
        ):
            continue

        if pin_name_raw in ("LQFP144", "TFBGA216", "UFBGA169"):
            continue

        pin_name_raw = pin_name_raw.replace("\n", " ").strip()
        alt_func_raw = alt_func_raw.replace("\n", " ").strip()
        add_func_raw = add_func_raw.replace("\n", " ").strip()

        pin_name = re.split(r"[-\(]", pin_name_raw)[0].strip()

        alt_funcs = split_function_list(alt_func_raw)
        add_funcs = split_function_list(add_func_raw)

        if pin_name not in pins:
            pins[pin_name] = {
                "pin_numbers": [],
                "alternate_functions": alt_funcs,
                "additional_functions": add_funcs,
                "all_functions": set(alt_funcs + add_funcs),
            }

        if pin_number_raw not in pins[pin_name]["pin_numbers"]:
            pins[pin_name]["pin_numbers"].append(pin_number_raw)

    return pins


def parse_kicad_sym(sym_path):
    """Parse pin definitions from a KiCad ``.kicad_sym`` file.

    Each ``(pin ...)`` block is parsed for its name and number.
    Alternate function names are read from ``(alternate "NAME" ...)``
    child entries that follow each pin block.

    Args:
        sym_path: Path to the ``.kicad_sym`` file.

    Returns:
        Dict keyed by pin number string.  Each value is a dict with
        ``name`` (full pin name as written in the symbol), ``primary``
        (first token before any ``/`` or ``-``), ``alternates`` (set
        of raw alternate name strings), and ``all_kicad_funcs`` (set
        of all function tokens with slash-compound names expanded).

    """
    with open(sym_path, encoding="utf-8") as sym_file:
        content = sym_file.read()

    pin_header_pattern = re.compile(
        r"\(pin\s+\w+\s+\w+\s*"
        r"(?:\(at[^)]+\)\s*)?"
        r"\(length[^)]+\)\s*"
        r'\(name\s+"([^"]+)"[\s\S]*?'
        r'\(number\s+"([^"]+)"',
    )

    alternate_pattern = re.compile(r'\(alternate\s+"([^"]+)"')

    header_matches = [
        (match.start(), match.end(), match.group(1), match.group(2))
        for match in pin_header_pattern.finditer(content)
    ]

    kicad_pins = {}

    for index, (_start, end, pin_name, pin_number) in enumerate(
        header_matches
    ):
        if index + 1 < len(header_matches):
            next_start = header_matches[index + 1][0]
        else:
            next_start = len(content)

        block = content[end:next_start]
        alternates = set(alternate_pattern.findall(block))

        expanded_alternates = expand_slash_names(alternates)

        primary = re.split(r"[/\-]", pin_name)[0].strip()
        name_tokens = {
            token.strip()
            for token in re.split(r"[/\-]", pin_name)
            if token.strip()
        }
        name_extras = name_tokens - {primary}

        kicad_pins[pin_number] = {
            "name": pin_name,
            "primary": primary,
            "alternates": alternates,
            "all_kicad_funcs": expanded_alternates | name_extras,
        }

    return kicad_pins


def sort_key_for_pin(pin_item):
    """Return a sort key that orders pin numbers numerically.

    Non-numeric references are placed after all numeric ones.

    Args:
        pin_item: A ``(pin_number_str, pin_dict)`` tuple.

    Returns:
        Tuple of ``(int_value, str_value)`` suitable for ``sorted()``.

    """
    pin_number_str = pin_item[0]
    if pin_number_str.isdigit():
        return (int(pin_number_str), pin_number_str)
    return (9999, pin_number_str)


def compare(csv_pins, kicad_pins):
    """Cross-reference symbol pins against CSV entries and report differences.

    Both function sets are normalised before comparison so minor
    formatting differences do not cause false positives.
    Slash-compound names are expanded so each component is matched
    independently.

    Args:
        csv_pins: Dict returned by ``parse_csv``.
        kicad_pins: Dict returned by ``parse_kicad_sym``.

    Returns:
        List of result dicts, one per pin, each with ``pin_number``
        (str), ``kicad_name`` (str), ``csv_name`` (str), ``status``
        (one of ``OK``, ``MISMATCH``, ``MISSING_IN_KICAD``,
        ``EXTRA_IN_KICAD``, ``MISSING_IN_CSV``),
        ``missing_in_kicad`` (sorted list of functions absent from the
        symbol), ``extra_in_kicad`` (sorted list of functions absent
        from the CSV), and ``notes`` (str).

    """
    results = []

    for pin_number, kicad_pin in sorted(
        kicad_pins.items(), key=sort_key_for_pin
    ):
        primary = kicad_pin["primary"]
        csv_entry = csv_pins.get(primary)

        if csv_entry is None:
            results.append({
                "pin_number": pin_number,
                "kicad_name": kicad_pin["name"],
                "csv_name": "-",
                "status": "MISSING_IN_CSV",
                "missing_in_kicad": [],
                "extra_in_kicad": [],
                "notes": f"'{primary}' not found in CSV",
            })
            continue

        ds_expanded = expand_slash_names(csv_entry["all_functions"])

        ds_norm = {normalize(func): func for func in ds_expanded}
        kicad_norm = {
            normalize(func): func for func in kicad_pin["all_kicad_funcs"]
        }

        missing_in_kicad = [
            func
            for norm_key, func in ds_norm.items()
            if norm_key not in kicad_norm
        ]
        extra_in_kicad = [
            func
            for norm_key, func in kicad_norm.items()
            if norm_key not in ds_norm
        ]

        if extra_in_kicad and missing_in_kicad:
            status = "MISMATCH"
        elif extra_in_kicad:
            status = "EXTRA_IN_KICAD"
        elif missing_in_kicad:
            status = "MISSING_IN_KICAD"
        else:
            status = "OK"

        results.append({
            "pin_number": pin_number,
            "kicad_name": kicad_pin["name"],
            "csv_name": primary,
            "status": status,
            "missing_in_kicad": sorted(missing_in_kicad),
            "extra_in_kicad": sorted(extra_in_kicad),
            "notes": "",
        })

    return results


def print_results(results):
    """Print a detailed issue list and a summary table to stdout.

    Entries with status ``OK`` are omitted from the detailed listing
    but counted in the summary.

    Args:
        results: List of result dicts returned by ``compare``.

    """
    issues = [row for row in results if row["status"] != "OK"]

    print(f"\n{'=' * 70}")
    print(f"  ISSUES  ({len(issues)} of {len(results)} pins)")
    print(f"{'=' * 70}\n")

    for row in issues:
        pin_label = f"Pin {row['pin_number']:>4}"
        status_tag = f"[{row['status']}]"
        print(
            f"{pin_label}  {status_tag}"
            f"  KiCad: {row['kicad_name']!r}"
            f"  CSV: {row['csv_name']!r}"
        )

        if row["missing_in_kicad"]:
            funcs = ", ".join(row["missing_in_kicad"])
            print(f"         ⚠ In datasheet, missing in KiCad : {funcs}")
        if row["extra_in_kicad"]:
            funcs = ", ".join(row["extra_in_kicad"])
            print(f"         ✗ In KiCad, not in datasheet     : {funcs}")
        if row["notes"]:
            print(f"         ℹ {row['notes']}")
        print()

    counts = {}
    for row in results:
        counts[row["status"]] = counts.get(row["status"], 0) + 1

    print(f"{'=' * 70}")
    print("  SUMMARY")
    print(f"{'=' * 70}")
    for status, count in sorted(counts.items()):
        print(f"  {status:<35} {count}")
    print(f"  {'TOTAL':<35} {len(results)}")
    print()


if __name__ == "__main__":
    print(f"Parsing CSV   : {CSV_FILE}")
    csv_pins = parse_csv(CSV_FILE)
    print(f"  -> {len(csv_pins)} unique pins\n")

    print(f"Parsing KiCad : {KICAD_FILE}")
    kicad_pins = parse_kicad_sym(KICAD_FILE)
    print(f"  -> {len(kicad_pins)} pins in symbol")

    results = compare(csv_pins, kicad_pins)
    print_results(results)
