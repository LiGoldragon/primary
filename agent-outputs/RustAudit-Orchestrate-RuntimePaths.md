# Rust audit — Orchestrate runtime paths/defaults/config writer

## Verdict

Conditional pass for the currently materialized systemd deployment, not a full Rust-behavior pass.

The live deployed path shape is correct: the unit writes config/state under `/home/li/.local/state/orchestrate`, binds sockets under `%t/orchestrate`, and the ordinary CLI default reached the live daemon through `$XDG_RUNTIME_DIR/orchestrate/orchestrate.sock` from `/home/li/primary`.

The Rust surfaces still have safety gaps around malformed environment/path input and daemon configuration trust. These do not appear to block the current managed deployment because systemd supplies absolute paths and runs `orchestrate-write-configuration` before daemon start, but they should block treating the new runtime path behavior as generally hardened.

Spirit evidence: public lookup `10pz` supports replacing legacy bad shapes instead of preserving repo-local compatibility paths. I found no need for legacy repo-local fallback.

## Evidence

Source inspected:

- `/git/github.com/LiGoldragon/orchestrate/Cargo.toml`
- `/git/github.com/LiGoldragon/orchestrate/src/bin/orchestrate.rs`
- `/git/github.com/LiGoldragon/orchestrate/src/bin/meta_orchestrate.rs`
- `/git/github.com/LiGoldragon/orchestrate/src/bin/orchestrate_write_configuration.rs`
- `/git/github.com/LiGoldragon/orchestrate/src/configuration.rs`
- `/git/github.com/LiGoldragon/orchestrate/src/daemon.rs`
- `/git/github.com/LiGoldragon/orchestrate/src/schema/daemon.rs`
- `/git/github.com/LiGoldragon/orchestrate/src/layout.rs`
- `/git/github.com/LiGoldragon/orchestrate/src/signal_transport.rs`
- relevant tests under `/git/github.com/LiGoldragon/orchestrate/tests/`
- relevant listener behavior in `/git/github.com/LiGoldragon/triad-runtime/src/async_runtime.rs`

Positive evidence:

- `src/bin/orchestrate.rs:51-55, 76-81, 95-100` defaults the ordinary CLI to `$XDG_RUNTIME_DIR/orchestrate/orchestrate.sock` when `PERSONA_ORCHESTRATE_SOCKET` is unset.
- `src/bin/meta_orchestrate.rs:48-52, 73-78, 92-97` defaults the meta CLI to `$XDG_RUNTIME_DIR/orchestrate/orchestrate-owner.sock` when `PERSONA_ORCHESTRATE_META_SOCKET` is unset.
- `src/bin/orchestrate_write_configuration.rs:101-109` writes a typed `DaemonConfiguration` with store, ordinary socket, meta socket, upgrade socket, workspace root, and git index root as `WirePath`s.
- `src/configuration.rs:44-60` uses rkyv bytes for the daemon configuration, and the daemon accepts a signal-file argument only through generated daemon argument handling.
- `systemctl --user cat orchestrate-daemon.service` shows `ExecStartPre=orchestrate-write-configuration /home/li/.local/state/orchestrate/orchestrate-daemon.signal /home/li/.local/state/orchestrate/orchestrate.sema %t/orchestrate/orchestrate.sock %t/orchestrate/orchestrate-owner.sock %t/orchestrate/orchestrate-upgrade.sock /home/li/primary /git/github.com/LiGoldragon` and `RuntimeDirectory=orchestrate` with mode `0700`.
- Live process evidence: `orchestrate-daemon /home/li/.local/state/orchestrate/orchestrate-daemon.signal`; sockets exist as `srw-------` under `/run/user/1001/orchestrate`; no `.sock`, `.signal`, `.sema`, `.redb*`, or `.log` files were found under `/home/li/primary/orchestrate` by the read-only find command.
- `env -u PERSONA_ORCHESTRATE_SOCKET orchestrate "(Observe Lanes)"` returned `(LanesObserved [])`, exercising the ordinary CLI default path in the current shell.

## Findings by severity

### High — decoded daemon configuration does not revalidate domain path invariants

Path: `/git/github.com/LiGoldragon/orchestrate/src/configuration.rs:50-60`, used by `/git/github.com/LiGoldragon/orchestrate/src/daemon.rs:86-98`.

Risk: `DaemonConfiguration::from_signal_bytes` trusts rkyv deserialization of `WirePath` fields. rkyv validation protects archive shape, not the domain invariant that paths are absolute, normalized, non-empty paths generated through `WirePath::from_absolute_path`. A validly shaped but domain-invalid config archive could make the daemon open a relative store or bind relative sockets from whatever cwd launches the daemon. That reintroduces repo-local runtime state if the daemon is started from a checkout and bypasses the writer.

Expected correction: after decode, run semantic validation on every path field before returning the configuration. The validation should reject relative, empty, `..`, and non-normalized paths with field-specific diagnostics. Prefer a `DaemonConfiguration::validate` method called by `from_signal_bytes`/`from_signal_file` and by the writer before any filesystem mutation.

Current deployed behavior blocker: not for the current managed service path, because the unit runs the writer with absolute arguments before daemon start. It is a blocker for declaring bad config/signal files safely detected at the Rust boundary.

### High — socket binding removes any existing file at the configured socket path

Path: `/git/github.com/LiGoldragon/triad-runtime/src/async_runtime.rs:1049-1066`, reached from `/git/github.com/LiGoldragon/orchestrate/src/schema/daemon.rs:187-216`.

