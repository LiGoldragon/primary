# Skill — enum contact points

*Engine logic at the high level is tree-vs-tree matching. Two enums
meeting under `match` form a typed relationship — name it.*

## What this skill is for

Apply this skill when writing the load-bearing logic of an engine,
handler, dispatcher, executor, classifier, or state machine — any
code whose job is to decide what to do based on the combination of
two structured inputs. The pattern is most visible in Rust because
`match` makes the cross-product explicit, but the principle applies
to any language with sum types (Haskell, OCaml, Scala, TypeScript
discriminated unions, Python tagged dataclasses, Swift enums) and
to any language that simulates them (C tagged unions, dynamic
languages with type tags).

If you're writing a single-input dispatcher (one enum, one
`match`), this skill isn't the one — that's plain pattern matching
and the variants speak for themselves. Reach here when **two enums
meet**, or when one enum meets a method-derived value whose shape
the matching depends on.

## The principle

> **Engine logic at the high level is tree-vs-tree matching:
> canonically enum-against-enum, sometimes enum-against-a-mix-of-
> enums-and-method-calls. The cross-product of the two variant sets
> is the "common-language relationship node point" — make it
> explicit, as a typed `match` or as a trait whose impl carries
> the matrix, rather than scattering the relationship across ad-hoc
> arms and string predicates.**

The cross-product **IS** the typed relationship. When `State` has
*N* variants and `Operation` has *M* variants, there are up to *N*
* *M* meaningful (state, operation) pairs. Some are valid
transitions; some are rejections; some are no-ops. The pair itself
is the unit of logic. Naming that pair — as the head of a `match`,
or as a trait impl over the pair — is what makes the engine
readable.

The drift you're guarding against: spreading the matrix across
nested `if state.is_active() && operation.is_marker_request() …`
chains, or branching on string predicates (`if name.starts_with(…
)`), or piling sentinel-bool flags. Each of these encodes one
column of the matrix in one place and one row in another, and the
reader can't see the matrix at all.

## The canonical traits

When the cross-product is large enough to deserve its own type,
extract it as a trait keyed on the *right-hand* enum (or on a token
type that names the variant axis). Two common shapes:

### `Reaches<Right>` — left value decides what reaches a right value

The left enum is the active side: it asks "given this right-hand
value, do I touch it?" The trait carries the left enum's
discrimination; the impl carries the right-hand cross-product.

```rust
pub trait Reaches<Right> {
    fn reaches(&self, right: &Right) -> bool;
}

impl Reaches<StoredActivity> for ActivityFilter {
    fn reaches(&self, activity: &StoredActivity) -> bool {
        match self {
            ActivityFilter::RoleFilter(role) => &activity.role == role,
            ActivityFilter::PathPrefix(prefix) => match &activity.scope {
                ScopeReference::Path(path) => path.has_prefix(prefix),
                ScopeReference::Task(_) => false,
            },
            ActivityFilter::TaskToken(token) => match &activity.scope {
                ScopeReference::Path(_) => false,
                ScopeReference::Task(activity_token) => activity_token == token,
            },
        }
    }
}
```

The nested `match` IS the cross-product. The shape forces the
author to consider every (filter, scope) pair — the type checker
fails if a variant is forgotten.

### `Contact<Other>` — symmetric meeting, neither side privileged

Two enums meet at equal status (neither is a verb on the other).
The trait names the meeting itself.

```rust
pub trait Contact<Other> {
    type Outcome;
    fn contact(&self, other: &Other) -> Self::Outcome;
}
```

Use when the relationship is genuinely two-sided — a collision
between protocol versions, a comparison between schema kinds, a
match between two filters. If one side is clearly the active
verb-bearer, prefer `Reaches`; if neither is, `Contact` names the
node-point honestly.

### `Dispatch<Token>` — input variant decides which method to call

The left enum holds the inputs; the right side is a token type
naming what handler to call; the trait stamps the handler interface.
This is what `signal-frame`'s `signal_channel!` macro emits.

