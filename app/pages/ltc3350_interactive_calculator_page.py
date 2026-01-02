"""LTC3350 Interactive Calculator Page.

This module contains the layout for the LTC3350 Interactive Calculator
page of the Dash web application. It serves as a calculator tool
for the LTC3350 project.

Attributes:
    link_name (str): The name of the page link.
    module_name (str): The name of the module.

"""

from dash import html, register_page

link_name = __name__.rsplit(".", maxsplit=1)[-1].replace("_page", "").title()
module_name = __name__.rsplit(".", maxsplit=1)[-1]

register_page(
    __name__,
    name=link_name,
    path="/ltc3350_interactive_calculator",
    order=99,
    **{"exclude_from_nav": True},
)


def layout() -> html.Div:
    """Define the page layout.

    Returns:
        html.Div: The layout for the Minimal LTC3350 Project page

    """
    return html.Div(
        [
            html.Div(
                [
                    html.H1(
                        "LTC3350 Interactive Calculator",
                        className="d-inline-block me-auto",
                    ),
                    html.A(
                        "Return Home",
                        href="/",
                        className="text-decoration-none text-primary fw-bold",
                    ),
                ],
                className="d-flex align-items-center mb-4",
            ),
            html.P("This is an interactive calculator for the LTC3350 IC. "),
        ],
        className="p-4",
    )
