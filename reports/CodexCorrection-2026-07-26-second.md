SECOND AUDIT VERDICT + CORRECTION — revised with the block-model ruling

Read with /home/li/primary/reports/CodexCourseCorrection-2026-07-26.md.
This version supersedes any earlier copy of this file.

NEW PSYCHE RULINGS — append to the design log verbatim, dated 07-26,
per its convention. The dictation below is his words, unedited.

Ruling A — the block model (dictated; he opened this after being
shown that the shipped textual-decode replacement was refused):

"Okay, so let's go over this together. In all languages there's
blocks. And these blocks can be represented by typed data, which is
what we have, the encoded form. Plus their names, right? The capsule.
So in a protose language, the delimiters are very straightforward.
And all one has to do is balance them out to find the beginning and
the end of blocks, along with, I would say, the prefix to the opening
delimiter, right? Which we have the dotted prefix. So the first pass,
and I actually wanted to do this, and I've talked about this before,
and I thought, well, I don't assume that my designs are being
implemented anymore. But in my mind, because agents have proven that
they can't follow my instructions yet, I think because my system
isn't complete enough yet, not because the models are not capable,
but because the ontology isn't there yet, and the structure, and the
memory system, and everything isn't properly set up. So we're doing a
lot of this by hand. I'm repeating myself now, but I'm going to go
deeper. So there's a logic to finding the beginning and the end of
each blocks. And so we could say that we have different variants of
block delimiters, of finding the beginning and the end of a block.
And I know that Rust is more particular because there's a lot more
rules that are involved in balancing out, so to speak, the
delimiters. They don't really have delimiters, but there's inclusive
and exclusive delimiters, I would say. So when we look at a Rust
block, let's say it starts with struct. Struct is the beginning cue,
right? It's the cue that there's a struct block that begins here. And
to find the end, we have to follow all of the parsing rules that
apply inside of a struct, that could possibly apply inside of a
struct, to find the final semicolon. Meaning if we come across
certain things, then there's a certain number of semicolons that have
to be skipped, right? So we could say this is an inclusive, meaning
the struct keyword is part of the block. It's an inclusive complex
block. And then we have exclusive. On the other side of the spectrum,
we have exclusive simple blocks, in which the delimiter is not really
part of the block in the sense that when we want to parse the inside
of it, we don't need to look at the delimiters, which are parentheses
and braces and square brackets. But we do have the prefix, which is a
bit of a trick, because actually we could say that there's no such
thing as an exclusive block because of the dotted prefix. The dotted
prefix, the word, the prefix word is part of the data of the block.
So we should just look at it as a whole, including the parentheses
and the square brackets and so on. It's just the logic for finding
the end of the block is different. And that inside logic, which can
also, by the way, find the inner blocks. Because as it looks for
clues to tell it that it needs to skip some more closing delimiters,
it also finds other blocks. So we could have sort of this recursive
block beginning and ending pass, which has different logic for
different languages, which is really simple for the Protus family of
languages. And then with that pass done, then we can do the typed
parsing, because we've found the blocks. It's a lot easier to just
pass these strings now, which are limited to only their content, and
parse them through the structural typed parsing step."

Ruling B — the block tree is a trait:
Agent: "The block tree itself can be one universal shape — bounds,
cue/prefix, children — because it carries no typing at all"
Psyche 07-26: "so it should be a trait. we love traits; they make
agents smarter by giving them an ontology (that could go in
standards, in a better presented form)"

Ruling C — pass-1 opacity:
Agent: "In pass 1 for Rust, the scan must still treat strings and
comments as opaque (a ';' inside a string literal terminates
nothing)?"
Psyche 07-26: "yes"

Ruling D — source bounds:
Agent: "The block tree keeps source bounds so every later error can
point at bytes?"
Psyche 07-26: "yes"

THE ARCHITECTURE THESE RULINGS FIX

Two passes. Pass 1 is recursive BLOCK DISCOVERY driven by
per-language block-boundary rule data — not full grammar:
- Protos family: balance delimiters; the dotted prefix word is part
  of the block's data (there is no truly "exclusive" block — prefix
  plus delimiters plus content is one whole; only the end-finding
  logic is simple).
- Rust-like: cue-opened, rule-terminated, inclusive — the cue
  (struct, enum, fn, ...) is inside the block; the end is found by
  following only the termination rules (what changes how many
  semicolons/closers to skip). Those rules are the "that's the data
  we need" from the standing 07-23 ruling. While scanning for its
  own end this logic also discovers inner blocks — that is the
  recursion.
- Carriers (strings) and comments are opaque to pass 1 (Ruling C).
- Every discovered block carries source bounds (Ruling D).
- The discovered block tree is one universal shape expressed as a
  PROTOS TRAIT (Ruling B): bounds, cue/prefix, children, content —
  no typing. Per-language discovery logic yields per-language
  implementors of the trait. Note as a standards candidate: traits
  as agent ontology.

Pass 2 is the existing expectation-driven TYPED STRUCTURAL PARSING,
run per block over content-bounded text, producing EncodedForm +
NameTree — the capsule.

