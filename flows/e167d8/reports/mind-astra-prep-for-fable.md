# Mind Astra 31147a — preparation to talk with Fable before production

From Psyche Opus e167d8, 2026-09-26, on the living's request to 31147a.

## One objective
Bring the cluster onto tonight's integrated state safely: ouranos on Route A (bootstrap deploy, then step-2 deploy), Prometheus boot-once, Zeus first deploy, with nothing but a node's own closure ever landing on it. Flow/Message 0.16 is step 3, after ouranos runs step-2 main.

## Authority and rulings in force
- The living (2026-09-26): "There must never be AI models on any other node than Prometheus, which is why Prometheus can only be built on Prometheus." — "There should be no AI models on [ouranos] ever and we can garbage collect." — "You can reboot Prometheus whenever you want. I don't have any limitation on rebooting it." — Nix builds on Prometheus by default; local ouranos building only as fallback (2026-09-25).
- Fable b860be: integration head — rulings, main-move authority, the morning book. Route A (handoff.md §5); lojix 3fc95f0c (8.1.0, build-on-target) pinned before gates.
- Field Sol b7da5d: deploys (handoff.md rules 3–6), only after b860be's green-main handoff.
- Mind Astra 31147a: bootstrap build, step-2 gates, main moves on green; stop and report on red.
- Psyche Opus e167d8: Flow and Message (0.14 rides step 2; 0.16 is step 3).
- Open with the living: deleting the two Lojix audit roots (~29 GiB each); one lojix skill line on model placement (e167d8's and b860be's proposals, one to land).

## What to check NOW, in order
1. Classify python3.14-pysilero-vad-3.4.0: what it contains (a bundled ONNX voice-activity classifier? size?), which ouranos service or package pulls it in, and whether the copy into ouranos was ouranos's OWN closure returning from a remote build (normal) or Prometheus's closure staging through ouranos (forbidden). Evidence: nix path-info -S, nix why-depends from the ouranos toplevel, file listing. Owner: 31147a. If it is ouranos's own dependency carrying model data, that is a question for the living (is a small bundled classifier an "AI model"?) — do not decide it, and do not strip it silently.
2. Finish the bootstrap builds on Prometheus: ouranos toplevel and ouranos Home activation from 438a04a1. Gate: both build; nothing from Prometheus's closure lands on ouranos. Owner: 31147a.
3. Report to b860be and b7da5d.

## What to deploy NOW, and who
4. Field Sol b7da5d deploys the bootstrap revision to ouranos (Route A deploy 1) on b860be's word. Gates: Evaluate → Realize → TestActivation → ActivateNow, with the Prometheus-hop witness before ActivateNow, heartbeat masks kept.
5. 31147a rebases 416afd41 onto the same two pins, runs the step-2 gates (48 checks, two VM tests, five Home checks, Home build on 7dd9e666) on Prometheus. Green → fast-forward CriomOS main and CriomOS-home main. Red → stop.
6. Field: second ouranos deploy (step-2 main); Prometheus boot-once (any time); Zeus first deploy; daisy-chain test.

## What to test in production after each ouranos activation
- flow-nexus 0.14.0 running: `flow 'List.{}'` shows live seats Active and gone panes Exited (never Retired); a Start continues into its brief with no second prompt.
- Message 0.14.0 running; hm-send still Transports to a live seat (messenger-clj unchanged).
- Herdr up; Claude and Codex seats alive after activation.
- Tailnet enrollment (after step 2) and the Wi-Fi AP country (after step 2).
- ouranos /nix free space before and after (144 GiB free now), and no model paths in its store.

## Blockers
- pysilero-vad classification (step 1).
- Codex seats cannot be started by Flow (Herdr 0.8.2 never fills agent_session for a fresh Codex) — known Flow fault, e167d8's.

## e167d8's response for Fable
- I support Route A and the lojix 8.1.0 pin before gates.
- On pysilero-vad: my inference, not witnessed — it is likely a small bundled voice-activity classifier that is a library dependency of ouranos's own closure, not staged Prometheus content. If Mind finds it is ouranos's own dependency, the placement question is the living's, not ours; if it is Prometheus's closure passing through ouranos, the build path is wrong and 8.1.0 must fix it before any deploy.
- Flow/Message: 0.14 goes with step 2 as pinned. 0.16 (Flow sole pane writer; Message through Flow) goes as step 3; I will rebase its Home bookmark onto step-2 main once main moves, and it needs its own activation and production test (flow-configuration.service active, Deliver presents to a disposable seat, a /compact body refused).

## For the operational skills (candidate guidance only — no edits requested; operational- skills are authored in Curriculum and need the living's review)
- `lojix` (source Curriculum skills/lojix.md): "AI models and Prometheus's closure are built, fetched and stored only on Prometheus; no deploy stages them through another node, and no other node keeps a model." (pending the living's choice between this and b860be's wording)
- A production-readiness checklist per activation (the list under "What to test in production") as an operational skill once the living approves its home.
