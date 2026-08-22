# Remembering 5c8be3ca

Single-layer remembering, by subflow of b7465e71.

## The contextualized psyche

Eleven rulings, all in `psyche-raw/Vision/flowArtifacts.md`, lines
3-117. Verbatim psyche words:

**5c8be3ca-1** (line 9): "no of course not! the directory gives the flow. only subflows need to indicate their id"

**5c8be3ca-2** (lines 16-20): "there's no handoff file; the flow *reads its previous flow(s)* - it's the inverse of push dont pull, since LLM flows are totally different than regular software (non deterministic); the new flow needs to make its own view of the old; we are refreshing for that very reason, so imposing the old opinion on the new flow is the wrong approach."

**5c8be3ca-3** (line 28): "then we should drop the idea"

**5c8be3ca-4** (line 33): "lets make it simple, in workspace for now."

**5c8be3ca-5** (lines 39-40): "the context-handover skill could be renamed, as its used to generate prompts manually for other flows which are copy pasted manually."

**5c8be3ca-6** (lines 49-57): "1. subdirectories; easier to search / 2. what is pronouncement? Is that an established vocabulary? we need to establish the anatomy of the flow and llm based engineering. research this / 3. Awareness isnt used in this context anymore, root that out. the statement is good though / 4. yes that's good"

**5c8be3ca-7** (lines 64-67): "a lot of your negative rules are context confusion. dont involve the refusals with the composition. See you understand with a skill design proposal, and repropose the protocol; I need to see the skill proposal itself"

**5c8be3ca-8** (lines 73-74): "lets create a file for external edits. annotations.md? and will agents know what is a witness?"

**5c8be3ca-9** (lines 82-84): "this is just noise. models will do this naturally / great, let's land this"

**5c8be3ca-10** (lines 93-108): "body leaking into description. skill design description training proposal? / was session-log removed? / I want a prompt for another flow to migrate all the artifacts that can be pinpointed to a session file, along with all the psyche logs, etc. Do you understand what I mean by that? / re divergence: are you session a flow implemented both protocols? then a merge is in order. to be done by the fore mentionned external flow / rewording is better. / delay the vocabulary expansion. We'll start a new session after this"

**5c8be3ca-11** (lines 112-117): "no, psyche records that can be traced will also be moved. / spiritbackup.nota sounds like a really old artifact."

## High-level awareness of the work done

Flow 5c8be3ca was a design session with the psyche on 2026-08-21 and
2026-08-22. Its subject was the flow-artifacts protocol: the system by
which anything a flow produces that has no specific home repository
gets filed under `flows/<short-id>/`. The flow produced the protocol
design, got it approved, and landed the `flows` skill as a replacement
for the old `session-log` skill.

The main decisions were: the directory gives the flow (no origin marks
in files); no handoff file (a successor reads its predecessors and
forms its own view, because LLM flows are non-deterministic); subflow
marking dropped (a subflow cannot see its own id); the structure lives
in the workspace for now; `context-handover` renamed to
`prompt-crafting`; kind subdirectories (`witnesses/`, `reports/`);
external edits go in `annotations.md`.

The flow also produced two research reports (prior art on
flow-artifact protocols, and flow-anatomy vocabulary research),
witnessed Claude Code subagent identity behavior (shared session id,
per-subflow agentId), inventoried the old workspace artifacts,
surveyed and rooted out current uses of "awareness", and delivered a
migration prompt for a follow-on flow to execute.

