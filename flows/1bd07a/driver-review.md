# Proposal 2 driver: current source handoff

The candidate source is assembled and unreviewed. It requires a manifest-bound independent-review record and Field admission, and the template contains pending values. Source assembly confers no execution grant. No fixture, provider, service, native, credential or workload action was executed in this work. No stage, commit or push was made.

## Current changes

- `controller.py`: admission/artifact validation and private-workload wiring; private endpoint binding; actual dynamic rehearsal receipts; matrix invocation.
- `bootstrap.py`: private staging, exact provider checks, owned daemons, event readiness and private socket peer/process endpoint binding.
- `orchestration.py`: external unit and pidfd-bound peer custody, supervised operator forwarding, held ready/go, production witnesses, terminal/cgroup reconciliation and outside-root evidence retention.
- `matrix.py`: observed initial turns; ordered A/B admission and Field-captured own-session consumption; typed wrong-kind/duplicate, kept-answer and routed-result checks; one successor and carry checks; control completion cuts; exact-flow and pane closure. ObserveSends is drained by a supervised event-driven thread after its opening receipt; its failure pipe is monitored while waiting for Field, and cleanup stops and joins the drain before closing its resources. Failure is also raised at cleanup. No consumer polling is used.
- `provider-manifest.template.json`: pinned candidate package inputs and explicit pending Field/review/runtime/retention values.
- `test_controller.py`, `test_bootstrap.py`, `test_orchestration.py`, `test_matrix.py`, `test_wiring.py`: source fixtures, including drain retention, EOF failure and join, and fake matrix lifecycle/failure. `TEST-SPEC.md` describes the boundary.

## Field frame protocol for independent review

The outer operator process creates `root/evidence/startup-envelope.json` containing its PID/start ticks/nonce. Field writes newline-delimited JSON frames to the outer operator's stdin, each with that exact `nonce`; the forwarder verifies and removes it before delivery. Frames go through the in-unit FIFO. Field prepares referenced files under `root/evidence` or `root/transcripts` as owned single-link regular files, at most 1 MiB; each reference is `{ "path": "relative/path", "sha256": "..." }`. The channel retains the submitted frame and referenced bytes. The process identity and nonce are custody checks, not a cryptographic authentication claim.

1. The driver retains the actual sender/receiver rehearsal hashes in `evidence/operator-channel/rehearsal-review-request.json`. Review both full receipts for the admitted private route, endpoint, home, hook, place and Luna/medium. Submit `{ "nonce": "...", "cut": "rehearsal-review", "sha256": { "sender": "...", "receiver": "..." }, "decision": "approved" }` with those exact actual hashes. Refusal, mismatch, peer exit or timeout stops the run.
2. After both actual initial TurnEnded events, each sender admission frame has `cut: "admission"`, `label`, `kind`, `marker`, `request_id`, `minutes` (15 for a Task, null otherwise), `invocation`, `receipt`, and `identity` equal to the captured sender binding. Invocation files hold `{ "call_id": "...", "arguments": {...} }` for native tool calls or `{ "call_id": "...", "command": "..." }` for CLI calls. The arguments/command and typed receipt are checked. Ordered A labels are O/Q/T/N/L; B labels O2/Q2/T2. Call IDs and request IDs cannot be reused.
3. After the receiver instruction, each separate consumption frame has `cut: "consumption"`, `label`, `request_id`, `marker`, `identity` equal to the captured receiver binding, `reply` containing the exact marker and ID, and `transcript` referencing Field's capture of that receiver's own-session reply. Task replies additionally include Minutes. Admission itself is not consumption.
4. For each requested reply outcome, send `{cut: "reply-outcome", label, surface, identity, invocation, response}`. `surface` is native or cli; `identity` is the currently bound receiver. Source-captured invocations include a unique call ID and exact arguments/command. The response file contains the raw native JSON tool response or raw CLI datom. Frames are consumed in the source-defined sequence, including separate duplicate new calls. Routed sender acknowledgments use `cut: "routed-consumption"`, label, original `request_id`, marker, sender `identity`, `reply` and `transcript`.
5. Before a control Question's Answer is read, submit `cut: "control-completion"`, `request_id`, `side`, matching `identity`, `invocation` and `response` references. Its native Result invocation and Kept reply must match that control ID and sender. These cuts are consumed in control insertion order. The unbound K Question has its own receiver consumption and kept-result cuts.
6. After the subscribed metaflow event establishes a new FlowId, submit `cut: "successor"`, `binding` (flow_id, native_session, herdr_session, agent, pane, terminal) and `first_prompt` reference. Current, Inspect and private Herdr independently bind the proposed route. The first prompt must contain Q2/T2 IDs and original question/task markers and Task Minutes, and exclude the Order ID and marker. The subsequent `cut: "successor-report"` frame carries successor `identity`, `reply` and `transcript`; the own-session reply names both IDs, Task text marker and Minutes. Later successor outcomes and routed acknowledgments use the same reply-outcome/routed-consumption forms.

Review the source for the exact label, message and control order; this protocol is a handoff to the reviewer, not authorization to run it. No provider acknowledgement or native PID binding is claimed as the consumption oracle. Source 319e3c3 publicly exposes Task ID, Minutes and text, not an absolute due timestamp; the source-level deadline-carry gate is separate, and the driver uses a conservative monotonic 15-minute cutoff.

## Acceptance matrix

| Item | Status |
| --- | --- |
| Source wiring, event-driven sends drain and fail-closed cuts | Present, unreviewed |
| Nine Python source syntax parses and manifest JSON syntax | Passed, syntax only |
| Synthetic fixtures | UNRUN |
| Candidate and package gate | Inherited handover evidence, not rerun here |
| Manifest runtime values, immutable source hashes and independent nonwriter review | Pending |
| Separate fixture and native/Field admission | Pending |
| Native receipts, own-session observations, successor, closure and terminal/cgroup-empty witnesses | Unobserved |
| Production before/after comparison and outside-root retention | Unobserved; retention copies evidence and Field transcripts and is not a proven secret-filtering boundary |
| Final switch | Not admitted |

Exact **UNRUN** fixture command, requiring a separate grant:

```sh
cd /home/li/primary/flows/1bd07a/driver && python3 -B -m unittest test_controller test_bootstrap test_orchestration test_matrix test_wiring
```

Current source/fixture hashes are in `/tmp/proposal2-source-work.bkRQITc6/final-hashes.txt`. The reserved independent reviewer must examine the immutable artifacts, source-bound event and receipt shapes, Field frame ordering and attribution, evidence safety, dynamic review, deadline handling, concurrency and retention/cleanup failure paths before any execution.

## Primary review packet custody

Successor 89ad44 continues the same source-only paths under reservation 433,
confirmed by Core r40p. Core dispatches its existing reserved nonwriter; there
is no duplicate auditor. Core txl0 relays Psyche t39d: Field's capture of the
recipient model's own reply in its own native session naming the delivered
RequestId is the consumption witness required for this release.

The Flow source remains fe5a6930871707a7086c9a647867a519734220ef in
/git/worktrees/flow-order-lifetime-2b25fa. Its accepted whole-gate witness is
/tmp/order-gate-provenance.yIWhQJ/report.md; no separately stamped rebuild is
required. Package publication and the accepted three-package phase are recorded
in source-publication.md and package-result.md beside this packet. The driver
changes do not change that Rust candidate. All unrelated inherited work stays
held. No fixture, native, auth-link, service or live grant is asserted.

Primary independently repeated only AST/JSON syntax parsing and git diff --check;
all passed. No driver module was imported and no fixture was run. The commit and
sealed-source digest accompanying this report identify the reviewed artifact.
