# Field census and Mind checkup — architecture contract

**Date:** 2026-09-20  
**Owner:** Mind4b0f60. **Implementation and deployment:** Field. **Lifecycle sequencing:** Field Low2fe3f1.  
**Status:** implementation contract published at the living/Field request. The names and types below are proposed implementation work, not an observed wire schema, running service, or runtime-readiness claim. The Field/Mind/Flow/Message boundary was accepted in the conversation.

Field has reported a read-only collector on main `a63e08b0d`, remotely verified by Field, with an 85 ms pass across 19 panes and 17 agents. Six older HM rows retain `provenance_gap`; their evidence includes source timestamps, errors, and exact routes, but neither contents nor mutations. This report attributes those observations to Field; it does not independently assert current runtime state or an exact full SHA. A historical approximately-five-second/15-agent report differs in time and scope, so neither result establishes a cycle guarantee.

## Ownership and implementation boundary

| Domain | Owner and boundary |
|---|---|
| Field Nexus | Observes host, panes, services, and resources; owns census observations and cache. It is read-only evidence collection. |
| Flow | Resolves logical identity, native binding, and lifecycle. HM is transitional only. |
| Message | Owns durable requests, attempts, and receipt grades. Its receipt remains the delivery record of authority. |
| Orchestrate | Remains ownership and lock authority. |
| checkup-nexus | Owns desired-duty policy, reconciliation, wake episodes, and status aggregation. It is a Mind-owned Nexus capability, not a thirteenth model role. |

Field implements, packages, and deploys; Mind owns semantics; Psyche approves intent and priority. The proposed main-repository line is `checkup` (binary `checkup-nexus`) with `signal-checkup` and `meta-signal-checkup`, following existing Nexus core conventions: a compiled binary, typed signals on ordinary/meta sockets, typed Sema durability, and meta configuration. These names are not observed files. Duty or wake policy must not enter `tools/field-census.mjs` or Field observation storage. The collector remains a bootstrap adapter to future `field` / `signal-field` / `meta-signal-field`. There is no competing Flow/Message identity or delivery store: a checkup local outbox/episode is intent and correlation, while Message is authoritative for delivery receipts.

## Census design types

This is abstract design algebra, **not** Datom syntax or an implemented Rust ABI.

```text
FieldQuery = Census{scope, detail: Baseline | Diagnostics, freshness, page}
           | SubscribeCensus{scope, after: Optional<CensusCursor>}
           | SeatDiagnostics{expected: SeatBindingRef, selection}
           | TranscriptMetadata{binding: SeatBindingRef}

FieldAnswer = Rejected{reason} | CensusSnapshot{snapshot_id, collection_window,
              source_results, seats, host_health, completeness, next_page}
            | SeatDiagnosticsReport{binding, observations}
            | TranscriptMetadataReport{binding, availability, freshness, size, ref, provenance}
            | SubscriptionOpened{snapshot, cursor}
CensusEvent = Snapshot | SeatChanged | SourceDegraded | CursorInvalidated

Observation<T> = Value{value, provenance, observed_at, source_time?, source_epoch}
               | Stale{last_value, last_observed_at, cause}
               | Unavailable{cause} | Unsupported | Conflict{references}

Aspect = Mind | Field | Psyche
Power = High | Medium | Low | UltraLow
CellKey{aspect: Aspect, power: Power}
HarnessHealth = Operational | Unavailable | Unknown
StructuralReport{policy_revision, scope, snapshot_ref, expected_cells,
                 cell_observations, gaps, ghosts, harness_findings,
                 assignment_findings, completeness}
Ghost{binding, cause, protection, disposition}
```

Measured `Absent` is scoped evidence; it is never the default for a missing row or error. There is no global atomic-snapshot claim: each probe retains its collection window. Pages are pinned to a snapshot. Cursors are opaque, carry source/producer epoch and bounded replay, and invalidate to require a fresh snapshot rather than invent continuity. Ordinary subscriptions provide initial state then deltas; baseline does not carry terminal or transcript bodies.

