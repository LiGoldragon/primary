# The Goldragon Estate: A High-Level View

## The Dream

The Goldragon estate is building a personal operating environment where every
distinct concern -- storing intentions, routing messages, deploying machines,
managing approval, tracking time -- runs as its own long-lived daemon. These
daemons do not speak JSON or plain text to each other. They exchange compact
binary messages called **signals** (typed request/reply payloads serialized
with rkyv, a zero-copy Rust archive format). Each daemon owns its own durable
database and exposes exactly two sockets: one for ordinary callers and one for
privileged owner operations. Human interaction happens through thin text
command-line tools that translate typed commands into signal frames, send them
to a daemon, and print the reply. These CLIs are shims -- temporary
conveniences until richer interfaces exist.

None of this typed wiring is written by hand. A custom four-layer language
engine authors all of it from declarations:

- **Ethos** -- the authored types. You declare what things *are*: an Interface
  with its request and reply variants, a storage document shape, a Nexus
  message vocabulary.
- **Nomos** -- the transformation rules. Given sealed Ethos declarations,
  Nomos lowers them: deciding how types map to wire formats, how storage
  shapes relate to each other, how one layer feeds the next.
- **Logos** -- the explicit program representation. The output of Nomos is a
  typed, ordered program model that knows what code to emit but has not yet
  chosen a target language.
- **Dotos** -- the data notation. A minimal structural format (atoms and
  delimited blocks) used for configuration, cluster proposals, and the source
  text of Ethos declarations themselves.

The guiding philosophy is that adding more correctness -- more precise types,
more verified boundaries -- pays for itself by making every subsequent
expansion simpler. Beauty is the symptom of good engineering.

## The Standard Component Shape

Every daemon in the estate follows the same pattern. **Spirit** -- the
intention-storage service -- is the best example because it is the most
complete.

A component consists of:

1. **An Ethos declaration** that defines the Interface (what you can ask
   Spirit and what it answers), the Nexus (what Spirit announces to the
   wider system), and the Sema documents (what Spirit stores durably).
   Today the authored source lives beside the contract crate it generates;
   the older dedicated repository (spirit-ethos) is condemned and awaiting
   deletion.

2. **A signal contract** (`signal-spirit`) -- Rust types generated from the
   Ethos declaration that define the exact binary shape of every request and
   reply on the wire. A separate **meta-signal contract** (`meta-signal-spirit`)
   defines the privileged owner-only operations (configure, import, observe).

3. **A daemon** (`spirit`) -- a long-running process built on the kameo actor
   framework. It listens on a Unix socket, accepts signal frames, does its
   work (querying or mutating its Sema store), and sends replies. Spirit
   stores entries with domain, kind, description, and importance fields.

4. **A judge** (`spirit-judge`) -- an edge adapter that wraps an LLM model
   call behind the same typed signal interface. The judge reads prompt packs,
   calls a model provider, and returns structured verdicts. It fails closed on
   bad input.

5. **Sema storage** -- the daemon's own database, built on `redb` (an
   embedded key-value store) through the sema-engine library. Each component
   owns its storage schema; no component reads another's database.

6. **Thin CLIs** -- one ordinary CLI for normal operations, one meta CLI for
   privileged owner operations. Each is a small binary that frames a typed
   request, sends it to the daemon's socket, and prints the reply.

Not every component has all six pieces yet. Many have the signal contract and
daemon but lack the meta-signal contract, the judge, or both CLIs.

## The Map

### The Language Engine

The engine that generates all typed wiring from Ethos declarations. This is
the generative heart of the estate.

**core-ethos** reads raw Ethos source text through a strict five-phase
bootstrap pipeline: structural planning, identity cataloging, name
assignment, textual metadata, and authority-sealed transactions. Working.

**core-nomos** takes those sealed transactions and lowers them into a typed
Logos model, revalidating the authority receipt at each step. Working.

**core-logos** defines the ordered program model that sits between lowering
and code emission. Working.

**logos-engine** drives the Rust projection pipeline: it consumes the Logos
model and emits compilable Rust source files through the structural codec.
Partial -- it has an actor-based daemon with minimal test coverage.

