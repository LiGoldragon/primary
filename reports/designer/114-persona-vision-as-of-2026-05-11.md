# 114 — Persona vision as of 2026-05-11

*Designer report. A panoramic synthesis of what Persona is, how it fits the
sema-ecosystem, how the human and the agents share the engine, and how
work opens and closes. Written after a full sweep of every workspace skill
and every active-repo `ARCHITECTURE.md`. Visuals + contracts + scenarios.*

---

## 0 · TL;DR

**Persona is the durable agent.**

It is the workspace's answer to two failure modes: one-shot agent CLIs
that hold no state across sessions, and reconciliation-stack controllers
that lose sight of what's actually happening. Persona replaces both with a
**federation of long-lived, supervised, typed daemons** — each owning one
plane of state, each speaking only through typed wire contracts, each
introspectable from outside.

The federation has six components, each a separate repo with its own
redb store and its own `signal-persona-*` contract:

| Component | What it owns |
|---|---|
| **`persona`** (engine manager) | Supervisor of the whole engine. Component health, lifecycle, engine status. |
| **`persona-mind`** | The work graph. Role coordination, activity, items, notes, edges, ready/blocked views. Replaces lock-files + BEADS. |
| **`persona-router`** | Message routing, delivery state, gate decisions. Sits between message senders and harnesses. |
| **`persona-system`** | OS / window-manager observations (focus, prompt-buffer state). Pushed, not polled. |
| **`persona-harness`** | Harness identity, lifecycle, transcript. Models AI sessions (Codex, Claude, Pi) as addressable nouns. |
| **`persona-terminal`** | Durable PTYs + viewers. Today still `persona-wezterm` + `terminal-cell`; production split pending. |

Underneath sits the **sema-ecosystem**: `sema-db` (typed-database library),
`criome` (today's records validator), `signal-core` (wire kernel), the
`signal-*` contract crates. Persona links `sema-db` for storage and speaks
`signal-core`-framed messages.

**The human appears in three places**: at the terminal (typing into a
viewer attached to a `persona-terminal` cell); at the design surface
(authoring ESSENCE.md, reports, skills); and at the deploy surface
(authoring NOTA deploy requests for `lojix-cli` to execute).

**Agents take and close work** through `persona-mind`'s typed work graph.
A claim is a typed `RoleClaim` record; release is a typed `RoleRelease`;
opening a work item is an `Opening`; closing is a `StatusChange` to
`Closed`. The lock-file helper is the transitional projection; the
destination is the `mind` CLI as a thin client to the `persona-mind`
daemon.

**Persona today is built rightly for today's stack** (Rust on Linux,
direct Kameo, `sema-db`, signal-* wire). The **eventual** form is
Sema-on-Sema: every Persona component as a Sema program on a Sema
runtime on a Sema-written OS, with auth realized as Criome's
quorum-signature multi-sig. Per `ESSENCE.md` §"Today and eventually",
this is a **scope discipline, not a quality one** — each piece below is
built to be eventually impossible to improve in its current scope, not
sketched as a draft of the eventual.

---

## 1 · The bird's-eye view

```mermaid
flowchart TB
    subgraph human["The human"]
        terminal["Ghostty / WezTerm viewer<br/>(types, sees output)"]
        editor["text editor<br/>(writes ESSENCE.md, reports, skills, NOTA requests)"]
    end

    subgraph agents["Agents (Claude Code, Codex, …)"]
        designer_agent["designer"]
        operator_agent["operator"]
        system_agent["system-specialist"]
        poet_agent["poet"]
        assistant["…-assistant variants"]
    end

    subgraph persona_layer["Persona federation"]
        persona_mgr["persona<br/>(engine manager)"]
        mind["persona-mind<br/>(work graph)"]
        router["persona-router<br/>(message routing)"]
        system_obs["persona-system<br/>(focus / prompt-buffer obs)"]
        harness["persona-harness<br/>(harness identity)"]
        term["persona-terminal<br/>(PTYs + viewers)"]
    end

    subgraph sema_layer["Sema ecosystem (today)"]
        sema_db["sema-db<br/>(typed database library)"]
        signal_core["signal-core<br/>(wire kernel + 12 verbs)"]
        criome_daemon["criome<br/>(records validator)"]
        forge_daemon["forge<br/>(executor)"]
        arca_daemon["arca-daemon<br/>(privileged blob store)"]
        nexus_daemon["nexus daemon<br/>(text↔signal)"]
    end

    subgraph os_layer["OS / cluster"]
        criomos["CriomOS<br/>(NixOS host)"]
        lojix["lojix-cli<br/>(deploy)"]
        clavifaber["clavifaber<br/>(host keys, certs)"]
        goldragon["goldragon<br/>(cluster proposal)"]
        chroma_daemon["chroma<br/>(theme / warmth / brightness)"]
    end

    terminal --> term
    editor --> agents
    agents --> mind
    agents -.->|messages| router
    router --> harness
    harness --> term
    term --> terminal

    system_obs -->|pushed observations| router
    persona_mgr -->|supervises| mind
    persona_mgr -->|supervises| router
    persona_mgr -->|supervises| system_obs
    persona_mgr -->|supervises| harness
    persona_mgr -->|supervises| term

    mind -->|sema-db| sema_db
    router -->|sema-db| sema_db
    harness -->|sema-db| sema_db
    persona_mgr -->|sema-db| sema_db

    agents -.->|signal frames| signal_core

    criome_daemon -->|owns records| sema_db
    criome_daemon -->|signal-forge| forge_daemon
    forge_daemon -->|signal-arca| arca_daemon
    nexus_daemon -->|NOTA ↔ signal| criome_daemon

    persona_layer -.->|"runs on"| criomos
    lojix -->|deploys| criomos
    goldragon -->|projection| lojix
    clavifaber -->|host keys| criomos
    chroma_daemon -->|theme| terminal
```

Eight layers, each owning a sliver. None of the arrows are runtime calls
to a shared in-memory state; every arrow is a **typed wire boundary**
(rkyv frames on UDS) or an **OS-level interface** (PTY, filesystem, nix
activate).

---

## 2 · Persona — the durable agent

### 2.1 What Persona IS

Persona is **a federation of long-lived daemons** that collectively
provide the substrate for autonomous agents (Claude, Codex, future
agents) to act on a shared workspace with persistent memory, durable
work tracking, and inspectable execution.

Each daemon is:

- **Long-lived.** Started at session start; lives until shutdown.
  Survives individual agent CLI invocations.
- **Supervised.** Each component is one or more Kameo actors with
  declared restart policies; the `persona` engine manager supervises
  the supervisors.
- **Typed.** Inputs and outputs are typed records, defined in a
  dedicated `signal-persona-*` contract crate. No string-tagged
  dispatch, no `Unknown` escape variants.
