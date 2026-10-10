# Witness — Zeus user environments redeployed onto the rolled-back line

Flow db267d. Method: direct execution of the commands below from ouranos
(the operator host) against Lojix's sockets and against Zeus over SSH.
Every reply, terminal record and log excerpt below is quoted from actual
output. Nothing here is inferred from a previous run.

Target line:

- CriomOS-home `main` = `ed958211e8bfaa4384aca6622d92bc9bdb429fa1`
- CriomOS `main` = `bc3c4917b5df7b4842bd12996ff46926476cdcd8` (call it `$R`)

Both confirmed present on `origin` before any deployment:

```sh
cd /git/github.com/LiGoldragon/CriomOS      && git fetch origin && git rev-parse origin/main
cd /git/github.com/LiGoldragon/CriomOS-home && git fetch origin && git rev-parse origin/main
```

```
bc3c4917b5df7b4842bd12996ff46926476cdcd8
ed958211e8bfaa4384aca6622d92bc9bdb429fa1
```

Proposal source is an existing absolute regular non-symlink file:
`-rw-r--r-- 1 li users 5163 Sep  1 14:12 /git/github.com/LiGoldragon/goldragon/proposal.datom`.

## 1. Node identity check (before any state change)

```sh
ssh -o BatchMode=yes root@zeus.goldragon.criome 'hostname; cat /etc/machine-id; readlink -f /run/current-system; ls -l /nix/var/nix/profiles/system; df -h /nix/store | tail -1; readlink -f /home/bird/.local/state/nix/profiles/home-manager; readlink -f /home/li/.local/state/nix/profiles/home-manager'
```

```
zeus
c3d2385e2078489cb60b558135493b78
/nix/store/kgg7yk3b22w0dakn9sz3l6nz23rcw5ly-nixos-system-zeus-26.11.20260813.0e251e2
lrwxrwxrwx 1 root root 14 Sep  6 14:47 /nix/var/nix/profiles/system -> system-72-link
/dev/nvme0n1p2  468G  411G   34G  93% /nix/store
/nix/store/7hnqikaqghyd8a5fxdq3778hy933z3ii-home-manager-generation
/nix/store/aicm5x2lc58k56r22gh9y9hh4k7g0jpc-home-manager-generation
```

`lojix 'Query.ByNode.(goldragon zeus None)'` records generation 207 as the
`Current` `CompleteHost` for logical node `goldragon`/`zeus`, artifact
`/nix/store/kgg7yk3b22w0dakn9sz3l6nz23rcw5ly-nixos-system-zeus-26.11.20260813.0e251e2`.
That is byte-identical to live `/run/current-system` above, so the logical
node and the activation destination identify the same machine. Proceeded.

System generation 72 was not touched. Nothing in this work required a host
redeployment, and none was performed. No reboot was performed.

Store stayed at 93% (34G free) throughout. No copy failed for space, so
nothing was deleted.

## 2. Deployments through Lojix

All owner requests via `meta-lojix` on `LOJIX_OWNER_SOCKET`, all queries via
`lojix` on `LOJIX_ORDINARY_SOCKET`. Request form (bird, `Realize`; the others
differ only in user, transport, output selector and action):

```sh
R=bc3c4917b5df7b4842bd12996ff46926476cdcd8
meta-lojix "Deploy.UserEnvironment.(goldragon zeus bird /git/github.com/LiGoldragon/goldragon/proposal.datom github:LiGoldragon/CriomOS?rev=$R (ssh-ng://bird@zeus.goldragon.criome bird@zeus.goldragon.criome) Horizon (homeConfigurations.bird.activationPackage) HomeManagerNixProfileV1 Realize RequireImmutable Some.@/etc/nix/machines [])"
```

li's requests use `(ssh-ng://li@zeus.goldragon.criome li@zeus.goldragon.criome)`
and `(homeConfigurations.li.activationPackage)`.