WHAT LANDED WELL (unchanged from the audit)

Spikes preserved and pushed with refusal coverage restored. R3
kernel retype real and absorbed into the ONE shared evaluator (the
parallel spike engine was not promoted). R4 type-id retype correct
(namespace-variant-wrapped u16, private fields). All three identity
fixes correct. disjoint.rs structural and conservative. The
content-identity short-display implementation matches the ruling
exactly. All frozen surfaces untouched. No new agent-derived law.

BLOCKING PROBLEM 1 — PUBLISHED STATE IS BROKEN

content-identity main deleted ShortCode (correct). protos main still
imports and re-exports it and its Capsule supertrait still returns
it: the two published repos cannot compile together. Retire protos'
ShortIdentifier supertrait, re-exports, and the getter from the
Capsule contract, and land that together with the structural-codec
push so the family regains a composable published state.

BLOCKING PROBLEM 2 — SPLIT THE UNPUSHED COMMIT

The 29-file commit mixes R3, R4, identity fixes, pins, re-locks, a
subsystem replacement, and a 54% test deletion. Split it: kernel
retype, type-id retype, identity fixes, pins, and re-locks each
stand alone. Every commit names its behavior change in its own body.

BLOCKING PROBLEM 3 — THE TEXTUAL DECODE REPLACEMENT, REFUSED AS
SHIPPED; REBUILD AS THE BLOCK-DISCOVERY PASS

The shipped replacement is not the psyche's pass 1. Evidence:
- Its recognizer finds a closing boundary by parsing EVERY interior
  object with full grammar — not by termination rules. The one true
  balanced scanner in the family (raw-discovery discover_delimited)
  is dead code, called only from its own tests. It is nearly the
  protos-family pass-1 variant already — minus dotted-prefix
  attachment. Seed the rebuild from it, do not rewrite it.
- One document-wide trigger set, fixed at construction: every
  trigger live at every byte.
- Boundaries hardcoded to ( [ { — any other opener rejected; angle
  brackets unrepresentable, which alone disqualifies it for
  rust-logos.
- Blocks carry no source bounds, so decode errors carry no position
  (now directly contrary to Ruling D).

Rebuild requirements, in the rulings' own terms:
a. Pass 1 discovers blocks by balancing/termination rules only,
   never by full interior grammar; recursion comes from the
   end-finding scan discovering inner blocks.
b. Per-language rule data selects the variant: protos
   delimiter-balancing with dotted-prefix attachment now; the
   rust-like cue/termination variant lands with rust-logos as rule
   data, not code.
c. Carriers and comments opaque; source bounds on every block; any
   boundary spelling the profile declares is admissible.
d. The block tree is the protos trait of Ruling B.
e. Pass 2 is the shared typed evaluator, unchanged in role,
   consuming block content.
f. Restore or reimplement the deleted evidence: conformance laws 1-4
   and the boundary-first suite re-established against the two-pass
   arrangement before it lands. Coverage is the proof the new engine
   behaves; deleting it silently is what the last audit caught.

SLICE STATE — ZERO PROGRESS SINCE LAST AUDIT; RESUME HERE

1. core-nomos: still pinned to the dead monorepo revision for three
   of four engine crates, still Core*-named while core-logos already
   renamed, name minting live on the newtype slice path (case
   derivations in the name boundary; leaf_path text literals for
   Integer/String/Boolean/Bytes and Vec/Option/ScopeOf/Map heads).
   Repin, rename, take the newtype path string-free with
   NameProjection::Exact as the typed carrier.
2. core-schema: unify the duplicated reflection family — the
   trait-facing leg hard-fails on un-interned builtin spellings
   where the direct leg interns and succeeds. One path, one
   behavior. The string-keyed builtin lexicon dies with slice 1's
   builtins-as-priors; do not grow it.
3. rust-logos does not exist; textual-rust not renamed; its declared
   structural-codec dependency is never used — 66 quote! sites and
   202 syn references remain the whole mechanism.
4. logos-engine calls textual-rust's projector on its production
   request path — prettyplease is live in production emission. That
   leg is what the typed rule vocabulary replaces.
5. Ratified item schema still unimplemented for touched types: no
   NewtypePayload, no WrappedField, Visibility still spelled Module
   not Restricted. Field's stored name correctly UNCHANGED — leave
   it until ratified.

Open questions stay open: function parameter names, let-binding
names, capsule container enum-vs-struct, manifest self-generation,
reify/reflect derivation.

DESIGN-LOG FIDELITY

The appended fidelity correction is itself unfaithful: it asserts
"This exact agent question" over a truncated one-line rendering,
rewrites the agent text of the two short-identifier entries, and adds
a period to a psyche quote inside the correction section. Append a
further correction deferring to the firsthand record
(design/ProtosEngine/ShapeAndSliceRulings-2026-07-26.md) for all
overlapping entries; resolve the provenance conflict between the two
files (they currently disagree about whether R1-R5 were logged
firsthand, and the recency rule points at the wrong one); and
cross-reference the firsthand file from the older log. Surface
conformance law 5's homelessness in published history — its only
discharge today sits inside the unpushed commit.
