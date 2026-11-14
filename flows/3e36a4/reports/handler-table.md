# Connection handler inventory for vyz4

## Identity and authority

Read-only inspection of Flow `eabddc8d29ddd30b4665065cec4bee57ea7410ce` (0.56.2), using `git show`, not the mutable checkout. No branch, worktree, source, build, launch, store, configuration, pin or live unit was changed. This report extends `flows/b5fa74/reports/generated-dispatch-plan.md`. Generator ownership remains Astra/Psyche's pending decision.

All line numbers below are in `crates/flow-nexus/src/lib.rs` at that revision unless a file is named. Inventory: **42 ordinary capabilities and 24 meta capabilities**, including all Observe selections. This is static control-flow evidence, not a newly executed regression gate.

## Common connection and gate contract

`Connection::accepted` (1808) derives `process` from kernel peer credentials plus process-birth identity. Socket greeting precedes input decoding; ordinary undecodable frames go through `ordinary_query` with both persisted process and kernel peer evidence (1999–2022). Meta reads its own typed query (2233). Greeting/reading errors end the connection before dispatch. The generated `Answerable` call remains exhaustive, but socket handling has a preceding handwritten Input match.

The following gate symbols describe the **front-end dispatch_gate lifetime**, not a claim that a called domain operation takes no internal locks:

- **G**: `dispatch_serially` holds the gate through `dispatch_from` and request-id announcements, releases it, then calls `wake_deferred`, all before socket reply (2730–2790).
- **O**: serial dispatch calls the domain handler without an outer gate, then acquires the gate for request-id announcements only; this ordinary branch does **not** call `wake_deferred`. Domain capabilities retain their existing step locks. This is the explicit classifier, not a proposed new policy.
- **D**: socket intercept bypasses `dispatch_serially` entirely; no front-end gate or announcement pass.
- **L**: resolve caller origin; acquire gate only around `declared_launch`; release it; dispatch the resulting Start/Replace through serial dispatch. Start follows G, Replace O. Native launch internals remain domain-owned; the outer table does not justify extending this gate into a native wait.
- **MG**: meta serial dispatch holds gate through handler and announcements, releases it, then drains for a successful ResolveQueueDelivery or Withdraw. There is no general meta `wake_deferred` in this branch (2791–2846).
- **MO**: meta Restart/Refresh domain call off gate, announcements under gate, `wake_deferred` off gate, all before reply.

**W0** is the common ordinary tail: compute output; `write_response?`; drop connection; `settle_stops_at_confirmation`; return success. Write failure returns early, automatically drops the connection, and skips this tail settlement. G/O/L handlers can already have committed or performed their pre-reply follow-ups. A failed write does not roll them back.

**WD**: direct return of `write_response`; connection drops on return, with no common tail settlement. **W1**: save write result, explicitly drop connection, perform the named follow-up even when the write failed, then return the saved result. **WR**: Report uses `write_response?`, so only a successful write reaches explicit close and attributed follow-up. These differences are part of the observed baseline and must be made deliberate in any replacement.

For meta non-stream calls, **MW**: domain work including serial follow-up; `write_meta_response?`; close; settle stops; if BoundExisting contains Bound and its flow is Awake as a metaflow, drain that address. Write failure skips the post-close settlement and BoundExisting drain. Stream paths have their own termination described below.

## Ordinary capabilities

Caller `none` means no peer-specific evidence consumed at this front-end, rather than anonymous access control. Fields identifying a target are retained as payload. Replies name success/opening cases; every handler preserves its typed alternative/refusal Output through the generated Result error arm, rather than fabricating the positional success.

