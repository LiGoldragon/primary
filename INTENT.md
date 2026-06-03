# INTENT — primary workspace

*The psyche's intent for this workspace, synthesised from Spirit
intent records and legacy `intent/*.nota` history. Verbatim psyche
quotes appear in italics; surrounding prose is agent-composed from
intent-log summaries. Companion to `ESSENCE.md` (the most universal
psyche intent — gold of the gold) and `AGENTS.md` (every-session
contract and override rules). Maintenance:
`skills/intent-manifestation.md`.*

## Intent is primordial

Intent drives the system. *If any agent needs to know what to do,
they fall back on intent.* The psyche is the human; psyche prompts
arrive in natural language. Persona messages between agents
(NOTA-formatted) are not psyche; agent-written files are not
psyche. Only the psyche is the source of new intent.

When intent on a question is unclear, absent, or contradicted,
**ask the psyche** before deciding. *Inferring is the discipline
breaking; asking is the discipline working.*

## The engine is intent and design

The workspace operates as an **intent-and-design-driven engine** —
*the whole engine is mostly intent and design driven. It's a
back-and-forth of designing and intending. And when enough is, the
intent is clear and the design is good enough, we can implement.*
**Designer and operator are the two halves of that dance.** Intent
clarifies what the system should be; design clarifies how it takes
shape; implementation crosses the threshold when both halves of the
readiness signal are met — intent clear AND design good enough.
Either half missing is a stop sign. The full discipline lives in
`ESSENCE.md` §"Intent and design — the engine's dance"; this prose
synthesis names the dance and its readiness signal. Per psyche
2026-05-22.

## Guidance files — the layered surface

The workspace calls every file that shapes agent behavior a
**guidance file**: `ESSENCE.md`, `AGENTS.md`, `INTENT.md`, every
skill in `skills/`, Spirit intent records and legacy intent files,
and per-repo `INTENT.md` / `skills.md` / `ARCHITECTURE.md`. The
shape an intent statement takes depends on its level of clarity and
importance: *highest-certainty universal psyche statements land in
ESSENCE.md; per-keystroke override-shaped rules in AGENTS.md hard
overrides; topic-specific discipline in skills; raw psyche records
in Spirit.*

Editing guidance files is the cadence of workspace evolution.

## The intent layer

Three surfaces, in increasing distillation:

The **intent log** lives in Spirit. It carries psyche statements as
typed intent entries. The current deployed shape stores one dense
agent-clarified description, kind, magnitude, and daemon-stamped
date/time; it deliberately does not store large verbatim/context
payloads. Agents do not manually append to `intent/*.nota` during
normal work. Discipline: `skills/intent-log.md` and
`skills/spirit-cli.md`.

**Per-repo `INTENT.md`** synthesises the project's psyche intent
into prose, the same shape as this file. Discipline:
`skills/repo-intent.md`.

`ESSENCE.md` (workspace and per-repo where it exists) holds the
**essential intent** — *the gold of the gold; only the most
universal, maximum-certainty psyche intent — statements made
with such force that they could stand as the founding rule of a
whole way of working.* Most psyche intent lives in the log and
in INTENT.md; ESSENCE holds the supreme.

The intent layer has **higher authority than every other
workspace surface**. *When two surfaces disagree, the intent
layer wins.* Agent-written documents (architecture, reports,
skills outside the intent layer) have lower precedence.

Supersession of psyche intent is **always explicit, and only the
psyche can supersede**. An agent encountering documented intent
that seems wrong asks; it does not override on its own
authority.

## Recording is the first task of any psyche-prompt turn

When a psyche prompt arrives, *capturing intent through Spirit is
the absolute first task — before editing reports, before responding,
before implementing. Everything else derives from intent.* The
agent reads the prompt, identifies every intent statement
(Decision / Principle / Correction / Clarification / Constraint),
records each through the deployed `spirit` CLI, *then* proceeds
with the work the prompt asked for. The legacy `intent/*.nota`
append path is not the normal workflow.

## Reports are for agents; chat is for the psyche

Substantive output — analysis, proposal, audit, synthesis — goes
in a report under `reports/<role>/`. Chat carries the
user-attention items inline with full substance. *The user runs
many parallel agents and cannot read giant chat responses.*

A chat reply names the report path and carries open questions,
blockers, and recommendations *each restated with enough
substance that the user can engage without opening the report*.
Opaque IDs (bead UIDs, content hashes, change IDs) always carry
an inline description — humans don't have a CLI in their head.

The full discipline: `skills/reporting.md` and
`skills/report-naming.md`.

Engine situation reports are the standard way to make a runtime or
schema-derived component quickly readable. They show component roles,
production/generated/test/schema size, schema-to-code ratios, root
interfaces, exact engine-trait signatures, live runtime paths, and
witnesses that prove architecture is used rather than merely present.
The discipline lives in `skills/engine-report.md`; inventory is useful,
but live architecture claims require call-path, runtime, trace,
process-boundary, database, type-system, or removal-breaks-behavior
witnesses.

