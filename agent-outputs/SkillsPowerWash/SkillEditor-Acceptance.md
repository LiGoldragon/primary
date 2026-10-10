# SkillEditor Acceptance

## Task and scope

Power-washed the canonical LiGoldragon/skills source repo source-first, removed explicitly deprecated skills, reconciled generated runtime surfaces in primary, validated, committed, and pushed. Also created the requested follow-up bead for speech-to-text vocabulary/tool work.

## Source truth consulted

- `/git/github.com/LiGoldragon/skills/AGENTS.md`
- `/git/github.com/LiGoldragon/skills/skills.md`
- `/git/github.com/LiGoldragon/skills/manifests/active-outputs.nota`
- `/git/github.com/LiGoldragon/skills/manifests/module-dependencies.nota`
- `/git/github.com/LiGoldragon/skills/manifests/skills-roster.nota`
- `/git/github.com/LiGoldragon/tree-sitter-nota/grammar.js` for raw NOTA grammar facts: atoms, parenthesized/vector/map forms, pipe forms, pipe text, and `;;` comments.
- `/git/github.com/LiGoldragon/nota-next/ARCHITECTURE.md` and tests for codec/schema-layer facts: schema assigns meaning, records are positional, structs/enums/codecs own typed shape.

## Removed skills

Fully removed from source modules, active manifest, dependency index/role deps where applicable, compatibility roster, and generated runtime surfaces:

- `report-naming`
- `stt-interpreter`
- `main-next`
- `double-implementation-strategy`
- `subscription-lifecycle`
- `when-to-use-helpers`
- `worker-output-core` (dependency module, not active first-class skill)
- `workspace-context-core` (dependency module, not active first-class skill)
- `workspace-vocabulary`
- `safety-core` (dependency module, not active first-class skill)
- `autonomous-agent`
- `rust-parsers` (removed after folding parser discipline into Rust core/discipline)

No disabled source stubs were kept.

## Explicit named outcomes

- `intent-led-orchestration`: rewritten to positively state that the orchestrator always dispatches spawned agents for any task/action, even when psyche wording sounds like direct action. It now says the orchestrator interviews, gates, dispatches, and synthesizes only.
- `session-lanes`: trimmed to lane/discipline identity, registration, lifecycle, and drain routing. Report-directory/report-system discussion removed.
- `context-maintenance`: trimmed to current artifact-disposition discipline and durable-home routing; report-centric flow removed.
- `nix-usage`: shortened to Nix command evidence, daemon-visible settings, remote-builder probe, and store-path hygiene. Jujutsu/version-control steps, hostnames, and host-specific facts removed.
- `secrets`: shortened to transient secret handling, blind piping, secret-store/deployment-ciphertext split, and verification without printing values.
- `rust-storage-and-wire`: trimmed to stable typed-boundary rules: typed stores, typed Rust-to-Rust wire contracts, NOTA as human projection, schema/version upgrade discipline. Removed obsolete/current-status/project-specific claims.
- `rust-parsers`: removed; essential parser rule now lives in `rust-core`/`rust-discipline` as “use NOTA codec for NOTA and established parser libraries for structured/external input.”
- NOTA/notice: `nota-design` stayed and was updated from raw grammar/codec source truth; `nota-schema-docs` stayed as compact pseudo-NOTA documentation convention; `nota-comments` stayed as compact `(Why ...)` rationale-comment discipline. No standalone notice skill was found; generated-file notice checks remain in skill-editor/skill-source-core verification guidance.

## Other notable pruned/kept skills

- `intent-log`, `intent-maintenance`, `intent-manifestation`, `spirit-cli`: drastically shortened; kept because Spirit intent operation remains their subject.
- `engine-analysis`, `engine-report`: shortened; `engine-report` kept because its whole subject remains an engine report artifact.
- `library`: kept as source-backed research discipline; local paths/tool specifics removed.
- `micro-components`: kept as one-capability component boundary discipline; URL/path examples removed.
- `repository-management`: kept as minimal ghq/gh discipline; local filesystem layout and URL doctrine removed.
- `feature-development`: kept as branch/worktree discipline; local paths/report boilerplate removed.
- `privacy`: kept as privacy boundary; private paths/report-system detail removed.
- `bead-weaver`: kept as BEADS dependency-graph discipline; report template and boilerplate removed.
- `beauty`, `typed-records-over-flags`, `push-not-pull`, `rust-crate-layout`, `rust-errors`, `intent-clarification`: See Also sections and stale/report references pruned where feasible.
- `reporting`: kept only because its subject is still explicitly reports; remains a later psyche-decision candidate as reports phase out.

## Speech-to-text bead

Created bead `primary-9s3j` in primary:

Title: `Teach speech-to-text tool workspace vocabulary`

Purpose: fix the speech-to-text tool/model vocabulary and context so it transcribes workspace terms directly instead of relying on an agent-side guessing skill. Acceptance requires tool/model vocabulary/context support or a documented blocker and representative transcription witnesses.

## Changed files by repo

### LiGoldragon/skills

