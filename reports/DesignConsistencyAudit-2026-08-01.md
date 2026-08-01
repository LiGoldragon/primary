# Design Consistency Audit — 2026-08-01

Commissioned by the psyche: "do a deep audit of the design for consistency.
find anything inelegant and/or inconsistent with the simplicity and
correctness-first approach of my philosophy, and syntax ugliness."

Three parallel read-critical audits: the design-ruling corpus, every syntax
surface, and the implementation's design-visible shapes. This report is the
ranked synthesis. Grades: findings are [agent-inference] evidence for psyche
review; psyche quotes inside are as recorded in their sources.

## Verdict in one paragraph

The design center is sound and demonstrably working: structural-codec is
fully language-agnostic with zero ruling violations; Ethos, Nomos, and Logos
already round-trip through the one shared mechanism; production
transformation paths are string-free with the translator monopoly intact;
and the architecture documents are honest about every legacy path. The
problems cluster in a small number of identifiable choke points — most
already quarantined — plus one systemic weakness that is not in the code at
all: the design record itself carries stale, unsuperseded authority.

## 1. Supersession debt in the record (top correctness risk)

The corpus audit's core finding: psyche reversals happen faster than the
record flags them, so agents can read stale authority as current.

- Capsule: the 07-23 "a capsule per namespace mirrors the file concept"
  stood unsuperseded in the protos-engine compilation
  (`ProtosEngineDesign-2026-07-29.md:423`) until the psyche's 2026-08-01
  ruling; now seated (`capsuleIsCompilationUnit-2026-08-01.md`) —
  RESOLVED during this audit.
- Six-slot model: `reports/EthosPositionalGrammar-2026-07-31.md` still
  presents the six-slot document as current fact after the psyche dismissed
  it as "an old design"; no supersession banner.
- Imports: older entries assume authored import root-sections; the 08-01
  ruling makes imports derived views; no supersession notes.
- NomosTrainAddendum: Decisions 1 and 3 were reversed by psyche rulings;
  the addendum document carries no note. Five of nine overnight leans
  (4: alias law, 5: syn/quote scope, 6: StoreSchema naming, 7:
  cross-package Invoke, 9: sema-engine "macro" wording) remain
  [not-understood-by-psyche] and unconfirmed, yet cited as operative.
- Template(X): approved at delegated-assent expressly FOR joint review of
  resulting code; the bead (po2.14) was closed "wired" and the review never
  happened.
- Minor: the Dotos entry does not name the 07-27 "nota is fine" ruling it
  supersedes; "intent" heading styling in the compilation section 7 was
  agent framing even before the spirit rename.

## 2. Root-record residue: SixSlot naming, projection indices (refined)

Refined verdict after a follow-up sweep: all three languages parse through
the one shared `structural_codec::StructuralEvaluator`, and each defining
its own typed root record via the generic OrderedProduct/Position/FieldRole
vocabulary is the CORRECT pattern under the file-kinds ruling — per-kind
roots, one machinery. What remains non-compliant or fragile:

- The `SixSlot` prefix hardcoded into 10+ public type names in core-ethos
  (`SixSlotDocumentRecord`, `SixSlotEthosCodec`, `SixSlotSourceBounds`, …)
  bakes the current slot count of a psyche-dismissed layout into the API
  surface, and leaks into language-engine-witness acceptance tests and a
  structural-codec test fixture.
- Hardcoded projection indices in `core-nomos/src/native.rs`
  (project_newtype :2069, project_enumeration :2089, project_visibility
  :2141) — per-kind, per-slot destructuring in the production evaluator,
  flagged "temporary po2.6, po2.8 owns retiring."
- The Nomos document root (`core-nomos/src/textual.rs:935-1021`, six roles:
  Revision/Inputs/Outputs/Transformers/Selection/Capsule) is a legitimate
  separate root by the ruling, but its shape predates the re-explanation
  and inherits the dead layout's assumptions (a revision slot the syntax
  audit flags as boilerplate); it should be re-derived, not trusted.
- Root definitions are hand-authored Rust structure rather than data; under
  the file-kinds ruling's cost model (new kind = new type + a simple trait
  impl) that may be acceptable, but the aspiration that a new form be
  "declarative data interpreted by one evaluator" argues for root records
  as data eventually.

## 3. Dotos is the fourth-language gap (common-mechanism ruling)

NOTA/Dotos does not round-trip through the shared structural-codec
mechanism: raw-discovery still carries the older span-free Block/Document
recognizer path for NOTA compatibility (acknowledged in its ARCHITECTURE).
Three of four languages are on the shared mechanism; the foundational data
language is the one still off it.

## 4. The syntax choke point: Rust vocabulary in authored Nomos

Nearly ALL authored-surface ugliness concentrates in two templates —
WireAttributes and EnumerationAttributes (`core-nomos/tests/textual_nomos.rs:44-58`):

```text
rustfmt.skip                                            Rust tooling name
(|nota-text|).[nota.NotaDecode nota.NotaDecodeTraced nota.NotaEncode]
[rkyv.Archive rkyv.Serialize rkyv.Deserialize Clone Debug PartialEq Eq]
```

