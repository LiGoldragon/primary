# 0 · Frame and method — cloud component design recap

Session-spawning prompt (psyche, 2026-05-27): *"recap situation with
cloud component design"*, with `skills/context-maintenance.md`
cited and "subagents" named as the dispatch shape.

This is the orchestrator frame for the meta-report directory; the
sub-agent reports land beside it as numbered files, and the
synthesis lands as the highest-numbered file
(`4-overview.md` here).

## What I'm trying to recover

The cloud component is a triad target that has been accumulating
intent in Spirit and (probably) substance across a few report
lanes. The psyche's prompt is *recap*, not *design* — the task is
to surface the current settled state and the open questions in a
form a future cloud-designer session can pick up from. The recap
should answer four questions:

1. **What IS cloud** as a component? Purpose, identity in the
   triad family, relation to adjacent components.
2. **What is its scope**, both as already-decided and as
   projected? Cloudflare DNS is the named first ground; what else?
3. **What design decisions are settled** vs. **still open**?
4. **Does the code exist yet**, in any form, anywhere? Or is it
   wholly aspirational?

## Method — three parallel Explore subagents

The substance lives in three roughly-independent surfaces, so the
sweep parallelises naturally. Each subagent gathers from one
surface and writes its findings to a numbered report in this
directory. Dispatch is non-blocking (workspace rule — every
subagent goes to background, even when synthesis depends on the
return). The harness notifies when each completes; the
orchestrator synthesises once all three are in.

**Sub-agent 1 — Spirit substance.** Reads every cloud-topic
Spirit record (description-only and with-provenance), organises
into (a) identity, (b) scope, (c) settled decisions, (d) open
questions, (e) explicit constraints. Quotes record IDs. Lands
at `1-spirit-substance.md`.

**Sub-agent 2 — Cross-lane reports sweep.** Greps every
`reports/<lane>/` for cloud-component-design substance.
Distinguishes settled design from open questions from adjacent
mentions. Surfaces the seven existing reports under
`reports/cloud-operator/` and decides which (if any) are actually
about cloud-component design vs. pi-harness operations. Lands at
`2-existing-reports.md`.

**Sub-agent 3 — Repos and architecture.** Checks
`protocols/active-repositories.md` and `/git/github.com/LiGoldragon/`
for cloud, signal-cloud, owner-signal-cloud, or persona-cloud
repos. Recovers triad-shape discipline from
`skills/component-triad.md` so the recap can ground in the
template the cloud component would adopt. Lands at
`3-repos-and-architecture.md`.

## Synthesis target

`4-overview.md` will weave the three sub-agent findings into the
four-question recap, ending with a short "next move" pointer for
the next cloud-designer session. The overview is the artifact
the psyche reads; the sub-agent reports are the underlying
material in case the synthesis is missing nuance.

## Out of scope for this pass

- Designing the cloud component or proposing changes to its
  shape — this pass is recap-only.
- Auditing the existing `reports/cloud-operator/` directory for
  context-maintenance migration. (Worth a separate pass; lane was
  written to before being registered, and the seven reports
  there look pi-harness-flavoured.)
- The cloud-designer lane scope-definition itself
  (deferred from `1-lane-bootstrap-2026-05-27.md`, still
  awaiting psyche direction).
