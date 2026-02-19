"""Library for managing transistor specifications.

This module provides data structures and definitions for various transistor
series, including their specifications and individual component
information.
"""

from typing import NamedTuple, Optional

from utilities import print_message_utilities


class SeriesSpec(NamedTuple):
    """Transistor series specifications structure for individual transistors.

    Attributes:
        manufacturer: The manufacturer of the transistor.
        base_series: The base series name of the transistor.
        footprint: The KiCad footprint name for the transistor.
        datasheet: The URL of the datasheet for the transistor.
        trustedparts_link: The URL of the TrustedParts website.
        package: The package type of the transistor.
        transistor_type: The type of transistor (e.g., N-Channel, P-Channel).
        drain_source_voltage: A list of drain-source voltage ratings.
        drain_current: A list of drain current ratings.
        collector_emitter_voltage:
            A list of collector-emitter voltage ratings.
        collector_current: A list of collector current ratings.
        reference: The reference designator prefix for the transistor.

    """

    manufacturer: str
    base_series: str
    footprint: str
    datasheet: str
    trustedparts_link: str
    package: str
    transistor_type: str
    drain_source_voltage: Optional[list[float]] = None
    drain_current: Optional[list[float]] = None
    collector_emitter_voltage: Optional[list[float]] = None
    collector_current: Optional[list[float]] = None
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
        collector_current: The collector current rating of the transistor.
        package: The package type of the transistor.
        transistor_type: The type of transistor (e.g., N-Channel, P-Channel).

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
    collector_current: float
    package: str
    transistor_type: str

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

        # Initialize both drain and collector currents to 0.0
        drain_current = 0.0
        collector_current = 0.0

        # Check if it's a MOSFET or BJT and handle accordingly
        if specs.transistor_type in [
            "N-Channel",
            "P-Channel",
            "N-Channel Dual",
            "P-Channel Dual",
        ]:
            # It's a MOSFET - use drain-source voltage and drain current
            if specs.drain_source_voltage and specs.drain_current:
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
            else:
                print_message_utilities.print_error(
                    f"Error: No drain_current data available "
                    f"for MOSFET {specs.base_series}",
                )
                drain_current = 0.0
        elif specs.transistor_type in ["NPN", "PNP", "NPN/PNP"]:
            # It's a BJT - use collector-emitter voltage and collector current
            if specs.collector_emitter_voltage and specs.collector_current:
                try:
                    index = specs.collector_emitter_voltage.index(value)
                    collector_current = float(specs.collector_current[index])
                except ValueError:
                    print_message_utilities.print_error(
                        f"Error: value {value} V "
                        f"not found in series {specs.base_series}",
                    )
                    collector_current = 0.0
                except IndexError:
                    print_message_utilities.print_error(
                        "Error: No collector current specifications found "
                        f"for value {value} V in series {specs.base_series}",
                    )
                    collector_current = 0.0
            else:
                print_message_utilities.print_error(
                    f"Error: No collector current data available for BJT "
                    f"{specs.base_series}",
                )
                collector_current = 0.0
        else:
            # Default to MOSFET behavior for unknown types
            if specs.drain_source_voltage and specs.drain_current:
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
            else:
                drain_current = 0.0

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
            collector_current=collector_current,
            transistor_type=specs.transistor_type,
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
        # Determine which voltage list to use based on transistor type
        voltage_list = []
        if specs.transistor_type in [
            "N-Channel",
            "P-Channel",
            "N-Channel Dual",
            "P-Channel Dual",
        ]:
            # It's a MOSFET - use drain-source voltage
            if specs.drain_source_voltage:
                voltage_list = specs.drain_source_voltage
        elif specs.transistor_type in ["NPN", "PNP", "NPN/PNP"]:
            # It's a BJT - use collector-emitter voltage
            if specs.collector_emitter_voltage:
                voltage_list = specs.collector_emitter_voltage
        else:
            # For unknown types, default to drain-source voltage if available
            if specs.drain_source_voltage:
                voltage_list = specs.drain_source_voltage

        return [
            cls.create_part_info(value, specs)
            for value in voltage_list
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
    "SI7113ADN-T1-GE3": SeriesSpec(
        manufacturer="Vishay Semiconductors",
        base_series="SI7113ADN-T1-GE3",
        footprint="transistor_footprints:PowerPAK 1212-8",
        datasheet="https://www.vishay.com/docs/77678/si7113adn.pdf",
        drain_source_voltage=[-100.0],
        drain_current=[-10.8],
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
        footprint="transistor_footprints:PowerPAK SO-8 Dual",
        datasheet=("https://www.vishay.com/docs/66719/si7997dp.pdf"),
        drain_source_voltage=[-30],
        drain_current=[-60],
        package="PowerPAK SO-8 Dual",
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
    "BSS138-7-F": SeriesSpec(
        manufacturer="Diodes Incorporated",
        base_series="BSS138-7-F",
        footprint="transistor_footprints:SOT23-3",
        datasheet=("https://www.diodes.com/datasheet/download/BSS138.pdf"),
        drain_source_voltage=[50],
        drain_current=[0.2],
        package="SOT23-3",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "SIR680DP-T1-RE3": SeriesSpec(
        manufacturer="Vishay Semiconductors",
        base_series="SIR680DP-T1-RE3",
        footprint="transistor_footprints:PowerPAK SO-8 Single",
        datasheet=("https://www.vishay.com/docs/75267/sir680dp.pdf"),
        drain_source_voltage=[80],
        drain_current=[100],
        package="PowerPAK SO-8 Single",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BSC014N04LSI": SeriesSpec(
        manufacturer="Infineon Technologies",
        base_series="BSC014N04LSI",
        footprint="transistor_footprints:TDSON-8 FL",
        datasheet=(
            "https://www.infineon.com/assets/row/public/documents/24/49/"
            "infineon-bsc014n04lsi-datasheet-en.pdf"
        ),
        drain_source_voltage=[40],
        drain_current=[195],
        package="TDSON-8 FL",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "FMMT625TA": SeriesSpec(
        manufacturer="Diodes Incorporated",
        base_series="FMMT625TA",
        footprint="transistor_footprints:SOT23-3",
        datasheet=("https://www.diodes.com/assets/Datasheets/FMMT625.pdf"),
        collector_emitter_voltage=[150],
        collector_current=[1],
        package="SOT23-3",
        transistor_type="NPN",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BSZ065N06LS5ATMA1": SeriesSpec(
        manufacturer="Infineon Technologies",
        base_series="BSZ065N06LS5ATMA1",
        footprint="transistor_footprints:TSDSON-8FL",
        datasheet=(
            "https://www.infineon.com/assets/row/public/documents/24/49/"
            "infineon-bsz065n06ls5-datasheet-en.pdf?"
            "fileId=5546d4625696ed760156e55f60164817"
        ),
        drain_source_voltage=[60],
        drain_current=[65],
        package="TSDSON-8FL",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BSZ042N06NSATMA1": SeriesSpec(
        manufacturer="Infineon Technologies",
        base_series="BSZ042N06NSATMA1",
        footprint="transistor_footprints:TSDSON-8FL",
        datasheet=(
            "https://www.infineon.com/assets/row/public/documents/24/49/"
            "infineon-bsz042n06ns-datasheet-en.pdf?"
            "fileId=db3a3043345a30bc013465d4bf1862fd"
        ),
        drain_source_voltage=[60],
        drain_current=[98],
        package="TSDSON-8FL",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BSZ100N06LS3GATMA1": SeriesSpec(
        manufacturer="Infineon Technologies",
        base_series="BSZ100N06LS3GATMA1",
        footprint="transistor_footprints:TSDSON-8FL",
        datasheet=(
            "https://www.infineon.com/assets/row/public/documents/24/49/"
            "infineon-bsz100n06ls3-g-datasheet-en.pdf"
        ),
        drain_source_voltage=[60],
        drain_current=[20],
        package="TSDSON-8FL",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BSZ099N06LS5ATMA1": SeriesSpec(
        manufacturer="Infineon Technologies",
        base_series="BSZ099N06LS5ATMA1",
        footprint="transistor_footprints:TSDSON-8FL",
        datasheet=(
            "https://www.infineon.com/assets/row/public/documents/24/49/"
            "infineon-bsz099n06ls5-datasheet-en.pdf"
        ),
        drain_source_voltage=[60],
        drain_current=[40],
        package="TSDSON-8FL",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BSZ068N06NSATMA1": SeriesSpec(
        manufacturer="Infineon Technologies",
        base_series="BSZ068N06NSATMA1",
        footprint="transistor_footprints:TSDSON-8FL",
        datasheet=(
            "https://www.infineon.com/assets/row/public/documents/24/49/"
            "infineon-bsz068n06ns-datasheet-en.pdf"
        ),
        drain_source_voltage=[60],
        drain_current=[40],
        package="TSDSON-8FL",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BSZ040N06LS5ATMA1": SeriesSpec(
        manufacturer="Infineon Technologies",
        base_series="BSZ040N06LS5ATMA1",
        footprint="transistor_footprints:TSDSON-8FL",
        datasheet=(
            "https://www.infineon.com/assets/row/public/documents/24/49/"
            "infineon-bsz040n06ls5-datasheet-en.pdf"
        ),
        drain_source_voltage=[60],
        drain_current=[40],
        package="TSDSON-8FL",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BSZ042N06NS": SeriesSpec(
        manufacturer="Infineon Technologies",
        base_series="BSZ042N06NS",
        footprint="transistor_footprints:TSDSON-8FL",
        datasheet=(
            "https://www.infineon.com/assets/row/public/documents/24/49/"
            "infineon-bsz042n06ns-datasheet-en.pdf"
        ),
        drain_source_voltage=[60],
        drain_current=[98],
        package="TSDSON-8FL",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BSZ100N06NS": SeriesSpec(
        manufacturer="Infineon Technologies",
        base_series="BSZ100N06NS",
        footprint="transistor_footprints:TSDSON-8FL",
        datasheet=(
            "https://www.infineon.com/assets/row/public/documents/24/49/"
            "infineon-bsz100n06ns-datasheet-en.pdf"
        ),
        drain_source_voltage=[60],
        drain_current=[40],
        package="TSDSON-8FL",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BSZ100N06NSATMA1": SeriesSpec(
        manufacturer="Infineon Technologies",
        base_series="BSZ100N06NSATMA1",
        footprint="transistor_footprints:TSDSON-8FL",
        datasheet=(
            "https://www.infineon.com/assets/row/public/documents/24/49/"
            "infineon-bsz100n06ns-datasheet-en.pdf"
        ),
        drain_source_voltage=[60],
        drain_current=[40],
        package="TSDSON-8FL",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BSZ068N06NS": SeriesSpec(
        manufacturer="Infineon Technologies",
        base_series="BSZ068N06NS",
        footprint="transistor_footprints:TSDSON-8FL",
        datasheet=(
            "https://www.infineon.com/assets/row/public/documents/24/49/"
            "infineon-bsz068n06ns-datasheet-en.pdf"
        ),
        drain_source_voltage=[60],
        drain_current=[40],
        package="TSDSON-8FL",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BSZ031NE2LS5ATMA1": SeriesSpec(
        manufacturer="Infineon Technologies",
        base_series="BSZ031NE2LS5ATMA1",
        footprint="transistor_footprints:TSDSON-8FL",
        datasheet=(
            "https://www.infineon.com/assets/row/public/documents/24/49/"
            "infineon-bsz031ne2ls5-datasheet-en.pdf?"
            "fileId=5546d4624eeb2bc7014f17a9bb6a75fa"
        ),
        drain_source_voltage=[25],
        drain_current=[80],
        package="TSDSON-8FL",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BSZ060NE2LS": SeriesSpec(
        manufacturer="Infineon Technologies",
        base_series="BSZ060NE2LS",
        footprint="transistor_footprints:TSDSON-8FL",
        datasheet=(
            "https://www.infineon.com/assets/row/public/documents/24/49/"
            "infineon-bsz060ne2ls-datasheet-en.pdf?"
            "fileId=db3a30432ea425a4012ec927cb360e1f"
        ),
        drain_source_voltage=[20],
        drain_current=[51],
        package="TSDSON-8FL",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BC847A-AQ": SeriesSpec(
        manufacturer="Diotec Semiconductor",
        base_series="BC847A-AQ",
        footprint="transistor_footprints:SOT23",
        datasheet=("https://diotec.com/request/datasheet/bc846.pdf"),
        collector_emitter_voltage=[45],
        collector_current=[0.1],
        package="SOT23",
        transistor_type="NPN",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BC857A-AQ": SeriesSpec(
        manufacturer="Diotec Semiconductor",
        base_series="BC857A-AQ",
        footprint="transistor_footprints:SOT23",
        datasheet=("https://diotec.com/request/datasheet/bc856.pdf"),
        collector_emitter_voltage=[45],
        collector_current=[0.1],
        package="SOT23",
        transistor_type="PNP",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "DMP6350S-7": SeriesSpec(
        manufacturer="Diodes Incorporated",
        base_series="DMP6350S-7",
        footprint="transistor_footprints:SOT23",
        datasheet=(
            "https://sy-dep-epc-lpc.web.cern.ch/components/datasheets/"
            "epc-lpc%20(converters)/DMP6350S-P%20Signal%20MOSFET-"
            "Diodes%20Inc.pdf"
        ),
        drain_source_voltage=[-60],
        drain_current=[-1.2],
        package="SOT23",
        transistor_type="P-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "FMMT718TA": SeriesSpec(
        manufacturer="Diodes Incorporated",
        base_series="FMMT718TA",
        footprint="transistor_footprints:SOT23",
        datasheet=("https://www.diodes.com/assets/Datasheets/FMMT718.pdf"),
        collector_emitter_voltage=[20],
        collector_current=[1.5],
        package="SOT23",
        transistor_type="PNP",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "SIS438DN-T1-GE3": SeriesSpec(
        manufacturer="Vishay Semiconductors",
        base_series="SIS438DN-T1-GE3",
        footprint="transistor_footprints:PowerPAK 1212-8",
        datasheet="https://www.vishay.com/docs/64826/sis438dn.pdf",
        drain_source_voltage=[20.0],
        drain_current=[16],
        package="PowerPAK 1212-8",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "SI2374DS-T1-BE3": SeriesSpec(
        manufacturer="Vishay Semiconductors",
        base_series="SI2374DS-T1-BE3",
        footprint="transistor_footprints:SOT23",
        datasheet=("https://www.vishay.com/docs/62947/si2374ds.pdf"),
        drain_source_voltage=[20.0],
        drain_current=[5.9],
        package="SOT23",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "SIA436DJ-T1-GE3": SeriesSpec(
        manufacturer="Vishay Semiconductors",
        base_series="SIA436DJ-T1-GE3",
        footprint="transistor_footprints:PowerPAK SC-70",
        datasheet=("https://www.vishay.com/docs/63535/sia436dj.pdf"),
        drain_source_voltage=[8],
        drain_current=[12],
        package="PowerPAK SC-70",
        transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "MMBTA06-7-F": SeriesSpec(
        manufacturer="Diodes Incorporated",
        base_series="MMBTA06-7-F",
        footprint="transistor_footprints:SOT23-3",
        datasheet=(
            "https://4donline.ihs.com/images/VipMasterIC/IC/DIOD/"
            "DIODS20593/DIODS20593-1.pdf?hkey=CECEF36DEECDED6468708AAF2E19C0C6"
        ),
        collector_emitter_voltage=[80],
        collector_current=[0.5],
        package="SOT23-3",
        transistor_type="NPN",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
}
