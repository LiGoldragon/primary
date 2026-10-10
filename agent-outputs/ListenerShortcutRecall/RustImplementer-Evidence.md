# Listener Transcript History + Recall — Rust Implementation Evidence

Phase 2 of the ListenerShortcutRecall plan: persist each successful transcript
to a private local history store and add a recall path that re-selects a past
transcript and copies it to the clipboard.

## Task And Scope

Repo: `listener` (its own code repo, not primary) at
`/git/github.com/LiGoldragon/listener`, jj-managed, pushed to
`origin` `main`. Built on the Scout map at
`agent-outputs/ListenerShortcutRecall/Scout-SituationalMap.md`.

Delivered: a typed transcript history store (JSONL projection), a Listener-owned
`listener-recall` binary using a `fuzzel --dmenu` picker, a version bump to
`0.6.0`, and tests plus objective end-to-end evidence. The working
record -> transcribe -> clipboard path and typed cancel semantics are unchanged;
a cancelled capture writes no history entry.

## Recall Approach Decision — Listener-owned recall (not whisrs-recall reuse)

Chose a **Listener-owned recall** (`listener-recall` binary + `src/recall.rs`),
not reuse of the whisrs-recall drop-in.

The brief said to prefer the drop-in only if Listener can emit the *identical*
whisrs JSONL schema without contortions. It cannot:

- The whisrs schema is `{timestamp: DateTime<Local> (RFC3339), text, backend,
  language, duration_secs}`. Listener has no `backend`, `language`, or
  `duration_secs` concept; emitting them would mean fabricating meaningless
  fields, and matching chrono's `DateTime<Local>` serde format would force a new
  `chrono` dependency purely for wire-format parity.
- Reuse also means the recall keybind spawns a whisrs binary with the `whisrs> `
  prompt branding, coupling two independently-versioned tools across the criomos
  fork boundary. The workspace component discipline (component-architecture /
  micro-components) says a component owns its own capability surface and typed
  storage.

The Scout map independently recommended this option (Area 3, option c). The
extra cost is a ~120-line recall module that mirrors whisrs-recall's pattern;
in exchange Listener owns its history schema natively (carrying its own session
metadata) and stays independently versionable. Net: less contortion, no new
dependency, no cross-fork runtime coupling, same fuzzel dmenu UX.

The recall binary reads the history JSONL **directly** and does not open the
daemon path — matching whisrs-recall, and meaning recall works even while
`listener.service` is stopped. This is a deliberate design point: the daemon
(runtime) owns history *writes*; recall is a read-only projection reader.

## History Store Design (storage discipline)

- Typed store in Rust; JSON line is the human/interchange projection
  (per rust-storage-and-wire). `TranscriptHistoryEntry` is the typed record;
  a private serde `TranscriptHistoryLine` DTO is the JSON boundary.
- Location: `$XDG_DATA_HOME/listener/history.jsonl` (typically
  `~/.local/share/listener/history.jsonl`), overridable with
  `LISTENER_HISTORY_STORE`. This matches the whisrs precedent (XDG *data* dir)
  and keeps durable browsable user data out of the capture *state* dir.
