# TV Show Organizer — Quickstart

## 1. Dry run

```bash
tv-organizer /path/to/show --dry-run
```

Prints every folder it would create and every file it would move, and changes nothing.

**Read the output before going further.** Check especially that no file has been assigned a
season number that looks like part of a resolution — `Season 20` and `Season 80` are the
give-aways. See [`internal/known-issues.md`](./internal/known-issues.md).

## 2. Organize

```bash
tv-organizer /path/to/show
```

Creates the season folders and moves the files.

## 3. Or just the folders

```bash
tv-organizer /path/to/show --only-create-folders
```

Creates `Season 01`, `Season 02`, and so on, and moves nothing — useful if you would rather move
the files yourself, or with another tool.

## The GUI

```bash
tv-organizer --gui
```

**Browse…** for the directory, tick **Dry Run** or **Only Create Season Folders** if you want
them, then **Organize Files**. The dry-run report appears in a dialog.

## From a checkout

```bash
python -m tv_organizer /path/to/show
```

No install needed.

## What gets matched

The filename must contain `NNxNN` — two digits, an `x`, two digits:

```text
The.Show.08x01.Episode.Name.mkv   → Season 08
The.Show.00x03.Christmas.mkv      → Specials
The.Show.S01E05.mkv               → not matched, left alone
```

`S01E05` is the commoner convention and is **not** recognised. If your files use it, rename them
first or use a different tool — see [FAQ](./faq.md).

## What is skipped

Files with no match are ignored, and the summary counts only what moved. If you expect 60 files
organised and see "Successfully organized 42 files", the other 18 did not match — nothing tells
you which.

Subdirectories are not scanned. Only the top level of the directory you name.
