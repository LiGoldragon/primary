# Orchestrate changes proposal

Status: the Orchestrate contract is proposed for the living's review; it is not approved or implemented. Its ruled Datom prerequisite was subsequently implemented and pushed in Protos `1e0890175319` and Datom `bc16426703fa`.

## What is already ruled

- The service is the **Orchestrate Nexus**. It starts without a bootstrap executable, owns useful defaults, persists those defaults for a new store, and receives later configuration only through its separate meta socket.
- The ordinary interface is imperative. Its domain thing is **Lock**, not `PathLock`; **Observe** is a reusable root with a typed selection beneath it.
- A Lock carries Flow attribution and exposes its paths and reason.
- A flow releases every Lock before it becomes idle, except while it has explicitly delegated that Lock to an active subflow. No authority capable of proving whole-tree idleness has yet been established.
- The ordinary `orchestrate` skill contains no meta operation or meta explanation.
- The parenthesized examples previously offered for the new interface are obsolete Dotos/NOTA, not modern Datom.
- Datom text is interpreted against an expected type. An enum root starts at its variant; a non-enum root need not. A typed map has no `Map` head, and the living's later delimiter choice for maps is guillemets.

The last point does **not** establish that the fixed fields of a Lock request should be encoded as a map. They form a known product type and should remain a product unless the Ethos type says otherwise.

## Proposed ordinary contract

Approve this breaking authored Ethos contract:

```ethos
Interface.{0 2 0}
Channel.{Orchestrate 1 5}
[]
{
  [
    Lock.LockRequest
    Release.LockId
    Observe.ObserveSelection
  ]
  [
    Locked.Lock
    LockRejected.LockRejection
    Released.Lock
    ReleaseRejected.ReleaseRejection
    Observed.Observation
  ]
  []
  []
  [
    LockName.String
    FlowId.String
    LockPath.String
    LockPaths.Vector<LockPath>
    LockReason.String
    LockRequest.{LockName FlowId LockPaths LockReason}

    LockId.Integer
    Lock.{LockId LockName FlowId LockPaths LockReason}

    DuplicateName.Lock
    LockOverlap.{LockPath Lock}
    LockRejection.[DuplicateName.Lock PathOverlap.LockOverlap]
    ReleaseRejection.[UnknownLockId]

    ObserveSelection.[Locks]

    Locks.Vector<Lock>
    LockSnapshot.{Locks}
    Observation.[Locks.LockSnapshot]
  ]
}
```

This is valid in the current Ethos parser/generator. The inputs generate `Lock(LockRequest)`, `Release(LockId)`, and `Observe(ObserveSelection)`; the unit selection realizes `Observe.Locks`, with future observation categories added as siblings such as `ExpiredLocks`. `LockId` is absent from `LockRequest`, assigned by the Nexus, returned inside `Lock`, and accepted by `Release`.

The binding is `1/5`, not the previously proposed `2/0`: the current generator prohibits zero for both binding numbers, contract ID `2` is already Meta-Orchestrate, and changing `1/4` to `1/5` gives the breaking ordinary wire a distinct binding. `Interface.{0 2 0}` carries the interface release version.

I propose these semantics:

1. `Lock` atomically acquires the complete normalized path set or rejects it. Existing duplicate-name and ancestor/descendant overlap behavior remains, expressed under the new names.
2. The Nexus assigns an opaque, durable, non-reused `LockId`. `Release` addresses that ID, not the reusable human name; this prevents a delayed release from targeting a later Lock that reused the name.
3. `Locked` and `Released` return the complete Lock. A coordinator therefore receives the paths, reason, Flow, name, and ID without reconstructing state.
4. `Observe.Locks` returns one complete point-in-time snapshot, sorted canonically by Lock name and then Lock ID. It is a request/reply, neither polling nor a subscription.
5. Every peer on the per-user ordinary socket can observe all current Lock names, IDs, Flow IDs, paths, and reasons. That is coordination state. This is disclosure within the existing per-user trust boundary, not a claim of authentication.
6. Flow ID is attribution, not authorization. Release is cooperative. Automatic forfeiture and force release do not enter this revision; they require a future lifecycle authority that can prove the owner and every descendant idle.
7. The new Signal channel is a clean breaking contract at `Channel.{Orchestrate 1 5}` and `Interface.{0 2 0}`. It contains no `Register`, `PathLock`, `PathLockRelease`, old reply names, aliases, or compatibility parser.
8. Existing active rows are quiesced and released before deployment. Configuration may be carried forward, but no old active row is assigned an invented Flow ID.
9. The meta contract remains separate and unchanged unless a later meta-design round finds a required change.

