# B3 — CriomOS consumption + cutover and parity

Cloud-designer lane, sub-agent B3 of the Horizon/Logix rewrite audit. 2026-06-04.
Read-only on all repos. The goal this whole session serves: finish the rewrite to
cutover and **retire the dual production-and-next deploy stacks** (intent
`75auhtr308tgt4kaa9a`, High). This file is the consumption + cutover/parity leg.

The path under audit is `authored NOTA facts → horizon-rs projection → CriomOS
flake inputs → running NixOS`, as documented in
`reports/system-designer/70-cluster-data-feature-horizon-criomos-2026-06-04.md`.
B3 answers: what consumes the projection, where Stack A and Stack B diverge, the
VmTesting typed-source gap, the full parity gap, and a low-regret cutover sequence.

Note on the brief: the system-operator smoke-build report `134*` does **not**
exist (the nearest, `139-arca-daemon-...`, is unrelated). The closest live
smoke-build status is the lojix README on the `horizon-leaner-shape` branch
(quoted in §5) plus the active-repositories Truth Pins.

## 1. What consumes the Horizon projection today, and how

The consumer is **CriomOS**, identically across both stacks at the Nix surface.
The deployer (lojix-cli in A, lojix-daemon in B) is **not** a CriomOS flake input;
it is the external process that produces a per-node `horizon` flake input and pins
it into a `nix build` via `--override-input`. CriomOS only sees the projected JSON.

### 1a. The horizon flake input

CriomOS declares four content-addressed override axes — `system`, `pkgs`,
`horizon`, `deployment` (plus `secrets`) — each a stub path-flake by default
(`CriomOS/flake.nix:48`,`61`,`65`,`69`). The `horizon` stub is
`path:./stubs/no-horizon`; the deployer overrides it per deploy. The deployer
materializes a tiny generated flake whose only output reads the projected JSON:

```nix
{ outputs = _: { horizon = builtins.fromJSON (builtins.readFile ./horizon.json); }; }
```

(`lojix-cli/src/artifact.rs:11`). That generated dir is hashed
(`nix hash path --type sha256 --sri`, `artifact.rs:218`) and passed as
`--override-input horizon <flakeref>` to the `nix build` of
`<criomos>#nixosConfigurations.target.config.system.build.toplevel`
(`lojix-cli/src/build.rs:181`,`307`-`315`). Same axis layout in the leaner
CriomOS flake (`CriomOS/horizon-leaner-shape/flake.nix:43`,`56`,`60`,`64`).

### 1b. specialArgs.horizon

The flake reads `horizon = inputs.horizon.horizon` (`CriomOS/flake.nix:77`) and
threads it through `nixosSystem`'s `specialArgs` (`flake.nix:115`-`124`):

```nix
specialArgs = { inherit horizon system deployment inputs constants criomos-lib; };
```

So every module takes `{ horizon, ... }` and reads `horizon.node`,
`horizon.cluster`, `horizon.exNodes`, `horizon.users` (camelCase — serde renames
the Rust fields). The leaner flake is identical (`horizon-leaner-shape/flake.nix:73`,`111`-`119`).

### 1c. node-services.nix — has / payload

The service-role resolver `modules/nixos/node-services.nix` is **byte-identical**
between Stack A (`CriomOS/modules/nixos/node-services.nix`) and Stack B
(`CriomOS/horizon-leaner-shape/modules/nixos/node-services.nix`). It treats each
entry as a bare string (`TailnetClient`) or single-key attrset
(`{ VmTesting = {payload}; }`) and exposes:

- `has services name` — `builtins.any` over the list (`node-services.nix:38`)
- `payload services name` — the attrset under the matching key, else `{ }` (`:40`)
- `personaDevelopmentHas` — nested-capability lookup (`:47`)

This is the load-bearing consumption seam: every CriomOS module gates on
`nodeServices.has (node.services or [ ]) "<Role>"` and pulls per-node config via
`payload`. It is string-keyed at the Nix layer **by construction** — the typed
NodeService projects to camelCase JSON, and Nix matches the variant tag as a
string. That is fine for the consumer; the typing discipline lives upstream
(see §3).

## 2. The precise Stack A vs Stack B divergence

The two stacks share the CriomOS consumption surface (§1c identical) but diverge
sharply at the model, the projection signature, the authored-fact schema, and the
deployer. Per `protocols/active-repositories.md:138`-`164`: schemas have diverged;
do not fold piecemeal.

### 2a. project() signature — the central divergence

