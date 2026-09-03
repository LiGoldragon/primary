# Concurrent Psyche-Interaction Flow

Report prepared by b9f4f6 subflow on 2026-09-03. Scope: identify the
flow the psyche referred to on 2026-09-03T12:13 UTC as "another flow
actually addressing almost exactly the same points" as b9f4f6's
psyche-interraction corrections.

---

## 1. Identity: flow a5940a

**Index entry 153** (flows/index.md):

> realization, a5940a, Investigate flow d30eb1's main-thread command
> behavior and land the approved main-flow delegation correction.

**Flow log**: flows/a5940a/log.md.

**Codex session**: `01a0635e-8508-7782-9312-1fba5940a0db`.
Session file: `/home/li/.codex/sessions/2026/09/02/rollout-2026-09-02T20-25-33-01a0635e-8508-7782-9312-1fba5940a0db.jsonl`.

The flow opened 2026-09-02 in response to the psyche's complaint that
flow d30eb1's main thread had run giant commands instead of delegating
to child flows.

Candidate 4ad49f was examined and ruled out: its session (from 4ad49f
log) was a ChatGPT Desktop stock-boundary rollback with no
skill-correction content.

Candidate 4decf7 was examined and ruled out: its log and transcript
concern datom/ethos/protos/nexus/sema/signal distillation; the
psyche's 11:54 UTC message to that session ("show me the distillation
proposal. kinds are qualifier-named") is about datom content, not
psyche-interraction corrections.

---

## 2. What the psyche said there

All quotes are from Codex history `/home/li/.codex/history.jsonl`,
session `01a0635e-8508-7782-9312-1fba5940a0db`.

**2026-09-02T18:26:06 UTC** — opening instruction:

> $main-flow $spirit $psyche $psyche-interraction $behavior
> $realization $operating-system $edit-coordination
>
> find out wtf d30eb1 was doing. its main flow transcript is full of
> giant commands, which it should never have run as a main flow.

-- psyche, typed (history record).

**2026-09-02T18:28:21 UTC**:

> I still want to know what the flow's task was!

-- psyche, typed.

**2026-09-02T18:30:32 UTC**:

> ok I dont care about the rest, tell them to report what they found
> so far and summarize. dont waste a bunch of tokens on this

-- psyche, typed.

**2026-09-02T20:03:00 UTC**:

> any skill edit recommendation to avoid this outcome again?

-- psyche, typed.

**2026-09-02T20:08:44 UTC**:

> isnt some of this already in the skill?

-- psyche, typed.

