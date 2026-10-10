# YouTube Skill Doctrine Report

## Task And Scope

Analyze the YouTube video `https://www.youtube.com/watch?v=UNzCG3lw6O0` for concrete proposals that could affect the user's agent/skill doctrine. Do not edit doctrine or source files. Prefer transcript evidence over commentary.

## Consulted Sources And Commands

- `yt-dlp --no-cache-dir --skip-download --print ... https://www.youtube.com/watch?v=UNzCG3lw6O0`: video metadata.
- `yt-dlp --no-cache-dir --skip-download --list-subs https://www.youtube.com/watch?v=UNzCG3lw6O0`: caption availability.
- `yt-dlp --no-cache-dir --skip-download --dump-single-json ... | jq ... automatic_captions["en-orig"]`: YouTube timedtext caption URL.
- `curl -L -s "$url" | jq ...`: extracted timestamped `en-orig` automatic caption transcript.
- `yt-dlp --no-cache-dir --skip-download --print '%(description)s' ...`: YouTube description and timestamp outline.
- `curl -L -s https://raw.githubusercontent.com/mattpocock/skills/main/skills/productivity/writing-great-skills/SKILL.md`: linked author skill, used as secondary corroboration only because it may drift after publication.
- `spirit "(Lookup n9fl)"`, `spirit "(Lookup 346n)"`, `spirit "(Lookup ty3g)"`, `spirit "(Lookup w312)"`: verified supplied public intent records.
- Local doctrine read: `AGENTS.md`, `.agents/skills/helper-context-transfer/SKILL.md`, `.agents/skills/orchestration/SKILL.md`, `.agents/skills/skill-editor/SKILL.md`, `.agents/skills/repo-intent/SKILL.md`, `.agents/skills/session-lanes/SKILL.md`, `.agents/skills/reporting/SKILL.md`.

No repository doctrine/source files were edited. This report file is the only output artifact.

## 1. Video Identity

- Title: `Building Great Agent Skills: The Missing Manual`
- Channel/uploader: `AI Engineer`
- Video ID: `UNzCG3lw6O0`
- Upload date from YouTube metadata via `yt-dlp`: `2026-06-29`
- Duration: `20:43`
- URL: `https://www.youtube.com/watch?v=UNzCG3lw6O0`
- Secondary linked resource in YouTube description: `https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/SKILL.md`

Transcript/source confidence: medium-high for proposal extraction. `yt-dlp --list-subs` found YouTube automatic captions including `en-orig`, but no creator-provided subtitle track. The transcript used here is the YouTube timedtext `en-orig` auto-caption JSON. The YouTube description's timestamp outline matches the transcript's structure, increasing confidence in the extracted proposal list. Exact wording should be treated cautiously because captions are automatic.

## 2. Concrete Video Proposals

Observed proposals, separated from interpretation:

1. Use a skill checklist/rubric.
   The video says the missing piece is a shared way to distinguish good skills from bad skills, then gives a checklist: trigger, internal structure, steering, and pruning. Transcript refs: about `2:12` through `3:14`; YouTube description also lists these four sections.

2. Decide whether each skill is user-invoked or model-invoked.
   The video distinguishes user-invoked skills from model-invoked skills. Model-invoked skills expose a description in the agent context so the model can choose to load the `SKILL.md`; user-invoked skills do not expose that context pointer to the model. Transcript refs: `3:16` through `5:09`.

3. Treat model invocation as a tradeoff, not an automatic default.
   Model-invoked skills increase context load by adding a description to every request and can be unpredictable because the model might not follow the pointer even when relevant. User-invoked skills lower agent context load but increase the user's cognitive load. The speaker personally prefers more user control. Transcript refs: `5:09` through `7:25`.

4. Structure a skill around steps and reference.
   The video proposes two main units: steps are the procedure; reference is supporting material used to complete the steps. Some skills may be all steps or all reference. Transcript refs: `7:29` through `8:53`.