- Schema per line: `{"unix_millis":<i64>,"session":<u64>,"text":<string>}`.
  At least a timestamp and the transcript text (the brief's minimum), plus the
  capture session as metadata. Timestamp is Unix milliseconds — a standard
  machine-interchange timestamp — chosen over RFC3339 to avoid pulling in chrono
  for a field the picker never displays (whisrs-recall shows only the preview).
- Privacy: spoken content, local only, no external transmission. The directory
  is created `0700` and the file `0600` (enforced on every append even if it
  pre-existed looser), matching the whisrs history's owner-only mode.
- Reads: newest-first (file order reversed), truncated to a `HistoryLimit`;
  a missing store reads as empty; a malformed line is skipped rather than
  failing the whole read.

## Where History Is Written (and why it is non-fatal)

`src/runtime.rs` `stop()` appends the entry right after a successful transcript
is obtained (before delivery), via `record_transcript_history`. Placing it
before delivery means recall captures the transcript even if clipboard delivery
fails — which is exactly when recall is most valuable. `cancel()` never calls it.

History append is **best-effort**: the transcript is already in the typed
`Output::Stopped` reply and about to be delivered, so a history-write failure
must not abort the stop or drop the transcript. (The `Output::Stopped` contract
has no field to surface a history outcome, and failing the stop would falsely
tell the user the whole capture failed.) The failure is swallowed with a comment
documenting the choice; the transcript path is unaffected.

## Changed / Added Files

New:
- `src/history.rs` — `TranscriptHistoryStore`, `TranscriptHistoryEntry`,
  `HistoryTimestamp`, `HistoryLimit`, and the private `TranscriptHistoryLine`
  JSON projection.
- `src/recall.rs` — `TranscriptRecall`, `RecallSelector`, `RecallOutcome`, and
  the private `RecallSelection`. Reuses the existing `ClipboardCommand` seam to
  copy the pick.
- `src/bin/listener_recall.rs` — thin `listener-recall` entry point.
- `tests/history.rs` — 5 tests (append/read-back newest-first, limit truncation,
  multiline round trip, owner-only `0700`/`0600` permissions, empty-store read).
- `tests/recall.rs` — 3 tests (read->select->copy end to end via stub selector
  and clipboard programs, empty history, cancelled selection).

Modified:
- `src/runtime.rs` — `history_store` field + `with_dependencies` param;
  `record_transcript_history` on successful stop; history-error classification.
- `src/lib.rs` — module declarations and re-exports; exported `ClipboardCommand`.
- `src/error.rs` — `HistoryEntryEncode`, `HistoryEntryDecode`,
  `RecallSelectorUnavailable` typed variants.
- `tests/runtime.rs` — fixture injects a temp-dir history store; stop test
  asserts the transcript is appended; cancel test asserts history is untouched
  and the store file is never created.
- `Cargo.toml` — version `0.5.1` -> `0.6.0`; new `listener-recall` bin.
- `Cargo.lock` — package version bump to `0.6.0`.
- `flake.nix` — `recall` app; `test-history` and `test-recall` checks.
- `README.md`, `ARCHITECTURE.md`, `skills.md` — feature, env knobs, code map.

New env knobs: `LISTENER_HISTORY_STORE`, `LISTENER_RECALL_SELECTOR`.

## Version — 0.6.0; signal-listener UNCHANGED

Minor bump `0.5.1 -> 0.6.0` (user-facing feature). Only Cargo.toml/Cargo.lock
carry the version string; no other version surface. **The `signal-listener`
contract does NOT change**: recall reads the transcript from the existing
`Output::Stopped.transcript_text` field and the history store, so no new wire
operation or reply is needed. `signal-listener` stays at `0.4.0`.

## Verification Results

Inner-loop (cargo), all from `/git/github.com/LiGoldragon/listener`:

- `cargo build --all-targets` — PASS (clean, `listener v0.6.0`).
- `cargo test` — PASS, 33 tests: lib 1, history 5, recall 3, runtime 17,
  recording_log 4, capture 2, configuration 1, doc 0.
- `cargo clippy --all-targets --all-features -- -D warnings` — PASS (no warnings).
- `cargo fmt --check` — PASS.

Objective end-to-end run of the compiled `listener-recall` binary
(`target/debug/listener-recall`), driven non-interactively via env stubs:

- Seeded `history.jsonl` with two entries; selector stub chose index 0 (newest);
  clipboard stub recorded the copied text. Result: binary exit 0, printed
  "copied selected transcript to the clipboard", and the clipboard file held the
  newest transcript ("schedule the dentist for tuesday") — the FULL text, not
  the preview.
- Empty history (`LISTENER_HISTORY_STORE` pointing at a missing file): binary
  exit 0, printed "no transcript history yet", clipboard file never created.

Cancel-untouched confirmation:

- `tests/runtime.rs::cancel_stops_capture_retains_artifact_and_skips_transcription_and_delivery`
  now also asserts `recorded_history().is_empty()` and that the history store
  file does not exist after a cancel — PASS.

Durable Nix evidence (flake checks, built on remote builder `prometheus` from
the committed `main` tree `d69f4970`):

- `nix flake show` — evaluates cleanly; `apps.*.recall`,
  `checks.*.test-history`, `checks.*.test-recall` present; derivations show
  `0.6.0`.
- `nix build .#checks.x86_64-linux.fmt` — PASS
  (`/nix/store/7mjbfydmfhwcrpq0hsd1r7sfap98d13d-listener-fmt-0.6.0`).
- `nix build .#checks.x86_64-linux.{test-history,test-recall,clippy}` — PASS
  (built on remote builder `prometheus`; produced `listener-test-0.6.0` for
  test-history and test-recall, and `listener-clippy-0.6.0`).

## Commit / Push

- jj commit `d69f4970` on `main`:
  "listener: persist transcript history and add clipboard recall (Claude Opus 4.8)".
- Pushed: `origin/main` = `d69f49704903...` (confirmed via `git ls-remote`).
- Orchestrate claim held on `(editor [(Path /git/github.com/LiGoldragon/listener)])`.
- Working copy was clean on entry; no peer edits were present or disturbed.

## For The Keybind Worker

(a) Recall command to bind on `Mod+Alt+M`:

```
listener-recall
```

No arguments or flags required for the default flow. It reads
`$XDG_DATA_HOME/listener/history.jsonl` and copies the pick with `wl-copy`.
The picker binary must be on PATH (default `fuzzel`; override with
`LISTENER_RECALL_SELECTOR`), and `wl-clipboard` must be on PATH (override with
`LISTENER_CLIPBOARD_PROGRAM`) — mirror how the whisrs package wraps
`whisrs-recall` with `fuzzel` + `wl-clipboard`. The binary ships from the
listener package as `${listener}/bin/listener-recall`. Optional history-path
override: `LISTENER_HISTORY_STORE=<path>`.

(b) Toggle and cancel commands — UNCHANGED from the Scout map:

- toggle/record: `listener-toggle-capture toggle`
- cancel: `listener-cancel-capture cancel`

Phase 2 touched no CLI wrapper, no toggle/cancel path, and no `signal-listener`
contract, so those wrappers keep working as-is. Per the plan, the keybind lane
moves toggle to `Mod+M`, cancel to `Mod+Ctrl+M`, and binds recall on the freed
`Mod+Alt+M` to `listener-recall`.

(c) New Listener version: `0.6.0`.