- **State-isolated.** Each owns one redb file (`mind.redb`,
  `router.redb`, `harness.redb`, …) opened by exactly one actor.
- **Inspectable.** Every actor has a trace; every state transition
  has a typed event; the `persona` engine manager exposes status
  through `signal-persona`.

### 2.2 The six components

```mermaid
flowchart LR
    mgr["persona<br/>engine manager"]
    mind_node["persona-mind"]
    router_node["persona-router"]
    system_node["persona-system"]
    harness_node["persona-harness"]
    term_node["persona-terminal<br/>(transitional: persona-wezterm + terminal-cell)"]

    mgr -->|signal-persona| mind_node
    mgr -->|signal-persona| router_node
    mgr -->|signal-persona| system_node
    mgr -->|signal-persona| harness_node
    mgr -->|signal-persona| term_node

    system_node -->|signal-persona-system observations| router_node
    router_node -->|signal-persona-harness deliveries| harness_node
    harness_node -->|signal-persona-terminal| term_node
```

| Component | Owns | Does not own |
|---|---|---|
| `persona` (mgr) | supervisor state; component desired/actual state; engine status surface | component-internal logic, work graph, message routing |
| `persona-mind` | role claims, activity, work graph, decisions, aliases, ready views | message delivery, harness lifecycle, terminal transport |
| `persona-router` | message frames, delivery queue, gate state, pending delivery records | role state, work graph, harness process lifecycle |
| `persona-system` | OS / window / input observations (FocusObservation, InputBufferObservation) | routing decisions, harness state |
| `persona-harness` | harness identity, lifecycle state, transcript events | router policy, terminal byte transport |
| `persona-terminal` | durable PTYs, viewer attachments, transcript replay, raw byte transport | Persona message semantics, role state, slash-command parsing |

### 2.3 Why federated, not monolithic

The federation is not coincidence — it is the workspace's
`skills/micro-components.md` rule applied to the agent runtime:

- **One capability, one crate, one repo.** Each component fits in
  one LLM context window (3k–10k lines including tests). A single
  agent can hold the whole component in mind.
- **Filesystem-enforced boundaries.** A bug in the router cannot
  silently corrupt the mind's work graph; they are different
  processes with different redb files.
- **Typed protocols cross every boundary.** Module-level
  boundaries decay under pressure ("modular monolith" failure
  mode); separate repos with separate contract crates do not.
- **Independent replaceability.** When the `persona-wezterm`
  + `terminal-cell` split lands as `persona-terminal`, the rest of
  the federation keeps working unchanged because the
  `signal-persona-terminal` contract is the contract.

### 2.4 The actor density

Each component is **actor-dense** per `skills/actor-systems.md` —
every non-trivial logical plane gets a named, supervised, data-bearing
actor with typed mailbox and trace witnesses.

For example, `persona-mind`'s topology (from its ARCHITECTURE.md):

```mermaid
flowchart TB
    mind_root["MindRoot<br/>(runtime root; routes ingress/dispatch/domain/store/view/reply)"]
    store_super["StoreSupervisor"]
    store_kernel["StoreKernel<br/>(sole redb opener)"]
    memory_store["MemoryStore<br/>(graph reducer)"]
    claim_store["ClaimStore"]
    activity_store["ActivityStore"]
    ingress_phase["IngressPhase<br/>(trace witness)"]
    dispatch_phase["DispatchPhase"]
    view_phase["ViewPhase"]
    sub_super["SubscriptionSupervisor"]

    mind_root --> ingress_phase
    mind_root --> dispatch_phase
    mind_root --> store_super
    mind_root --> view_phase
    mind_root --> sub_super

    store_super --> store_kernel
    store_super --> memory_store
    store_super --> claim_store
    store_super --> activity_store
```

Every actor has a typed message vocabulary (per-kind `Message<T>`
impls). Every long-lived state is in `mind.redb` (via `sema-db`), so
restart reconstruction works. Every blocking plane is one of three
templates (per `skills/kameo.md` §"Blocking-plane templates"): detach,
dedicated thread, or `tokio::process` + timeout.

---

## 3 · How Persona relates to Criome

The relationship is **two things at two scopes**, and conflating them
is the workspace's most common failure mode.

### 3.1 Today: separate stacks, separate concerns

```mermaid
flowchart TB
    subgraph persona_today["Persona stack (today)"]
        p_mind["persona-mind"]
        p_router["persona-router"]
        p_etc["…the federation"]
    end

    subgraph sema_today["sema-ecosystem stack (today)"]
        criome_d["criome daemon<br/>(records validator)"]
        forge_d["forge daemon"]
        arca_d["arca-daemon"]
        nexus_d["nexus daemon"]
    end

    subgraph shared["Shared substrate"]
        sema_lib["sema-db<br/>(typed database library)"]
        sig_core["signal-core<br/>(wire kernel + 12 verbs)"]
    end

    persona_today --> sema_lib
    sema_today --> sema_lib
    persona_today -.->|signal frames| sig_core
    sema_today -.->|signal frames| sig_core
```

| Concern | Persona today | sema-ecosystem today |
|---|---|---|
| **Domain** | Agent runtime; durable workspace coordination | Typed records (Graph/Node/Edge/Derivation/CompiledBinary); build/deploy |
| **State** | Component-owned redb files via sema-db | criome.redb owned by criome daemon |
| **Contracts** | `signal-persona-*` family | `signal` + `signal-forge` + `signal-arca` |
| **Auth/identity** | (none yet; uses local-user-trust shim) | (none yet; capability tokens are designed but not landed) |
| **Effect dispatch** | Direct (within Persona) | criome validates + dispatches to forge/arca |

The split is **today's correct shape**. Persona is the durable-agent
runtime; criome is the records validator. They share `sema-db` (the
typed-database library) and `signal-core` (the wire kernel) but
otherwise their concerns are disjoint.

A Persona session **does not call criome** for anything in its
day-to-day operation. Persona writes its own state to its own redb
files; criome owns its records database independently.

### 3.2 Eventually: convergent paradigms in one Sema substrate

Per `ESSENCE.md` §"Today and eventually":

- **Eventual Sema** is the universal medium for meaning — a
  self-hosting computational substrate, a fully-typed
  human-language representation, a universal interlingua.
- **Eventual Criome** is the universal computing paradigm,
  expressed in Sema — replacing Git, the editor, SSH, the web;
  encompassing programming, version control, network identity,
  validation, and auth/security across the stack.

When the OS itself is written in Sema, the split between
"persona-the-federation" and "criome-the-validator" dissolves
into one paradigm:

```mermaid
flowchart TB
    subgraph eventually["Eventual Sema-on-Sema stack"]
        persona_sema["Persona (Sema program)<br/>durable agents, work graph"]
        criome_sema["Criome (Sema program)<br/>computing paradigm: VCS, editor, network, auth"]
        sema_runtime["Sema runtime<br/>(Sema interpreter / compiler / assembler)"]
        sema_os["Sema-OS<br/>(host written in Sema)"]
    end

    persona_sema --> sema_runtime
    criome_sema --> sema_runtime
    sema_runtime --> sema_os
```

In the eventual:

- Persona's state is one view of typed Sema records, not a
  separate component-owned redb.
- Persona's logic projects from Sema rules, not hand-coded Rust.
- Persona's auth lives in Criome's quorum-signature multi-sig
  (infinitely programmable multi-sig on every object), not in
  ad-hoc local-user-trust.
- The wire between Persona and Criome dissolves — they share a
  substrate, not a socket.

**This is one stack, not many.** The split today is "today's stack"
(Rust + Linux + redb + separate daemons + legacy auth) **vs** "the
eventually self-hosting stack" (Sema all the way down) — not
per-component slow climbs.

### 3.3 The convergence vector — what survives

What carries across both eras:

1. **Perfect specificity.** Every typed boundary names exactly
   what flows through it. Closed enums, no `Unknown` variants, no
   string-tagged dispatch. This is the apex invariant.
2. **Content addressing.** Identity is the hash of canonical
   encoding; mutable handles (slots) sit on top of immutable
   identities. Same shape in both eras.
3. **Push, not poll.** Producers push; consumers subscribe.
   `skills/push-not-pull.md` survives without modification.
4. **Verb belongs to noun.** The Sema substrate is built from
   the same discipline that shapes today's Rust.
5. **One capability, one crate, one repo** — even when "crate"
   becomes "Sema module" and "repo" becomes "Criome graph."
   Filesystem decomposition becomes graph decomposition; the
   discipline is unchanged.

What gets retired:

- The Rust/Nix/Linux/redb substrate (replaced by Sema).
- Per-component-owned databases (replaced by typed Sema records
  in one substrate).
- The `signal-*` wire crates (replaced by Sema-native semantics).
- ClaviFaber-shaped key-material shims (replaced by Criome's
  quorum-signature multi-sig).
- BEADS, lock files, the orchestrate helper (replaced by the
  Sema work graph directly).

---

## 4 · The wire vocabulary

Persona's wire is fully typed and closed. Every inter-component
message is a length-prefixed rkyv archive of a closed Rust type
defined in a `signal-*` crate.

### 4.1 The hierarchy

```mermaid
flowchart TB
    sig_core["signal-core<br/>Frame, handshake, auth, 12-verb spine,<br/>Slot<T>, Revision, PatternField<T>"]

    sig["signal<br/>(sema-ecosystem record vocabulary:<br/>Node, Edge, Graph, AssertOp, MutateOp, …)"]

    sig_persona["signal-persona<br/>(engine manager contract:<br/>EngineRequest, EngineReply, ComponentStatus)"]

    sig_mind["signal-persona-mind<br/>(work graph: RoleClaim, Opening, Note, Link, …)"]
    sig_msg["signal-persona-message<br/>(MessageSubmission, InboxQuery)"]
    sig_sys["signal-persona-system<br/>(FocusObservation, InputBufferObservation)"]
    sig_harn["signal-persona-harness<br/>(MessageDelivery, DeliveryFailureReason, harness lifecycle)"]
    sig_term["signal-persona-terminal<br/>(OpenTerminal, ResizeTerminal, transcript events)"]

    sig_forge["signal-forge<br/>(criome ↔ forge: Build, Deploy)"]
    sig_arca["signal-arca<br/>(planned: writers ↔ arca-daemon)"]

    sig_core --> sig
    sig_core --> sig_persona
    sig_core --> sig_mind
    sig_core --> sig_msg
    sig_core --> sig_sys
    sig_core --> sig_harn
    sig_core --> sig_term

    sig --> sig_forge
    sig --> sig_arca
```

### 4.2 The twelve verbs

`signal-core` owns the closed twelve-verb spine. Every contract
crate pairs verbs with its own typed payloads.

| Verb | Meaning | Used by (representative) |
|---|---|---|
| `Assert` | introduce a typed record | `signal::AssertOperation`, `signal-persona-message::MessageSubmission` |
| `Subscribe` | register a push subscription | `signal-persona-system::FocusSubscription` |
| `Constrain` | snapshot query (point-in-time) | `signal-persona-system::FocusSnapshot` |
| `Mutate` | change an existing record | `signal::MutateOperation`, `signal-persona-mind::Opening` |
| `Match` | pattern-based query | `signal::QueryOperation`, `signal-persona-mind::Query` |
| `Infer` | derive new records from rules | (future; not yet used) |
| `Retract` | remove a record | `signal::RetractOperation` |
| `Aggregate` | grouped result | (future) |
| `Project` | structural projection | `signal-forge::StoreGet` (control-plane) |
| `Atomic` | atomic group of operations | `signal::AtomicBatch` |
| `Validate` | dry-run validation | `signal::ValidateOperation` |
| `Recurse` | nested traversal | (future) |

The verb set is **closed**. Adding new behavior lands as new
typed payloads under existing verbs, not as new verbs.

### 4.3 The relation matrix

Each contract names exactly one relation. Knowing the relation
sentence (per `skills/contract-repo.md`) makes the matrix readable.

| Source | Destination | Contract | Verbs used | Key records |
|---|---|---|---|---|
| client | criome | `signal` | Assert, Mutate, Match, Atomic, Retract, Validate | `Node`, `Edge`, `Graph`, `AssertOperation`, `MutateOperation`, `QueryOperation` |
| criome | forge | `signal-forge` | Mutate (effect), Project (store-ops) | `Build`, `Deploy`, capability-token |
| orchestrate / harness | `persona` | `signal-persona` | Match (status query), Mutate (component start/stop) | `EngineRequest`, `EngineReply`, `ComponentStatus` |
| `mind` CLI / agent | `persona-mind` | `signal-persona-mind` | Mutate (claims, activity, work), Match (queries, observation) | `RoleClaim`, `Opening`, `Note`, `Link`, `StatusChange`, `RoleSnapshot`, `View` |
| `message` CLI | `persona-router` | `signal-persona-message` | Assert (submission), Match (inbox) | `MessageSubmission`, `MessageSlot`, `InboxListing` |
| `persona-router` | `persona-system` | `signal-persona-system` | Subscribe, Constrain | `FocusObservation`, `InputBufferObservation`, `SystemTarget`, `ObservationGeneration` |
| `persona-router` | `persona-harness` | `signal-persona-harness` | Mutate (delivery, cancellation), Subscribe (lifecycle) | `MessageDelivery`, `DeliveryFailureReason`, `HarnessStarted` |
| `persona-harness` | `persona-terminal` | `signal-persona-terminal` (planned) | Mutate (open/resize/close), Subscribe (transcript) | `TerminalRequest`, `TerminalEvent` |

