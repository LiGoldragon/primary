# Orchestrate runtime witnesses

## Source and local gates

- `cargo test --workspace --all-targets`: pass. The workspace ran 18 tests:
  four client process tests, five store/migration tests, three live socket tests,
  and four ordinary Lock contract tests; binary targets contained no unit tests.
- `cargo fmt --all -- --check`: pass.
- `cargo clippy --workspace --all-targets -- -D warnings`: pass.
- `cargo tree -p orchestrate-nexus --edges normal | rg 'datom|protos'`: no
  matches. Datom/Protos are absent from the daemon's normal dependency graph.
- `jj status` after push: clean. Orchestrate `main` is
  `1bc55af1859e41a7a8310f05c6b3588b8da47a65`.

## Remote Nix gate

`nix flake check -L` used `@/etc/nix/machines` with substitutions enabled and
built on `ssh-ng://nix-ssh@prometheus.goldragon.criome`. The final run against
Ethos Zero 6.1.2 reported `all checks passed!` for all 16 Orchestrate checks,
including workspace build/test, live Nexus, ordinary Lock contract, both
clients, docs, formatting, and clippy. Its only final notice was that systems
other than x86_64-linux were omitted.

## Isolated packaged candidate

The remotely built Nix package exposed exactly these binaries:
`orchestrate`, `orchestrate-meta`, `orchestrate-nexus`,
`orchestrate-store-migrate`, and `orchestrate-upgrade-preflight`.

It ran with `XDG_RUNTIME_DIR=/tmp/orchestrate-stage.dzNpYw/runtime` and
`XDG_STATE_HOME=/tmp/orchestrate-stage.dzNpYw/state`. The observed exchange was:

```text
Observed.Locks.[]
Configured.{ «/tmp/orchestrate-stage.dzNpYw/runtime/orchestrate-nexus/orchestrate.sock» «/tmp/orchestrate-stage.dzNpYw/runtime/orchestrate-nexus/meta-orchestrate.sock» }
Locked.{ 1 Stage 857335 [ /tmp/orchestrate-stage-resource ] Staging }
Observed.Locks.[ { 1 Stage 857335 [ /tmp/orchestrate-stage-resource ] Staging } ]
```

After stopping and restarting that packaged Nexus against the same isolated
roots, `Observe.Locks` returned the same complete Lock. Both starts logged
`orchestrate-nexus ready`.

The final Ethos 6.1.2 package was also staged with a stored configuration that
contained the real absolute socket paths. Bubblewrap mounted
`/tmp/orchestrate-remap.7hAI73/mapped-sockets` over
`/run/user/1001/orchestrate-nexus` inside the candidate namespace and mounted
only the isolated state root writable. The candidate logged ready and the host
client reached its mapped source socket, returning `Observed.Locks.[]`.
Outside the namespace the production unit remained active as PID 2323. This
proves the runbook can validate preserved absolute configuration without
binding or replacing either host production socket.

The live integration tests separately prove typed ordinary and privileged
Signal round trips, malformed archive rejection before store handling, zero
startup arguments, and restart persistence. Client process tests prove exact
Datom input/output and generated Ethos self-description.

## Migration and live boundary

`previous_signal_rows_require_an_explicit_migration` constructs exact historical
tuple archives via types independent of the migration reader. It proves the
configuration, two complete locks, and allocator value 9 survive conversion,
and that the next Lock uses 9. `migration_source_failure_preserves_v1_records`
proves an incomplete source is left intact.

The live service read-only witness after staging was:

```text
ActiveState=active
SubState=running
MainPID=2323
ExecMainStartTimestamp=Wed 2026-09-09 21:49:23 CEST
path=/home/li/.local/state/orchestrate-nexus/orchestrate-nexus.sema size=638976
filesystem=/dev/nvme0n1p2 ext4
```

No stop, signal, state copy, migration, or production socket request was made.
Because there is no online consistent file backup, the latest-state migration
witness is deferred to the final controlled quiescence described in the report.

## Sources

- Commands and outputs executed by subflow `/root/runtime_complete`, thread
  `01a088c1-067b-7be0-87d9-16807125ceb8`, on 2026-09-10.
- Orchestrate `1bc55af1859e41a7a8310f05c6b3588b8da47a65` test sources.
- Historical Orchestrate `5f016531e765d9b679a86cc47a2d75eaca43d624`
  `src/store.rs` for the deployed archive and Sema-family shapes.
- Nix derivations built by `nix flake check -L` on
  `ssh-ng://nix-ssh@prometheus.goldragon.criome`.
