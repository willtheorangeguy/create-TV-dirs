# Known Issues — create-TV-dirs

Concrete defects and gaps found while writing this repository's documentation in
August 2026. **Nothing here was changed** — each one needs a code, configuration, or
licensing decision rather than a documentation one.

Ordered by severity. See [`docs/roadmap.md`](../roadmap.md) for the narrative version,
which also covers deliberate non-goals.

**4 open:** 2 high, 1 medium, 1 low.

## 1. A resolution in the filename is matched as a season number

**Severity:** High
**Where:** `tv_organizer/__main__.py` -> `get_organization_plan`, `season_pattern`

**What:** `season_pattern = re.compile(r'(\d{2})x\d{2}')`, applied with `search`, so it matches anywhere in the filename. Verified against real naming: `Show.1920x1080.mkv` matches on `20x10` and is filed under **Season 20**; `Show.1280x720.x264.mkv` matches on `80x72` and is filed under **Season 80**. Neither file has a season marker at all.

**Why it matters:** Resolutions in filenames are not an edge case -- they are the norm for downloaded video, which is the entire population this tool exists to organise. So on a typical library the tool invents season folders and moves files into them, and because it moves rather than copies, the episodes are gone from where the user left them. The damage compounds with the collision issue below: several files claiming Season 20 land in one folder, and identically-named ones overwrite each other. `--dry-run` does reveal it, but only to someone who reads the plan closely enough to notice a season number they were not expecting.

**Suggested fix:** Require a separator or word boundary before the match -- `(?&lt;![\dx])(\d{2})x(\d{2})(?![\dx])` rejects both resolutions while still accepting `Show.08x01.mkv`. Add the two resolution cases to `test_organizer.py`; `get_organization_plan` is pure, so a case is a filename and an expected mapping.

## 2. Moving a file onto an existing file of the same name replaces it silently

**Severity:** High
**Where:** `tv_organizer/__main__.py` -> `run_cli`, `organize_from_gui`

**What:** `shutil.move(source_path, destination_path)` with no prior existence check and no error handling. When `destination_path` already exists, `shutil.move` overwrites it: `os.rename` replaces silently on POSIX, and where it refuses (Windows, or across filesystems) `shutil` falls back to `copy2` followed by removing the source -- which also overwrites. Neither front end warns, and the summary reports the move as a success.

**Why it matters:** The destination filename is the source filename, so a collision means two files that were both wanted -- a duplicate download, a re-encode, an episode already filed by a previous run of another tool. One of them is destroyed, permanently, with no message and no undo. For a tool whose only action is moving files, silently losing one is the worst outcome available, and it is reachable by simply running the tool twice on a directory that has been partially organised by hand.

**Suggested fix:** Check `os.path.exists(destination_path)` before moving and skip with a warning, or move to a de-duplicated name. Report skipped collisions in the summary so a partial run is visible. The dry run should flag planned collisions too, since that is where a user would want to find out.

## 3. Files that do not match are skipped silently and are not reported

**Severity:** Medium
**Where:** `tv_organizer/__main__.py` -> `get_organization_plan`, `run_cli`

**What:** `get_organization_plan` builds `actions` only from filenames that match the pattern; non-matching files are simply never added. The final line reports `Successfully organized {organized_count} files` -- a count of what moved, never of what was examined or skipped.

**Why it matters:** The most common real input is a directory using `S01E05`, which this pattern does not match at all. Run against it, the tool prints 'No files with the expected season format were found' -- fine. But a **mixed** directory, where some files use `NNxNN` and others do not, organises the matching ones and says nothing about the rest. The user sees a success message and a count they have no reason to check against the directory, and only later notices episodes still loose at the top level.

**Suggested fix:** Count non-matching files in the plan and report them: 'organized 42 files, skipped 18 with no season marker'. Listing the skipped names under `--dry-run` would make the gap obvious at the point it matters.

## 4. Only NNxNN is recognised, not the commoner SNNENN form

**Severity:** Low
**Where:** `tv_organizer/__main__.py` -> `season_pattern`

**What:** The pattern requires two digits, a literal `x`, and two digits. `S01E05` -- the dominant convention in practice -- does not match, and neither does a single-digit form like `1x05`. The README documents the `NNxNN` requirement, so this is a stated limitation rather than a surprise.

**Why it matters:** It is filed low precisely because the failure is safe: unmatched files are left where they are, so an `SNNENN` library is untouched rather than mis-sorted. But it means the tool does nothing at all for most users' collections, and the fix shares its shape with the resolution issue above -- both are about making the pattern precise about what a season marker looks like.

**Suggested fix:** Extend the pattern to accept `S(\d{1,2})E\d{1,2}` and `(\d{1,2})x(\d{1,2})`, case- insensitively, with the boundary guard from the resolution fix. Test all four forms plus the two resolutions together; they interact.

---

## Also, across every repository

**`.bandit` is present on disk but untracked in git.** Verified in PyWorkout, treklogger,
skyscanner-cli, booking-cli, piggy, and aibot — the config file exists locally in each but
`git ls-files` does not know about it, so none of it reached GitHub.

The August 2026 security sweep therefore looks complete locally and landed nowhere. Worth
checking across all 44 repositories it covered.
