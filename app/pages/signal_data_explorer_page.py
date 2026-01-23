"""Signal Data Explorer Page for Signal data visualization and analysis.

This module provides a Dash-based web application page for exploring and
visualizing signal data from CSV and ZIP files containing CSV data. It also
supports selecting files directly from a GitHub repository, providing a
convenient way to access and analyze signal data stored in remote locations.
The module offers an interactive interface for file upload, data selection,
and dynamic plotting.

Key Features:
- File upload support for CSV and ZIP files containing CSV data
- GitHub file selection feature for accessing signal data from remote
  repositories
- Interactive selection of files, frames (segments), records,
    and data channels
- Dynamic updating of data visualizations based on user selections
- Responsive layout using Dash Bootstrap Components
- Integrated signal processing utilities for data analysis
- Themeable interface with light and dark mode support

Components:
- File upload area for CSV and ZIP files
- GitHub file selection dropdown
- Range sliders for selecting specific files, frames, records, and channels
- Interactive graph for data visualization
- Theme switch for toggling between light and dark modes

The page is designed to be part of a larger Dash application and is registered
as a page using the Dash pages plugin. It leverages various utility modules
for styling, component creation, and signal processing.

Usage:
1. Upload a CSV or ZIP file containing CSV data or select a file directly from
   a GitHub repository using the file selection dropdown.
2. Use the range sliders to select specific portions of the data.
3. Click "View selected data" to update the visualization.
4. Interact with the generated plot for detailed data exploration.
5. Toggle between light and dark themes as needed.

Dependencies:
- dash and its components (dcc, html, callback, etc.)
- dash_bootstrap_components
- Custom utility modules (style_utils, dash_component_utils,
  signal_processing_utils)

Note: This module is part of a larger application and relies on custom utility
functions and components defined in separate modules.
"""

import base64
from typing import Any, Dict, List, Tuple

import dash_bootstrap_components as dbc
import pages.utils.dash_component_utils as dcu
import pages.utils.signal_processing_utils as spu
import pages.utils.style_utils as styles
import requests
from dash import (
    Input,
    Output,
    State,
    callback,
    ctx,
    dcc,
    html,
    no_update,
    register_page,
)
from dash.exceptions import PreventUpdate

link_name = __name__.rsplit(".", maxsplit=1)[-1].replace("_page", "").title()
module_name = __name__.rsplit(".", maxsplit=1)[-1]

register_page(
    __name__,
    name=link_name,
    path="/signal_data_explorer",
    order=2,
    exclude_from_nav=True,
)


TITLE = "Signal Data Explorer"
ABOUT = (
    "The Signal Data Explorer is an advanced interactive web application "
    "designed for visualizing and analyzing complex signal data from ZIP "
    "files containing CSV data.",
    "It offers a powerful and user-friendly interface for exploring "
    "multi-channel, multi-segment signal data sets, allowing users to "
    "select and analyze specific portions of the data with precision.",
    "This tool is particularly effective for working with oscilloscope "
    "segmented memory data, enabling efficient analysis of long-duration "
    "captures with intermittent signals of interest across multiple "
    "channels.",
    "The application also supports selecting files directly from a GitHub "
    "repository, providing a convenient way to access and analyze signal "
    "data stored in remote locations.",
)

features = [
    "Support for ZIP files containing multiple CSV data files",
    "Interactive selection of files, frames (segments), records, "
    "and channels",
    "Multi-axis plotting capabilities for comparing different data channels",
    "Dynamic updating of data visualization based on user selections",
    "Responsive layout adapting to various screen sizes",
    "Integrated signal processing utilities for advanced data analysis",
    "Support for oscilloscope segmented memory data, allowing analysis "
    "of multiple waveform segments captured over extended time periods",
    "Customizable Y-axis placement for optimal data comparison",
    "Theme switching between light and dark modes for comfortable viewing",
    "GitHub file selection feature for accessing signal data from remote "
    "repositories",
]

