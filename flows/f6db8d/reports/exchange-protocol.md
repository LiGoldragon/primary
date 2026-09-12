# The Signal exchange protocol — the design, and what was rejected to reach it

Subflow of main flow f6db8d, 2026-09-12, thread
`f6db8d14-1dfe-472d-914e-9c441f852834`.

Brief: `reports/landings-consumers.md` found four consumers — router,
persona, criome, mentci — blocked not on size but on an undecided design.
`signal` 5.0.0's own `src/lib.rs` said *"The protocol layered on top of the
rkyv archive is not decided; nothing here anticipates it"*, and
`Vision/signal.md` agrees: *"The protocol is to be decided."* The brief
directed this flow to research how comparable systems settle it, design the
smallest protocol that serves every existing contract with no compatibility
path, implement it in `signal` under a lock with tests seen failing first,
and then port the four consumers.

**Witnessed** means this flow read or ran it on this machine, or read a
Prometheus build log from a build it launched. **Relayed** means a dispatched
read-only subflow reported it; where a relayed claim was load-bearing this
flow re-read the source and says so.

## 0. The authority this flow decided under, and the tension in it

`Vision/signal.md` says the protocol is *to be decided* — by the living.
`reports/landings-consumers.md` §3a framed the remainder as *"one design
decision, then three ports"* and put the decision to the living.

The decision was taken here on two warrants, both witnessed:

- `flows/f6db8d/vision/designPractice.md`, 2026-09-12, typed: *"I cant
  really answer much right now, but the vision is imperfect. Use common
  sense and research good ontology and software anatomy to make better
  design decisions."*
- The main flow's brief, which names web research authorized and instructs
  the design be written and implemented.

The tension is recorded rather than smoothed: this is a wire protocol the
living said was theirs to decide, decided by a flow under a general
authorization to decide. Everything below is falsifiable against the
living's own Vision, and §8 lists the three Vision lines it completes and
the one it reads against its letter.

## 1. Two corrections to the brief's premise, before the design

**The brief's "five of seven contracts contradict the one-request-one-frame
reading" conflates two findings.** Witnessed in
`reports/landings-consumers.md:283-288`: the five-of-seven figure is about
**vendoring** — five migrated contracts declared their own
`pub struct Signal<T>` with no `signal` dependency — not about framing. The
one-request-one-frame proposition comes from a different place,
`aggregator/ARCHITECTURE.md:45-50`.

Re-read at the cut (relayed, then re-read by this flow against each
`Cargo.toml`): the vendoring five is now **one**. signal-persona `:20`,
signal-harness `:25`, signal-mind `:24`, signal-message `:19` and
signal-mirror `:25` all depend on `signal`; only **signal-terminal** still
vendors `Signal<T>` (`src/lib.rs:9`, no frame dependency at all). The
de-fork landed.

**The honest framing count is seven and four, not five and two.** Of the
eleven contracts on or adjacent to the new stack, **seven declare
vocabulary that one request and one frame cannot carry** — harness, mind,
terminal, message, criome, mentci, router — and **four do not** — mirror,
aggregator, persona, repository-ledger. Cited in §2.

**And the sharpest single fact in the inventory is a self-contradiction.**
`signal-router/src/lib.rs:17-20` says *"no exchange identifier, no lane, no
epoch, and no route code: … the connection is the correlation"*, while its
own `ethos/signal.ethos:24-26` declares `SessionClientHello`,
`SessionClientProof` and `SessionData` as three ordinary `Query` variants —
a three-step handshake on one connection, running today at
`router/src/router.rs:442-481`. The contract that denies the need is the one
that needs it most.

## 2. What the estate actually requires

Each line names the witnessed site that demands it. Relayed items are marked.

| # | Requirement | Evidence |
|---|---|---|
| R1 | Correlate an answer to its question | `mentci/src/daemon.rs:156-166` echoes the client's identifier (relayed); every other site mints a constant — `router/src/peer_session.rs:485-491` returns epoch 0 / Connector / sequence 0 for **every** exchange on a session (witnessed) |
| R2 | One question, one answer | signal-mirror, signal-aggregator, signal-persona, signal-repository-ledger; `persona/src/transport.rs:399-403` opens a socket per call (relayed) |
| R3 | One question, an open-ended stream of answers | `orchestrate/crates/orchestrate-nexus/src/transport/session.rs:161-211` — one `Observed` on open, then one per change, forever (witnessed, quoted §3); `harness/src/daemon.rs:1394-1412`; `criome/src/transport.rs:104-141` |
| R4 | Many exchanges on one connection | `router/src/router.rs:442-481` loops for the life of a session; `harness/src/daemon.rs:1282-1294` reads repeatedly under `tokio::select!` while pushing events; signal-router's three-step handshake |
| R5 | Retract one subscription without killing its siblings | `harness/src/daemon.rs:1289-1291` closes the connection when `subscriptions.is_empty()`; `UnwatchHarnessTranscript`, `DropSubscription`, `IdentitySubscriptionRetraction`, `TerminalWorkerLifecycleRetraction` all declared per contract |
| R6 | Typed refusal that does not drop the connection | `signal-frame/src/reply.rs:117-119`: frame decode failures *"are protocol errors (close + log), not typed rejections — they have no `ExchangeIdentifier` to address"*, against `signal-mirror/ARCHITECTURE.md:24-25`: *"No dropped connection is required to communicate a storage fault"* |
| R7 | An intermediary forwards without reading the payload | `router/src/daemon.rs:294-310` trial-decodes two contracts and returns the **first** arm's error (witnessed, quoted §6) |
| R8 | A handshake payload | `Vision/nexus.md`, Routing: the signal repository *"holds what every signal needs in common — the handshake payload among it"* |

