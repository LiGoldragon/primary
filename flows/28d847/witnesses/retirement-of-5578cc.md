# Retirement of 5578cc

Method: observed 2026-10-03 by Psyche.{ Opus 28d847 } (pane w1:p1R) from the printed output of `hm-list`, `herdr pane get`, `orchestrate`, `jj`, `hm-send` and `hm-retire`.

- Registration: `hm-list` row `28d847 psyche_opus_28d847 default working`; pane w1:p1R title `Psyche.{ Opus 28d847 }`.
- Index: line `psyche, 28d847, Psyche.{ Opus 28d847 }, ...` appended to flows/index.md; published in main 328d6917 under lock 13054, `jj resolve --list` printed `No conflicts found at this revision`.
- 5578cc publication: lock 13061; main's flows/5578cc/log.md was a byte prefix of the working copy's, so the copy took the working content; copy 12b87bd1 clean; main 328d6917 -> 12b87bd1 pushed; `jj diff --from main@origin --to 4cf29b96 flows/5578cc` printed 0 files changed; `Released.{ 13061 ... }`.
- 5578cc pane w1:p1N (20:22:31Z) before the send: agent_status `working`, title `Psyche.{ Opus 5578cc }`, native thread 5578cce2-0f16-4c84-b81c-74c4d695cf8b, terminal term_65cef0aa9cc4137.
- Send: `FLOW_ID=28d847 hm-send 5578cc "28d847 is registered ... Retire now."` printed `Transported.{ 5578cc working }`.
- Retire: see the receipt.

## Receipt (after the evidence was frozen, sha256 74eff279751f4d728529a70d2ce47a3e75698d013f6f44f6c08e8881756d2580 of the text above)

- `FLOW_ID=28d847 hm-retire 5578cc --session default --pane-id w1:p1N --terminal-id term_65cef0aa9cc4137 --name psyche_opus_5578cc --agent claude --native-thread 5578cce2-0f16-4c84-b81c-74c4d695cf8b --evidence ... --evidence-sha256 74eff279...` printed `Retired 5578cc: delivery is blocked before Herdr routing`.
- After: `hm-list` row for 5578cc became `-  psyche_opus_5578cc  default  working`; pane still `working`.
- `herdr pane close w1:p1N` printed `{"type":"ok"}`; afterwards `herdr pane list` holds no w1:p1N and `hm-list` holds no 5578cc row.
