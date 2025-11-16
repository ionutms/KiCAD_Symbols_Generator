"""Terminal Block Series Specifications Module.

This module defines data structures and specifications for terminal block
series, providing a framework for managing terminal block component
information.
"""

from __future__ import annotations

from typing import NamedTuple


class SeriesSpec(NamedTuple):
    """Terminal block series specifications.

    This class defines the complete specifications for a series of terminal
    blocks, including physical characteristics and documentation.

    Attributes:
        manufacturer: Manufacturer name
        base_series: Base series identifier
        footprint_pattern: KiCad footprint pattern string
        datasheet: URL to the manufacturer's datasheet
        pin_counts: List of available pin counts
        trustedparts_link: URL to the Trusted Parts terminal block listing
        color: Color of the terminal block housing
        pitch: Pin-to-pin spacing in millimeters
        mounting_angle: Mounting orientation of the terminal block
        current_rating: Maximum current rating in amperes
        voltage_rating: Maximum voltage rating in volts
        mounting_style: Method of mounting (e.g., Through Hole, SMD)
        contact_plating: Material used for contact plating
        reference: Reference designator prefix (default: "J")
        rectangle_width:
            Width of the terminal block symbol rectangle (default: 5.08mm)
        pin_names:
            Optional dictionary mapping pin identifiers to pin names
            (default: None)
        symbol_pin_length:
            Optional override for symbol pin length in mm (default: 2.54)

    """

    manufacturer: str
    base_series: str
    footprint_pattern: str
    datasheet: str
    pin_counts: list[int]
    trustedparts_link: str
    color: str
    pitch: float
    mounting_angle: str
    current_rating: float | str
    voltage_rating: int
    mounting_style: str
    contact_plating: str
    reference: str = "J"
    number_of_rows: int = 1
    rectangle_width: float = 5.08
    pin_names: dict[str, str] | None = None
    symbol_pin_length: float = 2.54


class PartInfo(NamedTuple):
    """Component part information structure for individual terminal blocks.

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
        trustedparts_link: URL to the Trusted Parts terminal block listing
        color: Color of the terminal block housing
        pitch: Pin-to-pin spacing in millimeters
        pin_count: Number of pins
        mounting_angle: Mounting orientation of the terminal block
        current_rating: Maximum current rating in amperes
        voltage_rating: Maximum voltage rating in volts
        mounting_style: Method of mounting (e.g., Through Hole, SMD)
        contact_plating: Material used for contact plating
        rectangle_width: Width of the terminal block symbol rectangle

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
    pitch: float
    pin_count: int
    mounting_angle: str
    current_rating: float | str
    voltage_rating: int
    mounting_style: str
    contact_plating: str
    number_of_rows: int
    rectangle_width: float = 5.08

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
            pitch=specs.pitch,
            pin_count=pin_count,
            mounting_angle=specs.mounting_angle,
            current_rating=specs.current_rating,
            voltage_rating=specs.voltage_rating,
            mounting_style=specs.mounting_style,
            contact_plating=specs.contact_plating,
            number_of_rows=specs.number_of_rows,
            rectangle_width=specs.rectangle_width,
        )

    @classmethod
    def generate_part_code(
        cls,
        pin_count: int,
        series_code: str,
        manufacturer: str,
    ) -> str:
        """Generate terminal block part code based on pin count.

        Args:
            pin_count: Number of pins
            series_code: Base series code
            manufacturer: Manufacturer Name

        Returns:
            str: Part code string

        """
        if manufacturer == "Same Sky":
            return f"{series_code}-{pin_count:02d}BE"
        if manufacturer == "Amphenol Anytek":
            return f"{series_code}{pin_count:02d}31530000G"
        # else if manufacturer is Samtec
        return f"{series_code.replace('xx', f'{pin_count:02d}')}"

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
            f"{pin_count} positions terminal block, ",
            f"{specs.pitch} mm pitch, ",
            f"{specs.color}, ",
            f"{specs.mounting_angle} mounting, ",
            f"{specs.current_rating} A, ",
            f"{specs.voltage_rating} V, ",
            f"{specs.mounting_style}, ",
            f"{specs.contact_plating} plated",
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
    "TBP02P1-381": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TBP02P1-381",
        footprint_pattern="terminal_block_footprints:TBP02P1-381-{:02d}BE",
        datasheet=(
            "https://www.sameskydevices.com/product/resource/tbp02p1-381.pdf"
        ),
        pin_counts=list(range(2, 25)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Blue",
        pitch=3.81,
        mounting_angle="Vertical",
        current_rating=8.0,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin",
    ),
    "TJ": SeriesSpec(
        manufacturer="Amphenol Anytek",
        base_series="TJ",
        footprint_pattern="terminal_block_footprints:TJ{:02d}31530000G",
        datasheet=(
            "http://www.anytek.com.tw/UserUpFiles/20181017/vCheHtsK2_to.pdf"
        ),
        pin_counts=list(range(2, 11)) + [12] + list(range(16, 25)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Green",
        pitch=3.81,
        mounting_angle="Vertical",
        current_rating=8.0,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin",
    ),
}
