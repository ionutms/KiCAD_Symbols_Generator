"""Library for managing coupled inductor series specifications and part info.

This module provides data structures and definitions for various Coilcraft
coupled coupled inductor series, including their specifications and individual
component information.
It is used to maintain a standardized database of coupled coupled inductor
specifications and generate consistent part information.
"""

from typing import NamedTuple

from utilities import print_message_utilities


class PinConfig(NamedTuple):
    """Configuration specification for a single transformer pin.

    Attributes:
        number: Pin number identifier
        y_pos: Vertical position of the pin center in millimeters
        pin_type: Pin type identifier (e.g., "unspecified", "power")
        lenght: Pin length in millimeters
        hide: If True, hide the pin in the symbol drawing

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
    right_alternative: list[PinConfig]


class SeriesSpec(NamedTuple):
    """Coupled inductor series specifications for Coilcraft components.

    This class defines the complete specifications for a series of inductors,
    including physical, electrical, and documentation characteristics.

    Attributes:
        manufacturer: Component manufacturer name
        base_series: Product series identifier
        footprint: PCB footprint identifier
        tolerance: Component value tolerance
        datasheet: URL to the manufacturer's datasheet
        inductance_values: List of available inductance values in µH
        trustedparts_link: URL to component listing on Trusted Parts
        value_suffix: Coilcraft value code suffix
        max_dc_current: List of maximum DC current ratings in Amperes (A)
        max_dc_resistance: List of maximum DC resistance in milliohms (mΩ)
        pin_config: SidePinConfig
        reference: Reference designator prefix (default: "L")

    """

    manufacturer: str
    base_series: str
    footprint: str
    tolerance: str
    datasheet: str
    inductance_values: list[float]
    trustedparts_link: str
    value_suffix: str
    max_dc_current: list[float]
    max_dc_resistance: list[float]
    pin_config: SidePinConfig
    reference: str = "L"


class PartInfo(NamedTuple):
    """Component part information structure for individual inductors.

    This class contains all necessary information to fully specify a single
    coupled inductor component, including its specifications, documentation,
    and sourcing information.

    Attributes:
        symbol_name: KiCad symbol name
        reference: Reference designator prefix
        value: Inductance value in µH
        footprint: PCB footprint identifier
        datasheet: URL to the manufacturer's datasheet
        description: Component description string
        manufacturer: Component manufacturer name
        mpn: Manufacturer part number
        tolerance: Component value tolerance
        series: Base series identifier
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
            return f"{int(inductance * 1000)} nH"
        return f"{inductance} µH"

    @classmethod
    def create_description(
        cls,
        inductance: float,
        specs: "SeriesSpec",
    ) -> str:
        """Create component description.

        Args:
            inductance: Value in µH
            specs: Series specifications

        Returns:
            Description string

        """
        parts = [
            "COUPLED INDUCTOR SMD",
            cls.format_inductance_value(inductance),
            specs.tolerance,
        ]

        return " ".join(parts)

    @classmethod
    def generate_value_code(
        cls,
        inductance: float,
        value_suffix: str,
        manufacturer: str,
    ) -> str:
        """Generate Coilcraft value code for inductance values.

        The value code consists of:
        1. Two digits representing the significant
            figures of the inductance value
        2. A decimal position indicator (0-4)
        3. Optional AEC qualification suffix

        Decimal position indicators:
        - 4: Multiply by 10 µH (100.0-999.99 µH)
        - 3: Value is in µH (10.0-99.99 µH)
        - 2: Divide by 10 µH (1.0-9.99 µH)
        - 1: Divide by 100 µH (0.1-0.99 µH)
        - 0: Divide by 1000 µH (0.01-0.099 µH)

        Args:
            inductance:
                Value in µH (microhenries), must be between 0.01 and 999.99
            value_suffix:
                AEC qualification suffix to append when is_aec is True
            manufacturer:
                Manufacturer name for value code generation

        Returns:
            str: Value code string.

        Raises:
            ValueError:
                If inductance is outside the valid range (0.01-9999.99 µH)

        """
        if inductance >= 1000.0:  # noqa: PLR2004
            value = round(inductance / 100)
            base_code = (
                f"{value:02d}5"
                if manufacturer == "Coilcraft"
                else f"{value:02d}2"
            )
            return f"{base_code}{value_suffix}"

        if inductance >= 100.0:  # noqa: PLR2004
            value = round(inductance / 10)
            base_code = (
                f"{value:02d}4"
                if manufacturer == "Coilcraft"
                else f"{value:02d}1"
            )
            return f"{base_code}{value_suffix}"

        if inductance >= 10.0:  # noqa: PLR2004
            value = round(inductance)
            base_code = (
                f"{value:02d}3"
                if manufacturer == "Coilcraft"
                else f"{value:02d}0"
            )
            return f"{base_code}{value_suffix}"

        if inductance >= 1.0:
            value = round(inductance * 10)
            base_code = f"{value:02d}2"
            return f"{base_code}{value_suffix}"

        if inductance >= 0.1:  # noqa: PLR2004
            value = round(inductance * 100)
            base_code = f"{value:02d}1"
            return f"{base_code}{value_suffix}"

        value = round(inductance * 1000)
        base_code = f"{value:02d}0"
        return f"{base_code}{value_suffix}"

    @classmethod
    def create_part_info(
        cls,
        inductance: float,
        specs: SeriesSpec,
    ) -> "PartInfo":
        """Create complete part information.

        Args:
            inductance: Value in µH
            specs: Series specifications
            is_aec: If True, create AEC-Q200 qualified part

        Returns:
            PartInfo instance with all specifications

        """
        value_code = cls.generate_value_code(
            inductance,
            specs.value_suffix,
            specs.manufacturer,
        )
        mpn = f"{specs.base_series}-{value_code}"
        trustedparts_link = f"{specs.trustedparts_link}/{mpn}"

        try:
            index = specs.inductance_values.index(inductance)
            max_dc_current = float(specs.max_dc_current[index])
            max_dc_resistance = float(specs.max_dc_resistance[index])
        except ValueError:
            print_message_utilities.print_error(
                f"Error: Inductance value {inductance} µH "
                f"not found in series {specs.base_series}",
            )
            max_dc_current = 0.0
            max_dc_resistance = 0.0
        except IndexError:
            print_message_utilities.print_error(
                "Error: No DC specifications found for inductance "
                f"{inductance} µH in series {specs.base_series}",
            )
            max_dc_current = 0.0
            max_dc_resistance = 0.0

        return cls(
            symbol_name=f"{specs.reference}_{mpn}",
            reference=specs.reference,
            value=inductance,
            footprint=specs.footprint,
            datasheet=specs.datasheet,
            description=cls.create_description(inductance, specs),
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
    ) -> list["PartInfo"]:
        """Generate all part numbers for the series.

        Args:
            specs: Series specifications
            is_aec: If True, generate AEC-Q200 qualified parts

        Returns:
            List of PartInfo instances

        """
        return [
            cls.create_part_info(value, specs)
            for value in specs.inductance_values
        ]


