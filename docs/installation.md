# TV Show Organizer — Installation

## Requirements

| | |
|---|---|
| Python | 3.8 or newer |
| Dependencies | None — standard library only |
| Tkinter | Only for `--gui` |

## From PyPI

```bash
pip install tv-show-organizer
```

Installs the `tv-organizer` command. Note the package name and the command differ.

## From a clone

```bash
git clone https://github.com/willtheorangeguy/create-TV-dirs.git
cd create-TV-dirs
pip install .
```

## Without installing

```bash
python -m tv_organizer /path/to/show
```

Works from a checkout with no install at all.

## Docker

A `Dockerfile` is included. Remember to mount the directory you want organised:

```bash
docker build -t tv-organizer .
docker run --rm -v /path/to/show:/data tv-organizer /data
```

The GUI will not work in a container without an X server; use the CLI.

## Tkinter for the GUI

Bundled with Python on Windows and macOS. On Linux:

```bash
sudo apt install python3-tk        # Debian, Ubuntu
sudo dnf install python3-tkinter   # Fedora
```

The CLI needs none of this — `tkinter` is imported inside the GUI functions, not at module
level, so the command works on a machine without it.

## Verify

```bash
tv-organizer --help
tv-organizer /some/folder --dry-run
```

The dry run is the real check: it exercises the scan and the plan without touching anything.

## Tests

```bash
python test_organizer.py -v
```

## Uninstall

```bash
pip uninstall tv-show-organizer
```

Nothing is written outside the directories you point it at — no config, no cache.
