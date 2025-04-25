"""Home page module for the Dash application.

This module defines the layout and callbacks for the main landing page of the
Dash app, providing a centralized dashboard for repository analytics and
navigation.

Key Features:
- Dynamic visualization of GitHub repository traffic metrics
- Graphs showing repository activity trends over time
- Automated generation of navigation links to other application pages
- Project-specific sections with direct links to GitHub, BOM, schematics,
    and 3D models
- Responsive Bootstrap-based layout that adapts to different screen sizes

The module uses a combination of Plotly graphs, Dash components, and Bootstrap
styling to create an interactive and informative dashboard experience.
"""

from __future__ import annotations

from typing import Any

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, State, callback, dcc, html

import pages.utils.dash_component_utils as dcu
import pages.utils.style_utils as styles

link_name = __name__.rsplit(".", maxsplit=1)[-1].replace("_page", "").title()
module_name = __name__.rsplit(".", maxsplit=1)[-1]

dash.register_page(__name__, name=link_name, path="/")

TITLE = "Home Page"

ABOUT = (
    "The Home page serves as a dynamic dashboard and analytics hub for "
    "monitoring repository activity and accessing multiple project "
    "resources.",
    "It combines GitHub traffic analytics with centralized "
    "navigation, providing insights into repository engagement while "
    "offering comprehensive access to project documentation, "
    "interactive tools, and hardware designs across all projects.",
)

features = [
    "Visualization of repository clones and visitor traffic using "
    "interactive graphs",
    "Automated tracking of multiple repositories with metrics "
    "for each project",
    "Direct links to project resources including GitHub repos, "
    "Interactive BOMs, and technical documentation",
    "Project-specific sections with detailed analytics and navigation links",
    "Integrated viewers for schematics (PDF), 3D models (WRL), "
    "and interactive BOMs (HTML)",
    "Dynamic navigation system that automatically updates as new pages are "
    "added to the application",
    "Responsive dashboard layout that adapts to different screen sizes and "
    "devices",
    "Dual-theme support with light and dark mode visualization options",
]

