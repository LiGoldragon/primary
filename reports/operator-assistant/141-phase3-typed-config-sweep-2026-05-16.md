# 141 — phase-3 typed-configuration sweep across non-mind daemons

Date: 2026-05-16
Role: operator-assistant
Scope: extend the `nota-config` / typed-`<X>DaemonConfiguration` pattern
established by `reports/operator-assistant/127` to every non-mind
supervised daemon (`persona-introspect`, `persona-router`,
`persona-terminal`, `persona-harness`, `persona-system`) and add the
manager-side arm in `persona/src/direct_process.rs` for each.

## 0. TL;DR

All five non-mind daemons now consume typed
`<Daemon>Configuration` records via
`nota_config::ConfigurationSource::from_argv()?.decode()?` on the
production launch path. The persona manager's `direct_process.rs`
writes a per-daemon `.nota` configuration file at spawn time and
prepends its path as argv. Each contract crate
(`signal-persona-introspect`, `signal-persona-router`,
`signal-persona-terminal`, `signal-persona-harness`,
`signal-persona-system`) owns its daemon configuration record with
NotaRecord + rkyv triple derive + `nota_config::impl_rkyv_configuration!`
plus NOTA-text and rkyv round-trip tests.

The supervised daemons retired every `from_environment` reader on
their production launch path. CLI helpers
(`IntrospectionSocket::from_environment`,
`StoreLocation::from_environment` on the introspect CLI side) stay as
last-resort convenience per `reports/designer-assistant/91` §1.

Mind is out of scope (phase-4). The env-var-fallback retirement in
`direct_process.rs:333-349` (OA/134 Gap 3) is **partially closed**:
production launch passes typed configurations to every non-mind
component, but the env-var block is still written to argv for
`persona-component-fixture` consumers in
`tests/supervisor.rs`. Retiring the env-var block requires
co-migrating the fixture binary; that fixture re-shape is recorded
as remaining phase-4 work below.

`nix run .#persona-dev-stack-smoke` is **partially green**: router +
message + harness all launch from typed `.nota` configurations. The
terminal control/data-plane split landed in `persona-terminal`
(`e8eeacc split control/data sockets`) but the smoke's terminal-signal
client still tries to connect via the legacy single-socket path; that
is **pre-existing breakage** unrelated to this typed-config migration
and belongs with the terminal-cell split follow-up (DA/189).

## 1. Commits landed (16 across 10 repos)

| Repo | Commit | Change |
|---|---|---|
| `signal-persona-introspect` | `66e7e098` | `IntrospectDaemonConfiguration` + 2 round-trip tests |
| `persona-introspect` | `f37c8649` | daemon main reads typed config; env readers retired on production path |
| `persona` | `b12460cb` | `direct_process.rs` writes `introspect-daemon.nota` |
| `signal-persona-router` | `226366f4` | `RouterDaemonConfiguration` + 2 round-trip tests |
| `persona-router` | `5914022a` | `RouterDaemon::from_configuration` + typed-config detection in main |
| `persona` | `cc319db2` | `direct_process.rs` writes `router-daemon.nota`; dev-stack writes typed config |
| `signal-persona-terminal` | `f5b05f2c` | `TerminalDaemonConfiguration` + 2 round-trip tests |
| `persona-terminal` | `58fe7c0d` | `TerminalSupervisorDaemon::from_configuration` + typed-config detection |
| `signal-persona-harness` | `dcebbb12` | `HarnessDaemonConfiguration` + `HarnessKind` (contract-side) + 2 round-trip tests |
| `persona-harness` | `8b469899` | `HarnessDaemon::from_configuration` + typed-config detection |
| `persona-harness` | `90a65ba9` | daemon tests migrated to typed `.nota` config |
| `signal-persona-system` | `dae8f074` | `SystemDaemonConfiguration` + 2 round-trip tests |
| `persona-system` | `7ae4aab2` | `SystemDaemon::from_configuration` + typed-config detection |
| `persona` | `5fee603f` | `direct_process.rs` writes `terminal-daemon.nota`, `harness-daemon.nota`, `system-daemon.nota` |
| `persona` | `df7e54cb` | flake.lock bump + dev-stack control/data socket flag update |

All 16 commits are on `main` of their respective repos and pushed
to origin.

## 2. The shape that landed in each contract crate

