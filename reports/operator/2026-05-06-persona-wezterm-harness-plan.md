# Persona WezTerm Harness Plan

Date: 2026-05-06
Agent: operator

## Goal

Start Persona's harness-control module with WezTerm as the first practical
adapter. The adapter is not the final Persona harness protocol; it is the
fastest credible bridge for:

- spawning terminal harnesses;
- discovering sessions, windows, tabs, and panes;
- reading pane text;
- injecting terminal input such as `/compact`;
- reconnecting to existing sessions;
- testing local and later remote/headless WezTerm mux workflows.

## First Slice

```mermaid
flowchart LR
    shim[shim binary]
    lib[persona::harness::wezterm]
    cli[wezterm cli]
    mux[WezTerm mux]
    pane[pane running command]

    shim --> lib
    lib --> cli
    cli --> mux
    mux --> pane
```

The first implementation should wrap `wezterm cli` rather than link to private
WezTerm internals. That keeps the dependency simple and lets us pin the runtime
tool through Nix.

## Library Shape

```text
harness
  Adapter trait
  HarnessCommand
  HarnessTarget
  HarnessPane
  HarnessSnapshot

harness::wezterm
  Wezterm
  WeztermSpawn
  WeztermPane
  WeztermTextCapture
```

Operations:

```text
spawn(command, args, domain, cwd) -> pane id
list() -> panes
get_text(pane id) -> text snapshot
send_text(pane id, text, paste_mode) -> result
send_key(pane id, key) -> result
```

## Shim Binaries

Initial binaries should stay small and exercise the library:

```text
persona-harness-wezterm
  list
  spawn -- <command> [args...]
  text --pane-id <id>
  send --pane-id <id> --text <text>
  smoke -- <command> [args...]

persona-harness-run
  claude
  codex
  pi
```

`persona-harness-run` should start as a configuration-aware convenience shim.
It can know default commands and model flags later, but the first pass should
avoid hardcoding secrets or assuming logged-in provider state.

## Test Strategy

Automated closed tests:

- parse sample `wezterm cli list --format json` output;
- build correct `wezterm cli` command lines;
- handle non-zero command failures cleanly;
- run a smoke command only when `wezterm` is available.

Runnable authenticated tests:

- spawn `claude`;
- spawn `codex`;
- spawn `pi`;
- capture initial text;
- send a harmless prompt or slash command;
- reconnect/list/capture again.

These should be normal binaries or explicitly ignored tests so they can use the
user's existing authenticated sessions without running in CI or during ordinary
`cargo test`.

## Nix

Add WezTerm to the development/build environment if the package is available
for the target system. The Rust crate should still build without WezTerm
installed; WezTerm is a runtime dependency for integration shims and tests.

## Immediate Risks

- WezTerm may not be installed on this machine outside `nix develop`.
- Some `wezterm cli` commands need a GUI/mux context to already exist.
- Remote/headless mux tests need a second step after local spawn/read/send works.
- `claude`, `codex`, and `pi` authenticated tests must be opt-in.

## Implementation Pass

Landed in `/git/github.com/LiGoldragon/persona`:

- `persona::harness` with `HarnessProgram`, `HarnessProfile`, and cheap default
  profiles for `claude`, `codex`, and `pi`;
- `persona::harness::wezterm` with typed pane ids, pane list parsing, spawn
  requests, text capture requests, typed/bracketed input, kill, and smoke
  operations;
- `persona-harness-wezterm` shim for low-level `list`, `spawn`, `text`, `send`,
  `kill`, and `smoke`;
- `persona-harness-run` shim for profile-based `claude`, `codex`, and `pi`
  spawns;
- Nix dev-shell and package wrapping for WezTerm;
- normal unit/integration tests plus ignored live WezTerm/authenticated tests.

Verified:

```text
nix develop -c cargo fmt --all
nix develop -c cargo test
nix flake check
nix build .#
PERSONA_WEZTERM_PREFER_MUX=1 result/bin/persona-harness-wezterm list
PERSONA_WEZTERM_PREFER_MUX=1 result/bin/persona-harness-wezterm smoke --new-window -- sh -lc 'printf PERSONA-WEZTERM-SMOKE; sleep 60'
```

The headless smoke succeeded against an auto-started WezTerm mux and captured
`PERSONA-WEZTERM-SMOKE` from the pane. The test-created pane and mux server were
cleaned up after the manual smoke.
