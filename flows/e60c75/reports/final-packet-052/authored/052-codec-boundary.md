# 052 narrow codec boundary — authored proposal

Pins: Protos15b41da8f2579e73ead59bc0c2b97529b8ac32d3 and Datom4dff16b4f7412febc3b71aac8b49680cd20988cb. Preparation/version/consumer closure and independent review remain gates. No bodies.

## Shared lexical machinery, borrowed and nonrecursive

Protos gains a data-bearing cursor with private borrowed text and byte offset. Existing Reader delegates lexical work to the SAME implementation. No copied whitespace/comment/canonical-integer grammar and no public recursive Reader.

```rust
pub struct LexicalCursor<'text> { /* private text: &'text str, offset: usize */ }
pub trait LexicallyReadable {
    fn lexical_cursor(&self) -> LexicalCursor<'_>;
}
pub trait LexicallyTraversable<'text> {
    fn skip_space_and_comments(&mut self);
    fn expect_delimiter(&mut self, expected: char) -> Result<(), protos::Error>;
    fn token(&mut self) -> Result<&'text str, protos::Error>;
    fn offset(&self) -> usize;
}
// LexicallyReadable for str; LexicallyTraversable for LexicalCursor.
```

The cursor handles only the existing lexical operations. token returns a borrowed run and respects the same delimiter/token boundaries as Reader. No tree, mutable Reader, ownership proof or recursive parse is exposed. Errors retain existing Protos extent/problem. Before bodies the lexical helper extraction must have an exhaustive equivalence fixture set covering Unicode whitespace, semicolon comments/newlines, delimiters, UTF-8 positions and bare tokens.

expect_delimiter refuses an expected glyph outside the existing Protos enclosure-delimiter set; it is not an arbitrary-character matcher. This domain check reuses the codec's existing delimiter classification and reports typed lexical failure. No new delimiter set is authored in Flow.

Datom extracts canonical Integer decoding into one capability used by its existing Integer composition and bootstrap decoder:

```rust
pub enum IntegerDecodeError {
    NonCanonical,
    Invalid(std::num::ParseIntError),
}
pub trait CanonicalIntegerReadable {
    fn canonical_integer(&self) -> Result<Integer, IntegerDecodeError>;
}
// Implemented for str. The existing Integer composition maps this result to
// its existing typed Error with the current datom path; no error text copying.
```

This preserves malformed-token/overflow native parse evidence while distinguishing existing canonical-spelling rejection. It is not the reader suggestion's incomplete enum of four cases. Empty/non-numeric/invalid-sign tokens remain errors. No conversion accepts leading plus, negative zero or leading zero contrary to the current codec. Exact existing branch precedence is preserved; no new numeric language is introduced.

## Five supplied limits, preserving existing field meanings

```rust
// Protos: preserve existing remaining field; add supplied depth.
pub struct ReaderBudget {
    pub remaining: usize,
    pub maximum_depth: usize,
}
// Datom: preserve existing counters; add supplied forming depth.
pub struct Budget {
    pub remaining: Integer,
    pub reader: protos::ReaderBudget,
    pub depth: Integer,
    pub maximum_depth: Integer,
    pub forming_maximum_depth: Integer,
}
```

StructuralNodeLimit maps to reader.remaining, StructuralDepthLimit to reader.maximum_depth, DatomFormDepthLimit to forming_maximum_depth, CompositionStepLimit to remaining, and CompositionDepthLimit to maximum_depth. depth starts at0 because it counts active composition entries, not because0 is a policy fallback. All configured limits are positive, representable and checked before converting Integer to usize. No saturating/as casts. Existing hidden256 and4096 are replaced at their actual checks; there is no convenience default constructor.

Potential::actualize remains the one whole-pipeline owner. It passes supplied forming depth to Former through the actual forming capability; all direct forming call sites must also receive an explicit limit. This is a signature change with an all-consumer ledger, not a hidden alternate path. Reader's node/depth checks use its supplied ReaderBudget. Typed composition retains its separate step/depth checks.

The exact forming capability replacement is:

```rust
pub trait DatomForming {
    fn datom_form(&self, path: Path, maximum_depth: Integer)
        -> Result<Datom, Error>;
}
```

Update datom-codec-kinds.ethos and its generated declaration with this extra forming-depth input. Potential::actualize passes Budget.forming_maximum_depth; direct dependency callers pass their explicit configured or fixture value. No overload supplies4096. Existing error locus/layer remains unchanged.

Remove the text-reading Protosizable::protosize() implementations for str/String that currently construct remaining4096; text callers use existing BoundedProtosizable::protosize_with with explicit ReaderBudget node/depth. Output-only structural Protosizable implementations retain their role. Every old text convenience consumer moves in the same versioned change; no fallback wrapper survives.

## Bootstrap and adapters

The approved Startup envelope begins with five typed limits. A fixed-position intrinsic uses only LexicalCursor and CanonicalIntegerReadable to read them, validates shape/positive representability, then full-decodes the SAME envelope with exactly those five limits. It does not spend the full-decode counters during prefix scanning. It accepts ordinary Datom whitespace/comments; no alternate grammar or recursive pre-parser.

Ordinary Invocation, Meta Invocation, composer input and HookConfiguration each explicitly supply the codec/frame settings consumed by that process. Composer and hook target-invocation settings are separate from their own decoding settings. These records are Nix/launch-produced configuration, not lookups into Nexus Memory before connection. Exact field additions must update every producer/consumer and remain one source of configuration.

Nexus-owned Datom decoding uses its committed RuntimePolicy budget snapshot. Codex WebSocket proxy byte settings also remain in Nexus RuntimePolicy, passed to its adapter at operation construction. WebSocket byte allowances have no demonstrated bound in the textual Codex character maximum; no dimensionally invalid comparison is added. Client response-frame limits belong to client invocation configuration. Shared TYPES do not mean shared mutable values.

Each length-prefixed boundary has ONE explicit FrameBytes allowance applying to both inbound and outbound messages at that boundary. Check configured bounds and checked usize-to-u32 conversion before ANY outbound prefix/payload write; check inbound length against configured allowance before allocation. u32 representability is the fixed wire invariant, not an operational default. Flow/Meta clients and Nexus CarriesSignalFrames all change together; their independently owned allowances need not have equal values. Oversized outbound messages refuse before partial emission. WebSocket header/message allowances are separate adapter fields, not this u32 framed contract.

## Acceptance

Independently force each stage's cap with the other four ample: structural nodes, structural depth, forming depth, composition steps, composition depth. Check exact boundary and one-over cases at the actual stage. Prefix missing/zero/negative/overflow/noncanonical/arity refusals precede general parse and side effects. Equivalent whitespace/comments must match existing codec. String bytes/raw argv size are not claimed bounded by node/depth limits. Client frame/WebSocket limits test their own byte boundaries separately.

Required pre-body evidence: independent codec clone locks/pins; narrow helper/signature review; every ReaderBudget/Budget/direct-former consumer and generated invocation/Nix/hook producer; namespace allocation; coherent dependency pins. Post-body source/fault tests then prove the specified behavior. This does not authorize changes to cached sources, broad codec redesign or a second parser.
