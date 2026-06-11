# build and test ground truth — Build + test ground truth

cloud-designer, 2026-06-11. Grounded run for report 40. Area: Build + test health of the new lojix daemon (Stack B) on lojix main HEAD 7d66d2e, triad-port/ v0.3.0

## Method

All runs in the /git checkout's detached-HEAD worktree at exactly HEAD 7d66d2e (clean tree, `git status` empty; build/eval only, non-mutating). Toolchain: cargo/rustc 1.95.0; manifest requires 1.88 (satisfied). nix 2.34.6. CARGO_HOME=/home/li/.cargo (warm git cache). Commands run, each with exit captured to a /tmp log: (1) `cargo build --offline --bins` (warm); (2) forced recompile after removing lojix's own fingerprint+deps artifacts: `rm -rf target/debug/.fingerprint/lojix-* target/debug/deps/lojix-* target/debug/deps/liblojix-*` then `cargo build --offline --bins` (cold-compile of the lojix crate against cache); (3) plain network `cargo build --bins` (no --offline); (4) `cargo test --offline` (non-ignored); (5) `cargo test --offline -- --ignored --nocapture --test-threads=1` (timeout 540s); (6) `git ls-remote` against nota-codec.git and horizon-rs.git; (7) `nix flake metadata github:LiGoldragon/CriomOS-test-cluster`; (8) direct `./target/debug/lojix-daemon` invocations with no-arg and a malformed-NOTA arg. Also read schema_runtime.rs, lib.rs, daemon.rs, both bin entrypoints, and all four test files to ground claims at file:line.

## Findings

### ✅ confirmed — cargo build of both binaries succeeds offline against the warm cargo cache (exit 0).

- **Evidence:** Warm: /tmp/lojix_build_offline.log -> `Finished dev profile ... in 0.22s` / `BUILD_OFFLINE_EXIT=0`. Cold-compile of the lojix crate after deleting its fingerprint+deps artifacts: /tmp/lojix_build_cold.log -> `Compiling lojix v0.3.0 (/git/.../triad-port)` / `Finished dev profile ... in 1.54s` / `BUILD_COLD_EXIT=0` (wall 0:01.55). Both binaries present: target/debug/lojix (39.7MB), target/debug/lojix-daemon (45.6MB).
- **Cutover implication:** Build health is green TODAY on this warm-cache machine. Builds reproduce only where the cargo git cache already holds the pinned revs; not a from-cold-clone guarantee (see nota-codec finding).

### ✅ confirmed — A plain (non-offline) `cargo build` does NOT hit the network because the Cargo.lock is already satisfied by cache; it succeeds and fetches nothing.

- **Evidence:** /tmp/lojix_build_network.log -> `Finished dev profile ... in 0.05s` / `BUILD_NETWORK_EXIT=0` — no `Updating git repository` / `Downloading` lines. General network IS up: `git ls-remote https://github.com/LiGoldragon/horizon-rs.git HEAD` returns `9fae4a36...`.
- **Cutover implication:** On the current builder (ouranos/this workstation) the build is reproducible offline or online. The risk is only a cold machine or a `cargo update`.

### ✅ confirmed — The nota-codec.git remote 404s (report-38 concern is REAL and live), but the pinned rev is in the warm cache, so only a cold clone / `cargo update` would red-build.

- **Evidence:** `git ls-remote https://github.com/LiGoldragon/nota-codec.git HEAD` -> `ERROR: Repository not found. fatal: Could not read from remote repository.` Cargo.lock pins `git+https://github.com/LiGoldragon/nota-codec.git?branch=main#f761421c...` (line 404) and that rev IS checked out at ~/.cargo/git/checkouts/nota-codec-99150e6780a2590a/f761421. All other pinned git-dep revs (triad-runtime 069ba8e, schema-rust-next 5cadd25, nota-config bd9173a, nota-next d8862b6, horizon-rs 9fae4a3) are likewise present in the cache.
- **Cutover implication:** BLOCKER for a clean/cold-machine build and for any dependency bump. The cutover plan must pin engine deps to explicit, resolvable revs (or a flake-level vendored pin / fork the dead nota-codec repo) BEFORE building on a fresh deploy host. Do not assume CI/another node can build this lock today.

### ✅ confirmed — Non-ignored test suite is fully green: 11 passed, 0 failed, 7 ignored across all targets.

- **Evidence:** /tmp/lojix_test_nonignored.log: engine_routing `8 passed; 0 failed; 1 ignored`; build_smoke `0 passed; 0 failed; 6 ignored`; actor_native_runtime `1 passed`; horizon_materialization_contract `2 passed`; lib/bin unit + doc-tests `0 tests`. No FAILED lines anywhere.
- **Cutover implication:** The non-IO engine logic (reads, subscription handshake, pin/retire rejection, deploy guard, materialization contract) is verified. Confidence the in-process pipeline behaves as specified.

