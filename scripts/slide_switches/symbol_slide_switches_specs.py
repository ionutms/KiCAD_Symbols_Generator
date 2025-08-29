"""Slide Switches Specifications Module.

This module defines data structures and specifications for slide switches
series, providing a framework for managing slide switch component
information.
"""

from __future__ import annotations

from typing import List, NamedTuple, Optional, Tuple


class SeriesSpec(NamedTuple):
    """Slide switch series specifications.

    This class defines the complete specifications for a series of slide
    switches, including physical characteristics and documentation.

    Attributes:
        manufacturer: Manufacturer name
        base_series: Base series identifier
        footprint_name: Name of the shared footprint (e.g., SS12)
        datasheet: URL to the manufacturer's datasheet
        pin_count: Number of pins
        trustedparts_link: URL to the Trusted Parts slide switch listing
        mounting_angle: Mounting orientation of the slide switch
        mounting_style: Method of mounting (e.g., Through Hole, SMD)
        reference: Reference designator prefix (default: "S")
        number_of_rows: Number of rows of pins
        override_pins_specs:
            Optional list of tuples specifying custom pin configurations
            (pin_number, x, y, angle)

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
    override_pins_specs: Optional[List[Tuple[str, float, float, int]]] = None

    @property
    def footprint_pattern(self) -> str:
        """Generate footprint pattern using the footprint_name."""
        return f"slide_switches_footprints:{self.footprint_name}"


class PartInfo(NamedTuple):
    """Component part information structure for individual slide switches.

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
        trustedparts_link: URL to the Trusted Parts slide switch listing
        pin_count: Number of pins
        mounting_angle: Mounting orientation of the slide switch
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
        """Create complete part information from series specifications.

        Args:
            specs: Series specifications

        Returns:
            PartInfo instance with all specifications

        """
        mpn = cls.generate_part_code(specs.base_series)
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
        series_code: str,
    ) -> str:
        """Generate slide switch part code.

        Args:
            series_code: Base series code

        Returns:
            Part code string

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
    "8SS1012-Z": SeriesSpec(
        manufacturer="Nidec Components Corporation",
        base_series="8SS1012-Z",
        footprint_name="8SS1012-Z",
        datasheet="https://www.nidec-components.com/e/catalog/switch/8ss.pdf",
        pin_count=3,
        trustedparts_link="https://www.trustedparts.com/en/search",
        number_of_rows=1,
        mounting_angle="Vertical",
        mounting_style="Through Hole",
        override_pins_specs=[
            ("1", 5.08, -2.54, 180),
            ("2", -5.08, 0, 0),
            ("3", 5.08, 2.54, 180),
        ],
    )
}
