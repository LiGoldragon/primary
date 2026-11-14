# Flow 0.51.2 Memory inventory, for designing Exported.Record

Worktree `/git/worktrees/flow-0513-restart-31724f` @ 7773fe0. Every path below is relative to `crates/flow-nexus/src/` unless it says otherwise.
Short forms: **S** = signal-flow 79ca533 `ethos/signal.ethos`; **M** = meta-signal-flow 421a865 `ethos/signal.ethos`; **L** = `crates/flow-ethos/ethos/library.ethos`; **G:x** = `src/generated/x.rs` (flow-nexus's own ethos).
"Local" means a store-local Rust struct that derives only rkyv. "Wire✓" means a generated ethos type that derives `datom_codec::Datomizable` + `Composing`.

## 0. Which tables exist (observed)

- 48 live `flow_nexus_*` tables. They are `RUNNING_TABLES` (20, store.rs:191-212), `RUNNING_ADDED_TABLES` (1, store.rs:213) and `ADDED_LATER_TABLES` (27, store.rs:225-253).
- The configuration-only subset is store.rs:182-189 and 256-265.
- `RETIRED_TABLES` (6: meta_module_configuration, start_bundles, metaflow_refreshes, meta_threshold_configuration, landings, refresh_due) are dropped at open (store.rs:149-180, `drop_retired_tables` store.rs:8288). The export does not carry them.
- Every family is registered in `open_configured_in_place` (store.rs:4912-5000). The struct fields are listed at store.rs:4126-4163.
- On disk, each table is redb `TableDefinition<String, &[u8]>`. The key is the `RecordKey` text and the value is the plain rkyv archive of the record. Witnesses: store.rs:280-281 and 8490-8498 (decodes `FlowStoreState` directly), store.rs:5925-5935 (raw launch-attempt archives).

**Datom status (observed in the manifests; not built):**
- Generated types carry `#[cfg_attr(feature="datom", derive(Datomizable, Composing))]`:
  - signal.rs: 122 of 122 types.
  - meta-signal-flow: 98 of 98.
  - flow-ethos: 42 of 42.
  - flow-nexus G:*: all of them.
- The `datom` feature is on in each crate:
  - flow-nexus: `default=["datom"]` (crates/flow-nexus/Cargo.toml:10).
  - meta-signal-flow: `features=["datom"]` (crates/flow-nexus/Cargo.toml:22).
  - flow-ethos: `features=["datom"]` (Cargo.toml:14).
  - signal-flow: switched on through meta-signal-flow's `datom = [... "signal-flow/datom" ...]` (meta Cargo.toml:14). That signal-flow therefore compiles with datom is an inference from Cargo feature unification.
- No store-local struct derives Datomizable. A grep of store.rs and store/ finds only `use` lines (queue_delivery.rs:2777, send_v32.rs:11).

## 1. Family table

Abbreviations: LRID = launch request id; Addr = `Address{Aspect Topic Layer}` (L:63). The key column gives the RecordKey. "Settled vs not" names the field that shows it.

| # | table `flow_nexus_…` | record type: fields | key | scope | native provenance | in-flight? settled vs not | datom |
|---|---|---|---|---|---|---|---|
| 1 | flows | `FlowRecord` (store.rs:432): flow_id String, flow_type String, origin `Origin` (S:379, `Flow.FlowOrigin{FlowId SessionId}`/Unbound), thread_id Option<String>, harness_kind `HarnessKind` (L), endpoint_selection `EndpointSelection` (S:383, EndpointPath+RouteReadiness), lifecycle local `FlowLifecycle` (store.rs:1442: Pending Active Stopped Retired Exited), generation u64 | FlowId (store.rs:1472-1475) | per-flow. The origin is cross-flow: it names the parent flow and its session | yes: thread_id (native session), harness_kind, origin.session_id, endpoint path | yes: `lifecycle=Pending` is a launch not yet confirmed. Active means live. Stopped/Retired/Exited mean ended | Local wrapper. Fields are Wire✓ except the local FlowLifecycle (mirrors S FlowLifecycle) |
| 2 | native_owner_proofs | `NativeOwnerProofRecord` (store.rs:506): flow_id, proof `NativeOwnerProof` (store.rs:445): process_id i64, process_user_id i64, process_start_token String, host_id, boot_id, harness_kind, native_session_id | FlowId (store.rs:511-514) | per-flow | yes: process identity, host and boot ids, harness, native session | no. It is a witness that is valid for one host boot (doc store.rs:443). Liveness is computed, not stored (store.rs:570-611) | Local |
| 3 | state | `FlowStoreState` (store.rs:1604): next_flow_number u64 | "identity" (store.rs:1618-1621, 271) | global singleton | no | no | Local |
| 4 | metaflows | `StoredMetaflow` (store.rs:660){metaflow `Metaflow`}. Metaflow (L:64-67) = {Address, State[Awake.FlowId Asleep], Past Vector<FlowId>, Queue Vector<QueueEntry{LogicalDeliveryId SentBy Delivery Message}>} | Address (store.rs:664-668; key text `address_record_key` store.rs:7791) | per-address. It names the current flow and all past flows, and its queue entries name their senders (SentBy) | no | partly: Queue holds undelivered entries, and State=Awake names the live flow | Local wrapper over Wire✓ Metaflow |
| 5 | metaflow_processes | `StoredMetaflowProcess` (store.rs:1000): process `Process{Pid Started}` (L:69), address | Address (store.rs:1005-1008). The doc comment says "indexed by PID" (store.rs:997), but the key code uses the Address | per-address | yes: pid and start token | live binding, with no settled field | Local over Wire✓ |
| 6 | metaflow_locks | `StoredMetaflowLock` (store.rs:1013){lock `Lock{Sender Address Until}`} (L:68) | recipient Address (store.rs:1017-1020) | cross-address: Sender is the sender's address, Address is the recipient | no | yes: the row exists while the lock is held. `Until` is its expiry (Unix seconds); removal is a retraction (address_hold.rs:372-392) | Local over Wire✓ |
| 7 | configuration | `FlowStoreConfiguration` (store.rs:1628): ordinary_socket_path, meta_socket_path | "configured" (store.rs:1672-1675) | global configuration | no | no | Local |
| 8 | runtime_configuration | `RuntimeConfiguration` (store.rs:369): source_root, stable_codex and next_codex as local `CodexEndpointConfiguration` (store.rs:376: client_path, home, socket, model_names) | "runtime" (store.rs:425-429) | global configuration | Codex endpoint paths and model names | no | Local. It mirrors `flow_ethos::CodexEndpoint` (L), and conversions exist at store.rs:383-403 |
| 9 | herdr_routes | `FlowHerdrRouteRecord` (store.rs:1591): flow_id, route `HerdrRoute{HerdrSessionName HerdrAgentName HerdrPaneId HerdrTerminalId}` (S:385) | FlowId (store.rs:1596-1600) | per-flow | yes: Herdr session, agent, pane and terminal | no | Local over Wire✓ |
| 10 | launch_attempts | `StoredLaunchAttempt` (store.rs:1681): attempt `LaunchAttempt` (S:370: LRID, LaunchProfile (S:349, with Address, ModelName, Effort, flow_id_option, HerdrSessionName, InstructionPrompt…), PromptSha256, Origin, LaunchAttemptPhase, Option<NativeLaunchIntent>, Option<NativeLaunchBinding{LRID FlowId NativeSessionId HarnessKind HerdrPaneBinding}>, Option<RegistrationAcknowledgement>, Option<PromptDeliveryIntent>, Option<PromptDeliveryResult>), context `LaunchContext` (G:starter; starter.ethos:61 [Modules / BeforeModules]) | LRID (store.rs:1686-1690) | belongs to a launch. Its flow is reached through `native_launch_binding_option.flow_id`, which is None before NativeBound. Cross-flow via Origin (the requester) | yes: native session, harness, model, effort, Herdr pane/workspace/terminal, transcript boundary | yes: `launch_attempt_phase` (S:369, Reserved…PromptObserved/PromptAmbiguous). Settled exactly when a launch_outcomes row exists for the same LRID | Local wrapper over Wire✓ |
| 11 | launch_panes | `StoredLaunchPane` (store/created_pane.rs:9): pane `HerdrPaneBinding` (S:357: LRID, HerdrSessionName, HerdrAgentName, HerdrWorkspaceId, HerdrPaneId, HerdrTerminalId), harness_start_requested bool, orphaned bool | LRID (created_pane.rs:15-18) | belongs to a launch | yes: Herdr ids | yes: one-shot pane. Recoverable when `harness_start_requested && !orphaned` (created_pane.rs:79) | Local over Wire✓ |
| 12 | launch_outcomes | `StoredLaunchOutcome` (store.rs:2514): launch_request_id, launch_outcome `LaunchOutcome` (G:memory:5: Started.LaunchedRecord{FlowId SessionId Origin} / Replaced.ReplacedRecord{FlowId LaunchedRecord} / StartRejected / ReplaceRejected) | LRID (store.rs:2519-2523) | belongs to a launch. Replaced is cross-flow: it names the predecessor FlowId and the launched FlowId | SessionId (native session) | no: this is the settlement itself | Local wrapper over Wire✓ (G:memory) |
| 13 | replacements | `Replacement` (G:memory:16): launch_request_id, predecessor String (a FlowId) | LRID (store.rs:3434-3438) | cross-flow: the predecessor's FlowId plus the successor reached through the launch | no | yes: a replacement under way. Asserted at store.rs:6740-6744, withdrawn by retraction at store.rs:6747-6755. `held_successor` treats it as settled once launch_outcome=Replaced (store.rs:6773-6795) | Wire✓ (the row type itself) |
| 14 | roles | `StoredRole` (store.rs:1565){caller `Caller{FlowId Aspect PowerLevel ModelName}`} (S:532) | FlowId (store.rs:1569-1573) | per-flow | model name | no | Local over Wire✓ |
| 15 | quarantined_launch_attempts | `QuarantinedLaunchAttempt` (store.rs:2288): launch_request_id, quarantine_number u64, archive Vec<u8>, shape local `ArchivedLaunchAttemptShape` (store.rs:2274) | "LRID/n" (store.rs:2296-2303) | belongs to a launch. The flow is inside opaque bytes | opaque | no: set aside at open | Local, raw bytes |
| 16 | deliveries | `StoredDelivery` (store/delivery.rs:33){delivery `Delivery{DeliveryId FlowId InterruptWitness DeliveryGrade}`} (M:384) | DeliveryId (delivery.rs:38-40) | per-flow (the recipient) | no | no: written once the pane delivery settles (doc delivery.rs:1-9) | Local over Wire✓ |
| 17 | pane_leases | `PaneLease` (delivery.rs:58): delivery_id, flow_id, herdr_pane_id, lease_step local `LeaseStep` (delivery.rs:45: Acquired Interrupted Placed Submitted) | DeliveryId (delivery.rs:66-68) | per-flow (the recipient) | Herdr pane id | yes: the row exists only while typing. `lease_step` shows how far it got. A seeded open settles any leftover row as Uncertain (delivery.rs:350-363, store.rs:5277) | Local |
| 18 | delivery_configuration | `DeliveryConfiguration` (delivery.rs:95): harness_profile_vector Vec<HarnessProfile>, meta_aspects MetaAspects, message_nexus_path_option | "delivery" (delivery.rs:144-147) | global configuration | no | no | Local over Wire✓ (L) |
| 19 | meta_nexus_configuration | `StoredMetaNexusConfiguration` (store/nexus_configuration.rs:23){nexus `ConfigureNexus`} (M:283) | "nexus" (nexus_configuration.rs:28-30) | global configuration | Codex paths | no | Local over Wire✓ |
| 20 | meta_model_configuration | `StoredMetaModelConfiguration` (store.rs:1025){model `ConfigureModel{Layer Aspect Native}`} (M:273) | layer+aspect (store.rs:1029-1036, 7773) | global configuration | model name | no | Local over Wire✓ |
| 21 | flow_events | `FlowEvents` (store/events.rs:34): flow_id, event_vector Vec<`Event`> (S:697: Started.Option<NativeSessionId>, ToolUsed, Stopped.NativeStop{session, transcript path, last assistant message} (S:581), PromptSubmitted.NativePrompt{session, PromptId, sha} (S:582), Ended, Cleared) | FlowId (events.rs:40-42) | per-flow | yes: native session ids, native prompt ids, transcript path | no: an append-only journal | Local wrapper over Wire✓ Event |
| 22 | flow_context_sizes | `FlowContextSize` (store/context.rs:27): flow_id, tokens i64 | FlowId (context.rs:33-35) | per-flow | no | no | Local |
| 23 | address_holds | `AddressHold` (store/address_hold.rs:39): flow_id, address, found Option<Metaflow> | FlowId (address_hold.rs:46-48) | per-flow, but it references an Address and the metaflow that held it (which names other flows) | no | yes: the row exists while a launch is unconfirmed. Confirmation drops it, and refusal or ending gives the Address back (doc address_hold.rs:1-12) | Local over Wire✓ Metaflow |
| 24 | meta_leave_out_configuration | `StoredMetaLeaveOutConfiguration` (store.rs:1308){leave_out `ConfigureLeaveOut{Address HarnessKind LeaveOuts}`} (M:277) | Address+harness (store.rs:1312-1319, 7783) | global configuration, keyed per address | no | no | Local over Wire✓ |
| 25 | launch_opened_threads | `OpenedLaunchThread` (store/opened_thread.rs:27): launch_request_id, native_session_id | LRID (opened_thread.rs:33-35) | belongs to a launch | yes: the Codex thread id | no: written once (doc opened_thread.rs:1-11) | Local |
| 26 | send_calls | `SendCall` (G:send_tool:114): tool_call_key `ToolCallKey{ThreadId TurnId CallId}`, ContentSha256, SendOutcome [Accepted{Sender Target SendAcceptance} / LegacyUnknown{Sender Target} / Refused] (send_tool.ethos:82) | the tool-call key as text (send_call.rs:57-61, 43-50) | cross-flow: the sender is reached through the Codex thread and the Sender Address; the recipient is the Target Address | yes: Codex thread, turn and call ids | no | Wire✓ (the row type itself) |
| 27 | launch_cleanups | `LaunchCleanup` (store/launch_cleanup.rs:41): launch_request_id, native_session_id, thread_step and pane_step as local `CleanupStep` (Pending/Done) | LRID (launch_cleanup.rs:50-52) | belongs to a launch | Codex thread id | yes: `thread_step` and `pane_step`. Pending means it is resumed at start (doc launch_cleanup.rs:1-10) | Local |
| 28 | meta_send_server_configuration | `StoredMetaSendServerConfiguration` (store/send_server.rs:32){send_server `ConfigureSendServer{CodexAppServerBinary McpSendServerBinary}`} (M:286) | app-server binary (send_server.rs:37-39) | global configuration | binary paths | no | Local over Wire✓ |
| 29 | queue_delivery_counter | `DeliveryCounter` (store/queue_delivery.rs:84): next_request u64, next_attempt u64 | singleton COUNTER_KEY (queue_delivery.rs:90-92) | global | no | no | Local |
| 30 | queue_delivery_requests | `StoredDeliveryRequest` (queue_delivery.rs:130): request_id, address, queue_evidence `QueueEvidence` (M:432: Logical.QueueEntry / Legacy{SentBy Request}), state local `RequestState` (queue_delivery.rs:96: Queued Settled Unsent Parked) | request_id (queue_delivery.rs:138-140) | cross-address: the recipient is `address` and the sender is the SentBy inside the evidence | no | yes: `state` Queued/Unsent is pending; Settled/Parked is final | Local (the evidence is Wire✓) |
| 31 | queue_delivery_attempts | `QueueDeliveryAttempt` (queue_delivery.rs:397): request_id, attempt_id, native_request_id u64, flow_id, thread_id, harness_kind, history_anchor local `NativeHistoryAnchor` (queue_delivery.rs:325: ClaudeTranscript{device inode offset} / CodexTurns Option<String>), address, queue_evidence, phase local `QueueDeliveryPhase` (queue_delivery.rs:342) | attempt_id (queue_delivery.rs:411-413) | per-flow (the recipient flow_id) and per-address | yes: thread id, native request id, transcript device/inode/offset, Codex turn id, NativeDeliveryReceipt{thread turn receipt} (queue_delivery.rs:306) | yes: `phase` Prepared / Uncertain / ReceiptRecorded is in flight; Settled / Absent / Resolved(QueueResolutionRecord, M:425, carrying ProcessIdentity) is final. A seeded open recovers them (store.rs:5285-5300) | Local (QueueEvidence, Undecided, AbsenceProof and QueueResolutionRecord are Wire✓ from M) |
| 32 | meta_metaflow_configuration | `StoredMetaMetaflowConfiguration` (store/metaflow_declaration.rs:30){metaflow `ConfigureMetaflow`} (M:308) | Address (metaflow_declaration.rs:35-37) | global configuration, keyed per address | no | no | Local over Wire✓ |
| 33 | meta_model_threshold_configuration | `StoredMetaThresholdConfiguration` (store.rs:1115){threshold `ConfigureThreshold{ModelName Refresh}`} (M:275) | model name (store.rs:1119-1123) | global configuration | model name | no | Local over Wire✓ |
| 34 | meta_investigation_configuration | `StoredMetaInvestigationConfiguration` (store.rs:1141){investigation Address} | "investigation" (store.rs:1145-1149) | global singleton | no | no | Local over Wire✓ |
| 35 | meta_default_minutes_configuration | `StoredMetaDefaultMinutesConfiguration` (store.rs:1167){default_minutes i64} | "default-minutes" (store.rs:1171-1175) | global singleton | no | no | Local |
| 36 | meta_harness_flags_configuration | `StoredMetaHarnessFlagsConfiguration` (store.rs:1194){configured `ConfigureHarnessFlags{Address HarnessFlags}`} (M:312) | Address (store.rs:1198-1202) | global configuration, keyed per address | no | no | Local over Wire✓ |
| 37 | meta_heartbeat_configuration | `StoredMetaHeartbeatConfiguration` (store.rs:1230){heartbeat `HeartbeatConfig`} (M:317) | "heartbeat" (store.rs:1234-1238) | global singleton | no | no | Local over Wire✓ |
| 38 | compactions | `Compaction` (store/compaction.rs:38): flow_id, boundary String, address Option<Address>, investigation local `Investigation` (compaction.rs:25) | "flow_id:boundary" (compaction.rs:48-50, 58-59) | per-flow | yes: `boundary` is the harness's own compaction id (Claude uuid / Codex item id) | no | Local |
| 39 | reminders | `Reminder` (store/reminder.rs:61): key (LogicalDeliveryId), address (the sender), recipient, minutes, due Option<i64>, sent i64 | LogicalDeliveryId (reminder.rs:79-81) | cross-address: the sender is `address` and the recipient is `recipient` | no | yes: an open task. A Done retracts the row (reminder.rs:208). `due=None` means every reminder has been sent (doc reminder.rs:70-73) | Local |
| 40 | successor_intents | `SuccessorIntent` (store/successor.rs:52): address, predecessor String (a FlowId), cause local `SuccessionCause` (successor.rs:34), launch_request_id | Address (successor.rs:60-62) | per-address. It names the predecessor flow and the successor's LRID | no | yes: a successor is owed. The row exists until confirmation retracts it (successor.rs:194-260, doc 1-10) | Local |
| 41 | send_outcome_counter | `SendOutcomeCounter` (store/send_outcome.rs:22): next_id u64 | singleton (send_outcome.rs:27-29) | global | no | no | Local |
| 42 | send_outcomes | `StoredSendOutcome` (send_outcome.rs:43){record `SendOutcomeRecord`} (M:435: SendOutcomeId, Option<Process>, Option<Address> (the sender), Option<Address> (the recipient), RequestDigest, OrdinarySendOutcome) | send_outcome_id (send_outcome.rs:48-50) | cross-address: first is the sender and second the recipient (send_outcome.rs:541-548) | yes: the caller's Process (pid and start). A Sent receipt carries NativeReceipt | no: an audit journal | Local wrapper over Wire✓ |
| 43 | logical_delivery_counter | `LogicalDeliveryCounter` (store/logical_delivery.rs:78): next_cursor i64 | singleton (logical_delivery.rs:82-84) | global | no | no | Local |
| 44 | logical_delivery_current | `CurrentLogicalDelivery` (logical_delivery.rs:96){snapshot `DeliverySnapshot{DeliveryCursor LogicalDeliveryId SentBy Address DeliveryState}`} (S:637) | LogicalDeliveryId (logical_delivery.rs:100-102) | cross-address: SentBy is the sender and Address the recipient | Delivered carries `NativeReceipt{HarnessKind NativeSessionId NativePromptId}` (S:618) | yes: DeliveryState (S:622) Queued / Attempting / Retryable / Uncertain is open; Delivered / Failed / Withdrawn is final | Local wrapper over Wire✓ |
| 45 | logical_delivery_events | `LogicalDeliveryEvent` (logical_delivery.rs:225){snapshot DeliverySnapshot} | cursor, zero-padded to 20 digits (logical_delivery.rs:229-231) | cross-address | as in #44 | no: a journal of transitions | Local wrapper over Wire✓ |
| 46 | simplified_reply_bindings | `SimplifiedReplyBinding` (logical_delivery.rs:357): flow_id, input_delivery_id, source Address, recipient Address, completed bool | FlowId (logical_delivery.rs:376-378) | per-flow (the simplified seat). Cross-address through source and recipient | no | yes: `completed`. False means a reply is still owed (logical_delivery.rs:366-374) | Local |
| 47 | logical_delivery_purposes | `LogicalDeliveryPurpose` (logical_delivery.rs:34): logical_delivery_id, address, purpose local `DeliveryPurpose` (heartbeat.rs:9: Ordinary / Heartbeat) | LogicalDeliveryId (logical_delivery.rs:40-42) | per-address (the recipient) | no | no | Local |
| 48 | heartbeat_standings | `StoredHeartbeatStanding` (store.rs:1255): address, baseline_/latest_ awake, working, working_complete, sent, queue; outstanding Option<String> | Address (store.rs:1279-1283) | per-address | no | yes: `outstanding` holds the LogicalDeliveryId of a heartbeat that has not settled. It is cleared once that delivery settles (heartbeat.rs:257-272) | Local |

## 2. How the store is read today

**Read-only opens (observed):**
- `FlowStore::recognize_flow_memory` (store.rs:8350-8378) calls `redb::ReadOnlyDatabase::open` (store.rs:8366). The comment says it "refuses an active writer and never runs redb recovery" (store.rs:8362).
  - `RepairAborted` sends it to `recognize_repaired_copy` (store.rs:8380-8416). That function copies the file, repairs the copy with `redb::Database::create`, then reopens the copy read-only.
  - `DatabaseAlreadyOpen` returns `StoreHeld` (store.rs:8373-8375).
- `recognize_open_memory` (store.rs:8419-8504) runs one `begin_read` and reads only identity data:
  - the `__sema_meta` schema version (store.rs:8429-8441);
  - the storage layout in `__sema_engine_counters` (store.rs:8443-8459);
  - every registration in `__sema_engine_catalog`, through `is_current_flow_registration` (store.rs:8026) and `has_expected_flow_catalog` (store.rs:8326);
  - the `flow_nexus_state` identity row, decoded with `rkyv::from_bytes` (store.rs:8488-8500).
  It reads no other family rows.
- `StagedUpgrade::run` also opens `ReadOnlyDatabase` (store/staged_upgrade.rs:136). It reads only the catalog, in `upgrade_pending` (staged_upgrade.rs:250-294), which answers whether any table in scope is absent or not at its current identity.
- `flow-store-check` (bin/flow-store-check.rs:33-47 → store_check.rs:83-104) does not read the original store through ReadOnlyDatabase beyond recognition.
  - It copies the store into a private tempdir (store_check.rs:28-41).
  - It then runs `FlowStore::open_configured` on the copy (store_check.rs:65). That is a full writer `Engine::open` with family upgrades.

**Writer opens (observed):**
- `Engine::open` (sema-engine 9884905 src/engine.rs:121) is a writer open.
- `open_configured_in_place` (store.rs:4771-5051) upgrades families (store.rs:4963-5000). It then writes: `archive_legacy_queue` (store.rs:5045; queue_delivery.rs:962-) and `seed_missing_queued_deliveries` (store.rs:5046; logical_delivery.rs:1283-).
- `open_seeded` also settles interrupted pane leases (store.rs:5277) and recovers queue attempts (store.rs:5285-5300).

**Family reads (observed):**
- Every family read goes through `Engine::match_records` (engine.rs:1128-1166). Each call opens its own `storage.read` transaction and returns that transaction's `DatabaseMarker`.
- Flow uses only `QueryPlan::all` and `QueryPlan::key`. There is no secondary index, so a read "by FlowId" of a table keyed otherwise is a full scan plus a filter.
- Reads that span families are several reads checked against one marker, not one transaction:
  - `meta_configuration_snapshot` (store.rs:8508-8540, 10 meta families, `ConfigurationReadViewChanged`);
  - `launch_inspection_records` (store.rs:6964-7090: attempts, outcomes, flows, herdr_routes; documented as "a checked multi-read view, not a storage transaction", store.rs:6961-6963);
  - `list_metaflows` (store.rs:5491-5503).
  Nothing else compares markers.
- `Engine::storage_reader()` (engine.rs:1450) lends one raw sema `ReadTransaction`. Flow uses it once, in `launch_attempt_archives` (store.rs:5925-5935), to read raw `(key, archive)` pairs.

**Existing read functions that take a FlowId:**
- flows: `flow` (store.rs:6875); all rows through `flow_nodes` (store.rs:7112).
- native_owner_proofs: `native_owner_proof_record` (store.rs:627).
- herdr_routes: `herdr_route` (store.rs:6888).
- roles: `role` (store.rs:6272).
- flow_events: `event_row` (events.rs:341).
- context sizes: `context_size_row` (context.rs:69).
- address_holds: `address_hold` (address_hold.rs:393).
- simplified replies: `simplified_reply_receipt` (logical_delivery.rs:833).
- compactions: `compactions_of` (compaction.rs:117, a scan).
- launch attempts bound to a flow: `launch_requests_bound_to` (store.rs:6816, a scan that returns LRIDs).
- the metaflow a flow is awake as: `metaflow_awake_as` (metaflow.rs:376, a scan).
- whether a flow holds a successor: `held_successor` (store.rs:6773, scans replacements).

**Existing read functions that take an Address:**
- `stored_metaflow` (store.rs:5420), `stored_metaflow_process` (store.rs:5436), `stored_metaflow_lock` (store.rs:5455).
- `successor_intent` (successor.rs:206).
- `default_leave_outs` (store.rs:5390), `harness_flags` (store.rs:5406), `metaflow_declaration` (metaflow_declaration.rs:401).
- `configured_model` (store.rs:1359, keyed by layer and aspect).
- `give_back_ended_holds` (address_hold.rs:406, a scan).
- `read_logical_delivery_snapshots` (logical_delivery.rs:1649, a scan by sender address).
- `debug_snapshot` (logical_delivery.rs:681).
- heartbeat standings: no Address read; only `heartbeat_standings` (store.rs:4173, all rows).

**Read functions by other keys or all rows (nothing by FlowId or Address):**
- By LRID: `stored_launch_attempt` (store.rs:6916), `launch_outcome` (store.rs:6721), `replacement` (store.rs:6757), `stored_launch_pane` (created_pane.rs:109), `opened_thread` (opened_thread.rs:90), `launch_cleanup` (launch_cleanup.rs:126), `quarantined_launch_attempts_of` (store.rs:5946).
- By native session: `thread_launch` (opened_thread.rs:114).
- By DeliveryId: `delivery` (delivery.rs:274).
- By attempt id: `queue_delivery_attempt` (queue_delivery.rs:1716).
- By request id: `request_state` (queue_delivery.rs:919).
- By logical id: `logical_delivery_snapshot` (logical_delivery.rs:1635), `reminder` (reminder.rs:192).
- By tool-call key: `send_call` (send_call.rs:599).
- All rows: `delivery_attempts` (queue_delivery.rs:889), `retained_logical_requests` (queue_delivery.rs:929), `read_send_outcomes` (send_outcome.rs:566), `delivery_purposes` (logical_delivery.rs:674), `due_reminders` (reminder.rs:215), `successor_intents` (successor.rs:222), `opened_threads` (opened_thread.rs:106).
- Pane leases have no public read; they are read inside `settle_interrupted_deliveries` (delivery.rs:350).

## 3. Inferences (not witnessed)

- **One consistent read.** One `ReadOnlyDatabase::open` plus one `begin_read` could read all 48 tables as raw rkyv rows in a single consistent snapshot, with no marker checks. Basis: the row format seen at store.rs:8490-8498 and 5925-5935.
- **Predecessor shapes.** Such a read sees rows in the shape they were stored in. If `upgrade_pending` (staged_upgrade.rs:250) answers true, some tables still hold predecessor shapes. The exporter must then either refuse or decode through the existing `UpgradeFrom` chains in memory. Example: launch_attempts accepts V1/V2/V3 (store.rs:4834-4836), and quarantining may apply.
- **Rows keyed by FlowId** group under one flow directly: #1, 2, 9, 14, 21, 22, 23, 46, and #38 by key prefix.
- **Rows keyed by LRID** (#10, 11, 12, 13, 15, 25, 27) reach a flow only through `LaunchAttempt.native_launch_binding_option.flow_id` or the LaunchOutcome. A launch that is Reserved or NativeLaunchIntentRecorded has no FlowId except `LaunchProfile.flow_id_option`, so it needs a home outside the per-flow record (the Address, or the launch itself).
- **Rows keyed by delivery id that carry flow_id** (#16, 17, 31) can be filed under the recipient flow.
- **Per-address and cross-address families** have no single owning flow: #4, 5, 6, 30, 39, 40, 42, 44, 45, 47, 48. Neither do the global configuration and counters (#3, 7, 8, 18, 19, 20, 24, 28, 29, 32-37, 41, 43). Under a "per flow, whole" record they would be duplicated, split by side (sender or recipient), or exported as separate per-address and global records. That is a design choice the inventory does not settle.
- **Datomizing the export.** Every wire value inside these rows is already Datomizable. What the export needs to type anew is the store-local wrappers and enums: FlowLifecycle, NativeOwnerProof, LeaseStep, CleanupStep, RequestState, QueueDeliveryPhase, NativeHistoryAnchor, NativeDeliveryReceipt, SuccessionCause, Investigation, DeliveryPurpose, the counters, StoredHeartbeatStanding, CodexEndpointConfiguration and the other scalar-field structs.

## 4. Unknowns

- I did not check whether redb's `ReadOnlyDatabase` can open while a stopped Nexus left the recovery flag set. The code takes the repair-copy path in that case (store.rs:8369-8372).
- I did not trace what EndpointSelection's EndpointPath names at runtime.
- I did not trace the meaning of `FlowRecord.flow_type` and `generation`.
- I did not read the predecessor decode chains for every family.
