# 48 - Persona-introspect start shape and open questions

*Designer-assistant report, 2026-05-14. Written for the operator
assistant before starting work on `persona-introspect`. Reads the current
architecture through the latest Sema split: `persona-introspect` is a
fan-out inspection daemon, a NOTA projection edge, and now also an owner
of its own local introspection database. It is still not a peer database
reader and not a central store of peer truth.*

## 0. Current View

`persona-introspect` should be the development inspection plane for the
Persona engine. It exists so humans, agents, and later UIs can ask "what
is the engine doing?" without joining the operational delivery path.

It has three surfaces:

1. **Ingress and projection.** The `introspect` CLI and
   `persona-introspect-daemon` socket speak `signal-persona-introspect`.
   Nexus/NOTA appears at the CLI/UI edge only. Inside the engine, the
   payloads stay typed Signal/RKYV records.
2. **Peer fan-out.** `persona-introspect` asks live component daemons
   over their sockets. Each client actor speaks that component's own
   signal contract. Peer truth stays in the peer daemon.
3. **Local introspection database.** `persona-introspect` owns its own
   database through `sema-engine` for what *introspect itself* knows:
   target catalog, query/audit trail, observed reply metadata,
   projection cache, and eventually subscriptions over its own
   observations.

The most important boundary:

```text
allowed:
persona-introspect -> sema-engine -> introspect.redb
persona-introspect -> peer daemon socket -> peer contract request
peer daemon -> sema-engine -> peer-owned redb
peer daemon -> peer contract reply -> persona-introspect

forbidden:
persona-introspect -> peer sema-engine instance directly
persona-introspect -> peer redb file directly
signal-persona-introspect -> bucket of every component row type
```

So the component is not "just a proxy" anymore, but it is also not the
engine's central database. It is a high-privilege observation component
that records and projects its own observations.

## 1. What Already Exists

`persona-introspect/ARCHITECTURE.md` already says the component is not in
the message delivery path and proves that path after the fact. It owns
the daemon, CLI, Kameo actors, fan-out to component daemons, fan-in of
typed observations, and NOTA projection.

The current code has useful scaffolding:

- `persona-introspect-daemon` binds `introspect.sock` and handles
  `signal-persona-introspect` frames.
- `introspect` CLI exists and accepts one NOTA input record.
- `IntrospectionRoot` is a Kameo actor with child actors:
  `TargetDirectory`, `QueryPlanner`, `ManagerClient`, `RouterClient`,
  `TerminalClient`, and `NotaProjection`.
- `signal-persona-introspect` has the current envelope scopes:
  `EngineSnapshot`, `ComponentSnapshot`, `DeliveryTrace`, and
  `PrototypeWitness`.

What is still scaffold:

- `ManagerClient`, `RouterClient`, and `TerminalClient` hold socket
  paths but do not send real component-contract requests.
- The CLI only has `PrototypeWitness` as an input shape.
- `signal-persona-introspect` has no `ComponentObservations` shape for
  "give me component records in this range."
- `persona-introspect` has no local database yet.

## 2. Contract Ownership

`signal-persona-introspect` is the central envelope contract. It should
own selectors, correlation, wrapping, unimplemented/denied replies, and
projection-facing records.

It should not own component row vocabularies. Router observations belong
in `signal-persona-router`; terminal observations belong in
`signal-persona-terminal`; manager lifecycle/status observations belong
in `signal-persona`; and so on.

The runtime daemon may depend on the component contracts it actually
uses. The contract crate should not import them all just to become a
mega-schema.

The right split:

```text
signal-persona-introspect
  envelope, target names, query wrappers, correlation, projection wrappers

component signal contracts
  component-owned observation records and component-owned introspection
  query/reply relations

persona-introspect daemon
  depends on signal-persona-introspect plus the component contracts used
  by the current implementation slice
```

## 3. Local Database Shape

The user clarified that `persona-introspect` has its own database. That
database should be component-owned state, not a shadow copy of every peer
database.

