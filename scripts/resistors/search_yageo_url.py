"""Module to check Yageo URL for resistors."""

import os
import re
import sys
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utilities import print_message_utilities


def fetch_webpage(url: str) -> str:
    """Fetch webpage content with timing information.

    Args:
        url: The URL to fetch

    Returns:
        The webpage content as text

    Raises:
        requests.exceptions.RequestException: If the request fails

    """
    start_time = time.time()
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36",
    }
    response = requests.get(url, headers=headers, timeout=60)
    response.raise_for_status()
    print_message_utilities.print_info(
        f"Time for HTTP request: {time.time() - start_time:.2f} seconds")
    return response.text


def parse_total_records(page_text: str) -> str:
    """Extract total records count from page text.

    Args:
        page_text: The webpage text content

    Returns:
        The number of records found as a string

    """
    match = re.search(r"Total records\s*(\d+)", page_text)
    return match.group(1) if match else "0"


def extract_part_numbers(soup: BeautifulSoup) -> list[str]:
    """Extract part numbers from webpage tables.

    Args:
        soup: BeautifulSoup object of the parsed webpage

    Returns:
        List of extracted part numbers

    """
    part_numbers = []
    tables = soup.find_all("table")

    for table in tables:
        rows = table.find_all("tr")
        for row in rows[1:]:  # Skip header row
            cells = row.find_all("td")
            if cells:  # Assuming part number is in first column
                part_number = cells[0].get_text(strip=True)
                if part_number:
                    # Remove "Stock" string if present
                    cleaned_part_number = part_number.replace(
                        "Stock", "").strip()
                    if cleaned_part_number:
                        part_numbers.append(cleaned_part_number)

    return part_numbers


def analyze_webpage_content(partnumber_prefix: str) -> tuple[str, list[str]]:
    """Analyze webpage content.

    Args:
        partnumber_prefix: The part number prefix to search for

    Returns:
        A tuple containing:
        - The total number of records found as a string
        - A list of part numbers (empty if no records found)

    """
    base_url = "https://www.yageo.com/en/ProductSearch/PartNumberSearch?"
    url_partnumber = f"part_number={partnumber_prefix}&"
    page_number = 1
    url_page = f"page={page_number}&"
    url_page_size = "page_size=100"

    url = f"{base_url}{url_partnumber}{url_page}{url_page_size}"

    # Fetch webpage
    html_content = fetch_webpage(url)

    # Parse HTML
    start_time = time.time()
    soup = BeautifulSoup(html_content, "html.parser")
    print_message_utilities.print_info(
        f"Time for parsing HTML: {time.time() - start_time:.2f} seconds")

    # Get record count
    number = parse_total_records(soup.get_text())

    all_part_numbers = []

    for page_number in range(1, (int(number))//100 + 2):

        url_page = f"page={page_number}&"
        url = f"{base_url}{url_partnumber}{url_page}{url_page_size}"
        print(url)

        # Fetch webpage
        html_content = fetch_webpage(url)

        # Parse HTML
        start_time = time.time()
        soup = BeautifulSoup(html_content, "html.parser")
        print_message_utilities.print_info(
            f"Time for parsing HTML: {time.time() - start_time:.2f} seconds")

        if number == "0":
            print_message_utilities.print_error(
                f"Total Records: {number}")
            return number, []

        # Extract part numbers
        part_numbers = extract_part_numbers(soup)
        all_part_numbers.extend(part_numbers)

    return number, all_part_numbers


def extract_resistance_value(mpn: str, mpn_prefix: str) -> float:
    """Extract resistance value from MPN."""
    value_code = mpn.replace(mpn_prefix, "")[:-1]

    if "M" in value_code:
        multiplier = 1_000_000
        value = value_code.split("M")
    elif "K" in value_code:
        multiplier = 1_000
        value = value_code.split("K")
    else:
        multiplier = 1
        value = value_code.split("R")

    if len(value) == 2:  # noqa: PLR2004
        return float(value[0] + "." + value[1]) * multiplier
    return float(value[0]) * multiplier


if __name__ == "__main__":
    mpn_prefixes = ["RT0805BRE07"]

    for mpn_prefix in mpn_prefixes:
        file_path = f"data/{mpn_prefix}_part_numbers.csv"
        dataframe = pd.read_csv(file_path)
        mpn_csv_list = dataframe["MPN"].tolist()

        records, partnumbers = analyze_webpage_content(mpn_prefix)
        mpn_web_list = set(partnumbers)

        print(
            f"Number of MPNs in CSV: {len(mpn_csv_list)}, "
            f"Number of MPNs from web: {len(mpn_web_list)}")

        difference_web_csv = [
            part_number for part_number
            in mpn_web_list if part_number not in mpn_csv_list]
        print_message_utilities.print_success(
            f"Parts found on web but not in CSV ({len(difference_web_csv)}):")

        missing_values = [
            extract_resistance_value(part_number, mpn_prefix)
            for part_number in difference_web_csv]
        missing_values.sort()
        print_message_utilities.print_success(
            f"Missing resistance values: {missing_values}")

        difference_csv_web = [
            part_number for part_number
            in mpn_csv_list if part_number not in mpn_web_list]
        print_message_utilities.print_info(
            f"Parts found in CSV but not on web ({len(difference_csv_web)}):")

        missing_values = [
            extract_resistance_value(part_number, mpn_prefix)
            for part_number in difference_csv_web]
        missing_values.sort()
        print_message_utilities.print_info(
            f"Missing resistance values: {missing_values}")

