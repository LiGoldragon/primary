# Field split proposal

Draft for e51411. Nothing is landed. Sources are Curriculum `main` at `60be395c7f9d`; `field.md`, `metaflow.md`, and `refresh.md` there match the working copy byte for byte.

Summary: `field` shrinks to its identity. A new `reaping` skill carries the procedure. `metaflow` gets the model roster. `refresh` already owns the Field refresh naming and gates, so nothing moves into it. It only loses its two model ids, which now live in the roster. "Primary Field" and the launch-gating paragraph are dropped.

## Rulings needed before landing

1. **Field Low / Terra.** The living said on 2026-09-24 (`flows/752e0f/vision/models.md`): "we're going to take out Terra until Terra 6 releases and we're just going to give those jobs to the new Luna 6 instead." The brief says "Field low Terra". The Codex catalog (`~/.codex-next/models_cache.json`) has no `gpt-6-terra`, only `gpt-5.6-terra`. Subflows still run on `gpt-5.6-terra` today, and no native Field Terra seat is live (`field-terra 2fe3f1` is STALE). The roster below follows the 09-24 words. If Terra stays, replace that cell with `Terra, gpt-5.6-terra`.
2. **Psyche Medium.** The live seats d8df70 ("Psyche Medium") and e51411 run `claude-opus-5-5`. `SKILL_VARIABLES.md` says `Psyche medium Claude model: claude-opus-4-6[1m]`, from the living's 2026-09-18 words in `flows/1ac573/vision/operational-defaultModelPsycheMediumClaude.md`. The roster uses the live id. One of the two must change, and a model id should have only one home.
3. **Effort.** The roster says every seat and subflow runs at medium effort. That comes from `field.md` L25 and `flows/5851f4/vision/subagents.md`. Both Codex configs set `default_subagent_reasoning_effort = "xhigh"` with `default_subagent_model = "gpt-5.6-luna"`, and many of today's Luna subflows ran at xhigh on 5.6. The config disagrees with the skill.
4. **Plan item 1 deviation.** The approved plan keeps "a Field refresh is not ready because panes exist …" in `field`. `refresh.md` L21 already states the same gates in full. `field` depends on `refresh`, so under one home per meaning I cut the sentence from `field`. To keep it anyway, add it after the identity line as: `A Field refresh is ready only when refresh's gates pass; panes existing is not readiness.` Adding it would duplicate `refresh`.

## Roster evidence

| Seat | Witnessed model, effort | Evidence |
|---|---|---|
| Field Astra | `gpt-6-astra`, medium | 5f38bc, 504461: first `turn_context` of their Codex rollouts |
| Field Sol | `gpt-6-sol`, medium | b7da5d rollout `…c55b7da5da58` |
| Field Luna | `gpt-6-luna`, medium | e71dab rollout `…f29e71dabb46` |
| Field Terra | no live seat; `gpt-5.6-terra` in subflows | see ruling 1 |
| Mind Astra | `gpt-6-astra`, medium | 26c50c, f5a74e |
| Mind Sol | `gpt-6-sol`, medium | 00f95a, a676b3 |
| Mind Low / Ultra-low | **unconfirmed**: no live Mind Terra or Luna seat | roster assumes the same as Field |
| Psyche Fable (High) | `claude-fable-5-1` | 38de5b transcript |
| Psyche Opus (Medium) | `claude-opus-5-5` | d8df70, e51411 transcripts; see ruling 2 |
| Psyche Sonnet (Low) | `claude-sonnet-5` | 9c7514 transcript; living 2026-09-25, `flows/e51411/vision/launch.md`: "Low corresponds with Sonnet" |
| Psyche Haiku (Ultra-low) | `claude-haiku-4-5-20251001` in recent Claude transcripts; **seat binding unconfirmed** (pane `psyche-haiku-of-b80e55` titled "Psyche Ultra Low (claim pending)", no session id) | living 2026-09-21, `flows/1b8ac0/vision/autonomousOperation.md`: "a haiku running Psyche ultra low" |
| Old Opus | `claude-opus-4-6` | e88ca4 transcript (seat STALE) |

