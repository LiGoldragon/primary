# Ouranos ChatGPT launcher

Method: probe `readlink -f /home/li/.nix-profile/bin/{codex-desktop,codex}; sed -n '1,200p' /home/li/.nix-profile/share/applications/codex-desktop.desktop; nix-store -q --binding name --binding system <derivation>; ps -efww | rg 'codex-desktop|webview-server|codex app-server'`

The probes were carried out read-only through the `ouranos_desktop` subflow on `li@ouranos`.

The menu entry `/home/li/.nix-profile/share/applications/codex-desktop.desktop` says `Name=ChatGPT`, but its `Exec` launches the Nix-store `codex-desktop` wrapper. Both `x-scheme-handler/codex` and `x-scheme-handler/codex-browser-sidebar` resolve to this desktop entry.

The executable chain is:

```text
/home/li/.nix-profile/bin/codex-desktop
  -> /nix/store/ij7k32xbgjdpc3kwjr85yydp39qysg3b-codex-desktop-computer-use-ui-remote-mobile-control-26.721.41059-codex-cli-path/bin/codex-desktop
  -> /nix/store/jxnzg81k635cwklj2wpy3j2bk4ihiscz-codex-desktop-computer-use-ui-remote-mobile-control-26.721.41059/opt/codex-desktop/start.sh
```

The package is `codex-desktop-computer-use-ui-remote-mobile-control-26.721.41059`. Its build metadata identifies Electron 42.3.0 and third-party source `ilysenko/codex-desktop-linux` version 0.10.3 at commit `c6d76231…`. That source's README calls the Linux package unofficial.

The running application is Electron/Chromium. Its launcher passes `--no-sandbox` and `--disable-gpu-sandbox` and starts a Python webview server bound to `127.0.0.1:5175`. No separate ChatGPT/Codex Flatpak, AppImage, or Chrome PWA was found for `li`.

The current profile's Codex CLI is 0.149.0. The already-running GUI's app-server process still resolves to Codex CLI 0.148.0.

Method: code read `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/agent-intercom.nix`

Lines 156–167 enable `programs.codexDesktopLinux`, its computer-use UI and remote-mobile-control feature variant, and the Codex CLI wrapper. The flake input is pinned in `CriomOS-home/flake.nix` near line 244.

Method: probe `readlink -f /home/li/.nix-profile/bin/claude; claude --version; find /home/li/.local/share/applications -iname '*claude*' -type f`

No Claude Desktop executable, package, launcher, or GUI process was found. The current package is Claude Code 2.1.241 at `/nix/store/z8v8iqiw084sxw2licg0pad9hwy7wmkg-claude-code-2.1.241`; the only desktop file is a non-display Claude Code URL handler. An older Claude Code 2.1.235 process was still resident.
