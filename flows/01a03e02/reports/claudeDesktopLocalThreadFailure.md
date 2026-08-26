# Claude Desktop local-thread failure on NixOS

## Conclusion

Claude Desktop did not itself crash. It downloaded and invoked its own Claude Code `2.1.237` executable for the local thread. That executable is built for a conventional Linux filesystem and asks for `/lib64/ld-linux-x86-64.so.2`; this NixOS system routes that request to its explanatory stub loader rather than a usable generic-Linux runtime. The child exits `127` before Claude Code begins.

The Nix-packaged Desktop and the separately pinned terminal Claude Code are different runtime paths. The former is patched in the Nix store and starts; the terminal `claude` is separately packaged as `2.1.241` and starts; Desktop's child under `~/.config/Claude/claude-code/` is mutable state outside both derivations and is not patched by either.

That versioned executable is also a stateful software installation by the Desktop application. The earlier deployment proved that Home Manager did not add an imperative installer; it did not observe this later application-managed installation boundary. Under the living's recorded ruling that software must not be installed statefully, this is the architectural fault beneath the immediate loader error.

## Design boundary

Patching the downloaded file in place is not a durable repair: a Desktop update can replace it, and doing so would introduce another imperative mutation into a declarative installation.

For diagnosis, the narrow compatibility bridge is a Claude-Desktop-specific wrapper that supplies Nix's declared generic-ELF loader and the smallest required library closure to Desktop and its descendants. A system declaration using `programs.nix-ld` is the broader alternative. Neither is the desired repair here: each makes Desktop's statefully installed runtime executable, and the system option additionally broadens generic downloaded-ELF execution into an operating-system capability. Anthropic does not document NixOS as a supported Linux Desktop target, and an upstream Claude Code issue reports `nix-ld` interactions with bundled command shims, so even an authorized experiment needs a behavioral local-thread test rather than only an executable-start test.

Compatibility does not settle runtime alignment. Desktop selected `2.1.237` while the remembered deployed terminal CLI was `2.1.241`. The desired end shape is for Desktop to invoke the already pinned Nix executable, through upstream support or a maintained package patch, without materializing a second executable under user state. No supported Desktop external-CLI setting was found in this investigation. If the package cannot provide that boundary, local Desktop threads are incompatible with the current declarative-installation ruling.

## Smallest meaningful proof after a repair

Start a new local thread from the installed Claude Desktop entry and observe that its actual downloaded or redirected Claude Code process crosses the loader boundary, completes initialization, and executes one harmless prompt in the selected local project. Also exercise a bundled command/tool path so a loader-only success cannot hide the reported `nix-ld` shim incompatibility.

## Sources

- Flow `01a038be`, especially `log.md`, `reports/rememberedDesktopDeployment.md`, `reports/codexHomeActivation.md`, and `vision/installingSoftwareStatefully.md`.
- Current screenshot/error and delegated local probes of `~/.config/Claude/claude-code/2.1.237/claude`, the NixOS loader path, the current environment, and the installed Desktop/terminal commands.
- Local authored deployment: `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/agent-intercom.nix` and `/git/github.com/LiGoldragon/CriomOS-home/ARCHITECTURE.md`.
- [NixOS stub loader explanation](https://nix.dev/permalink/stub-ld).
- [NixOS `nix-ld` module](https://github.com/NixOS/nixpkgs/blob/master/nixos/modules/programs/nix-ld.nix).
- [`llm-agents.nix` Claude Desktop package at the deployed pin](https://github.com/numtide/llm-agents.nix/blob/ed38c11e34e72199025ab70dc0042d78ef4c64cd/packages/claude-desktop/package.nix).
- [`llm-agents.nix` Claude Code package at the deployed pin](https://github.com/numtide/llm-agents.nix/blob/ed38c11e34e72199025ab70dc0042d78ef4c64cd/packages/claude-code/package.nix).
- [Anthropic Linux Desktop documentation](https://code.claude.com/docs/en/desktop-linux).
- [Anthropic Claude Code NixOS support request](https://github.com/anthropics/claude-code/issues/20012).
- [Anthropic Claude Code `nix-ld` command-shim issue](https://github.com/anthropics/claude-code/issues/74109).
- [Anthropic Remote Control documentation](https://code.claude.com/docs/en/remote-control).
