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
from dash import Input, Output, callback, dash_table, dcc, html, register_page

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


def create_slider(
    label,
    slider_id,
    min_val,
    max_val,
    step,
    default_val,
    marks_list=None,
    marks_step=None,
    use_mathjax=False,
):
    """Create a slider with label.

    Args:
        label: Label text for the slider
        slider_id: ID for the slider component
        min_val: Minimum slider value
        max_val: Maximum slider value
        step: Step size
        default_val: Default value
        marks_list: List of specific mark values
        marks_step: Step for automatic marks
        use_mathjax: Whether to render label with MathJax

    """
    if marks_list is not None:
        marks = {
            mark: f"{mark:.1f}" if isinstance(mark, float) else str(mark)
            for mark in marks_list
        }
    elif marks_step is not None:
        marks = {
            i: str(i)
            for i in range(int(min_val), int(max_val) + 1, marks_step)
        }
    else:
        marks = None

    return html.Div([
        dcc.Markdown(label, mathjax=use_mathjax),
        dcc.Slider(
            id=slider_id,
            min=min_val,
            max=max_val,
            step=step,
            value=default_val,
            marks=marks,
            tooltip={"placement": "bottom", "always_visible": True},
        ),
    ])


def calculate_backup_time(
    cap_si, esr_si, eta, n, p_backup_si, v_cell_max_si, i_peak
):
    """Calculate backup time for given capacitor parameters."""
    v_stk_min_power = np.sqrt(4 * esr_si * n * p_backup_si / eta)
    v_stk_min_current = (p_backup_si / (eta * i_peak)) + (n * esr_si * i_peak)
    v_stk_min_calc = max(v_stk_min_power, v_stk_min_current)

    gama_max_calc = 1 + np.sqrt(
        1
        - (
            (4 * n * esr_si * p_backup_si)
            / (eta * np.power(n * v_cell_max_si, 2))
        )
    )
    gama_min_calc = 1 + np.sqrt(
        1
        - (
            (4 * n * esr_si * p_backup_si)
            / (eta * np.power(v_stk_min_calc, 2))
        )
    )

    v_loss_sq_calc = ((4 * n * esr_si * p_backup_si) / eta) * np.log(
        (gama_max_calc * n * v_cell_max_si) / (gama_min_calc * v_stk_min_calc)
    )

    t_backup_calc = (
        eta
        * (cap_si / n)
        / (4 * p_backup_si)
        * (
            gama_max_calc * (n * v_cell_max_si) ** 2
            - gama_min_calc * v_stk_min_calc**2
            - v_loss_sq_calc
        )
    )

    return t_backup_calc


def create_markdown_div(content, class_name="col-12 text-center"):
    """Create a markdown div with consistent styling."""
    return html.Div(
        [
            dcc.Markdown(content, mathjax=True),
        ],
        className=class_name,
    )


