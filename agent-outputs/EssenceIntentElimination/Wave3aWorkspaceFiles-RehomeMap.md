# Wave 3a — Workspace-File Elimination + Rehome Map

Handoff artifact for the skills worker and the closeout wave. Wave 3a executed
the WORKSPACE-FILE half of the ESSENCE.md / workspace-INTENT.md elimination
(beads D2 `primary-euru`, D3 `primary-5vjc`, D4 `primary-1dux`, AGENTS.md
portion of D1 `primary-fc70`).

## Scope and boundaries

- Touched only workspace files. Did NOT touch skill source, `.claude/skills`,
  `.agents/skills`, or generated role packets — those are the skills worker's.
- Did NOT `jj` commit or push — closeout wave commits the whole working copy.
- Did NOT inspect `private-repos/`. `repos/`-scoped content left to the per-repo
  deferred bead.

## Re-inventory correction (audit was partly wrong)

- Actual `ESSENCE.md` had **8 headings**: Intent is the cornerstone; Inferring
  intent is forbidden; What I am building; What I am not optimising for; Beauty
  is the criterion; Naming; Backward compatibility is not a constraint.
- **No "Today and eventually" section existed in ESSENCE.md.** Its citations in
  `active-repositories.md` were already dangling/phantom.
- **No "Polling is forbidden" section existed in ESSENCE.md.** The no-poll
  doctrine lived in `INTENT.md` §"Push, not poll" ("Polling design is
  forbidden."). The audit's claim that a "Polling is forbidden" section was in
  ESSENCE.md was inaccurate.
- Actual workspace `INTENT.md` had 21 headings.

## REHOME MAP (section -> new durable home)

### From ESSENCE.md

| Section | New home |
|---|---|
| Intent is the cornerstone | `ARCHITECTURE.md` §0.5 "The intent layer" + `intent-log`/`intent-clarification`/`intent-manifestation` skills |
| Inferring intent is forbidden | `ARCHITECTURE.md` §0.5 "The intent layer" + intent skills |
| What I am building | `ARCHITECTURE.md` §0.5 "### What the workspace is building" |
| What I am not optimising for | `ARCHITECTURE.md` §0.5 "### What the workspace is building" (priority list + not-optimised-for) |
| Beauty is the criterion | `beauty` skill (already carries it); one-line pointer in ARCHITECTURE.md vision |
| Naming | `naming` skill (already carries it); ARCHITECTURE.md §Constraints citation repointed to the skill |
| Backward compatibility is not a constraint | `ARCHITECTURE.md` §0.5 vision paragraph + `versioning`/`feature-development` skills |

### From workspace INTENT.md

| Section | New home |
|---|---|
| Push, not poll / Polling design is forbidden | **`ARCHITECTURE.md` STABLE anchor `### Push, not poll`** (skills worker repoints push-not-pull SKILL here) |
| What the workspace is building (Persona) | `ARCHITECTURE.md` §0.5 "### What the workspace is building" |
| Intent is primordial / The intent layer / Spirit gate / Guidance lean | `ARCHITECTURE.md` §0.5 "### The intent layer" |
| Two deploy stacks coexist / Where work happens | already lives in `active-repositories.md` (Replacement Stack §"Two deploy stacks coexist") |
| Today/eventual scope (implied) | `ARCHITECTURE.md` `### Today and eventually — different things, different names` |
| BEADS transitional / workspace-truth-in-files / Nix-store-not-search / roles-loose | already reflected in `ARCHITECTURE.md` §§4–6 and `AGENTS.md`; no new content needed |
| Language-is-data / compiler-build-time / role-is-type / recompiling / new-roles-auditor | cite Spirit records + per-repo nota/schema surfaces; left to per-repo deferred bead (repos/ scoped OUT) |

## Load-bearing anchors created (for downstream repoints)

- **`ARCHITECTURE.md` `### Push, not poll`** — the push-not-pull skill citation
  (`.agents/skills/push-not-pull/SKILL.md` line 8 `ESSENCE.md §"Polling is
  forbidden"`, line 36) must be repointed here by the skills worker. Note the
  old citation named a heading ESSENCE never actually had; the new anchor is
  §"Push, not poll".
- **`ARCHITECTURE.md` `### Today and eventually — different things, different
  names`** — already repointed from all three `active-repositories.md`
  citations (lines 33, 98, 220).
- **`ARCHITECTURE.md` `## 0.5 · Workspace vision and intent`** — durable home
  for vision + intent framing.

## Files edited / deleted

- DELETED: `ESSENCE.md`, `INTENT.md` (jj working copy: D)
- EDITED: `ARCHITECTURE.md` (added §0.5; removed ESSENCE/INTENT file-tree
  entries; repointed TL;DR, precedence chain, Boundaries-owns, Naming citation,
  Invariants-upstream, See-also; fixed stale See-also `lore/ARCHITECTURE.md` ->
  `lore/AGENTS.md`)
- EDITED: `protocols/active-repositories.md` (3 `ESSENCE §"Today and eventually"`
  citations -> `ARCHITECTURE.md §"Today and eventually"`)
- EDITED: `orchestrate/AGENTS.md` (claim-flow example `repo INTENT.md` ->
  `repo ARCHITECTURE.md`)
- VERIFIED CLEAN, no edit: `AGENTS.md` (thin boot contract; zero ESSENCE/INTENT
  authority framing, no INTENT.md first-read mention)

## Grep evidence — workspace-file half is clean

Fresh sweep (excl reports/repos/private-repos/target/agent-outputs/.git/.jj):
the only remaining live `ESSENCE.md`/`INTENT.md` references in WORKSPACE files
are intentional — ARCHITECTURE.md prose naming the eliminated files and the
new "Today and eventually" anchor, plus active-repositories.md citations now
pointing at ARCHITECTURE.md. Every other remaining hit is in a
**skills-worker-owned** surface.

## REMAINING for skills worker (NOT this wave)

Repoint/recast these (and reconcile generated `.claude`/`.agents`/`.codex`/`.pi`
copies):

1. `push-not-pull/SKILL.md` lines 8, 36 — `ESSENCE.md §"Polling is forbidden"`
   -> `ARCHITECTURE.md §"Push, not poll"`.
2. `intent-clarification/SKILL.md` line 9 — recast `ESSENCE.md … source of
   authoritative direction`.
3. `repo-intent/SKILL.md` — per-repo INTENT.md eliminated; home is repo
   `ARCHITECTURE.md`/code stub (D1).
4. `architecture-editor/SKILL.md` — name ARCHITECTURE.md/code-stub as the
   intent/vision/telos home (D1).
5. `intent-manifestation/SKILL.md` — reroute durable content off INTENT.md (D1).
6. Role packets `.claude/.codex/.pi/agents/{intent-maintainer,repo-scaffolder}`
   reference repo `INTENT.md` — reconcile per D1.

## FLAG (ambiguous home, resolved without inventing controversy)

- "Today and eventually": the active-repositories.md citations referenced an
  ESSENCE section that **did not exist** in the actual file. Rather than invent
  a controversial home, I created a `### Today and eventually` anchor in
  ARCHITECTURE.md carrying the exact scope-discipline doctrine that already
  lives verbatim in active-repositories.md's "Current Truth Pins" (lines
  215–222), and repointed the citations to it. If the psyche prefers this
  doctrine live solely inside active-repositories.md (self-citing), the
  ARCHITECTURE.md anchor can be dropped and the 3 citations repointed locally —
  surfacing this as the one place a content owner might want a different call.

## Bead status

- D1 `primary-fc70`: AGENTS.md portion DONE (verified clean, no edit); note
  added listing the 6 skill/role items remaining for the skills worker. Bead
  stays OPEN for the skills portion.
- D2 `primary-euru`, D3 `primary-5vjc`, D4 `primary-1dux`: workspace-file work
  COMPLETE; could not `bd close` because the dependency guard holds on open D1
  (and D4 on D2/D3). Completion evidence recorded as notes on each. They are
  ready to close once D1 closes — closeout wave or skills worker should close
  the chain (or `--force` D2/D3/D4 once D1's skill portion lands).
