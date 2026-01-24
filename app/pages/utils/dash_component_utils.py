"""Dash Component Utilities.

This module contains utility functions for creating and managing
Dash components, particularly for tables and their styling.
"""

from typing import Any, Callable

import dash_bootstrap_components as dbc
import pages.utils.signal_processing_utils as spu
import pages.utils.style_utils as styles
import pandas as pd
from dash import callback, ctx, dcc, html, no_update
from dash.dependencies import ALL, MATCH, Input, Output, State, Union
from dash.exceptions import PreventUpdate


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
        url_columns (list[str]):
            A list of column names that should be treated as URL links

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
            col_def = {
                "field": col,
                "headerName": col,
                "wrapText": True,
                "autoHeight": True,
                "maxWidth": 300,
                "cellClass": "centered-cell",
                "cellStyle": {
                    "white-space": "normal",
                    "line-height": "1.2em",
                    "padding": "15px",
                },
            }
            if col in url_columns:
                col_def.update({
                    "cellRenderer": "markdown",
                    "cellStyle": {
                        "textAlign": "center",
                        "white-space": "normal",
                        "line-height": "1.2em",
                        "padding": "15px",
                    },
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


def labeled_counter_trio(
    id_section: str,
    label: str,
    limits: dict[str, float],
    default_count: int = 1,
    md: int = 3,
) -> dbc.Col:
    """Create a labeled button group for changing a count.

    Args:
        id_section (str): Unique identifier for component IDs.
        label (str): Text to display above the button group.
        limits (dict[str, float]):
            Dictionary defining min and max limits for the counter.
        default_count (int, optional): Initial count value. Defaults to 1.
        max_count (int, optional):
            Maximum value for the counter. Defaults to 1.
        md (int, optional):
            Column width for medium and larger screens. Defaults to 3.

    Returns:
        dbc.Col:
            Bootstrap column containing the label and counter button group.

    """
    counter_button_group = dbc.Col(
        [
            dcc.Store(id=f"{id_section}_store", data=limits),
            dbc.Label(
                children=label,
                id=f"{id_section}_label",
                className=styles.CENTER_CLASS_NAME,
            ),
            dbc.ButtonGroup(
                [
                    dbc.Button(
                        "<",
                        id=f"{id_section}_decrement_button",
                        outline=False,
                        color="secondary",
                    ),
                    dbc.Button(
                        f"{default_count}",
                        id=f"{id_section}_button",
                        outline=False,
                        color="secondary",
                        disabled=True,
                    ),
                    dbc.Button(
                        ">",
                        id=f"{id_section}_increment_button",
                        outline=False,
                        color="secondary",
                    ),
                ],
                className="d-flex flex-wrap",
            ),
            html.Br(),
        ],
        xs=12,
        md=md,
    )
    return counter_button_group


def labeled_range_slider(
    id_section: str,
    label: str,
    default_value: list[int],
    min_value: int = 1,
    md=9,
) -> dbc.Col:
    """Create a labeled range slider column.

    Args:
        id_section (str): ID prefix for the range slider component.
        label (str): Label text to display above the range slider.
        default_value (List[int]):
            Default values for the range slider (two ints).
        min_value (int, optional):
            Minimum value for the range slider. Defaults to 1.
        md (int, optional):
            Column width for medium and larger screens. Defaults to 9.

    Returns:
        dbc.Col: Dash Bootstrap column containing the labeled range slider.

    """
    labeled_range_slider_column = dbc.Col(
        [
            dbc.Label(label, className=styles.CENTER_CLASS_NAME),
            dcc.RangeSlider(
                id=f"{id_section}_range_slider",
                min=min_value,
                value=default_value,
                pushable=1,
                step=1,
                marks=None,
                tooltip={
                    "placement": "topLeft",
                    "always_visible": False,
                    "style": {"fontSize": "12px"},
                },
            ),
            html.Br(),
        ],
        xs=12,
        md=md,
    )
    return labeled_range_slider_column


def labeled_counter_quintet(
    id_section: str,
    label: str,
    limits: dict[str, float],
    default_count: int = 1,
    md: int = 3,
) -> dbc.Col:
    """Create a labeled button group with five buttons for count manipulation.

    Args:
        id_section (str): Unique identifier for component IDs.
        label (str): Text to display above the button group.
        limits (Dict[str, float]):
            Dictionary containing min and max count limits.
        default_count (int, optional): Initial count value. Defaults to 1.
        md (int, optional):
            Column width for medium and larger screens. Defaults to 3.

    Returns:
        dbc.Col:
            Bootstrap column containing the label and counter button group.

    """
    counter_button_group = dbc.Col(
        [
            dcc.Store(id=f"{id_section}_store", data=limits),
            dbc.Label(
                children=label,
                id=f"{id_section}_label",
                className=styles.CENTER_CLASS_NAME,
            ),
            dbc.ButtonGroup(
                [
                    dbc.Button(
                        "<<",
                        id=f"{id_section}_divide_button",
                        outline=False,
                        color="secondary",
                    ),
                    dbc.Button(
                        "<",
                        id=f"{id_section}_decrement_button",
                        outline=False,
                        color="secondary",
                    ),
                    dbc.Button(
                        f"{default_count}",
                        id=f"{id_section}_button",
                        outline=False,
                        color="secondary",
                        disabled=True,
                    ),
                    dbc.Button(
                        ">",
                        id=f"{id_section}_increment_button",
                        outline=False,
                        color="secondary",
                    ),
                    dbc.Button(
                        ">>",
                        id=f"{id_section}_multiply_button",
                        outline=False,
                        color="secondary",
                    ),
                ],
                className="d-flex flex-wrap",
            ),
            html.Br(),
        ],
        xs=12,
        md=md,
    )
    return counter_button_group


def callback_update_store_at_upload(
    base_id: str,
    file_store_id: str,
    store_id: str,
    process: Callable,
    search_key: str | None = None,
) -> None:
    """Create a callback function to update a store.

    This function generates a callback that processes ZIP file uploads,
    extracts specific information based on the provided search key,
    and updates the corresponding store.

    Args:
        base_id (str): Base ID for the store component.
        file_store_id (str): ID of the file store component.
        store_id (str): ID of the main store component.
        process (Callable):
            Function to process the uploaded ZIP file.
        search_key (str | None, optional):
            Key to search for within the ZIP file.

    Returns:
        None. The function registers callbacks with the Dash app.

    """

    @callback(
        Output(f"{base_id}_store", "data", allow_duplicate=True),
        Output(f"{base_id}_range_slider", "marks", allow_duplicate=True),
        Input(f"{file_store_id}", "data"),
        State(f"{store_id}", "data"),
        State(f"{base_id}_store", "data"),
        prevent_initial_call=True,
    )
    def update_count_from_zip(
        contents: str,
        global_store: dict[str, Any],
        store: dict[str, Any],
    ) -> dict[str, Any]:
        """Update the store with information extracted.

        This callback function processes ZIP file uploads, extracting specific
        information based on the search_key and updating the store
        accordingly.

        Args:
            contents (str): Base64 encoded contents of the uploaded file.
            global_store (Dict[str, Any]):
                Global store containing additional context.
            store (Dict[str, Any]): Current state of the store.

        Returns:
            Dict[str, Any]:
                Updated store with new information extracted.

        Raises:
            PreventUpdate: If the uploaded file is not a ZIP file.

        """
        if contents["filename"].lower().endswith(".zip"):
            if process.__name__ == "extract_info_from_zip_as_int":
                store["max_count"] = process(
                    contents["content"], contents["filename"], search_key
                )
                return store, None
            if process.__name__ == "count_csv_files_from_zip":
                store["max_count"] = process(contents["content"])
                return store, None
            if process.__name__ == "extract_data_frame_from_zip_contents":
                names = process(
                    contents["content"], contents["filename"], global_store
                )
                store["max_count"] = len(names)
                marks = dict(enumerate(names, 1))
                return store, marks
        return no_update, no_update


def extract_info_from_zip_as_int(
    contents: str,
    file_name: str,
    search_key: str,
) -> int:
    """Extract information from a ZIP file and return it as an integer.

    This function uses the `extract_info_from_zip` function to extract
    information based on a given search key from a ZIP file's contents.
    It then converts the first extracted value to an integer.

    Args:
        contents (str): Base64 encoded string of the ZIP file contents.
        file_name (str): The name of the uploaded ZIP file.
        search_key (str): The key to search for in the ZIP file's CSV
        contents.

    Returns:
        int: The first extracted value converted to an integer.

    Raises:
        ValueError: If the extracted value cannot be converted to an integer.
        IndexError: If no value is found for the given search key.

    Note:
        This function assumes that the `extract_info_from_zip` function
        returnsa dictionary where values are either strings or lists of
        strings.

    """
    if file_name.lower().endswith(".zip"):
        return int(
            next(
                iter(
                    spu.extract_info_from_zip(contents, [search_key]).values()
                )
            )
        )
    return no_update


def callbacks_radioitems(id_section: str, row_id: str) -> None:
    """Generate callbacks for radio items in a section.

    This function sets up three callback functions for handling radio items
    in a specific section of a Dash application. The callbacks are registered
    with the Dash app and do not need to be returned.

    Args:
        id_section: The ID of the section.
        row_id: The ID of the row.

    Returns:
        None. The function registers callbacks with the Dash app.

    """

    @callback(
        Output(row_id, "children"),
        Input(f"{id_section}_range_slider", "value"),
        State(f"{id_section}_range_slider", "marks"),
        prevent_initial_call=True,
    )
    def generate_radioitems(
        values: list[int], marks: dict[str, str]
    ) -> list[dbc.Col]:
        """Generate radio items based on range slider values.

        Args:
            values: The selected values from the range slider.
            marks: The marks on the range slider.

        Returns:
            A list of Column components containing radio items.

        """
        if values is None:
            raise PreventUpdate

        columns = []
        y_axis_channels = [marks[f"{position}"] for position in values[1:]]
        options = [
            {"label": f"y{index}" if index > 1 else "y", "value": index}
            for index, _ in enumerate(y_axis_channels, 1)
        ]

        for index, y_axis_data in enumerate(y_axis_channels[1:], 1):
            columns.append(
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.Row([
                                    dbc.Col(
                                        [
                                            dbc.Label(
                                                f"{y_axis_data} "
                                                "axis selection",
                                                id={
                                                    "type": "label selection",
                                                    "index": index,
                                                },
                                                className=styles.CENTER_CLASS_NAME,
                                            ),
                                            dbc.RadioItems(
                                                options=options,
                                                value=options[0]["value"],
                                                id={
                                                    "type": "radioitems",
                                                    "index": index,
                                                },
                                                className=styles.CENTER_CLASS_NAME,
                                                inline=True,
                                            ),
                                        ],
                                        xs=10,
                                        md=10,
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Label(
                                                "Left",
                                                id={
                                                    "type": "label side",
                                                    "index": index,
                                                },
                                            ),
                                            dbc.Switch(
                                                id={
                                                    "type": "switch",
                                                    "index": index,
                                                },
                                                value=False,
                                                className=(
                                                    "d-flex "
                                                    "justify-content-center"
                                                ),
                                            ),
                                        ],
                                        xs=2,
                                        md=2,
                                        className=styles.FLEX_CENTER_COLUMN,
                                    ),
                                ])
                            ],
                            body=True,
                            style={
                                "border": "1px dashed",
                                "border-radius": "10px",
                                "padding": "1px",
                                "background-color": "transparent",
                            },
                        ),
                        html.Br(),
                    ],
                    xs=12,
                    md=4,
                )
            )

        return columns

    @callback(
        Output("filtering_store", "data", allow_duplicate=True),
        Input("legend_group_switch", "value"),
        Input("filtering_store", "data"),
        prevent_initial_call=True,
    )
    def update_filtering_store_2(
        legend_group_switch: bool, filtering: dict[str, Any]
    ) -> dict[str, Any]:
        """Update the filtering store with the legend group switch state.

        This function adds or updates the 'legend_group' key in the filtering
        dictionary based on the state of the legend group switch.

        Args:
            legend_group_switch (bool): The state of the legend group switch.
            filtering (Dict[str, Any]): The current filtering dictionary.

        Returns:
            Dict[str, Any]: The updated filtering dictionary.

        Note:
            If filtering is None or not a dictionary, an empty dictionary
            is returned with only the 'legend_group' key.

        """
        if not isinstance(filtering, dict):
            return {"legend_group": legend_group_switch}

        filtering["legend_group"] = legend_group_switch
        return filtering

    @callback(
        Output("filtering_store", "data", allow_duplicate=True),
        Output({"type": "switch", "index": ALL}, "value"),
        Input({"type": "radioitems", "index": ALL}, "value"),
        Input({"type": "switch", "index": ALL}, "value"),
        Input("filtering_store", "data"),
        prevent_initial_call=True,
    )
    def update_filtering_store(
        radioitems_values: list[int],
        switch: list[bool],
        filtering: dict[str, Any],
    ) -> dict[str, Any]:
        """Update the filtering store based on radio item selections.

        Args:
            radioitems_values: The selected values from the radio items.
            switch: The current states of the switches.
            filtering: The current filtering data.

        Returns:
            The updated filtering data.

        """
        try:
            selection = {}
            for index, key in enumerate(filtering["y_axis_data"][1:]):
                selection[key] = (
                    f"y{radioitems_values[index]}"
                    if radioitems_values[index] > 1
                    else "y"
                )
            filtering.update({"y_axis_selection": selection})

            def update_list(original_list):
                value_states = {}

                for value, state in original_list:
                    if value not in value_states:
                        value_states[value] = state

                result = [
                    (value, value_states[value]) for value, _ in original_list
                ]

                return result

            for index, item in enumerate(radioitems_values):
                if item == 1:
                    switch[index] = False
                if item > 1:
                    unzipped = list(
                        zip(
                            *update_list(list(zip(radioitems_values, switch)))
                        )
                    )
                    switch = [list(state) for state in unzipped][1]

            side = {}
            for index, key in enumerate(filtering["y_axis_data"][1:]):
                side[key] = switch[index]
            filtering.update({"y_axis_side": side})

            return filtering, switch
        except (KeyError, IndexError):
            return filtering, no_update

    @callback(
        Output({"type": "label side", "index": MATCH}, "children"),
        Input({"type": "switch", "index": MATCH}, "value"),
        prevent_initial_call=True,
    )
    def update_side_label(switch: bool) -> str:
        """Update the side label based on the switch value.

        Args:
            switch: The current state of the switch (True/False).

        Returns:
            The updated label text ('Right' or 'Left').

        """
        return "Right" if switch else "Left"


