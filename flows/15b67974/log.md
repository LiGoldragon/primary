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

Proposal 1 reshaped by psyche (logged psycheLogStructure + spirit,
2026-08-22 16:47): a skill is still a file; the "distilled psyche"
description untrue until the corpus is distilled — rename the current
corpus directory, encourage distillation into the new location; the flow
subdir is vision/ (we log psyche *vision*); top-level psyche/ maybe
unnecessary — distillation into typed Vision/ and Intent/ (caps leaning);
spirit treated specially: live in entry-files' top section stating
spirit's absolute primacy (codex puts skills in mid stratum only with
manual $ prefix). Forks posed: corpus rename name; caps confirm; raw
intent captured as vision; spirit skill's fate beside entry files.
Proposals 1–4 rework after forks; proposal 5 (session-log retirement)
stands.

Forks RULED (16:55, all logged): psyche-raw/ good; case split liked; raw
intent and spirit only from the living ("the living" coined as shorthand
— letsUseTheSameVocabulary); spirit skill retires only when generated
entry files carry spirit — kept now, machinery deferred; entry-file
complete takeover with @-prefixed workspace-specific secondary files
(same stratum) — deferred direction, logged in entryFiles. Proposal set
rewritten FINAL: reports/psycheLoggingSkillEdits.md — six proposals
(psyche skill incl. "or the living"; psyche-interraction vision/ logging;
flows vision/ anatomy; psyche-distillation skill; session-log retirement;
vocabulary "The living" entry) + cutover = batch landing + psyche-raw
rename with reference sweep. GREEN RECEIVED ("all good. implement and
deploy now") — implementation worker dispatched: six Curriculum edits +
authored-skill reference sweep + regeneration + primary cutover (psyche/
→ psyche-raw/ rename, entry-file reference updates, no empty Vision/
Intent/ created). From the landing on, this flow logs raw psyche in
flows/15b67974/vision/.

LANDED AND LIVE (Curriculum ebba084a + cc71bf56, primary 67e7690b, all
pushed): psyche skill five-item homes list + "or the living";
psyche-interraction vision/ logging; flows anatomy vision/<topic>.md;
psyche-distillation created, registered in the (still-extant) manifests,
deployed — body witnessed verbatim by this flow; vocabulary "The living"
entry; session-log authored source already absent (no-op). Sweep: only
psyche.md and psyche-interraction.md carried path references. Cutover:
psyche-raw/ rename tracked as renames; CLAUDE.md:18,
NON_MANAGEMENT_AGENTS.md:43, AGENTS.md:18 now say search Vision/,
psyche-raw/, flows/*/vision/. CUTOVER IS LIVE — raw logging here goes to
flows/15b67974/vision/ from now on.

Skill-edit proposal set written on psyche request:
flows/15b67974/reports/psycheLoggingSkillEdits.md — five proposals with
exact wordings: psyche skill Where-psyche-lives rewrite (Vision =
distilled, flows/*/psyche/ = raw); psyche-interraction Logging paragraph;
flows anatomy gains psyche/<topic>.md; new psyche-distillation skill
(settled rulings only, open mechanics left out); session-log skill
retirement. Cutover proposed = the batch's landing. Awaiting green.

## Notes