usage_steps = [
    "Monitor repository engagement through the interactive clone and "
    "visitor graphs",
    "Use the Components Data Base section to access different parts of the "
    "application",
    "Navigate to specific projects through their dedicated sections",
    "Access project resources through quick links to view GitHub "
    "repositories for source code and documentation, "
    "open interactive BOMs for component exploration, "
    "review schematics in the PDF viewer, "
    "examine 3D models in the online viewer",
    "Toggle between light and dark themes using the theme switch",
    "Navigate through different time periods using the graph's date axis",
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

    return [clones_graph, html.Hr(), visitors_graph]


links_display_div = html.Div(
    id="links_display",
    style={"display": "flex", "flex-direction": "column", "gap": "10px"},
)

image_prefixes = ["side", "top"]


def create_project_links(
    project_name: str,
    image_prefixes: list[str],
) -> html.Div:
    """Create links for a specific project with image carousel.

    Args:
        project_name (str): Name of the project (e.g., 'ADP1032')
        image_prefixes (list[str]): List of image prefixes

    Returns:
        html.Div: Div containing all project links and image carousel

    """
    project_name_lower = project_name.lower()
    base_github_url = f"https://github.com/ionutms/{project_name}"

    links = [
        html.A(
            children=f"GitHub Repo -> {project_name.replace('_', ' ')}",
            href=base_github_url,
            target="_blank",
        ),
        html.A(
            "View Interactive BOM (HTML)",
            href=(
                f"https://htmlpreview.github.io/?{base_github_url}/blob/main/"
                f"{project_name_lower}/bom/ibom.html"
            ),
            target="_blank",
        ),
        html.A(
            children="View Schematics (PDF)",
            href=(
                f"https://mozilla.github.io/pdf.js/web/viewer.html?file="
                f"https://raw.githubusercontent.com/ionutms/{project_name}/"
                f"main/{project_name_lower}/{project_name_lower}.pdf"
            ),
            target="_blank",
        ),
        html.A(
            children="View 3D Model (WRL)",
            href=(
                f"https://3dviewer.net/index.html#model={base_github_url}/"
                f"blob/main/{project_name_lower}/docs/3d_models/"
                f"{project_name_lower}.wrl"
            ),
            target="_blank",
        ),
        html.A(
            children="View 3D Model (GLB)",
            href=(
                f"https://3dviewer.net/index.html#model={base_github_url}/"
                f"blob/main/{project_name_lower}/docs/3d_models/"
                f"{project_name_lower}.glb"
            ),
            target="_blank",
        ),
    ]

    image_paths = [
        f"https://raw.githubusercontent.com/ionutms/{project_name}/"
        f"main/{project_name_lower}/docs/pictures/"
        f"{project_name_lower}_{prefix}.png"
        for prefix in image_prefixes
    ]

    modal_carousel_items = [{"src": img_path} for img_path in image_paths]

    modal = dbc.Modal(
        [
            dbc.ModalBody(
                dbc.Carousel(
                    items=modal_carousel_items,
                    controls=True,
                    indicators=False,
                    interval=None,
                    id=f"{project_name_lower}_modal_carousel",
                ),
            ),
        ],
        id=f"{project_name_lower}_modal",
        size="lg",
        is_open=False,
    )

    carousel = dbc.Carousel(
        items=[{"src": img_path} for img_path in image_paths],
        controls=False,
        indicators=False,
        id=f"{project_name_lower}_carousel",
        style={"cursor": "pointer"},
    )

    carousel_controls = html.Div(
        [
            dbc.Button(
                "Previous",
                id=f"{project_name_lower}_carousel_prev",
                color="primary",
                outline=True,
                size="sm",
                className="me-2",
                n_clicks=0,
            ),
            dbc.Button(
                "View Full Size",
                id=f"{project_name_lower}_view_details",
                color="primary",
                outline=True,
                size="sm",
                className="me-2",
                n_clicks=0,
            ),
            dbc.Button(
                "Next",
                id=f"{project_name_lower}_carousel_next",
                color="primary",
                outline=True,
                size="sm",
                className="me-2",
                n_clicks=0,
            ),
        ],
        className="d-flex justify-content-center mt-2",
    )

    carousel_div = html.Div(
        children=[carousel, carousel_controls],
        style={
            "marginTop": "1px",
            "marginBottom": "1px",
            "borderRadius": "10px",
            "overflow": "hidden",
        },
    )

    return html.Div(
        children=[*links, carousel_div, modal],
        style={
            "display": "flex",
            "flex-direction": "column",
            "gap": "10px",
        },
    )


REPOS_NAMES = [
    "KiCAD_Symbols_Generator",
    "3D_Models_Vault",
    "docker_kicad_learning",
    "Minimal_ADP1032",
    "Minimal_MAX14906",
    "Minimal_AD74413R",
    "Modular_Software_Configurable_IO_PLC",
    "Minimal_ADIN1110",
    "Minimal_LTC9111",
    "Minimal_MAX17761",
    "Minimal_LT8304",
    "Minimal_MAX32650",
]

COLORS = [
    ["#2E8B57", "#4169E1"],
    ["#66CED1", "#668C00"],
    ["#aaCED1", "#aa8C00"],
    ["#FF4500", "#9932CC"],
    ["#FFD700", "#C71585"],
    ["#20B2AA", "#FF6B6B"],
    ["#1E90FF", "#8A2BE2"],
    ["#32CD32", "#FF69B4"],
    ["#40E0D0", "#FF7F50"],
    ["#228B22", "#FF1493"],
    ["#00CED1", "#FF8C00"],
    ["#3390FF", "#332BE2"],
]

REPOS_DATA = []

for repo_index, repo_name in enumerate(REPOS_NAMES):
    REPOS_DATA.append(
        {
            "name": repo_name,
            "clones_csv": f"{repo_name.lower()}_clones_history.csv",
            "visitors_csv": f"{repo_name.lower()}_visitors_history.csv",
            "colors": COLORS[repo_index],
        },
    )


PROJECTS = [repo["name"] for repo in REPOS_DATA[1:]]


def register_modal_callbacks() -> None:
    """Register callbacks for project modals."""
    for project in PROJECTS:
        if project in ("3D_Models_Vault", "docker_kicad_learning"):
            continue

        project_lower = project.lower()

        @callback(
            Output(f"{project_lower}_modal", "is_open"),
            Input(f"{project_lower}_view_details", "n_clicks"),
            State(f"{project_lower}_modal", "is_open"),
        )
        def toggle_modal(
            view_details_clicks: int | None,
            is_open: bool,  # noqa: FBT001
        ) -> bool:
            """Toggle modal visibility.

            Args:
                view_details_clicks: Click count for the view details button
                is_open: Current state of the modal

            Returns:
                bool: Updated modal visibility state

            """
            if view_details_clicks:
                return not is_open
            return is_open


def register_carousel_callbacks(num_items: int) -> None:
    """Register callbacks for carousel control buttons."""
    for project in PROJECTS:
        if project in ("3D_Models_Vault", "docker_kicad_learning"):
            continue

        project_lower = project.lower()

        @callback(
            Output(f"{project_lower}_carousel", "active_index"),
            Input(f"{project_lower}_carousel_prev", "n_clicks"),
            Input(f"{project_lower}_carousel_next", "n_clicks"),
            State(f"{project_lower}_carousel", "active_index"),
        )
        def control_carousel(
            _prev_clicks: int | None,
            _next_clicks: int | None,
            current_index: int,
        ) -> int:
            """Control carousel with next/prev buttons.

            Args:
                prev_clicks: Click count for the prev button
                next_clicks: Click count for the next button
                current_index: Current active slide index

            Returns:
                int: Updated active slide index

            """
            # Determine which button was clicked
            ctx = dash.callback_context
            if not ctx.triggered:
                return current_index or 0

            button_id = ctx.triggered[0]["prop_id"].split(".")[0]

            if button_id.endswith("_carousel_prev"):
                return (current_index - 1) % num_items

            if button_id.endswith("_carousel_next"):
                return (current_index + 1) % num_items

            return current_index or 0


register_modal_callbacks()
register_carousel_callbacks(len(image_prefixes))


def create_header_section(
    link_name: str,
    title: str,
    about: tuple[str, str],
    features: list[str],
    usage_steps: list[str],
) -> list[Any]:
    """Create the header section with title and description.

    Args:
        link_name (str): Name of the link
        title (str): Title of the page
        about (tuple[str, str]): Description of the page
        features (list[str]): List of features
        usage_steps (list[str]): List of usage steps

    Returns:
        List of components for the header section

    """
    return [
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
                [dcu.app_description(title, about, features, usage_steps)],
                width=12,
            ),
        ]),
    ]


