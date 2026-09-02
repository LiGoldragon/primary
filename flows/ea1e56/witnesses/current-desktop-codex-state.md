# Current Desktop Codex State Witness

Captured 2026-09-02 on host `ouranos` (Europe/Madrid). This is a read-only snapshot of the local ChatGPT desktop/Codex connection surfaces. Runtime observation does not establish that the desktop client is currently connected: the persistent Codex server was running, but no ChatGPT main process was present at the time of inspection.

## Bottom line

The selected declarative source is the CriomOS root flake's pinned `CriomOS-home` revision `90a12633cc60148b62bc47fd44957e6165727094`, not the dirty Home working copy. That pinned source produced the active ChatGPT package `26.831.21537` and Codex package `0.152.1`.

The active ChatGPT wrapper sets `CODEX_APP_SERVER_USE_LOCAL_DAEMON=1`, forces the Wayland launch flag, and unsets the direct CLI/private-pipe override variables. Its bundled `resources/codex` is linked to the same Codex `0.152.1` executable used by the persistent service. The active Home Manager generation also installs `codex-remote-control.service`, which is running and listening on the Codex Unix control socket.

Static inspection of the active `app.asar` shows the app-server configuration resolver reduced to `getConfigOverrides:()=>[]`, while legacy/private App Tools material remains in the bundle, including a serialized `mcp_servers.codex_app={command="",enabled=false}` fallback and thread/background code that synthesizes a disabled `mcp_servers.codex_app`. The newer working-copy patcher contains additional removal/request-sanitization logic, but it is not in the pinned revision and is not deployed.

## Declarative source selected

- `/git/github.com/LiGoldragon/CriomOS/flake.nix` pins `criomos-home.url` to `github:LiGoldragon/CriomOS-home/90a12633cc60148b62bc47fd44957e6165727094`.
- `/git/github.com/LiGoldragon/CriomOS/flake.lock` records the same `criomos-home` revision and its locked narHash.
- CriomOS-home's working copy is dirty at `438d70ff5f60`; it modifies `checks/desktop-app-support/default.nix` and `owned-agents/chatgpt/patch-asar.py` and has an untracked Python bytecode file. These changes are source evidence only. The active root pin remains `90a12633cc60`.
- In the selected Home source, `modules/home/profiles/min/agent-intercom.nix` takes `config.criomos.corePackages.codex` as `codexCliPackage`, passes it to the ChatGPT package, and enables the desktop surface when the user is medium-sized and the node behaves as an edge. The same source defines the user service with `codex app-server --remote-control --listen unix://`.
- `modules/home/core-packages.nix` defines `criomos.corePackages.codex` through `owned-agents/codex`; `modules/nixos/userHomes.nix` imports the Home module into the system Home Manager configuration.

## Installed and generated surfaces

The active Home Manager generation is:

`/nix/store/8cl8gr7xhkxbv3zm7vzn15mz0gnx3nh5-home-manager-generation`

Its generated files and active profile links show:

- `/home/li/.nix-profile/bin/chatgpt` -> `/nix/store/1yizxk7zmjhd7zzllrg88kz77gf1rhbf-chatgpt-26.831.21537/bin/chatgpt`.
- `/home/li/.nix-profile/bin/codex` -> `/nix/store/j7xbc7wppa4zrzb5d50s3jw05fvqgns3-codex/bin/codex`; `codex --version` reports `codex-cli 0.152.1`.
- The ChatGPT wrapper's generated script exports `CODEX_APP_SERVER_USE_LOCAL_DAEMON=1`, unsets `CODEX_CLI_PATH`, `CODEX_APP_SERVER_FORCE_CLI`, `CODEX_APP_SERVER_CLI_COMMAND`, and `CODEX_APP_TOOLS_PIPE_PATH`, then executes the unwrapped ChatGPT binary with `--ozone-platform=wayland`.
- `/nix/store/sggmyn0j99xypqala8vaqhhr5ghiq0f8-chatgpt-unwrapped-26.831.21537/lib/chatgpt/resources/codex` -> `/nix/store/vp307a51wwncdl5cd7a8mm3d1w1x5qj6-codex-0.152.1/bin/codex`; the link was inspected with `readlink -f`.
- The generated desktop entry is `/nix/store/8cl8gr7xhkxbv3zm7vzn15mz0gnx3nh5-home-manager-generation/home-files/.local/share/applications/chatgpt.desktop`, with `Exec=chatgpt %U` and `x-scheme-handler/codex` in its MIME types. The live entry and both MIME maps select `chatgpt.desktop` for `x-scheme-handler/codex`.
- `/home/li/.config/codex-desktop/electron-flags.conf` exists, but all flag lines are commented. No user Electron flag override is active.
- `/home/li/.codex/config.toml` contains an active `mcp_servers.agent-intercom` command pointing to the installed Agent Intercom package and an active `mcp_servers.node_repl` using ChatGPT's packaged Node REPL resources. Its `mcp_servers.cua_repl` entry is explicitly `enabled = false`. The `CODEX_CLI_PATH` seen there is inside the Node REPL MCP environment, not the persistent service environment.
- The installed browser native-messaging host metadata and `/home/li/.codex/plugins/cache/openai-bundled/browser/26.831.21537` are present. They are browser integration surfaces, not evidence of a desktop-to-Codex socket connection.

