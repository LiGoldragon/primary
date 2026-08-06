# Protos Bootstrap File-Kind Schemas

Date: 2026-08-06

Status: provisionally authorized for MVP implementation. Final psyche review is
deferred to `primary-5pm`. The choices marked **[MVP]** are the active bootstrap
contract until that review revises them. This document supersedes
`reports/ProtosFileKindSchemas-2026-08-05.md` only as the current implementation
proposal; it does not supersede any psyche ruling. The historical report remains
evidence of the earlier design pass.

Current vision:
`reports/deep-vision/protos-engine-renewed-vision-2026-08-06.md`.

## 1. The staged spine

Protos develops in stages. The current stage begins with component interfaces;
executable behavior remains handwritten Rust deliberately. These schemas must be
strict, beautiful, and extendable, but they must not pre-allocate positions for
runtime logic, effects, resources, concurrency, lifecycle machinery, or general
data anatomy.

The later complete executable representation belongs to `primary-w2q`. General
Ethos/Dotos data anatomy that is neither a component role nor persistent Sema
storage belongs to `primary-bfs`. Neither future is a gate on this proposal.

The current deliverable is exactly three bootstrap roots:

- Interface: public typed roles.
- Nexus: traits that handwritten behavior implements, plus signature-local types.
- Sema: persistent record types and keyed tables.

This is a bootstrap taxonomy, not a claim that all future programming reduces to
these three roots.

## 2. Authority legend

- **[R] Ruled**: directly stated by the psyche or an agent proposal explicitly
  confirmed by the psyche.
- **[D] Derived**: a mechanical consequence of ruled structure. It remains an
  agent interpretation and may be corrected.
- **[P] Proposed**: new design in this report, pending psyche ruling.
- **[MVP] Provisionally authorized**: the active implementation choice for the
  bootstrap reader. Final psyche review may revise it through `primary-5pm`, but
  that review is not a reader gate.
- **[O] Open**: no exact shape is proposed because authority or delegated design
  has not supplied enough information.

Schema field names below explain positional meaning. They are not authored field
labels. Canonical Dotos and Ethos values remain positional.

## 3. Shared envelope

### 3.1 Root schema

```text
EthosFile.{
  Header
  Imports
  Body
}

Header.{EthosKind EthosVersion}
EthosKind.[Interface Nexus Sema]

EthosVersion.{Major Minor Patch}

Imports.Vector<ImportEntry>
ImportEntry.{ModulePath ImportedNames}
ModulePath.{ModuleName Submodules}
Submodules.Vector<ModuleName>
ImportedNames.Vector<VisibleName>
```

Authority by position:

| Schema | Position | Meaning | Authority |
|:--|:--|:--|:--|
| `EthosFile` | 1 | header | **[R]** |
| `EthosFile` | 2 | imports | **[R]** |
| `EthosFile` | 3 | kind-specific body | **[R]** |
| `Header` | 1 | Ethos file kind | **[R]** |
| `Header` | 2 | Ethos compatibility version | **[R]** |
| `EthosVersion` | 1–3 | major, minor, patch | **[MVP]** |
| `ImportEntry` | 1 | module path | **[MVP]** |
| `ImportEntry` | 2 | nonempty imported-name vector | **[R/MVP]** |

The header is exactly kind and version for this stage **[R]**. The version denotes
the version of Ethos with which the content last worked and is writer-bumped when
a change may break compatibility **[R]**. It is not a file revision, component
release, database schema revision, or content identity **[D]**.

The active bootstrap projection is **[MVP]**:

```ethos
Interface.{1 0 0}
```

The first atom is exactly one `EthosKind`. The following brace product is exactly
three nonnegative base-ten integers in major, minor, patch order. Canonical decimal
has no sign and no leading zero except the value `0`. No fourth component, omitted
component, or prerelease/build suffix is accepted. The earlier `Interface.1`
spelling remains historical evidence rather than the MVP projection.

The header is retained in bootstrap source/document metadata for compatibility and
provenance **[MVP]**. It selects the body root and records the writer's compatibility
claim, but it is excluded from every declared semantic object's body and therefore
from every declared object's TrueName. Imports are different: after they resolve
textual references, they are discarded rather than retained in encoded document
metadata **[R/MVP]**.