### 4.4 Shape of a contract — `signal-persona-mind` in detail

The mind contract is the most-developed example. Its top-level
shape:

```rust
// signal-persona-mind/src/lib.rs (skeleton sketch — see repo for current)

pub enum MindRequest {
    RoleClaim(RoleClaim),
    RoleRelease(RoleRelease),
    RoleHandoff(RoleHandoff),
    RoleObservation(RoleObservation),
    ActivitySubmission(ActivitySubmission),
    ActivityQuery(ActivityQuery),
    Opening(Opening),
    NoteSubmission(NoteSubmission),
    Link(Link),
    StatusChange(StatusChange),
    AliasAssignment(AliasAssignment),
    Query(Query),
}

pub enum MindReply {
    ClaimAcceptance(ClaimAcceptance),
    ClaimRejection(ClaimRejection),
    ReleaseAcknowledgment(ReleaseAcknowledgment),
    HandoffAcceptance(HandoffAcceptance),
    HandoffRejection(HandoffRejection),
    RoleSnapshot(RoleSnapshot),
    ActivityAcknowledgment(ActivityAcknowledgment),
    ActivityList(ActivityList),
    OpeningReceipt(OpeningReceipt),
    NoteReceipt(NoteReceipt),
    LinkReceipt(LinkReceipt),
    StatusReceipt(StatusReceipt),
    AliasReceipt(AliasReceipt),
    View(View),
    Rejection(Rejection),
}

pub struct RoleClaim {
    pub role: RoleName,           // closed enum of eight roles
    pub scopes: Vec<ScopeReference>,  // Path or Task
    pub reason: ScopeReason,
}

pub struct Opening {
    pub kind: ItemKind,           // Task | Decision | Question | Memory
    pub priority: ItemPriority,   // Low | Normal | High
    pub title: ItemTitle,         // newtype-wrapped String
    pub body: Option<ItemBody>,
    pub parent: Option<StableItemId>,
}
```

Caller identity (`who is claiming`), timestamp, and event sequence
are infrastructure-supplied at the daemon boundary — they never
appear in `MindRequest`. Per `ESSENCE.md` §"Infrastructure mints
identity, time, and sender".

Worked NOTA example (`mind` CLI invocation):

```text
$ mind '(RoleClaim Operator ((Path "/git/github.com/LiGoldragon/persona-mind"))
                    "implement command-line mind")'
(ClaimAcceptance ...)

$ mind '(Opening Task High "wire command-line mind"
                  "replace lock-file helper with typed mind state")'
(OpeningReceipt (item_id 42) (timestamp 1748600000000000000))

$ mind '(Query Ready 20)'
(View (ready_items ((Item (id 42) (title "wire command-line mind") (priority High) ...))))
```

Each invocation is one NOTA record in, one NOTA reply record out.
The CLI is a thin client; the daemon owns `MindRoot` and
`mind.redb`.

---

## 5 · Where the human lives

The human is not a peer of the agents. The human is **upstream of
the work** — they are the source of every claim that survives
across roles, the author of every design report's why, and the
final approver of every action that touches shared state outside
local edits.

Three live human-machine seams:

### 5.1 The terminal seam (live interaction)

```mermaid
flowchart LR
    human["human at keyboard"]
    viewer["Ghostty / WezTerm viewer"]
    cell["terminal-cell<br/>(PTY owner)"]
    input_gate["TerminalInputWriter<br/>(input gate)"]
    pty["child PTY<br/>(shell, harness CLI, agent)"]
    transcript["TerminalTranscript<br/>(append-only)"]

    human -->|keystrokes| viewer
    viewer -->|raw bytes| cell
    cell --> input_gate
    input_gate --> pty
    pty -->|output| cell
    cell -->|output to viewer| viewer
    viewer --> human
    cell -.->|side effect| transcript
```

The human types at a Ghostty (or WezTerm) viewer. The viewer attaches
to a `terminal-cell` daemon over a Unix socket. Bytes pass through
the **input gate** (`TerminalInputWriter`), which arbitrates between
human keystrokes and programmatic input (from `persona-harness`
delivering an agent-generated message). The PTY output flows back
through the cell to the viewer, with the transcript recording
everything as a side effect.

Two invariants:

- **Closing the viewer does not kill the harness.** The PTY daemon
  is durable; the viewer is disposable. Detach, reattach, kill the
  Ghostty window — the child process keeps running.
- **Input gate enforces mutual exclusion.** When Persona writes
  injected bytes (delivering a message to the harness), human
  keystrokes are either queued or rejected — gate state is observable
  per `signal-persona-terminal` events.

### 5.2 The design seam (authoring intent)

```mermaid
flowchart LR
    human2["human at editor"]
    essence["ESSENCE.md"]
    skills_dir["skills/<name>.md"]
    reports_dir["reports/<role>/N-*.md"]
    archdocs["<repo>/ARCHITECTURE.md"]

    human2 --> essence
    human2 --> skills_dir
    human2 --> reports_dir
    human2 --> archdocs

    essence -.->|read by every agent| agents_box["agents apply the intent"]
    skills_dir -.->|read by every agent| agents_box
    reports_dir -.->|read on demand| agents_box
    archdocs -.->|read in-repo| agents_box
```

The human writes `ESSENCE.md` (workspace intent), edits or directs
edits to skills, files designer reports through the designer agent,
and approves substantive changes to per-repo ARCHs. Agents read all of
this; the user's voice in design conversation carries the workspace's
vocabulary, and the **designer** agent's job is to be in continuous
dialogue with that voice (per `skills/designer.md` §"The user's
vocabulary").

The human's design surface is **append-mostly**: ESSENCE grows by
reframing, not by replacement; skills evolve in place; reports
accumulate per role and supersede older reports cleanly (per
`skills/reporting.md` §"Hygiene").

### 5.3 The deploy seam (cluster intent)

```mermaid
flowchart LR
    human3["human (or autonomous agent acting on their behalf)"]
    nota_req["one NOTA deploy request<br/>(FullOs / OsOnly / HomeOnly)"]
    lojix_cli["lojix-cli"]
    horizon["horizon-rs (projection)"]
    nix_build["nix build (crane + fenix)"]
    activate["activate on target node"]

    human3 --> nota_req
    nota_req --> lojix_cli
    lojix_cli --> horizon
    horizon --> nix_build
    nix_build --> activate
```

For cluster-affecting changes (a new host, a new home-manager module,
a re-pin of a flake input that affects the running system), the human
authors **one typed NOTA record** describing the deploy. `lojix-cli`
reads it, projects through `horizon-rs`, builds via Nix, copies
closures with `--substitute-on-destination` so the cluster cache
signs them, and activates on the target node(s).

The whole deploy is one NOTA record — reproducible, auditable, and
identical across machines. No flags, no env vars, no interactive
prompts. The human's intent is the typed input.

### 5.4 Where the human is NOT

The human is **not** in the message-routing loop. When an agent writes
a message and the router commits it, the human doesn't approve each
delivery. The human's authority lives upstream (in the intent docs,
the design reports, the role discipline) and downstream (in the
terminal where they read or override). The middle is the federation.

