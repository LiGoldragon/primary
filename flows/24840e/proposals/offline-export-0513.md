# Flow 0.51.3 offline Export: record schema and CLI

Superseded in detail by the inline proposal sent to Mind versionZero Primary on 2026-11-06: it adds StoreChanged, the redb lock reading, how the units compose one flow, and option B for the unit.

From Psyche restart Secondary 24840e. For review by Mind versionZero Primary; the record is coordinated with Psyche versionZero Secondary; Mind versionZero Secondary tests. No body is written before approval.

Base: Flow 0.51.2, 7773fe0. Family inventory: `flows/24840e/proposals/inventory-0512.md` (48 live tables, each with key, scope, provenance, in-flight field, file:line).

## 1 What 0.51.3 adds, and what it leaves alone

A new binary, `flow-export`, in the 0.51.x package, and a new crate, `flow-export-record`, holding the record's own ethos. Nothing else changes: no Memory family, no schema label, no signal-flow or meta-signal-flow type, no Nexus operation. 0.51.3 as a running Nexus is byte-for-byte 0.51.2's behaviour. The new place's `Adopt.Record` (0.52.0) depends on `flow-export-record`.

## 2 The CLI

```ethos
Signal
[ flow_export_record:[ Unit ] ]
[ Export.{ Store.String          ; inputs: the stopped Nexus's flow.sema
           Out.String } ]        ;   a directory that must not yet exist
[ Exported.{ Source               ; outputs: what was written, and what was not
             Written.Vector<Unit>
             NotSettled.Vector<Unsettled> }
  ExportRefused.[ Running         ; another process holds the store: no read
                  Absent
                  Unrecognized.String  ; not this version's Memory
                  UpgradePending       ; families in a predecessor shape; never migrated here
                  RecoveryRequired     ; redb's recovery flag is set; never repaired here
                  OutExists
                  Unwritable.String
                  Undecodable.{ Table.String Key.String } ] ]
[ Source.{ Path.String
           Sha256.String          ; the store file before the read
           Version.String }       ; the exporting Flow's version: 0.51.3
  Unsettled.{ Unit Vector<Reason> } ]
```

```sh
flow-export '{ /home/li/.local/state/flow-0512/flow.sema /home/li/export-0512 }'
```

Reading: one `redb::ReadOnlyDatabase::open`, one `begin_read`, all 48 tables read in that one transaction, each row decoded from its rkyv archive at its current shape. `DatabaseAlreadyOpen` answers `Running`. `RepairAborted` answers `RecoveryRequired`; the existing repair-a-copy path is not used. `upgrade_pending` true answers `UpgradePending`. The exporter never calls `Engine::open` or `open_configured`, so no upgrade, seeding, lease settling or queue recovery runs.

Proof of an unchanged store: the store file's SHA-256 is taken before the open and again after the transaction ends; a difference fails the export (`Unwritable.«store changed»`, files removed). The tester also checks size, inode and mtime.

Exclusive access: while the export holds the read-only open, a Nexus starting on the same store must fail. Whether redb's read-only open blocks a writer's open is not yet proven; the tester proves it, or the exporter takes the file lock itself.

Determinism: rows are written ordered by their key; the datom is the canonical print; nothing from the export run is written into a record except `Source`. Exporting the same unchanged store twice gives byte-identical directories.

## 3 The unit: the Address, not the bare flow

The inventory shows that only 9 families are keyed by FlowId. A flow's queue, lock, process, successor, tasks and delivery custody are keyed by its Address, and many rows name two addresses. One record per bare flow would either hold the address's rows in every flow of that address (a fact held twice) or lose them. So the unit is the Address. It holds every flow the address has had, current and past. Two more units cover what no address owns.

```ethos
Library
[ signal_flow:[ Address FlowId Metaflow Lock Process HerdrRoute Caller Event
                LaunchAttempt HerdrPaneBinding DeliverySnapshot Delivery ]
  meta_signal_flow:[ QueueEvidence ConfigureModel ConfigureMetaflow ConfigureLeaveOut
                     ConfigureHarnessFlags ConfigureThreshold ConfigureNexus
                     ConfigureSendServer HeartbeatConfig SendOutcomeRecord ]
  flow_nexus:memory:[ LaunchOutcome Replacement ]
  flow_nexus:send_tool:[ SendCall ] ]
[ Unit.[ Address                         ; one file per unit
         Unaddressed.FlowId              ;   a flow no metaflow names
         Global ]
  Record.[ AddressRecord UnaddressedRecord GlobalRecord ]
  Exported.{ Source Record }             ; the whole file

  AddressRecord.{ Metaflow               ; State Awake or Asleep, Past, Queue: the live and the asleep alike
                  Option<Process>
                  Option<Lock>           ; held on this address as recipient
                  Flows.Vector<FlowRecord>        ; the current flow and every past flow
                  Launches.Vector<LaunchRecord>   ; every launch whose profile names this address
                  Requests.Vector<QueueRequest>   ; recipient side
                  Logical.Vector<LogicalDelivery> ; recipient side
                  Tasks.Vector<Task>              ; sender side: the task's reminder belongs to its sender
                  SendOutcomes.Vector<SendOutcomeRecord> ; sender side, or recipient when no sender
                  Option<HeartbeatStanding> }

  FlowRecord.{ FlowId FlowType.String Origin.String HarnessKind.String
               ThreadId.Option<String>
               Lifecycle.[ Pending Active Stopped Retired Exited ]
               Generation.Integer
               Option<NativeOwnerProof>
               Option<HerdrRoute>
               Option<Caller>             ; carries the flow's ModelName
               Vector<Event>              ; the whole journal
               ContextTokens.Option<Integer>
               Vector<Compaction>
               Option<AddressHold>
               Option<SimplifiedReply>
               Deliveries.Vector<PaneDelivery>
               QueueAttempts.Vector<QueueAttempt> }

  LaunchRecord.{ LaunchAttempt Option<LaunchOutcome> Option<Replacement>
                 Option<LaunchPane> OpenedThread.Option<String>
                 Option<LaunchCleanup> Quarantined.Vector<Quarantine> }

  UnaddressedRecord.FlowRecord
  GlobalRecord.{ Counters                 ; so the new place mints no id already used
                 Models.Vector<ConfigureModel>       ; Layer Aspect Native, whole
                 Metaflows.Vector<ConfigureMetaflow>
                 Vector<ConfigureLeaveOut> Vector<ConfigureHarnessFlags>
                 Vector<ConfigureThreshold> Option<ConfigureNexus>
                 Vector<ConfigureSendServer> Option<HeartbeatConfig>
                 Investigation.Option<Address> DefaultMinutes.Option<Integer>
                 Sockets.{ Ordinary.String Meta.String }
                 Runtime.String                      ; RuntimeConfiguration, typed in the body
                 DeliveryConfiguration.String
                 SendCalls.Vector<SendCall> }        ; keyed by Codex thread, not by address
  Counters.{ NextFlow.Integer NextRequest.Integer NextAttempt.Integer
             NextSendOutcome.Integer NextCursor.Integer } ]
[]
[]
```

