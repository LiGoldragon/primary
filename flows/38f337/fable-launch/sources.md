# Psyche Fable recovery — launch source

This is the single launch source of the corrected Fable recovery profile. It
exists so the composed Claude first line names one path instead of five, and
so the full path and hash detail lives here rather than in that line.

The seat reads this file after it is running. Nothing here is pasted into the
first prompt.

## Seat

Psyche High, Claude harness, `claude-fable-5-1`, effort `medium`. A fresh seat,
not a resumed session.

Its ancestry is two deep and the order matters. `8904b1` is the live Fable and
the immediate predecessor: it is remembered at depth one. `b7ba00` is the
prior, dead Fable generation that was never resumed; it is the genuine earlier
ancestor and is remembered at depth two, not at depth one. An earlier draft of
this packet had `b7ba00` at depth one and named no `8904b1` at all, which
placed a dead generation where the live one belongs.

The seat does not resume either flow, reuse a Message binding, or assume an old
pane survives. It claims a fresh identity, then establishes a new Flow and
Message binding after native acceptance.

## What to read, in this order

The paths are absolute under the Primary source root, `/home/li/primary`. Each
is named with its SHA-256 as recorded when this packet was corrected; a
mismatch is a finding, not a thing to work around.

1. `/home/li/primary/flows/8904b1/summary.md`
   `bd7f6a2ffde2f420490939c435cf040357c8c3f1921627f81334187fc89a4847`
   The live predecessor's own handoff, with its `log.md`, `reports/` and
   `witnesses/` beside it. Point to it; do not restate it.
2. `/home/li/primary/flows/38f337/handoff-fable.md`
   `05d8694b2a87e9046f33968c78b4b6c04e860754376c62837d58a85a6993eca8`
   The living's own words on Fable's role, cost, refresh, effort, Terra and the
   newer Flow. Verbatim; never paraphrased.
3. `/home/li/primary/flows/38f337/successor-prompt-fable.md`
   `9cf8f20249f78e87476c3704ab26a994b3edfcc637bbe956eaef0e89db0e3adc`
   The drafted successor prompt and its gates.
4. `/home/li/primary/flows/56ae53/fable-recovery/predecessor-handoff.md`
   `1ac7572402b48c8dda2cd0895940b550a58894ba3d3868cc5217924fa7f02f80`
   The compact handoff from `b7ba00`: what that generation was, what is
   historical only, and what the recovery is for.
5. `/home/li/primary/flows/b7ba00/receipts/readiness-announce.md`
   `a3253d14c56f7aa4997f60098b59aed41f2444577ba5aa6041242fbefcfc25b9`
6. `/home/li/primary/flows/b7ba00/vision/modelFlows.md`
   `5339c9c724df45da9323314c075d14ccef1fc55d7636cc1a569578c0cb3ca6c5`
7. `/home/li/primary/flows/56ae53/vision/model-flow-emergency.md`
   `e7041b49c9fde37c3b4a8d1729bb2ea403acbd528b7fb2aef39033b1421c2cce`
8. `/home/li/primary/flows/56ae53/log.md`
   `88720dec1a4e6c8062639fcc442bfa7b68f337ff86c2ea1c2231d4fff462995f`
   This log grows, so read the file and treat a changed hash as expected here
   alone. Every other hash above is binding.
9. `/home/li/primary/flows/56ae53/fable-recovery/README.md`
   `5ce0f89cd58378d6cfe407e0cf9c72269fb9c61f601a5360ee247efbab157734`
   The predecessor packet's own launch note, superseded on the first-line
   mechanics by `/home/li/primary/flows/38f337/fable-launch/README.md`.

Entries 1 through 3 were previously named here without hashes, only mentioned
beside the vector. They carry the content the packet actually hands over, so
they are hash-bound now: naming a path without binding its bytes authenticates
nothing.

## The system-prompt bundle

`/home/li/primary/tools/main-flow-mode/system-prompt.md`
`a0cfec7610d9908db6a7b9abaf5c5329f3fa2817a56e4699d708e3b8d8bfb03a`

This is the profile's `system_prompt_bundle_file`: an absolute, existing,
non-symlink regular file, as `LaunchComposer::validate` requires. The Nexus
copies it per launch into its launch-bundle directory with the launch section
appended, and the composed first line names that copy, never this path.

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
