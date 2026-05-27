# Skill — component triad (daemon + working signal + policy signal)

*The universal shape for every stateful capability in the workspace.
Five invariants and one argument rule determine whether a design is
in this system at all. Read this once; recognise the shape in every
component's `ARCHITECTURE.md`.*

## Two triads — distinguish them

The workspace uses "triad" in two senses; both apply at different layers.

| Triad | Scope | Members |
|---|---|---|
| **Repo triad** (this skill) | Packaging — how a component is laid out across repositories | `<component>` + `signal-<component>` + `core-signal-<component>` |
| **Runtime triad** | Logic — what happens INSIDE the daemon (three schema-driven planes) | **Signal** + **Nexus** + **SEMA** |

The runtime triad lives INSIDE the `<component>` daemon repo. This skill
covers the repo triad below; the runtime triad gets its own section at
the bottom of this file. Per psyche record 856; refined by record 964
(Executor renamed to Nexus; all three planes are schema-driven).

## The shape

Every stateful capability is a triad of three repositories:

```
<component>/                      runtime
  src/lib.rs                      component library
  src/bin/<name>-daemon.rs        long-lived daemon
  src/bin/<name>.rs               thin CLI client
  bootstrap-policy.nota           first-start policy declaration
signal-<component>/               ordinary wire vocabulary
  schema/lib.schema               schema-derived ordinary signal
  src/schema/*.rs                 generated signal types
  tests/round_trip.rs             rkyv + NOTA round-trips
owner-signal-<component>/         owner-only authority/configuration vocabulary
  schema/lib.schema               schema-derived owner signal
  src/schema/*.rs                 generated owner signal types
  tests/round_trip.rs             rkyv + NOTA round-trips
```

The contract crates carry no runtime, no actors, no `tokio` — they
declare typed wire vocabulary and generated method surfaces, and
nothing else. The runtime crate
owns the daemon, the CLI, and the typed sema-engine state. The
split is filesystem-enforced (per `skills/micro-components.md`).
The CLI is bundled runtime machinery: the daemon's thin first client,
not one of the triad's three legs.

## Component binary naming

A component has two binaries: a CLI half and a daemon half. The
component name (`persona`, `spirit`, `harness`, `orchestrator`,
`chroma`, `chronos`) names the **role** of the whole — it is not
itself the name of any single binary. The binaries are:

- **CLI binary** — named `<component>`. The thin Signal client.
- **Daemon binary** — named `<component>-daemon`. The long-lived
  process holding the sema-engine state.

So the `persona` component is two binaries — `persona` (CLI) and
`persona-daemon` (daemon). The `spirit` component is `spirit` (CLI)
and `spirit-daemon` (daemon). Same shape for `harness`,
`orchestrator`, `chroma`, `chronos`, and every future component.

The CLI binary takes the unprefixed role-name because that is what
the human or peer agent types most often; the daemon binary takes
the `-daemon` suffix because it names the long-lived process and is
typed only by launch infrastructure. Both halves together comprise
the component (per intent records 215 + 216 + 270).

### Repository name vs binary name

