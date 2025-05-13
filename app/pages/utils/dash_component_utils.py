"""Dash Component Utilities

This module contains utility functions for creating and managing
Dash components, particularly for tables and their styling.
"""

from typing import Any

import dash_bootstrap_components as dbc
import pages.utils.style_utils as styles
import pandas as pd
from dash import callback, dcc, html
from dash.dependencies import Input, Output, State


def app_description(
    title: str,
    about: tuple[str],
    features: tuple[str],
    usage_steps: tuple[str],
) -> html.Div:
    """Create a description component for any app page.

    Args:
        title (str): The title of the page.
        about (Tuple[str]): A brief description of the page's purpose.
        features (Tuple[str]): A tuple of key features of the page.
        usage_steps (Tuple[str]):
            A tuple of steps describing how to use the page.

    Returns:
        html.Div: A Div component containing the formatted app description.

    """
    left_column_content: dbc.Col = dbc.Col(
        [
            html.H4("Key Features:"),
            html.Ul([html.Li(feature) for feature in features]),
        ],
        xs=12,
        md=6,
    )

    right_column_content: dbc.Col = dbc.Col(
        [
            html.H4("How to Use:"),
            html.Ol([html.Li(step) for step in usage_steps]),
        ],
        xs=12,
        md=6,
    )

    description: html.Div = html.Div([
        html.Hr(),
        html.H3(f"About the {title}"),
        *[html.Div(content) for content in about],
        html.Hr(),
        dbc.Row([left_column_content, right_column_content]),
        html.Hr(),
    ])
    return description


def callback_update_table_style_and_visibility(
    table_id: str,
) -> None:
    """Create a callback function to update DataTable styles based on theme.

    This is a factory function that generates a callback for updating the
    visual styles of a Dash DataTable component in response to theme changes.
    The callback updates multiple style properties to ensure consistent
    theming across the table's various elements.

    The generated callback will:
    - Update data cell styles based on theme
    - Update header styles based on theme
    - Apply conditional styles for alternating rows
    - Set theme-independent table layout properties
    - Configure cell styling properties
    - Update filter row styling
    - Apply theme-specific CSS rules

    Args:
        table_id (str): The ID of the DataTable component for which to create
            the callback. This ID will be used to target the specific table's
            style properties.

    Returns:
        None:
            This function registers a callback with Dash and
            doesn't return a value directly.

    """

    @callback(
        Output(table_id, "style_data"),
        Output(table_id, "style_header"),
        Output(table_id, "style_data_conditional"),
        Output(table_id, "style_table"),
        Output(table_id, "style_cell"),
        Output(table_id, "style_filter"),
        Output(table_id, "css"),
        Input("theme_switch_value_store", "data"),
    )
    def update_table_style_and_visibility(
        switch: bool,  # noqa: FBT001
    ) -> tuple[
        dict[str, str],
        dict[str, str],
        list[dict[str, str]],
        dict[str, str],
        dict[str, str],
        dict[str, str],
        list[dict[str, str]],
    ]:
        """Update the styles of the DataTable based on the theme switch value.

        Args:
            switch: The state of the theme switch. True for light theme, False
                for dark theme.

        Returns:
            A tuple containing seven style-related elements:
                1. Style for data cells (dict[str, str])
                2. Style for header cells (dict[str, str])
                3. Conditional styles for alternating rows
                    (list[dict[str, str]])
                4. Table style (dict[str, str])
                5. Cell style (dict[str, str])
                6. Filter row style (dict[str, str])
                7. CSS rules (list[dict[str, str]])

        """
        return (
            styles.generate_style_data(switch),
            styles.generate_style_header(switch),
            styles.generate_style_data_conditional(switch),
            styles.generate_style_table(),
            styles.generate_style_cell(),
            styles.generate_style_filter(switch),
            styles.generate_css(switch),
        )


