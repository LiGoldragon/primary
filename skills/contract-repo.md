# Skill — contract repos

*The wire contract between Rust components lives in a dedicated
repo of typed records, not duplicated across consumer crates.
Every component on the same fabric depends on the same contract
crate; rkyv archives produced by one are readable by every
other.*

---

## What this skill is for

When two or more Rust components need to **signal** each other
over a wire — a Unix socket, TCP, message bus, named pipe,
mmap region — the record types they exchange live in a
**contract repo**: one crate, one home, every consumer pulls
it as a dependency. This skill is *when* you reach for that
pattern, *what* belongs in the contract crate, and *how* it
relates to layered protocols and human-facing NOTA projections.

**Signaling** is the workspace verb for inter-component
communication via length-prefixed rkyv archives. A contract
repo is the typed vocabulary of one signaling fabric — the
shared `Frame`, the closed enum of payloads, the handshake,
the auth proofs. Components that signal each other depend on
the same contract repo.

The principle is `~/primary/ESSENCE.md` §"Perfect specificity at
boundaries" applied across processes. The Rust enforcement
sits on top of `~/primary/skills/rust-discipline.md` §"redb +
rkyv — durable state and binary wire" — that skill defines
the rules; this one names how the contract is *organised* in
repos.

The canonical workspace example is **signal**
(`~/primary/repos/signal`) — the wire-protocol crate of the
sema-ecosystem, and the namesake of the pattern. Read its
`ARCHITECTURE.md` once before designing a new contract repo;
the shape is concrete there.

---

## Why a contract repo exists

rkyv archives interoperate **only** when both ends compile
against the same types with the same feature set. Three
consequences make a shared crate the right home:

- **Schema agreement.** A `Frame` defined in one component and
  redefined in another is two types — the bytes don't round-
  trip even if the field lists look identical. The contract
  crate is the single definition.
- **Derive sharing.** Wire-format derives (rkyv's
  `Archive`/`Serialize`/`Deserialize`, `bytecheck`) and any
  project-specific derives all live with the type.
  Re-deriving in each consumer is dead code at best, drift
  at worst.
- **Front-end stability.** When a layered effect crate adds
  per-verb payloads (e.g. signal-forge over signal), front-end
  clients that depend only on the base contract don't recompile
  on layered-crate churn. Audience-scoped compile-time
  isolation.

A workspace pattern that doesn't follow this:
- types defined in component A, copy-pasted into component B,
- two components own "the same" wire format,
- bytes silently drift on schema changes.

This is exactly the class of bug rkyv's strict layout makes
invisible (no parse error, just wrong values).

---

## What goes in a contract repo

```
contract-repo/
├── src/
│   ├── lib.rs        — module entry + re-exports
│   ├── frame.rs      — Frame envelope, encode/decode, error type
│   ├── handshake.rs  — ProtocolVersion + handshake exchange
│   ├── auth.rs       — auth-proof types (capability tokens, signatures)
│   ├── request.rs    — Request enum (closed; per-verb dispatch)
│   ├── reply.rs      — Reply enum (closed; matches request kinds)
│   ├── <verb>.rs     — per-verb typed payloads
│   ├── <kind>.rs     — domain record kinds + paired *Query types
│   └── error.rs      — crate Error enum (thiserror)
├── tests/            — round-trip per record kind, per verb
├── Cargo.toml        — pinned rkyv feature set, versioned
└── ARCHITECTURE.md   — what's owned, what's not, schema discipline
```

The contract crate **owns**:

- The `Frame` envelope and its `encode` / `decode` methods.
- Length-prefix framing rule (4-byte big-endian per archive).
- Handshake + protocol version + compatibility rule
  (major-exact / minor-forward, or whatever the project picks).
- Auth-proof types and capability-token shape.
- The closed enum of request kinds + paired reply kinds.
- Per-verb typed payloads (closed enums of typed kinds — no
  generic record wrapper, no `Unknown` variant).
- The version-skew guard's known-slot record (schema +
  wire-format version).
- A complete round-trip test per record kind.
- Reserved record heads stay reserved workspace-wide. No
  domain type defines a record kind named `Bind` or
  `Wildcard`; those heads belong to
  `signal_core::PatternField<T>` dispatch.

It **does not own**:

- Daemon code. No actors, no runtime, no `tokio`.
- Component-internal state. Each daemon's redb tables, its
  reducer state, its supervisor tree are private.
- Logic that interprets the records. Validation pipelines,
  routing rules, gate decisions stay in the daemons.
