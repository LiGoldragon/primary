# Context-usage Nexus integration contract

**Date:** 2026-09-21  
**Owner:** Mind Astra4b0f60 owns cross-contract architecture, schema semantics, and this SEMA record specification. Field Astra6db4fe, with Terra research workers, owns the collector witnesses and tests.  
**Status:** a Primary architecture report, not a compiled, deployed, or installed contract. Proposed names and types are abstract semantics, not runnable Datom grammar or an ABI.

The prior statement that “Field Terra6db4fe owns collector research/testing” was an inference from an initial prompt and is corrected by current living authority: 6db4fe is the Field Astra parent; Terra workers share its Flow ID and perform research/testing. This correction does not rewrite the original living words.

## Ownership and target boundary

The target is shared typed native-observation records in `signal-harness`, with authored schema extensions and coherent updates to actual consumers. Mind owns this query/response/process/SEMA specification; Field owns observation runtime implementation and deployment. Existing repository writers retain their scopes. Canonical Field, `signal-field`, checkup, and `signal-checkup` repositories were not found in the bounded source probe, so these are future implementation homes. Flow remains exact logical/native identity authority. Message is not a metric store. Existing schema-language/ethos generation pipelines remain authoritative: do not edit generated Rust or hand-construct engine descriptors. Field's short-term Codex `--overview` is a read-only snapshot consumer, never a substitute for a live Watch.

This report does not take retained writer paths: preserve f72ab7 Flow/signal-flow/Message reservations and Field6db4fe collector locks 3559/3560. The inspected roots are source anchors only: Nexus `c495f2a`, Signal `66e7b15`, signal-frame `000d866`, signal-harness `17bdd58`, Flow `61d765e`, signal-flow `968ae3b`, Message `55657f4` (origin/main `9330640`), and signal-message `37c3e5b` (origin/main `7f2fc2d`). They do not establish installed parity.

## Witness-grounded source matrix

| Harness and source | Witnessed/attributed observation | Limit that the contract preserves |
|---|---|---|
| Codex CLI/appserver 0.153.4 | Exact `thread/read(includeTurns:false)` validates ID and canonical path without resuming/subscribing; bounded rollout tail is 1 MiB default/2 MiB cap. `token_usage_record` supplies response/turn/thread emitted counts; `token_count` supplies a source window and quota/fallback counters. | `thread/read` has no usage field. It neither resumes nor subscribes. A local rollout record is not a stable public response contract. |
| Codex occupancy and quota | Latest response `input_tokens` is `LastInputProxy`; cached input is a subset of input and reasoning output a subset of output, so neither is double-counted. Account quota is source-scoped and can stale independently. | Exact resident occupancy/remaining tokens are unknown. Emitted thread total is an invalid interpretation of current context and must never serve as one. Account read/update interfaces were documentation/schema reviewed, never live invoked here. Cache-write relationships are only those witnessed. |
| Claude Code 2.1.263 | Passive 512 KiB transcript tail gives last-request uncached/cache-create/cache-read input proxy. Exact-session statusline JSON can provide source-reported context percent/window and account quota. | Transcript has no full window, exact percent, or quota. Prompt, compaction, summary, or incomplete records invalidate occupancy. Prepared statusline wrapper is not installed; prior stdin values cannot be recovered. |
| Claude statusline | A native statusline feed can update relevant events/resets. Its five-minute freshness is collector policy, not vendor TTL; retain last known value, time, and `Stale`. | Rounded percentages never certify resident tokens; quota can disappear after reset. Do not add a polling/timer fallback or settings change merely to fill columns. |

The 18 ms Codex and 1–3 ms Claude figures are individual samples, not freshness promises or SLAs. Reported tests are two Codex and six Claude fixture/Node tests; bounded live reads are separate witnesses. Neither is a Nexus runtime Watch or SEMA pass. Claude's first failed fixture depended on `/bin/cat` on this Nix host; it is not a claim that native behavior first failed. No Claude cumulative turn/session total is witnessed from last-request usage: it remains unknown pending a separate witness, not globally unsupported. Null/missing is never zero. Codex `contextCompaction` is documentation evidence only; no live compaction/reset was tested. The documented future Codex usage notification is active-traffic oriented; no cold dedicated read/subscription has been established.

## Typed semantic model