Two facts that shaped the design as much as the requirements:

**Vocabulary that was built, shipped and never used.** Witnessed across the
estate: no site anywhere constructs anything but
`Reply::committed(NonEmpty::single(SubReply::Ok(_)))`, and every real
receiver refuses a request of length greater than one
(`router/src/daemon.rs:332-341`). `AcceptedOutcome::{OperationAborted,
BatchAborted}`, `SubReply::{Invalidated, Failed, Skipped}`,
`BatchFailureReason`, `RetryClassification`, `CommitStatus`,
`BatchErrorClassification`, `WireRoute`'s root/variant triage, `LogVariant`,
`ExchangeMode`, `ExchangeHandshake` and `NamespaceSection` all have no
consumer. `StreamingFrameBody` was reachable only through the hand-written
`signal_channel!` macro and **no generated contract crate in the estate
binds it** — which is exactly why every migrated streaming contract has a
declared event root and no way to send it.

**Absence in the mechanism paid for in the payloads.** `mind` declares
`SubscriptionCursor`, `SubscriptionDemandCredit` and
`SubscriptionBufferBound` in its contract
(`signal-mind/src/generated/signal.rs:439-443`) and serves subscriptions by
**polling** (`ReadSubscriptionEvents` → `SubscriptionEventLog`,
`mind/src/transport.rs:148-166`) — against `Vision/nexus.md`'s *"Polling is
forbidden."* `router/src/peer_session.rs:62-70` reimplements a session epoch
at the application layer because the wire copy was pinned at zero. Each is a
requirement the protocol should absorb rather than leave to every contract.

## 3. The one working subscription, which the design had to serve unchanged

Witnessed, `orchestrate` 0.35.0, `transport/session.rs:161-211`:

```rust
let mut announcements = attendance.announcements;
self.answer(&OrdinaryResponse::Observed(attendance.opening)).await?;
loop {
    let observation = match announcements.recv().await {
        Ok(observation) => observation,
        Err(RecvError::Lagged(_)) => core.ask(Overtaking { .. }).await.delivered()?,
        Err(RecvError::Closed) => return Ok(()),
    };
    match self.answer(&OrdinaryResponse::Observed(observation)).await { .. }
}
```

Four things this settles. The state on open and then each change are the
**same** `Observed` variant — no snapshot marker exists and none is wanted.
Correlation today is the connection: one `Query` is read per connection
(`session.rs:151`, not in a loop), and interleaving is impossible by
construction. A lag is recovered by re-sending the whole observation and the
subscriber is **never told** — harmless only because `Observation.Locks` is
always a full state, and a latent defect for any contract that ever sends an
increment. `RecvError::Closed` is a real case of the answering side ending a
live exchange, so an ending frame cannot be omitted.

The `orchestrate` skill states the current design in one line: *"the
connection itself is the subscription, with no token and no `Unwatch`."*
That is the design this flow had to decide whether to keep.

## 4. The design

Landed as `signal` 7.0.0 `e1a83028`, gate green on Prometheus, verified on
the real remote by `git ls-remote`.

**Vocabulary, in `ethos/signal.ethos`:**

```
ExchangeId.Integer
ContractDigest.Integer
Handshake.{ ContractDigest }
HandshakeRejection.[ ContractMismatch.ContractDigest ]
HandshakeReceipt.[ Greeted.ContractDigest  GreetingRefused.HandshakeRejection ]
ExchangeFault.[ GreetingExpected  GreetingRepeated  ExchangeInUse  UnknownExchange
                ExchangeLimit  UnreadableQuery  Lagged ]
Conclusion.[ Completed  Faulted.ExchangeFault ]
```

**Envelope, hand-written in `src/exchange.rs`** because Ethos has no
generics and the envelope must be generic over the contract's root, so that
one archive carries the envelope and the contract value together with no
nested encoding:

```rust
pub enum Dispatch<Q> { Greet(Handshake), Open(Opening<Q>), Abandon(ExchangeId) }
pub struct Opening<Q> { pub exchange: ExchangeId, pub query: Q }

pub enum Delivery<R> { Greeted(HandshakeReceipt), Answer(Answer<R>), End(Ending) }
pub struct Answer<R> { pub exchange: ExchangeId, pub response: R }
pub struct Ending { pub exchange: ExchangeId, pub conclusion: Conclusion }
```

