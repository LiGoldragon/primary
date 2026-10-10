# ScopeOf Salvageability Assessment

Date: 2026-08-01

Bead: `primary-36y`

## Decision boundary

This report is the first deliverable of the overnight work order. It assesses
what can survive into the contract-first ScopeOf vertical slice. It does not
authorize code, grammar, identity infrastructure, a Dotos rename, standards or
skill changes, recursion, or a commit.

The assessment observes these controlling rulings:

- Traits are the mandated first implementation pass: the specification is
  expressed in code before bodies are written.
- A generic parameter is a contract reference. There is no unconstrained type
  variable in the concept layer; a visible Rust generic name is an assembly
  projection.
- Rust tuples are forbidden except for the single-field newtype. Protos
  positional fields are a separate encoded-data concern.
- Transformations do not own textual names or allocate identities. Generated
  identity belongs at the translator and atomic-operation boundary.
- Transformation dependencies form a DAG. Evaluation is dependency ordered,
  affected work runs exactly once, cycles are typed errors, and there is no
  fixpoint iteration.
- Authored Ethos must not repeat anything the system can infer.
- A capsule is one compilation unit, analogous to one Rust crate, rather than
  one namespace or file.
- Root Scope `All` covers the whole tree.

The unruled recursion surface remains a hard stop. This assessment also
introduces no escape spelling, `syn`, `quote`, `prettyplease`, strings in a
transformation contract, allocator capability, slot/change-log mechanism, or
new parser branch.

## Provenance grades

| Grade | Meaning | Sources used here |
| --- | --- | --- |
| A | Direct psyche wording, a seated ruling, or an explicit supersession | `design/ProtosEngine/traitStandardAndSpiritRename-2026-08-01.md`; `design/ProtosEngine/genericParametersAreTraits-2026-08-01.md`; `design/ProtosEngine/dependencyDagLaw-2026-08-01.md`; `design/ProtosEngine/atomicOperationEditing-2026-08-01.md`; `design/ProtosEngine/ethosNonRepetitionLaw-2026-08-01.md`; `design/ProtosEngine/capsuleIsCompilationUnit-2026-08-01.md`; `design/ProtosEngine/sameFormAndFileKinds-2026-08-01.md`; `design/Nomos/allMatchesAllScopeOf-2026-07-31.md`; `design/Nomos/rustTuplesForbiddenLawScope-2026-07-30.md` |
| B | Agent synthesis that is consistent with Grade A but is not itself psyche authority | `handoffs/codex-overnight-2026-08-01.md`; `reports/DesignConsistencyAudit-2026-08-01.md`; `NON_IDEAL_AGENTS.md` where it applies the later handwritten-mirror ruling |
| C | Current implementation, architecture, tests, or repository history; evidence of behavior, not authority for intent | The pinned `raw-discovery`, `structural-codec`, `core-nomos`, `core-ethos`, and historical `signal-domain` sources named below |
| D | Unreviewed research, proposal, or inference; usable only as a visibly named assumption or question | `reports/protosVisionReacquisition/2-Research-psyche-vision-open-questions-and-proposals.md`; `reports/NomosLogosMirrorTypesResearch-2026-07-31.md`; `reports/OperationalEditingPriorArt-2026-08-01.md`; `reports/NomosAuthoredRulesDesign-2026-07-29.md` |
| X | Superseded or expressly unreliable for present design authority | `reports/NomosTrainAddendum-2026-07-30.md`; the six-slot canonical-root claims in `core-ethos`; the capsule-per-namespace section of `design/ProtosEngine/ProtosEngineDesign-2026-07-29.md` |

Grade C evidence may show a useful mechanism. It cannot settle an open
relation, root shape, trait owner, identity rule, or recursion design.

## Four salvage verdicts