5. Keep `SKILL.md` small and progressively disclose branch-specific reference.
   The video says the main skill file should be as small as possible. Reference material needed only by some branches should move behind context pointers into separate files; material needed on every branch can remain inline. Transcript refs: `9:00` through `11:53`.

6. Use "leading words" to steer behavior.
   The video proposes compact terms that pack substantial meaning, repeat through the skill, and recruit the model's prior knowledge. Example: use "vertical slice" to steer coding away from layer-by-layer implementation. Transcript refs: `11:54` through `14:56`.

7. Increase legwork by splitting phases when later goals cause shallow earlier work.
   The video says plan-mode agents often rush clarifying questions because they see the later goal of creating a plan. The proposed fix is to split the clarifying phase into its own skill, then run planning/PRD generation after that phase completes. Transcript refs: `14:56` through `16:47`.

8. Prune duplication, sediment, and no-ops.
   The video advises single source of truth for each piece of reference or instruction; remove stale/irrelevant accumulated material; delete no-op lines that do not change agent behavior. Transcript refs: `16:48` through `19:05`.

9. Use the linked "writing-great-skills" skill as a practical resource.
   The video and description point to the author's skill repository. The linked skill adds sharper wording around predictability, information hierarchy, completion criteria, granularity, and a router skill for managing many user-invoked skills. This is secondary evidence, not transcript-primary evidence, because the repository can change after the video. Transcript refs: about `2:57` through `3:13` and `19:55`; linked source above.

## 3. Compatibility Assessment

Against `n9fl`:

- Compatible: specific, small skills and phase splitting fit the desire for extremely specific agents/skills.
- Compatible with adaptation: the warning against model-invoked skill sprawl supports keeping only relevant doctrine in context.
- Tension: the speaker's preference for user-invoked skills should not become a rule to minimize early context. `n9fl` says quality comes from maximizing early context and using very specific agents/skills. In this workspace, the stronger translation is deterministic up-front selection of the right role packet or skill set, not asking the user to remember every skill.

Against `346n`:

- Compatible: pruning no-ops, eliminating sediment, and splitting rushed phases are quality moves when backed by evidence.
- Risk: over-pruning can sacrifice quality if deletion tests are not based on behavior. Quality remains primary; token savings are secondary.

Against `ty3g`:

- Compatible: "agent does not do what I want" is treated as a guidance-design problem. Leading words, better structure, and phase splitting are all ways to upgrade guidance.
- Required adaptation: do not evaluate success by blaming the model or by assuming hidden reasoning traces are a reliable surface. Treat failures as evidence that instructions, role packet, routing, or context are insufficient.

Against `w312`:

- Compatible: the video's concern about unpredictable model invocation supports moving deterministic routing out of agent judgment.
- Tension: model-invoked skills and the linked resource's "router skill" are weaker fits when the correct route is derivable from inputs. In this doctrine, deterministic routing, lookup, classification, projection, and address resolution belong in code/schema/dispatch machinery, not a model deciding from descriptions.

Against current local doctrine style:

- `AGENTS.md` already says the boot contract stays small and generated role packets carry required doctrine. This matches the video's concern about always-loaded skill descriptions, but the local reason is stronger: precise early loading by role/context.
- `.agents/skills/skill-editor/SKILL.md` already requires terse, present-tense, one-capability skills, no tutorial padding, no duplicate description/body restatement, and splitting distinct capabilities. This overlaps strongly with the video's pruning and granularity advice.
- `.agents/skills/helper-context-transfer/SKILL.md` and `.agents/skills/session-lanes/SKILL.md` already support bounded helpers/fresh lanes for focused work, which is the workspace-native version of "hide future steps" to increase legwork.
- `.agents/skills/orchestration/SKILL.md` already says to select an agent type whose generated role packet embeds the required doctrine. That is more compatible with deterministic routing than broad model-invoked skill discovery.

## 4. Recommendations

1. Adopt the checklist as a review heuristic.
   Use trigger, structure, steering, and pruning when auditing or editing skills. Do not add it as a long tutorial; it belongs as terse skill-editor guidance or a review checklist.

