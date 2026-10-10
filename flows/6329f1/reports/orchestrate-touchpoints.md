# Orchestrate Touchpoints

Thread: orchestrate-anatomy
Flow: 6329f1
Method: `git show origin/main:<path>` against dadd537 (orchestrate), a597f1a (signal-orchestrate), 5cdf35a (meta-signal-orchestrate), and CriomOS-home origin/main.

## 1. Signal crates

### 1a. Ethos sources (verbatim)

**signal-orchestrate** `ethos/signal.ethos`:
```
Interface.{0 3 0}
Channel.{Orchestrate 1 6}
[]
{
  [Lock.LockRequest Release.LockId Observe.ObserveSelection]
  [Locked.Lock Released.Lock Observed.Observation]
  [LockRejected.LockRejection ReleaseRejected.ReleaseRejection]
  []
  [
    LockName.String
    FlowId.String
    LockPath.String
    LockPaths.Vector<LockPath>
    LockReason.String
    LockRequest.{LockName FlowId LockPaths LockReason}

    LockId.Integer
    Lock.{LockId LockName FlowId LockPaths LockReason}

    DuplicateName.Lock
    LockOverlap.{LockPath Lock}
    LockRejection.[DuplicateName.Lock PathOverlap.LockOverlap]
    ReleaseRejection.[UnknownLockId]

    ObserveSelection.[Locks]

    Locks.Vector<Lock>
    Observation.[Locks.Locks]
  ]
}
```

**meta-signal-orchestrate** `ethos/signal.ethos`:
```
Interface.{0 2 0}
Channel.{MetaOrchestrate 2 5}
[]
{
  [Configure.Configure]
  [Configured.Configured]
  [ConfigurationRejected.ConfigurationRejected]
  []
  [
    OrdinarySocketPath.String
    MetaSocketPath.String
    Configure.{OrdinarySocketPath MetaSocketPath}
    ConfigurationRefusal.[InvalidConfiguration]
    Configured.{Configure}
    ConfigurationRejected.{Configure ConfigurationRefusal}
  ]
}
```

Both use `Interface` and `Channel` roots. Both will be rewritten to `Signal` root per the design.

### 1b. Generation at origin/main

**build.rs is gone.** Regeneration happens via:
- `examples/regenerate.rs` — a Cargo example that reads `ethos/signal.ethos`, calls `ethos_zero::RustEmitter::wire_contract().emit()`, runs `rustfmt --edition 2024`, and writes the output to `src/generated/signal.rs`.
- `tests/regeneration.rs` — the freshness assertion. It re-runs the same generation pipeline into a temp directory and asserts byte-identity with `src/generated/signal.rs`. Both crates have identical regeneration tests.

ethos-zero is a **dev-dependency** (rev 2309e5b) used only in tests and the example. The generated code is committed.

### 1c. Generated public surface

#### signal-orchestrate (ordinary)

