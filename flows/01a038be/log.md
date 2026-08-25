# Flow 01a038be

## About

Deploy Claude Desktop and Codex CLI through an external flake after auditing its source and installation behavior.

Remembered: 01a0338f — depth 1
Remembered: 01a02fe5 — depth 1

## Settled

- Flow 01a0338f established that Ouranos's `ChatGPT` entry is an unofficial `ilysenko/codex-desktop-linux` Electron package, Zeus's `Codex` entry is a Chrome PWA, and neither host had Claude Desktop; both hosts had Claude Code.
- The living wants Desktop applications on medium-size graphical nodes, a streamlined source/install audit on every third-party-flake update, and explicit terminal/Desktop engine-version alignment.
- The living narrowed Codex alignment to one `llm-agents` derivation declared once and used by every consumer; upstream Desktop launcher behavior remains unchanged.
- Home commit `f05a3639de72` removes the standalone Codex provider, installs Claude Desktop at the medium graphical gate, and evaluates the Codex terminal/Desktop/remote package equality on the pushed revision.
- The exact pushed Home revision passed its graphical-TUI contract evaluation and remote-only build through the configured Prometheus Nix builder.  The build included Codex `0.149.0`, Claude Desktop `1.34493.1`, the maintained Desktop integration, Agent Intercom, and the contract itself.
- CriomOS commit `e1008e20abad`, on top of preserved commit `4c3da1562c49`, pins `criomos-home` exactly to `f05a3639de72`.  Its exact pushed materialized NixOS target passed separate evaluation and a remote-only Prometheus build.
- After endpoint identity proof, Lojix UserEnvironment deployment `61` activated immutable Home revision `f05a3639de72` for `goldragon/ouranos/li`.  Its terminal node-ledger record is `Completed/Succeeded` and Current; the live Home generation changed, Codex reports `0.149.0`, Claude Code reports `2.1.241`, both desktop executables are present, and the Codex remote-control and bridge services are active.
- Read-only live diagnosis found that the maintained Codex Desktop frontend is itself named `ChatGPT` by its shipped desktop metadata; the wrapper remains active and supplies the shared Codex CLI.  Claude Desktop instead has a missing discoverable `claude://` handler entry, which explains the callback chooser failure and has a small declarative repair path.

## Open

- Claude Desktop's embedded Code runtime version remains unobservable through the supported package interface.  The package identity is checked, but no unsupported external-runtime override or exact embedded-runtime parity claim exists.
- The concrete Home repair and regression check for Claude Desktop callback registration remain a proposal, not an authorized source/deployment change.
