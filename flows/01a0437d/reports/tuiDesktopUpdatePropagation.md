# TUI and desktop update propagation

## Question

Determine whether changing the declared Codex or Claude Code TUI package makes the corresponding desktop derivation rebuild and consume that exact package, and identify the terminal design if either desktop can retain a separately versioned runtime.

## Governing design

- Codex is to be declared once and used everywhere; extra launcher machinery is not the design.
- Claude Desktop must use the declaratively packaged Claude Code and must not download or copy a second executable into mutable user state.
- Terminal/Desktop alignment means equality of the CLI derivation used by their execution paths. It does not mean that a vendor desktop application's own release number must equal its separately released CLI product's version number.

## Current evidence

### Nix propagation

Both desktop integrations have explicit derivation edges to the shared CLI package:

- ChatGPT's local wrapper depends on `codexCliPackage` and exports its executable through `CODEX_CLI_PATH`. The terminal-facing `codexTui` is a different wrapper around that same CLI derivation. A `codexCliPackage` change therefore changes both outputs; a change confined to the TUI wrapper changes only the terminal wrapper because Desktop does not consume the terminal UI wrapper itself.
- The local Claude Desktop overlay takes both `claudeDesktopPackage` and `claudeCodePackage`, patches the Desktop ASAR with the exact `${claudeCodePackage}/bin/claude`, and has both derivations as build inputs. A read-only substitute-package evaluation produced a different Desktop derivation when only the Claude Code derivation changed.

This automatic invalidation occurs when the Home graph is evaluated and the resulting Desktop package is built. Editing or locking the Home producer does not itself rebuild, activate, or change the separately pinned CriomOS consumer.

The complete propagation path is:

1. update the `llm-agents` input and any separately pinned extension inputs in CriomOS-home;
2. evaluate the relevant Home packages and checks, then publish an immutable Home revision;
3. advance CriomOS's locked `criomos-home` input to that revision and inspect the flattened lock nodes;
4. evaluate and build the complete host toplevel;
5. deploy it through the typed CompleteHost route;
6. restart already-running desktop processes so they enter the new closure.

### What is and is not aligned

The shared executable derivations are aligned; the vendor Desktop products remain independent releases. ChatGPT's payload physically contains Codex `0.150.0-alpha.8`, while the shared declared CLI is currently `0.149.1`. Its resolver reads `CODEX_CLI_PATH` first and only falls back to the bundled binary when the override is absent; its local-daemon branch is also disabled when the override is present. A prior runtime witness observed the frontend spawn the selected executable as `codex app-server`. The bundled executable is therefore fallback residue rather than a second normal execution stack, but it remains directly reachable if the wrapper is bypassed.

Claude Desktop likewise retains vendor runtime-management machinery inside its payload, but the local patch selects the exact declared CLI and makes invalid/missing selection terminal rather than downloading, copying, or falling back.

The strongest terminal single-stack shape is to retain the explicit shared-package edges and add absence/fail-closed proof for vendor fallbacks. Claude already has that contract. ChatGPT can be strengthened by removing its bundled Codex executable from the packaged output or patching the resolver to require `CODEX_CLI_PATH`, then testing the real packaged runtime both with a valid override and with the override absent. Until that is realized and witnessed, the current wrapper provides one normal stack but the package still contains an alternate executable.

### Current consumer qualification

The checked CriomOS source and lock metadata do not trivially prove that the newest CriomOS-home revision is selected: the source URL and locked node can name different revisions, and locked evaluation wins. Producer correctness must therefore be paired with a consumer-lock and realized-host witness on every update.

## Sources

- `flows/01a0338f/vision/tuiAndDesktopVersions.md`
- `flows/01a038be/vision/codexDerivation.md`
- `flows/01a038be/vision/installingSoftwareStatefully.md`
- `flows/01a03e02/vision/claudeDesktopUsesOurClaudeCode.md`
- `flows/01a038be/reports/codexDesktopDeployment.md`
- `flows/01a03e02/reports/claudeDesktopDeclaredCliRealization.md`
- `flows/01a03f47/reports/claudeDesktopEglRepair.md`
- `flows/01a0338f/witnesses/codexDesktopAlignment.md`
- `flows/01a0437d/witnesses/updateMechanics.md`
- `/git/github.com/LiGoldragon/CriomOS-home/packages/codex/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/packages/codex/tui.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/overlays/claude-desktop.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/overlays/patch-claude-desktop-runtime.mjs`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/agent-intercom.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.lock`
- `/git/github.com/LiGoldragon/CriomOS/flake.nix`
- `/git/github.com/LiGoldragon/CriomOS/flake.lock`
