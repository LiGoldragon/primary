# Intent Translator — Implementation Brief (RoleSkillReview)

## Artifact

The executable dependency graph and per-implementer briefs for two settled
psyche orders:

1. Delete `skills/skills.nota` and remove it from the `AGENTS.md` startup
   contract; fix every downstream reference (primary docs, the generator,
   prose modules, and the `mentci` hard-coded validator) so nothing breaks.
2. Make role-packet generation FULL-INLINE: every generated role packet bakes
   in the full bodies of its curated skills; the spawned worker reads no skill
   file. The generator/manifest must express role to skill assignment and
   inline those bodies into `.claude/agents/*.md`, `.codex/agents/*.toml`, and
   `.pi/agents/*.md`.

Both orders are binding. This brief executes them and solves their downstream
consequences in the task set; it does not re-open them or offer alternatives.

## Scope and authority of this brief

Read-only translation. No source was edited; the single writable artifact is
this file. The tasks below are written EXECUTE-style for downstream worker
roles. The lead/orchestrator commits primary and dispatches the workers; it is
not itself one of these tasks.

## Source artifacts consulted

- `agent-outputs/RoleSkillReview/IntentTranslator-RoleSkillAssignment.md` — the
  per-role curated skill SETS plus the shared baseline. The NAME-vs-INLINE
  question in that file is RESOLVED to inline by settled order 2; its
  "recommended default: name, do not inline" is overruled. The skill-set
  selections remain the curation input (the anti-bloat knob).
- `agent-outputs/RoleSkillReview/SkillEditor-CorpusTrimProposal.md` — the
  de-duplication and bloat-trim actions. No whole-skill deletions exist.
  Inlining multiplies duplicated skill text across packets, so the cross-skill
  dedup trims and the high-bloat within-skill trims must land before or with
  regeneration.
- `agent-outputs/RoleSkillReview/Scout-SkillsNotaDeletionPlan.md` — the full
  `skills.nota` reference inventory, the change-list, and the `mentci`
  dependency with exact path:line cites.
- `agent-outputs/RoleSkillReview/Scout-PiSubagentMining.md` — Pi bundled
  subagent mining. Its role/skill additions are SEPARATE proposals, folded in
  only as clearly-marked optional follow-on (Phase 6), never as blockers.

## Settled downstream resolutions (consequences solved, not surfaced)

These are decided here as the forced consequence of the two settled orders, so
no task waits on them:

- Lead/ad-hoc discovery surface after the index is gone: spawned workers carry
  full-inline skills and need no discovery surface. The only surface left
  uncovered is the lead/orchestrator lane and ad-hoc primary sessions, which
  boot from `AGENTS.md` with no packet. Their discovery surface becomes the
  harness-injected available-skills list (present in every Claude Code session
  today). The fallback for any harness that does not inject such a list is the
  standalone skill files (`.agents/skills/*/SKILL.md`,
  `.claude/skills/*/SKILL.md`), which remain materialized after this work — the
  inline order multiplies bodies into packets but does not remove the
  standalone skill surfaces. Both surfaces are concrete and already present;
  Task S1 only verifies harness injection and records the fallback.
- `mentci` re-point target: `mentci`'s scaffold "expansion index" stops being a
  file path that points at the deleted index; it is parameterized and its
  default re-points at the primary `AGENTS.md` startup contract (the surface
  that now names the harness-injected list). The exact replacement value is a
  bounded mentci-lane detail inside Task M1, not a blocker on the primary work.
- Corpus-trim scope split: only the non-psyche-gated trims (cross-skill dedup
  A1–A6, high-bloat within-skill trims, and the pure-correctness fixes) are in
  the critical path (Task C1). The psyche-gated trims (prose exemplar cull B2,
  NOTA tail-omission conflict C2, the component-triad split, the helper-pair
  merge) are explicitly deferred to optional follow-on (Phase 6) and gate
  nothing here.

## Dependency graph (text, no cycles)

Phase 0 — parallel prep (no cross-break):
- C1 corpus dedup + prose pass (generator source modules)
- M1 mentci re-point (mentci repo)
- S1 harness-discovery verification (read-only)