def callback_update_ag_grid_table_theme(
    table_id: str,
) -> None:
    """Create a callback function to update AG Grid table theme.

    This is a factory function that generates a callback for updating the
    visual theme of an AG Grid table component in response to theme changes.

    Args:
        table_id (str):
            The ID of the AG Grid table component for which to create
            the callback. This ID will be used to target the specific table's
            style properties.

    Returns:
        None:
            This function registers a callback with Dash and
            doesn't return a value directly.

    """

    @callback(
        Output(table_id, "className"),
        Input("theme_switch_value_store", "data"),
    )
    def update_table_style_and_visibility(
        switch: bool,  # noqa: FBT001
    ) -> str:
        """Update the styles of the AG Grid table based on the theme switch.

        Args:
            switch: The state of the theme switch. True for light theme, False
                for dark theme.

        Returns:
            A string representing the class name for the AG Grid table theme.
            This will be either "ag-theme-quartz" or "ag-theme-quartz-dark"
            depending on the value of the switch.

        """
        if switch:
            return "ag-theme-quartz"
        return "ag-theme-quartz-dark"


def callback_update_visible_columns(
    table_id: str,
    checklist_id: str,
    dataframe: pd.DataFrame,
) -> None:
    """Create a callback function to update DataTable columns visibility.

    This is a factory function that generates a callback for managing visible
    columns in a Dash DataTable component. The callback responds to changes in
    a checklist component that controls column visibility.

    The generated callback will:
    - Filter column definitions based on selected visibility options
    - Update the table data to include only visible columns
    - Update the DataTable component with new column definitions and data

    Args:
        table_id (str):
            The ID of the DataTable component to update.
            This ID will be used to target the table's columns and
            data properties.
        checklist_id (str):
            The ID of the Checklist component that controls column visibility.
            This component should have column names as its options.
        dataframe (pd.DataFrame):
            The source DataFrame containing all possible columns and data.
            Used to filter and format data based on selected columns.

    Returns:
        None:
            This function registers a callback with Dash and doesn't return
            a value directly.

    """

    @callback(
        Output(table_id, "columns"),
        Output(table_id, "data"),
        Input(checklist_id, "value"),
    )
    def update_visible_columns(visible_columns: list) -> list:
        """Update the visible columns based on the checklist selection.

        Args:
            visible_columns:
                list of column names that should be displayed in the table.

        Returns:
            A tuple containing:
                - list of column definitions for the visible columns
                - list of dictionaries containing the filtered data records

        """
        columns = create_column_definitions(dataframe, visible_columns)
        filtered_data = dataframe[visible_columns].to_dict("records")
        return columns, filtered_data


def callback_update_ag_grid_visible_table_columns(
    table_id: str,
    checklist_id: str,
    dataframe: pd.DataFrame,
    url_columns: list[str],
) -> None:
    """Create a callback function to update AG Grid table columns visibility.

    This is a factory function that generates a callback for managing visible
    columns in a Dash AG Grid component. The callback responds to changes in
    a checklist component that controls column visibility.

    The generated callback will:
    - Filter column definitions based on selected visibility options
    - Update the table data to include only visible columns

    Args:
        table_id (str):
            The ID of the AG Grid table component to update.
            This ID will be used to target the table's columns and
            data properties.
        checklist_id (str):
            The ID of the Checklist component that controls column visibility.
            This component should have column names as its options.
        dataframe (pd.DataFrame):
            The source DataFrame containing all possible columns and data.
            Used to filter and format data based on selected columns.

    Returns:
        None:
            This function registers a callback with Dash and doesn't return

    """

    @callback(
        Output(table_id, "columnDefs"),
        Output(table_id, "dashGridOptions"),
        Input(checklist_id, "value"),
    )
    def update_visible_columns(visible_columns: list) -> list:
        """Update the visible columns based on the checklist selection.

        Args:
            visible_columns:
                list of column names that should be displayed in the table.

        Returns:
            A list of dictionaries containing the column definitions for
            the visible columns.

        """
        dashGridOptions = {
            "pagination": True,
            "paginationPageSize": 10,
            "paginationAutoPageSize": False,
            "paginationPageSizeSelector": [5, 10, 25, 50, 100],
            "domLayout": "autoHeight",
            "enableCellTextSelection": True,
            "columnSize": "autoSize",
            "autoSizeStrategy": {"type": "fitCellContents"},
            "resizable": True,
            "suppressColumnVirtualisation": True,
            "animateRows": False,
        }

        columnDefs = []
        for col in dataframe.columns:
            col_def = {"field": col, "headerName": col}
            if col in url_columns:
                col_def.update({
                    "cellRenderer": "markdown",
                    "cellStyle": {"textAlign": "center"},
                })
            columnDefs.append(col_def)

        filtered_list = [
            item
            for item in columnDefs
            if item.get("field") in visible_columns
        ]
        return (filtered_list, dashGridOptions)

    @callback(
        Output(table_id, "columnSize"),
        Input(table_id, "columnDefs"),
    )
    def update_column_size(_column_defs: list) -> str:
        """Update the column size of the AG Grid table.

        Args:
            _column_defs:
                The column definitions of the AG Grid table.
                This is used to trigger the callback.

        Returns:
            A string representing the column size of the AG Grid table.

        """
        return "autoSize"


