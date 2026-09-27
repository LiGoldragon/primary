# Psyche Fable recovery — launch source

This is the single launch source of the corrected Fable recovery profile. It
exists so the composed Claude first line names one path instead of five, and
so the full path and hash detail lives here rather than in that line.

The seat reads this file after it is running. Nothing here is pasted into the
first prompt.

## Seat

Psyche High, Claude harness, `claude-fable-5-1`, effort `medium`. A fresh seat
that remembers `b7ba00` at depth one, not a resumed session. It does not
resume `b7ba00`, reuse its Message binding, or assume its old pane survives.
It claims a fresh identity, then establishes a new Flow and Message binding
after native acceptance.

## What to read, in this order

The paths are absolute under the Primary source root. Each is named with the
SHA-256 the predecessor packet recorded for it; a mismatch is a finding, not a
thing to work around.

1. `/home/li/primary/flows/56ae53/fable-recovery/predecessor-handoff.md`
   `1ac7572402b48c8dda2cd0895940b550a58894ba3d3868cc5217924fa7f02f80`
   The compact handoff from `b7ba00`: what the predecessor was, what is
   historical only, and what the recovery is for.
2. `/home/li/primary/flows/b7ba00/receipts/readiness-announce.md`
   `a3253d14c56f7aa4997f60098b59aed41f2444577ba5aa6041242fbefcfc25b9`
3. `/home/li/primary/flows/b7ba00/vision/modelFlows.md`
   `5339c9c724df45da9323314c075d14ccef1fc55d7636cc1a569578c0cb3ca6c5`
4. `/home/li/primary/flows/56ae53/log.md`
   `8c85b86cd9c0e5083cc0ba169dff4b6e68c7d073e378983492d4e12f653af046`
   The hash is the one recorded when the packet was published; this log grows,
   so read the file and treat a changed hash as expected here alone.
5. `/home/li/primary/flows/56ae53/vision/model-flow-emergency.md`
   `e7041b49c9fde37c3b4a8d1729bb2ea403acbd528b7fb2aef39033b1421c2cce`

Beside them, and not part of the profile's source vector:

- `/home/li/primary/flows/38f337/handoff-fable.md` — the living's own words on
  Fable's role, cost, refresh, effort, Terra and the newer Flow. Verbatim;
  never paraphrased.
- `/home/li/primary/flows/38f337/successor-prompt-fable.md` — the drafted
  successor prompt and its gates.
- `/home/li/primary/flows/8904b1/summary.md` — Fable's own handoff, with its
  `log.md`, `reports/` and `witnesses/` beside it. Point to it; do not restate
  it.
- `/home/li/primary/flows/56ae53/fable-recovery/README.md` — the predecessor
  packet's own launch note, superseded on the first-line mechanics by
  `/home/li/primary/flows/38f337/fable-launch/README.md`.

## Skills

Five are stacked in the first line, in this order, and three of them are
forced: `main-flow`, `refresh` and `claude-harness` carry
`disable-model-invocation: true` in the `.claude` projection, so the Skill
tool cannot load them once the session is running. `psyche` and `spirit` fill
the two remaining slots by judgment, not necessity.

The other sixteen are named in the same line for the Skill tool and load after
start: `testing-flow-titles`, `psyche-interraction`, `psyche-acquisition`,
`psyche-distillation`, `behavior`, `correction`, `vocabulary`, `testing`,
`subflow`, `edit-coordination`, `flow-evidence`, `prompt-crafting`, `herdr`,
`messaging`, `file-editing`, `operational-final-response`.
