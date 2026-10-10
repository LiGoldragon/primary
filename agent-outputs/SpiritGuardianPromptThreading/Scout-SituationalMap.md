# Scout Situational Map — Spirit Daemon Configuration & Guardian Prompt Threading

## Task and Scope

Map the Spirit daemon's configuration-write mechanism, runtime config path, the
`signal-spirit` contract shape (`SpiritDaemonConfiguration` /
`SpiritGuardianAgentConfiguration`), the contract version, the deployed-vs-main
version state (0.18.1 vs 0.19.0), and any existing plumbing for a runtime
guardian prompt file path. Read-only scouting for a downstream implementer
considering whether to add a `guardian_prompt` field to the contract.

Read-only. Nothing was edited.

## Files and Commands Consulted

- `/home/li/primary/repos/spirit/src/bin/spirit-write-configuration.rs` (full)
- `/home/li/primary/repos/spirit/flake.nix` (full)
- `/home/li/primary/repos/spirit/src/config.rs` (config wrapper + `from_binary_path`)
- `/home/li/primary/repos/spirit/src/daemon.rs` (daemon hooks, `load_configuration`)
- `/home/li/primary/repos/spirit/src/bin/spirit-daemon.rs` (5-line entry)
- `/home/li/primary/repos/spirit/src/guardian.rs` (`AgentGuardianConfiguration`)
- `/home/li/primary/repos/spirit/src/guardian_prompt.rs` (prompt assembly via `include_str!`)
- `/home/li/primary/repos/spirit/src/guardian-prompts/*.md` (compile-time prompt prose)
- `/home/li/primary/repos/spirit/ARCHITECTURE.md` (guardian + config sections)
- `/home/li/primary/repos/spirit/README.md`, `manual.md`
- signal-spirit contract source (cargo git checkout for the locked rev):
  `/home/li/.cargo/git/checkouts/signal-spirit-44a4bfaa970650f7/5d0905a/`
  (`src/lib.rs`, `src/schema/signal.rs`, `schema/signal.schema`)
- `jj log` / `jj file show` / `jj status` in the spirit repo
- `Cargo.lock` / `Cargo.toml` in the spirit repo

## OBSERVED FACTS

### 1. Config-write mechanism (`spirit-write-configuration`)

The binary `spirit-write-configuration` takes a NOTA argument (inline NOTA or a
NOTA file via `triad_runtime::ComponentCommand`; a `SignalFile` argument is
explicitly rejected as unimplemented). It parses one
`ConfigurationWriterInput::ConfigurationWriteRequest`, builds a
`signal_spirit::SpiritDaemonConfiguration`, encodes it with `to_rkyv_bytes()`,
and `fs::write`s the rkyv bytes to `output_path`. It prints
`(ConfigurationWritten <path>)` as NOTA.

The writer's own NOTA-input record (`ConfigurationWriteRequest`, positional) is:

```
socket_path:                    ConfigurationWriterPath          (String)
meta_socket_path:               Option<ConfigurationWriterPath>
database_path:                  ConfigurationWriterPath
trace_socket_path:              Option<ConfigurationWriterPath>
authorization_mode:             AuthorizationMode                (Gating | Observing)
guardian_agent_configuration:   Option<ConfigurationWriterGuardianAgent>
output_path:                    ConfigurationWriterPath          (where the rkyv is written)
```

`ConfigurationWriterGuardianAgent` (positional):

```
agent_socket_path:      ConfigurationWriterPath   (String)
provider_name:          Option<ConfigurationWriterProviderName>   (Option String)
model_name:             Option<ConfigurationWriterModelName>      (Option String)
timeout_milliseconds:   ConfigurationWriterTimeoutMilliseconds    (u64)
maximum_output_tokens:  Option<ConfigurationWriterMaximumOutputTokens> (Option u64)
```

The builder path is `ConfigurationWriteRequest::configuration()` →
`SpiritDaemonConfiguration::new(socket, database)` then chained
`.with_meta_socket_path`, `.with_trace_socket_path`,
`.with_authorization_mode`, `.with_guardian_agent_configuration`. So YES, the
writer sets the full guardian agent configuration (socket / provider / model /
timeout / tokens) when the optional guardian block is present.

Inputs that feed it: a single NOTA argument only (inline or a file). NO env
vars, NO other CLI flags, NO file reads beyond the NOTA argument file.