A `SeatObservation` separates declared role/aspect and owning flow; native harness/thread; registered and observed Herdr tuple; an optional independently joined process PID/start/boot identity; activity, responsiveness, readiness, quota/context observations, locks, and transcript metadata. Incomplete or conflicting native/process/Herdr joins stay typed. A session+pane+terminal+name+harness match without `native_thread` is retained as `provenance_gap`, for diagnosis only and ineligible for wake. Unknown role is `Unassigned`; raw unjoined seats remain visible. Flow lifecycle/generation, native/restart generation, persisted delivery-binding generation, and census sequence are distinct. UI titles/status, file presence, and registry rows are hints, not identity or activity proof. Context percentage requires its source and denominator; unavailable native counters cannot authorize refresh. Process pins are not presumed part of Flow's public contract.

## Twelve-pane structural and harness invariant

This is a direct latest living design constraint for checkup, not an observation of current census totals. A declared cluster census scope has an expected Cartesian grid `Aspect{Mind, Field, Psyche} × Power{High, Medium, Low, UltraLow}`: exactly one main pane per `CellKey`, with a matching declared role/profile. Twelve total is insufficient. Use authoritative unique designated matching between expected cells and observed panes, never `max(0, panes-12)`: gaps are unmatched expected cells and ghosts are unmatched observed panes, including surplus duplicates and unassigned panes even when fewer than twelve panes exist. Ambiguous duplicate assignment remains `Conflict` until authority designates its occupant. Historical and crossover panes are never silently excluded to pass a count.

Count distinct currently observed physical session/pane/terminal instances within the declared cluster scope, retaining instance identity and collection window; do not count HM registrations, transcripts, or per-flow census joins. Multiple or stale HM records for one pane yield identity/provenance findings, not extra physical ghosts; an HM row without an observed pane is a stale registration, not an observed extra pane. Each cell records harness health separately as `Operational | Unavailable | Unknown`, with exact native/process/Herdr evidence. Operational means functioning, not continuously executing work: a verified healthy idle harness satisfies the requirement. Pane presence or UI status does not prove operational health. A present pane with absent or broken harness is `HarnessUnavailable`, not a passing occupied cell; ambiguous identity or observability is `Unverified`, never proven absence. A pending liveness probe, native request, or known queue delay, including the observed 303-second pattern, remains an activity/pending finding and is neither failed/dead proof nor fresh operational verification; it authorizes neither a duplicate launch nor reaping. Only twelve correctly bound, appropriately assigned cells with operational harnesses pass the structural-and-health invariant. If two known panes map to one cell, the report records an explicit duplicate-map conflict and requires authoritative assignment to select a designated occupant; it never guesses from a name.

Assignments are proportional structurally: each aspect has one seat at each power, with declared model/effort and scope/tier responsibility taken from the current authoritative role declaration, not historic hard-coded models; task delegation respects existing power ceilings. This contract supplies no numeric compute, work, task-weight, or ratio quota. Any unresolved task-weight/ratio definition is reported separately from structural compliance. `StructuralReport` includes exact gap/ghost cell or binding, evidence time, health/pending state, protection, current owner, and disposition. Missing declared scope/policy yields `Inconclusive`, not an arbitrary threshold.

All extras are ghosts, including protected retained crossover or writer extras. Their retention/protection/owner evidence and disposition are attached, without treating them as legitimate expected cells or inferring removal permission. A protected ghost makes the literal twelve-pane invariant `Nonconforming`; there is no pass-with-excluded-crossovers state. That finding can coexist with a valid authorized status-review wake for a verified existing UL when the duty gate permits it, but it never marks the full structure passed. Preserve the recorded 9e7ea5/98ac2e/0ab019 routes/writers and b81560 no-resume boundary. Ghost diagnosis alone never releases locks, reaps, retires routes, kills sessions, resumes a closed native, or assigns a new model. Field lifecycle handles authorized remediation one at a time. The historical Field coverage of 3/4, 3/4, and 2/4 is only a receipt; it does not establish a current ghost count from a stale 19-pane scan. Read-only census introduces no fresh model prompts or health mutations: operational/liveness findings retain their observed evidence grade.

