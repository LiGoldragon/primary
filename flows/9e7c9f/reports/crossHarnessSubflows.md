# Cross-harness subflows

Flow 9e7c9f, read-only subflow. Brief: gather every psyche record touching
cross-harness subflow launching, subflow identity, permission flags, and
main-flow/subflow skill training; give the flow accounts of what was decided
and what landed; and witness the currently installed skill state on both
harnesses. Claims are marked **witnessed** (this subflow read the file or ran
the command itself), **read** (this subflow read a cited source directly),
or **relayed** (carried from another flow's report/log without independent
re-verification by this subflow).

---

## 1. Raw psyche records

None of the records below appear in `Vision/` (checked: `grep -rl "subflow"
Vision/` returns nothing). **Every record in this section is still raw** —
none has been distilled into a landed Vision document. Where a record has
since been realized in a skill file (not a Vision distillation, but an
applied edit), this is noted separately in §2/§3.

### `flows/162eb3/vision/subflows.md` (the central record)

> ## 2026-09-10 — Launching subflows in the same harness
>
> Context: flow 857335, a Codex main flow, had launched its Sol audit as a separate `codex exec` process under systemd with a read-only sandbox instead of through its subagent tool; the flow asked why and no reasoning was recorded.
>
> > Okay, we need better training on how to launch subflows. Codex doesn't need another Codex to run ChatGPT models, and vice versa.
>
> -- psyche, typed.

> ## 2026-09-12 — A cross-harness invocation is still a subflow
>
> Context: asked whether a Codex flow launching `claude -p` for an Opus audit is still a subflow with the same liability and identity.
>
> > 1. yes, its still a subflow
>
> -- psyche, typed.

> ## 2026-09-12 — No sandbox, all permissions
>
> Context: asked whether the rule is "no restriction beyond what the brief states" after 857335 added `--sandbox read-only` on its own.
>
> > 2. no sandbox. all permissions. codex with "--sandbox danger-full-access --ask-for-approval=never" and claude with "--dangerously-skip-permissions" - but some of our wrappers might already add those flags. double check the status on that
>
> -- psyche, typed.

> ## 2026-09-12 — A different harness is invoked with the subflow training, not the main flow training
>
> Context: asked whether the launch rule goes in `main-flow` only or also in `subflow`. The psyche asked the flow to check that the statement makes sense.
>
> > 3. Well, if harness is launched as a main flow, the only way it would start using subflows is if it's loaded with the main flow skill. It's possible to do that, although I'm not sure I want to go down that route. Maybe we should also add into the main flow edit that you're suggesting that, when a different harness is invoked, it shouldn't be invoked with the main flow training, but with the subflow training rather, right?
>
> -- psyche, typed.

> ## 2026-09-12 — The main-flow skill is only ever typed into the prompt
>
> Context: the flow proposed a `subflow` skill sentence saying a nested cross-harness subflow "follows the same cross-harness rule as the main flow."
>
> > Well, there's one problem: the main flow should not be available for agents to load by themselves, so that it can only be typed into the prompt. Make sure that that's the case and that the way it's done works for both harnesses. If that's the case, then telling the subflow that something is like the main flow is useless.
>
> -- psyche, typed.

Status: raw. **Realized in a skill edit** (not a Vision distillation) by flow
f6db8d, Curriculum commit `2ef2b538f7efa9b7da4b98b98b1e9cb73c6f2fdf` — see §2
and §3.

### `flows/01a05e95/vision/subflows.md` — parent flow directory

> ## Parent flow directory
>
> > "I want subflows to use the parent flow directory ... We need to figure out how we can reliably create a situation where the subflows use the same flow ID as their parent for everything that they want to write."
>
> -- psyche, typed.

Status: raw. Realized in the installed `subflow`/`main-flow` skills (FLOW_ID/FLOW_DIRECTORY propagation), not distilled to Vision.