The repository name follows the component name. When the repository
carries a disambiguation prefix because the component sits inside a
larger system (e.g. `persona-spirit` to mark spirit as the
persona-system's spirit, distinct from any other future spirit), the
binaries inside it follow the **repository's** component identity:

- Repository `persona-spirit` ships binaries `spirit` (CLI) and
  `persona-spirit-daemon` (daemon).
- Repository `persona-mind` ships a `mind` CLI; the daemon (when it
  lands) is `persona-mind-daemon`.

The CLI keeps the short role-name because users type it; the daemon
keeps the full repo-prefixed name because two persona-system
daemons running side by side need disambiguation in process listings,
socket paths, and systemd units.

### Persona harness wrapping — the `persona-<agent>` family

`persona-codex`, `persona-pi`, `persona-claude` are persona-wrapping
harnesses. The `persona-` prefix marks them as components that wrap
an external agent runtime (Codex, the Pi runtime, Claude Code) into
the persona system. The unprefixed `persona` is reserved for the
engine-manager component (per intent 215). So:

- `persona` (repo + CLI + daemon) — the engine-manager. CLI binary
  `persona`, daemon binary `persona-daemon`.
- `persona-pi` (repo + CLI + daemon) — the Pi-runtime-wrapping
  harness. CLI binary `pi`, daemon binary `persona-pi-daemon`.
- `persona-codex`, `persona-claude` — same shape: CLI `<agent>`,
  daemon `persona-<agent>-daemon`.

### Binary naming table

| Component | Repo | CLI binary | Daemon binary |
|---|---|---|---|
| persona | `persona` | `persona` | `persona-daemon` |
| persona-spirit | `persona-spirit` | `spirit` | `persona-spirit-daemon` |
| persona-mind | `persona-mind` | `mind` | `persona-mind-daemon` |
| persona-router | `persona-router` | `router` | `persona-router-daemon` |
| persona-orchestrate | `persona-orchestrate` | `orchestrate` | `persona-orchestrate-daemon` |
| persona-harness | `persona-harness` | `harness` | `persona-harness-daemon` |
| persona-system | `persona-system` | `system` | `persona-system-daemon` |
| persona-message | `persona-message` | `message` | `persona-message-daemon` |
| persona-terminal | `persona-terminal` | `terminal` | `persona-terminal-daemon` |
| persona-pi | `persona-pi` | `pi` | `persona-pi-daemon` |
| orchestrator | `orchestrator` | `orchestrator` | `orchestrator-daemon` |
| chroma | `chroma` | `chroma` | `chroma-daemon` |
| chronos | `chronos` | `chronos` | `chronos-daemon` |

A standalone top-level component (no parent system) reuses the
component-name for both the repo and the CLI binary; the daemon
binary appends `-daemon`. A child component inside a parent system
(the persona-system family above) carries the parent prefix in the
repo and daemon names; the CLI keeps the short role-name.

### What this is NOT

- The role-name on its own (`persona`, `spirit`, `harness`) is not a
  binary unless that binary is the CLI. There is no binary called
  `persona` that is the daemon; the daemon is `persona-daemon`.
- A `<component>-cli` suffix is not used (the unprefixed name IS the
  CLI). `lojix-cli` is a transitional carry-over name, not the
  convention.
- A `<component>-server` or `<component>-service` suffix is not
  used; the daemon binary always ends in `-daemon`.

## Vocabulary

Use these words consistently:

- **Component triad** — `<component>` runtime repo plus two signal
  contract repos: `signal-<component>` and
  `owner-signal-<component>`.
- **Working signal** / **working contract** —
  `signal-<component>`, the ordinary peer-callable contract.
- **Policy signal** / **owner contract** —
  `owner-signal-<component>`, the owner-only authority and
  configuration contract.
- **Signal types** — the schema-generated data types declared in
  either signal contract: operation roots, payload records, replies,
  rejection reasons, filters, mail events, stream tokens, and related
  newtypes.
- **Signal tree** — the whole typed schema shape: which relation
  families exist, what the root enums are, how payloads nest, which
  replies and events correspond, and whether the names reveal the
  right logic separation.
- **Policy state** — daemon-owned durable rules/configuration,
  bootstrapped once from `bootstrap-policy.nota` and then changed
  only through owner-signal authority.
- **Working state** — daemon-owned durable operational records
  produced by ordinary operation, with owner-signal mutations only
  where owner authority is required.

Names in signal types are architecture. If a contract name feels
wrong, audit the signal tree before writing more consumers; the name
may be exposing a misplaced relation, an over-broad root enum, or a
policy/working boundary error.

## The five invariants

Each invariant becomes a witness test (per
`skills/architectural-truth-tests.md`). The test names appear in the
table at the end of this section.

### 1. The CLI has exactly one Signal peer — its own daemon

The CLI is a text bridge into the typed wire for *one* daemon's
contract. It cannot multiplex across daemons, open **any** durable
database, open another component's socket, or speak its own parallel
protocol. "Any database" includes the component's own redb/sema store:
the daemon is the only process that opens durable component state.
The CLI exists because humans and early agents need a text-to-Signal
adapter; once peer daemons speak Signal directly to each other (which
they already do — `persona-introspect`'s daemon queries
`persona-router` over `signal-persona-router`), the CLI is no longer
load-bearing for that path and retires.

The CLI is **eventually obsolete machinery**. Keep CLI-side logic thin
accordingly. A "temporary direct-store CLI" is not a prototype; it is
a triad violation. If the daemon socket is not implemented yet, the
CLI fails closed or remains unshipped rather than opening the store.

### 2. The daemon's external surface is exclusively `signal-frame` frames

No `serde_json` socket, no NOTA on the wire between components, no
parallel control protocol. NOTA exists at three named projection edges
— CLI argv/stdin, daemon ↔ harness terminal, audit/debug dumps —
never inter-component.

A daemon may be a Signal client of any number of peer daemons (this is
how daemons compose); the "exactly one peer" constraint applies to
CLIs, not daemons. What no daemon may do is bypass another daemon's
contract — no opening another component's redb, no shared in-memory
state.

### 3. Verbs come in three layers

A component contract speaks three distinct languages, each with
its own concern:

| Layer | Owns | Examples |
|---|---|---|
| **Contract Operation** (external, on the wire) | the domain action the caller invokes | `Submit(Message)`, `Query(Selection)`, `Configure(Configuration)`, `State(Statement)` |
| **Component Command** (internal, per-daemon) | the daemon's typed executable record | `LedgerCommand::RecordEvent(EventRecord)`, `SpiritCommand::AssertEntry(Entry)` |
| **Sema Operation** (cross-component classification) | the universal payloadless class label for observation/introspection | `Assert`, `Mutate`, `Retract`, `Match`, `Subscribe`, `Validate` |

The contract crate's schema names the Layer-1 operations (per
`skills/naming.md` verb-form rule). The daemon owns its Layer-2
commands, but those commands are also schema-authored objects, not
hand-written parallel enums hidden inside daemon code. The six Sema
classes (Layer 3) live in `signal-sema` as
a **payloadless** enum used by observation only — never
executable, never wire-payload-carrying. Component Commands
project to Sema classes via a `ToSemaOperation` trait so
cross-component observation can filter on classification ("all
Asserts across the workspace") without knowing per-daemon
command payloads.

The six Sema classes and their semantic meanings (the same
table, now framed as classification vocabulary):

| Class | Direction | What kind of state-action |
|---|---|---|
| `Assert` | bottom-up or peer | append a new typed fact / event / row |
| `Mutate` | top-down authority order — *"change this, I don't care what you think"*. Authority issues; subordinate obeys and confirms | replace / transition a record at stable identity |
| `Retract` | top-down authority order | tombstone / remove a typed fact |
| `Match` | any direction | one-shot pattern / range / key query |
| `Subscribe` | observer ↔ producer | initial state + commit-deltas (push, not poll) |
| `Validate` | any direction | dry-run an operation without commit |

**Mutate is the authority verb.** When mind issues a `Mutate` to
orchestrate, mind is *ordering* a change, not asserting a fact. The
recipient obeys and confirms; the issuer transitions its own state
from *possibly-mutated* to *now-mutated* on the confirmation, and only
then proceeds to any downstream order. The Mutate chain maintains
correctness top-down.

**Subscribe flows the other way.** Authority observes state via push-
subscriptions from down-tree (per `skills/push-not-pull.md`), decides,
orders via Mutate down-tree. Observation up, authority down.

**Assert is for new facts.** When a CLI user sends a message, the
component asserts the message exists. When a sensor records an
observation, it asserts. No authority chain — just a new typed fact
entered the system.

### 4. Two authority tiers — both part of the triad

A stateful component has two typed authority surfaces, both part of
the triad:

- **`signal-<component>`** — ordinary peer surface. Variants here are
  callable by any authenticated peer.
- **`owner-signal-<component>`** — owner-only authority/configuration
  surface. Variants here are callable only by the component's owner
  (the entity above it in the workspace's owner graph — e.g., mind
  owns orchestrate; orchestrate owns router and harness).

Each surface gets its own typed listener actor inside the daemon and
its own permission-separated socket. Per-component Unix users/groups
enforce the owner socket as an OS security boundary; same-UID prototype
is for author-only development.

**Contracts split by who-can-call, not by what-state-they-touch.**
Variants in the owner contract are owner-only; variants in the
ordinary contract are peer-callable. *Both contracts can carry
`Mutate` variants* against any kind of state — what places a variant
in one contract rather than the other is whether the caller needs
owner authority. A peer-callable `Mutate` (peer mutates a record they
own, like releasing their own claim) lives in the ordinary contract;
an owner-only `Mutate` (mind orders orchestrate to spawn an agent)
lives in the owner contract.

The two surfaces ship together. A daemon with only the ordinary
surface is not yet triad-shaped — the next implementation arc for any
component must deliver both. Privileged mutable configuration enters
through the owner-signal actor; there is no separate privileged side
channel and no "static local config first, owner-signal later"
implementation path.

**Proposed rename: `owner-signal` → `meta-signal`.** Per Spirit
records 290 + 299, the psyche prefers `meta-signal` over
`owner-signal` for the policy contract name. The rename is
**tentative direction, not a completed vocabulary change** —
record 293 explicitly directs that `owner-signal` remains the
active naming convention until an explicit rename pass lands.
Continue using `owner-signal-<component>` in new repos, ARCH
files, and code; do not pre-rename. When the rename lands, the
cascade resembles the persona- prefix removal (Spirit record 280)
and lands as its own coordinated bead.

### 5. Policy state and working state — both in one sema-engine DB

Every triad daemon's durable state splits into two typed categories,
both living in the same `<component>.redb` opened through
`sema-engine`:

**Policy state** — the rules the daemon enforces.
- Source of truth: the daemon's sema tables, after bootstrap.
- How it changes: only owner-signal `Mutate` verbs (variants in the
  owner contract).
- First-start population: from `bootstrap-policy.nota` in the
  component's repo. The daemon reads this file exactly once — on first
  start, when the policy tables are empty — writes the declared
  records as if they had been Mutated, then records bootstrap-complete
  in a one-shot table. Never reads the file again.
- After first start: changes to `bootstrap-policy.nota` are ignored.
  Policy changes only via owner `Mutate`. Factory reset is deliberate
  — blow away the redb (the daemon re-bootstraps), or issue an explicit
  reset verb.
- Examples (orchestrate): `lane_registry`, `scheduling_policy`,
  `supervision_policies`.

**Working state** — the records produced by operation.
- Source of truth: the daemon's sema tables, from operation.
- How it changes: per the variants in either contract — some peer
  `Assert`s (e.g. activity submission), some peer `Mutate`s of records
  the peer owns (e.g. releasing their own claim), some owner `Mutate`s
  (e.g. mind ordering a run stopped).
- First-start population: empty. Working state never bootstraps from
  file.
- Examples (orchestrate): `claims`, `activities`, `agent_runs`,
  `spawn_plans`, `scope_acquisitions`, `escalation_state`.

The split is by table category — table name prefixes or a sema
table-set declaration — not by storage backend. One sema-engine DB
per component; two categories of table within.

This invariant settles a recurring design question: *"how does the
daemon get its config on first start?"* The answer is bootstrap-once
from a declared NOTA file in the repo; thereafter, owner Mutate is
the only path. The bootstrap file is a one-shot seed, not source-of-
truth.

### Witness tests

| Test | Proves invariant |
|---|---|
| `<component>-cli-accepts-one-argument-and-prints-one-nota-reply` | 1 |
| `<component>-cli-has-exactly-one-signal-peer` | 1 |
| `<component>-cli-cannot-open-any-database-or-peer-socket` | 1 |
| `<component>-daemon-rejects-non-signal-traffic-on-its-socket` | 2 |
| `<component>-signal-verb-mapping-covers-every-request-variant` | 3 |
| `<component>-owner-socket-rejects-ordinary-frame` | 4 |
| `<component>-ordinary-socket-rejects-owner-frame` | 4 |
| `<component>-owner-socket-mode-matches-spawn-envelope` | 4 |
| `<component>-policy-tables-empty-on-first-start-trigger-bootstrap` | 5 |
| `<component>-bootstrap-runs-exactly-once` | 5 |
| `<component>-policy-changes-after-bootstrap-only-via-owner-signal` | 5 |
| `<component>-working-tables-never-read-bootstrap-file` | 5 |
| `<component>-binary-rejects-flag-style-arguments` | argument rule below |

## The single argument rule

Every component binary — CLI and daemon both — takes exactly one
argument on argv. That argument is one of:

- An **inline NOTA argument**: `persona-orchestrate "(RoleClaim ...)"`
- A path to a **NOTA file**: `persona-orchestrate ./request.nota`
- A path to a **signal-encoded file** (rkyv binary):
  `persona-orchestrate-daemon ./config.signal`

Inline NOTA in a shell is wrapped in double quotes around the whole
NOTA object. NOTA strings use `[text]` or `[|text|]`, not `"` string
delimiters, so the shell double quotes remain available as the clean
single-argument boundary. Do not teach agents to wrap inline NOTA in
single quotes as the normal form.

**No flags.** No `--verbose`, no `--format=json`, no `--config=path`,
no positional second arguments. If the binary needs additional
configuration, that configuration is a field of the NOTA payload —
the contract's NOTA schema is the only source of truth for what
arguments mean.

For the CLI: the argument is a NOTA request record matching one of
the request variants in the component's ordinary or owner contract.

For the daemon: the argument is a NOTA config record naming the
daemon's identity, socket paths, redb path, and the path to its
`bootstrap-policy.nota`. The config record's schema lives in
`signal-<component>` (or a small `<component>-config` crate if it
needs to be shared between daemon and a deploy helper).

If a new argument shape is needed, the contract's NOTA schema gets a
new field or variant — not a new CLI flag. This is the rule that
keeps NOTA the single language for invoking the workspace: the
moment one binary starts accepting flags, the workspace fragments
into ad-hoc CLIs.

## Help operations — discovery through NOTA, not through flags

Because the single-argument rule forbids `--help`, every component
carries discovery through the NOTA channel like any other operation.
Per Spirit record 263, **every component supports the two Help
operations** in its ordinary contract:

- **`(Help Main)`** — top-level discovery. Reply lists the
  component's operations with a one-line description of each and
  the canonical NOTA shape for invoking them.
- **`(Help (Verb <name>))`** — verb-level detail. Reply carries
  the typed schema for one named operation: payload fields and
  their types, a worked example invocation, and the reply shape.

Help operations follow the same discipline as every other
operation: positional NOTA records, single-argument, daemon-side
implementation, typed reply. No flags, no special parsing.

The cleanest implementation direction is **auto-injection** via
the `signal_channel!` macro — the macro emits the Help arm into
every contract automatically, with help text derived from the
existing Rust doc comments on operation variants. Every contract
picks Help up on the next rebuild; no per-contract boilerplate.

## Named carve-outs

These look like triad violations but aren't. Each is *narrow*; do not
extend the pattern of carve-outs.

1. **Pure libraries don't need a daemon.** `signal-frame`, `signal-sema`, `sema`,
   `sema-engine`, `horizon-rs` (projection library) own no state and
   cross no process; the triad does not apply. A test CLI like
   `horizon-cli` for ad-hoc projection is convenience, not a triad.

2. **Data-plane bytes that cannot afford Signal framing.** When a
   component has a high-bandwidth byte path (raw PTY bytes, video,
   audio), the data plane is a separate socket outside the triad. The
   control plane still follows the triad. Canonical example:
   `persona-terminal`'s `control.sock` (Signal) vs `data.sock` (raw
   viewer bytes); raw bytes flow viewer ↔ `terminal-cell`'s
   `data.sock` directly. Document the exception in the component's
   ARCH.