## Skills must not grow noisy

Smart models can fill in blanks from good high-level guidance;
over-elaborated skills add cost without benefit. *Agents are
smart. … They can fill in the blanks. They just need good
guidance, good overall guidance.* When editing a skill, prefer
cutting to adding. Detail that doesn't change agent behavior is
noise.

The same principle pulled AGENTS.md to compactness and is the
forcing function on every guidance-file edit going forward.

## Roles are loose; beads are not role-labeled

The workspace organises work under four nominal roles (operator,
designer, system-operator, poet) plus lanes, but as of
2026-05-19 the psyche has loosened role boundaries — *I'm
keeping a single agent on a sort of task or topic instead of
shuffling context back and forth between agent windows.* Beads do
not carry `role:*` labels; any agent can pick up any bead based
on topic affinity rather than a prescribed lane.

Lanes still coordinate through lock files and per-role report
subdirectories; the role-label gate on beads is gone.

## Two deploy stacks coexist

**Production today** runs the old monolithic `lojix-cli` stack on
`main` branches in the canonical checkouts: `horizon-rs`,
`lojix-cli`, `CriomOS`, `CriomOS-home`, `CriomOS-lib`, `goldragon`.
Fixes for live nodes go on `main` in those checkouts.

**The lean rewrite** — new `lojix` daemon + thin `lojix` CLI +
lean horizon proposal/view + pan-horizon config — lives on
`horizon-leaner-shape` branches in worktrees under `~/wt/...`,
plus the new repos `lojix` and `criomos-horizon-config`. It has
smoke-built `zeus` end-to-end through `prometheus` but has not
been cut over. *Do not deploy it as if it were a fix.*

**Do not fold one stack into the other piecemeal.** Schemas have
diverged; cutover happens as a coordinated multi-repo merge
after the rewrite reaches feature parity. Until then:
production edits → `main` in the canonical checkout; rewrite
edits → `horizon-leaner-shape` worktree.

## Production work belongs in worktrees, not the canonical checkout

When work touches code already in production and the arc spans
more than one commit, the work belongs on a feature branch in a
**separate worktree** at `~/wt/github.com/<owner>/<repo>/<branch>/`
— parallel-and-predictable to the ghq layout under `/git/...`.
The canonical checkout stays on `main` so every peer agent sees
production reality without negotiating who-has-the-checkout. Full
discipline: `skills/feature-development.md`.

## Optional third "stable" branch is deferred

Per Spirit record 313 (Maximum certainty, 2026-05-23), an optional
third `stable` branch alongside `main` and `next` is **deferred**
until two preconditions hold: the architecture port from Spirit
(the architecture-discovery pilot) reaches all other components,
AND each component bootstraps from its own architecture discovery.
Until then `main` + `next` is sufficient: `next` carries the
in-flight version daemon for handover; `main` is the current
production version. A third branch dedicated to "stable releases"
would compete for psyche attention without reducing risk that the
existing two-branch model isn't already managing through Persona's
upgrade orchestration. Revisit when the preconditions land.

## BEADS is transitional; persona-mind is the destination

`.beads/` exists today for short-tracked-item coordination. The
destination is **persona-mind's native typed work graph** —
captured as memory variants in `persona-mind`'s schema. *Don't
build a Persona↔bd bridge; don't deepen the bd investment.*
Design new shapes assuming bd goes away.

BEADS is never an ownership lock. Any agent may create, update,
comment on, or close BEADS tasks at any time.

## Workspace truth lives in files every agent can open

Memory and persistent agent state must live in workspace files —
`skills/`, `repos/lore/`, `reports/`, `protocols/`, repo
`skills.md`, repo `ARCHITECTURE.md`, or `.beads/` while bd is
the active substrate. Don't use harness-dependent memory systems
(e.g. Claude Code's per-session memory files at
`~/.claude/projects/<workspace>/memory/`, or any agent-private
state store an outside agent cannot read). *Memory tied to one
harness is invisible to every other harness and to the human.*

## NOTA is the universal embedding-safe payload

NOTA is the workspace's text data format for typed records — used
for `.schema` files, for signal payloads on the wire, for intent
records in Spirit, and for inline CLI arguments to every persona
component. The workspace-shape consequence of NOTA's bracket-only
string discipline is that **a complete NOTA expression embeds
escape-free inside any host whose string syntax uses double quotes**
— JSON, Rust string literals, Nix attribute values, YAML, TOML,
shell double-quote arguments, HTTP request bodies, database string
columns, environment variable values. *"JSON-in-JSON requires
escape cascades; NOTA-in-anything-with-doublequote-strings is
escape-free. This is a load-bearing design property of NOTA, not
an incidental side effect."* Design every workspace emitter and
storage path to take advantage of this — the shell-double-quote
wrapping convention (`spirit "(Record (...))"`) is the same
principle at the CLI scale.