```rust
pub trait OperationHandler {
    type Error;
    async fn handle_ask_handover_marker(
        &mut self,
        payload: MarkerRequest,
    ) -> Result<Reply, Self::Error>;
    async fn handle_ready_to_handover(
        &mut self,
        payload: ReadinessReport,
    ) -> Result<Reply, Self::Error>;
    // … one method per Operation variant
}

pub trait OperationDispatch: OperationHandler {
    async fn dispatch_operation(
        &mut self,
        operation: Operation,
    ) -> Result<Reply, Self::Error> {
        match operation {
            Operation::AskHandoverMarker(payload) => {
                self.handle_ask_handover_marker(payload).await
            }
            Operation::ReadyToHandover(payload) => {
                self.handle_ready_to_handover(payload).await
            }
            // … one arm per variant, mechanically derived
        }
    }
}
```

The `match` lives in the blanket impl; every handler implements the
flat per-variant trait. This is the right shape when the engine
side is "one method per operation," with the per-variant logic
genuinely different.

## Worked examples in the workspace

### 1. HandoverState × Operation in Spirit

`/git/github.com/LiGoldragon/persona-spirit/src/actors/root.rs:221-388`
holds `SpiritRoot::submit_upgrade_request`. The two enums:

- `HandoverState` (line 93): `Active` / `HandoverMode { accepted_marker }` /
  `PrivateUpgradeOnly`.
- `signal_version_handover::Operation`: `AskHandoverMarker` /
  `ReadyToHandover` / `HandoverCompleted` / `Mirror` / `Divergence`
  / `RecoverFromFailure`.

The cross-product (3 × 6 = 18 combinations) sits in one outer
`match request { … }`, with `matches!(self.handover, …)` and inner
`match &self.handover { … }` arms checking the state for each
operation that needs it. The matrix is visible: every operation
arm explicitly names which states it accepts, with the rejection
reason at hand.

Drift hazard: when this code's seven `matches!` and inner-`match`
calls multiply by another operation, the engine becomes hard to
read. The skill's recommendation is to lift the matrix into a
`Reaches<HandoverState>` impl on `Operation` (or vice-versa) when
a new state or operation joins — the trait header names the
relationship and forces every new variant to declare its row.

### 2. HandoverState × UpgradeOperation in Orchestrate

`/git/github.com/LiGoldragon/orchestrate/src/service.rs:186-318`
shows the *same* cross-product expressed differently:
`handle_upgrade_operation` is the single `match operation` arm,
and each operation calls a dedicated handler method
(`ready_to_handover` line 218, `handover_completed` line 246,
`recover_handover` line 305). Each handler holds its own column
of the matrix as a `match &*state { HandoverState::Active … }`.

This is the **factored** version of the Spirit pattern: instead
of one giant nested `match`, the outer enum dispatches to a
method-per-variant, and each method's body holds the inner
`HandoverState` match. Compare to the Dispatch trait shape
above — the factoring is the same; the trait would name what the
ad-hoc per-method factoring leaves implicit.

The two side-by-side codebases show the same matrix at two levels
of explicitness. Either is honest about the cross-product. The
trait shape becomes worth the ceremony once a third consumer
appears that must also walk the (HandoverState, Operation) matrix.

### 3. SchemaMacro<Input> over BuiltinMacroVariant

`/git/github.com/LiGoldragon/schema/src/engine.rs:7-44` shows the
canonical `Dispatch` shape. `BuiltinMacroVariant` (line 16) is one
enum:

```rust
pub enum BuiltinMacroVariant {
    Import(ImportInput),
    Header(HeaderInput),
    Type(TypeInput),
    Feature(FeatureInput),
    UpgradeRule(UpgradeRuleInput),
}
```

The trait `SchemaMacro<Input>` (line 46) — generic over the input
type, with one impl per variant (`ImportMacro` line 225, `HeaderMacro`
line 234, etc.) — is the per-variant handler. The variant's `lower`
method (line 35) is the single `match` that dispatches each variant
to its impl. `NodeDefinitionPoint` (line 7) is the witness enum:
`point(&self)` (line 25) projects each variant onto its definition
context, so downstream code matches on `NodeDefinitionPoint` instead
of `BuiltinMacroVariant` when only the point matters.

This is the schema-engine analogue of `signal_channel!`'s dispatch
trait emission (see example 4): one variant per handler, one
witness enum naming the per-variant axis, one method bridging them.