3. **A daemon may be a Signal client of any number of peer daemons.**
   `persona-introspect`'s daemon opens client connections to
   `persona-router`, `persona-terminal`, `persona-manager` over their
   contracts. This is the right shape. The CLI's "exactly one peer"
   constraint does not extend to daemons — fanning out across peers
   is how daemons compose.

## Compile-time module index for triad-internal dispatch

When a daemon dispatches across a static set of internal modules
(sema-upgrade across per-component migrations; a parser across
per-grammar handlers; a codec across per-version translators),
prefer a **compile-time index** over runtime registration. Each row
is an explicit submodule reference plus a function pointer:

```rust
pub struct MigrationModule {
    supported: SupportedMigration,
    run: fn(&Attempt) -> Result<ModuleResult, RejectionReason>,
}
pub struct MigrationIndex { modules: Vec<MigrationModule> }

impl MigrationIndex {
    pub fn prototype() -> Self {
        Self { modules: vec![
            MigrationModule {
                supported: persona_spirit::version_0_1_0_to_0_1_1::supported(),
                run: persona_spirit::version_0_1_0_to_0_1_1::run,
            },
            // each new module = one row added here
        ]}
    }
}
```

The index reads as the daemon's literal catalogue: adding a module
is a single-file edit; no dynamic loading, no `Box<dyn Trait>`, no
inventory crate, no plugin protocol. Owner-side policy (which
dispatches are enabled or blocked) is the daemon's overlay on top:
the index says "what the binary knows how to do," the owner-signal
vocabulary says "what the binary is permitted to do."

