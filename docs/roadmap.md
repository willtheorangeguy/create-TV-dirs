# TV Show Organizer — Roadmap

Direction, not a schedule. Defects are in
[`internal/known-issues.md`](./internal/known-issues.md).

## Where it is

Scans a directory, plans, and moves — with a dry run, a folders-only mode, a CLI, a GUI, and
tests. Standard library only.

## Considered

**Not matching resolutions as seasons.** The most important fix. Requiring a word boundary or a
separator before the pattern would stop `1920x1080` becoming season 20, which is currently the
tool's most damaging behaviour on real libraries.

**Supporting `S01E05`.** The commoner convention, and unrecognised. Doing it properly means
handling both forms and keeping them apart from resolutions — the same change as above.

**A collision check before moving.** Replacing an existing file silently is the other thing worth
fixing before anything cosmetic.

**Reporting what was skipped.** Files that do not match are invisible in the output; listing them
would make a partial run obvious.

**Single-digit seasons.** `1x05` is not matched.

**Recursion, or a `--recursive` flag.** Top-level only today.

## Non-goals

**Renaming files.** It moves them and leaves the names alone. Renaming is a separate, much
riskier operation, and there are tools that do it well.

**Looking anything up online.** No metadata APIs, no episode titles, no network. The filename is
the only input, which is what keeps this small and predictable.

**Becoming a media manager.** Sonarr and its relatives exist. This sorts a folder you already
have.

**Guessing.** A file with no recognisable marker is left alone rather than assigned a best-guess
season. Given that the tool moves files, declining to act is the right default — and the reason
the unmatched-file behaviour is a reporting gap rather than a correctness one.

**An undo log.** Worth considering only if renaming or recursion is ever added; for a top-level
move, the filenames are unchanged and reversing by hand is straightforward.

## Contributing

Issues and pull requests welcome — see the
[Contributing Guide](https://github.com/willtheorangeguy/.github/blob/main/CONTRIBUTING.md).

The pattern change is small and well covered by the existing test structure —
`get_organization_plan` is pure, so a case is a filename and an expected mapping.
