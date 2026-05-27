# 351 — Intent file tour and relocation

*Designer-lane subagent dispatch 2026-05-26 per psyche records
717-719. Walks workspace + per-repo intent files, relocates
misplaced content to its right scope, and flags suspected
hallucinations for psyche review.*

## Frame (per psyche 2026-05-26 records 717-719)

- **Record 717 (Principle).** Intent lives in the file that owns its
  scope. Primary workspace `INTENT.md` is for intent ABOUT the
  primary workspace itself. Each per-repo `INTENT.md` is for intent
  ABOUT that repo. Misplaced intent (e.g. schema-syntax intent
  leaking into primary workspace `INTENT.md`) is a discipline error.
- **Record 718 (Principle).** Agents inferring to close the loop
  when design is incomplete produces fake intent that accumulates
  as hallucinated records. Don't infer; ask the psyche.
- **Record 719 (Decision).** Intent log audit policy — agents may
  FLAG suspected duplicates, misalignments, and hallucinated
  records for psyche review but never delete or supersede
  unilaterally. Same rule for intent FILE cleanup.

## Files walked

| File | Verdict |
|---|---|
| `/home/li/primary/INTENT.md` | Substantial relocation applied |
| `/home/li/primary/ESSENCE.md` | Stays as-is — all workspace-shape |
| `/home/li/primary/AGENTS.md` | Stays as-is — Hard Overrides are per-keystroke and universal |
| `/git/github.com/LiGoldragon/schema/INTENT.md` | Rewritten to receive relocated content + drop drift framing |
| `/git/github.com/LiGoldragon/persona-spirit/INTENT.md` | Walked; one drift section flagged for psyche review (Reading-actor + auto-tap) |
| `/git/github.com/LiGoldragon/signal-persona-spirit/INTENT.md` | Right-scope; no change |
| `/git/github.com/LiGoldragon/nota/INTENT.md` | Right-scope; receives workspace embedding-safety pointer-back |
| `/git/github.com/LiGoldragon/nota-codec/INTENT.md` | Right-scope; no change |
| `/git/github.com/LiGoldragon/signal-frame/INTENT.md` | **Does not exist on main.** Stale content on unmerged branch — flagged for psyche review |
| `/git/github.com/LiGoldragon/owner-signal-persona-spirit/INTENT.md` | Does not exist; flagged as gap |

Skill files scanned for repo-specificity: `nota-design.md`,
`nota-schema-docs.md`, `component-triad.md`, `architectural-truth-
tests.md`, `naming.md`, `architecture-editor.md`. All are
cross-cutting agent disciplines applying workspace-wide. No
relocations from skills triggered.

## Relocations applied

| Source | Destination | Content |
|---|---|---|
| primary `INTENT.md` §"The schema-driven stack" (schema-language detail) | `repos/schema/INTENT.md` §"The namespace is a key-value map of user-defined types" + §"Language shape — positional, no labels" | Namespace-as-key-value-map; `EnumName (Variant1 Variant2 …)` enum syntax; `StructName [FieldType1 FieldType2 …]` struct syntax; universal-Unknown-is-behind-the-scenes-not-authored; canonical `spirit.schema` pointer |
| primary `INTENT.md` §"Spirit deploys side-by-side; cutover is an alias change" | already in `repos/persona-spirit/INTENT.md` §"Deployment — next, main, previous side-by-side" | Side-by-side state directory; `spirit-vX.Y.Z` wrapper + `spirit-next` slot + unsuffixed `spirit` symlink; alias-change-not-destructive-replace; v0.2.0 validation; "Migrate live Spirit to v0.2 now" — all already present in persona-spirit/INTENT.md, so primary section deleted outright |
| primary `INTENT.md` §"NOTA is the universal embedding-safe payload" (language design + emitter discipline) | already in `repos/nota/INTENT.md` §"Strings come exclusively from bracket forms" + `repos/nota-codec/INTENT.md` §"Encoder is the canonical-emission engine" | Bracket-form rules; encoder structural-cannot-emit-quote; legacy-quote-acceptance-as-migration-only — compressed primary section to the workspace-shape embedding-safety statement + pointers |
| primary `INTENT.md` §"Persona-spirit is the apex; concept designer is the entry" (persona-spirit architecture) | already in `repos/persona-spirit/INTENT.md` §"What persona-spirit is" + ESSENCE.md §"Persona is meta-AI; spirit animates" | The apex/owns-mind/spawned-last/Bead `primary-ojxq` framing — compressed primary section to a one-paragraph concept-designer entry + pointer-back |

