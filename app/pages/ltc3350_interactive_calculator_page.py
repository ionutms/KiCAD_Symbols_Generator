"""LTC3350 Interactive Calculator Page.

This module contains the layout for the LTC3350 Interactive
Calculator page of the Dash web application. It provides a
documentation page with formulas and explanations for capacitor
calculations, ESR analysis, and backup time verification.

The page uses a responsive multi-column layout system that adapts
to different screen sizes, displaying technical content alongside
mathematical formulas.

"""

import forallpeople as si
import numpy as np
from dash import Input, Output, callback, dcc, html, register_page

si.environment("default")

link_name = __name__.rsplit(".", maxsplit=1)[-1].replace("_page", "").title()
module_name = __name__.rsplit(".", maxsplit=1)[-1]

register_page(
    __name__,
    name=link_name,
    path="/ltc3350_interactive_calculator",
    order=99,
    **{"exclude_from_nav": True},
)


def create_section(*columns, column_widths=None, responsive_breakpoint="lg"):
    """Create a responsive section with multiple columns.

    All columns are treated equally - content is always wrapped
    in a list for consistent handling, regardless of position.

    Args:
        *columns:
            Variable number of content items. Each can be:
                - A single component (will be wrapped in list)
                - A list of components (used as-is)
        column_widths:
            List of column widths for each column
            (default: equal distribution)
            Can be integers (1-12) or tuples for responsive widths
            Examples: [6, 6], [(12, 6), (12, 6)], [4, 4, 4]
        responsive_breakpoint:
            Bootstrap breakpoint for responsive behavior.
            Options: 'sm', 'md', 'lg', 'xl', 'xxl' (default: 'lg')

    Returns:
        html.Div: Responsive row container with specified columns

    """
    if not columns:
        return html.Div(className="row mb-4")

    num_columns = len(columns)

    # Determine column widths
    if column_widths is None:
        # Equal distribution
        width_per_column = 12 // num_columns
        column_widths = [width_per_column] * num_columns

    # Validate column widths
    if len(column_widths) != num_columns:
        raise ValueError(
            f"Number of column_widths ({len(column_widths)}) "
            f"must match number of columns ({num_columns})"
        )

    # Create column divs
    column_divs = []
    for idx, (content, width) in enumerate(zip(columns, column_widths)):
        # ALWAYS normalize content to list for consistent handling
        if not isinstance(content, list):
            content = [content]

        # Handle responsive widths
        if isinstance(width, tuple):
            mobile_width, desktop_width = width
            col_class = (
                f"col-{mobile_width} "
                f"col-{responsive_breakpoint}-{desktop_width}"
            )
        else:
            col_class = f"col-12 col-{responsive_breakpoint}-{width}"

        # Add spacing classes
        spacing_class = "mb-3" if idx < num_columns - 1 else ""
        spacing_class += (
            f" mb-{responsive_breakpoint}-0" if idx < num_columns - 1 else ""
        )

        column_divs.append(
            html.Div(
                content,
                className=f"{col_class} {spacing_class}".strip(),
            )
        )

    return html.Div(
        column_divs,
        className="row mb-4",
    )


# Content components
paragraph_1 = dcc.Markdown(
    "When choosing the capacitance needed the condition of the "
    "supercapacitor at end of life (EOL) needs to be considered."
)

paragraph_2 = dcc.Markdown(
    "Since the backup time and backup power are known, the next "
    "item that needs to be determined is the maximum voltage to "
    "be applied to the capacitor $\\pmb{V_{CELL(MAX)}}$ to "
    "provide the maximum life expectancy for the application.",
    mathjax=True,
)

paragraph_3 = dcc.Markdown(
    "The number of capacitors in the stack also needs to be "
    "chosen plus the Utilization Factor ($\\pmb{\\alpha_B}$). "
    "$\\pmb{\\alpha_B}$ is the amount of energy in the "
    "capacitor to be used for backup. A typical "
    "$\\pmb{\\alpha_B}$ is 80%, but a conservative "
    "$\\pmb{\\alpha_B}$ of 70% can be used.",
    mathjax=True,
)

