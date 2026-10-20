# Recency/frequency GC for a Nix builder-cache

Research done 2026-10-16. The question was how to collect garbage on a remote build machine that also serves the cluster's cache. The goal was to collect by how recently and how often paths were used, not by GC roots. Clients would keep only their in-use profiles.

Sources were read directly. Nix source is pinned at tag `2.35.1`, the version installed here (`nix --version`). Other repos were read at their default-branch HEAD on the date above. github.com and codeload were unreachable from this host, so files were fetched from raw.githubusercontent.com.

## What Nix itself records and offers

### No access time or use count in the store database

- `ValidPaths` has the columns `id, path, hash, registrationTime, deriver, narSize, ultimate, sigs, ca`. It has no column for last access or use count.
  https://raw.githubusercontent.com/NixOS/nix/2.35.1/src/libstore/schema.sql
- `registrationTime` is set once, when the path becomes valid: `info.registrationTime == 0 ? time(nullptr) : ...` in `LocalStore::addValidPath`. It records when a path was built or substituted. It does not record use.
  https://raw.githubusercontent.com/NixOS/nix/2.35.1/src/libstore/local-store.cc (around line 717)
- Every store file's mtime is reset to 1 (`mtimeStore = 1`), so mtime carries no signal.
  https://raw.githubusercontent.com/NixOS/nix/2.35.1/src/libstore/posix-fs-canonicalise.cc
- Serving a path writes nothing to the store database:
  - The daemon's `NarFromPath` handler, used by ssh-ng and by `nix copy` through the daemon, only calls `store->narFromPath(path, conn.to)`, which streams the NAR.
    https://raw.githubusercontent.com/NixOS/nix/2.35.1/src/libstore/daemon.cc (line 906)
  - Harmonia reads the SQLite database directly ("no nix-daemon connection is used") and streams files.
    https://github.com/nix-community/harmonia (README)
  - nix-serve likewise only reads.
- The only side effect of serving is the filesystem **atime** of the files read. Whether that updates depends on mount options. On this host `/nix/store` is ext4 mounted `relatime`. Because mtime is 1, relatime updates atime at most once every 24 hours per inode. That gives day-granularity recency, and no count.

### Built-in GC knobs, all reachability-based

- `nix-store --gc --max-freed N` deletes dead paths until N bytes are freed. The order is the raw `readdir()` order of `/nix/store`, which is effectively the order of the hashes, so it is random with respect to use. Size and age are not considered.
  https://raw.githubusercontent.com/NixOS/nix/2.35.1/src/libstore/gc.cc (around lines 790-820 and 569)
  Manual: https://nix.dev/manual/nix/2.31/command-ref/nix-collect-garbage
- `min-free` / `max-free` / `min-free-check-interval`: when free space drops below `min-free`, an automatic GC runs with `maxFreed = max-free - avail`. It uses the same random order (gc.cc around lines 925-965).
  https://nix.dev/manual/nix/stable/command-ref/conf-file
- `keep-outputs` / `keep-derivations` only widen what counts as live: outputs of live .drv files, and derivers of live outputs (gc.cc around lines 600-710). Both are `true` on this host (`nix config show`).
- `--delete-older-than` / `--delete-generations` act on **profile generations**, not on store paths.
- NixOS: `nix.gc.{automatic,dates,options,randomizedDelaySec,persistent}` wraps `nix-collect-garbage ${options}`; `nix.settings.min-free` / `max-free`.
  https://raw.githubusercontent.com/NixOS/nixpkgs/nixos-unstable/nixos/modules/services/misc/nix-gc.nix

## Third-party tools

| Tool | What it deletes and how it decides | Maturity | NixOS integration |
|---|---|---|---|
| **nix-heuristic-gc** (risicle) | Asks Nix for the dead set (`GCReturnDead`). Ranks it greedily by the **max atime over the path's files**. Optional weights for size, inode count, .drv files, invalid paths and substitutability. `--inherit-atime` passes a referrer's atime down to its references. Deletes through `GCDeleteSpecific` until a byte or inode limit is reached. | The author calls it "mostly intended as a testbed". It does not hold the GC lock between selection and deletion, and "may not work (at all) well with both keep-derivations and keep-outputs". nixpkgs has v0.7.4, built against Nix 2.31. | Package only, no module. Run it from your own systemd timer. |
| **angrr** (linyinfeng) | Deletes **GC roots**, not store paths. Temporary roots (direnv, `result*`) go by the **mtime of the root symlink** older than a period, and `angrr touch` refreshes them. Profile generations go by `keep-since`, `keep-latest-n` and buckets. Runs before `nix-gc.service`. | Active. v0.2.7 in nixpkgs unstable; the README warns that 25.11 ships v0.1.1. | `services.angrr` module, with a NixOS test. |
| **nix-sweep** (jzbor) | Removes profile generations by age and minimum count, and lists or removes leftover GC roots. Interactive presets. | v0.8.0 in nixpkgs. Contributions not accepted. | Package only. |
| **Attic** (zhaofengli) | Separate S3/DB-backed cache, not `/nix/store`. Every NAR fetch calls `bump_object_last_accessed` (`get_nar`). GC deletes objects with `created_at < cutoff AND (last_accessed_at IS NULL OR < cutoff)` for each cache's `retention_period`. It does not walk closures. | "Early prototype." | `services.atticd`. |
| **Cachix** | Hosted. "Sorts all store paths by their last accessed date or creation date if the path was never accessed" and deletes the oldest until under the storage limit. | Commercial service. | Not applicable. |
| **Harmonia** | Serves the local `/nix/store`. Has no GC. Exposes the actix access log (`RUST_LOG`) and Prometheus `harmonia_http_requests_total`, labelled by method, path and status. | Mature, nix-community. | `services.harmonia`. |

