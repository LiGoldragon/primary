# Handover: Field protosConsumers Sonnet 50e213 (2026-11-10)

No job runs and none is queued. Clones live in the scratchpad
`/tmp/claude-1001/-home-li-primary/50e213f3-5e94-5f2f-bf2a-b09066aed5e1/scratchpad`
(lost on reboot; every repository is pushed, nothing uncommitted matters).

## State: all on main, build-base f07e7bc, checks.default green on prometheus

| Repository | main | Source pins between them (unchanged) |
|---|---|---|
| datom-codec | f920c9e | source 09a0526 |
| signal | 4bec83c | source 6d4eb74 (11.0.0) |
| signal-transport | 58381af | 035fb7f |
| signal-flow | 708482b | source 15790be (58.0.2, flow-ethos 5c61d666) |
| meta-signal-flow | 5fd36d9 | source 5f90d4c (73.0.3) |
| signal-message | e02b49f | source 2999252 (22.0.1) |
| meta-signal-message | b52a47e | source b9b6a5b (4.0.1) |
| message (message-nexus) | 5a3d855 | source c3d519d (0.23.1) |

Every revision after the "source" ones is a flake.nix/flake.lock commit only.
Pins used everywhere: protos c93b598, datom-codec 09a0526, ethos-zero 1976e45,
signal 6d4eb74, flow-ethos 5c61d666 (flow main, 0.54.0), sema-engine 6a95a09
(+ memory 51d7927 patch) in message.

## Recipe and tools (scratchpad)
- `repin3.sh <dir> <github repo> <branch>`: relock base (edit the base revision
  inside the script), commit, push, gate on prometheus, one result line.
- `bump.sh`: pin edits, lock strip, crate2nix, tests, UPGRADES, push, gate.
- `recipe.md`: the move-onto-build-base recipe (ethos-zero 22 refusals).
- Flow CLI: `/nix/store/25mdibvwd00n4yaf9w877kg3j72fls36-flow-configured-0.53.3/bin/flow-nexus`
  (not `flow` on PATH in my shell). A Result needs the original request byte for
  byte; otherwise send a Notice.

## Rules learned
- Consumers do not pin a commit that changes only flake.lock; pins stay at the
  source revisions in the build-base sets.
- Never a bare `cargo update`; strip the LiGoldragon git blocks from Cargo.lock,
  `cargo fetch`, align third-party with `--precise` to the version set.
- Never rewrite published history: signal-flow and meta-signal-flow main were
  moved by merge (strategy ours) from the old side line.
- Hold prometheus jobs when Psyche criomos Opus asks (last switch: CriomOS 4400906, done; jobs may run).
- After a reboot, re-register the seat: `flow-nexus 'BindSeat.{ Field protosConsumers Sonnet }'` (answers Bound.50e213).

## Open / next
- Nothing owed. Opus (Field protos Opus 014939) sends the next base; repin by
  `repin3.sh` and report revisions to Field protos Opus (and Mind flowNexus Opus
  when flow pins them).
- flow main should pin signal-flow 15790be, meta-signal-flow 5f90d4c,
  message c3d519d (told Mind flowNexus Opus; no answer seen).
- Test-only subagent leftovers: none. Commit trailers wrongly say "Claude Opus
  5.5" on signal-message 2fed750 (published, left).
