"""Library for managing diode specifications.

This module provides data structures and definitions for various diode
series, including their specifications and individual component
information. It handles creation and management of diode part numbers,
specifications, and related information, with support for different
manufacturers and series types.

The module includes two main classes:
- SeriesSpec: For defining diode series specifications
- PartInfo: For managing individual diode component information
"""

from __future__ import annotations

from typing import NamedTuple, Self

from utilities import print_message_utilities


class SeriesSpec(NamedTuple):
    """Diode series specifications.

    This class defines the complete specifications for a series of diodes,
    including physical, electrical, and documentation characteristics.

    Attributes:
        manufacturer: Manufacturer of the diode series
        base_series: Base series name of the diode
        footprint: KiCad footprint name for the diode
        datasheet: URL link to the diode datasheet
        voltage_rating: List of voltage ratings for the diode series
        trustedparts_link: URL link to the TrustedParts website
        current_rating: List of current ratings for the diode series
        package: Package type for the diode series
        diode_type: Type of diode (e.g., Schottky, Zener)
        part_number_suffix: Optional suffix for the diode part number
        reference: Reference designator prefix for the diode

    """

    manufacturer: str
    base_series: str
    footprint: str
    datasheet: str
    voltage_rating: list[float]
    trustedparts_link: str
    package: str
    diode_type: str
    current_rating: list[float] | None = None
    part_number_suffix: str | None = None
    reference: str = "D"


