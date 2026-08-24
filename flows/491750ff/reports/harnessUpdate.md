# Claude Code and Codex Home update

The declarative owner is `/git/github.com/LiGoldragon/CriomOS-home`. Its published `main` already contained the complete update: commit `30e19a081d1fdc8916b7645b7fa4ffffda3c1a8d` refreshed the Codex input/locks and version witnesses, and commit `0836e4b7e367efe6a81a4fa657e2a2f741f0d801` aligned the Codex sidebar metadata. The preceding published Home commit `756ce723ea7f1a58d20e2b6f153f15e30aa9b885` had already moved Claude Code and its VSIX to `2.1.241`; that version remains current.

The current upstream releases are Codex CLI `0.149.1` and Claude Code `2.1.241`. The coordinated Codex VSIX is `26.5818.61809`. The Home lock pins the Codex packaging flake to revision `05b1b39da135e34526f898600e09e67b55d5436c`; no generated `.agents`, `.claude`, `.codex`, or `.pi` tree was edited.

The focused projected evaluation and remote-only activation-package build passed. Lojix deployment 60 was submitted through the owner socket with the explicit Ouranos transport, Horizon input, `homeConfigurations.li.activationPackage`, `HomeManagerNixProfileV1`, `ActivateNow`, and `RequireImmutable`. It reached `Completed/Succeeded` and became the Current user-environment generation. The target login shell independently returned Codex `0.149.1` and Claude Code `2.1.241`.

The only coordination blocker was the unavailable Orchestrate socket during registration. It did not prevent source ownership, published revision use, Lojix deployment, or live verification. No reboot or emergency runtime mutation occurred.

## Sources

- Witness: `flows/491750ff/witnesses/upstreamVersions.md`.
- Witness: `flows/491750ff/witnesses/homeDeployment.md`.
- Code read: `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`.
- Code read: `/git/github.com/LiGoldragon/CriomOS-home/flake.lock`.
- Code read: `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix`.
- Code read: `/git/github.com/LiGoldragon/CriomOS-home/packages/claude-code/default.nix`.
- Upstream: https://github.com/openai/codex/releases/latest.
- Upstream: https://github.com/anthropics/claude-code/releases/latest.
- Upstream: https://marketplace.visualstudio.com/items?itemName=openai.chatgpt.
