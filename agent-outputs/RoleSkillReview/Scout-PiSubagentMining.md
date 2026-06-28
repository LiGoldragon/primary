# Scout: Pi-Subagent Mining (full-body review of 8 bundled subagents)

## Task and scope

Read the FULL body of all 8 subagents bundled by `pi-subagents` 0.31.0, and for
each recommend exactly one of ADOPT-as-is / MINE-substance / IGNORE against our
own 10 V1 generated roles. Specifically resolve the bundled-`scout` vs
project-`scout` precedence, assess `oracle` and `delegate` as new-role vs
skill candidates, and flag substance that should become a SKILL vs a ROLE.

This is a READ-ONLY proposal. The only file written is this one.

## Files and commands consulted

Bundled agents (active 0.31.0 store path, identical bytes across the 0.31.0
store paths `12kywv69…`, `2fbpkcdc…`, `x4wv0rk3…`; `2fbpkcdc…` is the one
symlinked from `~/.pi/agent/packages/pi-subagents`):

- `…-pi-subagents-0.31.0/share/pi-packages/pi-subagents/agents/scout.md`
- `…/agents/oracle.md`
- `…/agents/delegate.md`
- `…/agents/worker.md`
- `…/agents/context-builder.md`
- `…/agents/planner.md`
- `…/agents/researcher.md`
- `…/agents/reviewer.md`
- Package `…/share/pi-packages/pi-subagents/README.md` (precedence sections, lines 441-452 and 693-715)

Our surfaces:

- `/home/li/primary/.pi/agents/scout.md` (and the other 9 emitted roles in that dir)
- `/home/li/primary/skills/generated-role-outputs.nota` (generator emits `.pi/agents/scout.md`)
- Absence checks: no `/home/li/primary/.pi/settings.json`; no `scout`/`agentScope`/`disableBuiltins`/`agentOverrides` entries in `~/.pi/agent/settings.json`.
- Prior scout map: `/home/li/primary/agent-outputs/AgentProtocolDesign/Scout-HarnessAgentDiscovery.md`

## Scout collision finding (precedence resolved from source)

RESOLVED from the package README, not guessed.

README "Agent locations, lowest to highest priority" (lines 441-452):
Builtin < Installed package < User < **Project** (`.pi/agents/**/*.md`).
Quoted: "Builtin agents load at the lowest priority, so a user or project agent
with the same name overrides them." And line 450: "If both `.agents/` and the
project config agents directory define the same parsed runtime agent name, the
project config directory wins. Use `agentScope: "user" | "project" | "both"` …
`both` is the default and project definitions win runtime-name collisions."

Therefore our `/home/li/primary/.pi/agents/scout.md` (Project scope)
deterministically **shadows** the bundled `scout` whenever a launch resolves the
name `scout`. There is no project `.pi/settings.json` and no user
`agentOverrides`/`disableBuiltins`/`agentScope` override, so the default
`agentScope: both` applies and the project definition wins. The generator
(`skills/generated-role-outputs.nota`) emits `.pi/agents/scout.md`, so this
collision is produced on every regeneration.

Consequence: the collision is benign for correctness (our richer Scout wins) but
the bundled `scout` recon persona — the `context.md` handoff output, the
`# Code Context` / `Files Retrieved` / `Start Here` template — becomes
**unreachable by name**. If we ever want the bundled recon behavior we must
either rename ours, name the bundled persona differently, or `disabled`-gate.
This is a conscious-design choice, not an accident, and is acceptable as-is.

How to verify live (not done here; no live Pi session was spawned): inside a
trusted Pi session run `subagent({ action: "list" })` and confirm a single
`scout` entry sourced from project scope, or run `/subagents-doctor`. The
precedence is already proven from README + source; the live check only confirms
the runtime honors it in this workspace.

## Per-agent recommendation table

