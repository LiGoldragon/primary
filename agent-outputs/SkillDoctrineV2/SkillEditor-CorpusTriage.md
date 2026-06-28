# Skill Doctrine V2 Corpus Triage

## Task and Scope

Read-only Skill Editor triage for SkillDoctrineV2. No skill source, manifest,
generator, commit, or push changes were made. The question was which active and
archived skills should be kept, merged, slimmed, archived, or eliminated under
settled V2 intent:

- `skills.nota` is dead as runtime discovery.
- V2 worker role packets should be self-contained enough for normal role work by
  bundling curated critical doctrine modules.
- Skills should be terse, self-contained information packets.
- Skills should not require brittle links or implementation files as required
  reading.
- A skill is justified by preventing real workspace errors, not by existing.

## Files and Commands Consulted

- `/git/github.com/LiGoldragon/skills/manifests/active-outputs.nota`
- `/git/github.com/LiGoldragon/skills/manifests/module-dependencies.nota`
- `/git/github.com/LiGoldragon/skills/manifests/skills-roster.nota`
- `/git/github.com/LiGoldragon/skills/modules/*/full.md`
- `/git/github.com/LiGoldragon/skills/roles/*/full.md`
- `/git/github.com/LiGoldragon/skills/skills/archive/*.md`
- Commands: `sed`, `find`, `wc -w`, `rg`, heading scans over active modules and
  archive files.

## Observed Corpus Facts

- Active generated output manifest lists 63 active first-class skills and 10
  active role packets.
- `module-dependencies.nota` has every dependency edge empty, including role
  packets. V2 self-contained role bundles need new dependency data rather than
  preserving V1 graph behavior.
- The active source corpus is about 109k words.
- Largest active modules by word count: `component-triad` 8483, `reporting`
  6099, `prose` 4426, `kameo` 4167, `contract-repo` 4129, `actor-systems`
  4094, `architectural-truth-tests` 3446, `nota-design` 3230, `jj` 3045,
  `intent-log` 3001.
- Direct stale `skills.nota` references appear in `nota-design`,
  `nota-schema-docs`, `helper-context-transfer`, and current `skill-editor`
  guidance outside this repo. The manifest comments also still describe V1.
- Archive contains old role skills: `operator`, `designer`, `schema-designer`,
  `system-operator`, `system-maintainer`, `poet`, `editor`, `assistant`,
  `counselor`. They are NoEmission in `skills-roster.nota`.
- Several active modules still teach report/lane-era mechanics as first-class
  doctrine: `reporting`, `report-naming`, `context-maintenance`,
  `context-maintenance-deep`, `workspace-update-report`, `session-lanes`.

## Proposed Actions

### Keep

| Skills | Rationale | Confidence |
|---|---|---|
| `agent-output-protocol` | Directly matches V2 worker durable-output shape; small and self-contained. | High |
| `secrets`, `privacy` | Prevent high-cost leaks; workspace-specific private/public boundary. Keep separate but bundle together in roles touching secrets/private scopes. | High |
| `naming`, `abstractions`, `beauty`, `typed-records-over-flags`, `enum-contact-points`, `push-not-pull` | Compact core craft doctrine that prevents recurrent LLM code/design errors. Some can be bundled, but each rule is distinct. | High |
| `language-design`, `structural-forms` | Unique workspace doctrine for typed data, NOTA-shaped language design, and structural macros. Slim citations, keep doctrine. | High |
| `micro-components`, `library`, `repository-management`, `versioning` | Short, specific operational rules with real error-prevention value. Keep with minor pruning. | Medium-High |
| `secrets`, `nix-usage`, `nix-discipline`, `testing`, `jj` | Necessary safety/verification/mechanics doctrine. Merge/bundle where roles need self-contained packets, but preserve content. | High |
| `intent-clarification`, `intent-maintenance`, `repo-intent`, `intent-manifestation`, `spirit-cli` | Still load-bearing for intent workflows, but should be assigned mainly to lead/intent-maintainer packets, not all workers. | Medium |
| `mermaid`, `nota-schema-docs`, `nota-comments`, `stt-interpreter`, `context-handover`, `keep-working`, `main-feature-integration` | Small mechanism packets; keep only if triggered by exact mechanism or included in a role bundle that actually uses them. | Medium |

