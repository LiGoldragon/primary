# Flow traits first

Subflow of 3ec648, 2026-10-02. Repository `flow` (/git/github.com/LiGoldragon/flow),
from remote main f89df0a5 (0.17.4) to main 0e3ce038 (0.18.0), six commits,
pushed. Nothing deployed; no running flow-nexus was touched (every test run
had `/run/user/1001` masked by a bwrap tmpfs).

## What changed

**Trait laws.** `checks/no-free-functions.sh`, `checks/no-inherent-methods.sh`
and `checks/production-rust.sh` are copied from lojix (orchestrate main has no
such checks; lojix and ethos-zero carry them) and wired into `flake.nix` as
`checks.no-free-functions` and `checks.no-inherent-methods` over the four
crates' `src/`, excluding the cfg(test)-only files `flow-nexus/src/tests/` and
`fixture_executable.rs`. The free-function grep also catches
`const`/`async`/`unsafe fn`. Both pass locally on main.

Before: 15 production free functions, 45 inherent impl blocks (~126 methods),
8 zero-sized namespaces. After: `fn main()` only, no inherent impl, no
zero-sized type with behaviour (`UnreadLaunchAttempt` stays: a row type
with no behaviour).

- Zero-sized namespaces moved to data-bearing owners: `Frame` became
  `CarriesSignalFrames` on `UnixStream`; `LaunchReceipt` became
  `AsksForLaunchReceipt` on `HarnessKind`; `ClaudePasteThreshold` became
  `FitsClaudePaste` on `str`; `ClaudeCommandStack` became
  `StacksClaudeCommands` on skill slices; `ModelDisplay` became `NamesModel`
  on `str`; `CommandLine` became `ReadsCommandLine` on `HarnessProfile`;
  `BriefContinuation` became a constant of `ContinuesIntoBrief`.
- Free functions moved to owners: the MetaBindExisting checks went to a new
  `binding` module (`ChecksProcessIdentity`, `ChecksFlowContainer`,
  `ChecksFlowBinding`, `RefusesBinding`). The Claude readiness projection
  became `ClaudeDaemon` with `ProjectsClaudeReadiness`; its jobs and roster
  paths now come from Claude's home, where they were hard-coded under
  `/home/li/.claude`. `version_answer` became `AnswersVersion` on `[String]`.
- Every inherent impl became a named trait. HerdrCli's 22 associated
  functions that took no HerdrCli moved onto the type of their first
  argument (`ComposedLaunch`, `Path`, `File`, `str`, `PromptDeliveryIntent`,
  `serde_json::Value`, `NativeSkillSelection`, `HarnessKind`, `[&str]`).

**One home for defaults.** The new crate `flow-defaults` holds the anchors
(`HOME`, `XDG_RUNTIME_DIR`, with `/run/user/<uid>` as the fallback) and every
default path: the store, `$XDG_RUNTIME_DIR/flow/flow.sock`,
`flow-meta.sock`, the source root and the Codex endpoints. The Nexus seeds
from it. The `flow` and `flow-meta` clients default to its sockets; before,
they defaulted to `/run/user/1001/flow/`. `flow-meta register-codex` no
longer defaults to `/home/li/.codex`.

**Configuration only over meta.** `DeploymentOverrides` is gone:
`FLOW_SOURCE_ROOT` and `FLOW_CODEX_*` are no longer read, and `Configure` is
the only way in. `CODEX_HOME` was also dropped; it only fed placeholder
endpoints that the configured ones replace.

**Version.** 0.17.4 to 0.18.0 (Cargo.toml, flake.nix), with an UPGRADES.md
entry. There is no wire or storage change. The deployment changes: a fresh
next-slot store (`HOME=~/.local/state/flow-next`) now seeds
`~/.local/state/flow-next/primary` and needs a `Configure`. Stores that
already adopted the env values keep them.

## Tests

The 177 tests that existed before all pass, except one that was removed:
`deployment_overrides_replace_stored_runtime_values_only_when_valid` tested
the override feature, which is gone. Four tests were added, so the count is
now 180. Three of the new tests were seen failing first, with the live
socket masked:

- `the_client_reaches_the_default_ordinary_socket_under_the_runtime_directory`
  (flow) failed with `No such file or directory` against `/run/user/1001`.
- `the_meta_client_reaches_the_default_meta_socket_under_the_runtime_directory`
  (flow-meta) failed the same way.
- `a_flow_variable_in_the_environment_does_not_reach_the_configuration`
  (flow-nexus, a spawned Nexus started with `FLOW_SOURCE_ROOT`) failed with
  left `/srv/elsewhere`, right `<home>/primary`.

The fourth, a `flow-defaults` unit test of the layout, was not seen failing.
Each of the three is also an exact Nix check. `cargo clippy --workspace
--all-targets --all-features -D warnings` is clean.

`nix flake check` on 0e3ce038 (detached user unit, 45-minute limit):
RESULT_PENDING.

## Not settled (returned)

- `CLAUDE_CONFIG_DIR` and `CLAUDE_ENTERPRISE_SKILLS_DIR` are still read in
  `HerdrCli::default`. meta-signal-flow's `Configuration` has no field for
  Claude's home or its skill catalogs, so no `Configure` can carry them, and
  no test needs them. They are named in flow's `NON_IDEAL_AGENTS.md` (in the
  repository, as orchestrate keeps its own) with the contract fix.
- `FLOW_SOCKET` and `FLOW_META_SOCKET` are kept. They configure nothing in
  the Nexus: they choose which Nexus a client reaches, as orchestrate's
  `ORCHESTRATE_SOCKET` does. CriomOS-home's next-slot wrappers (`flow-next`,
  `flow-next-meta`) select the next Nexus with them, and a socket moved by
  `Configure` can only be reached this way. Whether to replace them with an
  `XDG_RUNTIME_DIR` anchor in the wrappers is a design question; it is named
  in `NON_IDEAL_AGENTS.md`.
- CriomOS-home `modules/home/profiles/min/flow.nix` and
  `flow-message-next.nix` still set `FLOW_SOURCE_ROOT` and `FLOW_CODEX_*`.
  From 0.18.0 these are inert, and the deployment should send `Configure`
  instead. Not changed here (out of scope; no deploy).
- `lib.rs` (about 3.5k lines), `store.rs`, `herdr/launch.rs` and `codex.rs`
  are far past the few-hundred-line piece size. The trait names were chosen
  per block, not designed as one ontology before any body was written.

## Sources

- Brief from main flow 3ec648; skills vision-nexus, knowledge-flow, versioning, testing, nix-workflow, file-editing.
- lojix `flake.nix` and `checks/*.sh` (/git/github.com/LiGoldragon/lojix): the shape copied.
- orchestrate main d80a617f `crates/orchestrate{,-meta}/src/main.rs`, `crates/orchestrate-nexus/src/defaults.rs`: client socket variables and XDG defaults.
- CriomOS-home `lib/stable-next-service.nix`, `modules/home/profiles/min/flow-message-next.nix`: next-slot anchors and wrappers.
- flow commits 56b6940b, 4387e2ce, ef823615, 78db7dc9, 14325e38, 0e3ce038.
