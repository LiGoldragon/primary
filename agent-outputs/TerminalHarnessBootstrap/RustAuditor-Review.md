# Rust Auditor Review

Task: audit the terminal archival guidance and first harness bootstrap slice. Scope was the changed documentation in primary, `terminal`, and `terminal-cell`, plus `harness/src/daemon.rs`, `harness/tests/daemon.rs`, and `harness/flake.nix`. I did not edit source files, commit, or push.

## Findings

### High: daemon watch opens an actor subscription but does not preserve the provider-neutral stream

Path: `/git/github.com/LiGoldragon/harness/src/daemon.rs:105`, `/git/github.com/LiGoldragon/harness/src/daemon.rs:112`, `/git/github.com/LiGoldragon/harness/src/daemon.rs:620`, `/git/github.com/LiGoldragon/harness/src/daemon.rs:628`, `/git/github.com/LiGoldragon/harness/tests/daemon.rs:589`

Risk: `HarnessEngine::handle_working_connection` reads exactly one request, writes exactly one `HarnessEvent`, and returns. `watch_transcript_event` opens `TranscriptSubscriptionManager` with `TranscriptSubscriptionSink::new()` and then returns only `opened.snapshot.into()`. The sink is not attached to the accepted Unix stream or any socket-writer actor, and it is dropped from the daemon-side handler after the manager stores it inside the internal reply handler. That means the public daemon boundary can return the opening snapshot, but it has no wire path for later `TranscriptObservation` pushes on the subscribed connection.

This violates the stream contract described by `signal-harness`: `WatchHarnessTranscript` opens `HarnessTranscriptStream`, and subsequent `TranscriptObservation` events arrive on the same connection (`/git/github.com/LiGoldragon/signal-harness/src/lib.rs:551` through `554`; stream declaration at `606` through `636`). It also contradicts the local harness architecture, which says the per-subscription handler holds the connection and writes events onto the wire (`/git/github.com/LiGoldragon/harness/ARCHITECTURE.md:136` through `138`) and that the daemon pushes typed deltas after the snapshot (`/git/github.com/LiGoldragon/harness/ARCHITECTURE.md:243` through `246`).

Expected correction: make the daemon watch path create or hand off a real stream writer tied to the accepted connection, keep that connection alive for the stream lifecycle, and route handler sink events onto the `signal-harness` stream frame until `UnwatchHarnessTranscript` closes it. Add a daemon-level witness that publishes a transcript observation after watch and reads a `TranscriptObservation` from the subscribed wire stream. The current tests only assert the snapshot reply and a separately requested unwatch ack, so they cannot catch this bypass (`/git/github.com/LiGoldragon/harness/tests/daemon.rs:608` through `616`, `638` through `656`).

### Medium: unwatch acknowledgement is returned on a new request path, not proven as the final stream event

Path: `/git/github.com/LiGoldragon/harness/src/daemon.rs:635`, `/git/github.com/LiGoldragon/harness/src/daemon.rs:647`, `/git/github.com/LiGoldragon/harness/tests/daemon.rs:630`, `/git/github.com/LiGoldragon/harness/tests/daemon.rs:646`

Risk: the test opens a watch connection, reads the snapshot, then opens a separate Unix connection and sends `UnwatchHarnessTranscript`. The daemon returns `HarnessSubscriptionRetracted` on that second request connection. This proves the close request can find a matching manager entry, but it does not prove the final ack is delivered before the subscribed stream ends, which is the lifecycle described in `signal-harness` architecture (`/git/github.com/LiGoldragon/signal-harness/ARCHITECTURE.md:69` through `74`, `103` through `108`).

Expected correction: after the stream writer exists, test the same stream observes its final `HarnessSubscriptionRetracted` event before shutdown. If the intended protocol is request-reply ack on the unwatch connection rather than final event on the original stream, update the contract docs and stream abstraction together; currently they say stream final ack.

### Low: terminal README still uses current-runtime wording inside an archived repo

Path: `/git/github.com/LiGoldragon/terminal/README.md:41`, `/git/github.com/LiGoldragon/terminal/README.md:43`

