# 052 missing-policy resolved family — schema proposal

Proposed data shape for judgment; no allocation, generated source or body. Existing ConfigureNexus ten fields and all existing configured families retain their values. This new family holds only policies missing from those families in916. Startup/meta per-value changes are generated from these declarations once; the persisted resolved row uses the same leaf types. Groups describe consumers, not separate stores. Every field is supplied explicitly or start refuses; no literal value below is a seed.

DefaultContinuity is an explicit optional leaf in this same new resolved family, using existing Continuity; it is not a required operational-policy value. Member Option preserves historical explicit values as Some. Existing Minutes, heartbeat period/recipients, source root, endpoint/model sets, harness profiles, flags/leave-outs, lease, investigation and thresholds are NOT duplicated here.

## Proposed Ethos

```ethos
Library
[ :meta_signal_flow:Continuity
  :flow_ethos:[ Aspect Layer ]
  :signal_flow:Effort ]          ; imports: existing version-zero continuity
[ DurationMilliseconds.Integer          ; types: unit-bearing configured durations
  ByteCount.Integer
  CharacterCount.Integer
  LineCount.Integer
  ItemCount.Integer
  DepthCount.Integer
  RetryMultiplier.Integer
  ExecutablePath.String
  DirectoryPath.String
  DirectoryName.String
  SessionName.String
  ReminderPolicy.{                      ; task reminder and cancellation scans, not accepted task deadlines
     Firings.ItemCount
     Scan.DurationMilliseconds
     StopPoll.DurationMilliseconds }
  DeliveryPolicy.{                      ; native prompt limits and send coordination
     Payload.ByteCount
     Deadline.DurationMilliseconds
     ServingSlice.DurationMilliseconds
     InterruptedReplay.DurationMilliseconds }
  RetryPolicy.{                         ; responder reconnect policy
     FirstWait.DurationMilliseconds
     LongestWait.DurationMilliseconds
     RetryMultiplier }
  HistoryPolicy.{                       ; bounded transcript/history reads and retained completed turns
     PageSize.ItemCount
     Pages.ItemCount
     RememberedTurns.ItemCount
     ClaudeTail.ByteCount }
  AncestryPolicy.{                      ; process and native-thread ancestry searches
     Processes.DepthCount
     Threads.DepthCount }
  PollingPolicy.{                       ; polling intervals where916 still polls
     HeartbeatConfiguration.DurationMilliseconds
     AgentStop.DurationMilliseconds
     CompactionWindow.DurationMilliseconds }
  TransportPolicy.{                     ; consumer-specific waits, not one ambiguous timeout
     SocketRead.DurationMilliseconds
     SocketWrite.DurationMilliseconds
     CodexExchange.DurationMilliseconds
     CurriculumExchange.DurationMilliseconds
     HerdrPrompt.DurationMilliseconds
     HerdrCall.DurationMilliseconds }
  TitlePolicy.{                         ; title/readiness observations
     Attempts.ItemCount
     Interval.DurationMilliseconds
     PaneRest.DurationMilliseconds }
  PanePolicy.{                          ; existing terminal delivery choices
     SubmissionReads.ItemCount
     SubmissionInterval.DurationMilliseconds
     InterruptPresses.ItemCount
     InterruptWait.DurationMilliseconds
     ComposerLines.LineCount
     StoppedRest.DurationMilliseconds
     RetractionLines.LineCount }
  FramePolicy.{                         ; configured operational bounds checked against any retained maxima
     Nexus.ByteCount
     WebSocketHeader.ByteCount
     WebSocketMessage.ByteCount
     CurriculumReply.ByteCount
     HerdrEnvelopeAllowance.ByteCount }
  ParserPolicy.{                        ; ONLY Nexus-owned decoding, not standalone adapters
     StructuralNodes.ItemCount
     StructuralDepth.DepthCount
     DatomFormDepth.DepthCount
     CompositionSteps.ItemCount
     CompositionDepth.DepthCount }
  LaunchPolicy.{                        ; missing executable/location/session policy only
     Herdr.ExecutablePath
     FlowIdentity.ExecutablePath
     Hook.ExecutablePath
     ClaudeHome.DirectoryPath
     FlowDirectory.DirectoryName
     DefaultSession.SessionName }
  EffortSelection.{ Aspect Layer Effort } ; one configured value for each existing aspect/layer pair
  EffortPolicy.Vector<EffortSelection>    ; complete, unique twelve-pair table; no fallback
  RuntimePolicy.{                       ; ONE resolved persisted record
     ReminderPolicy
     DeliveryPolicy
     RetryPolicy
     HistoryPolicy
     AncestryPolicy
     PollingPolicy
     TransportPolicy
     TitlePolicy
     PanePolicy
     FramePolicy
     ParserPolicy
     LaunchPolicy
     EffortPolicy
     DefaultContinuity.Option<Continuity> } ]
[]                                      ; traits: none introduced by this data declaration
[]                                      ; associations
```