| Deployment | Subject | Action | Terminal |
|---|---|---|---|
| 222 | bird | `Realize` | `Some.Succeeded` |
| 223 | li | `Realize` | `Some.Succeeded` |
| 224 | li | `SetProfile` | `Some.Succeeded` |
| 225 | li | `ActivateNow` | `Some.Succeeded` |
| 226 | bird | `SetProfile` | `Some.Failed.(Activate ActivationFailed)` |

Admissions and terminal records, quoted:

```
DeployAccepted.(222 (5847 5847))
Queried.([] [(222 222 (UserEnvironment.bird goldragon zeus UserEnvironment UserEnvironment.Realize ProfileOnly RequireImmutable Some.bc3c4917b5df7b4842bd12996ff46926476cdcd8) Some.(5847 5847) Completed Some.(5878 5878) Some.Succeeded)] (5888 5888))

DeployAccepted.(223 (5852 5852))
Queried.([] [(223 223 (UserEnvironment.li goldragon zeus UserEnvironment UserEnvironment.Realize ProfileOnly RequireImmutable Some.bc3c4917b5df7b4842bd12996ff46926476cdcd8) Some.(5852 5852) Completed Some.(5884 5884) Some.Succeeded)] (5888 5888))

DeployAccepted.(224 (5889 5889))
Queried.([] [(224 224 (UserEnvironment.li goldragon zeus UserEnvironment UserEnvironment.SetProfile ProfileOnly RequireImmutable Some.bc3c4917b5df7b4842bd12996ff46926476cdcd8) Some.(5889 5889) Completed Some.(5922 5922) Some.Succeeded)] (5926 5926))

DeployAccepted.(225 (5927 5927))
Queried.([] [(225 225 (UserEnvironment.li goldragon zeus UserEnvironment UserEnvironment.ActivateNow LiveActivation RequireImmutable Some.bc3c4917b5df7b4842bd12996ff46926476cdcd8) Some.(5927 5927) Completed Some.(5960 5960) Some.Succeeded)] (5964 5964))

DeployAccepted.(226 (5965 5965))
Queried.([] [(226 226 (UserEnvironment.bird goldragon zeus UserEnvironment UserEnvironment.SetProfile ProfileOnly RequireImmutable Some.bc3c4917b5df7b4842bd12996ff46926476cdcd8) Some.(5965 5965) Failed Some.(5989 5989) Some.Failed.(Activate ActivationFailed))] (5993 5993))
```

Note on query syntax, recorded because it cost time: `Query.ByDeployment`
requires a parenthesis block. `lojix 'Query.ByDeployment.222'` is refused
with `(CliRejected [DOTOS request did not decode: expected … to be a
parenthesis block])`. The accepted form is `lojix 'Query.ByDeployment.(222)'`.

### Realized artifacts match the derivations named in the brief

```sh
nix-store -q --outputs /nix/store/c99v0bygd9g8dkiq7js9gf2iy7nk3a0n-home-manager-generation.drv   # bird
nix-store -q --outputs /nix/store/jk3391v76mf5d514cd2mpp9fnzc5mfks-home-manager-generation.drv   # li
```

```
/nix/store/x3k5s0nbg7y6l20rpxvn3r0cv70ifpl8-home-manager-generation
/nix/store/lmib8nnss60cg1pim9xdbi6vyakfxi18-home-manager-generation
```

### bird's transport gap, re-witnessed on this line

```sh
ssh -o BatchMode=yes -o ConnectTimeout=10 bird@zeus.goldragon.criome 'echo BIRD_SSH_OK'
```

```
bird@zeus.goldragon.criome: Permission denied (publickey,keyboard-interactive).
```

Unchanged from this morning. Lojix reaches a user environment by SSHing as
that user with the operator (li) key; that key is in
`/etc/ssh/authorized_keys.d/li` and not in bird's. So bird's `Realize`
(222) succeeds — a build needs no target SSH — and her `SetProfile` (226)
fails, with Lojix collapsing the stage failure to
`Some.Failed.(Activate ActivationFailed)` and discarding stderr. One
`SetProfile` attempt was made to record that the gap persists on this line;
`ActivateNow` was not attempted, since its outcome is determined by the same
gap and a second failed ledger entry would add nothing.

