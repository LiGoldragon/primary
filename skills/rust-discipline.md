# Skill — Rust discipline

*Behavior lives on types. Domain values are typed. Boundaries take
and return one object. Errors are enums you implement by hand.*

---

## What this skill is for

When you write or review Rust in this workspace, this skill is the
discipline. It is the Rust-specific enforcement of the cross-language
rules in this workspace's `skills/abstractions.md`,
`skills/naming.md`, `skills/beauty.md`, and `skills/micro-components.md`.

For toolchain reference (Cargo.toml shape, cross-crate dependencies,
git-URL deps + `cargoLock.outputHashes` pattern, pin strategy, Nix
packaging), see lore's `rust/style.md` and lore's
`rust/nix-packaging.md`. This skill is *how to write*; lore is *how
the toolchain works*.

---

## The rules in one sentence

**Behavior lives on types. Domain values are typed. Boundaries take
and return one object. Errors are enums you implement by hand.**

---

## Methods on types, not free functions

The only free function in a binary crate is `main`. Reusable
behavior is a method on a type or a trait impl. Test helpers are
methods on a fixture struct.

```rust
// Wrong
pub fn parse_cert(pem: &str) -> Result<Cert, Error> { … }

// Right
impl Cert {
    pub fn from_pem(pem: &str) -> Result<Self, Self::Error> { … }
}
```

A small private helper inside one module is fine if it is
genuinely local (`fn hex(h: &Hash) -> String` next to a single
`Display` impl). Anything that smells reusable becomes a method.

For the cross-language version of this rule (the same idea
language-neutrally, plus the LLM-codegen reasoning and the
principled exceptions), see this workspace's
`skills/abstractions.md`. This section is the Rust enforcement.

**The deeper consequence**: free functions let the agent skip
creating the type that should own the behavior. If you're tempted
to write

```rust
// Wrong
pub fn parse_query(text: &str) -> Result<QueryOp, Error> { … }
```

the rule forces you to ask: *what type owns query parsing?* The
answer is `QueryParser`, and the rule's pressure makes that type
exist:

```rust
// Right
pub struct QueryParser<'input> { lexer: Lexer<'input> }

impl<'input> QueryParser<'input> {
    pub fn new(input: &'input str) -> Self { … }
    pub fn into_query(self) -> Result<QueryOp, Error> { … }
}
```

The rule of thumb: **every reusable verb belongs to a noun**. If
you can't name the noun, you haven't found the right model yet —
keep looking until you can.

---

## No ZST method holders

A `pub struct Foo;` whose `impl Foo` is just a parking lot for
functions that do real work on data they don't carry is a free
function in namespace clothing. The ZST is a label, nothing more —
the type doesn't track what the work operates on, only what it's
named after. This is the **methods-on-types** rule evaded one
level deeper: the verb got attached to *something*, but the
something is hollow.

When you see this, don't rename `Foo`. Don't accept the smell.
**Step back and find the noun.** A ZST-with-methods is the visible
scar of "I had a verb but couldn't find a noun, so I created a
fake noun to hold the verb." The right noun is a type that holds
the data the verb reads or writes — and it may not exist yet.
Invent it. Naming the right object is often the load-bearing
design decision the prior thinking missed.

```rust
// Wrong — ZST as a folder for free functions
pub struct CertParser;

impl CertParser {
    pub fn parse_pem(pem: &str) -> Result<Cert, Error> { … }
    pub fn parse_der(der: &[u8]) -> Result<Cert, Error> { … }
    pub fn fingerprint(cert: &Cert) -> Hash { … }
}

// Right — the verbs belong on the noun whose data they touch
impl Cert {
    pub fn from_pem(pem: &str) -> Result<Self, Error> { … }
    pub fn from_der(der: &[u8]) -> Result<Self, Error> { … }
    pub fn fingerprint(&self) -> Hash { … }
}
```

If parsing genuinely needs its own state (a buffered lexer,
accumulated diagnostics, a configurable mode), then the noun is
`CertParser` *with fields* — see the `QueryParser` example above.
Either the work belongs on the data type, or it belongs on a
stateful parser type. The ZST middle ground is the gap.

### Legitimate ZST uses — narrow, named

ZSTs earn their keep when they carry **type-level information**
rather than pretending to carry runtime state:

- **`PhantomData<T>`** and other generic-parameter trackers.
- **Marker types required by external frameworks** — `ractor`
  actor behaviour markers, sealed-trait gates, an `Iterator` impl
  on a unit struct that genuinely has no carried state. The ZST
  has *only* trait-impl methods that delegate to a data-bearing
  partner type; never inherent methods doing real work.
- **Type-level enum variants** in trait-encoded state machines,
  where the unit struct *is* the state and the type system
  enforces transitions.

The test: does the ZST's job vanish if you erase its name from
the type system? If yes (it was just a namespace), the verbs need
a real noun. If no (the type-system position is what does the work
— phantom parameter, marker, state), the ZST is fine.

---

## Domain values are types, not primitives

If a value has identity beyond its bits, it gets a newtype. A
content hash is not a `String`. A node name is not a `String`. A
file path used as an identifier is not a `Path`.

```rust
// Wrong
pub fn details(&self, md5: &str) -> Result<Item, Error> { … }

// Right
pub struct Md5([u8; 16]);
pub fn details(&self, md5: &Md5) -> Result<Item, Error> { … }
```

**The wrapped field is private.** A `pub` field exposes the
primitive and defeats every reason to wrap it: callers can
construct unchecked values and read the raw bytes back out.

```rust
// Wrong — pub field, the type is just a label
pub struct NodeName(pub String);

// Right — field private; construction and access go through methods
pub struct NodeName(String);

impl NodeName {
    pub fn new(s: impl Into<String>) -> Self { Self(s.into()) }   // or TryFrom if validated
}

impl AsRef<str> for NodeName {
    fn as_ref(&self) -> &str { &self.0 }
}
```

Construction with validation goes through `TryFrom<&str>` (or
`from_str`) returning the crate's `Error`.

---

## One type per concept — no `-Details` / `-Info` companions

If you find yourself defining `Item` *and* `ItemDetails`, stop.
The `-Details` or `-Info` suffix paired with a base type is one
concept fragmented across two types because the base was designed
too thin. Fix the base type. The same applies to `-Extra`,
`-Meta`, `-Full`, `-Extended`, `-Raw`/`-Parsed` pairs, and any
other suffix that means "the real version of the thing next door."

```rust
// Wrong — two types for one concept
struct Item { md5: Md5, name: String }
struct ItemDetails { md5: Md5, name: String, size: u64, mirrors: Vec<Url>, … }

// Right — one Item, complete
struct Item {
    md5: Md5,
    name: String,
    size: u64,
    mirrors: Vec<Url>,
    …
}
```

If different *call sites* genuinely need different *projections*,
model that with a method that returns a smaller view
(`item.summary()`), not with a parallel type.

---

## Don't hide typification in strings

When a value has a typed identity, **the type system carries
the discrimination**. Don't reach for `starts_with(...)`,
`contains(...)`, or `match s.as_str()` to recover information
the type system already encodes.

### Wrong: verifying type by string prefix in tests

```rust
// the field's type is already MessageId — the assertion adds nothing
assert!(messages[0].id.as_str().starts_with("m-"));
assert_eq!(messages[0].id.as_str().len(), 9);
```

If the test wants to check that a particular kind of ID was
returned, the types should already separate them.
`Vec<Message>::id: MessageId` already proves the kind. If the
same field can carry several kinds, that's the missing
sum-type — not a string-prefix discriminator.

### Wrong: dispatching on string prefix at runtime

```rust
fn route(id: &Id) -> Handler {
    if id.as_str().starts_with("m-") { handle_message }
    else if id.as_str().starts_with("d-") { handle_delivery }
    else if id.as_str().starts_with("a-") { handle_authorization }
    else { panic!("unknown id kind") }
}
```

That's a closed enum with extra steps. Use one:

```rust
pub enum Id {
    Message(MessageId),
    Delivery(DeliveryId),
    Authorization(AuthorizationId),
}

fn route(id: &Id) -> Handler {
    match id {
        Id::Message(_)       => handle_message,
        Id::Delivery(_)      => handle_delivery,
        Id::Authorization(_) => handle_authorization,
    }
}
```

### Prefixes for human readability are fine

A prefix like `m-2026-05-07-001` is fine **on the wire** —
humans reading the log see the kind. The rule is against
*recovering* the kind from the prefix in code. Wire form:
prefix is a hint; in-memory: types carry the truth.

If the workspace uses prefix conventions, the convention
lives in the type's constructor (`MessageId::mint()` produces
a string starting with `m-`); no other code knows about the
prefix.

