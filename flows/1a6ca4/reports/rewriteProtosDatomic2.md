# Rewrite: protos 0.18.0 and datomic 0.12.0 (second pass)

## Audit items

| # | Audit item | Status |
|---|---|---|
| 1 | Non-structural faults are never situated | Closed -- datom root conceived at path [0] matching delineation; all containers (Vec, Option, Result, Box, struct fields) prepend child index via Prepending; Protosizable for Datom computes situation by textualize-then-delineate round-trip |
| 2 | Untrusted text can abort the process | Closed -- delineator uses an explicit stack bounded by DEPTH_LIMIT (100,000); bare run parsing is iterative (find split points, build chain from right to left); textualize is iterative for Headed chains; Delineation Drop is iterative |
| 3 | Inner structural faults swallowed into Unclosed | Closed -- MissingBody and MissingHead removed entirely; a bare run whose separators do not split stays a Bare structure; the innermost delimiter fault is reported at its actual extent |
| 4 | Layer table not borne as vision states | Closed -- Datom bears protos::Textualizable and protos::Protosizable concretely; the Datomic kind provides the chain (conceive, protosize, textualize) through its default textualize method |
| 5 | Reader not under trait ontology | Closed -- no free functions, no inherent impls in either crate; glyph characters live once in Glyphing/Delimiting trait implementations; classification walks the enum variant by variant via Identifying/Recognizing; protos flake carries no-free-functions, no-inherent-methods, no-forbidden-vocabulary checks |
| 6 | Parenthesis escaping does not round-trip | Closed -- textualize escapes all three characters (opening paren, closing paren, backslash) unconditionally; delineator unescapes only those three; property-tested over random ASCII strings; curly quote U+201D unrepresentable in curly-quoted content (typed decision: no escape exists; the one glyph a curly-quoted string cannot carry) |
| 7 | .ethos files break Declaration | Closed -- rewritten: types file and kinds file per crate, variant-headed, no version, imports first, kinds in the kinds file, associations third in types file |
| 8 | cargo fmt --check fails | Closed -- both crates formatted, fmt check passes |
| 9 | Stale documents and tracked build artifact | Closed -- ARCHITECTURE.md, AGENTS.md, NON_IDEAL_AGENTS.md, UPGRADES.md deleted from both crates; README.md rewritten in new vocabulary; flake descriptions corrected; result symlink removed and added to .gitignore |
| 10 | Scores example not in tests | Closed -- Person struct with Vec<i64> scores round-trips typed; Observed.Locks.[] and Success round-trip through typed enum (Response) |
| 11 | Ascent computes no spans | Closed -- Protosizable for Datom textualizes the protoform tree and re-delineates to fill the situation map; situate on the resulting delineation yields the correct extents |
| 12 | Two representations of variant carrying nothing | Closed -- Datom::Variant(Head, Box<Datom>) always carries a body; a variant carrying nothing is Datom::Bare, the position decides at incorporate time |
| 13 | Hand-written derives and triplicate impls | Closed -- all types derive Clone, Debug, PartialEq, Eq; impl_datomic_scalar! macro generates Conceivable, Datomic, and Incorporable from two closures; no triplicate blocks |

## Passes

### protos

| Pass | Kind | Borne by | Yields | Faults |
|---|---|---|---|---|
| Delineation | Protosizable | Text | Result<Delineation, Fault> | Unclosed, UnclosedBoundary, Unopened |
| Textualization | Textualizable | Head, Protoform, Delineation | Text | (cannot fault) |
| Actualization | Actualizable<T> | Potential<T, C> | Result<T, Situated<Fault>> | Structural, Conceptual, Corporate (from C) |
| Situation lookup | Situating | Delineation | Option<Extent> | (cannot fault) |

### datomic

