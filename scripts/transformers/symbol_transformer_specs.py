"""Module for defining and managing transformer component specifications.

This module provides data structures and configurations
for managing transformer and coupled inductor specifications,
particularly for Coilcraft components.
It includes definitions for pin layouts, series specifications,
and individual component details used in electronic design.

The module supports:
- Pin configuration management for transformer components
- Series specifications for different transformer families
- Detailed part information tracking for individual components
- Standard configurations for common transformer layouts
"""

from typing import NamedTuple, Optional


class PinConfig(NamedTuple):
    """Configuration specification for a single transformer pin.

    Attributes:
        number: Pin identifier/number as string (e.g., "1", "2")
        y_pos: Vertical position of the pin in millimeters relative to center
        pin_type: Pin type specification (e.g., "unspecified", "no_connect")
        hide: Boolean flag indicating if pin should be hidden in schematic

    """

    number: str
    y_pos: float
    pin_type: str
    lenght: float
    hide: bool = False


class SidePinConfig(NamedTuple):
    """Pin configuration specification for both sides of a transformer.

    Defines the complete pin layout for a transformer by specifying pins
    on both the left and right sides of the component.

    Attributes:
        left: List of PinConfig objects for the left side pins
        right: List of PinConfig objects for the right side pins

    """

    left: list[PinConfig]
    right: list[PinConfig]


class SeriesSpec(NamedTuple):
    """Specifications for a series of coupled inductors.

    Comprehensive specification for a transformer series, including electrical
    characteristics, documentation references, and mechanical specifications.

    Attributes:
        manufacturer: Name of the component manufacturer
        base_series: Base series identifier for the component family
        footprint: PCB footprint identifier for the component series
        tolerance: Component value tolerance specification
        datasheet: URL to the manufacturer's datasheet
        inductance_values: List of available inductance values in µH
        trustedparts_link: URL to component listing on Trusted Parts
        value_suffix: Suffix used in part numbering for the series
        has_aec: Boolean indicating AEC-Q200 qualification status
        max_dc_current: List of maximum DC current ratings in Amperes (A)
        max_dc_resistance:
            List of maximum DC resistance values in milliohms (mΩ)
        pin_config: Optional pin configuration specification

    """

    manufacturer: str
    base_series: str
    footprint: str
    tolerance: str
    datasheet: str
    inductance_values: list[float]
    trustedparts_link: str
    value_suffix: str
    has_aec: bool = True
    max_dc_current: list[float] = []  # noqa: RUF012
    max_dc_resistance: list[float] = []  # noqa: RUF012
    pin_config: Optional[SidePinConfig] = None  # noqa: FA100
    reference: str = "T"


class PartInfo(NamedTuple):
    """Detailed specification for an individual transformer component.

    Provides a complete description of a single transformer component,
    including electrical specifications, documentation references,
    and sourcing information.

    Attributes:
        symbol_name: Schematic symbol identifier for the component
        reference: Component reference designator used in schematics
        value: Inductance value in microhenries (µH)
        footprint: PCB footprint identifier
        datasheet: URL to component datasheet
        description: Human-readable component description
        manufacturer: Name of component manufacturer
        mpn: Manufacturer part number
        tolerance: Component value tolerance specification
        series: Product series identifier
        trustedparts_link: URL to component listing on Trusted Parts
        max_dc_current: Maximum DC current rating in Amperes (A)
        max_dc_resistance: Maximum DC resistance in milliohms (mΩ)

    """

    symbol_name: str
    reference: str
    value: float
    footprint: str
    datasheet: str
    description: str
    manufacturer: str
    mpn: str
    tolerance: str
    series: str
    trustedparts_link: str
    max_dc_current: float
    max_dc_resistance: float

    @staticmethod
    def format_inductance_value(inductance: float) -> str:
        """Format inductance value with appropriate unit.

        Shows integer values where possible (no decimal places needed).

        Args:
            inductance: Value in µH

        Returns:
            Formatted string with unit

        """
        if inductance < 1:
            return f"{int(inductance*1000)} nH"
        if inductance.is_integer():
            return f"{int(inductance)} µH"
        return f"{inductance:.1f} µH"

    @classmethod
    def create_description(
        cls,
        value: float,
        specs: "SeriesSpec",
        is_aec: bool,  # noqa: FBT001
    ) -> str:
        """Create component description.

        Args:
            value: Inductance value in µH
            specs: Series specifications
            is_aec: If True, add AEC-Q200 qualification

        Returns:
            Formatted description string

        """
        parts = [
            "POWER TRANSFORMER SMD",
            cls.format_inductance_value(value),
            specs.tolerance,
        ]

        if is_aec and specs.has_aec:
            parts.append("AEC-Q200")

        return " ".join(parts)

    @classmethod
    def create_part_info(
        cls,
        inductance: float,
        specs: SeriesSpec,
        is_aec: bool = True,  # noqa: FBT001, FBT002
    ) -> "PartInfo":
        """Create complete part information.

        Args:
            inductance: Value in µH
            specs: Series specifications
            is_aec: If True, create AEC-Q200 qualified part

        Returns:
            PartInfo instance with all specifications

        """
        mpn = f"{specs.base_series}{specs.value_suffix}"
        trustedparts_link = f"{specs.trustedparts_link}/{mpn}"

        try:
            index = specs.inductance_values.index(inductance)
            max_dc_current = float(specs.max_dc_current[index])
            max_dc_resistance = float(specs.max_dc_resistance[index])
        except (ValueError, IndexError):
            msg = (
                f"Error: Inductance value {inductance} µH "
                f"not found in series {specs.base_series}"
            )
            raise ValueError(msg)  # noqa: B904

        return cls(
            symbol_name=f"{specs.reference}_{mpn}",
            reference=specs.reference,
            value=inductance,
            footprint=specs.footprint,
            datasheet=specs.datasheet,
            description=cls.create_description(inductance, specs, is_aec),
            manufacturer=specs.manufacturer,
            mpn=mpn,
            tolerance=specs.tolerance,
            series=specs.base_series,
            trustedparts_link=trustedparts_link,
            max_dc_current=max_dc_current,
            max_dc_resistance=max_dc_resistance,
        )

    @classmethod
    def generate_part_numbers(
        cls,
        specs: SeriesSpec,
        is_aec: bool = True,  # noqa: FBT001, FBT002
    ) -> list["PartInfo"]:
        """Generate all part numbers for the series.

        Args:
            specs: Series specifications
            is_aec: If True, generate AEC-Q200 qualified parts

        Returns:
            List of PartInfo instances

        """
        return [
            cls.create_part_info(value, specs, is_aec)
            for value in specs.inductance_values
        ]


