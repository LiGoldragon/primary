# Design Vision — rebuilt 2026-07-28

This document presents the psyche's design vision for the engine family, rebuilt
from two sources and cross-checked against each other:

1. `/home/li/primary/reports/CodexContextHandover-2026-07-27.md` — the corrected
   handover, whose wording is controlled by the firsthand design logs it cites.
2. Claude session `49d0a8e0-369f-47db-933e-e3dc2c6f33ba` (2026-07-26 21:45 →
   2026-07-27 10:42 UTC), re-mined from the raw transcript. This is the sitting
   that ruled the five slice-1 decisions, corrected the daemon architecture,
   dictated the sema vision, named Ethos, and commissioned the handover itself
   ("audit it, then create a better version, with a more complete and accurate
   psyche vision").

The re-mining found **no divergence** between what the psyche said in session and
what the handover records. Where this document adds anything, it is session
material the handover compressed (the conduct demands, the naming rounds) —
flagged below.

Provenance marks, on every claim:

- **[ruled]** — verbatim psyche words, character-exact from a source.
- **[confirmed]** — a restatement the psyche confirmed as his; substance carries
  his authority, wording may be an agent's.
- **[derived]** — agent-formalized standing doctrine, consistent with rulings but
  not his words. Never cited back to him as a ruling.

Later statements govern earlier ones. Open questions are answered by the psyche,
never by code.

## The vision, in one paragraph

A family of engines — **Ethos** (the schema language, the sweet syntax), **Nomos**
(the string-free transformer), **Logos** (the encoded program) — over one shared
protos substrate, in which programs exist as **typed encoded data**: identity is
integers and content hashes, never spelling; there are no field names; text —
including Rust — is only the interim interface, produced and consumed exclusively
through the name tree and the structure tree; Rust is treated as an assembly
language and emitted fully qualified so naming conflicts cannot exist. Each
engine is a stateful daemon with its own embedded sema db; one small translator
daemon owns the name-to-integer authority. The long arc — the sema vision — is a
new way of thinking about data that eventually contains no strings at all.

## 1. Two organs, one view — text is interim

TextualForm and EncodedForm, **[confirmed]** "one is a view on the other".

**[ruled]** the trees drive everything: "I had a great vision for a shared
abstraction around textualform and encodedform", "a nametree and a
structuretree", "textualform trait writes and reads the name and structure
trees", "this drives all textual en/decoding, including rust", "actually, the
vision even allowed multiple textualforms per encodedform; logos -> logos or
logos -> rust", "even nota can take this architecture; it would be the
basic/most-universal example."

**[confirmed]** the strict invariant, confirmed 2026-07-27 as his words:

> "nametree and structural tree from the protos library drive all the decoding
> and encoding to/from text with DATA - strict invariant. nothing else will do."

**[ruled]** one shared mechanism for all structure-based decoding, reused by
every parser, with a parallel shared machinery for deparsing; "the textualform
traits should force the use of structural data".

**[ruled]** the hand-written Rust reader/printer is being *replaced*, never
*rejected* — "That's DEMANDING it".

**[ruled]** text's place: "text is the current standard programming interface;
it is what we *must* work with in order to get to the future interface".

**[confirmed]** "Exactness is structural. Values that matter semantically must
have exact representations… Errors are also structural values."

## 2. The two-pass block model

**[ruled]** in one dictation (07-26, verbatim in the handover §2): all languages
have blocks; pass 1 finds block beginnings and ends by balancing delimiters plus
the dotted prefix (protos family) or by cue-opened, rule-terminated scanning
(Rust: `struct` is the inclusive cue; the end is found by following only the
termination rules, which also discovers inner blocks — that is the recursion).
Then pass 2 does the typed parsing over content-bounded strings.

**[ruled]** the block tree is a trait — "we love traits; they make agents
smarter by giving them an ontology". (Distilled to standards:
`traits-as-ontology.md`, verified present.)
**[ruled]** strings and comments are opaque to pass 1.
**[ruled]** every block carries source bounds.

**[derived]** the formalization: pass 1 is recursive block discovery driven by
per-language boundary-rule *data*, never full grammar; the block tree is one
universal shape — bounds, cue/prefix, children, content — with per-language
implementors; pass 2 is the existing expectation-driven typed structural
parsing, producing EncodedForm plus NameTree — the capsule.

## 3. Structural parsing laws

