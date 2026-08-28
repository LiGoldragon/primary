# Rust-side archaeology: how each shape came to be

Six shapes found by the structural map, traced to their origin commits,
dates, and the psyche's recorded words.

All "current" line counts and variant counts cite `origin/main` of each
repository (lojix `33b8b6b7`, horizon-rs `c70915eb`, goldragon
`5bc563bf`). Local working copies differ; history was read via
`jj log` on the colocated jj repos.

---

## 1. Lojix's growth to ~21,000 lines of Rust

### Line-count timeline

| Date | Commit | Rust lines | Event |
|---|---|---|---|
| 2026-05-13 | `67fd454` | 0 | Skeleton: docs only |
| 2026-06-05 | `5c0ee76` | ~6,224 | Initial import from untracked `~/wt` triad-port. Co-Authored-By: Claude Opus 4.8 |
| 2026-06-12 | `1375bd9` | 6,524 | Flatten crate; split CLI into lojix + meta-lojix |
| 2026-06-15 | `bef1fd1` | 9,247 | Horizon materialization, deploy transport, Test-op |
| 2026-06-19 | `fc9707b` | 12,079 | Pipeline growth |
| 2026-07-04 | `c9344e1` | 13,425 | Schema regeneration (positional form) |
| 2026-07-16 | `bd7a05a` | 15,223 | Steady growth |
| 2026-07-28 | `9adc6c7` | ~16,700 | Schema-one store migration |
| 2026-08-04 | `cf20fb1` | 24,204 | "Make deploy transitions durable and private" +11,542/-4,759 |
| 2026-08-06 | `fda1a21` | ~20,800 | Replace generated schema with handwritten runtime. -5,791 net |
| 2026-08-23 | `782805b` | 21,277 | |
| 2026-08-28 | `33b8b6b` | 21,255 | origin/main tip: "Pin Horizon 0.4.0 node-service removal" |

### Feature introduction

| Feature | Date | Commit |
|---|---|---|
| Nexus with ordinary/owner sockets | 2026-06-05 | `5c0ee76` — present from initial import |
| signal-lojix + meta-signal-lojix deps | 2026-06-05 | `5c0ee76` |
| triad-runtime dep | 2026-06-05 | `5c0ee76` |
| CLI split (lojix / meta-lojix) | 2026-06-12 | `1375bd9` |
| sema-engine dep (redb .sema store) | 2026-06-13 | `196ab50` — "durable sema-engine state plane + self-resume" |
| Append-only event log | 2026-06-05 | `5c0ee76` — mentioned in docs from skeleton; implemented in import |
| schema_runtime.rs | 2026-06-05 | `5c0ee76` — 1,400 lines at import; 8,127 lines at origin/main (`33b8b6b`) |
| Schema version tracking | 2026-07-05 | `ad9e273` — "add read-only store inspection" |
| Schema v4 + migration | 2026-07-28 | `9adc6c7` / 2026-08-04 `cf20fb1` |

### Psyche evidence

No surviving psyche transcript from the entire June 2026 development
period. The foundational architecture — the two-socket Nexus, sema
store, event log, signal contracts, triad-runtime — was laid down by
agents (co-authored with Claude Opus 4.8) without recorded psyche
interaction.

The psyche's earliest recorded Lojix utterance is from 2026-07-28:

> So apparently the previous agent had trouble. We want to deploy a
> fix on another host in our cluster, and he's saying our deployment
> tool Logix needs to be fixed.

— psyche, spoken, 2026-07-28, Codex session `019fa89b`.
psycheStackOrigins.md. STT: "Logix" = lojix.

The psyche treats Lojix as "our deployment tool" and directed its
placement (OS-only), its CLI interface (lojix and meta-lojix only,
typed input only), and its operational rules (no hardwired hostnames,
no setup-specific scripts). But the internal architecture — the
two-socket Nexus with signal contracts, the redb sema store with
schema versioning, the append-only event log, the triad-runtime
dependency, the schema_runtime.rs engine — traces to agent decisions
during June 2026.

The largest single commit (`cf20fb1`, 2026-08-04, +11,542/-4,759) has
no Co-Authored-By and no corresponding psyche session found.
*Inference:* this was an autonomous agent rewrite.

---

## 2. Lojix's duplicated types (runtime_flow.rs vs runtime_model.rs)

### What happened