---

## 6 · How agents take and close work

This is the heart of Persona-the-engine: **typed work, typed claims,
typed closure**, all flowing through `persona-mind`.

### 6.1 The eight roles

Per `protocols/orchestration.md`, the workspace recognises eight
coordination roles:

| Role | Default agent | Primary scope |
|---|---|---|
| `operator` | Codex | Rust crates, persona, sema-ecosystem implementation |
| `operator-assistant` | (any) | Operator-shaped support (audits, migrations) |
| `designer` | Claude | ESSENCE, AGENTS, skills, design reports |
| `designer-assistant` | Codex | Designer-shaped support (audits, cross-ref cleanup) |
| `system-specialist` | (any) | CriomOS, lojix-cli, horizon-rs, deploy |
| `system-assistant` | (any) | System-shaped support (host-tool work) |
| `poet` | (any) | TheBookOfSol, prose-as-craft |
| `poet-assistant` | (any) | Poet-shaped support (citation, publishing) |

The role is the discipline — **what kind of attention the work
demands**, not which model holds the role. Any model can take any
role; the role determines scope authority and which skills apply.

### 6.2 Where open work comes from

Work enters Persona's graph from four sources:

```mermaid
flowchart TB
    human4["human, in conversation<br/>('do X', 'design Y', 'fix Z')"]
    designer_role["designer authoring reports"]
    in_flight["work-in-progress<br/>(discovered while doing other work)"]
    audit["audit / cross-reference sweep<br/>(designer-assistant, operator-assistant)"]

    mind_graph["persona-mind work graph"]

    human4 -->|"user prompt"| mind_graph
    designer_role -->|"report's open questions"| mind_graph
    in_flight -->|"newly discovered task"| mind_graph
    audit -->|"drift findings"| mind_graph
```

1. **Human prompt.** The user says "do X" or "what should we do
   about Y?" in conversation. The receiving agent either acts
   directly (if the work is small and routine, per
   `skills/autonomous-agent.md`) or files an Opening in
   `persona-mind`.
2. **Designer reports.** Most substantive work is preceded by a
   designer report that frames the problem. The report's "Open
   questions" section becomes one or more typed work items.
3. **In-flight discovery.** While operator is implementing a
   designer report, they discover an unexpected gap. They file an
   implementation-consequences report and an Opening for the
   follow-up.
4. **Audit sweeps.** Designer-assistant or operator-assistant
   reviews recent work; drift findings become typed work items.

In every case, the work item is a typed `Opening` record going
through `signal-persona-mind`:

```text
(Opening Task Normal
         "audit terminal-cell input gate against persona-system observations"
         "after terminal-cell daemon work landed, the gate state should be
          observable through signal-persona-system; check the contract")
```

The item gets a stable id (`StableItemId`), a display id (e.g.,
`primary-bkb` — bd-shaped during the transitional era), a typed
kind, priority, and body.

### 6.3 How agents take work

When an agent starts a session:

```mermaid
sequenceDiagram
    participant Agent
    participant MindCLI as mind CLI
    participant Daemon as persona-mind daemon
    participant Redb as mind.redb

    Agent->>MindCLI: mind '(Query Ready (role designer) 20)'
    MindCLI->>Daemon: (signal-persona-mind frame)
    Daemon->>Redb: read ready-work view for role:designer
    Redb-->>Daemon: items
    Daemon-->>MindCLI: View { ready_items: [...] }
    MindCLI-->>Agent: NOTA reply

    Agent->>Agent: choose highest-priority item

    Agent->>MindCLI: mind '(RoleClaim Designer ([Path ".../skills/designer.md"]) "update designer skill")'
    MindCLI->>Daemon: (RoleClaim frame)
    Daemon->>Daemon: check overlap with other roles
    alt no overlap
        Daemon->>Redb: write RoleClaim row
        Daemon-->>MindCLI: ClaimAcceptance
    else overlap
        Daemon-->>MindCLI: ClaimRejection { reason }
    end
    MindCLI-->>Agent: NOTA reply
```

The agent's workflow:

1. **Session start: query ready work.** `mind '(Query Ready
   (role designer) 20)'` returns up to 20 ready items the
   designer role can take. "Ready" means not blocked by another
   open item, not claimed by another agent, not closed.
2. **Pick the highest priority item.** Per
   `skills/autonomous-agent.md`, the highest-priority open item
   is the workspace's continuing intent. The user's live prompt
   in the current turn wins over the bead, but absent that, the
   bead is the answer.
3. **Claim the role + scope.** `mind '(RoleClaim …)'` writes a
   typed claim with the role name, the scopes (paths or task
   tokens), and a reason. The daemon checks overlap with other
   roles' active claims — overlap is rejected.
4. **Update item status.** `mind '(StatusChange (id N)
   InProgress)'` marks the item as actively being worked on.

The lock-file helper is the transitional projection: while agents
are still using `tools/orchestrate claim`, the helper writes both
the lock-file and the typed claim (eventually only the typed
claim).

### 6.4 How agents close work

When the work lands:

```mermaid
sequenceDiagram
    participant Agent
    participant MindCLI as mind CLI
    participant Daemon as persona-mind daemon
    participant Redb as mind.redb

    Agent->>Agent: ship the work (commit + push)

    Agent->>MindCLI: mind '(NoteSubmission (item N) "landed in commit abc123, see designer/114")'
    MindCLI->>Daemon: (NoteSubmission frame)
    Daemon->>Redb: append note event
    Daemon-->>MindCLI: NoteReceipt

    Agent->>MindCLI: mind '(StatusChange (id N) Closed)'
    MindCLI->>Daemon: (StatusChange frame)
    Daemon->>Redb: mutate item state to Closed; append event
    Daemon-->>MindCLI: StatusReceipt

    Agent->>MindCLI: mind '(RoleRelease Designer)'
    MindCLI->>Daemon: (RoleRelease frame)
    Daemon->>Redb: clear active claim; append activity event
    Daemon-->>MindCLI: ReleaseAcknowledgment
```

