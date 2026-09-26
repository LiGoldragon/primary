# Launch

## Skills loaded one prompt after another are inefficient

Context: d8df70's launch had loaded its skills in separate prompts (`/spirit`, `/main-flow`, `/testing-flow-titles`, `/refresh`, `/psyche`), each followed by a model turn.

> Create a bunch of flashbooks with everybody's main flow from the recent presentation that they left in their transcript, including your own, and do an audit on the fact that you were loaded with the prompts broken up. I don't know. I feel like it's inefficient. Did you have your model changed halfway or something? The way your skills were loaded, one after another, is really inefficient because then you talk and then it's a bunch of LLM calls. It's really inefficient.

-- psyche, STT (inferred), 2026-09-23 22:02Z, to Psyche Medium d8df70; recovered by 88475f from d8df70's transcript (session d8df703d, line 387). The first sentence is a working instruction, kept for context.


## A fresh flow starts from one prompt, with /main-flow in it

Context: said to Psyche Medium e51411 after it corrected who sent `/main-flow`. The launcher had sent `/main-flow` as a second prompt after the first one, because the harness does not let the model load it through the Skill tool.

> Well the real mistake was that the /main flow should have been in there. There should be only one prompt when we start a fresh flow, not two, because then that costs more money and it's less efficient.

-- living, input mode not established, 2026-09-24, to Psyche Medium e51411. Reading note (inference): "the /main flow" is `/main-flow`, and "in there" is the first prompt.

## Skill commands belong in the original prompt; several /skill commands in one Claude prompt have worked

Context: follows the entry above. This seat had said that probably only a leading slash command expands in Claude.

> So the command should have been in the original prompt. Is there a problem with putting a bunch of skill commands in the Claude initial prompt, because there isn't in Codex?

> Well I was putting in the /skill command style in Claude for a long time and it was working. Do you want to test this with a haiku model or something?

-- living, input mode not established, 2026-09-24, to Psyche Medium e51411, two consecutive messages. Tested afterward; see flows/e51411/reports/multi-skill-first-prompt.md and one-block-startup-prompt.md.

(Merged from flows/e51411/vision, the living's words to Psyche Medium e51411, 2026-09-24; kept as e51411 logged them.)
