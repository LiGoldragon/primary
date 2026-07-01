# Testing Strategy

I have enough to build the map. My earlier "thin" flags for `domain-criome`/`repository-ledger` were wrong — both single files are full daemon-spawn socket tests. Here is the situational map.

# Integration/E2E Testing Situational Map — LiGoldragon micro-component daemon federation

Scope: read-only inspection of `/git/github.com/LiGoldragon/*` on 2026-07-01. Skills `testing` + `nix-usage` loaded. Every claim tagged FACT (backed by a path/command) or INFERENCE.

## 0. Substrate the tests sit on (context)

- FACT: `triad-runtime` (`/git/github.com/LiGoldragon/triad-runtime`) is the shared daemon shell every daemon depends on (22 `Cargo.toml` deps found). It exports the wire codec `LengthPrefixedCodec` + `FrameBody` (`src/frame.rs`), the daemon loops (`src/daemon.rs`, `src/async_runtime.rs`), TCP ingress (`src/tcp.rs`), and peer-identity types `ConnectionContext`/`PeerIdentity`/`UnixCredentials` (`src/process.rs`). Wire is length-prefixed (4-byte BE) binary signal frames carrying rkyv; `spirit/tests/socket_negative.rs` proves the transport rejects raw-NOTA and garbage bodies.
- FACT: `triad-runtime` exports **no test harness** — `src/lib.rs` `pub use` list has codec/daemon/runtime primitives only. There is no shared crate for "spawn a daemon + drive its socket + assert." Each repo hand-rolls its own fixture.
- FACT: contracts are split per component into `signal-<name>` (working wire) and `meta-signal-<name>` (owner/meta wire) crates; ~30 of each exist, almost all carrying `round_trip.rs` (+ `dependency_boundary.rs`, `channel.rs`).

## 1. Per-component test-coverage snapshot

Legend: REAL = spawns/composes a real daemon over a real socket and asserts replies/durable state; GOOD = real daemon-spawn test but narrower; WIRE = contract round-trip/boundary only; THIN = one shallow surface.

Daemon repos (each has a `tests/` dir; counts are `Command::new` spawn sites in tests):

| Component | Grade | Evidence (path) |
|---|---|---|
| `spirit` | REAL (deepest) | `spirit/tests/` — `process_boundary.rs` (52KB), `runtime_triad.rs` (124KB), `end_to_end_offline_full_chain.rs`, `socket_negative.rs`, `guardian_live_scenarios.rs`; 20 spawn sites |
| `router` | REAL + cross-daemon | `router/tests/` — `process_boundary.rs`, `criome_forward_lands_in_mirror.rs`, `end_to_end_remote_forward.rs`, `criome_forward_attestation.rs`, `smoke.rs`, `actor_runtime_truth.rs` |
| `lojix` | REAL | `lojix/tests/` — `actor_native_runtime.rs`, `deploy_job_survival.rs`, `durable_resume.rs`, `build_smoke.rs`, `test_op.rs`; 15 spawn sites |
| `terminal-cell` | REAL | `terminal-cell/tests/` — `daemon_witness.rs`, `production_witnesses.rs`, `session_witnesses.rs`; 13 spawn sites |
| `harness` | REAL + multi-process e2e | `harness/tests/daemon.rs`, `component_cli.rs`, **`message_router_harness_e2e.rs`** (spawns 4 processes) |
| `persona` | REAL | `persona/tests/daemon.rs`, `direct_process.rs`, `supervisor.rs`, `manager.rs` + `tests/support/mod.rs` + `persona-component-fixture` bin |
| `mirror` | REAL | `mirror/tests/end_to_end_arc.rs`, `daemon_logic.rs`, `landed_body_readback.rs`, `append_addressing_refusal.rs` |
| `criome` | REAL | `criome/tests/daemon_skeleton.rs`, `distinct_node_identities.rs`, `intercept_policy.rs` + 3 `criome-*-witness-test` bins (`criome/Cargo.toml`) |
| `terminal` | GOOD | `terminal/tests/component_cli.rs`, `terminal_supervisor.rs`, `terminal_registry.rs` |
| `orchestrate` | GOOD | `orchestrate/tests/daemon_cli.rs`, `worktree.rs`, `ledger.rs`, `handover.rs` |
| `mind` | GOOD | `mind/tests/daemon_wire.rs`, `actor_topology.rs`, `orchestrate_caller.rs` |
| `introspect` | GOOD | `introspect/tests/daemon.rs`, `actor_runtime_truth.rs`, `component_trace.rs` |
| `system` | GOOD | `system/tests/daemon.rs`, `component_cli.rs`, `smoke.rs` |
| `message` | GOOD | `message/tests/process_boundary.rs`, `forward_to_router.rs` |
| `mentci` | GOOD | `mentci/tests/criome_bridge.rs`, `client.rs`, `harness_liveness.rs`, `state.rs` |
| `listener` | GOOD | `listener/tests/runtime.rs`, `capture.rs`, `configuration.rs` |
| `cloud` | GOOD | `cloud/tests/runtime.rs`, `schema_daemon.rs`, `digitalocean_live.rs` |
| `upgrade` | GOOD | `upgrade/tests/binaries.rs`, `runtime.rs`, `handover_driver.rs` |
| `domain-criome` | GOOD | `domain-criome/tests/runtime.rs` — single file but real spawn+socket |
| `repository-ledger` | GOOD | `repository-ledger/tests/store.rs` — single file, real spawn+`UnixStream` |
| `sema-engine` | REAL (storage lib) | 14 files (`engine.rs`, `subscriptions.rs`, `tamper.rs`, `outbox.rs`…) — deep, but it is the store engine, not a socket daemon |
| `agent` | THIN (INFERENCE) | `agent/tests/configuration_writer.rs`, `fixture_round_trip.rs` — no obvious full daemon socket loop; the guardian's live behavior is exercised indirectly via `spirit/tests/guardian_live_scenarios.rs` |

