# Logix (lojix) triad-port — the big questions

*cloud-designer subagent (B2), 2026-06-04. Read-only audit. Logix is
the component the psyche named as the traditional component that
receives the full triad-engine + schema-based-component port (Spirit
`1bok2bxvu3beswif9mv`), while Horizon stays the simple projection
surface. This report maps the lojix surface onto the now-settled
per-plane triad shape proven by the cloud component, and surfaces the
six big questions each with a recommended answer + evidence.*

## What grounds this report — three sources, one corrected target

Three bodies of evidence converge here, and they do not agree, which
is the most important finding:

1. **The settled per-plane triad shape** — the cloud component as the
   worked template (`signal-cloud/schema/lib.schema`,
   `meta-signal-cloud/schema/lib.schema`, `cloud/schema/nexus.schema`,
   `cloud/schema/sema.schema`), the corrected three-schema layout
   (Spirit `2bgatqufm9m0dktxkv5`, `1up1ufia24c2opn3mqn`), and the
   generic runner in `triad-runtime`.
2. **The stale signal-lojix contract spec** — `signal-lojix/ARCHITECTURE.md`
   documents an OLD-stack three-LAYER migration (Layer 1 contract verbs /
   Layer 2 component commands / Layer 3 sema classification) built on
   `signal-frame` + `signal_channel!`, NOT the schema-derived per-plane
   triad.
3. **An existing logix triad PROTOTYPE already on disk** —
   `~/wt/github.com/LiGoldragon/lojix/schema-deep-iteration-2/` carries a
   working all-in-one `schema/lojix.schema`, a Kameo 9-actor topology, a
   `NexusMailKeeper`, redb `Store`, GC-root pinner, builder/copier/activator
   actors, and tests including `sandbox_build_pipeline.rs`,
   `sandbox_activation.rs`, `actor_topology.rs`, `nexus_mail_keeper.rs`,
   `sema_engine_durable.rs`. This is the `6wzz3up583b428kh3ok` schema-deep
   rewrite, already started — and it predates the per-plane correction.

The port is therefore not greenfield. It is a **reconciliation**: take
the prototype's domain logic (which is sound — it knows the deploy
pipeline), retarget it from the all-in-one + Kameo-actor-per-concern
shape onto the per-plane schema + generated-engine + `CommandEffect`
runner shape that cloud just proved.

## What the daemon must cover (legacy surface, from lojix-cli)

The daemon replaces the legacy monolith `lojix-cli`. Its operations,
from `lojix-cli/src/request.rs:48-53` and the deploy pipeline in
`deploy.rs` / `build.rs` / `activate.rs`:

- **Deploy variants**: `FullOs`, `OsOnly` (system deploys, home on/off),
  `HomeOnly` (home-profile deploy) — `request.rs:13-53`. Each carries
  cluster, node, source (proposal), flake ref, a `SystemAction`
  (`Eval`/`Build`/`Boot`/`Switch`/`Test`/`BootOnce` — `build.rs:9-23`)
  or `HomeMode`, an optional builder node, optional extra substituters.
- **The deploy pipeline** (`deploy.rs:89-148`): load proposal → project
  horizon (via `horizon-rs`) → validate home user → resolve builder/
  substituters → materialize override flake inputs → `nix build`/`nix eval`
  → `nix copy` closure → activate (`nixos-rebuild`/`systemd-run` switch/
  boot/test) — for system or home.
- **Diagnostics**: `CheckHostKeyMaterial` (read-only host-vs-cluster key
  diff — `check.rs`).
- **Scope expansion (intent `1orezxnzgedct1grkn4`)**: lojix-daemon owns
  GitHub-authenticated Nix flake-input resolution — an authenticated
  wrapper that injects the GitHub API token into the Nix call
  (`NIX_CONFIG` access-tokens) to dodge rate-limit stale-activation
  incidents. This is a deploy-path effect, not a Pi-package problem.

The replacement adds what lojix-cli never had (its ARCH §1): a live
generation set, GC-roots tree, append-only deploy event log, container-
lifecycle observation, and push subscriptions — i.e. the durable state
and observation surface that turns a one-shot CLI into a daemon.

