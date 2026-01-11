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
import pandas as pd
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

    if column_widths is None:
        width_per_column = 12 // num_columns
        column_widths = [width_per_column] * num_columns

    if len(column_widths) != num_columns:
        raise ValueError(
            f"Number of column_widths ({len(column_widths)}) "
            f"must match number of columns ({num_columns})"
        )

    column_divs = []
    for idx, (content, width) in enumerate(zip(columns, column_widths)):
        if not isinstance(content, list):
            content = [content]

        if isinstance(width, tuple):
            mobile_width, desktop_width = width
            col_class = (
                f"col-{mobile_width} "
                f"col-{responsive_breakpoint}-{desktop_width}"
            )
        else:
            col_class = f"col-12 col-{responsive_breakpoint}-{width}"

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

paragraph_14 = dcc.Markdown(
    "The maximum input current is determined by the resistance across the "
    "VOUTSP and VOUTSN pins, $\\pmb{R_{SNSI}}$.\n\n"
    "The maximum charge current is determined by the value of the sense "
    "resistor, $\\pmb{R_{SNSC}}$, used in series with the inductor.\n\n"
    "The input and charge current loops servo the voltage across their "
    "respective sense resistor to 32mV.\n\n"
    "The peak inductor current limit, $\\pmb{I_{PEAK}}$, is 80% higher than "
    "the maximum charge current",
    mathjax=True,
)

formula_i_in_max = html.Div(
    dcc.Markdown(
        r"""
        $$ I_{IN(MAX)} = \frac{32mV}
        {R_{SNSI}} $$
        """,
        mathjax=True,
    ),
    className="formula-container",
)

formula_i_chg_max = html.Div(
    dcc.Markdown(
        r"""
        $$ I_{CHG(MAX)} = \frac{32mV}
        {R_{SNSC}} $$
        """,
        mathjax=True,
    ),
    className="formula-container",
)

formula_i_peak = html.Div(
    dcc.Markdown(
        r"""
        $$ I_{PEAK} = \frac{58mV}
        {R_{SNSC}} $$
        """,
        mathjax=True,
    ),
    className="formula-container",
)

paragraph_15 = dcc.Markdown(
    "The LTC3350 $\\pmb{V_{CAP}}$ voltage is set by an external feedback "
    "resistor divider. \n\nThe regulated output voltage is determined by "
    "following formula where CAPFBREF is the output of the $\\pmb{V_{CAP}}$ "
    "DAC, programmed in the vcapfb_dac register",
    mathjax=True,
)

formula_v_cap = html.Div(
    [
        dcc.Markdown(
            r"""
            $$ V_{CAP} = 1 + \left( \frac{R_{FBC\ TOP}}
            {R_{FBC\ BOTTOM}} \right) \cdot CAPFBREF $$
            """,
            mathjax=True,
        )
    ],
    className="formula-container",
)

paragraph_16 = dcc.Markdown(
    "The input voltage threshold below which the power-fail status pin, "
    "$\\overline{\\text{PFO}}$, indicates a power-fail condition and the "
    "LTC3350 bidirectional controller switches to step-up mode is "
    "programmed using a resistor divider from the VIN pin to SGND via the "
    "PFI pin. $\\pmb{V_{PFI(TH)}}$ is 1.17V. Typical values for "
    "$\\pmb{R_{PF\\_TOP}}$ and $\\pmb{R_{PF\\_BOTTOM}}$ are in the range "
    "of 40k to 1M.",
    mathjax=True,
)

formula_v_in_step_up_mode = html.Div(
    [
        dcc.Markdown(
            r"""
            $$ V_{IN\_STEP\_UP} = 1 + \left( \frac{R_{PF\_TOP}}
            {R_{PF\_BOTTOM}} \right) \cdot V_{PFI(TH)} $$
            """,
            mathjax=True,
        )
    ],
    className="formula-container",
)

paragraph_17 = dcc.Markdown(
    "The input voltage above which the power-fail status pin "
    "$\\overline{\\text{PFO}}$ is high impedance and the bidirectional "
    "controller switches to step-down mode. $\\pmb{V_{PFI(HYS)}}$ is the "
    "hysteresis of the PFI comparator and is equal to 30mV",
    mathjax=True,
)