- **Stack A**: `ClusterProposal::project(&self, viewpoint: &Viewpoint)`
  (`horizon-rs/lib/src/horizon.rs:33`). One input: the viewpoint. Pan-horizon
  facts (domain suffixes, transitional LAN) are inlined or absent.
- **Stack B**: `ClusterProposal::project(&self, horizon: &HorizonProposal,
  viewpoint: &Viewpoint)`
  (`horizon-rs/horizon-leaner-shape/lib/src/proposal/cluster.rs:76`). **Two**
  inputs: cluster facts AND the pan-horizon `HorizonProposal`. The lojix daemon
  loads both and calls the two-arg form
  (`lojix/horizon-leaner-shape/src/deploy.rs:1077`-`1083`).

Any consumer/caller of `project` must change at cutover; this is not a follow-style
swap.

### 2b. Authored-fact schema (goldragon/datom.nota)

The two datom files are different NOTA schemas, not just different wrappers:

- **Stack A** (`goldragon/datom.nota:5`): a bare 4-tuple `({nodes} {users} {}
  trust)` with anonymous curly maps, `(Metal (Some X86_64) ...)`, `(NixBuilder
  (Some 6))`, curly `{ [/] (...) }` filesystem maps. Services as
  `[(TailnetClient) (NixBuilder (Some 6)) (NixCache)]` (`datom.nota:96`).
- **Stack B** (`goldragon/horizon-leaner-shape/datom.nota`): a named head record
  `(ClusterProposal [ (Entry balboa (NodeProposal ...)) ] ...)` with `(Entry k v)`
  map entries, flattened `(Machine Arm64 4 Rock64 None None None)`,
  `(NixBuilder 6)` (no `Some`), `(Io Qwerty ...)`, `(Disk ...)`. Services as
  `(NixBuilder 6)` bare (`horizon-leaner-shape/datom.nota:122`-`124`).

The Stack B datom still carries legacy quoted strings (`"/"`,
`"/dev/disk/by-label/..."`) — a NOTA migration-form artifact, not bracket-clean,
and a small cleanup the cutover should sweep (AGENTS hard override: strings come
exclusively from bracket forms).

### 2c. NodeService enum — same variants, different derive

Both enums carry exactly five variants — TailnetClient, TailnetController,
NixBuilder, NixCache, PersonaDevelopment — with the identical doc-comment
role-not-implementation discipline:

- **Stack A** (`horizon-rs/lib/src/proposal.rs:98`): hand-written `NotaEncode` /
  `NotaDecode` impls (`proposal.rs:183`+), `NotaRecord` derive on the structs.
- **Stack B** (`horizon-rs/horizon-leaner-shape/lib/src/proposal/services.rs:23`):
  `#[derive(... NotaSum)]` — the schema-component derive that auto-emits the codec.
  The model is also restructured into a `proposal/` + `view/` split, and the
  output `Node` lives in `view::Node` (`view/node.rs:25`).

Neither enum has VmTesting (§3).

### 2d. lojix-cli monolith vs lojix daemon

- **Stack A — lojix-cli** (`lojix-cli/src/main.rs`): a one-shot CLI. It already
  takes a single NOTA argument (`request.rs:248` `decode_request`, inline
  `(FullOs ...)` or a NOTA file or `$LOJIX_CONFIG` / XDG path) — so it is
  single-argument-rule compliant. But it does project + materialize + stage +
  build + activate **in one process** (`project.rs`, `artifact.rs`, `build.rs`,
  `stage.rs`, `activate.rs`, `copy.rs`). No daemon, no live ledger, no GC-root
  ownership, no observation stream. CriomOS / CriomOS-home flake locks pin it at
  `4c66b8a6fa55` (`active-repositories.md:149`).
- **Stack B — lojix** (`lojix/horizon-leaner-shape/README.md`): one crate, two
  binaries. `lojix-daemon` is the long-lived orchestrator binding
  `/run/lojix/daemon.sock`, owning the live generation ledger, GC-roots tree,
  deployment ledger (in `sema-engine`), and container-lifecycle observation,
  receiving `signal-core` frames carrying typed `signal-lojix` deploy requests
  (`Cargo.toml:25`,`29`; `socket.rs:9`,`280`; `deploy.rs:50`). `lojix` is the thin
  NOTA CLI client (reads one NOTA request → daemon frame → one NOTA reply). It runs
  on the OLD signal stack (`signal-core` + `signal-lojix` + `sema-engine` +
  `kameo`), NOT yet the new schema-derived triad — that port is B2's subject.

### 2e. criomos-horizon-config split

