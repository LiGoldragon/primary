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

Checked per coordinator request: all three are ancestors of current Home
main, so nothing was lost and none needed recreating.
- `HardenActiveNetworkWidget` — last remote rev `4d6de296d14c9f1b26de83245a2294d5f7753258`
  ("home: reject inconsistent active network status") — ancestor of main.
- `StrengthenActiveNetworkChecks` — last remote rev `62d3d68a315374234d162200d218601cb05cb3c1`
  ("home: strengthen active network checks") — ancestor of main.
- `emacs-markdown-visual-wrap` — last remote rev `95011c161eb11c9dbd34799d1d1e98ab47f6e7d4`
  ("emacs: enable Markdown visual word wrapping") — ancestor of main.

## CriomOS (second pass, main 3e2cc8be)

### prometheus-usb-bus-property-5f38bc — deleted
Tip `da85c4a9` was duplicated onto main as `786ac218`. Compared
`jj diff --ignore-working-copy --color=never --git -r da85c4a9` against the
same for `786ac218`: both 144 lines, byte-identical (`diff` reported no
differences). Deleted the bookmark, pushed the deletion, verified absent via
`git ls-remote` on the remote (no match for
`prometheus-usb-bus-property-5f38bc`).

### flow07-ouranos-b7da5d — kept, NOT deleted
Pin comparison (branch tip vs main 3e2cc8be), by top-level flake input
resolved through each lock's root node:
- `message`, `herdr`: identical rev/narHash on both — no change.
- `criomos-home`: branch `e6f60a1` (lastModified 1790366314) vs main
  `4a9d85d` (1790394129) — main newer, branch older. OK.
- `criomos-lib`: branch `6e3bcb0` (1786574672) vs main `6db67c3`
  (1790393545) — main newer, branch older. OK.
- `flow`: branch `812053c` (1790364945) vs main `34aaf78` (1790390839) —
  main newer, branch older. OK.
- No top-level pin on the branch is newer than main's.

However, the source-file check fails: `jj diff --ignore-working-copy --git
--from 3e2cc8be --to flow07-ouranos-b7da5d --summary` shows differences
outside flake.nix/flake.lock:
- `modules/nixos/network/networkd.nix` (M) — branch still has the pre-fix
  `Driver = "cdc_ether cdc_ncm r8152 ax88179_178a asix"` match; main has the
  now-merged `Property = "ID_BUS=usb"` bus-role match (the fix just verified
  and released above).
- `modules/nixos/router/default.nix` (M) — same pre-fix Driver-match vs
  main's Property=ID_BUS=usb match.
- `checks/router-usb-downlink-binding/default.nix` (D relative to main) —
  present on main, absent on the branch.

Per the ruling's condition ("no unique source exists outside
flake.nix/flake.lock"), this branch fails that check even though every pin
is equal-or-older. Kept `flow07-ouranos-b7da5d`; not deleted, not pushed.

### flow07-ouranos-b7da5d — recheck against merge-base, then deleted
Coordinator correction: the full tip-vs-main diff above conflates the
branch's own changes with main having moved ahead since the branch forked;
a branch behind main naturally differs at its tip. Correct test is branch
tip vs merge-base with main, read-only:

    git merge-base main flow07-ouranos-b7da5d
    → 864e01be3bd1ca74dbb8eb3cb5ed41c0ee0f4555
    git diff 864e01be3bd1ca74dbb8eb3cb5ed41c0ee0f4555 flow07-ouranos-b7da5d --stat
    → flake.lock | 305 +++++++++++++++++++++++++++++++++++---------------
    → flake.nix  |   4 +-
    → 2 files changed, 201 insertions(+), 108 deletions(-)

Only flake.nix/flake.lock changed on the branch side since the merge-base —
no branch-side source changes (the networkd.nix/router/default.nix/checks
differences reported above are main's later, unrelated USB-bus-property
work, not anything the branch carries). Combined with the pin check already
done (message, herdr identical; criomos-home, criomos-lib, flow all
equal-or-older than main), the branch carries no unique work. Deleted
`flow07-ouranos-b7da5d`, pushed the deletion, verified absent via
`git ls-remote` on the remote (no match).