## Transcript boundary

The recommended design is a separate canonical transcript domain/interface with a Field adapter, rather than census-owned transcript storage. Flow selects logical/native identity; the harness adapter associates a stable `TranscriptRef` (not immutable bytes of a growing native file) with a harness and native thread, with evidence. Field returns availability, freshness, size, reference, and provenance under a separate budget. Mind and Psyche consume bounded content/search:

```text
ReadRange{ref, cursor, max_bytes, event_filter}
  -> native event/line locators, observed length/window, next cursor,
     PartialTail | Rotation | Truncation | CursorInvalid
```

No repeated full scan or transcript-body copy belongs in census; arbitrary paths are not accepted as identity. The existing Claude-only transcript CLI and `signal-harness` transcript types are evidence, not a running cross-harness Transcript Nexus. An adapter may exist now without transferring canonical ownership through physical co-location. A later merger needs an explicit identity, retention, and subscription contract; the September 20 raw record left split/merge open, and this is the recommended implementation resolution.

## Desired work, pending state, and classification

```text
DutyGrant{duty_id, aspect: Mind | Field | Psyche, authority_ref, revision,
          effective_window, mode: ReviewDue | WorkDue | PermittedIdle | Paused | Held,
          work_refs, priority_ref, completion_condition}
```

A review may be a standing authorized health/status assessment, allowing UL to discover what matters without a pre-existing task. Observed idleness cannot create a duty. Policy changes need an authorized meta contract with issuer, provenance, and revision; an unrestricted caller cannot manufacture authority. Each due recurrence has its own `DutyOccurrenceId`, never a reused closed episode. Expired, missing, or conflicting policy yields `DutyUnknown` or no action as appropriate, with uncertainty reported. Checkup evaluates all three aspects and the declared seat tree, including delegated work retained through crossover parents; a dead parent never implies its children completed. Priority comes only from authorized work/policy; UL assesses meaning and census never ranks terminal text.

Keep activity, responsiveness, and readiness distinct:

```text
Activity = Executing | NativeQueued | AwaitingTool | WaitingOnDelegatedWork
         | BlockedExternal | Idle | Closed | Unknown
```

Each classification is tied to source event/request/binding and time. Executing, NativeQueued, AwaitingTool, active delegated work, or an outstanding wake suppresses a duplicate wake. `BlockedExternal` preserves original work and can justify one due status review; it does not rerun the job. Field reported Terrae798f3/Luna23d977 liveness replies around 22:32 UTC after roughly 303 seconds task-started-to-first-token. That is queue/response-latency evidence, not separately measured network/startup timing, and proves silence alone is insufficient. A fresh all-idle conclusion needs complete coverage of the authoritative current aspect roster and its owned task/delegation subtree. A relevant gap, stale observation, or unavailable source yields `Inconclusive`, never “no workers.” Unrelated retained/provenance-gap historical rows remain diagnostics and cannot block verified aspects forever. `Paused`, `Held`, and `PermittedIdle` without a due review are `HealthyIdle`. Native activity without a request identifier is evidence, not an exact wake acknowledgement.

## Wake contract

`WakeEligible` requires all of: a valid due duty/review occurrence; a complete fresh authoritative-roster census establishing no active, queued, in-flight, or delegated worker; no outstanding episode for that occurrence; an exact current nonclosed UL target resolved by Flow; and configured delivery/lifecycle permission. A consumer of the Field latest snapshot validates schema/version, source freshness, and a complete atomic producer snapshot (atomic replacement or equivalent); a parse failure, truncation, stale file, or mere path existence is `Inconclusive` and cannot wake. Structural gaps and ghosts are evidence/status findings routed to Field lifecycle, never a new wake launch. An unrelated protected extra does not block a valid existing UL status assessment forever unless the relevant aspect's identity or completeness is unresolved; structural nonconformance alone does not negate a permitted wake, whose existing duty gate still controls an authorized UL status review. If UL is missing, emit `RecoveryRequired` to Field lifecycle. Census/checkup does not launch it. No current policy or census is `Inconclusive`.

