# Scout Situational Map

Task: determine whether a local Pi extension/package already provides a generic configurable dark/light theme applier, or whether the current CriomOS-specific switcher needs rewrite/rename. Scope was `/home/li/.pi/agent/packages`, Pi settings, and scoped local references.

Commands consulted: `spirit "(PublicTextSearch [pi extension dark light theme])"`, `find`, `rg`, `sed` over `/home/li/.pi/agent/packages`, `/home/li/.pi/agent/settings*.json*`, and scoped `/home/li/primary` references. Spirit returned broad design/refactoring records only; no specific theme-extension intent.

## Observed facts

- Installed package manifests under `/home/li/.pi/agent/packages` list: `pi-continue`, `pi-criomos`, `@aliou/pi-linkup`, `pi-mcp-adapter`, and `@tintinweb/pi-subagents`.
- Only `pi-criomos` declares Pi themes and a theme extension: `/home/li/.pi/agent/packages/pi-criomos/package.json` has `"themes": ["./themes"]` and extension `"./src/extensions/theme-switcher.ts"`.
- `pi-criomos` contains only two theme files: `themes/criomos-dark.json` and `themes/criomos-light.json`.
- `/home/li/.pi/agent/packages/pi-criomos/src/extensions/theme-switcher.ts` is hard-coded to:
  - read `${XDG_STATE_HOME:-$HOME/.local/state}/chroma/current-mode`;
  - accept only `dark` or `light`;
  - map via `themeName(mode) { return \`criomos-${mode}\`; }`;
  - set status key `criomos-theme`;
  - run on `session_start`, `before_provider_request`, `tool_call`, and cleanup on `session_shutdown`.
- The current user settings include `"theme": "criomos-light"` and package `"packages/pi-criomos"` in `/home/li/.pi/agent/settings.json`.
- A backup settings file also used `pi-criomos` and `criomos-dark`: `/home/li/.pi/agent/settings.json.before-disable-pi-criomos-20260523151920`.
- No other local package grep hits indicate a dark/light theme applier; `pi-mcp-adapter/mcp-panel.ts` has an internal panel theme only, not Pi global theme switching.

## Interpretation

No existing local candidate already satisfies the desired behavior. The only candidate is a CriomOS-specific Chroma state watcher, not a generic reusable extension with configurable preferred dark/light theme names.

The likely rewrite/rename target is `/home/li/.pi/agent/packages/pi-criomos/src/extensions/theme-switcher.ts`; implementers should also inspect `/home/li/.pi/agent/packages/pi-criomos/package.json` and the two `themes/criomos-*.json` files.

## Naming/configuration clues

The generic replacement likely needs configurable dark/light theme names instead of `criomos-${mode}`, a non-CriomOS status key/name, and care not to keep stale `ExtensionContext` in long-lived watchers after session replacement/reload. Existing event hooks show where the stale-context bug could arise: `filesystem.watch` and `setInterval` closures capture the `context` passed to `startWatcher(context)`.

## Not checked

No web/package-registry search was run. No tests or Pi runtime sessions were run. No files were modified except this report.
