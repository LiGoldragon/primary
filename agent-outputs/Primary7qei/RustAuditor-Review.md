# Rust Auditor Review: primary-7qei

## Task And Scope

Audited tracker item `primary-7qei`: typed Start/Stop conflict replies for Listener.

Scoped commits:

- `/git/github.com/LiGoldragon/signal-listener` commit `16b54472f43c`
- `/git/github.com/LiGoldragon/listener` commit `fb54c1018f4a`
- `/git/github.com/LiGoldragon/meta-signal-listener` inspected for dependency impact; no source-change commit was in scope.

Context consulted:

- `/home/li/primary/agent-outputs/PrimaryZ1aq/GeneralCodeImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/ListenerFreshHandover/ContextHandover.md`
- `bd show primary-7qei`
- `bd show primary-dkrt`
- `bd show primary-z1aq` was attempted twice but the embedded tracker backend was locked by another process.
- Spirit public intent query: `PublicTextSearch [listener typed conflict replies]` returned no matching record.

## Findings

No blocking or non-blocking defects found in the audited scope.

## Evidence

### signal-listener Contract

The three lifecycle conflict replies are schema-authored public `Output` variants:

- `schema/lib.schema:13` defines `CaptureAlreadyActive`.
- `schema/lib.schema:14` defines `NoActiveCapture`.
- `schema/lib.schema:15` defines `CaptureSessionMismatch`.
- `schema/lib.schema:61` defines `CaptureAlreadyActive ActiveCaptureSession`.
- `schema/lib.schema:62` defines `NoActiveCapture { }`.
- `schema/lib.schema:63` defines `RequestedCaptureSession CaptureSession`.
- `schema/lib.schema:64` defines `CaptureSessionMismatch { ActiveCaptureSession, RequestedCaptureSession }`.

The generated/public Rust surface carries typed, rkyv-backed, NOTA-capable types and routes:

- `src/schema/lib.rs:262` has `pub struct CaptureAlreadyActive(ActiveCaptureSession)`.
- `src/schema/lib.rs:270` has `pub struct NoActiveCapture {}`.
- `src/schema/lib.rs:286` has `pub struct CaptureSessionMismatch`.
- `src/schema/lib.rs:471` through `src/schema/lib.rs:473` expose the public `Output` variants.
- `src/schema/lib.rs:1280` through `src/schema/lib.rs:1282` map the variants to `OutputRoute`.
- `src/schema/lib.rs:1291` through `src/schema/lib.rs:1295` assign short headers.
- `src/schema/lib.rs:1306` through `src/schema/lib.rs:1311` decode those short headers.

Round-trip coverage includes all three new replies:

- `tests/round_trip.rs:118` through `tests/round_trip.rs:125` include `CaptureAlreadyActive`, `NoActiveCapture`, and `CaptureSessionMismatch` in the reply corpus.
- The same test path round-trips each reply through `Frame::encode_length_prefixed`/`Frame::decode_length_prefixed` and NOTA text parsing.

Versioning is coherent for the changed contract:

- `Cargo.toml:3` sets `signal-listener` to `0.3.0`.
- `build.rs:4` through `build.rs:8` uses schema build version `0.3.0`.
- `Cargo.lock` contains `signal-listener` version `0.3.0`.

### listener Runtime

The runtime now maps the ordinary lifecycle conflicts to typed public replies instead of generic `RequestUnimplemented`:

- `src/runtime.rs:69` through `src/runtime.rs:73` turns start-while-active into internal `Error::CaptureAlreadyActive`.
- `src/runtime.rs:83` through `src/runtime.rs:84` turns stop-while-idle into internal `Error::NoActiveCapture`.
- `src/runtime.rs:87` through `src/runtime.rs:93` turns wrong-session stop into internal `Error::CaptureSessionMismatch`.
- `src/runtime.rs:272` through `src/runtime.rs:278` lowers start conflict to `Output::CaptureAlreadyActive`.
- `src/runtime.rs:281` through `src/runtime.rs:292` lowers stop conflicts to `Output::NoActiveCapture` and `Output::CaptureSessionMismatch`.
- Generic `RequestUnimplemented` remains only as the non-lifecycle fallback at `src/runtime.rs:297`.

Wrong-session stop preserves the active capture:

- `src/runtime.rs:83` temporarily takes the active capture.
- `src/runtime.rs:89` restores it before returning `CaptureSessionMismatch`.
- `tests/runtime.rs:502` through `tests/runtime.rs:532` checks the mismatch reply and then confirms status still reports the original active session.

