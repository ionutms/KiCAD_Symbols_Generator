"""Specifications and data structures for Panasonic ERJ series resistors.

This module defines the specifications for various Panasonic ERJ series
resistors, supporting both E96 and E24 value series.
It provides comprehensive component information including physical dimensions,
electrical characteristics, and packaging options.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Final, NamedTuple

if TYPE_CHECKING:
    from collections.abc import Iterator


class SeriesSpec(NamedTuple):
    """Detailed specifications for a resistor series.

    Contains all necessary parameters to define a specific resistor series,
    including physical characteristics, electrical ratings,
    and available configurations.

    Attributes:
        mpn_prefix: Manufacturer's part number prefix
        footprint: KiCad footprint library reference
        voltage_rating: Maximum voltage rating
        case_code_in: Package dimensions in inches
        case_code_mm: Package dimensions in millimeters
        power_rating: Maximum power rating
        mpn_sufix: Manufacturer's part number suffix
        tolerance_map: Mapping of tolerance series to human-readable values
        datasheet: URL to component datasheet
        manufacturer: Component manufacturer name
        trustedparts_url: URL to component listing on Trustedparts
        resistance_range: Minimum and maximum resistance values
        temperature_coefficient: Temperature coefficient specification
        reference: Reference designator prefix (default: 'R')
        excluded_values: Optional list of excluded resistance values
        specified_values: Optional list of specified resistance values
        extra_values: Optional list of additional resistance values
        component_type: Component type (default: 'Resistor')

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
    resistance_range: list[int | float]
    temperature_coefficient: str
    reference: str = "R"
    component_type: str = "Resistor"
    excluded_values: list[float] | None = None
    specified_values: list[float] | None = None
    extra_values: list[float] | None = None


E96_BASE_VALUES: Final[list[float]] = [
    *[10, 10.2, 10.5, 10.7, 11, 11.3, 11.5, 11.8, 12.1, 12.4, 12.7, 13, 13.3],
    *[13.7, 14, 14.3, 14.7, 15, 15.4, 15.8, 16.2, 16.5, 16.9, 17.4, 17.8],
    *[18.2, 18.7, 19.1, 19.6, 20, 20.5, 21, 21.5, 22.1, 22.6, 23.2, 23.7],
    *[24.3, 24.9, 25.5, 26.1, 26.7, 27.4, 28, 28.7, 29.4, 30.1, 30.9, 31.6],
    *[32.4, 33.2, 34, 34.8, 35.7, 36.5, 37.4, 38.3, 39.2, 40.2, 41.2, 42.2],
    *[43.2, 44.2, 45.3, 46.4, 47.5, 48.7, 49.9, 51.1, 52.3, 53.6, 54.9, 56.2],
    *[57.6, 59, 60.4, 61.9, 63.4, 64.9, 66.5, 68.1, 69.8, 71.5, 73.2, 75],
    *[76.8, 78.7, 80.6, 82.5, 84.5, 86.6, 88.7, 90.9, 93.1, 95.3, 97.6],
]

E24_BASE_VALUES: Final[list[float]] = [
    *[10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30],
    *[33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91],
]