| Input / capability reference | Caller evidence | Gate | Reply and lifetime / follow-up |
|---|---|---|---|
| Start (466) | kernel-derived process → Origin | G | Started or settled/admission result; W0 |
| Refresh (496) | none | O | Refreshed, RefreshQueued or rejection; W0 |
| ResolveRecipient (504) | payload resolution request | G | RecipientResolved with refreshed route; W0 |
| Stop (522) | target FlowId | G | Stopped or typed rejection; pane lease/close and durable Record precede answer; W0 |
| Replace (608) | process → Origin | O | Replaced/pending/rejection; W0 |
| LaunchStatus (631) | requested LaunchRequestId | D | LaunchInspected; W0; never waits for outer dispatch gate |
| Observe (644) | target/selection, no peer attribution | D | See six stream selections below; streaming returns directly |
| ResolveCaller (698) | kernel peer → caller pane plus optional claimed FlowId | D | CallerResolved/refusal; W0 |
| Report (708) | report FlowId + report Process option checked by report_acts | D | Reported; WR: close, then after_attributed_report only if Reported and attribution matches; false attribution logs only |
| Lock (715) | Connection.process passed to dispatch_metaflow_peer | D | Locked/refusal; WD |
| Bind (726) | Connection.process passed to bridge | D | Bound/refusal; WD |
| Identify (737) | payload Process plus Connection.process to bridge | D | Identified/refusal; WD |
| Deliver (748) | Connection.process to bridge | D | SendAccepted/refusal; W1: wake_due(request.lock.second_address) iff accepted |
| Acknowledge (762) | Connection.process to bridge, payload keys | D | Acknowledged/refusal; WD |
| ArchiveRequest (770) | Connection.process to bridge, RequestId | D | Archived/refusal; WD |
| Release (784) | Connection.process to bridge, supplied Lock | D | Released/refusal; WD |
| Current (795) | requested Address | G | Current/refusal; rest_ended_awake runs before store read; W0 |
| Metaflows (808) | none | G | Metaflows available rows; W0 |
| IdentifyThread (816) | payload Process/native session plus Connection.process to bridge | D | ThreadIdentified/refusal; WD |
| Send (832) | Connection.process → sender; absent process is Unbound | D | Sent/SendAccepted/refusal; W1: wake_due iff answer.pending exists, even after failed write |
| ObserveSends (844) | none; supplied optional cursor | D | SendsObserved then SendChanged; stream |
| ObserveSender (863) | payload Process/native session resolved by observation_sender, not socket identity | D | SendsObserved then SendChanged; resolution refusal is WD |
| ObserveDeliveries (892) | none; supplied optional cursor | D | DeliveriesObserved then SendChanged; stream |
| DeliverAll (908) | requested Address | D | Drained/refusal; WD; domain work before write |
| Launch (921) | process → Origin | L | resulting Start/Replace output or declared-launch refusal; W0 |
| Rehearse (936) | declared request, Origin unbound | G | Rehearsed/refusal; W0 |
| BindSeat (946) | payload binding evidence | D | SeatBound/refusal; W1: drain_awake iff SeatBound |
| Adopt (956) | payload adoption evidence | D | Adopted/refusal; W1: drain_awake iff Adopted |
| Restart (964) | target FlowId | O | Restarted/RestartQueued/refusal; W0 |
| Keep (972) | requested Address → awake handover writer | G | Kept/refusal; handover obligation uptake precedes write; W0 |
| Drop (979) | requested Address → awake handover writer | G | Dropped/refusal; obligation uptake precedes write; W0 |
| Glance (986) | requested Address | G | Glanced/refusal; W0 |
| Read (993) | requested Address | G | Handover/refusal; W0 |
| Cancel (1000) | RequestId | O | Cancelled/refusal; W0 |
| Silence (1010) | RequestId | G | Silenced/refusal; W0 |
| Clear (1020) | Address | O | Cleared/refusal; W0 |
| ClearAll (1027) | none | O | AllCleared/refusal; W0 |
| Push (1034) | Address + Priority | O | Pushed/refusal; W0 |
| Queues (1041) | none | G | Queues/refusal; W0 |
| Hot (1048) | none | G | Hot/refusal; W0 |
| Remind (1056) | process → sender_of, absent is Unbound; sender refusal retained | D | Reminded/refusal; WD |
| Answer (1066) | RequestId | G | Answered/refusal; W0 |

