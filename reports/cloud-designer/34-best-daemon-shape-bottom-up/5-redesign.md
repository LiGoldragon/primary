# 5 — synthesis: the best daemon shape (intent-grounded)

cloud-designer, 2026-06-07. The bottom-up redesign, zero compatibility. Three
independent proposals (`1`/`2`/`3`), three adversarial judges (`4` in the run
record), and — decisively — the standing Spirit intent that the judges split
without consulting. The winner is **Proposal C, corrected to the intent-decided
three-plane-engine surface**: a sync thread-per-request daemon driving the
Signal/Nexus/SEMA engine traits, with everything else generated.

## The pivotal fork is settled by intent, not by me

The judges split on actor-native (B) vs thread-per-request (A/C). All three said
"surface it to the psyche." But it does not need surfacing as an open fork —
**standing intent already resolves it**, and inferring otherwise would be the
inference-forbidden error:

- `czw0` (Decision): the generated Signal/Nexus/SEMA engine traits carry **minimal
  lifecycle hooks (on_start/on_stop)**; **full actor mailbox, backpressure, and
  runtime-control traits stay DEFERRED**.
- `59dr` (Decision): backpressure + deeper runtime-control is **deferred future
  runtime work, not the current slice**.
- `opvx` (Decision): runner concurrency mode is a **runtime/deployment config
  choice**; the **public contract does not encode how parallel a daemon runs**.