Both files were introduced in the **same commit**:

- **Commit:** `fda1a219`
- **Date:** 2026-08-06
- **Message:** "lojix: replace generated schema ownership with handwritten runtime"

This commit deleted 6,225 lines of generated schema code
(`schema/nexus.rs`: 1,779 lines; `schema/sema.rs`: 4,446 lines) and
the code-generation pipeline (`build.rs`, `schema/*.schema`), replacing
them with 1,484 lines of handwritten runtime across two files:

- `runtime_model.rs` (940 lines): durable nouns — derives `rkyv::Archive, rkyv::Serialize, rkyv::Deserialize`
- `runtime_flow.rs` (544 lines): transient flow types — derives `Clone, Debug, PartialEq, Eq` only (no rkyv)

The duplicated types — `DeploymentTransport`, `DeploymentInputMode`,
`ActivationBackend`, `ExtraSubstituter`, `TestExecutionProfile`,
`Input`/`Output` — appear in both because they need different
serialization characteristics in the durable vs transient planes.
`runtime_flow.rs` imports many types *from* `runtime_model.rs`; the
duplication is limited to types that genuinely differ in derives.

### Prior state

Before this commit, all types lived in a single generated file
`schema/nexus.rs` (1,779 lines) where `DeploymentTransport` was
defined once with both `rkyv` and `dotos` derives. No plane
distinction existed.

### Psyche evidence

**None.** All Codex sessions on 2026-08-06 contain zero user (psyche)
messages — they were autonomous agent sessions. No psyche message on
surrounding dates (Aug 4-8) mentions "generated," "handwritten,"
"runtime_flow," "runtime_model," or "schema replacement."

*Inference:* this was an agent's architectural decision to replace a
generated-code pipeline with handwritten Rust. The agent split the
types by serialization concern (durable vs transient), duplicating
definitions that needed different derive macros. The psyche never asked
for or commented on this split. The decision is consistent with the
psyche's general discomfort with generated schema infrastructure (the
"three stacks" frame identifies an "incorrect new stack" involving
agent-created schema machinery), but no explicit directive produced
this particular file split.

---

## 3. Horizon-rs: JSON projection, NodeSpecies, NodeService

### JSON projection with ~60 node fields

The `Node` struct with 54 `pub` fields appeared in the first runnable
scaffold commit `0b38626` on **2026-04-23**, authored by `li`. The
commit introduced the complete typed schema: input `ClusterProposal`
types, output `Horizon`/`Node`/`User`/`Cluster`, projection via
`ClusterProposal::project`, and viewpoint scoping via
`Node::fill_viewpoint`.

The DESIGN.md was written the same day in three commits:
- `f6bb6a5`: initial design — "agreed style is in place; design needs alignment with user before any code lands"
- `1bd58ad`: "user reviewed and answered the open questions; design now ready for code"
- `158ae92`: rewrote derived-field placement — "per user directive"

The Node struct grew from 54 to **64 fields** by commit `c70915e`
(2026-08-28, origin/main).

### Viewpoint scoping

Appeared in the scaffold commit `0b38626` (2026-04-23), via
`Node::fill_viewpoint`. The concept was described in DESIGN.md the same
day. No verbatim psyche quote about viewpoint scoping specifically
survives. The `--cluster --node` CLI shape was agent-designed.

### NodeSpecies growth

| Date | Commit | Count | Change |
|---|---|---|---|
| 2026-04-23 | `0b38626` | 9 | Center, LargeAi, LargeAiRouter, Hybrid, Edge, EdgeTesting, MediaBroadcast, Router, RouterTesting — ported from `speciesModule.nix` |
| 2026-06-13 | `59862dd` | 10 | + TestVm |
| 2026-06-20 | `a94e2b9` | 11 | + CloudNode |

The original 9 species were a mechanical port of the archive CriomOS
categories, which were the living's design. TestVm and CloudNode were
agent-proposed.

### NodeService growth

| Date | Commit | Count | Variants added |
|---|---|---|---|
| 2026-05-12 | `31d3fed` | 2 | TailnetClient, TailnetController — "replace tailnet booleans with NodeServices" |
| 2026-05-17 | `036b175` | 3 | + PersonaDevelopment |
| 2026-05-19 | `ab0fbb8` | 5 | + NixBuilder, NixCache |
| 2026-06-15 | `44415db` | 6 | + VmHost |
| 2026-06-20 | `4a0e29f` | 7 | + WebHost |
| 2026-07-23 | `3311d56` | 8 | + AgentIntercomLocal |
| 2026-07-27 | `7aa83fa` | 9 | + AgentIntercomGraphical |
| 2026-08-28 | `c70915e` | 7 | **removed** AgentIntercomLocal, AgentIntercomGraphical |

