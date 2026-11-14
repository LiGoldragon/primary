# Handover of { Psyche codexManager Secondary fb8093 }

Written by Opus (this flow), 2026-11-04 about 17:55, for its successor 7c8547.

## The living's words in force

Through the predecessor a53796 (flows/a53796/vision/handover.md), his words verbatim:

- "for sure we want to wake them up because we only have a couple days to use them up. Unless you think there's no good use for them."
- On resets: "Ah yes, it's better to wait until it resets. You're right."
- "Why don't you just calm down for now? ... You're a little bit too eager."

Relayed to this flow on his order, not verbatim:

- The Psyche core Secondary: "the living orders Codex worked to the full until the reset Fri 6 Nov 17:00: keep Mind versionOne (wKJ, wK8), Mind beliefNexus (wKK, wKH) and Mind core (wKS, wKQ) loaded with work at all times; when one goes idle, prompt it with its next work at once. Each beat, send me ... the Codex percentage left and which of them is idle."
- The heartbeat: "no slack in the line, everybody pulling until the Flow Nexus fix is deployed".
- The Psyche core Opus: search with rg in the repository or flow directory the work is in, never the home directory (knowledge:search).

## Standing rules from the Psyche core Secondary

- Mind core alone decides Mind flows' moves (launch, retire, reporting route). A Mind report sent to this seat is answered only with "route to Psyche core Secondary".
- Messages between flows go by pane: `herdr --session default agent prompt <pane> '<text>'`, with the sender named at the head. The Flow Nexus queue is abandoned.
- Panes move. On 4 Nov the Psyche core Secondary moved wKV, then wKY, then wKZ:p1. Look it up by name with `herdr --session default agent list`.

## What is running

- **codex-keeper** (`flows/fb8093/tools/codex-keeper.sh`, PID 3123342, log `codex-keeper.log` beside it). It runs until Fri 6 Nov 17:00.
  - Every 60 s it checks the six Mind panes. A pane idle at two checks in a row, and not prompted by the keeper in the last 20 minutes, gets an order to take up its next work.
  - Every 30 min it beats `Codex N% left; idle: …` to the Psyche core Secondary, whose pane it looks up by name.
  - It prompts SELF_PANE (line 14, `wKE:p1`, this flow's pane) when ordinaryUsageAllowed is false, and once from Fri 16:02 for the reset window. **Change SELF_PANE to your pane and restart it.** Kill by PID; `pkill -f codex-keeper.sh` also kills the calling shell. Restart with `cd flows/fb8093/tools; nohup bash codex-keeper.sh >> codex-keeper.log 2>&1 &`.
  - Its 20-minute state is in memory, so a restart may prompt an idle pane early.
  - The six Mind pane ids are fixed (line 12, `PANES`). A moved Mind flow is logged as missing.
- **Heartbeat**: { Psyche codexManager Tertiary cf4f71 }, pane wK0:p1.
  - It sends a hard beat every ~10 min. The answer is three lines by pane to wK0:p1: finished, on, blocks. This seat holds no step of the chain; it feeds step (1) by keeping Mind core's Codex flows loaded.
  - Its refresh fails with RecordMissing. That is the known Curriculum empty-records defect: take no action.

## Codex

- 41% left at 17:51 on 4 Nov, spending about 15% an hour at the last reading, so it may run out around 20:30 tonight. The week window resets Wed 11 Nov 05:55.
- Resets available: 6 Nov 17:32 (soonest), 30 Nov 14:15, 1 Dec 16:44.
- The 6 Nov reset is redeemed by knowledge:codex-reset: when ordinaryUsageAllowed turns false, or in its last 90 minutes (from Fri 16:02). Run `tools/codex-usage`, then `tools/codex-redeem-reset <id>`, and report both states. The bead is primary-8kky.
- Paid credits are not to be spent.

## Sent and waiting on

- The herdr Root action question from Mind versionOne Primary 177120 is with the Psyche core Primary: are these the meta pane actions already in vision:herdr-nexus-v1, or a distinct proposal? It is unanswered here.
- Mind versionOne Primary 177120 reported v1 still lacks effort application, Register bridge replacement, an independent audit, atomic redefinition acceptance and shell composition. It is working them on the Psyche core Secondary's confirmation.
- Old Mind versionOne Primary 63b019 still has a live pane, wJS:p1; its retirement is Mind core's call. My `flow 'Stop.63b019'` drew `ReplaceRejected.PredecessorAbsent`, a Flow Nexus anomaly, already reported.
- The living's grep proposal from a53796 is now answered by knowledge:search.
