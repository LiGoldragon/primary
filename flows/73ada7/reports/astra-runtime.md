# Astra's runtime questions on Message

Read: Message design `flows/73ada7/reports/build/message-design.md`
at e275b6 (blob 66d3fd), cited as M; Flow design
`flows/f5a6e9/reports/flow-buildable-design.md` at d84997, cited as
F; old Message at LiGoldragon/message 6fa4d0 (`flow_edge.rs`,
`listener.rs`, `store.rs`, `configuration.rs`), cited as old.

## 1. Flow edge, sender origin, admission

1. Replacement: settled by design. M 674-677: "Today Message calls Flow meta `ResolvePeer`, `Vet` and `Deliver` ... It now calls `Identify`, `Lock`, `Deliver` and `Release` on the socket of fork F2." M 172-175: Configuration holds only `Ordinary`, `Meta`, `Flow`, so old's `flow_meta_socket_path` (old flow_edge.rs 47) has no field. Its socket, the ordinary `flow.sock` (M 90, F 232-238), is the design's choice. It stays open as fork F2 (M 703-704, F 689-691): unresolved, needs the living's ruling.
2. Sender origin: settled by design. M 335-347: the pid from `SO_PEERCRED` plus "/proc/<pid>/stat field 22" form `Process`, then go out as `Identify.Process`, and "That Address becomes the `Sender` of the lock". The design keeps no caller field (M 231).
3. Process to metaflow: unresolved, needs f5a6e9. The two designs differ. M 343-345: "Flow walks `/proc/<pid>/environ` for `HERDR_PANE_ID` ... keeps that mechanism inside Flow". F 559-563: Flow "walks the process's ancestors to the harness process and compares both the pid and start time of a Flow record's Process". F governs, but F does not say how deep the walk goes or how to identify a flow that is neither spawned nor `Bind`-recorded (F 184-186, 411-415).
4. Admission at Message's ordinary socket: settled by design. M 194 and 444 refuse `Unidentified.Process`. Senders that are no metaflow are refused "for now": F11 (M 737-738), which needs the living's ruling.
5. Admission at Flow's ordinary socket for `Lock`/`Deliver`/`Release`: unresolved, needs f5a6e9. F names no gate, and nothing stops a process other than Message from calling `Deliver` there (M test 11 even takes a Flow `Lock` directly, M 547).
6. F 698 still reads "Deliver.{ Lock Sender Request }", while F 235-237 has `Deliver.{ Lock Request }`: needs f5a6e9.

## 2. Meta socket owner and its authority

1. Owner-only, no allowlist: settled by design, but as this flow's choice [I], not a ruling. M 124-127: "only a process that runs in no flow (the owner) is admitted. The deployed MetaAspects list is dropped". M 687-688 repeats it. Old admitted the owner plus `meta_aspects`, seeded `[Psyche]` (old listener.rs 4-9, 209-211; configuration.rs 40).
2. Mechanism: unresolved, needs the living's ruling. The design names none. "Runs in no flow" can only be read as Flow's `Unidentified` answer to `Identify`, the same answer F11 gives side jobs and the living's terminal (M 349-351, 737-738). That answer is the lack of a match, not a positive identity. The only positive bound is the kernel's: both sockets are mode 0600 (M 93), one Unix user. Old said of that same gate that it "stops accidents and model mistakes, not an adversary" (old listener.rs 6-8).
3. Unstated in M: whether meta `Configure` is admitted while Flow is unreachable. Old admitted it so the owner could repair a wrong Flow path (old listener.rs 8-9, 219). This is the design's own gap. Needs the living's ruling under F8 (M 729-731): whether the kernel peer or a CLI-carried identity is the caller.
4. Flow's meta socket keeps `MetaAspects.Vector<Aspect>` (F 371), so the two Nexuses differ in posture. Needs f5a6e9 if F2 moves `Lock` to Flow's meta socket.

## 3. Configuration, marker, schema, migration

1. Persisted configuration: settled by design. M 291-293 is `Standard.{ Configuration MetaConfigured.Boolean }`, and M 172-175 gives three path strings. M 99-100: "A store that exists holds the configuration. A store created new is seeded from the constant."
2. Marker and admission: settled by design. M 101-104: "While it is false, `Configure` is answered on the ordinary socket too. A meta `Configure` sets it true, after which an ordinary `Configure` is refused `AlreadyConfigured`" (test 13, M 549). That a new seed writes false is implied but not written. Whether a `RestartRequired` answer (M 122) sets the marker is also unwritten.
3. State: settled by design. Message holds only the configuration (M 296-298). Lock and queue state are Flow's (F 175, 183-184).
4. Schema and version: not in the design. M names no sema `SchemaVersion`, table, family or `SchemaHash`. Old used `SchemaVersion::new(1)` and table `message_nexus_configuration`, label `-v1` (old store.rs 138, 154-158). This is this flow's gap to fill, not a fork.
5. Migration: unresolved, needs the living's ruling. M 685-686: "The store starts fresh; no migration of the ledger [I]." But the new store path (M 91) equals old's `~/.local/state/message/message.sema` (old configuration.rs 5), and M 99 says an existing store "holds the configuration". Old stores a five-field `MessageConfiguration` (ordinary, meta, flow, flow_meta, meta_aspects; old configuration.rs 34-40) in the configuration table, and seeds it only when that table is empty (old store.rs 166-173). The design does not say whether the old store is refused, moved aside, or migrated to `Standard`, or what marker it gets. Starting fresh at the same path would be the silent reset Astra excludes, and setting the marker for an old store would infer it. Spirit replaces rather than keeps compatibility. Removing a deployed store needs its content kept or shown redundant first. The startup payload re-sends all three paths (M 105-111), so the old configuration looks redundant; that is this flow's inference.

## Sources

- Message design at e275b6 (blob 66d3fd), read through git show.
- Flow design at d84997, read through git show.
- Old Message source at 6fa4d0, read through git show in the
  local clone of LiGoldragon/message.
- Provenance receipt: unavailable; no PROVENANCE handoff exists for
  this run.