### bird activated by the psyche-authorised root route

The closure Lojix realised (222) was already present on Zeus:

```sh
ssh -o BatchMode=yes root@zeus.goldragon.criome 'ls -d /nix/store/x3k5s0nbg7y6l20rpxvn3r0cv70ifpl8-home-manager-generation'
```

```
/nix/store/x3k5s0nbg7y6l20rpxvn3r0cv70ifpl8-home-manager-generation
```

Activation, run as bird from a single non-interactive root SSH command that
exits:

```sh
ssh -o BatchMode=yes -o ConnectTimeout=20 root@zeus.goldragon.criome 'su -s /bin/sh bird -c "export HOME=/home/bird USER=bird XDG_RUNTIME_DIR=/run/user/1000 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus PATH=/run/current-system/sw/bin:/usr/bin:/bin; /nix/store/x3k5s0nbg7y6l20rpxvn3r0cv70ifpl8-home-manager-generation/activate"'
```

It ran to completion — `Activating dconfSettings` through
`Activating updateUserDesktopDatabase`, with `Stopping units:
chroma-daemon.service` and `Starting units: chroma-daemon.service,
criomos-ui-priority.service, orchestrate-nexus.service,
set-SSH_AUTH_SOCK.service`. It reported the **pre-existing** degraded unit
`orchestrate-nexus.service` ("The user systemd session is degraded … 
Attempting to continue anyway") and continued. That unit was already
degraded before this activation; it is recorded in this flow's earlier
witness of 17:14 in the same words. This activation did not introduce it.

Live result:

```sh
readlink -f /home/bird/.local/state/nix/profiles/home-manager
```

```
/nix/store/x3k5s0nbg7y6l20rpxvn3r0cv70ifpl8-home-manager-generation
```

New profile links written at 19:08:

```
lrwxrwxrwx 1 bird users 51 Sep  6 17:14 profile-254-link -> /nix/store/g99fkafq0qgxi0whnxa72d78mwnazmg2-profile
lrwxrwxrwx 1 bird users 51 Sep  6 17:14 profile-255-link -> /nix/store/iav407q2xw0k8ckfw6djck9h4nr3hw69-profile
lrwxrwxrwx 1 bird users 51 Sep  6 19:08 profile-256-link -> /nix/store/g99fkafq0qgxi0whnxa72d78mwnazmg2-profile
lrwxrwxrwx 1 bird users 51 Sep  6 19:08 profile-257-link -> /nix/store/a5rxixprrlirlvxb62sp39p84gznl9rx-profile
```

li's live profile after deployment 225:

```
/nix/store/lmib8nnss60cg1pim9xdbi6vyakfxi18-home-manager-generation
```

## 3. Verifying bird's Claude Desktop

### The new generation supplies the same app build as the working one

```sh
ssh … root@zeus 'readlink -f /nix/store/<gen>/home-path/bin/claude-desktop'
```

```
old gen 7hnqikaqghyd8a5fxdq3778hy933z3ii → /nix/store/ynk1b2pn8vq2blsmmi3rmjsx1dd2qn5g-claude-desktop-1.46388.2/bin/claude-desktop
new gen x3k5s0nbg7y6l20rpxvn3r0cv70ifpl8 → /nix/store/ynk1b2pn8vq2blsmmi3rmjsx1dd2qn5g-claude-desktop-1.46388.2/bin/claude-desktop
```

`diff` of the two generations' `home-path/bin` listings is empty. The
`claude` binary CCD invokes is also identical across the two generations:
`/nix/store/i9inl75s81bnmaczw8d89875z4g4i4n9-claude-code-2.1.261/bin/claude`.

Resolved through bird's live profile after activation:

```sh
readlink -f /home/bird/.nix-profile/bin/claude-desktop
→ /nix/store/ynk1b2pn8vq2blsmmi3rmjsx1dd2qn5g-claude-desktop-1.46388.2/bin/claude-desktop
```

That is the known-working build named in the brief.

### asar header marks the native modules unpacked

Parsed from the `app.asar` header. The store path is content-addressed and
present on both hosts; the two copies were confirmed byte-identical before
trusting the local parse:

```sh
sha256sum …/resources/app.asar        # on ouranos and on zeus
```

```
6c2923d4bcd12b8e762d67e6fa531125a2b66334417f4c1385869d156347bd48   (ouranos)
6c2923d4bcd12b8e762d67e6fa531125a2b66334417f4c1385869d156347bd48   (zeus)
```

Header entry for `node_modules/node-pty/prebuilds/linux-x64/pty.node`:

```
{'size': 75976, 'unpacked': True, 'integrity': {'algorithm': 'SHA256', 'hash': '123792d8f22f36d519b21dfb6f4b716f9b18b9e579085ea2840d0773d88d35fd', 'blockSize': 4194304, 'blocks': ['123792d8f22f36d519b21dfb6f4b716f9b18b9e579085ea2840d0773d88d35fd']}}
```

Three entries carry `unpacked: true`:

```
/node_modules/@ant/claude-native/claude-native-binding.node
/node_modules/node-pty/prebuilds/linux-x64/pty.node
/resources/github-mcp/github-mcp-server
```

### pty.node is a real file at the unpacked path

```
-r--r--r-- 5 root root 84799 Jan  1  1970 /nix/store/ynk1b2pn8vq2blsmmi3rmjsx1dd2qn5g-claude-desktop-1.46388.2/lib/claude-desktop/resources/app.asar.unpacked/node_modules/node-pty/prebuilds/linux-x64/pty.node
```

The on-disk size exceeds the header's recorded 75976 because Nix patchelfs
the unpacked copy; asar integrity covers packed content, not unpacked files.

### The app was not restarted, and why

The brief asked for a restart "so she picks up the new generation". The
evidence above shows that premise does not hold here: the new generation
supplies a **byte-identical** `claude-desktop` and a byte-identical
`claude-code` to the generation bird's already-running process was launched
from. The running main process is:

```sh
tr '\0' '\n' < /proc/43261/cmdline | head -1
→ /nix/store/ynk1b2pn8vq2blsmmi3rmjsx1dd2qn5g-claude-desktop-1.46388.2/lib/claude-desktop/claude-desktop
```

It is already executing exactly the code the new generation provides, so a
restart could not cause it to "pick up" anything. Meanwhile bird was
actively working in the app — `main.log` carried a permission response at
19:07:29, a git-worker diff at 19:07:55, and a healthy CCD cycle at
19:09:21. Killing that process would have destroyed live work for no gain,
so it was left running. This is a deliberate deviation from the brief's
step 3, taken on the evidence, and is flagged here rather than quietly
skipped. If the main flow wants the restart performed regardless, it is one
command away.

### Log evidence — including a positive PTY spawn

bird's current app instance started at ~17:30–17:31 (the 17:15 instance
quit at 17:30:31 with `Running onQuitCleanup: pty-host-shutdown`), running
the `ynk1b2pn8…` build. Log is `/home/bird/.config/Claude/logs/main.log`.

