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

paragraph_1 = dcc.Markdown(
    "When choosing the capacitance needed the condition of the "
    "supercapacitor at end of life (EOL) needs to be considered."
)

paragraph_2 = dcc.Markdown(
    "The number of capacitors in the stack also needs to be chosen plus the "
    "Utilization Factor ($\\pmb{\\alpha_B}$). $\\pmb{\\alpha_B}$ is the "
    "amount of energy in the capacitor to be used for backup. "
    "A typical $\\pmb{\\alpha_B}$ is 80%, but a conservative "
    "$\\pmb{\\alpha_B}$ of 70% can be used.",
    mathjax=True,
)

paragraph_3 = dcc.Markdown(
    "The minimum capacitance required for each capacitor in the stack at EOL "
    "can be calculated by the following equation:"
)

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
    className="formula-container",
)

paragraph_4 = dcc.Markdown(
    "Where $\\pmb{\\eta}$ represents the boost efficiency, "
    "$\\pmb{n}$ represents the number of capacitors in the stack.",
    mathjax=True,
)

paragraph_5 = dcc.Markdown(
    "Since the backup time and backup power are known, the next item that "
    "needs to be determined is the maximum voltage to be applied to the "
    "capacitor $\\pmb{V_{CELL(MAX)}}$ to provide the "
    "maximum life expectancy for the application.",
    mathjax=True,
)

paragraph_6 = dcc.Markdown(
    "The maximum capacitor ESR at end of life can then be determined below:"
)

formula_esr_end_of_life = html.Div(
    [
        dcc.Markdown(
            r"""
            $$ ESR_{EOL} = \frac{\eta \cdot (1-\alpha_B) \cdot n
            \cdot V_{CELL(MAX)}^2}{4 \cdot P_{BACKUP}} $$
            """,
            mathjax=True,
        )
    ],
    className="formula-container",
)

paragraph_7 = dcc.Markdown(
    "Now the EOL parameters are known, the capacitor can be chosen based on "
    "the manufacture capacitor specification for EOL."
)

paragraph_8 = dcc.Markdown(
    "To verify the capacitors are adequate at EOL we first need to determine "
    "the minimum stack voltage ($\\pmb{V_{CELL(MIN)}}$) at "
    "EOL. $\\pmb{V_{CELL(MIN)}}$ will be limited by either "
    "the maximum power transfer rule or by current limit, "
    "*whichever is greater*.",
    mathjax=True,
)

paragraph_9 = dcc.Markdown(
    "The minimum capacitor voltage due to the maximum power transfer rule "
    "can be calculated with the following formula:"
)

formula_v_stk_min_at_max_power = html.Div(
    [
        dcc.Markdown(
            r"""
            $$ V_{STK(MIN)} = \sqrt{\frac{4 \cdot ESR_{EOL} \cdot n
            \cdot P_{BACKUP}}{\eta}} $$
            """,
            mathjax=True,
        )
    ],
    className="formula-container",
)

paragraph_10 = dcc.Markdown(
    "$\\pmb{V_{STK(MIN)}}$ can also be determined by the "
    "current limit and the $\\pmb{ESR_{EOL}}$ as shown in "
    "the following equation:",
    mathjax=True,
)

formula_v_stk_min_at_crt_lim = html.Div(
    [
        dcc.Markdown(
            r"""
            $$ V_{STK(MIN)} = {\frac{P_{BACKUP}}{\eta \cdot I_{LMAX}}}
            + n \cdot ESR_{EOL} \cdot I_{LMAX} $$
            """,
            mathjax=True,
        )
    ],
    className="formula-container",
)

paragraph_11 = dcc.Markdown(
    "Where $\\pmb{I_{LMAX}}$ is the boost peak current limit.",
    mathjax=True,
)

paragraph_12 = dcc.Markdown(
    "The calculated $\\pmb{V_{STK(MIN)}}$ can be used to "
    "determine if the chosen capacitor will be sufficient for worst case EOL "
    "conditions, when both $\\pmb{ESR_{EOL}}$ and "
    "$\\pmb{C_{EOL}}$ have been reached.",
    mathjax=True,
)

formula_t_backup = html.Div(
    [
        dcc.Markdown(
            r"""
            $$ t_{BACKUP} = \frac{\eta \cdot C_{STK}}
            {4 \cdot P_{BACKUP}} \cdot
            \left[\gamma_{(MAX)} \cdot V_{STK(MAX)}^2 -
            \gamma_{(MIN)} \cdot V_{STK(MIN)}^2 - V_{LOSS}^2\right] $$
            """,
            mathjax=True,
        )
    ],
    className="formula-container",
)

paragraph_13 = dcc.Markdown(
    "Where $\\pmb{C_{STK}}$ is the total stack capacitance, "
    "$\\pmb{V_{STK(MIN)}}$ is based on the higher calculated "
    "$\\pmb{V_{STK(MIN)}}$,",
    mathjax=True,
)

formula_gamma_max = html.Div(
    [
        dcc.Markdown(
            r"""
            $$ \gamma_{(MAX)} = 1+\sqrt{1-\frac{4 \cdot n \cdot ESR_{EOL}
            \cdot P_{BACKUP}}{\eta \cdot V_{STK(MAX)}^2}} \text{ , } $$
            """,
            mathjax=True,
        )
    ],
    className="formula-container",
)

formula_gamma_min = html.Div(
    [
        dcc.Markdown(
            r"""
            $$ \gamma_{(MIN)} = 1+\sqrt{1-\frac{4 \cdot n \cdot ESR_{EOL}
            \cdot P_{BACKUP}}{\eta \cdot V_{STK(MIN)}^2}} \text{ and } $$
            """,
            mathjax=True,
        )
    ],
    className="formula-container",
)

formula_v_square_loss = html.Div(
    [
        dcc.Markdown(
            r"""
            $$ V_{LOSS}^2 = \frac{4 \cdot n \cdot ESR_{EOL} P_{BACKUP}}
            {\eta} \cdot \log{\left(\frac{\gamma_{(MAX)} \cdot V_{STK(MAX)}}
            {\gamma_{(MIN)} \cdot V_{STK(MIN)}}\right)} $$
            """,
            mathjax=True,
        )
    ],
    className="formula-container",
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
            paragraph_4,
            paragraph_5,
            paragraph_6,
            formula_esr_end_of_life,
            paragraph_7,
            paragraph_8,
            paragraph_9,
            formula_v_stk_min_at_max_power,
            paragraph_10,
            formula_v_stk_min_at_crt_lim,
            paragraph_11,
            paragraph_12,
            formula_t_backup,
            paragraph_13,
            formula_gamma_max,
            formula_gamma_min,
            formula_v_square_loss,
        ],
        className="p-4",
    )
