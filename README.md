# TV Show Organizer

Automatically organize your TV show files into season-specific folders.

`tv-organizer` scans a directory for video files whose names contain a
season/episode marker (e.g. `08x01`) and sorts them into `Season 08`,
`Season 01`, etc. Episodes from season `00` are moved into a `Specials`
folder instead.

## Features

- **CLI mode** for scripting and automation.
- **GUI mode** (Tkinter) for point-and-click use.
- **Season detection** via the `NNxNN` pattern (e.g. `08x01`, `01x05`).
- **"Specials" folder**: season `00` is mapped to `Specials` instead of `Season 00`.
- **Dry run**: preview the planned moves without touching any files.
- **Folder-creation-only mode**: create the season folders without moving files.

## Installation

Requires Python 3.8+. No external dependencies.

```bash
pip install tv-show-organizer
```

This installs the `tv-organizer` command. Alternatively, install from a
local clone:

```bash
git clone https://github.com/willtheorangeguy/create-TV-dirs.git
cd create-TV-dirs
pip install .
```

## Usage

### CLI mode

```bash
tv-organizer <directory>                     # organize files in-place
tv-organizer <directory> --dry-run           # preview only, no changes
tv-organizer <directory> --only-create-folders  # create season folders, don't move files
```

If you haven't installed the package, you can run it directly from a
checkout with:

```bash
python -m tv_organizer <directory>
```

### GUI mode

```bash
tv-organizer --gui
```

1. Click **"Browse..."** to select the directory containing your TV show files.
2. (Optional) Check **Dry Run** to preview the plan, or **Only Create Season Folders**
   to create folders without moving files.
3. Click **"Organize Files"**.

## Development

```bash
git clone https://github.com/willtheorangeguy/create-TV-dirs.git
cd create-TV-dirs
python test_organizer.py -v
```

## License

MIT — see [LICENSE](LICENSE).
