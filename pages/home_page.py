"""Home page module for the Dash application.

This module defines the layout and callback for the home page of the Dash app.
It displays a title and dynamically generates links to other pages in the app.
"""

from __future__ import annotations

from typing import Any

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html

import pages.utils.dash_component_utils as dcu
import pages.utils.style_utils as styles

link_name = __name__.rsplit(".", maxsplit=1)[-1].replace("_page", "").title()
module_name = __name__.rsplit(".", maxsplit=1)[-1]

dash.register_page(__name__, name=link_name, path="/")

TITLE = "Home Page"

ABOUT = (
    "The Home page serves as the main entry point and "
    "navigation hub for the Dash application.",
    "It provides a centralized location for users to access "
    "all available pages within the application, "
    "offering a simple and intuitive navigation experience.",
)

features = [
    "Dynamic generation of links to other pages in the application",
    "Clean and simple interface for easy navigation",
    "Responsive layout using Dash Bootstrap Components",
]

usage_steps = [
    "View the list of available pages displayed as clickable links.",
    "Click on any link to navigate to the corresponding page.",
    "Use the browser's back button or navigation controls "
    "to return to the Home page.",
]


clones_graph = dcc.Loading(
    [
        dcc.Graph(
            id=f"{module_name}_repo_clones_graph",
            config={"displaylogo": False},
        ),
    ],
    delay_show=100,
    delay_hide=100,
)

visitors_graph = dcc.Loading(
    [
        dcc.Graph(
            id=f"{module_name}_repo_visitors_graph",
            config={"displaylogo": False},
        ),
    ],
    delay_show=100,
    delay_hide=100,
)

links_display_div = html.Div(
    id="links_display",
    style={"display": "flex", "flex-direction": "column", "gap": "10px"},
)

minimal_adp1032_github_repo_anchor_tag = html.A(
    children="Minimal_ADP1032",
    href=("https://github.com/ionutms/Minimal_ADP1032"),
    target="_blank",
)

minimal_adp1032_interactive_bom_anchor_tag = html.A(
    "Interactive BOM",
    href=(
        "https://htmlpreview.github.io/?https://github.com/ionutms/"
        "Minimal_ADP1032/blob/main/minimal_adp1032/bom/ibom.html"
    ),
    target="_blank",
)

minimal_adp1032_schematics_anchor_tag = html.A(
    children="Schematics",
    href=(
        "https://mozilla.github.io/pdf.js/web/viewer.html?file="
        "https://raw.githubusercontent.com/ionutms/"
        "Minimal_ADP1032/main/minimal_adp1032/minimal_adp1032.pdf"
    ),
    target="_blank",
)

layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col([
                html.H3(
                    f"{link_name.replace('_', ' ')}",
                    style=styles.heading_3_style,
                ),
            ]),
        ]),
        dbc.Row([
            dbc.Col(
                [dcu.app_description(TITLE, ABOUT, features, usage_steps)],
                width=12,
            ),
        ]),
        dbc.Row([
            dbc.Col(children=[clones_graph, visitors_graph], xs=12, md=8),
            dbc.Col(
                [
                    html.H4("Components Data Base Pages"),
                    links_display_div,
                    html.Hr(),
                    html.H4("Projects Pages"),
                    html.Div(
                        [
                            minimal_adp1032_github_repo_anchor_tag,
                            minimal_adp1032_interactive_bom_anchor_tag,
                            minimal_adp1032_schematics_anchor_tag,
                            html.Hr(),
                        ],
                        style={"display": "flex", "gap": "10px"},
                    ),
                ],
                xs=12,
                md=4,
            ),
        ]),
        html.Hr(),
    ],
    fluid=True,
)


