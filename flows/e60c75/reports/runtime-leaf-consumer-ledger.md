# Exact runtime leaf consumer ledger

Only authored leaf names from `052-runtime-policy-shape.md:15-86` are used. Each row preserves the proposal spelling and gives observed 916 consumer anchors.

| Authored leaf | Observed symbol/location | Destination/activation | Oracle |
|---|---|---|---|
| ReminderPolicy.Firings | reminder firing/cancellation logic `flow-nexus/src/store/reminder.rs:25-55`; scanner `reminding.rs:15-16,93-99` | RuntimePolicy snapshot | firing count |
| ReminderPolicy.Scan | `reminding.rs:15-16,93-99` | RuntimePolicy snapshot | scan interval |
| ReminderPolicy.StopPoll | `store/reminder.rs:25-55` | RuntimePolicy snapshot | stop poll |
| DeliveryPolicy.Payload | `sending.rs:59-101` | RuntimePolicy send admission | payload boundary |
| DeliveryPolicy.Deadline | `sending.rs:1363` | RuntimePolicy send deadline | deadline refusal |
| DeliveryPolicy.ServingSlice | `send_tool.rs:708-810` | RuntimePolicy responder serving | slice boundary |
| DeliveryPolicy.InterruptedReplay | `send_tool.rs:909-955` | RuntimePolicy interrupted replay | replay boundary |
| RetryPolicy.FirstWait | reconnect loop `send_tool.rs:535-612` | RuntimePolicy reconnect | first wait |
| RetryPolicy.LongestWait | reconnect loop `send_tool.rs:535-612` | RuntimePolicy reconnect | cap |
| RetryPolicy.RetryMultiplier | reconnect loop `send_tool.rs:535-612` | RuntimePolicy reconnect | multiplier |
| HistoryPolicy.PageSize | `codex.rs:258-261` | RuntimePolicy Codex history | page size |
| HistoryPolicy.Pages | `codex.rs:258-261` | RuntimePolicy Codex history | page count |
| HistoryPolicy.RememberedTurns | `codex_turns.rs:72,159-174` | RuntimePolicy retained turns | retention |
| HistoryPolicy.ClaudeTail | `claude.rs:443` | RuntimePolicy Claude tail | tail bytes |
| AncestryPolicy.Processes | `caller.rs:172,302` | RuntimePolicy process ancestry | depth |
| AncestryPolicy.Threads | `caller.rs:172,302` | RuntimePolicy native-thread ancestry | depth |
| PollingPolicy.HeartbeatConfiguration | `heartbeat.rs:338` | RuntimePolicy heartbeat loop | interval |
| PollingPolicy.AgentStop | `observe_agent.rs:217` | RuntimePolicy observe-agent loop | stop interval |
| PollingPolicy.CompactionWindow | `compacting.rs:43,58-66` | RuntimePolicy compaction watch | window |
| TransportPolicy.SocketRead | socket read paths `lib.rs:768-784` | RuntimePolicy Nexus socket | read timeout |
| TransportPolicy.SocketWrite | socket write paths `lib.rs:768-784` | RuntimePolicy Nexus socket | write timeout |
| TransportPolicy.CodexExchange | `main.rs:254-256; codex.rs:60` | RuntimePolicy Codex adapter | exchange timeout |
| TransportPolicy.CurriculumExchange | `context.rs:50,128-129` | RuntimePolicy Curriculum adapter | exchange timeout |
| TransportPolicy.HerdrPrompt | `herdr/launch.rs:375` | RuntimePolicy Herdr launch | prompt timeout |
| TransportPolicy.HerdrCall | `herdr/launch.rs:411-412` | RuntimePolicy Herdr launch | call timeout |
| TitlePolicy.Attempts | `herdr/launch.rs:1447-1453` | RuntimePolicy title readiness | attempts |
| TitlePolicy.Interval | `herdr/launch.rs:1528-1579` | RuntimePolicy title readiness | interval |
| TitlePolicy.PaneRest | `herdr/launch.rs:2261-2279` | RuntimePolicy pane rest | rest |
| PanePolicy.SubmissionReads | `herdr/pane.rs:51-64` | RuntimePolicy terminal delivery | read count |
| PanePolicy.SubmissionInterval | `herdr/pane.rs:87-140` | RuntimePolicy terminal delivery | interval |
| PanePolicy.InterruptPresses | `herdr/pane.rs:368-405` | RuntimePolicy terminal delivery | press count |
| PanePolicy.InterruptWait | `herdr/pane.rs:368-405` | RuntimePolicy terminal delivery | wait |
| PanePolicy.ComposerLines | `herdr/pane.rs:87-140` | RuntimePolicy terminal composer | line count |
| PanePolicy.StoppedRest | `herdr/pane.rs:368-405` | RuntimePolicy terminal delivery | stopped rest |
| PanePolicy.RetractionLines | `herdr/pane.rs:368-405` | RuntimePolicy terminal delivery | retraction lines |
| FramePolicy.Nexus | `flow-nexus/src/lib.rs:1389` | RuntimePolicy Nexus frame boundary | inbound/outbound cap |
| FramePolicy.WebSocketHeader | `codex.rs:29,607-630` | RuntimePolicy WebSocket adapter | header cap |
| FramePolicy.WebSocketMessage | `codex.rs:30,519-528` | RuntimePolicy WebSocket adapter | message cap |
| FramePolicy.CurriculumReply | `context.rs:52,141` | RuntimePolicy Curriculum reply | reply cap |
| FramePolicy.HerdrEnvelopeAllowance | `composition.rs:181-205` | RuntimePolicy Herdr envelope | allowance |
| ParserPolicy.StructuralNodes | `flow-nexus/src/main.rs:55-62,361-368,508-515,625-632` | RuntimePolicy Nexus decoder only | node cap |
| ParserPolicy.StructuralDepth | same Nexus decoder sites | RuntimePolicy Nexus decoder only | depth cap |
| ParserPolicy.DatomFormDepth | same Nexus decoder sites | RuntimePolicy Nexus decoder only | form depth |
| ParserPolicy.CompositionSteps | same Nexus decoder sites | RuntimePolicy Nexus decoder only | step cap |
| ParserPolicy.CompositionDepth | same Nexus decoder sites | RuntimePolicy Nexus decoder only | composition depth |
| LaunchPolicy.Herdr | executable/path selection `herdr.rs:143-198` | RuntimePolicy launch | missing refusal |
| LaunchPolicy.FlowIdentity | identity executable selection `herdr.rs:143-198` | RuntimePolicy launch | missing refusal |
| LaunchPolicy.Hook | hook executable construction `herdr/launch.rs:484-496` | RuntimePolicy launch snapshot | missing refusal |
| LaunchPolicy.ClaudeHome | launch path selection `herdr.rs:143-198` | RuntimePolicy launch | missing refusal |
| LaunchPolicy.FlowDirectory | flow-directory selection `herdr.rs:143-198` | RuntimePolicy launch | path identity |
| LaunchPolicy.DefaultSession | session selection `sending.rs:485-568,waking.rs:1470-1477` | RuntimePolicy launch | missing refusal |
| EffortPolicy (12 EffortSelection coordinates) | selector `sending.rs:472-483`; profile `sending.rs:569-580`; wake `waking.rs:2691,2869`; readback `herdr/launch.rs:1923-1935,codex.rs:927-972` | RuntimePolicy complete Aspect×Layer table: Psyche/Mind/Field × Primary/Secondary/Tertiary/Quaternary | one unique value per coordinate; readback |
| DefaultContinuity | declaration `store/metaflow_declaration.rs:28-48`; launch fallback `store/successor.rs:164-176`; launch `store/metaflow.rs:237-245` | candidate meta config v6; resolve member then configured default | both absent Define succeeds/Launch NotConfigured |
| Existing HarnessProfiles | `store.rs:298,342`; retained Nexus `nexus_configuration.rs:21-40` | existing ConfigureNexus domain, not PanePolicy | profile present/missing error |
| Existing DefaultMinutes | `store.rs:1154-1205`; dispatch `store.rs:8677+` | existing family only; explicit configured value, no runtime literal fallback | absence/read failure refuses; explicit roundtrip |
| Existing LeaveOuts | `store.rs:1295-1421`; dispatch `store.rs:8677+` | existing family/harness domain | absence/read failure and wrong-harness refusal |

