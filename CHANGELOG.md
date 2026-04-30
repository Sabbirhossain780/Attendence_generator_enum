# Changelog

## 1.0.0 — 2026-04-30
### Added
- Interactive setup wizard (terminal step-by-step + Jupyter ipywidgets form)
- CLI: `attendance-gen` launches wizard with no args; direct flags for scripting
- `attendance-gen --version` flag
- Ready-to-run `notebooks/usage_notebook.ipynb`
- Packaged from attendance_generator_v7.ipynb
- Supports .dta / .xlsx / .csv input
- Repeating column headers on every page of attendance table
- Summary page with auto-filled survey days count
- Footer signatures: Enumerator, FA, RA, DA
- GitHub Actions: CI on push, auto GitHub Release on version tag
