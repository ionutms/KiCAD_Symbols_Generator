"""United Seven Segment Displays Database Page.

This module contains the layout and interactivity for the United Seven Segment
Displays Database page of the Dash web application. It provides an interactive
table displaying seven segment display specifications and a bar graph showing
the distribution of display types.

Attributes:
    link_name (str): The name of the page link.
    module_name (str): The name of the module.
    dataframe (pd.DataFrame): The seven segment display data.
    total_rows (int):
        The total number of seven segment displays in the database.
    TITLE (str): The title of the page.
    ABOUT (tuple[str, str]): Information about the page.
    features (list[str]): Key features of the page.
    usage_steps (list[str]): Steps for using the page.
    hidden_columns (list[str]): Columns to hide in the table.
    visible_columns (list[str]): Columns to display in the table.

"""

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pages.utils.dash_component_utils as dcu
import pages.utils.style_utils as styles
import pandas as pd
from dash import dcc, html, register_page

link_name = __name__.rsplit(".", maxsplit=1)[-1].replace("_page", "").title()
module_name = __name__.rsplit(".", maxsplit=1)[-1]

register_page(__name__, name=link_name, order=17)

ag_grid_data: pd.DataFrame = pd.read_csv(
    "data/UNITED_SEVEN_SEGM_DISPLAYS_DATA_BASE.csv"
)
total_rows = len(ag_grid_data)

TITLE = f"Seven Segment Displays Database ({total_rows:,} items)"
ABOUT = (
    "The Seven Segment Displays Database is an interactive web application "
    "that provides a comprehensive view of seven segment display "
    "specifications.",
    "It allows users to easily browse, search, and filter "
    f"through a database of {total_rows:,} seven segment displays, "
    "providing quick access to important information and datasheets.",
)

features = [
    "Interactive data table displaying seven segment display specifications",
    "Dynamic filtering and multi-column sorting capabilities",
    "Customizable pagination with adjustable items per page",
    "Direct links to seven segment display datasheets",
    "Responsive design adapting to light and dark themes",
    "Easy-to-use interface for exploring seven segment display data",
    "Customizable column visibility",
]

usage_steps = [
    "Navigate to the Seven Segment Displays Database page",
    "Use the table's built-in search functionality to find specific displays",
    "Click on column headers to sort the data",
    "Use the filter action to narrow down the displayed results",
    "Toggle column visibility using the checkboxes above the table",
    "Adjust the number of items per page using the dropdown menu",
    "Navigate through pages using the pagination controls at "
    "the bottom of the table",
    "Access display datasheets by clicking on the provided links in the "
    "'Datasheet' column",
    "Switch between light and dark themes for comfortable viewing in "
    "different environments",
]

hidden_columns = [
    "Reference",
    "Symbol Name",
    "Footprint",
    "Series",
    "Trustedparts Search",
    "Pitch (mm)",
    "Mounting Angle",
    "Current Rating (A)",
    "Voltage Rating (V)",
    "Mounting Style",
    "Number of Rows",
]

visible_columns = [
    col for col in ag_grid_data.columns if col not in hidden_columns
]

# Convert specific columns to markdown format links for AG Grid
url_columns = ["Datasheet", "Trustedparts Search"]

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
                html.Hr(),
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
