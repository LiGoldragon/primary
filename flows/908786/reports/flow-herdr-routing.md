# Flow Herdr routing delivery

## Result

Flow `0.3.0` is published at
`61d765e4814035c2c0a1424e670a1b62da3d10b6`. The local checkout was clean,
and a direct `git ls-remote origin refs/heads/main` observation returned the
same revision before this report was written.

The delivered source graph is:

| Component | Revision | Relationship |
| --- | --- | --- |
| `flow` | `61d765e4814035c2c0a1424e670a1b62da3d10b6` | Tested source and published `main` |
| `signal-flow` | `968ae3b00a64ebcb1ef05e21a0a55cee55ad015c` | Flow dependency pinned by `Cargo.toml`/`Cargo.lock` |
| `meta-signal-flow` | `aa6104012e1d9c9b9650590e502c51fbea902e81` | Flow dependency pinned by `Cargo.toml`/`Cargo.lock` |
| `sema-engine` | `516f01fe0b03157efc6cc3d38b588f0ca123ac94` | Transitive graph revision pinned by `Cargo.lock` |

Registered agents now carry an immutable Herdr binding in a side table while
the existing v5 Flow row layout remains byte-compatible. Registration uses a
strict `.FLOW_ID.flow-id` marker to authenticate the Flow identity and alias;
it does not infer a Flow ID from a native session UUID. Repeating the same
binding is idempotent. A conflicting binding is refused without partial store
mutation.

Resolution reads a fresh `herdr --session NAME api snapshot` and requires the
stored agent name, pane, terminal, and harness to match an idle or working,
interactive-ready agent. When a persisted Herdr binding cannot be resolved,
the Herdr route is unavailable and any otherwise available native endpoint is
parked. This prevents delivery from falling through to a stale native-looking
endpoint. Rows that predate Herdr bindings retain their native endpoint
behavior.

The meta `Configure` contract takes `ordinary_socket_path` and
`meta_socket_path`, persists both, and reports `NexusRestartRequired`. Its
defaults are `/run/user/1001/flow/flow.sock` and
`/run/user/1001/flow/flow-meta.sock`. This delivery does not activate or
switch either service.

## Remote gate

The exact published Flow source was built with Nix's local scheduler disabled
and the configured remote builders selected:

```console
nix build --no-link --print-out-paths --max-jobs 0 \
  --builders @/etc/nix/machines \
  .#checks.x86_64-linux.default \
  .#checks.x86_64-linux.fmt \
  .#checks.x86_64-linux.clippy \
  .#checks.x86_64-linux.flow-v5-row-preservation \
  .#checks.x86_64-linux.flow-herdr-route-durability \
  .#checks.x86_64-linux.flow-stale-route-unavailable \
  .#checks.x86_64-linux.flow-conflicting-registration-refusal \
  .#checks.x86_64-linux.flow-herdr-registration-binding \
  .#checks.x86_64-linux.flow-native-resolution-serialization \
  .#packages.x86_64-linux.default
```

The command exited with status `0`. The daemon log records all ten derivations
building on `ssh-ng://nix-ssh@prometheus.goldragon.criome`. In command order,
the realized outputs were:

| Attribute | Output |
| --- | --- |
| `checks.x86_64-linux.default` | `/nix/store/f0hc30sawv800n3q29ycjp0cdhpwpq5x-flow-workspace-test-0.3.0` |
| `checks.x86_64-linux.fmt` | `/nix/store/58n4ynr8pp28lw392xv98lck7ygq6ym5-flow-workspace-fmt-0.3.0` |
| `checks.x86_64-linux.clippy` | `/nix/store/xdaxrbhiag6kn1b0bf5m3lzrj39rmqbs-flow-workspace-clippy-0.3.0` |
| `checks.x86_64-linux.flow-v5-row-preservation` | `/nix/store/cjfmj6lm089ipnyvcxaj08pzg7phk5lf-flow-workspace-test-0.3.0` |
| `checks.x86_64-linux.flow-herdr-route-durability` | `/nix/store/wbrqbih39217l2msxmjmhq09w5zvsw8p-flow-workspace-test-0.3.0` |
| `checks.x86_64-linux.flow-stale-route-unavailable` | `/nix/store/1dy7cljxp4xbi3jcwvnccfq45lwnws2l-flow-workspace-test-0.3.0` |
| `checks.x86_64-linux.flow-conflicting-registration-refusal` | `/nix/store/sy1bs0kc1wbcj9kjh5193fi0vz2s750z-flow-workspace-test-0.3.0` |
| `checks.x86_64-linux.flow-herdr-registration-binding` | `/nix/store/slzni3vkmpcwk5554w2gl0n42aiqrbq2-flow-workspace-test-0.3.0` |
| `checks.x86_64-linux.flow-native-resolution-serialization` | `/nix/store/1h9q5vyfn8czv2ckpsd2jm7hk3l6xpp5-flow-workspace-test-0.3.0` |
| `packages.x86_64-linux.default` | `/nix/store/s78dixbvmbpyh8ha666hccfk1k9fd3qw-flow-0.3.0` |

Local corroboration also passed `cargo test --workspace`, `cargo fmt --check`,
and `cargo clippy --workspace --all-targets --all-features -- -D warnings`.
The workspace test totals were 3 `flow`, 2 `flow-meta`, and 23 `flow-nexus`
tests, with no failures.

## Method and sources

- Source identity: clean `/git/github.com/LiGoldragon/flow` checkout at the
  reported revision, compared with the actual GitHub `origin/main` ref using
  `git ls-remote`.
- Dependency identity: `Cargo.toml`, `Cargo.lock`, and `flake.lock` at the
  reported Flow revision.
- Check definitions: `flake.nix` at the reported Flow revision. Each focused
  attribute selects one named Rust witness, while `default`, `fmt`, and
  `clippy` cover the workspace gate.
- Remote execution evidence: supervisor-captured stdout, stderr, and exit
  status from the command above. The captured receipt files were
  `/tmp/flow-908786-nix-61d765e4.out`,
  `/tmp/flow-908786-nix-61d765e4.err`, and
  `/tmp/flow-908786-nix-61d765e4.status`; the durable facts from those
  temporary files are reproduced in this report.
- Identity evidence: the existing `.1ac573.flow-id` and `.af762b.flow-id`
  markers were observed read-only. The former demonstrates that an imported
  Flow alias can legitimately differ from its native UUID; the latter is the
  current canonical persisted identity.

