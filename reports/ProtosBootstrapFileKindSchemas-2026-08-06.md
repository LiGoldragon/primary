# Protos Bootstrap File-Kind Schemas

Date: 2026-08-06

Status: shipped provisional bootstrap contract and psyche-review target.
`primary-5pm` tracks the deferred ruling. This report replaces
`reports/ProtosFileKindSchemas-2026-08-05.md` as the description of the model
actually published; it does not raise any provisional choice to psyche-ruled
seniority.

The governing law is direct: “Beauty and elegant, extendable logic always wins
over everything, always. Beauty rules this universe.” Convenience, familiarity,
and token cost do not outrank it.

## 1. Scope and seniority

The bootstrap stage is interfaces-first. Authors describe component interfaces
in Ethos while executable behavior remains handwritten Rust. The three roots in
this report are therefore the current bootstrap entry points, not a universal
taxonomy of programs.

This report does not design behavior, effects, resources, concurrency, runtime
world anatomy, or general Dotos data anatomy. Their absence is staging, not an
invitation to add placeholder positions. The wider outcomes described by the
psyche—general adoption and the self-hosting cascade through Rust, LLVM, Mentci,
and the operating system—constrain these choices not to make a present substrate
permanent. Outcomes expected to happen are not relabelled here as intent or
vision.

Authority marks used below:

| Mark | Seniority |
|:--|:--|
| **[R]** | Direct psyche ruling or explicitly psyche-approved proposal. |
| **[D]** | Delegated bootstrap implementation choice. |
| **[P]** | Shipped provisional file-kind choice awaiting `primary-5pm`. |
| **[E]** | Exact observed behavior of the published implementation; evidence, not a language ruling. |

The implementation basis inspected for this reconciliation is:

| Published component | Revision | Relevant boundary |
|:--|:--|:--|
| `core-ethos` | `7a1384874f3747de97c6ccbb4ae6fa2149b27330` | root model, strict reader, canonical writer, archive status |
| `sema-translator` | `4675e5ddfdd0d24144498ec9b7d2e5b9cb422249` | production naming-authority assembly |
| `core-nomos` | `4758e8db3c72e7c84c30c1a0b597b6d9ed65d35d` | authority-sealed Interface/Nexus and Sema lowering |
| `schema-rust` | `c1d2ae1b0dd189cd8c8788a2cfc062e26c0377f3` | strict Interface and Sema generation and checked-artifact proofs |

`schema-rust` pins that exact producer train. Every model statement below is
about these published revisions.

## 2. Canonical envelope

Every file has exactly three source positions: header, import vector, and one
kind-selected body **[R/P]**.

```ethos
Kind.{Major Minor Patch}
[module:path.[Name OtherName]]
{
  [first kind-specific section]
  [later kind-specific section]
}
```

### 2.1 Header

The header is the visible projection of one of the three registered bootstrap
kind identities followed by exactly three canonical nonnegative decimal
components **[P/E]**:

```ethos
Interface.{1 0 0}
Nexus.{1 0 0}
Sema.{1 0 0}
```

The published catalog admits exactly version `1.0.0`. A different version is a
typed refusal, as are a missing component, an extra component, a sign, and a
noncanonical decimal such as `01`. The decoded header is retained compatibility
metadata and must agree with the selected semantic body. The three-root carrier
used by the bootstrap implementation is explicitly not an ontology claim.

### 2.2 Imports

Imports use the ruled square selector vector **[R]**. The outer vector may be
empty. Each entry has a nonempty colon-separated module path and a nonempty
vector of ownerless visible names **[P/E]**:

```ethos
[]
[dependency:domain.[External Identifier]]
```

Imports resolve textual projections to encoded identities. They remain in the
source-projection part of the decoded transaction so the canonical writer can
reproduce the file, but they are not positions in the kind-specific semantic
body **[D/E]**. Canonical emission groups selectors by module path, removes
duplicate selectors, and orders selected names by authority-owned identity
bytes. Missing, invalid, or ambiguous projections are refused.

Declarations in the current module are visible without a self-import when the
authority catalog seats their projection. Imported and current-module Shape
identities are usable when their catalog role and arity are valid; Shapes are
not restricted to the fixed bootstrap prior list.

