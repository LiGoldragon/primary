# CriomOS Lojix Rewrite Audit And Production Vision

## Frame

This report audits the current CriomOS plus Lojix rewrite surface and
describes a production path that improves Horizon rather than merely
porting the current production stack into a new daemon wrapper.

The source set for this pass:

- `protocols/active-repositories.md`
- `reports/system-operator/162-production-to-lean-criomos-reconciliation-2026-05-27.md`
- `reports/system-operator/163-critique-of-162-after-schema-next-refresh-2026-05-27.md`
- `reports/system-designer/29-lean-horizon-cluster-data-shape.md`
- `reports/system-designer/34-mvp-and-sandbox-audit/5-overview.md`
- `reports/system-designer/34-mvp-and-sandbox-audit/4-cutover-to-main-deployment-requirements.md`
- `reports/system-designer/35-schema-deep-new-logics/1-vision-schema-deep-new-logics.md`
- `reports/system-designer/35-schema-deep-new-logics/3-overview.md`
- `reports/system-designer/36-criomos-reconciliation-audit.md`
- `reports/designer/385-nota-schema-next-stack-design-via-nix-tests-2026-05-27.md`
- `reports/operator/212-brace-namespace-and-schema-modules-2026-05-27.md`
- live worktree state in `lojix`, `signal-lojix`, `horizon-rs`,
  `goldragon`, `CriomOS`, `CriomOS-home`, `CriomOS-lib`, and
  `criomos-horizon-config`.

## Executive Finding

The production stack is still the only deployable path. It has recent
hardening work: remote builder caps, router Wi-Fi projection fixes,
thermald and Nix job safety, stateful secrets direction, and several
production full-OS remote builds passing through Prometheus.

The `horizon-leaner-shape` rewrite is the nearest continuity branch,
but it is not production-ready. It carries important production fixes,
yet its Horizon data source is stale compared with production
`goldragon/datom.nota`, its Horizon parser/projection is mid-migration,
and the new `lojix` daemon still lacks the system integration needed
for a real cutover.

The `schema-deep` Lojix pilot is architecturally cleaner than the lean
branch. It has a schema-authored daemon shape, generated typed nouns,
deep actor topology, no-free-function checks, and a green Nix test
family. It is still a pilot: storage is in-memory, Criome
authorization is not live, owner policy signal is absent, real nspawn
activation is not wired, and it does not yet consume the production
Horizon/CriomOS stack.

The right production vision is not "finish the current lean branch as
is." The better target is:

1. Keep production stable on `lojix-cli` until replacement witnesses
   exist.
2. Use `schema-deep` as the new Lojix architecture target.
3. Rebuild Horizon as a schema-authored proposal to view reducer using
   the current NOTA/schema-next direction.
4. Carry forward every proven production fix into that target.
5. Shadow-test old projection versus new projection before activation.
6. Cut over only after remote full-OS builds and sandbox activation
   witnesses pass.

## Current Production Stack

Production today is the old stack:

- `horizon-rs/main`
- `lojix-cli/main`
- `CriomOS/main`
- `CriomOS-home/main`
- `CriomOS-lib/main`
- `goldragon/main`

The live deploy shape is monolithic: `lojix-cli` reads the cluster
proposal, projects Horizon, stages flake inputs, invokes Nix, copies
closures, and activates targets.

### Production Strengths

Production has the best operational proof:

- Zeus, Prometheus, and Tiger full-OS remote builds passed in the
  recent sweep.
- Prometheus is the active remote builder path.
- Current `goldragon/datom.nota` uses bracket strings, curly maps,
  Pascal booleans, and the current production `nota-codec` shape.
- Recent production fixes addressed concrete cluster problems:
  router Wi-Fi projection, Nix builder caps, system normalization,
  thermald/fan safety, and DNS/networking drift.

### Production Weaknesses

Production is structurally old:

- The CLI is too powerful; deploy effects live in the caller process
  rather than in a daemon with durable state and observations.