# Series specifications for supported transformer families
SYMBOLS_SPECS: dict[str, SeriesSpec] = {
    "ZA9384": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="ZA9384",
        footprint="transformer_footprints:ZA9384",
        tolerance="±10%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "cc4df0c9-0883-48fa-b8fb-d5dedac2b455/za9384.pdf"),
        inductance_values=[470.0],
        max_dc_current=[0.80],
        max_dc_resistance=[1.1],
        value_suffix="-ALD",
        trustedparts_link="https://www.trustedparts.com/en/search",
        pin_config=SidePinConfig(
            left=[
                PinConfig("4", 5.08, "unspecified", 5.08),
                PinConfig("5", 2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("3", 0.0, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("1", -2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("2", -5.08, "unspecified", 5.08)],
            right=[
                PinConfig("6", 5.08, "unspecified", 5.08),
                PinConfig("7", 2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("8", 0.0, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("9", -2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("10", -5.08, "unspecified", 5.08)],
        ),
    ),
    "ZA9644": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="ZA9644",
        footprint="transformer_footprints:ZA9644",
        tolerance="±10%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "cc4df0c9-0883-48fa-b8fb-d5dedac2b455/za9384.pdf"),
        inductance_values=[470.0],
        max_dc_current=[0.49],
        max_dc_resistance=[1.8],
        value_suffix="-AED",
        trustedparts_link="https://www.trustedparts.com/en/search",
        pin_config=SidePinConfig(
            left=[
                PinConfig("1", 5.08, "unspecified", 5.08),
                PinConfig("2", 2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("3", -2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("4", -5.08, "unspecified", 5.08)],
            right=[
                PinConfig("5", 5.08, "unspecified", 5.08),
                PinConfig("6", 2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("7", -2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("8", -5.08, "unspecified", 5.08)],
        ),
    ),
    "750315836": SeriesSpec(
        manufacturer="Wurth Elektronik",
        base_series="750315836",
        footprint="transformer_footprints:750315836",
        tolerance="±10%",
        datasheet=(
            "https://www.we-online.com/components/products/datasheet/"
            "750315836.pdf"),
        inductance_values=[40.0],
        max_dc_current=[3.2],
        max_dc_resistance=[0.095],
        value_suffix="",
        trustedparts_link="https://www.trustedparts.com/en/search",
        pin_config=SidePinConfig(
            left=[
                PinConfig("3", 10.16, "unspecified", 5.08),
                PinConfig("1", 5.08, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("4", 0.0, "unspecified", 5.08),
                PinConfig("2", -5.08, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("5", -10.16, "unspecified", 5.08),
                ],
            right=[
                PinConfig("7", 5.08, "unspecified", 5.08),
                PinConfig("6", 2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("8", 0.0, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("10", -2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("9", -5.08, "unspecified", 5.08)],
        ),
    ),
    "YA8779": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="YA8779",
        footprint="transformer_footprints:YA8779",
        tolerance="±10%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "26e99d96-72df-4173-a685-a01606cc3452/ya8779.pdf"),
        inductance_values=[24.0],
        max_dc_current=[1.2],
        max_dc_resistance=[0.14],
        value_suffix="-BLD",
        trustedparts_link="https://www.trustedparts.com/en/search",
        pin_config=SidePinConfig(
            left=[
                PinConfig("1", 5.08, "unspecified", 5.08),
                PinConfig("2", 2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("3", -2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("4", -5.08, "unspecified", 5.08)],
            right=[
                PinConfig("8", 7.62, "unspecified", 2.54),
                PinConfig("7", 5.08, "unspecified", 2.54),
                PinConfig("5", -5.08, "unspecified", 2.54),
                PinConfig("6", -7.62, "unspecified", 2.54)],
        ),
    ),
}
