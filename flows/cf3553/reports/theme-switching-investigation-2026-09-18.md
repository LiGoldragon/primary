# Theme switching investigation — 2026-09-18

The screenshot at `/tmp/codex-clipboard-Wl4frV.png` is preserved in place; its
SHA-256 is `7013d345f1ecbb8a05ef493671cc50fc0c6356707c3c0f1cd00a3821ca5f27a1`.
It shows a dark Ghostty/Herdr terminal with very low-contrast Codex transcript
and command text, while the status chrome remains readable and the composer
uses a pale surface.

The direct local mismatch was an explicit `[tui] theme = "github"` in
`~/.codex/config.toml` while Ghostty's active generated config used
`background = #000000` and `foreground = #d0d0d0`. The fixed TUI theme was
removed from the user config after evidence review. This is a reversible
startup/resume correction only; no active harness was restarted or recolored.
`[desktop] appearanceTheme = "light"` remains and was not changed because no
source evidence establishes it as a CLI TUI control.

The remaining defect is live palette propagation. The earlier source review in
`flows/01a02fd9/reports/codexThemeSwitching.md` identifies that Codex probes
terminal defaults at startup/resume and caches them, while Chroma replaces
Ghostty's explicit palette then calls its reload route. Codex has no proven
live palette-change subscription in this setup. The needed runtime repair is
a safe terminal palette-change trigger followed by a bounded OSC 10/11
foreground/background requery, atomic cache replacement, and redraw. It must
preserve queued input and retain the previous palette when probing fails.

Herdr has no configured `[theme]` section. Its shipped default has
`auto_switch=false`; that is a separate integration surface and was not
changed without a source-backed configuration review. Claude's theme behavior
for already-running sessions remains unverified.

The living's new build policy applies to any implementation: tests must run
Nix-built binaries and Nix-packaged scripts; remote builder receipts must prove
offload and a local compilation fallback is not acceptable. Rust-only source
repos and runtime/content data should remain separated. This report contains
no build or test claim after that instruction.

## Sources

- `/tmp/codex-clipboard-Wl4frV.png`
- `~/.codex/config.toml` before/after backup
- `~/.config/ghostty/config.ghostty`
- `flows/01a02fd9/reports/codexThemeSwitching.md`
- `/home/li/.config/herdr/config.toml`

## Scope and current limits

The prior Codex cache analysis is a historical, source-supported hypothesis;
it predates installed Codex `0.153.4` and is not a current-version reproduction.
No heavy current-source fetch or validation was run while the living requested
low local CPU/RAM use. Claude is configured for automatic theme selection, but
live refresh in an existing Claude session remains unverified. Chroma's D-Bus
theme consumer is Emacs-only (`theme_dbus.rs`); Herdr has no `[theme]` section
and its shipped default says `auto_switch=false`.

The living also directed that tests use Nix-built binaries and Nix-packaged
scripts, with verified remote-builder compilation and no local fallback, and
that Rust-only source repositories remain separate from runtime/content data.
This is recorded by the designated vision/skill writer. It rules out local
compilation, heavy test suites, browser suites, and RAM-heavy validation while
the living watches movies; Nix invocation alone is not a remote-offload proof.
