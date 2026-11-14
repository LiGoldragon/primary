# 052 policy validation — proposed exact domains

Core approved the leaf domains/arithmetic before bodies; source-width/name/unit verification remains required. This supplies the missing domains of the authored RuntimePolicy; it does not allocate names or change approved ownership. Acceptance applies to the fully resolved snapshot, at startup and live meta alike. Existing-family validators stay in force; the table below covers the new leaves, not an invented replacement for existing validation.

## Domains and every current leaf

`PositiveInteger` means canonical Integer in 1..=i64::MAX, additionally checked into the consumer's actual counter type before acceptance. No truncation or saturating conversion. Integer/usize representation ceilings are intrinsic, not policy defaults. Positive limits allow useful work; this change introduces no disabled state through zero.

| Exact leaves | Accepted domain |
|---|---|
| ReminderPolicy.Firings | PositiveInteger, checked usize |
| DeliveryPolicy.Payload | PositiveInteger, checked usize |
| HistoryPolicy.PageSize, Pages, RememberedTurns, ClaudeTail | PositiveInteger, checked usize; ClaudeTail is bytes |
| AncestryPolicy.Processes, Threads | PositiveInteger, checked actual depth counter |
| TitlePolicy.Attempts | PositiveInteger, checked actual attempt counter |
| PanePolicy.SubmissionReads, InterruptPresses, ComposerLines, RetractionLines | PositiveInteger, checked actual count counter; line counts remain lines |
| FramePolicy.Nexus, CurriculumReply | PositiveInteger, checked usize AND u32, the length-prefix representability bound |
| FramePolicy.WebSocketHeader, WebSocketMessage, HerdrEnvelopeAllowance | PositiveInteger, checked usize; no comparison against a character-count maximum |
| ParserPolicy.StructuralNodes, StructuralDepth | PositiveInteger, checked usize (both structural counters) |
| ParserPolicy.DatomFormDepth, CompositionSteps, CompositionDepth | PositiveInteger, checked i64 (all three Datom counters) |
| RetryPolicy.RetryMultiplier | Integer >= 1; checked arithmetic described below |
| ReminderPolicy.Scan, StopPoll; DeliveryPolicy.Deadline, ServingSlice, InterruptedReplay; RetryPolicy.FirstWait, LongestWait; PollingPolicy.HeartbeatConfiguration, AgentStop, CompactionWindow; TransportPolicy.SocketRead, SocketWrite, CodexExchange, CurriculumExchange, HerdrPrompt, HerdrCall; TitlePolicy.Interval, PaneRest; PanePolicy.SubmissionInterval, InterruptWait, StoppedRest | PositiveInteger milliseconds; checked u64 conversion and checked native Duration construction |
| LaunchPolicy.Herdr, FlowIdentity, Hook, ClaudeHome | Nonempty absolute native paths with no NUL; executables are explicit absolute path spellings, not PATH search names. Existence, file/directory kind and access are typed operational observations, never validation filesystem effects or a second configured fallback. ClaudeHome is lexically an absolute path; its actual directory kind is observed only at the operation boundary. |
| LaunchPolicy.FlowDirectory | One nonempty normal relative path component: neither dot nor parent, no separator or NUL; append to existing configured SourceRoot |
| LaunchPolicy.DefaultSession | Nonempty native session name containing none of NUL, CR or LF; existing composition validation immediately after effort checks rejects CR/LF |
| EffortPolicy | Exactly one entry for every existing Aspect/Layer pair; no duplicates or omitted pairs. Effort uses existing String, nonempty and containing none of NUL, CR or LF (existing composition.rs296–300 rejects CR/LF); no guessed supported-value enum or fallback. Native rejection remains typed operational evidence. |
| DefaultContinuity | None or Some(existing Continuity); None is valid configuration, not a missing required scalar |

The same five positive counter domains apply at translator bootstrap and each adapter boundary, using that boundary's explicit values. Each stage gets its own value; no hidden upper policy cap is reinstated. FrameBytes at an actual u32-prefixed adapter boundary has the same checked usize/u32 domain as Nexus frames. WebSocket values do not acquire a fictitious u32 framing constraint.

## Cross-field and arithmetic rules

