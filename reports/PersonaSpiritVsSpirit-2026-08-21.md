# persona-spirit vs spirit capability comparison

Design session `15b67974`, 2026-08-21. Answering the psyche's
question: "What is in [persona-spirit] that isnt in spirit?"

## 1. What persona-spirit has that spirit does not

### Kameo supervision-tree actor runtime

persona-spirit builds its entire runtime as a Kameo actor tree rooted
at `SpiritRoot`, with every actor spawned via `supervise().spawn()`
under the root actor reference. The tree has 13 named actors:
`RecordStore`, `PolicyPlane`, `MetaPlane`, `ReplyShaper`, `StatePlane`,
`ClassifierPlane`, `ClockPlane`, `SubscriptionPlane`, `DispatchPhase`,
`NotaDecoder`, `IngressPhase`, `ReplyTextEncoder`, and `SpiritRoot`
itself.

- File: `/git/github.com/LiGoldragon/persona-spirit/src/actors/root.rs:633-713` (`on_start` builds the full tree)
- Each actor carries typed `ActorRef<T>` handles and typed `Message<M>` impls.
- Observed: `src/actors/` directory has 14 files (root, meta, policy, ingress, decoder, classifier, clock, dispatch, store, state, subscription, reply, trace, pipeline, mod).

Spirit has no Kameo dependency and no actor tree. Spirit does not
depend on kameo at all (`Cargo.toml` has no kameo entry). Its
runtime is a schema-generated `NexusEngine` with a synchronous
decision loop (`Nexus::execute_to_reply`), SEMA engine, and tokio
tasks for the daemon socket listeners. The Nexus is a single struct,
not an actor.

- File: `/git/github.com/LiGoldragon/spirit/Cargo.toml` (no kameo in dependencies)
- File: `/git/github.com/LiGoldragon/spirit/src/nexus.rs:295-322` (Nexus is a plain struct with Store, StashTable, etc.)

### NOTA text ingress and decoder pipeline

persona-spirit has a dedicated NOTA text ingress path: `SubmitText`
flows through `IngressPhase` to `NotaDecoder` (NOTA parsing actor)
to `DispatchPhase`. The CLI can accept raw NOTA text, decode it in
the actor pipeline, and route the parsed request.

- File: `/git/github.com/LiGoldragon/persona-spirit/src/actors/root.rs:153-165` (submit_text path)
- File: `/git/github.com/LiGoldragon/persona-spirit/src/actors/ingress.rs`, `src/actors/decoder.rs`

Spirit's daemon never handles NOTA text internally. NOTA is an edge
format handled only by the CLI binaries (`spirit`, `meta-spirit`);
the daemon socket speaks only length-prefixed rkyv Signal frames.
The ARCHITECTURE.md states: "NOTA is an edge format for CLIs and
configuration writers, never the daemon transport."

- File: `/git/github.com/LiGoldragon/spirit/ARCHITECTURE.md:58-61`

### Actor trace witness system

persona-spirit has a full `ActorTrace` system that records which
actors a message passes through, used extensively in tests to
assert architectural invariants (which actor planes participate in
each operation).

- File: `/git/github.com/LiGoldragon/persona-spirit/src/actors/trace.rs`
- File: `/git/github.com/LiGoldragon/persona-spirit/tests/actor_runtime.rs`

Spirit has a `TraceEvent` / `TraceLog` system gated behind
`testing-trace`, but it traces Nexus and SEMA object activations,
not actor-to-actor message routing (since there are no actors).

### Psyche working-state and pending-question planes

persona-spirit has dedicated `StatePlane` and question observation
actors for tracking live psyche state and pending clarification
questions as first-class runtime state.

- File: `/git/github.com/LiGoldragon/persona-spirit/src/actors/state.rs`
- ARCHITECTURE.md constraints referencing `Observe(State(...))`, `Observe(Questions(...))`

Spirit has no psyche-state or pending-question subsystem. Its
`Input` enum has no `State` or `Questions` variants beyond the
classification pathway.

### Subscription and watch planes

persona-spirit has a `SubscriptionPlane` actor that manages
subscription tokens and live stream registrations, with
`Watch(State)` / `Watch(Records)` / `Unwatch` operations.

