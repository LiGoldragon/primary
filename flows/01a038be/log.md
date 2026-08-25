# Flow 01a038be

## About

Deploy Claude Desktop and Codex CLI through an external flake after auditing its source and installation behavior.

Remembered: 01a0338f — depth 1

## Settled

- Flow 01a0338f established that Ouranos's `ChatGPT` entry is an unofficial `ilysenko/codex-desktop-linux` Electron package, Zeus's `Codex` entry is a Chrome PWA, and neither host had Claude Desktop; both hosts had Claude Code.
- The living wants Desktop applications on medium-size graphical nodes, a streamlined source/install audit on every third-party-flake update, and explicit terminal/Desktop engine-version alignment.
- The living narrowed Codex alignment to one `llm-agents` derivation declared once and used by every consumer; upstream Desktop launcher behavior remains unchanged.
- Home commit `f05a3639de72` removes the standalone Codex provider, installs Claude Desktop at the medium graphical gate, and evaluates the Codex terminal/Desktop/remote package equality on the pushed revision.

## Open

- A configured remote builder is absent, so the durable Nix checks and remote build have not run.
- The CriomOS consumer pin remains unchanged until that remote-build proof succeeds.
