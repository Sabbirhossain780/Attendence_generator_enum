from datetime import date
import pytest
from attendance_generator.helpers import (
    parse_dates, parse_weekend_days, find_col, make_classifier
)
import pandas as pd


def test_parse_dates_single():
    result = parse_dates("2025-12-25")
    assert result == [date(2025, 12, 25)]


def test_parse_dates_range():
    result = parse_dates("2025-12-01:2025-12-03")
    assert result == [date(2025, 12, 1), date(2025, 12, 2), date(2025, 12, 3)]


def test_parse_dates_empty():
    result = parse_dates("")
    assert result == []


def test_parse_weekend_days_friday():
    result = parse_weekend_days("friday")
    assert result == {4}


def test_parse_weekend_days_multi():
    result = parse_weekend_days("friday,saturday")
    assert result == {4, 5}


def test_parse_weekend_days_default():
    result = parse_weekend_days("unknown")
    assert result == {4}


def test_find_col_exact():
    df = pd.DataFrame({"enu_code": [1], "name": ["test"]})
    result = find_col(df, ["enu_code"], "Enumerator ID")
    assert result == "enu_code"


def test_find_col_case_insensitive():
    df = pd.DataFrame({"Enumerator ID": [1]})
    result = find_col(df, ["enumerator id"], "ID")
    assert result == "Enumerator ID"


def test_find_col_missing_required():
    df = pd.DataFrame({"other": [1]})
    with pytest.raises(ValueError):
        find_col(df, ["missing"], "Test", required=True)


def test_find_col_missing_optional():
    df = pd.DataFrame({"other": [1]})
    result = find_col(df, ["missing"], "Test", required=False)
    assert result is None


def test_classifier_weekend():
    weekend_days = {4}  # Friday
    classify = make_classifier(weekend_days, set(), set())
    result = classify(date(2025, 12, 12), False)  # Friday
    assert result == "Weekend"


def test_classifier_holiday():
    holiday_dates = {date(2025, 12, 25)}
    classify = make_classifier(set(), holiday_dates, set())
    result = classify(date(2025, 12, 25), False)
    assert result == "Holiday"


def test_classifier_basework():
    basework_dates = {date(2025, 12, 20)}
    classify = make_classifier(set(), set(), basework_dates)
    result = classify(date(2025, 12, 20), False)
    assert result == "Base work"


def test_classifier_survey():
    classify = make_classifier(set(), set(), set())
    result = classify(date(2025, 12, 10), True)
    assert result == "Survey"


def test_classifier_blank():
    classify = make_classifier(set(), set(), set())
    result = classify(date(2025, 12, 10), False)
    assert result == ""