- The deployment topology is implicit. Builder, cache, source staging,
  target activation, and rollback are not modeled as durable daemon
  state.
- The Horizon shape still carries old debt: species/service splits,
  booleans, view-side derived predicates, and values that should be
  derived by Horizon or CriomOS rather than authored in cluster data.
- Repository source distribution can fail from local assumptions. The
  `repository-ledger` localhost input caused the Ouranos production
  build failure in the last sweep.
- Aarch64 deployment is not capability-planned; Balboa fails late
  because Prometheus cannot build that target.

Production is therefore stable enough to keep, but not the shape we
should keep extending.

## Current Rewrite Surfaces

### Horizon Leaner Shape

The branch family `horizon-leaner-shape` spans the lean rewrite:

- `lojix`
- `signal-lojix`
- `horizon-rs`
- `goldragon`
- `CriomOS`
- `CriomOS-home`
- `CriomOS-lib`

The intent is sound: merge node kind and feature booleans into a
variant-first role vector; keep cluster data as dials; move operational
constants and predicates into Horizon/CriomOS rather than cluster
authored records.

The implementation is uneven.

Live findings:

- `CriomOS/horizon-leaner-shape` has the production-fix port at change
  `ptzmopzw` / commit `95dda319` with many file changes on the mutable
  branch tip.
- `horizon-rs/horizon-leaner-shape` has documentation and intent
  updates on a mutable change, but the code still carries old
  namespaces such as `species`, view-side node derivations, and
  service split modules.
- `goldragon/horizon-leaner-shape/datom.nota` is stale: it still uses
  `(ClusterProposal ...)`, `(Entry key value)` maps, quoted strings,
  lowercase booleans, and older per-node fields. Production
  `goldragon/main/datom.nota` is ahead on the current NOTA shape.
- `signal-lojix/horizon-leaner-shape` has a large mutable change
  migrating to contract-local verbs and `signal-frame`; it is important
  work, but it is not yet a settled clean base for cutover.
- `criomos-horizon-config` exists only in the canonical checkout and
  has an unfinalized `AGENTS.md` change. There is no visible lean
  worktree at the expected path.

The lean branch is useful as a carry-forward staging area. It is not
yet the clean replacement stack.

### Schema-Deep Lojix

The `lojix/schema-deep` branch is the better daemon architecture.

What it has:

- `schema/lojix.schema` defines 28 typed nouns, including `Input`,
  `Output`, `SemaCommand`, `SemaResponse`, `ActorRequest`,
  `ActorReply`, payload records, newtypes, and daemon configuration.
- `schema-next` and `schema-rust-next` generate Rust types.
- Hand-written Rust attaches methods to emitted nouns.
- Kameo actor topology is dense and named: runtime root, socket
  listener, dispatcher, authorization, builder, copier, activator,
  GC-root pinner, store, observation fan, and trace log.
- Nix tests cover schema lowering, frame round trips, executor
  lowering, actor topology, no free functions, no zero-sized actors,
  trace witnesses, daemon plus CLI build-only pipeline, and a sandbox
  activation witness.
- The branch is clean and pushed at `schema-deep` with report-backed
  green checks.

What it lacks:

- Durable redb storage; store is in-memory.
- Real Criome authorization; policies are placeholders/test bypasses.
- `owner-signal-lojix`; owner policy vocabulary is absent.
- Real source staging; repository source distribution is not modeled
  as a first-class plane.
- Real nspawn root/cgroup activation; the current witness uses a
  sandbox marker command.
- Full production Horizon projection integration.
- Full CriomOS/CriomOS-home cutover integration.

This branch proves the right internal architecture. It does not yet
prove production replacement.

### Schema Substrate

The NOTA/schema substrate has moved past the lean branch assumptions.

Current direction:

- NOTA strings use bracket forms only.
- Namespace braces are key/value maps, not parenthesized named
  objects.
- `schema/lib.schema` is the crate entry point.
- Single-colon names express schema module paths.
- Generated Rust should move toward `src/schema/...` so schema-derived
  code is reviewable and visible.
