# 052 context warning — small supplemental proposal

New delta; NOT covered by the existing body grant. The living's exact ruling is recorded in this flow's vision/flow-nexus.md. Existing052 implementation and completed independent review remain valid for unchanged scope. This proposal requires Core judgment on the decisions below before any warning bodies.

## Observed source boundary

At immutable916, Claude hook Stop sends NativeStop session_id/transcript_path/last_assistant_message, not token counts (hook.rs120–165). Nexus reporting.rs61–86,118–165 reaches settle_stopped; waking.rs1003–1042 validates registered session and reported path against the Nexus-resolved native transcript. waking.rs2715–2737 reads actual transcript context tokens, records FlowContextSize{flow_id,tokens}; claude.rs434–481 derives main-thread input+cache-read+cache-creation token usage. This is a hook-correlated observation, not an inferred percentage from a stored old row. Codex token records currently arise from appserver/compaction usage, not a demonstrated hook handoff. Do not claim Codex warning parity from those records.

Model threshold is existing ConfigureThreshold{ModelName Refresh.Integer}, in TOKENS. Existing model selection uses role.model_name or the actual launch attempt profile; use that SAME selection, not a second model table. Existing context classification treats equality as Past; normal delivery rejects Past. Source pointers: context.rs110–174, delivery.rs216–226. Actual same-flow notice helper and duplicate-event semantics are the last bounded source pointers requested; warning delivery must not silently weaken the existing threshold refusal.

## Two explicit startup values, same configuration machinery

The Ethos addition to the ONE resolved RuntimePolicy, with generated per-value ConfigurationChange variants and existing startup/Memory/meta resolution:

```ethos
ContextWarningShare.{ Numerator.Integer Denominator.Integer } ; exact dimensionless rational
ContextWarningMessage.String                                  ; exact configured warning text
```

Both are required final resolved values: startup-present overrides, absent preserves committed value, absent both refuses before effects. No Rust percentage or message default. A message is nonempty, not a format string or shell expression; reuse normal typed message size/transport checks. Share requires 0 < Numerator <= Denominator, both representable positive Integer. Existing model threshold remains independently configured; do not duplicate it in warning configuration. This extends the still-unreleased runtime-policy-v1 shape explicitly, not an old-store silent enum/row change.

Compare a nonnegative actual token observation C to model threshold T > 0 using exact `C * Denominator >= T * Numerator` in checked wide arithmetic. For current signed64-bit nonnegative operands, u128 products fit; conversions are checked. Equivalent integer cutoff is ceil(T*N/D); no floating point or early rounding. Zero, negative or unrepresentable policy values refuse configuration. Missing/invalid model threshold produces no invented threshold or warning; retain the existing typed NoThreshold/not-configured outcome and surface it through the operation's existing reporting path.

## Trigger and delivery decision proposed

Only a NEW accepted hook-correlated observation of THIS FlowId and registered native session may evaluate/emit the warning. Startup, persisted FlowContextSize replay, timer/scan, cached transcript reread without a new accepted hook handoff and configuration changes alone never trigger it. A validated hook's source contains actual context; missing context is not zero, and unrelated/mismatched hook/session/path is not eligible. The current body grant does not authorize inventing a hook context payload or claiming the separate hook-handoff fix complete.

Recipient is that SAME FlowId/native session, using the existing ordinary same-flow notice delivery path with its normal typed outcomes and priority, once the bounded helper signature is pinned. No hook stdout message, no different-address successor delivery, no special caller class. Existing Past/delivery gates remain: if a newly observed context has already exhausted the model threshold, the normal path may refuse; record that outcome honestly, never claim the recipient was warned or bypass the gate silently. Core must explicitly judge whether this limitation is acceptable or a separate control-notice capability is required. A value Share=1 exposes this case directly; no hidden narrowing of the configured domain masks it.

## Repetition proposal requiring judgment

