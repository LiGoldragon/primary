# Field core Sol handover — flow 66f659

## Live work at refresh

- **d5jk remains open; holding 80 is incomplete.** Its worker safely stopped the one-time transaction at 96% on AC at 09:44:35: selected behavior `auto`, thresholds `0/100`, with no observer, timeout or SSH process remaining. Report: `flows/66f659/battery/one-time-discharge.md`; exact script: `flows/66f659/battery/discharge-transaction.sh`; raw log: `flows/66f659/battery/raw-discharge-to80/transaction.log`.
- Independent `{ Field inventory Sol }` accepted availability `6vbp`; continuation Task `haca` was accepted at cursor 13015 with `Uncertain` delivery and must not be resent. Once read, it owns the one-time continuation across core refresh. It must obtain a positive event acknowledgement, retain the same unconditional cleanup and success end threshold 80, and report to Field core and Fable. Original Fable order d5jk stays open until verified completion.
- The separate locked-idle sampler is stopped: no genuine event, no sample, zero monitor processes. Report: `flows/66f659/battery/locked-idle-followup.md`; preserve `flows/66f659/battery/locked-idle-raw/`.
- **np67** was answered from the consolidated source `flows/db9025/battery/laptop-facts.md`. It distinguishes kernel interfaces from observed UPower signals and does not claim d5jk completion.
- The trace card is gone and its work is finalized; reopen nothing for it.

## Home/source lane

- Home `f64f24d805eed9e5a9d001384524c4b5ba1df480` consumer proof was published only on `flow-66f659-stage1-home-proof`, CriomOS `163a9be4854363183bcab4ff4ca2f86cd60c787e`; report `flows/66f659/updates/consumer-proof-publication.md`. It is superseded and grants no gate.
- Obsolete non-activating UserEnvironment Realize 542 finished `Some.Succeeded`; every profile/runtime and Lojix invocation stayed unchanged. It has no artifact handoff or acceptance value. Report: `flows/66f659/updates/stage1-proof/obsolete-materialization-report.md`.
- Final drift-closed Home source is `544e63ca762fb8d9d7f882fabb8aeb60dfd7bde2`, expected transitive persona `e1ebf473fb100489a52cab4ec6e982e09095feea`. Exact CriomOS remote main is `583e727fb24701295d6a603ea34f9f1b43c504d4`; both CriomOS-origin and explicit HTTPS reads agree. The apparent `3a11b8…` drift was a command-context error: `git ls-remote origin` ran in `/home/li/primary` and queried `LiGoldragon/primary.git`. Evidence: `flows/66f659/updates/remote-main-ref-audit.txt`. No 544 branch/worktree was created; prepare its new isolated proof consumer from exact 583 only after refresh authority, and do not reuse/promote 163a.
- q188 generally authorizes proof-only publication, checks and Realize. Production mains and every activation wait full checks, exact RAW occupied-unit/sd-switch no-reach evidence, and replay/session authority proof; a Flow Nexus 0.54.7 audit is requested. Live occupied provenance is stable `4p67nm…0.167.1`, next `g2sf…0.158`, recorded in `flows/d09f73/stage1-occupied-server-provenance.md`; the current Home is `527sd47…`, request `63c637`.
- Replay proof must preserve every existing SendServer identity and endpoint route through **each** sequential non-atomic replay query; `Configured.Replaced` alone proves nothing. Forthcoming report: `flows/d09f73/stage1-flow-replay-semantics.md`.

## Other retained state and orders

- Lojix A/B/A materializations 539/540/541 passed without activation; aggregate evidence is `flows/66f659/materialization/materialization-report.md` and `flows/66f659/materialization/aggregate-comparison.md`. Ouranos boot profile/runtime state remains as handed in the launch context; reboot remains the living's choice.
- Prometheus-li orders **ub5l** and **2zei** remain open on the living's ruling: no key, projection/declaration change, Home build, workaround or ast-grep action.
- **izxy** is closed by Result receipt `q7vc`; **np67** was answered, receipt `xzjm`; **d2is** is closed by Result `ybqy` after its Done was correctly refused `Unresolved` because it was an Order. Only **d5jk** remains active besides held ub5l/2zei.
- Wider **pau5** work is held except explicitly authorized battery/update tasks. Independent Field inventory continuation is limited to the d5jk contract above.
- Protected Zeus–prometheus USB/network declarations remain untouched. No ping/link, network, adapter, power, interface, routing, restart, cleanup, main promotion or activation is authorized.