- The stack still lacks full sibling imports, cross-crate imports,
  schema diff/upgrade, append-only namespace checks, and schema-level
  vector support in the durable form.

This matters because the production replacement should not spend much
energy making old `nota-codec` and old hand-authored Horizon shapes
slightly less old. The durable path is schema-authored Horizon and
schema-deep Lojix.

## Improved Horizon Vision

Horizon should become a small, schema-authored reducer. It should not
be the place where all OS policy, service defaults, ports, domains,
and provider constants are authored.

### Inputs

The reducer takes:

- `HorizonProposal`: pan-horizon constants and operator-owned facts.
- `ClusterProposal`: cluster-authored facts only.
- `Viewpoint`: daemon-derived `(cluster, node)` lens.
- Optional source and secret references by logical name.

The Lojix daemon, not the CLI, derives the viewpoint and calls:

```text
ClusterProposal::project(&HorizonProposal, &Viewpoint) -> view::Horizon
```

### Cluster Proposal Boundary

Cluster data should contain only facts the cluster owner must author:

- cluster name and node names;
- node placement, hardware, disks, boot, and interfaces;
- public keys and public certificate material;
- trust magnitudes;
- secret references, not secret values;
- provider selections;
- feature and role variants.

Cluster data should not contain:

- internal or public domain suffix constants;
- port numbers;
- service URLs derived from host/cluster identity;
- router SSID strings when they can derive from cluster name;
- Nix cache URL templates;
- resolver listen addresses;
- model catalogs;
- provider implementation catalogs;
- operational defaults owned by CriomOS.

### Variant-First Shape

The cluster proposal should prefer self-describing variants over
booleans and loose optional records.

Good shape:

```text
roles = [
  Center
  TailnetClient
  (NixBuilder (Some 6))
  NixCache
  LargeAi
  (Router router-interface-record)
  (PersonaDevelopment [GitoliteServer])
]
```

Bad shape:

```text
is_builder = true
is_cache = true
large_ai = true
router_interfaces = Some(...)
persona_development = true
gitolite = true
```

The role vector lets the reader see the node's purpose without
position-counting a long field list. Data-carrying variants keep
inline tuning next to the feature being tuned.

### Horizon Output

The projected `view::Horizon` should give CriomOS exactly the facts
it needs to build. It should not make CriomOS reverse-engineer cluster
intent from raw proposal data, but it should also avoid emitting every
derived predicate as Rust-side booleans when CriomOS-lib can derive
them cleanly from roles and placement.

The clean split is:

- Horizon validates cluster data and produces typed, viewpoint-scoped
  identity and trust facts.
- CriomOS-lib owns operational constants and predicate helpers needed
  by Nix modules.
- CriomOS consumes projected fields and CriomOS-lib predicates.
- CriomOS-home consumes only user/profile-level projection and package
  surfaces.

### Horizon Tests

The improved Horizon needs architecture tests, not only round-trip
tests:

- current production `goldragon/datom.nota` parses under the new
  schema;
- every node has exactly one kind-role;
- role vectors, not booleans, carry optional node features;
- no concrete cluster node name decides a CriomOS module;
- cluster data contains no domain suffixes or ports;
- router SSID derives from the cluster identity;
- Nix builder and cache settings derive from roles and key material;
- projected views are stable enough for CriomOS/CriomOS-home
  consumers;
- old production projection and new projection agree on currently
  deployed nodes where the semantics are meant to be equivalent.

## Lojix Production Vision

The replacement Lojix stack should be a component triad:

- `lojix`: daemon/runtime repo with thin CLI.
- `signal-lojix`: working signal contract.
- `owner-signal-lojix`: owner policy signal contract.

The CLI has exactly one peer: `lojix-daemon`. It sends one typed
Signal request frame and prints one typed reply. It does not open
Horizon files, databases, Nix stores, or cluster proposal files.

The daemon owns the deployment planes:

- request intake;
- source staging;
- Horizon projection;
- authorization via Criome;
- build scheduling;
- binary cache/source transfer selection;
- closure copy;
- activation;
- GC-root pinning;
- deployment ledger;
- observation stream;
- rollback and retirement policy.

Each non-trivial plane should be an actor with typed messages and trace
witnesses. Effects must not hide inside helper methods.

## Production Path

### Phase 0 — Hold Production Stable

Keep production on `lojix-cli/main` until the replacement stack has
shadow proof. Continue applying live safety fixes to production main
when needed, but every production fix gets a carry-forward entry for
the rewrite target.

Builds that touch full systems should continue using remote builders
with local `--max-jobs 0` discipline where appropriate. Laptops should
not run uncontrolled full-closure builds.

### Phase 1 — Pick The Amalgamation Target

Recommendation: choose `lojix/schema-deep` as the daemon architecture
target, with `horizon-leaner-shape` as the source of domain lessons
and production-fix ports.

This avoids spending the next production replacement cycle on an
intermediate daemon that is already less elegant than the schema-deep
pilot.

### Phase 2 — Make Horizon Schema-Authored

Move Horizon toward the schema-next stack:

- author `schema/horizon.schema` or equivalent crate-local schema
  files;
- model `HorizonProposal`, `ClusterProposal`, `Viewpoint`, and
  `view::Horizon` as schema-derived nouns;
- emit reviewable Rust under a schema module tree;
- attach projection methods to emitted nouns;
- preserve current production NOTA syntax rules;
- migrate `goldragon/datom.nota` once, from production current shape
  into the new variant-first schema.

This should be a fresh production-quality branch, not a pile of parser
compatibility on stale lean files.

### Phase 3 — Harden Schema-Deep Lojix

Bring the pilot to production capability:

- replace in-memory store with redb-backed SEMA storage;
- add `owner-signal-lojix` for policy;
- wire Criome authorization as the authority path;
- add source staging as a named actor plane;
- model builder/cache/target capability preflight;
- add aarch64 capability planning;
- split package outputs for CLI and daemon;
- write the CriomOS NixOS module for `lojix-daemon`;
- bridge `criomos-horizon-config` into daemon configuration;
- keep the single-argument NOTA rule for both daemon and CLI.

### Phase 4 — Carry Forward Production Fixes

Every item from `reports/system-operator/162-production-to-lean-criomos-reconciliation-2026-05-27.md`
should be rechecked against the schema-deep target:

- Nix job and core caps;
- normalized system names;
- thermald/fan policy;
- router Wi-Fi secret/reference shape;
- desktop audio policy;
- devshell and ghq layout;
- Chroma legacy removal;
- VPN catalog handling;
- WireGuard and untrusted proxy logic;
- builder/cache roles;
- repository-ledger/source staging;
- Balboa/aarch64 planning.

The carry-forward target is not merely the lean CriomOS branch. It is
the final schema-deep Lojix plus improved Horizon stack.

### Phase 5 — Shadow Projection

Before activation, run old and new projection in parallel:

- old `lojix-cli`/`horizon-rs/main` projects each production node;
- new schema Horizon projects the same nodes from the same cluster
  proposal;
- a Nix check compares the fields CriomOS consumes;
- differences must be classified as intentional migration,
  bug, or newly-visible debt.

This phase should produce inspectable artifacts, not just a pass/fail.

### Phase 6 — Sandbox And Remote Build Witnesses

The cutover needs proof at three levels:

- pure Nix checks for schema, projection, actor topology, and contract
  round trips;
- stateful daemon/CLI tests through the real socket;
- system tests on Prometheus using the nspawn/test-cluster path.

The minimum system witness should build and activate a test CriomOS
node through `lojix-daemon`, not through direct `nixos-rebuild` and not
through the old monolithic CLI.

### Phase 7 — Controlled Cutover

Cutover should happen only when the replacement can:

- build every production node that production can build today;
- reject unsupported aarch64 work before invoking Nix on the wrong
  builder;