### `flows/01a05e95/vision/flowSkills.md` — main flow vs. subflow skill split, and visibility

> ## Main flow skill
>
> > "I think we should have some kind of a master flow or main flow skill that explains the part about using subflows. I think the skills are a bit misnamed. I think the flow skills should explain the whole protocol, both from the point of view of the parent and the child. They should be able to know that it's a child and how to behave."
>
> -- psyche, typed.
>
> ## Flow logging, flow directory, or flow files
>
> > "Maybe the flow protocol should be called Flow Logging or Flow Directory. It's more than just logging, where reports go and stuff like Flow Files. It explains that part, or maybe it explains it for the main flow, and that skill is not visible for agents. There's another smaller skill that explains it from the point of view of the subflow, which is visible for agents and which this subflow is told to read."
>
> -- psyche, typed.
>
> ## Main flow and subflow visibility
>
> > "Is the subflow not visible to agents? The skill that mandates using subflows for everything, we should basically use, and maybe rename that as Main Flow or something to explain everything that has to do with being the main flow."
>
> -- psyche, typed.
>
> ## Parent supplies the flow ID
>
> > "Perhaps the job of the main flow is to give all subflows the actual flow ID that they're supposed to use, so that they know where to put their files if they want to put reports or witnesses. I'm not saying they 100% should not. I think it's the job, like you said, of the main flow to decide whether or not it should be logged, so they shouldn't really be logging. They might want to put a report or witness, and that's where it should go."
>
> -- psyche, typed.

Status: raw. Realized (main-flow/subflow split, `main-flow` marked non-agent-loadable, subflow does not log/index) in the currently installed skills — see §3.

### `flows/01a04881/vision/subflows.md`

> ## "youre the one who can best guess why you did it, not another flow with a different context than yours"
>
> -- psyche, typed.

Status: raw, undated, no context recorded in the file itself.

### `flows/01a05826/vision/subflowIdentity.md`

> ## 2026-08-31T14:53:21.481Z — subflows use their parents' lanes
>
> > I guess we could also use session hooks, but it couldn't be a hook that also gets triggered by subflows, because then they get the same ID, and that would create a tension. I don't want subflows to start creating their own lanes. They just use their parents.
>
> -- psyche, typed.

Status: raw. Realized in the installed `subflow` skill ("Do not create a lane, index entry, or log").

### `flows/01a030df/vision/subagents.md`

> # must use subagents for all research, including openai
>
> ## 2026-08-24T01:08:51+02:00
>
> The living ruled:
>
> > remember that you must use subagents for all research, including openai.

Status: raw.

### `flows/5851f4/vision/subagents.md` — subagent models/effort/roles

> ## Default models for subagents
>
> Context: opening the flow, on the model the subagent roles default to.
>
> "I want to switch the default opus for your subagents to the latest version."
>
> -- psyche, typed.
>
> ## Sonnet too, effort medium everywhere, three roles
>
> Context: while subflows were out witnessing where the subagent default model is pinned.
>
> "and sonnet should also be the latest version. for claude. and all the effort levels everywhere should be medium, so we might only need 3 roles now instead of 4 for subagents."
>
> -- psyche, typed.
>
> ## Three roles on both sides, all medium effort
>
> Context: ruling on the questions about which role survives, effort on trivial, and whether "everywhere" covers the Codex aliases.
>
> "So now we can take out the critical role on both sides:
> - On the Claude side, we have Haiku, Sonnet, and Opus, all at medium effort: Haiku 4.5, Sonnet 5, and Opus 5.
> - On the codex side, we would also have three roles: Luna, Terra, and Sol [STT wrote "Soul"; the psyche later: "I never said Soul. That's the speech-to-text being defective"], all on the medium effort."
>
> -- psyche, STT.