usage_steps = [
    "Upload a ZIP file containing CSV signal data using "
    "the drag-and-drop area or file selector.",
    "Alternatively, select a file directly from a GitHub repository using "
    "the file selection dropdown.",
    "Use the range sliders to select specific files within the ZIP archive "
    "or GitHub repository.",
    "Adjust the frames slider to navigate between "
    "different segments of the data.",
    "Use the records slider to focus on specific portions within each frame.",
    "Select the data channels you wish to "
    "visualize using the data sets slider.",
    "Customize the Y-axis placement for each channel using the radio "
    "buttons.",
    "Click the 'View selected data' button to generate the visualization.",
    "Interact with the multi-axis plot to explore "
    "relationships between channels.",
    "Use the zoom and pan tools to investigate areas of interest in detail.",
    "Toggle between light and dark themes for optimal viewing.",
]

MAIN_DIV_CHILDREN = [
    dbc.Row([dbc.Col([dcc.Link("Go back Home", href="/")])]),
    dbc.Row([
        dbc.Col([
            html.H3(
                f"{link_name.replace('_', ' ')}", style=styles.heading_3_style
            )
        ])
    ]),
    dbc.Row([dcu.app_description(TITLE, ABOUT, features, usage_steps)]),
]


layout = dbc.Container(
    [html.Div(MAIN_DIV_CHILDREN, style=styles.GLOBAL_STYLE)], fluid=True
)


select_card = dbc.Card(
    [
        dbc.Row(
            [
                dcc.Store(id="repo_info_store", data={}),
                dcc.Store(id=f"{module_name}_contents_store"),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dcu.make_input_groups_column(
                                    label="github repository api",
                                    input_id="repo_api",
                                    value="https://api.github.com/repos",
                                    md=6,
                                    theme_trigger_id="theme_switch_value_store",
                                ),
                                dcu.make_input_groups_column(
                                    label="repository owner",
                                    input_id="repo_owner",
                                    value="ionutms",
                                    md=6,
                                    theme_trigger_id="theme_switch_value_store",
                                ),
                            ],
                            className=(
                                "g-0 align-items-center "
                                "justify-content-center"
                            ),
                        )
                    ],
                    xs=12,
                    md=5,
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dcu.make_input_groups_column(
                                    label="repository name",
                                    input_id="repo_name",
                                    value="demo_test_files",
                                    md=4,
                                    theme_trigger_id="theme_switch_value_store",
                                ),
                                dcu.make_input_groups_column(
                                    label="repository path",
                                    input_id="repo_path",
                                    value="contents/demo_test_files",
                                    md=4,
                                    theme_trigger_id="theme_switch_value_store",
                                ),
                                dbc.Col(
                                    [
                                        dbc.Button(
                                            "Search Files",
                                            id="search_files_button",
                                            className="w-100",
                                            color="secondary",
                                        ),
                                        dbc.Select(
                                            id=f"{module_name}_file_select",
                                            placeholder="No files ...",
                                            disabled=True,
                                            className="w-100",
                                        ),
                                    ],
                                    xs=12,
                                    md=4,
                                    className="mb-1 d-flex flex-column",
                                ),
                            ],
                            className=(
                                "g-0 align-items-center "
                                "justify-content-center"
                            ),
                        )
                    ],
                    xs=12,
                    md=7,
                ),
            ],
            className="g-0 align-items-center justify-content-center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            id="status_div",
                            className=styles.CENTER_CONTENT_CLASS,
                        )
                    ],
                    width=12,
                )
            ],
            className="g-0 align-items-center justify-content-center",
        ),
    ],
    body=True,
    style={
        "background-color": "transparent",
        "borderWidth": "1px",
        "padding": "2px",
        "borderColor": "#808080",
        "borderStyle": "dashed",
        "borderRadius": "10px",
    },
)


