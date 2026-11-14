# Missing link in the handover chain: c31020 to e29066

Cause: link 1, the warning. The running Nexus, 0.53.1, never warns a flow before its refresh threshold, so c31020 was never asked to write a handover. Links 2 and 3 behaved as designed when there is no warning: the flow wrote nothing, and the successor's first prompt carried nothing.

## Shown

- Deployed source: flow-nexus-0531.service runs /nix/store/vnfcw4w5…-flow-configured-0.53.1, whose source matches commit fc27dd86 (branch 0.53.1-precompose-e8b6) file for file.
- The warning work, b2460bbc "Flow 0.53.1: a flow is warned before its threshold", is not an ancestor of fc27dd86. It sits on 0.53.1-warning-b75b, 0.53.2-restart-codex-b75b and 0.53.3-restart-owed-b75b.
- The deployed code says it outright, waking.rs:2928-2929: a seat past its threshold "is told nothing and writes no handover". store/context.rs:158-177 has only a refresh threshold (Below, Protected, Past). The thresholds config holds { claude-opus-5-5 200000 } and no warning share.
- The Nexus did know the context size: every Stop ran flow-hook (46 times), and record_context_at_stop (waking.rs:2640-2652) reads the tokens.
- c31020 passed 170,298 tokens (15% of refresh left) at 06:25:29Z, then 200,110 at 07:17:29Z, and was refreshed at 07:18:43Z. Its transcript holds no handover Notice, and it wrote no handover.md.
- Link 3 works: handover.rs:43-63 reads flows/<pred>/handover.md, and when the file is missing (Absent), composition.rs places nothing. e29066's first prompt (07:18:43Z) is module text only.

## Inferred

- The warning missed the 0.53.1 cut rather than being dropped on purpose. No record of the reason was found.

## Side observation, cause unknown

- A Soft Notice was submitted to c31020 right after a Stop (07:18:34Z), and c31020 started a turn. The refresh closed the seat inside that turn, because waking.rs:2989 closes a Claude seat that is due for refresh whatever it is doing. With Soft waiting for idle (Fable's ruling, 0.53.3), this race narrows. The close itself still wants checking.

## Fix plan

1. Target 0.53.3. It already holds the warning work (717ec6d8, 1faf8ff5, b84fabd7, 0a5d2cdf, 87b92665): settle_rested sends due handover reminders at the Stop measurement and refreshes only once the handover is green.
2. A ruling is needed first. In 0.53.3 the warning asks the flow to run flow 'Keep…' / 'Drop' commands (handover_reminding.rs:33-64), and the successor's handover is read from Nexus Memory (handover.rs:5-8). The vision says a HardAbrupt Notice naming flows/<id>/handover.md, with that file as the successor's first prompt. Which holds?
3. Configure a warning share per model, 0..=100 (store.rs:5605). There is no default; it goes beside thresholds.datom.
4. Deploy 0.53.3 as its own unit. Witness the chain on one flow: its context crosses the share, the Notice arrives, the handover is written, and the successor's first prompt carries it.