interactive_calculator = html.Div([
    create_slider(
        "Boost Efficiency (${\\eta}$):",
        "eta_slider",
        min_val=0.5,
        max_val=1.0,
        step=0.01,
        default_val=0.9,
        marks_list=[i / 10 for i in range(5, 11)],
        use_mathjax=True,
    ),
    create_slider(
        "Number of Capacitors (n):",
        "n_slider",
        min_val=1,
        max_val=4,
        step=1,
        default_val=4,
        marks_list=[1, 2, 3, 4],
    ),
    create_slider(
        "Utilization Factor (${\\alpha_B}$):",
        "alpha_b_slider",
        min_val=0.1,
        max_val=0.9,
        step=0.05,
        default_val=0.7,
        marks_list=[i / 10 for i in range(1, 10)],
        use_mathjax=True,
    ),
    create_slider(
        "Backup Power (W):",
        "p_backup_slider",
        min_val=1,
        max_val=100,
        step=1,
        default_val=25,
        marks_step=20,
    ),
    create_slider(
        "Backup Time (s):",
        "t_backup_slider",
        min_val=0.1,
        max_val=60,
        step=0.1,
        default_val=1.8,
        marks_step=10,
    ),
    create_slider(
        "${V_{CELL(MAX)}}$",
        "v_cell_max_slider",
        min_val=1.0,
        max_val=5.0,
        step=0.1,
        default_val=2.5,
        marks_list=[1.0, 2.0, 3.0, 4.0, 5.0],
        use_mathjax=True,
    ),
    create_slider(
        "${R_{SNSC}}$ (${\\Omega}$)",
        "r_snsc_slider",
        min_val=0.001,
        max_val=0.02,
        step=0.001,
        default_val=0.006,
        use_mathjax=True,
    ),
    html.Div([
        html.Div(
            id="calculated_values_between_sliders",
            style={"fontSize": "1em"},
        ),
    ]),
    create_slider(
        "${ESR_{EOL\\ SELECTED}}$ (${\\Omega}$)",
        "esr_eol_selected_slider",
        min_val=0.001,
        max_val=0.2,
        step=0.001,
        default_val=0.064,
        use_mathjax=True,
    ),
    create_slider(
        "${C_{EOL\\ SELECTED}}$ (F)",
        "c_eol_selected_slider",
        min_val=1,
        max_val=300,
        step=1,
        default_val=7,
        use_mathjax=True,
    ),
    html.Hr(className="my-2"),
    html.Div([
        html.Div(
            id="calculated_values",
            style={"fontSize": "1em"},
        ),
    ]),
    html.Hr(className="my-2"),
    html.Div(id="backup_time_table"),
])