file_upload_component = dcc.Upload(
    id=f"{module_name}_upload",
    children=[
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            "Drag and Drop or ",
                            html.A("Select a zip with csv file(s)"),
                        ],
                        className="text-center",
                    ),
                    className=(
                        "d-flex align-items-center justify-content-center"
                    ),
                    style={"height": "100%"},
                )
            ],
            className="h-100",
        )
    ],
    style={
        "height": "76px",
        "borderWidth": "1px",
        "borderStyle": "dashed",
        "borderColor": "#808080",
        "borderRadius": "10px",
        "textAlign": "center",
    },
    multiple=False,
)


file_select_row = dbc.Row(
    [dbc.Col([select_card, html.Hr()])],
    className="g-3 align-items-center justify-content-center",
)

file_upload_row = dbc.Row(
    [dbc.Col([file_upload_component, html.Hr()])],
    className="g-3 align-items-center justify-content-center",
)

file_selection_row = dbc.Row(
    id=f"{module_name}_files_row",
    children=[
        dcu.labeled_counter_trio(
            f"{module_name}_files",
            "0 files detected",
            limits={"min_count": 1, "max_count": 2},
        ),
        dcu.labeled_range_slider(
            f"{module_name}_files", "Select which files to explore", [1]
        ),
    ],
)

frames_selection_row = dbc.Row(
    id=f"{module_name}_frames_row",
    children=[
        dcu.labeled_counter_trio(
            f"{module_name}_frames",
            "0 frames detected",
            limits={"min_count": 1, "max_count": 2},
        ),
        dcu.labeled_range_slider(
            f"{module_name}_frames", "Select which frames to explore", [1]
        ),
    ],
)

records_selection_row = dbc.Row(
    id=f"{module_name}_records_row",
    children=[
        dcu.labeled_counter_quintet(
            id_section=f"{module_name}_records",
            label="0 records per-frame detected",
            default_count=1,
            limits={"min_count": 1, "max_count": 2},
        ),
        dcu.labeled_range_slider(
            f"{module_name}_records",
            "Select a minimum number of records per-frame to explore",
            [0, 1],
            0,
        ),
    ],
)

data_sets_selection_row = dbc.Row(
    id=f"{module_name}_data_sets_row",
    children=[
        dcu.labeled_counter_trio(
            f"{module_name}_data_sets",
            "0 data sets detected",
            limits={"min_count": 2, "max_count": 3},
            default_count=2,
        ),
        dcu.labeled_range_slider(
            f"{module_name}_data_sets",
            "Select which data sets to explore",
            [1],
        ),
    ],
)

radioitems_row = dbc.Row([
    dbc.Col([dbc.Row(id="radioitems_row")], xs=12, md=9),
    dbc.Col(
        [
            dbc.Row([
                dbc.Col(
                    [
                        dbc.Card(
                            id="group_legend_card",
                            children=[
                                dbc.Label(
                                    "Group Legend",
                                    className=styles.CENTER_CLASS_NAME,
                                ),
                                dbc.Switch(
                                    id="legend_group_switch",
                                    value=False,
                                    className=styles.CENTER_CLASS_NAME,
                                ),
                            ],
                            body=True,
                            style={
                                "border": "1px dashed",
                                "border-radius": "10px",
                                "display": "none",
                                "padding": "1px",
                                "background-color": "transparent",
                            },
                        ),
                        html.Br(),
                    ],
                    xs=12,
                    md=6,
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.Button(
                                    "View",
                                    id="view_data_button",
                                    className=styles.CENTER_CLASS_NAME,
                                )
                            ],
                            body=True,
                            style={
                                "border": "none",
                                "background-color": "transparent",
                                "padding-top": "10px",
                                "padding-bottom": "10px",
                            },
                        )
                    ],
                    xs=12,
                    md=6,
                ),
            ])
        ],
        xs=12,
        md=3,
    ),
])


