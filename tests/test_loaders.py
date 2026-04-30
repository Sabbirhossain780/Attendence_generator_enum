import pytest
import os
import tempfile
import pandas as pd
from attendance_generator.loaders import load_dataframe, build_payloads
from attendance_generator.config import Config


def test_load_csv(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("enu_code,enu_name,startdate\n1,Alice,2025-12-01\n")

    df = load_dataframe(str(csv_file))
    assert len(df) == 1
    assert "enu_code" in df.columns


def test_load_unsupported_extension(tmp_path):
    bad_file = tmp_path / "test.json"
    bad_file.write_text("{}")

    with pytest.raises(ValueError):
        load_dataframe(str(bad_file))


def test_load_missing_file():
    with pytest.raises(FileNotFoundError):
        load_dataframe("/nonexistent/path.csv")


def test_build_payloads_basic(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "enu_code,enu_name,startdate,enddate\n"
        "1,Alice,2025-12-01,2025-12-03\n"
        "2,Bob,2025-12-01,2025-12-02\n"
    )

    df = load_dataframe(str(csv_file))
    cfg = Config(n_pre_survey=0)
    payloads = build_payloads(df, cfg)

    assert len(payloads) == 2
    assert payloads[0]["enu_name"] == "Alice"
    assert payloads[1]["enu_name"] == "Bob"


def test_build_payloads_demo_mode(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "enu_code,enu_name,startdate\n"
        "1,Alice,2025-12-01\n"
        "2,Bob,2025-12-02\n"
    )

    df = load_dataframe(str(csv_file))
    cfg = Config(demo_mode=True, n_pre_survey=0)
    payloads = build_payloads(df, cfg)

    assert len(payloads) == 1


def test_build_payloads_pre_survey(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "enu_code,enu_name,startdate\n"
        "1,Alice,2025-12-05\n"
    )

    df = load_dataframe(str(csv_file))
    cfg = Config(n_pre_survey=3)
    payloads = build_payloads(df, cfg)

    assert len(payloads) == 1
    blank_rows = [r for r in payloads[0]["rows"] if not r["date"]]
    assert len(blank_rows) == 5
