# 12 — Audit of persona-orchestrate triad against post-/243 primitives

*Companion to `reports/second-designer-assistant/11-audit-of-operator-assistant-157-persona-orchestrate-mvp.md`,
which graded the MVP against the designer handoff
`reports/designer/233-persona-orchestrate-operator-handoff.md` and
the contract-local-verbs migration guide
`reports/designer/241-signal-architecture-migration-guide.md`. This
companion grades the same work against the post-/243 implementation
primitives now landed in the workspace: `signal-executor` (commit
`57040d59`, the new `Lowering` trait + `Executor` + `ExecutorOutcome`),
`signal-frame`'s `observable` block (commits `1610be7c` + `b86442ac`),
and the reply-naming convention landed in
`skills/contract-repo.md` §"Reply discipline" (commit `a7f3a0ee`).
Most of these primitives did not exist when `reports/operator-assistant/157`
implemented its work, so the holes here are migration surface, not
discipline violations. The audit is read through the lens of
`reports/designer/244-hole-finding-after-243-implementations.md`
(holes in the post-/243 primitives themselves) and
`reports/designer/245-design-alternatives-for-244-holes.md`
(designer rethinks for three of /244's five holes — proposals,
not yet landed). The findings below grade against the current
primitive shape; where /245's proposed alternatives would change
the resolution path or migration shape, each hole's section
flags it.*

## 0 · TL;DR

Eight migration-surface holes the new primitives expose. Three high,
three medium, two low/opportunity. The three high holes are
load-bearing for any near-term persona-orchestrate refactor:

The ordinary contract carries `Observe(RoleObservation)` as a
one-shot read op. The `observable` block — the macro feature that
persona-orchestrate would adopt to gain typed observability —
injects `Observe(ObserverFilter)` into the channel's request enum.
Direct collision; the macro's compile-fail fixture
(`observable_operation_name_collision.rs`) would refuse to compile
the contract until one or the other is renamed. /244 §1 hole 2's
lean is to rename the macro-injected verb to `Probe` or `Tap`;
persona-orchestrate's claim on `Observe` is the precipitating
case. /245 §2 proposes a cleaner shape: extend the `observable`
grammar so the contract author *names* the open/close verbs
(`operation_open Watch(Filter)` / `operation_close Unwatch(Token)`),
which dissolves the collision entirely. If /245 lands first,
persona-orchestrate keeps `Observe(RoleObservation)` and picks its
own `Watch`/`Unwatch` (the names it already used for the hand-
rolled surface) — minimal rename.

Reply variants throughout the ordinary contract use noun-form
(`ClaimAcceptance` / `ClaimRejection` / `ReleaseAcknowledgment` /
`HandoffAcceptance` / `HandoffRejection` / `RoleSnapshot` /
`ActivityAcknowledgment` / `ActivityList` / `ObservationOpened` /
`ObservationClosed`). The verb-past-tense convention says these
become `ClaimAccepted` / `ClaimRejected` / `Released` /
`HandoffAccepted` / `HandoffRejected` / `Observed` / `Submitted` /
`Queried` / `Watched` / `Unwatched`. The owner contract is closer
to the convention (`RoleCreated` / `RoleRetired` /
`RepositoryIndexRefreshed` already conform) but has its own
divergences (`RoleCreationRejected` should be `CreateRejected`;
`OwnerOrchestrateRequestUnimplemented` is plainly noun-shape).
Cross-contract inconsistency means a reader's parsing model changes
across the triad.