Use a minimal **runtime-only** warning latch, following the existing version-zero in-process refusal-notice suppression pattern; this is transient working state, not a handover saved in Memory, not a new persisted family. This is an explicit proposed version-zero choice, not an inferred standing architecture rule.

- Key by held FlowId and native session. Arm initially; an eligible below-cutoff observation rearms it.
- An eligible observation at/above cutoff requests the warning only while armed. Reserve the latch before dispatch so concurrent reports cannot duplicate emission. Confirmed delivery or possible-effect uncertainty suppresses further warnings for that crossing; a known pre-effect refusal can remain armed for a later NEW hook observation, with no automatic retry timer.
- While context stays above cutoff, additional observations do not repeat the warning. This is a proposed crossing policy; the living's “only once ... actually receives” did not establish once-per-session semantics.
- Warning share/message change or selected model/threshold change rearms the relevant latch. Such a change does NOT itself send; the next actual eligible hook observation evaluates the new committed snapshot. Other configuration changes do not reset warning state.
- Nexus restart loses transient latches. It sends nothing from Memory on startup; the next eligible observation may warn again. Native session replacement also starts armed. These are disclosed repeat boundaries, not a durable exactly-once claim.

No context/handover text or warning latch is added to Memory. Existing measured token rows remain as they are. Old delivery receipts must not rearm a new native-session latch. The exact existing hook deduplication behavior is still being pinned; no receipt-as-read assumption is made.

## Minimum tests and consumer rows

1. Startup absent/present/preserve/invalid share/message; exact generated field mapping, no literals in runtime code.
2. Rational boundary and equality, non-divisible thresholds, maximum representable operands, missing/invalid threshold. Exact model-selection parity with existing context gate.
3. Actual accepted hook context triggers; missing context, mismatched session/path, stale/cached rows, startup and config-only events do not. Codex appserver measurements alone do not satisfy the hook prerequisite.
4. Same-flow delivery and exact configured text; known pre-effect refusal vs uncertain delivery; exhausted-threshold behavior remains explicit and cannot be disguised as successful warning.
5. Concurrent above-cutoff reports emit at most one warning per armed epoch; continued high observations suppress; below then above rearms. Config/model/threshold change and restart/session-reset semantics exactly as stated; no timer replay.
6. No Memory handover field/schema/table; original configured threshold/FlowContextSize schemas unchanged. Actual hook-handoff/native delivery proof belongs to isolated acceptance, not source assertions.

Only the warning policy leaves, actual accepted hook-context consumer, existing same-flow delivery call, transient latch owner and these tests are in this delta. No new audit, worker, production051 action, capsule or publication is authorized by this proposal.

## Bounded delivery and duplicate-hook evidence

Actual existing exact-FlowId path is `DeliversMessages::deliver(&self, meta_signal_flow::DeliveryRequest) -> Response` in delivery.rs190–226. Its request carries DeliveryId, FlowId and Message; Message has HardAbrupt/MiddleAbrupt/Soft(Letter). It still refuses PastThreshold except for the existing unrelated refresh-refusal suppression path. The warning must NOT claim that exception or reuse its latch.

The ordinary `accept_logical_delivery` helper in store/logical_delivery.rs586–612 targets Address, not exact FlowId. Existing successor-refused warning waking.rs2897–2945 sends UP and wakes it; it is not evidence for delivering a warning to the original same flow. Proposed transport is the existing exact-FlowId delivery capability with Soft configured text, preserving all current gate/outcome semantics; actual Letter construction and delivery-id allocation must be pinned before body wiring. No new meta operation or warning-specific threshold bypass is implied. Core must judge Soft priority and treatment of a late/Past observation explicitly.

NativeStop has only optional native session, transcript path and last assistant message (signal853–857); there is NO stop event/prompt id. Correlation validates Claude registered session/path but does not deduplicate a Stop. reporting.rs records each accepted event and store/events.rs359–385 appends it. Therefore the proposed latch is necessary for repeated identical above-cutoff hook observations; the design cannot rely on nonexistent upstream stop-event deduplication. NativePrompt's separate prompt id is not falsely borrowed as the Stop identity. A stale lower-context observation remains a real rearming concern: before permitting rearm, the trigger must use the current validated transcript usage for this hook, not blindly treat a payload count as the latest state. Exact producer/source ordering must be verified in the warning-specific tests.