Phase 1 — generator code, sequential (depends on nothing in Phase 0 for code,
but shares the regen gate):
- G1 role to skill assignment data  →  G2 inline emit  →  G3 remove
  `skills.nota` emission  →  G4 generator green (build + tests)

Phase 2 — regenerate primary:
- P1 regenerate primary surfaces  (depends on: C1, G4)

Phase 3 — primary contract + deletion:
- P2 primary contract edits + delete the index  (depends on: G3, M1, S1; lands
  in the same working copy as P1)

Phase 4 — validation and audit (validation precedes audit):
- V1 primary verification sweep  (depends on: P1, P2)
- A1 rust audit (generator + mentci)  (depends on: G4, M1)
- A2 nix audit (flake checks + regen drift)  (depends on: P1)
- A3 corpus + inline-content review  (depends on: P1, C1)

Phase 5 — land:
- R1 repo-operator: commit/push generator → mentci → primary, producers before
  consumers  (depends on: A1, A2, A3, V1)

Phase 6 — optional follow-on (NOT blockers): psyche-gated corpus trims; Pi
mining role/skill proposals.

Blocking summary: `C1` and `G4` block `P1`; `G3`, `M1`, `S1` block `P2`; `P1`
and `P2` block `V1`; `G4`, `M1`, `P1`, `C1` feed the audits; all audits plus
`V1` block `R1`.

## Per-task implementer briefs

### Task C1 — Corpus dedup and skills.nota prose removal (pre-regen)

- Role: skill-editor.
- Repo: `/git/github.com/LiGoldragon/skills` (generator source modules; this is
  a code-repo, so work on a branch per the repo's own main/next discipline).
- Objective: trim the cross-skill duplication and the highest-bloat skill
  bodies so inlining does not multiply duplicated text into packets, and remove
  every `skills/skills.nota` reference from prose modules.
- Do:
  - Remove `skills/skills.nota` references from `modules/skill-editor/full.md`
    (L53,63,80,102), `modules/helper-context-transfer/full.md` (L25),
    `modules/nota-design/full.md` (L9,154,285,333), and
    `modules/nota-schema-docs/full.md` (L79); for the NOTA pedagogical examples
    pick a new canonical live NOTA file (for example
    `skills/generated-role-outputs.nota`) so the "open and read three records"
    instruction still resolves.
  - Apply ONLY the non-psyche-gated trims from
    `SkillEditor-CorpusTrimProposal.md`: A1 (drain/three-fate/lane-registry/
    fresh-context-pickup canonical-owner pointers), A2 (trim `reporting`
    851→~560, the biggest single inline win because `reporting` is baseline and
    lands in every packet), A3 (actor-systems↔kameo dedup; both co-occur in the
    rust-heavy packets), A4 (component-triad↔contract-repo wire-vocabulary),
    A5 (intent-doc manifestation dedup), A6 trim-not-merge option, B1
    compression of `component-triad` 1160→~900 (no split), B4 (`rust-discipline`
    125→~70, re-taught leaf content to pointers), B5 (contract-repo /
    actor-systems / kameo internal trims), B6 (`naming` 367→~280), C1 (rewrite
    every stale `skills/rust/<x>.md` cross-ref to the flat `skills/<x>.md`), C3
    (drop `structural-forms` dated commit-hash provenance), C4 (fix the
    `intent-maintenance` anchor).
  - Do NOT apply the psyche-gated items: B2 prose exemplar cull, C2
    tail-omission conflict, the B1 component-triad split, the A6 merge option.
    They are Phase 6.
- Decision ownership: WHICH trim edits land is skill-editor's; the SET of
  in-scope trims and the before-regen sequencing are fixed by this brief.
- Completion claim: "Cross-skill dedup and skills.nota prose removal applied to
  the generator source modules; psyche-gated trims excluded."
- Evidence: before/after line counts for `reporting`, `component-triad`,
  `rust-discipline`, `naming` matching the proposal targets; `rg "skills\.nota"`
  over `modules/` returns zero; the generator's own check (duplicate-heading and
  drift gates) passes on the edited modules.
