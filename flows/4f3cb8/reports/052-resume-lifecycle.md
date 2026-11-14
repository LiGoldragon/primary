# 052 Resume — concrete lifecycle and schema proposal

Version-zero extension only. No gate, Living payload, StartedBy or Continues. No shared Refusal or LaunchStatusOutcome change is proposed. Ordinary caller identification stays as it is. Dedicated request Resume.FlowId; replies Resumed.FlowId, ResumeRejected.ResumeRejection and ResumeUncertain.FlowId. Native same-session emission, not a new Flow launch.

## Authored data shape

Existing imported leaves are the pinned ordinary contract types. New generation/id/state wrappers below are proposed ordinary signal-flow observation vocabulary. Flow persists them through explicitly versioned private record wrappers, following the existing version-zero record/projection pattern. Their exact schema identities require allocation; any future wire-shape change requires explicit frozen-mirror handling for these new records.

```ethos
Library
[ :flow_ethos:[ FlowId Address ProcessIdentity ]         ; existing layered identity
  :signal_flow:[ NativeSessionId HarnessKind NativeTranscriptCursor
                 HerdrSessionName HerdrAgentName HerdrRoute
                 HerdrRefusal NativeLaunchFailure BindingRefusal ] ]     ; existing kernel PID/UID/start-token observation
[ Generation.Integer                    ; checked positive per-flow sequence
  KernelBootId.String                    ; observed kernel boot identity, not caller privilege
  NativeProcessStamp.{ KernelBootId ProcessIdentity }
  ResumeAttemptId.{ FlowId Generation }  ; never a LaunchRequestId
  ResumeHead.{                           ; singleton per held FlowId
     FlowId
     LastGeneration.Generation
     Active.Option<ResumeAttemptId> }
  ResumeTarget.{                         ; requested place before any pane effect
     HerdrSessionName
     HerdrAgentName }
  ResumeStage.[ PreparePane StartHarness ] ; the external operation being attempted
  BeforeAttachment.{                    ; scoped pre-call observation after checking no active original attachment
     KernelBootId
     Vector<ProcessIdentity> }
  ResumeTargetObservation.{             ; exact observed route and prior processes, retained before start
     HerdrRoute
     BeforeAttachment }
  ResumeBinding.{                       ; confirmed observation for THIS attempt, not merely an old label
     ResumeAttemptId
     HerdrRoute
     NativeProcessStamp
     NativeSessionId
     HarnessKind
     NativeTranscriptCursor }
  ResumeEvidence.[                      ; actual native/observation failures after possible effects
     Herdr.HerdrRefusal
     Native.NativeLaunchFailure
     Binding.BindingRefusal
     ProcessObservationUnavailable
     BootIdentityUnavailable
     BootIdentityChanged
     PersistenceUnconfirmed
     ObservationAmbiguous ]
  ResumeRejection.[               ; only when no native effect was attempted
     UnknownFlow.FlowId
     Awake.FlowId
     NoTranscript.FlowId
     Locked
     PersistenceRefused
     NotReady.FlowId
     GenerationExhausted.FlowId
     ObservationUnavailable ]
  ResumeAttempt.{                        ; immutable identity/intent plus evolving phase
     ResumeAttemptId
     Address
     NativeSessionId
     HarnessKind
     NativeTranscriptCursor
     ResumeTarget
     Option<ResumeTargetObservation>
     ResumePhase }
  ResumePhase.[
     Prepared
     Emitting.ResumeStage
     PaneReady
     Uncertain.{ ResumeStage ResumeEvidence }
     Confirmed.ResumeBinding
     Refused.ResumeRejection ] ]
[]                                       ; traits: record ownership supplied by existing Memory machinery
[]                                       ; associations
```

Core approved KernelBootId plus existing ProcessIdentity as the new NativeProcessStamp. These are observations of resource lifetime, not authority. ResumeEvidence reuses existing native post-effect types only where their meaning fits; ResumeRejection contains no native launch/Herdr-start failure payload, no LaunchRequestId/new-flow fact is invented. Actual reachable branches must be listed before bodies, and unused proposed rejection branches are pruned. Boot mismatch/unavailable or insufficient attachment correlation remains uncertain. No arbitrary diagnostic string substitutes for these categories.

The before-attachment constructor is private to the observation boundary: it requires checking the target for an existing active original-session attachment. A matching attachment already present is not proof of this generation. Kernel PID/start token may stay the same across shell exec, so acceptance depends on a witnessed new original-session ATTACHMENT, not a fabricated requirement that PID changes. The persisted before/after observations are different temporal evidence, compared explicitly rather than treated as duplicate configuration authorities.

