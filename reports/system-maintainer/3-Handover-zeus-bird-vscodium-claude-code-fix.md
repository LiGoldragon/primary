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

The first cleanup removed the stale mutable `anthropic.claude-code-*-linux-x64` extension directory and left the Home Manager symlinked extension in place. That fixed the bad binary path, but it also removed the exact versioned path VSCodium's mutable `extensions.json` still referenced, so the Claude sidebar disappeared.

The corrected immediate fix restores that versioned path as a symlink to the Home Manager-managed extension:

- `anthropic.claude-code` remains the Home Manager symlink.
- `anthropic.claude-code-2.1.170-linux-x64` is a compatibility symlink to `anthropic.claude-code`.
- The native binary reached through the compatibility path resolves to the Nix-built `claude-code` binary.

Existing VSCodium windows may need a window reload or restart so the extension host rescans the restored path.

## Durable fix

CriomOS-home commit `26e825d8` was the too-aggressive cleanup. Commit `59b12b56` corrects it: the Home Manager activation hook now replaces stale mutable Claude Code versioned directories with a compatibility symlink to the managed extension, while pruning other stale Claude Code versioned directories. Future activations keep VSCodium on the managed binary without breaking VSCodium's versioned extension-location cache.
