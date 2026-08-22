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

## Open

- Roles-file cut: psyche says most of the seven system-wide decisions are
  dead machinery; the live-core question (are the 8 subagent roles with
  their model bindings the whole file?) is posed.
- lojix / nix-input-upgrade nature witnessed: lojix.md is a 408-line
  complete formal API reference for the Lojix deployment daemon (sockets,
  18 request families, replies, deployment contract, bootstrap);
  nix-input-upgrade.md is a 28-line unfinished draft of Nix flake-input
  upgrade wisdom, cutting off mid-sentence. Placement decision posed to the
  psyche under domainKnowledgePlacement ("docs live in the code they
  document"): lojix reference → Lojix repo; the draft's home open.
- Amended nexus line awaiting green: "A port starts from the map of what is
  being created; old code is possible inspiration, never the source of
  traits."
- Kameo identity line for nexus withdrawn — actor lines belong to the actor
  flow under the zero-trust ruling.
- Distillation-into-flows anatomy: questions posed (raw records' home,
  distilled file's role, archive's standing).
- Universal nexus traits (e06e4c07's thread): untouched.

## Notes

Reconciled 2026-08-22: sessions/design/15b67974.md (diverged superset per
annotations.md, 5c8be3ca entry) merged into this log and removed. Machinery:
orchestrate lane registration refuses its documented template ("expected
LaneRegistrationRequest to be a brace block") — claims this flow are
unregistered, advisory only. bd auto-export intermittently warns "git add
failed" — notes verified landing regardless.