The body type is selected after decoding `Header.EthosKind`. One shared context
machine then decodes that root. A discriminated Rust enum is a permissible
bootstrap implementation; it is not the language ontology.

### 3.2 Imports

Imports exist only in textual projection. They resolve visible names to encoded
identities and do not survive in encoded code **[R]**.

Ruled projection:

```ethos
interface.[Entry Referent RecordSet]
```

The square payload is ruled. The active singleton projection keeps that vector
form **[MVP]**:

```ethos
interface.[Entry]
```

Colon qualification and uniform module recursion yield this active nested
projection **[D/MVP]**:

```ethos
component:protocol:interface.[Entry Referent]
```

MVP import law:

1. The source is a nonempty path through the module tree. The first segment is
   the outermost module; every colon advances to a submodule.
2. The dot separates the module path from one nonempty square vector of names.
3. A singleton keeps its square vector. There is no second singleton grammar.
4. The path resolves within the source set's dependency closure through
   textual-form metadata. Ambiguous or absent paths are typed refusals.
5. Imports have no aliases in this bootstrap. Renaming and placement belong to
   textual-form metadata bound to encoded identity.
6. Body references use imported local names. Colon retains qualification meaning
   only in import context.

Only the colon, the square name vector, and recursive module terminology are
ruled. Absolute outermost-to-leaf path resolution, singleton uniformity, and the
lack of aliases are active **[MVP]** choices pending `primary-5pm`.

## 4. Atom roles and identity

The reader must never treat every atom as an undifferentiated string. Its expected
position assigns one of these roles:

| Atom role | Examples | Decode result |
|:--|:--|:--|
| fixed vocabulary | header kind; strict encoded variant selected by structure | a closed discriminant, never a user name |
| literal value | the three version integers | a validated typed scalar, never name resolution |
| declaration name | type, enum variant, trait, method, or table being introduced | consume the encoded-name assignment supplied by naming authority; record visible spelling and placement as textual metadata |
| reference | type, Shape, Trait, return, record, or key reference | resolve through local declarations and imports to an encoded name |
| local binder | the `Left` in `«Left.Sortable»` | scope-local parameter binder; never a global encoded name |
| import selector | module path segment or imported visible name | textual lookup only; discarded after resolution |

A declaration's own visible name is excluded from its true-name body **[R]**.
References in that body are encoded names **[R]**.

The reader never mints identity **[MVP]**. Before semantic sealing, naming authority
supplies a `NamingAssignments` input that maps every declaration occurrence to its
randomly allocated EncodedName and supplies the visible-name/module lookup used by
references. An unassigned declaration, duplicate assignment, or reference without
one unambiguous assignment is a typed refusal. The owning edit operation requests
allocation before sealing; allocation and collision handling remain outside the
reader.

```text
NamingAssignments.Vector<NamingAssignment>
NamingAssignment.{DeclarationOccurrence EncodedName}

TextualMetadataLookup.Vector<TextualMetadataEntry>
TextualMetadataEntry.{ModulePath VisibleName EncodedName}
```

`DeclarationOccurrence` is an ephemeral structural-discovery handle for this decode
operation. It is not an object identity, is not retained in semantic bodies, and is
never hashed. Every discovered declaration occurrence has exactly one assignment;
every assigned occurrence must exist in the document.

This distinction is why a bare atom can be a reference in a role position while
`Name.Type`, `Name.{...}`, and `Name.[...]` introduce declarations. The active
expected type, not spelling in isolation, decides.

### 4.1 Scope rules

The MVP scope model is **[MVP]**:

1. Every direct `Declaration`, `TraitDeclaration`, and `TableDeclaration` in one
   body contributes a top-level name to that body's module scope. Interface inline
   role declarations and Interface `Types` therefore share one scope.
2. Enum variant names are declarations scoped by their owning enum. They do not
   occupy the top-level module scope.
3. Trait method names are declarations scoped by their owning Trait. They do not
   occupy the top-level module scope.
4. A `ParameterBinder` is local to the nearest containing type declaration or
   method declaration. It never escapes that declaration and never receives a
   global EncodedName.
