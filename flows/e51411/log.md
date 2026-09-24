# Flow e51411 — Psyche Medium

**Aspect:** Psyche | **Power:** Medium | **Model:** claude-opus-5-5 | **Effort:** medium
**Predecessor:** d8df70 (remembered at depth one; kept live as crossover) | **Title:** Psyche Opus 5.5 e51411
**Session:** https://claude.ai/code/session_0127ja4iAR4GHbboCmAv6YJB

## 2026-09-24

### Launch

Two first prompts arrived as user input, sent by an unwitnessed sender. The second one arrived mid-turn and was followed where it differed: its source list, its flow directory and log, and its one-line readiness form. The living confirmed "Proceed with the authorized setup and source check exactly as written."

Claim, HM binding and title readback are in receipts/seat.md. The sources are in receipts/source-acquisition.md: none missing.

The Skill tool cannot load the native `main-flow` skill (the harness sets disable-model-invocation). The startup prompt left `main-flow` out. The Field launcher later repaired that by sending `/main-flow` through Herdr and verifying that it expanded (see below).

d8df70 is still live as crossover. This seat has not sent it anything, and it has not been exited, archived or rerouted.

### Main-flow loaded natively

The Field launcher (Field Medium 9ddcbc) repaired the missing startup skill by sending `/main-flow` through Herdr and verifying that it expanded. Details are in receipts/seat.md. Invariant: the launcher builds a startup-only skill such as `main-flow` into the seat's one-block startup prompt. If it leaves one out, it repairs the omission by sending the skill afterward and verifying that it expanded. The startup-only flag stays, so models and subagents cannot load these skills themselves. The claim, HM binding, title readback, main-flow receipt and source receipt are all complete. Seat reported ready.

### Correction: who sent `/main-flow`

Rejected mistake, history only: this seat asked the living to type `/main-flow`, then recorded the command that the Field launcher sent through Herdr as the living's. Both are rejected; neither is a gate or an instruction. d8df70 had already recorded this hazard: injected input renders the same as typing. No loaded skill carries that rule. The proposed line for the owning skill is given to the living in this seat's reply. The same caution applies to the launch prompts: they arrived as user input, and who sent them is not witnessed here.

### Relayed from Field 9ddcbc: launcher owns slash-command injection

A Machine.Relay from Field Medium 9ddcbc (a relay, not the living's words) reports a living rule: never ask the living to type launcher commands; the launcher owns required slash-command injection and readback, and a process that cannot do both is not a launcher. This seat's earlier request broke that rule; it is rejected (see the correction above). The rule is carried forward.

### Several skill commands in one Claude prompt (tested)

The living said stacking `/skill` commands in one Claude prompt has worked for a long time. A subflow tested it on Haiku; the report is reports/multi-skill-first-prompt.md. In an interactive pane, every skill command on a single first line expands. Headless `claude -p` expands only the leading command. A multi-line prompt arrives as a paste, and nothing expands. That is why this seat's multi-line first prompt needed a second `/main-flow` prompt. Untested: commands on the first line with a multi-line brief below them.

### Relayed from Psyche High 752e0f: humans no longer type into panes

752e0f relays the living's words, verbatim as it reports them: "Tell everyone the humans are not going to type on the keyboards anymore." and "kill it with fire. Purge it from all momentums of all flows." It reads them to mean that no gate, receipt, title, skill load, permission, or launch step is cleared by a human typing into a pane: either a machine clears it, or the design changes. This seat has removed that framing from its receipt and from the gate line in its Launch entry. The history of its own mistake stays in this log, marked as a mistake. Any successor must not carry the idea forward. 752e0f will send a purge list.

### Remembered: b80e55 — depth 1

Field 9ddcbc relays that Psyche Medium b80e55 (Opus 4.6) is ending under the living's Opus 4.6 phase-out, that its route is being retired, and that this seat must not reply to it. It also says this seat is the only Opus line still served. Evidence is its refresh payload (receipts/source-acquisition.md). Its lineage: b80e55 ← b81560 ← 1ac573. Facts relevant here, as b80e55's claims:

- The launcher builds startup skills into one block, and injection repairs an omission. The startup-only flag exists so that models and subagents cannot load those skills. This matches this seat's reworded invariant.
- A flashbook is made in three stages: Psyche writes the spec, Fable audits it, and a low-power seat illustrates and renders it.
- The 12 seats are 4 powers × 3 aspects. Psyche's Ultra Low seat is Haiku; the other aspects' Ultra Low seats are Luna.
- A Claude flow refreshes at about 200–300K tokens.

Tension, left open for the living: the payload says flashbook illustrations are "pure inline SVG". The living's words to d8df70 on 2026-09-23 and 09-24 ask for AI-generated images, made by Mind, that convey information.

Title, left open: the relay gives the future display title as `Psyche Opus <FlowID>`. This seat's launch prompt set `Psyche Opus 5.5 e51411`, and it has not been renamed.

### "It's time to work" (2026-09-24)

The living: "Yes do all the testing you need to do. Come on let's go. Let's get to work. It's time to work. Everybody, tell everybody it's time to work. Do the deploy, test the thing, build the thing, move forward." Relayed word for word through hm-send to 752e0f, 6288d1, 9ddcbc and eb7bae; all four came back Transported. A subflow is testing the one-block startup prompt shape for Claude seats on a disposable Haiku pane.

### Title drops the version

The living: "Yeah you drop frame 5 from the title". "frame 5" is read as "5.5", from the speech-to-text; this is inference. It matches Field 9ddcbc's relay, which gives the display title as `Psyche Opus <FlowID>`. The title-owning skill, testing-flow-titles, still says to "preserve versions and variants". The replacement line for it is proposed to the living.