Sources:
- https://github.com/risicle/nix-heuristic-gc (README, `nix_heuristic_gc/graph.py`, `__init__.py`)
- https://raw.githubusercontent.com/NixOS/nixpkgs/nixos-unstable/pkgs/by-name/ni/nix-heuristic-gc/package.nix
- https://discourse.nixos.org/t/nix-heuristic-gc-a-more-discerning-cousin-of-nix-collect-garbage/27472
- https://github.com/linyinfeng/angrr (README)
- https://raw.githubusercontent.com/NixOS/nixpkgs/nixos-unstable/nixos/modules/services/misc/angrr.nix
- https://github.com/jzbor/nix-sweep
- https://discourse.nixos.org/t/nix-sweep-clean-up-old-nix-profile-generations-and-left-over-garbage-collection-roots/66428
- https://github.com/zhaofengli/attic (`server/src/gc.rs`, `server/src/api/binary_cache.rs`)
- https://docs.cachix.org/garbage-collection
- https://github.com/nix-community/harmonia

No tool was found that collects a plain `/nix/store` by frequency of use. Only Attic and Cachix track last access, and only in their own databases.

## Limits of atime as the signal

1. **No frequency.** atime gives only the last access, and only at about 24-hour resolution under relatime. A use count needs our own log, for example by parsing harmonia's access log for `/<hash>.narinfo` and `/nar/...` requests. Requests over ssh-ng and builds on the builder itself leave no log by default.
2. **auto-optimise-store hard links.** `auto-optimise-store = true` here, and the builder should be checked for the same setting. Identical files share one inode through `/nix/store/.links`, so reading a file in path A bumps the atime of the same file in path B. Common files make unrelated paths look recent.
3. **Bulk readers reset atime everywhere.** `nix-store --optimise`, `nix store verify --check-contents`, backups and indexers all read every file. They should be run with `noatime`, or not on this store.
4. **Mount options.** `noatime` disables the signal entirely. `strictatime` gives exact last access but writes on every read.
5. **Builds count as use.** A sandboxed build reads its inputs, so build-time dependencies stay "recent" while builds keep using them. That is probably what we want.
6. **Closure consistency.** When paths are ranked one by one, an old dependency of a recent path can look stale. nix-heuristic-gc only deletes paths that are already dead, so it cannot break a live closure, and `--inherit-atime` handles this case for dead closures.

## Where a "registry" profile fits

Roots on the builder would be:
- its own system profile;
- one registry profile, for example `/nix/var/nix/profiles/registry`, listing builds worth keeping no matter how recently they were used;
- Nix's temporary roots for builds in flight.

Everything else is dead to Nix and is ranked by recency for deletion.

Notes:
- **Generations.** Every edit to the registry makes a new generation, and old generations are roots too. Delete them after each update with `nix-env -p … --delete-generations old` or `nix profile wipe-history`, or with an angrr `profile-policies` entry with `keep-latest-n = 1`.
- **Conflicts.** A `nix profile` built with buildEnv merges files, so two builds that ship the same file path conflict. Two ways to avoid that:
  - Install one generated derivation whose closure references every kept path, such as a `linkFarm` or a text file of store paths, as a single profile element.
  - Use plain indirect roots, `nix-store --add-root /nix/var/nix/gcroots/registry/<name> -r <path>`. This avoids profiles altogether.
- **keep-outputs / keep-derivations.** With both enabled, a registry entry that is a .drv also keeps its build outputs. With them disabled, the registry must name outputs.

## Simplest fit

Use the registry root on the builder, and run nix-heuristic-gc from a systemd timer, for example `nix-heuristic-gc --inherit-atime --penalize-drvs <bytes>`, or with a limit computed from free space.

Why: it is the only existing collector that ranks a plain `/nix/store` dead set by recency. It deletes through Nix's own `GCDeleteSpecific`, so it never removes anything Nix's GC would keep. The signal it uses, atime, is the only usage trace the store leaves, and harmonia and ssh-ng serving do update it.

Accept its caveats:
- testbed maturity;
- the race without the GC lock;
- the keep-outputs/keep-derivations caveat;
- atime contamination from hard links and bulk readers.

Frequency needs our own counter, most cheaply harmonia's access log aggregated per store hash. Such a counter could later replace atime as the ranking input to a small wrapper around `nix-store --gc --print-dead` and `nix-store --delete`.
