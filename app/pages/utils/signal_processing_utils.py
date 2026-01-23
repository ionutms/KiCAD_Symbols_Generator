"""Signal Processing Utilities.

This module provides a comprehensive collection of utility functions for
signal processing, data generation, file handling, and visualization tasks.
It includes tools for working with sine waves, CSV files, ZIP archives,
and Plotly graphs.

Key functionalities:
1. Signal generation: Create sine wave data with customizable parameters
2. Data manipulation: Process and transform pandas DataFrames
3. File operations: Handle CSV files and ZIP archives
4. Visualization: Generate and customize Plotly figures for signal data
5. Data extraction and validation: Parse specific information from CSV files
6. Multi-axis plotting: Create and configure plots with multiple y-axes

The utilities in this module are designed to support various signal processing
workflows, from data generation and manipulation to analysis and
visualization.
They can handle multiple CSV files within ZIP archives, extract specific
information, and create complex multi-axis plots.

Functions in this module can be used individually or combined to create more
complex signal processing pipelines. They support operations such as:
- Generating synthetic sine wave data with added noise
- Creating ZIP files with multiple CSV files
- Extracting and processing data from ZIP archives
- Configuring and styling Plotly figures with multiple y-axes
- Filtering and selecting specific data for visualization

This module is particularly useful for tasks involving time-series data,
multi-channel signals, and comparative data analysis across multiple files.

Functions:
    write_data_frame_to_buffer: Write a DataFrame to a StringIO buffer.
    generate_sine_wave_data: Generate sine wave data with added noise.
    create_zip_file: Generate multiple CSV files and package into a zip file.
    count_csv_files_from_zip: Count CSV files in a zip archive.
    find_first_empty_row_index: Find consistent first empty row across CSVs.
    extract_info_from_zip: Extract specific information from CSV files in zip.
    read_and_validate_zip: Read and validate a zip file from encoded contents.
    get_csv_file_list: Get list of CSV files from zip, applying filters.
    create_and_style_figure: Create and style a Plotly figure.
    process_one_csv_file_for_scatter_data: Process CSV file for scatter data.
    process_multiple_csv_files_for_scatter_data: Process multiple CSV files.
    plot_selected_zip_contents: Plot selected contents from zip with CSVs.
    create_base_layout_configuration: Create base layout for Plotly figure.
    update_layout_with_y_axes: Update layout with multiple y-axes.
    separate_left_right_axes: Separate y-axes into left and right lists.
    update_x_axis_domain: Update x-axis domain based on y-axes.
    calculate_axis_positions: Calculate positions for each y-axis.
    add_y_axes_to_layout: Add y-axes configurations to the layout.
    create_y_axis_config: Create configuration for a single y-axis.
    get_csv_files_from_zip: Get CSV files from zip, applying filters.
    process_csv_file_for_data_frame_extraction: Process CSV for column names.
    extract_data_frame_from_zip_contents: Extract data from CSVs in zip file.
"""

import base64
import csv
import io
import itertools
import zipfile
from typing import Any, Dict, List, Tuple, Union

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate


def write_data_frame_to_buffer(
    data_frame: pd.DataFrame, buffer: io.StringIO, header: bool = True
) -> None:
    """Write a DataFrame to a StringIO buffer.

    Args:
        data_frame (pd.DataFrame): The DataFrame to write.
        buffer (io.StringIO): The buffer to write to.
        header (bool, optional):
            Whether to write the header. Defaults to True.

    """
    data_frame.to_csv(buffer, index=False, header=header)
    buffer.write("\n")


