"""Detailed specifications for capacitor series and part numbers.

This module contains detailed specifications for various capacitor series,
including physical characteristics, electrical ratings, and available
configurations. It also provides a named tuple for complete information on a
specific capacitor part number.

Attributes:
    SeriesSpec: Detailed specifications for a capacitor series
    PartInfo: Complete information for a specific capacitor part number

"""

from __future__ import annotations

from typing import TYPE_CHECKING, Final, NamedTuple

if TYPE_CHECKING:
    from collections.abc import Iterator

ValueBasedSuffixMapping = dict[tuple[float, ...], str]
ValueBasedPrefixMapping = dict[tuple[float, ...], str]


class SeriesSpec(NamedTuple):
    """Detailed specifications for a capacitor series.

    Contains all necessary parameters to define a specific capacitor series,
    including physical characteristics, electrical ratings,
    and available configurations.

    Attributes:
        mpn_prefix: Manufacturer part number prefix for the series
        manufacturer: Name of the component manufacturer
        footprint: PCB footprint ID for the component
        voltage_rating: Maximum operating voltage for the component
        case_code_in: Package dimensions in inches (e.g., '0402')
        case_code_mm: Package dimensions in millimeters (e.g., '1005')
        mpn_sufix: List of manufacturer part number suffixes
        tolerance_map: Mapping of dielectric type to tolerance codes
        value_range: Mapping of dielectric type to capacitance value range
        datasheet_url: Base URL for component datasheets
        trustedparts_url: Base URL for component listings on Trustedparts
        dielectric_code: Mapping of dielectric type to dielectric codes
        characteristic_codes: Mapping of capacitance thresholds to codes
        excluded_values: Set of capacitance values to exclude
        specified_values: List of specified capacitance values
        additional_values:
            Dictionary mapping dielectric types to lists of additional values
        value_based_mpn_sufix_map:
            Optional mapping of value tuples to MPN suffixes
        value_based_mpn_prefix_map:
            Optional mapping of value tuples to MPN prefixes
        reference: Reference designator for the component

    """

    mpn_prefix: str
    manufacturer: str
    footprint: str
    voltage_rating: str
    case_code_in: str
    case_code_mm: str
    tolerance_map: dict[str, dict[str, str]]
    value_range: dict[str, tuple[float, float]]
    datasheet_url: str
    trustedparts_url: str
    dielectric_code: dict[str, str] = {}  # noqa: RUF012
    characteristic_codes: dict[float, str] = {}  # noqa: RUF012
    excluded_values: set[float] | None = None
    specified_values: list[float] | None = None
    additional_values: set[float] | None = None
    capacitor_type: str = "Ceramic"
    reference: str = "C"
    mpn_sufix: list[str] | str = ""
    value_based_mpn_sufix_map: ValueBasedSuffixMapping | None = None
    value_based_mpn_prefix_map: ValueBasedPrefixMapping | None = None
    value_footprints: dict[float, str] | None = None
    value_voltage_ratings: dict[float, str] | None = None
    value_case_codes_in: dict[float, str] | None = None
    value_case_codes_mm: dict[float, str] | None = None
    value_3d_models: dict[float, str] | None = None


