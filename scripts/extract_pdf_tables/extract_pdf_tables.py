"""PDF table extraction using Camelot.

Provides utilities for extracting tables from PDF files,
iterating over each page and saving all detected tables as CSV
files, with table names extracted from the text above each table.
Supports merging tables that span multiple pages and per-PDF
configuration for multiple tables.
"""

import csv
import re
from dataclasses import dataclass, field
from pathlib import Path

import camelot
import pandas as pd
import pdfplumber


@dataclass
class TableConfig:
    """Configuration for extracting a single table from a PDF.

    Attributes:
        table_name_filter: String to filter tables by name.
        page_range: Page range to process e.g. '78-105' or 'all'.
        header_rows: Number of rows forming the header block.
        exclude_column_names: List of column names to exclude.
            All header rows are searched for matching names.
        output_filename: Optional filename stem for the output CSV.
            When the same table is extracted multiple times with
            different parameters (e.g. different packages), set this
            to a unique name such as ``"Table 14_LQFP144"`` so each
            extraction saves to its own file instead of overwriting.
            The ``.csv`` extension is added automatically.
            If omitted, the filename is derived from the table name.

    """

    table_name_filter: str
    page_range: str = "all"
    header_rows: int = 2
    exclude_column_names: list[str] = field(default_factory=list)
    output_filename: str = ""


def get_table_name(
    page: pdfplumber.page.Page,
    table_bbox: tuple,
    lines: int = 3,
) -> str:
    """Extract the table name from text immediately above the table.

    Args:
        page: The PDF page containing the table.
        table_bbox: Bounding box as (x0, y0, x1, y1) in pdfplumber
            coordinate space.
        lines: Number of lines above the table to search.

    Returns:
        The extracted table name, or an empty string if not found.

    """
    left, top, right, _ = table_bbox
    margin = 5
    search_height = 50 * lines
    above_bbox = (left, max(0, top - search_height), right, top - margin)

    cropped = page.crop(above_bbox)
    text = cropped.extract_text()
    if not text:
        return ""

    lines_found = [line.strip() for line in text.splitlines() if line.strip()]
    return lines_found[-1] if lines_found else ""


def is_continued_table(table_name: str) -> bool:
    """Check if a table name indicates a continuation.

    Args:
        table_name: The table name to check.

    Returns:
        True if the name contains 'continued', False otherwise.

    """
    return "continued" in table_name.lower()


def get_base_name(table_name: str) -> str:
    """Strip the '(continued)' suffix to get the base table name.

    Args:
        table_name: The table name to strip.

    Returns:
        The base table name without continuation markers.

    """
    return table_name.lower().replace("(continued)", "").strip()


def same_table(table_name_1: str, table_name_2: str) -> bool:
    """Check if two table names refer to the same table.

    Args:
        table_name_1: First table name.
        table_name_2: Second table name.

    Returns:
        True if both names refer to the same base table.

    """
    return get_base_name(table_name_1) == get_base_name(table_name_2)


def matches_filter(table_name: str, table_name_filter: str) -> bool:
    """Check if a table name matches the given filter string.

    Uses a negative lookahead to avoid partial number matches,
    e.g. 'Table 14' will not match 'Table 140'.

    Args:
        table_name: The table name to check.
        table_name_filter: The filter string to match against.

    Returns:
        True if the table name matches the filter as a whole word.

    """
    pattern = re.escape(table_name_filter.lower()) + r"(?!\d)"
    return bool(re.search(pattern, table_name.lower()))


def camelot_bbox_to_pdfplumber(
    bbox: tuple,
    page_height: float,
) -> tuple:
    """Convert Camelot bbox to pdfplumber coordinate space.

    Camelot uses bottom-left origin, pdfplumber uses top-left origin.

    Args:
        bbox: Bounding box from Camelot as (x0, y0, x1, y1).
        page_height: Height of the page in points.

    Returns:
        Bounding box in pdfplumber coordinates as (x0, y0, x1, y1).

    """
    left, bottom, right, top = bbox
    return (left, page_height - top, right, page_height - bottom)


def _parse_page_range(
    page_range: str,
    total_pages: int,
) -> list[int]:
    """Parse a page range string into a list of page numbers.

    Args:
        page_range: Page range string e.g. '1-10', 'all', or '5'.
        total_pages: Total number of pages in the PDF.

    Returns:
        A list of page numbers to process.

    """
    if page_range == "all":
        return list(range(1, total_pages + 1))

    pages = []
    for part in page_range.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            pages.extend(range(int(start), int(end) + 1))
        else:
            pages.append(int(part))
    return pages


