# 38 - Prototype introspection reassessment after designer 146

*Designer-assistant report, 2026-05-13. Scope: fresh reading of
`reports/designer/146-introspection-component-and-contract-layer.md`
after the user's correction that introspection is prototype-critical.*

---

## 0. Position

`reports/designer/146-introspection-component-and-contract-layer.md`
is right about the architecture and wrong about the timing.

The parts that should stay load-bearing:

- Nexus/NOTA belongs at the edge: ingress, egress, inspection, human
  and agent display.
- Signal/rkyv belongs inside the engine: component-to-component
  communication uses typed archived records, not text.
- Sema/redb stores typed rkyv-archived records owned by the component.
- `persona-introspect` must ask live component daemons over Signal. It
  must not open peer redb databases.
- `signal-persona-introspect` should be the central query/reply
  envelope, not a bucket of every component's internal rows.
- Component contracts own the component-specific observation records.

The part that should change:

- `persona-introspect` should move from "planned after prototype" to
  "included in prototype as the inspection plane and acceptance oracle."

That does not make introspection part of the message-delivery path. The
operational first stack can remain the six delivery components. The
prototype's supervised set should become those six components plus
`persona-introspect`, because a prototype that cannot explain itself is
hard to trust and hard to debug.

---

## 1. Where this lands

### 1.1 Component

Create `persona-introspect` as a supervised, high-privilege,
per-engine component.

Names:

- Component and repo: `persona-introspect`
- Binary: `persona-introspect-daemon`
- CLI edge: `introspect`
- Socket: `/var/run/persona/<engine-id>/introspect.sock`

The socket should be internal-only, not user-writable like
`message.sock`. Development mode can be transparent, but the component
is still privileged because it can request engine state from many
daemons.

### 1.2 Contracts

The contract split should be:

| Contract | Owns |
|---|---|
| `signal-persona-introspect` | Introspection request/reply envelopes, selectors, projection wrappers, prototype witness records. |
| `signal-persona` | Manager-owned observations: engine status, component lifecycle, spawn/socket/readiness/process state. |
| `signal-persona-terminal` | Terminal-owned observations: session status, gate/prompt state, delivery attempt summary, transcript pointers later. |
| `signal-persona-router` | Router-owned observations: accepted message, route decision, delivery attempt/result, adjudication status. |
| `signal-persona-message` | Message-ingress observations only if needed: accepted ingress count, last accepted submission, message socket status. |

The most important correction is `signal-persona-router`. There is no
active router contract yet, and introspection creates real pressure for
one. Putting router observations into `signal-persona-introspect` would
turn the central envelope into a shared schema bucket. Putting them into
`signal-persona-message` would pretend routing state is message-ingress
state.

### 1.3 Manager topology

`persona` should distinguish two lists:

- **Operational first stack:** mind, router, system, harness, terminal,
  message.
- **Prototype supervised components:** the operational first stack plus
  introspect.

This keeps the conceptual model clean. Introspection is not a delivery
component, but it is supervised by the manager and belongs in prototype
readiness/status.

The manager and contract enums need an `Introspect` principal/kind in:

- `signal-persona::ComponentKind`
- `signal-persona-auth::ComponentName`
- `persona::EngineComponent` or the successor enum that drives spawn
  envelopes

The wording in `signal-persona-auth` should avoid saying that the closed
component-name enum is only the "first stack" if introspection joins as a
supervised inspection component. A better phrase is "supervised local
component principals", with the operational first stack named separately.

---

## 2. Minimal prototype witness

The first useful introspection slice should be deliberately narrow.

Flow:

1. `persona-daemon` starts mind, router, system, harness, terminal,
   message, and introspect.
2. All seven supervised components answer the common supervision
   relation.
3. A fixture message travels through the normal delivery path:
   `message -> router -> harness -> terminal -> terminal-cell`.
4. The `introspect` CLI sends one NOTA query to `persona-introspect`.
5. `persona-introspect` decomposes it into Signal queries to manager,
   router, and terminal.
6. Manager/router/terminal return typed observation records.
7. `persona-introspect` returns one NOTA projection proving the delivery
   path happened.

The first witness does not need raw transcript bytes. It needs enough
typed state to prove:

- the engine and components were ready,
- the message was accepted,
- the router committed a delivery attempt/result,
- the terminal recorded the relevant session/delivery attempt,
- any unimplemented edge replied through a typed `Unimplemented` record
  instead of silently disappearing.

This makes introspection a correctness witness, not an optional UI.

---

## 3. Gaps to close