Stack B factors the pan-horizon facts (horizon identity + transitional IPv4 LAN)
out of goldragon into their own one-record repo
(`criomos-horizon-config/horizon.nota` → `horizon-rs::HorizonProposal`;
`ARCHITECTURE.md:1`-`17`). Stack A has no such repo. Note: there is **no**
`horizon-leaner-shape` worktree for criomos-horizon-config under `~/wt` — only the
canonical `/git` checkout — so its branch posture relative to the worktree set is
worth confirming before cutover.

## 3. The VmTesting typed-source gap (correction 431pfi7l1akuu22b01b)

Correction `431pfi7l1akuu22b01b` (High) is blunt: the VmTesting work was garbage —
it matched a string `VmTesting` via `node-services` has/payload with a defensive
`node.services or [ ]` default, fed by a **synthetic horizon fixture**, instead of
adding VmTesting as a real typed `NodeService` variant, authoring it in
`goldragon/datom.nota`, projecting it typed, and consuming the typed value. The
correct order is **typed-source-first**: extend the model → author the fact →
project typed → consume typed.

Confirmed by source. VmTesting is:

- **NOT** a `NodeService` variant in Stack A (`grep VmTesting horizon-rs/` empty)
- **NOT** a `NodeService` variant in Stack B (`grep VmTesting
  horizon-rs/horizon-leaner-shape/` empty)
- **NOT** in either goldragon datom (`grep VmTesting` empty in both)
- Resolved purely through the string-keyed `node-services.nix`, validated by a
  synthetic fixture in the eval check
  (`CriomOS/next/checks/vm-testing-prometheus-policy/default.nix:80`, per report 70 §4)

So the VmTesting consumption end exists (on CriomOS `next`, which is Stack-A-shaped
per report 70 §5), but the typed source and authored fact are missing on BOTH
stacks. **What closes it** (do it in Stack B per the rewrite priority):

1. Add `VmTesting { gpu_passthrough: bool, display: Display, gpu: Option<PciIds> }`
   to `proposal/services.rs::NodeService`, with the `NotaSum` derive (Stack B
   auto-emits the codec; no hand-rolled encode/decode). Add the matching
   `NodeServiceKind::VmTesting`.
2. Author the fact in `goldragon/horizon-leaner-shape/datom.nota` on the
   large-ai-router node (`(VmTesting False Spice None)` positional).
3. Project typed — the `view::Node.services` vector already carries
   `Vec<NodeService>` (`view/node.rs:48`), so the typed value flows through with
   no projection change. (Per the new minimal-Horizon intent
   `7ggswqdxqqz97za6o7w`, Horizon must NOT derive a `gpuPassthrough` boolean or
   a VFIO decision — it carries the typed fact; Nix composes the decision.)
4. Consume typed — the existing `vm-testing/default.nix` already reads
   `has`/`payload` and treats the variant tag as a string; the typed projection
   now FEEDS that resolver with real data, retiring the fixture.

Note the naming correction `1n6ew7o2lx9coz3wfqg` (High): the role is large-ai-node
(NodeService taxonomy), not the host prometheus. Author VmTesting against the role
on whichever node fills it (prometheus today).

## 4. The parity gap — what must be true before lojix-cli can retire

Everything below must hold before CriomOS can be deployed by the lojix daemon's
projection and lojix-cli can be deleted.

### 4a. Functional parity (deployer)

The lojix daemon must reproduce every lojix-cli capability the cluster relies on:

- **Operation set.** lojix-cli handles `FullOs`, `OsOnly`, `HomeOnly`, and
  `CheckHostKeyMaterial` (`lojix-cli/src/request.rs:48`). The daemon currently
  documents an **active build-only** path (project → nix build → pin GC roots →
  record generation → `GenerationQuery`) plus deployment-observation streams
  (`lojix/.../README.md`, `deploy.rs:1076`-`1122`). Confirm the daemon covers all
  four operations, including the home-only path (`validate_home_user`,
  `deploy.rs:1084`) and the host-key-material check.
- **System actions.** lojix-cli supports Eval / Build / Boot / Switch / Test /
  **BootOnce** (`build.rs:9`-`23`) — BootOnce is the headless one-shot-default
  safety action that lands a new generation then auto-reverts on the second boot.
  Confirm the daemon's `BuildOnlyPlan` and activation path carry BootOnce; losing
  it is a production-safety regression for headless nodes (prometheus, balboa).
- **Builder selection + substituters.** lojix-cli resolves builder
  (dispatcher/named) and extra-substituter URLs from horizon nodes
  (`build.rs:284`+). Daemon has `BuilderPolicy` + `ExtraSubstituters::from_horizon_nodes`
  (`deploy.rs:1085`-`1087`) — but the daemon **disables local builds**
  (`deploy.rs:1004`: local builds rejected). Confirm that matches the production
  deploy habit (does anyone build locally on the dispatcher today?).
