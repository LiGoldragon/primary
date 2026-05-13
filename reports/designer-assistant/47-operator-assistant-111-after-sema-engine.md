# 47 - Operator-assistant 111 after the Sema engine split

*Designer-assistant analysis, 2026-05-14. Scope:
`reports/operator-assistant/111-persona-introspect-contract-dependency-gap.md`
read against the recent Sema work:
`reports/designer/157-sema-db-full-engine-direction.md`,
`reports/designer/158-sema-kernel-and-sema-engine-two-interfaces.md`,
and `reports/designer-assistant/46-review-designer-158-sema-two-interfaces.md`.
Question: what remains true, what is stale, and what should operators
do differently now that `sema-engine` is the planned full
database-operation engine.*

Update 2026-05-14: the user clarified that `persona-introspect` does
own its own database. This report therefore treats
`persona-introspect` as a `sema-engine` consumer for local
introspection state while preserving the socket/contract boundary for
peer inspection.

## 0. Bottom line

Operator-assistant/111 is directionally right about ownership:
`signal-persona-introspect` is an envelope, not a bucket for every
component's rows; `persona-introspect` should fan out to live component
daemons over sockets; component-specific records belong in the owning
component contracts.

The recent Sema design changes the implementation center of gravity.
In /111, every component appears to need its own hand-built
"introspect this time window" query machinery. After /157 and /158,
that shared database work belongs in `sema-engine`:

- component daemons still expose typed introspection over their own
  Signal contracts;
- those daemons answer by lowering typed requests into
  `sema-engine` plans, catalog queries, operation-log reads, and
  subscriptions;
- `persona-introspect` orchestrates and projects; it does not read
  peer redb files and does not reimplement database scans.

So /111 should not be implemented as "add all contract dependencies
and then hand-write per-component observation query loops." It should
be implemented as "add only the dependencies needed by the current
slice, and make those peer daemons expose engine-backed observation
relations."

## 1. What remains correct in /111

### 1.1 Central envelope, not shared schema bucket

/111 lines 8-11, 57-59, and 391-401 are still correct. The central
introspection contract should not absorb router rows, terminal rows,
mind graph rows, harness lifecycle rows, or manager event rows.

That remains true after `sema-engine`. The engine gives components a
common database execution layer, not a permission to move every record
type into `signal-persona-introspect`.

### 1.2 `persona-introspect` may depend on component contracts

/111 lines 21-22 and 250-264 identify the practical gap:
`persona-introspect` currently only depends on `signal-core`,
`signal-persona-auth`, and `signal-persona-introspect`, so it cannot
decode router, terminal, manager, system, harness, mind, or message
records.

That remains true. The runtime projection component is allowed to
depend on many component contracts because it is high-privilege
inspection infrastructure. The anti-pattern is putting all those rows
inside `signal-persona-introspect`, not consuming their owning
contracts from `persona-introspect`.

### 1.3 Live sockets, not peer database reads

/111 lines 371-387 are important and should survive unchanged. The
first tests should prove live introspection crosses daemon sockets and
does not open peer redb files directly.

The `sema-engine` split makes this even more important. Every
state-bearing daemon owns its own `sema-engine::Engine` instance over
its own state file. `persona-introspect` must ask the daemon; it must
not bypass the daemon to read that engine's backing `sema` database.

### 1.4 Client actors owning protocol codecs

/111 lines 347-359 say each component client actor should own its
protocol codec. That is still the right actor topology:

- `RouterClient` speaks `signal-persona-router`;
- `TerminalClient` speaks `signal-persona-terminal`;
- `ManagerClient` speaks `signal-persona`;
- future `MindClient`, `HarnessClient`, `SystemClient`, and
  `MessageClient` speak their own contracts.

`sema-engine` does not change this. It lives behind the peer daemon's
contract surface, not inside `persona-introspect`'s socket layer.

## 2. What is stale or incomplete after `sema-engine`

### 2.1 Per-component query machinery should not be hand-rolled

/111 lines 313-388 recommend wiring real peer queries relation by
relation. That is good as a fan-out plan, but stale as a storage/query
plan if operators interpret it as "each component implements its own
query engine."

After /157 and /158:

- time-window filtering becomes a `sema-engine` query-plan concern;
- record-kind discovery becomes `sema-engine` catalog/list-tables
  introspection;
- operation history becomes `sema-engine` operation-log range queries;
- snapshot identity comes from the engine's commit sequence or
  snapshot cursor;
- subscriptions should use `sema-engine`'s subscription primitive once
  Package 4 lands.

The component daemon still owns the semantic lowering:

```text
signal-persona-terminal::TerminalObservationQuery
  -> persona-terminal daemon validates/authenticates it
  -> daemon lowers it to sema-engine QueryPlan
  -> sema-engine executes against terminal's local state
  -> daemon returns signal-persona-terminal typed observations
  -> persona-introspect projects them
```

That path preserves component ownership without duplicating database
execution.

### 2.2 "Depend on every component contract" needs a slice rule

/111 lines 313-328 already says not to add every dependency at once
unless code immediately uses it. Keep that rule.

The new design strengthens it: adding all component contracts to
`persona-introspect` does not by itself make introspection real. The
dependency only earns its place when there is a peer query and a
witness proving the daemon used that contract over a socket.