Risk: the top of the README correctly says `terminal` is archived/inactive and that details below are the prior owner design (`README.md:5` through `8`), but the "Named sessions" section says `terminal-supervisor` is the "current engine-facing component socket during the consolidation." That is stale enough to conflict with the archival guidance for a reader scanning commands rather than the preamble.

Expected correction: change the section wording to "At archival time..." or "Historically..." and make any runnable witnesses explicitly historical/reference unless they are still meant to be run for archaeology.

## No Findings

I did not find a blocking contradiction in the primary active repository registry: `/home/li/primary/protocols/active-repositories.md:30` names prompt checking as `terminal-cell` owned for the V1 harness wave, `:32` marks `terminal-cell` active, and `:82` through `:89` moves `terminal` to inactive/archived.

I did not find horizontal-rule markdown violations in the audited docs. `rg -n '^---\s*$'` over the named markdown files returned no matches.

The `terminal-cell` guidance consistently says it is the active primitive for V1 harness work while `terminal` is archived (`/git/github.com/LiGoldragon/terminal-cell/ARCHITECTURE.md:52` through `55`, `78` through `84`, `96` through `98`, `172` through `177`, `404` through `418`).

## Verification

Commands consulted:

- `orchestrate "(Observe Roles)"`: no claim on `terminal`, `terminal-cell`, `harness`, or `primary`; unrelated claims existed elsewhere.
- `jj status --no-pager` in `/home/li/primary`, `/git/github.com/LiGoldragon/terminal`, `/git/github.com/LiGoldragon/terminal-cell`, and `/git/github.com/LiGoldragon/harness`: only the expected scoped files were dirty in the three target repos; primary also had unrelated report files plus `protocols/active-repositories.md`.
- `jj diff --no-pager -- ...` for the audited files: reviewed changed surfaces.
- `rg` and `nl -ba` over the changed docs and relevant `harness`/`signal-harness` sources: gathered line anchors above.
- `system=$(nix eval --raw --impure --expr builtins.currentSystem); nix build ".#checks.${system}.harness-daemon-watch-transcript-returns-typed-snapshot" --no-link --print-out-paths`: passed. Raw output path omitted per Nix reporting hygiene.
- `system=$(nix eval --raw --impure --expr builtins.currentSystem); nix build ".#checks.${system}.harness-daemon-unwatch-transcript-returns-final-retraction-ack" --no-link --print-out-paths`: passed. Raw output path omitted.
- `cargo test --test daemon harness_daemon_watch_transcript_returns_typed_snapshot -- --nocapture`: passed, 1 test.
- `cargo test --test daemon harness_daemon_unwatch_transcript_returns_final_retraction_ack -- --nocapture`: passed, 1 test.
- `cargo test --test subscription_truth -- --nocapture`: passed, 7 tests. This proves the in-process actor producer plane, not the daemon wire stream.
- `cargo test --test message_router_harness_e2e -- --nocapture`: failed as reported. The router daemon printed `daemon signal frame error: rkyv archive deserialization failed`; the test then panicked at `tests/message_router_harness_e2e.rs:67` because it expected `SubmissionAccepted` and got `Error("router socket unreachable; message not forwarded")`.

Two initial check attempts were invalid command shapes in this Nix/Cargo environment:

- `nix flake check .#harness-daemon-watch-transcript-returns-typed-snapshot` and the matching unwatch attribute failed because this Nix command does not accept that fragment form.
- One `cargo test --test daemon` invocation with two test filters failed because Cargo accepts one filter argument.

## Residual Risks

The subscription token shape is coarse. `signal-harness` currently defines `HarnessTranscriptToken` as only `{ harness: HarnessName }` and documents "one observer per harness" (`/git/github.com/LiGoldragon/signal-harness/src/lib.rs:540` through `548`), while other docs call it a per-stream token. The manager allows multiple open entries with the same token and closes the first match (`/git/github.com/LiGoldragon/harness/src/subscription.rs:489` through `507`, `534` through `542`). If multiple router or observer consumers are expected, the contract needs a distinct stream identity or the manager must enforce one open observer per harness.

The narrow new daemon tests pass but are weaker than the architecture truth tests named in `harness/ARCHITECTURE.md:302` through `304`; those stronger daemon-level stream checks are not present in the changed flake slice.
