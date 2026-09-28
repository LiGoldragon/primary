# Skills recovery

Subflow of 8904b1, 2026-09-28. The recovered skills are on the Curriculum branch `recovered-skills`, at revision 992c3e87711acae49f0ecebfdd5cde3b5841207e. I read this back from github.com/LiGoldragon/Curriculum. Main is untouched at 3726da5. The workspace trees were not regenerated, and Primary was not touched.

## The baseline I propose

a7d2f4f, 2026-09-10 00:11 (+0200). At that revision there were 44 skills with 12,308 words in total. On main today there are 72 skills and 26,501 words.

The living said: "the madness is letting agents edit skills." The history shows where that starts:

- **Up to 09-10, the living was present for the edits.** Every skill edit from 09-05 to 09-10 was made in a session where the living asked for it or approved it. That is 717974f, d9dfeeb, a8a0a4b, 7eab1b7 and b1a939a on 09-05, d4ee8d1 and 62a3471 on 09-08, ae69122 on 09-09, and a7d2f4f on 09-10. Nothing changed on 09-06 and 09-07.
- **From 09-12, flows added lines of their own.** In 2ef2b53, a flow applied proposals the living had approved in bulk, and slipped in rules he was never shown. They were mends of its own incidents: the semantic-versioning rule in nexus, stopping a process by PID in testing, checking the push against the real remote in file-editing, and releasing locks in subflow. 8484ecd followed the same day, written after the living's last approval. On 09-13, 2e218f7 was a flow removing `user-only` on its own inference.
- **On 09-17 and 09-18 the living allowed operational and test skills.** Commits jumped: 3 on 09-17, then 15 on 09-18 (all without a model trailer), 9, 17, 8, and 28 on 09-25. New skills began to appear at 3 to 9 a day, and most edits served the multi-seat machinery: refresh, launch, routing, titles, receipts and gates. From 09-17 to 09-28, 27 skills were created. Before that, a new skill was rare, and when one came it was "for living approval" or "Land the approved".
- **Earlier lapses exist inside the baseline.** 235ee46 (09-02, a verified-placements table in context-strata) was landed on a flow's own reading, and the living challenged it: "how did it go if I didn't approve?" In 6329f1, a flow authorized to work while the living slept made 09-04 edits to orchestrate (ede756f, 5716f71, 41f8366) and landed the dialect skills (datom, ethos, protos) before approval. Their bodies were approved on 09-12. 4197146, e5390b3 and 48d0122 lean the same way. These are sporadic and caught, not a pattern. They remain in the baseline, and the living may want to look at them.

Alternatives:
- **Earlier: 1b76791 (2026-09-02 14:31)**, the last revision before 235ee46. It has 38 skill files. It would also set aside the four harness skills and deepseek (approved on 09-05), the dialect skills, the main-flow locating lines, the testing and file-editing lines of 09-05, and the flow summary and bead closure rules of 09-08.
- **Later: 51d4922 (2026-09-18 08:13)**, after both of the living's permissions and before the 15-commit burst. It has 48 skills and 16,390 words. It would keep the f6db8d batch with the lines slipped into it, the lojix addendum, the refresh paragraph in main-flow, visual-report-from-md, operators-notes, subflow-scripts, herdr, the Terra psyche-audit paragraph and the new conflict rule in psyche.

## What the recovered set is

The recovered set is the baseline plus only the living's rulings of 09-27 and 09-28. It has 43 skills and 12,391 words. Where each ruling went:

- **Logging.** main-flow now says "The log holds the living's words and main events: a decision, a landing, a launch, a failure. Everything else is in the transcript." In psyche-interraction, the "it goes to log.md" clause was dropped.
- **One Primary workspace, and unsaved changes.** file-editing says all flows work in one Primary workspace and commit each change at once, and that changes found unsaved there are committed unless they look like nonsense. In other repositories, a commit names only the flow's own paths. "Commit existing dirty changes first" stands.
- **Regeneration.** skill-designing says a changed skill is committed and pushed at once, then the generated trees are regenerated and committed.
- **Conflicting records.** psyche takes the wording the living confirmed: a later explicit correction weighs most, and any other tension goes to the living. psyche-distillation was brought in line.
- **Kinds of skills.** skill-designing names four kinds once:
  - gold: unprefixed, the living's vision, changed only on his word;
  - `operation-`: deployed on the living's description and interpreted by the primary Mind seat, with no glance from him;
  - `test-` and `compensation-`: written by flows.

  In psyche-interraction, "Get approval before every skill edit" now points there. No documentation kind was made. No skill in the baseline has a prefix, so no reference had to follow the renames. In the review files, prefixed skills keep their old names, each with a note of its new name.
- **DeepSeek retired.** The skill is moved whole to `review/retired/deepseek-harness.md` with the living's sentence. **No skill covers the opencode harness.**
- **Already true or absent at the baseline.** Titles, route probes, refused sends, green builds and datom only where a tool reads it: the baseline text already agrees, or never mentions them.

## The review folder

`review/unapproved/` holds 23 files for baseline skills and 20 for skills created later. For a baseline skill, the file shows every later edit whole, as a diff against the baseline, with its commit, date, maker, the flow and reason where traced, and a view. For a later skill, it holds the whole skill as it stood on main. `review/retired/` holds 9 files: deepseek, field, metaflow, operational-status-presentation, operators-notes, subflow-scripts, testing-flow-titles, testing-harness-visual-state and testing-session-registry.

