"""Style Utilities for Dash Components.

This module defines styles and styling functions for various Dash components.
It includes predefined styles for headings, accordion items, radio buttons,
and table components. It also provides functions for generating dynamic styles
based on the current theme (light or dark).

Styles:
    heading_3_style: Style for h3 headings.
    accordionitem_style: Style for accordion items.
    accordion_style: Style for accordions.
    radioitems_style: Style for radio button groups.

Constants:
    CENTER_DIV_CONTENT: Class for centering div content.
    CENTER_CLASS_NAME: Class for centering elements.
    CENTER_BOTTOM_CLASS_NAME: Class for centering elements at the bottom.
    GLOBAL_STYLE: Global style applied to all components.
    FLEX_CENTER_COLUMN: Class for flex container with centered column layout.
    RESPONSIVE_CENTER_BUTTON_CLASS: Class for responsive centered buttons.
    CENTER_CONTENT_CLASS: Class for centering content.
    TABLE_GLOBAL_STYLES: Dictionary of global styles for table components.

Functions:
    generate_css: Generate CSS rules for the DataTable.
    generate_style_data: Generate style for table cells.
    generate_style_header: Generate style for table header.
    generate_style_data_conditional:
        Generate conditional styles for table rows.
    generate_style_table: Generate style for the table container.
    generate_style_cell: Generate style for table cells.
    generate_style_filter: Generate style for table filters.
    style_accordionitem_title: Create a styled accordion item title.
"""
from dash import html

heading_3_style = {"font-size": "30px", "font-weight": "bold"}

accordionitem_style = {"border": "2px solid #abc", "border-radius": "5px"}

accordion_style = {"width": "100%", "margin": "5px auto"}

radioitems_style = {"max-height": "400px", "overflow-y": "auto"}

CENTER_DIV_CONTENT = (
    "d-flex flex-column justify-content-center align-items-center h-100"
)

CENTER_CLASS_NAME = "w-100 d-flex justify-content-center align-items-center"

CENTER_BOTTOM_CLASS_NAME = "d-flex justify-content-center align-items-end"

GLOBAL_STYLE = {"font-family": "Roboto"}

FLEX_CENTER_COLUMN = (
    "d-flex flex-column justify-content-center align-items-center"
)

RESPONSIVE_CENTER_BUTTON_CLASS = (
    "w-100 d-flex justify-content-center align-items-center mb-2 mb-md-0"
)

CENTER_CONTENT_CLASS = (
    "w-100 d-flex justify-content-center align-items-center"
)

TABLE_GLOBAL_STYLES = {
    "font_family": "'Roboto', sans-serif",
    "light_background": "white",
    "dark_background": "#666666",
    "light_color": "black",
    "dark_color": "white",
    "header_background_light": "#DDDDDD",
    "header_background_dark": "#111111",
    "filter_background_light": "#F8F8F8",
    "filter_background_dark": "#555555",
    "placeholder_color_light": "#AAAAAA",
    "placeholder_color_dark": "#CCCCCC",
    "input_text_color_light": "#555555",
    "input_text_color_dark": "#E0E0E0",
    "cell_padding": "10px",
    "filter_padding": "5px",
    "cell_font_size": "14px",
    "header_font_size": "16px",
    "filter_font_size": "16px",
    "placeholder_font_size": "14px",
    "font_weight_normal": "normal",
    "font_weight_bold": "bold",
    "font_style_normal": "normal",
    "font_style_bold": "bold",
    "white_space_normal": "normal",
    "white_space_pre_wrap": "pre-wrap",
    "height_auto": "auto",
    "text_align_center": "center",
    "overflow_x_auto": "auto",
    "overflow_y_auto": "auto",
    "min_width_100": "100%",
    "width_100": "100%",
    "max_width_100": "100%",
    "overflow_hidden": "hidden",
    "text_overflow_ellipsis": "ellipsis",
}


def generate_css(switch: bool) -> list[dict[str, str]]:  # noqa: FBT001
    """Generate CSS rules for the DataTable based on the theme switch value.

    Args:
        switch (bool):
            The state of the theme switch (True for light, False for dark).

    Returns:
        list[dict[str, str]]:
            A list of CSS rule dictionaries for table filters and
            placeholders.

    """
    input_color = (
        TABLE_GLOBAL_STYLES["input_text_color_light"]
        if switch
        else TABLE_GLOBAL_STYLES["input_text_color_dark"]
    )
    placeholder_color = (
        TABLE_GLOBAL_STYLES["placeholder_color_light"]
        if switch
        else TABLE_GLOBAL_STYLES["placeholder_color_dark"]
    )

    return [
        {
            "selector": ".dash-filter input",
            "rule": f"""
                text-align: {TABLE_GLOBAL_STYLES["text_align_center"]}
                            !important;
                font-size: {TABLE_GLOBAL_STYLES["filter_font_size"]}
                           !important;
                padding: {TABLE_GLOBAL_STYLES["filter_padding"]} !important;
                color: {input_color} !important;
                font-family: {TABLE_GLOBAL_STYLES["font_family"]} !important;
            """,
        },
        {
            "selector": ".dash-filter input::placeholder",
            "rule": f"""
                color: {placeholder_color} !important;
                font-size: {TABLE_GLOBAL_STYLES["placeholder_font_size"]}
                           !important;
                text-align: {TABLE_GLOBAL_STYLES["text_align_center"]}
                            !important;
                font-style: {TABLE_GLOBAL_STYLES["font_style_bold"]}
                            !important;
                font-family: {TABLE_GLOBAL_STYLES["font_family"]} !important;
            """,
        },
    ]