2. Adopt invocation tradeoff language, but translate it to this system.
   Prefer deterministic role/skill selection before work starts. Use model-invoked descriptions only when the agent genuinely must discover the skill autonomously and that choice cannot be made by dispatcher/manifest/code.

3. Adopt branch-based progressive disclosure.
   Inline material every branch needs; move branch-only reference into named sibling files and point to it from the triggering branch. This fits current progressive-disclosure practice and would strengthen skill-editor guidance.

4. Adopt leading words cautiously.
   Use compact, well-known domain terms when they make behavior more precise, such as "vertical slice". Do not treat "leading words" as magic incantations, and do not rely on hidden reasoning traces as the verification surface. Verify through observable plans, tool use, diffs, reports, or tests.

5. Adopt phase splitting conditionally.
   When a step repeatedly completes shallowly because later goals dominate attention, first sharpen the step's completion criterion. If the rush persists, split that phase into a separate helper/skill/lane with its own output requirement. This is compatible with current helper-context-transfer and session-lane doctrine.

6. Adopt no-op and sediment pruning.
   This is already mostly present in local skill-editor style. The useful addition is the explicit deletion test: if removing a sentence does not change observable behavior in that skill's context, delete it.

7. Reject broad reliance on model-invoked skill routing for deterministic choices.
   If the correct skill can be derived from task type, path, manifest, role, or schema, route mechanically. This follows `w312`.

8. Reject hidden reasoning traces as an evaluation requirement.
   The video suggests watching for leading words in reasoning traces. For this workspace, use visible behavior and artifacts instead, because chain-of-thought may be unavailable, incomplete, or not a stable contract.

9. Investigate, but do not adopt yet: the linked skill's router-skill idea.
   It may be useful as a temporary human-facing index for many manually invoked skills. It should not replace deterministic dispatch or manifest routing where a correct route is derivable.

10. Investigate, but do not treat as transcript-primary: per-step completion criteria from the linked skill.
   The linked skill's completion-criterion advice is compatible with local doctrine and may be worth adding, but it is not a central transcript claim in this video.

## 5. Exact Wording Candidates

These are candidates only if the skill-editor source is revised later:

- "When a skill has branches, inline only material every branch needs; move branch-only reference into a named sibling file and point to it from the branch that uses it."
- "Prune by deletion test: if removing a sentence would not change observable agent behavior in this skill's context, delete it instead of rephrasing it."
- "Use compact domain terms as leading words only when they name the desired behavior more precisely than the surrounding prose; verify by observable output, not hidden reasoning traces."
- "When a workflow step repeatedly completes shallowly because later goals dominate attention, sharpen its completion criterion first; split it into a separate helper or skill only if the rush remains."

## 6. Evidence Links And Transcript References

- Video: `https://www.youtube.com/watch?v=UNzCG3lw6O0`
- Checklist overview: `https://youtu.be/UNzCG3lw6O0?t=132`
- User-invoked vs model-invoked trigger discussion: `https://youtu.be/UNzCG3lw6O0?t=196`
- Context load/cognitive load and unpredictability: `https://youtu.be/UNzCG3lw6O0?t=309`
- Steps and reference structure: `https://youtu.be/UNzCG3lw6O0?t=449`
- Minimal `SKILL.md` and branch-specific context pointers: `https://youtu.be/UNzCG3lw6O0?t=540`
- Leading words and vertical slice example: `https://youtu.be/UNzCG3lw6O0?t=714`
- Legwork through phase splitting: `https://youtu.be/UNzCG3lw6O0?t=896`
- Pruning duplication, sediment, and no-ops: `https://youtu.be/UNzCG3lw6O0?t=1008`
- Final checklist summary: `https://youtu.be/UNzCG3lw6O0?t=1148`
- Linked author skill from YouTube description: `https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/SKILL.md`

## Unknowns And Limits

- The transcript is automatic captions, not a verified human transcript.
- I did not watch the video visually; analysis is based on metadata, description, transcript, and the linked GitHub skill.
- I did not inspect the full external repository history, so the linked skill is treated as current secondary evidence rather than the video's historical content.
- No doctrine edits were made.
