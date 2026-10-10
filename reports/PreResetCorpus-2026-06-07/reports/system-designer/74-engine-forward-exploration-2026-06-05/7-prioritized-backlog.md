# Engine-Forward Prioritized Backlog

Synthesis of the six area maps (cloud, persona/supervisor, introspect,
schema-daemon, triad-runner, deploy/pilot) into one ranked
where-to-put-effort backlog for the orchestrated-system target.

Target state (Spirit Decision, described first): a LIVE orchestrated
system — persona is the manager/supervisor of the whole thing and runs
+ supervises the introspector, the schema daemon, and the other triad
components together, not merely proven in-tree.

This synthesizer re-verified every load-bearing citation against source
on 2026-06-05. Two facts shifted FAVOURABLY since the area maps were
written, and both change the backlog:

- The triad-runner map's WI-1 ("commit the uncommitted role.rs
  extraction") is **DONE**. `triad-runtime` working copy is clean;
  `role.rs` is committed (parent commit `triad-runtime: add triad role
  traits`). The crate's 6 listed modules are now 7 on disk
  (`argument frame daemon runner role trace lib`).
- The schema-daemon map's headline blocker ("schema-rust-next working
  tree does NOT compile — broken `emit_runtime_role_trait_impls` WIP")
  is **RESOLVED**. The working tree now builds clean and `cargo test`
  is 6/6 green. The emitter is wired (call `src/lib.rs:277`, def
  `src/lib.rs:2839`). The area's own repo is no longer red.

Net effect: the two "fix your own red tree first" items at the front of
the schema/runner maps are already cleared, so the critical path now
starts at the next primitive, not at a cleanup.

## A. The critical path — the dependency spine

The hypothesis to test was: "the triad runner (7ca4) unblocks every
daemon, so it is likely first; cloud is the psyche's emphasis and may
be the first real consumer." The maps **partially confirm and sharply
refine** this.

Refinement 1 — the runner is NOT greenfield-first; it is
already-extracted-and-proven for one of two halves. `triad-runtime`
v0.2.x is a real landed crate (frame codec, single-arg classifier,
single-listener daemon shell + accept loop, the recursive 5-outcome
Nexus `Runner` + typed continuation budget, plane-role marker traits,
trace). Its `RunnerEngines` trait is exactly intent rpr5 (3 plane
engines + effect handler + budget reply). And the **hardest** rpr5
claim — "the runner adapter is generated glue, authors write hooks" —
is LANDED for the Nexus plane: `spirit/src/schema/nexus.rs:821-832`
emits `NexusRunnerAdapter` (`impl triad_runtime::RunnerEngines`) and
`NexusEngine::execute` drives `triad_runtime::Runner::new(...)` at
`nexus.rs:812`. So 7ca4/rpr5 is not "to be built first"; it is
"finish the Signal half of an already-running mechanism."

Refinement 2 — the one remaining piece of per-daemon boilerplate is the
**Signal-plane accept bridge**, not the Nexus loop. Verified in spirit:
`src/daemon.rs:139-143` hand-writes `transport.read_input()` →
`self.engine.handle(input)` → `transport.write_output(...)`. Every
future daemon copies exactly this. Generating it (mirroring how
`NexusEngine::execute` is already generated) is the single move that
converts the second daemon from "copy spirit's daemon+transport+engine"
into "declare 3 schemas + write hooks."

The actual dependency order from the maps:

1. **Signal-plane accept-bridge generation** (schema-rust-next emits it;
   spirit is the proving consumer). This is the last hand-written
   boilerplate on the runner spine. Everything that wants
   "declare-schemas-not-write-a-daemon" sits behind it. — the true
   first runner-spine move now that role.rs + Nexus adapter + green tree
   are landed.
2. **Two-listener daemon runner in triad-runtime** (only
   `SingleListenerDaemon` exists). Cloud's owner+ordinary split, and
   any triad with both a Signal and meta-Signal socket, blocks on this.
   It is additive on stable socket machinery.
3. **Per-area first-real-consumer ports**, each gated only on the wire
   contract it consumes (all frozen): cloud effects/SEMA substance;
   persona standing-runner + orchestrate supervision; introspect
   contract realign + witness test; lojix reconcile + shell adoption.
4. **`TriadComponent::serve` umbrella** (compose daemon + transport +
   Nexus loop behind one generated `serve`) — deliberately AFTER a
   second daemon exercises the bridge, so the signature is frozen
   against two consumers not one.