class PartInfo(NamedTuple):
    """Container for detailed resistor component information.

    Stores comprehensive information about a specific resistor part,
    including its electrical characteristics, physical properties,
    and documentation links.

    Attributes:
        symbol_name: KiCad symbol reference name
        reference: Reference designator prefix (default: 'R')
        value: Resistance value in ohms
        footprint: KiCad footprint library reference
        datasheet: URL to component datasheet
        description: Human-readable component description
        manufacturer: Component manufacturer name
        mpn: Manufacturer's part number
        tolerance: Tolerance specification (e.g., '1%')
        voltage_rating: Maximum voltage rating
        case_code_in: Package dimensions in inches
        case_code_mm: Package dimensions in millimeters
        series: Manufacturer's series name
        trustedparts_link: URL to component listing on Trustedparts
        temperature_coefficient: Temperature coefficient specification
        component_type: Component type (default: 'Resistor')

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
    component_type: str

    @classmethod
    def format_value(cls, resistance: float) -> str:
        """Convert a resistance value to a human-readable string format.

        Args:
            resistance: Resistance value in ohms

        Returns:
            A human-readable string representation of the resistance value

        """

        def clean_number(num: float) -> str:
            """Clean up number formatting for display.

            Args:
                num: The number to format

            Returns:
                A cleaned up string representation of the number

            """
            return f"{num:g}"

        if resistance < 1:
            return f"{clean_number(resistance * 1000)} mΩ"
        if resistance >= 1_000_000:  # noqa: PLR2004
            return f"{clean_number(resistance / 1_000_000)} MΩ"
        if resistance >= 1_000:  # noqa: PLR2004
            return f"{clean_number(resistance / 1_000)} kΩ"
        return f"{clean_number(resistance)} Ω"

    @classmethod
    def generate_resistance_code(  # noqa: PLR0911
        cls,
        resistance: float,
        specs: SeriesSpec,
    ) -> str:
        """Generate the resistance code portion of a Panasonic part number.

        Args:
            resistance: Resistance value in ohms
            specs: SeriesSpec instance containing series specifications

        Returns:
            The resistance code portion of the manufacturer's part number

        Raises:
            ValueError: If the resistance value is out of range

        """
        # Unpack resistance range
        min_resistance, max_resistance = specs.resistance_range

        # Check resistance range first
        if resistance < min_resistance or resistance > max_resistance:
            msg = (
                f"Resistance value out of range "
                f"({min_resistance}Ω to {max_resistance}Ω)"
            )
            raise ValueError(msg)

        # Special handling for Yageo manufacturer
        if specs.manufacturer == "Yageo":
            return cls._generate_yageo_resistance_code(resistance)

        if specs.manufacturer == "Murata":
            return cls._generate_murata_resistance_code(resistance)

        if specs.manufacturer == "Bourns":
            if specs.mpn_prefix.startswith(("CRM", "CRF")):
                return cls._generate_bourns_cr_resistance_code(resistance)
            return cls._generate_bourns_resistance_code(resistance)

        if specs.manufacturer == "Vishay":
            if specs.mpn_prefix == "NTCS0805E3":
                return cls._generate_vishay_thermistor_code(resistance)
            return cls._generate_vishay_resistance_code(resistance)

        if specs.manufacturer == "SEI Stackpole":
            if specs.mpn_prefix == "RNCF0603TKY":
                return cls._generate_sei_stackpole_rncf_resistance_code(
                    resistance
                )
            return cls._generate_sei_stackpole_resistance_code(resistance)

        if specs.manufacturer == "ROHM Semiconductor":
            return cls._generate_rohm_semiconductor_resistance_code(
                resistance,
            )

        if specs.manufacturer == "Susumu":
            return cls._generate_susumu_resistance_code(resistance)

        # Special handling for specific ERJ series
        if specs.mpn_prefix in (
            "ERJ-2GEJ",
            "ERJ-2GE0",
            "ERJ-3GEY0",
            "ERJ-6GEY0",
            "ERJ-3GEYJ",
            "ERJ-6GEYJ",
            "ERJ-6DQJ",
            "ERJ-6DQF",
        ):
            return cls._generate_erj_special_series_code(resistance)

        # Special handling for specific ERA series
        if specs.mpn_prefix in ("ERA-2AEB"):
            return cls._generate_era_special_series_code(resistance)

        # Special handling for specific ERA series
        if specs.mpn_prefix in ("ERJ-B2CF", "ERJ-B2BF"):
            return cls._generate_erj_bxcf_special_series_code(resistance)

        # Standard Panasonic/generic resistance code generation
        return cls._generate_standard_resistance_code(resistance)

    @classmethod
    def _generate_yageo_resistance_code(cls, resistance: float) -> str:
        """Generate resistance code for Yageo series.

        Yageo uses a different resistance code format compared to Panasonic.
        This method generates the resistance code for Yageo series resistors.

        Args:
            resistance: Resistance value in ohms

        Returns:
            The resistance code portion of the manufacturer's part number

        """
        if resistance < 1000:  # noqa: PLR2004
            whole = int(resistance)
            decimal = f"{((resistance - whole) * 100):02.0f}".rstrip("0")
            return f"{whole:01d}R{decimal}"

        if resistance < 1_000_000:  # noqa: PLR2004
            whole = int(resistance / 1000)
            decimal = f"{(resistance % 1000) / 10:02.0f}".rstrip("0")
            return f"{whole}K{decimal}"

        whole = int(resistance / 1000000)
        decimal = f"{((resistance % 1000000) / 10000):02.0f}".rstrip("0")
        return f"{whole}M{decimal}"

    @classmethod
    def _generate_murata_resistance_code(cls, resistance: float) -> str:
        """Generate resistance code for Murata series.

        Args:
            resistance: Resistance value in ohms

        """
        power = int(math.log10(resistance)) - 1
        significant = int(resistance / (10**power))
        return f"{significant}{power}"

    @classmethod
    def _generate_bourns_resistance_code(cls, resistance: float) -> str:
        """Generate resistance code for Murata series.

        Args:
            resistance: Resistance value in ohms

        """
        power = int(math.log10(resistance)) - 1
        significant = int(resistance / (10**power))
        return f"{significant}{power}"

    @classmethod
    def _generate_bourns_cr_resistance_code(cls, resistance: float) -> str:
        """Generate resistance code for Bourns CRM series."""
        if resistance < 1:
            decimal_str = f"{resistance:.3f}".split(".")[1]
            return f"R{decimal_str}"
        elif resistance < 10:
            integer_part = int(resistance)
            decimal_fraction = resistance - integer_part
            decimal_str = f"{int(round(decimal_fraction * 100)):02d}"
            return f"{integer_part}R{decimal_str}"
        elif resistance < 100:
            integer_part = int(resistance)
            decimal_fraction = resistance - integer_part
            decimal_str = f"{int(round(decimal_fraction * 10))}"
            return f"{integer_part}R{decimal_str}"
        else:
            if resistance.is_integer():
                return f"{int(resistance)}0"
            else:
                return f"{str(resistance).replace('.', '')}"

    @classmethod
    def _generate_vishay_resistance_code(cls, resistance: float) -> str:
        """Generate resistance code for Murata series.

        Args:
            resistance: Resistance value in ohms

        """
        if resistance < 0.01:  # noqa: PLR2004
            whole = int(resistance * 1000)
            decimal = round((resistance * 1000 - whole) * 100)
            return f"{whole}L{decimal:03d}"

        if resistance < 0.1:  # noqa: PLR2004
            whole = int(resistance * 10000)
            return f"R0{whole}"

        if resistance < 10:  # noqa: PLR2004
            whole = int(resistance)
            decimal = round((resistance - whole) * 100)
            return f"{whole}R{decimal:02d}"

        if resistance < 100:  # noqa: PLR2004
            whole = int(resistance)
            decimal = round((resistance - whole) * 10)
            return f"{whole}R{decimal}"

        if resistance < 1_000:  # noqa: PLR2004
            whole = int(resistance)
            return f"{whole}R"

        if resistance < 10_000:  # noqa: PLR2004
            k_value = resistance / 1000
            whole = int(k_value)
            decimal = round((k_value - whole) * 100)
            return f"{whole}K{decimal:02d}"

        if resistance < 100_000:  # noqa: PLR2004
            k_value = resistance / 1000
            whole = int(k_value)
            decimal = round((k_value - whole) * 10)
            return f"{whole}K{decimal}"

        if resistance < 1_000_000:  # noqa: PLR2004
            whole = int(resistance / 1000)
            return f"{whole}K"

        if resistance < 10_000_000:  # noqa: PLR2004
            m_value = resistance / 1_000_000
            whole = int(m_value)
            decimal = round((m_value - whole) * 100)
            return f"{whole}M{decimal:02d}"

        m_value = resistance / 1_000_000
        whole = int(m_value)
        decimal = round((m_value - whole) * 100)
        return f"{whole}M{decimal}"

    @classmethod
    def _generate_vishay_thermistor_code(cls, resistance: float) -> str:
        """Generate resistance code for Vishay thermistor series.

        Args:
            resistance: Resistance value in ohms

        """
        resistance_int = int(resistance)

        multiplier = 0
        temp_value = resistance_int

        while temp_value % 10 == 0 and temp_value // 10 >= 10:
            temp_value //= 10
            multiplier += 1

        significant_digits = temp_value

        return f"{significant_digits}{multiplier}"

    @classmethod
    def _generate_sei_stackpole_resistance_code(
        cls,
        resistance: float,
    ) -> str:
        """Generate resistance code for SEI Stackpole series.

        SEI Stackpole uses a different resistance code format.
        This method generates the resistance code for SEI Stackpole series
        resistors.

        Args:
            resistance: Resistance value in ohms

        Returns:
            The resistance code portion of the manufacturer's part number

        """
        if resistance < 1000:  # noqa: PLR2004
            whole = int(resistance)
            decimal = f"{((resistance - whole) * 100):02.0f}".rstrip("0")
            return f"{whole:01d}R{decimal}"

        if resistance < 1_000:  # noqa: PLR2004
            whole = int(resistance / 1000)
            decimal = f"{(resistance % 1000) / 10:02.0f}"
            return f"{whole}K{decimal}"

        if resistance < 100_000:  # noqa: PLR2004
            whole = int(resistance / 1000)
            decimal = f"{(resistance % 1000) / 10:01.0f}"
            return f"{whole}K{decimal}"

        if resistance < 1_000_000:  # noqa: PLR2004
            whole = int(resistance / 1000)
            decimal = f"{(resistance % 1000) / 10:02.0f}".rstrip("0")
            return f"{whole}K{decimal}"

        whole = int(resistance / 1000000)
        decimal = f"{((resistance % 1000000) / 10000):02.0f}"
        return f"{whole}M{decimal}"

    @classmethod
    def _generate_sei_stackpole_rncf_resistance_code(
        cls,
        resistance: float,
    ) -> str:
        """Generate resistance code for SEI Stackpole series.

        SEI Stackpole uses a different resistance code format.
        This method generates the resistance code for SEI Stackpole series
        resistors.

        Args:
            resistance: Resistance value in ohms

        Returns:
            The resistance code portion of the manufacturer's part number

        """
        if resistance < 100:
            whole = int(resistance)
            decimal = int(round((resistance - whole) * 10))
            return f"{whole:01d}R{decimal}"

        if resistance < 1000:  # noqa: PLR2004
            whole = int(resistance)
            decimal = f"{((resistance - whole) * 100):02.0f}".rstrip("0")
            return f"{whole:01d}R{decimal}"

        if resistance < 1_000:  # noqa: PLR2004
            whole = int(resistance / 1000)
            decimal = f"{(resistance % 1000) / 10:02.0f}"
            return f"{whole}K{decimal}"

        if resistance < 10_000:
            whole = int(resistance / 1000)
            decimal = int((resistance % 1000) / 10)
            print(f"{whole}K{decimal:02d}")
            return f"{whole}K{decimal:02d}"

        if resistance < 100_000:  # noqa: PLR2004
            whole = int(resistance / 1000)
            decimal = f"{(resistance % 1000) / 10:01.0f}"
            return f"{whole}K{decimal}"

        if resistance < 1_000_000:  # noqa: PLR2004
            whole = int(resistance / 1000)
            decimal = f"{(resistance % 1000) / 10:02.0f}".rstrip("0")
            return f"{whole}K{decimal}"

        whole = int(resistance / 1000000)
        decimal = f"{((resistance % 1000000) / 10000):02.0f}"
        return f"{whole}M{decimal}"

    @classmethod
    def _generate_rohm_semiconductor_resistance_code(
        cls,
        resistance: float,
    ) -> str:
        """Generate resistance code for ROHM Semiconductor series.

        Args:
            resistance: Resistance value in ohms

        Returns:
            The resistance code portion of the manufacturer's part number

        """
        if resistance < 0.01:  # noqa: PLR2004
            whole = int(resistance * 1_000)
            decimal = f"{((resistance % 1000000) / 10000):02.0f}"
            return f"{whole}L{decimal}"

        if resistance < 0.1:  # noqa: PLR2004
            whole = int(resistance * 1_000)
            decimal = f"{((resistance % 1000000) / 10000):01.0f}"
            return f"{whole}L{decimal}"

        return f"{resistance}"

    @classmethod
    def _generate_susumu_resistance_code(
        cls,
        resistance: float,
    ) -> str:
        """Generate resistance code for Susumu series.

        Args:
            resistance: Resistance value in ohms

        Returns:
            The resistance code portion of the manufacturer's part number

        """
        if resistance < 0.01:
            return f"R00{int(resistance * 1_000)}"

        if resistance < 0.1:
            return f"R0{int(resistance * 1_000)}"

        if resistance < 1:
            return f"R{int(resistance * 1_000)}"

        return f"{resistance}"

    @classmethod
    def _generate_erj_special_series_code(cls, resistance: float) -> str:
        """Generate resistance code for special ERJ series.

        Special handling for ERJ series with unique resistance code format.

        Args:
            resistance: Resistance value in ohms

        Returns:
            The resistance code portion of the manufacturer's part number

        """
        if resistance == 0:
            return "R00"

        if resistance < 1:  # < 10Ω
            whole = int(resistance)
            decimal = round((resistance - whole) * 100)
            return f"R{decimal}"

        if resistance < 10:  # < 10Ω  # noqa: PLR2004
            whole = int(resistance)
            decimal = round((resistance - whole) * 10)
            return f"{whole:01d}R{decimal}"

        if resistance < 100:  # 10-99Ω  # noqa: PLR2004
            whole = int(resistance)
            decimal = round((resistance - whole) * 10)
            return f"{whole:01d}{decimal}"

        # Determine multiplier and significant digits for values ≥ 100Ω
        if resistance < 1000:  # 100-999Ω  # noqa: PLR2004
            significant = round(resistance / 10)
            multiplier = "1"
        elif resistance < 10000:  # 1k-9.99kΩ  # noqa: PLR2004
            significant = round(resistance / 100)
            multiplier = "2"
        elif resistance < 100000:  # 10k-99.9kΩ  # noqa: PLR2004
            significant = round(resistance / 1000)
            multiplier = "3"
        elif resistance < 1000000:  # 100k-999kΩ  # noqa: PLR2004
            significant = round(resistance / 10000)
            multiplier = "4"
        else:  # 1MΩ+
            significant = round(resistance / 100000)
            multiplier = "5"

        return f"{significant:02d}{multiplier}"

    @classmethod
    def _generate_era_special_series_code(cls, resistance: float) -> str:
        """Generate resistance code for ERA series.

        Special handling for ERA series with unique resistance code format.

        Args:
            resistance: Resistance value in ohms

        Returns:
            The resistance code portion of the manufacturer's part number

        """
        if resistance < 100:  # noqa: PLR2004
            whole = int(resistance)
            decimal = round((resistance - whole) * 10)
            return f"{whole:02d}{'R' if decimal else ''}{decimal}"

        ranges = [1e3, 1e4, 1e5, 1e6]
        for i, upper in enumerate(ranges):
            if resistance < upper:
                div = 10**i
                significant = round(resistance / div)
                multiplier = str(i)
                if str(resistance)[2] == "0":
                    significant = round(resistance / (div * 10))
                    multiplier = str(i + 1)
                return f"{significant:02d}{multiplier}"

        # 1MΩ+ case
        significant = round(resistance / 1e4)
        multiplier = "4"
        if str(resistance)[2] == "0":
            significant = round(resistance / 1e5)
            multiplier = "5"
        return f"{significant:02d}{multiplier}"

    @classmethod
    def _generate_erj_bxcf_special_series_code(cls, resistance: float) -> str:
        """Generate resistance code for ERA series.

        Special handling for ERA series with unique resistance code format.

        Args:
            resistance: Resistance value in ohms

        Returns:
            The resistance code portion of the manufacturer's part number

        """
        if resistance < 0.1:
            result = int(str(resistance).replace(".", ""))
            return f"R0{result}"
        if resistance < 1:
            result = int(resistance * 100)
            return f"R{result}"
        if resistance < 10:
            whole = int(resistance)
            decimal = round((resistance - whole) * 10)
            return f"{whole}R{decimal}"

        return f"R{resistance}"

    @classmethod
    def _generate_standard_resistance_code(cls, resistance: float) -> str:
        """Generate resistance code for standard Panasonic series.

        Generate the resistance code for standard Panasonic series resistors.

        Args:
            resistance: Resistance value in ohms

        Returns:
            The resistance code portion of the manufacturer's part number

        """
        # Handle values less than 100Ω using R notation
        if resistance < 100:  # noqa: PLR2004
            whole = int(resistance)
            decimal = round((resistance - whole) * 10)
            return f"{whole:02d}R{decimal}"

        # For values ≥ 100Ω, determine multiplier and significant digits
        if resistance < 1000:  # 100-999Ω  # noqa: PLR2004
            significant = round(resistance)
            multiplier = "0"
        elif resistance < 10000:  # 1k-9.99kΩ  # noqa: PLR2004
            significant = round(resistance / 10)
            multiplier = "1"
        elif resistance < 100000:  # 10k-99.9kΩ  # noqa: PLR2004
            significant = round(resistance / 100)
            multiplier = "2"
        elif resistance < 1000000:  # 100k-999kΩ  # noqa: PLR2004
            significant = round(resistance / 1000)
            multiplier = "3"
        else:  # 1MΩ+
            significant = round(resistance / 10000)
            multiplier = "4"

        return f"{significant:03d}{multiplier}"

    @classmethod
    def create_part_info(
        cls,
        resistance: float,
        tolerance_value: str,
        packaging: str,
        specs: SeriesSpec,
    ) -> PartInfo:
        """Create a PartInfo instance for a specific resistor part.

        Generates a PartInfo instance with detailed information for a specific
        resistor part based on the given resistance value, tolerance,
        and specs.

        Args:
            resistance: Resistance value in ohms
            tolerance_value: Tolerance specification (e.g., '1%')
            packaging: Manufacturer's part number suffix
            specs: SeriesSpec instance containing series specifications

        Returns:
            PartInfo instance with detailed component information

        """
        resistance_code = cls.generate_resistance_code(resistance, specs)
        packaging_code = packaging
        mpn = f"{specs.mpn_prefix}{resistance_code}{packaging_code}"

        description = (
            f"RES SMD {cls.format_value(resistance)} "
            f"{tolerance_value} {specs.case_code_in} {specs.voltage_rating}"
        )
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
            component_type=specs.component_type,
        )

    @classmethod
    def generate_part_numbers(
        cls,
        specs: SeriesSpec,
    ) -> list[PartInfo]:
        """Generate a list of PartInfo instances for a resistor series.

        Generates a list of PartInfo instances for a specific resistor series
        based on the given series specifications.

        Args:
            specs: SeriesSpec instance containing series specifications

        Returns:
            List of PartInfo instances for the specified resistor series

        """
        parts = []

        # Generate standard series parts
        for series_type in specs.tolerance_map:
            # Determine base values based on series type
            base_values = (
                E96_BASE_VALUES if series_type == "E96" else E24_BASE_VALUES
            )

            # Get tolerance value for this series
            tolerance_value = specs.tolerance_map[series_type]

            # Generate filtered values
            filtered_values = cls._filtered_resistance_values(
                base_values,
                specs.resistance_range,
                specs.excluded_values,
                specs.specified_values,
            )

            # Create parts for each valid resistance value
            for resistance in filtered_values:
                part = cls.create_part_info(
                    resistance=resistance,
                    tolerance_value=tolerance_value,
                    packaging=specs.mpn_sufix,
                    specs=specs,
                )
                parts.append(part)

        # Handle extra non-standard values if provided
        if specs.extra_values:
            min_resistance, max_resistance = specs.resistance_range

            # Determine tolerance to use for extra values
            extra_tolerance = (
                specs.tolerance_map.get("E96")  # Prefer E96 tolerance
                or next(iter(specs.tolerance_map.values()))  # Fallback
            )

            # Process each extra value
            for resistance in specs.extra_values:
                # Check if value is within valid range
                if min_resistance <= resistance <= max_resistance:
                    part = cls.create_part_info(
                        resistance=resistance,
                        tolerance_value=extra_tolerance,
                        packaging=specs.mpn_sufix,
                        specs=specs,
                    )
                    parts.append(part)

        return parts

    @classmethod
    def _filtered_resistance_values(
        cls,
        base_values: list[float],
        resistance_range: list[int | float],
        excluded_values: list[float] | None = None,
        specified_values: list[float] | None = None,
    ) -> Iterator[float]:
        """Generate filtered resistance values based on specified conditions.

        Generates a filtered list of resistance values based on the given
        base values, resistance range, and optional exclusion/specification
        conditions.

        Args:
            base_values: List of base resistance values for the series
            resistance_range: Minimum and maximum resistance values
            excluded_values: Optional list of excluded resistance values
            specified_values: Optional list of specified resistance values

        Yields:
            Filtered resistance values based on the specified conditions

        """
        min_resistance, max_resistance = resistance_range
        multipliers = [
            *[0.0001, 0.001, 0.01, 0.1, 0, 1],
            *[10, 100, 1000, 10000, 100000, 1000000],
        ]

        for base_value in base_values:
            for multiplier in multipliers:
                resistance = round(base_value * multiplier, 3)

                # Check if resistance is within range
                is_within_range = (
                    min_resistance <= resistance <= max_resistance
                )

                # Check exclusion conditions
                is_not_excluded = (
                    excluded_values is None
                    or resistance not in excluded_values
                )

                # Check specified values condition
                is_specified = (
                    specified_values is None or resistance in specified_values
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
            "RDA0000/AOA0000C304.pdf"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "ERA-2AEB": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERA-2AEB",
        mpn_sufix="X",
        footprint="resistor_footprints:R_0402_1005Metric",
        voltage_rating="50V",
        case_code_in="0402",
        case_code_mm="1005",
        power_rating="0.1W",
        temperature_coefficient="25 ppm/°C",
        resistance_range=[47, 100_000],
        tolerance_map={"E96": "0.1%", "E24": "0.1%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDM0000/AOA0000C307.pdf"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
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
            "RDA0000/AOA0000C304.pdf"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
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
            "RDA0000/AOA0000C304.pdf"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "ERJ-6DQF": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-6DQF",
        mpn_sufix="V",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        temperature_coefficient="100 ppm/°C",
        resistance_range=[0.1, 9.1],
        specified_values=[
            *[0.22, 0.24, 0.27, 0.3, 0.33, 0.36, 0.39, 0.43, 0.47, 0.51],
            *[0.56, 0.62, 0.68, 0.75, 0.82, 0.91, 1, 1.1, 1.2, 1.3, 1.5],
            *[1.6, 1.8, 2, 2.2, 2.4, 2.7, 3, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1],
            *[5.6, 6.2, 6.8, 7.5, 8.2, 9.1],
        ],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/RDN0000/"
            "AOA0000C313.pdf"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
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
            "RDO0000/AOA0000C331.pdf"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
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
            "RDO0000/AOA0000C331.pdf"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
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
            "RDO0000/AOA0000C331.pdf"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
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
            "RDA0000/AOA0000C301.pdf"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "ERJ-2GE0": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-2GE0",
        mpn_sufix="X",
        footprint="resistor_footprints:R_0402_1005Metric",
        voltage_rating="50V",
        case_code_in="0402",
        case_code_mm="1005",
        power_rating="0.1W",
        temperature_coefficient="200 ppm/°C",
        resistance_range=[0, 1],
        specified_values=[0],
        tolerance_map={"E24": "5%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C301.pdf"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "ERJ-3GEY0": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-3GEY0",
        mpn_sufix="V",
        footprint="resistor_footprints:R_0603_1608Metric",
        voltage_rating="75V",
        case_code_in="0603",
        case_code_mm="1608",
        power_rating="0.1W",
        temperature_coefficient="200 ppm/°C",
        resistance_range=[0, 1],
        specified_values=[0],
        tolerance_map={"E24": "5%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C301.pdf"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "ERJ-6GEY0": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-6GEY0",
        mpn_sufix="V",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        temperature_coefficient="200 ppm/°C",
        resistance_range=[0, 1],
        specified_values=[0],
        tolerance_map={"E24": "5%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C301.pdf"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
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
            "RDA0000/AOA0000C301.pdf"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
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
            "RDA0000/AOA0000C301.pdf"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "ERJ-6DQJ": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-6DQJ",
        mpn_sufix="V",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        temperature_coefficient="100 ppm/°C",
        resistance_range=[0.22, 9.1],
        tolerance_map={"E24": "5%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDN0000/AOA0000C313.pdf"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "ERJ-B2CF": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-B2CF",
        mpn_sufix="V",
        footprint="resistor_footprints:R_0612_1632Metric",
        voltage_rating="",
        case_code_in="0612",
        case_code_mm="1632",
        power_rating="1W",
        temperature_coefficient="",
        resistance_range=[0.01, 0.2],
        specified_values=[
            *[0.01, 0.013, 0.015, 0.016, 0.018, 0.02, 0.022, 0.024, 0.027],
            *[0.03, 0.033, 0.036, 0.047, 0.051, 0.056, 0.068, 0.075, 0.082],
            *[0.1, 0.11, 0.12, 0.13, 0.15, 0.16, 0.18, 0.2],
        ],
        extra_values=[0.05],
        tolerance_map={"E24": "1%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/RDN0000/"
            "AOA0000C325.pdf"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "ERJ-B2BF": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-B2BF",
        mpn_sufix="V",
        footprint="resistor_footprints:R_0612_1632Metric",
        voltage_rating="",
        case_code_in="0612",
        case_code_mm="1632",
        power_rating="1W",
        temperature_coefficient="",
        resistance_range=[0.22, 9.1],
        specified_values=[
            *[0.22, 0.24, 0.33, 0.39, 0.51, 0.62, 0.68, 0.75, 0.82, 0.91],
            *[1, 1.1, 1.2, 1.3, 1.5, 1.8, 2, 2.2, 2.4, 2.7, 3, 3.3, 3.6],
            *[4.3, 4.7, 5.1, 6.2, 6.8, 7.5, 8.2, 9.1],
        ],
        tolerance_map={"E24": "1%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/RDN0000/"
            "AOA0000C325.pdf"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
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
        specified_values=[
            *[41.2, 205, 806, 1000, 1050, 1800, 2000, 3000, 4020, 6800],
            *[8060, 10000, 11000, 12100, 15000, 20000, 22000, 27000, 49900],
        ],
        tolerance_map={"E96": "0.1%", "E24": "0.1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
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
            *[806000, 820000, 825000, 845000, 866000, 887000, 909000],
            *[910000, 931000, 953000, 976000],
        ],
        extra_values=[37, 50, 1720, 1930, 6890, 22900],
        tolerance_map={"E96": "0.1%", "E24": "0.1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
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
            *[806000, 820000, 825000, 845000, 866000, 887000, 909000],
            *[910000, 931000, 953000, 976000, 1000000],
        ],
        extra_values=[49200, 706000],
        tolerance_map={"E96": "0.1%", "E24": "0.1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
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
        extra_values=[
            *[13.5, 25, 29.8, 39.7, 43.7, 44.8, 49.3, 50.5, 59.7, 92],
            *[109, 167, 246, 248, 320, 328, 388, 505, 690, 723],
            *[835, 1290, 1450, 1520, 1760, 1890, 1980, 2180, 2230, 2340],
            *[2640, 3050, 3120, 3200, 3790, 4480, 4810, 5050, 5200, 5420],
            *[6260, 6730, 6890, 7230, 8160, 8560, 8980, 9200, 9420, 10100],
            *[10400, 10900, 11100, 11700, 12300, 14500, 14900, 17200, 20300],
            *[21300, 21800, 27100, 27700, 30500, 31200, 32000, 33600, 36100],
            *[37900, 38800, 39700, 40700, 41700, 42700, 43700, 44800, 45900],
            *[48100, 49300, 51700, 58300, 62600, 75900, 79600, 81600, 85600],
            *[87600, 89800, 92000, 101000, 109000, 111000, 135000, 142000],
            *[145000, 164000, 172000, 176000, 203000, 223000, 252000, 271000],
            *[277000, 305000, 352000, 397000, 459000, 723000, 942000],
            *[1170000, 1490000],
        ],
        tolerance_map={"E96": "0.1%", "E24": "0.1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
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
        excluded_values=[3.9],
        extra_values=[
            *[61.2, 96.5, 448, 1350, 3280, 3610, 7770, 9000, 10010, 10100],
            *[20300, 21300, 21800, 30500, 92000, 101000, 126000],
        ],
        tolerance_map={"E96": "0.1%", "E24": "0.1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
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
        specified_values=[
            *[6.8, 8.2, 18, 24.9, 36, 60.4, 75, 100, 110, 124, 200, 374],
            *[402, 510, 680, 909, 1000, 1200, 1270, 1500, 1800, 2320, 2430],
            *[2490, 2700, 3000, 3010, 3160, 3300, 3570, 4020, 4700, 4990],
            *[5100, 5490, 5620, 6190, 9100, 10000, 11000, 11500, 12000],
            *[13000, 15000, 17400, 20000, 20500, 21500, 22100, 23200, 24000],
            *[24900, 25500, 26100, 26700, 33000, 33200, 40200, 45300, 46400],
            *[47000, 49900, 51000, 60400, 62000, 66500, 68000, 68100, 73200],
            *[91000, 100000, 158000, 160000, 205000, 249000, 330000, 360000],
            *[390000, 470000, 604000, 698000, 910000, 931000, 976000],
            *[1000000],
        ],
        extra_values=[900, 1890, 4580, 5050, 11100, 22300, 417000],
        tolerance_map={"E96": "0.25%", "E24": "0.25%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
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
        extra_values=[
            *[30.5, 176, 234, 305, 597, 741, 759, 777, 796, 816, 835, 876],
            *[920, 942, 965, 988, 1010, 2230, 5050, 7060, 11100, 14500],
            *[15600, 17600, 20300, 21300, 27100, 44800, 101000, 417000],
        ],
        excluded_values=[
            *[1.02, 1.05, 1.07, 1.1, 1.13, 1.15, 1.18, 1.2, 1.21, 1.24, 1.27],
            *[1.3, 1.33, 1.37, 1.4, 1.43, 1.47, 1.5, 1.54, 1.58, 1.6, 1.62],
            *[1.65, 1.69, 1.74, 1.78, 1.8, 1.82, 1.87, 1.91, 1.96, 2.26],
            *[2.32, 2.37, 2.4, 2.49, 2.55, 2.61, 2.67, 2.7, 2.74, 2.8, 2.87],
            *[2.94, 3.09, 3.16, 3.24, 3.3, 3.32, 3.4, 3.48, 3.57, 3.6, 3.65],
            *[3.74, 3.83, 3.92, 4.12, 4.22, 4.3, 4.32, 4.42, 4.53, 4.64],
            *[4.75, 4.87, 5.11, 5.23, 5.36, 5.49, 5.62, 5.76, 5.9, 6.19],
            *[6.34, 6.49, 6.65, 6.98, 7.15, 7.32, 7.68, 7.87, 8.25, 8.45],
            *[8.66, 8.87, 9.09, 9.31, 9.53, 9.76, 10.2, 10.7, 11.3, 11.5],
            *[11.8, 12.7, 13.3, 13.7, 14.7, 15.4, 15.8, 16.5, 17.8, 18.7],
            *[20.5, 21, 23.7, 24.3, 25.5, 26.7, 28, 30.9, 31.6, 35.7],
            *[41.2, 43.2, 44.2, 46.4, 53.6, 59, 71.5, 73.2, 76.8, 84.5],
            *[88.7, 95.3, 97.6, 105, 107, 137, 215, 226, 316, 365, 392],
            *[536, 820, 910, 1180, 1650, 1870, 5760, 11300, 14700],
            *[37400, 53600, 60400, 118000, 124000, 160000, 210000],
            *[261000, 309000, 357000, 412000, 422000, 442000, 536000],
            *[549000, 562000, 620000, 698000, 715000, 732000, 768000],
            *[787000, 845000, 976000, 1020000, 1050000, 1070000],
            *[1100000, 1150000, 1180000, 1200000, 1210000, 1240000],
            *[1270000, 1300000, 1330000, 1370000, 1400000, 1430000],
            *[1470000],
        ],
        tolerance_map={"E96": "0.5%", "E24": "0.5%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
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
        extra_values=[706, 246000],
        excluded_values=[
            *[1.02, 1.05, 1.07, 1.1, 1.13, 1.15, 1.18, 1.21, 1.24, 1.27],
            *[1.3, 1.33, 1.37, 1.47, 1.54, 1.58, 1.62, 1.69, 1.74, 1.78],
            *[1.82, 1.87, 1.91, 1.96, 2.05, 2.1, 2.15, 2.21, 2.26, 2.32],
            *[2.37, 2.43, 2.55, 2.61, 2.67, 2.8, 2.87, 2.94, 3.01, 3.09],
            *[3.16, 3.24, 3.4, 3.57, 3.65, 3.74, 3.83, 3.92, 4.02, 4.3],
            *[4.32, 4.42, 4.53, 4.64, 4.87, 5.11, 5.49, 5.76, 5.9, 6.19],
            *[6.34, 6.65, 6.81, 7.15, 7.32, 7.68, 7.87, 8.45, 8.66, 8.87],
            *[9.31, 9.53, 9.76, 10.2, 10.7, 11.8, 12.4, 12.7, 13.3, 13.7],
            *[14, 16.5, 16.9, 17.8, 18.7, 19.1, 19.6, 23.2, 23.7, 26.1],
            *[27.4, 28.7, 29.4, 30.9, 32.4, 34, 38.3, 41.2, 42.2, 43.2],
            *[44.2, 52.3, 57.6, 59, 63.4, 66.5, 73.2, 84.5, 86.6, 107],
            *[127, 143, 165, 169, 210, 309, 412, 3240, 5360, 63400],
            *[324000, 634000, 649000, 732000, 768000, 806000, 845000, 866000],
            *[887000, 976000, 1020000, 1050000, 1070000, 1130000, 1150000],
            *[1180000, 1240000, 1270000, 1300000, 1330000, 1370000, 1400000],
            *[1430000, 1470000],
        ],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
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
        specified_values=[
            *[1, 1.5, 2, 2.2, 2.43, 3, 3.3, 3.6, 3.9, 4.02],
            *[4.7, 4.75, 5.1, 6.2, 6.65, 6.8, 7.5, 8.2, 10, 11],
            *[12, 15, 16.9, 18, 20, 22, 24.9, 27, 30, 33],
            *[36, 39, 47, 47.5, 49.9, 51, 51.1, 62, 68, 75],
            *[91, 100, 120, 150, 158, 200, 205, 210, 220, 221],
            *[240, 249, 270, 300, 301, 330, 390, 470, 475, 499],
            *[510, 511, 560, 562, 634, 665, 680, 750, 787, 820],
            *[825, 887, 910, 1000, 1200, 1210, 1300, 1500, 1600, 1800],
            *[1910, 2000, 2200, 2490, 2700, 3000, 3010, 3300, 3320, 3400],
            *[3900, 4020, 4300, 4420, 4700, 4990, 5100, 5600, 6800, 7500],
            *[8200, 9100, 10000, 10500, 11000, 12000, 12100, 15000],
            *[15800, 16000, 16200, 18000, 20000, 20500, 22000, 22100],
            *[24000, 24300, 24900, 26100, 27000, 27400, 28000, 28700],
            *[29400, 30000, 30100, 30900, 33000, 36000, 36500, 39000],
            *[39200, 47000, 49900, 51000, 56000, 62000, 68000, 68100],
            *[75000, 80600, 82500, 100000, 120000, 121000, 140000],
            *[147000, 150000, 180000, 182000, 200000, 220000, 237000],
            *[270000, 300000, 324000, 330000, 430000, 470000, 475000],
            *[499000, 560000, 590000, 604000, 634000, 680000, 750000],
            *[820000, 953000, 1000000],
        ],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
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
        extra_values=[3880, 5000, 1110000],
        excluded_values=[
            *[1.02, 1.05, 1.07, 1.13, 1.15, 1.18, 1.21, 1.24, 1.27, 1.33],
            *[1.37, 1.4, 1.43, 1.47, 1.54, 1.58, 1.62, 1.65, 1.69, 1.74],
            *[1.78, 1.82, 1.87, 1.91, 2.05, 2.1, 2.21, 2.26, 2.32, 2.37],
            *[2.43, 2.55, 2.61, 2.67, 2.74, 2.8, 2.87, 3.01, 3.09, 3.16],
            *[3.24, 3.32, 3.4, 3.48, 3.57, 3.65, 3.74, 3.83, 3.92, 4.02],
            *[4.22, 4.32, 4.42, 4.53, 4.64, 4.75, 4.87, 4.99, 5.11, 5.23],
            *[5.36, 5.49, 5.62, 5.76, 5.9, 6.19, 6.34, 6.49, 6.65, 6.98],
            *[7.15, 7.68, 7.87, 8.66, 8.87, 9.09, 9.31, 9.53, 9.76, 10.2],
            *[10.5, 10.7, 11.3, 11.5, 11.8, 12.4, 12.7, 13.3, 13.7, 14.3],
            *[15.8, 16.5, 17.4, 17.8, 18.7, 19.6, 20.5, 26.1, 28, 29.4],
            *[43.2, 102, 107, 115, 127, 137, 143, 169, 237, 280, 309],
            *[357, 412, 453, 523, 549, 649, 698, 787, 866, 887, 976],
            *[3570, 5490, 5760, 5900, 6980, 9760, 11300, 28700, 45300],
            *[52300, 76800, 78700, 158000, 196000, 267000, 294000],
            *[412000, 487000, 523000, 698000, 715000, 732000, 768000],
            *[1020000, 1050000, 1070000, 1130000, 1150000, 1180000],
            *[1240000, 1270000, 1330000, 1370000, 1400000, 1430000],
            *[1470000],
        ],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
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
        resistance_range=[4.7, 1_000_000],
        extra_values=[42, 54],
        specified_values=[
            *[7.5, 10, 15, 20, 24.9, 27, 33.2, 42, 54, 73.2, 100],
            *[105, 110, 137, 150, 158, 220, 240, 330, 470, 511, 909],
            *[1000, 1070, 1470, 1500, 2490, 3300, 3600, 3650, 3900],
            *[4700, 4990, 6650, 6800, 10000, 15800, 20500, 22100],
            *[30100, 33000, 36000, 39200, 52300, 68000, 120000],
            *[130000, 150000, 180000, 200000, 220000, 301000],
        ],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "RT2010FKE07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RT2010FKE07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_2010_5025Metric",
        voltage_rating="200V",
        case_code_in="2010",
        case_code_mm="5025",
        power_rating="0.5W",
        temperature_coefficient="50 ppm/°C",
        resistance_range=[4.7, 1_000_000],
        extra_values=[150000],
        specified_values=[
            *[6.04, 10, 13.7, 15, 18, 20, 24, 30, 33, 39, 39.2],
            *[40.2, 49.9, 56, 61.9, 64.9, 68, 73.2, 78.7, 100, 120],
            *[130, 180, 215, 348, 374, 470, 475, 487, 511, 820],
            *[1000, 1470, 1800, 2100, 2200, 4750, 5600, 5620, 6800],
            *[6810, 10000, 12000, 20000, 27000, 33000, 39000, 47000],
            *[49900, 68000, 100000, 200000, 220000, 330000, 383000],
            *[470000, 510000, 560000, 619000, 1000000],
        ],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "RT2512FKE07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RT2512FKE07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_2512_6332Metric",
        voltage_rating="200V",
        case_code_in="2512",
        case_code_mm="6332",
        power_rating="0.75W",
        temperature_coefficient="50 ppm/°C",
        resistance_range=[4.7, 1_000_000],
        specified_values=[
            *[8.2, 10, 12, 14, 15, 16.9, 18, 20, 21, 22, 24, 47, 100],
            *[150, 200, 220, 390, 511, 1000, 2000, 2200, 2400, 2700],
            *[4700, 5620, 10000, 12000, 22000, 27000, 51000, 100000],
            *[120000, 150000, 220000, 240000, 499000, 1000000],
        ],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "AA0805FR-07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="AA0805FR-07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        temperature_coefficient="25 ppm/°C",
        resistance_range=[1, 10_000_000],
        extra_values=[481, 2710, 4480],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "RC0402FR-7W": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RC0402FR-7W",
        mpn_sufix="L",
        footprint="resistor_footprints:R_0402_1005Metric",
        voltage_rating="50V",
        case_code_in="0402",
        case_code_mm="1005",
        power_rating="0.125W",
        temperature_coefficient="200 ppm/°C",
        resistance_range=[1, 10_000_000],
        specified_values=[
            *[1, 1.2, 1.5, 1.8, 2.2, 2.4, 2.7, 3.6, 4.7, 4.75, 5.6, 10],
            *[12, 12.1, 18, 20, 22, 23.2, 27, 29.4, 30.1, 33, 34, 36],
            *[37.4, 39, 43, 44.2, 45.3, 47, 49.9, 52.3, 56, 62, 71.5],
            *[75, 80.6, 82, 90.9, 95.3, 97.6, 100, 110, 120, 121, 127],
            *[130, 140, 143, 150, 162, 174, 180, 182, 187, 200, 210],
            *[220, 221, 240, 243, 270, 300, 301, 316, 330, 365, 390],
            *[392, 402, 422, 470, 475, 499, 510, 560, 604, 620, 649],
            *[665, 680, 750, 806, 820, 910, 1000, 1020, 1050, 1100],
            *[1180, 1200, 1210, 1240, 1300, 1400, 1500, 1600, 1690],
            *[1780, 1800, 1820, 1870, 1910, 2000, 2100, 2200, 2210],
            *[2400, 2490, 2700, 3000, 3090, 3300, 3480, 3570, 3600],
            *[3650, 3830, 3900, 4020, 4120, 4300, 4320, 4530, 4700],
            *[4750, 4990, 5100, 5600, 5620, 5760, 5900, 6040, 6190],
            *[6200, 6340, 6490, 6800, 7320, 7500, 7870, 8060, 8200],
            *[8660, 9090, 9100, 9310, 10000, 10200, 10700, 11800],
            *[12000, 12100, 12700, 13000, 14700, 15000, 15800, 16000],
            *[18000, 20000, 21000, 21500, 22000, 22100, 24000, 24300],
            *[24900, 25500, 26100, 27000, 27400, 28000, 29400, 30100],
            *[33000, 33200, 34000, 36000, 36500, 38300, 39000, 39200],
            *[40200, 41200, 42200, 46400, 47000, 47500, 49900, 51000],
            *[51100, 53600, 56000, 56200, 57600, 59000, 60400, 61900],
            *[62000, 64900, 68000, 68100, 69800, 71500, 75000, 76800],
            *[82000, 86600, 91000, 93100, 97600, 100000, 110000],
            *[115000, 120000, 130000, 133000, 137000, 140000, 143000],
            *[150000, 154000, 169000, 180000, 187000, 196000, 200000],
            *[220000, 232000, 237000, 240000, 249000, 270000, 294000],
            *[300000, 316000, 324000, 330000, 360000, 365000, 432000],
            *[442000, 470000, 475000, 510000, 536000, 560000, 590000],
            *[680000, 750000, 820000, 845000, 866000, 910000],
            *[1000000, 1100000, 1200000, 1300000],
        ],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "RC0402FR-07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RC0402FR-07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_0402_1005Metric",
        voltage_rating="50V",
        case_code_in="0402",
        case_code_mm="1005",
        power_rating="0.063W",
        temperature_coefficient="200 ppm/°C",
        resistance_range=[1, 10_000_000],
        extra_values=[2710, 35000],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "RC0603FR-07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RC0603FR-07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_0603_1608Metric",
        voltage_rating="75V",
        case_code_in="0603",
        case_code_mm="1608",
        power_rating="0.125W",
        temperature_coefficient="200 ppm/°C",
        resistance_range=[1, 10_000_000],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "RC0805BR-07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RC0805BR-07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        temperature_coefficient="200 ppm/°C",
        resistance_range=[1, 10_000_000],
        specified_values=[
            *[10, 47, 100, 499, 698, 820, 1000, 1200, 1500, 2100, 6980],
            *[10000, 10500, 15000, 16900, 20000, 33000, 52300, 75000, 84500],
            *[100000, 140000, 240000, 390000, 750000, 806000, 1000000],
        ],
        tolerance_map={"E96": "0.1%", "E24": "0.1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "RC0805FR-07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RC0805FR-07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        temperature_coefficient="200 ppm/°C",
        resistance_range=[1, 10_000_000],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "RT0402FRE07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RT0402FRE07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_0402_1005Metric",
        voltage_rating="50V",
        case_code_in="0402",
        case_code_mm="1005",
        power_rating="0.063W",
        temperature_coefficient="50 ppm/°C",
        resistance_range=[4.7, 500_000],
        extra_values=[80, 2710, 15200, 92000, 224000],
        excluded_values=[
            *[4.75, 4.87, 5.23, 5.36, 5.49, 5.62, 5.76, 5.9, 6.04, 6.19],
            *[6.34, 6.49, 6.65, 6.81, 6.98, 7.15, 7.32, 7.68, 7.87, 8.06],
            *[8.25, 8.45, 8.66, 8.87, 9.09, 9.31, 9.53, 9.76, 10.7, 11.3],
            *[11.8, 12.4, 15.8, 17.4, 19.1, 21, 23.2, 25.5, 28, 35.7],
            *[41.2, 45.3, 52.3, 54.9, 57.6, 73.2, 76.8, 88.7, 97.6, 118],
            *[137, 232, 324, 732, 768, 845, 1070, 1370, 6980, 7680],
            *[45300, 102000, 113000, 124000, 127000, 158000, 169000],
            *[191000, 237000, 243000, 249000, 255000, 261000, 267000],
            *[270000, 274000, 280000, 287000, 294000, 300000, 301000],
            *[309000, 316000, 324000, 330000, 332000, 340000, 348000],
            *[357000, 360000, 365000, 374000, 383000, 390000, 392000],
            *[402000, 412000, 422000, 430000, 432000, 442000, 453000],
            *[464000, 470000, 475000, 487000, 499000],
        ],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "RT0603FRE07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RT0603FRE07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_0603_1608Metric",
        voltage_rating="75V",
        case_code_in="0603",
        case_code_mm="1608",
        power_rating="0.1W",
        temperature_coefficient="50 ppm/°C",
        resistance_range=[1, 2_000_000],
        extra_values=[84.3, 1080, 5970, 8980, 16400, 44800, 79600, 89800],
        excluded_values=[
            *[1.02, 1.05, 1.07, 1.13, 1.15, 1.18, 1.2, 1.21, 1.24, 1.27],
            *[1.3, 1.33, 1.37, 1.4, 1.43, 1.54, 1.58, 1.6, 1.62, 1.65],
            *[1.69, 1.74, 1.78, 1.87, 1.91, 1.96, 2.05, 2.1, 2.15, 2.26],
            *[2.32, 2.37, 2.4, 2.43, 2.61, 2.67, 2.74, 2.8, 2.87, 2.94],
            *[3.09, 3.16, 3.24, 3.4, 3.48, 3.57, 3.74, 4.02, 4.12, 4.42],
            *[4.53, 4.87, 5.23, 5.36, 5.49, 5.9, 6.04, 6.19, 6.34, 6.49],
            *[6.65, 7.15, 7.32, 7.68, 7.87, 8.06, 8.45, 8.87, 9.09, 9.31],
            *[9.76, 10.5, 11.5, 12.4, 12.7, 13.3, 15.8, 16.9, 19.1, 20.5],
            *[23.2, 26.7, 28, 28.7, 29.4, 30.9, 32.4, 48.7, 57.6, 66.5],
            *[69.8, 73.2, 76.8, 84.5, 93.1, 97.6, 102, 107, 115, 255],
            *[280, 845, 52300, 715000, 732000, 768000, 787000, 845000],
            *[887000, 909000, 931000, 976000, 1020000, 1050000, 1070000],
            *[1100000, 1130000, 1150000, 1180000, 1200000, 1210000],
            *[1240000, 1270000, 1300000, 1330000, 1370000, 1400000],
            *[1430000, 1470000, 1500000, 1540000, 1580000, 1600000],
            *[1620000, 1650000, 1690000, 1740000, 1780000, 1800000],
            *[1820000, 1870000, 1910000, 1960000, 2000000],
        ],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "RC2512FK-7W": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RC2512FK-7W",
        mpn_sufix="L",
        footprint="resistor_footprints:R_2512_6332Metric",
        voltage_rating="200V",
        case_code_in="2512",
        case_code_mm="6332",
        power_rating="2W",
        temperature_coefficient="200 ppm/°C",
        resistance_range=[1, 10],
        specified_values=[
            *[1, 1.2, 1.6, 1.8, 2, 2.2, 2.7, 3],
            *[3.3, 3.9, 4.7, 6.2, 6.8, 7.5, 10],
        ],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://www.yageogroup.com/content/datasheet/asset/file/"
            "PYU-RC_GROUP_51_ROHS_L"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "SR2512FK-7W": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="SR2512FK-7W",
        mpn_sufix="L",
        footprint="resistor_footprints:R_2512_6332Metric",
        voltage_rating="200V",
        case_code_in="2512",
        case_code_mm="6332",
        power_rating="2W",
        temperature_coefficient="200 ppm/°C",
        resistance_range=[1, 100],
        specified_values=[1.4, 10, 22, 100],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://www.yageogroup.com/content/Resource%20Library/Datasheet/"
            "PYU-SR_20105_ROHS_L.pdf"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
}

SEI_STACKPOLE_SYMBOLS_SPECS: Final[dict[str, SeriesSpec]] = {
    "RMCF0402JT": SeriesSpec(
        manufacturer="SEI Stackpole",
        mpn_prefix="RMCF0402JT",
        mpn_sufix="",
        footprint="resistor_footprints:R_0402_1005Metric",
        voltage_rating="50V",
        case_code_in="0402",
        case_code_mm="1005",
        power_rating="0.063W",
        temperature_coefficient="100 ppm/°C",
        resistance_range=[10, 1_000_000],
        tolerance_map={"E24": "5%"},
        datasheet=("https://www.seielect.com/Catalog/SEI-RMCF_RMCP.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "RNCF0603TKY": SeriesSpec(
        manufacturer="SEI Stackpole",
        mpn_prefix="RNCF0603TKY",
        mpn_sufix="",
        footprint="resistor_footprints:R_0603_1608Metric",
        voltage_rating="75V",
        case_code_in="0603",
        case_code_mm="1608",
        power_rating="0.1W",
        temperature_coefficient="5 ppm/°C",
        resistance_range=[24.9, 59_000],
        specified_values=[
            *[75, 100, 150, 200, 250, 1000, 1200, 1500],
            *[2000, 3900, 4700, 10000, 20000],
        ],
        extra_values=[24.9, 49.9, 499, 1540, 3320, 4990],
        tolerance_map={"E24": "0.01%"},
        datasheet=("https://www.seielect.com/catalog/sei-rncf.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
}

ROHM_SEMICONDUCTOR_SYMBOLS_SPECS: Final[dict[str, SeriesSpec]] = {
    "PMR18EZPFV": SeriesSpec(
        manufacturer="ROHM Semiconductor",
        mpn_prefix="PMR18EZPFV",
        mpn_sufix="",
        footprint="resistor_footprints:R_1206_3216Metric",
        voltage_rating="200V",
        case_code_in="1206",
        case_code_mm="3216",
        power_rating="0.125W",
        temperature_coefficient="100 ppm/°C",
        resistance_range=[0.001, 0.004],
        specified_values=[1e-3, 2e-3, 3e-3, 4e-3],
        tolerance_map={"E24": "1%"},
        datasheet=(
            "https://fscdn.rohm.com/en/products/databook/datasheet/"
            "passive/resistor/chip_resistor/pmr_series-e.pdf"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "PMR18EZPFU": SeriesSpec(
        manufacturer="ROHM Semiconductor",
        mpn_prefix="PMR18EZPFU",
        mpn_sufix="",
        footprint="resistor_footprints:R_1206_3216Metric",
        voltage_rating="200V",
        case_code_in="1206",
        case_code_mm="3216",
        power_rating="0.125W",
        temperature_coefficient="100 ppm/°C",
        resistance_range=[0.005, 0.01],
        specified_values=[5e-3, 6e-3, 7e-3, 8e-3, 9e-3, 10e-3],
        tolerance_map={"E24": "1%"},
        datasheet=(
            "https://fscdn.rohm.com/en/products/databook/datasheet/"
            "passive/resistor/chip_resistor/pmr_series-e.pdf"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
}

MURATA_SYMBOLS_SPECS: Final[dict[str, SeriesSpec]] = {
    "NCP15XH": SeriesSpec(
        reference="RT",
        component_type="Thermistor",
        manufacturer="Murata",
        mpn_prefix="NCP15XH",
        mpn_sufix="F03RC",
        footprint="resistor_footprints:RT_0402_RT_1005Metric",
        voltage_rating="50V",
        case_code_in="0402_RT",
        case_code_mm="1005",
        power_rating="0.1W",
        temperature_coefficient="5 ppm/°C",
        resistance_range=[10_000, 10_000],
        tolerance_map={"E24": "1%"},
        datasheet=("https://www.murata.com/products/productdetail?partno="),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
}

BOURNS_SYMBOLS_SPECS: Final[dict[str, SeriesSpec]] = {
    "CHV2010-JW-": SeriesSpec(
        manufacturer="Bourns",
        mpn_prefix="CHV2010-JW-",
        mpn_sufix="ELF",
        footprint="resistor_footprints:R_2010_5025Metric",
        voltage_rating="2kV",
        case_code_in="2010",
        case_code_mm="5025",
        power_rating="0.5W",
        temperature_coefficient="200 ppm/°C",
        resistance_range=[100_000, 51_000_000],
        specified_values=[100_000, 4_700_000, 51_000_000],
        tolerance_map={"E24": "1%"},
        datasheet=("https://www.murata.com/products/productdetail?partno="),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "CRM1206-FX-": SeriesSpec(
        manufacturer="Bourns",
        mpn_prefix="CRM1206-FX-",
        mpn_sufix="ELF",
        footprint="resistor_footprints:R_1206_3216Metric",
        voltage_rating="200",
        case_code_in="1206",
        case_code_mm="3216",
        power_rating="0.5W",
        temperature_coefficient="100 ppm/°C",
        resistance_range=[0.047, 1_000_000],
        specified_values=[
            *[0.15, 0.68, 0.75, 1.5, 2, 2.2, 5.6],
            *[15, 22, 33, 47, 75, 120, 270],
        ],
        extra_values=[0.05, 4.75, 49.9],
        tolerance_map={"E24": "1%"},
        datasheet=(
            "https://bourns.com/docs/product-datasheets/"
            "crm0805_1206_2010.pdf?sfvrsn=a50d66f6_11"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "CRF2010-FZ-": SeriesSpec(
        manufacturer="Bourns",
        mpn_prefix="CRF2010-FZ-",
        mpn_sufix="ELF",
        footprint="resistor_footprints:R_2010_5025Metric",
        voltage_rating="-",
        case_code_in="2010",
        case_code_mm="5025",
        power_rating="1.5W",
        temperature_coefficient="100 ppm/°C",
        resistance_range=[0.001, 0.02],
        specified_values=[
            *[0.001, 0.002, 0.005, 0.01, 0.02],
        ],
        tolerance_map={"E24": "1%"},
        datasheet=("https://www.bourns.com/docs/product-datasheets/crf.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
}

VISHAY_SYMBOLS_SPECS: Final[dict[str, SeriesSpec]] = {
    "CRCW0402": SeriesSpec(
        manufacturer="Vishay",
        mpn_prefix="CRCW0402",
        mpn_sufix="FKED",
        footprint="resistor_footprints:R_0402_1005Metric",
        voltage_rating="50V",
        case_code_in="0402",
        case_code_mm="1005",
        power_rating="0.063W",
        temperature_coefficient="100 ppm/°C",
        resistance_range=[1, 10_000_000],
        extra_values=[
            *[1.02, 1.05, 1.07, 1.13, 1.15, 1.18, 1.21, 1.24, 1.27, 1.33],
            *[1.37, 1.43, 1.47, 1.54, 1.58, 1.62, 1.65, 1.69, 1.74, 1.78],
            *[1.82, 1.87, 1.91, 1.96, 2.05, 2.1, 2.21, 2.26, 2.32, 2.37],
            *[2.43, 2.49, 2.55, 2.61, 2.67, 2.74, 2.8, 2.87, 2.94, 3.01],
            *[3.09, 3.16, 3.24, 3.32, 3.4, 3.48, 3.57, 3.65, 3.74, 3.83],
            *[3.92, 4.02, 4.12, 4.22, 4.32, 4.42, 4.53, 4.64, 4.75, 4.87],
            *[4.99, 5.11, 5.23, 5.36, 5.49, 5.62, 5.76, 5.9, 6.04, 6.19],
            *[6.34, 6.49, 6.65, 6.81, 6.98, 7.15, 7.32, 7.5, 7.68, 7.87],
            *[8.06, 8.25, 8.45, 8.66, 8.87, 9.09, 9.31, 9.53, 9.76, 10.2],
            *[10.5, 10.7, 11.3, 11.5, 11.8, 12.1, 12.4, 12.7, 13.3, 13.7],
            *[14, 14.3, 14.7, 15.4, 15.8, 16.2, 16.5, 16.9, 17.4, 17.8],
            *[18.2, 18.7, 19.1, 19.6, 20.5, 21, 21.5, 22.1, 22.6, 23.2],
            *[23.7, 24.3, 24.9, 25.5, 26.1, 26.7, 27.4, 28, 28.7, 29.4],
            *[30.1, 30.9, 31.6, 32.4, 33.2, 34, 34.8, 35.7, 36.5, 37.4],
            *[38.4, 39.2, 40.2, 41.2, 42.2, 43.2, 44.2, 45.3, 46.4, 47.5],
            *[48.7, 49.9, 51.1, 52.3, 53.6, 54.9, 56.2, 57.6, 59, 60.4],
            *[61.9, 63.4, 64.9, 66.5, 68.1, 69.8, 71.5, 73.2, 76.8, 78.7],
            *[80.6, 82.5, 84.5, 86.6, 88.7, 90.9, 93.1, 95.3, 97.6, 102],
            *[105, 107, 113, 115, 118, 121, 124, 127, 133, 137, 143, 147],
            *[154, 158, 162, 165, 169, 174, 178, 182, 187, 191, 196, 205],
            *[210, 215, 221, 226, 232, 237, 243, 249, 255, 261, 267, 274],
            *[280, 287, 294, 309, 316, 324, 332, 340, 348, 357, 365, 374],
            *[383, 392, 402, 412, 422, 432, 442, 453, 464, 475, 487, 499],
            *[511, 523, 536, 549, 562, 576, 590, 604, 619, 634, 649, 665],
            *[681, 698, 715, 732, 768, 787, 806, 825, 845, 866, 887, 909],
            *[931, 953, 976, 1020, 1050, 1130, 1150, 1180, 1210, 1240, 1270],
            *[1330, 1370, 1400, 1430, 1470, 1540, 1580, 1620, 1650, 1690],
            *[1780, 1820, 1870, 1910, 1960, 2050, 2100, 2150, 2210, 2260],
            *[2320, 2370, 2430, 2550, 2610, 2670, 2740, 2800, 2870, 2940],
            *[3010, 3090, 3160, 3240, 3320, 3400, 3480, 3570, 3650, 3740],
            *[3830, 3920, 4020, 4120, 4220, 4320, 4420, 4530, 4640, 4750],
            *[4870, 4990, 5360, 5490, 5620, 5760, 5900, 6040, 6190, 6340],
            *[6490, 6650, 6810, 6980, 7150, 7320, 7500, 7680, 7870, 8060],
            *[8250, 8450, 8660, 8870, 9090, 9310, 9530, 9760, 10200, 10500],
            *[10700, 11300, 11500, 11800, 12100, 12400, 12700, 13300, 13700],
            *[14300, 14700, 15400, 15800, 16200, 16500, 16900, 17400, 17800],
            *[18200, 18700, 19100, 19600, 20500, 21000, 21500, 22100, 22600],
            *[23200, 23700, 24300, 24900, 25500, 26100, 26700, 27400, 28000],
            *[28700, 29400, 30100, 30900, 32400, 33200, 34000, 34800, 35700],
            *[36500, 37400, 38300, 39200, 40200, 42200, 43200, 44200, 45300],
            *[46400, 47500, 48700, 49900, 51100, 52300, 53600, 54900, 56200],
            *[57600, 59000, 60400, 61900, 63400, 64900, 68100, 69800, 71500],
            *[73200, 76800, 78700, 82500, 84500, 86600, 88700, 90900, 93100],
            *[95300, 97600, 102000, 105000, 107000, 113000, 115000, 118000],
            *[121000, 124000, 127000, 133000, 137000, 143000, 147000, 154000],
            *[158000, 162000, 165000, 169000, 174000, 178000, 182000, 187000],
            *[191000, 196000, 205000, 210000, 215000, 221000, 226000, 232000],
            *[237000, 243000, 249000, 255000, 267000, 274000, 280000, 287000],
            *[294000, 301000, 309000, 316000, 324000, 332000, 340000, 348000],
            *[357000, 365000, 374000, 383000, 392000, 402000, 412000, 422000],
            *[432000, 442000, 453000, 464000, 475000, 487000, 499000, 511000],
            *[523000, 536000, 549000, 562000, 576000, 590000, 604000, 619000],
            *[634000, 649000, 665000, 681000, 698000, 715000, 732000, 750000],
            *[768000, 787000, 806000, 825000, 845000, 866000, 887000, 909000],
            *[910000, 931000, 953000, 976000, 1000000, 1020000, 1050000],
            *[1070000, 1100000, 1130000, 1150000, 1180000, 1210000, 1240000],
            *[1270000, 1300000, 1330000, 1370000, 1400000, 1430000, 1470000],
            *[1500000, 1540000, 1580000, 1620000, 1650000, 1690000, 1740000],
            *[1780000, 1820000, 1870000, 1910000, 1960000, 2000000, 2050000],
            *[2100000, 2150000, 2210000, 2260000, 2320000, 2370000, 2430000],
            *[2490000, 2550000, 2610000, 2670000, 2740000, 2800000, 2870000],
            *[2940000, 3010000, 3090000, 3160000, 3240000, 3320000, 3400000],
            *[3480000, 3570000, 3650000, 3740000, 3830000, 3920000, 4020000],
            *[4120000, 4220000, 4320000, 4420000, 4530000, 4640000, 4750000],
            *[4870000, 4990000, 5100000, 5110000, 5230000, 5360000, 5490000],
            *[5620000, 5760000, 5900000, 6040000, 6190000, 6200000, 6340000],
            *[6490000, 6650000, 6800000, 6810000, 6980000, 7150000, 7320000],
            *[7500000, 7680000, 7870000, 8060000, 8200000, 8250000, 8450000],
            *[8660000, 8870000, 9090000, 9100000, 9310000, 9530000, 9760000],
            *[10000000],
        ],
        excluded_values=[20, 22, 1600, 10000],
        tolerance_map={"E24": "1%", "96": "1%"},
        datasheet=("https://www.vishay.com/docs/20035/dcrcwe3.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "CRCW0603": SeriesSpec(
        manufacturer="Vishay",
        mpn_prefix="CRCW0603",
        mpn_sufix="FKEAHP",
        footprint="resistor_footprints:R_0603_1608Metric",
        voltage_rating="75V",
        case_code_in="0603",
        case_code_mm="1608",
        power_rating="0.33W",
        temperature_coefficient="100 ppm/°C",
        resistance_range=[1, 1_000_000],
        excluded_values=[
            *[1.1, 1.2, 1.3, 1.33, 1.6, 1.8, 2.43, 3.6, 4.12, 4.22, 7.5, 9.1],
            *[11, 62, 91, 110, 130, 360, 1000, 1300, 1500, 1600, 3600, 6200],
            *[9100, 11000, 12000, 36000, 43000, 51000, 62000, 91000, 110000],
            *[130000, 160000, 200000, 300000, 360000, 390000, 430000, 510000],
            *[560000, 620000, 680000, 750000, 820000, 910000],
        ],
        extra_values=[
            *[1.05, 1.33, 1.54, 2.67, 3.01, 4.02, 4.64, 5.62, 6.81, 7.68],
            *[8.06, 8.25, 12.7, 16.2, 17.8, 22.1, 22.6, 24.9, 28, 32.4, 33.2],
            *[37.4, 38.3, 47.5, 49.9, 51.1, 53.6, 59, 60.4, 64.9, 69.8, 73.2],
            *[84.5, 86.6, 90.9, 121, 127, 143, 196, 215, 237, 249, 274, 294],
            *[301, 332, 374, 383, 402, 442, 499, 511, 562, 604, 649, 715],
            *[768, 845, 866, 1210, 1270, 1330, 2150, 2490, 2740, 2800, 3010],
            *[3320, 3650, 4220, 4530, 5490, 5760, 6040, 6340, 6490, 6810],
            *[6980, 8060, 8660, 9090, 10500, 12100, 12400, 13700, 14000],
            *[14700, 15400, 21000, 21500, 22100, 22600, 24300, 24900, 25500],
            *[26100, 28000, 30100, 30900, 31600, 32400, 34000, 40200, 46400],
            *[49900, 51100, 52300, 53600, 54900, 56200, 57600, 63400, 64900],
            *[69800, 80600, 86600, 105000, 127000, 133000, 154000, 158000],
            *[221000, 255000, 301000, 332000, 402000, 422000, 499000],
        ],
        tolerance_map={"E24": "1%", "96": "1%"},
        datasheet=("https://www.vishay.com/docs/20043/crcwhpe3.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "NTCS0805E3": SeriesSpec(
        reference="RT",
        component_type="Thermistor",
        manufacturer="Vishay",
        mpn_prefix="NTCS0805E3",
        mpn_sufix="JHT",
        footprint="resistor_footprints:RT_0805_RT_2012Metric",
        voltage_rating="50V",
        case_code_in="0805_RT",
        case_code_mm="2012",
        power_rating="0.21W",
        temperature_coefficient="5 ppm/°C",
        resistance_range=[10_000, 330_000],
        specified_values=[10_000, 22_000, 33_000, 47_000, 330_000],
        tolerance_map={"E24": "5%"},
        datasheet=("https://www.vishay.com/docs/29044/ntcs0805e3t.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
    "WFCP0612": SeriesSpec(
        manufacturer="Vishay",
        mpn_prefix="WFCP0612",
        mpn_sufix="FE66",
        footprint="resistor_footprints:R_0612_1632Metric",
        voltage_rating="",
        case_code_in="0612",
        case_code_mm="1632",
        power_rating="1W",
        temperature_coefficient="",
        resistance_range=[0.006, 0.03],
        specified_values=[
            *[0.006, 0.007, 0.008, 0.009, 0.01, 0.012, 0.015, 0.018, 0.02],
            *[0.024, 0.03],
        ],
        tolerance_map={"E24": "1%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/RDN0000/"
            "AOA0000C325.pdf"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
}

SUSUMU_SYMBOLS_SPECS: Final[dict[str, SeriesSpec]] = {
    "PRL1632-": SeriesSpec(
        manufacturer="Susumu",
        mpn_prefix="PRL1632-",
        mpn_sufix="-F-T1",
        footprint="resistor_footprints:R_0612_1632Metric",
        voltage_rating="",
        case_code_in="0612",
        case_code_mm="1632",
        power_rating="1W",
        temperature_coefficient="",
        resistance_range=[0.005, 0.1],
        specified_values=[
            *[5e-3, 6e-3, 7e-3, 8e-3, 9e-3, 10e-3, 11e-3, 12e-3, 13e-3],
            *[15e-3, 16e-3, 18e-3, 20e-3, 22e-3, 24e-3, 27e-3, 30e-3],
            *[33e-3, 36e-3, 39e-3, 43e-3, 47e-3, 50e-3, 51e-3, 56e-3, 62e-3],
            *[68e-3, 75e-3, 82e-3, 91e-3, 100e-3],
        ],
        tolerance_map={"E24": "1%"},
        datasheet=(
            "https://www.susumu.co.jp/common/pdf/n_catalog_partition07_en.pdf"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search/",
    ),
}

# Combined specifications dictionary
SYMBOLS_SPECS: Final[dict[str, SeriesSpec]] = {
    **PANASONIC_SYMBOLS_SPECS,
    **YAGEO_SYMBOLS_SPECS,
    **SEI_STACKPOLE_SYMBOLS_SPECS,
    **ROHM_SEMICONDUCTOR_SYMBOLS_SPECS,
    **MURATA_SYMBOLS_SPECS,
    **BOURNS_SYMBOLS_SPECS,
    **VISHAY_SYMBOLS_SPECS,
    **SUSUMU_SYMBOLS_SPECS,
}