NOTA language design lives in `repos/nota/INTENT.md`; emitter and
decoder discipline lives in `repos/nota-codec/INTENT.md`. Full
agent-side authoring discipline: `skills/nota-design.md`.

## NOTA is a typed text user interface

*"What's at the heart of NOTA is sort of a hack on the text user
interface, using common sense, good patterns, beauty, and
delimiters, and structure, typed structure. It's a typed language.
So everything is read as a known type, which could have
structurally different nodes at some points, because they're
structure macro nodes, but it's still a known type in the data type
theory. So we can reliably decode it if it's well-formatted, if
it's valid."* Per psyche 2026-06-03 (intent record 1508 Maximum).

NOTA's character as a typed language is the load-bearing property
behind the workspace's NOTA-everywhere direction. The text surface
is what humans and agents type; the typed-language guarantee is
what makes it round-trip with the binary substrate (rkyv) reliably.
Structure macro nodes — the extensibility mechanism that lets one
parser cover new shapes — extend the typed vocabulary itself, so
the macro extension is typed, the resulting node is typed, and
decoding remains deterministic.

## Symbols are paths through the schema namespace

Per psyche 2026-06-03 (intent records 1506 Maximum, 1507 High):
when an interface is defined, the enums and structs that create
the root data structures collectively create a global namespace
for symbols. Each typed symbol — type, variant, field, operation,
route — has a fully qualified identity expressed as a **path**
through that namespace. *"The fully-qualified-symbol-path
mechanism … is the workspace's universal machine-readable symbol
identity expressed through a text-user-interface form."*

The mechanism is canonical, not per-design. When a new surface
needs symbol identity, it uses the same SymbolPath rather than
inventing a parallel vocabulary:

- **Help / description namespace** (Spirit 1493 + designer 487.2)
  keys descriptions by SymbolPath, with the default-generator
  humanizing the path's terminal segment when no entry exists.
- **NOTA config-by-convention** (Spirit 1494 + designer 487.3)
  resolves a file path to a typed root via a registry keyed by
  the convention's path pattern; the registered root type is
  itself a SymbolPath.
- **Trace identity** (Spirit 1492 + operator 291) names trace
  events by the schema-defined path through the per-plane object
  hierarchy (`SignalObjectName::Input(InputRoute::Record)`, etc.).
- **Future surfaces** (introspection, schema-daemon upgrade,
  inter-component request routing) inherit the same identity
  mechanism — schema-emitted Rust types and NOTA renderings are
  two projections of one underlying symbol-path identity space.

The architectural manifestation discipline: when authoring a
design or skill that uses symbol identity, call out that this is
the canonical naming mechanism and reuse SymbolPath rather than
invent a per-design convention.

## Authored data files prefer typed NOTA, by path convention

Per psyche 2026-06-03 (intent record 1494): when the workspace
writes data — anything that isn't user-facing prose — *it might
as well just be in a NOTA vector of records.* A file's directory
plus its predictable name fixes the expected root type by
convention. *"Like config.nota in a certain type of directory has
a certain type to it. So it expects a certain type in it by
convention. So we decide what the convention is."* The root is
usually a struct (single-record file) or a vector of records
(multi-entry file), occasionally a top-level enum selection when
the file picks one alternative from a closed choice.

The convention turns each authored file into a typed object: the
schema registry knows that `<repo>/spirit-daemon-config.nota` is a
`SpiritDaemonConfiguration` struct, that `skills/skills.nota` is a
`Vec<SkillEntry>`, that `intent/<topic>.nota` is a
`Vec<IntentRecord>` (legacy). A typed loader reads the path,
resolves the convention, decodes the file as the expected type,
and fails loudly when the file doesn't match. No ad hoc parsing
per file; no untyped scratch data accumulating.

Daemons still receive binary on the wire (per §"NOTA is the
universal embedding-safe payload" + the single-argument rule +
intent record 1495). The convention applies to authored text files
that tools, CLIs, and codegen inputs load — not to inter-component
traffic.

Sub-design: `reports/designer/487-Design-trace-help-config-context-meta-2026-06-03/3-nota-config-convention-design.md`.

## The Nix store is not a search surface

Running `rg`, `grep`, `find`, `fd`, broad globs, or recursive
`ls` against `/nix/store` is forbidden — the store grows
unbounded, full-text search across it exhausts memory, and the
matches are usually dependency-tree noise.

When looking for Nix-controlled information, use Nix: the source
checkout, `nix eval` against an attribute path, `nix flake show`
/ `nix flake metadata`, `nix path-info` for a derivation output,
or a targeted check/passthru that exposes the value. If a value
cannot be reached this way, change the Nix code to expose it.

## Persona is LLM-mediated end-to-end

Persona components are dumb mechanism without internal
intelligence; the thinking happens in agent LLMs that drive
components through CLIs and through persona-spirit. Anything
inside a component that looks like a natural-language-
understanding decision — classifier, supersession judgment,
intent parsing — is an LLM call, not algorithm code.
*"there's no component that works without LLMs."* The LLM is
always on the other end of the wire, agent-side.