5. Import selectors extend only the document's textual-resolution environment.
   They do not introduce semantic declarations or alter an object's own name.
6. Duplicate names are refused within their exact scope. The same visible spelling
   in distinct enum, Trait, or local-binder scopes is valid.

## 5. Shared declaration schemas

### 5.1 Plain type declarations

```text
Declaration.[
  Type.TypeDeclaration
  Nomos.NomosDeclaration
]

TypeDeclaration.{DeclarationName TypeBody}

TypeBody.[
  Newtype.TypeExpression
  Struct.TypePositions
  Enum.Variants
]

TypePositions.Vector<TypeExpression>
Variants.Vector<VariantDeclaration>

VariantDeclaration.{VariantName VariantBody}

VariantBody.[
  Unit
  Unary.TypeExpression
  Product.TypePositions
]
```

Canonical structural projections already ruled or directly derived from ruled
delimiters:

```ethos
Topic.String
Entry.{Topics Kind Description}
Kind.[Decision Principle Correction]
Status.[Pending Ready.«Numeric»]
```

The authored surface does not write `Newtype`, `Struct`, `Enum`, `Unit`, `Unary`,
or `Product`. The declaration position and delimiter choose the strict encoded
alternative:

- `Name.Type` selects `Newtype` **[R/D]**.
- `Name.{...}` selects `Struct` **[R]**.
- `Name.[...]` selects `Enum` **[R]**.
- a bare enum member selects `Unit` **[D]**.
- `Variant.Type` selects `Unary` **[D]**.
- `Variant.{...}` selects `Product` **[D]**.

`TypePositions`, `Variants`, and the other named sequence types are
purpose-specific encoded types. Their bootstrap implementation may contain an
honest typed collection internally; they are not a universal `Vec<Fields>`.

### 5.2 Type expressions

```text
TypeExpression.[
  Reference.TypeReference
  ShapeApplication.ShapeApplication
  TraitRequirement.TraitRequirement
]

ShapeApplication.{ShapeReference TypeArguments}
TypeArguments.Vector<TypeExpression>

TraitRequirement.{ParameterBinder RequiredTraits}
ParameterBinder.[Inferred Named.LocalName]
RequiredTraits.Vector<TraitReference>
```

Ruled canonical forms:

```ethos
Vector<Timestamp>
Vector<«Ordered»>
Result<Vector<«Ordered»> «Error»>
Range.{«Ordered» «Ordered»}
Pair.{«Left.Sortable» «Right.Sortable»}
Value.Vector<«Ordered Serializable»>
```

Shape applications keep bare angles **[R]**. Trait requirements use guillemets
at every occurrence **[R]**. Several traits inside one guillemet pair constrain
one parameter **[R]**. Unmarked names inside a Shape are ordinary concrete type
references **[R]**. Repeated bare requirements co-refer and named prefixes create
distinct parameters **[R]**.

`ParameterBinder` and its exact strict representation are **[P/MVP]**. For an
inferred binder, the reader resolves every required Trait to its EncodedName,
rejects duplicates, sorts the EncodedNames by canonical byte order, and uses that
normalized nonempty vector as the co-reference key. Equal normalized vectors
co-refer only within the containing type or method declaration. Named binders remain
distinct even when their normalized Trait vectors are equal; reuse of one local name
with a different normalized vector is a typed refusal **[MVP]**.

The exact strict recursive algebra above is **[D/MVP]**. It makes the reader's
classification explicit without introducing authored generic-parameter heads or
string-based resolution.

### 5.3 Nomos declarations

There is no generic `TransformerApplication { name, transformer, payload }` in
encoded form **[R]**.

The declaration sum is extended by one purpose-designed Stream arm **[P/MVP]**:

```text
NomosDeclaration.[
  StreamInitiation.StreamInitiationDeclaration
]

StreamInitiationDeclaration.{
  DeclarationName
  Query.TypeExpression
  Event.TypeExpression
}
```

#### Authored declaration schema

The canonical authored projection is:

```ethos
Observer.Stream.(ObserverFilter ObservationEvent)
```

