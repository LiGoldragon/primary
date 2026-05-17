# 210 — Component triad: decisions, `Mutate` authority semantics, and orchestrate context

Date: 2026-05-17
Role: designer
Status: decisions landed + new authority-direction framing landed across
4 skills and 3 ARCH files. Q2 (persona-terminal CLI count)
investigation deferred to follow-up.

---

## 0 · TL;DR

User decisions on /209's three questions are settled and landed:

- **Q1 (skill location).** New `skills/component-triad.md` lives in
  the workspace skills directory. Kept short to maximize reading.
  Surfaced via a new "Skill importance" table at the top of
  `AGENTS.md` (tier 1: read this if you read nothing else).
  Cross-referenced from `skills/micro-components.md` and
  `skills/contract-repo.md`.
- **Q3 (Mutate semantics).** `Mutate` is **the authority verb** —
  top-down, *"change this; I do not care what you think"*. The
  issuer holds *possibly-mutated* state until the subordinate
  confirms; on the typed reply it transitions to *now-mutated* and
  may then issue the next downstream order. This is how Persona
  maintains correctness top-down. The framing is now canonical in
  `signal-core/ARCHITECTURE.md`, `skills/contract-repo.md`,
  `skills/component-triad.md`, `persona-mind/ARCHITECTURE.md`
  (§6.6, new), and `persona-router/ARCHITECTURE.md` (§2.5, new).