- NOTA projection policy. Human-facing projections use NOTA;
  the contract crate's wire is binary.
- Configuration. `Cargo.toml`, `flake.nix`, deployment.
- `serde`. Contract types may *also* derive serde for debug
  rendering, but the contract is rkyv-on-the-wire.

---

## The layered pattern

When a wire protocol has audience-scoped concerns — verbs that
only a subset of components care about — those verbs land in a
**layered effect crate**, not in the base contract:

```mermaid
flowchart TB
    subgraph contract["base contract crate"]
        frame["Frame envelope"]
        hs["handshake + protocol version"]
        auth["auth proofs"]
        front["front-end verbs<br/>(seen by every client)"]
    end

    subgraph layered["layered effect crate"]
        verbs["per-verb payloads<br/>(narrow audience)"]
    end

    layered -. depends on .-> contract

    fe["front-end clients"] --> contract
    daemon["daemon"] --> contract
    daemon --> layered
    backend["backend"] --> contract
    backend --> layered
```

The pattern (signal-forge over signal is the canonical
example): the layered crate **re-uses** the base contract's
`Frame`, handshake, and auth, and **adds** its own per-verb
payload enum. New layered verbs land in the layered crate;
front-end clients that depend only on the base contract don't
recompile.

Use a layered crate when:

- The verbs have a narrow audience (sender + receiver +
  maybe one transitional caller, not "every client").
- The base contract would otherwise grow to absorb effect-
  specific concerns that don't belong on the front-end
  surface.
- Recompile cost across the front-end surface is real (signal
  has many front-end clients; recompile churn matters).

Don't pre-layer. A second contract crate's layered shape
becomes obvious after one effect-bearing leg is real and a
second is being added.

---

## Versioning is the wire

The contract crate's semver **is** the wire's semver:

- A bumped major means breaking layout or breaking semantics.
  Every consumer upgrades together. Coordinated upgrade.
- A bumped minor means a backward-compatible addition (new
  variant in a forward-tolerant enum, new optional field).
  Forward-compatible enums must be marked open in their
  decoding strategy; closed enums never accept minor
  additions.
- A bumped patch is documentation, tests, internal cleanup.
  No layout change, no semantic change.

Pin the contract crate version in every consumer's
`Cargo.toml`. Don't `git = "..."` against `main` for
production wire — `main` moves under your feet. Use a tag
or a version-pinned crates.io release.

The **version-skew guard** is part of the wire: a known-slot
record at the canonical key carrying `(schema_version,
wire_version)`, checked at boot. Hard-fail on mismatch. The
guard runs *before* the daemon starts handling traffic; a
mismatch is a coordinated-upgrade signal, not a runtime
error to recover from.

---

## How NOTA fits

NOTA is the project's only text syntax. Nexus is a NOTA-using
request/message surface, not a second syntax. In practice,
request/message text usually means Nexus records written in NOTA
syntax; configs and convenience CLIs may use direct NOTA records.
NOTA is **not the inter-component wire**. The contract crate carries
rkyv types; NOTA appears only at boundaries that touch a human or a
text projection:

| Boundary | Format |
|---|---|
| Component ↔ component (Rust ↔ Rust) | contract-crate types via rkyv frames |
| CLI ↔ daemon | NOTA on argv/stdin (human types it), often through a convenience CLI that constructs the Nexus wrapper; daemon parses to typed contract record |
| Daemon ↔ harness terminal | Pre-harness component projects typed record to NOTA before write |
| Audit logs / debug dumps | NOTA projection |

The CLI, the router, and the pre-harness component are the
*only* parts of the system that touch NOTA. Everywhere else, a
component holds typed records (in memory) or rkyv archives (on
disk and on the wire). This is what `~/primary/skills/rust-
discipline.md` §"NOTA — the human-facing projection" already
states; the contract repo is how that discipline gets enforced
at the repo level.

---

## When to introduce a contract repo

Indicators the moment is now, not "later":

- A second component is about to read or write the same wire
  bytes. Two components ⇒ contract crate.
- The first component had its types in a private module. As
  soon as the second component needs them, hoist to a
  contract repo.
- A schema change is being planned and the change needs to
  land in two crates simultaneously. The pain is the signal.

Indicators the moment is **not yet**:

- One daemon, no clients, no other component reads its bytes.
  Keep the types private until a second consumer appears.
- Prototyping a serialization shape; the format will change
  three times this week. Stabilise first, hoist after.

The cost of premature hoisting is a contract repo with one
consumer — fine, low overhead. The cost of late hoisting is a
silent schema-drift bug that survives review because both
copies of the type *look* the same. Err early.

