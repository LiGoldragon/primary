# Listener Transcript History + Recall — Rust Audit Review

## Verdict

**CLEAN — issues-found: none blocking.** The change is correct, matches its
evidence, and satisfies every critical invariant the brief named. Findings are
limited to four low-severity / provisional observations and one out-of-scope
integration note. Nothing here should hold the release.

## Scope And What I Consulted

Independent audit of `listener` commit `d69f4970` (`0.5.1 -> 0.6.0`), verified
against source, not taken from the evidence file.

- Commit identity: `git rev-parse HEAD` = `origin/main` = `git ls-remote origin main`
  = `d69f4970490312aa20a886bd5efe53202d60a5bc`. jj `main` bookmark on the same
  commit. Pushed state matches the evidence.
- Read in full: `src/history.rs`, `src/recall.rs`, `src/bin/listener_recall.rs`,
  `src/delivery.rs` (the reused `ClipboardCommand` seam), the `src/runtime.rs`
  stop/cancel paths and `record_transcript_history`, `src/error.rs`, `src/lib.rs`
  re-exports, `tests/history.rs`, `tests/recall.rs`, the `tests/runtime.rs` diff,
  `Cargo.toml`/`Cargo.lock`, `flake.nix`, `README.md`, `ARCHITECTURE.md`,
  `skills.md`.
- Cross-repo: confirmed the consumed `signal_listener` API (`CaptureSession::value`,
  `TranscriptText::as_str`, `TranscriptText::new`, `CaptureSession::new(Integer=u64)`)
  in `signal-listener/src/lib.rs` and `src/schema/lib.rs`, and that
  `signal-listener` is at `0.4.0` and is not touched by this commit.

## Checks I Ran (exact results)

All from `/git/github.com/LiGoldragon/listener`, offline:

- `cargo test --test history --test recall --test runtime` — **PASS**:
  history 5/5, recall 3/3, runtime 17/17 (25 total).
- `cargo clippy --all-targets --all-features -- -D warnings` — **PASS**, no warnings.
- `cargo fmt --check` — **PASS**.
- `git grep 0.5.1` — only the third-party `nota` crate; `listener` is `0.6.0` in
  both `Cargo.toml` and `Cargo.lock`. No stale version strings.
- Network-reference grep over `history.rs`/`recall.rs`/`listener_recall.rs` — **none**.

Could **not** independently reproduce: the Nix flake checks on remote builder
`prometheus` (`test-history`, `test-recall`, `clippy`, `fmt`). I verified the
`flake.nix` wiring instead (below) and ran the equivalent cargo checks locally as
a substitute. See "Not Independently Verified".

## Critical Invariants (brief's must-verify list) — all hold

1. **Cancel writes NO history entry — verified on the real path, not just an
   assertion.** `runtime.rs::cancel()` (lines 158-174) never calls
   `record_transcript_history`; only `stop()` does, at line 144. The runtime test
   `cancel_stops_capture_retains_artifact_and_skips_transcription_and_delivery`
   drives the production `cancel()` through `handle_input` and asserts both
   `recorded_history().is_empty()` and `!history_path().exists()` against the
   injected temp store. That is a genuine runtime witness of the real cancel path,
   and it passed here.

2. **History-write failure never aborts the stop or drops the transcript —
   structurally guaranteed.** `record_transcript_history` discards the append
   result (`let _ = self.history_store.append(&entry);`) and wraps the fallible
   timestamp/entry build in `if let Ok(entry)`, so no history error can reach
   `stop()`'s control flow — a compile-enforced guarantee stronger than a test.
   The call sits at line 144, *before* the unconditional
   `output_target_dispatcher.deliver(...)` at 145-147, so delivery and the
   `Output::Stopped` reply are unaffected regardless of history outcome.
   Placement-before-delivery also means recall captures the transcript even when
   clipboard delivery fails — the stated design intent, confirmed in source.

3. **Privacy: local-only, `0700` dir / `0600` file — verified.**
   `append` creates the parent via `DirBuilder::mode(0o700)` and opens the file
   with `OpenOptions::mode(0o600)`, then force-sets `Permissions::from_mode(0o600)`
   on every append (tightens a pre-existing looser *file*). `mode 0700/0600` are
   umask-immune here (no group/other bits to mask). `history_store_uses_owner_only_permissions`
   asserts exactly `0o600`/`0o700` and passed. No network/socket/http anywhere in
   the history or recall modules; recall copies via the same local `ClipboardCommand`
   subprocess (`wl-copy`). Transcript text is never transmitted externally.

4. **Tests are meaningful and exercise real behavior — verified by running them.**
   History round-trip is real (append -> read newest-first, limit truncation,
   multiline/tab round-trip through `serde_json`, owner-only perms, empty-store
   read). Recall read->select->copy is end-to-end through real subprocess stubs
   (`/bin/sh` selector + clipboard scripts) using the production `RecallSelector`
   spawn/pipe path and the production `ClipboardCommand::deliver`; it asserts the
   FULL text is copied (index 1 -> older transcript), and that empty history and a
   cancelling selector both leave the clipboard file uncreated. Not green-rubber-stamped:
   I re-ran all 25 and inspected what each asserts.

5. **Versioning truthful; `signal-listener` correctly unchanged.** Minor bump
   `0.5.1 -> 0.6.0` is right for an additive user-facing feature (new
   `listener-recall` bin + new stop-time behavior). `Cargo.toml` and `Cargo.lock`
   both updated; no other version surface exists in the crate. `signal-listener`
   stays `0.4.0` and is not in this commit — correct, because recall reads the
   existing `Output::Stopped.transcript_text` and the local file, adding no wire
   operation or reply.

