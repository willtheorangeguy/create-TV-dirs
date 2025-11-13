# TV Show Organizer

A Python script with a GUI and CLI to automatically organize your TV show files into season-specific folders.

## Features

-   **GUI Mode**: An easy-to-use graphical interface for selecting a directory and organizing files.
-   **CLI Mode**: A command-line interface for automation and scripting.
-   **Season Detection**: Parses filenames to find season numbers (e.g., `S08E01`, `08x01`).
-   **"Specials" Folder**: Automatically moves episodes from "Season 00" into a `Specials` folder.
-   **Dry Run**: See what changes will be made without modifying any files.
-   **Folder Creation Only**: Create the required season folders without moving any files.

## Prerequisites

-   Python 3.6 or newer. No external libraries are needed.

## Usage

### GUI Mode

To launch the graphical interface, run the script without any arguments:

```bash
python organize_tv_shows.py
```

1.  Click the **"Browse..."** button to select the directory containing your TV show files.
2.  (Optional) Select one of the checkboxes:
    -   **Dry Run**: To see a report of what files will be moved without making any changes.
    -   **Only Create Season Folders**: To create the `Season XX` folders without moving the files.
3.  Click the **"Organize Files"** button to start the process.

### Command-Line Mode

You can also run the script directly from the command line.

**Arguments:**

-   `directory`: (Required) The path to the directory you want to organize.
-   `--dry-run`: (Optional) Show what changes would be made without actually moving or creating anything.
-   `--only-create-folders`: (Optional) Only create the season folders; do not move files.

**Examples:**

-   **To organize a directory:**
    ```bash
    python organize_tv_shows.py "/path/to/your/tv_shows"
    ```

-   **To perform a dry run:**
    ```bash
    python organize_tv_shows.py "/path/to/your/tv_shows" --dry-run
    ```

-   **To only create the season folders:**
    ```bash
    python organize_tv_shows.py "/path/to/your/tv_shows" --only-create-folders
    ```
