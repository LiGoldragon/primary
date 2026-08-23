# Codex live theme switching

## Conclusion

The live palette-refresh failure and its stale composer contrast are both reported upstream. No complete merged live-refresh fix was found as of 2026-08-23. The local explicit syntax-theme setting is a separate configured condition, not an upstream failure.

The local failure has two independent inputs:

1. `$CODEX_HOME/config.toml` explicitly sets `[tui] theme = "dracula"`. Official documentation says an explicit `tui.theme` overrides automatic light/dark syntax-theme detection. Removing that setting restores automatic syntax-theme selection at process startup, but does not make a running Codex follow later palette changes.
2. Codex 0.148.0 makes a best-effort probe of the terminal's default foreground/background at startup or resume and then caches the result or a fallback/unknown value. It does not subscribe to Ghostty's live color-scheme notifications. After Chroma reloads Ghostty's palette, Codex can redraw from the old cached result; the composer therefore keeps the wrong contrast until a later process obtains current defaults.

The `/theme` command is not a whole-interface light/dark switch. It selects a syntax-highlighting theme. Many semantic TUI styles, including the composer background, use cached terminal defaults, while some statuses and accents use fixed or ANSI colors. Changing `/theme` can therefore update highlighted content while leaving the composer wrong.

## Current event path

```text
Chroma ThemeMode
  -> replace Ghostty's explicit palette config
  -> Ghostty D-Bus reload-config
  -> Ghostty changes the live terminal palette
  -X-> Codex receives no palette-change event
  -> Codex redraws from its cached startup default-color result
  -> prompt/composer contrast remains stale
```

Chroma's current implementation does not scan PTYs or broadcast OSC sequences into applications. Its current D-Bus consumer interface supports Emacs, not Codex. Terminal-to-application notification is the recommended general boundary rather than a Chroma-specific Codex consumer; that is a design conclusion, not current documented behavior.

## Upstream reports and regression

- `openai/codex#18942` is open. Its initial 0.122.0 report says the input box remains dark after the system changes to light and uses restart as a workaround; later comments reproduce it in 0.147.0 and 0.149.0.
- `openai/codex#33694` is open. Its initial 0.144.5 report says composer and transcript rows retain Kitty's old palette and that focus-out/focus-in repairs the composer; a later 0.147.0 comment says focus changes, `Ctrl+L`, and terminal reload no longer repair it.
- `openai/codex#14105` is open and specifically reports unreadable composer text after a live terminal theme switch.
- `openai/codex#19153` was closed as completed and `#34585` was closed as a duplicate of `#33694`; neither establishes a merged complete live-refresh repair.
- `openai/codex#38575` is an open proposal to subscribe to DEC private mode 2031 palette-change notifications.
- `openai/codex#21130` remains open and records that `/theme` affects syntax highlighting rather than the complete TUI palette.
- `openai/codex#2020` was closed as completed for light-background support, with `#21950` supplying static light-mode contrast work. That establishes static detection/contrast behavior, not reliable live switching.

Codex previously re-queried default terminal colors on focus (`#4673`, merged 2025-10-03). That path was removed by `#35649`, shipped in 0.147.0, because a synchronous focus-time terminal query could block and discard queued keystrokes. Current `main` redraws on focus while deliberately retaining the startup-cached palette. The old resizing workaround was not a supported palette refresh: current resize handling only updates geometry/reflow. Older success was incidental to redraw/focus behavior around the resize.

The 0.149.0 reproduction in `#18942` means upgrading alone is not a demonstrated fix; it does not prove that every 0.149 build and environment must fail.

## Repair anatomy

A promising upstream repair design is:

1. Teach Codex's pinned crossterm fork to parse `CSI ? 997 ; 1 n` and `CSI ? 997 ; 2 n` as dark/light palette-change notifications. It currently discards those unknown CSI sequences.
2. Enable `DECSET 2031` when the TUI starts and disable it during every cleanup path.
3. On notification, coordinate a bounded OSC 10/11 foreground/background probe through a single input owner. The current probe does not replay unrelated bytes, and merely dropping/restarting the event broker may also lose parser-buffered input. A safe implementation needs an explicit broker pause/probe/replay/resume design rather than calling the current probe from an event handler.
4. Atomically replace the cached terminal palette only after a complete successful probe; retain the last known-good pair on failure.
5. Request a full draw. Composer styling reads the default palette on every render, and the markdown cache already includes terminal foreground/background in its key, so updating the central cache invalidates the right consumers.
6. When no explicit `tui.theme` is configured, reselect the adaptive runtime syntax theme and advance its revision. Preserve explicit user-selected themes.
7. For terminals without DECSET 2031 support, a coordinated asynchronous focus-time probe can be a fallback, but the removed synchronous query must not return.

