# 51 - review of designer 162 signal verb roots

*Designer-assistant report, 2026-05-14. Reviews
`reports/designer/162-signal-verb-roots-synthesis.md` against the
current workspace architecture, `signal-core`, contract discipline, and
the earlier DA proposal in `reports/designer-assistant/50-signal-core-base-verb-shape.md`.*

## 0. Position

Designer 162 is the right canonical decision document for the
`signal-core` verb-root question.

I agree with its operative decision:

```text
Assert  Mutate  Retract  Match  Subscribe  Atomic  Validate
```

These seven should be the closed `SignalVerb` root set. The other five
current names:

```text
Constrain  Project  Aggregate  Infer  Recurse
```

should survive as typed read-plan/query-algebra vocabulary, not as
frame roots.

The best conceptual sentence from 162 is the stratum split:

```text
12 = static vocabulary / semantic lattice
7  = dynamic operation roots
```

That is the clean way to preserve the value of the older twelve-name
Nexus/Sema work while correcting the shape of `signal-core`.

## 1. What 162 gets right

### 1.1 The seven-root conclusion is now well supported

The seven-root conclusion is no longer just a local design instinct.
Designer 162 brings together four independent kinds of evidence:

- database and distributed-system traditions;
- linguistic and Sanskrit grammar research;
- astrology, Arthur Young, and the 12/7 split;
- workspace archeology.

The important engineering evidence is still the same: roots should
change boundary behavior. `Project`, `Aggregate`, `Constrain`, `Infer`,
and `Recurse` change read computation, not the operation mode at the
Signal frame boundary.

### 1.2 The archeology matters

The report's lineage point is strong: the older `signal` repository
already had the seven-ish shape:

```text
Assert  Mutate  Retract  AtomicBatch  Query  Subscribe  Validate
```

After renaming `Query` to `Match` and `AtomicBatch` to `Atomic`, that is
the current recommendation. The May 2026 widening to twelve looks like
vocabulary recovery, not a root-criterion proof. That is exactly the
mistake to undo now.

### 1.3 The rename from `SemaVerb` to `SignalVerb` is correct

`SemaVerb` is the wrong public type name for `signal-core`. The type
classifies Signal messages at the wire boundary. Some consumers execute
those operations through `sema-engine`; not every Signal boundary is
literally a sema-engine call.

The rename should happen in the same breaking pass that shrinks the
root set.

## 2. Implementation blockers in 162

162 is good as a synthesis report, but it needs a few sharpenings before
it becomes a clean operator brief.

### 2.1 `ReadPlan` ownership must be explicit

162 says the five demoted verbs move into typed `ReadPlan<R>`. That is
right, but it does not say where `ReadPlan<R>` lives.

The rule should be:

- `signal-core` owns `SignalVerb`, frame envelopes, handshake, pattern
  markers, and small domain-free wire identity records.
- `signal-core` does **not** own `ReadPlan`.
- `sema-engine` owns the reusable engine-side `ReadPlan` / `QueryPlan`
  vocabulary.
- domain contract crates may own domain-specific query payloads that
  compile or lower into `sema-engine` query plans.

If this is not stated, an operator could accidentally move
`Constrain`, `Project`, `Aggregate`, `Infer`, and `Recurse` from
`SemaVerb` into a new `signal-core::ReadPlan`, making `signal-core` a
query-engine vocabulary crate. That would violate the current
wire-kernel split.

### 2.2 Stale skill and architecture text must be part of the work

The following files still describe the twelve-root model and need to be
updated as part of the adoption pass:

- `skills/contract-repo.md`
- `/git/github.com/LiGoldragon/signal-core/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal/README.md`

Other contract architecture files mention `SemaVerb` and should at
least be scanned:

- `/git/github.com/LiGoldragon/signal-persona-mind/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal-persona-introspect/ARCHITECTURE.md`
- any `signal-persona-*` repo with a `sema_verb()` mapping witness.

The most important stale skill text is in `skills/contract-repo.md`,
which currently says:

```text
Assert Subscribe Constrain Mutate Match Infer
Retract Aggregate Project Atomic Validate Recurse
```

That skill needs to become the seven-root rule. It should also explain
that the five demoted words are read-plan vocabulary under `Match` or
`Subscribe`, not legal frame roots.

### 2.3 The `Atomic` and `Validate` rename should not ride this pass

162 handles this mostly correctly, but the wording could be tightened.
It says to defer `Atomic` to `Bind` and `Validate` to `Assay`, while
also suggesting that a future breaking pass could take those renames.

My recommendation:

```text
Do not rename Atomic or Validate in the current SignalVerb pass.
```

The current pass should change only:

- `SemaVerb` to `SignalVerb`;
- twelve root variants to seven root variants;
- the demoted five into query/read-plan vocabulary.

`Atomic` and `Validate` are clear technical words. `Bind` and `Assay`
are interesting language-design candidates, but they need pressure from
real contract examples before becoming code names.

