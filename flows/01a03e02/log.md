# Flow 01a03e02

## About

Remember the declarative Claude Desktop installation and determine why a new local thread exits before Claude Code starts on NixOS.

Remembered: 01a038be — depth 1

## Settled

- Claude Desktop remains the declaratively deployed `llm-agents.nix` package; its launcher and the separately packaged terminal Claude Code work.
- A Desktop local thread selects a different, Desktop-downloaded Claude Code runtime at `~/.config/Claude/claude-code/2.1.237/claude`.
- That downloaded runtime is a generic x86-64 ELF requesting `/lib64/ld-linux-x86-64.so.2`. On this NixOS session that path reaches `stub-ld`, `NIX_LD` is unset, and direct execution reproduces exit 127.
- The failure is therefore at the generic-Linux dynamic-loader boundary before Claude Code starts. It is not evidence of a project, conversation, MCP, OAuth-handler, or Claude Desktop launcher failure.
- The versioned executable under `~/.config/Claude` is software installed statefully by Desktop. This violates the remembered ruling even though the Home configuration itself declared only the Desktop package; the runtime mutation was hidden behind the application boundary during the earlier audit.
- Mutating the downloaded runtime with `patchelf` would add another stateful mutation. A narrowly scoped Desktop wrapper or system-wide `programs.nix-ld` could diagnose compatibility, but either would merely make the prohibited mutable runtime executable.
- The terminal design is upstream support or a maintained package patch that makes Desktop invoke the Nix-packaged Claude Code executable; no supported external-runtime setting has been found. If that cannot be sustained, local Desktop threads do not fit the current declarative installation design.
- The living ruled that Desktop cannot use software it installs statefully and directed the Claude Desktop Nix code to force Desktop to use the declaratively packaged Claude Code. The exact words are preserved in `vision/claudeDesktopUsesOurClaudeCode.md`.
- Anthropic's APT index established that the deployed Desktop `1.34493.1` was obsolete relative to `1.37937.1`. Public Nix prior art independently found the same dormant `CLAUDE_CODE_LOCAL_BINARY` seam, but its activate-only patch retained fail-open download behavior.
- CriomOS-home `origin/main` commit `656afcdd1f56ea135ab0b0aaec084a215ba5a4b6` updates Desktop to `1.37937.1`, Claude Code to `2.1.246`, and ChatGPT Desktop to `26.820.60940` while Codex remains `0.149.1`. It derives Desktop with the exact terminal `claudeCodePackage`, activates the vendor's dormant local override, makes an absent/non-executable declared CLI terminal, suppresses invalidation, and refuses VM copying rather than materializing an executable under user state.
- A dedicated Nix check executes the actual patched manager through the packaged production Electron runtime in isolated valid and missing-override states. Its test was first witnessed failing with a deliberately wrong terminal error; the corrected immutable derivation then built on Prometheus with local fallback disabled and exited `0`. It proves the exact Nix CLI path, persistent failure on any downloader/copy/removal fallback, and no mutation under the manager's `Claude/claude-code` or `Claude/claude-code-vm` executable roots.
- The built wrapped launcher reports Desktop `1.37937.1` with exit `0` in fresh HOME/XDG state without opening a GUI or account session. Independent final review found no remaining contract-test blocker.

## Open

- CriomOS-home is landed and proven but not deployed. Its layered CriomOS consumer pin and the target user environment remain unchanged.
- After authorized deployment, one fresh local Desktop thread must witness the installed GUI/account path using the declared CLI and leaving the two managed executable roots absent. No GUI/account interaction was performed in this realization.
