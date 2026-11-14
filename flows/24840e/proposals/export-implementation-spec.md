# Flow 0.51.3 offline Export: implementation spec

Approved by Mind versionZero Primary (reviewer and releaser). The units by fact owner were approved by the parent. Worktree `/git/worktrees/flow-0513-export-24840e`, branch `0.51.3-offline-export`, base 7773fe0 (0.51.2). Family inventory: `flows/24840e/proposals/inventory-0512.md` (48 live tables, with file:line for each record type).

## Boundaries

- No change to any Memory family, schema label, table, or upgrade chain; no change to signal-flow or meta-signal-flow; no new Nexus operation; the running Nexus's behaviour is unchanged. 0.51.3 adds a crate and a binary only, plus the version bump.
- Local cargo is disabled. Compile and test on the configured remote Nix builder through the flake's checks (`checks.<system>.default`, and a focused check for the export if one is added). Use rustfmt for formatting.
- Follow the repository's rules: README.md, DESIGN.md, `checks/no-free-functions.sh` (only `fn main` is free), `checks/no-inherent-methods.sh` (every method lives in a trait), and generated ethos modules committed and equal to fresh generation (build.rs pattern of crates/flow-ethos).

## 1 The record crate: `crates/flow-export-record`

Its own ethos at `ethos/record.ethos`, generated into `src/generated/record.rs` by the same build.rs check as flow-ethos, with the `datom` feature on. It depends on flow-ethos, signal-flow and meta-signal-flow for wire types, which it carries as they are. It must not depend on flow-nexus. The 0.52.0 Adopt depends on this crate.

Every store-local type is mirrored variant for variant and field for field, with the same names. These include NativeOwnerProof, FlowLifecycle, LeaseStep, CleanupStep, RequestState, QueueDeliveryPhase, NativeDeliveryReceipt, NativeTranscriptCursor, NativeHistoryAnchor, AbsenceRecord, SuccessionCause, Investigation, DeliveryPurpose, HeartbeatStanding, CodexEndpointConfiguration, RuntimeConfiguration, DeliveryConfiguration and ArchivedLaunchAttemptShape. flow-nexus's own generated types that appear in rows are mirrored the same way: LaunchOutcome, LaunchedRecord, ReplacedRecord, Replacement, SendCall, ToolCallKey, SendOutcome and LaunchContext. A u64 becomes Integer. Conversion from store type to record type lives in flow-nexus, as a trait implemented on the store type.

The record's structure is this. The exact imports are resolved by the implementer and checked with `ethos-zero 'Check./abs/record.ethos'`.

```ethos
Unit.[ Address Unaddressed.FlowId Global ]
Exported.{ Source Record }                        ; one file
Record.[ AddressRecord UnaddressedRecord GlobalRecord ]
Source.{ Path.String Sha256.String Version.String }

AddressRecord.{ Address Portable.AddressPortable SourceBound.AddressSourceBound }
AddressPortable.{ Metaflow                        ; State, Past, Queue as stored
                  Configured.Option<ConfigureModel> ; the source Models row for its Layer and Aspect
                  Flows.Vector<FlowRecord>        ; every flow the metaflow names: State's flow and every Past flow
                  Launches.Vector<LaunchRecord>   ; every launch whose LaunchProfile names this Address
                  Successor.Option<SuccessorIntent>
                  Requests.Vector<QueueRequest>   ; recipient side
                  Logical.Vector<LogicalDelivery> ; recipient side, each with its event journal and its purpose
                  Tasks.Vector<Reminder>          ; sender side
                  SendOutcomes.Vector<SendOutcomeRecord> ; sender side, or recipient when no sender
                  Option<HeartbeatStanding> }
AddressSourceBound.{ Option<Process> Option<Lock> }   ; Lock filed at its recipient

FlowRecord.{ FlowId Portable.FlowPortable SourceBound.FlowSourceBound }
FlowPortable.{ FlowType.String Origin EndpointSelection HarnessKind
               Lifecycle.FlowLifecycle Generation.Integer
               Native
               Option<Caller> Vector<Event> ContextTokens.Option<Integer>
               Vector<Compaction> Option<AddressHold> Option<SimplifiedReply>
               Deliveries.Vector<Delivery>        ; settled pane deliveries
               QueueAttempts.Vector<QueueAttempt> } ; the history anchor sits in SourceBound
FlowSourceBound.{ Option<NativeOwnerProof> Option<HerdrRoute>
                  Leases.Vector<PaneLease>
                  Anchors.Vector<{ AttemptId.String NativeHistoryAnchor }> }
Native.{ HarnessKind
         Session.[ Thread.String Unrecorded ]                ; flows.thread_id
         Model.[ Role.String                                  ; roles Caller.ModelName
                 Launch.{ LaunchRequestId.String Model.String } ; the bound launch's LaunchProfile
                 Both.{ Role.String Launch.{ LaunchRequestId.String Model.String } } ; both recorded and differing
                 Unrecorded ]
         Transcript.[ Stopped.String Unrecorded ] }           ; the last Stopped event's transcript path

LaunchRecord.{ LaunchAttempt Context.LaunchContext Option<LaunchOutcome> Option<Replacement>
               Option<LaunchPane> OpenedThread.Option<String> Option<LaunchCleanup>
               Quarantined.Vector<Quarantine> }
Quarantine.{ LaunchRequestId.String Number.Integer Shape.ArchivedLaunchAttemptShape
             Format.{ Producer.String Encoding.[ Rkyv Unknown ] }
             Sha256.String Bytes.String                       ; lowercase hex
             NotAdoptable.[ Unverified ] }

UnaddressedRecord.FlowRecord
GlobalRecord.{ Counters Models.Vector<ConfigureModel> ... every global and configuration family, whole ... }
Counters.{ NextFlow NextRequest NextAttempt NextSendOutcome NextCursor }   ; Integers
Manifest.{ Source Units.Vector<{ Unit File.String Sha256.String }> }
```

