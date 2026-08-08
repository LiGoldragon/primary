# 57.3 — Overview: Spirit engine variant + collect + defaults

Kind: psyche
Topics: spirit, variants, collect, defaults, overview
Date: 2026-06-03

## Intent anchors

The four directions today that ground this meta-report:

[Spirit gains an explicit CollectRemovalCandidates operation as a
Signal root. It collects all records currently at Zero certainty
(the removal-candidate marker per the existing supersession
protocol) and emits their summary form to a configurable output
target. Separates the discovery / extraction concern from the
destruction concern in Remove — gives agents a discrete step to
archive or inspect candidates before any irreversible action.]
(Decision High, today)

[Operations that extract or emit content from Spirit accept a
customizable output-target enum as the final field in the request
shape. Variants include Stdout, Stderr, and File with a path
payload. Not an error channel — Stderr is one option among normal
outputs. Keeps the wire interface uniform across extraction
operations.] (Decision High, today)

[Spirit defines a small-record data type carrying the core
load-bearing fields — identifier, topics, kind, description
summary, magnitude, daemon-stamped date and time. The variant-
ladder short forms and CollectRemovalCandidates emit the small
record; archiving and downstream tools consume it. Reduces wire
weight; matches the natural reading shape an agent or human
wants.] (Decision High, today)

[Spirit gains a RecordDefault short-form recording operation
taking only fields agents commonly customize — topics, kind,
description, magnitude — with defaults injected for the rest
(privacy at Zero per the dev-mode public-repo grounding,
daemon-stamped date and time, plus any other rarely-customized
field). Record remains the canonical full-fidelity operation;
RecordDefault is the daily-use shortcut.] (Decision High, today)

These sit downstream of [Spirit operations should support a
simpler-to-more-complex variant ladder — short forms with summary
defaults for normal operations, complex forms with full metadata
for custom operations.] (Decision High, today, the parent
direction).

## What the two sub-agents found

The headline finding: the production engine is FURTHER ALONG than
either the psyche directive or the operator vision presumed.
`CollectRemovalCandidates` already exists in source at
`/git/github.com/LiGoldragon/persona-spirit/src/store.rs:126-144`
in a combined archive-then-retract shape; the existing
`CertaintySelection::removal_candidates()` constructor at
`/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs:556-559`
already returns `Self::Exact(Magnitude::Zero)` — the filter is
hooked, not contract-only. The operator vision missed this; the
designer psyche-analysis caught it by reading deeper into
`persona-spirit/src/store.rs`. A parallel system-operator report
at
`/home/li/primary/reports/system-operator/189-production-spirit-collect-removal-candidates-2026-06-03/`
independently ratifies the combined-handler design — three
perspectives converging on the same source-shape.

This reshapes the slice. The operator vision framed today's
work as "build four new operations". The designer psyche-analysis
reframes it more honestly: "reshape one existing operation +
add two new pieces (`SmallRecord` and `RecordDefault`) + land the
variant-ladder shortcuts the corpus mining surfaced". The slice
is substantially smaller than the vision suggested.

The deployed `spirit` binary (resolves to `spirit-v0.3.0`) does
NOT yet route `CollectRemovalCandidates` — the designer's
verification this session showed `unknown request head:
CollectRemovalCandidates` from the live binary. Same
source-ahead-of-deploy pattern as the privacy thread from
`/home/li/primary/reports/system-designer/56-psyche-meta-report-spirit-recent-work-2026-06-03.md`.
The slot infrastructure from
`/home/li/primary/reports/system-designer/53-spirit-next-production-parity-2026-06-02/5-overview.md`
remains the unblock.

## The two sub-reports, in one paragraph each

`/home/li/primary/reports/system-designer/57-spirit-engine-variant-and-collect-vision-2026-06-03/1-operator-vision.md`
walks the four-operation vision in operator analytic style with
schema declarations, handler shapes, and a seven-phase
sequencing. It anchors at the existing `Entry::open` constructor
at `signal-persona-spirit/src/lib.rs:372-387` as the in-process
twin of `RecordDefault` — `Entry::open` already bakes
`privacy: Magnitude::Zero` into the default, the source-level
manifestation of [The workspace context that grounds Spirit
1449's most-public default is development-mode for public
repositories — collaborative work on shared open-source software
where most intent captures inform future agents and
contributors.] (Clarification High, today). The operator
vision's seven phases are: small-record first as the type
dependency, then `OutputTarget`, then `CollectRemovalCandidates`,
then `RecordDefault`, then Tier 1 variant-ladder short reads,
then witness tests, then CLI surface (which actually requires
no hand-written changes since the bins are one-line
`signal_cli!` macro invocations).

