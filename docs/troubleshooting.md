# TV Show Organizer — Troubleshooting

## Files went into a season that does not exist

Almost certainly a resolution in the filename. `1920x1080` is read as season 20, `1280x720` as
season 80.

To recover, move them back out of the wrong folder — the filenames are unchanged, so it is
reversible by hand as long as nothing was overwritten.

Recorded in [`internal/known-issues.md`](./internal/known-issues.md). Always `--dry-run` first;
an unexpected `Season 20` in the plan is the tell.

## A file disappeared

If two files with the same name were moved into the same folder, the second replaced the first.
There is no collision check and no undo. Same known-issues file.

## `No files with the expected season format were found`

Your filenames do not contain `NNxNN`. The common `S01E05` form is not recognised — see
[FAQ](./faq.md).

Check the exact form:

```bash
ls /path/to/show
```

`1x05` also fails; the pattern requires two digits on both sides.

## `Error: Directory not found`

The path does not exist or is not a directory. Quote paths containing spaces.

## `No files to organize in the selected directory`

The directory exists but contains no **files** at the top level — only subdirectories, or
nothing. Subfolders are not scanned.

## Fewer files moved than expected

Files that do not match are skipped silently and are not counted. Compare `--dry-run` output
against the directory listing to see what is being ignored.

## `ModuleNotFoundError: No module named 'tkinter'`

Only affects `--gui`. The CLI imports Tkinter lazily and works without it.

```bash
sudo apt install python3-tk        # Debian, Ubuntu
sudo dnf install python3-tkinter   # Fedora
```

## The GUI will not start in Docker

There is no X server in the container. Use the CLI and mount the directory:

```bash
docker run --rm -v /path/to/show:/data tv-organizer /data
```

## `tv-organizer: command not found`

The package is `tv-show-organizer`; the command is `tv-organizer`. If the install succeeded, the
script may not be on your `PATH` — `python -m tv_organizer` works regardless.

## Permission denied while moving

The process needs write access to the directory. On a network share, check the mount is writable
and that nothing has the file open.

## It created folders but moved nothing

You passed `--only-create-folders`. Run again without it.

## Still stuck

[Open an issue](https://github.com/willtheorangeguy/create-TV-dirs/issues/new/choose) with a few
example filenames and the `--dry-run` output — those two together explain most reports.
