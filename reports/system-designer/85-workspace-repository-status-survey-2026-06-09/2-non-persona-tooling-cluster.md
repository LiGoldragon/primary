---
role: system-designer
session: 85-workspace-repository-status-survey-2026-06-09
report: 2-non-persona-tooling-cluster
date: 2026-06-09
scope: >
  Classification of the 44 repositories prior Persona-stack audits marked
  "out of audit scope," all under /git/github.com/LiGoldragon/. Read-only
  scout pass. No private-repos inspected. No builds run.
method: >
  Per repo: git log -1 for last-commit date+subject; presence of INTENT.md;
  role read from INTENT.md / README.md / CLAUDE.md / ARCHITECTURE.md or
  top-level listing where no doc exists.
relation_legend: >
  CORE-PERSONA | PERSONA-ADJACENT-TOOLING | SEPARATE-PROJECT |
  EXPERIMENT-OR-SPIKE | ARCHIVE | DEAD-OR-FROZEN | UNKNOWN
verdict_legend: KEEP-ACTIVE | KEEP-ADJACENT | ARCHIVE | RETIRE | ASK-PSYCHE
---

# Non-Persona / Out-of-Scope Tooling Cluster — Classification

Note on naming: in this workspace "Persona" = the live sema-ecosystem
restructuring stack (`nexus`, `nota-next`, the triad/daemon work,
`mentci-*`, `criomed`, `clavifaber`, etc.). "CORE-PERSONA" below means a
repo that is part of that current stack; the audits that skipped these
repos were Persona-stack audits, so several entries land back inside the
current stack on inspection.

Of 44 names requested, **43 directories exist**; `prism` is **absent** from
`/git/github.com/LiGoldragon/` (no `prism*` match) — listed as MISSING.

## Classification table

