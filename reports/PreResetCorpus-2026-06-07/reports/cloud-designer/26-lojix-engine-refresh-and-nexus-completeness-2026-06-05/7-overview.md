# 7 — Overview: where the lojix engine rewrite stands, and what reaches cutover

cloud-designer lane synthesis, 2026-06-05. The fresh-look overview the
psyche asked for, synthesising the five finder reports (1 intent sweep,
2 functionality inventory, 3 nexus completeness, 4 runtime state, 5
raw/pretty boundary) and the adversarial review (6). Incorporates report
6's corrections rather than papering over them: the headline severity is
WORSE than the finders individually concluded, because the runtime arms
that DO exist are individually broken in ways no single finder caught.

Read-only synthesis. Schemas re-read direct from
`/home/li/wt/github.com/LiGoldragon/lojix/triad-port/schema/{nexus,sema}.schema`
to ground every load-bearing claim. Legacy parity measured against
`/git/github.com/LiGoldragon/lojix-cli/src/*.rs`. No build, no `jj`, no
`cargo` (the parallel editing workflow holds the working copy and is
finalizing the two-socket daemon loop — tasks #10-13).

## Where the lojix engine rewrite stands (fresh situation)

State it honestly, at three altitudes (report 6 §E2's resolution — name
all three, don't pick one):

1. **The SHAPE of the declared subset is sound and compiles GREEN.** The
   triad-port lib + bins compile; the daemon two-socket loop is being
   finalized in parallel (task #12/#13); both wire contracts are GREEN;
   the operation-root payload fix landed (report 25/4). The
   `SignalArrived -> Command* -> Continue` re-entry protocol
   (`nexus.schema:75-76`) is real and works; the `EffectCommand` /
   `EffectResult` 1:1 pairing is clean; the four SEMA tables
   (`sema.schema:71-82`) are declared and routed. The
   local-build-never-rejected discipline (dropped guard 783n) is
   correctly encoded as `BuildTarget [Local (Remote BuilderNode)]`
   (`nexus.schema:52`) being a first-class variant, not an error. This
   is genuine, hard-won progress and should not be undersold.

2. **The CATALOG COMPLETENESS fails the governing principle (z6qu).**
   The Nexus catalog declares 6 effect verbs (`ResolveFlakeAuth`,
   `NixEval`, `NixBuild`, `CopyClosure`, `ActivateGeneration`,
   `PathInfoGc`) over a legacy pipeline of ~19 distinct effects (report
   2) / ~10 grouped stages (report 3) — both land on "the catalog is
   roughly 3x too small." Under z6qu (Principle, VeryHigh, psyche
   2026-06-05: the Nexus schema is the engine's INTERNAL FEATURE
   CATALOG, every computation / filter / conditional write / internal
   logic-feature MUST be a declared verb+object, nothing inline), the
   ~13 unmodeled effects are exactly the features that will otherwise
   land as hidden inline handler logic.

3. **The RUNTIME of even the declared subset is BROKEN.** This is report
   6's sharpest correction and it changes the situation materially.
   Three of the six declared verbs cannot deploy ANY real node, and no
   finder caught these — they sit inside verbs reports 2/3 rated
   "covered" or "partial":
   - **A1: the eval attribute is wrong.** `run_nix_eval` evaluates
     `<flake>#<cluster>.<node>.drvPath` (e.g. `criome.prometheus`)
     instead of legacy `build.rs`'s
     `<flake>#nixosConfigurations.target.config.system.build.toplevel`.
     Every deploy fails at the eval stage against an attribute that does
     not exist.
   - **A2: activation sets a literal `$CLOSURE`.**
     `run_activate_generation` runs
     `nix-env -p /nix/var/nix/profiles/system --set "$CLOSURE"` — the
     literal shell token, never substituted. The pipeline's
     `closure_path` is never threaded into the activate command because
     `ActivateGenerationCommand` (`nexus.schema:60`) has NO `ClosurePath`
     field (schema-confirmed in this synthesis). Activation always sets
     the profile to the empty/unset closure.
   - **A3: copy/activate/gc address the bare node name.** They ssh to
     `<node_name>` instead of legacy `host.rs`'s always-
     `<user>@<criome_domain_name>` (e.g. `root@prometheus.cluster.criome`).
     The rewrite has no horizon projection (Gap D/G2) so it has no
     domain to address with and falls back to a name that won't resolve.

   Honest verdict: the current GREEN daemon is a correct-shaped skeleton
   that **cannot yet deploy a real node even within its 6-verb subset.**
   "GREEN compile" and "can deploy" are far apart here.

## Nexus-for-lojix: is every internal operation in the schema?

**Completeness verdict: NO.** The catalog declares the pipeline SHAPE
faithfully but fails z6qu's visibility test on three axes (report 3's
framing, all verified): (a) real engine features with NO verb; (b)
declared verbs whose feature is empty or smaller than the name; (c)
entire legacy pipeline stages collapsed out. There is also a recurring
INVERSE pattern: the SEMA layer is over-built relative to Nexus — durable
state with no Nexus verb that drives or reaches it.

### The prioritized GAP LIST (Nexus verbs/objects not yet declared)

Ordered by blocks-cutover severity. Each is a feature that, implemented
inline, would violate z6qu.

**Blocks cutover (the rewrite cannot build/deploy a real closure
without these):**

1. **Artifact materialization — the override-input subsystem (LARGEST
   HOLE).** No verb for horizon-projection -> `horizon.json`/`flake.nix`
   templates -> `nix hash path --sri` nar-hash -> the four
   `--override-input horizon|system|deployment|secrets <ref>` refs
   (legacy `artifact.rs` + `cluster.rs:76 FlakeInputRef`).
   `NixEvalCommand`/`NixBuildCommand` carry NO input-ref field at all.
   This is the bridge that injects cluster data into the build; without
   it the rewrite can only model the shape of a build, not perform one.
   Recommend `EffectCommand::MaterializeArtifact` + thread
   `(Vec OverrideInput)` into eval/build commands.

2. **Horizon projection.** `project.rs:18 project` (proposal + viewpoint
   -> per-node `Horizon`) is the core typed-cluster-data computation EVERY
   downstream effect depends on (builder resolution, substituter URLs,
   home-user validation, the criome domain for addressing, the
   horizon.json artifact). It has NO Nexus verb. It is also the raw/pretty
   seam (9p8v) — horizon.json is RAW horizon serialized. Without it, A3's
   addressing break cannot be fixed. Recommend a `Project` Nexus verb (it
   becomes the future promoted-horizon daemon's Nexus body unchanged —
   the avvh seam).

3. **Secrets handling — entirely absent.** `artifact.rs:155 SecretsDir` /
   `ClusterSecrets` (sops files -> secrets override flake). Nothing in
   Nexus, SEMA, or either wire contract. Silent-correctness gap: a node
   needing router wifi passwords deploys broken. NOTE (report 6 A4): do
   NOT port the three hardcoded sops filenames forward — the secrets
   EFFECT must take its file set from projected horizon (cluster-data is
   horizon's, not a daemon const), per z6qu/a2t4.

4. **Remote input staging.** `stage.rs:170 RemoteInputStage` (mkdir +
   `rsync -a --delete` the generated input dirs to the builder, rewrite
   refs to remote paths). No verb. Remote builds cannot resolve the
   generated override inputs. Recommend
   `EffectCommand::StageRemoteInputs`. Tightly coupled to gap 1.

5. **The three runtime breaks must be fixed alongside the schema gaps**
   (A1/A2/A3 above). `ActivateGenerationCommand` needs a `ClosurePath`
   field; eval must build the nixos-toplevel / home-activationPackage
   attribute; copy/activate/gc must address the criome domain (which
   requires gap 2's projection). These are not new verbs but they are
   cutover blockers inside existing verbs.

**Clean follow-on (real features, but the daemon can reach a first
usable cutover without them, or they are daemon-new beyond Stack A
parity):**

6. **Activation richness — EFI reconcile + BootOnce + Test-no-bootloader.**
   `activate.rs` flattens to the `ActivationKind` discriminant; the
   `reconcile_efi` (bootctl set-default/oneshot), the transient
   `systemd-run --wait` BootOnce unit, and Test-skips-nix-env are all
   lost (all `ActivationKind`s produce identical IO today). Intent xv9v
   makes BootOnce load-bearing (Prometheus uses it until out-of-band
   access). Blocks parity for any node that needs Boot/BootOnce; may
   follow if first cutover nodes use Switch only.

7. **Home activation has no effect verb.** `activate.rs:266 HomeActivation`
   (profile/activate + local-vs-remote context detection) collapsed —
   `HomeMode` Build/Profile/Activate is dropped and a home closure would
   activate against the SYSTEM profile. Blocks HomeOnly cutover; clean
   follow-on if first cutover is system-only.

8. **CheckHostKeyMaterial — stub on the wrong plane.** A no-op returning
   empty mismatches, modeled as a SEMA read when it is real remote ssh +
   parse + diff IO (most-corroborated finding, reports 2/3/4 + 6 B3).
   Move to `EffectCommand::CheckHostKeyMaterial` and build the real
   publication diff. Not a deploy-path blocker.

9. **GitHub-auth flake resolution (intent 2qhw).** `ResolveFlakeAuth`
   does `nix flake metadata` only — no gopass token fetch / access-tokens
   injection. Verb name advertises auth the engine lacks. Needed for any
   private-flake build.

10. **PathInfoGc is inert.** No `path-info -r` reachability, no two-phase
    TTL, never reads the declared GcRoot/GenerationSlot retention tree.
    The retention model is declared but does nothing. Daemon-new; not a
    Stack A parity blocker.

11. **Subscription handshake is inline.** `open/close_subscription`
    (token mint + conditional reply) is hand-written Rust, no verb.
    Recommend a `SubscriptionRegistry` SEMA table (tokens are durable
    registry state). Needed before real push streaming, not before
    cutover.

12. **ReadEventLog unreachable + wired to fail.** SEMA read fully built
    but no ordinary Input verb reaches it, and `decide_read_completion`
    treats its completion as a `MalformedSelector` error. Add an ordinary
    `ReadEvents` verb, or drop the dead arm.

13. **Container observation, cache-retention events, the deploy stage
    machine** — the inverse-z6qu cluster: SEMA write paths
    (`RecordContainerTransition`, `LoggedEvent::CacheRetention`) fully
    built with NO producer; pin/unpin/retire mutate slots but append no
    retention event; and the deploy stage machine is a PRIVATE Rust enum
    (`DeployStage`, `schema_runtime.rs:56-67`) invisible to the schema —
    with a name-vs-action mismatch (report 6 B4: `BuildingRecorded`
    fires activate; the stage names describe the prior phase, not the
    next action). Per z6qu the pipeline sequencing is the engine's
    central logic-feature and must be schema-declared.

14. **Phase-emission incompleteness (report 6 B5).** Only 3 of 7
    declared `DeploymentPhase` values are ever recorded (Building,
    Copying, Activated); Submitted/Built/Activating/Failed never reach
    the event log. A z6qu visibility gap AND a parity gap against the
    wire contract's own declared phases.

## Runtime database-state model

### Target table model (report 4 §6, with type collapse)

Five tables, each keyed, redundant types collapsed:

- **Generation** (ONE durable record, replaces the
  `LiveGeneration`/`GcRoot` duplication). Primary key
  `GenerationIdentifier`; live-set index `(ClusterName, NodeName,
  DeploymentKind)`; unique `PinLabel` secondary index. The live-set is
  the view where slot ∈ {Current, BootPending}; gc-roots is all rows.
  Add `recorded_at` (for Recent/TTL grace) and `rollback_ordinal`.
- **DeployPipelineTable** (NEW) — one row per accepted-not-finished
  deploy, keyed by `DeploymentIdentifier`, carrying the resolved deploy
  + `DeployStage` + `closure_path`. The durable mirror of the in-memory
  cursor.
- **EventLogTable** — monotonic-keyed by `EventLogPosition` (a stored
  counter, not `Vec::len()`).
- **ContainerLifecycleTable** — keyed `(ClusterName, NodeName,
  ContainerName)`; carry as explicitly not-yet-load-bearing (no producer,
  no consumer wired).
- **Sequence/metadata table** (NEW) — the five persisted counters + the
  `DatabaseMarker`.

### Gap list — missing durable state (report 4 §7, verified by report 6 C1)

**Blocks production cutover:**

1. (C, high) **Live-set is append-only and never demotes.** Two
   switch-deploys to one node leave TWO rows both in slot `Current`. The
   keyed `BTreeMap<(cluster,node,kind)>` ARCHITECTURE.md:44 names is not
   built; needs key-overwrite with prior `Current` demoting to
   `Rollback`.
2. (C/F, high) **Rollback ring entirely absent.** `GenerationSlot::Rollback`
   is a declared variant NEVER constructed anywhere (grep-confirmed zero,
   report 6 C1). No N=4 ring, no eviction. A declared engine feature with
   no implementation.
3. (C, high) **In-flight deploy is non-durable.** `active_deploy` is an
   in-memory `Option<DeployPipeline>` on `SchemaRuntime`;
   `RecordDeploySubmitted` touches NO table. Restart loses every accepted
   deploy — a deploy daemon that forgets every generation on restart
   cannot run production.
4. (P, deferred-but-blocks-cutover) **The whole `Store` is in-memory
   Vec scans.** Real sema-engine/redb/`.sema` persistence is entirely
   unbuilt — no `Engine::open`, no `register_table`, no
   `state_file_path` in `DaemonConfiguration`. GREEN in-memory is fine
   for a compile but is a hard cutover blocker.

**Clean follow-on:**

5. (F, high) **Cache-retention events have no producer** — pin/unpin/
   retire emit no `CacheRetention` log entry, so `WatchCacheRetention`
   and `retention_events` are always empty.
6. (C, med) **ReadEventLog unreachable from the wire** (dead code; wire
   or drop).
7. (Boundary, med) **CheckKeyMaterial is on the wrong plane** (move to
   Nexus effect — see Nexus gap 8).
8. (F, low) **Recent slot has no timestamp** — the narinfo-TTL short-
   grace window is uncomputable. NOTE report 6 C2: the wire
   `GenerationSlot` is a bare flat enum, so the parameters
   (`Recent <timestamp>`, `Rollback <ordinal>`) must be sibling columns
   OR the wire enum must be parametrized — a wire decision.

### Type-reuse minimalism findings (a2t4 — collapse these)

- `LiveGeneration` vs `GcRoot` vs wire `Generation`: three near-identical
  generation records -> ONE durable `Generation`; live-set and gc-roots
  become keyed views. `project_generation` already proves the live->wire
  copy is field-for-field.
- `ActivationCommit` is a subset of `LiveGeneration` that smuggles
  kind/deployment-id/activation out of the Nexus cursor (a 3d5z
  separation smell) — carry the full fact; converge with `Generation`.
- `StateMarker` == `DatabaseMarker` (byte-identical; two convert methods
  bridge them) -> import `DatabaseMarker` into the SEMA plane, drop
  `StateMarker`/`CommitSequence`/`StateDigest`.
- `PhaseReceipt` == `ContainerReceipt` (both `{EventLogPosition
  StateMarker}`) -> one `EventLogReceipt`.

### Concurrency model — a decision is needed

`StateDigest` is fake (= `commit_sequence`; schema-confirmed
`sema.schema:67-69`), and no write takes an expected marker — so the
advertised optimistic-concurrency model is actually WRITE-WINS.
Recommendation: drop `StateDigest` for single-writer parity now
(ARCHITECTURE.md:166 one instance; opvx says the contract shouldn't
encode parallelism), with real content-hash + precondition checks as the
multi-writer follow-on.

### In-memory -> persistence deferred list (report 4 §5)

`Engine::open` on a `.sema` file (add `state_file_path` to
`DaemonConfiguration`); `register_table` for all 5 tables WITH keys;
replace the four Vec scans with engine match/range ops; persist the five
counters; atomic multi-table commit for the live-set+gc-roots dual write;
post-commit subscription bridge (blocked on the schema-next event-frame
emission follow-on, report 25 §6).

## Raw/pretty horizon boundary

### The crisp boundary contract (report 5 §1)

- **RAW horizon** = input pass-through + policy-free identity derivations
  (`criome_domain_name`, `system`, ssh/nix/ygg pubkeys + lines) +
  cross-node fan-in lists + arch resolution + typed validation + secret-
  binding resolution. The test: a field is RAW if it is authored cluster
  data OR a policy-free identity derivation every consumer would
  otherwise recompute identically. No `>=`, no `&&` of role flags, no
  threshold.
- **PRETTY horizon** = every DECISION field: `AtLeast` size/trust
  ladders, the gating booleans (`is_dispatcher`/`is_remote_nix_builder`/
  `is_nix_cache`/`is_large_edge`/`enable_network_manager`), `BehavesAs`/
  `TypeIs`/`ComputerIs`, lid-switch policy, derived routing/capacity
  (`max_jobs`, `nix_url`, `builder_configs`, `cache_urls`). The test: a
  field is PRETTY if its value is a decision.
- The fused `Node` struct cleaves into `RawNode` + `PrettyNode`, pretty
  deriving FROM raw via `impl From<&RawNode>` (verb-belongs-to-noun, NOT
  a free `project_pretty`).

### What lojix consumes (the sharpest finding — verified, report 6 D1)

lojix consumes BOTH raw and a THIN pretty slice — it is NOT a raw-only
consumer. It reads two pretty gating fields directly in Rust:
`node.is_remote_nix_builder` (builder gating, `deploy.rs:60`) and
`node.nix_url` (cache substituters, `deploy.rs:211-241`), plus raw fields
for SSH addressing / host-key verification. So pretty horizon has two
consumer profiles the spec must name:

- **deploy-routing pretty** (`is_remote_nix_builder`, `is_nix_cache`,
  `nix_url`, `builder_configs`, `cache_urls`, `max_jobs`) — consumed by
  lojix in Rust AND CriomOS in Nix.
- **OS-config pretty** (lid-switch, `enable_network_manager`, extra-
  groups, behaves-as, the ladders) — CriomOS only.

Consequence: pretty horizon's primary form must be a typed Rust record,
not a Nix-attrset emitter; the Nix attrset is a serialization OF the
record.

### The forward-promotion seam (avvh) — do NOW at near-zero cost

avvh (Clarification, High, 2026-06-05): the split is ALSO a forward-
integration seam toward later promotion of raw horizon into a real
component. Prepare it now, structurally, for free: (a) raw is a
standalone crate with NO pretty dependency; (b) raw is a types-only
schema document (the `vu2k` two-position `{} { ... }` shape that
`horizon-core/schema/magnitude.schema` already runs); (c) keep the
projection a single method on `ClusterProposal` (it becomes the future
daemon's Nexus `Project` body unchanged); (d) do NOT add Input/Output to
raw prematurely. Promotion then = add a wire document importing raw types
+ move the method into Nexus — not a rewrite.

### The x8iv fork recommendation (CONFIRMED, with a correction)

Build the raw/pretty split in **horizon-next** (schema-derived;
`horizon-core` already proves the types-only pattern), NOT the horizon-rs
hack (splitting hand-written structs slated for deletion is wasted work).
BUT horizon-next's `horizon` crate currently declares Input/Output and
emits a full Signal/Nexus/Sema triad — the wrong runtime shape per
tvbn/vu2k. Drop that triad from the projection crate until the x8iv
promotion decision lands; mint a triad only when the psyche decides
promotion is on.

### Fence this part for the synthesis (report 6 D1)

Report 5's §1-2 (the raw/pretty boundary + lojix dual-consumption) is
VERIFIED and SOUND. But its §3-5 reads files OUTSIDE this session's
lojix-triad-port scope (`horizon-rs`, `horizon-next`, `horizon-core`) and
asserts content the adversarial reviewer could not independently confirm
— specifically the `horizon-core` 6-point ladder (`Zero Min Low Medium
High Max`) vs `horizon-rs` 5-point (`Zero Min Medium Large Max`)
divergence, the horizon-next triad shape, and the stale-INTENT.md claim.
These are presented as report-5-sourced-and-unverified; the Magnitude-
ladder divergence is load-bearing for any horizon parity work and needs
its OWN verification pass before action. Treat horizon-repo promotion
mechanics as a SEPARATE horizon-scoped follow-up, not folded into the
lojix engine-completeness conclusions.

## Prioritized actionables toward cutover

### Blocks cutover — do these to reach a usable first cutover

In dependency order:

1. **Declare + build artifact materialization** (`MaterializeArtifact`
   verb + `OverrideInput` threaded into eval/build). Without it no real
   closure builds. (Nexus gap 1.)
2. **Declare + build horizon projection** (`Project` Nexus verb). It
   feeds materialization, supplies the criome domain for addressing
   (fixes A3), and resolves builders/substituters (fixes the inline
   gates G4/G5). (Nexus gap 2.)
3. **Fix the three runtime breaks** (A1 eval attribute, A2 closure-path
   threading + add `ClosurePath` to `ActivateGenerationCommand`, A3
   criome-domain addressing). Without these the existing 6 verbs cannot
   deploy. (Nexus gap 5.)
4. **Secrets effect** (`MaterializeSecrets`, file set FROM horizon, not a
   const). Silent-correctness blocker for nodes needing secrets. (Nexus
   gap 3.)
5. **Remote input staging** (`StageRemoteInputs`) — IF the first cutover
   uses a remote builder. (Nexus gap 4.)
6. **Real sema-engine persistence** + the keyed live-set (overwrite/
   demote) + durable in-flight deploy table + rollback ring. A daemon
   that forgets generations on restart cannot run production. (State
   gaps 1-4.)
7. **Activation richness for the first cutover nodes' needs** — at
   minimum Switch must work end-to-end; EFI-reconcile + BootOnce only
   if a first-cutover node needs Boot/BootOnce (xv9v: Prometheus does).
   (Nexus gap 6.)

### Deferred — clean follow-on after first cutover

- Full schema-derived streaming platform (brgo) — handshake+poll
  suffices until the schema-next event-frame substrate lands; explicitly
  does NOT block cutover. Subscription registry (Nexus gap 11),
  cache-retention event producers (state gap 5), ReadEventLog wiring
  (gap 12), container-lifecycle observer (gap 13) ride this.
- PathInfoGc retention engine (Nexus gap 10) — daemon-new, beyond Stack
  A parity.
- Home activation (Nexus gap 7) — unless first cutover includes HomeOnly.
- CheckHostKeyMaterial real diff + plane move (Nexus gap 8).
- GitHub-auth flake resolution (Nexus gap 9) — needed for private flakes.
- Pretty horizon layer — lands AFTER cutover (9p8v/m85j timing; parity
  is the bar, the raw/pretty collapse does not gate cutover). Prepare the
  seam now (raw standalone types-only crate, projection as a method).
- Lift the deploy stage machine into the schema (Nexus gap 13); collapse
  the redundant types (a2t4); real optimistic-concurrency (state §4).
- Type-minimalism collapses and phase-emission completeness (gap 14).

### Stale-surface manifestation chores (same-branch, continuous-manifestation)

- **lojix ARCHITECTURE.md is stale** (dated 2026-05-15): single-socket
  vs the two-socket/meta-socket split (vudl/3chp), `sema-engine`/
  `signal-core` vs `schema_runtime` + signal-frame + `.sema`, the
  Kameo-actor code map, "push never poll" contradicted by 2tfa. Needs a
  same-branch manifestation pass.
- **6njo host-vs-role chore** outstanding — nexus.schema header comment
  still references "prometheus"; should name the role.
- **horizon-next/INTENT.md stale** (report-5-sourced) — still frames the
  runtime shape as "open" and Input/Output as the direction, against
  tvbn/vu2k. Horizon-scoped, separate verification pass.

## Open questions for the psyche

1. **First-cutover scope — which Stack A surface gates the switch?**
   Intent says "reach parity then switch" (tvbn/fe2j) but never
   enumerates the exact parity bar. Concretely: is the FIRST cutover
   system-only Switch deploys to a small node set (deferring HomeOnly,
   BootOnce/EFI-reconcile, secrets, remote builders), or must full Stack
   A parity land first? This single answer reorders the entire blocks-
   cutover list above.

2. **Real persistence vs in-memory for the first cutover.** A daemon
   that forgets every generation on restart cannot run production — but
   building real sema-engine `.sema` persistence is substantial. Is the
   first cutover allowed to run in-memory on a small node set as a
   sandbox-pass milestone (v5d4), or must durable state land before any
   production node switches?

3. **Plan/approval state — in scope or vestigial?** (report 6 C3.)
   `RejectionReason::PlanNotApproved` and `PinSlotExhausted` are
   declared-reasons-without-features, mis-wired to lock-poison errors and
   never produced. Is plan-gated deploy approval a lojix feature to build,
   or should these vestigial reasons be dropped?

4. **Streaming-substrate provenance (brgo's carried question).** Was
   signal-frame's existing `StreamingFrameBody`/`ObservableSet` deliberate
   scaffolding ahead of this work, or leftover? This most changes the
   full-schema-derived-streaming effort estimate and whether the platform
   project is cheap or expensive.

5. **CheckKeyMaterial — confirm the plane move.** Three reports + the
   adversarial review agree it is real host IO mis-modeled as a SEMA read
   and currently a no-op stub. Confirm moving it to
   `EffectCommand::CheckHostKeyMaterial` and building the real publication
   diff (it is treated as settled by the reports, but it changes a wire/
   plane boundary, so a psyche nod closes it).

6. **x8iv promotion direction (carried, still open).** avvh decided the
   raw/pretty SPLIT but explicitly left open whether raw horizon gets
   promoted into a full triad component, and whether horizon-next is the
   forward base. The split prep is free now; the promotion is a separate
   decision. Does the psyche want to signal a direction, or keep it
   open while the lojix cutover proceeds?

7. **Live deploy observation fidelity (report 2 G17).** Accept coarse
   phase-only deploy events (`DeploymentPhaseEvent`
   Building/Built/Activated), or model live nix-progress-line events to
   preserve Stack A's line-by-line terminal streaming? Affects the
   streaming grammar and the cutover operator experience.

## Bottom line

The charter (tvbn), the Nexus-catalog principle (z6qu), the SEMA
expectations, the raw/pretty split (9p8v/avvh), and minimalism (a2t4) are
SETTLED and mutually consistent as of today's records. The triad-port
schemas are faithful to the CHARTER and to the pipeline SHAPE — but NOT
yet to z6qu: the Nexus catalog is a 6-verb skeleton over a ~19-effect
legacy pipeline, the materialization/override-input subsystem is entirely
absent, the SEMA layer is over-built with no producers, the stage machine
is a private Rust enum, and — the severity correction the finders missed —
three of the six declared verbs are non-functional at runtime (wrong eval
attribute, literal `$CLOSURE`, bare-node-name addressing). The current
GREEN daemon cannot deploy a real node even within its own skeleton.

The path to a usable cutover is concrete and ordered: declare + build
materialization and horizon projection, fix the three runtime breaks
(including adding `ClosurePath` to `ActivateGenerationCommand`), add
secrets + remote staging, and land real persistence with a keyed
demoting live-set. Streaming, the GC retention engine, home activation,
and the pretty-horizon layer are clean follow-ons that the cutover does
NOT gate on. The seven open questions above — most importantly the first-
cutover parity scope and the in-memory-vs-persistence milestone — need a
psyche decision to fix the ordering.