Three actions:

1. **Note the substance.** Where did the work land? A commit
   hash, a designer report number, a path. The note is the
   breadcrumb for future agents.
2. **Status to Closed.** The state transition triggers
   subscription pushes — anyone watching this item is notified.
3. **Release the claim.** Frees the scope for the next agent.

If the work didn't land — was superseded, abandoned, reformulated
as discipline — the closure includes a typed reason:

```text
(StatusChange (id N) Superseded
              "Folded into designer/110's cluster-trust-runtime placement
               work; the original concern is covered there")
```

### 6.5 How agents interact with each other

Agents don't talk to each other directly. They interact through:

```mermaid
flowchart LR
    agent_a["Agent A<br/>(in role X)"]
    agent_b["Agent B<br/>(in role Y)"]
    mind_g["persona-mind work graph"]
    reports_dir2["reports/<role>/"]
    pr["GitHub PR / issue"]

    agent_a -->|"file Opening for Y"| mind_g
    agent_b -->|"query ready items for Y"| mind_g
    mind_g -->|"surfaces work"| agent_b

    agent_a -->|"write report"| reports_dir2
    agent_b -->|"read report"| reports_dir2

    agent_a -->|"file PR / issue"| pr
    agent_b -->|"see PR review"| pr
```

Three channels:

1. **The work graph.** Agent A files an Opening tagged
   `role:Y`; Agent B (in role Y) sees it via `mind '(Query Ready
   (role Y))'`. The graph is the durable handoff.
2. **Role-owned reports.** Designer writes a report in
   `reports/designer/`; operator reads it and writes an
   implementation-consequences report in `reports/operator/`. The
   reports are visible to all; ownership of subdirs prevents
   race-edits.
3. **GitHub PRs and issues.** Cross-machine, cross-time work
   surfaces. PRs are merged by the designer or by the user; the
   merge is the signal.

