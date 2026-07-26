RULINGS RECEIVED — RESUME FROM STOP-THE-LINE

Two psyche rulings landed since your spike report. Append both to the
design log under protos-engine/design/ per its convention (each with
the agent text it answered; supersede by appending, never edit).

RULING 1 — capsule pin. Asked directly: did he rule the complete
composition? Psyche: "yes". A capsule pins the complete composed
nametree. Strike it from the open list. Consequence already folded
into your standing prompt: schema and logos capsules ride the
pipeline as the first production Capsule implementors; their
composed-nametree identity derives from real name-table slices, not
fixtures; rust-logos gets no capsule, only the fixed textualform
association.

RULING 2 — Rust structural rules are FULLY TYPED RECORDS. Shown the
spike's Product["struct", name, (...), ";"] representation, psyche:
"wtf is this garbage? Thats a vector of strings, not typed data! it
should be fully typed struct." Offered the fork explicitly — (1)
typed rule records in a custom structuretree vocabulary vs (2) keep
generic protos forms and teach the prover positional comparison —
psyche: "1".

This ratifies and sharpens his earlier ruling that rust-like
languages get "a custom structuraltree which is quite different than
protos primitives." Requirements:

- rust-logos defines a typed rule vocabulary. Each grammar rule is a
  typed record whose positions are typed — for the newtype item:
  Attributes, Visibility, ItemKeyword, TypeName,
  Parenthesized(TypeReference), Terminator. No homogeneous
  Vec<StructuralForm>, no literals-at-indexes, no position counting.
- The shared evaluator runs this vocabulary alongside the protos
  primitives. Same evaluator, second driven vocabulary — not a
  parallel engine, not handwritten match arms.
- Disjointness is proven over typed positions: two rules are disjoint
  at the first position where their types cannot accept the same
  text (ItemKeyword "struct" vs Visibility "pub"). The conservative
  refusal posture stays: what cannot be proven disjoint is rejected.
  You gain proof power through types, never by weakening the check.
- Your spike's two blockers are now requirements of this vocabulary,
  not patches to the old one:
  a. Item grouping is a typed boundary rule of the Rust structuretree
     — an item's extent is found structurally (attributes, then head,
     then the matching terminator: semicolon or balanced brace),
     boundary-first, preserving nested #[...], parens, and braces.
     This is his "delimiters are more complex rules — that's the data
     we need" ruling made concrete.
  b. The typed-position disjointness proof replaces the product-blind
     comparison for this vocabulary. Do not modify the protos-
     primitive prover's behavior for existing tables.
- Spellings live as data ON typed positions (ItemKeyword carries
  "struct"), never as bare strings in a sequence.

RESUME ORDER
1. Re-run the slice-0 spike against the typed vocabulary design: model
   the newtype subset (private and pub) as typed rule records and
   prove disjointness over typed positions. This can be a disposable
   witness again — green spike before plumbing.
2. Then slice 0 b/c/d (repins, structural-codec API migration,
   protos-engine allowlist fix) unchanged from the standing prompt.
3. Then slice 1 unchanged, with the Rust textualform built on the
   typed rule vocabulary.

All standing laws unchanged. Stop-the-line still applies: if typed-
position proof hits a case it cannot decide (genuinely overlapping
Rust prefixes beyond keyword/visibility), stop and surface it — do
not order-resolve, do not special-case.
