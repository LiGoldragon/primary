# Current Desktop deployment state

Method: code read `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`, `/git/github.com/LiGoldragon/CriomOS-home/flake.lock`, `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/agent-intercom.nix`, `/git/github.com/LiGoldragon/CriomOS-home/packages/claude-code/default.nix`, `/git/github.com/LiGoldragon/CriomOS/modules/nixos/agent-intercom.nix`, `/git/github.com/LiGoldragon/goldragon/datom.dotos`; `jj status` in the three consumer repositories.

The current Home checkout is clean at working-copy revision `7eaba480` on top of `2d6225a8`. Its flake declares `numtide/llm-agents.nix`, `sadjow/codex-cli-nix`, and the unofficial `ilysenko/codex-desktop-linux`; the lock pins `llm-agents` to `aa8a6076962029a05e40abc3742c000877027c60`, `codex-cli` to `05b1b39da135e34526f898600e09e67b55d5436c`, and `codex-desktop-linux` to `c6d76231f0623c3ef0b18c7e9158697c96bdcf9f`.

`modules/home/profiles/min/agent-intercom.nix` currently projects direct Codex and Claude Code packages for local Agent Intercom capability. When `AgentIntercomGraphical` is present it enables the Codex Desktop module, points it at the direct Codex package, and enables remote control; it has no Claude Desktop projection. `packages/claude-code/default.nix` consumes `inputs.llm-agents`'s `claude-code` package.

The current CriomOS checkout is dirty at working-copy revision `75ea5b2c`, with existing edits in `flake.nix`, the Agent Intercom ownership gate, and `modules/nixos/userHomes.nix`; this is not a clean deployment witness. Its Agent Intercom module gates graphical prerequisites on `AgentIntercomGraphical` plus `AgentIntercomLocal`. The current cluster data gives Ouranos and Tiger `Max` size plus `AgentIntercomGraphical`, Zeus `Max` size with no graphical capability, and no exact `Medium` graphical node.

This witness is read-only. It does not establish that the external flake is safe or that the requested deployment is complete.