def create_column_definitions(
    dataframe: pd.DataFrame,
    visible_columns: list[str] = None,  # noqa: RUF013
) -> list[dict[str, Any]]:
    """Create column definitions for the Dash DataTable.

    Generates a list of column specifications for the DataTable component,
    with support for selective column visibility and special handling for
    datasheet links.

    Args:
        dataframe: The pandas DataFrame containing the resistor data.
        visible_columns:
            Optional list of column names to include in the table.
            If None, all columns will be visible.

    Returns:
        A list of dictionaries, each containing the configuration for a
        single column. Each dictionary includes:
            - name:
                The display name of the column (with newlines for wrapping)
            - id: The column identifier matching the DataFrame column name
            - presentation:
                The column's display type (markdown for datasheet links)

    """
    if visible_columns is None:
        visible_columns = dataframe.columns.tolist()

    return [
        {
            "name": "\n".join(column.split()),
            "id": column,
            "presentation": "markdown"
            if column in ["Datasheet", "Trustedparts Search", "3dviewer Link"]
            else "input",
        }
        for column in dataframe.columns
        if column in visible_columns
    ]


def generate_centered_link(
    url_text: str,
    link_text: str = "Link",
) -> str:
    """Generate a centered HTML link with consistent styling.

    Creates an HTML div containing a centered link for the datasheet URLs.
    Returns an empty string for null/NaN values to handle missing links
    gracefully.

    Args:
        url_text:
            The URL to convert into a centered link. Can be any type,
            as the function handles null/NaN values.
        link_text:
            The text to display for the link. Defaults to "Link".

    Returns:
        A string containing HTML for a centered link, or an empty string if
        the input is null/NaN.

    """
    if pd.notna(url_text):
        return (
            f'<div style="width:100%;text-align:center;">'
            f'<a href="{url_text}" target="_blank" '
            f'style="display:inline-block;">{link_text}</a></div>'
        )
    return ""


def callback_update_page_size(
    table_id: str,
    dropdown_id: str,
) -> None:
    """Create a callback function to update DataTable page size.

    This is a factory function that generates a callback for managing the
    number of items displayed per page in a Dash DataTable component.

    Args:
        table_id (str): The ID of the DataTable component to update.
        dropdown_id (str): The ID of the Dropdown component that controls
            page size.

    Returns:
        None: This function registers a callback with Dash and doesn't
            return a value directly.

    """

    @callback(
        Output(table_id, "page_size"),
        Input(dropdown_id, "value"),
    )
    def update_page_size(page_size: int) -> int:
        """Update the number of items displayed per page.

        Args:
            page_size: The number of items to display per page.

        Returns:
            The selected page size value.

        """
        return page_size


def callback_update_dropdown_style(dropdown_id: str) -> None:
    """Create a callback function to update Dropdown styles based on theme.

    Args:
        dropdown_id (str): The ID of the Dropdown component to style.

    """

    @callback(
        Output(dropdown_id, "style"),
        Input("theme_switch_value_store", "data"),
    )
    def update_dropdown_style(switch: bool) -> dict:  # noqa: FBT001
        """Update the dropdown styling based on the theme.

        Args:
            switch: True for light theme, False for dark theme.

        Returns:
            Dictionary containing the dropdown styles.

        """
        base_style = {"width": "150px"}
        if not switch:
            return {
                **base_style,
                "backgroundColor": "#AAAAAA",
                "color": "#334455",
            }
        return base_style