Before delivery, atomically persist outbox and:

```text
WakeEpisode{episode_id, aspect, duty_occurrence, duty_revision, decision_snapshot,
            target_binding, request_id, state, receipt_refs, status_report_ref}
```

Atomic indexes enforce one active wake slot per aspect and idempotency by `(aspect, duty_occurrence)`: racing creation is rejected, and additional due duties coalesce into the active episode or queue until it closes. A new duty revision cannot release an `Unconfirmed` slot that was already submitted. Reconcile policy, current work, and exact Flow binding immediately before send. Message receives a stable request id and the typed `WakeStatusRequest{episode_id, aspect, duty_ref, snapshot_ref, important_work_refs, requested_report, expected_binding}` through its owned implementation, never a parallel HM auto-sender.

`EpisodeState = Recorded | DispatchPending | AwaitingReport | Reported | Closed | Cancelled | Unconfirmed`. Delivery attempt receipt grade is a separate witnessed field, and `WakeAccepted`, `WakeRefused`, and `Superseded` are separate application outcomes. Uncertain send/restart makes the episode `Unconfirmed`; late acknowledgement correlates episode, request, exact binding, and delivery generation. The target returns `WakeAccepted` or `WakeRefused`, then `AspectStatusReport`; generic activity or terminal writes are not an acknowledgement. Delivery never proves completion.

A report closes its episode even if it discovers follow-on work, which requires a newly assigned owner/occurrence. Crash recovery resumes the same request and episode. Retry that request only with established end-to-end idempotent acceptance; otherwise reconcile unknown attempts. A new attempt needs definitive non-delivery plus policy authorization, or a safe acknowledged binding transition under Flow/Message contract. Timeout, cooldown/backoff expiry, empty screen, and process disappearance do not establish non-delivery. Bound retries and escalate `Unconfirmed`. Cancellation, pause, or revision invalidates unsent intent; a delivered stale request is revalidated at the receiver and returns `Superseded`. No exactly-once claim exists without consumer idempotence, outbox, restart, and ABA witnesses.

## UL reports, lifecycle, and cadence

UL receives a short attributed evidence/status bundle: due reason, top authorized obligations, active/pending/delegated work, blockers, relevant resource/route issues, unknowns/freshness, exact report/request reference, and superior. Census or transcript excerpts are evidence only: they inject neither policy, skill, nor authority; `DutyGrant` alone authorizes. It returns:

```text
AspectStatusReport{episode, observations, important_work, blocked_or_pending,
                   next_action, owner, escalation, refresh_need}
```

UL notifies its superior through Message or requests its own refresh through authorized lifecycle; it never replaces itself. The aggregator combines the latest three aspect reports with per-aspect time, completeness, and pending state for higher-echelon review; missing stays missing. Event/due reporting avoids repeated full prompts on unchanged scans. The existing twelve-fold seat structure performs the assessment, with no extra persistent thinking role. Parent/role contacts resolve at send time. Preserve owner4b0f60, crossover9e7ea5/98ac2e/0ab019, and retained f72ab7/6ef34b handles with0ab019; b81560 is closed/no-resume and HM cleanup is not inferred. Generalize through explicit lifecycle declarations rather than historical IDs.

