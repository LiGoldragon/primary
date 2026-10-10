# Canonical Skills Recovery Fix

Task scope: emergency recovery to restore canonical `LiGoldragon/skills` as the only skills source, preserve generated-workspace drift before regeneration, update skill-editor/orchestration doctrine, regenerate primary targets from canonical source, and verify through Nix.

## Canonical repo verification

- Path verified: `/home/li/primary/repos/skills`
- JJ root verified: `/home/li/primary/repos/skills`
- Remote verified: `origin git@github.com:LiGoldragon/skills.git`
- Blocker status: no blocker; remote matches `github.com/LiGoldragon/skills`.

## Preserved generated-diff artifact

- Preserved before any successful regeneration at `/home/li/primary/agent-outputs/primary-ascl/generated-diff-recovery-artifact.md`.
- Capture result: primary had no tracked working-copy diffs in `.agents`, `.claude`, `.pi/agents`, or `.codex/agents` at capture time; sampled generated skill-editor/orchestration snippets were saved for source-vs-generated drift recovery.

## Canonical source changes

Pushed canonical skills commit: `61f5b4eeda8f474f682a3a05743d1a7453fb65a7` on `main`.

Files changed in that commit:

- `/home/li/primary/repos/skills/modules/skill-editor/full.md`
- `/home/li/primary/repos/skills/roles/skill-editor/full.md`
- `/home/li/primary/repos/skills/modules/skill-source-core/full.md`
- `/home/li/primary/repos/skills/modules/orchestration/full.md`
- `/home/li/primary/repos/skills/tests/generation.rs`
- `/home/li/primary/repos/skills/flake.nix`

Final canonical source state also preserves the existing mainline removal of `human-interaction` from active manifests/source and generator pruning checks.

## Primary generated target changes

Primary generated commit created: `a6643323adec139f1ab726ba661a13759aff8aab`.

Generated/lock files changed by canonical regeneration and lock update:

- `/home/li/primary/.agents/skills/orchestration/SKILL.md`
- `/home/li/primary/.agents/skills/skill-editor/SKILL.md`
- `/home/li/primary/.claude/agents/skill-editor.md`
- `/home/li/primary/.claude/skills/orchestration/SKILL.md`
- `/home/li/primary/.claude/skills/skill-editor/SKILL.md`
- `/home/li/primary/.codex/agents/skill-editor.toml`
- `/home/li/primary/.pi/agents/skill-editor.md`
- `/home/li/primary/flake.lock`

Primary `flake.lock` now points `skills` at `github:LiGoldragon/skills/61f5b4eeda8f474f682a3a05743d1a7453fb65a7`.

Note: primary already had unrelated added agent-output files before this work began. Primary instructions require committing the whole working copy, so those pre-existing files were included in the primary generated commit and are named in the acceptance report.

## Nix checks run

- `cd /home/li/primary/repos/skills && nix flake check` passed after source conflict resolution and guardrail fixes.
- `cd /home/li/primary/repos/skills && nix run .#generate-skills -- /home/li/primary` passed before lock update using the canonical local source.
- `cd /home/li/primary && nix flake lock --update-input skills` updated primary to the pushed canonical skills commit.
- `cd /home/li/primary && nix run .#generate-skills` passed using the locked canonical GitHub input.
- `cd /home/li/primary && nix run .#check-skills` passed.
- `cd /home/li/primary && nix flake check` passed.

## Commit and push status

- `LiGoldragon/skills`: committed and pushed `61f5b4eeda8f474f682a3a05743d1a7453fb65a7` to `main`.
- `primary`: generated-target commit `a6643323adec139f1ab726ba661a13759aff8aab` created and pushed on `main`; this report is committed as a follow-up evidence artifact on the same pushed branch.

## Blockers and residual risks