formula_v_in_step_down_mode = html.Div(
    [
        dcc.Markdown(
            r"""
            $$ V_{IN\_STEP\_DOWN} = 1 + \left( \frac{R_{PF\ TOP}}
            {R_{PF\ BOTTOM}} \right) \cdot (V_{PFI(TH)} + V_{PFI(HYS)}) $$
            """,
            mathjax=True,
        )
    ],
    className="formula-container",
)

paragraph_18 = dcc.Markdown(
    "The output voltage for the controller in step-up mode is set by an "
    "external feedback resistor divider",
    mathjax=True,
)

formula_v_out = html.Div(
    [
        dcc.Markdown(
            r"""
            $$ V_{OUT} = 1 + \left( \frac{R_{FBO\ TOP}}
            {R_{PBO\ BOTTOM}} \right) \cdot 1.2V $$
            """,
            mathjax=True,
        )
    ],
    className="formula-container",
)

paragraph_19 = dcc.Markdown(
    "The $\\pmb{R_{T}}$ pin is used to program the switching frequency. "
    "A resistor, $\\pmb{R_{T}}$, from this pin to ground sets the "
    "switching frequency according to:",
    mathjax=True,
)

paragraph_20 = dcc.Markdown(
    "$\\pmb{R_{T}}$ also sets the scale factor for the capacitor "
    "measurement value.",
    mathjax=True,
)

formula_f_sw = html.Div(
    [
        dcc.Markdown(
            r"""
            $$
            F_{SW}(MHz) = \frac{53.5}{R_{T}(kHz)}
            $$
            """,
            mathjax=True,
        )
    ],
    className="formula-container",
)

paragraph_21 = dcc.Markdown(
    "The switching frequency and inductor selection are interrelated. "
    "Higher switching frequencies allow the use of smaller inductor and "
    "capacitor values, but generally results in lower efficiency due to "
    "MOSFET switching and gate charge losses. In addition, the effect of "
    "inductor value on ripple current must also be considered. "
    "The inductor ripple current decreases with higher inductance or higher "
    "frequency and increases with higher VIN. Accepting larger values of "
    "ripple current allows the use of low inductances but results in higher "
    "output voltage ripple and greater core losses. "
    "$\\pmb{V_{IN(MAX)}}$ is the maximum input voltage, "
    "$\\pmb{I_{CHG(MAX)}}$ is the maximum regulated charge current, "
    "and $\\pmb{f_{SW}}$ is the switching frequency. "
    "Using these equations, the inductor ripple will be at most 25% of "
    "$\\pmb{I_{CHG(MAX)}}$.",
    mathjax=True,
)

formula_indunctance_v_in_max_leq_2_v_cap = html.Div(
    dcc.Markdown(
        r"""
        $$
        L_{V_{IN(MAX)} \leq 2V_{CAP}} = \frac{V_{IN(MAX)}}
        {I_{CHG(MAX)} \cdot f_{SW}}
        $$
        """,
        mathjax=True,
    ),
    className="formula-container",
)

formula_indunctance_v_in_max_geq_2_v_cap = html.Div(
    dcc.Markdown(
        r"""
        $$
        L_{V_{IN(MAX)} \geq 2V_{CAP}} = \left(1 - \frac{V_{CAP}}
        {V_{IN(MAX)}}\right) \cdot \frac{V_{CAP}}
        {0.25 \cdot I_{CHG(MAX)} \cdot f_{SW}}
        $$
        """,
        mathjax=True,
    ),
    className="formula-container",
)

paragraph_22 = dcc.Markdown(
    "$\\pmb{V_{OUT}}$ serves as the input to the synchronous controller in "
    "step-down mode and as the output in step-up (backup) mode. \n\nIf "
    "step-up mode is used, place 100µF of bulk (aluminum electrolytic, "
    "OS-CON, POSCAP) capacitance for every 2A of backup current desired. "
    "\n\nFor 5V system applications, 100µF per 1A of backup current is "
    "recommended. In addition, a certain amount of high frequency bypass "
    "capacitance is needed to minimize voltage ripple. \n\nMaximum ripple "
    "occurs at the lowest $\\pmb{V_{CAP}}$ that can supply "
    "$\\pmb{I_{OUT(BACKUP)}}$. \n\nMultilayer ceramics are recommended for "
    "high frequency filtering. \n\nIf step-up mode is unused, then the "
    "specification for $\\pmb{C_{OUT}}$ will be determined by the desired "
    "ripple voltage in step-down mode.",
    mathjax=True,
)

