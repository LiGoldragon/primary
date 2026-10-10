# Handover — Legacy-lane disposition → Spirit cleanup (2026-06-26)

Self-contained pickup for a fresh session. Read this, then
`spirit-cleanup-plan-2026-06-26.md` (the id-level plan) in this same dir.

## Essence

A request to "implement the weave" (dispose the backlog of agent-written legacy-lane
reports → beads/Spirit/drop) ran a 6-theme summary workflow, then the psyche pivoted
the energy into **cleaning Spirit itself**. The governing first-degree principle that
emerged: **Spirit stores only durable intent/direction.** Anything that *describes how
Spirit/the system works* → a **manual**; any *config/operational fact* → an
**architecture file**; both come OUT of Spirit. Skills are NOT the destination (don't
bloat them); the new semi-standard is a simple **manual** (single `manual.md` or a
book-style dir). Execution is APPROVED. No Spirit mutations have happened yet — the
store is intact (649 active / 739 Zero).

## Psyche's verbatim words (load-bearing — also the guardian testimony for retires)

- Original: "deploy a workflow to implement the weave. agents should make a summary of
  the topics so we can decide what needs to be addressed (put into beads) and what is
  durable intent (put into spirit)"
- Routing calls: #1 cloudflare "this kind of stuff belongs in architecture files, not
  spirit" · #2 immich "again, not spirit content" · #3 d3r2 "not spirit material" ·
  #4 asschema "yes, remove asschema entries"
- "Spirit is intent, not architecture facts" → "for spirit's manual"
- The pivot: "this stuff doesnt belong in spirit. it *describes spirit* to the user.
  you dont store the manual in the database. all this kind of stuff out of spirit,
  into the docs"
- Borderline policy: "aggressive"
- "those zero records should be garbage collected (they can be archived first)"
- Destinations: "lets make a manual in the spirit repo." / "just use the architecture
  file or create a manual (single manual.md or a directory)" / "no necessarily. we
  dont want to bloat our skills. consider architecture and manual files (new
  semi-standard is the manual - something simple for now...)" / "I approve with my
  corrections"

## What is DONE (persisted)

1. **Theme decision surface** — `reports/legacy-disposition/decision-surface-2026-06-26.md`:
   52 untracked topics across 6 themes (T1 Cloud/Lojix-VM · T2 Schema/Spirit/Sema ·
   T3 Criome/Router/Mentci · T4 Governance · T5 Hardware-Ops · T6 Research-Media),
   tagged 37 work / 6 intent / 9 drop. The 6 intent items were all adjudicated (below).
   **The 37 work beads + 9 drops are NOT yet routed — parked thread.**
2. **Full Spirit classification** — `reports/legacy-disposition/spirit-cleanup-plan-2026-06-26.md`:
   all 649 active records bucketed KEEP 575 / TO-MANUAL 57 / TO-ARCH 10 / STALE 7
   (after the aggressive borderline call). Exact id-lists + doc map + Spirit command
   templates are in that file. 739 records already at Zero (removal-nominated).
3. **Spirit manual drafted** — `/git/github.com/LiGoldragon/spirit/manual.md` (276 lines,
   8 sections, covers 23 Spirit-mechanism records, synthesized prose, no `---`).
   **UNCOMMITTED. No records retired.** Awaiting psyche review before commit + retire.
4. **Memory** — `~/.claude/projects/-home-li-primary/memory/spirit-holds-intent-only.md`
   (the boundary principle) + MEMORY.md index recreated (it was missing on disk).

Primary working copy is UNCOMMITTED (the two `reports/legacy-disposition/*.md` files +
this handover). The spirit-repo manual is uncommitted in that repo.

## OPEN FORKS (awaiting psyche)

