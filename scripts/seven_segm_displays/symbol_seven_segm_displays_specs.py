"""Seven Segment Display Series Specifications Module."""

from __future__ import annotations

from typing import NamedTuple


class SeriesSpec(NamedTuple):
    """Seven segment display series specifications."""

    manufacturer: str
    base_series: str
    footprint_pattern: str
    datasheet: str
    pin_count: int
    trustedparts_link: str
    color: str
    pitch: float
    mounting_angle: str
    mounting_style: str
    display_type: str
    reference: str = "DS"
    number_of_rows: int = 1
    rectangle_width: float = 7.62
    pin_names: dict[str, str] | None = None
    symbol_pin_length: float = 2.54


class PartInfo(NamedTuple):
    """Component part information structure."""

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
    mounting_style: str
    display_type: str
    number_of_rows: int
    rectangle_width: float = 7.62

    @classmethod
    def create_part_info(
        cls,
        pin_count: int,
        specs: SeriesSpec,
    ) -> PartInfo:
        """Create complete part information."""
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
            mounting_style=specs.mounting_style,
            display_type=specs.display_type,
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
        """Generate seven segment display part code based on pin count."""
        # For fixed part numbers like 157142B12803, return as is
        return series_code

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
            "Seven Segment Display, ",
            f"{pin_count} pins, ",
            f"{specs.display_type}, ",
            f"{specs.color} segments, ",
            f"{specs.mounting_angle} mounting, ",
            f"{specs.mounting_style}",
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
        return [cls.create_part_info(specs.pin_count, specs)]


SYMBOLS_SPECS: dict[str, SeriesSpec] = {
    "157119B12801": SeriesSpec(
        manufacturer="Würth Elektronik",
        base_series="157119B12801",
        footprint_pattern="seven_segm_display_footprints:157119B12801",
        datasheet=(
            "https://www.we-online.com/components/products/datasheet/"
            "157119B12801.pdf"
        ),
        pin_count=10,
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Blue",
        pitch=2.54,
        mounting_angle="Vertical",
        mounting_style="Through Hole",
        display_type="Common Anode",
        reference="DS",
        rectangle_width=2.54 * 6,
        pin_names={
            "1": "E",
            "2": "D",
            "3": "Anode",
            "4": "C",
            "5": "DP",
            "6": "B",
            "7": "A",
            "8": "Anode",
            "9": "F",
            "10": "G",
        },
    ),
    "157143B12800": SeriesSpec(
        manufacturer="Würth Elektronik",
        base_series="157143B12800",
        footprint_pattern="seven_segm_display_footprints:157143B12800",
        datasheet=(
            "https://www.we-online.com/components/products/datasheet/"
            "157143B12800.pdf?"
            "srsltid=AfmBOopWIjRtx3PotVrKoA5nX-pDkrLhAJL8G0V-MiBL1VxnND_REzTM"
        ),
        pin_count=10,
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Blue",
        pitch=2.54,
        mounting_angle="Vertical",
        mounting_style="Surface Mount",
        display_type="Common Anode",
        reference="DS",
        rectangle_width=2.54 * 6,
        pin_names={
            "1": "E",
            "2": "D",
            "3": "Anode",
            "4": "C",
            "5": "DP",
            "6": "B",
            "7": "A",
            "8": "Anode",
            "9": "F",
            "10": "G",
        },
    ),
    "157143V12800": SeriesSpec(
        manufacturer="Würth Elektronik",
        base_series="157143V12800",
        footprint_pattern="seven_segm_display_footprints:157143V12800",
        datasheet=(
            "https://www.we-online.com/components/products/datasheet/"
            "157143V12800.pdf"
        ),
        pin_count=10,
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Bright Green",
        pitch=2.54,
        mounting_angle="Vertical",
        mounting_style="Surface Mount",
        display_type="Common Anode",
        reference="DS",
        rectangle_width=2.54 * 6,
        pin_names={
            "1": "E",
            "2": "D",
            "3": "Anode",
            "4": "C",
            "5": "DP",
            "6": "B",
            "7": "A",
            "8": "Anode",
            "9": "F",
            "10": "G",
        },
    ),
    "FYS-15011BUHR-21": SeriesSpec(
        manufacturer="Würth Elektronik",
        base_series="FYS-15011BUHR-21",
        footprint_pattern="seven_segm_display_footprints:FYS-15011BUHR-21",
        datasheet=(
            "https://cetest02.cn-bj.ufileos.com/100001_2003185297/"
            "83%20FYS-15011A-BX-XX.pdf"
        ),
        pin_count=10,
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Red",
        pitch=2.54,
        mounting_angle="Vertical",
        mounting_style="Through Hole",
        display_type="Common Anode",
        reference="DS",
        rectangle_width=2.54 * 6,
        pin_names={
            "1": "Anode",
            "2": "E",
            "3": "D",
            "4": "C",
            "5": "Anode",
            "6": "B",
            "7": "A",
            "8": "DP",
            "9": "F",
            "10": "G",
        },
    ),
}
