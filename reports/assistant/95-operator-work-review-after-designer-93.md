# 95 · Operator work review after designer/93

Status: assistant review of the operator-shaped work adjacent to
`reports/designer/93-persona-orchestrate-rust-rewrite-and-activity-log.md`.

Author: Codex (assistant)

Date: 2026-05-09

---

## Findings

### P2 · Closed-enum versioning is described backwards in `signal-persona-system`

`/git/github.com/LiGoldragon/signal-persona-system/src/lib.rs:28`
documents `SystemTarget` as if future backend variants can be added
"without breaking existing consumers" because closed-enum decoding rejects
unknown variants.

That is the wrong lesson for this workspace's contract discipline. A closed
enum rejecting unknown variants means the addition is a coordinated schema
change, not a non-breaking extension. The same repo's `ARCHITECTURE.md`
versioning section says schema-level changes are breaking. The source comment
should match the architecture: future backend variants require coordinated
`persona-system` + `persona-router` upgrade.

### P3 · `signal-persona-system` overstates its test count

`/git/github.com/LiGoldragon/signal-persona-system/ARCHITECTURE.md:91`
says there are 15 round-trip tests. The repo currently has 14 `#[test]`
functions in `tests/round_trip.rs`. The arithmetic in the sentence also does
not resolve cleanly: 6 request variants + 5 event variants + 3 state-enum
coverage + 2 From-impl witnesses is not 15.

The tests are present and useful; this is documentation drift. It matters
because these are architectural-truth tests, and the doc should not make the
reader second-guess the witness surface.

### P3 · README files still carry retired store-actor language

The architecture files were cleaned up toward the correct shape: state-bearing
components own their own Sema database through `persona-sema`; there is no
shared store actor boundary. Three READMEs still say the old thing:

| File | Drift |
|---|---|
| `/git/github.com/LiGoldragon/persona-orchestrate/README.md:8` | says runtime Persona state belongs behind `persona-store`. |
| `/git/github.com/LiGoldragon/persona-message/README.md:76` | says durable commits flow through `persona-sema` and its store actor. |
| `/git/github.com/LiGoldragon/persona-sema/README.md:9` | says the runtime store actor is the separate concern. |

This does not break builds, but it weakens the `/92` and `primary-0q2` Sema
library framing. These should be rewritten to "component actor owns write
sequencing; persona-sema owns schema/table layout."

### Handoff Note · `persona-orchestrate` implementation has not landed

`/git/github.com/LiGoldragon/persona-orchestrate/ARCHITECTURE.md:28` now
describes the desired Rust component surface from designer/93: consuming
`signal-persona-orchestrate`, opening `orchestrate.redb`, exposing the
`orchestrate` binary, and owning `CLAIMS` / `ACTIVITIES` / `META`.

The source is still the older scaffold. `Cargo.toml:15` still names
`persona-orchestrate-daemon`, and there is no dependency yet on
`signal-persona-orchestrate`, `persona-sema`, `sema`, or NOTA parsing. This is
not an operator regression; it matches the still-open P1 handoff task
`primary-9iv`. It is the next implementation gap.

---

## Reviewed Work

I reviewed the designer/93 handoff plus the recent operator-shaped changes in
these repos:

| Repo | Commit / state | Review result |
|---|---|---|
| `signal-persona-system` | `238e9fd1` | New focus/input-buffer contract is structurally sound; findings above are documentation precision issues. |
| `signal-persona` | `f2916a82` | `PersonaRequest` / `PersonaReply` / `PersonaSignalError` prefix removal is coherent. No remaining current source/test/doc references found in that repo. |
| `signal-persona-message` | `f968b1eb` | `StoreRejected` became `PersistenceRejected`; this matches the no-shared-store-actor architecture. |
| `persona-message` | `0fb51a95` | Downstream `persona_system::Error` rename is consumed; flake lock points at the newer `persona-system`. README drift remains. |
| `persona-system` | `d469e2ee` plus prior error rename | Error export is now `Error`; architecture now says durable consumer history is not owned here. |
| `persona-router` | `53074412` | Architecture now says router-owned Sema database and commit-before-effect; no immediate code break found. |
| `persona-sema` | `9c2faf8a` | `PersonaSema::open` materializes the typed table set through `Table::ensure`; test covers fresh-open table materialization. |
| `signal-persona-orchestrate` | designer handoff | Contract crate builds and round-trips all request/reply variants. |
| `persona-orchestrate` | designer handoff | Architecture names the target runtime shape; implementation remains open under `primary-9iv`. |

---

## Verification

`nix flake check` passed in:

- `/git/github.com/LiGoldragon/signal-persona-system`
- `/git/github.com/LiGoldragon/signal-persona`
- `/git/github.com/LiGoldragon/persona-sema`
- `/git/github.com/LiGoldragon/signal-persona-orchestrate`
- `/git/github.com/LiGoldragon/persona-message`
- `/git/github.com/LiGoldragon/persona-router`

`rg '^#\[test\]' tests/round_trip.rs | wc -l` in
`signal-persona-system` returns `14`, confirming the test-count doc drift.

---

## Current Read

The operator work is directionally aligned with the workspace discipline:
contract records are typed, Sema is being used as a library rather than a
shared actor, the signal-persona prefix sweep improves naming, and
`persona-sema` now uses the Sema table-materialization API.

The next real code move is still `primary-9iv`: implement
`persona-orchestrate` against `signal-persona-orchestrate`, with
`persona-sema`/Sema-backed `CLAIMS`, `ACTIVITIES`, and `META` tables plus the
lock-file projection compatibility layer.
