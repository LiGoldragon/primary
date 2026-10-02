# Registration of 91ea9f and retirement of 6997eb (witness, 2026-10-02)

Method: `hm-list` (messenger-clj ledger joined with live Herdr agents), `flow 'List.{}'` (Flow nexus), `herdr pane list` / `herdr pane get`, `hm-retire` and `messenger-clj import-retirement`, `ps`.

## 91ea9f registered (witnessed before and after)
- Messenger registry: hm-list row `91ea9f  psyche_fable_91ea9f  default  working`, present before I acted (registered by the launcher) and unchanged after.
- Herdr: pane w1:p1A, terminal term_65cdf2f55d0822c, agent claude, native session 91ea9f9f-e4da-49dd-8102-9f235e68f41a, terminal title `Psyche.{ Fable 91ea9f }`; process launched with `--name Psyche.{ Fable 91ea9f }`. No title had to be set.
- Flow nexus (`flow 'List.{}'`): no row for 91ea9f, nor for any current Psyche seat (6997eb, fe945a, bd0019 also absent); the Flow nexus is not the registry these seats use. `flow-meta register-claude` was not run: that would add a second, non-matching registry entry outside the mechanism the seats use.

## 6997eb retired
- Before: Herdr pane w1:p19, terminal term_65ccb13f28aa02b, title `Psyche.{ Fable 6997eb }`, native 6997eb8a-30eb-49a1-a787-45279164a43b, status done. Messenger ledger held an old route named psyche_fable_6997eb on w1:p19 but hm-list showed no row (not live, not STALE); `hm-retire` refused: "No current registration".
- Evidence file (immutable): /home/li/primary/flows/91ea9f/evidence/retirement-6997eb.md, sha256 b9dd9064d642243afab3c5f109ab3c7583e583ee692642c6bd39cd2111cfe35a, committed 0c1f5dc6f.
- Ran `messenger-clj import-retirement 6997eb --session default --pane-id w1:p19 --terminal-id term_65ccb13f28aa02b --name psyche_fable_6997eb --agent claude --native-thread 6997eb8a-30eb-49a1-a787-45279164a43b --evidence <file> --evidence-sha256 <sha>` with FLOW_ID=91ea9f. Result: `Retired 6997eb: delivery is blocked before Herdr routing`.
- After: `herdr pane get w1:p19` returns pane_not_found; pane list has no 6997eb title; no claude process with session 6997eb8a. I did not close the pane myself: it was already gone when I went to close it, between the retire and the close (closer not identified, perhaps Herdr or another seat). Nothing else was killed.
