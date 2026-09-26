# Prometheus deploy tonight: ouranos store risk

Read-only subflow of da88cf, ouranos, 2026-09-25 ~22:00 CST. Nothing was built, copied, deployed or submitted. One side effect: `nix-store -q --roots` removed a few stale temporary-root files in ouranos's store. Nix does that cleanup on its own. Grades: **W** = witnessed, **I** = inferred.

## 1. How deployment 31 failed (W)

`lojix 'Query.ByDeployment.{ 31 }'` gives:

- Action `TestActivation` at CriomOS `f9343c68`.
- Terminal `Failed.{ Build BuildFailed }`. The command, run on ouranos, was:
  `nix build --no-link --print-out-paths --option max-jobs 0 --builders @/etc/nix/machines /nix/store/s6yprfbk…-nixos-system-prometheus….drv^*`
- The failing step was **substitution into ouranos's store** from `http://nix.prometheus.goldragon.criome` (Prometheus's nix-serve). Downloads either timed out ("Less than 1 bytes/sec … 300 seconds") or ended with "Transferred a partial file". Paths that failed include Nemotron-3-Nano, Qwen3.5-27B, gemma-4-31B, GLM-4.7-Flash, Nemotron-Super-120B shards, and `w0gsg8nz…-mmproj-F16.gguf`.
- The run ended with `error: interrupted by the user`, which was 5f38bc taking the store lock.

The log shows no out-of-space error. The failure was the transfer itself; disk pressure was the latent risk, not the cause.

## 2. How Realize works in Lojix 7.0.0 (`a67f5773`, `src/schema_runtime.rs`) (W)

**Evaluation is local.** `eval_drv_path` deliberately passes no `--store`. The code comment says "an ssh-ng evaluation can deadlock in remote transport".

**The build is local.** `run_nix_build` comments: "An explicit builder still uses the local Nix client and imports its result locally; no deploy stage builds through an ssh-ng target store."
- With a builder: `build_closure_remote` runs `nix build --no-link --print-out-paths --option max-jobs 0 --builders <spec> <drv>^*`.
- Without one: `build_closure` runs the same command minus the builder options.
- Neither uses `--store` or `--eval-store`.

**The copy happens only for activating actions.** `activates()` is true for SetBootProfile, ActivateNow, TestActivation and ScheduleBootOnce. It is false for Evaluate and Realize.
- `ClosureCopy` runs `nix copy --substitute-on-destination --to <store-uri> <toplevel>`.
- `nix copy` skips paths that are already valid on the target.

**Nothing roots the closure on ouranos.** The command uses `--no-link`. Lojix's `GcRoot` is a durable record in its own database, not a link in the filesystem.

**What this means:**
- **Every** Realize or ScheduleBootOnce stores the full toplevel closure in **ouranos's** store, model files included.
- The model files are fixed-output derivations. Ouranos uses `substituters = http://nix.prometheus… https://cache.nixos.org/` with `builders-use-substitutes = true`, so it first tries to fetch them from Prometheus's nix-serve.
- If a fetch fails, the builder in `@/etc/nix/machines` (`ssh-ng://nix-ssh@prometheus…`) runs the fetch on Prometheus. Nix then copies the output **back** into ouranos's store.
- The `Some.@/etc/nix/machines` field changes where derivations run. It does not change where outputs land.
- Neither `Horizon` nor `Direct`, and no other Lojix 7 request field, makes Lojix realize in the target store.
- Running ScheduleBootOnce after Realize **builds again**. That second build is a no-op only if ouranos still holds the paths.

## 3. The two models (W)

Criomos-lib main `6db67c3` has two models, `qwen3.5-122b-a10b` and `gemma-4-26b-a4b` with its mmproj. Their fixed-output paths, evaluated with `pkgs.fetchurl` at nixpkgs `0e251e24` exactly as CriomOS `modules/nixos/llm.nix` calls it:

| Path | Size | Prometheus store | Ouranos store |
|---|---|---|---|
| `cr3yl0w8…-Qwen3.5-122B…-00001-of-00003.gguf` | 10.4 MiB | valid | valid |
| `3dl3vi57…-Qwen3.5-122B…-00002-of-00003.gguf` | 46.5 GiB | valid | valid |
| `24z4j1ln…-Qwen3.5-122B…-00003-of-00003.gguf` | 24.7 GiB | valid | valid |
| `dqr9jn4r…-gemma-4-26B-A4B-it-BF16-00001-of-00002.gguf` | 46.5 GiB | valid | **absent** |
| `xcr75awh…-gemma-4-26B-A4B-it-BF16-00002-of-00002.gguf` | 555 MiB | valid | **absent** |
| `w0gsg8nz…-mmproj-F16.gguf` | 1.1 GiB | valid | **absent** (one of 31's partial downloads) |

- Prometheus was checked with `nix path-info --store ssh-ng://prometheus…`. Its nix-serve returns HTTP 200 for all six narinfos.
- No model needs fetching from Hugging Face.
- On ouranos, the Qwen shards are referenced only by `ma4kv0af…-model-qwen3.5-122b-a10b` → `1ld01ksl…-llm-models-dir`, and `nix-store -q --roots` lists **no roots**. About 71.2 GiB is therefore unrooted, which is very likely the "~80 GiB unrooted path" (**I**).
- `nix-gc.timer` fires at 00:00 and runs `nix-collect-garbage --delete-old`, so it will delete that path.

## 4. Space arithmetic (W for the figures, I for the sums)

Ouranos has 71 GB free (about 66 GiB, 92% used). Prometheus has 1014 GB free.

- **Before 00:00, with Qwen still present:** Realize adds about 48.1 GiB of Gemma plus the non-model closure. About 15 GiB would be left, which is tight but fits. If the non-model closure turns out large, it may not fit.
- **After 00:00 GC:** Qwen is gone, and roughly 137 GiB or more is free. Realize must fetch about 119 GiB of models again from nix-serve. That fits, but it is about 2.5 times the transfer that failed in 31.
- **Realize before 00:00, ScheduleBootOnce after:** the GC sweeps the whole unrooted closure (about 119 GiB) between the two deploys. ScheduleBootOnce then fetches all of it again. This is the worst order.

## 5. Recommended order

1. **Make sure the declared catalogue is really the two-model one.** Remote CriomOS main is still `d193baf`, which pins criomos-lib `6e3bcb08` (the old catalogue). The CriomOS main being integrated must pin criomos-lib `6db67c3`. Before Realize, confirm by checking that the Evaluate's drv references only the six paths above.
2. **Before 00:00, or with a root in place:** keep ouranos from collecting the closure between stages. Two choices:
   - (a) Run Evaluate → Realize → ScheduleBootOnce back to back, finishing before 00:00.
   - (b) Have the owner add a temporary indirect root on ouranos for the Qwen and Gemma paths, and remove it afterwards. This is a store write, and not this subflow's decision.
3. **Pre-seed Gemma over SSH, not nix-serve HTTP.** For example: `nix copy --from ssh-ng://root@prometheus.goldragon.criome <3 gemma paths>`, run on ouranos before Realize. This avoids the nix-serve streaming failure that killed 31. It is an ouranos store write (about 48 GiB); the owner decides.
4. **Realize is redundant with ScheduleBootOnce.** ScheduleBootOnce does its own build, copy and activation. Keep Realize only as a gate, and submit ScheduleBootOnce straight after it succeeds.
5. **Copy stage:** `nix copy --to ssh-ng://root@prometheus…` sends no model bytes, because Prometheus already holds all six paths.

No Lojix 7 option realizes directly in the target store. A mode that never stages on ouranos would need a Lojix change: a `--store`/`--eval-store` build in the target, which the code rejects because of the ssh-ng deadlock.

## Sources

- `lojix 'Query.ByDeployment.{ 31 }'`, saved in the scratchpad as `deploy-store-risk/dep31.txt`.
- Lojix `a67f5773:src/schema_runtime.rs`:
  - `NixInvoking::eval_drv_path` (~7249–7262, 7355–7372)
  - `build_closure` and `build_closure_remote` (7389–7432)
  - `run_nix_build` (5225–5245)
  - `DeployActionShape::activates` (1243–1260)
  - effect router (3435–3470)
  - `ClosureCopy` (6146–6190)
  - `build_target` (1787–1794)
- CriomOS `d193baf:modules/nixos/llm.nix` (`mkModelStorePath`, `mkMmprojFile`).
- CriomOS-lib `6db67c3:data/largeAI/llm.json`.
- `nix path-info` on both stores; nix-serve narinfo probes; `nix-store -q --roots/--referrers` on ouranos.
- `df -h /nix` on both hosts; `/etc/nix/nix.conf`, `/etc/nix/machines`, `nix-gc.timer` and its script on ouranos.
- `flows/da88cf/reports/prometheus-pending.md` §Risk.
- Scratch: `/tmp/claude-1001/-home-li-primary/da88cf8d-06f7-4a70-9c7a-e7c8cdb78908/scratchpad/deploy-store-risk/` (`paths.nix`, `paths.txt`, `llm.json`, `sr.rs`, `dep31.txt`).