**logos-runtime** provides the fixed, schema-independent carriers (Signal,
Nexus, Sema, Plane) that every generated crate and engine daemon shares.
Working.

**structural-codec** is the generic evaluator for archived structural rule
records. It handles textual decode, alternative-form proofs, and ordered
documents. High iteration count; mature.

**schema-rust** is the current verified bootstrap generation boundary: it
takes Ethos source text through the full pipeline (core-ethos, core-nomos,
Rust Logos projection) and writes out Rust contract crates. This is what
actually generates the signal and meta-signal crates today. Working.

**protos-engine** is the integration and conformance sink. It has no Rust
source of its own -- it assembles pinned revisions of roughly thirty-five
component repositories into a Nix flake that runs coherence scripts
(dependency direction, pin policy, identity checks, behavior witnesses).
Working as an integration gate.

**protos** defines the contract surface for the language family: capsule
types, wire-contract family allocations, and textual associations. Stable.

**tree-sitter-ethos** and **tree-sitter-dotos** provide editor grammars and
syntax highlighting for the two authored formats. Both lag the current
syntax rulings and need regrammaring.

### The Signal Framework

The typed binary messaging layer that all daemons speak.

**signal-frame** is the wire kernel: envelope headers, rkyv length-prefix
framing, exchange correlation, stream lifecycle, and the thin-client CLI
skeleton. Structurally complete and actively evolved.

**signal** is the older record-vocabulary crate, mid-migration toward
signal-frame's contract-shaped stack. Transitional.

**signal-derive** is a proc-macro that derives compile-time schema
descriptors for signal record kinds. Complete.

**signal-standard** is a pure vocabulary library holding the closed roster
of component kinds (fourteen variants across five zones). Stable.

Each component gets its own **signal contract crate** (signal-spirit,
signal-ethos, signal-nomos, signal-logos, and so on) and optionally a
**meta-signal contract crate** for privileged operations. The goal is for all
of these to be generated from Ethos declarations; today Spirit's are
generated while several others are still hand-written.

### The Storage Layer

**sema** is the database kernel: typed, version-guarded table access over
redb with rkyv-archived values. Deliberately minimal.

**sema-engine** layers full database operations on top: assert, mutate,
retract, match, subscribe, validate, with commit-log replay and subscription
delivery. Query-algebra operators (constrain, project, aggregate, infer,
recurse) are defined as plan nodes but execution is not yet implemented.
Partially done.

**sema-storage** wraps sema-engine into a long-running daemon. Very early.

**sema-translator** is the bootstrap identity authority: it mints opaque
encoded names, derives true names for each declaration, and stages canonical
metadata. It has no engine or wire surface -- it is a pure naming authority.
Well-iterated but durable replay is slated for a future milestone.

**mirror** is the version-control remote for Sema stores. It is a
payload-blind append-ingest daemon that validates sequence continuity and
deduplicates idempotently. One mirror serves all component stores. Working.

### Spirit and Its Ecosystem

**spirit** is the intention-storage daemon -- the most complete component in
the estate. It stores entries with domain, kind, description, and importance,
served over a Unix socket. Working.

**spirit-judge** is the LLM edge adapter for Spirit's admission contract.
Working.

### The Infrastructure Daemons

**router** -- the message delivery state machine. It owns message ingress,
pending delivery state, and event-driven delivery gates. Working.

**message** -- the ingress point. A CLI accepts one record, sends a typed
frame to message-daemon, which stamps it with origin credentials and forwards
to router. Working.

**orchestrate** -- workspace orchestration: role ownership, claimed scopes,
handoffs, activity log. The daemon is authority-bound to its own storage and
read-only observations. Working.

**mind** -- central state for Persona agents: memory, work items, thoughts,
relations, notes. Backed by kameo actors and sema-engine. Partially done --
core model exists but migration is in progress.

**harness** -- typed abstraction for interactive AI harnesses (Codex, Claude,
Pi): identity, lifecycle, transcript events, adapter capabilities. Working.

**agent** -- LLM API call daemon. Receives a typed prompt, makes HTTPS calls,
returns a completion. Working.

