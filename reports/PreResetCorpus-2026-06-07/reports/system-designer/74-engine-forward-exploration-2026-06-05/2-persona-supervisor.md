# Area map: Persona-as-supervisor + the orchestrated running system

*System-designer area report for the engine-forward exploration
(meta-report 74). Read-only mapping of the five area repos with
file:line / commit evidence. Scope: Persona as the MANAGER/SUPERVISOR
of the whole thing (Spirit Decision mazv — a live orchestrated system,
not just proven in-tree) and the concrete path to persona orchestrating
introspect + schema daemon + the rest.*

Area repos (under `/git/github.com/LiGoldragon/`): `persona`,
`owner-signal-persona`, `signal-engine-management`, `orchestrate`,
`mind`. Supporting evidence pulled from `introspect`, `router`,
`persona-spirit`, and the `persona` flake (the launcher + smoke
surface).

## Headline finding (correcting the likely first impression)

The live persona-supervises-N-real-components loop is **substantially
already built and proven in CI** — much further along than the in-tree
Rust tests alone suggest. The load-bearing evidence is a Nix flake
**check**, not a Rust test:
`persona/flake.nix:1815` `persona-daemon-launches-nix-built-prototype-topology`
runs the **real** `persona-daemon` binary and has it launch the **real
Nix-built daemons** for all eight prototype-supervised components
(`mind router system harness terminal message introspect spirit`),
each reaching readiness through the engine-management supervision
socket, with the manager verifying every component's capture file,
spawn envelope, socket modes, and peer wiring (`flake.nix:1873-1899`).

So "persona launches and supervises the introspector, and the other
triad components together" is **not aspirational** — it is a green
check on real binaries. What is missing for the full mazv target is
narrower than expected and is enumerated below. The single most
important caveat: this proves persona *launches and confirms readiness*
of real components; it does not yet prove persona *runs them as a
durable living system* (no health-loop / restart-on-crash against real
daemons in CI, `orchestrate` not yet in the supervised set, and the
generic runner extraction 7ca4 not started).

## 1 · CURRENT STATE (landed vs scaffold/placeholder/doc-only)

### persona — the supervisor daemon: LARGELY REAL

`persona` is by far the most mature repo in the area: ~28 source files,
real Kameo actors, real process supervision, real redb-backed manager
store, a real length-prefixed Signal transport, and an FD-handoff
router. This is landed code, not scaffold.

Landed and real:
- **Real process launcher.** `src/direct_process.rs` (`DirectProcessLauncher`,
  1329 lines) spawns child processes in their own process group
  (`configure_process_group`, `direct_process.rs:989`), watches them
  for natural exit via a detached watcher task
  (`direct_process.rs:278-306`), reaps process groups with
  SIGTERM→SIGKILL escalation (`await_stop_receipt`,
  `direct_process.rs:410-437`; `terminate_process_group`,
  `direct_process.rs:1001`), and writes per-component **typed NOTA
  daemon-configuration files** for message/introspect/router/terminal/
  harness/system/spirit (`write_typed_configuration_file`,
  `direct_process.rs:489-516`).
- **Real supervision sequence.** `src/supervisor.rs`
  (`EngineSupervisor`) launches every component in the layout, then
  for each verifies (a) the domain socket appears, (b) the supervision
  socket appears, and (c) the component answers the engine-management
  relation, appending typed `ComponentSpawned` / `ComponentReady`
  events to the manager store (`start_prototype_supervision`,
  `supervisor.rs:66-136`). This is genuine launch-then-confirm-readiness,
  not a stub.
- **Real daemon runtime.** `src/transport.rs` `PersonaDaemon::serve`
  (`transport.rs:515-539`) binds the manager socket, starts the
  `ManagerStore` actor, the `EngineManager` actor, and (when a launch
  plan is present) the `EngineSupervisor`, then serves Signal frames in
  an accept loop. `src/bin/persona_daemon.rs` is the real binary.
- **Real FD-handoff cutover.** `ComponentHandoffRouter`
  (`transport.rs:249-312`) binds the stable public socket, accepts
  client connections, and sends accepted FDs over `SCM_RIGHTS`
  (`handoff_one`, `transport.rs:294-303`) to the active-version daemon
  — the lossless-cutover mechanism from INTENT is implemented, not
  documented-only.
