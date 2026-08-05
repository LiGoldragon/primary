# Vision Reacquisition Rulings — 2026-08-05

## Ethos sources live in the owning component's repository

Agent text answered: the implementing codex session proposed creating a
`spirit-ethos` repository as a canonical public source home for Spirit's
`interface.ethos`, `nexus.ethos`, and `sema.ethos`, citing avoidance of
cyclic release ownership; the management session relayed the proposal.

Psyche: "we dont use a separate repo for ethos sources. why would we do
that?"

Ruling: Ethos sources are not split into a separate source repository.
They live in the repository of the component they describe. The
`spirit-ethos` repository proposal is rejected.

## Shapes keep bare angles; traits take a distinctive delimiter pair

Agent text answered: the management session argued the delimiter split
should give the cheap ASCII pair to the frequent kind — corpus counts
show shape applications outnumber trait pickups ~2:1 in young fixtures
and ~7.6:1 in mature code, and `Vector<Ordered>` is the Rust-shaped
surface whose recycled cognition bare angles were chosen to preserve —
so shapes keep `< >` and trait pickups take the new distinctive pair.

Psyche: proposed "a delimiter for shapes, to differentiate them from
traits"; answered the frequency-based inversion with "sounds
reasonable" and "is this always true though? If so then fine." The
corpus count confirmed it is.

Ruling: the two quality kinds are differentiated on the surface by
delimiter. Shape applications keep bare `< >`. Trait pickups take a
distinctive delimiter pair. This supersedes the 2026-08-04 "one
surface syntax; resolution classifies" ruling. The choice of the trait
pair (guillemets versus corner brackets) and the placement of the
trait mark inside shape slots are not yet ruled.

## Guillemets are the trait-pickup delimiter

Agent text answered: the management session presented the measured
candidates — guillemets best on every axis (+0.50 tokens per pair,
normal width, normalization-stable) but spending the reserved
extension pair; corner brackets equal in price but fullwidth.

Psyche: "guillemets"

Ruling: trait pickups are delimited by guillemets `« »`. The
2026-08-04 reservation of guillemets as the extension pair is spent by
this assignment and is superseded. The placement of the trait mark
inside shape slots remains unruled.

## Identity scheme: true names hash pure bodies; encoded names are table-assigned