Status: raw. Per flow f6db8d's own correction (`flows/f6db8d/log.md:29`), this record is **superseded** by flow 58a86d's Opus ruling only in the narrow sense of "avoid Opus 5 as interlocutor, not per se" — the three-role/medium-effort structure itself stands. See §2 for the live contradiction between `AGENTS.md`/`roles.datom` and this record on the Sol role that f6db8d flagged for the living.

### `flows/58a86d/vision/subagentModel.md` — Opus 4.6 not Opus 5

> ## 2026-09-05 — Opus 4.6, not Opus 5
>
> Context: the flow had offered Opus 5 for the demanding and critical subagent tiers, since no Opus 5.1 exists and those tiers are pinned to Opus 4.6.
>
> > I dont want opus 5, which is why I use 4.6
>
> -- psyche, typed.

Status: raw; predates and is qualified by 5851f4's later three-role Opus 5 ruling.

### `flows/58a86d/vision/codexModel.md` — Astra for the main flow only

> ## 2026-09-05 — Astra for the main flow only; subflows stay Luna and Terra
>
> Context: the flow had reported that GPT-6 Astra answers from the Codex login and asked whether it becomes the Codex main model.
>
> > Astra will be the main model, but only for the main flow. All subflows will still be Luna and Terra as they were before.
>
> -- psyche, STT.

Status: raw. Per f6db8d's tracking table (`reports/recent-vision.md:950`), the Astra half is **realized** (witnessed `/home/li/.codex/config.toml:4,11`, relayed by f6db8d) and the Sol half is **superseded** by `flows/5851f4/vision/subagents.md`; f6db8d flags a live contradiction between `AGENTS.md` and `roles.datom` on the Sol role that still needs the living.

### `flows/8a5caa/vision/codex.md` — explicit executables, full permission by default

> ## explicitly named executables
>
> On naming Codex launch commands:
>
> > what we want, which is explicitly named executables ... We shouldn't really have a wrapper.
>
> -- psyche, typed.
>
> ## all codexes to have full permission access
>
> > I would like all codexes to have full permission access, whatever flags they are. I think the dangerous set permissions or something like that. There are two flags. I think they're set now in the current wrapper, and I always want that enabled, but maybe there's a way to enable it somewhere else in the configuration file or something.
>
> -- psyche, typed.

Status: raw. Bears directly on the "double check the status on that" instruction in 162eb3's record #2 (wrappers add no flags; Codex's own `config.toml` already sets `danger-full-access`/`never` — see §3).

### `flows/38dec9/vision/skillLandingBySubflow.md`

> The psyche on having a subflow read the transcript and create/modify skill files from approved content, so the main flow doesn't waste context shuffling text.
>
> "If I approve them, you could set up some agent to just read your transcript and put these into files so we don't waste context for you to shuffle all this text around. Whatever you print in your response can be used by a subagent to create or modify the actual skill files and deploy them."
> -- psyche, STT.
>
> "This, I believe, is something that I wanted to develop into standard practice."
> -- psyche, STT.

Status: raw. Realized as standard practice: this is exactly the mechanism flow f6db8d used ("apply subflow" reading `skill-proposals.md` from its own transcript to produce `skill-edits.md`).

### `flows/01a0428b/vision/useASubflowToPutTheReportTogether.md`

> The living specified how this investigation and report should be carried out:
>
> > And what I would like, how I would like this to be done is because a subflow can actually read the transcript that it's here, it would be more efficient. I don't want the main flow to do a bunch of file files and code reading to just essentially repeat what's in its own context. So it would be better to use a subflow to put the report together. And then when doing something more script like that on the Codex side, we should use a terra model
>
> Provenance: Codex transcript `01a0428b-fc0e-7200-904e-2e2991e5425f`, line 9.
>
> ## I meant Terra for the report writing
>
> The living clarified the scope of the earlier model preference:
>
> > I didn't mean use terra for everything, I meant for the report writing
>
> This supersedes any reading of the earlier entry that selects Terra for investigation or other ordinary subflow work.
>
> Provenance: Codex transcript `01a0428b-fc0e-7200-904e-2e2991e5425f`, line 389.

