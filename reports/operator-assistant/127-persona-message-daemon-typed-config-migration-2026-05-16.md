# 127 — `persona-message-daemon` typed-configuration migration (per designer/183 §5–7)

Date: 2026-05-16
Role: operator-assistant
Scope: migrate `persona-message-daemon` from environment-variable
configuration to typed `MessageDaemonConfiguration` records passed
on argv via `nota-config`, per `reports/designer/183` §10 step 3.
First of the per-daemon migrations.

## 0. What landed

Three repos pushed to `main`:

| Repo | Commit | Change |
|---|---|---|
| `signal-persona-message` | `f1b36a8a` | Added `MessageDaemonConfiguration` typed record + `nota_config::impl_rkyv_configuration!`. Two round-trip tests (NOTA text + rkyv). |
| `persona-message` | `ad73f810` | Daemon `main` reads via `ConfigurationSource::from_argv()?.decode()?`; `MessageDaemon::from_configuration` is now the canonical constructor; env-var ingestion paths removed. Test fixture writes a typed configuration file. |
| `persona` | `cdfed291` | `direct_process.rs` writes a `MessageDaemonConfiguration` NOTA file at spawn time for the `Message` component and passes that path as argv. `scripts/persona-dev-stack` updated symmetrically. `flake.lock` bumped to the new `persona-message` rev. |

**End-to-end witness:** `nix run .#persona-dev-stack-smoke` passes
green after the cutover. The three-daemon stack (message + router +
terminal) runs the full submission/inbox flow through the new typed
config without any control-plane env vars on the message daemon's
launch path.

## 1. The shape that landed

### 1.1 `signal-persona-message::MessageDaemonConfiguration`

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, NotaRecord, ...)]
pub struct MessageDaemonConfiguration {
    pub message_socket_path: WirePath,
    pub message_socket_mode: SocketMode,
    pub supervision_socket_path: WirePath,
    pub supervision_socket_mode: SocketMode,
    pub router_socket_path: WirePath,
    pub owner_identity: OwnerIdentity,
}

nota_config::impl_rkyv_configuration!(MessageDaemonConfiguration);
```

Six fields, dual NotaRecord + rkyv triple derive, re-using
`signal_persona::{WirePath, SocketMode}` and
`signal_persona_auth::OwnerIdentity` (no new wire newtypes).
Round-trip tests confirm both forms.

### 1.2 `persona-message-daemon` main

```rust
fn main() -> Result<()> {
    let configuration: MessageDaemonConfiguration =
        ConfigurationSource::from_argv()?.decode()?;
    MessageDaemon::from_configuration(configuration).run()
}
```

Three lines, matches `designer/183` §7.2 exactly. The `MessageDaemon`
struct now carries every input field as data — no `Option`s, no
runtime env-var reads. `MessageDaemonInput` (the in-process test
constructor) requires the same fields explicitly.

The retired surface:
- `MessageDaemonCommandLine` (the argv+env reader)
- `SocketMode::from_environment`
- `MessageOriginStamper::from_environment`
- env-var reads for `PERSONA_SOCKET`, `PERSONA_SOCKET_PATH`,
  `PERSONA_SOCKET_MODE`, `PERSONA_MESSAGE_ROUTER_SOCKET`,
  `PERSONA_SUPERVISION_SOCKET_PATH`,
  `PERSONA_SUPERVISION_SOCKET_MODE`, `PERSONA_PEER_*`.

`MessageOriginStamper::from_spawn_envelope_path` is **kept** for an
existing test that exercises spawn-envelope decoding; the daemon's
production path no longer touches it.

The CLI (`message` binary) is unchanged — it still reads
`PERSONA_MESSAGE_SOCKET` to know where to *connect*. That's not
control-plane configuration; it's the CLI's connection target and
outside `designer/183`'s scope.

### 1.3 `persona/src/direct_process.rs`

`DirectProcessLauncher::launch` now calls a new
`write_typed_configuration_file(envelope)` helper that dispatches
per `EngineComponent`. For `Message` it builds a typed
`MessageDaemonConfiguration` from the spawn envelope's fields,
writes a `.nota` file next to the spawn envelope, and returns the
path. `command_from_envelope` accepts that path and prepends it as
argv.

For every **other** component, the helper returns `None` and the
existing env-var sets still apply — each component migrates on its
own PR per `designer/183` §5.3.

```rust
fn write_typed_configuration_file(envelope: &ComponentSpawnEnvelope)
    -> Result<Option<PathBuf>, DirectProcessFailure>
{
    match envelope.component() {
        EngineComponent::Message => Self::write_message_daemon_configuration_file(envelope).map(Some),
        _ => Ok(None),
    }
}
```

New error variant: `DirectProcessFailure::MissingRouterPeerForMessage`
— fires if a spawn envelope for the message component arrives
without a Router peer socket. Structural failure at spawn time
rather than runtime confusion.

### 1.4 `scripts/persona-dev-stack`

Symmetric to `direct_process.rs`: a new
`write_message_daemon_configuration` helper emits the NOTA record,
and `start_message_daemon` invokes
`"$message_daemon_bin" "$message_daemon_configuration"` — one argv,
no env vars on the message daemon's control plane.

## 2. Verification

| Witness | Result |
|---|---|
| `cargo test --release` in `signal-persona-message` | 18 tests passing (including 2 new `MessageDaemonConfiguration` round-trips). |
| `cargo test --release` in `persona-message` | 17 tests passing (11 in `tests/message.rs` after fixture rewrite, 6 in `actor_runtime_truth.rs`). |
| `cargo build --release` in `persona` | clean compile after `cargo update -p signal-persona-message`. |
| `nix run .#persona-dev-stack-smoke` | **green end-to-end** — submission stamps origin, router persists, inbox query returns the record. |

