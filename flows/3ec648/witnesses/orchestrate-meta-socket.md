# Orchestrate meta socket: wrapper and live Nexus disagree

## Method

Read-only observation of the live system on 2026-10-02 (no restart, no Configure, no profile change), reading the source in `/git/github.com/LiGoldragon/orchestrate` (main 9070cbb8, 0.35.0) and `/git/github.com/LiGoldragon/CriomOS-home` (main 0025894f), and a reproduction in the semi-sandbox `capsule.sh` (create, start, enter, stop, teardown) using the same 0.35.0 binary the live Nexus runs.

## Live observation

- `~/.nix-profile/bin/orchestrate-meta` exports `ORCHESTRATE_META_SOCKET="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/orchestrate-nexus/orchestrate-meta.sock"`. `~/.nix-profile/bin/orchestrate` exports `ORCHESTRATE_SOCKET=...orchestrate.sock` unconditionally, so it overwrites a value the caller set.
- `ss -xlp` shows that pid 1944 (`orchestrate-nexus` 0.35.0, `/nix/store/6ynfv0hy...-orchestrate-0.35.0`, up since 2026-09-26) listens on `/run/user/1001/orchestrate-nexus/orchestrate.sock` and `/run/user/1001/orchestrate-nexus/meta-orchestrate.sock`. The runtime directory holds no `orchestrate-meta.sock`.

## Source

- `crates/orchestrate-nexus/src/defaults.rs` sets `META_SOCKET_FILE = "orchestrate-meta.sock"`. The CriomOS-home wrapper (`modules/home/profiles/min/orchestrate.nix`) and its check `checks/orchestrate-wrapper-fallback` use the same name.
- UPGRADES.md 0.33.1 to 0.34.0, "The meta socket's default name is now `orchestrate-meta.sock`", follows the ruling that the meta CLI is `<component>-meta`. It states that a deployed store keeps binding `meta-orchestrate.sock` until a meta `Configure` moves it.
- The Nexus and both wrappers therefore already agree in source, and `orchestrate-meta.sock` is the designed name. The live store predates 0.34.0 and persists the legacy path. A fresh store binds the designed name. No code or name change was made. The README example still named `meta-orchestrate.sock`, and the UPGRADES note said that nothing outside the Nexus needed to change. Both were corrected.
- The wrappers are in CriomOS-home, not in the orchestrate repository, so the `ORCHESTRATE_SOCKET` honouring change was not made.

## Sandbox reproduction (0.35.0 binary, fresh store under /tmp/cap3ec)

1. Fresh store: the Nexus bound `orchestrate-meta.sock`. Installed wrapper `orchestrate-meta 'Configure.{ «…/orchestrate.sock» «…/orchestrate-meta.sock» }'` returned `Configured.{ { …/orchestrate.sock …/orchestrate-meta.sock } True }` (exit 0).
2. Configure moved meta to `…/meta-orchestrate.sock`, which returned `Configured`. The running Nexus kept serving the old path.
3. Restart. The populated store resumed `meta-orchestrate.sock`. The installed wrapper returned `Unreachable.{ …/orchestrate-meta.sock «Unix socket I/O failed: Connection refused (os error 111)» }` (exit 1), which is the live state. The ordinary wrapper still returned `Observed.Locks.[]`.
4. Remediation: the direct client with `ORCHESTRATE_META_SOCKET=…/meta-orchestrate.sock` sent Configure back to `orchestrate-meta.sock` and got `Configured`. The wrapper was still `Unreachable` until restart.
5. Restart. The installed wrapper returned `Configured.{ … orchestrate-meta.sock } True` (exit 0).
6. Teardown removed `/tmp/cap3ec` and the sandbox. The unit is inactive.

Side observations: the capsule's `start` waits only for `orchestrate.sock` to exist. On a restart the stale file satisfies it at once, so `start` can return before the meta socket is bound. A stale `orchestrate-meta.sock` socket file left behind refuses connections rather than being absent. The `orchestrate` skill's curly-quote reason (`“…”`) was refused by the live 0.35.0 client (`Unreadable.Error.{ Composition [ 1 ] Arity.{ 4 10 } }`), and `«…»` was accepted.

## Live remediation (not performed; it reconfigures and restarts the live Nexus)

```sh
ORCHESTRATE_META_SOCKET=/run/user/1001/orchestrate-nexus/meta-orchestrate.sock \
  /nix/store/6ynfv0hywpwg8gpapyfh7zn0yqzdg52z-orchestrate-0.35.0/bin/orchestrate-meta \
  'Configure.{ «/run/user/1001/orchestrate-nexus/orchestrate.sock» «/run/user/1001/orchestrate-nexus/orchestrate-meta.sock» }'
systemctl --user restart orchestrate-nexus
```

No profile rebuild is needed.

## Landed

orchestrate main `d80a617f7e03` (docs only, no version bump): README example and the UPGRADES 0.34.0 note. `nix flake check --max-jobs 0` (MemoryMax=4G, 900 s) evaluated 17 checks, all already built, and passed.
