# Flow 01a038be

## About

Deploy Claude Desktop and Codex CLI through an external flake after auditing its source and installation behavior.

Remembered: 01a0338f — depth 1

## Settled

- Flow 01a0338f established that Ouranos's `ChatGPT` entry is an unofficial `ilysenko/codex-desktop-linux` Electron package, Zeus's `Codex` entry is a Chrome PWA, and neither host had Claude Desktop; both hosts had Claude Code.
- The living wants Desktop applications on medium-size graphical nodes, a streamlined source/install audit on every third-party-flake update, and explicit terminal/Desktop engine-version alignment.
- Codex Desktop can select a shared pinned CLI through `CODEX_CLI_PATH`; Claude Desktop embeds and manages its own Code runtime and has no supported external-CLI override, so any embedded/standalone skew must be exposed.

## Open

- The external flake's malicious-intent and source/install audit outcome is still pending.
- The exact provider, medium-size projection, and Claude Desktop version policy remain implementation decisions for the parent realization after the audit.
- Current consumers still expose the unofficial Codex Desktop input and no Claude Desktop projection; the current CriomOS checkout has unrelated dirty changes and must not be treated as a clean deployment baseline.
