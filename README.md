# Codex lane-index snapshot proposal

This is a private, reviewable snapshot for the `cf7879` primary flow. It is
not an installation, a live registry, or a command to launch a Codex session.

## Use after review

Package `codex-layer-index.json` with the guarded `codex-primary` and
`codex-secondary` wrappers. A user can then either set
`CODEX_LAYER_INDEX=/path/to/codex-lane-index.json`, or place the approved file
at `${XDG_CONFIG_HOME:-$HOME/.config}/codex/lane-index.json`. The wrapper's
`--registry PATH` option has priority over both locations.

The primary wrapper then needs no arguments:

```text
codex-primary
codex-secondary
```

Each wrapper resolves only a `state: "current"` record with
`authority.kind: "lane-index"` and an exact UUID, then runs
`codex resume <threadId>`. It refuses title-only selection. If the child ends
from a signal, the wrapper re-raises that signal rather than reporting an
invented numeric success or failure.

## Snapshot contract

`observedAt` says when this identity was recorded; it does not establish live
freshness. On every layer refresh, replace the entire reviewed index with a
new snapshot, update the provenance and observed time, and mark retired
records non-current if they are retained elsewhere. Do not mutate this file
based on a thread title or an app-server `thread/list` result.

The app-server's read-only thread metadata has no semantic `layer` or
current-generation field, so it cannot by itself choose one of these records.

## Provenance limits

The two thread IDs are the supplied lane identities. Their source is recorded
as `flows/efa157/log.md` at claimed source revision `2265e56a`; that revision
was not locally present in this primary checkout during this proposal. The
record is therefore evidence for review, not a claim of live remote authority.