Recommended first slice remains manager/router/terminal because /111
is targeting the current prototype witness path. But the slice should
be stated as:

```text
Add signal-persona, signal-persona-router, and
signal-persona-terminal only for the live manager/router/terminal
queries currently being wired. Later dependencies land with later
client actors and tests.
```

### 2.3 There is now a wire-type ownership gap for engine-generic records

The new engine design introduces generic engine records:

- record family descriptors;
- index descriptors;
- operation-log entries;
- snapshot ids;
- validation diagnostics;
- subscription delta metadata.

/111 does not need to solve this because it predates /157-/158, but
the gap is now visible. If these records cross daemon sockets, they
need a contract home.

Three candidate shapes:

1. **Component contracts wrap engine-generic records locally.**
   Example: `signal-persona-terminal` defines
   `TerminalRecordKindDescriptor` or `TerminalOperationLogEntry` as
   terminal-owned projection records. This avoids depending on the
   engine implementation crate in wire contracts but repeats generic
   shape.
2. **A future engine protocol crate owns cross-wire engine records.**
   This is clean if engine plans/logs/descriptors truly cross process
   boundaries. It conflicts with the current "no premature engine
   protocol crate yet" guard from my review of /158, so it should not
   be created before a concrete crossing proves the need.
3. **`signal-persona-introspect` owns only projection wrappers.**
   It can wrap component-owned records for display, but it should not
   own the engine's canonical operation-log or catalog vocabulary.

My recommendation: keep v1 concrete. For the first implementation
slice, avoid crossing generic engine records where possible. Ask
manager/router/terminal for their already-owned status/trace/snapshot
records. When `ListRecordKinds` or `operation_log_range` becomes the
next slice, decide the contract home then with the concrete payload in
front of us.

### 2.4 `persona-introspect` depends on `sema-engine` for its own database

Because `persona-introspect` owns a local database, it should depend on
`sema-engine` for its own observation state, indexes, catalogs, audit
records, projection cache, and query surface. That is local state owned
by the introspection component.

That does not make `sema-engine` the peer-inspection boundary.
`persona-introspect` still reaches peer state by asking peer daemons
over their sockets and typed component contracts. The peer daemon uses
its own `sema-engine` instance internally and returns a typed contract
reply.

The shape to avoid:

```text
persona-introspect opens or imports peer sema-engine state directly
```

The correct shape:

```text
persona-introspect -> sema-engine -> its own introspection database

persona-introspect -> peer daemon socket -> peer contract request
peer daemon -> sema-engine -> local sema state
peer daemon -> peer contract reply -> persona-introspect projection
```

## 3. Revised implementation order

### Step 1 - Keep /111's first prototype slice

Add only the dependencies needed for current live queries:

- `signal-persona`;
- `signal-persona-router`;
- `signal-persona-terminal`.

Wire `ManagerClient`, `RouterClient`, and `TerminalClient` to real
socket round trips. Keep /111's Nix checks:

- manager readiness/health;
- router trace;
- terminal snapshot;
- no peer redb open.

### Step 2 - Make peer daemons' query handlers engine-backed when possible

Where the peer component already has enough state, the peer daemon
should answer by using `sema-engine` once that repo exists. Before
`sema-engine` exists, a narrow local implementation can be a witness
fixture, but it should be marked as temporary and not grown into a
component-private query engine.

The important distinction:

```text
persona-introspect fan-out code: implement now.
component-local query engine duplication: avoid; target sema-engine.
```

### Step 3 - Add engine-catalog introspection as its own design slice

Do not smuggle catalog/list-record-kinds/operation-log vocabulary into
the current prototype witness slice. File a separate design or
implementation slice once `sema-engine` skeleton exists:

- what wire record represents a record-family descriptor;
- what wire record represents an operation-log entry;
- whether those records live in component contracts or a later engine
  protocol crate;
- how `persona-introspect` renders them to Nexus/NOTA.

### Step 4 - Revisit /111's "full first-stack peer set" after Message/Mind/System/Harness contracts stabilize

/111 lines 330-345 correctly list the first-stack peer set. The new
design does not require adding all peers before the prototype witness
works. Add peer clients in the order live introspection needs them.

## 4. Suggested status banner for /111

If operator-assistant/111 remains in the report set, add a banner like
this at the top:

```text
Status after reports/designer/157 and /158:
This report is still correct about the contract ownership boundary:
signal-persona-introspect is an envelope, and persona-introspect
consumes component-owned contracts over daemon sockets. It is stale if
read as "each component must hand-roll its own query/filter/time-window
engine." Shared database mechanics now target sema-engine. Implement
the manager/router/terminal fan-out slice, but route component-local
query execution toward sema-engine as it lands.
```

## 5. Final assessment

/111 is a good dependency-gap report, not a complete implementation
plan after the Sema engine decision.

Use it for:

- contract ownership;
- first fan-out dependencies;
- actor/client shape;
- live socket witnesses;
- avoiding `signal-persona-introspect` bucket drift.

Do not use it for:

- per-component hand-rolled query engines;
- direct peer database reads;
- adding every contract dependency in one broad sweep;
- deciding the wire home for engine-generic catalog/log records.

The next implementation should combine /111's fan-out topology with
/157-/158's engine-backed database execution.