| Bundled agent | Recommendation | Our nearest counterpart | One-line justification |
|---|---|---|---|
| scout | MINE-substance | `scout` (ours wins; bundled shadowed) | Ours is richer (facts/interps/unknowns + output protocol); mine only the "Start Here: first file to open" pointer and strict line-range citation. |
| worker | MINE-substance | general-code-implementer | Strong role craft to fold in: "single writer thread", smallest-correct-change, escalate-don't-silently-decide, no-success-summary-without-edits, compact result shape. |
| reviewer | MINE-substance | rust-auditor / nix-auditor | Genuine gap: bundled reviewer is a *generalist* across diffs/plans/proposed-solutions/codebase-health/PR; we only have domain code auditors. Mine the 5-type review taxonomy. |
| planner | MINE-substance (heavy overlap) | intent-translator + bead-weaver | Overlaps our dependency-graph translation; mine only per-task **Acceptance** field + explicit **Dependencies** section. |
| context-builder | MINE-substance | intent-translator / scout | Mine the "meta-prompt as compact contract" handoff shape (goal/evidence/success/hard-constraints/validation/stop-rules) and "follow imports/callers/tests, don't stop at first symbol". |
| researcher | IGNORE (already covered) | `deep-research` skill | Web fan-out research is already a SKILL; researcher also needs the separate `pi-web-access` package. Nothing new to add as a role. |
| oracle | MINE-substance → propose ROLE | none | Most novel; no counterpart. Forked-context drift/consistency auditor against inherited decisions. Real gap; worth a role + supporting skill. |
| delegate | MINE-substance (config only) → fold into SKILL, not a role | `fork` / general-purpose helper | Cheap inheriting helper is a spawn-config primitive, not a discipline; covered by our fork helper + when-to-use-helpers. Don't add as a generated role. |

## Mined-substance list (the specific ideas worth carrying)

### From `worker` → into the general-code-implementer ROLE
- "You are the single writer thread" — a clean framing that one implementer owns
  the edit, decision authority stays with lead/psyche.
- Escalation contract: when implementation reveals an unapproved product/
  architecture/scope decision, **pause and escalate**, do not silently patch
  around it with an implicit decision. (We have escalation language; this
  sharpens the "silent decision is the failure mode" point.)
- Anti-false-success rule: "If your delegated task expects edits and you have
  not made them, do not return a success summary." Directly useful against
  agents that report done without editing.
- Compact final-result shape: `Implemented X / Changed files / Validation /
  Open risks / Recommended next step` — terse, matches our evidence-return goal.

### From `reviewer` → SKILL or new generalist-reviewer ROLE
- The five review types as a checklist: (1) code diffs, (2) **plans**,
  (3) **proposed solutions**, (4) **overall codebase health/drift**, (5) PR/issue
  root-cause. Types 2-4 are absent from our role set (we have only Rust/Nix code
  auditors). This is the clearest gap surfaced by the package.
- "Repo-local `progress.md` is allowed scratch — do not flag it as repo noise."
- Conflict-resolution rule: "review-only/no-edit wins over progress-writing."

### From `context-builder` → SKILL (fold into intent-led-orchestration / when-to-use-helpers)
- "Meta-prompt as a compact contract": goal, context/evidence, success criteria,
  hard constraints (true invariants only), suggested approach, validation,
  stop/escalation rules, resolved questions/assumptions. This is a crisp
  worker-brief envelope and maps onto our helper-dispatch discipline.
- Scouting craft: "read every file needed — follow imports, callers, tests,
  fixtures, configuration, docs — not just the first matching symbol." Worth a
  line in our scout role.

### From `planner` → fold into intent-translator / bead-weaver (already skills)
- Per-task **Acceptance** ("how to verify") attached to every numbered task.
- Explicit **Dependencies** section naming which tasks block which.