## Authority chain — worked example

Persona's correctness is maintained top-down via Mutate chains.
When mind decides a new agent run needs a channel grant so it can
talk to the router:

```mermaid
flowchart TB
    mind["persona-mind<br/>(authority root)"]
    orch["persona-orchestrate<br/>(spawning / supervision)"]
    router["persona-router<br/>(channel authority)"]
    harness["persona-harness<br/>(executes work)"]

    mind  -- "1. Mutate: spawn agent X in lane Y" --> orch
    orch  -- "2. ack mutated"                     --> mind
    mind  -- "3. Mutate: install channel grant"   --> router
    router -- "4. ack mutated"                     --> mind
    mind  -- "5. Mutate: spawn harness w/ rights" --> orch
    orch  -- "6. spawn"                            --> harness
    orch  -- "7. ack mutated"                     --> mind

    harness -. "Subscribe: lifecycle events"  .-> mind
    router  -. "Subscribe: delivery events"   .-> mind
    orch    -. "Subscribe: agent lifecycle"   .-> mind
```

At each Mutate step the issuer holds *possibly-mutated* state until
the ack arrives; only then does it advance to the next order. Replies
are not opinions — they are confirmations. The authority chain makes
the next step safe: the harness is not spawned with channel rights
until the router has confirmed the channel exists.

