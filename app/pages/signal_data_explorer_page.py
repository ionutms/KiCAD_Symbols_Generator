"""Signal Data Explorer Page for Signal data visualization and analysis.

This module provides a Dash-based web application page for exploring and
visualizing signal data from CSV and ZIP files containing CSV data.

Key Features:
- File upload support for CSV and ZIP files
- GitHub file selection for remote repositories
- Interactive selection of files, frames, records, and data channels
- Dynamic data visualizations
- Light and dark mode support
"""

from typing import Any, Dict, List, Tuple

import dash_bootstrap_components as dbc
import pages.utils.dash_component_utils as dcu
import pages.utils.signal_processing_utils as spu
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

# ============================================================================
# MODULE CONFIGURATION
# ============================================================================

link_name = __name__.rsplit(".", maxsplit=1)[-1].replace("_page", "").title()
module_name = __name__.rsplit(".", maxsplit=1)[-1]

register_page(
    __name__,
    name=link_name,
    path="/signal_data_explorer",
    order=2,
    exclude_from_nav=True,
)

# ============================================================================
# PAGE CONTENT CONSTANTS
# ============================================================================

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

FEATURES = [
    "Support for ZIP files containing multiple CSV data files",
    "Interactive selection of files, frames, records, and channels",
    "Multi-axis plotting capabilities for comparing different data channels",
    "Dynamic updating of data visualization based on user selections",
    "Responsive layout adapting to various screen sizes",
    "Integrated signal processing utilities for advanced data analysis",
    "Support for oscilloscope segmented memory data",
    "Customizable Y-axis placement for optimal data comparison",
    "Theme switching between light and dark modes",
    "GitHub file selection feature for accessing remote signal data",
]

USAGE_STEPS = [
    "Upload a ZIP file containing CSV data using the drag-and-drop area",
    "Alternatively, select a file from a GitHub repository",
    "Use range sliders to select specific files within the archive",
    "Adjust the frames slider to navigate between different segments",
    "Use the records slider to focus on specific portions within each frame",
    "Select data channels to visualize using the data sets slider",
    "Customize Y-axis placement for each channel",
    "Click 'View selected data' to generate the visualization",
    "Interact with the multi-axis plot to explore relationships",
    "Use zoom and pan tools to investigate areas of interest",
    "Toggle between light and dark themes",
]

# ============================================================================
# UI COMPONENTS
# ============================================================================


def create_file_upload_component() -> dcc.Upload:
    """Create the file upload component."""
    upload_style = {
        "height": "76px",
        "borderWidth": "1px",
        "borderStyle": "dashed",
        "borderColor": "#808080",
        "borderRadius": "10px",
        "textAlign": "center",
    }

    upload_text = html.Div(
        ["Drag and Drop or ", html.A("Select a zip with csv file(s)")],
        className="text-center",
    )

    upload_col = dbc.Col(
        upload_text,
        className="d-flex align-items-center justify-content-center",
        style={"height": "100%"},
    )

    return dcc.Upload(
        id=f"{module_name}_upload",
        children=[dbc.Row([upload_col], className="h-100")],
        style=upload_style,
        multiple=False,
    )