### 4. signal_channel! macro emits the Dispatch trait

`/git/github.com/LiGoldragon/signal-frame/macros/src/emit.rs:389-472`
is `emit_operation_dispatch`. For every channel declared via
`signal_channel!`, the macro emits a `<Operation>Handler` trait
(one async method per Operation variant) and a `<Operation>Dispatch`
trait whose blanket impl carries the `match operation` that maps
each variant to its handler method.

The macro IS the encoding of the discipline: every signal channel
in the workspace gets a typed `Dispatch` trait automatically,
because the `Operation × handler-method` cross-product is too
mechanical to leave to hand-rolling. The macro emit also names
the relationship via `OperationDispatchError`
(`/git/github.com/LiGoldragon/signal-frame/src/operation_dispatch.rs`),
so the kind of mismatch that the short-header check finds is itself
a typed enum — the contact point between a header byte and an
operation variant.

### 5. From<historical::T> for current::T in upgrade migrations

`/git/github.com/LiGoldragon/upgrade/src/migrations/persona_spirit/version_0_1_0_to_0_1_1.rs:293-313`
holds the **historical-to-current** projection: `From<historical::Kind>`
for `v010::Kind` and `From<historical::Certainty>` for
`v010::Certainty`. Each impl is a per-variant `match` —
the cross-product of the two enum shapes — and the absence
of `_ =>` ensures the type checker rejects forgetting a variant
when either side changes.

This is `Contact<Other>` realised as the standard `From` trait.
Every historical/current enum pair becomes a `From` impl; the
chain of `From` impls is the migration spine. The discipline:
when a new variant lands on either side, the `From` impl's
exhaustiveness check fails, forcing the migration's author to
declare what the new variant projects to.

### 6. ActivityFilter × ScopeReference in orchestrate

`/git/github.com/LiGoldragon/orchestrate/src/activity.rs:62-92`
holds `ActivityFilterMatch::matches` — the cleanest small example
of the pattern in the workspace. Three filter variants × two scope
variants = six pairs; the outer match arms each carry an inner
`match` over the scope. The relationship type
(`ActivityFilterMatch<'filter>`) names the contact point
explicitly even though it's a tiny struct around a borrowed
reference; the *naming* is what makes the cross-product readable.

The pattern is small enough that there's no trait — the matrix
fits in one method. The skill's reading: when the matrix grows
past one method's worth of arms (say, more than ~8 pairs), lift
it to `Reaches<ScopeReference>` on `ActivityFilter`.

## When method calls participate in the cross-product

Not every axis of the matrix is an enum field. Sometimes one side
is a method-derived value the engine computes on demand. The
question is whether the derived value should join the cross-product
as a temporary, or be promoted to a stored field on its noun.

### Temporary participation — cheap to recompute

```rust
match (operation.kind(), current_marker.commit_sequence == report.source_marker.commit_sequence) {
    (OperationKind::ReadyToHandover, true)  => self.accept_handover(report),
    (OperationKind::ReadyToHandover, false) => self.reject_advanced(report),
    // …
}
```

The boolean is a temporary derived from two fields; it joins the
cross-product as a tuple argument. Storing it as a flag on the
state would duplicate `commit_sequence` and `source_marker.commit_sequence`
in two places — drift hazard.

The diagnostic: ***if the derived value's computation reads only
from the inputs already on the call site, fold it in as a `match`
tuple element; don't store it.*** The cross-product naturally
extends to tuples of (enum, enum, bool, enum) when the boolean is
a method-derived predicate over the right-hand side.

### Stored participation — the derived value names a concept

When the same derivation appears at many call sites, the derivation
is hiding a typed concept. Promote it:

```rust
// Wrong — recomputed at every call site
if marker.commit_sequence == report.source_marker.commit_sequence {…}
// also: at another site …
if other_marker.commit_sequence == other_report.commit_sequence {…}

// Right — the concept gets a name and a type
pub enum SequenceAlignment { Aligned, Advanced }

impl HandoverMarker {
    pub fn align_with(&self, other: &HandoverMarker) -> SequenceAlignment { … }
}

// Now the matrix is (HandoverState, Operation, SequenceAlignment)
// — three typed enums, all visible.
```