- **Secrets axis.** lojix-cli copies the three sops files
  (router-wifi-sae-passwords, router-backup-wifi-password, local-llm-api-token)
  into a generated secrets flake (`artifact.rs:18`-`30`,`155`). Confirm the daemon
  materializes the identical secrets axis — a missing secret breaks the router
  WiFi and the local LLM token on prometheus.

### 4b. Schema/model parity (horizon-rs view)

- The Stack B `view::Node` output must produce every field CriomOS modules read.
  It carries the derived booleans (`is_remote_nix_builder`, `is_dispatcher`,
  `is_large_edge`, `enable_network_manager`, `chip_is_intel`, ...) and grouped
  sub-records (`nix_cache: Option<NixCache>`, `yggdrasil`) — see
  `view/node.rs:78`-`94`. A field-by-field consumption audit of CriomOS +
  CriomOS-home against `view::Node` is required: any field a module reads that the
  leaner view renamed/dropped/regrouped breaks the build. (The leaner view already
  retired `is_nix_cache`/`nix_cache_domain`/`nix_url` into `nix_cache`, and
  `build_cores` into `max_jobs` — every consumer of those must be updated.)
- The new minimal-Horizon intent (`7ggswqdxqqz97za6o7w`, `10v4744869xt5spwnam`)
  wants these derived booleans **pushed down into Nix composition** and in/out type
  reuse. That is B1's redesign. **Cutover does not require it** — parity is the
  bar for retiring the dual stack; the minimal-Horizon collapse can land before OR
  after cutover. Flagging so cutover is not blocked on the larger redesign.

### 4c. Authored-fact parity (goldragon datom)

Both datoms must describe the same five nodes with the same roles. Confirmed the
service vectors match in substance across stacks (ouranos: TailnetClient +
TailnetController + NixBuilder + PersonaDevelopment; prometheus: TailnetClient +
NixBuilder + NixCache). The leaner datom must be re-derived clean from the live
production datom at cutover (capture any production drift since the leaner branch
forked), VmTesting added per §3, and quoted strings converted to bracket forms.

### 4d. CriomOS flake-lock parity

- The leaner CriomOS flake.lock (`horizon-leaner-shape/flake.lock`) inputs the four
  axes from `path:./stubs/*` (same as production) and follows
  criomos-lib/criomos-home/horizon onto `horizon-leaner-shape` branches
  (`flake.lock:506`,`513`,`522`,`529`). Crucially it **still carries a
  `lojix-cli` lock node** at rev `1778671600` (`flake.lock:484`,`639`,`972`) —
  inherited transitively (it is NOT a horizon/system/deployment axis). Confirm
  that pin is dead weight (no CriomOS Nix code references it) and remove it as part
  of the leaner-branch cleanup; otherwise the retired lojix-cli stays fetched.
- CriomOS does not flake-input the deployer at all (correct) — so retiring
  lojix-cli is a deployer-process swap plus a flake-lock-node cleanup, not a CriomOS
  input migration.

### 4e. The end-to-end prototype bar (intent 3zue95xkt8gzui12cao, 5wo8xmt0qpl6u6t10md)

Before declaring parity, one full deploy must run through the lojix daemon against
the leaner CriomOS branch and produce a booted node (the existing intent
explicitly requires a working end-to-end prototype that uses the designed
components fully, not a fixture or a bypass). The lojix README says the build-only
path is active and targets the matching leaner branches — confirm a real
`Switch`/`BootOnce` deploy, not just `Build`.

## 5. The cutover sequence — ordered, low-regret, with breakage flags

prometheus is the live cluster router (large-ai-router role) — it serves the nix
cache, runs the WiFi/router interfaces, and routes the transitional IPv4 LAN. A
botched prometheus deploy can take down cluster networking for every other node.
This sequence keeps Stack A deployable until the last possible moment.

### Step 0 — Close the typed/authored gaps on Stack B (no production risk)

Add the VmTesting typed variant + authored fact (§3); re-derive the leaner
goldragon datom from current production + convert quoted strings to brackets (§4c);
remove the dead lojix-cli flake-lock node from the leaner CriomOS branch (§4d).
All on `horizon-leaner-shape`; production untouched. **Risk: none** (worktree only).

### Step 1 — Field-by-field consumption parity audit (no production risk)

