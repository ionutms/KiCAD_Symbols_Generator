"""Signal Data Generator Page.

This module provides a Dash page for generating and downloading sample data.
It allows users to specify parameters such as number of channels, frames,
records, and sample interval. The page includes interactive controls for
data generation and a DataTable for displaying the generated data. Users can
also download the generated data as a CSV file.

The module uses Dash components and callbacks to create an interactive
interface for data generation and visualization.
"""

import sys
from typing import Any, Dict, List, Tuple, Union

import dash_bootstrap_components as dbc
import pages.utils.dash_component_utils as dcu
import pages.utils.signal_processing_utils as spu
import pandas as pd
from dash import (
    callback,
    ctx,
    dash_table,
    dcc,
    html,
    no_update,
    register_page,
)
from dash.dependencies import Input, Output, State

link_name = __name__.rsplit(".", maxsplit=1)[-1].replace("_page", "").title()
module_name = __name__.rsplit(".", maxsplit=1)[-1]

register_page(
    __name__,
    name=link_name,
    path="/signal_data_generator",
    order=3,
    exclude_from_nav=True,
)


TITLE = "Signal Data Generator"
ABOUT = (
    "The Signal Data Generator is an interactive web application for "
    "creating sample signal data with customizable parameters.",
    "It allows users to generate multiple CSV files containing channel data "
    "and sine wave data, package them into a ZIP file, and download "
    "the generated data for further analysis or testing.",
)
features = [
    "Interactive controls for specifying data generation parameters",
    "Real-time data preview using a DataTable",
    "Generation of multiple CSV files with customizable parameters",
    "Packaging of generated CSV files into a downloadable ZIP file",
    "Dynamic calculation and display of generated data size",
    "Responsive layout with theme switching support",
]
usage_steps = [
    "Use the counter controls to set the number of "
    "channels, frames, records, and sample interval.",
    "Preview the generated data in the interactive DataTable.",
    "Specify the number of CSV files to generate and set the base filename.",
    "Click the 'Check ZIP size' button to see the "
    "estimated size of the generated data.",
    "Click the 'Download ZIP' button to generate and download "
    "the CSV files in a ZIP archive.",
    "Use the theme switch to toggle between light and dark modes.",
]

layout = dbc.Container(
    [
        html.Div(
            [
                dbc.Row([dbc.Col([dcc.Link("Go back Home", href="/")])]),
                dbc.Row([
                    dbc.Col([html.H3(f"{link_name.replace('_', ' ')}")])
                ]),
                dbc.Row([
                    dcu.app_description(TITLE, ABOUT, features, usage_steps)
                ]),
                dcc.Store(id=f"{module_name}_buttons_state_store", data={}),
                dbc.Row([
                    dcu.labeled_counter_trio(
                        id_section=f"{module_name}_channels",
                        label="Select a number of channels",
                        limits={"min_count": 1, "max_count": 4},
                    ),
                    dcu.labeled_counter_trio(
                        id_section=f"{module_name}_frames",
                        label="Select a number of frames",
                        limits={"min_count": 1, "max_count": 10},
                    ),
                    dcu.labeled_counter_quintet(
                        id_section=f"{module_name}_records",
                        label="Select a number of records",
                        default_count=2,
                        limits={"min_count": 2, "max_count": 100000},
                    ),
                    dcu.labeled_counter_quintet(
                        id_section=f"{module_name}_sample_interval",
                        label="Select a sample interval",
                        limits={"min_count": 0.000001, "max_count": 1},
                    ),
                ]),
                dash_table.DataTable(
                    id="data_table", merge_duplicate_headers=False
                ),
                html.Hr(),
                dbc.Row(
                    [
                        dcu.labeled_counter_trio(
                            id_section=f"{module_name}_csv_files",
                            label="Select a number of csv files",
                            limits={"min_count": 1, "max_count": 4},
                        ),
                        dcu.create_labeled_input(
                            id_section=f"{module_name}_csv_filename",
                            label="CSV filename",
                            placeholder="Enter a filename",
                            value="my_csv_file",
                        ),
                        dcu.create_labeled_input(
                            id_section=f"{module_name}_zip_filename",
                            label="ZIP filename",
                            placeholder="Enter a filename",
                            value="my_zip_file",
                        ),
                        dcc.Store(id="data_store"),
                        dcc.Download(id="download_dataframe_csv"),
                        dbc.Col(
                            [
                                dbc.Row([
                                    dcu.create_labeled_button(
                                        f"{module_name}_check_size",
                                        "No data available",
                                        "Check ZIP size",
                                    ),
                                    dcu.create_labeled_button(
                                        f"{module_name}_download_zip",
                                        "No data to download",
                                        "Download ZIP",
                                    ),
                                ])
                            ],
                            xs=12,
                            md=3,
                        ),
                    ],
                    className="h-100",
                ),
            ],
        )
    ],
    fluid=True,
)


