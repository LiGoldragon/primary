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