### 2.4 `Structure` needs a stricter default rule

162 raises `Structure` as a falsifiable eighth-verb candidate for
DDL-shaped operations. It also correctly says not to add it now.

The containment rule should be stronger:

```text
Schema/catalog changes default to Assert, Mutate, Retract, or Atomic.
Structure appears only if concrete DDL traffic cannot be honestly modeled
as data changes over schema/catalog records.
```

In the Persona/Sema worldview, schema is also data. That means creating
a table descriptor can be an `Assert`; changing an index descriptor can
be a `Mutate`; removing a deprecated relation can be a `Retract`; and
a migration can be an `Atomic` bundle. `Structure` should require a
real failure of that model, not just similarity to SQL DDL.

### 2.5 Temporary research artifacts should not be load-bearing

162 cites `/tmp/verb-research-{database,linguistics,astrology,archeology}.md`
as stream outputs. The synthesis report carries enough of the evidence,
so this is not a functional problem.

Still, `/tmp` files are not workspace memory. If any stream output is
meant to be durable evidence, the relevant part should be summarized in
162 or committed as an appendix report. Otherwise the `/tmp` references
should be treated as provenance notes, not sources future agents are
expected to find.

## 3. Concrete operator work implied by 162

If the user approves implementation, the work should be framed as one
coordinated breaking pass.

### 3.1 `signal-core`

Change the public root enum:

```rust
pub enum SignalVerb {
    Assert,
    Mutate,
    Retract,
    Match,
    Subscribe,
    Atomic,
    Validate,
}
```

Remove `Constrain`, `Project`, `Aggregate`, `Infer`, and `Recurse` from
the root enum and request constructors.

Rename `Request<Payload>::verb()` to return `Option<SignalVerb>`.
Keep `Handshake` as frame-control unless the user explicitly decides
that transport setup must become an operation root.

Update witnesses:

- root enum has exactly seven variants;
- no root constructor exists for the five demoted read-plan names;
- handshake is frame-control, not a Signal operation;
- every domain request maps to exactly one `SignalVerb`.

### 3.2 `sema-engine`

Own the reusable read-plan/query-plan vocabulary:

```text
Constrain
Project
Aggregate
Infer
Recurse
```

The first implementation can still leave some of these as typed
unimplemented query-plan variants. The key point is architectural:
these names are now plan nodes under `Match` / `Subscribe` / `Validate`,
not frame roots.

### 3.3 Contract repos

Rename `sema_verb()` to `signal_verb()` during the breaking pass, or
leave a temporary compatibility alias only if the migration becomes too
large for one pass.

The current scan shows `signal-persona-mind` already maps request
variants using only five of the seven roots:

```text
Assert  Match  Subscribe  Mutate  Retract
```

That supports 162's point: no current consumer appears to depend on the
five demoted names as roots.

### 3.4 Skills and documentation

Update `skills/contract-repo.md` before or in the same commit stack as
the code change. Agents will keep reproducing the twelve-root model
until the skill changes.

Minimum replacement rule:

```text
Signal is the typed binary database-operation language. Every
cross-component operational Signal request declares exactly one
SignalVerb: Assert, Mutate, Retract, Match, Subscribe, Atomic, or
Validate. Query algebra such as Project, Aggregate, Constrain, Infer,
and Recurse lives inside typed read-plan payloads; it is not a frame
root.
```

## 4. Recommended edits to 162

If designer revises 162, I would add four direct notes:

1. `ReadPlan` belongs in `sema-engine` and domain query payloads, not
   in `signal-core`.
2. `skills/contract-repo.md` and `signal-core/ARCHITECTURE.md` are
   mandatory stale-text edits for the adoption pass.
3. `Atomic` and `Validate` keep their current names for this pass.
   `Bind` and `Assay` stay future language-design candidates.
4. `Structure` is blocked by a concrete counterexample to schema-as-data.
   Until then, schema/catalog operations use the existing seven roots.

## 5. Final recommendation

Treat designer 162 as accepted architecture with implementation
sharpenings.

The implementation should not be "take 162 literally and start moving
types." It should be:

1. Shrink and rename the frame-root enum in `signal-core`.
2. Move query algebra into `sema-engine` / domain query payloads.
3. Update contract mappings from `sema_verb()` toward `signal_verb()`.
4. Update the skill and architecture text so future agents stop
   resurrecting the twelve-root model.

That gets the workspace to the desired rule:

```text
All operational Signal messages fit inside one of the base signal-core
verbs.
```

## 6. Addendum after designer revised 162

Designer revised `/162` after this report's first pass. The revised
document absorbs most of the structural critique above:

- `ReadPlan` is now explicitly assigned to `sema-engine`, not
  `signal-core`.
- `Atomic` and `Validate` are explicitly kept for the current pass.
- `Structure` is contained behind the schema-as-data default rule.
- `/tmp` research artifacts are no longer load-bearing sources.
- required documentation edits are listed directly in `/162`.

