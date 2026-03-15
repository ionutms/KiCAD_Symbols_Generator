"""PDF table extraction using Camelot.

Provides utilities for extracting tables from PDF files,
iterating over each page and saving all detected tables as CSV
files, with table names extracted from the text above each table.
Supports merging tables that span multiple pages.
"""

import csv
import re
from pathlib import Path

import camelot
import pandas as pd
import pdfplumber


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
    x0, y0, x1, _ = table_bbox
    margin = 5
    search_height = 50 * lines
    above_bbox = (x0, max(0, y0 - search_height), x1, y0 - margin)

    cropped = page.crop(above_bbox)
    text = cropped.extract_text()
    if not text:
        return ""

    lines_found = [line.strip() for line in text.splitlines() if line.strip()]
    return lines_found[-1] if lines_found else ""


def is_continued_table(name: str) -> bool:
    """Check if a table name indicates a continuation.

    Args:
        name: The table name to check.

    Returns:
        True if the name contains 'continued', False otherwise.

    """
    return "continued" in name.lower()


def get_base_name(name: str) -> str:
    """Strip the '(continued)' suffix to get the base table name.

    Args:
        name: The table name to strip.

    Returns:
        The base table name without continuation markers.

    """
    return name.lower().replace("(continued)", "").strip()


def same_table(name1: str, name2: str) -> bool:
    """Check if two table names refer to the same table.

    Args:
        name1: First table name.
        name2: Second table name.

    Returns:
        True if both names refer to the same base table.

    """
    return get_base_name(name1) == get_base_name(name2)


def matches_filter(name: str, table_name_filter: str) -> bool:
    """Check if a table name matches the given filter string.

    Uses a negative lookahead to avoid partial number matches,
    e.g. 'Table 14' will not match 'Table 140'.

    Args:
        name: The table name to check.
        table_name_filter: The filter string to match against.

    Returns:
        True if the table name matches the filter as a whole word.

    """
    pattern = re.escape(table_name_filter.lower()) + r"(?!\d)"
    return bool(re.search(pattern, name.lower()))


def camelot_bbox_to_pdfplumber(
    bbox: tuple,
    page_height: float,
) -> tuple:
    """Convert Camelot bbox to pdfplumber coordinate space.

    Camelot uses bottom-left origin, pdfplumber uses top-left origin.

    Args:
        bbox: Bounding box from Camelot as (x1, y1, x2, y2).
        page_height: Height of the page in points.

    Returns:
        Bounding box in pdfplumber coordinates as (x0, y0, x1, y1).

    """
    x0, y0, x1, y1 = bbox
    return (x0, page_height - y1, x1, page_height - y0)


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
        1 for a, b in zip(row, header) if str(a).strip() == str(b).strip()
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
        is_dup = any(_is_header_row(row, h, threshold) for h in headers)
        if not is_dup:
            cleaned.append(row)

    return cleaned