Model.Both is used only when both values exist and differ. When they are equal, Role is used. These are recorded facts: nothing is resolved from configuration, and nothing is guessed. A quarantined launch attempt sits in the LaunchRecord of its LRID. If no attempt row exists for it, it goes in GlobalRecord, in a `Quarantined` vector. GlobalRecord holds source facts only. Its doc comment states that Adopt installs none of it.

## 2 The CLI and its answers

The binary is `crates/flow-nexus/src/bin/flow-export.rs`, alongside flow-store-check, and takes one datom: `flow-export 'Export.{ /abs/flow.sema /abs/out }'`. Its replies, printed as datom; it exits nonzero on any refusal:

```ethos
[ Exported.{ Source Units.Vector<Unit> }
  ExportRefused.[ Running Absent Unrecognized.String UpgradePending RecoveryRequired
                  RetiredPresent.String OutExists Unwritable.String StoreChanged
                  Undecodable.{ Table.String Key.String }
                  UnknownTable.String
                  NotSettled.Vector<{ Unit Vector<Reason> }>
                  Unplaced.Vector<{ Table.String Key.String }>
                  Duplicated.Vector<{ Table.String Key.String }>
                  Unresolved.Vector<{ Unit Reference.String }> ] ]
Reason.[ LaunchUnsettled.String PaneRecoverable.String CleanupPending.String
         ReplacementOpen.String SuccessorOwed.String AddressHeld.String FlowPending.String
         PaneLeaseOpen.String QueueAttemptInFlight.String LogicalAttempting.String ]
```

## 3 The procedure: one function chain, each step a trait method on a type

1. If Out exists, refuse OutExists. If the store is absent, refuse Absent.
2. Open the store with `redb::ReadOnlyDatabase::open`, in the same configuration `recognize_flow_memory` uses (store.rs about line 8366). `DatabaseAlreadyOpen` maps to Running, `RepairAborted` to RecoveryRequired. Never take the repair-copy path.
3. Recognise the store as `recognize_open_memory` does: schema version, layout and catalog. A store that fails recognition is refused Unrecognized. If `upgrade_pending` is true, refuse UpgradePending. Factor the existing recognition so that it is shared, not copied; the behaviour of the existing callers must not change.
4. SHA-256 of the store file, read while the database is held open: hash 1.
5. One `begin_read`. For every live table, open it as `TableDefinition<String, &[u8]>` and decode each row with `rkyv::from_bytes` into its current stored type. A table present in the file but not in the live set is refused UnknownTable; a retired table present is refused RetiredPresent. A row that fails to decode is refused Undecodable. Engine internal tables (`__sema_*`) are excluded from the row inventory. Before writing this step, confirm how the engine lays out a family's table: its name and key and value types, from sema-engine 9884905 and `launch_attempt_archives` (store.rs about line 5925). If an engine family is not a plain `TableDefinition<String,&[u8]>`, read it the way the engine does, still inside this one transaction.
6. Drop the transaction.
7. Build the units. A Unit is an Address that has a metaflow row or another row naming it, an Unaddressed flow (a flows row no metaflow names), or Global. File each row once, by the rules in section 1.
8. Validate:
   - (a) Row identity bijection. Collect the set of (table, key) for every row read. Collect the multiset of (table, key) placed into units. A key placed twice is refused Duplicated; a key read and not placed is refused Unplaced. Compare identities, never counts.
   - (b) Every reference resolves inside the bundle: each FlowId named by a Metaflow State or Past entry, an address hold, a replacement, a successor intent, a launch binding, an outcome or an origin; each Address named by a task, request, delivery, lock or send outcome. A reference that does not resolve is refused Unresolved. List what counts as a reference in the code, as one typed enumeration.
   - (c) NotSettled: for each unit, every in-flight row matching a Reason. If any unit has one, the whole export is refused NotSettled, listing every unit and every reason.