def callback_update_range_slider_max_and_label(
    base_id: str, upload_id: str, reset_value: int = 1
) -> None:
    """Generate Dash callbacks to update range slider max value and label.

    This function sets up three callback functions for handling updates to
    range slider, label, and style based on file uploads and data changes.

    Args:
        base_id: Base ID for the related Dash components.
        upload_id: ID of the upload component.
        reset_value: Value to reset the counter to on upload (default: 1).

    Returns:
        None. The function registers callbacks with the Dash app.

    """

    @callback(
        Output(f"{base_id}_label", "children"),
        Output(f"{base_id}_range_slider", "max"),
        Input(f"{base_id}_store", "data"),
        State(f"{base_id}_label", "children"),
        prevent_initial_call=True,
    )
    def update_range_slider_max_and_label(
        store: dict[str, Any], label: str
    ) -> tuple[str, int]:
        """Update UI components based on the number of detected files.

        Args:
            store: A dictionary containing the count of detected files.
            label: The current label text for detected files.

        Returns:
            A tuple containing the updated label text and new max slider
            value.

        """
        try:
            new_label = label.replace(
                label.split(" ")[0], str(store["max_count"])
            )
            return new_label, store["max_count"]
        except KeyError:
            return label, 0

    @callback(
        Output(f"{base_id}_button", "children", allow_duplicate=True),
        Input(f"{upload_id}", "data"),
        prevent_initial_call=True,
    )
    def reset_labeled_counter_callback(_upload: str) -> int:
        """Reset the counter when an upload event occurs.

        Args:
            _upload: The contents of the upload component (unused).

        Returns:
            The reset value for the counter.

        """
        return reset_value

    @callback(
        Output(f"{base_id}_row", "style"),
        Input(f"{base_id}_store", "data"),
        prevent_initial_call=True,
    )
    def control_style(store: dict[str, Any]) -> dict[str, str]:
        """Control the visibility of the row based on max count.

        Args:
            store: A dictionary containing the max count of items.

        Returns:
            A dictionary specifying the display style for the row.

        """
        return (
            {"display": "none"}
            if store["max_count"] == 1
            else {"display": ""}
        )


