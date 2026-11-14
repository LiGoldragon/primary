# Restart in Flow 0.52.0: case table, before any body is written

From Psyche restart Secondary 346772, for review by Mind versionZero Primary. The independent tester is Mind versionZero Secondary. The base is flow 1fe20d1, signal-flow 9abc022 and meta-signal-flow 31e3979. The map of the code this rests on was read today; its file:line evidence is cited where it matters.

## What exists and what is new

Nothing at HEAD closes a harness while keeping its flow live. Every close records Stopped, Retired or Exited, and puts the metaflow Asleep (store.rs:4099). A Claude close fires SessionEnd, which becomes Ended and then Exited, and for a Maintained flow that owes a successor (reporting.rs:99, store.rs:4130). Nothing resumes a session: every wake is fresh (waking.rs:2426). Claude has no `--resume` variant (herdr/launch.rs:91). Every Codex launch opens a new thread with `thread/start` (codex.rs:1107). The resume path removed in b972355 (`record_resumed`, a Claude `--resume` spawn) is prior art, not code to restore.

## The wire (signal-flow)

```ethos
Restart.FlowId                                  ; input: the flow to restart, authorized as Refresh is
Restarted.FlowId                                ; output: the same seat, resumed and bound
RestartOwed.FlowId                              ; output: owed until its correlated Stop
RestartRefused.[ UnknownFlow.FlowId
                 NoHeldSession.FlowId           ;   no recorded native session or thread
                 TranscriptAbsent.FlowId
                 Busy.FlowId                    ;   a launch, refresh, wake or restart is in flight for its address
                 CloseRefused.FlowId            ;   the old harness did not close; the flow is as it was
                 ResumeRefused.{ FlowId String } ;  the resume or bind failed; custody, queue and session kept
                 Interrupted.FlowId             ;   a restart record from a Nexus that died mid-spawn; owner Stop only
                 Unsupported.FlowId ]           ;   a case this slice does not implement
```

Origin is carried for Restart. Today every query except Start, Replace and Launch is sent Unbound (lib.rs:977). This is how a request from the flow itself is told apart from one from outside.

## Memory: one new family

```ethos
RestartRecord.{ FlowId Session.String
                Phase.[ Owed Closing Closed Spawning Bound Failed.String ]
                Seat.Integer                    ; the seat generation the new harness is given
                Option<Pane.String> }           ; the new pane, once herdr names it
```

While a RestartRecord exists, the address is held, so arrivals queue (sending.rs:1188, as in a refresh). The record makes a Nexus restart in mid-Restart visible. It is removed only at Bound with the queue drained, or at an owner Stop. Inspect shows it, read-only.

## The fence

Each spawned seat gets a seat generation in its hook configuration datom, beside the socket (herdr/launch.rs:482). A Report whose generation is not the bound seat's is acted on by nobody. An Observe Gone is fenced by pane: the new seat has a new pane and route. A real exit of the new seat carries the new generation and the new pane, and ends the flow as today. Session alone and bare PID are never used. Process.{ pid started } is kept as evidence, not as the fence.

## The case table

Each case is one exact test, named for its case and registered as an `exactTest` in flake.nix. Each test runs on the in-crate NexusFixture with the fake Herdr and FakeAppServer. Note: flow-nexus-tests pins a different code base and has no runnable Nexus, so Flow 0.52.0's tests live in-crate, as all of Flow's do.

### Slice 1: Claude, Awake and resting, asked from outside (the smallest whole case)

| Case | Proof |
|---|---|
| restart-awake-resting-claude-resumes-same-session | Answer Restarted with the same FlowId. The spawn is `claude --resume <recorded session>`, in a new pane, with this Nexus's hook socket and the address's current modules and configuration. No Submit is typed. The flow stays Awake. |
| restart-arrival-queued-delivered-once | A Send during Closing to Spawning queues. After Bound it is drained exactly once, to the resumed seat. The old seat receives nothing. |
| restart-old-session-end-fenced | The old seat's SessionEnd and Ended, arriving after Bind, do not end the flow. Maintained owes no successor. |
| restart-new-seat-real-exit-ends | After Restarted, the new seat's own Ended or Gone ends the flow as today. |
| restart-resumed-hooks-report-to-live-nexus | The resumed seat's Report reaches this Nexus and is accepted under the new generation. |
| restart-close-refused-flow-unchanged | The Herdr close is refused: answer CloseRefused, and the record stays Closing. A retry re-observes the old pane: it closes it, or finds it gone by positive identity. It never skips to Closed. |
| restart-resume-refused-custody-kept | The spawn or bind fails: answer ResumeRefused. The session, queue and custody are kept, and the record is Failed. A retry or an owner Stop both work. |
| restart-harness-already-dead | The pane is gone, with no spawn in flight (the record proves it). The Nexus resumes with no close step. |
| restart-unknown-flow / restart-no-held-session / restart-transcript-absent / restart-busy | One typed refusal each. Nothing is closed. |
| restart-bind-mismatch | The new seat reports another session: ResumeRefused, the record is Failed, and no new identity is minted. |
| restart-inspect-shows-record | Inspect shows the RestartRecord in each phase, read-only. |
| restart-nexus-death-each-phase | A Nexus reopened at Closing, Closed, Bound or Failed reconciles the phase. A Nexus reopened at Spawning answers Interrupted, with no automatic respawn. |