def create_main_repo_section(
    module_name: str,
    links_display_div: html.Div,
) -> list[Any]:
    """Create repository section with graphs and component links.

    Args:
        module_name (str): Name of the module
        links_display_div (html.Div): Div containing all project links

    Returns:
        List of components for the main repository section

    """
    return [
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
    ]


def create_project_section(module_name: str, project: str) -> list[Any]:
    """Create a section for an individual project with graphs and links.

    Args:
        module_name (str): Name of the module
        project (str): Name of the project

    Returns:
        List of components for the project section

    """
    # For 3D_Models_Vault, don't create the project links
    if project in ("3D_Models_Vault", "docker_kicad_learning"):
        return [
            dbc.Row([
                dbc.Col(
                    children=create_repo_graphs(f"{module_name}_{project}"),
                    xs=12,
                    md=8,
                ),
            ]),
            html.Hr(),
        ]
    return [
        dbc.Row([
            dbc.Col(
                children=create_repo_graphs(f"{module_name}_{project}"),
                xs=12,
                md=8,
            ),
            dbc.Col(
                [
                    html.H4("Project Pages"),
                    create_project_links(project, image_prefixes),
                ],
                xs=12,
                md=4,
            ),
        ]),
        html.Hr(),
    ]


# Main layout construction
layout = dbc.Container(
    [
        *create_header_section(
            link_name,
            TITLE,
            ABOUT,
            features,
            usage_steps,
        ),
        *create_main_repo_section(module_name, links_display_div),
        *[
            component
            for project in PROJECTS
            for component in create_project_section(module_name, project)
        ],
    ],
    fluid=True,
)


def create_figure(
    theme_switch: bool,  # noqa: FBT001
    data_frames: list[pd.DataFrame],
    trace_colors: list[str],
    titles: tuple[str, str, str],
) -> go.Figure:
    """Create a figure with data from multiple repositories.

    Args:
        theme_switch: Boolean indicating light/dark theme
        data_frames: List of DataFrames containing repository data
        trace_colors: List of colors for traces (two colors per DataFrame)
        titles: Tuple of (main_title, y1_title, y2_title)

    Returns:
        Plotly Figure object

    """
    # Calculate axis ranges across all dataframes
    all_timestamps = []
    y1_values = []
    y2_values = []

    for df in data_frames:
        if not df.empty:
            all_timestamps.extend(df["clone_timestamp"])
            y1_values.extend(df["total_clones"])
            y2_values.extend(df["unique_clones"])

    # If no data is available, return an empty figure with a message
    if not all_timestamps:
        figure = go.Figure()
        figure.update_layout(
            annotations=[
                {
                    "text": "No data available",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 20},
                },
            ],
            height=250,
            template="plotly" if theme_switch else "plotly_dark",
            paper_bgcolor="white" if theme_switch else "#222222",
            plot_bgcolor="white" if theme_switch else "#222222",
            font_color="black" if theme_switch else "white",
        )
        return figure

    all_timestamps = sorted(set(all_timestamps))
    min_timestamp, max_timestamp = min(all_timestamps), max(all_timestamps)

    y1_min, y1_max = min(y1_values), max(y1_values)
    y2_min, y2_max = min(y2_values), max(y2_values)

    # Add padding to y-axis ranges
    y1_padding = max(1, int((y1_max - y1_min) * 0.1))
    y2_padding = max(1, int((y2_max - y2_min) * 0.1))

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
        if df.empty:
            continue

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
            "title": {
                "text": "Date",
                "standoff": 10,
                "font": {"color": "#808080"},
            },
            "title_font_weight": "bold",
            "range": [min_timestamp, max_timestamp],
            "type": "date",
            "tickmode": "array",
            "tickvals": all_timestamps,
            "ticktext": tick_text,
            "tickangle": -30,
            "fixedrange": True,
            "tickfont": {"color": "#808080", "weight": "bold"},
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
        height=250,
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
        "margin": {"l": 0, "r": 0, "t": 30, "b": 30},
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
        DataFrame with traffic data, with missing dates filled with 0.

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

    # Ensure missing dates are filled with 0
    if not data_frame.empty:
        date_range = pd.date_range(
            start=data_frame["clone_timestamp"].min(),
            end=data_frame["clone_timestamp"].max(),
        )
        data_frame = (
            data_frame.set_index("clone_timestamp")
            .reindex(date_range, fill_value=0)
            .reset_index()
            .rename(columns={"index": "clone_timestamp"})
        )

    return data_frame