### Companion to "Domain values are types"

The newtype rule says a domain value gets its own type. This
rule extends the principle: once you have the typed identity,
**use it**. Don't drop back to string operations to recover
what the type already proved.

---

## One object in, one object out

Method signatures take at most one explicit object argument and
return exactly one object. When inputs or outputs need more,
define a struct.

**Anonymous tuples are not used at type boundaries** — not as
return types, not as parameter types, not as struct fields, not in
type aliases. The exception is **tuple newtypes**: `struct
Md5([u8; 16])`, `struct NodeName(String)`. They use tuple syntax
to wrap a single thing, but the wrapper itself is a named type.
Local destructuring like `let (a, b) = pair;` against a
tuple-newtype's inner is fine; the rule is about type-level
appearances of unnamed tuples.

The verb is the method name; the noun is the type. Don't smuggle
the verb into the type name (`DownloadRequest` + `download_url(req)`)
— make it a method on the input (`Request::download`).

```rust
// Wrong — multi-primitive args at the boundary
fn download_url(&self, md5: &str, path_index: Option<u32>,
                domain_index: Option<u32>) -> Result<Download, Error> { … }

// Wrong — free function with tuple return
fn parse_results(html: &str) -> Result<(Vec<SearchResult>, bool), Error> { … }

// Right — input is a Request; the verb is a method on it
struct Request { md5: Md5, path_index: Option<u32>, domain_index: Option<u32> }

impl Request {
    pub fn download(&self) -> Result<Download, Error> { … }
}

// Right — input is a SearchPage; parse is a method on it
struct SearchPage { html: String, page: u32 }

impl SearchPage {
    pub fn parse(&self) -> Result<SearchResponse, Error> { … }
}

// Right — one explicit object alongside self (relational operation)
impl Tree {
    pub fn merge(&self, other: Tree) -> Result<Tree, Error> { … }
}
```

`self` is implicit; the rule counts explicit arguments only. A
method takes zero or one typed object alongside `self`.

---

## Constructors are associated functions

`new`, `with_*`, `from_*`, `build` — never module-level free
functions.

| Name           | Use when                                                       |
|----------------|----------------------------------------------------------------|
| `new`          | default / minimal construction.                                |
| `with_<thing>` | ergonomic alt with one extra knob (`Tree::with_bits`).         |
| `from_<src>`   | conversion from a specific source type or representation.      |
| `from_input`   | conversion from a typed input struct (single-object-in style). |
| `build`        | multi-step construction with clearly-named primitive args.     |
| `Default`      | when "empty / zero" is meaningful for the type.                |
| `From<T>`      | infallible conversion from another type.                       |
| `TryFrom<T>`   | fallible conversion. Pair with `Error` enum.                   |

Prefer `TryFrom` when the conversion has one canonical source
type; prefer `from_<src>(…) -> Result<Self, Error>` when there are
several plausible sources or extra args.

---

## Use existing trait domains

If `core::str::FromStr` already names what you do, implement
`FromStr`, not an inherent `parse` method. Same for `Display`,
`From`, `TryFrom`, `AsRef`, `Default`, `Iterator`. Don't reach for
an inherent method just because it's quicker.

```rust
use core::str::FromStr;

impl FromStr for Message {
    type Err = MessageParseError;
    fn from_str(input: &str) -> Result<Self, Self::Err> { … }
}
```

Inherent methods that bypass an obvious trait domain are a smell.

---

## Direction-encoded names

Prefer `from_*`, `to_*`, `into_*`, `as_*`. Avoid `read`, `write`,
`load`, `save` when a direction word already conveys the meaning.
`as_str` over `get_string`. `to_hex` over `format_hex`.
`from_bytes` over `parse_bytes`.

`get` / `put` are fine for storage interfaces (`ChunkStore::get`);
they name the storage operation, not a conversion.

---

## Naming — full English words

Spell every identifier as full English words; the cryptic
in-group dialect is fossil from 6-char FORTRAN, 80-column cards,
and 10-cps teletypes. Cross-language version with the offender
table and the six permitted exception classes lives in this
workspace's `skills/naming.md`.