```rust
// Constants
pub const INTERFACE_VERSION: ProtocolVersion = ProtocolVersion::new(0u16, 3u16, 0u16);
pub const CHANNEL_CONTRACT_ID: ChannelContractId = ChannelContractId(1u32);
pub const CHANNEL_WIRE_REVISION: ChannelWireRevision = ChannelWireRevision(6u16);
pub const PROTOCOL_VERSION: ProtocolVersion = INTERFACE_VERSION;

// Wire envelope types
pub struct ProtocolVersion { pub major: u16, pub minor: u16, pub patch: u16 }
pub struct ChannelContractId(pub u32);
pub struct ChannelWireRevision(pub u16);
pub struct Frame { pub channel_contract_id: ChannelContractId, pub channel_wire_revision: ChannelWireRevision, pub protocol_version: ProtocolVersion, pub body: FrameBody }
pub enum FrameBody { Request(Request), Reply(Reply), Refusal(Refusal) }

// Domain types (all pub fields, named struct fields)
pub struct LockName(String);          // newtype, TryFrom + AsRef<str>
pub struct FlowId(String);            // newtype, TryFrom + AsRef<str>
pub struct LockPath(String);          // newtype, TryFrom + AsRef<str>
pub struct LockPaths(pub Vec<LockPath>);
pub struct LockReason(String);        // newtype, TryFrom + AsRef<str>
pub struct LockRequest { pub lock_name: LockName, pub flow_id: FlowId, pub lock_paths: LockPaths, pub lock_reason: LockReason }
pub struct LockId(pub i64);
pub struct Lock { pub lock_id: LockId, pub lock_name: LockName, pub flow_id: FlowId, pub lock_paths: LockPaths, pub lock_reason: LockReason }
pub struct DuplicateName(pub Lock);
pub struct LockOverlap { pub lock_path: LockPath, pub lock: Lock }
pub enum LockRejection { DuplicateName(Lock), PathOverlap(LockOverlap) }
pub enum ReleaseRejection { UnknownLockId }
pub enum ObserveSelection { Locks }
pub struct Locks(pub Vec<Lock>);
pub enum Observation { Locks(Locks) }
pub enum Request { Lock(LockRequest), Release(LockId), Observe(ObserveSelection) }
pub enum Reply { Locked(Lock), Released(Lock), Observed(Observation) }
pub enum Refusal { LockRejected(LockRejection), ReleaseRejected(ReleaseRejection) }

// All types derive: Archive, RkyvSerialize, RkyvDeserialize, Clone, Debug, PartialEq, Eq
// All types implement datomic::Datomic (embody/portion)
```

Hand-owned codec (src/codec.rs):
```rust
pub trait SignalFrameCodec: Sized {
    fn encode_length_prefixed(&self) -> Result<Vec<u8>, FrameCodecError>;
    fn decode_length_prefixed(bytes: &[u8]) -> Result<Self, FrameCodecError>;
}
pub enum FrameCodecError {
    LengthPrefixMissing, LengthMismatch { expected: usize, found: usize },
    LengthTooLarge, ArchiveEncode, ArchiveDecode,
    WrongChannelContract { expected: ChannelContractId, found: ChannelContractId },
    WrongChannelWireRevision { expected: ChannelWireRevision, found: ChannelWireRevision },
    UnsupportedProtocol { expected: ProtocolVersion, found: ProtocolVersion },
}
impl SignalFrameCodec for Frame { ... }
```

#### meta-signal-orchestrate (privileged)

```rust
pub const INTERFACE_VERSION: ProtocolVersion = ProtocolVersion::new(0u16, 2u16, 0u16);
pub const CHANNEL_CONTRACT_ID: ChannelContractId = ChannelContractId(2u32);
pub const CHANNEL_WIRE_REVISION: ChannelWireRevision = ChannelWireRevision(5u16);
pub const PROTOCOL_VERSION: ProtocolVersion = INTERFACE_VERSION;

pub struct OrdinarySocketPath(String);  // newtype, TryFrom + AsRef<str>
pub struct MetaSocketPath(String);      // newtype, TryFrom + AsRef<str>
pub struct Configure { pub ordinary_socket_path: OrdinarySocketPath, pub meta_socket_path: MetaSocketPath }
pub enum ConfigurationRefusal { InvalidConfiguration }
pub struct Configured { pub configure: Configure }
pub struct ConfigurationRejected { pub configure: Configure, pub configuration_refusal: ConfigurationRefusal }
pub enum Request { Configure(Configure) }
pub enum Reply { Configured(Configured) }
pub enum Refusal { ConfigurationRejected(ConfigurationRejected) }
pub enum FrameBody { Request(Request), Reply(Reply), Refusal(Refusal) }
pub struct Frame { pub channel_contract_id: ChannelContractId, pub channel_wire_revision: ChannelWireRevision, pub protocol_version: ProtocolVersion, pub body: FrameBody }
```

Same codec pattern, same FrameCodecError shape.

### 1d. Field-name uses within the signal crates (hand-written files only; generated code regenerates itself)

