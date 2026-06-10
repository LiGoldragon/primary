# Spirit Intent Redesign Feedback After 578 Revision

Reviewed target: `reports/designer/578-intent-redesign-synthesis.md`

Companions checked:

- `reports/designer/577-intent-tool-state-and-the-real-flaw.md`
- `reports/designer/579-spirit-agglomeration-pass-2026-06-10.md`
- `/git/github.com/LiGoldragon/spirit/schema/signal.schema`
- `/git/github.com/LiGoldragon/spirit/src/store.rs`
- `/git/github.com/LiGoldragon/spirit/tests/collect_removal_candidates.rs`
- `/git/github.com/LiGoldragon/spirit/tests/process_boundary.rs`

This refresh replaces the previous content of this report. The edited `578`
resolved several earlier objections: handoff is block-for-now, retired arrows
archive, `Weight` is dedicated, `topic` is renamed to `category`, and
`Clarification` is an operation rather than a kind.

## Current Read

The revised synthesis is much closer to implementable. Its live-state model is
now coherent: stored records are current forward arrows; correction,
clarification, retirement, and supersession are operations/events around that
state; retired arrows leave the live query surface but remain recoverable in an
archive.

The most important implementation correction is already present in current
Spirit source: `Query` now has `CertaintySelection`, ordinary observation hides
zero-certainty records, and `CollectRemovalCandidates` uses exact zero certainty
for safe collection. The old "query cannot filter magnitude" blocker is stale
for current source, though it remains accurate for deployed v0.4.0 as described
in `577` and `579`.

What still needs attention is the contract layer between the revised design and
production code. The design now names the right semantic pieces; implementation
still needs record snapshots, category migration, durable operation history,
blocking harness transport, and precise write-operation schemas.

## Clear Attention Items

### 1. Observation must return identifiers

The revised design says full-text search returns whole records with identifiers,
categories, and text. Current Spirit still exposes identifier-bearing reads only
through `Lookup`; `Observe` returns `ObservedRecords` containing `Entry` values
without `RecordIdentifier`.

That is now the highest-priority schema gap. Guardian refusals, supersede
operations, auditor retirements, and category migration all need query results
that name the records they refer to.

Recommendation: introduce a snapshot type such as
`RecordSnapshot { RecordIdentifier Entry }`, and make the agent-facing query
surface return snapshots. Do this before guardian or auditor work.

### 2. Clarify needs durable before-and-after history

The edit correctly moves `Clarification` from kind to operation. The risky part
is "refine wording in place." If the old wording is overwritten without a
durable operation journal, a bad clarification is hard to audit or reverse.

The same is true for derived keyword behavior: a meaning-preserving wording
change can still change the keyword index and therefore retrieval/ranking.

Recommendation: a `clarify` operation should journal old entry, new entry,
guardian verdict, and database marker outside the live query surface. It should
emit a clarification event, and tests should prove the record identifier is
stable while the previous wording remains recoverable.

### 3. Blocking handoff needs an exact transport contract

The revised report chooses synchronous block for now because there is no callback
mechanism. That is a valid user contract, but it makes transport a production
design point rather than a detail.

The daemon cannot parse NOTA or embed the harness. The harness is described as a
separate client process. For a blocking gate, Spirit therefore needs a typed
signal request/reply path to that process, with timeout, failure, retry, and
refusal semantics.

Recommendation: define the blocking harness exchange explicitly:

- how Spirit discovers or is configured with the harness endpoint;
- what typed signal carries the proposal bundle;
- what typed signal returns the verdict;
- what happens on timeout, malformed verdict, model failure, or harness absence;
- whether the write is rejected or parked on infrastructure failure.

Until that exists, "daemon gathers records and hands them to the harness" is
still a diagram, not an implementable contract.

### 4. Binary verdict still needs typed refusal reasons

The revised design keeps the guardian's authority binary: yes or no. That is
right. But implementation still needs the no to be typed, not only prose.

The proposing agent needs machine-actionable reasons: duplicate, contradiction,
compound statement, non-intent/task-state, unclear privacy, unclear category,
clarify-tramples, clarify-loses-meaning, supersede-target-missing, and
retrieval-insufficient. Those reasons do not grant guardian discretion; they
make the refusal testable and revisable.

Recommendation: model `CaptureVerdict` or `GuardianVerdict` as an enum with
referenced `RecordSnapshot`s plus a short explanation string for human review.

### 5. Category rename needs a migration artifact

The revised design settles `topic` to `category`, closed and broad. Current
source still has `Topic`, `Topics`, and exact string matching. This cannot be a
cosmetic rename only.

Implementation needs:

- canonical category declarations;
- aliases/mappings from existing topic strings;
- a bootstrap clustering report or data file for psyche approval;
- rejection or enlargement flow for unknown categories;
- migration tests proving old narrow topics become broad category plus keyword.

Recommendation: build the category catalog before rewriting record kinds or
guardian prompts. Category is the retrieval spine; if it stays free-text during
guardian work, the guardian inherits the current recall problem.

### 6. Weight definition is settled, but its mechanics are not

The revised design correctly separates dedicated `Weight` from `magnitude`.
It defines weight as reaffirmation count and says repetition raises weight
instead of adding records.

The missing operational details are:

- how duplicate detection chooses "raise weight" instead of "new record";
- whether weight is monotonic;
- whether weight decays or can be lowered by audit;
- whether guardian can propose weight changes;
- how ranking combines category, keyword, full text, certainty, and weight.

Recommendation: make weight a typed field with explicit update operations and
ranking tests. Do not let it become an informal counter updated through
`ChangeRecord`.

### 7. Keyword extraction should be deterministic and tested

The revised report decides keyword extraction is derived on the fly from
asterisk emphasis in descriptions. That avoids stored-field drift, but it still
needs a small deterministic spec.

Recommendation: define and test case folding, phrase spans, repeated spans,
literal asterisks, unmatched asterisks, and interaction with bracket-string
text. Full-text search should remain the recall floor, as the report says.

### 8. Kind migration is now clearer but still large

The target kind set is now Decision, Principle, Constraint. Correction becomes
an event. Clarification becomes an operation.

Implementation still needs a migration pass over existing records:

- corrections become supersede/archive history or are folded into current
  forward records;
- clarifications become clarify events plus current rewritten records, or are
  reclassified as forward arrows;
- existing queries and docs stop treating Correction and Clarification as live
  kinds.

Recommendation: write migration fixtures from real `.schema` or exported record
files, not inline Rust strings, and prove both old-store import and new-store
query behavior.

## Updated Build Order

1. Add identifier-bearing observation snapshots.
2. Add category catalog plus old-topic migration map.
3. Add dedicated `Weight` and explicit weight update/ranking behavior.
4. Add durable operation journal/archive entries for clarify, supersede, retire,
   guardian refusal, and auditor proposals.
5. Define the synchronous harness signal exchange and failure modes.
6. Define typed guardian verdicts/refusal reasons.
7. Add deterministic keyword extraction and full-text search.
8. Migrate `Kind` to Decision/Principle/Constraint with real fixture coverage.
9. Wire guardian checks into propose, clarify, and supersede.
10. Only after that, automate the auditor.

## Net Feedback

The edited `578` is now a strong design basis. The biggest prior conceptual
gaps are closed.

The remaining risk is implementation order. If Spirit builds the guardian before
identifier-bearing reads, category migration, durable operation history, and a
real blocking harness transport, it will recreate the same bloat in a more
complex shape. The next production slice should be the contract substrate, not
the LLM judgment loop.