## Core judgment — approved policy, delivery still gated

Core approves required rational0<N<=D and nonempty literal message, exact wide comparison and existing model selection; evaluation only on a NEW validated context receipt. Core approves transient perFlowId/native crossing latch and the proposed below/config/model/threshold resets, predispatch reservation, uncertainty suppression and disclosed restart repeats. No Memory handover.

Core rejects ordinary Past refusal as fulfillment of the warning contract. Share1 and late jumps need a useful outcome. Exact lower control/notice emission and threshold-settlement ordering must be pinned before proposing the smallest same-session warning capability alongside ordinary user-message admission. No blanket Past bypass, successor routing or prevention of refresh. If native warning cannot be delivered before retirement, that limitation goes to Psyche for judgment. Policy leaves/latch/warning bodies remain HELD until exact delivery/dedup contract and independent delta review. The already granted unchanged052 implementation proceeds.

## Controlling delivery delta — proposed after Core's narrow capability ruling

This section replaces the earlier ordinary-delivery/Soft/Past-refusal proposal. Ordinary user-message admission remains unchanged. Add a private Nexus capability, `WarnsCurrentSession`, accepting only a validated context receipt plus the committed warning-policy snapshot; no public query, Address/Up recipient, arbitrary caller message or refresh-refusal exemption. Its target contains the exact held FlowId/native session and current route. The configured literal text is its only message source.

Proposed internal outcome is `WarningOutcome.[ PreEffectRefused.WarningRefusal Presented Transported Uncertain ]`, with existing typed native failure/observation payloads retained where their meanings fit. Presented means observed placement/submission evidence, NOT model consumption. Transported means submission without observed reaction. Any possible-effect/persistence uncertainty suppresses repetition; it is never returned as a clean refusal. No additional persistent warning family or handover is proposed.

### Settlement composition

Observed current order: reporting.rs61–86/118–165 → correlated Stop → settle_stopped/waking1347 → settle_rested3044 → record_context_at_stop2715–2740 → rest/admission checks → past_threshold3091 → refresh_due3137 or close_at_rest2761–2777. `record_context_at_stop` currently discards read/record failure in its unit result. Replace that internal result with a typed eligible observation or explicit failure/absence; a failed read/write cannot manufacture a receipt.

1. Read and validate current native transcript context for the correlated hook. Serialize observation/rearm against other warning observations so an older completed read cannot reset a newer crossing. Below-cutoff rearm requires a genuine newly observed current usage state, not duplicate hook identity (NativeStop has none).
2. In the existing lifecycle/admission serialization interval, revalidate exact FlowId/native/current route and that no successor/retirement has won. Capture model, threshold, warning policy and bounded transport budgets once. Reserve the transient crossing latch before emission. If lifecycle has already changed, return typed pre-effect refusal and never address the successor.
3. Hold the existing pane lease through the private same-session warning attempt and observation, before allowing this settlement to initiate successor creation or close. Factor the lower leased delivery execution so this capability does not call public delivery recursively under its locks. It may pass the threshold boundary ONLY for its internally constructed warning; ordinary Past rejection stays intact. All other native readiness/route/identity constraints remain checked.
4. Run at most ONE bounded native placement/submission attempt using the existing configured delivery timeout/observation budgets captured above. No new hardwired timeout and no retry loop. On its finite completion, record the truthful outcome/latch state, release the pane lease, and continue ordinary threshold settlement/refresh regardless of warning success. The implementation must show the actual aggregate bound and lock order from the selected lower executor before this delta's bodies; a component timeout alone is not an aggregate bound.

