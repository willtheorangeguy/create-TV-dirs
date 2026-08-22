# TV Show Organizer — Documentation

A small tool that reads a season number out of each filename and moves the file into the matching
season folder.

```text
create-TV-dirs/
├── tv_organizer/
│   ├── __init__.py     package marker
│   └── __main__.py     everything: plan, CLI, GUI
├── test_organizer.py
├── Dockerfile
└── docs/               this documentation
```

## Pages

- [Quickstart](./quickstart.md) — a dry run, then the real thing
- [Installation](./installation.md) — pip, a clone, or Docker
- [Configuration](./configuration.md) — the flags and the naming rule
- [Architecture](./architecture.md) — plan, then act
- [Development](./development.md) — tests and layout
- [FAQ](./faq.md) — naming schemes, safety, what is skipped
- [Troubleshooting](./troubleshooting.md) — wrong folders, missing files
- [Roadmap](./roadmap.md) — direction and non-goals
- [Known issues](./internal/known-issues.md) — recorded defects

## Read this before running it on a real library

Two recorded defects matter here, because this tool moves files:

**A resolution in the filename is read as a season number.** The pattern is `NNxNN`, and
`Show.1920x1080.mkv` contains `20x10` — so it is filed under `Season 20`. `1280x720` gives
`Season 80`. Resolutions in filenames are the norm for downloaded video.

**Moving a file onto an existing file of the same name replaces it.** There is no collision
check.

Both are in [`internal/known-issues.md`](./internal/known-issues.md). `--dry-run` shows you the
plan and changes nothing — use it every time.

## How it decides

One regular expression: `(\d{2})x\d{2}`. The first two digits are the season.

| Filename contains | Goes to |
|---|---|
| `08x01` | `Season 08` |
| `00x03` | `Specials` |
| No `NNxNN` match | Left alone |

Note what is **not** matched: `S01E05`, the most common convention in practice. See
[FAQ](./faq.md).

## What it touches

Only the top level of the directory you name — no recursion — and only files whose names match.
Everything else is left where it is, silently.