There is **no synchronous agent-to-agent communication**. Two
agents working in parallel on the same workspace see each other
through:
- The lock files (who holds what scope right now)
- The work graph (who's working what task)
- The git log (what just landed)

The orchestration protocol (`tools/orchestrate claim/release`)
prevents simultaneous edits to the same paths; the typed work
graph durably tracks who's doing what.

### 6.6 Where the orchestrate helper sits

Today's `tools/orchestrate` is the transitional ergonomic surface:

```mermaid
flowchart LR
    agent_shell["agent invoking shell command"]
    orchestrate["tools/orchestrate"]
    lock_file["<role>.lock<br/>(gitignored; per-machine)"]
    mind_path["mind CLI<br/>(future canonical path)"]
    daemon_path["persona-mind daemon"]

    agent_shell -->|"tools/orchestrate claim …"| orchestrate
    orchestrate -->|today| lock_file
    orchestrate -.->|future| mind_path
    mind_path --> daemon_path
```

The helper:
1. Writes the role's lock file (today).
2. Checks BEADS for open tasks.
3. Will eventually lower into a `mind` invocation (typed
   `RoleClaim` request).

When the `mind` CLI ships as a thin client to `persona-mind` and
agents adopt it, the orchestrate helper becomes either external
glue (translating ergonomic commands into `mind` invocations) or
retires. The lock files are not persisted by `persona-mind` — they
are transitional helper state that disappears at the cutover.

---

## 7 · Example scenarios

Five close-ups showing how the pieces fit at runtime. Each scenario
names which contracts cross which boundaries.

### 7.1 Scenario A — Operator picks up a P2 task

Setting: Operator (Codex) starts a session. There are open beads;
the highest-priority `role:operator` is `primary-bkb` (fix
persona-wezterm TerminalDelivery blocking violation).

```mermaid
sequenceDiagram
    participant Op as Operator (Codex)
    participant MindCLI as mind CLI
    participant Mind as persona-mind daemon
    participant Repo as persona-wezterm repo
    participant JJ as jj (version control)
    participant GitHub

    Op->>MindCLI: mind '(Query Ready (role operator) 10)'
    MindCLI->>Mind: signal-persona-mind frame
    Mind-->>MindCLI: View { items: [primary-bkb, primary-aww, ...] }
    MindCLI-->>Op: NOTA: ready items

    Op->>Op: read primary-bkb description; read designer/113

    Op->>MindCLI: mind '(RoleClaim Operator ([Path "/git/.../persona-wezterm"] [Task "primary-bkb"]) "fix TerminalDelivery blocking")'
    Mind-->>MindCLI: ClaimAcceptance
    MindCLI-->>Op: NOTA: claim accepted

    Op->>MindCLI: mind '(StatusChange (id primary-bkb) InProgress)'
    Mind-->>MindCLI: StatusReceipt

    Op->>Repo: read src/terminal.rs:150-157
    Op->>Repo: apply Template 3 (tokio::process + timeout per skills/kameo.md §"Blocking-plane templates")
    Op->>Repo: write test: handler_cannot_block_mailbox

    Op->>JJ: jj st (read working copy)
    Op->>JJ: jj commit -m 'TerminalDelivery: tokio::process + timeout (closes primary-bkb)'
    Op->>JJ: jj bookmark set main -r @-
    Op->>JJ: jj git push --bookmark main
    JJ->>GitHub: push

    Op->>MindCLI: mind '(NoteSubmission (item primary-bkb) "landed in commit <hash>")'
    Op->>MindCLI: mind '(StatusChange (id primary-bkb) Closed)'
    Op->>MindCLI: mind '(RoleRelease Operator)'
```

The whole cycle is:
1. **Discover** — `Query Ready`.
2. **Claim** — `RoleClaim` with paths + task token + reason.
3. **In progress** — `StatusChange InProgress`.
4. **Implement** — edit code per the relevant skills.
5. **Test** — Nix-backed test runs through `nix flake check`.
6. **Commit** — single `jj commit -m`, push.
7. **Note** — record where it landed.
8. **Close** — `StatusChange Closed`.
9. **Release** — `RoleRelease`.

Each step is a typed event in `mind.redb`. The next agent reading
the graph sees the full history.

### 7.2 Scenario B — Designer files a report; operator implements

Setting: Designer (Claude) writes designer/112 (day review) and
discovers in the process that persona-wezterm has a blocking-handler
violation. Designer writes designer/113 (the audit) and files a bead.

```mermaid
sequenceDiagram
    participant Design as Designer (Claude)
    participant MindCLI
    participant Mind
    participant Op as Operator (Codex; later session)

    Design->>Design: write reports/designer/113-actor-blocking-audit.md
    Design->>MindCLI: mind '(Opening Task Normal "Fix persona-wezterm::TerminalDelivery blocking violation" ...)'
    Mind-->>MindCLI: OpeningReceipt { item_id, display_id: "primary-bkb" }

    Design->>MindCLI: mind '(AliasAssignment (item primary-bkb) "role:operator-assistant")'
    Design->>MindCLI: mind '(AliasAssignment (item primary-bkb) "actor-discipline")'

    Note over Design,Mind: …time passes…

    Op->>MindCLI: mind '(Query Ready (role operator-assistant) 10)'
    Mind-->>Op: View { items: [primary-bkb, ...] }
    Op->>Op: read primary-bkb + designer/113 §"Suggested fix"
    Op->>Op: apply fix → commit → push
    Op->>MindCLI: mind '(StatusChange (id primary-bkb) Closed)'
```

The thread is:
1. Designer's report (designer/113) is the **frame**.
2. The Opening is the **handle** that surfaces in operator's queue.
3. The closing note points back at the commit, which references
   the report.

Reports and the work graph cross-reference each other; neither
duplicates the other. The report carries the substance; the work
graph carries the lifecycle.

### 7.3 Scenario C — Human types a message in a terminal

Setting: Human is at a Ghostty viewer attached to a `terminal-cell`
running a Claude harness. They type a question. Claude responds.

```mermaid
sequenceDiagram
    participant Human
    participant Ghostty as Ghostty viewer
    participant Cell as terminal-cell daemon
    participant Gate as TerminalInputWriter (input gate)
    participant PTY
    participant Claude as Claude harness (CLI in PTY)
    participant Router as persona-router (future)
    participant Harness as persona-harness

    Human->>Ghostty: keystrokes
    Ghostty->>Cell: attached input stream
    Cell->>Gate: write bytes
    Gate->>PTY: bytes (gate state: human)
    PTY->>Claude: bytes
    Claude->>Claude: compute response (calls Anthropic API or local)
    Claude->>PTY: response bytes
    PTY->>Cell: output bytes
    Cell->>Ghostty: forwarded output
    Ghostty->>Human: rendered text

    Note over Cell: side effect: TerminalTranscript appends every byte

    opt persona-router involvement (future)
        Claude->>Harness: signal-persona-harness DeliveryCompleted event
        Harness->>Router: subscription event
        Router->>Router: log delivery in router.redb
    end
```

Today, this is mostly raw byte transport through `terminal-cell` —
Persona's routing layer is not yet in the path. The destination
shape (per designer/110, designer/113, and the persona-router
ARCHITECTURE.md):

- Human keystrokes go through the input gate.
- The gate enforces mutual exclusion with Persona injections.
- Outputs flow back through the cell to the viewer.
- Persona-router subscribes to the harness's lifecycle events.
- When the router decides to inject a system message (e.g.,
  "another agent just claimed this scope"), it goes through
  `signal-persona-harness` → `persona-harness` → `signal-persona-terminal`
  → `terminal-cell`'s input gate → PTY.
- The input gate observes "Persona is writing now" state so
  human keystrokes don't interleave mid-injection.

The transcript captures everything — both human and Persona
bytes. The transcript is auditable evidence of what actually
happened in the session.

### 7.4 Scenario D — Designer-assistant audits operator's recent work

Setting: Designer-assistant (Codex in DA role) is asked to audit
the recent operator commits in `persona-mind` for drift from the
designer's stated architecture.

```mermaid
sequenceDiagram
    participant DA as Designer-assistant
    participant MindCLI
    participant Mind
    participant Repos as Recent operator commits
    participant ArchTests as Architectural-truth tests

    DA->>MindCLI: mind '(RoleClaim DesignerAssistant ([Path "/git/.../persona-mind"]) "audit recent operator work")'
    Mind-->>MindCLI: ClaimAcceptance

    DA->>Repos: git log --oneline persona-mind
    DA->>Repos: read recent commits
    DA->>Repos: read persona-mind/ARCHITECTURE.md
    DA->>Repos: read recent designer reports

    DA->>ArchTests: nix flake check (run topology, trace-pattern, forbidden-edge tests)
    ArchTests-->>DA: tests pass / fail

    DA->>DA: write reports/designer-assistant/<N>-persona-mind-audit.md

    DA->>MindCLI: mind '(NoteSubmission "audit landed: see designer-assistant/<N>")'
    DA->>MindCLI: mind '(RoleRelease DesignerAssistant)'
```

Designer-assistant's discipline (per `skills/designer-assistant.md`):
- Read the upstream design source first.
- Keep the work bounded — one audit target, one report.
- Surface drift through a typed report under
  `reports/designer-assistant/`.
- Don't make structural decisions; flag the question and hand
  back to designer.

The architectural-truth tests (per
`skills/architectural-truth-tests.md`) are how drift gets caught
mechanically: every load-bearing constraint in
`persona-mind/ARCHITECTURE.md` has a named witness test. If
operator's commits regressed an actor topology or bypassed a
required plane, the test fails.

### 7.5 Scenario E — System-specialist deploys a workspace-wide change

Setting: System-specialist needs to bump `nota-codec` across the
cluster after a designer-approved breaking change. The bump
affects every node that runs Persona components.

```mermaid
sequenceDiagram
    participant SS as System-specialist
    participant MindCLI
    participant Mind
    participant CO_Home as CriomOS-home repo
    participant FlakeLock as flake.lock files
    participant Cache as Prometheus (cluster cache)
    participant LojixCLI as lojix-cli
    participant Horizon as horizon-rs
    participant TargetNode as target node

    SS->>MindCLI: mind '(RoleClaim SystemSpecialist ([Path "/git/.../CriomOS-home"] [Path "/git/.../goldragon"]) "bump nota-codec cluster-wide")'

    SS->>CO_Home: nix flake update nota-codec
    SS->>FlakeLock: jj commit -m 'flake.lock: nota-codec to <rev>'
    SS->>CO_Home: jj git push

    SS->>SS: write NOTA deploy request:<br/>(FullOs goldragon zeus Switch prometheus)
    Note over SS,LojixCLI: builder=prometheus so cache signs closure

    SS->>LojixCLI: lojix deploy <request-file>
    LojixCLI->>Horizon: project (cluster zeus, viewpoint zeus)
    Horizon-->>LojixCLI: enriched horizon JSON

    LojixCLI->>Cache: build closure on prometheus
    Cache->>Cache: nix build (crane + fenix)
    Cache->>Cache: nix-serve signs closure

    LojixCLI->>TargetNode: nix copy --substitute-on-destination
    TargetNode->>Cache: substitute signed closure
    TargetNode->>TargetNode: nixos-rebuild switch
    TargetNode-->>LojixCLI: activation success

    SS->>MindCLI: mind '(NoteSubmission "deployed: zeus on rev <sha>")'
    SS->>MindCLI: mind '(RoleRelease SystemSpecialist)'
```

The deploy is one typed NOTA record. The flow:
1. SS updates the flake.lock (deterministic; the rev is pinned).
2. SS authors one `FullOs` request naming target, activation
   mode, and builder.
3. `lojix-cli` reads the request, projects through `horizon-rs`
   (a library), builds via Nix on the cache node, signs via
   `nix-serve`, copies with `--substitute-on-destination`, and
   activates.
4. SS records the deploy in `persona-mind` and releases.

The system-specialist's "just-do-it" rule (per
`skills/system-specialist.md` §"Just-do-it operations"): if the
session already authorized "use the new version", the downstream
flake.lock bump and the activating redeploy are part of the same
work — no need to confirm step-by-step.

