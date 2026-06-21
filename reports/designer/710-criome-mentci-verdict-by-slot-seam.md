# 710 — The criome-mentci verdict-by-slot seam (epic branch established)

The keystone seam from 708/709 is built, verified, and pushed as designer
prototypes on a new long-lived epic branch I now maintain for the
criome/mentci/spirit bootstrap. This unblocks the mentci CLI + GUI work the
psyche asked for ("start using mentci-lib with mentci's CLIs and GUI").

## What was built

The criome verdict path was *unwireable* because `signal-mentci`'s
`ApprovalSource::CriomeEscalation` carried no slot — an answered criome
question had nothing to key back to criome. Closed in two halves:

- **signal-mentci** (`criome-mentci-bootstrap` @ `eab23054`, off main
  `765ee355`): `CriomeEscalation` now carries the slot —
  `(CriomeEscalation AuthorizationRequestSlot)` — by **cross-importing the real
  `signal-criome:lib:AuthorizationRequestSlot`** (mirroring meta-signal-criome),
  not a local fork. `build.rs` adopts the dependency-schema `GenerationDriver`
  form; `src/lib.rs` adds `ApprovalSource::criome_slot()`; a round-trip test
  proves the slot survives the wire. The stale "cross-import deferred" note is
  retired (the grammar blocker is gone). 10 tests green, clippy clean,
  freshness gate holds.
- **mentci-lib** (`criome-mentci-bootstrap` @ `ad5bbedd`, off main `0731c374`):
  `on_user_event(AnswerQuestion)` now routes a *closed* answer on a
  criome-sourced question to `Cmd::SubmitCriomeVerdict { CriomeVerdict::from_decision(slot, decision) }`
  — keyed straight back to criome by the parked slot, zero stringly conversion.
  Non-criome answers still go over the mentci socket; `Defer` keeps the question
  pending and submits no criome verdict. **No new struct fields** — the slot was
  always recoverable off the retained question; it just wasn't typed before. 11
  tests green, clippy clean.

The decisive verification: the cross-import is a **re-export**
(`pub use signal_criome::schema::lib::AuthorizationRequestSlot`), so
`signal_mentci`'s slot *is* `signal_criome`'s type — `from_decision` accepts it
with no conversion. One typed identity end to end.

```mermaid
flowchart LR
    DA["mentci daemon<br/>projects parked criome question"] -->|"ApprovalSource::CriomeEscalation(slot)"| CL["mentci-lib ObservationModel<br/>(client: CLI / GUI)"]
    CL -->|"answer (close)"| SEAM{{"criome_slot() + from_decision(slot, decision)"}}
    SEAM -->|"Cmd::SubmitCriomeVerdict { request_slot, decision }"| RT["runtime / daemon"]
    RT -->|"meta-signal-criome SubmitAuthorizationApproval BY SLOT"| CR["criome — decider"]
```

## The proof (headline test)

`mentci-lib/tests/model.rs::answering_a_criome_question_routes_a_submit_criome_verdict_by_slot`:

```rust
let commands = model.on_user_event(UserEvent::AnswerQuestion { verdict });
assert_eq!(commands.len(), 1);
match &commands[0] {
    Cmd::SubmitCriomeVerdict { verdict } => {
        assert_eq!(verdict.decision(), AuthorizationApprovalDecision::Approve);
        assert_eq!(
            verdict.request_slot().payload(),
            AuthorizationRequestSlot::new("slot-1").payload(),
        );
    }
    other => panic!("expected SubmitCriomeVerdict, got {other:?}"),
}
assert_eq!(model.approval().pending().len(), 0);  // the question left the queue
```

A companion test proves `Defer` submits no criome verdict and keeps the
question pending — the safety guard the seam's `answered()` keying buys for free.

## The epic branch

`criome-mentci-bootstrap` is the designer-maintained epic branch for the
criome/mentci/spirit bootstrap (psyche direction, 2026-06-21). It exists per
repo in the bootstrap (signal-mentci + mentci-lib today; mentci + mentci-egui
next), recycled from the integrated re-found worktrees onto current main.
mentci-lib consumes the local signal-mentci epic via a `[patch]` that collapses
to the plain git dep at integration. Operator owns integration to each repo's
main from this epic.

## Spirit gate

No capture. The psyche's "I thought it would be a good client lib … probably a
good idea" answers 709-Q1 by leaning mentci-lib toward the **client-side**
library role (CLI + GUI), which is already consistent with `7x5z` ("reused by …
clients") — so this is greenlighting the direction, not a firm override of the
daemon-reuse aspiration. A `Clarify` that *dropped* the daemon-reuse clause was
correctly rejected by the guardian as `ClarifyTramples` (tentative wording must
not be laundered into a hard supersession). If the psyche wants the daemon-reuse
aspiration formally dropped, that is an explicit `Supersede` of the `7x5z`
clause — offered, not assumed.

## Operator handoff (daemon-side, after integration)

The prototype dovetails with operator's daemon wiring (450). After operator
integrates the two epic branches to main:

1. **Inbound** (`mentci/src/state.rs::into_question_proposal`): construct
   `ApprovalSource::CriomeEscalation(self.parked.request_slot.clone())` instead
   of the bare variant + the `criome-request-slot` `ContextBody`. The slot now
   lives typed on the question.
2. **Answer path** (`mentci/src/state.rs::answer`): on a closed answer whose
   matched question is `CriomeEscalation(slot)`, call
   `criome_bridge::submit_verdict(slot, decision)` — reading the slot straight
   off the source, no context-scan, no `String -> AuthorizationRequestSlot`
   round-trip. This makes the daemon's `submit_verdict` (today dead outside the
   test) live, closing the half-open loop (708 finding).
3. **Defer**: a deferred criome answer must not submit (mirror the model guard).

## Next on the epic

- **mentci CLI read+answer atom roster** — a grep-assertable observe/answer
  surface that prints the shared `RenderNota` and drives `mentci-lib`'s model
  (the first concrete "use mentci-lib with the CLI").
- **mentci-egui approval card** — render `ApprovalView.current` and emit
  `AnswerQuestion` / `ProposeEditedAnswer` through the shared model (the
  `pviw`/`gc0n` psyche-escalation surface made real), then a live subscription.
- **criome+mentci `runNixOSTest` on Prometheus** — the multi-daemon proof the
  seam ultimately needs (recycle `criome-nixos-module-142`).