### ✅ confirmed — The activate reject-guard is LIVE: every activating action is rejected with UnsupportedDeployAction; only Eval/Build proceed.

- **Evidence:** Test `activating_deploy_is_rejected_until_activate_lands ... ok` (engine_routing.rs:164, /tmp/lojix_test_nonignored.log:44). Guard source `unsupported_deploy_reason` (schema_runtime.rs:524-541): System admits only `Eval | Build`, Home admits only `Build`; everything else -> `UnsupportedDeployAction`. Called once at the Deploy entry.
- **Cutover implication:** Confirms report-38 gate 1: the daemon STILL cannot activate any node. It can eval+build only. A first cutover cannot perform a real Boot/Switch/Test/Activate; the guard must be lifted AND the broken effect bodies fixed first. Parallel-run safety is preserved (daemon refuses to write false activation state).

### ✅ confirmed — ALL 7 ignored end-to-end tests pass, including real `nix build`, real daemon-binary socket roundtrip, and concurrency — the closest thing to live ground truth (exit 0).

- **Evidence:** /tmp/lojix_test_ignored.log, `TEST_IGNORED_EXIT=0`. build_smoke `6 passed; 0 failed in 44.45s`: `build_dune_fixture_through_the_engine ... BUILD reached Deployed: deployment 1 realised at commit 1`; `eval_dune_fixture_through_the_engine ... EVAL reached Deployed`; `daemon_binary_socket_roundtrip_eval ... DAEMON SOCKET roundtrip reached Deployed: deployment 1`; `concurrent_requests_are_served_in_parallel ... CONCURRENT: ordinary query answered in 472.634µs while a deploy ran`; `oversized_frame_is_bounded_and_daemon_survives ... ok` (daemon logged `frame body is too large: 4294967295 bytes` and survived); `permissive_owner_socket_mode_is_refused ... ok`. engine_routing `production_eval_materializes_horizon_inputs_and_returns_deployed ... ok` (real `nix flake metadata`+`nix eval` with horizon input materialization -> Deployed commit 1).
- **Cutover implication:** The eval+build deploy path, the real daemon process, two-socket bind, length-prefixed frame codec, and concurrent service are all proven working end-to-end against a real fixture cluster. The daemon's CORE spine is production-shaped and demonstrably functional for the build/eval capability — the cutover's hard work is the activate plumbing and consumer migration, not the spine.

### ✅ confirmed — I started the real lojix-daemon binary and round-tripped a client deploy request over its owner socket — and it reached Deployed.

- **Evidence:** Done via the ignored test `daemon_binary_socket_roundtrip_eval` which spawns `env!(CARGO_BIN_EXE_lojix-daemon)` with a single NOTA config arg, binds ordinary+owner unix sockets, writes a length-prefixed `dune` Eval frame to the owner socket, and decodes the reply: `DAEMON SOCKET roundtrip reached Deployed: deployment 1`. The daemon process spawn + two-socket bind + frame codec + full pipeline + real nix IO all exercised in one run.
- **Cutover implication:** A live daemon-client round-trip works today for Eval. The wire path the production CLI client will use is verified end-to-end. This is the strongest single signal that Stack B's runtime is real, not a stub.

### ✅ confirmed — The daemon PARSES NOTA at startup from its single argv argument — the one-arg model holds but the no-NOTA-in-daemon hard override is violated.

- **Evidence:** Direct run: `./target/debug/lojix-daemon` (no arg) -> `(DaemonRejected [configuration decode error: no configuration argument supplied on argv])`; `./target/debug/lojix-daemon '(not valid nota %%%)'` -> `(DaemonRejected [configuration decode error: NOTA decode failed: expected u64 integer literal, got Ident("valid")])`. Source: lojix-daemon.rs:17 `nota_config::ConfigurationSource::from_argv()?.decode()?`. build_smoke.rs:89 comment confirms the test path exercises `config decode (inline NOTA)`.
- **Cutover implication:** Confirms report-38 gate 6 (hard-override violation). Before this privileged surface carries real deploy authority, startup must accept only a pre-generated rkyv message, not inline/`.nota` NOTA. The deploy/bootstrap tool must encode the config to binary before it reaches the daemon.

### ✅ confirmed — All daemon state is in-memory; the actor start() hook is a no-op; there is no redb/sema-engine dependency anywhere in the tree (no self-resume on restart).