Recommended first tables, once `sema-engine` is available:

| Record family | Purpose |
|---|---|
| `ObservedTarget` | Engine id, target kind, socket path or resolved endpoint, last contact result, last seen snapshot/sequence if available. |
| `IntrospectionQueryRecord` | Query id, engine id, target/scope, requested filter, requested at, caller/origin if available. |
| `IntrospectionReplyRecord` | Query id, reply status, peer snapshot/sequence, component origin, observed at, payload kind. |
| `ProjectionRecord` | Optional cached NOTA/projection output keyed by query id and projection format/version. |
| `IntrospectionErrorRecord` | Peer missing, peer unreachable, unimplemented, denied, decode failure, timeout, malformed reply. |

Payload policy is the part that needs the user's decision. The database
can store full peer observation payloads as "what introspect observed,"
or it can store only metadata and ask peers again for the full payload.
Both are coherent:

- Full payload cache is better for development, replay, and reports.
- Metadata-only is stricter about not duplicating peer truth.

My recommendation for development is full payload cache with an explicit
origin and snapshot/sequence on every cached item. It should be framed as
"record of what introspect saw," not "authoritative peer state."

## 4. Actor Topology

The current actor map is close but needs one more state-bearing actor.

Recommended v1 actor planes:

| Actor | State it carries | Job |
|---|---|---|
| `IntrospectionRoot` | child actor refs, local config | Root supervision and request dispatch. |
| `TargetDirectory` | known targets and socket paths | Resolve engine/target to peer socket. |
| `QueryPlanner` | supported scopes and target capability table | Turn envelope request into peer request plan. |
| `IntrospectionStore` | `sema-engine::Engine` for `introspect.redb`, or a typed unavailable state before engine exists | Persist local query/reply/error/projection records. |
| `ManagerClient` | manager socket + codec state | Speak `signal-persona` to persona-daemon. |
| `RouterClient` | router socket + codec state | Speak `signal-persona-router`. |
| `TerminalClient` | terminal socket + codec state | Speak `signal-persona-terminal`. |
| Later clients | each socket + codec state | Mind, harness, system, message. |
| `NotaProjection` | projection version/config | Render typed replies to NOTA only at the edge. |

Every actor should carry state. No public zero-sized actor types. If
`sema-engine` is not available yet, `IntrospectionStore` can carry a
typed `StoreState::Unavailable { reason }` plus the intended database
path, but it should not pretend persistence exists.

## 5. Suggested Operator-assistant Start