| Surface | Verdict | Salvage seam | Excluded from the first slice |
| --- | --- | --- | --- |
| `raw-discovery` | **Salvage the live source-bounded architecture as-is; quarantine its compatibility path.** | Preserve the language-agnostic first pass, `BlockTree`, source bounds, outside-in boundary discovery, and the separation between raw discovery and expected-type decoding. These are consistent with shared machinery and do not claim declaration semantics or identity allocation. | Do not extend the old `Block`/`Document` compatibility recognizer. Do not promote `ForeignLanguage { name: String }` into a transformation contract. Atomic-operation editing makes raw text a bootstrap input, not the durable semantic model. |
| `structural-codec` seal-time disjointness | **Salvage the semantics as-is; perform only later mechanical law alignment.** | Preserve typed structural positions, ordered products and sequences, archive declarations that consume translator-issued identities, one conservative disjointness prover, typed refusal at seal time, and cycle errors. The prover establishes surface-form separability. | Do not make seal-time disjointness answer Scope containment, overlap, matching, transformation order, or identity. Remove its multi-value tuple residue only when a code slice owns that path; this report does not edit it. |
| `core-nomos::TemplateValue` | **Substantial rework; salvage validators and value-role structure only after re-derivation.** | Candidate salvage is limited to constructor validation, stable role lookup, value/archive validation, and non-recursive value representation where those survive a contract-first derivation. | `RecursiveInvoke` and the delegated-assent recursion policy are outside authority and behind the hard stop. Text scalars are not admissible in transformation logic. `TemplateLandingShape::Fixed` and the dynamic-substrate claim require re-derivation. The tuple-bearing descriptor collector violates Rust law. `TemplateValue` does not displace the sanctioned handwritten Nomos/Logos mirror bootstrap. |
| `core-ethos` six-slot root | **Reject the six-slot root semantically; salvage only the shared root-record mechanism and item vocabulary.** | Preserve the ability to decode a typed root record through the common structural codec and reuse useful `WholeEthos` item types. A new file kind must differ by its root type and, at most, a simple trait implementation. | `Imports/Input/Output/Types/Generics/Impls` as a universal canonical root, `SixSlot*` API names, the five empty authored slots, and any new per-kind parser branch. The first replacement shape is explicitly an assumption below. |

The pinned implementation evidence behind these verdicts is:

- `raw-discovery` at `7290f65b...`, especially `ARCHITECTURE.md`,
  `src/block_tree.rs`, and `src/recognizer.rs`.
- `structural-codec` at `f47fac13...`, especially `ARCHITECTURE.md`,
  `src/table.rs`, `src/disjoint.rs`, and `src/error.rs`.
- `core-nomos` at `58fd8036...`, especially
  `src/template_language.rs` and `src/native.rs`.
- `core-ethos` at `736460fd...`, especially `src/whole.rs` and
  `tests/whole_six_slot.rs`.

## Contract-first ScopeOf thought object

The signatures below are a concrete review object, not a settled public API.
They contain no bare generic variable, tuple, string, allocator, generated
name, or identity slot. Associated types are constrained by named contracts;
Rust's visible `Self` projections are assembly for those concept-layer
contracts.

```rust
pub trait DomainTreeContract: Sized {
    type ScopeTree: ScopeTreeContract<DomainTree = Self>;
}

pub trait ScopeTreeContract: Sized {
    type DomainTree: DomainTreeContract<ScopeTree = Self>;
}

pub trait ScopeOf: DomainTreeContract {
    fn scope_of(&self) -> Self::ScopeTree;
}

pub trait ScopeContainment: ScopeTreeContract {
    fn contains_scope(&self, candidate: &Self) -> bool;
}

pub trait ScopeOverlap: ScopeTreeContract {
    fn overlaps_scope(&self, other: &Self) -> bool;
}

pub trait ScopeFiltering: ScopeTreeContract {
    fn matches_scope(&self, candidate: &Self) -> bool;
}

pub trait ScopeDomainMatching: ScopeTreeContract {
    fn matches_domain(&self, domain: &Self::DomainTree) -> bool;
}
```

`scope_of` describes a semantic projection of an already materialized Domain
value. Returning a value does not authorize creation of a generated true name,
visible name, stable identity, slot, operation, or change-log entry. A later
generated declaration must receive identity through the translator and atomic
operation boundary after that design is ruled and implemented elsewhere.

## Complete assumption register

Every unruled choice used by the thought object or the truth tables is named
here so it can be accepted, replaced, or removed independently.

- **[assumption A1 — contract decomposition and names]** `ScopeOf`,
  containment, overlap, filtering, and scope-domain matching are distinct
  contracts with the provisional method names shown above. The psyche has not
  ruled this API decomposition or spelling.
- **[assumption A2 — trait ownership]** For the first witness, the crate that
  owns the handwritten Domain/Scope mirror pair also owns these traits locally.
  Neither `core-nomos` nor historical `signal-domain` is declared the universal
  owner. Extraction to a shared owner waits for a second concrete consumer or a
  psyche ruling.
- **[assumption A3 — coherent relation operands]** Scope-to-scope relations
  compare values of the same contracted Scope family. Cross-family comparison
  is omitted until a named conversion contract exists.
- **[assumption A4 — total structural projection]** `scope_of` is total and
  structure-preserving for the first Domain/Scope pair; Domain `All` maps to
  Scope `All`. Failure and partial-projection behavior remain open beyond that
  witness.
- **[assumption A5 — API attachment of root All]** The ruled whole-tree meaning
  of root Scope `All` attaches to these proposed methods as
  `contains_scope(All, X)`, `overlaps_scope(All, X)`,
  `matches_scope(All, X)`, and `matches_domain(All, X)` being true.
- **[assumption A6 — containment against All]** A non-`All` scope does not
  contain root Scope `All`.
