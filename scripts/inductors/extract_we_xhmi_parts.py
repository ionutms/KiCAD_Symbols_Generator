"""Extract part numbers from product pages.

Extract part numbers from product pages and save them to a CSV file
with inductance, current rating, and DC resistance values.
This script is generic and can be configured for different part series.
Currently supports: WE-XHMI, WE-LHMI, and WE-HCF.
"""

import csv
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

SERIES_CONFIG = {
    "WE-XHMI": {
        "url": "https://www.we-online.com/en/components/products/WE-XHMI",
        "pattern": r"\b(744393\d+|74439\d+)\b",
        "filename": "we_xhmi_parts.csv",
        "inductance_col": 5,
        "current_col": 6,
        "resistance_col": 9,
    },
    "WE-LHMI": {
        "url": "https://www.we-online.com/en/components/products/WE-LHMI",
        "pattern": r"\b(744373\d+|74437\d+)\b",
        "filename": "we_lhmi_parts.csv",
        "inductance_col": 5,
        "current_col": 6,
        "resistance_col": 9,
    },
    "WE-HCF": {
        "url": "https://www.we-online.com/en/components/products/WE-HCF",
        "pattern": r"\b(74436\d{5}\w*|74437\d{5}\w*)\b",
        "filename": "we_hcf_parts.csv",
        "inductance_col": 5,
        "current_col": 6,
        "resistance_col": 9,
    },
}


def extract_part_numbers_with_inductance(
    url,
    part_pattern=r"\b\d{6,}\b",
    inductance_col=5,
    current_col=6,
    resistance_col=9,
):
    """Extract all part numbers and inductance from a product page.

    Args:
        url: The URL of the product page
        part_pattern: Regex pattern to match part numbers
        inductance_col: Column index for inductance value
        current_col: Column index for current rating value
        resistance_col: Column index for resistance value

    Returns:
        list: A list of tuples (part_number, inductance, irp_40k, rdc_max)

    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        parts_data = {}

        for row in soup.find_all("tr"):
            cells = row.find_all("td")
            if (
                len(cells)
                >= max(inductance_col, current_col, resistance_col) + 2
            ):
                order_code_cell = cells[0]
                order_code_text = order_code_cell.get_text(strip=True)

                part_match = re.search(part_pattern, order_code_text)

                if not part_match:
                    for link in order_code_cell.find_all("a"):
                        link_text = link.get_text(strip=True)
                        part_match = re.search(part_pattern, link_text)
                        if part_match:
                            break

                if part_match:
                    part_number = (
                        part_match.group(1)
                        if part_match.lastindex
                        else part_match.group(0)
                    )

                    inductance = None
                    irp_40k = None
                    rdc_max = None

                    cell_texts = [cell.get_text(strip=True) for cell in cells]

                    if len(cell_texts) > inductance_col:
                        num_match = re.search(
                            r"(\d+\.?\d*)", cell_texts[inductance_col]
                        )
                        if num_match:
                            inductance = num_match.group(1)

                    if len(cell_texts) > current_col:
                        num_match = re.search(
                            r"(\d+\.?\d*)", cell_texts[current_col]
                        )
                        if num_match:
                            irp_40k = num_match.group(1)

                    if len(cell_texts) > resistance_col:
                        num_match = re.search(
                            r"(\d+\.?\d*)", cell_texts[resistance_col]
                        )
                        if num_match:
                            rdc_max = num_match.group(1)

                    if part_number:
                        parts_data[part_number] = (
                            inductance if inductance else "N/A",
                            irp_40k if irp_40k else "N/A",
                            rdc_max if rdc_max else "N/A",
                        )

        if not parts_data:
            text = soup.get_text()
            part_numbers = set(re.findall(part_pattern, text))
            for pn in part_numbers:
                parts_data[pn] = ("N/A", "N/A", "N/A")

        parts_list = sorted([
            (pn, ind, irp, rdc) for pn, (ind, irp, rdc) in parts_data.items()
        ])

        return parts_list

    except Exception:
        return []


def extract_part_numbers_from_multiple_urls(
    urls,
    part_pattern=r"\b\d{6,}\b",
    inductance_col=5,
    current_col=6,
    resistance_col=9,
):
    """Extract all part numbers and inductance from multiple product pages.

    Args:
        urls: A list of URLs of the product pages
        part_pattern: Regex pattern to match part numbers
        inductance_col: Column index for inductance value
        current_col: Column index for current rating value
        resistance_col: Column index for resistance value

    Returns:
        list:
            A list of tuples (part_number, inductance, irp_40k, rdc_max)
            from all URLs

    """
    all_parts_data = []

    for url in urls:
        try:
            parts_data = extract_part_numbers_with_inductance(
                url, part_pattern, inductance_col, current_col, resistance_col
            )
            all_parts_data.extend(parts_data)
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
            continue

    unique_parts = {}
    for part_number, inductance, irp_40k, rdc_max in all_parts_data:
        unique_parts[part_number] = (inductance, irp_40k, rdc_max)

    parts_list = sorted([
        (pn, ind, irp, rdc) for pn, (ind, irp, rdc) in unique_parts.items()
    ])

    return parts_list


def save_to_csv(
    parts_data,
    filename="parts.csv",
    headers=[
        "Part Number",
        "Inductance (uH)",
        "IRP,40K (A)",
        "RDC Max (mOhm)",
    ],
):
    """Save part numbers and inductance to a CSV file."""
    script_dir = Path(__file__).parent
    filepath = script_dir / filename

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for pn, inductance, irp_40k, rdc_max in parts_data:
            writer.writerow([pn, inductance, irp_40k, rdc_max])

    print(f"Saved {len(parts_data)} parts to {filepath}")


def process_series(series_name):
    """Process a specific series using its configuration."""
    if series_name not in SERIES_CONFIG:
        print(f"Unknown series: {series_name}")
        print(f"Available series: {', '.join(SERIES_CONFIG.keys())}")
        return

    config = SERIES_CONFIG[series_name]
    print(f"Processing {series_name}...")

    parts_data = extract_part_numbers_with_inductance(
        url=config["url"],
        part_pattern=config["pattern"],
        inductance_col=config["inductance_col"],
        current_col=config["current_col"],
        resistance_col=config["resistance_col"],
    )

    if parts_data:
        save_to_csv(parts_data, filename=config["filename"])
        print(f"Found {len(parts_data)} parts for {series_name}")
    else:
        print(f"No parts found for {series_name}")


def process_all_series():
    """Process all configured series."""
    for series_name in SERIES_CONFIG.keys():
        process_series(series_name)
        print()


if __name__ == "__main__":
    process_all_series()
