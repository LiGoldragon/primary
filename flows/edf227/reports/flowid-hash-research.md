# FlowId as a hash: how it works today, how it could work

Marks: **[W]** witnessed (read in code at the named revision, or run);
**[I]** inferred (follows from what was read, not run or observed).

The living's words this answers are in `flows/edf227/vision/identifiers.md`:
the flow id is a hash; the Nexus thinks of it as a hash, "maybe an integer with
certain kinds of traits"; the text forms are serialization outside the Nexus;
"in the deserialization, we can have special implementations". The earlier
settled word form is 33 bits as three BIP-39 words
(`flows/5578cc/books/flow-ids-in-words-settled.md`).

Revisions read (repository root `/git`, from `SKILL_VARIABLES.md`) [W]:

| repo | local checkout (detached) | origin/main |
|---|---|---|
| flow | 83df560 | 5e0b1bf (pins signal-flow f95034d, meta-signal-flow 54eb561) |
| signal-flow | 5860383 (7.1.0) | e79fbc9 (10.0.0 line) |
| meta-signal-flow | 2ac045c (11.0.0) | 5d17742 (14.0.0 line) |
| harness | 75ff8a2 | 8604a07 (0.4.0); `src/flow_id.rs` identical |
| datom-codec | 4dff16b (0.32.2) | same |
| protos | 15b41da (0.32.2) | same |
| ethos-zero | c2653dd (16.0.0) | same |

Every local checkout of the flow family is behind origin/main; the facts below
hold at both unless a line says otherwise [W]. The installed `flow-id` is
`/nix/store/b4wz…-harness-0.3.4/bin/flow-id` [W]; that its source matches
`flow_id.rs` at 75ff8a2 is [I] (diff of that file to origin/main is empty).

## 1. Today

### Ethos and generated Rust

- signal-flow `ethos/signal.ethos` declares `FlowId.String` among its types,
  at 5860383 and at origin/main [W].
- Generated `src/generated/signal.rs` line 3: `pub type FlowId = String;` [W].
  An alias carries no derive, so FlowId has no type of its own: it is
  `String` everywhere, indistinguishable from `SessionId`, `TurnId`,
  `HerdrPaneId` and the other twenty-odd `.String` aliases [W].
- meta-signal-flow imports it, `signal_flow:[ FlowNode FlowId … ]`, and
  aliases `MetaFlowOwnerId.FlowId` [W].
- The flow repo has no ethos of its own; `crates/signal-flow/` and
  `crates/meta-signal-flow/` are empty directory stubs [W].

### CLI: text to FlowId

- `flow` (crates/flow/src/main.rs) takes one argument and runs
  `Potential::<Query>::from(value).actualize(&mut budget)` [W].
- A FlowId position therefore composes through datom-codec's
  `impl Composing for String`, which reads a `Form::Bare` or `Form::String`
  (and rejoins a dotted head chain into one bare string) [W,
  `src/composition.rs` 190–262]. `6329f1` is a bare string; nothing checks it
  is hex, six characters, or lowercase [W].
- No hand-written FlowId impl exists anywhere in flow, signal-flow or
  meta-signal-flow [W, grep].
- Datomizing writes it back as `Form::Bare` unless it contains whitespace or a
  delimiter glyph [W, composition.rs 165–188].

### Wire

- Every generated struct and enum derives `rkyv::Archive/Serialize/
  Deserialize` [W]; the flow CLI writes `rkyv::to_bytes(query)` with a 4-byte
  big-endian length [W, flow/src/main.rs].
- FlowId rides as rkyv 0.8.18's `ArchivedString` [W: Cargo.lock 0.8.18;
  alias = String]. Under `pointer_width_32`, `INLINE_CAPACITY` is the size of
  the out-of-line repr (u32 length + i32 offset), 8 bytes, so a six-character
  id is stored inline [I, from `rkyv/src/string/repr.rs:29`].
- The Nexus's own store keys flow records by that text:
  `RecordKey::new(self.flow_id.clone())` for `FlowRecord`, `StoredRole`,
  `FlowHerdrRouteRecord` [W, flow-nexus/src/store.rs 160–236].

### Harness: UUID to alias (`harness/src/flow_id.rs`) [W]