The structural map's count of 9 matched the state between 2026-07-27
and 2026-08-28. At origin/main (`c70915e`, 2026-08-28), NodeService has
**7 variants** (AgentIntercomLocal and AgentIntercomGraphical removed)
and NodeSpecies has **11 variants**.

### What the psyche said Horizon IS

> Horizon and the cluster-data it carries should be elegant and minimal:
> express only **what** the psyche (as cluster user) wants the cluster to
> do, never **how** and never decision-making.

— psyche, 2026-06-04 Designer session. Spirit record
`7ggswqdxqqz97za6o7w`. psycheHorizon.md.

> Horizon is a hack for now, and that's fine. Logix is the more
> traditional component.

— psyche, 2026-06-04 Designer session. Spirit record
`1bok2bxvu3beswif9mv`. psycheHorizon.md.

On AgentIntercomGraphical removal:

> this agentintercomgraphical is slop.

— psyche, typed, 2026-08-28.
`flows/01a04881/vision/agentIntercomGraphical.md`.

> AgentIntercomGraphical is a total misnomer and is now involved in a
> bunch of things it has nothing to do with

— psyche, typed, 2026-08-28. Session `01a048a6`, line 64.
`flows/01a048a6/vision/agentIntercomGraphical.md`.

*Inference:* The ~60-field Node shape was agent-written but
psyche-reviewed on its founding day (DESIGN.md records "user
reviewed"). The NodeService pattern (replacing booleans with
data-carrying variants) was agent-proposed but consistent with the
psyche's "variants over booleans" and "typed end-to-end" principles.
The specific NixBuilder, NixCache, PersonaDevelopment, VmHost, WebHost
additions were agent proposals. AgentIntercomLocal/Graphical were
agent-proposed and psyche-rejected.

---

## 4. The split between goldragon and criomos-horizon-config

### goldragon

- **Created:** 2022-09-20 by the living (`li`), commit `7da4ce47`, `(init)`.
  Originally experimental; reseeded 2026-04-23 (commit `87d19826`) as
  "the source of truth for the LiGoldragon kriom."
- Converted from `datom.nix` to `datom.nota` (NOTA) on 2026-04-23,
  then to DOTOS format on 2026-07-31.

### criomos-horizon-config

- **Created:** 2026-05-17, commit `1218566e`, "criomos-horizon-config:
  add pan-horizon configuration." Author: `li`.
- Per `active-repositories.md`: "pan-horizon constants **previously
  inlined in goldragon/datom.dotos** (operator/suffixes/LAN
  pool/reserved labels)." Introduced on the `horizon-leaner-shape`
  branch.
- Its ARCHITECTURE states: "This repository exists so pan-horizon
  identity and temporary network facts live in their own repo rather
  than being smuggled onto the cluster-authoring surface."
- 11 total commits through 2026-08-12.
- Per `active-repositories.md`: "horizon-rs main does **not** yet read
  [criomos-horizon-config] — constants remain inline in
  `goldragon/datam.dotos`." The extraction was created but the consumer
  never switched.

### Psyche evidence

**No psyche transcript mentions "horizon-config" or "pan-horizon" in
any user/typed message** — not in Codex sessions, not in Claude
sessions. No Codex sessions exist for 2026-05-17 or adjacent dates.

*Inference:* criomos-horizon-config was an agent initiative, created on
the `horizon-leaner-shape` feature branch as part of the daemon rewrite
arc. The architectural rationale — separating horizon-wide from
per-cluster constants — is consistent with the psyche's principles
("every concept should have its repo"), but the specific extraction was
never discussed with the psyche. The fact that horizon-rs main still
does not consume it, and constants remain duplicated in goldragon,
further suggests an agent proposal that was never fully landed or
reviewed by the psyche.

---

## 5. core-schema being a byte-identical copy of core-ethos

### What happened

