# 18 - Deferred Persona decisions response

*Designer-assistant report. Date: 2026-05-11. Scope: response to
the user's exchange with designer about the seven deferred decisions
from `reports/designer/125-channel-choreography-and-trust-model.md`
§6. This report does not edit designer-owned reports; it records the
designer-assistant read while designer is revising them.*

---

## 0 - Short Read

The exchange changes the center of gravity for the seven deferred
decisions.

The major correction is D1: delivery safety does not need focus as a
first-order gate. The terminal input gate is the safety primitive. If
the gate can lock human input, buffer human bytes while locked, inspect
prompt cleanliness after the lock, inject only when clean, then replay
buffered human bytes on unlock, the focus signal becomes advisory UX
state rather than the thing that prevents byte interleaving.

The second correction is D2/D3: the existing design language was too
hostile to plain text and too dogmatic about relation-only contract
repos. Plain text can be a perfectly good data-carrying body. Contract
repos are shared type crates; the discipline should be that they are
shared **boundary vocabularies**, not anonymous junk drawers.

## 1 - D1: Input Buffer / Prompt Cleanliness

Decision shape:

- `persona-terminal` owns the injection transaction.
- `terminal-cell` owns the low-level input gate mechanics: lock, buffer
  human bytes, inject programmatic bytes, unlock, replay buffered bytes.
- `persona-harness` may supply harness-specific semantic interpretation
  of the screen/prompt when needed.
- `persona-system` focus is deferred/advisory, not the first safety
  gate.

The safe primitive is not "focused window + clean prompt"; it is a
terminal-owned transaction:

1. Router asks the terminal/harness delivery path to deliver.
2. `persona-terminal` acquires an input-gate lease from the cell.
3. The cell begins caching human input bytes instead of passing them to
   the child.
4. `persona-terminal` checks prompt cleanliness after the lock is held.
5. If clean, it injects the programmatic bytes.
6. It releases the lock and the cell replays any cached human bytes.
7. If dirty or unknown, it releases the lock without injecting and
   reports a typed blockage/retry state.

Focus may return later for scheduling, UX, or "do not surprise the
human" policy, but it is not required to prevent interleaving. Plans
that make `persona-system` the producer of `InputBufferObservation`
should be revised. The terminal/harness layer is where prompt state
belongs.

One nuance: "prompt cleanliness" is not always visible from raw PTY
bytes. `terminal-cell` can gate and cache bytes, but semantic prompt
recognition may need the harness adapter. That argues for:

- `terminal-cell`: byte gate and transcript;
- `persona-terminal`: injection transaction and terminal observation;
- `persona-harness`: provider/harness-specific prompt semantics.

## 2 - D2: MessageBody And Typed Nexus

The old "MessageBody(String) is bad" framing is too absolute.

Plain text is not inherently untyped. A message body may legitimately
be textual for a long time. The real issue is whether the contract
names the text's role precisely enough and leaves room for more
specific bodies without pretending an unmodeled string is the final
semantic closure.

Recommended shape:

```text
MessageBody
  | PlainText(PlainTextBody)
```

where `PlainTextBody` is a domain newtype, not an arbitrary payload
field. Later variants can be added when they earn their place:
quoted reply, structured instruction, system notice, transcript
excerpt, handoff note, etc.

This means typed-Nexus work should not block router and harness durable
schemas for days. The durable schema can store `MessageBody::PlainText`
now, with the contract admitting that the body enum is expected to grow.
What should be avoided is hardening a naked `String` with no named
semantic role.

If designer still files a later Nexus-body report, it should be a
growth plan, not a claim that text bodies are invalid.

## 3 - D3: Contract Repos Are Shared Boundary Vocabularies

The skill phrase "A contract repo is not a shared-types bucket" is
overcorrected. A contract repo is absolutely a shared type crate: that
is why it exists. The failure mode is not sharing types; the failure
mode is collecting unrelated types without a named boundary, owner, or
semantic reason.

Recommended skill correction:

- A contract repo is a shared boundary vocabulary.
- It may be relation-shaped or component-shaped.
- If component-shaped, each relation inside it must be named in
  `ARCHITECTURE.md` and placed in an explicit module.
- Cross-component kernel vocabulary belongs in a small kernel contract
  crate, as with `signal-persona-auth`.
- A contract repo must not become an anonymous "whatever several repos
  need" drawer.

This supports designer's option B, but with better philosophical
wording: one crate per component with modules per relation is valid
when the relations co-evolve because the same component owns them.

## 4 - D4: Transcript Fanout And Inspection

