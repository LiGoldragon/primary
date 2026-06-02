# Ghostty file-link editor opening — 2026-06-02

## Result

Ghostty opens clicked OSC8 file links on Linux by passing the URI to `xdg-open`. Pi's file-path renderer emits OSC8 links with `file://` targets for tool paths; Ghostty treats OSC8 links separately from its plain URL matcher and sends the stored URI through its open path.

The failing example was a Rust source file. `handlr mime file:///git/github.com/LiGoldragon/spirit-next/src/engine.rs` resolves the file to `text/rust`. CriomOS-home registered `text/x-rust` but not the newer shared-mime-info `text/rust` type, so the user-local `xdg-open` wrapper (`handlr open`) had no handler for the clicked file URI.

## Changes

CriomOS-home now registers `text/rust` for the preferred editor path:

- `modules/home/profiles/med/emacs.nix` — Emacs preferred-editor MIME defaults include `text/rust`.
- `modules/home/profiles/med/codium.nix` — user-local `codium.desktop` advertises `text/rust`.
- `modules/home/vscodium/vscodium/default.nix` — Codium preferred-editor MIME defaults include `text/rust`.

CriomOS was repinned to the new CriomOS-home commit so FullOS deployments carry the fix.

## Validation

- `nix flake check --no-build` in CriomOS-home passed.
- CriomOS-home commit `bd1e5330ae61` was pushed: `home: register Rust MIME type for editor links`.
- CriomOS commit `d5ec73c221ff` was pushed: `system: repin CriomOS-home for editor links`.
- Home was activated on `ouranos` through `lojix-cli HomeOnly ... Activate`.
- Runtime checks now show:
  - `handlr get text/rust` -> `emacsclient.desktop` for the current user.
  - `xdg-mime query default text/rust` -> `emacsclient.desktop`.
  - `xdg-open file:///git/github.com/LiGoldragon/spirit-next/src/engine.rs` exits successfully.
- Pushed `github:LiGoldragon/CriomOS/main` evaluates through `lojix-cli FullOs ... Eval`.

## Note

This fixes opening the file URI. Jump-to-line is a separate emitter issue: a `file://` URI from Pi opens the file, while editor-specific line jumps require links such as a `vscodium://file/...:line` style URI or an editor-aware emitter.
