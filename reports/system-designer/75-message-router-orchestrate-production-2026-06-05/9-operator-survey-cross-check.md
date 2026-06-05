# 9 — Cross-check of system-operator survey 197 (+ "is the blocking work already done?")

Verifies `reports/system-operator/197-message-router-orchestrate-triad-port-survey-2026-06-05.md`
against source and against this session's reports 1-8. The psyche's prompt: *"Verify
his findings. Maybe the blocking work is already done."* It is — substantially. Read
2026-06-05, after report 197 was committed (`c2b26fe7`).

## Verdict: 197 is accurate and aligned; one finding is now STALE in our favor

The operator's survey agrees with report 75 on every load-bearing point and adds no
contradiction: all three are pre-triad (confirmed); message is the smallest /
intentionally stateless; router is the delivery brain; orchestrate is the best first
`MultiListenerDaemon` candidate (already 3 sockets, on `sema-engine`); persona is the
supervisor and orchestrate is a supervised child; message stays Signal+Nexus; the
move-order is foundation → orchestrate/message → rename → router → delivery spine →
persona. His repo-state ledger (line counts, "multi-listener landed; streaming
dirty/in-flight") matches what I see. **The one finding that has gone stale — in our
favor — is the streaming-foundation status, which is the crux of the psyche's question.**

## The blocking work that IS already done (verified in source)

Both report 197 and my report 3 (`brgo`) treated **schema-derived streaming/push** as
the not-yet-done foundation slice and the #1 thing to finish before porting. Since both
were written, it has **substantially landed**:

| Foundation piece | Report 197 / report 3 said | Actual state now (verified) |
|---|---|---|
| `schema-rust-next` streaming emission | "dirty/in-flight" (197); PROPOSED (rpt 3) | **LANDED on `main`** — `4ee2c898 emit schema streams through signal-frame`; `StreamDeclaration` + `streams()` + `emit_signal_frame_support(&root_enums, &streams)`; clean working copy on top |
| `signal-frame` stream surface | "primitives exist but daemons don't consume them" (op 320 audit) | **schema-marker / crystallized-stream surface on `main`**, clean working copy — the emitter now consumes them |
| `triad-runtime` runner-side streaming | "dirty/in-flight"; "main unsolved slice" | **uncommitted but written + tested** — `src/streaming.rs` (244 lines: `SubscriptionRegistry`, `Subscription`, `SubscriptionEventSequence`, `SubscriptionEventPublisher`) + `tests/streaming.rs` (4 tests incl. `subscription_event_publisher_builds_signal_frame_streaming_events`) |

So the streaming/push slice is ~80% landed: the **emitter (schema-rust-next) and the
wire kernel (signal-frame) are committed to main**, and the **runner-side subscription
registry/publisher (triad-runtime) is written and green, just not committed**. The
operator's citation of `reports/operator/320.../2-signal-frame-push-audit.md`
("schema-derived daemons do not consume the streaming primitives") is now stale — the
`emit schema streams through signal-frame` commit is exactly that consumption.

## The more important correction: streaming does NOT gate the first ports anyway

Report 197's move-order step 1 — *"Finish or intentionally bracket the operator's
streaming/push work. Do not start a port that needs subscriptions until the streaming
surface is clear"* — over-gates. It is correct that a *subscribe-shaped* feature waits
on streaming, but the **first ports are request/reply** and do not need it:

- message: ingress → stamp → `ForwardToRouter` effect → reply. Request/reply.
- router (first slice): accept `StampedMessageSubmission`, adjudicate, deliver, reply;
  channel grant/retract via the meta socket. Request/reply. (Delivery-delta
  *subscriptions* are a later slice — those need streaming.)
- orchestrate (first slice): claim/release/handoff/observe/submit/query, the owner
  verbs. Request/reply. (`Watch`/`Unwatch` is the one subscribe verb — defer it.)

Report 3 already drew this line precisely ("a port that needs push/subscribe hits this;
a port that only needs request-reply does not"). Net: **even the remaining uncommitted
triad-runtime streaming piece does not block the orchestrate-first or the message+router
request/reply ports.** They can start now.

## The blocking work that is genuinely NOT done

- **The meta-signal rename (`r9qy`) has not run.** Verified on disk:
  `owner-signal-router` and `owner-signal-orchestrate` still present;
  `meta-signal-router` / `meta-signal-orchestrate` absent. (The standard exists —
  `meta-signal-cloud` / `-domain-criome` / `-upgrade` are on disk — so it is
  mechanical, but it is a real prerequisite for the meta-tier slice, and it is
  coupled across router + orchestrate.) Both reports agree.
- **No worked `MultiListenerDaemon` reference daemon** — committed + tested in
  triad-runtime, unexercised by any daemon. orchestrate-first establishes it. (Agrees
  with report 5/6 and report 197 §"prove multi-listener through orchestrate.")
- **`triad-runtime` streaming not yet committed** — only matters for the later
  subscribe-shaped slices, not the first ports.

## Intent cross-check (forwarded-capture gap-check)

The operator logged `(Spirit Decision 3chp, High)` [The policy and control socket in
triad components should be called the meta socket, not the owner socket.]. This is
correct, aligns with `r9qy` (the contract-repo rename) and the component-triad skill,
and complements rather than duplicates them (3chp = socket name; `r9qy` = contract-repo
name). No gap to fill; good capture.

## Net answer to the psyche

Yes — the blocking work is largely already done. The streaming/push foundation that the
operator survey names as the #1 thing-to-finish-first is mostly landed (emitter + kernel
on main; runner registry written + green, uncommitted), AND it does not gate the first
request/reply ports regardless. The one genuine remaining prerequisite — the meta-signal
rename — is mechanical and only gates the meta-tier slice. **So the orchestrate-first
port (and the message+router request/reply spine) can start now; the "finish foundation
first" gate is effectively lifted for the request/reply slices.** The streaming surface
should be finished before the *subscribe* slices (router delivery-delta subscriptions,
orchestrate `Watch`, introspect taps) — but those are not the first deliverable.