**signal-orchestrate** `src/codec.rs` (hand-written):
```
src/codec.rs:68:  if frame.channel_contract_id != CHANNEL_CONTRACT_ID {
src/codec.rs:71:      found: frame.channel_contract_id,
src/codec.rs:74:  if frame.channel_wire_revision != CHANNEL_WIRE_REVISION {
src/codec.rs:77:      found: frame.channel_wire_revision,
src/codec.rs:80:  if frame.protocol_version != PROTOCOL_VERSION {
src/codec.rs:83:      found: frame.protocol_version,
```

**signal-orchestrate** `tests/contract.rs` (hand-written):
```
tests/contract.rs:28:  lock_id: LockId(17),
tests/contract.rs:29:  lock_name: name("orchestrate-interfaces"),
tests/contract.rs:30:  flow_id: flow("01a04a30"),
tests/contract.rs:31:  lock_paths: LockPaths(vec![...]),
tests/contract.rs:32:  lock_reason: reason("generated-contract-witness"),
tests/contract.rs:52:  lock_name: lock.lock_name.clone(),
tests/contract.rs:53:  flow_id: lock.flow_id.clone(),
tests/contract.rs:54:  lock_paths: lock.lock_paths.clone(),
tests/contract.rs:55:  lock_reason: lock.lock_reason.clone(),
tests/contract.rs:81:  lock_path: path("..."),
tests/contract.rs:98:  channel_contract_id: CHANNEL_CONTRACT_ID,
tests/contract.rs:99:  channel_wire_revision: CHANNEL_WIRE_REVISION,
tests/contract.rs:100: protocol_version: INTERFACE_VERSION,
tests/contract.rs:101: body: FrameBody::Request(...),
tests/contract.rs:109: channel_contract_id: ChannelContractId(99),
```

**meta-signal-orchestrate** `src/codec.rs` (hand-written):
```
src/codec.rs:68:  if frame.channel_contract_id != CHANNEL_CONTRACT_ID {
src/codec.rs:71:      found: frame.channel_contract_id,
src/codec.rs:74:  if frame.channel_wire_revision != CHANNEL_WIRE_REVISION {
src/codec.rs:77:      found: frame.channel_wire_revision,
src/codec.rs:80:  if frame.protocol_version != PROTOCOL_VERSION {
src/codec.rs:83:      found: frame.protocol_version,
```

**meta-signal-orchestrate** `tests/contract.rs` (hand-written):
```
tests/contract.rs:20:  ordinary_socket_path: ordinary_path("/tmp/orchestrate.sock"),
tests/contract.rs:21:  meta_socket_path: meta_path("/tmp/meta-orchestrate.sock"),
tests/contract.rs:46:  configure: configure.clone(),
tests/contract.rs:52:  configure,
tests/contract.rs:53:  configuration_refusal: ConfigurationRefusal::InvalidConfiguration,
tests/contract.rs:65:  channel_contract_id: CHANNEL_CONTRACT_ID,
tests/contract.rs:66:  channel_wire_revision: CHANNEL_WIRE_REVISION,
tests/contract.rs:67:  protocol_version: INTERFACE_VERSION,
tests/contract.rs:68:  body: FrameBody::Refusal(...),
tests/contract.rs:69:  configure: configure(),
tests/contract.rs:70:  configuration_refusal: ConfigurationRefusal::InvalidConfiguration,
tests/contract.rs:79:  channel_wire_revision: ChannelWireRevision(99),
```

### 1e. Interface and Channel roots (legacy names, will become Signal root)

Both ethos sources use `Interface.{version}` and `Channel.{name id revision}` — these are the roots the new ethos-zero Signal anatomy replaces.

## 2. Orchestrate crate

### 2a. Field-name accesses of generated structs (will become positional)

All accesses of fields on types generated from the signal ethos files:

**Frame fields** (`channel_contract_id`, `channel_wire_revision`, `protocol_version`, `body`):
```
src/transport.rs:198:  let OrdinaryFrameBody::Request(request) = frame.body else {
src/transport.rs:240:  let MetaFrameBody::Request(request) = frame.body else {
src/transport.rs:251:  channel_contract_id: ORDINARY_CHANNEL_CONTRACT_ID,
src/transport.rs:252:  channel_wire_revision: ORDINARY_CHANNEL_WIRE_REVISION,
src/transport.rs:253:  protocol_version: ORDINARY_PROTOCOL_VERSION,
src/transport.rs:260:  channel_contract_id: META_CHANNEL_CONTRACT_ID,
src/transport.rs:261:  channel_wire_revision: META_CHANNEL_WIRE_REVISION,
src/transport.rs:262:  protocol_version: META_PROTOCOL_VERSION,
src/bin/orchestrate.rs:49:  .body
src/bin/meta_orchestrate.rs:50:  .body
```

**Lock fields** (`lock_id`, `lock_name`, `flow_id`, `lock_paths`, `lock_reason`):
```
src/store.rs:71:   RecordKey::new(self.lock.lock_id.0.to_string())
src/store.rs:90:   if request.lock_paths.0.is_empty() {
src/store.rs:94:   for path in &mut request.lock_paths.0 {
src/store.rs:106:  self.request.lock_name == lock.lock_name
src/store.rs:110:  self.request.lock_paths.0.iter().find_map(|requested| {
src/store.rs:111:  lock.lock_paths.0.iter().find_map(|held| {
src/store.rs:122:  lock_name: self.request.lock_name,
src/store.rs:123:  flow_id: self.request.flow_id,
src/store.rs:124:  lock_paths: self.request.lock_paths,
src/store.rs:125:  lock_reason: self.request.lock_reason,
src/store.rs:381:  .map(|stored| stored.lock.clone())
src/store.rs:384:  left.lock_name.as_ref().cmp(right.lock_name.as_ref())
src/store.rs:386:  .then_with(|| left.lock_id.0.cmp(&right.lock_id.0))
src/store.rs:387:  (continuation of above)
src/store.rs:419:  .next_lock_id  (this is StoredAllocator, not a generated type)
src/store.rs:422:  let lock = request.into_lock(LockId(allocator.next_lock_id));
src/store.rs:449:  Ok(OrdinaryOutcome::Reply(OrdinaryReply::Released(stored.lock)))
```

**LockOverlap fields** (`lock_path`, `lock`):
```
tests/ordinary_lock_contract.rs:129-133:
    Refusal::LockRejected(LockRejection::PathOverlap(LockOverlap {
        lock_path: requested.as_str().try_into().expect("test path"),
        lock: held,
    })),
```

**Configure fields** (`ordinary_socket_path`, `meta_socket_path`):
```
src/transport.rs:63:  let ordinary_path = Path::new(configure.ordinary_socket_path.as_ref());
src/transport.rs:64:  let meta_path = Path::new(configure.meta_socket_path.as_ref());
src/defaults.rs:55:   ordinary_socket_path,   (struct literal construction)
src/defaults.rs:56:   meta_socket_path,        (struct literal construction)
```

**Configured fields** (`configure`):
```
src/store.rs:371:  Ok(MetaReply::Configured(Configured { configure }))
```

**LockRequest fields** (in NormalizedLockRequest):
```
src/store.rs:90:   request.lock_paths.0.is_empty()
src/store.rs:94:   for path in &mut request.lock_paths.0
src/store.rs:106:  self.request.lock_name
src/store.rs:110:  self.request.lock_paths.0.iter()
src/store.rs:122-125: lock_name, flow_id, lock_paths, lock_reason (from self.request)
```

**Test field accesses** (`ordinary_lock_contract.rs`):
```
tests/ordinary_lock_contract.rs:99:   acquired.lock_name.as_ref()
tests/ordinary_lock_contract.rs:100:  acquired.flow_id.as_ref()
tests/ordinary_lock_contract.rs:103:  acquired.lock_paths
tests/ordinary_lock_contract.rs:110:  acquired.lock_reason.as_ref()
tests/ordinary_lock_contract.rs:112:  acquired.lock_id.clone()
tests/ordinary_lock_contract.rs:188:  first.lock_id.clone()
tests/ordinary_lock_contract.rs:207:  first.lock_id / later.lock_id
tests/ordinary_lock_contract.rs:211:  first.lock_id
```

