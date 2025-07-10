"""Connector Series Specifications Module.

This module defines data structures and specifications for tactile switches series,
providing a framework for managing tactile switches component information.
"""

from __future__ import annotations

from typing import NamedTuple


class SeriesSpec(NamedTuple):
    """Connector series specifications.

    This class defines the complete specifications for a series of tactile switches,
    including physical characteristics and documentation.

    Attributes:
        manufacturer: Manufacturer name
        base_series: Base series identifier
        footprint_name: Name of the shared footprint (e.g., TS21)
        datasheet: URL to the manufacturer's datasheet
        pin_count: Number of pins
        trustedparts_link: URL to the Trusted Parts tactile switches listing
        mounting_angle: Mounting orientation of the tactile switches
        mounting_style: Method of mounting (e.g., Through Hole, SMD)
        reference: Reference designator prefix (default: "S")
        number_of_rows: Number of rows of pins
    """

    manufacturer: str
    base_series: str
    footprint_name: str
    datasheet: str
    pin_count: int
    trustedparts_link: str
    mounting_angle: str
    mounting_style: str
    reference: str = "S"
    number_of_rows: int = 1

    @property
    def footprint_pattern(self) -> str:
        """Generate footprint pattern using the footprint_name."""
        return f"tactile_switches_footprints:{self.footprint_name}"


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
        pin_count: Number of pins
        mounting_angle: Mounting orientation of the tactile switches
        mounting_style: Method of mounting (e.g., Through Hole, SMD)
        number_of_rows: Number of rows of pins
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
    pin_count: int
    mounting_angle: str
    mounting_style: str
    number_of_rows: int

    @classmethod
    def create_part_info(
        cls,
        specs: SeriesSpec,
    ) -> PartInfo:
        """Create complete part information.

        Args:
            specs: Series specifications

        Returns:
            PartInfo instance with all specifications
        """
        mpn = cls.generate_part_code(
            specs.pin_count,
            specs.base_series,
            specs.manufacturer,
        )
        trustedparts_link = f"{specs.trustedparts_link}/{mpn}"

        return PartInfo(
            symbol_name=f"{specs.reference}_{mpn}",
            reference=specs.reference,
            value=mpn,
            footprint=specs.footprint_pattern,
            datasheet=specs.datasheet,
            description=cls.create_description(specs),
            manufacturer=specs.manufacturer,
            mpn=mpn,
            series=specs.base_series,
            trustedparts_link=trustedparts_link,
            pin_count=specs.pin_count,
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
        specs: SeriesSpec,
    ) -> str:
        """Create component description with comprehensive specifications.

        Args:
            specs: Series specifications

        Returns:
            Formatted description string including all relevant specifications
        """
        parts = [
            f"{specs.manufacturer}",
            f"{specs.base_series} series, ",
            f"{specs.pin_count} positions tactile switch, ",
            f"{specs.mounting_angle} mounting, ",
            f"{specs.mounting_style}, ",
        ]

        return " ".join(parts)

    @classmethod
    def generate_part_numbers(
        cls,
        specs: SeriesSpec,
    ) -> list[PartInfo]:
        """Generate part number for the series.

        Args:
            specs: Series specifications

        Returns:
            List containing a single PartInfo instance
        """
        return [cls.create_part_info(specs)]


SYMBOLS_SPECS: dict[str, SeriesSpec] = {
    "TS21-34-035-BK-260-SMT-TR": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TS21-34-035-BK-260-SMT-TR",
        footprint_name="TS21",
        datasheet="https://www.sameskydevices.com/product/resource/ts21.pdf",
        pin_count=2,
        trustedparts_link="https://www.trustedparts.com/en/search",
        number_of_rows=2,
        mounting_angle="Vertical",
        mounting_style="Surface Mount",
    ),
    "TS21-34-035-BK-160-SMT-TR": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TS21-34-035-BK-160-SMT-TR",
        footprint_name="TS21",
        datasheet="https://www.sameskydevices.com/product/resource/ts21.pdf",
        pin_count=2,
        trustedparts_link="https://www.trustedparts.com/en/search",
        number_of_rows=2,
        mounting_angle="Vertical",
        mounting_style="Surface Mount",
    ),
    "TS24-62-14-BL-200-SMT-TR-67": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TS24-62-14-BL-200-SMT-TR-67",
        footprint_name="TS24-BL",
        datasheet="https://www.sameskydevices.com/product/resource/ts24.pdf",
        pin_count=2,
        trustedparts_link="https://www.trustedparts.com/en/search",
        number_of_rows=2,
        mounting_angle="Vertical",
        mounting_style="Surface Mount",
    ),
    "TS24-62-14-BL-250-SMT-TR-67": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TS24-62-14-BL-250-SMT-TR-67",
        footprint_name="TS24-BL",
        datasheet="https://www.sameskydevices.com/product/resource/ts24.pdf",
        pin_count=2,
        trustedparts_link="https://www.trustedparts.com/en/search",
        number_of_rows=2,
        mounting_angle="Vertical",
        mounting_style="Surface Mount",
    ),
    "TS24-62-14-CL-250-SMT-TR-67": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TS24-62-14-CL-250-SMT-TR-67",
        footprint_name="TS24-CL",
        datasheet="https://www.sameskydevices.com/product/resource/ts24.pdf",
        pin_count=2,
        trustedparts_link="https://www.trustedparts.com/en/search",
        number_of_rows=2,
        mounting_angle="Vertical",
        mounting_style="Surface Mount",
    ),
    "TS24-62-14-CL-200-SMT-TR-67": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TS24-62-14-CL-200-SMT-TR-67",
        footprint_name="TS24-CL",
        datasheet="https://www.sameskydevices.com/product/resource/ts24.pdf",
        pin_count=2,
        trustedparts_link="https://www.trustedparts.com/en/search",
        number_of_rows=2,
        mounting_angle="Vertical",
        mounting_style="Surface Mount",
    ),
    "TS29-1212-1-R-300-D": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TS29-1212-1-R-300-D",
        footprint_name="TS29-R",
        datasheet="https://www.sameskydevices.com/product/resource/ts29.pdf",
        pin_count=2,
        trustedparts_link="https://www.trustedparts.com/en/search",
        number_of_rows=2,
        mounting_angle="Vertical",
        mounting_style="Through Hole",
    ),
}