The serialization interval prevents a competing lifecycle operation from creating a successor between warning admission and this attempt's completion. It does not claim model execution is serialized with the Nexus. No lock is held indefinitely awaiting a model response. An already busy/occupied composer may prevent safe placement; refusal is surfaced, not followed by forced interrupt or message displacement.

### Real limit requiring judgment

The existing lower engine (delivery.rs326–359/461–600 and herdr/pane.rs82/279) observes pane/terminal placement and composer submission. Presented requires matching pane/terminal `agent_prompted` and composer text removal; Transported has weaker reaction evidence. Neither proves the model read the warning. Close uses the same pane lease but no existing read acknowledgement exists. Thus this composition can guarantee an ordered, bounded attempt and truthful placement evidence BEFORE retirement, not that a flow reasons about the warning before retirement. Share1/late jumps get that attempt rather than ordinary Past rejection. If “warns” requires consumption or a response before refresh, this transport cannot establish it; Psyche must judge the limitation rather than this implementation inventing a read receipt or delaying refresh indefinitely.

### Delta acceptance additions

Test share1/late jumps invoke only the private warning capability while ordinary messages still reject Past; concurrent successor creation cannot overtake the reserved warning attempt; exact native-session replacement refuses before effects; duplicate high hooks cannot rearm; stale lower observations cannot reset a newer crossing; missing/failing actual context produces no warning. Fault every placement/submission/observation/persistence boundary: truthful pre-effect versus possible-effect outcome, bounded settlement continuation, no retry to successor. Test occupied composer and no observed reaction explicitly. Verify no recursive lifecycle/pane-lock acquisition and measure the aggregate configured attempt bound. Native capsule evidence remains separately authorized; neither Presented nor Transported is labeled read.

## Latest controlling Psyche simplification

This supersedes the prior at/Past capability and its settlement proposal. Warn only when the newly validated actual receipt satisfies `C < T` AND `C*D >= T*N`. At/above threshold, skip warning and proceed with ordinary refresh without warning delay. Share=1 is valid and has no pre-threshold warning opportunity; no clamp/default. No at/Past exception or new control-delivery machinery is to be built. Same-session identity, crossing latch and literal configuration remain as approved. Native submission evidence is sufficient; no model read acknowledgement is required. A stale composer placement is not submission.

Below-threshold outcomes must distinguish pre-effect refusal, observed submission and possible-effect uncertainty. The ordinary exact-session lower delivery can be composed only with the correct existing lock ownership; no public meta dispatch recursively under dispatch_gate and no second pane-lease acquisition.

### Newly pinned deadline gap — unresolved before bodies

Bounded source evidence from Secondary: current `Command.output()` in herdr/pane.rs239–303 and herdr.rs744–747 has no parent deadline/kill. The Herdr `--timeout10000` flag bounds an observation, not the subprocess. PaneLease mutex/Condvar wait (delivery/lease.rs49–65) has no deadline. Durable delivery query/commit (store/delivery.rs290–331) has no wall-clock bound. Submission loop counts/sleeps are finite but each native call can wait indefinitely. Consequently neither current source nor naming component policy fields proves an aggregate warning deadline.

Exact current lock order is dispatch_gate → pane lease → durable Engine calls. Lower LeasedDelivery.run does not acquire the first two; its caller does. Settlement also holds dispatch_gate before close takes the pane lease. The below-threshold delta therefore still needs a concrete bounded admission/execution design, not a sum of sleeps. A timeout return must not leave a detached warning task capable of submitting later or holding lifecycle locks. A timed-out native call with possible effects must become Uncertain, not a clean retryable refusal.

This is a precise missing mechanism for Core judgment: the unchanged accepted transport budgets are configuration values, not evidence of aggregate cancellation across lock acquisition, subprocess and durable storage. Do not implement speculative cancellation or claim an aggregate bound before this gap is resolved. At/Past refresh remains unaffected and never enters this warning attempt.

## Controlling bounded warning attempt — no general locking/storage redesign