## Query coverage

Exact query scopes: `rg -n 'Firings|Scan|StopPoll|Payload|Deadline|ServingSlice|InterruptedReplay|FirstWait|LongestWait|RetryMultiplier|PageSize|Pages|RememberedTurns|ClaudeTail|Processes|Threads|HeartbeatConfiguration|AgentStop|CompactionWindow|SocketRead|SocketWrite|CodexExchange|CurriculumExchange|HerdrPrompt|HerdrCall|Attempts|Interval|PaneRest|SubmissionReads|SubmissionInterval|InterruptPresses|InterruptWait|ComposerLines|StoppedRest|RetractionLines|StructuralNodes|StructuralDepth|DatomFormDepth|CompositionSteps|CompositionDepth|DefaultSession|Effort|DefaultContinuity|Minutes|LeaveOut|HarnessProfile'` over immutable Flow916 workspace source. The proposal is the authoritative leaf-name list; observed locations are listed per leaf above.

## Exact symbol corrections

Observed symbols replacing broad anchors: Reminder `TASK_REMINDERS` `store/reminder.rs:27`; interval method `RulesMinutes::ruled_interval` `:34-50`; Effort `ChoosesEffort::effort_of` `sending.rs:474-483`; Retry `PacesReconnection::{FIRST_WAIT,LONGEST_WAIT,stopped_within}` `send_tool.rs:538-556` and doubling `respond_for` `:594-612`; Pane `WritesPane::{SUBMISSION_READS,SUBMISSION_SPACING,INTERRUPT_PRESSES,INTERRUPT_WAIT_MILLISECONDS,COMPOSER_LINES,REST_WAIT_MILLISECONDS}` `herdr/pane.rs:51-74`. These exact symbol names are the observed consumers; `RetryMultiplier` has no separate observed constant and is represented by the `wait = (wait * 2).min(Self::LONGEST_WAIT)` expression at `send_tool.rs:610`.

The previous `configure_runtime` caller statement is corrected in the adapters ledger: `lib.rs:2208` is fixture-only, and `store.rs:11083,11118,11686` are all under `#[cfg(test)] mod tests` beginning `store.rs:8871`.