@callback(
    Output("calculated_values", "children"),
    Output("calculated_values_between_sliders", "children"),
    Output("backup_time_table", "children"),
    Input("p_backup_slider", "value"),
    Input("t_backup_slider", "value"),
    Input("n_slider", "value"),
    Input("eta_slider", "value"),
    Input("v_cell_max_slider", "value"),
    Input("alpha_b_slider", "value"),
    Input("r_snsc_slider", "value"),
    Input("esr_eol_selected_slider", "value"),
    Input("c_eol_selected_slider", "value"),
)
def calculate_values(
    p_backup_slider_value,
    t_backup_slider_value,
    n_slider_value,
    eta_slider_value,
    v_cell_max_slider_value,
    alpha_b_slider_value,
    r_snsc_slider_value,
    esr_eol_selected_slider_value,
    c_eol_selected_slider_value,
):
    """Calculate values based on slider inputs."""
    p_backup = p_backup_slider_value * si.W
    t_backup = t_backup_slider_value * si.s
    v_cell_max = v_cell_max_slider_value * si.V
    r_snsc_slider = r_snsc_slider_value * si.Ohm
    esr_eol_selected_slider = esr_eol_selected_slider_value * si.Ohm
    c_eol_selected_slider = c_eol_selected_slider_value * si.F

    c_eol = (
        (4 * p_backup * t_backup)
        / (n_slider_value * eta_slider_value * (v_cell_max**2))
    ) * (
        (
            alpha_b_slider_value
            + np.sqrt(alpha_b_slider_value)
            - (1 - alpha_b_slider_value)
            * np.log(
                (1 + np.sqrt(alpha_b_slider_value))
                / np.sqrt(1 - alpha_b_slider_value)
            )
        )
        ** -1
    )

    esr_eol = (
        eta_slider_value
        * (1 - alpha_b_slider_value)
        * n_slider_value
        * (v_cell_max**2)
    ) / (4 * p_backup)

    i_peak = 0.058 * si.V / r_snsc_slider

    v_stk_min_max_power = np.sqrt(
        (4 * esr_eol_selected_slider * n_slider_value * p_backup)
        / eta_slider_value
    )

    v_stk_min_current_limit = p_backup / (eta_slider_value * i_peak) + (
        n_slider_value * esr_eol_selected_slider * i_peak
    )

    v_stk_min = max(v_stk_min_max_power, v_stk_min_current_limit)

    v_stk_max = n_slider_value * v_cell_max

    gamma_max = 1 + np.sqrt(
        1
        - (4 * n_slider_value * esr_eol_selected_slider * p_backup)
        / (eta_slider_value * (v_stk_max**2))
    )

    gamma_min = 1 + np.sqrt(
        1
        - (4 * n_slider_value * esr_eol_selected_slider * p_backup)
        / (eta_slider_value * (v_stk_min**2))
    )

    v_loss_squared = (
        (4 * n_slider_value * esr_eol_selected_slider * p_backup)
        / eta_slider_value
    ) * np.log((gamma_max * v_stk_max) / (gamma_min * v_stk_min))

    t_backup_calculated = (
        (eta_slider_value * (c_eol_selected_slider / n_slider_value))
        / (4 * p_backup)
    ) * (
        gamma_max * (v_stk_max**2)
        - gamma_min * (v_stk_min**2)
        - v_loss_squared
    )

    calculated_values_between_sliders = html.Div([
        html.Div(
            [
                create_markdown_div(
                    f"$C_{{EOL}}$ = {c_eol}",
                    "col-12 col-md-4 offset-md-2 text-center",
                ),
                create_markdown_div(
                    f"$ESR_{{EOL}}$ = {esr_eol:.1f}",
                    "col-12 col-md-4 offset-md-0 text-center",
                ),
            ],
            className="row",
        ),
    ])

    calculated_values_output = html.Div([
        html.Div(
            [
                create_markdown_div(
                    f"$I_{{PEAK}}$ = {i_peak}", "col-12 col-md text-center"
                ),
                create_markdown_div(
                    f"$V_{{STK(MIN) Max Power}}$ = {v_stk_min_max_power}",
                    "col-12 col-md text-center",
                ),
                create_markdown_div(
                    f"$V_{{STK(MIN) Current Limit}}$ = "
                    f"{v_stk_min_current_limit}",
                    "col-12 col-md text-center",
                ),
                create_markdown_div(
                    f"$V_{{STK(MIN)}}$ = {v_stk_min}",
                    "col-12 col-md text-center",
                ),
            ],
            className="row",
        ),
        html.Div(
            [
                create_markdown_div(
                    f"$\\gamma_{{(MAX)}}$ = {gamma_max:.4f}",
                    "col-12 col-md text-center",
                ),
                create_markdown_div(
                    f"$\\gamma_{{(MIN)}}$ = {gamma_min:.4f}",
                    "col-12 col-md text-center",
                ),
                create_markdown_div(
                    f"$V_{{LOSS}}^2$ = {v_loss_squared}",
                    "col-12 col-md text-center",
                ),
                create_markdown_div(
                    f"$t_{{BACKUP}}$ = {t_backup_calculated}",
                    "col-12 col-md text-center",
                ),
            ],
            className="row",
        ),
    ])

    cap_esr_pairs = [
        (10, 0.034),
        (15, 0.03),
        (20, 0.03),
        (50, 0.024),
        (100, 0.001),
        (300, 0.0045),
    ]

    table_data = []

    power_row = {"Parameter": "P<sub>BACKUP</sub> (W)"}
    for i in range(len(cap_esr_pairs)):
        power_row[f"Cap_{i + 1}"] = f"{p_backup_slider_value * si.W:.0f}"
    table_data.append(power_row)

    time_row = {"Parameter": "t<sub>BACKUP</sub> [s]"}
    for i in range(len(cap_esr_pairs)):
        time_row[f"Cap_{i + 1}"] = f"{t_backup_slider_value * si.s:.1f}"
    table_data.append(time_row)

    cap_row = {"Parameter": "C (C<sub>EOL</sub>) [F]"}
    for i, (cap_initial, _) in enumerate(cap_esr_pairs):
        cap_eol = f"{cap_initial * 0.8 * si.F:.0f}"
        cap_row[f"Cap_{i + 1}"] = f"{cap_initial * si.F:.0f} ({cap_eol})"
    table_data.append(cap_row)

    esr_row = {"Parameter": "ESR (ESR<sub>EOL</sub>) [Ω]"}
    for i, (_, esr_initial) in enumerate(cap_esr_pairs):
        esr_eol_val = f"{esr_initial * 2 * si.Ohm:.0f}"
        esr_row[f"Cap_{i + 1}"] = (
            f"{esr_initial * si.Ohm:.0f} ({esr_eol_val})"
        )
    table_data.append(esr_row)

    initial_time_row = {"Parameter": "t<sub>BACKUP Initial</sub> [s]"}
    for i, (cap_initial, esr_initial) in enumerate(cap_esr_pairs):
        cap_si = cap_initial * si.F
        esr_si = esr_initial * si.Ohm

        t_backup_calc = calculate_backup_time(
            cap_si,
            esr_si,
            eta_slider_value,
            n_slider_value,
            p_backup,
            v_cell_max,
            i_peak,
        )

        time_value = float(t_backup_calc.value)

        time_str = (
            "N/A"
            if time_value < 0 or np.isnan(time_value)
            else f"{time_value * si.s:.1f}"
        )
        initial_time_row[f"Cap_{i + 1}"] = time_str
    table_data.append(initial_time_row)

    eol_time_row = {"Parameter": "t<sub>BACKUP EOL</sub> [s]"}
    for i, (cap_initial, esr_initial) in enumerate(cap_esr_pairs):
        cap_eol = cap_initial * 0.8
        esr_eol_val = esr_initial * 2

        cap_si = cap_eol * si.F
        esr_si = esr_eol_val * si.Ohm

        t_backup_calc = calculate_backup_time(
            cap_si,
            esr_si,
            eta_slider_value,
            n_slider_value,
            p_backup,
            v_cell_max,
            i_peak,
        )

        time_value = float(t_backup_calc.value)

        time_str = (
            "N/A"
            if time_value < 0 or np.isnan(time_value)
            else f"{time_value * si.s:.1f}"
        )
        eol_time_row[f"Cap_{i + 1}"] = time_str
    table_data.append(eol_time_row)

    columns = [
        {"name": "Parameter", "id": "Parameter", "presentation": "markdown"}
    ]
    for i in range(len(cap_esr_pairs)):
        columns.append({"name": f"Capacitor {i + 1}", "id": f"Cap_{i + 1}"})

    backup_time_table = html.Div(
        dash_table.DataTable(
            data=table_data,
            columns=columns,
            cell_selectable=False,
            markdown_options={"html": True},
            css=[
                {
                    "selector": "tr:hover",
                    "rule": "background-color: rgba(0, 0, 0, 0) !important;",
                }
            ],
            style_cell={
                "textAlign": "center",
                "padding": "10px",
                "fontSize": "14px",
                "border": "1px solid rgba(100, 100, 100, 0.4)",
                "minWidth": "120px",
            },
            style_header={
                "backgroundColor": "rgba(0, 0, 0, 0)",
                "color": "inherit",
                "fontWeight": "bold",
                "border": "1px solid rgba(100, 100, 100, 0.4)",
                "borderBottom": "2px solid rgba(80, 80, 80, 0.6)",
            },
            style_data={
                "backgroundColor": "rgba(0, 0, 0, 0)",
                "color": "inherit",
                "border": "1px solid rgba(100, 100, 100, 0.4)",
            },
            style_data_conditional=[
                {
                    "if": {"column_id": "Parameter"},
                    "fontWeight": "bold",
                    "textAlign": "left",
                    "fontFamily": "inherit",
                },
            ],
        ),
        style={"overflowX": "auto"},
    )

    return (
        calculated_values_output,
        calculated_values_between_sliders,
        backup_time_table,
    )


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
            html.Hr(className="my-2"),
        ],
        className="container-fluid p-4",
    )
