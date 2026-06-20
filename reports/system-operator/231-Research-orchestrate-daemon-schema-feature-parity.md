# 231 - Orchestrate daemon schema feature parity

Variant: Research

## Intent anchors

This research treats the real `orchestrate-daemon` as the replacement target,
not the primary workspace compatibility helper.

- Spirit `5d5o`: the orchestrate component itself must be kept on the current
  triad, Signal, SEMA, and runtime crate set; compatibility helper lockfile
  work is not a substitute.
- Spirit `3d5z`: SEMA owns durable state, Nexus owns decision-making, and
  Signal owns communication.
- Spirit `a71r`: every component engine defines and uses Signal, Nexus, and
  SEMA interfaces in schema, with core logic passing through schema-emitted
  traits.
- Spirit `7l7l`: SEMA classification vocabulary stays off the public Signal
  contract wire.

The compatibility goal is therefore feature parity through domain Signal
operations, Nexus decisions, and SEMA read/write interfaces. It is not preserving
the old shell argument surface.

## Current state

Primary's `tools/orchestrate` is now only a shell shim to
`orchestrate-cli/target/release/orchestrate`. That compatibility helper still
owns command-line argument decoding, lazy daemon startup, `.beads` path refusal,
text status rendering, BEADS listing, `verify-jj`, and the release guard.

The real component in `repos/orchestrate` is already the daemon shape:

- `orchestrate-daemon` owns the store and daemon lifecycle.
- `orchestrate` is the ordinary one-argument Signal client.
- `meta-orchestrate` is the meta-policy one-argument Signal client.
- ordinary, meta, and upgrade sockets are separate.
- generated `src/schema/{nexus,sema,daemon}.rs` modules are in the runtime path.
- `orchestrate.sema` stores durable state through `sema-engine`.
- legacy lock files are downstream projections, not the source of truth.

Direct daemon calls through the ordinary socket worked in the live primary
workspace. `Observe Roles` returned a current `RoleSnapshot`, including active
claims, and `Observe Lanes` returned `(LanesObserved [])`. That proves the
daemon already provides lock-equivalent status, while also showing that the
live lane registry is not populated for the fixed role set.

## Feature parity matrix

| Feature | Helper owner today | Daemon/schema state | Required schema destination |
|---|---|---|---|
| Claim path or task scope | Helper normalizes argv and rejects `.beads` path scopes | Ordinary `Claim` executes through the daemon and projects lock files | Keep `Claim` in ordinary Signal; move forbidden-scope policy into Nexus validation and return a typed claim rejection |
| Release | Helper runs `verify-jj` before sending `Release` | Daemon removes the role's claims directly | Make release safety mandatory in Nexus before SEMA write; add typed release rejection for repository blockers |
| Status | Helper renders text and appends BEADS output | `Observe Roles` already returns structured role and claim state | Treat `RoleSnapshot` as the daemon status surface; text rendering is client-side |
| Lanes | Helper reports fixed lane lock files | Meta `Register`, `SetAuthority`, and `Retire Lane` exist; live `Observe Lanes` is empty | Seed or project fixed roles into lane registry, or explicitly declare `RoleSnapshot` the fixed-lane surface |
| `verify-jj` | Helper scans active repositories and local `push-*` bookmarks | No daemon operation | Add ordinary repository-bookmark verification request/reply, with Nexus running the `jj` effect and SEMA reading repository/claim context |
| BEADS open work list | Helper shells out to `bd --readonly list` | Not orchestrate-owned | Do not add BEADS to orchestrate daemon; move ready-work status to the future work graph or `mind` surface |
| Daemon startup | Helper lazily builds and starts daemon from argv command | Daemon supports binary startup and typed sockets | Replace helper startup with a managed user service or typed bootstrap path; this is process integration, not ordinary Signal |
| Watch/unwatch | Helper has no daemon stream usage | `Watch` and `Unwatch` allocate and close tokens | Implement current-state plus delta `ObservationStream` delivery for claim, role, lane, and activity changes |

## Schema shape

The ordinary Signal contract should stay domain-level and peer-callable. It can
name `Claim`, `Release`, `Handoff`, `Observe`, `Submit`, `Query`, `Watch`,
`Unwatch`, and a repository verification operation. It must not expose SEMA
verbs such as validate, assert, mutate, retract, or match.

The meta Signal contract should stay topology and policy focused: create or
retire roles, register or retire lanes, set lane authority, refresh repository
indexes, and configure daemon policy where that policy is mutable.

The Nexus schema needs more first-class work than the current generic
`SignalArrived -> CommandSemaWrite -> ReplyToSignal` loop expresses. The next
useful named decisions are forbidden-scope rejection, release safety checking,
repository bookmark verification, lane seeding policy, and projection decisions.

The SEMA schema should grow beyond broad `ApplyOrdinary(OrdinaryInput)` and
`ApplyMeta(MetaInput)` wrappers. Durable state operations should be named
directly: read claims, read roles, read lanes, read activity, read repository
index, apply claim, apply release, apply handoff, append activity, register
lane, retire lane, set lane authority, refresh repository index, and record
verification results if those results become durable.

## Recommended slice order

1. Move `.beads` forbidden path handling from `orchestrate-cli` into daemon
   claim validation, with a typed ordinary Signal rejection.
2. Add release safety to daemon release handling: Nexus reads claim and
   repository context, runs a repository bookmark verifier effect, and commands
   SEMA release only when clean.
3. Add a standalone repository bookmark verification ordinary operation so the
   `verify-jj` behavior is reachable without the compatibility helper.
4. Decide lane status semantics, then either seed fixed lanes into
   `lane_registry` or document that fixed-role status is `Observe Roles`.
5. Implement real observation streams that emit current state and deltas.
6. Modernize `signal-orchestrate` and `meta-signal-orchestrate` so generated
   schema nouns are the public Rust surface, then shrink the projection bridge
   in `orchestrate/src/execution.rs`.
7. Install a managed daemon service or typed bootstrap path, then update primary
   documentation to use one-argument NOTA clients and retire the helper or label
   it as an explicit temporary adapter.

## Open questions

- Should agent-facing status continue to include the BEADS open-work list until
  a work graph exists? If yes, that aggregation should sit outside orchestrate,
  because BEADS is not orchestrate state.
- Should release safety be overridable? The safer default is mandatory checked
  release, with any emergency override made explicit through meta policy.
- Should every fixed role become a lane registry row? That would make
  `Observe Lanes` useful immediately and align dynamic and fixed-lane status.

## Bottom line

The daemon can already replace the helper for core claim and role observation.
It cannot yet replace the helper as the default agent-facing tool because the
release guard, repository verification, `.beads` claim policy, lane population,
and real watch streams are not all represented as Signal/Nexus/SEMA schema
interfaces. Those are the parity gaps to close; argv compatibility and BEADS
shell aggregation should not be carried into the daemon as design goals.