- FACT: **No daemon repo has zero tests.** Every `triad-runtime` consumer carries at least one real daemon-spawn test.
- INFERENCE: coverage is "real per-component" but **overwhelmingly single-component** — a daemon is tested against hand-built fake peers/fixtures, not against its real neighbors, with the exceptions in §2.
- Contract crates: WIRE coverage is broad and uniform (`round_trip.rs` almost everywhere) — the rkyv/signal-frame encode/decode contract is well-witnessed; `signal-spirit`, `signal-frame`, `signal-sema`, `signal-terminal` go further (`dependency_boundary.rs`, `command_line.rs`, `generated_contract.rs`).

## 2. Existing multi-component test infrastructure (inventory)

There are **three distinct altitudes** already in the tree, and they are the conventions to build on:

### Altitude A — in-process library composition (hermetic, pure Nix check) — the strongest cheap integration
- FACT: `/git/github.com/LiGoldragon/router/tests/criome_forward_lands_in_mirror.rs` composes THREE real components in one test process: a real `criome::daemon::CriomeDaemon` on a real `criome.sock` with a `.sema` store (spawned in `thread::spawn`), a real `mirror::Engine` over a versioned `sema-engine` store behind a hand-rolled `UnixListener` serving loop, and a real `router::RouterRuntime::start_networked` with loopback TCP ingress. It drives real BLS attestation + length-prefixed signal frames and asserts the mirror's **durable head** advanced (`ObserveHeads`), not just the router's reply.
- FACT: peers are pulled as **git dev-dependencies** in `router/Cargo.toml` (`[dev-dependencies] criome = {git..., branch="criome-authorization-push"}`, `mirror = {git..., branch="main"}`, `signal-mirror`, `signal-criome`).
- FACT: these are wired as **pure `craneLib.cargoTest` flake checks** (no VM/kvm): `router/flake.nix` exposes `checks.router-criome-forward-lands-in-mirror`, `checks.router-criome-forward-lands-real-body-in-mirror`, `checks.router-accepts-only-real-criome-attestation`, `checks.router-refuses-forward-without-criome-credential`, each pinned to a single `--test … -- --exact` selector.
- FACT: `spirit/tests/runtime_triad.rs` (124KB) + `end_to_end_offline_full_chain.rs` do the same in-process full-triad composition for Spirit's Signal/Nexus/SEMA stack, with named spirit checks in `spirit/flake.nix` (`spirit-observe-head-object-rehashes-to-head`, `test-configuration-writer-process-boundary`, `operator-271-closed-claims`, etc.).

