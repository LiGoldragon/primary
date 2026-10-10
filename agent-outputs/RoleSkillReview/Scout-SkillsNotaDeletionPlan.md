# Scout — skills.nota Deletion Plan (Situational Map)

## Task and scope

Map every reference to `skills/skills.nota` across primary and the generator
source `/git/github.com/LiGoldragon/skills`; identify what breaks if it is
deleted; propose a safe replacement discovery mechanism; and produce a concrete
deletion change-list as a PLAN (nothing applied). Read-only scout; the only file
written is this one.

Psyche-confirmed intent: `skills/skills.nota` is to be deleted and removed from
the `AGENTS.md` startup contract; skill discovery moves into the generated role
packets.

## Files and commands consulted

- `rg -n "skills\.nota|skills/skills"` over primary and `/git`.
- Read: `/home/li/primary/AGENTS.md`, `/home/li/primary/skills/skills.nota`,
  `/git/github.com/LiGoldragon/skills/src/assembly.rs`,
  `/git/github.com/LiGoldragon/skills/skills.md`,
  `/git/github.com/LiGoldragon/skills/AGENTS.md`,
  `/git/github.com/LiGoldragon/skills/manifests/active-outputs.nota` (Role records),
  `/git/github.com/LiGoldragon/skills/roles/scout/full.md`.
- `sed -n` on `ARCHITECTURE.md`, `INTENT.md`, generator tests, mentci preflight.
- `git ls-files skills/`, `ls .agents/skills .claude/skills .pi/agents .codex/agents`.

## Observed facts vs interpretation

Facts are cited with path:line. Interpretations are labelled.

### How skills.nota is produced (the generator)

- `src/assembly.rs:254-258` — the generator pushes a hard-coded
  `GenerationJob::Rendered` whose `OutputPath::new("skills/skills.nota")` is
  rendered by `SkillIndex::new(self.configuration.active_skills()).render()`.
  This is the single emission site of the index.
- `src/assembly.rs:993-1044` — `struct SkillIndex` + `SkillIndex::render` +
  `ActiveSkill::index_record` build the file body (the comment header and the
  `(Category name path Tier [desc])` records).
- `src/assembly.rs:1046-1067` — `SkillCategory::as_str` and `SkillTier::as_str`
  are consumed only by `index_record`. Interpretation: they become dead code if
  the index is removed.
- `src/assembly.rs:383` — `expected_outputs()` inserts the literal
  `"skills/skills.nota"` into the stale-output allow-set; without it the file
  would later be flagged stale.
- `skills/skills.nota` is generated, but the **pruner does not remove it**
  (`WorkspacePruner::prune`, lines 1210-1224, only removes `.agents/skills`,
  `.claude/skills`, roster extras, and stale role outputs). Interpretation:
  dropping the emission job leaves the existing `skills/skills.nota` file as an
  orphan in primary; it must be deleted by hand (jj-tracked).
- `manifests/active-outputs.nota:75-84` — Role records have shape
  `(Role (output-id role-source-module-id [included-modules] [desc] [surfaces]))`.
  Every role currently includes only `[agent-output-protocol]`. No role includes
  any skill-discovery module.
- `roles/scout/full.md` (and the other 9 role source modules) contain **no**
  reference to `skills.nota` and **no** skill-discovery instruction. Confirmed by
  `rg` over `roles/` returning only one unrelated hit (`repo-scaffolder/full.md:33`
  "test discovery"). Interpretation: the intent "discovery moves into role
  packets" is not yet implemented anywhere — it is net-new wiring.

### Authoritative contract surfaces in primary (must edit)

- `AGENTS.md:8` — "Read `skills/skills.nota`. It is the only default discovery read."
- `AGENTS.md:18` — "`skills/skills.nota` is the discovery path. Query it by topic; do not scan `skills/`."
- `AGENTS.md:58` — "Rust editing requires the Rust skills selected from `skills/skills.nota`."
- `ARCHITECTURE.md:48` — tree line "`skills/skills.nota`     the typed skill index".
- `INTENT.md:199` — new-role narrative: "...queries `skills/skills.nota` for the closest existing role-skill...".
- `skills/skills.nota` — the file itself; **git-tracked** (`git ls-files skills/`
  lists `skills/skills.nota` and `skills/generated-role-outputs.nota`). 17,902 bytes.

### Generator-owned surfaces (must edit, then regenerate)

