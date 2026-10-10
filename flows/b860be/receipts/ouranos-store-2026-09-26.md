# ouranos /nix/store survey — 2026-09-26

Passive audit only. Nothing deleted, nothing sent. Requested ahead of Lojix
deployment 34 (ouranos system closure realize from Prometheus) landing on an
already-99%-full store.

## 1. Reclaimable dead paths (no roots touched)

`nix-store --gc --print-dead` ran to completion (took a few minutes; the
store has ~2600 distinct persistent GC roots to scan against). Result:

- **20 dead paths**, essentially all `.drv` files plus two small build
  artifacts (`horizon.json`, `initrd-units`).
- Total reclaimable size: **548 KiB** (`du -sch` over the dead-path list).

So a `nix-store --gc` run right now, with every existing root left in place,
would free essentially nothing (< 1 MiB). The store is 99% full because
almost everything reachable is rooted, not because of accumulated garbage.

## 2. Largest 10 roots by closure size

Resolved 2600 non-temp GC-root sources (excluding ~2600 `{temp:NNNNN}`
build-lock entries from 3 in-flight builds/evals) down to 891 distinct live
store targets; `nix path-info -S` returned sizes for 238 of them. Top 10 by
closure (NAR) size:

| Size | Store path | Root(s) pinning it | Category |
|---|---|---|---|
| 46.54 GiB | `3dl3vi5...-Qwen3.5-122B-A10B-Q4_K_M-00002-of-00003.gguf` | `/home/li/.local/state/da88cf-gcroots/qwen-shard-2` | da88cf Qwen shard |
| 46.49 GiB | `dqr9jn4...-gemma-4-26B-A4B-it-BF16-00001-of-00002.gguf` | `/home/li/.local/state/b860be-gcroots/gemma-1` | b860be Gemma shard |
| 32.19 GiB | `hm7zclf...-nixos-system-ouranos-26.11.20260813.0e251e2` | `/nix/var/nix/profiles/system-188-link`, `/run/current-system` | **current system generation** (essential) |
| 31.94 GiB | `8cvwmgd...-nixos-system-ouranos-26.11.20260813.0e251e2` | `/run/booted-system` | **booted system** (essential, same release as above but different hash — pre-switch build) |
| 29.43 GiB | `36hqmbs...-nixos-system-ouranos-26.05.20260422.0726a0e` | `/tmp/nordvpn-system-path-v4` | **old (26.05) system closure**, pinned only by a stray `/tmp` root — not an active system profile generation |
| 29.27 GiB | `386kvm9...-profile` | `/home/li/.nix-profile-6-link-196-link` | Home generation (user profile link, one of a long numbered series) |
| 29.03 GiB | `92i58i4...-home-manager-generation` | `/var/lib/lojix/audits/bird-zeus-9ef4d609` | lojix audit snapshot root, pins a full Home Manager closure |
| 29.03 GiB | `cn91wk3...-home-manager-generation` | `/var/lib/lojix/audits/bird-zeus-8e9fd484` | lojix audit snapshot root, pins a full Home Manager closure |
| 28.68 GiB | `4vjsj76...-home-manager-generation` | `/tmp/claude-1001/.../f6db8d14-.../scratchpad/li-activation-result` | stale scratch out-link from an unrelated, apparently old Claude session under `/tmp` |
| 28.40 GiB | `r3ci9jy...-home-manager-generation` | `/home/li/.local/state/home-manager/gcroots/current-home`, `new-home` | current Home Manager generation (essential) |

Notes on categories not in the top 10 but present among the 891 targets:
- **da88cf Qwen roots**: `qwen-shard-1/2/3` (only shard-2 made the top 10; shards 1 and 3 are comparable multi-GB `.gguf` files).
- **b860be Gemma roots**: `gemma-1/2/3` (only gemma-1 made the top 10).
- **jj/scratch out-links and `result` symlinks under `/home`**: dozens, e.g. every `/home/li/wt/github.com/LiGoldragon/*/result` worktree build output, `/home/li/primary/result`, and the many `/home/li/.nix-profile-{6,8}-link-*-link` / `home-manager-{NNNN}-link` generations under `/home/li/.local/state/nix/profiles` and `/home/li/.local/state/nix/profiles` for user `bird` too — each such generation closure runs ~28–30 GiB but heavily deduplicated on disk against each other and against the current generation.