These semantic wrapper names are proposed. Their Rust forms must use the ordinary generator's real inline/newtype lowering, not bespoke attributes or independent hand-maintained shapes. Positive/zero semantics and duration range are validated per field; an Integer by itself is not validation.

## Remaining row mappings requiring explicit completion

- Proposed EffortPolicy owns the previously address-derived effort. Exact916 sending.rs472–483 selects strings by Aspect/Layer; sending.rs569–580 and waking.rs2691,2869 materialize LaunchProfile.effort, consumed by herdr/launch.rs1923–1935. Existing signal Effort.String (ethos309) is reused. Require exactly one value per existing Aspect/Layer pair (3 aspects x4 layers); missing/duplicate pair refuses resolved configuration. No second member/model setting or precedence is evidenced. Each future Launch/wake/refresh snapshots this table and carries the selected effort unchanged in its existing LaunchProfile; old attempts retain their snapshot, active seats are unchanged. This new table replaces ChoosesEffort literals, not the public profile field. Core approved this exact twelve-pair policy; unsupported native values fail truthfully without substitution, and any newly discovered explicit selector must be brought back for precedence judgment before wiring.
- Required configured harness profiles remove delivery.rs absent-profile defaults; values remain in existing HarnessProfiles, not PanePolicy duplicates.
- Herdr/Codex transport maxima specifically retained by ruling stay checked constraints. Envelope allowance is chosen policy. Other frame/parser/send/history/ancestry bounds are configuration, not invariants inferred from use.
- SourceRoot and the flow-directory child name are different facts. SourceRoot stays existing live configuration; FlowDirectory names the currently literal `flows` segment. Existing seats retain their actual workspace/transcript identity; changing future-launch policy cannot move them.
- Herdr fixture Codex paths have no production consumer after configured overlay. Remove placeholder construction from production; fixture values stay test data, not new policy fields.
- Typed process UID observation is kernel evidence; failure refuses, no configured UID or zero fallback.
- Runtime error fallbacks other than the ruled failed leave-outs read are a separate audit, not new startup knobs.
- BootstrapTextBudget is separate translator-owned startup input, approved in 052-startup-envelope.md. It uses the same Datom lexical rules to read five fixed integer fields, then budget-decodes the full envelope. Runtime ParserPolicy is committed live policy; neither supplies a fallback for the other.

## Inventory source/consumer mapping

ReminderPolicy: store/reminder.rs25–55 and reminding.rs15–16,93–99. DeliveryPolicy: sending.rs59–101, send_tool.rs708–810,909–955 and sending.rs1363 deadline. RetryPolicy: send_tool.rs535–612. HistoryPolicy: codex.rs258–261, codex_turns.rs72,159–174, claude.rs443. AncestryPolicy: caller.rs172,302. PollingPolicy: heartbeat.rs338, observe_agent.rs217, compacting.rs43,58–66. TransportPolicy: lib.rs768–784, main.rs254–256, codex.rs60, context.rs50,128–129, herdr/launch.rs375,411–412, herdr.rs143–198. TitlePolicy: herdr/launch.rs1447–1453,1528–1579,2261–2279. PanePolicy: herdr/pane.rs51–64,87–140,368–405. FramePolicy: lib.rs1389, codex.rs29–30, context.rs52,141, composition.rs181–205. ParserPolicy: Nexus-owned decoder sites only. Ordinary/meta main, composer and hook parser/frame rows belong to explicit adapter Invocation/HookConfiguration settings, not this persisted record. LaunchPolicy: herdr.rs143–198, sending.rs485–568, waking.rs1470–1477. Paths relative to crates/flow-nexus/src except explicitly named client/hook sites; all evidence at immutable916.

This is a concrete candidate shape, not yet the EVERY-row closure matrix. Reader must check each leaf against the inventory for omissions, already-configured duplicates, conflated consumers and derived facts before Core judgment/allocation. The full row matrix must include existing-family mappings as well as these new fields, validation, missing/invalid refusal, live activation and test oracle.

Adapter placement correction: structural nodes, structural depth, Datom-form depth, composition steps and composition depth are distinct limits at every consuming parser. Standalone client/composer/hook values and client response-frame bytes are explicit process invocation configuration, not entries in RuntimePolicy. WebSocket header/message limits in the Nexus Codex proxy are chosen policy (no external-limit evidence); the textual Codex maximum remains the separately ruled fixed constraint.
