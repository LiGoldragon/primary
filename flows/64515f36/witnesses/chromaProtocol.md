# Chroma protocol witnesses

## Code reads

- `/git/github.com/LiGoldragon/chroma/src/state.rs`: `StateStore` currently persists `ThemeMode` alone under the `theme` table's `current` key. `record_theme` uses the generic archive writer; there is no revision field or state test.
- `/git/github.com/LiGoldragon/chroma/src/daemon.rs`: `ChromaRoot` owns current axes and persists/enqueues accepted theme changes. The daemon serves framed rkyv/DOTOS requests on a Unix socket and has no public D-Bus service or consumer-status registry. Existing D-Bus use is client-side GeoClue/Ghostty integration.
- `/git/github.com/LiGoldragon/chroma/src/theme.rs`: `ThemeMode` is the existing typed Light/Dark value. `ThemeConcern::Emacs`, `ThemeAdapters.emacsclient`, and `EmacsThemeConcern` implement the current one-shot `emacsclient --eval` projection with a two-second timeout and no durable acknowledgement/postcondition.
- `/git/github.com/LiGoldragon/chroma/src/config.rs`: native theme adapter parsing accepts `Emacsclient`; this is the configuration seam that must disappear with the one-shot projection.
- `/git/github.com/LiGoldragon/chroma/{README.md,AGENTS.md,skills.md,ARCHITECTURE.md}` and `tests/config.rs`: documentation and the native fixture still describe/configure the old Emacs concern. `tests/theme.rs` covers other concerns; no state or D-Bus protocol tests exist.
- `/git/github.com/LiGoldragon/chroma/Cargo.toml`, `Cargo.lock`: zbus 5.13.2 is available with tokio support; redb 2.6.3, rkyv 0.8, DOTOS, and Kameo are already the repository's persistence/message foundations.
- `/git/github.com/LiGoldragon/chroma/flake.nix`: the default check runs `cargoTest`; the sandbox check runs a `dbus-run-session` with fake D-Bus services and UDS clients. It is the existing durable integration gate, but currently has no Chroma public service or Emacs consumer case.

## Written-psyche and transcript reads

- `/home/li/primary/flows/01a0238b/reports/emacsAdapterDesign.md` is the accepted design. It settles Chroma semantic authority, a persisted monotonic revision, D-Bus desired-state publication, registration returning the current snapshot, revisioned desired-state signals, typed bounded acknowledgements, and queryable per-consumer `Pending`/`Applied`/`Unavailable`/`Failed` status. It also settles subscriber-first registration, stale-ack rejection, idempotent duplicate-current handling, owner re-registration, and removal of the one-shot path.
- `/home/li/primary/flows/01a0238b/vision/emacsPlugin.md` preserves the psyche's exact words: `1. yes a new public repo.`, `2. the dbus is good.`, `3. yes`, followed by `good enough, approved` after the architecture/semantics were restated.
- `/home/li/.codex/sessions/2026/08/21/rollout-2026-08-21T10-58-38-01a0238b-2c53-76e1-9ae9-5c87f909544f.jsonl` was searched narrowly around the D-Bus proposal. The illustrative `RegisterConsumer("emacs") → (Dark, 42)`, `ThemeChanged(Dark, 43)`, `ReportProjection(...)` names, and the proposed agent anatomy are agent text, not psyche wording. The psyche approved the proposed D-Bus shape and semantics, not a bus name, interface/path, exact method signatures, failure-code vocabulary, bounded byte limit, or identity/security policy.
- `/home/li/primary/psyche-raw/Vision/signalIsOurMessagingLayer.md` and `/home/li/primary/flows/cff271af/reports/psycheOnSoftwareDesignAndNexus.md` establish the general typed-signal/actor-oriented Nexus conventions. The accepted design's explicit D-Bus choice is authoritative for this slice; those records do not silently replace it with a new UDS/two-socket contract.

## State of the inspected worktrees

- Primary `/home/li/primary`: the shared worktree already had unrelated changes in `flows/01a02b46/...`, `flows/01a02b4b/log.md`, and `flows/index.md` when inspected. This subflow added only its own `flows/64515f36/...` artifacts and one index entry.
- Chroma `/git/github.com/LiGoldragon/chroma`: `jj status` showed `.beads/issues.jsonl` added on the current working copy (`mqtkyrpt 34dde605 bd: record Chroma issue`), with parent `vvpwtnnw 329a0edb bd init: initialize beads issue tracking`; no source edits were made by this subflow. Bookmarks observed included `main` at `mxlllmuw eea85f4a chroma: recover warmth ramps from projected state` (remote `@git` behind by four commits at `uozlysxr 227c35e4 docs: mark Protos estate status`), plus `chroma-geoclue-await-and-deploy` and `solar-time-status-bar-chroma`.