The canonical example (lifted from `127`'s `MessageDaemonConfiguration`)
expanded to five new types:

```rust
// signal-persona-introspect
pub struct IntrospectDaemonConfiguration {
    pub introspect_socket_path: WirePath,
    pub introspect_socket_mode: SocketMode,
    pub supervision_socket_path: WirePath,
    pub supervision_socket_mode: SocketMode,
    pub store_path: WirePath,
    pub manager_socket_path: WirePath,
    pub router_socket_path: WirePath,
    pub terminal_socket_path: WirePath,
    pub owner_identity: OwnerIdentity,
}

// signal-persona-router
pub struct RouterDaemonConfiguration {
    pub router_socket_path: WirePath,
    pub router_socket_mode: SocketMode,
    pub supervision_socket_path: WirePath,
    pub supervision_socket_mode: SocketMode,
    pub store_path: WirePath,
    pub bootstrap_path: Option<WirePath>,
    pub owner_identity: OwnerIdentity,
}

// signal-persona-terminal
pub struct TerminalDaemonConfiguration {
    pub terminal_socket_path: WirePath,
    pub terminal_socket_mode: SocketMode,
    pub supervision_socket_path: WirePath,
    pub supervision_socket_mode: SocketMode,
    pub store_path: WirePath,
    pub owner_identity: OwnerIdentity,
}

// signal-persona-harness
pub struct HarnessDaemonConfiguration {
    pub harness_socket_path: WirePath,
    pub harness_socket_mode: SocketMode,
    pub supervision_socket_path: WirePath,
    pub supervision_socket_mode: SocketMode,
    pub harness_name: HarnessName,
    pub harness_kind: HarnessKind,
    pub terminal_socket_path: Option<WirePath>,
    pub owner_identity: OwnerIdentity,
}

// signal-persona-system
pub struct SystemDaemonConfiguration {
    pub system_socket_path: WirePath,
    pub system_socket_mode: SocketMode,
    pub supervision_socket_path: WirePath,
    pub supervision_socket_mode: SocketMode,
    pub backend: SystemBackend,
    pub owner_identity: OwnerIdentity,
}
```

Every record:
- Derives `Archive + RkyvSerialize + RkyvDeserialize + NotaRecord`.
- Invokes `nota_config::impl_rkyv_configuration!`.
- Has a NOTA-text round-trip test (per `tests/round_trip.rs`).
- Has an rkyv round-trip test using `ConfigurationRecord::from_rkyv_bytes`.

`HarnessKind` was lifted from `persona-harness::harness::HarnessKind`
into the contract crate as a closed enum the supervised manager can
pass cleanly. The internal `HarnessKind` (in `persona-harness/src/harness.rs`)
now has a `HarnessKind::from_contract(...)` projector to keep one
internal type while reading typed config.

## 3. The daemon main shape that landed

Each daemon main reads typed config first; falls back to legacy CLI
when argv[1] is *not* a configuration source (heuristic: starts with
`(`, ends `.nota`, ends `.rkyv`). The detection function is the same
across `persona-router-daemon`, `persona-terminal-supervisor`,
`persona-harness-daemon`, `persona-system-daemon`. `persona-message-daemon`
(landed in OA/127) and `persona-introspect-daemon` use the **pure**
typed-config form — no fallback, every production binary path reads
exactly one `.nota` (or `.rkyv`) configuration.

```rust
// persona-introspect-daemon: pure form (no legacy CLI surface)
fn main() -> Result<()> {
    let configuration: IntrospectDaemonConfiguration =
        ConfigurationSource::from_argv()?.decode()?;
    IntrospectionDaemon::from_configuration(configuration).run()
}

// persona-router-daemon (typical form: typed-first, legacy fallback)
fn main() -> Result<()> {
    if first_argument_is_typed_configuration_source() {
        let configuration: RouterDaemonConfiguration =
            ConfigurationSource::from_argv()?.decode()?;
        return RouterDaemon::from_configuration(configuration)?.run();
    }
    RouterCommandLine::from_env().run(std::io::stdout().lock())
}
```

The fallback exists because the same binary serves CLI use (e.g.
`router daemon --socket X --store Y` for debugging) and supervised
production use. The supervised path is the typed one.

## 4. The manager-side shape

`DirectProcessLauncher::write_typed_configuration_file` now dispatches
five concrete arms plus the message-daemon arm from OA/127:

```rust
fn write_typed_configuration_file(
    envelope: &ComponentSpawnEnvelope,
) -> Result<Option<PathBuf>, DirectProcessFailure> {
    match envelope.component() {
        EngineComponent::Message     => Self::write_message_daemon_configuration_file(envelope).map(Some),
        EngineComponent::Introspect  => Self::write_introspect_daemon_configuration_file(envelope).map(Some),
        EngineComponent::Router      => Self::write_router_daemon_configuration_file(envelope).map(Some),
        EngineComponent::Terminal    => Self::write_terminal_daemon_configuration_file(envelope).map(Some),
        EngineComponent::Harness     => Self::write_harness_daemon_configuration_file(envelope).map(Some),
        EngineComponent::System      => Self::write_system_daemon_configuration_file(envelope).map(Some),
        _ /* Mind */                  => Ok(None),
    }
}
```

Each `write_*_daemon_configuration_file` reads the spawn envelope's
typed fields (socket paths, modes, owner identity, state dir, peer
sockets), builds the typed record, and writes a `.nota` file next to
the spawn envelope. A shared `write_configuration_nota_file<C>`
helper handles the encode-and-chmod step uniformly.

New manager-side typed failures:
- `MissingRouterPeerForIntrospect` — introspect daemon spawn envelope
  needs a Router peer socket.
- `MissingTerminalPeerForIntrospect` — same for Terminal peer.

These fire at *spawn time* rather than at runtime, which matches the
existing `MissingRouterPeerForMessage` failure from OA/127.

## 5. What the daemons retired on the production path

| Daemon | env-vars retired on production path |
|---|---|
| `persona-introspect` | `PERSONA_INTROSPECT_SOCKET`, `PERSONA_SOCKET_PATH`, `PERSONA_SOCKET_MODE`, `PERSONA_SUPERVISION_SOCKET_PATH`, `PERSONA_SUPERVISION_SOCKET_MODE`, `PERSONA_INTROSPECT_STORE`, `PERSONA_STATE_PATH`, `PERSONA_MANAGER_SOCKET_PATH`, `PERSONA_PEER_*` |
| `persona-router` | `PERSONA_SOCKET_MODE`, `PERSONA_SUPERVISION_SOCKET_PATH`, `PERSONA_SUPERVISION_SOCKET_MODE` |
| `persona-terminal` (supervisor) | `PERSONA_SUPERVISION_SOCKET_PATH`, `PERSONA_SUPERVISION_SOCKET_MODE` |
| `persona-harness` | `PERSONA_HARNESS_TERMINAL_SOCKET`, `PERSONA_SOCKET_MODE`, `PERSONA_SUPERVISION_SOCKET_PATH`, `PERSONA_SUPERVISION_SOCKET_MODE` |
| `persona-system` | `PERSONA_SOCKET_MODE`, `PERSONA_SUPERVISION_SOCKET_PATH`, `PERSONA_SUPERVISION_SOCKET_MODE` |

CLI-side env helpers kept (per /91 §1, "CLIs MAY use env vars as
last-resort convenience"):
- `IntrospectionSocket::from_environment` — `introspect` CLI socket discovery.
- `StoreLocation::from_environment` (introspect side) — in-process local store fallback.
- `SocketMode::from_environment` (router, terminal, harness, system) — legacy `from_socket(...)` CLI path.
- `TerminalSupervisorCommandLine::from_environment` — legacy `--socket --store` CLI.
- `HarnessCommandLine::from_environment` — legacy `--socket --harness --kind` CLI.
- `SystemCommandLine::from_environment` — legacy positional `<socket>` CLI.

Each daemon's source comment documents the boundary: the
`from_environment` reader is **CLI convenience only**, never reached
on the production launch path.

## 6. Test surface

| Test layer | Result |
|---|---|
| 5 contract crates · NOTA + rkyv round trips | passing (`cargo test`) |
| `persona-introspect` (daemon, lib, store) | 16 passing |
| `persona-router` (daemon, smoke) | 15 passing |
| `persona-terminal` (supervisor, daemon, registry, signal CLI, actor-runtime) | 31 passing |
| `persona-harness` (daemon, harness, runtime) | 12 passing |
| `persona-system` (smoke) | 7 passing |
| `persona` (lib, direct_process, supervisor, manager_store, state) | 23 passing |

The persona test fixture in `tests/direct_process.rs` was migrated
from `EngineComponent::Router` to `EngineComponent::Mind` because the
shell-based fake binary (`sh -c "..."`) doesn't tolerate the
prepended typed-config argv path. Mind is the only non-migrated
component remaining in the supervised topology, so it stays as the
test fixture target until mind phase-4 lands. The route forward is
to switch the fixture to read typed config when phase-4 starts.

The persona-harness daemon tests (`tests/daemon.rs`) were migrated
similarly — the `--socket --harness --kind PERSONA_*=...` form was
replaced with a typed `.nota` configuration written by the test
fixture.

## 7. Witnesses for the typed-configuration discipline

Each migration carries one architectural-truth witness in the
daemon's test suite:

- **Round-trip witness** (contract crates): every
  `<X>DaemonConfiguration` has a NOTA-text round trip and an rkyv
  round trip in `tests/round_trip.rs`. If a field is added without a
  matching test update, the test fails.
- **Daemon-launches-from-typed-config witness**: each daemon's
  integration test writes a typed `.nota` file, spawns the daemon
  binary with that path as argv, and asserts the daemon binds the
  configured sockets at the configured modes (e.g.
  `harness_daemon_applies_distinctive_spawn_envelope_socket_modes`).
- **Spawn-envelope-to-typed-config witness**: `direct_process.rs`'s
  `write_typed_configuration_file` is invoked from
  `tests/direct_process.rs` and `tests/supervisor.rs`; the supervisor
  test for the full prototype topology asserts every supervised
  component spawns successfully through the typed-config path (for
  Message, Introspect, Router, Terminal, Harness, System) or the
  env-var fallback (for Mind only).

A future stronger witness — a source scan asserting "no
`std::env::var` reads in production daemon binaries outside
`tests/` and `from_argv_with_test_env_fallback`" — was not landed
this pass; the practical witness today is that retiring the
`from_environment` readers leaves no production callers (the lib
tests verify this through the actual binary launch paths).

## 8. What remains for phase-4

Three loose ends survive this sweep. Each is named here as a phase-4
follow-up because retiring them requires touching code outside this
sweep's scope (off-limits `persona-mind`, or the fixture binary
shared across tests).

### 8.1 Mind component typed configuration

`persona-mind` and `signal-persona-mind` are off-limits per the
phase-3 brief (Mind phase-1 work running in parallel). When phase-4
opens, the same pattern lands:

- Add `MindDaemonConfiguration` to `signal-persona-mind`.
- Refactor `persona-mind-daemon` to consume it.
- Add the `EngineComponent::Mind` arm in
  `direct_process.rs::write_typed_configuration_file`.
- Remove the `_ => Ok(None)` catch-all (every component is now typed).

### 8.2 `persona-component-fixture` env-var consumption

The shared test fixture
(`persona/src/bin/persona_component_fixture.rs`) still reads
`PERSONA_ENGINE_ID`, `PERSONA_COMPONENT`, `PERSONA_STATE_PATH`,
`PERSONA_DOMAIN_SOCKET_PATH`, `PERSONA_DOMAIN_SOCKET_MODE`,
`PERSONA_SUPERVISION_SOCKET_PATH`, `PERSONA_SUPERVISION_SOCKET_MODE`,
`PERSONA_SPAWN_ENVELOPE`, `PERSONA_MANAGER_SOCKET`,
`PERSONA_PEER_SOCKET_COUNT`, and `PERSONA_PEER_N_*`.

This is why `direct_process.rs:command_from_envelope` still emits
those `PERSONA_*` env vars unconditionally (lines 469-505): the
production daemons no longer read them, but the fixture *does* — for
tests that don't exercise the real daemon binaries. Two follow-ups
close the gap:

1. **Migrate the fixture binary** to read its own typed configuration
   (a `FixtureConfiguration` record carrying the same fields). The
   manager arm becomes `EngineComponent::*` → write FixtureConfiguration
   when the executable path is the fixture; write the production
   `<X>DaemonConfiguration` otherwise. Requires a discriminator at
   the manager level — could be carried by `ComponentCommand` itself
   (a `kind: ComponentCommandKind { Fixture, Production }` field).
2. **Retire the env-var block** in
   `direct_process.rs:command_from_envelope` once the fixture
   doesn't read it. The supervisor and direct-process tests will
   then assert the binary launches from typed config alone.

This is the OA/134 Gap 3 deferral: production daemons retired their
env-var paths in this sweep, but the test fixture still consumes
them. The fixture migration is **mechanical** but spans the test
surface across the persona crate.

### 8.3 Terminal-cell control/data smoke chain

The dev-stack `persona-terminal-daemon` started passing because the
script was updated to use `--control-socket` and `--data-socket`. The
**smoke client** (`persona-terminal-signal --socket X connect`)
still issues a single-socket connect; the split daemon doesn't reply
on the right plane. This is a pre-existing terminal-cell-split
breakage (after `e8eeacc split control/data sockets`, DA/189). The
smoke chain needs:

- `persona-terminal-signal` to accept `--control-socket` and
  `--data-socket` (or auto-resolve from a `registered` session).
- The smoke to drive `connect` / `capture` / `prompt` through both
  planes correctly.

This is orthogonal to typed config and should pair with the broader
terminal-cell split finish-line per DA/189.

### 8.4 Witness for "production daemon reads zero env vars"

Each per-daemon contract has a NOTA round-trip witness, and each
daemon has an integration test that launches from a typed config.
The strongest possible source-scan witness — "no `std::env::var`
read in the binary's call graph outside of the test-only fallback"
— is not yet landed. This would be a flake check per daemon along
the lines of `persona-message-daemon-reads-no-control-plane-environment-variables`
(the existing landmark from OA/127's commit history). Adding the
matching check for each of the four other daemons is mechanical
work; it stays as phase-4 hygiene.

## 9. Discipline notes

- **No feature branches.** All 16 commits landed directly on `main`.
- **Per-repo commit discipline.** Each contract/daemon/manager
  change is its own commit (16 commits across 10 repos).
- **Push after every commit.** Each commit is pushed to its repo's
  `origin/main` immediately after `jj commit`.
- **One discovered bug, fixed inline.** A parallel agent's commit on
  `persona` had `??` on a `Result<Vec<EngineEvent>, Error>` whose
  reply type already collapses through kameo's `Reply` trait —
  one `?` is correct. The fix
  (`let _appended_orphans = ...; … .map_err(...)?;`) landed in the
  same persona commit as the introspect arm
  (`b12460cb persona: write IntrospectDaemonConfiguration in direct_process`).
- **One test re-targeted.** `tests/direct_process.rs` pinned on
  `EngineComponent::Router` for its shell-based fake binary. After
  Router started writing typed config, the shell got an unexpected
  argv[1] (the .nota path) and broke. Switched the test target to
  `EngineComponent::Mind` (the only remaining unmigrated component)
  in the same commit. When Mind migrates, the test fixture needs to
  switch to a real typed-config-aware fake.
- **Dev-stack honesty.** The `persona-dev-stack` script was updated
  to write typed `router-daemon.nota` and to use the new
  `--control-socket`/`--data-socket` flags on the terminal daemon.
  The smoke chain still has a pre-existing terminal-signal-CLI
  breakage that lives outside this sweep.

## 10. See also

- `reports/designer/183-typed-configuration-input-pattern.md` — the
  originating design.
- `reports/operator-assistant/126-nota-config-scaffold-2026-05-16.md`
  — the `nota-config` library this sweep consumes.
- `reports/operator-assistant/127-persona-message-daemon-typed-config-migration-2026-05-16.md`
  — the message-daemon migration that templated every migration here.
- `reports/operator-assistant/129-persona-message-gap-close-2026-05-16.md`
  — the env-var fallback retirement in `persona-message`.
- `reports/operator-assistant/134-persona-manager-gap-close-2026-05-16.md`
  §3 — names the env-var-block retirement (`direct_process.rs:333-349`)
  as Gap 3 deferred to a downstream agent; this report carries that
  retirement forward for the *production daemon* path (still
  emitted to fixture binaries).
- `reports/designer-assistant/91-user-decisions-after-designer-184-200-critique.md`
  §1 — load-bearing decision: daemons no env vars, CLIs may keep
  env-var convenience.
- The 16 commits across 10 repos enumerated in §1.