class PartInfo(NamedTuple):
    """Complete information for a specific capacitor part number.

    Contains all relevant details for a specific capacitor part number,
    including symbol name, reference designator, value, footprint, and more.

    Attributes:
        symbol_name: Unique symbol name for the component
        reference: Reference designator for the component
        value: Capacitance value in farads
        formatted_value: Human-readable capacitance value with units
        footprint: PCB footprint ID for the component
        datasheet: URL to component datasheet
        description: Detailed description of the component
        manufacturer: Name of the component manufacturer
        mpn: Manufacturer part number for the component
        dielectric: Dielectric material type (e.g., 'X7R')
        tolerance: Tolerance percentage for the component
        voltage_rating: Maximum operating voltage for the component
        case_code_in: Package dimensions in inches (e.g., '0402')
        case_code_mm: Package dimensions in millimeters (e.g., '1005')
        series: Part number series identifier (e.g., 'GCM155')
        trustedparts_link: URL to component listing on Trustedparts

    """

    symbol_name: str
    reference: str
    value: float
    formatted_value: str
    footprint: str
    datasheet: str
    description: str
    manufacturer: str
    mpn: str
    dielectric: str
    tolerance: str
    voltage_rating: str
    case_code_in: str
    case_code_mm: str
    series: str
    trustedparts_link: str
    capacitor_type: str

    @staticmethod
    def format_value(capacitance: float) -> str:
        """Format capacitance value with appropriate units.

        Args:
            capacitance: Capacitance value in farads

        Returns:
            Formatted capacitance value with units

        """
        pf_value = capacitance * 1e12

        # 1 F and above
        if capacitance >= 1:
            value = capacitance
            unit = "F"
        # Between 1000 µF and 1,000,000 µF (exclusive) -> convert to mF
        elif capacitance >= 1000e-6 and capacitance < 1:
            value = capacitance / 1e-3
            unit = "mF"
        # 1 µF and above
        elif capacitance >= 1e-6:  # noqa: PLR2004
            value = capacitance / 1e-6
            unit = "µF"
        # 1000 pF and above -> convert to nF
        elif pf_value >= 1000:  # noqa: PLR2004
            value = pf_value / 1000
            unit = "nF"
        else:  # Below 1000 pF
            value = pf_value
            unit = "pF"

        # Format the number to remove unnecessary decimals
        if value % 1 == 0:
            return f"{int(value)} {unit}"
        formatted = f"{value:.3g}"

        return f"{formatted} {unit}"

    @staticmethod
    def generate_capacitance_code(capacitance: float) -> str:
        """Generate capacitance code based on capacitance value.

        Args:
            capacitance: Capacitance value in farads

        Returns:
            Capacitance code as a string

        """
        pf_value = capacitance * 1e12

        # Handle values under 10pF
        if pf_value < 10:  # noqa: PLR2004
            whole = int(pf_value)
            decimal = round((pf_value - whole) * 10)
            return f"{whole}R{decimal}"

        # Handle values under 100pF
        if pf_value < 100:  # noqa: PLR2004
            value = round(pf_value * 10)
            return f"{value}"

        # Handle values under 1000pF
        if pf_value < 1000:  # noqa: PLR2004
            significant = round(pf_value)
            if significant % 10 == 0:
                significant += 1
            return f"{significant:03d}"

        # Handle values 1000pF and above
        sci_notation = f"{pf_value:.2e}"
        parts = sci_notation.split("e")
        significand = float(parts[0])
        power = int(parts[1])

        first_two = round(significand * 10)
        zero_count = power - 1

        return f"{first_two}{zero_count}"

    @staticmethod
    def generate_eaton_capacitance_code(capacitance: float) -> str:
        """Generate Eaton-style capacitance code from capacitance value.

        Args:
            capacitance: Capacitance value in farads

        Returns:
            Eaton capacitance code as a string

        """
        if capacitance >= 100:
            exp_indicator = 7
        elif capacitance >= 10:
            exp_indicator = 6
        elif capacitance >= 1:
            exp_indicator = 5
        elif capacitance >= 0.1:
            exp_indicator = 4
        elif capacitance >= 0.01:
            exp_indicator = 3
        else:
            exp_indicator = 2

        base_value = capacitance * (10 ** (6 - exp_indicator))

        base_value = round(base_value)

        code = f"{base_value}{exp_indicator}-R"

        return code

    @classmethod
    def get_characteristic_code(
        cls,
        capacitance: float,
        specs: SeriesSpec,
    ) -> str:
        """Get the characteristic code for a given capacitance value.

        Args:
            capacitance: Capacitance value in farads
            specs: Series specifications for the component

        Returns:
            Characteristic code for the given capacitance

        """
        if specs.mpn_prefix.startswith("CL"):
            return "X7R"

        if not specs.characteristic_codes:
            return ""

        for threshold, code in sorted(
            specs.characteristic_codes.items(),
            reverse=True,
        ):
            if capacitance > threshold:
                return code

        return list(specs.characteristic_codes.values())[-1]

    @classmethod
    def generate_standard_values(
        cls,
        min_value: float,
        max_value: float,
        excluded_values: set[float] | None = None,
        specified_values: list[float] | None = None,
    ) -> Iterator[float]:
        """Generate E12 standard values within a given range.

        Args:
            min_value: Minimum capacitance value in farads
            max_value: Maximum capacitance value in farads
            excluded_values: Set of capacitance values to exclude
            specified_values: List of specified capacitance values

        Yields:
            Standard capacitance values within the specified range

        """
        e12_multipliers = [
            *[1.0, 1.2, 1.5, 1.8, 2.2, 2.7],
            *[3.3, 3.9, 4.7, 5.6, 6.8, 8.2],
        ]

        normalized_excluded = {}
        if excluded_values is not None:
            normalized_excluded = {
                float(f"{value:.1e}") for value in excluded_values
            }

        decade = 1.0e-12
        while decade <= max_value:
            for multiplier in e12_multipliers:
                normalized_value = float(f"{decade * multiplier:.1e}")
                if (
                    min_value <= normalized_value <= max_value
                    and normalized_value not in normalized_excluded
                    and (
                        specified_values is None
                        or normalized_value in specified_values
                    )
                ):
                    yield normalized_value
            decade *= 10

    @classmethod
    def generate_all_values(
        cls,
        min_value: float,
        max_value: float,
        excluded_values: set[float] | None = None,
        specified_values: list[float] | None = None,
        additional_values: list[float] | None = None,
    ) -> Iterator[float]:
        """Generate all valid capacitance values.

        Args:
            min_value: Minimum capacitance value in farads
            max_value: Maximum capacitance value in farads
            excluded_values: Set of capacitance values to exclude
            specified_values: List of specified capacitance values
            additional_values:
                List of additional non-standard values to include

        Yields:
            All valid capacitance values within the specified range

        """
        # First yield all standard E12 values
        for value in cls.generate_standard_values(
            min_value,
            max_value,
            excluded_values,
            specified_values,
        ):
            yield value

        # Then yield additional values if provided
        if additional_values:
            normalized_excluded = set()
            if excluded_values is not None:
                normalized_excluded = {
                    float(f"{value:.1e}") for value in excluded_values
                }

            for value in additional_values:
                normalized_value = float(f"{value:.1e}")
                if (
                    min_value <= normalized_value <= max_value
                    and normalized_value not in normalized_excluded
                    and (
                        specified_values is None
                        or normalized_value in specified_values
                    )
                ):
                    yield normalized_value

    @staticmethod
    def generate_datasheet_url(
        mpn: str,
        specs: SeriesSpec,
    ) -> str:
        """Generate complete datasheet URL for a given part number.

        Args:
            mpn: Manufacturer part number for the component
            specs: Series specifications for the component

        Returns:
            Complete URL to the component datasheet

        """
        if specs.manufacturer == "Murata Electronics":
            return f"{specs.datasheet_url}{mpn[:-1]}-01.pdf"
        if specs.manufacturer in ("Vishay", "Panasonic", "Eaton Electronics"):
            return f"{specs.datasheet_url}"
        return f"{specs.datasheet_url}{mpn}"

    @classmethod
    def create_part_info(  # noqa: PLR0913
        cls,
        capacitance: float,
        tolerance_code: str,
        tolerance_value: str,
        packaging: str,
        dielectric_type: str,
        specs: SeriesSpec,
    ) -> PartInfo:
        """Create a PartInfo object for a specific capacitor part number.

        Args:
            capacitance: Capacitance value in farads
            tolerance_code: Tolerance code for the component
            tolerance_value: Tolerance percentage for the component
            packaging: Packaging code for the component
            dielectric_type: Dielectric material type (e.g., 'X7R')
            specs: Series specifications for the component

        Returns:
            PartInfo object with complete component information

        """
        capacitance_code = cls.generate_capacitance_code(capacitance)
        characteristic_code = cls.get_characteristic_code(capacitance, specs)
        formatted_value = cls.format_value(capacitance)

        effective_packaging = packaging
        if specs.value_based_mpn_sufix_map and packaging == "":
            value_found = False
            for (
                value_tuple,
                suffix,
            ) in specs.value_based_mpn_sufix_map.items():
                for specific_value in value_tuple:
                    if abs(capacitance - specific_value) < 1e-15:
                        effective_packaging = suffix
                        value_found = True
                        break
                if value_found:
                    break

            if not value_found:
                if (
                    isinstance(specs.mpn_sufix, list)
                    and len(specs.mpn_sufix) > 0
                ):
                    effective_packaging = specs.mpn_sufix[0]
                elif isinstance(specs.mpn_sufix, str) and specs.mpn_sufix:
                    effective_packaging = specs.mpn_sufix
                else:
                    effective_packaging = ""

        if specs.manufacturer == "Murata Electronics":
            mpn = (
                f"{specs.mpn_prefix}"
                f"{capacitance_code}"
                f"{tolerance_code}"
                f"{characteristic_code}"
                f"{effective_packaging}"
            )
        elif specs.manufacturer == "TDK":
            mpn = (
                f"{specs.mpn_prefix}"
                f"{capacitance_code}"
                f"{tolerance_code}"
                f"{effective_packaging}"
            )
        elif specs.manufacturer == "KYOCERA AVX":
            mpn = f"{specs.mpn_prefix}{capacitance_code}{effective_packaging}"
        elif specs.manufacturer == "YAGEO":
            mpn = f"{specs.mpn_prefix}{capacitance_code}"
        elif specs.manufacturer == "Wurth Elektronik":
            mpn = f"{specs.mpn_prefix}"
        elif specs.manufacturer == "Panasonic":
            mpn = (
                f"{specs.mpn_prefix}"
                f"{formatted_value.split(' ')[0]}"
                f"{specs.mpn_sufix}"
            )
        elif specs.manufacturer == "Eaton Electronics":
            capacitance_code = cls.generate_eaton_capacitance_code(
                capacitance
            )
            if specs.value_based_mpn_prefix_map:
                prefix = specs.mpn_prefix
                for (
                    value_tuple,
                    mapped_prefix,
                ) in specs.value_based_mpn_prefix_map.items():
                    for specific_value in value_tuple:
                        if abs(capacitance - specific_value) < 1e-15:
                            prefix = mapped_prefix
                            break
                    else:
                        continue
                    break
                mpn = f"{prefix}{capacitance_code}"
            else:
                mpn = f"{specs.mpn_prefix}{capacitance_code}"
        else:
            mpn = (
                f"{specs.mpn_prefix}"
                f"{capacitance_code}"
                f"{tolerance_code}"
                f"{effective_packaging}"
            )

        case_code_in_value = (
            specs.value_case_codes_in.get(capacitance, specs.case_code_in)
            if specs.value_case_codes_in
            else specs.case_code_in
        )
        voltage_rating_value = (
            specs.value_voltage_ratings.get(capacitance, specs.voltage_rating)
            if specs.value_voltage_ratings
            else specs.voltage_rating
        )

        description = (
            f"CAP SMD {formatted_value} "
            f"{dielectric_type} {tolerance_value} "
            f"{case_code_in_value} {voltage_rating_value}"
        )

        trustedparts_link = f"{specs.trustedparts_url}/{mpn}"
        datasheet_url = cls.generate_datasheet_url(mpn, specs)

        footprint_value = (
            specs.value_footprints.get(capacitance, specs.footprint)
            if specs.value_footprints
            else specs.footprint
        )
        case_code_mm_value = (
            specs.value_case_codes_mm.get(capacitance, specs.case_code_mm)
            if specs.value_case_codes_mm
            else specs.case_code_mm
        )

        if (
            specs.manufacturer == "Eaton Electronics"
            and specs.value_based_mpn_prefix_map
        ):
            if mpn.endswith(capacitance_code):
                actual_prefix = mpn[: -len(capacitance_code)]
            else:
                actual_prefix = specs.mpn_prefix
            series_value = actual_prefix
        else:
            series_value = specs.mpn_prefix

        return cls(
            symbol_name=f"{specs.reference}_{mpn}",
            reference="C",
            value=capacitance,
            formatted_value=formatted_value,
            footprint=footprint_value,
            datasheet=datasheet_url,
            description=description,
            manufacturer=specs.manufacturer,
            mpn=mpn,
            dielectric=dielectric_type,
            tolerance=tolerance_value,
            voltage_rating=voltage_rating_value,
            case_code_in=case_code_in_value,
            case_code_mm=case_code_mm_value,
            series=series_value,
            trustedparts_link=trustedparts_link,
            capacitor_type=specs.capacitor_type,
        )

    @classmethod
    def generate_part_numbers(
        cls,
        specs: SeriesSpec,
    ) -> list[PartInfo]:
        """Generate a list of PartInfo objects for a given series.

        Args:
            specs: Series specifications for the component

        Returns:
            List of PartInfo objects for the given series

        """
        parts_list: list[PartInfo] = []
        dielectric_types = [
            "X5R",
            "X7R",
            "X7S",
            "C0G (NP0)",
            "Polymer",
            "Supercapacitor",
        ]

        for dielectric_type in dielectric_types:
            if dielectric_type in specs.value_range:
                min_val, max_val = specs.value_range[dielectric_type]
                for capacitance in cls.generate_all_values(
                    min_val,
                    max_val,
                    specs.excluded_values,
                    specs.specified_values,
                    specs.additional_values,
                ):
                    for (
                        tolerance_code,
                        tolerance_value,
                    ) in specs.tolerance_map[dielectric_type].items():
                        if specs.value_based_mpn_sufix_map:
                            value_has_mapping = False
                            for (
                                value_tuple
                            ) in specs.value_based_mpn_sufix_map.keys():
                                for specific_value in value_tuple:
                                    if (
                                        abs(capacitance - specific_value)
                                        < 1e-15
                                    ):
                                        value_has_mapping = True
                                        break
                                if value_has_mapping:
                                    break

                            if value_has_mapping:
                                parts_list.append(
                                    cls.create_part_info(
                                        capacitance=capacitance,
                                        tolerance_code=tolerance_code,
                                        tolerance_value=tolerance_value,
                                        packaging="",
                                        dielectric_type=dielectric_type,
                                        specs=specs,
                                    ),
                                )
                            else:
                                suffixes = (
                                    specs.mpn_sufix
                                    if specs.mpn_sufix
                                    else [""]
                                )
                                for packaging in suffixes:
                                    parts_list.append(  # noqa: PERF401
                                        cls.create_part_info(
                                            capacitance=capacitance,
                                            tolerance_code=tolerance_code,
                                            tolerance_value=tolerance_value,
                                            packaging=packaging,
                                            dielectric_type=dielectric_type,
                                            specs=specs,
                                        ),
                                    )
                        else:
                            # Use traditional approach with fixed MPN suffixes
                            suffixes = (
                                specs.mpn_sufix if specs.mpn_sufix else [""]
                            )
                            for packaging in suffixes:
                                parts_list.append(  # noqa: PERF401
                                    cls.create_part_info(
                                        capacitance=capacitance,
                                        tolerance_code=tolerance_code,
                                        tolerance_value=tolerance_value,
                                        packaging=packaging,
                                        dielectric_type=dielectric_type,
                                        specs=specs,
                                    ),
                                )

        return sorted(parts_list, key=lambda x: (x.dielectric, x.value))


