# Ethos File Structure, Clean Cut, Traits Doctrine — 2026-08-02

Rulings and vision from the psyche's spoken answer to the Ethos production
bootstrap proposal's question A (which asked how to treat the legacy
six-slot form). Quotes condensed from dictation.

## Ruling 1: clean cut — the old form is not a topic

**[psyche-verbatim, condensed]**: "We don't care about the old form. We
never care about the old form, especially now... I don't want to talk
about the old form for the sake of the old form. If it's a good idea,
then great, but that's the only reason we might even ever bring it up...
we're making a clean cut here. It's over. We don't need to think about it
anymore."

Seated: the six-slot form and its migration are dissolved as design
topics. Proposal question A is void — there is no bridge question, no
migration phase to schedule, no old-form authority to respect. Old
mechanisms may be mentioned only if independently good ideas.

## Ruling 2: every Ethos file is header, imports, body

**[psyche-verbatim, condensed]**: "all of the ethos files will have as a
first object... like a header that gives us a hint for the type... we're
going to want to have a version in there and an ethos type... the import
is universal. It's just the second object. And then we have the content
or body... which will be ethos type specific."

Seated:

- Three top-level objects: **header**, **imports**, **body**.
- The **header** carries at least a **version** and the **ethos type**
  (file kind). It is how the reader learns the body's root type — this
  supersedes the expected-root-identity-only kind selection of the
  overnight slice (`primary-pjm-A1`'s selector aspect).
- **Imports** are universal across file kinds — the second object.
- The **body** is file-kind-specific; the file-kind law stands: kinds
  differ only in the body's root type, one shared machinery.

Open sub-points, not ruled: what the version versions (language/format,
declared content, or both); whether the header is exactly two positions
or extensible; exact header spelling.

## Ruling 3: initial file kinds

**[psyche-vision]**: database specification ("which is going to open the
door for eventually implementing the data evolution engine"); public
interface specification (the signal communication protocol, the old
input/output idea reborn without the old form); and likely a
design/traits file kind ("really useful for when designing").

## Ruling 4: input and output are traits

**[psyche-verbatim, condensed]**: "the old schema had this input section
and an output section, but in terms of code, they would do the same
thing... whereas I think they should fall under a trait. So then these
types implement the input trait and the output trait, meaning when the
code calls them, all it does is treat input and emit output on all of
these different objects, which creates the great cognitive reuse."

Seated: input/output are not structural sections that merely generate
types; they are trait memberships. A message type is an input because it
falls under the input trait, an output likewise. (Manager verification
commissioned: whether the ancestor's input/output sections were in fact
codegen-identical.)

## Ruling 5: traits doctrine deepened

**[psyche-verbatim, condensed]**: "traits... give us the high-level view
of the behavior of the program... they create shared mechanism that the
objects implement, which creates reusable logic... most people implement
traits as docs. So traits are actually more succinct... the ideal code
documentation that are actually used by the compiler... writing a bit
more code for agents is really not a big deal. So we can write traits for
every method. Not every method has a trait, but every method falls under
a trait. And we want to develop standards for agents to agglomerate
behavior under certain names, which is to say under certain traits."

Seated: extends the seated traits-first standard. Every method falls
under a trait; trait proliferation is not a cost in the agent era; a
standards item is warranted for the shared trait vocabulary (how agents
agglomerate behavior under named traits).

## Ruling 6: naming — traits lean, contract suspect

**[psyche-verbatim, condensed]**: traits are "well-named, but maybe we
want to think about different names... you've said contract before, but
because we're using contract in other ways — and you can find out about
that — it might be overloaded."

Seated as lean: the declaration form leans **Trait** over **Contract**;
manager commissioned to verify how "contract" is currently used across
the corpus before the name is fixed. Also open: whether a trait
declaration needs any tag at all where its body position already implies
it (non-repetition).

## Appended 2026-08-02: both commissioned verifications returned

**Contract overload — CONFIRMED, worse than suspected.** Beyond the prose
trait-synonym sense, `Contract` is a shipped Rust type in `signal-criome`
— a governance/authorization root of trust (`Contract::root`,
`AdmitContract`, `ContractAdmitted`, `ContractDigest`,
`AuthorizedObjectKind::Contract`) actively consumed by `spirit` and
`orchestrate`, two of the four ruled first targets. Additional live
senses: wire/version negotiation (`ContractVersion`,
`CURRENT_CONTRACT_VERSION`, `GenerationClass::WireContract`), a
legal-domain taxonomy value (`LawDomain::Contract`), and ad hoc boundary
wrappers. Verdict: "Contract" is unavailable as the Ethos
trait-declaration name; the **Trait** lean hardens.

**Input/output codegen identity — CONFIRMED.** The ancestor's
`TrueSchema::input_and_output()` merges both sections with no origin tag
(`schema/src/schema.rs:610-612`); the sole codegen consumption site
(`schema-rust/src/lib.rs:633-643`) pushes both through the same lowering
with no branch on section — identical derives, traits, naming. The
psyche's recollection was exact: the sections carried no behavioral
difference, reinforcing ruling 4 — membership belongs to traits, not to
sections that merely emit types.

## Appended 2026-08-02, later same session: header ruled, imports confirmed textual-only, no-tag ruled

Agent text answered: the manager's pushback — header minimalism and
version semantics; the imports authored-versus-derived tension; the
no-tag lean for trait declarations.

Psyche rulings [psyche-verbatim, condensed]:

- Header: "with the tiny header... the version for now should just be
  like a SemVer, incrementally bumped up by the writer whenever something
  feels like it could break... and the type. And just those two things
  for now in the header... maybe [it] describes the version of ethos that
  this uses. So the version number of the ethos used last, that last
  worked with this content."
- Imports: "imports are just for the source files... in encoded form we
  don't think about imports... everything's just pure code... we use the
  encoded name to find them. And encoded names are used in the code and
  the true name is used in the table that matches encoded name to true
  name to find the code, which is stored with the content address
  storage."
- No tag: "that's the whole point of creating different file types...
  it's a specialized file, so you obviously don't need to repeat
  yourself."

Seated:

- The header is exactly two things for now: the **ethos type** and a
  **SemVer-style version**, writer-bumped when a change could break,
  denoting the Ethos version the content last worked with. A bumping
  standard comes later.
- Imports are textual-form-only, confirming the three-layer ruling:
  encoded form addresses absolutely — encoded names in the code, the
  table mapping encoded name to current true name, content-addressed
  storage holding the code.
- In a specialized file kind, declarations carry **no kind tag** — the
  file type supplies it. In a traits file:
  `ScopeContainment.{contains.{Scope Bool}}`, no Trait or Contract head.
  The trait-versus-contract keyword question mostly dissolves; what
  remains is naming the file kinds themselves when the fixtures are
  authored.

Floated, explicitly not pushed [psyche-thought]: a source file might
carry an ancestor reference — the hash of an older encoded version that
already has a slot in the daemon, "put that hash back into the source
file." Connects to the encoded-name minting sub-choice (first-version
true name) and evolution lineage; recorded for later.

## Appended 2026-08-02, later same session: interface body confirmed, nexus introduced, sema naming

Agent text answered: the manager's four-position interface body (inputs,
outputs, refusals, shared types), the refusals-generate-Rust-errors
account, and the signature conventions (last position return, receiver
implied).