### Merge

| Skills | Proposed merge target | Rationale | Confidence |
|---|---|---|---|
| `rust-discipline`, `rust-methods`, `rust-errors`, `rust-parsers`, `rust-crate-layout` | `rust-core` or Rust worker bundle | `rust-discipline` is an index, which conflicts with self-contained V2 packets. Rust workers need the core rules together. | High |
| `rust-storage-and-wire`, relevant `contract-repo` excerpts | `rust-wire-storage` or component bundle | Storage/wire rules are often needed with contract work; avoid brittle "go read X" chains. | Medium |
| `nix-discipline`, `nix-usage`, Nix parts of `testing` | `nix-core` role bundle | Nix auditor/implementer packets need command discipline and authoring rules together. | High |
| `engine-analysis`, `engine-report` | `engine-analysis` | Report shape is subordinate to analysis; separate engine report skill is not justified. | High |
| `beads`, `bead-weaver` | `work-tracking` or lead-only bundle | Both are BEADS-specific and transitional. Split context hurts more than it helps. | Medium |
| `main-next`, `feature-development`, `double-implementation-strategy`, `main-feature-integration` | `code-repo-branching` | Same code-repo branch/integration doctrine spread across four small modules. Keep primary-vs-code-repo warnings prominent. | High |
| `human-interaction`, `intent-led-orchestration`, `when-to-use-helpers`, `helper-context-transfer`, lead parts of `autonomous-agent` | `lead-orchestration` | These are lead/human-boundary doctrine, not ordinary worker doctrine. Current split causes role/lead authority to bleed into workers. | High |
| `reporting`, `report-naming`, `workspace-update-report`, parts of `context-handover` | `durable-output-and-reports` | V2 should foreground agent outputs; report-era mechanics should be a smaller explicit report mechanism, not keystroke doctrine. | High |
| `nota-design`, `nota-schema-docs`, `structural-forms`, selected `language-design` | `nota-and-schema-design` role bundle | Schema workers need these together. First-class modules can remain separate only if self-contained and purged of `skills.nota` examples. | Medium |

### Slim

| Skills | Rationale | Confidence |
|---|---|---|
| `component-triad` | Keep unique component/Signal/Nexus/SEMA doctrine, but split or compress repo triad, runtime triad, binary naming, trace/config/help operations, and current spirit/meta-signal case study. Remove intent IDs, implementation-file references, stale current-state digressions, and long worked examples from required reading. | High |
| `reporting` | Reframe around V2 agent outputs and explicit report triggers. Remove broad report taxonomy, YAML/header details, numbering, lane directory mechanics, report-retirement process, and context-maintenance material into a report-system appendix or archive. | High |
| `prose` | Keep only operational prose criteria for roles that write prose. Remove or move long reference shelf, many examples, and TheBookOfSol-specific register unless bundled only for poet/editor. | High |
| `kameo` | Keep Kameo 0.20 traps, actor shape, lifecycle, supervision, mailbox, ask/tell, and blocking templates. Compress API tables and examples; merge conceptual actor content with `actor-systems` or make dependency explicit in role bundle. | High |
| `contract-repo` | Keep contract ownership, versioning, operation verb layering, rkyv/NOTA round-trip discipline. Compress naming catalogue, layered-pattern exposition, repo-name taxonomy, and examples. Remove required `signal` repo architecture read. | High |
| `actor-systems` | Keep actor-density, data-bearing actors, no blocking, no shared locks, supervision, traces, test witnesses. Remove duplicate Kameo sections and fold runtime-triad specifics into component bundle. | High |
| `architectural-truth-tests` | Keep proof-of-usage ladder and witness catalogue. Slim long worked examples and merge runner details into `testing`. | Medium-High |
| `nota-design` | Remove `skills.nota` as canonical example; replace with a V2-neutral NOTA example owned by this repo. Compress grammar facts into a self-contained packet. | High |
| `intent-log`, `spirit-cli` | Keep for intent-maintainer/lead, but reduce implementation-command detail in general packets. Worker roles should not load these unless they capture/maintain intent. | Medium |
| `jj` | Keep safety rules, inline messages, whole-working-copy commits, push recovery. Slim old lane/report references and any primary-only material not relevant to code-repo workers. | Medium |
| `architecture-editor`, `repo-intent`, `workspace-vocabulary` | Keep, but remove report-era cross-talk and "remaining work" style sections. Treat them as durable-guidance editors, not runtime discovery aids. | Medium |