- `src/assembly.rs` — emission + expected-output + (now-dead) SkillIndex code (lines above).
- `tests/generation.rs:37-38` — asserts the generated `skills/skills.nota` contains a specific record. Breaks.
- `tests/generation.rs:410` and `:428` — check-mode tests write `skills/skills.nota` as a fixture. Need updating.
- `skills.md:12` — "Primary discovery currently emits `skills/skills.nota` from the manifest." (generator doc prose)

### Generator skill-module prose referencing skills.nota (propagates into primary `.claude/skills` and `.agents/skills`)

These are prose mentions, not wiring. They reach primary because the generator
assembles them into `.claude/skills/<name>/SKILL.md` and `.agents/skills/<name>/SKILL.md`
(both surfaces are materialized in primary; sample paths resolve).

- Discovery-coupled (must rewrite — they describe the index as the discovery/single-source surface):
  - `modules/skill-editor/full.md:53,63,80,102` → emitted to `.claude/skills/skill-editor/SKILL.md:58,68,85,107`.
  - `modules/helper-context-transfer/full.md:25` ("skills named by the task, the role, or `skills/skills.nota`") → `.claude/skills/helper-context-transfer/SKILL.md:30`.
- Pedagogical (uses skills.nota as the canonical NOTA example — breaks "open skills.nota and read three records" once the file is gone):
  - `modules/nota-design/full.md:9,154,285,333` → `.claude/skills/nota-design/SKILL.md:14,159,290,338`.
  - `modules/nota-schema-docs/full.md:79` → `.claude/skills/nota-schema-docs/SKILL.md:84`.

### The dispatch boilerplate ("Read AGENTS.md and skills/skills.nota")