- Source context: `SkillEditor-CorpusTrimProposal.md` sections A, B, C; the
  module paths cited in `Scout-SkillsNotaDeletionPlan.md` step 3.

### Task M1 — Re-point and parameterize the mentci expansion index

- Role: general-code-implementer (Rust); audited by rust-auditor (A1).
- Repo: `/git/github.com/LiGoldragon/mentci` (code-repo; branch per its
  main/next discipline).
- Objective: stop hard-requiring the literal `skills/skills.nota` so deleting
  the index in primary does not break mentci-launched sessions or mentci's own
  preflight check.
- Do: parameterize the scaffold expansion index and re-point its default at the
  primary `AGENTS.md` startup contract (the surface that names the
  harness-injected skill list). Update `src/preflight.rs` (L243 prompt text,
  L525-527 the `expansion_index == "skills/skills.nota"` enforcement),
  `src/bin/mentci-claude-proof-test.rs` (L291,296,327),
  `schema/preflight-launch.nota.md` (L83,102), `ARCHITECTURE.md` (L94,283),
  `INTENT.md` (L72), and the named tests (`tests/harness_sessions.rs:135`,
  `tests/harness_adapters.rs:111,503`,
  `tests/preflight.rs:43,73,95,132,148,206,216`).
- Decision ownership: whether the index is parameterized, removed, or made
  configurable is a bounded mentci-lane choice; the fixed constraint is that
  preflight must no longer reference the deleted file and `cargo test` must stay
  green.
- Completion claim: "mentci no longer hard-requires `skills/skills.nota`;
  preflight validation, prompt text, schema, docs, and tests updated; tests
  green."
- Evidence: `cargo test` passes; `rg "skills/skills\.nota"` over mentci returns
  zero (or only an intentionally configurable default, not a hard validator).
- Source context: `Scout-SkillsNotaDeletionPlan.md` section "Cross-repo
  consumer ... mentci" and step 4.
- Dependency note: must be landed (committed) before P2 deletes the index in
  primary.

### Task S1 — Verify harness-injected discovery and record the fallback

- Role: scout (read-only).
- Objective: confirm the lead/ad-hoc discovery surface that replaces the index
  works on each target harness, and record the standalone-skill-file fallback.
- Do: confirm the Claude Code harness injects an available-skills list (it does
  — present in the live session). Check whether the Pi and Codex harnesses
  inject an equivalent list (Pi `skills.ts`/`formatSkillsForPrompt` was noted as
  surfacing skills; Codex is unverified). Record, per harness, whether the
  primary discovery surface (injected list) is present, and confirm the fallback
  surface (`.agents/skills/*/SKILL.md`, `.claude/skills/*/SKILL.md`) remains
  materialized after the inline order.
- Completion claim: "Per-harness discovery-surface availability mapped; fallback
  confirmed present."
- Evidence: per-harness yes/no on injected skill list; `ls` confirming the
  standalone skill files exist; the exact wording to put in `AGENTS.md` startup
  (primary surface plus fallback).
- Source context: `Scout-SkillsNotaDeletionPlan.md` "Replacement discovery
  mechanism" Option A and "Unknowns".
- Dependency note: feeds the `AGENTS.md` rewrite in P2.

### Task G1 — Express role to skill assignment in the manifest

- Role: skill-editor (manifest data); general-code-implementer if the generator
  schema must be extended to carry the curated set.
- Repo: `/git/github.com/LiGoldragon/skills`.
- Objective: make the role to skill channel carry each role's curated skill set
  plus the shared baseline declared once.
- Do: populate the role to skill assignment per the table in
  `IntentTranslator-RoleSkillAssignment.md`. Prefer the sidecar route: declare
  the six-entry baseline (`agent-output-protocol`, `reporting`, `naming`,
  `workspace-vocabulary`, `privacy`, `secrets`) once and carry it on every
  `role-*` record's dependency slot in
  `manifests/module-dependencies.nota` (currently `[]`), and add the
  role-specific ids per the table; let transitive resolution dedup. If the
  generator does not yet resolve role-* dependency edges into the packet, extend
  it minimally to do so.