formula_delta_v_out_step_up_used = html.Div(
    dcc.Markdown(
        r"""
        $$
        \Delta V_{OUT}(step\text{-}up\ used) = \left[\left(1
        - \frac{V_{CAP}}{V_{OUT}}\right)
        \cdot \frac{1}{C_{OUT} \cdot f_{SW}}
        + \frac{V_{OUT}}{V_{CAP}} \cdot R_{ESR}\right]
        \cdot I_{OUT(BACKUP)}
        $$
        """,
        mathjax=True,
    ),
    className="formula-container",
)

formula_delta_v_out_step_up_unused = html.Div(
    dcc.Markdown(
        r"""
        $$
        \Delta V_{OUT}(step\text{-}up\ unused) = \frac{V_{CAP}}
        {V_{OUT}} \cdot \left(1 - \frac{V_{CAP}}{V_{OUT}}\right)
        \cdot \frac{I_{CHG(MAX)}}{C_{OUT} \cdot f_{SW}}
        + I_{CHG(MAX)} \cdot R_{ESR}
        $$
        """,
        mathjax=True,
    ),
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
    unit=None,
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
        unit: forallpeople unit for mark formatting

    """

    def format_mark_value(mark, unit):
        """Format mark value with unit, removing unnecessary zeros."""
        if unit is not None:
            value_with_unit = mark * unit
            str_val = str(value_with_unit)
            if "." in str_val:
                parts = str_val.rsplit(" ", 1)
                if len(parts) == 2:
                    num_part, unit_part = parts
                    num_part = num_part.rstrip("0").rstrip(".")
                    return f"{num_part} {unit_part}"
            return str_val
        else:
            if isinstance(mark, float) and mark == int(mark):
                return str(int(mark))
            elif isinstance(mark, float):
                return f"{mark:.10f}".rstrip("0").rstrip(".")
            else:
                return str(mark)

    if marks_list is not None:
        marks = {mark: format_mark_value(mark, unit) for mark in marks_list}
    elif marks_step is not None:
        marks = {
            i: format_mark_value(i, unit)
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


def read_cap_esr_pairs_from_csv(csv_file_path):
    """Read data from a CSV file."""
    try:
        df = pd.read_csv(csv_file_path)
        cap_esr_pairs = [
            (
                float(row["cap_value"]),
                float(row["esr_value"]),
                row["part_number"],
            )
            for _, row in df.iterrows()
        ]
    except FileNotFoundError:
        print(f"Warning: CSV file {csv_file_path} not found.")

    return cap_esr_pairs


interactive_calculator = html.Div([
    html.H5("System Parameters", className="mt-3 mb-3 fw-bold text-primary"),
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
    html.H5(
        "Backup Requirements", className="mt-4 mb-3 fw-bold text-primary"
    ),
    create_slider(
        "Backup Power (W):",
        "p_backup_slider",
        min_val=1,
        max_val=100,
        step=1,
        default_val=25,
        marks_list=[1, 20, 40, 60, 80, 100],
        unit=si.W,
    ),
    create_slider(
        "Backup Time (s):",
        "t_backup_slider",
        min_val=0.1,
        max_val=60,
        step=0.1,
        default_val=1.8,
        marks_list=[0.1, 10, 20, 30, 40, 50, 60],
        unit=si.s,
    ),
    create_slider(
        "${V_{CELL(MAX)}}$ (V):",
        "v_cell_max_slider",
        min_val=2.2,
        max_val=5.0,
        step=0.1,
        default_val=2.5,
        marks_list=[2.2, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
        use_mathjax=True,
        unit=si.V,
    ),
    html.H5(
        "Current Sense Resistors", className="mt-4 mb-3 fw-bold text-primary"
    ),
    create_slider(
        "${R_{SNSC}}$ (${\\Omega}$)",
        "r_snsc_slider",
        min_val=0.001,
        max_val=0.02,
        step=0.001,
        default_val=0.006,
        marks_list=[0.001, 0.005, 0.01, 0.015, 0.02],
        use_mathjax=True,
        unit=si.Ohm,
    ),
    create_slider(
        "${R_{SNSI}}$ (${\\Omega}$)",
        "r_snsi_slider",
        min_val=0.001,
        max_val=0.02,
        step=0.001,
        default_val=0.016,
        marks_list=[0.001, 0.005, 0.01, 0.015, 0.02],
        use_mathjax=True,
        unit=si.Ohm,
    ),
    html.Div([
        html.Div(
            id="calculated_values_between_sliders",
            style={"fontSize": "1em"},
        ),
    ]),
    html.H5(
        "Selected Capacitor EOL Specifications",
        className="mt-4 mb-3 fw-bold text-primary",
    ),
    create_slider(
        "${ESR_{EOL\\ SELECTED}}$ (${\\Omega}$)",
        "esr_eol_selected_slider",
        min_val=0.001,
        max_val=0.2,
        step=0.001,
        default_val=0.064,
        marks_list=[0.001, 0.05, 0.1, 0.15, 0.2],
        use_mathjax=True,
        unit=si.Ohm,
    ),
    create_slider(
        "${C_{EOL\\ SELECTED}}$ (F)",
        "c_eol_selected_slider",
        min_val=1,
        max_val=300,
        step=1,
        default_val=7,
        marks_list=[1, 50, 100, 150, 200, 250, 300],
        use_mathjax=True,
        unit=si.F,
    ),
    html.Hr(className="my-3"),
    html.Div([
        html.Div(
            id="calculated_values",
            style={"fontSize": "1em"},
        ),
    ]),
    html.Hr(className="my-3"),
    html.Div(id="backup_time_table"),
    html.Hr(className="my-3"),
    html.H5(
        [html.Span("V"), html.Sub("CAP"), html.Span(" Feedback Resistors")],
        className="mt-3 mb-3 fw-bold text-primary",
    ),
    html.Div(
        [
            html.Div(
                [
                    create_slider(
                        "${R_{FBC\\ TOP}}$ (${\\Omega}$)",
                        "r_fbc_top_slider",
                        min_val=1000,
                        max_val=1_000_000,
                        step=1000,
                        default_val=886_000,
                        marks_list=[1000, 250000, 500000, 750000, 1000000],
                        use_mathjax=True,
                        unit=si.Ohm,
                    ),
                    create_slider(
                        "${R_{FBC\\ BOTTOM}}$ (${\\Omega}$)",
                        "r_fbc_bottom_slider",
                        min_val=1000,
                        max_val=1_000_000,
                        step=1000,
                        default_val=118_000,
                        marks_list=[1000, 250000, 500000, 750000, 1000000],
                        use_mathjax=True,
                        unit=si.Ohm,
                    ),
                    create_slider(
                        "CAPFBREF (V)",
                        "capfbref_slider",
                        min_val=0.6375,
                        max_val=1.2,
                        step=0.0375,
                        default_val=1.2,
                        marks_list=[0.6375, 0.8, 1.0, 1.2],
                        unit=si.V,
                    ),
                ],
                className="col-12 col-lg-10",
            ),
            html.Div(
                id="v_cap_display",
                className=(
                    "col-12 col-lg-2 d-flex align-items-center "
                    "justify-content-center"
                ),
                style={"fontSize": "1.2em"},
            ),
        ],
        className="row",
    ),
    html.Hr(className="my-3"),
    html.H5(
        "Power-Fail Input Resistors",
        className="mt-3 mb-3 fw-bold text-primary",
    ),
    html.Div(
        [
            html.Div(
                [
                    create_slider(
                        "${R_{PF\\ TOP}}$ (${\\Omega}$)",
                        "r_pf_top_slider",
                        min_val=1000,
                        max_val=1_000_000,
                        step=1000,
                        default_val=787_000,
                        marks_list=[1000, 250000, 500000, 750000, 1000000],
                        use_mathjax=True,
                        unit=si.Ohm,
                    ),
                    create_slider(
                        "${R_{PF\\ BOTTOM}}$ (${\\Omega}$)",
                        "r_pf_bottom_slider",
                        min_val=1000,
                        max_val=1_000_000,
                        step=1000,
                        default_val=100_000,
                        marks_list=[1000, 250000, 500000, 750000, 1000000],
                        use_mathjax=True,
                        unit=si.Ohm,
                    ),
                ],
                className="col-12 col-lg-9",
            ),
            html.Div(
                id="v_in_display",
                className=(
                    "col-12 col-lg-3 d-flex align-items-center "
                    "justify-content-center"
                ),
                style={"fontSize": "1.2em"},
            ),
        ],
        className="row",
    ),
    html.Hr(className="my-3"),
    html.H5(
        [html.Span("V"), html.Sub("OUT"), html.Span(" Feedback Resistors")],
        className="mt-3 mb-3 fw-bold text-primary",
    ),
    html.Div(
        [
            html.Div(
                [
                    create_slider(
                        "${R_{FBO\\ TOP}}$ (${\\Omega}$)",
                        "r_fbo_top_slider",
                        min_val=1000,
                        max_val=1_000_000,
                        step=1000,
                        default_val=669_000,
                        marks_list=[1000, 250000, 500000, 750000, 1000000],
                        use_mathjax=True,
                        unit=si.Ohm,
                    ),
                    create_slider(
                        "${R_{FBO\\ BOTTOM}}$ (${\\Omega}$)",
                        "r_fbo_bottom_slider",
                        min_val=1000,
                        max_val=1_000_000,
                        step=1000,
                        default_val=162_000,
                        marks_list=[1000, 250000, 500000, 750000, 1000000],
                        use_mathjax=True,
                        unit=si.Ohm,
                    ),
                ],
                className="col-12 col-lg-10",
            ),
            html.Div(
                id="v_out_display",
                className=(
                    "col-12 col-lg-2 d-flex align-items-center "
                    "justify-content-center"
                ),
                style={"fontSize": "1.2em"},
            ),
        ],
        className="row",
    ),
    html.Hr(className="my-3"),
    html.H5(
        [html.Span("Switching Frequency (R"), html.Sub("T"), html.Span(")")],
        className="mt-3 mb-3 fw-bold text-primary",
    ),
    html.Div(
        [
            html.Div(
                [
                    create_slider(
                        "${R_{T}}$ (${\\Omega}$)",
                        "r_t_slider",
                        min_val=53600,
                        max_val=267000,
                        step=100,
                        default_val=71500,
                        marks_list=[
                            53600,
                            100000,
                            150000,
                            200000,
                            250000,
                            267000,
                        ],
                        use_mathjax=True,
                        unit=si.Ohm,
                    ),
                ],
                className="col-12 col-lg-10",
            ),
            html.Div(
                id="f_sw_display",
                className=(
                    "col-12 col-lg-2 d-flex align-items-center "
                    "justify-content-center"
                ),
                style={"fontSize": "1.2em"},
            ),
        ],
        className="row",
    ),
    html.Hr(className="my-3"),
    html.H5(
        "Inductor Selection Parameters",
        className="mt-3 mb-3 fw-bold text-primary",
    ),
    html.Div(
        [
            html.Div(
                [
                    create_slider(
                        "${V_{IN(MAX)}}$ (${\\Omega}$)",
                        "v_in_max_slider",
                        min_val=4.5,
                        max_val=35,
                        step=0.1,
                        default_val=12,
                        marks_list=[4.5, 10, 15, 20, 25, 30, 35],
                        use_mathjax=True,
                        unit=si.V,
                    ),
                ],
                className="col-12 col-lg-9",
            ),
            html.Div(
                id="v_in_max_display",
                className=(
                    "col-12 col-lg-3 d-flex align-items-center "
                    "justify-content-center"
                ),
                style={"fontSize": "1.2em"},
            ),
        ],
        className="row",
    ),
    html.Hr(className="my-3"),
    html.H5(
        [
            html.Span("Output Capacitor (C"),
            html.Sub("OUT"),
            html.Span(") Parameters"),
        ],
        className="mt-3 mb-3 fw-bold text-primary",
    ),
    html.Div(
        [
            html.Div(
                [
                    create_slider(
                        "${C_{OUT}}$ (${\\mu}F$)",
                        "c_out_slider",
                        min_val=100,
                        max_val=500,
                        step=100,
                        default_val=100,
                        marks_list=[100, 200, 300, 400, 500],
                        use_mathjax=True,
                        unit=1e-6 * si.F,
                    ),
                    create_slider(
                        "${R_{ESR}}$ (${m\\Omega}$)",
                        "r_esr_slider",
                        min_val=1,
                        max_val=4500,
                        step=0.1,
                        default_val=12,
                        marks_list=[1, 1000, 2000, 3000, 4000, 4500],
                        use_mathjax=True,
                        unit=1e-3 * si.Ohm,
                    ),
                ],
                className="col-12 col-lg-8",
            ),
            html.Div(
                id="delta_v_out_display",
                className=(
                    "col-12 col-lg-4 d-flex align-items-center "
                    "justify-content-center"
                ),
                style={"fontSize": "1.2em"},
            ),
        ],
        className="row",
    ),
])


@callback(
    Output("calculated_values", "children"),
    Output("calculated_values_between_sliders", "children"),
    Output("backup_time_table", "children"),
    Output("v_out_display", "children"),
    Output("v_in_display", "children"),
    Output("v_cap_display", "children"),
    Output("f_sw_display", "children"),
    Output("v_in_max_display", "children"),
    Output("delta_v_out_display", "children"),
    Input("p_backup_slider", "value"),
    Input("t_backup_slider", "value"),
    Input("n_slider", "value"),
    Input("eta_slider", "value"),
    Input("v_cell_max_slider", "value"),
    Input("alpha_b_slider", "value"),
    Input("r_snsc_slider", "value"),
    Input("r_snsi_slider", "value"),
    Input("esr_eol_selected_slider", "value"),
    Input("c_eol_selected_slider", "value"),
    Input("r_fbc_top_slider", "value"),
    Input("r_fbc_bottom_slider", "value"),
    Input("capfbref_slider", "value"),
    Input("r_pf_top_slider", "value"),
    Input("r_pf_bottom_slider", "value"),
    Input("r_fbo_top_slider", "value"),
    Input("r_fbo_bottom_slider", "value"),
    Input("r_t_slider", "value"),
    Input("v_in_max_slider", "value"),
    Input("c_out_slider", "value"),
    Input("r_esr_slider", "value"),
)
def calculate_values(
    p_backup_slider_value,
    t_backup_slider_value,
    n_slider_value,
    eta_slider_value,
    v_cell_max_slider_value,
    alpha_b_slider_value,
    r_snsc_slider_value,
    r_snsi_slider_value,
    esr_eol_selected_slider_value,
    c_eol_selected_slider_value,
    r_fbc_top_slider_value,
    r_fbc_bottom_slider_value,
    capfbref_slider_value,
    r_pf_top_slider_value,
    r_pf_bottom_slider_value,
    r_fbo_top_slider_value,
    r_fbo_bottom_slider_value,
    r_t_slider_value,
    v_in_max_slider_value,
    c_out_slider_value,
    r_esr_slider_value,
):
    """Calculate values based on slider inputs."""
    p_backup = p_backup_slider_value * si.W
    t_backup = t_backup_slider_value * si.s
    v_cell_max = v_cell_max_slider_value * si.V
    r_snsc_slider = r_snsc_slider_value * si.Ohm
    r_snsi_slider = r_snsi_slider_value * si.Ohm
    esr_eol_selected_slider = esr_eol_selected_slider_value * si.Ohm
    c_eol_selected_slider = c_eol_selected_slider_value * si.F
    r_fbc_top_slider = r_fbc_top_slider_value * si.Ohm
    r_fbc_bottom_slider = r_fbc_bottom_slider_value * si.Ohm
    capfbref_slider = capfbref_slider_value * si.V
    r_pf_top_slider = r_pf_top_slider_value * si.Ohm
    r_pf_bottom_slider = r_pf_bottom_slider_value * si.Ohm
    r_fbo_top_slider = r_fbo_top_slider_value * si.Ohm
    r_fbo_bottom_slider = r_fbo_bottom_slider_value * si.Ohm
    r_t_slider = r_t_slider_value * si.Ohm
    v_in_max_slider = v_in_max_slider_value * si.V
    c_out_slider = c_out_slider_value * 1e-6 * si.F
    r_esr_slider = r_esr_slider_value * 1e-3 * si.Ohm

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

    i_in_max = 0.032 * si.V / r_snsi_slider
    i_chg_max = 0.032 * si.V / r_snsc_slider
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

    t_backup = (
        (eta_slider_value * (c_eol_selected_slider / n_slider_value))
        / (4 * p_backup)
    ) * (
        gamma_max * (v_stk_max**2)
        - gamma_min * (v_stk_min**2)
        - v_loss_squared
    )

    v_cap = 1 + (r_fbc_top_slider / r_fbc_bottom_slider) * capfbref_slider

    v_in_step_up = 1 + (r_pf_top_slider / r_pf_bottom_slider) * 1.17 * si.V

    v_in_step_down = 1 + (r_pf_top_slider / r_pf_bottom_slider) * (
        1.17 * si.V + 0.03 * si.V
    )

    v_out = 1 + (r_fbo_top_slider / r_fbo_bottom_slider) * 1.2 * si.V

    f_sw = 53.5 * 1_000_000 * si.Hz * 1000 * si.Ohm / r_t_slider

    indunctance_v_in_max_leq_2_v_cap = v_in_max_slider / (i_chg_max * f_sw)
    indunctance_v_in_max_geq_2_v_cap = (1 - v_cap / v_in_max_slider) * (
        v_cap / (0.25 * i_chg_max * f_sw)
    )

    delta_v_out_step_up_used = abs(
        (
            (1 - (v_cap / v_out))
            * (1 / (c_out_slider * f_sw) + ((v_out / v_cap) * r_esr_slider))
        )
        * ((c_out_slider / (100 * 1e-6 * si.F)) * 2 * si.A)
    )

    delta_v_out_step_up_unused = abs(
        (v_cap / v_out)
        * (
            (1 - (v_cap / v_out)) * (i_chg_max / (c_out_slider * f_sw))
            + i_chg_max * r_esr_slider
        )
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
                    f"$I_{{IN(MAX)}}$ = {i_in_max:.3f}",
                    "col-12 col-md text-center",
                ),
                create_markdown_div(
                    f"$I_{{CHG(MAX)}}$ = {i_chg_max:.3f}",
                    "col-12 col-md text-center",
                ),
            ],
            className="row",
        ),
        html.Div(
            [
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
            ],
            className="row",
        ),
        html.Div(
            [
                create_markdown_div(
                    f"$t_{{BACKUP}}$ = {t_backup:.1f}",
                    "col-12 col-md text-center",
                ),
            ],
            className="row",
        ),
    ])

    cap_esr_pairs = read_cap_esr_pairs_from_csv("cap_esr_pairs.csv")

    table_data = []

    power_row = {"Parameter": "P<sub>BACKUP</sub>"}
    for i in range(len(cap_esr_pairs)):
        power_row[f"Cap_{i + 1}"] = f"{p_backup_slider_value * si.W:.0f}"
    table_data.append(power_row)

    time_row = {"Parameter": "t<sub>BACKUP</sub>"}
    for i in range(len(cap_esr_pairs)):
        time_row[f"Cap_{i + 1}"] = f"{t_backup_slider_value * si.s:.1f}"
    table_data.append(time_row)

    part_number_row = {"Parameter": "Part Number"}
    for i, (_, _, part_number) in enumerate(cap_esr_pairs):
        part_number_row[f"Cap_{i + 1}"] = part_number
    table_data.append(part_number_row)

    cap_row = {"Parameter": "C (C<sub>EOL</sub>)"}
    for i, (cap_initial, _, _) in enumerate(cap_esr_pairs):
        cap_eol = f"{cap_initial * 0.8 * si.F:.0f}"
        cap_row[f"Cap_{i + 1}"] = f"{cap_initial * si.F:.0f} ({cap_eol})"
    table_data.append(cap_row)

    esr_row = {"Parameter": "ESR (ESR<sub>EOL</sub>)"}
    for i, (_, esr_initial, _) in enumerate(cap_esr_pairs):
        esr_eol_val = f"{esr_initial * 2 * si.Ohm:.1f}"
        esr_initial_val = f"{esr_initial * si.Ohm:.1f}"
        esr_row[f"Cap_{i + 1}"] = (
            f"{esr_initial_val.replace('.0', '')} "
            f"({esr_eol_val.replace('.0', '')})"
        )
    table_data.append(esr_row)

    initial_time_row = {"Parameter": "t<sub>BACKUP Initial</sub>"}
    for i, (cap_initial, esr_initial, _) in enumerate(cap_esr_pairs):
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
        initial_time_row[f"Cap_{i + 1}"] = time_str.replace(".0", "")
    table_data.append(initial_time_row)

    eol_time_row = {"Parameter": "t<sub>BACKUP EOL</sub>"}
    for i, (cap_initial, esr_initial, _) in enumerate(cap_esr_pairs):
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
        eol_time_row[f"Cap_{i + 1}"] = time_str.replace(".0", "")
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

    v_out_display = html.Div([
        create_markdown_div(
            f"$V_{{OUT}}$ = {v_out:.2f}",
            "col-12 col-md text-center",
        )
    ])

    v_in_display = html.Div([
        create_markdown_div(
            f"$V_{{IN\\_STEP\\_UP}}$ = {v_in_step_up:.2f}",
            "col-12 text-center",
        ),
        create_markdown_div(
            f"$V_{{IN\\_STEP\\_DOWN}}$ = {v_in_step_down:.2f}",
            "col-12 text-center",
        ),
    ])

    v_cap_display = html.Div([
        create_markdown_div(
            f"$V_{{CAP}}$ = {v_cap:.2f}",
            "col-12 text-center",
        )
    ])

    f_sw_display = html.Div([
        create_markdown_div(
            f"$f_{{SW}}$ = {f_sw:.2f}",
            "col-12 text-center",
        )
    ])

    inductance_display = html.Div([
        create_markdown_div(
            "$L_{{V_{{IN(MAX)}} \\leq 2V_{{CAP}}}}$ = "
            f"{indunctance_v_in_max_leq_2_v_cap:.2f}",
            "col-12 text-center",
        ),
        create_markdown_div(
            "$L_{{V_{{IN(MAX)}} \\geq 2V_{{CAP}}}}$ = "
            f"{indunctance_v_in_max_geq_2_v_cap:.2f}",
            "col-12 text-center",
        ),
    ])

    delta_vout_display = html.Div([
        create_markdown_div(
            "$\\Delta V_{{{{OUT}}}}$ (step-up used) = "
            f"{delta_v_out_step_up_used:.2f}",
            "col-12 text-center",
        ),
        create_markdown_div(
            "$\\Delta V_{{{{OUT}}}}$ (step-up unused) = "
            f"{delta_v_out_step_up_unused:.2f}",
            "col-12 text-center",
        ),
    ])

    return (
        calculated_values_output,
        calculated_values_between_sliders,
        backup_time_table,
        v_out_display,
        v_in_display,
        v_cap_display,
        f_sw_display,
        inductance_display,
        delta_vout_display,
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
            html.Hr(className="my-3"),
            html.H3("Capacitance Calculation at EOL", className="mb-2"),
            create_section(
                [paragraph_4, paragraph_5],
                [formula_c_end_of_life],
                column_widths=[5, 7],
            ),
            html.Hr(className="my-3"),
            html.H3("ESR Calculation at EOL", className="mb-2"),
            create_section(
                [paragraph_6, paragraph_7],
                [formula_esr_end_of_life],
                column_widths=[5, 7],
            ),
            html.Hr(className="my-3"),
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
            html.Hr(className="my-3"),
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
            html.Hr(className="my-3"),
            html.H3("Setting Input and Charge Currents", className="mb-2"),
            create_section(
                [paragraph_14],
                [formula_i_in_max],
                [formula_i_chg_max, formula_i_peak],
                column_widths=[8, 2, 2],
            ),
            html.Hr(className="my-3"),
            html.H3(
                ["Setting V", html.Sub("CAP"), " Voltage"], className="mb-2"
            ),
            create_section(
                [paragraph_15], [formula_v_cap], column_widths=[8, 4]
            ),
            html.Hr(className="my-3"),
            html.H3(
                "Power-Fail Comparator Input Voltage Threshold",
                className="mb-2",
            ),
            create_section(
                [paragraph_16],
                [formula_v_in_step_up_mode],
                column_widths=[7, 5],
            ),
            create_section(
                [paragraph_17],
                [formula_v_in_step_down_mode],
                column_widths=[7, 5],
            ),
            html.Hr(className="my-3"),
            html.H3(
                ["Setting V", html.Sub("OUT"), " Voltage in Backup Mode"],
                className="mb-2",
            ),
            create_section(
                [paragraph_18],
                [formula_v_out],
                column_widths=[8, 4],
            ),
            html.Hr(className="my-3"),
            html.H3(
                "RT Oscillator and Switching Frequency",
                className="mb-2",
            ),
            create_section(
                [paragraph_19, paragraph_20],
                [formula_f_sw],
                column_widths=[9, 3],
            ),
            html.Hr(className="my-3"),
            html.H3(
                "Inductor Selection",
                className="mb-2",
            ),
            create_section(
                [paragraph_21],
                [
                    formula_indunctance_v_in_max_leq_2_v_cap,
                    formula_indunctance_v_in_max_geq_2_v_cap,
                ],
                column_widths=[7, 5],
            ),
            html.Hr(className="my-3"),
            html.H3(
                [
                    "C",
                    html.Sub("OUT"),
                    " and C",
                    html.Sub("CAP"),
                    " Capacitance",
                ],
                className="mb-2",
            ),
            create_section(
                [paragraph_22],
                [
                    formula_delta_v_out_step_up_used,
                    formula_delta_v_out_step_up_unused,
                ],
                column_widths=[5, 7],
            ),
            html.Hr(className="my-3"),
            create_section([interactive_calculator]),
            html.Hr(className="my-3"),
        ],
        className="container-fluid p-4",
    )