September 20 explicitly requests bootstrap periodic census. Field now attributes main `f5de6bd73` as remote verified: the user `field-census.timer` is active every five minutes, its first service run succeeded, and it writes `/home/li/.local/state/field-census/latest.json`; bounded HM summaries were submitted to Field Low0347d0 and Ultra c88918, with 30-minute notifications and a fail-closed uncertain-send hold. Those recipients are current notification recipients, not a lifecycle-authority transfer from Low2fe3f1. Field reports no wake or lifecycle mutation. The existing user `core-heartbeat.timer` is every five minutes and `core-checkup.timer` every 30 minutes, monitoring only; `/home/li/.config/core-checkup/policy.json` has `wake.enabled=false`, static old harness targets, and a service pinned to immutable `/nix/store/.../tools/core-checkup.mjs`. These are Field receipts, not root live verification, source-parity, or exact store-hash claims. Field will neither edit the store nor enable/duplicate it. Existing core-checkup is a predecessor/bootstrap of the desired capability. Heartbeat observes supervisor/service health, while checkup handles aspect duty; overlapping probes consolidate into shared census snapshots. Static targets never qualify for wake: Flow resolution, provenance, and explicit current duty are required.

Preserve the deployed 5-minute Field census and heartbeat schedules, the 30-minute core-checkup schedule, and disabled wake during implementation; a configurable 120-second pass is future tuning only, with no new timer here. A bounded shadow evaluator may consume the same census alongside existing monitoring for comparison, but must not actuate. Migrate authored units/package/policy into the Mind-owned `checkup-nexus` domain and deliberately cut over one durable wake owner/scheduler at a time, reconciling the pending ledger; disable old actuation before scoped activation and retire only the replaced bootstrap path deliberately. Do not duplicate actuation policy/senders or retire unrelated timers/seats. The future target is subscription-driven initial snapshot+deltas, with native changes where available. This reconciles Vision’s anti-polling rule with the newer bootstrap exception. Keep collection cadence, freshness budget, acknowledgement deadline, pending-age alert, and escalation deadline separate. Five seconds, 85 ms, and 303 seconds are observations, not periods or SLAs. A threshold triggers diagnosis, never duplicate wake. At most one collection cycle runs at once, with bounded per-source/global deadlines, skipped/coalesced missed ticks, partial results, no catch-up flood, and no additional periodic sender introduced by this contract. Supervisor health, degraded state, and last heartbeat stay externally visible. A missing all-seat system returns independent Field lifecycle `RecoveryRequired`/manual dependency until typed desired-seat recovery exists; uncertainty never becomes reaping.

Source-limited reuse boundary: historical isolated primary snapshots contain `tools/core-checkup.mjs`, `docs/core-checkup.md`, and `systemd/user/core-checkup.{service,timer}`, but lack usable Git metadata and do not establish deployed parity. Their `core-checkup/v1` NDJSON and `state.failed` per-unit repair suppression are neither a duty/pending ledger nor generic receipt/idempotency mechanism; the state write is nonatomic and has no explicit flock. Its injected wake callback reports only `accepted|undelivered` and remains a no-op while wake is disabled. Separate historical `heartbeat.mjs`/`heartbeat-luna.mjs` has atomic temp+rename, flock, and per-recipient `pending|accepted|transcript_witnessed` event-hash receipts, but these are heartbeat-specific delivery records, not Message-grade evidence or a general duty schema. Do not reuse either failure flag or heartbeat receipt as checkup wake dedup. Field carries existing events as attributed observations with source/time/staleness, preserves the no-text/no-raw-output boundary, and defines its own atomic cursor/idempotency. Current CriomOS-home lacks those core-checkup sources; its distinct `field-luna-heartbeat` module is unrelated. Active endpoint and owned-unit configuration remain OS/Horizon-projected.

## Tests, rollout, and handoff