@callback(
    Output(f"{module_name}_repo_clones_graph", "figure"),
    Output(f"{module_name}_repo_visitors_graph", "figure"),
    *[
        Output(f"{module_name}_{project}_repo_{graph}_graph", "figure")
        for project in PROJECTS
        for graph in ["clones", "visitors"]
    ],
    Input("theme_switch_value_store", "data"),
)
def update_graph_with_uploaded_file(
    theme_switch: bool,  # noqa: FBT001
) -> tuple[Any, ...]:
    """Read CSV data and update the repository graphs."""
    base_github_url = (
        "https://raw.githubusercontent.com/ionutms/"
        "KiCAD_Symbols_Generator/main"
    )

    def load_repo_data(
        repo_config: dict,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Load clones and visitors data for a repository."""
        clones_source = {
            "github_url": (
                f"{base_github_url}/repo_traffic_data/"
                f"{repo_config['clones_csv']}"
            ),
            "local_file": f"repo_traffic_data/{repo_config['clones_csv']}",
            "rename_columns": None,
        }

        visitors_source = {
            "github_url": (
                f"{base_github_url}/repo_traffic_data/"
                f"{repo_config['visitors_csv']}"
            ),
            "local_file": f"repo_traffic_data/{repo_config['visitors_csv']}",
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
    repo_data = [load_repo_data(repo_config) for repo_config in REPOS_DATA]
    clones_data, visitors_data = zip(*repo_data)

    # Generate titles in the original order
    clones_titles = ["Git Clones", "Clones", "Unique Clones"]
    visitors_titles = ["Visitors", "Views", "Unique Views"]

    for repo_config in REPOS_DATA:
        clones_titles.extend([
            f"{repo_config['name']} Clones",
            f"{repo_config['name']} Unique Clones",
        ])
        visitors_titles.extend([
            f"{repo_config['name']} Views",
            f"{repo_config['name']} Unique Views",
        ])

    def create_and_adjust_figure(
        data_frames: list[pd.DataFrame],
        trace_colors: list[str],
        titles: tuple[str, ...],
        theme_switch: bool,  # noqa: FBT001
    ) -> dict[str, Any]:
        """Create and adjust a figure with the given parameters."""
        return create_figure(
            theme_switch=theme_switch,
            data_frames=data_frames,
            trace_colors=trace_colors,
            titles=titles,
        )

    # Update figure creation calls to remove relayout_data parameter
    figures = []
    for repo_index in range(len(REPOS_DATA)):
        repos_to_exclude = (
            REPOS_DATA[1:] if repo_index == 0 else REPOS_DATA[:repo_index]
        )

        filtered_clones_titles = [
            title
            for title in clones_titles
            if not any(
                repo_config["name"] in title
                for repo_config in repos_to_exclude
            )
        ]
        filtered_visitors_titles = [
            title
            for title in visitors_titles
            if not any(
                repo_config["name"] in title
                for repo_config in repos_to_exclude
            )
        ]

        current_repo = REPOS_DATA[repo_index]
        figures.append(
            create_and_adjust_figure(
                [clones_data[repo_index]],
                current_repo["colors"],
                tuple(filtered_clones_titles),
                theme_switch,
            ),
        )
        figures.append(
            create_and_adjust_figure(
                [visitors_data[repo_index]],
                current_repo["colors"],
                tuple(filtered_visitors_titles),
                theme_switch,
            ),
        )

    return tuple(figures)
