import sys
import argparse
import attendance_generator
from attendance_generator.config import Config
from attendance_generator.pipeline import run
from attendance_generator.wizard import run_wizard


def main():
    if len(sys.argv) == 1:
        cfg = run_wizard()
        if cfg.data_path:
            run(cfg)
        return

    parser = argparse.ArgumentParser(
        prog="attendance-gen",
        description=(
            "Generate attendance & travelling bill .docx sheets.\n\n"
            "  Run with no arguments for the interactive setup wizard:\n"
            "    attendance-gen\n\n"
            "  Or supply flags directly for scripting:"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version",
                        version=f"attendance-gen {attendance_generator.__version__}")
    parser.add_argument("--input",  "-i", required=True,
                        help="Path to survey dataset (.dta / .xlsx / .csv)")
    parser.add_argument("--output", "-o", default="./attendance_output",
                        help="Output directory  [./attendance_output]")
    parser.add_argument("--logo",   default="",
                        help="Path to logo image (JPEG or PNG)")
    parser.add_argument("--org1",   default="BRAC Institute of Governance and Development",
                        help="Organisation header line 1")
    parser.add_argument("--org2",   default="BRAC University",
                        help="Organisation header line 2")
    parser.add_argument("--project", default="",
                        help="Optional project name note in header")
    parser.add_argument("--weekend", default="friday",
                        help='Weekend days  [friday]  e.g. "friday,saturday"')
    parser.add_argument("--holidays", default="",
                        help='Holiday dates  e.g. "2025-12-25" or "2025-12-24:2025-12-26"')
    parser.add_argument("--basework", default="",
                        help="Base-work dates (same format as --holidays)")
    parser.add_argument("--pre-survey-days", type=int, default=5, dest="n_pre_survey",
                        help="Days to include before survey start  [5]")
    parser.add_argument("--demo", action="store_true", default=False,
                        help="Process first enumerator only (for testing)")

    args = parser.parse_args()
    cfg = Config(
        data_path          = args.input,
        out_dir            = args.output,
        logo_path          = args.logo,
        org_line1          = args.org1,
        org_line2          = args.org2,
        project_name       = args.project,
        weekend_days_raw   = args.weekend,
        holiday_dates_raw  = args.holidays,
        basework_dates_raw = args.basework,
        n_pre_survey       = args.n_pre_survey,
        demo_mode          = args.demo,
    )
    run(cfg)


if __name__ == "__main__":
    main()
