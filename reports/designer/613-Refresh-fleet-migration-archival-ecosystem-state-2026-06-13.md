---
title: 613 — Refresh — fleet migration, repo archival, ecosystem state (the architecture replacement)
role: designer
variant: Refresh
date: 2026-06-13
topics: [migration, workspace, repositories, archival, ecosystem, dependencies, signal-executor, nexus, contract, schema-next, persona-engine, audit, cleanup]
description: |
  Agglomerated current-state surface for the fleet-wide architecture-replacement
  arc — migrating every component daemon onto the schema-derived triad runtime,
  removing the old execution path (signal-executor -> nexus), migrating contracts
  to schema-next, and archiving the deprecated repos. Merges designer 544, 551,
  554, 555, 556, 557, 558/*, 559, 562, 563, 574/*. Carries the standing picture
  (we are REPLACING the architecture, not maintaining it), the three migration
  axes (daemon shell / execution / contracts), the repo archival results, and the
  per-component migration plan + residual debt.
---

# 613 — Refresh — fleet migration, repo archival, ecosystem state

Landing witness for the fleet-wide architecture-replacement arc. The 11 source
reports it merges are deleted in the same commit; git history holds them. The
durable principles this arc rests on are already Spirit records (cited inline); this
Refresh is the working snapshot of how they apply right now, expected to retire as
the migration completes.

## Intent Anchors

[We are pre-production: design the single best shape, expect every component to
change, never weigh backward compatibility as a virtue.] (Spirit `ax2k`)

[Usage does not justify keeping a superseded dependency — a migration is incomplete
until the superseded dependency and execution path are removed; wrapping is not
migrating.] (Spirit `hehp`, `ng1x`, `v3um`)

[Migrate component by component, smallest first, tested before moving on.] (Spirit
`r310`)

[A contract's Rust is always regenerated from its schema; the schema is the single
source of truth.] (Spirit `ug6i`)

## 1. The frame — replacing, not maintaining

This is an in-flight architecture overhaul, not maintenance (designer 559). Every
component daemon is migrating onto the schema-derived triad runtime (designer 612);
the old execution path and old contracts are being removed, not wrapped. The picture
is shared so agents stop re-litigating it each session. It is expected to go stale
and retire as the migration completes.

## 2. The three migration axes

A component is "migrated" only when all three axes are clean (designer 557):

- **A — daemon shell** -> the emitted triad runtime + kameo EngineActor (designer 575,
  612). Terminal, router, message, orchestrate, spirit, terminal-cell are
  done/in-flight. The terminal slice audit is designer 556 (verdict: works and
  honestly built). `terminal-cell` was ported off its hand-rolled `UnixListener`
  accept loop onto the schema-rust-next emitted daemon shell — DONE, landed to
  terminal-cell main (designer 566); the one residual is the transitional
  `Arc<Mutex<TerminalSignalControlState>>` in the excluded `src/bin/`, a known
  documented drift relocated by the port, with the Kameo `TerminalSignalControl`
  actor owned in `terminal` (ARCH §1.5) as the follow-up.
- **B — execution** -> nexus, remove `signal-executor` (designer 555). nexus is the
  execution engine now (`gb87`); `signal-executor` is the single old-execution-engine
  dependency and the removal gate. The four consumers (orchestrate, upgrade,
  repository-ledger, persona-spirit) were confirmed clean of it (designer 563).
- **C — contracts** -> schema-next-derived `signal-<component>` /
  `meta-signal-<component>` (designer 557). This is the *least*-advanced axis — most
  contracts, including the terminal contracts a daemon shell was already built for,
  are not yet migrated off hand-written / `signal_channel!` generation.

The per-component migration plan (the twelve-component assessment + foundation pass)
is designer 558 — the authoritative read was its synthesis; the residual per-component
debt lives there in git history.

## 3. The ecosystem state — new spine vs legacy

The dependency/usage audit over ~150 LiGoldragon repos (designer 551, the mechanical
Cargo.toml graph + each repo's INTENT.md) established the new-vs-old split per kernel
layer:

- **signal-frame** (new) vs **signal-core** (legacy, its INTENT says DEPRECATED).
- **nota-next** (new) vs **nota-codec** (legacy, ~67 consumers — the big migration
  tail).
- **schema-next / schema-rust-next** (new) vs **schema** (legacy).
- **sema-engine** over the kept **sema** kernel; **triad-runtime** the new daemon
  substrate.

The broad fleet "state of everything" audit (designer 574, ~75 core crates, ~200k
production Rust) found **no architectural rot** — the work is not broken anywhere, it
is **mid-migration**: real daemons, clean contracts, NOTA mostly on genuine typed
codecs, intent-fit aligned for the majority of repos. The live frontier and open
psyche decisions were the designer situation report 544 (the `triad_main!` daemon-emit
chain landed across triad-runtime/schema-rust-next/spirit; ConnectionContext peer-cred
extended it).

## 4. Repo archival — what was removed

Two psyche-directed archival passes ran (designer 554 triage, 562 delete-list):

- **30 repos archived on GitHub** (reversible via `gh repo unarchive`): the 26 clear
  deprecated candidates + `workspace` + `mentci-tools`, plus the abandoned Gas City
  set (`Criopolis`, `orchestrator`, `test-city`).
- **The rule** (`ax2k`/`hehp`): archive deprecated repos regardless of whether draft
  code still imports them — that importing code changes anyway. **One hard limit**:
  the production island (deployed `persona-spirit`, CriomOS) must not lose a remote
  its lockfile still pins, so the delete-set splits by *who still consumes it*,
  established by reverse-dep grep over every active Cargo.toml + the production
  `persona-spirit/Cargo.lock`.
- **Kept**: `mentci-lib` + `mentci-egui` (the real upcoming GUI). `signal-executor` is
  deprecated (nexus is the engine) but **not archived** — still pinned until the four
  consumers' execution paths are physically removed (axis B above).

The post-archival old-code audit (designer 563) confirmed the fleet is cleaner on
patterns than references: no `capnp`, no `ractor`, no `OwnerSignal` naming, no live
`Asschema`, no `signal-core` import, `serde_json` only at legitimate external
boundaries (niri IPC, Pi-RPC, Cloudflare).

## 5. Residual

- **Axis C (contracts)** is the bulk of the remaining work — most contracts not yet
  schema-next-derived.
- **nota-codec's ~67 consumers** are the longest migration tail.
- The per-component residual debt list is designer 558's synthesis (git history).
- The peer-cred / ConnectionContext doc-truthfulness fixes (designer 545 audit) — two
  self-contradicting INTENT.md files and a missing ARCHITECTURE.md trust-boundary
  entry — are operator follow-ups on a landed-and-green feature.
