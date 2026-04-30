# Attendance Sheet Generator — Simple User Guide

**Created by BRAC Institute of Governance and Development (BIGD)**

---

## What Does This Tool Do?

Think of this tool like a **magic helper that fills out forms for you**.

Instead of typing attendance sheets by hand for every person, you just:
1. Give it a list of people and dates
2. Click a button
3. It creates all the forms automatically ✓

**What you get:**
- Word documents (attendance sheets for each person)
- Excel file (checklist of who worked when)

No typing required. No magic needed. Just click and wait!

---

## How to Install (First Time Only)

### The Easy Way (No Command Line)

**If you're not comfortable using Command Prompt:**

1. Open the file named `usage_notebook.ipynb`
2. Click the ▶ button next to the instructions
3. Fill in the form that appears
4. Click "Generate"
5. Done!

### The Command Prompt Way

**Step 1:** Open Command Prompt
- Click Start menu
- Search for "Command Prompt"
- Click it to open

**Step 2:** Copy and paste this:
```
pip install --upgrade git+https://github.com/Sabbirhossain780/Attendence_generator_enum.git
```

**Step 3:** Press Enter and wait

When it says "Successfully installed", you're done!

### Check If It Worked

Type this and press Enter:
```
attendance-gen --version
```

You should see: `attendance-gen 1.0.0`

If you see that, it worked! ✓

---

## How to Use It

### Method 1: Using the Form (Easiest)

1. Open `usage_notebook.ipynb` in a web browser
2. Click the green "Run" button on the first cell
3. A form pops up
4. Fill in:
   - **Input file** = Your data file (Excel, CSV, or Stata)
   - **Output folder** = Where to save the forms
   - **Logo** = Your picture (optional)
   - **Organization** = Your company name
   - **Weekend** = Which day is weekend (usually Friday)
   - **Holidays** = Special days off (optional)

5. Click "Generate Attendance Sheets"
6. Wait a few seconds
7. Open the Output folder to see your files

### Method 2: Using Questions (Command Prompt)

**Step 1:** Open Command Prompt and type:
```
attendance-gen
```

**Step 2:** Answer the questions:

```
Path to your survey dataset: data.xlsx
```
Just type the name of your file.

```
Output folder [./attendance_output]:
```
Press Enter to use the default folder.

```
Logo image path (leave blank to skip):
```
Press Enter to skip, or type your logo file name.

Continue answering the questions (8 total). Most have defaults, so you can just press Enter.

**Step 3:** Review the summary and press Enter to create

**Step 4:** Your files are ready!

### Method 3: Advanced (For Experts)

If you know Command Prompt well:

```
attendance-gen --input data.xlsx --output ./output --weekend "friday,saturday"
```

---

## Prepare Your Data

Your data file needs these columns (they can have similar names):

| What | Examples | Do I Need It? |
|------|----------|---------------|
| **Person ID** | 3753, 4059, EMP001 | YES |
| **Person Name** | Md Zubaer, Alice Khan | YES |
| **Start Date** | 2025-12-01 | YES |
| **End Date** | 2025-12-15 | NO (optional) |
| **Location** | Dhaka, Sylhet | NO (optional) |

### Date Formats (All Work)

Any of these is fine:
- `2025-12-01` (best)
- `01/12/2025`
- `12/01/2025`
- `1-Dec-2025`

Just pick one and use it everywhere.

### Example Data

**Simple version:**
```
ID,Name,Start
3753,Md Zubaer,2025-12-01
4059,Iqbal Hossain,2025-12-01
```

**Full version:**
```
ID,Name,Start,End,Location
3753,Md Zubaer,2025-12-01,2025-12-11,Dhaka
4059,Iqbal Hossain,2025-12-01,2025-12-10,Dhaka
```

---

## What Files Do You Get?

### Word Documents (Attendance Sheets)

**File name:** `3753_Md_Zubaer_attendance.docx`

**What's in it:**
- Person's name and ID
- Calendar with dates
- Space to mark "Survey", "Training", "Holiday", etc.
- Signature boxes at the bottom
- Summary page with counts

**You can edit these!** Add notes, signatures, or changes anytime.

### Excel File (Quality Check)

**File name:** `_QC_Summary.xlsx`

**What's in it:**

**Sheet 1 - Color Grid:**
```
Name              | 1 Dec | 2 Dec | 3 Dec
Md Zubaer         | Green | Gray  | Green
Iqbal Hossain     | Green | Green | Blue
```

Colors mean:
- 🟢 Green = Survey day
- 🟡 Yellow = Training day
- 🟦 Blue = Office work
- ⬜ White = Off day
- ⬛ Gray = Weekend/Holiday