1. **Spirit manual review** → on the psyche's go: commit `manual.md` in the spirit repo
   + retire the 23 records (`7hrd qjrf tfpd mrsy j6r4 g78b yenl rvnf nr7h vjye 7xnx
   kasm dfii i59i oj3i t4uq qbx7 fiw4 rh29 8jtz 6z6t tbg6 l7kt`; rvnf covers the
   zt1-4/ztX dup-cluster). Retire/Supersede ARE recognized guardian ops — confirm the
   guardian accepts the retire pattern on the FIRST record before batching.
2. **739-record GC is BLOCKED (decision needed): defer+track vs fix-now.** See below.

## The GC blocker (real guardian bug, source-confirmed)

`CollectRemovalCandidates` (archive-then-remove) is deployed in the schema and the
daemon routes it through the guardian, BUT the guardian instruction prompt
(`/git/github.com/LiGoldragon/spirit/src/guardian-prompts/` — checklist.md/few-shot.md/
role.md) never lists it in its op vocabulary, so the guardian remands it as
"unrecognized." Second issue: querying the full 739-set overflows the guardian LLM call
(fails >~60 records) → needs batching by Kind (Decision 313/Principle 171/Correction
105/Clarification 90/Constraint 60; Importance=Minimum alone = 602/739, so may need
Kind×Importance split). The guardian's fallback (per-record `Remove`) is a HARD delete
with no archive — rejected, contradicts "archive first." Nothing was touched.
- **Defer+track (lead's lean):** 739 already at Zero (hidden, harmless); file the
  guardian gap as a work bead; run archival GC once the guardian's fixed.
- **Fix now:** add the op to the guardian instruction prompt + redeploy the guardian,
  then run GC batched by Kind.

## REMAINING cleanup work (after the manual + its 23 retires)

- The other ~34 TO-MANUAL records (orchestration, reporting, NOTA/schema-grammar,
  vocabulary, concepts) → simple per-domain **manuals** (NOT skills) + retire. Grouping
  + ids in the plan file's "Execution grounding" section.
- TO-ARCH 10 config facts (`go41 nz0t upza osoo 16l0 nsi2 bdse p6k5 qxye bnxx`) → each
  component's ARCHITECTURE.md or a manual in its repo (CriomOS-home, persona, spirit,
  cloud — create where missing; `cloud` has no symlink; `bnxx` → workspace-vocabulary).
  Psyche resolved the earlier "untracked-repo" worry: just put them in the component's
  arch/manual file.
- STALE 7: `6cfr a9sq hc0t` → Supersede preserving the live SpecifiedSchema/codec rule
  (held in active `6grf`/`bkcd`/`kfqa`); `dqmc` → Retire; `zNEW9 ztA ztB` → hard Remove.
- The 37 work beads + 9 drops from the theme decision surface (parked).

## Method / protocol notes

- Active protocol: `skills/intent-led-orchestration.md` — gates: psyche explicitly
  locks alignment, THEN explicitly approves method/dispatch; a directive does NOT skip
  gates. Lead delegates meaningful reading to subagents (Main Thread Mode in AGENTS.md).
- Psyche style: plain, ONE genuine fork per turn; he answers tersely and fast and
  decides in parallel — don't batch questions. Recommendations only as candidates.
- Every Spirit mutation is guardian-gated and needs VERBATIM psyche testimony
  (paraphrase → MissingTestimony); affirmative framing (negation → NegativeGuideline).
  Encode embedded parens as NOTA pipe-text `[|...|]`.
- On primary: work on `main` via `jj` (see skills/jj.md); commit whole working copy.
  repos/ are untracked separate VCS (psyche authorized editing them for this).

## Immediate next actions for the fresh session

1. Get the psyche's read on `manual.md` → commit it in the spirit repo + retire the 23
   (test the first retire, then batch).
2. Get the GC decision (defer+track vs fix-now-guardian).
3. Then proceed through the remaining TO-MANUAL groups (manuals), TO-ARCH (component
   arch/manuals), STALE, and eventually the parked 37 work beads.