The terminal notification is only a change trigger; Codex still needs OSC 10/11 to learn the effective RGB colors. If the event path proves safe across supported terminals, this design can work without introducing an application-specific Chroma contract.

Ghostty 1.3.1 contains the DECSET 2031 enable/disable and color-scheme report sequences, while local Codex 0.148.0 does not. There is one Ghostty-side uncertainty: `ghostty-org/ghostty#13604` reports incorrect notification state unless both light and dark conditional themes are configured. The local Chroma templates write explicit colors rather than a conditional theme pair, so both notification emission and the reported mode must be tested. Treating the notification as a trigger followed by an actual color query is a proposed mitigation, not established Ghostty behavior.

## Available action now

- Remove `theme = "dracula"` from `[tui]` to restore automatic syntax-theme selection for newly started or resumed Codex processes. This is a startup improvement, not a live-switch fix.
- Do not expect `/theme`, `Ctrl+L`, focus changes, resize, or 0.149.0 to repair the stale palette reliably.
- Quit/resume is the reported recovery in the cited reproductions; its reliability remains version- and environment-dependent.
- A locally patched Codex implementing and proving the event path above is the direct candidate. Downgrading to the former synchronous focus-query behavior trades this defect for known freezes/input loss and is not a sound fix.

Official OpenAI documentation covers syntax-theme selection, persistence, and explicit-versus-automatic syntax-theme behavior. It does not document live palette notifications, DECSET 2031, Ghostty/Chroma integration, or redraw/cache lifecycle; those conclusions above come from current source, first-party issue history, local inspection, and identified design inference.

## Unknowns to prove before implementation

- Whether the locally packaged Ghostty 1.3.1 emits a 997 notification after Chroma's exact `reload-config` transition.
- Whether Ghostty emits it under the current explicit-palette templates despite the conditional-theme issue.
- The safe pause/probe/resume API needed in Codex's event broker and the correct Unix/Windows split.
- Tests for queued typeahead, partial/malformed OSC replies, unsupported terminals, cleanup after panic, and explicit-versus-adaptive syntax themes.

## Sources

- [OpenAI CLI customization](https://learn.chatgpt.com/docs/cli-customization)
- [OpenAI configuration schema](https://learn.chatgpt.com/docs/config-schema.json)
- [Input box remains dark after system theme changes, openai/codex#18942](https://github.com/openai/codex/issues/18942)
- [TUI does not fully redraw after Kitty palette change, openai/codex#33694](https://github.com/openai/codex/issues/33694)
- [Composer text becomes unreadable, openai/codex#14105](https://github.com/openai/codex/issues/14105)
- [Adaptive theme does not refresh, openai/codex#19153](https://github.com/openai/codex/issues/19153)
- [Automatic theme change request, openai/codex#34585](https://github.com/openai/codex/issues/34585)
- [DECSET 2031 proposal, openai/codex#38575](https://github.com/openai/codex/issues/38575)
- [Configurable complete TUI colors, openai/codex#21130](https://github.com/openai/codex/issues/21130)
- [Static light-background support, openai/codex#2020](https://github.com/openai/codex/issues/2020)
- [Static light-mode contrast work, openai/codex#21950](https://github.com/openai/codex/pull/21950)
- [Original focus-time palette refresh, openai/codex#4673](https://github.com/openai/codex/pull/4673)
- [Removal of focus-time palette probing, openai/codex#35649](https://github.com/openai/codex/pull/35649)
- [Codex 0.147.0 release](https://github.com/openai/codex/releases/tag/rust-v0.147.0)
- [Current event-stream source](https://github.com/openai/codex/blob/2161ec272a7d6b775c9c721e6206f4fe63e383f2/codex-rs/tui/src/tui/event_stream.rs)
- [Current terminal palette cache](https://github.com/openai/codex/blob/2161ec272a7d6b775c9c721e6206f4fe63e383f2/codex-rs/tui/src/terminal_palette.rs)
- [Current composer style derivation](https://github.com/openai/codex/blob/2161ec272a7d6b775c9c721e6206f4fe63e383f2/codex-rs/tui/src/style.rs)
- [Contour palette-change notification protocol](https://contour-terminal.org/vt-extensions/color-palette-update-notifications/)
- [Ghostty notification-state issue](https://github.com/ghostty-org/ghostty/issues/13604)
- Local Codex configuration: `/home/li/.codex/config.toml`
- Local Chroma implementation: `/git/github.com/LiGoldragon/chroma/src/theme.rs`
- Local Chroma D-Bus contract: `/git/github.com/LiGoldragon/chroma/src/theme_dbus.rs`