- **Q2 (persona-terminal CLI count).** Investigated. The repo ships
  **nine binaries** — two daemons, five control-plane Signal CLIs
  (`-capture`, `-type`, `-sessions`, `-resolve`, `-signal`), two
  data-plane attachers (`-view`, `-send`). The five control-plane
  CLIs should collapse to one `terminal` CLI with subcommands per
  the triad discipline; the two data-plane attachers are a
  legitimate exception (per `skills/component-triad.md` §"Named
  carve-outs"). Remedy deferred to a follow-up implementation
  report — flagged at §4 below.

New context surfaced during this pass:

- **`persona-orchestrate` is in design.** Second-designer-assistant's
  report 4 (2026-05-17) recommends a new component for orchestration
  *machinery* — spawning, supervision, scheduling, escalation,
  agent lifecycle — distinct from the orchestration *records* mind
  already owns. The Mutate authority chain in this report runs
  through it: `mind → orchestrate → router/harness`. Bead
  `primary-699g` (role:designer) tracks the contract-design work.

---

## 1 · What landed in this pass

Files claimed in `designer.lock` and edited. All edits are surgical —
the goal is *naming* the discipline that already exists in practice,
not rewriting any working code or shape.

| File | Change |
|---|---|
| `skills/component-triad.md` | **NEW.** ~200 lines. Names the triad shape, the three invariants, the six verbs (with authority direction), named carve-outs, witness tests, and the canonical mind → orchestrate → router authority-chain worked example. |
| `AGENTS.md` | Added "Skill importance" section between "Required reading" and "Nix store search is forbidden." Tiered table; component-triad is tier 1 — "if you can read only one skill, read that one." Explicit cross-cutting skill ranking, not duplicating per-role lists. |
| `skills/micro-components.md` | Added new step 4 to the "How" sequence: *"If the new capability is stateful, default to the triad shape."* Added cross-ref to component-triad in §"See also". |
| `skills/contract-repo.md` | Verb table extended with an **authority direction** column. `Mutate` row carries the authority-order semantics inline ("change this; I do not care what you think"; possibly-mutated → now-mutated on confirmation). Brief paragraph after the table names the worked Persona case and points at the triad skill. |
| `signal-core/ARCHITECTURE.md` | Paragraph added after the verb-order block naming the authority direction for each verb (Mutate/Retract top-down; Subscribe up-tree; Assert/Match/Validate direction-free). Cross-ref to the triad skill. |
| `persona-mind/ARCHITECTURE.md` | New §6.6 "Authority direction — `Mutate` flows down-tree": per-verb inbound/outbound table for mind; ChoreographyAdjudicator's `ChannelGrant`/`ChannelExtend`/`ChannelRetract` named as outbound `Mutate`/`Retract` orders; orchestrate component's place in the extended chain. |
| `persona-router/ARCHITECTURE.md` | New §2.5 "Authority direction — channel grants are inbound `Mutate` orders": names the router's discipline on receipt (obey, then confirm; hold possibly-mutated state until commit); distinguishes inbound Mutate (channel changes) from inbound Assert (message ingress). |

No code changes — these are all design-surface (skills, ARCH, agent
instructions). Operator-lane code work that the new discipline implies
(updating `signal-core/src/verb.rs` doc comments on the variants;
auditing each contract crate's `signal_channel!` for verb correctness)
is listed under §6 (Follow-ups).

---

## 2 · The Mutate authority chain — the corrected model

Persona's correctness is maintained **top-down via Mutate chains**.
The shape, in one sentence: *higher authority observes lower
components up-tree (via push subscriptions), decides, and issues
Mutate orders down-tree; each subordinate obeys and confirms; the
issuer transitions its own state from possibly-mutated to now-mutated
on the confirmation and only then advances to the next downstream
order*.

```mermaid
flowchart TB
    mind["persona-mind<br/>(authority root)"]
    orch["persona-orchestrate<br/>(spawning / supervision)<br/>— co-resident actor, separate contract"]
    router["persona-router<br/>(channel + delivery authority)"]
    harness["persona-harness<br/>(executes work)"]

    mind  -- "1. Mutate: SpawnAgent X in lane Y" --> orch
    orch  -- "2. ack mutated"                    --> mind
    mind  -- "3. Mutate: ChannelGrant (X ↔ peer)" --> router
    router -- "4. ack mutated"                   --> mind
    mind  -- "5. Mutate: SpawnHarness (with new permitted channels)" --> orch
    orch  -- "6. Mutate: spawn (typed permissions)" --> harness
    orch  -- "7. ack mutated"                    --> mind

    harness -. "Subscribe: harness lifecycle"        .-> mind
    router  -. "Subscribe: delivery / channel events" .-> mind
    orch    -. "Subscribe: agent lifecycle"           .-> mind
```

At each step:

- **The issuer holds possibly-mutated state.** Mind, at step 1, knows
  it has *ordered* the spawn but doesn't yet know it has *happened*.
  It does not consider the spawn fact until the typed confirmation
  arrives (step 2). Acting on possibly-mutated state would create a
  drift bug — mind would think the agent exists before orchestrate
  has actually spawned it.
- **The subordinate obeys and confirms.** Orchestrate does not
  adjudicate "should I spawn X?" — that authority lives in mind. It
  obeys the order, commits the effect, replies with the typed
  confirmation. (Failure modes: the subordinate may reply with a
  typed `Rejected` reason — that is a *typed failure*, not the
  subordinate's policy decision, and is bounded by the contract.)
- **Confirmation gates the next step.** Mind cannot issue step 3
  (install the channel grant) until step 2 (spawn confirmed)
  returns — otherwise it would install a channel for an agent that
  doesn't exist. The Mutate chain is what makes the *next* step
  safe.
- **Subscriptions flow the other direction.** Mind subscribes to
  orchestrate's `AgentLifecycle`, router's delivery / channel
  events, and harness's lifecycle — observation up-tree, authority
  down-tree.

This is why **`Mutate` is the authority verb** and `Assert` is not.
Assert is for *facts that entered the system from somewhere*: a
sensor observation, a user-typed message, a new event. The receiver
of an Assert records it without ordering anyone to do anything. Mutate
is for *orders issued downward from an authority root*: install this
channel, spawn this agent, retract this delegation. The verbs are
different because the *protocols* are different — for Assert, the
issuer has no authority over the receiver; for Mutate, the
authority-and-obedience relationship is the contract.

---

## 3 · Where `persona-orchestrate` fits

Second-designer-assistant's report 4 (the latest direction on this
component) recommends a new component for orchestration **machinery** —
spawning, supervision, scheduling, escalation, agent lifecycle —
distinct from the orchestration **records** that `persona-mind` already
owns. The deployment recommendation is co-resident actor tree in
mind's process initially; peel-apart later if needed (Nomad-flavored
simplicity).

Reading their report 4 alongside the user's Mutate-authority framing,
the picture sharpens:

- **`signal-persona-orchestrate`** (new contract) carries the typed
  vocabulary for *spawning / supervision / scheduling / escalation*.
  Examples from report 4: `SpawnAgent`, `AcquireScope`, `ReleaseScope`,
  `SuperviseAgent`, `EscalateBlockedWork`, with replies `AgentSpawned`,
  `ScopeAcquired`, `ScopeRejected`, `SupervisionAck`, `EscalationAck`,
  and emitted events `AgentLifecycle`, `ScopeContested`, `WorkReady`,
  `Escalation`.
- **Most of these are `Mutate`.** `SpawnAgent` orders the spawn.
  `AcquireScope` orders the conflict-resolution-then-claim flow.
  `SuperviseAgent` orders a restart policy registration. The
  read-shaped ones (`Escalation` consumption, `WorkReady` events,
  `AgentLifecycle` observation) are `Subscribe`. The query for
  current orchestration state is `Match`.
- **The authority chain extends through orchestrate.** Mind issues a
  `Mutate (SpawnAgent X)` to orchestrate; orchestrate executes (which
  may itself involve issuing `Mutate` orders down to harness for
  spawn and to router for channel grants); each subordinate confirms;
  orchestrate confirms back to mind; mind transitions its state and
  may issue the next order in its choreography.

When the persona-orchestrate contract is designed (bead `primary-699g`,
role:designer), the new framework gives the designer a sharp lens:
each request variant's `SignalVerb` should reflect whether it's an
order (`Mutate`/`Retract`), a fact-append (`Assert`), a one-shot read
(`Match`), or a stream (`Subscribe`). The `signal_channel!` macro
declares the verb per variant; the witness tests
(`<component>-signal-verb-mapping-covers-every-request-variant`) keep
the mapping honest.

The `(mind → orchestrate → router → harness)` chain in §2 is now the
canonical worked example in `skills/component-triad.md` §"Authority
chain — worked example". The triad skill is upstream of the
persona-orchestrate contract design — read it before designing the
contract.

---

## 4 · Q2 — `persona-terminal`'s ten binaries (correction + consolidation plan)

The `/209` audit quoted "five CLIs"; that came from reading the ARCH's
code map. The actual `Cargo.toml` ships **ten binaries** (I undercounted
twice — the ARCH code map was stale, and a `-validate-capture` helper
was also added). And — load-bearing correction to my earlier reply —
**the two-daemon shape is not legitimate either**: there should be
**one daemon**, full stop.

### The current ten

| Binary | Plane | Today's role |
|---|---|---|
| `persona-terminal-daemon` | daemon | PTY-owning daemon — **one process per active terminal session**, embeds `terminal-cell` library, binds `control.sock` + `data.sock` |
| `persona-terminal-supervisor` | daemon | Registry frontend — knows about all per-terminal daemons; forwards Signal frames by name resolution from component Sema |
| `persona-terminal-view` | data | viewer attaches to a terminal's `data.sock` (raw bytes) |
| `persona-terminal-send` | data | raw input sender on `data.sock` |
| `persona-terminal-capture` | control (Signal) | captures transcript bytes |
| `persona-terminal-type` | control (Signal) | injects programmatic input |
| `persona-terminal-sessions` | control (Signal, read-only) | session inspection |
| `persona-terminal-resolve` | control (Signal, read-only) | name → control socket path resolver |
| `persona-terminal-signal` | control (Signal) | generic Signal request client |
| `persona-terminal-validate-capture` | control (Signal) | capture-validator helper |

### Why the two-daemon shape is wrong

The current layering is:

1. **`terminal-cell` repo** ships its own `terminal-cell-daemon`
   binary — one daemon per terminal session, owns one PTY.
2. **`persona-terminal-daemon`** *also* owns one PTY per process —
   it embeds the `terminal-cell` library and spawns its own
   `TerminalCell` actor. Per the persona-terminal ARCH §1.5:
   *"`persona-terminal-daemon` is a PTY-owning daemon. It embeds the
   `terminal_cell` library to spawn a `TerminalCell` actor… binds
   `--control-socket` and `--data-socket`."* That's **one
   persona-terminal-daemon process per terminal session**.
3. **`persona-terminal-supervisor`** is a *registry frontend* —
   binds one `signal-persona-terminal` socket, resolves
   names from component Sema, forwards Signal frames to whichever
   per-terminal daemon is named.

So there are conceptually three layers of daemon: terminal-cell's
own daemon binary, one persona-terminal-daemon per session, and one
supervisor knowing about all of them. The **supervisor exists
because the architecture made each terminal its own daemon, which
required a registry to find them.** Collapse the per-terminal
daemons and the supervisor's reason to exist evaporates.

The triad discipline says **one daemon per component**. A terminal
session is not a component — it is *state the component manages*,
exactly like a work-graph item in persona-mind, a channel in
persona-router, or a message in persona-message. None of those
spawn one daemon per work item; the daemon holds the state in
sema-engine + per-state actors.

### What the right `persona-terminal` daemon does

One daemon for the whole component:

1. **Binds the persona-terminal Signal control socket** — one
   socket for the entire component. Receives
   `signal-persona-terminal` frames from any client. Resolves
   `TerminalName → ActorRef<TerminalCell>` *in-process* and forwards
   the frame to that actor's mailbox.
2. **Maintains the terminal-session registry in its own
   `sema-engine` database** — names, child PIDs, creation time,
   prompt-pattern registrations, input-gate state history, viewer
   attachment state, session-archive records. Same shape as every
   other triad daemon's durable state.
3. **Spawns one Kameo `TerminalCell` actor per active terminal
   session.** Each actor owns one child process group, one PTY
   master fd, one transcript log (append-only via the existing
   `TranscriptScriber` worker pattern), one viewer attachment, one
   prompt-pattern + input-gate state, the per-terminal worker
   lifecycle (output reader, viewer fanout, scriber, input writer).
   `terminal-cell` is consumed as a *library only*, providing
   typed PTY primitives.
4. **Binds one data socket per active terminal** — these are
   short-lived, per-actor sockets at e.g.
   `${XDG_RUNTIME_DIR}/persona-terminal/<terminal-name>/data.sock`.
   The viewer attacher dials the named terminal's data socket
   directly; raw bytes pass through `TerminalInputWriter` /
   `ViewerFanout` as today. The data plane stays out of the actor
   mailbox per `terminal-cell/ARCHITECTURE.md` §3.2 "Data-plane
   latency".
5. **Answers `signal-persona::SupervisionRequest` from the persona
   engine manager** via a canonical `SupervisionPhase` actor in
   the daemon's tree (same as every other Persona triad daemon).
6. **Handles cross-terminal coordination** that today has no
   home: focus tracking, broadcast events, restart-all semantics.
   Each is mailbox-local in the consolidated daemon; cross-process
   coordination disappears as a problem.

### Why crash-isolation does not justify the per-terminal daemon

The most plausible argument for per-terminal daemons would be OS-level
process isolation — if one terminal's PTY hangs or its actor panics,
the others survive. Kameo's supervision discipline already provides
crash isolation **inside** one daemon: a panicking actor is restarted
under its supervisor; other actors are unaffected. PTY-level
pathologies (runaway child, syscall hang) cause the *worker thread*
inside the actor to misbehave, not the whole daemon — and the existing
worker-lifecycle observation (`TerminalWorkerLifecycle` events per
terminal-cell ARCH §3.8) is the mechanism that surfaces these as
queryable actor state.

If a *specific* terminal needs OS-level isolation (e.g., for security
reasons — a session running as a different user), that's a deployment
choice for *that one terminal*, expressed via Kameo's
spawn-in-subprocess facility or an equivalent IPC plumbing. It's not
the default architecture. The default is one daemon, many TerminalCell
actors.

### The consolidated binary count: 3 (down from 10)

| Binary | Plane | Role |
|---|---|---|
| `persona-terminal-daemon` | daemon | The one daemon. Binds the component's Signal control socket, owns the sema-engine registry, supervises N TerminalCell actors. |
| `persona-terminal` | control (Signal) | The one CLI. Accepts any `signal-persona-terminal` request as NOTA on argv/stdin; prints the typed NOTA reply. Subsumes `capture`, `type`, `sessions`, `resolve`, `signal`, `validate-capture`. |
| `persona-terminal-view` | data | Data-plane viewer attacher (raw bytes, named carve-out per triad §"Named carve-outs"). May also absorb `send` if the unified attach is interactive. |

`terminal-cell` becomes a **library only** at the production-Persona
layer. Its own daemon binary (`terminal-cell-daemon`) can stay for
independent testing of the PTY primitive in isolation, but it's not
on the production Persona path.

### Remedy proposal

This is a substantial implementation arc, not a fit for this report's
pass. The right shape is a focused designer report (this one is
broader) plus an implementation bead. The shape:

1. **Designer report** (next): "persona-terminal consolidation —
   one daemon per component" — names the actor topology, the
   sema-engine registry shape, the per-terminal data-socket
   lifecycle, the migration sequence for existing persona-terminal
   consumers (router, harness, introspect).
2. **Bead** (after designer report lands): `role:operator` for the
   consolidation work — embed terminal-cell as library only; collapse
   ten binaries to three; retire the supervisor binary and its
   registry-frontend code; convert the per-terminal daemon's
   lifecycle into per-actor Kameo supervision.
3. **Witness tests** added in lockstep:
   `persona-terminal-component-has-exactly-one-daemon-binary`,
   `persona-terminal-cli-has-exactly-one-signal-peer`,
   `persona-terminal-daemon-supervises-one-actor-per-terminal-session`.

I will draft the designer report as the natural next deliverable
unless you redirect.

---

## 5 · Where we're going — the architecture as a whole

The pieces now name themselves:

- **The triad** is the universal shape for every stateful component
  (`skills/component-triad.md`).
- **`signal-core`** is the wire kernel; six closed verb roots
  encoding both *what kind of operation* and *which authority
  direction*.
- **`Mutate`** is the authority verb. Persona's correctness flows
  top-down via Mutate chains; each subordinate obeys and confirms;
  the issuer advances on confirmation.
- **`Subscribe`** is the observation verb. Push, not poll. Authority
  observes up-tree before issuing orders down-tree.
- **`Assert`** is the new-fact verb. No authority chain — just *a
  typed fact entered the system*.
- **The CLI is a bridge**, not a destination. It exists to translate
  human/agent NOTA-sugar into typed Signal until peers can speak
  Signal directly. Eventually obsolete.

As new components land, they fit:

- **`persona-orchestrate`** (bead `primary-699g`) sits in the
  authority chain between mind and the runtime components
  (router/harness/future executors).
- **Raw-LLM-API executor** (mentioned in second-designer-assistant
  report 4) lands as a sibling of `persona-harness` under
  orchestrate's spawn authority — `orchestrate → Mutate (Spawn …
  RawLlm) → raw-llm-executor`.
- **Future components** (auth policy engine, audit, schedulers)
  similarly slot in by their position in the authority chain (who
  observes them; who orders them) and the named triad shape.

Each new component's ARCH should **cite the triad skill** and only
state component-specific carve-outs — not restate the universal
invariants. The duplication that exists today across the active
component ARCHs (per /209) should be cleaned up incrementally as
those ARCHs are next touched; not as a blanket sweep.

---

## 6 · Follow-ups (open work)

Filed informally here; convert to beads as the user prioritizes.

| Follow-up | Lane | Why |
|---|---|---|
| Update `signal-core/src/verb.rs` doc comments on each `SignalVerb` variant to reflect the authority direction (per the new ARCH paragraph) | operator | Designer drafts the shape (done in ARCH); operator owns the Rust source per `skills/designer.md`. |
| `signal-criome` per-variant verb mapping — verify in source + document in `signal-criome/ARCHITECTURE.md` | designer-assistant or operator | Gap surfaced in /209 §6; the triad now names the witness test that catches this. |
| `persona-terminal` CLI consolidation (5 control-plane CLIs → 1) | operator | Per §4 above. |
| Audit each existing contract crate's `signal_channel!` for verb correctness against the new framing (especially: anything currently mapped `Assert` whose semantics are actually "order the receiver to change something" should be `Mutate`) | designer-assistant | The reframing of Mutate as authority order means some existing classifications may need adjustment. Most likely candidates: anything in `signal-persona-mind` that mind ISSUES (channel grants, future spawn orders) vs anything mind RECEIVES (role claims, activity submissions). |
| `persona-orchestrate` contract design (bead `primary-699g`) | designer | The triad skill is now upstream of this; ready to consume. |
| Component ARCH duplication cleanup — let each new ARCH touch cite the triad skill and trim restated invariants | per-lane as ARCHs are touched | No blanket sweep; opportunistic during normal work. |

---

## 7 · Coordination

`orchestrate/system-specialist.lock` was idle at the start of this
pass (the SS work on horizon-leaner-shape ARCH alignment had been
released). The lojix/signal-lojix worktree work continues independently
and is now a **witness of the triad** — `signal-lojix` already
declares five SignalVerb mappings inside one channel, and
`lojix-daemon` + `lojix` CLI is the cleanest exemplar of the triad
shape.

`second-designer-assistant`'s work on `persona-orchestrate` (reports
1-4 in their lane subdirectory; latest is report 4) continues as the
next major design surface. The triad + Mutate authority framing
landed in this pass are inputs to that design. Their report 4
recommends a co-resident-actor deployment shape; this report doesn't
contradict that.

`designer.lock` releases after this report and the commit push land.

---

## 8 · See also

- `~/primary/ESSENCE.md` (intent; upstream of everything below).
- `~/primary/AGENTS.md` §"Skill importance" (the new tier table
  surfaces the triad skill at tier 1).
- `~/primary/skills/component-triad.md` (the new skill this report
  motivated).
- `~/primary/skills/contract-repo.md` §"Signal is the database
  language" + verb table (now with authority-direction column).
- `~/primary/skills/micro-components.md` §"How" step 4 + §"See
  also" (cross-ref to triad).
- `~/primary/skills/push-not-pull.md` (the observation half of the
  authority chain).
- `~/primary/skills/architectural-truth-tests.md` (the witness-test
  shape every triad invariant takes).
- `/git/github.com/LiGoldragon/signal-core/ARCHITECTURE.md`
  (authority-direction paragraph; the wire kernel).
- `/git/github.com/LiGoldragon/persona-mind/ARCHITECTURE.md` §6.6
  ("Authority direction — `Mutate` flows down-tree").
- `/git/github.com/LiGoldragon/persona-router/ARCHITECTURE.md` §2.5
  ("Authority direction — channel grants are inbound `Mutate`
  orders").
- `~/primary/reports/designer/209-component-triad-daemon-cli-contract-2026-05-17.md`
  (the audit that this report's decisions resolve).
- `~/primary/reports/second-designer-assistant/4-persona-orchestrate-control-plane-2026-05-17.md`
  (the orchestrate component recommendation that this report's
  Mutate framing slots into).
- `~/primary/protocols/active-repositories.md` §"Replacement Stack"
  (the active multi-repo arc — horizon-leaner-shape — that the lojix
  triad lives on).
- Bead `primary-699g` (role:designer) — design
  `signal-persona-orchestrate` contract + `persona-orchestrate`
  component (the natural next surface).
- Bead `primary-68cb` (role:operator) — Rust port of
  `tools/orchestrate` as thin `signal-persona-mind` client (a
  parallel arc; sec-DA report 4 narrows its scope).
