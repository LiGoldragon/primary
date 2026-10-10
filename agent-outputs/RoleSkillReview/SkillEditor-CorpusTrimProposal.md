# SkillEditor — Corpus Trim Proposal

Proposal-only review of the skill/module corpus for wordiness, cross-skill
redundancy, and staleness. Nothing is applied. Every item is a recommendation
for a later skill-editor pass; the psyche-decision and assignability flags are
called out per item.

## Task and scope

Review the generated-skill source corpus for (a) within-skill wordiness, (b)
cross-skill redundancy/overlap (merge / archive / eliminate / designate a
canonical owner), and (c) staleness (superseded, broken, or unused). For each
proposal: the skill(s), the evidence (line counts and quoted overlap), the
specific action, a confidence, and any psyche-decision. The separate per-role
skill-assignment question is out of scope; merges/eliminations that would change
what is assignable to roles are flagged.

## Sources consulted

- Generator source repo `/git/github.com/LiGoldragon/skills`:
  `README.md`, `AGENTS.md`, `skills.md`, `manifests/active-outputs.nota`,
  `manifests/module-dependencies.nota`, `skills-check.nota`,
  `skills-generate.nota`.
- `skills/skills.nota` (primary discovery index) and the `skill-editor` SKILL.
- Full reads of the flagged clusters: reporting, report-naming,
  context-maintenance, context-maintenance-deep, context-handover,
  workspace-update-report, when-to-use-helpers, helper-context-transfer,
  engine-analysis, engine-report, main-next, main-feature-integration,
  feature-development, double-implementation-strategy, intent-log, spirit-cli,
  intent-maintenance, intent-manifestation, intent-clarification, repo-intent,
  intent-led-orchestration, autonomous-agent, session-lanes, rust-discipline,
  rust-methods, abstractions, agent-output-protocol, role-skill-editor.
- Heading-level structural scans of prose, naming, mermaid, nix-discipline,
  beads, testing, architecture-editor, secrets, stt-interpreter,
  rust-storage-and-wire.
- Two read-only sub-agents (their file dumps kept out of this context):
  heavy-architecture cluster (component-triad, contract-repo, actor-systems,
  kameo) and NOTA/language cluster (nota-design, nota-comments, nota-schema-docs,
  structural-forms, language-design). Their line-cited findings are folded in
  below and independently consistent with my own reads of the cross-references.

## Corpus shape (facts)

- 66 emitted skill modules + 1 shared non-emitted module (`agent-output-protocol`)
  + 10 role modules = 77 module-dependency records vs 76 active outputs (66 Skill
  + 10 Role). The count delta is exactly `agent-output-protocol` (included by
  roles, never emitted as its own output). No orphan or missing module.
- Total skill-module body: ~15,534 lines. Heaviest: component-triad 1160,
  reporting 851, kameo 790, actor-systems 624, prose 585, contract-repo 571.
- Roles are well-factored: every role source is 37-54 lines of role prose and
  shares procedure through the `agent-output-protocol` module rather than
  duplicating it. No role-side redundancy found; do not touch the role layer for
  dedup.

## Verification results

- **Manifest paths all resolve.** Every `modules/<name>/full.md` and
  `roles/<name>/full.md` in `module-dependencies.nota` exists.
- **No real duplicate headings.** A naive heading scan flags "See also" in
  `skill-editor` and `architecture-editor`, and four "headings" in
  `nota-comments` — all false positives (headings inside fenced code blocks: the
  skill-editor template example and `#`-prefixed Nix/markdown samples). The
  generator's duplicate-heading gate evidently ignores fences; no generation
  failure exists.
- **Source modules carry no harness frontmatter** (confirmed on the modules
  read).

## Section A — cross-skill redundancy (ranked)

### A1. The drain / three-fate / retired-lane-registry / fresh-context-pickup complex is duplicated across 5+ skills (HIGH confidence, highest value)

This is the single largest cross-skill redundancy. Four near-verbatim concept
blocks are copy-pasted across the report/lane skills:

- **Three-fate disposition (intent / work / abandon)** appears in `reporting`
  (L637-642 table), `context-maintenance` (L37-41 table), `session-lanes`
  (L116-122), `context-maintenance-deep` (L39-40).