The diagnostic: ***if the derived predicate appears as a `match`
arm guard at more than two sites, the predicate is asking to be a
typed enum.*** Promotion makes the cross-product explicit; failing
to promote scatters the column across the codebase.

## Anti-patterns

Each anti-pattern below hides a cross-product behind something
that doesn't read as one. The refactor is always the same: make
the matrix explicit, either as a nested `match` or as a trait
named after the relationship.

### Anti-pattern: nested if chains over state combinations

The matrix is encoded as `if x.is_a() && y.is_p() { … } else if
x.is_a() && y.is_q() { … } else if x.is_b() && y.is_p() { … }`.
The cross-product is implicit in the conjunctions, and the
compiler can't tell you when a cell is missed.

```rust
// Wrong — the matrix is invisible
if matches!(state, HandoverState::Active) && marker_aligned {
    self.accept_ready_to_handover()
} else if matches!(state, HandoverState::Active) && !marker_aligned {
    self.reject_advanced()
} else if matches!(state, HandoverState::Ready { .. }) {
    self.reject_already()
} else {
    self.reject_not_ready()
}
```

The canonical refactor:

```rust
match (state, marker_aligned) {
    (HandoverState::Active, true)  => self.accept_ready_to_handover(),
    (HandoverState::Active, false) => self.reject_advanced(),
    (HandoverState::Ready { .. }, _) | (HandoverState::Complete, _) => self.reject_already(),
}
```

The tuple makes the cross-product visible. Exhaustiveness checking
catches the missing cell.

### Anti-pattern: sentinel values masquerading as state

A field on `SpiritEngine` named `current_phase: u8` with magic
values `0 = Active`, `1 = Ready`, `2 = Complete` is the same
matrix with the type system erased. Every comparison `if phase ==
1` is a row in the matrix that the compiler can't see.

The refactor: define the enum. `pub enum SpiritPhase { Active,
Ready, Complete }`. Now `match phase` over `(SpiritPhase, Operation)`
is exhaustive. Same code, type-checked.

### Anti-pattern: boolean flags hiding a closed enum

```rust
// Wrong — three booleans encoding a three-way axis
if request.is_owner && !state.is_handover && operation.is_marker_request() { … }
```

Three booleans = a three-axis cube with eight cells, but only some
cells are legal. The boolean form lets the illegal cells type-check.
Per `skills/typed-records-over-flags.md`: if the booleans are
mutually exclusive or the combinations are constrained, the type
is a closed enum (or a struct of `Option<T>`s where the variants
carry payloads).

The refactor lifts the booleans into one enum, then matches.

### Anti-pattern: string matching as dispatch

```rust
// Wrong — closed set hidden behind a string
match variable.as_str() {
    "PERSONA_SPIRIT_SOCKET"       => Self::MissingSpiritSocket,
    "PERSONA_SPIRIT_OWNER_SOCKET" => Self::MissingOwnerSpiritSocket,
    _ => Self::InputOutput { reason: format!("missing socket {variable}") },
}
```

This appears at
`/git/github.com/LiGoldragon/persona-spirit/src/error.rs:137`.
The two strings are the two members of a closed set — `Spirit` /
`SpiritOwner`. The right shape is:

```rust
pub enum SocketEnvironmentVariable { Spirit, SpiritOwner }

impl From<SocketEnvironmentVariable> for &'static str { … }
// match on the enum, not the string
```

Same constraint, type-checked. See `skills/rust/methods.md`
§"Don't hide typification in strings" for the cross-language form.

### Anti-pattern: predicate-method soup on the inner type

When one side of the cross-product needs to be inspected through
many `is_*` methods, those methods are an enum waiting to be named.

```rust
// /git/github.com/LiGoldragon/nota-codec/src/value.rs:85-156
impl NotaValue {
    pub fn is_record(&self) -> bool { … }
    pub fn is_sequence(&self) -> bool { … }
    pub fn is_map(&self) -> bool { … }
    pub fn is_block_string(&self) -> bool { … }
    pub fn is_identifier(&self) -> bool { … }
    pub fn is_pascal_identifier(&self) -> bool { … }
    pub fn is_pascal_case_identifier(&self) -> bool { … }
    // … plus has_record_head, has_data_shape, record_arity, data_field_count, …
}
```