The bridge interception includes ArchiveRequest and Acknowledge even though the serial classifier does not list them O: moving these under the old serial wrapper would newly serialize them. Likewise socket Send, Report, DeliverAll, Remind, BindSeat and Adopt skip that wrapper's announcement pass. An inventory-based replacement must account for these facts rather than treating the old classifier as the socket policy.

## Meta capabilities

Except ObserveConfiguration, the socket obtains `meta_resolver(kernel peer)` before serial dispatch. Only ResolveQueueDelivery actually consumes that resolver in MetaCall; its identity records the actor and is not an authorization guard. Other explicit target/process/container evidence remains payload.

| Input / capability reference | Evidence beyond common peer capture | Gate | Reply / lifetime |
|---|---|---|---|
| Configuration (1090) | none | MG | Configuration/Unconfigured/refusal; MW |
| Configure (1102) | ConfigurationChange | MG | Configured echo/refusal; commit/application and configuration/reminder announcements before reply; MW |
| ConsumeReset (1116) | ResetRequest and configured endpoint adapter | MG | reset outcome or ResetRejected; MW |
| RegisterFlow (1143) | supplied FlowNode checked with herdr.validate_registration | MG | FlowRegistered or registration rejection; MW |
| MetaBindExisting (1163) | container shape/socket/process liveness + verified seat/binding | MG | BoundExisting including Bound or Refused binding, or rejection; MW with conditional post-close drain |
| Retire (1238) | FlowId, persisted state, continuity and pane presence | MG | FlowRetired/rejection; pane lease/close then Record before reply; MW |
| Restart (1312) | FlowId | MO | Restarted/RestartQueued/RestartRefused via into_meta; MW |
| Refresh (1323) | Address | MO | Refreshed/RefreshQueued/RefreshRejected via into_meta; MW |
| Deliver (1334) | DeliveryRequest | MG | Delivered/refusal; MW |
| Vet (1344) | DeliveryRequest | MG | Vetted/refusal; MW |
| Command (1354) | CommandRequest | MG | Commanded/refusal; MW |
| ResolvePeer (1364) | supplied ProcessIdentity | MG | PeerResolved/refusal; MW |
| ReadEvents (1374) | FlowId | MG | EventsRead/refusal; MW |
| ReadQueueDeliveries (1384) | Address | MG | QueueDeliveriesRead/refusal; MW |
| ReadSendOutcomes (1394) | none | MG | SendOutcomesRead/projected records or rejection; MW |
| ObserveLegacyArchive (1413) | none | MG | LegacyArchiveObserved/projected records or rejection; one reply, **not a stream**; MW |
| Debug (1433) | Address | MG | Debugged/refusal; MW |
| ResolveQueueDelivery (1446) | captured resolver, fallback meta_resolver(None) for direct calls | MG | QueueDeliveryResolved/refusal; successful resolution drains after gate release **before write**, including when later write fails; MW |
| Inspect (1462) | Address | MG | Inspected/refusal; MW |
| DebugDelivery (1473) | RequestId | MG | DeliveryDebugged/rejection; MW |
| Rebind (1489) | Rebind payload | MG | Rebound/refusal; MW |
| Withdraw (1500) | Address + withdrawal payload | MG | Withdrawn/refusal; success drains requested address after gate release **before write**; MW |
| ObserveConfiguration (1513) | none | D | Configuration/Unconfigured/refusal then changes; dedicated meta stream, no common resolver or MW tail |
| Remove (1521) | Removal | MG | Removed/refusal; configuration edit/application before reply; MW |

## Streams and cancellation

All socket streams bypass the serial dispatcher and common reply tail. No dispatch gate is held for subscription lifetime. A write error ends streaming; it is not replaced by a success Output. Standard stream functions return Result<(), String>.