- **Retired-lane registry paragraph** (lane name, discipline, git revision
  range, transcript pointer, drain date, one-line decision → `protocols/retired-lanes.md`)
  appears near-verbatim in `reporting` (L656-663), `context-maintenance-deep`
  (L57), `session-lanes` (L130-136), and summarized in `report-naming` (L46).
- **"Fresh-context pickup point" rule** appears in `reporting` (L36-42),
  `report-naming` (L5-7), `session-lanes` (L92-99), and is referenced in
  `intent-led-orchestration` and `bead-weaver` (the latter two reference it
  appropriately, not duplicate it).

Action: designate **`context-maintenance` as the canonical owner** of the
three-fate/drain/lane-retirement material (its index description already is "run
an everyday single-lane sweep ... migrating substance to permanent homes"), and
reduce the copies in `reporting`, `session-lanes`, `report-naming`, and
`context-maintenance-deep` to one-line pointers. Designate **`report-naming` as
the canonical owner of the "fresh-context pickup point" statement** (or `reporting`)
and point the others at it. Estimated reclaim: ~40-60 lines from `reporting`,
~30 from `session-lanes`, smaller from the rest.

Psyche-decision: none required (these are internal boundary calls the index
already implies); but record the canonical-owner pick so future edits do not
re-spread the block. Assignability: no skill is added or removed, so role
assignment is unaffected.

### A2. reporting.md (851) has absorbed report-naming's and context-maintenance's entire scopes (HIGH confidence)

`reporting` is the heaviest Keystroke skill and re-teaches two dedicated skills:

- **report-naming scope** — `reporting` §"Where reports live" (L219-234),
  §"Filename convention" (L275-306), §"Numbering" (L308-335), §"Topic
  agglomeration" (L337-345), §"Iterating — v2/v3" (L347-371), §"Versioning
  committed reports" (L575-597), §"Within-session supersession" (L599-629) are
  the same material `report-naming` (51 lines) exists to own. `report-naming`
  even self-describes as "Companion to `skills/reporting.md`."
- **context-maintenance scope** — `reporting` §"Session drain" (L631-680) and
  §"Context maintenance — research-driven refresh" (L682-730) duplicate
  `context-maintenance`.

Action: trim `reporting` to its own capability — chat-vs-harness-vs-report
decision, what chat carries, question-asking discipline, YAML header, psyche
reports, prose+visuals medium — and replace the naming and maintenance sections
with pointers to `report-naming` and `context-maintenance`. Target: **851 →
~560-600**. `report-naming` stays as the canonical naming home (do not eliminate
it; it is the compact owner, `reporting` is the over-absorber).

Psyche-decision: none. Assignability: unchanged (no skill removed).

### A3. actor-systems ↔ kameo — the spawn-in-thread supervised-state trap is triplicated (HIGH confidence, lowest-risk edit in the corpus)

The Kameo-0.20 dedicated-thread shutdown-race trap appears three times,
paraphrase-level identical:

- `actor-systems` L256-271 (§"Supervision gotcha — dedicated-thread"),
- `kameo` L685-700 (inside Template 2),
- `kameo` L748-753 (anti-pattern bullet).

`actor-systems` L526-541 already delegates "how to express ... in Kameo" to
`kameo`. Action: keep one canonical statement in `kameo`, collapse the
`actor-systems` copy to a one-line pointer, and dedupe kameo's own second copy
to a back-reference. Same pattern for the **multi_thread parallel-restart-test
hang** (`actor-systems` L589-602 vs `kameo` L754-760 → kameo owns it) and the
minor **"counter at 12 reads back as 0" restart example** (`actor-systems`
L431-447 vs `kameo` L440-456 → keep both framings, drop the duplicate
illustration). Reclaim: ~20-30 lines.

Psyche-decision: none. Assignability: unchanged.

### A4. component-triad ↔ contract-repo — wire-vocabulary model duplicated (MEDIUM-HIGH confidence)

Both teach the full three-layer verb model and the six payloadless Sema classes:

- `component-triad` L288-302 (Contract Operation / Component Command / Sema
  Operation) + L304-314 (six Sema classes table) + `ToSemaOperation` at L300-302;
- `contract-repo` L182-213 (§"Three layers, distinct vocabularies") + L240-257
  (six-word forbidden-on-wire table) + `ToSemaOperation` at L210-213.

Both also teach the NOTA-is-not-the-inter-component-wire boundary
(`component-triad` L482-514 vs `contract-repo` L377-405 with the canonical
boundary table at L388-399).

Action: let **`contract-repo` own the wire-vocabulary table and the
NOTA-boundary table** (it is the wire-contract skill); compress
`component-triad` §3 (L284-329) and §"No NOTA between components" (L482-514) to
their authority-direction commentary plus pointers. Reclaim from
component-triad: ~30-40 lines.

Psyche-decision: none. Assignability: unchanged.

### A5. "Continuous manifestation discipline" / manifest-into-INTENT.md duplicated across the intent docs (MEDIUM confidence)

A "manifest recorded intent into the affected repo's INTENT.md as part of the
work cycle" block recurs in `repo-intent` (L70-98, §"Continuous manifestation
discipline"), `architecture-editor` (L224-252, same heading), `intent-log`
(L147-158, §"Capture is not done until it manifests"), and the manifest-target
material spreads across `intent-manifestation`, `intent-clarification`,
`context-maintenance-deep` (six files touch "manifest into INTENT.md").

Action: designate **`repo-intent` as the canonical owner of the continuous
per-repo manifestation rule** and **`intent-manifestation` as the owner of the
destination decision-tree**; reduce the `architecture-editor` and `intent-log`
copies to pointers. Reclaim: ~20-30 lines across the cluster.

Psyche-decision: none. Assignability: unchanged.

### A6. helper-dispatch pair overlap (MEDIUM confidence; assignability flag)

`when-to-use-helpers` (47, Apex) and `helper-context-transfer` (72, Mechanism)
overlap on the minimal-dispatch-envelope idea: `when-to-use-helpers` §"minimal
dispatch envelope" ≈ `helper-context-transfer` §"Use the helper as the context
carrier" + §"What the lead does before dispatch". The split is defensible as a
two-tier Apex-rule / Mechanism-how pairing, and the residue-readback nugget in
`when-to-use-helpers` is genuinely distinct.

Action (choose one):

- **Lower-risk (preferred): trim, don't merge.** Cut
  `helper-context-transfer`'s restatement of the minimal-envelope rule (its
  first two sections) to a pointer; keep its concrete "build the reading
  envelope" + "brief shape" content. ~15-line reclaim. No assignability change.