- Decision ownership: the curated SETS are fixed by
  `RoleSkillAssignment.md`; the carrying surface (sidecar dep edges vs the
  `active-outputs.nota` module list) is skill-editor's, with the brief's
  recommendation to use the sidecar so the baseline lives in one place. Treat
  the proposal's "conditional" skills as "always carry" for V1 static packets
  unless the psyche says otherwise (noted, not a blocker).
- Completion claim: "Each role's curated skill set plus the shared baseline is
  expressed in the manifest and resolves transitively."
- Evidence: the manifest diff; a generator dry-run or unit test showing each
  role resolves to its expected id set with the baseline applied exactly once.
- Source context: `RoleSkillAssignment.md` "Role to Skill Table" and
  "Generator and Manifest Requirement" 1 and 3.

### Task G2 — Inline emit semantics (full bodies into packets)

- Role: general-code-implementer (Rust); audited by rust-auditor (A1).
- Repo: `/git/github.com/LiGoldragon/skills` (`src/assembly.rs` and the emit
  path).
- Objective: emit each role packet with the FULL BODY of every assigned skill
  inlined (transitively resolved from G1), into `.claude/agents/*.md`,
  `.codex/agents/*.toml`, and `.pi/agents/*.md`. The spawned worker reads no
  skill file.
- Do: extend the packet assembler so that, in addition to the existing
  `agent-output-protocol` inline, it inlines the resolved curated skill bodies.
  Reuse the existing skill-body loading path (`active_skills()` / the per-skill
  `modules/<name>/full.md` reads) as the body source — this becomes the new
  consumer of that data, which matters for G3.
- Decision ownership: emit format details (ordering, per-skill headers, TOML
  escaping for the Codex surface) are the implementer's; the fixed requirement
  is full bodies, all three surfaces, no named-but-deferred references.
- Completion claim: "Role packets emit inlined full skill bodies across all
  three agent surfaces."
- Evidence: `cargo build` and `cargo test` green; a sample emitted packet (for
  example general-code-implementer) shown to contain the rust-cluster skill
  bodies verbatim; packet byte sizes recorded.
- Source context: settled order 2; `RoleSkillAssignment.md` "Generator and
  Manifest Requirement" 2 (read as RESOLVED to inline).
- Dependency: after G1.

### Task G3 — Remove the skills.nota emission from the generator

- Role: general-code-implementer (Rust); audited by rust-auditor (A1).
- Repo: `/git/github.com/LiGoldragon/skills`.
- Objective: stop emitting `skills/skills.nota` without breaking the
  skill-body assembly that G2's inliner now depends on.
- Do: remove the hard-coded `Rendered` job (`src/assembly.rs:254-258`) and the
  `expected.insert("skills/skills.nota")` (`:383`). Delete `SkillIndex`,
  `SkillIndex::render`, `ActiveSkill::index_record`, and
  `SkillCategory::as_str` / `SkillTier::as_str` ONLY if G2 left them with no
  consumer; verify `active_skills()` and the skill-body loaders still have the
  G2 inliner as a live consumer and are NOT pruned. Update
  `tests/generation.rs:37-38` (the index-content assertion) and `:410,:428`
  (the `skills/skills.nota` fixtures); update `skills.md:12` to describe the new
  mechanism.
- Completion claim: "The generator no longer emits or expects
  `skills/skills.nota`; skill-body assembly for inlining is preserved; tests
  updated."
- Evidence: `cargo build` and `cargo test` green; no dead-code warning for the
  skill-body path; a `generate-skills` dry-run output listing that contains no
  `skills/skills.nota` entry.
- Source context: `Scout-SkillsNotaDeletionPlan.md` step 1.
- Dependency: after G2 (so the skill-body code is never momentarily unused).

### Task G4 — Generator green gate

- Role: general-code-implementer (with nix-auditor verifying the flake side in
  A2).
- Objective: confirm the generator builds, tests pass, and its checks are clean
  with G1+G2+G3 and the C1 module edits in place.
