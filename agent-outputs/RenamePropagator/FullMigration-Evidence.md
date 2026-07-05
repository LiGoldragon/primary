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

## 2026-07-05 continuation after auditor GO_TO_FIX

Status: **BLOCKED**. No `drop-next` branch was landed to `main`.

Additional fixes pushed:

- `upgrade/drop-next 7e8321abca5fcb6a110e9eba552cc9e786f285e1`: removed stale `nota-next` dependency-boundary expectation and adjacent docs/skill residue. The working-copy commit also carried preexisting generated `src/schema/lib.rs` and `Cargo.lock` changes already present in that checkout.
- `meta-signal-introspect/drop-next 3e0393a1bde3c97ccd77d621ce2ddc71892fe01e`: added `trace_socket_path` to the round-trip fixture for the current `signal-introspect` configuration type.
- `persona/drop-next e314c0615253`: added top-level `rust-build`, wired `persona-spirit.inputs.rust-build.follows = "rust-build"`, regenerated `flake.lock`, and removed stale visible next-family comments/headers.
- `router/drop-next 97d701729caa07d682e7cecb144dcfbc8e556d6b`: in an isolated worker checkout tracked by bead `primary-alo7`, passed `ContentAddressing::Opaque` to the updated `mirror::Store::register_store` test call.
- `persona/drop-next 45e7942d0f146fa866528198921f16bb513eee6b`: advanced `persona-router` to the fixed router tip.
- `persona/drop-next 43761e8cb4a8f9a0e898849e36ab714b98839985`: advanced `mind` to the staged fixed `ca7c2e7fa41ecdc679b523fbadedc1a0dc095188` tip.

Targeted verification:

```sh
cargo test --test dependency_boundary
nix build --no-link github:LiGoldragon/upgrade/7e8321abca5fcb6a110e9eba552cc9e786f285e1
```

Result: passed.

```sh
cargo test --test round_trip
nix build --no-link github:LiGoldragon/meta-signal-introspect/3e0393a1bde3c97ccd77d621ce2ddc71892fe01e
```

Result: passed.

```sh
cargo test --test criome_forward_lands_in_mirror criome_verified_forward_lands_an_append_in_the_co_resident_mirror -- --exact
nix build --no-link .#checks.x86_64-linux.router-criome-forward-lands-in-mirror
```

Result: passed in the isolated router checkout before pushing `drop-next 97d701729caa`.

Persona verification progression:

```sh
nix build --no-link github:LiGoldragon/persona/45e7942d0f14#checks.x86_64-linux.persona-daemon-launches-nix-built-message-router-topology
```

Result: the original `spirit`/`rust-build` evaluation blocker was cleared, and the router package built with the fixed router tip, but the check then failed because persona still pinned `mind 0bba8e060b91`; that old mind revision used named-field syntax for `RepositoryIndexRefreshed`.

```sh
nix build --no-link github:LiGoldragon/persona/43761e8cb4a8#checks.x86_64-linux.persona-daemon-launches-nix-built-message-router-topology
```

Result: mind propagation was cleared, but persona itself failed to compile against the current staged graph. Key failures include missing `ComponentName::as_str()` uses in `src/unit.rs`, `EngineManagementProtocolVersion` move-from-shared-reference in `src/supervision_readiness.rs`, and 196 total compile errors reported by rustc. This is broader persona/source API drift and remains the verification blocker.

Remote-tarball residue scan required by auditor:

```sh
pattern='nota-next|schema-next|schema-rust-next|nota_next|schema_next|schema_rust_next|NOTA_NEXT|SCHEMA_NEXT|SCHEMA_RUST_NEXT|nota-next-derive'
# For each repo in worker2-synchronizer-continuation.nota: resolve GitHub drop-next ref,
# download the GitHub tarball for that exact SHA, extract outside VCS history, then run:
rg -l -I --hidden --glob '!.git/**' -e "$pattern" <extracted-tarball>
```

Corrected result:

- repos parsed: 86
- remote `drop-next` tips resolved: 85
- tarball/ref failures: 5
- match paths: 78
- tip evidence: `/home/li/primary/agent-outputs/RenamePropagator/worker2-remote-tarball-scan-tips.txt`
- failure evidence: `/home/li/primary/agent-outputs/RenamePropagator/worker2-remote-tarball-scan-failures.txt`
- match-path evidence: `/home/li/primary/agent-outputs/RenamePropagator/worker2-remote-tarball-scan-matches.txt`

Scan failures:

- `mind`: tarball timeout/failure at `ca7c2e7fa41ecdc679b523fbadedc1a0dc095188`.
- `signal-listener`: tarball timeout/failure at `4ad1154aed3e836c5be0fb6701f5096f9e3221d1`.
- `signal-mirror`: tarball timeout/failure at `0a8ab9afe57dc6ce55524e4da7b6b8ff1f59c9e9`.
- `synchronizer`: no `drop-next` ref.
- `system`: tarball timeout/failure at `fdfffe5f5df8e7ef77a33d745e4e74f52625386b`.

