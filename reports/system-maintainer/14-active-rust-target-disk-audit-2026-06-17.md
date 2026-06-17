# Active Rust target disk audit — 2026-06-17

## Question

The user noticed unexpectedly large Rust compile `target/` directories and asked whether active repositories are accidentally carrying fetched source duplicates, nested targets, full version-control histories, or some other fishy shape.

## Method

Scope was the public active-repository map in `protocols/active-repositories.md`: 73 existing public active paths under `/git/github.com/LiGoldragon/...` plus `/home/li/primary`. I did not inspect `private-repos/` and did not search `/nix/store`.

Checks performed:

- repository total size split into root `target/`, `.git`, `.jj`, and other bytes;
- recursive `target/` directories outside `.git`, `.jj`, `node_modules`, and `.direnv`;
- `target/debug` composition for the largest Rust repositories;
- global Cargo source caches under `~/.cargo`;
- non-active worktree `target/` directories under `~/wt/github.com/LiGoldragon`;
- nested `.git` / `.jj` directories;
- whether `target/` is tracked or ignored;
- flake source-filter patterns that could make Nix walk build-output trees;
- lockfile duplicate dependency sources/versions.

## Main finding

There is no evidence that active repo size is dominated by fetched source trees, nested repository histories, or committed `target/` artifacts. The active public working-set size is almost entirely ordinary Cargo build output, multiplied across many independent repos.

Aggregate active-public split:

| Bucket | Size |
|---|---:|
| all inspected active repo bytes | 118GB |
| root `target/` directories | 116GB |
| `.git` directories | 1.2GB |
| `.jj` directories | 863MB |
| other checked-out files | 456MB |
| share in `target/` | 97.9% |

There are 67 Rust repos in scope, 66 with a `target/` directory. `target/` is ignored everywhere it exists, and `git ls-files target` found no tracked target artifacts.

## Largest active `target/` directories

| Repo | `target/` size | Notes |
|---|---:|---|
| `spirit` | 15GB | Huge `debug/deps`, incremental cache, many test/dev artifacts. |
| `persona` | 9.4GB | Debug deps plus many executable-like test artifacts. |
| `router` | 7.4GB | Debug deps + 3.4GB incremental. |
| `terminal` | 6.1GB | Debug deps, terminal/test artifacts, older transitive crate versions. |
| `mind` | 5.6GB | Incremental cache is larger than deps; has duplicate `kameo` source issue. |
| `criome` | 5.0GB | Repeated large `libcriome` artifacts. |
| `cloud` | 4.8GB | Debug deps and build-script output. |
| `terminal-cell` | 3.6GB | Same Rust-cache pattern. |
| `domain-criome` | 3.2GB | Same Rust-cache pattern. |
| `introspect` | 3.0GB | Same Rust-cache pattern. |

The global Cargo cache is not the culprit: `~/.cargo` was 722MB total, with only 92MB in Cargo git caches and 630MB in the registry cache. Cargo's fetched git DB/checkouts are small compared with repo-local `target/` directories.

## What is inside the largest target directories

Representative `target/debug` splits:

| Repo | `debug/deps` | `debug/incremental` | `debug/build` |
|---|---:|---:|---:|
| `spirit` | 8.5GB | 4.3GB | 1.3GB |
| `persona` | 6.9GB | 1.7GB | 893MB |
| `router` | 3.5GB | 3.4GB | 388MB |
| `terminal` | 4.6GB | 1.3GB | 235MB |
| `mind` | 2.6GB | 2.9GB | 169MB |
| `criome` | 3.1GB | 1.7GB | 241MB |
| `cloud` | 3.3GB | 1.1GB | 361MB |

This is the normal shape of large debug builds: rlibs, test binaries, proc-macro/build output, and incremental state. The duplicate-looking files are mostly Cargo's hashed artifacts for the same crate compiled under different feature/profile/test contexts. Examples:

| Repo | Duplicate artifact pattern |
|---|---|
| `spirit` | 85 `spirit` artifacts totaling 799MB; 35 `signal_spirit` artifacts totaling 368MB; 110 executable-like files in `debug/deps`. |
| `persona` | 28 `persona` artifacts totaling 488MB; 90 executable-like files. |
| `router` | 38 `router` artifacts totaling 455MB; large `librouter` rlibs. |
| `criome` | 60 `criome` artifacts totaling 788MB. |
| `cloud` | 46 `cloud` artifacts totaling 373MB. |

The largest top-level targets were all recently modified; this is not mainly ancient stale data.

## Red herrings ruled out

- **Full VCS histories in each project**: not the cause. Most `.git` + `.jj` totals are tens of MB or less. The main exception is `primary`, whose `.git` + `.jj` are about 1017MB, but `primary` has no Rust root `target/` and is not part of the Rust compile-size issue.
- **Nested repositories under active repos**: no meaningful nested `.git` / `.jj` directories showed up outside repo roots, after excluding build-output and tool-cache directories.
- **Tracked target artifacts**: none found.
- **Cargo-fetched source trees with their own targets**: no evidence in active repo trees. Cargo git checkouts under `~/.cargo` are small and do not explain the 116GB.