- Negative evidence: `rg` for the boilerplate phrasing ("Read AGENTS.md and
  skills", "select any additional triggered", "additional triggered skills")
  across primary (excluding reports/agent-outputs) and the generator returned
  **no committed source**. It is not in `orchestrate/AGENTS.md`, not in any skill
  module, not in any role packet.
- Interpretation: the boilerplate is a **lead-typed convention** (the brief that
  launched this scout is an instance of it), anchored only by the `AGENTS.md`
  startup contract. "Fixing the boilerplate" therefore means rewriting the
  `AGENTS.md` startup contract (the source of the habit); there is no generated
  template file to patch.

### Non-authoritative / scratch (note only, no action)

- `context.md` (primary root) lines 4,5,102,112,153,174,201 — transient
  Pi-vs-Codex context-budget investigation notes, including
  `"command": "read AGENTS.md and skills/skills.nota"` at line 174. Not a
  contract.
- `reports/**` — many historical mentions; report-naming discipline says do not
  retro-edit landed reports. Leave.
- generator `AGENTS.md` points at primary `AGENTS.md` + repo `skills.md`, not at
  `skills.nota` directly. No edit needed beyond `skills.md:12`.

### Cross-repo consumer outside the brief scope — BLOCKER: mentci

`mentci` is an active repo (`protocols/active-repositories.md:72`). It hard-wires
the literal string `skills/skills.nota` as the scaffold "expansion index" and
**validates it**, so deleting the file silently points mentci-launched sessions
at a missing file, and mentci's own check still demands the exact string:

- `/git/github.com/LiGoldragon/mentci/src/preflight.rs:525-527` — returns
  `Error::PreflightLaunch("scaffold expansion index must be skills/skills.nota")`
  unless `expansion_index == "skills/skills.nota"`. Hard enforcement.
- `/git/github.com/LiGoldragon/mentci/src/preflight.rs:243` — scaffold prompt
  text: "The scaffold must stay minimal and use skills/skills.nota as the
  expansion index."
- `/git/github.com/LiGoldragon/mentci/src/bin/mentci-claude-proof-test.rs:291,296,327`.
- `/git/github.com/LiGoldragon/mentci/schema/preflight-launch.nota.md:83,102`.
- `/git/github.com/LiGoldragon/mentci/ARCHITECTURE.md:94,283`.
- `/git/github.com/LiGoldragon/mentci/INTENT.md:72`.
- Tests: `tests/harness_sessions.rs:135`, `tests/harness_adapters.rs:111,503`,
  `tests/preflight.rs:43,73,95,132,148,206,216`.

This is neither primary nor the skills generator, so it is outside the stated
scope, but the deletion is **not safe** until mentci's expansion-index target is
re-pointed (or made configurable). Surfaced as a required follow-up, not applied.

## Deletion consequences (what depends on the index, what breaks)

1. **The boot/lead session** boots from `AGENTS.md` → reads `skills/skills.nota`.
   This is the only default discovery read (`AGENTS.md:8`). Deleting the file
   with no replacement leaves the lead and any ad-hoc primary session with **no
   discovery surface**. Role packets do not help here: the lead session has no
   packet.
2. **Role/worker sessions** today rely on the lead pasting the boilerplate
   "Read AGENTS.md and skills/skills.nota". Once discovery is in packets, workers
   are covered — but only after the packets actually carry it (currently they do
   not; see facts above).
3. **The generator** breaks immediately: emission site, expected-outputs entry,
   and three tests reference the path; `check-skills` and `generate-skills` would
   fail or drift until updated.
4. **Generated skill bodies** in primary (`.claude/skills/skill-editor`,
   `nota-design`, `nota-schema-docs`, `helper-context-transfer`, plus `.agents/skills`
   mirrors) carry prose that names the index as the canonical example / single
   source; those instructions go stale/dangling.
5. **mentci** (cross-repo) breaks: scaffolds point at a missing file and its own
   preflight validation hard-requires the exact string (BLOCKER above).
6. **Doc surfaces** (`ARCHITECTURE.md:48`, `INTENT.md:199`, generator `skills.md:12`)
   describe a file that no longer exists.

## Replacement discovery mechanism — options + the one decision

Role packets solve discovery for spawned **roles**. The unsolved surface is the
**lead/orchestrator lane and ad-hoc primary sessions**, which boot from
`AGENTS.md` and have no packet. The options differ in how that surface discovers
skills.

- **Option A — Harness-injected skill registry (no workspace file).** Rely on the
  harness's own skill list. Evidence this is viable: the Claude Code harness
  already injects an available-skills block (a `<system-reminder>` listing every
  skill name + description — present in this very session). AGENTS.md would point
  to "the harness skill list" instead of a file.
  - Pros: zero file to maintain; always current; matches the delete-the-index
    intent exactly; no generator emission needed.
  - Cons: format/availability is harness-specific (Claude injects it; Pi/Codex
    behavior must be confirmed per `context.md` notes); AGENTS.md can no longer
    cite a concrete path; the NOTA tier metadata (Apex/Keystroke/Topic/Mechanism)
    is lost unless folded into descriptions.

- **Option B — Per-role curated skill list baked into each packet.** Generator
  emits, per role, the relevant skills (names + triggers), plus a dedicated
  **lead/orchestrator** packet that carries the broad index for the boot session.
  - Pros: precise, minimal context per worker; deterministic; lead packet
    replaces skills.nota for the boot session.
  - Cons: duplicates skill descriptions across packets; requires new generator
    schema (per-role skill lists) and a new lead role; biggest build.

- **Option C — Lighter generated index retained for the lead only.** Replace the
  17.9 KB `skills.nota` with a slim generated index (name + one-line + tier, or a
  markdown table) that only the lead/ad-hoc session reads; workers get discovery
  from packets.
  - Pros: smallest contract change; keeps one stable discovery surface; keeps tier
    metadata.
  - Cons: contradicts the literal intent ("delete the index"); still a generated
    file to maintain.

**The ONE decision the psyche must make:** *What is the discovery surface for the
lead/orchestrator lane and ad-hoc primary sessions that are not launched with a
role packet?* — (A) the harness-injected skill list is authoritative and
AGENTS.md points to it; (B) a dedicated lead/orchestrator role packet carries the
curated discovery; or (C) a slim generated index is kept for the lead only.
Everything else in the change-list is mechanical once this is chosen.

## Concrete deletion change-list (PLAN — not applied)

Ordered so nothing is left dangling. Assumes the psyche picks a lead-discovery
option above; steps marked [A]/[B]/[C] vary by that choice.

### 1. Generator source (`/git/github.com/LiGoldragon/skills`) — land first

1. `src/assembly.rs:254-258` — remove the hard-coded `skills/skills.nota`
   `Rendered` job.
2. `src/assembly.rs:383` — remove the `expected.insert("skills/skills.nota")`.
3. `src/assembly.rs:993-1067` — delete `SkillIndex`, `SkillIndex::render`,
   `ActiveSkill::index_record`, and (if now unused) `SkillCategory::as_str` /
   `SkillTier::as_str`. Verify `active_skills()` still has consumers; if the index
   was its only consumer, prune accordingly.
4. `tests/generation.rs:37-38` — remove/replace the index-content assertion.
   `tests/generation.rs:410,428` — drop the `skills/skills.nota` fixtures.
5. `skills.md:12` — delete the "Primary discovery currently emits
   `skills/skills.nota`" line; replace with the chosen mechanism description.
6. [B] Add generator schema + emission for per-role skill lists and a
   lead/orchestrator role; wire each Role's `included_modules` in
   `manifests/active-outputs.nota`. [C] Replace the index job with a slim-index
   job. [A] No new emission.
7. Rebuild + `cargo test`; run `check-skills` against primary to confirm no drift.

### 2. Primary contract + docs

1. `AGENTS.md` Startup section (lines 6-14) — rewrite. Proposed shape for Option A:
   replace "Read `skills/skills.nota`. It is the only default discovery read."
   with a pointer to the harness-injected skill list (and, if kept, the
   per-role packet discovery for spawned roles). Remove the "do not scan
   `skills/`" index sentence.
2. `AGENTS.md` Skill Index section (lines 16-19) — delete or rewrite to name the
   replacement surface.
3. `AGENTS.md:58` — change "the Rust skills selected from `skills/skills.nota`"
   to "the Rust skills" (selected via the replacement surface).
4. `ARCHITECTURE.md:48` — remove the `skills/skills.nota` tree line (keep
   `skills/<name>.md` and `skills/generated-role-outputs.nota`).
5. `INTENT.md:199` — reword the new-role narrative to drop the
   `skills/skills.nota` query, pointing at the replacement.
6. Delete the file `skills/skills.nota` (jj-tracked deletion; the generator
   pruner will not remove it). Keep `skills/generated-role-outputs.nota`.

### 3. Regenerate primary skill surfaces

1. After the generator lands, edit the prose modules so emitted skill bodies stop
   citing the deleted index:
   - `modules/skill-editor/full.md:53,63,80,102` (single-source/index claims).
   - `modules/helper-context-transfer/full.md:25` (discovery reference).
   - `modules/nota-design/full.md:9,154,285,333` and
     `modules/nota-schema-docs/full.md:79` (pick a new canonical NOTA example, or
     reference `skills/generated-role-outputs.nota`).
2. Run `generate-skills` against primary; confirm `.claude/skills/*` and
   `.agents/skills/*` no longer reference `skills.nota`; `rg` to verify zero hits
   outside reports/context.md.

### 4. Cross-repo follow-up (BLOCKER — schedule before/with deletion)

- `mentci`: re-point or parameterize the scaffold expansion index
  (`src/preflight.rs:243,525-527`, `mentci-claude-proof-test.rs:291,296,327`,
  `schema/preflight-launch.nota.md:83,102`, `ARCHITECTURE.md:94,283`,
  `INTENT.md:72`, and the named tests). This is its own repo's work; deleting
  `skills/skills.nota` in primary without it breaks mentci-launched sessions.

### 5. Leave as-is

- `context.md` (scratch) and `reports/**` (historical) — no edits.

## Checks run and exact result

- `git ls-files skills/` → `skills/generated-role-outputs.nota`,
  `skills/skills.nota` (confirms the index is tracked; deletion is a tracked op).
- `ls .agents/skills/component-triad/SKILL.md` and
  `ls .claude/skills/component-triad/SKILL.md` → both resolve (both skill
  surfaces materialized in primary; index record paths are valid today).
- `rg` boilerplate phrases over primary+generator (excluding reports/agent-outputs)
  → no committed dispatch-boilerplate source found.
- `rg "skills\.nota|skills/skills" /git` → complete generator + mentci inventory
  above.

## Unknowns / not checked

- Whether the Pi and Codex harnesses inject an equivalent skill registry to
  Claude's (Option A viability beyond Claude). `context.md` references Pi's
  `skills.ts`/`formatSkillsForPrompt`, suggesting Pi does surface skills, but the
  exact shape was not verified in this scout.
- Whether `active_skills()` has any consumer besides `SkillIndex` after removal
  (needs a quick compile check during implementation; flagged in step 1.3).
- mentci's own intent: whether the expansion index should be re-pointed,
  removed, or made configurable is a psyche/mentci-lane decision, not settled
  here.
- Generated-output drift: I did not run `check-skills`; the emitted
  `.claude/skills` prose was read directly and matches the modules.

## Output

This file: `/home/li/primary/agent-outputs/RoleSkillReview/Scout-SkillsNotaDeletionPlan.md`