Residue result: **not zero**. The scan found 78 path-level matches across the resolved tarballs, including docs, tests, schemas, and dependency-boundary witnesses in multiple signal/meta-signal/runtime repos. Because this was a path-only scan, it does not quote private file contents.

Landing decision: blocked by both nonzero remote-tarball residue and persona compilation failure. No landing to `main` was attempted.

## 2026-07-05 Worker 4 residue cleanup

Status: **RESIDUE CLEAN for the scanned remote tips**. Worker 4 did not address the separate persona compile drift.

Scope cleaned:

- Active source/use-path and error-literal residue in `criome`, `horizon-rs`, `mentci-lib`, `nexus`, `orchestrate`, `signal`, `signal-terminal`, `triad-runtime`, and `synchronizer`.
- Active schema/dependency-boundary residue in `mentci`, `meta-signal-lojix`, `meta-signal-mentci`, `meta-signal-mentci-client`, `signal-lojix`, `signal-mentci`, `meta-signal-upgrade`, and `signal-upgrade`.
- Generated comments, docs, tests, fixtures, and examples across the remaining matched repos.
- Prior tarball-failure repos were rescanned; `signal-listener` needed one ARCHITECTURE cleanup and was pushed.

Pushed changed tips:

```text
clavifaber/drop-next 53ca5e8df6f9db9e509e7109c98ce740c30359a7
cloud/drop-next 64ef285f2da07e74d2e76f45932bd8fad0ccc3d9
criome/drop-next 28cfc58e35155ed9f93040ba9bb27201019f646d
domain-criome/drop-next c0c4f7b267a6bff0b7c0fb3375150827203cc3ec
horizon-rs/drop-next 1f75fa81dcc43a915392cad14595717d1d71d8c9
introspect/drop-next 4b18d35c40946e390c531ebd216499e7d5306757
mentci/drop-next 311be2833e57bd7d409a721d3927daf40937da8b
mentci-lib/drop-next 921911295e645dda0ae3e8588c951e88a698a831
message/drop-next 687d472d80480d4ef0e3736ec495a96a6a370fbe
meta-signal-agent/drop-next afd16221a8fe16ddb81025d86f3b8776fbdadf4d
meta-signal-criome/drop-next e7420884763f1e458b103b85166daf7fcfd87f0a
meta-signal-listener/drop-next e815e19769afdccd6635eda99b4d139ead164d5b
meta-signal-lojix/drop-next 2657286777868238aed7567a0b02bbb991272162
meta-signal-mentci/drop-next da474387512bda773ab4342f22e6e113fd59bc8a
meta-signal-mentci-client/drop-next e8da017d9372bd0316ec10d95b0f245007130f87
meta-signal-message/drop-next c41a8b9efe133d8bdddb2f4663573e116a74a1de
meta-signal-mind/drop-next e847c129f41cb0aafb443a47c75e6dbc6fd718a0
meta-signal-persona/drop-next ce4094922035db034b23d0c1311b9a525b54200a
meta-signal-upgrade/drop-next 4e0435755499b9617f198ee79aa4f80c1c576bd9
nexus/drop-next 290de15ee14ac14444e80022c96501e499e252dc
nota-config/drop-next 88792a277d783198dcc325ef6d51ef9a1e6d64ac
orchestrate/drop-next 00877919b27ac3b816af98d592cb63f72f75807e
repository-ledger/drop-next 38b226b1847a7ae65de13fbc428f1fabdf714696
schema/drop-next f351f90d3b8898205cf3057f3c253a5e451180a9
signal/drop-next 85d9e029b39dbb491dd85dd020364e4123de948c
signal-agent/drop-next cedc8f69fb83b6983f96ec3a43e224d974bb5831
signal-cloud/drop-next 559e918b829c3f0da1419f945f62ca8dc5259e81
signal-domain-criome/drop-next e50b807f272fa11ce2d66f857e1bed44c8a125cd
signal-frame/drop-next bb86bef67e478ff52690a4dcceec8f22d2b005ad
signal-introspect/drop-next afe4d50adb6c9750293aa08e609b4ecf8b71ac10
signal-listener/drop-next 703a03b22e3f463c883b19fb1988ff09580207c9
signal-lojix/drop-next ee7abf4bb7d75bccf3aecf614025b9f0f3a0ae3d
signal-mentci/drop-next 6d1fd4d2a5a89eaa0f3f3b7bf57473f016b737e9
signal-terminal/drop-next 1a0775bc460d7d2ab5c0f17375082c3bb00c8eb2
signal-upgrade/drop-next aec31f0a53ff6f35d94c3b4cd93844c7cbca65df
skills/drop-next e69e3aaea98a547b77be6d023948487e1426c2fc
synchronizer/main 7b24c4163d42b9b5f2867fd7ab39049c68fe5b3a
terminal/drop-next 43985c91912e26336a2e1cd911d1b62952c205a3
terminal-cell/drop-next c4ac94f58ae4fa8931d55bef4239d0d95ca10b49
triad-runtime/drop-next 20c3b67b9d97523653da1c75405772ef1cf1ad5b
```

