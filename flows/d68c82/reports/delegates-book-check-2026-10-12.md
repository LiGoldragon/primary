# Check of «The main flow delegates» (33752b, book 8)

Checked 2026-10-12 by a subflow of d68c82. The published page (version 1791822512-b614) has the same text as the source `flows/33752b/books/8-main-flow-delegates.md`; the renderer added nothing. Every statement below was compared with the packet (subject A), the raw records it cites, `vision-raw/managementDelegation.md`, the current `psyche-skills` `vision-flow.md` and `vision-model-roles.md` (origin/main 9bba4bf), `mind-skills` `operation-main-flow.md`, `field-skills` `compensation-launch.md`, and `.claude/agents/`.

Classes: S supported, U unsupported, C contradicted, M a machine-coined term or mechanism.

## Verdict in one paragraph

The book is not a pile of fabrications. Its core does rest on his records: the main flow does not do the work; subflows are tailor-made and pre-prompted; briefs are one or two lines; a subflow escalates instead of being micromanaged. The faults are specific. The proposed line widens what he said: "most expensive", "everything it must know", "every search, edit, build and probe". It drops the exceptions he gave himself. It mixes in wording from machine skills. It welds a count onto a date range that the count does not cover. It ignores two lines already in the target file that conflict with it. It also states his words back to him.

## Statement by statement

### Figure

| Statement | Class | Evidence |
|---|---|---|
| MAIN FLOW, context kept clean | S | 6cc91b mainFlow 2026-09-14 "not waste context"; 0d557b 2026-09-09 "so that you don't use your context too much"; vision-raw managementDelegation 2026-08-09 "the manager's context is gold … keep his hands clean". |
| does no task work | S in substance, M in wording | b05237 2026-09-18 "You're a main flow. You don't do stuff." The phrase "task work" is machine wording, taken from `operation-main-flow` "Delegate all task work." (mind-skills), which the brief `33752b/reports/packet-2-brief.md` A2 put next to the records. |
| one or two lines | S | 9fb0ad / 41fa34 / dea0ba 2026-10-03 typed: "you just send them one or two lines, very extremely brief". |
| unclear way: escalates back | S, one record | managementDelegation 2026-08-09: "train subagents to escalate back to their parents if the way to proceed forward isn't clear". He said it of a steward ("manager"). Reading that as the main flow is the book's inference, and the book does not mark it as one. |
| TAILOR-MADE SUBFLOW | S | 28d847 / edf227 2026-10-03: "the fucking agent that's tailor-made for this". |
| pre-prompted definition | S | e5a0bc 2026-10-06 "a sort of pre-prompted book-publishing sub-agent"; 41fa34 / edf227 / 5578cc "That's what subagent definitions are for." |
| holds all it must know | overreach of S | 9fb0ad: "roles that already have **almost** everything they need to know". |

### Opening paragraph

| Statement | Class | Evidence |
|---|---|---|
| "You have said this from 2026-08-09 … to 2026-10-06, in twenty-six flows" | C as one claim | The packet counts 26 flows over 2026-08-22 to 2026-10-06, all under `flows/`. The 2026-08-09 record is in `vision-raw/`, so it is not one of those flows. The book joined the packet's count to a start date from another set (counted again here: 36 records, 26 distinct flow ids). The 26 flows also include records the packet itself sets aside: impurities (01a02a06, 01a030df, 8393ca, 752e0f «as shipped»), records already covered by `intent-startup-prompt` (162eb3, 9e7c9f), and HTML-conversion practice (62022e8f, 995a164e). "You have said this" in 26 flows therefore overstates what he said. |
| "(the manager's context is gold)" | S as a quote; breaks a book rule | The words are his (managementDelegation). `vision-book`: "A book does not restate the living's words. A proposal may cite the record it distils by path and date." |
| "the machine skills carry it as their own lines" | S | Witnessed: `operation-main-flow` lines 9 and 11 ("A brief carries the task only…", "Delegate all task work."); `compensation-launch` line 6 ("one- or two-line brief"). This is a statement about how the system runs today, which `vision-book` keeps out of books. |
| "no psyche skill says it" | S, with one gap | No vision-, intent- or spirit line states the posture. Missing from the book: `vision-model-roles` «Delegation ceiling» says Fable and Astra are main-flow only, and `intent-startup-prompt` places the main-flow skill. |
| Records list (5 paths, dates) | S | All five exist with those dates. |
| "One record of 2026-09-14 reads «not use subagents» through speech-to-text; its own sentence says the opposite and is read so." | U as stated | The STT reading is d68c82's flag in the packet, and it is an inference: a relay through Codex 34d94e, not his transcript. The book turns it into a settled reading ("is read so") and asks him no ruling. It is also a correction he never made, delivered in the book as context. |

### Proposal 1, the line for vision-flow

