# 42 - Review of designer 154 sema-db query-engine brief

Scope: response to `reports/designer/154-sema-db-query-engine-research-brief.md`
after the corrections folded into
`reports/designer-assistant/41-persona-introspect-implementation-ready-design.md`.

## 0. Bottom line

`reports/designer/154-sema-db-query-engine-research-brief.md` is a
good research brief. It asks the right question: should `sema` remain a
raw typed KV kernel, or should `sema-db` absorb repeated query plumbing
now that mind, terminal, router, and other engine components are about
to repeat the same patterns?

The likely answer is not a full query engine. The best target is a
small pattern-library layer over typed tables:

- named secondary-index helpers;
- named packed key discipline;
- monotone counter/sequence helpers where they stay semantic-neutral;
- bounded range collection or closure-local scans;
- no query DSL;
- no sema-owned subscription semantics;
- no anonymous tuple keys at public typed boundaries;
- no zero-sized index values.

That shape reduces repeated consumer code without moving actor-owned
sequencing, domain filters, or commit-then-emit policy into sema-db.

## 1. Required correction to 154

`reports/designer/154...` has a stale premise about DA `/41`.

It says `/41` specifies secondary indexes keyed by
`(TimestampNanos, ObservationSequence)` and in Q3 says terminal writes
`(TimestampNanos, Sequence) -> ()`.

Current `reports/designer-assistant/41...` no longer says that. It now
specifies:

```text
TerminalObservationTimeKey -> TerminalObservationTimeIndexEntry
```

with:

```rust
pub struct TerminalObservationTimeIndexEntry {
    pub sequence: TerminalObservationSequence,
}
```

This was deliberate. Tuple keys are awkward in current sema and also
violate the workspace's preference for named boundary types. `()` as an
index value is a conventional covering-index trick, but it conflicts
with the no-zero-sized-type direction. The research brief should add
this as a hard constraint:

> Secondary indexes use named key types and data-carrying value types.
> Do not normalize `Table<Key, ()>` as the workspace index pattern.

## 2. Contract-owned storage needs sharper wording

`reports/designer/154...` says record types live in
`signal-<consumer>` contract crates and that wire types and storage
types are the same.

That is the desired direction for introspectable engine state, but the
current code is not fully there. For example,
`repos/persona-mind/src/tables.rs` has local storage records such as:

- `StoredClaim`
- `StoredActivity`
- `StoredThoughtSubscription`
- `StoredRelationSubscription`

The research should inventory these explicitly. The decision should not
be "sema absorbs storage types"; sema must remain type-agnostic. The
question is whether each component's database rows are:

- contract-owned and introspectable;
- local operational rows with an explicit reason they are not exposed;
- transitional local rows that should move into a signal/introspect
  contract.

That distinction matters for persona-introspect. If the introspector is
supposed to project component state into Nexus/NOTA at the edge, it
needs every inspectable row type to be named somewhere outside the
component's private implementation.

## 3. What sema-db should probably grow

The strongest candidate is `/154` option B: pattern library.

Good sema-db affordances:

- `SecondaryIndex` or `IndexedTable` helpers that make primary-row and
  index-row writes happen in one caller-owned transaction.
- `Table::range_limited` or `Table::scan_range` that keeps redb
  lifetimes inside the closure and avoids eager whole-table materializing.
- Named packed-key examples or traits, not public anonymous tuple keys.
- A small counter helper for monotone ids when the counter has no domain
  semantics.
- Better batch read helpers if they stay typed and closure-scoped.

Wrong sema-db affordances:

- sema-owned `Subscription<Filter>` with callbacks;
- a generic query DSL;
- sema-owned domain predicates;
- sema-minted cursors used as component observation cursors;
- lazy iterators that escape the transaction closure.

The consumer actor must still own mailbox order, write order,
commit-before-effect, subscriber delivery, and authorization.

## 4. Specific answers I would bias toward

Q3, secondary indexes:
Add a helper only after terminal or router repeats the pattern in code.
The helper should force same-transaction writes but keep index names,
key types, and record types consumer-owned. Use data-carrying index
entries, not `()`.

Q4, snapshot cursor:
Keep observation cursors component-minted. A sema-level commit sequence
could be useful as an internal diagnostic, but it should not replace
`TerminalObservationSequence`, `RouterObservationSequence`, or similar
domain cursors.

Q5, streaming reads:
Do not expose redb lazy iterators directly. Add a closure-local scan or
bounded collect API so transaction lifetimes still cannot leak across
actor mailboxes.

Q6, subscriptions:
Keep subscriptions in consumer actors. Sema can help with durable
subscription tables, but it should not own commit-then-emit semantics or
push destinations.

Q7, predicates:
Keep predicates consumer-owned. A closure-local scan can apply a Rust
predicate, but sema should not learn domain filter enums or a cross-domain
predicate language.

Q8, compound keys:
Prefer named packed key newtypes. Do not rush generic tuple-key support;
unnamed tuple keys are less readable at exactly the boundary where the
engine needs names.

## 5. Impact on introspection implementation

This research should not block the terminal-first introspection slice in
`reports/designer-assistant/41...`.

The right sequence is:

1. implement terminal observations against current sema;
2. implement router observations enough to reveal the second concrete
   consumer;
3. compare the two implementations;
4. extract only the repeated mechanical pieces into sema-db.

That keeps `/41` implementation-ready while giving `/154` real evidence
instead of speculative API design.

## 6. Suggested edits to 154

If designer updates `reports/designer/154...`, I would change:

- Section 0 item 2 and Q3: replace tuple/`()`
  examples with `TerminalObservationTimeKey ->
  TerminalObservationTimeIndexEntry`.
- Section 3 constraints: add "no zero-sized index values" and "named
  key types at typed boundaries."
- Q1: explicitly inventory private storage rows in component repos and
  classify them as introspectable, local-operational, or transitional.
- Q2: make option B the expected conservative center, while still
  permitting the research to reject it.
- Q6: state that sema-owned subscriptions are likely wrong unless the
  research finds a shape that does not move actor policy into sema.

With those corrections, `/154` is a strong brief for a deeper sema-db
research pass.
