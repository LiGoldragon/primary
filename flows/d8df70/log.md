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