```rust
// Wrong — cryptic in-group dialect
fn parse(input: &str) -> Result<Token, Error> {
    let mut lex = Lexer::new(input);
    let tok = lex.next_tok()?;
    let kd = tok.kind();
    let ctx = ParseCtx::new(&kd);
    let de = Deser::with_ctx(ctx);
    de.deser_op(&tok)
}

// Right — every name reads as English
fn parse(input: &str) -> Result<Token, Error> {
    let mut lexer = Lexer::new(input);
    let token = lexer.next_token()?;
    let kind = token.kind();
    let context = ParseContext::new(&kind);
    let deserializer = Deserializer::with_context(context);
    deserializer.deserialize_operation(&token)
}
```

`self` is the implicit receiver and is universal across Rust —
leave it. This rule is about *naming the things you create*, not
renaming the language's primitives.

---

## Errors: typed enum per crate via thiserror

Each crate defines its own `Error` enum in `src/error.rs`,
derived with `thiserror`. Variants are structured — carry the data
needed to render a useful message. Foreign error types convert
via `#[from]`.

```rust
use thiserror::Error;

#[derive(Debug, Clone, Error)]
pub enum Error {
    #[error("chunk not found: {0}")]
    ChunkNotFound(Hash),

    #[error("deserialization failed: {0}")]
    DeserializationFailed(String),

    #[error("invalid node: {0}")]
    InvalidNode(String),

    #[error("merge conflict on key ({} bytes)", key.len())]
    MergeConflict { key: Vec<u8> },

    #[error("network: {0}")]
    Network(#[from] reqwest::Error),
}
```

Public APIs return `Result<T, Error>` with the crate's own enum.
**Never** `anyhow::Result`, `eyre::Result`, or `Result<T, Box<dyn
Error>>` — they erase the error type at the boundary, which loses
the typed-failure discipline the rest of the rules build up.
Callers can no longer pattern-match on what went wrong.

---

## Actors: logical units with ractor

When the daemon grows enough concurrent state to need an actor
framework, the reason is **logical cohesion, coherence, and
consistency** — not performance. An actor is the unit you reach
for when you want to model a coherent component: it owns its
state, exposes a typed message protocol, and has a defined
lifecycle. The framework is `ractor`.

- **Messages are typed.** Each actor's message type is its own
  enum, one variant per request kind. No untyped channels.
- **State is owned, not shared.** The actor's state lives inside
  the actor and is mutated only by its message handlers.
  `Arc<Mutex<T>>` shared between actors is a smell — send a
  message to whoever owns the state.
- **Supervision is recursive.** An actor that spawns sub-actors
  supervises them. Failures escalate; the parent decides restart
  vs shutdown. No detached tasks.
- **Use actors for components, not for chores.** A function that
  awaits an HTTP call is a method, not an actor. An actor exists
  because the *concept* it models warrants its own state and
  protocol.

**Ractor is the default** for any component with state and a
message protocol. The per-actor overhead is negligible on modern
hardware, and the discipline (typed messages, owned state,
supervision trees) pays back immediately — you never end up
retrofitting concurrency later. Ractor pulls tokio in; that's
acceptable everywhere — for daemons and structured services,
tokio via ractor is just the runtime.

**Every actor pairs with a `*Handle`.** The four-piece-per-file
shape (`Actor` ZST, `State`, `Arguments`, `Message`) is the
actor's *internal* surface; the `*Handle` struct
(`EngineHandle`, `SupervisorHandle`, `ReaderHandle`) is its
*consumer* surface. The Handle owns the spawn result
(`ActorRef + JoinHandle`) and exposes `start(Arguments)`.
Consumers reach for `*Handle::start`, never bare
`Actor::spawn`. The root daemon's `*Handle::start` is the only
place bare `Actor::spawn` is called; every other spawn happens
inside a parent's `pre_start` via `Actor::spawn_linked`.

For the *how* — the per-file four-piece template,
perfect-specificity messages, the `*Handle` consumer surface,
supervision, self-cast loops, pool initialization, and the
sync-façade pattern — see lore's `rust/ractor.md`. For testing
patterns (sync façade on State, two-process integration via
`CARGO_BIN_EXE_*`), see lore's `rust/testing.md`.

Plain sync code is fine for one-shot CLIs, build tools, and
library crates with no concurrent state.

---

## redb + rkyv — durable state and binary wire

**redb** (embedded key-value store) holds component state
that must survive a restart. **rkyv** (zero-copy archive
format) is the binary contract between Rust components —
both for the durable values inside redb and for the wire
bytes that travel over IPC, sockets, and pipes between
processes.

