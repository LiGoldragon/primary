*Kind: Design · Topic: next-as-dependency-design · Date: 2026-05-24*

# 317/3 · Design — next-as-dependency upgrade path

*Subagent C of the parallel three-way designer dispatch.
Captures spirit record 366 (Decision · Maximum): the upgrade
path is encoded by the next-version schema crate being a Cargo
dependency of the current schema crate, giving the macro
compile-time visibility into both schemas and letting it emit
`VersionProjection` impls at the current crate's compile time.
Sits inside the macro-convergence epic (spirit 367 Maximum) as
one of four concerns the `signal-frame-macros` extension surface
absorbs.*

## §0 Where this design lands relative to the audits

Subagent A (`./1-sema-upgrade-path-audit.md`) reports the deployed
state of the upgrade path: where `VersionProjection` lives, what
the live `mirror_with_projection` consumer expects, and what
gaps the Spirit pilot still has. Subagent B
(`./2-macro-current-state-audit.md`) reports what
`signal_channel!` emits today and what the eight macro beads still
need. This design is the third leg: the **per-pair projection
emission** that connects them.

Concretely: A's audit shows the consumer surface (the
`Projection: VersionProjection<Source, Target, Error =
ProjectionError>` trait bound at
`/git/github.com/LiGoldragon/sema-upgrade/src/handover.rs:226`).
B's audit shows the emitter surface (the `signal_channel!`
parser in
`/git/github.com/LiGoldragon/signal-frame/macros/src/parse.rs:29`
and emitter in
`/git/github.com/LiGoldragon/signal-frame/macros/src/emit.rs`).
The next-as-dep design joins them: it adds the missing emission
that satisfies the consumer's trait bound, given two schema crates
in scope at compile time.

The ground-truth example throughout this design is the live
Magnitude widening migration at
`/git/github.com/LiGoldragon/sema-upgrade/src/migrations/persona_spirit/version_0_1_0_to_0_1_1.rs`,
where a hand-written `historical` module mirrors the old shape,
`current_shape` mirrors the new shape, and `impl
From<historical::Certainty> for Magnitude` at lines 303-311 carries
the only domain-specific transform code. **The next-as-dep design
replaces the hand-mirrored `historical` module with a real
dependency on the historical crate; the `From` impl stays hand-
written; the `VersionProjection` impl that wraps it becomes
macro-emitted.**

## §1 The Cargo mechanic

The schema crate must be able to name a different version of itself
as a direct dependency. Three candidates evaluated.

### §1.1 Candidate A — Cargo rename via `package =` directive

**RECOMMENDED.** The current crate's `Cargo.toml` declares the
next crate under a renamed alias:

```toml
# In signal-persona-spirit v0.1.0's Cargo.toml
[dependencies]
signal-persona-spirit-next = { version = "0.1.1", package = "signal-persona-spirit" }
```

Cargo's `package` rename directive (a stable feature in the
Cargo manifest format) lets one crate depend on a published crate
under a different local name. The renamed alias produces a Rust
path identifier (`signal_persona_spirit_next::...`) the macro can
emit directly. The published crate name on crates.io / git is
unchanged — the renaming is purely local to the current crate's
build graph.

Why this wins:

- **Zero crate-naming churn.** Today's published crates
  (`signal-persona-spirit`, `signal-version-handover`, etc.) keep
  their names. Operators reading `protocols/active-repositories.md`
  see the same names as before. No mass rename across the
  workspace.
- **Single source of identity.** The publishing crate has one
  name; the alias is a local view. There is no risk of a
  `signal-persona-spirit-v0_1_0` and `signal-persona-spirit` both
  existing under different identities and drifting.
- **The macro emits a determinate path.** Inside the current
  crate, `signal_persona_spirit_next::Operation` is a real path.
  The macro can generate `impl VersionProjection<Self::Operation,
  signal_persona_spirit_next::Operation> for ...` without
  guessing.
- **Cycle-free by construction.** v0.1.0 depends on v0.1.1; the
  reverse never holds (see §3).
- **One named convention.** Every schema crate's `Cargo.toml`
  has at most one `*-next` alias. Sub-agents reading the
  manifest see the upgrade path immediately.

The Cargo `package =` directive is documented under the manifest
format's `[dependencies]` table; no extra Cargo feature flag is
needed.

### §1.2 Candidate B — separate crate-per-version naming (REJECTED)

Each version lives in its own crate name:
`signal-persona-spirit-v0_1_0`, `signal-persona-spirit-v0_1_1`.
The "current" pattern becomes "v0_1_0 happens to be re-exported
under the plain name."

Rejected because:

- **Doubles the crate count permanently.** Every component triad
  becomes a `<comp>-v0_1_0` + `<comp>-v0_1_1` pair plus a plain
  `<comp>` umbrella. Worse, the umbrella crate needs republishing
  every time the alias flips, creating a third moving part.
- **Breaks the AGENTS.md `<component>` triad name discipline.**
  AGENTS.md §"Component triad means daemon + working signal +
  policy signal" names the working signal crate as
  `signal-<component>` — singular, with no version suffix in the
  crate name. The version lives in `Cargo.toml` `version`, not in
  the crate name. This candidate would require an exception to a
  named rule.