- **Higher-risk: merge into one `helper-dispatch` skill (~90 lines).** This
  removes one index entry and **changes what is assignable to roles** (one
  skill instead of two; the Apex tier collapses into Mechanism). Flag to the
  per-role assignment worker.

Psyche-decision: only if the merge option is taken (it changes the index/tiers).

## Section B — within-skill wordiness trims (ranked)

### B1. component-triad 1160 → ~900 (HIGH confidence on the mass; structural split is a separate option)

Sub-agent (line-cited) found the runtime-triad half (L733-1160) re-describes
Nexus's "mail keeper + translator" role repeatedly, and L1140-1160 (§"Nexus's
inner-world / outer-world vocabulary") is near-pure restatement of L790-880.
Binary-naming is taught three times (prose L142-172, subsections L157-208, and
the 13-row table L189-203 — the table alone teaches it). War-story current-state
narration at L43-75 (spirit/criome meta-contract violations) is not discipline.
Trace is taught in two separated places (L516-540 and L1049-1108).

Action: compress per the cites above; preserve every normative rule
(single-source contract crate, `ToSemaOperation`, NexusWork/NexusAction at
L986-1047, engine traits). Target ~900.

Structural option (psyche/owner decision): the file is effectively two
capabilities — repo-triad (L1-731) and runtime triad / Signal-Nexus-SEMA
(L733-1160). Per the skill-editor "one capability per skill" test, this is a
candidate to **split into `component-triad` + `runtime-triad`**. A split **adds
an index entry and changes assignability** (roles/agents could load the runtime
half without the repo-shape half). Recommend raising the split to the psyche
before acting; the compression above is independently safe.

