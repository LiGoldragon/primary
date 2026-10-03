# Retirement receipt of 9fb0ad

Method: observed 2026-10-03T17:18Z by Psyche.{ Fable edf227 }; the retire ran after retirement-of-9fb0ad.md was frozen (sha256 f65ec56a8284148ea7dbb796d66140d1b26a6129da3bf0cba9bec14bdf0caa03, the evidence given to the ledger).

- `FLOW_ID=edf227 hm-retire 9fb0ad --session default --pane-id w1:p1M --terminal-id term_65cef099a513f36 --name psyche_fable_9fb0ad --agent claude --native-thread 9fb0ad7f-bb95-4b5d-80de-c369fa25ebfe --evidence flows/edf227/witnesses/retirement-of-9fb0ad.md --evidence-sha256 f65ec56a...` printed `Retired 9fb0ad: delivery is blocked before Herdr routing`.
- After: `hm-list` still shows a 9fb0ad row (state `done`); pane w1:p1M agent_status `done`. The pane was not closed or killed; reaping is separate.
