import os
import attendance_generator
from attendance_generator.config import Config
from attendance_generator.loaders import load_dataframe, build_payloads
from attendance_generator.generator import generate_doc
from attendance_generator.excel_qc import build_qc_workbook


def run(cfg: Config) -> None:
    print(f"attendance-generator v{attendance_generator.__version__}")
    df = load_dataframe(cfg.data_path)
    payloads = build_payloads(df, cfg)
    os.makedirs(cfg.out_dir, exist_ok=True)

    print(f"Generating {len(payloads)} document(s)...")
    for i, payload in enumerate(payloads, 1):
        fname = generate_doc(payload, cfg, cfg.out_dir)
        data_yes = sum(1 for r in payload["rows"] if r["has_data"] == "Yes")
        print(f"  [*] {i}/{len(payloads)}  {payload['enu_name']:<25} ({data_yes} data days)")

    qc_path = build_qc_workbook(payloads, cfg.out_dir)
    print(f"\n  [*] QC workbook -> {qc_path}")
    print(f"\n[Done] {len(payloads)} doc(s) saved to: {os.path.abspath(cfg.out_dir)}")