class PartInfo(NamedTuple):
    """Component part information structure for individual diodes.

    This class defines the complete information for a specific diode
    component, including symbol name, reference designator, value, footprint,
    datasheet, and other relevant details.

    Attributes:
        symbol_name: Symbol name for the diode component
        reference: Reference designator prefix for the diode
        value: Voltage rating of the diode
        footprint: KiCad footprint name for the diode
        datasheet: URL link to the diode datasheet
        description: Descriptive string for the diode component
        manufacturer: Manufacturer of the diode component
        mpn: Manufacturer part number for the diode component
        series: Base series name of the diode
        trustedparts_link: URL link to the TrustedParts website
        current_rating: Maximum DC current rating for the diode
        package: Package type for the diode
        diode_type: Type of diode (e.g., Schottky, Zener)

    """

    symbol_name: str
    reference: str
    value: float
    footprint: str
    datasheet: str
    description: str
    manufacturer: str
    mpn: str
    series: str
    trustedparts_link: str
    current_rating: float
    package: str
    diode_type: str

    @staticmethod
    def format_value(value: float) -> str:
        """Format the diode voltage value with a 'V' suffix.

        Converts a numerical voltage value to a string with a 'V' suffix,
        suitable for use in component descriptions and documentation.

        Args:
            value: The voltage rating of the diode.

        Returns:
            Formatted voltage value with 'V' appended.

        """
        return f"{value} V"

    @classmethod
    def create_description(
        cls,
        value: float,
        diode_type: str = "DIODE",
    ) -> str:
        """Create a descriptive string for the diode component.

        Generates a standardized description string that includes the diode
        type, mounting style (SMD), and voltage rating.

        Args:
            value: The voltage rating of the diode.
            diode_type: Type of diode component. Defaults to "DIODE".

        Returns:
            Descriptive string for the diode component.

        """
        parts = [f"{diode_type} SMD", cls.format_value(value)]
        return " ".join(parts)

    @classmethod
    def create_part_info(  # noqa: C901, PLR0912, PLR0915
        cls: type[Self],
        value: float,
        specs: SeriesSpec,
    ) -> Self | None:
        """Create a PartInfo object for a specific diode component.

        Generates a complete PartInfo instance based on the provided voltage
        value and series specifications. Handles different
        manufacturer-specific part number formats and validates the voltage
        value against the series specifications.

        Args:
            value: Voltage rating of the diode component
            specs: Series specifications for the diode component

        Returns:
            Instance of PartInfo for the diode component, or None if the
            voltage value is invalid or not found in the specifications.

        """
        # Construct MPN with optional suffix
        mpn = f"{specs.base_series}"

        if specs.manufacturer == "Kingbright":
            mpn = f"{specs.base_series.replace('-', '/', 1)}"

        if (
            specs.manufacturer == "Diodes Incorporated"
            and specs.part_number_suffix
        ):
            index = specs.voltage_rating.index(value)
            value = float(specs.voltage_rating[index])
            voltage = (
                f"{int(value)}"
                if value >= 10
                else f"{value:.1f}".replace(".", "V")
            )
            mpn = f"{specs.base_series}{voltage}{specs.part_number_suffix}"

        if specs.manufacturer == "Onsemi" and specs.part_number_suffix:
            # Find index of voltage in ratings list
            index = specs.voltage_rating.index(value)
            # Adjust index to start from 21
            adjusted_index = index + 21
            mpn = (
                f"{specs.base_series}{adjusted_index}"
                f"{specs.part_number_suffix}"
            )

        if specs.manufacturer == "Nexperia" and specs.part_number_suffix:
            # Find index of voltage in ratings list
            index = specs.voltage_rating.index(value)

            voltage_str = f"{float(specs.voltage_rating[index]):.3f}"
            whole, decimal = voltage_str.split(".")
            decimal = decimal.rstrip("0")
            if not decimal:
                decimal = "0"

            voltage_notation = (
                f"{whole}V{decimal}" if decimal else f"{whole}V0"
            )
            if float(whole) >= 10:  # noqa: PLR2004
                voltage_notation = f"{whole}V"

            mpn = (
                f"{specs.base_series}"
                f"{voltage_notation}"
                f"{specs.part_number_suffix}"
            )

        if (
            specs.manufacturer == "Nexperia"
            and specs.part_number_suffix is None
        ):
            # Find index of voltage in ratings list
            index = specs.voltage_rating.index(value)

            voltage_str = f"{float(specs.voltage_rating[index]):.3f}"
            whole, decimal = voltage_str.split(".")
            decimal = decimal.rstrip("0")
            if not decimal:
                decimal = "0"

            voltage_notation = (
                f"{whole}V{decimal}" if decimal else f"{whole}V0"
            )
            if float(whole) >= 10:  # noqa: PLR2004
                voltage_notation = f"{whole}"

            mpn = f"{specs.base_series}{voltage_notation}"

        if specs.manufacturer == "Littelfuse" and specs.part_number_suffix:
            # Find index of voltage in ratings list
            index = specs.voltage_rating.index(value)

            voltage_str = f"{float(specs.voltage_rating[index]):.3f}"
            whole, decimal = voltage_str.split(".")
            decimal = decimal.rstrip("0")
            if not decimal:
                decimal = "0"

            voltage_notation = f"{whole}.{decimal}" if decimal else f"{whole}"
            if float(whole) >= 10:  # noqa: PLR2004
                voltage_notation = f"{whole}"

            mpn = (
                f"{specs.base_series}"
                f"{voltage_notation}"
                f"{specs.part_number_suffix}"
            )

        if (
            specs.manufacturer == "STMicroelectronics"
            and specs.part_number_suffix
        ):
            # Find index of voltage in ratings list
            index = specs.voltage_rating.index(value)

            voltage_str = f"{float(specs.voltage_rating[index]):.3f}"
            whole, decimal = voltage_str.split(".")
            decimal = decimal.rstrip("0")
            if not decimal:
                decimal = "0"

            voltage_notation = f"{whole}.{decimal}" if decimal else f"{whole}"
            if float(whole) >= 10:  # noqa: PLR2004
                voltage_notation = f"{whole}"

            mpn = (
                f"{specs.base_series}"
                f"{voltage_notation}"
                f"{specs.part_number_suffix}"
            )

        trustedparts_link = f"{specs.trustedparts_link}/{mpn}"

        # Handle current rating
        try:
            index = specs.voltage_rating.index(value)
            if specs.current_rating is not None:
                try:
                    current_rating = float(specs.current_rating[index])
                except IndexError:
                    print_message_utilities.print_error(
                        "Error: Current rating index out of range "
                        f"for value {value} V in series {specs.base_series}",
                    )
                    current_rating = 0.0
            else:
                # Set default current rating when specs.current_rating is None
                current_rating = 0.0
        except ValueError:
            print_message_utilities.print_error(
                f"Error: value {value} V "
                f"not found in series {specs.base_series}",
            )
            return None

        return cls(
            symbol_name=f"{specs.reference}_{mpn.replace('/', '-')}",
            reference=specs.reference,
            value=value,
            footprint=specs.footprint,
            datasheet=specs.datasheet,
            description=cls.create_description(value, specs.diode_type),
            manufacturer=specs.manufacturer,
            mpn=mpn,
            package=specs.package,
            series=specs.base_series,
            trustedparts_link=trustedparts_link,
            current_rating=current_rating,
            diode_type=specs.diode_type,
        )

    @classmethod
    def generate_part_numbers(
        cls,
        specs: SeriesSpec,
    ) -> list[Self]:
        """Generate all part numbers for the series.

        Creates a list of PartInfo instances for all voltage ratings defined
        in the given series specifications. Filters out any invalid voltage
        ratings that fail to create valid part information.

        Args:
            specs: Series specifications for the diode component

        Returns:
            List of PartInfo instances for all valid voltage ratings
            in the series

        """
        return [
            part_info
            for value in specs.voltage_rating
            if (part_info := cls.create_part_info(value, specs)) is not None
        ]