def _is_header_row(
    row: list,
    header: list,
    threshold: float = 0.7,
) -> bool:
    """Check if a row is a header row using fuzzy matching.

    Args:
        row: The row to check.
        header: The reference header row.
        threshold: Minimum fraction of matching cells.

    Returns:
        True if the row is considered a header row.

    """
    if len(row) != len(header):
        return False
    matches = sum(
        1
        for cell, ref in zip(row, header)
        if str(cell).strip() == str(ref).strip()
    )
    return matches / len(header) >= threshold


def _remove_duplicate_headers(
    rows: list[list],
    header_rows: int = 2,
    threshold: float = 0.7,
) -> list[list]:
    """Remove rows that match any row in the header block.

    Each data row is checked individually against all header rows.
    If it matches any of them, it is considered a duplicate and
    removed.

    Args:
        rows: All rows from the merged table.
        header_rows: Number of rows that form the header block.
        threshold: Minimum fraction of matching cells to consider
            a row a duplicate header.

    Returns:
        Rows with duplicate header rows removed.

    """
    if not rows:
        return rows

    headers = rows[:header_rows]
    cleaned = list(headers)

    for row in rows[header_rows:]:
        is_dup = any(
            _is_header_row(row, header, threshold) for header in headers
        )
        if not is_dup:
            cleaned.append(row)

    return cleaned


def _exclude_cols_by_name(
    rows: list[list],
    exclude_column_names: list[str],
    header_rows: int = 2,
) -> list[list]:
    """Exclude columns by name from a list of rows.

    Searches all header rows for matching column names, then
    filters out those columns from all rows. This handles tables
    with multi-row headers where some column names appear in the
    first header row and others in the second.

    Args:
        rows: All rows from the table including headers.
        exclude_column_names: List of column names to exclude.
        header_rows: Number of header rows to search for names.
            Defaults to 2.

    Returns:
        Rows with the specified columns removed.

    """
    if not rows or header_rows > len(rows):
        return rows

    exclude_set = set(exclude_column_names)
    indices_to_exclude = set()

    for header_row_index in range(header_rows):
        header = rows[header_row_index]
        for col_idx, cell in enumerate(header):
            if str(cell).strip() in exclude_set:
                indices_to_exclude.add(col_idx)

    found_names = {
        str(rows[row_idx][col_idx]).strip()
        for row_idx in range(header_rows)
        for col_idx in indices_to_exclude
        if col_idx < len(rows[row_idx])
    }
    missing = [
        col_name
        for col_name in exclude_column_names
        if col_name not in found_names
    ]
    if missing:
        print(f"  Warning: column names not found: {missing}")

    return [
        [
            cell
            for col_idx, cell in enumerate(row)
            if col_idx not in indices_to_exclude
        ]
        for row in rows
    ]


def _collect_tables(
    pdf_path: str,
    table_name_filter: str | None,
    page_range: str = "all",
    header_rows: int = 2,
) -> list[dict]:
    """Collect all matching tables from a PDF with their metadata.

    Duplicate header rows are removed from each table immediately
    after extraction, before merging.

    Args:
        pdf_path: Path to the PDF file.
        table_name_filter: Optional filter string to match table names.
        page_range: Page range to process e.g. '78-105' or 'all'.
        header_rows: Number of rows forming the header block.

    Returns:
        A list of dicts with keys: page, bbox, df, name.

    """
    all_tables = []

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        pages_to_process = _parse_page_range(page_range, total_pages)
        total = len(pages_to_process)

        for page_idx, page_num in enumerate(pages_to_process, start=1):
            print(
                f"Processing page {page_num} ({page_idx}/{total})...",
                end="\r",
            )

            tables = None
            for attempt in range(1, 4):
                try:
                    tables = camelot.read_pdf(
                        pdf_path,
                        pages=str(page_num),
                        flavor="lattice",
                    )
                    break
                except KeyboardInterrupt:
                    if attempt < 3:
                        print(
                            f"\n  Warning: pypdfium2 rendering error on"
                            f" page {page_num}, retrying"
                            f" ({attempt}/3)..."
                        )
                    else:
                        print(
                            f"\n  Warning: pypdfium2 rendering error on"
                            f" page {page_num} after 3 attempts"
                            f" — skipping."
                        )

            if tables is None:
                continue

            page = pdf.pages[page_num - 1]
            page_height = page.height

            for table in tables:
                plumber_bbox = camelot_bbox_to_pdfplumber(
                    table._bbox, page_height
                )
                table_name = get_table_name(page, plumber_bbox)

                if table_name_filter:
                    is_match = matches_filter(table_name, table_name_filter)
                    is_cont = is_continued_table(
                        table_name
                    ) and matches_filter(table_name, table_name_filter)
                    if not is_match and not is_cont:
                        continue

                rows = _remove_duplicate_headers(
                    table.df.values.tolist(),
                    header_rows=header_rows,
                )
                clean_df = pd.DataFrame(rows)

                print(
                    f"  Found '{table_name}' on page {page_num} "
                    f"({clean_df.shape[0]} rows, "
                    f"accuracy: {table.accuracy:.1f}%)"
                )

                all_tables.append({
                    "page": page_num,
                    "bbox": table._bbox,
                    "df": clean_df,
                    "name": table_name,
                })

    return all_tables