Each `is_*` is a row of the (caller-context, NotaValue-variant)
matrix, expressed as a free-standing predicate. A caller doing
`if v.is_record() { … } else if v.is_sequence() { … }` is
manually walking the cross-product.

The refactor: define a `Shape` enum (`Record / Sequence / Map /
BlockString / Identifier / PascalIdentifier / …`) and one
`shape(&self) -> Shape` method. Callers `match` on `Shape`;
exhaustiveness catches missed cases; the predicate soup
collapses into one type.

Tradeoff: per `skills/rust/methods.md` §"Use existing trait
domains", `is_*` predicates are fine for fielded methods used once
or twice. The diagnostic is **scale**: when more than ~4 `is_*`
predicates are mutually exclusive over the same value, they want
to be one enum. The 14-predicate count in `NotaValue` crosses
that threshold by any reasonable reading.

## When the trait is overkill

The `Reaches<Right>` / `Contact<Other>` / `Dispatch<Token>` trait
shapes are useful when:

- the cross-product has more than ~8 cells,
- the same matrix appears at more than one call site, or
- the relationship deserves a name in its own right (`OperationDispatch`,
  `ObserverFilterMatch`, `From<historical::Kind>` chain).

For one-call-site matrices smaller than ~8 cells, **a nested
`match` is the right shape** — the matrix fits in one screen, the
trait would add ceremony without revealing structure that the
`match` doesn't already reveal. `ActivityFilterMatch` (example 6
above) is at the threshold — a `Reaches<ScopeReference>` trait
would be honest but the inline `match` is fine because there's
exactly one caller.

The diagnostic: ***name the matrix as a trait when naming it
helps the reader; otherwise, write the `match`.***

## What this means for engine design

Engine logic at the high level decomposes into:

1. **Receive a typed input** (an operation enum, a request frame,
   an inbound message).
2. **Read a typed state** (a state enum, a current-phase marker,
   a stored value's variant).
3. **Compute the cross-product entry** — sometimes via direct
   match, sometimes via a trait whose impl carries the matrix.
4. **Emit a typed output** — an action, an effect, a reply enum
   variant.

The contact points between (1) and (2) — between input and state
— are where the engine's logic lives. Make them explicit. The
agent-LLM failure mode is to spread them across `if` chains and
strings; the discipline is to surface them as `match` heads or as
named trait impls.

When the engine is well-designed, the read order is:

1. Open the file; see one outer `match operation` per handler.
2. Within each arm, see an inner `match` over the relevant state.
3. Each inner arm names what happens — usually one constructor
   call on the reply enum, optionally with a state transition.

No engine source where this is true is hard to follow. Every
engine source where the matrix is hidden in `if state.is_a() &&
op.starts_with("...") && other_flag` is hard to follow.

## Cross-references

This skill pairs with several other workspace skills, each
covering one face of the same diamond:

- `skills/abstractions.md` — verb belongs to noun. The
  cross-product `match` IS the verb; the noun is the relationship
  type. This skill is what `abstractions.md` looks like when the
  noun is a *contact* between two enums.
- `skills/typed-records-over-flags.md` — close cousin. That skill
  says "boolean-on-a-noun whose `yes` carries data wants to be
  a typed record." This skill says "two enums whose pairs carry
  logic want to be a typed `match` or a typed trait." Both rules
  push the same direction: the type system carries the meaning.
- `skills/rust/methods.md` §"Don't hide typification in strings" —
  the corollary at the value level. The string-matching anti-
  pattern above is the same rule at the dispatch surface.
- `skills/beauty.md` — beauty as the criterion. A scattered
  matrix is ugly; the discomfort is the diagnostic.
- `skills/language-design.md` §"No keywords beyond truth values" —
  parsers dispatch on position and head identifier, not on a
  reserved word. Same shape: closed enum over the variant axis,
  matched explicitly.
- `skills/architectural-truth-tests.md` — tests that catch the
  matrix going stale. Exhaustive `match` is the compile-time
  version; truth tests are the runtime version for what the
  compiler can't see.
