# Receipt: signal-flow 4.0.0 (Flow gaps G8 and G9, contract side)

- Repo: LiGoldragon/signal-flow, main 5ca97cee791df0a63c14ae665e9bd7ad15f1f2b0 (parent f881ab3, 3.0.0). `git ls-remote origin main` returned 5ca97ce after the push.
- Version: 4.0.0 (wire change: three new Query variants, three new Response variants).
- Generation: ethos-zero built at the pinned rev 4bf73ca; it first reproduced the committed 3.0.0 `src/generated/signal.rs` byte for byte, then generated the new file. build.rs freshness check passes.
- Tests: `cargo test --features datom`: 9 passed, 0 failed (5 existing, 4 new). `cargo test` without the feature: builds, 0 tests (contract tests are datom-gated).
- Not touched: flow and meta-signal-flow repos. The Nexus side (Replace ordering, LaunchStatus, Observe stream) is the later task.

## New ethos lines, whole

```
; Flow ordinary Signal.
;
; Replace carries a StartRequest whose LaunchProfile names the replaced
; flow as its predecessor. The successor is launched; once it has
; Started, the predecessor is Stopped and taken out of receiving, and
; only then is the successor routable. Reaping belongs to the refresh
; event: no state holds both flows routable. Replaced carries the
; stopped predecessor's FlowId and the successor's Started.
; ReplaceRejection names why no replacement took place; after
; ReapRefused the successor is not routable.
;
; LaunchStatus answers once for a LaunchRequestId: LaunchPending with
; the LaunchAttempt and its phase while the launch runs, else its
; outcome, Started, Replaced, StartRejected or ReplaceRejected.
;
; Observe.Launch opens an exchange that goes on answering: on open it
; sends what LaunchStatus would, then one LaunchPending frame for every
; later phase change, and it ends after the frame carrying the
; outcome. Nothing is re-read on a timer; a launch that does not move
; sends nothing. Every other query is answered with exactly one frame.

Signal
```

The queries line, the responses line and the types line, as now written (each replaced its old line whole):

```
[ Start.StartRequest Restart.RestartRequest ResolveRecipient.RecipientResolutionRequest Send.SendRequest Stop.StopRequest List.ListRequest Replace.StartRequest LaunchStatus.LaunchRequestId Observe.ObserveSelection ]
[ Started.Started LaunchPending.LaunchAttempt StartAmbiguous.PromptDeliveryIntent Restarted.Restarted RecipientResolved.FlowNode Sent.SendOutcome Stopped.FlowId Listed.FlowList StartRejected.StartRejection RestartRejected.RestartRejection RecipientResolutionRejected.RecipientResolutionRejection SendRejected.SendRejection StopRejected.StopRejection ListRejected.ListRejection Replaced.Replaced ReplaceRejected.ReplaceRejection LaunchStatusRejected.LaunchStatusRejection ]
[ FlowId.String SessionId.String TurnId.String FlowType.String Generation.Integer EndpointPath.String HerdrSessionName.String HerdrAgentName.String HerdrWorkspaceId.String HerdrPaneId.String HerdrTerminalId.String LaunchRequestId.String SourcePath.String SourceSha256.String SkillName.String ModelName.String Effort.String RememberingDepth.Integer SystemPromptBundleFile.String InstructionPrompt.String FirstPromptBody.String FirstPromptText.String PromptSha256.String BareInput.String PresentationMarker.String PresentationReadUnixMilliseconds.Integer NativeSessionId.String NativeTurnId.String ReceiptSha256.String TranscriptDevice.String TranscriptInode.String TranscriptByteOffset.Integer TranscriptPrefixSha256.String TranscriptRootDevice.String TranscriptRootInode.String NativeSkillPath.String NativeSkillSha256.String FlowAspect.[ Psyche Mind Field ] PowerLevel.[ High Medium Low UltraLow ] LaunchSource.{ SourcePath SourceSha256 } RememberedFlow.{ FlowId RememberingDepth } LaunchProfile.{ LaunchRequestId Vector<LaunchSource> Vector<SkillName> FlowAspect PowerLevel HarnessKind ModelName Effort Option<FlowId> Vector<RememberedFlow> HerdrSessionName SystemPromptBundleFile InstructionPrompt } TargetReceiptRequest.{ LaunchRequestId PromptSha256 } FirstPromptPayload.{ FirstPromptBody PromptSha256 FirstPromptText } ComposedLaunch.{ LaunchProfile FirstPromptPayload TargetReceiptRequest } HerdrPaneBinding.{ LaunchRequestId HerdrSessionName HerdrAgentName HerdrWorkspaceId HerdrPaneId HerdrTerminalId } NativeLaunchIntent.{ LaunchRequestId PromptSha256 HarnessKind ModelName Effort Vector<SkillName> } NativeLaunchBinding.{ LaunchRequestId FlowId NativeSessionId HarnessKind HerdrPaneBinding } RegistrationAcknowledgement.{ LaunchRequestId FlowId NativeSessionId HerdrPaneBinding } NativeTranscriptCursor.{ NativeSessionId HarnessKind TranscriptDevice TranscriptInode TranscriptByteOffset TranscriptPrefixSha256 } NativeTranscriptAbsence.{ NativeSessionId HarnessKind TranscriptRootDevice TranscriptRootInode } NativeTranscriptBoundary.[ Existing.NativeTranscriptCursor Absent.NativeTranscriptAbsence ] NativeSkillSelection.{ SkillName NativeSkillPath NativeSkillSha256 } PromptDeliveryIntent.{ LaunchRequestId PromptSha256 FlowId NativeSessionId HarnessKind ModelName Effort Vector<NativeSkillSelection> HerdrPaneBinding NativeTranscriptBoundary } NativeTargetReceipt.{ LaunchRequestId PromptSha256 FlowId NativeSessionId NativeTurnId ReceiptSha256 ModelName Effort Vector<NativeSkillSelection> } PromptDeliveryResult.[ Observed.NativeTargetReceipt Ambiguous.PromptDeliveryIntent ] LaunchAttemptPhase.[ Reserved NativeLaunchIntentRecorded NativeBound RegistrationAcknowledged PromptIntentRecorded PromptObserved PromptAmbiguous ] LaunchAttempt.{ LaunchRequestId LaunchProfile PromptSha256 OriginClue LaunchAttemptPhase Option<NativeLaunchIntent> Option<NativeLaunchBinding> Option<RegistrationAcknowledgement> Option<PromptDeliveryIntent> Option<PromptDeliveryResult> } LaunchAttemptReservation.[ Reserved.LaunchAttempt Existing.LaunchAttempt Conflict ] OriginClue.{ FlowId SessionId TurnId } StartRequest.{ LaunchProfile OriginClue } RestartRequest.{ FlowId OriginClue } RecipientResolutionRequest.FlowId SendRequest.{ FlowId BareInput } PresentationReceipt.{ FlowId HerdrPaneId PresentationMarker PresentationReadUnixMilliseconds } SendOutcome.[ Accepted.FlowId Presented.PresentationReceipt ] StopRequest.FlowId ListRequest.{} HarnessKind.[ Codex Claude ] RouteReadiness.[ Ready Parked ] EndpointSelection.[ Available.{ EndpointPath RouteReadiness } Unavailable ] HerdrRoute.{ HerdrSessionName HerdrAgentName HerdrPaneId HerdrTerminalId } HerdrRouteSelection.[ Available.HerdrRoute Unavailable ] FlowLifecycle.[ Pending Active Stopped ] FlowNode.{ FlowId SessionId HarnessKind EndpointSelection HerdrRouteSelection OriginClue FlowLifecycle } FlowList.Vector<FlowNode> Started.{ FlowId SessionId OriginClue } Restarted.{ FlowId SessionId Generation } StartRejection.[ CompositionRefused LaunchRequestConflict LaunchPersistenceRefused NativeLaunchRefused BindingRefused RegistrationRefused IntentPersistenceRefused OriginUnavailable ] RestartRejection.[ ProvenanceMismatch UnknownFlow ResumeRefused ] RecipientResolutionRejection.[ UnknownFlow FlowUnavailable ] SendRejection.[ UnknownFlow FlowStopped RouteUnavailable DeliveryRefused PersistenceRefused ] StopRejection.[ UnknownFlow AlreadyStopped RouteUnavailable CloseRefused PersistenceRefused ] ListRejection.[ PersistenceRefused ] Replaced.{ FlowId Started } ReplaceRejection.[ PredecessorAbsent UnknownPredecessor PredecessorStopped LaunchRefused.StartRejection ReapRefused.StopRejection ] ObserveSelection.[ Launch.LaunchRequestId ] LaunchStatusRejection.[ UnknownLaunchRequest PersistenceRefused ] ]
```

