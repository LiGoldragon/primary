# Context handover — skills and roles redesign

Written 2026-07-25 at the psyche's instruction, to restart this thread in a fresh
session. The vision section is the load-bearing part; everything below it is
state.

## Vision

**An instruction earns its place only by changing behavior.** The test is
unusualness. Agents already behave in the usual way, so a line that matches what
an agent would do untold changes nothing. The unusual line is the load-bearing
one, and it is the one to cut last.

**A rule needs evidence.** Write a rule only when it prevents a failure that has
actually happened, or states a choice an agent cannot derive. Name the incident
or the choice. If you can name neither, do not write the rule. Imagined failures
produce prohibitions against things nobody was going to do.

**Minimalism means cutting what carries nothing.** It never means compressing
what carries something into a tautology. Commit `7f5753642f1d` (2026-07-20,
"skills: reduce reusable guidance") deleted 87% of the doctrine corpus —
roles 519 lines to 78, skills 4371 to 568 — and it deleted the load-bearing
specifics first, because a reserved-keyword list looks like noise next to a
sensible-sounding generality. That commit is the cautionary case for this whole
effort. The pre-transition content is at `7f5753642f1d^`.

**Three destinations for every line.** Skills carry behavior. Standards carry
domain facts. Everything else is over-instruction and goes. Models are capable
now; telling a 2026 model what it already does is waste, not safety.

**Agents are capable inferrers.** Do not spell out a link a reader can make.
Consistent terminology connects surfaces on its own; naming the connection is
noise. This applies to enforcement too — a rule about editing files already
covers the shell that edits them.

**Do not ask a worker to do accounting.** The dispatcher judges what the work
needs; the psyche decides what that costs. Putting cost into a selection surface
degrades both the selection and the work. Ask a painter to price the paint and
you get a worse painting.

**Repositories are independent.** Each documents itself. Do not document another
repository's internals from outside it. Skills name capabilities; workspaces name
the implementations that fill them.

**Do not fake a component with a hand-maintained file.** `protocols/repos-manifest.nota`
declared itself the authoritative repo inventory, was parsed by nothing, and had
drifted to 128 records against 166 real checkouts within 24 days of creation.

**The psyche owns doctrine.** Agents may flag harmful or unclear guidance. They
do not infer authority to rewrite it. When in doubt, leave it empty.

**Never pretend to know.** Admit what you do not know. Do not relay a subagent's
conclusion as fact without checking it.

## Style the psyche wants

- Plain sentences. No antithesis, no inverted pairs, no matched clauses, no
  aphorism. A line built for rhetorical effect reads as settled and conceals
  what it failed to specify.
- Every line directs an action. Rationale and justification are not doctrine.
- One rule per line. Never pair a goal with a mechanism — the reader cannot tell
  which one binds.
- Give a reference the reader can check against. "Decide ordinary things
  yourself" is useless; "the brief is your authority" is checkable.
- Concrete over abstract, always.

## Style the psyche rejects, in his own words

- `Do not publish private material.` — "this is stupid. do not try to swallow
  your tongue, and do not kill your family."
- `Review Rust changes and their evidence.` — "Might as well say 'audit rust'."
- `Preserve external names only at their boundary.` — confusing noise; the
  reader must guess what it governs.
- `Verify whether the remote exists before creating one.` — "dont smash your
  head against the wall?"
- `including through the shell` — telling a capable model what it infers.
- A cost marker in a role description — the painter and the paint.

He caught rhetorical shape in my drafts three separate times after I had proposed
the rule against it. Watch for it.

## How he works

He iterates by rejection. He does not approve drafts; he attacks the weakest line
until what remains is right. Expect that, and put the actual text in front of him
rather than describing it.

He punishes both failure modes: asking when the answer is derivable, and acting
on inference where he has not decided. The line is that routine judgment is
yours, and anything he would want to rule on is his. When unsure, deliver
everything that does not depend on the question, then ask.

He does not want ceremony around mistakes. Correct and continue.

## What landed

Skills repo `LiGoldragon/skills`, commits `b1e7e80f` and `a908323b`.
Primary, commits `fc7b5a57` and `37425e1f`. Standards repo `LiGoldragon/standards`,
commits `e541828fd0fa` and `d0691c225269`. All pushed.

**Roles: 14 authored prose files replaced by 8 generated cells.** A role is a
permission crossed with a depth and nothing else. Domain was never a role
property; that was the error being corrected.

| depth | Claude | OpenAI |
|---|---|---|
| trivial | `claude-haiku-4-5` (no effort) | `gpt-5.4-mini` medium |
| ordinary | `claude-sonnet-5` medium | `gpt-5.6-luna` high |
| demanding | `claude-sonnet-5` high | `gpt-5.6-terra` high |
| critical | `claude-opus-5` high | `gpt-5.6-sol` medium |

`xhigh` is the ceiling; `max` is not used. Manifests: `role-permissions.nota`,
`role-depths.nota`, `role-descriptions.nota`. Deleted: `role-model-assignments`,
`role-model-profiles`, `role-optional-skills`, `nested-role-relations`.

Descriptions are the selection surface and are written as tests the dispatcher
can answer about a task before starting — for example `write-demanding`: "The
approach has to be chosen, or the change spans surfaces that must agree."

