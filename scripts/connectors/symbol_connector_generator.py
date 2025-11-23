"""KiCad Connector Symbol Generator.

Generates KiCad symbol files for connectors from CSV data.
Modified to match specific pin and field positioning requirements.
"""

# import sys
from pathlib import Path
from typing import TextIO

# Add the parent directory to sys.path to import symbol_connectors_specs
# sys.path.append(str(Path(__file__).parent))
import symbol_connectors_specs
from utilities import file_handler_utilities, symbol_utils


def generate_kicad_symbol(
    input_csv_file: str,
    output_symbol_file: str,
) -> None:
    """Generate a KiCad symbol file from CSV data for connectors.

    Args:
        input_csv_file (str): Path to the input CSV file with component data.
        output_symbol_file (str): Path for the output .kicad_sym file.

    Returns:
        None

    """
    component_data_list = file_handler_utilities.read_csv_data(input_csv_file)
    all_properties = symbol_utils.get_all_properties(component_data_list)

    with Path.open(output_symbol_file, "w", encoding="utf-8") as symbol_file:
        symbol_utils.write_header(symbol_file)
        for component_data in component_data_list:
            write_component(symbol_file, component_data, all_properties)
        symbol_file.write(")")


def write_component(
    symbol_file: TextIO,
    component_data: dict[str, str],
    property_order: list[str],
) -> None:
    """Write a single component to the KiCad symbol file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        component_data (Dict[str, str]): Data for a single component.
        property_order (List[str]): Ordered list of property names.

    Returns:
        None

    """
    symbol_name = component_data.get("Symbol Name", "")
    number_of_rows = int(component_data.get("Number of Rows", "1"))
    symbol_utils.write_symbol_header(symbol_file, symbol_name)
    pin_count = int(component_data.get("Pin Count", "1"))
    row_count = int(component_data.get("Number of Rows", "1"))

    series_name = component_data.get("Series", "")
    rectangle_width = symbol_connectors_specs.SYMBOLS_SPECS[
        series_name
    ].rectangle_width

    rect_half_width = rectangle_width / 2

    extra_offset = (
        ((pin_count / row_count) / 2)
        if row_count == 1
        else (pin_count / row_count)
    )

    symbol_utils.write_properties(
        symbol_file,
        component_data,
        property_order,
        1 + extra_offset,
        rect_half_width + 2.54,
    )

    write_symbol_drawing(
        symbol_file,
        symbol_name,
        component_data,
        number_of_rows,
    )
    symbol_file.write(")")


def write_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
    component_data: dict[str, str],
    number_of_rows: int,
) -> None:
    """Write the drawing for a connector symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
        component_data (Dict[str, str]): Data for the component.
        number_of_rows (int): Number of rows of the symbol.

    Returns:
        None

    """
    pin_count = int(component_data.get("Pin Count", "2"))
    pin_spacing = 2.54

    series_name = component_data.get("Series", "")
    series_spec = symbol_connectors_specs.SYMBOLS_SPECS[series_name]
    rectangle_width = series_spec.rectangle_width
    rect_half_width = rectangle_width / 2

    # Use per-series symbol pin length if provided
    pin_length = getattr(series_spec, "symbol_pin_length", 2.54)

    # Compute X positions for pin anchors
    left_pin_x_default = -rect_half_width - pin_length
    right_pin_x_default = rect_half_width + pin_length
    left_pin_x = left_pin_x_default
    right_pin_x = right_pin_x_default

    min_height = 7.62
    calculated_height = (pin_count * pin_spacing) + 2.54
    rectangle_height = max(min_height, calculated_height)

    symbol_file.write(f'\t\t(symbol "{symbol_name}_0_0"\n')

    start_y = (pin_count - 1) * pin_spacing / 2

    if number_of_rows == 2:  # noqa: PLR2004
        # Support using provided pin_names order without sorting
        left_keys: list[str] | None = None
        right_keys: list[str] | None = None
        if series_spec.pin_names:
            keys = list(series_spec.pin_names.keys())
            pins_per_side = pin_count
            if len(keys) == pin_count * 2:
                left_keys = keys[:pins_per_side]
                right_keys = keys[pins_per_side:]

        for index, pin_num in enumerate(range(1, pin_count * 2, 2)):
            y_pos = start_y - (pin_num - 1) * pin_spacing / 2
            # Left pin identifier
            left_id = (
                left_keys[index]
                if (left_keys is not None and index < len(left_keys))
                else str(pin_num)
            )
            pin_name = (
                series_spec.pin_names.get(left_id, "")
                if series_spec.pin_names
                else ""
            )
            symbol_utils.write_pin(
                symbol_file,
                left_pin_x,
                y_pos,
                0,
                left_id,
                pin_name,
                length=pin_length,
                pin_type="passive",
            )
            # Right pin identifier (reverse order on right)
            right_index = (
                (len(right_keys) - 1 - index)
                if right_keys is not None
                else None
            )
            right_id = (
                right_keys[right_index]
                if (
                    right_keys is not None
                    and 0 <= right_index < len(right_keys)
                )
                else str(pin_num + 1)
            )
            pin_name = (
                series_spec.pin_names.get(right_id, "")
                if series_spec.pin_names
                else ""
            )
            symbol_utils.write_pin(
                symbol_file,
                right_pin_x,
                y_pos,
                180,
                right_id,
                pin_name,
                length=pin_length,
                pin_type="passive",
            )
    else:
        # Determine numbering order: use pin_names keys if provided
        if series_spec.pin_names:
            # Use provided order directly for single row
            pin_numbers = list(series_spec.pin_names.keys())
        else:
            pin_numbers = list(range(1, pin_count + 1))

        for index, pin_num in enumerate(pin_numbers):
            y_pos = start_y - index * pin_spacing
            key = str(pin_num)
            pin_name = (
                series_spec.pin_names.get(key, "")
                if series_spec.pin_names
                else ""
            )
            symbol_utils.write_pin(
                symbol_file,
                left_pin_x,
                y_pos,
                0,
                str(pin_num),
                pin_name,
                length=pin_length,
                pin_type="passive",
            )

    symbol_file.write("\t\t)\n")

    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')
    write_rectangle(
        symbol_file,
        -rect_half_width,
        rectangle_height / 2,
        rect_half_width,
        -rectangle_height / 2,
    )
    symbol_file.write("\t\t)\n")


def write_rectangle(
    symbol_file: TextIO,
    start_x: float,
    start_y: float,
    end_x: float,
    end_y: float,
) -> None:
    """Write a rectangle to the KiCad symbol file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        start_x (float): X-coordinate of the start point.
        start_y (float): Y-coordinate of the start point.
        end_x (float): X-coordinate of the end point.
        end_y (float): Y-coordinate of the end point.

    Returns:
        None

    """
    symbol_file.write(f"""
        (rectangle
            (start {start_x} {start_y})
            (end {end_x} {end_y})
            (stroke (width 0.254) (type solid) )
            (fill (type none) )
        )
        """)