Tracing, for 74 commits after the baseline that touch unprefixed skills: about 51 were made with the living present and asking or approving, many of them only in part. About 17 were a flow's own judgment, and 6 are uncertain. So most edits had the living's word behind them. The growth came from the many rulings he gave, plus what flows added around them.

Sizes, main, then recovered:

| Skill | Main | Recovered |
|---|---|---|
| main-flow | 1,274 | 592 |
| psyche-interraction | 1,013 | 894 |
| claude-harness | 1,076 | 319 |
| psyche | 695 | 590 |
| lojix | 1,803 | 1,507 |
| testing | 392 | 190 |
| file-editing | 349 | 172 |
| subflow | 159 | 114 |
| field | 958 | not in the set |
| refresh | 678 | not in the set |
| messaging | 344 | not in the set |
| flow-communication | 477 | not in the set |

What was moved aside from these:
- main-flow: Field seats, titles, launcher first prompt, dispatch receipt, Terra and Luna, subflow scripts, and the Flow refresh section.
- claude-harness: operators' notes, input routes and skill visibility.
- lojix: the f6db8d body and the addendum.

## Candidates I would offer the living

These are not restored.

- **main-flow Flow refresh paragraph (4876988).** The living said "the wording is good". The workspace CLAUDE.md points at this section, and it is missing from the recovered set. This is the first to restore.
- **The f6db8d dialect bodies for datom, ethos, protos and lojix (2ef2b53).** They were approved. The Composing renames (02a3770, d6b5b07) match the released code.
- **datom's "a datom needs a type" and correction's "the cause is context, never the flow's care" (1cce102).** Both approved.
- **psyche-interraction.** The speech-to-text brackets and [sic] (8864d42), "a tier word names power" (60be395), and relaying the living's words verbatim with context (fec7c66). All with the living.
- **main-flow.** Every seat logs the living's words (0ffce58). The title is `<Aspect>V2.{ <Model> <FLOW_ID> }` (190ecfe). A named model means the other main seat (89992a2). One launcher-composed first prompt (43c6075, core only). A model the harness cannot run is launched as a subflow (2ef2b53).
- **The harness facts on skill visibility (3ab0251).** The living asked for these. The Claude input-route facts in 93e7b4d, which were the flow's own.
- **Approved by the living.** breaking-upgrades countdown rollback (0a62275), the nexus CLI and Signal boundary (fd99d0e), psyche-distillation "distill in the gathering conversation" (631f4d5), codex-harness model pinning (a7d2f4f is inside the baseline), vocabulary's "Field" (4526932), and nix-workflow's Nix-built tests and Rust-only repositories (21672ff, without the offload receipt).
- **Sound, but the flow's own.** Stop a process by its PID, confirm a push against the real remote, release locks before reporting (2ef2b53), and "do not wake a flow to test delivery" (7974b03, which rests on the living's words).
- **Whole skills.**
  - stale-lock (text approved) and compensation-nix with its rationale;
  - compensation-messenger-clj, trimmed, less the pane fallback;
  - visual-report-from-md, the flashbook pair, testing-generated-projection and testing-long-run-progress;
  - trimmed: herdr, voice-psyche (without Terra), operational-layer-communication, and the definitions in flow-aspect.

## What I was unsure of

- The trace counts are approximate. Several commits are mixed, and some quotes were relayed by other flows, not heard directly.
- Whether 3726da5's logging sentence has a recorded word of the living. The 8904b1 log records the approval: "the rest of my proposals stand approved, the logging sentence among them". I treated it as a ruling.
- Whether the baseline's own lapses of 09-02 to 09-04 should move the baseline earlier. I judged them sporadic.
- Whether the Primary one-workspace sentence means feature-development's isolated worktrees should also go. I left feature-development as it is.
- Commit attribution. The brief asked for a Claude Fable 5.1 trailer, but this session is Opus 5.5, so the commit says Opus 5.5.

## Sources

- Curriculum history: `git log` of `skills/` since 2026-06-26 (272 commits), and commits per day with trailers since 2026-08-15. Baseline a7d2f4f, alternatives 1b76791 and 51d4922. Main is 3726da5.
- The living's records: `flows/8904b1/vision/skills.md` (8904b1-13 to -17), `vision/anatomy.md` (8904b1-5 to -10), `vision/logging.md` (8904b1-12), `vision/datom.md` (8904b1-2 to -4), and the 8904b1 log.
- `flows/8904b1/reports/skill-garbage-audit.md`.
- The tracing subflows' findings, drawn from `/home/li/primary/flows/`, among them 403a1a, 564f55, f6db8d, 9e7c9f, 692df8, 82c299, 6cc91b, 9993b5, 108ab0, 908786, 1ac573, b05237, cf3553, 8393ca, b81560, 1b8ac0, 03e825, 753e69, 0347d0, 9ddcbc, 752e0f, d8df70, e51411, 38de5b, b860be, 995a164e, 6329f1 and 1a6ca4. Also Claude session transcripts under `~/.claude/projects/` and Codex sessions under `~/.codex/sessions/`.
- The branch: `review/README.md`, `review/unapproved/*.md` and `review/retired/*.md` at 992c3e8. Push read back with `git ls-remote https://github.com/LiGoldragon/Curriculum.git`.
