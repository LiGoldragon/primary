# Operator Audit 351 - Spirit Intent Redesign Synthesis Feedback

Target reviewed: `reports/designer/578-intent-redesign-synthesis.md`

Companions checked:

- `reports/designer/577-intent-tool-state-and-the-real-flaw.md`
- `reports/designer/579-spirit-agglomeration-pass-2026-06-10.md`
- `/git/github.com/LiGoldragon/spirit/schema/signal.schema`
- `/git/github.com/LiGoldragon/spirit/src/store.rs`
- `/git/github.com/LiGoldragon/spirit/src/engine.rs`
- `/git/github.com/LiGoldragon/spirit/src/daemon.rs`

## Summary

The synthesis is directionally strong. The state/stream split is the right
model: live intent should be coherent at rest, while correction/supersession is
motion. The guardian/auditor split is also the right division of labor: a write
door prevents new bloat; a rest-time distiller repairs accumulated bloat.

The production risk is that the synthesis currently mixes three different
layers:

- the ideal semantic model,
- the daemon contract needed to expose that model,
- the agent workflow needed to operate it.

Before implementation, those need to be separated into typed operations and
state transitions. Otherwise the first implementation will either embed agent
judgment in the daemon, or ship a guardian that cannot query, refuse, collect,
or explain with enough precision.

## Findings

### 1. Magnitude-aware query is the first hard blocker

The synthesis names magnitude-aware query as the keystone, and that is correct.
It is more than an unlock; it is a safety prerequisite.

Current Spirit schema:

- `Entry` has `Topics`, `Kind`, `Description`, `Magnitude`, `Privacy`.
- `Query` has only `TopicMatch`, optional `Kind`, and `PrivacySelection`.
- `CollectRemovalCandidates` wraps a `Query`.

Current store behavior in `/git/github.com/LiGoldragon/spirit/src/store.rs`:

- `Query::matches` checks topic, kind, and privacy only.
- `Entry::magnitude_weight` exists, but query matching does not use it.
- `CollectRemovalCandidates` iterates records and removes everything matching
  the query, because the query cannot express candidate certainty.

So the next production step should not be "guardian" in isolation. It should be
the query contract upgrade:

- add a magnitude/certainty selector to `Query`;
- make default observation exclude soft-tombstones or explicitly choose whether
  tombstones are visible;
- make collection target only the candidate magnitude range;
- add tests proving a `Zero`-magnitude public record is not accidentally
  collected unless the query says so.

Without this, the current collection operation is too broad for the manual
agglomeration result in `579`.

### 2. Identifier-bearing reads are required for any real auditor

`579` had to snapshot the database and recover identifiers outside the Spirit
contract. That is a production blocker for the auditor and a practical blocker
for guardian explanations.

Current replies split identifiers unevenly:

- `Lookup` returns `FoundRecord` with `RecordIdentifier`.
- `Observe` returns `ObservedRecords`, which is a vector of `Entry` only.
- `LookupStash` returns the same identifier-less record set.

The future guardian must say "this proposal conflicts with these existing
records." The future auditor must propose "retire these source records." Both
need identifiers from ordinary reads.

Recommended contract change:

- introduce `RecordSnapshot { RecordIdentifier Entry }`;
- have a new observation reply return `RecordSnapshots`;
- keep identifier-less `Records` only if there is a specific consumer that
  benefits from it.

Pre-production compatibility should not block this. If the current shape is
wrong for the actual domain, replace it.

### 3. "State has no lineage" is right for the live surface, wrong as an audit rule

The synthesis says supersession/correction events evaporate. That is clean as a
semantic model of the live intent surface, but dangerous as an implementation
rule.

The live query surface should absolutely show only current forward arrows. But
the system still needs a durable event journal or archive for:

- explaining why a record disappeared;
- reversing a bad supersede;
- reproducing an auditor decision;
- debugging guardian false positives or false negatives;
- proving which psyche confirmation authorized retirements.

This does not mean lineage belongs inside the `Entry` description. It means
lineage belongs outside the live state: an append-only operation/event log, or a
separate archive relation keyed by record identifiers. The current separate
archive database for removal candidates is already pointing in that direction.

Recommendation: preserve the design phrase "live state is pure forward arrows,"
but replace "events evaporate" with "events do not pollute live intent; they are
durably journaled outside the live query surface."

### 4. The guardian verdict needs a typed refusal surface, not just yes/no prose

The synthesis says the guardian verdict is binary: yes or no, with reason and
references. As a safety principle, yes/no is good: the guardian must not
silently rewrite or suppress intent. As a contract, it is underspecified.

The caller needs to know what kind of no happened:

- duplicate;
- contradiction;
- compound record;
- non-intent/task state;
- unclear privacy;
- unclear topic;
- retrieval incomplete / guardian cannot decide.

