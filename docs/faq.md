# TV Show Organizer — FAQ

## Why did some files go into `Season 20` or `Season 80`?

Because their names contain a resolution. The pattern is `NNxNN` and it is unanchored, so
`1920x1080` matches on `20x10` and `1280x720` matches on `80x72`.

Resolutions in filenames are the norm for downloaded video, so this affects a lot of real
libraries. Recorded in [`internal/known-issues.md`](./internal/known-issues.md) — and it is why
`--dry-run` first is worth insisting on.

## Does it handle `S01E05`?

No. Only `NNxNN`. `S01E05` is the more common convention and is left alone entirely, which at
least means nothing is moved wrongly — the files simply are not touched.

## What happens if the destination file already exists?

It is replaced, with no warning. `shutil.move` overwrites an existing destination on both
platforms. Same known-issues file — export or back up before running on a library where
duplicates are likely.

## Is there an undo?

No. Files are moved, not copied, and nothing records what went where. `--dry-run` is the only
safeguard.

## Why does the count not match my file count?

Files with no `NNxNN` match are skipped silently, and the summary counts only what moved. Thirty
of fifty files organised means twenty did not match — and nothing says which.

`--dry-run` lists everything it *would* move, so comparing that against the directory tells you
what is being ignored.

## Does it look in subfolders?

No. Only the top level of the directory you name. That also means running it twice is harmless —
the files it already moved are now one level down and out of scope.

## Can I change the folder names?

Not without editing `tv_organizer/__main__.py`. `Season NN` and `Specials` are literals.

## Why is season 0 called `Specials`?

Because that is the convention media servers use for episodes outside the numbered run —
Christmas episodes, pilots, behind-the-scenes. Plex and Jellyfin both expect it.

## Do I need Tkinter?

Only for `--gui`. It is imported inside the GUI functions, so the CLI works on a machine without
it.

## Can I run it in Docker?

Yes, for the CLI — mount the directory you want organised. The GUI needs an X server. See
[Installation](./installation.md).

## Does it rename files?

No. It only moves them. The filenames are unchanged.

## Does it look anything up online?

No. There is no network code — it reads a directory listing and matches a pattern.

## Why is the package `tv-show-organizer` but the command `tv-organizer`?

They differ, and both are correct. `pip install tv-show-organizer` gives you `tv-organizer`.
