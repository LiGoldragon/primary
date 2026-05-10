# 3 - ractor-only actor architecture recheck

*Designer-assistant report. This replaces report 2 because report 2
kept a fictitious actor-library idea alive by renaming it. The live
architecture is direct `ractor`; this report intentionally does not
repeat the invented wrapper names.*

---

## 0. Correction

Li's correction is right: giving a hallucinated actor library a nicer
workspace-shaped name still keeps the hallucination alive. The correct
rule is simpler:

> We use `ractor`.

Actor density remains load-bearing. A second actor abstraction is not
current architecture and should not appear in live plans as a step,
dependency, migration, or prerequisite.

---

## 1. Recent reports reread

### `reports/operator/100-persona-mind-central-rename-plan.md`

Keep. It establishes `persona-mind` as the central state component and
does not require any extra actor abstraction. Its old "lock files +
work views" projection wording is stale; later architecture has moved
lock files to compatibility debris.

### `reports/operator/101-persona-mind-full-architecture-proposal.md`

Keep the target shape: central state, actor-dense runtime, typed
envelope, strict write ownership, read-only query path, event append,
commit boundary, and trace/topology tests.

Do not read its actor density as permission to build a generic actor
framework. It means persona-mind must name and test its own runtime
planes.

### `reports/operator/102-actor-heavy-persona-mind-research.md`

Keep the actor-density argument and the direct `ractor` recommendation.
Retire the parts that propose a new actor abstraction layer,
deterministic scheduler layer, virtual-actor layer, or raw-spawn
abstraction as near-term work.

### `reports/designer/100-persona-mind-architecture-proposal.md`

Keep. Its pins for display ID minting, table keys, caller identity,
`MindEnvelope`, and `mind.redb` path remain useful. Interpret any
four-piece raw-ractor wording as implementation mechanics, not
philosophy.

### `reports/designer/101-extreme-actor-system-and-no-zst-actors.md`

Retire as an implementation plan. Salvage only the critique: public
hollow actor nouns are suspicious, and raw ractor's behavior-marker plus
`State` split deserves care. Do not implement its proposed trait, crate,
handle layer, or adoption order.

### `reports/operator-assistant/97-persona-mind-actor-density-compliance-review.md`

Historically useful, now partly overtaken by code. Current persona-mind
already has direct `ractor`, an actor tree, local manifest/trace
witnesses, and actor topology tests. Future compliance checks should
test that real actor path, not demand an exact wrapper or file taxonomy.

---

## 2. Current persona-mind state

I read:

- `/git/github.com/LiGoldragon/persona-mind/AGENTS.md`
- `/git/github.com/LiGoldragon/persona-mind/skills.md`
- `/git/github.com/LiGoldragon/persona-mind/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/persona-mind/Cargo.toml`
- `/git/github.com/LiGoldragon/persona-mind/src/actors/*.rs`
- `/git/github.com/LiGoldragon/persona-mind/tests/actor_topology.rs`

Current state:

- `persona-mind` depends directly on `ractor`.
- It has no extra actor abstraction dependency.
- It starts real long-lived ractor actors:
  `MindRoot`, `Config`, `IngressSupervisor`,
  `DispatchSupervisor`, `DomainSupervisor`, `StoreSupervisor`,
  `ViewSupervisor`, `SubscriptionSupervisor`, and `ReplySupervisor`.
- Smaller domain planes are currently trace phases, not separate spawned
  ractor actors.
- `ActorManifest` and `ActorTrace` are local persona-mind witness types.
- `tests/actor_topology.rs` proves manifest presence, write-path trace,
  commit trace, and read path without `SemaWriterActor`.

That is the right direction: direct ractor plus local witnesses.

---

## 3. Architecture doc improvements

`persona-mind/ARCHITECTURE.md` is broadly up to date. It should add one
explicit boundary so future agents do not re-import the extra
abstraction idea from older reports.

Recommended section after `## 2 - Runtime Topology`:

```md
## 2.1 - Actor framework boundary

`persona-mind` uses `ractor` directly. No second actor abstraction is
required before persistence work proceeds.

The local `actors::manifest` and `actors::trace` modules are
persona-mind architecture witnesses. Keep them local until multiple
real runtime crates duplicate the same concrete API.

Raw ractor splits behavior markers from mutable `State`. Treat that as
framework mechanics. Keep marker types private or crate-private where
possible; domain behavior belongs on data-bearing state, reducers owned
by that state, or public handles.
```

Recommended invariant under `## 6 - Invariants`:

```md
- Production code uses direct `ractor`; no second actor abstraction is
  a dependency or prerequisite.
```

Recommended test expectation:

```md
- no production dependency on a second actor abstraction crate
```

Also update `/git/github.com/LiGoldragon/persona-mind/skills.md`:

```md
- Lock files are compatibility artifacts while the workspace migrates;
  they are not durable truth and should not be regenerated as the
  long-term interface.
```

That replaces the current "lock projections" wording.

---

## 4. ZST rule with direct ractor

The current raw-ractor code has the expected shape:

```rust
pub struct StoreSupervisor;

pub struct State {
    memory: MemoryState,
}

impl ractor::Actor for StoreSupervisor {
    type State = State;
    ...
}
```

This is mechanically normal for ractor. The local improvement is not a
new library. It is tighter naming and ownership:

1. Keep behavior marker structs private or crate-private where possible.
2. Give state structs specific names when they carry domain weight:
   `StoreSupervisorState`, `DispatchSupervisorState`, etc.
3. Put domain methods on those data-bearing state/reducer types.
4. Keep `*Handle` or service facades as the public surface, not raw
   `ActorRef`.
5. Revisit runtime choice only after direct-ractor implementation
   exposes concrete pain.

---

## 5. Lock status

`operator-assistant` currently holds the persona-mind repo:

```text
/git/github.com/LiGoldragon/persona-mind # weird actor truth tests and nix wiring
[primary-9iv] # weird actor truth tests and nix wiring
```

So I did not edit `persona-mind/ARCHITECTURE.md` directly. The patch
above should be applied by the current repo owner or after the lock
clears.

---

## 6. Bottom line

Use direct `ractor`. Actor density is mandatory. A second actor
abstraction layer is not.