**Sheet 2 - Statistics:**
```
Name              | Survey Days | Training Days | Weekends
Md Zubaer         | 10          | 2             | 2
Iqbal Hossain     | 9           | 1             | 2
```

Quick way to check if everything looks right!

---

## Customize Your Settings

### Change the Weekend Day

By default, Friday is the weekend.

If you want Friday AND Saturday:

**In the form:** Type `friday,saturday`

**In Command Prompt:**
```
attendance-gen --weekend "friday,saturday"
```

### Add Holidays

Mark special days off:

**One day:**
```
--holidays "2025-12-25"
```

**Multiple days:**
```
--holidays "2025-12-25, 2025-01-01"
```

**A range:**
```
--holidays "2025-12-20:2025-12-27"
```

This marks Dec 20 through Dec 27 as holidays.

### Add Your Logo

Put your organization's picture in the header:

```
--logo "C:\Users\YourName\Pictures\mylogo.png"
```

**The picture must be:** PNG or JPG file

### Blank Rows at the Start

Add empty rows before the first day (for writing things in by hand):

```
--pre-survey-days 5
```

This adds 5 blank rows at the top.

---

## Questions & Answers

### Q: It says "File not found"

**A:** Use the full path to your file.

**Windows example:**
```
C:\Users\YourName\Documents\data.xlsx
```

Or navigate to the folder first, then use just the filename.

---

### Q: Can I change the organization name?

**A:** Yes!

```
--org1 "My Organization"
--org2 "My Division"
```

---

### Q: How long does it take?

**A:**
- 10 people = 5-10 seconds
- 50 people = 30 seconds
- 100 people = 1 minute

---

### Q: Can I edit the documents after?

**A:** YES! They're normal Word and Excel files. Add notes, signatures, changes — whatever you want.

---

### Q: What if someone has multiple date ranges?

**A:** The tool handles it automatically. One person, multiple date ranges = one document with blank space in between.

---

### Q: How do I update the tool to get new features?

**A:**
```
pip install --upgrade git+https://github.com/Sabbirhossain780/Attendence_generator_enum.git
```

---

## Problems & Fixes

### Problem: File not found

**What to do:**
1. Make sure the file actually exists
2. Copy the full path from Windows File Explorer
3. Paste it into the tool

---

### Problem: Column names not recognized

**What to do:**

Option 1: Rename your columns to:
- `ID` or `enu_code` or `enum_id`
- `Name` or `enu_name`
- `Start` or `startdate`

Option 2: Check your column names match common patterns.

---

### Problem: Dates don't work

**What to do:**

1. Use same date format everywhere
2. In Excel: Right-click cells → Format as Date
3. In CSV: Use `2025-12-01` format

---

### Problem: Logo doesn't appear

**What to do:**

1. Make sure the file exists
2. Make sure it's PNG or JPG
3. Use the full path

---

### Problem: Weird letters show up (Windows)

Type this in Command Prompt first:
```
chcp 65001
```

Then run the tool again.

---

## Simple Steps to Success

### Your First Time:

1. Get your data file ready
   - Make sure it has columns for: ID, Name, Start Date
   - Make sure all dates are filled in
   - Check for extra spaces in names

2. Open Command Prompt

3. Type: `attendance-gen`

4. Answer the 8 questions
   - For most questions, just press Enter for defaults
   - Only required: your data file path

5. Press Enter when it asks to generate

6. Check the "Output folder" for your files

7. Open the Word and Excel files

**That's it!** You're done.

---

## Tips to Remember

✓ **Test first:** Use `--demo` to generate for just one person first:
```
attendance-gen --input data.xlsx --demo
```

✓ **Clean data:** Remove extra spaces, fix dates, check for blanks

✓ **Use short paths:** Put your file on Desktop or Documents for easy paths

✓ **Save your data:** Keep your original Excel/CSV file as backup

✓ **Use Excel QC sheet:** Check the color grid to spot problems quickly

✓ **You can edit outputs:** Add signatures and notes to the Word documents

---

## What If You Get Stuck?

1. **Read the error message** — it usually tells you what's wrong
2. **Check your data** — missing columns? Wrong date format?
3. **Try the help command:**
   ```
   attendance-gen --help
   ```
4. **Ask someone** — show them the error message

---

## Summary: What Just Happened?

You installed a tool that:
- Takes a list of people and dates
- Creates professional attendance forms
- Saves them as Word and Excel files
- Saves you hours of typing

No magic, just automation. ✓

**You're ready to use it!**

---

**Version:** 1.0.0

**Made by:** BIGD, BRAC University

**License:** MIT (free to use)