### Partial-failure semantics — commit-first-success-and-record-divergence

When an issuer's Mutate chain crosses multiple downstream
components (e.g. mind issues a Mutate that orchestrate
propagates to router *and* harness for a single logical
operation), the partial-failure rule is:

**The issuer commits on the first success and records the
divergence on failure.** It does not roll back the successful
leg; it does not stall waiting for an all-or-nothing two-phase
commit; it advances on the success and records the failed-leg
state as a divergence row that downstream tooling (introspect,
the recovery agent) can reconcile.

This matches the precedent established for version-handover
between main and next: spirit records 180 + 183 settled that
*"operations main cannot process at all are acceptable; dev does
the op and main records only the divergence"* and *"when next
catastrophically fails, main recovers what it can from the
original message via partial application; preserves caller intent
across version-divergence failures."* The shape generalizes
beyond version-handover to any Mutate chain that fans out: the
issuer commits the legs that succeeded and records what diverged,
trusting the introspect plane and recovery agent to surface and
heal the divergence later.

Rationale: an issuer that rolls back on first downstream failure
must hold inverse-mutate logic for every Mutate it issues, and
must succeed in applying the inverse against a remote daemon
that may itself be unhealthy — turning partial-failure into a
distributed-rollback problem with worse failure modes than the
original. An issuer that runs two-phase commit pays the
synchronization cost on every Mutate, slowing the common-case
all-success path for the rare partial-failure case. The commit-
first-success path keeps the common-case fast and pays the
reconciliation cost only where divergence actually occurred.