**lojix** -- the deploy orchestrator for CriomOS. Owns durable deploy state,
live generation set, GC roots, deployment event log, and activation pipeline.
Working.

**listener** -- supervised speech-to-text. Thin client for a listener daemon.
Working.

**mentci** -- programmable human approval surface. Owns UI state, routes
approval verdicts. Partially done.

**aggregator** -- evidence collection from transcripts and repositories.
Working.

**chronos** -- zodiacal time, sunrise/sunset, and twilight events. Working.

**persona** -- the apex integration repository that supervises the component
ecosystem and wires repos through Nix. Current binary is a minimal stub;
component implementations live in their own repos. Hub, not a standalone
daemon.

**forge** -- future build executor daemon. Skeleton only; not in any
production path.

**introspect** -- inspection plane for asking running components for typed
observations. Early prototype.

**upgrade** -- migration scaffold. Skeleton with placeholder policy.

### The Operating System

**CriomOS** is a declarative NixOS platform. Each node's configuration is
generated from a cluster proposal (a Dotos data file in the **goldragon**
repository) through **horizon-rs**, which projects the proposal into per-node
JSON that Nix consumes. Deployments are driven by lojix.

**content-identity** provides content-addressed hashing for the Protos family.
**name-table** provides generic nested module-owned name tables. Both are
small, stable leaf crates.

**standards** is a documentation repository collecting binding conventions:
component naming, Rust practices, micro-component architecture, vocabulary
rules.

## The Honest State

### Two tracks that diverged

The estate has two ways of getting from Ethos declarations to running code,
and they have not yet converged.

The **batch track** works today: you write an Ethos declaration, run
schema-rust (which calls core-ethos, core-nomos, and the Logos Rust
projection), and it emits a signal contract crate. You pin that crate's
revision in your daemon's dependencies, rebuild, and the daemon speaks the new
contract. The protos-engine flake enforces coherence across all the pinned
revisions. This pipeline is complete and in daily use.

The **daemon track** is the intended future: ethos-engine, nomos-engine, and
logos-engine would each run as daemons, receiving Ethos changes as signals,
transforming them through Nomos, and emitting Logos projections
continuously -- a live compiler pipeline. Today, ethos-engine exists but
still carries legacy ingest adapters. Logos-engine has an actor-based daemon
but no tests. There is no nomos-engine daemon at all -- nomos-engine is a
library that runs only inside the batch pipeline.

### What works end to end

- The batch generation pipeline: Ethos source to Rust signal contracts via
  schema-rust. Proven daily.
- Spirit: full daemon, judge, ordinary and meta CLIs, storage. The reference
  component.
- CriomOS deployment: goldragon cluster proposal through horizon-rs and lojix
  to running NixOS nodes.
- The signal-frame wire protocol: contract-shaped framing, exchange
  correlation, stream lifecycle.
- Several infrastructure daemons (router, message, orchestrate, agent,
  harness, aggregator, chronos) are functional within their scopes.
- Editor support for Ethos and Dotos via tree-sitter grammars.
- Protos-engine integration gate enforcing coherence across the estate.

### The biggest gaps

- **No Nomos daemon.** Transformations run only in the batch pipeline. The
  live daemon track cannot function without a Nomos daemon to sit between
  Ethos and Logos.
- **Daemon ingest on old syntax.** Ethos-engine still carries legacy adapters
  from a prior storage topology. It has not fully cut over to the current
  authority-sealed pipeline.
- **Missing meta-signal contracts and CLIs.** Many components have their
  ordinary signal contract but lack the meta-signal contract for privileged
  operations, or lack one or both CLI shims.
- **Sema query algebra unimplemented.** The sema-engine defines query plan
  nodes (constrain, project, aggregate, infer, recurse) but cannot execute
  them yet.
- **Persona is a stub.** The apex integration binary that should supervise all
  daemons is minimal. Component wiring happens through Nix, not through a
  running supervisor.
- **Mind migration incomplete.** The central agent state service has its core
  model but older work tables have not been migrated to the current shape.
- **Forge, introspect, and upgrade are skeletons.** Build execution,
  runtime inspection, and migration cataloging are designed but not built.