### B2. prose 585 → ~400 (MEDIUM confidence; psyche-decision)

§"The reference shelf" (L267-450) carries **13 named literary exemplars**
(Heraclitus, Plutarch, Cicero, Marcus Aurelius, Hemingway, Blake, Bastiat,
Ptolemy, Vedic/Upaniṣadic, Castaneda, Arnau, Rudhyar). The skill-editor rule is
"keep the single best example; cut second and third." Thirteen exemplars is the
exact shape that rule names.

Action: cut the shelf to **3-4 exemplars** that span the needed registers;
target 585 → ~400.

Psyche-decision: **required.** `prose` is an aesthetic/voice skill; the psyche
may deliberately value the breadth of the reference shelf. Confirm before
culling exemplars.

### B3. NOTA/language cluster trims (MEDIUM confidence)

From the NOTA sub-agent (line-cited), preserving every rule and WHY:

- `nota-design` 334 → ~280: §"Schema enum sugar" (L57-130) and §"Type-table
  variant resolution" (L132-140) teach the explicit-`(Variant PayloadType)`
  spelling twice (L71 vs L140) — fold and compress the five code blocks; trim
  the inline-`\n`-escape section (L214-236) and the §"Before you sketch"
  checklist (L281-290) that re-derives Rules 1/2/3/5.
- `language-design` 282 → ~240: §"18. Delimiters earn their place" (L209-236)
  and §"0. NOTA is the only text syntax" (L21-46) carry rhetorical padding; the
  "cost X / gain Y" tail recurs in instincts #4/#5/#13/#16.
- `nota-comments` 142 → ~125: §"Mind integration" (L126-136) is speculative
  future, compress to ~5.
- `nota-schema-docs` 79 → ~72 and `structural-forms` 168 → ~150 are near floor;
  only soft spots are a second worked example (nota-schema-docs L49-73) and the
  duplicated commit-hash provenance in structural-forms (see C3).

Cross-overlap (MEDIUM): `nota-design` ↔ `language-design` duplicate three atomic
rules in substance — PascalCase=type / first-char dispatch (`nota-design` L45 vs
`language-design` L76-79), no-multi-field-tuples (`nota-design` L273-275 vs
`language-design` L161-169), records-are-positional (`nota-design` L288 vs
`language-design` L171-180). Action: make `language-design` instincts #4/#13/#14
thin (principle + pointer to `nota-design` for the worked NOTA detail) and **add
`nota-design` to `language-design`'s See-also** (it is currently absent despite
being the most-overlapping sibling). No merge warranted.

### B4. rust-discipline index re-teaches its leaf skills (MEDIUM confidence)

`rust-discipline` (125) is meant to be an index but re-teaches leaf content:
§"Naming — full English words" (L64-88) duplicates `naming` (including a
Wrong/Right code example and the C-CRATE-PREFIX rule), and §"Actors: logical
units with kameo" (L89-117) re-lists 8 actor rules that live in `kameo` /
`actor-systems`. Action: cut both to pointers, keeping the index's unique
content (one-sentence rules, the sub-file table — with paths corrected per C1,
Toolchain authority, Target-directory hygiene). Target 125 → ~70.

### B5. contract-repo / actor-systems / kameo internal trims (MEDIUM, from sub-agent)

- `contract-repo` 571 → ~500: the "Sema vocabulary forbidden on the public wire"
  point is made three times (L202-213, L239-257, L289-291) — keep the table +
  one cross-ref; trivial kernel-extraction mermaid at L432-438.
- `actor-systems` 624 → ~545: the "no non-actor wrapper around ActorRef" rule is
  stated three times (L106-128, L463-492, L526-541); the ZST anti-pattern code
  example (L163-203) is ~18 lines for a point the prose already makes.
- `kameo` 790 → ~735: the L731-784 anti-patterns list restates earlier sections
  (tell-fallible L287-297, spawn_in_thread, multi_thread) — dedupe to pointers.

### B6. naming 367 → ~280 (LOWER confidence)