## Q1 — Working vs policy contract split (signal-lojix vs meta-signal-lojix)

**Recommended answer: TWO contracts. Deploy / Pin / Unpin / Retire are
OWNER-ONLY and live in `meta-signal-lojix`. Query and the two Watch
subscriptions are peer-callable and live in `signal-lojix`. Unwatch
follows whichever stream it closes (so it appears on the ordinary
contract for the ordinary streams).**

The split rule is who-can-call, not what-state-it-touches
(`component-triad.md` §"Two authority tiers"). The cloud port is the
precedent: the read surface (`Observe`, `Validate`) is the ordinary
`signal-cloud`; every mutation (`RegisterAccount`, `PreparePlan`,
`ApprovePlan`, `ApplyPlan`, `SetPolicy`, …) is the owner-only
`meta-signal-cloud`. Lojix maps cleanly:

| lojix operation | Authority | Contract | Cloud analogue |
|---|---|---|---|
| `Deploy` (submit) | owner-only | `meta-signal-lojix` | `ApplyPlan` |
| `Pin` / `Unpin` | owner-only | `meta-signal-lojix` | `SetPolicy` |
| `Retire` | owner-only | `meta-signal-lojix` | `RetireAccount` |
| `Query` (live set) | peer-callable | `signal-lojix` | `Observe` |
| `WatchDeployments` | peer-callable | `signal-lojix` | (subscribe) |
| `WatchCacheRetention` | peer-callable | `signal-lojix` | (subscribe) |
| `Unwatch` | peer-callable | `signal-lojix` | (subscribe-close) |