paragraph_4 = dcc.Markdown(
    "The minimum capacitance required for each capacitor in the "
    "stack at EOL can be calculated by the following equation:"
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

paragraph_5 = dcc.Markdown(
    "Where $\\pmb{\\eta}$ represents the boost efficiency, $\\pmb{n}$ "
    "represents the number of capacitors in the stack.",
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
    "the minimum stack voltage ($\\pmb{V_{CELL(MIN)}}$) at EOL. "
    "$\\pmb{V_{CELL(MIN)}}$ will be limited by either the maximum power "
    "transfer rule or by current limit, *whichever is greater*.",
    mathjax=True,
)

paragraph_9 = dcc.Markdown(
    "The minimum capacitor voltage due to the maximum power "
    "transfer rule can be calculated with the following formula:"
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
    "The calculated $\\pmb{V_{STK(MIN)}}$ can be used to determine if the "
    "chosen capacitor will be sufficient for worst case EOL conditions, "
    "when both $\\pmb{ESR_{EOL}}$ and $\\pmb{C_{EOL}}$ have been reached.",
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

interactive_calculator = html.Div(
    [
        html.Div(
            [
                dcc.Markdown("Boost Efficiency (${\\eta}$):", mathjax=True),
                dcc.Slider(
                    id="eta_slider",
                    min=0.5,
                    max=1.0,
                    step=0.01,
                    value=0.9,
                    marks={i / 10: f"{i / 10:.1f}" for i in range(5, 11)},
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
            ],
        ),
        html.Div(
            [
                dcc.Markdown("Number of Capacitors (n):"),
                dcc.Slider(
                    id="n_slider",
                    min=1,
                    max=4,
                    step=1,
                    value=4,
                    marks={i: str(i) for i in range(1, 5)},
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
            ],
        ),
        html.Div(
            [
                dcc.Markdown(
                    "Utilization Factor (${\\alpha_B}$): ", mathjax=True
                ),
                dcc.Slider(
                    id="alpha_b_slider",
                    min=0.1,
                    max=0.9,
                    step=0.05,
                    value=0.7,
                    marks={i / 10: f"{i / 10:.1f}" for i in range(1, 10)},
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
            ],
        ),
        html.Div(
            [
                dcc.Markdown("Backup Power (W):"),
                dcc.Slider(
                    id="p_backup_slider",
                    min=1,
                    max=100,
                    step=1,
                    value=25,
                    marks={i: str(i) for i in range(0, 101, 20)},
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
            ],
        ),
        html.Div(
            [
                dcc.Markdown("Backup Time (s):"),
                dcc.Slider(
                    id="t_backup_slider",
                    min=0.1,
                    max=60,
                    step=0.1,
                    value=1.8,
                    marks={i: str(i) for i in range(0, 61, 10)},
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
            ],
        ),
        html.Div(
            [
                dcc.Markdown("${V_{CELL(MAX)}}$", mathjax=True),
                dcc.Slider(
                    id="v_cell_max_slider",
                    min=1.0,
                    max=5.0,
                    step=0.1,
                    value=2.5,
                    marks={
                        mark: f"{mark:.1f}"
                        for mark in [1.0, 2.0, 3.0, 4.0, 5.0]
                    },
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
            ],
        ),
        html.Hr(className="my-2"),
        html.Div([
            html.Div(
                id="c_eol_output",
                style={"fontSize": "1.2em"},
            ),
        ]),
        html.Hr(className="my-2"),
    ],
)


@callback(
    Output("c_eol_output", "children"),
    Input("p_backup_slider", "value"),
    Input("t_backup_slider", "value"),
    Input("n_slider", "value"),
    Input("eta_slider", "value"),
    Input("v_cell_max_slider", "value"),
    Input("alpha_b_slider", "value"),
)
def calculate_c_eol(p_backup, t_backup, n, eta, v_cell_max, alpha_b):
    """Calculate C_EOL based on slider inputs using forallpeople."""
    P_BACKUP = p_backup * si.W
    t_BACKUP = t_backup * si.s
    V_CELL_MAX = v_cell_max * si.V

    sqrt_alpha = np.sqrt(alpha_b)
    numerator = 1 + sqrt_alpha
    denominator = np.sqrt(1 - alpha_b)

    if denominator == 0:
        return "Error: Invalid alpha_B value"

    log_term = np.log(numerator / denominator)
    bracket_term = alpha_b + sqrt_alpha - (1 - alpha_b) * log_term

    if bracket_term == 0:
        return "Error: Division by zero in calculation"

    numerator_ceol = 4 * P_BACKUP * t_BACKUP
    denominator_ceol = n * eta * (V_CELL_MAX**2)

    C_EOL = (numerator_ceol / denominator_ceol) * (1 / bracket_term)

    return f"C_EOL = {C_EOL}"


def layout() -> html.Div:
    """Define the page layout.

    Returns:
        html.Div: The layout for the LTC3350 Calculator page

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
                        className=(
                            "text-decoration-none text-primary fw-bold"
                        ),
                    ),
                ],
                className="d-flex align-items-center mb-4",
            ),
            create_section([paragraph_1, paragraph_2, paragraph_3]),
            html.Hr(className="my-2"),
            html.H3("Capacitance Calculation at EOL", className="mb-2"),
            create_section(
                [paragraph_4, paragraph_5],
                [formula_c_end_of_life],
                column_widths=[5, 7],
            ),
            html.Hr(className="my-2"),
            html.H3("ESR Calculation at EOL", className="mb-2"),
            create_section(
                [paragraph_6, paragraph_7],
                [formula_esr_end_of_life],
                column_widths=[5, 7],
            ),
            html.Hr(className="my-2"),
            html.H3(
                "Minimum Stack Voltage Verification",
                className="mb-2",
            ),
            create_section([paragraph_8]),
            create_section(
                [paragraph_9],
                [paragraph_10],
            ),
            create_section(
                [formula_v_stk_min_at_max_power],
                [formula_v_stk_min_at_crt_lim, paragraph_11],
            ),
            create_section([paragraph_12]),
            html.Hr(className="my-2"),
            html.H3("Backup Time Calculation", className="mb-2"),
            create_section(
                [formula_t_backup, paragraph_13],
                [
                    formula_gamma_max,
                    formula_gamma_min,
                    formula_v_square_loss,
                ],
                column_widths=[7, 5],
            ),
            html.Hr(className="my-2"),
            create_section([interactive_calculator]),
        ],
        className="container-fluid p-4",
    )
