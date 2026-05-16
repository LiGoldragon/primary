# Lojix Real Build Smoke And Stream Close Cleanup

Role: system-specialist  
Date: 2026-05-16  
Branch: `lojix/horizon-re-engineering`  
Commits:

- `a002123a` — sema-backed built-generation ledger
- `e6bb95e9` — stream subscription retraction on client disconnect

## Real Build Smoke

I reran the daemon/CLI smoke against the current Lojix head using the
horizon redesign branches:

- Proposal source:
  `/home/li/wt/github.com/LiGoldragon/goldragon/horizon-re-engineering/datom.nota`
- System flake:
  `github:LiGoldragon/CriomOS/horizon-re-engineering`
- Target:
  `goldragon/zeus`
- Builder:
  `NamedBuilder prometheus`
- Plan:
  `(FullOsDeployment Build)`

The daemon accepted the deployment:

```nota
(DeploymentAccepted deployment_1)
```

The final observation included:

```nota
(DeploymentBuilt deployment_1
  (RealizedStorePath "/nix/store/qsz55smwzwl11i9p150ikkw5zisrmf6p-nixos-system-zeus-26.05.20260510.da5ad66"))
```

`GenerationQuery` returned the sema-backed generation:

```nota
(Generation generation_12 goldragon zeus FullOs
  "/nix/store/qsz55smwzwl11i9p150ikkw5zisrmf6p-nixos-system-zeus-26.05.20260510.da5ad66"
  Built)
```

The built GC root pointed at the same store path:

```text
/tmp/lojix-real-build-current-YSuvYG/gcroots/goldragon/zeus/full-os/built/deployment_1
  -> /nix/store/qsz55smwzwl11i9p150ikkw5zisrmf6p-nixos-system-zeus-26.05.20260510.da5ad66
```

## Stream Close Cleanup

While polling observations through the CLI, the returned subscription
token sequence advanced. That is not by itself a leak: token values are
durable sequence identities, not a count. The missing proof was that a
client which opens a deployment-observation stream and then exits
without sending a retraction does not leave a durable subscription row.

Commit `e6bb95e9` adds that proof and makes EOF after an opened stream
a normal close path:

- `DeploymentObservationStreamConnection` retracts the token on EOF.
- `UnexpectedEof` after the stream is open returns `Ok(())`, not a
  socket error.
- `tests/socket.rs` adds
  `deployment_observation_subscription_retracts_when_client_disconnects`,
  which opens a stream, drops the client, and asserts the durable
  subscription count is zero.

## Verification

Rust:

- `cargo test --jobs 1 --test socket -- --test-threads=1`
- `cargo clippy --jobs 1 --all-targets -- -D warnings`

Nix:

- `nix build --max-jobs 1 --cores 2 .#checks.x86_64-linux.test-socket .#checks.x86_64-linux.clippy`

Manual smoke:

- `cargo build --jobs 1 --bin lojix --bin lojix-daemon`
- temp daemon state/socket/GC root
- real `DeploymentSubmission` above
- `DeploymentObservationSubscription` polling until `DeploymentBuilt`
- `GenerationQuery goldragon zeus FullOs`
- GC-root symlink check

All passed.

## Remaining Work

The engine now builds real closures, roots them, records built
generations in sema, returns them from `GenerationQuery`, and pushes
live deployment observations. It is still build-only. The next
production gaps are closure copy, activation/current-generation
promotion, rollback, sema-backed GC-root retention records, cache
retention, and the CriomOS/Home cutover from `lojix-cli`.
