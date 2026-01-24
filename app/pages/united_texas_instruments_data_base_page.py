"""Dash page module for the IC Texas Instruments database interface.

This module provides an interactive web interface for exploring and filtering
IC Texas Instruments specifications. It includes features such as:
- Dynamic data table with sorting and filtering
- Customizable column visibility
- Adjustable pagination
- Direct links to device datasheets
- Responsive theme support
"""

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pages.utils.dash_component_utils as dcu
import pages.utils.style_utils as styles
import pandas as pd
from dash import dcc, html, register_page

link_name = __name__.rsplit(".", maxsplit=1)[-1].replace("_page", "").title()
module_name = __name__.rsplit(".", maxsplit=1)[-1]

register_page(__name__, name=link_name, order=18)

ag_grid_data: pd.DataFrame = pd.read_csv("data/UNITED_IC_TI.csv")
total_rows = len(ag_grid_data)

TITLE = (
    f"Texas Instruments Integrated Circuits Database ({total_rows:,} items)"
)
ABOUT = (
    "The Texas Instruments IC Database is an interactive web application "
    "that provides a comprehensive view of Texas Instruments "
    "integrated circuits and their specifications. ",
    "It allows users to easily browse, search, and filter "
    f"through a database of {total_rows:,} integrated circuits, "
    "providing quick access to detailed specifications, parameters, "
    "and official datasheets.",
)

features = [
    "Interactive data table displaying comprehensive IC specifications and "
    "parameters",
    "Dynamic filtering and multi-column sorting for rapid device selection",
    "Customizable pagination with adjustable items per page",
    "Direct links to official ADI datasheets and documentation",
    "Responsive design adapting to light and dark themes",
    "Advanced search functionality for finding specific IC models and "
    "parameters",
    "Customizable column visibility for focused device comparison",
]

usage_steps = [
    "Navigate to the Texas Instruments IC Database page",
    "Use the table's built-in search functionality "
    "to find specific ICs by existing parameters",
    "Click on column headers to sort devices by specifications",
    "Use the filter action to narrow down devices based on multiple criteria",
    "Toggle column visibility to focus on relevant "
    "specifications for your application",
    "Adjust the number of items per page using the dropdown menu",
    "Navigate through pages using the pagination "
    "controls at the bottom of the table",
    "Access detailed device information and specifications "
    "through the provided datasheet",
    "Switch between light and dark themes for comfortable "
    "viewing in different environments",
]

hidden_columns = []

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
                dcu.ag_grid_table_controls_row(
                    module_name,
                    ag_grid_data,
                    visible_columns,
                ),
                dag.AgGrid(
                    id=f"{module_name}_ag_grid_table",
                    rowData=ag_grid_data.to_dict("records"),
                    defaultColDef={"filter": True},
                    style={"height": 200},
                ),
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