- **Forces every external dependent to update.** Today a sandbox
  test that imports `signal_persona_spirit` would have to choose
  `signal_persona_spirit_v0_1_0` or `signal_persona_spirit_v0_1_1`
  on every cutover. Operator churn.
- **The plain `signal-persona-spirit` umbrella crate has to be
  a re-export of one specific version.** Which version? Whichever
  is "current" — but then the umbrella crate's identity is
  ambiguous during the handover window.

### §1.3 Candidate C — path-only / git-pinned alias (REJECTED)

Use `path = "../signal-persona-spirit-next"` or `git = "...",
rev = "abc123"` to point at the next-version sources.

Rejected because:

- **Path dependencies don't survive publication.** Cargo's
  `publish = true` strips path dependencies; the cratesio version
  must use a version selector. (The workspace today uses
  `publish = false`, so this is technically allowed today, but the
  rule weakens the workspace's ability to publish-when-ready.)
- **Git pins break reproducibility unless `Cargo.lock` is also
  committed everywhere.** The workspace runs ghq checkouts under
  `/git/...`; pinning a sibling crate by git rev couples every
  dependent to a specific commit. The `package = "..."` rename
  with a version selector survives any lock-file refresh.
- **It hides the version step in the URL.** Operators reading the
  manifest see `git = "..."`, not `0.1.1`. The intent of the
  declaration — "we depend on the NEXT version, which is 0.1.1" —
  is encoded by spelling the version explicitly.

The shape that survives all three failure modes is Candidate A.

## §2 The macro consumption mechanism

Given v0.1.0 and v0.1.1 both in scope at v0.1.0's compile time,
how does `signal_channel!` actually emit the projection?

### §2.1 Candidate A — `signal_channel!` gains a `next_schema:` attribute

**RECOMMENDED.** The macro grammar grows one top-level keyword,
`next_schema`, whose body names the next-version crate's
operation/reply enum modules:

```rust
// In signal-persona-spirit v0.1.0's src/lib.rs

signal_channel! {
    channel Spirit {
        operation State(Statement),
        operation Record(Entry),
        operation Observe(Observation),
        operation Watch(Subscription) opens DomainStream,
        operation Unwatch(SubscriptionToken),
    }
    reply Reply {
        // ...
    }
    next_schema {
        crate signal_persona_spirit_next;
        // optional: explicit pair mapping when the variant set
        // changes; default is "same name maps to same name."
        operation Record => signal_persona_spirit_next::Operation::Record;
    }
}
```

The next_schema block is the natural extension of the
existing top-level keyword grammar at
`/git/github.com/LiGoldragon/signal-frame/macros/src/parse.rs:11-27`
(`reply`, `event`, `stream`, `observable` already follow the same
syntactic shape). The parser learns one more `syn::custom_keyword!`
plus a small `Parse` impl mirroring the existing
`ObservableBlockSpec` pattern.

Why this wins:

- **One macro, one site of truth.** The contract crate has a
  single source of declarative truth for its wire shape AND its
  upgrade-projection. An operator reading the crate sees
  everything in one block.
- **Cohesion with `assert_triad_sections!` and the other
  emissions.** /307 §2.2 already shows the macro emitting daemon-
  side coordination via a sibling helper. next-as-dep is the same
  kind of cross-version-coupling concern; it belongs in the same
  macro family.
- **The macro convergence epic (spirit 367) bundles four
  concerns into one extension surface.** Splitting next-as-dep
  into a sibling macro would split the same epic across two
  macros, exactly the convergence the epic argues against.
- **Per-variant default sane.** When v0.1.0 → v0.1.1 is purely
  additive at the variant level (the Spirit Magnitude case —
  `Statement`, `Entry`, etc. stay named the same), the macro
  defaults to mapping `Operation::Record` to
  `next_crate::Operation::Record` automatically. Explicit
  per-variant mapping is needed only when a variant is renamed
  or split — and then it's a one-line addition.

### §2.2 Candidate B — sibling macro `version_projection!` invoked separately (REJECTED)

A second proc-macro `version_projection! { current = ..., next = ...
}` invoked separately inside the contract crate.

Rejected because:

- **Two declarations to keep in sync.** The contract crate now
  has a `signal_channel!` block AND a `version_projection!` block.
  Adding a new operation requires editing both; forgetting to
  edit the projection block silently breaks the upgrade path at
  runtime, not at compile time.
- **Loses the macro convergence's main benefit.** /307 §2.4 and
  /308 §"observable block" both argue the macro is the single
  authoritative compiler for the contract crate's wire surface.
  Splitting projection off pulls a load-bearing concern out of
  that compiler.
- **The split has no compelling advantage.** The argument for
  splitting macros is usually "different sites of use" — but
  `version_projection!` would be invoked exactly once per
  contract crate, in the same file as `signal_channel!`, by the
  same author. The split adds work without reducing scope.

### §2.3 What the macro emits — concrete shape

For the Spirit v0.1.0 contract with the `next_schema` block
above, the macro emits one `impl VersionProjection` per
operation/reply/event variant:

```rust
// Macro-emitted in v0.1.0's expanded source:

pub struct ForwardSpiritOperation;

impl ::version_projection::VersionProjection<
    Operation,
    signal_persona_spirit_next::Operation,
> for ForwardSpiritOperation {
    type Error = ::version_projection::ProjectionError;

    fn project(source: Operation)
        -> Result<signal_persona_spirit_next::Operation, Self::Error>
    {
        match source {
            Operation::State(payload) => Ok(
                signal_persona_spirit_next::Operation::State(payload.into())
            ),
            Operation::Record(payload) => Ok(
                signal_persona_spirit_next::Operation::Record(payload.into())
            ),
            Operation::Observe(payload) => Ok(
                signal_persona_spirit_next::Operation::Observe(payload.into())
            ),
            // Watch / Unwatch unchanged → Identity
            Operation::Watch(payload) => Ok(
                signal_persona_spirit_next::Operation::Watch(payload.into())
            ),
            Operation::Unwatch(payload) => Ok(
                signal_persona_spirit_next::Operation::Unwatch(payload.into())
            ),
        }
    }
}

// One projection per payload type — auto-emitted from each variant:

pub struct ForwardStatement;

impl ::version_projection::VersionProjection<
    Statement,
    signal_persona_spirit_next::Statement,
> for ForwardStatement {
    type Error = ::version_projection::ProjectionError;

    fn project(source: Statement)
        -> Result<signal_persona_spirit_next::Statement, Self::Error>
    {
        source.try_into().map_err(|e| {
            ::version_projection::ProjectionError::TransformFailed(e.to_string())
        })
    }
}
```

The macro's per-variant emission rule:

1. The payload type must implement `Into<NextCratePayloadType>`
   (the `From` impl lives next to the payload type in the
   current crate — `impl From<Self> for next::Self` is fallible-
   free, `impl TryFrom<Self> for next::Self` is fallible).
2. The macro emits the `VersionProjection` impl that calls into
   the `From` / `TryFrom`; the trait error variant maps to
   `ProjectionError::TransformFailed`.
3. When `TryFrom`'s error is structural ("the target type cannot
   represent this value"), the human-written impl returns
   `ProjectionError::NotRepresentable` and the macro forwards it
   untouched — matching the existing
   `/git/github.com/LiGoldragon/version-projection/src/projection.rs:36-40`
   `NotRepresentable` variant semantics.

The only hand-written code per migration is the `From` / `TryFrom`
impl on each payload type. The macro emits the wiring.

## §3 Cycle-avoidance

The direction is fixed: **current → next**. v0.1.0's `Cargo.toml`
depends on v0.1.1; v0.1.1's `Cargo.toml` does NOT depend on
v0.1.0. The reverse direction never holds. This makes the
dependency graph a one-way chain: v0.1.0 → v0.1.1 → v0.1.2 → ...,
with the head (latest version) having no `next_schema` block.

### §3.1 The boundary case — what if v0.1.1 is itself prototyping?

The hard case: v0.1.0 is being modified to ADD the `next_schema`
declaration for the first time, and v0.1.1 is itself still in
flux. If v0.1.0's `signal_channel!` invocation requires v0.1.1 to
compile, then v0.1.1's API must already be stable.

**Recommendation: v0.1.0 lands its `next_schema` declaration
ONLY when v0.1.1's schema is frozen.** Specifically:

1. v0.1.1 develops to the point where its `signal_channel!`
   invocation no longer changes signature (operation set, reply
   set, payload types).
2. v0.1.1 publishes a tagged release (or, in workspace-local
   terms, lands an immutable git commit that becomes the
   `version = "0.1.1"` snapshot).
3. v0.1.0's branch is created (forking from the pre-0.1.1
   workspace state if v0.1.0 has already been retired).
