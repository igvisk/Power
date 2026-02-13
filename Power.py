import flet as ft
from logic import calculate_power

VERSION = "v1.3b"


def main(page: ft.Page):
    # --- WINDOW ---
    page.title = f"Power Calculator {VERSION}"
    page.window_width = 420
    page.window_height = 560
    page.padding = 5
    page.theme_mode = ft.ThemeMode.LIGHT
    
    page.bgcolor = "#fffafa"

    # # --- APP BAR ---     musi byt inak je uplne hore nalepena a zacina apka od hrany     ---vyriesene cez safeArea v page.add
    # page.appbar = ft.AppBar(
    #     title=ft.Text(" "),
    #     center_title=True,
    # )

    # --- INPUT STYLE ---
    input_style = dict(
        dense=True,
        text_size=13,
        text_align=ft.TextAlign.CENTER,
    )

    # --- INPUTS ---
    current = ft.TextField(label="I (A)", value="16", expand=True, keyboard_type=ft.KeyboardType.NUMBER_WITH_OPTIONS(decimal=True),  **input_style)
    voltage = ft.TextField(label="U (V)", value="230", expand=True, keyboard_type=ft.KeyboardType.NUMBER_WITH_OPTIONS(decimal=True), **input_style)
    pf = ft.TextField(label="cos φ", value="0.98", keyboard_type=ft.KeyboardType.NUMBER_WITH_OPTIONS(decimal=True), expand=True, **input_style)

    inputs_row = ft.Row(
        width=300,
        spacing=6,
        controls=[current, voltage, pf],
    )

    # --- PHASE SELECTOR ---
    selected_phase = 1

    def set_phase(e):
        nonlocal selected_phase
        selected_phase = int(e.control.data)

        # vizuálne zvýraznenie
        for btn in phase_buttons.controls:
            btn.style = None  # reset - not helped 

        for btn in phase_buttons.controls:
            if btn.data == selected_phase:
                btn.style = ft.ButtonStyle(
                    bgcolor=ft.Colors.BLUE_400,
                    color=ft.Colors.WHITE,
                )
            else:
                btn.style = ft.ButtonStyle(
                    bgcolor=ft.Colors.GREY_200,
                    color=ft.Colors.BLACK,
                )

        # automatická zmena napätia
        try:
            current_voltage = float(voltage.value.replace(",", "."))

            if selected_phase in [2, 3] and current_voltage == 230:
                voltage.value = "400"

            elif selected_phase == 1 and current_voltage == 400:
                voltage.value = "230"

        except:
            pass

        page.update()

    phase_buttons = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
        controls=[
            ft.Button("1", width=90, data=1, on_click=set_phase),
            ft.Button("2", width=90, data=2, on_click=set_phase),
            ft.Button("3", width=90, data=3, on_click=set_phase),
        ],
    )

    # default zvýraznenie
    phase_buttons.controls[0].style = ft.ButtonStyle(
        bgcolor=ft.Colors.BLUE_400,
        color=ft.Colors.WHITE,
    )

    # --- RESULT TEXTS ---
    p_text = ft.Text(size=14, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    s_text = ft.Text(size=14, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    q_text = ft.Text(size=14, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    result_row = ft.Row(
        width=300,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[ft.Text("Active (W)", size=12, opacity=0.7), p_text],
            ),
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[ft.Text("Apparent (VA)", size=12, opacity=0.7), s_text],
            ),
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[ft.Text("Reactive (VAr)", size=12, opacity=0.7), q_text],
            ),
        ],
    )

    result_box = ft.Container(
        width=300,
        padding=6,
        border=ft.Border.all(1, ft.Colors.GREY_400),
        border_radius=8,
        content=result_row,
    )

    # --- CALCULATE ---
    def on_calculate(e):
        try:
            entered_current = float(current.value.replace(",", "."))
            entered_voltage = float(voltage.value.replace(",", "."))
            entered_pf = float(pf.value.replace(",", "."))

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

        except Exception as err:
            p_text.value = "❌"
            s_text.value = str(err)
            q_text.value = ""

        page.update()

    calculate_btn = ft.Button(
        "Calculate power",
        width=300,
        on_click=on_calculate,
    )

    footer = ft.Container(
        padding=10,
        content=ft.Text(
            f"Power Calculator {VERSION}  |  ©2026 Igor Vitovský  |  github.com/igvisk",
            size=10,
            opacity=0.6,
            text_align=ft.TextAlign.CENTER,
        ),
    )

    page.add(
    ft.SafeArea(   # 👈 toto vyrieši horný okraj
        expand=True,
        content=ft.Container(
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                width=320,
                spacing=14,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("⚡ Power Calculator",
                            size=26,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER),
                    result_box,
                    inputs_row,
                    ft.Text("Number of phases", size=12, opacity=0.7),
                    phase_buttons,
                    calculate_btn,
                ],
            ),
        ),
    ),
    footer,
    )


ft.run(main)
