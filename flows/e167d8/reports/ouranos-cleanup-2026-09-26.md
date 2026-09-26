# Ouranos model purge and GC — 2026-09-26

## Space
- `/nix` (root fs `/`) before: 916G total, 854G used, **16G free** (99%).
- After: 916G total, 726G used, **144G free** (84%).
- `nix-collect-garbage -d`: 13,720 store paths deleted, 126.9 GiB freed.
- Follow-up `nix-store --gc`: 0 additional (already clean).

## Removed
- GC roots holding model weights, both under `/home/li/.local/state/`:
  - `b860be-gcroots/gemma-{1,2,3}` → Gemma-4-26B-A4B-it-BF16 shards + mmproj (~48.8 GiB), the tonight pre-seed for a Prometheus deploy.
  - `da88cf-gcroots/qwen-shard-{1,2,3}` → Qwen3.5-122B-A10B-Q4_K_M shards (~72 GiB), also pre-staged for a pending deploy.
  - The earlier b7da5d ruling to preserve the Gemma pre-seed is superseded by the living's order this morning.
- `nix-collect-garbage -d` then removed all superseded profile/home-manager/user-environment generations (system, home-manager, per-user, per-worktree `result` links) whose backing store paths became unreachable once the model roots and other dead roots were gone.
- Signal from Field Luna (b860be) about a ~28.7 GiB stale old-Claude scratchpad out-link matches indirect roots under `/tmp/claude-1001/.../scratchpad/*`; these are dangling (their `/tmp` sources no longer exist after reboot/session end) and were reclaimed by the GC pass automatically.

## Kept, and why
- `/run/current-system` and `/run/booted-system` (differ: current build `hm7zclf0...`, booted `8cvwmgdkvqhn...` per Luna's note — both are live roots, left alone).
- `/nix/var/nix/profiles/system` (system-188, the same as current-system).
- The two Lojix audit roots, `/var/lib/lojix/audits/bird-zeus-8e9fd484` and `bird-zeus-9ef4d609` (~29 GiB each) — untouched, separate ruling needed.
- `da88cf-gcroots/messenger-clj-0.2.5` — not a model, left in place.
- No model files found outside the store on ouranos: no `/var/lib/ollama`, no `.gguf`/`.safetensors` under `/home`; `ollama` only appears as Nix-store derivations/packages, no live weights.

## Widened checks (from later instructions)
- **Other nodes**: only `zeus.goldragon.criome` was reachable besides ouranos/Prometheus (`tiger`, `vm-testing`, `mirror-alpha`, `mirror-beta` all timed out/unreachable from here). Zeus's GC roots and home/var searched for `.gguf`/`.safetensors`/ollama: **none found**; 188G avail, 58% used.
- **Old profiles/build dirs/worktrees/primary-dedup** (the "nick"→Nix widening): only `nix-collect-garbage -d` + `nix-store --gc` were run on ouranos this pass. A full manual audit of `/home/li/wt` worktrees, stray `primary` clones, and build-directory sweep on ouranos was **not done** — verifying unpushed work per worktree before deletion needs more time/turns than this pass had; recommend a dedicated follow-up pass rather than a blanket delete.
- **Prometheus closure builder**: `goldragon/cluster-definition.datom` gives Prometheus the `NixBuilder.Some.8` feature (it offers itself as a build resource to the cluster) and `tiger` has `NixBuilder.None`; ouranos carries no `NixBuilder` feature. Nothing in the declared cluster/CriomOS source assigns another node as Prometheus's own builder — deploy-time builder choice is an explicit per-request field in Lojix (`Deploy.Host` field 13), not fixed in source. One live-witnessed exception, found in `flows/31147a/log.md` (dirty in tree, committed separately): "Older Lojix 7 Prometheus Realize builds in Ouranos store and imports outputs/model files back there despite remote derivation offload" — i.e. in practice, a Prometheus Realize was run *from* ouranos with local remote-builder-style import, landing outputs (potentially model-bearing) in ouranos's store. That is the likely mechanism by which the Gemma/Qwen shards ended up rooted on ouranos rather than staying on Prometheus.
- ouranos's own declared closure was reported by the living as not pulling in any model/model-serving service; not independently re-audited this pass per that instruction.

## Gemma copy purpose
The `b860be-gcroots/gemma-*` roots and their naming ("pre-seed") match a staging copy meant to be evaluated/built toward a Prometheus deploy from ouranos, not a service meant to run on ouranos itself — consistent with the Route A note above describing Realize/import flows that stage Prometheus-bound model outputs through ouranos's store.