This section is the *living* discipline for these two
tools. It accumulates patterns and anti-patterns over
time. When a new way of misusing redb or rkyv comes up,
name it here so it stops reappearing. When a clean
pattern gets validated, add it. The aim is correct code
*by default*, with the surface area of bad patterns
shrinking as the document grows.

### What goes where

The first decision when designing a boundary is: **what
crosses it, and to whom does the other side answer?**

| Boundary | Format | Why |
|---|---|---|
| In-process: actor ↔ actor, method ↔ method | typed Rust values | The type system is the schema. No serialization until something leaves the process. |
| Process ↔ process: daemon ↔ harness, IPC, sockets, pipes between Rust components | **rkyv** archives | Zero-copy reads, content-addressable canonical bytes, bytecheck validation. The binary contract is the wire. |
| Component ↔ disk: queues, transition logs, harness bindings, transcripts, snapshots | **redb** tables of rkyv values | Single embedded store, crash-consistent, snapshot reads, no separate server. |
| Component ↔ human: CLI invocations, lock-file projections, debug prints, audit dumps | NOTA text projection | Human-readable + git-trackable; projected from the typed record, never the source of truth. |
| Component ↔ legacy external system | the format the legacy demands | Adapters live at the edge. Internally, the component works in typed Rust; external bytes round-trip through one explicit codec at the boundary. |

The rule: **rkyv is the binary contract for everything
between Rust components.** NOTA is the projection format
when the other side is a human. JSON / serde appears only
at external boundaries that demand it (legacy APIs).

### redb — the durable store

Persistent component state lives in redb: router queues,
harness bindings, transition logs, lock state in-process,
anything the running component mutates and re-reads.

- **Persistent state lives in redb.** Not flat files,
  not JSON files, not bare blobs.
- **Values are rkyv-archived bytes.** Not serde-JSON,
  not hand-rolled binary, not text.
- **One redb file per component.** Each component owns
  its own database. No shared cross-component database.

```rust
// Wrong — flat-file log as the durable store
fn append_lock(path: &Path, lock: &Lock) -> Result<()> {
    let line = lock.to_text()?;
    OpenOptions::new().append(true).open(path)?.write_all(line.as_bytes())?;
    Ok(())
}

// Right — typed record archived with rkyv, stored in redb
const LOCKS: TableDefinition<&str, &[u8]> = TableDefinition::new("locks");

let txn = self.db.begin_write()?;
{
    let mut table = txn.open_table(LOCKS)?;
    let bytes = rkyv::to_bytes::<rancor::Error>(lock)?;
    table.insert(role.as_str(), &bytes[..])?;
}
txn.commit()?;
```

### rkyv — the binary contract on the wire (signaling)

The workspace term for the rkyv-archive-on-the-wire pattern
is **signal**, taken from the canonical reference
`~/primary/repos/signal`. The verb is **to signal** — a
component signals another by sending a length-prefixed rkyv
archive on the wire. "Signaling" describes process-to-process
communication in this workspace; "the signal pattern" describes
the discipline this section defines. Cross-machine signaling
(future networked transport) is a deferred extension; today,
signaling is local IPC over Unix sockets, TCP, pipes, or mmap.