**[ruled]** boundary-first: "structural parsing doesnt reacting blindly on
characters; it has a state-machine to de/parse the type by finding the outside
boundaries first, and passing through the inside of that block again and again,
recursively and structurally."

**[ruled]** the expected type carries a payload for custom structure-based
logic; the parser picks it up when non-empty.

**[derived]** conservative refusal: disjointness is proven over typed positions;
what cannot be proven disjoint is rejected; proof power is gained through types,
never by weakening the check. Stop-the-line on undecidable cases — surfaced,
never order-resolved, never special-cased.

**Fidelity guard:** do not carry "explicitly denies horizontal parsing" as a
quote (no source contains it), and neither assert nor ban a global longest-match
law — his assent was never captured. Both stay open.

## 4. Typed data laws

**[ruled]** "wtf is this garbage? Thats a vector of strings, not typed data! it
should be fully typed struct." — grammar rules are fully typed records with
typed positions (fork option 1, ruled "1"). Spellings live as data **on** typed
positions, never as bare strings in a sequence.

**[derived, ratified-adjacent]** the R2 requirements: rust-logos defines a typed
rule vocabulary run by the *same* shared evaluator — a second driven vocabulary,
not a parallel engine and not hand-written match arms.

**[derived standing law]** no `syn`, `quote`, or `prettyplease` anywhere on the
pipeline — grounded in his rulings, but he never said the crate names; do not
attribute the sentence to him.

**[ruled]** one concession: one hand-written Rust-specific evaluator object is
permitted as MVP — "sure, if you think that's a good first MVP".

## 5. Names are positional; identity is a number

**[ruled]** "ALL FIELDS ARE POSITIONAL! … field names are now COMPLETLY ILLEGAL
EVERYWHERE". Fields "are deterministically named in the conversion to
textualform of rust."

