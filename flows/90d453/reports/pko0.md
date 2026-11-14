# pko0 onto the release line, phase 1 of 2: the condition does not hold

Phase 1 stops here, as briefed. Part A found inputs at start beyond the Place, and the translator side finds its sockets from something else. Nothing was rebased, built, pushed or gated. Part B waits on a ruling.

Read: flow pko0-e3a7d1 8f78c73, translator pko0-e3a7d1 130c27a, CriomOS-home origin/main e7a4157e (its Flow units are the ones named below; the working checkout is dirty and was not read). Line numbers are those revisions'.

## The condition, answered

The condition: the sockets, the memory and the translator are each found from the Place alone, with nothing else read at start.

- **Sockets and memory: found from the Place once the Place is found, but the Place is not found from itself.** The daemon takes Runtime and State from the place file. To find that file it reads its argument and two environment variables, and with no file it reads three more. See the list.
- **The translator: there is none in Flow, and Flow's text front end does not use the Place.** The condition fails here, and it is the larger failure.

## Every input read at start

### The Nexus daemon, `flow-nexus-daemon`

Entry is `crates/flow-nexus/src/main.rs`.

| # | Input | Where | Used for | Kind |
|---|---|---|---|---|
| 1 | argv[1], the place name datom | main.rs:98 (`std::env::args`), parsed main.rs:44-60 | which place; names the place file's directory | argument |
| 2 | `XDG_CONFIG_HOME`, else `HOME` | translator 130c27a `src/place_file.rs:41-42` (`ConfigurationHome::of_process`), called from flow `crates/flow-nexus/src/place.rs:70` | where the place file lies: `<home>/nexus/<place-name>/flow-nexus.signal` | environment |
| 3 | The Nexus name `flow-nexus` | flow-ethos `crates/flow-ethos/src/place.rs:95` (`NEXUS_NAME`), via `place.rs:61` | the place file's name | compiled constant |
| 4 | The place file itself | `place.rs:77-80`, read by translator `place_file.rs` (`ReadsPlaceFile`) | Runtime and State | file (this is the Place) |
| 5 | `XDG_RUNTIME_DIR` | translator `src/lib.rs:106,122`, called from flow `place.rs:82` when there is no place file | the default Runtime `$XDG_RUNTIME_DIR/nexus/<place>` | environment, only with no place file |
| 6 | `XDG_STATE_HOME`, else `HOME` | translator `src/lib.rs:106,133,137` | the default State | environment, only with no place file |

Inputs 5 and 6 are choice 3 of the build report: with no place file the Nexus starts at the defaults and does not refuse. They are a second way to find sockets and memory, and that second way reads the environment.

The sockets and the memory themselves are then `Runtime/flow.sock`, `Runtime/flow-meta.sock` and `State/flow.sema`: compiled file names (flow-ethos `place.rs:42-43`, flow-nexus `place.rs:21`) joined to the Place's two directories.

Other reads at start, none of which finds a socket or the memory:

| # | Input | Where | Used for |
|---|---|---|---|
| 7 | `HOME`, `XDG_RUNTIME_DIR`, `/etc/passwd`, `/proc/self` | `crates/flow-defaults/src/lib.rs:45-54,73-90`, called from `crates/flow-nexus/src/herdr.rs:161` (`HerdrCli::default`, run from `RunningNexus::open`, lib.rs:1067) | placeholders for the Codex endpoints and source root, replaced when the first `Configure.Nexus` is applied; also an ordinary-socket default (herdr.rs:215) that lib.rs:1071 overrides with the Place's |
| 8 | `CLAUDE_CONFIG_DIR`, else `HOME/.claude` | herdr.rs:166-206 | `claude_transcript_root`, `claude_daemon`, `claude_sessions`. **No configuration replaces these**: they stay read from the environment for the whole run. |
| 9 | `std::env::current_exe()` | herdr.rs:211 | the default hook path beside the daemon |
| 10 | `NOTIFY_SOCKET` | lib.rs:2338 | readiness is announced to systemd; an output, not a place |
| 11 | The memory at `State/flow.sema` | lib.rs:1043-1057 | the committed configuration, if any (it is empty on a new memory) |

So the daemon reads nothing but the Place for Runtime, State and the file names. Two things stand against "the Place alone": the file's own address (inputs 1 to 3), and the no-file fallback (inputs 5 and 6). Inputs 7 and 8 are not sockets or memory, but they are read at start and one of them is never replaced by configuration.

### The translator: Flow has no translator process