## Datom boundary

The contract is authored in Ethos. Its generated Datom projection must obey these rules:

- The expected root type is `Operation`, so command text begins directly with the selected variant (`Lock`, `Release`, or `Observe`), not an `Operation` or `DatomRoot` wrapper.
- Variant payloads use the structural shape generated for their Ethos type. Fixed Lock fields are not represented as an ad hoc generic map.
- If a typed map occurs anywhere, it has no `Map` head and uses the newer guillemet delimiter.
- Bare text realizes String only in a String position.
- Old Dotos command forms are rejected; they are not accepted through a fallback.

The exact entry grammar inside `«…»` remains unsettled. The observation request spelling is now ruled as `Observe.Locks`.

The ruled prerequisite has now landed: Protos recognizes headless guillemet structural blocks, and Datom realizes guillemet maps without `Map.` plus type-directed roots—an enum begins at its variant and a record directly at `{…}`. The implementation deliberately preserved the existing map-entry model rather than inventing the unruled positional-pair grammar. Canonical Orchestrate commands should be published only after the Ethos projection round-trips approved fixtures through this new Datom surface.

## Realization order

```text
Protos + Datom grammar/realization
                │
                ▼
Ethos projection + signal-orchestrate 2.0
                │
                ▼
Orchestrate Nexus store + ordinary CLI
                │
                ▼
Curriculum authored skills ──► generated consumer workspaces
                │
                ▼
Home/CriomOS live checks and deployment

meta-orchestrate remains a separate sibling contract
```

1. **Protos and Datom — completed:** guillemet structural form, typed maps without `Map`, and expected-type roots were implemented and witnessed. The map entry rule remains unchanged pending explicit approval.
2. **Ethos and signal-orchestrate:** define the operation/reply tree above; add the missing generated Datom codecs/projection; cut the breaking channel; replace ABI fixtures; prove every command and reply by text-to-type-to-wire-to-type-to-text round trip.
3. **Orchestrate:** remove the Dotos dependency and parser; replace `StoredPathLock` and `active_path_locks`; persist Lock ID and Flow attribution; add the serialized Current snapshot; preserve path normalization/conflict correctness; reject old frames and old text; prove restart persistence, ID non-reuse, snapshot consistency/order, conflict replies, and quiescent store transition.
4. **Curriculum:** update authored `orchestrate`, `edit-coordination`, `flows`, and `nexus` sources after the runtime is witnessed. Keep the ordinary skill strictly ordinary and correct its current stale Nexus bootstrap account. Regenerate `.agents/`, `.claude/`, `.codex/`, and `.pi/`; never edit them directly.
5. **Consumers:** update Home's service-path command/reply witness, then Home and CriomOS pins/locks and the stale ownership gate. Give Persona, dirty `mind`, and the judge repositories an explicit inclusion decision rather than silently treating their obsolete surfaces as current authority.

The separate statement that there should be no Dotos files everywhere is broader than this Orchestrate release and currently intersects authored `manifests/*.dotos`. This proposal removes Dotos from Orchestrate's runtime and wire surface. Replacing the authored manifest format requires its own approved successor and coordinated migration.

## Approval boundary

Approval of this proposal would settle the type-level ordinary contract, semantics, disclosure boundary, clean-break policy, and dependency order. It would **not** yet approve guessed Datom punctuation, map entry semantics, Flow-ID allocation, lifecycle forfeiture, or a global manifest-format replacement. Those need their own anatomy and, where applicable, exact approved examples before realization.

## Sources

- Flow `01a03d6e`: its vision records, reports, targeted transcript records, and final response; especially `vision/ethosInterfaces.md`, `vision/locks.md`, `vision/flows.md`, `vision/nexus.md`, `vision/orchestrateSkill.md`, and `reports/orchestrateLockInterfaceProposal.md`.
- Flow `ac1e9ec8`: `vision/datomSyntax.md`, its log and unapproved distillation proposal, and the originating transcript's guillemet ruling.
- Current code witnesses: `signal-orchestrate/ethos/signal.ethos`, `orchestrate/src/store.rs`, `orchestrate/src/bin/orchestrate.rs`, `orchestrate/src/transport.rs`, Datom/Protos shape and realization sources, Curriculum's authored `orchestrate` and `edit-coordination` skills, and Home's `orchestrate-service-path` check.
- Datom prerequisite realization: Protos `1e0890175319` (v0.7.0) and Datom `bc16426703fa` (v0.3.0); their local suites and remote-builder `nix flake check` gates passed.