The downstream legs are responsible for typed Unimplemented or
typed failure replies per the skeleton-honesty rule (per
`signal-persona/ARCHITECTURE.md` §"Skeleton honesty"). The
issuer's "record divergence on failure" relies on those typed
replies — a silent drop or panic breaks the partial-failure
protocol.

## When this skill applies

- **Designing a new stateful component.** Default to the triad. If
  the shape doesn't fit, name which carve-out justifies the
  divergence — or escalate to the user before deviating.
- **Auditing an existing component.** Check it against the five
  invariants and the single-argument rule. Surface deviations in a
  report.
- **Reading a component's `ARCHITECTURE.md`.** The ARCH cites this
  skill and only states component-specific carve-outs — never restates
  the universal invariants.

## See also

- `~/primary/ESSENCE.md` §"Micro-components" — the one-capability-
  one-crate-one-repo rule the triad applies on top of.
- `~/primary/skills/micro-components.md` — filesystem-enforced
  per-capability boundary; the triad is the *shape inside the
  boundary*.
- `~/primary/skills/contract-repo.md` — what lives in a `signal-*`
  contract crate; the verb spine; the boundary table for where NOTA
  renders.
- `~/primary/skills/actor-systems.md` §"Runtime roots are actors" —
  the daemon's actor-root shape.