Status: raw.

---

## 2. Flow accounts

### Flow 162eb3 — the ruling flow

`flows/162eb3/log.md`, 2026-09-12 entry (own words, relayed here verbatim):

> 2026-09-12 — The living ruled: subflows run through the harness's own subagent tool; a cross-harness invocation is still a subflow; no sandbox, all permissions; the main-flow skill is human-typed only on both harnesses. Vision logged in vision/subflows.md. Witnessed: wrappers add no permission flags (Codex user config defaults to danger-full-access; 857335 overrode it downward); Codex already gates main-flow via generated openai.yaml; Claude Code ignored `user-only`. Delegated the generator fix: curriculum-deploy 0.6.2 (c669b27b) rewrites `user-only: true` to `disable-model-invocation: true` for the Claude target. Regeneration of primary's trees is blocked by the in-flight Curriculum roles.datom migration (flow 542442, lock 851); live trees unchanged. Proposed main-flow and subflow skill lines await approval.

**This account is now stale on two points**, superseded by flow f6db8d (§ below):
the proposed lines were subsequently drafted with exact text, approved, and
landed; and the roles.datom-migration block has since cleared.

### Flow f6db8d — the skill-proposals flow that drafted, and then applied, the lines

`flows/f6db8d/reports/skill-proposals.md` (Wave 1, **proposal only, nothing
applied at the time it was written**) records the exact proposed text, §1
"`main-flow` — how a subflow is launched, and what a cross-harness launch
carries", grounded explicitly in `flows/162eb3/vision/subflows.md`:

- §1a, current `skills/main-flow.md` line 7:
  > Use subflows for investigation, implementation, probes, and verification.

  proposed:
  > Use subflows for investigation, implementation, probes, and verification, launched through this harness's own subagent tool.

- §1b, current `skills/main-flow.md` lines 25-27 (last line unchanged, quoted for context):
  > Tell subflows what is wanted, not how, unless the mechanism is explicit and witnessed.
  > A flow is liable for its subflows: what a subflow did, the flow did; asked how, it says it did it through a subflow.
  > Before the first flow artifact, run `flow-id claude --flows-root ABSOLUTE_DIRECTORY --parent-session "$CLAUDE_CODE_SESSION_ID"`.

  proposed (one line inserted between the second and third):
  > A model this harness cannot run is launched as a process of the harness that runs it, briefed as a subflow and never as a main flow; it is a subflow, with the same liability and the same flow identity. Launch it with no sandbox and every permission — `claude -p --dangerously-skip-permissions`, `codex exec --sandbox danger-full-access --ask-for-approval=never` — except where the installed wrapper or that harness's own configuration already supplies them.

- §1c, **deliberately not proposed**: no cross-harness sentence for `skills/subflow.md`, citing the "main-flow skill is only ever typed into the prompt" ruling — since `main-flow.md` already carries `user-only: true` (and `skill-designing.md` explains what that deploys to per harness), "the `subflow` skill gains nothing" from restating it.

`skill-proposals.md` also independently re-witnessed the "double check the
status on that" instruction: `claude` and `codex` are Nix wrapper scripts
that only prepend `PATH` (and, for claude, export
`DISABLE_AUTOUPDATER`/`DISABLE_NON_ESSENTIAL_MODEL_CALLS`/`DISABLE_INSTALLATION_CHECKS`);
**neither adds a sandbox or permission flag**; `~/.codex/config.toml` already
sets `approval_policy = "never"` and `sandbox_mode = "danger-full-access"`
(so the Codex flags are redundant but harmless); no `defaultMode`/
`bypassPermissions` key exists in either `~/.claude/settings.json` or
`/home/li/primary/.claude/settings.json`, so `--dangerously-skip-permissions`
must be passed explicitly for a `claude -p` subflow. This subflow
independently re-witnessed the same wrapper facts today (§3) and confirms
them unchanged.