### From `oracle` → SKILL (drift-check method) + propose ROLE (forked auditor)
- Core method worth capturing as discipline: reconstruct the inherited
  decisions/constraints/open-questions and treat them as the **authoritative
  contract**; detect **drift** between current trajectory and that contract;
  surface contradictions and hidden assumptions; "protect consistency over
  novelty"; exploit a **clean forked context** to catch context-rot errors the
  lead can no longer see; when recommending a pivot, name exactly which prior
  decision is being revised.
- Output shape: Inherited decisions / Diagnosis / Drift-contradiction check /
  Recommendation / Risks / Need-from-main / Suggested execution prompt.

### From `delegate` → SKILL note only (when-to-use-helpers / helper-context-transfer)
- The minimal inheriting-helper config pattern: `systemPromptMode: append` +
  `inheritProjectContext: true` + `inheritSkills: false` + no default reads +
  inherits parent model — a cheap fan-out worker when full role personas are
  overkill. This is a spawn option, not a discipline.

### From `scout` (bundled) → our scout ROLE (minor)
- "Start Here: name the first file another agent should open and why" — a single
  high-value pointer at the end of a recon map.
- Strict exact-path + line-range citation when quoting code.

## SKILL vs ROLE flags (answering brief item 3)

- **oracle** → both. The drift/consistency-check *method* is SKILL material; the
  forked-context *auditor* is a candidate ROLE because it needs
  `defaultContext: fork` spawn semantics (a role/config capability, not just
  prose). Strongest single addition the package suggests, because our system is
  intent-led: an oracle-style role naturally checks the active trajectory
  against captured **Spirit intent records** (drift between work and psyche
  intent) — a gap nothing in the current 10 roles fills.
- **delegate** → SKILL/spawn-config note, NOT a new generated role. The
  capability is already met by our `fork`/general-purpose helper plus
  `when-to-use-helpers`. Adding it as a 11th generated persona would add a role
  with almost no body (the bundled file is ~2 sentences).
- **reviewer generalist taxonomy** → either a SKILL (review checklist consumed
  by existing auditors/oracle) or a new generalist-reviewer ROLE. Lean SKILL
  first; promote to ROLE only if plan/solution/health review proves to need its
  own spawn persona distinct from the domain auditors.
- **context-builder meta-prompt contract** → SKILL (brief-writing envelope),
  fold into `intent-led-orchestration` / `when-to-use-helpers`; do not add a
  role (it overlaps intent-translator + scout).
- **worker craft** → ROLE refinement of general-code-implementer (no new skill).
- **planner acceptance/dependency** → fold into existing intent-translator /
  bead-weaver skills.

## Interpretations vs facts

- FACT: precedence (project beats builtin) from README lines 441-452, 450.
- FACT: our generator emits `.pi/agents/scout.md`; no overriding settings exist.
- INTERPRETATION: the oracle role being "worth introducing" is a recommendation,
  not an accepted decision. Per the agent-output protocol, all role-set changes
  here are provisional proposals for the psyche, not new authority.

## Checks run (exact)

- `ls` of bundled `agents/` across store paths: 8 files, byte-identical between
  the three 0.31.0 paths.
- `rg` over README for precedence/override/discovery: matched lines 120-146,
  441-452, 460-485, 697-715.
- `ls /home/li/primary/.pi/settings.json` → "No such file or directory".
- `rg 'scout|disableBuiltins|agentScope|disabled' ~/.pi/agent/settings.json` → no matches.
- `rg` of `generated-role-outputs.nota` → confirms `.pi/agents/scout.md` is emitted.

## Blockers, unknowns, follow-ups

- NOT CHECKED live: no Pi session was spawned, so `subagent({ action: "list" })`
  / `/subagents-doctor` precedence behavior is proven only from README + source,
  not observed at runtime. Verify live before relying on the shadow being exactly
  as documented.
- The `researcher` builtin requires the `pi-web-access` package; whether that is
  active was noted in prior scouting (`pi list` showed `packages/pi-web-access`
  active) but not re-verified here.
- Whether to add an oracle role and/or a generalist-reviewer role is a psyche
  decision; this file only proposes.
