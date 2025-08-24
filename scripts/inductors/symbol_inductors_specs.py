"""Library for managing inductor specifications.

This module provides data structures and definitions for various Coilcraft
inductor series, including their specifications and individual component
information. It is used to maintain a standardized database of inductor
specifications and generate consistent part information.
"""

import os
import sys
from typing import NamedTuple

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utilities import print_message_utilities


class SeriesSpec(NamedTuple):
    """Inductor series specifications for Coilcraft components.

    This class defines the complete specifications for a series of inductors,
    including physical, electrical, and documentation characteristics.

    Attributes:
        manufacturer: Manufacturer name
        base_series: Series identifier
        footprint: KiCad footprint name
        tolerance: Inductance tolerance
        datasheet: URL to the series datasheet
        inductance_values: List of available inductance values
        trustedparts_link: URL to the TrustedParts search page
        max_dc_current: List of maximum DC current ratings
        max_dc_resistance: List of maximum DC resistance ratings
        value_suffix: AEC qualification suffix
        reference: Component reference prefix (default: "L")

    """

    manufacturer: str
    base_series: str
    footprint: str
    tolerance: str
    datasheet: str
    inductance_values: list[float]
    trustedparts_link: str
    max_dc_current: list[float]
    max_dc_resistance: list[float]
    value_suffix: str = ""
    reference: str = "L"


class PartInfo(NamedTuple):
    """Component part information structure for individual inductors.

    This class contains all necessary information to fully specify a single
    inductor component, including its specifications, documentation, and
    sourcing information.

    Attributes:
        symbol_name: KiCad symbol name
        reference: Component reference prefix
        value: Inductance value in µH
        footprint: KiCad footprint name
        datasheet: URL to the component datasheet
        description: Component description string
        manufacturer: Manufacturer name
        mpn: Manufacturer part number
        tolerance: Inductance tolerance
        series: Series identifier
        trustedparts_link: URL to the TrustedParts search page
        max_dc_current: Maximum DC current rating in A
        max_dc_resistance: Maximum DC resistance rating in Ω

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
    def format_value(inductance: float) -> str:
        """Format inductance value with appropriate unit.

        Shows integer values where possible (no decimal places needed).

        Args:
            inductance: Inductance value in µH

        Returns:
            Formatted inductance string

        """
        if inductance < 1e-6:  # noqa: PLR2004
            return f"{int(inductance * 1e9)} nH"
        if inductance < 1:
            return f"{int(inductance * 1000)} nH"
        return f"{inductance:.1f} µH"

    @staticmethod
    def generate_value_code(
        inductance: float,
        value_suffix: str,
    ) -> str:
        """Generate inductance values according to part numbering system.

        Args:
            inductance: Inductance value in µH
            value_suffix: AEC qualification suffix

        Raises:
            ValueError: If inductance value is out of range

        Returns:
            Formatted inductance value code

        """
        if inductance >= 100.0:  # noqa: PLR2004
            value = round(inductance / 10)
            base_code = f"{value:02d}4"
            return f"{base_code}{value_suffix}"

        if inductance >= 10.0:  # noqa: PLR2004
            value = round(inductance)
            base_code = f"{value:02d}3"
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

    @staticmethod
    def generate_wurth_value_code(inductance: float) -> str:
        """Generate Wurth Elektronik inductance value codes.

        Args:
            inductance: Inductance value in µH
            value_suffix: AEC qualification suffix (unused for Wurth)

        Returns:
            Formatted inductance value code

        """
        if inductance < 1:
            return f"00{int(inductance * 100)}"
        if inductance < 10:
            return f"0{int(inductance * 10)}"
        if inductance < 100:
            return f"{inductance * 10}"
        if inductance < 1000:
            return f"{int(inductance / 10)}1"
        return f"{inductance}"

    @classmethod
    def create_description(
        cls,
        inductance: float,
        specs: SeriesSpec,
    ) -> str:
        """Create component description.

        Args:
            inductance: Inductance value in µH
            specs: Series specifications

        Returns:
            Description string for the component

        """
        if specs.reference == "E":
            parts = [
                "Ferrite Bead",
                cls.format_value(inductance).replace(" µH", " Ω @ 100 MHz"),
                specs.tolerance,
            ]
            return " ".join(parts)
        parts = [
            "INDUCTOR SMD",
            cls.format_value(inductance),
            specs.tolerance,
        ]
        return " ".join(parts)

    @classmethod
    def create_part_info(
        cls,
        inductance: float,
        specs: SeriesSpec,
    ) -> "PartInfo":
        """Create complete part information.

        Args:
            inductance: Inductance value in µH
            specs: Series specifications

        Returns:
            PartInfo instance for the component

        """
        value_code = cls.generate_value_code(inductance, specs.value_suffix)
        mpn = f"{specs.base_series}-{value_code}"
        datasheet = specs.datasheet

        if specs.manufacturer in ("Taiyo Yuden", "Murata"):
            mpn = f"{specs.base_series}"

        if specs.manufacturer == "Wurth Elektronik":
            value_code = cls.generate_wurth_value_code(inductance)
            mpn = f"{specs.base_series}{value_code}"
            datasheet = f"{specs.datasheet}{value_code}.pdf"

        if specs.reference == "E":
            mpn = f"{specs.base_series}"
            datasheet = specs.datasheet

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
            datasheet=datasheet,
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

        Returns:
            List of PartInfo instances for the series

        """
        return [
            cls.create_part_info(value, specs)
            for value in specs.inductance_values
        ]


