"""Extract footprint code and modify it in a KiCad .kicad_pcb file.

This script can extract the complete footprint code for a specified reference,
or modify the footprint by adding/removing (hide yes) to/from the model field.

Usage:
    Extract:
        python extract_footprints.py <kicad_pcb_file> <reference> --code
    Hide 3D model:
        python extract_footprints.py <kicad_pcb_file> <reference> --hide
    Show 3D model:
        python extract_footprints.py <kicad_pcb_file> <reference> --show

"""

import argparse
import re
import sys
from pathlib import Path


def parse_kicad_pcb(file_path):
    """Parse a KiCad PCB file and extract footprint data by reference.

    Args:
        file_path (str or Path): Path to the .kicad_pcb file

    Returns:
        tuple: (file_content, dict mapping reference designators to footprint
        data), including the start and end positions in the file

    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    footprints = {}

    for match in re.finditer(r"\(footprint", content):
        start_pos = match.start()

        paren_count = 0
        for i in range(start_pos, len(content)):
            if content[i] == "(":
                paren_count += 1
            elif content[i] == ")":
                paren_count -= 1
                if paren_count == 0:
                    footprint_raw = content[start_pos : i + 1]

                    ref_match = re.search(
                        r'\(property "Reference"\s+"([^\"]+)"', footprint_raw
                    )
                    if ref_match:
                        ref = ref_match.group(1)
                        footprints[ref] = {
                            "full_data": footprint_raw,
                            "start_pos": start_pos,
                            "end_pos": i + 1,
                        }
                    break

    return content, footprints


def replace_footprint_in_file(file_path, reference, new_footprint_code):
    """Replace the footprint with the specified reference in the file.

    Args:
        file_path (str or Path): Path to the .kicad_pcb file
        reference (str): Reference designator to replace
        new_footprint_code (str): New footprint code to insert

    Returns:
        bool: True if replacement was successful, False otherwise

    """
    content, footprints = parse_kicad_pcb(file_path)

    if reference not in footprints:
        print(f"Error: No footprint found with reference: {reference}")
        return False

    footprint_info = footprints[reference]
    start_pos = footprint_info["start_pos"]
    end_pos = footprint_info["end_pos"]

    new_content = content[:start_pos] + new_footprint_code + content[end_pos:]

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(new_content)

    print(f"Successfully replaced footprint for reference {reference}")
    return True


def add_hide_to_model(footprint_code):
    """Add (hide yes) to the model field in the footprint code.

    Args:
        footprint_code (str): The footprint code to modify

    Returns:
        str: The modified footprint code

    """
    pattern = r'(\(model\s+"[^"]+"\s*\n\s*)(\(\s*offset)'

    def replace_func(match):
        return match.group(1) + "(hide yes)\n\t\t\t" + match.group(2)

    modified_code = re.sub(pattern, replace_func, footprint_code)

    hide_pattern = r'\(model\s+"[^"]+"\s*\n\s*\t*\s*\(\s*hide\s+yes\s*\)'
    if re.search(hide_pattern, footprint_code):
        print(
            "Warning: This footprint already has "
            "(hide yes) in the model section."
        )

    return modified_code


def remove_hide_from_model(footprint_code):
    """Remove (hide yes) from the model field in the footprint code.

    Args:
        footprint_code (str): The footprint code to modify

    Returns:
        str: The modified footprint code

    """
    pattern = (
        r'(\(model\s+"[^"]+"\s*\n\s*)'
        r"(\t*\s*\(\s*hide\s+yes\s*\)\s*\n\s*)"
        r"(\(\s*offset)"
    )

    def replace_func(match):
        return match.group(1) + match.group(3)

    modified_code = re.sub(pattern, replace_func, footprint_code)

    hide_pattern = r'\(model\s+"[^"]+"\s*\n\s*\t*\s*\(\s*hide\s+yes\s*\)'
    if not re.search(hide_pattern, footprint_code):
        print(
            "Note: This footprint does not have "
            "(hide yes) in the model section."
        )

    return modified_code


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Extract footprint code and modify 3D model visibility "
            "in a KiCad .kicad_pcb file"
        )
    )
    parser.add_argument("pcb_file", help="Path to the .kicad_pcb file")
    parser.add_argument(
        "reference",
        help="Reference designator to extract/modify (e.g., M3, U2)",
    )
    parser.add_argument(
        "--code",
        action="store_true",
        help="Show the complete footprint code for a specific footprint",
    )
    parser.add_argument(
        "--hide",
        action="store_true",
        help="Add (hide yes) to the model section of the footprint",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help=(
            "Remove (hide yes) from the model section "
            "of the footprint to show 3D model"
        ),
    )

    args = parser.parse_args()

    pcb_path = Path(args.pcb_file)

    if not pcb_path.exists():
        print(f"Error: File {pcb_path} does not exist.")
        sys.exit(1)

    if not pcb_path.suffix.lower() == ".kicad_pcb":
        print(f"Warning: File {pcb_path} does not have .kicad_pcb extension.")

    if args.code and args.reference and not args.hide and not args.show:
        _, footprints = parse_kicad_pcb(pcb_path)
        if args.reference in footprints:
            print(f"Complete footprint code for reference: {args.reference}")
            print(footprints[args.reference]["full_data"])
        else:
            print(f"No footprint found with reference: {args.reference}")
            print("Available references:")
            for ref in sorted(footprints.keys()):
                print(f"  - {ref}")
    elif args.hide and args.reference and not args.code and not args.show:
        _, footprints = parse_kicad_pcb(pcb_path)
        if args.reference not in footprints:
            print(
                f"Error: No footprint found with reference: {args.reference}"
            )
            sys.exit(1)

        original_footprint = footprints[args.reference]["full_data"]
        modified_footprint = add_hide_to_model(original_footprint)

        replace_footprint_in_file(
            pcb_path, args.reference, modified_footprint
        )
    elif args.show and args.reference and not args.code and not args.hide:
        _, footprints = parse_kicad_pcb(pcb_path)
        if args.reference not in footprints:
            print(
                f"Error: No footprint found with reference: {args.reference}"
            )
            sys.exit(1)

        original_footprint = footprints[args.reference]["full_data"]
        modified_footprint = remove_hide_from_model(original_footprint)

        replace_footprint_in_file(
            pcb_path, args.reference, modified_footprint
        )
    else:
        _, footprints = parse_kicad_pcb(pcb_path)
        print(f"Found {len(footprints)} footprints in {pcb_path.name}:")
        print("Available references:")
        for ref in sorted(footprints.keys()):
            print(f"  - {ref}")
        print("\nUsage:")
        print("  Extract: --code option")
        print("  Hide 3D model: --hide option")
        print("  Show 3D model: --show option")