Separately, `skill-proposals.md` Addendum "A10" proposed one line for
`skills/subflow.md`: release every lock before reporting finished — this is
the line now present as installed-subflow line 12, "Release every Orchestrate
Lock you hold before reporting the work finished."

**What landed**, from `flows/f6db8d/reports/skill-edits.md` (2026-09-12, "apply
subflow"): Curriculum commit `2ef2b538f7efa9b7da4b98b98b1e9cb73c6f2fdf`
applied §1a/§1b to `skills/main-flow.md` (3 lines +/-) and A10 to
`skills/subflow.md` (1 line +), among ten files (271 insertions, 320
deletions total). `flows/f6db8d/log.md` Wave 6: "Curriculum 2ef2b538 (…one
line each in main-flow, nexus, orchestrate, testing, file-editing, subflow),
AGENTS.md skill-loading paragraph, trees regenerated (check-skills
Checked.{44 21}; main-flow, design, realization now
disable-model-invocation)." Regeneration in primary: "24 files, 667
insertions, 760 deletions: `.agents/skills/` and `.claude/skills/` for the
ten edited skills, plus three files … `.claude/skills/design/SKILL.md`,
`.claude/skills/realization/SKILL.md` and `.claude/skills/main-flow/SKILL.md`
change `user-only: true` to `disable-model-invocation: true` …. `.codex/` and
`.pi/` are unchanged." This subflow independently confirms both the applied
skill text and the regenerated tree in §3 below.

**Curriculum-deploy 0.6.2 regeneration blocked by flow 542442 — has it since
happened? Yes.** `flows/f6db8d/log.md` Wave 2 first records the block: "skill
regeneration blocked: `check-skills` on the pinned Curriculum fails because
roles.datom uses typographic quotes that the pinned protos does not treat as
boundaries … curriculum-deploy's migration to the new datom is held by flow
542442's Lock 851 and not landed. Nothing regenerated; main-flow remains
agent-loadable. Left for the living and flow 542442." Later the same flow's
Wave 6 (`skill-edits.md`) confirms roles.datom's conversion "had already
landed on Curriculum `main` before this subflow opened the file" (witnessed:
zero curly quotes remain in `roles.datom`) and that the regeneration then ran
and succeeded. Primary's own git history corroborates: commit
`ac102226daa78663eee6262bc1f41275077be376`, "Regenerate the deployed skill
and role trees," 2026-09-12 04:15:28 -0600, two minutes after Curriculum's
`2ef2b538…` "Apply the approved skill proposals from flow f6db8d" at
04:13:15.

### Flow 564f55 / 857335 — the incident that provoked the ruling, and the launch mechanics

`flows/564f55/log.md` records the Codex realization flow launch and the
dual-audit order that led to 857335 overriding its own sandbox and to the
"we need better training" ruling: "2026-09-10: the living instructed the
Codex realization flow, through this flow: 'use an opus 5 medium (the same
way you did) for an against-the-vision skeptical audit, as well as his own
sol medium subflow audit.'" `flows/564f55/reports/codexLaunch.md` (a design
report, read directly, not yet realized as an installed launch script)
records the launch convention actually used by prior flows: `codex exec`
(never the TUI, never remote) with `--dangerously-bypass-approvals-and-sandbox`,
and the rule that "the identity block (`FLOW_ID=`, `FLOW_DIRECTORY=`) appears
**only in subflow prompts**; main-flow prompts omit it so the Codex flow
claims its own lane through `$main-flow`" — consistent with the later 162eb3
ruling that a cross-harness launch is a subflow launch. `flows/162eb3/log.md`
names 857335 as the flow that "launched two independent skeptical audits
(Claude Code claude-opus-5 medium; Codex gpt-5.6-sol medium) as systemd user
units," with Sol run under `--sandbox read-only` — the deviation the psyche
asked about.