`claude --help` names only the aliases `fable`, `opus`, `sonnet` and the example `claude-fable-5`. It does not confirm the full ids above; the transcripts do.

## New `skills/field.md`

```markdown
---
description: A Field seat is selected, refreshed, launched, or described.
user-only: true
dependencies: [main-flow, refresh, subflow, testing, vocabulary, metaflow, reaping]
---

Field keeps the system deployed, fixed, and running, and reaps what is dead.
```

This keeps the role, its user-only status, and its dependency on `refresh`, which carries the readiness gates. It adds `reaping`. It removes everything else, as the mapping table shows.

## New `skills/reaping.md`

No prefix: the living approved it (e51411). I searched the reference collections (`obra/superpowers`, `anthropics/skills`) and found no prior art for flow reaping. The only hits were about process cleanup for a visual companion.

```markdown
---
description: A flow, its pane, or its session registration may be finished, superseded, or dead, and closing it is being judged, executed, or scheduled.
dependencies: []
---

Field reaps. No watcher, daemon, or future framework takes this over.

Death is shown by lifecycle evidence: the flow is finished, superseded, or otherwise dead. Idleness, a pane, a live PID or TTY, a runtime or harness companion process, ready-idle status, or a stale status record neither proves death nor counts as active work.
A quiescent superseded predecessor is reapable while its PID lives, once its handoff is accepted, its transcript and evidence are retained, and it holds no jobs or locks. Its unfinished work may pass to an owner that accepts it. A finished bounded test needs its retained result and completion record, not a successor.
Retain the handoff, transcript, and evidence, then close the registration or pane through the supported lifecycle. Process death is not required.

Field Astra or Field Sol judges. For careful transcript and successor investigation, delegate the judgment to old Opus. Give the judge the transcript, handoff, and readiness or judgment receipt contents, or read access to them; names, links, candidate pairs, and HOLD labels are not input. A judge without that input requests it and issues no hold.

Within recorded user delegation, a positive judgment authorizes Field Luna to cut. The judgment job message names the judge and source flow, the exact target native identity or endpoint, the successor and evidence-retention references, the authorized cutoff action, and the hold conditions. Authority comes from the parent delegation or a durable judgment receipt, never from a messenger readback's claimed sender. At the last moment Luna checks the exact target identity and that no new work has arrived, then cuts without repeating the investigation. An approved reap job stays Luna's priority until its outcome or blocker is recorded; unrelated peer review queues behind it.

Luna runs an evidence-only reaping and archive-maintenance pass on each recorded start or lifecycle change, and every thirty minutes as a fallback. A pass continues only for a changed candidate or a cut whose outcome is unrecorded. Each candidate ends in retained cleanup evidence or an explicit blocker with its owner. Luna never wakes or resumes a target.
```

What this keeps, changes, or removes, compared with `field.md` L9–L15:
- **Kept:** every eligibility, judge, executor, preflight, retention, priority, and cadence rule.
- **Merged:** L9's list of non-evidence and L13's list of things that are not active work become one line. "Establish eligibility … then close" and "preserve … before reaping" become one retention line.
- **Removed:** "Preserve active work and unpersisted state until the evidence supports reaping" restates the eligibility and retention lines. "applies the eligibility, retention, and preflight requirements above" is self-reference within one skill.

## `skills/metaflow.md` diff

