"""Extract part numbers.

Extract part numbers from the WE-XHMI product page and
save them to a CSV file with inductance values.
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
        list: A list of tuples (part_number, inductance, irp_40k)

    """
    try:
        # Fetch the webpage
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse the HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Dictionary to store part numbers with their inductance
        parts_data = {}

        # Find the product table - look for table rows
        for row in soup.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) >= 8:  # Ensure we have enough columns
                # First cell typically contains the order code
                order_code_cell = cells[0]
                order_code_text = order_code_cell.get_text(strip=True)

                # Extract part number from the cell
                part_match = re.search(
                    r"\b(744393\d+|74439\d+)\b", order_code_text
                )

                # Also check links in the cell
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

                    # Extract inductance (L) and IRP,40K
                    inductance = None
                    irp_40k = None

                    # Parse each cell to find the values
                    for idx, cell in enumerate(
                        cells[1:10]
                    ):  # Check relevant columns
                        cell_text = cell.get_text(strip=True)
                        # Look for numeric values
                        num_match = re.search(r"^(\d+\.?\d*)$", cell_text)
                        if num_match:
                            # First numeric value is likely inductance
                            if inductance is None:
                                inductance = cell_text
                            # Second numeric value is likely IRP,40K
                            elif irp_40k is None:
                                irp_40k = cell_text

                    if part_number and inductance:
                        parts_data[part_number] = (
                            inductance,
                            irp_40k if irp_40k else "N/A",
                        )

        # If table parsing didn't work well, try alternative method
        if not parts_data:
            # Look for patterns in the entire page
            text = soup.get_text()
            # This is a fallback - try to find part numbers
            part_numbers = set(re.findall(r"\b(744393\d+|74439\d+)\b", text))
            for pn in part_numbers:
                parts_data[pn] = ("N/A", "N/A")

        # Convert to sorted list of tuples
        parts_list = sorted([
            (pn, ind, irp) for pn, (ind, irp) in parts_data.items()
        ])

        return parts_list

    except Exception as e:
        print(f"Error extracting part numbers: {e}")
        return []


def save_to_csv(parts_data, filename="we_xhmi_parts.csv"):
    """Save part numbers and inductance to a CSV file."""
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Part Number", "Inductance (µH)", "IRP,40K (A)"])
        for pn, inductance, irp_40k in parts_data:
            writer.writerow([pn, inductance, irp_40k])
    print(f"Saved {len(parts_data)} part numbers to {filename}")


if __name__ == "__main__":
    # URL of the WE-XHMI product page
    url = "https://www.we-online.com/en/components/products/WE-XHMI"

    print(
        "Extracting part numbers, inductance, and IRP,40K from WE-XHMI page"
    )
    parts_data = extract_part_numbers_with_inductance(url)

    if parts_data:
        print(f"\nFound {len(parts_data)} unique part numbers:\n")

        # Display first 10 and last 10
        for i, (pn, ind, irp) in enumerate(parts_data[:10], 1):
            print(f"{i}. {pn} - {ind} µH - {irp} A")

        if len(parts_data) > 20:
            print("...")
            for i, (pn, ind, irp) in enumerate(
                parts_data[-10:], len(parts_data) - 9
            ):
                print(f"{i}. {pn} - {ind} µH - {irp} A")
        elif len(parts_data) > 10:
            for i, (pn, ind, irp) in enumerate(parts_data[10:], 11):
                print(f"{i}. {pn} - {ind} µH - {irp} A")

        # Save to CSV
        print("\nSaving to CSV...")
        save_to_csv(parts_data)

    else:
        print("No part numbers found or an error occurred.")
