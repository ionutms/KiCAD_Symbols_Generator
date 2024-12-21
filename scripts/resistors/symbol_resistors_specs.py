"""Specifications and data structures for Panasonic ERJ series resistors.

This module defines the specifications for various Panasonic ERJ series
resistors, supporting both E96 and E24 value series.
It provides comprehensive component information including physical dimensions,
electrical characteristics, and packaging options.
"""

from collections.abc import Iterator
from typing import Final, NamedTuple, Optional, Union


class SeriesSpec(NamedTuple):
    """Detailed specifications for a resistor series.

    Contains all necessary parameters to define a specific resistor series,
    including physical characteristics, electrical ratings,
    and available configurations.

    Attributes:
        mpn_prefix: Part number prefix
        footprint: PCB footprint ID for the component
        voltage_rating: Maximum operating voltage specification
        case_code_in: Package dimensions in inches (e.g., '0402')
        case_code_mm: Package dimensions in millimeters (e.g., '1005')
        power_rating: Maximum power dissipation specification
        resistance_range: Minimum and maximum resistance values in ohms
        mpn_sufix: Part number sufix
        tolerance_map:
            Maps series types to available tolerance codes and values
            Format: {str: {code: value}}
        datasheet: Complete URL to component datasheet
        manufacturer: Name of the component manufacturer
        trustedparts_url:
            Base URL for component listing on Trustedparts platform
        reference: Reference designator for the component
        excluded_values: Optional list of values to exclude from calculations
        specified_values: Optional list of values to specifically include

    """

    mpn_prefix: str
    footprint: str
    voltage_rating: str
    case_code_in: str
    case_code_mm: str
    power_rating: str
    mpn_sufix: str
    tolerance_map: dict[str, dict[str, str]]
    datasheet: str
    manufacturer: str
    trustedparts_url: str
    resistance_range: list[Union[int, float]]  # noqa: FA100
    temperature_coefficient: str
    reference: str = "R"
    excluded_values: Optional[list[float]] = None  # noqa: FA100
    specified_values: Optional[list[float]] = None  # noqa: FA100


E96_BASE_VALUES: Final[list[float]] = [
    10.0, 10.2, 10.5, 10.7, 11.0, 11.3, 11.5, 11.8, 12.1, 12.4, 12.7,
    13.0, 13.3, 13.7, 14.0, 14.3, 14.7, 15.0, 15.4, 15.8, 16.2, 16.5,
    16.9, 17.4, 17.8, 18.2, 18.7, 19.1, 19.6, 20.0, 20.5, 21.0, 21.5,
    22.1, 22.6, 23.2, 23.7, 24.3, 24.9, 25.5, 26.1, 26.7, 27.4, 28.0,
    28.7, 29.4, 30.1, 30.9, 31.6, 32.4, 33.2, 34.0, 34.8, 35.7, 36.5,
    37.4, 38.3, 39.2, 40.2, 41.2, 42.2, 43.2, 44.2, 45.3, 46.4, 47.5,
    48.7, 49.9, 51.1, 52.3, 53.6, 54.9, 56.2, 57.6, 59.0, 60.4, 61.9,
    63.4, 64.9, 66.5, 68.1, 69.8, 71.5, 73.2, 75.0, 76.8, 78.7, 80.6,
    82.5, 84.5, 86.6, 88.7, 90.9, 93.1, 95.3, 97.6,
]

E24_BASE_VALUES: Final[list[float]] = [
    10.0, 11.0, 12.0, 13.0, 15.0, 16.0, 18.0, 20.0, 22.0, 24.0, 27.0,
    30.0, 33.0, 36.0, 39.0, 43.0, 47.0, 51.0, 56.0, 62.0, 68.0, 75.0,
    82.0, 91.0,
]


