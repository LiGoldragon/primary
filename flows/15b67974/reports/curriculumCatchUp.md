# Curriculum catch-up to psyche — full proposal

Bring Curriculum into line with every standing psyche ruling that bears on
it. Standing frame: Curriculum stays hand-maintained until the flow Nexus
replaces what it does; this catch-up is not that rewrite — it removes
everything already ruled dead so the eventual rewrite starts from a clean
floor.

## The end shape: two inputs

**`skills/`** — authored `*.md` runtime skills only. Presence is
registration: every file in the directory deploys; the filename is the
identity and the source path. No manifest entry, no category, no tier, no
target-surface field, no module kind — none of these carried live
information.

**`roles.dotos`** — one file of its own (name proposed) holding everything
role-shaped that lives:

- the eight subagent roles — read/write × trivial/ordinary/demanding/
  critical — each carrying its description text and its model + effort
  binding directly (no separate model catalog, no depth-axis machinery:
  depth is in the role's name and its binding; permission is read vs write
  in the name);
- the three Codex aliases ("the codex aliases are still useful");
- the two role-composition modules (today distinguished from runtime
  skills only by the manifest's module-kind field): their `.md` sources
  move out of `skills/` to live beside the roles file and are referenced
  from it — otherwise presence-is-registration would deploy them as
  skills.

## What is deleted

- All ten `manifests/*.dotos`.
- Curriculum's own `.agents/` and `.claude/` trees — generated output in
  the source repo, violating the 2026-08-10 source-only ruling.
- Every text-assertion test: the registration check
  (tests/generation.rs:344 asserting literal manifest text) and its
  siblings. All source-searching tests are forbidden. What remains is
  behavioral: run the generator, compare generated output against authored
  source (check mode / flake check) — the one place text assertion is
  legitimate, because there the text is the product.
- The elaborate-phase leftovers: `skill-module-compositions.dotos`
  (empty), `module-dependencies.dotos` (restates the filesystem).

## Skills inventory at cutover

33 authored `.md` files today: 29 registered runtime skills, 2
role-composition modules (move out, above), 2 unregistered files.

- `lojix.md` — stays and deploys; already registered this week. The
  superseding strata ruling holds: skills are the current gateway to the
  agent-accessible mid stratum, so component references belong here, not
  in their component repos.
- `nix-input-upgrade.md` — an unfinished 28-line draft ending
  mid-sentence. Under presence-is-registration it would deploy broken.
  Decision for the psyche: finish it before cutover, or move it out of
  `skills/` until finished.

## Generator

Input: a scan of `skills/` plus `roles.dotos`. Output: unchanged consumer
surfaces — `.agents/skills/` and `.claude/skills/` skill files, the role
packets across `.claude/`, `.codex/`, `.pi/` agents, the role inventory.
A `Requires: X` dependency renders as "requires X" in the dependent
skill's description and nothing else, as already ruled. Invocation
unchanged: `nix run .#generate-skills` / `.#check-skills` from the
consumer workspace.

## Sequencing

Codex is actively committing to Curriculum (test cleanup, skill
registrations). Propose: implementation lands as a dedicated realization
flow (tracked as primary-cnp) after the current Codex pass, jj-coordinated;
the flow also removes the generated trees and dead tests in the same
change so the repo is consistent at every commit.

## Open inside this proposal

1. The roles file's name and format (`roles.dotos` proposed).
2. Where the two role-composition module sources land (beside the roles
   file proposed).
3. `nix-input-upgrade.md`: finish or park.
4. Launch timing relative to Codex's current pass.

## Sources

- psyche/Vision/skillsRepository.md — 2026-08-21 (kill the manifest;
  generate from present files; roles in a file of their own) and
  2026-08-22 entries (most system-wide machinery dead; codex aliases still
  useful; not orphan skills).
- psyche/Vision/skillsRepoSourceOnly.md — 2026-08-10 (source-only),
  2026-08-14 (requires X in the description, nothing else).
- psyche/Vision/testTravesties.md — 2026-08-20 (no grep-style tests; text
  asserted only where text is the product), 2026-08-22 (all
  source-searching tests forbidden).
- psyche/Vision/domainKnowledgePlacement.md — 2026-08-22 (strata: skills
  are the gateway to the mid stratum).
- psyche/Vision/flowDaemon.md — 2026-08-19 (Curriculum rewritten as a
  Nexus eventually; hand-maintained until flow replaces it).
- reports/CurriculumManifestMap-2026-08-21.md — witnessed manifest
  decision inventory, generator shape, test sites, orphan census.
- Flows: e06e4c07 (parent design flow), 15b67974 (this flow; rulings and
  landings), 5c8be3ca (flows protocol).
