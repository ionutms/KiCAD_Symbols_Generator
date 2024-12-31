"""Connector Series Specifications Module.

This module defines data structures and specifications for connector series,
providing a framework for managing connector component information.
"""

from typing import NamedTuple


class SeriesSpec(NamedTuple):
    """Connector series specifications.

    This class defines the complete specifications for a series of connectors,
    including physical characteristics and documentation.

    Attributes:
        manufacturer: Name of the component manufacturer
        base_series: Base model number for the series
        footprint_pattern: Pattern string for generating footprint names
        datasheet: URL to the manufacturer's datasheet
        pin_counts: List of available pin configurations
        trustedparts_link: URL to the component listing on Trusted Parts
        color: Color of the connector housing
        pitch: Pin-to-pin spacing in millimeters
        mounting_angle: Mounting orientation of the connector
        current_rating: Maximum current rating in amperes
        voltage_rating: Maximum voltage rating in volts
        mounting_style: Method of mounting (e.g., Through Hole, SMD)
        contact_plating: Material used for contact plating

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
    current_rating: float
    voltage_rating: int
    mounting_style: str
    contact_plating: str
    reference: str = "J"


class PartInfo(NamedTuple):
    """Component part information structure for individual connectors.

    Attributes:
        symbol_name: Schematic symbol identifier
        reference: Component reference designator (typically "J")
        value: Component value field in schematic
        footprint: PCB footprint identifier
        datasheet: URL to the manufacturer's datasheet
        description: Human-readable component description
        manufacturer: Component manufacturer name
        mpn: Manufacturer part number
        series: Product series identifier
        trustedparts_link: URL to component listing on Trusted Parts
        color: Color of the connector housing
        pitch: Pin-to-pin spacing in millimeters
        pin_count: Number of pins in the connector
        mounting_angle: Mounting orientation of the connector
        current_rating: Maximum current rating in amperes
        voltage_rating: Maximum voltage rating in volts
        mounting_style: Method of mounting (e.g., Through Hole, SMD)
        contact_plating: Material used for contact plating

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
    current_rating: float
    voltage_rating: int
    mounting_style: str
    contact_plating: str


    @classmethod
    def create_part_info(
        cls,
        pin_count: int,
        specs: SeriesSpec,
    ) -> "PartInfo":
        """Create complete part information.

        Args:
            pin_count: Number of pins
            specs: Series specifications

        Returns:
            PartInfo instance with all specifications

        """
        mpn = cls.generate_part_code(pin_count, specs.base_series)
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
        )


    @classmethod
    def generate_part_code(
        cls,
        pin_count: int,
        series_code: str,
    ) -> str:
        """Generate connector part code based on pin count.

        Args:
            pin_count: Number of pins
            series_code: Base series code

        Returns:
            str: Part code string

        """
        return f"{series_code}-{pin_count:02d}BE"


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
            f"{pin_count} positions connector, ",
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
    ) -> list["PartInfo"]:
        """Generate all part numbers for the series.

        Args:
            specs: Series specifications

        Returns:
            List of PartInfo instances

        """
        return [
            cls.create_part_info(pin_count, specs)
            for pin_count in specs.pin_counts]


SYMBOLS_SPECS: dict[str, SeriesSpec] = {
    "TBP02R1-381": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TBP02R1-381",
        footprint_pattern="connector_footprints:TBP02R1-381-{:02d}BE",
        datasheet=(
            "https://www.sameskydevices.com/"
            "product/resource/tbp02r1-381.pdf"),
        pin_counts=[2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16],
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Blue",
        pitch=3.81,
        mounting_angle="Vertical",
        current_rating=8.0,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin"),
    "TBP02R2-381": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TBP02R2-381",
        footprint_pattern="connector_footprints:TBP02R2-381-{:02d}BE",
        datasheet=(
            "https://www.sameskydevices.com/"
            "product/resource/tbp02r2-381.pdf"),
        pin_counts=[2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16],
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Blue",
        pitch=3.81,
        mounting_angle="Vertical",
        current_rating=8.0,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin"),
    "TBP04R1-500": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TBP04R1-500",
        footprint_pattern="connector_footprints:TBP04R1-500-{:02d}BE",
        datasheet=(
            "https://www.sameskydevices.com/"
            "product/resource/tbp04r1-500.pdf"),
        pin_counts=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Blue",
        pitch=5.00,
        mounting_angle="Vertical",
        current_rating=15.0,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin"),
    "TBP04R12-500": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TBP04R12-500",
        footprint_pattern="connector_footprints:TBP04R12-500-{:02d}BE",
        datasheet=(
            "https://www.sameskydevices.com/"
            "product/resource/tbp04r12-500.pdf"),
        pin_counts=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Blue",
        pitch=5.00,
        mounting_angle="Vertical",
        current_rating=15.0,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin"),
    "TBP04R2-500": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TBP04R2-500",
        footprint_pattern="connector_footprints:TBP04R2-500-{:02d}BE",
        datasheet=(
            "https://www.sameskydevices.com/"
            "product/resource/tbp04r2-500.pdf"),
        pin_counts=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Blue",
        pitch=5.00,
        mounting_angle="Vertical",
        current_rating=15.0,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin"),
    "TBP04R3-500": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TBP04R3-500",
        footprint_pattern="connector_footprints:TBP04R3-500-{:02d}BE",
        datasheet=(
            "https://www.sameskydevices.com/"
            "product/resource/tbp04r3-500.pdf"),
        pin_counts=[2, 3, 4, 5, 6],
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Blue",
        pitch=5.00,
        mounting_angle="Vertical",
        current_rating=15.0,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin"),
    "TB004-508": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TB004-508",
        footprint_pattern="connector_footprints:TB004-508-{:02d}BE",
        datasheet=(
            "https://www.sameskydevices.com/"
            "product/resource/tb004-508.pdf"),
        pin_counts=list(range(2, 25)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Blue",
        pitch=5.08,
        mounting_angle="Vertical",
        current_rating=16.0,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin"),
    "TB006-508": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TB006-508",
        footprint_pattern="connector_footprints:TB006-508-{:02d}BE",
        datasheet=(
            "https://www.sameskydevices.com/"
            "product/resource/tb006-508.pdf"),
        pin_counts=list(range(2, 25)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Blue",
        pitch=5.08,
        mounting_angle="Vertical",
        current_rating=12.0,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin"),
}