@callback(
    Output(f"{module_name}_csv_filename", "style"),
    Output(f"{module_name}_zip_filename", "style"),
    Input("theme_switch_value_store", "data"),
)
def update_csv_filename_input_style(switch: bool) -> Dict[str, str]:
    """Update the CSV filename input style based on the theme switch value.

    Args:
        switch (bool):
            The state of the theme switch.
            True for light theme, False for dark theme.

    Returns:
        Dict[str, str]: Style dictionary for the input.

    """
    input_style = {
        "backgroundColor": "white" if switch else "#333",
        "color": "black" if switch else "white",
        "borderColor": "#ced4da" if switch else "#6c757d",
    }
    return input_style, input_style


@callback(
    Output(f"{module_name}_buttons_state_store", "data"),
    Input("interval_component", "n_intervals"),
    Input(f"{module_name}_frames_button", "children"),
    Input(f"{module_name}_channels_button", "children"),
    Input(f"{module_name}_records_button", "children"),
    Input(f"{module_name}_csv_files_button", "children"),
    Input(f"{module_name}_sample_interval_button", "children"),
)
def store_buttons_states(*states: Any) -> Dict[str, Any]:
    """Store the current states of multiple buttons in a dictionary.

    This callback function is triggered by changes in the interval component
    or any of the specified buttons. It captures the current state of each
    button and stores it in a dictionary.

    Args:
        *states:
            Variable length argument list containing the current values
            of all Input components in the order they are specified in
            the callback decorator.

    Returns:
        A dictionary where keys are the IDs of the Input components and
        values are their current states.

    """
    # Get all input IDs
    input_ids: List[str] = [item["id"] for item in ctx.inputs_list]

    # Create a dictionary of input IDs and their current values
    input_states: Dict[str, Any] = dict(zip(input_ids, states))

    return input_states


@callback(
    Output("download_dataframe_csv", "data"),
    Output(f"{module_name}_download_zip_label", "children"),
    Output(f"{module_name}_check_size_label", "children"),
    Input(f"{module_name}_download_zip_button", "n_clicks"),
    Input(f"{module_name}_check_size_button", "n_clicks"),
    State(f"{module_name}_buttons_state_store", "data"),
    State("data_store", "data"),
    State(f"{module_name}_csv_filename", "value"),
    State(f"{module_name}_zip_filename", "value"),
    prevent_initial_call=True,
)
def download_multiple_csv(
    _download_zip_button: int,
    _check_size_button: int,
    state: Dict[str, Any],
    data_store: Dict[str, Any],
    csv_filename: str,
    zip_filename: str,
) -> Dict[str, Union[str, bytes]]:
    """Generate multiple CSV files and package them into a zip file.

    This callback function is triggered when the download multiple CSV button
    is clicked. It generates the specified number of CSV files, each
    containing channel data and sine wave data, and packages them into a
    single zip file for download.

    Args:
        _download_zip_button (int):
            Number of times the download button was clicked.
        _check_size_button (int):
            Number of times the check size button was clicked.
        state (Dict[str, Any]): Dictionary containing the current states
            of various input components.
        data_store (Dict[str, Any]): Dictionary containing the data to be
            downloaded and column information for the DataFrame.
        csv_filename (str): The base name for the CSV files to be generated.
        zip_filename (str): The name for the resulting zip file.

    Returns:
        Dict[str, Union[str, bytes]]: A dictionary with zip file data for
        download, compatible with Dash's dcc.send_bytes function.

    """
    content = spu.create_zip_file(
        state, data_store, csv_filename, module_name
    )

    def format_zip_size(size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} B"
        if size_bytes < 1024**2:
            return f"{size_bytes / 1024:.1f} kB"
        return f"{size_bytes / (1024**2):.1f} MB"

    zip_size = format_zip_size(sys.getsizeof(content))

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == f"{module_name}_download_zip_button":
        download_zip_file = dcc.send_bytes(
            content, f"{zip_filename.split('.')[0]}.zip"
        )
        return download_zip_file, f"{zip_size} downloaded", no_update

    return no_update, no_update, f"{zip_size} to download"


