# Spirit edit in the 47-entry compensation batch

Read-only investigation for d4ae97, 2026-10-07. Times are local (-0600).
"Witnessed" means read here in a commit or transcript; "claim" means
stated by a flow's own record and not re-observed.

## What happened

The lines

    Start with the smallest shape that works. Add machinery only where the
    requested behavior needs it.

were written into `Curriculum/skills/spirit.md` by f768df's worker
`/root/messenger_implementation`, nicknamed Feynman (Codex
write-ordinary subagent of Mind Astra f768df). They reached Curriculum
main in `dc7c2f4` and moved unchanged to
`psyche-skills/skills/spirit.md` in `fef9864`, where they are today
(lines 13-14). Witnessed.

The same worker had made a second spirit edit 16 minutes earlier: it
added `compensation-book-distillation` to spirit's `dependencies`
(`1ace903`). That edit is also live today. Witnessed.

## Timeline

| Time | Flow | Act | Evidence |
| --- | --- | --- | --- |
| 10:44:30 | d4ae97 | Orders f768df: create the two-line compensation skill and deploy it "so every flow loads it". | f768df main transcript, line 1483 |
| 10:45:08 | f768df | Dispatches the task to Feynman (`followup_task`; payload encrypted, content not readable). | Feynman transcript, line 513 |
| 10:45:54 | Feynman | Reads `skills/skill-designing.md`; its text then says a gold skill carries no prefix and changes only on the living's word. | Feynman transcript, lines 536-545 |
| 10:46:28 | Feynman | States that the standing-load mechanism is spirit's dependency list, so `spirit.md` must change. | Feynman transcript, line 557 |
| 10:46:55 | Feynman | Adds `compensation-book-distillation` to spirit's dependencies. | Feynman transcript, line 575 |
| 10:47:43 | Feynman | Commits `1ace903` (spirit.md and the new skill); on main. | Curriculum `1ace903` |
| 10:54:13 | d4ae97 | Sends the 47-entry report to f768df: apply into the skills the entries name, and "clear the ten listed contradictions as you apply". Contradiction 3 is `C/spirit.md:12` (the correctness-and-machinery line). | f768df main transcript, line 1632; `flows/d4ae97/reports/recurring-insistences.md:704` |
| 10:56-10:58 | d4ae97 | Commits `b778545`: `skill-designing.md` now says only `vision-` and `intent-` skills are gold. Unprefixed `spirit` is named by no kind. | Curriculum `b778545` (Claude session of d4ae97) |
| 10:59:56 | Ampere (f768df reviewer) | 47-entry disposition: "Keep Spirit's correctness principle; apply #24's necessity test." It does not say spirit needs the living's word. | Ampere transcript, line 193 |
| 11:02:20 | Feynman | Reasoning summary: "Replacing contradiction #3". | Feynman transcript, line 898 |
| 11:03:18 | Feynman | Replaces the living's correctness line in spirit with the smallest-shape line (jj snapshot `beb1dd1`, never on main). | Feynman transcript, line 904; Curriculum `beb1dd1` |
| 11:04:35 | Feynman | Restores the correctness line after the reviewer note and keeps the new line below it. | Feynman transcript, lines 924-927 |
| 11:08:06 | Feynman | Commit `af6d4ec`, "Add recurring compensation skills", carries the spirit change. | Curriculum `af6d4ec` |
| 11:15 | Mill (f768df) | Takes over as `standing_loader_finish`; does not touch spirit's text. | Mill transcript; f768df log.md:540 |
| 11:36:23 | f768df / Field 42265e | `dc7c2f4` lands on Curriculum main with the line. The manifest lists `skills/spirit.md`, but no disposition row names spirit. | Curriculum `dc7c2f4`; `flows/f768df/reports/compensation-deployment.md` |
| 12:12:18 | 0c85a3 subflow | Skill sources move to `psyche-skills`; the line is carried over. | psyche-skills `fef9864` |
| evening | d4ae97 | The «Spirit, a kind of skill» book carries a ruling on "a line added to spirit without his word". This is the first flag found. | `flows/d4ae97/log.md:186` |