When two Rust components talk across a process boundary
— Unix domain socket, TCP, named pipe, message bus,
mmap region — the bytes on the wire are rkyv archives.
Both ends compile against the *same* rkyv feature set
(see lore's `rust/rkyv.md`); they exchange `Archived<T>`
for some shared frame type `T`; framing is a length
prefix per archive.

```rust
// Wrong — JSON between Rust components
let body = serde_json::to_vec(&request)?;
stream.write_all(&body)?;

// Wrong — ad-hoc binary
stream.write_all(&request.id.to_le_bytes())?;
stream.write_all(request.payload.as_bytes())?;

// Right — rkyv frame, length-prefixed
let archived = rkyv::to_bytes::<rancor::Error>(&request)?;
stream.write_all(&(archived.len() as u32).to_be_bytes())?;
stream.write_all(&archived)?;

// Reader (zero-copy validate-on-receive)
let archived = rkyv::access::<ArchivedRequest, rancor::Error>(&buf)?;
let id = archived.id;        // direct read, no allocation
```

The wire schema *is* the framing. Both parties know the
same `Frame` type; the bytes are `Archived<Frame>`. The
discipline:

- **The shared `Frame` type lives in a contract repo.**
  When two or more components speak the same wire, the
  record types are not re-defined per consumer. They live
  in a dedicated crate that every consumer pulls as a
  dependency. See `~/primary/skills/contract-repo.md` for
  the pattern (what belongs in a contract crate, the
  layered-effect-crate shape, when to introduce one).
  `signal` (`~/primary/repos/signal`) is the canonical
  worked example.
- **One frame type per channel.** A socket between two
  components carries one shared `Frame` enum; new
  request kinds are new variants, not new channels.
- **Same feature set both ends.** A crate that adds or
  drops an rkyv feature (`little_endian`,
  `pointer_width_32`, `unaligned`, `bytecheck`) breaks
  archive compatibility silently. Pin the feature set
  exactly per lore's `rust/rkyv.md`.
- **Validate on receive.** Use `rkyv::access` (or
  `from_bytes`) which runs bytecheck. Don't read fields
  out of unvalidated buffers.
- **Newtype the wire form.** `WirePath(Vec<u8>)` over
  `PathBuf`; platform-dependent stdlib types don't
  archive deterministically.
- **No `serde_json` between Rust components, ever.**
  JSON erases the schema; it appears only at external
  boundaries that demand it.

The Criome direction makes this concrete: the messaging
substrate that lets Persona and Criome eventually merge
is rkyv on the wire. That convergence works only because
both sides agree on the same archive contract today.

### NOTA — the human-facing projection

NOTA is the project's text format. It is **not the wire
between Rust components.** It is what a typed record
*projects to* when a human, a CLI, or a git diff is on
the other side.

- A `Lock` record exists as a typed Rust value. It
  archives to rkyv inside redb. It projects to NOTA
  when written to a `<role>.lock` file. The text
  projection is regenerated from the record; the record
  is never reconstructed *from* the text by parsing
  inside the daemon.
- The CLI form `orchestrate '(ClaimScope ...)'` takes
  one NOTA record on argv (so a human can type it) and
  prints one NOTA record on stdout (so a human can read
  it). Inside the binary, the value travels as typed
  Rust.
- Debug dumps, audit logs, error renderings — all NOTA
  projections of typed records.

The asymmetry: humans use NOTA, machines use rkyv. The
codec at the boundary is `nota-codec`; it is the *only*
text codec each crate ships. No second project-wide
text format.

### Patterns and anti-patterns

This table is the accumulation surface — when a new
shape comes up in review, add the row.

#### Anti-patterns

| Anti-pattern | What it looks like | Why it's wrong | Replace with |
|---|---|---|---|
| Flat-file log as durable state | Append-only `state.log` re-read on startup | No transactions, no atomic updates, parser races writer | redb table with rkyv values |
| JSON between Rust components | `serde_json::to_vec` → socket | Schema erased; can't pattern-match on archive bytes; bytecheck unavailable | rkyv frame + length prefix |
| Ad-hoc binary serialization | Hand-written `to_le_bytes` chains | No schema validation; subtle byte-order bugs; rewriting rkyv badly | rkyv archive |
| NOTA text on the inter-component wire | Daemon ↔ daemon over UDS using NOTA records | NOTA is for human/CLI projection; using it inter-process means re-parsing canonical text in the hot path | rkyv frames; NOTA stays the CLI/lock-file form |
| Storage actor as namespace | `StorageActor` that owns the redb handle and answers "store this" / "fetch that" for everyone | Verb-shaped; the actor owns *storing*, not domain data; each domain actor should own its tables | Each domain actor opens its own tables on the shared `Database` |
| `Arc<Mutex<Database>>` shared across actors | Coarse lock around the whole DB | Defeats redb's transaction model; serializes all writers | One actor per logical data domain; pass values, not handles |
| Reading a record from text in the daemon | `Lock::from_nota(disk_text)?` inside the running component | The text is a projection, not the source. Drift between in-memory and disk silently | Daemon owns the typed record; lock file is rewritten from the record |
| Mixed feature set across crates | One crate has `unaligned`, another doesn't | Archives produced by one don't validate in the other; failure is silent (wrong values, not parse error) | Pin the exact rkyv feature string per lore |
| Reordering struct fields casually | Renaming + reordering in one PR | rkyv archives change layout on field reorder within 0.8 — old data unreadable | Append-only fields; treat any layout change as a coordinated upgrade |
| `anyhow` / `eyre` at component boundaries | `Result<T, anyhow::Error>` on a `pub fn` | Erases the typed-failure discipline; callers can't pattern-match | crate's own `Error` enum via thiserror |

#### Validated patterns

| Pattern | When to use | Notes |
|---|---|---|
| `TableDefinition<&str, &[u8]>` with rkyv-encoded value | Most component tables | Key shape is domain-typed (e.g. `RoleName`, `MessageId.as_str()`); value is rkyv bytes |
| Single `Frame` enum per channel | Inter-component sockets | New variants for new requests; never a second channel for "the new thing" |
| Length-prefixed framing | TCP / UDS streams | 4-byte big-endian length, then the archive |
| `rkyv::access` on the read path | Hot-path reads where ownership isn't needed | Returns `&Archived<T>`; zero allocation |
| Version-skew guard at boot | Any persisted store or long-lived socket | Known-slot record `(schema_version, wire_version)`; hard-fail on mismatch |
| Sync façade on actor `State` | Tests for components that own redb + rkyv | Per lore's `rust/testing.md` |
| Newtype around platform-fragile stdlib types | `PathBuf`, `OsString`, `SocketAddr` on the wire | `WirePath(Vec<u8>)` shape; deterministic across platforms |

### Named exceptions — text-on-disk that stays text

The rule is about *state the component mutates and
re-reads* and *bytes between Rust components*. Some
text-on-disk forms stay text by design and are not state
in the redb sense:

- **Lock-file projections** (per
  `~/primary/protocols/orchestration.md`).
  `<role>.lock` files are human-readable runtime
  coordination state, gitignored — they exist on disk for
  agents to read with `cat` or `tools/orchestrate status`,
  not in version control. The redb store is the in-process
  truth; the lock file is the outward projection
  regenerated from the record.
- **Configuration files.** `Cargo.toml`, `flake.nix`,
  per-repo configs. Inputs, not state.
- **Reports and prose docs.** Markdown is markdown.
- **Interchange artifacts.** A NOTA-line file shared
  across components for one-shot ingestion is
  interchange, not the running component's state.
- **Logs for human eyes.** A line-oriented audit log
  intended for a human reading `tail -f` is a
  projection. The structured log a component re-reads
  on restart is not — that lives in redb.

If a component owns the data and mutates it during
operation, it lives in redb + rkyv. If a component
sends bytes to another Rust component, those bytes are
rkyv archives. The named exceptions above don't satisfy
either condition.

### Schema discipline

rkyv archives are schema-fragile. Adding, removing, or
reordering fields changes the archive layout. The
disciplined consequences:

- **No silent backward compatibility.** Old archives
  don't read into new types and vice versa.
- **Version-skew guard.** A known-slot record carrying
  `(schema_version, wire_version)`, checked at boot.
  Hard-fail on mismatch. rkyv's own version handling is
  not enough.
- **Treat schema changes as coordinated upgrades.** A
  field reorder is a breaking change; a field addition
  is too, in 0.8. Plan rollout across every consumer.

For the tool-level details (the canonical feature set
character-for-character, derive-alias pattern,
encode/decode API, `bytecheck` semantics), see lore's
`rust/rkyv.md`. This skill is *what discipline to apply*;
lore is *how the tool works*.

### When to lift to a shared crate

Multiple components using the same redb + rkyv patterns —
typed `Table<K, V>` wrapper, common error variants,
transaction helpers, migration utilities — eventually
warrant a shared helper crate.

**Don't pre-abstract.** Each component uses redb + rkyv
inline first; the shared shape becomes obvious after
2–3 components have crystallized their patterns. The
sema → criome path followed exactly this growth:
shared shape became visible from real use, then
extracted.

### Why this discipline is strict

The rules above feel laborious before the components are
written. They are not laborious *while* the components
are running: a typed wire makes wrong calls fail at
compile time, a typed store makes wrong reads fail at
boot time, and the projection-from-record discipline
makes the disk and the in-memory truth impossible to
disagree.

Each entry in the anti-pattern table is a class of bug
the workspace has either lived through or watched
nearby. Each entry in the validated-pattern table is a
shape that earned its place by surviving real use. The
table grows; the work gets more correct as it grows.

---

## One Rust crate per repo

Rust crates live in their own dedicated repos and are consumed
via flake inputs. Don't inline a Rust crate inside a non-Rust
repo (e.g. under a NixOS-platform repo's `packages/`). A Rust
crate has its own toolchain pin, its own Cargo lockfile, its own
test surface, its own release cadence, and its own style
obligations. Inlining one inside a heterogeneous repo couples
those concerns to the host repo's churn for no gain. Consume via
flake input instead.

A workspace of related Rust crates (e.g. lib + cli) belongs in
**one** repo together. The split is per *project*, not per crate.

For the toolchain reference (Cargo.toml conventions, cross-crate
dependencies, git-URL deps, pin strategy), see lore's
`rust/style.md`.

---

## Tests live in separate files

Unit tests do **not** go in a `#[cfg(test)] mod tests` block at
the bottom of the source file. They live in a sibling file under
`tests/` at the crate root, named for the module they exercise.

```
src/
├── cert.rs
├── tree.rs
└── error.rs
tests/
├── cert.rs      # integration tests for Cert
└── tree.rs      # integration tests for Tree
```

This keeps the source file focused on behavior, lets the test
file grow without bloating the source file, and forces tests to
exercise the public API (integration tests can't reach private
items — which is the right pressure: if something is hard to test
from outside, the API needs work, not the test). Private-helper
tests are rare and can go in a small `tests_internal` module with
a clear boundary; if you find yourself reaching for many, that's
a signal the helper wants to be its own type with a public
constructor.

One test file per source file. Don't collect tests from multiple
modules into a single `tests/common.rs` unless the shared
fixtures genuinely apply to more than one module.

---

## Module layout

One concern per file. Typical crate:

```
src/
├── lib.rs        # re-exports + crate-level doc (//!)
├── error.rs      # Error enum + impls
├── types.rs      # domain newtypes + small structs
├── <thing>.rs    # one file per major type / subsystem
└── main.rs       # only if the crate is a binary; only free fn lives here
```

Impls live in the same file as the type they're for. Don't split
types and impls across files.

### Split traits into their own files when they accumulate

When a single file grows past ~300 lines because traits have
piled up on a type, split each trait impl into its own file. The
file for a type holds the type definition + its inherent impls;
each separate file holds one trait impl for that type, named for
the trait.

```
src/cert/
├── mod.rs              # type definition + inherent impls (Cert::new, fields)
├── from_str.rs         # impl FromStr for Cert
├── display.rs          # impl Display for Cert
├── try_from_pem.rs     # impl TryFrom<Pem> for Cert
└── serde_impls.rs      # impl Serialize + Deserialize for Cert (paired traits)
```

This is the deliberate trade-off **explicit code is fine; long
files are not**. Splitting trait impls into separate files keeps
any single file readable, makes the type's surface discoverable
from the directory listing, and prevents impl blocks from growing
into a wall of unrelated behavior.

Use this pattern when traits accumulate. Don't pre-split a type
with two trait impls — that's premature ceremony. Split when a
file is becoming hard to navigate.

---

## Documentation

Doc comments are impersonal, timeless, precise. Document the
contract; don't restate the signature.

```rust
impl Cert {
    /// Issue a server certificate against this CA.
    ///
    /// The CA's signing key must be an Ed25519 key resolvable via the
    /// local GPG agent. The server keypair is ECDSA P-256, generated fresh.
    pub fn issue_server(&self, request: ServerCertRequest) -> Result<Self, Error> { … }
}
```

Module-level docs go in `//!` at the top of `lib.rs` or `///` at
the top of a single-purpose module file. Skip docs on obvious
boilerplate: getters, `From` impls, internal helpers.

No examples in doc comments unless the API is non-obvious. No
personal voice. No future tense. Present indicative only.

---

## See also

- this workspace's `skills/abstractions.md` — cross-language
  version of the methods-on-types rule.
- this workspace's `skills/naming.md` — cross-language naming
  rule with the full offender table.
- this workspace's `skills/beauty.md` — beauty as criterion;
  the rules above are how Rust code gets there.
- this workspace's `skills/micro-components.md` — one capability
  per crate per repo.
- lore's `rust/style.md` — toolchain reference (Cargo.toml,
  cross-crate deps, pin strategy, Nix-based tests).
- lore's `rust/nix-packaging.md` — canonical crane + fenix flake
  layout.
- lore's `rust/ractor.md` — ractor template, per-verb typed
  messages, supervision patterns.
- lore's `rust/rkyv.md` — rkyv portable feature set, derive-alias
  pattern, schema fragility.