- `~/primary/skills/push-not-pull.md` — Subscribe, not poll.
- `~/primary/skills/architectural-truth-tests.md` — witness-test
  discipline for the invariants above.
- `/git/github.com/LiGoldragon/signal-frame/ARCHITECTURE.md` — the
  wire kernel and signal-frame runtime support.
- `/git/github.com/LiGoldragon/signal-sema/ARCHITECTURE.md` — the
  payloadless Sema classification vocabulary.

## Runtime triad — Signal / Nexus / SEMA (three schema-driven planes)

Inside the `<component>` daemon, three layers organise the logic.
Per psyche record 856; refined by record 964 (Maximum, 2026-05-27);
**consolidated by record 970** (Maximum, 2026-05-27) which names
these the **THREE EXECUTION CENTERS** of the daemon. All three
planes are schema-driven and correspond to the workspace's three
schema types — `Signal` / `Nexus` / `Sema`. Each plane has its
own engine with its own traits, but all three engines share the
pattern of *running code based on input message and returning
output message with populated data*.

**This is Pattern B in the workspace's recurring pattern index**
(per `~/primary/INTENT.md` §"Recurring architectural patterns"
+ record 988, Maximum, 2026-05-27). Pattern A — async lives at
the data-type level — is realised inside the Signal and Nexus
planes via the universal mail mechanism + hookable lifecycle
events (records 935, 962, 963, 970). Pattern D — single-writer
authority + REST-shaped wire — is the SEMA / signal-side pairing
(records 949, 951). Both patterns are intrinsic to this section.

At the schema-language level, all three planes share the same root
shape: imports/exports, input, output, and namespace. Import/export
uses single-colon paths that mirror Rust modules (`crate:module:Type`,
not `crate::module::Type`). The planes differ by runtime ownership,
not by notation: Signal owns communication, Nexus owns execution and
in-flight mail, and SEMA owns durable state.

| Execution center | Schema type | What runs there |
|---|---|---|
| **Signal** | `Signal` schemas | Wire and communication: inter-component messaging |
| **Nexus** | `Nexus` schemas | Execution + mail keeper + Signal-to-SEMA translator: IO, external calls, UI, in-flight message processing |
| **SEMA** | `Sema` schemas | Durable state: single-writer database engine |

### Signal (wire and communication)

**Signal** is the reactive external surface — the daemon's edge,
where messages arrive from outside (people, agents, sibling
daemons). Owns: wire-level framing (length + short-header + rkyv per
the schema-derived stack); schema-emitted Operation enum dispatch;
connection lifecycle; short-header triage before full body decode;
mail-event emission such as `MessageSent`. Does NOT decide
acceptability, touch storage, or interpret payload semantically.

Per record 963: messages on the signal protocol move through a
universal **mail mechanism** with hookable lifecycle events
(including a method-on-message-sent that fires as soon as a message
is sent). Async representation lives at the data-type level — the
message types themselves carry correlation identifiers and lifecycle
state.

Per record 951 (High, 2026-05-27): the wire is **REST-shaped**.
Schema-emitted Operation enums on the Signal plane are typed
resource operations, not RPC method calls. The single-owner
property (SEMA owns the durable state for each resource kind) is
REST's stateless-server-with-canonical-state semantics realized in
the schema-driven stack.

### Nexus (execution — IO, external calls, UI, mail keeper, translator)