Default should be typed observations plus sequence pointers. Raw
transcripts should stay in `terminal-cell` / `persona-terminal`
storage and should not be pushed broadly to router or mind.

The user's "office shoulder-checker" agent is a real future role, but
it should not imply raw transcript fanout by default. That role can get
an explicit transcript-inspection capability:

- request a transcript range or section from `persona-terminal`;
- receive raw bytes only for that authorized read;
- produce summaries, observations, or questions;
- store summaries/pointers in mind rather than duplicating raw bytes.

This is not naturally a router-delivered user message. It is closer to
inspection/read capability over terminal-owned transcript storage. If
the federation later routes all component calls through the router,
the router can carry a small authorization/control message, but it
should not carry the raw transcript stream as normal delivery payload.

## 5 - D5: ForceFocus

Focus can be put aside for the current injection path. Terminal input
gate safety removes focus as the near-term delivery blocker.

When the system privileged-action surface returns, `ForceFocus` should
not be the name. The honest names remain `FocusIntervention` or
`RequestFocus`, with typed replies such as `Applied`,
`DeniedByBackend`, `DeniedByPolicy`, `NoSuchWindow`, and
`Failed { reason }`.

## 6 - D6: HarnessKind::Other

`HarnessKind::Other { name: String }` should be removed. Enums at
contract boundaries are closed vocabularies. "Other" is an unmodeled
case with a string payload.

`Fixture` is acceptable only if it is a real named harness kind used by
tests/integration fixtures. Production harnesses should be explicit
variants: `Codex`, `Claude`, `Pi`, and future named variants through
schema evolution.

## 7 - D7: terminal-cell Integration

The user's instinct is right that `terminal-cell` may no longer need
to pretend to be a general-purpose independent tool. It is our
low-level terminal primitive.

The important split is data plane versus control plane:

- The byte path must stay minimal and fast. It is where previous
  relay designs failed by mangling human input.
- The control/observation plane can become more Persona-shaped:
  worker lifecycle push, input-gate leases, prompt-readiness
  observations, resize/session health.

There are two viable implementation shapes:

1. `terminal-cell` remains a separate daemon/repo, and
   `persona-terminal` speaks a typed cell protocol to it. Add the
   `WorkerObservation` push form now if `persona-terminal` needs
   session health. Do not poll.
2. `terminal-cell` becomes a library/subcomponent inside
   `persona-terminal`. Then `persona-terminal` is the Signal-facing
   component, while terminal-cell remains the low-level Rust module
   that owns PTY, gate, transcript, and worker threads.

Either way, do not force the raw PTY byte stream itself through a
heavy Signal contract unless a concrete witness says the byte path
still behaves like a real terminal. Signal is a good fit for the
control plane; the byte plane has stricter latency and transparency
requirements.

## 8 - Report Edits This Implies

Designer-owned reports likely need these edits:

- `designer/114`: stop saying `persona-system` owns
  `InputBufferObservation`; terminal/harness own prompt cleanliness.
- `designer/118`: router's delivery gate should consume terminal
  delivery readiness, not system-produced input-buffer facts as the
  first safety model.
- `designer/119`: put `InputBufferTracker` and focus-driven delivery
  behavior on hold; keep system focused on OS observations and later
  privileged actions.
- `designer/121`: add the terminal-owned injection transaction:
  acquire gate lease, cache human bytes, check cleanliness, inject or
  release, replay cached human bytes.
- `designer/123`: revise `WorkerObservation` push from optional to
  required if `persona-terminal` session health depends on it; also
  consider whether terminal-cell is a daemon, a library, or both.
- `designer/126`: update T6/T7 so transcript fanout is pointers plus
  observations; D1 uses terminal readiness; D2 is not a hard blocker
  on text bodies; D7 may expand T6 into terminal-cell integration.
- `skills/contract-repo.md`: replace the anti-shared-types wording
  with "shared boundary vocabulary" discipline.

## 9 - Operator Implications

Near-term implementation should avoid three traps:

1. Do not implement focus as a required injection safety gate before
   the terminal input-gate transaction exists.
2. Do not overbuild typed-Nexus before a concrete need; do make
   `MessageBody` a named domain type, ideally an enum with a
   `PlainText` variant rather than a naked `String`.
3. Do not route raw transcript bytes broadly. Build pointers,
   summaries, typed observations, and explicit raw-range requests.

The highest-value operator work after the designer edits is likely:

- terminal-cell input-gate lease witness with cached human-byte replay;
- persona-terminal delivery-readiness API over that lease;
- router test that no delivery occurs unless the terminal readiness
  transaction succeeds;
- terminal-cell worker lifecycle push if session health depends on it.
