---
title: 83 — repo audit — keep / migrate / delete / archive, with dependency evidence
role: system-designer
variant: Audit
date: 2026-06-07
topics: [repository-audit, signal-stack, owner-signal, deprecated, signal-core, sema, signal-sema, orphan, cleanup, dependency-graph]
description: |
  Mechanical reverse-dependency audit of the ~150 LiGoldragon repos, built from
  every Cargo.toml + flake.nix at any depth (478 edges). Per-repo verdict:
  keep (live), migrate (deprecated but still depended-on), delete (dead +
  orphan), archive (intentional). The signal-* / owner-signal- / sema-*
  proliferation collapses to a small live core plus a clear delete list. Method
  is reproducible; delete verdicts carry the consumer evidence. Nothing deleted
  without psyche sign-off on the contract batch.
---

# 83 — repo audit

## SUPERSEDED — read `reports/designer/551-workspace-dependency-ecosystem-state.md`

This report's mechanical zero-consumers→delete heuristic conflated **genuinely
dead** with **intended-but-not-yet-adopted**, and the psyche corrected it
(Spirit `k2o1`, 2026-06-07): *zero consumers does not mean dead — some contracts
are meant to be used and the action is to START using them, not delete them.*
Designer report **551** is the authoritative ecosystem audit; defer to it.

Specific errors in this report's DELETE list, per 551 + psyche:
- **`signal-forge`** — NOT dead; paused-not-dead criome-executor vision cluster
  (`criome → signal-forge → forge → prism → arca`). Deferred, do not delete.
- **`signal-lojix`, `meta-signal-lojix`** — NOT dead; **live-pending**, land with
  the lojix daemon cutover.
- **`signal-spirit`, `core-signal-spirit`** — the persona-prefix-retirement
  rename track; the psyche confirms `signal-spirit` is the **intended** contract
  name for spirit (drop the `persona-` prefix from `signal-persona-spirit`) —
  a target to adopt, not a tombstone.

No deletions from this report's list were executed (the only repos deleted were
the earlier throwaway batch — design passes / mockup / repro / Gas-City — which
551 also classifies as garbage). The genuinely-safe retirements (`spirit-next`
stale checkout, `orchestrator` old-name, `sema-upgrade` + `owner-signal-sema-upgrade`
self-declared-retired, `schema-core` spent witness, the frozen aski compiler
cluster) are catalogued correctly in 551 §"Dead, abandoned, and orphan repos".

## Method (retained for the dependency-graph technique only)

Reverse-dependency graph from **every `Cargo.toml` + `flake.nix` at any depth**
(catches nested workspace crates like `lojix/triad-port/Cargo.toml`): 478
dependency edges. A repo's reverse-dep count = how many repos depend on it via
cargo OR nix-flake input. Zero reverse-deps = "orphan" — but a leaf daemon/app
(cloud, router, a website) is *supposed* to be an orphan, so orphan-status is a
verdict only for **library/contract** repos that exist to be depended on.

## KEEP — the live core (depended-on, current)

| Repo | reverse-deps | Role |
|---|---|---|
| `nota-codec` | 70 | NOTA codec — universal |
| `signal-frame` | 44 | frame/streaming core (the live signal substrate) |
| `schema-rust-next` | 21 | the Rust emitter |
| `signal-sema` | 21 | SEMA-operation observer vocabulary (**live but misnamed — see flag**) |
| `nota-next` | 20 | NOTA structural library |
| `signal-persona-origin` | 19 | persona origin contract |
| `signal-persona` | 15 | persona working contract |
| `nota-config` | 15 | config decode |
| `triad-runtime` | 11 | the runtime kernel |
| `schema-next` | 9 / `version-projection` 9 | schema concept lib / version projection |
| `sema-engine` | 8 | the in-process exclusive DB boundary |
| `schema` 6, `signal-message` 5, `signal-engine-management` 5, `signal` 5, `signal-domain-criome` 4, `nota-derive` 4, `signal-upgrade` 3, `signal-terminal` 3, `signal-router` 3 | … | live contracts/libs |

Plus the live **daemons/apps** (orphans by design — keep): cloud, spirit,
message, mind, router, orchestrate, terminal, domain-criome, lojix, persona,
persona-spirit, harness, system, and the non-stack projects (CriomOS*, books,
websites, aski*, etc. — out of audit scope).