```text
ContextUsageView{flow: FlowRef, harness: HarnessKind, native_session: NativeSessionId,
                 binding: RuntimeBindingRef}
Epochs{flow_lifecycle, process_incarnation, binding_generation, context,
       usage_series, counter_reset_epoch, source_stream}

Metric<T> = Observed{value, precision_or_definition, unit, scope, source_ref,
                     event_time?, observed_time, received_time, freshness, source_cursor?}
          | Unknown{reason} | Unavailable{cause} | Unsupported{source_capability}
          | Stale{last_value, last_times, cause} | Conflict{candidate_refs}
```

None of the epochs substitutes for another or defaults unknown to zero. Compaction may advance `ContextEpoch` without a Flow lifecycle change, but only on witnessed events; an invented serial is not authority. Each envelope and each metric can be partial.

Store separately: context occupancy (`LastInputProxy`, `SourceReportedPercentage`, or explicitly witnessed `ResidentTokens`); window capacity and basis; remaining (`SourceReported`, compatible `DerivedEstimate`, or unknown); response/turn/session emitted usage; cache breakdown and its subset relations; account/model-bucket quota with reset/rate limit; lifecycle/task/activity; and independently sourced availability. Idle never proves availability and task-start does not prove responsiveness; the 303-second queue witness is a boundary, not a hard timeout. Source version/method distinguishes documented API from local persisted format.

An exact source counter is exact only within its reported metric basis, never automatically billing or current residency. Derive remaining only from compatible token basis, model, context epoch, source window, and occupancy observations; store inputs and rule version. A mismatched/stale window after model change becomes `Unknown` or `Conflict`, never a clamped false value. Raw values and derived facts stay distinct. An account quota is attached by scope reference, not copied into Flow-owned quota; a Flow observation cannot refresh its timestamp.

Metric precision is therefore a required response property, not display decoration. `LastInputProxy` answers what the last completed request reported; it cannot answer an in-flight turn or certify the current resident prompt. `SourceReportedPercentage` remains the source's declared percentage and rounding basis, even where a UI displays it differently. `ResidentTokens` is legal only when a source actually declares current resident tokens for the exact binding and context epoch. A `DerivedEstimate` retains all operand observation references and becomes stale when any required operand does. Response, turn, and session counters describe emitted usage under their own source definitions; no response converts them into a single “context used” field. This lets a consumer choose whether it can tolerate a proxy without silently changing the claim made by the stored observation.

## Snapshot, Watch, and process contract

```text
SnapshotUsage{resolved_selection, metric_groups, freshness_requirement}
  -> UsageSnapshot{binding, evidence_window, per_metric_states,
                   source_capabilities, snapshot_cursor, limitations}
  | Rejected{reason} | IdentityConflict{references}

WatchUsage{resolved_selection, metric_groups, resume_cursor?}
  -> bounded ObservationProcess + initial snapshot/cursor + ordered deltas
```

`WatchUsage` is an observation process, not a model turn, native resume, or an OS-process identity. Flow resolves authoritative identity and cross-checks native events. If public `FlowNode` lacks a lifecycle generation, return explicit `Unknown`/prospective integration rather than fabricating one. Proposed events are `SourceObserved`, `MetricChanged`, `SourceUnavailable`, `ContextInvalidated`, `CounterSeriesReset`, `BindingChanged`, `StaleTransition`, `ConflictObserved`, `ConflictResolved`, `ReplayGap`, and `ResetRequired`. A private source sequence, durable SEMA `CommitSequence`, and `SnapshotIdentifier` are different values.

Process order is: resolve exact identity; establish native event watch plus buffer/snapshot high-watermark where supported; perform bounded cold one-shot read; publish initial snapshot; consume native events; normalize and commit; publish deltas. If a race-free watch/snapshot cannot be established, return `SnapshotOnly`/`ContinuityUnproven`. Cold reads happen on open or explicit recovery, not an interval loop. Codex `thread/read` creates no watch; a future active appserver owner must witness attachment and ordering without resuming the thread. Claude needs a separately scoped installed statusline publisher that preserves original display input and projects metadata only; otherwise it returns `SourceNotConfigured`. A file-event adapter is allowed only after testing rename, partial-tail, and gap behavior, never by interval tail polling. Freshness expiry emits a single stale transition without advancing timestamps. Quota is an independent shared-scope stream. Shutdown detaches observation only; it never kills a native Flow. Compaction invalidates a proxy until fresh usage arrives.