- **Real Nix launcher bridge.** `flake.nix:155-217` defines real
  prototype launchers for **all nine** component kinds
  (mind/orchestrate/router/system/harness/terminal/message/introspect/
  spirit); each adapts the manager's spawn-envelope environment and
  `exec`s the real Nix-built component daemon. This is the bridge
  between persona's supervisor and the real triad.
- **The proven real-stack loop.**
  `flake.nix:1815` (the check described in the headline) — eight real
  daemons launched and confirmed ready by the real persona-daemon.

Scaffold / not-yet-real:
- **systemd production path is a trait with a manual default.**
  `EngineManager::new` wires `ManualUnitController`
  (`manager.rs:50`); the production `UnitController` (systemd D-Bus /
  transient-unit / systemctl backends described in `ARCHITECTURE.md`
  §1.7) exists behind the trait but the default supervised path is the
  direct-fork launcher, which `INTENT.md:104-106` and `ARCHITECTURE.md`
  §1.7 both label "not the production path."
- **Owner mutating verbs are stubs in the manager.** `Operation::Launch`
  is hard-rejected with `LaunchPlanRejected` (`manager.rs:181-184`),
  and `Operation::Retire` is hard-rejected
  (`manager.rs:192-199`). The owner contract *declares* Launch/Retire
  (see §below) but the daemon does not execute them yet — Start/Stop/
  Query work, Launch/Retire do not.
- **The concept schema is placeholder.** `schema/persona.concept.schema`
  is a v0.1 `Status Concept` sketch (`(Status Concept)`,
  `persona.concept.schema:37`) — NOT the schema-engine source of truth.
  The repo's hand-written `signal_channel!`/types are still canonical;
  the schema-derived cutover is `INTENT.md:226-237` "Pending schema-engine
  upgrade," explicitly **after** the Spirit pilot.

### owner-signal-persona — owner-only manager contract: REAL, complete

`src/lib.rs` (216 lines) is a real, closed Signal contract. The
`signal_channel! { channel Owner { ... } }` (`lib.rs:180-205`) carries
exactly the owner-only lifecycle verbs the brief asks for:
`Launch(EngineLaunch)`, `Query(Query)`,
`Retire(EngineIdentifier)`, `Start(ComponentStartup)`,
`Stop(ComponentShutdown)`, with a closed `Reply` enum and an
observable stream (`OperationReceived` / `EffectEmitted`). It re-exports
the component vocabulary from `signal-engine-management`
(`lib.rs:13-15`). The concept schema
(`schema/owner-signal-persona.concept.schema`) is again a v0.1
placeholder (`(Status Concept)`), so the hand-written contract is
canonical. **Contract: landed. Daemon execution of its mutating verbs:
not yet (Launch/Retire stubbed in persona, see above).**

### signal-engine-management — manager↔component lifecycle contract: REAL, complete, and the keystone

`src/lib.rs` (283 lines) is the real ordinary lifecycle contract — and
it is the single most important type in the whole area, because it is
the relation that "makes a process a Persona component." It carries:
- `signal_channel! { channel EngineManagement { Announce(Presence),
  Query(Query), Stop(ComponentName) } }` (`lib.rs:268-282`) with replies
  `Identified / Ready / NotReady / HealthReport / StopAcknowledged /
  Unimplemented`.
- `SpawnEnvelope` (`lib.rs:246-260`) — the typed launch record (engine
  id, component kind/name, owner identity, state dir, domain socket +
  mode, engine-management socket + mode, peer sockets, manager socket,
  protocol version). This is the data the manager hands each child.
- The skeleton-honesty rule (`ARCHITECTURE.md` §"Skeleton Honesty",
  `INTENT.md` §"Skeleton honesty is mandatory"): every supervised
  daemon decodes every variant and answers `Unimplemented` rather than
  panicking.

This contract is landed and is **already implemented by real
components**: `introspect/src/supervision.rs:112` answers `Announce`,
`router/src/supervision.rs`, `persona-spirit/src/{lib,daemon}.rs`, and
crucially `mind/src/supervision.rs:157-176` all answer the four
prototype variants. The concept schema is the v0.1 placeholder again.