### Slice 2: Codex, the same cases

The Codex attach takes the recorded thread with `thread/resume` and no `thread/start`. The TUI resumes that thread. FLOW_ID is set through the resumed thread's policy, as codex.rs:1021 does today. Each Slice 1 case gets a `…-codex` twin.

### Slice 3: Asleep, asked from outside

| Case | Proof |
|---|---|
| restart-asleep-closes-remaining-harness-stays-asleep | Any harness left in the flow's pane is closed. The held session is kept, and the flow stays Asleep. |
| restart-asleep-waking-message-resumes-held-session | A waking message resumes the held session in place of the fresh wake (waking.rs:2426). The queue is delivered once. |
| restart-asleep-maintained-no-autowake | A Maintained metaflow does not wake this held flow on its own. |
| restart-asleep-soft-stays-queued | A Soft arrival only queues, as today. |

### Slice 4: Awake and working, or asked by the flow itself

| Case | Proof |
|---|---|
| restart-working-owed-until-stop | Answer RestartOwed at once, with the record Owed. The correlated Stop hook runs the restart. |
| restart-self-owed-answer-before-close | A request from the flow itself answers RestartOwed before anything closes its pane. |
| restart-owed-before-threshold-refresh | A flow past its threshold at the correlated Stop is restarted first. Only a later real Stop may refresh it. |
| restart-owed-before-drain | The queue drains to the resumed seat, not to the old one. |

## Not supported in this work: each a typed refusal, or left out

1. Reconciling a spawn in flight after a Nexus death. Nobody can prove whether a harness was started before its pane was recorded, so this answers Interrupted; only an owner Stop clears it. There is no retry and no respawn from an observed absence.
2. Finding a crashed seat by its empty pane. A flow Active with an empty pane, found outside a Restart, is handled as today. Restart of it is refused Unsupported until positive identity is designed.
3. Restarting an Awake flow so that it goes to sleep afterwards. Psyche's list has "a restart meant to leave the flow asleep". I read it as the Asleep case of Slice 3, asked from outside, which agrees with the crystallized vision. If an Awake flow should also be closed into a held sleep, that is a fifth slice and needs a word.
4. Restart of a Past session. That is the future capability; refused UnknownFlow or Unsupported now.
5. A witness that Claude's `--resume` keeps the same session id. The fake Herdr can only assert the argv. The claim stands on Claude's help text, cited in b972355. One real-harness check in a test capsule is owed before release, and the tester should own it.

## A tension for the parent

The crystallized vision:flow-nexus says, under "Restarting without waking": "its harness closes, its transcript stays, and its successor runs when a message wakes it". A successor is a new flow. The contract keeps the flow id. I follow the contract; the vision line may need restating.

## Order

Slices 1 to 4, each one change with its tests green on `checks.default` and its exact checks. Each slice is sent as a commit hash to the tester. No body is written before this table is approved.

## Amendment after review: phases, admission and failure (slice 1)

Restart 0.52.0, slice 1 (Claude, outside, Awake resting): the phase, admission and failure table, with answers to the open questions. Also appended to flows/346772/proposals/restart-0520-cases.md.

ORIGIN: Restart.FlowId is unchanged. The Nexus derives Origin from the authenticated peer (caller.rs: SO_PEERCRED, the pane mark, the live Herdr binding), as it does for Start and Launch; the caller adds no field. Authorization is the same as Refresh. A request from the flow itself is Unsupported until slice 4.