selection_row = dbc.Row(
    [
        dbc.Col([
            dcc.Loading(
                [
                    file_selection_row,
                    frames_selection_row,
                    records_selection_row,
                    data_sets_selection_row,
                    radioitems_row,
                ],
                delay_show=2000,
            ),
            html.Hr(),
        ])
    ],
    id="selection_row",
    style={"display": "none"},
)

graph_row = dbc.Row([
    dbc.Col(
        [
            dcc.Store("filtering_store", data={}),
            dcc.Loading([dcc.Graph(id=f"{module_name}_data_graph")]),
            html.Hr(),
        ],
        id="graph_column",
        style={"display": "none"},
    )
])

output = dbc.Row([dbc.Col([html.Div(id="output-data-upload")])])


MAIN_DIV_CHILDREN.extend([
    output,
    file_select_row,
    file_upload_row,
    selection_row,
    graph_row,
])


@callback(
    Output("repo_info_store", "data"),
    Input("search_files_button", "n_clicks"),
    Input("repo_api", "value"),
    Input("repo_owner", "value"),
    Input("repo_name", "value"),
    Input("repo_path", "value"),
)
def store_repo_info(
    n_clicks: int, api: str, owner: str, name: str, path: str
) -> Dict[str, str]:
    """Store repository information in the repo_info_store.

    This callback is triggered when the "Search Files" button is clicked.
    It collects the current values of the repository API, owner, name, and
    path inputs and stores them in a dictionary.

    Args:
        n_clicks (int):
            Number of times the "Search Files" button has been clicked.
        api (str): The base URL of the GitHub API.
        owner (str): The owner of the GitHub repository.
        name (str): The name of the GitHub repository.
        path (str): The path within the repository to search for files.

    Returns:
        Dict[str, str]: A dictionary containing the repository information.

    Raises:
        PreventUpdate: If the function is called without the button being
            clicked (on initial load).

    """
    if n_clicks is not None and n_clicks > 1:
        raise PreventUpdate
    return {"api": api, "owner": owner, "name": name, "path": path}


@callback(
    Output(f"{module_name}_file_select", "options"),
    Output(f"{module_name}_file_select", "placeholder"),
    Output(f"{module_name}_file_select", "disabled"),
    Output("status_div", "children"),
    Input("search_files_button", "n_clicks"),
    State("repo_info_store", "data"),
    prevent_initial_call=True,
)
def update_github_files_dropdown(
    n_clicks: int, repo_info: Dict[str, str]
) -> Tuple[List[Dict[str, str]], str, bool, str]:
    """Update the file selection dropdown with files from the repository.

    This callback is triggered when the "Search Files" button is clicked. It
    uses the repository information stored in repo_info_store to fetch the
    list of files from the specified GitHub repository path.

    Args:
        n_clicks (int):
            Number of times the "Search Files" button has been clicked.
        repo_info (Dict[str, str]):
            A dictionary containing the repository information.

    Returns:
        Tuple[List[Dict[str, str]], str, bool, str]: A tuple containing:
            - A list of dictionaries, each representing a file option for
              the dropdown.
            - A string for the dropdown placeholder text.
            - A boolean indicating whether the dropdown should be disabled.
            - A string containing a status message.

    """
    if n_clicks is None or not repo_info:
        raise PreventUpdate

    repo_api = repo_info.get("api", "")
    repo_owner = repo_info.get("owner", "")
    repo_name = repo_info.get("name", "")
    repo_path = repo_info.get("path", "")

    url = f"{repo_api}/{repo_owner}/{repo_name}/{repo_path}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        file_names_list = [
            item["name"] for item in response.json() if item["type"] == "file"
        ]
        options = [{"label": file, "value": file} for file in file_names_list]
        return (
            options,
            "Select a file ...",
            False,
            f"Found {len(file_names_list)} files",
        )
    except requests.exceptions.RequestException as error_message:
        status_message = f"Error fetching GitHub files: {error_message}"
        return [], "No files available", True, status_message