| Pass | Kind | Borne by | Yields | Faults |
|---|---|---|---|---|
| Protosizing | Protosizable | Datom | Result<Delineation, Infallible> | (cannot fault) |
| Textualization | Textualizable | Datom | Text | (cannot fault) |
| Conception | Conceivable<Datom> | Protoform, Delineation | Result<Datom, Fault> | Conceptual(path, problem) |
| Incorporation | Incorporable<T> (via Datomic) | Datom | Result<T, Fault> | Corporate(path, problem) |

## New anatomy

### protos 0.18.0

| Module | Layer or kind | What it holds |
|---|---|---|
| lib.rs | Ontology | Type definitions, kind (trait) definitions, Glyphing/Delimiting/Identifying/Recognizing impls, Potential/Situated impls, iterative Drop for Delineation |
| delineation.rs | Text to Protoform | BareRunParser (iterative), BodyAttacher (iterative), Delineator (stack-based), Frame, Pending, Protosizable for Text and Potential |
| textualization.rs | Protoform to Text | Escaping for parentheses, Spacing for enclosures, LeafTextualizing, Textualizable for Head/Protoform/Delineation |
| actualization.rs | Chain | Actualizable for Potential, Situating for Delineation |

### datomic 0.12.0

| Section | Layer or kind | What it holds |
|---|---|---|
| Datom and faults | Concept | Datom (6 variants), Meaning, Expected, Problem, Fault, Prepending |
| Protosizing | Concept to Protoform | Protosizing trait, Protosizable and Textualizable for Datom (situation computed by round-trip) |
| Conceiving | Protoform to Concept | Conceiving trait, Conceivable<Datom> for Protoform and Delineation; non-dot separators produce Bare |
| Datomic kind | Corporate | Datomic trait with incorporate_from and textualize |
| Scalars | Corporate | impl_datomic_scalar! macro, impls for Integer, Boolean, Decimal, Text, Meaning |
| Containers | Corporate | Vec<T>, Option<T>, Result<T,E> with path prepending |
| Fault types | Self-describing | Expected, Problem, Fault, Separator, Enclosure, Boundary, Extent, protos::Problem, protos::Fault |
| Identity and Box | Bridging | Datom identity, blanket Incorporable<Box<T>>, impl_datomic_box! macro, Situated<F> |

## Public API changes since 0.17.0/0.11.0

### protos 0.17.1 to 0.18.0

- **Removed**: Problem::MissingBody, Problem::MissingHead
- **Added**: pub trait Glyphing, Delimiting, Identifying, Recognizing, Texted, LeafTextualizing (private)
- **Added**: impl Drop for Delineation (iterative)
- **Changed**: Potential no longer has Protosizable for Potential<(), C>; now Protosizable for Potential<T, C>
- **Changed**: all Debug/PartialEq/Eq derived instead of hand-written (Debug output format may differ)
- **Removed**: Pathed trait (kept, unchanged)
- **Changed**: Textualizable for Protoform now iterative (same output, no stack overflow)
- **Changed**: parenthesis escape now unconditional (canonical form escapes all parens/backslashes)
- **Changed**: delineation module is new (stack-based), textualization and actualization are new modules

### datomic 0.11.1 to 0.12.0

- **Changed**: Datom::Variant(Symbol, Separator, Option<Box<Datom>>) to Datom::Variant(Head, Box<Datom>)
- **Changed**: all Debug/PartialEq/Eq derived
- **Added**: pub trait Prepending { fn prepend(self, index: Integer) -> Self }
- **Added**: impl Textualizable for Datom (protos::Textualizable, concrete)
- **Changed**: Protosizable for Datom now computes situation (was empty)
- **Changed**: non-dot separator headed protoforms conceive as Bare (text content) instead of Variant
- **Changed**: all struct incorporations prepend child field index to fault path
- **Changed**: Option/Result incorporate prepend 0 to body fault path
- **Removed**: Datom::Variant no longer carries Separator or Option
- **Removed**: private Glyphing duplicate (uses protos::Glyphing)
- **Added**: impl_datomic_scalar! macro replaces triplicate impl blocks
- **Removed**: result symlink from tracking