---

## Kernel extraction trigger

A contract repo grows in two distinct ways:
- **Domain growth:** new record kinds, new typed payloads,
  new query shapes — all within the original audience.
- **Audience growth:** a *second* domain wants to speak the
  same wire conventions. The first domain's repo now carries
  both the universal kernel (Frame, handshake, auth, version,
  the verb spine) *and* its own record kinds.

The audience case triggers extraction. **When two or more
domains share the kernel, extract the kernel into its own
crate** so neither domain's records contaminate the other's
namespace.

The trigger:

```mermaid
flowchart TB
    one["one domain<br/>(kernel + records together)"]
    two["second domain appears<br/>(needs kernel; doesn't need first domain's records)"]
    extract["extract kernel<br/>(both domains depend on kernel only)"]

    one --> two --> extract
```

Concrete: `signal` originally held both the sema-ecosystem's
kernel (Frame, handshake, universal verbs) and Criome's
record kinds (Node, Edge, Graph). When a second domain
(`signal-persona`) needed the same kernel, leaving everything
in `signal` would have forced `signal-persona` to depend on
a Criome-flavored crate — exactly the boundary confusion
this skill exists to prevent.

The extraction:
- New crate (`signal-core`, or whatever the project calls it)
  holds Frame, handshake, auth, version, the universal verb
  spine, the typed identity records (Slot, Revision).
- The original crate (`signal`) becomes the first domain's
  *vocabulary* over the kernel — Criome's records, Criome's
  per-verb payloads.
- The new domain (`signal-persona`) is also a *vocabulary*
  over the kernel — Persona's records, Persona's per-verb
  payloads.

After extraction, both domains depend only on the kernel,
not on each other. New domains can join the family without
naming-confusion.

**When NOT to extract early:** with a single domain, the
kernel-and-records-together shape is fine. Don't pre-extract
"in case" a second domain shows up. The cost of a one-domain
contract crate is zero; the cost of a kernel crate with no
second consumer is one extra artifact to maintain. Wait for
the second domain.

The signal-forge / signal-arca pattern (per the layered-
effect-crate section above) is *complementary* to kernel
extraction: a layered crate adds per-verb payloads for a
narrow audience, but it depends on the same kernel as the
base contract. After extraction, signal-forge depends on the
kernel directly *plus* the base contract for record kinds it
references.

---

## Examples-first round-trip discipline

Every record kind in a contract repo lands as **a concrete
text example + a round-trip test** before its Rust definition
is final.

The order of work:

```mermaid
flowchart LR
    example["1. write canonical text example"]
    type["2. derive Rust type from example"]
    rt["3. round-trip test (text → typed → text)"]
    archive["4. rkyv archive round-trip"]

    example --> type --> rt --> archive
```

The discipline:

1. **Write the canonical text example.** Before defining the
   Rust struct, write what the record looks like in nexus
   text. The example exercises the field positions, the
   typed enum variants, the optional fields. If the example
   is awkward, the type is wrong — fix the type before
   coding.
2. **Derive the Rust type from the example.** The Rust
   struct's field order matches the text example's positional
   order. The closed enum's variant set matches what the
   example positions can hold. The PatternField fields
   match the positions where binds and wildcards appear.
3. **Round-trip test as the first test.** The first test
   ever written for a new record kind is `text → typed →
   text` and asserts equality. If the round-trip doesn't
   close, the codec or the type definition has a bug.
4. **rkyv archive round-trip as the second test.** The
   record encodes to rkyv bytes, decodes back, and equals
   the original. Per-feature-set parity (per
   `~/primary/repos/lore/rust/rkyv.md`) is checked
   independently.

Why this order:
- The text example is the **falsifiable specification.** A
  Rust definition without an example is unverified
  guesswork.
- The round-trip test catches encoder/decoder asymmetry
  immediately.
- A new agent can read the example file before reading any
  Rust source and know what the record kind is *for*.

In contract crate practice, this means each record kind ships
with:
- An entry in the canonical examples file (one canonical text
  form per kind).
- A test in `tests/<kind>.rs` exercising round-trip in both
  directions.
- The Rust definition in `src/<kind>.rs`.

If the example file is empty, the contract crate is
incomplete — even if all the Rust definitions compile.

---

## Naming a contract repo

The contract crate is the *protocol the components speak*.
The naming hierarchy reflects the relationship to `signal`:

### `signal-<consumer>` — layered effect crate (the prefix form)

