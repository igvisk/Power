import flet as ft
from logic import calculate_power

VERSION = "2.0"


def main(page: ft.Page):

    # ===============================
    # ===== WINDOW ==================
    # ===============================
    page.title = f"Power Calculator {VERSION}"
    page.padding = 5
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#111111"

    # ===============================
    # ===== DEFAULT VALUES ==========
    # ===============================
    DEFAULT_CURRENT = 16
    DEFAULT_VOLTAGE_1PH = 230
    DEFAULT_VOLTAGE_3PH = 400
    DEFAULT_PF = 0.98

    # ===============================
    # ===== INPUT STYLE =============
    # ===============================
    input_style = dict(
        dense=True,
        text_size=13,
        text_align=ft.TextAlign.CENTER,
        bgcolor="#1c1c1c",
        border_color="#2a2a2a",
        color="#e5e5e5",
    )

    # ===============================
    # ===== INPUTS ==================
    # ===============================
    current = ft.TextField(
        label="I (A)",
        value=str(DEFAULT_CURRENT),
        expand=True,
        keyboard_type="number",
        **input_style,
    )

    voltage = ft.TextField(
        label="U (V)",
        value=str(DEFAULT_VOLTAGE_1PH),
        expand=True,
        keyboard_type="number",
        **input_style,
    )

    pf = ft.TextField(
        label="cos φ",
        value=str(DEFAULT_PF),
        expand=True,
        keyboard_type="number",
        **input_style,
    )

    inputs_row = ft.Row(
        width=300,
        spacing=6,
        controls=[current, voltage, pf],
    )

    # ===============================
    # ===== PHASE SELECTOR ==========
    # ===============================
    selected_phase = 1

    def refresh_phase_buttons():
        for i, btn in enumerate(phase_buttons.controls, start=1):
            btn.bgcolor = "#facc15" if i == selected_phase else "#2a2a2a"
            btn.content.color = "#000000" if i == selected_phase else "#e5e5e5"
            btn.scale = 1.05 if i == selected_phase else 1

    def set_phase_value(value):
        nonlocal selected_phase
        selected_phase = value

        try:
            current_voltage = float(voltage.value.replace(",", "."))
            if selected_phase in [2, 3] and current_voltage == DEFAULT_VOLTAGE_1PH:
                voltage.value = str(DEFAULT_VOLTAGE_3PH)
            elif selected_phase == 1 and current_voltage == DEFAULT_VOLTAGE_3PH:
                voltage.value = str(DEFAULT_VOLTAGE_1PH)
        except:
            pass

        refresh_phase_buttons()
        page.update()

    def phase_button(label, value):
        return ft.Container(
            content=ft.Text(label, size=16, weight=ft.FontWeight.BOLD),
            width=90,
            height=40,
            alignment=ft.Alignment.CENTER,
            border_radius=20,
            bgcolor="#facc15" if value == selected_phase else "#2a2a2a",
            on_click=lambda e: set_phase_value(value),
            animate_scale=150,
            ink=False,
        )

    phase_buttons = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
        controls=[
            phase_button("1", 1),
            phase_button("2", 2),
            phase_button("3", 3),
        ],
    )

    refresh_phase_buttons()

    # ===============================
    # ===== RESULTS =================
    # ===============================

    display_style = dict(
        size=16,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
        color="#facc15",
        font_family="RobotoMono",
        no_wrap=True,
    )

    p_text = ft.Text(**display_style)
    s_text = ft.Text(**display_style)
    q_text = ft.Text(**display_style)

    result_row = ft.Row(
        expand=True,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Active (W)", size=12, color="#6b7280"),
                    p_text,
                ],
            ),
            ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Apparent (VA)", size=12, color="#6b7280"),
                    s_text,
                ],
            ),
            ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Reactive (VAr)", size=12, color="#6b7280"),
                    q_text,
                ],
            ),
        ],
    )



    result_box = ft.Container(
        width=360,
        padding=16,
        bgcolor="#0a0a0a",
        border_radius=12,
        border=ft.Border.all(2, "#222222"),
        shadow=ft.BoxShadow(
            blur_radius=40,
            spread_radius=3,
            color="#facc15",
        ),
        content=result_row,
    )

    # ===============================
    # ===== CALCULATE ==============
    # ===============================
    def on_calculate(e):

        try:
            entered_current = float(current.value.replace(",", "."))
            if entered_current <= 0:
                entered_current = DEFAULT_CURRENT
        except:
            entered_current = DEFAULT_CURRENT

        current.value = str(entered_current)

        try:
            entered_voltage = float(voltage.value.replace(",", "."))
            if entered_voltage <= 0:
                raise ValueError
        except:
            entered_voltage = (
                DEFAULT_VOLTAGE_3PH if selected_phase in [2, 3]
                else DEFAULT_VOLTAGE_1PH
            )

        voltage.value = str(entered_voltage)

        try:
            entered_pf = float(pf.value.replace(",", "."))
            if entered_pf < 0.1 or entered_pf > 1:
                entered_pf = DEFAULT_PF
        except:
            entered_pf = DEFAULT_PF

        pf.value = f"{entered_pf:.2f}"

        res = calculate_power(
            current=entered_current,
            voltage=entered_voltage,
            power_factor=entered_pf,
            phases=selected_phase,
        )

        voltage.value = str(res["voltage"])

        p_text.value = f"{res['P']:.0f}"
        s_text.value = f"{res['S']:.0f}"
        q_text.value = f"{res['Q']:.0f}"

        page.update()

    calculate_btn = ft.ElevatedButton(
        "Calculate power",
        width=300,
        elevation=6,
        style=ft.ButtonStyle(
            bgcolor={
                ft.ControlState.DEFAULT: "#facc15",
                ft.ControlState.HOVERED: "#ffe58a",
            },
            color="#000000",
        ),
        on_click=on_calculate,
    )

    # ===============================
    # ===== LAYOUT ==================
    # ===============================
    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Container(
                alignment=ft.Alignment.CENTER,
                content=ft.Column(
                    width=320,
                    spacing=22,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            "⚡ Power Calculator",
                            size=26,
                            weight=ft.FontWeight.BOLD,
                            color="#e5e5e5",
                        ),
                        result_box,
                        ft.Container(height=6),  # <-- medzera navyše
                        inputs_row,
                        ft.Text(
                            "Number of phases",
                            size=12,
                            color="#6b7280",
                        ),
                        phase_buttons,
                        ft.Container(height=0.1),  # <-- medzera navyše
                        calculate_btn,
                    ],
                ),
            ),
        ),
    )

    page.bottom_appbar = ft.Container(
        padding=65,
        content=ft.Text(
            f"Power Calculator {VERSION} | ©2026 Igor Vitovský | github.com/igvisk",
            size=10,
            color="#4b5563",
            text_align=ft.TextAlign.CENTER,
        ),
    )


ft.run(main)