Every atom is a Rust implementation identifier riding in the transformation
layer — contradicting the psyche's "composing a wire object implies the
rkyv serialization and all of these things automatically." The two
templates are 13 atoms of character-identical content differing by one atom
(`Copy`) — a reuse-equals-correctness smell that composition would cure.
Fixing this one choke point would make the authored surface entirely free
of Rust vocabulary.

Other syntax findings, ranked: five-of-six empty slots (`{} [] [] {…} {} {}`)
as boilerplate of the dead root — violates "only write the bits that
change"; the `Public` literal opening every structural template (the psyche
already challenged fixed visibility — either it is a default and is noise,
or it is variable and should be an escape); dual escape spellings
($ / $@ vs Realize / Splice / Invoke) still unreconciled, with the
two-textualforms reading graded agent-inference only; enum delimiters
`X.{…}` vs `X.[…]` both accepted with no governing rule; `Named` transformer
kind one atom deep while `Structural.Newtype` / `Recursive.Enumeration` are
two; `Map.(A B)` parenthesized application surviving in fixtures although
the current codec has no parenthesis trigger.

Confirmed beauty worth preserving: `DomainScope.ScopeOf.Domain` (three
atoms replacing ~2,300 lines of generated Rust); the type-declaration forms
(`Identifiers.Vector.Integer`, `Domain.[Technology.Software]`,
`Entry.{ Topic Kind Description Magnitude }`); escapes as ordinary dotted
application with no special glyphs (satisfying no-grammar-keywords); and
declaration-vs-reference decided purely by position (test-proven).

## 5. Impls-under-traits baseline (the new standard's starting line)

Aggregate ~169 inherent vs ~76 trait impls (~69% inherent). Worst:
raw-discovery 46:7 (boundary.rs 9:0, profile.rs 12:2); core-ethos and
core-logos define ZERO public traits; core-nomos 60:28
(template_language.rs 15:1). Model citizen: protos (12 trait : 4 inherent,
sealed CapsuleKind is the cleanest contract in the codebase). This is the
measured baseline the traits-first standard now works against.

## 6. Tuple register: unchanged, no new violations

All 27 multi-field tuple structs from
`RustTupleViolationsRegister-2026-07-30.md` remain; none added since. Worst
live cases: `SixSlotSourceBounds` (6 fields), `AuthoredTransformerDeclaration`
(6), `PlannedNomosPopulation` (5, production manifest loader, `.0`-`.4`
access throughout), and the misnamed 4-field `WholeEthosNewtype` /
`WholeLogosNewtype`. Register's remediation sequencing still correct.

## 7. Smaller findings

- `ForeignLanguage { name: String }` (raw-discovery/src/recognizer.rs:133)
  — string-typed language identity below the transformation layer; likely
  out of the no-strings law's scope but inconsistent with identity
  philosophy.
- `NameTreeProjectionEntry` carries a `Name` spelling in production
  sealed.rs — legitimate naming-boundary projection, noted for awareness.
- `NativeSchema` validation machinery in native.rs uses "schema" ~15 times
  for shape-validation in the general sense — domain-appropriate but
  avoidably confusing where "schema" is Ethos's old name; also hand-rolled
  validation that might be expressible as structural-codec declarations.
- `Identifier::Schema(u16)` namespace variant and the frozen
  `"core-schema 2026..."` hash-domain string ride the rename train (the
  latter cannot change without a deliberate layout bump).
- Legacy mass (~3,400 lines in core-nomos: engine.rs, name_boundary.rs,
  generation.rs, prelude.rs, fixtures.rs) violates rulings 5/6/7 but is
  genuinely quarantined — the native evaluator imports none of it; its
  correctness payoff is the regression oracle.
- structural-codec carries substantial String machinery at the
  textual-form boundary (14 sites: `ScalarValue::Text`, `TextChunk`,
  `structural_stops: &[String]` with `starts_with` comparison over source
  text, rendered output). This is source-text handling, not identity-path
  string use — no ruling violated — but the codec's ARCHITECTURE does not
  acknowledge this string surface.
- `GlyphSet::NomosExtended` (raw-discovery/src/profile.rs:43) puts a
  language name in the nominally language-agnostic discovery crate — a
  per-language parameter, not a separate path, but the crate's "depends on
  no encoded language model" claim overstates slightly.

## Proposed actions (for psyche disposition, none taken)

1. Supersession-flagging pass: append notes/banners to the stale documents
   (addendum reversals, six-slot grammar report, compilation capsule and
   imports sections) — mechanical, one write agent.
2. A short ruling session to confirm or void the five unconfirmed overnight
   leans (4, 5, 6, 7, 9).
3. Fold the second six-slot root and projection-index retirement into the
   Codex implementer's adaptation train (extends existing po2.8 intent).
4. Design the "wire type implies its apparatus" abstraction to purge Rust
   vocabulary from the two attribute templates (candidate next worked
   aspect after generated-output identity).
5. Slate Dotos onto the shared round-trip mechanism with the rename train.
6. Schedule the Template(X) joint review the delegated-assent grade
   promised.