### What is still pending

- The `roles.datom` Sol-vs-`AGENTS.md` contradiction flagged by f6db8d
  (`reports/recent-vision.md:950`, relayed) is explicitly left for the
  living; not resolved by any record this subflow found.
- No Vision distillation of any record in §1 exists yet — the skill edits
  that landed are realization, not distillation, and 9e7c9f's own vision
  (`flows/9e7c9f/vision/distillAnythingThatIsUsed.md`) records the living's
  instruction to distill raw vision found in the course of gathering it,
  which is why this report marks every §1 record's status explicitly.

---

## 3. Current installed state, witnessed

All claims in this section were read or run directly by this subflow today
(2026-09-12), as evidence, not as skill loading.

### `.claude/skills/subflow/SKILL.md` (installed, Claude side)

```
---
description: A subflow receives the main flow's identity and is carrying out delegated work.
dependencies: [vocabulary]
---

Use the `FLOW_ID` and `FLOW_DIRECTORY` in the main flow's brief.
Obtain the current `THREAD_ID` from the harness after launch.
Use `THREAD_ID` only for transcript and evidence provenance.
Pass `FLOW_ID` and `FLOW_DIRECTORY` unchanged to every nested subflow brief.
Do the delegated work and return its final response.
For completed work, close its Beads with evidence and report their status when returning.
Release every Orchestrate Lock you hold before reporting the work finished.
Do not create a lane, index entry, or log.
Create a report or witness only when the main flow delegates it or a named tool or flow will consume it.
Load `flow-evidence` before creating that artifact.
```

Says nothing about launching another harness. Confirms §2's account:
`skills/subflow.md` was deliberately not given a cross-harness sentence
(§1c of `skill-proposals.md`); the A10 lock-release line is present as the
second-to-last line. `.agents/skills/subflow/SKILL.md` is byte-identical.

### `.claude/skills/main-flow/SKILL.md` (installed, Claude side)

Frontmatter: `disable-model-invocation: true`. Body carries the cross-harness
line exactly as proposed and applied:

> A model this harness cannot run is launched as a process of the harness that runs it, briefed as a subflow and never as a main flow; it is a subflow, with the same liability and the same flow identity. Launch it with no sandbox and every permission — `claude -p --dangerously-skip-permissions`, `codex exec --sandbox danger-full-access --ask-for-approval=never` — except where the installed wrapper or that harness's own configuration already supplies them.

Before-the-first-flow-artifact line is the Claude-specific `flow-id claude
--flows-root ABSOLUTE_DIRECTORY --parent-session "$CLAUDE_CODE_SESSION_ID"`.

### `.agents/skills/main-flow/SKILL.md` (installed, generated Codex-consuming side)