**IdentifiesLock trait** (ordinary.rs):
```
src/ordinary.rs:48:  &self.lock_id
```

### 2b. Store ↔ contract conversions

The store wraps contract types directly with no field-level mapping:

```rust
struct StoredConfiguration { configuration: Configure }  // wraps meta_signal_orchestrate::Configure
struct StoredLock { lock: Lock }                          // wraps signal_orchestrate::Lock
struct StoredAllocator { next_lock_id: i64 }              // not a contract type
```

`StoredLock` key: `self.lock.lock_id.0.to_string()` (accesses Lock.lock_id.0 which is i64).

`NormalizedLockRequest.into_lock()`:
```rust
fn into_lock(self, lock_id: LockId) -> Lock {
    Lock {
        lock_id,
        lock_name: self.request.lock_name,
        flow_id: self.request.flow_id,
        lock_paths: self.request.lock_paths,
        lock_reason: self.request.lock_reason,
    }
}
```

Sorting uses `lock.lock_name.as_ref()` and `lock.lock_id.0`.

### 2c. Nexus dispatch

**Reading a Frame** (transport.rs `OrdinarySocket::serve`):
```rust
async fn serve(&mut self, store: Arc<Mutex<OrchestrateStore>>) -> Result<(), TransportError> {
    let frame = self.read_frame().await?;
    let OrdinaryFrameBody::Request(request) = frame.body else {
        return Err(TransportError::UnexpectedRequestFrame);
    };
    let outcome = store.lock().await.ordinary(request)?;
    let body = match outcome {
        OrdinaryOutcome::Reply(reply) => OrdinaryFrameBody::Reply(reply),
        OrdinaryOutcome::Refusal(refusal) => OrdinaryFrameBody::Refusal(refusal),
    };
    self.write_frame(&ordinary_frame(body)).await
}
```

**Meta dispatch** (transport.rs `MetaSocket::serve`):
```rust
async fn serve(&mut self, store: Arc<Mutex<OrchestrateStore>>) -> Result<(), TransportError> {
    let frame = self.read_frame().await?;
    let MetaFrameBody::Request(request) = frame.body else {
        return Err(TransportError::UnexpectedRequestFrame);
    };
    let reply = store.lock().await.meta(request)?;
    self.write_frame(&meta_frame(MetaFrameBody::Reply(reply))).await
}
```

**Frame construction** (transport.rs):
```rust
fn ordinary_frame(body: OrdinaryFrameBody) -> OrdinaryFrame {
    OrdinaryFrame {
        channel_contract_id: ORDINARY_CHANNEL_CONTRACT_ID,
        channel_wire_revision: ORDINARY_CHANNEL_WIRE_REVISION,
        protocol_version: ORDINARY_PROTOCOL_VERSION,
        body,
    }
}

fn meta_frame(body: MetaFrameBody) -> MetaFrame {
    MetaFrame {
        channel_contract_id: META_CHANNEL_CONTRACT_ID,
        channel_wire_revision: META_CHANNEL_WIRE_REVISION,
        protocol_version: META_PROTOCOL_VERSION,
        body,
    }
}
```

### 2d. CLI printing (verbatim)

**orchestrate** (src/bin/orchestrate.rs:48-54):
```rust
match Frame::decode_length_prefixed(&bytes)
    .map_err(|error| format!("{error:?}"))?
    .body
{
    FrameBody::Reply(reply) => println!("{}", reply.textualize().as_ref()),
    FrameBody::Refusal(refusal) => println!("{}", refusal.textualize().as_ref()),
    _ => return Err("Nexus returned a non-reply frame".to_owned()),
}
```

**meta-orchestrate** (src/bin/meta_orchestrate.rs:49-55) — identical pattern with meta types.

**Request parsing** (both CLIs):
```rust
let request = Text::<signal_orchestrate::Request>::from(single_argument()?)
    .embody()
    .map_err(|error| format!("Datomic request: {error:?}"))?;
```