**Skills: 65 to 49.** Deleted: `context-maintenance-deep`, `reporting`,
`privacy`, `prose`, `repo-intent`, `session-archive-garbage-collection`,
`intent-clarification`, `intent-maintenance`, `intent-manifestation`, `secrets`,
`helper-context-transfer`, `design-quality`, `mermaid`, `micro-components`,
`push-not-pull`, `spirit-cli`, `spirit-query`. Added `psyche-vision`.
`skill-designing` gained the cut-list and keep-list guards.

**Standards repo** gained `mermaid-syntax.md`, `naming.md`, `micro-components.md`
recovered verbatim from `7f5753642f1d^`, plus `unsorted.md` for substance with no
home yet. Standards take no frontmatter.

**AGENTS.md** gained the ghq root binding and the standards repo location.

## Open, needing the psyche

1. **48 to 23 skill deletion.** Proposed and unruled: delete `abstractions`,
   `library`, `code-implementation`, `engine-report`; move to standards then
   delete `naming` (already duplicated), the four `rust-*`, the six `nota-*`,
   `component-architecture`, `contract-repo`, `enum-contact-points`,
   `actor-systems`, `structural-forms`, `typed-records-over-flags`,
   `protos-syntax`; merge `session-lanes` into `edit-coordination`,
   `pi-internals` into `pi-extension-updates`, and cut
   `release-train-development` down to its own lines.
2. **`nix-usage` and `nix-discipline` merge into one**, with much of the content
   moving to standards. Stated but not executed.
3. **Serious redesign, not trimming**, of: `version-control` (he called it
   useless), `testing`, the merged Nix skill, `operating-system-operations`,
   `disk-hygiene`, `work-tracking`, `main-feature-integration` (better name, or
   merge), `intent-log`. `intent-log` is the largest job — it is the universal
   entry to the intent system, needs a much better explanation of what qualifies
   as intent, and must filter heavily *out*: most things do not qualify.
   Refine `versioning` and `engine-analysis`. `helper-context-transfer` is gone;
   the vocabulary is "subagent", not "helper".
4. **NOTA optional-effort encoding.** Shipped as `(claude-haiku-4-5 None)` /
   `(gpt-5.4-mini (Some Medium))`. Alternative is `[]` / `[Medium]`, which admits
   an invalid two-effort state.
5. **Read permission is unenforced on Codex.** Claude gets `disallowedTools`,
   Pi gets `disallowed_tools`, `.codex/agents/*.toml` has no tool field. The
   restriction there is prose only.
6. **`psyche-vision` shipped with the mechanical description** `Psyche vision
   rules.` — the exact garbage this effort exists to remove.
7. **Nothing tells a writing agent how to register a lane.** The literal
   `meta-orchestrate` invocation was stripped from `edit-coordination` in favour
   of naming the capability, and never placed anywhere. The natural home is the
   orchestrate repo's own README.
8. **14 orphaned `RoleComposition` modules** — `edit-coordination-core`,
   `editing-closeout`, `non-ideal-registry`, `rust-core`, `intent-core` and
   others — are called by nothing since roles stopped inlining doctrine.
9. **Skill descriptions are still generated from the name** — `'Mermaid rules.'`
   The `description` field must become authored source, saying when the skill
   applies. This is the field the harness uses to decide whether to load a skill.
10. **The Spirit daemon is down** — `spirit-daemon.service` inactive since
    2026-07-24, `spirit-judge.service` failed, socket refuses connections.
11. **A workspace convention with no home:** Technology and Software are the
    Spirit domains this workspace's records live under. Not a property of Spirit,
    so it belongs with the AGENTS.md bindings.
12. **Worktrees are being created inside the ghq owner directory** — 211
    directories against 166 `ghq list` entries. This actively obstructed a
    dependency survey.

## Research already paid for, still unconsumed

`agent-outputs/` holds substantial commissioned research that never reached the
corpus. Read it before re-deriving any of this:

- `ExternalAgentResearch/Scout-ResearchBase.md` — 567 lines, 60 sourced references.
- `SkillsRolesCritique/Scout-Critique.md` — 228 lines. Thesis: the important
  orchestration choices are carried by prose, with no deterministic dispatch
  machinery or evaluation to prove they happen well.
- `SkillBenchmark/Researcher-PublicPatterns.md` — "Always-loaded rules should be
  limited to safety, workspace invariants, delegation boundaries, and output
  contracts."
- `SkillDoctrineV2/SkillEditor-CorpusTriage.md` — "a skill is justified by
  preventing real workspace errors, not by existing."
- `YoutubeSkillDoctrine/ScoutVideoDoctrineReport.md` — progressive disclosure,
  steps-versus-reference structure.
- `RoleSkillReview/IntentTranslator-RoleSkillAssignment.md` — contains the open
  question "NAME versus INLINE" addressed to the psyche and never answered. It
  is now answered: NAME.

## My own failures this session, so they are not repeated

- Relayed a subagent's claim of a contradiction in the standards repo without
  checking it. There was none — the subagent reproduced a misreading that the
  document itself records and corrects, and I passed it on as fact.
- Wrote rhetorical, aphoristic lines repeatedly after proposing the rule against
  them.
- Invented a failure mode (a race between two agents cloning the same repo) one
  message after proposing that rules require real incidents.
- Raised a false alarm that the skill corpus had collapsed, from a partial tool
  listing, without counting first.
- Proposed a cost marker in a role description, which is the accounting error.
