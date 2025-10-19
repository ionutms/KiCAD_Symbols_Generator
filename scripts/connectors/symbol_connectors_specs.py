"""Connector Series Specifications Module.

This module defines data structures and specifications for connector series,
providing a framework for managing connector component information.
"""

from __future__ import annotations

from typing import NamedTuple


class SeriesSpec(NamedTuple):
    """Connector series specifications.

    This class defines the complete specifications for a series of connectors,
    including physical characteristics and documentation.

    Attributes:
        manufacturer: Manufacturer name
        base_series: Base series identifier
        footprint_pattern: KiCad footprint pattern string
        datasheet: URL to the manufacturer's datasheet
        pin_counts: List of available pin counts
        trustedparts_link: URL to the Trusted Parts connector listing
        color: Color of the connector housing
        pitch: Pin-to-pin spacing in millimeters
        mounting_angle: Mounting orientation of the connector
        current_rating: Maximum current rating in amperes
        voltage_rating: Maximum voltage rating in volts
        mounting_style: Method of mounting (e.g., Through Hole, SMD)
        contact_plating: Material used for contact plating
        reference: Reference designator prefix (default: "J")
        rectangle_width:
            Width of the connector symbol rectangle (default: 5.08mm)
        pin_names:
            Optional dictionary mapping pin identifiers to pin names
            (default: None)
        symbol_pin_length:
            Optional override for symbol pin length in mm (default: 2.54)

    """

    manufacturer: str
    base_series: str
    footprint_pattern: str
    datasheet: str
    pin_counts: list[int]
    trustedparts_link: str
    color: str
    pitch: float
    mounting_angle: str
    current_rating: float | str
    voltage_rating: int
    mounting_style: str
    contact_plating: str
    reference: str = "J"
    number_of_rows: int = 1
    rectangle_width: float = 5.08
    pin_names: dict[str, str] | None = None
    symbol_pin_length: float = 2.54


class PartInfo(NamedTuple):
    """Component part information structure for individual connectors.

    Attributes:
        symbol_name: KiCad symbol name
        reference: Reference designator prefix
        value: Part value (MPN)
        footprint: KiCad footprint name
        datasheet: URL to the manufacturer's datasheet
        description: Comprehensive component description
        manufacturer: Manufacturer name
        mpn: Manufacturer part number
        series: Base series identifier
        trustedparts_link: URL to the Trusted Parts connector listing
        color: Color of the connector housing
        pitch: Pin-to-pin spacing in millimeters
        pin_count: Number of pins
        mounting_angle: Mounting orientation of the connector
        current_rating: Maximum current rating in amperes
        voltage_rating: Maximum voltage rating in volts
        mounting_style: Method of mounting (e.g., Through Hole, SMD)
        contact_plating: Material used for contact plating
        rectangle_width: Width of the connector symbol rectangle

    """

    symbol_name: str
    reference: str
    value: str
    footprint: str
    datasheet: str
    description: str
    manufacturer: str
    mpn: str
    series: str
    trustedparts_link: str
    color: str
    pitch: float
    pin_count: int
    mounting_angle: str
    current_rating: float | str
    voltage_rating: int
    mounting_style: str
    contact_plating: str
    number_of_rows: int
    rectangle_width: float = 5.08

    @classmethod
    def create_part_info(
        cls,
        pin_count: int,
        specs: SeriesSpec,
    ) -> PartInfo:
        """Create complete part information.

        Args:
            pin_count: Number of pins
            specs: Series specifications

        Returns:
            PartInfo instance with all specifications

        """
        mpn = cls.generate_part_code(
            pin_count,
            specs.base_series,
            specs.manufacturer,
        )
        footprint = specs.footprint_pattern.format(pin_count)
        trustedparts_link = f"{specs.trustedparts_link}/{mpn}"

        return PartInfo(
            symbol_name=f"{specs.reference}_{mpn}",
            reference=specs.reference,
            value=mpn,
            footprint=footprint,
            datasheet=specs.datasheet,
            description=cls.create_description(pin_count, specs),
            manufacturer=specs.manufacturer,
            mpn=mpn,
            series=specs.base_series,
            trustedparts_link=trustedparts_link,
            color=specs.color,
            pitch=specs.pitch,
            pin_count=pin_count,
            mounting_angle=specs.mounting_angle,
            current_rating=specs.current_rating,
            voltage_rating=specs.voltage_rating,
            mounting_style=specs.mounting_style,
            contact_plating=specs.contact_plating,
            number_of_rows=specs.number_of_rows,
            rectangle_width=specs.rectangle_width,
        )

    @classmethod
    def generate_part_code(
        cls,
        pin_count: int,
        series_code: str,
        manufacturer: str,
    ) -> str:
        """Generate connector part code based on pin count.

        Args:
            pin_count: Number of pins
            series_code: Base series code
            manufacturer: Manufacturer Name

        Returns:
            str: Part code string

        """
        if manufacturer == "Same Sky":
            return f"{series_code}-{pin_count:02d}BE"
        # else if manufactures is Samtec
        return f"{series_code.replace('xx', f'{pin_count:02d}')}"

    @classmethod
    def create_description(
        cls,
        pin_count: int,
        specs: SeriesSpec,
    ) -> str:
        """Create component description with comprehensive specifications.

        Args:
            pin_count: Number of pins
            specs: Series specifications

        Returns:
            Formatted description string including all relevant specifications

        """
        parts = [
            f"{specs.manufacturer}",
            f"{specs.base_series} series, ",
            f"{pin_count} positions connector, ",
            f"{specs.pitch} mm pitch, ",
            f"{specs.color}, ",
            f"{specs.mounting_angle} mounting, ",
            f"{specs.current_rating} A, ",
            f"{specs.voltage_rating} V, ",
            f"{specs.mounting_style}, ",
            f"{specs.contact_plating} plated",
        ]

        return " ".join(parts)

    @classmethod
    def generate_part_numbers(
        cls,
        specs: SeriesSpec,
    ) -> list[PartInfo]:
        """Generate all part numbers for the series.

        Args:
            specs: Series specifications

        Returns:
            List of PartInfo instances

        """
        return [
            cls.create_part_info(pin_count, specs)
            for pin_count in specs.pin_counts
        ]


