"""Capacitors Database Page.

This module provides a Dash page for viewing and interacting with capacitor
specifications. It allows users to browse, search, and filter through a
database of capacitors, with features for customizing the view and accessing
detailed information.

Key features:
- Interactive DataTable displaying capacitor specifications
- Column visibility controls for customizing the view
- Dynamic filtering and multi-column sorting capabilities
- Pagination with customizable page size
- Theme-aware styling with light/dark mode support
- Direct links to capacitor datasheets
- Responsive design for various screen sizes

The module uses Dash components and callbacks to create an interactive
interface for data visualization and exploration. It integrates with
Bootstrap components for a polished user interface and includes
comprehensive styling support for both light and dark themes.
"""

from typing import Any

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pages.utils.dash_component_utils as dcu
import pages.utils.style_utils as styles
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html, register_page

link_name = __name__.rsplit(".", maxsplit=1)[-1].replace("_page", "").title()
module_name = __name__.rsplit(".", maxsplit=1)[-1]

register_page(__name__, name=link_name, order=3)

ag_grid_data: pd.DataFrame = pd.read_csv(
    "data/UNITED_CAPACITORS_DATA_BASE.csv"
)
total_rows = len(ag_grid_data)

TITLE = "Capacitors Database"
ABOUT = (
    "The Capacitors Database is an interactive web application that "
    "provides a comprehensive view of capacitor specifications.",
    "It allows users to easily browse, search, and filter "
    f"through a database of {total_rows:,} capacitors, "
    "providing quick access to important information and datasheets.",
)

features = [
    "Interactive data table displaying capacitor specifications",
    "Dynamic filtering and multi-column sorting capabilities",
    "Customizable pagination with adjustable items per page",
    "Direct links to capacitor datasheets",
    "Responsive design adapting to light and dark themes",
    "Easy-to-use interface for exploring capacitor data",
    "Customizable column visibility",
]

usage_steps = [
    "Navigate to the Capacitors Database page",
    "Use the table's built-in search functionality "
    "to find specific capacitors",
    "Click on column headers to sort the data",
    "Use the filter action to narrow down the displayed results",
    "Toggle column visibility using the checkboxes above the table",
    "Adjust the number of items per page using the dropdown menu",
    "Navigate through pages using the pagination controls at "
    "the bottom of the table",
    "Access capacitor datasheets by clicking on the provided links in the "
    "'Datasheet' column",
    "Switch between light and dark themes for comfortable viewing in "
    "different environments",
]

hidden_columns = [
    "Reference",
    "Case Code - mm",
    "Case Code - in",
    "Series",
    "Dielectric",
    "Tolerance",
    "Voltage Rating",
    "Capacitor Type",
    "MPN",
    "Description",
]

visible_columns = [
    col for col in ag_grid_data.columns if col not in hidden_columns
]


# Convert specific columns to markdown format links for AG Grid
url_columns = ["Datasheet", "Trustedparts Search", "3dviewer Link"]

for col in url_columns:
    if col in ag_grid_data.columns:
        ag_grid_data[col] = ag_grid_data[col].apply(
            lambda url: f"[{col}]({url})" if pd.notna(url) and url else ""
        )

layout = dbc.Container(
    [
        html.Div(
            [
                dbc.Row([dbc.Col([dcc.Link("Go back Home", href="/")])]),
                dbc.Row([
                    dbc.Col([
                        html.H3(
                            f"{link_name.replace('_', ' ')} "
                            f"({total_rows:,} items)",
                            style=styles.heading_3_style,
                        ),
                    ]),
                ]),
                dbc.Row([
                    dcu.app_description(TITLE, ABOUT, features, usage_steps),
                ]),
                dcu.generate_range_slider(module_name, ag_grid_data, 25),
                html.Hr(),
                dbc.Row([
                    dcc.Loading(
                        [
                            dcc.Graph(
                                id=f"{module_name}_bar_graph",
                                config={"displaylogo": False},
                            ),
                        ],
                        delay_show=100,
                        delay_hide=100,
                    ),
                ]),
                html.Hr(),
                dcu.ag_grid_table_controls_row(
                    module_name,
                    ag_grid_data,
                    visible_columns,
                ),
                html.Hr(),
                dag.AgGrid(
                    id=f"{module_name}_ag_grid_table",
                    rowData=ag_grid_data.to_dict("records"),
                    defaultColDef={"filter": True},
                    style={"height": 200},
                ),
                html.Hr(),
            ],
            style=styles.GLOBAL_STYLE,
        ),
    ],
    fluid=True,
)

dcu.callback_update_ag_grid_visible_table_columns(
    f"{module_name}_ag_grid_table",
    f"{module_name}_column_toggle",
    ag_grid_data,
    url_columns,
)

dcu.callback_update_ag_grid_table_theme(f"{module_name}_ag_grid_table")

dcu.save_previous_slider_state_callback(
    f"{module_name}_value_rangeslider",
    f"{module_name}_rangeslider_store",
    step=25,
)


def get_visible_y_max(
    figure_data: list[go.Bar],
    x_range: tuple[int, int],
) -> int:
    """Get the maximum y value within the visible x range.

    Args:
        figure_data (list[go.Bar]): List of bar traces in the figure.
        x_range (tuple[int, int]): The visible x-axis range.

    Returns:
        int: The maximum y value within the visible x range.

    """
    x_min, x_max = x_range
    maximum_y_value = 0

    for trace in figure_data:
        # Get positions within range
        positions = range(len(trace.x))
        visible_positions = [
            index for index in positions if x_min <= index <= x_max
        ]

        if visible_positions:
            y_values = [trace.y[index] for index in visible_positions]
            maximum_y_value += max(y_values)

    return maximum_y_value