Keystroke-tier skill that should be quick-reference. Three "Anti-pattern:"
sections (L165, L222, L268) plus the offender table; the skill-editor rule
"prefer canonical positive forms over enumerating failed alternatives" suggests
compressing the anti-pattern prose around the (kept) offender table. Lower
confidence — the anti-patterns are genuinely distinct. Note the C-CRATE-PREFIX
overlap with `rust-discipline` (B4).

## Section C — staleness and correctness

### C1. Stale `skills/rust/<x>.md` cross-references, corpus-wide (HIGH confidence; pure correctness)

The generated skills are flat: `rust-methods`, `rust-errors`,
`rust-storage-and-wire`, `rust-parsers`, `rust-crate-layout` (emitted at
`.agents/skills/rust-methods/SKILL.md`, etc.). But ~18 cross-references across 11
modules point at a non-existent nested `skills/rust/<x>.md` layout. Occurrences:
`rust-discipline` (L15, L20-24 sub-file table, L117), `rust-methods` (L484 →
`skills/rust/errors.md` while the same file uses the correct flat
`skills/abstractions.md`), `actor-systems` (L516), `contract-repo` (L15, L566),
`enum-contact-points` (L268, L293, L334), `kameo` (L683), `rust-crate-layout`
(L147), `rust-errors` (L42), `rust-parsers` (L15), `rust-storage-and-wire`
(L188), `versioning` (L99).

Action: rewrite every `skills/rust/methods.md` → `skills/rust-methods.md` (and
errors / storage-and-wire / parsers / crate-layout likewise). Pure find/replace
discipline; every one of these is currently a broken pointer. No psyche-decision.

### C2. Tail-omission contradiction between nota-design and language-design (HIGH confidence; substantive, needs owner/psyche resolution)

The two files state opposite rules:

- `nota-design` L271 (and L144): "Tail omission is **not** a compatibility
  shape: every position in the text carries every position in the schema,
  always ... NOTA forbids tail-omission."
