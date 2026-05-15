# 120 - Hard Context Maintenance

*Operator maintenance ledger, 2026-05-15. Purpose: reduce the live
operator context surface after the Signal redesign chain was compressed
into newer designer-assistant reports, and name the current pickup
points for the next implementation pass.*

## Current Load-Bearing Truth

Sources read for the current Signal / sema-engine slice:

| Path | Inline summary |
|---|---|
| `reports/designer-assistant/61-signal-redesign-current-spec.md` | Current compact Signal spec: six `SignalVerb` roots, non-empty requests, async lane/sequence frame exchanges, no payload metadata. |
| `reports/designer-assistant/62-signal-redesign-implementation-brief.md` | Operator implementation brief: first slice is `signal-core` primitives, async exchange state, and sema-engine structural commit logs. |
| `reports/designer/176-signal-channel-macro-redesign.md` | Macro redesign; its top update removes intent, `NoIntent`, tracked/named constructors, and three-axis frames. |
| `reports/designer/177-typed-request-shape-and-execution-semantics.md` | Typed request semantics; read through the corrections in `/176` and DA/61, not as a standalone intent-bearing spec. |
| `reports/operator/115-sema-engine-split-implementation-investigation.md` | Still-current operator guide for the `sema` / `sema-engine` split, now marked so its old `SemaVerb` / `Atomic` language is historical. |

If the DA/61 or DA/62 files have not landed in version control yet,
use the inline target below as the operator pickup summary until the
designer-assistant commit lands.

The current target is:

```text
signal-core:
  SignalVerb = Assert Mutate Retract Match Subscribe Validate
  NonEmpty<Value>
  Operation<Payload>
  Request<Payload>
  Reply<ReplyPayload>
  SubReply<ReplyPayload>
  ExchangeHandshake
  ExchangeMode::LaneSequence
  ExchangeIdentifier
  Frame<RequestPayload, ReplyPayload>
  FrameBody<RequestPayload, ReplyPayload>

sema-engine:
  no SignalVerb::Atomic
  no AtomicBatch / AtomicOperation / AtomicReceipt public names
  structural commit/write request shape
  commit log carries one snapshot and per-operation write effects

runtime:
  connection actor owns lane ownership, outgoing sequence, pending map
  wrong-lane, duplicate-open, unknown-reply, duplicate-reply paths are protocol errors
```

## Retired Operator Reports

These reports were working notes during the redesign, not permanent
architecture. Their useful substance is now absorbed by DA/61 and
DA/62, with the sema-engine split parts preserved in `/115`.

| Retired path | Reason |
|---|---|
| `reports/operator/116-early-evaluation-typed-request-and-channel-macro.md` | Superseded by the post-DA61 compact spec; kept reviving old `Intent`, `RequestHeader`, and `Atomic` context. |
| `reports/operator/117-post-175-signal-core-sema-engine-readiness.md` | DA/62 explicitly absorbs its useful sema-engine-first correction. |
| `reports/operator/118-frame-metadata-correlation-impact.md` | Superseded by DA/61's layer split and async exchange spec. |
| `reports/operator/119-async-first-signal-exchange-impact.md` | Superseded by DA/61 and DA/62, which carry the same async-first lane/sequence decision in compact form. |

Do not chase those paths from stale cross-references. Use DA/61 and
DA/62.

## Kept Operator Reports

| Path | Decision |
|---|---|
| `reports/operator/108-persona-mind-system-overview.md` | Keep for persona-mind system context until a newer mind implementation report replaces it. |
| `reports/operator/109-beads-audit-and-session-discipline.md` | Keep while BEADS remains the transitional coordination substrate. |
| `reports/operator/110-persona-meta-integration-start.md` | Keep as early persona meta-integration context; review later when persona daemon work resumes. |
| `reports/operator/111-persona-daemon-implementation-review.md` | Keep as scaffold review, but newer daemon/supervision reports win where they conflict. |
| `reports/operator/112-persona-engine-work-state.md` | Keep as implementation state snapshot until replaced by a working engine report. |
| `reports/operator/113-persona-engine-supervision-slice-and-gaps.md` | Keep for supervision slice and gap inventory. |
| `reports/operator/114-persona-introspect-prototype-impact-survey.md` | Keep because introspection remains prototype-critical. |
| `reports/operator/115-sema-engine-split-implementation-investigation.md` | Keep as the sema/sema-engine split guide, with the Signal vocabulary caveat added in this pass. |

## Next Implementation Pickup

The next operator pass should work from DA/62's first slice:

1. Update `signal-core` toward the six-root async exchange model.
2. Move `sema-engine` in the same wave so no public or logged path uses
   `SignalVerb::Atomic` or Atomic-colored names.
3. Add Nix witnesses from DA/62: non-empty request/reply, two-axis
   frame, lane ownership, duplicate/unknown exchange errors,
   out-of-order replies, and no payload exchange ids.
4. Only after the core shape builds, update `signal_channel!` and the
   contract repos.

Implementation should not reintroduce:

- `Request<Payload, Intent>`;
- `RequestHeader<Intent>` or `ReplyHeader<Intent>`;
- `CorrelationId` for request matching;
- `NoIntent`;
- `single_named`, `single_tracked`, or `batch_tracked`;
- `(Batch ...)`, `(Named ...)`, or `(Tracked ...)` as core-visible
  human input.

## Working-Copy Note

At the time of this maintenance pass, the workspace also contains dirty
files owned by other roles, including DA/61 and DA/62, designer report
edits, and lock/workspace files. Operator did not normalize or commit
those. This pass touches only operator reports.