Schema-repo INTENT.md was also rewritten to:
- Drop the drift framing in the old item 2 ("the SIX fixed positional
  fields: imports, ordinary header, owner header, sema header,
  namespace, features") — per record 715, no Features section.
- Drop item 5's "feature-carried upgrade annotations" framing — same
  retraction.
- Drop item 6's framing of `AssembledSchema` as consumed by "storage
  descriptors and version projection" — narrowed to short-header
  generation, code emission, and version projection (storage
  descriptors are the drift surface).

## Per-repo branches pushed

| Repo | Branch | Commit | Status |
|---|---|---|---|
| `schema` | `designer-intent-cleanup-2026-05-26` | `1b5c8037` | Pushed to origin; awaiting operator integration |
| `persona-spirit` | — | — | No edits needed; one section flagged for psyche review (see below) |
| `signal-persona-spirit` | — | — | No edits; right-scope already |
| `nota` | — | — | No edits; right-scope already |
| `nota-codec` | — | — | No edits; right-scope already |
| `signal-frame` | — | — | No edits applied; flagged for psyche review (see below) |

Primary workspace `INTENT.md` edits land directly on `main` (the
workspace is not a repo with feature branches; designer edits land
on the workspace's own main per existing practice).

## Flagged for psyche review

Per record 719, the following content is flagged rather than deleted
because uncertainty exists about whether it's real psyche intent or
agent inference closing the loop on incomplete design.

### Flag 1 — persona-spirit/INTENT.md §"Reading-actor + auto-tap"

**File:** `/git/github.com/LiGoldragon/persona-spirit/INTENT.md`
lines 207-215.

**Excerpt:** *"The daemon's response dispatch is itself an actor —
the reading actor — with its own schema. Its action vocabulary is
dispatch-by-response-type. Its fan-out targets always include a
`(Tap LogSinkSet WriteEntry)` row; the auto-tap to a logging
facility is declared by the schema, not enforced by runtime
convention. Every response is captured; nothing is invisible. Per
record 696 §5."*

**Reasoning:** This describes fan-out targets as authored schema
content, which is the exact drift the psyche retracted in records
713-715 (Maximum certainty, 2026-05-26). Schemas define data types
only; fan-out is runtime logic, not data. The auto-tap concept may
still be a real persona-spirit design feature, but its expression as
*"declared by the schema"* is the retracted direction. Needs psyche
review: (a) is auto-tap a real intended persona-spirit feature, or
agent-introduced? (b) if real, where does it actually live — actor
runtime configuration, supervisor wiring, hand-written Rust, or
some non-schema authored surface?

### Flag 2 — persona-spirit/INTENT.md §"Database upgrades are auto-migration on load"

**File:** `/git/github.com/LiGoldragon/persona-spirit/INTENT.md`
lines 173-205.

**Excerpt:** *"A schema-diff machine identifies what types are
added, dropped, renamed, structurally changed. The developer writes
hand-written Rust bridge code per version-boundary — the `From`-impl
per type that moved, in a `mod previous` / `mod next` pair. … A
version-marker stored alongside the database tells the daemon which
schema the persisted data was written under. … Per record 696."*

**Reasoning:** The section is heavily synthesised across what looks
like multiple records (672 mentions the NEXT/MAIN/PREVIOUS
vocabulary; 696 was the records-696-grouped batch). Specific claims
about the schema-diff machine, the `From`-impl per type, the
`mod previous` / `mod next` Rust shape, the version-marker store —
these may be one psyche statement worth of intent or agent
elaboration filling in a sketch. The auto-migration arc IS real
psyche intent at the high level. The detail level may be agent
inference. Needs psyche review for whether the implementation
detail captures intent at the right granularity.

### Flag 3 — signal-frame INTENT.md (stale unmerged branch)

**File:** `/git/github.com/LiGoldragon/signal-frame/INTENT.md` does
NOT exist on `main`; content exists only on the unmerged branch
`designer-sweep-349-intent-2026-05-25` (created by the /349 sweep).

**Excerpt (from the stale branch):** §"The composer's responsibility
— authored-feature consumption" — *"When a schema declares
`Feature::EffectTable`, the composer emits `AuthoredEffect` /
`AuthoredFanOutOutput` / `AuthoredFanOut` / `AuthoredEffectTable`
from the AUTHORED rows the schema carries. … Three emission
functions handle the authored-feature surface: `authored_effect_
items()` … `storage_descriptor_items()` …"*

**Reasoning:** The /349 sweep authored this INTENT.md while the
schema-features-drift direction was still in play. Per records
713-715, the entire framing of "authored-feature consumption" as a
composer responsibility is drift. The non-drift content (composer
walks `AssembledSchema` + emits `pub mod` TokenStream; extensible-
header pattern with 8-byte ShortHeader prefix-preservation;
`emit_schema!` proc-macro entry point; record-field-disambiguation)
may be real intent worth preserving. Needs psyche review: should a
signal-frame INTENT.md exist at all? If yes, what content survives
post-/350 retraction? Not landing the rewrite without psyche
direction.

### Flag 4 — owner-signal-persona-spirit/INTENT.md missing

**File:** `/git/github.com/LiGoldragon/owner-signal-persona-spirit/INTENT.md`
does not exist.

**Reasoning:** The repo exists and has an `ARCHITECTURE.md` plus
the owner-channel `.schema` file, but no INTENT.md. Per record 668
(*"when the psyche describes a major part of the system, that
description IS a warrant to create a schema for that part"*) and
the channel-per-contract discipline, the owner channel is a
distinct contract from the ordinary channel. The decision of
whether owner-signal-persona-spirit warrants its own INTENT.md
depends on whether the psyche treats it as a distinct repo-scope
intent surface or as an addendum to persona-spirit. Worth a psyche
prompt; not creating one unilaterally.

### Flag 5 — workspace INTENT.md §"Possible additional role — auditor"

**File:** `/home/li/primary/INTENT.md` §"Possible additional role —
auditor (Medium certainty)" + the parallel §"Possible additional
role — auditor (Medium certainty)" in `AGENTS.md`.

**Excerpt:** The workspace INTENT.md describes auditor open
questions — authority class, lane mechanism, audit-findings
substrate — with four candidate substrates listed (reports under
`reports/auditor/`, comments on beads, Spirit records from an
auditor agent identity, or PR-style review on jj commits).

**Reasoning:** Records 234 + 235 (2026-05-22, Medium) name the
auditor role + DeepSeek + automation. The detailed substrate
options listed in the INTENT.md walk-through (the four
candidates) look like agent elaboration extending beyond the
psyche-stated content. This is borderline — the section labels
itself "proposed-not-decided" and carries the uncertainty
explicitly. Worth a psyche review on whether to compress to just
the role + DeepSeek + automation, or whether the substrate
options are real shape-of-the-question content.

## Line counts before / after

| File | Before | After | Delta |
|---|---|---|---|
| `/home/li/primary/INTENT.md` | 416 | 345 | −71 |
| `/git/github.com/LiGoldragon/schema/INTENT.md` | 37 | 101 | +64 |
| `/home/li/primary/ESSENCE.md` | 232 | 232 | 0 |
| `/home/li/primary/AGENTS.md` | 341 | 341 | 0 |
| `/git/github.com/LiGoldragon/persona-spirit/INTENT.md` | 298 | 298 | 0 |
| `/git/github.com/LiGoldragon/signal-persona-spirit/INTENT.md` | 136 | 136 | 0 |
| `/git/github.com/LiGoldragon/nota/INTENT.md` | 118 | 118 | 0 |
| `/git/github.com/LiGoldragon/nota-codec/INTENT.md` | 73 | 73 | 0 |
| **Total** | **1651** | **1644** | **−7** |

Net decrease: 7 lines. The headline reduction is modest because
moving content from primary to schema/ required expanding schema/
INTENT.md (formerly a tight 37-line bullet list) into a properly
shaped INTENT.md with intro framing, principles, and pointers. The
substantive win is that schema-language syntax now lives in the
right scope, NOT line count.

If the flagged drift sections (Flag 1, Flag 2) are confirmed as
agent inference by psyche review, additional line reductions will
follow (Flag 1 = ~9 lines in persona-spirit/INTENT.md; Flag 2 =
~30 lines or more depending on how much of the schema-diff
mechanism survives review).

## What stays / what moves

**Stays in primary INTENT.md (workspace-shape):**

- Intent layer architecture (the three surfaces — log, per-repo,
  ESSENCE — and supersession discipline).
- Guidance file taxonomy.
- Reports-vs-chat split.
- Skill-noise discipline.
- Role loosening + lane structure.
- Two-deploy-stacks discipline (cross-repo workspace shape).
- Worktree discipline (cross-repo workflow shape).
- Third-stable-branch deferral (workspace-wide branching policy).
- BEADS-transitional framing (workspace tooling).
- Workspace-truth-in-files (anti-harness-memory).
- NOTA universal-embedding-safety as a workspace-emitter principle.
- Nix store search anti-pattern.
- Persona-LLM-mediated workspace principle.
- Persona-components-ship-raw workspace principle.
- The schema-driven stack workspace framing (without language
  syntax).
- Concept designer + new-role-without-skill + auditor (workspace
  role taxonomy).

**Moved to repos:**

- Schema language syntax (namespace-as-map, enum/struct shapes,
  Universal-Unknown-is-behind-the-scenes) → `repos/schema/INTENT.md`.
- Persona-spirit deployment substrate (already there; primary
  duplicate removed).
- NOTA language design + codec emitter discipline (already there;
  primary duplicates compressed to a pointer).
- Persona-spirit apex architecture (already there; primary
  duplicate removed).

## References (Spirit records walked)

- Record 713 (Correction, 2026-05-26, Maximum) — Schema defines
  data types ONLY; no effects, fan-out, effect tables.
- Record 714 (Clarification, 2026-05-26, Maximum) — NOTA schema
  namespace is a key-value map.
- Record 715 (Correction, 2026-05-26, Maximum) — Subagent drift
  introduced a Features section; retract.
- Record 716 (Principle, 2026-05-26, Maximum) — Agent-authored
  content is not psyche-authorized design surface.
- Record 717 (Principle, 2026-05-26, Maximum) — Intent lives in the
  file that owns its scope.
- Record 718 (Principle, 2026-05-26, Maximum) — Agents inferring to
  close the loop produces fake intent.
- Record 719 (Decision, 2026-05-26, Maximum) — Audit policy: flag
  for psyche, don't delete unilaterally.

Plus historic load-bearing records for the canonical content:

- Record 698 (NOTA bracket-only strings) — referenced in nota
  INTENT.
- Record 705 (NOTA embedding-safety contract) — referenced in
  nota and nota-codec INTENT.
- Record 668 (Schemas warrant per channel) — referenced in
  persona-spirit and signal-persona-spirit INTENT.
- Record 672 (NEXT/MAIN/PREVIOUS vocabulary) — referenced in
  workspace INTENT and persona-spirit INTENT.
- Record 692 (Schema/signal/sema vocabulary) — referenced in
  workspace INTENT and persona-spirit INTENT.

## See also

- `reports/designer/349-context-maintenance-sweep-2026-05-25/` —
  the prior sweep this tour partially undoes (the /349 sweep was
  the source of misplaced schema-syntax content in primary
  INTENT.md).
- `/350` (schema-feature-drift retraction) retired in sweep /377;
  retraction substance landed in `INTENT.md` §"The schema-driven stack",
  per-repo `INTENT.md` files (schema, persona-spirit, signal-persona-spirit),
  and `reports/designer/341-schema-crystallizes-architecture-2026-05-25.md`
  STATUS-BANNER. The current tour follows up on that retraction.
- `skills/intent-manifestation.md` — the decision tree for where
  intent statements land.
- `skills/intent-maintenance.md` — sweep + supersession discipline.
