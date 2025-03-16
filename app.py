"""Main application module for a Dash web application.

This module implements a Dash web application with theme switching
capabilities and dynamic page navigation.
It uses Dash Bootstrap Components for styling and implements a dark/light
theme switcher.

Features:
    - Multi-page functionality with dynamic content loading
    - Theme switching between light (Cerulean) and dark (Darkly) themes
    - Automatic page link generation with item counts
    - Environment variable configuration for port settings

Environment Variables:
    PORT (int): The port number on which to run the server (default: 8050)
"""

import importlib
import os
from typing import Optional

import dash
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, callback, dcc, html
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import ThemeSwitchAIO


def get_page_count(module_path: str) -> Optional[int]:  # noqa: FA100
    """Retrieve the number of items in a page's dataframe.

    Dynamically imports the specified module and attempts to access its
    dataframe attribute to count the number of items.

    Args:
        module_path (str): The dot-notation path to the module to import

    Returns:
        Optional[int]:
            The number of items in the dataframe if found, None otherwise

    """
    try:
        module = importlib.import_module(module_path)
        if hasattr(module, "dataframe"):
            return len(module.dataframe)
    except (ImportError, AttributeError):
        pass
    return None


# Initialize Dash application with multi-page support
app = Dash(__name__, use_pages=True)
server = app.server

# Define application layout
app.layout = dbc.Container([
    html.Div([
        dbc.Row([
            ThemeSwitchAIO(
                aio_id="theme",
                themes=[dbc.themes.CERULEAN, dbc.themes.DARKLY],
                switch_props={"persistence": False, "value": 0}),
        ]),
    ], id="theme_switch", style={"display": ""}),

    dcc.Store(id="theme_switch_value_store", data=[]),

    # Interval component for initial load
    dcc.Interval(id="interval_component", interval=1*100, max_intervals=1),

    # Store component for navigation links
    dcc.Store(id="links_store"),

    dash.page_container,
], fluid=True)


@app.callback(
    Output("theme_switch_value_store", "data"),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
)
def update_graph_theme(
    switch: bool,  # noqa: FBT001
) -> bool:
    """Update the application theme based on the theme switch value.

    Args:
        switch (bool):
            The current state of the theme switch
            (True for dark theme, False for light theme)

    Returns:
        bool: The same switch value, stored for persistence

    """
    return switch


@callback(
    Output("links_store", "data"),
    Input("interval_component", "n_intervals"),
)
def update_links_store(
    interval_component: Optional[int],  # noqa: FA100
) -> list[dict[str, str]]:
    """Generate and update the navigation links with item counts.

    This callback is triggered once on initial load and creates a list of
    navigation links for all registered pages. If a page has a dataframe,
    the number of items is appended to the page name.

    Args:
        interval_component (Optional[int]):
            The number of intervals elapsed (used for triggering only)

    Returns:
        List[Dict[str, str]]:
            A list of dictionaries containing page names and their paths

    Raises:
        PreventUpdate: If the callback is triggered with no intervals

    """
    if interval_component is None:
        raise PreventUpdate

    links = []
    for page in dash.page_registry.values():
        name = page["name"]
        module_path = page.get("module", "")

        if module_path:
            count = get_page_count(module_path)
            if count is not None:
                name = f"{name} ({count:,} items)"

        links.append({
            "name": name,
            "path": page["relative_path"],
        })

    return links


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run_server(
        port=port,
        debug=True,
        dev_tools_ui=True,
        dev_tools_props_check=True,
    )