## MIGRATE — deprecated but still depended-on (do NOT delete; migrate consumers first)

| Repo | consumers | Action |
|---|---|---|
| `signal-core` | **23** | DEPRECATED (split into `signal-frame` + `signal-sema`). 23 repos still pull it — fleet migration debt. Delete only after the 23 move to `signal-frame`/`signal-sema`. |
| `sema` | **14** | the old DB kernel. `sema-engine` is the exclusive boundary (`fosp`); 14 consumers should move to `sema-engine`-only. Migration debt, not a delete. |
| `owner-signal-persona` | signal-persona | OwnerSignal deprecated (`hnpo` → MetaSignal). Migrate `signal-persona` to `meta-signal-persona`, then delete. |
| `owner-signal-persona-spirit` | persona-spirit | same |
| `owner-signal-terminal` | terminal | same |
| `owner-signal-version-handover` | persona-spirit | same |

## DELETE — dead + orphan (zero consumers, safe; recommended batch)

| Repo | Evidence |
|---|---|
| `owner-signal-agent` | deprecated OwnerSignal (`hnpo`) + 0 consumers + concept-only draft |
| `owner-signal-mind` | deprecated + 0 consumers + concept-only |
| `owner-signal-sema-upgrade` | deprecated + 0 consumers + concept-only |
| `signal-spirit` | 0 consumers; `spirit` emits its contract in-repo (its deps don't include `signal-spirit`) — dead standalone contract |
| `core-signal-spirit` | 0 consumers; superseded by in-repo emission |
| `signal-agent` | 0 consumers; concept-only; no `agent` daemon exists |
| `signal-forge` | 0 consumers; concept-only draft |
| `signal-lojix` | 0 consumers; `lojix` does not depend on it |
| `sema-upgrade` | 0 consumers; concept-only |
| `semac` | 0 consumers; concept-only |
| `schema-core` | 0 consumers; superseded by `schema` / `schema-next` |
| `noesis-schema` | 0 consumers |
| `spirit-next` | local symlink → `spirit` (shim); remove symlink + delete the stale GitHub repo if one exists |

All have **zero** cargo and flake reverse-deps across the fleet. (`signal-lojix`
/ `signal-forge` / `signal-agent`: confirm there's no out-of-fleet or
deploy-only consumer before deleting — the in-fleet evidence says dead.)

## ARCHIVE — keep, intentional

`criomos-archive`, `lojix-archive`, `nexus-spec-archive` — explicit archives.
They don't need `repos/` symlinks, but keep the repos.

## FLAG — `signal-sema` is live but misnamed (naming decision for the psyche)

`signal-sema` is depended on by 21 repos (incl. `sema-engine` itself, 5×), so
it is **live, not deletable**. But the name is wrong and you caught it:

- There is **no `signal-nexus` and no `signal-signal`** (404) — so it is not a
  per-plane pattern; it's an asymmetric one-off.
- The `signal-<component>` convention means "the working wire contract for
  daemon `<component>`." There is **no `sema` daemon** (`sema` is a library, no
  `src/bin/`), so `signal-sema` is not the contract *of* anything.
- It is actually the **cross-component SEMA-operation observer vocabulary**
  (payloadless labels Assert/Mutate/Match/…), and it's a `.concept.schema`
  draft.

So it wears a component-contract name but is a plane-observability vocabulary.
Recommend a rename (e.g. `sema-observation` / `sema-labels`) and a decision on
whether the cross-component observer layer is actually wired end-to-end (a live
subscriber) or is half-built coupling worth pruning. Distinct from the
**trace system** (`triad-runtime/src/trace.rs`, intra-daemon activation
tracing, used by spirit) — different layer, both real.

## Recommended action order

1. **Delete the DELETE batch** (13 repos above) — zero consumers, evidence in
   table. Needs psyche go-ahead (contract deletion is irreversible).
2. Remove the `spirit-next` symlink.
3. **Schedule the migration debt**: move the 23 `signal-core` consumers to
   `signal-frame`/`signal-sema`; move the 14 `sema` consumers to `sema-engine`;
   migrate the 4 single-consumer `owner-signal-*` to `meta-signal-*`, then
   delete them.
4. Decide `signal-sema` rename + whether the observer layer earns its keep.
5. (Separately, ocu7) migrate orchestrate onto triad_main + sema-engine.