# Base URLs for documentation
MURATA_DOC_BASE = (
    "https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/"
)

MURATA_SYMBOLS_SPECS = {
    "GCM155R71H": SeriesSpec(
        manufacturer="Murata Electronics",
        mpn_prefix="GCM155R71H",
        value_range={"X7R": (220e-12, 0.1e-6)},  # 220pF to 0.1µF
        tolerance_map={"X7R": {"K": "10%"}},
        characteristic_codes={22e-9: "E02", 4.7e-9: "A55", 0: "A37"},
        mpn_sufix=["D", "J"],
        footprint="capacitor_footprints:C_0402_1005Metric",
        voltage_rating="50V",
        case_code_in="0402",
        case_code_mm="1005",
        excluded_values={27e-9, 39e-9, 56e-9, 82e-9},
        datasheet_url=f"{MURATA_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "GCM155C71A": SeriesSpec(
        manufacturer="Murata Electronics",
        mpn_prefix="GCM155C71A",
        value_range={"X7S": (470e-9, 1e-6)},
        tolerance_map={"X7S": {"K": "10%"}},
        characteristic_codes={470e-9: "E38", 1e-6: "E36"},
        mpn_sufix=["D", "J"],
        footprint="capacitor_footprints:C_0402_1005Metric",
        voltage_rating="10V",
        case_code_in="0402",
        case_code_mm="1005",
        excluded_values={560e-9, 820e-9},
        datasheet_url=f"{MURATA_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "GRM155C70J": SeriesSpec(
        manufacturer="Murata Electronics",
        mpn_prefix="GRM155C70J",
        value_range={"X7S": (1e-6, 2.2e-6)},
        tolerance_map={"X7S": {"K": "10%"}},
        characteristic_codes={2.2e-6: "E11"},
        mpn_sufix=["D", "J"],
        footprint="capacitor_footprints:C_0402_1005Metric",
        voltage_rating="6.3V",
        case_code_in="0402",
        case_code_mm="1005",
        excluded_values={1.2e-6, 1.5e-6, 1.8e-6},
        datasheet_url=f"{MURATA_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "GRT155R61A": SeriesSpec(
        manufacturer="Murata Electronics",
        mpn_prefix="GRT155R61A",
        value_range={"X5R": (10e-6, 10e-6)},
        tolerance_map={"X5R": {"M": "20%"}},
        characteristic_codes={10e-6: "E13"},
        mpn_sufix=["D", "J"],
        footprint="capacitor_footprints:C_0402_1005Metric",
        voltage_rating="10V",
        case_code_in="0402",
        case_code_mm="1005",
        specified_values=[10e-6],
        datasheet_url=f"{MURATA_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "GCM1555C1H": SeriesSpec(
        manufacturer="Murata Electronics",
        mpn_prefix="GCM1555C1H",
        value_range={"C0G (NP0)": (5e-12, 1e-9)},
        tolerance_map={"C0G (NP0)": {"F": "1%"}},
        characteristic_codes={1e-9: "A16"},
        mpn_sufix=["D", "J"],
        excluded_values={5.6e-12, 8.2e-12},
        additional_values={
            *[5e-12, 5.1e-12, 6e-12, 7e-12, 8e-12, 11e-12, 13e-12, 16e-12],
            *[20e-12, 24e-12, 30e-12, 36e-12, 43e-12, 51e-12, 62e-12, 75e-12],
            *[91e-12, 110e-12, 130e-12, 160e-12, 200e-12, 240e-12, 300e-12],
            *[360e-12, 430e-12, 510e-12, 620e-12, 750e-12, 910e-12],
        },
        footprint="capacitor_footprints:C_0402_1005Metric",
        voltage_rating="50V",
        case_code_in="0402",
        case_code_mm="1005",
        datasheet_url=f"{MURATA_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "GRM155Z71A": SeriesSpec(
        manufacturer="Murata Electronics",
        mpn_prefix="GRM155Z71A",
        value_range={"X7R": (1e-6, 2.2e-6)},
        tolerance_map={"X7R": {"K": "10%"}},
        characteristic_codes={2.2e-6: "E44"},
        mpn_sufix=["D", "J"],
        footprint="capacitor_footprints:C_0402_1005Metric",
        voltage_rating="10V",
        case_code_in="0402",
        case_code_mm="1005",
        excluded_values={1.2e-6, 1.5e-6, 1.8e-6},
        datasheet_url=f"{MURATA_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "GCM188R71H": SeriesSpec(
        manufacturer="Murata Electronics",
        mpn_prefix="GCM188R71H",
        value_range={"X7R": (1e-9, 220e-9)},  # 1nF to 220nF
        tolerance_map={"X7R": {"K": "10%"}},
        characteristic_codes={
            100e-9: "A64",
            47e-9: "A57",
            22e-9: "A55",
            0: "A37",
        },
        mpn_sufix=["D", "J"],
        footprint="capacitor_footprints:C_0603_1608Metric",
        voltage_rating="50V",
        case_code_in="0603",
        case_code_mm="1608",
        excluded_values={120e-9, 180e-9},
        datasheet_url=f"{MURATA_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "GRM188R71A": SeriesSpec(
        manufacturer="Murata Electronics",
        mpn_prefix="GRM188R71A",
        value_range={"X7R": (0.33e-6, 0.68e-6)},
        tolerance_map={"X7R": {"K": "10%"}},
        characteristic_codes={0.68e-6: "A61"},
        mpn_sufix=["D"],
        footprint="capacitor_footprints:C_0603_1608Metric",
        voltage_rating="10V",
        case_code_in="0603",
        case_code_mm="1608",
        datasheet_url=f"{MURATA_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "GCM216R71H": SeriesSpec(
        manufacturer="Murata Electronics",
        mpn_prefix="GCM216R71H",
        value_range={"X7R": (1e-9, 22e-9)},
        tolerance_map={"X7R": {"K": "10%"}},
        characteristic_codes={22e-9: "A55", 0: "A37"},
        mpn_sufix=["D", "J"],
        footprint="capacitor_footprints:C_0805_060_2012Metric",
        voltage_rating="50V",
        case_code_in="0805_060",
        case_code_mm="2012",
        excluded_values=set(),
        datasheet_url=f"{MURATA_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "GRM21BR61H": SeriesSpec(
        manufacturer="Murata Electronics",
        mpn_prefix="GRM21BR61H",
        value_range={"X5R": (10e-6, 10e-6)},
        tolerance_map={"X5R": {"K": "10%"}},
        characteristic_codes={0: "E43"},
        mpn_sufix=["K", "L"],
        footprint="capacitor_footprints:C_0805_125_2012Metric",
        voltage_rating="50V",
        case_code_in="0805_125",
        case_code_mm="2012",
        excluded_values=set(),
        datasheet_url=f"{MURATA_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "GRM185R61E": SeriesSpec(
        manufacturer="Murata Electronics",
        mpn_prefix="GRM185R61E",
        value_range={"X5R": (1e-6, 1e-6)},
        tolerance_map={"X5R": {"K": "10%"}},
        characteristic_codes={0: "A12"},
        mpn_sufix=["D", "J"],
        footprint="capacitor_footprints:C_0603_1608Metric",
        voltage_rating="25V",
        case_code_in="0603",
        case_code_mm="1608",
        excluded_values=set(),
        datasheet_url=f"{MURATA_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "GRJ21BC72A": SeriesSpec(
        manufacturer="Murata Electronics",
        mpn_prefix="GRJ21BC72A",
        value_range={"X7S": (1e-6, 1e-6)},
        tolerance_map={"X7S": {"K": "10%"}},
        characteristic_codes={1e-6: "E11"},
        mpn_sufix=["L", "K"],
        footprint="capacitor_footprints:C_0805_2012Metric",
        voltage_rating="100V",
        case_code_in="0805",
        case_code_mm="2012",
        excluded_values=set(),
        datasheet_url=f"{MURATA_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "GCM31MR71H": SeriesSpec(
        manufacturer="Murata Electronics",
        mpn_prefix="GCM31MR71H",
        value_range={"X7R": (100e-9, 1e-6)},  # 100nF to 1µF
        tolerance_map={"X7R": {"K": "10%"}},
        characteristic_codes={560e-9: "A55", 100e-9: "A37", 0: "A37"},
        mpn_sufix=["K", "L"],
        footprint="capacitor_footprints:C_1206_3216Metric",
        voltage_rating="50V",
        case_code_in="1206",
        case_code_mm="3216",
        excluded_values={180e-9, 560e-9},
        datasheet_url=f"{MURATA_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "GCM31CR71E": SeriesSpec(
        manufacturer="Murata Electronics",
        mpn_prefix="GCM31CR71E",
        value_range={"X7R": (4.7e-6, 4.7e-6)},  # Only 4.7µF
        tolerance_map={"X7R": {"K": "10%"}},
        characteristic_codes={0: "A55"},
        mpn_sufix=["K", "L"],
        footprint="capacitor_footprints:C_1206_3216Metric",
        voltage_rating="25V",
        case_code_in="1206",
        case_code_mm="3216",
        excluded_values=set(),
        datasheet_url=f"{MURATA_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "GRM188C71A": SeriesSpec(
        manufacturer="Murata Electronics",
        mpn_prefix="GRM188C71A",
        value_range={"X7S": (4.7e-6, 4.7e-6)},  # Only 4.7µF
        tolerance_map={"X7S": {"K": "10%"}},
        characteristic_codes={0: "E11"},
        mpn_sufix=["D"],
        footprint="capacitor_footprints:C_0603_1608Metric",
        voltage_rating="10V",
        case_code_in="0603",
        case_code_mm="1608",
        excluded_values=set(),
        datasheet_url=f"{MURATA_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "GCM32DC72A": SeriesSpec(
        manufacturer="Murata Electronics",
        mpn_prefix="GCM32DC72A",
        value_range={"X7S": (4.7e-6, 4.7e-6)},  # Only 4.7µF
        tolerance_map={"X7S": {"K": "10%"}},
        characteristic_codes={0: "E02"},
        mpn_sufix=["K", "L"],
        footprint="capacitor_footprints:C_1210_200_3225Metric",
        voltage_rating="100V",
        case_code_in="1210_200",
        case_code_mm="3225",
        excluded_values=set(),
        datasheet_url=f"{MURATA_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "GRM32ER71A": SeriesSpec(
        manufacturer="Murata Electronics",
        mpn_prefix="GRM32ER71A",
        value_range={"X7R": (47e-6, 47e-6)},
        tolerance_map={"X7R": {"K": "10%"}},
        characteristic_codes={0: "E15"},
        mpn_sufix=["L"],
        footprint="capacitor_footprints:C_1210_200_3225Metric",
        voltage_rating="10V",
        case_code_in="1210_200",
        case_code_mm="3225",
        excluded_values=set(),
        datasheet_url=f"{MURATA_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "GRM32EC72A": SeriesSpec(
        manufacturer="Murata Electronics",
        mpn_prefix="GRM32EC72A",
        value_range={"X7S": (10e-6, 10e-6)},
        tolerance_map={"X7S": {"K": "10%"}},
        characteristic_codes={0: "E05"},
        mpn_sufix=["L"],
        footprint="capacitor_footprints:C_1210_250_3225Metric",
        voltage_rating="100V",
        case_code_in="1210_250",
        case_code_mm="3225",
        excluded_values=set(),
        datasheet_url=f"{MURATA_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "GRM31CR60J": SeriesSpec(
        manufacturer="Murata Electronics",
        mpn_prefix="GRM31CR60J",
        value_range={"X5R": (220e-6, 220e-6)},
        tolerance_map={"X5R": {"M": "20%"}},
        characteristic_codes={0: "E11"},
        mpn_sufix=["K", "L"],
        footprint="capacitor_footprints:C_1206_3216Metric",
        voltage_rating="6.3V",
        case_code_in="1206",
        case_code_mm="3216",
        datasheet_url=f"{MURATA_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
}

YAGEO_DOC_BASE = "https://www.yageo.com/en/Chart/Download/pdf/"

YAGEO_SYMBOLS_SPECS = {
    "AC0402KRX7R9BB": SeriesSpec(
        manufacturer="YAGEO",
        mpn_prefix="AC0402KRX7R9BB",
        value_range={"X7R": (220e-12, 100e-9)},
        excluded_values={
            *[390e-12, 27e-9, 39e-9, 56e-9, 82e-9],
        },
        tolerance_map={"X7R": {"": "10%"}},
        footprint="capacitor_footprints:C_0402_1005Metric",
        voltage_rating="50V",
        case_code_in="0402",
        case_code_mm="1005",
        datasheet_url=f"{YAGEO_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "CC0603JRNPO9BN": SeriesSpec(
        manufacturer="YAGEO",
        mpn_prefix="CC0603JRNPO9BN",
        value_range={"C0G (NP0)": (8e-12, 10e-9)},
        additional_values=[
            *[8e-12, 11e-12, 13e-12, 16e-12, 20e-12, 24e-12, 25e-12, 30e-12],
            *[36e-12, 43e-12, 51e-12, 62e-12, 75e-12, 91e-12, 110e-12],
            *[130e-12, 160e-12, 200e-12, 240e-12, 300e-12, 360e-12, 430e-12],
            *[500e-12, 510e-12, 620e-12, 750e-12],
        ],
        excluded_values=[3.9e-9, 5.6e-9, 6.8e-9, 8.2e-9],
        tolerance_map={"C0G (NP0)": {"": "5%"}},
        footprint="capacitor_footprints:C_0603_1608Metric",
        voltage_rating="50V",
        case_code_in="0603",
        case_code_mm="1608",
        datasheet_url=f"{YAGEO_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
}

# Base URLs for documentation
SAMSUNG_DOC_BASE = (
    "https://weblib.samsungsem.com/mlcc/mlcc-ec-data-sheet.do?partNumber="
)

SAMSUNG_SYMBOLS_SPECS = {
    "CL31B": SeriesSpec(
        mpn_prefix="CL31B",
        manufacturer="Samsung Electro-Mechanics",
        footprint="capacitor_footprints:C_1206_3216Metric",
        voltage_rating="50V",
        case_code_in="1206",
        case_code_mm="3216",
        mpn_sufix=["BHNNN#"],
        tolerance_map={"X7R": {"K": "10%"}},
        value_range={"X7R": (0.47e-6, 10e-6)},
        dielectric_code={"X7R": "B"},
        specified_values=[0.47e-6, 1e-6, 2.2e-6, 4.7e-6, 10e-6],
        datasheet_url=f"{SAMSUNG_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search/CL31",
    ),
    "CL31A": SeriesSpec(
        mpn_prefix="CL31A",
        manufacturer="Samsung Electro-Mechanics",
        footprint="capacitor_footprints:C_1206_3216Metric",
        voltage_rating="25V",
        case_code_in="1206",
        case_code_mm="3216",
        mpn_sufix=["AHNNNE"],
        tolerance_map={"X5R": {"K": "10%"}},
        value_range={"X5R": (0.47e-6, 22e-6)},
        dielectric_code={"X5R": "B"},
        specified_values=[4.7e-6, 10e-6, 22e-6],
        datasheet_url=f"{SAMSUNG_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search/CL31",
    ),
}

# Base URLs for documentation
TDK_DOC_BASE = (
    "https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no="
)

TDK_SYMBOLS_SPECS = {
    "C1005X7S1A": SeriesSpec(
        manufacturer="TDK",
        mpn_prefix="C1005X7S1A",
        value_range={"X7S": (0.33e-6, 2.2e-6)},
        tolerance_map={"X7S": {"K": "10%"}},
        mpn_sufix=["050BC"],
        footprint="capacitor_footprints:C_0402_1005Metric",
        voltage_rating="10V",
        case_code_in="0402",
        case_code_mm="1005",
        excluded_values={0.39e-6, 0.56e-6, 0.82e-6, 1.2e-6, 1.8e-6},
        datasheet_url=f"{TDK_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "C1005X6S1C": SeriesSpec(
        manufacturer="TDK",
        mpn_prefix="C1005X6S1C",
        value_range={"X7S": (1e-6, 1e-6)},
        tolerance_map={"X7S": {"K": "10%"}},
        mpn_sufix=["050BC"],
        footprint="capacitor_footprints:C_0402_1005Metric",
        voltage_rating="16V",
        case_code_in="0402",
        case_code_mm="1005",
        datasheet_url=f"{TDK_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "C1005X7S2A": SeriesSpec(
        manufacturer="TDK",
        mpn_prefix="C1005X7S2A",
        value_range={"X7S": (1e-9, 10e-9)},
        specified_values=[1e-9, 2.2e-9, 4.7e-9, 10e-9],
        tolerance_map={"X7S": {"K": "10%"}},
        mpn_sufix=["050BB"],
        footprint="capacitor_footprints:C_0402_1005Metric",
        voltage_rating="100V",
        case_code_in="0402",
        case_code_mm="1005",
        datasheet_url=f"{TDK_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "C1608X7S1A": SeriesSpec(
        manufacturer="TDK",
        mpn_prefix="C1608X7S1A",
        value_range={"X7S": (2.2e-6, 4.7e-6)},
        tolerance_map={"X7S": {"K": "10%"}},
        mpn_sufix=["080AC"],
        footprint="capacitor_footprints:C_0603_1608Metric",
        voltage_rating="10V",
        case_code_in="0603",
        case_code_mm="1608",
        specified_values=[2.2e-6, 4.7e-6],
        datasheet_url=f"{TDK_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "C1608X5R1C": SeriesSpec(
        manufacturer="TDK",
        mpn_prefix="C1608X5R1C",
        value_range={"X5R": (10e-6, 10e-6)},
        tolerance_map={"X5R": {"M": "20%"}},
        mpn_sufix=["080AB"],
        footprint="capacitor_footprints:C_0603_1608Metric",
        voltage_rating="16V",
        case_code_in="0603",
        case_code_mm="1608",
        datasheet_url=f"{TDK_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "C2012X5R1C": SeriesSpec(
        manufacturer="TDK",
        mpn_prefix="C2012X5R1C",
        value_range={"X5R": (22e-6, 22e-6)},
        tolerance_map={"X5R": {"M": "20%"}},
        mpn_sufix=["125AC"],
        footprint="capacitor_footprints:C_0805_2012Metric",
        voltage_rating="16V",
        case_code_in="0805",
        case_code_mm="2012",
        datasheet_url=f"{TDK_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "CGA4J1X7R2A": SeriesSpec(
        manufacturer="TDK",
        mpn_prefix="CGA4J1X7R2A",
        value_range={"X7R": (2.2e-6, 2.2e-6)},
        tolerance_map={"X7R": {"K": "10%"}},
        mpn_sufix=["125AC"],
        footprint="capacitor_footprints:C_0805_2012Metric",
        voltage_rating="100V",
        case_code_in="0805",
        case_code_mm="2012",
        datasheet_url=f"{TDK_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "C1608X7S2A": SeriesSpec(
        manufacturer="TDK",
        mpn_prefix="C1608X7S2A",
        value_range={"X7S": (47e-9, 100e-9)},
        tolerance_map={"X7S": {"K": "10%"}},
        mpn_sufix=["080AB"],
        footprint="capacitor_footprints:C_0603_1608Metric",
        voltage_rating="100V",
        case_code_in="0603",
        case_code_mm="1608",
        specified_values=[47e-9, 100e-9],
        datasheet_url=f"{TDK_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "C2012X7S1A": SeriesSpec(
        manufacturer="TDK",
        mpn_prefix="C2012X7S1A",
        value_range={"X7S": (15e-6, 22e-6)},
        tolerance_map={"X7S": {"M": "20%"}},
        mpn_sufix=["125AC"],
        footprint="capacitor_footprints:C_0805_2012Metric",
        voltage_rating="10V",
        case_code_in="0805",
        case_code_mm="2012",
        excluded_values={18e-6},
        datasheet_url=f"{TDK_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "CGA2B2NP02A": SeriesSpec(
        manufacturer="TDK",
        mpn_prefix="CGA2B2NP02A",
        value_range={"C0G (NP0)": (100e-12, 470e-12)},
        tolerance_map={"C0G (NP0)": {"J": "5%"}},
        mpn_sufix=["050BA"],
        footprint="capacitor_footprints:C_0402_1005Metric",
        voltage_rating="100V",
        case_code_in="0402",
        case_code_mm="1005",
        datasheet_url=f"{TDK_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "CGA3E2X7R2A": SeriesSpec(
        manufacturer="TDK",
        mpn_prefix="CGA3E2X7R2A",
        value_range={"X7R": (1e-9, 22e-9)},
        excluded_values={
            *[1.2e-9, 1.5e-9, 1.8e-9, 2.7e-9, 3.3e-9, 3.9e-9],
            *[5.6e-9, 6.8e-9, 8.2e-9, 12e-9, 15e-9, 18e-9],
        },
        tolerance_map={"X7R": {"M": "20%"}},
        mpn_sufix=["080AA"],
        footprint="capacitor_footprints:C_0603_1608Metric",
        voltage_rating="100V",
        case_code_in="0603",
        case_code_mm="1608",
        datasheet_url=f"{TDK_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "CGA4J1X7R1V": SeriesSpec(
        manufacturer="TDK",
        mpn_prefix="CGA4J1X7R1V",
        value_range={"X7R": (1.5e-6, 4.7e-6)},
        excluded_values=[1.8e-6, 2.7e-6, 3.9e-6],
        tolerance_map={"X7R": {"K": "10%"}},
        mpn_sufix=["125AC"],
        footprint="capacitor_footprints:C_0805_2012Metric",
        voltage_rating="35V",
        case_code_in="0805",
        case_code_mm="2012",
        datasheet_url=f"{TDK_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "C1005X5R1V": SeriesSpec(
        manufacturer="TDK",
        mpn_prefix="C1005X5R1V",
        value_range={"X5R": (1.5e-6, 2.2e-6)},
        tolerance_map={"X5R": {"M": "20%"}},
        mpn_sufix=["050BC"],
        footprint="capacitor_footprints:C_0603_1608Metric",
        voltage_rating="35V",
        case_code_in="0603",
        case_code_mm="1608",
        specified_values=[1.5e-6, 2.2e-6],
        datasheet_url=f"{TDK_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "C3216X5R1E": SeriesSpec(
        manufacturer="TDK",
        mpn_prefix="C3216X5R1E",
        value_range={"X5R": (15e-6, 47e-6)},
        tolerance_map={"X5R": {"M": "20%"}},
        mpn_sufix=["160AB"],
        value_based_mpn_sufix_map={
            (15e-6, 22e-6): "160AB",
            (33e-6, 47e-6): "160AC",
        },
        footprint="capacitor_footprints:C_1206_3216Metric",
        voltage_rating="25V",
        case_code_in="1206",
        case_code_mm="3216",
        specified_values=[15e-6, 22e-6, 33e-6, 47e-6],
        datasheet_url=f"{TDK_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "C1005X5R1E": SeriesSpec(
        manufacturer="TDK",
        mpn_prefix="C1005X5R1E",
        value_range={"X5R": (10e-9, 47e-6)},
        tolerance_map={"X5R": {"K": "10%"}},
        mpn_sufix=["050BA"],
        value_based_mpn_sufix_map={
            (100e-9, 220e-9, 680e-9, 1e-6, 1.5e-6, 2.2e-6): "050BC",
            (330e-9, 470e-9): "050BB",
        },
        footprint="capacitor_footprints:C_0402_1005Metric",
        voltage_rating="25V",
        case_code_in="0402",
        case_code_mm="1005",
        specified_values=[
            *[10e-9, 22e-9, 47e-9, 100e-9, 220e-9, 330e-9],
            *[470e-9, 680e-9, 1e-6, 1.5e-6, 2.2e-6],
        ],
        datasheet_url=f"{TDK_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
}

# Base URLs for documentation
VISHAY_DOC_BASE = "https://www.vishay.com/docs/45199/vjcommercialseries.pdf"

VISHAY_SYMBOLS_SPECS = {
    "VJ0603Y": SeriesSpec(
        mpn_prefix="VJ0603Y",
        manufacturer="Vishay",
        footprint="capacitor_footprints:C_0603_1608Metric",
        voltage_rating="100V",
        case_code_in="0603",
        case_code_mm="1608",
        mpn_sufix=["XBAC"],
        tolerance_map={"X7R": {"K": "10%"}},
        value_range={"X7R": (0.33e-9, 39e-9)},
        dielectric_code={"X7R": "B"},
        datasheet_url=f"{VISHAY_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search/CL31",
    ),
}

# Base URLs for documentation
KEMET_DOC_BASE = "https://www.kemet.com/en/us/search.html?q="

KEMET_SYMBOLS_SPECS = {
    "C0805C": SeriesSpec(
        mpn_prefix="C0805C",
        manufacturer="Kemet",
        footprint="capacitor_footprints:C_0805_2012Metric",
        voltage_rating="100V",
        case_code_in="0805",
        case_code_mm="2012",
        mpn_sufix=["1RACTU"],
        tolerance_map={"X7R": {"J": "5%"}},
        value_range={"X7R": (220e-9, 220e-9)},
        datasheet_url=f"{KEMET_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "C1812C": SeriesSpec(
        mpn_prefix="C1812C",
        manufacturer="Kemet",
        footprint="capacitor_footprints:C_1812_4532Metric",
        voltage_rating="3kV",
        case_code_in="1812",
        case_code_mm="4532",
        mpn_sufix=["HGACTU"],
        tolerance_map={"C0G (NP0)": {"J": "5%"}},
        value_range={"C0G (NP0)": (10e-12, 330e-12)},
        specified_values=[10e-12, 100e-12, 120e-12, 150e-12, 330e-12],
        datasheet_url=f"{KEMET_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "C1206R": SeriesSpec(
        mpn_prefix="C1206R",
        manufacturer="Kemet",
        footprint="capacitor_footprints:C_1206_3216Metric",
        voltage_rating="25V",
        case_code_in="1206",
        case_code_mm="3216",
        mpn_sufix=["3RAC7800"],
        tolerance_map={"X7R": {"K": "10%"}},
        value_range={"X7R": (1e-6, 1e-6)},
        datasheet_url=f"{KEMET_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "C1210C": SeriesSpec(
        mpn_prefix="C1210C",
        manufacturer="Kemet",
        footprint="capacitor_footprints:C_1210_140_3225Metric",
        voltage_rating="1.5kV",
        case_code_in="1210_140",
        case_code_mm="3225",
        mpn_sufix=["FRACAUTO"],
        tolerance_map={"X7R": {"K": "10%"}},
        value_range={"X7R": (4.7e-9, 39e-9)},
        specified_values=[4.7e-9, 10e-9, 33e-9, 39e-9],
        datasheet_url=f"{KEMET_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "A768KE336M1HLAE042": SeriesSpec(
        mpn_prefix="A768KE336M1HLAE042",
        manufacturer="Kemet",
        footprint="capacitor_footprints:C_034x0263_8_0x6_7Metric",
        voltage_rating="50V",
        capacitor_type="Polymer",
        case_code_in="034x0263",
        case_code_mm="8_0x6_7",
        tolerance_map={"Polymer": {"": "20%"}},
        value_range={"Polymer": (33e-6, 33e-6)},
        datasheet_url=f"{KEMET_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
}

# Base URLs for documentation
KYOCERA_AVX_DOC_BASE = "https://datasheets.kyocera-avx.com/KGM_X7R.pdf"

KYOCERA_AVX_SYMBOLS_SPECS = {
    "KGM31BR71H": SeriesSpec(
        mpn_prefix="KGM31BR71H",
        mpn_sufix=["KT"],
        manufacturer="KYOCERA AVX",
        footprint="capacitor_footprints:C_1206_3216Metric",
        voltage_rating="50V",
        case_code_in="1206",
        case_code_mm="3216",
        tolerance_map={"X7R": {"K": "10%"}},
        value_range={"X7R": (220e-12, 10e-6)},
        specified_values=[
            *[220e-12, 330e-12, 470e-12, 680e-12, 1e-9, 1.5e-9, 2.2e-9],
            *[3.3e-9, 3.9e-9, 4.7e-9, 5.6e-9, 6.8e-9, 10e-9, 12e-9, 15e-9],
            *[18e-9, 22e-9, 27e-9, 33e-9, 39e-9, 47e-9, 68e-9, 82e-9, 100e-9],
            *[120e-9],
        ],
        datasheet_url=f"{KYOCERA_AVX_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "KGM31HR71H": SeriesSpec(
        mpn_prefix="KGM31HR71H",
        mpn_sufix=["KU"],
        manufacturer="KYOCERA AVX",
        footprint="capacitor_footprints:C_1206_3216Metric",
        voltage_rating="50V",
        case_code_in="1206",
        case_code_mm="3216",
        tolerance_map={"X7R": {"K": "10%"}},
        value_range={"X7R": (220e-12, 10e-6)},
        specified_values=[470e-9, 680e-9, 1e-6, 2.2e-6, 4.7e-6, 10e-6],
        datasheet_url=f"{KYOCERA_AVX_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "KGM05AR71C": SeriesSpec(
        mpn_prefix="KGM05AR71C",
        mpn_sufix=["KH"],
        manufacturer="KYOCERA AVX",
        footprint="capacitor_footprints:C_0402_1005Metric",
        voltage_rating="16V",
        case_code_in="0402",
        case_code_mm="1005",
        tolerance_map={"X7R": {"K": "10%"}},
        value_range={"X7R": (100e-12, 220e-9)},
        excluded_values=[
            *[120e-12, 180e-12, 270e-12, 390e-12, 560e-12, 820e-12],
            *[1.2e-9, 1.8e-9, 2.7e-9, 3.3e-9, 8.2e-9],
            *[56e-9, 68e-9, 120e-9, 150e-9, 180e-9],
        ],
        datasheet_url=f"{KYOCERA_AVX_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
}

# Base URLs for documentation
WURTH_ELEKTRONIK_DOC_BASE = (
    "https://www.we-online.com/components/products/datasheet/885012208119.pdf"
)

WURTH_ELEKTRONIK_SYMBOLS_SPECS = {
    "885012208119": SeriesSpec(
        mpn_prefix="885012208119",
        mpn_sufix="",
        manufacturer="Wurth Elektronik",
        footprint="capacitor_footprints:C_1206_3216Metric",
        voltage_rating="100V",
        case_code_in="1206",
        case_code_mm="3216",
        tolerance_map={"X7R": {"": "10%"}},
        value_range={"X7R": (150e-9, 150e-9)},
        datasheet_url=f"{WURTH_ELEKTRONIK_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "851617031001": SeriesSpec(
        mpn_prefix="851617031001",
        mpn_sufix="",
        manufacturer="Wurth Elektronik",
        footprint="capacitor_footprints:C_138x315_3_5x8Metric",
        voltage_rating="2.7V",
        capacitor_type="Supercapacitor",
        case_code_in="138x315",
        case_code_mm="3_5x8",
        tolerance_map={"Supercapacitor": {"": "10%"}},
        value_range={"Supercapacitor": (1, 100)},
        specified_values=[100],
        datasheet_url=(
            "https://www.we-online.com/components/products/datasheet/"
            "851617031001.pdf"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search",
        value_based_mpn_prefix_map={(100,): "HV1860-2R7"},
        value_footprints={
            100: "capacitor_footprints:C_22x45_10x10Metric",
        },
        value_case_codes_in={100: "22x45"},
        value_case_codes_mm={100: "7_5x18"},
        value_3d_models={100: "capacitor_3d_models:C_22x45_H10"},
    ),
    "851617034001": SeriesSpec(
        mpn_prefix="851617034001",
        mpn_sufix="",
        manufacturer="Wurth Elektronik",
        footprint="capacitor_footprints:C_138x315_3_5x8Metric",
        voltage_rating="2.7V",
        capacitor_type="Supercapacitor",
        case_code_in="138x315",
        case_code_mm="3_5x8",
        tolerance_map={"Supercapacitor": {"": "10%"}},
        value_range={"Supercapacitor": (1, 300)},
        specified_values=[300],
        datasheet_url=(
            "https://www.we-online.com/components/products/datasheet/"
            "851617034001.pdf"
        ),
        trustedparts_url="https://www.trustedparts.com/en/search",
        value_based_mpn_prefix_map={(300,): "HV1860-2R7"},
        value_footprints={
            300: "capacitor_footprints:C_35X61_10x10Metric",
        },
        value_case_codes_in={300: "35X61"},
        value_case_codes_mm={300: "7_5x18"},
        value_3d_models={300: "capacitor_3d_models:C_35X61_H24_3"},
    ),
}

# Base URLs for documentation
PANASONIC_DOC_BASE = (
    "https://industrial.panasonic.com/cdbs/www-data/pdf/AAB8000/"
    "AAB8000C226.pdf"
)

PANASONIC_SYMBOLS_SPECS = {
    "35SVPK330M": SeriesSpec(
        mpn_prefix="35SVPK330M",
        manufacturer="Panasonic",
        footprint="capacitor_footprints:C_039x0496_10_0x12_6Metric",
        voltage_rating="35V",
        capacitor_type="Polymer",
        case_code_in="039x0496",
        case_code_mm="10_0x12_6",
        tolerance_map={"Polymer": {"": "20%"}},
        value_range={"Polymer": (330e-6, 330e-6)},
        datasheet_url=f"{PANASONIC_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "50SVPK10M": SeriesSpec(
        mpn_prefix="50SVPK10M",
        mpn_sufix="",
        manufacturer="Panasonic",
        footprint="capacitor_footprints:C_023x0196_5_9x5_0Metric",
        voltage_rating="50V",
        capacitor_type="Polymer",
        case_code_in="023x0196",
        case_code_mm="5_9x5_0",
        tolerance_map={"Polymer": {"": "20%"}},
        value_range={"Polymer": (10e-6, 10e-6)},
        datasheet_url=f"{PANASONIC_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "50SVPK22M": SeriesSpec(
        mpn_prefix="50SVPK22M",
        mpn_sufix="",
        manufacturer="Panasonic",
        footprint="capacitor_footprints:C_023x0248_5_9x6_3Metric",
        voltage_rating="50V",
        capacitor_type="Polymer",
        case_code_in="023x0248",
        case_code_mm="5_9x6_3",
        tolerance_map={"Polymer": {"": "20%"}},
        value_range={"Polymer": (22e-6, 22e-6)},
        datasheet_url=f"{PANASONIC_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "50SVPK33M": SeriesSpec(
        mpn_prefix="50SVPK33M",
        manufacturer="Panasonic",
        footprint="capacitor_footprints:C_027x0314_6_9x8_0Metric",
        voltage_rating="50V",
        capacitor_type="Polymer",
        case_code_in="027x0314",
        case_code_mm="6_9x8_0",
        tolerance_map={"Polymer": {"": "20%"}},
        value_range={"Polymer": (33e-6, 33e-6)},
        datasheet_url=f"{PANASONIC_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "50SVPK68M": SeriesSpec(
        mpn_prefix="50SVPK68M",
        manufacturer="Panasonic",
        footprint="capacitor_footprints:C_031x0468_8_0x11_9Metric",
        voltage_rating="50V",
        capacitor_type="Polymer",
        case_code_in="031x0468",
        case_code_mm="8_0x11_9",
        tolerance_map={"Polymer": {"": "20%"}},
        value_range={"Polymer": (68e-6, 68e-6)},
        datasheet_url=f"{PANASONIC_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "50SVPK120M": SeriesSpec(
        mpn_prefix="50SVPK120M",
        manufacturer="Panasonic",
        footprint="capacitor_footprints:C_039x0496_10_0x12_6Metric",
        voltage_rating="50V",
        capacitor_type="Polymer",
        case_code_in="039x0496",
        case_code_mm="10_0x12_6",
        tolerance_map={"Polymer": {"": "20%"}},
        value_range={"Polymer": (120e-6, 120e-6)},
        datasheet_url=f"{PANASONIC_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
}

# Base URLs for documentation
CHEMI_CON_DOC_BASE = (
    "https://www.chemi-con.co.jp/products/relatedfiles/"
    "capacitor/catalog/NTFNL-e.PDF"
)

CHEMI_CON_SYMBOLS_SPECS = {
    "KTS350B": SeriesSpec(
        manufacturer="Chemi-Con",
        mpn_prefix="KTS350B",
        value_range={"X7R": (47e-6, 47e-6)},
        tolerance_map={"X7R": {"K": "10%"}},
        characteristic_codes={0: ""},
        mpn_sufix=["76N0T00"],
        footprint="capacitor_footprints:C_3025_400_7563Metric",
        voltage_rating="35V",
        case_code_in="3025_400",
        case_code_mm="7563",
        datasheet_url=f"{CHEMI_CON_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
}


EATON_ELECTRONICS_DOC_BASE = (
    "https://www.eaton.com/content/dam/eaton/"
    "products/electronic-components/resources/data-sheet/"
    "eaton-hv-supercapacitors-cylindrical-cells-data-sheet.pdf"
)

EATON_ELECTRONICS_SYMBOLS_SPECS = {
    "HV": SeriesSpec(
        mpn_prefix="HV0810-2R7",
        manufacturer="Eaton Electronics",
        footprint="capacitor_footprints:C_138x315_3_5x8Metric",
        voltage_rating="2.7V",
        capacitor_type="Supercapacitor",
        case_code_in="138x315",
        case_code_mm="3_5x8",
        tolerance_map={"Supercapacitor": {"": "10%"}},
        value_range={"Supercapacitor": (1, 100)},
        specified_values=[1, 3, 5, 6, 10, 15, 25, 35, 60, 100],
        additional_values=[3, 5, 6, 25, 35, 60],
        value_based_mpn_prefix_map={
            (1,): "HV0810-2R7",
            (3,): "HV0820-2R7",
            (5,): "HV1020-2R7",
            (6,): "HV0830-2R7",
            (10,): "HV1030-2R7",
            (15,): "HV1325-2R7",
            (25,): "HV1625-2R7",
            (35,): "HV1245-2R7",
            (60,): "HV1840-2R7",
            (100,): "HV1860-2R7",
        },
        value_footprints={
            1: "capacitor_footprints:C_138x315_H13_5_3_5x8Metric",
            3: "capacitor_footprints:C_138x315_H21_3_5x8Metric",
            5: "capacitor_footprints:C_197x394_H22_3_5_0x10Metric",
            6: "capacitor_footprints:C_138x315_H31_3_5x8Metric",
            10: "capacitor_footprints:C_197x394_H31_5_5_0x10Metric",
            15: "capacitor_footprints:C_197x512_H28_4_5_0x10Metric",
            25: "capacitor_footprints:C_295x630_H28_4_5_0x10Metric",
            35: "capacitor_footprints:C_197x492_H49_5_0x12_5Metric",
            60: "capacitor_footprints:C_295x709_H42_5_0x10Metric",
            100: "capacitor_footprints:C_295x709_H60_5_5_0x10Metric",
        },
        value_case_codes_in={
            1: "138x315_H13_5",
            3: "138x315_H21",
            5: "197x394_H22_3",
            6: "138x315_H31",
            10: "197x394_H31_5",
            15: "197x512_H28_4",
            25: "295x630_H28_4",
            35: "197x492_H49",
            60: "295x709_H42",
            100: "295x709_H60_5",
        },
        value_case_codes_mm={
            1: "3_5x8",
            3: "3_5x8",
            5: "5_0x10",
            6: "3_5x8",
            10: "5_0x10",
            15: "5_0x13",
            25: "7_5x16",
            35: "5_0x12_5",
            60: "7_5x18",
            100: "7_5x18",
        },
        value_3d_models={
            1: "capacitor_3d_models:C_138x315_H13_5",
            3: "capacitor_3d_models:C_138x315_H21",
            5: "capacitor_3d_models:C_197x394_H22_3",
            6: "capacitor_3d_models:C_138x315_H31",
            10: "capacitor_3d_models:C_197x394_H31_5",
            15: "capacitor_3d_models:C_197x512_H28_4",
            25: "capacitor_3d_models:C_295x630_H28_4",
            35: "capacitor_3d_models:C_197x492_H49",
            60: "capacitor_3d_models:C_295x709_H42",
            100: "capacitor_3d_models:C_295x709_H60_5",
        },
        datasheet_url=f"{EATON_ELECTRONICS_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
}

# Combined specifications dictionary
SERIES_SPECS: Final[dict[str, SeriesSpec]] = {
    **MURATA_SYMBOLS_SPECS,
    **SAMSUNG_SYMBOLS_SPECS,
    **TDK_SYMBOLS_SPECS,
    **VISHAY_SYMBOLS_SPECS,
    **KEMET_SYMBOLS_SPECS,
    **WURTH_ELEKTRONIK_SYMBOLS_SPECS,
    **PANASONIC_SYMBOLS_SPECS,
    **CHEMI_CON_SYMBOLS_SPECS,
    **KYOCERA_AVX_SYMBOLS_SPECS,
    **YAGEO_SYMBOLS_SPECS,
    **EATON_ELECTRONICS_SYMBOLS_SPECS,
}