## Bundle-level wiring observed

The active ASAR is:

`/nix/store/sggmyn0j99xypqala8vaqhhr5ghiq0f8-chatgpt-unwrapped-26.831.21537/lib/chatgpt/resources/app.asar`

Read-only binary marker/context checks found:

- `getConfigOverrides:()=>[]` in the app-server configuration path.
- Multiple `mcp_servers.codex_app` references remain, including a disabled serialized fallback and disabled thread/background producer objects.
- `Codex app tools unavailable` remains as a fallback/warning marker.

This supports the classification “local shared app-server path active; old App Tools producer/fallback material still present but disabled or unresolved.” It does not prove what a running desktop client would request after launch.

## Services, processes, and sockets

`codex-remote-control.service` is currently loaded, enabled, and active/running. Its generated/live service file is:

`/home/li/.config/systemd/user/codex-remote-control.service`

The service executes:

`/nix/store/vp307a51wwncdl5cd7a8mm3d1w1x5qj6-codex-0.152.1/bin/codex app-server --remote-control --listen unix://`

with `WorkingDirectory=/home/li/primary`, `UMask=0077`, `Restart=always`, and `RestartSec=2s`. Its main PID at inspection was `1664375`; the filtered environment showed no `CODEX_CLI_PATH` or remote-control override variables.

The inspecting shell exposed `CODEX_REMOTE_CONTROL_DAEMON_AUTOSTART_DISABLED=1`, but that variable was not present in the user-manager environment or the service environment. It is therefore a caller/harness setting, not evidence that the active systemd service is disabled.

The relevant Unix listener was:

`/home/li/.codex/app-server-control/app-server-control.sock`

owned by the running `.codex-wrapped` Codex server. No ChatGPT-specific listener was found. The process listing showed Codex app-server and its code-mode/Node REPL children, including Node REPL helpers from the installed ChatGPT package, but no ChatGPT main `/lib/chatgpt/ChatGPT` process. Consequently there was no live desktop client process or established client connection to observe.

The companion `claude-remote-control.service` was also active. No `:18080` listener was present.

## Active, installed-but-inactive, and absent

Active now:

- Pinned ChatGPT desktop package/wrapper `26.831.21537`.
- Shared Codex executable `0.152.1`, linked into the ChatGPT resources and used by the running remote-control service.
- ChatGPT desktop entry and `x-scheme-handler/codex` MIME selection.
- `CODEX_APP_SERVER_USE_LOCAL_DAEMON=1` wrapper wiring and Wayland launch flag.
- Home Manager generated `codex-remote-control.service` and its Unix control socket.
- Active Codex config entries for Agent Intercom and Node REPL; `cua_repl` is explicitly disabled.

Installed or present but inactive/stale:

- The newer ASAR patch/check behavior in the dirty CriomOS-home working copy (request sanitization and removal of additional `codex_app` producers). It is not selected by the pinned root flake and is not in the active store generation.
- Comment-only `~/.config/codex-desktop/electron-flags.conf`.
- Old `~/.local/state/codex-desktop` state and `~/.cache/codex-desktop/launcher.log`; the launcher log was not opened because it may contain user data.
- Old `~/.config/openai-api-server-via-codex` PID/log files. No matching service, process, or listener remains.
- The old `cf0ed9-chatgpt-corrected.service` custom service is absent as a unit; its recent journal record shows a crash, not current activity.

