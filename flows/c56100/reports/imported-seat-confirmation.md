# Imported-seat confirmation: bounded implementation plan

## Sources

- Live read-only stable ordinary Flow API, `flow 'List.{}'`, at
  `2026-09-27T07:10:54Z`: Mind Astra `6fe957` is durably `Active`, with native
  session `01a0dfdc-a500-7271-8f54-e446fe9578dd`, endpoint `Unavailable`, and
  route `default / mind-astra-6fe957 / w1:p2 / term_65c6a758e81952`; its origin
  is `56ae53 / default / meta-bind-existing`.
- Same-time read-only `herdr agent get w1:p2`: the live Codex agent has the
  same native session, pane and terminal and is interactive-ready.  It is
  `done`.
- `flows/56ae53/summary.md`: an earlier stable record described Astra's
  imported Flow row as `Pending/RegisteredUnconfirmed`.
- Flow immutable release `bc464e5e1b94fcc179af73111f43b69db1f69fc5` (0.17.4):
  `crates/flow-nexus/src/lib.rs`, `store.rs`, `delivery.rs`, `herdr.rs`,
  `README.md`, `DESIGN.md`, and `UPGRADES.md`.
- Psyche topic evidence: `flows/836818/vision/flowNexus.md` and
  `flows/d8df70/vision/flowTool.md` authorize binding existing live Herdr
  flows through the meta socket.  They do not settle the later confirmation
  criterion.

## Observations

The actual current durable row is Active.  The earlier Pending statement is
historical; it is not the current status of Astra `6fe957`.

`MetaBindExisting` in 0.17.4 accepts only a live, well-formed Flow container,
matching Herdr-server process identity, unique Flow IDs and pane identities,
matching live process identity and working directory.  It writes an imported
node as `Pending`, endpoint `Unavailable`, with the exact Herdr session, pane,
terminal and harness.  The result reports `Bound.{ <id> RegisteredUnconfirmed
}`.  An existing row can only receive its missing role when native session,
harness, session, pane and terminal match; another binding or role is refused
as `DuplicateFlowId` without a partial mutation.

The release's durable promotion is narrower than a new `Start`: a Pending
import becomes Active only after `Deliver` receives `Presented`.  `Presented`
means Herdr observed the target reacting to the typed message on the exact
bound pane.  The imported Codex endpoint remains `Unavailable` and does not
gate delivery or promotion.  Flow rechecks the current Herdr snapshot for the
session, pane, terminal, harness, readiness and state before it writes.  A
changed terminal, pane, harness, or noninteractive snapshot makes the route
unavailable; stale pending delivery is refused before a prompt.  A missing
pane is observed as `Exited`, never retired.

No native transcript receipt is required by the imported-row promotion path.
The import path requires process identity and working-directory evidence; the
promotion path requires the exact current Herdr route plus a presented typed
delivery.  Message supplies the typed delivery and grade.  This is a
source-backed implementation fact, not a claim that Astra's historical row
has these current witnesses.

## Smallest safe implementation

Do not add a second confirmation verb or a route-repair path.  Reuse the
existing imported-row transition: resolve the stored binding against a fresh
Herdr snapshot and let a single authorized typed Message delivery promote only
when it is `Presented`.  Preserve `Pending` for `Transported`, `Uncertain`,
or refusal.  Do not infer a native receipt, endpoint readiness, or acceptance
from `RegisteredUnconfirmed`.

## Meaningful source-level test plan

1. Keep an import fixture that proves accepted rows are Pending and reply
   `RegisteredUnconfirmed`; cover duplicate Flow ID, duplicate pane, dead
   process, wrong working directory, and conflicting role with no mutation.
2. Assert a valid exact Herdr route plus `Presented` delivery makes the
   imported Codex row Active while its endpoint remains Unavailable.
3. Assert terminal, pane, harness, and interactive-readiness drift makes the
   route unavailable before typing and retains Pending; assert a missing pane
   yields Exited and cannot be promoted.
4. Assert `Transported` and `Uncertain` do not promote, and repeated delivery
   returns its stored outcome instead of typing again.

## Limits and next step

The stable daemon's ordinary API directly supplied the durable row, so the
earlier report's statement that this was unavailable was wrong.  No delivery
confirmation action is indicated for Astra: it is already Active.  The test
plan remains a source-level plan for future imported Pending rows; validate it
against 0.17.4 before authorizing an implementation.

## Sources

- Live read-only `hm-list` on 2026-09-27: stable `flow-nexus 0.12.2` lists
  Mind Astra `6fe957` in `default`, state `done`.  It does not expose the
  durable lifecycle.
- `flows/56ae53/summary.md`: the earlier stable record describes Astra's
  imported Flow row as `Pending/RegisteredUnconfirmed`.
- Flow immutable release `bc464e5e1b94fcc179af73111f43b69db1f69fc5` (0.17.4):
  `crates/flow-nexus/src/lib.rs`, `store.rs`, `delivery.rs`, `herdr.rs`,
  `README.md`, `DESIGN.md`, and `UPGRADES.md`.
- Psyche topic evidence: `flows/836818/vision/flowNexus.md` and
  `flows/d8df70/vision/flowTool.md` authorize binding existing live Herdr
  flows through the meta socket.  They do not settle the later confirmation
  criterion.

The current store is held by the stable daemon, so this review did not read a
durable row directly.  The stable CLI exposes the current `done` projection,
while the earlier `Pending/RegisteredUnconfirmed` statement remains a recorded
source fact.  Before implementation, obtain a read-only stable-store or
daemon-owned List witness for Astra's actual lifecycle and exact binding.  If
it is still Pending, implement the tests above against 0.17.4 before any
authorized delivery-based confirmation.
