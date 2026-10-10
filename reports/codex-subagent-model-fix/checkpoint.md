# Codex subagent-model fix checkpoint

- Scope: Codex only. Do not edit generated primary agent files, Pi, Claude, or skills.
- Prior worker artifact is empty; the failed transcript stopped during reconnaissance. The authoritative `CriomOS-home` and `CriomOS` working copies are clean.
- Declarative owner: `CriomOS-home/modules/home/profiles/min/default.nix`, its `flake.lock`, and its Codex check. Deployment consumer: `CriomOS` pins `criomos-home`.
- Current live evidence: `codex-cli 0.144.6`; managed config has no collaboration/agent overrides.
- Planned minimum chain: update the Codex input and config/check in CriomOS-home, commit/push; repin CriomOS to that commit, commit/push; activate through `meta-lojix` UserEnvironment and verify.
- Published chain: CriomOS-home `e41233841ead37124796993106a83b2bbf4cf7fb`; CriomOS `8e92d5014f3cb4b581e00883307039e9e6657dec`.
- Lane: `codex-subagent-model-fix`; target/action/rollback owner: `goldragon/ouranos/li`, typed Lojix `UserEnvironment` `ActivateNow`; rollback owner is this operator by redeploying the prior pushed CriomOS revision through the same typed path. Activation evidence: Lojix terminal `Current` user-environment generation for `ouranos`, then local Codex version/config/role and one V1 child rollout witness.
