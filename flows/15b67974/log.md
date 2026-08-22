# Design flow 15b67974 — continuing e06e4c07: actor land, Curriculum reorganization, skill lines, distillation into flows

Rulings landed over 2026-08-21/22, all logged verbatim in psyche/Vision: no
arc-mutex ban ever existed; the actor subject gets a dedicated zero-trust
flow — distrust all prior actor work including our kameo fork (actorLibrary);
Curriculum manifests die — skills generate from the present files, subagent
roles in a file of their own, and most of the system-wide machinery is dead
too (skillsRepository); lojix and nix-input-upgrade are not orphan skills;
flow launches an existing harness for now, our own 100%-typed-datom harness
later (flowDaemon); hexis architecture review in its own flow (hexis);
persona dormant yet slated to orchestrate the meta harness (persona);
persona-spirit abandoned, spirit to be abandoned for psyche
(spiritComponentAndFile); the momentum assumption thoroughly disproven
(flowKnowledge); old code is possible inspiration, not evidence, for the map
(worldModelBeforeCode); nexus/software-design overlap ignorable, probable
merge (skillDesigning); psyche logging into the flow protocol + more
frequent distillation with a per-flow distilled file — under consideration
(psycheLogStructure).

## Delivered

Reports (reports/, 2026-08-21): CurriculumManifestMap (18 manifest decisions;
per-skill layer inert; registration grep test tests/generation.rs:344),
ActorLibraryNexusSkillReview (kameo 0.20.0 via LiGoldragon fork, 21 repos,
hexis on ractor; nexus skill documents none of it), KameoForkReview (fork
2026-06-19 off v0.20.0; terminal-lifecycle system has no upstream
equivalent; upstream 5 releases ahead), PersonaSpiritVsSpirit (ten
capabilities stranded in abandoned persona-spirit; spirit has no kameo;
psyche repo an empty scaffold).

Skill landings: four testing lines verbatim (Curriculum 3629e2c9, primary
951081cc, deployed copy witnessed); vocabulary liability sentence removed
(d76600ff, bf49a189); skill-designing cut-line and nexus porting-sentence
cut found already true — the porting sentence was cut by e06e4c07's own
evening regeneration (17bd79d3, primary generated trees; authored-source
history unwitnessed).

Findings: Curriculum contains .agents/ and .claude/ trees, violating the
2026-08-10 source-only ruling — removal noted on primary-cnp.

Artifacts: Curriculum Pipeline
(https://claude.ai/code/artifact/d2720739-fe7b-476d-9f9f-e6db76487748),
August 21 Design Board
(https://claude.ai/code/artifact/225d0be5-89ee-4118-855e-e757fce842a0).

Beads: created primary-z0r (hexis review), primary-uxf (actor flow — carries
the zero-trust ruling and both actor reports), primary-cnp (Curriculum
reorganization); closed stale primary-ky7 (training rename, superseded).

## Settled 2026-08-22 afternoon

- Roles file: 8 subagent roles (model bindings + text) PLUS the codex
  aliases ("the codex aliases are still useful"); everything else dead.
  Reorganization shape complete on primary-cnp.
- lojix.md stays a deployed skill: superseding strata ruling
  (domainKnowledgePlacement 2026-08-22) — "skills are the current gateway
  to agent-accessible mid stratum"; docs-live-in-domain predates the
  strata realization. Codex may lack a mid-layer interface; own/modified
  harness possibly needed.
- Nexus line LANDED and witnessed in the deployed skill (Curriculum
  1fa939a8, primary regen 469512d1, both pushed): "A port starts from the
  map of what is being created; old code is at most inspiration for that
  map." — traits section, between reuse-or-extend and the exceptions
  paragraph.
- Kameo settled as the actor layer in nexus ("definitely using kameo
  actors"); undesigned part is the standards of use — actor flow scope
  refined on primary-uxf.
- Psyche-logging protocol ruled: psyche/Vision/<topic>.md = home of
  distilled psyche going forward; raw psyche in flows/*/psyche/; on
  distillation raw logs move to an archive- prefixed file in the same
  directory (psyche-archive/ superseded). Logged in psycheLogStructure.

## Open

- Cutover timing for raw psyche logging (flows/*/psyche/ now vs when the
  skills carry it) + pronouncement mechanics of distillation proposals —
  asked.
- Psyche-logging skill edits: missing pieces inventoried for the psyche —
  raw-file shape inside flows/<id>/psyche/; old-corpus archive- handling;
  distilled-entry reference format (left ambiguous 2026-08-14, 06196cc7
  L694 "this is also ambiguous. id is repeated"); proposal staging;
  skill-ownership split (standalone distillation skill still unlanded —
  fb1008c0 mission, 7c3f0c1d draft stopped mid-read); non-primary-workspace
  flows' raw psyche home. Sprawl confirmed: 7801001a (08-07 roots),
  steward 08-09/10, 012fbf07, 06196cc7, fb1008c0, 1030529c, d2bb5f5f
  (referenced, never mined — acquisition dispatched), 7c3f0c1d, this flow.
  Codex-side sessions outside the transcript tool's scope.
- Acquisition returned: d2bb5f5f holds NOTHING on the subject (it is the
  Spirit-reform session; the 08-14 reference was a misremembering, already
  verified in-session at 06196cc7 L646). fb1008c0: nothing uncaptured.
  06196cc7: one flag — the draft principle "agent annotations are not
  records" got "I dont understand" (L716 opening) and was never ratified;
  reconstructed into psycheLogStructure.md at its chronological place.
  Missing-pieces list grows to seven (annotations-principle ratification).
- Reorganization launch sequencing vs active Codex work in Curriculum —
  asked.
- nix-input-upgrade.md fate — folded into primary-cnp.
- Universal nexus traits (e06e4c07's thread): untouched.

## 2026-08-22 late afternoon

Distillation defined by the psyche (logged, psycheLogStructure): a
distilled record is self-standing, clarified and purified by the model,
always explicitly reviewed by the living psyche; agglomerates records
across flows on one topic, favoring recency and certainty on conflict.
Closes missing piece 7 (context lines are understanding input; the
distilled output stands alone).

Curriculum catch-up proposal written on psyche request:
flows/15b67974/reports/curriculumCatchUp.md — two inputs (skills/ +
roles.dotos), full deletion list, cutover inventory, generator shape,
sequencing; four open sub-decisions. Pointed from primary-cnp. Awaiting
green.

## Notes

Reconciled 2026-08-22: sessions/design/15b67974.md (diverged superset per
annotations.md, 5c8be3ca entry) merged into this log and removed. Machinery:
orchestrate lane registration refuses its documented template ("expected
LaneRegistrationRequest to be a brace block") — claims this flow are
unregistered, advisory only. bd auto-export intermittently warns "git add
failed" — notes verified landing regardless.
