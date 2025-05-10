"""Test Points Database Page.

This module provides a Dash page for viewing and interacting with test
points specifications. It allows users to browse, search, and filter through
a database of test points, with features for customizing the view and
accessing detailed information.

Key features:
- Interactive DataTable displaying test points specifications
- Column visibility controls for customizing the view
- Dynamic filtering and multi-column sorting capabilities
- Pagination with customizable page size
- Theme-aware styling with light/dark mode support
- Direct links to test points datasheets
- Responsive design for various screen sizes

The module uses Dash components and callbacks to create an interactive
interface for data visualization and exploration. It integrates with
Bootstrap components for a polished user interface and includes
comprehensive styling support for both light and dark themes.
"""

import dash_bootstrap_components as dbc
import pages.utils.dash_component_utils as dcu
import pages.utils.style_utils as styles
import pandas as pd
from dash import dash_table, dcc, html, register_page

link_name = __name__.rsplit(".", maxsplit=1)[-1].replace("_page", "").title()
module_name = __name__.rsplit(".", maxsplit=1)[-1]

register_page(__name__, name=link_name, order=15)

dataframe: pd.DataFrame = pd.read_csv("data/UNITED_SOLDER_JUMPERS.csv")
total_rows = len(dataframe)

TITLE = f"Transistors Database ({total_rows:,} items)"
ABOUT = (
    "The test points Database is an interactive web application that "
    "provides a comprehensive view of inductor specifications.",
    "It allows users to easily browse, search, and filter "
    f"through a database of {total_rows:,} test points, "
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
    "Navigate to the test points Database page",
    "Use the table's built-in search functionality "
    "to find specific test points",
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
