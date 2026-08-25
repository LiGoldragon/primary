# Orchestrate Nexus audit witness

Flow f426777b auditing flow 01a03603 claims about orchestrate 09c19ce2af53 (0.22.0).

## 1. Fresh durable PathLock Nexus shape (claims 1, 19)

**Claim:** Legacy lane/claim/workflow/upgrade runtime replaced wholesale; what remains is daemon, Sema-owned state, two required sockets, generated contracts, and two thin clients (orchestrate, meta-orchestrate).

**Method: code read** `/git/github.com/LiGoldragon/orchestrate/Cargo.toml`, all `src/` files, `tests/`.

The source tree contains exactly five source files and one test:

- `src/main.rs` (daemon startup, 49 lines)
- `src/store.rs` (Sema durable state owner, 407 lines)
- `src/transport.rs` (two Unix socket listeners, 381 lines)
- `src/lib.rs` (2 lines: re-exports store and transport modules)
- `src/bin/orchestrate.rs` (ordinary CLI, 106 lines)
- `src/bin/meta_orchestrate.rs` (meta CLI, 91 lines)
- `tests/live_nexus.rs` (process scenario test, 172 lines)

No lane, claim, workflow, worktree, upgrade, agent, divergence, repository, execution, role, router, messenger, presentation, handover, or layout modules exist. Those were all deleted in the single commit 09c19ce (11,439 lines removed, 1,304 added; 44 files changed).

**Method: probe** `git diff --stat 09c19ce^..09c19ce`.

The diff confirms wholesale removal: `src/claim.rs`, `src/lane.rs`, `src/workflow.rs`, `src/upgrade_frame.rs`, `src/execution.rs`, `src/daemon.rs`, `src/service.rs`, `src/tables.rs` (2,244 lines), `src/orchestrator_presentation.rs` (1,418 lines), and 12 other legacy modules were deleted. `checks/stateful-nix-scenario.sh` was deleted. `tests/state_only.rs` was deleted. Three new files were added: `src/store.rs`, `src/transport.rs`, `tests/live_nexus.rs`.

Cargo.toml declares exactly three binaries: `orchestrate-daemon`, `orchestrate`, `meta-orchestrate`. No upgrade socket, no compatibility binary, no alias.

**Verdict: CONFIRMED.**

## 2. Daemon-owned Sema durability (claims 2, 22-25)

**Claim:** One Sema store persists configuration and active locks via sema-engine; neither CLI opens storage. Registration conflicts reject atomically with typed refusals carrying the holder. Release by name, re-registration allowed. Reconfiguration: repeat OK, store change = StorePathImmutable, other incompatible = InvalidConfiguration.

**Method: code read** `src/store.rs`, `src/bin/orchestrate.rs`, `src/bin/meta_orchestrate.rs`.

- `OrchestrateStore::open` calls `sema_engine::Engine::open`, registers two tables (`orchestrate_configuration` and `active_path_locks`), and either persists the startup Configure value (virgin store) or reads back the persisted one (reopened store). Only `src/store.rs` references `sema_engine` (confirmed by `grep -c`; both CLIs have zero occurrences).
- Neither CLI imports, references, or opens any storage engine. They connect to their respective Unix sockets via environment variables (`ORCHESTRATE_SOCKET`, `ORCHESTRATE_META_SOCKET`) and exchange Signal frames only.
- `register()` checks all stored locks for duplicate active name (returns `DuplicateActiveName` carrying the holder `PathLock`) and ancestor/descendant path overlap (returns `PathOverlap` carrying the conflicting `PathLockPath` and holder). Both are atomic: the check runs before any assertion.
- `release()` retracts the active row by `RecordKey`. Unknown name returns `UnknownActiveName`. After release, re-registration succeeds.
- `meta()` matches the three Configure cases: identical configuration returns `Configured`; changed store_path returns `StorePathImmutable`; any other difference returns `InvalidConfiguration`.

**Method: probe** `cargo test --offline -- --nocapture`.

Three store unit tests pass:
- `persists_normalized_locks_and_refuses_conflicts`: opens a store, registers a lock with an unnormalized path, drops the store, reopens it, and verifies the lock survives (a duplicate-name refusal on re-register proves persistence). Then tests overlap refusal (both descendant and ancestor), release, release-of-unknown refusal, and re-registration after release.
- `configure_refuses_store_path_changes`: confirms repeat-Configure success and changed-store StorePathImmutable refusal.
- `rejects_an_empty_or_nonabsolute_path_set_before_writing`: validates path constraints.

The `persists_normalized_locks_and_refuses_conflicts` test is direct evidence that state survives store close/reopen (lines 333-339 of store.rs: `drop(store)` then `OrchestrateStore::open` on the same path, then the alpha lock is still active).

**Note:** The live integration test does not test durability across daemon restart. It tests one daemon lifecycle only. Durability across restart is proven at the unit level (store open/close/reopen), not at the assembled-system level.

**Verdict: CONFIRMED.**

## 3. CLI Datom-only boundary and daemon binary-only (claims 3, 26)

