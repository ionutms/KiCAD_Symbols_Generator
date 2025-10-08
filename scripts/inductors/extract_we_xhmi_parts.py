"""Extract part numbers.

Extract part numbers from the WE-XHMI product page and save them to a CSV file
with inductance, current rating, and DC resistance values.
"""

import csv
import re

import requests
from bs4 import BeautifulSoup


def extract_part_numbers_with_inductance(url):
    """Extract all part numbers and inductance from the WE-XHMI product page.

    Args:
        url: The URL of the WE-XHMI product page

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
            if len(cells) >= 11:
                order_code_cell = cells[0]
                order_code_text = order_code_cell.get_text(strip=True)

                part_match = re.search(
                    r"\b(744393\d+|74439\d+)\b", order_code_text
                )

                if not part_match:
                    for link in order_code_cell.find_all("a"):
                        link_text = link.get_text(strip=True)
                        part_match = re.search(
                            r"\b(744393\d+|74439\d+)\b", link_text
                        )
                        if part_match:
                            break

                if part_match:
                    part_number = part_match.group(1)

                    inductance = None
                    irp_40k = None
                    rdc_max = None

                    cell_texts = [cell.get_text(strip=True) for cell in cells]

                    if len(cell_texts) > 5:
                        num_match = re.search(r"(\d+\.?\d*)", cell_texts[5])
                        if num_match:
                            inductance = num_match.group(1)

                    if len(cell_texts) > 6:
                        num_match = re.search(r"(\d+\.?\d*)", cell_texts[6])
                        if num_match:
                            irp_40k = num_match.group(1)

                    if len(cell_texts) > 9:
                        num_match = re.search(r"(\d+\.?\d*)", cell_texts[9])
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
            part_numbers = set(re.findall(r"\b(744393\d+|74439\d+)\b", text))
            for pn in part_numbers:
                parts_data[pn] = ("N/A", "N/A", "N/A")

        parts_list = sorted([
            (pn, ind, irp, rdc) for pn, (ind, irp, rdc) in parts_data.items()
        ])

        return parts_list

    except Exception:
        return []


def save_to_csv(parts_data, filename="we_xhmi_parts.csv"):
    """Save part numbers and inductance to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Part Number",
            "Inductance (uH)",
            "IRP,40K (A)",
            "RDC Max (mOhm)",
        ])
        for pn, inductance, irp_40k, rdc_max in parts_data:
            writer.writerow([pn, inductance, irp_40k, rdc_max])


if __name__ == "__main__":
    url = "https://www.we-online.com/en/components/products/WE-XHMI"

    parts_data = extract_part_numbers_with_inductance(url)

    if parts_data:
        save_to_csv(parts_data)
    else:
        pass