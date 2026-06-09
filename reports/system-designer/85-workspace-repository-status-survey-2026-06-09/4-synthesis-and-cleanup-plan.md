---
title: 85.4 — synthesis — workspace repository status & lean-set cleanup plan
role: system-designer
variant: Synthesis
date: 2026-06-09
topics: [workspace-status, repository-inventory, repo-hygiene, lean-repo-set, cleanup, two-contract, index-drift, archive, survey]
description: |
  Consolidated whole-workspace repository status across 138 on-disk checkouts,
  synthesised from the frame (metrics + index drift) and three cluster scouts
  (two-contract completeness, non-Persona tooling, creative/web/OS). Buckets
  every repo as KEEP-ACTIVE / KEEP-ADJACENT / ARCHIVE / RETIRE / ASK-PSYCHE
  against the lean-set principle (bds6). Headline: the aski family (13 repos) is
  explicitly dead; the workspace is already leaner on disk than its index files
  claim; five live components lack a meta-signal contract; a long tail needs
  psyche adjudication. Ends with a staged cleanup order and the decision list.
---

# 85.4 — synthesis & cleanup plan

## The shape in one paragraph

138 repos on disk. A coherent ~70-repo **Persona core stack** (≈210k Rust LOC
in the runtime crates plus ~40 thin contract repos) is hot and healthy — the
reset is landing. Around it sits a **long tail of ~45 non-core repos**: a few
live adjacent surfaces (nexus, mentci, kameo, chroma/chronos, the poet books,
two websites), and a large sediment of **frozen, superseded, and dead projects**
the lean-set principle (`bds6`: *"150 active repos is too many"*) says to
archive. The single biggest win is the **aski language/compiler family — 13
repos, explicitly retired by the psyche**. The workspace is already leaner on
disk than its index files claim, but the indexes were never updated after the
recent migration, so they now point at deleted repos.

## What's healthy (KEEP-ACTIVE) — the Persona reset

The core stack is on-discipline and active (all committed 2026-06-08/09):

- **Foundation:** `schema-next` + `schema-rust-next` (schema→Rust emission,
  ~32k LOC), `nota-next` + `nota-config` (NOTA), `sema-engine` (DB boundary),
  `signal-frame` (wire substrate), `triad-runtime`, `signal` + `signal-sema`
  (vocabularies), `version-projection`.
- **Components (daemon + triad):** `persona`, `mind`, `router`, `message`,
  `terminal` + `terminal-cell`, `harness`, `system`, `introspect`, `orchestrate`,
  `cloud`, `criome`, `domain-criome`, `repository-ledger`, `upgrade`, `spirit`
  (+ production `persona-spirit`), `nexus` + `nexus-cli`.
- **~40 contract repos** `signal-*` / `meta-signal-*` — the bulk of the count.

Adjacent live surfaces (KEEP): `mentci-lib`/`mentci-egui`/`mentci-tools`,
`kameo` (+ testing spikes), `arca`/`hexis`/`library`/`maisiliym` (sema-adjacent
infra), `chroma`/`chronos` (system-operator daemons), `TheBookOfSol` /
`TheBookOfGoldragon` / `caraka-samhita` (poet), `AnaSeahawk-website` /
`WebPublish` (web), `goldragon` (production cluster data), `forge`/`signal-forge`
(paused criome-stack executor), CriomOS family (Stack A production deploy).

## What's drifted (owned by frame; recap)

- **5 broken `repos/` symlinks** — all `owner-signal-*` (deleted per `hnpo`).
  Remove the symlinks (untracked local index).
- **15 dead `RECENT-REPOSITORIES.md` entries** — the old `persona-*`-prefixed
  stack + retired `nota`/`nota-codec`/`nota-derive`/`signal-core`/`prism`.
  `RECENT-REPOSITORIES.md` and `active-repositories.md` both need a refresh.

## Two-contract completeness (scout 1)

Against `n0ss` (every component = `signal-<c>` + `meta-signal-<c>`):

- **COMPLETE pairs (11):** persona, mind, router, terminal, orchestrate, cloud,
  domain-criome, repository-ledger, upgrade, spirit, lojix.
- **MISSING-META (5 live gaps):** `message`, `harness`, `system`, `introspect`,
  `criome` — each has the ordinary contract, no meta. All freshly worked, so
  these are gaps to fill, not dead ends. (criome's auth substrate is plausibly
  meta-less by design — undeclared.)