Frame construction in CLIs:
```rust
fn frame(body: FrameBody) -> Frame {
    Frame {
        channel_contract_id: signal_orchestrate::CHANNEL_CONTRACT_ID,
        channel_wire_revision: signal_orchestrate::CHANNEL_WIRE_REVISION,
        protocol_version: signal_orchestrate::PROTOCOL_VERSION,
        body,
    }
}
```

### 2e. live_nexus.rs assertions (verbatim)

```rust
// Test: zero_argument_startup_initializes_default_store_and_rejects_extras
assert_eq!(ready, "orchestrate-nexus ready\n");
// Configured reply (double-brace nesting):
format!("Configured.{{{{{} {}}}}}", roots.ordinary_socket().display(), roots.meta_socket().display())
// which produces: Configured.{{/path/ordinary.sock /path/meta.sock}}

// Test: ordinary_cli_uses_datomic_request_reply_and_refusal_roots_against_a_live_nexus
assert_eq!(reply(..., "Observe.Locks"), "Observed.Locks.[]");

let locked = format!("Locked.{{1 cli-lock 01a03eda [{}] cli-reason}}", lock_path.display());
assert_eq!(reply(..., &lock_request), locked);

// Duplicate name refusal:
format!("LockRejected.DuplicateName.{{1 cli-lock 01a03eda [{}] cli-reason}}", lock_path.display())

// Release:
assert_eq!(reply(..., "Release.1"), format!("Released.{{1 cli-lock 01a03eda [{}] cli-reason}}", lock_path.display()));

// Unknown release:
assert_eq!(reply(..., "Release.1"), "ReleaseRejected.UnknownLockId");

// Obsolete observe form rejected:
let obsolete = invoke(&roots, ..., "Observe.{Locks.{Current}}");
assert!(!obsolete.status.success());
```

### 2f. Flake checks

| Check | What it runs |
|---|---|
| `build` | `cargoBuild --all-targets` |
| `test` | `cargoTest` (default unit and integration) |
| `live-nexus` | `cargoTest --test live_nexus` |
| `ordinary-lock-contract` | `cargoTest --test ordinary_lock_contract` |
| `test-doc` | `cargoTest --doc` |
| `doc` | `cargoDoc -D warnings` |
| `fmt` | `cargoFmt` |
| `clippy` | `cargoClippy --all-targets -- -D warnings` |

### 2g. Cargo.toml pins (verbatim)

```toml
[dependencies]
datomic = { git = "https://github.com/LiGoldragon/datomic.git", rev = "b670c72d0c2cb94ad1e39b372271f6569d91e214" }
meta-signal-orchestrate = { git = "https://github.com/LiGoldragon/meta-signal-orchestrate.git", rev = "5cdf35a989f273b84f20a802855a03b6593b376d", default-features = false }
protos = { git = "https://github.com/LiGoldragon/protos.git", rev = "bfde3b878dd3de2991d7f605b59f57a13ef8f20b" }
rkyv = { version = "0.8", default-features = false, features = ["std", "bytecheck", "little_endian", "pointer_width_32", "unaligned"] }
sema-engine = { git = "https://github.com/LiGoldragon/sema-engine.git", rev = "7158e5503f37fd2fbca1d707f134e38a3fda1176" }
signal-orchestrate = { git = "https://github.com/LiGoldragon/signal-orchestrate.git", rev = "a597f1ae991059f6c2029b59a4773b2f77a62064", default-features = false }
thiserror = "2"
tokio = { version = "1", features = ["io-util", "macros", "net", "rt-multi-thread", "sync", "time"] }
```

Signal crate Cargo.toml pins (both identical):
```toml
protos = { git = "https://github.com/LiGoldragon/protos", rev = "bfde3b878dd3de2991d7f605b59f57a13ef8f20b" }
datomic = { git = "https://github.com/LiGoldragon/datomic", rev = "b670c72d0c2cb94ad1e39b372271f6569d91e214" }
rkyv = { version = "0.8", default-features = false, features = ["std", "bytecheck", "little_endian", "pointer_width_32", "unaligned"] }
# dev-dependencies:
ethos-zero = { git = "https://github.com/LiGoldragon/ethos-zero", rev = "2309e5b968b8702f2ecc679cd577b3e2bce0e99e" }
```