Byte-for-byte the same body text as the Claude version (including the
cross-harness line), except: frontmatter still reads `user-only: true`
(not `disable-model-invocation: true` — that rewrite is Claude-target-only
per 162eb3's account), and the before-the-first-flow-artifact line reads
`flow-id codex --flows-root` with the explicit absolute flows root. Both
targets are generated from one authored source with `{% if claude %}` /
`{% if codex %}` blocks (see below), so the divergence is templated, not
accidental drift.

### Authored source, `/git/github.com/LiGoldragon/Curriculum/skills/main-flow.md`

Frontmatter carries `user-only: true` uniformly (the per-target
`disable-model-invocation` rewrite is curriculum-deploy's own generation-time
transform, confirmed by the installed `.claude/skills/main-flow/SKILL.md`
actually differing from this authored frontmatter). Body is otherwise
identical to both installed copies, including the cross-harness line and the
`{% if claude %}...{% endif %}` / `{% if codex %}...{% endif %}` blocks
around the two `flow-id` invocations.

### Authored source, `/git/github.com/LiGoldragon/Curriculum/skills/subflow.md`

Identical text to the installed `.claude/skills/subflow/SKILL.md` above
(frontmatter `dependencies: [vocabulary]`, no `user-only`/
`disable-model-invocation` key at all — this skill is agent-loadable on both
harnesses, unlike `main-flow`).

### The installed wrappers

Witnessed directly:

```
$ which claude codex
/home/li/.nix-profile/bin/claude
/home/li/.nix-profile/bin/codex
```

`claude` (`/nix/store/…-claude-code-2.1.263/bin/claude`, a generated Bash
wrapper): sets `DISABLE_AUTOUPDATER=1`, `DISABLE_NON_ESSENTIAL_MODEL_CALLS`
(default `1`), `DISABLE_INSTALLATION_CHECKS=1`; prepends `socat` and
`bubblewrap` to `PATH`; execs `.claude-wrapped` with `"$@"` unchanged. **No
sandbox or permission flag is added.**

`codex` (`/nix/store/…-codex-0.153.4/bin/codex`, a generated Bash wrapper):
prepends `bubblewrap` to `PATH`; execs `.codex-wrapped` with `"$@"`
unchanged. **No sandbox or permission flag is added.**

This matches — independently, not by re-reading its report — flow f6db8d's
`skill-proposals.md` witness of the same two wrappers.

`~/.codex/config.toml` line 1: `approval_policy = "never"`; line 8:
`sandbox_mode = "danger-full-access"` — so a bare `codex` launch on this
machine already inherits both flags the psyche named, making
`--ask-for-approval=never --sandbox danger-full-access` redundant but
harmless if passed explicitly by a subflow brief, exactly as the installed
`main-flow` skill's caveat ("except where the installed wrapper or that
harness's own configuration already supplies them") anticipates. (Note:
this file also currently pins `model = "gpt-5.6-luna"` as the Codex config
default, not Astra — Astra-as-main-flow-only is a launch-time choice per
`flows/58a86d/vision/codexModel.md`, not a config default, so this is not a
contradiction of that record.)

`~/.claude/settings.json` and `/home/li/primary/.claude/settings.json`:
witnessed directly, neither has a `defaultMode` or `bypassPermissions` key —
so `claude -p --dangerously-skip-permissions` must indeed be passed
explicitly for a Claude cross-harness subflow, as the installed skill states.

### curriculum-deploy version and generated-tree freshness

Installed Nix store paths: `/nix/store/…-curriculum-deploy-0.6.2/bin/curriculum-deploy`
(current) alongside a stale `…-curriculum-deploy-0.1.0` (unreferenced,
presumably orphaned garbage). `flake.nix` pins
`curriculum-deploy` at `github:LiGoldragon/curriculum-deploy/c669b27b…` —
the exact 0.6.2 revision 162eb3's account names.

**Freshness against authored sources — mixed.** The `.claude/`/`.agents/`
trees for `main-flow` and `subflow` (and the other nine skills f6db8d's apply
subflow touched) match Curriculum commit `2ef2b538f7efa9b7da4b98b98b1e9cb73c6f2fdf`
exactly — confirmed above by direct comparison of installed and authored
text. But `flake.lock`'s own `curriculum` input is still pinned at
`a7d2f4f1fc57c2376ae041288d05b55ab7577052`, an **older** commit that predates
`2ef2b538` on Curriculum's `main` (witnessed: `git log a7d2f4f1` shows
"codex-harness pins model and effort at launch" as its tip, several commits
before the skill-proposals apply). This is not a contradiction: `flake.nix`'s
`generate-skills`/`check-skills` apps take an explicit
`Operation.{ data-root workspace-root }` argument at invocation time, so
f6db8d's regeneration subflow evidently pointed `data-root` at the live
`/git/github.com/LiGoldragon/Curriculum` checkout directly rather than at the
flake's own `curriculum` input — the generated trees are current, the
flake's lockfile pin of that input is not, and nothing depends on the two
agreeing. Curriculum's own `main` has since advanced past `2ef2b538` to
`8484ecd` ("Apply lojix skill addendum 2 (B2, B3, B4/B5, B6)"), which does
not touch `main-flow` or `subflow` and is therefore outside this report's
scope, but is a further sign the generated tree is a point-in-time snapshot,
not a live mirror.