@callback(
    Output("data_table", "columns"),
    Output("data_table", "data"),
    Output("data_table", "style_cell"),
    Output("data_store", "data"),
    Output("data_table", "style_table"),
    Input(f"{module_name}_channels_button", "children"),
    Input(f"{module_name}_frames_button", "children"),
    Input(f"{module_name}_records_button", "children"),
    Input(f"{module_name}_sample_interval_button", "children"),
)
def update_data_table(
    current_count: str,
    frames_count: str,
    records_count: str,
    sample_interval: str,
) -> Tuple[List[Dict], List[Dict], Dict, Dict, Dict]:
    """Update the DataTable based on the input parameters.

    This function creates a new DataFrame with channel data, generates column
    definitions, calculates cell styles, prepares data for storage, and
    determines if horizontal scrolling should be enabled.

    Args:
        current_count (str): The current number of channels as a string.
        frames_count (str): The number of frames as a string.
        records_count (str): The number of records as a string.
        sample_interval (str): The sample interval as a string.

    Returns:
        tuple: Contains five elements:
            - List[Dict]: Column definitions for the DataTable.
            - List[Dict]: Data records for the DataTable.
            - Dict: Style definitions for table cells.
            - Dict: Data to be stored in the dataframe store.
            - Dict:
                Style definitions for the table, including overflow settings.

    """
    current = int(current_count)
    params = [
        "Waveform Type",
        "Horizontal Units",
        "Sample Interval",
        "Record Length",
        "Vertical Units",
        "FastFrame Count",
    ]
    values = [
        "ANALOG",
        "s",
        sample_interval,
        records_count,
        "V",
        frames_count,
    ]

    channel_data = {}
    for ch_index in range(1, current + 1):
        channel_data[f"ch{ch_index}_par"] = params
        channel_data[f"ch{ch_index}_val"] = values

    columns = []
    for ch_index in range(1, current + 1):
        columns.extend([
            {"name": ["Channel"], "id": f"ch{ch_index}_par"},
            {"name": [f"CH{ch_index}"], "id": f"ch{ch_index}_val"},
        ])

    data_frame = pd.DataFrame(data=channel_data)

    column_width = f"{100 / len(data_frame.columns)}%"

    style_cell = {
        "width": column_width,
        "minWidth": column_width,
        "maxWidth": column_width,
        "textAlign": "left",
        "whiteSpace": "normal",
        "overflow": "hidden",
        "textOverflow": "ellipsis",
    }

    data_store = {"channel_data": channel_data, "columns": columns}

    style_table = {"overflowX": "auto"} if len(columns) > 4 else {}

    return (
        columns,
        data_frame.to_dict("records"),
        style_cell,
        data_store,
        style_table,
    )


dcu.callback_labeled_counter_trio(f"{module_name}_csv_files")
dcu.callback_labeled_counter_trio(f"{module_name}_channels")
dcu.callback_labeled_counter_trio(f"{module_name}_frames")
dcu.callback_labeled_counter_quintet(f"{module_name}_records", resolution=1)
dcu.callback_labeled_counter_quintet(
    f"{module_name}_sample_interval", resolution=0.1, decimal_places=6
)


@callback(
    Output("data_table", "style_data"),
    Output("data_table", "style_header"),
    Output("data_table", "style_data_conditional"),
    Input("theme_switch_value_store", "data"),
)
def update_table_style_and_visibility(
    switch: bool,
) -> Tuple[Dict, Dict, List[Dict]]:
    """Update the DataTable styles based on the theme switch value.

    This function changes the appearance of the DataTable,
    including data cells, header, and alternating row colors,
    depending on the selected theme.

    Args:
        switch (bool):
            The state of the theme switch.
            True for light theme, False for dark theme.

    Returns:
        Tuple[Dict, Dict, List[Dict]]:
            Styles for data cells, header cells,
            and conditional styles for alternating rows.

    """
    return (
        {
            "backgroundColor": "white" if switch else "#666666",
            "color": "black" if switch else "white",
            "fontWeight": "bold",
        },
        {
            "backgroundColor": "#DDDDDD" if switch else "#111111",
            "color": "black" if switch else "white",
            "fontWeight": "bold",
        },
        [{"if": {"row_index": "odd"}, "backgroundColor": "#DDDDDD"}]
        if switch
        else [{"if": {"row_index": "odd"}, "backgroundColor": "#555555"}],
    )