- Do: build the generator, run `cargo test`, and run the generator's own
  `check` against the edited modules.
- Completion claim: "Generator builds, tests pass, and checks are clean with
  inline emit, assignment data, no skills.nota emission, and trimmed modules."
- Evidence: green `cargo test`; clean check output; the dry-run packet listing.
- Dependency: after C1, G1, G2, G3.

### Task P1 — Regenerate primary surfaces

- Role: skill-editor (generated-surface reconciliation); nix-auditor reviews the
  Nix run in A2.
- Repo: `/home/li/primary` (work on `main`, jj).
- Objective: regenerate primary so packets carry inlined full bodies and the
  index is no longer produced.
- Do: run the generator against primary
  (`nix run github:LiGoldragon/skills#generate-skills -- /home/li/primary`, or
  the local path if testing the branch). Then run `check-skills` for drift.
- Completion claim: "Primary regenerated with inlined role packets; no
  `skills.nota` produced; check-skills drift clean."
- Evidence: the regen diff (packets gain inlined bodies); `check-skills` clean;
  spot-check that a representative packet on each of the three surfaces carries
  the expected skill bodies; packet sizes recorded against the "enough, not
  bloated" target.
- Dependency: after C1 and G4 (the generator and modules must be final).

### Task P2 — Primary contract edits and index deletion

- Role: skill-editor for `AGENTS.md` and `ARCHITECTURE.md`; intent-maintainer
  for the `INTENT.md` narrative reword (psyche-statement fidelity); the file
  deletion lands in the same working copy.
- Repo: `/home/li/primary` (`main`, jj).
- Objective: remove `skills/skills.nota` from the startup contract and all
  primary docs, point lead/ad-hoc discovery at the harness-injected list with
  the standalone-skill-file fallback, and delete the orphan index file.
- Do:
  - `AGENTS.md` Startup (L6-14) and Skill Index (L16-19): replace "Read
    `skills/skills.nota`. It is the only default discovery read." and the "do
    not scan `skills/`" sentence with the discovery wording from S1 — the
    harness-injected available-skills list as the primary surface, the
    standalone `.agents/skills/*/SKILL.md` files as the fallback for any harness
    without injection. `AGENTS.md:58`: change "the Rust skills selected from
    `skills/skills.nota`" to "the Rust skills" via the replacement surface.
  - `ARCHITECTURE.md:48`: remove the `skills/skills.nota` tree line; keep
    `skills/generated-role-outputs.nota`.
  - `INTENT.md:199`: reword the new-role narrative to drop the
    `skills/skills.nota` query.
  - Delete `skills/skills.nota` (jj-tracked; the pruner does not remove it).
    Keep `skills/generated-role-outputs.nota`.
- Completion claim: "Primary startup contract and docs no longer reference the
  index; the index file is deleted; discovery points at the harness list with a
  fallback."
- Evidence: the doc diffs; the tracked deletion; `rg "skills\.nota|skills/skills"`
  over primary excluding `reports/`, `agent-outputs/`, and `context.md` returns
  zero.
- Source context: `Scout-SkillsNotaDeletionPlan.md` step 2; S1's discovery
  wording.
- Dependency: after G3 (generator no longer re-emits), M1 (mentci safe), and S1
  (discovery wording). Lands in the same working copy as P1.

### Task V1 — Primary verification sweep

- Role: the dispatching lead, or a scout, before audit.
- Objective: confirm the end state is internally consistent before auditors
  review.
- Do: `rg "skills\.nota|skills/skills"` over primary (excluding reports,
  agent-outputs, context.md) is zero; confirm each of the ten role packets on
  all three surfaces contains its expected inlined skill bodies and no dangling
  `skills/<name>.md` cross-reference points at a missing file; confirm
  `check-skills` is clean.
- Completion claim: "Primary end state verified: zero index references, packets
  carry expected inlined bodies, no broken cross-refs, drift clean."
- Evidence: the `rg` result; the per-packet spot-check; the `check-skills`
  output.
- Dependency: after P1 and P2. Validation precedes all audits.