**2026-09-02T20:10:32 UTC** (on the flow's use of "task witnessing"):

> what is task witnessinga/

-- psyche, typed. (apparent STT artifact in "witnessinga/")

**2026-09-02T20:15:44 UTC** (on "return evidence gaps to a child
flow"):

> return evidence gaps to a child flow
>
> explain. I cant clearly understand that

-- psyche, typed.

**2026-09-03T11:57:23 UTC**:

> recap the proposal

-- psyche, typed.

**2026-09-03T12:02:51 UTC** — approval:

> ok. land it

-- psyche, typed.

These are the psyche's only typed messages in this session per the
Codex history. The session contained no psyche-logged vision and the
flow log says it adds no Vision entry.

---

## 3. Lines proposed and landed

### Proposed (from session transcript, assistant responses)

Initial proposal (not approved in this form):

> Run all investigation, implementation, and verification tool calls
> in child flows.
> Return evidence gaps to a child flow.
> The parent manages the flow tree, loads applicable skills, and reads
> or writes only beads, reports, design documents, the psyche log, and
> the parent session log.

Revised proposal (after psyche questioned "task witnessing"):

> Delegate task work, probes, and verification to child flows. Relay
> their findings by origin and return evidence gaps to a child flow.

Final approved form (from the flow's last model response and the a5940a
log):

Replace:
> Delegate task work to child flows.

With:
> Delegate task work, probes, and verification to child flows.

Add:
> Relay child findings with their origin. When more evidence is
> needed, ask a child to obtain it.

### Psyche approval

Approved at **2026-09-03T12:02:51 UTC**: "ok. land it"

### Committed to Curriculum

Commit `28f7953ff78116d0e0270cc60196dd92b6825446`,
2026-09-03 14:09:17 +0200 (Europe/Paris),
message: "Delegate probes and evidence gathering to child flows".
File changed: `skills/main-flow.md` only.

No psyche-interraction.md was touched by this flow. No behavior.md
was touched.

### Regenerated to Primary

Primary commit `799ddc3ee` ("Regenerate main-flow projections") carries
the updated generated projections. Witnessed in the main flow: Primary
has both approved lines in `.agents/skills/main-flow/SKILL.md`.

---

## 4. State of a5940a and Curriculum edit status

**a5940a state**: The flow log records the approval and landing as
complete. The Curriculum working tree is clean (verified: `git -C
/git/github.com/LiGoldragon/Curriculum status` → "nothing to commit,
working tree clean"). The flow appears done.

**Curriculum HEAD position**: The Curriculum checkout is at detached
HEAD `3872f96` (the b2da01 flow's commit), one commit behind `28f7953`
(a5940a's commit). This is a checkout state, not an uncommitted change.
The remote at `28f7953` is current.

**Uncommitted psyche-interraction.md changes**: None. The last edit to
`skills/psyche-interraction.md` in Curriculum is `ae972e7`
("Add synthesis provenance rule and extend pre-asking instruction",
2026-09-02T22:19:58 +0200), which was b9f4f6's own approved landing.
No other flow has a psyche-interraction edit in flight.

**Edit coordination implication**: No lock coordination is needed
before b9f4f6 proposes further psyche-interraction lines; the Curriculum
file is clean and no other flow has stated an intention to edit it.

---

## 5. Psyche preferences observed in this flow's session

The psyche's messages in the a5940a session state several preferences
directly relevant to this flow:

- **Do not waste tokens on lengthy summaries**: "ok I dont care about
  the rest, tell them to report what they found so far and summarize.
  dont waste a bunch of tokens on this." (2026-09-02T18:30)

- **Conciseness matters**: the psyche cut off the investigation after
  the flow had been running and asked for the summary early.

- **Delegate probes to child flows, not the parent**: the psyche's
  frustration was that d30eb1's parent ran giant commands. The approved
  wording ("Delegate task work, probes, and verification to child
  flows") makes explicit that probes and verification are child work.

- **Relay findings with origin**: the approved line "Relay child
  findings with their origin" addresses the presentation side — the
  parent should say where information came from, not just assert it.

---

## 6. Relation to b9f4f6's concerns

The a5940a flow's corrections address the same class of problem as
b9f4f6's psyche-interraction corrections, but at the main-flow level
rather than the psyche-conversation level:

| b9f4f6 concern (psyche-interraction) | a5940a correction (main-flow) |
|--------------------------------------|-------------------------------|
| Don't present while subflows outstanding | Delegate probes and verification to child flows |
| Relay content, not file paths | Relay child findings with their origin |
| Synthesis must carry claim origin | Same: relay by origin |

The psyche observed both failures in the same period (2026-09-02 to
2026-09-03) and the two flows ran concurrently.

---

## 7. What was not found

- No evidence that a5940a proposed or landed any psyche-interraction.md
  line. Its Curriculum commit touched only main-flow.md.
- No other flow active in 2026-09-01 to 2026-09-03 was found to have a
  psyche-interraction edit in flight or a stated intention to propose
  such an edit.
- The psyche's exact words about a5940a being the "other flow" were not
  found in the Codex history for session 01a0635e. The identification
  relies on: (a) timing (a5940a was active when the psyche said "another
  flow"), (b) subject overlap (both flows correct flow behavior in the
  psyche's direction), and (c) no other candidate was found. This is an
  inference, not a witnessed match.

---

## Sources

- flows/index.md, entries 151–154
- flows/a5940a/log.md
- flows/4ad49f/log.md
- flows/4decf7/log.md
- flows/b9f4f6/log.md
- flows/b9f4f6/vision/presentation.md
- /home/li/.codex/history.jsonl — session 01a0635e-8508-7782-9312-1fba5940a0db (all psyche messages)
- /home/li/.claude/history.jsonl — session e1d79fd3-d374-45d5-a84e-ff5b9f4f6681 (psyche's "another flow" message)
- /home/li/.claude/history.jsonl — session 4decf7af-9e62-4ea9-8df0-d34602c8f4c2 (ruled out)
- /home/li/.codex/sessions/2026/09/02/rollout-2026-09-02T20-25-33-01a0635e-8508-7782-9312-1fba5940a0db.jsonl (assistant responses, proposed wording)
- git -C /git/github.com/LiGoldragon/Curriculum log: commits 28f7953, ae972e7, 3872f96
- git -C /git/github.com/LiGoldragon/Curriculum show 28f7953 (exact diff)
- git -C /home/li/primary log --oneline -5 (Primary state, commit 799ddc3ee)
- /home/li/primary/.agents/skills/main-flow/SKILL.md (deployed state witnessed)