README run snippet (`/home/li/primary/repos/spirit/README.md` lines 40-41):

```
spirit-write-configuration "(ConfigurationWriteRequest (/tmp/spirit.sock (Some /tmp/spirit-meta.sock) /tmp/spirit.sema None Gating None /tmp/spirit.config.rkyv))"
spirit-daemon /tmp/spirit.config.rkyv
```

(Here the 6th positional `None` is the absent guardian block; the 7th is the
output rkyv path.)

### 2. Runtime config-read path (`Configuration::from_binary_path`)

- `src/bin/spirit-daemon.rs` is 5 lines: `SpiritDaemon::run_to_exit_code()`.
- `spirit-daemon` takes exactly ONE argument: the path to the binary rkyv
  `SpiritDaemonConfiguration` (ARCHITECTURE.md §"The daemon" step 1; README
  line 34). The argv parsing lives in the schema-emitted `DaemonCommand`
  (`triad_runtime`); not hand-written in spirit.
- `src/daemon.rs:97-101`: `ComponentDaemon::load_configuration(path)` calls
  `Configuration::from_binary_path(path)`.
- `src/config.rs:107-116`: `from_binary_path` does `fs::read(path)` then
  `SpiritDaemonConfiguration::from_rkyv_bytes(bytes)` → `Configuration::from_raw`.
- The daemon does NOT parse NOTA at startup (binary-only build; flake check
  `nota-surface-is-opt-in` forbids `nota`/`NotaSource` in `config.rs`,
  `daemon.rs`, `spirit-daemon.rs`).
- `Configuration::from_raw` (src/config.rs:61-74) maps the guardian block to
  `crate::guardian::AgentGuardianConfiguration::from_contract` (only under the
  `agent-guardian` feature, which the daemon package is built with — see flake
  `daemonPackage` `--features agent-guardian`).

### 3. signal-spirit contract — version, structs, schema

LOCKED VERSION: `signal-spirit` **0.9.0**, git rev
`5d0905a7aa8c43951253b86193d76be67a89a945` (branch main).
(`Cargo.lock` lines 1495-1497; dep declared `branch = "main"` in
`Cargo.toml:167`.) Contract source confirmed at the cargo checkout
`.../signal-spirit-44a4bfaa970650f7/5d0905a/`, `Cargo.toml` version 0.9.0.

`SpiritDaemonConfiguration` (generated, `src/schema/signal.rs:1080-1087`):

```
socket_path:                   ConfigurationPath          (pub)            -- String newtype
meta_socket_path:              MetaSocketPath             (pub(crate))     -- Option<ConfigurationPath>
database_path:                 ConfigurationPath          (pub)            -- String newtype
trace_socket_path:             TraceSocketPath            (pub(crate))     -- Option<ConfigurationPath>
authorization_mode:            AuthorizationMode          (pub)            -- enum [Gating Observing]
guardian_agent_configuration:  GuardianAgentConfiguration (pub(crate))     -- Option<SpiritGuardianAgentConfiguration>
```

`SpiritGuardianAgentConfiguration` (generated, `src/schema/signal.rs:1022-1028`):

```
agent_socket_path:      ConfigurationPath               (pub)        -- String newtype
provider_name:          ProviderName                    (pub(crate)) -- Option<SpiritGuardianProviderName> (String)
model_name:             ModelName                       (pub(crate)) -- Option<SpiritGuardianModelName>    (String)
timeout_milliseconds:   SpiritGuardianTimeoutMilliseconds (pub)      -- Integer (u64)
maximum_output_tokens:  MaximumOutputTokens             (pub(crate)) -- Option<SpiritGuardianMaximumOutputTokens> (Integer/u64)
```

Primitive newtypes (`src/schema/signal.rs:641-674`,
`schema/signal.schema:116-120`):

```
ConfigurationPath                  String
SpiritGuardianProviderName         String
SpiritGuardianModelName            String
SpiritGuardianTimeoutMilliseconds  Integer
SpiritGuardianMaximumOutputTokens  Integer
```

NOTA schema source (`schema/signal.schema:153-168`) — the authoritative source
of truth; the Rust files under `src/schema/` are generated from it by
schema-rust:

```
  SpiritGuardianAgentConfiguration {
    agent_socket_path.ConfigurationPath
    ProviderName.(Optional SpiritGuardianProviderName)
    ModelName.(Optional SpiritGuardianModelName)
    timeout_milliseconds.SpiritGuardianTimeoutMilliseconds
    MaximumOutputTokens.(Optional SpiritGuardianMaximumOutputTokens)
  }
  AuthorizationMode [Gating Observing]
  SpiritDaemonConfiguration {
    socket_path.ConfigurationPath
    MetaSocketPath.(Optional ConfigurationPath)
    database_path.ConfigurationPath
    TraceSocketPath.(Optional ConfigurationPath)
    AuthorizationMode
    GuardianAgentConfiguration.(Optional SpiritGuardianAgentConfiguration)
  }
```

Schema-record convention (observed in this `.schema`): a named field is
`lower_snake.TypeName` (e.g. `agent_socket_path.ConfigurationPath`,
`timeout_milliseconds.SpiritGuardianTimeoutMilliseconds`); a field whose name is
just the type uses the bare `PascalCase` type name, optionally wrapped
`(Optional T)` (e.g. `ProviderName.(Optional SpiritGuardianProviderName)`,
`AuthorizationMode`). Optional wrapper is `(Optional T)`. Primitive newtypes are
declared `Name String` / `Name Integer`.

Builder + archive API (`src/lib.rs`):
- `SpiritDaemonConfiguration::new(socket, database)` defaults meta=None,
  trace=None, authorization=Gating, guardian=None.
- `.with_meta_socket_path / .with_trace_socket_path / .with_authorization_mode /
  .with_guardian_agent_configuration` builders (lines 132-154).
- `SpiritGuardianAgentConfiguration::new(agent_socket_path, provider_name,
  model_name, timeout_milliseconds, maximum_output_tokens)` (lines 73-88) —
  takes `Option<...>` for provider/model/tokens.
- `from_rkyv_bytes` / `to_rkyv_bytes` via `rkyv::rancor::Error` (lines 186-195);
  error type `SpiritDaemonConfigurationArchiveError { Encode, Decode }`.

There is NO `guardian_prompt` / prompt field anywhere in the contract
(`rg -i 'guardian_prompt|prompt'` over the checkout's `src/` and `schema/`
returns nothing).

### 4. Guardian prompt is COMPILE-TIME ONLY — no runtime prompt path plumbed

- The guardian prompt prose lives in `src/guardian-prompts/*.md`
  (`role.md`, `record-shape.md`, `justification-shape.md`, `burden-ladder.md`,
  `checklist.md`, `few-shot.md`, `referent.md`).
- `src/guardian_prompt.rs:395-412` embeds each as a `const` via `include_str!`.
  `GuardianPromptBuilder` (constructed in `src/guardian.rs:255-256` with only
  provider_name / model_name / maximum_output_tokens) ASSEMBLES these constants
  and splices in two enum-rendered sections (the rejection-reason catalogue and
  the verdict grammar). `referent.md` is a template with `{accept}`/`{reject}`
  placeholders filled by `.replace`.
- ARCHITECTURE.md §"Guardian admission and its prompts" (lines 451-460):
  "The guardian prompt prose lives in standalone files, never in the Rust… 
  embedded at compile time with `include_str!` so the daemon stays a single
  self-contained binary." A regression test
  (`assembled_system_prompt_includes_every_file_section`) guards completeness.
- The flake (`flake.nix:199-205`, `promptFilter`) deliberately pulls
  `src/guardian-prompts/` into the Nix build source because the prose is
  `include_str!`-ed into the daemon binary.
- `AgentGuardianConfiguration` (src/guardian.rs:36-42) holds socket_path,
  provider_name, model_name, timeout, maximum_output_tokens — NO prompt field.

CONCLUSION (observed): there is currently NO runtime-supplied guardian prompt
file path anywhere — not in the contract, not in the writer, not in the daemon
config, not in `AgentGuardianConfiguration`. The prompt is baked into the binary
at compile time. Adding a runtime prompt path would be a genuinely new surface.

### 5. Version state in the spirit repo — 0.19.0 is committed on `main`

`jj` facts (spirit repo):
- `Cargo.toml` on the `main` bookmark: `version = "0.19.0"`
  (`jj file show -r main Cargo.toml`).