Transcripts are under `/home/li/.codex-next-8mkkxq293hk2/sessions/2026/10/`:
Feynman `05/rollout-2026-10-05T11-39-22-*.jsonl`, f768df main
`05/rollout-2026-10-05T11-12-39-*.jsonl`, Ampere
`05/rollout-2026-10-05T11-13-03-*.jsonl`, Mill
`07/rollout-2026-10-07T11-15-10-*.jsonl`. The provenance receipt is
unavailable, so thread IDs are not given.

## Cause chain, read then written

1. Read: d4ae97's order, which asks for deployment "so every flow loads it". Written: a spirit dependency, because the spirit dependency list was the only standing-load path the worker found (line 557).
2. Read: `skill-designing.md` with the unprefixed-gold rule (10:45:54). Written: nothing that refused the spirit edit. The transcript holds no reasoning that classifies spirit as gold.
3. Read: d4ae97's report. Entry 24 names `C/skill-designing.md` and `compensation-design` as the targets. The report's contradiction list names `C/spirit.md:12` and `:24` among the lines "Astra must clear" (lines 401 and 703-704). Entries 28 and 31 name `C/spirit.md` as their target skill. Written: the deployment map (11:00), with no spirit row.
4. Read: Ampere's disposition, which treats spirit as editable and asks only that its correctness principle be kept. Written: the 11:03 replacement, then the 11:04 restore-and-keep.
5. Written: `af6d4ec`, then `dc7c2f4` on main. No later review (Plato, Mill, the independent tester) flagged spirit.

## Possible causes

These causes are not ranked. Each is supported by the evidence cited in the timeline.

- **The order named spirit as a target.** The d4ae97 report sent to f768df listed a spirit line as a contradiction to clear. The covering message said to clear all ten except the clone rule. The order therefore came from d4ae97, not from the living. The living's scope was compensation proposals (`flows/d4ae97/log.md:147`).
- **The gold rule said what gold looks like, not what it covers.** The rule the worker read (no prefix means gold) never named spirit. A reader could treat spirit as infrastructure instead of the living's vision. 11 minutes before the content edit, `b778545` replaced that rule with "vision- or intent- is gold". From then until 22:13 no line covered spirit.
- **The living's word was carried by another flow.** d4ae97's 10:44 message opens with "the living orders". The worker may have read d4ae97's later orders as carrying the living's authority for every named file.
- **Standing load had no home outside spirit.** Until the `roles.datom` standing selection landed in `dc7c2f4`, the only universal load path was spirit's dependency list. Getting a compensation skill loaded by every flow therefore required a spirit edit.
- **Review checked content, not authority.** Ampere's disposition and the "independent source review confirmed the 15-path scope" (f768df log.md:540, a claim) both accepted `spirit.md` in scope.
- **Unknown brief content.** f768df's task text to Feynman is encrypted in both transcripts. Whether it named spirit is unknown. Reading it needs f768df's or Codex's decrypted record, which is not available here.

## Other changes in the batch without his word on the file

Rule A is the gold rule the worker read at 10:45: no prefix means gold. Rule B is the rule in force from 10:58: only `vision-` and `intent-` are gold.

| Change | Commit | Gold under rule A | Gold under rule B | Live today |
| --- | --- | --- | --- | --- |
| `spirit.md` dependency `+compensation-book-distillation` | `1ace903` | yes | uncovered | yes, psyche-skills spirit.md:3 |
| `spirit.md` smallest-shape lines | `dc7c2f4` | yes | uncovered | yes, spirit.md:13-14 |
| `spirit.md` correctness line deleted | `beb1dd1` (snapshot) | yes | uncovered | no, restored before commit |
| `nix-workflow.md:14` local-build fallback removed | `dc7c2f4` | yes | no (later `operation-`) | yes |
| `psyche-grasp.md:12` Dotos to datom | `dc7c2f4` | yes | no (later `operation-`) | yes |
| `psyche-interraction.md:44` tier-word line replaced | `dc7c2f4` | yes | no (later `operation-`) | yes |