**core-schema** and **core-ethos** share the exact same commit history
from `33e5be2` (2026-07-15, "core-schema 0.1.0: first real stringless
Core layer + TextualSchema") through `6067b52` (2026-07-27, "core-schema:
make textual reflection lookup-only"). That is 48 commits — the entire
core-schema history.

On **2026-07-28**, commit `42fbbc08` in the core-ethos repo renamed the
crate from `core-schema` to `core-ethos`: types, tests, docs. Commit
message: "Rename the crate [...] without changing encoded layouts or
runtime mechanics." core-schema received no further commits — it is
frozen at the pre-rename state.

### The compat pin in ethos-engine

On **2026-07-29**, commit `ed12804` renamed `schema-engine` to
`ethos-engine` (0.1.0 to 0.2.0). The agent introduced a compat
dependency:

```toml
central-storage-core-schema = {package="core-schema", git="...core-schema.git", rev="d3cdee9..."}
central-storage-name-table  = {package="name-table",   git="...name-table.git",  rev="c3237f77..."}
```

Comment: "The currently wired central-storage contract archives this
exact pre-Ethos package and name-table layout. Keep the compatibility
types isolated to the legacy storage adapter until that separately
designed topology is dissolved."

### Who still needs core-schema?

1. **ethos-engine** — compat dep, explicitly labeled legacy, pending dissolution.
2. **signal-sema-storage** (checkout `31ab486`) — still pins `core-schema` at `d3cdee9`.
3. **core-logos** and **core-nomos** — older checkouts pin core-schema; newer checkouts have migrated to core-ethos.

*Inference:* The compat pin is an agent decision to preserve wire-level
compatibility with the pre-rename central-storage contract, not a
psyche directive. The psyche's spirit principle — "backward
compatibility is never a design variable" — suggests the compat pin is
a candidate for dissolution once the central-storage topology is
redesigned.

### Psyche evidence

No psyche quote was found specifically directing the core-schema to
core-ethos rename. The psyche's framing of Schema to Ethos as a
terminology boundary:

> schema is the old syntax. And datum [Datom] is the new syntax and
> ethos is the new syntax.

— psyche, 2026-08-10, spoken (Designer session 13cfc23f).
`psyche-raw/Vision/archive-threeStacks.md`.

> It would also be great if we can use ethos instead of schema but
> ethos-monolith might not be ready to use.

— psyche, 2026-08-22T21:43Z, typed.
`flows/01a02a34/vision/archive-ethos.md`, line 288.

| Event | Date | Commit |
|---|---|---|
| core-schema repo created | 2026-07-15 | `33e5be2` |
| core-schema frozen (last commit) | 2026-07-27 | `6067b52` |
| core-ethos rename commit | 2026-07-28 | `42fbbc08` |
| ethos-engine compat pin introduced | 2026-07-29 | `ed12804` |
| Psyche "schema is old, ethos is new" | 2026-08-10 | spoken |

---

## 6. The content-addressed flake emission pipeline

### Pipeline stage introduction

All commits authored as `li <li@goldragon.criome.net>`.

| Date | Commit | Event |
|---|---|---|
| 2026-05-27 | `b9097c13` | All five stages first appear in `schema-deep` branch: activator.rs, builder.rs, copier.rs, dispatcher.rs, gc_root.rs, engine.rs |
| 2026-06-05 | `5c0ee76f` | Imported to main. Co-Authored-By: Claude Opus 4.8. "import schema-derived triad-port daemon crate (new-stack rewrite, M1 build+evaluate)" |
| 2026-06-10 | `7d66d2ec` | MaterializeHorizon: "materialize horizon inputs for production eval" |
| 2026-06-13 | `cbe3c06b` | CopyClosure + ActivateGeneration construction. Co-Authored-By: Claude Opus 4.8 |
| 2026-08-04 | `cf20fb1e` | Durable pipeline transitions: "make deploy transitions durable and private" |
| 2026-08-06 | `fda1a219` | All stages rewritten: "replace generated schema ownership with handwritten runtime" |

### Deployment selection fields

All four appeared together on **2026-08-04** in commit `b1a6fb20`
("make deployment routing request-owned in v4"):
DeploymentTransport, DeploymentInputMode, ActivationBackend,
DeploymentOutputSelector.

### manifests/*.dotos status

The `/home/li/primary/manifests/` directory exists but is **empty**.
Flow 01a048a6 log: "No authoritative `manifests/*.dotos` selection
supplies the required explicit store/SSH transport, builder, selector,
and input mode for Ouranos and Zeus." Deployment is blocked on this.

### Psyche evidence

No surviving psyche transcript from the pipeline founding period
(May 27 through June 13 2026). The June 4-6 pre-reset design audit
reports cite `intent/deploy.nota` (legacy substrate):

> "Three deploy variables: where the build happens, where the Nix cache
> is, and where the target is"

— psyche intent, captured in `intent/deploy.nota:1-13` and reported in
the 2026-06-04 design audit (`1-intent-agglomerated-subject.md:130-165`).

The psyche's bar for M1:

> "bring the whole stack online so that at least we can build things
> with it and evaluate."

— psyche, pre-June 2026, cited in M1 report (report 28, 2026-06-05).

Later reinforcements:

> make sure nothing no host names or anything like that is hardwired
> into lojix

— psyche, typed, 2026-08-01. Session `019fbf4a`, line 3801.

> CLIs cannot accept any other type of argument than the typed input
> object. I feel like I keep repeating myself.

— psyche, typed, 2026-08-14.
`psyche-raw/Vision/setupIndependentInterfaces.md`, lines 14-16.

> Seems like letting agents "fix" it ended up abandoning my vision.
> The interface is lojix and meta-lojix CLI only.

— psyche, typed, 2026-08-14.
`psyche-raw/Vision/setupIndependentInterfaces.md`, lines 8-9.

*Inference:* The five-stage pipeline (MaterializeHorizon, NixEval,
NixBuild, CopyClosure, ActivateGeneration) is an agent's engineering of
the psyche's "three deploy variables" intent into a concrete state
machine. The stage names and the state-machine shape are agent
decisions; the psyche specified the domain model (what variables, what
triad architecture, what Lojix is) but not the internal pipeline
stages. The deployment selection fields (DeploymentTransport,
DeploymentInputMode, DeploymentOutputSelector, ActivationBackend)
formalize what was originally "three deploy variables" into a richer
typed vocabulary — an agent expansion the psyche has not reviewed.

No psyche quote on the shape of `manifests/*.dotos` deployment
selection was found.

---

## Sources

### Repositories examined

- `lojix`: `/home/li/wt/github.com/LiGoldragon/lojix` — full git history
- `horizon-rs`: `/home/li/wt/github.com/LiGoldragon/horizon-rs` — full git history
- `goldragon`: `/home/li/wt/github.com/LiGoldragon/goldragon` — full git history
- `core-schema`: `/home/li/.cargo/git/db/core-schema-013bdd6a13064374` (bare)
- `core-ethos`: `/home/li/.cargo/git/db/core-ethos-dc285e9aa5f2c51c` (bare)
- `ethos-engine`: `/home/li/.cargo/git/db/ethos-engine-d6c0846b7d3a62af` (bare); checkout at `/home/li/.cargo/git/checkouts/ethos-engine-d6c0846b7d3a62af/ed12804`
- `criomos-horizon-config`: commit history from GitHub API via `active-repositories.md`

### Psyche records consulted

- `flows/674a4dab/reports/psycheHorizon.md`
- `flows/674a4dab/reports/psycheLojix.md`
- `flows/674a4dab/reports/psycheStackOrigins.md`
- `psyche-raw/Vision/setupIndependentInterfaces.md`
- `psyche-raw/Vision/lojixOwnership.md`
- `psyche-raw/Vision/everythingIsInTheDaemon.md`
- `psyche-raw/Vision/archive-threeStacks.md`
- `flows/01a04881/vision/agentIntercomGraphical.md`
- `flows/01a048a6/vision/agentIntercomGraphical.md`
- `flows/01a02a34/vision/archive-ethos.md`

### Codex transcript sessions searched

- `~/.codex/sessions/2026/07/28/` (session `019fa89b`)
- `~/.codex/sessions/2026/08/01/` (session `019fbf4a`)
- `~/.codex/sessions/2026/08/04/` through `2026/08/08/` — autonomous, zero user messages
- `~/.codex/sessions/2026/08/28/` (sessions `01a04881`, `01a048a6`)

### Pre-reset corpus

- `reports/PreResetCorpus-2026-06-07/reports/cloud-designer/23-horizon-lojix-rewrite-audit-2026-06-04/`
- `protocols/active-repositories.md`
