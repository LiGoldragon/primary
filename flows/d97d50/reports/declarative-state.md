# Declarative ChatGPT Desktop source-to-live boundary

Captured 2026-09-03 on `ouranos`. This is a read-only source/profile/package
inspection after flow `4ad49f`; no GUI launch, build, deployment, activation,
service restart, process kill, runtime edit, or conversation-data read was
performed.

## Directly witnessed current state

The fresh ordinary Lojix query for `goldragon/ouranos` ended at marker `3843`.
It identifies deployment `149` as the current user-environment activation:

```text
(149 149 (UserEnvironment.li goldragon ouranos UserEnvironment
 UserEnvironment.ActivateNow LiveActivation RequireImmutable
 Some.158aa4c99a16b9be4aa77a8fc00d79752e0b49ca)
 Some.(3806 3806) Completed Some.(3839 3839) Some.Succeeded)
```

The active user profile is `/home/li/.local/state/nix/profiles/home-manager`
-> `home-manager-998-link` ->
`/nix/store/d3q0z43zv3ig5n36j4fx2dm3dhd4m0j4-home-manager-generation`.
The profile link mtime is `2026-09-02 22:48:22 +0200`. Its `home-path` is
`/nix/store/zh4fnjv1660jn21bliz5gfb4ankh08i0-home-manager-path`.

Deployment `149` therefore directly witnesses the currently selected
immutable CriomOS consumer revision as
`158aa4c99a16b9be4aa77a8fc00d79752e0b49ca` (the commit is
`Accept Claude UUIDv5 flow IDs`). At that revision, `CriomOS/flake.nix` pins
CriomOS-home to
`3e4e7a9bf96f1ab4d1cc59539aaab51ed61c2b96`; its lock entry records narHash
`sha256-4RGI0ujMH55xVSW29Ks6mWJ0tW0WhYphtcbtZcTEVJ8=`. These are the live
user-environment selections, not an inference from the local checkout.

The host is separately unchanged at the Lojix-current deployment `138`,
source revision `7cd12262874fc5f6c1ed133dc3ef56c669d29959`, with
`/run/current-system` ->
`/nix/store/sd0h59z66mggbqnnd5r8am5ai3hbbd34-nixos-system-ouranos-26.11.20260813.0e251e2`.

The active executable chain is directly witnessed as:

```text
/home/li/.nix-profile/bin/chatgpt
  -> /nix/store/a2nvjsivkzqq957c8wjr3i260v6d0721-chatgpt-26.831.21537/bin/chatgpt
  -> /nix/store/p3vjdpavgmgqv92wga4palispkbyw17j-chatgpt-unwrapped-26.831.21537/bin/chatgpt
  -> codex-launcher -> ChatGPT
```

The installed package and vendor metadata both identify version
`26.831.21537`. The x86_64 archive source in the selected Home source is
`https://persistent.oaistatic.com/codex-app-prod/linux/deb/pool/main/c/chatgpt/chatgpt_26.831.21537_amd64.deb`
with SRI hash
`sha256-XBVu8qLgKRWW0HuuhmDvTwt0jfO6+Rv8ko97XjxhCxE=`. The active packaged
ASAR is a read-only regular file, size `292435829`, SHA-256
`9745ec1195897c019533d08e8415ab81a3c4e59e845403fdfea42ce1272fe954`.
`resources/codex` is a read-only regular executable, size `255505120`, not a
Nix symlink. The active XDG desktop entries point to the same unwrapped
package's desktop file, whose `Exec` is `chatgpt %U`.

The generated outer wrapper is directly observed as:

```sh
exec "/nix/store/p3vjdpavgmgqv92wga4palispkbyw17j-chatgpt-unwrapped-26.831.21537/bin/chatgpt" \
  ${NIXOS_OZONE_WL:+${WAYLAND_DISPLAY:+--ozone-platform=wayland}} \
  --ozone-platform=wayland "$@"
```

The actual shell environment has `XDG_SESSION_TYPE=wayland`,
`WAYLAND_DISPLAY=wayland-1`, `DISPLAY=:0`, and an empty `NIXOS_OZONE_WL`, so
the current invocation contributes one unconditional
`--ozone-platform=wayland` flag. No `CODEX_APP_SERVER_USE_LOCAL_DAEMON`,
`CODEX_CLI_PATH`, `CODEX_APP_SERVER_FORCE_CLI`,
`CODEX_APP_SERVER_CLI_COMMAND`, or `CODEX_APP_TOOLS_PIPE_PATH` assignment is
present in the generated outer wrapper.

## Change since flow 4ad49f

Flow `4ad49f` directly recorded user deployment `148`, CriomOS
`663fefb70f9962c6751fd0d87b07f8cfef01ef9e`, Home `c025a681df31d55b9035364c01e2f6c8d7b59c1c`, and active generation `997` at
`/nix/store/hli4cf0csmxsh3364aq0qdh8klvbalzi-home-manager-generation`.
The current witness shows a real source/profile change: deployment `149`
and generation `998` replaced those selections with CriomOS `158aa4c…` and
Home `3e4e7a9…`.

