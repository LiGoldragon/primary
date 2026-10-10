# Zeus Deployment Preflight

Flow: 0384e0
Date: 2026-09-06
Method: Direct observation from Ouranos via SSH, ICMP, DNS, nix store info, lojix ordinary socket query, and local file inspection.

## 1. REACHABILITY

### DNS resolution

```
$ getent hosts zeus.goldragon.criome
200:17f7:4fad:e50b:a50c:2048:2169:41f7 zeus.goldragon.criome
```

Resolves to Yggdrasil overlay address `200:17f7:4fad:e50b:a50c:2048:2169:41f7`.

### SSH connectivity

```
$ ssh -o StrictHostKeyChecking=yes -o BatchMode=yes root@zeus.goldragon.criome 'hostname'
ssh: connect to host zeus.goldragon.criome port 22: Connection timed out
EXIT: 255
```

### ICMP to resolved address

```
$ ping -c 1 -W 5 200:17f7:4fad:e50b:a50c:2048:2169:41f7
PING 200:17f7:4fad:e50b:a50c:2048:2169:41f7 (200:17f7:4fad:e50b:a50c:2048:2169:41f7) 56 data bytes

--- 200:17f7:4fad:e50b:a50c:2048:2169:41f7 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss, time 0ms

PING_EXIT: 1
```

### Stale address check

```
$ ping -c 1 -W 3 192.168.18.95
PING 192.168.18.95 (192.168.18.95) 56(84) bytes of data.

--- 192.168.18.95 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss, time 0ms

EXIT: 1
```

The stale address `192.168.18.95` also does not answer. Neither route reaches Zeus.

**Verdict: BLOCKED.** Zeus is unreachable at its resolved Yggdrasil address. SSH times out on port 22. The stale IPv4 `192.168.18.95` is also dead. The node appears to be powered off or disconnected from the overlay network.

## 2. NIX STORE

```
$ nix store info --store ssh-ng://root@zeus.goldragon.criome
Store URL: ssh-ng://root@zeus.goldragon.criome
ssh: connect to host zeus.goldragon.criome port 22: Connection timed out
error: failed to start SSH connection to 'zeus.goldragon.criome'
EXIT: 1
```

**Verdict: BLOCKED.** The ssh-ng channel that CopyClosure uses cannot reach Zeus. This is the same connectivity failure as check 1.

## 3. SAME MACHINE

Could not be verified. SSH does not connect, so the far-side hostname cannot be read.

Local hostname confirmed:

```
$ hostname
ouranos
```

**Verdict: BLOCKED.** Cannot verify the far-side identity because Zeus is unreachable.

## 4. DAEMON

### Service status

```
$ systemctl is-active lojix-daemon.service
active
```

### Socket paths and modes

```
$ ls -la /run/lojix/ordinary.sock /run/lojix/owner.sock
srw-rw---- 1 li users 0 Sep  4 18:17 /run/lojix/ordinary.sock
srw------- 1 li users 0 Sep  4 18:17 /run/lojix/owner.sock

$ stat -c '%a %F' /run/lojix/ordinary.sock /run/lojix/owner.sock
660 socket
600 socket
```

Ordinary socket mode 660 (decimal 432). Owner socket mode 600 (decimal 384). Both match the expected configuration.

### Ordinary socket query

```
$ LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock lojix 'Query.ByNode.(goldragon zeus None)'
```

Response received (abbreviated for readability; full output follows):

Current generation records for zeus:
- Generation 181: CompleteHost LiveActivation Current, store path `/nix/store/c3753yv0095xj97hld1mszyx6585xv5k-nixos-system-zeus-26.11.20260813.0e251e2`, revision `59d12e6fc664c8be0f8dc8af2846c81abdf860cb`
- Generation 167: UserEnvironment LiveActivation Current (bird), store path `/nix/store/dhwq1j6ndp5kh47nqasmfblv2w93h82d-home-manager-generation`
- Generation 49: UserEnvironment LiveActivation Current (li), store path `/nix/store/czqlj0ws84i9v9mxhv95bvk07xirff17-home-manager-generation`

Most recent deployment records include:
- Deployment 181: HostEnvironment goldragon zeus CompleteHost Host.ActivateNow LiveActivation, Succeeded (revision `59d12e6fc664c8be0f8dc8af2846c81abdf860cb`)
- Deployment 180: UserEnvironment.bird ActivateNow, Failed.(Activate ActivationFailed)
- Deployment 173: HostEnvironment Evaluate, Succeeded

Notable failures in history:
- Deployment 166: CopyClosure BuilderUnreachable
- Deployment 162: CopyClosure BuilderUnreachable
- Deployment 158: CopyClosure BuilderUnreachable
- Deployment 150: CopyClosure BuilderUnreachable
- Deployment 119: Failed.(Activate ActivationFailed)
- Deployment 53: Failed.(Activate ActivationFailed)
- Deployment 30: CopyClosure BuilderUnreachable

**Verdict: CLEAR.** The daemon is active, both sockets exist at the expected paths with the expected modes, and the ordinary socket responds to queries.

## 5. PROPOSAL

```
$ ls -la /git/github.com/LiGoldragon/goldragon/proposal.datom
-rw-r--r-- 1 li users 5163 Sep  1 14:12 /git/github.com/LiGoldragon/goldragon/proposal.datom

$ test -L /git/github.com/LiGoldragon/goldragon/proposal.datom && echo "IS SYMLINK" || echo "NOT SYMLINK"
NOT SYMLINK
```

Regular file, not a symlink, at an absolute path.

Zeus declaration found in the proposal:

```
zeus {Edge Max Max {Metal Some.X86_64 4 Some.ThinkPadT14Gen2Intel None None None Some.12 None None None []}
```

**Verdict: CLEAR.** The proposal file exists as an absolute regular non-symlink file and declares zeus as an Edge node in the goldragon cluster.

## 6. CAPACITY

Could not be verified. SSH does not connect, so disk space on Zeus cannot be queried.

**Verdict: BLOCKED.** Cannot check Nix store free space because Zeus is unreachable.

## 7. BOOT SURFACE

Could not be verified. SSH does not connect, so boot configuration and generation count on Zeus cannot be read.

From Lojix state (check 4), the most recent Current CompleteHost generation is 181, with store path `/nix/store/c3753yv0095xj97hld1mszyx6585xv5k-nixos-system-zeus-26.11.20260813.0e251e2`. This is Lojix's committed state; the live Nix profile on Zeus cannot be confirmed.

**Verdict: BLOCKED.** Cannot inspect boot configuration because Zeus is unreachable.

## 8. ACTIVATION HAZARD

Could not be verified. SSH does not connect, so the state of `complex-init.service` (or its successor) on Zeus cannot be inspected.

From Lojix deployment history: the most recent CompleteHost activation (deployment 181, Host.ActivateNow) succeeded. The most recent activation failure was deployment 180, a UserEnvironment.bird ActivateNow that failed with `Failed.(Activate ActivationFailed)`. Deployment 119 failed with `Failed.(Activate ActivationFailed)` on a CompleteHost TestActivation at revision `99db2f40f2037890cc597c2aeb7a3386932d216f`, but subsequent CompleteHost activations at later revisions succeeded.

**Verdict: BLOCKED.** Cannot inspect the remote unit state or the source being deployed because Zeus is unreachable. Lojix history suggests the most recent CompleteHost activation succeeded, but live state cannot be confirmed.