That makes `/162` good as canonical architecture. Remaining issues are
handoff/status issues, not objections to the seven-root decision.

### 6.1 Status table should distinguish prior state from live state

`/162` now has a required documentation edits table. The table is
useful, but the workspace is moving while the report is being read.
Some rows already changed in the live tree: `skills/contract-repo.md`,
`signal-core/ARCHITECTURE.md`, and `signal-core/src/request.rs` now
show the seven-root `SignalVerb` model.

To avoid sending operators after completed stale-text edits, `/162`
should phrase that table as:

```text
Prior state | Target | Status
```

rather than:

```text
Today | Target
```

The point is not to rewrite history. The point is to keep `/162`
implementation-safe as operators continue landing pieces in parallel.

### 6.2 Add an explicit contract-crate sweep

The revised `/162` correctly says every contract request declares
`signal_verb()`, but its implementation checklist should explicitly
require a sweep of every direct `signal-core` consumer.

Current live scan still finds stale `SemaVerb` / `sema_verb()` mentions
in at least `signal-persona-introspect`; the operator lock shows active
migration work in `signal-persona`, `signal-persona-mind`, and
`persona-mind`.

The missing row:

```text
All signal-* contract repos with verb mappings must migrate from
SemaVerb/sema_verb() to SignalVerb/signal_verb(), or be explicitly
listed as pending.
```

Without that row, an operator can shrink `signal-core` correctly while
leaving dependent contract crates in a half-migrated state.

### 6.3 Put `sema-engine` ownership in the TL;DR

The body now says `ReadPlan<R>` belongs in `sema-engine`; the TL;DR
still says only "Move five demoted to typed `ReadPlan<R>`." Skimming
agents will read the TL;DR first and may miss the boundary.

The TL;DR should say:

```text
Move the five demoted names to typed sema-engine ReadPlan<R> operators.
```

That closes the ambiguity at the highest-friction reading point.

### 6.4 Split macro work from constructor work

The `/162` required-edits table currently combines two surfaces:

- `Request::assert(...)` and other free-form request constructors;
- `signal_channel!` macro support for verb annotations and generated
  mapping witnesses.

Those are related but not the same implementation. Split them into two
rows so an operator can land them independently:

- `src/request.rs`: seven constructors only; demoted-root constructors
  removed; unchecked generic operation constructor explicitly treated
  as low-level/internal.
- `signal_channel!`: variant-level verb annotations, generated
  `signal_verb()`, and generated/required witnesses.

### 6.5 Updated bottom line

The design is settled enough to implement. The only remaining issue is
keeping the implementation handoff precise while operators are already
landing pieces.

The clean next handoff is:

1. Keep `/162` as canonical seven-root architecture.
2. Update `/162`'s required-edits section to be status-aware.
3. Add a direct contract-crate migration row.
4. Keep `ReadPlan` ownership visible in the TL;DR.
5. Split constructor cleanup from macro generation work.

## 7. Context-maintenance note after follow-up landings

Designer subsequently applied the §6 handoff corrections to `/162`, and
operators began landing the actual code migration. Treat §6 as the
review trail, not as the current todo list.

Current state observed during context maintenance:

- `reports/designer/162-signal-verb-roots-synthesis.md` now has a
  status-aware table, explicit `sema-engine` `ReadPlan` ownership in
  the TL;DR/body, a contract-crate sweep row, and separate rows for
  request constructors and `signal_channel!`.
- `skills/contract-repo.md` now names the seven `SignalVerb` roots and
  says the read-algebra names live in `sema_engine::ReadPlan`.
- `signal-core` now exposes `SignalVerb` with seven variants,
  `RequestPayload::signal_verb()`, payload-first request construction,
  and `unchecked_operation` as the named low-level escape hatch.
- `sema-engine` architecture now states that schema/catalog operations
  are catalog data under the seven roots, not an eighth `Structure`
  root.

The remaining implementation risk is the downstream contract sweep, not
the root decision itself. At the time of this note, `/162` still marks
some direct `signal-core` consumers as partially migrated. Those crates
need either `SignalVerb`/`signal_verb()` migration or an explicit pending
status in `/162`.

### 7.1 `Structure` conclusion

The latest designer examples make the seven-only case stronger:

```text
DDL is the same acts applied to the catalog table.
```

In the workspace model, SQL's fused `CREATE TABLE` operation separates
into:

```text
declare shape       -> Rust type / contract
allocate storage    -> internal sema-engine work
make visible        -> Assert/Mutate/Retract catalog row, often under Atomic
```

So `Structure` is not a root now. It remains a named pressure point only
if future traffic proves a schema operation has different Signal
boundary semantics from catalog writes. Runtime user-defined types alone
are not enough; they can still begin as `Assert(RuntimeRecordKind)`,
`Assert(RuntimeField)`, `Validate(RuntimeSchema)`, and `Atomic([...])`.
The pressure becomes real only when schema changes require distinct
visibility, consensus, invalidation, or legality semantics at the wire
boundary.