---

## 8 · Open seams and drift

The map above is the **intended shape**. Several pieces are in
flight; the seams are honestly visible.

| Seam | Status | Where it lives |
|---|---|---|
| **`persona-wezterm` → `persona-terminal` split** | Pending rename. Today's `persona-wezterm` carries terminal-owner architecture; production split to `persona-terminal` (owner) with WezTerm/Ghostty/Niri as viewer adapters. | persona-wezterm/ARCHITECTURE.md; designer reports under designer/ |
| **`sema` → `sema-db` rename** | Pending. Bead `primary-ddx`. Naming reflects "today's piece" vs eventual `Sema`. | active-repositories.md; ESSENCE.md §"Today and eventually" |
| **Durable router state** | MVP uses in-memory pending-delivery; destination is `router.redb` via `sema-db`. | persona-router/ARCHITECTURE.md |
| **`persona-message` → router** | `persona-message` is transitional CLI/projection layer; durable message storage will live in router-owned sema tables. | persona-message/ARCHITECTURE.md |
| **`signal-persona-terminal` contract** | Planned, not yet instantiated. Currently inferred from terminal-cell + persona-wezterm boundaries. | terminal-cell/skills.md; persona-wezterm/ARCHITECTURE.md |
| **Trace phases → real actors** | Persona-mind has trace witnesses (`NotaDecoder`, `CallerIdentityResolver`, etc.) that should graduate to data-bearing actors. | persona-mind/ARCHITECTURE.md §"Trace phases" |
| **Actor blocking violation in TerminalDelivery** | Bead `primary-bkb` (P2). Fix is mechanical (Template 1 or Template 3 from `skills/kameo.md`). | designer/113; persona-wezterm/src/terminal.rs:150-157 |
| **Cluster trust runtime placement** | Designer/110 settled the scope discipline; system-specialist work pending on the runtime daemon. | reports/designer/110-cluster-trust-runtime-placement.md |
| **BEADS retirement** | Transitional. Native mind work graph is the destination. No long-term Persona↔bd bridge. | AGENTS.md §"BEADS is transitional" |
| **Lock-files retirement** | Transitional. `tools/orchestrate` becomes external glue (or retires) once agents use `mind` directly. | protocols/orchestration.md §"Command-line mind target" |

None of these are blockers for understanding the vision. They are
the **frontier of the work** — exactly where the next pieces land.

---

## 9 · Reading list — minimal path

For an agent or human entering the workspace cold, the minimal
reading sequence to understand Persona:

1. **`~/primary/ESSENCE.md`** — intent (the upstream of everything).
2. **`~/primary/AGENTS.md`** + **`repos/lore/AGENTS.md`** —
   workspace contract.
3. **`~/primary/protocols/orchestration.md`** — role coordination.
4. **`~/primary/protocols/active-repositories.md`** — current
   attention map.
5. **`~/primary/repos/persona/ARCHITECTURE.md`** — the engine
   manager's apex view.
6. **`~/primary/repos/criome/ARCHITECTURE.md`** — the
   sema-ecosystem apex (the eventual scope is named here).
7. **`~/primary/repos/signal-core/ARCHITECTURE.md`** — wire
   kernel.
8. **`~/primary/repos/signal-persona-mind/ARCHITECTURE.md`** — the
   most-developed contract; reading it teaches the pattern.
9. **`~/primary/repos/persona-mind/ARCHITECTURE.md`** — the
   work-graph runtime.
10. **`~/primary/skills/actor-systems.md`** +
    **`~/primary/skills/kameo.md`** — actor discipline.
11. **`~/primary/skills/contract-repo.md`** — wire-contract
    discipline.
12. **`~/primary/skills/push-not-pull.md`** — push-not-poll
    invariant.

Everything else is reachable from these twelve.

---

## 10 · Closing — the criterion

The vision can be summarised in one sentence:

> **A federation of typed, supervised, inspectable daemons —
> each owning one plane of state, each speaking through typed
> wire contracts — providing the substrate for durable agents to
> act on a shared workspace, with the human upstream of the
> intent and downstream of the live interaction.**

The criterion this report is held to is the same as everything
else in the workspace: **clarity → correctness → introspection →
beauty.** Each daemon reads cleanly. Each contract names exactly
what flows through it. Each state transition is observable from
outside. When the right shape is found, the structure dissolves
the special case into the normal case; what's left is the
operative architecture, not the residue of past decisions.

Today's Persona is built rightly for today's stack. The eventual
Sema-on-Sema substrate is one step up the same ladder, not a
different ladder. The convergence vector is the **closed verb
spine**, the **content-addressing discipline**, the
**verb-belongs-to-noun rule**, and the **micro-component
filesystem-enforced decomposition** — these survive the substrate
swap because they are truths about meaning, not artifacts of
implementation.

If a future agent (human or LLM) cannot derive the right shape
of a new component from these invariants, the invariants need
sharpening — not the shape weakening. That is the discipline
this report enforces.

---

## See Also

- `~/primary/ESSENCE.md` — workspace intent (upstream).
- `~/primary/repos/persona/ARCHITECTURE.md` — engine manager apex.
- `~/primary/repos/criome/ARCHITECTURE.md` — sema-ecosystem apex.
- `~/primary/protocols/orchestration.md` — role coordination.
- `~/primary/protocols/active-repositories.md` — active repo map.
- `~/primary/reports/designer/110-cluster-trust-runtime-placement.md`
  — scope discipline in action.
- `~/primary/reports/designer/112-day-review-2026-05-10.md` —
  recent work that this report synthesizes.
- `~/primary/reports/designer/113-actor-blocking-audit.md` — the
  blocking-plane discipline (one of the open seams).
- `~/primary/skills/actor-systems.md`, `~/primary/skills/kameo.md`
  — actor discipline (foundational).
- `~/primary/skills/contract-repo.md` — wire-contract discipline.
- `~/primary/skills/push-not-pull.md` — push-not-poll invariant.
- `~/primary/skills/designer.md` — the role this report is filed
  under; the discipline that shapes its form.
