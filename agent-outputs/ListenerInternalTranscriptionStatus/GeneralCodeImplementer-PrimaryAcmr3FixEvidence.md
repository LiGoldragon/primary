# General Code Implementer Evidence: primary-acmr.3 Fix

## Task And Scope

Fixed the `primary-acmr.3` Rust audit finding in
`/git/github.com/LiGoldragon/listener`: actor timeout or disconnect errors
returned as `Error::TranscriptionActorUnavailable` now map to the public typed
reply reason `TranscriptionBackendUnavailable` instead of the generic
`NotBuiltYet`.

Scope stayed narrow to Listener runtime error mapping and focused test coverage.
No status-bar/UI work, CriomOS-home work, real microphone smoke test, live
OpenAI request, transcript contents, or secrets were touched.

## Context Consulted

- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/RustAuditor-Review.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/GeneralCodeImplementer-Evidence.md`
- `bd show primary-acmr.3`
- `/git/github.com/LiGoldragon/listener/AGENTS.md`
- `/git/github.com/LiGoldragon/lore/AGENTS.md`
- `/git/github.com/LiGoldragon/listener/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/listener/README.md`
- `/git/github.com/LiGoldragon/listener/skills.md`
- Listener runtime and transcription sources.
- `signal-listener` generated schema accessors for `Reason`,
  `UnimplementedOperationKind`, and `UnimplementedReason`.

## Changed Files

Repository: `/git/github.com/LiGoldragon/listener`

- `src/runtime.rs`
- `tests/runtime.rs`

Pushed commit:

- `4080f8e8`: `listener: classify actor transcription failures`

## Implementation

Observed fact: `OpenAiBatchTranscriptionActor::transcribe` already returns
`Error::TranscriptionActorUnavailable` when actor send fails, reply wait times
out, or the reply channel disconnects.

Changed behavior: `Error::unimplemented_reason` now classifies both
`TranscriptionBackendUnavailable` and `TranscriptionActorUnavailable` as
`UnimplementedReason::TranscriptionBackendUnavailable`.

Test coverage added: a runtime integration test starts capture, stops with a
transcriber stub that returns `TranscriptionActorUnavailable`, and asserts the
public `Stop` reply is `RequestUnimplemented` with:

- `OperationKind::Stop`
- `UnimplementedReason::TranscriptionBackendUnavailable`

The test also asserts the UI-safe status recorder receives an `error` event.

## Checks Run

All checks passed:

- `cargo fmt --check`
- `cargo test --test runtime stop_actor_unavailable_returns_transcription_backend_unavailable_reply`
- `cargo test --test runtime`
- `cargo clippy --all-targets --all-features -- -D warnings`
- `nix build .#checks.x86_64-linux.test .#checks.x86_64-linux.clippy .#checks.x86_64-linux.fmt --no-link --print-out-paths`

## Tracker State

Added a comment to `primary-acmr.3` naming commit `4080f8e8`, the fixed
finding, checks run, and the need for re-audit.

`primary-acmr.3` remains open because the item is an audit closure task. It
should be re-audited against Listener commit `4080f8e8`.

## Blockers And Follow-Up

No implementation blocker remains for the cited actor unavailable reply mapping
finding.

Follow-up requirement: re-audit `primary-acmr.3` against Listener commit
`4080f8e8` and close the bead only if the audit acceptance criteria pass.
