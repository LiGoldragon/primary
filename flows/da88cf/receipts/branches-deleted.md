# Branch discard receipt — 2026-09-25

Lock: BranchDiscard 6952 (CriomOS-home, horizon-rs, goldragon) — released.
CriomOS and lojix were already covered by this flow's own MainIntegration
locks (6834, 6832) at time of use; no separate lock taken there.

## CriomOS
- `prometheus-usb-downlink-5f38bc` (de5ac1b7) — deleted, verified absent.
  This is the same bookmark as "de5ac1b's bookmark" in the brief — one item,
  not two.
- `flow-main-opencode-luna6` (c0b02d8a) — deleted, verified absent.
- `flow-final-aba74675-luna6` (203273f5) — deleted, verified absent.
- `flow07-ouranos-b7da5d` — NOT touched (held for pin review), per instruction.
- `prometheus-usb-bus-property-5f38bc` (da85c4a9) — NOT touched (tip being integrated), per instruction.
- "e0aef3d's bookmark" — SKIPPED. Commit e0aef3da0511 exists in the repo but
  carries no bookmark, and no descendant of it carries one either. Not
  ambiguous (multiple candidates) — simply absent. Reported, not deleted.

## horizon-rs
- `prometheus-usb-downlink-5f38bc` (fed0a12a) — revision matched; deleted, verified absent.
- `usb-gateway-6db4fe` (37416e10) — deleted, verified absent.

## goldragon
- `prometheus-usb-downlink-5f38bc` (1781f079) — revision matched; deleted, verified absent.
- "a911515's bookmark" — found by rev: `usb-gateway-data-753e69` (the daisy-chain
  report's "obsolete data format" branch). Deleted, verified absent.

## lojix
- `prometheus-usb-downlink-5f38bc` (387c13b5) — revision matched; deleted, verified absent.

## CriomOS-home
- Created `retained/opencode-home-5f38bc` at 926d9d6e54cda241197d0406f89c73e2dee74332
  (which was also the tip of `opencode-home-b7da5d-repaired-flow`), pushed,
  verified present on remote before any deletion.
- Deleted, verified absent: `flow07-home-b7da5d`, `opencode-home-b7da5d`,
  `opencode-home-b7da5d-repaired-flow`, `flow-final-2586ea19-luna6`,
  `flow-final-aba74675-luna6`, `flow-main-opencode-luna6`,
  `prompt-relay-a07f01a-luna6`. No other `opencode-home-*` or `*-luna6`
  bookmarks remained after this.

## Side effect noted
`jj git push --deleted` in CriomOS-home also flushed three unrelated,
already-locally-deleted bookmarks left over from this flow's own prior
main-integration work in the same checkout (before this lock was taken):
`HardenActiveNetworkWidget`, `StrengthenActiveNetworkChecks`,
`emacs-markdown-visual-wrap`. These were not on this brief's list; they were
pending local deletions from the sibling integration task in this same flow,
not something this task chose to delete. Flagging for awareness, not undoing.
