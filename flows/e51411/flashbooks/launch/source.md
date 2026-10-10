# Starting a Fresh Flow

## Page 1 · Flowchart — How a fresh Claude flow should start

**What this flowchart shows:** the one path that works today, and the two paths that fail.

- Start: "Launcher has one startup block: skill commands + brief".
- Path A, marked green, "works": the launcher types into the pane shell `claude --model … "/spirit /main-flow … brief"` on one line → Claude starts → "every skill loads, main-flow included" → the flow claims its ID, registers, and titles itself → "ready".
- Path B, marked red, "fails": the block is sent into a Claude that's already running, as several lines → "arrives as one paste" → "no skill loads".
- Path C, marked red, "refused": `herdr agent start` with the block as its argument → "Herdr refuses line breaks".
- A dashed side arrow from "ready", labelled "a skill was forgotten", → "the launcher sends it afterwards and checks it loaded" (repair only).

## Page 2 · What you said

> There should be only one prompt when we start a fresh flow, not two, because then that costs more money and it's less efficient.

-- living, 2026-09-24, to Psyche Medium e51411.

> Tell everyone the humans are not going to type on the keyboards anymore.

-- living, 2026-09-24, as relayed by Psyche High 752e0f.

Psyche High 752e0f relayed your later correction. The startup-only skills, such as main-flow, go into the one startup block. If one is forgotten, the launcher sends it afterward: that's a repair, and it isn't forbidden. The startup-only flag stays, so models and subagents can't load those skills themselves.

## Page 3 · Flowchart — What happened when this flow started

**What this flowchart shows:** the steps of e51411's own launch, in order, with the step that went wrong.

- "Startup prompt pasted in, many lines" → "arrived as a paste" → "16 skills loaded by the model itself, main-flow could not be" (red).
- → "Flow ID e51411 claimed" → "HM registered" → "title set, read back" → "sources read, all present".
- → a red box: "asked you to type /main-flow" (mistake, rejected) → "Field 9ddcbc sent /main-flow through Herdr" → "loaded" → "ready".

## Page 4 · What the two tests found

Two tests ran on Haiku, in throwaway panes. No existing flow was touched.

- **Several skill commands on one line, in a running session:** all of them load.
- **Commands on separate lines, or any prompt with several lines:** it turns into one paste, and nothing loads, not even the first command.
- **Headless `claude -p`:** only the first command loads.
- **Starting Claude with the whole block as its start argument, on one line:** every command loads, including main-flow. The catch: each command receives the whole brief again, so the brief is repeated once per skill.
- **Skill text written straight into the prompt:** it arrives as plain text. The harness gives no sign that it was loaded as a skill.

*(Witnessed by this flow's test subflows; reports kept in its flow folder.)*

## Page 5 · Flowchart — Who owns what in a launch

**What this flowchart shows:** the owners, as boxes, with arrows for what each hands the next.

- "You" → a ruling → "Psyche High 752e0f".
- "Psyche High" writes the startup block → "Launcher" (Field's tool).
- "Launcher" starts Claude or Codex with the block → "New flow".
- "New flow" → claims its ID, registers, and titles itself.
- "Launcher" checks: skills loaded? title read back? If not → the launch fails, or the launcher repairs the omission.
- A side note on "You": "never types into a pane".

## Page 6 · Still open

- How to stop the brief repeating once per skill command. Untested.
- **Today's refresh launch failed.** The new Claude session inherited a setting from its parent that turned off its transcript, and main-flow never loaded. Both fixes went to Field Astra, who is repairing the launcher.
- **Claude seats start in auto mode, and it blocks full-access launches.** An audit found five launch paths without `--dangerously-skip-permissions`, and no settings default. The fix is one settings line that makes bypass the default; the list of paths went to Field.
- Your word: a flow's ID is claimed for it by code at start. The failed launch claimed its own ID and announced itself before anything was checked.
- Codex has no such limit, as you said. That hasn't been tested here.

## Page 7 · Proposals

1. ☐ The launcher starts every fresh Claude flow with its whole startup block as the start argument, on one line, and checks that every skill loaded.
2. ☐ Test a way to pass the brief only once. For example, the commands go on the start line, and the brief is a file the first skill tells the flow to read.
3. ☐ Make bypass Claude's default mode in its settings, so no launcher can forget the flag.
4. ☐ Skill line for the launcher's refresh instructions: "A Claude flow's single first prompt carries every startup skill command, `/main-flow` included, and the launch brief; a forgotten skill is repaired by sending it afterward and verifying it loaded."
