# 708-0 — Frame & method: audit of yesterday's designer work

Psyche prompt (2026-06-21): *"audit everything we did yesterday. look for
gaps, unmerged good ideas, winded/difficult to read code, repetition, and
just generally ugly patterns and code. assemble the picture of
size/logic/architecture with visuals and code blocks with the most complex
scenario tested for everything."*

**Spirit gate:** no capture. This is a task-only order — it dies when the
task is erased (task state, not durable intent). The durable
worktree-registration intent from the prior prompt is already recorded as
`eh5a`. No new Decision/Principle/Correction/Clarification/Constraint.

## What "yesterday" (2026-06-20) means here

Yesterday's designer-lane work, by the git log, is two bodies:

1. **The 707 task — mentci re-founding + worktree registry.** Built as
   designer prototypes on branches, **now integrated on main by operator**
   (`operator: integrate mentci and orchestrate wave2 handoffs`, report
   447). Eight repos:
   - mentci cluster (intent `7x5z` / `t00s` / `p43g` / `pviw`/`gc0n`): `mentci-lib`
     (the re-founded keystone), `signal-mentci`, `meta-signal-mentci`,
     `mentci` (daemon), `mentci-egui`.
   - worktree-registry cluster (intent `eh5a`): `signal-orchestrate`,
     `meta-signal-orchestrate`, `orchestrate` (daemon).
2. **The 706 tail — criome E1 cross-criome peer transport.** Increment 3
   hardened + re-verified yesterday; **still on branch**
   (`criome-peer-transport` / sibling `signal-criome-peers`), not on main.
   Included for completeness as a context-priority target.

Because operator already integrated cluster 1, the audit target is the
**current `main`** of those repos (what actually survived integration), not
the retired designer prototype bookmarks. The "unmerged good ideas" lens is
baselined against the 707 reports (which document the prototype content in
full) and the operator integration reports (445/446/447).

## Size picture (measured at frame time)

| repo | src LOC (mixed hand/generated) | role |
|---|---|---|
| mentci-lib | 1115 | shared state-machine library — re-founded keystone |
| signal-mentci | 1877 | mentci working signal (mostly generated) |
| meta-signal-mentci | 815 | mentci meta policy signal |
| mentci | 1336 | mentci daemon + thin CLI |
| mentci-egui | 501 | thin GUI client |
| signal-orchestrate | 3345 | orchestrate working signal (mostly generated) |
| meta-signal-orchestrate | 1303 | orchestrate meta policy signal |
| orchestrate | 8344 | orchestrate daemon (owns redb store) |

~18.6k LOC across 8 on-main repos; a large fraction is schema-generated.
The hand-written-vs-generated split is resolved per repo in `1-size-and-architecture.md`.

## Method — the audit workflow

A single dynamic workflow (`audit-yesterday-designer-work`), 5 phases:

- **Map** — one cartographer per repo (9): size (hand-written vs generated),
  architecture/logic of the delta, and the single most-complex tested
  scenario quoted verbatim.
- **Audit** — one skeptical auditor per repo (pipelined off its map): gaps,
  unmerged ideas, hard-to-read code, repetition, ugly patterns,
  rust-discipline violations, naming, dead code — each with file:line +
  snippet + harm + fix.
- **Cross** — four cross-cutting analyses (barrier on all maps): cross-repo
  repetition/duplication, architecture coherence (with mermaid), report-vs-
  reality gaps, and intent fidelity (`7x5z`/`t00s`/`p43g`/`pviw`/`gc0n`/`eh5a`).
- **Verify** — every high/medium finding handed to an adversarial skeptic
  who reads the real code and defaults to *refuted* unless it truly stands
  (kills false positives like the wave-1 `structural-forms-integration`
  mislabel; respects pre-production = no backward-compat harm).
- **Write** — four parallel section-writers produce finished markdown:
  size+architecture (with visuals), most-complex-test-per-component (code
  blocks), verified findings (severity-grouped), and the executive synthesis.

The numbered files in this directory hold the results; the highest-numbered
file is the synthesis. All audit work is read-only — no repo was modified.
