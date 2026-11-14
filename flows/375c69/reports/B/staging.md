# B staging report — flow375c69

## Scope and identity

Read-only inspection only. No build, test, Nexus start, process fixture,
network/model call, capsule/VM creation, database open, production path or
configuration change was performed.

The native/thread identity of this model run is not exposed in the available
shell environment. `FLOW_ID`, `THREAD_ID`, `NATIVE_*`, and `MODEL` are absent;
therefore no native binding or thread identifier is asserted.

The inspection shell was:

- PID `2036005`, UID `1001` (`li`), started `Thu Nov 5 17:05:41 2026`.
- Parent PID `2242`, UID `1001`, `codex app-server --remote-control
  --listen unix:///home/li/.codex-next-8mkkxq293hk2/app-server-control/app-server-control.sock`,
  started `Mon Nov 2 08:18:38 2026`.
- Grandparent PID `2183`, UID `1001`, user systemd, started `Mon Nov 2
  08:18:38 2026`; its parent is PID 1.

This is process ancestry for the inspection shell, not proof of the model's
native/thread identity.

## Immutable Flow source and pins

Inspected exactly:

`/nix/store/dz5dwigzydw2khv6wpgq3556hw83j4x7-source`

Observed Nix path metadata:

- NAR hash `sha256-Ujf7Jrw1cwprxxy8Pd4e5XI+yufalS/6Tav+SdXkudc=`.
- NAR size `3482224`.
- No deriver; no store references.
- Cargo workspace version `0.51.0` (`Cargo.toml`).
- `signal-flow` git revision `ce083f2ba9cc0bd928735ba4cc09e59965982e30`.
- `meta-signal-flow` git revision `281f5aa1b88cd43609c127cdf6f3c12645faf58b`.
- The source has no `flake.nix`, no Nix files, and its `capsule/`, `checks/`,
  `docs/`, `launcher/`, and `nix/` directories are empty.

Pointers:

- `Cargo.toml`: workspace version and signal/meta-signal pins.
- `crates/flow/Cargo.toml`: `flow-hook` binary and dependencies.
- `crates/flow/tests/hook_socket.rs`: bounded socket witness.
- `crates/flow/src/hook.rs`: hook event parsing and typed socket invocation.
- `crates/flow/src/main.rs`: explicit invocation socket connection.

## Supported bootstrap currently visible

The primary workspace declares these pinned inputs in `/home/li/primary/flake.nix`,
including `flow` at `f111805de99494addb7cb3c3f668723373cfa123` and `nixpkgs` at
`2d1e72b652ee13fd1297641ce735e06416d22827`. This is workspace tooling, not a
capsule implementation.

The checked-in `/home/li/primary/flow/flake.nix` declares a Nix-supported
bootstrap surface:

- `nix build /home/li/primary/flow` (default package, workspace build).
- `nix develop /home/li/primary/flow` (dev shell with Rust toolchain,
  jujutsu, and Nix).
- The flake's checks include ordinary Cargo tests and exact tests, but no
  capsule target.

These commands were not run. No supported capsule bootstrap command or capsule
pin is present in the immutable installed Flow source. The supplied immutable
path and dependency pins are the only exact installed source pins verified.

## Isolation evidence

No source evidence establishes OS-level capsule isolation, network denial,
mount allowlists, home/credential exclusion, or test-only path confinement.

The strongest relevant witness is
`crates/flow/tests/hook_socket.rs`: it uses a `tempfile` root, creates two Unix
socket listeners, invokes `flow-hook` with `env_clear()`, supplies an explicit
socket argument, and sets an inherited decoy `FLOW_SOCKET`; the hook reports
only through the typed socket. This proves typed-socket selection and a clean
child environment in that test, not a capsule boundary.

`crates/flow/src/hook.rs` states that `FLOW_ID` is read from the harness
environment and the socket is supplied as typed invocation configuration.
`crates/flow/src/main.rs` connects to the explicit invocation socket. Neither
file provides namespace, mount, network, credential, HOME, Memory, Herdr, or
host-production-socket isolation.

## Gate result and unknowns

Core's requested precondition is not met: a supported real capsule bootstrap
and isolation proof cannot be verified from the immutable installed source or
available workspace flakes. Fresh/refresh actual hook execution, adoption,
Stop/marks/continuities/successor-queue effects, and all other prospective
runtime effects remain unauthorized and were not attempted.

Unknowns requiring a separately supplied authoritative artifact: the capsule
runtime/tool, its exact pinned source, its bootstrap invocation, and a witness
covering no host production socket/Memory/Herdr/home/credentials mounts and no
network.

## Identity correction (next inspection child)

The earlier shell identity was historical and is not reused. This records the actual /proc identity of the next inspection child used for this correction:

- PID: `2045130`
- UID: `1001`
- Executable: `/nix/store/8aprjbczx0admjfd7zrjafk236zib0mv-zsh-5.9.2/bin/zsh`
- /proc/2045130/stat field 22 (starttime token, after the final ) space): `29122596`
- Parent PID: `2242`
- CODEX_THREAD_ID: `01a1adf5-cdf0-76e1-84d6-f0fe34833dd4`

CODEX_THREAD_ID is the collaboration subthread/session identifier available to this inspection child; it is not proof of the main-flow native identity. The native identity and binding remain unknown.