The daemon's hand-rolled `OperationLowering` struct
(`persona-orchestrate/src/lowering.rs` lines 28-49) is a parallel
implementation of what `signal-executor::Lowering` now offers as a
trait. The static one-to-one map flagged in report 11 §9 is also a
missed integration with `ExecutorOutcome` — and per /244 §1 hole 1,
the current trait surface loses typed rejection reasons on the
wire (the typed `L::RejectionReason` lives inside `ExecutorOutcome`
but the wire reply is `Reply::Rejected { Internal }`). /245 §1
proposes a much cleaner shape: drop the `RejectionReason`
associated type entirely; `lower()` returns
`Result<Vec<SemaOperation>, Self::Reply>`, with Err carrying the
contract's typed `Reply::*Rejected(*RejectionReason)` variant
directly. persona-orchestrate is well-positioned for either shape
— its contract already carries the typed rejection variants
(`HandoffRejectionReason`, `ScopeConflict`,
`RoleCreationRejectionReason`) on the `Reply` enum, so they slot
straight into /245's Err path or into /244's extended trait
methods.

Beyond the high three: bool-flag observation filter selection
(`include_operations: bool, include_sema_effects: bool`) is the
anti-pattern typed `ObserverFilter` exists to replace; the
`observable` block hand-roll skips the macro's published-event
infrastructure; the `RoleObservation` unit struct has no schema
for what's being observed, leaving filtering implicit; the owner
contract's `OwnerOrchestrateRequestUnimplemented` reply variant
breaks the verb-past-tense rule the rest of the owner contract
mostly follows. And persona-orchestrate is the natural worked
end-to-end example /244 §2 hole 5 names as missing — a daemon with
real lowering need plus observability surface plus contract-reply
discipline.

The bottom line: report 11 listed twelve deviations from /233 and
/241. This audit lists eight more migration items that exist purely
because the workspace has moved since /157 landed. None of these
are operator-side errors — they're the structural cadence catching
up. The next persona-orchestrate refactor pass needs to absorb both
lists.

## 1 · What this audit grades against

Three primitives landed after `reports/operator-assistant/157`:

`signal-executor` crate (at
`https://github.com/LiGoldragon/signal-executor`, commit `57040d59`)
defines the `Lowering` trait (operation → Sema effects),
`ExecutorOutcome<L, S>` (the three-variant outcome carrying typed
rejection reason or engine error), the `SemaEngine` trait, and the
`Executor` runtime that orchestrates them. Per /244 §1 hole 1, the
`Lowering` trait needs extending with
`reply_from_lowering_rejection` so typed rejection reasons survive
the wire — but the trait surface exists as the new integration
point for daemons.

`signal-frame`'s `observable` block (commits `1610be7c` +
`b86442ac` in `signal-frame`/macros). A `signal_channel!`
invocation can now declare an `observable { event ... event ... }`
block. The macro injects the `Observe(ObserverFilter)` and
`Unobserve(...)` operations into the channel's request enum,
generates a per-channel `ObserverSet` runtime with `publish_*`
methods (one per declared event), and emits the
`ObserverFilterMatch` trait skeleton the contract author
implements. The block's purpose is to make observability a
first-class macro feature instead of every daemon hand-rolling it.

`skills/contract-repo.md` §"Reply discipline" (commit `a7f3a0ee`).
Reply success variants are verb-past-tense matching the operation
root — `Submit → Submitted`, `Register → Registered`,
`Launch → Launched`, `Retire → Retired`, `Query → Queried` or
`Observed`. Reply rejection variants are verb-past-tense plus
`Rejected` — `Submit → SubmitRejected`, `Register → RegisterRejected`.
Domain-level rejection reasons live as payload variants of the
`*Rejected` reply (a typed enum named e.g. `SubmitRejectionReason`).
The lifecycle exception (shared `ActionAccepted` / `ActionRejected`
pairs for `Start` / `Stop` / `Drain`) applies only when the reply
contract is uniform across the verbs.

The companion designer report `reports/designer/244` enumerates
five holes in those primitives. The persona-orchestrate audit
below uses /244's same hole-types as the lens; one of /244's
holes (the `Observe` verb collision) is precipitated *by*
persona-orchestrate's existing contract.

## 2 · Hole alpha — `Observe` verb collision

`signal-persona-orchestrate` declares `operation Observe(RoleObservation)`
at the ordinary channel surface (`src/lib.rs` line 567 per the
prior Explore mapping). `RoleObservation` is a unit struct; the
operation is the contract's one-shot read affordance for "give me
the current role snapshot."

