# Skill - engine analysis

*How to inspect a multi-component engine from code, contracts, runtime
topology, state, and trust boundaries, then write a reusable compendium.*

---

## What this skill is for

Use this skill when asked to explain how an engine currently works, what talks
to what, which paths are wired in code, which paths are only architectural, and
what state each component owns.

The output is an analysis report, not a rewrite plan by default. Code beats
architecture: every claim must say whether it is **hooked**, **stubbed**,
**contract-only**, **conceptual**, or **stale**.

## Reading order

1. Read workspace intent and coordination: `ESSENCE.md`,
   `repos/lore/AGENTS.md`, `orchestrate/AGENTS.md`, and
   `protocols/active-repositories.md`.
2. Read the apex engine repo `ARCHITECTURE.md`, then each component repo's
   `AGENTS.md`, `skills.md`, `ARCHITECTURE.md`, `TESTS.md`, and code map.
3. Read every contract crate on the engine fabric before judging channels.
4. Read runtime code, daemon/client entrypoints, Nix apps/checks, scripts, and
   tests that witness the runtime path.
5. If the task asks for outside research, borrow vocabulary from established
   architecture methods without importing their process wholesale:
   C4 zoom levels for system/container/component views, arc42 building-block,
   runtime, deployment, and crosscutting-concept sections, SEI views for
   module/component-and-connector/allocation separation, DFD trust boundaries
   for security, and trace/span language for worked request paths.

## Analysis passes

### 1. Engine Boundary Map

List the engine, components, processes, binaries, sockets, state roots, and
deployment/sandbox entrypoints. Mark which processes actually launch today.

### 2. Channel Ledger

For each channel, record:

| Field | Question |
|---|---|
| Producer | Who writes or initiates? |
| Consumer | Who reads or handles? |
| Contract | Which `signal-*` crate or byte protocol defines the payload? |
| Transport | Unix socket, raw PTY stream, CLI stdout, file, database, etc. |
| Payloads | Closed request/reply/event variants that cross the boundary. |
| Authority | Which side mints sender, origin, time, slots, IDs, revisions? |
| State effect | Which component state can change after receipt? |
| Status | Hooked, stubbed, contract-only, conceptual, or stale. |

Call out contract-version skew and duplicated wire types.

### 3. Component State Machine

For each component, name:

- entrypoints and public surface;
- long-lived actors or blocking workers;
- state fields and durable tables;
- messages/events handled;
- transition rules;
- logs/traces/events written;
- what the component refuses to own.

Actors should carry state. If a type is only a forwarding shell, say so.

### 4. Flow Traces

Work through concrete examples end to end. Each example should include:

1. inbound payload;
2. transport and contract;
3. actor/mailbox path or direct call path;
4. durable writes and in-memory mutations;
5. reply/event emitted;
6. downstream possible effects;
7. current breakpoints where the path stops.

Use trace/span language: one request path, named steps, and propagation across
process boundaries.

### 5. Trust, Permissions, And Auth

Map the trust boundaries separately from message payloads:

- Unix socket owner/mode, runtime directory, system user, and filesystem ACLs;
- provenance tags carried as audit context;
- cryptographic verification services, keys, signatures, revocation, replay;
- inter-engine or inter-persona channels;
- which checks are implemented versus planned.

Do not treat provenance tags as runtime auth gates unless code does.

### 6. Observability

Inventory logs, structured events, traces, transcript storage, worker lifecycle
events, daemon stderr, database event tables, and CLI output. Say what is
durable, what is memory-only, and what is merely a test witness.

### 7. Witness Inventory

List tests by constraint, not by filename only. A good witness proves the
intended component path was used, not just that visible behavior succeeded.

### 8. Drift And Next Questions

Separate findings into:

- **wired facts**: code does this now;
- **stubbed facts**: valid request returns typed unimplemented or placeholder;
- **contract-only facts**: shared types exist, no daemon path yet;
- **conceptual facts**: architecture says it, code does not;
- **stale facts**: docs, skills, reports, or code names contradict current truth.

Questions for the human must be self-contained: restate the concrete code fact,
why it matters, and the options.

## Report Shape

An engine compendium report should include:

1. a one-screen current-state summary;
2. a diagram of hooked versus planned component paths;
3. a channel ledger table;
4. one page per component;
5. worked flow examples;
6. trust/auth and state-storage summary;
7. witness/test inventory;
8. gaps and decision questions.

Prefer tables and small Mermaid diagrams. Use local file links for code and
plain URLs for external method references. Keep history secondary; current code
and current architecture are primary.
