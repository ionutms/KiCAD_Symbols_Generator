"""Mechanical Database Page.

This module provides a Dash page for viewing and interacting with mechanical
specifications. It allows users to browse, search, and filter through a
database of mechanical, with features for customizing the view and
accessing detailed information.

Key features:
- Interactive DataTable displaying mechanical specifications
- Column visibility controls for customizing the view
- Dynamic filtering and multi-column sorting capabilities
- Pagination with customizable page size
- Theme-aware styling with light/dark mode support
- Direct links to mechanical datasheets
- Responsive design for various screen sizes

The module uses Dash components and callbacks to create an interactive
interface for data visualization and exploration. It integrates with
Bootstrap components for a polished user interface and includes
comprehensive styling support for both light and dark themes.
"""

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pages.utils.dash_component_utils as dcu
import pages.utils.style_utils as styles
import pandas as pd
from dash import dcc, html, register_page

link_name = __name__.rsplit(".", maxsplit=1)[-1].replace("_page", "").title()
module_name = __name__.rsplit(".", maxsplit=1)[-1]

register_page(__name__, name=link_name, order=10)

ag_grid_data: pd.DataFrame = pd.read_csv(
    "data/UNITED_MECHANICAL_DATA_BASE.csv"
)
total_rows = len(ag_grid_data)

TITLE = f"Mechanical Database ({total_rows:,} items)"
ABOUT = (
    "The mechanical Database is an interactive web application that "
    "provides a comprehensive view of inductor specifications.",
    "It allows users to easily browse, search, and filter "
    f"through a database of {total_rows:,} mechanical, "
    "providing quick access to important information and datasheets.",
)

features = [
    "Interactive data table displaying inductor specifications",
    "Dynamic filtering and multi-column sorting capabilities",
    "Customizable pagination with adjustable items per page",
    "Direct links to inductor datasheets",
    "Responsive design adapting to light and dark themes",
    "Easy-to-use interface for exploring inductor data",
    "Customizable column visibility",
]

usage_steps = [
    "Navigate to the Mechanical Database page",
    "Use the table's built-in search functionality to find specific "
    "mechanical",
    "Click on column headers to sort the data",
    "Use the filter action to narrow down the displayed results",
    "Toggle column visibility using the checkboxes above the table",
    "Adjust the number of items per page using the dropdown menu",
    "Navigate through pages using the pagination controls at "
    "the bottom of the table",
    "Access inductor datasheets by clicking on the provided links in the "
    "'Datasheet' column",
    "Switch between light and dark themes for comfortable viewing in "
    "different environments",
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