Core narrows the deadline obligation: no hard aggregate bound is claimed over inherited settlement/Engine work. At/Past skips warning. Below threshold, contention means no attempt; only a later NEW actual context receipt may retry. This section supersedes the earlier request to bound all Engine/lock waits.

Proposed configuration reuses the existing committed `Transport.HerdrCall : DurationMilliseconds` as the ONE captured native warning-attempt deadline, rather than introducing a third warning-policy value. Its meaning here is the total budget shared by all warning-owned native calls, not a fresh budget per subprocess. Core must judge that reuse explicitly; no Rust timeout default is supplied.

### Executable lock/cancellation boundary proposed

- The settlement caller already owns lifecycle dispatch serialization when it reaches warning eligibility; this is an inherited settlement wait, not a new warning wait. An entry point that does not own it uses try-acquire and skips on contention. A private borrowed admission token makes that ownership explicit; never recursively invoke public dispatch.
- Acquire the pane lease with a nonblocking try-acquire on the existing lease state. Held or contended returns `WarningAttempt::NotAttempted(Busy)` without waiting on Condvar or reserving the crossing latch. This is a narrow additional acquisition capability on the existing lease, not a new lock service.
- With both held, revalidate exact FlowId/native/route and current below-threshold policy snapshot. Reserve the in-process latch immediately before the first possible native effect. Complete required existing durable intent work under its actual Engine contract. Storage waits are inherited delivery-contract work and reported separately, not advertised as bounded by the native deadline.
- Start one monotonic deadline immediately before the first warning-owned subprocess spawn. A warning-local native runner owns each Child and its stdout/stderr handles. It shares the same absolute deadline across placement/submission/observation calls and any permitted sleeps. After expiry it starts NO further native command. It uses deadline-aware process/I/O waiting, not blocking `Command.output()` and not a detached timeout task.
- The runner owns a dedicated child process group so timeout cancellation targets only this attempt's command and any command children. On deadline it terminates that group, reaps its direct Child, closes its owned pipes, and returns possible-effect uncertainty if an effectful call had been entered. It cannot return a clean refusal based on timeout merely because no stdout arrived. Cancellation/reaping completion is a prerequisite to releasing the attempt's owned resources; no background worker remains capable of later submission. OS kill/reap behavior is a real platform contract, not a claim that arbitrary kernel scheduling is hard real-time.
- Reuse the lower route-bound placement/submission observations without the ordinary Past exception. Only observed submission earns `Submitted`; text merely remaining in a composer is not that outcome. A placed but unconfirmed warning is `Uncertain`, with the latch suppressed. Do not force an interrupt, replace user composer text, or perform post-deadline cleanup commands. Retain evidence so ordinary settlement does not mislabel residual composer text as a delivered warning.
- Record the truthful existing delivery outcome using existing Engine semantics, then release the pane lease and continue ordinary settlement. If post-effect persistence fails, return/log Uncertain and keep the transient latch suppressed. No new durable warning family or handover. No hard wall-clock promise over that persistence stage.

The private operation returns `WarningAttempt.[ NotAttempted.WarningPreEffect Submitted.WarningSubmission Uncertain.WarningUncertainty ]`; inner payloads carry witnessed existing native errors/observations, exact FlowId/native identity and phase. `WarningPreEffect` distinguishes Busy, changed identity/lifecycle, missing actual receipt/config and a known spawn refusal before effect. `WarningSubmission` identifies the observed same-session submission, never model consumption. `WarningUncertainty` identifies the entered effect phase plus timeout/native/observation/persistence failure. Exact existing payload reuse is checked before bodies; broad strings or fictitious launch IDs are not introduced.

Tests add contended dispatch/pane paths with zero native spawn, one absolute deadline across multiple native calls, blocked child output, child process-group cancellation and reap, no command after expiry, timeout before spawn versus after placement, residual composer text classified uncertain, post-effect persistence failure, and ordinary settlement continuation. No native test against production seats is authorized. The independent delta review must check actual native command wrappers support owned process groups and deadline-aware I/O without a new hidden polling default; substantive platform capability gaps return for judgment.
