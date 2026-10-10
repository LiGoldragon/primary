# Implementer Evidence

Task: Validate generated role outputs and cleanup behavior for AgentProtocolDesign.

BEADS: `primary-y0h6.7` - Validate generated role outputs and cleanup behavior.

## Status

Validated locally in `/git/github.com/LiGoldragon/skills` and `/home/li/primary`.

I claimed the task through orchestration as `general-code-implementer` over `(Task primary-y0h6.7)` and this evidence file. I closed the validation bead after writing this evidence, then released the orchestration claim. I made no code or generator fixes. I did not commit or push.

## Required Context Read

- `/home/li/primary/agent-outputs/AgentProtocolDesign/IntentTranslator-TranslationBrief.md`
- `/home/li/primary/agent-outputs/AgentProtocolDesign/Scout-SituationalMap.md`
- `/home/li/primary/agent-outputs/AgentProtocolDesign/Scout-HarnessAgentDiscovery.md`
- `/home/li/primary/agent-outputs/AgentProtocolDesign/SkillEditor-ManifestIndex.md`
- `/home/li/primary/agent-outputs/AgentProtocolDesign/SkillEditor-RoleSources.md`
- `/home/li/primary/agent-outputs/AgentProtocolDesign/Implementer-Generator.md`
- `/home/li/primary/agent-outputs/AgentProtocolDesign/SkillEditor-HarnessOutputs.md`
- `/home/li/primary/agent-outputs/AgentProtocolDesign/SkillEditor-OrchestrationDoctrine.md`
- `/git/github.com/LiGoldragon/skills/AGENTS.md`
- `/git/github.com/LiGoldragon/skills/INTENT.md`
- `/git/github.com/LiGoldragon/skills/skills.md`
- `/home/li/primary/INTENT.md`
- `/home/li/primary/ARCHITECTURE.md`
- `.agents/skills/beads/SKILL.md`
- `.agents/skills/jj/SKILL.md`
- `.agents/skills/repo-intent/SKILL.md`
- `.agents/skills/testing/SKILL.md`
- `.agents/skills/nix-usage/SKILL.md`

## Commands Run

In `/git/github.com/LiGoldragon/skills`:

```sh
cargo test
```

Result: passed. The integration suite reported 12 tests passing, including:

- `active_manifest_and_module_index_cover_current_skills_and_roles`
- `role_generation_expands_dependencies_in_order_and_writes_harness_paths`
- `write_mode_removes_only_inventory_owned_stale_role_outputs`

BEADS/orchestration:

```sh
orchestrate "(Claim (general-code-implementer [(Task primary-y0h6.7) (Path /home/li/primary/agent-outputs/AgentProtocolDesign/Implementer-Evidence.md)] [validate generated role outputs and cleanup behavior]))"
```

Result: accepted.

```sh
bd close primary-y0h6.7 -r "Validated generated role outputs and cleanup behavior for AgentProtocolDesign. Source checks passed, primary generated state is current, role inventory exactly matches 30 Claude/Codex/Pi physical outputs, no symlinks or generated notices were found, and cleanup is covered by an automated stale-inventory preservation test. Evidence: /home/li/primary/agent-outputs/AgentProtocolDesign/Implementer-Evidence.md. Runtime Codex/Pi live role listing remains residual audit risk."
```

Result: closed.

```sh
orchestrate "(Release general-code-implementer)"
```

Result: released `(Task primary-y0h6.7)` and the evidence path.

```sh
cargo clippy --all-targets -- -D warnings
```

Result: passed.

```sh
nix flake check
```

Result: passed. The flake ran 9 checks, including build, test, fmt, clippy, no hard-coded generation roots, non-writing check request, active-manifest request use, and obsolete wrapper removal. The command output included transient Nix store paths; this report intentionally omits those concrete paths.

```sh
SKILLS_SOURCE_ROOT=$PWD SKILLS_WORKSPACE_ROOT=/home/li/primary cargo run -- skills-check.nota
```

Result: passed. Check mode reported generated outputs for the current skills, all 30 role files, and `skills/generated-role-outputs.nota`; no drift was reported against `/home/li/primary`.

In `/home/li/primary`:

