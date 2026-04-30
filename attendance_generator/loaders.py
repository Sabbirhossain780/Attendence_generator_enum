import os
from datetime import timedelta
import pandas as pd

from attendance_generator.config import Config
from attendance_generator.helpers import find_col, make_classifier, parse_dates


def load_dataframe(data_path: str) -> pd.DataFrame:
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Not found: {data_path}")

    ext = os.path.splitext(data_path)[1].lower()

    if ext == ".dta":
        reader = pd.io.stata.StataReader(data_path)
        df = reader.read(convert_dates=True, convert_categoricals=True)
        for col in df.select_dtypes(['category']).columns:
            df[col] = df[col].astype(str).replace({'nan': pd.NA})

    elif ext in (".xlsx", ".xls", ".xlsm"):
        df = pd.read_excel(data_path)

    elif ext == ".csv":
        try:
            df = pd.read_csv(data_path, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(data_path, encoding="latin-1")

    else:
        raise ValueError(
            f"Unsupported file extension '{ext}'.\n"
            f"Supported: .dta  .xlsx  .xls  .xlsm  .csv"
        )

    return df


def _parse_date_col(series):
    if pd.api.types.is_datetime64_any_dtype(series):
        return series
    if pd.api.types.is_integer_dtype(series) or pd.api.types.is_float_dtype(series):
        try:
            converted = pd.to_datetime(series, unit="D", origin="1960-01-01", errors="coerce")
            valid = converted.dropna()
            if len(valid) > 0:
                in_range = ((valid.dt.year >= 1990) & (valid.dt.year <= 2100)).mean()
                if in_range >= 0.5:
                    return converted
        except Exception:
            pass
    return pd.to_datetime(series, errors="coerce")


def build_payloads(df: pd.DataFrame, cfg: Config) -> list:
    def resolve(label, candidates, required=True):
        if cfg.col_override.get(label) is not None and cfg.col_override[label] != "":
            c = cfg.col_override[label]
            if c not in df.columns: raise ValueError(f"Override '{c}' not found.")
            return c
        if cfg.col_override.get(label) == "":
            return None
        return find_col(df, candidates, label, required)

    col_id      = resolve("Enumerator ID",   ["enu_code","enumerator_id","enum_id","enu_id","EnumID"])
    col_name    = resolve("Enumerator Name", ["enu_name","enumerator_name","enum_name","enu_nm","EnumName"])
    col_start   = resolve("Start Date",      ["startdate","start_date","survey_day","survey_date","date"])
    col_end     = resolve("End Date",        ["enddate","end_date","finishdate","finish_date","endtime","end_time"], required=False)
    col_upazila = resolve("Upazila",         ["upazila","upazilla"], required=False)

    df[col_start] = _parse_date_col(df[col_start])
    bad = df[col_start].isna().sum()
    if bad: print(f"  ⚠  {bad} rows with unparseable start date dropped.")
    df = df.dropna(subset=[col_start])

    if col_end:
        df[col_end] = _parse_date_col(df[col_end])
        mask_bad = df[col_end].isna() | (df[col_end].dt.date < df[col_start].dt.date)
        if mask_bad.sum():
            print(f"  ⚠  {mask_bad.sum()} rows with missing/invalid end date — using start date for those.")
        df.loc[mask_bad, col_end] = df.loc[mask_bad, col_start]

    id_names = df.groupby(col_id)[col_name].apply(lambda x: set(x.dropna().unique()))
    dups = {k:v for k,v in id_names.items() if len(v)>1}
    if dups:
        print("⚠  Duplicate ID with multiple name spellings (using most frequent):")
        for eid,names in dups.items(): print(f"   {eid} → {names}")
        freq = df.groupby(col_id)[col_name].agg(lambda x: x.value_counts().index[0])
        df[col_name] = df[col_id].map(freq)

    weekend_days   = _parse_weekend_days_set(cfg.weekend_days_raw)
    holiday_dates  = set(parse_dates(cfg.holiday_dates_raw))
    basework_dates = set(parse_dates(cfg.basework_dates_raw))
    classify = make_classifier(weekend_days, holiday_dates, basework_dates)

    work_df = df[[col_id, col_name, col_start] + ([col_end] if col_end else [])].copy()
    work_df["_start"] = work_df[col_start].dt.date
    work_df["_end"]   = work_df[col_end].dt.date if col_end else work_df[col_start].dt.date

    if col_upazila:
        upz = df[[col_id, col_start, col_upazila]].copy()
        upz["_date"] = upz[col_start].dt.date
        upz = upz.dropna(subset=[col_upazila])
        place_map = (upz.groupby([col_id,"_date"])[col_upazila]
                     .agg(lambda x: x.value_counts().index[0] if len(x) else ""))
    else:
        place_map = None

    def expand_dates(grp):
        dates = set()
        for _, r in grp.iterrows():
            d = r["_start"]
            while d <= r["_end"]:
                dates.add(d)
                d += timedelta(days=1)
        return dates

    grouped = (
        work_df.groupby([col_id, col_name], group_keys=False)
        .apply(expand_dates, include_groups=False)
        .reset_index()
        .rename(columns={0: "data_dates"})
    )

    if cfg.demo_mode:
        grouped = grouped.sort_values(col_name).head(1)

    payloads = []

    for _, row in grouped.iterrows():
        enu_id      = str(row[col_id]).strip()
        enu_name    = str(row[col_name]).strip()
        data_dates  = row["data_dates"]

        span_start = min(data_dates)
        span_end   = max(data_dates)

        rows, sn = [], 1

        if cfg.n_pre_survey > 0:
            d = span_start - timedelta(days=cfg.n_pre_survey)
            while d < span_start:
                rows.append({"sn":sn, "date":d.strftime("%d %b %Y"),
                             "purpose":"", "has_data":"", "working_place":""})
                sn += 1; d += timedelta(days=1)

        d = span_start
        while d <= span_end:
            is_survey = d in data_dates
            wp = ""
            if place_map is not None and is_survey:
                try: wp = str(place_map.loc[(row[col_id], d)])
                except: wp = ""
            rows.append({
                "sn": sn,
                "date": d.strftime("%d %b %Y"),
                "purpose": classify(d, is_survey),
                "has_data": "Yes" if is_survey else "",
                "working_place": wp,
            })
            sn += 1; d += timedelta(days=1)

        for _ in range(5):
            rows.append({"sn":"","date":"","purpose":"","has_data":"","working_place":""})

        p_start = (span_start - timedelta(days=cfg.n_pre_survey)).strftime("%d %b %Y") \
                  if cfg.n_pre_survey > 0 else span_start.strftime("%d %b %Y")

        payloads.append({
            "enu_id": enu_id, "enu_name": enu_name,
            "period_start": p_start, "period_end": span_end.strftime("%d %b %Y"),
            "rows": rows,
        })

    return payloads


def _parse_weekend_days_set(raw):
    mapping = {
        "monday":0,"mon":0,"0":0,"tuesday":1,"tue":1,"1":1,
        "wednesday":2,"wed":2,"2":2,"thursday":3,"thu":3,"3":3,
        "friday":4,"fri":4,"4":4,"saturday":5,"sat":5,"5":5,
        "sunday":6,"sun":6,"6":6,
    }
    days = set()
    for p in raw.lower().split(","):
        p = p.strip()
        if p in mapping: days.add(mapping[p])
    return days or {4}