Reconciled 2026-08-22: sessions/design/15b67974.md (diverged superset per
annotations.md, 5c8be3ca entry) merged into this log and removed. Machinery:
orchestrate lane registration refuses its documented template ("expected
LaneRegistrationRequest to be a brace block") — claims this flow are
unregistered, advisory only. bd auto-export intermittently warns "git add
failed" — notes verified landing regardless.

## Summary

Continues design flow e06e4c07. Psyche direction at start: (1) the Arc/Mutex-ban
approach is disliked; review the actor library we use and whether it is well
documented in the nexus skill. (2) Re the registration check: get rid of the
Curriculum manifest and generate whatever skills are present; the elaborate
abandoned phase's artifacts (e.g. breakup into modules) are unwanted.
(3) Mid-turn: testing skill lines approved verbatim ("A new test is seen
failing once before it is trusted. ... no order between them.") — "this is
good, we can land it".

## State

All three dispatches delivered. Testing lines LANDED: Curriculum 3629e2c9
(skills/testing.md, four lines appended verbatim, no existing text altered),
primary 951081cc (regenerated via SKILLS_WORKSPACE_ROOT=/home/li/primary
nix run .#generate-skills, exit 0), both pushed; deployed skill witnessed by
this flow carrying the four lines verbatim. Note: a duplicate generator run
from the GitHub URL also exited 0; its writes are an unread claim.

Transcript context recovered (e06e4c07 L963, L990): the Arc<Mutex> ban is an
agent-created grep-over-source test (persona/tests/actor_discipline_truth.rs);
the registration check is a Curriculum test asserting the manifest text
contains a skill's entry; the four testing lines were proposed at L990.

Rulings logged: testTravesties (four lines approved verbatim, "this is good,
we can land it"); actorLibrary (new topic — approach disliked; review the
actor library we use and its nexus-skill coverage); skillsRepository (get rid
of the manifest, generate whatever skills are present; module breakup was the
bad approach).

Dispatched: (1) land the four testing lines in the Curriculum testing skill
source, regenerate, push; (2) actor-library review →
reports/ActorLibraryNexusSkillReview-2026-08-21.md; (3) Curriculum manifest
mechanism map → reports/CurriculumManifestMap-2026-08-21.md (delivered, see below).

Manifest map delivered (reports/CurriculumManifestMap-2026-08-21.md): ten
manifests/*.dotos decide 18 things. Per-skill: only active/inactive is a real
decision — identifier and path are filename-determined; category/tier parsed
but produce no output; target surfaces uniform; module kind separates 2
role-composition modules from 29 runtime skills; 29 of 33 on-disk skill .md
registered, 2 orphans (lojix, nix-input-upgrade). System-wide (would remain
as config regardless): model catalog, permissions axis, depth axis, role
descriptions, aliases, universal role modules, target insertions.
skill-module-compositions.dotos is empty; module-dependencies.dotos restates
the filesystem. Registration check = tests/generation.rs:344-353 asserting
literal "[general-instructions]" in universal-role-modules.dotos. Generator:
one DOTOS arg, reads Curriculum + ten manifests, writes 58 skill files +
27 role packets + inventory into consumer trees; nix run .#generate-skills /
.#check-skills.

Actor-library review delivered
(reports/ActorLibraryNexusSkillReview-2026-08-21.md): kameo 0.20.0 via org
fork LiGoldragon/kameo (lifecycle/shutdown customizations), 21 repos depend;
hexis is the outlier on ractor 0.15. Supervision diverges: persona manual
lifecycle, persona-spirit full kameo supervision trees. The only two
Arc<Mutex> in production are intra-actor (persona direct_process.rs:202
StopHandoff; persona-spirit actors/dispatch.rs:62 SharedTrace), not
inter-actor shared state. Reply pattern split (Result vs derive(Reply))
uncodified. Nexus skill names none of this — kameo not even named; nine gap
items listed in the report.

Psyche answered the four forks (2026-08-21 ~13:00): (1) "there is no ban of
arc mutex. the whole actor subject deserves its own discussion in another
flow" — logged in actorLibrary.md; (2) wants the manifest situation shown
visually — artifact "Curriculum Pipeline" published
(https://claude.ai/code/artifact/d2720739-fe7b-476d-9f9f-e6db76487748) from
the manifest-map report: today/after diagrams, 18 decisions split per-skill
vs system-wide, leftovers, the config-home fork; (3) asked for the kameo
divergence explained — explanation given in conversation (no ruling sought,
actor discussion deferred to its own flow); (4) asked to see the batched
edits — shown verbatim from e06e4c07 L609/L495.

## Open, awaiting the living psyche

- Manifest removal scope: all of manifests/ (config moves, home to be named)
  vs per-skill layer only (slimmed config file stays). Visual delivered.
- Batched skill edits awaiting green: vocabulary drop "A flow is liable for
  its subflows."; skill-designing add under Cut these: "A line that restates
  a rule another skill holds."; nexus keep/cut: "Porting existing code uses
  extraction — lifting the latent trait out of the method name."
- e06e4c07 Question 1 (does flow launch an existing harness with a composed
  system prompt, or run its own model loop) — restated to the psyche.
- Actor subject: awaits its own dedicated flow per ruling; the review report
  is its starting ground.

## Open

- Roles-file cut: psyche says most of the seven system-wide decisions are
  dead machinery; the live-core question (are the 8 subagent roles with
  their model bindings the whole file?) is posed.
- lojix / nix-input-upgrade nature: not orphan skills; identification read
  dispatched.
- Amended nexus line awaiting green: "A port starts from the map of what is
  being created; old code is possible inspiration, never the source of
  traits."
- Kameo identity line for nexus withdrawn — actor lines belong to the actor
  flow under the zero-trust ruling.
- Distillation-into-flows anatomy: questions posed (raw records' home,
  distilled file's role, archive's standing).
- Universal nexus traits (e06e4c07's thread): untouched.

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

## 2026-08-22 late afternoon

Forks RULED (16:55, all logged): psyche-raw/ good; case split liked; raw
intent and spirit only from the living ("the living" coined as shorthand
— letsUseTheSameVocabulary); spirit skill retires only when generated
entry files carry spirit — kept now, machinery deferred; entry-file
complete takeover with @-prefixed workspace-specific secondary files
(same stratum) — deferred direction, logged in entryFiles. Proposal set
rewritten FINAL: reports/psycheLoggingSkillEdits.md — six proposals
(psyche skill incl. "or the living"; psyche-interraction vision/ logging;
flows vision/ anatomy; psyche-distillation skill; session-log retirement;
vocabulary "The living" entry) + cutover = batch landing + psyche-raw
rename with reference sweep. Awaiting green.
