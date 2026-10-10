# Prometheus disk witness

Read-only witness of prometheus.goldragon.criome (primary), plus comparison
data from zeus.goldragon.criome and ouranos (local). All remote commands run
as `ssh -o BatchMode=yes -o ConnectTimeout=5 <host> '<cmd>'`. Nothing was
deleted, edited, or restarted. No git/jj commands were run.

## 1. Filesystems (prometheus)

Witnessed: `df -h`
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme0n1p2  1.9T  1.4T  437G  77% /
tmpfs            32G  5.6M   32G   1% /run
/dev/nvme0n1p2  1.9T  1.4T  437G  77% /var
/dev/nvme0n1p2  1.9T  1.4T  437G  77% /nix
devtmpfs        6.3G     0  6.3G   0% /dev
tmpfs            63G     0   63G   0% /dev/shm
efivarfs        128K   48K   76K  39% /sys/firmware/efi/efivars
/dev/nvme0n1p2  1.9T  1.4T  437G  77% /home
/dev/nvme0n1p1 1022M  257M  766M  26% /boot
tmpfs            13G   20K   13G   1% /run/user/1001
```
`/`, `/var`, `/nix`, `/home` are all the *same* btrfs partition
(`/dev/nvme0n1p2`, 1.9T) â€” they are not separate volumes, so their "Used"
figures are identical (1.4T) and not additive.

Witnessed: `lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINT`
```
NAME        SIZE FSTYPE MOUNTPOINT
nvme0n1     1.8T
├─nvme0n1p1   1G vfat   /boot
└─nvme0n1p2 1.8T btrfs  /home
```

## 2. Size table by category (prometheus, on the single 1.9T/1.4T-used partition)

| Category | Size | Notes |
|---|---|---|
| Nix store (`/nix/store`) | **1.5T** | dominates the partition; see Â§2a/2b |
| â€” of which: current system closure | 545 GB | `nix path-info -S /run/current-system` |
| â€” of which: GC-rooted GGUF model files at store top level | 707 GB | see model table below; these are *not* reclaimable by GC while rooted |
| â€” of which: reported dead (GC-eligible) store paths | 99,161 paths | `nix-store --gc --print-dead \| wc -l`, capped at 115s, completed at ~99k; **no aggregate byte size collected** (would need a second pass, out of scope for a 300s-bounded witness) |
| `/nix/var` (profiles, gcroots, generations metadata) | 672 MB | |
| `/var/log` | 3.2 GB | |
| `/var/lib` | 723 MB | includes `/var/lib/private/ollama` (permission denied to inspect) |
| `/var/cache` | 31 MB | |
| `/home/li` | 661 MB | see breakdown below |
| `/home/bird`, `/home/maikro` | 0 (empty/inaccessible) | |
| `/boot` | 257 MB | |
| Media (video/audio) | **none found** | no `movies`/`music`/`videos`/`media` dirs; `Downloads` exists but is empty (0 bytes); 0 `.mkv/.mp4/.flac/.mp3` files under `/home/li` |
| Git repositories (untouched >30 days) | **none found** | see Â§3 |
| Everything else on the partition (root fs overhead, /var/db, /var/spool, etc.) | negligible (single-digit MB or 0) | |

`/home/li` breakdown (661 MB total; non-dotfile listing summed to only
~1 MB, remainder is dotdirs):
```
478M  .cache        (includes .cache/huggingface = 72M, mostly `hub`+`xet` dirs)
181M  .cargo
92K   .emacs.d
64K   .zcompdump
60K   .vscode-oss
44K   .pi
12K   .gnupg, .ssh
528K  nixos-efi-vars.fd
0     Downloads, Pictures
```

### 2a. GC-rooted AI model files (`/nix/var/nix/gcroots/llm-*`)

These are the named GC roots described in the brief's Â§3 as possibly meaning
"cluster/node/kind/generation" â€” witnessed reality is different: they are a
flat set of `llm-<model>-<shard>` symlinks straight into `/nix/store`, with
**no** `criomos`-prefixed gcroots directory (`/nix/var/nix/gcroots/criomos/`
does not exist on prometheus; `find` for anything `*criomos*` under gcroots
returned nothing).

| Root name | Size | Target (store path, truncated) |
|---|---|---|
| llm-gpt-oss-shard-1 | 47G | gpt-oss-120b-Q4_K_M-00001-of-00002.gguf |
| llm-nemotron-shard-2 | 47G | NVIDIA-Nemotron-3-Super-120B-A12B-...-00002-of-00003.gguf |
| llm-qwen3.5-122b-shard-2 | 47G | Qwen3.5-122B-A10B-Q4_K_M-00002-of-00003.gguf |
| llm-deepseek-r1-70b-1 | 38G | DeepSeek-R1-Distill-Llama-70B-Q8_0-00001-of-00002.gguf |
| llm-deepseek-r1-70b-2 | 38G | DeepSeek-R1-Distill-Llama-70B-Q8_0-00001-of-00002.gguf (same filename as -1; distinct store hash) |
| llm-qwen3.5-35b | 35G | Qwen3.5-35B-A3B-Q8_0.gguf |
| llm-nemotron-nano-30b | 32G | Nemotron-3-Nano-30B-A3B-Q8_0.gguf |
| llm-nemotron-shard-3 | 31G | NVIDIA-Nemotron-3-Super-120B-A12B-...-00003-of-00003.gguf |
| llm-glm-4.7-flash | 30G | GLM-4.7-Flash-Q8_0.gguf |
| llm-qwen3.5-27b | 27G | Qwen3.5-27B-Q8_0.gguf |
| llm-qwen3.5-122b-shard-3 | 25G | Qwen3.5-122B-A10B-Q4_K_M-00003-of-00003.gguf |
| llm-qwen3-8b | 8.2G | Qwen3-8B-Q8_0.gguf |
| llm-gpt-oss-shard-2 | 13G | gpt-oss-120b-Q4_K_M-00002-of-00002.gguf |
| llm-llama-3.2-1b-instruct | 771M | llama-3.2-1b-instruct-q4_k_m.gguf |
| llm-qwen3.5-122b-shard-1 | 11M | Qwen3.5-122B-A10B-Q4_K_M-00001-of-00003.gguf (tiny â€” header/metadata shard) |
| llm-nemotron-shard-1 | 7.6M | NVIDIA-Nemotron-3-Super-120B-A12B-...-00001-of-00003.gguf (tiny â€” header/metadata shard) |
| **Total** (`find /nix/store -maxdepth 1 -iname '*.gguf'`, all top-level gguf) | **707G** | |

There are also non-gguf gcroots (`llm-model-*`, `llm-llm-models-dir`)
pointing at store derivation outputs, not measured separately (small
relative to the gguf payload).

No `.safetensors`/`.bin` model files, ollama installation
(`/home/li/.ollama`, `/var/lib/ollama` both absent), or comfyui/stable-diffusion/whisper
trees were found. `~/.cache/huggingface` exists but is only 72M (hub
metadata + xet cache, not model weights).

### 2b. Nix store totals and dead paths

- `nix path-info -S /run/current-system`: **545,366,616,456 bytes** (508 GiB)
  for the currently-active system closure.
- `du -xsh /nix/store`: **1.5T**.
- `nix-store --gc --print-dead | wc -l` (capped 115s of the 120s budget):
  completed, returned **99,161** dead (GC-eligible) paths. No byte total was
  collected for those paths (a `nix-store --gc --print-dead | xargs du -c`
  style pass was out of scope for the witness time budget); given ~1.5T
  store minus 545G live closure minus 707G rooted models, the dead-path
  total is bounded above by roughly **250 GB**, but that arithmetic assumes
  no overlap between "current closure" and "rooted models" and is not a
  direct measurement â€” treat as an order-of-magnitude estimate only.

## 3. Git repositories

`find /home /var/lib /srv /data -maxdepth 4 -name .git -type d`: **no
results**. No `/data` mount exists on prometheus. No git repositories were
found on the searched paths, so no "untouched >30 days" list applies.

## 4. Generations, gcroots, and what "next generations" could mean

- System generations (`ls /nix/var/nix/profiles/ | grep system-`): **41
  generations** present, `system-11-link` through `system-51-link`
  (`system-11` dated 2026-03-22, `system-51` dated 2026-07-03; current
  `system` symlink points at `system-51-link`). Gaps in the numbering (no
  system-1..10) indicate earlier generations have already been pruned by
  prior GC/gc-keep-generations policy.
- `find ... -iname '*next*' -o -iname '*generation*'` under
  `/nix/var/nix/profiles`, `/nix/var/nix/gcroots`, `/var/lib`, `/home`:
  **no matches** (the search command itself exited non-zero/empty on the
  live host, witnessed as a plain empty result, not an error).
- `/nix/var/nix/gcroots/` top level (witnessed via `ls -la`) contains: `auto/`
  (105 entries), `booted-system` and `current-system` symlinks into `/run`,
  the 16 `llm-*` model roots above, `per-container/`, `per-user/`, and a
  `profiles -> /mnt/nix/var/nix/profiles` symlink. **No `criomos/`
  subdirectory exists**, so the brief's expected
  "cluster/node/kind/generation"-named gcroots were not found on
  prometheus as such â€” the closest analog is the `llm-*` roots, which are
  flat and model-named, not cluster/node/kind/generation-named.
- Best reading of "next generations" given what's on disk: prometheus is
  still running NixOS release **26.05** (`nixos-version` â†’
  `26.05.20260422.0726a0e "Yarara"`) while zeus and ouranos are both on
  **26.11** (`26.11.20260813.0e251e2 "Zokor"`). A `lojix` query
  (`Query.ByNode.{ goldragon prometheus None }`) shows repeated recent
  attempts (event ids 5, 6, 8, 11, 12) to realize/activate a 26.11-era
  `nixos-system-prometheus-26.11.20260813.0e251e2` build, several of which
  **failed**: two on Nix evaluation errors (`test-vm-host.nix` producing a
  null network address; a duplicate/read-only `home-manager...stylix.base16`
  definition), and one (event 12) on `Host.Realize` timing out downloading
  its own NARs from `nix.prometheus.goldragon.criome` (the build was later
  interrupted). So "next generations" plausibly refers to this stalled
  26.05â†’26.11 upgrade, not a special gcroot category that exists on disk.

## 5. Systemd units matching ollama/llama/whisper/comfy/model/ai- (prometheus)

`systemctl list-units --all --no-pager | grep -iE 'ollama|llama|whisper|comfy|stable|model|ai-'`:
```
prometheus-llama-router.service   loaded active running   prometheus llama.cpp router — multi-model on-demand serving
```
Only one matching unit, currently loaded/active/running. No ollama, whisper,
or comfyui units exist on prometheus.

## 6. Host update state

| Host | `readlink /run/current-system` | `readlink .../profiles/system` | `nixos-version` | Newest 3 system-*-link mtimes | Uptime | current == newest profile link? |
|---|---|---|---|---|---|---|
| prometheus | `...-nixos-system-prometheus-26.05.20260422.0726a0e` | `system-51-link` | `26.05.20260422.0726a0e (Yarara)` | system-49 2026-06-20, system-50 2026-07-03, system-51 2026-07-03 | 2 days, 4:26 | **Yes** â€” current-system matches the newest (system-51) profile link. (But see Â§4: it is on an older *release* than zeus/ouranos, and the in-flight 26.11 upgrade attempts are failing.) |
| zeus | `...-nixos-system-zeus-26.11.20260813.0e251e2` | `system-72-link` | `26.11.20260813.0e251e2 (Zokor)` | system-70 2026-09-03, system-71 2026-09-04, system-72 2026-09-06 | 4 days, 22:16 | **Yes** |
| ouranos | `...-nixos-system-ouranos-26.11.20260813.0e251e2` | `system-183-link` | `26.11.20260813.0e251e2 (Zokor)` | (only most-recent captured) system-183 2026-09-12 | 5 days, 22:13 | **Yes** |

Lojix (`lojix 'Query.ByNode.{ goldragon <node> None }'`, timeout 20s each,
run from ouranos where the CLI is on PATH):
- **prometheus**: newest events show repeated failed `Host.Realize`/
  `Host.Evaluate` attempts toward the 26.11 build (see Â§4); most recent fully
  **Succeeded** `Host.Evaluate` event was id 6 (26.05-era rev
  `5dc34...`), i.e. no successful 26.11 evaluation/realize/activate has
  landed yet as of this query.
- **zeus**: query returned an **empty** record set (`Queried.{ [] [] { 369 369 } }`)
  â€” no DeployTerminal history found for zeus under that node key at the
  time of the query.
- **ouranos**: newest `Host.ActivateNow` for `CompleteHost` (event id 4,
  rev `36653a1...`) **Succeeded**, matching the live `system-183-link`.
  An earlier activation attempt (event id 2, same rev family) had
  **Failed** with `NOPERMISSION` (exit code 4) from the self-switch script
  refusing to run `bootctl set-default`/`set-oneshot`, before a later
  attempt (id 3) succeeded. The most recent `UserEnvironment.li` realize
  (event id 7, rev `b029b31...`) **Failed** on the same
  `stylix.base16` read-only/duplicate-definition Nix eval error seen on
  prometheus, and a later realize attempt (event id 9) **Failed** trying to
  remote-build on prometheus (`failed to start SSH connection to
  'prometheus.goldragon.criome'`) â€” i.e. ouranos's own home-manager
  generation is currently stuck on the same defect that is blocking
  prometheus's host upgrade, compounded by prometheus being unreachable as
  a remote builder at that time (it answered SSH fine for this witness,
  so that failure looks transient/historical).

## 7. Free space on ouranos

Witnessed: `df -h /nix /home` (run locally on ouranos; no separate `/nix` or
`/home` filesystem exists â€” same partition as `/`):
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme0n1p2  916G  555G  314G  64% /
/dev/nvme0n1p2  916G  555G  314G  64% /
```
**314G available**, consistent with the brief's note that a build stopped
for lack of "315 GiB" â€” ouranos is right at that edge with only ~314G free
on its single 916G partition.

## Sources

All commands run 2026-09-16 via
`ssh -o BatchMode=yes -o ConnectTimeout=5 <host> '<cmd>'` against
`prometheus.goldragon.criome` and `zeus.goldragon.criome`, plus local
commands on `ouranos` (this host). Exact commands are inlined next to each
result above. `lojix` queried from ouranos (CLI found at
`/run/current-system/sw/bin/lojix`), 20s timeout per call. No destructive,
write, restart, or VCS command was issued.