| repo | role / what-it-is | last commit | relation | fit verdict | INTENT? |
|---|---|---|---|---|---|
| aski | The Aski Language — explicitly RETIRED 2026-04-21; historical design record | 2026-04-25 (retirement banner) | ARCHIVE | ARCHIVE | no |
| askic | The Aski Compiler (generic dialect engine; reads .core/.aski/.synth/.exec → rkyv) | 2026-04-20 | DEAD-OR-FROZEN | ARCHIVE | no |
| askicc | The Synth Compiler (.synth → dsls.rkyv state-machine data) | 2026-04-20 | DEAD-OR-FROZEN | ARCHIVE | no |
| aski-cc | The Aski Compiler "written in aski, compiled by aski-rs" | 2026-05-30 (lockfile refresh) | DEAD-OR-FROZEN | ARCHIVE | no |
| aski-core | Parse-tree rkyv contract crate (askic↔veric↔semac) | 2026-04-20 | DEAD-OR-FROZEN | ARCHIVE | no |
| astro-aski | Astro/render front-end built on aski_rs codegen | 2026-05-30 (add render sources) | DEAD-OR-FROZEN | ARCHIVE | no |
| vscode-aski | VS Code extension: aski tree-sitter grammar + highlights | 2026-04-16 | DEAD-OR-FROZEN | ARCHIVE | no |
| corec | Core Compiler — `.core` → Rust + rkyv derives; bootstrap seed for *-core crates | 2026-04-20 | DEAD-OR-FROZEN | ARCHIVE | no |
| synth-core | Grammar rkyv contract (askicc↔askic) | 2026-04-20 | DEAD-OR-FROZEN | ARCHIVE | no |
| veric | The Aski Verifier+Linker (per-module rkyv → program.rkyv); src culled, awaiting rewrite | 2026-04-20 | DEAD-OR-FROZEN | ARCHIVE | no |
| veri-core | Verified-program rkyv contract (veric↔semac) | 2026-04-20 | DEAD-OR-FROZEN | ARCHIVE | no |
| semac | The Sema Compiler — rkyv parse trees → sema binary + Rust | 2026-05-24 (add v0.1 concept schema) | DEAD-OR-FROZEN | ASK-PSYCHE | no |
| domainc | Per-program domain-type generator (proc macro over program.rkyv) | 2026-04-19 (STALE marker) | DEAD-OR-FROZEN | ARCHIVE | no |
| noesis | LLM binary-communication layer (rkyv sema types on wire); reset toward aski-native | 2026-04-06 | DEAD-OR-FROZEN | ASK-PSYCHE | no |
| noesis-schema | Cozo schema seeds (field_type graph, world init/seed) for noesis | 2026-03-24 | DEAD-OR-FROZEN | ARCHIVE | no |
| nexus | Typed semantic NOTA text vocabulary + translator daemon (nexus-daemon) | 2026-06-08 (migrate to nota-next) | CORE-PERSONA | KEEP-ACTIVE | yes |
| nexus-cli | Thin text client for the nexus daemon (binary `nexus`); reference client | 2026-06-05 | CORE-PERSONA | KEEP-ACTIVE | yes |
| nexus-spec-archive | Archived earlier nexus grammar spec ("criomed" request language, nota-serde-core) | 2026-05-30 | ARCHIVE | ARCHIVE | no |
| mentci-lib | Heavy application-logic library for the mentci interaction surface | 2026-06-05 | CORE-PERSONA | KEEP-ACTIVE | yes |
| mentci-egui | First mentci surface — egui introspection workbench atop mentci-lib | 2026-05-14 | CORE-PERSONA | KEEP-ACTIVE | no |
| mentci-tools | Nix package set (annas, beads, dolt, substack, cli, linkup) — workspace tooling | 2026-04-27 | PERSONA-ADJACENT-TOOLING | KEEP-ADJACENT | no |
| clavifaber | CriomOS host key-material provisioning tool (NOTA request/response CLI) | 2026-06-08 (migrate to nota-next) | PERSONA-ADJACENT-TOOLING | KEEP-ACTIVE | yes |
| kameo | Vendored fork of the Kameo Rust actor framework (origin=LiGoldragon/kameo) | 2026-05-13 (dep bump #327) | PERSONA-ADJACENT-TOOLING | KEEP-ADJACENT | no |
| kameo-testing | Kameo 0.20 testing bed — falsifiable source for primary/skills/kameo.md | 2026-05-14 | PERSONA-ADJACENT-TOOLING | KEEP-ADJACENT | no |
| kameo-testing-assistant | Designer-assistant Kameo fit experiments (actor discipline) | 2026-05-30 | EXPERIMENT-OR-SPIKE | KEEP-ADJACENT | no |
| hexis | Managed-mutable config reconciliation, per-key modes | 2026-05-13 (migrate to Kameo) | PERSONA-ADJACENT-TOOLING | KEEP-ADJACENT | no |
| arbor | Content-addressed prolly trees for sema versioning (rkyv + blake3) | 2026-04-10 | PERSONA-ADJACENT-TOOLING | ASK-PSYCHE | no |
| arca | Content-addressed filesystem (blake3, redb index) — nix-store analogue | 2026-05-30 (refresh arch) | PERSONA-ADJACENT-TOOLING | KEEP-ADJACENT | no |
| library | Sema-ecosystem scholarly book repo (Anna's-Archive-indexed corpus) | 2026-06-05 | PERSONA-ADJACENT-TOOLING | KEEP-ADJACENT | no |
| substack-cli | CLI to publish/manage Substack posts | 2026-05-01 | SEPARATE-PROJECT | KEEP-ADJACENT | no |
| annas-mcp | Anna's Archive MCP server + CLI (upstream third-party tool) | 2026-02-22 | SEPARATE-PROJECT | KEEP-ADJACENT | no |
| whisrs | Speech-to-text "speak. type. done." utility | 2026-05-11 | SEPARATE-PROJECT | KEEP-ADJACENT | no |
| maisiliym | Nix NodeProposal for the Maisiliym cluster (CriomOS hardware coordination) | 2026-04-18 | PERSONA-ADJACENT-TOOLING | KEEP-ADJACENT | no |
| brightness-ctl | Laptop backlight + idle-dim daemon (Nix flake) | 2026-05-09 | SEPARATE-PROJECT | KEEP-ADJACENT | no |
| kibord | Ergodone/keyboard keymap backups | 2026-05-30 | SEPARATE-PROJECT | KEEP-ADJACENT | no |
| qmkBinaries | Prebuilt QMK firmware binaries (minidox) | 2026-05-30 | SEPARATE-PROJECT | KEEP-ADJACENT | no |
| ndi | NDI SDK v5 Linux installer wrapper | 2023-02-13 | SEPARATE-PROJECT | ARCHIVE | no |
| atom | Decentralized source-archive format (Ekala ecosystem) — early-dev, third-party | 2024-12-22 | SEPARATE-PROJECT | ASK-PSYCHE | no |
| awesome | Olivier Francoeur's "awesome" list (third-party content) | 2025-02-07 | SEPARATE-PROJECT | ARCHIVE | no |
| Armbian-RockPi4B-NixOS | Armbian → NixOS bootstrap scripts for RockPi 4B | 2026-01-21 | SEPARATE-PROJECT | KEEP-ADJACENT | no |
| pi-delegate | Node/TS tool: delegate tasks to Claude/Gemini/Codex/Pi via their CLIs | 2026-04-03 | PERSONA-ADJACENT-TOOLING | ASK-PSYCHE | no |
| persona-pi | Nix-packaged Pi harness — agent-harness backend wiring upstream pi into Persona | 2026-05-24 | CORE-PERSONA | KEEP-ACTIVE | no |
| test-city | Sandbox to reproduce Gas City / Criopolis bugs in isolation | 2026-05-06 | EXPERIMENT-OR-SPIKE | ASK-PSYCHE | no |
| workspace | Meta-repo / meta-deploy aggregator for the criome sema-ecosystem (older `workspace`) | 2026-05-02 | PERSONA-ADJACENT-TOOLING | ASK-PSYCHE | no |
| prism | (no directory under LiGoldragon/) | MISSING | UNKNOWN | ASK-PSYCHE | n/a |

## Notes by family

### The aski cluster — frozen older compiler/language project (ARCHIVE)
`aski` carries an explicit psyche-authored retirement banner (2026-04-21:
"aski is dead… it was the wrong way"). Its CLAUDE.md forbids reasoning from
aski axioms into the current sema architecture and calls any nexus overlap
"coincidence not lineage." The whole pipeline hangs off it: `askicc`
(synth→dsls.rkyv) → `askic` (compiler) → `veric`/`veri-core` (verify+link)
→ `semac` (sema compiler) → `domainc` (domain proc-macro), with `corec`
the bootstrap `.core`→Rust seed and `aski-core`/`synth-core` the rkyv
contract crates. `aski-cc` is the self-hosted compiler-in-aski. `veric` is
already gutted (src deleted, "full rewrite awaits"). `astro-aski` and
`vscode-aski` are aski front-ends. **All ARCHIVE.** The two later commits
(`aski-cc` and `astro-aski` on 2026-05-30) are lockfile/source refreshes,
not revival — treat as touch-ups on dead trees.

`semac` and `noesis` are marked **ASK-PSYCHE** rather than auto-ARCHIVE:
both received later schema-adding commits ("v0.1 concept schema" 2026-05-24;
noesis reset toward rkyv sema types). They may be sema-backend ideas the
psyche intends to carry forward into the live stack rather than aski legacy.
Worth one explicit confirmation before retiring. `noesis-schema` and
`domainc` are unambiguously dead aski-pipeline pieces.

### nexus — CORE-PERSONA, the live vocabulary + engine (KEEP-ACTIVE)
`nexus` (typed semantic NOTA vocabulary + translator daemon) and `nexus-cli`
(thin reference client, binary `nexus`) are current — both have proper
INTENT.md, recent nota-next migration commits (2026-06-08/05), and match
record gb87's "execution engine" framing. **KEEP-ACTIVE.**
`nexus-spec-archive` is exactly what its name says: an archived earlier
grammar spec (its ARCHITECTURE.md still describes a "criomed" request
language parsed by `nota-serde-core`). **ARCHIVE** — superseded by `nexus`.

### mentci cluster — CORE-PERSONA human surface (KEEP)
`mentci-lib` (heavy app logic, has INTENT.md) and `mentci-egui` (first egui
workbench) are the live human-facing introspection surface for criome sema.
**KEEP-ACTIVE.** `mentci-tools` is a Nix package set of workspace utilities
(annas, beads, dolt, substack, cli, linkup) — adjacent tooling, **KEEP-ADJACENT.**

### kameo — vendored actor runtime the stack depends on (KEEP-ADJACENT)
`kameo` is a fork of the upstream Kameo Rust actor framework (origin
`LiGoldragon/kameo`), the actor runtime the live stack migrated onto (see
`hexis` "migrate legacy actor runtime with Kameo"). `kameo-testing` is the
falsifiable source for `primary/skills/kameo.md`; `kameo-testing-assistant`
is a designer-assistant fit-experiment variant. All **KEEP-ADJACENT**
(`kameo-testing-assistant` is an EXPERIMENT-OR-SPIKE but still useful).

### sema-adjacent storage / config (KEEP-ADJACENT, one ASK)
`arca` (content-addressed FS, redb index) and `hexis` (managed config
reconciliation, now on Kameo) are live adjacent infra. `arbor`
(content-addressed prolly trees for sema versioning) is the same family but
last touched 2026-04-10 and its commit admits prior trait-unity drift —
**ASK-PSYCHE** whether it's still the chosen versioning substrate vs `arca`.
`library` (scholarly corpus) is active (2026-06-05). `maisiliym` is a
CriomOS cluster NodeProposal — adjacent infra.

### Pi / delegate harness surfaces (factual classification only)
`persona-pi` is the Nix-packaged Pi harness backend for the Persona engine
(ARCHITECTURE.md; **CORE-PERSONA**, KEEP-ACTIVE). `pi-delegate` is a Node/TS
multi-CLI task-delegation tool (Claude/Gemini/Codex/Pi), last touched
2026-04-03 — **ASK-PSYCHE** on whether it's still in use or superseded by
current harness orchestration. Neither inspected beyond top-level docs; no
private-repos touched.

### Misc personal / hardware / third-party tools (mostly KEEP-ADJACENT)
Genuinely separate, useful, keep where live: `whisrs` (STT), `brightness-ctl`
(backlight daemon), `kibord` + `qmkBinaries` (keyboard keymaps/firmware),
`Armbian-RockPi4B-NixOS` (board bootstrap), `substack-cli`, `annas-mcp`
(third-party MCP). `maisiliym` listed with sema infra above.

### Clearly dead / stale by age (ARCHIVE)
`ndi` (2023-02-13, SDK installer wrapper), `awesome` (2025-02-07, a
third-party awesome-list, not LiGoldragon's own work), `atom` (2024-12-22,
third-party Ekala source-archive format — ASK-PSYCHE since it's someone
else's early-dev project mirrored here). `nexus-spec-archive`,
`noesis-schema`, and the entire aski pipeline also fall here.

### test / meta
`test-city` (Gas City / Criopolis bug-repro sandbox, 2026-05-06) and
`workspace` (older meta-repo/meta-deploy aggregator for the criome
sema-ecosystem, 2026-05-02) are both **ASK-PSYCHE**: `workspace` overlaps in
purpose with the current `primary` coordination repo and may be a
predecessor; `test-city` may be live debugging infra. Confirm before
deciding.

### MISSING
`prism` — no directory exists under `/git/github.com/LiGoldragon/`. May be
under a different owner path, not yet checked out, or renamed. **ASK-PSYCHE.**

## Tally

- **KEEP (ACTIVE or ADJACENT): 23** — nexus, nexus-cli, mentci-lib,
  mentci-egui, mentci-tools, clavifaber, kameo, kameo-testing,
  kameo-testing-assistant, hexis, arca, library, persona-pi, substack-cli,
  annas-mcp, whisrs, maisiliym, brightness-ctl, kibord, qmkBinaries,
  Armbian-RockPi4B-NixOS.
  (21 listed here; mentci-egui + clavifaber make 23 — count includes both
  KEEP-ACTIVE and KEEP-ADJACENT.)
- **ARCHIVE/RETIRE: 13** — aski, askic, askicc, aski-cc, aski-core,
  astro-aski, vscode-aski, corec, synth-core, veric, veri-core, domainc,
  noesis-schema, nexus-spec-archive, ndi, awesome. (the aski pipeline +
  dead misc.)
- **ASK-PSYCHE: 8** — semac, noesis, arbor, pi-delegate, test-city,
  workspace, atom, prism(MISSING).

### INTENT.md coverage gap
Only **4 of 43** repos have an INTENT.md (`mentci-lib`, `clavifaber`,
`nexus`, `nexus-cli`) — all KEEP-ACTIVE. Per workspace discipline every live
repo needs one; the KEEP-set without INTENT.md (`mentci-egui`, `kameo*`,
`hexis`, `arca`, `library`, `persona-pi`, the personal tools) is the
backlog. Archived repos don't need one.
