# Spirit Intent Redesign Second-Pass Feedback

Reviewed target: `reports/designer/578-intent-redesign-synthesis.md`

Current companion context:

- `reports/designer/577-intent-tool-state-and-the-real-flaw.md`
- `reports/designer/579-spirit-agglomeration-pass-2026-06-10.md`
- `/git/github.com/LiGoldragon/spirit/schema/signal.schema`
- `/git/github.com/LiGoldragon/spirit/src/store.rs`
- `/git/github.com/LiGoldragon/spirit/tests/collect_removal_candidates.rs`
- `/git/github.com/LiGoldragon/spirit/tests/process_boundary.rs`

This replaces the previous `352` content after designer folded the first-pass
operator feedback into `578`.

## Current Read

`578` is now strong enough to guide implementation. The major earlier gaps are
resolved inside the design:

- guardian refusals carry typed reasons and referenced `RecordSnapshot`s;
- `clarify` keeps the record identifier stable and journals prior wording;
- synchronous handoff fails closed when the harness is absent, malformed,
  timed out, or failed;
- retired arrows archive instead of being destroyed;
- the actual first build is identifier-bearing observation;
- weight has explicit duplicate-refusal mechanics;
- existing `Correction` and `Clarification` records get a one-time migration
  into forward arrows, operations, and events.

The remaining feedback is therefore narrower. I would not block on philosophy
now; I would block only on the schema vocabulary and the executable transport
shape before code lands.

## Remaining Attention Items

### 1. Settle the certainty / magnitude / weight axes before editing schema

The design now correctly adds dedicated `Weight`, but it still mixes three
nearby words:

- deployed/current source has `Entry.magnitude`;
- source query names that axis `CertaintySelection`;
- revised `578` says weight is separate from `magnitude`
  `(strength/importance)`;
- the de-bloat behavior treats zero on that axis as removal-candidate
  currentness.

Those are not all the same thing.

If the psyche wants **certainty and weight**, the clean implementation likely
needs:

- `Certainty`: currentness / confidence / live-vs-retired filtering;
- `Weight`: reaffirmation count / ranking force from repetition;
- no third vague `Magnitude` field in `Entry`, unless it has a separate
  explicit job.

If `Magnitude` survives as "importance," then Spirit would have three axes:
certainty, weight, and importance. That may be real, but it should be an
explicit decision, not an inherited name from the old schema.

Operator recommendation: rename the stored `Entry.magnitude` axis to
`Certainty` during the breaking schema pass, add `Weight`, and retire
`Magnitude` from `Entry` unless a third importance axis is deliberately chosen.

### 2. The event/archive distinction needs one sentence of precision

`578` still says stream events "evaporate," while also saying retired arrows and
clarify prior wording are archived/journaled. This is probably intended, but the
wording can still mislead implementation.

Recommended precision:

Subscription events are ephemeral delivery notifications; operation history and
retired/prior record bodies are durable archive/journal data outside the live
intent query surface.

That keeps "state is rest, stream is motion" without losing auditability.

### 3. The harness transport remains the first implementation design task after snapshots

`578` now acknowledges that the exact typed request/reply transport is open.
That is fine as a design status, but it means the guardian itself is not the
next code slice after snapshots/category/weight unless this transport is
specified first.

Implementation needs a small concrete contract:

- harness endpoint configuration;
- binary startup/config implications;
- signal type carrying proposal bundle plus retrieved snapshots;
- verdict reply type;
- timeout/error mapping;
- tests proving fail-closed behavior.

This can be narrow, but it should exist before any LLM judgment loop is wired.

### 4. Category migration should precede guardian prompt work

The category plan is now good: closed broad categories, agent proposal, psyche
approval, enlargement gate. The implementation order should keep it ahead of
guardian prompts.

Reason: if guardian retrieval starts while the live field is still free-text
`Topic`, it will bake old recall failure into the new gate. The first usable
guardian bundle should already be `category + keyword + full-text`, not old
topic-only matching.

### 5. Use exported fixture files for migration tests

The kind migration is now clearly described. The test design should use exported
record fixtures or schema files checked into the repo, not inline Rust strings.

The fixture should cover at least:

- an old `Correction` folded into a forward record plus correction event/archive;
- an old `Clarification` converted into clarify history or a forward record;
- a removal-candidate record hidden from default query but visible to explicit
  candidate query;
- an old narrow topic becoming broad category plus keyword.

## Suggested Implementation Gate

Ready to implement first substrate slice:

1. identifier-bearing `RecordSnapshot` observations;
2. schema vocabulary cleanup for `Certainty` and `Weight`;
3. category catalog and migration fixtures;
4. durable operation journal/archive model;
5. typed harness transport;
6. guardian verdict integration.

Not ready to implement as "the guardian" until those substrate pieces are
concrete.

## Net Feedback

The report is now substantially aligned with production needs. My only strong
pushback is vocabulary: do not let `magnitude`, `certainty`, `importance`, and
`weight` blur into one another during the schema rewrite.

Once that axis naming is settled, the next operator work should be contract
substrate, not model prompts.