## Persona components ship in raw form first

Components ship as standalone CLI + daemon + sema state first;
integration with sibling components comes after the raw form is
working. Agents use components individually through their CLIs
before component-to-component wiring lands. *"we can use the
components in the raw form like they don't have to be talking
to each other right away."* No pre-coordinated integration
ceremony; ship the triad, let usage demand wiring.

## The schema-driven stack

The workspace is migrating to a schema-driven architecture where
each persona component declares its contracts — wire, storage, and
internal-actor channels — in NOTA `.schema` files; the schema is the
canonical source the macro pipeline projects into Rust, NOTA-text,
and rkyv-binary. *The schema IS the architecture, not a tool that
produces it.* Schemas warrant per channel; *contract = channel; one
channel = one contract = one schema*. Three categories — wire (the
process boundary), storage (the lifetime boundary), internal (the
actor mailbox) — with wire schemas in the `signal-*` crate and
storage + internal schemas in the daemon crate. **Schemas define
data types only** — effects, fan-out targets, and effect tables are
runtime dispatch / logic, not authored schema content (per psyche
2026-05-26, records 713-715).

The rkyv binary encoding lives in one byte layout that survives two
homes: **sema** in storage, **signal** on the wire. NOTA is the text
projection on top. The vocabulary closes the loop:
**schema specifies, signal moves, sema holds.**

The `.schema`/NOTA pair is a **specification language more specific
than Rust** — Rust mixes data shape with derives, trait impls,
visibility, and validation; a `.schema` declaration is JUST the
structural truth, and the noisy-but-mechanical Rust + rkyv codec +
optional NOTA codec EMIT from it.
This is the same reason CapnProto exists as a separate language from
C++. Schema is a **superset of CapnProto-style declaration** with
three additions: a module system (named imports/exports as the
document's first position), a macro system (extensible type-
declaration vocabulary, where macros are data), and shape-driven
node-type matching. NOTA owns the universal substrate for that:
parsed delimiter/atom structure, known-root document-body codecs,
derive-generated typed readers/writers, and a programmable macro-node
registry that matches structure by delimiter / count / position /
captured child shapes. Schema is a consumer of that substrate: it
declares the schema vocabulary and lowers matches into `Asschema`.
Future structural-macro languages should reuse the same NOTA layer
instead of inventing another parser. NOTA is the text view of the
portable rkyv format's specification; the binary it specifies appears
in two contexts — SEMA at rest and signal in transit (psyche
2026-05-26, records 839-844; 2026-05-31, record 1281).

Authored schema sugar lowers into **assembled schema** (`Asschema`)
before Rust emission. `Asschema` is macro-free typed data, not hidden
parser state: it can be written as legal NOTA, read back as the same
typed value, written as rkyv bytes, and read back before
`schema-rust-next` emits Rust. The CLI opts into the generated NOTA
surface; daemons and binary-only clients keep the rkyv surface without
linking a NOTA decoder.

Authors write from the point of view of **NEXT**; **MAIN** is the
published baseline (imported as comparison); **PREVIOUS** or **LAST**
is the prior iteration. The same vocabulary applies wherever a
prior shape is referenced — schema versions, wire-header
extensions, on-disk migration markers, deployment slots.

A brace `{ ... }` in NOTA is ALWAYS a key/value map; the schema
namespace at position 3 is a brace and authors pair-style
`Name TypeDefinition` entries directly — parenthesised named-object
form `(Name TypeDefinition)` is redundant and rejected by the
engine. Conceptually the namespace is a DYNAMIC ENUM where each key
is a variant tag and each value is the variant payload, stored as a
key/value map for composition convenience and APPEND-ONLY in the
Cap'n Proto style so existing positions stay stable across upgrades
(intent records 891-894, 2026-05-27).

A bracket `[...]` is a homogeneous vector. In schema enum bodies,
that vector's element type is "variant signature": a bare PascalCase
symbol for a unit variant, or a parenthesised `(Variant PayloadType)`
record for a data-carrying variant. Interleaving variant names and
payload types as separate vector elements is notation lying about
the data shape, so the production parser rejects it (intent records
1267-1269, 1277, 1294).

Schema-language design (namespace shape, enum/struct syntax,
imports, lowering) lives in `repos/schema/INTENT.md`. Composer +
wire-substrate intent lives in `repos/signal-frame/INTENT.md`.
Actor-schema architecture for the spirit daemon lives in
`repos/persona-spirit/INTENT.md`.

## Tracing is its own typed schema-defined interface

Per psyche 2026-06-03 (intent records 1489 High, 1490 Maximum,
1491 High, 1492 Maximum): tracing is its own schema-defined
interface with closed generated enum vocabularies — typed
objects, typed events — not an ad hoc string log. Trace data
remains typed all the way from daemon emission through the wire
to the client; *string rendering happens only when a client or
user-interface surface prints them.* The daemon emits binary
trace frames; the CLI parses them into typed events and renders
strings only at the display surface.