**Claim:** Both CLIs accept exactly one concrete Datom positional object (PathLock / PathLockRelease / Configure), reject flags and file inputs, and convert text to validated generated Signal frames; the daemon speaks only pure binary signal and never textualizes.

**Method: code read** `src/bin/orchestrate.rs`, `src/bin/meta_orchestrate.rs`, `src/main.rs`, `src/transport.rs`, `src/store.rs`.

- Both CLIs have a `single_argument()` function that collects `env::args().skip(1)`, matches exactly one value, and rejects anything starting with `-`. This is flag and multi-argument rejection.
- The ordinary CLI parses the text argument via `DotosSource::new(&text).parse::<PathLock>()` or `.parse::<PathLockRelease>()`, wrapping the result in `OrchestrateRequest::Register` or `::Release`. It prints the reply via `.to_dotos()`. Text handling is confined to this binary.
- The meta CLI parses via `DotosSource::new(&text).parse::<Configure>()` and prints via `.to_dotos()`.
- The daemon (`src/main.rs`) imports `meta_signal_orchestrate::{Frame, MetaOrchestrateRequest}` and `signal_frame::{ClientFrame, ExchangeFrameBody}`. It decodes binary frames, not text. No `dotos`, `DotosSource`, or `DotosEncode` appears in `src/main.rs`, `src/transport.rs`, `src/store.rs`, or `src/lib.rs` (confirmed by grep: zero occurrences).
- Transport (`src/transport.rs`) reads/writes `LengthPrefixedSignal` binary frames via `decode_length_prefixed` / `encode_length_prefixed`. No text parsing or formatting anywhere in the daemon process.

**Verdict: CONFIRMED.**

## 4. Startup base64url Configure frame (claims 4, 21)

**Claim:** Startup carries one base64url argument containing a generated Configure frame, decoded and validated immediately, never a socket protocol.

**Method: code read** `src/main.rs`.

`startup_configure()` at lines 29-48:
- Collects args, requires exactly one (`[encoded]`).
- Decodes with `URL_SAFE_NO_PAD.decode(encoded)`.
- Decodes the binary as a `Frame::decode_client_frame(&bytes)`.
- Requires the frame body to be `ExchangeFrameBody::Request`.
- Requires `request.payloads().tail().is_empty()` (exactly one operation).
- Matches `MetaOrchestrateRequest::Configure(configure)` and returns the Configure value.
- This is called in `run()` before any socket binding or runtime creation.

Base64 is used only for argv delivery. The socket protocol in `src/transport.rs` uses raw `LengthPrefixedSignal` binary, never base64.

**Verdict: CONFIRMED.**

## 5. Actual-process scenario test (claims 5, 29, 30)

### Test shape

**Claim:** An actual-process scenario test starts orchestrate-daemon with a temporary .sema store and two sockets, invokes both real CLIs, and observes register, duplicate-name refusal, path-overlap refusal, release, re-register, and meta Configure.

**Method: code read** `tests/live_nexus.rs`.

The test `live_daemon_reserves_releases_and_configures_over_separate_signal_sockets`:
- Creates a `tempfile::tempdir()` for the store, ordinary socket, and meta socket.
- Constructs a Configure frame, encodes it as base64url via the same `startup_argument()` function.
- Spawns the real daemon binary via `Command::new(env!("CARGO_BIN_EXE_orchestrate-daemon"))` with the encoded argument. This is a real OS process, not an in-process call.
- Waits for the daemon's `"orchestrate-daemon ready\n"` line on stdout.
- Invokes the real `orchestrate` binary via `Command::new(env!("CARGO_BIN_EXE_orchestrate"))` with `ORCHESTRATE_SOCKET` env var, passing Datom text as the argument. Each invocation is a real process.
- Invokes the real `meta-orchestrate` binary via `Command::new(env!("CARGO_BIN_EXE_meta-orchestrate"))` with `ORCHESTRATE_META_SOCKET` env var.
- The `invoke()` helper runs the binary, asserts success, and returns trimmed stdout.
- Sequence tested: register alpha (success), duplicate alpha with different path (DuplicateActiveName), beta with nested path (PathOverlap), release alpha, re-register alpha (success), meta Configure (Configured).
- The daemon is killed and reaped at the end.

There are no mocked transports, no in-process calls, no hardcoded byte expectations. The test exercises the assembled system: three real binaries communicating over real Unix sockets with a real Sema store.

**Verdict: CONFIRMED. The test is a genuine actual-process scenario proof.**

### Local execution

**Method: probe** `cargo test --test live_nexus -- --nocapture` at `/git/github.com/LiGoldragon/orchestrate`.