- **Evidence:** lib.rs:121-137 `StoreState { live_set, gc_roots, event_log }` are three `Vec` tables behind one `Mutex` (lib.rs:181 `state: Mutex<StoreState>`). daemon.rs:153-155 `async fn start(&self) -> Result<()> { Ok(()) }` — no load/resume. `grep -riE 'redb|sema.engine'` over Cargo.toml/Cargo.lock/src finds only doc-comment mentions (lib.rs:11, lib.rs:177) — zero dependency.
- **Cutover implication:** Confirms report-38 gate 4: a restarted daemon cannot self-resume, violating its own SEMA-state invariant. Per the critique this blocks the FULL charter (durable live-set ownership), not minimal lojix-cli parity (lojix-cli is itself stateless). The psyche's open question 2 — first cutover on in-memory state vs. land persistence first — remains the gating decision; this run does not settle it.

### ✅ confirmed — The activate/copy/GC effect bodies behind the guard are broken exactly as report 38 stated (verified by direct grep, not re-run since the guard blocks them).

- **Evidence:** schema_runtime.rs:1819-1826 `activate_system` ssh-runs `nix-env -p /nix/var/nix/profiles/system --set "$CLOSURE"` — `$CLOSURE` is an unset shell var, and despite the :1821 comment there is no `switch-to-configuration` call. :1807-1813 `copy_closure` targets bare `ssh-ng://{node_name}` (no criome_domain_name resolution). :1831-1834 `collect_garbage` is bare `ssh <node> nix-store --gc` with no --max-freed/keep-roots guard. `run_path_info_gc` exists (:1351) and is dispatched (:1909) but per report 38 is never constructed.
- **Cutover implication:** These are the remediation targets that must land+test before lifting the guard: domain-resolved SSH host, interpolated real closure path, switch-to-configuration, keep-roots-gated GC. Confirms the activate capability is not merely gated but unimplemented underneath.

### 🟡 partial — The owner socket enforces a file-mode rejection (the 'other-access' guard), but only by mode — no SO_PEERCRED.

- **Evidence:** Test `permissive_owner_socket_mode_is_refused ... ok` confirms the daemon exits and prints an 'other-access' rejection when given owner mode 0o666. But report 38 (gate 8) notes authority rests on socket file-mode alone with no SO_PEERCRED; I did not find/exercise any peer-credential check in this run.
- **Cutover implication:** Mode-based refusal works as a first guard, but per-connection peer authentication (SO_PEERCRED) is still absent. Mitigated today because activate is rejected and no production consumer connects; must land before the owner socket carries real deploy authority.

## Notes

- GROUND-TRUTH BOTTOM LINE: On this warm-cache workstation, Stack B is GREEN — both binaries build offline (exit 0), 11/11 non-ignored tests pass, and ALL 7 ignored end-to-end tests pass including a real `nix build` to a realized closure, a real daemon-binary socket roundtrip to Deployed, and live concurrency (472us). The daemon's build/eval spine demonstrably works end-to-end today.
- The verdict from report 38 (NOT READY) is unaffected: every green test is on the eval/build path; the activate reject-guard is confirmed live (activating_deploy_is_rejected_until_activate_lands passes), so the daemon still cannot deploy a real node. The tests pass precisely BECAUSE the unimplemented/broken activate path is gated off.
- Three cutover-blocking realities re-confirmed by direct command/code inspection this run: (1) nota-codec.git 404s live — build reproduces only from warm cache, a cold/CI build or any dep bump red-builds; (2) the daemon parses inline NOTA at startup (hard-override violation, shown by a live malformed-NOTA run); (3) state is in-memory with a no-op start() and zero redb/sema-engine dep — no restart self-resume.
- TEST_NONIGNORED_EXIT printed blank due to a PIPESTATUS-with-tee scoping quirk, NOT a failure — every per-target `test result:` line reads `ok ... 0 failed`. TEST_IGNORED_EXIT=0 captured cleanly (no tee). I did not see any FAILED/panic line in either run.
- The report-38 trait-rename time-bomb (triad-runtime ActorMultiListenerDaemon -> Async*) is latent only: the current pinned rev 069ba8e compiles against the names in daemon.rs (the live trait is `ActorMultiConnectionRuntime` at daemon.rs:150). A naive `cargo update` to a renamed rev would break the compile — but nothing broke in THIS run because the lock is pinned and cache-warm.
- Nothing was mutated: all builds/tests ran in the /git detached-HEAD worktree at HEAD 7d66d2e (clean tree), build/eval/test only, in temp dirs for daemon sockets. No code-repo main was touched. The fixture flake github:LiGoldragon/CriomOS-test-cluster resolved and was already in the local nix store, so the end-to-end nix paths used real (not stubbed) evaluation/build.
- Caveat on reproducibility for the cutover plan: 'build is green' is true for THIS machine's warm cargo+nix caches. The plan must independently verify a cold builder can resolve the lock (blocked today by the nota-codec 404) before relying on any other deploy host.