Additions within them: queries `Replace.StartRequest LaunchStatus.LaunchRequestId Observe.ObserveSelection`; responses `Replaced.Replaced ReplaceRejected.ReplaceRejection LaunchStatusRejected.LaunchStatusRejection`; types `Replaced.{ FlowId Started } ReplaceRejection.[ PredecessorAbsent UnknownPredecessor PredecessorStopped LaunchRefused.StartRejection ReapRefused.StopRejection ] ObserveSelection.[ Launch.LaunchRequestId ] LaunchStatusRejection.[ UnknownLaunchRequest PersistenceRefused ]`.

## Concrete datoms under test

```
LaunchStatusRejected.PersistenceRefused
LaunchStatusRejected.UnknownLaunchRequest
LaunchStatus.request-8
Observe.Launch.request-8
Replaced.{ fac697 { 908786 session-2 { fac697 session-1 turn-2 } } }
ReplaceRejected.LaunchRefused.NativeLaunchRefused
ReplaceRejected.PredecessorAbsent
ReplaceRejected.PredecessorStopped
ReplaceRejected.ReapRefused.CloseRefused
ReplaceRejected.UnknownPredecessor
Replace.{ { request-8 [] [ spirit ] Field High Claude opus-5-5 high Some.fac697 [] messaging-build /workspace/bundles/flow.md «Carry on from fac697.» } { fac697 session-1 turn-2 } }
Replace.{ { request-8 [] [ spirit main-flow ] Field High Claude opus-5-5 high Some.fac697 [] messaging-build /workspace/bundles/flow.md «Carry on from fac697.» } { fac697 session-1 turn-2 } }
```

## Choices a reviewer may overturn

- Replace reuses StartRequest rather than a duplicate ReplaceRequest; a missing predecessor is refused at runtime as ReplaceRejected.PredecessorAbsent, since the type allows None.
- LaunchStatus answers with existing responses (LaunchPending.LaunchAttempt carries the phase; Started, Replaced, StartRejected, ReplaceRejected carry the outcome) instead of a new status response.
- The subscription follows signal-orchestrate's Observe shape (Observe.ObserveSelection, the exchange itself is the subscription). Its frames are LaunchPending per phase change and one closing outcome frame, not a new Observed response.

## Sources

- /home/li/primary/flows/38de5b/reports/audit-flow.md (G8, G9, Witnessed state, Unknowns)
- /home/li/primary/Vision/flowNexus.md, /home/li/primary/Vision/nexus.md
- /git/github.com/LiGoldragon/signal-orchestrate/ethos (Observe pattern, e722119)
