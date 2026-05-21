# Persona-Spirit Production User Session Deployment

## Result

Production CriomOS is the `main` stack under `/git/github.com/LiGoldragon`, not the `~/wt/horizon-leaner-shape` rewrite worktrees.

I deployed persona-spirit through production `CriomOS-home` only. No CriomOS OS rebuild was needed because persona-spirit is a user-session daemon plus command-line client, not a system service.

The deployed production home commits are:

- `e765cac2`: adds `persona-spirit` as a CriomOS-home flake input, installs `spirit`, adds `persona-spirit-daemon.service`, and pins the persona-spirit input in `flake.lock`.
- `7e99b67c`: fixes the daemon service contract by passing inline NOTA configuration instead of a NOTA file path.
- `d09eac39`: wraps the installed `spirit` command so it defaults to the packaged socket paths when the current shell lacks the socket environment variables.

## Production Wiring

The Home Manager module is:

- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/spirit.nix`

It installs `spirit` in the home profile for `size.min` users and enables:

- `persona-spirit-daemon.service`
- `PERSONA_SPIRIT_SOCKET=/home/li/.local/state/persona-spirit/spirit.sock`
- `PERSONA_SPIRIT_OWNER_SOCKET=/home/li/.local/state/persona-spirit/owner.sock`

The daemon uses:

- ordinary socket: `/home/li/.local/state/persona-spirit/spirit.sock`
- owner socket: `/home/li/.local/state/persona-spirit/owner.sock`
- store: `/home/li/.local/state/persona-spirit/persona-spirit.redb`
- socket mode: `0600`

## Component Contract Findings

The persona-spirit CLI does not auto-discover sockets. It reads `PERSONA_SPIRIT_SOCKET` for ordinary requests and `PERSONA_SPIRIT_OWNER_SOCKET` for owner requests.

The daemon accepts exactly one inline NOTA configuration argument. It does not currently read a NOTA config file path, even though the CLI can read request files. The service therefore starts through a small Home Manager-generated wrapper that executes:

```sh
persona-spirit-daemon '("/home/li/.local/state/persona-spirit/spirit.sock" "/home/li/.local/state/persona-spirit/owner.sock" "/home/li/.local/state/persona-spirit/persona-spirit.redb" 384 None)'
```

The installed `spirit` command is also wrapped. It preserves explicit socket environment overrides, but defaults both socket variables to the production home paths when they are unset. This makes the command work in already-running shells that have not picked up the new Home Manager session variables.

## Verification

Component package check:

- Built `persona-spirit` packages `spirit` and `persona-spirit-daemon`.
- Ran a temporary live daemon smoke test: `spirit` recorded a test entry, observed it back, and sent an owner `Register` request.

Home build and deploy:

- Built the Home Manager activation package from the local production CriomOS-home checkout with the real `goldragon ouranos li` projection.
- Pushed the production home commits to `CriomOS-home/main`.
- Refreshed `github:LiGoldragon/CriomOS-home/main` and confirmed it resolved to `d09eac39`.
- Activated with lojix:

```nota
(HomeOnly goldragon ouranos li "/git/github.com/LiGoldragon/goldragon/datom.nota" "github:LiGoldragon/CriomOS-home/main" Activate None None)
```

Runtime checks after activation:

- `persona-spirit-daemon.service` is enabled.
- `persona-spirit-daemon.service` is active and running.
- Both sockets exist with owner-only socket permissions.
- `spirit '(Observe State)'` succeeds even with `PERSONA_SPIRIT_SOCKET` unset in the invoking environment.
- `spirit '(Register (operator))'` succeeds even with `PERSONA_SPIRIT_OWNER_SOCKET` unset in the invoking environment.

## User Attention

No approval or manual action is needed for this deployment. The current user session has a running persona-spirit daemon, and `spirit` is available from the home profile.