def table_controls_row(
    module_name: str,
    dataframe: pd.DataFrame,
    visible_columns: list[str],
) -> dbc.Row:
    """Create a row of controls for a data table.

    This function generates a responsive row with two columns:
    1. A dropdown to select the number of items per page
    2. A checklist to show/hide columns in the table

    Args:
        module_name (str): A unique identifier prefix for component IDs.
        dataframe (pd.DataFrame):
            The source DataFrame to derive column options.
        visible_columns (Optional[List[str]], optional):
            Initial list of visible columns.
            Defaults to all columns if not provided.

    Returns:
        dbc.Row: A Dash Bootstrap Components row with table control elements.

    """
    # Use all columns if no visible columns are specified
    if visible_columns is None:
        visible_columns = list(dataframe.columns)

    col_left = dbc.Col(
        [
            html.Div(
                [
                    html.H6("Items per page:", className="mb-1"),
                    dcc.Dropdown(
                        id=f"{module_name}_page_size",
                        options=[
                            {"label": str(page_size), "value": page_size}
                            for page_size in [10, 25, 50, 100]
                        ],
                        value=10,
                        clearable=False,
                    ),
                    html.Br(),
                ],
                className="d-flex flex-column align-items-start",
            ),
        ],
        xs=12,
        sm=3,
        md=2,
    )

    col_right = dbc.Col(
        [
            html.Div([
                html.H6("Show/Hide Columns:", className="mb-1"),
                dbc.Checklist(
                    id=f"{module_name}_column_toggle",
                    options=[
                        {"label": " ".join(col.split()), "value": col}
                        for col in dataframe.columns
                    ],
                    value=visible_columns,
                    inline=True,
                    className="flex-wrap",
                ),
                html.Br(),
            ]),
        ],
        xs=12,
        sm=9,
        md=10,
    )

    return dbc.Row([col_left, col_right], className="mb-1")


def ag_grid_table_controls_row(
    module_name: str,
    dataframe: pd.DataFrame,
    visible_columns: list[str],
) -> dbc.Row:
    """Create a row of controls for a data table.

    This function generates a responsive row with two columns:
    1. A dropdown to select the number of items per page
    2. A checklist to show/hide columns in the table

    Args:
        module_name (str): A unique identifier prefix for component IDs.
        dataframe (pd.DataFrame):
            The source DataFrame to derive column options.
        visible_columns (Optional[List[str]], optional):
            Initial list of visible columns.
            Defaults to all columns if not provided.

    Returns:
        dbc.Row: A Dash Bootstrap Components row with table control elements.

    """
    # Use all columns if no visible columns are specified
    if visible_columns is None:
        visible_columns = list(dataframe.columns)

    col_right = dbc.Col(
        [
            html.Div([
                html.H6("Show/Hide Columns:", className="mb-1"),
                dbc.Checklist(
                    id=f"{module_name}_column_toggle",
                    options=[
                        {"label": " ".join(col.split()), "value": col}
                        for col in dataframe.columns
                    ],
                    value=visible_columns,
                    inline=True,
                    className="flex-wrap",
                ),
                html.Br(),
            ]),
        ],
    )

    return dbc.Row([col_right], className="mb-1")


def generate_range_slider(
    module_name: str,
    dataframe: pd.DataFrame,
    step: int = 50,
) -> dbc.Row:
    """Generate a Dash RangeSlider component for exploring DataFrame values.

    Creates a range slider with marks at regular intervals, allowing users
    to select and explore a subset of values from a DataFrame column.

    Args:
        module_name (str): Unique prefix for component IDs to avoid conflicts.
        dataframe (pd.DataFrame):
            Source DataFrame containing values to visualize.
        step (int, optional):
            Interval between slider marks. Defaults to 50.
            Controls the density of marks and initial range selection.

    Returns:
        dbc.Row: A Dash Bootstrap Row containing:
            - A dcc.Store component to persist slider state
            - A dcc.RangeSlider for value selection

    Raises:
        ValueError:
            If the DataFrame is empty or the 'Value' column is missing.

    Notes:
        - Marks are created at specified step intervals
            to prevent overcrowding
        - The slider covers the entire range of values
        - Initial selected range starts from the first value
            to the step-th index

    """
    # Validate input DataFrame
    if dataframe is None or dataframe.empty:
        msg = "Input DataFrame cannot be None or empty"
        raise ValueError(msg)

    if "Value" not in dataframe.columns:
        msg = "DataFrame must contain a 'Value' column"
        raise ValueError(msg)

    # Extract consecutive value groups (assuming this function exists)
    values, _ = extract_consecutive_value_groups(dataframe["Value"].to_list())

    # Validate values list
    if not values:
        msg = "No values found in the 'Value' column"
        raise ValueError(msg)

    # Create marks with specified step increments, avoiding duplicates
    marks: dict[int, float] = {}

    # Add intermediary marks at step increments
    for mark_index in range(0, len(values), step):
        marks[mark_index] = values[mark_index]

    # Always add the last value
    marks[len(values) - 1] = values[-1]

    return dbc.Row([
        dcc.Store(
            id=f"{module_name}_rangeslider_store",
            data=[0, step],
        ),
        dcc.RangeSlider(
            id=f"{module_name}_value_rangeslider",
            min=0,
            max=len(values) - 1,
            value=[0, step],
            marks=marks,
            step=step,
        ),
    ])


