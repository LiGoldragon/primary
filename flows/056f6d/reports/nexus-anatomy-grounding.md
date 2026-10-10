# Nexus anatomy grounding — Orchestrate as the concrete Nexus

Grounding for the living's request to see the ethos of the signal, the queries
and responses, the Nexus processes, and how the signal and the CLI interact.
This report is the substrate; the visuals are not this flow's work.

Every claim below carries a source path and line range. Quotes are verbatim.
Observed / inferred / unknown are kept apart and labelled.

## 0. Repositories and revisions read

| Repository | Path | Revision read | Tree state |
|---|---|---|---|
| orchestrate (the Nexus) | `/git/github.com/LiGoldragon/orchestrate` | `9070cbb8717813b127e448dd5a43a2095daf7d1b` | clean |
| signal-orchestrate (ordinary wire) | `/git/github.com/LiGoldragon/signal-orchestrate` | `e7221190ed4cf256ee1f0ead1b8af4758c67079a` | **dirty** — see §0.1 |
| meta-signal-orchestrate (meta wire) | `/git/github.com/LiGoldragon/meta-signal-orchestrate` | `4279ad05141c392ad4fee83be7cee09d5dc12df5` | clean |
| signal (shared framing) | `/git/github.com/LiGoldragon/signal` | checkout HEAD `66e7b153706696c2cfbb2abcf931a5e83aec91af`; **read at the pinned `8f9a0deb701cebbea518679548df4a795affc918`** | checkout is ahead of the pin |
| nexus (shared library) | `/git/github.com/LiGoldragon/nexus` | `c495f2acbfff57e017092b9cc1fbf9f73ca2badf` | matches the pin |

The pins are read from `/git/github.com/LiGoldragon/orchestrate/Cargo.toml:17-29`
(`[workspace.dependencies]`): `signal-orchestrate` rev `e7221190…` (line 27),
`meta-signal-orchestrate` rev `4279ad05…` (line 21), `signal` rev `8f9a0deb…`
(line 26), `nexus` rev `c495f2ac…` (line 22), `sema-engine` rev `27e814a7…`
(line 25), `kameo = "0.22"` (line 20). Workspace version `0.35.0`
(`Cargo.toml:10`).

### 0.1 Disconfirming evidence: the signal-orchestrate checkout is not what is deployed

`git -C /git/github.com/LiGoldragon/signal-orchestrate status --porcelain`
reports modifications to `Cargo.toml`, `ethos/signal.ethos`, `src/lib.rs`,
`src/generated/signal.rs`, and a new `tests/exchange_envelope.rs` — in-flight
work bumping the crate to `4.0.0` and adding a greeting/exchange layer
(`signal` rev `66e7b153…`, `datom-codec` rev `09e2a9d5…`).

**Orchestrate pins `e7221190…`, so none of that in-flight work is in the
running Nexus.** Everything in §§1–6 below is stated from the *pinned*
revisions. The in-flight shape is recorded in §7 as vision-adjacent, not as
observation of the running system.

### 0.2 The running process, witnessed

```
li  3257720  … Ssl  Sep12  0:01  /nix/store/6ynfv0hywpwg8gpapyfh7zn0yqzdg52z-orchestrate-0.35.0/bin/orchestrate-nexus
```
(method: `ps aux | grep orchestrate-nexus`, 2026-09-18)

Sockets present, witnessed by `ls -la $XDG_RUNTIME_DIR/orchestrate-nexus/`:

```
srw-------  1 li users  0 Sep 12 10:20 meta-orchestrate.sock
-rw-------  1 li users  0 Sep 12 10:20 meta-orchestrate.sock.claim
srw-rw----  1 li users  0 Sep 12 10:20 orchestrate.sock
-rw-------  1 li users  0 Sep 12 10:20 orchestrate.sock.claim
```

Store present: `/home/li/.local/state/orchestrate-nexus/orchestrate-nexus.sema`
(958464 bytes, mtime 2026-09-18 14:34), beside a
`orchestrate-nexus.sema.pre-v2-20260908T111047+0200.bak`.

---

## 1. The signal ethos

### 1.1 The ordinary socket — `signal-orchestrate/ethos/signal.ethos` @ `e7221190`

Reproduced in full (47 lines):

```
; Orchestrate Lock signal — the ordinary wire contract.
;
; The Lock family: acquire, release, observe coordination locks.
; Every lock carries an integer id, a name, a flow, absolute paths,
; and a reason.
;
; Observe opens a subscription rather than answering once. The Nexus
; writes one Observed frame carrying the state on open and one more
; for every later change, on the same connection, until the peer
; closes it. The subscription is the connection, so there is no token
; and no Unwatch: a peer that stops reading has unsubscribed. Every
; other query is answered with exactly one frame.
;
; Configure is accepted here only while the meta Configure has never
; been done. The receipt carries that fact, and once it is set this
; surface answers ConfigurationRefused.MetaConfigureOccurred.

Signal

[]

[ Configure.OrchestrateNexusConfiguration  Lock.LockRequest  Release.LockId  Observe.ObserveSelection ]

[ ConfigurationAccepted.ConfigurationReceipt  ConfigurationRefused.ConfigurationRejection
  Locked.Lock  Released.Lock  Observed.Observation
  LockRejected.LockRejection  ReleaseRejected.ReleaseRejection ]

[ ConfigurationPath.String
  OrdinarySocketPath.ConfigurationPath
  MetaSocketPath.ConfigurationPath
  OrchestrateNexusConfiguration.{ OrdinarySocketPath MetaSocketPath }
  MetaConfigureDone.Boolean
  ConfigurationReceipt.{ OrchestrateNexusConfiguration MetaConfigureDone }
  ConfigurationRejectionReason.[ MetaConfigureOccurred InvalidConfiguration ]
  ConfigurationRejection.{ ConfigurationRejectionReason }
  LockId.Integer
  LockName.String
  FlowId.String
  LockPath.String
  LockReason.String
  LockRequest.{ LockName FlowId Vector<LockPath> LockReason }
  Lock.{ LockId LockName FlowId Vector<LockPath> LockReason }
  LockOverlap.{ LockPath Lock }
  LockRejection.[ DuplicateName.Lock  PathOverlap.LockOverlap ]
  ReleaseRejection.[ UnknownLockId ]
  ObserveSelection.[ Locks ]
  Observation.[ Locks.Vector<Lock> ] ]
```