### 3.1 Canonical architecture drift

`reports/designer/146-introspection-component-and-contract-layer.md`,
`reports/designer/147-designer-side-report-and-bead-cleanup-2026-05-13.md`,
and `persona/ARCHITECTURE.md` still preserve the old scheduling posture:
introspection is planned, not prototype-critical.

That should be corrected. The format/layering doctrine in `/146` should
stay; the timing and prototype surface should change.

### 3.2 Component vocabulary gap

The current code and contracts name the six operational components but
not `Introspect`. Prototype inclusion requires the closed component
vocabulary to grow. This is a good schema change, not a special case.

### 3.3 Router contract gap

Router state is central to proving delivery, but there is no dedicated
`signal-persona-router` contract. The prototype can either avoid router
observations, which weakens the witness, or create the router contract.
The second option is better.

### 3.4 Observation shape gap

The first records should be summary observations, not raw table mirrors.
For example, terminal does not need to expose every stored row. It needs
a delivery/session observation that says what terminal, what generation,
what attempt sequence, what state, and what prompt/gate condition.

Raw row dumps will make the contract brittle and will pull internal
storage accidents into the public architecture.

### 3.5 Projection ownership gap

Existing code has some NOTA projection near the manager CLI surface. That
is acceptable as today's local display path, but the prototype
introspection path should establish the future rule:

- component daemons return typed Signal records,
- `persona-introspect` owns the projection to NOTA at the edge.

### 3.6 Direct-redb bypass gap

The easiest bad implementation is to let `persona-introspect` inspect
peer database files directly. That would break the component ownership
model and make tests lie about the real engine topology.

Add a witness that rejects peer redb opens from `persona-introspect`. If
`persona-introspect` later gets its own `introspect.redb`, that is a
different database and should be explicitly scoped as its own audit or
subscription state.

### 3.7 Actor-shape gap

`persona-introspect` is a good actor component, but only if the actors
carry real state:

- `IntrospectionRoot`: daemon configuration and child actor refs.
- `TargetDirectory`: engine id and peer socket map from the spawn
  envelope.
- `QueryPlanner`: decomposition of one user query into target-specific
  Signal requests, with correlation ids.
- `ManagerClient`, `RouterClient`, `TerminalClient`: connection state and
  target-specific failure handling.
- `NotaProjection`: projection policy and display options.

Do not create zero-sized actors just to match a topology diagram.

---

## 4. Problems to watch

### 4.1 Bucket drift in `signal-persona-introspect`

The central envelope should not become `all-engine-types.rs`. It should
ask, wrap, correlate, and project. Component state belongs in the
owning component's contract.

### 4.2 Prototype bloat

Introspection is important enough to include early, but the first slice
must stay small. Manager, router, and terminal are sufficient for the
first delivery witness. Mind/system/harness-specific observations can
arrive after the first query works.

### 4.3 Privacy by accident

Development mode can be transparent, but typed observations should still
make non-exposure explicit. Private keys and raw transcript bytes should
not appear in the first witness. If a field is withheld later, model that
as a typed projection result, not a string redaction heuristic.

### 4.4 Circular tests

The witness must query live daemons. It should not prove delivery by
reading the Nix test's own fixture files, parsing stdout, or opening
component databases. Otherwise introspection becomes another test script,
not an engine surface.

### 4.5 Naming drift

Do not call the component `persona-introspect-daemon`. Per
`reports/designer/145-component-vs-binary-naming-correction.md`, the
component is `persona-introspect`; `-daemon` is binary/file-level only.

---

## 5. Recommended landing order

1. Update canonical architecture to say `persona-introspect` is included
   in prototype acceptance as the inspection plane, while the operational
   delivery path remains the six-component first stack.
2. Add `Introspect` to the supervised component vocabulary in
   `signal-persona`, `signal-persona-auth`, and `persona`.
3. Create `signal-persona-introspect` with only central query/reply
   envelopes and prototype witness wrappers.
4. Create `signal-persona-router` before router observations are needed.
5. Add minimal manager, router, and terminal observation records in their
   owning contracts.
6. Create a stateless `persona-introspect` daemon and CLI.
7. Add a Nix witness named around the actual outcome, for example
   `persona-prototype-delivery-is-introspectable`.
8. Add guardrail witnesses: no peer redb opens, NOTA projection at the
   introspect edge, internal-only `introspect.sock`, Signal target
   relations only.

Bottom line: implement it with the prototype, but keep it as an
inspection plane. The engine should not merely run a path; it should be
able to explain that path through its own typed component boundaries.