### Archive

| Skills | Rationale | Confidence |
|---|---|---|
| `session-lanes` | V2 role packets and `agent-outputs` reduce the old session-lane/report-directory model. Keep only if the psyche confirms lanes still exist as runtime identity outside V2 workers. | Medium |
| `context-maintenance`, `context-maintenance-deep` | Heavy report/lane garbage-collection doctrine, not ordinary worker doctrine. Archive or lead-only after extracting any still-current "migrate durable substance" rule. | High |
| `workspace-update-report` | Report-era synthesis mechanism. Keep archived or explicit-ask-only; not an active worker skill. | Medium-High |
| `beads`, `bead-weaver` | Transitional by their own description. Keep temporarily only while BEADS remains live; archive when Persona/mind tracking is available. | Medium |
| `engine-report` | Merge useful section list into `engine-analysis`; archive standalone report skill. | High |
| Archived `designer`, `operator`, `schema-designer` | Superseded by V2 role modules and curated dependencies. Archive remains useful only as extraction source; do not emit. | High |
| Archived `poet`, `editor` | Keep archived unless V2 restores those roles. Extract unique prose/source-evidence doctrine into role packets if needed. | Medium |
| Archived `assistant`, `counselor` | Keep archived and private-scope-aware; do not emit into public worker packets without explicit psyche decision about personal-affairs roles. | Medium |

### Eliminate

| Skills | Rationale | Confidence |
|---|---|---|
| `rust-discipline` as first-class index | V2 packets should be self-contained; an index that exists mainly to point at subfiles is obsolete. Merge its one-sentence rules into Rust bundles, then remove first-class output. | High |
| `helper-context-transfer` as standalone | Content belongs in lead orchestration. Standalone trigger encourages brittle required-reading envelopes. | High |
| `when-to-use-helpers` as standalone | Same lead-only doctrine as `helper-context-transfer`; merge into `lead-orchestration`. | High |
| `report-naming` as standalone | Useful only inside a report mechanism; merge into slimmed reporting or archive. | High |
| `main-feature-integration` as standalone | Too small and inseparable from code-repo branch integration doctrine; merge into `code-repo-branching`. | High |
| Archived role files after extraction | Once unique doctrine is either discarded or moved into V2 role/source modules, old role skills have no owner or trigger. Delete in a later cleanup if psyche accepts. | Medium |

## Top 10 Highest-Impact Targets

1. `component-triad`: split/slim from 8483 words into component-core plus optional runtime-triad detail; remove current-state case studies and intent IDs.
2. `reporting`: rewrite for V2 agent-output-first behavior; demote report/lane taxonomy.
3. `rust-discipline` plus Rust subskills: replace index with self-contained Rust role bundle.
4. `human-interaction` + orchestration/helper modules: merge into lead-only packet; keep out of normal worker packets.
5. `kameo` + `actor-systems`: merge or strongly bundle; remove duplicated conceptual/API teaching.
6. `contract-repo`: compress to contract ownership and wire-shape rules; remove external required readings.
7. `context-maintenance` + `context-maintenance-deep`: archive or lead-only; they are report-era lane cleanup, not V2 worker doctrine.
8. `nota-design`: replace `skills.nota` canonical examples and remove runtime-discovery references.
9. `prose`: slim for poet/editor only; avoid broad first-class loading for ordinary workers.
10. Archived `system-operator` / `system-maintainer`: extract unique CriomOS live-host doctrine into `criomos-implementer` dependencies, then keep old files archived or delete.