- `flow-id codex --flows-root DIR` reads `CODEX_SESSION_ID`;
  `flow-id claude --flows-root DIR --parent-session UUID` takes the Claude
  parent session.
- `normalize_uuid` requires the 36-char hyphenated form, strips hyphens,
  lowercases: 32 hex. Claude's path additionally requires lowercase input,
  version nibble 4 or 5 and RFC 4122 variant.
- Candidate alias = `identity[start .. start+6]`, extended one hex digit at a
  time on collision up to the end: `FIRST_CANDIDATE_LENGTH = 6`,
  `CODEX_CANDIDATE_START = 23` for Codex, 0 for Claude.
- Each candidate is claimed under a lock file `.<alias>.flow-id.lock` and
  written as marker `.<alias>.flow-id`:
  `version=1 / harness= / identity=<32 hex> / alias= / [uuid-version=]`.
  A lane directory without a marker is "Legacy" and skipped.
- The alias is printed on stdout; it is the FlowId.
- [I] Codex thread ids are UUIDv7: 32-hex index 23 lies inside `rand_b`, so a
  Codex alias is random bits, not the timestamp. A Claude v4 alias's first six
  hex are 24 random bits. The alias is variable-length text: its width is
  decided by what collides on disk, not by a type.

### Hex text inside the Nexus today [W, flow origin/main]

The Nexus does know text, in five places:

1. `herdr/launch.rs` (~372): runs the `flow-id` executable, reads its stdout,
   refuses unless non-empty lowercase hex.
2. `herdr.rs` `VerifiesFlowClaim::identity_is_claimed` (~570) and
   `FlowClaim::decode` (~626–630): re-checks lowercase hex on the FlowId and
   on the marker's 32-hex identity, opens `.<flow_id>.flow-id`.
3. `herdr/reservation.rs` (~90): `release_flow_identity` refuses a non-hex id
   and opens `.<flow_id>.flow-id.lock`.
4. `title.rs` (~67): `native_title` requires exactly six chars of `[0-9a-f]`;
   a seven-digit alias (a collision extension) cannot be titled.
5. Store keys are the text (above); the id also enters the composed prompt.

