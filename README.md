<!-- Logo -->
<h1 align="center">TV Show Organizer</h1>

<!-- Copy -->
<h4 align="center">Sorts a folder of TV episodes into season folders, by reading the season number out of each filename.</h4>

<!-- Badges -->
<div align="center">
  <img alt="GitHub Issues" src="https://img.shields.io/github/issues/willtheorangeguy/create-TV-dirs">
  <img alt="GitHub Pull Requests" src="https://img.shields.io/github/issues-pr/willtheorangeguy/create-TV-dirs">
  <img alt="License" src="https://img.shields.io/github/license/willtheorangeguy/create-TV-dirs">
</div>

<!-- Navigation -->
<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#support">Support</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>

## Key Features

- Reads the `NNxNN` marker in a filename — `08x01` means season 8 — and moves the file into `Season 08`.
- Season `00` goes to `Specials`.
- **Dry run** prints the whole plan and changes nothing.
- Folder-creation-only mode, if you would rather move the files yourself.
- CLI for scripting, Tkinter GUI for clicking.
- Python 3.8+, standard library only.

## Installation

```bash
pip install tv-show-organizer
```

Or from a clone: `pip install .`. See [`docs/installation.md`](docs/installation.md).

## Usage

```bash
tv-organizer <directory> --dry-run              # always start here
tv-organizer <directory>                        # move the files
tv-organizer <directory> --only-create-folders  # folders only
tv-organizer --gui                              # point and click
```

> **Run `--dry-run` first, every time.** Two things make that worth insisting on: a filename containing a resolution like `1920x1080` is read as season 20, and a file moved onto an existing file of the same name replaces it. Both are recorded in [`docs/internal/known-issues.md`](docs/internal/known-issues.md).

## Documentation

Full documentation lives in [`docs/`](docs/README.md):
[Quickstart](docs/quickstart.md) · [Installation](docs/installation.md) · [Configuration](docs/configuration.md) · [Architecture](docs/architecture.md) · [Development](docs/development.md) · [FAQ](docs/faq.md) · [Troubleshooting](docs/troubleshooting.md) · [Roadmap](docs/roadmap.md)

## Support

Open a [GitHub Discussion](https://github.com/willtheorangeguy/create-TV-dirs/discussions/new) or file an [issue](https://github.com/willtheorangeguy/create-TV-dirs/issues/new/choose).

## Contributing

Contributions welcome. See the org-wide [Contributing Guide](https://github.com/willtheorangeguy/.github/blob/main/CONTRIBUTING.md) and [Code of Conduct](https://github.com/willtheorangeguy/.github/blob/main/CODE_OF_CONDUCT.md).

## Credits

Standard library only — `os`, `re`, `shutil`, `argparse`, and Tkinter for the GUI.

## License

MIT — see [`LICENSE`](LICENSE).
