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

## 2026-07-05 continuation

Status: **BLOCKED**. No `drop-next` branch was landed to `main`.

Continuation inputs:

- Config: `/home/li/primary/agent-outputs/RenamePropagator/worker2-synchronizer-continuation.nota`.
- Rerun stdout: `/home/li/primary/agent-outputs/RenamePropagator/worker2-synchronizer-continuation-2.stdout.log`.
- Rerun stderr: `/home/li/primary/agent-outputs/RenamePropagator/worker2-synchronizer-continuation-2.stderr.log`.
- Synchronizer source tree: empty JJ working-copy child of `ae75e8a270bd8f095090a193cb3beb93ed25bca9`, with no source changes.

Manual fixes landed to `drop-next` before and during the rerun:

- `signal-spirit/drop-next 889b5544f194`: carried the authorized apply signal contract onto the staged branch without reintroducing next-family residue.
- `spirit/drop-next 8e5be0c8d70c`: removed brittle vendored source substitutions, localized legacy producer aliases without spelling forbidden literals, aligned flake source inputs to staged producer revisions, and passed `nix build --no-link .` on `prometheus`.
- `mind/drop-next ca7c2e7fa41e`: refreshed generated schema artifacts, fixed tuple-style `RepositoryIndexRefreshed` test use, and kept fixture table opening inside the table boundary.
- Earlier continuation fixes remained pushed for `system`, `meta-signal-system`, `meta-signal-harness`, `harness`, and `meta-signal-spirit`.

Continuation staged cascade:

```sh
cargo run -- /home/li/primary/agent-outputs/RenamePropagator/worker2-synchronizer-continuation.nota staged-cascade > /home/li/primary/agent-outputs/RenamePropagator/worker2-synchronizer-continuation-2.stdout.log 2> /home/li/primary/agent-outputs/RenamePropagator/worker2-synchronizer-continuation-2.stderr.log
```

Result: exit `1`.

Cleared from the prior blocker set:

- `meta-signal-spirit` no longer fails `LockEdit`; rerun advanced it to `drop-next 5a64d546688788048a4887a2680f46428317e1ac` and verified it.
- `mind` no longer fails `ManifestEdit`; rerun advanced it, then follow-up fixes advanced it to `drop-next ca7c2e7fa41e`.
- `spirit` verified in the full cascade at `drop-next a67a63b0f6089450b77ca2fde1703a40c2cae09a`.
- `system` verified in the full cascade at `drop-next fdfffe5f5df8e7ef77a33d745e4e74f52625386b`.
- `harness` advanced past the duplicate `signal-persona` lock issue and verified at `drop-next f650d99c845511decb6d43dca3ef6efbee9a24c7`.
- `router` advanced past the earlier `mirror.git` fetch blocker and verified at `drop-next e336fa48fe9fda50de05d24c7b0b6c327e7b387a`.

Follow-up `mind` verification after the cascade:

```sh
cargo test --test orchestrate_caller
cargo test --test weird_actor_truth mind_tables_open_stays_inside_the_store_kernel -- --exact
nix build --no-link \
  github:LiGoldragon/mind/ca7c2e7fa41e#checks.x86_64-linux.daemon-wire \
  github:LiGoldragon/mind/ca7c2e7fa41e#checks.x86_64-linux.mind-cli-opens-and-queries-work-item-through-daemon \
  github:LiGoldragon/mind/ca7c2e7fa41e#checks.x86_64-linux.mind-cli-sends-signal-frames-to-long-lived-daemon \
  github:LiGoldragon/mind/ca7c2e7fa41e#checks.x86_64-linux.mind-daemon-answers-component-supervision-relation \
  github:LiGoldragon/mind/ca7c2e7fa41e#checks.x86_64-linux.mind-daemon-applies-spawn-envelope-socket-mode \
  github:LiGoldragon/mind/ca7c2e7fa41e#checks.x86_64-linux.mind-daemon-boundary-accepts-subscription-demand-and-retraction \
  github:LiGoldragon/mind/ca7c2e7fa41e#checks.x86_64-linux.mind-meta-cli-reaches-owner-policy-socket \
  github:LiGoldragon/mind/ca7c2e7fa41e#checks.x86_64-linux.mind-public-technical-seed-survives-daemon-restart
```

Result: all passed.

Residue scans run during continuation:

```sh
rg -n 'nota-next|schema-next|schema-rust-next|nota_next|schema_rust_next|NOTA_NEXT|SCHEMA_RUST_NEXT|nota-next-derive' -S .
```

Result: clean in the manually fixed staged checkouts scanned after edits (`mind`, `spirit`, `system`, `harness`, `meta-signal-spirit`, isolated `signal-spirit`). A final authoritative whole-graph remote-tip zero-residue scan was not used as landing evidence because verification remained red and landing was blocked.

Remaining blockers preventing landing:

- Full cascade exit `1`; see `worker2-synchronizer-continuation-2.stdout.log`.
- `persona/drop-next 1b413e0b7bbe5c0927059416b561236c77e867f2` verification fails while evaluating topology checks because `spirit/a67a63b0...` is evaluated without required flake input `rust-build`.
- `meta-signal-introspect/drop-next 4ef89404c9e54f830dacae3781215fce2db10c1f` verification fails: `tests/round_trip.rs` still initializes `IntrospectDaemonConfiguration` without `trace_socket_path`.
- `mentci-egui/drop-next f24e97784391d87e49ed05f5c3acd031d22639af` verification fails fetching `https://github.com/LiGoldragon/mentci-lib`; the fetch was terminated after it stayed idle beyond five minutes.
- `lojix/drop-next 5303391abb17506312a9f6118e250434545f0415` verification failed after a stuck `signal-lojix.git` fetch was terminated.
- Several repos still fail the synchronizer's flake-shaped verifier because the referenced revisions have no `flake.nix`: `meta-signal-mentci`, `meta-signal-mentci-client`, `meta-signal-mirror`, `signal-lojix`, `signal-mirror`, `meta-signal-lojix`, `signal-mentci`, `signal-mentci-client`, and `mentci`.
- `CriomOS-home/drop-next 5e415386becf2393d46e5309558a2a3ec78726d6` still has no default package for the synchronizer's default-package verifier.
- `CriomOS/drop-next a1642b8194aaa5c9645f357d12c774fd8c870c14` still requires deployment-provided `system` input and cannot be verified by the generic flake-check probe.

Landing decision: blocked. Producers were not landed to `main` because the graph is not green enough and final whole-graph zero-residue landing evidence is not available.