No ethos-zero runtime dependency. No sema-engine or tokio in the signal crates.

## 3. CriomOS-home check

### checks/orchestrate-service-path/default.nix

Asserted CLI output lines (verbatim from the Nix source, after interpolation):

```bash
# preflight binary
test "$preflight" = 'active legacy PathLock rows: 0'

# Lock round-trip
lock="{1 home-nexus-check home-nexus-check [$claimed_path] home-nexus-check}"
registration="Lock.{home-nexus-check home-nexus-check [$claimed_path] home-nexus-check}"
test "$registered" = "Locked.$lock"
# expands to: Locked.{1 home-nexus-check home-nexus-check [/build/.../claimed] home-nexus-check}

test "$observed" = "Observed.Locks.[$lock]"
# expands to: Observed.Locks.[{1 home-nexus-check ...}]

released="$(... orchestrate 'Release.{1}')"
# NOTE: sends Release.{1} (braced), not Release.1 (bare)
test "$released" = "Released.$lock"

test "$observed_empty" = 'Observed.Locks.[]'

configured="$(... meta-orchestrate 'Configure.{${ordinarySocketPath} ${metaSocketPath}}')"
test "$configured" = 'Configured.{${ordinarySocketPath} ${metaSocketPath}}'
# After Nix interpolation: Configured.{/build/.../orchestrate.sock /build/.../meta-orchestrate.sock}
# NOTE: single braces, while the Rust test expects Configured.{{path path}} (double braces)
```

**Observation:** The CriomOS check asserts `Configured.{path path}` (single braces) while `tests/live_nexus.rs` asserts `Configured.{{path path}}` (double braces). The datom structure of `Configured.{Configure}` should produce double braces (outer for Configured, inner for Configure). The CriomOS check also sends `Release.{1}` while the Rust test sends `Release.1`. The `embody` path accepts both forms since datomic parses the content positionally, but the textual output will differ.

### checks/orchestrate-wrapper-fallback/default.nix

Tests wrapper scripts that supply `ORCHESTRATE_SOCKET` / `ORCHESTRATE_META_SOCKET` from `$XDG_RUNTIME_DIR/orchestrate-nexus/`. Asserts the fallback socket paths but does not assert any datom text. No impact from the contract rewrite.

## 4. Legacy names

### Interface / Channel roots

Both ethos sources use the old roots:
- signal-orchestrate: `Interface.{0 3 0}` + `Channel.{Orchestrate 1 6}`
- meta-signal-orchestrate: `Interface.{0 2 0}` + `Channel.{MetaOrchestrate 2 5}`

These will become `Signal.{version}` in the new anatomy. The `CHANNEL_CONTRACT_ID` and `CHANNEL_WIRE_REVISION` constants and the codec validation that checks them will be removed. The Frame struct will become `Frame.{ Version Body }` with `Body.[ Request Reply Refusal ]` and `Refusal.[ VersionMismatch Unreadable ]` per the design.

### Dotos / ethos-monolith

**None found** in any of the three crates at origin/main. These were removed by flow e4 (01a04a30).

### Debug-format printing of replies

No `{reply:?}` or `{:?}` formatting of replies in user-facing output. Debug formats appear only in:
- Error paths in CLIs: `format!("Datomic request: {error:?}")`, `format!("{error:?}")` for codec/IO errors
- thiserror derives on error types (not replies)
- Test panic messages: `{refusal:?}`, `{reply:?}`, `{other:?}` in test helper functions

No Debug-format printing of actual reply values to stdout.

## Sources

- `/git/github.com/LiGoldragon/orchestrate` at origin/main dadd537
- `/git/github.com/LiGoldragon/signal-orchestrate` at origin/main a597f1a
- `/git/github.com/LiGoldragon/meta-signal-orchestrate` at origin/main 5cdf35a
- `/git/github.com/LiGoldragon/CriomOS-home` at origin/main (checks/orchestrate-service-path, checks/orchestrate-wrapper-fallback)
