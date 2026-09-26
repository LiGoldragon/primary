# GC root protection for messenger-clj 0.2.5

Timestamp: 2026-09-26T03:24:07Z (host: ouranos)

## Finding confirmed

All ten `hm-*` symlinks under `~/.local/bin` (`hm-send`, `hm-send-abrupt`,
`hm-list`, `hm-register`, `hm-repair`, `hm-deregister`, `hm-rebind`,
`hm-move`, `hm-retire`, `hm-heartbeat-state`) resolve through
`~/.local/libexec/messenger-clj` (itself a hand-made symlink) to a single
top-level store path:

```
/nix/store/p8mz1msm8lxiahnw6sfipi8m258x1q3z-messenger-clj-0.2.5
```

## Runtime closure (`nix-store -qR`)

```
/nix/store/3gdswy2pnrc6jb89hzbkrb09pdn7wng5-source
/nix/store/bv3lx708clpz3m6zbd5742np4dlry0yj-libunistring-1.4.2
/nix/store/i3jw341xs88r6wxf1j22rjx1mmd8cfjw-libidn2-2.3.8
/nix/store/m07syxhld8hpprrdmzq565ziia6vlw9l-xgcc-15.3.0-libgcc
/nix/store/lm3pknxi0ipypy3lxh1wmm8wvvavdwrn-glibc-2.42-84
/nix/store/svx59425zxp552p2b8gm11qj5r09b56i-bash-5.3p15
/nix/store/wxbwfdnn41rkgdfcm221ql5qmk3i29c4-babashka-unwrapped-1.13.220
/nix/store/p8mz1msm8lxiahnw6sfipi8m258x1q3z-messenger-clj-0.2.5
```

8 paths total. `--add-root -r` on the top-level path pins the whole
closure, so no per-dependency root is needed.

## Root status before

`nix-store --query --roots /nix/store/p8mz1msm8lxiahnw6sfipi8m258x1q3z-messenger-clj-0.2.5`
returned only:

```
/proc/3566025/fd/3 -> /nix/store/p8mz1msm8lxiahnw6sfipi8m258x1q3z-messenger-clj-0.2.5
```

A `/proc/<pid>/fd` entry is a temporary root tied to one live process's
open file descriptor; it disappears when that process exits and is not a
persistent GC root. **Confirmed: no permanent root existed** before this
action. The nightly `00:00` GC could have collected it and killed all
`hm-*` messaging.

## Root created

```
mkdir -p ~/.local/state/da88cf-gcroots
nix-store --add-root ~/.local/state/da88cf-gcroots/messenger-clj-0.2.5 --indirect \
  -r /nix/store/p8mz1msm8lxiahnw6sfipi8m258x1q3z-messenger-clj-0.2.5
```

Result:

```
/home/li/.local/state/da88cf-gcroots/messenger-clj-0.2.5
```

(symlink -> `/nix/store/p8mz1msm8lxiahnw6sfipi8m258x1q3z-messenger-clj-0.2.5`)

## Root status after (verification)

`nix-store --query --roots /nix/store/p8mz1msm8lxiahnw6sfipi8m258x1q3z-messenger-clj-0.2.5`:

```
/home/li/.local/state/da88cf-gcroots/messenger-clj-0.2.5 -> /nix/store/p8mz1msm8lxiahnw6sfipi8m258x1q3z-messenger-clj-0.2.5
```

