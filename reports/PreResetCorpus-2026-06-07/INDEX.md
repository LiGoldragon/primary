# Pre-Reset Corpus — 2026-06-07

## Source commit

**Commit:** `56b6411164b09db006b4b8ad6d865dc901e56866`
**Date:** 2026-06-07 16:00:18 +0200
**Commit message:** designer 553: actor-native engine rewrite — design + component-triad correction (Spirit zk6y)

This is the immediate parent of the tight-teaching rewrite commit
`027c5c1f841bd12508b0a7194730ff906b901296` (2026-06-07 16:20:24, "skills:
tight-teaching rewrite of the whole corpus (Spirit k4i3)"), which was the
first cut that reduced the corpus 36% (24,252 → 15,587 lines). The skills
lived under `skills/` in the primary repo at this time; no separate skills
repository is involved.

## Corpus totals

| Category | Files | Lines |
|---|---|---|
| skills/ | 66 | 24,397 |
| ESSENCE.md | 1 | 277 |
| reports/ | 368 | 84,636 |
| **Total** | **435** | **109,310** |

The skills line count (24,397) matches the expected stratum exactly.

## Skills file listing

| Lines | File | Description |
|---|---|---|
| 396 | skills/abstractions.md | Doctrine that behavior belongs to the type that owns it; not to callers or helpers |
| 751 | skills/actor-systems.md | Full actor-systems doctrine: kameo actors, message types, supervision, and anti-patterns |
| 691 | skills/architectural-truth-tests.md | How to verify that architecture claims are actually true in running code |
| 567 | skills/architecture-editor.md | How to read, edit, and maintain ARCHITECTURE.md files faithfully |
| 35 | skills/assistant.md | Minimal skill for the assistant role: guiding principles and tone |
| 475 | skills/autonomous-agent.md | Doctrine for fully autonomous agent operation without blocking on psyche approval |
| 421 | skills/beads.md | Work-tracking protocol: bead IDs, dispatch envelopes, progress records |
| 129 | skills/beauty.md | Treating beauty as the primary engineering criterion, not an afterthought |
| 1375 | skills/component-triad.md | Full component-triad doctrine: daemon + working signal contract + meta policy signal |
| 196 | skills/context-maintenance-deep.md | Deep context-maintenance protocol for multi-session and handover-heavy work |
| 426 | skills/context-maintenance.md | Standard context-maintenance protocol: when and how to update awareness files |
| 881 | skills/contract-repo.md | Contract repository pattern: signal crates, schema files, generation pipeline |
| 44 | skills/counselor.md | Counselor role: how to give honest counsel when asked for an opinion |
| 953 | skills/designer.md | Designer role: synthesizing psyche vision, auditing designs, leading architecture decisions |
| 131 | skills/double-implementation-strategy.md | How to build two implementations in parallel to validate design choices |
| 143 | skills/engine-analysis.md | How to audit a running engine: surface reality, not stated intent |
| 137 | skills/engine-report.md | Engine-report format: dependency snapshots, measurement defs, component ledger |
| 555 | skills/enum-contact-points.md | Doctrine for enum-driven dispatch and the contact-point pattern |
| 263 | skills/feature-development.md | Feature development workflow: branch strategy, testing, and landing |
| 153 | skills/human-interaction.md | How to interact with the psyche: pace, escalation, and honesty norms |
| 107 | skills/intent-clarification.md | When and how to surface ambiguity to the psyche before proceeding |
| 492 | skills/intent-log.md | Intent-log format and maintenance: capturing psyche rulings durably |
| 229 | skills/intent-maintenance.md | How to maintain and prune the intent log across sessions |
| 209 | skills/intent-manifestation.md | Moving from declared intent to implemented code: the manifestation protocol |
| 684 | skills/jj.md | Jujutsu (jj) version control: commands, workflow, and estate conventions |
| 1074 | skills/kameo.md | Kameo actor framework: actor definitions, message passing, supervision trees |
| 66 | skills/keep-working.md | Staying in motion: how to avoid stalling when blocked on information |
| 386 | skills/language-design.md | Design instincts for the Ethos/Nomos/Logos language family |
| 252 | skills/library.md | Research library skill: how to use the knowledge base effectively |
| 78 | skills/main-next.md | Main and next branch conventions and when to use each |
| 605 | skills/mermaid.md | Mermaid diagram syntax: workarounds, traps, and rendering quirks |
| 290 | skills/micro-components.md | Micro-component architecture: one capability, one crate, one repo |
| 513 | skills/naming.md | Naming doctrine: full English words, no redundant ancestry, no abbreviations |
| 533 | skills/nix-discipline.md | Nix discipline: flake authoring, pinning, and estate conventions |
| 124 | skills/nix-usage.md | Practical Nix usage: common commands and troubleshooting patterns |
| 284 | skills/nota-comments.md | NOTA-as-comments pattern: inline annotation without polluting source |
| 529 | skills/nota-design.md | NOTA data notation design: atoms, blocks, positional records |
| 101 | skills/nota-schema-docs.md | NOTA schema documentation conventions |
| 704 | skills/operator.md | Operator role: implementation work, landing code, and staying in scope |
| 227 | skills/poet.md | Poet role: capturing psyche voice, writing session summaries, tone |
| 128 | skills/privacy.md | Privacy doctrine: what to log, what to redact, and private-repo rules |
| 1079 | skills/prose.md | Prose style guide: sentence structure, vocabulary, and document conventions |
| 164 | skills/push-not-pull.md | Push-not-pull doctrine: daemons push events; callers do not poll |
| 228 | skills/repo-intent.md | Repository intent file format and maintenance |
| 1351 | skills/reporting.md | Full reporting doctrine: format, structure, dependency context, and anti-patterns |
| 145 | skills/report-naming.md | Report naming conventions: date suffixes, role prefixes, and directory placement |
| 239 | skills/repository-management.md | Repository management: creation, archival, and estate inventory |
| 251 | skills/role-lanes.md | Role lanes: how roles divide work and how lane boundaries are enforced |
| 151 | skills/rust-discipline.md | Rust discipline index: pointer to the rust/ subdirectory skills |
| 154 | skills/secrets.md | Secrets handling: how to pass credentials without embedding them in agent context |
| 297 | skills/skill-editor.md | Skill editor: authoring standard, what skills are and are not |
| 145 | skills/skills.nota | NOTA records file: tier and metadata declarations for all skills |
| 438 | skills/spirit-cli.md | Spirit CLI usage: recording decisions, querying intent, and Spirit record anatomy |
| 177 | skills/stt-interpreter.md | Speech-to-text interpreter role: transcription conventions and correction patterns |
| 311 | skills/subscription-lifecycle.md | Subscription lifecycle: how streaming and event-subscription protocols work |
| 324 | skills/system-operator.md | System operator role: OS-level, Nix, and CriomOS deployment work |
| 448 | skills/testing.md | Nix-backed testing doctrine: test structure, check integration, durable proofs |
| 269 | skills/typed-records-over-flags.md | Typed records over flags doctrine: why booleans are wrong for variant behavior |
| 121 | skills/versioning.md | Versioning conventions: when to bump, semver meaning in the estate |
| 194 | skills/workspace-update-report.md | Workspace update report format: what to include when closing a session |
| 230 | skills/workspace-vocabulary.md | Workspace vocabulary: canonical terms for roles, repos, and work artifacts |
| 187 | skills/rust/crate-layout.md | Rust crate layout: file and module organization conventions |
| 58 | skills/rust/errors.md | Rust errors: typed enums via thiserror; no stringly-typed errors |
| 554 | skills/rust/methods.md | Rust methods and types: method naming, receiver conventions, type design |
| 116 | skills/rust/parsers.md | Rust parsers: no hand-rolled parsing; approved parser crate list |
| 429 | skills/rust/storage-and-wire.md | Rust storage and wire: redb + rkyv patterns and estate conventions |

## ESSENCE.md

| Lines | File | Description |
|---|---|---|
| 277 | ESSENCE.md | Psyche's core self-statement: the estate's purpose, values, and guiding philosophy |

## Reports tree (368 files, 84,636 lines)

The full reports/ tree from the baseline is included verbatim. Summary by subdirectory:

| Files | Lines | Directory | Contents |
|---|---|---|---|
| 3 | 157 | reports/assistant/ | Assistant role reports |
| 86 | 19,097 | reports/cloud-designer/ | Cloud component architecture, lojix, horizon, actor-native audit reports |
| 27 | 3,073 | reports/cloud-operator/ | Cloud operator implementation reports |
| 2 | 295 | reports/cluster-operator/ | Cluster operation reports |
| 3 | 553 | reports/counselor/ | Counselor session reports |
| 31 | 6,150 | reports/designer/ | Designer-role architecture and audit reports |
| 1 | 0 | reports/nota-designer/ | Nota designer placeholder |
| 71 | 13,070 | reports/operator/ | Operator implementation reports |
| 7 | 883 | reports/pi-operator/ | Pi-operator reports |
| 2 | 64 | reports/poet/ | Poet-role session reports |
| 2 | 943 | reports/second-designer/ | Second-designer reports |
| 1 | 0 | reports/second-operator/ | Second-operator placeholder |
| 89 | 32,709 | reports/system-designer/ | System-designer deep-audit reports |
| 40 | 7,556 | reports/system-operator/ | System-operator implementation reports |
| 1 | 1 | reports/third-designer/ | Third-designer placeholder |
| 2 | 85 | reports/videographer/ | Videographer reports |

## Expected content NOT found

The following items were mentioned in the recovery brief as expected in the 2026-06-07 stratum but do not appear anywhere in this repository's git history:

- **Lore research files** — no directory or files matching "lore" exist in the repo at or before this commit. These were likely in a separate repository or in Pi conversation files outside this repo.
- **Spirit guardian prompts** — no files matching "spirit guardian" or "guardian prompt" exist. The word "guardian" appears only in deployment reports referring to a CriomOS system guardian (a NixOS service), not a skill or prompt file.

No separate skills repository is involved. At the baseline commit the entire skills corpus lived under `skills/` in this repository (`primary`). The skills directory in `.agents/skills/` and `.claude/skills/` did not exist yet at this commit; those paths appear only in later commits.