Three consequences:

- **Generated, not hand-rolled.** Schema-rust-next emits the
  trace object names (`SignalObjectName`, `NexusObjectName`,
  `SemaObjectName`, the umbrella `ObjectName`, and `TraceEvent`)
  from the component's schema. The engine traits emit trace
  default hooks at every actor boundary. Component code overrides
  only the sink behavior; the trace vocabulary is schema-owned.
- **Client-side trace handling is generic.** *"Client-side
  tracing should be generated or generic from schema interface
  definitions; the CLI should stay a thin client and should not
  own component-specific trace logic beyond enabling or
  displaying the generic trace surface."* The CLI is the
  translation/display surface; the listener, frame decode, and
  print path live in the shared runtime substrate or are emitted
  from schema, not hand-written per component.
- **No trace on trace, controlled per crate.** *"We wouldn't
  have tracing enabled on tracing at all for now and no matter
  what. So this tracing enablement has to be controlled per crate
  I guess."* Production builds compile no trace logic; the
  `testing-trace` feature compiles the trace hooks per crate. The
  trace interface itself is never observed by tracing — the trace
  system does not recursively trace its own events.

Current implementation status (operator 291 + 292): triad-runtime
owns reusable trace log/frame/socket/listener mechanics;
schema-rust-next emits typed trace object names + engine trait
default hooks + lifecycle hooks; spirit-next supplies the
component-specific adapter (one `TraceEventFrame` impl + one
`Display for TraceEvent` impl). The open work is generating the
CLI/client trace adapter so the per-component adapter shrinks to
zero. Audit: `reports/designer/487-Design-trace-help-config-context-meta-2026-06-03/1-trace-and-daemon-boundary-audit.md`.

## Help and documentation are schema data in a mirror namespace

Per psyche 2026-06-03 (intent record 1493): help and
documentation belong inside the schema substrate as a mirror
description namespace over the global symbol namespace. Every
fully qualified symbol — type, variant, field, operation, route —
has a slot in the mirror that carries its description. When the
slot is empty, a default is generated from the symbol's schema
declaration (humanized variant name, field-type-derived prose).
*"This is where you generate the help, where you have all of the
global namespace together. And if there's no entry for a certain
symbol to get help from."*

The mirror keeps help in the closed-language discipline: a
`Description` is a typed bracket-string field on the description
schema, not an ad hoc Rust doc comment. The rendering edge
(CLI `Help` reply, generated documentation site) is the only
place strings are emitted. This refines the older direction in
component-triad.md §"Help operations — discovery through NOTA,
not through flags" (Spirit 263 + 1396): the source of help text
is now the schema description namespace, not Rust doc comments,
though generated `Help` operations remain the discovery surface
for clients.

Design: `reports/designer/487-Design-trace-help-config-context-meta-2026-06-03/2-help-namespace-design.md`.

## Three schema types, three runtime planes

Per intent records 964 + 965 (Maximum, 2026-05-27): the schema layer
has **THREE SCHEMA TYPES** corresponding to the three runtime
planes. Each has its own engine with its own traits, but all three
engines share the pattern of *running code based on input message
and returning output message with populated data*. The root type of
a schema is what is meant to be sent as a message; everything is
serializable but the root type is the message surface.

| Schema type | Plane | Owns |
|---|---|---|
| **SIGNAL schemas** | Wire and communication layer | Inter-component messaging; the wire protocol substrate |
| **NEXUS schemas** | Execution layer — IO, external calls, all user interfaces | Code-runs-on-input-returns-output: internal IO, external CLIs (e.g. cloud calling the Cloudflare CLI to change DNS), and ALL UI panels |
| **SEMA schemas** | Durable database-work layer | Database engine; single-writer durable storage |

File extensions remain **OPEN** per record 964: candidates include
`.signal.schema` / `.nexus.schema` / `.sema.schema`, OR the schema
type as the first record of the schema content (`Signal …`, `Nexus
…`, `Sema …` in parens). The schema author declares the variant;
the engine routes.

Each schema type uses namespace imports for shared types per the
single-colon namespace rule (record 902) and emits Rust types and
traits via `schema-rust-next`. Per record 964 the runtime triad
framing from record 371 is **refined: Executor is renamed to Nexus**
and all three planes are schema-driven. Per record 965 Nexus
specifically covers ANY layer where code runs in response to typed
input and returns typed output — unifying IO, external execution,
and UI under one schema-driven plane.

Per record 982 (Maximum, 2026-05-27), the three schema types are
symmetric at the schema-language level. Signal, Nexus, and SEMA each
have the same four-position shape: imports/exports, input, output,
and namespace. Import/export uses the same single-colon namespace
convention that mirrors Rust modules (`signal:sema:Magnitude`,
`spirit:core:SemaOutput`) instead of Rust's `::`. The planes differ
by ownership and runtime semantics, not by authored schema shape:
Signal communicates, Nexus executes and holds mail, and SEMA owns
durable single-writer database work.