- `main` bookmark = change `yzsxyqqt` / commit `43d6a069`
  ("migrate StoreRegistration call sites to typed record … relock
  meta-signal-mirror 0.2.0 + mirror 0.2.0").
- The 0.19.0 version bump landed in ancestor change `sqvuykswxnun`
  ("spirit: 0.19.0 — relock meta-signal-spirit + chain contracts …"), which is
  in `::main` history. So **0.19.0 is committed on main, not working-copy-only.**
- 0.18.1 is an OLDER committed ancestor on the same line
  (change `wtlryqplrxzm`, "spirit: 0.18.1 — recognize dbe53794 (0.16.0) records
  family as schema-10 legacy-family migration source"), already superseded by
  0.18.x → 0.19.0 on main.
- The working copy `@` is on the **`criome-authorization-push`** bookmark
  (change `tlxyvxrq` / `52f97d07`), NOT on `main`. Its `Cargo.toml` is also
  `0.19.0`. `@-` parent is also 0.19.0.
- The repo's initial git-status snapshot said branch "HEAD" / main; the live
  `jj` working copy is actually on `criome-authorization-push` with several
  modified files (`jj status`: Cargo.lock, Cargo.toml, flake.lock, flake.nix,
  src/criome_gate.rs, tests/criome_gate_1of1.rs, tests/runtime_triad.rs).
- Build artifacts present: `result*` symlinks point to
  `…-spirit-test-0.19.0` / `…-spirit-build-0.19.0` (Jun 29 builds).

So the in-repo source (both main and the active feature bookmark) is at
**0.19.0**. The task's claim that the LIVE/DEPLOYED version is **0.18.1** is a
statement about a SEPARATE deployment pin, not about repo main (see Deployment
section / Unknowns).

## INTERPRETATIONS

- Adding `guardian_prompt` to the contract is the natural extension point IF the
  intent is to make the guardian prompt runtime-configurable. The cleanest
  contract shape, by symmetry with the existing optional fields, would be an
  optional newtype on `SpiritGuardianAgentConfiguration` (where socket / model /
  tokens already live), e.g. a `GuardianPrompt.(Optional SpiritGuardianPrompt)`
  field with `SpiritGuardianPrompt String`. Whether it should be the prompt TEXT
  or a prompt FILE PATH is a design choice the contract does not currently
  constrain; a path is consistent with the existing `ConfigurationPath` style
  (paths-in, daemon reads the file), but it breaks the "daemon stays a single
  self-contained binary, prompt baked at compile time" property asserted in
  ARCHITECTURE.md lines 451-456 — so this is a doctrine tension a reviewer/psyche
  should weigh, not a free win.
- The contract change would ripple: `signal-spirit` schema (`signal.schema`) +
  regenerated `src/schema/signal.rs` + `lib.rs` builder/accessor; then spirit's
  `spirit-write-configuration.rs` (`ConfigurationWriterGuardianAgent` +
  `into_guardian_agent_configuration`), `config.rs`/`guardian.rs`
  (`AgentGuardianConfiguration` + `from_contract`), and the
  `GuardianPromptBuilder` assembly to consume a runtime override. signal-spirit
  is a git-dep on branch main (locked rev 5d0905a / 0.9.0); a contract bump means
  landing signal-spirit main first, then relocking spirit (the flake vendors
  signal-spirit by path and rewrites its Cargo.toml — see flake.nix:395-402).

## LIKELY RELEVANT FILES (for the implementer)

Contract side (`LiGoldragon/signal-spirit`, locked rev 5d0905a, v0.9.0):
- `schema/signal.schema` (source of truth, lines 116-168)
- `src/schema/signal.rs` (generated; 1022-1028, 1080-1087, 641-674)
- `src/lib.rs` (builders/accessors; 73-196)

Spirit daemon side (`/home/li/primary/repos/spirit`):
- `src/bin/spirit-write-configuration.rs` (writer; guardian block at 62-69,
  159-162, 181-194)
- `src/config.rs` (61-74, 100-116)
- `src/guardian.rs` (36-112, 255-256)
- `src/guardian_prompt.rs` (395-412 include_str consts; `GuardianPromptBuilder`)
- `src/guardian-prompts/*.md` (current compile-time prose)
- `flake.nix` (promptFilter 199-205; signal-spirit vendor patch 395-402,
  patch table 510-514; daemon `--features agent-guardian` 720-726)
- `ARCHITECTURE.md` (435-484 guardian/prompts; 150-184 startup/config)

## UNKNOWNS / BLOCKERS

- **Live deployment + the "0.18.1 deployed" claim**: the spirit repo's own
  `nix/` directory is EMPTY and `flake.nix` defines NO NixOS module / systemd
  service for `spirit-daemon`. So the deployment (host config, the actual runtime
  `*.config.rkyv` path, the guardian socket/provider/model/tokens chosen at
  deploy time, and the deployed spirit rev/version) lives elsewhere — a sibling
  repo `/home/li/primary/repos/spirit-guardian-config/` references
  `spirit-daemon` / `spirit-write-configuration` / `SpiritDaemonConfiguration`,
  and the true host deployment may be under `private-repos/` (NOT inspected per
  hard boundary). A subagent (Explore) was dispatched to resolve this; its
  findings are folded in below if returned. No host `flake.lock` under
  `repos/` pins `LiGoldragon/spirit` directly (checked).
- Whether `spirit-guardian-config` is the deployment surface or a separate
  component was not fully read by this scout.
- Not verified: that the deployed binary actually corresponds to 0.18.1 (would
  require reading the deployment pin, pending the subagent / private scope).

## DEPLOYMENT (resolved)

Deployment is home-manager, not a NixOS module. Source of truth:
`/home/li/primary/repos/CriomOS-home/modules/home/profiles/min/spirit.nix`.

Observed facts:
- `spiritPackage = inputs.spirit.packages.${system}.default;` (line 20). The
  deployed package is the REAL `LiGoldragon/spirit` repo — NOT
  `spirit-guardian-config`. (The subagent cited `spirit-guardian-config` for the
  prompt files; that repo is a sibling and is NOT the deployed source. The live
  daemon's guardian prompts are the `src/guardian-prompts/*.md` baked into the
  `spirit` package at build time, same `include_str!` mechanism described in §4.)
- systemd USER service `spirit-daemon` (lines 173-206):
  `ExecStart = "${spiritPackage}/bin/spirit-daemon ${daemonConfiguration}/${configurationPath}"`
  (line 200). `After`/`Wants` = `agent-daemon.service`. `Restart = on-failure`.
- Runtime config rkyv path: `${daemonConfiguration}/spirit.config.rkyv`
  (`configurationPath = "spirit.config.rkyv"`, line 35), generated at build time
  by a `pkgs.runCommand` derivation `daemonConfiguration` (lines 63-71) that
  invokes `${spiritPackage}/bin/spirit-write-configuration` with the inline NOTA
  `(ConfigurationWriteRequest (...))` (lines 67-68). So deploy uses exactly the
  writer mechanism in §1.
- Guardian agent block set at deploy time (line 53):
  `guardianAgentConfiguration = "(Some (${agentSocketPath} (Some ${providerName}) (Some ${guardianModel}) 180000 None))"`
  → agent socket `~/.local/state/agent/agent.sock`, provider `deepseek`,
  guardian model `deepseek-v4-pro`, timeout 180000 ms (3 min),
  maximum_output_tokens `None`. (provider token via gopass at the agent daemon,
  not in the spirit config.) `authorizationMode` is also threaded.
- **Deployed spirit version: 0.18.1.** Pinned in
  `/home/li/primary/repos/CriomOS-home/flake.lock` — the `spirit` input rev is
  `f64bc8ad74cf859d6335a43c1f11b67f974b3c8f`; the subagent verified
  `Cargo.toml` at that rev is `version = "0.18.1"`.

So the 0.18.1 vs 0.19.0 split is precisely: **0.18.1 is the DEPLOYED pin**
(CriomOS-home flake.lock `spirit` rev f64bc8ad), while the spirit repo's own
`main` (and the active `criome-authorization-push` working copy) is already at
**0.19.0**, committed. Deploying the prompt-threading change would require
landing it on spirit main and bumping the CriomOS-home `spirit` input.

- **No runtime/external guardian prompt FILE PATH is threaded at deploy time.**
  Confirmed: prompts are compile-time `include_str!` in the deployed package.
  The deploy config carries no prompt field (the contract has none — §3, §4).