- **`owner-signal-*`:** fully gone on disk — deprecation complete. ✓
- **Off-pattern / superseded:** `signal-sema` (misnamed — it's the universal
  Sema observer vocabulary, no `sema` daemon; see report 83), `signal-executor`
  (superseded by nexus per `gb87`; survives as a shared library, not a wire
  contract).
- **Stale concept stubs (no INTENT.md, last touched 2026-05-24):**
  `signal-derive`, `signal-sema-upgrade`, `signal-forge` (the last is
  intended-but-not-adopted; the other two look abandoned).

## What to archive / retire (the lean-set work, `bds6`)

### ARCHIVE — dead, superseded, frozen (recommended batch)

| Group | Repos | Evidence |
|---|---|---|
| **aski family (13)** | aski, askic, askicc, aski-cc, aski-core, astro-aski, vscode-aski, corec, synth-core, veric, veri-core, domainc, noesis-schema | `aski` carries explicit psyche banner *"aski is dead, it was the wrong way"*; `veric` already gutted. The old compiler/language project. |
| spec/old archives | nexus-spec-archive | superseded grammar spec |
| dead misc | ndi (2023), atom (2024, third-party mirror), awesome (2025, third-party list) | no Persona relation, long cold |

The aski 13 is the headline: archiving it alone is the largest single reduction
in the active set.

### RETIRE / fold — stubs and stale siblings

| Repo | Action |
|---|---|
| `signal-derive`, `signal-sema-upgrade` | abandoned concept stubs — retire (confirm no consumer) |
| `schema-core` | spent witness, superseded by schema-next (per 83) |
| `horizon-next` | scaled-down PoC, superseded by `horizon-rs` — retire |
| `orchestrator` | old-name predecessor of `orchestrate` |
| `spirit-next` | symlink → spirit (already noted in 82) |

## Decisions needed from the psyche (ASK)

The genuinely ambiguous repos — I can't resolve these from intent or code:

1. **`semac` / `noesis`** — got later schema commits; do they carry into the
   live sema backend, or are they aski-era legacy to archive?
2. **`workspace`** — its coordination role overlaps `primary`; is it a
   predecessor to retire?
3. **`webpage`** (ligoldragon.com, Hugo) — superseded by `WebPublish`, or still
   the live site?
4. **`arbor`** — versioning/storage substrate overlapping `arca`; keep both?
5. **`pi-delegate`** — still used (Pi/assistant surface)?
6. **`Armbian-RockPi4B-NixOS`** — stale one-off bootstrap; keep/archive?
7. **`test-city`** — scratch (82 already flagged); confirm retire.
8. **`prism`** — referenced (criome-executor vision, paused-not-dead per 83) but
   **absent from disk** — already gone, or needs re-checkout?

## Systemic gap — INTENT.md coverage

Per the repo-intent discipline every repo needs an `INTENT.md` read before code.
Coverage is thin outside the core daemons: ~4/43 non-Persona repos and ~5/20
creative/web repos have one. The lean-set move resolves most of this — archive
the dead (no INTENT needed), then write INTENT.md only for the confirmed
keepers. Don't write INTENT for repos headed to archive.

## Migration debt still open (not cleanup, but status)

- `sema` (old storage kernel) — still has consumers that should move to
  `sema-engine`-only (`fosp`).
- `orchestrate` — not yet on emitted `triad_main` + `sema-engine` (ocu7;
  see 82 §5).
- The 5 missing `meta-signal-*` contracts (above).

## Recommended staged order (all archive/delete needs psyche go-ahead)

1. **Index refresh (low-risk, primary commit, reversible):** update
   `active-repositories.md` + `RECENT-REPOSITORIES.md` to disk reality; remove
   the 5 broken `owner-signal-*` symlinks. (I can do this now on request.)
2. **Archive batch** (psyche go-ahead): aski family (13) + nexus-spec-archive +
   dead misc. Biggest lean-set win.
3. **Resolve the ASK list** (8 items above) → archive/keep each.
4. **Retire stubs/siblings:** signal-derive, signal-sema-upgrade, schema-core,
   horizon-next, orchestrator, spirit-next.
5. **Fill two-contract gaps:** create `meta-signal-{message,harness,system,
   introspect,criome}` or declare them intentionally meta-less.
6. **Schedule migration debt:** sema→sema-engine consumers; orchestrate→triad_main.

Archiving/deleting a GitHub repo is irreversible and outward-facing — nothing in
§2–4 executes without explicit per-batch psyche authority.
