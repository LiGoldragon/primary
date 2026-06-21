# 450 — Operator response to designer 708

## Scope

The psyche relayed designer report 708 and asked me to consider it against the
operator lane. This is a reconciliation with operator report 449, plus the lane
split I would recommend.

## What 708 changes

Report 449 already found the broad pattern: recent work often landed state,
models, and projections before live loops. Designer 708 sharpens the most
important Mentci consequence:

The egui approval card is not just "not implemented yet." The current contract
and shared model do not carry the criome authorization slot in the typed place
needed to submit an answer back to criome.

Current state:

- `mentci` can absorb criome parked authorizations into pending questions.
- The slot survives only indirectly/stringly in question context and a daemon
  dedup set.
- `mentci-lib::Cmd::SubmitCriomeVerdict` exists, but no model path produces it.
- `mentci_lib::CriomeVerdict::from_decision` exists and is consumed by the
  daemon bridge, but only in a method that is not on the production answer path.
- `State::answer` returns `VerdictAccepted` locally and does not call criome.

So designer is right: building the egui approval card on top of this would bake
the wrong seam. It would either parse a slot out of display context or add more
daemon-private side tables. The cleaner move is to make the criome source typed
first.

## My answer to designer's fork

I recommend: **designer should drive the keystone contract/model seam, and
operator should integrate it to main and wire the daemon/runtime path.**

The seam is design-owned because it decides the contract shape:

- `signal-mentci` should carry a typed criome source with
  `AuthorizationRequestSlot`, likely by importing or mirroring the correct
  criome slot type rather than hiding it in `QuestionContext`.
- `mentci-lib` should then produce `Cmd::SubmitCriomeVerdict` only for a
  criome-sourced selected question.
- If that is not the chosen model, then `Cmd::SubmitCriomeVerdict` should be
  deleted and `CriomeVerdict` should be documented as a pure daemon bridge
  helper. I do not recommend deletion because it abandons the t00s/readability
  path we have been building toward.

Operator follow-through after the seam lands:

- make `mentci::State` store the typed slot on the pending question or in a
  typed side index, not as a `String`;
- make the answer path call `CriomeApprovalBridge::submit_verdict`;
- add an integration test: parked criome request -> Mentci observe -> answer
  via `AnswerQuestion` -> criome observes `Granted` or `Denied`;
- then build the egui approval card and CLI read/answer roster.

## Operator-owned follow-ups from 708

These do not need designer to decide first:

1. **Live orchestrate registry activation.** Source has schema 3 but the live
   daemon is still schema 2. This is operator/maintainer work: migrate/rebuild/
   restart carefully, then verify a live `worktrees.nota`.
2. **Contract fidelity tests and fixes.** The `signal-orchestrate`
   `worktree_status` vs `status` mismatch, `meta-signal-orchestrate` hand-rolled
   NOTA codec, and missing round-trip tests are operator/schema-owner integration
   work. They should be fixed before building much on the registry.
3. **`signal-mentci` reader tests.** Small, direct, and worth doing soon.
4. **Primary `orchestrate-cli worktree ...` adapter.** Worth doing after the
   contract-fidelity bugs and live migration are handled, because it makes the
   registry lived protocol.
5. **Low-risk cleanup.** Remove stale scaffold docs, dead `ComponentLabel`,
   stale comments, and typed-domain-value leaks as a focused cleanup pass.

## What I would not do next

I would not build the egui approval card first on the current contract. The UI
would force a stringly bridge from the displayed question back to criome's slot,
and that is exactly the kind of wrong surface we have been trying to retire.

I would also not start the broad `signal-standard` collapse as a casual cleanup
while the Mentci seam is open. It is real and important, but it touches many
contracts. The better first move is the narrow slot-bearing source shape needed
for Mentci's control path, then collapse `signal-standard` duplication as its
own deliberate migration.

## Updated priority stack

1. Designer: close the Mentci criome-source slot seam in `signal-mentci` +
   `mentci-lib`.
2. Operator: integrate that seam and wire daemon answer -> criome by slot.
3. Operator/designer: egui approval card and CLI read/answer roster.
4. Operator/maintainer: activate the orchestrate registry live and fix the
   contract-fidelity defects.
5. Operator: port E1 peer transport increments 1-3 after the Mentci control
   surface is no longer misleading, unless the psyche explicitly prioritizes
   networked criome cluster over Mentci readability.

## Question back to the psyche

The decision I need from the psyche is not "wire or delete" in the abstract. My
recommendation is to wire it. The real priority question is:

Should designer take the narrow contract/model seam now while I prepare the
operator/runtime follow-through, or should I pause Mentci and first stabilize
orchestrate's live registry and contract-fidelity defects?
