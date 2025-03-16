"""Library for managing transistor specifications.

This module provides data structures and definitions for various transistor
series, including their specifications and individual component
information.
"""

from typing import NamedTuple

from utilities import print_message_utilities


class SeriesSpec(NamedTuple):
    """Transistor series specifications structure for individual transistors.

    Attributes:
        manufacturer: The manufacturer of the transistor.
        base_series: The base series name of the transistor.
        footprint: The KiCad footprint name for the transistor.
        datasheet: The URL of the datasheet for the transistor.
        drain_source_voltage: A list of drain-source voltage ratings.
        trustedparts_link: The URL of the TrustedParts website.
        drain_current: A list of drain current ratings.
        package: The package type of the transistor.
        transistor_type: The type of transistor (e.g., N-Channel, P-Channel).
        reference: The reference designator prefix for the transistor.

    """

    manufacturer: str
    base_series: str
    footprint: str
    datasheet: str
    drain_source_voltage: list[float]
    trustedparts_link: str
    drain_current: list[float]
    package: str
    transistor_type: str
    reference: str = "Q"


class PartInfo(NamedTuple):
    """Transistor component information structure.

    Attributes:
        symbol_name: The name of the KiCad symbol for the transistor.
        reference: The reference designator prefix for the transistor.
        value: The voltage rating of the transistor.
        footprint: The KiCad footprint name for the transistor.
        datasheet: The URL of the datasheet for the transistor.
        description: A descriptive string for the transistor component.
        manufacturer: The manufacturer of the transistor.
        mpn: The manufacturer part number of the transistor.
        series: The base series name of the transistor.
        trustedparts_link: The URL of the TrustedParts website.
        drain_current: The drain current rating of the transistor.
        package: The package type of the transistor.
        transistor_type: The type of transistor (e.g., N-Channel, P-Channel).
        step_file_viewer_link: URL to 3D model viewer for the component model

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
    drain_current: float
    package: str
    transistor_type: str
    step_file_viewer_link: str

    @classmethod
    def create_description(cls, value: float) -> str:
        """Create a description string for a transistor component.

        Args:
            value: The voltage rating of the transistor.

        Returns:
            A descriptive string for the transistor component

        """
        parts = ["Transistor", f"{value} V"]
        return " ".join(parts)

    @classmethod
    def create_part_info(
        cls,
        value: float,
        specs: SeriesSpec,
    ) -> "PartInfo":
        """Create a PartInfo instance for a transistor component.

        Args:
            value: The voltage rating of the transistor.
            specs: Series specifications for the transistor.

        Returns:
            A PartInfo instance for the transistor component

        """
        # Construct MPN with optional suffix
        mpn = f"{specs.base_series}"

        trustedparts_link = f"{specs.trustedparts_link}/{mpn}"

        try:
            index = specs.drain_source_voltage.index(value)
            drain_current = float(specs.drain_current[index])
        except ValueError:
            print_message_utilities.print_error(
                f"Error: value {value} V "
                f"not found in series {specs.base_series}",
            )
            drain_current = 0.0
        except IndexError:
            print_message_utilities.print_error(
                "Error: No DC specifications found for value "
                f"{value} V in series {specs.base_series}",
            )
            drain_current = 0.0

        viewer_3d_link = (
            "https://3dviewer.net/index.html#model="
            "https://github.com/ionutms/"
            "KiCAD_Symbols_Generator/blob/main/3D_models/"
            f"{specs.footprint.split(':')[-1]}.step"
        )

        return cls(
            symbol_name=f"{specs.reference}_{mpn}",
            reference=specs.reference,
            value=value,
            footprint=specs.footprint,
            datasheet=specs.datasheet,
            description=cls.create_description(value),
            manufacturer=specs.manufacturer,
            mpn=mpn,
            package=specs.package,
            series=specs.base_series,
            trustedparts_link=trustedparts_link,
            drain_current=drain_current,
            transistor_type=specs.transistor_type,
            step_file_viewer_link=viewer_3d_link,
        )

    @classmethod
    def generate_part_numbers(
        cls,
        specs: SeriesSpec,
    ) -> list["PartInfo"]:
        """Generate PartInfo instances for all transistor components.

        Args:
            specs: Series specifications for the transistor.

        Returns:
            A list of PartInfo instances for the transistor components.

        """
        return [
            cls.create_part_info(value, specs)
            for value in specs.drain_source_voltage
            if cls.create_part_info(value, specs) is not None
        ]


SYMBOLS_SPECS: dict[str, SeriesSpec] = {
    "SI7309DN-T1-GE3": SeriesSpec(
        manufacturer="Vishay Semiconductors",
        base_series="SI7309DN-T1-GE3",
        footprint="transistor_footprints:PowerPAK 1212-8",
        datasheet="https://www.vishay.com/docs/73434/si7309dn.pdf",
        drain_source_voltage=[-60.0],
        drain_current=[-8.0],
        package="PowerPAK 1212-8",
        transistor_type="P-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "PSMN040-100MSEX": SeriesSpec(
        manufacturer="Nexperia",
        base_series="PSMN040-100MSEX",
        footprint="transistor_footprints:LFPAK33-8",
        datasheet=(
            "https://assets.nexperia.com/documents/data-sheet/"
            "PSMN040-100MSE.pdf"
        ),
        drain_source_voltage=[100.0],
        drain_current=[30],
        package="LFPAK33-8",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BUK9M34-100EX": SeriesSpec(
        manufacturer="Nexperia",
        base_series="BUK9M34-100EX",
        footprint="transistor_footprints:LFPAK33-8",
        datasheet=(
            "https://assets.nexperia.com/documents/data-sheet/"
            "BUK9M34-100E.pdf"
        ),
        drain_source_voltage=[100.0],
        drain_current=[29],
        package="LFPAK33-8",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BUK9M43-100EX": SeriesSpec(
        manufacturer="Nexperia",
        base_series="BUK9M43-100EX",
        footprint="transistor_footprints:LFPAK33-8",
        datasheet=(
            "https://assets.nexperia.com/documents/data-sheet/"
            "BUK9M43-100E.pdf"
        ),
        drain_source_voltage=[100.0],
        drain_current=[25],
        package="LFPAK33-8",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "PSMN075-100MSEX": SeriesSpec(
        manufacturer="Nexperia",
        base_series="PSMN075-100MSEX",
        footprint="transistor_footprints:LFPAK33-8",
        datasheet=(
            "https://assets.nexperia.com/documents/data-sheet/"
            "PSMN075-100MSE.pdf"
        ),
        drain_source_voltage=[100.0],
        drain_current=[18],
        package="LFPAK33-8",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BUK9M120-100EX": SeriesSpec(
        manufacturer="Nexperia",
        base_series="BUK9M120-100EX",
        footprint="transistor_footprints:LFPAK33-8",
        datasheet=(
            "https://assets.nexperia.com/documents/data-sheet/"
            "BUK9M120-100E.pdf"
        ),
        drain_source_voltage=[100.0],
        drain_current=[11.5],
        package="LFPAK33-8",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BUK9M156-100EX": SeriesSpec(
        manufacturer="Nexperia",
        base_series="BUK9M156-100EX",
        footprint="transistor_footprints:LFPAK33-8",
        datasheet=(
            "https://assets.nexperia.com/documents/data-sheet/"
            "BUK9M156-100E.pdf"
        ),
        drain_source_voltage=[100.0],
        drain_current=[9.3],
        package="LFPAK33-8",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BUK9K29-100E": SeriesSpec(
        manufacturer="Nexperia",
        base_series="BUK9K29-100E",
        footprint="transistor_footprints:LFPAK56D-8",
        datasheet=(
            "https://assets.nexperia.com/documents/data-sheet/"
            "BUK9K29-100E.pdf"
        ),
        drain_source_voltage=[100],
        drain_current=[30],
        package="LFPAK56D-8",
        transistor_type="N-Channel Dual",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "SI7997DP-T1-GE3": SeriesSpec(
        manufacturer="Vishay Semiconductors",
        base_series="SI7997DP-T1-GE3",
        footprint="transistor_footprints:PowerPAK SO-8",
        datasheet=("https://www.vishay.com/docs/66719/si7997dp.pdf"),
        drain_source_voltage=[-30],
        drain_current=[-60],
        package="PowerPAK SO-8",
        transistor_type="P-Channel Dual",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "ZXMP6A17E6TA": SeriesSpec(
        manufacturer="Diodes Incorporated",
        base_series="ZXMP6A17E6TA",
        footprint="transistor_footprints:SOT-26",
        datasheet=("https://www.diodes.com/assets/Datasheets/ZXMP6A17E6.pdf"),
        drain_source_voltage=[-60],
        drain_current=[-3],
        package="SOT-26",
        transistor_type="P-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BSS123WQ-7-F": SeriesSpec(
        manufacturer="Diodes Incorporated",
        base_series="BSS123WQ-7-F",
        footprint="transistor_footprints:SOT-323",
        datasheet=("https://www.diodes.com/assets/Datasheets/BSS123WQ.pdf"),
        drain_source_voltage=[100],
        drain_current=[0.17],
        package="SOT-323",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "NVMFS5C460NLWFAFT1G": SeriesSpec(
        manufacturer="Onsemi",
        base_series="NVMFS5C460NLWFAFT1G",
        footprint="transistor_footprints:SO-8FL",
        datasheet=("https://www.onsemi.com/pdf/datasheet/nvmfs5c460nl-d.pdf"),
        drain_source_voltage=[40.0],
        drain_current=[78],
        package="SO-8FL",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
}