def generate_sine_wave_data(
    records: int,
    channels: int,
    sample_interval: float,
    noise_level: float = 0.01,
) -> pd.DataFrame:
    """Generate sine wave data with added noise for multiple channels.

    Args:
        records (int): Number of data points to generate.
        channels (int): Number of channels to generate data for.
        sample_interval (float): Total time interval for the data.
        noise_level (float): Standard deviation of the Gaussian noise to add.

    Returns:
        pd.DataFrame: DataFrame with TIME and channel columns.

    """
    half_interval = sample_interval / 2
    time_points = np.linspace(-half_interval, half_interval, records)

    total_time_range = 2 * half_interval
    frequency = 6 / total_time_range
    ch_values = 3 * np.sin(2 * np.pi * frequency * time_points)

    data = {"TIME": time_points}
    for channel_index in range(1, channels + 1):
        noise = np.random.normal(0, noise_level, records)
        data[f"CH{channel_index}"] = ch_values + noise

    return pd.DataFrame(data)


def create_zip_file(
    app_state: Dict[str, Any],
    channel_data: Dict[str, Any],
    base_filename: str,
    module_prefix: str,
) -> bytes:
    """Generate multiple CSV files and package them into a zip file.

    This function creates a zip file containing multiple CSV files. Each CSV
    file includes channel data and repeated sine wave data based on the
    specified parameters.

    The function uses in-memory buffers to create the CSV content and the zip
    file, avoiding the need for temporary files on disk.

    Args:
        app_state:
            A dictionary containing the current state of the application,
            including button states for number of files, records, channels,
            and frames.
        channel_data:
            A dictionary containing channel data and column information.
        base_filename: Base name for the CSV files.
        module_prefix: Prefix used to construct state keys.

    Returns:
        The content of the zip file as a bytes object.

    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(
        zip_buffer, "a", zipfile.ZIP_DEFLATED, False
    ) as zip_archive:
        for file_index in range(
            int(app_state[f"{module_prefix}_csv_files_button"])
        ):
            csv_buffer = io.StringIO()

            # Create DataFrame with channel data
            channel_df = pd.DataFrame(data=channel_data["channel_data"])
            column_names = [
                col_info["name"][0] for col_info in channel_data["columns"]
            ]
            channel_df.columns = column_names
            write_data_frame_to_buffer(channel_df, csv_buffer)

            # Generate and add sine wave data
            sine_wave_df = generate_sine_wave_data(
                int(app_state[f"{module_prefix}_records_button"]),
                int(app_state[f"{module_prefix}_channels_button"]),
                float(app_state[f"{module_prefix}_sample_interval_button"]),
                noise_level=0.2 - 0.05 * file_index,
            )

            repeated_sine_df = pd.concat(
                [sine_wave_df]
                * int(app_state[f"{module_prefix}_frames_button"]),
                ignore_index=True,
            )
            write_data_frame_to_buffer(repeated_sine_df, csv_buffer)

            # Add CSV content to zip file
            output_filename = (
                f"{base_filename.split('.')[0]}_{file_index + 1}.csv"
            )
            zip_archive.writestr(output_filename, csv_buffer.getvalue())

    return zip_buffer.getvalue()


def count_csv_files_from_zip(file_contents: str) -> int:
    """Count the number of CSV files in a zip archive.

    Args:
        file_contents (str): Base64 encoded string of the zip file contents.

    Returns:
        int: Number of CSV files found in the zip archive.

    """
    try:
        decoded_contents = base64.b64decode(file_contents.split(",")[1])
    except IndexError:
        decoded_contents = base64.b64decode(file_contents)

    with zipfile.ZipFile(io.BytesIO(decoded_contents)) as zip_file:
        csv_file_list = [
            csv_file
            for csv_file in zip_file.namelist()
            if csv_file.lower().endswith(".csv")
        ]
    return len(csv_file_list)


def find_first_empty_row_index(
    zip_file: zipfile.ZipFile, csv_file_list: List[str], chunk_size: int = 20
) -> int:
    """Find the consistent first empty row index across multiple CSV files.

    An empty row is defined as a row where all fields are empty or contain
    only whitespace. The function returns the index of the first empty row
    if it's consistent across all CSV files, otherwise 0.

    The function reads CSV files in chunks to handle large files efficiently.

    Args:
        zip_file (zipfile.ZipFile): The ZIP file containing CSV files.
        csv_file_list (List[str]): List of CSV file names in the ZIP file.
        chunk_size (int): Number of rows to read in each chunk. Default 20.

    Returns:
        int:
            The index of the first empty row (0-based) if consistent
            across all CSVs, or 0 if not consistent or not found.

    """

    def process_csv(file):
        csv_reader = csv.reader(io.TextIOWrapper(file, "utf-8"))
        for chunk_start, chunk in enumerate(
            iter(lambda: list(itertools.islice(csv_reader, chunk_size)), [])
        ):
            for row_index, row in enumerate(chunk):
                if not any(field.strip() for field in row):
                    return chunk_start * chunk_size + row_index
        return 0

    first_empty_row_index_list: List[int] = []

    for csv_file_name in csv_file_list:
        with zip_file.open(csv_file_name) as file:
            first_empty_row_index_list.append(process_csv(file))

    results = {"first_empty_row_index": 0}

    if first_empty_row_index_list and all(
        index == first_empty_row_index_list[0]
        for index in first_empty_row_index_list
    ):
        results["first_empty_row_index"] = first_empty_row_index_list[0] - 1

    return results


def extract_info_from_zip(
    file_contents: str, keywords: List[str]
) -> Dict[str, Union[str, List[str]]]:
    """Extract specific information from CSV files in a zip archive.

    Args:
        file_contents (str): Base64 encoded string of the zip file contents.
        keywords (List[str]): List of keywords to search for in the CSV files.

    Returns:
        Dict[str, Union[str, List[str]]]:
            Dictionary with keywords as keys and either a single string,
            if all values are the same, or a list of unique strings as values.

    """

    def process_csv_file(file_object, search_keywords):
        csv_reader = csv.reader(io.TextIOWrapper(file_object, "utf-8"))
        chunk = list(itertools.islice(csv_reader, 20))
        return {
            keyword: [
                row[index + 1]
                for row in chunk
                for index, cell in enumerate(row)
                if cell == keyword and index + 1 < len(row)
            ]
            for keyword in search_keywords
        }

    def simplify_result_values(value_list):
        unique_values = list(dict.fromkeys(value_list))
        return unique_values[0] if len(unique_values) == 1 else unique_values

    try:
        decoded_contents = base64.b64decode(file_contents.split(",")[1])
    except IndexError:
        decoded_contents = base64.b64decode(file_contents)
    extraction_results = {keyword: [] for keyword in keywords}

    with zipfile.ZipFile(io.BytesIO(decoded_contents)) as zip_archive:
        csv_file_list = [
            filename
            for filename in zip_archive.namelist()
            if filename.lower().endswith(".csv")
        ]
        for csv_filename in csv_file_list:
            with zip_archive.open(csv_filename) as csv_file:
                file_results = process_csv_file(csv_file, keywords)
                for keyword, values in file_results.items():
                    extraction_results[keyword].extend(values)
    return {
        keyword: simplify_result_values(values)
        for keyword, values in extraction_results.items()
    }


def read_and_validate_zip(
    file_contents: str, file_name: str
) -> zipfile.ZipFile:
    """Read and validate a zip file from base64 encoded contents.

    Args:
        file_contents (str): Base64 encoded file contents.
        file_name (str): Name of the file.

    Returns:
        zipfile.ZipFile: A ZipFile object.

    Raises:
        ValueError: If the file is not a zip file.

    """
    if not file_name.lower().endswith(".zip"):
        raise ValueError("Not a zip file")
    try:
        decoded_contents = base64.b64decode(file_contents.split(",")[1])
    except IndexError:
        decoded_contents = base64.b64decode(file_contents)
    return zipfile.ZipFile(io.BytesIO(decoded_contents))


def get_csv_file_list(
    zip_file: zipfile.ZipFile, filtering: Dict[str, Any]
) -> List[str]:
    """Get a list of CSV files from the zip file, applying any filters.

    Args:
        zip_file (zipfile.ZipFile): The zip file object.
        filtering (Dict[str, Any]):
            Dictionary containing filtering information.

    Returns:
        List[str]: List of CSV file names.

    Raises:
        ValueError: If no CSV files are found in the zip.

    """
    csv_file_list = [
        csv_file
        for csv_file in zip_file.namelist()
        if csv_file.lower().endswith(".csv")
    ]
    if not csv_file_list:
        raise ValueError("No CSV files found in zip")
    try:
        return [
            item
            for index, item in enumerate(csv_file_list)
            if index in set(filtering["files_to_keep"])
        ]
    except KeyError:
        return csv_file_list


def create_and_style_figure(
    figure_data: List[go.Scatter],
    theme_switch: bool,
    figure_layout: Dict[str, Any],
) -> go.Figure:
    """Create and style a Plotly figure.

    Args:
        figure_data (List[go.Scatter]): List of Scatter objects to plot.
        theme_switch (bool):
            Boolean indicating light (True) or dark (False) theme.
        figure_layout (Dict[str, Any]):
            Additional layout parameters for the figure.

    Returns:
        go.Figure: A styled Plotly figure.

    """
    scatter_fig = go.Figure(data=figure_data, layout=figure_layout)

    theme = {
        "template": "plotly" if theme_switch else "plotly_dark",
        "paper_bgcolor": "white" if theme_switch else "#222222",
        "plot_bgcolor": "white" if theme_switch else "#222222",
        "font_color": "black" if theme_switch else "white",
        "margin": {"l": 10, "r": 10, "t": 10, "b": 10},
    }

    scatter_fig.update_layout(**theme)
    scatter_fig.update_layout(
        height=600,
        legend={
            "visible": True,
            "orientation": "h",
            "yanchor": "bottom",
            "y": -0.25 + (-0.025 * len(figure_data)),
            "xanchor": "center",
            "x": 0.5,
        },
        shapes=[
            {
                "type": "rect",
                "xref": "paper",
                "yref": "paper",
                "x0": figure_layout["xaxis"]["domain"][0],
                "x1": figure_layout["xaxis"]["domain"][1],
                "y0": 0,
                "y1": 1,
                "line": {"width": 1, "dash": "dot"},
            }
        ],
    )

    return scatter_fig


def process_one_csv_file_for_scatter_data(
    zip_file: zipfile.ZipFile,
    csv_file_name: str,
    filtering: Dict[str, Any],
    process_result: Dict[str, Any],
) -> List[go.Scatter]:
    """Process a single CSV file and generate scatter data.

    Args:
        zip_file (zipfile.ZipFile): The zip file object.
        csv_file_name (str): Name of the CSV file to process.
        filtering (Dict[str, Any]):
            Dictionary containing filtering information.
        process_result (Dict[str, Any]):
            Dictionary containing processing results.

    Returns:
        List[go.Scatter]: List of Scatter objects for plotting.

    """
    csv_contents = zip_file.read(csv_file_name).decode("utf-8")
    skiprows = process_result["first_empty_row_index"] + 1
    data_frame = pd.read_csv(io.StringIO(csv_contents), skiprows=skiprows)

    scatter_data = []
    records_slice = filtering["records_slice"]
    slice_size = records_slice[1] - records_slice[0]

    for frame_index in filtering["frames_to_keep"]:
        start = filtering["records_max"] * frame_index + records_slice[0]
        for channel_name in filtering["y_axis_data"]:
            trace_name = (
                f"{channel_name} frame{frame_index + 1} {csv_file_name}"
            )

            yaxis = "y"
            if "y_axis_selection" in list(filtering.keys()):
                if channel_name in list(filtering["y_axis_selection"].keys()):
                    yaxis = filtering["y_axis_selection"][channel_name]

            scatter_data.append(
                go.Scatter(
                    x=data_frame[filtering["x_axis_data"]][
                        start : start + slice_size
                    ],
                    y=data_frame[f"{channel_name}"][
                        start : start + slice_size
                    ],
                    yaxis=yaxis,
                    name=trace_name,
                    legendgroup=channel_name
                    if filtering.get("legend_group")
                    else None,
                )
            )
    return scatter_data


def process_multiple_csv_files_for_scatter_data(
    validated_zip: zipfile.ZipFile,
    csv_files: List[str],
    skiprows: int,
    filtering: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """Process multiple CSV files from a ZIP archive.

    This function iterates through the provided CSV files, processes each one
    to extract scatter plot data, and combines the results into a single list.

    Args:
        validated_zip (ZipFile):
            A validated ZIP file object containing the CSV files.
        csv_files (List[str]): A list of CSV file names to process.
        skiprows (int):
            The number of rows to skip at the beginning of each CSV file.
        filtering (Dict[str, Any]):
            A dictionary containing filtering criteria.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary
        represents a trace for a scatter plot.

    Raises:
        KeyError: If there's an issue accessing required keys in the CSV data
        or filter information. The error is caught and ignored, returning
        whatever data was successfully processed.

    """
    scatter_data_list = []
    for csv_file_name in csv_files:
        for trace in process_one_csv_file_for_scatter_data(
            validated_zip, csv_file_name, filtering, skiprows
        ):
            scatter_data_list.append(trace)
    return scatter_data_list


def plot_selected_zip_contents(
    zip_contents: str,
    zip_name: str,
    filtering: Dict[str, Any],
    use_selected_theme: bool,
) -> go.Figure:
    """Plot selected contents from a zip files.

    Args:
        zip_contents (str): Base64 encoded file contents.
        zip_name (str): Name of the zip file.
        filtering (Dict[str, Any]):
            Dictionary containing filtering information.
        use_selected_theme (bool):
            Indicates light (True) or dark (False) theme.

    Returns:
        go.Figure:
            A Plotly figure object with multiple y-axes,
            or PreventUpdate if an error occurs.

    """
    try:
        validated_zip = read_and_validate_zip(zip_contents, zip_name)
        csv_file_names = get_csv_file_list(validated_zip, filtering)
        skiprows = find_first_empty_row_index(validated_zip, csv_file_names)

        scatter_data = process_multiple_csv_files_for_scatter_data(
            validated_zip, csv_file_names, skiprows, filtering
        )

        layout_configuration = create_base_layout_configuration(filtering)
        update_layout_with_y_axes(layout_configuration, filtering)

        return create_and_style_figure(
            scatter_data, use_selected_theme, layout_configuration
        )

    except (base64.binascii.Error, zipfile.BadZipFile, ValueError) as error:
        print(f"Error: {str(error)}")
        return PreventUpdate


def create_base_layout_configuration(
    filtering: Dict[str, Any],
) -> Dict[str, Any]:
    """Create the base layout configuration for the plot.

    Args:
        filtering (Dict[str, Any]):
            Dictionary containing filtering information.

    Returns:
        Dict[str, Any]: Base layout configuration.

    """
    return {
        "xaxis": {
            "gridcolor": "#808080",
            "griddash": "dash",
            "zerolinecolor": "lightgray",
            "zeroline": False,
            "title": {"text": filtering["Horizontal Units"], "standoff": 5},
            "domain": (0.0, 1.0),
        },
        "yaxis": {
            "gridcolor": "#808080",
            "griddash": "dash",
            "zerolinecolor": "lightgray",
            "zeroline": False,
            "tickangle": -90,
            "position": 0.0,
            "anchor": "free",
            "title": {"text": filtering["Vertical Units"], "standoff": 5},
        },
    }


def update_layout_with_y_axes(
    layout_configuration: Dict[str, Any], filtering: Dict[str, Any]
) -> None:
    """Update the layout configuration with multiple y-axes.

    Args:
        layout_configuration (Dict[str, Any]):
            The layout configuration to update.
        filtering (Dict[str, Any]):
            Dictionary containing filtering information.

    """
    try:
        y_selection = list(filtering["y_axis_selection"].values())
        y_side = list(filtering["y_axis_side"].values())
        left_list, right_list = separate_left_right_axes(y_selection, y_side)

        update_x_axis_domain(layout_configuration, left_list, right_list)
        positions = calculate_axis_positions(left_list, right_list)
        add_y_axes_to_layout(
            layout_configuration, left_list, right_list, positions, filtering
        )

    except KeyError:
        pass


def separate_left_right_axes(
    y_selection: List[str], y_side: List[bool]
) -> Tuple[List[str], List[str]]:
    """Separate y-axes into left and right lists.

    Args:
        y_selection (List[str]): List of y-axis selections.
        y_side (List[bool]):
            List of booleans indicating right (True) or left (False).

    Returns:
        Tuple[List[str], List[str]]: Left and right y-axis lists.

    """
    left_list = [
        item
        for item, flag in zip(y_selection, y_side)
        if not flag and item != "y"
    ]
    right_list = [
        item
        for item, flag in zip(y_selection, y_side)
        if flag and item != "y"
    ]
    return left_list, right_list


def update_x_axis_domain(
    layout_configuration: Dict[str, Any],
    left_list: List[str],
    right_list: List[str],
) -> None:
    """Update the x-axis domain based on the number of left and right y-axes.

    Args:
        layout_configuration (Dict[str, Any]):
            The layout configuration to update.
        left_list (List[str]): List of left y-axes.
        right_list (List[str]): List of right y-axes.

    """
    left_side_domain = len(set(left_list)) * 0.05 if left_list else 0.0
    right_side_domain = (
        1.05 - len(set(right_list)) * 0.05 if right_list else 1.0
    )
    layout_configuration["xaxis"]["domain"] = (
        left_side_domain,
        right_side_domain,
    )


def calculate_axis_positions(
    left_list: List[str], right_list: List[str]
) -> Dict[str, float]:
    """Calculate the positions for each y-axis.

    Args:
        left_list (List[str]): List of left y-axes.
        right_list (List[str]): List of right y-axes.

    Returns:
        Dict[str, float]: Dictionary of axis positions.

    """
    positions = {
        item: round((i + 1) * 0.05, 2)
        for i, item in enumerate(set(left_list))
    }
    positions.update({
        item: round(1.0 - i * 0.05, 2)
        for i, item in enumerate(set(right_list))
    })
    return positions


def add_y_axes_to_layout(
    layout_configuration: Dict[str, Any],
    left_list: List[str],
    right_list: List[str],
    positions: Dict[str, float],
    filtering: Dict[str, Any],
) -> None:
    """Add y-axes configurations to the layout.

    Args:
        layout_configuration (Dict[str, Any]):
            The layout configuration to update.
        left_list (List[str]): List of left y-axes.
        right_list (List[str]): List of right y-axes.
        positions (Dict[str, float]): Dictionary of axis positions.
        filtering (Dict[str, Any]):
            Dictionary containing filtering information.

    """
    for name, is_right in zip(
        left_list + right_list,
        [False] * len(left_list) + [True] * len(right_list),
    ):
        axis_config = create_y_axis_config(
            name, positions, filtering, is_right
        )
        layout_configuration[f"{name.replace('y', 'yaxis')}"] = axis_config


def create_y_axis_config(
    name: str,
    positions: Dict[str, float],
    filtering: Dict[str, Any],
    is_right: bool,
) -> Dict[str, Any]:
    """Create configuration for a single y-axis.

    Args:
        name (str): Name of the y-axis.
        positions (Dict[str, float]): Dictionary of axis positions.
        filtering (Dict[str, Any]):
            Dictionary containing filtering information.
        is_right (bool): Whether the axis is on the right side.

    Returns:
        Dict[str, Any]: Configuration for the y-axis.

    """
    config = {
        "overlaying": "y",
        "showgrid": False,
        "zeroline": False,
        "position": positions[name],
        "tickangle": -90,
        "title": {"text": filtering["Vertical Units"], "standoff": 5},
    }
    if is_right:
        config["side"] = "right"
    return config


def get_csv_files_from_zip(
    zip_file: zipfile.ZipFile, filtering: Dict[str, Any]
) -> List[str]:
    """Get a list of CSV files from the zip file, applying any filters.

    Args:
        zip_file (zipfile.ZipFile): The zip file object.
        filtering (Dict[str, Any]):
            Dictionary containing filtering information.

    Returns:
        List[str]: List of CSV file names.

    """
    csv_file_list = [
        csv_file
        for csv_file in zip_file.namelist()
        if csv_file.lower().endswith(".csv")
    ]
    try:
        return [
            item
            for index, item in enumerate(csv_file_list)
            if index not in set(filtering.get("files_to_remove", []))
        ]
    except KeyError:
        return csv_file_list


def process_csv_file_for_data_frame_extraction(
    zip_file: zipfile.ZipFile,
    csv_file_name: str,
    process_result: Dict[str, Any],
) -> List[str]:
    """Process a single CSV file and extract its column names.

    This function reads a CSV file from a zip archive, skips rows up to the
    first empty row, and returns the column names of the CSV.

    Args:
        zip_file (zipfile.ZipFile): The zip file object.
        csv_file_name (str): Name of the CSV file to process.
        process_result (Dict[str, Any]): Dictionary containing processing
            results, including the index of the first empty row.

    Returns:
        List[str]: A list of column names from the CSV file.

    """
    csv_contents = zip_file.read(csv_file_name).decode("utf-8")
    data_frame = pd.read_csv(
        io.StringIO(csv_contents),
        skiprows=process_result["first_empty_row_index"] + 1,
        nrows=1,
    )
    return list(data_frame.columns)


def extract_data_frame_from_zip_contents(
    file_contents: str, file_name: str, filtering: Dict[str, Any]
) -> List[List[str]]:
    """Parse and extract contents of CSV files within an uploaded ZIP file.

    Args:
        file_contents (str): Base64 encoded contents of the ZIP file.
        file_name (str): Name of the uploaded ZIP file.
        filtering (Dict[str, Any]):
            Dictionary containing filtering information.

    Returns:
        List[List[str]]:
            A list of lists representing the extracted data frame contents,
            or an empty list if an error occurs or no matching CSV files are
            found.

    """
    if not file_name.lower().endswith(".zip"):
        print("Please upload a zip file.")
        return []

    try:
        try:
            decoded_contents = base64.b64decode(file_contents.split(",")[1])
        except IndexError:
            decoded_contents = base64.b64decode(file_contents)

        with zipfile.ZipFile(io.BytesIO(decoded_contents)) as zip_file:
            csv_files = get_csv_files_from_zip(zip_file, filtering)

            if not csv_files:
                print("No CSV files found in the zip archive.")
                return []

            first_empty_row_index = find_first_empty_row_index(
                zip_file, csv_files
            )

            data_frames = [
                process_csv_file_for_data_frame_extraction(
                    zip_file, csv_file, first_empty_row_index
                )
                for csv_file in csv_files
            ]

        return (
            data_frames[0]
            if len(set(tuple(map(tuple, df)) for df in data_frames)) == 1
            else []
        )

    except (base64.binascii.Error, zipfile.BadZipFile) as error_msg:
        print(f"There was an error processing the file: {str(error_msg)}")
        return []