Runtime tests cover the three requested conflict shapes:

- `tests/runtime.rs:470` through `tests/runtime.rs:488` covers start while active.
- `tests/runtime.rs:490` through `tests/runtime.rs:499` covers stop while idle.
- `tests/runtime.rs:501` through `tests/runtime.rs:532` covers wrong-session stop and state preservation.

Socket replies preserve exchange identity for a conflict reply:

- `src/daemon.rs:85` through `src/daemon.rs:90` receives a contract request, handles it through runtime, and sends the reply using the request object.
- `src/transport.rs:220` through `src/transport.rs:222` builds the reply frame with `request.exchange()`.
- `tests/runtime.rs:611` through `tests/runtime.rs:651` sends an idle stop request with a fixed exchange identifier and verifies the reply exchange and `Output::NoActiveCapture`.

Downstream dependency/version state is coherent for `listener`:

- `Cargo.toml:3` sets `listener` to `0.3.0`.
- `Cargo.toml:39` depends on `signal-listener` branch `main`.
- `Cargo.lock:322` through `Cargo.lock:323` records `listener` version `0.3.0`.
- `Cargo.lock:642` through `Cargo.lock:644` records `signal-listener` version `0.3.0` at commit `16b54472f43c9e3cf20b5bef726617156ce8b3a4`.

### meta-signal-listener Impact

`meta-signal-listener` remains clean at commit `30ed2770`. Its source imports the Listener configuration record from `signal-listener`, not the ordinary start/stop/status reply vocabulary changed here:

- `schema/lib.schema:9` imports `ListenerDaemonConfiguration signal-listener:lib:ListenerDaemonConfiguration`.
- `Cargo.toml:30` depends on `signal-listener` branch `main`.

Its standalone `Cargo.lock` still pins `signal-listener` `0.2.0`, but that is not a blocker for this audit because no meta source consumes the new lifecycle reply variants and `listener`'s resolved lock uses `signal-listener` `0.3.0` for the integrated build. Updating the meta lock can be done in a separate housekeeping pass if desired, but it is not required for `primary-z1aq` closure or `primary-dkrt` start.

## Checks Run

Commands run:

- In `/git/github.com/LiGoldragon/signal-listener`:
  - `cargo test --locked --features nota-text --test round_trip --target-dir /tmp/primary-7qei-signal-listener-target`
  - Result: passed, 4 tests.
  - `nix flake check`
  - Result: passed for x86_64-linux outputs; Nix omitted incompatible aarch64-linux outputs.
  - `jj status`
  - Result: clean; parent commit is `16b54472`.
- In `/git/github.com/LiGoldragon/listener`:
  - `cargo test --locked --test runtime --target-dir /tmp/primary-7qei-listener-target`
  - Result: passed, 11 tests.
  - `nix flake check`
  - Result: passed for x86_64-linux outputs; Nix emitted app metadata warnings and omitted incompatible aarch64-linux outputs.
  - `jj status`
  - Result: clean; parent commit is `fb54c101`.
- In `/git/github.com/LiGoldragon/meta-signal-listener`:
  - `jj status`
  - Result: clean; parent commit is `30ed2770`.

The implementer's cited checks are meaningful for the changed behavior: the contract round-trip test witnesses wire/NOTA compatibility for the added reply variants, while the runtime test witnesses the runtime lowering, wrong-session state preservation, and public socket envelope identity.

## Tracker State

Observed tracker state:

- `primary-7qei` was open before this report.
- `primary-7qei` depends on completed `primary-z1aq`.
- `primary-7qei` blocks open deployment bead `primary-dkrt`.
- `primary-dkrt` remains open and depends on `primary-7qei`.

Tracker state changes made by this auditor: none.

`primary-z1aq` is supported for closure by this audit. `primary-7qei` is supported for closure. `primary-dkrt` can start after the tracker is advanced past `primary-7qei`.

## Blockers And Residual Risks

No deployment blockers were found in the audited commits.

Residual risks outside this audit:

- No real microphone-to-clipboard smoke test was in scope.
- No deployment through CriomOS-home was in scope.
- The standalone `meta-signal-listener` lock file still points at the previous `signal-listener` commit, but the audited runtime build resolves `signal-listener` `0.3.0` and the meta source does not consume the changed reply vocabulary.