## Generated Role Assignment Implications

- `role-scout`: include `agent-output-protocol`, `privacy`, `secrets` when scope can expose private/secret material, and a tiny read-only inspection protocol. Do not include lead orchestration or report-lane doctrine.
- `role-general-code-implementer`: include `agent-output-protocol`, `naming`, `abstractions`, `beauty`, `testing`, `versioning`, and language-specific bundles by task. Rust tasks should get `rust-core`; actor tasks should get `actor-runtime`; wire tasks should get `contract-component`.
- `role-criomos-implementer`: include `nix-core`, `secrets`, `privacy`, `versioning`, `repository-management` as needed, plus extracted live-host safety from archived `system-operator`/`system-maintainer`.
- `role-rust-auditor`: include `rust-core`, `architectural-truth-tests`, `testing`, `naming`, `abstractions`, `enum-contact-points`, and `typed-records-over-flags`; add `actor-runtime` or `contract-component` only when changed surface requires.
- `role-nix-auditor`: include `nix-core`, `testing`, `secrets`, and `versioning`; no broad code or report doctrine by default.
- `role-skill-editor`: include `skill-editor`, `agent-output-protocol`, manifest/index rules, and the V2 rule that `skills.nota` is not runtime discovery. Do not require broad `reporting`.
- `role-intent-maintainer`: include `intent-core` (`intent-log`, `spirit-cli`, `intent-maintenance`, `intent-manifestation`, `intent-clarification`, `repo-intent`) plus privacy/secrets.
- `role-intent-translator`: include `agent-output-protocol`, slim `lead-orchestration` outputs relevant to translating, and optional `beads/work-tracking` only when tracked implementation is requested.
- `role-repo-operator`: include `jj`, `repository-management`, `testing` evidence expectations, `versioning`, `agent-output-protocol`, and repo-specific branch bundle for code repos.
- `role-repo-scaffolder`: include `repository-management`, `micro-components`, `architecture-editor`, `repo-intent`, `naming`, and language/build bundles by scaffold type.

Composite modules likely needed for V2:

- `worker-output-core`: `agent-output-protocol` plus concise chat/locator rules.
- `rust-core`: methods-on-types, typed errors, parser discipline, crate layout, naming.
- `actor-runtime`: actor systems plus Kameo-specific traps.
- `contract-component`: component triad core, contract repo core, subscription lifecycle, wire/storage excerpts.
- `nix-core`: Nix authoring, command use, checks, store-path hygiene.
- `intent-core`: Spirit capture/maintenance/manifestation/clarification.
- `lead-orchestration`: human boundary, helper dispatch, alignment, intent-led orchestration.
- `code-repo-branching`: `main`/`next`, feature branches, double implementation, integration.

## Decisions That Must Go Back to Psyche

- Whether session lanes remain active runtime identity under V2 or should be
  archived entirely in favor of role packets plus `agent-outputs`.
- Whether BEADS remains a required work-tracking substrate during V2, or should
  be archived now as transitional debt.
- Whether poet/editor/assistant/counselor roles should return as V2 role packets
  or remain archived/private/manual.
- Whether old archived role files should be deleted after extraction, or kept as
  historical NoEmission sources.
- Whether component-triad should stay one first-class doctrine packet or split
  into separate component packaging, runtime triad, and signal-contract packets.
- Whether active first-class surfaces should emit individual atomic skills at
  all, or whether V2 should emit only curated role bundles plus optional
  mechanism modules.

## Verification and Blockers

- Verified required paths exist and archive is `skills/archive`.
- Verified active manifest and dependency index are readable.
- Verified module size and stale-reference patterns with scoped shell scans.
- No generator/parser checks were run because this was read-only triage and no
  source files were edited.
- This triage is a recommendation set, not settled doctrine. Psyche decisions
  above should be resolved before turning archive/delete recommendations into
  manifest changes.