### Altitude B — multi-process binary spawn (present but not Nix-gated; skips)
- FACT: `/git/github.com/LiGoldragon/harness/tests/message_router_harness_e2e.rs` spawns **four real OS processes**: `harness-daemon` (via `CARGO_BIN_EXE_harness-daemon`), plus `message-daemon`, `message` CLI, and `router-daemon` built from **sibling repos** (`CargoBinary::build(repositories.router(), "router-daemon")`) or from `MESSAGE_DAEMON_BINARY`/`ROUTER_DAEMON_BINARY`/`MESSAGE_CLI_BINARY` env vars. It round-trips a message agent-a → harness → router → agent-b terminal.
- FACT: `MessageRouterHarnessE2e::new()` returns `Option` and the test **silently skips** ("skipping message/router/harness e2e; set … or provide sibling repositories") when neither env binaries nor `MESSAGE_REPOSITORY`/`ROUTER_REPOSITORY` are present.
- FACT: it is **NOT** wired as a check in `harness/flake.nix` — the checks list there is all single-target `cargoTest "daemon"/"actor_runtime_truth"/"component_cli"` named tests; `message_router_harness_e2e` does not appear. INFERENCE: this multi-process e2e effectively does not run in the normal `nix flake check` gate; it is a manual/opportunistic harness.

### Altitude C — booted multi-VM service federation (heavy, kvm/prometheus only) — the closest thing to a federation smoke test
- FACT: `/git/github.com/LiGoldragon/CriomOS-test-cluster` is the "independent fixture cluster." Its `lib/mkCriomeAuthWitnessTest.nix` boots a **two-VM `runNixOSTest`** running real `spirit` + `criome` + persona-`router` + `mirror` daemon *services* across two guests, mints a real Spirit-record head, attests a `signal-mirror::Append` forward through real criome BLS, sends one `signal-router::ForwardMessage` over TCP to node-b, and asserts the mirror durably lands the head — plus two fail-closed negatives (`UnknownSigner`, `InvalidSignature`).
- FACT: exposed as `checks.criome-auth-witness` and reproduce app `apps.test-criome-auth-witness` / `nix run .#run-criome-auth-on-prometheus`; it consumes daemons as **flake inputs** (`CriomOS-test-cluster/flake.nix`: `inputs.criome`, `inputs.router` `.packages.witness`, `inputs.mirror`, `inputs.spirit`). Needs `/dev/kvm`; boots only on prometheus.
- FACT: same repo also has `lib/mkVmTest.nix` (per-node booted behaviour tests, auto-generated per hosted Pod), `lib/mkDeployTest.nix` (2-node real lojix production deploy under `runNixOSTest`), and eval-only static contract checks (`checks/cluster-contracts.nix`, `full-module-contracts.nix`, `source-constraints.nix`). Its `INTENT.md` explicitly states the non-negotiable: **proof is first-hand reproducible evidence (per-causal-link logs + one reproduce command), not a green result** (Spirit `vcin`, `7let`), and a Nix cache-hit must not be able to fake a VM boot.

Other genuine cross-daemon points (Altitude A style, in-repo): `router/tests/end_to_end_remote_forward.rs`, `router/tests/criome_forward_attestation.rs`, `message/tests/forward_to_router.rs`, `mentci/tests/criome_bridge.rs`, `mirror/tests/end_to_end_arc.rs`, `spirit/tests/mirror_shipper.rs`.

- FACT: **`CriomOS-test-cluster` is not `kameo-testing`.** `kameo-testing` (`/git/github.com/LiGoldragon/kameo-testing`) is a Kameo actor-runtime conformance suite (`tests/lifecycle.rs`, `supervision.rs`, `mailbox.rs`, `registry.rs`, `spawn.rs`, `streams.rs`, `topology.rs`) — it validates the actor library beneath the daemons, not daemon federation.

## 3. The integration gap (precise)