`/home/li/primary/reports/system-designer/57-spirit-engine-variant-and-collect-vision-2026-06-03/2-designer-psyche-analysis.md`
verifies the operator vision against current source and corrects
several under-credits — `RemovalCandidateCollection::inline()` and
`::file(path)` constructors already exist, an `archived_records`
reply field exists, a four-variant `SkippedRemovalCandidate`
reason enum exists. Line numbers shifted slightly from the
operator vision's brief (`CertaintySelection::removal_candidates()`
is at 556-559 not 622-633) but the substance was there at the
equivalent locations. The analysis lays out nine open decisions
for the psyche in plain-terms style, with the combined-or-split
question for `CollectRemovalCandidates` as the central one.

## The pivotal open decision

The directive clause [Separates the discovery / extraction
concern from the destruction concern in Remove] reads two ways
when matched against the existing source.

Reading A — pure extract. `CollectRemovalCandidates` strictly
collects, never retracts. A subsequent multi-Remove flow
destroys. This is the literal reading of "separates discovery
from destruction" if "destruction" means any retraction.
Estimated work: ~250 lines, significant rework of the existing
combined handler.

Reading B — bulk collect distinct from per-record Remove. The
existing combined handler already separates BULK archive-then-
retract (called once for the whole removal candidate set) from
per-record Remove (called individually for specific records).
Both achieve a distinction; the existing one is in the bulk
direction. Estimated work: ~80 lines this cycle (reshape the
contract field names, expose the existing handler through the
new wire shape, add the missing `SmallRecord` and
`RecordDefault`).

The system-operator parallel report at
`/home/li/primary/reports/system-operator/189-production-spirit-collect-removal-candidates-2026-06-03/`
independently lands on Reading B. Cross-lane triple-convergence
(designer 57 + operator 189 + the existing source) on the
combined-handler design is the correctness signal the workspace's
three-way-convergence discipline names.

The recommendation surfaced by the designer analysis: Reading B,
because the existing source is already shipped and tested and
matches the operator's parallel ratification. Reading A would
discard working code to chase a literal interpretation of one
clause. If the psyche prefers Reading A on first-principles
grounds — that destruction and extraction should ALWAYS be
separate operations — the operator vision can be re-briefed.

## The other open decisions, in plain terms

The full nine open decisions live in
`/home/li/primary/reports/system-designer/57-spirit-engine-variant-and-collect-vision-2026-06-03/2-designer-psyche-analysis.md`
§4. The most important after the combined-or-split question:

- **File-target failure mode.** When the `OutputTarget::File`
  variant points at a path that does not exist, does the daemon
  create it or fail-fast? The psyche needs to choose. Create-if-
  absent is the conventional Unix pipe behavior; fail-fast is the
  Nix-style "be explicit about paths" preference. The workspace
  has not settled this style.

- **Small-record field list — minimum or generous.** The
  directive named "identifier, topics, kind, description summary,
  magnitude, daemon-stamped date and time". Is that the complete
  field list, or does the small record also include the privacy
  field (so archiving can carry the privacy classification with
  the record)? Carrying privacy on the small record means
  consumers can filter without re-querying.

- **RecordDefault override semantics.** Can a caller pass an
  explicit privacy value when calling `RecordDefault`, or is
  privacy strictly defaulted? Override-allowed gives flexibility
  but undermines the "default-injected for rare-customized
  fields" framing. Strict-default keeps the contract clean but
  forces fallback to the canonical `Record` for any record that
  wants non-default privacy.

- **Source-first vs deploy-first sequencing.** The privacy field
  is source-implemented but not deployed (from
  `/home/li/primary/reports/system-designer/56-psyche-meta-report-spirit-recent-work-2026-06-03.md`).
  `CollectRemovalCandidates` is in the same state. Does this
  slice land alongside the deployment cutover (the one-line
  flake-input redirect from
  `/home/li/primary/reports/system-designer/53-spirit-next-production-parity-2026-06-02/5-overview.md`),
  or does it ship in a follow-on after the cutover stabilizes?

