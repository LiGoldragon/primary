# Scout Situational Map: Chroma-to-Pi Theme Trigger

Task: read-only discovery of supported ways for external Chroma to push/trigger theme changes in an already-running Pi session, without a Pi-side polling/watcher extension.

Consulted: `spirit (PublicTextSearch [Pi Chroma theme external trigger])` (no specific Chroma/Pi intent found); local docs/source under `/home/li/.local/share/criomos/pi/package` for themes/settings/extensions/RPC/TUI/reload/IPC.

## Ranked mechanisms

1. **Terminal color-scheme notification + Pi “automatic” theme setting — best fit, if Chroma can change the terminal appearance.** Pi has built-in runtime sync: `InteractiveThemeController` registers `ui.onTerminalColorSchemeChange(...)`, enables `ui.setTerminalColorSchemeNotifications(true)` only for auto theme settings, and applies light/dark theme names on notification. Evidence: `src/modes/interactive/theme/theme-controller.ts:34,37-44,107-123`; auto setting syntax is `lightTheme/darkTheme` in `parseAutoThemeSetting`, `theme.ts:638-652`; color-scheme query falls back to OSC 11/background/COLORFGBG, `theme.ts:767-778`, `745-764`, `724-743`. Affects already-running interactive Pi sessions when auto-sync is enabled and the terminal/TUI emits color-scheme changes. Constraint: only light/dark selection, not arbitrary named theme unless encoded as the two sides of `theme`. Requires terminal support; settings UI warns “Light/dark detection requires terminal support” (`components/settings-selector.ts` found via grep). Direct OSC support from an external process depends on writing to the same terminal/pty and terminal support.

2. **Extension API `ctx.ui.setTheme(...)` — supported in-process control, but needs an ingress.** Docs explicitly support theme management: `ctx.ui.setTheme("light")`, `getAllThemes`, `getTheme`, and Theme objects in `docs/extensions.md:2357-2365`; implementation persists named theme and applies immediately via `themeController.setThemeName`, `interactive-mode.ts:2085-2099`; controller invalidates UI, `theme-controller.ts:92-104`. This affects running sessions. However, Pi has no built-in socket/server IPC for external Chroma to call; scoped search for `createServer|listen|socket|ipc|.sock|WebSocket` found only provider/auth/server references, not a Pi control server. A push design would need a small extension that opens a local socket/stdin/etc. and calls `ctx.ui.setTheme` on messages. That is a Pi-side extension, but not polling/watching if event-driven.

3. **Editing active custom theme file hot-reloads colors — runtime but not preferred.** Docs: “Hot reload: When you edit the currently active custom theme file, pi reloads it automatically” (`docs/themes.md:30-40` and hot reload line in same section). Source watches only `~/.pi/agent/themes/<current>.json` for non-built-in names and reloads after 100ms (`theme.ts:876-940`). This affects running sessions, but it is explicitly Pi-side file watching, so it violates the approved alignment if used as the control path.

4. **`/reload`, settings file, CLI flags, RPC mode — lower fit.** `/reload` reloads themes/settings in the current TUI (`usage.md:55`; `interactive-mode.ts:5044-5120`), but I found no supported external command channel to send `/reload` to an existing TUI. `--theme` loads resources at process startup (`usage.md:213-224`) and does not notify an existing session. RPC mode is stdio for a Pi subprocess (`usage.md:169-170`, `docs/rpc.md`) and includes no theme command; it is not an attach-to-running-session API.

## Recommendation

Prefer Chroma changing the terminal’s light/dark/color-scheme state and configure Pi `theme` as `lightTheme/darkTheme`. If Chroma must select arbitrary Pi themes, implement a minimal event-driven Pi extension exposing an explicit local control endpoint that calls `ctx.ui.setTheme`; avoid polling files.

Unknowns not fully checked: upstream `@earendil-works/pi-tui` package internals were not locally resolvable from this installed package, so exact escape sequences for color-scheme notifications were inferred only from Pi’s TUI interface names and fallback OSC 11 code.
