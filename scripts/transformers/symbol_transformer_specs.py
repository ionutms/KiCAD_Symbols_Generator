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

from __future__ import annotations

from typing import NamedTuple


class PinConfig(NamedTuple):
    """Configuration specification for a single transformer pin.

    Attributes:
        number: Pin number identifier
        y_pos: Vertical position of the pin on the component
        pin_type: Type of pin (e.g., "unspecified", "no_connect")
        lenght: Length of the pin in millimeters
        hide: Flag to hide the pin in the schematic (default: False)

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
        left:
            List of PinConfig instances for the left side of the transformer
        right:
            List of PinConfig instances for the right side of the transformer

    """

    left: list[PinConfig]
    right: list[PinConfig]
    right_alternative: list[PinConfig] | None = None


class SeriesSpec(NamedTuple):
    """Specifications for a series of coupled inductors.

    Comprehensive specification for a transformer series, including electrical
    characteristics, documentation references, and mechanical specifications.

    Attributes:
        manufacturer: Name of the component manufacturer
        base_series: Identifier for the transformer series
        footprint: KiCAD footprint identifier
        tolerance: Inductance value tolerance specification
        datasheet: URL to component datasheet
        primary_inductance: Typical primary inductance in µH
        trustedparts_link: URL to component listing on Trusted Parts
        value_suffix: Suffix for the component value
        turns_ratio: Transformer turns ratio specification
        pin_config: Pin configuration for the transformer
        max_dc_resistance: Maximum DC resistance for the transformer
        reference: Reference designator prefix for the series (default: "T")

    """

    manufacturer: str
    base_series: str
    footprint: str
    tolerance: str
    datasheet: str
    primary_inductance: float
    trustedparts_link: str
    value_suffix: str
    turns_ratio: dict[dict[str, str]]
    pin_config: SidePinConfig
    max_dc_resistance: dict[dict[str, str]]
    reference: str = "T"


