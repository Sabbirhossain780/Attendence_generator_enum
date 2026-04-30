# Attendance Sheet Generator — User Manual

**BRAC Institute of Governance and Development (BIGD)**

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Installation](#installation)
3. [Step-by-Step Guide](#step-by-step-guide)
4. [Input Data Preparation](#input-data-preparation)
5. [Output Files Explained](#output-files-explained)
6. [Calendar Customization](#calendar-customization)
7. [Frequently Asked Questions](#frequently-asked-questions)
8. [Troubleshooting](#troubleshooting)
9. [Tips & Best Practices](#tips--best-practices)

---

## Getting Started

This tool generates **professional attendance sheets** and **QC workbooks** for field survey enumerators automatically.

**What it does:**
- Takes your survey dataset (Excel, Stata, or CSV)
- Creates one Word document per enumerator with:
  - Attendance table (dates, purposes, data markers, signatures)
  - Repeating headers/footers on every page
  - Auto-classified days (Weekends, Holidays, Surveys, etc.)
  - Summary page with day counts
- Creates an Excel QC workbook with:
  - Color-coded matrix of all enumerators and dates
  - Summary statistics
  - Legend

**Target audience:** Non-technical field research staff. You can use it without opening a terminal.

---

## Installation

### Option 1: First-Time Installation

**On Windows, Mac, or Linux:**

1. Open **Command Prompt** (Windows) or **Terminal** (Mac/Linux)

2. Copy and paste this command:
   ```
   pip install git+https://github.com/Sabbirhossain780/attendance-generator.git
   ```

3. Press **Enter** and wait for "Successfully installed..."

### Option 2: Using Jupyter Notebook (Recommended for Non-Technical Users)

1. Install Jupyter:
   ```
   pip install jupyter
   ```

2. Download or clone the tool
3. Open the provided `usage_notebook.ipynb` in Jupyter
4. Click **Run** on Cell 2 (automatic installation)

### Verify Installation

Open Command Prompt/Terminal and type:
```
attendance-gen --version
```

You should see: `attendance-gen 1.0.0`

---

## Step-by-Step Guide

### Using the Jupyter Form (Easiest)

**Step 1: Open Jupyter**
```
jupyter notebook notebooks/usage_notebook.ipynb
```

**Step 2: Read the instructions** in Cell 1

**Step 3: Run Cell 2** (click the ▶ button)
- Wait for "✓ attendance-generator is up to date."

**Step 4: Run Cell 3**
- A **form appears** with input fields

**Step 5: Fill the form**

| Field | Example | Required? |
|-------|---------|-----------|
| Input file * | `/path/to/data.xlsx` | Yes |
| Output folder | `./attendance_output` | No (default provided) |
| Logo image | `/path/to/logo.png` | No |
| Org line 1 | BRAC Institute of Governance and Development | No (default provided) |
| Org line 2 | BRAC University | No (default provided) |
| Pre-survey days | 5 | No |
| Weekends | friday | No |
| Holidays | 2025-12-25, 2025-01-01 | No |

**Step 6: Click "✓ Generate Attendance Sheets"**

**Step 7: Wait** for the documents to generate
- For 10 enumerators: ~5-10 seconds
- For 50 enumerators: ~30 seconds

**Step 8: Find your files**
- Navigate to the "Output folder" you specified
- You'll see Word documents (one per enumerator) + Excel QC workbook

---

### Using Terminal (Command Line)

**Step 1: Open Command Prompt/Terminal**

**Step 2: Navigate to your data folder**
```
cd C:\Users\YourName\Documents
```

**Step 3: Run the tool**
```
attendance-gen
```

**Step 4: Answer the questions**

```
==============================================================
Attendance Sheet Generator - Setup Wizard
BRAC Institute of Governance and Development
==============================================================

Answer each question and press Enter.
Press Enter alone to accept the default shown in [brackets].

-- Step 1 of 8 : Input file -----------------------------------
Path to your survey dataset (.dta / .xlsx / .csv): data.xlsx
```

- Type your data file path
- Press **Enter**

```
-- Step 2 of 8 : Output folder --------------------------------
Output folder [./attendance_output]: 
```

- Press **Enter** to use the default folder, or type a custom path
- Press **Enter**

```
-- Step 3 of 8 : Logo -----------------------------------------
Logo image path (leave blank to skip): 
```

- Press **Enter** to skip, or type the path to your logo file
- Press **Enter**

Continue answering the remaining 5 questions...

```
-- Summary ------------------------------------------------
  Input file   : data.xlsx
  Output folder: ./attendance_output
  Logo         : (none)
  Org line 1   : BRAC Institute of Governance and Development
  Org line 2   : BRAC University
  Pre-survey   : 5 days
  Weekends     : friday
  Holidays     : (none)
--------------------------------------------------------------
Press Enter to generate, or Ctrl+C to cancel.
```

- Review the summary
- Press **Enter** to generate

**Step 5: Done!**
Documents are saved to your output folder.

---

### Using Command Flags (Advanced)

For scripting or automation:

```bash
attendance-gen --input data.dta --output ./output --logo logo.png --weekend "friday,saturday" --pre-survey-days 3
```

See all options:
```bash
attendance-gen --help
```

---

## Input Data Preparation

### Column Requirements

Your dataset must have these columns (exact names not required; tool auto-detects):

| What | Example Names | Required? | Description |
|-----|---|---|---|
| **Enumerator ID** | `enu_code`, `enum_id`, `EnumID` | Yes | Unique ID per enumerator |
| **Enumerator Name** | `enu_name`, `enum_name`, `EnumName` | Yes | Full name |
| **Start Date** | `startdate`, `start_date`, `survey_day` | Yes | Survey start date |
| **End Date** | `enddate`, `end_date`, `finishdate` | No | Survey end date (if different from start) |
| **Upazila/District** | `upazila`, `upazilla` | No | Working area (appears in "Working Place" column) |

### Date Formats

Supported:
- `2025-12-01` (ISO format, preferred)
- `01/12/2025` (DD/MM/YYYY)
- `12/01/2025` (MM/DD/YYYY)
- `01-Dec-2025` (text format)
- Stata date formats (`%td`, `%tC`)

### Example: CSV Format

```csv
enu_code,enu_name,startdate,enddate,upazila
3753,Md Zubaer,2025-12-01,2025-12-11,Dhaka
4059,Iqbal Hossain,2025-12-01,2025-12-10,Dhaka
4148,Md Mokhsed Ali,2025-12-01,2025-12-15,Sylhet
```

### Example: Excel Format

| enu_code | enu_name | startdate | enddate | upazila |
|---|---|---|---|---|
| 3753 | Md Zubaer | 2025-12-01 | 2025-12-11 | Dhaka |
| 4059 | Iqbal Hossain | 2025-12-01 | 2025-12-10 | Dhaka |
| 4148 | Md Mokhsed Ali | 2025-12-01 | 2025-12-15 | Sylhet |

### Cleanup Tips

1. **Remove extra spaces** in names
2. **Use consistent date format** throughout the file
3. **No missing ID or name** — one enumerator per row
4. **One record per calendar day** covered by that enumerator

---

## Output Files Explained

### Attendance Sheet (Word Document)

**Filename:** `{ID}_{NAME}_attendance.docx`

Example: `3753_Md_Zubaer_attendance.docx`

**Contents:**

**Pages 1+: Attendance Table**

```
═══════════════════════════════════════════════════════════════
              BRAC Institute of Governance and Development
                        BRAC University
                      Attendance Sheet
═══════════════════════════════════════════════════════════════

Name: Md Zubaer (3753)    Designation: Enumerator    Mobile: ___

Period: 22 Nov 2025 to 11 Dec 2025

┌─────┬──────────────┬──────────────────────────┬──────┬────────┬────────┐
│ S/N │ Date         │ Purpose                  │ Data │ Place  │ Remark │
├─────┼──────────────┼──────────────────────────┼──────┼────────┼────────┤
│  1  │ 22 Nov 2025  │ Training ☐ Survey ☐ ... │      │        │        │
│  2  │ 23 Nov 2025  │ Weekend                  │      │        │        │
│  3  │ 24 Nov 2025  │ Survey                   │ Yes  │ Dhaka  │        │
│ ... │ ...          │ ...                      │ ...  │ ...    │ ...    │
│  25 │ (blank)      │ (blank)                  │      │        │        │
│ ... │ 5 blank rows for manual additions ...                            │
└─────┴──────────────┴──────────────────────────┴──────┴────────┴────────┘

═══════════════════════════════════════════════════════════════
                    Authorized by:
┌─────────────────────┬─────────────────────┬─────────────────────┐
│                     │                     │                     │
│ __________________ │ __________________ │ __________________ │
│    Enumerator       │       FA            │        RA           │
└─────────────────────┴─────────────────────┴─────────────────────┘
```

**Last Page: Summary**

```
═══════════════════════════════════════════════════════════════
              Enumerator Summary                  Days Count
───────────────────────────────────────────────────────────────
Name:              Md Zubaer                              
ID No.:            3753                                    
Period:                                                    
Survey Days:                                          13   
Training Days:                                             
Travel Days:                                               
Base Work Days:                                            
Office Work Days:                                          
Holiday/Off Days:                                          
Weekend Days:                                               
Total Working Days:                                        
Remarks / Notes:                                           
```

### QC Workbook (Excel)

**Filename:** `_QC_Summary.xlsx`

**Sheet 1: Matrix**

| Enumerator | 22 Nov | 23 Nov | 24 Nov | ... | 11 Dec |
|---|---|---|---|---|---|
| Md Zubaer (3753) | Training | Weekend | Survey | ... | (blank) |
| Iqbal Hossain (4059) | Survey | Survey | Holiday | ... | (blank) |

Colors:
- 🟢 Green = Survey
- 🟡 Yellow = Training
- 🟦 Blue = Base work
- ⬜ White = Blank/Off
- ⬛ Gray = Weekend/Holiday

**Sheet 2: Summary**

| ID | Name | Period Start | Period End | Data Days | Survey Days | Training Days | Travel Days | Weekend Days | Base Work Days | Blank Days |
|---|---|---|---|---|---|---|---|---|---|---|
| 3753 | Md Zubaer | 22 Nov 2025 | 11 Dec 2025 | 13 | 13 | 0 | 0 | 2 | 0 | 11 |
| 4059 | Iqbal Hossain | 21 Nov 2025 | 10 Dec 2025 | 13 | 13 | 0 | 0 | 2 | 0 | 11 |

**Sheet 3: Legend**

| Colour | Meaning |
|---|---|
| 🟢 Green | Survey |
| 🟡 Yellow | Training Day |
| 🟦 Blue | Base work |
| ⬛ Gray | Weekend |

---

## Calendar Customization

### Weekends

By default, Friday is marked as weekend. Customize:

**Terminal:**
```
-- Step 6 of 8 : Weekend days --------------------------------
Weekend days [friday]:
(e.g. "friday"  or  "friday,saturday"): friday,saturday
```

**Command line:**
```bash
attendance-gen --input data.xlsx --weekend "friday,saturday"
```

**Supported day names:** Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday (case-insensitive)

**Or by number:** 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun

```bash
--weekend "4,5"  # Friday and Saturday
```

### Holidays

Days to mark as "Holiday" in the attendance sheet.

**Terminal:**
```
-- Step 7 of 8 : Public holidays --------------------------------
Public holiday dates to mark (leave blank if none) []:
(e.g. "2025-12-25"  or  "2025-12-24:2025-12-26, 2025-01-01"): 2025-12-25, 2025-01-01
```

**Command line:**
```bash
--holidays "2025-12-25, 2025-01-01"
```

**Date range:**
```bash
--holidays "2025-12-20:2025-12-27"  # 20-27 Dec
```

**Multiple ranges:**
```bash
--holidays "2025-12-20:2025-12-27, 2025-01-01:2025-01-02"
```

### Base Work Days

Days to mark as "Base work" in Purpose column (e.g., office work, training at headquarters).

```bash
--basework "2025-12-10:2025-12-12"
```

### Pre-Survey Days

Blank rows before the first survey date (for manual additions).

**Default:** 5 days

**Terminal:**
```
-- Step 5 of 8 : Pre-survey days -----------
Days to include BEFORE survey start [5]: 3
```

**Command line:**
```bash
--pre-survey-days 3
```

---

## Frequently Asked Questions

### Q: What if the tool doesn't find my data file?

**A:** Use the **full path** to your file:

**Windows:**
```
C:\Users\YourName\Documents\survey_data.xlsx
```

**Mac/Linux:**
```
/Users/YourName/Documents/survey_data.xlsx
```

Or navigate to the folder in Command Prompt first:
```
cd C:\Users\YourName\Documents
attendance-gen
```

Then just type: `survey_data.xlsx`

---

### Q: Can I customize the organization name?

**A:** Yes!

**Terminal:**
```
-- Step 4a -- Org line 1 [BRAC Institute of Governance and Development]: My Organization
-- Step 4b -- Org line 2 [BRAC University]: My Division
```

**Command line:**
```bash
--org1 "My Organization" --org2 "My Division"
```

---

### Q: How do I add a logo?

**A:** Provide the path during setup:

**Terminal:**
```
-- Step 3 -- Logo image path (leave blank to skip): C:\path\to\logo.png
```

**Command line:**
```bash
--logo "C:\path\to\logo.png"
```

**Logo requirements:**
- Format: JPEG or PNG
- File must exist
- Appears in header, top-left, on every page
- Size adjusted automatically

---

### Q: How long does it take to generate documents?

**A:**
- 10 enumerators: ~5 seconds
- 50 enumerators: ~30 seconds
- 100 enumerators: ~60 seconds

Processing time depends on:
- Number of enumerators
- Date range length
- Computer speed

---

### Q: Can I edit the generated documents?

**A:** **Yes!** The Word documents are fully editable. After generation, you can:
- Add handwritten signatures
- Modify text
- Add notes
- Change formatting

The Excel QC workbook is also editable.

---

### Q: What if an enumerator has multiple survey date ranges?

**A:** The tool handles this automatically. If your data has:

```
enu_code,enu_name,startdate,enddate
3753,Md Zubaer,2025-12-01,2025-12-05
3753,Md Zubaer,2025-12-10,2025-12-15
```

The tool creates **one document** for Md Zubaer covering both ranges, with blank space in between.

---

### Q: How do I update the tool?

**A:**
```bash
pip install --upgrade git+https://github.com/Sabbirhossain780/attendance-generator.git
```

Or in Jupyter: re-run Cell 2 of the notebook.

---

## Troubleshooting

### Issue: "File not found" error

**Solution:**
1. Check the file **exists** at the path you provided
2. Use the **full path** (not relative path)
3. Copy the full path from Windows File Explorer:
   - Right-click the file
   - Hold Shift
   - Click "Copy as path"
   - Paste it into the tool

---

### Issue: Column names not detected

**Symptom:**
```
Error: Cannot find column for 'Enumerator ID'
Available: [list of your columns]
```

**Solution:**

Option 1: Rename your columns to match expected names:
- `enu_code`, `enum_id`, `EnumID` (for ID)
- `enu_name`, `enum_name` (for Name)
- `startdate`, `start_date`, `survey_day` (for Start Date)

Option 2: Provide column overrides (advanced):
```bash
--col-override "Enumerator ID=your_column_name"
```

---

### Issue: Dates not being parsed

**Symptom:**
```
[!] X rows with unparseable start date dropped
```

**Solution:**
1. Check date format — use `YYYY-MM-DD` or `DD/MM/YYYY`
2. In Excel: Ensure cells are formatted as **Date**, not Text
3. In Stata: Use `%td` (date) or `%tC` (clock) format
4. In CSV: Use text date like `2025-12-01` (ISO format preferred)

---

### Issue: Logo not appearing in document

**Symptom:** The Word document doesn't show the logo image

**Solution:**
1. Check file **exists** at the path provided
2. Ensure it's **JPEG or PNG** format
3. Try with the **full path**:
   ```bash
   --logo "C:\Users\YourName\Pictures\logo.png"
   ```

---

### Issue: Unicode characters causing errors (Windows)

**Symptom:**
```
UnicodeEncodeError: 'charmap' codec can't encode...
```

**Solution:**

Set your terminal to use UTF-8:

**Windows Command Prompt:**
```
chcp 65001
```

Then run the tool again.

---

### Issue: Different date formats in same file

**Symptom:** Some dates parse, others show as errors

**Solution:**
1. Use Find & Replace to standardize dates to `YYYY-MM-DD`
2. In Excel: Select all date cells → Format → Date → ISO 8601
3. In CSV: Open in a text editor and manually fix date format

---

## Tips & Best Practices

### 1. Prepare Data First

Before running the tool:
- ✓ Remove extra spaces from names
- ✓ Check all dates are valid
- ✓ Ensure no missing IDs or names
- ✓ Use consistent date format

**Quick check in Excel:**
- Sort by ID to spot duplicates
- Sort by Start Date to catch weird dates
- Look for blank cells

---

### 2. Test with Demo Mode First

For new datasets, test with one enumerator:

```bash
attendance-gen --input data.xlsx --demo
```

This generates documents for **first enumerator only** (alphabetically). Check the output before running on all enumerators.

---

### 3. Use Relative Paths for Portability

Instead of:
```bash
attendance-gen --input "C:\Users\YourName\Data\survey.xlsx"
```

Navigate to the folder and use:
```bash
cd C:\Users\YourName\Data
attendance-gen --input survey.xlsx
```

This makes scripts portable across computers.

---

### 4. Create a Batch Script (Windows)

For repeated use, create a file named `generate_attendance.bat`:

```batch
@echo off
cd C:\Users\YourName\Data
attendance-gen --input survey.xlsx --weekend "friday" --holidays "2025-12-25, 2025-01-01"
pause
```

Double-click the `.bat` file to run.

---

### 5. Use Excel for QC

After generation:
1. Open `_QC_Summary.xlsx`
2. Check the **Matrix** sheet for gaps or anomalies
3. Review **Summary** sheet for accuracy
4. Use counts to verify against your fieldwork reports

---

### 6. Archive Your Outputs

Create a folder structure:
```
attendance_outputs/
  2025_December/
    survey_2025_12_attendance_sheets/
      *.docx files
      _QC_Summary.xlsx
    raw_data/
      survey_data.xlsx (original)
```

---

### 7. Keep Your Data File as Backup

Always keep the original dataset (CSV, Excel, or Stata) alongside the generated documents for audit trails.

---

## Getting Help

**Issue not listed above?**

1. Check the terminal error message — it usually tells you what's wrong
2. Verify your data format matches the requirements
3. Try the `--help` flag to see all options:
   ```bash
   attendance-gen --help
   ```

---

## Summary: Your First Run

```
1. Open Command Prompt / Terminal
2. Type: attendance-gen
3. Answer 8 questions
4. Press Enter to confirm
5. Wait 5-30 seconds
6. Check the "Output folder" for .docx and .xlsx files
7. Open documents in Word/Excel
8. Done!
```

**That's it.** No technical knowledge required.

---

**Version:** 1.0.0  
**Built by:** BIGD, BRAC University  
**License:** MIT (free to use and modify)