The CriomOS diff from `663fefb…` to `158aa4c…` is limited to
`ARCHITECTURE.md`, `UPGRADES.md`, `checks/lojix-ownership/default.nix`,
`flake.nix`, and `flake.lock`; the relevant change in `flake.nix` is the Home
pin from `c025a…` to `3e4e7a9…` (the lock also moves the Harness input). The
Home package/check/module file object IDs are exactly equal at both revisions:

```text
owned-agents/chatgpt/default.nix       8023ed9cc1029c355013b0dac99753d168ec76fd
owned-agents/chatgpt/unwrapped.nix     48ee1bb6d50f2d4828e261ca65b7f4ccce43107d
checks/desktop-app-support/default.nix 1591cad183b2284314ae12534cdb4db5d68bcbad
modules/home/profiles/min/agent-intercom.nix
                                         ed6396d700f071d028ff58209c8c7c60624924e4
```

The generation-997 and generation-998 `home-path/bin/chatgpt` links resolve
to the exact same wrapper store path, and the active wrapper/package paths and
hashes above are unchanged from the `4ad49f` live witness. Thus the live
profile changed generation and consumer pin, but did not change the ChatGPT
package implementation or produced ChatGPT package.

The local source checkouts are not themselves the live selector: the local
CriomOS checkout is detached at `663fefb…` while its `origin/main` is
`158aa4c…`; the local Home checkout is detached at an unrelated fixture
revision while its `main` is `c025a…` and `origin/main` is `3e4e7a9…`. The
Lojix record plus the immutable source's own flake pin are the authority for
the live selection.

## Package/check inspection and plausible causes

The ChatGPT package source has a deliberately thin outer wrapper. It adds the
conditional Wayland flag and the caller-provided `commandLineArgs`, then links
the package `share` tree. The profile factory supplies
`commandLineArgs = "--ozone-platform=wayland"`. In a session with
`NIXOS_OZONE_WL` set, the wrapper would pass the same Wayland flag twice; the
current environment does not set that variable. Duplicate Electron flags are
a plausible wrapper hypothesis but are not a witnessed cause, and the prior
flow saw the real Electron process tree survive more than five seconds with
this package.

The unwrapped derivation copies the vendor `usr/lib/chatgpt` tree, retains the
vendor ASAR and bundled `resources/codex`, patches ELF loading, and wraps the
vendor `ChatGPT` executable with `wrapGAppsHook3` plus a PATH prefix for
`coreutils` and `xdg-utils`. The generated binary wrapper directly contains
two `GIO_EXTRA_MODULES` prefixes and that PATH prefix. Qt5 and Qt6 shim RPATHs
are added in `postFixup`. These Nix runtime adaptations are the only visible
package-owned execution surface that could plausibly affect an Electron
window that appears and then exits, but static inspection does not isolate any
one of them as the cause. The vendor ASAR itself is byte-identical, excluding
the prior ASAR sanitizer as the current cause.

The durable `desktop-app-support` check verifies exact ASAR and bundled-Core
equality against an independently fetched archive, runs the retained Core
privately through `--version` and stdio app-server EOF, and probes the outer
wrapper using a fake unwrapped executable with inherited vendor variables.
It does not execute the real `ChatGPT` GUI, observe an Electron process
lifetime, collect a crash/exit status, or test authenticated initialization.
Therefore a green check cannot currently explain a window-then-exit failure.
The prior live witness observed a bounded healthy Electron process tree and
then self-exit, while explicitly leaving the immediate exit cause unknown.

## Source write set decision

No fix is evidenced by this inspection, so there is no justified source write
set. In particular, upgrading the pinned archive, changing Wayland flags,
changing ELF/GApps wrapping, or adding a GUI-lifetime check would each be a
material compatibility or behavior decision requiring explicit authority and
an actual runtime witness. If the caller later authorizes diagnosis work, the
smallest candidate inspection surface is `owned-agents/chatgpt/default.nix`,
`owned-agents/chatgpt/unwrapped.nix`, and
`checks/desktop-app-support/default.nix`; no change is proposed here.

## Sources

- [Flow 4ad49f live stock Desktop witness](/home/li/primary/flows/4ad49f/witnesses/live-stock-desktop.md:1)
- [Flow 4ad49f system integration report](/home/li/primary/flows/4ad49f/reports/system-integration.md:1)
- [CriomOS flake at live revision](/git/github.com/LiGoldragon/CriomOS/flake.nix:33)
- [CriomOS-home ChatGPT wrapper source](/git/github.com/LiGoldragon/CriomOS-home/owned-agents/chatgpt/default.nix:17)
- [CriomOS-home ChatGPT package source](/git/github.com/LiGoldragon/CriomOS-home/owned-agents/chatgpt/unwrapped.nix:55)
- [CriomOS-home Desktop support check](/git/github.com/LiGoldragon/CriomOS-home/checks/desktop-app-support/default.nix:1)
- [CriomOS-home profile factory](/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/agent-intercom.nix:20)
- Fresh ordinary Lojix `Query.ByNode.(goldragon ouranos None)` and `Query.ByDeployment.(149)` outputs.
- Fresh profile symlink, package metadata, wrapper, ASAR/Core hash, and read-only source-diff observations described above.
