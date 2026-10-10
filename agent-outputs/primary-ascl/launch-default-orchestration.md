# Launch Default Orchestration Implementation

Task: Work bead `primary-ascl.3` to default Claude, Codex, and pi sessions into orchestration mode at launch, with a launch-time escape hatch for non-orchestrator roles/sessions. Scope was source/config truth for the active home profile that installs the three CLIs.

Implemented in `CriomOS-home` source of truth:

- `modules/home/profiles/min/default.nix` now installs wrapper commands named `claude`, `codex`, and `pi` instead of the raw packages in the home profile.
- The default wrappers inject a compact parent-orchestrator instruction before the first model turn:
  - Claude: `--append-system-prompt` at process launch.
  - pi: `--append-system-prompt` at process launch.
  - Codex: `--config developer_instructions=...` at process launch, preserving the existing skill-read de-duplication instruction inside the combined developer instruction.
- Escape hatches are launch-time and mandatory:
  - `direct-claude`, `direct-codex`, and `direct-pi` launch the underlying tools with no default orchestration injection.
  - `CRIOMOS_AGENT_MODE=direct` also disables wrapper injection.
  - Claude skips injection for explicit `--agent`, `--agents`, `--system-prompt`, or `--append-system-prompt` launches.
  - pi skips injection for `PI_SUBAGENT_CHILD=1` or explicit system-prompt launches.
  - Codex skips injection for `--profile non-orchestrator`, explicit `developer_instructions` overrides, or the direct wrapper. A `~/.codex/non-orchestrator.config.toml` source declaration is installed so that profile keeps only the existing skill-read de-duplication instruction.
- `checks/ai-agent-launch-orchestration/default.nix` was added and wired into `flake.nix` to check the default injection and bypass surfaces.

Changed files:

- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/ai-agent-launch-orchestration/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`

Tests/checks run through Nix:

- `cd /git/github.com/LiGoldragon/CriomOS-home && nix run nixpkgs#nixfmt-rfc-style -- modules/home/profiles/min/default.nix flake.nix checks/ai-agent-launch-orchestration/default.nix` — passed; Nix emitted the local flake-registry warning before formatting.
- `cd /git/github.com/LiGoldragon/CriomOS-home && nix eval .#checks.x86_64-linux.ai-agent-launch-orchestration.drvPath` — passed.
- `cd /git/github.com/LiGoldragon/CriomOS-home && nix build .#checks.x86_64-linux.ai-agent-launch-orchestration --no-link` — passed.
- `cd /git/github.com/LiGoldragon/CriomOS-home && nix build .#checks.x86_64-linux.pi-harness-profile --no-link` — passed.
- `cd /git/github.com/LiGoldragon/CriomOS-home && nix eval --impure --expr '<mock min-profile import listing wrapper package names>'` — passed; evaluated wrapper package names as `claude`, `codex`, `pi`, `direct-claude`, `direct-codex`, and `direct-pi`.
- `cd /git/github.com/LiGoldragon/CriomOS-home && nix build --impure --no-link --expr '<mock min-profile wrapper symlinkJoin>'` — passed; built the six wrapper scripts.
- `jj -R /git/github.com/LiGoldragon/CriomOS-home status --no-pager` — passed after commit; working copy clean.

Commit/push status:

- Committed in `CriomOS-home`: `18761876a356` (`home: default agent launches to orchestration`).
- Pushed: `jj git push --bookmark main` reported `Bookmark main@origin already matches main` on verification.

Progress/tracker note:

- I did not update `/home/li/.pi/agent/sessions/--home-li-primary--/subagent-artifacts/progress/05f1f533/progress.md` or close/update the primary bead because Orchestrate rejected claims on both that progress file and `/home/li/primary/.beads`; they were owned by `skill-editor` for `primary-ascl.4-primary-ascl.5` progress/tracker work.

Residual risks:

- The change is declarative Home Manager source and is effective after the next home/profile activation using this pushed CriomOS-home revision.
- The new check is static plus wrapper-build smoke coverage. Full live behavioral proof would require launching the real CLIs after activation and observing first-turn prompt behavior; that would involve live model sessions and was not run here.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Implemented only the launch-time default orchestration mechanism and escape hatches in CriomOS-home home-profile source; added a focused Nix check and wrapper-build smoke validation."
    }
  ],
  "changedFiles": [
    "/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/default.nix",
    "/git/github.com/LiGoldragon/CriomOS-home/checks/ai-agent-launch-orchestration/default.nix",
    "/git/github.com/LiGoldragon/CriomOS-home/flake.nix"
  ],
  "testsAddedOrUpdated": [
    "/git/github.com/LiGoldragon/CriomOS-home/checks/ai-agent-launch-orchestration/default.nix"
  ],
  "commandsRun": [
    {
      "command": "orchestrate \"(Observe Roles)\"",
      "result": "passed",
      "summary": "Inspected active claims before editing."
    },
    {
      "command": "orchestrate \"(Claim (primary-ascl [(Path /git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/default.nix) (Path /git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/pi-models.nix) (Path /git/github.com/LiGoldragon/CriomOS-home/flake.nix) (Path /git/github.com/LiGoldragon/CriomOS-home/checks)] [primary-ascl.3 launch-time orchestration default implementation]))\"",
      "result": "passed",
      "summary": "Claimed the CriomOS-home source and check paths used for implementation."
    },
    {
      "command": "cd /git/github.com/LiGoldragon/CriomOS-home && nix run nixpkgs#nixfmt-rfc-style -- modules/home/profiles/min/default.nix flake.nix checks/ai-agent-launch-orchestration/default.nix",
      "result": "passed",
      "summary": "Formatted changed Nix files through Nix."
    },
    {
      "command": "cd /git/github.com/LiGoldragon/CriomOS-home && nix eval .#checks.x86_64-linux.ai-agent-launch-orchestration.drvPath",
      "result": "passed",
      "summary": "Evaluated the new check derivation."
    },
    {
      "command": "cd /git/github.com/LiGoldragon/CriomOS-home && nix build .#checks.x86_64-linux.ai-agent-launch-orchestration --no-link",
      "result": "passed",
      "summary": "Built the new focused launch orchestration check."
    },
    {
      "command": "cd /git/github.com/LiGoldragon/CriomOS-home && nix build .#checks.x86_64-linux.pi-harness-profile --no-link",
      "result": "passed",
      "summary": "Built the adjacent Pi harness profile check."
    },
    {
      "command": "cd /git/github.com/LiGoldragon/CriomOS-home && nix eval --impure --expr '<mock min-profile import listing wrapper package names>'",
      "result": "passed",
      "summary": "Confirmed the min profile evaluates the six wrapper package names."
    },
    {
      "command": "cd /git/github.com/LiGoldragon/CriomOS-home && nix build --impure --no-link --expr '<mock min-profile wrapper symlinkJoin>'",
      "result": "passed",
      "summary": "Built the Claude, Codex, pi, and direct wrapper scripts."
    },
    {
      "command": "cd /git/github.com/LiGoldragon/CriomOS-home && jj commit -m 'home: default agent launches to orchestration ...' && jj bookmark set main -r @- && jj git push --bookmark main",
      "result": "passed",
      "summary": "Committed and pushed the CriomOS-home implementation."
    },
    {
      "command": "cd /git/github.com/LiGoldragon/CriomOS-home && jj status --no-pager && jj git push --bookmark main",
      "result": "passed",
      "summary": "Verified clean worktree and that origin main matches local main."
    }
  ],
  "validationOutput": [
    "New Nix check built successfully.",
    "Adjacent pi-harness-profile check built successfully.",
    "Wrapper package evaluation returned claude, codex, pi, direct-claude, direct-codex, and direct-pi.",
    "CriomOS-home working copy is clean after commit and push."
  ],
  "residualRisks": [
    "Requires a home/profile activation before the wrappers become the live default commands.",
    "Live first-turn behavioral proof was not run because it would require launching real model sessions."
  ],
  "noStagedFiles": true,
  "diffSummary": "CriomOS-home min profile now installs launch wrappers for Claude, Codex, and pi that inject parent-orchestrator instructions by default and provide direct/profile/env escape hatches; a new Nix check covers the source constraints.",
  "reviewFindings": [
    "no blockers"
  ],
  "manualNotes": "Progress file and primary bead tracker updates were blocked by existing Orchestrate claims owned by skill-editor for primary-ascl.4-primary-ascl.5."
}
```