Per record 1007 (Maximum, 2026-05-27), **SEMA means database work**:
the real SEMA plane is the part that writes durable state to the
component database file. Today's storage substrate is redb, but the
file extension may become `.sema` instead of `.redb` so the file name
states its architectural role. An in-memory `Store` can prototype the
`SemaInput` / `SemaOutput` language, but it is not a full SEMA proof
until the operation writes the durable database artifact.

Per record 965, **Mencie (the persona's multi-modal UI, with
mencie-audio / mencie-introspect / etc. as panels) is implemented
as nexus schemas — each UI panel has its own nexus schema describing
data flow and return types.** Cloud-to-Cloudflare style external
interactions are also nexus schemas. Record 965 SUPERSEDES record
880's scope-restriction on Nexus terminology: *"Nexus is now PART
OF the schema-derived stack as the execution-layer schema type."*

### Nexus is the MAIL KEEPER — runtime flow consolidation

Per intent record 970 (Maximum, 2026-05-27): **Nexus is the mail
keeper** — the in-between runtime layer that owns mail tracking
and Signal-to-SEMA translation. *"When Nexus has the mail, the
mail is in the BEING-PROCESSED state; Nexus IS the runtime
representation that a mail is being processed."*

The daemon has **THREE EXECUTION CENTERS**: Signal (communication
messaging), Nexus (execution + mail keeper + translator), SEMA
(state). The complete flow:

```text
Signal IN
  -> Nexus accepts mail (mail enters BEING-PROCESSED state)
  -> Nexus translates to SEMA query
  -> SEMA engine runs database work and produces durable state change + SEMA reply
  -> Nexus receives SEMA reply (mail has reached state + got response)
  -> Nexus translates SEMA reply to Signal response with logging
     (the response has been "seriously received" because there has
     been a response)
Signal OUT
```

Basic Nexus actions are *"submitting query to Nexus (execution
action) and getting a reply (state change or SEMA reply) which
the Nexus then translates back into the Signal reply for the
Signal plane."*

Record 970 **CONSOLIDATES** four earlier records into one picture:
record 935 (Communicate + signal-frame + mail + database marker),
record 963 (mail mechanism + on_sent hook), record 964 (three
schema types), and record 965 (Nexus as execution + IO + UI). The
on_sent hook fires when Signal hands mail TO Nexus. The database
marker travels on the SEMA reply that Nexus receives and Nexus
propagates it in the Signal response. The UI and external-IO uses
of Nexus from 965 are **specific uses of the more fundamental
in-between translator + mail keeper role**.

Per record 988 (Maximum, 2026-05-27), this flow is also an
implementation discipline: async mail flow is actor-object flow.
Runtime code should not be a procedural chain of helper functions.
A Signal root becomes a generated mail object; Nexus owns that mail
object while processing; SEMA writes durable database state and returns
a generated reply with a state marker; Nexus translates that object into the Signal response. The
behavior belongs on generated schema nouns and data-bearing actor or
store objects as methods or trait impls.

Per record 998 (Maximum, 2026-05-27), tests for the schema-derived
runtime chain must use schema-emitted data types and schema-type
traits as their witnesses. A test for Signal→Nexus→SEMA must assert
against generated objects such as `MailLedgerEvent`,
`NexusInput`/`NexusOutput`, and `SemaInput`/`SemaOutput`; ad hoc
test-only enums are not a valid substitute. SEMA engine operations
take SEMA schema input and emit SEMA schema output.

Per records 999 and 1000 (Maximum, 2026-05-27), the next prototype
iteration keeps **schema at the heart**. Schema-emitted Rust types are
the canonical truth source for every system boundary type; hand-written
runtime code is behavior on those generated nouns or generated trait
impls. End-to-end tests must construct schema-emitted values, invoke
the runtime through schema-emitted trait surfaces, observe
schema-emitted lifecycle events, and assert schema-emitted outputs.
No hand-written boundary enum, observer state, validation error, or
database marker shim counts as a valid witness. Prototype restarts
begin from the latest operator main stack, then audit any remaining
shim as the next component-development task.

## Signal protocol — universal mail mechanism

Per intent record 963 (High, 2026-05-27): the wire protocol is
named the **SIGNAL PROTOCOL**; messages on the signal protocol move
through a universal **MAIL MECHANISM** (the mailer / dispatcher /
push system) — the same lifecycle infrastructure every component
shares.

Message lifecycle has **hookable events** including a
**method-on-message-sent** that fires as soon as the message is
sent and commits an action through the mail dispatching system. The
hook point allows UI consequences, observers, and other components
to react when a message is sent. Per record 962: the mail mechanism
is a **push system** — sending a message invokes methods on typed
mail events instead of relying on polling, so observers can attach
hooks at the message-sent boundary.

**Async representation lives at the data-type level** of the signal
protocol — the message data types themselves carry the correlation
identifiers and lifecycle state needed to track sent / queued /
processing / replied transitions. The mail manager pushes messages
and emits lifecycle events. This extends record 935 (Communicate
trait + signal-frame + mail state manager + database marker) by
naming the lifecycle-event surface and the hookable callback
mechanism on top.

