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


def create_repo_graphs(name_sufix: str) -> list[dcc.Loading]:
    """Create repository graphs for clones and visitors.

    Args:
        name_sufix (str): Suffix to append to the graph IDs

    Returns:
        list[dcc.Loading]: List of Loading components containing the graphs

    """
    clones_graph = dcc.Loading(
        [
            dcc.Graph(
                id=f"{name_sufix}_repo_clones_graph",
                config={"displaylogo": False},
            ),
        ],
        delay_show=100,
        delay_hide=100,
    )

    visitors_graph = dcc.Loading(
        [
            dcc.Graph(
                id=f"{name_sufix}_repo_visitors_graph",
                config={"displaylogo": False},
            ),
        ],
        delay_show=100,
        delay_hide=100,
    )

    return [clones_graph, visitors_graph]


links_display_div = html.Div(
    id="links_display",
    style={"display": "flex", "flex-direction": "column", "gap": "10px"},
)


def create_project_links(project_name: str) -> html.Div:
    """Generate GitHub repo, Interactive BOM, and Schematics links.

    Args:
        project_name (str): Name of the project (e.g., 'ADP1032')

    Returns:
        html.Div: Div containing all project links

    """
    project_name_lower = project_name.lower()
    base_github_url = f"https://github.com/ionutms/{project_name}"

    links = [
        html.A(
            children=f"{project_name.replace('_', ' ')}",
            href=base_github_url,
            target="_blank",
        ),
        html.A(
            "Interactive BOM",
            href=(
                f"https://htmlpreview.github.io/?{base_github_url}/blob/main/"
                f"{project_name_lower}/bom/ibom.html"
            ),
            target="_blank",
        ),
        html.A(
            children="Schematics",
            href=(
                f"https://mozilla.github.io/pdf.js/web/viewer.html?file="
                f"https://raw.githubusercontent.com/ionutms/{project_name}/"
                f"main/{project_name_lower}/{project_name_lower}.pdf"
            ),
            target="_blank",
        ),
        html.Hr(),
    ]

    return html.Div(
        children=[*links],
        style={"display": "flex", "gap": "10px"},
    )


