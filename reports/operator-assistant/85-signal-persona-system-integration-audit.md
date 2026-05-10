# 85 - signal-persona-system integration audit

Status: assistant audit of the operator's recent `signal-persona-system`
integration slice across `persona-system`, `persona-message`, and
`persona-router`.

Author: Codex as `assistant`

Date: 2026-05-09

---

## 0 - TL;DR

The dependency and check shape is green: all three repos use portable git
dependencies for the audited cross-repo crates, `nix flake check` passes, and
`nix build .#checks.x86_64-linux.default --print-build-logs` succeeds for
`persona-system`, `persona-message`, and `persona-router`.

The integration is still not end-to-end. `persona-router/src/delivery.rs` now
uses `signal_persona_system::{FocusObservation, InputBufferObservation,
InputBufferState}`, but that `DeliveryGate` is only exported and tested.
`persona-router/src/router.rs` does not feed live router state through it; the
daemon still reads one NOTA line, decodes `RouterInput::from_nota`, and imports
`persona_system::{FocusObservation, SystemTarget}` for focus input.

The next architectural-truth witness should be a router test and daemon path
that decode a `signal-persona-system` `Frame`, accept `SystemEvent` focus and
input-buffer observations into `RouterActor`, and make `retry_pending` use the
same `DeliveryGate` that the new tests exercise.

---

## 1 - Scope

Audited repos:

| Repo | Commit inspected | Scope |
|---|---|---|
| `/git/github.com/LiGoldragon/persona-system` | `acbb2f38` | formatter/dependency baseline and system observation docs |
| `/git/github.com/LiGoldragon/persona-message` | `b405804d` | portable dependency move and text-boundary docs |
| `/git/github.com/LiGoldragon/persona-router` | `79b3d8f8` | `signal-persona-system` consumption in delivery gate |

Reference reports:

- `reports/designer/81-three-agent-orchestration-with-assistant-role.md` -
  assigns assistant's first lane to auditing this integration.
- `reports/operator-assistant/82-three-agent-orchestration-feedback.md` - says the audit
  should verify flake status, portable dependencies, architecture/skill drift,
  string dispatch, free functions, public newtype fields, `Persona*` prefixes,
  and the next architectural-truth witness.

---

## 2 - Verification

| Repo | Command | Result |
|---|---|---|
| `persona-system` | `nix flake check` | Passed; app meta warning only |
| `persona-message` | `nix flake check` | Passed; app meta warnings only |
| `persona-router` | `nix flake check` | Passed; app meta warning only |
| `persona-system` | `nix build .#checks.x86_64-linux.default --print-build-logs` | Passed |
| `persona-message` | `nix build .#checks.x86_64-linux.default --print-build-logs` | Passed |
| `persona-router` | `nix build .#checks.x86_64-linux.default --print-build-logs` | Passed |

The `nix flake check` output evaluated the derivations and reported
`running 0 flake checks`; the explicit `nix build` commands above are the
stronger test-build witness.

---

## 3 - Findings

### 3.1 - Router has a typed reducer, not live signal consumption yet

Good part: `persona-router/src/delivery.rs:1-2` imports the
`signal-persona-system` observation types, and
`persona-router/src/delivery.rs:31-101` makes `DeliveryGate` decide from
`FocusObservation` plus `InputBufferObservation`. The tests in
`persona-router/tests/smoke.rs:5-93` cover focused, occupied, unknown, target
mismatch, and ready states.

Gap: `DeliveryGate` is not used by `RouterActor`. A repo-wide search finds it
only in `src/delivery.rs`, `src/lib.rs`, and tests. Meanwhile
`persona-router/src/router.rs:9-12` imports `nota_codec` and
`persona_system::{FocusObservation, SystemTarget}`; the daemon reads one text
line and calls `RouterInput::from_nota` in `persona-router/src/router.rs:49-53`;
`RouterInput` still stores `FocusObservation(FocusObservation)` at
`persona-router/src/router.rs:301-325`.

Impact: the live router path still bypasses `signal_core::Frame`,
`signal-persona-system`'s protocol-version guard, and the channel's closed
`SystemEvent` enum. `InputBufferObservation` has no route into `RouterActor`
state yet. This is the live router instance of `primary-3fa` ("Converge
FocusObservation + InputBufferObservation contracts").

### 3.2 - The message contract is documented as consumed, but is not wired

`persona-router/ARCHITECTURE.md:17-25` shows `signal-persona-message` feeding
`RouterActor`, and `persona-router/skills.md:8-11` says the router should depend
on `signal-persona-message` and `signal-persona-system` for shared frame
records. `persona-router/Cargo.toml:23-29` depends on
`signal-persona-system`, but not `signal-persona-message`.

The current router daemon still uses `persona_message::schema::{Actor,
ActorId, Message, expect_end}` in `persona-router/src/router.rs:9-10` and NOTA
record-head dispatch in `persona-router/src/router.rs:319-331`.

Impact: this is probably the next `persona-router` refactor slice, not a
regression in the system integration commit. It does mean the docs describe the
target architecture more strongly than the shipped router path.

### 3.3 - Split-channel doc drift remains in persona-system and persona-message

`persona-system/ARCHITECTURE.md:52-58` still says shared frame definitions live
in `signal-persona`, and `persona-system/ARCHITECTURE.md:79-83` links
`../signal-persona/ARCHITECTURE.md`. The shipped contract for this channel is
`signal-persona-system`.

`persona-message/ARCHITECTURE.md:14-16`, `persona-message/ARCHITECTURE.md:45-52`,
`persona-message/skills.md:8-9`, and `persona-message/skills.md:36-38` still
name `signal-persona` as the binary contract. The shipped message channel is
`signal-persona-message`; `signal-persona` is now at most an umbrella/lift-out
place, not the concrete CLI-to-router frame repo.

Impact: small but real drift. This is safe to fix mechanically once the
operator confirms whether all umbrella references should be rewritten or only
the channel-specific references.

### 3.4 - Style-smell inventory

No sibling `path = "../..."` dependencies remain in the audited `Cargo.toml`
files; cross-repo dependencies are git dependencies.

No public tuple-field newtypes were found in `src/` or `tests/` for the three
audited repos.

Existing cleanup remains:

| Item | Current evidence | Tracking |
|---|---|---|
| `endpoint.kind` string dispatch | `persona-message/src/delivery.rs:74-79`, `persona-router/src/router.rs:227-263`, `persona-message/src/schema.rs:180-198` | `primary-0cd` |
| `Persona*` crate-name type prefixes | `persona-system/src/error.rs:4`, `persona-system/src/event.rs:56`, `persona-router/src/error.rs:6`, `persona-router/src/message.rs:36` | `primary-tlu` |
| free function drift | `persona-message/src/schema.rs:231` exports `expect_end` | `primary-0ty` |

These are real issues, but they are not blockers for the next signal-system
witness unless the same files are already being touched.

---

## 4 - Next witness

Operator should keep the next router slice small and falsifiable:

1. Add a router boundary that decodes `signal_persona_system::Frame` bytes and
   extracts `SystemEvent::FocusObservation` and
   `SystemEvent::InputBufferObservation`.
2. Store the latest focus and input-buffer observations per target in
   `RouterActor`.
3. Make `retry_pending` call `DeliveryGate::from_observations(...)` instead of
   the current `HarnessActor::blocks_delivery` focus/prompt shortcut.
4. Add a test that constructs `signal-persona-system` frames, applies them to a
   pending router delivery, and proves the pending count changes only when both
   focus and input-buffer facts permit delivery.

That witness would turn the current reducer-level integration into actual
runtime channel consumption.