When the contract is **layered atop `signal`** — re-uses
signal's `Frame`, handshake, and auth, adds per-verb payloads
for a narrower audience — the canonical name is
**`signal-<consumer>`**:

- `signal-forge` — criome ↔ forge effect verbs
- `signal-arca` — writers ↔ arca-daemon effect verbs
- `signal-persona` — Persona's wire, layered atop signal

Same shape signal/criome already established. The prefix
order (`signal-` first, consumer name second) is read as
*"this is signal, scoped to consumer."* Front-end clients
that depend only on `signal` don't recompile when a layered
crate churns.

### `<project>-signal` — independent base contract (the suffix form)

When the project's wire is **its own base contract** — owns
its own `Frame`, handshake, auth — the name is
**`<project>-signal`**:

- `signal` — the base contract of the sema-ecosystem (named
  without prefix because it IS the base)

Use this only when the project is genuinely a separate
signaling fabric with its own envelope and auth shape.
Almost always, what feels like "a new ecosystem" is
better modelled as a layered crate atop signal.

### `<project>-protocol` / `<project>-contract` / `<project>-wire`

When the project deliberately uses a **different wire shape
than signal-family** — different framing, different envelope,
no convergence intended — name it `<project>-protocol`,
`<project>-contract`, or `<project>-wire`. These are escape-
hatch names for projects that explicitly aren't part of the
signal family.

### Choosing

```mermaid
flowchart TD
    q1{"Re-uses signal's<br/>Frame + handshake + auth?"}
    q2{"Has its own<br/>base envelope?"}
    layered["signal-&lt;consumer&gt;<br/>(layered effect crate)"]
    base["&lt;project&gt;-signal<br/>(independent base contract)"]
    other["&lt;project&gt;-protocol<br/>(non-signal-family)"]

    q1 -->|yes| layered
    q1 -->|no| q2
    q2 -->|yes, signal-shaped| base
    q2 -->|no, deliberately different| other
```

The default is `signal-<consumer>` — the layered shape is
how the workspace's signaling fabric grows.

Don't pick names that name the consumer's *internals*
(`<project>-types`, `<project>-shared`). The repo isn't a
bag of utilities — it is the spoken protocol.

---

## Common mistakes

| Mistake | What it looks like | Fix |
|---|---|---|
| Types redefined per consumer | Each daemon has its own `Frame` struct with the same fields | One contract crate; every consumer depends on it |
| `serde_json` between Rust components | "We'll switch to rkyv later" | rkyv from the start; if iterating fast, prototype with rkyv too |
| `path = "../contract"` in `Cargo.toml` | Local sibling reference | `git = "..."` with a tag, or a published crates.io version. Cross-crate `path = "../sibling"` is forbidden per ESSENCE §"Micro-components" |
| Contract crate carries logic | Validation, routing, or reducer code in the contract | Move logic to the daemon; contract holds types only |
| Contract crate has a runtime dependency | tokio, ractor, nix system bindings | Contract crate depends only on rkyv + thiserror + (optionally) the project's derive crate |
| New wire verb added to the base contract because it was easy | Front-end clients now recompile on every effect-side change | Add a layered effect crate; base stays stable |
| No `ARCHITECTURE.md` in the contract repo | Schema discipline is unwritten | Every contract repo carries `ARCHITECTURE.md` per `~/primary/lore/AGENTS.md`; schema discipline is the load-bearing part |
| Open enum where closed was meant | Adding `Unknown` variant "for forward compatibility" | Closed enum + coordinated upgrade. The `Unknown` is a polling-shaped escape hatch |

---

## See also

- `~/primary/ESSENCE.md` §"Perfect specificity at boundaries"
  — the principle the contract repo encodes.
- `~/primary/skills/rust-discipline.md` §"redb + rkyv" — the
  Rust-specific rules for the binary contract; this skill
  organises those types into repos.
- `~/primary/skills/micro-components.md` — every component is
  its own repo; the contract crate is the typed protocol
  between them.
- `~/primary/skills/push-not-pull.md` §"Subscription
  contract" — the producer contract for push primitives;
  contract crates own the subscription frame types.
- `~/primary/repos/signal/ARCHITECTURE.md` — the canonical
  worked example.
- `~/primary/repos/signal-forge/ARCHITECTURE.md` — the
  canonical layered effect crate.
- `~/primary/repos/lore/rust/rkyv.md` — the tool reference
  (cargo features, derive aliases, encode/decode API).
- `~/primary/repos/lore/rust/style.md` — Cargo.toml
  conventions, cross-crate dependencies, pin strategy.
