"""LTC3350 Interactive Calculator Page.

This module contains the layout for the LTC3350 Interactive Calculator
page of the Dash web application. It serves as a calculator tool
for the LTC3350 project.

Attributes:
    link_name (str): The name of the page link.
    module_name (str): The name of the module.

"""

from dash import dcc, html, register_page

link_name = __name__.rsplit(".", maxsplit=1)[-1].replace("_page", "").title()
module_name = __name__.rsplit(".", maxsplit=1)[-1]

register_page(
    __name__,
    name=link_name,
    path="/ltc3350_interactive_calculator",
    order=99,
    **{"exclude_from_nav": True},
)

formula_markdown_style = {
    "display": "flex",
    "justifyContent": "center",
    "alignItems": "center",
    "width": "98%",
    "margin": "2px auto",
}

paragraph_1 = dcc.Markdown(
    "When choosing the capacitance needed the condition of the "
    "supercapacitor at end of life (EOL) needs to be considered."
)

paragraph_2 = dcc.Markdown(
    "The number of capacitors in the stack also needs to be chosen plus the "
    "Utilization Factor ($\\alpha_B$). $\\alpha_B$ is the amount of energy "
    "in the capacitor to be used for backup. A typical $\\alpha_B$ is 80%, "
    "but a conservative $\\alpha_B$ of 70% can be used.",
    mathjax=True,
)

paragraph_3 = dcc.Markdown(
    "The minimum capacitance required for each capacitor in the stack at EOL "
    "can be calculated by the following equation:"
)

# Create a Div for the formula with centered layout
formula_c_end_of_life = html.Div(
    [
        dcc.Markdown(
            r"""
            $$ C_{EOL} = \frac{4 \cdot P_{BACKUP} \cdot t_{BACKUP}}
            {n \cdot \eta \cdot V_{CELL(MAX)}^2} \cdot
            \left[\alpha_B + \sqrt{\alpha_B} -
            (1-\alpha_B)\log\left(\frac{1+\sqrt{\alpha_B}}
            {\sqrt{1-\sqrt{\alpha_B}}}\right)\right]^{-1} $$
            """,
            mathjax=True,
        )
    ],
    style=formula_markdown_style,
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
            paragraph_1,
            paragraph_2,
            paragraph_3,
            formula_c_end_of_life,
        ],
        className="p-4",
    )