SYMBOLS_SPECS: dict[str, SeriesSpec] = {
    "XAL1010": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL1010",
        footprint="inductor_footprints:XAL1010",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "dd74e670-e705-456a-9a69-585fe02eaf3c/xal1010.pdf"
        ),
        inductance_values=[
            *[0.22, 0.45, 0.68, 1, 1.5, 2.2, 3.3],
            *[4.7, 5.6, 6.8, 8.2, 10, 15],
        ],
        max_dc_current=[
            *[55.5, 53, 48, 43.5, 40.5, 32, 25],
            *[24, 21.2, 18.5, 17.1, 15.5, 13.8],
        ],
        max_dc_resistance=[
            *[0.5, 0.72, 0.96, 1.1, 1.76, 2.8, 4.1],
            *[5.7, 6.93, 8.9, 12.9, 14.75, 18.6],
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XAL1030": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL1030",
        footprint="inductor_footprints:XAL1030",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "7b108457-7731-456d-9256-ca72f2e1a551/xal1030.pdf"
        ),
        inductance_values=[0.16, 0.3, 0.56, 1.0],
        max_dc_current=[42.0, 35.0, 32.0, 23.0],
        max_dc_resistance=[1.21, 1.7, 2.75, 4.95],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XAL1060": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL1060",
        footprint="inductor_footprints:XAL1060",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "8909f858-b441-4d60-acff-8b8ca36f9ede/xal1060.pdf"
        ),
        inductance_values=[0.18, 0.4, 0.68, 1.2, 1.5, 2.2, 3.3, 4.7],
        max_dc_current=[46.0, 36.8, 33.9, 26.3, 24.4, 20.0, 16.8, 14.0],
        max_dc_resistance=[0.55, 0.88, 1.5, 2.75, 3.3, 4.95, 7.92, 10.72],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XAL1080": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL1080",
        footprint="inductor_footprints:XAL1080",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "18b60eaf-2c95-4723-8b7f-5f43f66ed007/xal1080.pdf"
        ),
        inductance_values=[10.0, 12.0, 15.0, 18.0, 22.0, 33.0],
        max_dc_current=[14.8, 13.9, 11.7, 10.8, 10.0, 7.5],
        max_dc_resistance=[12.3, 13.8, 17.9, 21.3, 24.5, 38.4],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XAL1350": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL1350",
        footprint="inductor_footprints:XAL1350",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "dc536f86-3a3b-454f-950e-8e153260e61c/xal1350.pdf"
        ),
        inductance_values=[0.63, 0.93, 1.3, 2.2, 3.0],
        max_dc_current=[38.0, 33.0, 32.0, 24.0, 21.0],
        max_dc_resistance=[1.7, 2.2, 2.7, 4.8, 6.8],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XAL1510": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL1510",
        footprint="inductor_footprints:XAL1510",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "cd1cef27-13f0-4568-8894-f7311475209b/xal1510.pdf"
        ),
        inductance_values=[4.7, 6.8, 8.2, 10.0, 15.0, 22.0, 33.0],
        max_dc_current=[29.0, 26.0, 24.0, 22.0, 18.0, 14.0, 12.0],
        max_dc_resistance=[3.8, 4.6, 7.5, 9.0, 12.4, 16.0, 20.0],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XAL1513": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL1513",
        footprint="inductor_footprints:XAL1513",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "129ad6f3-0445-47fd-a0b3-edeb49177c17/xal1513.pdf"
        ),
        inductance_values=[15.0],
        max_dc_current=[22.0],
        max_dc_resistance=[7.5],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XAL1580": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL1580",
        footprint="inductor_footprints:XAL1580",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "7fdfd306-5217-4ddc-b6b7-a2659ceeb6e3/xal1580.pdf"
        ),
        inductance_values=[
            *[0.4, 0.74, 1.0, 1.3, 1.8],
            *[2, 3, 4.5, 5.3, 6.1],
        ],
        max_dc_current=[
            *[60, 59.7, 57.5, 46.7, 43.8],
            *[39.9, 34.4, 27, 26.5, 22.6],
        ],
        max_dc_resistance=[
            *[0.7, 0.86, 1.12, 1.38, 1.93],
            *[2.29, 3.1, 4.58, 5.22, 6.79],
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XAL4020": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL4020",
        footprint="inductor_footprints:XAL4020",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "6adcb47d-8b55-416c-976e-1e22e0d2848c/xal4000.pdf"
        ),
        inductance_values=[0.22, 0.4, 0.6, 1.0, 1.2, 1.5, 2.2],
        max_dc_current=[16.8, 14.0, 11.7, 9.6, 9.0, 7.5, 5.5],
        max_dc_resistance=[6.4, 8.3, 10.45, 14.6, 19.5, 23.6, 38.7],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XAL4030": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL4030",
        footprint="inductor_footprints:XAL4030",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "6adcb47d-8b55-416c-976e-1e22e0d2848c/xal4000.pdf"
        ),
        inductance_values=[3.3, 4.7, 6.8],
        max_dc_current=[6.6, 5.1, 3.9],
        max_dc_resistance=[28.6, 44.1, 74.1],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XAL4040": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL4040",
        footprint="inductor_footprints:XAL4040",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "6adcb47d-8b55-416c-976e-1e22e0d2848c/xal4000.pdf"
        ),
        inductance_values=[8.2, 10.0, 15.0],
        max_dc_current=[3.4, 3.1, 2.8],
        max_dc_resistance=[66.9, 92.4, 120.0],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XAL5020": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL5020",
        footprint="inductor_footprints:XAL5020",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "1941eff1-c018-493c-8cd6-d88d2edf5029/xal5020.pdf"
        ),
        inductance_values=[0.16, 0.33, 0.56, 0.8, 1.2],
        max_dc_current=[18.8, 14.4, 13.9, 13.0, 9.4],
        max_dc_resistance=[5.0, 7.68, 9.54, 11.8, 20.5],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XAL5030": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL5030",
        footprint="inductor_footprints:XAL5030",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "49bc46c8-4b2c-45b9-9b6c-2eaa235ea698/xal50xx.pdf"
        ),
        inductance_values=[
            *[0.16, 0.33, 0.6, 0.8, 1],
            *[1.2, 2.2, 3.3, 4.7],
        ],
        max_dc_current=[
            *[22.2, 19.2, 17.7, 13.0, 11.1],
            *[10.4, 9.7, 8.1, 5.9],
        ],
        max_dc_resistance=[
            *[2.36, 3.52, 4.52, 5.65, 9.4],
            *[12.4, 14.5, 23.3, 40],
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XAL5050": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL5050",
        footprint="inductor_footprints:XAL5050",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "49bc46c8-4b2c-45b9-9b6c-2eaa235ea698/xal50xx.pdf"
        ),
        inductance_values=[4.7, 5.6, 6.8, 8.2, 10.0, 15.0, 22.0],
        max_dc_current=[8.2, 7.2, 6.4, 6.1, 4.9, 3.9, 3.4],
        max_dc_resistance=[24.15, 25.8, 29.45, 34.95, 45.0, 76.7, 99.65],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XAL6020": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL6020",
        footprint="inductor_footprints:XAL6020",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "467ff589-8942-4e57-92d0-5bef6e04ce09/xal6020.pdf"
        ),
        inductance_values=[0.12, 0.16, 0.27, 0.45, 0.6, 0.9, 1.1],
        max_dc_current=[27.0, 26.0, 25.0, 22.0, 18.5, 15.2, 12.0],
        max_dc_resistance=[1.85, 2.7, 3.85, 5.05, 7.1, 11.1, 13.1],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XAL6030": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL6030",
        footprint="inductor_footprints:XAL6030",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "ea51f14b-7f32-4dc6-8dfe-d4b70549040f/xal60xx.pdf"
        ),
        inductance_values=[0.18, 0.33, 0.56, 1.0, 1.2, 1.8, 2.2, 3.3],
        max_dc_current=[32.0, 25.0, 22.0, 18.0, 16.0, 14.0, 10.0, 8.0],
        max_dc_resistance=[1.75, 2.53, 3.31, 6.18, 7.5, 10.52, 13.97, 20.81],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XAL6060": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL6060",
        footprint="inductor_footprints:XAL6060",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "ea51f14b-7f32-4dc6-8dfe-d4b70549040f/xal60xx.pdf"
        ),
        inductance_values=[*[4.7, 5.6, 6.8, 8.2], *[10, 15, 22, 33]],
        max_dc_current=[*[11, 10, 9, 8], *[7, 6, 5, 3.6]],
        max_dc_resistance=[
            *[14.4, 15.9, 20.8, 26.4],
            *[29.82, 43.75, 60.63, 105],
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XAL7020": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL7020",
        footprint="inductor_footprints:XAL7020",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "0197e98c-67f7-4375-9e38-14d7376a46f3/xal7020.pdf"
        ),
        inductance_values=[0.15, 0.27, 0.33, 0.47, 0.68, 1.0, 1.2, 1.5, 2.2],
        max_dc_current=[24.0, 21.0, 20.0, 17.0, 13.0, 11.0, 10.0, 9.0, 7.0],
        max_dc_resistance=[2.5, 3.8, 5.2, 6.4, 9.5, 10.8, 12.8, 19.3, 31.6],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XAL7030": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL7030",
        footprint="inductor_footprints:XAL7030",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "0d05a05e-d55d-4a0c-911d-46bd73686633/xal7030.pdf"
        ),
        inductance_values=[
            *[0.16, 0.3, 0.6, 1, 1.5, 2.2, 2.7],
            *[3.3, 4.7, 5.6, 6.8, 8.2, 10],
        ],
        max_dc_current=[
            *[32.5, 27.6, 23, 21.8, 15, 12.9, 11.4],
            *[10, 9, 7.3, 6.8, 5.9, 5.3],
        ],
        max_dc_resistance=[
            *[1.26, 1.92, 3.3, 5.0, 8.36, 15.07, 17.3],
            *[21.45, 30, 32.32, 51.75, 60.94, 69.46],
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XAL7050": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL7050",
        footprint="inductor_footprints:XAL7050",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "13a991b3-4273-4be3-81ba-f3cf372b4691/xal7050.pdf"
        ),
        inductance_values=[10.0, 15.0, 18.0, 22.0, 33.0, 47.0],
        max_dc_current=[8.5, 7.0, 6.2, 5.0, 4.6, 3.5],
        max_dc_resistance=[29.0, 41.0, 50.0, 70.0, 85.0, 120.0],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XAL7070": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL7070",
        footprint="inductor_footprints:XAL7070",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "1ba55433-bcc8-4838-9b21-382f497e12e0/xal7070.pdf"
        ),
        inductance_values=[
            *[0.16, 0.3, 0.55, 0.65, 0.8, 1],
            *[1.2, 1.8, 2.2, 3.3, 4.7, 5.6],
            *[6.8, 10, 12, 15, 18, 22, 33, 47],
        ],
        max_dc_current=[
            *[36.1, 33.4, 29, 26.5, 25.8, 25],
            *[21.6, 21, 17.8, 15.1, 13.6, 11.4],
            *[9.2, 9.3, 8.2, 7.4, 6.8, 6.5, 4.9, 4.1],
        ],
        max_dc_resistance=[
            *[0.83, 1.17, 1.56, 1.93, 2.29, 2.81],
            *[3.41, 4.46, 6.33, 9.42, 14.26, 15.03],
            *[19.62, 20.17, 22.23, 29.52, 32.82, 39.69, 62.08, 97.07],
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XAL8050": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL8050",
        footprint="inductor_footprints:XAL8050",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "5885ede8-ea4f-464a-9dcb-18dbf143a845/xal8050.pdf"
        ),
        inductance_values=[22.0],
        max_dc_current=[5.2],
        max_dc_resistance=[71],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XAL8080": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL8080",
        footprint="inductor_footprints:XAL8080",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "345e50d6-a804-4ecb-9a92-5185221faf3e/xal8080.pdf"
        ),
        inductance_values=[
            *[0.68, 0.84, 1, 2.2, 4.7, 6.8],
            *[10, 12, 15, 18, 22, 33, 47],
        ],
        max_dc_current=[
            *[37.0, 35, 34.1, 21.5, 14.6, 11.3],
            *[8.7, 10.5, 9.4, 8.3, 7.6, 6, 4.8],
        ],
        max_dc_resistance=[
            *[1.65, 1.90, 2.33, 4.49, 9.77, 14.5],
            *[23.1, 18.2, 22.5, 28, 32.9, 48.5, 71.8],
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XFL2005": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL2005",
        footprint="inductor_footprints:XFL2005",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "73b70df2-8cfe-46c3-92db-66951708f060/xfl2005.pdf"
        ),
        inductance_values=[
            *[0.15, 0.22, 0.33, 0.47, 0.68, 1.0, 1.5],
            *[2.2, 3.3, 4.7, 5.6, 6.8, 8.2, 10],
        ],
        max_dc_current=[
            *[1.6, 1.48, 1.3, 1.25, 1.05, 0.84, 0.7],
            *[0.66, 0.5, 0.41, 0.39, 0.38, 0.33, 0.29],
        ],
        max_dc_resistance=[
            *[0.098, 0.128, 0.166, 0.204, 0.247, 0.43, 0.555],
            *[0.775, 1.06, 1.69, 1.98, 2.21, 2.8, 3.1],
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XFL2006": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL2006",
        footprint="inductor_footprints:XFL2006",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "65419ba7-9eac-409b-830a-74bf182a8aca/xfl2006.pdf"
        ),
        inductance_values=[
            *[1, 2.2, 3.3, 4.7, 5.6, 6.8, 8.2, 10],
            *[15, 22, 33, 47, 56, 68, 82, 100],
        ],
        max_dc_current=[
            *[1.22, 0.950, 0.72, 0.66, 0.6, 0.52, 0.49, 0.44],
            *[0.35, 0.305, 0.205, 0.205, 0.195, 0.155, 0.165, 0.135],
        ],
        max_dc_resistance=[
            *[0.169, 0.306, 0.506, 0.732, 0.825, 1.02, 1.19, 1.4],
            *[2.22, 3.06, 4.9, 5.16, 7.32, 9.35, 10.18, 12.25],
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XFL2010": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL2010",
        footprint="inductor_footprints:XFL2010",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "50382b97-998f-4b75-b5ee-4a93b0ac4411/xfl2010.pdf"
        ),
        inductance_values=[
            *[0.04, 0.12, 0.22, 0.38, 0.6, 0.82, 1],
            *[1.5, 2.2, 3.3, 4.7, 6.8, 8.2, 10],
            *[18, 22, 33, 47, 56, 68, 82, 100, 220],
        ],
        max_dc_current=[
            *[4.8, 3.7, 3.1, 2.85, 2.35, 2.15, 1.8],
            *[1.55, 1.35, 1.2, 0.91, 0.79, 0.76, 0.67],
            *[0.46, 0.42, 0.35, 0.31, 0.27, 0.26, 0.21, 0.2, 0.14],
        ],
        max_dc_resistance=[
            *[0.016, 0.022, 0.025, 0.033, 0.054, 0.061, 0.083],
            *[0.115, 0.156, 0.213, 0.32, 0.405, 0.511, 0.595],
            *[1.17, 1.5, 2.14, 2.91, 3.66, 3.98, 5.81, 6.98, 13.66],
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XFL3010": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL3010",
        footprint="inductor_footprints:XFL3010",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "0118859e-f2e2-4063-93cf-e50ed636ea4e/xfl3010.pdf"
        ),
        inductance_values=[
            *[0.60, 1, 1.5, 2.2, 3.3, 4.7, 6.8, 10, 15],
            *[22, 33, 39, 47, 56, 68, 82, 100, 220],
        ],
        max_dc_current=[
            *[2.5, 2.3, 1.9, 1.3, 1.2, 1.1, 0.95, 0.82, 0.76],
            *[0.66, 0.56, 0.51, 0.44, 0.41, 0.36, 0.34, 0.29, 0.19],
        ],
        max_dc_resistance=[
            *[0.033, 0.049, 0.08, 0.122, 0.166, 0.23, 0.346, 0.519, 0.56],
            *[0.818, 1.2, 1.4, 1.93, 2.16, 2.6, 3.1, 5.5, 12],
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XFL3012": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL3012",
        footprint="inductor_footprints:XFL3012",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "f76a3c9b-4fff-4397-8028-ef8e043eb200/xfl3012.pdf"
        ),
        inductance_values=[
            *[0.33, 0.56, 0.68, 1, 1.5],
            *[2.2, 3.3, 4.7, 6.8, 10, 15],
            *[22, 33, 39, 47, 56, 68, 82, 100, 220],
        ],
        max_dc_current=[
            *[3.5, 3, 2.8, 2.6, 2.2, 1.9],
            *[1.6, 1.4, 1.3, 1.2, 1, 0.8],
            *[0.57, 0.54, 0.46, 0.44, 0.42, 0.34, 0.39, 0.23],
        ],
        max_dc_resistance=[
            *[0.027, 0.032, 0.04, 0.046, 0.072, 0.097],
            *[0.127, 0.171, 0.2, 0.306, 0.483, 0.63],
            *[0.896, 0.985, 1.32, 1.52, 1.985, 2.44, 3, 3.07],
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XFL4012": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL4012",
        footprint="inductor_footprints:XFL4012",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "2d7c4d90-1677-4c05-9569-33b6dc7153e7/xfl4012.pdf"
        ),
        inductance_values=[0.12, 0.25, 0.47, 0.6],
        max_dc_current=[13.2, 11.45, 8.7, 7.65],
        max_dc_resistance=[5.88, 8.4, 15.48, 19.14],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XFL4015": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL4015",
        footprint="inductor_footprints:XFL4015",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "84927b8b-f089-421b-a7f4-a0fa23afe908/xfl4015.pdf"
        ),
        inductance_values=[0.18, 0.33, 0.47, 0.7, 1.2],
        max_dc_current=[14.5, 13.2, 11.2, 10.1, 7.1],
        max_dc_resistance=[4.7, 7.5, 8.36, 10.45, 20.7],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XFL4020": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL4020",
        footprint="inductor_footprints:XFL4020",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "50632d43-da1b-4cdb-8ab4-3029cab51df3/xfl4020.pdf"
        ),
        inductance_values=[
            *[0.12, 0.24, 0.33, 0.47, 0.56],
            *[1.0, 1.5, 2.2, 3.3, 4.7],
        ],
        max_dc_current=[
            *[22, 20, 17.5, 17, 13],
            *[11, 9.1, 8, 5.2, 5],
        ],
        max_dc_resistance=[
            *[1.6, 2.7, 3.85, 5.1, 6.15],
            *[11.9, 15.8, 23.5, 38.3, 57.4],
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XFL4030": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL4030",
        footprint="inductor_footprints:XFL4030",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "d12f7f67-cfc1-404a-9993-f09a1451b0a9/xfl4030.pdf"
        ),
        inductance_values=[0.47, 1.0, 2.0, 3.0, 4.7],
        max_dc_current=[18.0, 14.5, 11.8, 8.0, 7.5],
        max_dc_resistance=[4.4, 6.6, 11.5, 20.5, 30.0],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XFL5015": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL5015",
        footprint="inductor_footprints:XFL5015",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "5f7b596c-8f2f-415e-931e-74a5b6804936/xfl5015.pdf"
        ),
        inductance_values=[0.22, 0.42, 0.68, 1.2, 1.5],
        max_dc_current=[16.2, 12.7, 11.3, 9.2, 8.0],
        max_dc_resistance=[4.83, 7.19, 9.4, 16.6, 20.1],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XFL5018": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL5018",
        footprint="inductor_footprints:XFL5018",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "5f7b596c-8f2f-415e-931e-74a5b6804936/xfl5015.pdf"
        ),
        inductance_values=[2.2, 3.3],
        max_dc_current=[9.2, 8.0],
        max_dc_resistance=[24.5, 37.0],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XFL5030": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL5030",
        footprint="inductor_footprints:XFL5030",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "f01e4ccd-6be9-43eb-bb01-c23b4deeb2c5/xfl5030.pdf"
        ),
        inductance_values=[0.27, 0.56, 1.0, 2.2, 3.3, 4.7],
        max_dc_current=[25.5, 21.0, 18.0, 11.5, 10.0, 8.7],
        max_dc_resistance=[2.55, 3.8, 5.0, 12.0, 16.0, 22.0],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XFL6012": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL6012",
        footprint="inductor_footprints:XFL6012",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "ae4a44fc-deeb-45d7-81a6-abe1d0432add/xfl6012.pdf"
        ),
        inductance_values=[0.18, 0.39, 0.6, 0.8, 1.0],
        max_dc_current=[13.2, 12.5, 11.2, 9.4, 8.0],
        max_dc_resistance=[8.12, 12.1, 15.5, 20.7, 25.2],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XFL6060": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL6060",
        footprint="inductor_footprints:XFL6060",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "9e8cc1df-cee0-4215-90fb-b5193fa22761/xfl6060-473.pdf"
        ),
        inductance_values=[47.0],
        max_dc_current=[3.7],
        max_dc_resistance=[75.3],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "XFL7015": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL7015",
        footprint="inductor_footprints:XFL7015",
        tolerance="±20%",
        datasheet=(
            "https://www.coilcraft.com/getmedia/"
            "ccf09628-6e8c-462a-9dc9-fa4346e7cf0a/xfl7015.pdf"
        ),
        inductance_values=[0.25, 0.47, 0.68, 1.0, 1.5],
        max_dc_current=[20.0, 17.0, 15.0, 10.5, 8.0],
        max_dc_resistance=[4.3, 6.38, 8.47, 16.0, 22.6],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "742792731": SeriesSpec(
        manufacturer="Wurth Elektronik",
        reference="E",
        base_series="742792731",
        footprint="inductor_footprints:742792731",
        tolerance="±25%",
        datasheet=(
            "https://www.we-online.com/components/products/datasheet/"
            "742792731.pdf"
        ),
        inductance_values=[100.0],
        max_dc_current=[1.2],
        max_dc_resistance=[0.09],
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "LCENA2016MKTR47M0NK": SeriesSpec(
        manufacturer="Taiyo Yuden",
        base_series="LCENA2016MKTR47M0NK",
        footprint="inductor_footprints:LCENA2016MKTR47M0NK",
        tolerance="±20%",
        datasheet=(
            "https://www.cyntec.com/upfile/products/download/"
            "HTEH20121T-000%20(A1).pdf"
        ),
        inductance_values=[0.47],
        max_dc_current=[4.6],
        max_dc_resistance=[0.025],
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "DFE21CCN1R0MELL": SeriesSpec(
        manufacturer="Murata",
        base_series="DFE21CCN1R0MELL",
        footprint="inductor_footprints:DFE21CCN1R0MELL",
        tolerance="±20%",
        datasheet=(
            "https://search.murata.co.jp/Ceramy/image/img/P02/"
            "JETE243A-0052.pdf"
        ),
        inductance_values=[1.0],
        max_dc_current=[3.3],
        max_dc_resistance=[0.06],
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "LQG15HS47NJ02D": SeriesSpec(
        manufacturer="Murata",
        base_series="LQG15HS47NJ02D",
        footprint="inductor_footprints:LQG15HS47NJ02D",
        tolerance="±5%",
        datasheet=(
            "https://www.murata.com/products/productdetail?partno="
            "LQG15HS47NJ02%23"
        ),
        inductance_values=[47e-9],
        max_dc_current=[0.3],
        max_dc_resistance=[0.72],
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "74404020": SeriesSpec(
        manufacturer="Wurth Elektronik",
        base_series="74404020",
        footprint="inductor_footprints:74404020",
        tolerance="±20%",
        datasheet="https://www.we-online.com/components/products/datasheet/",
        inductance_values=[
            *[0.16, 0.33, 0.47, 0.68, 1, 1.5],
            *[2.2, 3.3, 4.7, 6.8, 10],
        ],
        max_dc_current=[
            *[3, 2.5, 2.1, 1.8, 1.5, 1.2],
            *[0.96, 0.87, 0.72, 0.55, 0.5],
        ],
        max_dc_resistance=[
            *[0.025, 0.034, 0.047, 0.064, 0.094, 0.147],
            *[0.225, 0.275, 0.41, 0.7, 0.86],
        ],
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "74404024": SeriesSpec(
        manufacturer="Wurth Elektronik",
        base_series="74404024",
        footprint="inductor_footprints:74404024",
        tolerance="±20%",
        datasheet="https://www.we-online.com/components/products/datasheet/",
        inductance_values=[
            *[0.16, 0.47, 0.68, 1.0, 1.5, 2.2],
            *[3.3, 4.7, 6.8, 10, 15, 18],
            *[22, 33, 47, 68],
        ],
        max_dc_current=[
            *[3.7, 2.6, 2.5, 2.3, 1.8, 1.65],
            *[1.35, 1.12, 0.85, 0.65, 0.47, 0.46],
            *[0.45, 0.35, 0.33, 0.28],
        ],
        max_dc_resistance=[
            *[0.016, 0.032, 0.035, 0.036, 0.065, 0.080],
            *[0.120, 0.173, 0.300, 0.430, 0.820, 0.830],
            *[0.910, 1.530, 1.650, 2.400],
        ],
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "74404032": SeriesSpec(
        manufacturer="Wurth Elektronik",
        base_series="74404032",
        footprint="inductor_footprints:74404032",
        tolerance="±20%",
        datasheet="https://www.we-online.com/components/products/datasheet/",
        inductance_values=[
            *[0.47, 1.0, 1.5, 2.2, 3.3, 4.7, 6.8],
            *[10, 15, 22, 33, 47, 68, 100],
        ],
        max_dc_current=[
            *[3.0, 2.2, 2.0, 1.8, 1.5, 1.3, 1.16],
            *[0.84, 0.73, 0.6, 0.5, 0.4, 0.34, 0.3],
        ],
        max_dc_resistance=[
            *[0.018, 0.033, 0.040, 0.050, 0.070, 0.096, 0.120],
            *[0.230, 0.3, 0.45, 0.911, 1.050, 1.600, 1.900],
        ],
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "74404041": SeriesSpec(
        manufacturer="Wurth Elektronik",
        base_series="74404041",
        footprint="inductor_footprints:74404041",
        tolerance="±20%",
        datasheet="https://www.we-online.com/components/products/datasheet/",
        inductance_values=[
            *[0.47, 1, 3.3, 4.7, 10],
            *[22, 33, 47, 68, 100],
        ],
        max_dc_current=[
            *[3.25, 2.52, 1.75, 1.55, 1.32],
            *[0.95, 0.65, 0.56, 0.45, 0.43],
        ],
        max_dc_resistance=[
            *[0.028, 0.041, 0.069, 0.091, 0.168],
            *[0.38, 0.628, 0.987, 1.495, 1.697],
        ],
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "74404042": SeriesSpec(
        manufacturer="Wurth Elektronik",
        base_series="74404042",
        footprint="inductor_footprints:74404042",
        tolerance="±20%",
        datasheet="https://www.we-online.com/components/products/datasheet/",
        inductance_values=[
            *[0.33, 1, 1.5, 2.2, 3.3, 4.7, 6.8, 10, 15],
            *[22, 33, 47, 68, 100, 150, 220, 330],
        ],
        max_dc_current=[
            *[4.5, 3.2, 2.95, 2.2, 2, 1.7, 1.45, 1.2, 0.85],
            *[0.7, 0.65, 0.6, 0.54, 0.42, 0.3, 0.25, 0.2],
        ],
        max_dc_resistance=[
            *[0.013, 0.027, 0.031, 0.042, 0.055, 0.07, 0.098, 0.15, 0.21],
            *[0.29, 0.46, 0.62, 0.84, 1.43, 2.853, 3.45, 5.3],
        ],
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "74404043": SeriesSpec(
        manufacturer="Wurth Elektronik",
        base_series="74404043",
        footprint="inductor_footprints:74404043",
        tolerance="±20%",
        datasheet="https://www.we-online.com/components/products/datasheet/",
        inductance_values=[
            *[1, 2.2, 3.3, 4.7, 10, 15, 22],
            *[33, 47, 100, 150, 220, 470],
        ],
        max_dc_current=[
            *[4.9, 3.83, 3.23, 2.3, 1.76, 1.45, 1.11],
            *[0.88, 0.71, 0.49, 0.39, 0.31, 0.25],
        ],
        max_dc_resistance=[
            *[0.014, 0.023, 0.033, 0.046, 0.089, 0.132, 0.2],
            *[0.316, 0.492, 1.043, 1.634, 2.43, 4.15],
        ],
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
}