`.codex/` (`/home/li/primary/.codex/agents/*.toml`) holds only subagent
role configs (`write-demanding.toml`, `default.toml`, `read-demanding.toml`,
`worker.toml`, `write-ordinary.toml`, `read-ordinary.toml`,
`read-trivial.toml`, `explorer.toml`, `write-trivial.toml`) — no
`main-flow`/`subflow` files live there; per f6db8d's report, `.codex/` and
`.pi/` were unchanged by the latest regeneration.

---

## Sources

Raw psyche records (§1), all **read** directly by this subflow:
- `/home/li/primary/flows/162eb3/vision/subflows.md`
- `/home/li/primary/flows/01a05e95/vision/subflows.md`
- `/home/li/primary/flows/01a05e95/vision/flowSkills.md`
- `/home/li/primary/flows/01a04881/vision/subflows.md`
- `/home/li/primary/flows/01a05826/vision/subflowIdentity.md`
- `/home/li/primary/flows/01a030df/vision/subagents.md`
- `/home/li/primary/flows/5851f4/vision/subagents.md`
- `/home/li/primary/flows/58a86d/vision/subagentModel.md`
- `/home/li/primary/flows/58a86d/vision/codexModel.md`
- `/home/li/primary/flows/8a5caa/vision/codex.md`
- `/home/li/primary/flows/38dec9/vision/skillLandingBySubflow.md`
- `/home/li/primary/flows/01a0428b/vision/useASubflowToPutTheReportTogether.md`
- Checked for landing: `grep -rl "subflow" /home/li/primary/Vision/` (no hits)

Flow accounts (§2):
- `/home/li/primary/flows/162eb3/log.md` (read)
- `/home/li/primary/flows/f6db8d/log.md` (read)
- `/home/li/primary/flows/f6db8d/reports/skill-proposals.md` (read)
- `/home/li/primary/flows/f6db8d/reports/skill-edits.md` (read)
- `/home/li/primary/flows/f6db8d/reports/recent-vision.md` (read, relayed excerpts)
- `/home/li/primary/flows/564f55/log.md` (read)
- `/home/li/primary/flows/564f55/reports/codexLaunch.md` (read)
- Curriculum git history: `git -C /git/github.com/LiGoldragon/Curriculum log --oneline -5 a7d2f4f1…` and `log --oneline -1` (witnessed)
- Primary git history: `git -C /home/li/primary log -5` (witnessed)

Installed state (§3), all **witnessed** by this subflow today:
- `/home/li/primary/.claude/skills/subflow/SKILL.md`
- `/home/li/primary/.claude/skills/main-flow/SKILL.md`
- `/home/li/primary/.agents/skills/subflow/SKILL.md`
- `/home/li/primary/.agents/skills/main-flow/SKILL.md`
- `/git/github.com/LiGoldragon/Curriculum/skills/main-flow.md`
- `/git/github.com/LiGoldragon/Curriculum/skills/subflow.md`
- `which claude codex`; `head -c 2000` of each resolved wrapper script
- `/home/li/.codex/config.toml`
- `/home/li/.claude/settings.json`, `/home/li/primary/.claude/settings.json`
- `/home/li/primary/flake.nix`, `/home/li/primary/flake.lock`
- `find /nix/store -iname "curriculum-deploy*"`
- `find /home/li/primary/.codex -maxdepth 2`

Not investigated: `flows/444e5e` (log.md contains one unrelated entry about
Claude flow-ID initialization after a Codex-only instruction; not
cross-harness-subflow-launching material) and `flows/857335`'s own
report/witness files beyond what 162eb3 and 564f55 already relay about it.
