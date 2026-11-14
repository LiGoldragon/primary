# Flow at start: three facts (for Fable int7)

Read from the pushed revisions: flow origin/main (0.56.2, the live line), flow origin/pko0-90d453 and pko0-e3a7d1, translator origin/main e7cd5bc and origin/pko0-e3a7d1, CriomOS-home origin/main.

## 1. A tool compiling datom configuration into a Signal file

- **On a branch only, not on any main and not live.** translator `pko0-e3a7d1`, `src/bin/nexus-configure.rs`:
  `nexus-configure 'Compile.{ place.datom flow-nexus.signal }'` compiles a place written in datom into "the place file every Nexus reads before any socket opens", framed signal, at `$XDG_CONFIG_HOME/nexus/<place-name>/<nexus-name>.signal` (`src/place_file.rs:1-2`). It holds the Place alone (name, Runtime, State), per ruling qyb2, not the Nexus's configuration.
- The Flow branch `pko0-90d453` reads that file (`crates/flow-nexus/src/place.rs:70-80`). It is not merged; translator main has no such binary (only `placement.ethos`).
- **No Nexus reads such a file today.** Nothing on any main reads a configuration Signal file at start.

## 2. flow-defaults

`crates/flow-defaults/src/lib.rs`, literals in Rust (`LaysOutDefaults`, lines 93-106):

```rust
const STATE_DIRECTORY: &str = ".local/state/flow";
const STORE_FILE: &str = "flow.sema";
const SOCKET_DIRECTORY: &str = "flow";
const ORDINARY_SOCKET: &str = "flow.sock";
const META_SOCKET: &str = "flow-meta.sock";
const SOURCE_ROOT: &str = "primary";
const STABLE_CODEX_CLIENT: &str = "codex-stable-flow-client";
const STABLE_CODEX_HOME: &str = ".codex";
const STABLE_CODEX_MODELS: [&str; 2] = ["gpt-5.6-sol", "gpt-5.6-luna"];
const NEXT_CODEX_CLIENT: &str = "codex-next-flow-client";
const NEXT_CODEX_HOME: &str = ".codex-next";
const NEXT_CODEX_MODELS: [&str; 3] = ["gpt-6-sol", "gpt-6-luna", "gpt-6-astra"];
const CODEX_CONTROL_SOCKET: &str = "app-server-control/app-server-control.sock";
```

anchored on `HOME`, `XDG_RUNTIME_DIR`, `/etc/passwd` and `/proc/self` (lines 45-90). Who reads them, on main:
- the store seeds a new Memory's configuration from them (`crates/flow-nexus/src/store.rs:344-404`, `impl SeedsConfiguration for DefaultConfiguration`; `open_seeded`, line 2175);
- `herdr.rs:161-215` builds the herdr and Codex placeholders and the Claude paths from them, until the first `Configure.Nexus` replaces the placeholders (the Claude paths are never replaced; bead primary-12s9);
- the clients reach the default sockets through them.

## 3. What the Flow Nexus reads at start today (main, live)

- **Its place: one typed datom argument**, `flow-nexus-daemon "{ <name> <runtime> <state> }"`, written by CriomOS-home (`modules/home/profiles/min/flow-nexus-place.nix:261`, `ExecStart` line 429); parsed in `crates/flow-nexus/src/main.rs:111-118`.
- **Its sockets and Memory: compiled file names joined to the place's two directories**: `Runtime/flow.sock`, `Runtime/flow-meta.sock`, `State/flow.sema` (`crates/flow-nexus/src/place.rs:16-24`, `crates/flow-ethos/src/place.rs:42-43`).
- **Its configuration, for a new Memory: compiled into the executable.** The live package builds the daemon with the feature `executable-default-configuration` (`nix/mk-flow-package.nix:1-10, 218`), a generated Rust module of the configuration that seeds a new, unconfigured Memory (`main.rs:25-43`). A Memory that exists is not re-seeded.

So today the configuration your words describe as a Signal file is carried as Rust compiled into the daemon, and the Signal-file tool on the branch carries only the place.