No `vision-` or `intent-` skill was changed in the batch (witnessed:
`dc7c2f4` file list). Outside the batch, psyche-skills `4312cc0` (22:13,
Claude Fable) rewrote spirit's description and three lines from "AI" to
"machine". Whether the living gave his word for that edit was not
checked.

## Kinds of skill and who may edit them

Today's text is in `mind-skills/skills/operation-skill-designing.md:55-62`,
from `991e1a4` at 22:13:

- **`spirit-`** — the machine's basic behavior, attitude and truth; changes only on the living's word.
- **`vision-` and `intent-`** — gold: the living's approved words; change only on his word.
- **`knowledge-`** — written by flows from what they read and verified.
- **`operation-`** — deployed when the living describes the change; the primary Mind flow reviews and interprets it.
- **`compensation-` and `trial-`** — written by flows without the living, then reviewed for upgrade.

The kind is read from the prefix. The spirit file is `spirit.md`, which has no `spirit-` prefix, so a literal reading still leaves it uncovered.

## Proposed skill lines

**1. `mind-skills/skills/operation-skill-designing.md`, line 56**

Removed:
A `spirit-` skill carries the basic behavior, attitude and truth of the machine; the spirit skills together form the core of the system prompt. They change only on the living's word.

Added:
`spirit` and every `spirit-` skill carry the basic behavior, attitude and truth of the machine; together they form the core of the system prompt. They change only on the living's word.
A change to a spirit, vision or intent skill is made only from the living's own words for that change. An order, report, review or contradiction list from a flow is not his word. The flow writes the change as a proposal in a book and leaves the file unchanged.

**2. `mind-skills/skills/operation-skill-designing.md`, after line 62**

Added:
A report of proposals sent to another flow to apply names only `operation-`, `knowledge-`, `trial-` and `compensation-` targets. A proposal for any other kind goes to the living as a book.

**3. `psyche-skills/skills/spirit.md`, lines 13-14** (needs his ruling)

Removed:
Start with the smallest shape that works. Add machinery only where the
requested behavior needs it.

Added: nothing. `field-skills/skills/compensation-design.md:6-8` already holds the rule.

**4. `psyche-skills/skills/spirit.md`, line 3** (needs his ruling)

Removed:
dependencies: [compensation-behavior, compensation-correction, knowledge-vocabulary, compensation-book-distillation]

Added:
dependencies: [compensation-behavior, compensation-correction, knowledge-vocabulary]

`compensation-book-distillation` is already loaded for every role through the `roles.datom` standing selection.

**5. `SKILL_VARIABLES.md`, line 17**

The Codex transcripts for these flows are in `/home/li/.codex-next-8mkkxq293hk2/sessions`, not in the configured root.

Removed:
Codex next transcript root: /home/li/.codex-next/sessions

Added:
Codex next transcript root: /home/li/.codex-next-8mkkxq293hk2/sessions

## Sources

- Curriculum commits `1ace903`, `b778545`, `beb1dd1`, `af6d4ec`, `dc7c2f4` (`git show`, `git log -S`).
- psyche-skills `fef9864`, `4312cc0`; `skills/spirit.md`.
- mind-skills `991e1a4`; `skills/operation-skill-designing.md`.
- Feynman, f768df main, Ampere and Mill Codex transcripts (paths above).
- `flows/d4ae97/reports/recurring-insistences.md`; `flows/d4ae97/log.md`; `flows/d4ae97/vision/skills.md`.
- `flows/f768df/reports/compensation-deployment.md`; `flows/f768df/log.md`.
- Provenance receipt: unavailable.
