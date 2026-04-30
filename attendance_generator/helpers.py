from datetime import timedelta
import pandas as pd


def parse_dates(raw):
    out = []
    if not raw or not raw.strip(): return out
    for part in raw.split(","):
        part = part.strip()
        if not part: continue
        if ":" in part:
            try:
                a, b = [pd.to_datetime(s.strip()).date() for s in part.split(":",1)]
                d = a
                while d <= b: out.append(d); d += timedelta(days=1)
            except: print(f"  ⚠  Cannot parse range '{part}' — skipped.")
        else:
            try: out.append(pd.to_datetime(part).date())
            except: print(f"  ⚠  Cannot parse date '{part}' — skipped.")
    return out


def parse_weekend_days(raw):
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
        else: print(f"  ⚠  Unknown day '{p}' — skipped.")
    return days or {4}


def find_col(df, candidates, label, required=True):
    lower_map = {c.lower(): c for c in df.columns}
    for c in candidates:
        if c in df.columns: return c
        if c.lower() in lower_map: return lower_map[c.lower()]
        hits = [orig for lo,orig in lower_map.items() if c.lower() in lo]
        if len(hits)==1: return hits[0]
    if not required: return None
    raise ValueError(
        f"Cannot find column for '{label}'.\n"
        f"Available: {list(df.columns)}\n"
        f"Set COL_OVERRIDE['{label}'] to the correct name."
    )


def make_classifier(weekend_days, holiday_dates, basework_dates):
    def classify(d, is_survey):
        if d.weekday() in weekend_days: return "Weekend"
        if d in holiday_dates:          return "Holiday"
        if d in basework_dates:         return "Base work"
        if is_survey:                   return "Survey"
        return ""
    return classify