This work should attach to the operator lane, probably existing bead
`primary-0uy2` ("persona-introspect: store local observation state
through sema-engine"). The operator currently owns the `sema-engine`
scaffold, so operator-assistant should avoid racing that repo. Good
parallel work lives in `persona-introspect` and its immediate contracts.

Recommended first pass:

1. Update `persona-introspect/ARCHITECTURE.md` to state explicitly:
   `persona-introspect` owns `introspect.redb`; local state goes through
   `sema-engine`; peer state only crosses daemon sockets.
2. Add the actor topology target to the architecture:
   `IntrospectionStore` sits beside client actors, not inside them.
3. Add source/witness tests that can pass before `sema-engine` exists:
   no peer redb opens, no direct `redb::Database::open` on peer paths,
   no component row vocabulary added to `signal-persona-introspect`.
4. Once `sema-engine` is available by git revision, add the
   `IntrospectionStore` skeleton and local database schema records.
5. Add only the component contract dependencies needed for the first
   live peer slice. Do not add every component contract in one sweep.
6. Wire one real peer round trip end-to-end, with a typed
   unimplemented/unavailable path if the peer has no observation
   relation yet.

Recommended first peer slice depends on the user's answer below. My
default would be:

```text
manager first for engine/component status,
then router for delivery trace,
then terminal for terminal observations.
```

That keeps the existing `PrototypeWitness` path honest before widening
into arbitrary component observations.

## 6. Witnesses

Minimum witnesses for operator-assistant:

| Witness | What it proves |
|---|---|
| `introspect_arch_names_local_database` | Architecture says `persona-introspect` owns `introspect.redb` through `sema-engine`. |
| `introspect_does_not_open_peer_redb` | Source/test scan forbids peer database opens in live path. |
| `signal_introspect_is_envelope_not_bucket` | `signal-persona-introspect` does not define router/terminal/mind row vocabularies. |
| `introspection_store_actor_carries_state` | Store actor is not a zero-sized actor; it carries DB config and engine/store state. |
| `prototype_witness_records_query_locally` | Once store exists, a prototype witness request writes a local query/reply record. |
| `peer_unreachable_is_typed` | Missing/unreachable peer returns a typed introspection unavailable/unimplemented reply and records an error locally. |
| `nota_projection_is_edge_only` | CLI output is NOTA, but peer/client layers exchange typed Signal records. |

Later witnesses:

- `component_observations_round_trip`
- `component_observation_cache_has_origin_and_snapshot`
- `introspect_local_db_reopens_with_schema`
- `introspect_subscribe_initial_snapshot`
- `introspect_does_not_add_unused_component_contract_dependency`

## 7. Unclear Intent

These are the points that need user clarification before this becomes
fully implementation-ready.

### Q1 - What exactly should introspect persist?

Should `introspect.redb` store full peer observation payloads as an
audit/replay cache, or only metadata/pointers to peer observations?

My recommendation: full payload cache for development, with
`origin_component`, peer snapshot/sequence, observed-at timestamp, and
query id. Treat it as "what introspect saw," not peer truth.

### Q2 - Does local database work wait for `sema-engine`?

`sema-engine` is the target storage interface, and the operator is
currently scaffolding it. Should operator-assistant wait for that repo
before touching `persona-introspect` persistence, or should they land
architecture + actor skeletons with `StoreState::Unavailable` first?

My recommendation: land architecture/tests/skeleton first, add the
actual `sema-engine` dependency only when it exists by git revision.

### Q3 - Which peer slice starts first?

Options:

- manager first: best for engine status and prototype readiness;
- router first: best for message/delivery trace;
- terminal first: matches older designer guidance and has concrete
  operational observations;
- harness first: exposes a currently weak testing surface.

My recommendation: manager -> router -> terminal, because that turns the
existing `PrototypeWitness` from scaffold into a real live witness.

### Q4 - Do we add `ComponentObservations` now?

The current envelope scopes are useful aggregations. The missing general
primitive is "target this component and return observations for this
filter/range." Should that land now, or should v1 only make the current
four scopes real?

My recommendation: make the current four scopes real first, then add
`ComponentObservations` after one peer relation proves the shape.

### Q5 - Are raw peer payloads allowed in development projections?

If full payload cache is allowed, `introspect` can replay and render old
observations even if the peer is down. If not, `introspect` becomes
stricter but less useful during debugging.

My recommendation: allow raw typed payload caching in development, but
never as an authority source. Private keys and similar secrets should
remain non-introspectable.

### Q6 - Should subscriptions be in v1?

Push subscriptions fit the full Sema engine direction, but they depend
on commit-then-emit machinery. Should `persona-introspect` start with
snapshot queries only?

My recommendation: v1 is snapshot/query only; subscriptions begin after
`sema-engine` Subscribe and `persona-mind` first-consumer work land.

## 8. Bottom Line

Operator-assistant can start useful work now, but the scope should be
careful:

- update architecture around `introspect.redb`;
- add guard witnesses;
- add the store actor skeleton;
- keep peer truth behind sockets;
- do not add all component contracts at once;
- do not hand-roll a private query engine while `sema-engine` is being
  built.

The main design choice left is whether `persona-introspect`'s own
database is an audit/replay cache of full observed payloads or only a
metadata ledger. That answer shapes the first schema.
