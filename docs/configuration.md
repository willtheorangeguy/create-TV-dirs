# TV Show Organizer — Configuration

No configuration file and no environment variables. Four flags, and one naming rule.

## Flags

| Flag | Effect |
|---|---|
| `directory` | The folder to organise. Required unless `--gui` |
| `--dry-run` | Print the plan; change nothing |
| `--only-create-folders` | Create the season folders, move no files |
| `--gui` | Launch the Tkinter interface |

With no directory and no `--gui`, it prints help and points you at `--gui`.

`--dry-run` and `--only-create-folders` are checked in that order, so passing both gives you the
dry run.

## The naming rule

One regular expression, in `get_organization_plan`:

```python
season_pattern = re.compile(r'(\d{2})x\d{2}')
```

Two digits, a literal `x`, two digits. The **first** two digits are the season.

| Filename | Season | Destination |
|---|---|---|
| `Show.08x01.mkv` | `08` | `Season 08` |
| `Show.00x03.mkv` | `00` | `Specials` |
| `Show.1x05.mkv` | — | not matched; single digits fail |
| `Show.S01E05.mkv` | — | not matched |
| `Show.1920x1080.mkv` | `20` | **`Season 20`** — see below |

### The pattern is not anchored

`search` is used, so the match can occur anywhere in the name — including inside a resolution.
`1920x1080` contains `20x10`; `1280x720` contains `80x72`. Resolutions are extremely common in
downloaded filenames, and those files are filed under invented seasons.

Recorded in [`internal/known-issues.md`](./internal/known-issues.md). `--dry-run` reveals it
immediately: a `Season 20` or `Season 80` in the plan that you did not expect.

### `S01E05` is not supported

The dominant convention in practice, and not recognised. Only `NNxNN`. Changing the pattern is a
one-line edit in `__main__.py`, though doing it properly means handling both forms and
disambiguating from resolutions.

## Folder names

| Season | Folder |
|---|---|
| `00` | `Specials` |
| Anything else | `Season NN`, keeping the leading zero |

`Season 08`, not `Season 8` — the zero comes straight from the filename.

## Scope

Top-level files only. Subdirectories are not scanned and not recursed into, so running it twice
on the same directory does not re-sort what it already moved.

## What is not configurable

The pattern, the folder naming, the `Specials` mapping, and the destination root. All are
literals in `tv_organizer/__main__.py`.