Diff every `horizon.node.*` / `horizon.cluster.*` / `horizon.exNodes.*` field read
across CriomOS + CriomOS-home modules against Stack B `view::Node` / `Cluster` /
`User`. Fix the leaner CriomOS branch to read the renamed/regrouped fields
(`max_jobs`, `nix_cache`, `yggdrasil`, ...). **Risk: none** (worktree only); this is
the single most likely silent-breakage source at cutover, so do it thoroughly.

### Step 2 — Daemon functional-parity completion (no production risk)

Bring the lojix daemon to cover all four operations, all six system actions
(especially BootOnce), builder/substituter resolution, and the secrets axis (§4a).
Decide the local-builds-disabled question against production habit. **Risk: none**
(worktree only).

### Step 3 — Shadow eval against production facts (no production risk)

Run the lojix daemon to PROJECT + `Build` (not activate) the leaner CriomOS branch
for each node, using production cluster facts, and diff the resulting
`config.system.build.toplevel` store path / closure against what Stack A produces
for the same node. A matching (or explainably-different) closure is the parity
proof. Do an `Eval`-only run first (cheapest). **Risk: none** — Build/Eval never
activate (`build.rs:30` `activates()` excludes Build/Eval).

### Step 4 — Cut over ONE low-stakes node first (bounded risk)

`Switch` (or `BootOnce` for safety) ONE non-critical node — **zeus or tiger** (Edge
/ EdgeTesting, no cluster-critical role) — via the lojix daemon + leaner branches.
Verify boot, tailnet join, nix-builder role. **Risk: bounded** — a single
edge/testing node; BootOnce auto-reverts on second boot if the generation is bad.
Keep Stack A able to redeploy that node as rollback.

### Step 5 — Cut over the cache/builder nodes (moderate risk)

Next `BootOnce` the NixBuilder/NixCache nodes that are NOT the router — confirm the
cache stays served and remote builds still dispatch. **Risk: moderate** — losing
the cache slows every other deploy but does not break networking; losing a builder
loses parallel build capacity. Keep prometheus on Stack A as the fallback cache.

### Step 6 — Cut over prometheus LAST (highest risk)

`BootOnce` prometheus (large-ai-router) only after every other node is healthy on
Stack B. **Risk: HIGHEST** — prometheus carries the router interfaces, the
transitional IPv4 LAN (gateway 10.18.0.1, DHCP pool), the WiFi SAE/backup secrets,
and the cluster cache. A bad generation can drop LAN + WiFi + DNS for the whole
cluster. Mitigations: use BootOnce (auto-revert on reboot 2); have physical/serial
console access before the deploy; verify the secrets axis materialized the two WiFi
sops files (§4a); keep the Stack-A lojix-cli + production CriomOS lock available to
redeploy prometheus from a second machine.

### Step 7 — Retire Stack A (cleanup, after a soak)

After all nodes have run healthy on Stack B through at least one full reboot cycle
(BootOnce → permanent default), merge `horizon-leaner-shape` → `main` across the
six repos + the two new repos (lojix, criomos-horizon-config) as the coordinated
multi-repo merge (`active-repositories.md:160`), delete the `lojix-cli` repo's
deploy role, drop the dead flake-lock node, and remove the two-deploy-stacks
section from `active-repositories.md`. **Risk: low** (cleanup) provided the soak
held; the only regret is premature retirement before a real reboot proved the
permanent-default generation, so DO complete a reboot cycle per node first.

## Anchors

- Pipeline + VmTesting gap: `reports/system-designer/70-cluster-data-feature-horizon-criomos-2026-06-04.md`.
- Two-deploy-stack + cutover discipline: `protocols/active-repositories.md:138`-`170`.
- Stack A monolith: `lojix-cli/src/{request,project,artifact,build}.rs`.
- Stack B daemon: `lojix/horizon-leaner-shape/src/{deploy,socket,client}.rs` + `README.md`.
- project() divergence: `horizon-rs/lib/src/horizon.rs:33` vs
  `horizon-rs/horizon-leaner-shape/lib/src/proposal/cluster.rs:76`.
- Intent: `75auhtr308tgt4kaa9a` (cutover/retire), `431pfi7l1akuu22b01b` (typed-source-first),
  `7ggswqdxqqz97za6o7w` + `10v4744869xt5spwnam` (minimal Horizon, in/out reuse),
  `1bok2bxvu3beswif9mv` (Horizon hack-for-now, Logix gets the triad),
  `3zue95xkt8gzui12cao` + `5wo8xmt0qpl6u6t10md` (working end-to-end prototype bar),
  `1n6ew7o2lx9coz3wfqg` (name the role, not the host).