PROJECTS = ["Minimal_ADP1032", "Minimal_MAX14906", "Minimal_AD74413R"]

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
            dbc.Col(
                children=create_repo_graphs(f"{module_name}"),
                xs=12,
                md=8,
            ),
            dbc.Col(
                [
                    html.H4("Components Data Base Pages"),
                    links_display_div,
                ],
                xs=12,
                md=4,
            ),
        ]),
        html.Hr(),
        html.H4("Projects Pages"),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                children=create_repo_graphs(f"{module_name}_{PROJECTS[0]}"),
                xs=12,
                md=8,
            ),
            dbc.Col(
                [
                    create_project_links(PROJECTS[0]),
                ],
                xs=12,
                md=4,
            ),
        ]),
        dbc.Row([
            dbc.Col(
                children=create_repo_graphs(f"{module_name}_{PROJECTS[1]}"),
                xs=12,
                md=8,
            ),
            dbc.Col(
                [
                    create_project_links(PROJECTS[1]),
                ],
                xs=12,
                md=4,
            ),
        ]),
        dbc.Row([
            dbc.Col(
                children=create_repo_graphs(f"{module_name}_{PROJECTS[2]}"),
                xs=12,
                md=8,
            ),
            dbc.Col(
                [
                    create_project_links(PROJECTS[2]),
                ],
                xs=12,
                md=4,
            ),
        ]),
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
    relayout_data: dict[str, Any] | None,
    *dataframes: pd.DataFrame,
) -> go.Figure:
    """Adjust y-axis range based on the visible x-axis range.

    Args:
        figure: The plotly figure to adjust
        relayout_data: The relayout data containing x-axis range information
        *dataframes: Variable number of pandas DataFrames to process

    """

    def filter_dataframe(
        df: pd.DataFrame,
        x_min: pd.Timestamp,
        x_max: pd.Timestamp,
    ) -> pd.DataFrame:
        """Filter dataframe based on timestamp range."""
        return df[
            (df["clone_timestamp"] >= x_min)
            & (df["clone_timestamp"] <= x_max)
        ]

    def get_column_range(
        dataframes: list[pd.DataFrame],
        column: str,
    ) -> tuple[float, float]:
        """Calculate min and max values for a column across all dataframes."""
        valid_dfs = [df for df in dataframes if not df.empty]
        if not valid_dfs:
            return 0, 0  # Return default range if all dataframes are empty

        min_val = min(df[column].min() for df in valid_dfs)
        max_val = max(df[column].max() for df in valid_dfs)
        return min_val, max_val

    if not dataframes:
        return figure  # Return unchanged figure if no dataframes provided

    if relayout_data and "xaxis.range[0]" in relayout_data:
        x_min = pd.Timestamp(relayout_data["xaxis.range[0]"])
        x_max = pd.Timestamp(relayout_data["xaxis.range[1]"])

        # Filter all dataframes
        filtered_dfs = [
            filter_dataframe(df, x_min, x_max) for df in dataframes
        ]

        if any(not df.empty for df in filtered_dfs):
            # Calculate ranges for both total and unique clones
            y1_min, y1_max = get_column_range(filtered_dfs, "total_clones")
            y2_min, y2_max = get_column_range(filtered_dfs, "unique_clones")

            # Calculate padding
            y1_padding = (y1_max - y1_min) * 0.05 if y1_max > y1_min else 1
            y2_padding = (y2_max - y2_min) * 0.05 if y2_max > y2_min else 1

            # Update both y-axes
            for axis, y_min, y_max, padding in [
                (figure.layout.yaxis, y1_min, y1_max, y1_padding),
                (figure.layout.yaxis2, y2_min, y2_max, y2_padding),
            ]:
                axis.update({
                    "range": [y_min - padding, y_max + padding],
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
    Output(f"{module_name}_{PROJECTS[0]}_repo_clones_graph", "figure"),
    Output(f"{module_name}_{PROJECTS[0]}_repo_visitors_graph", "figure"),
    Output(f"{module_name}_{PROJECTS[1]}_repo_clones_graph", "figure"),
    Output(f"{module_name}_{PROJECTS[1]}_repo_visitors_graph", "figure"),
    Output(f"{module_name}_{PROJECTS[2]}_repo_clones_graph", "figure"),
    Output(f"{module_name}_{PROJECTS[2]}_repo_visitors_graph", "figure"),
    Input("theme_switch_value_store", "data"),
    Input(f"{module_name}_repo_clones_graph", "relayoutData"),
    Input(f"{module_name}_repo_visitors_graph", "relayoutData"),
)
def update_graph_with_uploaded_file(
    theme_switch: bool,  # noqa: FBT001
    clones_relayout: dict[str, Any] | None = None,
    visitors_relayout: dict[str, Any] | None = None,
) -> tuple[Any, ...]:
    """Read CSV data and update the repository graphs."""
    repos = [
        {
            "name": "KiCAD_Symbols_Generator",
            "clones_csv": "kicad_symbols_generator_clones_history.csv",
            "visitors_csv": "kicad_symbols_generator_visitors_history.csv",
            "colors": ["#2E8B57", "#4169E1"],
        },
        {
            "name": "Minimal_ADP1032",
            "clones_csv": "minimal_adp1032_clones_history.csv",
            "visitors_csv": "minimal_adp1032_visitors_history.csv",
            "colors": ["#FF4500", "#9932CC"],
        },
        {
            "name": "Minimal_MAX14906",
            "clones_csv": "minimal_max14906_clones_history.csv",
            "visitors_csv": "minimal_max14906_visitors_history.csv",
            "colors": ["#FFD700", "#C71585"],
        },
        {
            "name": "Minimal_AD74413R",
            "clones_csv": "minimal_ad74413r_clones_history.csv",
            "visitors_csv": "minimal_ad74413r_visitors_history.csv",
            "colors": ["#20B2AA", "#8B4513"],
        },
    ]

    base_github_url = (
        "https://raw.githubusercontent.com/ionutms/"
        "KiCAD_Symbols_Generator/main"
    )

    def load_repo_data(repo: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Load clones and visitors data for a repository."""
        clones_source = {
            "github_url": (
                f"{base_github_url}/repo_traffic_data/{repo['clones_csv']}"
            ),
            "local_file": f"repo_traffic_data/{repo['clones_csv']}",
            "rename_columns": None,
        }

        visitors_source = {
            "github_url": (
                f"{base_github_url}/repo_traffic_data/{repo['visitors_csv']}"
            ),
            "local_file": f"repo_traffic_data/{repo['visitors_csv']}",
            "rename_columns": {
                "visitor_timestamp": "clone_timestamp",
                "total_visitors": "total_clones",
                "unique_visitors": "unique_clones",
            },
        }

        return (
            load_traffic_data(**clones_source),
            load_traffic_data(**visitors_source),
        )

    # Load all repository data
    repo_data = [load_repo_data(repo) for repo in repos]
    clones_data, visitors_data = zip(*repo_data)

    # Generate titles in the original order
    clones_titles = ["Git Clones", "Clones", "Unique Clones"]
    visitors_titles = ["Visitors", "Views", "Unique Views"]

    for repo in repos:
        clones_titles.extend([
            f"{repo['name']} Clones",
            f"{repo['name']} Unique Clones",
        ])
        visitors_titles.extend([
            f"{repo['name']} Views",
            f"{repo['name']} Unique Views",
        ])

    def create_and_adjust_figure(
        data_frames: list[pd.DataFrame],
        trace_colors: list[str],
        titles: tuple[str, ...],
        theme_switch: bool,  # noqa: FBT001
        relayout_data: dict[str, Any] | None,
    ) -> dict[str, Any]:
        """Create and adjust a figure with the given parameters."""
        figure = create_figure(
            theme_switch=theme_switch,
            data_frames=data_frames,
            trace_colors=trace_colors,
            titles=titles,
            relayout_data=relayout_data,
        )
        return adjust_y_axis_range(figure, relayout_data, *data_frames)

    # Create all figures in a single loop
    figures = []
    for i in range(len(repos)):  # Generate figures for all repositories
        # Determine which repos to exclude from titles
        repos_to_exclude = repos[1:] if i == 0 else repos[:i]

        filtered_clones_titles = [
            x
            for x in clones_titles
            if not any(repo["name"] in x for repo in repos_to_exclude)
        ]
        filtered_visitors_titles = [
            x
            for x in visitors_titles
            if not any(repo["name"] in x for repo in repos_to_exclude)
        ]

        repo = repos[i]
        figures.append(
            create_and_adjust_figure(
                [clones_data[i]],
                repo["colors"],
                tuple(filtered_clones_titles),
                theme_switch,
                clones_relayout,
            ),
        )
        figures.append(
            create_and_adjust_figure(
                [visitors_data[i]],
                repo["colors"],
                tuple(filtered_visitors_titles),
                theme_switch,
                visitors_relayout,
            ),
        )

    return tuple(figures)