## The wire architecture is REST-shaped

Per intent record 951 (High, 2026-05-27): the schema-emitted data
types are positioned as **REST-shaped at the wire layer**. *"The data
type REST is emitted by this schema system and the single-owner
system mirrors the REST concept."* Schema defines the resource /
message types; the single-owner state-of-record property (SEMA owns
the durable state for each kind; mutations route through that one
owner) mirrors REST's stateless-server-with-canonical-state
semantics. This frames the wire pattern architecturally — the
schema-emitted Operation enums on the Signal plane are REST-shaped
typed resource operations, not RPC method calls — and binds future
schema decisions to that shape: every wire operation has a typed
resource it acts on, and the canonical state for that resource lives
at exactly one owner (the SEMA plane of the owning daemon).

## Schema-emitted Rust mirrors the schema namespace

Per intent record 952 (High, 2026-05-27): the naming system between
schema-emitted code and Rust source **mirrors each other**. *"You
can use the naming system that way to like a mirror."* The
colon-path namespace in schema (e.g. `spirit-next:signal:Frame`)
maps to Rust module-and-type names by direct correspondence
(`spirit_next::signal::Frame`) — agents can grep across both
artifacts via the shared identifier, and a path in one form
translates mechanically to the other. The property is load-bearing
for navigability: the schema and the emitted Rust are two views of
the same identity, and the mirror property makes either view a
sufficient entry point. Per record 909, the emitted Rust lives at
`src/schema/<module>.rs` in the consumer crate so the two surfaces
sit side-by-side in the source tree.

## Recurring architectural patterns

Per intent record 988 (Maximum, 2026-05-27): several disciplines
in records 700-988 recur across multiple records, multiple repos,
and multiple kinds of code. This section names those patterns so
the recurring nature is visible. Each pattern below is realised
by multiple records, applies to multiple repos, and is a
discipline-shaped statement rather than a one-off decision. The
detailed records and their per-section homes above remain the
source; this section is the index that calls out *which records
together name a pattern*.

### Pattern A — Async lives at the data-type level (push, hookable, mail-based)

**Anchoring records:** 935, 962, 963, 970.

Async correlation, message lifecycle, and observer notification
are CARRIED BY THE TYPED MESSAGE OBJECTS themselves, not imposed
externally by polling or by hidden state machinery. Messages on
the Signal protocol move through a universal MAIL MECHANISM with
hookable lifecycle events (`on_sent`, etc.); the mail manager
pushes events; observers attach methods on typed mail-event
objects. The consequence binds every component: same mail
substrate, same lifecycle hooks, same database-marker
propagation. Full discipline: §"Signal protocol — universal mail
mechanism" above; per-repo realisations in `signal-frame`,
`spirit-next`, `spirit`, `signal-spirit`, `core-signal-spirit`.
Skill: `skills/component-triad.md` §"Runtime triad" plus
`skills/push-not-pull.md`.

### Pattern B — Three execution centers (Signal + Nexus + SEMA)

**Anchoring records:** 371 (Executor → Nexus per 964), 964, 970,
981, 982, 1326, 1327, 1330-1336.

Every persona daemon's runtime decomposes into three execution
centers — Signal (wire/communication), Nexus (execution + mail
keeper + Signal-to-SEMA translator), SEMA (durable single-writer
state). Each has its OWN schema language with the same 4-position
shape (Imports / Input / Output / Namespace) and the SAME
import-export mechanism via colon-path namespaces. All three
engines share the pattern *"running code based on input message
and returning output message with populated data."* Full
discipline: §"Three schema types, three runtime planes" above.
Skill: `skills/component-triad.md` §"Runtime triad".

Per records 1326 (Constraint High, operator-specific) and 1327
(Principle Maximum, workspace-wide): every component runtime
conducts its core logic through three **schema-emitted engine
traits** whose methods take and return plane root types —
`SignalEngine` (triage only, Spirit 1330), `NexusEngine` (heavy
logic + bidirectional translator, Spirit 1331), `SemaEngine`
(durable single-writer with parallel reads via apply/observe
split, Spirit 1332). The trait surface is uniform across
components; each component's runtime is a composition of three
trait impls attached to data-bearing nouns. Signal hands the
typed Input to Nexus one-way; Nexus reaches SEMA exclusively
through the trait surface; SEMA returns to Nexus which decides
the reply. Full discipline: `skills/component-triad.md` §"Runtime
triad engine traits — Signal triage / Nexus computation / SEMA
durable". Worked example today: `spirit-next` at main `d29dc6c`
(Spirit 1332 landed).

### Pattern C — Methods on schema-generated data types

**Anchoring records:** 712, 882, 942, 945, 947, 953, 954.

