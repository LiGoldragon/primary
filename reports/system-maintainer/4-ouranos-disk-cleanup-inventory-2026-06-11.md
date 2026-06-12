# Ouranos disk cleanup inventory — 2026-06-11

## Current state after first cleanup

Root filesystem after deleting LiGoldragon Rust `target/` directories and stale temporary build directories:

- `/`: 916 GiB total, 514 GiB used, 356 GiB free, 60% used.
- Remaining top-level consumers:
  - `/nix`: 318.08 GiB
  - `/home`: 117.30 GiB
  - `swapfile`: 32.00 GiB
  - `/git`: 26.26 GiB
  - `/tmp`: 9.91 GiB
  - `/var`: 6.12 GiB

## High-value remaining deletion candidates

### 1. Archived Rust build outputs in `~/git-archive`

`/home/li/git-archive` is 27.05 GiB. Most of this is not archive source; it is Rust build output.

- `/home/li/git-archive/github.com/LiGoldragon/persona-spirit/target`: 22.54 GiB
- All `target/` directories under `/home/li/git-archive`: 24.64 GiB

Recommendation: delete all `target/` directories under `/home/li/git-archive`. This preserves archived source/history while reclaiming about 24.6 GiB.

### 2. Codex session history

`~/.codex` is 15.94 GiB, mostly session logs:

- `~/.codex/sessions`: 15.37 GiB
- `~/.codex/logs_2.sqlite`: 319 MiB
- `~/.codex/logs_2.sqlite-wal`: 105 MiB

Age-based reclaim estimates for `~/.codex/sessions`:

- Older than 7 days: about 15 GiB, 684 files
- Older than 14 days: about 7.1 GiB, 653 files
- Older than 30 days: about 1.8 GiB, 542 files
- Older than 60 days: about 1.4 GiB, 98 files
- Older than 90 days: about 57 MiB, 30 files

Largest session files:

- 2.2 GiB: `~/.codex/sessions/2026/05/06/...jsonl`
- 1.8 GiB: `~/.codex/sessions/2026/06/03/...jsonl`
- 1.7 GiB: `~/.codex/sessions/2026/06/01/...jsonl`
- 1.6 GiB: `~/.codex/sessions/2026/05/28/...jsonl`
- 1.5 GiB each: several sessions from 2026-05-24 through 2026-05-27

Recommendation: if preserving recent context matters, delete Codex sessions older than 14 days first. If aggressive cleanup is acceptable, delete older than 7 days.

### 3. Claude project history

`~/.claude` is 1.39 GiB:

- `~/.claude/projects`: 1.27 GiB
- Largest project: `~/.claude/projects/-home-li-primary`: about 1.27 GiB

Age-based reclaim estimates for `~/.claude/projects`:

- Older than 7 days: about 450 MiB
- Older than 14 days: about 302 MiB
- Older than 30 days: about 13 MiB

Recommendation: not high-value. Leave unless specifically pruning agent history.

### 4. Reclonable `/git` repositories

After deleting Rust build outputs, `/git/github.com` is 26.1 GiB. Large reclonable repos:

- `/git/github.com/NixOS/nixpkgs`: 6.78 GiB
- `/git/github.com/tqwewe/kameo`: 5.62 GiB
- `/git/github.com/LiGoldragon/library`: 3.00 GiB
- `/git/github.com/wezterm/wezterm`: 0.79 GiB
- `/git/github.com/Significant-Gravitas/AutoGPT`: 0.61 GiB
- `/git/github.com/langchain-ai/langgraph`: 0.51 GiB

Recommendation: delete reclonable external repos if not actively used. The biggest safe candidates are `NixOS/nixpkgs` and `tqwewe/kameo`, subject to whether any worktrees or symlinks still expect them.

### 5. Browser/application caches

`~/.cache` is about 5.33 GiB. Main candidates:

- `~/.cache/nix`: about 1.98 GiB
- `~/.cache/google-chrome`: about 1.73 GiB
- `~/.cache/puppeteer`: about 635 MiB
- `~/.cache/qutebrowser`: about 309 MiB
- `~/.cache/cloud-code`: about 126 MiB
- `~/.cache/whisper`: about 139 MiB

`~/.config` is about 7.89 GiB, mostly Chrome state:

- `~/.config/google-chrome`: about 7.38 GiB
- `~/.config/google-chrome/OptGuideOnDeviceModel`: about 4.07 GiB
- Chrome profiles under `~/.config/google-chrome`: about 3 GiB combined
- `~/.config/VSCodium`: about 388 MiB

Recommendation: cache deletion is moderate value. Chrome `OptGuideOnDeviceModel` is a notable 4 GiB model cache/state candidate, but browser profile/state directories should be handled carefully.

### 6. Downloads and media

`~/Downloads` is 8.56 GiB. Large media files include:

- Several TV episode `.mkv` files from 637 MiB to 1.5 GiB.

Recommendation: user-choice cleanup only.

### 7. Nix store

`/nix` is 318.08 GiB, but `nix store gc --dry-run` currently reports 0 store paths would be deleted. The store is rooted, not unreferenced garbage.

Found roots include:

- 197 system profile generations under `/nix/var/nix/profiles/system`.
- Current user home-manager generation root.
- Several `result` roots in active repos and worktrees.
- Many Bird and Maikro profile generations.

Recommendation: Nix cleanup requires deleting old profile generations and stale `result` symlinks, then running garbage collection. Do not delete store paths directly.

## Suggested cleanup order

1. Delete all `target/` directories under `~/git-archive`: about 24.6 GiB.
2. Delete Codex sessions older than 14 days: about 7.1 GiB, or older than 7 days for about 15 GiB.
3. Delete obvious reclonable external repos if approved: `NixOS/nixpkgs` and `tqwewe/kameo` together about 12.4 GiB.
4. Remove stale repo/worktree `result` symlinks and old profile generations, then run Nix GC.
5. Optionally clear browser/tool caches, especially `~/.cache/nix`, `~/.cache/google-chrome`, and Puppeteer cache.

## Cleanup resolution — later same session

Additional cleanup completed after tracing duplicate Nix store entries:

- Deleted all remaining `/git/**/target` directories, including non-LiGoldragon repos such as `tqwewe/kameo` and `y0sif/whisrs`.
- Deleted all `~/git-archive/**/target` directories.
- Deleted Codex session files older than 7 days.
- Removed stale user-owned `result` symlink roots under `/git`, `/home/li/wt`, `/home/li/primary`, and `/tmp`.
- Removed root-owned stale profile generations while preserving current profile links:
  - system: kept `system-114-link`
  - bird: kept `profile-53-link` and `home-manager-6-link`
  - maikro: kept `profile-28-link` and `home-manager-4-link`
  - li: already only had current `profile-1809-link` and `home-manager-768-link`
- Removed root-owned stale `/tmp/criomos-deploy` result root.
- Ran Nix garbage collection.

Final observed state:

- `/`: 916 GiB total, 239 GiB used, 630 GiB free, 28% used.
- `/nix`: 86.32 GiB.
- Non-proc roots are now only current profile/current OS roots:
  - current and booted system roots
  - one current system generation
  - current Li/Bird/Maikro profile and home-manager roots

Root cause:

- FullOS/Home deployments update current profile links but do not prune old profile generations.
- Bird and Maikro had many stale imperative `user-environment` profile generations, not just Home Manager generations.
- Those old profile generations retained historical `pi-*` and Rust toolchain store paths.
- Some remaining older store paths after cleanup are held only by live processes and `/run/booted-system`; they will disappear after reboot or session/process restart plus GC.