| Statement | Class | Evidence |
|---|---|---|
| "A main flow does no task work itself" | S (M wording) | As in the figure. |
| "its model is the most expensive" | U / C | 6cc91b says "their models are **way more** expensive", which compares the main flow with its subflows. The book makes it a superlative. In the system, main flows run at every layer and model (Psyche Medium d8df70, Mind Sol 6288d1, Field Sol 33ba2b). `vision-model-roles` lets Opus and Sonnet tiers launch subflows too. |
| "its context the most valuable" | S, mild overreach | 6cc91b "way more valuable"; 08-09 "gold". |
| "so every search, edit, build and probe goes to a subflow" | C in part, M in part | "Build" and "probe" are from machine skills (`compensation-launch` "builds"; `operation-main-flow` "probes"), not from his records. "Every" contradicts the exceptions he set himself: a5940a 2026-09-03 (the main flow may read a file it knows exactly where to find and knows is 100% relevant); 7fba5f 2026-09-03 (the main flow still writes its flow log, records the psyche, writes beads); 0d557b 2026-09-09 ("you do want to read skill files yourself"). |
| "and the main flow keeps its hands clean" | S | managementDelegation 2026-08-09, his metaphor restated. |
| "The subflow is tailor-made: a pre-prompted definition holds everything it must know" | S except "everything" | "Almost everything" (9fb0ad). |
| "the brief it is launched with is one or two lines" | S, but conflicts with the target file | The same file, `vision-flow` «Starting flows», already says: "A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph". The book does not show or resolve this. |
| "A subflow whose way forward is unclear escalates back to its parent; the parent does not micromanage it." | S, one record | managementDelegation 2026-08-09. Ruling 2 honestly says it rests on one record. |
| Placement before «Subflows replace the harness subagent facility» | conflict not surfaced | That section says the harness subagent facility is replaced by independent flows with their own system prompts. The proposal's "pre-prompted definition" is today's harness subagent definition (`.claude/agents/`: book, read-*, write-*, tester). edf227 flowRole 2026-10-03 ("eventually all the sub-agents will themselves be flows") bears directly on this, and the omission check found it, but the book leaves it out. |
| Home: vision-flow | choice not shown | The packet named an intent- skill as a second home (d8df70 2026-09-24 "it has to be only in the system prompt"; d4ae97 2026-10-07 intent specializes metaflows) and said "Fable chooses". The book chose and gives no reason or ruling. |

### What the line leaves out (his records, not in the proposal)

- a5940a: locating a file is always subflow work, and a trivial subflow returns only the relevant content.
- 6cc91b (second record): a context subflow assembles the implementation brief, which enters the implementer's middle layer.
- e51411 2026-09-24: main flows write agent scripts rather than code; some skills are seen only by subagents.
- 7fba5f: the main flow's own writes (log, psyche, beads).
- edf227 flowRole: subagents will become flows.

## Invented structure, restating, overreach

- **Restating:** yes. The opening quotes "the manager's context is gold", and the proposal reuses "keeps its hands clean" and "micromanage".
- **Invented roles, names or layers:** none. "Main flow", "subflow", "tailor-made", "pre-prompted", "parent" and "brief" are his or already landed. The coined pieces are "task work", "build" and "probe" (from machine skills), plus the superlative "most expensive".
- **Overreach:** "most expensive", "every …", "everything it must know", "you have said this … in twenty-six flows", and the STT reading delivered as settled.

## Where the errors came in

Order of reading and writing, from the logs and files:

1. d68c82's audit subflow wrote the packet.
2. 33752b's omission check reported that the packet missed the August vision-raw records and edf227 flowRole, and never read the mind- and field-skills (33752b log, 2026-10-12).
3. 33752b's brief subflow wrote `reports/packet-2-brief.md`. It cut subject A to 8 records and placed the `operation-main-flow` and `compensation-launch` lines in A2, beside them.
4. 33752b authored book 8.
5. A Sonnet subflow rendered it with no change in content.

The packet introduced:

- the 26-flow / 36-record count, taken over a mixed set that includes its own impurities and covered records;
- the STT reading of 6cc91b, flagged as an inference;
- the miss on `vision-raw/managementDelegation.md`.

Its quotes and provenance were checked against the cited files and are faithful.

The authoring introduced:

- joining the count to the 2026-08-09 date;
- "most expensive" and "everything";
- "every search, edit, build and probe";
- dropping the a5940a, 7fba5f and 0d557b exceptions;
- not showing the conflict with `vision-flow` «a brief of a small paragraph» or with «Subflows replace the harness subagent facility»;
- choosing the home without a ruling;
- restating his words;
- delivering the STT reading as settled.

Possible causes, none of them witnessed:

- The author worked from the 8-record brief, not the 36 packet records, so the exceptions were never in front of it.
- The brief set machine-skill lines beside the records with no line marking them as not his words, so their vocabulary carried into the proposal.
- No rule in `compensation-book-distillation` or `vision-book` requires a proposal to show the target file's lines that it conflicts with, though `vision-book` does require showing the file around the change.
- The book shows no context lines of `vision-flow`, so the «small paragraph» line never came into view.

## Sources

- `/home/li/primary/flows/33752b/books/8-main-flow-delegates.md`; artifact https://claude.ai/artifact/E5RZEtBG1oa44tNBcXB6RA, version 1791822512-b614 (read)
- `/home/li/primary/flows/d68c82/reports/fable-packet-undistilled-2026-10-12.md`, subject A, lines 15–366
- `/home/li/primary/flows/33752b/reports/packet-2-brief.md`; `/home/li/primary/flows/33752b/log.md`, 2026-10-12 lines
- `/home/li/primary/vision-raw/managementDelegation.md`; `/home/li/primary/flows/edf227/vision/flowRole.md`; `/home/li/primary/flows/6cc91b/vision/mainFlow.md`
- `/git/github.com/LiGoldragon/psyche-skills/skills/vision-flow.md`, `vision-model-roles.md` (9bba4bf)
- `/git/github.com/LiGoldragon/mind-skills/skills/operation-main-flow.md`; `/git/github.com/LiGoldragon/field-skills/skills/compensation-launch.md`
- `/home/li/primary/.claude/agents/` (8 definitions)
- Provenance receipt: unavailable, because no PROVENANCE handoff exists for this thread.