4. v0.1.0's `Cargo.toml` is amended to add the renamed alias.
5. v0.1.0's `signal_channel!` block grows the `next_schema`
   line.
6. v0.1.0's macro expansion compiles the `VersionProjection`
   impls against v0.1.1's frozen types.
7. The human writes the `From` / `TryFrom` impls (one per
   widened/transformed payload type).
8. v0.1.0 is now ready for the handover protocol — but is itself
   frozen, never to receive new schema changes.

The Spirit pilot's actual sequence demonstrates this: v0.1.1 is
the deployed crate
(`/git/github.com/LiGoldragon/signal-persona-spirit/Cargo.toml:3`,
already `version = "0.1.1"`); the v0.1.0 historical shape lives
inline in the migration file
(`/git/github.com/LiGoldragon/sema-upgrade/src/migrations/persona_spirit/version_0_1_0_to_0_1_1.rs:102-236`).
Under next-as-dep, v0.1.0 becomes a real (frozen, archived) crate
named `signal-persona-spirit` at `version = "0.1.0"`, and its
`Cargo.toml` would carry the `signal-persona-spirit-next =
{ version = "0.1.1", package = "signal-persona-spirit" }` line.

### §3.2 Two parallel-work cases

**Case 1 — v0.1.0 is frozen; v0.1.1 is current; v0.1.2 is being
prototyped.** No cycle: v0.1.0 → v0.1.1 dependency is stable;
v0.1.1's `next_schema` block is added once v0.1.2 freezes;
v0.1.0 never needs re-editing.