1. FACT: There is **no shared daemon-spawn/socket-drive test harness crate.** Every fixture is hand-rolled: `router`'s `CriomeFixture`/`MirrorBehindComponentSocket`, `harness`'s `CargoBinary`/`RepositoryPaths`, `persona`'s `tests/support/mod.rs` + `persona-component-fixture` bin, `spirit`'s in-`process_boundary` spawner. The "wait until socket appears," "encode length-prefixed signal frame," "connect + ask + decode reply" logic is re-implemented per repo on top of `triad-runtime`'s codec.
2. FACT/INFERENCE: The reliable, Nix-gated multi-component coverage that exists is **narrow** — essentially the criome→router→mirror auth-forward triangle (Altitude A in `router`, Altitude C in the cluster) and Spirit's own triad. The larger federation (spirit ↔ persona ↔ mind ↔ harness ↔ terminal ↔ orchestrate ↔ system ↔ message) has **single-component tests against fakes**, not real-peer integration.
3. FACT: The one multi-**process** binary harness (`harness` e2e) **skips by default and is not in any flake check**, so "N real daemon binaries talking in one hermetic sandbox" is **not** an exercised altitude. There is a hole between Altitude A (in-process, hermetic, cheap, but not real binaries/sockets-as-shipped) and Altitude C (real service processes, but only under a kvm VM on one host).
4. FACT: Altitude A integration relies on **branch-pinned git dev-dependencies** (e.g. `criome` on `criome-authorization-push`). INFERENCE: this couples the integration test's truth to branch coordination and makes a "stand up everything at once" test a version-alignment problem.
5. INFERENCE: "What does it take today to stand up 2+ real daemons and assert they talk?" — Either (a) add the peer as a git dev-dep and compose its library in-thread on a temp socket (the `router` pattern; ~250 lines of bespoke fixture per test), or (b) set `*_REPOSITORY`/`*_BINARY` env and run the `harness` e2e by hand, or (c) write a `runNixOSTest` and boot VMs on prometheus. There is no `nix run .#test-federation` that spawns the real daemon binaries hermetically.

## 4. Recommended staged path forward (buildable, aligned to existing conventions)

The grain of the codebase already answers "how": **Altitude A (in-process real-library composition) exposed as named `craneLib.cargoTest` checks** is the cheapest honest multi-daemon test and already ships in `router`. Grow from there; reserve VMs for the federation headline. Concretely:

Stage 0 — Extract the harness that everyone re-implements (unblocks all later stages).
- Create a small dev-only crate (working name `daemon-test-harness`, `-test`-suffixed per the `testing` skill's test-only-binary rule) that owns: temp-dir + `.sema` store + socket-path allocation; "spawn daemon binary (`CARGO_BIN_EXE_*`) or run library daemon in-thread"; `wait_until_listening`; and a typed `ask(socket, Input) -> Output` over `triad-runtime::LengthPrefixedCodec` + `signal-frame`. This generalizes `router`'s `CriomeFixture`/`MirrorBehindComponentSocket` and `harness`'s `CargoBinary`. INFERENCE: this removes the ~250-line bespoke-fixture tax that currently blocks writing new cross-daemon tests.
- Nix: it is a plain library dev-dep; no new flake surface yet.

Stage 1 — First useful two-daemon test as a pure flake check (smallest real win).
- Pick the already-proven pair with the cleanest durable assertion: **`message` → `router`** (both already have real daemons; `message/tests/forward_to_router.rs` and `router` already touch this). Compose real `message-daemon` + real `router-daemon` behind the Stage-0 harness, send one `signal-message` submission, assert it lands as a routed object with the router's durable state advancing (the `router` durable-head assertion style).
- Exactly mirror the existing convention: one behavior, named-for-invariant test, exposed as `checks.message-forwards-through-router-to-registered-actor = craneLib.cargoTest { cargoTestExtraArgs = "--test <name> … -- --exact"; }` in whichever consumer repo owns the pair (put it in `router`, which already has the peer dev-deps and the check pattern). This runs under ordinary `nix flake check` — no kvm.

Stage 2 — Promote the multi-process e2e out of "skips by default."
- Make `harness/tests/message_router_harness_e2e.rs` deterministic by feeding it the daemon binaries as Nix-built `packages.*` via env (`MESSAGE_DAEMON_BINARY`, `ROUTER_DAEMON_BINARY`, `MESSAGE_CLI_BINARY`), then expose it as a **named stateful output** (per the `testing` skill: stateful tests are named outputs, not pure `flake check` members) — e.g. `checks.harness-message-router-e2e` built in a derivation whose `buildInputs` are the four daemon packages, or a `apps.test-harness-federation` runner. This is the missing **Altitude B** middle tier: real shipped binaries, real sockets, hermetic sandbox, no VM. It closes the "in-process libs ≠ real binary/socket-as-shipped" gap without paying VM cost.

Stage 3 — A hermetic N-daemon "core federation smoke" (the buildable federation target below VM level).
- Build one runner (`apps.federation-smoke` in a new small aggregator flake, or extend `harness`) that Nix-builds the core loop's daemon packages — `spirit`, `criome`, `router`, `mirror`, `persona`, `harness`, `message`, `terminal` — spawns each real binary in a temp sandbox with its own socket + `.sema` store via the Stage-0 harness, applies the real bootstrap (`router-write-bootstrap`, `*-write-configuration` bins that already exist per repo), and drives ONE end-to-end causal chain: seed a Spirit record → criome attests → router forwards → mirror lands → assert durable head. This is the `criome-auth-witness` chain (Altitude C) **without VMs** — proving the wire/auth/durability federation on any builder. Keep the VM version (Stage 4) for the isolation properties the sandbox can't prove.
- Aggregation model: prefer flake **inputs** (the `CriomOS-test-cluster` precedent) over git dev-deps, so the federation smoke pins one coherent input set instead of per-repo branch pins — this directly addresses gap #4.

Stage 4 — Full federation under VM, honoring the cluster's proof standard.
- Grow the existing `CriomOS-test-cluster/lib/mkCriomeAuthWitnessTest.nix` from the 4-daemon auth chain toward the full core-loop federation as a `runNixOSTest`, keeping its non-negotiables (`INTENT.md`, Spirit `vcin`/`7let`): per-causal-link timestamped logs, one reproduce command (`nix run .#run-…-on-prometheus`), and a cache-hit that cannot fake a boot. This remains the kvm/prometheus-gated headline; Stages 1–3 are the everyday gate.

Why this ordering: it reuses the one integration pattern that already passes in Nix (`router-criome-forward-lands-in-mirror`), pays the harness-extraction cost once (Stage 0), and fills the exact missing altitude (real binaries, hermetic, no VM — Stages 2–3) before scaling the expensive VM federation. Every stage lands as the same `checks.<invariant-name> = craneLib.cargoTest{…--exact}` (pure) or named stateful output (heavy) that the `testing` skill and these repos already use.

## 5. Unknowns / not checked

- NOT CHECKED: whether any of the named checks currently pass — I did not run `nix flake check` or `cargo test` anywhere (read-only inspection only). Grades reflect test *presence/shape*, not green status.
- UNKNOWN: exact behavioral depth of `agent`'s tests (guardian daemon) — I read only file names + `spirit`'s guardian scenarios; `agent`'s own socket-level coverage is INFERENCE (looks thin).
- NOT CHECKED: the full body of `spirit/tests/runtime_triad.rs` (124KB) and `process_boundary.rs` (52KB) — I confirmed they spawn/compose real daemons over sockets and are Nix-checked, but did not enumerate every scenario.
- UNKNOWN: whether a `federation`/aggregator repo exists that I did not surface — I checked `CriomOS-test-cluster`, `criome`, `harness`, `goldragon` flakes for multi-daemon inputs; only `CriomOS-test-cluster` aggregates daemons. Other repos (e.g. `goldragon`, `lore`, `mind`) were not exhaustively opened.
- NOT CHECKED: whether the `harness` e2e's sibling-repo/`*_BINARY` env path actually builds today (it depends on sibling checkout layout at `/git/github.com/LiGoldragon`, which exists, but I did not execute it).
- UNKNOWN: whether Spirit intent records govern a preferred integration-test altitude beyond `vcin`/`7let`/`dqg3`/`xxgp` cited in `CriomOS-test-cluster/INTENT.md`; I did not query the Spirit daemon (no `spirit` CLI invocation made).

Per your instruction, this map is delivered inline (no report file written).