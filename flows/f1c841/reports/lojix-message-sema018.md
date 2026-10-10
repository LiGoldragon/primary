# Lojix and Message on sema-engine 0.18.0

Both landed on their own main, each at its next patch version. Neither needed a source change, and neither store changed.

- lojix 9.0.1, main `fe672bdf6248`: moved from sema-engine 0.15.1 (`27e814a7`) to 0.18.0 (`9884905f`).
- message 0.19.1, main `6fa4d0c1ba19`: moved from sema-engine 0.16.0 (`516f01fe`) to 0.18.0. `flake.nix` carries the new version.

Neither repository used `with_prior` or `EvolutionStep`, so the 0.18.0 change from closures to typed upgrades needed no code. The Home candidate still pins message `ce3eb6c6`; nothing here touches it.

## signal-frame was not dropped

sema-engine 0.16.0 and later no longer use signal-frame, and lojix does not use it directly. But lojix pins triad-runtime 0.8.1 (`02cdd49d`), and triad-runtime still depends on signal-frame 0.3.1. So signal-frame stays in the lock. triad-runtime main is 0.10.1 (`4b8582bd`), which no longer depends on signal-frame. Moving lojix to it would be a separate repin, not started because of the time limit.

## Gates

- `cargo test`: green in both worktrees.
- `nix flake check path:<worktree>`: green for both after the version bump.
  - lojix runs 15 checks, including the NixOS VM tests `same-host-test-activation` and `target-store-realization`.
  - message runs 8 checks.
- The message worktree's parent directory `~/wt/github.com/LiGoldragon/message` contains a stray `.git` that is not ours. Because of it, a plain `nix flake check` refuses with "not tracked by Git". That is why the checks ran against the `path:` form.

## Store-open witness (method)

These checks used throwaway stores under `mktemp -d /tmp/f1c841?.XXXX`, with the runtime and state directories set in the environment.

- **message:** `message-nexus` from the 0.19.0 Nix build (`2nf3ilwwx5q6wfc2pnaxrvgbclk0xjyc`) seeded a fresh store, which holds its configuration. The new build then ran on that same store, then the old build again, then the new build again. Every start bound both sockets and was still alive after the open.
- **lojix:** `lojix-nexus` 9.0.0 from the Nix build (`8py0wmjm…`) created a store. The order was then new, old, new.
  - Every start announced `LojixNexusReady`.
  - Every start answered `Query.ByNode` with `Queried.{ [] [] { 2 2 } }` and `Pin` with `PinRejected.{ GenerationUnknown { 2 2 } }`.
  - After each stop, `lojix-inspect-store` from 9.0.0 read `Schema matches version=5` and found 12 registered tables.
  - The stores contained no rows, so the witness shows the schema and layout open in both directions, not that rows carry across.

## Incident: one start reached the live lojix store path

My first lojix attempt set only `LOJIX_CONFIGURATION`, which `lojix-nexus` ignores. It opens its default store path, `/var/lib/lojix/lojix.sema`.

- Three starts (old, new, old) tried that path.
- Each one failed at once with `redb database: Database already open. Cannot acquire lock`, because the live lojix-nexus 8.1.0 holds the lock.
- None of them served or wrote anything, and the live Nexus was left as it was.
- The witness was then rerun with `XDG_STATE_HOME` and `XDG_RUNTIME_DIR` set.

A Nexus binary with no environment set opens the live store's path. Only redb's lock prevented damage.

## Lock

Lock 11716 (Sema018) covered the two worktrees only. It was released after both pushes, at the coordinator's request.

## Sources

- sema-engine `UPGRADES.md` at `9884905f` (the 0.18.0 entry).
- `cargo tree -i signal-frame` in the lojix worktree.
- lojix `src/lib.rs` (`state_directory`, `store_path`) and `src/daemon.rs` (`from_environment`).
- Worktrees `~/wt/github.com/LiGoldragon/{lojix,message}/sema018-f1c841`.
