# Skill — Rust methods and types

*Methods on types, not free functions. Domain values are typed.
Boundaries take and return one object. Don't hide typification
in strings.*

---

## What this skill is for

When writing Rust types and methods in this workspace, this skill
is the discipline. It is the Rust-specific enforcement of the
cross-language rules in `skills/abstractions.md`, `skills/naming.md`,
and `skills/beauty.md`.

For the index pointing at the wider Rust discipline (errors,
storage and wire, parsers, crate layout), see
`skills/rust-discipline.md`.

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

For the cross-language rule — the forcing-function reasoning,
the Karlton bridge, the wrong-noun trap, and the principled
exceptions (local helper, relational operation, standard-library
convention) — see `skills/abstractions.md`. This section is the
Rust enforcement.

---

## No ZST method holders

A `pub struct Foo;` whose `impl Foo` is just a parking lot for
functions that do real work on data they don't carry is a free
function in namespace clothing — the methods-on-types rule evaded
one level deeper. Per `skills/abstractions.md` §"The wrong-noun
trap" and §"The forcing function": find the noun whose data the
verb reads or writes; invent it if it doesn't exist yet.

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
accumulated diagnostics, a configurable mode), the noun is
`CertParser` *with fields*. Either the work belongs on the data
type, or it belongs on a stateful parser type. The ZST middle
ground is the gap.

### Legitimate ZST uses — narrow, named

ZSTs earn their keep when they carry **type-level information**
rather than pretending to carry runtime state:

- **`PhantomData<T>`** and other generic-parameter trackers.
- **Marker types required by external frameworks** — sealed-trait
  gates or an `Iterator` impl on a unit struct that genuinely has no
  carried state. The ZST has *only* trait-impl methods that delegate
  to a data-bearing partner type; never inherent methods doing real
  work. For actors, the workspace runtime is Kameo, whose `Self IS
  the actor` shape removes the need for framework marker types
  entirely — the actor type carries data fields and is the noun.
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

### The system mints identity, not the agent

Even when a string ID's discriminator is type-correct in
code, an agent-minted prefix-encoded ID is the wrong shape
because the agent shouldn't be minting identity at all.

```rust
// Wrong — agent invents an ID
let id = format!("m-{}-{:03}", today_iso8601(), counter.next());
store.send(Message { id, sender, recipient, body }).await?;
```

The agent does clock work, maintains counter state, packs
typed values into stringly-typed form, and produces an
opaque key parallel to the slot the store assigns anyway.

```rust
// Right — the store assigns Slot<T>
let slot = store.assert(Message { recipient, body }).await?;   // returns Slot<Message>
```

The wire form on the read path shows the surrounding record
kind at the head ident (`(Message ...)`) and the slot as a
bare integer; humans see *what kind of thing* and *which one*
without any agent-minted prefix.

The same shape applies when the agent supplies its own
sender or its own timestamps:

```rust
// Wrong — sender on the record body (already on the auth proof)
store.assert(Message { sender: my_principal, recipient, body }).await?;

// Wrong — commit time as a record field (transition log already stamps it)
store.assert(HarnessObservation {
    subject,
    state,
    observed_at: Utc::now().to_rfc3339(),    // string, agent-minted
}).await?;

// Right — agent supplies only content; infrastructure stamps the rest
store.assert(Message { recipient, body }).await?;
store.assert(HarnessObservation { subject, state }).await?;
```

The unifying test: ***could the system supply this value
without asking the agent?*** If yes, the agent must not
supply it. Identity, commit time, sender principal — all
infrastructure context. The wire carries only what only
the sender knows.

*Content* timestamps (a `Deadline`'s expiration, a
scheduled message's send-at) are different — those are
values the agent genuinely supplies, and they appear as a
typed `Timestamp` (a bare integer in NotaTransparent shape
— nanos since epoch — not a string).

For the apex statement of this rule, see ESSENCE
§"Infrastructure mints identity, time, and sender."

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

## See also

- `skills/rust-discipline.md` — Rust discipline index.
- `skills/abstractions.md` — cross-language methods-on-types rule.
- `skills/naming.md` — cross-language naming, full English words,
  framework-category-suffix anti-pattern.
- `skills/rust/errors.md` — typed Error enum per crate.
- `skills/rust/storage-and-wire.md` — redb + rkyv discipline.
- `skills/beauty.md` — beauty as criterion.