Those do not give the guardian resolution authority. They give the proposing
agent the information needed to revise or ask the psyche. A single free-text
reason will be hard to test and hard to automate.

Recommendation: model a `GuardianVerdict` or `CaptureVerdict` enum with a
structured rejection reason and record references. Keep the final admission
choice binary, but make refusal typed.

### 5. Park-vs-block is not an implementation detail; it changes the user contract

The synthesis leans toward "park": the daemon shelves a proposal as pending,
then a guardian agent later admits or drops it. That is coherent, but it is not
the same behavior as a blocking capture gate.

If `Record` replies "pending," then capture did not succeed. Every caller must
understand a new lifecycle:

- proposed;
- pending guardian review;
- admitted;
- rejected;
- supersede-required.

If `Record` blocks until the guardian answers, callers keep the simpler
accepted/rejected lifecycle, but daemon responsiveness and LLM dependency become
hard operational constraints.

Recommendation: decide the lifecycle before coding. My operator lean is park,
but only if the schema makes pending status explicit and subscriptions announce
the later admit/reject result. Do not call a pending proposal "recorded."

### 6. Closed topics need a migration artifact, not just a policy

Closed broad topics are the right direction. The implementation cannot be only
"agents should use fewer topics."

The migration needs a typed topic catalog and a mapping pass:

- canonical topic declarations;
- aliases from old free-text topic strings to canonical topics;
- rejected/split/merged topic decisions;
- a tool that rewrites or reclassifies existing records in batches;
- tests proving an unknown topic is rejected or enters the enlargement process.

This also interacts with keywords. If `schema-language` collapses into topic
`schema` plus keyword `schema language`, that mapping should be explicit and
inspectable.

### 7. Asterisk keywords are acceptable as authoring sugar, but weak as the only index

The asterisk-emphasis idea is attractive because it makes descriptions readable
and cheap for agents to author. It is probably safe at the NOTA layer: inside a
bracket string, `*` is ordinary text.

The risk is treating markup inside prose as the only structured keyword source.
It creates several edge cases:

- editing prose changes query indexes;
- missed emphasis silently weakens retrieval;
- repeated terms can become noise;
- multi-word phrase matching needs stable normalization;
- literal asterisks in descriptions need an escape or convention.

Recommendation: allow asterisk emphasis as authoring syntax, then normalize it
into a derived keyword index with clear rules. It does not have to become a
stored `Entry` field immediately, but the indexer should be deterministic and
tested from bracket-string descriptions.

### 8. Kind reduction needs a migration decision for existing `Correction` and `Clarification`

Removing `Correction` from live state is conceptually right if corrections are
events. `Clarification` is less obvious. Many clarification records are probably
forward arrows wearing a conversational label; others may be discussion residue.

This should not be decided only at the enum-design level. The existing record
set needs a migration pass:

- `Correction` records become supersede/archive events or are folded into the
  canonical forward record they point to.
- `Clarification` records are either rewritten as `Decision` / `Principle` /
  `Constraint`, or the kind survives with a precise forward-only definition.

Until that migration is specified, shrinking `Kind` is not production-ready.

### 9. The daemon/agent boundary needs a concrete transport story

The synthesis says the daemon is the gate and an agent is the brain. That is the
right safety shape if the daemon remains a typed store/router and does not
perform LLM judgment.

But the actual triad rule still matters:

- daemons accept binary startup;
- daemons do not parse NOTA;
- text/NOTA belongs at the CLI/client/tool edge;
- agent work must be represented as typed signal messages or external operator
  workflow, not an ad hoc daemon side channel.

Recommendation: make guardian review an explicit signal surface. The daemon can
own a pending-proposal table and subscription stream; guardian agents consume
typed pending proposals and return typed verdicts. That keeps the daemon dumb
without making the gate imaginary.

## Suggested Build Order

1. Upgrade the read/query contract: magnitude selector, identifier-bearing
   observations, deterministic ordering, tombstone visibility semantics.
2. Fix `CollectRemovalCandidates` so it can safely target only removal
   candidates.
3. Add a durable event/archive journal for suppressions and guardian/auditor
   actions, outside the live intent query surface.
4. Define the capture lifecycle: proposed/pending/admitted/rejected/supersede
   required.
5. Add the guardian verdict schema with typed rejection reasons and referenced
   record snapshots.
6. Add the topic catalog plus old-topic mapping mechanism.
7. Add keyword extraction/indexing from bracket-string descriptions.
8. Migrate `Kind`, starting with `Correction`, then decide `Clarification`
   after inspecting actual records.
9. Only then wire the guardian agent flow.

## Net Feedback

The synthesis should stay. It captures the right philosophical move: Spirit
should query as rest, not as accumulated motion.

The part that clearly needs attention is turning the philosophy into contracts.
The most urgent correction is to stop treating the guardian as the next single
thing to build. The first production chunk is the query/read/collection contract
that makes a guardian and auditor possible without out-of-band database
inspection.