## Audit recommendation

Substantial work; distinct auditors by default. Validation (V1 and each task's
evidence) precedes audit. Corpus-trim items remain provisional observations
until accepted; the audits below are defect review, not guideline adoption.

- A1 rust-auditor — reviews the generator Rust (G2 inline emit, G3 removal and
  the dead-code reconciliation) and the mentci Rust (M1). Receives: the
  generator and mentci diffs, `cargo test` output, the dry-run packet listing,
  and the changed-file paths. Defect review: correctness of inline assembly,
  that the skill-body path keeps a live consumer, typed-error and method
  discipline, and that no test was weakened rather than updated.
- A2 nix-auditor — reviews the flake check derivations touched by the generator
  change and the regeneration/drift behavior (P1). Receives: the flake-check
  results, the `generate-skills` and `check-skills` output, and the regen diff.
  Defect review: check coverage and that regeneration is reproducible and
  drift-clean.
- A3 corpus and inline-content review — a distinct skill-editor instance.
  Receives: the C1 module diffs, before/after line counts, and the emitted
  packets. Defect review: that the non-psyche-gated trims preserved every
  normative rule, that no `skills.nota` reference survives in any inlined body,
  that cross-references resolve, and that packets read as "enough, not bloated"
  after the trims. This auditor's trim-quality notes beyond defects are
  provisional corpus observations, not new authority.

## Landing

### Task R1 — Commit and push, producers before consumers

- Role: repo-operator.
- Objective: land the three repos in dependency order without leaving a broken
  intermediate state.
- Do: land the generator branch (`/git/github.com/LiGoldragon/skills`) first
  (the producer), then mentci (`/git/github.com/LiGoldragon/mentci`), then
  primary (`/home/li/primary` on `main` via `jj commit` / `jj bookmark set main
  -r @-` / `jj git push --bookmark main`) carrying the regen output, the
  contract edits, and the index deletion in one working-copy commit. Mentci must
  be landed before the primary deletion is pushed.
- Completion claim: "Generator, mentci, and primary landed in producer-before-
  consumer order; primary deletion landed only after mentci was safe."
- Evidence: the push results per repo; final `rg` over primary confirming zero
  index references on the landed revision.
- Dependency: after A1, A2, A3, and V1.

## Phase 6 — Optional follow-on (not blockers)

These gate nothing in the two settled orders and are filed separately only if
the psyche elects them:

- Psyche-gated corpus trims as a second trim+regen pass: B2 prose exemplar cull
  (aesthetic, confirm the psyche does not value the full reference shelf), C2
  NOTA tail-omission rule conflict (resolve the canonical rule before any
  NOTA/language trim), the component-triad split, and the helper-pair merge.
  Each changes assignability or needs psyche sign-off per
  `SkillEditor-CorpusTrimProposal.md`.
- Pi mining proposals from `Scout-PiSubagentMining.md`: an `oracle` role plus a
  drift-check skill; a generalist-reviewer skill or role for plan/solution/
  health review; folding `worker` craft into general-code-implementer; folding
  the `context-builder` meta-prompt contract into the orchestration/helper
  skills; the `scout` Start-Here pointer; and the `planner` per-task acceptance
  and explicit dependencies fields. All provisional proposals, not part of the
  two settled orders.

## Remaining psyche decision points

None block the settled orders. The downstream consequences (lead discovery,
mentci re-point target, corpus-trim scope split) are solved in-brief above. The
only items requiring a psyche choice are the Phase 6 optional follow-on, which
are deferred by design and gate nothing here.

## Verification of this brief

- Every task has an objective, source context, completion claim, evidence
  expectation, and a downstream owner role.
- The graph has no cycles; validation (V1 and per-task evidence) precedes every
  audit; the generator producer lands before the primary consumer; mentci lands
  before the primary deletion.
- Each task's scope cites the input-artifact path and the source path:line it
  touches; a fresh worker can pick up any task from this file without chat
  memory.
- The two settled orders are executed, not re-opened; no alternatives are
  offered; the inline-vs-name question is treated as RESOLVED to inline.