SYMBOLS_SPECS: dict[str, SeriesSpec] = {
    "DFLS1200-7": SeriesSpec(
        manufacturer="Diodes Incorporated",
        base_series="DFLS1200-7",
        footprint="diode_footprints:PowerDI_123",
        datasheet="https://www.diodes.com/datasheet/download/DFLS1200.pdf",
        voltage_rating=[100.0],
        current_rating=[1.2],
        package="PowerDI_123",
        diode_type="Schottky",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "MMSZ52": SeriesSpec(
        manufacturer="Onsemi",
        base_series="MMSZ52",
        footprint="diode_footprints:SOD_123",
        datasheet=(
            "https://www.onsemi.com/download/data-sheet/pdf/mmsz5221bt1-d.pdf"
        ),
        voltage_rating=[
            *[2.4, 2.5, 2.7, 2.8, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6],
            *[6.0, 6.2, 6.8, 7.5, 8.2, 8.7, 9.1, 10.0, 11.0, 12.0, 13.0],
            *[14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 22.0, 24.0, 25.0],
            *[27.0, 28.0, 30.0, 33.0, 36.0, 39.0, 43.0, 47.0, 51.0, 56.0],
            *[60.0, 62.0, 68.0, 75.0, 82.0, 87.0, 91.0],
        ],
        current_rating=[0.5] * 51,
        package="SOD_123",
        diode_type="Zener",
        trustedparts_link="https://www.trustedparts.com/en/search",
        part_number_suffix="BT1G",
    ),
    "US1DWF": SeriesSpec(
        manufacturer="Diodes Incorporated",
        base_series="US1DWF",
        footprint="diode_footprints:SOD_123F",
        datasheet="https://www.diodes.com/assets/Datasheets/US1DWF.pdf",
        voltage_rating=[200.0],
        current_rating=[1.0],
        package="SOD_123F",
        diode_type="Rectifier",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "APHHS1005LSECK-J3-PF": SeriesSpec(
        manufacturer="Kingbright",
        base_series="APHHS1005LSECK-J3-PF",
        footprint="diode_footprints:LED_RED_0402_1005Metric",
        datasheet=(
            "https://www.kingbrightusa.com/product.asp?catalog_name="
            "LED&product_id=APHHS1005LSECK/J3-PF"
        ),
        voltage_rating=[1.8],
        current_rating=[0.03],
        package="LED_RED_0402_1005Metric",
        diode_type="Red LED",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "APHHS1005CGCK": SeriesSpec(
        manufacturer="Kingbright",
        base_series="APHHS1005CGCK",
        footprint="diode_footprints:LED_GREEN_0402_1005Metric",
        datasheet=(
            "https://www.kingbrightusa.com/product.asp?catalog_name="
            "LED&product_id=APHHS1005CGCK"
        ),
        voltage_rating=[2.1],
        current_rating=[0.03],
        package="LED_GREEN_0402_1005Metric",
        diode_type="Green LED",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "KP-1608SGC": SeriesSpec(
        manufacturer="Kingbright",
        base_series="KP-1608SGC",
        footprint="diode_footprints:LED_GREEN_0603_1608Metric",
        datasheet=(
            "https://www.tme.eu/Document/00c026014e4e4cabfb9c846616baea66/"
            "KP-1608SGC.pdf"
        ),
        voltage_rating=[2.2],
        current_rating=[0.02],
        package="LED_GREEN_0603_1608Metric",
        diode_type="Green LED",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "SBAV99WT1G": SeriesSpec(
        reference="CR",
        manufacturer="Onsemi",
        base_series="SBAV99WT1G",
        footprint="diode_footprints:SC_70",
        datasheet=(
            "https://www.onsemi.com/products/discrete-power-modules/"
            "small-signal-switching-diodes/bav99w"
        ),
        voltage_rating=[100],
        current_rating=[0.215],
        package="SC_70",
        diode_type="Dual Small Signal Switching Diodes",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BAT54AWFILMY": SeriesSpec(
        manufacturer="STMicroelectronics",
        base_series="BAT54AWFILMY",
        footprint="diode_footprints:SOT-323",
        datasheet=("https://www.st.com/resource/en/datasheet/bat54-y.pdf"),
        voltage_rating=[40],
        current_rating=[0.3],
        package="SOT-323",
        diode_type="Small Signal Schottky Diodes",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "PMEG10020AELR": SeriesSpec(
        manufacturer="Nexperia",
        base_series="PMEG10020AELR",
        footprint="diode_footprints:SOD123W",
        part_number_suffix="",
        datasheet=(
            "https://assets.nexperia.com/documents/data-sheet/"
            "PMEG10020AELR.pdf"
        ),
        voltage_rating=[100.0],
        current_rating=[2.0],
        package="SOD123W",
        diode_type="Schottky",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "PTVS": SeriesSpec(
        manufacturer="Nexperia",
        base_series="PTVS",
        part_number_suffix="P1UTP,115",
        footprint="diode_footprints:SOD128",
        datasheet=(
            "https://assets.nexperia.com/documents/data-sheet/"
            "PTVSXP1UTP_SER.pdf"
        ),
        voltage_rating=[
            *[3.3, 5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 10, 11, 12, 13, 14, 15, 16],
            *[17, 18, 20, 22, 24, 26, 28, 30, 33, 36, 40, 43, 45, 48, 51, 54],
            *[58, 60, 64],
        ],
        package="SOD128",
        diode_type="Unidirectional TVS",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "SMBJ": SeriesSpec(
        manufacturer="Littelfuse",
        base_series="SMBJ",
        part_number_suffix="CA",
        footprint="diode_footprints:DO-214AA",
        datasheet=(
            "https://www.littelfuse.com/assetdocs/tvs-diodes-smbj-series-"
            "datasheet?assetguid=09a6ae9a-73cb-4ac4-acac-e6dab92ab953"
        ),
        voltage_rating=[
            *[5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 10, 11, 12, 13, 14, 15, 16, 17],
            *[18, 20, 22, 24, 26, 28, 30, 33, 36, 40, 43, 45, 48, 51, 54, 58],
            *[60, 64, 70, 75, 78, 85, 90, 100, 110, 120, 130, 150, 170, 180],
            *[188, 200, 220, 250, 300, 350, 400, 440],
        ],
        package="DO-214AA",
        diode_type="Bidirectional TVS",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "SP4020-01FTG-C": SeriesSpec(
        manufacturer="Littelfuse",
        base_series="SP4020-01FTG-C",
        part_number_suffix="",
        footprint="diode_footprints:SOD323",
        datasheet=(
            "https://www.littelfuse.com/assetdocs/tvs-diode-array-"
            "sp4020-datasheet?assetguid=b6e2c598-7d86-4fa2-a063-fb053ce07713"
        ),
        voltage_rating=[3.3],
        package="SOD323",
        diode_type="Bidirectional TVS",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "SP4020-01FTG": SeriesSpec(
        manufacturer="Littelfuse",
        base_series="SP4020-01FTG",
        part_number_suffix="",
        footprint="diode_footprints:SOD323",
        datasheet=(
            "https://www.littelfuse.com/assetdocs/tvs-diode-array-"
            "sp4020-datasheet?assetguid=b6e2c598-7d86-4fa2-a063-fb053ce07713"
        ),
        voltage_rating=[3.3],
        package="SOD323",
        diode_type="Unidirectional TVS",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "ESD9M5.0ST5G": SeriesSpec(
        manufacturer="Onsemi",
        base_series="ESD9M5.0ST5G",
        part_number_suffix="",
        footprint="diode_footprints:SOD323",
        datasheet=(
            "https://www.onsemi.com/download/data-sheet/pdf/esd9m5.0s-d.pdf"
        ),
        voltage_rating=[5.0],
        package="SOD_923",
        diode_type="Unidirectional TVS",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "SMCJ": SeriesSpec(
        manufacturer="STMicroelectronics",
        base_series="SMCJ",
        part_number_suffix="A/CA",
        footprint="diode_footprints:DO-214AB-2",
        datasheet=("https://www.st.com/resource/en/datasheet/smcj26a.pdf"),
        voltage_rating=[
            *[5, 6, 6.5, 8.5, 10, 12, 13, 15, 18, 20, 22, 24, 26, 28, 30],
            *[33, 36, 40, 48, 58, 70, 85, 100, 130, 154, 170, 188],
        ],
        package="DO-214AB-2",
        diode_type="Bidirectional TVS",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BZX384-A": SeriesSpec(
        manufacturer="Nexperia",
        base_series="BZX384-A",
        footprint="diode_footprints:SOD323",
        datasheet=(
            "https://assets.nexperia.com/documents/data-sheet/BZX384_SER.pdf"
        ),
        voltage_rating=[
            *[2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8],
            *[7.5, 8.2, 9.1, 10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30],
            *[33, 36, 39, 43, 47, 51, 56, 62, 68, 75],
        ],
        package="SOD323",
        diode_type="Zener",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BZX384-B": SeriesSpec(
        manufacturer="Nexperia",
        base_series="BZX384-B",
        footprint="diode_footprints:SOD323",
        datasheet=(
            "https://assets.nexperia.com/documents/data-sheet/BZX384_SER.pdf"
        ),
        voltage_rating=[
            *[2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8],
            *[7.5, 8.2, 9.1, 10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30],
            *[33, 36, 39, 43, 47, 51, 56, 62, 68, 75],
        ],
        package="SOD323",
        diode_type="Zener",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BZX384-C": SeriesSpec(
        manufacturer="Nexperia",
        base_series="BZX384-C",
        footprint="diode_footprints:SOD323",
        datasheet=(
            "https://assets.nexperia.com/documents/data-sheet/BZX384_SER.pdf"
        ),
        voltage_rating=[
            *[2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8],
            *[7.5, 8.2, 9.1, 10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30],
            *[33, 36, 39, 43, 47, 51, 56, 62, 68, 75],
        ],
        package="SOD323",
        diode_type="Zener",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "MSE1PB-M3/89A": SeriesSpec(
        manufacturer="Vishay",
        base_series="MSE1PB-M3/89A",
        footprint="diode_footprints:DO-219AD",
        datasheet="https://www.vishay.com/docs/89067/mse1pj.pdf",
        voltage_rating=[100.0],
        current_rating=[1.0],
        package="DO-219AD",
        diode_type="Rectifier",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BAT41KFILM": SeriesSpec(
        manufacturer="STMicroelectronics",
        base_series="BAT41KFILM",
        footprint="diode_footprints:SOD_523",
        datasheet="https://www.st.com/resource/en/datasheet/bat41.pdf",
        voltage_rating=[100.0],
        current_rating=[1.0],
        package="SOD_523",
        diode_type="Schottky",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "1N4148WX-TP": SeriesSpec(
        manufacturer="Micro Commercial Components",
        base_series="1N4148WX-TP",
        footprint="diode_footprints:SOD323",
        datasheet=(
            "https://www.mccsemi.com/pdf/Products/1N4148WX(SOD-323).pdf"
        ),
        voltage_rating=[100],
        package="SOD323",
        diode_type="Zener",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BZT52C": SeriesSpec(
        manufacturer="Diodes Incorporated",
        base_series="BZT52C",
        footprint="diode_footprints:SOD_123",
        datasheet=(
            "https://4donline.ihs.com/images/VipMasterIC/"
            "IC/DIOD/DIOD-S-A0003550684/DIOD-S-A0003550684-1.pdf?hkey="
            "CECEF36DEECDED6468708AAF2E19C0C6"
        ),
        voltage_rating=[
            *[2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6],
            *[6.2, 6.8, 7.5, 8.2, 9.1, 10, 11, 12, 13],
            *[15, 16, 18, 20, 22, 24],
            *[27, 30, 33, 36, 39, 43, 47, 51],
        ],
        current_rating=[0.5] * 51,
        package="SOD_123",
        diode_type="Zener",
        trustedparts_link="https://www.trustedparts.com/en/search",
        part_number_suffix="-7-F",
    ),
    "B240A-13-F": SeriesSpec(
        manufacturer="Diodes Incorporated",
        base_series="B240A-13-F",
        footprint="diode_footprints:SMA",
        datasheet=(
            "https://4donline.ihs.com/images/VipMasterIC/IC/"
            "DIOD/DIOD-S-A0001756908/DIOD-S-A0001756908-1.pdf?"
            "hkey=CECEF36DEECDED6468708AAF2E19C0C6"
        ),
        voltage_rating=[40],
        current_rating=[2],
        package="SMA",
        diode_type="Schottky",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "S1B-13-F": SeriesSpec(
        manufacturer="Diodes Incorporated",
        base_series="S1B-13-F",
        footprint="diode_footprints:SMA",
        datasheet=(
            "https://4donline.ihs.com/images/VipMasterIC/IC/DIOD/"
            "DIOD-S-A0007810797/DIOD-S-A0007810797-1.pdf?"
            "hkey=CECEF36DEECDED6468708AAF2E19C0C6"
        ),
        voltage_rating=[100],
        current_rating=[1],
        package="SMA",
        diode_type="Rectifier",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BAT46WJ,115": SeriesSpec(
        manufacturer="Nexperia",
        base_series="BAT46WJ,115",
        footprint="diode_footprints:SOD323F",
        part_number_suffix="",
        datasheet=(
            "https://assets.nexperia.com/documents/data-sheet/BAT46WJ.pdf"
        ),
        voltage_rating=[100.0],
        current_rating=[0.25],
        package="SOD323F",
        diode_type="Schottky",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "1N4448HWT-7": SeriesSpec(
        manufacturer="STMicroelectronics",
        base_series="1N4448HWT-7",
        footprint="diode_footprints:SOD_523",
        datasheet="https://www.diodes.com/assets/Datasheets/1N4448HWT.pdf",
        voltage_rating=[80.0],
        current_rating=[0.125],
        package="SOD_523",
        diode_type="Rectifier",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BAT54WS-7-F": SeriesSpec(
        manufacturer="Diodes Incorporated",
        base_series="BAT54WS-7-F",
        footprint="diode_footprints:SOD323F",
        part_number_suffix="",
        datasheet=(
            "https://eu.mouser.com/ProductDetail/Diodes-Incorporated/"
            "BAT54WS-7-F?qs=BJo294706GxanB6a%2FKrrdw%3D%3D"
        ),
        voltage_rating=[30.0],
        current_rating=[0.6],
        package="SOD323F",
        diode_type="Schottky",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
}