**[ruled]** name projections confirmed as his standing design ("I thought that's
what I had designed"): derived text is a typed algebra over identifiers,
evaluated only at textualform time; disambiguation keys on **type identity,
never derived spelling**; no string anywhere in the algebra.

**[ruled]** identity: "if it got re-ID'ed then its not the same, and if it's the
same and got re-ID'ed, the system is implemented wrong". The ID shape is the
variant with its inner u16 — `Schema.Id16`, `Logos.Id16`. "encoded identity is
the only durable one". **[ruled]** "no aliases". **[ruled]** EncodedForm has no
concept of files; filenames are a beautification algorithm (his own hedge, "if
im not mistaken", kept).

**[ruled] 2026-07-27** content identity: "I think it's better if it's
Variant.ContentAddressedHash", then "Variant-only" — the kind lives solely in
the outer variant, protos-style; the hash pre-image is pure content. Existing
digests move; this rides the one bump train with the R3/R4 kernel work.

**[ruled]** short identifiers are display operations, never state: "it's a full
content-addressed hash. the short identifiers is for common display operations…
the 4 or more chars shortened version that doesnt conflict in the db". Kind-
distinct short-code types — "they should be a different type for sure".

## 6. The unified namespace

**[ruled] 2026-07-27** "I dont see any problem with all components sharing a
unified namespace; it's just an integer to string correspondance, including the
"standard" or "builtin" terms. am I wrong?" — he is not wrong. One
integer-to-string correspondence for all components; builtins are ordinary prior
entries; this **supersedes** the 07-19 one-nametable-per-component ruling (the
per-component dimension survives as slice structure of one global namespace).

**[ruled]** redefinition is an error — landing at universe seal.

**[ruled] 2026-07-27** the space is never flat: a 16-bit integer cannot fit all
of human language; "I would start with an enum at the root, which we always
prefer or almost enforce actually in daemon interfaces so that we can split the
domain." The root variant set is matter and is **undesigned** (schema.org was
floated as a possible ontology to borrow — floated, not ruled).

## 7. Daemon architecture — every daemon is stateful

**[ruled] 2026-07-27** "sema is the database of each daemon. either you are
mistaken, or the implementation is. each daemon is stateful". The 2026-07-17
"seat it centrally in sema" ruling "was later overruled" — and was mis-voiced
when given: "I shouldnt have said "in sema", since all daemon state lives in
*its* sema db. There can be no sema-storage daemon, as it would overload the
term sema."

**[ruled]** the shared nametable component is **its own small daemon** ("a, its
own small daemon"). **[derived]** working name sema-translator — a leaning, not
a fixed name. **[derived]** the durable identity-authority laws (never re-mint,
never rebind to a different shape) reseat into this daemon; sema-storage's
stateless-client architecture is dead law and the repo cannot keep its name.

The term-overload law is distilled to standards (`component-naming.md`,
confirmed by him in session: "yes. those are my words").

## 8. The sema vision — intent

**[ruled] 2026-07-27**, psyche-initiated dictation (verbatim in full in the
handover §8): sema "means more than just a database. It's a new way of thinking
about data, which doesn't contain strings eventually." Anything that is a single
word becomes a **dynamically assigned enum** — spelling-constrained, stored as
integers through the translator component. Long prose blocks stay strings for
now; changing that is "a very, very long-term thing".

**[ruled]** dynamic enums "could later be re-compiled into proper enums, while
keeping their place in the translator table" — identity survives graduation.

**[ruled] — intent-grade**, his words:

> "the ultimate computer language cannot use strings, since they are an
> extremely inefficient way of representing a set (which language is)"

(qualified by "almost, if it is extracted into a universal").

**[ruled] — standing preference:** the names, root variant set, and ontology
borrowing are "something to distill into standards; which I want to lean on
more, and use more now."

## 9. Capsule

**[ruled]** the full 07-23 dictation (handover §10): a capsule per namespace
mirrors the file concept; conflicts are dealt with at each layer; emitted Rust
is always fully qualified — "we treat Rust like an assembly language" — so
naming problems cannot exist in the compiler; a top-level capsule is the
manifest; capsules are otherwise homogeneous, each able to declare
executable/library and public/private sub-namespaces; Logos accommodates Rust
without following it exactly.

**[ruled] 2026-07-27** the container is a **generic struct** — kind as a type
parameter, kind-distinct types by construction (closes his earlier "im not
actually sure").
**[ruled]** the name is "Capsule". **[ruled]** a capsule pins the complete
composition of its nametree (re-confirmed against a prior fabrication).
**[ruled]** rust-logos gets no capsule; a textualform-transformation object is
*fixed* to a capsule kind — though he reopened the opposite ("OR, rust has also
a capsule…?") and that reopening is still open.
**[ruled]** capsule and short-identifier are protos concepts — protos traits
with per-engine implementations. **[ruled]** capsule-to-crate correspondence is
optional, driven by generated-code accessibility. **[ruled]**
"content-identity is that library — add ShortCode to it" (the *stored* ShortCode
value model has since died under the display-operation ruling; the library seat
stands).

## 10. The names — Ethos

**[ruled] 2026-07-27** the schema language is **Ethos** ("yes, ethos"),
completing Ethos → Nomos → Logos. Repo renames were directed ("If so I want
that done") and the whole living family confirmed ("yes, we'll have all those
renamed as well"). **Executed and verified:** core-ethos, ethos-engine,
signal-ethos, tree-sitter-ethos; GitHub redirects live.

**[ruled]** NOTA keeps its name — "nota is fine". Session detail the handover
compresses: he first asked for NOTA candidates too, then reversed within the
exercise. Constraint rulings from the rounds: "the -os isnt a constraint",
"we arent tied to greek", "no, not english", "eidos isnt very evocative for
english speakers", "no, nothing pulls me" (twice).

## 11. Pipeline

**[ruled]** "schema is the sugar, sweet syntax" — schema keeps a dedicated
declaration surface. **Recorded contradiction, unreconciled:** earlier the same
day he ruled "make them the same thing - exceptions are symptoms of bad design".
Recency gives the sugar ruling the floor; do not resolve by inference.

**[ruled]** the no-strings nomos invariant: "in the nomos transformation (schema
to logos), there shall be *no string manipulation/introduction/reading of any
kind*", with walkers at the boundary. **[confirmed]** "transformers are data".

**[ruled]** the manifest is a nota config associating files to top-level
namespaces with rust-like directory resolution rules — with his own open flag:
"we can generate rust with modern syntax schema? <- big question actually".

**[derived]** there is no logos source: logos is produced by nomos from ethos,
never authored as text — follows from the pipeline, not a psyche prohibition.

## 12. The ratified item schema

The full typed item block (handover §13) stands ratified by **[ruled]**
"otherwise I like the syntax." — **what "otherwise" excepted was never
recovered.** The ratification is conditional on something that cannot be named;
flag it wherever the block is relied on. Supporting rulings: every item kind
takes the brace payload; the first field is the identifying subject, realized
positionally; `Field` carries no name; the escape set is closed at two
primitives (`$x` realizes, `$@xs` splices — "agreed").

## 13. Topology

**[ruled]** micro-repos only: "we dont use the monorepo style", "the
consolidation was never approved", "the monorepo was an agent
hallucination/bad-decision" (reversing his own 07-19 "consolidate into protos").
**[ruled]** protos.git holds the common daemon traits; protos-engine is "a new
ASSEMBLY repo, not an engine source repo", mostly nix plus launch scripts plus
tests. **[derived]** the dependency-sink law: nothing links against
protos-engine; its micro-repo deps are published git revs, never path deps.

## 14. Acceptance

**[ruled]** "I dont care about byte-exactness. get rid of that. working programs
is what we want." **[ruled]** "near roadmap is getting everything running on the
new protos engine and testing the hell ouf of it." **[confirmed]** the
spirit-port test: Spirit ported to the new engine, normal operations against an
isolated migrated copy of production data, zero dependency on schema-rust, no
compatibility adapters. **[derived]** vertical slices, each compiling and
running the generated Rust; witness oracle — scratch crate, real cargo compile,
behavior round-trips, no byte-golden.

## 15. How the psyche is asked — conduct, in his words

The handover's rule — every question is explained in practice: storage, sharing,
failure paths; a yes/no wrapped around an undesigned mechanism gets sent back —
was earned in this session. **[ruled]**, the session verbatim:

> "am I supposed to understand this? Do you? Like *actually understand* what
> that means in practice?"

> "that still doesnt explain anything about this "stored tabe" - where is it
> stored? how is it shared between the 3 daemons? How are stale entries dealt
> with? probably more questions I havent thought of"

And on decision 5 he answered simply "5. explain" — the ruling came only after
the mechanism was concrete, and came as a reshaping ("Variant.ContentAddressedHash",
"Variant-only"), not as the yes/no that was posed.

## The five slice-1 decisions — all closed 2026-07-27

1. Capsule container: **generic struct** [ruled].
2. Durable declaration IDs: **yes**; the authority's seat is the new small
   nametable daemon [ruled via §7]; its design needs a proposal before code.
3. SchemaStandard variant: **no as posed** — superseded by the unified
   namespace [ruled].
4. Wrapped-field visibility: **"yes, Private"** [ruled].
5. Whole-logos identity: **yes in substance, reshaped** — Variant-only
   content-addressed identity [ruled]; digests move on the one bump train.

## Undesigned — needs a proposal before any code

- **The nametable/translator daemon**: name (sema-translator is a leaning), wire
  contract, minting flow, how the three engines consult it.
- **sema-storage dissolution**: repo rename, migration of document storage into
  per-daemon sema dbs, correction of its dead-law ARCHITECTURE.md.
- **The unified table's root enum variant set**, possibly borrowing an existing
  ontology (schema.org was his suggestion to examine).

## Open questions — do not infer

1. Function-parameter and let-binding names (nearest word: let statements are
   "semi-anonymous (very private) types" — not a ruling on parameters).
2. Micro-capsule: full pin or light pair ("might need").
3. Manifest self-generation — his own "big question actually".
4. reify/reflect: eventually derived? No psyche words exist.
5. StringLiteral remedy: `NameLiteral(Identifier)` vs rename-instability.
6. Plane vocabulary survival — deferred until daemon emission.
7. His reopened question: does rust get a capsule as a different syntax for
   logos?
8. The global longest-match law — neither assert nor ban.
9. What "otherwise" excepted in the item-schema ratification.
10. ID retirement policy (stale entries are inert; retirement itself unruled).
11. The translator daemon's final name.
12. The root enum's variant set, and whether to borrow schema.org.

Slice 2 still opens by presenting the deterministic field-naming rule for
ratification.

## Fidelity notes from the session re-mining

- The handover was commissioned in this session and matches it; nothing the
  psyche said in session contradicts the handover.
- Prior-session quotes pasted into the session's opening context keep their
  original dates; nothing there is 07-26/27 speech.
- Two messages exist in the transcript as edit-before-send drafts of their final
  versions (the daemon-statefulness correction and the no-sema-storage-daemon
  ruling); only the final versions are statements.
- The provenance confirmations "yes, those are my words" (07:44, for five
  circulating quotes; 10:31, for the term-overload law) are themselves rulings
  and anchor those quotes' authority.
- Both standards directives from the session are discharged and verified
  present: `component-naming.md` (noun rule, term-overload law) and
  `traits-as-ontology.md`.
