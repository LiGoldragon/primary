# 110 — Cluster-trust runtime is persona-shaped

*Designer report. Resolves `primary-rab` (cluster-registry component
identity). Records the user's decision: cluster-trust runtime lives in
the persona ecosystem because **persona is the durable agent — our
answer to OpenClaw and Gas City**. Proposes concrete component identity
and updates `persona/ARCHITECTURE.md`.*

---

## 0 · TL;DR

The cluster-trust runtime — the long-lived component that consumes
ClaviFaber per-host publications, holds the cluster's trust state, and
pushes trust observations to host subscribers — is a persona-shaped
component. Not lojix-cli (deploy CLI), not goldragon (cluster proposal
data), not a new criome-* component (would orphan from the durable-agent
narrative).

**Concrete identity proposed**: a new long-lived persona component,
`persona-trust`, sibling to `persona-mind` / `persona-router`. Owns the
cluster-trust redb, the `ClusterRegistryActor` and `TrustDistributionActor`
named in `primary-e3c`, and a typed `signal-clavifaber` channel to each
host.

**Headline architectural commitment**: persona's `ARCHITECTURE.md` now
states explicitly — *"Persona is the durable agent. The Persona ecosystem
is our answer to OpenClaw and Gas City: an autonomous, persistent,
inspectable agent system instead of a state-machine reconciliation
stack."* That positioning is upstream of every component; it explains why
cluster-trust belongs here rather than in deploy or data repos.

---

## 1 · The question `primary-rab` asked

ClaviFaber writes a typed `PublicKeyPublication` record per host
(`/git/github.com/LiGoldragon/clavifaber/src/publication.rs:7-13`):

```rust
pub struct PublicKeyPublication {
    pub node_name: String,
    pub open_ssh_public_key: String,
    pub yggdrasil_address: Option<String>,
    pub yggdrasil_public_key: Option<String>,
    pub wifi_client_certificate_pem: Option<String>,
}
```

ClaviFaber's current `ARCHITECTURE.md` disclaims the cluster-DB writer:

> *"The cluster database writer belongs in the cluster-management/deployment
> layer that already owns the database revision and deployment transaction.
> In the current workspace shape, that means a Lojix/CriomOS cluster
> publisher or a dedicated successor component, not ClaviFaber. ClaviFaber's
> contract ends at a complete public PublicKeyPublication record."*

`primary-3m0` reverses that disclaimer: the cluster wave (`primary-e3c`)
needs `ClusterRegistryActor` + `TrustDistributionActor` as real long-lived
components. `primary-rab` asks: *which component owns the cluster-trust
runtime?*

Three options the bead enumerated:

- (a) New component: `criome-cluster-registry` (or similar criome-*)
- (b) Absorb into `goldragon` (data-only today)
- (c) Absorb into `lojix-cli` (deploy CLI today)

User's answer (2026-05-10): none of the above. **It's persona — the
durable agent.**

---

## 2 · Why persona, not lojix-cli / goldragon / criome-*

The choosing principle, per `~/primary/skills/abstractions.md` §"the
verb belongs to the *right* noun, not just any nearby noun":

- **adjacency of types is not the same as adjacency of concerns.**
  `lojix-cli`, `goldragon`, and a new `criome-cluster-registry` are
  *adjacent* to cluster trust (they touch related data, run in similar
  deployment contexts) but their **concerns differ**.

| Candidate | Concern today | Why cluster-trust does not fit |
|---|---|---|
| `lojix-cli` | Transactional deploy CLI; runs Nix; projects horizon. | A deploy tool is a *one-shot operator action*, not a long-lived service. Cluster-trust is durable, push-receiving, push-emitting. Adding a daemon mode to a CLI tool is the modular-monolith failure mode. |
| `goldragon` | Cluster proposal data (`datom.nota`); declarative shape. | Goldragon is *data*, not a runtime. The cluster proposal describes *what should be*; cluster-trust observes *what is*. Different concern even though both are cluster-shaped. |
| New `criome-cluster-registry` | Hypothetical new criome-* component. | Sits in the wrong ecosystem. Criome is the data/CRDT/sema-ecosystem framing. Cluster-trust is the **agent's responsibility** — it consumes per-host publications because it acts on behalf of the system as a durable agent. |
| `persona-trust` (proposed) | Long-lived agent state for cross-host trust. | Sits in the right ecosystem. Persona is already the home of long-lived state-bearing components (`persona-mind`, `persona-router`); cluster-trust is the same shape with cross-host scope. |

The user's framing — *"the component that's gonna take the output of
ClaviFaber and populate the cluster data is an agent"* — names the
deciding criterion. **An agent**, not a deploy tool, not a data record,
not a registry component in the abstract. Persona is the workspace's
agent-shaped ecosystem.

---

## 3 · The durable-agent positioning

