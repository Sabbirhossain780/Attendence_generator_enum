import re
import os
import tempfile
import pandas as pd
import pytest
from attendance_generator.config import Config
from attendance_generator.pipeline import run
import attendance_generator


def test_run_creates_docx_files(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text(
        "enu_code,enu_name,startdate,enddate\n"
        "1,Alice,2025-12-01,2025-12-05\n"
    )
    out_dir = tmp_path / "output"

    cfg = Config(
        data_path=str(csv_file),
        out_dir=str(out_dir),
        n_pre_survey=1
    )
    run(cfg)

    files = os.listdir(out_dir)
    assert any(f.endswith(".docx") for f in files)
    assert "_QC_Summary.xlsx" in files


def test_run_demo_mode(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text(
        "enu_code,enu_name,startdate\n"
        "1,Alice,2025-12-01\n"
        "2,Bob,2025-12-02\n"
    )
    out_dir = tmp_path / "output"

    cfg = Config(
        data_path=str(csv_file),
        out_dir=str(out_dir),
        demo_mode=True
    )
    run(cfg)

    files = os.listdir(out_dir)
    docx_files = [f for f in files if f.endswith(".docx")]
    assert len(docx_files) == 1


def test_version_string_is_semver():
    pattern = r"\d+\.\d+\.\d+"
    assert re.match(pattern, attendance_generator.__version__)


def test_run_prints_version(tmp_path, capsys):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("enu_code,enu_name,startdate\n1,Alice,2025-12-01\n")
    out_dir = tmp_path / "output"

    cfg = Config(data_path=str(csv_file), out_dir=str(out_dir))
    run(cfg)

    captured = capsys.readouterr()
    assert "attendance-generator v" in captured.out
