# Prometheus builder capacity

**Live (ssh -o BatchMode=yes prometheus):** nproc 32, RAM 124G/60G free,
load 0.53/0.31/0.22 (idle), 32 nixbld users, `nix show-config`: cores=6,
max-jobs=6, build-users-group/allowed-uris unset, nix-daemon has no
CPU/nice limit unit (only LimitNOFILE=1048576).

**Cluster datom** (`goldragon-cluster-definition.datom`, prometheus record):
`NixBuilder.Some.6` — the *only* capacity field; `Metal.{ ... 8 ... }` cores
figure is stale (real box is 16c/32t GMKtec EVO-X2, not 8).

**CriomOS wiring** (single field drives both sides):
- `horizon-rs/lib/src/proposal.rs:457` `nix_builder_maximum_jobs()` reads
  `NixBuilder{maximum_jobs}` straight off the datom.
- `horizon-rs/lib/src/node.rs:420-421`: `max_jobs = nix_builder_maximum_jobs().unwrap_or(1); build_cores = max_jobs;` — **cores is not independent, it copies max_jobs**.
- `modules/nixos/nix/builder.nix` `buildMachineFor`: emits that same
  `maxJobs` into ouranos's `/etc/nix/machines` (`nix.buildMachines.*.maxJobs`).
- `modules/nixos/nix/client.nix`: `dedicatedNixBuilder` branch sets
  Prometheus's own `nix.settings.max-jobs`/`cores` from `node.maxJobs`/`node.buildCores`.

So the six-slot cap is **both**: ouranos's machines-file `maxJobs` and
Prometheus's own `max-jobs`/`cores` — one datom, two consumers.

**Repo's own rule** (`horizon-rs/docs/BUILD_CORES.md`): dedicated builder
should be `max_jobs = cores, build_cores = 0` (unlimited); doc's own
formula is unused by this direct path. For 32 threads, ~4GB/job budget
(124G/32≈3.9G) → max-jobs ≈ cores/4 fits RAM better than max_jobs=cores.

**Proposal** (no edit made):
```
NixBuilder.Some.8
```
on the prometheus node record, plus decoupling `build_cores` from
`max_jobs` in `node.rs:421` to `let build_cores = 0;` so Nix gets
`max-jobs=8, cores=0` (unlimited per-build) — saturates 32 threads
(8×4≈32) without RAM pressure, vs. today's 6×6=36 undersubscribed.