Sections (the ethos skill's Signal order — imports, queries, responses, types):
line 20 imports (empty), line 22 queries, lines 24-26 responses, lines 28-47
types.

The four queries, with their paired responses and typed refusals — the pairing
is not expressed in the ethos syntax (the two sections are flat lists), it is
the Nexus's dispatch in `orchestrate-nexus/src/core.rs:138-147` and
`store/transition.rs:44-112,145-171`:

| Query (ethos:22) | Payload type | Success response | Typed refusal |
|---|---|---|---|
| `Configure` | `OrchestrateNexusConfiguration` | `ConfigurationAccepted.ConfigurationReceipt` | `ConfigurationRefused.ConfigurationRejection` (reason `MetaConfigureOccurred` or `InvalidConfiguration`) |
| `Lock` | `LockRequest` | `Locked.Lock` | `LockRejected.LockRejection` (`DuplicateName.Lock` \| `PathOverlap.LockOverlap`) |
| `Release` | `LockId` (Integer) | `Released.Lock` | `ReleaseRejected.ReleaseRejection` (`UnknownLockId`) |
| `Observe` | `ObserveSelection` (`Locks`) | `Observed.Observation` (`Locks.Vector<Lock>`), repeated | none — no refusal variant exists for Observe |

Every type the ordinary contract carries (ethos:28-47):

- Aliases: `ConfigurationPath.String`; `OrdinarySocketPath.ConfigurationPath`;
  `MetaSocketPath.ConfigurationPath`; `MetaConfigureDone.Boolean`;
  `LockId.Integer`; `LockName.String`; `FlowId.String`; `LockPath.String`;
  `LockReason.String`.
- Structs: `OrchestrateNexusConfiguration.{ OrdinarySocketPath MetaSocketPath }`;
  `ConfigurationReceipt.{ OrchestrateNexusConfiguration MetaConfigureDone }`;
  `ConfigurationRejection.{ ConfigurationRejectionReason }`;
  `LockRequest.{ LockName FlowId Vector<LockPath> LockReason }`;
  `Lock.{ LockId LockName FlowId Vector<LockPath> LockReason }`;
  `LockOverlap.{ LockPath Lock }`.
- Enums: `ConfigurationRejectionReason.[ MetaConfigureOccurred InvalidConfiguration ]`;
  `LockRejection.[ DuplicateName.Lock PathOverlap.LockOverlap ]`;
  `ReleaseRejection.[ UnknownLockId ]`; `ObserveSelection.[ Locks ]`;
  `Observation.[ Locks.Vector<Lock> ]`.

Observation: the ethos file *is* the CLI's help text — `orchestrate` with no
arguments prints it (`crates/orchestrate/src/main.rs:35-39`), witnessed by
running `orchestrate` with no arguments, whose first five lines are the
comment header above.

### 1.2 The meta socket — `meta-signal-orchestrate/ethos/signal.ethos` @ `4279ad05`

Reproduced in full (10 lines):

```
; Orchestrate meta signal — the privileged configuration wire contract.
Signal
[ signal_orchestrate:[ OrchestrateNexusConfiguration ConfigurationReceipt ] ]
[ Configure.OrchestrateNexusConfiguration ReverseMetaConfiguration ]
[ Configured.ConfigurationReceipt OrdinaryConfigurationReopened.ConfigurationReceipt
  ConfigurationRejected.ConfigurationRejection PeerRefused.PeerRejection ]
[ ConfigurationRejectionReason.[ InvalidConfiguration ]
  ConfigurationRejection.{ ConfigurationRejectionReason }
  PeerUserId.Integer
  PeerRejection.{ PeerUserId } ]
```

| Query (line 4) | Payload | Success response | Typed refusal |
|---|---|---|---|
| `Configure` | `OrchestrateNexusConfiguration` (imported from `signal_orchestrate`) | `Configured.ConfigurationReceipt` | `ConfigurationRejected.ConfigurationRejection` (`InvalidConfiguration`) |
| `ReverseMetaConfiguration` | none (bare variant) | `OrdinaryConfigurationReopened.ConfigurationReceipt` | — |
| *(pre-query, any connection)* | — | — | `PeerRefused.PeerRejection { PeerUserId }` |

Types the meta contract carries: imported `OrchestrateNexusConfiguration` and
`ConfigurationReceipt` (line 3, an ethos import of the form `source:[ Type … ]`);
own `ConfigurationRejectionReason.[ InvalidConfiguration ]`,
`ConfigurationRejection.{ ConfigurationRejectionReason }`, `PeerUserId.Integer`,
`PeerRejection.{ PeerUserId }`.

`PeerRefused` is the one response no query produces: the session writes it
before reading any frame, when the connecting uid is not the socket's owner
(`orchestrate-nexus/src/transport/session.rs:98-104,125-138`).

### 1.3 The client-failure ethos — a third, non-wire ethos per CLI

Both CLIs carry a `Library`-root ethos describing failures that never reach the
wire. `crates/orchestrate/client.ethos` and
`crates/orchestrate-meta/client.ethos` are byte-identical (10 lines each):

```
; Datom-boundary failures for the ordinary Orchestrate client.
Library
[ datom_codec:Error ]
[ SocketPath.String
  TransportError.String
  Unreachable.{ SocketPath TransportError }
  ClientFailure.[ Unreadable.Error
                  Unreachable.Unreachable ] ]
[]
[]
```
(the meta copy's line 1 reads "privileged" for "ordinary")

---

## 2. The generated Rust

### 2.1 Which crate the ethos generates into

Each wire repo is a single crate whose `src/generated/signal.rs` is the
projection of its own `ethos/signal.ethos`, committed and held fresh by a
build script.

- `signal-orchestrate/src/lib.rs` (@`e7221190`, 3 lines):
  `pub mod generated; pub use generated::signal::*;` and
  `pub const ETHOS: &str = include_str!("../ethos/signal.ethos");`
- `meta-signal-orchestrate/src/lib.rs` — the same shape.
- The CLIs generate their `client.ethos` into
  `crates/orchestrate/src/generated/client.rs` and
  `crates/orchestrate-meta/src/generated/client.rs` via `build.rs`
  (`crates/orchestrate/build.rs:1-19`), which regenerates and asserts
  byte-equality: `assert_eq!(generated, committed, "committed client.rs is stale");`
  (`build.rs:18`).

### 2.2 The Query/Response enums as generated

`/git/github.com/LiGoldragon/signal-orchestrate/src/generated/signal.rs`
(the committed file at `e7221190`; the working tree differs — see §7.1):

```rust
pub enum Query {
    Configure(OrchestrateNexusConfiguration),
    Lock(LockRequest),
    Release(LockId),
    Observe(ObserveSelection),
}
pub enum Response {
    ConfigurationAccepted(ConfigurationReceipt),
    ConfigurationRefused(ConfigurationRejection),
    Locked(Lock),
    Released(Lock),
    Observed(Observation),
    LockRejected(LockRejection),
    ReleaseRejected(ReleaseRejection),
}
```
(working-tree line numbers 101-118; the committed text is identical apart from
the derive block, §7.1)

`/git/github.com/LiGoldragon/meta-signal-orchestrate/src/generated/signal.rs:37-52`:

```rust
pub enum Query {
    Configure(signal_orchestrate::OrchestrateNexusConfiguration),
    ReverseMetaConfiguration,
}
pub enum Response {
    Configured(signal_orchestrate::ConfigurationReceipt),
    OrdinaryConfigurationReopened(signal_orchestrate::ConfigurationReceipt),
    ConfigurationRejected(ConfigurationRejection),
    PeerRefused(PeerRejection),
}
```

Observed: imported types are written fully qualified with no `use`, exactly as
the ethos skill states.

### 2.3 The derive and feature that give them datom kinds

Every generated struct and enum in a Signal root carries, verbatim
(`meta-signal-orchestrate/src/generated/signal.rs:2-7`, and the committed
signal-orchestrate file):

```rust
#[rustfmt::skip]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq)]
#[cfg_attr(
    feature = "datom",
    derive(datom_codec::Datomizable, datom_codec::Compositional)
)]
```

Aliases carry no derive (`signal.rs:37-46`: `pub type LockId = i64;` etc.),
bearing the kinds through the type they name.

The feature gate is honoured on both sides, observed in the manifests:

- CLI enables it — `crates/orchestrate/Cargo.toml:20`:
  `signal-orchestrate = { workspace = true, features = ["datom"] }`
- Nexus does not — `crates/orchestrate-nexus/Cargo.toml:41`:
  `signal-orchestrate.workspace = true`, under the comment at lines 29-32:
  "No `datom-codec` and no `protos`: the Nexus thinks in typed values and never
  textualizes." A Nix check named `datom-free-nexus`
  (`orchestrate/flake.nix:210-214`) witnesses it.

The `Library` root generates unconditionally, not behind a feature
(`crates/orchestrate/src/generated/client.rs:7,13`):
`#[derive(datom_codec::Datomizable, datom_codec::Compositional, Clone, Debug, PartialEq)]`.

Every generated file opens with
`#![allow(dead_code, non_camel_case_types, non_snake_case)]` (line 1 of each)
and every item bears `#[rustfmt::skip]`.

---

## 3. The Nexus process

### 3.1 The executable and how it starts

Binary `orchestrate-nexus` from `crates/orchestrate-nexus/src/main.rs`
(declared at `crates/orchestrate-nexus/Cargo.toml:14-16`). Two other binaries
exist in the same crate: `orchestrate-upgrade-preflight` (lines 18-20) and
`orchestrate-relocate` (lines 25-27), the latter annotated at lines 22-24 as
"Not a client and not a CLI in the Nexus sense: it speaks no signal, opens no
socket, and reaches no Nexus."

**No arguments.** `src/defaults.rs:30-33`:

```rust
fn from_process() -> Result<Self, DefaultConfigurationError> {
    if env::args_os().nth(1).is_some() {
        return Err(DefaultConfigurationError::StartupArguments);
    }
```
with `#[error("accepts zero arguments")]` at `defaults.rs:109`.

**Default configuration, owned by the executable** (`defaults.rs:11-14`):

```rust
const STATE_DIRECTORY: &str = "orchestrate-nexus";
const STORE_FILE: &str = "orchestrate-nexus.sema";
const ORDINARY_SOCKET_FILE: &str = "orchestrate.sock";
const META_SOCKET_FILE: &str = "orchestrate-meta.sock";
```

Resolved from XDG roots (`defaults.rs:34-51,74-93`): store at
`$XDG_STATE_HOME/orchestrate-nexus/orchestrate-nexus.sema`, falling back to
`$HOME/.local/state`; sockets at
`$XDG_RUNTIME_DIR/orchestrate-nexus/{orchestrate.sock,orchestrate-meta.sock}`.
`XDG_RUNTIME_DIR` is required (`MissingRuntimeDirectory`, line 111); relative
paths are refused (lines 95-104).

**Sema store location and the new/populated rule** —
`src/store/mod.rs:61-170`. The store is opened by `sema_engine::Engine::open`
with `SCHEMA_VERSION` (line 71-74). A store with no metadata row is *seeded*
from the executable defaults (`mod.rs:84` → `seed_metadata`, lines 188-227,
`ConfigurationState::from_default(StoredConfiguration::from_public(defaults))`
at line 211); a populated one *resumes* from the stored row (`mod.rs:85`). The
configuration handed back to `main` is the store's, not the defaults'
(`mod.rs:156`: `let configuration = state.desired_configuration().clone().into_public();`).

**Start sequence** (`src/main.rs:8-31`): read defaults → open the store → build
a two-worker multi-thread Tokio runtime → `TransportRuntime::bind(configuration, store)`
→ print `orchestrate-nexus ready` → `serve_until(Termination::asked()?)`. The
two-worker choice is argued in a comment at `main.rs:15-20`: "the core is one
actor and its durable step is synchronous, so one worker runs that step and one
keeps accepting while it does."

### 3.2 The sockets it opens

`src/transport/mod.rs:61-80` (`impl Binding for TransportRuntime`): both paths
are **claimed before either is bound**, then the ordinary is bound with
`SocketAuthority::Ordinary` and the meta with `SocketAuthority::Privileged`
(lines 67-70), then `store.situate(...)` records where it actually bound
(lines 71-74), and only then is the core founded around the store (line 78).

A claim is an advisory `flock` on a `<socket>.claim` file beside the socket
(`src/transport/socket.rs:56-78`), held for the life of the process
(`socket.rs:36-45`). The reasoning is at `socket.rs:8-21`: connecting to the
socket answers a different question than "does this path belong to somebody
else". A claim contention yields `TransportError::SocketAlreadyActive`.

Modes come from `nexus::SocketAuthority` (`nexus/src/authority.rs:33-46`):
`Ordinary => 0o660`, `Privileged => 0o600`, set after bind because a Unix
socket takes permissions from the umask (`socket.rs:95-100`). Witnessed on the
live sockets in §0.2.

**Observed divergence, witnessed:** the running Nexus bound
`meta-orchestrate.sock`, while `defaults.rs:14` names `orchestrate-meta.sock`.
The rename landed in commit `2266b06` (2026-09-12, "Make Nexus Core the actor,
claim socket paths, and refuse a carried store"), whose diff shows
`-const META_SOCKET_FILE: &str = "meta-orchestrate.sock";` /
`+const META_SOCKET_FILE: &str = "orchestrate-meta.sock";`. Because a populated
store resumes its own persisted configuration (§3.1), the new default never
took effect on this host. Consequence, witnessed by running
`orchestrate-meta 'ReverseMetaConfiguration'`:

```
Unreachable.{ /run/user/1001/orchestrate-nexus/orchestrate-meta.sock «Unix socket I/O failed: No such file or directory (os error 2)» }
```

The installed meta CLI cannot reach the running Nexus. (Inferred, not observed:
the fix would need a meta `Configure`, which is reachable only over the meta
socket — unless ordinary `Configure` is still open. Whether `MetaConfigureDone`
is set on this store is **unknown**: reading it requires issuing a `Configure`,
which mutates, and this flow did not.)

### 3.3 The actor structure inside

One Kameo actor, and the file says so — `src/core.rs:4-9`:

> "The core is an actor, and it is the only actor in the Nexus. What an actor
> is for is owning exclusive mutable state and serialising access to it, so the
> boundary is drawn at the state: one lock table is one unit of consistency, so
> it gets one actor, and that actor owns the store outright."

and `core.rs:11-16`:

> "Sockets are not actors and sessions are not actors. A listener is a task and
> a connection is a task holding a reference to this one actor… What separates
> the two doors is not the actor: it is which message type the session on the
> other side of them can construct."

Structure, all in `core.rs`:

- `struct NexusCore { store: OrchestrateStore, announcements: broadcast::Sender<Observation> }` (105-108)
- `impl Actor for NexusCore { type Args = OrchestrateStore; type Error = StoreError; }` (115-128); `on_start` creates the broadcast channel (121-127). There is deliberately no `on_stop` (110-114).
- `struct FoundedCore { core: ActorRef<NexusCore>, ended: JoinHandle<…> }` (65-68), built by `trait Founding` (71-78) with `PreparedActor::new(mailbox::bounded(MAILBOX_CAPACITY))` (82-83) and stopped by `settled()` → `stop_gracefully()` then await (98-101).
- Constants: `ANNOUNCEMENT_BACKLOG: usize = 64` (50), `MAILBOX_CAPACITY: usize = 64` (56).

Four Kameo `Message` impls on `NexusCore`:

| Message | Reply | Lines |
|---|---|---|
| `OrdinaryQuery` (`signal_orchestrate::Query`) | `Result<OrdinaryResponse, StoreError>` | 130-158 |
| `MetaQuery` (`meta_signal_orchestrate::Query`) | `Result<MetaResponse, StoreError>` | 160-174 |
| `Attending { selection }` | `Result<Attendance, StoreError>` | 176-206 |
| `Overtaking { selection }` | `Result<Observation, StoreError>` | 208-225 |

The two sockets are two doors onto one actor; the privilege separation is that
an ordinary session can only construct `signal_orchestrate::Query` and a meta
session only `meta_signal_orchestrate::Query` — a type-level, not a
runtime-check, separation.

Tasks (not actors): `TransportRuntime::serve_until` runs one `tokio::select!`
loop over shutdown, the two listeners' `accept()`, and a `JoinSet` of
connections (`transport/mod.rs:184-241`). Each accepted stream is spawned into
the `JoinSet` as a `Session` (lines 205-226).

### 3.4 One request, socket frame to reply

Path for `orchestrate 'Lock.{ … }'`, cited step by step:

1. **Accept** — `transport/mod.rs:205-215`: the ordinary listener yields a
   stream; `Session::opened(stream, authority, owner)` and the session is
   spawned with a clone of `ActorRef<NexusCore>`.
2. **Admit** — `transport/session.rs:146-150`: `self.admitted::<OrdinaryResponse>()`
   reads `SO_PEERCRED` (`socket.rs:123-127`, `peer_cred()?.uid()`) and asks
   `SocketAuthority::admits(peer_user, owner)` (`nexus/src/authority.rs:41-46`).
   `Ordinary => true` always. A refusal is a value of the contract the socket
   bears — `trait Refusing` (`session.rs:94-110`); `OrdinaryResponse::peer_refusal`
   returns `None`, "and silence is what the ordinary contract can honestly say"
   (session.rs:89-93).
3. **Read the frame** — `session.rs:58-67`, `trait Exchanging::receive`:
   `self.stream.read_frame(FrameCapacity::default())` then
   `Signal::<T>::from(Vec::from(body)).restore()`, mapping any failure to
   `TransportError::Archive`. Framing is disclaimed as signal's own at
   `session.rs:3-5`: "Framing is `signal`'s and only `signal`'s: this Nexus
   owns no length prefix of its own."
4. **Decode** — `Restorable<T>::restore` is
   `rkyv::from_bytes::<T, Error>(self.bytes())` (`signal/src/portable.rs:64-73`),
   which is the validating path (`CheckBytes<HighValidator<…>>` bound, line 68).
5. **Dispatch** — `session.rs:151-157`: `Observe` branches to `subscribe`;
   every other query goes `core.ask(query).await.delivered()?`. `delivered()`
   (`transport/mod.rs:248-263`) separates "the store refused" from "the core was
   not there to ask": `HandlerError → Store`, `MailboxFull|Timeout → CoreOverloaded`,
   `ActorNotRunning|ActorStopped|ActorRestarting → CoreStopped`.
6. **Handle** — `core.rs:130-158`: match on the `Query` variant into
   `ordinary_configure` / `lock` / `release` / `observe`.
7. **Mutate state** — `store/transition.rs:44-83` (`impl Locks for OrchestrateStore`):
   normalize the request (line 46), scan `current_locks()` for a duplicate name
   (48-51) or an overlapping path (52-60) returning the typed `LockRejected`,
   read the single allocator row (62-69), then one atomic commit asserting the
   `StoredLock` and mutating the allocator (75-80), answering
   `OrdinaryResponse::Locked(lock)` (81).
8. **Announce** — `core.rs:148-155`: if the response is `Locked` or `Released`,
   `self.announcements.send(self.store.observe(ObserveSelection::Locks)?)`.
9. **Encode and write** — `session.rs:69-78`, `Exchanging::answer`:
   `response.signalize()` (`portable.rs:40-47`,
   `rkyv::to_bytes::<Error>(self)?.to_vec()`) then
   `self.stream.write_frame(&signal, FrameCapacity::default())`.

Traits and kinds involved, named: `signal::Signalizable`, `signal::Restorable<T>`,
`signal::ByteViewable`, `signal::Framable`, `signal::FrameReading` /
`FrameWriting` (blocking, used by the CLI) and `AsyncFrameReading` /
`AsyncFrameWriting` (used by the Nexus session), `signal::Capacious`,
`signal::LengthDeclaring`; crate-local `Exchanging`, `Admitting`, `Refusing`,
`ServingOrdinary`, `ServingMeta`, `Subscribing`, `Opening`, `Delivered<Effect>`,
`Binding`, `Bounds`, `Serving`, `StopsOnSignal`, `Recording`, `Claiming`,
`Claimable`, `Attributable`, `OwnsSocket`; domain traits `Locks`, `Releases`,
`Observes`, `IdentifiesLock` (`ordinary.rs:16-40`), `Configures`
(`transition.rs:120-131`), `OpensStore`, `SeedsMetadata`, `KeepsMetadata`,
`Situates`, `Relocates`, `Validates`, `AnswersMeta`, `Founding`; and from the
`nexus` library `Permissive`, `Configurable`, `Identifying`, `Situated`,
`Situating`, `Relocating`.

Observed: `IdentifiesLock` (`ordinary.rs:32-39`) is a single-method trait on a
data-bearing type, `Lock` — the shape the nexus skill warns about ("One type
implementing many single-function traits is one trait not yet seen") is
present but in the singular here.

---

## 4. The CLI

### 4.1 The two binaries

- `orchestrate` — `crates/orchestrate/src/main.rs` (183 lines), bin declared at
  `crates/orchestrate/Cargo.toml:12-14`; module docstring line 1: "Datom edge
  client for the ordinary Orchestrate Signal."
- `orchestrate-meta` — `crates/orchestrate-meta/src/main.rs` (183 lines), line 1:
  "Datom edge client for the privileged Orchestrate Signal."

They are structurally identical: the same `Invocation`, `Client`, `Querying`,
`DatomText`, `SignalConnection`, `Connecting`, `Exchanging`, `TransportError`
types and traits, differing only in which contract crate they import
(`signal_orchestrate` vs `meta_signal_orchestrate`, line 10 vs line 8), which
environment variable names the socket, and the program name in the error
prefix.

Socket from the environment, no flag:
- `orchestrate/src/main.rs:62-63`: `env::var("ORCHESTRATE_SOCKET")` else
  `"ORCHESTRATE_SOCKET is required"`.
- `orchestrate-meta/src/main.rs:62-63`: `env::var("ORCHESTRATE_META_SOCKET")`.

The installed wrappers supply them (witnessed, `cat $(which orchestrate)`):
```
export ORCHESTRATE_SOCKET="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/orchestrate-nexus/orchestrate.sock"
exec "/nix/store/6ynfv0hywpwg8gpapyfh7zn0yqzdg52z-orchestrate-0.35.0/bin/orchestrate"  "$@"
```
and the meta wrapper the same with `orchestrate-meta.sock` — the path that does
not exist (§3.2).

### 4.2 The one-positional-datom-argument rule as implemented

`crates/orchestrate/src/main.rs:24-31` (identical at
`crates/orchestrate-meta/src/main.rs:24-31`):

```rust
fn from_process() -> Result<Self, String> {
    let arguments = env::args().skip(1).collect::<Vec<_>>();
    match arguments.as_slice() {
        [] => Ok(Self::Describe),
        [source] if !source.starts_with("--") => Ok(Self::Query(source.clone())),
        _ => Err("accepts exactly one inline Datom query and no flags".to_owned()),
    }
}
```

Three arms only: zero arguments describe, exactly one non-`--` argument is the
datom, anything else is the error. Witnessed: `orchestrate --help` and
`orchestrate a b` both print
`orchestrate: accepts exactly one inline Datom query and no flags`.

`Describe` (`main.rs:35-39`) prints the contract ethos then the client ethos:
```rust
println!("{}", signal_orchestrate::ETHOS.trim());
println!("{}", include_str!("../client.ethos").trim());
```
— the ethos skill's "point at the object and its ethos prints", witnessed.

### 4.3 Datom to signal: protosize, datomize, compose

**Inbound (text → typed → signal)**, `main.rs:74-96`:

```rust
let mut potential = Potential::<Query>::from(source);
let mut budget = Budget {
    remaining: 10_000,
    reader: ReaderBudget { remaining: 10_000 },
    depth: 0,
    maximum_depth: 256,
};
let result = potential
    .actualize(&mut budget)
    .map_err(ClientFailure::Unreadable)
    .and_then(|query| self.query(&query));
```

`Potential::<Query>::from(text)` then `actualize(&mut budget)` is exactly the
datom skill's `let query: Query = Potential::<Query>::from(text).actualize(&mut budget)?;`
— the compose direction, which walks `Query`'s positions through
`datom_codec::Compositional` (derived on the generated types under the `datom`
feature, §2.3). A failure is `ClientFailure::Unreadable(datom_codec::Error)`,
the variant declared in `client.ethos:7`.

**Outbound (typed → text)**, `main.rs:117-128`:

```rust
trait DatomText { fn datom_text(&self) -> String; }
impl<T> DatomText for T where T: Datomizable<Output = Datom> {
    fn datom_text(&self) -> String {
        self.datomize(Vec::new()).protosize().textualize()
    }
}
```

The datom skill's `response.datomize(Path::new()).protosize().textualize()`,
with `Vec::new()` as the empty path. Both the success response and the
`ClientFailure` go through it (`main.rs:87-94`): success to stdout with
`ExitCode::SUCCESS`, failure to stderr with `ExitCode::FAILURE`. So the
*textualization of the reply* is one `Datomizable → Protosizable → Textualizable`
chain, and it lives entirely in the client — the Nexus does none of it.

Witnessed round trip, `orchestrate 'Observe.Locks'` (excerpt):

```
Observed.Locks.[ { 937 C6CraneGitBundles 542442 [ /home/li/wt/… ] «Store finite Crane Git replay artifacts» } … ]
```

Positional, no field names, guillemets where the reason has spaces, bare runs
where it has none — the ethos type supplies every name.

**The exchange**, `main.rs:98-114` and `146-163`:

```rust
fn query(&self, query: &Query) -> Result<Response, ClientFailure> {
    let exchange = query
        .signalize()
        .map_err(|_| TransportError::Archive)
        .and_then(|signal| SignalConnection::connect(&self.socket_path)?.exchange(&signal))
        .and_then(|bytes| Signal::<Response>::from(bytes).restore().map_err(|_| TransportError::Archive));
```

with `exchange` being "One framed query out, one framed reply in" over a
blocking `std::os::unix::net::UnixStream` (`main.rs:141-142, 158-162`), and a
transport failure collapsing into
`ClientFailure::Unreachable(Unreachable { socket_path, transport_error })`
(`main.rs:108-113`) — the client-ethos variant, so even a dead socket answers
in datom.

---

## 5. The wire

### 5.1 Frame format

`signal/src/frame.rs` @ `8f9a0deb`. Module docstring, lines 1-7:

> "The Signal wire frame: a four-byte big-endian length prefix and a body. One
> implementation, shared by every Nexus. Before this crate held it, Orchestrate
> hand-rolled the prefix in its transport and Lojix took it from
> `triad-runtime`'s `LengthPrefixedCodec`; the two disagreed on byte order.
> Big-endian is kept…"

- `pub const FRAME_PREFIX_BYTES: usize = 4;` (line 16)
- `pub const MAXIMUM_SIGNAL_BYTES: usize = 8 * 1024 * 1024;` (line 19) — 8 MiB,
  the `FrameCapacity::default()` both the CLI and the Nexus pass.
- Prefix read: `u32::from_be_bytes(self.bytes) as usize` (line 122).
- Frame written: `length.to_be_bytes()` then the body (lines 139-142).
- Over-capacity is a typed `FrameError::BodyTooLarge { found, capacity }` (43-44).

The body is one rkyv archive (`signal/src/portable.rs:19-23`,
`struct Signal<T> { bytes: Vec<u8>, target: PhantomData<fn() -> T> }`),
serialized by `Signalizable::signalize` → `rkyv::to_bytes` (40-47) and restored
by `Restorable<T>::restore` → `rkyv::from_bytes` with a `CheckBytes` validator
bound (64-73). rkyv features, pinned identically in every manifest
(`orchestrate/Cargo.toml:24`):
`default-features = false, features = ["std", "bytecheck", "little_endian", "pointer_width_32", "unaligned"]`.

### 5.2 Handshake payload

**None, at the pinned revision.** `signal/src/lib.rs:9-10` @ `8f9a0deb` says so
directly:

> "The protocol layered on top of the rkyv archive is not decided; nothing here
> anticipates it."

The files at that revision are `frame.rs`, `portable.rs`, `taxonomy.rs`,
`transport.rs`, `generated/`. There is no `accord.rs` and no `exchange.rs`.
The first frame a session reads is the `Query` itself
(`session.rs:151`, `223`); the only thing that precedes it is the kernel-level
`SO_PEERCRED` admission check, which puts no bytes on the wire (and, on the
meta socket, may put one `PeerRefused` frame on it before any query is read).

### 5.3 Router or wrapping enum

**Not present on this edge.** `signal/ethos/signal.ethos` @ `8f9a0deb` (17
lines) declares a cross-component *taxonomy* — `ComponentKind` (with an
`Orchestrate` variant), `ObjectDigest`, `StandardSocket`,
`AuthorizedObjectReference`, `ComponentClassification` — but no wrapping enum
over signal objects and no handshake type. The root type on each socket is that
socket's own contract `Query`, chosen by which socket the frame arrived on
(`session.rs:151` receives `OrdinaryQuery`, `session.rs:223` receives
`MetaQuery`); nothing on the wire says which. Inference: the socket *is* the
discriminator today, so a router would need the wrapping enum
`Vision/nexus.md:66-72` describes, which does not exist yet.

---

## 6. Subscription

### 6.1 How `Observe.Locks` works today

**Nexus side — a real subscription.** `session.rs:152` routes `Observe` to
`subscribe` (`session.rs:170-211`):

```rust
let attendance = core.ask(Attending { selection: selection.clone() }).await.delivered()?;
let mut announcements = attendance.announcements;
self.answer(&OrdinaryResponse::Observed(attendance.opening)).await?;
loop {
    let observation = match announcements.recv().await {
        Ok(observation) => observation,
        Err(RecvError::Lagged(_)) => core.ask(Overtaking { selection: selection.clone() }).await.delivered()?,
        Err(RecvError::Closed) => return Ok(()),
    };
    match self.answer(&OrdinaryResponse::Observed(observation)).await { … }
}
```

The opening state and the channel subscription are taken in **one** step of the
core (`core.rs:193-206`, `Message<Attending>`), argued at `core.rs:182-187`:
"Both halves are taken in one step of the core, so nothing can commit between
the two. A subscriber therefore never misses a change and never sees the same
one twice." A lagged subscriber is re-sent the current state via `Overtaking`
(`core.rs:215-225`), not dropped. A peer closing the connection is an ordinary
end, not a failure (`session.rs:202-208`).

Changes are announced only for `Locked` and `Released` (`core.rs:148-155`) —
so a `Configure` that changed the socket paths produces no announcement, which
is correct for an `ObserveSelection::Locks` subscription and is the only
selection that exists.

**CLI side — one frame, then exit.** `orchestrate/src/main.rs:152-162`, with
the reason stated in the doc comment (lines 152-157):

> "Exactly one reply is read even where the Nexus would go on writing — an
> Observe opens a subscription there. A CLI that takes one argument and prints
> one value ends at the state on open; dropping the connection is how it
> unsubscribes."

So the subscription is implemented on the server and truncated at the client.
The orchestrate skill already records this (`.claude/skills/orchestrate/SKILL.md`):
"The current `orchestrate` CLI reads one `Observed` frame and exits; it does not
yet hold the connection open to receive the later ones, so re-issuing
`Observe.Locks` is today's only way to see a change, not the designed one."

### 6.2 Versus the designed subscription

`Vision/nexus.md:117-125`:

> "State is observed by subscription: the subscriber receives the state on
> open, then each change as it happens."
> "Polling is forbidden; a correct system goes quiet when nothing changes."

Observation: the Nexus half satisfies this exactly. The CLI half does not, and
every consumer that wants to see a change therefore re-issues `Observe.Locks` —
which is polling, performed by callers rather than by the client. No token and
no `Unwatch` exist, as the ethos header (`ethos/signal.ethos:10-11`) states:
"The subscription is the connection, so there is no token and no Unwatch: a
peer that stops reading has unsubscribed."

---

## 7. Gaps — observation versus vision text

Each entry gives the observation, then the vision or skill text it sits beside.
No verdicts.

### 7.1 The derive name in the working tree

*Observation.* `signal-orchestrate/src/generated/signal.rs` **in the working
tree** emits
`#[cfg_attr(feature = "datom", derive(datom_codec::Datomizable, datom_codec::Composing))]`
(lines 10, 19, 26, …) and adds `Eq, Hash` to the rkyv derive. The **committed**
file at `e7221190` — the one Orchestrate builds — emits
`datom_codec::Compositional` with no `Eq, Hash`.

*Vision text.* `Vision/ethos.md:251-256`: "Ethos Zero emits `Datomizable` and
`Compositional` on every struct and enum it generates". The `ethos` skill's
example likewise reads `datom_codec::Compositional`, and the `datom` skill names
the trait `Compositional` in `pub trait Compositional: Sized`.

*Note.* `meta-signal-orchestrate` (clean) and the two `client.rs` files still
emit `Compositional`. The three crates are therefore split across two names of
the same kind, pending the in-flight 4.0.0 work.

### 7.2 No handshake, no contract digest on the wire (pinned) — one is being built

*Observation.* §5.2: nothing precedes the `Query` frame at `8f9a0deb`.

*Vision text.* `Vision/nexus.md:66-72`: "Signals cross the network through a
router. The router tells signal types apart by an enum that wraps the objects,
held in the signal repository, which every component depends on. That repository
also holds what every signal needs in common — the handshake payload among it."
`Vision/signal.md:40-43`: "Signal is portable rkyv plus whatever protocol is
standardized on top of it. The protocol is to be decided."

*In flight, not deployed.* The dirty `signal-orchestrate/src/lib.rs` adds
`impl signal::Contracted for Query { const CONTRACT_SOURCE: &'static str = ETHOS; }`
with the comment "two peers built from different sources refuse each other
rather than negotiate — there is no version range, no minor tolerance and no
compatibility path", and the local `signal` checkout at `66e7b153` carries
`src/accord.rs` and `src/exchange.rs`. None of it is pinned by Orchestrate.

### 7.3 The subscription ends at the CLI

*Observation.* §6.1: the Nexus streams; the CLI reads one frame and exits.

*Vision text.* `Vision/nexus.md:119-125` (subscription, polling forbidden), and
the `nexus` skill: "State is observed by subscription… Polling is forbidden; a
correct system goes quiet when nothing changes."

### 7.4 The Sema records are hand-written Rust, not an Ethos Sema root

*Observation.* `crates/orchestrate-nexus/src/store/record.rs` (216 lines)
declares `StoredConfiguration`, `StoredMetadata`, `StoredSituation`,
`StoredRelocation`, `StoredLock`, `StoredAllocator` as hand-written Rust with
`#[derive(Archive, RkyvSerialize, RkyvDeserialize, …)]` and `impl EngineRecord`
(e.g. lines 35-52). Table names are string constants (lines 17-28). No `.ethos`
file with a `Sema` root exists anywhere in the orchestrate repository (only two
`Library`-root `client.ethos` files).

*Vision text.* `Vision/sema.md:5-14`: "Sema is the database engine of a Nexus,
authored in Ethos so the stored types are visible; its root, Sema, declares
record types." The `ethos` skill: "Three roots: Library, Signal, Sema. Signal
gives a Nexus its main types and Sema its database types."

### 7.5 The executable's default meta socket name and the persisted one disagree

*Observation.* §3.2, witnessed: the live Nexus serves `meta-orchestrate.sock`;
`defaults.rs:14` and the installed wrapper both say `orchestrate-meta.sock`;
`orchestrate-meta` answers `Unreachable`.

*Vision text.* `Vision/nexus.md:76-81`: "On start it looks for its Sema database
at the default location: a database that exists holds the configuration; a
database created new is seeded with the defaults." The code follows this
exactly (`store/mod.rs:83-87,156`) — the persisted value wins, which is the
designed behaviour; the divergence is between the persisted value and the
*client wrapper's* hard-coded path, which no vision text governs.
`Vision/orchestrate.md:4-7`: "Orchestrate is deployed unconditionally, in the
home, for every user. Its meta binary is part of it; a deployment without
meta-orchestrate is wrong." Observed: the meta binary is deployed and cannot
reach its Nexus.

### 7.6 The wire carries storage-shaped vocabulary in one place

*Observation.* `ConfigurationReceipt.{ OrchestrateNexusConfiguration MetaConfigureDone }`
and `ConfigurationRejectionReason.[ MetaConfigureOccurred InvalidConfiguration ]`
on the **ordinary** contract (`ethos/signal.ethos:32-34`) expose whether a
privileged configure has ever been done — a fact about the Nexus's own metadata
tree.

*Skill text.* The `nexus` skill: "Storage classification vocabulary never
appears on the public wire — what a peer may ask is domain language, not
database language."

*Counter-reading (disconfirming).* `Vision/nexus.md:85-92` explicitly designs
this fact as wire-relevant: "In it a type records whether the meta Configure was
ever done; that record is reversed only on the meta socket, and while it is
unset Configure is accessible on the ordinary socket." So `MetaConfigureDone`
may be domain language for the configuration lifecycle rather than database
language. Recorded as an open reading, not a gap resolved.

### 7.7 `Observe` has no typed refusal

*Observation.* §1.1: `Observe` is the one query with no rejection variant. A
failure to subscribe surfaces as a `TransportError` and an ended connection
(`session.rs:180-185` via `delivered()?`), not as a frame.

*Skill text.* The `nexus` skill: "Every surface answers with typed replies,
including a typed refusal — errors are vocabulary, not strings."

### 7.8 `fn main` aside, the free-function rule holds; one trait sits on a zero-argument shape

*Observation.* Every verb in the three crates is a trait method; the only free
functions are the three `fn main()`s and `build.rs`'s `fn main()`. Two check
scripts enforce it in the wire repos (`signal-orchestrate/checks/no-free-functions.sh`,
`checks/no-inherent-methods.sh`). `IdentifiesLock` (`ordinary.rs:32-39`) is one
single-method trait on `Lock`.

*Skill text.* The `nexus` skill: "`fn main()` is the only production free
function"; "One type implementing many single-function traits is one trait not
yet seen."

### 7.9 Exception noted at its site, as the skill asks

*Observation.* `session.rs:89-93` names an exception explicitly: "The exception
taken here: `None` is silence, and silence is what the ordinary contract can
honestly say." `Cargo.toml:22-24` in orchestrate-nexus names another: the
`orchestrate-relocate` binary "Not a client and not a CLI in the Nexus sense".

*Skill text.* The `nexus` skill: "Exceptions are permitted… but each exception
is noted at the site where it is taken." Observed: followed.

---

## 8. Skills and vision touched

| Part of the anatomy | Authored skill | Vision topic |
|---|---|---|
| The ethos files, roots, sections, sweet form, derives | `/git/github.com/LiGoldragon/Curriculum/skills/ethos.md` (read as `/home/li/primary/.claude/skills/ethos/SKILL.md`) | `/home/li/primary/Vision/ethos.md` — esp. §"Every declared type bears both kinds" (251-264) and §"The datom kinds are compiled in only where text is spoken" (266-283) |
| Query/Response as the Signal root's first two sections | `Curriculum/skills/ethos.md` | `/home/li/primary/Vision/signal.md:14-28` ("A Signal declares queries and responses; input and output are too low-level for it") |
| The Nexus whole: sockets, core, default clients, actors, subscription | `Curriculum/skills/nexus.md` (`.claude/skills/nexus/SKILL.md`) | `/home/li/primary/Vision/nexus.md` (all 125 lines; §Sockets 33-39, §Default clients 41-49, §Configuration 74-81, §First configuration 83-92, §Actors 107-110, §Observation by subscription 117-120, §Polling is forbidden 122-125) |
| Why the Nexus has the shape it has | `Curriculum/skills/nexus-rationale.md` | `/home/li/primary/Vision/nexus.md` |
| The wire: rkyv, framing, portability | `Curriculum/skills/nexus.md` (§Signal — the wire format) | `/home/li/primary/Vision/signal.md:7-12, 40-43` |
| The CLI's one datom argument, textualize/compose | `Curriculum/skills/datom.md` (`.claude/skills/datom/SKILL.md`) | `/home/li/primary/Vision/datom.md` §"The interface shape" (190-211), §"From text and back" (151-161) |
| The datom text itself: positional, guillemets, bare runs | `Curriculum/skills/datom.md` | `/home/li/primary/Vision/datom.md` §Syntax (48-109), §Strings (34-47) |
| The protos substrate under datom (`protosize`, `textualize`) | `Curriculum/skills/protos.md` | `/home/li/primary/Vision/protos.md` |
| The Sema store | *(no dedicated skill in the listing)* | `/home/li/primary/Vision/sema.md` (15 lines) |
| Using the ordinary socket in practice | `Curriculum/skills/orchestrate.md` (`.claude/skills/orchestrate/SKILL.md`) | `/home/li/primary/Vision/orchestrate.md` (12 lines) |
| Lock etiquette between flows | `Curriculum/skills/edit-coordination.md` | `/home/li/primary/Vision/orchestrate.md` |
| Relaying these findings as claims, not verdicts | `Curriculum/skills/behavior.md` | — |

In-repository prose not in `Vision/` that documents the same anatomy:
`/git/github.com/LiGoldragon/orchestrate/ARCHITECTURE.md`,
`/git/github.com/LiGoldragon/signal-orchestrate/ARCHITECTURE.md`,
`/git/github.com/LiGoldragon/signal/DESIGN.md` and `ARCHITECTURE.md` (the last
read only as a file listing at `8f9a0deb`, not as content).

---

## 9. What is observed, inferred, and unknown

**Observed** (read in a file, or witnessed by running a command): every ethos
text and generated enum in §§1-2; every code path in §§3-6; the running process,
its two sockets and their modes, the `.sema` file; `orchestrate` with no
arguments printing the ethos; `orchestrate --help` and `orchestrate a b`
refusing; `orchestrate 'Observe.Locks'` returning a populated
`Observed.Locks.[ … ]`; `orchestrate-meta 'ReverseMetaConfiguration'` returning
`Unreachable`; the `META_SOCKET_FILE` rename in commit `2266b06`.

**Inferred** (reasoned from the observed, not witnessed): that the live store
was seeded before commit `2266b06` and so persists the old meta socket name;
that the socket is today's only discriminator between the two contracts, so a
router would require a wrapping enum that does not exist; that the in-flight
`signal-orchestrate` 4.0.0 work is a greeting/exchange layer.

**Unknown** (not established, and deliberately not probed because probing
mutates): whether `MetaConfigureDone` is set on the live store, and therefore
whether ordinary `Configure` is still open as a way to repair the meta socket
path; what `signal` at `66e7b153` does in `accord.rs`/`exchange.rs` beyond the
names of the files; whether the `datom-free-nexus` and `no-free-functions`
checks currently pass (the flake was read, not run).

**Method.** Files were read at the revisions named in §0; where a checkout was
dirty or ahead of its pin, the pinned revision was read through `git show`.
Four commands were run against the live system: `ps`, `ls`, `orchestrate`
(no arguments, `--help`, `a b`, `Observe.Locks`) and `orchestrate-meta`
(`ReverseMetaConfiguration`, which failed to connect and so mutated nothing).
Nothing was written outside this file, and no Lock was taken or released.

---

## Sources

Revisions as in §0.

**Ethos and generated Rust**
- `/git/github.com/LiGoldragon/signal-orchestrate/ethos/signal.ethos` @ `e7221190`, lines 1-47 (and the dirty working-tree version, lines 1-62)
- `/git/github.com/LiGoldragon/signal-orchestrate/src/generated/signal.rs` (committed and working tree), lines 1-118
- `/git/github.com/LiGoldragon/signal-orchestrate/src/lib.rs` @ `e7221190` and its working-tree diff
- `/git/github.com/LiGoldragon/signal-orchestrate/Cargo.toml`, lines 1-18 and its working-tree diff
- `/git/github.com/LiGoldragon/meta-signal-orchestrate/ethos/signal.ethos`, lines 1-10
- `/git/github.com/LiGoldragon/meta-signal-orchestrate/src/generated/signal.rs`, lines 1-52
- `/git/github.com/LiGoldragon/orchestrate/crates/orchestrate/client.ethos`, lines 1-10
- `/git/github.com/LiGoldragon/orchestrate/crates/orchestrate-meta/client.ethos`, lines 1-10
- `/git/github.com/LiGoldragon/orchestrate/crates/orchestrate/src/generated/client.rs`, lines 1-17

**The Nexus**
- `/git/github.com/LiGoldragon/orchestrate/Cargo.toml`, lines 1-34
- `/git/github.com/LiGoldragon/orchestrate/crates/orchestrate-nexus/Cargo.toml`, lines 1-49
- `/git/github.com/LiGoldragon/orchestrate/crates/orchestrate-nexus/src/main.rs`, lines 1-39
- `/git/github.com/LiGoldragon/orchestrate/crates/orchestrate-nexus/src/lib.rs`, lines 1-15
- `/git/github.com/LiGoldragon/orchestrate/crates/orchestrate-nexus/src/defaults.rs`, lines 1-120
- `/git/github.com/LiGoldragon/orchestrate/crates/orchestrate-nexus/src/core.rs`, lines 1-225
- `/git/github.com/LiGoldragon/orchestrate/crates/orchestrate-nexus/src/ordinary.rs`, lines 1-40
- `/git/github.com/LiGoldragon/orchestrate/crates/orchestrate-nexus/src/configuration.rs`, lines 1-101
- `/git/github.com/LiGoldragon/orchestrate/crates/orchestrate-nexus/src/transport/mod.rs`, lines 1-283
- `/git/github.com/LiGoldragon/orchestrate/crates/orchestrate-nexus/src/transport/session.rs`, lines 1-227
- `/git/github.com/LiGoldragon/orchestrate/crates/orchestrate-nexus/src/transport/socket.rs`, lines 1-165
- `/git/github.com/LiGoldragon/orchestrate/crates/orchestrate-nexus/src/store/mod.rs`, lines 1-261
- `/git/github.com/LiGoldragon/orchestrate/crates/orchestrate-nexus/src/store/transition.rs`, lines 1-195
- `/git/github.com/LiGoldragon/orchestrate/crates/orchestrate-nexus/src/store/record.rs`, lines 1-60
- `/git/github.com/LiGoldragon/orchestrate/flake.nix`, lines 49, 210-214
- `git -C /git/github.com/LiGoldragon/orchestrate show 2266b06 -- crates/orchestrate-nexus/src/defaults.rs`

**The CLIs**
- `/git/github.com/LiGoldragon/orchestrate/crates/orchestrate/src/main.rs`, lines 1-183
- `/git/github.com/LiGoldragon/orchestrate/crates/orchestrate/build.rs`, lines 1-19
- `/git/github.com/LiGoldragon/orchestrate/crates/orchestrate/Cargo.toml`, lines 1-30
- `/git/github.com/LiGoldragon/orchestrate/crates/orchestrate-meta/src/main.rs`, lines 1-80

**Shared libraries**
- `/git/github.com/LiGoldragon/signal/src/lib.rs` @ `8f9a0deb`, lines 1-31
- `/git/github.com/LiGoldragon/signal/src/frame.rs` @ `8f9a0deb`, lines 1-181
- `/git/github.com/LiGoldragon/signal/src/portable.rs` @ `8f9a0deb`, lines 1-73
- `/git/github.com/LiGoldragon/signal/ethos/signal.ethos` @ `8f9a0deb`, lines 1-17
- `/git/github.com/LiGoldragon/nexus/src/lib.rs`, lines 1-16
- `/git/github.com/LiGoldragon/nexus/src/authority.rs`, lines 1-47
- `/git/github.com/LiGoldragon/nexus/src/situation.rs`, lines 1-134

**Skills and vision**
- `/home/li/primary/SKILL_VARIABLES.md`, all lines
- `/home/li/primary/.claude/skills/nexus/SKILL.md` (authored: `/git/github.com/LiGoldragon/Curriculum/skills/nexus.md`)
- `/home/li/primary/.claude/skills/ethos/SKILL.md` (authored: `Curriculum/skills/ethos.md`)
- `/home/li/primary/.claude/skills/datom/SKILL.md` (authored: `Curriculum/skills/datom.md`)
- `/home/li/primary/.claude/skills/orchestrate/SKILL.md` (authored: `Curriculum/skills/orchestrate.md`)
- `/home/li/primary/.claude/skills/behavior/SKILL.md`, `/home/li/primary/.claude/skills/flow-evidence/SKILL.md`, `/home/li/primary/.claude/skills/subflow/SKILL.md`
- `/home/li/primary/Vision/nexus.md`, lines 1-125
- `/home/li/primary/Vision/signal.md`, lines 1-43
- `/home/li/primary/Vision/orchestrate.md`, lines 1-12
- `/home/li/primary/Vision/sema.md`, lines 1-15
- `/home/li/primary/Vision/ethos.md`, lines 251-290 (headings of all 442 lines read)
- `/home/li/primary/Vision/datom.md`, lines 190-215 (headings of all 312 lines read)

**Live witnesses** (2026-09-18, host `goldragon.criome`, uid 1001)
- `ps aux | grep orchestrate-nexus`
- `ls -la $XDG_RUNTIME_DIR/orchestrate-nexus/`, `ls -la ~/.local/state/orchestrate-nexus/`
- `cat $(which orchestrate)`, `cat $(which orchestrate-meta)`
- `orchestrate` (no arguments), `orchestrate --help`, `orchestrate a b`, `orchestrate 'Observe.Locks'`
- `orchestrate-meta 'ReverseMetaConfiguration'`
