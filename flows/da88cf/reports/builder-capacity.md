# Prometheus builder capacity

**Live** (ssh -o BatchMode=yes prometheus): nproc 32, RAM 124G/60G free,
load 0.53/0.31/0.22 (idle), 32 nixbld users; `nix show-config`: cores=6,
max-jobs=6; no daemon CPU/nice limit (only LimitNOFILE=1048576).

**Cluster datom** (`goldragon-cluster-definition.datom`, prometheus record):
`NixBuilder.Some.6` is the only capacity field (the record's `Metal` cores
figure of 8 is stale; box is 16c/32t GMKtec EVO-X2).

**CriomOS wiring** — one field, two consumers:
- `horizon-rs/lib/src/proposal.rs:457` `nix_builder_maximum_jobs()` reads
  `NixBuilder{maximum_jobs}` off the datom.
- `horizon-rs/lib/src/node.rs:420-421`: `max_jobs = ...unwrap_or(1); build_cores = max_jobs;` — cores just copies max_jobs, not independent.
- `modules/nixos/nix/builder.nix` emits that `maxJobs` into ouranos's
  `/etc/nix/machines` line.
- `modules/nixos/nix/client.nix` sets Prometheus's own
  `nix.settings.max-jobs`/`cores` from the same `node.maxJobs`/`buildCores`.

So the six-slot cap is **both** ouranos's machines-file maxJobs and
Prometheus's own max-jobs/cores.

**Repo's rule** (`horizon-rs/docs/BUILD_CORES.md`): dedicated builder →
`max_jobs=cores, build_cores=0` (unlimited); unused by this direct path.
~4GB RAM/job (124G/32) favors max-jobs≈cores/4 over max_jobs=cores.

**Proposal (no edit):** `NixBuilder.Some.8` on prometheus, plus decouple
`node.rs:421` to `build_cores = 0` → `max-jobs=8, cores=0`, saturating
32 threads (8×4) without swapping, vs. today's undersubscribed 6×6.
