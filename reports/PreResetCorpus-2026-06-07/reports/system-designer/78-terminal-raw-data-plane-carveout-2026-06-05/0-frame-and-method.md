# 78.0 — Frame & method: the terminal raw data-plane carve-out (psyche study)

Role: system-designer. Date: 2026-06-05. Variant: **Psyche** (written for the psyche to
understand the whole topic). Session unit: this directory. Ultracode session.

## Why this report exists

In the all-component port sweep (report 77), `terminal-cell` was the **only** component
that came back `canStartNow=false`. The reason: its `data.sock` is a **raw byte plane**
(PTY bytes flowing to a viewer), but the canonical daemon shell `MultiListenerDaemon`
assumes every listener speaks **signal-frame** (length-prefixed rkyv frames routed through
the Nexus engine). A triad daemon that needs both a signal-frame control plane and a raw
data plane has no template — that is a foundation decision the recipe does not cover, and
it also gates `terminal`'s per-session viewer plane.

The psyche's response (2026-06-05): *"a raw pass-through listener on multi-listener
daemon … you're going to have to explain to me more of what you mean … do some research on
the whole context of this so I get a full understanding. Make a Psyche report on that
topic and make it thorough. I want to understand the whole thing and the solutions that
you know of, the problem as it is and everything."*

So this is a **teaching + decision report**: the whole context, the problem as it actually
is in source, every solution I know of with tradeoffs, and a recommendation — written so
the psyche fully understands before committing. The psyche's initial lean (raw-passthrough
listener) is carried as a lean, not a settled decision; the carve-out intent is captured
to Spirit only after the psyche confirms post-report.

## Method (workflow `terminal-raw-data-plane-research`)

Two phases. **Read** (3 parallel deep source reads): `terminal-cell` end-to-end (the
`data.sock`/`control.sock` protocols, the PTY/transcript/viewer model, why INTENT forbids
interpreting bytes); `terminal` (its viewer data socket + relation to terminal-cell); and
**the exact MultiListenerDaemon signal-frame coupling** (is the decode hard-wired in the
framework accept loop, or port-controlled in `handle_stream`? — this determines whether
"raw-passthrough listener" needs a triad-runtime change or is already achievable).
**Solutions** (1 architect): the full solution space — raw-passthrough listener, sibling
accept loop, FD-passing via `SCM_RIGHTS`, tunnel-as-opaque-signal-frame, separate
data-daemon — each with tradeoffs and real-world precedent (tmux/dtach/abduco, ssh channel
mux, mosh, conmon/containerd PTY), then a recommendation.

## Output

`1-the-carveout-explained.md` is the thorough psyche-facing document (the whole context +
problem + solution space + recommendation). Raw per-agent detail is in workflow transcript
`w43o3klf0` / `wf_21b0d691-7da`.

## Discipline

Read-only on `/git`. The two durable intents from this turn (meta-signal canonical
`hnpo`; manual upgrade `4lcv`) were captured before this study. The carve-out decision is
NOT yet captured — it waits on the psyche's post-report confirmation.