Also [W]: flow-nexus enables `meta-signal-flow/datom` and depends on
datom-codec and protos directly (Cargo.toml comment: "The Nexus renders one
typed value as text, the Message it types into a pane"). So datom is not
compiled out of this Nexus today, contrary to vision-nexus.

## 2. The mechanism

### Intrinsics and derived types [W]

- Intrinsic impls live in datom-codec: `String`, `i64`, `bool`, `Decimal`,
  `Meaning`, `Vec<T>`, `Option<T>`, `Result<T,E>`, `Box<T>`, tuples, and the
  protos error types (composition.rs 165–680, decimal.rs 135–150). Scalars go
  through `trait Scalar`. `i64` parses ASCII decimal only, refusing `+`, `-0`
  and leading zeros; there is no u64, u128, byte array or hash intrinsic.
- ethos-zero maps intrinsics in `generation.rs` ~60: `Integer → i64`,
  `Decimal → datom_codec::Decimal`, `Meaning → datom_codec::Meaning`, etc.
- The derive (`crates/datom-codec-derive`) is `#[proc_macro_derive(Composing)]`
  and `#[proc_macro_derive(Datomizable)]` with no `attributes(...)`: no
  `with`, no `serialize_with`, no per-field override exists. A struct
  composes positionally (`Compositional::ARITY`, `positions.position()?`); a
  one-field struct is still a struct, `{ 42 }`; an enum reads a bare head or
  `Head.body`.

### The rule on hand-written impls

Quoted, datom-codec `README.md` 37–43 [W]:

> Both are derived, with no attributes, for any Rust struct or enum […]
> Hand-written impls are reserved to the intrinsics: `String`, `i64`,
> `Decimal`, `bool`, `Meaning`, `Vec`, `Option`, `Result`, `Box`, the tuples,
> and the protos types the errors carry.

The same sentence is in Curriculum `skills/datom.md:53` [W].

Enforcement: none in code [W]. `Composing` and `Datomizable` are public,
unsealed traits (no `Sealed` anywhere in datom-codec); the Nix check
`checked-anatomy.sh` only runs `ethos-zero Check` on the anatomy file; and
`tests/core.rs:810` itself hand-writes `impl Composing for Recursive`. The rule
is convention.

What does constrain it is Rust [I, orphan rule quoted in Sources]:
- A CLI crate cannot write `impl datom_codec::Composing for signal_flow::FlowId`:
  foreign trait, foreign type.
- Inside signal-flow, a hand impl collides with the generated
  `#[cfg_attr(feature = "datom", derive(Datomizable, Composing))]` whenever the
  type is a struct or enum. While FlowId is an alias of `String`/`i64`, no
  impl can target it at all without targeting every `String`/`i64`.

### protos Textualizable and rkyv Archive [W]

- protos `Textualizable::textualize(&self) -> String` and `Compactable` are
  implemented only for the `Protos` tree (rendering.rs 312, 321). A value
  reaches text by `value.datomize(Path::new()).protosize().textualize()`.
- rkyv `Archive` is independent: derived on every generated type, used for
  wire and store. The two meet only in the CLI, where datom is the bridge
  between text and the Rust value that rkyv then archives. protos's and
  datom-codec's own `rkyv` features exist only so error/extent/decimal types
  can sit in archived positions.

### Can an ethos kind declare "textualizes as"? (ethos-zero 16.0.0, run) [W]

Built `ethos-zero` 16.0.0 at c2653dd into the scratchpad and ran it:

- `FlowId.Integer` with kind `Wordable.[ as_words.[ String ] as_hex.[ String ] ]`
  and association `[ FlowId.[ Wordable ] ]` → `pub type FlowId = i64;`,
  `pub trait Wordable { fn as_words(&self) -> String; fn as_hex(&self) -> String; }`,
  and a const assertion that `FlowId` (i.e. `i64`) is `Wordable`.
- A capability input of `String` is refused:
  `Conceptual.{ [ 1 2 0 1 1 1 0 0 ] KindWanted.String }`.
- `FlowId.{ Integer }` with `Hashable.{ [] [] [ WIDTH.Integer ] [ width.[ Integer ] ] }`
  and `Wordable.{ [ Hashable ] [] [] [ as_words.[ String ]
  parse_words:{ [ Textualizable ] [ Option<Self> ] } ] }` →
  `pub struct FlowId { pub integer: i64 }` with rkyv derives and the
  `cfg_attr(feature = "datom", …)` derives; `pub trait Hashable { const WIDTH: i64; fn width(&self) -> i64; }`;
  `pub trait Wordable: Hashable { fn as_words(&self) -> String;
  fn parse_words<N: protos::Textualizable>(input: N) -> Option<Self> where Self: Sized; }`;
  assertions for both.
- A bare `[ WIDTH ]` constant is refused (`Expected.Constant`); it needs a type.

So a kind can carry text capabilities as an ordinary trait, but nothing links
that trait to datom: the derived `Composing` still reads `{ 42 }`. There is no
"this kind's text replaces the structural form" in ethos-zero today.

## 3. Prior art (fetched)

1. **Newtype + Display/FromStr in the edge crate.** std: FromStr is "Parse a
   value from a string"; "the input format of a type's FromStr implementation
   might not necessarily accept the output format of its Display". Here the
   orphan rule decides placement: the trait-owning or type-owning crate
   only, so "in the CLI crate only" needs a CLI-local wrapper type.
2. **serde `serialize_with` / `deserialize_with` / `with`.** "Serialize this
   field using a function that is different from its implementation of
   Serialize"; `with = "module"` pairs both. Per-field, chosen at the
   containing type: exactly the attribute datom's derive refuses to have.
3. **rkyv `with` wrappers.** `ArchiveWith`, `SerializeWith`, `DeserializeWith`
   ("A variant of Archive that works with wrappers") via `#[rkyv(with = …)]`
   on a field, e.g. `Inline`, `AsBox`, `Skip`. Wire layout chosen per field
   by a zero-sized adapter type; the value's type is unchanged.
4. **uuid.** `Uuid` "is always guaranteed to be have the same ABI as
   `Bytes`" (`[u8; 16]`), with `as_u128`/`from_u128`. Text forms are adapters:
   `as_simple()` (32 hex, today's normalized identity), `as_hyphenated()`,
   `as_urn()`, `as_braced()`; `parse_str` accepts all. One value, many
   formatters, none inside the value.
5. **bip39 + multibase.** bip39 `Mnemonic::from_entropy` needs "a multiple of
   32 bits … 128-256 bits", 12–24 words, last word carries a SHA-256 checksum;
   `to_entropy` inverts. So the crate's Mnemonic cannot carry 33 bits; only
   its 2048-word list fits (as signal-5f4fea-word-identifiers already does:
   `bip39 = "2"` for `Language`, own 11-bit packing, no checksum [W]).
   multibase: `<base-encoding-code-point><base-encoded-data>`, `f` base16,
   `b` base32, `z` base58btc: one byte string, the encoding named by a prefix
   at the text edge.

In-house prior art [W]: `signal-5f4fea-word-identifiers` (d2dfa3b)
`src/identifiers.rs` holds rkyv newtypes `LocalNameReference([u16; 3])` etc.
with inherent `parse` and `Display` (lowerCamelCase BIP-39), outside ethos,
because "Pinned Datom and Protos provide text and integer intrinsics but no
standard hash primitive" (`reports/identifier-poc.md`). It packs words from a
BLAKE3 digest, which the living then corrected to the id's own bits.

## 4. Three designs

### (a) `FlowId.{ Integer }` newtype, a Hashable kind with WIDTH, text in the edge

- Ethos: `FlowId.{ Integer }` in signal-flow, kinds
  `Hashable.{ [] [] [ WIDTH.Integer ] [ … ] }` and a text kind (Hexable/Wordable);
  association `[ FlowId.[ Hashable Wordable ] ]`. Must be a struct, not
  `FlowId.Integer`: an alias gives `i64` the impls.
- Nexus sees `FlowId { integer: i64 }`, archived as 8 bytes; store key the
  integer. 33 bits fits; a full 128-bit UUID does not (no u128 intrinsic).
- CLI sees text `6329f1` or `abandonAbilityAble`, only if `Composing` for
  FlowId is not the derive (which would read `{ 6501873 }`).
- ethos-zero: a way to mark a type whose datom form is hand-supplied, so it
  omits the `cfg_attr` derive for that type. Without it, conflict.
- datom-codec: no change if the hand impl is allowed outside intrinsics;
  the README rule changes to admit "a type bearing a text kind".
- protos: none. Where the impl lives: signal-flow behind `feature = "datom"`
  (orphan rule), which the Nexus does not enable for signal-flow [I].
- Special deserialization = the hand `Composing`/`Datomizable` for FlowId,
  dispatching on the text: 6–8 lowercase hex → hex parse; camelCase → words.

### (b) An opaque `Hash` intrinsic, encoding chosen by a kind

- Ethos: a new intrinsic `Hash` (bytes of fixed width) beside String/Integer;
  `FlowId.Hash` aliases it, or `FlowId.{ Hash }`; encodings as kinds the
  intrinsic accepts, e.g. a position `Hash<Wordable>` — but ethos has no
  generics, so the parameter must be a kind, which ethos-zero has no syntax
  for on an intrinsic today [I].
- Nexus sees e.g. `Hash([u8; N])` archived as N bytes; compares and keys bytes.
- CLI sees a multibase-like bare text: `f6329f1…` hex, a words form, others.
- ethos-zero: new `Intrinsic::Hash` → a Rust path, plus parameter parsing.
- datom-codec: hand `Composing`/`Datomizable` for Hash (admitted: it is an
  intrinsic), reading a prefix or the kind to pick the decoder.
- protos or a new tiny crate owns the `Hash` type and its rkyv; not
  datom-codec, or the Nexus links datom-codec as it does for `Decimal` [I].
- Special deserialization = a registry of encodings inside the intrinsic's
  impl; every Nexus gains a typed hash, not only Flow.

### (c) The id kept as bytes, a Wordable kind over it

- Ethos: `FlowId.{ Vector<Integer> }` today (generated `Vec<i64>` [W]), or
  bytes once ethos has them; Memory keeps the full 16-byte native UUID, the
  short id derived (first 33 bits, or the alias window).
- Nexus sees the full native identity; the flow-id marker file and the
  hex-alias lane become redundant (the Nexus can compute the prefix) [I].
- CLI sees words or hex; resolves a short form to the full bytes by asking
  the Nexus (ambiguity = typed refusal naming the matches, as the living
  asked for collisions) — a lookup, not a pure decode.
- ethos-zero: a bytes intrinsic (`[u8; N]` or `Vec<u8>`) or nothing (Vec<i64>,
  wasteful: 8 bytes per byte); Wordable as a plain kind (works today [W]).
- datom-codec: a short-form `Composing` still needed for the CLI text; or the
  short form is a distinct type (`FlowReference`) that composes from text and
  never enters Memory.
- protos: none.
- Special deserialization = Wordable/Hexable impls on FlowReference, plus a
  Resolve query that the Nexus answers.

## 5. Open questions

1. Which bits are the hash: the alias window of the native UUID (today), the
   first 33 bits of it (5578cc), or a hash of the launch record? Codex
   aliases come from index 23, Claude's from 0 [W].
2. Is the width fixed (33, 64, 128 bits) or kept variable as now, where a
   collision extends the alias and `title.rs` then refuses it [W]?
3. Does the Nexus keep the full native session UUID as the identity, with the
   short id a projection (c), or only the short id (a)?
4. Is the rule "hand-written impls are reserved to the intrinsics" to be
   widened to types bearing a text kind (a), or held by adding an intrinsic
   (b)? It is not enforced in code either way [W].
5. Ethos has no syntax linking a kind to the datom form, nor a kind parameter
   on an intrinsic. Which of the two does ethos grow?
6. Should the Nexus stop linking datom (meta-signal-flow `datom` feature,
   pane-message rendering) before FlowId text leaves it? Today it is in [W].
7. The marker file `.<alias>.flow-id` and lock lanes are text names on disk
   that the Nexus opens [W]; under a typed hash, who renders the file name,
   and does the marker survive?
8. Store migration: Memory keys are the alias text today; changing the key
   type is a Memory upgrade per vision-ethos.
9. Hex-to-words: 33 bits is 8 hex digits and one bit, so words → hex leaves
   the ninth digit's low three bits open; the living accepts this [W, vision].

## Sources

- `/home/li/primary/flows/edf227/vision/identifiers.md`;
  `/home/li/primary/flows/5578cc/books/flow-ids-in-words-settled.md`,
  `answers-flow-ids.md`, `flow-ids-in-words.md`.
- signal-flow `ethos/signal.ethos`, `src/generated/signal.rs` (5860383; origin/main e79fbc9).
- meta-signal-flow `ethos/signal.ethos` (2ac045c).
- flow `Cargo.toml`, `crates/flow/src/main.rs`, `crates/flow-nexus/Cargo.toml`,
  `src/store.rs`, `src/herdr.rs`, `src/herdr/launch.rs`,
  `src/herdr/reservation.rs`, `src/title.rs` (83df560; origin/main 5e0b1bf).
- harness `src/flow_id.rs`, `src/bin/flow_id.rs` (75ff8a2 = origin/main for these files).
- datom-codec `README.md`, `src/composition.rs`, `src/decimal.rs`,
  `crates/datom-codec-derive/src/lib.rs`, `tests/core.rs`, `tests/hygiene.rs`,
  `checks/checked-anatomy.sh` (4dff16b).
- protos `src/core.rs`, `src/rendering.rs`, `protos-kinds.ethos` (15b41da).
- ethos-zero `src/generation.rs`, `src/conception.rs` (c2653dd); run of the
  built 16.0.0 binary on scratch files `a.ethos` … `e.ethos` in the session
  scratchpad (`…/scratchpad/ez/`), outputs quoted above.
- signal-5f4fea-word-identifiers `src/identifiers.rs`, `reports/identifier-poc.md`, `Cargo.toml` (d2dfa3b).
- rkyv 0.8.18 `src/string/repr.rs` (cargo registry).
- Curriculum `skills/datom.md:53`.
- Web: https://doc.rust-lang.org/std/str/trait.FromStr.html ;
  https://serde.rs/field-attrs.html ;
  https://docs.rs/rkyv/latest/rkyv/with/index.html ;
  https://docs.rs/uuid/latest/uuid/struct.Uuid.html ;
  https://docs.rs/uuid/latest/uuid/fmt/index.html ;
  https://docs.rs/bip39/latest/bip39/struct.Mnemonic.html ;
  https://github.com/multiformats/multibase ;
  https://doc.rust-lang.org/reference/items/implementations.html (orphan rule).