## Actual fishy items

### 1. Per-repo target duplication across the active stack

The dominant issue is architectural/tooling shape: many small component repos each have their own `target/`, but they compile overlapping dependency graphs: `schema-next`, `schema-rust-next`, `sema-engine`, `signal-frame`, `triad-runtime`, `nota-next`, `tokio`, `rkyv`, `rend`, etc. Cargo shares source fetches globally, but it does not share compiled artifacts across independent target directories.

That means the same large dependency graph is compiled into dozens of independent `target/debug/deps` trees. This explains the scale better than fetched source duplication.

### 2. Broad Nix source filters may walk `target/` trees

Several flakes use a source filter shape like:

```nix
type == "directory" || craneLib.filterCargoSources path type || schemaFilter path type
```

Observed in active repos including `cloud`, `domain-criome`, `message`, `meta-signal-mind`, `nota-next`, `schema-next`, `signal-agent`, and `signal-message`; similar broad directory allowances appear in parts of `mind` and related repos.

This probably does **not** copy `.rlib`/`.o` files into Nix source derivations, because regular files under `target/` are still rejected by `craneLib.filterCargoSources`. But it is still fishy because Nix may need to descend through huge ignored build trees during source filtering. That can make evaluation/source-copy operations unexpectedly slow or memory-heavy. The safer pattern is to allow directories only when they are part of the cargo/schema/script include set, or rely on `craneLib.filterCargoSources` for directory traversal and add narrow directory matches for `schema/`, `scripts/`, etc.

### 3. `mind` has a true same-version duplicate source

`mind` contains both crates.io `kameo v0.20.0` and a git fork of `kameo v0.20.0`, plus both corresponding `kameo_macros`. `cargo tree -d --locked --no-default-features` showed:

- `kameo v0.20.0` from crates.io via `triad-runtime`;
- `kameo v0.20.0` from `LiGoldragon/kameo` branch `persona-lifecycle-terminal-outcome` directly in `mind`.

That is a real duplicate-source problem, not just normal Cargo artifact hashing. It is probably not the whole 5.6GB, but it is the kind of graph mismatch that wastes compile time and bytes and can cause type-identity surprises if shared types ever cross the boundary.

### 4. `spirit` intentionally carries old `sema-engine` revisions

`spirit` has multiple `sema-engine` versions/revisions in its lockfile (`0.2.3`, `0.4.0`, `0.6.2`) because its manifest names previous/layout engines for migration/testing. This is plausibly intentional, but it is a real contributor to extra compile artifacts. If the old migration fixtures are no longer needed in routine developer builds, gating them behind narrower features or moving them to a dedicated migration-test profile would reduce default target growth.

### 5. Worktree targets add extra pressure

Outside canonical active checkouts, `~/wt/github.com/LiGoldragon` has additional target directories, especially:

| Worktree target | Size |
|---|---:|
| `spirit/mirror-shipper/target` | 4.2GB |
| `spirit/guardian-positive-guidance/target` | 3.2GB |
| `criome/language-content-addressed-bls/target` | 1.7GB |
| `schema-next/reaction-expand/target` | 744MB |
| `schema-rust-next/reaction-expand/target` | 701MB |

These are not in the active-repo aggregate above, but they are additional local disk use from the same per-worktree target model.

## Recommendations

1. **Safe immediate reclaim**: remove selected repo-local `target/` directories when no agent is compiling in that repo. Biggest wins are `spirit`, `persona`, `router`, `terminal`, `mind`, `criome`, and `cloud`. This can reclaim tens of GB, at the cost of a slow next compile.
2. **Fix the broad flake source filters**: replace global `type == "directory" || ...` filters with narrow directory predicates. This is the most suspicious Nix-side issue found.
3. **Unify or centralize developer target storage**: consider a deliberate shared `CARGO_TARGET_DIR` for the active Persona stack, or a few shared target dirs by stack/toolchain. This moves bytes out of repo trees and lets identical package IDs reuse artifacts. It may introduce Cargo lock contention and should be deliberate, not a hidden shell accident.
4. **Consider `sccache` for developer builds**: a compiler cache would attack repeated dependency compilation without forcing one shared mutable target tree for every repo.
5. **Clean dependency-source duplicates**: start with `mind`'s forked-vs-crates.io `kameo` split; then decide whether `spirit`'s old `sema-engine` revisions are still needed in default/dev builds.
6. **Add a recurring audit command**: a small workspace script could report top `target/` sizes, worktree targets, broad source-filter patterns, and `cargo tree -d` duplicate-source warnings without deleting anything.

## Bottom line

The weirdness is real, but it is mostly not hidden source/history duplication. It is the cost of dozens of active independent Rust repositories compiling the same large ecosystem into separate debug target directories, amplified by incremental caches and test artifacts. The most concrete bugs/smells are the broad Nix source-filter directory predicates and `mind`'s duplicated `kameo` source.