def create_figure(
    theme_switch: bool,  # noqa: FBT001
    data_frames: list[pd.DataFrame],
    trace_colors: list[str],
    titles: tuple[str, str, str],
    relayout_data: dict[str, Any] | None = None,
) -> go.Figure:
    """Create a figure with data from multiple repositories.

    Args:
        theme_switch: Boolean indicating light/dark theme
        data_frames: List of DataFrames containing repository data
        trace_colors: List of colors for traces (two colors per DataFrame)
        titles: Tuple of (main_title, y1_title, y2_title)
        relayout_data: Optional relayout data from Plotly

    Returns:
        Plotly Figure object

    """
    # Calculate axis ranges across all dataframes
    all_timestamps = []
    y1_values = []
    y2_values = []

    for df in data_frames:
        all_timestamps.extend(df["clone_timestamp"])
        y1_values.extend(df["total_clones"])
        y2_values.extend(df["unique_clones"])

    all_timestamps = sorted(set(all_timestamps))
    min_timestamp, max_timestamp = min(all_timestamps), max(all_timestamps)

    y1_min, y1_max = min(y1_values), max(y1_values)
    y2_min, y2_max = min(y2_values), max(y2_values)

    # Add padding to y-axis ranges
    y1_padding = max(1, int((y1_max - y1_min) * 0.1))
    y2_padding = max(1, int((y2_max - y2_min) * 0.1))

    # Determine x-axis range based on relayout data
    x_range = [min_timestamp, max_timestamp]
    if relayout_data and "xaxis.range[0]" in relayout_data:
        x_range = [
            pd.to_datetime(relayout_data["xaxis.range[0]"]),
            pd.to_datetime(relayout_data["xaxis.range[1]"]),
        ]

    # Create tick labels
    tick_text = [ts.strftime("%m/%d") for ts in all_timestamps]

    # Optimize number of ticks
    max_ticks = 8
    num_data_points = len(all_timestamps)

    if num_data_points > max_ticks:
        tick_indices = list(
            range(0, num_data_points, num_data_points // max_ticks),
        )
        if tick_indices[-1] != num_data_points - 1:
            tick_indices.append(num_data_points - 1)

        all_timestamps = [all_timestamps[i] for i in tick_indices]
        tick_text = [tick_text[i] for i in tick_indices]

    # Create hover templates
    hover_template_total = (
        "Date: %{x|%Y-%m-%d}<br>Total %{data.name}: %{y}<br>"
    )
    hover_template_unique = (
        "Date: %{x|%Y-%m-%d}<br>Unique %{data.name}: %{y}<br>"
    )

    traces = []
    for data_frames_index, df in enumerate(data_frames):
        color_idx = data_frames_index * 2
        project_name = titles[3 + (data_frames_index * 2)]
        project_name = project_name.split(" ")[0]

        # Create a trace group for each project
        traces.extend([
            go.Scatter(
                x=df["clone_timestamp"],
                y=df["total_clones"],
                mode="lines+markers",
                name="Total",
                legendgroup=project_name,
                legendgrouptitle_text=project_name,
                marker={"color": trace_colors[color_idx], "size": 8},
                line={"color": trace_colors[color_idx], "width": 2},
                yaxis="y1",
                hovertemplate=hover_template_total,
            ),
            go.Scatter(
                x=df["clone_timestamp"],
                y=df["unique_clones"],
                mode="lines+markers",
                name="Unique",
                legendgroup=project_name,
                marker={"color": trace_colors[color_idx + 1], "size": 8},
                line={"color": trace_colors[color_idx + 1], "width": 2},
                yaxis="y2",
                hovertemplate=hover_template_unique,
                showlegend=True,
            ),
        ])

    # Figure layout configuration
    figure_layout = {
        "xaxis": {
            "gridcolor": "#808080",
            "griddash": "dash",
            "zerolinecolor": "lightgray",
            "zeroline": False,
            "domain": (0.0, 1.0),
            "showgrid": True,
            "title": {"text": "Date", "standoff": 10},
            "title_font_weight": "bold",
            "range": x_range,
            "type": "date",
            "tickmode": "array",
            "tickvals": all_timestamps,
            "ticktext": tick_text,
            "tickangle": -30,
            "fixedrange": True,
            "tickfont": {"color": "#808080", "weight": "bold"},
            "titlefont": {"color": "#808080"},
        },
        "yaxis": {
            "gridcolor": "#808080",
            "griddash": "dash",
            "zerolinecolor": "lightgray",
            "zeroline": False,
            "tickangle": -90,
            "position": 0.0,
            "title": titles[1],
            "showgrid": False,
            "anchor": "free",
            "autorange": False,
            "fixedrange": True,
            "range": [y1_min - y1_padding, y1_max + y1_padding],
            "tickformat": ".0f",
        },
        "yaxis2": {
            "gridcolor": "#808080",
            "griddash": "dash",
            "zerolinecolor": "lightgray",
            "zeroline": False,
            "tickangle": -90,
            "position": 1.0,
            "title": titles[2],
            "showgrid": False,
            "overlaying": "y",
            "side": "right",
            "autorange": False,
            "fixedrange": True,
            "range": [y2_min - y2_padding, y2_max + y2_padding],
            "tickformat": ".0f",
        },
        "title": {
            "text": titles[0],
            "x": 0.5,
            "xanchor": "center",
        },
        "showlegend": True,
        "legend": {
            "orientation": "h",
            "yanchor": "top",
            "y": 0.995,
            "xanchor": "left",
            "x": 0.005,
            "bgcolor": "rgba(255, 255, 255, 0.5)"
            if theme_switch
            else "rgba(0, 0, 0, 0.5)",
            "bordercolor": "rgba(0, 0, 0, 0)",
        },
    }

    figure = go.Figure(data=traces, layout=figure_layout)

    # Update layout with primary y-axis styling
    figure.update_layout(
        height=300,
        hovermode="x unified",
        yaxis={
            "tickcolor": trace_colors[0],
            "linecolor": trace_colors[0],
            "linewidth": 2,
            "title_font_color": trace_colors[0],
            "title_font_size": 14,
            "title_font_weight": "bold",
            "tickfont": {
                "color": trace_colors[0],
                "size": 12,
                "weight": "bold",
            },
            "title_standoff": 10,
        },
        yaxis2={
            "tickcolor": trace_colors[1],
            "linecolor": trace_colors[1],
            "linewidth": 2,
            "title_font_color": trace_colors[1],
            "title_font_size": 14,
            "title_font_weight": "bold",
            "tickfont": {
                "color": trace_colors[1],
                "size": 12,
                "weight": "bold",
            },
            "title_standoff": 10,
        },
    )

    # Theme configuration
    theme = {
        "template": "plotly" if theme_switch else "plotly_dark",
        "paper_bgcolor": "white" if theme_switch else "#222222",
        "plot_bgcolor": "white" if theme_switch else "#222222",
        "font_color": "black" if theme_switch else "white",
        "margin": {"l": 0, "r": 0, "t": 50, "b": 80},
    }

    figure.update_layout(
        **theme,
        modebar={
            "remove": [
                "zoom",
                "pan",
                "select2d",
                "lasso2d",
                "zoomIn2d",
                "zoomOut2d",
                "autoScale2d",
                "resetScale2d",
                "toImage",
            ],
        },
    )

    return figure


def adjust_y_axis_range(
    figure: go.Figure,
    data_frame1: pd.DataFrame,
    data_frame2: pd.DataFrame,
    data_frame3: pd.DataFrame,
    relayout_data: dict[str, Any] | None,
) -> go.Figure:
    """Adjust y-axis range based on the visible x-axis range."""
    if relayout_data and "xaxis.range[0]" in relayout_data:
        x_min = pd.Timestamp(relayout_data["xaxis.range[0]"])
        x_max = pd.Timestamp(relayout_data["xaxis.range[1]"])

        # Filter data within the zoomed range for both datasets
        filtered_df1 = data_frame1[
            (data_frame1["clone_timestamp"] >= x_min)
            & (data_frame1["clone_timestamp"] <= x_max)
        ]
        filtered_df2 = data_frame2[
            (data_frame2["clone_timestamp"] >= x_min)
            & (data_frame2["clone_timestamp"] <= x_max)
        ]
        filtered_df3 = data_frame3[
            (data_frame3["clone_timestamp"] >= x_min)
            & (data_frame3["clone_timestamp"] <= x_max)
        ]

        if (
            not filtered_df1.empty
            or not filtered_df2.empty
            or not filtered_df3.empty
        ):
            # Calculate ranges across both filtered datasets
            y1_min = min(
                filtered_df1["total_clones"].min()
                if not filtered_df1.empty
                else float("inf"),
                filtered_df2["total_clones"].min()
                if not filtered_df2.empty
                else float("inf"),
                filtered_df3["total_clones"].min()
                if not filtered_df3.empty
                else float("inf"),
            )
            y1_max = max(
                filtered_df1["total_clones"].max()
                if not filtered_df1.empty
                else float("-inf"),
                filtered_df2["total_clones"].max()
                if not filtered_df2.empty
                else float("-inf"),
                filtered_df3["total_clones"].max()
                if not filtered_df3.empty
                else float("-inf"),
            )
            y2_min = min(
                filtered_df1["unique_clones"].min()
                if not filtered_df1.empty
                else float("inf"),
                filtered_df2["unique_clones"].min()
                if not filtered_df2.empty
                else float("-inf"),
                filtered_df3["unique_clones"].min()
                if not filtered_df3.empty
                else float("-inf"),
            )
            y2_max = max(
                filtered_df1["unique_clones"].max()
                if not filtered_df1.empty
                else float("-inf"),
                filtered_df2["unique_clones"].max()
                if not filtered_df2.empty
                else float("-inf"),
                filtered_df3["unique_clones"].max()
                if not filtered_df3.empty
                else float("-inf"),
            )

            y1_padding = (y1_max - y1_min) * 0.05
            y2_padding = (y2_max - y2_min) * 0.05

            figure.layout.yaxis.update({
                "range": [y1_min - y1_padding, y1_max + y1_padding],
                "autorange": False,
            })

            figure.layout.yaxis2.update({
                "range": [y2_min - y2_padding, y2_max + y2_padding],
                "autorange": False,
            })

    return figure


@callback(
    Output("links_display", "children"),
    Input("links_store", "data"),
)
def display_links(links: list[dict] | None) -> html.Div | str:
    """Generate and display links based on the provided data."""
    if not links:
        return "Loading links..."

    return html.Div(
        [
            html.Div(dcc.Link(link["name"], href=link["path"]))
            for link in links
        ][:-1],
    )


def load_traffic_data(
    github_url: str,
    local_file: str,
    rename_columns: dict[str, str] | None = None,
) -> pd.DataFrame:
    """Load traffic data from GitHub, fallback to local file if needed.

    Args:
        github_url: URL of the CSV file on GitHub
        local_file: Path to local CSV file
        rename_columns: Optional dictionary to rename columns

    Returns:
        DataFrame with traffic data

    """
    try:
        # Try loading from GitHub
        data_frame = pd.read_csv(github_url)
    except (
        pd.errors.ParserError,
        pd.errors.EmptyDataError,
        OSError,
    ) as error_message:
        print(f"Error reading github file: {error_message} from {github_url}")
        try:
            # Fallback to local file
            data_frame = pd.read_csv(local_file)
        except (
            FileNotFoundError,
            pd.errors.ParserError,
            pd.errors.EmptyDataError,
        ) as error_message:
            print(f"Error reading local file: {error_message}")
            # Return empty DataFrame if both attempts fail
            return pd.DataFrame({
                "clone_timestamp": pd.Series(dtype="datetime64[ns]"),
                "total_clones": pd.Series(dtype="int"),
                "unique_clones": pd.Series(dtype="int"),
            })

    # Rename columns if specified
    if rename_columns:
        data_frame = data_frame.rename(columns=rename_columns)

    # Convert timestamp to datetime
    data_frame["clone_timestamp"] = pd.to_datetime(
        data_frame["clone_timestamp"],
    )

    return data_frame


@callback(
    Output(f"{module_name}_repo_clones_graph", "figure"),
    Output(f"{module_name}_repo_visitors_graph", "figure"),
    Input("theme_switch_value_store", "data"),
    Input(f"{module_name}_repo_clones_graph", "relayoutData"),
    Input(f"{module_name}_repo_visitors_graph", "relayoutData"),
)
def update_graph_with_uploaded_file(
    theme_switch: bool,  # noqa: FBT001
    clones_relayout: dict[str, Any] | None = None,
    visitors_relayout: dict[str, Any] | None = None,
) -> tuple[Any, dict[str, Any]]:
    """Read CSV data and update the repository graphs."""
    # Configure repositories with their specific CSV files
    repos = [
        {
            "name": "KiCAD_Symbols_Generator",
            "clones_csv": "kicad_symbols_generator_clones_history.csv",
            "visitors_csv": "kicad_symbols_generator_visitors_history.csv",
            "github_path": "repo_traffic_data",
            "local_path": "repo_traffic_data",
        },
        {
            "name": "Minimal_ADP1032",
            "clones_csv": "minimal_adp1032_clones_history.csv",
            "visitors_csv": "minimal_adp1032_visitors_history.csv",
            "github_path": "repo_traffic_data",
            "local_path": "repo_traffic_data",
        },
        {
            "name": "Minimal_MAX14906",
            "clones_csv": "minimal_max14906_clones_history.csv",
            "visitors_csv": "minimal_max14906_visitors_history.csv",
            "github_path": "repo_traffic_data",
            "local_path": "repo_traffic_data",
        },
    ]

    base_github_url = (
        "https://raw.githubusercontent.com/ionutms/"
        "KiCAD_Symbols_Generator/main"
    )
    clones_data = []
    visitors_data = []

    # Load data for each repository
    for repo in repos:
        # Clones data
        clones_source = {
            "github_url": (
                f"{base_github_url}/"
                f"{repo['github_path']}/{repo['clones_csv']}"
            ),
            "local_file": f"{repo['local_path']}/{repo['clones_csv']}",
            "rename_columns": None,
        }
        clones_data.append(load_traffic_data(**clones_source))

        # Visitors data
        visitors_source = {
            "github_url": (
                f"{base_github_url}/"
                f"{repo['github_path']}/{repo['visitors_csv']}"
            ),
            "local_file": f"{repo['local_path']}/{repo['visitors_csv']}",
            "rename_columns": {
                "visitor_timestamp": "clone_timestamp",
                "total_visitors": "total_clones",
                "unique_visitors": "unique_clones",
            },
        }
        visitors_data.append(load_traffic_data(**visitors_source))

    # Create titles using repository names
    trace_colors = [
        "#227b33",
        "#4187db",
        "#f0a088",
        "#f668c9",
        "#f0a022",
        "#f66822",
    ]
    clones_titles = ["Git Clones", "Clones", "Unique Clones"]
    visitors_titles = ["Visitors", "Views", "Unique Views"]

    # Add repository-specific titles
    for repo in repos:
        clones_titles.extend([
            f"{repo['name']} Clones",
            f"{repo['name']} Unique Clones",
        ])
        visitors_titles.extend([
            f"{repo['name']} Views",
            f"{repo['name']} Unique Views",
        ])

    # Create figures
    repo_clones_figure = create_figure(
        theme_switch=theme_switch,
        data_frames=clones_data,
        trace_colors=trace_colors,
        titles=tuple(clones_titles),
        relayout_data=clones_relayout,
    )
    repo_clones_figure = adjust_y_axis_range(
        repo_clones_figure,
        *clones_data,
        clones_relayout,
    )

    repo_visitors_figure = create_figure(
        theme_switch=theme_switch,
        data_frames=visitors_data,
        trace_colors=trace_colors,
        titles=tuple(visitors_titles),
        relayout_data=visitors_relayout,
    )
    repo_visitors_figure = adjust_y_axis_range(
        repo_visitors_figure,
        *visitors_data,
        visitors_relayout,
    )

    return repo_clones_figure, repo_visitors_figure