```sh
find /home/li/primary/.claude/agents /home/li/primary/.codex/agents /home/li/primary/.pi/agents -maxdepth 1 -type f | sed 's#^/home/li/primary/##' | sort
```

Result: exactly these 30 role outputs:

```text
.claude/agents/criomos-implementer.md
.claude/agents/general-code-implementer.md
.claude/agents/intent-maintainer.md
.claude/agents/intent-translator.md
.claude/agents/nix-auditor.md
.claude/agents/repo-operator.md
.claude/agents/repo-scaffolder.md
.claude/agents/rust-auditor.md
.claude/agents/scout.md
.claude/agents/skill-editor.md
.codex/agents/criomos-implementer.toml
.codex/agents/general-code-implementer.toml
.codex/agents/intent-maintainer.toml
.codex/agents/intent-translator.toml
.codex/agents/nix-auditor.toml
.codex/agents/repo-operator.toml
.codex/agents/repo-scaffolder.toml
.codex/agents/rust-auditor.toml
.codex/agents/scout.toml
.codex/agents/skill-editor.toml
.pi/agents/criomos-implementer.md
.pi/agents/general-code-implementer.md
.pi/agents/intent-maintainer.md
.pi/agents/intent-translator.md
.pi/agents/nix-auditor.md
.pi/agents/repo-operator.md
.pi/agents/repo-scaffolder.md
.pi/agents/rust-auditor.md
.pi/agents/scout.md
.pi/agents/skill-editor.md
```

```sh
printf 'claude '; find /home/li/primary/.claude/agents -maxdepth 1 -type f | wc -l
printf 'codex '; find /home/li/primary/.codex/agents -maxdepth 1 -type f | wc -l
printf 'pi '; find /home/li/primary/.pi/agents -maxdepth 1 -type f | wc -l
printf 'inventory '; tr ' []' '\n' < /home/li/primary/skills/generated-role-outputs.nota | sed '/^$/d' | wc -l
```

Result:

```text
claude 10
codex 10
pi 10
inventory 30
```

```sh
missing=0; for p in $(tr ' []' '\n' < /home/li/primary/skills/generated-role-outputs.nota | sed '/^$/d'); do test -f "/home/li/primary/$p" || { printf 'missing %s\n' "$p"; missing=1; }; done; exit $missing
```

Result: passed with no missing inventory paths.

```sh
actual=$(mktemp); inventory=$(mktemp); find /home/li/primary/.claude/agents /home/li/primary/.codex/agents /home/li/primary/.pi/agents -maxdepth 1 -type f | sed 's#^/home/li/primary/##' | sort > "$actual"; tr ' []' '\n' < /home/li/primary/skills/generated-role-outputs.nota | sed '/^$/d' | sort > "$inventory"; echo 'actual_not_in_inventory'; comm -23 "$actual" "$inventory"; echo 'inventory_not_actual'; comm -13 "$actual" "$inventory"; rm "$actual" "$inventory"
```

Result:

```text
actual_not_in_inventory
inventory_not_actual
```

So the physical role files exactly match the generated inventory: no extra inactive role file exists in the generator-owned role target directories, and no inventoried path is missing.

```sh
find /home/li/primary/.claude/agents /home/li/primary/.codex/agents /home/li/primary/.pi/agents -maxdepth 1 -type l -printf '%p\n' | sort
```

Result: no symlinks reported.

```sh
grep -RInE '@generated|generated by|DO NOT EDIT|Generated by|This file is generated' /home/li/primary/.claude/agents /home/li/primary/.codex/agents /home/li/primary/.pi/agents || true
```

Result: no generated-file notice matches in runtime role packets.

## Cleanup Behavior

Existing automated coverage directly validates the requested cleanup behavior, so I did not add a separate temporary-workspace check.

The passing test `write_mode_removes_only_inventory_owned_stale_role_outputs` in `/git/github.com/LiGoldragon/skills/tests/generation.rs` sets up:

- stale generated inventory path: `skills/generated-role-outputs.nota` containing `.claude/agents/old.md`;
- existing stale generated file: `.claude/agents/old.md`;
- existing non-inventoried file: `.claude/agents/human.md`;
- active generated output: `.claude/agents/worker.md`.