Left open at flow end: the "pronouncement" vocabulary entry (delayed
by the psyche to a new session); the superseded-marking of
VISION-2026-08-07.md line 566; the description-leak training line
proposed for skill-designing ("Nothing of the skill's body appears in
the description.").

## Things touched, lightly audited

**`flows` skill** (`.claude/skills/flows/SKILL.md`): Exists and is
live. Two differences from the proposal in the protocol design
document (`design/Flows/flowArtifactsProtocol-2026-08-21.md` lines
112-142): (1) the current skill adds `vision/<topic>.md` to the
directory tree and a paragraph "A psyche record goes in
`vision/<topic>.md`, the psyche's words verbatim" that the original
proposal did not have; (2) the current skill omits the paragraph about
creating `log.md` at first prompt, appending to the index, and the
log's terse-summary editing pattern. The `vision/` addition came from
a later flow (the corpus rename commit a37a2422f mentions "flows
vision/"). The log-creation paragraph's absence means that instruction
is carried only in the protocol design document, not in the deployed
skill itself. (Parallel witness, this flow: the authored source
`/git/github.com/LiGoldragon/Curriculum/skills/flows.md` does carry
the paragraph — the deployed copy is stale; regeneration owed.)

**`prompt-crafting` skill**: Exists. Description "A prompt must be
crafted for another flow." and body "The crafted prompt is printed
once, in the response, for the caller to paste." match the final
landed state (5c8be3ca-10 reword approved).

**`session-log` skill**: No longer exists under `.claude/skills/`.
Removal witnessed.

**`skill-designing` skill**: The proposed description-leak line
("Nothing of the skill's body appears in the description.") is not
present. The skill has the inverse-direction line ("Nothing in a
description appears in the skill.") which does not cover the same
failure class the flow flagged.

**Protocol design document**
(`design/Flows/flowArtifactsProtocol-2026-08-21.md`): Exists, 207
lines, intact.

**Research reports**: Both exist at
`flows/5c8be3ca/reports/flowArtifactsPriorArt.md` and
`flows/5c8be3ca/reports/flowAnatomyVocabulary.md`.

**VISION-2026-08-07.md line 566**: "The awareness file supersedes the
reset bead as the session carrier" still present at
`design/ProtosEngine/VISION-2026-08-07.md` line 566, unmarked as
superseded. Still open.

**`sessions/` directory**: Still exists with `design/`, `design.log`,
`index.md`, `realization/`. The divergent double-protocol log
`sessions/design/15b67974.md` no longer exists — its merge or removal
was handled by a later flow. (The migration flow the psyche ordered in
5c8be3ca-10 appears in the index as acquisition flow 01a02a06,
currently running: "no migration begun".)

**"pronouncement" vocabulary entry**: Not present in the vocabulary
skill or any `Vision/` or `Intent/` file. Still undelivered, as the
psyche delayed it.

**`psyche-raw/Vision/flowArtifacts.md`**: Holds all eleven rulings. No
distilled counterpart at `Vision/flowArtifacts.md` yet.

**`flows/index.md`**: Lists 5c8be3ca; format matches the protocol.

## Chain links

**Predecessors**: no direct predecessor flow; a new design session
grounded in psyche records from sessions 06196cc7, fb1008c0, 7c3f0c1d,
e06e4c07, and 98fbfa47.

**Successors and references**: 15b67974 (annotated by 5c8be3ca —
`flows/15b67974/annotations.md` lines 3-11, the divergent session
log); 2b34fafa (uses the 5c8be3ca protocol, `flows/2b34fafa/log.md`
line 56); b7465e71 (this flow, remembering it).

## Sources

- Method: code read `/home/li/primary/flows/5c8be3ca/log.md`
- Method: code read `/home/li/primary/psyche-raw/Vision/flowArtifacts.md`
- Method: code read `/home/li/primary/.claude/skills/flows/SKILL.md`
- Method: code read `/home/li/primary/design/Flows/flowArtifactsProtocol-2026-08-21.md`
- Method: code read `/home/li/primary/.claude/skills/prompt-crafting/SKILL.md`
- Method: code read `/home/li/primary/.claude/skills/skill-designing/SKILL.md`
- Method: code read `/home/li/primary/.claude/skills/vocabulary/SKILL.md`
- Method: code read `/home/li/primary/flows/15b67974/annotations.md`
- Method: code read `/home/li/primary/flows/b7465e71/vision/remembering.md`
- Method: code read `/home/li/primary/flows/index.md`
- Method: code read `/home/li/primary/design/ProtosEngine/VISION-2026-08-07.md` (lines 564-568)
- Method: probe `ls /home/li/primary/.claude/skills/session-log/` (not found)
- Method: probe `ls /home/li/primary/sessions/design/15b67974.md` (not found)
- Method: probe `ls /home/li/primary/flows/5c8be3ca/reports/`
- Method: probe `grep -n "pronouncement" /home/li/primary/.claude/skills/vocabulary/SKILL.md` (no hits)
- Method: probe `grep -rn "5c8be3ca" flows/*/annotations.md flows/*/log.md`
- Carried claim: `flows/5c8be3ca/log.md` for session narrative and dispatch records
- Flows: 5c8be3ca (subject), e06e4c07 (grounding), 15b67974 (annotated), 2b34fafa (successor reference), b7465e71 (this flow)