SYMBOLS_SPECS: dict[str, SeriesSpec] = {
    "MSD7342": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="MSD7342",
        footprint="coupled_inductor_footprints:MSD7342",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "bd00e7ca-3707-4fbb-84fc-c9b381ce0e78/msd7342.pdf"
        ),
        inductance_values=[
            *[2.5, 3.3, 4.7, 5.6, 6.8, 8.2, 10, 12, 15, 18],
            *[22, 27, 33, 39, 47, 56, 68, 82, 100, 120],
            *[150, 180, 220, 270, 330, 390, 470, 560, 680, 820],
            *[1000],
        ],
        max_dc_current=[
            *[3.06, 2.89, 2.46, 2.22, 2.10, 2.03, 1.76, 1.61, 1.54, 1.35],
            *[1.19, 1.11, 1.07, 0.90, 0.86, 0.82, 0.72, 0.67, 0.63, 0.55],
            *[0.48, 0.45, 0.42, 0.36, 0.34, 0.32, 0.28, 0.26, 0.25, 0.21],
            *[0.2],
        ],
        max_dc_resistance=[
            *[0.033, 0.037, 0.051, 0.063, 0.07, 0.075, 0.1, 0.12, 0.13, 0.17],
            *[0.22, 0.25, 0.27, 0.38, 0.42, 0.46, 0.6, 0.68, 0.77, 1.03],
            *[1.35, 1.52, 1.72, 2.41, 2.7, 3.05, 4.0, 4.43, 5.0, 6.8],
            *[7.8],
        ],
        value_suffix="ML",
        trustedparts_link="https://www.trustedparts.com/en/search",
        pin_config=SidePinConfig(
            left=[
                PinConfig("1", 5.08, "passive", 5.08),
                PinConfig("3", -5.08, "passive", 5.08),
            ],
            right=[
                PinConfig("2", 5.08, "passive", 5.08),
                PinConfig("4", -5.08, "passive", 5.08),
            ],
            right_alternative=[
                PinConfig("2", -5.08, "passive", 5.08),
                PinConfig("4", 5.08, "passive", 5.08),
            ],
        ),
    ),
    "MSD1048": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="MSD1048",
        footprint="coupled_inductor_footprints:MSD1048",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "2945f640-8140-48a6-993e-28832f57720a/msd1048.pdf"
        ),
        inductance_values=[10.0, 22.0, 47.0, 68.0, 100.0],
        max_dc_current=[2.1, 1.9, 1.6, 1.4, 1.2],
        max_dc_resistance=[0.053, 0.098, 0.208, 0.297, 0.387],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
        pin_config=SidePinConfig(
            left=[
                PinConfig("1", 5.08, "passive", 5.08),
                PinConfig("3", -5.08, "passive", 5.08),
            ],
            right=[
                PinConfig("4", 5.08, "passive", 5.08),
                PinConfig("2", -5.08, "passive", 5.08),
            ],
            right_alternative=[
                PinConfig("4", -5.08, "passive", 5.08),
                PinConfig("2", 5.08, "passive", 5.08),
            ],
        ),
    ),
    "MSD1260": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="MSD1260",
        footprint="coupled_inductor_footprints:MSD1260",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "79bacbf1-ec2a-4e20-9b30-12448424231b/msd1260.pdf"
        ),
        inductance_values=[
            *[4.7, 5.6, 6.8, 8.2, 10, 12, 15, 18],
            *[22, 27, 33, 39, 47, 56, 68, 82, 100],
        ],
        max_dc_current=[
            *[4.47, 4.24, 3.88, 3.72, 3.46, 3.12, 2.92, 2.73],
            *[2.49, 2.41, 2.32, 2.25, 2.03, 1.91, 1.83, 1.62, 1.5],
        ],
        max_dc_resistance=[
            *[0.036, 0.04, 0.048, 0.052, 0.06, 0.074, 0.085, 0.097],
            *[0.116, 0.124, 0.134, 0.142, 0.174, 0.198, 0.216, 0.274, 0.322],
        ],
        value_suffix="ML",
        trustedparts_link="https://www.trustedparts.com/en/search",
        pin_config=SidePinConfig(
            left=[
                PinConfig("1", 5.08, "passive", 5.08),
                PinConfig("3", -5.08, "passive", 5.08),
            ],
            right=[
                PinConfig("2", 5.08, "passive", 5.08),
                PinConfig("4", -5.08, "passive", 5.08),
            ],
            right_alternative=[
                PinConfig("2", -5.08, "passive", 5.08),
                PinConfig("4", 5.08, "passive", 5.08),
            ],
        ),
    ),
    "SRF0905A": SeriesSpec(
        manufacturer="Bourns",
        base_series="SRF0905A",
        footprint="coupled_inductor_footprints:SRF0905A",
        tolerance="±20%",
        datasheet=("https://bourns.com/docs/product-datasheets/srf0905a.pdf"),
        inductance_values=[
            *[10, 25, 40, 50, 250, 470, 500],
            *[1000, 2000, 4700, 6500],
        ],
        max_dc_current=[
            *[1.6, 1, 0.9, 0.8, 1.2, 1.1, 1],
            *[0.8, 0.6, 0.4, 0.3],
        ],
        max_dc_resistance=[
            *[0.08, 0.16, 0.25, 0.32, 0.13, 0.14, 0.15],
            *[0.31, 0.42, 0.9, 1.05],
        ],
        value_suffix="Y",
        trustedparts_link="https://www.trustedparts.com/en/search",
        pin_config=SidePinConfig(
            left=[
                PinConfig("1", 5.08, "passive", 5.08),
                PinConfig("4", -5.08, "passive", 5.08),
            ],
            right=[
                PinConfig("2", -5.08, "passive", 5.08),
                PinConfig("3", 5.08, "passive", 5.08),
            ],
            right_alternative=[
                PinConfig("2", 5.08, "passive", 5.08),
                PinConfig("3", -5.08, "passive", 5.08),
            ],
        ),
    ),
}