This source contains exactly one declaration. The outer `Observer` supplies its
`DeclarationName`; that name is therefore elided from the parenthesized payload.
The resolved `Stream` Nomos head selects `StreamInitiationDeclaration`, whose payload
is exactly the query `TypeExpression` then the event `TypeExpression`. `Stream` is
not preserved as a transformer field, and the reader never constructs a generic
transformer or application node. There is no separately authored termination arm.

#### Generated Interface declaration schemas

Resolving that strict declaration causes one atomic schema transaction to produce
exactly three nominal Interface declarations and exactly three Interface-owned role
relations **[P/MVP]**:

```text
GeneratedStreamInterfaceDeclarations.{
  Initiation.StreamInitiationInterfaceDeclaration
  Output.StreamInterfaceDeclaration
  Termination.StreamTerminationInterfaceDeclaration
}

StreamInitiationInterfaceDeclaration.{
  EncodedName
  Query.TypeExpression
}

StreamInterfaceDeclaration.{
  EncodedName
  StreamOfEvent.ShapeApplication
}

StreamTerminationInterfaceDeclaration.{
  EncodedName
  StreamHandle.TypeReference
}

GeneratedStreamRoleRelations.{
  InitiationInput.InterfaceRoleMembership
  StreamOutput.InterfaceRoleMembership
  TerminationInput.InterfaceRoleMembership
}
```

The output declaration body is directly `Stream<Event>`. The termination declaration
body is a reference to that output declaration, not a second handle type. The three
relations are, in order, Input to the initiation declaration, Output to the direct
`Stream<Event>` declaration, and Input to the termination declaration. These are
ordinary `InterfaceRoleMembership` relations; Stream creates no fifth Interface
section.

The transaction obtains exactly three stable EncodedNames from naming authority:
the authored outer `DeclarationName` designates the output identity, and the same
transaction obtains the initiation and termination identities. Either all three
declarations, their bodies, and their role relations are installed, or none are.
Later edits preserve those associations rather than deriving new identities from
visible text. The reader requests and consumes this complete atomic assignment; it
does not mint any of the identities.

The following are generated explanatory projections. They are not additional
authored declarations, and their visible spellings are only textual metadata:

```ethos
ObserverInitiation.ObserverFilter
Observer.Stream<ObservationEvent>
ObserverTermination.Observer
```

#### Runtime value schemas

The runtime values are narrower than the declaration machinery **[P/MVP]**:

```text
StreamInitiationValue<Query>.Query
StreamValue<Event>.StreamIdentity<Event>
StreamTerminationValue<Event>.Stream<Event>
```

An initiation value is exactly the query value. A `Stream<Event>` handle contains
exactly one `StreamIdentity<Event>`. A termination value contains exactly that same
`Stream<Event>` handle value; it does not introduce another stream identity.
`StreamIdentity<Event>` remains opaque at this schema boundary.

#### Handwritten Rust behavior

Runtime routing, the live-stream registry, termination handling, and refusal
production and handling remain handwritten Rust in this stage. Existing behavior
demonstrates a live handle, routing, and termination, but it does not prove Interface
Output membership. This provisional generation contract therefore adds the explicit
Interface-owned Output relation for the direct `Stream<Event>` declaration. No
existing implementation is treated as schema authority.

This contract admits no generic carrier, separately authored termination arm,
grant or subscription declaration, grant or subscription value, or Stream-specific
Interface section.

### 5.4 Strict leaf references

Every reference leaf has one admitted target class **[MVP]**:

| Leaf | Admitted target | Refusal examples |
|:--|:--|:--|
| `TypeReference` | a named plain type declaration or audited strict Nomos declaration whose result is a nominal type | Trait, Shape, table, method, absent identity |
| `ShapeReference` | a prior-vocabulary Shape identity | ordinary type or Trait identity |
| `TraitReference` | a local, imported, or prior-vocabulary Trait identity | type or Shape identity |
| `RoleEntry.Reference` | a concrete nominal type identity | anonymous application, Trait, table |
| `RecordType` | a `PersistentNominalDeclaration` admitted as storable | anonymous expression, Trait, table |
| `KeyType` | any `PersistentNominalDeclaration`; the key is a separately supplied typed value | anonymous expression, Trait, Shape, table |
| resolved Nomos head | one concrete audited Nomos identity with one strict declaration schema | unknown head or head whose schema is not admitted in this body position |

