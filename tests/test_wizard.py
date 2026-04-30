import pytest
import os
import tempfile
import pandas as pd
from unittest.mock import patch
from attendance_generator.wizard import _terminal_wizard


def test_wizard_terminal_accepts_defaults(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("enu_code,enu_name,startdate\n1,Alice,2025-12-01\n")

    inputs = iter([str(csv_file), "", "", "", "", "5", "friday", "", ""])
    with patch("builtins.input", side_effect=lambda _="": next(inputs)):
        cfg = _terminal_wizard()

    assert cfg.data_path == str(csv_file)
    assert cfg.out_dir == "./attendance_output"
    assert cfg.n_pre_survey == 5
    assert cfg.org_line1 == "BRAC Institute of Governance and Development"


def test_wizard_terminal_rejects_missing_file(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("enu_code,enu_name,startdate\n1,Alice,2025-12-01\n")

    inputs = iter(["/nonexistent", str(csv_file), "", "", "", "", "5", "friday", "", ""])
    with patch("builtins.input", side_effect=lambda _="": next(inputs)):
        cfg = _terminal_wizard()

    assert cfg.data_path == str(csv_file)


def test_wizard_terminal_rejects_bad_pre_survey_days(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("enu_code,enu_name,startdate\n1,Alice,2025-12-01\n")

    inputs = iter([str(csv_file), "", "", "", "", "abc", "3", "friday", "", ""])
    with patch("builtins.input", side_effect=lambda _="": next(inputs)):
        cfg = _terminal_wizard()

    assert cfg.n_pre_survey == 3


def test_wizard_strips_quotes_from_path(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("enu_code,enu_name,startdate\n1,Alice,2025-12-01\n")

    quoted = f'"{csv_file}"'
    inputs = iter([quoted, "", "", "", "", "5", "friday", "", ""])
    with patch("builtins.input", side_effect=lambda _="": next(inputs)):
        cfg = _terminal_wizard()

    assert cfg.data_path == str(csv_file)
