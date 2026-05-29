# 423 — Signal / Nexus / Sema: the reactive plane layer

*Kind: Current-design spec · Component: signal/nexus/sema (reactive schema → emitted runtime) · Topics: signal, nexus, sema, planes, envelopes, origin-route, engines, type-safety · 2026-05-28*

*One of three current-design component reports — [[421-nota]] is the substrate,
[[422-schema]] is the schema layer this builds on. Grounded in the real emitter
output in `schema-rust-next/src/lib.rs` and records 964/982 (three schema
types/planes), 1028 (trait-ordered engines), 1029 (origin route is automatic
metadata), 1037 (plane envelopes), 1038 (auto origin-route on root), 1042
(plane-scoped Input/Output), 1052 (plane is one data-carrying enum).*

## 1. Base schema vs reactive schema

A **base schema** describes data only — the type model of [[422-schema]]. A
**reactive schema** adds a reactive surface as its **roots** — the named
entry-point set (e.g. an input root and an output root), held in the `roots`
section of the assembled `Asschema` (record 1155); a base schema declares no
roots. A reactive schema lives across **three planes** — signal, nexus, sema —
and the runtime emitted from it threads a message through all three.

## 2. The three planes and their flow

The planes are ordered: a message enters at **signal**, is pushed to **nexus**,
and is applied at **sema**, with the reply travelling back out. The order is
enforced in the type system by trait-ordered engines (1028): each engine's
method takes the downstream engines as generic parameters and yields a token the
next stage requires, so a stage cannot be skipped.

```text
SignalEngine::push_to_nexus(Signal<Input>, &NexusEngine, &SemaEngine) -> Signal<Output>
NexusEngine ::receive_pushed_signal(Nexus<…>, &SemaEngine)            -> Nexus<…>
SemaEngine  ::apply(Sema<Input>)                                      -> Sema<Output>
```

## 3. The plane envelope — marks the plane, carries the route

Each plane has an **envelope**: a thin generic container that says "this message
belongs to this plane" (1037). The emitter generates one per plane, and it is
where the auto-created origin route lives (1038):

```rust
pub struct Signal<Root> { pub origin_route: OriginRoute, pub root: Root }
pub struct Nexus<Root>  { pub origin_route: OriginRoute, pub root: Root }
pub struct Sema<Root>   { pub origin_route: OriginRoute, pub root: Root }
// each with new(), origin_route(), root(), into_root()
```

Two properties fall out of this one shape:

- **Plane type-checking.** Because the engine signatures take and return the
  matching envelope (`Signal<…>`, `Nexus<…>`, `Sema<…>`), a signal-plane message
  cannot be passed where a nexus or sema message is expected — a compile error,
  not a runtime check. Combined with the order enforcement of §2, the trait
  chain is un-mis-wireable on both axes at once: you can neither skip a step nor
  cross a plane.
- **Auto-created origin route.** The schema author never writes `origin_route`;
  the emitter adds it to every root plane object (1029/1038). It is minted at
  signal ingress, carried onto the nexus and sema roots and back onto the reply
  roots, so a reply correlates to its originating query. It is a distinct minted
  id, **not** the message identifier reused.

The payloads shed their plane prefix (1042): each plane owns its own `Input` /
`Output` (plane-module-scoped), so the plane is named once — `Signal<Input>`,
not `Signal<SignalInput>` — aligning with three-schema-languages-as-modules
(982).

## 4. Plane identity is one data-carrying enum

The per-plane distinct types above are the *compile-time* view. When the runtime
must **branch** by plane — a received message whose plane it must discover — the
plane is one data-carrying enum (1052), emitted as:

```rust
pub mod schema {
    pub enum Plane<SignalRoot, NexusRoot, SemaRoot> {
        Signal(Signal<SignalRoot>),
        Nexus(Nexus<NexusRoot>),
        Sema(Sema<SemaRoot>),
    }
    // origin_route() matches the variant and delegates to the envelope
}
```

Matching the variant both identifies the plane and yields the message. There is
**no separate `kind` tag** beside the envelope: the type (compile-time) or the
variant (runtime) already encodes the plane, so a duplicate tag is the
redundancy 1052 forbids.

## 5. Where it lives

The envelopes, the `Plane` enum, and the auto-created `origin_route` are all
**emitted** by `schema-rust-next` from a reactive assembled schema — the same
emission pass that produces the data structs of [[422-schema]]. The runtime
(`spirit-next` and other component daemons) consumes the emitted types: it
receives a `Plane` message, routes by variant, threads the matching envelope
through the trait-ordered engines, and replies on the same route. So the
reactive design is not hand-written per component — it falls out of declaring a
schema reactive and emitting it.

## 6. Pointers

Records 964/982 (three planes / schema-languages-as-modules), 1028 (trait-ordered
engines), 1029 (origin route automatic), 1037 (envelopes), 1038 (auto-route on
root), 1042 (plane-scoped Input/Output), 1052 (plane is one data-carrying enum).
Substrate: [[421-nota]]. Schema layer: [[422-schema]].

## 7. Testing — reactive fixtures (record 1180)

The reactive layer is tested the same way: a plane message is a real
`.sema` / `.signal` / `.nexus` fixture file (never an inline string), loaded with
`fixture!` ([[421-nota]] §7), decoded into the emitted envelope, and checked for
the round-trip and origin-route correlation:

```nota
; tests/fixtures/observed.sema   — a Sema<Output> envelope: origin_route then root
(41 (Observed (RecordSet [(records [])])))
```
```rust
#[test]
fn sema_reply_preserves_origin_route() {
    let message = Sema::<Output>::from_nota(fixture!("observed.sema")).unwrap();
    assert_eq!(message.origin_route(), OriginRoute(41));
    assert_eq!(message.to_nota(), fixture!("observed.sema").trim());   // envelope round-trips
}
```

So the envelope, the auto `origin_route`, and `schema::Plane` routing are all
exercised against real fixture files. The fixture shows the envelope's two
positional fields — the route, then the plane root — as plain NOTA.
