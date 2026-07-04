# Full `-next` removal migration evidence

Status: **BLOCKED**. No `drop-next` branch was landed to `main`.

Worker: Worker 2 implementation owner. Date: 2026-07-05.

## Coordination

- Read `/home/li/primary/AGENTS.md`.
- Claimed the migration graph with Orchestrate lane `worker2`.
- Existing claims blocked direct use of `cloud`, `router`, and `signal-spirit`; created isolated JJ clones under `/home/li/primary/worktrees/worker2-next-removal/` and tracked them in bead `primary-1erv`.
- Existing dirty `drop-next` working-copy commits were observed in several claimed repos and left intact. The synchronizer run used remote refs/object stores, not those working copies.

## Synchronizer run

Tool:

```sh
cargo run -- /home/li/primary/agent-outputs/RenamePropagator/worker2-synchronizer-full.nota staged-cascade
```

Inputs:

- Synchronizer repo `main`: `ae75e8a270bd8f095090a193cb3beb93ed25bca9`.
- Config: `/home/li/primary/agent-outputs/RenamePropagator/worker2-synchronizer-full.nota`.
- Report: `/home/li/primary/agent-outputs/RenamePropagator/worker2-synchronizer-full-report.nota`.
- Stderr log: `/home/li/primary/agent-outputs/RenamePropagator/worker2-synchronizer-full-stderr.log`.
- Builder strategy: `(DirectHost localhost)`, so Nix fetches ran on credentialed `ouranos` and compilation could use configured remote builders including prometheus.

Result:

- Exit code: `1`.
- Many `drop-next` branches were advanced by the tool; the report is the authoritative pushed-tip ledger.
- Not landable: the report contains `BumpFailed` actions and verification failures.

## Hard blockers

The synchronizer report has two actual bump blockers:

```text
(meta-signal-spirit (BumpFailed LockEdit) NotAttempted)
(meta-signal-spirit LockEdit [|unbumpable pin: ComponentName("meta-signal-spirit") -> schema-rust: several same-name entries pin the producer|])

(mind (BumpFailed ManifestEdit) NotAttempted)
(mind ManifestEdit [|unbumpable pin: ComponentName("mind") -> meta-signal-mind: the entry deliberately pins an exact revision|])
```

Additional verification blockers include:

- `spirit` build fails in `spirit-source-with-local-schema-patches`: a `substituteStream --replace-fail` pattern still expects `https://github.com/LiGoldragon/mirror.git` at `branch = "main"` after the staged manifest changed.
- `router` verification failed after a Nix git-cache fetch of `https://github.com/LiGoldragon/mirror.git` wedged for more than 15 minutes; I terminated the stuck fetch/ssh wrapper so the synchronizer could continue. The final report records this as `Failed to fetch git repository 'https://github.com/LiGoldragon/mirror.git'`.
- `harness` lock resolution fails with duplicate `links = "signal-persona"` from `signal-harness@main` and `signal-persona@drop-next`.
- `CriomOS-home` has no default package for the synchronizer verifier.
- `CriomOS` eval requires the deployment-provided `system` flake input.
- Several no-flake or eval failures remain in the report (`mentci`, `meta-signal-*`, etc.); see the full report for exact stderr excerpts.

## Residue scan

Exact pattern used for remote-tip scans:

```sh
git -C <repo> grep -n -I -E 'nota-next|schema-next|schema-rust-next|nota_next|schema_rust_next|NOTA_NEXT|SCHEMA_NEXT|SCHEMA_RUST_NEXT|schema_next' <remote-tip> -- .
```

Remote tips checked:

- `meta-signal-spirit/drop-next`: `b05464fd1c5c76ee4c3a06caf43eb5226fe8cbf9`
- `mind/main`: `292b11c582197c4fb185a264635e9e4b3d923eba`
- `spirit/drop-next`: `af5cf6be478e8a47aabc9d8f575543f767cfdeb5`
- `system/drop-next`: `ffd0b74a17587bb6c90f40d170b57b355c43648f`

Result: **not zero**.

- `meta-signal-spirit`: stale `Cargo.lock` references to `nota-next.git` and `schema-next.git`.
- `mind`: live Cargo manifest/lock residue, `build.rs` `schema_rust_next`, live `nota_next` imports/extern crate paths, generated headers, docs.
- `spirit`: Cargo/flake lock residue, `flake.nix` inputs and `--replace-fail` literals, scripts (`NOTA_NEXT_REF`, `schema-next`, `schema-rust-next`), tests, README, and production migration comment residue.
- `system`: `Cargo.lock` `nota-next-derive`, generated header `schema-rust-next`, and doc/comment residue.

Because residue is nonzero and bump failures remain, no `main` landing was attempted.

## Verification

Passed/green examples from the synchronizer report include `schema-rust`, `agent`, `cloud`, `criome`, `domain-criome`, `introspect`, `message`, `orchestrate`, `terminal-cell`, and many lower-level signal/meta-signal packages. Some passed the configured `WireChecks` gate (`criome`, `message`, `introspect`, `orchestrate`, `terminal-cell`).

Failed:

- Full staged cascade command above: exit `1`.
- Verification failures are recorded in the NOTA report with the exact `nix eval`/`nix build` stderr excerpts.
- No landing verification was run because the staged graph is blocked.

## Conclusion

The full graph advanced substantially but is **not landable**. The next implementation pass must first remove the explicit `mind` revision pins or replace them with post-rename pins, fix `meta-signal-spirit`'s same-name `schema-rust` lock duplication with a full lock regeneration/coherent pin set, then resolve the `spirit` hardcoded substitution literals and remaining zero-residue findings before rerunning the staged cascade and landing producers before consumers.