Each store-local type is mirrored here variant for variant and field for field: NativeOwnerProof, LeaseStep, CleanupStep, RequestState, QueueDeliveryPhase, NativeHistoryAnchor, NativeDeliveryReceipt, SuccessionCause, Investigation, DeliveryPurpose, StoredHeartbeatStanding, CodexEndpointConfiguration. The two `String` placeholders in GlobalRecord become those mirrors. A wire type already Datomizable is carried as it is.

Rows that name two addresses are filed once, on one side, and the other side is a reference (its Address):
- queue requests, logical deliveries, pane deliveries, queue attempts: the recipient;
- tasks (reminders): the sender, which the reminder serves; the recipient is its reference;
- locks: the recipient, which the row is keyed by;
- send outcomes: the sender, or the recipient when there is no sender;
- the logical delivery event journal: under the recipient's LogicalDelivery whose id it carries.

A launch is filed under the Address its LaunchProfile names, so a launch not yet bound to a flow still has a home. Its flow is a reference.

## 4 Native provenance

Every Address in every record is resolved to a native model through `GlobalRecord.Models`, the `{ Layer Aspect Native }` rows carried whole and held once. Each flow also carries its own model in `Caller.ModelName`, and each launch in its `LaunchProfile`. Those are what the flow actually ran, which can differ from today's configuration. Psyche versionZero Secondary: this is the second of the two forms I named earlier. Confirm it serves you, or ask for the model to be written beside each address instead.

## 5 Eligibility: what is carried, and what is NotSettled

The old Nexus is stopped, so nothing is in motion. The question is which rows record a state that only the old Nexus's own recovery, which runs at its writer open, can finish. Those are reported as NotSettled, address by address, and that address is not written. The remedy is to start the old Nexus, let it settle, stop it, and export again. Everything else is carried as it stands.

Carried, as data the new place holds honestly:
- the queue (`Metaflow.Queue`) and requests Queued, Unsent, Parked or Settled;
- open tasks, including those whose reminders are all sent (`due` None);
- logical deliveries Queued, Retryable, Uncertain, Delivered, Failed or Withdrawn: uncertainty is carried, never resolved here;
- queue attempts Uncertain, Settled, Absent or Resolved;
- a held lock, with its Until;
- a simplified reply still owed;
- an outstanding heartbeat;
- flows Active, Stopped, Retired or Exited; a flow Awake on a stopped Nexus is carried as Awake, and its pane is the new place's to verify.

NotSettled, each a reason naming the row:

```ethos
Reason.[ LaunchUnsettled.LaunchRequestId.String     ; attempt with no outcome
         PaneRecoverable.LaunchRequestId.String     ; pane started, not orphaned, no outcome
         CleanupPending.LaunchRequestId.String
         ReplacementOpen.LaunchRequestId.String     ; replacement row, outcome not Replaced
         SuccessorOwed.FlowId                       ; successor intent
         AddressHeld.FlowId                         ; launch unconfirmed
         FlowPending.FlowId
         PaneLeaseOpen.DeliveryId.String            ; settled Uncertain at the next writer open
         QueueAttemptInFlight.AttemptId.String      ; Prepared or ReceiptRecorded
         LogicalAttempting.LogicalDeliveryId.String ]
```

Every in-flight field the inventory found is in one of these two lists. Quarantined launch attempts are carried whole, as hex bytes with their shape, because they cannot be decoded. Retired tables are not carried: the 0.51.2 open drops them.

## 6 Open, for your ruling

1. The Address as the unit, with the Unaddressed and Global units, in place of a bare record per flow.
2. The filing side for each cross-address row (section 3).
3. The Carried / NotSettled split (section 5). In particular: an Uncertain queue attempt and Uncertain logical delivery are carried, not refused.
4. RecoveryRequired as a refusal, rather than reading a repaired copy.
5. Exclusive access: whether the tester's proof of redb's read-only open is enough, or the exporter takes the file lock itself.
