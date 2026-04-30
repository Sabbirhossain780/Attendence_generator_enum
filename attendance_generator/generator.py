import os
from docx import Document
from docx.shared import Emu
from docx.enum.section import WD_ORIENT

from attendance_generator.config import Config
from attendance_generator.builders import (
    dxa_emu, PAGE_W_DXA, PAGE_H_DXA, MARGIN_DXA,
    register_logo, build_header, build_footer,
    build_attendance_table, build_summary_table, fix_zoom
)


def generate_doc(payload: dict, cfg: Config, out_dir: str) -> str:
    enu_id       = payload["enu_id"]
    enu_name     = payload["enu_name"]
    period_start = payload["period_start"]
    period_end   = payload["period_end"]
    rows         = payload["rows"]

    doc = Document()
    fix_zoom(doc)

    sec = doc.sections[0]
    sec.orientation   = WD_ORIENT.LANDSCAPE
    sec.page_width    = Emu(dxa_emu(PAGE_W_DXA))
    sec.page_height   = Emu(dxa_emu(PAGE_H_DXA))
    sec.top_margin    = Emu(dxa_emu(MARGIN_DXA))
    sec.bottom_margin = Emu(dxa_emu(MARGIN_DXA))
    sec.left_margin   = Emu(dxa_emu(MARGIN_DXA))
    sec.right_margin  = Emu(dxa_emu(MARGIN_DXA))

    logo_rId = register_logo(sec, cfg.logo_path)

    build_header(sec, logo_rId, enu_name, enu_id, period_start, period_end, cfg.org_line1, cfg.org_line2)
    build_footer(sec)

    build_attendance_table(doc, rows)

    doc.add_page_break()
    survey_days_count = sum(1 for r in rows if r["has_data"] == "Yes")
    build_summary_table(doc, enu_name, enu_id, survey_days_count)

    safe = enu_name.replace(" ","_").replace("/","_")
    fname = f"{enu_id}_{safe}_attendance.docx"
    doc.save(os.path.join(out_dir, fname))
    return fname