Psyche ruling [psyche-verbatim]: "that looks good, yes." Also directed: a
deep design hunting gaps for MVP protos-based components, "with the
signal repos obviously adapted, as well as the in-repo database
specification (formerly called sema.schema; we could call it sema.ethos
for now, unless you have a better suggestion)".

Seated:

- The interface file body is four positions: **inputs, outputs, refusals,
  shared types**. Refusal declarations generate the Rust error machinery;
  membership in the input/output/refusal traits is positional and never
  written.
- Signature conventions confirmed: `method.{Params... Return}`, last
  position the return type, receiver implied by trait membership,
  borrowing and dispatch owned by the Nomos object.
- The per-component database specification file is `sema.ethos` for now
  (formerly sema.schema); the header carries the kind, so filenames are
  convention.

## The nexus [psyche-vision, same session]

**[psyche-verbatim, condensed]**: "what we used to call the nexus...
describes the main machinery of the logic of the daemon, how it
transforms things. So perhaps that's a different kind of file... we used
to use the same input-output concept, which arguably is valid, but is
also invalid in the sense that every one of these components is
significantly different in implementation... if we're defining the traits
in ethos, then we need to define the types — the inputs and outputs, the
signature for the methods for those traits — so they can be referenced.
So perhaps that's mostly what the nexus is: defining the types that its
traits implement and its traits. Like Spirit has a judge that judges
whether an entry is valid to be accepted — you would have this trait of
validate or judge, and then the types that come in and out of that
judgment apparatus."

Seated as vision: the **nexus file kind** declares the daemon's internal
machinery spec — its behavior traits and the types those traits' method
signatures reference. The old file-level input/output idea for the nexus
is demoted, not lost: in/out is real per method, so it lives in the
signatures, not in file sections. Manager brainstorming and the MVP deep
design commissioned in this session's proposal thread.