Restricted to lines at or after 17:31 — i.e. the whole life of the current
instance, about 100 minutes of real use:

```sh
grep -a 'LOCAL OVERRIDE'      → nothing
grep -a 'pty-host'            → nothing
```

`[CCD] LOCAL OVERRIDE: declared binary unavailable` does not appear. No
`[pty-host] worker exited` line appears.

Every `worker exited` line in the entire log, with timestamps:

```
2026-09-06 15:02:10 [error] [pty-host] worker exited (1) with 1 live PTY(s) before a real spawn ack; backing off 600000ms before refork
2026-09-06 15:43:22 [info]  [heavy-work] worker exited (0); will refork on next request
2026-09-06 15:53:05 [error] [pty-host] worker exited (1) with 1 live PTY(s) before a real spawn ack; backing off 30000ms before refork
2026-09-06 17:14:58 [info]  [git] worker exited (0); will refork on next request
2026-09-06 17:30:31 [info]  [git] worker exited (0); will refork on next request
```

The only two `[pty-host]` failures are at 15:02 and 15:53, both before the
repair. The later two are ordinary `[git]` worker exits with status 0.

Attributing every native-module failure in the log to a build:

```sh
grep -a 'Failed to load native module' -A2 | grep -oE '/nix/store/[a-z0-9]{32}-claude-desktop[^/]*' | sort | uniq -c
```