Proposal B *is* the deferred thing — it makes the daemon a kameo actor system with
mailboxes now. That contradicts `czw0`/`59dr`. The actor-density truth-pin and
`skills/actor-systems.md` ("schema-driven daemons are Signal/Nexus/SEMA actors,
Nexus is the async mail keeper") describe the **eventual** actor-dense shape; the
current slice explicitly defers the mailbox machinery. This is the workspace's own
"today vs eventually" boundary (`ESSENCE`): **today** is sync three-plane engine
traits with lifecycle hooks; **eventually** is full actor density. B is the right
*eventual* picture and a real liability *now* (async-rewrite of five 100%-sync
engines for machinery intent has deferred). C is the *today* shape.

The judges' verdict agrees on the merits independent of intent: C wins Clarity
(the top ESSENCE criterion) and Beauty (2 of 3 judges); B wins Introspection but
its proponent judge conceded B loses Clarity and rests on a false premise (kameo
is in **zero** Cargo.toml; `message`, the supposed actor, is a synchronous-blocking
`Mutex<Engine>` stamp-and-forward — a mailbox makes its outbound forward *worse*).

## Guidance-hygiene flag (a real inconsistency, not mine to silently resolve)

`skills/actor-systems.md:86` states schema-driven daemons **are** Signal/Nexus/SEMA
actors with mailboxes ("Nexus is the async mail keeper… if that flow appears as a
group of helper functions, the actor boundary has been erased"). `czw0`/`59dr`
**defer** exactly that mailbox machinery. The skill describes the eventual shape as
if it were current; the intent slice defers it. The skill should be marked
today-vs-eventually so future agents (and judges) stop reading it as a mandate to
build kameo daemons now. Flagged for the skill owner; not silently edited here.

## The design (Proposal C, corrected to the three-plane engine surface)

**Concurrency — sync thread-per-request, and parallelism is runtime config
(`opvx`).** The `triad-runtime` accept loop stays serial; the generated runner
offloads each request onto `BoundedWorkers` and returns immediately; each worker
builds a fresh per-request engine over a shared `Arc<Shared>`, so there is no
shared mutable state to serialize (this is what lets a multi-minute nix build never
block queries — the lojix `2alg` property). **Correction to all three proposals
per `opvx`:** the worker-pool capacity is a `DaemonConfiguration`/deployment datum,
**not** a schema field — the contract does not encode how parallel the daemon runs.

**The hook surface is the three plane engine traits, not a single `decide()`
(`rpr5`/`czw0`/`h3u7`).** The proposals abstracted the engine as one
`decide(SignalInput)->SignalOutput`; the intent-decided shape is that a component
implements the **Signal / Nexus / SEMA engine traits** (plus the effect handler and
budget-exhausted reply, `rpr5`) on **real data-bearing types** (the redb handle,
config, child refs — `actor-systems.md` "engine traits live on real data-bearing
types", never a ZST namespace). `triad_main` (the shared runner, implemented per
`ocu7`) drives them. lojix's `SchemaRuntime` (impl `NexusEngine`+`SemaEngine` over
`Arc<Store>`) is already exactly this. The generated transport feeds the plane
engines; the component never hand-writes accept/decode/frame/tier-split.

**Two archetypes, selected by a real semantic — not a compatibility hedge.**
`ReplyOnce` (request/reply) and `ReplyThenSubscribe` (streaming, a strict superset
adding one owned noun: the writer registry). The selector is `schema.streams()`
being non-empty — a genuine request disposition `opvx` explicitly permits
("semantic constraints… read fanout… when those semantics are real"), the same
`emits_stream` bit the emitter already computes. Request/reply stays **pure**: no
registry, no subscription hooks in its trait. This is the Beauty test read
correctly — streaming is its own clean superset, not dead weight carried by every
daemon (the flaw in A's one-archetype thesis).

**Meta/owner tier — one typed model, no escape hatch.** The owner contract is a
typed second leg of the one `nexus::SignalInput` root (`MetaInput`), arriving at
the same plane engines. `handle_meta_stream` (the raw-`UnixStream` escape hatch) is
**deleted** from the generated surface for cloud/spirit/lojix; spirit's `Configure`
becomes `MetaInput::Configure` in a typed `meta-signal-spirit` contract. The owner
tier differs from the working tier in exactly two generated ways: the fail-closed
peer-cred gate and the `0o600` socket-mode default.

**Fail-closed owner auth, Required by default (graft from A, fixing C's footgun;
`9v7h`).** `ConnectionContext::from_stream` (kernel `SO_PEERCRED`, safe `rustix`,
`forbid(unsafe_code)` kept) is read on every accepted connection on both tiers and
threaded into the engine as a **typed `RequestOrigin`** (graft from A/B: peer
identity is request *data*, minting provenance — replacing lojix's hardcoded
`OriginRoute(0)` and message's payload-derived origin). On the owner tier,
`OwnerAuthority::Required` is the **default** (not an `Option<u32>` that no-ops on
`None` — that would fail *open*): a peer uid mismatch **rejects the connection
before decode/engine**. Owner uid is deployment config.

**Transport always bounded.** The generated transport always builds
`LengthPrefixedCodec::new(MaximumFrameLength::new(bound))` (default 8 MiB) and calls
`set_read_timeout` (default 10 s) before every read; the 4 GiB `::default()` codec
is never emitted.

**Introspection — graft B's strongest idea into the thread model.** Rather than a
mailbox, emit a **typed trace witness per request** (tier + live permit count +
decode/decide/encode spans) over the existing trace socket — the trace plane is
already intent (`xqkv`, `cmsx`, ESSENCE "the trace edge"). This gives
observability-by-construction within the sync spine, answering the one criterion B
won, without the deferred mailbox machinery. The `BoundedWorkers` permit gauge is
the live-load readout.

## What every component changes (all five offended, per `ax2k`)

| Component | What changes |
|---|---|
| `lojix` | Whole ~280-line `daemon.rs` deleted; `validate_owner_socket_mode` deleted (emitted peer-cred gate is strictly stronger). Keeps only `Store` + the three plane-engine impls (the nix effect plane). Pure win. |
| `cloud` | `handle_meta_stream` escape hatch deleted; frame/timeout constants become runtime config; gains the `BoundedWorkers` offload it lacked (was serial). Second proof the shape is shared. |
| `message` | `Mutex<MessageEngine>` and the `&mut self`-engine model deleted; engine built fresh per request; gains real parallelism (N blocking forwards no longer queue behind one lock). The "kameo actor" framing is dropped as never-having-been-true (no kameo dep; synchronous blocking forward). |
| `spirit` | `Configure` escape hatch + `MetaSignalTransport` deleted → typed `meta-signal-spirit`; long-lived `&self` engine → per-request over shared redb; subscription hooks become the `ReplyThenSubscribe` archetype's (reduce toward A's 3-method set if token-extraction is schema-derivable). |
| `repository-ledger` | The most: entire raw-`UnixListener` + `thread::spawn` + `Arc<Mutex<Store>>` daemon + hand-codec deleted; joins the emitter for the first time (must author a `signal-*`/`meta-signal-*` contract). Its 2-second spool-ingest loop becomes a declared runtime maintenance task (a periodic worker), not a free `thread::spawn` — the one genuine non-request shape, named explicitly. |

## What stays open (and is genuinely the psyche's, if anything)

The actor fork is **resolved** (deferred per `czw0`) — I am not re-asking it. Two
real items remain:

1. **Confirm the today/eventually framing** — is "today = sync three-plane engine
   traits, full actor mailboxes deferred (`czw0`); eventually = actor-dense" still
   the intended trajectory? This is a light confirmation, not an open fork; the
   design proceeds on it.
2. **`repository-ledger`'s contract authoring** — joining the emitter means it
   needs a `signal-*`/`meta-signal-*` schema; in scope for this redesign or a
   follow-on?

This redesign is the design; no emitter code is landed. The staged plan from
`33/6` still holds mechanically (triad-runtime seam → emitter declaration → emitter
spine → per-component adoption), now targeting the C shape with the three-plane
engine surface, runtime-config concurrency, Required-by-default owner auth, and the
trace-witness introspection — and with **no** opt-in/byte-stable scaffolding.