def callback_labeled_counter_trio(base_id: str, resolution: int = 1) -> None:
    """Generate a Dash callback for incrementing and decrementing a count.

    Args:
        base_id (str): Base ID for the related Dash components.
        resolution (int, optional):
            Step size for incrementing/decrementing. Defaults to 1.

    Returns:
        None. The function registers callbacks with the Dash app.

    """

    @callback(
        Output(f"{base_id}_button", "children"),
        Input(f"{base_id}_decrement_button", "n_clicks"),
        Input(f"{base_id}_increment_button", "n_clicks"),
        State(f"{base_id}_store", "data"),
        State(f"{base_id}_button", "children"),
        prevent_initial_call=True,
    )
    def labeled_counter_trio_callback(
        _decrement: int,
        _increment: int,
        stored_data: dict[str, Any],
        current_count: str,
    ) -> Union[int, Any]:
        """Update the count when increment/decrement buttons are clicked.

        This function adjusts the current count, ensuring it stays within
        the range of 'resolution' to the maximum count stored in the data.

        Args:
            _increment: Number of times increment button clicked (unused).
            _decrement: Number of times decrement button clicked (unused).
            stored_data: Dictionary containing the maximum count.
            current_count: Current count as a string.

        Returns:
            Updated count, or no_update if no change.

        """
        try:
            max_count = stored_data["max_count"]
            min_count = stored_data["min_count"]
            current = int(current_count)
        except (KeyError, ValueError):
            return no_update

        if ctx.triggered_id == f"{base_id}_decrement_button":
            current -= resolution
        elif ctx.triggered_id == f"{base_id}_increment_button":
            current += resolution

        return max(min(current, max_count), min_count)


