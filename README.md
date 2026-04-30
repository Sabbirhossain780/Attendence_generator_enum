# attendance-generator

**Automated attendance sheet & travelling bill generator for field survey teams**

Developed by BRAC Institute of Governance and Development (BIGD), BRAC University

---

## Overview

This tool generates professional attendance and travelling bill documents for field survey enumerators in seconds. It automates the creation of:

- **Attendance sheets** — One landscape A4 document per enumerator with:
  - Repeating header on every page (organization name, logo, enumerator details, survey period)
  - Attendance table (S/N, Date, Purpose, Data marker, Working place, Remarks)
  - Auto-classified days (Weekend, Holiday, Base work, Survey, Training, Travel, etc.)
  - Repeating footer with signature boxes (Enumerator, FA, RA, DA)
  - Summary page with survey day counts

- **QC workbook** — Single Excel file with:
  - Matrix sheet (enumerators × dates with color-coded day types)
  - Summary sheet (enumerator stats: data days, survey days, weekends, holidays, etc.)
  - Legend sheet (color meanings)

---

## Quick Start

### For Non-Technical Users (Jupyter) ⭐ Recommended

1. Install Jupyter if you don't have it:
   ```bash
   pip install jupyter
   ```

2. Open the tool notebook:
   ```bash
   jupyter notebook notebooks/usage_notebook.ipynb
   ```

3. **Cell 2**: Click "Run" (installs/updates the tool — safe to re-run anytime)

4. **Cell 3**: Click "Run" (a form appears)
   - Fill in your survey data file path
   - Click **Generate Attendance Sheets**
   - Done! Documents saved to your chosen folder

**No command-line experience needed.**

---

### For Terminal Users

```bash
attendance-gen
```

The tool asks questions one at a time. Press **Enter** to accept defaults shown in `[brackets]`.

---

## Installation

**First time:**
```bash
pip install git+https://github.com/Sabbirhossain780/attendance-generator.git
```

**Update to latest version:**
```bash
pip install --upgrade git+https://github.com/Sabbirhossain780/attendance-generator.git
```

---

## Usage Modes

### 1. Interactive Setup Wizard (Terminal)

```bash
attendance-gen
```

Guided step-by-step prompts:
- Input dataset path (.dta, .xlsx, .csv)
- Output folder
- Logo image (optional)
- Organization name (defaults: BIGD, BRAC University)
- Pre-survey blank days (default: 5)
- Weekend days (default: Friday)
- Holiday dates (e.g., "2025-12-25" or "2025-12-24:2025-12-26")

### 2. Interactive Form (Jupyter)

Same as terminal wizard, but in a web form. Open `notebooks/usage_notebook.ipynb`.

### 3. Command-Line Flags (Scripting)

```bash
attendance-gen --input data.dta --output ./output --logo logo.jpeg
```

**All flags:**
```bash
attendance-gen --help
```

**Common examples:**
```bash
# Basic usage
attendance-gen --input survey_data.xlsx

# With logo and custom organization
attendance-gen --input data.dta --logo bigd_logo.png \
  --org1 "My Organization" --org2 "My Division"

# Custom survey calendar
attendance-gen --input data.csv \
  --weekend "friday,saturday" \
  --holidays "2025-12-25, 2025-01-01" \
  --pre-survey-days 3

# Basework days (if applicable)
attendance-gen --input data.dta \
  --basework "2025-12-15:2025-12-17"

# Demo mode (first enumerator only, for testing)
attendance-gen --input data.dta --demo

# Show version
attendance-gen --version
```

---

## Input Data Format

Your dataset must have these columns (names are flexible, auto-detected):

| Column | Required | Description | Examples |
|--------|----------|-------------|----------|
| Enumerator ID | Yes | Unique identifier per enumerator | `3753`, `4059`, `emp001` |
| Enumerator Name | Yes | Full name | `Md Zubaer`, `Alice Khan` |
| Start Date | Yes | Survey start date | `2025-12-01`, `01/12/2025` |
| End Date | No | Survey end date (if different from start) | `2025-12-15` |
| Upazila | No | Working area/district (for "Working Place" column) | `Dhaka`, `Sylhet` |

**Supported file formats:**
- Stata: `.dta`
- Excel: `.xlsx`, `.xls`, `.xlsm`
- CSV: `.csv` (UTF-8 or Latin-1)

**Example CSV:**
```
enu_code,enu_name,startdate,enddate
3753,Md Zubaer,2025-12-01,2025-12-11
4059,Iqbal Hossain,2025-12-01,2025-12-10
```

---

## Output Files

All files saved to your chosen output folder:

| File | Format | Description |
|------|--------|-------------|
| `{ID}_{NAME}_attendance.docx` | Word | Attendance sheet (one per enumerator) |
| `_QC_Summary.xlsx` | Excel | QC workbook with matrix, summary, legend |

**Example filenames:**
- `3753_Md_Zubaer_attendance.docx`
- `4059_Iqbal_Hossain_attendance.docx`
- `_QC_Summary.xlsx`

---

## Document Contents

### Attendance Sheet (per enumerator)

**Page 1+: Attendance Table**
- Header: Organization logo (if provided), name, designation, period
- Table rows: One per calendar day from pre-survey through survey end
  - **S/N**: Serial number
  - **Date**: Day in "01 Jan 2025" format
  - **Purpose**: Auto-filled day type (Survey, Weekend, Holiday, Base work, Training, Travel, Office work, or blank)
  - **Data**: "Yes" if data was collected, blank otherwise
  - **Working Place**: Location (if provided in dataset)
  - **Remarks**: Blank for manual notes
- Footer: "Authorized by:" label + signature boxes (Enumerator, FA, RA, DA)

**Last page: Summary**
- Enumerator name & ID
- Period covered
- Pre-filled counts:
  - **Survey Days**: Days with data collected
  - All other counts blank (for manual fill)
- Same header/footer as attendance pages

### QC Workbook

**Sheet 1: Matrix**
- Rows: Enumerators
- Columns: Calendar dates
- Cells: Color-coded day type (Survey=green, Weekend=gray, Holiday=gray, Base work=blue, Training=yellow, Travel=light green, Blank=white)
- Frozen headers

**Sheet 2: Summary**
- Enumerator ID, Name, Period
- Data Days: Days with surveys marked "Yes"
- Survey Days, Training Days, Travel Days, Weekend Days, Base Work Days, Blank Days counts

**Sheet 3: Legend**
- Color meanings reference

---

## Configuration & Customization

### Weekend Days

Default: Friday

Examples:
```bash
--weekend "friday"              # Single day
--weekend "friday,saturday"     # Multiple days
--weekend "4"                   # By number (0=Mon, 6=Sun)
```

### Holiday Dates

Format: `YYYY-MM-DD` or date ranges with `:` separator

Examples:
```bash
--holidays "2025-12-25"                    # Single date
--holidays "2025-12-24:2025-12-26"         # Range
--holidays "2025-12-25, 2026-01-01"        # Multiple
```

### Base Work Days

Same format as holidays. Days marked "Base work" in Purpose column.

```bash
--basework "2025-12-10:2025-12-12"
```

### Pre-Survey Days

Blank rows added before first survey date (for manual fill-in).

```bash
--pre-survey-days 5     # Default
--pre-survey-days 3     # Custom
```

### Logo Image

JPEG or PNG image. Appears in header, top-left corner, on every page.

```bash
--logo path/to/logo.jpeg
```

### Organization Details

```bash
--org1 "BRAC Institute of Governance and Development"
--org2 "BRAC University"
--project "2025 Resilience Project"  # Optional subtitle
```

---

## Troubleshooting

### "File not found"
- Check the path to your data file
- Use full absolute path if relative path doesn't work:
  ```bash
  attendance-gen --input "C:\Users\YourName\Documents\data.xlsx"
  ```

### Column not detected
- Column names are case-insensitive and auto-matched (e.g., "enu_code" matches "Enumerator ID")
- If still not found, use `--help` to see expected column names, then rename your columns

### Dates not parsing
- Ensure dates are in a standard format: `YYYY-MM-DD`, `DD/MM/YYYY`, `MM/DD/YYYY`
- For Stata files: use `%td` or `%tC` date formats
- For Excel: use built-in date formatting

### Logo not showing
- File must exist and be JPEG or PNG
- Check the exact file path

### Unicode/encoding errors (especially on Windows)
- Use UTF-8 encoding for CSV files
- Tool auto-detects CSV encoding (UTF-8 → Latin-1 fallback)

---

## For Developers

**Install for development:**
```bash
pip install -e ".[dev]"
```

**Run tests:**
```bash
pytest tests/ -v
```

**Build from source:**
```bash
git clone https://github.com/Sabbirhossain780/attendance-generator.git
cd attendance-generator
pip install -e ".[dev]"
attendance-gen --version
```

---

## Updates

New versions released on GitHub. To update:

```bash
pip install --upgrade git+https://github.com/Sabbirhossain780/attendance-generator.git
```

Or in Jupyter: re-run Cell 2 of `usage_notebook.ipynb`.

---

## Support & Feedback

Issues or feature requests: [GitHub Issues](https://github.com/Sabbirhossain780/attendance-generator/issues)

---

## License

MIT License — free to use and modify.

---

**Built for non-technical field research staff. No manual memorization required.**