def create_selection_controls() -> List[dbc.Row]:
    """Create all selection control rows."""
    file_selection = dbc.Row(
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

    frames_selection = dbc.Row(
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

    records_selection = dbc.Row(
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

    data_sets_selection = dbc.Row(
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

    return [
        file_selection,
        frames_selection,
        records_selection,
        data_sets_selection,
    ]


def create_control_buttons() -> dbc.Row:
    """Create the control buttons row (legend switch and view button)."""
    legend_card_style = {
        "border": "1px dashed",
        "border-radius": "10px",
        "display": "none",
        "padding": "1px",
        "background-color": "transparent",
    }

    view_button_style = {
        "border": "none",
        "background-color": "transparent",
        "padding-top": "10px",
        "padding-bottom": "10px",
    }

    legend_card = dbc.Card(
        id="group_legend_card",
        children=[
            dbc.Label("Group Legend"),
            dbc.Switch(id="legend_group_switch", value=False),
        ],
        body=True,
        style=legend_card_style,
    )

    view_button = dbc.Card(
        [dbc.Button("View", id="view_data_button")],
        body=True,
        style=view_button_style,
    )

    return dbc.Row([
        dbc.Col([dbc.Row(id="radioitems_row")], xs=12, md=9),
        dbc.Col(
            [
                dbc.Row([
                    dbc.Col([legend_card, html.Br()], xs=12, md=6),
                    dbc.Col([view_button], xs=12, md=6),
                ])
            ],
            xs=12,
            md=3,
        ),
    ])


# ============================================================================
# PAGE LAYOUT
# ============================================================================


def create_layout() -> dbc.Container:
    """Create the main page layout."""
    # Header section
    header = [
        dbc.Row([dbc.Col([dcc.Link("Go back Home", href="/")])]),
        dbc.Row([dbc.Col([html.H3(link_name.replace("_", " "))])]),
        dbc.Row([dcu.app_description(TITLE, ABOUT, FEATURES, USAGE_STEPS)]),
    ]

    # File upload section
    file_upload = dbc.Row(
        [dbc.Col([create_file_upload_component(), html.Hr()])],
        className="g-3 align-items-center justify-content-center",
    )

    # Selection controls section
    selection_controls = create_selection_controls()
    control_buttons = create_control_buttons()

    selection_section = dbc.Row(
        [
            dbc.Col([
                dcc.Loading(
                    selection_controls + [control_buttons],
                    delay_show=2000,
                ),
                html.Hr(),
            ])
        ],
        id="selection_row",
        style={"display": "none"},
    )

    # Graph section
    graph_section = dbc.Row([
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

    # Combine all sections
    main_content = header + [
        dcc.Store(id=f"{module_name}_contents_store"),
        file_upload,
        selection_section,
        graph_section,
    ]

    return dbc.Container([html.Div(main_content)], fluid=True)


layout = create_layout()

# ============================================================================
# CALLBACKS - FILE HANDLING
# ============================================================================


@callback(
    Output(f"{module_name}_contents_store", "data"),
    Input(f"{module_name}_upload", "contents"),
    State(f"{module_name}_upload", "filename"),
    prevent_initial_call=True,
)
def store_uploaded_file(contents: str, filename: str) -> Dict[str, str]:
    """Store uploaded ZIP file contents.

    Args:
        contents: Base64 encoded file contents
        filename: Name of the uploaded file

    Returns:
        Dictionary with filename and content, or no_update if not
        a ZIP file

    """
    if filename.endswith(".zip"):
        return {"filename": filename, "content": contents}
    return no_update


@callback(
    Output("selection_row", "style"),
    Output("graph_column", "style", allow_duplicate=True),
    Input(f"{module_name}_upload", "filename"),
    prevent_initial_call=True,
)
def toggle_file_selection_visibility(
    upload_filename: str,
) -> Tuple[Dict[str, str], Dict[str, str]]:
    """Show/hide selection controls based on uploaded file type.

    Args:
        upload_filename: Name of the uploaded file

    Returns:
        Tuple of style dictionaries for selection row and graph
        column

    """
    if ctx.triggered_id == f"{module_name}_upload":
        if upload_filename.lower().endswith(".zip"):
            return {"display": ""}, {"display": "none"}

    return {"display": "none"}, {"display": "none"}


# ============================================================================
# CALLBACKS - DATA FILTERING
# ============================================================================


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
def update_filtering_store(
    files: List[int],
    frames: List[int],
    records_range: List[int],
    value: List[int],
    records_max: int,
    marks: Dict[str, str],
    select_contents: Dict[str, str],
) -> Dict[str, Any]:
    """Update filtering parameters based on slider selections.

    Args:
        files: Selected file indices
        frames: Selected frame indices
        records_range: Range of selected records
        value: Selected data set indices
        records_max: Maximum number of records
        marks: Data sets slider marks
        select_contents: Uploaded file contents and metadata

    Returns:
        Updated filtering dictionary or no_update

    """
    try:
        filename = select_contents["filename"]
        contents = select_contents["content"]

        if not filename.lower().endswith(".zip"):
            return no_update

        units_info = spu.extract_info_from_zip(
            contents, ["Horizontal Units", "Vertical Units"]
        )
        horizontal_units, vertical_units = units_info.values()

        filtering = {
            "files_to_keep": [file - 1 for file in files],
            "frames_to_keep": [frame - 1 for frame in frames],
            "x_axis_data": marks[f"{value[0]}"],
            "y_axis_data": [marks[f"{position}"] for position in value[1:]],
            "records_slice": records_range,
            "records_max": records_max,
            "Horizontal Units": horizontal_units,
            "Vertical Units": vertical_units,
        }
        return filtering

    except (TypeError, KeyError):
        return no_update


# ============================================================================
# CALLBACKS - VISUALIZATION
# ============================================================================


@callback(
    Output(f"{module_name}_data_graph", "figure"),
    Output("graph_column", "style"),
    Input("view_data_button", "n_clicks"),
    Input("theme_switch_value_store", "data"),
    State(f"{module_name}_contents_store", "data"),
    State("filtering_store", "data"),
    prevent_initial_call=True,
)
def update_graph(
    _view_data_button: int,
    theme_switch: bool,
    select_contents: Dict[str, str],
    filtering: Dict[str, Any],
) -> Tuple[Any, Dict[str, str]]:
    """Update graph with filtered data from uploaded file.

    Args:
        _view_data_button: Button click count (unused,
            triggers callback)
        theme_switch: Current theme state (light/dark)
        select_contents: Uploaded file contents and metadata
        filtering: Current filtering parameters

    Returns:
        Tuple of (figure object, style dictionary)

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

    except (TypeError, KeyError):
        return no_update, {"display": "none"}

    return no_update, {"display": "none"}


@callback(
    Output("group_legend_card", "style"),
    Input(f"{module_name}_data_sets_range_slider", "value"),
    State("group_legend_card", "style"),
    prevent_initial_call=True,
)
def toggle_legend_card(
    slider_value: List[int], style_state: Dict[str, str]
) -> Dict[str, str]:
    """Show/hide legend grouping card based on selected data sets.

    Args:
        slider_value: Current range slider value
        style_state: Current card style

    Returns:
        Updated style dictionary

    """
    style_state["display"] = "" if len(slider_value) > 2 else "none"
    return style_state


# ============================================================================
# CALLBACK REGISTRATION - STORE UPDATES
# ============================================================================

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

# ============================================================================
# CALLBACK REGISTRATION - UI CONTROLS
# ============================================================================

# Radio items for data sets
dcu.callbacks_radioitems(f"{module_name}_data_sets", "radioitems_row")

# Files controls
dcu.callback_update_range_slider_max_and_label(
    f"{module_name}_files", f"{module_name}_contents_store"
)
dcu.callback_labeled_counter_trio(f"{module_name}_files")
dcu.callback_update_range_slider_value(f"{module_name}_files")

# Frames controls
dcu.callback_update_range_slider_max_and_label(
    f"{module_name}_frames", f"{module_name}_contents_store"
)
dcu.callback_labeled_counter_trio(f"{module_name}_frames")
dcu.callback_update_range_slider_value(f"{module_name}_frames")

# Records controls
dcu.callback_update_range_slider_max_and_label(
    f"{module_name}_records", f"{module_name}_contents_store"
)
dcu.callback_labeled_counter_quintet(f"{module_name}_records", resolution=1)
dcu.callback_update_range_slider_pushable_and_value(f"{module_name}_records")

# Data sets controls
dcu.callback_update_range_slider_max_and_label(
    f"{module_name}_data_sets", f"{module_name}_contents_store", reset_value=2
)
dcu.callback_labeled_counter_trio(f"{module_name}_data_sets")
dcu.callback_update_range_slider_value(f"{module_name}_data_sets", 0)
