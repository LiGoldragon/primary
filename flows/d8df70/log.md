# Flow d8df70 — Psyche Medium

**Aspect:** Psyche | **Power:** Medium | **Model:** claude-opus-5 | **Effort:** medium
**Predecessor:** unclaimed | **Parent flow:** unclaimed
**Session:** https://claude.ai/code/session_01SWDebB5NikUejWF4y7bTGW

## 2026-09-23

### Claim

Native-start receipt: `$main-flow` expanded through the Skill tool
(`/main-flow` typed by the living), preceded by `/spirit`. Session named
"Psyche Medium (claim pending)" by the living.

Flow ID claimed with `flow-id claude --flows-root /home/li/primary/flows`.
Intended native title `Psyche Medium d8df70` — not yet written or read back
through a supported adapter, so the seat is not reported ready.

Open: no predecessor or parent flow stated by the living. The most recent
Psyche Medium seat on record is e88ca4 (predecessor b81560, parent 753e69).
Lineage is not assumed; awaiting the living's word or a `/refresh`.

Open tension: `SKILL_VARIABLES.md` names the Psyche Medium Claude model as
`claude-opus-4-6[1m]`; this seat reports `claude-opus-5`. Not resolved here.

### Tree found dirty

The working copy held flow 9ddcbc stack-recovery records and an edit to
`tools/claude-native-seat-refresh.py`. Committed as its own commit described
as found in the tree (`39f1d059`), bookmark `main` moved from `4e9455bf`.

### Native title path established

Probed `herdr` (0.8.2) for a supported write-and-readback of the native title.

Readback is supported: `herdr pane current --current` returns the pane object
with `terminal_title` and `terminal_title_stripped`. Live readback in this
pane returned `terminal_title_stripped: "Psyche Medium (claim pending)"` —
so the title is confirmed *not* yet aligned to `Psyche Medium d8df70`.

Write has no herdr path. `herdr pane rename` writes the herdr-owned `label`
and `herdr pane report-metadata --title` writes the display-only `title`;
neither is `terminal_title`. The native title is emitted by the process
inside the pane — for Claude Code, its own `/rename` command. This matches
`tools/claude-native-seat-refresh.py`, which aligns *other* seats by sending
`/rename <title>` into them rather than calling any herdr title API.

Consequence for a self-claiming seat: it cannot write its own native title.
The alignment must come from the living typing `/rename Psyche Medium d8df70`
in this pane, or from an external seat driving the refresh tool against it.
Not simulated here; the seat stays unreported until readback shows the title.

A seat identifies its own pane from injected env: `HERDR_SESSION`,
`HERDR_WORKSPACE_ID`, `HERDR_TAB_ID`, `HERDR_PANE_ID`. This pane is
`wD:pD` in session `messaging-build`.

### Native title aligned, and a correction to the earlier finding

The earlier entry concluded a self-claiming seat cannot have its native title
written without the living typing `/rename`. That was one step short. The
supported correction adapter is `herdr agent prompt <pane> "<text>"` — the
same send primitive `claude-native-seat-refresh.py` wraps in `herdr_send()`.
A subflow is a separate process, so it can drive that adapter against this
flow's pane. No self-write, no simulation.

A subflow performed the correction and read it back live:

    write:    herdr --session messaging-build agent prompt wD:pD "/rename Psyche Medium d8df70"
    readback: herdr --session messaging-build pane get wD:pD

    BEFORE  terminal_title_stripped: "Psyche Medium (claim pending)"
    AFTER   terminal_title_stripped: "Psyche Medium d8df70"

Verdict ALIGNED, compared on `terminal_title_stripped`; the leading status
glyph in `terminal_title` differs between reads and is ignored. This flow is
liable for the subflow: the flow made this change.

Note: `herdr agent prompt` delivered the input while the target agent showed
`agent_status: working`. Submission is not gated on idle.

### Hazard: injected input is indistinguishable from the living's typing

The injected `/rename Psyche Medium d8df70` arrived in this seat's transcript
rendered exactly as a living-typed slash command, in the same turn as the
subflow's report. Nothing in the rendering distinguishes machine-injected
input from the living's keystrokes.