1. RetryPolicy.FirstWait <= LongestWait. Multiplier1 deliberately means constant backoff. Compute each next wait as min(current * multiplier, LongestWait) through checked/division-bounded arithmetic that cannot overflow; no wraparound or hidden maximum.
2. No artificial ordering is imposed between independent parser limits, between header/message limits, or between independently owned adapter and Nexus settings. A valid small budget can refuse a particular request. That is exhaustion, not invalid configuration.
3. Chosen limits never waive retained terminal/Herdr/textual-Codex constraints. Validate constructed emissions against each constraint at its actual unit/consumer. If a configurable leaf itself expresses that same constrained quantity, its accepted range intersects that exact witnessed constraint. A byte allowance is not compared with a character maximum.
4. Checked duration-to-deadline arithmetic remains an operation-time typed refusal when the actual current clock value cannot represent the sum. Configuration validity cannot promise future clock arithmetic. No clamping or replacement duration.
5. Allocation sizes, derived lengths, counter arithmetic and conversions are checked before allocation/emission. Configuration acceptance does not guarantee resources are available; actual allocation/I/O failures remain existing typed operational failures, not knobs.

## Typed validation result and generation boundary

The implementation must generate one `ConfigurationField` variant per actual setting from the SAME authored setting declaration used for ConfigurationChange, including each RuntimePolicy leaf. It must not maintain a parallel string field registry. Existing keyed settings retain their typed key alongside the field identity.

Proposed vocabulary (names subject to ordinary allocation, semantics fixed by this proposal):

```ethos
ConfigurationValidationFailure.[
   MissingRequired.ConfigurationField
   Duplicate.ConfigurationField
   InvalidValue.{ ConfigurationField ValueFailure }
   InvalidRelation.{ ConfigurationField ConfigurationField }
   StartupOnly.ConfigurationField ]
ValueFailure.[ NonPositive Unrepresentable InvalidPath InvalidName ]
```

The duplicate-key and aggregate/individual-overlap cases preserve their actual typed key/field evidence through the existing key vocabulary; exact generated declarations must include it, not discard keys into strings. `ConfigurationField` is generated, not a manually authored second enum. `InvalidRelation` covers the retry ordering with its exact two fields. Native filesystem/session failures are not misreported as validation success or converted to default values.

Validation produces only the already-approved sealed resolved snapshot, never writes, emits, repairs, opens for mutation, or activates partially. Reject the whole startup/meta change set on any failure; prior committed configuration is unchanged. Startup-only placement attempts name the exact setting and refuse. The public reply wraps this typed result in the existing appropriate configuration/startup response, not a convenient unrelated shared Refusal extension.

## Test oracle per row

For every required scalar: absent from startup and Memory -> MissingRequired; absent startup with stored valid value -> preserved; present valid -> exact replacement; zero/negative -> NonPositive; conversion overflow -> Unrepresentable, all with the exact field and no committed change. Boundary1 and largest representable values are validation tests, not permission to allocate huge buffers in tests.

Paths/names: empty, relative executable/home, parent/compound child component and NUL refuse; valid explicit values are passed unchanged. Retry relation inversion refuses the entire set; multiplier1 is accepted. DefaultContinuity None remains accepted; member/default both None refuses Launch, not Define/startup. Individual parser exhaustion is tested with the other four budgets ample. Existing profile/minutes/leave-out family oracles stay in their source-row ledger. Fault/compile/capsule execution follows body clearance; this is the prebody acceptance contract.

## Remaining precise inputs

Exact pinned counter widths are usize/usize/i64/i64/i64 for the five stages. Retained emission constraints are Herdr encoded1MiB bytes including allowance and Codex1<<20 characters (composition.rs181–204), checked at their own consumers; chosen WebSocket byte bounds remain independent. Effort source pins now establish one selector and derived LaunchProfile field; proposed complete Aspect/Layer table is in the runtime-policy artifact for Core judgment. Existing Herdr session-name restrictions, actual native count counter types and any exact same-unit fixed limit must be cited by the bounded consumer ledger; an unstated external assumption cannot become a new bound. Those spelling/source checks do not authorize a new fallback or additional policy family.