The remaining decisions cover the small-record's relationship
to the `DatabaseMarker` provenance envelope (whether the small
record inherits the provenance footer), the wire encoding of the
`OutputTarget::File` path (whether file paths get a typed
wrapping or stay as raw strings), the variant-ladder tier-1
naming question (whether `(Recent)` zero-arg or
`(Recent <N>)` one-arg is the canonical Tier-1), the privacy
filter default behavior on the new variant operations, and the
witness-test pattern for the new operations (whether each gets a
standalone test in `boundary.rs` or rides on existing test
patterns).

## Path to ship, narrated

The slice composes cleanly with the larger picture. The operator
vision's seven phases reshape under the combined-handler
recognition: phases 1-3 collapse to "expose the existing
combined-handler under the new wire-shape name + add the missing
`SmallRecord` type + add the `OutputTarget` enum"; phases 4-5
become "add `RecordDefault` as the one-arm addition to
`WorkingOperation` and the variant-ladder tier-1 short reads"; phase
6 is "extend the test suite"; phase 7 is no-op (CLI bins are
already macro-driven). Net effort estimate from the designer
analysis: substantially under the half-day implied by the seven-
phase framing, possibly closer to four hours of operator-shape
work for the source changes.

The deployment dimension stays the bottleneck. Whatever this
slice lands, it ships through the same cutover path that the
privacy thread waits on — the `persona-spirit-next.url` flake
input in `/git/github.com/LiGoldragon/CriomOS-home/` that today
tracks `github:LiGoldragon/persona-spirit?ref=main` and needs the
redirect (or a version bump) plus a home-manager activation
snippet for the rkyv binary configuration. The slot
infrastructure is wired; the target is the gap. This slice
landing in source is half the story; the cutover is the other
half, and it has been half-the-story for two days already.

## What this means for the next step

The clean next move depends on which Reading the psyche picks for
the combined-or-split question. If Reading B (the recommendation
from both the designer analysis and the parallel operator 189
report), the next step is a small designer-shape worktree on
`signal-persona-spirit` reshaping the wire contract to expose the
existing combined handler under the directed name plus the two
new pieces, plus the variant-ladder tier-1 shortcuts. The
operator pickup is a smaller, cleaner integration than the
seven-phase framing suggested.

If Reading A, the existing combined handler gets dismantled and
the work is meaningfully larger; the operator vision's seven-
phase framing applies more literally, and the slice grows from
a four-hour reshape into a multi-day rework. The system-operator
parallel report would also need re-framing.

The other open decisions can land alongside whichever Reading
the psyche picks; they're parameters, not architectural pivots.

## See also

- `/home/li/primary/reports/system-designer/57-spirit-engine-variant-and-collect-vision-2026-06-03/0-frame-and-method.md` — the frame for this meta-report
- `/home/li/primary/reports/system-designer/57-spirit-engine-variant-and-collect-vision-2026-06-03/1-operator-vision.md` — the operator vision sub-agent's report
- `/home/li/primary/reports/system-designer/57-spirit-engine-variant-and-collect-vision-2026-06-03/2-designer-psyche-analysis.md` — the designer psyche-analysis sub-agent's report
- `/home/li/primary/reports/system-operator/189-production-spirit-collect-removal-candidates-2026-06-03/` — the parallel operator-lane report that independently ratifies the combined-handler design
- `/home/li/primary/reports/system-designer/56-psyche-meta-report-spirit-recent-work-2026-06-03.md` — yesterday's psyche-style meta-report; the discipline this directory continues
- `/home/li/primary/reports/system-designer/55-spirit-variant-ladder-design-research-2026-06-02.md` — the variant-ladder research with corpus mining
- `/home/li/primary/reports/system-designer/53-spirit-next-production-parity-2026-06-02/5-overview.md` — the production-parity audit and the deployment-chain gap that remains the slice's external dependency
- Intent anchors as captured Spirit records: 1474, 1547-1550 today, plus the prior thread at 1463 (Magnitude-on-privacy) and 1449 (default-public) and 1480 (atomic topic naming)