Risk: the async listener preparation calls `remove_file` on the configured socket path without checking that the existing file is actually a Unix socket. A bad or malicious daemon configuration can delete a regular file at the socket path before binding. With dedicated `%t/orchestrate` paths this is low probability in the current unit, but it is not safe override behavior.

Expected correction: the listener should treat an existing non-socket as a typed error and leave it in place. Orchestrate can also preflight its three socket paths before handing them to triad-runtime, but the correct shared fix belongs in the runtime listener substrate.

Current deployed behavior blocker: not for the current unit's dedicated runtime directory; blocker for manual/override hardening.

### Medium — configuration writer creates parent directories before validating paths

Path: `/git/github.com/LiGoldragon/orchestrate/src/bin/orchestrate_write_configuration.rs:90-117`.

Risk: `write` calls `create_runtime_directories` before `configuration`. Relative or tilde-like arguments can create directories under the caller's cwd, then fail later when `wire_path` rejects the path. Example class: `~/.local/state/...` is not home-expanded, but the writer would first create a literal `~` subtree relative to the checkout before rejecting it as not absolute.

Expected correction: parse and validate all seven path arguments into typed absolute path values before calling `create_dir_all` or `write`. If home expansion is unsupported, fail before mutation with a clear “absolute path required; shell did not expand ~” style message.

Current deployed behavior blocker: not for the current unit, which passes absolute `/home/li/...`, `%t/...` expanded by systemd, and `/git/...` paths. It is a blocker for safe standalone use of the writer.

### Medium — CLI default and override socket paths are not validated as absolute/non-empty

Paths: `/git/github.com/LiGoldragon/orchestrate/src/bin/orchestrate.rs:51-55,95-105`; `/git/github.com/LiGoldragon/orchestrate/src/bin/meta_orchestrate.rs:48-52,92-102`.

Risk: unset `XDG_RUNTIME_DIR` fails clearly, but empty or relative `XDG_RUNTIME_DIR` is accepted and produces a relative default such as `orchestrate/orchestrate.sock`. Explicit `PERSONA_ORCHESTRATE_SOCKET` and `PERSONA_ORCHESTRATE_META_SOCKET` overrides are also accepted as arbitrary strings, including relative paths. That lets a checkout-local stale socket be used accidentally.

Expected correction: introduce a shared runtime socket path type for the CLIs. Require default `XDG_RUNTIME_DIR` and explicit overrides to be absolute and non-empty; reject relative values before connect. Include the variable name and resolved/rejected value in the diagnostic.

Current deployed behavior blocker: no, because the observed shell has `XDG_RUNTIME_DIR=/run/user/1001` and the managed sockets are there. It is a blocker for the audit question “including when run from a repo checkout” under malformed env/override conditions.

### Low — connection failures do not include the socket path attempted

Paths: `/git/github.com/LiGoldragon/orchestrate/src/bin/orchestrate.rs:43-47`; `/git/github.com/LiGoldragon/orchestrate/src/bin/meta_orchestrate.rs:40-44`; `/git/github.com/LiGoldragon/orchestrate/src/signal_transport.rs:31-47,55-65`.

Risk: a missing daemon reports only `transport IO error: No such file or directory` through `TransportError`. That is not actionable when defaults have changed and users need to distinguish repo-local stale sockets from `$XDG_RUNTIME_DIR` sockets.

Expected correction: wrap connect failures with the attempted socket path and whether it came from the default or an override variable.

Current deployed behavior blocker: no.

## Recommended fixes/questions

- Add semantic validation after daemon configuration rkyv decode and before writer filesystem effects.
- Move `orchestrate-write-configuration` to validate-first/create-second ordering; add regression tests that relative and `~` paths fail without creating anything in cwd.
- Add CLI tests for default socket path construction with valid, unset, empty, and relative `XDG_RUNTIME_DIR`; add override tests for absolute and relative `PERSONA_ORCHESTRATE_SOCKET`/`PERSONA_ORCHESTRATE_META_SOCKET`.
- Add a daemon/listener regression that a pre-existing regular file at a socket path is not removed.
- Consider centralizing the runtime path constants so the Nix unit, writer invocation, and CLI defaults cannot drift.
- Consider owner-only modes for the state/config files if the state contents are considered sensitive; current live files are under `/home/li` but are mode `0644` inside a `0755` state directory.

## Checks run

Read-only/source-inspection commands only; I did not run cargo or nix builds because the assignment allowed only the requested report as mutation and cargo/nix checks would write target/store artifacts.

- `spirit "(Lookup 10pz)"` → design constraint found.
- `jj status --no-pager` in `/git/github.com/LiGoldragon/orchestrate` → clean working copy.
- `jj show --no-pager --stat @-` → confirmed changed files and commit `62a7682e578863d372fc2b655331029a550a1cdc`.
- Source reads and `rg`/`nl` line inspections listed above.
- `systemctl --user cat orchestrate-daemon.service` → confirmed current materialized paths.
- `pgrep -af 'orchestrate-daemon'`, `ls -l "$XDG_RUNTIME_DIR/orchestrate"`, `ls -la /home/li/.local/state/orchestrate` → confirmed live process and path placement.
- `env -u PERSONA_ORCHESTRATE_SOCKET orchestrate "(Observe Lanes)"` → default ordinary CLI path reached live daemon.
- `find /home/li/primary/orchestrate -maxdepth 1 ...` → no repo-local runtime state/socket files found.

Reported prior checks considered but not rerun:

- Recovery worker: `nix build .#checks.x86_64-linux.test-daemon-cli --no-link --print-build-logs` passed.
- Recovery worker: `nix build .#packages.x86_64-linux.default --no-link --print-build-logs` passed.
- Nix/OS auditor: current unit and live sockets/state passed the non-repo path audit.