class PartInfo(NamedTuple):
    """Detailed specification for an individual transformer component.

    Provides a complete description of a single transformer component,
    including electrical specifications, documentation references,
    and sourcing information.

    Attributes:
        symbol_name: Name of the KiCAD symbol for the component
        reference: Reference designator prefix for the series
        value: Inductance value in µH
        footprint: KiCAD footprint identifier
        datasheet: URL to component datasheet
        description: Detailed description of the component
        manufacturer: Name of the component manufacturer
        primary_inductance: Primary inductance in µH
        mpn: Manufacturer part number for the component
        tolerance: Inductance value tolerance specification
        series: Base series identifier for the component
        trustedparts_link: URL to component listing on Trusted Parts
        max_dc_resistance: Maximum DC resistance for the component
        turns_ratio: Transformer turns ratio specification

    """

    symbol_name: str
    reference: str
    value: float
    footprint: str
    datasheet: str
    description: str
    manufacturer: str
    primary_inductance: float
    mpn: str
    tolerance: str
    series: str
    trustedparts_link: str
    max_dc_resistance: dict[dict[str, str]]
    turns_ratio: dict[dict[str, str]]

    @staticmethod
    def format_inductance_value(primary_inductance: float) -> str:
        """Format inductance value for display.

        Args:
            primary_inductance: Inductance value in µH

        Returns:
            Formatted inductance value string

        """
        if primary_inductance < 1:
            return f"{int(primary_inductance * 1000)} nH"
        if isinstance(primary_inductance, int):
            return f"{primary_inductance} µH"
        return f"{primary_inductance:.1f} µH"

    @classmethod
    def create_description(
        cls,
        value: float,
        specs: SeriesSpec,
    ) -> str:
        """Create a detailed description for the component.

        Args:
            value: Inductance value in µH
            specs: Series specifications

        Returns:
            Detailed description string for the component

        """
        parts = [
            cls.format_inductance_value(value),
            specs.tolerance,
        ]

        return " ".join(parts)

    @classmethod
    def create_part_info(
        cls,
        primary_inductance: float,
        specs: SeriesSpec,
    ) -> PartInfo:
        """Create a PartInfo instance for a transformer component.

        Args:
            primary_inductance: Primary inductance value in µH
            specs: Series specifications

        Returns:
            PartInfo instance for the transformer component

        """
        mpn = f"{specs.base_series}{specs.value_suffix}"
        trustedparts_link = f"{specs.trustedparts_link}/{mpn}"

        return cls(
            symbol_name=f"{specs.reference}_{mpn}",
            reference=specs.reference,
            value=primary_inductance,
            footprint=specs.footprint,
            datasheet=specs.datasheet,
            description=cls.create_description(primary_inductance, specs),
            manufacturer=specs.manufacturer,
            primary_inductance=primary_inductance,
            mpn=mpn,
            tolerance=specs.tolerance,
            series=specs.base_series,
            trustedparts_link=trustedparts_link,
            max_dc_resistance=specs.max_dc_resistance,
            turns_ratio=specs.turns_ratio,
        )

    @classmethod
    def generate_part_numbers(
        cls,
        specs: SeriesSpec,
    ) -> list[PartInfo]:
        """Generate part numbers for a transformer series.

        Args:
            specs: Series specifications

        Returns:
            List of PartInfo instances for the transformer series

        """
        return [
            cls.create_part_info(specs.primary_inductance, specs),
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
            "cc4df0c9-0883-48fa-b8fb-d5dedac2b455/za9384.pdf"
        ),
        primary_inductance=470,
        max_dc_resistance={"pri": "1.1", "sec": "1.6"},
        value_suffix="-ALD",
        trustedparts_link="https://www.trustedparts.com/en/search",
        turns_ratio={"pri : sec": "1 : 1"},
        pin_config=SidePinConfig(
            left=[
                PinConfig("4", 5.08, "unspecified", 5.08),
                PinConfig("5", 2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("3", 0.0, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("1", -2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("2", -5.08, "unspecified", 5.08),
            ],
            right=[
                PinConfig("6", 5.08, "unspecified", 5.08),
                PinConfig("7", 2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("8", 0.0, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("9", -2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("10", -5.08, "unspecified", 5.08),
            ],
        ),
    ),
    "ZA9644": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="ZA9644",
        footprint="transformer_footprints:ZA9644",
        tolerance="±10%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "cc4df0c9-0883-48fa-b8fb-d5dedac2b455/za9384.pdf"
        ),
        turns_ratio={"pri : sec": "1 : 1"},
        primary_inductance=470,
        max_dc_resistance={"pri": "1.8", "sec": "1.8"},
        value_suffix="-AED",
        trustedparts_link="https://www.trustedparts.com/en/search",
        pin_config=SidePinConfig(
            left=[
                PinConfig("1", 5.08, "unspecified", 5.08),
                PinConfig("2", 2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("3", -2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("4", -5.08, "unspecified", 5.08),
            ],
            right=[
                PinConfig("5", 5.08, "unspecified", 5.08),
                PinConfig("6", 2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("7", -2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("8", -5.08, "unspecified", 5.08),
            ],
        ),
    ),
    "750315836": SeriesSpec(
        manufacturer="Wurth Elektronik",
        base_series="750315836",
        footprint="transformer_footprints:750315836",
        tolerance="±10%",
        datasheet=(
            "https://www.we-online.com/components/products/datasheet/"
            "750315836.pdf"
        ),
        turns_ratio={"N1+N2 : N3": "1 : 1"},
        primary_inductance=40,
        max_dc_resistance={"pri": "0.095", "sec": "0.09"},
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
                PinConfig("9", 5.08, "unspecified", 5.08),
                PinConfig("6", 2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("8", 0.0, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("10", -2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("7", -5.08, "unspecified", 5.08),
            ],
            right_alternative=[
                PinConfig("9", -5.08, "unspecified", 5.08),
                PinConfig("6", 2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("8", 0.0, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("10", -2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("7", 5.08, "unspecified", 5.08),
            ],
        ),
    ),
    "YA8779": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="YA8779",
        footprint="transformer_footprints:YA8779",
        tolerance="±10%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "26e99d96-72df-4173-a685-a01606cc3452/ya8779.pdf"
        ),
        turns_ratio={"pri : sec1": "1 : 0.33"},
        primary_inductance=30,
        max_dc_resistance={"pri": "0.14", "sec": "0.013"},
        value_suffix="-BLD",
        trustedparts_link="https://www.trustedparts.com/en/search",
        pin_config=SidePinConfig(
            left=[
                PinConfig("1", 5.08, "unspecified", 5.08),
                PinConfig("2", 2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("3", -2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("4", -5.08, "unspecified", 5.08),
            ],
            right=[
                PinConfig("8", 7.62, "unspecified", 2.54),
                PinConfig("7", 5.08, "unspecified", 2.54),
                PinConfig("5", -5.08, "unspecified", 2.54),
                PinConfig("6", -7.62, "unspecified", 2.54),
            ],
        ),
    ),
    "YA8916": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="YA8916",
        footprint="transformer_footprints:YA8916",
        tolerance="±10%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "26e99d96-72df-4173-a685-a01606cc3452/ya8779.pdf"
        ),
        turns_ratio={"pri : sec1": "1 : 1", "pri : sec2": "1 : 0.52"},
        primary_inductance=30,
        max_dc_resistance={"pri": "0.36", "sec1": "0.695", "sec2": "0.392"},
        value_suffix="-BLD",
        trustedparts_link="https://www.trustedparts.com/en/search",
        pin_config=SidePinConfig(
            left=[
                PinConfig("1", 5.08, "unspecified", 5.08),
                PinConfig("2", 2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("3", -2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("4", -5.08, "unspecified", 5.08),
            ],
            right=[
                PinConfig("8", 12.7, "unspecified", 5.08),
                PinConfig("7", 2.54, "unspecified", 5.08),
                PinConfig("6", -2.54, "unspecified", 5.08),
                PinConfig("5", -12.7, "unspecified", 5.08),
            ],
        ),
    ),
    "YA8864": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="YA8864",
        footprint="transformer_footprints:YA8864",
        tolerance="±10%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "26e99d96-72df-4173-a685-a01606cc3452/ya8779.pdf"
        ),
        turns_ratio={"pri : sec1": "1 : 1.5", "pri : sec2": "1 : 0.4"},
        primary_inductance=30,
        max_dc_resistance={"pri": "0.18", "sec1": "0.68", "sec2": "0.18"},
        value_suffix="-BLD",
        trustedparts_link="https://www.trustedparts.com/en/search",
        pin_config=SidePinConfig(
            left=[
                PinConfig("1", 5.08, "unspecified", 5.08),
                PinConfig("2", 2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("3", -2.54, "no_connect", 2.54, True),  # noqa: FBT003
                PinConfig("4", -5.08, "unspecified", 5.08),
            ],
            right=[
                PinConfig("8", 12.7, "unspecified", 5.08),
                PinConfig("7", 2.54, "unspecified", 5.08),
                PinConfig("6", -2.54, "unspecified", 5.08),
                PinConfig("5", -12.7, "unspecified", 5.08),
            ],
        ),
    ),
    "PL160X9-102L": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="PL160X9-102L",
        footprint="transformer_footprints:PL160X9-102L",
        tolerance="±10%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "2a17d20e-ce43-41cf-8df1-58b60bcf2330/pl160.pdf"
        ),
        turns_ratio={"pri1 : sec": "5 : 4", "pri2 : sec": "5 : 4"},
        primary_inductance=378,
        max_dc_resistance={"pri1": "0.185", "pri2": "0.185", "sec": "0.0068"},
        value_suffix="-BLD",
        trustedparts_link="https://www.trustedparts.com/en/search",
        pin_config=SidePinConfig(
            left=[
                PinConfig("2", 2.54 * 7, "unspecified", 5.08),
                PinConfig("4", 2.54 * 3, "unspecified", 5.08),
                PinConfig("3", 5.08, "unspecified", 5.08),
                PinConfig("5", -5.08, "unspecified", 5.08),
                PinConfig("1", -2.54 * 3, "unspecified", 5.08),
                PinConfig("6", -2.54 * 7, "unspecified", 5.08),
            ],
            right=[
                PinConfig("7", 20.32, "unspecified", 5.08),
                PinConfig("8", 10.16, "unspecified", 5.08),
                PinConfig("9", 0, "unspecified", 5.08),
                PinConfig("10", -10.16, "unspecified", 5.08),
                PinConfig("11", -20.32, "unspecified", 5.08),
            ],
        ),
    ),
    "PL300X9-102L": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="PL300X9-102L",
        footprint="transformer_footprints:PL300X9-102L",
        tolerance="±10%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "636aef6f-8168-4ece-bb01-e16574e130d8/pl300.pdf"
        ),
        turns_ratio={"pri1 : sec": "5 : 4", "pri2 : sec": "5 : 4"},
        primary_inductance=378,
        max_dc_resistance={"pri1": "0.009", "pri2": "0.009", "sec": "0.0042"},
        value_suffix="-BLD",
        trustedparts_link="https://www.trustedparts.com/en/search",
        pin_config=SidePinConfig(
            left=[
                PinConfig("2", 2.54 * 7, "unspecified", 5.08),
                PinConfig("4", 2.54 * 3, "unspecified", 5.08),
                PinConfig("3", 5.08, "unspecified", 5.08),
                PinConfig("5", -5.08, "unspecified", 5.08),
                PinConfig("1", -2.54 * 3, "unspecified", 5.08),
                PinConfig("6", -2.54 * 7, "unspecified", 5.08),
            ],
            right=[
                PinConfig("7", 20.32, "unspecified", 5.08),
                PinConfig("8", 10.16, "unspecified", 5.08),
                PinConfig("9", 0, "unspecified", 5.08),
                PinConfig("10", -10.16, "unspecified", 5.08),
                PinConfig("11", -20.32, "unspecified", 5.08),
            ],
        ),
    ),
}