Only one **system profile generation** exists (see §3), so the two ~32 GiB
"system" entries above are current + booted, not an accumulation of old
system generations.

## 3. System profile generations

```
lrwxrwxrwx 1 root root   15 Sep 24 18:43 system -> system-188-link
lrwxrwxrwx 1 root root   87 Sep 24 18:43 system-188-link -> /nix/store/hm7zclf03cyr797vacqj8mgz3qmkkm5d-nixos-system-ouranos-26.11.20260813.0e251e2
```

Just **one** generation (188), dated 2026-09-24 18:43. No old system
generations are being kept in `/nix/var/nix/profiles/`; the pressure comes
from other roots (see §2), not system-generation buildup.

## 4. Disk and time

```
$ df -h /nix/store
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme0n1p2  916G  860G  8.9G  99% /nix/store

$ date
Sat Sep 26 01:03:14 AM CST 2026
```

(8.9–9.1 GiB free across the survey window; it moved slightly during the
in-flight builds noted in §2.)

## 5. GC action taken (2026-09-26, same day)

Authorized action: remove the stray `/tmp/nordvpn-system-path-v4` symlink
(rooting the dead 26.05 system closure via an `auto` GC root) and run
`nix-store --gc`.

### 5.1 Confirm target is not an active generation

```
$ readlink -f /tmp/nordvpn-system-path-v4
/nix/store/36hqmbskadywqv7nz1c08hzrkzg96pqx-nixos-system-ouranos-26.05.20260422.0726a0e

$ readlink -f /run/current-system
/nix/store/hm7zclf03cyr797vacqj8mgz3qmkkm5d-nixos-system-ouranos-26.11.20260813.0e251e2

$ readlink -f /run/booted-system
/nix/store/8cvwmgdkvqhn4hyd2mqccphr5h588q7l-nixos-system-ouranos-26.11.20260813.0e251e2

$ ls -la /nix/var/nix/profiles/ | grep system
lrwxrwxrwx 1 root root   15 Sep 24 18:43 system -> system-188-link
lrwxrwxrwx 1 root root   87 Sep 24 18:43 system-188-link -> /nix/store/hm7zclf03cyr797vacqj8mgz3qmkkm5d-nixos-system-ouranos-26.11.20260813.0e251e2

$ readlink -f /nix/var/nix/profiles/system-188-link
/nix/store/hm7zclf03cyr797vacqj8mgz3qmkkm5d-nixos-system-ouranos-26.11.20260813.0e251e2
```

Confirmed: `/tmp/nordvpn-system-path-v4` resolves to the 26.05 store path,
distinct from `/run/current-system`, `/run/booted-system`, and the only
`system-*-link` profile target (188, the 26.11 generation). Safe to remove.

### 5.2 Confirm no store-writing Lojix copy or nix build running

```
$ pgrep -af 'nix copy|nix-store --import|nix-daemon.*build'
none found
```

No matching process. (The only hit in the raw pgrep output was the invoking
shell's own command line containing the search pattern as text — not a real
match; discounted.) Evaluations only, consistent with the brief's expectation.

### 5.3 Locate and remove the stray root

```
$ ls -la /nix/var/nix/gcroots/auto/ | grep -i nordvpn
lrwxrwxrwx 1 root root 27 Aug 10 04:41 m0526vbqza8cvdgyfdxsvk3y6kqp7ri0 -> /tmp/nordvpn-system-path-v4
```

Auto-root `m0526vbqza8cvdgyfdxsvk3y6kqp7ri0` points at the `/tmp` symlink
(this is how nix-daemon auto-registers a root for any live symlink under
`/tmp` it has seen referenced).

```
$ ls -la /tmp/nordvpn-system-path-v4
lrwxrwxrwx 1 li users 87 Aug 10 04:41 /tmp/nordvpn-system-path-v4 -> /nix/store/36hqmbskadywqv7nz1c08hzrkzg96pqx-nixos-system-ouranos-26.05.20260422.0726a0e

$ id
uid=1001(li) gid=100(users) groups=100(users),17(audio),26(video),27(dialout),57(networkmanager),62(systemd-journal),979(power),980(uinput),994(plugdev),995(nixdev)

$ sudo -n true
sudo: a password is required
```