class PartInfo(NamedTuple):
    """Container for detailed resistor component information.

    Stores comprehensive information about a specific resistor part,
    including its electrical characteristics, physical properties,
    and documentation links.

    Attributes:
        symbol_name: KiCad schematic symbol identifier
        reference: Component reference designator (e.g., 'R1')
        value: Resistance value in ohms (float)
        footprint: PCB footprint library reference
        datasheet: URL to component documentation
        description: Descriptive text about the component
        manufacturer: Component manufacturer name
        mpn: Manufacturer's part number
        tolerance: Component tolerance specification (e.g., '1%', '5%')
        voltage_rating: Maximum voltage specification
        case_code_in: Package dimensions in inches
        case_code_mm: Package dimensions in millimeters
        series: Component series identifier
        trustedparts_link: URL to component listing on Trustedparts

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
    voltage_rating: str
    case_code_in: str
    case_code_mm: str
    series: str
    trustedparts_link: str
    temperature_coefficient: str

    @classmethod
    def format_resistance_value(cls, resistance: float) -> str:
        """Convert a resistance value to a human-readable string format.

        Args:
            resistance: The resistance value in ohms

        Returns:
            A formatted string with appropriate unit suffix (Ω, kΩ, or MΩ)

        """
        def clean_number(num: float) -> str:
            return f"{num:g}"

        if resistance >= 1_000_000:  # noqa: PLR2004
            return f"{clean_number(resistance / 1_000_000)} MΩ"
        if resistance >= 1_000:  # noqa: PLR2004
            return f"{clean_number(resistance / 1_000)} kΩ"
        return f"{clean_number(resistance)} Ω"

    @classmethod
    def generate_resistance_code(
        cls,
        resistance: float,
        specs: SeriesSpec,
    ) -> str:
        """Generate the resistance code portion of a Panasonic part number.

        Args:
            resistance: The resistance value in ohms
            specs: Series specifications

        Returns:
            A string representing the resistance code

        Raises:
            ValueError: If resistance is outside valid range

        """
        # Unpack resistance range
        min_resistance, max_resistance = specs.resistance_range

        # Check resistance range first
        if resistance < min_resistance or resistance > max_resistance:
            msg = (
                f"Resistance value out of range "
                f"({min_resistance}Ω to {max_resistance}Ω)")
            raise ValueError(msg)

        # Special handling for Yageo manufacturer
        if specs.manufacturer == "Yageo":
            return cls._generate_yageo_resistance_code(resistance)

        # Special handling for specific ERJ series
        if specs.mpn_prefix in ("ERJ-2GEJ", "ERJ-3GEYJ", "ERJ-6GEYJ"):
            return cls._generate_erj_special_series_code(resistance)

        # Standard Panasonic/generic resistance code generation
        return cls._generate_standard_resistance_code(resistance)

    @classmethod
    def _generate_yageo_resistance_code(cls, resistance: float) -> str:
        """Generate resistance code for Yageo manufacturer."""
        if resistance < 1000:  # < 1kΩ  # noqa: PLR2004
            whole = int(resistance)
            decimal = str(int(round((resistance - whole) * 100))).rstrip("0")
            return f"{whole:01d}R{decimal}"

        if resistance < 10_000:  # 1-10kΩ  # noqa: PLR2004
            whole = int(resistance / 1000)
            decimal = str(int(round((resistance % 1000) / 10))).rstrip("0")
            return f"{whole}K{decimal}"

        # ≥ 10kΩ
        whole = int(resistance / 1000000)
        decimal = str(int(round((resistance % 1000000) / 10))).rstrip("0")
        return f"{whole}M{decimal}"

    @classmethod
    def _generate_erj_special_series_code(cls, resistance: float) -> str:
        """Generate resistance code for special ERJ series."""
        if resistance < 10:  # < 10Ω  # noqa: PLR2004
            whole = int(resistance)
            decimal = int(round((resistance - whole) * 10))
            return f"{whole:01d}R{decimal}"

        if resistance < 100:  # 10-99Ω  # noqa: PLR2004
            whole = int(resistance)
            decimal = int(round((resistance - whole) * 10))
            return f"{whole:01d}{decimal}"

        # Determine multiplier and significant digits for values ≥ 100Ω
        if resistance < 1000:  # 100-999Ω  # noqa: PLR2004
            significant = int(round(resistance / 10))
            multiplier = "1"
        elif resistance < 10000:  # 1k-9.99kΩ  # noqa: PLR2004
            significant = int(round(resistance / 100))
            multiplier = "2"
        elif resistance < 100000:  # 10k-99.9kΩ  # noqa: PLR2004
            significant = int(round(resistance / 1000))
            multiplier = "3"
        elif resistance < 1000000:  # 100k-999kΩ  # noqa: PLR2004
            significant = int(round(resistance / 10000))
            multiplier = "4"
        else:  # 1MΩ+
            significant = int(round(resistance / 100000))
            multiplier = "5"

        return f"{significant:02d}{multiplier}"

    @classmethod
    def _generate_standard_resistance_code(cls, resistance: float) -> str:
        """Generate standard resistance code for Panasonic style."""
        # Handle values less than 100Ω using R notation
        if resistance < 100:  # noqa: PLR2004
            whole = int(resistance)
            decimal = int(round((resistance - whole) * 10))
            return f"{whole:02d}R{decimal}"

        # For values ≥ 100Ω, determine multiplier and significant digits
        if resistance < 1000:  # 100-999Ω  # noqa: PLR2004
            significant = int(round(resistance))
            multiplier = "0"
        elif resistance < 10000:  # 1k-9.99kΩ  # noqa: PLR2004
            significant = int(round(resistance / 10))
            multiplier = "1"
        elif resistance < 100000:  # 10k-99.9kΩ  # noqa: PLR2004
            significant = int(round(resistance / 100))
            multiplier = "2"
        elif resistance < 1000000:  # 100k-999kΩ  # noqa: PLR2004
            significant = int(round(resistance / 1000))
            multiplier = "3"
        else:  # 1MΩ+
            significant = int(round(resistance / 10000))
            multiplier = "4"

        return f"{significant:03d}{multiplier}"

    @classmethod
    def create_part_info(
        cls,
        resistance: float,
        tolerance_value: str,
        packaging: str,
        specs: SeriesSpec,
    ) -> "PartInfo":
        """Create a PartInfo instance with complete component specifications.

        Args:
            resistance: Resistance value in ohms
            tolerance_value: Human-readable tolerance (e.g., '1%')
            packaging: Packaging code (e.g., 'X' or 'V')
            specs: SeriesSpec instance containing series specifications

        Returns:
            PartInfo instance containing all component details
            and vendor information

        """
        resistance_code = cls.generate_resistance_code(resistance, specs)
        packaging_code = packaging
        mpn = f"{specs.mpn_prefix}{resistance_code}{packaging_code}"

        description = (
            f"RES SMD {cls.format_resistance_value(resistance)} "
            f"{tolerance_value} {specs.case_code_in} {specs.voltage_rating}")
        trustedparts_link = f"{specs.trustedparts_url}{mpn}"

        datasheet = specs.datasheet
        if specs.manufacturer == "Yageo":
            datasheet = f"{specs.datasheet}{mpn}"

        return PartInfo(
            symbol_name=f"{specs.reference}_{mpn}",
            reference=specs.reference,
            value=resistance,
            footprint=specs.footprint,
            datasheet=datasheet,
            description=description,
            manufacturer=specs.manufacturer,
            mpn=mpn,
            tolerance=tolerance_value,
            voltage_rating=specs.voltage_rating,
            case_code_in=specs.case_code_in,
            case_code_mm=specs.case_code_mm,
            series=specs.mpn_prefix,
            trustedparts_link=trustedparts_link,
            temperature_coefficient=specs.temperature_coefficient,
        )

    @classmethod
    def generate_part_numbers(
        cls,
        specs: SeriesSpec,
    ) -> list["PartInfo"]:
        """Generate all possible part numbers for a resistor series.

        Args:
            specs: SeriesSpec instance containing series specifications

        Returns:
            List of PartInfo instances for all valid combinations

        """
        return [
            cls.create_part_info(
                resistance,
                tolerance_value,
                specs.mpn_sufix,
                specs,
            )
            for series_type in specs.tolerance_map
            for resistance in cls._filtered_resistance_values(
                E96_BASE_VALUES if series_type == "E96" else E24_BASE_VALUES,
                specs.resistance_range,
                specs.excluded_values,
                specs.specified_values,
            )
            for tolerance_value in [specs.tolerance_map[series_type]]
        ]

    @classmethod
    def _filtered_resistance_values(
        cls,
        base_values: list[float],
        resistance_range: list[Union[int, float]],  # noqa: FA100
        excluded_values: Optional[list[float]] = None,  # noqa: FA100
        specified_values: Optional[list[float]] = None,  # noqa: FA100
    ) -> Iterator[float]:
        """Generate resistance values with optional exclusions and inclusions.

        Args:
            base_values: List of base resistance values (E96 or E24 series)
            resistance_range:
                Minimum and maximum resistance values to generate
            excluded_values: Optional list of values to exclude
            specified_values: Optional list of values to include if not None

        Yields:
            float: Valid resistance values in ascending order

        """
        min_resistance, max_resistance = resistance_range
        multipliers = [0.1, 1, 10, 100, 1000, 10000, 100000, 1000000]

        for base_value in base_values:
            for multiplier in multipliers:
                resistance = round(base_value * multiplier, 2)

                # Check if resistance is within range
                is_within_range = \
                    min_resistance <= resistance <= max_resistance

                # Check exclusion conditions
                is_not_excluded = (
                    excluded_values is None or
                    resistance not in excluded_values
                )

                # Check specified values condition
                is_specified = (
                    specified_values is None or
                    resistance in specified_values
                )

                # Yield only if all conditions are met
                if is_within_range and is_not_excluded and is_specified:
                    yield resistance

PANASONIC_SYMBOLS_SPECS: Final[dict[str, SeriesSpec]] = {
    "ERJ-2RKF": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-2RKF",
        mpn_sufix="X",
        footprint="resistor_footprints:R_0402_1005Metric",
        voltage_rating="50V",
        case_code_in="0402",
        case_code_mm="1005",
        power_rating="0.1W",
        temperature_coefficient="100 ppm/°C",
        resistance_range=[10, 1_000_000],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C304.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "ERJ-3EKF": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-3EKF",
        mpn_sufix="V",
        footprint="resistor_footprints:R_0603_1608Metric",
        voltage_rating="75V",
        case_code_in="0603",
        case_code_mm="1608",
        power_rating="0.1W",
        temperature_coefficient="100 ppm/°C",
        resistance_range=[10, 1_000_000],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C304.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "ERJ-6ENF": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-6ENF",
        mpn_sufix="V",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        temperature_coefficient="100 ppm/°C",
        resistance_range=[10, 2_200_000],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C304.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "ERJ-P08F": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-P08F",
        mpn_sufix="V",
        footprint="resistor_footprints:R_1206_3216Metric",
        voltage_rating="500V",
        case_code_in="1206",
        case_code_mm="3216",
        power_rating="0.66W",
        temperature_coefficient="100 ppm/°C",
        resistance_range=[10, 1_000_000],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDO0000/AOA0000C331.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "ERJ-P06F": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-P06F",
        mpn_sufix="V",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="400V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.5W",
        temperature_coefficient="100 ppm/°C",
        resistance_range=[10, 1_000_000],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDO0000/AOA0000C331.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "ERJ-P03F": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-P03F",
        mpn_sufix="V",
        footprint="resistor_footprints:R_0603_1608Metric",
        voltage_rating="150V",
        case_code_in="0603",
        case_code_mm="1608",
        power_rating="0.25W",
        temperature_coefficient="150 ppm/°C",
        resistance_range=[10, 1_000_000],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDO0000/AOA0000C331.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "ERJ-2GEJ": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-2GEJ",
        mpn_sufix="X",
        footprint="resistor_footprints:R_0402_1005Metric",
        voltage_rating="50V",
        case_code_in="0402",
        case_code_mm="1005",
        power_rating="0.1W",
        temperature_coefficient="200 ppm/°C",
        resistance_range=[1, 1_000_000],
        tolerance_map={"E24": "5%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C301.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "ERJ-3GEYJ": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-3GEYJ",
        mpn_sufix="V",
        footprint="resistor_footprints:R_0603_1608Metric",
        voltage_rating="75V",
        case_code_in="0603",
        case_code_mm="1608",
        power_rating="0.1W",
        temperature_coefficient="200 ppm/°C",
        resistance_range=[1, 1_000_000],
        tolerance_map={"E24": "5%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C301.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "ERJ-6GEYJ": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-6GEYJ",
        mpn_sufix="V",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        temperature_coefficient="200 ppm/°C",
        resistance_range=[1, 1_000_000],
        tolerance_map={"E24": "5%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C301.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/"),
}

YAGEO_SYMBOLS_SPECS: Final[dict[str, SeriesSpec]] = {
    "RT0805BRA07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RT0805BRA07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        temperature_coefficient="5 ppm/°C",
        resistance_range=[20, 50_000],
        specified_values=[41.2, 205, 806, 1000, 1800, 2000, 3000, 6800],
        tolerance_map={"E96": "0.1%", "E24": "0.1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "RT0805BRB07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RT0805BRB07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        temperature_coefficient="10 ppm/°C",
        resistance_range=[4.7, 1_000_000],
        excluded_values=[
            6.04, 8.06, 9.09, 1070, 2050, 3010, 4020, 6040, 8060, 9090,
            100000, 102000, 105000, 107000, 110000, 113000, 115000, 118000,
            120000, 121000, 124000, 127000, 130000, 133000, 137000, 140000,
            143000, 147000, 150000, 154000, 158000, 160000, 162000, 165000,
            169000, 174000, 178000, 180000, 182000, 187000, 191000, 196000,
            200000, 205000, 210000, 215000, 220000, 221000, 226000, 232000,
            237000, 240000, 243000, 249000, 255000, 261000, 267000, 270000,
            274000, 280000, 287000, 294000, 300000, 301000, 309000, 316000,
            324000, 330000, 332000, 340000, 348000, 357000, 360000, 365000,
            374000, 383000, 390000, 392000, 402000, 412000, 422000, 430000,
            432000, 442000, 453000, 464000, 470000, 475000, 487000, 499000,
            510000, 511000, 523000, 536000, 549000, 560000, 562000, 576000,
            590000, 604000, 619000, 620000, 634000, 649000, 665000, 680000,
            681000, 698000, 715000, 732000, 750000, 768000, 787000, 806000,
            820000, 825000, 845000, 866000, 887000, 909000, 910000, 931000,
            953000, 976000],
        tolerance_map={"E96": "0.1%", "E24": "0.1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "RT0805BRC07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RT0805BRC07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        temperature_coefficient="15 ppm/°C",
        resistance_range=[4.7, 1_000_000],
        excluded_values=[
            6.04, 8.06, 9.09, 1070, 2050, 3010, 4020, 6040, 8060, 9090,
            100000, 102000, 105000, 107000, 110000, 113000, 115000, 118000,
            120000, 121000, 124000, 127000, 130000, 133000, 137000, 140000,
            143000, 147000, 150000, 154000, 158000, 160000, 162000, 165000,
            169000, 174000, 178000, 180000, 182000, 187000, 191000, 196000,
            200000, 205000, 210000, 215000, 220000, 221000, 226000, 232000,
            237000, 240000, 243000, 249000, 255000, 261000, 267000, 270000,
            274000, 280000, 287000, 294000, 300000, 301000, 309000, 316000,
            324000, 330000, 332000, 340000, 348000, 357000, 360000, 365000,
            374000, 383000, 390000, 392000, 402000, 412000, 422000, 430000,
            432000, 442000, 453000, 464000, 470000, 475000, 487000, 499000,
            510000, 511000, 523000, 536000, 549000, 560000, 562000, 576000,
            590000, 604000, 619000, 620000, 634000, 649000, 665000, 680000,
            681000, 698000, 715000, 732000, 750000, 768000, 787000, 806000,
            820000, 825000, 845000, 866000, 887000, 909000, 910000, 931000,
            953000, 976000, 1000000],
        tolerance_map={"E96": "0.1%", "E24": "0.1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "RT0805BRD07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RT0805BRD07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        temperature_coefficient="25 ppm/°C",
        resistance_range=[1, 1_500_000],
        excluded_values=[
            1.07, 2.05, 3.01, 4.02, 6.04, 8.06, 9.09, 1070, 2050, 3010, 4020,
            6040, 8060, 9090, 100000, 102000, 105000, 107000, 110000, 113000,
            115000, 118000, 120000, 121000, 124000, 127000, 130000, 133000,
            137000, 140000, 143000, 147000, 150000, 154000, 158000, 160000,
            162000, 165000, 169000, 174000, 178000, 180000, 182000, 187000,
            191000, 196000, 200000, 205000, 210000, 215000, 220000, 221000,
            226000, 232000, 237000, 240000, 243000, 249000, 255000, 261000,
            267000, 270000, 274000, 280000, 287000, 294000, 300000, 301000,
            309000, 316000, 324000, 330000, 332000, 340000, 348000, 357000,
            360000, 365000, 374000, 383000, 390000, 392000, 402000, 412000,
            422000, 430000, 432000, 442000, 453000, 464000, 470000, 475000,
            487000, 499000, 510000, 511000, 523000, 536000, 549000, 560000,
            562000, 576000, 590000, 604000, 619000, 620000, 634000, 649000,
            665000, 680000, 681000, 698000, 715000, 732000, 750000, 768000,
            787000, 806000, 820000, 825000, 845000, 866000, 887000, 909000,
            910000, 931000, 953000, 976000, 1070000.0],
        tolerance_map={"E96": "0.1%", "E24": "0.1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "RT0805BRE07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RT0805BRE07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        temperature_coefficient="50 ppm/°C",
        resistance_range=[1, 1_500_000],
        excluded_values=[
            1.07, 2.05, 3.01, 3.9, 4.02, 6.04, 8.06, 9.09, 1070, 2050, 3010,
            4020, 6040, 8060, 9090, 100000, 102000, 105000, 107000, 110000,
            113000, 115000, 118000, 120000, 121000, 124000, 127000, 130000,
            133000, 137000, 140000, 143000, 147000, 150000, 154000, 158000,
            160000, 162000, 165000, 169000, 174000, 178000, 180000, 182000,
            187000, 191000, 196000, 200000, 205000, 210000, 215000, 220000,
            221000, 226000, 232000, 237000, 240000, 243000, 249000, 255000,
            261000, 267000, 270000, 274000, 280000, 287000, 294000, 300000,
            301000, 309000, 316000, 324000, 330000, 332000, 340000, 348000,
            357000, 360000, 365000, 374000, 383000, 390000, 392000, 402000,
            412000, 422000, 430000, 432000, 442000, 453000, 464000, 470000,
            475000, 487000, 499000, 510000, 511000, 523000, 536000, 549000,
            560000, 562000, 576000, 590000, 604000, 619000, 620000, 634000,
            649000, 665000, 680000, 681000, 698000, 715000, 732000, 750000,
            768000, 787000, 806000, 820000, 825000, 845000, 866000, 887000,
            909000, 910000, 931000, 953000, 976000, 1070000],
        tolerance_map={"E96": "0.1%", "E24": "0.1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "RT0805CRE07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RT0805CRE07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        temperature_coefficient="50 ppm/°C",
        resistance_range=[1, 1_050_000],
        tolerance_map={"E96": "0.25%", "E24": "0.25%"},
        excluded_values=[
            1, 1.07, 1.1, 1.13, 1.15, 1.18, 1.2, 1.21, 1.24, 1.27, 1.3, 1.33,
            1.37, 1.4, 1.43, 1.47, 1.5, 1.54, 1.58, 1.6, 1.62, 1.65, 1.69,
            1.74, 1.78, 1.8, 1.82, 1.87, 1.91, 1.96, 2, 2.05, 2.1, 2.15, 2.2,
            2.21, 2.26, 2.32, 2.37, 2.4, 2.43, 2.49, 2.55, 2.61, 2.67, 2.7,
            2.74, 2.8, 2.87, 2.94, 3, 3.01, 3.16, 3.24, 3.3, 3.32, 3.4, 3.48,
            3.57, 3.6, 3.65, 3.74, 3.83, 3.9, 3.92, 4.02, 4.12, 4.22, 4.3,
            4.32, 4.42, 4.53, 4.64, 4.7, 4.75, 4.87, 4.99, 5.1, 5.11, 5.23,
            5.36, 5.49, 5.6, 5.62, 5.76, 5.9, 6.04, 6.19, 6.2, 6.34, 6.49,
            6.65, 6.81, 6.98, 7.15, 7.32, 7.5, 7.68, 7.87, 8.06, 8.25, 8.45,
            8.66, 8.87, 9.09, 9.1, 9.31, 9.53, 9.76, 10, 10.2, 10.5, 10.7, 11,
            11.3, 11.5, 11.8, 12, 12.1, 12.4, 12.7, 13, 13.3, 13.7, 14, 14.3,
            14.7, 15, 15.4, 15.8, 16, 16.2, 16.5, 16.9, 17.4, 17.8, 18.2,
            18.7, 19.1, 19.6, 20, 20.5, 21, 21.5, 22, 22.1, 22.6, 23.2, 23.7,
            24, 24.3, 25.5, 26.1, 26.7, 27, 27.4, 28, 28.7, 29.4, 30, 30.1,
            30.9, 31.6, 32.4, 33, 33.2, 34, 34.8, 35.7, 36.5, 37.4, 38.3, 39,
            39.2, 40.2, 41.2, 42.2, 43, 43.2, 44.2, 45.3, 46.4, 47, 47.5,
            48.7, 49.9, 51, 51.1, 52.3, 53.6, 54.9, 56, 56.2, 57.6, 59, 61.9,
            62, 63.4, 64.9, 66.5, 68, 68.1, 69.8, 71.5, 73.2, 76.8, 78.7,
            80.6, 82, 82.5, 84.5, 86.6, 88.7, 90.9, 91, 93.1, 95.3, 97.6, 102,
            105, 107, 113, 115, 118, 120, 121, 127, 130, 133, 137, 140, 143,
            147, 150, 154, 158, 160, 162, 165, 169, 174, 178, 180, 182, 187,
            191, 196, 205, 210, 215, 220, 221, 226, 232, 237, 240, 243, 249,
            255, 261, 267, 270, 274, 280, 287, 294, 300, 301, 309, 316, 324,
            330, 332, 340, 348, 357, 360, 365, 383, 390, 392, 412, 422, 430,
            432, 442, 453, 464, 470, 475, 487, 499, 511, 523, 536, 549, 560,
            562, 576, 590, 604, 619, 620, 634, 649, 665, 681, 698, 715, 732,
            750, 768, 787, 806, 820, 825, 845, 866, 887, 910, 931, 953, 976,
            1070, 1100, 1130, 1150, 1180, 1210, 1240, 1300, 1330, 1370, 1400,
            1430, 1470, 1540, 1580, 1600, 1620, 1650, 1690, 1740, 1780, 1820,
            1870, 1910, 1960, 2000, 2050, 2100, 2150, 2200, 2210, 2260, 2370,
            2400, 2550, 2610, 2670, 2740, 2800, 2870, 2940, 3010, 3240, 3320,
            3400, 3480, 3600, 3650, 3740, 3830, 3900, 3920, 4020, 4120, 4220,
            4300, 4320, 4420, 4530, 4640, 4750, 4870, 5110, 5230, 5360, 5600,
            5760, 5900, 6040, 6200, 6340, 6490, 6650, 6800, 6810, 6980, 7150,
            7320, 7500, 7680, 7870, 8060, 8200, 8250, 8450, 8660, 8870, 9090,
            9310, 9530, 9760, 100000, 102000, 105000, 107000, 110000, 113000,
            115000, 118000, 120000, 121000, 124000, 127000, 130000, 133000,
            137000, 140000, 143000, 147000, 150000, 154000, 158000, 160000,
            162000, 165000, 169000, 174000, 178000, 180000, 182000, 187000,
            191000, 196000, 200000, 205000, 210000, 215000, 220000, 221000,
            226000, 232000, 237000, 240000, 243000, 249000, 255000, 261000,
            267000, 270000, 274000, 280000, 287000, 294000, 300000, 301000,
            309000, 316000, 324000, 330000, 332000, 340000, 348000, 357000,
            360000, 365000, 374000, 383000, 390000, 392000, 402000, 412000,
            422000, 430000, 432000, 442000, 453000, 464000, 470000, 475000,
            487000, 499000, 510000, 511000, 523000, 536000, 549000, 560000,
            562000, 576000, 590000, 604000, 619000, 620000, 634000, 649000,
            665000, 680000, 681000, 698000, 715000, 732000, 750000, 768000,
            787000, 806000, 820000, 825000, 845000, 866000, 887000, 909000,
            910000, 931000, 953000, 976000],
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "RT0805DRE07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RT0805DRE07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        temperature_coefficient="50 ppm/°C",
        resistance_range=[1, 1_500_000],
        excluded_values=[
            1.02, 1.05, 1.07, 1.1, 1.13, 1.15, 1.18, 1.2, 1.21, 1.24, 1.27,
            1.3, 1.33, 1.37, 1.4, 1.43, 1.47, 1.5, 1.54, 1.58, 1.6, 1.62,
            1.65, 1.69, 1.74, 1.78, 1.8, 1.82, 1.87, 1.91, 1.96, 2.05, 2.26,
            2.32, 2.37, 2.4, 2.49, 2.55, 2.61, 2.67, 2.7, 2.74, 2.8, 2.87,
            2.94, 3.01, 3.16, 3.24, 3.3, 3.32, 3.4, 3.48, 3.57, 3.6, 3.65,
            3.74, 3.83, 3.92, 4.02, 4.12, 4.22, 4.3, 4.32, 4.42, 4.53, 4.64,
            4.75, 4.87, 5.11, 5.23, 5.36, 5.49, 5.62, 5.76, 5.9, 6.04, 6.19,
            6.34, 6.49, 6.65, 6.98, 7.15, 7.32, 7.68, 7.87, 8.06, 8.25, 8.45,
            8.66, 8.87, 9.09, 9.31, 9.53, 9.76, 10.2, 10.7, 11.3, 11.5, 11.8,
            12.7, 13.3, 13.7, 14.7, 15.4, 15.8, 16.5, 17.8, 18.7, 20.5, 21,
            23.7, 24.3, 25.5, 26.7, 28, 30.9, 31.6, 35.7, 41.2, 43.2, 44.2,
            46.4, 53.6, 59, 71.5, 73.2, 76.8, 84.5, 88.7, 95.3, 97.6, 105,
            107, 137, 215, 226, 316, 365, 392, 536, 820, 910, 1070, 1180,
            1650, 1870, 2050, 3010, 4020, 5760, 6040, 8060, 9090, 100000,
            102000, 105000, 107000, 110000, 113000, 115000, 118000, 120000,
            121000, 124000, 127000, 130000, 133000, 137000, 140000, 143000,
            147000, 150000, 154000, 158000, 160000, 162000, 165000, 169000,
            174000, 178000, 180000, 182000, 187000, 191000, 196000, 200000,
            205000, 210000, 215000, 220000, 221000, 226000, 232000, 237000,
            240000, 243000, 249000, 255000, 261000, 267000, 270000, 274000,
            280000, 287000, 294000, 300000, 301000, 309000, 316000, 324000,
            330000, 332000, 340000, 348000, 357000, 360000, 365000, 374000,
            383000, 390000, 392000, 402000, 412000, 422000, 430000, 432000,
            442000, 453000, 464000, 470000, 475000, 487000, 499000, 510000,
            511000, 523000, 536000, 549000, 560000, 562000, 576000, 590000,
            604000, 619000, 620000, 634000, 649000, 665000, 680000, 681000,
            698000, 715000, 732000, 750000, 768000, 787000, 806000, 820000,
            825000, 845000, 866000, 887000, 909000, 910000, 931000, 953000,
            976000, 1070000, 1100000, 1150000, 1180000, 1200000, 1210000,
            1240000, 1270000, 1300000, 1330000, 1370000, 1400000, 1430000,
            1470000],
        tolerance_map={"E96": "0.5%", "E24": "0.5%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "RT0805FRE07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RT0805FRE07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        temperature_coefficient="50 ppm/°C",
        resistance_range=[1, 1_500_000],
        excluded_values=[
            1.07, 1.1, 1.13, 1.15, 1.18, 1.21, 1.24, 1.27, 1.3, 1.33, 1.37,
            1.47, 1.54, 1.58, 1.62, 1.69, 1.74, 1.78, 1.82, 1.87, 1.91, 1.96,
            2.05, 2.1, 2.15, 2.21, 2.26, 2.32, 2.37, 2.43, 2.55, 2.61, 2.67,
            2.8, 2.87, 2.94, 3.01, 3.16, 3.24, 3.4, 3.57, 3.65, 3.74, 3.83,
            3.92, 4.02, 4.3, 4.32, 4.42, 4.53, 4.64, 4.87, 5.11, 5.49, 5.76,
            5.9, 6.04, 6.19, 6.34, 6.65, 6.81, 7.15, 7.32, 7.68, 7.87, 8.06,
            8.45, 8.66, 8.87, 9.09, 9.31, 9.53, 9.76, 10.2, 10.7, 11.8, 12.4,
            12.7, 13.3, 13.7, 14, 16.5, 16.9, 17.8, 18.7, 19.1, 19.6, 23.2,
            23.7, 26.1, 27.4, 28.7, 29.4, 30.9, 32.4, 34, 38.3, 41.2, 42.2,
            43.2, 44.2, 52.3, 57.6, 59, 63.4, 66.5, 73.2, 84.5, 86.6, 107,
            127, 143, 165, 169, 210, 309, 412, 1070, 2050, 3010, 3240, 4020,
            5360, 6040, 8060, 9090, 100000, 102000, 105000, 107000, 110000,
            113000, 115000, 118000, 120000, 121000, 124000, 127000, 130000,
            133000, 137000, 140000, 143000, 147000, 150000, 154000, 158000,
            160000, 162000, 165000, 169000, 174000, 178000, 180000, 182000,
            187000, 191000, 196000, 200000, 205000, 210000, 215000, 220000,
            221000, 226000, 232000, 237000, 240000, 243000, 249000, 255000,
            261000, 267000, 270000, 274000, 280000, 287000, 294000, 300000,
            301000, 309000, 316000, 324000, 330000, 332000, 340000, 348000,
            357000, 360000, 365000, 374000, 383000, 390000, 392000, 402000,
            412000, 422000, 430000, 432000, 442000, 453000, 464000, 470000,
            475000, 487000, 499000, 510000, 511000, 523000, 536000, 549000,
            560000, 562000, 576000, 590000, 604000, 619000, 620000, 634000,
            649000, 665000, 680000, 681000, 698000, 715000, 732000, 750000,
            768000, 787000, 806000, 820000, 825000, 845000, 866000, 887000,
            909000, 910000, 931000, 953000, 976000, 1070000, 1130000, 1150000,
            1180000, 1240000, 1270000, 1300000, 1330000, 1370000, 1400000,
            1430000, 1470000],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "RT0805FRD07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RT0805FRD07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        temperature_coefficient="25 ppm/°C",
        resistance_range=[1, 1_050_000],
        excluded_values=[
            1.07, 1.1, 1.13, 1.15, 1.18, 1.2, 1.21, 1.24, 1.27, 1.3, 1.33,
            1.37, 1.4, 1.43, 1.47, 1.54, 1.58, 1.6, 1.62, 1.65, 1.69, 1.74,
            1.78, 1.8, 1.82, 1.87, 1.91, 1.96, 2.05, 2.1, 2.15, 2.21, 2.26,
            2.32, 2.37, 2.4, 2.49, 2.55, 2.61, 2.67, 2.7, 2.74, 2.8, 2.87,
            2.94, 3.01, 3.16, 3.24, 3.32, 3.4, 3.48, 3.57, 3.65, 3.74, 3.83,
            3.92, 4.02, 4.12, 4.22, 4.3, 4.32, 4.42, 4.53, 4.64, 4.87, 4.99,
            5.11, 5.23, 5.36, 5.49, 5.6, 5.62, 5.76, 5.9, 6.04, 6.19, 6.34,
            6.49, 6.81, 6.98, 7.15, 7.32, 7.68, 7.87, 8.06, 8.25, 8.45, 8.66,
            8.87, 9.09, 9.1, 9.31, 9.53, 9.76, 10.2, 10.5, 10.7, 11.3, 11.5,
            11.8, 12.1, 12.4, 12.7, 13, 13.3, 13.7, 14, 14.3, 14.7, 15.4,
            15.8, 16, 16.2, 16.5, 17.4, 17.8, 18.2, 18.7, 19.1, 19.6, 20.5,
            21, 21.5, 22.1, 22.6, 23.2, 23.7, 24, 24.3, 25.5, 26.1, 26.7,
            27.4, 28, 28.7, 29.4, 30.1, 30.9, 31.6, 32.4, 33.2, 34, 34.8,
            35.7, 36.5, 37.4, 38.3, 39.2, 40.2, 41.2, 42.2, 43, 43.2, 44.2,
            45.3, 46.4, 48.7, 52.3, 53.6, 54.9, 56, 56.2, 57.6, 59, 60.4,
            61.9, 63.4, 64.9, 66.5, 68.1, 69.8, 71.5, 73.2, 76.8, 78.7, 80.6,
            82, 82.5, 84.5, 86.6, 88.7, 90.9, 93.1, 95.3, 97.6, 102, 105,
            107, 110, 113, 115, 118, 121, 124, 127, 130, 133, 137, 140, 143,
            147, 154, 160, 162, 165, 169, 174, 178, 180, 182, 187, 191, 196,
            215, 226, 232, 237, 243, 255, 261, 267, 274, 280, 287, 294, 309,
            316, 324, 332, 340, 348, 357, 360, 365, 374, 383, 392, 402, 412,
            422, 430, 432, 442, 453, 464, 487, 523, 536, 549, 576, 590, 604,
            619, 620, 649, 681, 698, 715, 732, 768, 806, 845, 866, 909, 931,
            953, 976, 1070, 1100, 1130, 1150, 1180, 1240, 1270, 1330, 1370,
            1400, 1430, 1470, 1540, 1580, 1620, 1650, 1690, 1740, 1780, 1820,
            1870, 1960, 2050, 2100, 2150, 2210, 2260, 2320, 2370, 2400, 2430,
            2550, 2610, 2670, 2740, 2800, 2870, 2940, 3010, 3160, 3240, 3480,
            3570, 3600, 3650, 3740, 3830, 3920, 4020, 4120, 4220, 4320, 4530,
            4640, 4750, 4870, 5110, 5230, 5360, 5490, 5620, 5760, 5900, 6040,
            6190, 6200, 6340, 6490, 6650, 6810, 6980, 7150, 7320, 7680, 7870,
            8060, 8250, 8450, 8660, 8870, 9090, 9310, 9530, 9760, 100000,
            102000, 105000, 107000, 110000, 113000, 115000, 118000, 120000,
            121000, 124000, 127000, 130000, 133000, 137000, 140000, 143000,
            147000, 150000, 154000, 158000, 160000, 162000, 165000, 169000,
            174000, 178000, 180000, 182000, 187000, 191000, 196000, 200000,
            205000, 210000, 215000, 220000, 221000, 226000, 232000, 237000,
            240000, 243000, 249000, 255000, 261000, 267000, 270000, 274000,
            280000, 287000, 294000, 300000, 301000, 309000, 316000, 324000,
            330000, 332000, 340000, 348000, 357000, 360000, 365000, 374000,
            383000, 390000, 392000, 402000, 412000, 422000, 430000, 432000,
            442000, 453000, 464000, 470000, 475000, 487000, 499000, 510000,
            511000, 523000, 536000, 549000, 560000, 562000, 576000, 590000,
            604000, 619000, 620000, 634000, 649000, 665000, 680000, 681000,
            698000, 715000, 732000, 750000, 768000, 787000, 806000, 820000,
            825000, 845000, 866000, 887000, 909000, 910000, 931000, 953000,
            976000],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "RT1206FRE07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RT1206FRE07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_1206_3216Metric",
        voltage_rating="200V",
        case_code_in="1206",
        case_code_mm="3216",
        power_rating="0.125W",
        temperature_coefficient="50 ppm/°C",
        resistance_range=[1, 1_500_000],
        excluded_values=[
            1.07, 1.13, 1.15, 1.18, 1.21, 1.24, 1.27, 1.33, 1.37, 1.4, 1.43,
            1.47, 1.54, 1.58, 1.62, 1.65, 1.69, 1.74, 1.78, 1.82, 1.87, 1.91,
            2.05, 2.1, 2.21, 2.26, 2.32, 2.37, 2.43, 2.55, 2.61, 2.67, 2.74,
            2.8, 2.87, 3.01, 3.16, 3.24, 3.32, 3.4, 3.48, 3.57, 3.65, 3.74,
            3.83, 3.92, 4.02, 4.22, 4.32, 4.42, 4.53, 4.64, 4.75, 4.87, 4.99,
            5.11, 5.23, 5.36, 5.49, 5.62, 5.76, 5.9, 6.04, 6.19, 6.34, 6.49,
            6.65, 6.98, 7.15, 7.68, 7.87, 8.06, 8.66, 8.87, 9.09, 9.31, 9.53,
            9.76, 10.2, 10.5, 10.7, 11.3, 11.5, 11.8, 12.4, 12.7, 13.3, 13.7,
            14.3, 15.8, 16.5, 17.4, 17.8, 18.7, 19.6, 20.5, 26.1, 28, 29.4,
            43.2, 102, 107, 115, 127, 137, 143, 169, 237, 280, 309, 357, 412,
            453, 523, 549, 649, 698, 787, 866, 887, 976, 1070, 2050, 3010,
            3570, 4020, 5490, 5760, 5900, 6040, 6980, 8060, 9090, 9760,
            100000, 102000, 105000, 107000, 110000, 113000, 115000, 118000,
            120000, 121000, 124000, 127000, 130000, 133000, 137000, 140000,
            143000, 147000, 150000, 154000, 158000, 160000, 162000, 165000,
            169000, 174000, 178000, 180000, 182000, 187000, 191000, 196000,
            200000, 205000, 210000, 215000, 220000, 221000, 226000, 232000,
            237000, 240000, 243000, 249000, 255000, 261000, 267000, 270000,
            274000, 280000, 287000, 294000, 300000, 301000, 309000, 316000,
            324000, 330000, 332000, 340000, 348000, 357000, 360000, 365000,
            374000, 383000, 390000, 392000, 402000, 412000, 422000, 430000,
            432000, 442000, 453000, 464000, 470000, 475000, 487000, 499000,
            510000, 511000, 523000, 536000, 549000, 560000, 562000, 576000,
            590000, 604000, 619000, 620000, 634000, 649000, 665000, 680000,
            681000, 698000, 715000, 732000, 750000, 768000, 787000, 806000,
            820000, 825000, 845000, 866000, 887000, 909000, 910000, 931000,
            953000, 976000, 1070000, 1130000, 1150000, 1180000, 1240000,
            1270000, 1330000, 1370000, 1400000, 1430000, 1470000],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "RT1210FRE07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RT1210FRE07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_1210_3225Metric",
        voltage_rating="200V",
        case_code_in="1210",
        case_code_mm="3225",
        power_rating="0.125W",
        temperature_coefficient="50 ppm/°C",
        resistance_range=[10, 6_800],
        specified_values=[
            10, 15, 20, 24.9, 27, 33.2, 73.2, 100, 105, 110, 137, 150, 158,
            220, 240, 330, 470, 511, 909, 1000, 1470, 1500, 2490, 3300,
            3600, 3650, 3900, 4700, 4990, 6650, 6800],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="),
        trustedparts_url="https://www.trustedparts.com/en/search/"),
}

# Combined specifications dictionary
SYMBOLS_SPECS: Final[dict[str, SeriesSpec]] = {
    **PANASONIC_SYMBOLS_SPECS, **YAGEO_SYMBOLS_SPECS}
