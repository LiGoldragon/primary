# Pi Automatic Theme Evidence

Task: stop loading the broken local CriomOS Pi theme-switcher extension, configure Pi 0.80.3 built-in automatic theme mode, and activate as far as safe locally.

Files consulted:
- `/home/li/.local/share/criomos/pi/package/README.md`
- `/home/li/.local/share/criomos/pi/package/docs/extensions.md`
- `/home/li/.local/share/criomos/pi/package/docs/themes.md`
- `/home/li/.local/share/criomos/pi/package/docs/packages.md`
- `/home/li/.local/share/criomos/pi/package/docs/settings.md`
- `/home/li/.local/share/criomos/pi/package/src/modes/interactive/theme/theme.ts`
- `/home/li/.local/share/criomos/pi/package/src/modes/interactive/components/settings-selector.ts`
- `/home/li/.local/share/criomos/pi/package/src/core/resource-loader.ts`
- `/home/li/.pi/agent/settings.json`
- `/home/li/.pi/agent/packages/pi-criomos/package.json`

Source truth found:
- Built-in automatic theme mode is encoded in the single `theme` setting as `<lightTheme>/<darkTheme>`.
- `parseAutoThemeSetting()` splits one slash and returns `{ lightTheme, darkTheme }`; `resolveThemeSetting()` selects `lightTheme` when terminal theme is `light`, otherwise `darkTheme`.
- `/settings` labels the automatic choices as “Light theme” and “Dark theme”; `getAutomaticThemeSetting()` writes `${lightTheme}/${darkTheme}`.
- Resource loading filters disabled package resources out before loading extensions; disabled resolved extensions are not executed.

Files changed:
- `/home/li/.pi/agent/settings.json`
  - Changed `theme` from fixed `criomos-light` to built-in automatic `criomos-light/criomos-dark`.
  - Changed the `packages/pi-criomos` entry to object form with `extensions: []`, leaving other pi-criomos resources enabled by omission.
- `/home/li/.pi/agent/packages/pi-criomos/package.json` was not changed because `packages/pi-criomos` is a read-only Home Manager symlink into the Nix store. The obsolete extension file remains present but is disabled by settings filtering.

Theme-related settings snippet:

```json
{
  "theme": "criomos-light/criomos-dark",
  "packages": [
    {
      "source": "packages/pi-criomos",
      "extensions": []
    }
  ]
}
```

Validation and activation evidence:
- `PI_OFFLINE=1 pi --version` passed: Pi reports `0.80.3`.
- `PI_OFFLINE=1 pi --help` passed and confirmed `/reload` exists for interactive reload of keybindings, extensions, skills, prompts, and context files; there is no non-interactive reload command in help.
- Node validation against installed Pi `dist` passed:
  - settings parsed with no `SettingsManager` errors;
  - `parseAutoThemeSetting("criomos-light/criomos-dark")` returned `{"lightTheme":"criomos-light","darkTheme":"criomos-dark"}`;
  - `resolveThemeSetting(..., "light")` returned `criomos-light` and `resolveThemeSetting(..., "dark")` returned `criomos-dark`;
  - package resolution shows `theme-switcher.ts` only as `enabled:false`;
  - resource loader loaded no pi-criomos extensions;
  - resource loader loaded `criomos-dark` and `criomos-light` themes;
  - theme diagnostics and extension errors were empty.

Deployment status:
- The user Pi settings file is updated in place, so new Pi processes will use built-in automatic theme mode and will not load the old extension.
- No safe non-interactive Pi reload/package-refresh command was found. For an already-running Pi TUI, run `/reload`; if the current process already loaded the old extension, restart Pi to guarantee the long-lived watcher/timer closures are gone.

Old extension loadability:
- The `theme-switcher.ts` file still exists in the read-only Home Manager package path, but Pi’s resolved resource list marks it `enabled:false` and the resource loader does not load it. It can still load only if another settings source or CLI `-e` explicitly enables that file/path.

Repository closeout:
- No commit or push was performed. The edited surface is live `~/.pi/agent/settings.json`, and `pi-criomos` itself is a read-only Nix store symlink with no local VCS checkout at that path.