`DeclarationName`, `VariantName`, `TraitName`, `MethodName`, `TableName`, and
`LocalName` are not reference leaves. Module and imported-name atoms are textual
selectors, not semantic references. A visible spelling never chooses a semantic
kind after resolution; the resolved EncodedName's registered kind does.

### 5.5 Bootstrap prior vocabulary

The reader receives this minimum prior vocabulary from the naming and schema
authorities **[MVP]**:

| Class | Prior entries |
|:--|:--|
| file kinds | `Interface`, `Nexus`, `Sema` |
| Interface roles | `Input`, `Output`, `Refusal` |
| primitive nominal types | `String`, `Integer`, `Boolean`, `Unit` |
| Shapes | `Vector`, `Option`, `Map`, `Result` |
| Stream declaration head | `Stream`, exactly two ordered `TypeExpression` payload positions: Query then Event; selects `StreamInitiationDeclaration` |
| Stream handle Shape | `Stream`, exactly one Event `TypeExpression` argument; produces the direct stream-handle type |
| Stream identity Shape | `StreamIdentity`, exactly one Event `TypeExpression` argument; types the opaque runtime identity inside a stream handle |
| structural declaration alternatives | newtype, struct, enum, Trait, table |

These are typed prior identities, not magic string comparisons. Their visible
spellings are textual metadata. Domain types, domain Traits, and component modules
must be declared or imported. The expected declaration-head or Shape role determines
the admitted `Stream` arity; the reader does not overload by comparing its spelling.
`StreamIdentity` is not a Nomos declaration head and cannot replace either Query or
Event in the two-position authored Stream payload except as an ordinary resolved
type expression where the surrounding schema independently admits it.

## 6. Interface root

```text
InterfaceBody.{
  Inputs
  Outputs
  Refusals
  Types
}

Inputs.Vector<RoleEntry>
Outputs.Vector<RoleEntry>
Refusals.Vector<RoleEntry>
Types.Vector<Declaration>

RoleEntry.[
  Declaration.Declaration
  Reference.TypeReference
]

InterfaceRoleMembership.{InterfaceRole TypeReference}
InterfaceRole.[Input Output Refusal]
```

The four body positions and their order are ruled **[R]**. Their universal Input,
Output, and Refusal memberships are supplied by position and never repeated as tags
**[R]**.

`RoleEntry = Declaration | TypeReference` is active **[MVP]**. It avoids requiring
every role entry to redefine a type:

- an imported type may acquire a component role by reference;
- a type declared once in `Types` may serve several roles;
- one encoded identity can be both Input and Output where the domain requires it;
- a role-specific type can still be declared inline when it has no independent
  non-role home.

A bare type reference in a role vector does not mutate the referenced type. The
Interface root owns an `InterfaceRoleMembership` relation from Input, Output, or
Refusal to that type's EncodedName **[MVP]**. An inline declaration receives its
naming-authority assignment and the Interface creates the same relation. Thus one
type body remains unchanged while one Interface may assign several roles. All
top-level declaration names still resolve in one module scope.

Refusals are not restricted to a fixed `{Reason Explanation}` product. A Refusal
entry may declare or reference any strict type, and its role position drives the
generated refusal/error membership **[MVP]**. Mapping each input to its possible
outputs or refusals would introduce interaction behavior not present in the ruled
four-position root; that belongs to later behavior growth, not this bootstrap.

Streams add no fifth position. Initiation and termination participate as ordinary
typed Inputs; the successfully established `Stream<Event>` participates as an
ordinary Output; event and refusal types use the existing roles as appropriate
**[R/D]**. Section 5.3 gives the provisional strict authored declaration, its three
generated Interface declarations, and the exact Interface-owned role relations.

Minimal neutral review witness:

```ethos
Interface.{1 0 0}
[]
{
  [Submit.Request]
  [Accepted.Response]
  [Rejected.{Reason Explanation}]
  [Request.String Response.String Reason.String Explanation.String]
}
```

The body order and plain declaration syntax are ruled. The three-position version
spelling and nested role algebra are active **[MVP]**. This witness deliberately
contains no Stream syntax.