**Nexus** (renamed from Executor per record 964) is the
**execution-layer schema type** and the daemon's **mail keeper +
Signal-to-SEMA translator**. Per record 970 (Maximum, 2026-05-27):
Nexus is *"the in-between runtime layer that owns mail tracking
and Signal-to-SEMA translation. When Nexus has the mail, the mail
is in the BEING-PROCESSED state; Nexus IS the runtime
representation that a mail is being processed."*

Basic Nexus actions: **submit query to Nexus** (execution action)
and **get a reply** (state change or SEMA reply) which Nexus then
translates back into the Signal reply for the Signal plane.

Per records 965-969: Nexus covers ANY layer where code runs in
response to typed input and returns typed output — unifying internal
IO, external execution, and user interfaces under one schema-driven
plane. Per record 970 these uses are **specific instances of the
more fundamental in-between translator + mail keeper role**.

Nexus covers:

| Sub-scope | Example |
|---|---|
| Internal-decision execution | Takes each decoded Operation; decides acceptability, routes forward-only vs state-involving operations; composes Reply |
| External calls (IO) | Cloud component starts the Cloudflare CLI to change DNS — the external call is a nexus schema |
| All user interfaces | **Mencie** (the persona's multi-modal UI with mencie-audio, mencie-introspect, etc. as panels) — each UI panel has its own nexus schema describing data flow and return types |

Two paths through Nexus's internal-decision sub-scope:
**state-involving** (Nexus → SEMA → Nexus → Reply) and
**forward-only** (Nexus → Reply, no SEMA touch).

At the Signal/Nexus boundary, a decoded Signal root becomes
`NexusMail<Payload>` with a `MessageIdentifier`. While Nexus holds
that object, the mail is in processing state. When Nexus receives the
SEMA reply or other execution result, it emits `MessageProcessed<Reply>`
and translates that reply back to the Signal output surface, alongside
logging and hookable lifecycle events. **The on_sent hook fires when
Signal hands mail TO Nexus** (per record 970). The **database marker
travels on the SEMA reply that Nexus receives** and Nexus propagates
it in the Signal response.

Per record 965: Nexus is now **PART OF the schema-derived stack as
the execution-layer schema type**, superseding record 880's earlier
scope-restriction that named Nexus as a separate vocabulary track
parallel to the schema stack.

### SEMA (durable single-writer state)

**SEMA** is the single-writer state layer. Things that don't change
on their own — only the SEMA engine writes. Owns: redb (or
equivalent) read/write of generated archive types; daemon-stamped
timestamps; migration on database load (`mod previous` → `mod next`
bridge); derived indices (topic catalog, identifier mint, etc.);
sema-projection traits where schema declares a sema turn.
**Single-writer invariant**: concurrent operations queue through
SEMA's engine; readers can be multiple but writers are one.

Per record 948: internal database logic uses the same schema-defined
message language as component signals; a growing database component
can split into its own daemon without changing the language pattern.

### The flow (record 970's consolidated picture)

```text
Signal IN
  -> Nexus accepts mail (mail enters BEING-PROCESSED state)
     [on_sent hook fires here — Signal hands mail TO Nexus]
  -> Nexus translates to SEMA query
  -> SEMA engine runs and produces state change + SEMA reply
     (SEMA reply carries the database marker)
  -> Nexus receives SEMA reply (mail has reached state + got response)
  -> Nexus translates SEMA reply to Signal response, propagating
     the database marker; logs the "seriously received" event
     (because there has been a response)
Signal OUT
```

Above all three planes: the schema layer provides the typed shapes
(Input, Output, Action, Response, payload types, mail events) via
schema-emitted Rust. The Rust layer provides the methods on those
shapes (per `skills/rust/methods.md` §"Schema-generated objects are
the method surface").

This is an object-flow rule, not only a naming rule. A decoded Signal
object enters Nexus as mail; the Nexus mail object produces or requests
SEMA work; the SEMA reply carries the database marker; Nexus turns that
reply into the outgoing Signal object. Agents should implement those
steps as methods on the generated objects or on data-bearing actors
(`Engine`, `Nexus`, `Store`, `MailLedger`), never as a loose chain of
free functions.