Schema-emitted types are the nouns; hand-written Rust attaches
verbs to them as methods on the data-bearing type or as trait
impls. No free functions. No ZST namespace holders. No parallel
hand-rolled mirrors of generated types. When the runtime gains a
behaviour (encode/decode, upgrade, mail-event hook, actor
reaction), the behaviour lives as a method on the schema-emitted
noun, not on a helper-function library beside it. Skill:
`skills/rust/methods.md` §"Methods on types, not free functions"
+ §"Schema-generated objects are the method surface".

### Pattern D — Single-writer authority + REST-shaped wire

**Anchoring records:** 949, 951.

SEMA owns the durable state for each resource kind; mutations
route through that one owner. Schema-emitted Operation enums on
the Signal plane are REST-shaped typed resource operations, not
RPC method calls. The single-owner property at SEMA mirrors
REST's canonical-state semantics — distributed semantics with one
canonical owner per kind, no shared-write races, all observation
via push-subscription not poll. Combined with Pattern A: writers
are single; observers are many; communication is push-via-mail-
events. Full discipline: §"The wire architecture is REST-shaped"
above. Skill: `skills/component-triad.md` (the Mutate-down /
Subscribe-up authority discipline).

### Pattern E — Schema is one recursive struct down to scalars

**Anchoring records:** 894, 932, 933, 940.

A `.schema` document is a typed struct read positionally; nested
struct and enum definitions are macros applied at known
positions; macros bottom out in scalar leaves (booleans,
integers, strings, vectors, typed-string newtypes). The recursion
is one shape — the macro engine is shared substrate for all three
schema types (Signal, Nexus, SEMA), each of which is its own
language (record 982) but uses the same structural skeleton.
Repo-scope detail: `repos/schema/INTENT.md`,
`repos/schema-next/INTENT.md`,
`repos/nota-next/INTENT.md`.

### Pattern F — Mirror naming (schema namespace mirrors Rust modules)

**Anchoring records:** 902, 909, 952.

A schema position named `spirit-next:signal:Frame` maps
mechanically to the Rust type `spirit_next::signal::Frame`. The
identifier IS the same in both views; only the case-rules and
separator differ (`:` → `::`; kebab → snake; PascalCase
unchanged). Agents grep across either surface and reach the
matching point in the other. The schema and the emitted Rust are
two views of one identity — either view is a sufficient entry
point for navigation. Full discipline: §"Schema-emitted Rust
mirrors the schema namespace" above + `skills/naming.md` §"Schema
and emitted Rust mirror each other".

## Concept designer is the entry for new concepts

**Concept designer** is a real role — *an entry point for new
concepts the psyche is juggling*. Compares new concepts against
existing ones; surfaces relationships; decides when a concept
earns its own dedicated lane. Fleshing out next.

(Persona-spirit's own apex-role + architecture intent lives in
`repos/persona-spirit/INTENT.md`; the workspace-shape consequence
is in `ESSENCE.md` §"Persona is meta-AI; spirit animates".)

## When a new role appears without a skill

A workspace where new roles can be created dynamically (e.g. by
a future `persona-orchestrate` daemon, or by the concept
designer spawning a new lane) needs an entry point so that a
new role isn't a dead end. The new-role agent reads `AGENTS.md`,
`ESSENCE.md`, this file; queries `skills/skills.nota` for the
closest existing role-skill (likely `skills/designer.md`,
`skills/operator.md`, or another discipline file); escalates to
the psyche for scope clarification per
`skills/intent-clarification.md`; and drafts a new
`skills/<role>.md` in-place as it does substantive work.

## Possible additional role — auditor (Medium certainty)

Per intent records 234 and 235 (2026-05-22, Medium certainty),
a third role is under consideration: the **auditor**. The
auditor closes the loop back to designer — it doubts, finds
flaws, identifies bad patterns, catches broken workspace rules.
*"The auditor is just going to be mostly mechanical. It's just
a doubter, something that finds flaws or bad patterns … things
that broke rules that we have."* The auditor knows the rules
because they live in the workspace's standing guidance files
(`ESSENCE.md`, `AGENTS.md`, `skills/`); the mechanical nature
of the work makes it suit a smaller model good at pattern
checking. The psyche named **DeepSeek** as the chosen model and
the direction is to **automate** the auditor: *"deep seek is
going to be our main auditor, because our audits are just going
to be mostly mechanical."*

Carried under the carry-uncertainty discipline
(`skills/architecture-editor.md` §"Carrying uncertainty"): the
role is **proposed, not decided**. Open questions: authority
class (structural or support-tier?), lane mechanism (windows on
a shared agent identity or external CI-style pipeline?),
substrate for audit findings flowing back to designer (reports
under a `reports/auditor/` subdir, comments on beads, Spirit
intent records from an auditor agent identity, or PR-style
review on jj commits). No `skills/auditor.md` skill file and no
`reports/auditor/` subdirectory yet — those land when the
role's shape settles. The entry point for the bootstrap, if an
auditor agent starts work before the skill file exists, is the
"When a new role appears without a skill" section above.