- **Observe.Launch / Observe.Agent** (2026–2045): `serve_cancellable_observation`, in `observation_lifetime.rs`. Opens cancellation and completion eventfds, clones peer, starts a scoped descriptor watcher for completion, Nexus stop and peer EOF/error. Domain observer writes frames through the actual peer. Completion announces and joins watcher, including write-error completion. Distinct PeerClosed/NexusStopped causes announce launch_changes; errors or normal terminal completion return without waiting for another input. This watcher does not require shutting down the peer to join.
- **Observe.Undecodable / Observe.TurnEnds / Observe.Metaflows**: `serve_undecodable` (1857), `serve_turn_ends` (1890), `serve_metaflows` (1923). Each clones a peer reader with no read timeout; EOF/error sets AtomicBool disconnected and announces its condition variable (launch_changes for first two; metaflow_changes for last). Domain observer sends opening snapshot and subsequent changed state. On domain completion/error, shutdown Both and join reader, then return combined result. Nexus stop announces all these sources. Preserve setup failures as transport errors too.
- **ObserveSends / ObserveSender / ObserveDeliveries**: `serve_sends` (1818), `observe_sends.rs`. Same blocking-reader cancellation and shutdown/join lifecycle; wake source launch_changes. Each opening honors optional replay cursor. Every/selected-sender opens SendsObserved; Message opens DeliveriesObserved. Later durable snapshots become SendChanged, cursor advances to observation.delivery_cursor; waits are event-driven. Store error emits typed Refused and ends. Domain checks both disconnect and stop. ObserveSender uses its forwarded identity selection, not connection origin.
- **Observe.Retirement**: subscribe at ordinary interception; missing evidence writes RetirementObservationFailed and returns. For a successful subscription, `serve_retirement` calls `serve_attached_retirement` (2261) and **always detaches afterward**, even on error. First write RetirementObserved(snapshot); then create blocking reader watcher which calls subscription.disconnect on EOF/error. Read subscription.next_response, write responses until typed RetirementObservationFailed, a write error, or subscription error. Shutdown Both and join watcher. Opening-write/clone/spawn failure returns through the outer detach. Nexus stop fails all subscriptions under handover_write_gate and wakes them (StopsNexus, 2524). Do not lose detach on early return.
- **Meta ObserveConfiguration**: `serve_configuration` (1956) uses blocking-reader disconnected flag + configuration_changes; shutdown Both and join on return. `observe_configuration.rs` sends current Configuration/Unconfigured/refusal, then only changed responses; waits on the announcement. Stop announces configuration_changes. No meta resolver attribution or common post-close drain.

## In-process snapshot contract

`dispatch_from` calls generated `Input::answer(&OrdinaryCall{nexus,origin})`; `dispatch_meta_from` similarly uses MetaCall. These are value-returning, non-streaming calls, not socket emulation. `dispatch` itself still hand-special-cases Start (harness_arguments precheck), Launch (declared request then recursive dispatch), and Rehearse (314–335). This is an additional source-review seam if the acceptance target includes every hand Input route.

OrdinaryCall carries only nexus/origin. It has no peer: ResolveCaller passes no pane; Send and bridge methods pass None process; Remind is Unbound. Its Report records but does not run socket after_attributed_report; BindSeat/Adopt have no socket post-close drain. Observe returns exactly one opening snapshot: LaunchInspected, AgentObserved, UndecodableObserved, TurnEndsObserved, MetaflowsObserved or RetirementObserved. Retirement attaches only to capture snapshot and immediately detaches. ObserveSends and ObserveDeliveries deliberately ignore the optional cursor and read a whole snapshot with None; ObserveSender resolves forwarded identity but likewise reads snapshot with None. Positional mismatch uses the generated Result error arm (e.g. ObserveSender returns SendsObserved there); this is not a refusal.

MetaCall Configuration and ObserveConfiguration return the same single configuration response; the latter returns Unconfigured through its positional success and Configuration through its alternate Output arm. A direct MetaCall resolver defaults to meta_resolver(None), documented as process 0. Direct dispatch does not synthesize socket close, write failure or subscription lifetime. Any generic mutable completion design must preserve both this value/snapshot contract and the connection contract; they are not interchangeable.

## Immutable baseline and capsule evidence