def _merge_tables(
    all_tables: list[dict],
    header_rows: int = 2,
) -> list[dict]:
    """Merge tables that continue across consecutive pages.

    Header rows are unconditionally stripped from continuation
    tables before merging.

    Args:
        all_tables: List of table dicts collected from the PDF.
        header_rows: Number of header rows to strip from each
            continuation table.

    Returns:
        A list of merged table dicts with keys:
        start_page, name, df.

    """
    merged_tables = []
    skip_indices = set()

    for table_idx, table in enumerate(all_tables):
        if table_idx in skip_indices:
            continue

        merged_df = table["df"].copy()
        merged_name = table["name"]
        start_page = table["page"]

        next_idx = table_idx + 1
        while next_idx < len(all_tables):
            next_table = all_tables[next_idx]

            if next_table["page"] > all_tables[next_idx - 1]["page"] + 1:
                break

            if is_continued_table(next_table["name"]) and same_table(
                merged_name, next_table["name"]
            ):
                continuation_df = next_table["df"].iloc[header_rows:]

                merged_df = pd.concat(
                    [merged_df, continuation_df],
                    ignore_index=True,
                )
                skip_indices.add(next_idx)
                print(
                    f"  Merged page {next_table['page']} "
                    f"continuation into '{merged_name}'"
                )
                next_idx += 1
            else:
                break

        merged_tables.append({
            "start_page": start_page,
            "name": merged_name,
            "df": merged_df,
        })

    return merged_tables


def _save_to_csv(
    merged_tables: list[dict],
    output_path: Path,
    exclude_column_names: list[str] | None = None,
    header_rows: int = 2,
    output_filename: str = "",
) -> None:
    """Save merged tables to CSV files.

    Args:
        merged_tables: List of merged table dicts.
        output_path: Directory path to save the CSV files.
        exclude_column_names: Optional list of column names to
            exclude. All header rows are searched for matches.
        header_rows: Number of header rows to search for column
            names. Defaults to 2.
        output_filename: Optional filename stem that overrides the
            table name when naming the output file.  Useful when the
            same table is extracted multiple times with different
            parameters.  The ``.csv`` extension is added
            automatically.

    """
    for table_idx, table in enumerate(merged_tables, start=1):
        if output_filename:
            safe_name = "".join(
                char if char.isalnum() or char in " _-" else "_"
                for char in output_filename
            ).strip()
        else:
            safe_name = "".join(
                char if char.isalnum() or char in " _-" else "_"
                for char in table["name"]
            )
            safe_name = safe_name.strip() or f"table{table_idx}"

        csv_file = output_path / f"{safe_name}.csv"

        rows = table["df"].values.tolist()

        if exclude_column_names:
            rows = _exclude_cols_by_name(
                rows,
                exclude_column_names,
                header_rows=header_rows,
            )

        header = rows[:header_rows]
        data = [
            row
            for row in rows[header_rows:]
            if row and str(row[0]).strip() != "-"
        ]
        rows = header + data

        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        print(f"  Saved: {csv_file} ({len(rows)} rows)")


def _config_cache_key(config: TableConfig) -> tuple:
    """Return a hashable key identifying the PDF parsing parameters.

    Configs that share the same key can reuse a single parse result.

    Args:
        config: TableConfig to derive the key from.

    Returns:
        Tuple of ``(table_name_filter, page_range, header_rows)``.

    """
    return (config.table_name_filter, config.page_range, config.header_rows)