```diff
 ---
-description: A Field flow must place, coordinate, or transfer work across the Field power tiers.
+description: Work must be placed, coordinated, or transferred across the Field power tiers, or the model for an aspect's power tier must be chosen or named.
 ---
 
-Field has four power tiers: high, medium, low, and ultra-low.
+Each aspect has four power tiers: high, medium, low, and ultra-low. One model carries each tier:
+
+| Power | Psyche | Mind | Field |
+|---|---|---|---|
+| High | Fable, `claude-fable-5-1` | Astra, `gpt-6-astra` | Astra, `gpt-6-astra` |
+| Medium | Opus, `claude-opus-5-5` | Sol, `gpt-6-sol` | Sol, `gpt-6-sol` |
+| Low | Sonnet, `claude-sonnet-5` | none until Terra 6; Luna carries its jobs | none until Terra 6; Luna carries its jobs |
+| Ultra-low | Haiku, `claude-haiku-4-5-20251001` | Luna, `gpt-6-luna` | Luna, `gpt-6-luna` |
+
+Old Opus is `claude-opus-4-6`. Every seat and subflow runs at medium effort.
 
 Every Field tier works in the same shared operational scope: keeping the system observed, healthy, fixed, and running. A tier changes the amount of judgment applied to a job. It does not create a separate Field domain, separate authority, or separate destination for the work.
```

The rest of `metaflow.md` is unchanged. The description widens because the roster covers all three aspects and the brief puts it here. No other description currently matches "choose or name the model for a power tier". `testing-flow-titles` covers deriving a title from a model, which is a different situation. The table cells for Low and Psyche Medium depend on rulings 1 and 2. Mind Low and Ultra-low are unconfirmed.

## `skills/refresh.md` diff

Refresh already states Field refresh naming (L17), crossover-only (L19), and readiness gates (L21), so nothing is added. The only change removes its copies of the model ids. The roster is now their one home, and refresh's `gpt-5.6-sol` is stale anyway: live is `gpt-6-sol`.

```diff
-For a Field refresh, create exactly two fresh main seats: `field-astra-of-<ancestor-flow-id>` and `field-sol-of-<ancestor-flow-id>`. `of` means descendant of, and `<ancestor-flow-id>` is the immediate predecessor's canonical short `FLOW_ID`. Field Astra is `gpt-6-astra` at medium effort and is the high-power Field companion. Field Sol is `gpt-5.6-sol` at medium effort and becomes the ongoing Field owner only after readiness. The two new seats must have distinct new flow IDs. Neither replaces Psyche or Mind.
+For a Field refresh, create exactly two fresh main seats: `field-astra-of-<ancestor-flow-id>` and `field-sol-of-<ancestor-flow-id>`. `of` means descendant of, and `<ancestor-flow-id>` is the immediate predecessor's canonical short `FLOW_ID`. Field Astra is the high-power Field companion. Field Sol becomes the ongoing Field owner only after readiness. The two new seats must have distinct new flow IDs. Neither replaces Psyche or Mind.
```

## "Primary Field" and launch gating

- **"Primary Field" (L27): drop it.** The only vision source is `flows/b05237/vision/operational-fieldTestingAndUltraLow.md` (2026-09-18): "You're the field medium, or just field Sol … That's your primary field Sol." It says Field Sol is the main Field flow, not that there is a conversational front end to Psyche and Mind. The paragraph (commit `37a540f8385d`) goes beyond that source. It also contradicts `operational-layer-communication`: the living speaks to Fable and Astra, and Field joins only when the machine is affected. Its "light reasoning effort" clashes with medium effort for every seat. Nothing else has to take it over, because "Field Sol is primary" is already true through refresh L17/L21, where Field Sol owns Field.
- **Launch gating (L35): drop it.** It gates starting a main flow by loading `$main-flow` from the Codex catalog. That is no longer how a main flow starts: the launcher injects the byte-exact `main-flow` as the first prompt block and reads it back (`main-flow` L34, `refresh` L13). Both already say that anything unable to inject and verify is not a launcher, and that the blocker is reported (`refresh` L9). The paragraph describes one retired mechanism and holds nowhere else.

## Mapping of every current `field.md` sentence

