# Lojix Daemon Install-First Zeús Deploy Handoff

Role target: `system-maintainer`.

User order: test a Zeús deploy through the new `lojix-daemon`, but do it by
installing the daemon in the system first, not by running the daemon directly
from the source tree.

## Current verified state

The relevant source repos are clean, fetched, pushed, and on `main`:

- `lojix` main: `efbc5ea8` — build closure selects `.drv` outputs with `^*`.
- `signal-lojix` main: `c33e2be4` — regenerated against current
  `schema-rust-next`.
- `meta-signal-lojix` main: `defade02` — regenerated against
  `signal-lojix c33e2be4`.

The daemon source already ships the intended binaries:

- `lojix-daemon`
- `lojix`
- `meta-lojix`
- `lojix-write-configuration`

Verification already run from source:

- `cargo test --locked` passed in all three repos.
- `cargo test --locked --features nota-text` passed in all three repos.
- The ignored daemon smoke
  `cargo test --locked --test build_smoke daemon_binary_socket_roundtrip_eval -- --ignored --exact --nocapture`
  passed: it spawned `lojix-daemon`, bound sockets, sent an owner-socket deploy,
  ran real `nix eval`, and got `Deployed`.
- Owner-socket hardening passed:
  `permissive_owner_socket_mode_is_refused`.
- Oversized hostile frame hardening passed:
  `oversized_frame_is_bounded_and_daemon_survives`.
- Concurrent owner deploy plus ordinary query passed:
  `concurrent_requests_are_served_in_parallel`.

Important caveats:

- The three repos do not yet have repo-local Nix flakes. That is below the
  workspace standard for shipping system software.
- No `lojix-daemon` is installed locally today: no process, no systemd unit, no
  `/run/lojix/*` sockets.
- CriomOS-home still installs `lojix-run`, which wraps legacy `lojix-cli`; it is
  not wired to the daemon stack.
- One ignored external test currently fails:
  `production_eval_materializes_horizon_inputs_and_returns_deployed` expects an
  Eval reply marker commit sequence of `1`, but the daemon returns `0`. Because
  Eval does not activate or commit a generation, this may be a stale assertion,
  but system-maintainer should treat it as a readiness blemish to resolve or
  explicitly document before claiming a fully green external suite.

## Required maintainer shape

Do not test Zeús by running `target/debug/lojix-daemon` as the final validation.
The requested path is:

1. Add a Nix package/check surface for `lojix` that builds the daemon and both
   CLIs with `nota-text` enabled for human-facing NOTA requests.
2. Add an installed service/socket configuration for the local operator host.
3. Deploy that system/home change so `lojix-daemon`, `lojix`, `meta-lojix`, and
   `lojix-write-configuration` are available from the profile or system closure.
4. Start the installed daemon from binary rkyv startup configuration.
5. Run Zeús deploy validation through the installed `meta-lojix` client and the
   installed daemon sockets.

The daemon itself must still obey the component rule: it takes exactly one
binary rkyv startup argument. `lojix-write-configuration` is the NOTA-to-rkyv
boundary.

## Suggested installed runtime contract

Use ordinary and owner sockets under `/run/lojix`:

- ordinary socket: `/run/lojix/ordinary.sock`
- owner socket: `/run/lojix/owner.sock`
- state directory: `/var/lib/lojix`
- ordinary socket mode: `0660`
- owner socket mode: `0600` or `0660` with no other-access; the daemon rejects
  modes granting other access.

The daemon client env vars are:

- `LOJIX_ORDINARY_SOCKET`
- `LOJIX_OWNER_SOCKET`

The package must enable `nota-text`; otherwise inline `.nota` operator requests
are intentionally rejected.

## Manual commands after install

These commands are for the installed binaries, not `target/debug`.

Generate startup:

```sh
sudo install -d -m 0750 /run/lojix /var/lib/lojix
lojix-write-configuration \
  '(ConfigurationWriteRequest (/run/lojix/ordinary.sock 432 /run/lojix/owner.sock 384 /var/lib/lojix /run/lojix/startup.rkyv))'
```

Start the daemon through the installed service if one exists. If the service
does not yet exist, system-maintainer should add it before calling the install
work complete. As a temporary smoke only:

```sh
lojix-daemon /run/lojix/startup.rkyv
```

Zeús Eval through the installed owner socket:

```sh
LOJIX_OWNER_SOCKET=/run/lojix/owner.sock \
meta-lojix \
  '(Deploy (System (goldragon zeus FullOs /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS/main Eval None [] None)))'
```

Then Build:

```sh
LOJIX_OWNER_SOCKET=/run/lojix/owner.sock \
meta-lojix \
  '(Deploy (System (goldragon zeus FullOs /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS/main Build None [] None)))'
```

Then cautious activation with Boot, not Switch:

```sh
LOJIX_OWNER_SOCKET=/run/lojix/owner.sock \
meta-lojix \
  '(Deploy (System (goldragon zeus FullOs /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS/main Boot None [] None)))'
```

Query daemon state:

```sh
LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock \
lojix '(Query (ByNode (goldragon zeus None)))'
```

## Acceptance for the handoff

The work is not complete when the source test passes. It is complete when:

- The installed system/home closure provides the daemon and both clients.
- The daemon is started from generated rkyv startup, not inline NOTA.
- The installed daemon exposes the two sockets with correct modes.
- `meta-lojix` Eval and Build for Zeús succeed through the installed owner
  socket.
- The Boot deploy is either completed successfully or explicitly stopped with a
  typed daemon rejection that names the real missing prerequisite.
- An ordinary query through the installed ordinary socket reports the daemon's
  post-test state.