Proposed namespace identities, unallocated: table `flow_nexus_resume_heads`, family `flow-nexus-resume-head`, schema `flow-nexus-resume-head-v1`; table `flow_nexus_resume_attempts`, family `flow-nexus-resume-attempt`, schema `flow-nexus-resume-attempt-v1`. Head key is held FlowId; history key is an authored collision-free domain projection of ResumeAttemptId: canonical decimal UTF-8 byte length of FlowId, colon, exact FlowId bytes, colon, canonical positive decimal Generation. For example FlowId abc and generation2 project to `3:abc:2`. This is the versioned record declaration's projection, not a nonexistent generic Engine key encoder. Head keys remain exact FlowId. Checked generation exhaustion returns GenerationExhausted(requested FlowId) before reservation, never a persistence error. MemoryVersion1 for each. No predecessor family is rewritten solely to create these rows. Normal catalog/schema compatibility still must admit the new families explicitly.

## One admission owner and durable boundaries

The store-private identity/admission capability serializes Resume with Launch/Adopt/Stop changes to that flow/address. All served/direct/internal entry points enter it, not only the network dispatch gate. It uses existing AtomicCommit and the existing address-hold helpers that add writes to that plan.

The current hold is AddressHold.{flow_id,address,found:Option<Metaflow>}, schema address-hold-v5. It has no HoldId or generation. Preserve that shape. Generation ownership is established by the matching ResumeHead+ResumeAttempt in the same transaction, not inferred from a hold containing the same FlowId. A preexisting unassociated hold refuses as Locked; it is not silently appropriated. Existing given_back compares flow identity only, so the admission owner must first validate the active attempt generation before calling it.

1. Resolve requested held flow, actual native session and existing bounded transcript. UnknownFlow/Awake/NoTranscript carry requested FlowId and refuse before reservation/emission. Pending returns NotReady; Active returns Awake; Stopped/Exited/Retired are explicitly eligible as the same flow, resumed Maintained, with verified original native session/transcript and free address admission; an occupied successor blocks without displacement. Both closed harness variants Claude/Codex are required supported before release, so no unreachable UnsupportedHarness variant is declared. Missing concrete native capability is NotReady before effects, not inferred support. Installed Claude2.1.294 help proves --resume session-id exists and --fork-session would change identity; actual capsule proof is later. Codex native resume paths exist in916.
2. Under admission owner, observe no conflicting active attempt/hold/address occupant. Allocate checked next per-flow generation, write active head and Prepared history, and acquire address hold in ONE transaction. First generation is storage-sequence initialization, not a behavioral default. Retain all previous terminal attempts.
3. Commit Emitting.PreparePane before the pane call. Persist requested Herdr session/name and attempt association; a future actual pane id is not invented. If pane creation/result is ambiguous, retain active head/hold and record Uncertain with native evidence. Do not emit another pane request merely because observation found nothing.
4. After exact attempt-owned pane observation, persist PaneReady AND Some(ResumeTargetObservation { exact route, BeforeAttachment { boot identity, observed process identities } }) in the SAME transaction before harness resume. PaneReady or Emitting.StartHarness with absent prior observation is InconsistentRecords and cannot emit. Commit Emitting.StartHarness with that route before the same-session native call. A crash after either intent may mean the effect occurred; it is not a clean refusal.
5. Independently observe ORIGINAL FlowId/native session/transcript prefix and the exact route associated with THIS generation. Correlate new attachment evidence, not merely an old matching label/transcript. On sufficient proof, atomically record Confirmed, update existing current native binding coherently, clear matching head and release matching address admission. Return Resumed(original FlowId) only after successful durable publication.
6. Known pre-effect refusal records Refused and atomically clears matching head/hold. Cleanup touches only resources positively proven owned by that attempt. Any possible effect or uncertain cleanup remains Uncertain with reconciliation required. A terminal old receipt can neither clear a newer head nor release its hold.

The head retains LastGeneration after completion. A later stop/resume creates a new generation; previous Confirmed never suppresses or authorizes it. A duplicate request while an attempt is Prepared/PaneReady cannot launch a competing attempt. An unresolved emitting/uncertain attempt returns ResumeUncertain without new native emission. Exact in-progress rejection versus observed uncertainty follows recorded phase; no clean rejection asserts the previous attempt had no effect.