The user's wider claim is that **persona is the answer to OpenClaw and
Gas City**. This positioning is upstream of every individual persona
component and worth recording as the architectural commitment that
explains *why the persona ecosystem exists at all*.

### What persona is contrasting against

- **Gas City** (per `~/primary/reports/1-gas-city-fiasco.md`): an
  orchestration system that tried to reconcile too many sources of truth
  (TOML config, runtime state, session beads, metadata hashes, tmux
  state, Dolt SQL, file events, cached store, controller memory) by
  *polling, scanning, and writing markers*. The failure mode was a
  state-machine reconciliation stack that turned uncertainty into hidden
  mutation. Idle systems paid full Dolt commit cost; supervisors fell
  into hot loops; sessions multiplied; "one fix surfaced the next hidden
  loop." That report's recommendation: *"every state transition should
  have an owner, an input event, an output event, and a durable record."*
- **OpenClaw** (and similar agent-CLI products): one-shot agent harnesses
  with no persistent state across invocations, no inspectable system
  behind them, no durable orchestration beyond a session.

Persona is the alternative to **both failure modes**. Concretely:

| Gas-City failure mode | Persona answer |
|---|---|
| Many sources of truth reconciled by polling | Each state-bearing component owns one redb file; producers push, consumers subscribe. No polling. |
| Hidden mutation under uncertainty | Every state transition has a typed input event, typed output event, and a durable record. Constraints become witness tests. |
| State-machine controller spawning processes | Direct Kameo actors with named planes, supervised, traceable. |
| Tmux-as-runtime-substrate | Terminal as adapter; harnesses as first-class records. |
| One-shot agent CLIs with no persistent state | Long-lived daemons (mind, router, harness). Agent-shaped CLIs are thin clients. |
| OpenClaw-shaped scope: one chat, no system | The whole stack is the system. The agent is durable across days. |

This is not new architecture — it is the explicit naming of what the
persona ecosystem has been *for* all along. The reporter's discipline
(`~/primary/skills/reporting.md` §"State assumptions explicitly") is
satisfied by writing this down rather than letting it stay implicit in
the component shapes.

### Why this matters for `primary-rab`

If persona is the durable agent, then **anything cluster-shaped that the
agent must observe, decide on, or act through belongs in the persona
ecosystem.** Cluster-trust qualifies: the agent must know which hosts
in the cluster are trusted, must distribute trust observations to host
subscribers, must commit new publications atomically. That's
durable-agent work.

It would be a category error to put cluster-trust in `lojix-cli`
(operator-action shape) or `goldragon` (declarative-data shape). They are
different concerns even though they touch similar deployment contexts.

---

## 4 · Concrete component proposal — `persona-trust`

A new long-lived persona-* component, sibling to `persona-mind` and
`persona-router`. Same shape as those: typed Kameo actor tree, owns its
own redb file, owns its own Sema layer/table declarations, talks to
neighbors through Signal contracts.

### What it owns

- **`cluster-trust.redb`** — durable per-host trust state. One slot per
  `NodeName` mapping to the latest committed `PublicKeyPublication`
  plus its commit slot and timestamp from the transition log.
- **`ClusterRegistryActor`** — accepts publication submissions from each
  host's clavifaber convergence run; mints `Slot<PublicKeyPublication>`
  on commit; idempotent on re-submission of same `NodeIdentity`.
- **`TrustDistributionActor`** — owns subscriber set; emits `TrustUpdate`
  events to each subscriber per committed revision change. Subscription
  contract per `~/primary/skills/push-not-pull.md`: emit current state
  on connect, then deltas. No polling.
- **`signal-clavifaber` channel endpoints**: see `designer/111` for
  contract shape.

### What it does not own

| Concern | Owner | Reason |
|---|---|---|
| Per-host private key material | `clavifaber` (each host) | Local authority over private bytes; never crosses the cluster boundary in raw form. |
| Cluster *configuration* (which hosts should exist) | `goldragon` (declarative proposal) | Cluster-trust is *what is*, not *what should be*. |
| Activation / deploy of host-side clavifaber | `lojix-cli` / `CriomOS` | Deploy-time action, not durable runtime. |
| Cross-machine wire transport | `signal-network` (future, `primary-uea`) | Cluster-trust is a typed-channel consumer; the wire layer is a separate concern. |
| Workspace-coordination state (roles, work graph) | `persona-mind` | Different durable-agent surface; one `persona-mind` per workspace, one `persona-trust` per cluster. |
| Message routing / delivery | `persona-router` | Different stream; trust observations are one-way push from registry to subscribers. |

### Why `persona-trust`, not `persona-cluster`

Two candidate names; my recommendation is `persona-trust`. The argument:

- **Concern-first naming**: "trust" is the **content** the component
  owns (cross-host trust observations). "Cluster" describes **where**
  the content sits (the cluster as a system shape). Per `naming.md` and
  the verb-belongs-to-noun discipline, the name should describe the
  *content* the component is responsible for, not the deployment
  context. `Tracker`/`Cache`/`Ledger` shapes are right-side names;
  `ClusterCache` is the wrong shape (locates instead of names).
- **Trust is the load-bearing concept**: the component's purpose is to
  *establish trust between hosts*. The cluster is the scope; trust is
  the verb-noun. Future components might also be cluster-scoped
  (cluster-routing, cluster-mind extensions); naming this one
  `persona-cluster` would block them.
- **Symmetry with persona-mind**: `persona-mind` owns mind state;
  `persona-trust` owns trust state. Both are noun-form names that
  describe what the component holds, not where it runs.

If the user prefers `persona-cluster` to keep the per-host vs.
per-cluster boundary visible in the name, that's a defensible call —
but the trade-off is naming the *scope* over the *content*. I'd lean on
`persona-trust` and let any future cluster-scoped components find their
own right names.

### Where it runs

`persona-trust` runs as a long-lived daemon on the **cluster's central
node** (today: Prometheus). Each host's clavifaber convergence run pushes
its publication to `persona-trust`. Each host that needs to consume
trust observations subscribes to `persona-trust`'s `TrustDistribution`
channel.

This is asymmetric: clavifaber is per-host, one-shot, ephemeral;
`persona-trust` is per-cluster, long-lived, durable. The user surfaced
this asymmetry on `primary-rab` ("cluster registry it publishes to is
long-lived... cannot collapse into one"). The component identity
respects it.

---

## 5 · `persona/ARCHITECTURE.md` updates

Three additions to `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md`
(landing in the same commit as this report):

1. **New §0.5 "Persona — the durable agent"** between the current §0
   (TL;DR) and §1 (Component Map): names the OpenClaw/Gas-City framing
   as the upstream architectural commitment. Two paragraphs + one table
   contrasting Gas-City failure modes with persona answers.
2. **Component map (§1) gains `persona-trust` and `signal-clavifaber`
   rows**: with the role descriptions above, marked as *"in design;
   first implementation in `primary-e3c`"*.
3. **Mind/Router/Harness/System table (§5) gains a `persona-trust`
   row**: names what it owns and what it doesn't own. The split table
   is now five components, not four.
4. **Constraints (§7) gains one bullet**: *"Cluster-trust runtime is
   persona-shaped — it lives in the persona ecosystem, not in deploy
   tools, declarative cluster data, or a separate registry component."*

The actual diff is in the `persona` repo commit alongside this report;
the report names the shape, the architecture file holds the truth.

---

## 6 · Follow-up beads

`primary-rab` closes with this report. Two new beads to file as the
implementation thread continues:

- **`persona-trust` repo creation**: new GitHub repo under
  `LiGoldragon/`, `cargo init` with the Kameo+Sema+signal-* template.
  Owner: system-specialist (deployment-context-shaped) or operator
  (Rust-implementation-shaped); my pick is operator since the
  initial scaffolding mirrors `persona-mind`'s actor + Sema +
  signal-channel pattern. Files later when needed.
- **`persona/ARCHITECTURE.md` cluster-trust integration tests**: the
  apex repo's §9 architectural-truth-tests gains rows for
  *"persona-trust holds per-host publications by NodeName"* and
  *"trust subscribers receive updates without polling"*. Ties into
  `primary-e3c`'s acceptance criteria.

`primary-9xo` (signal-clavifaber contract) closes with `designer/111`
(separate report, same session).

`primary-e3c` (the implementation bead) keeps its existing dependency
edges — it was blocked-by `primary-rab`, `primary-9xo`, and
`primary-7a7`; once `rab` and `9xo` close it depends only on `7a7`
(per-host clavifaber convergence runner, system-assistant lane).

---

## See also

- `~/primary/reports/1-gas-city-fiasco.md` — the durable-agent framing's
  upstream record; what persona is contrasting against.
- `~/primary/protocols/active-repositories.md` — current persona
  ecosystem; will gain `persona-trust` and `signal-clavifaber` rows
  alongside the architecture commit.
- `~/primary/reports/designer/111-signal-clavifaber-contract-shape.md`
  — sibling report; defines the channels `persona-trust` exposes.
- `~/primary/skills/abstractions.md` §"the verb belongs to the *right*
  noun" — discipline for picking persona over deploy/data candidates.
- `~/primary/skills/micro-components.md` §"adding a feature defaults to
  a new crate" — discipline for picking a new persona-* component over
  absorbing into existing ones.
- `/git/github.com/LiGoldragon/clavifaber/src/publication.rs:7-13` —
  `PublicKeyPublication` shape persona-trust consumes.
- `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md` — destination
  for the durable-agent positioning + `persona-trust` component map
  entry.