- No active blocker.
- Residual risk: primary commit includes pre-existing unrelated agent-output files because this workspace instructs agents to commit the whole working copy.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Verified canonical repo path `/home/li/primary/repos/skills` and remote `git@github.com:LiGoldragon/skills.git`; recorded concrete changed source and generated target paths; severity noted for residual risk on pre-existing unrelated primary agent-output files."
    }
  ],
  "changedFiles": [
    "/home/li/primary/repos/skills/flake.nix",
    "/home/li/primary/repos/skills/modules/orchestration/full.md",
    "/home/li/primary/repos/skills/modules/skill-editor/full.md",
    "/home/li/primary/repos/skills/modules/skill-source-core/full.md",
    "/home/li/primary/repos/skills/roles/skill-editor/full.md",
    "/home/li/primary/repos/skills/tests/generation.rs",
    "/home/li/primary/.agents/skills/orchestration/SKILL.md",
    "/home/li/primary/.agents/skills/skill-editor/SKILL.md",
    "/home/li/primary/.claude/agents/skill-editor.md",
    "/home/li/primary/.claude/skills/orchestration/SKILL.md",
    "/home/li/primary/.claude/skills/skill-editor/SKILL.md",
    "/home/li/primary/.codex/agents/skill-editor.toml",
    "/home/li/primary/.pi/agents/skill-editor.md",
    "/home/li/primary/flake.lock",
    "/home/li/primary/agent-outputs/primary-ascl/generated-diff-recovery-artifact.md",
    "/home/li/primary/agent-outputs/primary-ascl/canonical-skills-recovery-fix.md"
  ],
  "testsAddedOrUpdated": [
    "/home/li/primary/repos/skills/tests/generation.rs",
    "/home/li/primary/repos/skills/flake.nix"
  ],
  "commandsRun": [
    {
      "command": "orchestrate \"(Claim (assistant [(Path /home/li/primary/repos/skills)] [canonical skills recovery source edits]))\"",
      "result": "passed",
      "summary": "Claimed canonical skills repo before edits."
    },
    {
      "command": "cd /home/li/primary/repos/skills && jj git remote list",
      "result": "passed",
      "summary": "Verified origin remote as git@github.com:LiGoldragon/skills.git."
    },
    {
      "command": "cd /home/li/primary/repos/skills && nix run .#generate-skills -- /home/li/primary",
      "result": "passed",
      "summary": "Regenerated primary workspace targets from canonical skills source after source fixes."
    },
    {
      "command": "cd /home/li/primary/repos/skills && nix flake check",
      "result": "passed",
      "summary": "All canonical skills checks passed, including new source-of-truth and orchestration guardrails."
    },
    {
      "command": "cd /home/li/primary && nix flake lock --update-input skills",
      "result": "passed",
      "summary": "Updated primary skills input to LiGoldragon/skills commit 61f5b4eeda8f474f682a3a05743d1a7453fb65a7."
    },
    {
      "command": "cd /home/li/primary && nix run .#generate-skills",
      "result": "passed",
      "summary": "Regenerated primary targets from the locked canonical GitHub skills input."
    },
    {
      "command": "cd /home/li/primary && nix run .#check-skills",
      "result": "passed",
      "summary": "Primary generated targets matched the locked canonical skills input."
    },
    {
      "command": "cd /home/li/primary && nix flake check",
      "result": "passed",
      "summary": "Primary generated-skills-current check passed."
    }
  ],
  "validationOutput": [
    "LiGoldragon/skills `nix flake check`: all checks passed.",
    "Primary `nix run .#check-skills`: generated output report completed without stale-output errors.",
    "Primary `nix flake check`: all checks passed."
  ],
  "residualRisks": [
    "low: `/home/li/primary` commit includes pre-existing unrelated agent-output files because local primary doctrine says to commit the whole working copy."
  ],
  "noStagedFiles": true,
  "diffSummary": "Canonical skills doctrine now names LiGoldragon/skills as source, labels workspace skill/agent files as generated targets, routes durable-intent candidates instead of saying orchestrator captures them directly, keeps context-handover separate/manual-load, and adds Nix/Rust guardrails; primary targets and skills lock were regenerated from the pushed canonical source.",
  "reviewFindings": [
    "no blockers",
    "low: /home/li/primary agent-output additions outside this task were present before primary commit and were included under whole-working-copy doctrine"
  ],
  "manualNotes": "Preserved pre-regeneration artifact: /home/li/primary/agent-outputs/primary-ascl/generated-diff-recovery-artifact.md."
}
```