def generate_style_data(switch: bool) -> dict[str, str]:  # noqa: FBT001
    """Generate style for table cells based on the theme switch value.

    Args:
        switch (bool):
            The state of the theme switch (True for light, False for dark).

    Returns:
        dict[str, str]: A dictionary of style properties for table cells.

    """
    return {
        "backgroundColor": (
            TABLE_GLOBAL_STYLES["light_background"]
            if switch
            else TABLE_GLOBAL_STYLES["dark_background"]
        ),
        "color": (
            TABLE_GLOBAL_STYLES["light_color"]
            if switch
            else TABLE_GLOBAL_STYLES["dark_color"]
        ),
        "fontWeight": TABLE_GLOBAL_STYLES["font_weight_normal"],
        "whiteSpace": TABLE_GLOBAL_STYLES["white_space_normal"],
        "height": TABLE_GLOBAL_STYLES["height_auto"],
        "font-family": TABLE_GLOBAL_STYLES["font_family"],
    }


def generate_style_header(switch: bool) -> dict[str, str]:  # noqa: FBT001
    """Generate style for table header based on the theme switch value.

    Args:
        switch (bool):
            The state of the theme switch (True for light, False for dark).

    Returns:
        dict[str, str]: A dictionary of style properties for table header.

    """
    return {
        "backgroundColor": (
            TABLE_GLOBAL_STYLES["header_background_light"]
            if switch
            else TABLE_GLOBAL_STYLES["header_background_dark"]
        ),
        "fontSize": TABLE_GLOBAL_STYLES["header_font_size"],
        "textAlign": TABLE_GLOBAL_STYLES["text_align_center"],
        "height": TABLE_GLOBAL_STYLES["height_auto"],
        "whiteSpace": TABLE_GLOBAL_STYLES["white_space_pre_wrap"],
        "fontWeight": TABLE_GLOBAL_STYLES["font_weight_bold"],
        "color": (
            TABLE_GLOBAL_STYLES["light_color"]
            if switch
            else TABLE_GLOBAL_STYLES["dark_color"]
        ),
        "font-family": TABLE_GLOBAL_STYLES["font_family"],
    }


def generate_style_data_conditional(
    switch: bool,  # noqa: FBT001
) -> list[dict[str, dict[str, str]]]:
    """Generate conditional styles for table rows based on the theme switch.

    Args:
        switch (bool):
            The state of the theme switch (True for light, False for dark).

    Returns:
        list[dict[str, dict[str, str]]]:
            A list of conditional style dictionaries for table rows.

    """
    return [
        {
            "if": {"row_index": "odd"},
            "backgroundColor": (
                TABLE_GLOBAL_STYLES["filter_background_light"]
                if switch
                else TABLE_GLOBAL_STYLES["filter_background_dark"]
            ),
        },
    ]


def generate_style_table() -> dict[str, str]:
    """Generate style for the table container.

    Returns:
        dict[str, str]:
            A dictionary of style properties for the table container.

    """
    return {
        "overflowX": TABLE_GLOBAL_STYLES["overflow_x_auto"],
        "minWidth": TABLE_GLOBAL_STYLES["min_width_100"],
        "width": TABLE_GLOBAL_STYLES["width_100"],
        "maxWidth": TABLE_GLOBAL_STYLES["max_width_100"],
        "height": TABLE_GLOBAL_STYLES["height_auto"],
        "overflowY": TABLE_GLOBAL_STYLES["overflow_y_auto"],
        "font-family": TABLE_GLOBAL_STYLES["font_family"],
    }


def generate_style_cell() -> dict[str, str]:
    """Generate style for table cells.

    Returns:
        dict[str, str]: A dictionary of style properties for table cells.

    """
    return {
        "textAlign": TABLE_GLOBAL_STYLES["text_align_center"],
        "overflow": TABLE_GLOBAL_STYLES["overflow_hidden"],
        "textOverflow": TABLE_GLOBAL_STYLES["text_overflow_ellipsis"],
        "fontSize": TABLE_GLOBAL_STYLES["cell_font_size"],
        "padding": TABLE_GLOBAL_STYLES["cell_padding"],
        "font-family": TABLE_GLOBAL_STYLES["font_family"],
        "whiteSpace": TABLE_GLOBAL_STYLES["white_space_normal"],
        "height": TABLE_GLOBAL_STYLES["height_auto"],
    }


def generate_style_filter(switch: bool) -> dict[str, str]:  # noqa: FBT001
    """Generate style for table filters based on the theme switch value.

    Args:
        switch (bool):
            The state of the theme switch (True for light, False for dark).

    Returns:
        dict[str, str]: A dictionary of style properties for table filters.

    """
    return {
        "backgroundColor": (
            TABLE_GLOBAL_STYLES["filter_background_light"]
            if switch
            else TABLE_GLOBAL_STYLES["filter_background_dark"]
        ),
    }


def style_accordionitem_title(title: str, font_size: int = 24) -> html.H1:
    """Create a styled accordion item title.

    Args:
        title (str): The text content of the title.
        font_size (int, optional): The font size in pixels. Defaults to 24.

    Returns:
        html.H1: A styled H1 element for use as an accordion item title.

    """
    style_accordionitem_title_params = {
        "font-size": f"{font_size}px",
        "font-weight": "bold",
        "font-family": "Roboto",
        "text-align": "center",
        "width": "100%",
        "margin": "0px auto",
        "padding": "0px",
    }
    return html.H1(title, style=style_accordionitem_title_params)