## 3. Shared authored vocabulary

This section names the semantic alternatives accepted by the published reader.
It is not a transcription of its Rust carriers.

### 3.1 Plain nominal types

A plain type declaration has one of three authored bodies **[P/E]**:

```ethos
Identifier.Integer
Pair.{Left Right}
Choice.[None One.Left Both.{Left Right}]
```

- A bare payload is a newtype over one type expression.
- Braces are an ordered struct product.
- Squares are an enum; a variant is unit, unary, or a nonempty ordered product.

The recursive type-expression alternatives are:

- an encoded nominal reference projected as a bare visible name;
- a Shape application, written with bare angle brackets, such as
  `Vector<String>`;
- a Trait requirement, marked everywhere with guillemets, such as
  `«Sortable Serializable»` or the named binder `«Value.Sortable»` **[R]**.

Shape arity comes from the identity schema catalog. Product positions and Shape
argument positions retain semantic order. Named collections—declarations,
variants, traits, methods, Tables, and role entries—are canonically ordered by opaque
authority-owned identity bytes **[D/E]**.

### 3.2 Traits

A Trait contains zero or more methods. A method product contains zero or more
parameters followed by exactly one return type **[P/E]**:

```ethos
Transform.{apply.{Input Output}}
```

Trait requirement binders are local to the containing type or method. They are
not globally minted objects. Reusing one named binder with different
requirements, or repeating a Trait in one requirement, is refused.

### 3.3 The one admitted bootstrap Nomos form

The authored declaration

```ethos
Observer.Stream.(Query Event)
```

is the one closed, audited Nomos form admitted by this bootstrap **[P/E]**. It
means Stream initiation with exactly two ordered arguments, Query then Event.
It is accepted only in Interface support Types. This closed admission is a
bootstrap limit, not a claim about the eventual Nomos language.

## 4. Interface

Interface has exactly four authored sections, in this order **[P]**:

1. Input roles
2. Output roles
3. Refusal roles
4. support Types

```ethos
Interface.{1 0 0}
[]
{
  [Submit.Request]
  [Response]
  [Rejected.{String}]
  [Request.String Response.String Observer.Stream.(Request Response)]
}
```

Each entry in Input, Output, or Refusal is either:

- an inline plain nominal declaration, such as `Submit.Request`; or
- a reference to a visible nominal declaration, such as `Response`.

An inline declaration both declares the nominal and supplies the role target.
A reference supplies only the role target. A Stream initiation is never a role
entry; putting it directly in a role section is refused.

### 4.1 Memberships are derived, not authored

The sealed Interface meaning also carries one membership relation for every
authored role entry **[D/P]**:

| Authored section | Derived relation |
|:--|:--|
| Input entry targeting `T` | `Input → T` |
| Output entry targeting `T` | `Output → T` |
| Refusal entry targeting `T` | `Refusal → T` |

`memberships` is therefore not a fifth source section. It belongs to the
Interface root and does not mutate the target type. The writer validates it
against the three role sections and emits only those sections. Memberships are
canonically ordered first by the prior role identity and then by target identity.

### 4.2 Support Types and prepared Stream generation

The fourth section accepts plain nominal declarations and the single audited
Stream initiation form. For each authored `Name.Stream.(Query Event)`, the
authority must supply two additional already-minted identity seats. Sealing
prepares one atomic family **[D/P]**:

| Prepared declaration | Identity | Type/value relation | Interface role |
|:--|:--|:--|:--|
| initiation | authority-supplied generated identity | Query | Input |
| direct Stream output | the authored `Name` identity | `Stream<Event>` | Output |
| termination | authority-supplied generated identity | references the direct Stream output | Input |

These three generated role relations live with the prepared Stream generation,
not in the Interface body’s authored-role memberships. Generated declarations
are transaction output for an external atomic commit; the canonical writer does
not add them as source declarations.

## 5. Nexus

Nexus has exactly two authored sections, Traits first and supporting Types
second **[P]**:

```ethos
Nexus.{1 0 0}
[]
{
  [Sortable.{} Transform.{apply.{«Value.Sortable» «Value.Sortable»}}]
  [Pair.{«Left.Sortable» «Left.Sortable»}]
}
```

The first section contains Trait declarations. The second contains plain
nominal declarations used by signatures. Although Interface and Nexus share an
internal declaration carrier, the published Nexus root refuses Stream/Nomos
declarations **[E]**. Nexus has no role sections and no membership relations.

Traits-first is the shipped order. The types-first order described by the old
report is obsolete.

## 6. Sema

Sema has exactly two authored sections, persistent record Types followed by
keyed Tables **[P]**:

```ethos
Sema.{1 0 0}
[dependency:domain.[External]]
{
  [Identifier.Integer Stored.{Identifier External}]
  [stored.{Stored Identifier}]
}
```

The first section admits only plain nominal types—newtypes, structs, and enums—
and registers them as persistent nominals. It does not admit Stream or any
other Nomos declaration **[P/E]**.

Each Table entry is exactly:

```ethos
TableName.{RecordType KeyType}
```

Both leaves are visible references with the persistent-nominal schema role.
The reader establishes that schema relation. The current storage-aware Nomos
lowering then imposes the narrower generation contract: both record and key
must be declared by this exact Sema document, and the key must be a newtype.
That distinction matters: the source model and the currently implemented Rust
generation subset are not the same claim.

## 7. Identity and authority transaction

Encoded identity is never inferred from source spelling or declaration content
in this lane **[R/E]**. The reader also never mints an identity and never commits
authority state. The production path is:

1. `core-ethos` plans structure and enumerates every declaration occurrence,
   its visible spelling, source bound, lexical scope, and semantic purpose.
2. The configured authority supplies an approved after-snapshot of textual
   metadata, canonical bytes for exactly the already-minted new identities, and
   the two generated seats for every authored Stream.
3. `sema-translator` matches each occurrence to an exact projection in that
   snapshot. Each seat is classified as `Existing` or `New`; a `New` seat
   carries its authority-owned canonical bytes.
4. `core-ethos` seals the source with the exact assignments, generated Stream
   assignments, before-to-after metadata transition, schema additions, and
   canonical identity order.
5. The naming authority issues a receipt bound to the complete prepared draft,
   its durable authority identity, and its monotonic revision. The resulting
   transaction remains branded by that authority type.
6. Every writer, Nomos lowerer, and generator revalidates the receipt and all
   prepared-model invariants before use.

The authority approval must be exact. Missing and unused seats are refusals;
`Existing` must already exist; `New` must not; canonical bytes must be nonempty
and unique; the metadata transition’s before snapshot must equal the reader’s
catalog; and its after snapshot may not smuggle unrelated identities.

The prepared transaction contains the decoded semantic body, retained source
imports, generated Stream families, identity-schema additions, the verified
metadata transition and dispositions, the receipt, and the complete canonical
order **[D/E]**. It is a proposal for an external store to commit or reject
atomically. Preparing it is not persistence.

Visible name and module placement live in the authority’s textual metadata
snapshot, keyed by encoded identity **[R]**. The canonical writer resolves from
that same validated after-snapshot; it does not reverse-engineer spelling from
source content or from generated Rust.

## 8. Lowering and generation boundary

The shipped readers accept more truthful source meaning than the first lowering
slice can yet preserve. Unsupported meaning is refused, never erased **[E]**.

| Published lane | Exact accepted subset | Exact boundary |
|:--|:--|:--|
| `core-nomos` direct Slice One | role-free Interface Types; trait-free Nexus Types | Revalidates the matching authority transaction and lowers plain nominal types and Shapes to `WholeLogos`. Refuses Interface roles, Stream, Nexus Traits, Sema, Tables, and Trait requirements. |
| `core-nomos` Sema | one Sema transaction | Emits stored nominal Logos declarations before Tables. Requires document-local record/key types, a newtype key, and explicit owner-and-revision-bound storage provenance for every reachable nonlocal storage leaf. |
| `schema-rust` Interface | one verified Interface assembly within the direct Slice One subset | Requires caller-supplied sealed Rust vocabulary and explicit encoded-identity-to-Rust-path resolution. Emits paired canonical Ethos and Rust artifacts. It does not accept Nexus or Sema. |
| `schema-rust` Sema | one verified Sema assembly satisfying storage lowering | Requires the same explicit Rust projection inputs plus external storage provenance. Emits paired canonical Sema and Rust artifacts, including stored types and table specifications. |