Focused checks passed:

```sh
cargo check --features nota-text --bin criome-encode-configuration
cargo test --manifest-path lib/Cargo.toml --test proposal
cargo test --test ledger path_overlap_uses_component_boundaries_not_substrings -- --exact
cargo test --test text_round_trip
cargo test --test round_trip
cargo test --features nota-text --test reaction
cargo test
cargo test --test dependency_boundary
cargo test --test cargo_manifest --test transitive_gap --test topology
cargo test --test publication_writing
```

Remote tarball residue scan:

```text
pattern: nota-next|schema-next|schema-rust-next|nota_next|schema_next|schema_rust_next|NOTA_NEXT|SCHEMA_NEXT|SCHEMA_RUST_NEXT|nota-next-derive
full scan: 86 repos scanned, 84 refs resolved, 7 fetch/ref failures, 0 match paths
targeted retry of the 7 failed refs/tarballs: 0 failures, 0 match paths
combined result: 86 repo set clean for the required pattern, with no remaining scan failures
```

Scan artifacts:

- `/home/li/primary/worktrees/worker4-residue/worker4-remote-tarball-scan-summary.txt`
- `/home/li/primary/worktrees/worker4-residue/worker4-remote-tarball-scan-tips.txt`
- `/home/li/primary/worktrees/worker4-residue/worker4-remote-tarball-scan-matches.txt`
- `/home/li/primary/worktrees/worker4-residue/worker4-remote-tarball-scan-failures.txt`
- `/home/li/primary/worktrees/worker4-residue/worker4-remote-tarball-scan-retry-tips.txt`
- `/home/li/primary/worktrees/worker4-residue/worker4-remote-tarball-scan-retry-matches.txt`
- `/home/li/primary/worktrees/worker4-residue/worker4-remote-tarball-scan-retry-failures.txt`

Remaining risk:

- `repository-ledger` has a split remote shape: the authoritative GitHub `drop-next` used by the tarball scan is clean at `38b226b1847a`, while local `origin` is gitolite and still has a separate cleanup commit. Worker 4 pushed the GitHub branch used by the migration scan.
- Persona compile drift remains outside Worker 4 scope.

## 2026-07-05 Worker 2 persona compile drift continuation

Narrowed scope: persona compile drift only. No broad residue cleanup was attempted in this continuation.

Persona fixes pushed:

- `persona/drop-next b68001ca531ce9c4d61e315d54deb1ddc4a4205c`: adapted persona source and helper binaries to the staged generated contract API:
  - replaced removed `signal_persona::origin` paths with current top-level generated types;
  - replaced removed `ComponentName::as_str()` style access through persona's local generated-contract adapter;
  - updated meta-signal-persona wrapper handling for `Query`, `Start`, `Stop`, `EngineStatus`, `ComponentStatus`, action, catalog, launch, and retire replies;
  - updated signal-persona spawn envelopes to use component principals and current path/mode wrappers;
  - added `trace_socket_path` to the persona-written introspect daemon configuration;
  - updated router, terminal, harness, system, and message helper configuration/bootstrap construction for current wrapper/newtype fields.
- `persona/drop-next 94b0f555c16e3edbac017ebb85c5af4d1cecc0af`: updated persona tests to the same staged wrapper contracts and current report projection shape.

Verification:

```sh
cargo check --locked
```

Result: passed before test updates.

```sh
cargo test --locked
```

Result: passed. Test summary included all persona integration tests, with 1 preexisting ignored daemon rejection test.

```sh
nix build --no-link github:LiGoldragon/persona/b68001ca531ce9c4d61e315d54deb1ddc4a4205c#checks.x86_64-linux.persona-daemon-launches-nix-built-message-router-topology
```

Result: failed in persona test compilation only (`tests/state.rs` still used old `ComponentStartup`/`ComponentShutdown` fields and old action rejection fields). This failure was fixed by `94b0f555c16e3edbac017ebb85c5af4d1cecc0af`.

```sh
nix build --no-link github:LiGoldragon/persona/94b0f555c16e3edbac017ebb85c5af4d1cecc0af#checks.x86_64-linux.persona-daemon-launches-nix-built-message-router-topology
```

Result: passed. The build used `ssh-ng://nix-ssh@prometheus.goldragon.criome` as the remote builder and copied back `/nix/store/fa6ydambg9h1z3y3jw6p5mzh657bz24k-persona-daemon-launches-nix-built-message-router-topology`.

Current persona status: **green for the requested exact topology check** at `drop-next 94b0f555c16e3edbac017ebb85c5af4d1cecc0af`.