### mind — central persona state: REAL daemon, REAL supervision answer

`mind` is a real serving daemon: 28 source files, a `MindRoot` Kameo
actor tree (`src/actors/`), a real `mind.redb` `StoreKernel`, a typed
`MindEnvelope` request boundary, sema-engine-backed Thought/Relation
graph (`INTENT.md`, `README.md`). For THIS area the load-bearing fact:
**mind answers the engine-management supervision contract for real.**
`src/supervision.rs` has a real `SupervisionListener` that reads
`PERSONA_SUPERVISION_SOCKET_PATH` from the environment
(`supervision.rs:82-89`), binds the supervision socket, spawns a
`SupervisionServer` over the live `MindRoot`
(`supervision.rs:96-119`), and answers `Announce→Identified`,
`ReadinessStatus→Ready`, `HealthStatus→HealthReport`,
`Stop→StopAcknowledged` (`supervision.rs:154-178`). It is wired into
the served daemon, not dead code: `BoundMindDaemon::bind` spawns the
supervision listener against the same root the domain socket serves
(`transport.rs:227-241`). So mind is a join-able supervised component
today. (Note: mind's `Cargo.toml` does not list
`signal-engine-management` directly; it gets the engine-management
types transitively via `signal-persona`'s re-export — `lib.rs:12-18`
of mind's supervision module imports `signal_persona::engine_management`.)

### orchestrate — orchestration component runtime: REAL daemon, but NOT yet supervision-join-able

`orchestrate` is a real serving daemon: 20 source files, a real
three-socket daemon (`src/daemon.rs:52-65` binds ordinary + owner +
upgrade listeners, each on its own thread), real redb-backed claim /
lane / activity / handover state (`src/{claim,lane,activity,handover,
service}.rs`), and a real generated signal CLI
(`src/bin/orchestrate.rs`, git `c2f9837`). It carries the dynamic-role
registry the MVP wants (`INTENT.md` Goals; `src/role.rs`, `src/lane.rs`).

The gap for THIS area: **orchestrate does not answer the
engine-management supervision contract.** A grep across all of
`orchestrate/src/*.rs` for `supervision` / `PERSONA_SUPERVISION` /
`Announce` / `EngineManagement` returns **zero** hits (the `Ready`
matches in `service.rs` are the upgrade-handover state machine, an
unrelated protocol). So although persona's flake defines a
`persona-orchestrate-prototype-launcher` (`flake.nix:164-167`) and the
`MindOrchestrate` topology exists (`persona/src/engine.rs:368`),
orchestrate launched under persona would bind its domain/owner/upgrade
sockets but **fail the supervision-readiness check** because it never
binds or answers the supervision socket. It is real but not yet a
Persona-supervised component.

### The generic triad runner (7ca4): NOT STARTED anywhere

A grep across `persona`, `orchestrate`, and `mind` src for any
runner/adapter/plane-engine/effect-handler/budget-reply vocabulary
returns nothing. Each daemon hand-writes its own `transport.rs` accept
loop + frame codec + dispatch: persona (`transport.rs`), orchestrate
(`daemon.rs` + `service.rs`), mind (`transport.rs`). This is exactly
the "hand-written boilerplate" 7ca4 / rpr5 want to delete. The shared
`signal_channel!` macro (`signal-frame`) generates the wire *types*,
but there is no shared Signal/Nexus/SEMA **runner object** that a
daemon plugs three plane engines + an effect handler into. tirp's
"daemon code minimal" is not yet realized; the daemons are not minimal.

## 2 · MOVE-FORWARD WORK ITEMS (ordered) + 3 · STABILITY VERDICT per item

The column on the right is load-bearing: the psyche wants to port now
WITHOUT rework. Each verdict cites what is stable under it.

**W1 — Drive the full-prototype real-stack as a standing smoke /
nixosTest, including a health-loop tick and a crash-restart assertion.**
*Repo/file:* `persona/flake.nix` (extend the existing
`persona-daemon-launches-nix-built-prototype-topology` check
`flake.nix:1815`). *Size:* S–M. *Depends on:* nothing — the launchers
and the supervisor already exist. *Verdict:* **[SAFE-NOW].** The
launch+readiness loop on real binaries is already a green check; the
foundation under it (the spawn-envelope shape in
`signal-engine-management::SpawnEnvelope`, the manager-store event log,
the eight launchers) is stable and asschema-free. Extending the same
check to assert a health tick and a restart costs nothing in rework
because it builds on the proven path, not a new one. This converts
"proven launch" into "proven *running system*" — the heart of mazv.

**W2 — Teach `orchestrate` to answer the engine-management supervision
contract (bind `PERSONA_SUPERVISION_SOCKET_PATH`, answer Announce/
Ready/Health/Stop).** *Repo/file:* new `orchestrate/src/supervision.rs`,
mirroring `mind/src/supervision.rs:69-178`; wire into `daemon.rs:52`
alongside the existing three listeners. *Size:* S (mind's
implementation is a ~180-line template; copy it). *Depends on:* the
`signal-engine-management` contract (stable). *Verdict:* **[SAFE-NOW].**
The contract orchestrate must answer is landed and closed; mind already
implements the exact pattern against a Kameo root; orchestrate has a
service object to delegate readiness/health to. This is the smallest
high-value step that makes the second state-bearing component (after
mind) join the supervised loop. No rework risk: the supervision
contract is wire-frozen and asschema-removal is complete.

**W3 — Add `orchestrate` (and then `spirit`) to a supervised
multi-component topology end-to-end on real binaries.** *Repo/file:*
`persona/src/engine.rs` topology arrays + `persona/flake.nix` check.
*Size:* M. *Depends on:* W2 (orchestrate answering supervision); the
`MindOrchestrate` topology scaffold already exists
(`engine.rs:368`, `flake.nix` `mind-orchestrate` launchers). *Verdict:*
**[PREP].** Can structure now (the topology enum + launcher exist);
finalize after W2 lands so the readiness check passes. Stable parts:
the topology mechanism, the layout/spawn-envelope generation. Hold the
*final* check assertion until orchestrate answers supervision.

**W4 — Implement the owner mutating verbs in the manager: real
`Launch(EngineLaunch)` and `Retire(EngineIdentifier)`.** *Repo/file:*
`persona/src/manager.rs:181-199` (currently hard-rejects both) +
`src/state.rs`. *Size:* M. *Depends on:* multi-engine state shape
(`ARCHITECTURE.md` §1.5, mostly settled). *Verdict:* **[PREP].** The
owner contract (`owner-signal-persona`) is landed and closed, and the
single-engine Start/Stop/Query path is real, so the *wire* is stable.
But multi-engine launch/retire semantics (per-engine paths, catalog
mutation) touch state shape that is still evolving — structure the
handlers now against the frozen contract, finalize the multi-engine
state transitions once the federation model in `ARCHITECTURE.md` §1.5
fully settles. Not [WAIT] because the contract won't move; not
[SAFE-NOW] because the state-mutation semantics might.

**W5 — Extract the generic triad runtime runner (7ca4 / rpr5 / tirp):
shared Signal/Nexus/SEMA runner object that mind, orchestrate, and
persona plug into; authors write 3 plane engines + effect handler +
budget reply.** *Repo/file:* a new shared crate (e.g. a
`triad-runner`/`nexus`-adjacent crate), consumed by `mind/src/transport.rs`,
`orchestrate/src/daemon.rs`, `persona/src/transport.rs`. *Size:* L.
*Depends on:* the Signal wire shape (stable), the Nexus-as-feature-catalog
model (z6qu, VeryHigh, but the Nexus schema substrate is still forming),
and the schema-engine pilot landing (the macro library `primary-ezqx.1`).
*Verdict:* **[WAIT].** This is the one item to NOT port onto sand. The
runner's whole value is that it is *generated glue* (rpr5); generating
it depends on the schema-derived emission pipeline that is mid-flight
(the Spirit schema pilot builds `schema/*.schema → src/schema/*.rs`,
but the runner-emission half — dispatcher + plane wiring from schema —
is not yet a thing). Building a hand-written "generic runner" now would
be exactly the boilerplate 7ca4 wants deleted, and would be thrown away
when the schema engine emits it. Blocker: the schema→runner emission
path. Carry it as the north star; do W1–W4 first against the stable
hand-written transports, which the runner will later subsume without
changing the wire contracts.

**W6 — Bootstrap policy authored as NOTA, consumed as pre-encoded
binary at first start (7x50).** *Repo/file:* `persona` launch plan
(`transport.rs:619-693` `PersonaLaunchPlan`) + the concept schema's
`Policy [Bootstrap Selector]` node (`persona.concept.schema:10-11`).
*Size:* M. *Depends on:* the schema-engine cutover (the policy node is
schema-shaped). *Verdict:* **[PREP].** The launch-plan plumbing is real
and stable (env-driven topology + command catalog); the *NOTA-authored,
pre-encoded-binary* bootstrap is schema-engine-adjacent. Structure the
launch-plan to accept a pre-encoded policy file now (the
`bootstrap_policy_path` field already exists in the spirit daemon config,
`direct_process.rs:40`); finalize the schema-derived policy encoding
after the schema engine lands. Partially stable (the consumption path),
partially shifting (the schema-derived authoring).

**W7 — Replace the persona/orchestrate/mind concept schemas
(`*.concept.schema`, all `Status Concept` placeholders) with real
schema-engine source files once the Spirit pilot proves the pipeline.**
*Repo/file:* `persona/schema/`, `owner-signal-persona/schema/`,
`signal-engine-management/schema/`, `orchestrate/schema/`,
`mind/schema/`. *Size:* L (across the area). *Depends on:* the Spirit
schema pilot (`primary-ezqx.1`) succeeding — explicitly sequenced after
Spirit in every repo's "Pending schema-engine upgrade" section
(`persona/INTENT.md:226-237`, `orchestrate/INTENT.md` Pending section).
*Verdict:* **[WAIT].** The sequencing is psyche-settled: Spirit is the
MVP pilot; persona/orchestrate/mind follow. Porting the schemas before
the pilot proves the emission would be porting onto sand. Blocker:
Spirit pilot completion. (Note the encouraging signal: asschema removal
is COMPLETE in code and the structural-macro node landed in nota-next,
so the *substrate* is firming — but the per-repo emission cutover still
waits on the pilot.)

## What is stable enough to build on NOW (the foundation-caveat answer)

Per the brief's foundation caveat, every [SAFE-NOW]/[PREP] above rests
on these verified-stable pieces:
- **The wire contracts are frozen and real.** `owner-signal-persona`
  (owner verbs) and `signal-engine-management` (lifecycle + SpawnEnvelope)
  are landed closed Signal contracts with round-trip witnesses; they are
  not slated to change shape in the schema cutover (the cutover changes
  how the *types are emitted*, not the wire vocabulary —
  `persona/INTENT.md:230-232`).
- **The supervisor / launcher shape is proven on real binaries**
  (`flake.nix:1815`), and asschema-removal is complete, so the
  spawn-envelope + readiness path won't be reworked by the schema engine.
- **The plane separation holds:** Signal wire lives in the contract
  repos (`owner-signal-persona`, `signal-engine-management`), the
  daemon-local concerns live in `persona`/`mind`/`orchestrate` — matching
  lc2r. Building W1–W4 respects this and won't be re-laid by the runner
  extraction (W5), which subsumes the transport *plumbing* while keeping
  the same wire types.

What is NOT stable and must be waited on: the schema→runner / schema→types
**emission pipeline** (blocks W5, W7) and the multi-engine state-mutation
semantics (gates the finalization of W4).

## 4 · THE ONE highest-leverage first thing in this area

**W1 — turn the already-green
`persona-daemon-launches-nix-built-prototype-topology` flake check into a
standing full-stack runner that also ticks health and asserts
crash-restart.** It is [SAFE-NOW], depends on nothing, and it is the
shortest distance from where the code actually is to the mazv target:
the eight-real-daemon launch+readiness loop is *already proven*, so the
only thing standing between "persona launches real components" and
"persona *runs and supervises* a living orchestrated system" is the
health/restart loop on top of the exact path CI already exercises. It
converts the strongest existing asset into the target state with no
rework risk, and it gives every later item (W2–W7) a living end-to-end
harness to land against.
