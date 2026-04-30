# Building a Python Package: A Step-by-Step Tutorial

**From Jupyter Notebook to Pip-Installable Package**

This is a **real, project-based tutorial** where we converted a Jupyter notebook into a professional Python package. You'll learn actual Python packaging techniques by following the exact steps used to build the `attendance-generator` tool.

---

## Table of Contents

1. [The Problem We Started With](#the-problem)
2. [The Solution: Python Package](#the-solution)
3. [Project Structure](#project-structure)
4. [Step 1: Initialize Git & Project](#step-1-initialize-git)
5. [Step 2: Create Basic Package Structure](#step-2-package-structure)
6. [Step 3: Extract Code from Notebook](#step-3-extract-code)
7. [Step 4: Organize Into Modules](#step-4-organize-modules)
8. [Step 5: Configuration Management](#step-5-config)
9. [Step 6: Create Tests](#step-6-tests)
10. [Step 7: CLI Entry Point](#step-7-cli)
11. [Step 8: Package Configuration Files](#step-8-config-files)
12. [Step 9: Documentation](#step-9-docs)
13. [Step 10: Git Workflow](#step-10-git)
14. [Step 11: Publish to GitHub](#step-11-publish)
15. [Key Lessons Learned](#lessons)

---

## The Problem

We had a **Jupyter notebook** (`attendance_generator_v7.ipynb`) that:
- Works great for one person running it
- Hard to share with non-technical users
- Can't be installed via `pip`
- No version control for dependencies
- Difficult for others to install or use

**The challenge:** How do we make this reusable, shareable, and installable?

---

## The Solution

Convert it to a **Python package** that:
- Works on Windows, Mac, and Linux
- Installs with one command: `pip install git+https://github.com/...`
- Has a professional structure
- Includes tests
- Has a command-line interface
- Can be updated easily
- Is beginner-friendly

**The benefit:** Non-technical users can use it WITHOUT understanding Python.

---

## Project Structure

Here's what a Python package looks like:

```
attendance-generator/
├── .git/                          # Git version control folder
├── .gitignore                     # Files to NOT commit (cache, etc)
├── README.md                      # Quick overview
├── MANUAL.md                      # User guide
├── DEVELOPMENT_GUIDE.md           # THIS FILE
├── LICENSE                        # MIT license
│
├── pyproject.toml                 # Modern Python project config
├── setup.py                       # Older Python project config (fallback)
│
├── attendance_generator/          # MAIN PACKAGE FOLDER
│   ├── __init__.py                # Makes this a package + exports
│   ├── config.py                  # Configuration dataclass
│   ├── helpers.py                 # Utility functions
│   ├── loaders.py                 # Load Excel/CSV/Stata files
│   ├── builders.py                # Build Word documents
│   ├── generator.py               # Main document generator
│   ├── excel_qc.py                # Create Excel QC workbooks
│   ├── pipeline.py                # Orchestrate the whole flow
│   ├── wizard.py                  # Interactive terminal/Jupyter forms
│   └── cli.py                     # Command-line interface
│
├── tests/                         # TEST FOLDER
│   ├── __init__.py                # Makes this a package
│   ├── test_helpers.py            # Test helper functions
│   ├── test_loaders.py            # Test loading data
│   ├── test_wizard.py             # Test the wizard
│   └── test_pipeline.py           # Test end-to-end flow
│
├── notebooks/                     # Jupyter notebooks
│   ├── usage_notebook.ipynb       # For non-technical users
│   └── attendance_generator_v7.ipynb  # Original notebook
│
└── .github/
    └── workflows/
        ├── ci.yml                 # Automated testing
        └── release.yml            # Automated releases
```

**Key concept:** Everything is organized by PURPOSE, not by file type.

---

## Step 1: Initialize Git & Project

### 1.1 Create the GitHub Repository

First, we created a GitHub repo at:
```
https://github.com/Sabbirhossain780/Attendence_generator_enum.git
```

### 1.2 Initialize Git Locally

```bash
# Initialize git in the folder
git init

# Add the remote (connect to GitHub)
git remote add origin https://github.com/Sabbirhossain780/Attendence_generator_enum.git

# Verify connection
git remote -v
```

**What this does:**
- `git init` — Creates a `.git/` folder to track changes
- `git remote add origin URL` — Connects your local folder to GitHub
- `git remote -v` — Shows all connections

### 1.3 Create .gitignore

We created a `.gitignore` file to tell Git which files to ignore:

```
# Python cache
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Build artifacts
dist/
build/
*.egg-info/

# Logs
*.log

# Output folders
attendance_output/
```

**Why?** Because:
- `__pycache__/` are auto-generated, don't need to commit
- `venv/` is huge and can be recreated, don't commit
- IDE files (`.vscode/`) are personal, don't commit
- Build artifacts are temporary, don't commit

**First commit:**
```bash
git add .gitignore
git commit -m "Initial commit: add .gitignore"
git push -u origin master
```

---

## Step 2: Package Structure

### 2.1 Create the Main Package Folder

```bash
mkdir attendance_generator
cd attendance_generator
touch __init__.py
```

**Why `attendance_generator/`?**
- This is the **package folder**
- When someone does `pip install ...`, this folder is what gets installed
- The package name becomes the import name: `import attendance_generator`

### 2.2 Create the `__init__.py` File

This tells Python "this folder is a package". Here's what goes in it:

```python
# attendance_generator/__init__.py

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("attendance-generator")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["run", "run_wizard", "generate_doc", "__version__"]

from attendance_generator.pipeline import run
from attendance_generator.wizard import run_wizard
from attendance_generator.generator import generate_doc
```

**What this does:**
1. **Imports the version** from package metadata (set in `pyproject.toml`)
2. **Defines `__all__`** — tells Python which functions are public
3. **Imports main functions** — so users can do:
   ```python
   from attendance_generator import run, run_wizard
   ```
   Instead of:
   ```python
   from attendance_generator.pipeline import run
   from attendance_generator.wizard import run_wizard
   ```

**Key lesson:** `__init__.py` is the **public face** of your package.

---

## Step 3: Extract Code from the Notebook

The original Jupyter notebook had ~1500 lines of code. We extracted it by:

### 3.1 Understand the Notebook Structure

We divided the notebook into **logical sections**:
- Data loading & parsing (Cell: 08c0da3f)
- Date/classification logic (Cell: 1a6081d2, 8b993b26)
- Document building (Cell: f0df1d51, 59aba217, 1da98519)
- Excel generation (Cell: 00990c49)
- Main flow (Cell: 4be00bee)

### 3.2 Identify Dependencies

From the notebook, we found:
```python
import pandas as pd           # Read Excel/CSV
from docx import Document    # Create Word docs
from docx.shared import Pt, RGBColor, Inches
from openpyxl import Workbook  # Create Excel files
from lxml import etree       # XML manipulation
```

**Why each one?**
- **pandas:** Reads `.xlsx`, `.csv`, `.dta` files
- **python-docx:** Creates `.docx` files
- **openpyxl:** Creates `.xlsx` files
- **lxml:** Manipulates XML inside Word docs

---

## Step 4: Organize Into Modules

### 4.1 Create `config.py` — Configuration

**Problem:** The notebook had global variables everywhere:
```python
# Bad (notebook style)
ORG_LINE1 = "BRAC Institute..."
ORG_LINE2 = "BRAC University"
WEEKEND_DAYS = {"friday"}
OUT_DIR = "./attendance_output"
```

**Solution:** Create a config class:

```python
# attendance_generator/config.py

from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Config:
    """Holds all configuration for the tool"""
    
    # Input/Output
    data_path: str
    out_dir: str = "./attendance_output"
    logo_path: str = ""
    
    # Organization
    org_line1: str = "BRAC Institute of Governance and Development"
    org_line2: str = "BRAC University"
    project_name: str = ""
    
    # Calendar settings
    weekend_days_raw: str = "friday"
    holiday_dates_raw: str = ""
    basework_dates_raw: str = ""
    n_pre_survey: int = 5
    
    # Column overrides
    col_override: dict = field(default_factory=dict)
    
    # Demo mode
    demo: bool = False
```

**Why `@dataclass`?**
- Automatically creates `__init__`, `__repr__`, etc.
- Type hints help catch errors
- Clean, readable code
- Easy to pass around

**Usage:**
```python
cfg = Config(
    data_path="data.xlsx",
    org_line1="My Company",
    weekend_days_raw="friday,saturday"
)

print(cfg.org_line1)  # "My Company"
```

### 4.2 Create `helpers.py` — Utility Functions

These are **small functions** used by other modules:

```python
# attendance_generator/helpers.py

from datetime import datetime
import re

def parse_dates(raw: str) -> list:
    """Parse date string like '2025-12-01' or '2025-12-01:2025-12-05'"""
    if not raw:
        return []
    
    dates = []
    for part in raw.split(","):
        part = part.strip()
        if ":" in part:
            # Range: 2025-12-01:2025-12-05
            start_str, end_str = part.split(":")
            start = datetime.strptime(start_str.strip(), "%Y-%m-%d")
            end = datetime.strptime(end_str.strip(), "%Y-%m-%d")
            current = start
            while current <= end:
                dates.append(current.date())
                current += timedelta(days=1)
        else:
            # Single date: 2025-12-01
            dates.append(datetime.strptime(part, "%Y-%m-%d").date())
    
    return dates

def parse_weekend_days(raw: str) -> set:
    """Convert 'friday,saturday' or '4,5' to set of weekday numbers"""
    # Map day names to numbers: Mon=0, Sun=6
    day_map = {
        "monday": 0, "tuesday": 1, "wednesday": 2,
        "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6
    }
    
    days = set()
    for day in raw.lower().split(","):
        day = day.strip()
        if day.isdigit():
            days.add(int(day))
        elif day in day_map:
            days.add(day_map[day])
    
    return days

def make_classifier(weekend_days, holiday_dates, basework_dates):
    """Create a classifier function (closure pattern)"""
    def classify(date_obj, is_survey: bool) -> str:
        if date_obj.weekday() in weekend_days:
            return "Weekend"
        elif date_obj in holiday_dates:
            return "Holiday"
        elif date_obj in basework_dates:
            return "Base work"
        elif is_survey:
            return "Survey"
        else:
            return ""
    
    return classify
```

**Key pattern:** **Closure** (a function that returns a function)

The `make_classifier()` returns a `classify()` function that **remembers** the weekend_days, holiday_dates, etc. from when it was created.

**Why closures?**
- Avoids global variables
- Each execution can have different settings
- Testable and reusable

### 4.3 Create `loaders.py` — Load Data

This module reads Excel/CSV/Stata files:

```python
# attendance_generator/loaders.py

import pandas as pd
from datetime import datetime
from attendance_generator.helpers import find_col, parse_dates

def load_dataframe(data_path: str) -> pd.DataFrame:
    """Load data from Excel, CSV, or Stata file"""
    
    if data_path.endswith(".dta"):
        df = pd.read_stata(data_path)
    elif data_path.endswith((".xlsx", ".xls", ".xlsm")):
        df = pd.read_excel(data_path)
    elif data_path.endswith(".csv"):
        try:
            df = pd.read_csv(data_path, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(data_path, encoding="latin-1")
    else:
        raise ValueError(f"Unsupported file type: {data_path}")
    
    return df

def build_payloads(df: pd.DataFrame, cfg: Config) -> list:
    """Convert DataFrame into payloads for document generation"""
    
    # Find the columns
    col_id = find_col(df, ["enu_code", "enum_id", "id"], "Enumerator ID")
    col_name = find_col(df, ["enu_name", "enum_name", "name"], "Enumerator Name")
    col_start = find_col(df, ["startdate", "start_date", "survey_day"], "Start Date")
    col_end = find_col(df, ["enddate", "end_date", "finishdate"], "End Date", required=False)
    col_upazila = find_col(df, ["upazila", "upazilla", "location"], "Upazila", required=False)
    
    # Parse dates
    weekend_days = parse_weekend_days(cfg.weekend_days_raw)
    holiday_dates = set(parse_dates(cfg.holiday_dates_raw))
    basework_dates = set(parse_dates(cfg.basework_dates_raw))
    
    # Create classifier function
    classify = make_classifier(weekend_days, holiday_dates, basework_dates)
    
    # Build payloads
    payloads = []
    for group_name, group_df in df.groupby(col_id):
        enu_name = group_df[col_name].iloc[0]
        
        # Build rows
        rows = []
        for _, row in group_df.iterrows():
            start = pd.to_datetime(row[col_start]).date()
            end = pd.to_datetime(row[col_end]).date() if col_end else start
            
            current = start
            while current <= end:
                purpose = classify(current, True)
                rows.append({
                    "date": current,
                    "purpose": purpose,
                    "has_data": "Yes" if purpose == "Survey" else "",
                    "working_place": row.get(col_upazila, "")
                })
                current += timedelta(days=1)
        
        payloads.append({
            "enu_id": group_name,
            "enu_name": enu_name,
            "rows": rows
        })
    
    return payloads
```

**Key concept:** **Separation of concerns**
- `loaders.py` only handles data loading
- It doesn't know about Word documents or Excel
- Other modules use the data it loads

### 4.4 Create `builders.py` — Build Documents

This is the biggest module (~760 lines). It creates Word documents:

```python
# attendance_generator/builders.py

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# Page constants
DXA = 635  # Device-independent units
CONTENT_DXA = 14400  # Page width in DXA
MARGIN_DXA = 720

# Column widths (sum must equal CONTENT_DXA)
COL_SN = 500
COL_DATE = 1500
COL_PURPOSE = 6600
COL_DATA = 600
COL_PLACE = 2400
COL_REMARK = 2800

def register_logo(section, logo_path: str) -> str:
    """Add logo to header"""
    if not logo_path:
        return None
    
    header = section.header
    paragraph = header.paragraphs[0]
    run = paragraph.add_run()
    
    # Add image to header
    picture = run.add_picture(logo_path, width=Inches(1))
    
    # Get the relationship ID
    return picture._inline.graphic.graphicData.pic.nvPicPr.cNvPr.id

def build_header(section, logo_rid, enu_name, enu_id, start_date, end_date, org_line1, org_line2):
    """Build repeating header"""
    header = section.header
    
    # Clear default
    header.paragraphs[0].text = ""
    
    # Organization line 1
    p = header.paragraphs[0]
    p.text = org_line1
    p.alignment = 1  # Center
    
    # Organization line 2
    p = header.add_paragraph(org_line2)
    p.alignment = 1  # Center
    
    # Title
    p = header.add_paragraph("Attendance Sheet")
    p.alignment = 1  # Center
    
    # Enumerator details
    p = header.add_paragraph(f"Name: {enu_name} ({enu_id})")
    p.runs[0].bold = True
    
    # Period
    date_range = f"{start_date.strftime('%d %b %Y')} to {end_date.strftime('%d %b %Y')}"
    p = header.add_paragraph(f"Period: {date_range}")

def build_attendance_table(doc, rows):
    """Build main attendance table"""
    
    table = doc.add_table(rows=1 + len(rows), cols=6)
    table.style = "Light Grid Accent 1"
    
    # Header row
    header_cells = table.rows[0].cells
    headers = ["S/N", "Date", "Purpose", "Data", "Working Place", "Remarks"]
    for i, header_text in enumerate(headers):
        header_cells[i].text = header_text
        # Style
        for paragraph in header_cells[i].paragraphs:
            for run in paragraph.runs:
                run.bold = True
    
    # Data rows
    for i, row in enumerate(rows, 1):
        cells = table.rows[i].cells
        cells[0].text = str(i)
        cells[1].text = row["date"].strftime("%d %b %Y")
        cells[2].text = row["purpose"]
        cells[3].text = row["has_data"]
        cells[4].text = row["working_place"]
        cells[5].text = ""
    
    return table
```

**Why split into functions?**
- Each function does ONE thing
- Easy to test
- Easy to reuse
- Easy to understand

### 4.5 Create `pipeline.py` — Orchestrate Everything

This is the "conductor" that brings everything together:

```python
# attendance_generator/pipeline.py

from attendance_generator.loaders import load_dataframe, build_payloads
from attendance_generator.generator import generate_doc
from attendance_generator.excel_qc import build_qc_workbook

def run(cfg: Config) -> None:
    """Main execution pipeline"""
    
    print(f"[*] Attendance Generator v{__version__}")
    
    # Step 1: Load data
    print("[*] Loading data...")
    df = load_dataframe(cfg.data_path)
    
    # Step 2: Build payloads
    print("[*] Building payloads...")
    payloads = build_payloads(df, cfg)
    
    # Step 3: Create output folder
    os.makedirs(cfg.out_dir, exist_ok=True)
    
    # Step 4: Generate documents
    print(f"[*] Generating {len(payloads)} attendance sheets...")
    for i, payload in enumerate(payloads, 1):
        print(f"  [{i}/{len(payloads)}] {payload['enu_name']}...", end=" ", flush=True)
        generate_doc(payload, cfg, cfg.out_dir)
        print("OK")
    
    # Step 5: Create QC workbook
    print("[*] Creating QC workbook...")
    build_qc_workbook(payloads, cfg.out_dir)
    
    print("[*] Done!")
    print(f"[*] Files saved to: {cfg.out_dir}")
```

**Why a pipeline?**
- Clear, readable sequence of steps
- Easy to add logging
- Easy to add error handling
- Each step is independent

---

## Step 5: Configuration Management (The Config Pattern)

### The Problem

**Notebook style (bad):**
```python
# Global variables everywhere
ORG_LINE1 = "BRAC..."
ORG_LINE2 = "BRAC..."
WEEKEND_DAYS = {"friday"}
HOLIDAY_DATES = {...}
N_PRE_SURVEY = 5
OUT_DIR = "./output"

def build_header(section):
    p = section.add_paragraph(ORG_LINE1)  # Uses global
    # ...

def generate_doc(payload):
    # ...can't change settings easily!
```

**Problems:**
- Hard to test (can't use different settings)
- Hard to reuse (settings are scattered)
- Globals are bad practice
- Can't run multiple configurations

### The Solution

**Package style (good):**
```python
@dataclass
class Config:
    org_line1: str = "BRAC..."
    org_line2: str = "BRAC..."
    weekend_days_raw: str = "friday"
    # ...

def build_header(section, org_line1, org_line2):
    p = section.add_paragraph(org_line1)  # Explicit parameter
    # ...

def generate_doc(payload, cfg: Config):
    build_header(section, cfg.org_line1, cfg.org_line2)
```

**Benefits:**
- Settings in one place
- Easy to test (different configs)
- Easy to reuse (pass config around)
- Clear what each function needs

### How It Flows

```
1. User runs: attendance-gen --input data.xlsx --weekend "friday,saturday"
                                      ↓
2. CLI creates Config object with settings
                                      ↓
3. Config is passed to pipeline.run(cfg)
                                      ↓
4. pipeline passes cfg to build_payloads(df, cfg)
                                      ↓
5. build_payloads uses cfg.weekend_days_raw to parse
                                      ↓
6. Config is passed to generate_doc(payload, cfg, out_dir)
                                      ↓
7. generate_doc uses cfg.org_line1, cfg.logo_path, etc.
```

---

## Step 6: Testing

### Why Test?

Tests verify your code works **before** users try it.

### 6.1 Create `tests/test_helpers.py`

```python
# tests/test_helpers.py

import pytest
from attendance_generator.helpers import parse_dates, parse_weekend_days

def test_parse_single_date():
    """Test parsing a single date"""
    result = parse_dates("2025-12-01")
    assert len(result) == 1
    assert str(result[0]) == "2025-12-01"

def test_parse_date_range():
    """Test parsing a date range"""
    result = parse_dates("2025-12-01:2025-12-03")
    assert len(result) == 3
    assert str(result[0]) == "2025-12-01"
    assert str(result[2]) == "2025-12-03"

def test_parse_weekend_days():
    """Test parsing weekend days"""
    result = parse_weekend_days("friday,saturday")
    assert result == {4, 5}  # 4=Friday, 5=Saturday
```

### 6.2 Run Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=attendance_generator --cov-report=html
```

**Output:**
```
tests/test_helpers.py::test_parse_single_date PASSED
tests/test_helpers.py::test_parse_date_range PASSED
tests/test_helpers.py::test_parse_weekend_days PASSED

======================== 3 passed in 0.05s ========================
```

### Why This Matters

- Catches bugs early
- Prevents regression (old bugs coming back)
- Proves your code works
- Makes refactoring safe

---

## Step 7: CLI Entry Point

### 7.1 Create `cli.py`

This is what users run when they type `attendance-gen`:

```python
# attendance_generator/cli.py

import sys
import argparse
from attendance_generator.config import Config
from attendance_generator.pipeline import run
from attendance_generator.wizard import run_wizard
from attendance_generator import __version__

def main():
    """Command-line interface"""
    
    parser = argparse.ArgumentParser(
        description="Generate attendance & travelling bill sheets",
        epilog="Run with no arguments for interactive wizard: attendance-gen"
    )
    
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--input", "-i", required=True, help="Path to data file")
    parser.add_argument("--output", "-o", default="./attendance_output", help="Output folder")
    parser.add_argument("--logo", help="Path to logo image")
    parser.add_argument("--org1", help="Organization line 1")
    parser.add_argument("--org2", help="Organization line 2")
    parser.add_argument("--weekend", help="Weekend days (e.g., 'friday,saturday')")
    parser.add_argument("--holidays", help="Holiday dates (e.g., '2025-12-25')")
    parser.add_argument("--demo", action="store_true", help="Demo mode: first enumerator only")
    
    args = parser.parse_args()
    
    # Build config from arguments
    cfg = Config(
        data_path=args.input,
        out_dir=args.output,
        logo_path=args.logo or "",
        org_line1=args.org1 or "BRAC Institute of Governance and Development",
        org_line2=args.org2 or "BRAC University",
        weekend_days_raw=args.weekend or "friday",
        holiday_dates_raw=args.holidays or "",
        demo=args.demo
    )
    
    # Run
    run(cfg)

if __name__ == "__main__":
    main()
```

### 7.2 Register Entry Point in `pyproject.toml`

```toml
[project.scripts]
attendance-gen = "attendance_generator.cli:main"
```

**What this does:**
- When you install the package, pip creates a command `attendance-gen`
- Running `attendance-gen` calls `main()` in `cli.py`
- Works on Windows, Mac, and Linux

**How it works:**
```bash
$ attendance-gen --help
usage: attendance-gen [-h] [--version] --input INPUT ...
```

---

## Step 8: Package Configuration Files

### 8.1 `pyproject.toml` — Modern Standard

This is the **single source of truth** for your package:

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "attendance-generator"
version = "1.0.0"
description = "Automated attendance & travelling bill .docx generator"
readme = "README.md"
requires-python = ">=3.9"
license = { text = "MIT" }
authors = [
    { name = "BIGD Research Team", email = "research@bigd.bracu.ac.bd" }
]

dependencies = [
    "python-docx>=1.1.0",
    "openpyxl>=3.1.0",
    "pandas>=2.0.0",
    "lxml>=5.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
]

[project.scripts]
attendance-gen = "attendance_generator.cli:main"

[tool.setuptools]
packages = ["attendance_generator"]
```

**What each section does:**

- **`[build-system]`** — How to build the package
- **`[project]`** — Metadata (name, version, description, etc.)
- **`dependencies`** — What this package needs to run
- **`[project.optional-dependencies]`** — Extra packages for development
- **`[project.scripts]`** — Command-line commands to create
- **`[tool.setuptools]`** — Where to find the package

### 8.2 `setup.py` — Older Fallback

Some tools still use `setup.py`. We provide it for compatibility:

```python
#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="attendance-generator",
    version="1.0.0",
    author="BIGD Research Team",
    author_email="research@bigd.bracu.ac.bd",
    description="Automated attendance & travelling bill generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sabbirhossain780/Attendence_generator_enum",
    packages=find_packages(),
    install_requires=[
        "python-docx>=1.1.0",
        "openpyxl>=3.1.0",
        "pandas>=2.0.0",
        "lxml>=5.0.0",
    ],
    entry_points={
        "console_scripts": [
            "attendance-gen=attendance_generator.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.9",
)
```

**Why both files?**
- Modern tools use `pyproject.toml`
- Old tools use `setup.py`
- Having both ensures compatibility

### 8.3 `LICENSE` — MIT License

We chose MIT because it's:
- Simple and clear
- Allows commercial use
- Requires attribution
- No liability

```
MIT License

Copyright (c) 2025 BIGD Research Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:
...
```

---

## Step 9: Documentation

### 9.1 `README.md` — First Impression

Users see this on GitHub. It should:
- Explain what it does (1 sentence)
- Show quick start (3 commands)
- Link to full docs

```markdown
# attendance-generator

Automated attendance sheet generator for field surveys.

## Quick Start

```bash
pip install git+https://github.com/Sabbirhossain780/Attendence_generator_enum.git
attendance-gen
```

[Full documentation →](README.md)
```

### 9.2 `MANUAL.md` — User Guide

For non-technical users. Explains:
- How to install
- How to prepare data
- How to use the tool
- Troubleshooting

### 9.3 `DEVELOPMENT_GUIDE.md` — THIS FILE

For developers learning Python packaging. Explains:
- Why each file exists
- How the code is organized
- How modules work together
- Git workflow

---

## Step 10: Git Workflow

### 10.1 Making Your First Commit

```bash
# Stage all files
git add .

# Create a commit (note the message format)
git commit -m "Initial release v1.0.0: attendance-generator package"

# Send to GitHub
git push -u origin master
```

**Commit message format:**
```
<type>: <description>

<optional longer explanation>

<optional footer>
```

**Types:**
- `feat:` — New feature
- `fix:` — Bug fix
- `docs:` — Documentation
- `refactor:` — Code restructuring (no feature change)
- `test:` — Test addition
- `chore:` — Maintenance (dependencies, etc.)

### 10.2 Creating a Release Tag

After you're ready to release:

```bash
# Create a tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tag to GitHub
git push origin v1.0.0
```

**Why tags?**
- Mark specific versions
- GitHub creates Release pages
- Users can install specific versions: `pip install package==1.0.0`

### 10.3 Making Updates

When you fix a bug or add a feature:

```bash
# Make changes
# ... edit files ...

# Stage changes
git add file1.py file2.py

# Commit
git commit -m "fix: Handle unicode errors on Windows"

# Push
git push origin master

# If it's a release
git tag -a v1.0.1 -m "Bugfix release"
git push origin v1.0.1
```

### 10.4 Branch Strategy (for teams)

For bigger projects:

```bash
# Create feature branch
git checkout -b feature/add-logging
# ... make changes ...
git add .
git commit -m "feat: Add detailed logging"
git push origin feature/add-logging

# Create pull request on GitHub (ask for review)
# After review is approved, merge to main
git checkout main
git merge feature/add-logging
git push origin main
```

---

## Step 11: Publish to GitHub

### 11.1 Create Repository on GitHub

1. Go to https://github.com/new
2. Enter name: `Attendence_generator_enum`
3. Choose "Public"
4. Click "Create repository"

### 11.2 Connect Local to GitHub

```bash
# Add remote
git remote add origin https://github.com/Sabbirhossain780/Attendence_generator_enum.git

# Verify
git remote -v
```

### 11.3 Push Everything

```bash
# Push all branches
git push -u origin master

# Push all tags
git push origin --tags
```

### 11.4 GitHub Actions (Automated Testing)

We can automatically run tests when you push:

```yaml
# .github/workflows/ci.yml

name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11"]
    
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
      
      - name: Run tests
        run: |
          pytest tests/ -v
```

**What this does:**
- Every time you push, GitHub runs tests
- Tests on Python 3.9, 3.10, 3.11
- If tests fail, GitHub shows it
- You can't merge without passing tests

---

## Key Lessons Learned

### 1. Separate Concerns

**Bad:**
```python
# One big file with everything
def load_and_build_and_generate():
    # 1000 lines of mixed logic
```

**Good:**
```python
# Each module has one responsibility
loaders.py       # Loading
builders.py      # Building
generator.py     # Generating
pipeline.py      # Orchestration
```

**Benefit:** Easy to test, easy to understand, easy to reuse

### 2. Use Configuration, Not Globals

**Bad:**
```python
ORG_NAME = "BRAC"  # Global variable
WEEKEND = "friday"  # Global variable

def build_doc():
    # Uses globals, hard to test
```

**Good:**
```python
@dataclass
class Config:
    org_name: str
    weekend: str

def build_doc(cfg: Config):
    # Explicit, testable
```

**Benefit:** Can test with different configs, easy to reuse

### 3. Type Hints Help

**Bad:**
```python
def parse_dates(raw):
    # What type is raw? What does it return?
```

**Good:**
```python
def parse_dates(raw: str) -> list[datetime.date]:
    # Crystal clear what goes in and out
```

**Benefit:** IDE autocomplete, catches bugs, self-documenting

### 4. Closures for State

**Problem:** How to pass settings to a function without globals?

**Solution:**
```python
def make_classifier(weekends, holidays):
    def classify(date, is_survey):
        # This function "remembers" weekends and holidays
        if date.weekday() in weekends:
            return "Weekend"
        return "Survey" if is_survey else ""
    
    return classify

# Use it
classifier = make_classifier({"friday"}, {...})
result = classifier(some_date, True)
```

**Benefit:** No globals, flexible, testable

### 5. Entry Points for CLI

**Problem:** How to create a command-line command?

**Solution:** Register in `pyproject.toml`:
```toml
[project.scripts]
attendance-gen = "attendance_generator.cli:main"
```

**Result:**
```bash
$ attendance-gen --help
```

**Benefit:** One command, works on all OS, no shell scripts needed

### 6. Git Workflow

**Good commits:**
- Commit frequently (not huge changes)
- Write clear messages
- One logical change per commit
- Can revert easily if needed

**Good tags:**
- Tag every release
- Use semantic versioning: `v1.0.0`, `v1.0.1`, `v2.0.0`
- Users can install specific versions

### 7. Testing Saves Time

**Without tests:**
- Make change
- Hope it works
- Deploy
- User finds bug

**With tests:**
- Make change
- Tests verify it works
- Deploy with confidence
- Catch bugs before users do

### 8. Documentation is Code

- `README.md` — What is this?
- `MANUAL.md` — How do I use it?
- `DEVELOPMENT_GUIDE.md` — How do I develop it?
- Code comments — Why does this work?

**Benefit:** Users can help themselves, developers can onboard quickly

---

## Practical Exercise: Create Your Own Package

Now you understand how this package works. Try creating your own:

### 1. **Start Small**

Create a package that calculates stats on some data:

```
my-stats/
├── my_stats/
│   ├── __init__.py
│   ├── calculator.py
│   └── cli.py
├── tests/
│   └── test_calculator.py
├── pyproject.toml
├── README.md
└── .gitignore
```

### 2. **Structure**

- `calculator.py` — Core logic
- `cli.py` — Command-line interface
- `test_calculator.py` — Tests

### 3. **Follow the Pattern**

- Use `@dataclass` for config
- Separate concerns (loading, processing, output)
- Write tests first (TDD)
- Use type hints

### 4. **Deploy**

- Push to GitHub
- Create release
- Install with `pip install git+https://github.com/your-name/my-stats.git`

---

## Resources for Learning

### Python Packaging
- https://packaging.python.org/ — Official guide
- https://setuptools.pypa.io/ — Setuptools docs
- https://python-poetry.org/ — Modern alternative to setuptools

### Testing
- https://docs.pytest.org/ — Pytest docs
- https://en.wikipedia.org/wiki/Test-driven_development — TDD explained

### Git & GitHub
- https://git-scm.com/book/ — Git book (free)
- https://guides.github.com/ — GitHub guides
- https://www.atlassian.com/git/ — Git tutorials

### Design Patterns
- https://refactoring.guru/design-patterns — Design patterns explained
- https://en.wikipedia.org/wiki/Closure_(computer_programming) — Closures explained

---

## Summary

You now understand:

✓ **Project structure** — How to organize a Python package

✓ **Module design** — How to split code into reusable pieces

✓ **Configuration** — How to pass settings instead of using globals

✓ **Testing** — How to verify your code works

✓ **CLI** — How to make command-line tools

✓ **Packaging** — How to make installable packages

✓ **Git** — How to version control and collaborate

✓ **Documentation** — How to help users understand your work

**Next steps:**
1. Read the actual code in the `attendance_generator/` folder
2. Make a small change and see how it flows
3. Run tests to verify changes work
4. Try creating your own package following this pattern

**Remember:** Every professional package you use started exactly like this.

Happy coding! 🎉

