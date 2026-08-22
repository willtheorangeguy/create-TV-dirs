# TV Show Organizer — Architecture

One module, 241 lines, three parts: a planner, a CLI, and a GUI.

```text
get_organization_plan(directory)   →  {folder: [filenames]}
        ├── run_cli(args)          →  print, or create, or move
        └── organize_from_gui(...) →  the same, in dialogs
```

## `get_organization_plan`

The only piece of real logic, and deliberately **pure**: it lists the directory, matches each
filename against the season pattern, and returns a mapping of destination folder to file list —
plus an error string, or `None`.

```python
return actions, None      # or None, "Error: Directory not found at ..."
```

It writes nothing. That is what makes `--dry-run` trustworthy: the dry run and the real run
compute the same plan, and only the caller differs. A tool that moves files should be built this
way.

It is also the natural place for tests, and where the two recorded defects live — see
[`internal/known-issues.md`](./internal/known-issues.md).

## The season pattern

```python
season_pattern = re.compile(r'(\d{2})x\d{2}')
```

Applied with `search`, so it matches anywhere in the name. Group 1 is the season; `00` maps to
`Specials`.

Unanchored matching is what lets `1920x1080` register as season 20.

## `run_cli`

Three branches over the same plan:

| Flag | Does |
|---|---|
| `--dry-run` | Prints the plan and returns |
| `--only-create-folders` | `os.makedirs` for each folder, then returns |
| neither | Creates folders and `shutil.move`s each file |

The move has no collision check:

```python
shutil.move(source_path, destination_path)
```

If `destination_path` already exists, it is replaced — on both platforms, since `shutil.move`
falls back to `copy2` when `os.rename` refuses. Same known-issues file.

## `organize_from_gui`

The same three branches, reporting through `messagebox` instead of `print`. `tkinter` is imported
**inside** the function rather than at module scope, so the CLI runs on a machine with no Tkinter
installed — a small thing, and the right call for a tool whose main use is headless.

`run_gui` builds the window: a directory entry with **Browse…**, two checkboxes, and
**Organize Files**.

## `main`

`argparse`, then a three-way dispatch: `--gui`, a directory, or help.

## Testing

`test_organizer.py` (207 lines) exercises the planner and the CLI paths with temporary
directories.

Because `get_organization_plan` is pure and returns data, it can be tested by constructing
filenames and asserting on the mapping — no filesystem needed for the interesting half.

## What it does not do

No recursion, no renaming, no metadata lookup, no undo. It reads a directory listing, matches a
pattern, and moves files — which is the right scope, and the reason the whole thing is one small
module.