**Is deploy submission owner-only policy? YES.** A deploy mutates the
live cluster — it activates a NixOS generation on a node, rewrites GC
roots, and can break networking on the router node (intent
`5hir5bnz9af64zjg53d`, `5er7r9fj9whba2ewgit` — Prometheus is the cluster
router; deploys there must use BootOnce until sign-off). This is the
strongest possible case for the owner socket: the
security-edit-visibility property (`component-triad.md` §"Why the
contract is a separate repo", point 2) means a change to who-may-deploy
lands in `meta-signal-lojix` and nowhere else. Pin/Unpin/Retire mutate
the GC-roots policy that protects/evicts closures — equally owner-only.

This directly **contradicts the stale `signal-lojix/ARCHITECTURE.md`**,
which puts `Deploy`, `Pin`, `Unpin`, `Retire` all in the single
`signal-lojix` contract (its §"MUST IMPLEMENT" Layer-1 table,
lines 41-49 and the operation table lines 107-114). That spec predates
the two-authority-tier rule's hardening and the meta-signal rename; it
has no `meta-signal-lojix` at all. The prototype's `lojix.schema` makes
the same omission — one `Input [Submit Cancel Query Help]` root on one
socket, no policy surface (`lojix.schema:2-7`). Both need the split.

One subtlety from the cloud reflected-external-state generalization
(`signal-cloud/ARCHITECTURE.md` §"Ordinary vs owner split"): a component
whose state is a reflected external resource exposes reads on the
ordinary contract and mutations on the meta contract. Lojix's live set
IS a reflection of what is actually activated on cluster nodes — so
`Query` (read) on ordinary, `Deploy`/`Pin`/`Retire` (mutate) on meta is
the same generalization applied a second time. Cloud is the first worked
example; lojix is the second, which strengthens the rule.

## Q2 — Nexus CommandEffects for the deploy pipeline + systemd observation

**Recommended answer: the deploy pipeline is a chain of explicit Nexus
`CommandEffect` variants, threaded by `Continue`; systemd/dbus container
observation is a long-lived effect/subscription that asserts into the
event log. Nothing in the pipeline runs inline in a handler.**

The single most important shape decision in the cloud port was making
the Cloudflare DNS call a Nexus `CommandEffect` rather than inline IO
(cloud report 18 §5.1, cloud `nexus.schema:40-46`:
`EffectCommand [CloudflareObserveZones CloudflareObserveRecords
CloudflareApplyPlan]`). The same shape applies to lojix's external Nix
work. The effect vocabulary, derived from the legacy pipeline:

| Effect | Legacy source | What it does |
|---|---|---|
| `NixEval` | `build.rs:291-297` `nix eval --raw .drvPath` | resolve derivation path (Eval action) |
| `NixBuild` | `build.rs:298-305` `nix build --print-out-paths` | realize the closure (local or via ssh builder) |
| `CopyClosure` | `copy.rs`, `deploy.rs:166-172` `nix copy` | copy closure to target / from builder |
| `ActivateGeneration` | `activate.rs:135` `systemd-run … nixos switch/boot/test` | activate on target over ssh |
| `PathInfoGc` | ARCH §1 `nix path-info -r` + two-phase delete | closure introspection + GC respecting narinfo TTL |
| `ResolveFlakeAuth` | intent `1orezxnzgedct1grkn4` | GitHub-token-injected flake input resolution |

The Nexus `decide` body for `Deploy` orchestrates these as a sequence of
`CommandEffect` actions, each effect's completion re-entering Nexus as
the next `NexusWork` (the runner's `EffectCompleted` → next step,
`triad-runtime/src/runner.rs` §"RunEffect → re-enter with effect
completion"). Between effects, Nexus emits a `DeploymentPhaseEvent`
(Submitted/Building/Built/Copying/Activating/Activated/Failed) and
`CommandSemaWrite`s the event into the append-only log. This is exactly
the cloud `ApplyPlan` trace (read→effect→write→reply via `Continue`,
cloud report 18 §4.1) generalized to a multi-effect pipeline.

**What stays inline (in Nexus's own decide body, not as effects):**
horizon projection and validation. Per intent `7ggswqdxqqz97za6o7w`
Horizon emits simple typed facts; the projection from a goldragon
proposal to the per-node horizon view is a pure transform (horizon-rs is
a projection library, a named triad carve-out — `component-triad.md`
§"Named carve-outs" point 1). It has no external IO, so it is Nexus
decision logic, not an effect. Builder/substituter resolution
(`deploy.rs:49-65`, `210-224`) is likewise pure lookup over the
projected horizon — inline.

**systemd/dbus container observation:** this is NOT a request/reply
effect — it is a continuous source. The right shape is a long-lived
effect started at daemon boot (or on first `WatchDeployments`) that
subscribes to `systemd` dbus for `containers.<name>.service`
transitions (lojix ARCH §1 line 63-65) and **asserts** each transition
(`ContainerStarted`/`ContainerStopped`) into the event log via
`CommandSemaWrite`. The subscription bridge from SEMA deltas to the wire
`CacheRetentionTransitionEvent` / `DeploymentPhaseEvent` is the
push-not-poll surface. The legacy code has no container observation
(grep shows only `systemd-run` for activation, `activate.rs:135`) — this
is genuinely new daemon surface, so it should be modeled as the
canonical long-lived-effect pattern rather than retrofitted.

**Effects per-component declared in schema** (Spirit `1486`): these
effect variants live in `lojix/schema/nexus.schema`'s `Effect` enum,
exactly as cloud declares `EffectCommand`. `Stash` is the first universal
candidate (slim Nexus output via handle) but lojix's BuildLog and
HorizonView are large text payloads that are strong second candidates
for stash-by-handle rather than inline-in-mail.

## Q3 — SEMA storage planes (live-set / GC-roots / event-log / container)

**Recommended answer: four table families in one `lojix.redb`, declared
in `lojix/schema/sema.schema`. The live set and GC roots are policy-ish
working state with single-writer Mutate; the event log and
container-lifecycle records are append-only Assert.**

Mapping the lojix ARCH §1 owned surface onto the cloud `sema.schema`
table-declaration pattern (`cloud/schema/sema.schema:64-67`:
`AccountPolicyTable { bindings (Vec AccountBinding) }`,
`PlanTable { plans (Vec StoredPlan) }`):

| SEMA table | Key/shape | Sema class | lojix ARCH source |
|---|---|---|---|
| `LiveSetTable` | `BTreeMap<(ClusterName,NodeName,Kind),Generation>` | Mutate (Deploy/Pin/Retire) | §1 "Live generation set" |
| `GcRootsTable` | per-kind slots: current / boot-pending / rollback[N] / pinned[label] / recent[ts] | Mutate | §1 "GC roots tree" |
| `EventLogTable` | append-only typed events | Assert | §1 "Deploy event log" |
| `ContainerLifecycleTable` | systemd-mirrored container records | Assert | §1 "Container lifecycle observation" |

The `SemaWriteInput` / `SemaReadInput` split (cloud `sema.schema:34-56`):
writes are `Deploy`/`Pin`/`Unpin`/`Retire`/`AppendEvent`/`RecordContainer`;
reads are `Query` (live set, whole or filtered) plus event-log/
generation reads. Per `component-triad.md` §"Interface roots are enums
with more than one variant" (Spirit `1401`), each root must have ≥2
meaningful variants — the read root should carry `Query` + `Lookup` (one
generation by id) + `History` (event-log range) so it is a real interface,
not a single-op newtype.

The prototype already proves the durable SEMA half:
`schema-deep-iteration-2/tests/sema_engine_durable.rs` +
`src/runtime/store.rs` carry a redb-backed generation ledger with a
`DatabaseMarker [TransactionCounter StateHash]` (`lojix.schema:36`). That
marker is exactly the cloud `StateMarker { CommitSequence StateDigest }`
(`cloud/schema/sema.schema:60`) and threads on the SEMA reply per the
Nexus protocol — keep it. What the prototype lacks vs the ARCH: GC-roots
slot management and the two-phase narinfo-TTL deletion. Those land as the
`GcRootsTable` write ops + the `PathInfoGc` effect.

**Reuse-not-repeat (intent `10v4744869xt5spwnam`)** applies inside SEMA
too: a `GenerationRecord` read out of `LiveSetTable` is the same type
written in. Do not mint a parallel `GenerationOutput`. The cloud schema
already follows this (the `Plan` type is both the prepared-plan write
payload and the `PlanResult` read payload — `signal-cloud/schema/lib.schema:41,50`).

## Q4 — schema-next → schema-rust-next per-plane generation + resolver lessons

**Recommended answer: follow the cloud `build.rs` pattern exactly — two
wire contracts publish their schema dirs via `CargoSchemaMetadata`; the
daemon's `build.rs` reads them as `DependencySchema` and generates
`nexus.schema` (NexusRuntime) + `sema.schema` (SemaRuntime) per plane.
Reconcile type names BEFORE wiring the build, because that is the
deepest blocker the cloud port hit.**

The generation path, lifted verbatim from the cloud template:

- `signal-lojix/build.rs` and `meta-signal-lojix/build.rs` use
  `GenerationPlan::wire_contract(...)` and call
  `CargoSchemaMetadata::new("signal-lojix").emit_schema_directory(...)`
  (cloud `signal-cloud/build.rs`, `meta-signal-cloud/build.rs` verbatim).
  A wire-only schema emits NO engine traits — only rkyv/NOTA codec +
  mail envelopes (cloud report 20 §"The macro reality").
- `lojix/build.rs` uses `GenerationPlan::daemon_runtime(...)`
  `.with_dependency_schema(ordinary).with_dependency_schema(meta)`,
  reading both via `DependencySchema::from_cargo_metadata` keyed on the
  `DEP_<LINKS>_SCHEMA_DIR` Cargo seam (cloud `cloud/build.rs`'s
  `ContractSchemaDependencies`, verbatim). `nexus.schema` →
  `RustEmissionTarget::NexusRuntime`, `sema.schema` →
  `RustEmissionTarget::SemaRuntime` (schema-rust-next ARCH lines 75-96).
- The daemon's `nexus.schema` imports the contract wire roots with the
  single-colon path form: `OrdinaryInput signal-lojix:lib:Input`,
  `MetaInput meta-signal-lojix:lib:Input`, plus its own
  `cloud:sema:*`-style local SEMA roots (cloud `nexus.schema:8-21`).
  Cross-crate imports emit as `pub use … as` aliases preserving type
  identity (schema-rust-next ARCH lines 122-128).

**The resolver / type-name lessons (cloud reports 22 + cloud-operator
15) — apply these or the build fails the same way:**

1. **Type-name content drift is the deepest blocker (report 22 item 1).**
   The cloud daemon `sema.schema` imported `PlanQuery`, `Validated`,
   `Observed`, `PlanResult` while the contract's `lib.schema` defined
   `ObservationResult`, `ValidationReport`, `Plan` — so even with the
   resolver fixed and files present, resolution hit `ImportedTypeNotFound`.
   **Lesson for lojix: author the contract schemas FIRST, then write the
   daemon plane schemas importing EXACTLY the names the contracts export.**
   The contracts are the source of truth for wire type names.
2. **Canonical-vs-next split (report 22 item 2).** Cloud's daemon plane
   schemas referenced contract modules that existed only on `next`
   worktrees, not the canonical `/git` checkouts (which carried only
   `*.concept.schema`). **Lesson: decide whether lojix generation
   consumes canonical or `next` contract schemas, and make the module
   files present at that surface before generation.** lojix-cli's
   `schema/lojix-cli.concept.schema` and signal-lojix having no schema at
   all is the same trap waiting.
3. **The nested-resolver bug (report 22 item 4) — LANDED, no longer a
   dependency.** CORRECTION (orchestrator, verified): this fix has shipped.
   `schema-next` HEAD is "preserve resolver through nested imports" and
   `resolution.rs:206` now reads `module_source.lower_with_resolver(engine,
   self)`. The `nexus → sema → contract` chain no longer drops the resolver.
   What remains genuinely unproven for lojix is NOT this bug but the
   **multi-effect pipeline** through `Continue` (cloud ran only one effect) and
   **streaming-subscription emission** (see the open question below) — lojix is
   the first to exercise both. Original (now stale) text follows: the bug was
   that `resolution.rs:206` lowered a directly-imported module with a fresh
   empty resolver, dropping the caller's resolver through nested imports;
   the one-line fix `lower_with_resolver(engine, self)` (`module.rs:203-213`)
   was present but uncalled.
4. **`meta-signal-cloud` package-name vs repo subtlety (report 22).**
   Resolution matches by registered Cargo crate-name string, not repo
   directory. So `meta-signal-lojix:meta-signal-lojix:*` imports resolve
   if the dep is wired by path, even before a separate repo exists — but
   the separate production repo is still a deployment gate.

## Q5 — Reconcile the stale three-layer-migration doc in signal-lojix

**Recommended answer: DELETE the entire `## MUST IMPLEMENT — three-layer
migration` section and the layer-table framing; KEEP the channel-boundary,
record-type, reply/event/stream domain vocabulary; RE-TARGET the whole
spec from `signal_channel!` + `signal-frame` to schema-derived per-plane.**

`signal-lojix/ARCHITECTURE.md` is built on a superseded model. What to do
section by section:

**DELETE:**
- §"MUST IMPLEMENT — three-layer migration" (lines 32-78) entirely. The
  Layer 1 / Layer 2 / Layer 3 framing is the OLD verb-layering model. In
  the schema-derived stack, Layer 1 = the contract's schema `Input`/`Output`
  roots, Layer 2 = the daemon's `nexus.schema` decisions, Layer 3 = SEMA
  classification is daemon-local. They are no longer "layers in one
  contract" — they are separate schemas in separate places. The whole
  section's premise (that this contract carries all three) is exactly the
  all-in-one error Spirit `2bgatqufm9m0dktxkv5` corrects.
- The references to designer reports 246/248 (the old three-layer design).
- The §3/§4 language about "one `signal_channel!` invocation" and the
  macro emitting enums — replaced by schema-derived emission.
- The `signal-sema` `ToSemaOperation` projection paragraphs (§"Layer 3",
  §4 last bullet) — Sema classification is daemon-local in the new model,
  not a contract concern.

**KEEP (re-homed):**
- §1 Channel Boundary (who produces/consumes) — still accurate.
- The domain record vocabulary: `DeploymentIdentifier`, the phase events
  (`Submitted`…`Failed`), `GenerationListing`, the typed `*Rejected`
  reasons. These become the contract schema's namespace types.
- The boundary rules that are still true: pure contract crate, no behavior/
  storage/actors, no `Unknown` variant, typed errors not strings, full
  English names.

**RE-TARGET:**
- Split into two contracts (Q1). `signal-lojix` = ordinary (Query + the
  Watch/Unwatch subscriptions); `meta-signal-lojix` = policy (Deploy /
  Pin / Unpin / Retire). Each is a wire-only `schema/lib.schema`.
- `signal-frame` is correct as the wire kernel (the spec already shifted
  to it, §"Frame layer"), but framing comes from schema emission now, not
  a hand-written `signal_channel!`.

The `Note to remover` in the doc (lines 76-78) anticipates exactly this —
honor it: replace the MUST-IMPLEMENT section with a short
`## Migration history` paragraph noting the three-layer model was
superseded by the schema-derived per-plane triad (Spirit
`2bgatqufm9m0dktxkv5`, `1up1ufia24c2opn3mqn`).

## Q6 — Actors: how Kameo actors relate to generated Nexus/SEMA engines

**Recommended answer: the generated `NexusEngine` / `SemaEngine` traits
ARE the engine surface; the deploy-pipeline concerns (build, copy,
activate, gc-root, container-observe) are NOT separate Kameo actors —
they are Nexus `CommandEffect` variants dispatched by the schema-emitted
runner. Collapse the prototype's 9-actor topology into the three-engine
+ effect-handler shape. Reserve real Kameo actors only for genuinely
concurrent long-lived sources (the container/systemd observer).**

This is the central tension between the two prototypes. Intent
`6wzz3up583b428kh3ok` says "deep actor system with actors whose
interfaces AND data shapes are schema-defined." The
`schema-deep-iteration-2` prototype read that as **one Kameo actor per
deploy concern** — `actor_topology.rs:42` asserts an `Engine` root with
**9 children**: AuthorizationGate, Builder, ClosureCopier, Activator,
GcRootPinner, ObservationFan, Store, TraceLog, NexusMailKeeper. Each is a
hand-written Kameo actor with its own message protocol
(`DriveBuild`, `DriveCopy`, `DriveActivation`, `DrivePin` — `nexus.rs`
imports).

The settled shape (Spirit `1326-1336`, cloud port, `triad-runtime`)
reads the same intent differently and is the one to follow:

- **The "actors whose interfaces are schema-defined" ARE the three
  engine traits.** `SignalEngine` (triage), `NexusEngine` (decide/heavy
  logic), `SemaEngine` (apply/observe) — each attached to ONE
  data-bearing noun (cloud: `SignalActor` / `Nexus` / `Store`, cloud
  report 18 §3.4). The schema defines their interfaces (Input/Output/
  NexusWork/NexusAction/SemaWriteInput/…) and data shapes. That satisfies
  "interfaces AND data shapes are schema-defined" precisely.
- **Build / copy / activate / gc-root are EFFECTS, not actors.** They are
  external IO steps in the deploy pipeline. In the cloud port the single
  Cloudflare call is one `CommandEffect`; in lojix the pipeline is a
  *sequence* of effects (Q2). The runner (`triad-runtime/src/runner.rs`)
  dispatches them and re-enters Nexus — no per-step actor, no
  `Box<dyn>`, no per-concern mailbox. The prototype's `Builder`,
  `ClosureCopier`, `Activator`, `GcRootPinner` actors collapse into
  `NixBuild`, `CopyClosure`, `ActivateGeneration`, `PathInfoGc` effect
  variants + their handlers.
- **The NexusMailKeeper IS the generated Nexus envelope, not a
  hand-written actor.** The prototype's `NexusMailKeeper` (`nexus.rs`)
  hand-rolls the mail lifecycle (Sent→Queued→Processing→Replied) that the
  schema emitter now generates as `signal::Signal<Root>` /
  `nexus::Nexus<Root>` envelopes with `MessageSent`/`MessageProcessed`
  hooks (schema-rust-next ARCH lines 135-146). Delete the hand-written
  keeper; use the generated envelopes.
- **The Store IS the SemaEngine impl** — that mapping the prototype
  already got right (`store.rs` ≈ `SemaEngine for Store`).
- **Genuine concurrency stays an actor.** The container/systemd observer
  is a long-lived independent source that must run concurrently with
  request processing. That is a legitimate Kameo actor (or a tokio task)
  whose only job is to assert observed transitions into SEMA via the
  effect/write path — the one place the actor model earns its keep. This
  is the lojix analogue of cloud's `RemoteOperationTracker` /
  `RateLimitGate` actors (cloud ARCH §"Actor Shape") that sit behind the
  engine, not in front of it.

So the deep-actor intent is honored — but the depth lives in the
**schema-defined engine traits + typed effect vocabulary + the
generated runner**, not in a wide hand-written actor fan-out. The
prototype's domain logic (it knows how to build/copy/activate and pin GC
roots, and it has sandbox tests that pass) is the valuable part to
salvage; its topology is the part to retarget. This is precisely the
double-implementation comparison the strategy intends
(`double-implementation-strategy.md`): the `schema-deep-iteration-2`
prototype and the cloud-derived per-plane shape diverge on actor
topology, and the divergence resolves toward the cloud shape because the
workspace ratified per-plane generation after the prototype was written
(`schema-deep-iteration-2/schema/lojix.schema` is all-in-one; Spirit
`2bgatqufm9m0dktxkv5` corrects all-in-one).

## Sequenced port plan (no-regret order)

Derived from cloud report 22's corrected fix path, adapted to lojix:

1. **Author the two wire contracts FIRST** — `signal-lojix/schema/lib.schema`
   (ordinary: Query + Watch/Unwatch) and `meta-signal-lojix/schema/lib.schema`
   (policy: Deploy/Pin/Unpin/Retire), wire-only, sharing record types via
   cross-crate import. They emit codec, no engines. Salvage the record
   vocabulary from both the stale signal-lojix ARCH and the prototype's
   `lojix.schema` namespace.
2. **Reconcile + delete the stale signal-lojix ARCH section** (Q5) so the
   contract spec matches the schema.
3. **Author the daemon plane schemas** — `lojix/schema/nexus.schema`
   (Effect enum = the deploy pipeline, importing both contracts' Input/
   Output) and `lojix/schema/sema.schema` (the four tables), importing
   EXACTLY the contract type names (avoid report 22 item-1 drift).
4. **Wire `build.rs`** per the cloud template (`CargoSchemaMetadata` +
   `DependencySchema` + per-plane targets). Confirm the schema-next
   nested-resolver fix (report 22 item 4) has landed on schema-next main,
   or flag it as a blocking dependency.
5. **Port the prototype's domain logic** into the generated engine impls:
   `Store` → `SemaEngine`, the build/copy/activate/pin functions →
   `CommandEffect` handlers, the Nexus decide loop replacing the
   hand-written NexusMailKeeper. Keep the container observer as a real
   actor behind the SEMA write path.
6. **Prove parity to cutover** — sandbox tests
   (`sandbox_build_pipeline.rs`, `sandbox_activation.rs` already exist),
   then at least one sandbox OS booted on the new logics (intent
   `6wzz3up583b428kh3ok`'s explicit done-criterion;
   `29o9zjczlfvp2n7o28d` makes passing sandbox testing a cutover
   precondition). Then retire the dual stacks (intent
   `75auhtr308tgt4kaa9a`, `a5anew11ndgk5cq40z`).

## Open question for the psyche

**The deploy event-stream subscriptions vs the cloud template's
read-only ordinary surface.** Cloud's ordinary contract has NO
subscribe/stream — it is pure `Observe`/`Validate` request/reply. Lojix's
ordinary contract MUST carry `WatchDeployments` / `WatchCacheRetention`
streaming subscriptions (push-not-poll deploy phase events). That means
lojix's `signal-lojix` needs `StreamingFrame` + stream-relation witnesses
that the cloud template never exercised. The schema-derived stream
emission path is therefore unproven by the cloud port — it may need the
same kind of schema-next/schema-rust-next enhancement that the root-import
gap needed (cloud report 20). Recommend confirming with the psyche / a
schema-next probe whether streaming-subscription emission is generation-
ready before committing the lojix contract to streams, vs. starting with
poll-based Query and adding Watch in a later slice.