- `language-design` L177-180 (#14): "Tail-omitted optionals are a compatibility
  read-shape: a decoder may accept a record missing trailing optional fields,
  but canonical encoders emit explicit `None` ..."

This is a genuine rule conflict, not redundancy. Action: resolve to one
statement across the cluster **before** trimming either file (B3). Flag to the
NOTA/schema owner; this is a correctness decision, not an editorial trim.

### C3. structural-forms carries commit-hash / dated provenance (HIGH confidence; skill-editor rule violation)

`structural-forms` L71-74 cites "on schema-next main as of 2026-06-18: `af3705c`
... `95f1ee7` ... `1de72dde`" and repeats the same three hashes in §"See also"
(L165-168). The skill-editor doctrine ("No correction or changelog banners —
describe what IS, not what changed; the path lives in version-control history")
forbids this. Action: state the behavior as current-state and drop both
dated-commit citations. Reclaim ~10 lines.

### C4. Broken section anchor in intent-maintenance (LOW stakes; correctness)

`intent-maintenance` L144 references `skills/intent-log.md §"Certainty
vocabulary"`, but `intent-log`'s actual heading is §"Certainty versus
importance" (L249). The same loose "certainty vocabulary" phrasing recurs in
`spirit-cli`'s See-also (L457-459) and `intent-maintenance` L198. Action: fix the
anchor to the real heading.

### C5. intent-log ↔ spirit-cli record-shape duplication (LOW-MEDIUM confidence)

`intent-log` §"Record shape" (L187-227) re-spells the seven-field `Entry` +
court-model `Justification` NOTA block that `spirit-cli` §"Recording intent"
(L75-165) owns, even though `intent-log` L225-226 explicitly says "the wire
shape may drift; `spirit-cli.md` covers reading the currently deployed shape."
The "clarification is an edit, not a fresh Record" rule is stated at length in
three files (`intent-log` gate + Recordable-kinds, `intent-maintenance` opening,
`spirit-cli` §"Clarifying"). Action: keep `intent-log`'s conceptual field list,
defer the literal NOTA wire block to `spirit-cli`, and consolidate the
clarification-is-an-edit rule to one canonical statement (`intent-maintenance`)
with pointers. Low priority; the split itself is principled (see D below).

## Section D — clusters checked and found sound (do NOT merge/eliminate)

Recording negative findings so a later pass does not re-litigate them:

- **The 6-skill intent stack is NOT over-split.** `intent-log` (what/when to
  capture), `spirit-cli` (how to invoke the binary), `intent-maintenance`
  (sweep/supersede), `intent-manifestation` (into guidance files),
  `intent-clarification` (asking the psyche), `repo-intent` (the per-repo file)
  each carry a distinct trigger and follow "one capability per skill." Keep all
  six; the only work is the cross-cluster dedup in C5/A5/C4. **Do not merge.**
- **engine-analysis vs engine-report are complementary, not redundant.** Deep
  architecture lens vs measurement/presentation pass; each cross-references the
  other correctly. Only a minor shared status-vocabulary (hooked/stubbed/
  contract-only/conceptual/stale) and visual-rules overlap — not worth a merge.
  Keep both.
- **The code-repo branch-workflow set is a coherent family.** `main-next`,
  `feature-development`, `main-feature-integration`, `double-implementation-strategy`
  teach distinct mechanisms. Minor overlap: the "branch, never a new repo" rule
  is stated in `feature-development` §"A branch has no limits" and
  `double-implementation-strategy` §"Both tracks are branches", and the
  "code-repos-only, NOT primary" scope banner is in both `main-next` (L3-5) and
  `feature-development` (L3-10). `double-implementation-strategy` (86) re-states
  `main-next` + `feature-development` for its scenario — trimmable to pointers,
  but no merge. Keep all four.
- **component-triad ↔ actor-systems engine-traits material is correctly
  cross-referenced** (`actor-systems` L494-516 cites component-triad rather than
  re-teaching). Not an overlap to cut.
- **The role layer is clean.** No dedup work there.

## No whole-skill elimination or archive candidates found

No skill is dead or wholly superseded. `report-naming` looks redundant against
`reporting` only because `reporting` over-absorbed its scope (A2) — `report-naming`
is the correct canonical home and stays. The corpus problem is duplication and
bloat within/across live skills, not unused skills.

## Assignability flags (for the per-role skill-assignment worker)

Only two proposals would change the set of assignable skills:

- **A6 merge option** (helper pair → one `helper-dispatch` skill): removes one
  index entry, collapses an Apex+Mechanism pair. Default recommendation is the
  trim-not-merge option, which preserves both.
- **B1 split option** (component-triad → `component-triad` + `runtime-triad`):
  adds one index entry; lets an agent load the runtime half alone.

Every other proposal trims or de-duplicates content within the existing 66-skill
set and leaves the index membership and tiers unchanged.

## Psyche-decisions required

- **C2 tail-omission contradiction** — a real rule conflict; the NOTA/schema
  owner (or psyche) must pick the canonical rule before B3 trims either file.
- **B2 prose exemplar cull** — aesthetic; confirm the psyche does not value the
  full 13-exemplar reference shelf before reducing it.
- **B1 component-triad split** and **A6 helper-pair merge** — only if the
  structural option is taken (both change the index/assignability).

All other items in A, B, C are within ordinary skill-editor authority (boundary
calls the index already implies, or pure correctness fixes) and need no psyche
sign-off to enact in a later applying pass.

## Provisional-learning note

These are recommendations from a read-only audit, not accepted doctrine. They
become authority only when the psyche accepts them or they land through the
generator-source skill-editing path. Confidence levels are the auditor's, to be
re-checked at apply time.

## Follow-up / blockers

- Apply pass is a separate, write-authorized skill-editor task against
  `/git/github.com/LiGoldragon/skills` modules, followed by
  `nix run github:LiGoldragon/skills#generate-skills -- /home/li/primary` and a
  `check-skills` drift inspection. Nothing here was applied.
- C1 (stale `skills/rust/` paths) and C3/C4 (provenance + anchor) are the safest
  first wins — pure correctness, no judgment, no psyche-decision.
- Resolve C2 (the rule conflict) before any NOTA/language trimming.