- Manifests: `manifests/active-outputs.nota`, `manifests/module-dependencies.nota`, `manifests/skills-roster.nota`.
- Tests: `tests/generation.rs` updated for active skill count and role dependency changes.
- Removed module files: the fully removed skills listed above.
- Pruned module files: `modules/bead-weaver/full.md`, `modules/beauty/full.md`, `modules/context-maintenance/full.md`, `modules/context-maintenance-deep/full.md`, `modules/engine-analysis/full.md`, `modules/engine-report/full.md`, `modules/feature-development/full.md`, `modules/helper-context-transfer/full.md`, `modules/intent-clarification/full.md`, `modules/intent-led-orchestration/full.md`, `modules/intent-log/full.md`, `modules/intent-maintenance/full.md`, `modules/intent-manifestation/full.md`, `modules/keep-working/full.md`, `modules/library/full.md`, `modules/micro-components/full.md`, `modules/nix-usage/full.md`, `modules/nota-comments/full.md`, `modules/nota-design/full.md`, `modules/nota-schema-docs/full.md`, `modules/privacy/full.md`, `modules/push-not-pull/full.md`, `modules/repo-intent/full.md`, `modules/repo-operation-core/full.md`, `modules/repo-scaffold-core/full.md`, `modules/repository-management/full.md`, `modules/rust-crate-layout/full.md`, `modules/rust-discipline/full.md`, `modules/rust-errors/full.md`, `modules/rust-storage-and-wire/full.md`, `modules/secrets/full.md`, `modules/session-lanes/full.md`, `modules/spirit-cli/full.md`, `modules/typed-records-over-flags/full.md`, `modules/versioning/full.md`.
- Role source files pruned: `roles/intent-maintainer/full.md`, `roles/nix-auditor/full.md`, `roles/repo-operator/full.md`, `roles/rust-auditor/full.md`, `roles/scout/full.md`.

### primary

- Generated skill surfaces under `.agents/skills/*/SKILL.md` and `.claude/skills/*/SKILL.md` were regenerated; removed skill directories were pruned.
- Generated role surfaces under `.claude/agents/*.md`, `.codex/agents/*.toml`, and `.pi/agents/*.md` were regenerated for role dependency changes.
- `skills/generated-role-outputs.nota` was reconciled by the generator.
- Bead `primary-9s3j` was created through `bd`; the `.beads` backing store is not shown in `jj status`.

## Commits and push status

- LiGoldragon/skills: `6b8cf0d6a62c` — `skills: power-wash doctrine corpus`; pushed, `main@origin` matches `main`.
- primary: `483c30eccf5b` — `skills: reconcile power-washed runtime surfaces`; pushed, `main@origin` matches `main`.

## Validation commands and results

- `cargo test` in LiGoldragon/skills: first run failed after count changes (`roster_model_covers_current_skills_without_entrypoint_extras` and `active_manifest_and_module_index_cover_current_skills_and_roles` expected counts too low); updated expected active/roster counts.
- `cargo test` in LiGoldragon/skills after fixes: passed, 16 integration tests passed plus doc tests.
- `nix flake check` in LiGoldragon/skills: first run failed `fmt` because `tests/generation.rs` needed `cargo fmt`; ran `cargo fmt`.
- `nix flake check` in LiGoldragon/skills after formatting/final source edits: passed all checks for x86_64-linux.
- `nix run .#generate-skills -- /home/li/primary`: passed and regenerated primary `.agents`, `.claude`, `.codex`, `.pi`, and generated role inventory surfaces.
- `nix run .#check-skills -- /home/li/primary`: passed; generated outputs match source.
- Source validation script: passed; manifest/index paths resolve and changed headings are unique.
- Source scan: passed for no `## See also`, no local path/URL patterns, no removed skill references, and no source frontmatter delimiter lines in modules/roles.
- Generated scan: passed for no `## See also`, no local path/URL patterns, no generated-file notices, no removed skill references, no commit-hash/template-label hits.
- Generated report/Spirit scan: nonzero by design/residual; report refs remain in `reporting`, `engine-report`, and role/module output protocol wording; Spirit refs remain in intent/Spirit subject surfaces.
- Generated temporal scan: only residual hits were `roadmap` in `prose` and “not yet done” in `beauty`, both non-roadmap rule prose.

## Residual risks and follow-up

- `reporting` and `engine-report` remain active because their subject is reports; psyche should decide whether to remove them as report deprecation continues.
- Role packets still include the shared agent-output protocol, which uses output-file/report-adjacent language; later cleanup can rename that doctrine toward artifacts if desired.
- Spirit/intent skills were shortened aggressively without re-validating against the deployed Spirit binary; exact CLI wire shape remains delegated to `spirit-cli` and should be source-truth reviewed before high-risk intent maintenance.
- Several remaining craft skills are still larger than the new desired floor (`beauty`, `push-not-pull`, `typed-records-over-flags`, `rust-crate-layout`, `jj`, `main-feature-integration`) and are good next psyche-decision candidates.
- Primary working copy still has unrelated pre-existing uncommitted agent-output files; they were not committed.

## Review findings

No blockers found. The only residual issues are the follow-up risks above.