def _exclude_cols(
    rows: list[list],
    exclude_columns: list[int],
) -> list[list]:
    """Exclude columns by index from a list of rows.

    Args:
        rows: List of rows to filter.
        exclude_columns: List of column indices to exclude.

    Returns:
        Rows with the specified columns removed.

    """
    return [
        [
            cell
            for col_idx, cell in enumerate(row)
            if col_idx not in exclude_columns
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

        for i, page_num in enumerate(pages_to_process, start=1):
            print(
                f"Processing page {page_num} ({i}/{total})...",
                end="\r",
            )

            tables = camelot.read_pdf(
                pdf_path,
                pages=str(page_num),
                flavor="lattice",
            )

            page = pdf.pages[page_num - 1]
            page_height = page.height

            for table in tables:
                plumber_bbox = camelot_bbox_to_pdfplumber(
                    table._bbox, page_height
                )
                name = get_table_name(page, plumber_bbox)

                if table_name_filter:
                    is_match = matches_filter(name, table_name_filter)
                    is_cont = is_continued_table(name) and matches_filter(
                        name, table_name_filter
                    )
                    if not is_match and not is_cont:
                        continue

                # Remove duplicate headers immediately per page
                rows = _remove_duplicate_headers(
                    table.df.values.tolist(),
                    header_rows=header_rows,
                )
                clean_df = pd.DataFrame(rows)

                print(
                    f"  Found '{name}' on page {page_num} "
                    f"({clean_df.shape[0]} rows, "
                    f"accuracy: {table.accuracy:.1f}%)"
                )

                all_tables.append({
                    "page": page_num,
                    "bbox": table._bbox,
                    "df": clean_df,
                    "name": name,
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

    for i, table in enumerate(all_tables):
        if i in skip_indices:
            continue

        merged_df = table["df"].copy()
        merged_name = table["name"]
        start_page = table["page"]

        j = i + 1
        while j < len(all_tables):
            next_table = all_tables[j]

            if next_table["page"] > all_tables[j - 1]["page"] + 1:
                break

            if is_continued_table(next_table["name"]) and same_table(
                merged_name, next_table["name"]
            ):
                # Unconditionally strip header rows from continuation
                continuation_df = next_table["df"].iloc[header_rows:]

                merged_df = pd.concat(
                    [merged_df, continuation_df],
                    ignore_index=True,
                )
                skip_indices.add(j)
                print(
                    f"  Merged page {next_table['page']} "
                    f"continuation into '{merged_name}'"
                )
                j += 1
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
    exclude_columns: list[int] | None = None,
) -> None:
    """Save merged tables to CSV files.

    Args:
        merged_tables: List of merged table dicts.
        output_path: Directory path to save the CSV files.
        exclude_columns: Optional list of column indices to exclude.

    """
    for idx, table in enumerate(merged_tables, start=1):
        safe_name = "".join(
            c if c.isalnum() or c in " _-" else "_" for c in table["name"]
        )
        safe_name = safe_name.strip() or f"table{idx}"

        csv_file = output_path / f"page{table['start_page']}_{safe_name}.csv"

        rows = table["df"].values.tolist()
        if exclude_columns:
            rows = _exclude_cols(rows, exclude_columns)

        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        print(f"  Saved: {csv_file} ({len(rows)} rows)")


def extract_tables_from_pdf(
    pdf_path: str,
    output_dir: str = "tables",
    table_name_filter: str | None = None,
    page_range: str = "all",
    header_rows: int = 2,
    exclude_columns: list[int] | None = None,
) -> None:
    """Extract all tables from a PDF file and save each as a CSV.

    Tables spanning multiple pages are merged into a single file.
    The filename includes the table name extracted from the text
    above each table.

    Args:
        pdf_path: Path to the PDF file to extract tables from.
        output_dir: Directory to save the extracted CSV files.
        table_name_filter: Optional string to filter tables by name.
            Only tables whose name contains this string will be
            extracted. Defaults to None (all tables).
        page_range: Page range to process e.g. '78-105' or 'all'.
            Defaults to 'all'.
        header_rows: Number of rows forming the header block.
            Used to detect and remove repeated headers. Defaults
            to 2.
        exclude_columns: Optional list of column indices to exclude
            from the output. Defaults to None.

    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    all_tables = _collect_tables(
        pdf_path, table_name_filter, page_range, header_rows
    )

    print(
        f"\nFound {len(all_tables)} matching tables. "
        f"Merging multi-page tables..."
    )

    merged_tables = _merge_tables(all_tables, header_rows)

    print(f"\nSaving {len(merged_tables)} tables to '{output_path}'...")

    _save_to_csv(merged_tables, output_path, exclude_columns)

    print(f"\nDone. {len(merged_tables)} tables saved.")


if __name__ == "__main__":
    script_dir = Path(__file__).parent
    pdf_files = list(script_dir.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in script directory.")
    else:
        print(f"Found {len(pdf_files)} PDF file(s) to process.")
        for pdf_file in pdf_files:
            print(f"\nProcessing: {pdf_file.name}")
            extract_tables_from_pdf(
                str(pdf_file),
                output_dir=str(script_dir / "tables" / pdf_file.stem),
                table_name_filter="Table 14",
                page_range="78-105",
                header_rows=2,
                exclude_columns=list(range(10))
                + list(range(11, 14))
                + list(range(17, 18)),
            )