```
6 /nix/store/80i8csx7km7jjvw6gn6frn23fcvzikz0-claude-desktop-1.40609.0
1 /nix/store/y08k9q372w81jyczclkpji77c0rw5ihn-claude-desktop-1.46388.2
```

Both are superseded builds. Searching the whole log for any line mentioning
`ynk1b2pn8` together with `pty-host` or `Failed to load native` returns
**nothing**. The working build has never produced a native-module failure.

**Positive PTY spawn — the gap the earlier witness left open is now
closed.** The current instance started and cleanly tore down two real shell
PTYs:

```
2026-09-06 17:31:51 [info] LocalSessions.startShellPty: sessionId=local_f83bb69c-e5c2-4ed9-b1bd-b9a4bd1376e4, cols=80, rows=24
2026-09-06 17:32:00 [info] Stopping shell PTY for session local_f83bb69c-e5c2-4ed9-b1bd-b9a4bd1376e4
2026-09-06 17:32:00 [info] Shell PTY for session local_f83bb69c-e5c2-4ed9-b1bd-b9a4bd1376e4 exited (stale — already replaced)
2026-09-06 17:32:01 [info] LocalSessions.stopShellPty: sessionId=local_f83bb69c-e5c2-4ed9-b1bd-b9a4bd1376e4
2026-09-06 17:43:40 [info] LocalSessions.startShellPty: sessionId=local_2fce7262-8362-4139-8ea5-e8afe8c09d35, cols=80, rows=24
```

A `startShellPty` forks the pty-host worker and loads `pty.node`. On the
broken builds that is exactly where the worker died with `worker exited (1)
with 1 live PTY(s) before a real spawn ack`. Here both spawns proceeded and
the sessions ran; session `local_2fce7262-…` was still logging
`[CCD CycleHealth] healthy cycle` at 19:09:21. This is a positive spawn, not
merely the absence of a startup crash.

Sessions warm successfully:

```
2026-09-06 17:15:15 [info] [CCD] Session local_2a5140ca-f237-4f4c-a94d-990fe889177c warmed successfully in 99ms
2026-09-06 17:31:00 [info] [CCD] Session local_2a5140ca-f237-4f4c-a94d-990fe889177c warmed successfully in 134ms
2026-09-06 17:31:54 [info] [CCD start-timing] local_f83bb69c-… total_to_assistant=4356ms … online=true
2026-09-06 17:43:45 [info] [CCD start-timing] local_2fce7262-… total_to_assistant=6555ms … online=true
```

**Verdict: bird's Claude Desktop is working.** The build is correct, the
native module is unpacked and present, the app is running from it, real PTYs
spawn, sessions warm, and the two failure signatures the brief named are
absent for the entire life of the current instance.

Stated honestly as unproven: the PTY spawns quoted above happened at 17:31
and 17:43, i.e. under this same app build but before tonight's activation
wrote profile-257 at 19:08. Since the activation changed neither the
`claude-desktop` build nor the `claude-code` binary, there is no mechanism by
which it could have regressed them — but no new PTY has been spawned in the
minutes since 19:08, so that is an argument from identity of inputs rather
than a fresh observation.

## 4. Lojix state and live state, stated separately

**Lojix state.** `Current` `UserEnvironment` records for `goldragon`/`zeus`:

```
(225 225 goldragon zeus UserEnvironment LiveActivation Current Some./nix/store/lmib8nnss60cg1pim9xdbi6vyakfxi18-home-manager-generation Some.bc3c4917b5df7b4842bd12996ff46926476cdcd8)
(167 167 goldragon zeus UserEnvironment LiveActivation Current Some./nix/store/dhwq1j6ndp5kh47nqasmfblv2w93h82d-home-manager-generation Some.eefa86f117ee173670b82b49f1a60e86b94fac27)
```

li is at deployment/generation 225 on the new line, `LiveActivation`,
`Some.Succeeded`, source `bc3c4917…`. bird's ledger is **unchanged and still
stale**: generation 167, artifact
`/nix/store/dhwq1j6ndp5kh47nqasmfblv2w93h82d-home-manager-generation`, source
`eefa86f117ee…`, left there by flow 0384e0. Her only records on this line are
222 (`Realize`, `Succeeded`) and 226 (`SetProfile`, `Failed`). Tonight's work
did not move her `Current`, and could not have: her activation did not go
through Lojix.

**Live state.**

```
/home/bird/.local/state/nix/profiles/home-manager → /nix/store/x3k5s0nbg7y6l20rpxvn3r0cv70ifpl8-home-manager-generation
/home/li/.local/state/nix/profiles/home-manager   → /nix/store/lmib8nnss60cg1pim9xdbi6vyakfxi18-home-manager-generation
```

li's live state matches her Lojix record exactly. **bird's live state is
three generations ahead of what Lojix believes** — Lojix says
`dhwq1j6n…` at `eefa86f1…`, the machine says `x3k5s0nb…` at `bc3c4917…`.
That divergence is caused entirely by the authorized-keys gap and will
persist until the operator key is added to bird's authorized keys in the OS
source and she is redeployed through Lojix. Nothing in this witness closes
it.

The host itself was not redeployed: system generation 72,
`kgg7yk3b22w0…`, unchanged, matching Lojix generation 207.

## 5. Root-session verification on Zeus

Every SSH invocation in this witness was a single non-interactive command
that exits. bird was reached only as `su -s /bin/sh bird -c …`, never
`su - bird`. No interactive shell was opened. No reboot was performed.

Final check, quoted verbatim:

```sh
ssh -o BatchMode=yes root@zeus.goldragon.criome 'echo "=== who ==="; who; echo "(empty above = no login sessions)"; echo "=== loginctl list-sessions ==="; loginctl list-sessions'
```

```
=== who ===
(empty above = no login sessions)
=== loginctl list-sessions ===
SESSION  UID USER SEAT  LEADER CLASS         TTY  IDLE SINCE
    125    0 root -     91686  manager-early -    no   -
    126    0 root -     91718  user          -    no   -
      3 1000 bird seat0 2071   user          tty1 no   -
      4 1000 bird -     2139   manager       -    no   -

4 sessions listed.
```

`who` is empty: **no root login session of mine remains.** Sessions 125/126
are the transient root systemd user manager that each SSH command spawns and
tears down — they carry no seat and no TTY. That they are per-invocation and
not a lingering login was confirmed by running the check a second time:

```
125    0 root -     91686 manager-early -    no -
127    0 root -     91745 user          -    no -
  3 1000 bird seat0 2071  user          tty1 no -
  4 1000 bird -     2139  manager       -    no -
```

Session 126 (leader 91718) is gone and replaced by 127 (leader 91745); on an
earlier check the pair was 92/93 with leaders 40794/40841. bird's sessions 3
and 4 are her own tty1 login, untouched throughout.

## 6. Constraints observed

- Flow 542442 was not woken, its worktrees were not touched, and its locks
  were not released. No lock collision occurred: the only lock taken was
  Orchestrate 955, over this witness path alone, released after writing.
- `checks/lojix-ownership` was not touched and was not evaluated; deployment
  does not evaluate `checks`.
- No reboot, and no runtime mutation beyond the authorized bird activation.
