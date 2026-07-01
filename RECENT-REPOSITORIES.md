# Recent Repository Index (superseded)

This file no longer carries the repository inventory. The authoritative inventory
of LiGoldragon repos is now `protocols/repos-manifest.nota` — a NOTA manifest that
records, per repo, its name, remote, family, status (`Active` / `Content` /
`Deprecated`), doctrine-home, and fact-flags (`IsFork` / `IsPrivate` /
`BuildTimeConsumed` / `DataRepo`).

Read `protocols/repos-manifest.nota` for what repos exist and their status. A
coverage or doctrine run filters that manifest to `status = Active` and iterates
`/git/github.com/LiGoldragon/<name>` directly. For the smaller human attention map
and per-repo role narrative used during Persona architecture sweeps, read
`protocols/active-repositories.md`.

The former hand-maintained table here had gone stale (it still listed retired or
absent checkouts such as `lojix-cli` and `persona-spirit`) and is retired to avoid
a third, disagreeing inventory surface.

## Archived repositories

Archived repositories are not checked out under `/git`; their checkouts live under
`~/git-archive/github.com/LiGoldragon/` (re-`ghq get` to reactivate) and are out of
scope for the `/git` working-set manifest. See
`gh repo list LiGoldragon --json name,isArchived` for the authoritative archived set.