Absent at inspection:

- A running ChatGPT main desktop process.
- `chatgpt.service`, `codex-desktop.service`, or `cf0ed9-chatgpt-corrected.service` user units.
- A legacy TCP API server on port `18080`.
- A `codex-raw` executable in the active profile.
- Evidence that ChatGPT completed a connection to the running Codex app-server during this snapshot.

## Recent safe log evidence and uncertainties

Narrow, filtered `journalctl --user` reads found:

- At approximately 17:48, `cf0ed9-chatgpt-corrected.service` exited with `SIGSEGV`/core-dump and was then unavailable as a current unit.
- Around 18:06–18:08, the prior Codex remote-control process was stopped, timed out during termination, killed by systemd, and replaced by the currently running service. The current service start completed successfully at approximately 18:08:18.

The app-server being alive is strong evidence that the persistent endpoint is installed and running. It is not evidence that the ChatGPT GUI was running or connected, because the GUI process was absent. Static ASAR markers also cannot distinguish code that is reachable from code retained only for compatibility. The stale launcher/API-server files were intentionally not opened beyond metadata, and no cookies, browser databases, authentication material, or transcript contents were inspected.

## Method and exact paths/commands

All inspection was read-only. Commands and paths used included:

```text
sed -n '1,240p' /home/li/primary/NON_MANAGEMENT_AGENTS.md
sed -n '1,240p' /home/li/primary/.agents/skills/child-flow/SKILL.md
sed -n '1,260p' /home/li/primary/.agents/skills/flow-evidence/SKILL.md
orchestrate 'Observe.Locks'
jj status
jj log -r '::@' -n 8
# from /git/github.com/LiGoldragon/CriomOS-home:
jj file show -r 90a12633cc60 owned-agents/chatgpt/patch-asar.py
jj file show -r 90a12633cc60 checks/desktop-app-support/default.nix
readlink -f /run/current-system /home/li/.nix-profile /home/li/.local/state/home-manager/gcroots/current-home
readlink -f /home/li/.nix-profile/bin/chatgpt /home/li/.nix-profile/bin/codex
nix-store -q --deriver /nix/store/1yizxk7zmjhd7zzllrg88kz77gf1rhbf-chatgpt-26.831.21537 /nix/store/j7xbc7wppa4zrzb5d50s3jw05fvqgns3-codex
nix-store -q --roots /nix/store/1yizxk7zmjhd7zzllrg88kz77gf1rhbf-chatgpt-26.831.21537 /nix/store/j7xbc7wppa4zrzb5d50s3jw05fvqgns3-codex
systemctl --user list-units --all
systemctl --user list-unit-files
systemctl --user show codex-remote-control.service -p LoadState -p ActiveState -p SubState -p FragmentPath -p UnitFileState -p MainPID -p ExecStart -p WorkingDirectory -p Restart -p RestartUSec
systemctl --user show chatgpt.service codex-desktop.service cf0ed9-chatgpt-corrected.service -p LoadState -p ActiveState -p FragmentPath
ps -eo pid,ppid,user,comm,args
pgrep -af '(chatgpt|ChatGPT)'
ss -xlpn
ss -ltnp
journalctl --user --since '2026-09-02 17:40' --until '2026-09-02 18:15' -o short-iso
journalctl --user -u codex-remote-control.service --since '2026-09-02 18:00' -o short-iso
grep -aob 'getConfigOverrides\|mcp_servers.codex_app\|Codex app tools unavailable' /nix/store/sggmyn0j99xypqala8vaqhhr5ghiq0f8-chatgpt-unwrapped-26.831.21537/lib/chatgpt/resources/app.asar
```

Source files additionally read for the declarative/configuration interpretation were `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/agent-intercom.nix`, `/git/github.com/LiGoldragon/CriomOS-home/modules/home/core-packages.nix`, `/git/github.com/LiGoldragon/CriomOS-home/owned-agents/chatgpt/default.nix`, `/git/github.com/LiGoldragon/CriomOS-home/owned-agents/chatgpt/unwrapped.nix`, `/git/github.com/LiGoldragon/CriomOS-home/owned-agents/codex/default.nix`, `/git/github.com/LiGoldragon/CriomOS/modules/nixos/userHomes.nix`, and `/home/li/.codex/config.toml` (selected non-secret MCP fields only).