**Case 2 — v0.1.1 needs an emergency fix after v0.1.0 has
already declared it as `next`.** A patched v0.1.1 → v0.1.1.1
release that doesn't change the schema (the `version` minor
bumps but `ContractVersion` hash stays equal — same shape) is
safe; v0.1.0's Cargo selector resolves the latest 0.1.x. A
patched v0.1.1 that DOES change schema is a new version (0.1.2)
and requires a new freeze step.

In short: the freezing discipline is the cycle-avoidance proof,
and it matches how published crate semver already works.

## §4 Bootstrap — first version with no next

When v0.1.0 first ships, no v0.1.1 exists. Three candidates.

### §4.1 Candidate A — omit projection emission silently (REJECTED)

The macro detects no `next_schema:` block and emits nothing.
Rejected because:

- **Silent emission is invisible.** An operator reading the
  contract crate sees `signal_channel!` but cannot tell whether
  the omission is intentional or accidental.
- **The Identity blanket impl at
  `/git/github.com/LiGoldragon/version-projection/src/projection.rs:26-32`
  is `impl<T: Projected> VersionProjection<T, T> for Identity` —
  it covers self-projection, not "no next-projection-needed."
  Silently omitting next-projection means the consumer (the
  handover state machine) can't statically check whether a given
  contract supports next-projection.**

### §4.2 Candidate B — generate a `NoNextVersion` marker projection (REJECTED)

The macro emits a placeholder projection from each variant to a
`NoNextVersion` marker type (defined in `version-projection`)
that satisfies the trait bound but always returns
`ProjectionError::DirectionNotImplemented`. Rejected because:

- **It pollutes the consumer's match arms.** Code that asks
  "does this contract support next-projection?" must now treat
  `Ok(NoNextVersion)` vs `Err(DirectionNotImplemented)` as the
  same answer. Two variants, one meaning.
- **It generates dead code in every v0.1.0 contract.** Every
  schema crate that hasn't shipped a next yet carries dummy
  impls in its expanded source.

### §4.3 Candidate C — require explicit opt-in via `next_schema:` attribute

**RECOMMENDED.** No `next_schema:` block in the macro invocation
means no `VersionProjection` impls are emitted. The contract
crate compiles without any next-related output. The handover
state machine that consumes a `VersionProjection` impl gets a
plain "no impl in scope" error at compile time if it tries to
use one on a contract that doesn't declare next.

Why this wins:

- **Lexically visible.** An operator reading the crate sees
  `next_schema { crate ... }` OR they don't. The presence/
  absence is the answer.
- **Aligns with the existing `version-projection` trait usage.**
  The trait at
  `/git/github.com/LiGoldragon/version-projection/src/projection.rs:9-13`
  has no fallback for "no impl." Consumers that want an impl
  fail to compile if none is in scope. That's the right shape —
  the bootstrap state is just "no impl yet."
- **The `Identity` blanket
  (`/git/github.com/LiGoldragon/version-projection/src/projection.rs:26-32`)
  remains the only universal impl.** Every type that is
  `Projected` self-projects via `Identity`. The next-as-dep
  emission adds a SECOND impl (with different type parameters)
  for the same source type — `VersionProjection<Foo,
  v0_1_1::Foo>`. These don't collide because the trait's two
  type parameters distinguish them.
- **Bootstrap is a NORMAL state.** Every component starts at
  v0.1.0 with no successor. Requiring an opt-in matches the
  natural lifecycle.

A contract author who knows the next version is coming "soon"
can add a stub crate at v0.1.1 (publishing exactly the same
schema as v0.1.0 — same payload types, same operations) and
declare `next_schema` pointing at it. The `From` impls become
trivial `impl From<Self> for next::Self { fn from(s: Self) -> _
{ s } }` clones. This is rarely needed, since at v0.1.0 there is
no past from which to migrate, but the option exists.

## §5 Interaction with the `VersionProjection` trait

The trait at
`/git/github.com/LiGoldragon/version-projection/src/projection.rs:9-13`
is:

```rust
pub trait VersionProjection<Source, Target> {
    type Error;
    fn project(source: Source) -> Result<Target, Self::Error>;
}
```

Two facts settle whose crate owns each impl:

1. **The macro runs at the current crate's compile time** (the
   crate doing the `signal_channel!` invocation).
2. **The `next_schema:` block names the next crate as a
   dependency.**

Therefore the current crate has both types in scope (its own
types directly, the next crate's types via the renamed
dependency). The macro emits:

```rust
impl ::version_projection::VersionProjection<
    Self::Operation,           // current crate's type
    next_crate::Operation,     // next crate's type, in scope via the rename
> for ForwardSpiritOperation { ... }
```

The impl lives in the **current** crate, not the next. The next
crate has no knowledge of the current — by direction.

### §5.1 The witness type per direction

Each direction needs its own witness type because Rust's
coherence rules forbid two `impl VersionProjection<A, B>` blocks
for the same `Self` and same type params. The macro emits one
named struct per projection:

- `ForwardSpiritOperation` for `Operation → next::Operation`
- `ForwardSpiritReply` for `Reply → next::Reply`
- (and one per per-variant payload that needs explicit projection)

Reverse projection (next → current — used for Mirror payload
reverse-projection at the handover boundary, per
`/git/github.com/LiGoldragon/signal-version-handover/ARCHITECTURE.md:107-160`)
is emitted as **separate impls in the NEXT crate's macro
expansion** (when v0.1.1's `signal_channel!` invocation declares
v0.1.2 as its next, and v0.1.1's handover-time reverse-projection
goes through human-written `From<next::T> for Self` impls
shipped in v0.1.1's crate). This is symmetric and clean.

**Important: the macro does NOT emit reverse projection in v0.1.0
for current → next; it ONLY emits forward.** Reverse direction
goes through the same mechanism with v0.1.1 as the "current
crate" and v0.1.0 as the dependency — but v0.1.1 (being the
newer version) depends NEITHER on v0.1.0 NOR on itself. So
reverse-projection requires a different mechanism: it lives in
**v0.1.0's** macro emission too, declared via an optional
`reverse:` keyword inside the `next_schema` block.

### §5.2 The complete `next_schema` shape with reverse

```rust
signal_channel! {
    channel Spirit { ... }
    reply Reply { ... }
    next_schema {
        crate signal_persona_spirit_next;
        forward;   // default; emits Current → Next
        reverse;   // opt-in; emits Next → Current (needed for Mirror)
    }
}
```

When `reverse` is declared, the macro emits BOTH directions —
satisfied by `impl From<next::T> for Self` (reverse) and
`impl From<Self> for next::T` (forward). The two human-written
impl families live side-by-side in the current crate.

## §6 The N+2 case

What about v0.1.0 → v0.1.2 when v0.1.1 is in between?

### §6.1 Recommendation — two-hop chain composed at runtime

**RECOMMENDED.** The macro emits ONLY adjacent-version
projections (v0.1.0 → v0.1.1; v0.1.1 → v0.1.2). The N+2 case is
handled at the **handover boundary**, not in the macro.

The sema-upgrade execution layer composes:

```rust
fn project_v010_to_v012(value: V010::T) -> Result<V012::T, ProjectionError> {
    let intermediate = ForwardSpiritOperation::project(value)?;  // 0 → 1
    let final_value = V011_ForwardSpiritOperation::project(intermediate)?;  // 1 → 2
    Ok(final_value)
}
```

The composition lives in the sema-upgrade runtime's migration-
chain executor, not in any contract crate. The contract crates
themselves are oblivious to multi-hop chains; each knows only
about its immediate successor.

### §6.2 Why two-hop is preferred over direct per-pair

Reasons:

- **Quadratic crate dependencies are avoided.** A direct
  v0.1.0→v0.1.2 projection requires v0.1.0's `Cargo.toml` to
  depend on v0.1.2. That cascades: v0.1.0→v0.1.N requires
  v0.1.0 to depend on every later version. The dependency graph
  becomes a clique; the build cost is quadratic.
- **Each pair is independently auditable.** Each hop has its
  own `From` impls reviewable in isolation. A direct N-hop impl
  has to bundle all the intermediate transforms into one
  function — much harder to review.
- **Compositionality is a property of the trait.** Two
  `VersionProjection` impls compose by their nature; the
  abstraction already supports the chain.

### §6.3 The lossiness corner

The two-hop chain is lossless when the schema changes are
**additive only at each hop** (the v0.1.0 → v0.1.1 → v0.1.2
chain widens fields without dropping any). If a hop is lossy
(e.g., v0.1.1 → v0.1.2 narrows a field), then composing through
v0.1.1 loses information that v0.1.0 might have wanted to
preserve. Two responses:

1. **Lossy hops surface as `ProjectionError::NotRepresentable`
   at the lossy boundary.** The chain stops; the upgrade path
   degrades to `Mirror`/`Divergence` per the policy at
   `/git/github.com/LiGoldragon/version-projection/src/policy.rs:33-66`.
2. **If preserving v0.1.0 information across a lossy hop is
   genuinely needed**, the operator hand-writes a direct
   v0.1.0 → v0.1.2 path in the migration-chain executor — but
   that is an exceptional escape hatch, not the default.

