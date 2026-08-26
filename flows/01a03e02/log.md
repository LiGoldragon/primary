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

## Open

- The living has requested diagnosis, not authorized a repair.
- A realization round must first establish whether Desktop can be made to invoke the pinned Nix CLI without materializing a second executable. A loader experiment, if explicitly authorized for diagnosis, must remain narrower than a system-wide generic-ELF capability and must prove a real Desktop local thread end to end.
- The supported Remote Control alternative changes transcript-sync/privacy scope and requires an explicit choice.
