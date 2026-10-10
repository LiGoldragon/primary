# Context visibility: current capability and self-query gap

## Proposed design

`harness-usage` is a sound one-call, owner-local inventory of the context
*observations it can obtain*.  It is not yet a reliable answer to “how full is
this Flow's live context?”, even when the Flow itself invokes it.  The proposed
missing piece is not another quota collector: it is an authoritative,
leased Flow-to-native-session binding plus a harness-specific live occupancy
source.

Do not label a token counter “context size” unless it describes the current
prompt occupying the model window.  A last request's input tokens, a
thread-cumulative token total, and a compaction count are different facts.

## What is working today

The deployed acceptance evidence covers Harness 0.6.1's `UsageSnapshotQuery`
and `harness-usage`: a daemon-scoped, fresh, read-only request that returns
subscription windows and context observations.  It is a one-shot query with
observation timestamps and typed unavailable results; it starts no model and
does not expose secrets.  That is the existing working surface, not a new
quota implementation.

The inspected source's context semantics are deliberately narrow:

| Harness | Observable value | Freshness and meaning | Capacity / exact live fill |
| --- | --- | --- | --- |
| Codex | `token_count.info.last_token_usage.input_tokens` from the bound rollout tail; `model_context_window` when recorded | `Proxy` until a later user message or compaction; then `Superseded` | Window is available when recorded, but `last input / window` is an estimate for the preceding request, never current occupancy. |
| Codex | `token_usage_record.thread_token_usage` | Thread cumulative accounting, timestamped in the rollout | Not a context-window reading and must not be divided by window capacity. |
| Claude | Last assistant request's `input + cache_creation + cache_read` in the transcript tail | `Proxy`; a later user event, compact boundary, or partial tail removes its value | Transcript supplies no window size or exact percentage. |
| Claude, only if a fresh structured status snapshot exists | `total_input_tokens`, `context_window_size`, used/remaining percentages | The field-census reference treats it as `Exact` only after matching the native session id and a five-minute freshness bound | The deployed Harness collector does not produce or consume this snapshot. Headless Claude was recorded as emitting no statusline. |

The contract already has `Exact`, `Proxy`, `Superseded`, and `Unknown`, but its
two present bases are only `ClaudeTranscriptLastRequest` and
`CodexRolloutLastTokenCount`.  The `Exact` variant is therefore vocabulary for
a future authoritative source, not evidence that either current collector is
exact.  The deployed review also establishes that neither a Claude session-id
prefix nor a Codex thread display name is a Flow binding; `FlowIdentifier` is
absent on every present observation.

This report has no receipt for a live query made by this Flow.  Per the flow
provenance boundary, the native thread id has not been handed over as a
readable receipt, so this investigation neither obtained nor reports it.

## The semantic boundary

An answer must carry all applicable times separately:

- `observed_at`: when the reader looked;
- `source_event_at`: when the harness produced the source value;
- `binding_observed_at` and lease expiry: when the Flow/session association
  was witnessed and when it stops being trusted;
- `compacted_at` / compaction sequence, when seen: an invalidation boundary;
- `last_request_usage`: request accounting, explicitly scoped to that
  response/request; and
- `occupancy`: current prompt tokens, window capacity, and derived share,
  only when one source says those are current.

A compaction count or the most recent compaction time says that prior prompt
state has changed.  It neither reconstructs the retained summary nor reports
the current prompt size.  Likewise, `thread_token_usage` may be valuable for
cost/history and `last_token_usage` for the preceding request, but neither is
live context usage.  On any later user message or compaction, a previous
occupancy value must become `Superseded`, never be carried forward as zero or
as a live percentage.

## Smallest sound next change

The smallest sound proposal is to extend the existing `UsageSnapshotQuery`
reply, without adding a polling service, ledger, dashboard, or universal
cross-harness promise.  The binding lifecycle below is a proposed shape; this
review did not establish the present launcher binding code well enough to call
it the only possible implementation.

1. At launch, the component that knows both values registers an owner-local,
   renewable binding: `(FlowIdentifier, provider, native_session_id,
   harness_instance, bound_at, lease_expiry)`.  The launcher, not a thread
   name, creates it; end, handoff, and successor creation retract or replace
   it.  A query returns `BindingAbsent`, `BindingExpired`, or
   `BindingMismatched` rather than guessing.
2. Add a focused `FlowContextQuery` (or an optional Flow selector on
   `UsageSnapshotQuery`) that resolves exactly one such binding and returns
   its `SessionContext` with those binding facts.  Keep the existing all-live
   inventory available for the screen/list use case.
3. Model a current runtime measurement and a last-request proxy as distinct
   facts.  Only the former may populate `current_tokens`, `window_tokens`,
   and `used_basis_points` as `Exact`; request accounting and cumulative
   accounting remain separately available because they answer different
   questions.  Update every affected consumer to the resulting contract.
4. Implement only adapters whose native control surface actually supplies a
   current measurement.  For Claude, this requires a safe, session-bound
   structured status export; the known headless transcript path is
   insufficient.  For Codex, the inspected control/rollout path establishes
   metadata and proxy accounting, not a current occupancy endpoint.  Until
   either provider supplies that measurement, return the bound proxy plus
   `ExactUnavailable`, not a fabricated exact count.

The binding record must contain no transcript text, prompts, credential
material, raw provider replies, environment, or process arguments.  Its
native session id remains owner-local; presentation may show the Flow id and
a non-secret stable session label.

## Focused implementation handoff

Start with contract tests, then adapters:

1. In `signal-harness`, model `FlowContextQuery`, binding status/lease facts,
   source event time, and a distinct exact-unavailable reason.  Define the
   complete resulting `ContextBasis`/`ContextFreshness` contract and update
   its consumers, with canonical cases for valid binding + exact observation,
   valid binding + proxy, expired binding, mismatch, and compaction after a
   reading.
2. In Harness, make the launch owner own the binding lifecycle and make the
   daemon resolve it before reading one adapter.  The existing source has a
   `flow_id.rs` identity module in its current dirty working copy, but this
   investigation did not establish it as deployed, wired to `UsageSnapshot`,
   or an authoritative native-session binding.  Do not treat it as completion.
3. Codex adapter tests must prove that `thread/read`'s id/path matches the
   registered native id, that a post-reading user/compaction marker supersedes
   the result, and that cumulative usage is never presented as occupancy.
   Claude tests must prove native-id match, status-snapshot freshness, and
   fallback to proxy/unavailable when the status export is absent or stale.
4. Ship a terse human view suitable for a screen: `Flow · provider/model ·
   exact|proxy|superseded|unavailable · used/window/share · source event ·
   observed`.  It must visibly state why an exact reading is unavailable.

This serves the requested individual-flow visibility first.  An aggregate
screen can call the established inventory and group only the records carrying
a valid Flow binding.  It should not infer Flow identity for the remaining
native sessions.

## External reference checked

Wheelhouse is verified: Yegge's August 2026 primary essay calls it his
closed-source, bespoke harness and shows its cockpit and a separate Castellan
dashboard.  The same source's dashboard caption names session and VM counters,
per-account burn telemetry, and attention/incident state; it does not claim a
per-flow provider-authoritative current-context occupancy meter.  The official
Gas Town repository documents an activity-feed/dashboard for agent, work, and
health state, and Yegge's official `gastown-otel` repository publishes a
Grafana/VictoriaMetrics/VictoriaLogs stack with per-API-request Claude input
and output token telemetry.  These sources support the feasibility of a
monitoring screen and timestamped per-request accounting.  They do **not**
support a cross-harness universal current-context promise.  The screen should
therefore consume the contract above, not invent its semantics.

## Psyche packet — verbatim, bounded to observation and self-query

These are the relevant user words, reproduced rather than paraphrased.  They
set the need and the intended delivery moment; they do not select the binding
or adapter design above.

> “Can we get context size on everything? How hard is that?”

> “That doesn't really answer my question. Can we make a single tool call that
> gets us the context size of every flow?”

— psyche, typed directly to Field Sol, 2026-09-25,
[`flows/b7da5d/vision/contextSize.md`](../../b7da5d/vision/contextSize.md).

> “Let's all keep track of the quotas and the burn rates, estimated burn
> rates. Do we even want a hook that automatically injects the context and the
> quotas into the periodic message that gets queued in the model, and that
> attaches itself into the next message with a timestamp?”

— psyche, artifact comment, 2026-09-18,
[`flows/b05237/vision/operational-quotaBurnRateHook.md`](../../b05237/vision/operational-quotaBurnRateHook.md).

> “When a model reaches a certain context window, whoever is in charge of
> refreshing should get a message that some flow needs to be refreshed. I
> guess the flow itself needs to know so that it can create a handover
> response.”

— psyche, typed direct user turn, 2026-09-26,
[`flows/b860be/vision/refreshAutomation.md`](../../b860be/vision/refreshAutomation.md).

> “There's Steve Yeggy: he has his own wheelhouse and he has a screen where he
> can see the context and the usage of everything.”

— psyche, typed, 2026-10-04,
[`flows/d66c26/vision/context-visibility.md`](../vision/context-visibility.md).

> “We can use that opportunity to inject a bunch of other stuff that has been
> queued in preparation for that particular flow to be woken up, so that it
> would know all of this as soon as it woke up. Yet we wouldn't have to wake up
> every time some accumulation of vision or whatever that touches its lanes or
> its topics is coming into the system.”

— psyche, typed, 2026-10-04,
[`flows/d66c26/vision/flow-context-injection.md`](../vision/flow-context-injection.md).

## Evidence

- [quota acceptance review](quota-acceptance-review.md) — reported activation
  of 0.6.1/`UsageSnapshotQuery` and its stated limits.
- [`harness` usage architecture](/git/github.com/LiGoldragon/harness/ARCHITECTURE.md)
  and [`signal-harness` contract architecture](/git/github.com/LiGoldragon/signal-harness/ARCHITECTURE.md)
  — one-shot scope, current bases, freshness, unbound Flow identity.
- [`codex_context.rs`](/git/github.com/LiGoldragon/harness/src/usage/codex_context.rs)
  and [`claude_context.rs`](/git/github.com/LiGoldragon/harness/src/usage/claude_context.rs)
  — source behavior and invalidation logic inspected 2026-10-04.
- [`codex-context.mjs`](../../../tools/field-census/codex-context.mjs) and
  [`claude-context.mjs`](../../../tools/field-census/claude-context.mjs) —
  bounded reference readers, including the optional Claude status snapshot.
- [Steve Yegge, “The Shape of Things to Come”](https://yegge.ai/essays/the-shape-of-things-to-come/),
  [Gas Town official repository](https://github.com/gastownhall/gastown), and
  [Steve Yegge’s official Gas Town OpenTelemetry repository](https://github.com/steveyegge/gastown-otel)
  — primary external sources checked 2026-10-04.
- [psyche request](../vision/context-visibility.md),
  [context-size question](../../b7da5d/vision/contextSize.md), and
  [refresh-hook direction](../../b860be/vision/refreshAutomation.md) — the
  requested visibility and its later use for a threshold-triggered handoff.