The `observable` block injects `operation Observe(ObserverFilter)`
into the channel's request enum (/244 §1 hole 2). When
persona-orchestrate adopts the observable block — which is the
correct migration path for daemon observability now — the macro's
injected `Observe` collides with the contract's existing `Observe`.
The compile-fail fixture `observable_operation_name_collision.rs`
in `signal-frame` catches this; the contract author must rename
one or the other.

Three resolution paths. /244 §1 hole 2's incremental: rename the
macro-injected verb workspace-wide; lean is `Probe` or `Tap`.
Single-file edit in the macro's emitter plus tests; benefits every
observable contract but introduces a less-natural name for them.
The alternative is renaming persona-orchestrate's existing
`Observe` to something domain-specific (`Survey`, `Inspect`,
`Snapshot`) — but `Observe` is exactly the verb-form rule /241 §4
says to prefer, and the domain action *is* observation. Renaming
the contract here is a worse fit than renaming the macro.

/245 §2 proposes a third path: extend the `observable` grammar so
the contract author *names* the open/close verbs in the block
itself (`operation_open Watch(Filter) opens ObserverStream`,
`operation_close Unwatch(ObserverToken)`). The macro keeps owning
the token type, stream injection, filter-match skeleton, and
publish-function emission; the contract author owns the verb names
and the event types. This dissolves the collision class entirely:
every contract picks the verbs that fit its domain, and
persona-orchestrate keeps `Observe(RoleObservation)` alongside its
own `Watch(Filter)` / `Unwatch(Token)` for the observability
surface.

The decision belongs upstream (signal-frame's macro grammar is
designer surface). persona-orchestrate is the precipitating
contract; the resolution applies broadly. If /245's grammar
extension lands, this hole transmutes into a migration-shape
detail (persona-orchestrate keeps its existing verb names with no
collision) rather than a workspace-wide rename.

Severity: high under current grammar; resolves cleanly under
/245's proposal.

## 3 · Hole bravo — Reply-naming convention not followed

`signal-persona-orchestrate/src/lib.rs` line 836-842 declares the
ordinary `OrchestrateReply` variants:

`ClaimAcceptance(ClaimAcceptance)`, `ClaimRejection(ClaimRejection)`,
`ReleaseAcknowledgment(ReleaseAcknowledgment)`,
`HandoffAcceptance(HandoffAcceptance)`,
`HandoffRejection(HandoffRejection)`, `RoleSnapshot(RoleSnapshot)`,
`ActivityAcknowledgment(ActivityAcknowledgment)`,
`ActivityList(ActivityList)`, `ObservationOpened(ObservationOpened)`,
`ObservationClosed(ObservationClosed)`.

Every variant is noun-form. The convention is verb-past-tense
matching the operation root. The conforming names by operation:

`Claim` → success: `ClaimAccepted` (or just `Claimed`); rejection:
`ClaimRejected`. The current shape is `ClaimAcceptance` /
`ClaimRejection` — both nouns derived from the verb plus an
abstract-noun suffix, exactly the shape §"Reply discipline" replaces.

`Release` → success: `Released` (the daemon released the claim);
rejection if it ever exists: `ReleaseRejected`. Current:
`ReleaseAcknowledgment` — the noun-shape of "the daemon
acknowledged the release," which buries the active fact (the
release happened) under the procedural noun.