## Rust Discipline Assessment — conforms

- **Methods on data-bearing types:** every behavior is a method on a non-ZST type
  (`HistoryLimit`, `HistoryTimestamp`, `TranscriptHistoryEntry`,
  `TranscriptHistoryStore`, `TranscriptRecall`, `RecallSelector`, `RecallSelection`,
  `RecallOutcome`). Free functions are limited to `main` and test helpers — allowed.
- **Typed domain values:** `HistoryLimit(usize)` and `HistoryTimestamp(i64)` wrap
  primitives; the bare `i64/u64/String` live only in the private serde DTO
  `TranscriptHistoryLine`, which is the correct place for the JSON boundary.
- **Typed errors at the boundary:** new `HistoryEntryEncode`, `HistoryEntryDecode`,
  `RecallSelectorUnavailable` via `thiserror`; `io::Error` via `#[from]`; no
  `anyhow`/`eyre` at the edge. Crate boundary returns the crate `Result`.
- **Typed-records-over-flags:** `RecallOutcome` (EmptyHistory / NoSelection /
  Copied) is a closed enum, not bool soup — a textbook application of the rule.
- **Real parser, no hand-rolled parsing:** JSONL uses `serde_json`; the only
  hand-parse is a single-integer selector index (`token.parse::<usize>()`) —
  trivial and local, which the discipline permits.
- **Reuse of the production clipboard seam:** recall calls
  `ClipboardCommand::deliver` returning `DeliveryOutcome`, i.e. the exact path
  production delivery uses — no duplicate clipboard implementation.
- **Naming:** full English words throughout (`unix_milliseconds`, `recorded_at`,
  `MAXIMUM_PREVIEW_CHARACTERS`); no crate-name prefixing.
- **Defensive row format:** `preview()` flattens via `split_whitespace().join(" ")`,
  stripping tabs/newlines, so the `{index}\t{preview}` fuzzel row is guaranteed to
  carry exactly one tab and multiline transcripts cannot corrupt column parsing —
  and this is the behavior the multiline test pins.
- **flake.nix wiring:** `test-history`/`test-recall` use `craneLib.cargoTest` with
  `cargoTestExtraArgs = "--test history"` / `"--test recall"`, mirroring the
  existing `test-configuration` check; the `recall` app points at
  `${package}/bin/listener-recall`. Correct and consistent with repo convention.

## Findings By Severity

### Blocking

None.

### Low / Provisional

- **L1 (provisional, architecture) — storage format deviates from the workspace
  default.** `rust-storage-and-wire` says persistent state "normally" uses redb
  with a NOTA human projection; this uses append-only JSONL with a JSON projection.
  It is a defensible, precedent-backed choice: it mirrors the sibling `whisrs`
  history store, the append-only immutable-event shape fits a flat log better than
  transactional redb, the line-oriented format is what the fuzzel dmenu contract
  consumes, and this component already stores its capture log as a bespoke binary
  format rather than redb. Recommend the architecture owner confirm the JSONL/JSON
  deviation is acceptable for this component; not a defect.
  (`src/history.rs`)

- **L2 (privacy edge) — directory tightening only on creation.** `append` force-sets
  the *file* to `0600` on every write, but `prepare_directory` returns early when
  the parent already exists, so a pre-existing looser `listener` data directory is
  not re-tightened to `0700`. Low risk: Listener creates the directory fresh with
  `0700`, and the transcript-bearing file is always `0600`. Consider tightening the
  directory on append too, or documenting the create-time assumption.
  (`src/history.rs`, `prepare_directory`)

- **L3 (test completeness, informational) — no failure-injection witness for the
  best-effort invariant.** There is no test that forces the history append to fail
  and asserts stop still returns Ok and still delivers. The invariant is
  structurally guaranteed (the append `Result` is discarded), which is stronger
  than a runtime test, so this is informational; an unwritable-path witness would
  satisfy the architectural-truth-test "the shortcut must fail" preference but adds
  little.
  (`src/runtime.rs::record_transcript_history`)

### Trivial

- History file grows unbounded (no rotation/pruning), and `read_recent` reads the
  whole file into memory each call. Matches the `whisrs` precedent; out of scope.
- The JSON key `unix_millis` abbreviates "milliseconds"; it is a deliberate wire
  key and the Rust domain field uses the full word `unix_milliseconds`. No action.

## Residual Risks / Out Of Scope

- **Store-path parity across processes (integration, for the keybind/packaging
  worker).** The daemon (writer) and `listener-recall` (reader) both derive the
  path via `TranscriptHistoryStore::from_environment()`
  (`LISTENER_HISTORY_STORE` -> `XDG_DATA_HOME/listener/history.jsonl` ->
  `HOME/.local/share/listener/history.jsonl`). Correct recall in production
  therefore depends on the `listener.service` systemd user unit and the interactive
  recall process resolving `XDG_DATA_HOME`/`HOME` identically — the same coupling
  `whisrs` relies on (its Nix service even pre-creates the file). Packaging should
  ensure that env parity; it is not a Rust defect in this change.

## Not Independently Verified

- The Nix flake checks (`test-history`, `test-recall`, `clippy`, `fmt`) as built on
  remote builder `prometheus`. Prerequisite missing: the remote builder. I verified
  the `flake.nix` derivations are correctly wired to the `history`/`recall` test
  files and ran the equivalent `cargo test`/`clippy`/`fmt` locally (all green) as a
  substitute. The recall tests spawn `#!/bin/sh` stubs; the Nix build sandbox
  provides `/bin/sh`, and the evidence reports these checks passed on `prometheus`,
  consistent with the local cargo runs.
