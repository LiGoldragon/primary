# ChatGPT Wayland override witness

Method: code read `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/agent-intercom.nix`.

The graphical profile's `chatgptPackage` binding overrides the llm-agents
ChatGPT package with `commandLineArgs = "--ozone-platform=wayland"`. The
existing `chatgptWithSharedCodex` wrapper remains in place and still sets
`CODEX_CLI_PATH` to the pinned Codex CLI.

Method: focused graphical Home Manager evaluation with `nix eval --option eval-cache false --impure --json --expr '<graphical Agent Intercom configuration expression>'`.

The focused configuration evaluation returned `true`, confirming that the
graphical module assembled its ChatGPT desktop entry and Codex URI default.

Method: remote-only historical precondition with `nix build --impure --refresh --no-link --option max-jobs 0 --option fallback false --builders '@/etc/nix/machines' --expr '<905dfdd9f751 generated-launcher precondition>'`.

The historical precondition failed with builder exit 1: the generated shared
launcher still referenced the unoverridden llm-agents ChatGPT package. This is
the red witness for the new artifact-level no-original-package-reference
condition.

Method: remote-only current wrapper contract with `nix build --impure --refresh --no-link --option max-jobs 0 --option fallback false --builders '@/etc/nix/machines' --expr '<8b41cc323f17 graphical ChatGPT wrapper contract>'`.

Prometheus completed the current wrapper contract. It observed a generated
launcher that does not reference the original package, reaches a package with
the Wayland Ozone argument, and retains both `CODEX_CLI_PATH` and the pinned
Codex executable target.

Method: full graphical durable check with `nix build --impure --refresh --no-link --option max-jobs 0 --option fallback false --builders '@/etc/nix/machines' --expr '<8b41cc323f17 agent-intercom-graphical-tui check>'`.

The full check did not complete: the independently landed
`claude-desktop-with-declared-claude-code` derivation failed when removing its
`app.asar` file with permission denied. ChatGPT and Agent Intercom derivations
had completed before that dependency failure.

Limitations: the focused green witness proves the generated package and wrapper
contract, not a live graphical session. No Home Manager activation, ChatGPT
launch, OAuth interaction, or desktop-process inspection was performed.