- **No translator process exists in flow at 8f78c73.** There is no `flow-translator` binary and no `flow-translator.sock` or `flow-meta-translator.sock` anywhere in the flow repository or in Home's Flow units. The vision's socket list for Flow (`vision:nexus` 1, "A Nexus starts in its place") names them, and they are not built.
- **The `translator` crate is a library.** Flow takes only `translator::placement` and `translator::place_file` from it. The only translator process Home runs is Energy's (`modules/home/profiles/min/energy-nexus.nix`, `energy-translator.sock`), another Nexus.
- **Flow's text front end is its two CLIs**, `flow-nexus` and `flow-nexus-meta`, which speak signal straight to `flow.sock` and `flow-meta.sock`. They do not read the place file:

| # | Input | Where | Used for |
|---|---|---|---|
| a | `XDG_CONFIG_HOME`, else `HOME` | flow-ethos `place.rs:193-197`, `211-219` | where the CLI configuration lies |
| b | `$XDG_CONFIG_HOME/nexus/flow-nexus.datom`, `CliConfiguration.{ PlaceName }` | flow-ethos `place.rs:104-170` | the place name |
| c | `XDG_RUNTIME_DIR` | flow-ethos `place.rs:195,220` | the socket directory `$XDG_RUNTIME_DIR/nexus/<place>/`, taken from the standard variable and from nothing else |

The consequence: a place file whose Runtime is not `$XDG_RUNTIME_DIR/nexus/<place>` moves the daemon's sockets where the CLIs do not look. Today the two agree only because the default Runtime and the CLI's rule are the same string. The capsule keeps them together by writing both a place file and a `flow-nexus.datom` (capsule `flow-capsule.clj` lines 229-247 and 1358-1363) and by setting `XDG_RUNTIME_DIR` to its own runtime.

The Claude hook (`crates/flow/src/hook.rs:295`) reads `CLAUDE_CONFIG_DIR` and `HOME`, and is handed the ordinary socket in its typed configuration. It is no translator.

## What this means for wntk

The standing ruling is one startup file holding the sockets, the memory and the translator, found from the Place alone. Against the build:

1. **The translator is not in the build at all.** Flow has none, and the CLIs are not placed by the Place. If the translator means the CLI, it must take its socket from the place file, which makes `flow-nexus.datom` carry nothing the Place does not. If it means a real translator process, Flow does not have one yet, and the Place would name its sockets (Runtime joined to `flow-translator.sock` and `flow-meta-translator.sock`).
2. **The file's own address needs something besides the Place.** Any file has to be found from something: here the place name argument plus the standard configuration home. That may be what the ruling means by the Place alone. It is a question, not an assumption.
3. **The no-file default reads the environment** (inputs 5 and 6). To meet the condition literally, a missing place file refuses instead.
4. **Inputs 7 and 8 read the user's home and Claude's directory at start.** They are not the Nexus's sockets or memory. They are what a user-configurable value should be, and the Claude one has no configuration to replace it.

## Questions back to the design

1. Is the translator the CLI, or a process Flow does not have yet? If the CLI, should `flow-nexus` and `flow-nexus-meta` read the same place file as the daemon and drop `flow-nexus.datom` and `XDG_RUNTIME_DIR`?
2. Is the place file found from the place name and the standard configuration home (inputs 1 to 3) acceptable as "the Place alone"?
3. With no place file, should the daemon start at the defaults (inputs 5 and 6) or refuse?
4. Are inputs 7 and 8, the home and Claude's directory read at start, in scope? If so, a Claude home belongs to configuration received while running.

I stopped before any change because each answer changes what is built. If answers 1 and 3 are "the CLI reads the place file" and "refuse", the work is in translator and flow-ethos and is small.

## Part B, not started

- build-base main has moved past d58fa6f by four commits, to ab3b3d8 (`Reuse repeated normal dependencies in test builds`, `Register meta-signal-flow 81`, `Register the Orchestrate Signal 11 cohort`, `Align Orchestrate contract Datom graph`). The release line pins d58fa6f; a `pko0-90d453` branch is to be made from d58fa6f, as briefed.
- translator origin/main is still e7cd5bc, so the rebase onto main is nothing: `pko0-90d453` would be the pko0 commits as they stand.
- flow origin/main is now eabddc8d (0.56.2), past the 4282dda the pko0 flow branch was made from. The branch is to be made from release-521d44 eb55a9d4 as briefed, not main.
- The local build-base clone was shallow, with no history before 951c69b; I unshallowed it (`git fetch --unshallow`). Nothing else in any repository was changed.

## What Home's Flow units must change to start the daemon from the place file

`modules/home/profiles/min/flow-nexus-place.nix` (shared by every version; `flow-0550.nix` imports it) at the version that takes this Flow:

1. **Build Flow once.** Replace `inputs."flow-${slug}".lib.${system}.mkFlowPackage { defaultConfiguration = ...; }` (lines 125-148) with `inputs."flow-${slug}".packages.${system}.default`. The `nexus` attribute set stays; it feeds the configure unit (`nexusQuery`), not the build. The `runtimeDirectory` placeholder goes.
2. **Start with the place name, not the place datom.** `ExecStart = "${runtime}/bin/flow-nexus-daemon \"${place}\""` (line 429) becomes `"${runtime}/bin/flow-nexus-daemon ${text cfg.place}"`, and the `place` binding (line 261) is removed. The unit still sets no environment, so inputs 5 and 6 read the systemd user manager's own `XDG_RUNTIME_DIR` and `HOME`.
3. **Put the place file under the configuration home the daemon reads.** For the defaults no file is needed: `%t/nexus/<place>` and `%S/nexus/<place>` equal what the defaults resolve to. A place elsewhere gets a file from translator's `lib.<system>.mkPlaceFile`, linked at `~/.config/nexus/<place>/flow-nexus.signal`. The Runtime path holds the uid, so it is written at activation, not at build.
4. **The two configuration homes must agree.** The unit's daemon reads `~/.config/nexus/<place>/flow-nexus.signal` from the user's `XDG_CONFIG_HOME`, while the clients and the configure unit run with `XDG_CONFIG_HOME` set to `placeConfiguration` (lines 217-219 and 224-246), which holds only `nexus/flow-nexus.datom`. If the place file is linked under the user's home, the daemon finds it and the versioned clients do not need it; if the answer to question 1 is that the CLIs read the place file, `placeConfiguration` must hold the place file as well and `flow-nexus.datom` goes.
5. **Replay into every new memory.** The executable seeds nothing, so a new memory serves unconfigured until the configure unit runs. It does already: After= and Requires= the Nexus (lines 443-453), `Configure.Nexus` first. On a new memory it answers `Configured.Replaced` where the seeded Nexus answered `Unchanged`; `configure-flow-<slug>` already accepts any `Configured.*` (line 236).
6. **Choose the version and pin** the merged translator, build-base and flow revisions in Home's flake.

## Built (5k9t)

Branch `pko0-90d453` in each repo, all pushed; scratch logs under `/tmp/claude-1001/-home-li-primary/90d453b1-172e-5b51-9ba4-a3c3ee6f806f/scratchpad/pko0/`.

| Repo | Head | Gate | Log |
|---|---|---|---|
| translator (from e7cd5bc) | 6892a15 | green, exit 0 | gate-translator-6892a15.log |
| build-base (from d58fa6f, not main ab3b3d8) | 79188c7 | green, exit 0 | gate-build-base-79188c7.log |
| flow (8 commits over release-521d44 eb55a9d4) | 291b73e6 | green, exit 0; 20 check attributes built, 22 builds | gate-flow-291b73e-run2.log (earlier run with test output: gate-flow-291b73e.log) |
| CriomOS-home (Flow input pinned at 234bfe4d) | 8c0abbcd | Flow, configure, clients, place-configuration and service units built; activation package not yet built, see Open | home-build-8c0abbc-run2.log |

Flow test counts (gate-flow-291b73e.log): flow-nexus 927 unit (8 ignored) and 13, 3, 1 integration; flow 10, 15, 4, 4; flow-meta 5, 1; flow-place 2; flow-ethos 3, 4. None failed.

Behavior changed:
- The Nexus is started with its place name alone (`flow-nexus-daemon main`). It reads the place (Runtime, State) from `$XDG_CONFIG_HOME/nexus/<place>/flow-nexus.signal` (`$HOME/.config` when unset or empty) before any socket opens. No place file: it refuses, naming the file.
- `flow-nexus` and `flow-nexus-meta` read the place name from `~/.config/nexus/flow-nexus.datom`, then the Runtime from that place's place file. Their `XDG_RUNTIME_DIR` read is gone; a missing configuration or place file is refused naming it. Tests (default_socket.rs in flow and flow-meta) set a different runtime variable and still reach the place file's Runtime.
- The new crate `flow-place` holds the lookup, through translator's `FindsPlace`. The executable holds no configuration: a new memory starts unconfigured and the configure unit replays into it (`Configured.Replaced`). `mk-flow-package.nix` and the seeded `library.ethos` are removed.
- Home writes the place file at every activation, before units reload, with translator's `nexus-configure`; the versioned clients' configuration home links it beside `flow-nexus.datom`.

Open:
- Home's activation package is blocked on a source build of `electron-unwrapped-43.2.0` on prometheus (pid 835623, started about 12:50, still running), which the wispr-flow service needs. Main's Home needs the same derivation, so it is not caused by this change. The 15 remaining derivations are electron and its dependents. The activation script, which writes the place file, is evaluated but not built.
- Home's lock pins flow at 234bfe4d, not head 291b73e6; the later commits change tests only. Re-pin Home to the flow head, and to merged translator and build-base revisions, when the branches merge.
- Home is not rebased onto CriomOS main; the capsule test (`flow-capsule-test.clj`) is not run; nothing deployed or switched; Claude paths are out of scope.
