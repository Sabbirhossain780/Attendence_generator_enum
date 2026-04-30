from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class Config:
    # ── File paths ─────────────────────────────────────────────────────────
    data_path: str = ""
    logo_path: str = ""
    out_dir: str = "./attendance_output"

    # ── Organisation identity ──────────────────────────────────────────────
    org_line1: str = "BRAC Institute of Governance and Development"
    org_line2: str = "BRAC University"
    project_name: str = ""

    # ── Survey calendar ────────────────────────────────────────────────────
    weekend_days_raw: str = "friday"
    holiday_dates_raw: str = ""
    basework_dates_raw: str = ""
    n_pre_survey: int = 5

    # ── Column mapping overrides ───────────────────────────────────────────
    # Keys: "Enumerator ID", "Enumerator Name", "Start Date", "End Date", "Upazila"
    # None → auto-detect | "" → disable | "col_name" → use that column
    col_override: Dict[str, Optional[str]] = field(default_factory=dict)

    # ── Run control ────────────────────────────────────────────────────────
    demo_mode: bool = False
