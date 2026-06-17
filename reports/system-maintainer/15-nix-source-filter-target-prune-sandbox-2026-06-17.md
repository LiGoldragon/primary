# Nix source-filter target traversal — sandbox diagnosis and repair shape — 2026-06-17

## Question

Follow-up from report 14: the suspicious line was that some Nix source filters allow every directory, which may make Nix walk huge Rust `target/` trees. The user asked to find the source of all those problems and test solutions in a sandbox.

## Short answer

The source is broader than the explicit `type == "directory" || ...` expressions. `craneLib.filterCargoSources` itself returns true for directories, including `target/` and `.git`, so any `pkgs.lib.cleanSourceWith` filter that calls `craneLib.filterCargoSources` without a prior prune guard can still traverse huge build/cache trees.

The safe repair shape is not to hand-tighten every repo's schema/script include logic first. Put a prune guard in front of the existing predicate:

```nix
let
  prunedSourceDirectory = path: type:
    type == "directory" && builtins.elem (builtins.baseNameOf path) [
      ".git"
      ".jj"
      ".direnv"
      "node_modules"
      "target"
    ];
in
(!prunedSourceDirectory path type) && (
  # existing source filter body unchanged
  craneLib.filterCargoSources path type
  || schemaFilter path type
  || scriptFilter path type
)
```

For repos that currently start with `type == "directory" || ...`, keep the existing include behavior behind the same guard during the first cleanup:

```nix
(!prunedSourceDirectory path type) && (
  type == "directory"
  || craneLib.filterCargoSources path type
  || schemaFilter path type
)
```

That preserves source inclusion while preventing descent into the heavyweight cache/build directories.

## Sandbox tests

Sandbox path: `/tmp/nix-source-filter-sandbox`.

The sandbox contained:

- ordinary Cargo files: `Cargo.toml`, `Cargo.lock`, `src/main.rs`;
- extra build data: `schema/`, `scripts/`;
- fake cache/history trees: `.git/objects/*`, `target/debug/deps/layer1/layer2/*.o`.

Three filter shapes were tested with Nix `builtins.path` plus `builtins.trace`:

| Filter | Included files | Trace lines | Target trace lines | Git trace lines |
|---|---:|---:|---:|---:|
| broad `type == "directory" || ...` | same intended files | 157 | 125 | 22 |
| plain `craneLib.filterCargoSources` | target files rejected, dirs allowed | 158 | 125 | 22 |
| prune guard before existing predicate | same intended files | 12 | 1 | 1 |

Both the broad filter and crane's own cargo-source filter visited every fake target object. Neither included those files in the final source. The cost is traversal/source filtering, not copied target artifacts.

The pruned filter still included exactly the intended source/data files:

```text
Cargo.lock
Cargo.toml
schema/nested/child.schema
schema/root.schema
scripts/check.sh
src/main.rs
```

It excluded target and git files, and traced only the top-level rejected `target` and `.git` directories.

## Real-repo sandbox check

Without editing the repositories, I applied the same pruned predicate through a temporary Nix expression to two large real repos:

| Repo | Trace lines with pruned predicate | Target trace lines | Git trace lines | JJ trace lines |
|---|---:|---:|---:|---:|
| `spirit` | 87 | 1 | 2 | 1 |
| `cloud` | 41 | 1 | 2 | 1 |

That confirms the guard prunes the large target trees in real checkouts while still allowing normal source traversal.

## Affected active repos

The active-public scan found 63 flakes using `craneLib.filterCargoSources` or `cleanCargoSource` through a source-cleaning path with no target/cache prune guard. All should be considered affected by the general traversal problem:

| Repository | Explicit global `type == "directory"` too? |
|---|---|
| `chroma` | no |
| `chronos` | no |
| `cloud` | yes |
| `criome` | no |
| `domain-criome` | yes |
| `harness` | no |
| `horizon-rs` | no |
| `introspect` | no |
| `lojix-cli` | no |
| `mentci-lib` | no |
| `message` | yes |
| `meta-signal-agent` | no |
| `meta-signal-cloud` | no |
| `meta-signal-criome` | no |
| `meta-signal-domain-criome` | no |
| `meta-signal-mind` | yes |
| `meta-signal-orchestrate` | no |
| `meta-signal-persona` | yes |
| `meta-signal-repository-ledger` | no |
| `meta-signal-router` | yes |
| `meta-signal-spirit` | no |
| `meta-signal-terminal` | no |
| `meta-signal-upgrade` | no |
| `meta-signal-version-handover` | no |
| `mind` | yes |
| `nexus` | no |
| `nexus-cli` | no |
| `nota-config` | no |
| `nota-next` | yes |
| `orchestrate` | no |
| `persona` | no |
| `repository-ledger` | no |
| `router` | no |
| `schema-next` | yes |
| `schema-rust-next` | no |
| `sema` | no |
| `sema-engine` | no |
| `signal` | no |
| `signal-agent` | yes |
| `signal-cloud` | no |
| `signal-criome` | no |
| `signal-domain-criome` | no |
| `signal-harness` | no |
| `signal-introspect` | no |
| `signal-message` | yes |
| `signal-mind` | no |
| `signal-orchestrate` | no |
| `signal-persona` | yes |
| `signal-repository-ledger` | no |
| `signal-router` | yes |
| `signal-sema` | no |
| `signal-spirit` | no |
| `signal-system` | no |
| `signal-terminal` | no |
| `signal-upgrade` | no |
| `signal-version-handover` | no |
| `spirit` | no |
| `system` | no |
| `terminal` | no |
| `terminal-cell` | no |
| `triad-runtime` | no |
| `upgrade` | no |
| `version-projection` | no |

The explicit global directory-allow subset is 13 repos: `cloud`, `domain-criome`, `message`, `meta-signal-mind`, `meta-signal-persona`, `meta-signal-router`, `mind`, `nota-next`, `schema-next`, `signal-agent`, `signal-message`, `signal-persona`, and `signal-router`.

## Why regex-scoped filters are not enough

Some repos do not have a global `type == "directory"`; instead they have scoped extras like:

```nix
(type == "regular" || type == "directory")
&& (builtins.match ".*/schema(/.*)?" path != null)
```

Those are less risky by themselves, but they still sit next to `craneLib.filterCargoSources`, which permits all directories. Also, absolute `.*` regexes can match generated/build paths if a build tree contains a `schema`, `scripts`, `examples`, or similar segment. The prune guard solves both concerns before any include predicate runs.

## Recommended implementation plan

1. Add a local `prunedSourceDirectory` helper near each `sourceFilter` / `filter = path: type:` block.
2. Wrap the existing filter body with `(!prunedSourceDirectory path type) && (...)`.
3. Do not initially rewrite every schema/examples/scripts predicate; preserve behavior first, prune cache/build traversal first.
4. For the 13 explicit global directory-allow repos, do not merely delete `type == "directory"`; crane still permits all directories. Add the guard.
5. After the broad guard lands everywhere, a second cleanup can make extras root-anchored (`schemaRoot = "${toString ./.}/schema"`) instead of absolute `.*` regexes.

## Test command shape for each real repo after patching

For each patched repo:

```sh
nix flake check --no-build
nix build --no-link .#checks.<system>.<small-check>
```

Where a repo has no cheap check, evaluate or build the default package only after the patch is committed/pushed per normal Nix discipline. For local sandbox confidence before a full build, run a temporary trace expression that applies the repo's patched predicate to the working tree and verifies only one `target` trace line appears: the top-level rejected directory.

## Bottom line

The first repair should be a uniform prune guard, not an ad hoc set of narrow source-filter rewrites. The sandbox proves it keeps the same intended source files while eliminating target/git traversal. The affected set is essentially every active Rust flake using crane source filtering without an explicit prune guard, with 13 repos having an additional obvious `type == "directory"` broadening line.