Agent text answered: across the session the management agent proposed
successively heavier mints (birth records carrying name and place,
change-log chain parents); the psyche cut each — place is too much,
the textual name is not content ("if the object is literally the same
object, then it doesn't need a different true name"), and proposed the
association table `[{A X} {B X}]`; he then observed true names face
the same circular-derivation problem and that the right angle might
dissolve it. The agent assembled the resulting scheme; the psyche
confirmed: "that looks right."

Ruling:
- True name = hash of the object's full body — its own name excluded,
  references included, each reference present as the referent's
  encoded name. Identical bodies share one true name; deduplication is
  the point, not a collision.
- Encoded names are randomly minted, not content-derived. Identity
  lives in the association table `{EncodedName TrueName}`; two
  identities may point at one content.
- The table is the living state of the system, updated by atomic
  operations; the change log records every association, so identities
  replay by reading, never by re-derivation.
- References to living objects are by encoded name; true-name hashing
  never resolves them, so self-reference and mutual reference among
  objects cost nothing.
- Rebirth mints fresh: a deleted object recreated identically is a new
  object. Deletion is a real death.
- True-name (Merkle) recursion is reserved for frozen closures — pins,
  releases — where the dependency DAG law bars cycles.

This resolves the open encoded-name minting question recorded in
threeLayerNamingAndNomosBootstrap-2026-08-01: the mint is random.

## Trait marks stand everywhere; the guillemet pair is a requirement vector

Agent text answered: the management session asked whether the trait
mark appears everywhere a trait stands or only at bare pickup slots.

Psyche: called the question nonsensical — "of course, if something is
a trait, it's marked as a trait structurally using whatever syntax we
use to mark traits." The real question is whether delimiters are
needed at all, "and the only reason you would use a delimiter is
because there's more than one symbol as a payload" — the guillemet
pair "totally opens up the possibility of putting multiple traits in
there," where the meta-trait alternative has elegance but "a lot of
complexity."

Ruling: a trait requirement is guillemet-marked at every position it
occupies, including inside shape slots. One guillemet pair may carry
several trait symbols; the slot then requires all of them. Meta-traits
remain expressible but are not the mechanism for multiple
requirements. Unmarked names inside shape slots are ordinary type
references.

## Import entries carry their names in a square-bracket vector

Agent text answered: the management session reported the fixture
import spellings `interface.{Entry Referent RecordSet}` and
`interface.{Entry Referent} signal-domain.Domain`.

Psyche: the braces are "agents just mindlessly copying what they
find" — the payload is a vector of names, and square brackets are how
vectors are mentally portrayed (the same reason enum variants use
square brackets: a list of possibilities is a vector). The dot
separator and the lowercase module spelling are fine.

Ruling: an import entry's imported-name payload is a square-bracket
vector: `interface.[Entry Referent RecordSet]`. Braces are wrong
there. The dot between source and payload stands for now; the
qualification syntax underneath (module versus repo, and the proposed
`:` name qualifier) is under active design and not yet ruled.

## Textual-form metadata is bound to the encoded identity

Agent text answered: the management session asked whether one nested
hierarchy covers module and repo imports, how import entries are
spelled under `:`, and how the module segment is capitalized.

Psyche: the name table generalizes — "we extended the concept of the
textual form name table. It's just the textual form metadata," bound
to the encoded ID. All textual-projection information for an object
lives in that one place, including where the object lives in terms of
files. Operational renaming targets "the configuration object in such
module, in such crate or metamodule" — one specific object resolving
to one encoded ID, never a spelling-wide textual rename. Lookups must
work in both directions.

Ruling: textual-form metadata is a single record per object, keyed to
the encoded identity, carrying the visible name and module/file
placement; module qualification therefore lives in metadata, not
inside the object's name proper. Rename operations resolve through
this metadata to exactly one encoded identity. This extends the
2026-08-01 three-layer naming design.

## The colon qualifies in import space; symbols are context-scoped

Psyche: "I agree with the colon, I think," noting that with
textual-form metadata the stakes drop and the reading can be scoped:
"we can treat the colon differently in the import space. Our parser
should be able to be context dependent." The colon is already a legal
character inside unquoted single-word strings (the Nix-style
`github:owner/repo` path precedent), and in import space it serves
visual cognition — signalling importing, not defining. Token
efficiency in this exact context should still be measured; the colon
must conflict with nothing.

Ruling: the colon is adopted as the qualification separator in import
space, as a context-scoped reading rather than a globally special
symbol. Unquoted single-word strings remain legal with interior
colons.

## Parsing is a context machine

Psyche: "at any point there is this parsing context machine that
decides how parsing proceeds." Angle-bracket delimiters cannot collide
with arithmetic comparison because typed positions say what is
expected — inside a typed arithmetic block the parser is "not looking
for the closing delimiter. It's looking for the end of the arithmetic
block." How contexts are known "is our job as designers of the ethos
language."

Ruling: the parser is context-dependent by design; every symbol's
meaning is scoped by the active typed parsing context. This seats the
2026-08-04 finding that bare angle brackets are safe under structural
parsing as a general law.

## Root-container terminology is open

Open question, psyche requested brainstorm: the name for the outermost
module container. "Repository" is wrong (version-control connotation,
and a monorepo holds several crates); "root" is overloaded; Rust's
"crate" shows coining a term is legitimate; "root module" and
"metamodule" were floated without enthusiasm. Modules recurse
indefinitely beneath it (submodule of submodule).
