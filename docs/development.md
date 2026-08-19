# TV Show Organizer — Development

## Setup

```bash
git clone https://github.com/willtheorangeguy/create-TV-dirs.git
cd create-TV-dirs
python -m tv_organizer --help
```

No dependencies to install.

## Tests

```bash
python test_organizer.py -v
```

207 lines covering the planner and the CLI branches, using temporary directories.

`get_organization_plan` returns `(actions, error)` and touches nothing, so most of the behaviour
worth testing needs no filesystem at all — construct filenames, assert on the mapping. That is
where a regression test for the resolution-matching defect belongs:

```python
actions, err = get_organization_plan(dir_with("Show.1920x1080.mkv"))
# currently plans Season 20
```

## Layout

| File | Contents |
|---|---|
| `tv_organizer/__main__.py` | The planner, the CLI, and the GUI |
| `tv_organizer/__init__.py` | Package marker |
| `test_organizer.py` | The suite |
| `Dockerfile` | Container build |

Everything is in one module. At 241 lines that is reasonable; splitting the GUI out would be the
first move if it grows.

## Conventions

- **Keep `get_organization_plan` pure.** It returns a plan and writes nothing. `--dry-run` is
  only trustworthy because the dry run and the real run compute the same plan.
- **Import `tkinter` inside the GUI functions**, not at module scope, so the CLI works without it.
- **Standard library only.** The tool is small enough that a dependency would cost more than it
  buys.
- **Errors as return values.** The planner returns `(None, "message")` rather than raising, so
  both front ends report the same thing their own way.

## If you change the pattern

`(\d{2})x\d{2}` is the whole matching rule, and it is unanchored. Any change should come with
cases for:

- `S01E05` — the common convention, currently unmatched
- `1920x1080`, `1280x720` — resolutions, currently matched as seasons
- `1x05` — single-digit seasons, currently unmatched

See [`internal/known-issues.md`](./internal/known-issues.md).

## Recording defects

Bugs found while working here go in [`internal/known-issues.md`](./internal/known-issues.md)
rather than being fixed in passing, unless fixing them is the job you are on.