@callback(
    Output(f"{module_name}_file_select", "style"),
    Input("theme_switch_value_store", "data"),
)
def update_theme_styles(theme_switch):
    """Update the styles of multiple elements based on the theme switch.

    This callback function changes the appearance of the file select dropdown,
    search button, and status div when the theme is toggled between light and
    dark modes.

    Args:
        theme_switch (bool): True for light theme, False for dark theme.

    Returns:
        tuple:
            A tuple containing style dictionaries for file_select,
            search_files_button, and status_div.

    """
    text_color = "#555" if theme_switch else "#eee"
    bg_color = "#eee" if theme_switch else "#555"

    file_select_style = {
        "background-color": bg_color,
        "color": text_color,
    }
    return file_select_style


@callback(
    Output(f"{module_name}_contents_store", "data"),
    Input(f"{module_name}_upload", "contents"),
    State(f"{module_name}_upload", "filename"),
    prevent_initial_call=True,
)
def store_uploaded_file(contents: str, filename: str) -> Dict[str, str]:
    """Store the contents of an uploaded file if it's a zip file.

    This callback function is triggered when a file is uploaded. It checks if
    the file is a zip file and if so, stores its contents and filename in the
    contents store.

    Args:
        contents (str):
            The contents of the uploaded file, encoded as a base64 string.
        filename (str): The name of the uploaded file.

    Returns:
        Union[Dict[str, str], dash._no_update.NoUpdate]:
            - If a zip file is uploaded, returns a dictionary with 'filename'
              and 'content' keys.
            - If the file is not a zip, returns dash.no_update to prevent any
              changes to the store.

    Behavior:
        - The function checks if the filename ends with '.zip'.
        - If it's a zip file, it stores the filename and contents in a
          dictionary.
        - For any other case (non-zip file), it returns no_update to prevent
          changes to the store.

    Note:
        This function assumes that the uploaded file contents are provided as
        a base64 encoded string, which is the default behavior for Dash
        upload components. It also assumes that the callback will always
        receive non-None values for contents and filename.

    """
    if filename.endswith(".zip"):
        return {"filename": filename, "content": contents}
    return no_update