## Decisions on flow authority

- **Angles tight, braces/brackets spaced** -- recorded as a flow decision; follows Vision/ethos.md examples
- **Parentheses: backslash escapes for (, ), \ only; all three escaped unconditionally on print** -- ensures any content round-trips; the stale skill's balance-based escaping replaced
- **Curly quotes: no escape; U+201D unrepresentable** -- typed decision visible in code and this report; the one glyph a curly-quoted string cannot carry
- **-0 rejected as integer** -- carried from previous pass; Vision/datom.md says "no leading zero except 0 itself"
- **Decimal: point mandatory, digits on both sides, no exponent, no leading zero except 0., shortest round-trip print** -- flow decision; canonical form trims trailing zeros but keeps at least x.0
- **Non-dot separator in datom produces Bare, not Variant** -- a colon or exclamation headed protoform is text content at the concept level; the dialect decides by position at incorporate time
- **Datom::Variant always carries a body; dot implied** -- a variant carrying nothing is Datom::Bare; the incorporate step maps Bare to unit variant
- **MissingBody/MissingHead eliminated from protos** -- a bare run whose separators do not split stays Bare; the dialect decides what it means
- **Split rule: a separator splits when both neighbors are non-separator** -- adjacent separators (a..b, a.!b) and edge separators (a., .a) do not split
- **Situation computed on ascent by textualize-then-delineate** -- the round-trip through text ensures paths agree; cost is a full re-parse, justified by the vision's multi-pass principle

## Commits and versions

| Crate | Old version | New version | Commit (main) |
|---|---|---|---|
| protos | 0.17.1 | 0.18.0 | 3b29b61e431b |
| datomic | 0.11.1 | 0.12.0 | 83d92f9d5047 |

datomic pins protos at 3b29b61e431b.

## Test, clippy, fmt, flake-check output

### protos

- `cargo test`: 47 passed, 0 failed (including proptest round-trips and deep nesting)
- `cargo clippy --all-targets -- -D warnings`: clean
- `cargo fmt --check`: clean
- `nix flake check`: passed (all checks: build, test, no-free-functions, no-inherent-methods, no-forbidden-vocabulary, doc, fmt, clippy)

### datomic

- `cargo test`: 29 passed, 0 failed
- `cargo clippy --all-targets -- -D warnings`: clean
- `cargo fmt --check`: clean
- `nix flake check`: passed (all checks: build, test, no-free-functions, no-inherent-methods, no-zst-behavior, no-forbidden-vocabulary, doc, fmt, clippy)

## Left hanging

- **Delineation Drop is iterative but standalone Protoform Drop is not** -- a deeply nested Protoform created outside a Delineation could stack-overflow on drop; the parser always produces Delineations, so this affects only programmatic construction of extreme chains
- **Consumer crates not updated** -- protos and datomic pin exact revisions; consumers (ethos-zero, orchestrate) need re-pinning
- **Potential<T, C> still requires two type parameters** -- the orphan rule prevents a one-parameter blanket in protos; C is the concept type for the actualize chain

## Sources

- /home/li/primary/Vision/protos.md, Vision/datom.md, Vision/ethos.md
- /home/li/primary/Intent/mandatoryTraits.md, Intent/protosParsing.md, Intent/data.md
- /home/li/primary/flows/995a164e/vision/{rust,layerMatching,kinds,concept,contexts,explodedForm}.md
- /home/li/primary/flows/1a6ca4/reports/auditProtosDatomic.md -- the acceptance list
- /home/li/primary/flows/1a6ca4/reports/rewriteProtosDatomic.md -- the first pass's account
- /git/github.com/LiGoldragon/protos @ 3b29b61e431b: all source files
- /git/github.com/LiGoldragon/datomic @ 83d92f9d5047: all source files
