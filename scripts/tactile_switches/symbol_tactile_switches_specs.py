"""Connector Series Specifications Module.

This module defines data structures and specifications for tactile switches series,
providing a framework for managing tactile switches component information.
"""

from __future__ import annotations

from typing import NamedTuple


class SeriesSpec(NamedTuple):
    """Connector series specifications.

    This class defines the complete specifications for a series of tactile switchess,
    including physical characteristics and documentation.

    Attributes:
        manufacturer: Manufacturer name
        base_series: Base series identifier
        footprint_pattern: KiCad footprint pattern string
        datasheet: URL to the manufacturer's datasheet
        pin_counts: List of available pin counts
        trustedparts_link: URL to the Trusted Parts tactile switches listing
        color: Color of the tactile switches housing
        pitch: Pin-to-pin spacing in millimeters
        mounting_angle: Mounting orientation of the tactile switches
        mounting_style: Method of mounting (e.g., Through Hole, SMD)
        contact_plating: Material used for contact plating
        reference: Reference designator prefix (default: "J")

    """

    manufacturer: str
    base_series: str
    footprint_pattern: str
    datasheet: str
    pin_counts: list[int]
    trustedparts_link: str
    color: str
    mounting_angle: str
    mounting_style: str
    reference: str = "S"
    number_of_rows: int = 1


class PartInfo(NamedTuple):
    """Component part information structure for individual connectors.

    Attributes:
        symbol_name: KiCad symbol name
        reference: Reference designator prefix
        value: Part value (MPN)
        footprint: KiCad footprint name
        datasheet: URL to the manufacturer's datasheet
        description: Comprehensive component description
        manufacturer: Manufacturer name
        mpn: Manufacturer part number
        series: Base series identifier
        trustedparts_link: URL to the Trusted Parts tactile switches listing
        color: Color of the tactile switches housing
        pitch: Pin-to-pin spacing in millimeters
        pin_count: Number of pins
        mounting_angle: Mounting orientation of the tactile switches
        mounting_style: Method of mounting (e.g., Through Hole, SMD)

    """

    symbol_name: str
    reference: str
    value: str
    footprint: str
    datasheet: str
    description: str
    manufacturer: str
    mpn: str
    series: str
    trustedparts_link: str
    color: str
    pin_count: int
    mounting_angle: str
    mounting_style: str
    number_of_rows: int

    @classmethod
    def create_part_info(
        cls,
        pin_count: int,
        specs: SeriesSpec,
    ) -> PartInfo:
        """Create complete part information.

        Args:
            pin_count: Number of pins
            specs: Series specifications

        Returns:
            PartInfo instance with all specifications

        """
        mpn = cls.generate_part_code(
            pin_count,
            specs.base_series,
            specs.manufacturer,
        )
        footprint = specs.footprint_pattern.format(pin_count)
        trustedparts_link = f"{specs.trustedparts_link}/{mpn}"

        return PartInfo(
            symbol_name=f"{specs.reference}_{mpn}",
            reference=specs.reference,
            value=mpn,
            footprint=footprint,
            datasheet=specs.datasheet,
            description=cls.create_description(pin_count, specs),
            manufacturer=specs.manufacturer,
            mpn=mpn,
            series=specs.base_series,
            trustedparts_link=trustedparts_link,
            color=specs.color,
            pin_count=pin_count,
            mounting_angle=specs.mounting_angle,
            mounting_style=specs.mounting_style,
            number_of_rows=specs.number_of_rows,
        )

    @classmethod
    def generate_part_code(
        cls,
        pin_count: int,
        series_code: str,
        manufacturer: str,
    ) -> str:
        """Generate tactile switches part code based on pin count.

        Args:
            pin_count: Number of pins
            series_code: Base series code
            manufacturer: Manufacturer Name

        Returns:
            str: Part code string

        """
        return f"{series_code}"

    @classmethod
    def create_description(
        cls,
        pin_count: int,
        specs: SeriesSpec,
    ) -> str:
        """Create component description with comprehensive specifications.

        Args:
            pin_count: Number of pins
            specs: Series specifications

        Returns:
            Formatted description string including all relevant specifications

        """
        parts = [
            f"{specs.manufacturer}",
            f"{specs.base_series} series, ",
            f"{pin_count} positions tactile switch, ",
            f"{specs.color}, ",
            f"{specs.mounting_angle} mounting, ",
            f"{specs.mounting_style}, ",
        ]

        return " ".join(parts)

    @classmethod
    def generate_part_numbers(
        cls,
        specs: SeriesSpec,
    ) -> list[PartInfo]:
        """Generate all part numbers for the series.

        Args:
            specs: Series specifications

        Returns:
            List of PartInfo instances

        """
        return [
            cls.create_part_info(pin_count, specs)
            for pin_count in specs.pin_counts
        ]


SYMBOLS_SPECS: dict[str, SeriesSpec] = {
    "TS21-34-035-BK-260-SMT-TR": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TS21-34-035-BK-260-SMT-TR",
        footprint_pattern="tactile_switches_footprints:TS21-34-035-BK-260-SMT-TR",
        datasheet=(
            "https://www.sameskydevices.com/product/resource/ts21.pdf"
        ),
        pin_counts=[2],
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        number_of_rows=2,
        mounting_angle="Vertical",
        mounting_style="Surface Mount",
    ),
}
