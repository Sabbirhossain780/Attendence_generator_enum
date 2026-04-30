# attendance-generator

Automated attendance sheet & travelling bill generator for BRAC field survey teams.
Developed at BRAC Institute of Governance and Development (BIGD).

---

## For Jupyter users (recommended for non-technical staff)

1. Open `notebooks/usage_notebook.ipynb` in Jupyter
2. Run **Cell 2** (installs / updates the tool — safe to re-run anytime)
3. Run **Cell 3** (a form appears — fill it in and click **Generate**)

That's it. No commands to memorise.

---

## For terminal users

Just run:

    attendance-gen

The tool will ask you questions one at a time. Press Enter to accept defaults.

---

## Installation

    pip install git+https://github.com/Sabbirhossain780/attendance-generator.git

## Update to latest version

    pip install --upgrade git+https://github.com/Sabbirhossain780/attendance-generator.git

---

## Advanced: flags for scripting / automation

    attendance-gen --input data.dta --output ./output --logo logo.jpeg

    attendance-gen --help    ← see all available flags

    attendance-gen --version

---

## Supported input formats

| Format | Extension |
|--------|-----------|
| Stata  | .dta      |
| Excel  | .xlsx, .xls, .xlsm |
| CSV    | .csv      |

## Output

| File | Description |
|------|-------------|
| `{id}_{name}_attendance.docx` | One per enumerator |
| `_QC_Summary.xlsx`            | Matrix + Summary + Legend sheets |