In practice schema migrations are additive-only by convention
(the workspace's evolution discipline); the chain is lossless
the overwhelming majority of the time.

### §6.4 Hop invocation at handover

At handover time, the executor walks the version graph from the
source database's `ContractVersion` to the target daemon's
`ContractVersion`, finds the chain of intermediate
`VersionProjection` witnesses, and composes them. The
`MigrationIndex` at
`/git/github.com/LiGoldragon/version-projection/src/index.rs:57-81`
is the lookup table; each `MigrationIndexEntry` carries the
adjacent-pair projection. The executor sequences them.

## §7 Mirror-payload coupling — recheck under next-as-dep

Per /315 §2.3 and spirit 274 (Maximum certainty), Mirror payload
is raw bytes in its own container; the typed-enum alternative is
rejected.

Does next-as-dep change the analysis?

### §7.1 The original cost argument

The typed-enum alternative was rejected because typing the
Mirror payload would force `signal-version-handover` to import
every signal-X crate, exploding the dependency graph:

```text
signal-version-handover (contract) ─→ signal-persona-spirit
                                  ─→ signal-persona-mind
                                  ─→ signal-persona-orchestrate
                                  ─→ ... (every component contract, every version)
```

The cost was the cross-crate dependency footprint at the
SIGNAL-VERSION-HANDOVER level — not at the macro level. The
macro never needed every contract's types.

### §7.2 Does next-as-dep change this?

**No, the analysis stands. Recommendation: keep Mirror payload
as raw bytes in its own container.**

Reasons:

- **next-as-dep gives the macro visibility into TWO schemas
  (current + next), not N schemas.** The cost argument was
  about coupling `signal-version-handover` to every component's
  every version. next-as-dep only couples each contract to its
  own next version. The two are different scope concerns.
- **Mirror is at the WIRE level**, not the per-component-pair
  level. `signal-version-handover` is a single wire contract that
  one daemon-pair-per-cutover speaks. Typing its Mirror operation
  would require enumerating all possible (component, version-pair)
  payloads in one contract — that's still untyped from
  `signal-version-handover`'s point of view, because the contract
  doesn't know which component speaks it.
- **The raw-bytes-plus-RecordKind shape at
  `/git/github.com/LiGoldragon/signal-version-handover/ARCHITECTURE.md:107-160`
  already gives the receiver enough information to reverse-
  project.** The receiver knows its OWN current version + its
  OWN next version (via next-as-dep) + the RecordKind (from the
  wire). That's sufficient to dispatch to the right
  `VersionProjection` impl.

### §7.3 The corner where the analysis might re-open

The one corner: if the workspace's contract crates become so
numerous that the receiver-side dispatch table becomes a
maintenance burden, AND the typing benefit (compile-time
witness of valid payload shapes) outweighs the cost — then
**re-open for ONE component first** as an A/B test.
`persona-spirit` is the natural candidate (first production
handover; smallest schema; lowest blast radius). The conclusion
of the A/B feeds the workspace-level decision.

**Final stance: keep raw bytes (spirit 274 stands); re-open
candidate is persona-spirit only, after the first cutover ships,
and only if the dispatch-table burden actually materialises.**

## §8 Worked example — Spirit v0.1.0 → v0.1.1

The Magnitude widening: v0.1.0's `Certainty { Minimum, Medium,
Maximum }` widens to v0.1.1's `Magnitude { Minimum, VeryLow,
Low, Medium, High, VeryHigh, Maximum }`. Walk through the
next-as-dep design step by step.

### §8.1 Today's hand-rolled shape

Today the historical schema lives INLINE inside the migration
file at
`/git/github.com/LiGoldragon/sema-upgrade/src/migrations/persona_spirit/version_0_1_0_to_0_1_1.rs:102-236`
as a `mod historical { ... }` containing hand-written struct
definitions, an inline `enum Certainty { Maximum, Medium,
Minimum }` at lines 194-199, and the `impl From<historical::
Certainty> for Magnitude` at lines 303-311.

The drawback: any bug in the historical struct definitions
(field name typo, field type drift) is INVISIBLE — the
hand-mirrored shape isn't the same one the deployed v0.1.0
daemon used.

### §8.2 Under next-as-dep — the v0.1.0 schema crate (frozen, archived)

The published `signal-persona-spirit` v0.1.0 source contains:

```rust
// In signal-persona-spirit v0.1.0's src/lib.rs

// Hand-written enum (the historical Certainty):

#[derive(
    Archive, RkyvSerialize, RkyvDeserialize, NotaEnum, Debug, Clone, Copy,
    PartialEq, Eq, Hash,
)]
pub enum Certainty {
    Minimum,
    Medium,
    Maximum,
}

// Hand-written conversion to v0.1.1's Magnitude (the only
// domain-specific transform code):

impl From<Certainty> for signal_persona_spirit_next::Magnitude {
    fn from(certainty: Certainty) -> Self {
        match certainty {
            Certainty::Maximum => Self::Maximum,
            Certainty::Medium => Self::Medium,
            Certainty::Minimum => Self::Minimum,
        }
    }
}

// Macro invocation with next_schema block:

signal_channel! {
    channel Spirit {
        operation State(Statement),
        operation Record(Entry),       // Entry carries Certainty
        operation Observe(Observation),
        operation Watch(Subscription) opens DomainStream,
        operation Unwatch(SubscriptionToken),
    }
    reply Reply {
        RecordAccepted(RecordAccepted),
        // ... same shape as v0.1.1's Reply
    }
    next_schema {
        crate signal_persona_spirit_next;
        forward;
    }
}

// Cargo.toml — v0.1.0's manifest carries:
// [dependencies]
// signal-persona-spirit-next = { version = "0.1.1", package = "signal-persona-spirit" }
```

The macro then emits:

```rust
// Macro-emitted in v0.1.0's expanded source:

pub struct ForwardSpiritOperation;

impl ::version_projection::VersionProjection<
    Operation,
    signal_persona_spirit_next::Operation,
