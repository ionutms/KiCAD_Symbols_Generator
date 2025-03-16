"""Utility module for colored console message printing.

This module provides functions for printing formatted messages to the console
using different colors to indicate different message types.
Uses colorama for cross-platform colored terminal text.
"""

from colorama import Fore, Style, init

init(autoreset=True)


def print_success(message: str) -> None:
    """Print a success message in green color.

    Args:
        message (str): The message to be printed

    """
    print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")


def print_error(message: str) -> None:
    """Print an error message in red color.

    Args:
        message (str): The error message to be printed

    """
    print(f"{Fore.RED}{message}{Style.RESET_ALL}")


def print_info(message: str) -> None:
    """Print an informational message in yellow color.

    Args:
        message (str): The information message to be printed

    """
    print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")
