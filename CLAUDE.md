# CLAUDE.md

## Project Overview

**tv-show-organizer** is a Python CLI/GUI tool that organizes TV show files into season-specific folders based on filename patterns (e.g., `08x01` → `Season 08`). Season `00` maps to a `Specials` folder.

## Repository Structure

```
tv_organizer/          # Main package
  __main__.py          # All application code: core logic, CLI, and tkinter GUI
  __init__.py          # Package marker
test_organizer.py      # Unit + integration tests (unittest)
pyproject.toml         # Package metadata and build config (setuptools)
Dockerfile             # Container image definition
.github/workflows/
  ci.yml               # Runs tests on Python 3.8–3.12
  release.yml          # Release workflow
.github/agents/        # GitHub agent prompt files
```

## Commands

### Run tests
```
python test_organizer.py -v
```
No test framework install needed — uses stdlib `unittest`.

### Run the tool
```
python -m tv_organizer <directory>          # CLI mode
python -m tv_organizer <directory> --dry-run
python -m tv_organizer <directory> --only-create-folders
python -m tv_organizer --gui               # GUI mode (requires tkinter)
```

### Install as package
```
pip install .
tv-organizer <directory>
```

## Architecture

All logic lives in `tv_organizer/__main__.py`:
- `get_organization_plan(directory)` — scans files, returns `(actions_dict, error_string)` tuple
- `run_cli(args)` — CLI entry point
- `run_gui()` / `organize_from_gui()` — tkinter GUI
- `main()` — argparse dispatcher

The season pattern regex is `(\d{2})x\d{2}` (e.g., `01x05`).

## Conventions

- Python 3.8+ compatibility (no walrus operator, no `match` statements)
- No external dependencies — stdlib only (`os`, `re`, `shutil`, `argparse`, `tkinter`)
- Tests use `unittest` with `setUp`/`tearDown` creating temp directories
- Integration tests invoke the module via `subprocess.run([sys.executable, "-m", "tv_organizer", ...])`
- CI runs `python test_organizer.py -v` directly (no pytest)

## Key Patterns

- `get_organization_plan` returns `(None, error_message)` on failure or `(actions_dict, None)` on success — always check both return values
- The `actions` dict maps folder names (`"Season 01"`, `"Specials"`) to lists of filenames
- GUI imports (`tkinter`) are deferred to function scope to avoid import errors on headless systems