> for ForwardSpiritOperation {
    type Error = ::version_projection::ProjectionError;

    fn project(source: Operation)
        -> Result<signal_persona_spirit_next::Operation, Self::Error>
    {
        match source {
            Operation::State(payload) => Ok(
                signal_persona_spirit_next::Operation::State(payload.into())
            ),
            Operation::Record(payload) => Ok(
                signal_persona_spirit_next::Operation::Record(payload.into())
            ),
            Operation::Observe(payload) => Ok(
                signal_persona_spirit_next::Operation::Observe(payload.into())
            ),
            Operation::Watch(payload) => Ok(
                signal_persona_spirit_next::Operation::Watch(payload.into())
            ),
            Operation::Unwatch(payload) => Ok(
                signal_persona_spirit_next::Operation::Unwatch(payload.into())
            ),
        }
    }
}

// One per payload that carries Certainty/changed shape:

pub struct ForwardEntry;

impl ::version_projection::VersionProjection<
    Entry,                                  // current Entry with Certainty
    signal_persona_spirit_next::Entry,      // next Entry with Magnitude
> for ForwardEntry {
    type Error = ::version_projection::ProjectionError;

    fn project(source: Entry)
        -> Result<signal_persona_spirit_next::Entry, Self::Error>
    {
        // The macro emits a struct-field-by-field walk; each field
        // either Identity-projects (same type) or routes through
        // `Into` (the hand-written From impl).
        Ok(signal_persona_spirit_next::Entry {
            topic: source.topic.into(),
            kind: source.kind.into(),
            summary: source.summary.into(),
            context: source.context.into(),
            certainty: source.certainty.into(),  // Certainty → Magnitude
            quote: source.quote.into(),
        })
    }
}