- File: `/git/github.com/LiGoldragon/persona-spirit/src/actors/subscription.rs`

Spirit has subscription tokens (via `SubscriptionTokenIssuer` from
triad-runtime) and `SubscribeIntent` / `Tap` / `Untap` operations
in the Nexus, but no dedicated subscription actor or Watch/Unwatch
semantic.

### Reply shaping and NOTA encoding actors

persona-spirit has `ReplyShaper` and `ReplyTextEncoder` actors that
shape typed replies and encode them back to NOTA text.

- File: `/git/github.com/LiGoldragon/persona-spirit/src/actors/reply.rs`

Spirit encodes replies through its daemon transport and CLI
boundary, not through dedicated actors.

### Version handover protocol (full three-state machine)

persona-spirit implements a complete three-state handover protocol
(`Active` / `HandoverMode` / `PrivateUpgradeOnly`) with readiness
acceptance, marker drift rejection, write freezing during handover,
recovery, and mirrored `StampedEntry` replay after completion.

- File: `/git/github.com/LiGoldragon/persona-spirit/src/actors/root.rs:93-99` (HandoverState enum)
- File: `/git/github.com/LiGoldragon/persona-spirit/src/actors/root.rs:221-388` (full protocol)

Spirit does not have a version-handover protocol. It has no
`signal-version-handover` dependency.

### Persona supervisor integration (SCM_RIGHTS fd handoff)

persona-spirit integrates with the `persona` supervisor via
`DaemonConfiguration` handoff-control sockets. Persona can hand off
accepted client file descriptors via `SCM_RIGHTS`, and Spirit serves
them directly. This enables the persona supervisor to flip version
selectors during live upgrades.

- File: `/git/github.com/LiGoldragon/persona-spirit/ARCHITECTURE.md:177-184`
- Dependency: `unix-ancillary = "0.2"` in Cargo.toml

Spirit has no persona supervisor integration or fd handoff.

### Schema-driven actor substrate (next-substrate, design branch)

persona-spirit's ARCHITECTURE.md documents a parallel schema-driven
actor substrate on the `designer-schema-full-stack-spirit-2026-05-25`
branch, with `.schema` files (spirit-storage, spirit-recorder,
spirit-observer, spirit-supervisor, spirit-reading-actor,
spirit-upgrade-log) and hand-written engines.

- File: `/git/github.com/LiGoldragon/persona-spirit/ARCHITECTURE.md:247-418`

This is documented design, not main-branch code. Spirit's production
code is already schema-derived (Nexus and SEMA schemas checked into
the repo), so this is persona-spirit's design to reach parity with
spirit's approach.

### Privacy magnitude on records

persona-spirit stores a `privacy` magnitude on each record entry,
with `Zero` = public and higher values narrowing the audience. The
default observation is exact-Zero so private records are hidden
unless explicitly requested.

- File: `/git/github.com/LiGoldragon/persona-spirit/ARCHITECTURE.md:72-75`

Spirit has an `Importance` magnitude on entries but no separate
privacy magnitude.

### Record certainty changes and removal-candidate collection

persona-spirit has `ChangeCertainty` and `CollectRemovalCandidates`
operations for managing record lifecycle through certainty levels,
including archive-database collection before retraction.

- File: `/git/github.com/LiGoldragon/persona-spirit/ARCHITECTURE.md:47-68`

Spirit has `Retire` and `Supersede` for explicit lifecycle changes,
but no certainty-based removal-candidate workflow.

## 2. What spirit has that persona-spirit lacks

Spirit is substantially larger and more mature. Briefly:

- **Schema-generated Nexus and SEMA engines** with checked-in Rust from `build.rs` and drift detection. Spirit's core decision logic is schema-derived; persona-spirit's is hand-written Kameo actors.
- **Guardian admission system** with external judge integration (`signal-spirit-judge`), `AdmissionJudgePacket`, typed verdicts, and an unversioned guardian journal. Feature-gated behind `agent-guardian`.
- **Criome cluster authorization gate** (`criome-gate` feature): staged acceptance, cluster-gated head advances, typed refusal, crash-window recovery. Full end-to-end witnesses.
- **Mirror shipper** (`mirror-shipper` feature): ships authorized versioned-log state to sema version-control mirrors. Gated behind criome authorization.
- **Router integration** for offline full-chain end-to-end and cluster-authorization loopcheck tests.
- **Propagation engine** (`src/propagation.rs`): gated head fan-out with gate-and-ship semantics.
- **Production v13-to-v14 migration** with destructive projection, rollback bundles, and frozen v13 reader.
- **Nix service bundle** (`nix/service-bundle.nix`): `mkUserServiceArtifacts` for deployment.
- **Configuration binary** (`spirit-write-configuration`): daemon startup artifact writer.
- **Rich read semantics**: `TextSearch`, `Intent`, `Lookup`, `Count`, `BumpImportance`, `Propose`, `Clarify`, `ResolveClarification`, `Supersede`, `Retire` operations.
- **Stash table**: in-memory recovery-handle store for Observe-then-Stash recursion.
- **Observer tap table**: ported `Tap`/`Untap` operator stream for meta-observation.
- **Lifecycle archive**: separate schema-14 records store for archive-before-retract durability.
- **Mail ledger**: origin-route tracking for cross-plane message accounting.
- **Version 0.27.0** (schema 14, signal wire revision 2) vs persona-spirit's 0.5.2.

File: `/git/github.com/LiGoldragon/spirit/Cargo.toml:1-9`
File: `/git/github.com/LiGoldragon/spirit/ARCHITECTURE.md:1-219`

## 3. Recency (observed from git history)

| Repo | Last commit date | Last commit message | Version |
|---|---|---|---|
| persona-spirit | 2026-08-13 00:59:17 +0200 | `docs: mark Protos estate status` | 0.5.2 |
| spirit | 2026-08-13 00:48:01 +0200 | `docs: mark Protos estate status` | 0.27.0 |
| psyche | 2026-08-14 00:03:05 +0200 | `Repair Nix segregation check boundary` | 0.1.0 |

Observation: Both persona-spirit and spirit received their last
commits on the same day (2026-08-13), as part of the same Protos
estate documentation pass. Neither has received a functional commit
since then (eight days ago). The psyche repo received one commit one
day later.

Observation: persona-spirit's recent commit history shows dependency
refresh and migration work (signal stack, sema store paths, dep
repointing); no new capability work is visible in the last 15
commits.

Observation: spirit's recent history shows the v14 intent model, the
Luna xhigh service release, and schema rescue work. More capability
development than persona-spirit in the same period.

## 4. psyche repo status

The `psyche` repo at `/git/github.com/LiGoldragon/psyche` is an
intentionally empty scaffold.

- `src/lib.rs` contains only a doc comment and `#![forbid(unsafe_code)]`
- `Cargo.toml` has zero dependencies, version 0.1.0
- `ARCHITECTURE.md` states: "No record, private psyche content, Ethos fixture, generated type, signal contract, daemon, CLI, Sema design, wire design, or freshness mechanism is defined in this repository yet."
- A segregation invariant is defined and guarded: psyche must not depend on or modify the "protected terminal correct-new stack" (spirit). The relationship is "source semantics only" from production spirit: "human re-authoring from evidence, never a Cargo or Nix dependency."
- 2 total commits. The most recent (2026-08-14) repairs the Nix segregation check.

File: `/git/github.com/LiGoldragon/psyche/ARCHITECTURE.md:1-38`
File: `/git/github.com/LiGoldragon/psyche/src/lib.rs:1-5`
File: `/git/github.com/LiGoldragon/psyche/Cargo.toml:1-16`

Observation: psyche exists as a claimed scaffold with an enforced
segregation boundary. No functionality exists there today.

## Unknowns

- Whether persona-spirit's Kameo supervision-tree runtime was ever
  considered for adoption by spirit, or whether spirit's schema-derived
  approach was always intended to supersede it.
- Whether the schema-driven next-substrate branch in persona-spirit
  (`designer-schema-full-stack-spirit-2026-05-25`) was merged or
  abandoned.
- Whether any persona-spirit capability (privacy, certainty lifecycle,
  version handover, persona fd handoff) is planned for psyche's
  eventual design.
- The intended timeline for psyche to reach functional parity with
  either predecessor.
