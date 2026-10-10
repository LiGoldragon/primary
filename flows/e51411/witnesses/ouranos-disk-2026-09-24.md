# Ouranos disk hygiene — 2026-09-24

## Method

Reached ouranos over `ssh ouranos` as user `li` (no passwordless `sudo`
available on that account, so all work ran unprivileged through the
multi-user Nix daemon). `/`, `/nix`, and `/home` are all the same
filesystem on ouranos (`/dev/nvme0n1p2`, 916G), so one `df -h` line covers
all three.

## Before

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme0n1p2  916G  703G  167G  81% /
```

Booted and current system generations (recorded, not touched):

- `/run/booted-system` -> `/nix/store/8cvwmgdkvqhn4hyd2mqccphr5h588q7l-nixos-system-ouranos-26.11.20260813.0e251e2`
- `/run/current-system` -> `/nix/store/41cvi7l9rjy3n05jixzqdk937rg8gz27-nixos-system-ouranos-26.11.20260813.0e251e2`

These two differ (a switch is staged but not yet booted). Both were left
alone. Listing/pruning older generations needs root (`system.lock` refused
write access to the unprivileged `li` session), and 167G/916G free was not
"critically short," so per the disk-hygiene rule old generations were left
alone entirely — no generation was pinned, retired, or deleted.

## What was removed and why

Ran `nix-collect-garbage` twice as `li` (the daemon performed the actual
deletion as root; no explicit `sudo` was needed or used):

- Pass 1: 1035 dead store paths deleted, 5.6 GiB freed. The deleted set
  included the exact debris named in the brief — dead `.drv`/`.lock`
  entries for the large model files from the failed Lojix deployment 31
  (`gemma-4-26B-A4B-it-BF16-...gguf.drv`, `gpt-oss-120b-Q4_K_M-...gguf.lock`,
  `mmproj-F16.gguf.drv`, `NVIDIA-Nemotron-3-Super-120B-A12B-UD-Q4_K_M-...gguf.lock`,
  `gemma-4-31B-it-BF16-...gguf.lock`), plus a large number of unrelated dead
  sources, crate tarballs, and stale `.drv`/`.lock` files from other
  finished builds that were simply no longer referenced by any live root.
- Pass 2 (re-run to confirm the sweep was complete): 6 more dead paths,
  20.8 MiB freed. Confirms the store had reached a stable, fully-collected
  state.
- Verified afterward: no `.gguf`/`.safetensors` files remain anywhere
  under `/tmp`, `/var/tmp`, or `/home/li`; no `/tmp/nix-build-*` scratch
  directories exist; `nix-store --gc --print-dead` no longer names any
  model file. The partial-download debris from deployment 31 is gone —
  GC alone absorbed it, since Nix had already recorded those `.gguf`
  fetches as dead (unreferenced) derivations/outputs once the deploy was
  redirected to build Prometheus on Prometheus instead of relaying
  through ouranos.
- Checked but found nothing to remove by hand: `/nix/var/nix/gcroots/auto`
  (stale indirect roots from old `result` symlinks under other flows'
  worktrees are pruned automatically by `nix-collect-garbage`, not by
  manual `rm`), `/nix/var/nix/temproots` (only small in-flight lock files
  from the current session, all under a few MB each), and
  `/nix/store` top level for stray `.tmp`/`-tmp-`/`.check` names (none
  found beyond ordinary `Cargo.lock`/`Gemfile.lock` derivation outputs,
  which are normal build inputs, not scratch).

## What was deliberately not touched

- Any `/tmp` content not identified as `nix-build-*` scratch, a dead GC
  root, or deployment-31 download/build debris. `/tmp` is still ~43G:
  mostly other flows' live Rust `target/` build directories, active
  Claude/Codex session scratch (`/tmp/claude-1001/...`), browser
  (`cdp-*`, `com.google.Chrome.*`) state, and old evidence-gathering
  artifacts from unrelated completed flows (e.g. `lojix-v4-inspection.*`,
  `lojix-evidence-reader.*`, `lojix-skill-examples-*`). None of these are
  understood to be deployment-31 debris, and several are plainly live
  (`/tmp/prometheus-5f38bc-direct-inputs`, `/tmp/prometheus-recovery-remote-smoke`
  belong to the concurrently active field-astra/5f38bc flow's own
  Prometheus work) — out of this task's authorization and risky to touch.
- All Nix system generations, pinned or not: not critically short on
  space, so none were retired. Both the booted and current generations
  are intact regardless.
- No repository checkouts, worktrees, or anything under
  `/home/li/primary/flows`.
- No `sudo`-only actions (generation deletion, direct store-permission
  changes) were attempted; the account had no passwordless `sudo` and
  none was used.

## After

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme0n1p2  916G  696G  174G  81% /
```

Net freed: ~7 GiB (167G -> 174G available; 703G -> 696G used). Booted
and current system generations unchanged (same two store paths as
before).
