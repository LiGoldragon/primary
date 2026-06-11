---
title: 3 — Zeus Bird VSCodium Claude Code fix
role: system-maintainer
date: 2026-06-11
topics: [zeus, bird, vscodium, claude-code, home-manager]
description: Fix VSCodium loading the mutable Claude Code VSIX binary instead of the Nix-managed Claude Code extension binary.
---

# 3 — Zeus Bird VSCodium Claude Code fix

## Symptom

Bird's VSCodium Claude Code extension on Zeus failed to launch Claude with NixOS's stub loader message for a generic dynamically linked executable. The extension log showed VSCodium spawning the mutable extension path under Bird's profile directory rather than the Nix-managed Home Manager extension symlink.

## Cause

CriomOS-home already packages the Anthropic Claude Code VSCodium extension with the generic bundled `resources/native-binary/claude` replaced by a symlink to the Nix-built `claude-code` binary from the `llm-agents` flake input.

Zeus still had an older marketplace-installed versioned extension directory alongside the Home Manager symlink. VSCodium selected that mutable directory, so it ran the bundled generic-Linux executable and failed on NixOS.

## Immediate fix on Zeus

Removed the stale mutable `anthropic.claude-code-*-linux-x64` extension directory from Bird's VSCodium extension directory, leaving the Home Manager symlinked extension in place.

Verification completed through root-mediated commands as Bird:

- The active `anthropic.claude-code` extension path is the Home Manager symlink.
- Its native binary resolves to the Nix-built `claude-code` binary.
- `claude --version` through that extension path returns `2.1.170 (Claude Code)`.
- `codium --list-extensions --show-versions` lists `anthropic.claude-code@2.1.170`.

Existing VSCodium windows may need a window reload or restart so the extension host stops referring to the deleted mutable directory.

## Durable fix

CriomOS-home commit `26e825d8` adds a Home Manager activation hook in `modules/home/vscodium/vscodium/default.nix` that removes stale mutable `anthropic.claude-code-*-linux-x64` extension directories after link generation. Future activations keep VSCodium on the managed extension path.
