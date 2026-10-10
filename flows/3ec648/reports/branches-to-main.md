# The e167d8 branches landed on main

Subflow of 3ec648, 2026-10-02. What runs today (Flow on signal-flow 7.0.0 and
meta-signal-flow 11.0.0; message-nexus 0.17.0 on signal-message 8.0.0 and
meta-signal-message 0.8.0) is now on main in all five repositories. Every
branch is kept, locally and on origin.

## The author flow

e167d8 (Psyche Opus, 2026-09-26) still has its line in `flows/index.md`.
`hm-list` did not list it: the messenger knew eight flows and only 3ec648 was
working. Since it was not alive, nothing was sent through hm-send.

## Per repository

| repo | branch HEAD before | main before | main after | how |
|---|---|---|---|---|
| signal-flow | s1-e167d8 `1c9e4b306e26` (7.0.0) | `eba28170aeea` (6.3.0) | `58603838309a` (7.1.0) | merge |
| meta-signal-flow | s1-e167d8 `2ac045c2cb77` (11.0.0) | `a897462cc719` (8.0.2, no flake) | `2ac045c2cb77` (11.0.0, flake present) | fast-forward |
| signal-message | s2-e167d8 `d57420055970` (8.0.0) | `7f2fc2d44b7b` | `d57420055970` (8.0.0) | fast-forward |
| meta-signal-message | s2-e167d8 `14f57596fc23` (0.8.0) | `87a54b0a1cbc` | `14f57596fc23` (0.8.0) | fast-forward |
| message | s2-e167d8 `481b579fcf72` (0.17.0) | `930c5169ffcf` | `481b579fcf72` (0.17.0) | fast-forward |

The four fast-forwards had no commits on main that their branches lacked, so
nothing conflicted. Their versions stay as the branch has them.

## signal-flow: the only conflict

After the branch forked at `e9e243c75cce` (6.2.0), main gained one commit,
`eba28170` (2026-10-01, signal-flow 6.3.0). It declared the Presentation and
QueueTurnEnd vocabulary (QueueTurnEnd request; TurnEndQueued and
TurnEndRejected replies; the types Title, Presentation, TranscriptPath,
TurnEndRequest and TurnEndRejection) and replaced the flake with a rust-build
flake. In the branch's 7.0.0, Send is removed and Observe.Agent and
AgentObserved are added. All six changed files conflicted.

How each was resolved:
- `ethos/signal.ethos`: a token-level three-way merge, base 6.2.0. The only
  real clash was the end of the reply list, where both sides appended. The
  branch's AgentObserved comes first, then main's TurnEndQueued and
  TurnEndRejected. QueueTurnEnd goes after the 7.0.0 requests. Every 7.0.0
  wire index is unchanged and 6.3.0's vocabulary is added after it. 6.3.0's
  comment block is kept.
- `src/generated/signal.rs`: regenerated from the merged ethos with
  ethos-zero at the pinned `407f938`. As a check, the same generator was first
  run on the branch's ethos, and its output was byte-identical to the
  branch's committed file. The build.rs freshness assertion passes.
- `Cargo.toml` / `Cargo.lock`: taken from the branch, version set to 7.1.0.
  This bump is required: the merge adds public wire vocabulary to 7.0.0, so
  calling it 7.0.0 would make it a different 7.0.0 from the one deployed. The
  deployed 7.0.0 (`1c9e4b30`) is the merge's first parent and stays reachable
  from main, and consumers pin that rev.
- `flake.nix` / `flake.lock`: main's rust-build flake (checks test,
  test-datom, fmt) replaces the branch's fenix flake (one cargoTest).
- `tests/contract.rs`: rustfmt only (one array of tuples re-wrapped), because
  main's fmt check would otherwise fail.

## Tests

`cargo test --all-features`, CARGO_TARGET_DIR in the scratchpad, under a
12G memory cap with a timeout, run on the exact revision that became main:

| repo | cargo test | nix flake check (20 min, Prometheus) |
|---|---|---|
| signal-flow | pass (14 contract + 3 presentation_turn_end) | timed out (124) still building dependencies; inconclusive |
| meta-signal-flow | pass (9) | timed out (124) at the deps derivation; inconclusive |
| signal-message | pass (5) | pass (exit 0) |
| meta-signal-message | pass (3) | timed out (124); inconclusive |
| message | pass (2 + 1 + 13) | pass (exit 0) |

## Notes

- The brief named a `main-feature-integration` skill. No such skill exists in
  the deployed tree or in the Curriculum sources, so this work followed
  file-editing (jj, `bookmark set main`, push) and feature-development
  (Orchestrate lock 11484 on the five checkouts, now released).
- signal-flow 7.1.0 is on main only. Nothing deployed pins it. The next Flow
  repin may take it, or keep pinning `1c9e4b30`.

## Sources

- jj logs and bookmarks in /git/github.com/LiGoldragon/{signal-flow,
  meta-signal-flow, signal-message, meta-signal-message, message}, fetched
  2026-10-02.
- `hm-list` output and `flows/index.md` lines 224-225, 2026-10-02.
- Nix logs: scratchpad `nix-<repo>.log` for this session (not kept).
