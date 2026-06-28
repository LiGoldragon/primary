# Auditor Report

Task: independently audit role packet generator and doctrine for AgentProtocolDesign, bead `primary-y0h6.8`.

## Recommendation

Approve with follow-up.

The current generator, manifests, generated role files, and doctrine satisfy the V1 intent well enough to hand to Repo Operator, with two non-blocking engineering follow-ups and live-runtime discovery still unproven for Codex/Pi.

## Findings

### Medium: module dependency cycles are not rejected with a typed error

`ModuleIndex::append_with_dependencies` recursively expands dependency edges and only marks a module as resolved after all of its dependencies return. There is no `visiting` set or equivalent cycle detection, so a cycle in `module-dependencies.nota` would recurse until stack overflow instead of returning a useful generator error.

Evidence:

- `/git/github.com/LiGoldragon/skills/src/assembly.rs:532` starts recursive expansion.
- `/git/github.com/LiGoldragon/skills/src/assembly.rs:541` loads the dependency record.
- `/git/github.com/LiGoldragon/skills/src/assembly.rs:542` recurses into each dependency before inserting the current module at `/git/github.com/LiGoldragon/skills/src/assembly.rs:545`.
- Tests cover acyclic ordering and duplicate/missing modules indirectly, but not cycles: `/git/github.com/LiGoldragon/skills/tests/generation.rs:206`.

This is not blocking for the current manifest because the active `module-dependencies.nota` has no dependency edges except role includes modeled in the active manifest, but the generator now owns a graph-shaped input and should fail cycles deliberately.

### Low: duplicate output paths are not validated before write/check

Active outputs and target-surface vectors can produce the same output path more than once, but generation collects jobs and writes/checks them without first asserting path uniqueness. A duplicate `Role` output id, duplicate `Skill` output id, or repeated target surface could make one job silently overwrite another in write mode or make check mode depend on job order.

Evidence:

- Job construction appends all skill jobs, role jobs, and the inventory job without a duplicate-output check: `/git/github.com/LiGoldragon/skills/src/assembly.rs:252`.
- Writes happen per rendered output path: `/git/github.com/LiGoldragon/skills/src/assembly.rs:999`.
- The module index already rejects duplicate module ids at `/git/github.com/LiGoldragon/skills/src/assembly.rs:507`, but there is no corresponding output-path guard.
- Current manifest paths are unique in practice: `/git/github.com/LiGoldragon/skills/manifests/active-outputs.nota:75` through `/git/github.com/LiGoldragon/skills/manifests/active-outputs.nota:84`.

This is also not blocking for the present generated state, but it is a reasonable V1 hardening test.

## Open Questions

- Codex role discovery is source-evidenced, not live-spawn evidenced. Generated files exist at `.codex/agents/<role>.toml`, and the TOML parses, but no local command proved a spawned Codex role can be listed or selected.
- Pi role discovery is package/source-evidenced, not live-subagent evidenced. Generated files exist at `.pi/agents/<role>.md`, and `pi-subagents` is active according to prior evidence, but no interactive subagent list was captured.
- The manifest/index split is workable but should stay explicit: role packet assembly includes `agent-output-protocol` through active `Role` includes in `/git/github.com/LiGoldragon/skills/manifests/active-outputs.nota:75`, while `/git/github.com/LiGoldragon/skills/manifests/module-dependencies.nota:73` keeps role source dependency vectors empty. That is acceptable if "included module" is intentionally distinct from "module dependency"; otherwise it is an ownership ambiguity to resolve before more shared role modules appear.

## Evidence Reviewed

- Translator, Scout, Skill Editor, Implementer, harness-output, doctrine, and validation reports under `/home/li/primary/agent-outputs/AgentProtocolDesign/`.
- Repo instructions: `/home/li/primary/AGENTS.md`, `/git/github.com/LiGoldragon/skills/AGENTS.md`, `/git/github.com/LiGoldragon/skills/INTENT.md`, and `/git/github.com/LiGoldragon/skills/skills.md`.
- Generator code: `src/assembly.rs`, `src/markdown.rs`, `src/error.rs`, `src/workspace_path.rs`, `schema/assembly.schema`, and `tests/generation.rs`.
- Source data: `manifests/active-outputs.nota`, `manifests/module-dependencies.nota`, role source markdown, and `modules/agent-output-protocol/full.md`.
- Generated primary outputs: `.claude/agents/*.md`, `.codex/agents/*.toml`, `.pi/agents/*.md`, `.agents/skills/*/SKILL.md`, `.claude/skills/*/SKILL.md`, `skills/skills.nota`, and `skills/generated-role-outputs.nota`.

## Checks Run

- `cargo test` in `/git/github.com/LiGoldragon/skills`: passed; 12 integration tests passed.
- `cargo clippy --all-targets -- -D warnings` in `/git/github.com/LiGoldragon/skills`: passed.
- `SKILLS_SOURCE_ROOT=$PWD SKILLS_WORKSPACE_ROOT=/home/li/primary cargo run -- skills-check.nota`: passed with no generated drift.
- `nix flake check` in `/git/github.com/LiGoldragon/skills`: passed on the dirty local checkout. Concrete Nix store paths were intentionally omitted from this report.
- Parsed all 10 generated Codex role TOML files with Python `tomllib`: passed.
- Scanned Rust production code for module-level free functions and ZST namespace structs: no production violations found.

## Positive Audit Notes

- Role output paths match Scout evidence: Claude Markdown under `.claude/agents`, Codex TOML under `.codex/agents`, and Pi Markdown under `.pi/agents`.
- Generated role inventory has 30 paths and matches the physical role files.
- Role packets are physical files, not symlinks.
- Runtime role packets contain no generated-file notice banners.
- Dependency expansion and first-position deduplication are covered for the acyclic case.
- Stale role cleanup is inventory-owned and preserves non-inventoried files in role target directories.
- Doctrine changes correctly preserve the intent-only lead, default Intent Translator handoff, distinct auditor default, evidence-backed success, psyche satisfaction authority, and provisional guideline handling.

## Provisional Observations

- Future guidance should probably require graph-shaped generator inputs to have explicit cycle tests as soon as a sidecar dependency index exists. This is a provisional engineering guideline pending psyche review.
- Future role-output manifests should probably validate unique physical output paths before rendering. This is a provisional hardening guideline pending psyche review.