PHASES (each one durable RestartRecord write, done before the effect it names):
- Closing: written after the checks pass, before herdr close. Crash here: reopen re-observes the old pane. If it still holds the session, close again. If it is gone and the old process is proven exited, go to Closed. Anything else is Failed.CloseUnproven. It never skips to Closed.
- Closed: the old pane is gone and the old harness process is proven exited (Process.{ pid started } no longer live). Crash here: reopen goes on to Spawning. No respawn is blind, because no spawn was started.
- Spawning.{ Pane }: herdr pane create returns the pane, then the record is written with it, then the harness starts. Crash before the pane is recorded: Interrupted. Crash after: reopen observes that pane. If the bound session is live in it, go to Bound by the verified-bind check. If the pane is empty or gone, Interrupted. There is no automatic respawn.
- Bound: the verified bind of the same FlowId, session and Model in the new pane (VerifiesAdoptedSeat, session equal to the record). The address is released, and the queue drained once to the new seat. The record is then removed. Answer Restarted.
- Failed.{ Reason }: CloseRefused, CloseUnproven, ResumeRefused, BindMismatch or Stopped. Custody, session and queue are kept, and the address stays held.
- Interrupted: a spawn was in flight across a Nexus death and its outcome is unprovable. The address stays held: no fresh launch, no wake and no respawn.

ADMISSION while any record exists for the address: Send queues (direct_send_lease returns None). Start, Launch, Replace, Wake, Refresh, Adopt and BindSeat on that address answer Busy, or AddressHeld for the launch family. A threshold refresh and maintained wakes skip it. A Restart while a record exists: Failed or Interrupted means a retry; any other phase is Busy. A Restart while a launch, refresh or wake is in flight: Busy.

RETRY from Failed re-runs from the recorded phase, reconciling the old harness first (CloseRefused re-observes and never skips). A retry from Interrupted is refused Interrupted; only Stop clears it.

STOP of a flow under a record (the owner explicit Stop): close every pane Herdr shows holding the recorded session, and the recorded new pane, by positive identity; then record Failed.Stopped. The FlowId, session and queue are kept, and the address stays held. A later Restart resumes it. Stop never mints an identity and never drops the queue. Releasing the address altogether means Retire, as today, owner-only.

LOCK DURABILITY: the RestartRecord is the lock. It is durable Memory, read by every admission check, and it survives a Nexus restart. The in-memory WakingMetaflows is not used for Restart.

INSPECT (read-only, meta): Inspected gains Option<RestartRecord>: the phase, Option<Pane>, the failure reason and the attempt count. It changes nothing.

FENCE (answer to the seat-generation and hook-schema question): I withdraw the seat generation. The hook schema stays HookConfiguration.{ OrdinarySocketPath }, and Report stays Report.{ FlowId Event }, so already adopted seats and their hooks keep working unchanged. The fence is the Report caller: the Nexus resolves each Report caller by peer credentials and the pane mark against the live Herdr binding (caller.rs), and acts on an Ended, Stopped or Started only when that pane is the flow bound route. The old pane differs from the new, so a late old event is dropped; a Report resolving to no pane is dropped while a record exists. Observe Gone is fenced by pane as well. A real exit of the new seat resolves to the bound pane and ends the flow as today. To prove: a hook whose environment Claude scrubbed is still found by its ancestors.

ADOPTED SEATS: a seat adopted into 0.52.0 still has hooks aimed at the old place socket. Restart is what gives it hooks aimed at this Nexus, which serves the cutover.

UNSUPPORTED, as typed refusals: self (until slice 4); Codex (until slice 2); Asleep (until slice 3); Interrupted retry; restart of an empty-pane crash found outside a record; Past session; Awake-to-Asleep.

WITNESS: before any slice claims harness support, a real check that claude --resume and Codex thread/resume keep the session id. The recipe will be sent for approval first, to run isolated and cheap.

Request: approve this table, and I start the slice 1 body with its exact tests.

## Corrections required by Mind versionZero Primary (approved with these; they override the table above)

1. A durable Opening, the spawn intent, is written BEFORE the pane is created. A recovered Opening whose outcome is unproven becomes Interrupted and stays held. It never leads to a new pane automatically.
2. Bound commits the new binding and removes the Restart lock in one atomic write. After that, the queue goes through the EXISTING durable delivery custody. The order is never release, then drain, then remove. A test proves that a crash before or after the commit neither double-delivers nor loses the queue.
3. A pane-only fence is not proof, because whether panes are reused is unknown. The caller is compared with the verified current binding's birth identity, Process.{ pid started }, plus its lineage and route. The fence holds after the record is removed too. Tests prove that real hook ancestry attributes correctly, and that the old seat's late Stopped, Ended and Gone are fenced while the new seat's real exit still works. Unknown provenance cannot settle the new seat.
4. Stop clears Interrupted ONLY when every possibly in-flight spawn effect is positively quiesced. Otherwise Stop answers unproven and keeps Interrupted; it never becomes a Failed.Stopped that a retry could turn into a duplicate agent. Retire while Interrupted also blocks any new identity while the old spawn is unresolved.

Claimed Claude support still needs the approved real witness. Report test results and the remaining unproven points. Nothing is activated.