The test runs write mode and asserts:

- `.claude/agents/old.md` is removed;
- `.claude/agents/human.md` is preserved;
- `.claude/agents/worker.md` is written.

That is the exact safety condition required here: stale inventoried role outputs are removed, while non-inventoried files in role target directories are preserved.

## Representative Packets

Representative role inspected: `scout`.

Claude:

- Path: `/home/li/primary/.claude/agents/scout.md`
- Shape: Markdown with YAML frontmatter containing `name: scout` and a `description`.
- Body starts at line 6 with `# Role - scout`.
- `## Contract` appears at line 8.
- Shared `## Module - agent output protocol` appears at line 44.

Codex:

- Path: `/home/li/primary/.codex/agents/scout.toml`
- Shape: TOML with `name`, `description`, and `developer_instructions`.
- `developer_instructions` begins with `# Role - scout`, then the role contract, then the shared `agent-output-protocol` module.

Pi:

- Path: `/home/li/primary/.pi/agents/scout.md`
- Shape: Markdown with YAML frontmatter containing `name: scout` and a `description`.
- Body starts at line 6 with `# Role - scout`.
- `## Contract` appears at line 8.
- Shared `## Module - agent output protocol` appears at line 44.

This validates role-first packet assembly followed by shared module expansion for all three harness output formats.

## Runtime And Discovery Validation

Codex:

- `codex --help` and `codex debug --help` expose no role-listing or agent-spawn discovery command usable for a local smoke test.
- `codex -C /home/li/primary debug prompt-input 'generated role discovery probe'` confirmed current Codex prompt input still loads project skills from `/home/li/primary/.agents/skills`.
- The command did not list `.codex/agents/*.toml` roles, so it is not live runtime proof of spawned-role discovery.
- Source-evidenced validation remains the Scout report: local Codex source loads TOML role files under project `.codex/agents/**/*.toml`, with required `name` and `developer_instructions`, and a description from file or declaration.

Pi:

- `pi list` reports `packages/pi-subagents` as an active user package.
- `pi --help` exposes `--approve`, `--offline`, `--no-tools`, and non-interactive `--print`.
- `pi --approve --offline --no-tools --no-session -p '/subagents-models'` returned no useful output.
- `pi --approve --offline --no-tools --no-session -p '/subagents-doctor'` returned no useful output.
- Source/package-evidenced validation remains active: the installed `pi-subagents` package README and source document project discovery at `.pi/agents/**/*.md`, and `pi list` shows the package is active.

Live runtime listing or spawning of Codex and Pi generated roles remains unproven in this validation pass because the available local commands did not expose a non-interactive role list with useful output.

## Evidence Summary

- Parser coverage: `cargo test` passed, including active manifest and module index coverage.
- Dependency expansion coverage: `cargo test` passed, including ordered role dependency expansion and deduplication behavior.
- Physical copy coverage: `cargo test` passed and `/home/li/primary` check mode passed, with 10 Claude, 10 Codex, and 10 Pi role files present.
- No-notice coverage: runtime role packet scan found no generated-file notice banners.
- Cleanup coverage: existing automated test directly covers stale inventoried role removal plus non-inventoried file preservation.
- Current generated state: `/home/li/primary` is current with local `/git/github.com/LiGoldragon/skills` source according to `skills-check.nota`.
- Inventory correctness: `skills/generated-role-outputs.nota` contains exactly 30 paths and exactly matches the physical role files.
- Symlink check: role outputs are physical files, not symlinks.

## Fixes Made

None.

## Residual Risks For Auditor

- Codex spawned-role discovery was validated from local source and generated file shape, not from a live `codex` role-list or spawned-role command.
- Pi project role discovery was validated from active package state plus installed package source/README, not from a live subagent list or spawned-role command.
- `nix flake check` validated the dirty local checkout, not a pushed remote ref. This is expected for this bead because commit/push is explicitly out of scope and assigned downstream.
- The working copies in both `/git/github.com/LiGoldragon/skills` and `/home/li/primary` were already dirty from earlier AgentProtocolDesign beads; this validation preserved those changes and did not attempt to normalize or commit them.
