# 92 — A reusable version-controlled Sema-state library: frame and method

Frame for this dispatched-subagent session. It continues the arc of
report 91 (versioning component Sema databases) and its design file
`91-component-db-version-control/7-design-log-as-source-of-truth.md`,
plus system-operator audit `208`.

## What the psyche asked

In one sitting, three things:

1. **Refresh** the recently-covered topic (server-backed atomic version
   control of component Sema state), study the current architecture
   (spirit as the poster-child), and refresh skills/guidelines.
2. **A new, explicitly-important intent:** the version-control aspect of
   Sema must be **reusable** — built **once** as a library of generic
   types and traits, **not** reimplemented per component. Every component
   is to have the *option* to version-control its state through this one
   shared mechanism. The psyche flagged this as high importance but low
   certainty on *how*.
3. **A two-track deliverable:** first a **comprehensive context report** —
   "all the problems, all the constraints, all the things to watch for,
   what's been done before, what worked, what didn't, what applies to our
   system, what doesn't, what we're going for" — **without deciding how
   it will be done.** Then the psyche passes that report to an operator
   to implement something real on a component's main branch, *while* this
   designer lane works concept branches in worktrees (forking sema /
   sema-engine, new repos as needed, feature branches). The psyche
   explicitly wants **both** the same-file log and the separate-file log
   tested — more than one implementation is welcome.

This report is the **first** deliverable, the gate before implementation.

## Spirit gate

Outcome: **Record.** The reusability constraint is durable, psyche-sourced
intent, and the psyche explicitly authorized logging it. Captured as
Spirit **`j487`** (the build-once-as-a-reusable-library constraint;
importance High, certainty Medium — the reusable-library *direction* is
firm while the exact generic *mechanism* is undesigned). It **extends
`29pb`** (the atomic, server-backed, native-version-control constraint;
state loss unacceptable; native VC, not opaque blob).

The *mechanism* remains design, not intent — so this report maps it and
proposes nothing as new intent. Only the psyche is the source of new
intent.

## Deliverable discipline — this report decides nothing

The psyche was explicit: *"Don't decide on how it's going to be done.
Just list all of the things to watch for."* Every chapter and the
synthesis frame **options with tradeoffs** and **deliberately do not pick
a winner**. The adversarial critic was tasked specifically with catching
any place the synthesis slipped into deciding.

## Method

A background Workflow (`reusable-versioned-sema-context`, run
`wf_5c498d3b-72c` — the 20-agent research fan-out): **5 grounding
agents** reading our real code, **10 prior-art agents** (web-verified),
**2 design-space agents**, then **synthesis → adversarial critic →
revise**.

| Phase | Agents | What they establish |
|---|---|---|
| Ground | `ground-sema-kernel`, `ground-sema-engine`, `ground-spirit-poster-child`, `ground-existing-version-infra`, `ground-server-and-ingest` | The real on-disk kernel, the engine's genericity mechanism (the reusability crux), what spirit hand-rolls that a library would absorb, the no-reinvent boundary against existing upgrade/version-handover infra, and the server/ingest/content-hash facts. |
| Prior art | `prior-dolt-noms-prolly`, `prior-datomic-family`, `prior-git-mercurial-fossil`, `prior-irmin-ipld`, `prior-terminusdb`, `prior-event-sourcing-cqrs`, `prior-wal-shipping-replication`, `prior-crdt-patch-theory`, `prior-serialization-evolution`, `prior-cdc-backup-fs-snapshot` | Everything that looks remotely like what we're doing — what worked, what didn't, what applies, what doesn't. |
| Design space | `space-genericity-rust`, `space-log-file-experiments` | How to be reusable in Rust without a stringly-typed generic-record store (the central tension); and the same-file-vs-separate-file experiment matrix. |
| Synthesis | `synthesis` | Ties the chapters into the comprehensive context map. |
| Critique | `critic` | Adversarial accuracy + cargo-cult + completeness + did-it-decide check. |
| Revise | `revise` | Applies corrections; produces the final synthesis + ledger. |

The numbered chapter files and the highest-numbered synthesis file are
written into this directory when the workflow lands.

## Inherited context the agents build on

The accepted *direction* (report 91 file 7 + audit 208), **not a decided
spec**: version the log not the store; migration as a typed
`SchemaTransition` + checkpoint; a typed replay envelope keyed by
schema-hash; digests beside (not replacing) monotonic markers; per-store
remote durability levels with a named RPO; a first-class checkpoint
protocol; and the rejection of prolly-trees and git-as-substrate as
Dolt-by-analogy cargo-cult. The kernel inversion (log authoritative,
redb a view) remains the `sema` / `sema-engine` owners' call.
