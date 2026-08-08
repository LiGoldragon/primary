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

## Follow-up — chooser popup

After the first fix, Ghostty reached the system opener but displayed the GTK "Open With" chooser. The reason was that the running Ghostty daemon's `PATH` did not include `~/.local/bin`, so it used system `xdg-open` instead of the Home-managed handlr wrapper. CriomOS-home now installs the same handlr-backed `xdg-open` wrapper into the Home profile's `bin`, which is already ahead of `/run/current-system/sw/bin` in Ghostty's process `PATH`.

Additional commits:

- CriomOS-home `f416f4c5b66b` — `home: expose handlr xdg-open in profile`.
- CriomOS `16272447c38e` — `system: repin CriomOS-home for xdg-open wrapper`.

Additional validation:

- Home was activated on `ouranos`.
- `type -a xdg-open` now resolves `~/.nix-profile/bin/xdg-open` before system `xdg-open`.
- `xdg-open file:///git/github.com/LiGoldragon/spirit-next/src/engine.rs` now goes through `handlr`, selects `emacsclient.desktop` from the `text/rust` default, and exits successfully.
- Pushed `github:LiGoldragon/CriomOS/main` still evaluates through `lojix-cli FullOs ... Eval`.

## Follow-up — VSCodium as default editor when enabled

Per Spirit record 1450, when VSCodium is enabled in the active CriomOS-home profile, it is the default editor for file-opening links and editor MIME handling for now.

Additional commits:

- CriomOS-home `de18823635e9` — `home: make VSCodium default editor when enabled`.
- CriomOS `94328542906e` — `system: repin CriomOS-home for VSCodium editor default`.

Additional validation:

- Home was activated on `ouranos`.
- `handlr get text/rust`, `handlr get text/markdown`, and `handlr get text/plain` now return `codium.desktop`.
- `xdg-mime query default text/rust` and `xdg-mime query default text/markdown` now return `codium.desktop`.
- `xdg-open file:///git/github.com/LiGoldragon/spirit-next/src/engine.rs` now goes through `handlr`, selects `codium.desktop`, and launches `codium` with the Rust source file.
- Pushed `github:LiGoldragon/CriomOS/main` evaluates through `lojix-cli FullOs ... Eval`.

## Follow-up — dirty plain-path links still selected GNOME Text Editor

A later click still opened GNOME Text Editor because it was not the clean OSC8 `file://` path case. Ghostty / handlr received plain terminal text such as `reports/system-operator/181-ghostty-file-link-editor-open-2026-06-02.md     ` or `reports/operator/287-nexus-recursive-computation-continuation-2026-06-02.md:1`. Because the clicked string carried trailing spaces or a line suffix, Ghostty could not resolve it against the terminal's current directory before invoking `xdg-open`; `handlr` then classified it as `application/x-zerosize`, whose system fallback was GNOME Text Editor.

Additional commits:

- CriomOS-home `b731b44181f9` — `home: route dirty editor links through Codium`.
- CriomOS `460e577ed8dd` — `system: repin CriomOS-home for dirty editor links`.

Additional validation:

- Home was activated on `ouranos`.
- `handlr get application/x-zerosize` now returns `codium.desktop`.
- The user-local `codium.desktop` now runs a CriomOS Codium launcher that trims trailing spaces, strips `:line[:column]` suffixes when the underlying file exists, resolves Primary-relative report paths from Ghostty's daemon cwd, and calls `codium --goto` when a position was present.
- Simulated Ghostty-style dirty paths from `/home/li` now go through `handlr`, select `codium.desktop`, and execute the CriomOS Codium launcher instead of `org.gnome.TextEditor.desktop`.
- Pushed `github:LiGoldragon/CriomOS/main` evaluates through `lojix-cli FullOs ... Eval`.

## Note

This fixes clean file URI links, chooser fallback, VSCodium default editor selection, and dirty plain-path terminal links. True universal jump-to-line from arbitrary relative paths still belongs in the emitter when possible, because the opener cannot always know the terminal program's current directory; the CriomOS launcher handles the common Primary-workspace report-path case.
