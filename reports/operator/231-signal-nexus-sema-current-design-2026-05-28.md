# 231 - Signal, Nexus, SEMA Current Design

Date: 2026-05-28  
Lane: operator  
Component: reactive runtime / `schema-rust-next`

## Current Rule

Signal, Nexus, and SEMA are the three reactive planes of a daemon.

Signal is the communication plane. Nexus is the execution and mail-keeper
plane. SEMA is database work: durable state mutation and reads, currently over
the `.redb` store and conceptually eligible for a future `.sema` extension.

The schema-emitted Rust types are the nouns. Runtime behavior attaches to those
types and to data-bearing engine objects through traits; it does not route
through free helper functions.

## Message Flow

```text
Signal message
  -> Signal engine validates and pushes
  -> Nexus engine owns in-flight mail and decides work
  -> SEMA engine performs database work
  -> Nexus resolves mail from SEMA reply
  -> Signal reply returns to caller
```

The origin route is automatic metadata on root envelopes. It is not authored in
the schema and it stays with the message as the message crosses planes.

## Emitted Shape

`schema-rust-next` emits plane envelopes:

```rust
pub struct Signal<Root> {
    pub origin_route: OriginRoute,
    pub root: Root,
}

pub struct Nexus<Root> {
    pub origin_route: OriginRoute,
    pub root: Root,
}

pub struct Sema<Root> {
    pub origin_route: OriginRoute,
    pub root: Root,
}
```

It also emits a matched plane enum so code can match the plane and the carried
message together:

```rust
pub enum Plane<SignalRoot, NexusRoot, SemaRoot> {
    Signal(signal::Signal<SignalRoot>),
    Nexus(nexus::Nexus<NexusRoot>),
    Sema(sema::Sema<SemaRoot>),
}
```

The envelope carries the plane-level route. Payloads remain schema-generated
types such as `SignalRequest`, `NexusRequest`, and `SemaRequest` until the
per-plane module split can make names like `signal::Input`, `nexus::Input`,
and `sema::Input` collision-free.

## Engine Traits

Generated engine traits enforce the intended order:

```rust
pub trait NexusEngine {
    type Reply;
    type Error;
}

pub trait SemaEngine {
    type Reply;
    type Error;
}
```

The generated dispatch methods pass typed mail objects through those traits.
Tests assert the chain uses schema-emitted payloads and typed outputs rather
than string assertions.

## Code Witness

The large triad fixture uses the same authored schema syntax as the schema
report:

```nota
((SignalIn SignalRequest)
 (NexusIn NexusRequest)
 (SemaIn SemaRequest)
 Heartbeat)
((SignalOut SignalReply)
 (NexusOut NexusReply)
 (SemaOut SemaReply)
 (Rejected Rejected))
{
  SignalRequest ((RecordIntent RecordIntent) (ObserveIntent ObserveIntent))
  NexusRequest ((PushSignal PushSignal) (PushSemaResult PushSemaResult) ResolveMail)
  SemaRequest ((WriteEntry WriteEntry) (ReadEntries ReadEntries))
  RuntimeEvent ((MailSent MailSent) (MessageCommitted MessageCommitted))
  RecordSet [(records [Entry]) (byTopic {Topic RecordIdentifier})]
}
```

`schema-rust-next` generates Rust from that fixture and the generated snapshots
compile in tests.

## Current Proof

Commands passed in `/git/github.com/LiGoldragon/schema-rust-next`:

```sh
cargo fmt && cargo test
nix flake check --print-build-logs
```

Commit `7244e8c1` (schema-rust fixture cleanup) removed the old
assembled-schema fixture comparisons. Commit `38114fc2` (`schema-rust: use
native schema collection syntax`) updated schema fixtures, regenerated Rust
snapshots, and added Nix guards against obsolete collection macro forms and
same-name star suffix syntax.