## 7. Nexus root

Recommended essence-first root:

```text
NexusBody.{
  Traits
  Types
}

Traits.Vector<TraitDeclaration>
Types.Vector<Declaration>

TraitDeclaration.{TraitName Methods}
Methods.Vector<MethodDeclaration>

MethodDeclaration.{MethodName MethodSignature}
MethodSignature.{Parameters Return}
Parameters.Vector<TypeExpression>
Return.TypeExpression
```

Nexus declares a component's behavioral traits and the types referenced by their
method signatures **[R]**. It does not declare implementation bodies. The method
surface is `method.{Parameters... Return}`; the final position is the return type,
the receiver is implied by trait membership, and borrowing and dispatch belong
below Ethos **[R]**. A specialized trait position writes no `Trait` tag **[R]**.

The exact root order is unruled. The historical 2026-08-05 proposal used
`{Types Traits}`. The active MVP root is `{Traits Types}` **[MVP]** because traits
are the essence of Nexus and their supporting local types are subordinate, matching
Interface's roles-first/support-types-last anatomy. This order is isolated behind
the typed `NexusBody` root schema; `primary-5pm` may revise that root without changing
the shared parser or declaration algebra.

The active signature encoding **[MVP]** separates a possibly empty parameter vector
from one mandatory return. Its canonical source projection flattens them into the ruled
last-position form. `Unit` is written explicitly when no value is returned. No
effects, resources, concurrency, lifecycle hooks, visibility, async marker,
configuration, or implementation positions are admitted in this stage.

A zero-method Trait is a marker Trait and projects exactly with an explicit empty
method product **[MVP]**:

```ethos
Serializable.{}
```

A bare `Serializable` in the Trait-declaration vector is not the marker projection;
there it would lack the explicit declaration body.

Minimal neutral review witness under the recommended order:

```ethos
Nexus.{1 0 0}
[]
{
  [Transformation.{transform.{Input Output}}]
  [Input.String Output.String]
}
```

Trait and signature syntax are ruled. Root order and version anatomy remain
active **[MVP]** choices pending deferred review.

## 8. Sema root

```text
SemaBody.{
  RecordTypes
  Tables
}

RecordTypes.Vector<PersistentNominalDeclaration>
Tables.Vector<TableDeclaration>

PersistentNominalDeclaration.Declaration

TableDeclaration.{TableName RecordType KeyType}
RecordType.TypeReference
KeyType.TypeReference
```

Sema specifies persistent record types, tables, and keys **[R]**. The active MVP
shape is the two-position body above and `table.{RecordType KeyType}` with exactly
those two positions **[MVP]**.

`RecordTypes` means any persistent nominal declaration admitted by the bootstrap
storage vocabulary **[MVP]**. It is not restricted to struct-shaped “records”:
newtypes, structs, enums, and a later audited strict Nomos declaration may qualify
when its concrete encoded result is nominal and storable. Anonymous type expressions,
Trait requirements, tables, and generic application carriers do not qualify.

The active MVP projection reads `records.{StoredRecord RecordIdentifier}` as “a table of
`StoredRecord`, keyed by `RecordIdentifier`.” Both slots require concrete nominal
type references. A compound row or key is declared once as a named type and then
referenced. The table's own name is declaration metadata tied to its encoded
identity; its true-name body contains the two referenced encoded names, not its
visible name.

One primary key and its uniqueness are inherent in the table abstraction **[MVP]**.
There are no index, uniqueness-list, migration-policy, lifecycle, storage-engine,
or evolution-hint positions. Database migration logic is derived from the atomic
schema edit **[R]**, not authored into each table. A real later need may introduce
another strict Sema declaration kind without widening every existing table.

Minimal neutral review witness:

```ethos
Sema.{1 0 0}
[]
{
  [StoredItem.{Identifier Item} Identifier.Integer Item.String]
  [items.{StoredItem Identifier}]
}
```

Plain type syntax is ruled. The Sema root, table spelling, record/key order, and
version anatomy are active **[MVP]** projections pending deferred review.

## 9. Exact cardinalities

These cardinalities are active **[MVP]** unless separately marked ruled:

| Structure | Cardinality |
|:--|:--|
| file top level | exactly one Header, one Imports vector, one Body **[R]** |
| Header semantic positions | exactly kind then version **[R]** |
| `EthosKind` | exactly one of Interface, Nexus, Sema |
| `EthosVersion` | exactly three nonnegative integers |
| import entries | zero or more |
| module path | exactly one outermost module plus zero or more submodules |
| imported names per entry | one or more |
| naming assignments | exactly one per discovered declaration occurrence; no extras |
| textual-metadata lookup | zero or more entries; at most one EncodedName per exact module-path/name pair |
| `Declaration` | exactly one TypeDeclaration or one audited concrete Nomos alternative |
| type declaration | exactly one assigned name and one strict TypeBody alternative |
| `TypeBody` | exactly one newtype, struct, or enum alternative |
| struct type positions | zero or more |
| enum variants | one or more |
| variant declaration | exactly one assigned variant name and one VariantBody alternative |
| `VariantBody` | exactly one unit, unary, or product alternative |
| unit variant payload | zero |
| unary variant payload | exactly one TypeExpression |
| product variant positions | one or more |
| Shape type arguments | one or more |
| `ParameterBinder` | exactly inferred or one named LocalName |
| Trait requirement | exactly one ParameterBinder and one or more distinct Trait references |
| strict Nomos declaration | exact arity fixed independently by its concrete arm |
| authored `StreamInitiationDeclaration` | exactly one outer DeclarationName plus Query then Event TypeExpressions; the parenthesized payload contains exactly the latter two |
| generated Stream Interface declarations | exactly three: initiation, direct `Stream<Event>` output, termination |
| generated Stream role relations | exactly three: initiation Input, stream Output, termination Input |
| `Stream<Event>` Shape arguments | exactly one Event TypeExpression |
| `StreamIdentity<Event>` Shape arguments | exactly one Event TypeExpression |
| Stream initiation runtime value | exactly the query value |
| Stream handle runtime value | exactly one `StreamIdentity<Event>` |
| Stream termination runtime value | exactly the same `Stream<Event>` handle value being terminated |
| Interface body | exactly Inputs, Outputs, Refusals, Types in that order **[R]** |
| each Interface role vector | zero or more RoleEntries |
| Interface support Types | zero or more Declarations |
| RoleEntry | exactly one Declaration or one TypeReference |
| Interface role relation | exactly one role and one resolved type per RoleEntry |
| Nexus body | exactly Traits then Types **[MVP]** |
| Nexus Traits | zero or more; zero methods makes a marker Trait |
| Nexus support Types | zero or more Declarations |
| Trait declaration | exactly one assigned Trait name and one Methods collection |
| Trait methods | zero or more |
| method declaration | exactly one assigned method name and one signature |
| method parameters | zero or more TypeExpressions |
| method return | exactly one TypeExpression **[R]** |
| Sema body | exactly RecordTypes then Tables **[MVP]** |
| Sema RecordTypes | zero or more persistent nominal declarations |
| Sema Tables | zero or more |
| table body | exactly RecordType then KeyType |

Empty vectors remain explicit `[]`. An empty marker Trait method product remains
explicit `{}`. A missing object or position is never inferred as empty.

## 10. Shared reader invariants

The hand-written bootstrap reader must obey these invariants:

1. Discover raw structural boundaries before semantic classification **[R]**.
2. Decode the header first and select exactly one expected body root **[R]**.
3. Retain the Header in bootstrap source/document metadata; exclude it from every
   declared semantic body and TrueName **[MVP]**.
4. Decode imports second as textual resolution context and discard them after
   reference resolution **[R/MVP]**.
5. Discover declaration occurrences before resolving bodies, require a complete
   `NamingAssignments` input from naming authority, and never mint identity in the
   reader **[MVP]**.
6. Make source order semantically irrelevant within each scope **[MVP]**.
7. Enforce the top-level, enum-variant, Trait-method, and local-binder scopes in
   section 4.1 **[MVP]**.
8. Load the typed bootstrap prior vocabulary before resolving authored references
   **[MVP]**.
9. At every recursive position, expected type plus local structure selects one
   strict alternative **[R/D]**.