Exact eabddc8d gate is recorded in `flows/565bc8/release-0562/gate-eabddc8d.log` and `flows/565bc8/reports/release-0562.md`: exit 0. Both exact release and preceding emission-head logs contain the same flow-nexus target results: 920 passed/8 ignored, 10 passed/1 ignored, and 3 passed/0 ignored, plus zero-test targets. Thus 933 passed/9 ignored is the aggregate and 920/8 is one target, not a lost-test discrepancy. No new gate was run.

**Discrepancy:** the existing 8/22 capsule is on `0d39641be708b119e4676067eae09f45ecfa74f0` (0.56.1), not exact eabddc8d (0.56.2). Its report states only a version bump separates the release, but it is not an exact-package eabddc8d capsule. Package `/nix/store/1qblz7hqx5pd0fdnn5m0kq2fp0fcpjqq-flow-configured-0.56.1`; Curriculum `/nix/store/79zjg9f0iz9ljndlqnw6csv7bvyc7psc-rust_curriculum-0.1.0`.

Evidence: `flows/565bc8/reports/emission-rebase-b.md`; full stdout `flows/565bc8/capsule-emission-b-0d39641.log`; Nexus log with same basename `.nexus.log`; witnesses `/home/li/witnesses/565bc8/capsule-0.56.1-20261114T105748Z` (claude-transcripts/, codex-sessions/, nexus.log). Passed scenarios 0,1,2,5,8,10,11,12; exit 1, reported 1163 s; teardown stopped Nexus/app-server/Curriculum/Herdr. Scenario 19 Sent parsing remains a known fixture issue, not new route acceptance.

Report identifies invocation ingredients: scratch `capsule-94bfd37` wrapper, the head capsule plus `flows/e3a7d1/capsule-scratch-fixes.diff`, `--keep-going`, Codex included, `FLOW_CAPSULE_WITNESS_DIR=/home/li/witnesses/565bc8`, package above. Owner supplied the exact invocation in Result fm8q, after the initial inventory. Wrapper: `/tmp/claude-1001/-home-li-primary/565bc82a-9854-530d-bd62-4d0faa6e2c11/scratchpad/capsule-94bfd37/bin/flow-capsule`. From `/home/li/primary/flows/565bc8`, the full run was:

```sh
FLOW_CAPSULE_WITNESS_DIR=/home/li/witnesses/565bc8 /tmp/claude-1001/-home-li-primary/565bc82a-9854-530d-bd62-4d0faa6e2c11/scratchpad/capsule-94bfd37/bin/flow-capsule /nix/store/1qblz7hqx5pd0fdnn5m0kq2fp0fcpjqq-flow-configured-0.56.1 --keep-going --log /home/li/primary/flows/565bc8/capsule-emission-b-0d39641.nexus.log > capsule-emission-b-0d39641.log 2>&1
```

Owner reports the rerun used the same invocation with `timeout 580`, `--only 0,18,19`, and `capsule-emission-b-0d39641-s19-rerun.log` / `.nexus.log`, witnesses ending `T111732Z`. Historical transcript pointer: `/tmp/claude-1001/-home-li-primary/565bc82a-9854-530d-bd62-4d0faa6e2c11/tasks/adfa595d7ff897824.output`. This is owner-attested command provenance; this successor has not rerun it or read that large transcript. The package is the emission branch head before its release-version bump, **not the earlier 0.56.1 release build**. The exact-eabddc8d capsule discrepancy remains. A candidate must retain the eight named passes and clean teardown; count alone is insufficient.

## Next bounded step

Return table and discrepancies to Astra. Astra notice 9150 confirms Fable owns the generated Answerable design and the ruling remains pending; hold both generator and Flow edits. If approved, Mind curriculum Opus owns the ethos-zero producer. Exact capsule invocation recovery is now complete through owner Result fm8q; await the design ruling. No implementation or capsule lane is open. Historical efforts/.20/.21/Home work remain held. The settlement-liveness ruling a79u stands; this table does not reverify its historical stopped-successor candidate or assert recovery exists.
