# 41 · Lojix production refresh — frame and method

## Psyche directive (2026-06-12)

Refresh on the latest core-crate, design, and Spirit state, then finalize the
new lojix logics component for production so the cluster can finally run on the
daemon-based stack. Concretely the psyche asked for:

- **Two CLIs** — one speaking the **meta socket**, one the **regular socket**.
- **Modern schema syntax** — the schema language has changed; expect to rewrite
  the lojix `.schema` files and update all dependencies.
- **Feature parity with production `lojix-cli`** — must deploy a full OS, the
  deploy must survive an SSH disconnect, and *every operation must be described
  in schema types*.
- **End-to-end deployment testing** against a VM / test cluster on another host
  (assign it a reachable IP; adapt the test cluster we already have).
- **Work on `main`** in the triad repos. **Train first** — be well acquainted
  with the new code style before authoring.
- Then deliver a **full report on the situation**.

> The psyche's framing: *"I am pretty sure you can achieve this goalpost."*

## What this meta-report is

This directory is the **refresh / training / reconnaissance** phase. It
establishes ground truth and the staged execution plan. The execution itself —
schema rewrite + dependency bumps, the two CLIs, parity work, VM end-to-end —
follows in subsequent sessions, grounded on what lands here.

## Method

A parallel reconnaissance fan-out (files 1–10), each dimension writing its own
numbered report, then a synthesis (file 11). The orchestrator (cloud-designer)
reads the intent and coding skills directly to retrain, runs the Spirit gate on
the directive, captures the durable psyche intent, and turns the synthesis into
the psyche-facing briefing plus the staged execution plan.

Dimensions:

1. lojix daemon crate — current capability end to end
2. signal-lojix + meta-signal-lojix contract state (the two sockets)
3. dependency crates (signal-frame, signal-sema, sema-engine, triad-runtime,
   schema codegen, horizon)
4. the modern schema syntax — what changed, what must be rewritten
5. two-CLI / meta-vs-regular-socket model
6. coding-skills digest (the current Rust + schema discipline)
7. intent-model digest (how Spirit/intent works now)
8. Spirit topic sweep — durable intent bearing on this work
9. production parity baseline — full-OS deploy, SSH-disconnect survival
10. test cluster / VM deployment-testing availability
11. synthesis + staged execution plan
