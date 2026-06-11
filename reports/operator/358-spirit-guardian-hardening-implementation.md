# Spirit Guardian Hardening Implementation

Operator worktree:
`/home/li/wt/github.com/LiGoldragon/spirit/operator-guardian-hardening`

Feature bookmark:
`operator/guardian-hardening`

## What Landed

- Guardian prompts are operation-aware for `Record`, `Propose`, `Clarify`,
  `Supersede`, and `Retire`.
- `Record` is schema-visible as the Nexus effect command `GuardRecord` when
  the `agent-guardian` feature is compiled, so model-gated record admission is
  not hidden in hand-written dispatch.
- The model remains the semantic judge. Deterministic duplicate handling is
  only a mechanical consequence when the model returns `Reject Duplicate`:
  Spirit bumps the existing record's importance and returns the duplicate
  rejection.
- Guardian calls use temperature `0`, a closed reason set in the system prompt,
  exact `GuardianVerdict` grammar examples, and one typed retry when the agent
  returns malformed NOTA for the verdict type.
- Guardian retrieval now unions domain overlap, referent overlap, keyword
  overlap, and full-text overlap, ranks by relevance/certainty/importance, and
  caps the bundle at 64 records. Clarify, supersede, and retire always pin
  their target records into the bundle.
- Guardian decisions are written by Spirit to a separate sidecar database
  derived from the live database path as `<stem>.guardian.sema`. The live intent
  SEMA store and marker stay separate.
- Nexus runs effect work through `block_in_place` on multi-thread Tokio
  runtimes, so blocking Guardian socket/model calls do not occupy an async
  worker for the whole model round-trip.

## Scope Notes

Default and trace builds still route `Record` and classified `State` through the
old SEMA write path when `agent-guardian` is not compiled. That preserves the
existing Signal/Nexus/SEMA trace witnesses and the binary-only daemon surface.

Deployment wiring to DeepSeek / CriOMOS was not touched here because the
canonical deployment checkouts are held by `system-operator`. This branch is
ready for integration into that deployment lane once the lock clears.

## Verification

All commands passed in the Spirit worktree:

- `cargo test`
- `cargo test --features agent-guardian,nota-text`
- `cargo test --features testing-trace --test instrumentation_logging`
- `nix flake check --max-jobs 0`

The first Nix run caught the trace regression from routing non-Guardian
`Record` through `GuardRecord`; the final Nix run passed after restoring the
non-Guardian SEMA path.