def extract_consecutive_value_groups(
    input_list: list,
) -> tuple[list, list]:
    """Extract unique consecutive values and their repetition counts.

    Processes a list to identify consecutive identical values, returning
    two separate lists: one with unique consecutive values and another
    with their respective repetition counts.

    Args:
        input_list: The input list to process.

    Returns:
        A tuple containing two lists:
        - First list: Unique consecutive values
        - Second list: Corresponding repetition counts

    """
    if not input_list:
        return [], []

    unique_counts = []
    current_value = input_list[0]
    current_count = 1

    for item in input_list[1:]:
        if item == current_value:
            current_count += 1
        else:
            unique_counts.append((current_value, current_count))
            current_value = item
            current_count = 1

    unique_counts.append((current_value, current_count))

    unique_values, counts = zip(*unique_counts)

    return list(unique_values), list(counts)


def pad_values_and_counts(
    values: list[Any],
    specific_values: list[Any],
    specific_counts: list[int],
) -> tuple[list[Any], list[int]]:
    """Pad values with their corresponding counts.

    This function takes a list of values and compares it with a list of
    specific values and their counts. For each value in the input list:
    - If the value exists in specific values, its corresponding count is used
    - If the value does not exist, it is added with a zero count

    Args:
        values: A list of values to be padded
        specific_values: A list of specific values with known counts
        specific_counts: A list of counts corresponding to specific_values

    Returns:
        A tuple containing two lists:
        - A list of padded values in the same order as the input values
        - A list of corresponding counts (with zero for missing values)

    """
    # Add missing values with zero count
    padded_specific_values = []
    padded_specific_counts = []

    for val in values:
        if val in specific_values:
            # If the value exists in specific values, use its count
            index = specific_values.index(val)
            padded_specific_values.append(val)
            padded_specific_counts.append(specific_counts[index])
        else:
            # If the value doesn't exist, add it with a zero count
            padded_specific_values.append(val)
            padded_specific_counts.append(0)

    return padded_specific_values, padded_specific_counts


def save_previous_slider_state_callback(
    rangeslider_id: str,
    rangeslider_store_id: str,
    step: int = 50,
) -> None:
    """Create a callback to manage range slider state.

    This callback ensures that when one end of the range slider is moved,
    the other end adjusts by a specified step size while maintaining the
    overall range width.

    Args:
        rangeslider_id (str): The ID of the range slider component.
        rangeslider_store_id (str): The ID of the data store for slider state.
        step (int, optional):
            The fixed step size for slider adjustments. Defaults to 50.

    Returns:
        dash.development.base_component.Callback: A Dash callback function.

    """

    @callback(
        Output(rangeslider_store_id, "data"),
        Output(rangeslider_id, "value"),
        Input(rangeslider_id, "value"),
        State(rangeslider_store_id, "data"),
        prevent_initial_call=True,
    )
    def save_previous_slider_state(
        current_value: list[int],
        stored_value: list[int],
    ) -> list[int]:
        """Adjust range slider values to maintain a consistent step size.

        When one end of the slider is moved, this function ensures the
        other end moves by the specified step size while preserving the
        relative positioning.

        Args:
            current_value (List[int]):
                Current values of the range slider. Expected to be a list
                of two integers representing the lower and upper bounds.
            stored_value (List[int], optional):
                Previous values of the range slider. Defaults to None.

        Returns:
            List[int]: Adjusted slider values with consistent step size.

        """
        # Use empty list as default if stored_value is None
        stored_value = stored_value or [0, 0]

        # If upper bound changed, adjust lower bound
        if current_value[1] != stored_value[1]:
            current_value[0] = current_value[1] - step

        # If lower bound changed, adjust upper bound
        if current_value[0] != stored_value[0]:
            current_value[1] = current_value[0] + step

        return current_value, current_value

    return save_previous_slider_state