The transient `/proc/.../fd` entry from the earlier query is gone (that
process's query completed); the new indirect root is present and durable
across GC runs. **Verified: rooted.**

## Adjacent checks (per task instruction, no changes made)

- **flow-nexus 0.12.2** — active `ExecStart` (via
  `~/.config/systemd/user/flow-nexus.service.d/override.conf`) points to
  `/nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2`.
  `nix profile list` shows this exact path as the `flow` profile element's
  store path, and `nix-store --query --roots` on it returns
  `/home/li/.nix-profile-8-link-19-link -> /nix/store/i69j84zxsjxppa0ihq1x2ch1y5rga74m-profile`
  (plus a transient `/proc/<pid>/exe|maps` entry for the running daemon).
  **Confirmed rooted** via the user's Nix profile; no action needed.
- **message-daemon.service** `ExecStart` points to
  `/nix/store/npnsww3fsa2g4hk72r9yd9nw6bfqnm08-message-0.12.0`.
  `nix-store --query --roots` on it returns, among other entries,
  `/run/current-system -> /nix/store/hm7zclf03cyr797vacqj8mgz3qmkkm5d-nixos-system-ouranos-...`
  and `/nix/var/nix/profiles/system-188-link -> ...` (the NixOS system
  closure), plus home-manager and profile roots.
  **Confirmed rooted**; no action needed.

## No other changes

No symlink, systemd unit, or Nix profile was modified. No garbage
collection was run. No filesystem search of `/nix/store` was performed;
all paths were obtained from `readlink`, `nix-store -qR`, `nix profile
list`, and `systemctl cat`, per `nix-workflow` (ask Nix or source, not the
store filesystem).

## Protective measure only

This GC root is a **temporary protective measure**. It is not committed
to the repository (per task instruction) and does not replace the
declared fix: messenger-clj should be reached through the **CriomOS-home
package declaration** assigned to flow `00f95a`, which will make its
presence declarative (and therefore self-rooting via the home-manager
generation) rather than dependent on this hand-added indirect root or the
hand-made `~/.local/bin` / `~/.local/libexec` symlinks.

## Qwen shards (temporary, until the Prometheus deploy lands; then remove these three roots so the next GC frees the laptop)

Timestamp: 2026-09-26T04:06Z (host: ouranos). Source: `flows/da88cf/reports/prometheus-deploy-risk.md` §"Where the models are" (§3, "The two models").

Tonight's Prometheus deploy stages its whole closure through ouranos's
store (Lojix 7.0.0: `ClosureCopy`/`nix copy` only skips paths already
valid on the target — see the report §2). The three Qwen3.5-122B shards
are present on ouranos but unrooted (about 71.2 GiB); the `nix-gc.timer`
at 00:00 would delete them and force a 71 GiB re-fetch from Prometheus's
nix-serve during the deploy. The Gemma shards are **not** present on
ouranos and were **not** copied or rooted here — pre-seeding Gemma is a
separate, larger store write left to the deploy owner (report §5.3). The
old Prometheus system closure (the ~80 GiB whole mentioned in the
original task) was **not** rooted — only the three Qwen shard paths
below.

Paths (from `flows/da88cf/reports/prometheus-deploy-risk.md` §3):

```
/nix/store/cr3yl0w80abpb9mwlm8w9c90sx5w287c-Qwen3.5-122B-A10B-Q4_K_M-00001-of-00003.gguf   (10.4 MiB)
/nix/store/3dl3vi57wll2j32097crcjbxw90bq6v5-Qwen3.5-122B-A10B-Q4_K_M-00002-of-00003.gguf   (46.5 GiB)
/nix/store/24z4j1lnv614aaig28q1qi6nigx35vrc-Qwen3.5-122B-A10B-Q4_K_M-00003-of-00003.gguf   (24.7 GiB)
```

### Root status before

`nix path-info` confirmed all three valid locally. `nix-store --query
--roots` returned no persistent root for any of the three (shard 1's
query also flushed a few stale temproots files, which is Nix's own
housekeeping, not a root). **Confirmed: no roots existed.**

### Roots created

```
mkdir -p ~/.local/state/da88cf-gcroots
nix-store --add-root ~/.local/state/da88cf-gcroots/qwen-shard-1 --indirect -r <shard 1>
nix-store --add-root ~/.local/state/da88cf-gcroots/qwen-shard-2 --indirect -r <shard 2>
nix-store --add-root ~/.local/state/da88cf-gcroots/qwen-shard-3 --indirect -r <shard 3>
```

### Root status after (verification)

`nix-store --query --roots` on each shard now shows:

```
/home/li/.local/state/da88cf-gcroots/qwen-shard-1 -> .../Qwen3.5-122B-A10B-Q4_K_M-00001-of-00003.gguf
/home/li/.local/state/da88cf-gcroots/qwen-shard-2 -> .../Qwen3.5-122B-A10B-Q4_K_M-00002-of-00003.gguf
/home/li/.local/state/da88cf-gcroots/qwen-shard-3 -> .../Qwen3.5-122B-A10B-Q4_K_M-00003-of-00003.gguf
```

**Verified: rooted.** `df -h /` unchanged (798G used / 71G avail, 92%)
before and after — no store write occurred, only root symlinks.

### Protective measure only

**Remove these three roots once the Prometheus deploy has landed**, so
the next `nix-gc.timer` run is free to reclaim ouranos's disk again:

```
rm ~/.local/state/da88cf-gcroots/qwen-shard-1 \
   ~/.local/state/da88cf-gcroots/qwen-shard-2 \
   ~/.local/state/da88cf-gcroots/qwen-shard-3
```
