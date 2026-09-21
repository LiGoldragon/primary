# Mentci Web remote-check stall: bounded builder triage

**Read-only observation:** 2026-09-21 16:24–16:32 Mexico City time (22:24–22:32 UTC). **Source under test:** `mentci-web` branch `mentci-web-stage2-2c61af`, published revision `de937d77`. This report changes neither Mentci source nor network, Nix daemon, or the stopped VM guest.

## Result

The final Mentci check has **no compiler or test result**. Both recorded attempts reached the local Nix daemon, displayed only Crane evaluation warnings, and were interrupted after roughly 70 seconds without a derivation line. The exact wait operation during those attempts was not captured. At the later read-only check, the configured Prometheus remote-builder path and its local binary cache were unreachable, while the public cache worked. This is a present remote-route blocker and a plausible explanation for the stalls, **not proof** that the earlier wait was specifically an SSH connection, cache lookup, or remote slot.

## Evidence

| Boundary | Witness | Meaning / limit |
| --- | --- | --- |
| Source and attempts | Medium's exact worktree is `/home/li/wt/github.com/LiGoldragon/mentci-web/mind-medium-mentci-web-2c61af`. The command was `nix build --no-link -L --option max-jobs 0 --option fallback false .#checks.x86_64-linux.test`, twice after the final source changes. Recorded process IDs were `65679` and `27771`; output had two Crane placeholder-name evaluation warnings, then `interrupted by the user`. | No derivation dispatch, compiler failure, or test failure is in the captured output. Earlier 9/9 pass covered an earlier revision only. |
| Nix daemon | Ouranos journal: accepted trusted client at 16:24:23 and 16:26:33; each child was reaped after user interruption at 16:25:33 and 16:27:43. Daemon remained active. | Client-to-local-daemon worked. No daemon log identified the remote/cache wait point. |
| Configured routes | `builders = @/etc/nix/machines`; its exact builder is `ssh-ng://nix-ssh@prometheus.goldragon.criome` with six jobs. Substituters are `http://nix.prometheus.goldragon.criome` first, then `https://cache.nixos.org/`. `connect-timeout = 60`, `stalled-download-timeout = 300`; the command explicitly set max-jobs 0 and fallback false. | Configured remote path, not proof a slot was occupied or that Nix reached the SSH stage. A roughly 70-second wait is compatible with a 60-second connection timeout but is not a causal trace. |
| Current cache path, 16:30 | One bounded `curl` to configured Prometheus cache `/nix-cache-info` timed out after 7 seconds; public `cache.nixos.org/nix-cache-info` returned HTTP 200 in 0.33 seconds. | Public Internet/cache works from Ouranos; private cache is presently unreachable. No repeated cache requests were made. |
| Current builder path, 16:30 | One direct SSH to the configured Prometheus name timed out. A separate one-shot strict-host-key SSH to its previously leased USB IP `10.44.0.148` returned `No route to host`; neighbor entry was `INCOMPLETE`. Ouranos USB interface remained `UP,LOWER_UP` at `10.44.0.1/24`, with its NetworkManager shared profile connected. | Neither known route currently reaches the peer. Local USB carrier does not establish peer IP service. Exact peer-side cause is unknown; no blind retry or network change followed. |
| Existing alternate management path, 16:32 | Ouranos's already-connected `goldragon.criome` Wi-Fi had `10.18.0.102/24` and an on-link route to Prometheus AP `10.18.0.1`. One strict-host-key SSH to that known address returned `No route to host`; its neighbor entry was also `INCOMPLETE`. | Even the already configured Wi-Fi management route is not presently usable. A connection profile reporting connected does not prove AP bridge/IP response. No Wi-Fi connection or profile was changed. |

## One next action

The current Field/network owner needs a **peer-side or physical/console state witness** for Prometheus before choosing a repair: both known local IPv4 paths have unresolved neighbors, while the configured Ygg SSH times out. That does not identify whether the host, interface, bridge, radio, cable, or service is at fault, so no Ouranos-side software change is justified from this evidence. Once the peer responds, witness one strict-host-key builder handshake and `/nix-cache-info` response. Only then should Medium rerun one remote-only check of `de937d77`; do not redirect silently to local builds or another builder. The earlier Flow `Cargo.lock`/Git-fetch issue is a different project and does not diagnose this Mentci stall. The `microvm@vm-testing` guest remains stopped under its separate graph/parity gate.

## Sources

- Exact Mentci worktree and published revision: `/home/li/wt/github.com/LiGoldragon/mentci-web/mind-medium-mentci-web-2c61af` and remote bookmark `mentci-web-stage2-2c61af@origin`.
- Medium attempt records: bounded native session events at `2026-09-21T22:25:33Z` and `22:27:43Z`, plus Ouranos `nix-daemon.service` journal for 16:23–16:28 local.
- Read-only Ouranos checks at 22:29–22:32 UTC: `nix config show`, `/etc/nix/machines`, `curl --max-time 7` to the two configured caches, `getent`, `ip link/address/route/neigh`, `nmcli device status`, and three distinct one-shot SSH routes with strict host-key checking.