def extract_tables_from_pdf(
    pdf_path: str,
    output_dir: str = "tables",
    table_configs: list[TableConfig] | None = None,
) -> None:
    """Extract tables from a PDF file and save each as a CSV.

    Each TableConfig defines a separate output with its own column
    exclusions and output filename.  Configs that share the same
    table filter, page range, and header-row count are grouped so the
    PDF is only parsed once per unique combination, avoiding redundant
    passes through the file.

    Args:
        pdf_path: Path to the PDF file to extract tables from.
        output_dir: Directory to save the extracted CSV files.
        table_configs: List of TableConfig objects defining which
            tables to extract and how. Defaults to extracting all
            tables with default settings.

    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if not table_configs:
        table_configs = [TableConfig(table_name_filter="")]

    parse_cache: dict[tuple, list[dict]] = {}

    for config in table_configs:
        cache_key = _config_cache_key(config)

        if cache_key not in parse_cache:
            print(
                f"\n--- Extracting '{config.table_name_filter}' "
                f"(pages: {config.page_range}) ---"
            )

            all_tables = _collect_tables(
                pdf_path,
                config.table_name_filter or None,
                config.page_range,
                config.header_rows,
            )

            print(
                f"\nFound {len(all_tables)} matching tables. "
                f"Merging multi-page tables..."
            )

            merged_tables = _merge_tables(all_tables, config.header_rows)
            parse_cache[cache_key] = merged_tables
        else:
            merged_tables = parse_cache[cache_key]
            print(
                f"\n--- Reusing cached parse for "
                f"'{config.table_name_filter}' "
                f"(pages: {config.page_range}) ---"
            )

        print(f"\nSaving {len(merged_tables)} tables to '{output_path}'...")

        _save_to_csv(
            merged_tables,
            output_path,
            config.exclude_column_names or None,
            header_rows=config.header_rows,
            output_filename=config.output_filename,
        )

    print(f"\nDone processing '{Path(pdf_path).name}'.")


if __name__ == "__main__":
    script_dir = Path(__file__).parent
    pdf_files = list(script_dir.glob("*.pdf"))

    PDF_CONFIGS: dict[str, list[TableConfig]] = {
        "stm32h562ag": [
            TableConfig(
                table_name_filter="Table 14",
                page_range="78-105",
                header_rows=2,
                output_filename=(
                    "Table 14 STM32H562xx and STM32H563xx"
                    " pin_ball definition LQFP144"
                ),
                exclude_column_names=[
                    "WLCSP80 SMPS",
                    "LQFP100 SMPS",
                    "LQFP144 SMPS",
                    "UFBGA169 SMPS",
                    "LQFP176 SMPS",
                    "UFBGA176+25 SMPS",
                    "TFBGA225 SMPS",
                    "LQFP64",
                    "VFQFPN68",
                    "LQFP100",
                    "UFBGA169",
                    "LQFP176",
                    "UFBGA176+25",
                    "Pin type",
                    "I/O structure",
                    "Notes",
                ],
            ),
            TableConfig(
                table_name_filter="Table 14",
                page_range="78-105",
                header_rows=2,
                output_filename=(
                    "Table 14 STM32H562xx and STM32H563xx"
                    " pin_ball definition LQFP64"
                ),
                exclude_column_names=[
                    "WLCSP80 SMPS",
                    "LQFP100 SMPS",
                    "LQFP144 SMPS",
                    "UFBGA169 SMPS",
                    "LQFP176 SMPS",
                    "UFBGA176+25 SMPS",
                    "TFBGA225 SMPS",
                    "LQFP144",
                    "VFQFPN68",
                    "LQFP100",
                    "UFBGA169",
                    "LQFP176",
                    "UFBGA176+25",
                    "Pin type",
                    "I/O structure",
                    "Notes",
                ],
            ),
        ],
    }

    if not pdf_files:
        print(f"No PDF files found in '{script_dir}'.")
    else:
        print(f"Found {len(pdf_files)} PDF file(s) to process.")
        for pdf_file in pdf_files:
            print(f"\n{'=' * 60}")
            print(f"Processing: {pdf_file.name}")
            print(f"{'=' * 60}")

            configs = PDF_CONFIGS.get(
                pdf_file.stem,
                [TableConfig(table_name_filter="")],
            )

            extract_tables_from_pdf(
                str(pdf_file),
                output_dir=str(script_dir / "tables" / pdf_file.stem),
                table_configs=configs,
            )
