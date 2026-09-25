# meta-signal-flow 6.0.0 receipt

Opus subflow of Psyche High 38de5b, 2026-09-25. Follows `i1-g10-flow.md` ("What meta Configure lacks") and G10 of `reports/audit-flow.md`.

## Landed

- LiGoldragon/meta-signal-flow main a1316a0 (5.0.0) to **4748cfa** (6.0.0). `git ls-remote origin main` = 4748cfa854131cc4feb592167aa89516840a59e5.
  - 91f32c0 made the Configuration change.
  - 4748cfa repinned signal-flow, as the coordinator asked mid-task: the dependency and the build-dependency both went from f881ab3 (3.0.0) to 5ca97ce (4.0.0). This lets the Nexus consume both crates at one signal-flow revision.
- The flow repo and signal-flow were not touched.
- Version: 5.0.0 to 6.0.0, a major bump. `Configuration` gained fields, so the rkyv archive of `Configure` and `Configured` changed.

## New ethos lines

These replace the single former line `Configuration.{ OrdinarySocketPath MetaSocketPath }` in the types section of `ethos/signal.ethos`:

    SourceRoot.String
    ClientPath.String
    Home.String
    ControlSocketPath.String
    CodexEndpoint.{ ClientPath Home ControlSocketPath Vector<ModelName> }
    StableCodex.CodexEndpoint
    NextCodex.CodexEndpoint
    Configuration.{ OrdinarySocketPath MetaSocketPath SourceRoot StableCodex NextCodex }

`ModelName` is the `signal_flow:ModelName` import that was already in the file. `ConfigureRequest.Configuration` and `Configured.{ Configuration Activation }` pick the new fields up with no further change.

Generated Rust (ethos-zero 4bf73ca, the build.rs pin; regenerated through its library, and `build.rs` asserts it is fresh):

    pub struct CodexEndpoint { client_path: ClientPath, home: Home, control_socket_path: ControlSocketPath, model_name_vector: Vec<signal_flow::ModelName> }
    pub type StableCodex = CodexEndpoint;  pub type NextCodex = CodexEndpoint;
    pub struct Configuration { ordinary_socket_path, meta_socket_path, source_root, stable_codex, next_codex }

Naming choices:

- The endpoint struct is written once, and the stable and next roles are aliases of it. The fields therefore read `stable_codex` and `next_codex`, as in flow-nexus's `RuntimeConfiguration`.
- The Nexus's `socket` field is `ControlSocketPath` here. The module already has `OrdinarySocketPath` and `MetaSocketPath`, and a bare `Socket` would be ambiguous among them. The path is the Codex app-server control socket.
- `model_names` is `model_name_vector`.

## Concrete datom (contract test)

    Configure.{ /run/user/1001/flow/flow.sock /run/user/1001/flow/flow-meta.sock /home/li/primary { /etc/profiles/per-user/li/bin/codex-stable-flow-client /home/li/.codex /home/li/.codex/app-server-control/app-server-control.sock [ gpt-5.6-terra gpt-5.6-sol gpt-5.6-luna ] } { /etc/profiles/per-user/li/bin/codex-next-flow-client /home/li/.codex-next /home/li/.codex-next/app-server-control/app-server-control.sock [ gpt-6-sol gpt-6-luna gpt-6-astra ] } }

## Tests

- `cargo test --features datom`: 5 passed, at 91f32c0 and again at 4748cfa after the repin. Before: 3.
  - `privileged_requests_have_concrete_datoms` now uses the Configure datom above.
  - New: `configured_carries_source_root_and_both_codex_endpoints`. It is a datom and rkyv round trip of `Configured`, with field-level assertions and an empty model vector.
  - New: `configure_missing_an_endpoint_is_refused_by_the_reader`. This is the negative case: a Configure datom without its endpoints is refused.
- `cargo test` without the feature: 0 tests, as before, because every contract test is gated on `datom`.
- `cargo clippy --all-targets --features datom -D warnings`: clean. `rustfmt` has been applied to the tests.
- Nix was not run.

## What the Nexus must do to consume it (later task, flow repo)

1. Repin `meta-signal-flow` to 4748cfa (6.0.0), together with signal-flow 5ca97ce, in the flow workspace. The `flow-meta` CLI picks the new shape up automatically, because it only textualizes.
2. `lib.rs` meta dispatch of `Query::Configure`:
   - Persist the socket paths as today.
   - Also persist `RuntimeConfiguration { source_root, stable_codex, next_codex }` through `configure_runtime`, mapping `control_socket_path` to `socket` and `model_name_vector` to `model_names`.
   - Answer `Configured` with the whole stored Configuration.
3. Unify types. Either replace `store::RuntimeConfiguration` and `CodexEndpointConfiguration` with the contract's `Configuration` and `CodexEndpoint`, or keep them and add one `From` pair. One stored record for the whole Configuration would remove the second table.
4. `DefaultConfiguration::configuration()` must fill the new fields from `runtime_configuration()`, so that the default start and `Configured` replies carry them.
5. Once meta Configure carries the fields, retire the `DeploymentOverrides` exception (the `FLOW_SOURCE_ROOT` and `FLOW_CODEX_*` environment variables). The Nix unit then either configures over the meta socket after start (`flow-meta 'Configure.{ … }'`) or keeps the overrides until that is wired. This is a ruling for the flow owner.
6. Fix the tests that build a `Configuration`. Their 2-field literals will not compile. These include `tests/default_start.rs`, which sends a meta Configure.
7. Decide whether a change of source root or endpoint takes effect live or still answers `Activation::NexusRestartRequired`. The Codex adapter reads the runtime configuration at construction.

## Lock

Orchestrate locks 6370 and 6379 on the scratch clone path, both released.