| L | Sentence (abridged) | Goes to / reason cut |
|---|---|---|
| 2 | description | `field`, unchanged |
| 3 | `user-only: true` | `field`, unchanged (role skill) |
| 4 | dependencies | `field`, plus `reaping` |
| 7 | Field is an enduring role, not the name of reaping. | Cut: the identity line states the role, with reaping as one duty |
| 7 | Reaping is one Field capability. | Cut: same |
| 9 | Field workers are the reapers … through the supported lifecycle. | `field` identity ("reaps what is dead") and `reaping` retention/close line |
| 9 | Do not defer to a separate watcher, daemon, or future framework. | `reaping` L1 |
| 9 | Establish eligibility from lifecycle evidence, preserve handoff and transcript, then close … | `reaping` death-evidence and retention lines |
| 9 | Idleness, a pane, a process, or a stale status record alone does not establish death. | `reaping`, merged with L13 s1 |
| 9 | A quiescent obsolete predecessor … can be reaped while its PID remains live. | `reaping` |
| 9 | Preserve active work and unpersisted state until the evidence supports reaping. | Cut: restates the eligibility and retention lines |
| 11 | Field Astra or Sol judges; delegate careful investigation to old Opus. | `reaping`; the old Opus id goes to the `metaflow` roster |
| 11 | Give the judge transcript, handoff, receipts; names/links/HOLD labels insufficient. | `reaping` |
| 11 | A judge lacking input requests it without a substantive hold. | `reaping` |
| 11 | Unfinished work may transfer to an accepting owner. | `reaping` |
| 11 | A positive judgment authorizes Luna, conditional on preflight. | `reaping` |
| 11 | The judgment job message names judge, source, target, successor, retention, action, holds. | `reaping` |
| 11 | A messenger readback's claimed sender is not independent authority … | `reaping` |
| 11 | Luna makes the final check, cuts without repeating the investigation or requiring process death. | `reaping` (split across the retention and executor lines) |
| 13 | Companion process, live TTY/PID, ready-idle are not active delegated work. | `reaping`, merged with L9 s4 |
| 13 | A finished bounded test needs its retained result, not a successor. | `reaping` |
| 13 | An approved reap job remains priority …; queue unrelated peer review. | `reaping` |
| 15 | Luna runs a pass on start/lifecycle change and every thirty minutes. | `reaping` |
| 15 | It continues only when a candidate changed or an outcome is unrecorded. | `reaping` |
| 15 | Each candidate reaches cleanup evidence or an explicit blocker with its owner. | `reaping` |
| 15 | Luna never wakes or resumes a target and applies the requirements above. | `reaping` (first half); second half cut as self-reference |
| 17 | Field Sol is the protected main seat: `gpt-5.6-sol` at medium effort. | `metaflow` roster, corrected to `gpt-6-sol`; "protected" see L29 |
| 17 | It is a main flow only after `$main-flow`, `FLOW_ID` claim, native-start receipt. | Cut: `main-flow` L34–35 |
| 17 | Do not call collaboration-tool subagents native Flow-Nexus flows. | Cut: `main-flow` L28, `subflow` |
| 19 | Field Astra is `gpt-6-astra` at medium effort. | `metaflow` roster |
| 19 | High-power names the Field tier, never an effort override. | Cut: `psyche-interraction` L44 |
| 19 | Astra is a fresh main seat, distinct `FLOW_ID`, does not replace Psyche or Mind. | Cut: `refresh` L17 |
| 21 | For a Field refresh load `$refresh`; it creates `field-astra-of-…` / `field-sol-of-…`. | Cut: `refresh` L17; `field` depends on `refresh` |
| 21 | `of` means descendant of. | Cut: `refresh` L17 |
| 21 | Successor seats have distinct new flow IDs. | Cut: `refresh` L17 |
| 21 | Refreshed Field Sol inherits ownership only after ready. | Cut: `refresh` L17, L21 |
| 21 | Predecessor crossover-only until both gates pass. | Cut: `refresh` L19, L21 |
| 21 | Never kill, retire, or remove its routing automatically. | Cut: `refresh` L19 |
| 23 | Field low is `gpt-5.6-terra`; ultra-low is `gpt-5.6-luna`. | `metaflow` roster: Luna corrected to `gpt-6-luna`; Terra per ruling 1 |
| 23 | When the living names Terra/Luna/low power, address the native main seat. | Cut: `main-flow` L28 (also in `flow-communication` L18 and `operational-layer-communication` L10) |
| 23 | Field Sol may delegate to an internal Terra/Luna child under `$subflow`; it inherits the flow identity. | Cut: `subflow`, `main-flow` L11/L28 |
| 25 | Field subflows use medium reasoning effort. | `metaflow` roster ("Every seat and subflow runs at medium effort"); see ruling 3 |
| 25 | Luna is the ultra-low investigation tier; Terra the low escalation tier. | Cut: `metaflow` L13/L15 define the tiers; the Terra half is stale per ruling 1 |
| 25 | Preserve Luna's findings when escalating to Terra. | Cut: `metaflow` L19 (a transfer carries evidence and open questions) |
| 27 | Primary Field is the fast conversational front end … (5 sentences) | Dropped; see "Primary Field and launch gating" |
| 29 | Do not spend the protected Sol seat on reaping, probing, or a routine retry. | Cut: `reaping` makes Luna the executor; `main-flow` L7/L11 delegate inspection to Luna |
| 29 | Keep its coordination and judgment available; use a lower seat. | Cut: same |
| 31 | Field exists to keep the system deployed, fixed, and running. | `field` identity |
| 31 | A Field refresh is not ready when panes merely exist. | Cut: `refresh` L21; see ruling 4 |
| 31 | Before transfer, witness deployment current, live health, routing, defects owned or open. | Cut: `refresh` L21 |
| 31 | Report unavailable evidence as open; don't infer readiness from pane/process/stale record. | Cut: `refresh` L21 |
| 33 | Field-Luna testing is isolated: disposable situation, bounded inputs, no production lane or identity, observed cleanup. | Cut: `testing` covers bounded runs, cleanup by PID, and not waking production flows. The residual "no production lane or identity" is not carried; if wanted, it belongs in `testing` |
| 33 | A passing isolated Luna test is evidence only for that surface. | Cut: `testing` "Live acceptance has a boundary" |
| 35 | If the Codex catalog cannot load `$main-flow` …, do not start Field Sol; use only a proved route. | Dropped; see "Primary Field and launch gating" |