`Handoff` → `HandoffAccepted` / `HandoffRejected` (already typed
rejection reasons on the payload — that's good). Current:
`HandoffAcceptance` / `HandoffRejection` — same noun-shape issue.

`Observe` → `Observed` (the daemon observed and the snapshot is
the payload). Current: `RoleSnapshot` — names the *shape* of the
observed thing, not what the daemon did. After renaming `Observe`
per hole alpha, the conforming reply becomes the verb-past-tense
of whatever replaces it (`Inspected`, `Surveyed`).

`Submit` → `Submitted`. Current: `ActivityAcknowledgment` — same
noun-shape, also leaks the `Activity` prefix into a reply name
that's redundant given the verb's payload type.

`Query` → `Queried`. Current: `ActivityList` — names the payload
shape, not the daemon's action.

`Watch` → `Watched` (matches the verb-past-tense rule). Current:
`ObservationOpened` — fine semantically but doesn't follow the
"reply matches the verb-past-tense" rule mechanically.

`Unwatch` → `Unwatched`. Current: `ObservationClosed` — same
pattern.

The owner contract is closer to the rule but inconsistent. The
verb-past-tense success replies `RoleCreated` / `RoleRetired` /
`RepositoryIndexRefreshed` conform (modulo the `Role` prefix
arguably violating the no-ancestry naming rule when these replies
live in the owner-signal-persona-orchestrate crate). The rejection
reply `RoleCreationRejected` doesn't — the convention is
`CreateRejected` (the verb-past-tense of `Create` plus `Rejected`),
keeping the rejection variant flat under the operation verb. The
catch-all `OwnerOrchestrateRequestUnimplemented` is plainly
noun-shape; the verb-past-tense form would be `Unimplemented`
(or `Rejected { reason: Unimplemented(OperationKind) }` on the
verb-specific reply).

Severity: high. The convention is the active discipline; every
contract author reads `skills/contract-repo.md` before deciding
reply shapes. persona-orchestrate's shipped names won't read
right to anyone who's internalized the convention.

## 4 · Hole charlie — `OperationLowering` bypasses `signal-executor::Lowering`

`persona-orchestrate/src/lowering.rs` lines 28-49 defines
`OperationLowering` as a struct with two static methods,
`ordinary()` and `owner()`, that pattern-match request variants
and return a `LoweredOperation<OperationKind>` carrying a vec of
`SemaOperation`. The shape is hand-rolled; it doesn't reference
or implement the new `signal-executor::Lowering` trait.

`signal-executor`'s `Lowering` trait (per /244 §1 hole 1) has three
associated types — `Operation`, `Reply`, `RejectionReason` — and
two main methods: `lower(&self, op: &Self::Operation) -> Result<Vec<SemaOperation>, Self::RejectionReason>`
and `reply_from_effects(&self, op: &Self::Operation, effects: &[SemaEffect]) -> Self::Reply`.
The trait's purpose is exactly what `OperationLowering` does
manually: map a typed contract operation to a sequence of Sema
operations (possibly empty, possibly multiple, possibly rejected
with typed reason). The `ExecutorOutcome<L, S>` then routes the
result back through the contract's `Reply` enum.

Two consequences of the bypass. First, the static one-to-one map
flagged in report 11 §9 isn't just *defeating* /241 §5's runtime
decision — it's also *not using* the now-existing primitive that
makes runtime decision ergonomic. The `Lowering::lower` method is
where `Claim` would return `Match` (check conflicts) + `Assert`
(write claim if no conflict) — multi-effect, payload-dependent,
runtime-decided. With the trait, the daemon writes one impl per
contract surface; without it, the daemon hand-rolls dispatch in
`service.rs::handle()`.

Second, the typed-rejection-on-the-wire gap. The current trait
surface loses typed rejection on the wire per /244 §1 hole 1.
Two design alternatives are in play. /244's incremental fix adds
two methods to `Lowering` (`reply_from_lowering_rejection`,
`reply_from_engine_rejection`) — three methods total, auxiliary
plumbing. /245 §1's cleaner shape drops the `RejectionReason`
associated type entirely and changes `lower()`'s signature to
`fn lower(&self, op: &Self::Operation) -> Result<Vec<SemaOperation>, Self::Reply>`,
so the Err path carries the contract's typed `Reply::*Rejected`
variant directly. The executor passes it through; no translation
layer. /245's shape reduces the trait to one method and makes the
verb-past-tense reply-naming convention from §3 below operative on
the wire without auxiliary methods.

persona-orchestrate is *already* better-positioned than the spirit
daemon discussed in /243 — its contract's `Reply::HandoffRejection`
carries the typed `HandoffRejectionReason` enum
(`SourceRoleDoesNotHold | TargetRoleConflict(Vec<ScopeConflict>)`),
so the typed reason is on the contract today. Under /244's shape,
the migration plugs the existing typed reply into the trait's
`reply_from_lowering_rejection` path; under /245's shape, the
`lower()` impl returns `Err(OrchestrateReply::HandoffRejected(...))`
directly. /245's shape is cleaner for persona-orchestrate because
the contract's typed rejection variants slot in at one place
instead of two.

The daemon-side refactor: `OrchestrateLowering` implements
`Lowering` over the ordinary contract's operation/reply pair;
`OwnerOrchestrateLowering` implements it over the owner pair;
`Executor` runs them against the sema engine; the hand-rolled
`OperationLowering` deletes.

Severity: high. The primitive exists; persona-orchestrate uses
none of it. The pending trait-shape decision (/244 vs /245) only
affects how the migration looks, not whether it's needed.

## 5 · Hole delta — `Watch` / `Unwatch` hand-rolled instead of the `observable` block

Per `signal-frame/macros/src/lib.rs` lines 28-31, the `observable`
block in `signal_channel!` declares observable events and auto-
generates the subscription protocol: macro-injected
`Observe(ObserverFilter)` and `Unobserve(...)` ops, a per-channel
`ObserverSet` runtime with `publish_*` methods (one per declared
event), an `ObserverFilterMatch` trait skeleton the contract
author implements, and stream-token plumbing.

`signal-persona-orchestrate` instead declares `Watch(ObservationSubscription
{ include_operations: bool, include_sema_effects: bool })` and
`Unwatch(ObservationToken)` as regular operations. No `observable`
block. No per-event `publish_*` methods. No typed `ObserverFilter`.
No event variants declared in the contract — the "observed events"
(inbound operations, outbound Sema effects) live only in the
daemon's runtime, not in the contract's event vocabulary.

This is exactly the hand-roll the `observable` block exists to
replace. Adopting the block would surface the verb collision in
hole alpha (resolved cleanly under /245 §2's grammar extension),
but it would also give persona-orchestrate the benefits: typed
event variants in the contract (so `persona-introspect` can decode
them), typed filter primitives (so subscribers pick what they care
about with type safety), and the macro's published publish-bridge
surface for the daemon to plug events into. The bridge concern
from /244 §1 hole 3 (no shared adapter between macro publish
closures and the executor's `ObserverChannel` trait) is upstream
to persona-orchestrate; /245 §3 proposes moving `ObserverChannel`
to `signal-frame` itself so the macro emits the impl automatically,
which makes the daemon-side adopt-observable step zero glue code.
Either way persona-orchestrate's hand-roll discards work the macro
will do for free.

Severity: high. Hand-rolled observability won't survive the
workspace's standardization on the `observable` block.

## 6 · Hole echo — bool-flag observation filter

`ObservationSubscription { include_operations: bool,
include_sema_effects: bool }` is filter-by-bool-flag. This is
precisely the smell `skills/typed-records-over-flags.md` (a
Keystroke-tier skill) warns against — *"Closed typed records over
bool flags. Surface the variant set in the type system."* The
typed alternative is `ObserverFilter` as a closed enum / record
carrying the subject and any predicates per /244 §1 hole 2's
discussion of typed filter primitives.

The bool-flag shape interacts with /244 §2 hole 4 (filter-match
trait impl is contract-author-trusted). The hand-rolled bool flags
have *no* filter logic — every subscriber with `include_operations
= true` sees every operation. /244's typed filter impls let
contract authors implement `matches_operation_received(...) ->
bool` per-event with arbitrary predicates. That's safer than no
filtering, with the trust caveat /244 hole 4 names: the impl is
contract-author code. /245 §4 concurs with /244's incremental
here — macro-generated closed-enum filter defaults are the right
shape. If persona-orchestrate adopted the observable block, the
bool flags become typed filter variants (`All`, `OnlyOperations
{ kinds: Vec<OrchestrateOperationKind> }`, etc.) with
macro-generated default impls; the contract author writes a
custom filter-match only when no preset variant fits.

Already partly covered in report 11 §4 from the typed-records angle;
this audit adds the migration-shape angle (the typed `ObserverFilter`
is now first-class via the macro).

Severity: medium.

## 7 · Hole foxtrot — Inter-contract reply-naming inconsistency

The owner contract conforms to the verb-past-tense rule for three
of its five reply variants (`RoleCreated`, `RoleRetired`,
`RepositoryIndexRefreshed`); the ordinary contract conforms to
zero of its ten variants. A reader switching between
`signal-persona-orchestrate` and `owner-signal-persona-orchestrate`
sees two different reply-naming idioms in the same triad. This is
worse than uniform non-conformance — the eye learns one pattern
from one file and gets the other wrong on the second.

The owner-contract divergences are also worth fixing:
`RoleCreationRejected` should be `CreateRejected` (the convention
keeps the rejection variant flat under the operation verb name;
the `Role` prefix is incidental to the operation and lives on the
payload). `OwnerOrchestrateRequestUnimplemented` is the unimplemented
catch-all and doesn't have an operation root, so it's a special
case — but `Unimplemented` alone reads cleaner if the
"Owner-Orchestrate-Request" prefix is workspace-coupled noise
(per `skills/naming.md` and ESSENCE.md §"Naming" — names don't
carry their full ancestry; the contract crate already says owner
and orchestrate).

Severity: medium. Mechanical fix; the convention is the standard.

## 8 · Hole golf — `RoleObservation` is a unit struct

`Observe(RoleObservation)` carries `RoleObservation` as a unit
struct — zero fields. The single reply `RoleSnapshot { roles,
recent_activity }` returns *everything* the daemon knows. There's
no filter, no selection, no pagination.

This is the same gap report 11 §4 named (typed Subscribe families
collapsed) from the read-side: a daemon with N kinds of observable
state should expose N typed reads, each with a typed filter
specifying which slice the caller wants. The unit-struct
`RoleObservation` says "give me everything you have" — fine for an
MVP but doesn't survive growth.

The post-/243 fix uses the `Lowering::lower` runtime decision:
`Observe(RoleObservation { filter: Option<RoleFilter> })` lowers
to a `Match` against the right table with the right predicate,
producing a snapshot scoped to the filter. Or split into
multiple read operations (`Observe`, `Inspect`, `List` etc.) per
the typed-records-over-flags rule.

Severity: medium. Operational gap; not blocking.

## 9 · Hole hotel — persona-orchestrate as the worked end-to-end example

/244 §2 hole 5: *"No end-to-end worked example."* The new
primitives (observable block, signal-executor, reply-naming
convention) exist as separate crates and skills; nothing
demonstrates the full path (contract crate → daemon with
`Lowering` impl → executor → observer subscriber → wire frame).
/244 §4 recommendation 4 names `signal-repository-ledger` (the
phase-3 pilot per /241 §7) as the natural candidate. /245 §5
sharpens this: don't write a separate example daemon; adopt
`observable` in `signal-repository-ledger` and let the existing
pilot serve as the canonical example. Its existing tests already
exercise a real contract, an external consumer (the gitolite hook
+ `ouranos` service), and real daemon dispatch — adding the
observable block + Lowering impl + a subscribing test reuses
that surface.

persona-orchestrate is the *second* natural candidate. It has
a real `Lowering` need (the typed contract verb → multi-effect
Sema dispatch persona-orchestrate already needs but doesn't yet
encode), a real observability surface (the hand-rolled `Watch`
/ `Unwatch` is exactly the use case the `observable` block
exists for), real domain-level rejection reasons
(`HandoffRejectionReason` etc.) already declared, and a non-trivial
authority chain (the owner contract carries different verbs than
the ordinary surface).

The opportunity: with `signal-repository-ledger` landing first as
the canonical worked example per /245 §5, persona-orchestrate
becomes the *second* example — and the divergences between the
two surface what's worth lifting into shared adapter crates
(though /245 §3 proposes the bridge crate is unnecessary if
`ObserverChannel` moves to signal-frame, in which case the second
example mostly validates the design rather than driving lift-out).
A workspace with two worked examples gets the abstraction right
faster than one with one. /233 §9 already names persona-orchestrate's
next arc as full-triad implementation; that arc absorbs the
post-/243 migration cleanly.

Severity: opportunity, not hole. Names a positive.

## 10 · Migration shape — what a post-/243 persona-orchestrate refactor looks like

Five steps, in priority order. The shape changes meaningfully
depending on whether /244's incremental fixes or /245's cleaner-
shape proposals land first. Both paths are sketched.

Step one: settle the `Observe` verb question. Under /244 §1
hole 2 incremental, the macro-injected verb renames to `Probe`
or `Tap` workspace-wide; persona-orchestrate keeps its `Observe`.
Under /245 §2, the `observable` block grammar extends to let the
contract author name the open/close verbs; persona-orchestrate
keeps `Observe(RoleObservation)` *and* picks `Watch`/`Unwatch` for
the observable surface (the names the hand-rolled ops already
use). Either way persona-orchestrate's own work is light;
/245's path is lighter still because no contract anywhere needs
to rename.

Step two: rewrite the ordinary contract's reply variants per the
verb-past-tense convention. Ten reply variants in the ordinary
contract, two in the owner contract (`RoleCreationRejected` →
`CreateRejected`, `OwnerOrchestrateRequestUnimplemented` →
`Unimplemented` plus the prefix call). Mechanical change touching
contract source + every round-trip witness. The contract's typed
rejection reasons (`HandoffRejectionReason`, `ScopeConflict`,
`RoleCreationRejectionReason`) carry over unchanged as payload
variants of the renamed `*Rejected` replies. This step is the
same under /244 and /245.

Step three: adopt the `observable` block. Replace
`Watch(ObservationSubscription)` and `Unwatch(ObservationToken)`
with `observable { event OperationReceived(...) event
SemaEffectEmitted(...) ... }` in the channel macro. Under /244,
the macro injects the renamed verb (`Probe`/`Unprobe` or whatever
lands); under /245 §2, the block declares
`operation_open Watch(Filter) opens OrchestrateObserverStream`
and `operation_close Unwatch(OrchestrateObserverToken)`
explicitly. The contract author writes the filter-match impl with
typed predicates; under /244 §2 hole 4 + /245 §4, the macro
generates closed-enum defaults for common shapes (`All`,
`OnlyOperations { kinds }`, etc.), so most cases need no custom
impl.

Step four: implement `signal-executor::Lowering` for both the
ordinary and the owner contract surface. Under /244's trait
shape, `OrchestrateOrdinaryLowering` declares `Operation`,
`Reply`, `RejectionReason` associated types plus `lower`,
`reply_from_effects`, `reply_from_lowering_rejection`,
`reply_from_engine_rejection`. Under /245 §1's shape, the
`RejectionReason` associated type drops and `lower()` returns
`Result<Vec<SemaOperation>, Self::Reply>` with Err carrying the
typed `OrchestrateReply::HandoffRejected(...)` variant directly —
one method instead of three or four. The hand-rolled
`OperationLowering` deletes either way; the daemon's `service.rs`
dispatch routes through `Executor::execute` instead of bespoke
`handle()` / `handle_owner()`.

Step five: position as the second worked example. With
`signal-repository-ledger` adopting `observable` first per /245
§5, persona-orchestrate is the second example through the new
primitives — validating the abstraction across two daemons before
the phase-3 fan-out across the remaining eight-plus
`signal-persona-*` contracts. /233 §9 already names this as the
next arc; the post-/243 migration shape slots into that arc
without a separate report cycle.

Across the five steps, the contract gains: typed observability
through a shared macro feature, typed rejection on the wire
through a shared trait, naming consistency with the rest of the
workspace, and a published `Lowering` impl that other daemons
can read as the worked pattern. The /245 path is consistently
the cleaner shape — fewer methods on `Lowering`, fewer
workspace-uniform constraints to maintain, no auto-generated
bridge crate needed. Whether to wait for /245's proposals to
land before starting the persona-orchestrate refactor depends on
how the bundled fix in /245 §7 progresses; in the meantime, the
audit findings hold against the current primitive shape.

## 11 · References

`reports/operator-assistant/157-persona-orchestrate-dynamic-role-mvp.md`
— the implementation under audit.

`reports/second-designer-assistant/11-audit-of-operator-assistant-157-persona-orchestrate-mvp.md`
— the companion audit against /233 + /241; this report extends
the audit to the post-/243 primitives.

`reports/designer/244-hole-finding-after-243-implementations.md`
— the post-/243 hole inventory; §§1, 2, 4 supply this audit's
grading lens.

`reports/designer/245-design-alternatives-for-244-holes.md`
— designer rethinks for three of /244's five holes (typed
rejection via `lower()`'s Err path; contract-author-named
observable verbs; `ObserverChannel` to `signal-frame`).
Proposals, not yet landed; each hole's section above flags
where /245 changes the resolution path.

`reports/designer/243-reply-naming-observer-hook-executor-trait.md`
— the designs whose implementations /244 audits.

`reports/designer/241-signal-architecture-migration-guide.md`
— the migration spec; §5's "lowering may be 0 → many Sema
operations" is the rule the static map in `OperationLowering`
defeats and the `Lowering` trait makes ergonomic.

`reports/designer/233-persona-orchestrate-operator-handoff.md`
— the designer handoff; §4's authority chain and §6's sema
state schema constrain what `Lowering` impls need to express.

`skills/contract-repo.md` §"Reply discipline" — verb-past-tense
reply-naming rule (success: verb-past matching the operation root;
rejection: verb-past + `Rejected`; payload variants carry domain
reasons).

`skills/typed-records-over-flags.md` — the rule the bool-flag
`ObservationSubscription` violates and the typed `ObserverFilter`
respects.

`/git/github.com/LiGoldragon/signal-executor/src/{lib,lowering,executor,observer,effect,engine,error}.rs`
— the `Lowering` trait, `Executor` runtime, `ExecutorOutcome`,
`SemaEngine` trait. Hand-rolled `OperationLowering` parallels what
this crate now provides.

`/git/github.com/LiGoldragon/signal-frame/macros/src/lib.rs`
lines 28-31 (and the surrounding `observable` block implementation)
— the macro feature `signal-persona-orchestrate` should adopt
instead of hand-rolling `Watch` / `Unwatch`.

`/git/github.com/LiGoldragon/signal-persona-orchestrate/src/lib.rs`
lines 441-720 (request/reply declarations), 836-842 (the ten
`OrchestrateReply` noun-form variants).

`/git/github.com/LiGoldragon/owner-signal-persona-orchestrate/src/lib.rs`
— the owner contract's mixed naming convention; `RoleCreated` /
`RoleRetired` / `RepositoryIndexRefreshed` conform,
`RoleCreationRejected` and `OwnerOrchestrateRequestUnimplemented`
don't.

`/git/github.com/LiGoldragon/persona-orchestrate/src/lowering.rs`
lines 28-49 — the hand-rolled `OperationLowering` static map.

Bead `primary-699g` (P2, persona-orchestrate component design)
— the design bead this work responds to; needs scope extension
for the post-/243 migration.

Bead `primary-es9` (P2, persona-harness daemon, closed
HarnessKind) — names persona-harness as the home for closed
`HarnessKind`; report 11 §8 flagged the wrong-home placement
in persona-orchestrate.

Bead `primary-ojxq` (P1, persona-spirit triad) — the canonical
post-/243 first candidate per /244 references; persona-orchestrate
is the second.
