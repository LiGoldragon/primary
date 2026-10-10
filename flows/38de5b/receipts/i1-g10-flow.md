# I1 and G10 receipt — flow repo

Opus subflow of Psyche High 38de5b, 2026-09-25. Tasks I1 and G10 of `reports/audit-flow.md`.

## Landed

- Repo LiGoldragon/flow, branch `i1-g10-38de5b`, rebased onto main 4671f8d (Flow 0.7.1 from the f2-g5 branch) and pushed to main: **972d8d2** (`git ls-remote origin main` = 972d8d229029d560a14145d1eaf18a7fa333c73f).
- No version bump: main was already at 0.7.1 from the concurrent branch when this landed.
- Rebase conflict in `crates/flow-nexus/src/main.rs` (their `--version` answer); resolved by keeping `version_answer` and its test inside the new `main`.

## I1 — one bad frame no longer kills serving

- `lib.rs`: each ordinary and meta connection is a `Connection` served on its own scoped thread, with 5 s read and write timeouts. A malformed frame, an oversized frame, an idle peer or a failed write drops and logs only that connection (`flow-nexus: <surface> connection dropped: ...`). Accept errors are logged and the listener continues.
- Dispatch stays serialized across both sockets through one `dispatch_gate` mutex: store transitions such as `reserve_start` are read-modify-write, so concurrent dispatch would race. Consequence: a long Start still blocks other dispatches, but no longer blocks frame reading, idle peers, or malformed frames.
- `main.rs`: no `unwrap`; a failed ordinary listener exits the process with status 1, so systemd `Restart=on-failure` fires.
- Test `tests::a_malformed_frame_drops_only_its_connection`: holds an idle connection open, sends a 16-byte garbage frame, then `List` on a new connection answers `Listed`. Negative check: with the old serial loop restored, the same test fails (List times out).

## G10 — starts with no arguments and no Flow environment

- `store.rs`: `DefaultConfiguration { home, runtime_directory }` holds the executable's default configuration as associated constants anchored on `HOME` (else the password database) and `XDG_RUNTIME_DIR` (else `/run/user/<uid>`). Nothing names `/home/li` or uid 1001 any more.
- The socket `Configuration` is seeded from those defaults. A new Sema table, `flow-nexus-runtime-configuration-v1`, holds `RuntimeConfiguration` (the source root plus the stable and next Codex endpoints: client, home, socket and models). A new store persists the defaults; a populated store resumes them. The live store gains the table on first open and keeps its existing socket record.
- `FLOW_SOURCE_ROOT` and `FLOW_CODEX_{STABLE,NEXT}_{CLIENT,SOCKET,HOME,MODELS}` are now optional `DeploymentOverrides`. They are laid over the stored runtime configuration and persisted only when they differ. An absent or relative value is ignored and logged. This keeps the live Nix unit (Nix store client paths) working. It is marked at the site as an exception until meta Configure carries the fields.
- `codex.rs`: the flow directory, the `FLOW_DIRECTORY` in the turn brief, and thread `cwd` follow the configured source root (`CodexAdapter::flow_directory`). `reserve_start`'s endpoint path comes from the stored stable socket.
- `herdr.rs` (outside the briefed file list, but not touched by the other branch): `HerdrCli::default` no longer panics on a missing `HOME` or `FLOW_SOURCE_ROOT`, and `with_source_root` re-roots the flows directory and the workspace skill catalog.
- `deployment/flow-nexus.service`: no configuration variables. `Requires=` became `Wants=` on codex-remote-control, so the Nexus starts without it. The only `Environment=` line is PATH, so the unit finds herdr, codex and the Codex flow clients.
- Test `tests/default_start.rs`: spawns `flow-nexus` with `env_clear`, a temporary `HOME` and a temporary `XDG_RUNTIME_DIR`. Meta `Configure` answers `Configured`, then ordinary `List` answers `Listed` (empty), and `~/.local/state/flow/flow.sema` exists. A temporary runtime directory is set because the fallback `/run/user/<uid>/flow` would unlink the live Nexus's sockets.
- Store tests: `new_store_seeds_defaults_from_home_and_runtime_directory` and `deployment_overrides_replace_stored_runtime_values_only_when_valid`.
- The unit shape was run under systemd: `systemd-run --user` with only HOME and XDG_RUNTIME_DIR set came up `active` and bound both sockets. The committed unit file itself was not started, because `%h/.local/bin/flow-nexus` does not exist on this host; the live deployment is the Nix-generated unit.

## What meta Configure lacks

meta-signal-flow a34bc65 `Configuration` is `{ OrdinarySocketPath MetaSocketPath }` only. To make the runtime configuration settable over the meta socket, it needs a source root and the two Codex endpoints (client path, home, socket, model names). The contract repos were not changed.

## Remaining hard-codes outside scope

- `claude.rs`: `/home/li/.claude/jobs` and `/home/li/.claude/daemon/roster.json`.
- `lib.rs` test fixtures: `/home/li/primary` strings.
- `herdr/launch.rs` test: asserts that `/home/li/primary` is absent.

## Tests

- Before, 812053c: `cargo test` 62 passed (4 + 2 + 56 + 0 + 0).
- After, 972d8d2 (main now includes 0.7.1): 69 passed (flow 5, flow-meta 2, flow-nexus lib 60, flow-nexus bin 1, default_start 1). Six full runs were green. One pre-push summary count came out anomalous (2 result lines); every rerun was green.
- `cargo clippy --workspace --all-targets --all-features -- -D warnings`: clean.
- `cargo fmt --check` still reports pre-existing diffs in `composition.rs` and `herdr/launch.rs`, which came from main and were not touched. The flake's `fmt` check will fail on those.
- Nix `nix build` and `nix flake check` were not run.

## Lock

Orchestrate lock 6344 on the scratch clone path, released.
