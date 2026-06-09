---
title: 85.0 — frame & method — workspace repository status survey
role: system-designer
variant: Frame
date: 2026-06-09
topics: [workspace-status, repository-inventory, repo-hygiene, cleanup, lean-repo-set, index-drift, two-contract, survey]
description: |
  Orchestrator frame for a whole-workspace repository status survey requested
  by the psyche after a heavy renovation period ("a lot of activity and
  renovation, now we need to clean up"). Establishes the intent grounding,
  the hard metrics across all 138 on-disk repos, the index-drift finding, the
  core-stack sizing, and the three background scouts dispatched over the
  clusters prior audits skipped. Synthesis lands in the highest-numbered file.
---

# 85.0 — frame & method

## Request

Psyche, 2026-06-09: refresh skill + intent (read, not edit), then survey the
whole workspace — every repository, how big, how active, its role, and whether
it still fits ("active / in-between / deprecated"). Include my own assessment
even where it may diverge from intent. Come back with one or more reports and
questions. Subagent scan authorized for the wide area.

**Spirit gate:** working order (a status survey + cleanup-prep; dies if the
task is erased) → no capture. Psyche asked to refresh intent → Observe/refresh
(done; records below).

## Intent grounding (Spirit, refreshed this session)

- **`bds6`** (Principle) — keystone: *keep the active repository set lean;
  superseded, dead, duplicate, and stub repositories are archived rather than
  left to clutter; a smaller active set is better. 150 active repos is too
  many.* This is the intent behind the request.
- **`op4b`** (Correction, VeryHigh) — agents must NOT create repos for breaks /
  experiments / mockups / repros / design passes; that work is feature branches
  in worktrees. `major-break-via-new-repo` skill retired. New repos only on
  explicit psyche authority. Names the throwaway repos already retired.
- **`hnpo`** (Decision, VeryHigh) — `MetaSignal` canonical; `OwnerSignal`
  deprecated. Every policy contract is `meta-signal-<component>`.
- **`n0ss`** (Correction, VeryHigh) — every component has EXACTLY two contracts:
  `signal-<c>` + `meta-signal-<c>`. No third, no owner-signal, no
  engine-management split.
- **`gb87`** (Clarification) — nexus is the execution engine; `signal-executor`
  / executor role superseded.
- **`cb0j`** (Constraint) — during multi-component migration, claim/lock one
  component at a time.
- repo-intent skill (`944`, Maximum) — every repo needs an `INTENT.md`, read
  before code; its absence is the first gap to fill.

## Method

1. Read ESSENCE / workspace INTENT / active-repositories / RECENT-REPOSITORIES;
   query `skills.nota`; refresh Spirit (recent + repo-hygiene topics).
2. Hard metrics sweep across all 138 `/git/github.com/LiGoldragon` checkouts:
   last commit date, commit count, tracked file count, branch count; Rust LOC
   for the core stack.
3. Detect index drift (broken `repos/` symlinks; dead `RECENT-REPOSITORIES.md`
   entries).
4. Fan out three background scouts over the clusters prior audits (82/83)
   explicitly skipped or that the recent migration changed:
   - `1-component-two-contract-audit.md` — current-disk two-contract
     completeness across the Persona component stack (refreshes 83's contract
     section under `n0ss`/`hnpo`).
   - `2-non-persona-tooling-cluster.md` — the ~45 non-Persona software repos
     (aski*, mentci*, noesis*, veri*, kameo*, nexus*, misc tools) marked
     "out of audit scope" in 82/83.
   - `3-creative-web-os-cluster.md` — books, websites, wiki, chroma/chronos,
     CriomOS family, forge.
5. Synthesis (highest-numbered file): consolidated status + lean-set
   recommendation + questions.

This survey **supersedes the now-stale parts of reports 82 and 83**: since those
landed (2026-06-07) the current-stack migration (`nota-codec`→`nota-next`,
`signal-core`→`signal-frame`, `sema`→`sema-engine`) advanced across the fleet,
the throwaway-repo and `owner-signal-*` families were deleted from disk, and 83's
contract section was superseded by `n0ss`. Report 85 is the current picture.

## Index drift (owned by this frame)

The on-disk `/git` set is already LEANER than the workspace index files claim —
the recent migration deleted repos the indexes still point at.

**Broken `repos/` symlinks (target deleted) — 5, all deprecated OwnerSignal:**
`owner-signal-agent`, `owner-signal-mind`, `owner-signal-orchestrate`,
`owner-signal-router`, `owner-signal-terminal`. Pure cruft; remove the symlinks
(`repos/` is untracked local index).

**`RECENT-REPOSITORIES.md` entries no longer on disk — 15:** the entire old
`persona-*`-prefixed component stack (`persona-mind`, `persona-message`,
`persona-router`, `persona-system`, `persona-terminal`, `persona-harness`,
`signal-persona-mind`, `signal-persona-message`, `signal-persona-system`,
`signal-persona-harness`), plus retired core crates `nota`, `nota-codec`,
`nota-derive`, `signal-core`, and `prism`. These confirm the migration landed;
the index was never updated. `RECENT-REPOSITORIES.md` and
`active-repositories.md` both need a refresh pass (tracked files — a primary
commit).

## Hard metrics — all on-disk repos

138 checkouts. Activity buckets by last-commit date (full per-repo table follows).

### Core Persona stack — size (Rust LOC) and activity

All committed 2026-06-08 unless noted; this is the live reset surface.

| Repo | RS LOC | files | role tier |
|---|---:|---:|---|
| schema-rust-next | 19507 | 55 | Rust emission engine |
| persona | 15006 | 76 | meta-repo / engine-manager |
| persona-spirit | 13879 | 51 | production Spirit (Stack A) |
| mind | 13544 | 63 | central state component |
| router | 12973 | 47 | message routing |
| schema-next | 12897 | 59 | schema engine |
| spirit | 12693 | 51 | schema-derived Spirit pilot |
| terminal | 10760 | 58 | terminal owner |
| cloud | 9798 | 31 | provider API runtime (triad_main pilot) |
| orchestrate | 9180 | 53 | orchestration runtime (pre-triad_main) |
| upgrade | 7567 | 38 | upgrade/handover scaffold |
| signal-frame | 6774 | 65 | live wire substrate |
| terminal-cell | 6705 | 41 | PTY/transcript primitive |
| nota-next | 6122 | 25 | NOTA structural lib + codec |
| sema-engine | 5832 | 36 | in-process DB engine boundary |
| harness | 5502 | 38 | harness control |
| message | 5241 | 41 | engine message ingress |
| triad-runtime | 5208 | 30 | shared daemon runtime |
| domain-criome | 4342 | 26 | domain registry runtime |
| criome | 3882 | 33 | trust/attestation daemon (in-flight port) |
| repository-ledger | 3181 | 22 | gitolite push ledger |
| introspect | 3109 | 32 | inspection plane |
| system | 2945 | 34 | OS observation (deferred) |
| signal | 2109 | 40 | sema-ecosystem record vocabulary |
| signal-sema | 1359 | 26 | SEMA-op observer vocab (misnamed — see 83) |
| nexus | 1202 | 34 | execution-engine NOTA vocabulary |
| sema | 1053 | 26 | old storage kernel (migration debt) |
| version-projection | 584 | 15 | version projection lib |
| nota-config | 508 | 23 | typed config decode |
| nexus-cli | 87 | 21 | nexus CLI (thin) |

Core stack ≈ 210k Rust LOC. The emission/schema pair
(`schema-rust-next` + `schema-next` ≈ 32k) and the four state-heavy daemons
(`persona`, `mind`, `router`, `spirit` ≈ 54k) dominate.

### Contract repos (signal-* / meta-signal-*) — small, many

~40 contract repos, each 11–26 tracked files, 3–70 commits. These are the bulk
of the repo count and the primary lean-set pressure (`bds6`). Two-contract
completeness is audited in `1-component-two-contract-audit.md`.

### Full activity table

See the raw sweep in the synthesis file; activity tiers:
- **Hot (last commit 2026-06-08/09):** the entire core stack + most contracts (~75 repos).
- **Warm (2026-06-05..07):** lore, schema-next, sema, forge, nexus-cli, library, goldragon, criomos-horizon-config, caraka-samhita, several contracts.
- **Cooling (2026-05):** horizon-next, schema-core, semac, signal-forge, kameo*, CriomOS-test-cluster, lojix-archive, hexis, whisrs, mentci-egui, arca, WebPublish, kibord, orchestrator(old), nexus-spec-archive.
- **Cold/frozen (≤2026-04):** aski* family, veri*/corec/synth-core, noesis*, domainc, arbor, vscode-aski, maisiliym, annas-mcp, pi-delegate, AnaSeahawk-website, TheBookOfGoldragon, BookMaker, Armbian-RockPi4B-NixOS, atom (2024), ndi (2023), awesome (2025), wiki (2025).

## Scouts dispatched

Three background general-purpose scouts (system-designer lane), each writing a
numbered report here and returning a summary. Synthesis follows on completion.