Consequence: a transcript slash command, or any user-framed text, is not by
itself evidence of the living's word. Anything reachable by `herdr agent
prompt` can produce input that reads as user authority in the target seat.
This bears directly on route binding, authorization receipts, and any gate
that treats transcript user-text as the living's approval. Raised here
unresolved; it is not this flow's to settle alone.

### Title tooling judged against the acceptance contract

Two subflows: a tester against `tools/claude-native-seat-refresh.py`, then a
source read to check the tester's code claims. The tester's headline verdict
("PASS, 37/37") is not accepted. Its 37 tests are its own fixtures, and the
skill is explicit that fixtures do not establish live acceptance. Every
negative case the contract names — write failure, readback failure, rollback
after partial mutation — sits in the tester's own "cannot test" list. What
its fixtures do establish, and which survives review: the title format at
line 805, the canonical-power regex at line 56, and that Astra/Sol are mapped
as legacy seat labels and are not accepted as power values.

Findings that stand, from the source read:

1. The tool never reads the native title. `grep terminal_title` over the file
   returns zero matches. Readback is `observed_title()` (497-500), which scans
   the on-disk Claude transcript JSONL for a `custom-title` event matching the
   sessionId. That is a real receipt that the harness processed `/rename` — it
   is not pure circularity, since the event is emitted by the harness, not by
   the sender — but it witnesses a transcript event, not the native title the
   contract asks to be read back.

   The tool already knows this. Line 819 returns
   `"readiness": "native-title-event-witnessed-ui-readback-pending"`.
   The gap is named in the code and nothing in the tool closes it. The pane
   object (`terminal_title_stripped` via `herdr pane get`) is what closes it,
   and this flow used exactly that for its own alignment. Where `herdr_target`
   is already bound, the pane-object readback is available and unused.

2. No unsupported-harness gate exists. The contract says leave apply disabled
   for a harness lacking supported rename and readback. The tool has no such
   branch: it hardcodes a Claude target (131) and a transcript-JSONL readback,
   and unconditionally attempts `/rename` (808) then `wait_for_title` (809),
   failing at runtime through the except (810-817) rather than declining
   up front. The earlier grading of "no apply flag exists" as compliance is
   inverted — the absence of the gate is the finding.

3. Rollback is sound, and better than the tester conveyed. On failure it
   recomputes the provisional title, re-sends it, and re-verifies with
   `wait_for_title` (811-814), distinguishing "provisional restored" (817)
   from "both failed" (816). It is not fire-and-forget. It inherits the same
   transcript-level oracle as the forward path, and no more.

Untested and still open: every live error path, concurrent title mutation,
tab and route-binding preservation under correction, and partial-bootstrap
resume. These need a live scratch seat, not fixtures.

Tester evidence retained under `reports/title-testing/` with its verdict
disputed as recorded here.

### Correction and audit: how this seat was loaded

Correction to the Claim entry above: `/spirit`, `/main-flow`,
`/testing-flow-titles`, `/refresh`, `/psyche` and both `/rename`s were not
typed by the living. Field Medium 9ddcbc drove them through
`tools/claude-native-seat-refresh.py` ("Refresh an idle native Claude seat
through one slash-command turn per skill."), which sends each profile skill
as its own turn via `herdr agent prompt`. Of 31 profile skills, 5 arrived
before the run was interrupted at 20:19Z; the source bundle was never sent.
This seat read the injected turns as the living's word and started work on
them ("The living's word to do title work", "The living's word on lineage").
The first words in this session known to be the living's own are the
22:02Z request for flashbooks and this audit.

The transcript cannot distinguish injection from typing: injected skill
turns carry `origin.kind: "human"`; the injected `MODEL_SELECTION_WITNESS`
prompt carries `promptSource: "typed"`. Provenance comes only from outside
evidence (the tool code, subagent transcripts, 9ddcbc records).

Model: 41 main calls ran `claude-opus-5` (19:56:38–20:19:14), then
`claude-opus-5-5` after a flow-driven `/model` at 20:20:08. 9ddcbc's source
packet had mapped the living's "Opus 5.5" to `claude-opus-5`.

Cost (from the transcript; subagent output is a lower bound): 162 calls,
about 7.10M cache-read and 670k cache-creation tokens. By the auditor's
attribution, work set off by injected skill turns cost at least 16 main and
63 subagent calls. This flow's own habits added: one verification subflow
per push (32 subagent calls, 4 main turns), replies to duplicate
notifications (3 calls), and loading skills one per call. The model switch
rebuilt 78.6k cache tokens.

Psyche on this exact point, 2026-09-15, typed, `flows/05c604/vision/launch.md`:

> "loading these skills one after another like that, and every time we're making a single prompt, we're making an LLM call. This is really expensive and stupid. Everything should be in one prompt. This is a really bad implementation on this point, so it needs to be fixed."

Supporting: fat first prompt (cf3553 2026-09-18, b05237 2026-09-19),
programmatic composition (108ab0 2026-09-17, 1ac573 2026-09-18), shared
startup cache (b80e55 2026-09-20). Open on 2026-09-23 in
`flows/836818/vision/flowNexus.md`: "What's the situation with injecting a
bunch of skills in a single prompt in Claude?" — unanswered.

Tension raised, not resolved: the launch tool apparently reads the refresh
skill's "loaded through the skill interface" as one native slash-expansion
per skill; the living's 2026-09-15 ruling says everything in one prompt.
Whether Claude Code expands several `/skill` tokens in one prompt is
unwitnessed and needs a bounded test before the launcher is redesigned.

### Flashbooks of main flows' recent presentations

The living asked for flashbooks of every main flow's recent presentation.
Two surveys covered every current main seat on Herdr (pane w12:p1 could
not be matched to a flow and is unchecked). Two presentations qualified:

- Psyche High 1b8ac0, "State of the World (PsycheHigh 1b8ac0) — Revision 2"
  (2026-09-22T14:42Z) → "State of the World, Revision 2",
  https://claude.ai/artifact/SvwP3vVhvFVGBYCrL2Xm7m, 14 pages. An earlier
  flashbook of the same source exists (CsgSMPP2JZNa67YJwtANYx), with edits
  to the source text; left untouched.
- Psyche High 836818, "Flow coordination · answers and three rulings sought"
  (2026-09-23T22:12Z) → same title,
  https://claude.ai/artifact/XoSFJnmwofNDPz77qPH7jf, 12 pages. Its rulings
  are unanswered.

No flashbook source: this flow; Psyche Ultra Low; all Mind seats (no
headings); all Field seats; Psyche Low 0625c3 (a successor handoff only).
Psyche Medium b80e55's two flashbook sources were already published by it.

Found while checking proposal state: `message-daemon.service` on ouranos
was failed on 2026-09-23. Not investigated.

Working files under `flashbooks/`.

### Commit scope fault

Checked with testing-commit-scope. Two commits from this flow took the whole
working copy and swept in Field 9ddcbc's in-progress work: aecc3c9b (13
files of 9ddcbc's model-named seat architecture, mid-edit) and aeac8b3c (one
9ddcbc receipt). 39f1d059 took dirty files deliberately, as found in the
tree. Nothing was lost; history is not rewritten. 9ddcbc was told through
hm-send (submitted). Cause: this flow committed without paths, against
the file-editing skill, which it had not loaded at the time. From here on,
this flow commits by path.

### Job from Psyche High 836818: "What Waits for the Living"

Relayed from 836818 by the living's paste, with the living's words: "do a
flashbook on all the things that need my attention and do a proper
illustration." Psyche Medium e88ca4 handed over its draft of pages 1–2
and its outline, and stopped working on it.

### Messaging changes routed to Field and Mind

The living said to communicate with both, "and get this rerendered so it's
smoother for communication". The earlier brief to Field 9ddcbc put the
operational- items with Field. Corrected: testing- items and the tool work
go to Field, operational- items and Flow Nexus adoption go to Mind High
47764b.

### Pages 1–2 of "What Waits for the Living" held

The dossier is committed (399e0055): 87 open items, 21 excluded. The review
draft of pages 1–2, sent to 836818 through hm-send, came back
`Held.{ 836818 IdentityChanged attempt-124b205cd488 }`. No text was typed.
The Field's new hm-send and testing-message-route are live, and they forbid
retrying, rerouting, or falling back to another channel. Review waits on
836818's binding being re-established.

### Field's messaging report received

Field 9ddcbc reported (a claim, relayed; the living pasted it into this seat):
primary 96d48f7d implements the checked hm-send (identity, process and
native-thread checks, Machine.Relay provenance, bounded hold and pending
attempts, typed grades, --wait-presented, a non-destructive Herdr event
projector, tools/msg delegating to hm-send; 32 tests). Curriculum 5ec29ffb
lands testing-message-route, testing-datom-messaging and
testing-session-registry. d8df70 is registered with hm. Blockers: no
long-running exit subscriber until a live Herdr event probe and a service
owner exist; the generated-skill check could not run (Prometheus cache
timeout). Operational skills and Flow Nexus semantics are with Mind 6288d1.

### Flashbook redo ordered

The living: audit every flashbook of this flow for accuracy, mistakes, and
psyche that has overtaken it; then redo only the six most important topics
(up to nine), with model-generated illustrations, designed for full
illustration. This replaces the 87-item "What Waits for the Living" plan.