@callback(
    Output(f"{module_name}_contents_store", "data", allow_duplicate=True),
    Output("status_div", "children", allow_duplicate=True),
    Input(f"{module_name}_file_select", "value"),
    State("repo_info_store", "data"),
    prevent_initial_call=True,
)
def store_selected_file(
    selected_file: str, repo_info: Dict[str, str]
) -> Tuple[Dict[str, Any], str]:
    """Store the content of the selected file and update the status.

    This callback is triggered when a file is selected from the dropdown.
    It fetches the file from GitHub, stores its content, and returns a
    status message.

    Args:
        selected_file (str): The name of the selected file.
        repo_info (Dict[str, str]): Repository information dictionary.

    Returns:
        Tuple[Dict[str, Any], str]: File content, metadata, and status.

    """
    if not selected_file or not repo_info:
        raise PreventUpdate

    github_repository_api = repo_info.get("api", "")
    repo_owner = repo_info.get("owner", "")
    repo_name = repo_info.get("name", "")
    repo_path = repo_info.get("path", "")

    url = (
        f"{github_repository_api}/{repo_owner}/{repo_name}/"
        f"{repo_path}/{selected_file}"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        file_data = response.json()

        download_url = file_data["download_url"]
        zip_response = requests.get(download_url, timeout=10)
        zip_response.raise_for_status()

        file_content = base64.b64encode(zip_response.content).decode("utf-8")

        return (
            {"filename": selected_file, "content": file_content},
            f"File '{selected_file}' has been stored.",
        )
    except requests.RequestException as error:
        return None, f"Error fetching the file: {str(error)}"


dcu.callback_update_store_at_upload(
    f"{module_name}_files",
    f"{module_name}_contents_store",
    "filtering_store",
    spu.count_csv_files_from_zip,
)

dcu.callback_update_store_at_upload(
    f"{module_name}_frames",
    f"{module_name}_contents_store",
    "filtering_store",
    dcu.extract_info_from_zip_as_int,
    "FastFrame Count",
)

dcu.callback_update_store_at_upload(
    f"{module_name}_records",
    f"{module_name}_contents_store",
    "filtering_store",
    dcu.extract_info_from_zip_as_int,
    "Record Length",
)

dcu.callback_update_store_at_upload(
    f"{module_name}_data_sets",
    f"{module_name}_contents_store",
    "filtering_store",
    spu.extract_data_frame_from_zip_contents,
)


dcu.callbacks_radioitems(f"{module_name}_data_sets", "radioitems_row")


@callback(
    Output("group_legend_card", "style"),
    Input(f"{module_name}_data_sets_range_slider", "value"),
    State("group_legend_card", "style"),
    prevent_initial_call=True,
)
def set_group_legend_card_style(
    slider_value: List[int], style_state: Dict[str, str]
) -> Dict[str, str]:
    """Set the display style of the group legend card based on slider value.

    This callback function determines whether to show or hide the group legend
    card depending on the number of selected data sets in the range slider.

    Args:
        slider_value (List[int]):
            The current value of the data sets range slider.
            Expected to be a list of integers representing the selected range.
        style_state (Dict[str, str]):
            The current style dictionary of the group legend card.
            This state is used to preserve other style properties while
            updating the 'display' property.

    Returns:
        Dict[str, str]: An updated style dictionary for the group legend card.

    Behavior:
        - If more than two data sets are selected (len(slider_value) > 2),
          the group legend card is displayed by setting style['display'] to an
          empty string.
        - If two or fewer data sets are selected, the group legend card is
          hidden by setting style['display'] to 'none'.
        - The function prevents initial call to avoid unnecessary executions
          on page load.

    Note:
        This function assumes that the slider_value is a list of at least two
        integers representing the start and end of the selected range.

    """
    style_state["display"] = "" if len(slider_value) > 2 else "none"
    return style_state


@callback(
    Output("filtering_store", "data"),
    Input(f"{module_name}_files_range_slider", "value"),
    Input(f"{module_name}_frames_range_slider", "value"),
    Input(f"{module_name}_records_range_slider", "value"),
    Input(f"{module_name}_data_sets_range_slider", "value"),
    Input(f"{module_name}_records_range_slider", "max"),
    State(f"{module_name}_data_sets_range_slider", "marks"),
    Input(f"{module_name}_contents_store", "data"),
    prevent_initial_call=True,
)
def update_files_filtering_store_with_slider_values(
    files: List[int],
    frames: List[int],
    records_range: List[int],
    value: List[int],
    records_max: int,
    marks: Dict[str, str],
    select_contents: str,
) -> Dict[str, Any]:
    """Update filtering store with slider values and file information.

    Args:
        files: List of selected file indices.
        frames: List of selected frame indices.
        records_range: Range of selected records.
        value: List of selected data set indices.
        records_max: Maximum number of records.
        marks: Dictionary of marks for data sets slider.
        select_contents: Contents of the uploaded file.
        filename: Name of the uploaded file.

    Returns:
        Updated filtering dictionary or no_update if file is not a ZIP.

    """
    try:
        filename = select_contents["filename"]
        contents = select_contents["content"]

        units_info = spu.extract_info_from_zip(
            contents, ["Horizontal Units", "Vertical Units"]
        )

        if filename.lower().endswith(".zip"):
            horizontal_units, vertical_units = units_info.values()
            filtering = {
                "files_to_keep": [file - 1 for file in files],
                "frames_to_keep": [frame - 1 for frame in frames],
                "x_axis_data": marks[f"{value[0]}"],
                "y_axis_data": [
                    marks[f"{position}"] for position in value[1:]
                ],
                "records_slice": records_range,
                "records_max": records_max,
                "Horizontal Units": horizontal_units,
                "Vertical Units": vertical_units,
            }
            return filtering
    except TypeError:
        return no_update

    return no_update


@callback(
    Output("selection_row", "style"),
    Output("graph_column", "style", allow_duplicate=True),
    Input(f"{module_name}_upload", "filename"),
    Input(f"{module_name}_file_select", "value"),
    prevent_initial_call=True,
)
def toggle_file_selection_visibility(
    upload_filename: str,
    select_filename: str,
) -> Dict[str, str]:
    """Toggle the visibility of file selection components.

    This function is a callback that responds to changes in the file upload or
    file selection components. It shows or hides the selection row and graph
    column depending on whether the file is a ZIP archive or not.

    Args:
        upload_filename (str): The name of the file uploaded by the user.
        select_filename (str):
            The name of the file selected from existing options.

    Returns:
        Dict[str, str]:
            A tuple of two dictionaries, each containing CSS display property.
            The first dictionary is for the selection row,
            the second for the graph column.

    Behavior:
        - If a ZIP file is uploaded or selected, the selection row is
          displayed and the graph column is hidden.
        - For any other file type, both the selection row and graph column
          are hidden.
        - The function prevents initial call to avoid unnecessary executions
          on page load.

    """
    if ctx.triggered_id == f"{module_name}_upload":
        if upload_filename.lower().endswith(".zip"):
            return {"display": ""}, {"display": "none"}

    if select_filename.lower().endswith(".zip"):
        return {"display": ""}, {"display": "none"}

    return {"display": "none"}, {"display": "none"}


@callback(
    Output(f"{module_name}_data_graph", "figure"),
    Output("graph_column", "style"),
    Input("view_data_button", "n_clicks"),
    Input("theme_switch_value_store", "data"),
    State(f"{module_name}_contents_store", "data"),
    State("filtering_store", "data"),
    prevent_initial_call=True,
)
def update_graph_with_uploaded_file(
    _view_data_button: int,
    theme_switch: bool,
    select_contents: str,
    filtering: Dict[str, Any],
) -> Tuple[Any, Dict[str, str]]:
    """Update the graph with the contents of the uploaded file.

    Args:
        _view_data_button: Number of clicks on the view data button (unused).
        theme_switch: Boolean indicating the theme switch state.
        select_contents: Contents of the uploaded file.
        filename: Name of the uploaded file.
        filtering: Dictionary containing filtering options.

    Returns:
        A tuple containing the updated figure and its style.

    Raises:
        PreventUpdate:
            If no file is uploaded or the file type is not supported.

    """
    try:
        filename = select_contents["filename"]
        contents = select_contents["content"]

        file_extension = filename.lower().split(".")[-1]

        if file_extension == "zip":
            figure = spu.plot_selected_zip_contents(
                contents, filename, filtering, theme_switch
            )
            return figure, {"display": ""}
    except TypeError:
        return no_update, {"display": "none"}

    return no_update, {"display": "none"}


dcu.callback_update_range_slider_max_and_label(
    f"{module_name}_files", f"{module_name}_contents_store"
)
dcu.callback_labeled_counter_trio(f"{module_name}_files")
dcu.callback_update_range_slider_value(f"{module_name}_files")

dcu.callback_update_range_slider_max_and_label(
    f"{module_name}_frames", f"{module_name}_contents_store"
)
dcu.callback_labeled_counter_trio(f"{module_name}_frames")
dcu.callback_update_range_slider_value(f"{module_name}_frames")

dcu.callback_update_range_slider_max_and_label(
    f"{module_name}_records", f"{module_name}_contents_store"
)
dcu.callback_labeled_counter_quintet(f"{module_name}_records", resolution=1)
dcu.callback_update_range_slider_pushable_and_value(f"{module_name}_records")

dcu.callback_update_range_slider_max_and_label(
    f"{module_name}_data_sets", f"{module_name}_contents_store", reset_value=2
)
dcu.callback_labeled_counter_trio(f"{module_name}_data_sets")
dcu.callback_update_range_slider_value(f"{module_name}_data_sets", 0)