**State and kinds, in `src/accord.rs`:** `ExchangeLedger` is one
connection's exchange state — greeted or not, which identifiers are open,
bounded at `MAXIMUM_OPEN_EXCHANGES` so a peer-driven table cannot grow
without limit. The kinds are `Contracted` (a contract root names its
authored Ethos source and is identified by that source's digest), `Greeted`,
`ExchangeTracking`, `ExchangeMinting: ExchangeTracking`, and `Exchanged` (a
frame names the exchange it belongs to). `CONNECTION_EXCHANGE` is `0`, which
no minted exchange ever is, so a fault the answering side cannot attribute
to an exchange is reported against the connection — R6, discharged.

**In one paragraph.** A connection is greeted once, settling the contract by
the digest of its authored Ethos source; two peers agree exactly when their
sources agree, and a mismatch is a typed refusal, never a negotiation. After
the greeting the connection carries any number of concurrent exchanges, each
named by an identifier the querying side mints and no other side rewrites;
every frame the answering side sends names the exchange it belongs to. One
query and one answer is an exchange that ends after its answer; a
subscription is an exchange that goes on answering, its first answer the
state on open. Whether an exchange takes one answer or many is **not on the
wire** — both sides know the contract, so the contract says. What is on the
wire is one integer and six variants.

**One obligation this places on contracts, and it must be written into every
streaming contract:** a contract whose exchange streams must send its first
answer even when the state is empty. Relying on position means a peer
otherwise cannot distinguish an empty state from a state not yet sent.
Orchestrate already satisfies this — it answers `Observed(Locks([]))` — but
by accident rather than by rule.

**The contract digest.** FNV-1a over the source bytes, taken as a signed
64-bit integer, computed in a `const fn` so a contract's identity is settled
when it is compiled rather than hashed at every connection. Each contract
crate already exports the constant this reads: `pub const ETHOS: &str =
include_str!("../ethos/signal.ethos")` in signal-orchestrate, signal-router,
signal-criome, signal-mentci, signal-persona and signal-message (witnessed);
signal-mirror spells it `MIRROR_SIGNAL_SOURCE`. So adopting the greeting is
one line per contract. This follows the `nexus` skill's rule that identity
is trait-borne and an encoded form fingerprints itself, and it has direct
precedent: Cap'n Proto's type ids are *"the first 8 bytes of the MD5 hash of
the parent scope's ID concatenated with the declaration's name"*, chosen
over symbolic names because *"It's easy for symbolic names to collide, and
these collisions could be hard to detect in a large distributed system with
many different binaries using different versions of protocols."*

**What the layer deliberately does not carry.** Each is recorded in
`src/exchange.rs` beside the requirement it was there to serve, so the
reasoning cannot drift from the code.

| Omitted | The system that proves it can go | The argument |
|---|---|---|
| End-of-stream flag | gRPC's `END_STREAM` and Varlink's `continues` exist because their payloads are not schema-bound | `Vision/signal.md`: *"fully typed with both sides knowing the full schema, nothing on the wire labeling itself."* A peer that sent `Observe` knows its exchange streams. gRPC's own precedent: server-streaming and bidi are **byte-identical** on the wire and a cardinality violation surfaces as `UNIMPLEMENTED` |
| Sequence number | Cap'n Proto, gRPC and Varlink all carry none | A stream socket delivers one connection's frames in order and drops none. `signal-frame`'s `LaneSequence` numbered what the transport already ordered — and `LaneSequence::next()` is never called on router's peer path (witnessed) |
| Session epoch | Cap'n Proto: *"a newly-established connection starts with no valid IDs"*; gRPC: stream ids *"are contextual to an open HTTP2 session … nor can they be used as GUIDs"* | An epoch is necessary exactly when correlation state may outlive the channel that named it — MQTT's case, by design. On `AF_UNIX` it cannot outlive it silently: closure surfaces as EOF or `EPIPE`. An identifier's scope is the connection that minted it, so a stale answer has no namespace to land in |
| Lane / id parity | gRPC splits stream ids odd and even because **either** end may open one | `Vision/nexus.md`: *"An edge joins two vertices and carries one contract."* One side queries, one answers; the querying side owns the whole identifier space |
| Subscription token | Cap'n Proto's subscription idiom, sd-bus's slot and Erlang's monitor all make the correlation token the liveness token | The exchange **is** the token. `Abandon` retracts it; closing the connection retracts all of them. This deletes `SubscriptionTokenInner` and four contracts' retraction vocabulary |
| Cursor, demand credit, buffer bound | — | The socket applies backpressure. The one thing it cannot say is that the answering side fell behind, and `ExchangeFault::Lagged` says it; the recovery is to open the exchange again, which by the subscription's own semantics delivers the state on open. This deletes `mind`'s three contract types and its polling |
| Snapshot-versus-increment bit | Varlink's monitor pattern carries none: *"a typical Varlink monitor method call first returns the current state and then sends changes in subsequent replies to the same request on the same connection"* | Position identifies it, because the exchange id makes the per-exchange sequence total and the schema fixes the snapshot's arity at one. It becomes load-bearing only for a multi-frame snapshot (Wayland, which needed both `wl_display.sync` and `wl_output.done`), a mid-stream re-snapshot, or a snapshot whose arrival is not guaranteed (MQTT's `RETAIN`, the one system that genuinely needs the bit) |
| Batch | — | Nothing in the estate constructs a batch and every receiver refuses one (§2) |
| Caller record | `signal-frame/src/caller.rs:122-125` calls its own contents *"advisory. Socket credentials remain the authoritative security boundary"* | Peer credentials at accept are the authority; `design-decisions.md` item 6 Rule 3 rules the message type **is** the authority token. A contract that wants to name a caller declares it |
| Per-frame contract marker | See §6 — this is the closest call in the whole design | |

## 5. Alternatives rejected

**A. The connection is the exchange — zero envelope bytes.** This is what
orchestrate does today and what the `orchestrate` skill states as the
design. It serves R1, R2, R3 and R6 with nothing on the wire at all, and it
is genuinely the smallest thing that could work. Poettering names the trade
as a feature: varlink is *"built around notion of 'cheap' connections … if
you want parallel operations being queued, you allocate multiple
connections, instead of multiplexing them into one."*

Rejected on three grounds, in increasing weight. It cannot serve R4, which
router needs today (`router/src/router.rs:442-481`) and harness needs today
(`harness/src/daemon.rs:1282-1294`). It cannot serve R5: closing the
connection to retract one subscription kills its siblings — the survey's law
is that cancellation is mandatory if and only if you multiplex, and D-Bus is
the instructive failure, multiplexing while omitting cancel so that an
in-flight call cannot be stopped by any means, which is why sd-bus had to
invent the slot as a purely local fiction. And decisively, `Vision/nexus.md`
names a **handshake payload** as belonging in `signal`; a handshake
amortizes over a connection that outlives one exchange and is pure overhead
on a connection that does not. Vision rules for multiplexing by ruling for a
handshake.

Correctness argument, independent of the router, from Wayland's own
documentation: *"Messages are guaranteed to arrive in the order they were
sent, **but only with respect to one sender**."* Wayland does not have one
total order either — it has two independently ordered streams, which is
exactly why it needs `wl_display.sync` as a barrier. Bidirectional
concurrency alone breaks ordering-correlation; Varlink survives only by
forbidding multiplexing outright.

**B. Wayland-style object-id addressing, with no correlation id.** Superficially
the smallest multiplexed design: `object_id:u32, opcode:u16, size:u16` — three
fields, eight bytes.

Rejected. First, the framing is false: object ids **are** ids, and there are
more of them than correlation needs. The real trade is lifetime — a
correlation id's lifetime is the exchange; an object id's lifetime is the
object, so it outlives any single message and needs an id-lifecycle protocol
a correlation-id design has none of: a split id space (client
`[2, 0xfeffffff]`, server `[0xff000000, 0xffffffff]`) so both ends can
allocate without a round trip, a dense-packing rule that is *"not merely a
guideline, but a strict requirement"*, and an explicit reclamation
handshake, `wl_display.delete_id`. Cap'n Proto pays the same price for the
same reason — *"messages using the ID could be traveling in both directions
simultaneously, we must define the end of life of each ID in each
direction"* — with `Finish`, `Release.referenceCount` and `Disembargo`. **A
per-exchange id retired on its own terminal frame needs no handshake: the
terminal frame is the release.** Second, it cannot serve R6: `wl_display.error`
is fatal by definition, every per-interface error enum feeds into it, and
recoverable failure must be hand-rolled per protocol
(`wl_data_source.cancelled`, `zwp_linux_buffer_params_v1.created` xor
`.failed`). A non-fatal error needs correlation to be actionable, so
requirement R6 and requirement R1 are the same requirement.

Wayland's own `serial` proves the concepts are distinct and is worth naming,
because it is the thing a correlation id is not: `xdg_surface.ack_configure`
lets a client *"discard all but the last"* configure, and acking *"consumes
the serial number sent with the request, as well as serial numbers sent by
all configure events sent on this xdg_surface prior."* Collapsing many into
one is legal — which a correlation id can never permit.

**C. `signal-frame`'s shape: an eight-byte bit-packed `ShortHeader` carrying a
registry-allocated `ContractId` and `WireRevision`, plus `ExchangeIdentifier
= (SessionEpoch, ExchangeLane, LaneSequence)`.** This is the incumbent, and
35 repositories still declare it (witnessed).

Rejected on its own record. The registry it required was never maintained
and the field it existed for was never read: router carries `ContractId` on
every frame and dispatches by **decode-success order** instead
(§6). Its three-part identifier is a constant in every consumer but one —
epoch 0, Connector, sequence 0, for every exchange on a session
(`router/src/peer_session.rs:485-491`). A field that is always zero is a lie
on the wire. Its streaming envelope was unreachable from schema generation,
so seven contracts declare events they cannot send. And the bit-packed
header invites exactly one failure: waypipe, the standard Wayland proxy,
steals unused high bits of the opcode word to smuggle an fd count
(`h2 = (h2 & !0xff00) | (1 << 11)`). An rkyv enum has no slack to steal.

**D. blake3, or any cryptographic digest, for contract identity.** Rejected,
and this one was reversed mid-implementation on evidence. It adds a
dependency to the crate 34 repositories depend on, for a property decidable
at compile time; the first Prometheus build refused it outright because the
lockfile cannot be re-vendored on a cold machine (`error: no matching package
named blake3 found`, witnessed). The `const fn` FNV-1a needs no dependency,
makes identity a compile-time constant, and costs eight bytes on the wire
once per connection. It detects two peers built from different sources, and
nothing here defends against a peer choosing its own bytes — which is what a
cryptographic digest would buy and what the threat model does not ask for.

**E. Registry numbers or symbolic names instead of a digest.** Rejected on
Cap'n Proto's stated reasoning, quoted in §4: names collide, collisions are
hard to detect across many binaries on different protocol versions, and
fully-qualified names waste wire space. A digest is computed, not allocated,
so there is nothing to maintain and nothing to get out of step.

**F. A version-range handshake, as `signal-frame` had — `ProtocolVersion` with
`accepts(peer) = self.major == peer.major && self.minor >= peer.minor`.**
Rejected by Spirit: *"Backward compatibility is never a design variable."*
An exact digest and a typed refusal is the whole mechanism. Varlink reaches
the same place from a different direction: *"Varlink interfaces do not have a
version number, they only have a feature set described in detail by the
interface definition, which is part of the wire protocol"* — an incompatible
change is a rename, not a negotiation.

**G. A single bidirectional frame enum, as `signal-frame`'s
`ExchangeFrameBody` was.** Rejected: a `Request` variant can never arrive
from the answering side and an `Answer` never from the querying side, so one
enum makes half its variants unreachable at every read site. Two
direction-typed enums make the unreachable unrepresentable, which is the
same reason `signal-frame`'s own doc comment gives for splitting event
payloads from reply payloads.

**H. Putting `origin` on every frame, so a router forwards statelessly — the
research's own recommendation, `{ origin: u32, exchange: u32, contract: u64,
kind: tag }`.** This is the most serious rejected alternative and the
argument for it is strong: *"the difference between a stateless and a
stateful router is not effort, it is whose number space the correlation id
lives in. A connection-local slot number forces a per-exchange translation
table that must be garbage-collected — and for open-ended subscriptions that
table's lifetime is unbounded."* D-Bus is the existence proof of the
stateless shape: the daemon routes on `DESTINATION`, stamps `SENDER`, never
rewrites the serial, and holds **zero** per-call state, because the exchange
is named by `(sender, serial)` rather than by a connection-local slot.

Rejected for three reasons. `Vision/nexus.md` places routing in the router's
own vocabulary, not in the frame: *"The router tells signal types apart by an
enum that wraps the objects."* `signal` already holds `ComponentKind`, which
is that enum, so a router's contract can address a destination without
`signal` growing a field that is meaningless on every direct edge — and
almost every edge in the estate is direct. Second, router already tunnels
rather than translates: `router/src/router.rs:451-461` carries a complete
framed exchange inside one sealed payload field, so the originator's
exchange id travels end-to-end and is never rewritten, which is precisely
the property `origin` was to buy. Third, the translation table the argument
warns about **is** the `ExchangeLedger`, bounded at
`MAXIMUM_OPEN_EXCHANGES` per connection and released when an exchange ends
or its connection closes, so the unbounded-lifetime failure is structurally
excluded rather than left to discipline.

One consequence of this rejection is recorded as owed, not solved: a router
that reconnects to a Nexus transparently while keeping client exchanges
alive across the gap would be offering session-outlives-transport semantics
and would then need an epoch. It must not offer that. The disconnect is
propagated as a typed refusal — Cap'n Proto's `disconnected` type exists to
prescribe exactly that client response, *"disconnect and start over"*.

**I. Multi-contract sockets with a per-frame discriminator.** Rejected, and
it is the change this design forces on the router port. Waypipe is real
evidence for the other side: a Wayland intermediary must be a stateful,
protocol-aware translator that generates code from the protocol XML and
replicates the whole id-lifetime rule by hand, precisely because the
interface appears on the wire exactly once, at `wl_registry.bind`. But
`Vision/nexus.md` rules that *"An edge joins two vertices and carries one
contract"* and that a Nexus *"opens at least two sockets … A Nexus that
needs more levels of access opens more sockets."* Router's working socket
carrying both signal-message and signal-router is drift from that rule, and
the fix is two sockets rather than a marker. The greeting then cures the
symptom the trial decode causes: a peer on the wrong contract is refused
with a typed `ContractMismatch` naming both digests, instead of reading EOF
from a connection that closed without replying.

## 6. What the router routes on today, and what this changes

Witnessed, `router/src/daemon.rs:294-310`:

```rust
fn decode(body: &[u8]) -> Result<Self, signal_frame::FrameError> {
    match WorkingSignalMessageInput::decode(body) {
        Ok(input) => Ok(Self::SignalMessage(input)),
        Err(signal_error) => match WorkingRouterObservationInput::decode(body) {
            Ok(input) => Ok(Self::RouterObservation(input)),
            Err(_router_error) => Err(signal_error),
        },
    }
}
```

Three facts. The `ContractId` in the short header is **never read** — the
discriminator on the wire is present and unused, and the discriminator in
the code is decode-success order. The second arm's error is discarded and
the first arm's returned, which is exactly the persona failure recorded in
`reports/landings-consumers.md` §3: persona sends a bare archive, both arms
fail, router closes without replying, and
`persona/src/bin/wire_router_client.rs:92` reads EOF. And both arms require
an envelope from **different copies of the crate** —
`router/Cargo.toml:62-63` declares `signal-frame` twice, once by branch and
once by rev, so `ReceivedSignalMessageInput.exchange` and
`ReceivedRouterObservationInput.exchange` are two incompatible Rust types
for one wire field in one binary. That is the `links` collision the de-fork
solved for `Signal<T>`, still live for the envelope.

Actual routing is a `match` on the decoded payload enum
(`src/daemon.rs:182-212`), not on any marker, address or route code.
`WireRoute`'s root and variant bytes are populated on encode and read by
nobody.

## 7. What was implemented, and the witness for it

`signal` 7.0.0, commits `e1a83028` then `66e7b153`, on the real remote
(verified after each push by
`git ls-remote https://github.com/LiGoldragon/signal main`). Built on
`signal` 6.0.0 `9d8b2b8c` as the coordinator directed, carrying protos
0.31.0 `1febca78`, datom-codec 0.31.0 `09e2a9d5` and ethos-zero 10.0.0
`4bf73cae`.

Files: `ethos/signal.ethos` (seven types added), `src/generated/signal.rs`
(regenerated), `src/exchange.rs`, `src/accord.rs`, `src/lib.rs`,
`tests/exchange.rs` (19 tests), `ARCHITECTURE.md`, `UPGRADES.md`,
`Cargo.toml`, `Cargo.lock`.

**The generator was verified before it was trusted.** ethos-zero 10.0.0 was
built on Prometheus (`nix build --max-jobs 0`, `/nix/store/jzgqsx…-ethos-zero-10.0.0`)
and run against the **unmodified** `ethos/signal.ethos`; its output was
**byte-identical** to the checked-in `src/generated/signal.rs`. Only then
was the ethos file changed and regenerated.

**Failing first, witnessed on Prometheus.** `src/accord.rs` and
`src/exchange.rs` were stubbed so that the digest was a constant `0`, the
ledger admitted and released anything without recording it, `bears` was
always false, the greeting never refused a repeat, `mint` always returned
`FIRST_EXCHANGE`, `Answer::exchange` always returned `CONNECTION_EXCHANGE`,
`Ending::faulted` always produced `Completed`, and `is_connection_wide` was
always false. Result of `nix build --max-jobs 0 .#checks.x86_64-linux.test`:

```
test result: FAILED. 4 passed; 15 failed; 0 ignored; 0 measured
```

The fifteen red are named in the log: the three contract-identity tests, the
six ledger tests, the interleave test, the lag test, the connection-fault
test, the completed-versus-faulted test, and the abandon-slot test. The
implementation was then restored and the same check ran `19 passed; 0
failed`.

**Two tests came after, and prove the shape a consumer would otherwise have
discovered.** `signal`'s own taxonomy declares no vector type, so the first
nineteen proved the envelope only against roots of enums and structs. The
shape it must actually carry is `signal-orchestrate`'s
`Observed(Locks(Vec<Lock>))` — a variant holding a vector of structs that
hold owned strings and vectors of their own. That root is declared in the
test and carried through the wire. The second states the obligation §4
names: an empty state on open is still an answer. Both are in `66e7b153`,
with the full gate green again.

**Stated honestly: six tests were not seen failing.** `no_minted_exchange_is_
ever_the_connection_itself` passed against the stub because
`FIRST_EXCHANGE` is not `0` — an honest pass that distinguishes nothing —
and five envelope round-trip equality tests — three in the first wave and
both of the two added after — passed because their failure mode is a
serialization defect, which a behavioural stub cannot fake.

**The expected value comes from outside the code under test.** The digest
oracle, `-501540396992439027`, is FNV-1a over
`"Signal\n[]\n[]\n[]\n[ Ping.Integer ]\n"` computed in Python from the
published algorithm, not through the tested path. The test types are real
generated taxonomy enums (`AuthorizedObjectInterest`,
`ComponentClassification`), derived exactly as a contract's roots are, so
the generic envelope is proved against the shape it will actually carry.

**The load-bearing test** —
`a_subscription_and_a_one_answer_exchange_interleave_on_one_connection` —
writes six `Delivery` frames to one byte stream: a greeting, the state on
open, a change, a one-answer exchange's answer and its `End`, and then
another change on the subscription; reads them back frame by frame; and
attributes every one by exchange alone. That is the behaviour `signal-frame`
could not express and seven contracts need.

**Full gate, green on Prometheus**, `nix flake check -L --max-jobs 0
--keep-going` → `all checks passed!` — all fourteen checks, including
`clippy --all-targets -- -D warnings` in three feature configurations,
`cargo doc` with `-D warnings`, `cargo fmt --check`, the datom and transport
feature legs, and the `--no-default-features` build. `--keep-going` was
passed deliberately, per the standing caution in
`reports/landings-consumers.md` §7 that a `nix flake check` without it stops
at the first failure.

No local cargo was run and no local build was performed; every compile ran
on Prometheus under `--max-jobs 0`. `rustfmt` and `b3sum` were fetched as
built store paths and run directly, which is neither a build nor cargo.

## 8. Vision lines this completes, and the one it reads against its letter

- `Vision/signal.md`, **Protocol** — *"Signal is portable rkyv plus whatever
  protocol is standardized on top of it. The protocol is to be decided."*
  **Decided, pending the living's review.** Proposed replacement:

  > Signal is portable rkyv plus the exchange layer. A connection is greeted
  > once, settling the contract by the digest of its authored source. It then
  > carries any number of exchanges, each named by an identifier the querying
  > side mints. Whether an exchange takes one answer or goes on answering is
  > not on the wire: both sides know the contract.

- `Vision/nexus.md`, **Routing** — *"That repository also holds what every
  signal needs in common — the handshake payload among it."* **Discharged**:
  the handshake payload is the contract digest, and it lives in `signal`.
  The routing half is **not** discharged and is not this layer's: the enum
  that wraps the objects is `ComponentKind`, already in `signal`, and the
  addressing built on it belongs in the router's own contract.

- `Vision/nexus.md`, **Observation by subscription** and **Polling is
  forbidden** — **now expressible**. `mind`'s polling was a workaround for
  the missing mechanism, not a design.

- The line read against its letter: nothing in Vision says a subscription
  may be retracted without closing its connection, and the `orchestrate`
  skill states the opposite as the current design — *"the connection itself
  is the subscription, with no token and no `Unwatch`."* This design keeps
  that true for a connection carrying one exchange and adds `Abandon` for a
  connection carrying several. Recorded because it is a change to a stated
  design, on the argument in §5A.

## 9. What did not happen, and exactly where it stands

The brief's second half — port router, then persona, criome and mentci,
landing each on main when green — **was not done**. Stated plainly rather
than partially attempted, because a half-done port of a 20,500-line
consumer is worse than none.

The scale, witnessed or relayed: router 20,500 lines with a working socket
that must be split in two and two copies of `signal-frame` to remove;
criome 22,280 lines, 464 `Type::new(...)` call sites, ~700 root-type
occurrences, its whole transport resting on ten `signal-frame` types; mentci
depends on criome as a library crate, so its order is forced; persona is
blocked on router.

**A sibling sweep is now running over exactly these repositories, and it must
be told `signal` moved.** Witnessed in `Observe.Locks` at the close of this
work: locks 1362 `F6db8dFinalSweepMetaSignalSystem` and 1363
`F6db8dFinalSweepMetaSignalTerminal`, both flow f6db8d, while
signal-message, signal-router, router, criome, mentci and persona — all
locked earlier in this thread — are now free. A sweep repinning contracts to
`signal` 6.0.0 will leave every one of them a major behind and, because
`links = "signal"` admits one package per graph, un-co-resolvable with
anything that reaches 7.0.0. The coordinator was told.

That is also why this flow did **not** start the repin wave itself: the
estate's own rule, from `reports/landings-consumers.md` §4, is that a
conversion is safe only across a whole producer closure in one pass, and a
half-converted graph is strictly worse than an unconverted one. Repinning
signal-criome to 7.0.0 while signal-message sits on 5.0.0 would break
router's graph further rather than less, and doing it against a moving sweep
would collide.

**The prerequisite nobody has done yet, and the right next step:** each
contract crate in a consumer's closure must be repinned to `signal` 7.0.0
and given a one-line `Contracted` impl naming the `ETHOS` constant it
already exports. For router that is signal-router, meta-signal-router,
signal-message, signal-criome, signal-persona, signal-harness, signal-mind
and signal-mirror — because `signal` declares `links = "signal"` and cargo
admits one package per `links` key per graph, so router's graph cannot
resolve until every member reaches 7.0.0. That repin wave is bounded and
mechanical and should be one actor's single pass.

**Two defects found and not fixed.**

`ExchangeFault::Lagged` has no producer yet. Orchestrate's
`RecvError::Lagged` arm re-sends the whole observation and tells the
subscriber nothing (§3). That is harmless for `Observation.Locks` and wrong
for any contract that sends an increment. Fixing it is an orchestrate
change, in the file item 6 of `reports/design-decisions.md` already names as
the one that changes.

The **deployed** Orchestrate 0.30.0 mis-parses a guillemet-delimited
`LockReason` containing a space. Witnessed twice by this flow:
`«two words»` is refused with `Corporate(… Arity(4, 5))` — the space inside
the guillemets was read as a position separator — while `«oneword»` is
accepted and echoed back in guillemets. This contradicts the `orchestrate`
skill's own copyable example,
`orchestrate 'Lock.{ OrchestrateDocs 444e5e [ /absolute/path/to/file ] «Clarify Lock fields» }'`.
Every lock this flow took therefore used a single-token reason. The deployed
binary is `orchestrate-0.30.0`; the checkout is at 0.35.0, so this may
already be fixed unreleased — which is the first thing to check.

**One estate-wide figure larger than any report has carried.** Thirty-five
repositories still declare `signal-frame` in `Cargo.toml` (witnessed by
`grep -l` over `/git/github.com/LiGoldragon/*/Cargo.toml`): agent, cloud,
criome, harness, introspect, listener, mentci, mentci-egui, mind,
mind-judge, mirror, orchestrator-judge, persona-spirit, repository-ledger,
router, sema-storage, spirit, spirit-judge, system, upgrade, and the
contract crates meta-signal-agent, meta-signal-cloud, meta-signal-harness,
meta-signal-listener, meta-signal-mentci-client, meta-signal-mind,
meta-signal-version-handover, signal-agent, signal-cloud, signal-listener,
signal-mentci-client, signal-mind-judge, signal-orchestrator-judge,
signal-sema-storage, signal-version-handover. `signal-frame` 0.4.0 is
2,812 lines. "Being deleted estate-wide" describes an intention, not a
state.

## 10. Consumers not repinned, and deliberately so

`signal` 7.0.0 is a breaking bump and `links = "signal"` makes staleness a
resolution failure rather than a deferred debt. This flow repinned **nothing
but `signal` itself**, per the brief. The complete list of direct `signal`
consumers and the revision each holds, read from each local `Cargo.toml`
(so a remote may differ and must be re-read by the sweep):

On `7bcb0949` (signal 5.0.0) — 17: message, meta-signal-criome,
meta-signal-mentci, meta-signal-message, meta-signal-mirror,
meta-signal-persona, meta-signal-repository-ledger, meta-signal-router,
meta-signal-system, signal-criome, signal-harness, signal-introspect,
signal-mentci, signal-message, signal-mind, signal-mirror, signal-persona,
signal-repository-ledger, signal-router, signal-system.

On `48ae17b4` (signal 4.0.0) — 5: aggregator, meta-signal-aggregator,
meta-signal-spirit, signal-aggregator, signal-spirit.

On `8f9a0deb` (signal 3.0.2) — 5: lojix, meta-signal-lojix, orchestrate
(spelled with a `.git` suffix), signal-lojix.

On `626e407b` — 2: meta-signal-orchestrate, signal-orchestrate.

On `branch = "main"` — 1, and this one is the mutable-pin disease the wave
has been fighting: **signal-forge**.

Two spellings are in use and both must be normalized to the canonical one,
`https://github.com/LiGoldragon/signal` with no suffix:
`orchestrate/Cargo.toml` uses `signal.git`, everything else does not.

## Sources

Read by this flow on this machine:

- `/home/li/primary/Vision/signal.md`, `/home/li/primary/Vision/nexus.md`
- `/home/li/primary/flows/f6db8d/vision/designPractice.md`
- `/home/li/primary/flows/f6db8d/reports/landings-consumers.md`
- `/git/github.com/LiGoldragon/signal` — `src/lib.rs`, `src/frame.rs`,
  `src/portable.rs`, `src/transport.rs`, `ethos/signal.ethos`,
  `src/generated/signal.rs`, `build.rs`, `flake.nix`, `Cargo.toml`,
  `Cargo.lock`, `tests/*.rs`, `ARCHITECTURE.md`, `UPGRADES.md`
- `/git/github.com/LiGoldragon/signal-frame` — `src/exchange.rs`,
  `src/frame.rs`, public declaration census
- `/git/github.com/LiGoldragon/signal-orchestrate/ethos/signal.ethos`
- `/git/github.com/LiGoldragon/nexus/src/lib.rs`
- `/git/github.com/LiGoldragon/ethos-zero` — `Cargo.toml`, `flake.nix`
- Every `/git/github.com/LiGoldragon/*/Cargo.toml` for the `signal` and
  `signal-frame` pin census

Run by this flow: `git ls-remote` against the real `signal` remote before
and after the push; `orchestrate 'Observe.Locks'`; the guillemet probe
(locks 1340, released); `nix build --max-jobs 0` for ethos-zero 10.0.0,
`b3sum`, `rustfmt` and `.#checks.x86_64-linux.test`;
`nix flake check -L --max-jobs 0 --keep-going`; `ethos-zero
'Generate.{ … }'`; `jj commit`, `jj bookmark set`, `jj git push`.

Relayed by dispatched read-only subflows, re-read by this flow where
load-bearing:

- The `signal-frame` public API and its estate-wide usage inventory,
  including criome's `src/transport.rs:104-141`, harness's
  `src/daemon.rs:1256-1428`, mind's `src/actors/subscription.rs`, and the
  seven-and-four framing count (§1, §2). Router's `src/daemon.rs:294-354`
  and `src/router.rs:442-481` and `src/peer_session.rs:485-491` were re-read
  by this flow.
- Orchestrate's subscription implementation, `transport/session.rs:146-211`
  and `crates/orchestrate/src/main.rs:146-163` (§3).
- The psyche search across `Vision/`, `vision-raw/`, `flows/*/vision/` and
  `flows/*/notion/`, which found **no** record of the living speaking to
  correlation, request ids, multiplexing or subscription framing — the
  absence that §0 rests on. It did find the origin of the Routing section,
  `flows/012fbf07/vision/archive-threeStacks.md`, 2026-08-11, typed: *"it
  should be an enum in a universal signal repo that all components depend
  on, which wrap the objects. that universal-signal repo could also serve
  other functions that all signals need to deal with (handshake payload
  basically)."*

External, with citations, relayed by a research subflow:

- Cap'n Proto RPC — `rpc.capnp`, https://capnproto.org/rpc.html,
  https://capnproto.org/language.html: the four tables, `QuestionId = UInt32`
  and its reuse rule, `Finish` as advisory cancellation, `Exception.Type`
  and the ruling that *"'checked exceptions' … do NOT make sense"*, the MD5
  type id and the case against symbolic names, and
  https://www.mail-archive.com/capnproto@googlegroups.com/msg00792.html for
  the subscription idiom.
- gRPC over HTTP/2 —
  https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md,
  https://www.rfc-editor.org/rfc/rfc9113.html: 31-bit stream ids, client-odd
  and server-even, `END_STREAM` as a flag, trailers-only errors, the sixteen
  status codes, and the absence of any wire-level server-streaming versus
  bidi distinction.
- D-Bus — https://dbus.freedesktop.org/doc/dbus-specification.html: the
  `yyyyuua(yv)` header, `serial` and `REPLY_SERIAL`, `NO_REPLY_EXPECTED` as
  a should, signals as uncorrelated by construction, `AddMatch` plus
  `GetManagedObjects` as the two-call snapshot workaround, error names as
  strings with no integer code, and the complete absence of cancellation.
- Varlink — https://varlink.org/, https://varlink.org/Method-Call,
  https://varlink.org/FAQ, https://uapi-group.org/specifications/specs/varlink/:
  the `NUL`-terminated JSON framing, `more`/`continues`/`oneway`/`upgrade`,
  errors as declared typed vocabulary, the monitor pattern's
  state-then-changes rule, and the FAQ heading *"Why are there no sequence
  numbers in calls and replies?"* Plus
  https://harald.hoyer.xyz/2017/12/18/varlink/ and
  https://lists.freedesktop.org/archives/dbus/2024-April/018402.html for the
  stated case against D-Bus.
- sd-bus — http://0pointer.net/blog/the-new-sd-bus-api-of-systemd.html and
  the `sd_bus_slot` manual pages: the slot and floating-reply model, and why
  cancellation in D-Bus is definitionally client-side bookkeeping.
- Wayland — https://wayland.freedesktop.org/docs/book/Protocol.html,
  https://wayland-book.com/protocol-design/design-patterns.html,
  https://ppaalanen.blogspot.com/2014/07/wayland-protocol-design-object-lifespan.html,
  xdg-shell.xml, and waypipe's `src/tracking.rs`: the split id space,
  `wl_display.delete_id`, per-sender-only ordering, fatal-only errors, and
  the proxy that must parse the whole protocol.
- MQTT 5.0 — https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html:
  `RETAIN`, Retain Handling, and Session-scoped packet identifiers as the
  one genuine case for a snapshot bit and for an epoch.
- AMQP 0-9-1 and 1.0, and Erlang/OTP `gen_server` —
  https://www.rabbitmq.com/resources/specs/amqp0-9-1.pdf,
  https://github.com/erlang/otp/blob/master/lib/stdlib/src/gen.erl,
  https://www.erlang.org/eeps/eep-0053.html: channels as cheap substreams,
  and the monitor reference that is correlation token and liveness
  subscription at once.