9. Hash the store file again while the database is still held: hash 2. If it differs from hash 1, refuse StoreChanged.
10. Publish, still holding the database.
    - Create a fresh temporary directory beside Out, named `.flow-export-<pid>-<random>`, with `create_dir`. It must not exist beforehand; retry on EEXIST.
    - Write one canonical datom file per unit, `global.datom`, `address-<Aspect>-<topic>-<Layer>.datom` and `unaddressed-<FlowId>.datom`, then `manifest.datom` holding each file's SHA-256.
    - fsync the files and the directory.
    - Rename the directory onto Out with `renameat2(RENAME_NOREPLACE)`, through rustix or libc. EEXIST means OutExists, and the temporary directory is removed. A plain rename is never used, because it would replace an empty directory.
    - On any failure, remove only the temporary directory this run created, identified by the path it created. Nothing else is ever removed.
11. Drop the database. Answer Exported.

Determinism: every vector is ordered by its row key, files are canonical datom, and only Source comes from the run. Source.Version is the crate version, 0.51.3.

## 4 Tests, in the flake's checks

Fixture stores are built with the existing FlowStore writer APIs in a tempdir. The tests are:
1. Round trip:
   - a store with an Awake address, an Asleep address with a queue, a past flow, a task, an Uncertain logical delivery, an Uncertain queue attempt, a held lock, an owed simplified reply, and an unaddressed flow;
   - the export succeeds;
   - each record decodes back from its datom file into its record type;
   - Uncertain is preserved as Uncertain.
2. Determinism: export twice into two Outs, and the bytes are identical.
3. Store unchanged: hash, size, inode and mtime before and after an export are equal, and also after a refused export.
4. Running: hold the store open with the FlowStore writer and run the export; the answer is Running and no Out exists.
5. Writer excluded: while the exporter holds its read-only open, a FlowStore writer open of the same store fails. This needs a hook that pauses between steps; a test-only trait implementation is acceptable.
6. Each NotSettled reason, one fixture each. The whole export is refused, no Out exists, and the store is unchanged.
7. Bijection:
   - a unit-level test that a duplicate plus an omission with an equal count is refused (Duplicated and Unplaced);
   - an Unresolved reference is refused.
8. OutExists, including Out created as an empty directory, and the race: Out created after the check and before the rename is not replaced. Temp cleanup removes only its own directory.
9. UpgradePending and Unrecognized, on fixtures from an older shape if the repository already has them (the v5 row-preservation fixtures); otherwise the gap is stated.
10. A quarantined attempt is carried with its hex bytes, and its Sha256 matches the bytes.

## 5 Deliverables

- A commit on `0.51.3-offline-export`, with the workspace version 0.51.3 and an UPGRADES.md entry stating that 0.51.3 changes no Memory format and adds `flow-export`.
- The remote Nix check results.
- A list of gaps: everything not proven, each stated plainly.

## 6 Amendments after the independent review (Mind versionZero Secondary). These override sections 1 to 4 where they differ.

A1 An Address unit with no metaflow row.
- AddressPortable's first field becomes `Metaflow.[ Stored.Metaflow Absent ]`. Absent is used when rows name the Address but no metaflow row exists, for example a failed launch or one refused before binding.
- No metaflow is synthesised.
- Adopt disposition: an Absent address takes no seat; its rows are carried as history.