def callback_update_range_slider_value(
    base_id: str,
    lock: int | None = None,
) -> None:
    """Create a Dash callback to update the range slider value.

    Args:
        base_id: Base ID for the related Dash components.
        lock: Index of the slider handle to lock (0 or 1). Defaults to None.

    Returns:
        None. The function registers callbacks with the Dash app.

    """

    @callback(
        Output(f"{base_id}_range_slider", "value"),
        Input(f"{base_id}_button", "children"),
        Input(f"{base_id}_range_slider", "value"),
        prevent_initial_call=True,
    )
    def update_range_slider_value(
        current_count: str,
        range_slider_input,
    ) -> list[int]:
        """Update the range slider value based on the current count.

        Args:
            current_count: Current count as a string.
            range_slider_input: Current value of the range slider.

        Returns:
            A list of integers from 1 to the current count.

        """
        if ctx.triggered_id == f"{base_id}_range_slider":
            if lock is not None:
                if range_slider_input[lock] != 1:
                    range_slider_input[lock] = 1
                    return range_slider_input
            return no_update

        current = int(current_count)
        return list(range(1, current + 1))


def callback_labeled_counter_quintet(
    base_id: str,
    resolution: Union[int, float],
    decimal_places: Union[int, None] = None,
) -> None:
    """Create a Dash callback for incrementing and decrementing a count.

    Args:
        base_id: Base ID for the related Dash components.
        resolution: Step size for incrementing/decrementing.
        decimal_places: Number of decimal places to round to.

    Returns:
        None. The function registers callbacks with the Dash app.

    """

    @callback(
        Output(f"{base_id}_button", "children"),
        Input(f"{base_id}_divide_button", "n_clicks"),
        Input(f"{base_id}_decrement_button", "n_clicks"),
        Input(f"{base_id}_increment_button", "n_clicks"),
        Input(f"{base_id}_multiply_button", "n_clicks"),
        State(f"{base_id}_store", "data"),
        State(f"{base_id}_button", "children"),
        prevent_initial_call=True,
    )
    def labeled_counter_quintet_callback(
        _divide: int,
        _decrement: int,
        _increment: int,
        _multiply: int,
        stored_data: dict[str, Any],
        current_count: str,
    ) -> Union[float, Any]:
        """Update the count when increment/decrement buttons are clicked.

        This function adjusts the current count, ensuring it stays within
        the range of min_count to max_count stored in the data.

        Args:
            _divide: Number of times divide button clicked (unused).
            _increment: Number of times increment button clicked (unused).
            _decrement: Number of times decrement button clicked (unused).
            _multiply: Number of times multiply button clicked (unused).
            stored_data: Dictionary containing min and max counts.
            current_count: Current count as a string.

        Returns:
            Updated count, or no_update if no change.

        """
        try:
            max_count = stored_data["max_count"]
            min_count = stored_data["min_count"]
            current = float(current_count)
        except (KeyError, ValueError):
            return no_update

        if ctx.triggered_id == f"{base_id}_divide_button":
            current /= 10
        elif ctx.triggered_id == f"{base_id}_decrement_button":
            current -= resolution
        elif ctx.triggered_id == f"{base_id}_increment_button":
            current += resolution
        elif ctx.triggered_id == f"{base_id}_multiply_button":
            current *= 10

        return round(
            float(max(min(current, max_count), min_count)), decimal_places
        )


def callback_update_range_slider_pushable_and_value(base_id: str) -> None:
    """Generate a callback to update range slider pushable property and value.

    Args:
        base_id (str): Base ID for the Dash components.

    Returns:
        None. The function registers callbacks with the Dash app.

    """

    @callback(
        Output(f"{base_id}_range_slider", "pushable"),
        Output(f"{base_id}_range_slider", "value"),
        Input(f"{base_id}_button", "children"),
        State(f"{base_id}_range_slider", "value"),
        prevent_initial_call=True,
    )
    def update_range_slider_pushable_and_value(
        current_count: str,
        slider_value: list[int],
    ) -> tuple[int, list[int]]:
        """Update range slider pushable and value based on button clicks.

        Args:
            current_count (str): Current count from button clicks.
            slider_value (List[int]): Current slider value.

        Returns:
            Tuple[int, List[int]]: Updated pushable value and slider value.

        """
        slider_value[1] = slider_value[0] + int(current_count)
        return int(current_count), slider_value
