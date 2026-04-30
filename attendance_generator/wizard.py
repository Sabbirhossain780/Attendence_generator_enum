import os
from attendance_generator.config import Config


def _in_jupyter() -> bool:
    try:
        from IPython import get_ipython
        shell = get_ipython()
        return shell is not None and hasattr(shell, "kernel")
    except ImportError:
        return False


def run_wizard() -> Config:
    if _in_jupyter():
        return _jupyter_wizard()
    else:
        return _terminal_wizard()


def _terminal_wizard() -> Config:
    print()
    print("="*62)
    print("Attendance Sheet Generator - Setup Wizard")
    print("BRAC Institute of Governance and Development")
    print("="*62)
    print()
    print("Answer each question and press Enter.")
    print("Press Enter alone to accept the default shown in [brackets].")
    print()

    data_path = ""
    while not data_path or not os.path.exists(data_path):
        print("-- Step 1 of 8 : Input file " + "-"*39)
        inp = input("Path to your survey dataset (.dta / .xlsx / .csv): ").strip().strip('"\'')
        if inp:
            data_path = inp
            if not os.path.exists(data_path):
                print("  [!] File not found. Please check the path and try again.")
                data_path = ""
        else:
            print("  [!] File path required.")

    print()
    print("-- Step 2 of 8 : Output folder " + "-"*36)
    out_dir = input("Output folder [./attendance_output]: ").strip() or "./attendance_output"

    print()
    print("-- Step 3 of 8 : Logo " + "-"*45)
    logo_path = input("Logo image path (leave blank to skip): ").strip().strip('"\'')
    if logo_path and not os.path.exists(logo_path):
        print("  [!] Logo file not found - continuing without logo.")
        logo_path = ""

    print()
    print("-- Step 4 of 8 : Organization " + "-"*37)
    org_line1 = input("Organisation line 1 [BRAC Institute of Governance and Development]: ").strip() or \
                "BRAC Institute of Governance and Development"
    org_line2 = input("Organisation line 2 [BRAC University]: ").strip() or "BRAC University"

    print()
    print("-- Step 5 of 8 : Pre-survey days " + "-"*34)
    while True:
        n_pre_survey_str = input("Days to include BEFORE survey start (blank rows for manual fill) [5]: ").strip()
        if not n_pre_survey_str:
            n_pre_survey = 5
            break
        try:
            n_pre_survey = int(n_pre_survey_str)
            if n_pre_survey >= 0:
                break
        except ValueError:
            pass
        print("  [!] Please enter a whole number (e.g. 5).")

    print()
    print("-- Step 6 of 8 : Weekend days " + "-"*37)
    weekend_days_raw = input("Weekend days [friday]:\n(e.g. \"friday\"  or  \"friday,saturday\"): ").strip() or "friday"

    print()
    print("-- Step 7 of 8 : Public holidays " + "-"*34)
    holiday_dates_raw = input("Public holiday dates to mark (leave blank if none) []:\n(e.g. \"2025-12-25\"  or  \"2025-12-24:2025-12-26, 2025-01-01\"): ").strip()

    print()
    print("-- Summary " + "-"*57)
    print(f"  Input file   : {data_path}")
    print(f"  Output folder: {out_dir}")
    print(f"  Logo         : {logo_path if logo_path else '(none)'}")
    print(f"  Org line 1   : {org_line1}")
    print(f"  Org line 2   : {org_line2}")
    print(f"  Pre-survey   : {n_pre_survey} days")
    print(f"  Weekends     : {weekend_days_raw}")
    print(f"  Holidays     : {holiday_dates_raw if holiday_dates_raw else '(none)'}")
    print("-"*62)
    input("Press Enter to generate, or Ctrl+C to cancel.")

    return Config(
        data_path=data_path,
        out_dir=out_dir,
        logo_path=logo_path,
        org_line1=org_line1,
        org_line2=org_line2,
        n_pre_survey=n_pre_survey,
        weekend_days_raw=weekend_days_raw,
        holiday_dates_raw=holiday_dates_raw,
    )


def _jupyter_wizard() -> Config:
    try:
        import ipywidgets as widgets
        from IPython.display import display
    except ImportError:
        print("[!] ipywidgets not installed - using text prompts instead.")
        print("   To get the form-based UI: pip install ipywidgets")
        return _terminal_wizard()

    header = widgets.HTML(
        "<h3>Attendance Sheet Generator</h3>"
        "<p style='color:gray'>BRAC Institute of Governance and Development<br>"
        "Fill in the fields below and click Generate.</p>"
        "<p><b>*</b> = required</p>"
    )

    data_path_widget = widgets.Text(placeholder="Path to .dta / .xlsx / .csv", description="Input file *", style={'description_width': '140px'})
    out_dir_widget = widgets.Text(value="./attendance_output", description="Output folder", style={'description_width': '140px'})
    logo_widget = widgets.Text(placeholder="Leave blank for no logo", description="Logo image", style={'description_width': '140px'})
    org1_widget = widgets.Text(value="BRAC Institute of Governance and Development", description="Org line 1", style={'description_width': '140px'})
    org2_widget = widgets.Text(value="BRAC University", description="Org line 2", style={'description_width': '140px'})
    pre_survey_widget = widgets.BoundedIntText(value=5, min=0, max=365, description="Pre-survey days", style={'description_width': '140px'})
    weekend_widget = widgets.Text(value="friday", description="Weekends", style={'description_width': '140px'})
    holidays_widget = widgets.Text(placeholder='e.g. "2025-12-25" or leave blank', description="Holidays", style={'description_width': '140px'})
    generate_btn = widgets.Button(description="✓ Generate Attendance Sheets", button_style="success")
    status_out = widgets.Output()

    form = widgets.VBox([
        header,
        data_path_widget, out_dir_widget, logo_widget,
        org1_widget, org2_widget,
        pre_survey_widget, weekend_widget, holidays_widget,
        generate_btn, status_out
    ])

    def on_generate_click(b):
        status_out.clear_output()
        if not data_path_widget.value:
            with status_out:
                print("[!] Input file is required.")
            return
        if not os.path.exists(data_path_widget.value):
            with status_out:
                print(f"[!] File not found: {data_path_widget.value}")
            return

        cfg = Config(
            data_path=data_path_widget.value,
            out_dir=out_dir_widget.value,
            logo_path=logo_widget.value,
            org_line1=org1_widget.value,
            org_line2=org2_widget.value,
            n_pre_survey=pre_survey_widget.value,
            weekend_days_raw=weekend_widget.value,
            holiday_dates_raw=holidays_widget.value,
        )

        with status_out:
            print("[*] Generating...")
            try:
                from attendance_generator.pipeline import run
                run(cfg)
                print("\n[OK] Done!")
            except Exception as e:
                print(f"\n[ERROR] Error: {e}")

    generate_btn.on_click(on_generate_click)
    display(form)
    return Config()