A2 The Lock moves to Portable.
- A held lock is owed custody, and its Until is wall-clock time, so it holds true off the old process.
- AddressSourceBound keeps only `Option<Process>`.

A3 `Configured` is removed from AddressPortable. The source Models rows live once, in GlobalRecord, as provenance only; a copy beside each address would be the same fact held twice.

A4 Native.Model becomes `Model.{ Role.Option<String> Launch.Option<{ LaunchRequestId.String Model.String }> }`.
- Both sources are always carried as recorded, None where nothing was recorded.
- There is no Both, Unrecorded or equality rule.
- The launch's whole LaunchProfile also stays in its LaunchRecord.

A5 Disposition matrix. The record crate's doc comments mark every field, and Adopt (0.52.0) follows the marks; nothing is installed or dropped implicitly. The marks:
- Install: a portable fact taken as the destination's own. Identity, lifecycle, the event journal, context, compactions, Metaflow State/Past/Queue, requests, logical deliveries with their journals, tasks, the lock, the owed simplified reply, send outcomes, launches with outcomes and replacements, heartbeat standing.
- Verify: a portable fact naming something outside the store, which the destination checks before activation and refuses the bundle if it fails. Native.Session, Native.Transcript (the path must exist and be that session's transcript), HerdrRoute when a seat is Awake.
- Evidence: carried, never installed. Everything in SourceBound (Process, NativeOwnerProof, pane leases, history anchors) and everything in GlobalRecord.
- Blocking: the presence of the field blocks activation unless handling has been explicitly approved. A Quarantine is Blocking, so it blocks the bundle.
Every field of every record type gets exactly one mark. A test asserts that no field is unmarked, from a mark table kept beside the types.

A6 References. One typed enumeration of every reference kind, each Required or Tolerated.
- Required, refused Unresolved when it does not resolve:
  - every FlowId (Metaflow State and Past, hold, replacement predecessor, successor predecessor, launch binding, launch outcome, origin parent, delivery, lease, queue attempt, simplified reply);
  - every Address;
  - every LaunchRequestId (replacement, successor intent, pane, opened thread, cleanup, outcome, quarantine);
  - every LogicalDeliveryId (event, purpose, reminder key, heartbeat outstanding, queue entry);
  - every queue request id named by an attempt;
  - every DeliveryId named by a lease.
- Tolerated, an explicit, closed list:
  - each case carries a name and a code-cited reason why the target can legitimately be gone (for example a row retracted on settlement while a journal still names it);
  - each case is found in the code, not assumed;
  - the manifest gains `Orphans.Vector<{ Kind Table.String Key.String Reference.String }>` so that every tolerated orphan is listed;
  - anything not on the list is Required.

A7 The exact catalog.
- The exporter's live table list is RUNNING_TABLES ∪ RUNNING_ADDED_TABLES ∪ ADDED_LATER_TABLES, taken from the same constants, not copied. This includes native_owner_proofs and the one RUNNING_ADDED table.
- A test asserts it equals the 48 names in inventory-0512.md section 1.
- Each table maps to exactly one placement rule, in one typed match. A table with no rule fails to compile, or is refused UnknownTable.

A8 Order of refusals.
1. Recognition.
2. RetiredPresent, from the catalog and the file's table list, checked before upgrade_pending so that it is reachable.
3. UnknownTable.
4. UpgradePending.
If upgrade_pending itself classifies the retired tables, the exporter checks them first, and a test proves RetiredPresent is reachable.

A9 Publish adds fsync of Out's parent directory after the RENAME_NOREPLACE, before Exported is answered.

A10 The bijection test on a real fixture.
- An independent oracle iterates every live table directly through redb and builds the set of (table, key), with multiplicity.
- The test compares that set with the placed identities recovered by decoding the published files.
- Unit duplicates alone are not enough.

A11 Further tests:
- Out race: Out created between the check and the rename, through a test hook.
- Crash: a failure injected after the files are written and before the rename leaves no Out and only this run's temporary directory, which cleanup removes. A crashed process's leftover temporary directory is never removed by a later run.
- RetiredPresent, UnknownTable and Undecodable, each on a fixture made with raw redb writes into a copy.
- StoreChanged, through an injected hash source, since a writer is excluded while the read lock is held.
- RecoveryRequired, on a fixture with redb's recovery flag set, if one can be made; otherwise stated as a gap.

A12 GlobalRecord, in full. Each line below is a whole family; the exporter reads the singleton and per-key configuration families and writes them all:
- Counters: NextFlow from state; NextRequest and NextAttempt from queue_delivery_counter; NextSendOutcome from send_outcome_counter; NextCursor from logical_delivery_counter.
- Sockets, from configuration.
- RuntimeConfiguration and DeliveryConfiguration.
- Nexus, from meta_nexus_configuration.
- Models, from meta_model_configuration.
- LeaveOuts, from meta_leave_out_configuration.
- SendServers, from meta_send_server_configuration.
- Metaflows, from meta_metaflow_configuration.
- Thresholds, from meta_model_threshold_configuration.
- Investigation, from meta_investigation_configuration.
- DefaultMinutes, from meta_default_minutes_configuration.
- HarnessFlags, from meta_harness_flags_configuration.
- Heartbeat, from meta_heartbeat_configuration.
- SendCalls.
- Quarantined, for quarantined attempts that have no attempt row.

A13 Private output, independent of the umask; no symlink or path replacement.
- Open Out's parent once, as a directory fd with O_DIRECTORY | O_NOFOLLOW; every later step is relative to that fd.
- Create the temporary directory with mkdirat at mode 0700, then fchmod it to 0700, so a permissive umask cannot widen it.
- Open the temporary directory O_DIRECTORY | O_NOFOLLOW and create each file with openat, O_CREAT | O_EXCL | O_NOFOLLOW at mode 0600, then fchmod it to 0600.
- Publish with renameat2(parent_fd, temp, parent_fd, Out, RENAME_NOREPLACE). A symlink, file or directory already at Out is EEXIST, which answers OutExists; nothing is followed or replaced.
- Cleanup unlinks only the files this run created, by name relative to its own temporary directory fd, then removes that directory relative to the parent fd.
- Tests:
  - under umask 000, Out is 0700 and every file is 0600;
  - a symlink at Out, whether dangling or pointing to a directory, answers OutExists and its target is untouched;
  - Out's parent being a symlink is followed only at the single open of the parent fd, which is documented as the caller's choice of directory.

A14 File names carry no record text.
- Each unit's file is named `unit-<hex>.datom`, where hex is the lowercase SHA-256 of that unit's canonical Unit datom. The global unit is named the same way.
- The only fixed name is `manifest.datom`, which maps each Unit to its file and that file's SHA-256.
- No Topic, FlowId or other stored string reaches a path. Dots, slashes, NUL, case or length in stored values cannot affect where a file lands.
- Two units with the same name are already refused as Duplicated before any write; a test also asserts that every name is distinct.
- Before each openat, the name is checked against `^(manifest|unit-[0-9a-f]{64})\.datom$`. A mismatch is an internal error and nothing is published.
- Tests:
  - fixtures whose Topic or FlowId hold `..`, `/`, NUL, a case-only difference, or an over-long value all land in hashed names inside the temporary directory;
  - nothing exists outside Out afterwards;
  - cleanup after an injected failure removes only the names this run recorded, relative to its own directory fd (A13), so a path replaced or symlinked after creation is never followed.

A15 The temporary directory keeps its identity through publish.
- After mkdirat, open the new directory O_DIRECTORY | O_NOFOLLOW and fstat it. Hold its (st_dev, st_ino) as the owned identity. Every file is written through that fd, never through a name.
- Before the rename: fstatat(parent_fd, temp_name, AT_SYMLINK_NOFOLLOW) must be a directory with the owned identity. A mismatch answers Substituted; nothing is renamed, and nothing under the name is removed.
- After the rename: fstatat(parent_fd, Out, AT_SYMLINK_NOFOLLOW) must have the owned identity, and fstat of the held fd must be unchanged.
  - A mismatch answers Substituted. The entry now at Out is foreign and is left in place, never removed.
  - Our own directory is then reached only through its held fd: its files are emptied by fd-relative unlinkat, and the directory itself stays as an empty, reported orphan, because its name is no longer known.
- Prevention, not only detection: the parent must be trusted. Before any write, fstat the parent fd. It must be owned by the running uid, and must be neither group- nor other-writable; otherwise the answer is ParentUntrusted.
  - The sticky bit is not accepted as a substitute, since the owner's other processes are not excluded by it.
- Residual, stated as a gap: a process of the same uid can still swap the entry between the pre-rename check and renameat2. That process is inside the trust domain, and the post-rename identity check detects the swap but cannot prevent it.
- Tests:
  - ParentUntrusted, for a group-writable, other-writable or foreign-owned parent;
  - through a test hook, the temp entry swapped for a foreign directory before the rename gives Substituted, with both the foreign directory and the store untouched;
  - through a test hook, a swap after the pre-check is detected by the post-rename check and the foreign entry is left in place.

A16 The recorded native identity is kept apart from source configuration (parent ruling on 0.52.0 Restart and Adopt).
- Native.Session, Native.Model.Launch and Native.Model.Role are each flow's recorded native identity:
  - Launch is the ModelName in the LaunchProfile the session was launched with;
  - Role is Flow's Caller row.
- Neither is ever drawn from configuration.
- GlobalRecord.Models and every other configuration family are source evidence only. No record field derives from them.
- The exporter performs no drift check and no refusal between the recorded model and the configured model.
- A5's marks describe field classes for Adopt's owner. The disposition and drift policy is Adopt's, not the exporter's.

A17 Chronology and ordering facts are preserved, never inferred (parent collision rule for 0.52.0).
- Rows are laid out in key order only to make the files deterministic. That layout carries no meaning, and the manifest says so.
- Vectors inside a row are written exactly in their stored order and never sorted. This covers Metaflow.Queue, Past, the event journal and the logical delivery journal.
- Every stored ordering fact is carried whole:
  - DeliveryCursor;
  - the counters;
  - FlowRecord.Generation;
  - Process.Started;
  - NativeOwnerProof's start token;
  - Reminder due and sent;
  - the event and journal positions;
  - every timestamp or sequence field in a launch attempt.
- The exporter adds no derived order, no started-at, and no merge.
- The second pass lists, with file:line, which stored field records each of these: when a flow started, the order of messages in a queue, and the order of tasks. Where no stored field records one, the list says so as a gap. Nothing is reconstructed.

A18 Both queue sequences are exposed as they are (parent legacy-order ruling).
- Every QueueRequest and every Metaflow.Queue entry carries a typed sequence kind beside its stored id:
  `Sequence.[ Legacy.{ RequestId.String } Logical.{ LogicalDeliveryId.String } ]`
- Legacy means the stored id has the `legacy:` prefix (queue_delivery.rs 991, 1046) or the evidence is QueueEvidence.Legacy. Logical means its cursor journal is in the record.
- Ids are stored strings. The record carries them as they are and parses no number out of them.
- The counters stay whole in GlobalRecord, each named by kind: QueueRequest is `queue_delivery_counter.next_request`, LogicalCursor is `logical_delivery_counter.next_cursor`.
- No sort, merge or cross-sequence ranking.
- The second pass states, with file:line:
  - how a `legacy:` id is minted, and whether it embeds the counter value;
  - whether any stored fact proves that a legacy entry predates the journal, for example archive_legacy_queue (store.rs 5045) running before seed_missing_queued_deliveries (5046) on one open, and whether that is recorded anywhere;
  - if no such fact exists, that is the stated gap, and Adopt refuses by Address.

A19 Two more facts for the second pass to establish, each with file:line or stated as unproven. They are only reported; no record field changes.
1. Metaflow.Past:
   - Is it append-only on succession, at every write site: refresh, exit, ordered, replace, retire, rebind, adopt?
   - Is a flow Awake in State always newer than every Past entry, at every write site?
   - List each site that writes Past or State and what it does.
2. Is there a store-wide launch counter?
   - Observed so far: launch request ids are caller-supplied, or a wake's `wake-<past length>-<unix nanos>` (waking.rs 2680).
   - `queue_delivery_counter.next_attempt` counts queue delivery attempts, not launches.
   - Confirm whether any counter is allocated in launch start order and tied to the actual start or binding, so that concurrent completion cannot reverse it. If none exists, say so.

A19 is withdrawn. The parent withdrew keeper selection by start chronology: a duplicate held flow on one Aspect, Topic and Model is an invalid Adopt bundle. The second pass does not audit the Past and State write sites or the launch counter. A17 and A18 stand.

A19 correction (Psyche versionZero Secondary, for Adopt's Asleep rule): item 1 stands, report only — audit every write site of Metaflow.Past and State, whether Past is append-only on succession and whether its last entry is the most recent flow of an Asleep address. Item 2, the launch counter, is dropped.
