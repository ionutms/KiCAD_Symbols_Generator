"""Dash page module for the IC Texas Instruments database interface.

This module provides an interactive web interface for exploring and filtering
IC Texas Instruments specifications. It includes features such as:
- Dynamic data table with sorting and filtering
- Customizable column visibility
- Adjustable pagination
- Direct links to device datasheets
- Responsive theme support
"""

import dash_bootstrap_components as dbc
import pandas as pd
from dash import dash_table, dcc, html, register_page

import pages.utils.dash_component_utils as dcu
import pages.utils.style_utils as styles

link_name = __name__.rsplit(".", maxsplit=1)[-1].replace("_page", "").title()
module_name = __name__.rsplit(".", maxsplit=1)[-1]

register_page(__name__, name=link_name, order=15)

dataframe: pd.DataFrame = pd.read_csv("data/UNITED_IC_TI.csv")
total_rows = len(dataframe)

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
    col for col in dataframe.columns if col not in hidden_columns
]

try:
    dataframe["Datasheet"] = dataframe["Datasheet"].apply(
        lambda url_text: dcu.generate_centered_link(url_text, "Datasheet"),
    )

    dataframe["Trustedparts Search"] = dataframe["Trustedparts Search"].apply(
        lambda url_text: dcu.generate_centered_link(url_text, "Search"),
    )
except KeyError:
    pass

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
                dcu.table_controls_row(
                    module_name,
                    dataframe,
                    visible_columns,
                ),
                dash_table.DataTable(
                    id=f"{module_name}_table",
                    columns=dcu.create_column_definitions(
                        dataframe,
                        visible_columns,
                    ),
                    data=dataframe[visible_columns].to_dict("records"),
                    cell_selectable=False,
                    markdown_options={"html": True},
                    page_size=10,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                ),
            ],
            style=styles.GLOBAL_STYLE,
        ),
    ],
    fluid=True,
)


dcu.callback_update_visible_columns(
    f"{module_name}_table",
    f"{module_name}_column_toggle",
    dataframe,
)


dcu.callback_update_table_style_and_visibility(f"{module_name}_table")

dcu.callback_update_page_size(
    f"{module_name}_table",
    f"{module_name}_page_size",
)

dcu.callback_update_dropdown_style(f"{module_name}_page_size")