There is no published `schema-rust` Nexus generator in this train. The direct
Nomos lowerer can lower a Nexus only when its Trait section is empty; it never
silently drops a Trait.

Both schema-rust lanes are deterministic for the same verified inputs. Their
freshness boundary checks canonical source and generated Rust together, or
updates both only under the explicit update environment variable. Generated
Rust uses stable encoded identities for object coordinates and explicit paths
for external Rust types; visible Ethos spellings are not treated as identity.

Rust is the current bootstrap projection, not a permanent substrate **[R]**.
The exact Rust-facing APIs above describe present staging only.

## 9. Typed refusals

The refusal surface is part of the shipped model, not incidental parser text.
The principal classes are:

| Boundary | Refuses |
|:--|:--|
| envelope and projection | unknown kind, unsupported or noncanonical version, wrong section arity, invalid module/name projection, empty import selectors, unresolved, ambiguous, invisible, or non-round-tripping references |
| catalog and schema | missing or duplicate identities, wrong or incompatible schema roles, invalid prior relationships, Shape/Nomos arity mismatch, and Nomos identities outside the one seated prior |
| declaration and scope | duplicate declarations or assignments, missing/extra assignments, identity collisions, incompatible Trait binders, repeated Trait requirements, Stream outside Interface Types, and non-plain Sema declarations |
| authority transaction | before-snapshot mismatch, missing/extra metadata, rejected proof or receipt, incorrect Existing/New disposition, missing/duplicate canonical bytes, and missing/extra generated Stream seats |
| direct Nomos lowering | any Interface membership, Stream declaration, Nexus Trait, Sema/Table in the type-only lane, Trait requirement, or invalid empty structural product/application |
| Sema lowering | wrong kind, duplicate local record, nonlocal table record/key, non-newtype key, absent/duplicate/conflicting external storage provenance, cyclic storage shape, Trait requirement, or unresolved storage parameter |
| Rust projection | wrong file kind, any propagated Nomos/storage refusal, unresolved explicit Rust type path, or invalid sealed Rust projection |
| checked-artifact boundary | stale canonical source or stale generated Rust |

Prepared transactions are validated again at every consuming boundary. A caller
cannot bypass these refusals by constructing a decoded body or a naming map and
passing it directly to Nomos or schema-rust.

## 10. Intentional `NotYetArchived` boundary

Both the published reader and every prepared bootstrap transaction report
exactly:

```text
NotYetArchived
```

This is deliberate **[D/E]**. Archiving the bootstrap transaction carrier is
deferred until the random EncodedName substrate is stable enough that an
archive layout will not freeze today’s encoded-name chain representation.
There is no fallback archive format and no claim of durable transaction replay
in this model.

`NotYetArchived` does not mean that Sema storage generation is absent. The Sema
lane separately derives storage fingerprints and generated Rust archive/table
support from explicit provenance. Nor are the paired canonical source/Rust
artifacts an archive of the prepared authority transaction. The persisted
restart finish line remains a downstream MVP acceptance proof, not something
this report manufactures from checked-in projections.

## 11. Deferred psyche review

`primary-5pm` should review this document, not the superseded 2026-08-05 report.
The provisional choices needing ruling are now visible without implementation
transcription:

- three bootstrap roots and their exact versioned envelope;
- Interface’s four authored sections, Declaration-or-Reference role entries,
  derived memberships, and prepared Stream lifecycle family;
- Nexus’s Traits-first ordering and current two-section division;
- Sema’s persistent Types followed by exact two-reference Tables;
- the current separation between source meaning, authority-sealed transaction,
  supported Nomos lowering, and Rust projection;
- the deliberate `NotYetArchived` boundary.

Until that ruling, these are the exact shipped provisional choices. A psyche
correction changes the readers and consumers; the existence of published code
does not convert a delegated choice into authority.