Field may implement/deploy read-only and shadow mode. Add schema adapters and source-failure tests; then shadow decisions, persisted intent with dispatch disabled, isolated disposable-recipient proof, and configured duty/aspect scopes only after exact binding, typed acknowledgement, and report acceptance. Meaningful Nix checks use synthetic event streams and deterministic time, not sleeps/text greps: partial source/six missing native rows; same-name native/process reuse and ABA; concurrent single episode; crash before/after Message acceptance; lost reply/corrupt storage fail closed; duplicate/late/stale/superseded acknowledgement and receiver idempotence; 303-second queue; dormant/pause/held/closed/unknown; delegated suppression; blocked work; policy expiry/clock change; cursor and growing-transcript recovery; missing UL lifecycle-only; and partial three-aspect aggregation. Structural tests cover exactly twelve valid cells; twelve total with duplicate-plus-missing; four gaps plus one ghost from eight designated cells and one extra pane; a missing cell; an extra unassigned pane; protected crossover extra as nonconforming ghost/no action; correct pane with unavailable harness; wrong profile/role; unknown native; 303-second pending without duplicate/reap; incomplete census as inconclusive; no invented numerical proportion; and duplicate/stale HM rows for one physical pane that do not inflate the count. New tests must fail before they pass. Durable hold/reattach/binding generations and idempotent Message acceptance are inherited unproven work and cannot be bypassed by a timer or HM sender. No daemon/deployment success follows from source alone.

Next Field deliverables, under scoped reservations, are `signal-field`/meta plus collector adapter; `checkup`/signals with shadow reconciliation and persistent outbox; owned Flow/Message integration with retained writers; Nix checks and isolated proof; then configured dark runtime followed by scoped acceptance. Mind reviews semantic deviations; Psyche intent approval remains. This architecture authorizes implementation planning and bounded shadow/read-only delivery work, not autonomous activation.

## Sources

- **Current conversation and Field receipts:** living tasks and Field acceptance/publication request; attributed collector main `a63e08b0d` remote/pass metrics; native queue liveness and ownership receipts; main `f5de6bd73` remote-verified Field census timer (5 min), first successful service run, `latest.json` output, bounded Low0347d0/Ultra c88918 notifications (30 min) with fail-closed uncertain-send hold and no wake/lifecycle mutations; current `core-heartbeat.timer` (5 min), `core-checkup.timer` (30 min), disabled `/home/li/.config/core-checkup/policy.json`, static old targets, and immutable store-pinned `core-checkup.mjs`. These are attributed observations, not root live verification or source-parity claims.
- **Latest living authority:** user instruction that checkup verifies the declared 4-power × 3-aspect twelve-pane invariant, working harnesses, proportional assignment, gaps, and ghosts. This is a design constraint, not a runtime observation.
- **Directly reviewed by root:** `flows/b80e55/reports/system-census-capabilities.md`; `flows/b80e55/vision/fieldNexusSystemQuery.md`; `flows/b80e55/vision/systemCheckupAgentAndAutoWake.md`; `Vision/nexus.md`; `Vision/modelRoles.md`; `flows/1ac573/reports/field-nexus-concept.md` (Sept. 18 conceptual report, not an independent ruling).
- **Judgment companions, source review returned by `/root/census_psyche_review` rather than root direct review of all:** `flows/b81560/vision/operational-twelveFoldRolesOnly.md` (Sept. 20 relay); `operational-triadWorkDivision.md` (Sept. 19 direct); `flows/e06e4c07/vision/flowKnowledge.md` (Aug. 19 typed); `flows/b05237/vision/operational-reportIsTranscript.md` (Sept. 18); `Vision/messaging.md`; `operational-refreshFlowAndMessageFlowCoordination.md` (Sept. 19).
- **`/root/census_contract_design` source-only checkout findings:** `flow@61d765e` / `signal-flow@968ae3b` FlowNode native+Herdr tuple; separate Message HarnessProcessPin in `signal-message@37c3e5b` / `message@55657f4`, without an established Flow→Message join; `signal-harness@17bdd58` typed transcript observation without runtime; `transcript@4b52ed3` Claude-only CLI; bounded source search found no Field Nexus/signal-field. These are inspected revisions, never deployment/current-main claims.
- **Inherited handoff:** corrected `b1f8ff61fbdae63a66ec584abb5101bd374a121f`; Message durable-gate open boundaries.
- **Historical source-only mapping returned by `/root/census_contract_design`:** isolated `heartbeat-cf7879`/`core-checkup-cf7879` snapshots and their core-checkup/heartbeat files and state behavior. They lack usable Git metadata; the mapping is not a deployed-source equivalence claim.