@callback(
    Output(f"{module_name}_bar_graph", "figure"),
    Input("theme_switch_value_store", "data"),
    Input(f"{module_name}_value_rangeslider", "value"),
)
def update_distribution_graph(
    theme_switch: bool,  # noqa: FBT001
    rangeslider_value: list[int],
) -> tuple[Any, dict[str, Any]]:
    """Create a bar graph showing the distribution of components values.

    Args:
        theme_switch (bool): Indicates the current theme (light/dark).
        rangeslider_value:
            Range slider values for filtering components values.

    Returns:
        Plotly figure with components distribution visualization.

    """
    # Prepare full data range
    values, _ = dcu.extract_consecutive_value_groups(
        ag_grid_data["Value"].to_list(),
    )

    # Dynamically extract all unique tolerances
    tolerances = sorted(ag_grid_data["Tolerance"].unique())

    # Create tolerance-based dataframes and configurations
    tolerance_configs = [
        {
            "dataframe": ag_grid_data[ag_grid_data["Tolerance"] == tolerance],
            "name": f"{tolerance} Tolerance",
        }
        for tolerance in tolerances
    ]

    # Existing figure layout configuration
    figure_layout = {
        "xaxis": {
            "gridcolor": "#808080",
            "griddash": "dash",
            "zerolinecolor": "lightgray",
            "zeroline": False,
            "domain": (0.0, 1.0),
            "showgrid": True,
            "title": {
                "text": "Capacitance Value",
                "standoff": 10,
                "font": {"color": "#808080"},
            },
            "title_font_weight": "bold",
            "tickmode": "array",
            "tickangle": -45,
            "fixedrange": True,
            "tickfont": {"color": "#808080", "weight": "bold"},
        },
        "yaxis": {
            "gridcolor": "#808080",
            "griddash": "dash",
            "zerolinecolor": "lightgray",
            "zeroline": False,
            "tickangle": -45,
            "title_font_weight": "bold",
            "position": 0.0,
            "title": {
                "text": "Number of Capacitors",
                "font": {"color": "#808080"},
            },
            "fixedrange": True,
            "tickfont": {"color": "#808080", "weight": "bold"},
            "showgrid": True,
            "anchor": "free",
            "autorange": True,
            "tickformat": ".0f",
            "dtick": 2,
            "tickmode": "linear",
        },
        "title": {
            "text": "Capacitance Value Distribution",
            "x": 0.5,
            "xanchor": "center",
        },
        "showlegend": True,
    }

    # Create the figure
    figure = go.Figure(layout=figure_layout)

    # Add traces for each tolerance group
    for config in tolerance_configs:
        # Extract values and counts
        values_tolerance, counts_tolerance = (
            dcu.extract_consecutive_value_groups(
                config["dataframe"]["Value"].to_list(),
            )
        )

        # Pad values and counts to match full range
        values_tolerance, counts_tolerance = dcu.pad_values_and_counts(
            values,
            values_tolerance,
            counts_tolerance,
        )

        # Add trace for this tolerance group
        figure.add_trace(
            go.Bar(
                x=values_tolerance,
                y=counts_tolerance,
                name=config["name"],
                textposition="none",
                textangle=-30,
                text=counts_tolerance,
                hovertemplate=(
                    "Capacitance: %{x}<br>"
                    "Number of Capacitors: %{y}<extra></extra>"
                ),
            ),
        )

    # In update_distribution_graph function:
    x_min, x_max = rangeslider_value[0], rangeslider_value[1]
    y_max = get_visible_y_max(figure.data, (x_min, x_max))

    # Add scatter traces for all tolerances
    for tolerance in tolerances:
        tolerance_data = ag_grid_data[ag_grid_data["Tolerance"] == tolerance]
        scatter_x = []
        scatter_y = []
        scatter_mpn = []  # Track MPN for each point

        # Track cumulative heights at each x position
        cumulative_heights = {}

        for value in tolerance_data["Value"].unique():
            value_data = tolerance_data[tolerance_data["Value"] == value]
            count = len(value_data)
            base_height = 0

            # Get the base height from previous tolerance bars
            for trace in figure.data:
                if isinstance(trace, go.Bar):
                    value_index = list(trace.x).index(value)
                    if trace.name == f"{tolerance} Tolerance":
                        break
                    base_height += trace.y[value_index]

            # Add dots stacked on top of base height
            for dot_position, mpn in enumerate(value_data["MPN"]):
                scatter_x.append(value)
                scatter_y.append(base_height + dot_position + 0.5)
                scatter_mpn.append(mpn)

            cumulative_heights[value] = base_height + count

        figure.add_trace(
            go.Scatter(
                x=scatter_x,
                y=scatter_y,
                mode="markers",
                name=f"{tolerance} Values",
                text=scatter_mpn,  # Add MPN as text
                hovertemplate=(
                    "Capacitance: %{x}<br>MPN: %{text}<extra></extra>"
                ),
            ),
        )

    # Update layout with new ranges
    figure.update_layout(
        xaxis_range=[x_min - 0.5, x_max + 0.5],
        yaxis_range=[0, y_max],
        yaxis_autorange=False,
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "xanchor": "center",
            "y": -0.5,
            "x": 0.5,
        },
    )

    # Define theme settings
    theme = {
        "template": "plotly" if theme_switch else "plotly_dark",
        "paper_bgcolor": "white" if theme_switch else "#222222",
        "plot_bgcolor": "white" if theme_switch else "#222222",
        "font_color": "black" if theme_switch else "white",
        "margin": {"l": 0, "r": 0, "t": 50, "b": 50},
    }

    # Update figure layout with theme and remove unnecessary modebar options
    figure.update_layout(
        **theme,
        barmode="stack",
        bargap=0.0,
        bargroupgap=0.05,
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