5. **Persona real Launch/Retire + standing supervised topology** — the
   convergence point where "persona launches real binaries" (already a
   green Nix check, `persona/flake.nix:1815`) becomes "persona runs and
   supervises a living, self-healing system" (the target).

On the psyche's cloud emphasis: cloud is the most-advanced TWO-contract
port and the only area where the generic runner already drives two
contracts end-to-end in test. But cloud's daemon still serves the
legacy hand-written `Store` (`cloud/src/daemon.rs:12,24`), and the
fresh `SchemaRuntime` serves no socket and stubs plan ops
(`schema_runtime.rs:186-195` return `RequestRejected`). So cloud is the
first real **two-contract** consumer, gated on the two-listener runner
(item 2). It is NOT the very first spine move; the Signal accept bridge
(item 1) is upstream of cloud's eventual daemon flip.

Critical-path one-liner: **finish the Signal half of the runner (accept
bridge, then two-listener shell) → stand up the first real two-contract
consumer (cloud) and the first supervised observer (introspect) on
it → converge on persona standing-supervision with real Launch/Retire.**

## B. Ranked work items (leverage × foundation-readiness)

Ranked across all areas. Size: S ≈ hours, M ≈ a day or two, L ≈
multi-day. Verdict: SAFE-NOW (foundation-stable, won't be rework) /
PREP (scaffold, don't freeze) / WAIT (defer, named blocker).

| # | Item | Area / repo | Verdict | Depends on | Size |
|---|---|---|---|---|---|
| 1 | Generate the Signal-plane accept bridge as glue, mirroring the already-generated `NexusEngine::execute` | schema-rust-next (emit) + spirit (consume) | PREP | wire frame + Nexus entry stable; only the author-hook split line is open | M |
| 2 | Add two-listener daemon runner to triad-runtime (only `SingleListenerDaemon` exists) | triad-runtime | SAFE-NOW | stable socket machinery + frozen contracts; additive | M |
| 3 | Realign persona onto renamed `signal-introspect` contract + binary name (close the revision drift) | persona (+ introspect) | SAFE-NOW | rename complete in contract+daemon; deletes drift | S |
| 4 | End-to-end orchestrated witness test: persona spawns real introspect + router; introspect queries live router `Summary` | introspect / persona | SAFE-NOW | item 3; both wire ends stable+aligned | M |
| 5 | Turn the green `persona-daemon-launches-nix-built-prototype-topology` check into a standing runner with health-tick + crash-restart assertion | persona | SAFE-NOW | nothing; builds on strongest existing asset | M |
| 6 | Teach orchestrate to answer engine-management supervision (port mind's supervision handler into `orchestrate/src/supervision.rs`) | orchestrate | SAFE-NOW | contract frozen; mind handler is the template | M |
| 7 | Reconcile lojix to signal-frame; adopt triad-runtime `SingleListenerDaemon`, delete lojix `socket.rs` accept loop (keep Kameo tree behind it) | lojix | SAFE-NOW | contract migration settled; spirit proves the shell | M |
| 8 | Lift `SignalTransport` into triad-runtime as a generic transport object | triad-runtime | SAFE-NOW (object) / PREP (frame trait) | item 1 frame trait shape | M |
| 9 | Self-host the macro table from `core.schema` (close the bootstrap loop) | schema-rust-next | SAFE-NOW | inputs landed | M |
| 10 | Emit the daemon-binary glue (`SingleListenerDaemon`/`ComponentCommand`/`DaemonRuntime`) so daemons stop copying spirit's daemon.rs | schema-rust-next | PREP | single-listener stable; multi-listener deferred | M |
| 11 | Add orchestrate (then spirit) to a supervised multi-component topology end-to-end | persona | PREP | item 6 | M |
| 12 | Port real Cloudflare effects into `SchemaRuntime::run_effect` | cloud | PREP | effect schema stable; finish Nexus decide-loop `EffectCompleted`→continuation | M |
| 13 | Implement cloud SEMA plan/projection substance (replace `RequestRejected` stubs) | cloud | PREP | items 1+12 parity | M |
| 14 | Wire introspect `ManagerClient` to a real readiness query | introspect | PREP | shape knowable; finalize after Layer-1 | M |
| 15 | Define `TriadComponent::serve` umbrella (daemon + transport + Nexus loop behind one generated serve) | triad-runtime + schema-rust-next | PREP | items 1+8; freeze only after a 2nd daemon exercises it | M |
| 16 | Implement real Launch/Retire in persona manager (`manager.rs:181-198` reject stubs) | persona | PREP | owner contract frozen; multi-engine state semantics still evolving | L |
| 17 | Re-express lojix Kameo tree as one `RunnerEngines` impl | lojix | PREP | trait landed; lojix is first multi-job sub-actor author | L |
| 18 | Bootstrap policy authored as NOTA, consumed as pre-encoded rkyv at first start (7x50) | triad-runtime / schema-rust-next | WAIT | meta-signal / meta-policy plane shape unsettled | M |
| 19 | Flip cloud daemon to serve `SchemaRuntime` via the runner; retire `Store` | cloud | WAIT | items 12+13 parity (flipping now regresses live Cloudflare path) | M |
| 20 | Durable cloud SEMA persistence (redb) | cloud | WAIT | shared sema-engine still pulls deprecated `signal-core` (ARCHITECTURE.md:67-69) | M |
| 21 | Introspect Layer-1 verb migration (bare `Observe` + observable `Tap`/`Untap`) | introspect / contracts | WAIT | signal-frame macro shape | M-L |
| 22 | Introspect push subscriptions | introspect | WAIT | observable macro AND sema-engine per-peer commit-then-emit (ARCHITECTURE.md:157-165) | L |
| 23 | Author lojix plane schemas via schema-rust-next | lojix | WAIT | operator `primary-vllc` (dual-lowering bare-header bug under payload-less deploy-phase enums) | L |
| 24 | Extract generic runner from persona's hand-written transport (W5) | persona | WAIT | schema→runner emission pipeline (= items 1+10+15); hand-writing now is the exact boilerplate it deletes | L |
| 25 | Replace `*.concept.schema` v0.1 placeholders with schema-engine sources | persona / introspect | WAIT | psyche-sequenced after the Spirit pilot generalizes | M |
| 26 | spirit hash-identity + relations record redesign | spirit | WAIT | psyche-gated (flat-vs-per-kind unresolved) + `primary-vllc` | L |

## C. The "start porting now" set (SAFE-NOW)

Conservative. Each item below is foundation-stable AND high-leverage AND
justified as zero-rework. The justification for each cites what is
stable — never "it seems ready."

- **Item 2 — two-listener daemon runner in triad-runtime.** Stable
  ground: `triad-runtime`'s socket/accept machinery is landed and
  proven by spirit's 7 process-boundary tests; both cloud wire
  contracts (signal-cloud Observe+Validate; meta-signal-cloud the 8
  owner mutations) are frozen. This is purely additive — a second
  listener alongside `SingleListenerDaemon`, not a rewrite of it. It
  is the named generator/runtime blocker for every two-contract triad
  and unblocks cloud's eventual flip. No moving foundation touched.

- **Item 3 — realign persona onto renamed `signal-introspect`.**
  Stable ground: the rename is COMPLETE in both the contract repo and
  the introspect daemon (verified: persona Cargo.toml:35 still pins the
  old `signal-persona-introspect`; introspect Cargo.toml:35 pins the new
  `signal-introspect`). Closing this deletes a real drift; it cannot
  create rework because it moves a pin onto the already-canonical
  contract. S-sized.

- **Item 4 — orchestrated introspect witness test.** Stable ground:
  introspect's `RouterClient` sends a real `RouterRequest::Summary` over
  a length-prefixed frame, and `router/src/observation.rs:38` answers it
  live; persona already registers and prototype-supervises introspect.
  The test consumes only stable wire contracts + the implemented
  handshake and asserts decoded typed replies (not verb spelling), so
  it survives the owed Layer-1 bare-verb migration. Converts the area
  from proven-in-tree to demonstrably-live. Gated only on item 3.

- **Item 5 — persona standing full-stack runner (health-tick +
  crash-restart).** Stable ground: the load-bearing proof already
  exists and is green — `persona/flake.nix:1815`
  `persona-daemon-launches-nix-built-prototype-topology` launches the
  REAL persona-daemon launching REAL Nix-built daemons for all 8
  prototype-supervised components, each confirmed ready over the
  engine-management socket. Spawn-envelope/launcher foundation is
  stable and asschema-free. Extending a green check into a standing
  health+restart loop depends on nothing and builds on the strongest
  asset in the stack. This is the shortest path from "persona launches
  real components" to "persona supervises a living system."

- **Item 6 — orchestrate answers engine-management supervision.**
  Stable ground: the `signal-engine-management` contract (Announce /
  Ready / Health / Stop + typed SpawnEnvelope) is landed and closed;
  `mind/src/supervision.rs:157-176` is a working answer-handler that
  ports directly. Verified that orchestrate today has ZERO
  engine-management supervision (its `Ready` hits are its own
  upgrade/handover state machine, `service.rs:228`/`handover.rs:30`,
  and it has no engine-management dep). This is the gating gap between
  "orchestrate is a real daemon" and "orchestrate can join the
  supervised loop." Copy-the-template work.

- **Item 7 — reconcile lojix to signal-frame + adopt the daemon
  shell.** Stable ground: the signal-frame contract migration is
  already settled (`signal-lojix` migrated; lojix is the lagging
  consumer, likely not even compiling against its own contract because
  it still pins `signal-core`); spirit proves the exact
  `SingleListenerDaemon` shell end-to-end. Keep lojix's Kameo tree
  behind the new shell, so nothing functional is bet on
  not-yet-frozen surfaces. Zero-rework; unblocks all later lojix work;
  touches none of the gated surfaces (`primary-vllc`, hash-identity).

- **Item 9 — self-host the macro table from `core.schema`.** Stable
  ground: schema-rust-next builds + tests green (verified 6/6), and the
  bootstrap inputs are landed. Closing the bootstrap loop is internal
  to the already-green schema engine. M-sized.

Deliberately EXCLUDED from start-now (would be porting onto sand):

- The Signal accept-bridge generation (item 1) is PREP not SAFE-NOW:
  the wire frame and Nexus entry are rock, but the exact
  author-hook/glue split line is the one open design decision; scaffold
  it, don't freeze the generated shape until spirit + a second daemon
  both consume it.
- Cloud effects/SEMA substance (items 12, 13) are PREP: the schemas are
  stable but the Nexus decide-loop's `EffectCompleted`→continuation
  finish is in-flight.
- Anything gated on the sema-engine emit path, the signal-frame macro,
  `primary-vllc`, or hash-identity is WAIT (section D).

## D. The PREP / WAIT set

PREP — scaffold against the landed trait/contract, but DO NOT freeze
signatures or finalize, because one input is still moving:

- **Item 1 — Signal accept-bridge generation.** Scaffold the emitter
  and the spirit consumer; the open piece is the author-hook split
  line. Freeze only once spirit consumes it AND a second daemon
  exercises it.
- **Item 8 — `SignalTransport` into triad-runtime.** The transport
  OBJECT is liftable now; the generic FRAME TRAIT shape is PREP, tied to
  item 1.
- **Item 10 — daemon-binary glue emission.** Single-listener glue is
  stable to emit; the multi-listener variant waits on item 2 landing
  and on triad-runtime un-deferring multi-listener concurrency.
- **Item 11 — orchestrate (then spirit) into a supervised topology.**
  Topology + launchers exist; finalize after item 6.
- **Item 12 / 13 — cloud effects and SEMA substance.** Effect schema
  and cloudflare.rs are reusable; finish the Nexus decide-loop
  `EffectCompleted` handling first, then the SEMA plan/projection
  bodies (currently `RequestRejected` stubs, `schema_runtime.rs:186-195`).
- **Item 14 — introspect `ManagerClient` readiness query.** Shape is
  knowable; finalize after Layer-1 verb migration so it isn't rewritten.
- **Item 15 — `TriadComponent::serve` umbrella.** Composes items 1+8;
  explicitly do not freeze the signature until a second daemon exercises
  the bridge — one consumer is not enough to freeze a generic.
- **Item 16 — persona real Launch/Retire.** Owner contract is frozen,
  but multi-engine state semantics are still evolving; scaffold the
  manager path, gate the cutover.
- **Item 17 — lojix Kameo tree → one `RunnerEngines` impl.** Trait is
  landed; lojix is the first multi-job sub-actor author, so keep the
  Kameo tree until tests are green, then cut over.

WAIT — defer; do not start until the named blocker clears:

- **Item 18 / 7x50 bootstrap policy.** Blocker: the meta-signal /
  meta-policy plane shape is unsettled. The binary-config transport
  exists, but the policy schema is shifting.
- **Item 19 — flip cloud daemon to `SchemaRuntime`, retire `Store`.**
  Blocker: items 12+13 parity. Flipping now regresses the live
  Cloudflare path (the legacy `Store` is the only thing serving real
  Cloudflare via flarectl, `cloud/lib.rs:448-1288`).
- **Item 20 — durable cloud SEMA persistence (redb).** Named blocker:
  the shared sema-engine still pulls deprecated `signal-core`
  (`cloud/ARCHITECTURE.md:67-69`).
- **Item 21 — introspect Layer-1 verb migration.** Blocker:
  signal-frame macro shape (both introspect wire contracts still carry
  `Match` Sema-verb tags in `signal_channel!`).
- **Item 22 — introspect push subscriptions.** Blocker: observable
  macro AND sema-engine per-peer commit-then-emit
  (`introspect/ARCHITECTURE.md:157-165`).
- **Item 23 — author lojix plane schemas.** Blocker: operator
  `primary-vllc` (dual-lowering bare-header bug under payload-less
  deploy-phase enums).
- **Item 24 — extract the runner from persona's hand-written
  transport.** Blocker: the schema→runner emission pipeline (items
  1+10+15). Hand-writing it now produces the exact boilerplate the
  pipeline deletes — this is the trap the foundation caveat warns
  against.
- **Item 25 — replace `*.concept.schema` v0.1 placeholders.** Blocker:
  psyche-sequenced after the Spirit pilot's schema-derive generalizes.
- **Item 26 — spirit hash-identity + relations redesign.** Blocker:
  psyche-gated (flat-vs-per-kind unresolved) + `primary-vllc`. Pilot
  record identity is currently NUMERIC (no hash, no relations field).

## E. Proposed first execution

**Do item 2 first: add the two-listener daemon runner to
triad-runtime.**

Rationale. After re-verification, the two "fix your own red tree"
front-runners from the source maps are already cleared (triad-runtime
role.rs committed; schema-rust-next green). Among the genuinely
SAFE-NOW set, item 2 is the highest-leverage zero-rework move: it is
the single missing runtime primitive between "the runner drives two
contracts in a unit test" (already true in cloud) and "the runner can
be a daemon's serving loop for BOTH a Signal and a meta-Signal socket."
It is the named generator/runtime blocker. It is purely additive on
landed, test-proven socket machinery and frozen wire contracts, so it
cannot be rework. And it is the thing that unblocks the
psyche-emphasized area (cloud's eventual daemon flip needs
owner+ordinary listeners) without touching any shifting surface
(no sema-engine emit, no signal-frame macro, no `primary-vllc`, no
hash-identity).

It is sequenced ahead of the Signal accept-bridge generation (item 1)
on purpose: item 1 is PREP (its author-hook split line is the one open
design decision), whereas item 2 is SAFE-NOW. Land the stable primitive
first; the bridge generation then has two concrete socket modes
(single + dual) to generate against, which is exactly what keeps its
signature from being frozen prematurely against one consumer.

Steps:

1. In `triad-runtime`, add a `TwoListenerDaemon` (or extend the daemon
   module) alongside the existing `SingleListenerDaemon`: accept on two
   Unix sockets (ordinary + owner / Signal + meta-Signal), each routing
   into the same `Engine::handle` admission path the single-listener
   shell already uses. Reuse the existing accept loop and frame codec —
   do not fork them.
2. Keep the engine-facing contract identical to `SingleListenerDaemon`
   so spirit (single) and cloud (dual) share one `RunnerEngines`-driven
   handle path; the only difference is socket count.
3. Add a triad-runtime integration test that spawns the dual-listener
   shell over two temp Unix sockets and round-trips one frame on each,
   mirroring spirit's existing process-boundary test style.
4. Update `triad-runtime/ARCHITECTURE.md` Code Map to list the
   `role.rs` module (currently missing — the latest extraction is
   committed but not yet documented) and the new two-listener shell.
5. Commit on the triad-runtime `next`/feature branch under
   `~/wt` per the code-repo branch discipline (designers ship `next`,
   operators own main). Inline `jj` description only.
6. Hand-off note for the next session: with the dual-listener shell
   landed, the immediate follow-ons are item 1 (generate the Signal
   accept bridge against both socket modes) and item 12/13 (cloud
   effects + SEMA substance) so cloud can become the first real
   two-contract consumer running on the generic runner.

Scope guard: this first execution touches ONLY triad-runtime's
additive daemon shell + its own test + ARCHITECTURE.md. It does not
flip cloud's daemon (that is WAIT item 19), does not generate the
accept bridge (PREP item 1), and does not touch any gated surface.