## Flagged outside this split (not proposed here)

- `operational-layer-communication` L14 sends reaping to "a field Terra". The new `reaping` skill makes Luna the executor, and Terra is out per ruling 1. That line conflicts.
- `main-flow` L11 ("Use Terra for implementation") and L14 ("Terra in Codex") conflict with ruling 1 if Terra stays out.
- The rule "the living naming Terra/Luna/low addresses the native seat" has three homes: `main-flow` L28, `flow-communication` L18, and `operational-layer-communication` L10.

## Sources

- `/git/github.com/LiGoldragon/Curriculum/skills/{field,metaflow,refresh,main-flow,testing,testing-flow-titles,operational-layer-communication,flow-communication,psyche-interraction,skill-designing}.md` at `main` `60be395c7f9d`
- `hm-list`, `herdr agent list` (2026-09-25)
- `/home/li/.codex-next/config.toml`, `/home/li/.codex/config.toml`, `/home/li/.codex-next/models_cache.json`
- Codex rollouts under `/home/li/.codex-next/sessions/2026/09/2{4,5}/` (first `turn_context` model/effort)
- Claude transcripts under `/home/li/.claude/projects/-home-li-primary/`
- `claude --help`
- Vision: `flows/752e0f/vision/models.md`, `flows/e51411/vision/launch.md`, `flows/1b8ac0/vision/autonomousOperation.md`, `flows/1ac573/vision/operational-defaultModelPsycheMediumClaude.md`, `flows/b05237/vision/operational-fieldTestingAndUltraLow.md`, `flows/5851f4/vision/subagents.md`, `flows/4a2502/vision/operational-delegationTierRules.md`
- `/home/li/primary/SKILL_VARIABLES.md`
