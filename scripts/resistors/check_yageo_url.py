"""Check Yageo URLs for missing parts.

This script checks the URLs in a CSV file for missing parts. It uses the
requests library to fetch the webpage content and the BeautifulSoup library to
parse the HTML. It then searches for the pattern "Total records" followed by
numbers to determine the number of parts available. If the number of parts is
zero, it extracts the resistance value from the CSV file and adds it to a list
of missing parts.

"""

import os
import re
import sys
import time
from collections import defaultdict

import pandas as pd
import requests
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utilities import print_message_utilities


def analyze_webpage_content(url: str) -> str:
    """Analyze the content of a webpage to determine the number of parts.

    Args:
        url: The URL of the webpage to analyze.

    Returns:
        The number of parts available on the webpage.

    """
    number = "0"
    try:
        start_time = time.time()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36",
        }
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        print_message_utilities.print_info(
            f"Time for HTTP request: {time.time() - start_time:.2f} seconds",
        )

        start_time = time.time()
        # Create BeautifulSoup object to parse HTML
        soup = BeautifulSoup(response.text, "html.parser")
        print_message_utilities.print_info(
            f"Time for parsing HTML: {time.time() - start_time:.2f} seconds",
        )

        start_time = time.time()
        # Get all text content
        page_text = soup.get_text()

        start_time = time.time()
        # Look for the pattern "Total records" followed by numbers
        match = re.search(r"Total records\s*([\d,]+)", page_text)

        print_message_utilities.print_info(f"\nURL: {url}")
        if match:
            number = match.group(1).replace(",", "")
            if number == "0":
                print_message_utilities.print_error(
                    f"Total Records: {number}",
                )
            else:
                print_message_utilities.print_success(
                    f"Total Records: {number}",
                )

    except requests.exceptions.RequestException as e:
        print_message_utilities.print_error(
            f"Error fetching the webpage: {e}",
        )
    except Exception as e:  # noqa: BLE001
        print_message_utilities.print_error(f"An error occurred: {e}")

    return number


def convert_resistance_string(resistance_str: str) -> float:
    """Convert a resistance string with units to a float value.

    Args:
        resistance_str: The resistance string to convert.

    Returns:
        The resistance value as a float.

    Raises:
        ValueError: If the resistance string is invalid.

    """
    # Define multipliers for prefixes
    multipliers = {
        "": 1,
        "k": 1e3,
        "M": 1e6,
        "G": 1e9,
    }

    # Extract the numeric part and the prefix
    match = re.match(r"(\d+(\.\d+)?)\s*([kMG]?)Ω", resistance_str)
    if not match:
        msg = f"Invalid resistance value: {resistance_str}"
        raise ValueError(msg)

    value, _, prefix = match.groups()
    return round(float(value) * multipliers[prefix], 2)


def check_url(
    csv_file_path: str,
    patern: str,
) -> None:
    """Check the URLs in a CSV file for missing parts.

    Args:
        csv_file_path: The path to the CSV file.
        patern: The pattern to search for in the CSV file.

    Returns:
        None

    """
    dataframe: pd.DataFrame = pd.read_csv(f"{csv_file_path}")
    missing_parts = defaultdict(list)
    if (dataframe["Series"] == patern).any():
        for index, url in enumerate(dataframe["Datasheet"]):
            parts = analyze_webpage_content(url)
            if parts == "0":
                resistance_value = convert_resistance_string(
                    dataframe["Value"][index],
                )
                missing_parts[patern].append(resistance_value)
                missing_parts[patern].sort()
            print_message_utilities.print_error(
                f"Missing Parts: {missing_parts.items()} "
                f"at search number {index}",
            )


if __name__ == "__main__":
    mpn_prefixes = ["RC0402FR-7W"]

    for mpn_prefix in mpn_prefixes:
        file_path = f"data/{mpn_prefix}_part_numbers.csv"
        dataframe = pd.read_csv(file_path)
        resistance_values = [
            convert_resistance_string(val) for val in dataframe["Value"]
        ]
        print_message_utilities.print_success(
            f"Initial Resistance values: {resistance_values}",
        )
        print_message_utilities.print_info(
            f"{len(resistance_values)} parts found",
        )

        check_url(file_path, mpn_prefix)