// (etc. — one per record type touched by the widening.)
```

### §8.3 What changed vs the inline-mirror shape

- **The `historical::Certainty` enum** at the migration file's
  lines 194-199 disappears. The real v0.1.0 crate IS the source
  of truth for the historical shape.
- **The `historical::Entry` struct** at lines 201-209 disappears.
  Same reason.
- **The `From<historical::Certainty> for Magnitude` impl** at
  lines 303-311 MOVES into v0.1.0's crate, where it can be
  reviewed alongside the type it's about.
- **The `VersionProjection` impls** become macro-emitted; the
  `From`/`Into` impls remain hand-written (the only domain code).
- **The `migrate_paths` function** at lines 34-51 simplifies: it
  no longer needs the inline historical shape; it calls
  `ForwardSpiritOperation::project` directly on the deserialized
  v0.1.0 records.

### §8.4 Confirming the trait-usage match

The macro-emitted impl satisfies the trait bound at
`/git/github.com/LiGoldragon/sema-upgrade/src/handover.rs:226`
(`Projection: VersionProjection<Source, Target, Error =
ProjectionError>`) by:

- The witness type is `ForwardSpiritOperation` (or per-payload
  variants).
- `Source` = `Operation` (current).
- `Target` = `signal_persona_spirit_next::Operation` (next).
- `Error` = `ProjectionError`.

All four fit. The handover state machine consumes the impl
directly with no glue code.

## §9 Operator-bead decomposition

Sized for parallel pickup. Each bead 1-4 operator-hours.

### §9.1 Bead — Cargo manifest rename + workspace policy

Update workspace doc + protocols/active-repositories.md to name
the `*-next` rename convention; add it as a `Cargo.toml` style
rule to `skills/component-triad.md`. The bead does NOT modify any
component's Cargo.toml — it sets the rule. ~1 hour.

### §9.2 Bead — `next_schema` block grammar + parse

Add `next_schema` keyword to
`/git/github.com/LiGoldragon/signal-frame/macros/src/parse.rs:12-27`,
extend the `ChannelSpec` model in
`/git/github.com/LiGoldragon/signal-frame/macros/src/model.rs:7-14`,
add the parser block mirroring `ObservableBlockSpec`. Update
`validate.rs` to reject duplicate `next_schema` blocks. Cover with
unit tests in macros/tests for grammar acceptance and rejection
patterns. ~2-3 hours.

### §9.3 Bead — `VersionProjection` impl emission

Extend `/git/github.com/LiGoldragon/signal-frame/macros/src/emit.rs`
to emit one `pub struct Forward<Channel><Operation>` per channel
operation and the matching `impl ::version_projection::
VersionProjection<...>` block. The emit logic walks each
operation variant, generates the per-variant match arm, and
expects the `Into` impl to exist for each payload type (compile
error if missing). Include `forward` keyword handling; defer
`reverse` to a separate bead. ~3-4 hours.

### §9.4 Bead — emit per-payload struct projection (field-walk)

For each payload struct/enum reachable from operation/reply
variants, emit a `pub struct Forward<PayloadType>` plus impl
that walks the fields. This is the field-by-field shape from
§8.2's `ForwardEntry`. The emission rule: same field name on both
sides + `Into` impl available → emit `Into::into` call. ~3-4
hours.

### §9.5 Bead — reverse projection emission

Add `reverse` keyword to the `next_schema` block, emit the
mirror impls (next → current). Same shape as forward but with
type params swapped. Compile error if `reverse` is declared
without the next crate's `From<next::T> for Self` impls. ~2-3
hours.

### §9.6 Bead — first real cutover: signal-persona-spirit v0.1.0 crate

Create the published v0.1.0 crate as a frozen snapshot
(`/git/github.com/LiGoldragon/signal-persona-spirit` rolled back
to its pre-Magnitude state, with the `next_schema` block added
and the `From<Certainty> for Magnitude` impl written). Delete the
inline `mod historical` from
`/git/github.com/LiGoldragon/sema-upgrade/src/migrations/persona_spirit/version_0_1_0_to_0_1_1.rs:102-236`.
Update the migration to consume the real v0.1.0 crate. ~3-4
hours.

**Bead count: 6. Total estimated operator-hours: ~14-19.**

## §10 Open psyche questions

Four corners worth surfacing. The next-as-dep design itself is
spirit 366 Maximum — these are the implementation corners, not
the direction.

### §10.1 What's the freezing protocol for v0.1.N when v0.1.N+1 stabilises?

The frozen v0.1.0 crate needs a stable git location. Options:

- **A separate branch in the same git repo.** `signal-persona-
  spirit` carries a `v0.1.0` branch and a `main` (v0.1.1) branch.
  Cargo resolves either by git rev. Drawback: branch-per-version
  in every component repo.
- **A separate repo per frozen version.** `signal-persona-
  spirit-v0_1_0` exists as its own repo, frozen at the v0.1.0
  state. Drawback: repo proliferation.
- **A tag in the same git repo.** `v0.1.0` is a git tag; Cargo
  resolves `version = "0.1.0"` against the registry (or directly
  against the tag). Drawback: only works once the workspace
  publishes to a real Cargo registry.

The current workspace uses ghq + `branch = "main"` resolution.
Branch-per-version is the lowest-churn option in the current
shape; tag-per-version becomes natural once a registry exists.

### §10.2 How do extra (non-schema) `From` impls in v0.1.0 surface to operators?

The `From<Certainty> for Magnitude` impl carries the only
domain-specific code in the v0.1.0 crate beyond its schema. It's
the highest-bug-risk surface in the design. How do reviewers see
it as "the migration logic" rather than "incidental Cargo
plumbing"?

Lean: a `src/migration.rs` convention. Every schema crate that
declares `next_schema` puts its hand-written `From` impls in
`src/migration.rs`; the macro doesn't enforce this, but the
workspace skill file does. Operator reviews of v0.1.0 → v0.1.1
land focus on this one file.

### §10.3 What's the macro behaviour when the `From` impl is missing?

The macro emits `payload.into()` for each variant. If the human
hasn't written `impl From<Self> for next::T`, the compile error
points at the macro-emitted line, not at the missing impl. Does
the macro intercept this with a clearer message?

Lean: a compile-time assertion via a const fn that the `Into`
exists, with a `concat!`-built error message naming the missing
impl. Adds work to the emit pass; might be deferred to a
follow-up if the standard Rust error is clear enough.

### §10.4 Does owner-signal-version-handover need its own next_schema declaration?

The owner contract carries `ForceFlip` / `Rollback` /
`Quarantine` verbs per spirit 214. These verbs are simpler
shapes than the ordinary contract's; their next-version
projection is overwhelmingly likely to be Identity (the verbs
don't change shape across schema revisions). Does the macro
still require a `next_schema` declaration for owner contracts?

Lean: yes — uniform discipline. Even if every variant projects
through `Identity`, the explicit declaration makes the upgrade
path visible. The `From<Self> for next::Self { fn from(s: Self)
-> _ { s } }` impl is a one-line per-variant ceremony.

## See also

- `./0-frame-and-method.md` — orchestrator frame for this
  meta-report; full slice contracts and §5 cross-cutting
  constraints.
- `./1-sema-upgrade-path-audit.md` — Subagent A's audit of the
  deployed upgrade path (gap matrix: what's shipped vs designed).
- `./2-macro-current-state-audit.md` — Subagent B's audit of the
  current macro surface and the 8 macro beads' status.
- `reports/designer/307-design-golden-ratio-namespace-split.md`
  — first design adding cross-version coordination to the macro
  family (`assert_triad_sections!`); the next-as-dep block sits
  in the same extension surface.
- `reports/designer/308-design-pretyped-envelope-and-tap-anywhere.md`
  — second design extending `signal_channel!` (Frame envelope,
  Tap anywhere); confirms the macro is the convergence point.
- `reports/designer/312-design-recursive-help-on-every-enum.md`
  — third design extending `signal_channel!` (Help noun); same
  extension-surface argument.
- `reports/designer/315-design-sema-upgrade-and-handover-current-state.md`
  — current state of the sema-upgrade stack; the next-as-dep
  design replaces /315 §3's inline historical shape with a real
  crate dependency.
- `version-projection/ARCHITECTURE.md` — the trait the macro
  emits an impl for; current state of the projection vocabulary.
- `signal-version-handover/ARCHITECTURE.md` — the wire contract
  whose Mirror operation reverse-projects through the macro-
  emitted impls; §7's recheck confirms its raw-bytes shape
  stands.