SYMBOLS_SPECS: dict[str, SeriesSpec] = {
    "TBP02R1-381": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TBP02R1-381",
        footprint_pattern="connector_footprints:TBP02R1-381-{:02d}BE",
        datasheet=(
            "https://www.sameskydevices.com/product/resource/tbp02r1-381.pdf"
        ),
        pin_counts=[2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16],
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Blue",
        pitch=3.81,
        mounting_angle="Vertical",
        current_rating=8.0,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin",
    ),
    "TBP02R2-381": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TBP02R2-381",
        footprint_pattern="connector_footprints:TBP02R2-381-{:02d}BE",
        datasheet=(
            "https://www.sameskydevices.com/product/resource/tbp02r2-381.pdf"
        ),
        pin_counts=[2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16],
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Blue",
        pitch=3.81,
        mounting_angle="Vertical",
        current_rating=8.0,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin",
    ),
    "TBP04R1-500": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TBP04R1-500",
        footprint_pattern="connector_footprints:TBP04R1-500-{:02d}BE",
        datasheet=(
            "https://www.sameskydevices.com/product/resource/tbp04r1-500.pdf"
        ),
        pin_counts=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Blue",
        pitch=5.00,
        mounting_angle="Vertical",
        current_rating=15.0,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin",
    ),
    "TBP04R12-500": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TBP04R12-500",
        footprint_pattern="connector_footprints:TBP04R12-500-{:02d}BE",
        datasheet=(
            "https://www.sameskydevices.com/product/resource/tbp04r12-500.pdf"
        ),
        pin_counts=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Blue",
        pitch=5.00,
        mounting_angle="Vertical",
        current_rating=15.0,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin",
    ),
    "TBP04R2-500": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TBP04R2-500",
        footprint_pattern="connector_footprints:TBP04R2-500-{:02d}BE",
        datasheet=(
            "https://www.sameskydevices.com/product/resource/tbp04r2-500.pdf"
        ),
        pin_counts=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Blue",
        pitch=5.00,
        mounting_angle="Vertical",
        current_rating=15.0,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin",
    ),
    "TBP04R3-500": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TBP04R3-500",
        footprint_pattern="connector_footprints:TBP04R3-500-{:02d}BE",
        datasheet=(
            "https://www.sameskydevices.com/product/resource/tbp04r3-500.pdf"
        ),
        pin_counts=[2, 3, 4, 5, 6],
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Blue",
        pitch=5.00,
        mounting_angle="Vertical",
        current_rating=15.0,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin",
    ),
    "TB004-508": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TB004-508",
        footprint_pattern="connector_footprints:TB004-508-{:02d}BE",
        datasheet=(
            "https://www.sameskydevices.com/product/resource/tb004-508.pdf"
        ),
        pin_counts=list(range(2, 25)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Blue",
        pitch=5.08,
        mounting_angle="Vertical",
        current_rating=16.0,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin",
    ),
    "TB006-508": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TB006-508",
        footprint_pattern="connector_footprints:TB006-508-{:02d}BE",
        datasheet=(
            "https://www.sameskydevices.com/product/resource/tb006-508.pdf"
        ),
        pin_counts=list(range(2, 25)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Blue",
        pitch=5.08,
        mounting_angle="Vertical",
        current_rating=12.0,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin",
    ),
    "SLM-1xx-01-G-S": SeriesSpec(
        manufacturer="Samtec",
        base_series="SLM-1xx-01-G-S",
        footprint_pattern="connector_footprints:SLM-1{:02d}-01-G-S",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/slm_th.pdf?"
            "_gl=1*1d4b5ri*_gcl_au*MTM0MTYyNTQ5MS4xNzM2MDk5MTUz*"
            "_ga*MTYxNDYyMTQ0Mi4xNzM2MDk5MTUz*"
            "_ga_3KFNZC07WW*MTczNjA5OTE1My4xLjEuMTczNjEwMDY3My4zMC4wLjA."
        ),
        pin_counts=list(range(1, 51)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=1.27,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin",
    ),
    "HMTSW-1xx-10-G-S-530-RA": SeriesSpec(
        manufacturer="Samtec",
        base_series="HMTSW-1xx-10-G-S-530-RA",
        footprint_pattern="connector_footprints:HMTSW-1{:02d}-10-G-S-530-RA",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/hmtsw.pdf?"
            "_gl=1*ilxh7h*_gcl_au*MTM0MTYyNTQ5MS4xNzM2MDk5MTUz*"
            "_ga*MTYxNDYyMTQ0Mi4xNzM2MDk5MTUz*"
            "_ga_3KFNZC07WW*MTczOTYxNDU2My4zNy4xLjE3Mzk2MTUzNTkuNjAuMC4w"
        ),
        pin_counts=list(range(1, 51)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=2.54,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin",
    ),
    "MTSW-1xx-10-L-D-530-RA": SeriesSpec(
        manufacturer="Samtec",
        base_series="MTSW-1xx-10-L-D-530-RA",
        footprint_pattern="connector_footprints:MTSW-1{:02d}-10-L-D-530-RA",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/mtsw.pdf?"
            "_gl=1*143vrvp*_gcl_aw*R0NMLjE3Mzk2ODk4NTMuQ2p3S0NBaUFrOE"
            "c5QmhBMEVpd0FPUXhtZnBxNGtid2RzbUtZdVAxNHNtU0RyMV9EYlVGX2"
            "0zcWFYTlVYU2w2UG00UVlkbEJkTWNnblpSb0NWcXdRQXZEX0J3RQ..*"
            "_gcl_au*MTM0MTYyNTQ5MS4xNzM2MDk5MTUz*"
            "_ga*MTYxNDYyMTQ0Mi4xNzM2MDk5MTUz*"
            "_ga_3KFNZC07WW*MTczOTY4OTg1My4zOS4xLjE3Mzk2OTU3NzcuMzcuMC4w"
        ),
        pin_counts=list(range(1, 51)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=2.54,
        number_of_rows=2,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin",
    ),
    "MTMM-1xx-04-L-D-196": SeriesSpec(
        manufacturer="Samtec",
        base_series="MTMM-1xx-04-L-D-196",
        footprint_pattern="connector_footprints:MTMM-1{:02d}-04-L-D-196",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/mtmm_th.pdf?"
            "_gl=1*10xs2wh*_gcl_au*OTQ3NjE2MTIwLjE3NTQ5MDMyODE.*"
            "_ga*NzIxODQzNjU3LjE3NTQ5MDMyODI.*"
            "_ga_3KFNZC07WW*"
            "czE3NTQ5MDMyODEkbzEkZzEkdDE3NTQ5MDYwODAkajYwJGwwJGgw"
        ),
        pin_counts=list(range(1, 51)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=2.00,
        number_of_rows=2,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin",
    ),
    "TMS-1xx-02-G-S": SeriesSpec(
        manufacturer="Samtec",
        base_series="TMS-1xx-02-G-S",
        footprint_pattern="connector_footprints:TMS-1{:02d}-02-G-S",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/tms_th.pdf?"
            "_gl=1*ta0q2w*_gcl_au*MTM0MTYyNTQ5MS4xNzM2MDk5MTUz*"
            "_ga*MTYxNDYyMTQ0Mi4xNzM2MDk5MTUz*"
            "_ga_3KFNZC07WW*MTczNjE2MDY1Mi40LjEuMTczNjE2MDc4OS41NS4wLjA."
        ),
        pin_counts=list(range(1, 51)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=1.27,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin",
    ),
    "TMS-1xx-02-G-D": SeriesSpec(
        manufacturer="Samtec",
        base_series="TMS-1xx-02-G-D",
        footprint_pattern="connector_footprints:TMS-1{:02d}-02-G-D",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/tms_th.pdf?"
            "_gl=1*ta0q2w*_gcl_au*MTM0MTYyNTQ5MS4xNzM2MDk5MTUz*"
            "_ga*MTYxNDYyMTQ0Mi4xNzM2MDk5MTUz*"
            "_ga_3KFNZC07WW*MTczNjE2MDY1Mi40LjEuMTczNjE2MDc4OS41NS4wLjA."
        ),
        pin_counts=list(range(1, 51)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=1.27,
        number_of_rows=2,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin",
    ),
    "SL-1xx-G-11": SeriesSpec(
        manufacturer="Samtec",
        base_series="SL-1xx-G-11",
        footprint_pattern="connector_footprints:SL-1{:02d}-G-11",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/sl.pdf?"
            "_gl=1*1p6n3ck*_gcl_au*MTM0MTYyNTQ5MS4xNzM2MDk5MTUz*"
            "_ga*MTYxNDYyMTQ0Mi4xNzM2MDk5MTUz*"
            "_ga_3KFNZC07WW*MTczNjU4NzcxMi4xMi4xLjE3MzY1ODg1ODguNjAuMC4w"
        ),
        pin_counts=list(range(1, 33)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=2.54,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin",
    ),
    "BBS-1xx-G-A": SeriesSpec(
        manufacturer="Samtec",
        base_series="BBS-1xx-G-A",
        footprint_pattern="connector_footprints:BBS-1{:02d}-G-A",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/bbs.pdf?"
            "_gl=1*oynpe4*_gcl_au*MTM0MTYyNTQ5MS4xNzM2MDk5MTUz*"
            "_ga*MTYxNDYyMTQ0Mi4xNzM2MDk5MTUz*"
            "_ga_3KFNZC07WW*MTczNjY3MzY1Ny4xMy4xLjE3MzY2NzM4NjguNDIuMC4w"
        ),
        pin_counts=list(range(1, 33)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=2.54,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin",
    ),
    "BSW-1xx-04-G-S": SeriesSpec(
        manufacturer="Samtec",
        base_series="BSW-1xx-04-G-S",
        footprint_pattern="connector_footprints:BSW-1{:02d}-04-G-S",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/bsw.pdf?"
            "_gl=1*kyaku3*_gcl_aw*R0NMLjE3Mzk2ODk4NTMuQ2p3S0NBaUFrO"
            "Ec5QmhBMEVpd0FPUXhtZnBxNGtid2RzbUtZdVAxNHNtU0RyMV9EYlV"
            "GX20zcWFYTlVYU2w2UG00UVlkbEJkTWNnblpSb0NWcXdRQXZEX0J3RQ..*"
            "_gcl_au*MTM0MTYyNTQ5MS4xNzM2MDk5MTUz*"
            "_ga*MTYxNDYyMTQ0Mi4xNzM2MDk5MTUz*"
            "_ga_3KFNZC07WW*MTc0MTExMjA4Ni40Ni4xLjE3NDExMTMwODkuNjAuMC4w"
        ),
        pin_counts=list(range(2, 37)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=2.54,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin",
    ),
    "CLP-1xx-02-G-D-BE": SeriesSpec(
        manufacturer="Samtec",
        base_series="CLP-1xx-02-G-D-BE",
        footprint_pattern="connector_footprints:CLP-1{:02d}-02-G-D-BE",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/clp_sm.pdf?"
            "_gl=1*1y4jlr9*_gcl_au*MTM0MTYyNTQ5MS4xNzM2MDk5MTUz*"
            "_ga*MTYxNDYyMTQ0Mi4xNzM2MDk5MTUz*"
            "_ga_3KFNZC07WW*MTczNjY4MDQ4OS4xNS4xLjE3MzY2ODEzNzcuNjAuMC4w"
        ),
        pin_counts=list(range(2, 51)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=1.27,
        number_of_rows=2,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Surface Mount",
        contact_plating="Tin",
    ),
    "TSM-1xx-03-L-DH-TR": SeriesSpec(
        manufacturer="Samtec",
        base_series="TSM-1xx-03-L-DH-TR",
        footprint_pattern="connector_footprints:TSM-1{:02d}-03-L-DH-TR",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/tsm.pdf?"
            "_gl=1*15mav39*_gcl_aw*R0NMLjE3Mzk2ODk4NTMuQ2p3S0NBaUFr"
            "OEc5QmhBMEVpd0FPUXhtZnBxNGtid2RzbUtZdVAxNHNtU0RyMV9EYl"
            "VGX20zcWFYTlVYU2w2UG00UVlkbEJkTWNnblpSb0NWcXdRQXZEX0J3RQ..*"
            "_gcl_au*MTM0MTYyNTQ5MS4xNzM2MDk5MTUz*"
            "_ga*MTYxNDYyMTQ0Mi4xNzM2MDk5MTUz*"
            "_ga_3KFNZC07WW*MTc0MDA3NzE4OC40NC4wLjE3NDAwNzc3ODMuNDguMC4w"
        ),
        pin_counts=list(range(2, 37)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=2.54,
        number_of_rows=2,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Surface Mount",
        contact_plating="Tin",
    ),
    "TSM-1xx-03-L-SH-TR": SeriesSpec(
        manufacturer="Samtec",
        base_series="TSM-1xx-03-L-SH-TR",
        footprint_pattern="connector_footprints:TSM-1{:02d}-03-L-SH-TR",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/tsm.pdf?"
            "_gl=1*15mav39*_gcl_aw*R0NMLjE3Mzk2ODk4NTMuQ2p3S0NBaUFr"
            "OEc5QmhBMEVpd0FPUXhtZnBxNGtid2RzbUtZdVAxNHNtU0RyMV9EYl"
            "VGX20zcWFYTlVYU2w2UG00UVlkbEJkTWNnblpSb0NWcXdRQXZEX0J3RQ..*"
            "_gcl_au*MTM0MTYyNTQ5MS4xNzM2MDk5MTUz*"
            "_ga*MTYxNDYyMTQ0Mi4xNzM2MDk5MTUz*"
            "_ga_3KFNZC07WW*MTc0MDA3NzE4OC40NC4wLjE3NDAwNzc3ODMuNDguMC4w"
        ),
        pin_counts=list(range(2, 37)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=2.54,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Surface Mount",
        contact_plating="Tin",
    ),
    "TSW-1xx-14-G-S": SeriesSpec(
        manufacturer="Samtec",
        base_series="TSW-1xx-14-G-S",
        footprint_pattern="connector_footprints:TSW-1{:02d}-14-G-S",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/tsw_th.pdf?"
            "_gl=1*jw1r0n*_gcl_aw*R0NMLjE3Mzk2ODk4NTMuQ2p3S0NBaUFrOEc5"
            "QmhBMEVpd0FPUXhtZnBxNGtid2RzbUtZdVAxNHNtU0RyMV9EYlVGX20zc"
            "WFYTlVYU2w2UG00UVlkbEJkTWNnblpSb0NWcXdRQXZEX0J3RQ..*"
            "_gcl_au*MTM0MTYyNTQ5MS4xNzM2MDk5MTUz*"
            "_ga*MTYxNDYyMTQ0Mi4xNzM2MDk5MTUz*"
            "_ga_3KFNZC07WW*MTc0MTE5MzI3NC40OC4xLjE3NDExOTMzODUuMjUuMC4w"
        ),
        pin_counts=list(range(1, 51)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=2.54,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Gold",
    ),
    "FW-xx-04-G-D-070-315": SeriesSpec(
        manufacturer="Samtec",
        base_series="FW-xx-04-G-D-070-315",
        footprint_pattern="connector_footprints:FW-{:02d}-04-G-D-070-315",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/fw_th.pdf?"
            "_gl=1*bk9ipk*_gcl_au*MTM0MTYyNTQ5MS4xNzM2MDk5MTUz*"
            "_ga*MTYxNDYyMTQ0Mi4xNzM2MDk5MTUz*"
            "_ga_3KFNZC07WW*MTczNzc5NjUxNS4yOS4xLjE3Mzc3OTczNzkuNjAuMC4w"
        ),
        pin_counts=list(range(2, 51)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=1.27,
        number_of_rows=2,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Gold",
    ),
    "FW-xx-03-G-D-085-315": SeriesSpec(
        manufacturer="Samtec",
        base_series="FW-xx-03-G-D-085-315",
        footprint_pattern="connector_footprints:FW-{:02d}-03-G-D-085-315",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/fw_sm.pdf?"
            "_gl=1*1xtxv9c*_gcl_au*MTM0MTYyNTQ5MS4xNzM2MDk5MTUz*"
            "_ga*MTYxNDYyMTQ0Mi4xNzM2MDk5MTUz*"
            "_ga_3KFNZC07WW*MTczODE2NTI0NS4zMi4xLjE3MzgxNjU1NjMuNjAuMC4w"
        ),
        pin_counts=list(range(2, 51)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=1.27,
        number_of_rows=2,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Surface Mount",
        contact_plating="Gold",
    ),
    "FW-xx-03-G-D-085-155": SeriesSpec(
        manufacturer="Samtec",
        base_series="FW-xx-03-G-D-085-155",
        footprint_pattern="connector_footprints:FW-{:02d}-03-G-D-085-155",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/fw_sm.pdf?"
            "_gl=1*1xtxv9c*_gcl_au*MTM0MTYyNTQ5MS4xNzM2MDk5MTUz*"
            "_ga*MTYxNDYyMTQ0Mi4xNzM2MDk5MTUz*"
            "_ga_3KFNZC07WW*MTczODE2NTI0NS4zMi4xLjE3MzgxNjU1NjMuNjAuMC4w"
        ),
        pin_counts=list(range(2, 51)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=1.27,
        number_of_rows=2,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Surface Mount",
        contact_plating="Gold",
    ),
    "FW-xx-05-F-D-248-160": SeriesSpec(
        manufacturer="Samtec",
        base_series="FW-xx-05-F-D-248-160",
        footprint_pattern="connector_footprints:FW-{:02d}-05-F-D-248-160",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/fw_sm.pdf?"
            "_gl=1*1mheflh*_gcl_au*OTQ3NjE2MTIwLjE3NTQ5MDMyODE.*"
            "_ga*NzIxODQzNjU3LjE3NTQ5MDMyODI.*_ga"
            "_3KFNZC07WW*czE3NTk0MTUxODQkbzckZzEkdDE3NTk0MTc0NDAkajYwJGwwJGgw"
        ),
        pin_counts=list(range(2, 51)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=1.27,
        number_of_rows=2,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Surface Mount",
        contact_plating="Gold",
    ),
    "FW-xx-03-G-D-120-160": SeriesSpec(
        manufacturer="Samtec",
        base_series="FW-xx-03-G-D-120-160",
        footprint_pattern="connector_footprints:FW-{:02d}-03-G-D-120-160",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/fw_sm.pdf?"
            "_gl=1*8ugof3*_gcl_au*OTQ3NjE2MTIwLjE3NTQ5MDMyODE.*"
            "_ga*NzIxODQzNjU3LjE3NTQ5MDMyODI.*_ga_3KFNZC07WW*"
            "czE3NTk0MjczODckbzgkZzEkdDE3NTk0Mjk2MzQkajYwJGwwJGgw"
        ),
        pin_counts=list(range(2, 51)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=1.27,
        number_of_rows=2,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Surface Mount",
        contact_plating="Gold",
    ),
    "FW-xx-03-G-D-150-160": SeriesSpec(
        manufacturer="Samtec",
        base_series="FW-xx-03-G-D-150-160",
        footprint_pattern="connector_footprints:FW-{:02d}-03-G-D-150-160",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/fw_sm.pdf?"
            "_gl=1*696njn*_gcl_au*OTQ3NjE2MTIwLjE3NTQ5MDMyODE.*"
            "_ga*NzIxODQzNjU3LjE3NTQ5MDMyODI.*_ga_3KFNZC07WW*"
            "czE3NTk0NzU3MTckbzkkZzEkdDE3NTk0Nzk3ODIkajYwJGwwJGgw"
        ),
        pin_counts=list(range(2, 51)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=1.27,
        number_of_rows=2,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Surface Mount",
        contact_plating="Gold",
    ),
    "FW-xx-05-G-D-470-160": SeriesSpec(
        manufacturer="Samtec",
        base_series="FW-xx-05-G-D-470-160",
        footprint_pattern="connector_footprints:FW-{:02d}-05-G-D-470-160",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/fw_sm.pdf?"
            "_gl=1*dqfgvk*_gcl_au*OTQ3NjE2MTIwLjE3NTQ5MDMyODE.*"
            "_ga*NzIxODQzNjU3LjE3NTQ5MDMyODI.*_ga_3KFNZC07WW*"
            "czE3NTk3NjQxNTMkbzEyJGcwJHQxNzU5NzY1NzUzJGo2MCRsMCRoMA.."
        ),
        pin_counts=list(range(2, 51)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=1.27,
        number_of_rows=2,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Surface Mount",
        contact_plating="Gold",
    ),
    "FTSH-1xx-01-L-DV": SeriesSpec(
        manufacturer="Samtec",
        base_series="FTSH-1xx-01-L-DV",
        footprint_pattern="connector_footprints:FTSH-1{:02d}-01-L-DV",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/ftsh_smt.pdf?"
            "_gl=1*sm7rbj*_gcl_au*MTM0MTYyNTQ5MS4xNzM2MDk5MTUz*"
            "_ga*MTYxNDYyMTQ0Mi4xNzM2MDk5MTUz*"
            "_ga_3KFNZC07WW*MTczNjcwNzA1MC4xOC4xLjE3MzY3MDczODQuMzkuMC4w"
        ),
        pin_counts=list(range(2, 51)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=1.27,
        number_of_rows=2,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Surface Mount",
        contact_plating="Tin",
    ),
    "FTSH-1xx-01-L-DV-K": SeriesSpec(
        manufacturer="Samtec",
        base_series="FTSH-1xx-01-L-DV-K",
        footprint_pattern="connector_footprints:FTSH-1{:02d}-01-L-DV-K",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/ftsh_smt.pdf?"
            "_gl=1*13r0j96*_gcl_aw*R0NMLjE3Mzk2ODk4NTMuQ2p3S0NBaUFrOEc5Q"
            "mhBMEVpd0FPUXhtZnBxNGtid2RzbUtZdVAxNHNtU0RyMV9EYlVGX20zcWFY"
            "TlVYU2w2UG00UVlkbEJkTWNnblpSb0NWcXdRQXZEX0J3RQ..*"
            "_gcl_au*MTM0MTYyNTQ5MS4xNzM2MDk5MTUz*"
            "_ga*MTYxNDYyMTQ0Mi4xNzM2MDk5MTUz*"
            "_ga_3KFNZC07WW*MTczOTcyNzA5MC40MS4xLjE3Mzk3Mjc5NzAuNDguMC4w"
        ),
        pin_counts=list(range(5, 26)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=1.27,
        number_of_rows=2,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Surface Mount",
        contact_plating="Tin",
    ),
    "FTSH-1xx-04-L-D": SeriesSpec(
        manufacturer="Samtec",
        base_series="FTSH-1xx-04-L-D",
        footprint_pattern="connector_footprints:FTSH-1{:02d}-04-L-D",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/ftsh_th.pdf?"
            "_gl=1*bi311t*_gcl_au*MTM0MTYyNTQ5MS4xNzM2MDk5MTUz*"
            "_ga*MTYxNDYyMTQ0Mi4xNzM2MDk5MTUz*"
            "_ga_3KFNZC07WW*MTczNjk0NTEyMi4yNi4xLjE3MzY5NDU1NjAuNjAuMC4w"
        ),
        pin_counts=list(range(2, 51)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=1.27,
        number_of_rows=2,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Tin",
    ),
    "FTSH-1xx-04-L-DH": SeriesSpec(
        manufacturer="Samtec",
        base_series="FTSH-1xx-04-L-DH",
        footprint_pattern="connector_footprints:FTSH-1{:02d}-04-L-DH",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/ftsh_smt.pdf?"
            "_gl=1*uwyfuk*_gcl_au*OTQ3NjE2MTIwLjE3NTQ5MDMyODE.*"
            "_ga*NzIxODQzNjU3LjE3NTQ5MDMyODI.*_ga_3KFNZC07WW*"
            "czE3NTk5OTE3NDIkbzE1JGcxJHQxNzU5OTkxODU5JGo4JGwwJGgw"
        ),
        pin_counts=list(range(2, 51)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=1.27,
        number_of_rows=2,
        mounting_angle="Horizontal",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Surface Mount",
        contact_plating="Tin",
    ),
    "TSM-1xx-01-S-SV-P-TR": SeriesSpec(
        manufacturer="Samtec",
        base_series="TSM-1xx-01-S-SV-P-TR",
        footprint_pattern="connector_footprints:TSM-1{:02d}-01-S-SV-P-TR",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/tsm.pdf?"
            "_gl=1*1eihxyt*_gcl_au*MTM0MTYyNTQ5MS4xNzM2MDk5MTUz*"
            "_ga*MTYxNDYyMTQ0Mi4xNzM2MDk5MTUz*"
            "_ga_3KFNZC07WW*MTczNjc2MTAxMy4xOS4xLjE3MzY3NjE0NjIuMjIuMC4w"
        ),
        pin_counts=list(range(2, 51)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=2.54,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Surface Mount",
        contact_plating="Tin",
    ),
    "RSM-1xx-02-STL-S": SeriesSpec(
        manufacturer="Samtec",
        base_series="RSM-1xx-02-STL-S",
        footprint_pattern="connector_footprints:RSM-1{:02d}-02-STL-S",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/rsm_sm.pdf?"
            "_gl=1*1uxcywd*_gcl_au*MTM0MTYyNTQ5MS4xNzM2MDk5MTUz*"
            "_ga*MTYxNDYyMTQ0Mi4xNzM2MDk5MTUz*"
            "_ga_3KFNZC07WW*MTczNjg1MTE0OS4yMi4xLjE3MzY4NTE1MTQuMTcuMC4w"
        ),
        pin_counts=list(range(2, 37)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=1.27,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Surface Mount",
        contact_plating="Tin",
    ),
    "FTR-1xx-03-L-S": SeriesSpec(
        manufacturer="Samtec",
        base_series="FTR-1xx-03-L-S",
        footprint_pattern="connector_footprints:FTR-1{:02d}-03-L-S",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/ftr_smt.pdf?"
            "_gl=1*17eh0a1*_gcl_au*MTM0MTYyNTQ5MS4xNzM2MDk5MTUz*"
            "_ga*MTYxNDYyMTQ0Mi4xNzM2MDk5MTUz*"
            "_ga_3KFNZC07WW*MTczNjg3NzAzNy4yNC4xLjE3MzY4NzcyMTEuMjQuMC4w"
        ),
        pin_counts=list(range(2, 41)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=1.27,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Surface Mount",
        contact_plating="Tin",
    ),
    "1043": SeriesSpec(
        manufacturer="Keystone Electronics",
        base_series="1043",
        footprint_pattern="connector_footprints:1043",
        datasheet=("https://www.keyelco.com/userAssets/file/M65p27.pdf"),
        pin_counts=[2],
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=71.6,
        number_of_rows=1,
        mounting_angle="Vertical",
        current_rating="N/A",
        voltage_rating="N/A",
        mounting_style="Through Hole",
        contact_plating="Tin",
    ),
    "1042P": SeriesSpec(
        manufacturer="Keystone Electronics",
        base_series="1042P",
        footprint_pattern="connector_footprints:1042P",
        datasheet=("https://www.keyelco.com/userAssets/file/M65p27.pdf"),
        pin_counts=[2],
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=71.6,
        number_of_rows=1,
        mounting_angle="Vertical",
        current_rating="N/A",
        voltage_rating="N/A",
        mounting_style="Surface Mount",
        contact_plating="Tin",
    ),
    "UJ32-C-V-G-TH-8-P24-TR": SeriesSpec(
        manufacturer="Samtec",
        base_series="UJ32-C-V-G-TH-8-P24-TR",
        footprint_pattern="connector_footprints:UJ32-C-V-G-TH-8-P24-TR",
        datasheet=(
            "https://www.sameskydevices.com/product/resource/"
            "uj32-c-v-g-th-8-p24-tr.pdf"
        ),
        pin_counts=[12],
        number_of_rows=2,
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=1.27,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Surface Mount",
        contact_plating="Tin",
        rectangle_width=15.24,
        symbol_pin_length=5.08,
        pin_names={
            **{
                "A12": "GND",
                "A11": "RXp2",
                "A10": "RXn2",
                "A9": "VBUS",
                "A8": "SBU1",
                "A7": "Dn1",
                "A6": "Dp1",
                "A5": "CC1",
                "A4": "VBUS",
                "A3": "TXn1",
                "A2": "TXp1",
                "A1": "GND",
            },
            **{
                "B12": "GND",
                "B11": "RXp1",
                "B10": "RXn1",
                "B9": "VBUS",
                "B8": "SBU2",
                "B7": "Dn2",
                "B6": "Dp2",
                "B5": "CC2",
                "B4": "VBUS",
                "B3": "TXn2",
                "B2": "TXp2",
                "B1": "GND",
            },
        },
    ),
    "FW-xx-04-G-D-370-160": SeriesSpec(
        manufacturer="Samtec",
        base_series="FW-xx-04-G-D-370-160",
        footprint_pattern="connector_footprints:FW-{:02d}-04-G-D-370-160",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/fw_th.pdf?"
            "_gl=1*13f8b1s*_gcl_au*OTQ3NjE2MTIwLjE3NTQ5MDMyODE.*"
            "_ga*NzIxODQzNjU3LjE3NTQ5MDMyODI.*"
            "_ga_3KFNZC07WW*"
            "czE3NTc1MTM2MzIkbzUkZzEkdDE3NTc1MTczNTEkajE2JGwwJGgw"
        ),
        pin_counts=list(range(2, 51)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=1.27,
        number_of_rows=2,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Gold",
    ),
    "FW-xx-01-G-D-160-160": SeriesSpec(
        manufacturer="Samtec",
        base_series="FW-xx-01-G-D-160-160",
        footprint_pattern="connector_footprints:FW-{:02d}-01-G-D-160-160",
        datasheet=(
            "https://suddendocs.samtec.com/catalog_english/fw_th.pdf?"
            "_gl=1*12wer0i*_gcl_au*OTQ3NjE2MTIwLjE3NTQ5MDMyODE.*"
            "_ga*NzIxODQzNjU3LjE3NTQ5MDMyODI.*_ga_3KFNZC07WW*"
            "czE3NjA4NTY2ODgkbzE3JGcxJHQxNzYwODU5NDQxJGo2MCRsMCRoMA.."
        ),
        pin_counts=list(range(2, 51)),
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Black",
        pitch=1.27,
        number_of_rows=2,
        mounting_angle="Vertical",
        current_rating=5.2,
        voltage_rating=300,
        mounting_style="Through Hole",
        contact_plating="Gold",
    ),
}