```
running 1 test
orchestrate PathLock.{alpha [/tmp/.tmpaldRko/first] (first reservation)} -> PathLockRegistered.{alpha [/tmp/.tmpaldRko/first] (first reservation)}
orchestrate PathLock.{alpha [/tmp/.tmpaldRko/elsewhere] (duplicate reservation)} -> PathLockRegistrationRejected.{{alpha [/tmp/.tmpaldRko/elsewhere] (duplicate reservation)} DuplicateActiveName.{alpha [/tmp/.tmpaldRko/first] (first reservation)}}
orchestrate PathLock.{beta [/tmp/.tmpaldRko/first/nested] (overlapping reservation)} -> PathLockRegistrationRejected.{{beta [/tmp/.tmpaldRko/first/nested] (overlapping reservation)} PathOverlap.{/tmp/.tmpaldRko/first/nested {alpha [/tmp/.tmpaldRko/first] (first reservation)}}}
orchestrate PathLockRelease.{alpha} -> PathLockReleased.{alpha}
orchestrate PathLock.{alpha [/tmp/.tmpaldRko/first] (first reservation)} -> PathLockRegistered.{alpha [/tmp/.tmpaldRko/first] (first reservation)}
meta-orchestrate Configure.{/tmp/.tmpaldRko/orchestrate.sema /tmp/.tmpaldRko/ordinary.sock /tmp/.tmpaldRko/meta.sock} -> Configured.{/tmp/.tmpaldRko/orchestrate.sema /tmp/.tmpaldRko/ordinary.sock /tmp/.tmpaldRko/meta.sock}
test live_daemon_reserves_releases_and_configures_over_separate_signal_sockets ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.02s
```

All six steps passed. The output matches the claimed sequence in the flow witness.

### Remote Nix builder evidence

**Claim:** The test passed as a release test on the remote Nix builder, where a contract build-script defect was found and fixed first.

**Method: probe** `nix eval`, `nix path-info`, `nix log`.

- `nix eval '.#checks.x86_64-linux.live-nexus.drvPath'` resolves to `/nix/store/flb6w49zplv0xk36mick6rr51jnhd31s-orchestrate-test-0.22.0.drv`.
- The output path `/nix/store/kwzckhgy708773a6rdx77ga4v91bmk6x-orchestrate-test-0.22.0` exists in the local Nix store.
- `nix path-info --json` reports `"ultimate":false` (not built locally) and `"registrationTime":1787617422` (2026-08-25 02:23:42 CEST, 20 minutes after the commit at 02:03:26 CEST).
- `nix log` shows the full build log: `cargo test --release --locked --test live_nexus` compiled orchestrate v0.22.0 and the test passed: `test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.03s`.
- `ultimate: false` with no signatures and a build log present indicates the path was built on a remote builder and copied back, not fetched from a binary cache.

**Note:** `/home/li/orchestrate-test.log` is NOT evidence of this remote test. It dates from 2026-07-18 and shows orchestrate version 0.14.0, from a different era.

**Note:** The contract build-script defect and its repair are claimed in the witness and decision ledger (decisions 17, 18, 30) but are not directly verifiable from this repo alone. The fix would be in the signal-orchestrate and meta-signal-orchestrate repositories. What is verifiable is that the final remote build succeeded with the pinned revisions (`signal-orchestrate` rev `d23fb6430eda`, `meta-signal-orchestrate` rev `ebefb65c7076`).

**Verdict: CONFIRMED. The remote Nix build is evidenced by the store path with `ultimate:false`, consistent timestamp, and full build log showing the test passing at version 0.22.0.**

## Additional observations

### Transport serialization (decision 27)

**Method: code read** `src/transport.rs`.

The `TransportRuntime` holds `store: Arc<Mutex<OrchestrateStore>>`. Both `OrdinarySocket::serve` and `MetaSocket::serve` acquire `store.lock().await` before dispatching to `replies_from_ordinary_request` or `replies_from_meta_request`. All store mutations are serialized through this single Mutex. This confirms decision 27.

### Commit scope and timing

**Method: probe** `git log --format='%h %ai %s'`.

The replacement is a single commit `09c19ce` dated 2026-08-25 02:03:26 +0200. The previous commit `b143555` was 2026-08-13. The commit message is "Replace Orchestrate with durable PathLock Nexus". The change is 44 files, net removal of ~10,135 lines.

### Version

**Method: code read** `Cargo.toml` line 3.

`version = "0.22.0"` confirmed.

### Revision

**Method: probe** `git rev-parse HEAD`.

HEAD is `09c19ce2af53328748a73dd2d7b5c4288bc33d98`, matching the claimed revision exactly.

### Nix flake description

**Method: code read** `flake.nix` line 2.

`description = "orchestrate -- durable PathLock Nexus."` The flake defines seven checks (build, test, live-nexus, test-doc, doc, fmt, clippy) and three apps (default=orchestrate, daemon=orchestrate-daemon, meta=meta-orchestrate).

### Flow witness consistency

**Method: code read** `/home/li/primary/flows/01a03603/witnesses/orchestrateNexus.md`.

The flow's own witness records the same test output sequence as observed in this audit's local probe, differing only in the temporary directory name (expected). The witness records the "Red before replacement" state (156 compile errors), which is consistent with the wholesale removal claim. The witness records the remote Nix build, which is confirmed by independent Nix store evidence.