- **[assumption A7 — containment reflexivity]** Every materialized scope
  contains itself.
- **[assumption A8 — ancestor containment]** An ancestor scope contains a
  descendant scope.
- **[assumption A9 — reverse containment]** A strict descendant does not
  contain its ancestor.
- **[assumption A10 — unrelated containment]** Unrelated sibling scopes do not
  contain one another.
- **[assumption A11 — overlap symmetry]** Overlap is symmetric and true exactly
  when either operand contains the other. This makes ancestor/descendant
  overlap true in both argument orders and unrelated sibling overlap false.
- **[assumption A12 — filtering direction]** `matches_scope(filter, candidate)`
  uses the directional containment table, while remaining a distinct contract
  from containment so later filter semantics can diverge without changing
  overlap.
- **[assumption A13 — exact scope-domain match]** A scope and domain at the same
  structural location match.
- **[assumption A14 — ancestor scope-domain match]** An ancestor scope matches a
  descendant domain.
- **[assumption A15 — reverse scope-domain match]** A strict descendant scope
  does not match an ancestor domain.
- **[assumption A16 — unrelated scope-domain match]** An unrelated scope and
  domain do not match.
- **[assumption A17 — domain-side All]** Any materialized scope matches Domain
  `All`. This preserves historical `signal-domain` behavior but has no psyche
  ruling.
- **[assumption A18 — nested All]** If a nested Scope `All` is representable, it
  covers that scope's local subtree rather than the entire root tree. Whether a
  nested `All` should be representable is itself unruled.
- **[assumption A19 — minimal Ethos witness root]** The first replacement for
  the dead six-slot root is a types-only root decoded through the same
  structural machinery. Its exact record shape and delimiters remain open.

### Containment matrix

| Container | Candidate | Proposed result | Assumption |
| --- | --- | --- | --- |
| root `All` | any scope, including `All` | true | A5, with `All/All` also consistent with A7 |
| non-`All` | root `All` | false | A6 |
| scope X | the same X | true | A7 |
| ancestor | strict descendant | true | A8 |
| strict descendant | ancestor | false | A9 |
| one sibling | unrelated sibling | false | A10 |

### Overlap and filtering matrices

| Relation | Left/filter | Right/candidate | Proposed result | Assumption |
| --- | --- | --- | --- | --- |
| overlap | root `All` | any scope | true | A5, A11 |
| overlap | any scope | root `All` | true | A11 |
| overlap | scope X | the same X | true | A7, A11 |
| overlap | ancestor | strict descendant | true | A8, A11 |
| overlap | strict descendant | ancestor | true | A8, A11 |
| overlap | one sibling | unrelated sibling | false | A10, A11 |
| filter | root `All` | any scope | true | A5, A12 |
| filter | non-`All` | root `All` | false | A6, A12 |
| filter | scope X | the same X | true | A7, A12 |
| filter | ancestor | strict descendant | true | A8, A12 |
| filter | strict descendant | ancestor | false | A9, A12 |
| filter | one sibling | unrelated sibling | false | A10, A12 |

### Scope-domain matrix

| Scope | Domain | Proposed result | Assumption |
| --- | --- | --- | --- |
| root Scope `All` | any domain, including Domain `All` | true | A5 |
| non-`All` scope | Domain `All` | true | A17 |
| scope X | domain at the same location X | true | A13 |
| ancestor scope | strict descendant domain | true | A14 |
| strict descendant scope | ancestor domain | false | A15 |
| one branch's scope | unrelated branch's domain | false | A16 |

These tables exhaust the relation cells identified as open in
`reports/protosVisionReacquisition/2-Research-psyche-vision-open-questions-and-proposals.md` and make the otherwise implicit reverse-direction and
same-value cells visible. Historical `signal-domain` methods and tests are only
Grade C evidence for A17; they do not elevate it to a ruling.

## Unresolved contradiction and stop point

The pinned `core-nomos` implementation already exposes `RecursiveInvoke` and a
delegated-assent recursion policy, and the current protos-engine history carries
a recursive-daemon witness. The controlling overnight instruction says the
po2.19 recursion surface is unruled and must not be built. This report resolves
the execution boundary, not the repository contradiction: the first ScopeOf
slice must neither call, extend, normalize, nor bless those recursive surfaces.
Disposition of the pre-existing code requires a separate ruling or dispatch.

A second adaptation tension remains visible: the current `TemplateValue`
direction was built as a dynamic substrate, while the later ruling sanctions
handwritten Nomos/Logos mirror pairs until self-hosting. The safe seam is to
treat validators as candidates and re-derive the representation behind the
named contracts; this report does not decide whether `TemplateValue` ultimately
survives.

The next code slice may begin only with the trait declarations and an explicit
choice on A1 through A4 and A2 in particular. No method body should precede
that contract review.