`sudo -n` fails as expected (known not to work). No root escalation was
needed: the stray symlink itself is owned by `li`, so it was removed as the
invoking user with a plain `rm`:

```
$ rm -v /tmp/nordvpn-system-path-v4
removed '/tmp/nordvpn-system-path-v4'
```

The `auto/m0526vbqza8cvdgyfdxsvk3y6kqp7ri0` entry (owned by root) was left
in place for the daemon to reap during GC; it was gone after the GC run
(confirmed in §5.5), so no separate root action was required.

### 5.4 Run the GC

`nix-store --gc` talks to `nix-daemon` over its socket, so no direct root
write to the store was needed from this session — the daemon (running as
root) performs the deletion:

```
$ nix-store --gc
... (7773 store paths deleted, including the old 26.05 closure and its
     now-dead-only dependencies not shared with the current generation) ...
deleting unused links...
note: hard linking is currently saving 70.9 GiB
7773 store paths deleted, 9.5 GiB freed
```

Freed: **9.5 GiB** — less than the closure's full 29.43 GiB NAR size because
much of the 26.05 closure's content is hardlink-deduplicated on disk against
paths still live in the current (26.11) generation and other roots; only the
non-shared blocks were actually reclaimed.

### 5.5 Witness: disk space before/after, roots still intact

```
$ df -h /nix/store   # before (this session, just before rm+gc)
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme0n1p2  916G  860G  8.8G  99% /nix/store

$ df -h /nix/store   # after
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme0n1p2  916G  850G   20G  98% /nix/store
```

Free space rose from **8.8 GiB to 20 GiB**.

```
$ ls /nix/var/nix/gcroots/auto/m0526vbqza8cvdgyfdxsvk3y6kqp7ri0
ls: cannot access '/nix/var/nix/gcroots/auto/m0526vbqza8cvdgyfdxsvk3y6kqp7ri0': No such file or directory
```

The dangling auto-root was cleaned up by the GC run itself.

```
$ readlink -f /home/li/.local/state/b860be-gcroots/gemma-1
/nix/store/dqr9jn4rq8975lrww1dyi2yx9vihw7ln-gemma-4-26B-A4B-it-BF16-00001-of-00002.gguf

$ nix-store --query --roots /nix/store/dqr9jn4rq8975lrww1dyi2yx9vihw7ln-gemma-4-26B-A4B-it-BF16-00001-of-00002.gguf
/home/li/.local/state/b860be-gcroots/gemma-1 -> /nix/store/dqr9jn4rq8975lrww1dyi2yx9vihw7ln-gemma-4-26B-A4B-it-BF16-00001-of-00002.gguf

$ readlink -f /home/li/.local/state/da88cf-gcroots/qwen-shard-2
/nix/store/3dl3vi57wll2j32097crcjbxw90bq6v5-Qwen3.5-122B-A10B-Q4_K_M-00002-of-00003.gguf

$ nix-store --query --roots /nix/store/3dl3vi57wll2j32097crcjbxw90bq6v5-Qwen3.5-122B-A10B-Q4_K_M-00002-of-00003.gguf
/home/li/.local/state/da88cf-gcroots/qwen-shard-2 -> /nix/store/3dl3vi57wll2j32097crcjbxw90bq6v5-Qwen3.5-122B-A10B-Q4_K_M-00002-of-00003.gguf
```

Both the b860be Gemma-1 root and the da88cf Qwen-shard-2 root resolve
cleanly and their store paths still exist and are still rooted. No other
roots listed in §2 of this receipt were touched.

### 5.6 Summary

- Freed: **9.5 GiB** (7773 store paths deleted)
- Free space after: **20 GiB** on `/nix/store` (up from 8.8 GiB)
- Roots verified intact: Gemma (b860be) and Qwen shard-2 (da88cf) both
  resolve; no in-flight Lojix copy or build was running or disturbed
- Nothing blocked: the stray symlink was owned by the invoking user, so no
  sudo/root path was needed for the removal step; the GC itself ran through
  `nix-daemon` as usual