10. Resolve every semantic reference to an EncodedName and validate the strict leaf
    target class in section 5.4 **[R/MVP]**.
11. Do not preserve visible spelling inside semantic bodies **[R]**.
12. Carry each semantic form in its purpose-designed type. Do not use universal
    field vectors or a generic transformer application **[R]**.
13. Decode a `RoleEntry` declaration or reference to one resolved type identity,
    then create an Interface-owned role-membership relation; never alter the type
    body to add a role **[MVP]**.
14. Normalize inferred Trait binder vectors and limit co-reference to the containing
    declaration **[MVP]**.
15. Parse all three file kinds with the same machinery. A kind supplies only its body
    root; per-kind parsing code is implementation failure **[R]**.
16. Preserve encoded meaning, not source bytes **[R]**.
17. Do not add current-substrate concepts merely because Rust generation needs them.
    Handwritten Rust is this stage's behavior implementation, not its schema source
    **[R]**.

The complete hand-written bootstrap reader inventory is therefore:

```text
Envelope
  Header
    EthosKind
    EthosVersion
  Imports
    ImportEntry
    ModulePath
    ImportedNames

Context
  BootstrapPriorVocabulary
  NamingAssignments
  TextualMetadataLookup
  ScopeStack

Declaration
  TypeDeclaration
    DeclarationNameAssignment
    Newtype
    Struct
      TypePositions
    Enum
      Variants
      VariantDeclaration
        Unit
        Unary
        Product
  NomosDeclaration
    StreamInitiationDeclaration

GeneratedStreamInterfaceDeclarations
  StreamInitiationInterfaceDeclaration
  StreamInterfaceDeclaration
  StreamTerminationInterfaceDeclaration
  GeneratedStreamRoleRelations

RuntimeStreamValues
  StreamInitiationValue<Query> = Query
  StreamValue<Event> = StreamIdentity<Event>
  StreamTerminationValue<Event> = Stream<Event>

TypeExpression
  TypeReference
  ShapeApplication
    ShapeReference
    TypeArguments
  TraitRequirement
    ParameterBinder
    RequiredTraits

InterfaceBody
  Inputs
  Outputs
  Refusals
  Types
  RoleEntry = Declaration | TypeReference
  InterfaceRoleMembership
  InterfaceRole = Input | Output | Refusal

NexusBody
  Traits
  Types
  TraitDeclaration
    MarkerTrait
    Methods
    MethodDeclaration
      MethodSignature
        Parameters
        Return

SemaBody
  RecordTypes
  Tables
  PersistentNominalDeclaration
  TableDeclaration
    RecordType
    KeyType

Validation
  Cardinality
  Scope
  StrictLeafTarget
  TraitBinderNormalization
  NamingAssignmentCompleteness
```

Every listed item is either a purpose-designed encoded type, a textual reader input,
or a typed validation boundary. Nothing is a generic semantic catch-all.

## 11. Deferred psyche review

Final psyche review is deferred to `primary-5pm`. It is not a gate on implementing
the provisionally authorized reader. The review docket is deliberately only five
questions:

1. **Envelope projection.** Confirm the three-integer `EthosVersion` anatomy and
   canonical `Kind.{major minor patch}` header projection. The version's meaning is
   already ruled.
2. **Interface role entries.** Confirm `RoleEntry = Declaration | TypeReference`,
   allowing imported/shared types and one identity with several roles.
3. **Nexus root.** Confirm active `{Traits Types}`, or revise it to the historical
   `{Types Traits}` proposal; confirm the exact trait/method signature schema.
4. **Sema root.** Confirm `{RecordTypes Tables}` and
   `table.{RecordType KeyType}` with exactly those two table positions.
5. **Import projection.** Confirm outermost-to-leaf colon-qualified module paths,
   an always-square nonempty imported-name vector, and no bootstrap alias form.

All five have active **[MVP]** answers in this report, so none blocks the reader.
The provisional Stream contract in section 5.3 is likewise active for the reader;
deferred review may revise it without reopening a generic application carrier.
Runtime logic, effects, resources, concurrency, temporal protocol semantics, and
neutral general data anatomy remain outside this report by the staged vision.