Use existing shared Signal/frame mechanics after compatibility verification, not untyped JSON maps, prose, or raw transcript wire payloads. The native JSON collector edge normalizes into a compiled pure-binary internal signal. Backpressure/reconnect must produce bounded `ReplayGap` rather than silently treating latest as continuity.

## Current SEMA record specification

Sema remains the typed storage kernel, not a home for usage policy or records. `sema-engine` is the exclusive component database interface: it owns catalog/schema identity, commit sequence, snapshots, subscriptions, and engine operation logging. Components use authored record families and `schema/sema.schema` through generation, not custom redb, a component commit ledger, or internal `Assert`/`Mutate` roots on the public wire.

The proposed logical family is `HarnessUsageObservationBundle`, containing identity references; independent epochs; source provenance and native-event cursor; field observations; derivation references; source capability/freshness data; and applicability. Correlation/latest view and history are engine projections retaining originals and conflicts. A stable source-observation key/replay dedup follows the generated key specification. If an event has no ID, do not assume filename/mtime uniqueness: a normalized fingerprint plus collector stream/cursor needs its own witness. The component does not invent successor storage identity or direct table keys.

Current engine evidence constrains the design. `Engine::commit`'s witnessed atomic unit is a nonempty `WriteOperation` bundle for one registered table; this contract does not promise a cross-family transaction. Keep source cursor, observation, and publish correlation in one supported record/commit bundle; derive the latest projection rather than commit a second ledger. Publish notifications after engine commit and replay through engine cursors. Startup derives state from source-backed records without silently resetting counters. Where configured, a versioned log is authoritative; remote durability/mirror activation is not claimed.

The current semantic gap is explicit: `sema.schema` document kind is settled, but entry/index/projection syntax and successor stored-record identity are reserved/undesigned in the inspected engine architecture. Per-family schema hashes exist; a retired-family declaration is not revived. Thus this report specifies fields and key constraints, never invented schema syntax/catalog migration. Evolution requires an engine-owned migration and coordinated consumer preservation; no destructive database reset is a shortcut.

## `--overview`, evidence gates, and rollout

`--overview` may show native ID/binding verification; separate metric groups; the `LastInputProxy`/estimate label; source/event age and stale state; unknown/null as unknown; explicitly account-scoped quota; separate emitted response/turn/session totals; and availability only when independently evidenced. It must not imply subscription from a read, equate 18 ms with fresh context, or trigger compaction, wake, or lifecycle action from a proxy. It follows the requested read-only scope and adds no statusline configuration.

Initial work is typed record/query/event fixture design, subject to observed source versions. Before a native process/storage claim, prove: live Codex token-use plus compaction/reset and attachment ownership; installed Claude exact-session feed, event health/pass-through, reset/missing fields; ordering/replay/late events; model/window proxy mismatch; process/native binding-generation joins; quota scope/reset and actually invoked subscriptions; SEMA registration, atomicity, recovery, and commit-before-notification; and snapshot/delta race, restart, out-of-order, and conflict handling. Use Nix behavioral tests with real machinery/fixtures, bounded inputs, deterministic virtual time, and no sleeps/text greps. Current status is bounded collector fixtures/live reads only. This artifact deploys neither a Nexus process, record schema, Watch, nor storage.

## Sources

- **Committed Field witnesses:** `flows/6db4fe/reports/codex-context-usage.md`, commit `bcc203eaf1ba6399dbc9e961624fae5c25e5a120`, content SHA-256 `94442afc35b2636ee4203aa0163786f71b79b314cfc6aa8a84c6a8f81aacc120`; and `claude-context-usage.md`, commit `48857de319efa9590dc67456107668675dc50a3d`, content SHA-256 `664e8f51f386dcf46be75fa4df753946698bda019e1da50a8c85aff62df998e7`. Vendor capabilities in these reports are attributed documentation/schema review unless their reports label them live tests; no remote documentation browsing was performed here.
- **Living authority:** `HM_CTX_USAGE_6DB4FE_20260921`, including the Field Astra parent/Terra-worker correction and the current ownership boundary.
- **Inspected source specifications:** `sema/ARCHITECTURE.md` at `4fdc612`; `sema-engine/ARCHITECTURE.md` at `516f01f`; source-root/probe map returned by `/root/census_contract_design`. These are source anchors, not deployment claims.
- **Existing contract:** `flows/4b0f60/reports/field-census-and-checkup-architecture.md` at `e066bd045` for identity/evidence boundary only. Retained reservations/locks are time-bounded reported ownership, not global claims.