## Reconciliation and readback

Reconciliation inspects native/route/transcript evidence for the recorded attempt. It does not retry the call automatically or assume an absent listing proves absence of effect. It can confirm only sufficient current-generation evidence; otherwise the attempt remains uncertain. Core authorizes bounded typed Resume-attempt readback by FlowId/attempt through existing operation observation and repeated unresolved Resume inspecting the SAME attempt. No administrative force-resolution, manual row deletion or fresh emission is added. Exact existing observation variant additions and consumers belong to the final wire packet.

Approved readback boundary: Observe is read-only and performs NO reconciliation or mutation. Explicit Resume may reconcile its existing active attempt without emission. The proposed ordinary additions are:

```ethos
ResumeSelection.[ Flow.FlowId Attempt.ResumeAttemptId ] ; nested under existing ObserveSelection.Resume
ResumeInspection.[ NoAttempt.FlowId                    ; known flow, no attempt history
                   Flow.{ ResumeHead ResumeAttempt }   ; active, otherwise latest terminal, at most one
                   Attempt.ResumeAttempt ]             ; the exact requested historical attempt
ResumeObservationRejection.[ UnknownFlow.FlowId
                              UnknownAttempt.ResumeAttemptId
                              PersistenceRefused
                              ReadViewChanged
                              InconsistentRecords ]
```

Existing ordinary Response gains ResumeObserved.ResumeInspection and ResumeObserveRejected.ResumeObservationRejection. Socket Observe.Resume sends exactly ONE consistent-view response then closes; it is not a subscription. The existing CLI read-until-EOF branch therefore terminates after that frame; its tests cover EOF. Direct dispatch, exhaustive socket Observe arms and the store-only Observe catchall all receive explicit Resume handling, not inherited LaunchStatusRejected behavior. Flow head plus selected attempt are read from ONE consistent view; absence is not an empty/false fallback on storage failure. No unbounded history vector is emitted. Core approved flow-ethos Library as single owner of the exact four current declarations ProcessId, ProcessUserId, ProcessStartToken and ProcessIdentity, unchanged. Meta imports and reexports its old public paths; ordinary imports the shared types. Ordinary Process remains distinct; historical mirrors remain frozen. The witnessed graph is acyclic. Coherent actual shared revisions, default/datom feature graphs, nominal API allocation and predecessor-produced binding/container/resolver/queue plus reopen evidence remain pre-body checks; workspace patching alone proves none of these.

Terminal history and current active head readback are consistent. Engine commit/maintenance results retain committed-versus-refused meaning. Failure to persist observation after a native effect returns uncertainty, not clean failure/success. This requirement may need durable recovery from the Emitting phase even when the last write failed.

## Required proofs

- Repeated stop/resume generations, concurrent Resume/Launch/Adopt/Stop, stale receipts, duplicate requests and active head/hold correlation.
- Crash/failure at each reserve/intent/call/observe/persist/terminal-cleanup boundary, including both pane creation and harness resume; no duplicate native effects after uncertainty.
- Claude and Codex actual same-session resume in isolated capsule, original transcript/context/FlowId and this-attempt attachment proof. Capability help is not runtime success.
- Missing native capability (NotReady), missing transcript (NoTranscript), Awake and other pre-effect refusals versus possible-effect uncertainty; owned cleanup only.
- Exact current record reuse and every new/changed wire/persisted consumer, catalog admission, namespace allocation, frozen predecessor fixtures and readback. Shared Refusal remains byte-identical unless separately demonstrated necessary.
- No provenance field, no gate, no invented LaunchRequestId, no old abandoned patch/green, no claim partial harness support satisfies EVERY-flow migration.

## Total lifecycle admission — approved

Pending -> NotReady.FlowId; Active -> Awake.FlowId. Explicit Resume permits Stopped, Exited and Retired held rows as themselves, with verified original native session/transcript and FREE address admission, preserving FlowId and resuming Maintained. An occupied successor blocks; no displacement or automatic retired recovery. Known held lifecycle states never become UnknownFlow, which means absence of the held row. Missing native capability, missing transcript and possible-effect uncertainty remain distinct outcomes.

Pre-effect BindingRefusal was also removed: no source-verified pre-call subset was established. Observation failures before native emission use the finite ObservationUnavailable branch; post-effect binding categories remain ResumeEvidence.Binding. Actual field-specific diagnostics may accompany internal evidence through existing typed observation paths, but no broad string replaces the public state.