- deploy at least one sandbox node through the daemon;
- produce durable deployment records and observation streams;
- roll back or leave an explicit recovery path.

The first live target should be a low-risk node. The production
`lojix-cli` path should remain available until at least one full
deployment cycle succeeds under the daemon stack.

### Phase 8 — Retire Old Stack

Only after successful daemon deployments:

- remove `lojix-cli` from home profiles;
- remove old Horizon compatibility fields and parser paths;
- remove stale lean branch work that did not become the target;
- update skills, repo `INTENT.md`, and architecture docs to name the
  daemon stack as production.

## Highest Risks

### Risk 1 — Confusing Three Rewrite Tracks

There are three different things in flight:

- production `main`;
- lean `horizon-leaner-shape`;
- schema-deep Lojix plus schema-next Horizon direction.

Treating lean as the final target will waste work. Treating
schema-deep as production-ready will break deployments. The right
move is explicit amalgamation.

### Risk 2 — Horizon Data Shape Drift

Production `goldragon/datom.nota` is more current than lean
`goldragon/datom.nota`. Any test that uses the stale lean file can
pass while proving the wrong input shape.

### Risk 3 — Source Staging Is Still Not A First-Class Plane

The Ouranos failure on `repository-ledger` is not an isolated URL bug.
It shows that source availability must be part of the daemon's
deployment plan. The future `SourceStager` or Arca-backed plane should
stage content-addressed inputs before build/activation proceeds.

### Risk 4 — Architecture Tests Can Accidentally Test Fakes

Several current witnesses prove the route through a shape, but not yet
the real host effect. The schema-deep activation witness is valuable,
but it is not a real nspawn activation. Production readiness requires
both pure witnesses and root/system witnesses.

### Risk 5 — Aarch64 Late Failure

Balboa currently fails because the available builder cannot build the
target. The new daemon should classify that before invoking Nix. It
should know the builder fleet and decline or route work by capability.

## Immediate Recommendations

1. Declare `schema-deep` the Lojix amalgamation target unless the
   psyche explicitly chooses the lean daemon as the shorter cutover.
2. Start an improved Horizon branch on the current schema-next
   substrate rather than backfilling old parser support into stale lean
   data.
3. Migrate production `goldragon/datom.nota` forward, not lean
   `goldragon/datom.nota`.
4. Create a production-fix carry-forward matrix from report 162 into
   schema-deep Lojix, schema Horizon, CriomOS, CriomOS-home, and
   CriomOS-lib.
5. Promote source staging and builder capability preflight to first
   class daemon actors.
6. Build shadow-projection tests before attempting live activation.
7. Keep `lojix-cli` available until the daemon has real sandbox and
   production-node build witnesses.

## Open Questions For Psyche

1. Should `schema-deep` become the explicit production replacement
   target for Lojix, with `horizon-leaner-shape` treated as a staging
   and learning branch?
2. Should improved Horizon be a deep branch of `horizon-rs`, or is the
   break large enough to create a parallel `horizon-next` style repo
   and later rename after stabilization?
3. For Balboa and future aarch64 nodes, should Prometheus gain emulated
   build support, should a real aarch64 builder be added, or should
   aarch64 deploys be explicitly deferred?
4. Until Arca exists, should source staging use SSH store import,
   an ad-hoc Git source mirror, or a temporary daemon-managed cache?
5. Should generated schema Rust be committed under `src/schema/` for
   Horizon and Lojix during this migration, matching the current
   schema-stack direction?

## Bottom Line

The production stack should remain in place while the replacement is
made real. The replacement should be better than the current lean
branch: schema-authored Horizon, schema-deep Lojix, daemon-owned
deployment state, actorized effect planes, and Nix-backed witnesses
that compare old and new projections before live activation.

The most important next decision is whether to bless `schema-deep` as
the production replacement target. If yes, the next implementation
work is a carry-forward/amalgamation plan, not more patching of stale
lean proposal data.