The dev-stack smoke is the load-bearing witness: it runs real
daemons (no actor-in-process mocks), drives the full
`message → router → terminal` flow through Unix sockets, and
confirms the daemon binds and stamps from the typed config alone.

## 3. Discipline notes

- **No feature branches.** Per user direction: all three repos
  worked directly on `main`. Commits landed in dependency order
  (contract → consumer → manager) and each push was self-contained
  enough that nothing was broken between commits — the manager
  doesn't compile against the new message-daemon until the lock is
  bumped, which is the same commit that introduces the dev-stack
  config path.
- **Tests updated, not deleted.** The integration test that spawns
  the real binary now writes a typed config file via the fixture
  helper `write_message_daemon_configuration`. The shape of the
  test is the same; only the launch contract changed.
- **`MessageOriginStamper::from_environment` retired.** It read
  `PERSONA_SPAWN_ENVELOPE`. The owner identity now flows on the
  argv'd typed config; the spawn envelope file still exists (the
  manager keeps writing it for other components and as an audit
  artifact) but the message daemon never reads it.
- **No test-shim env-var fallback in this daemon.** Per
  `designer/183` §7.3's note ("for `persona-message-daemon`, it's
  not [appropriate]") and the fact that the existing integration
  tests already used argv positions, the cleaner cutover was to
  update the fixture to write a config file rather than introduce
  `from_argv_with_test_env_fallback`.
- **A 2026-05-16 bump of `persona-message` in `persona/flake.lock`**
  is part of this PR. The dev-stack smoke pulls the daemon binary
  through that pin; without the bump, it would silently keep the
  old env-var-reading binary.

## 4. What's next — the rest of `designer/183` §5.3

The migration order from heaviest to lightest env-var user:

| Daemon | Migration done? |
|---|---|
| `persona-message` | ✅ this PR |
| `persona-introspect` | open |
| `persona` manager | open |
| `persona-terminal` | open |
| `persona-mind` / `persona-router` / `persona-harness` / `persona-system` | open |
| `criome` | open |

Each follows the same three-repo shape that landed here:

1. **Add `<X>DaemonConfiguration` to `signal-persona-<x>`** (per
   `designer/183` §8 Q4: per-component contract crate owns its
   config) with NotaRecord + rkyv triple + `impl_rkyv_configuration!`.
2. **Refactor `<x>-daemon`'s main + struct** to consume the typed
   config; drop the env-var reads.
3. **Update `persona/src/direct_process.rs`'s
   `write_typed_configuration_file` match arm** for the new
   component to write its config file and pass argv; update
   `scripts/persona-dev-stack` symmetrically.

The pattern is now templated. The next migration (likely
`persona-introspect`, second-heaviest env-var user) can follow this
report's shape line-for-line.

## 5. See also

- `reports/designer/183-typed-configuration-input-pattern.md` —
  the originating design.
- `reports/operator-assistant/126-nota-config-scaffold-2026-05-16.md`
  — the `nota-config` crate scaffold that this migration consumes.
- `reports/designer-assistant/76-review-operator-assistant-125-persona-engine-audit.md`
  §2.2 + Q1 — names typed daemon configuration as the right
  destination for stateful-daemon launch paths.
- `reports/designer/181-persona-engine-analysis-2026-05-15.md`
  §7 Q2 — supersedes the older owner-uid-from-spawn-envelope
  question by pointing at this migration.
- `https://github.com/LiGoldragon/nota-config` — the library.
- `https://github.com/LiGoldragon/signal-persona-message/commit/f1b36a8a`
  — the contract addition.
- `https://github.com/LiGoldragon/persona-message/commit/ad73f810`
  — the daemon refactor.
- `https://github.com/LiGoldragon/persona/commit/cdfed291`
  — the manager + dev-stack updates.
