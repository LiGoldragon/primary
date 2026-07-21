# Language-family proof-of-concept epic — exploratory design v1

Retired vocabulary (psyche ruling 2026-07-21): "mouth" -> textual interface; "organs" -> the two trees (nametree, structuretree); "spine" -> core invariant / core pathway; "door" -> entry point; "currency" -> value type. Historical text below is unreworded; read it through this table.

**Status:** design-only; no proof-of-concept branches or component repositories were created.

**Written:** 2026-07-15, `management-language-family-poc` / `exploratory-design`.

This presentation precedes implementation of a language-family proof of concept.
It reconciles the evidence ledger, Claude-authored design corpus, current source,
and a fresh exact-revision compatibility measurement. It intentionally distinguishes
psyche rulings from implementation facts and agent design. A design report is an
agent working surface, not evidence that its proposals were accepted.

## 1. Executive outcome

The smallest coherent end-to-end proof of concept is not a Spirit deployment and
not a full NOTA merge. It is a bounded CoreSchema-to-CoreLogos slice, using
`CommitSequence` and `DatabaseMarker`, that proves all of the following together:

1. stringless Core plus separately versioned NameTable;
2. layout-tagged, domain-separated content identity over Core rkyv bytes, with
   NameTable excluded and rename therefore Core-hash-stable;
3. raw structural discovery that never assigns domain meaning;
4. one Core-type-associated bidirectional structural table driving decode and
   canonical encode;
5. both a trusted structural evaluator and one generated typed codec, proven
   equivalent on the slice;
6. two Textual forms over the same CoreLogos: TextualLogos and a bounded
   TextualRust form;
7. TextualRust conversion through `syn` and `prettyplease`, reproducing selected
   existing schema-rust goldens byte-for-byte;
8. a migration-shaped wire boundary that can transport Core plus NameTable without
   making the existing deployed signal/Spirit interfaces depend on unfinished work.

The PoC should prove the architecture without pretending to implement all Nomos,
all Logos, every daemon, all signal replacement, or a Spirit migration. It makes
those future interfaces explicit and tests their compatibility seam, but leaves
those components stubbed until the structural and Core contracts are proven.

A new exact-revision measurement resolves the apparent NOTA/Schema dispute:
current schema repositories compile only because their locks resolve old `nota`
main revisions. When the three source trees are copied to an isolated temporary
directory, their locks are removed, and the git source is patched to a clean
snapshot of `nota` commit `08ce05ca4eb2`, `schema-language` fails with exactly
13 errors. `schema-rust` fails through that pinned schema-language dependency.
The base `schema` repository fails more broadly (57 errors) because it targets an
older NOTA API as well as missing the new raw `Application` variant. Therefore
next-gen NOTA is integration-blocked, not falsified.

The exact next-gen NOTA flake check passed on 2026-07-15T10:51:54Z, including its
tests, formatting, clippy, docs, and custom architectural checks. Remote building
on `prometheus.goldragon.criome` was observed. This is durable evidence for NOTA
commit `08ce05ca4eb2` only; it is not evidence that the multi-repository integration
closure builds.

## 2. Evidence method and temporal reconstruction

### Classification rules

- **EXPLICIT-PSYCHE**: directly stated by the psyche.
- **ACCEPTED-DIRECTION, GATED**: a proposed direction accepted, but explicitly
  held pending the requested up-close review before implementation.
- **IMPLEMENTED-FACT**: observed code or build behavior; it does not imply
  approval.
- **AGENT-PROPOSAL**: an agent recommendation, including this document's concrete
  PoC and branch topology.
- **SUPERSEDED**: explicit later psyche ruling replaces an earlier position.
- **OPEN**: requires psyche authority or evidence is absent.

Conversation timestamps were not preserved as absolute timestamps in the supplied
session record. Artifact commit timestamps are absolute when recorded below; chat
items retain the 2026-07-14/15 bound and their ledger locators. This avoids forging
precision that the available evidence does not contain.

### Consequential shift ledger

| Time / source locator | Event | Classification | Present consequence |
| --- | --- | --- | --- |
| 2026-07-14, ledger L0 handover | Core/sema is the strictly typed rkyv substance; text is a bridge. Stack is NOTA → Schema → Nomos → Logos → Rust → rustc. Rust is the assembly language. | EXPLICIT-PSYCHE | Governing architectural constraint. |
| 2026-07-14, ledger L1 | “all Core* have no strings, they use the corresponding NameTable”; pattern may belong in a library. | EXPLICIT-PSYCHE | Core values must not retain display strings. |
| 2026-07-14, ledger L2 | BLAKE3 identity over stringless Core rkyv bytes, domain-separated and layout-tagged, NameTable excluded; rename stable. | ACCEPTED-PROPOSAL | Required PoC identity witness. |
| 2026-07-14, ledger L3 | CoreNomos is durable state at rest, symmetric with schema and Logos. | ACCEPTED-PROPOSAL | Future Nomos is a durable component, not a stateless macro helper. |
| 2026-07-14, ledger L5–L7 | Agglomerate parsing/encoding concerns, including delimiters; complex Core types associate with the table that expands the next block; one association drives encoding and decoding. | EXPLICIT-PSYCHE | The PoC must use one type-associated bidirectional structural surface. |
| 2026-07-14, ledger L9.1 and L9.3 | Four-crate and lowering directions accepted only after up-close design review. | ACCEPTED-DIRECTION, GATED | This report presents a PoC; it is not implementation authorization. |
| 2026-07-14/15, ledger L11/L13 | `Textual*` replaces the confusing `True*` text-side naming; CoreLogos has Logos and Rust textual form trees and may later gain other language forms. | EXPLICIT-PSYCHE | Many-form design is required; concrete trait mechanics remain proposal. |
| 2026-07-15, artifact `7f2782ac3` / `up-close-design-v1.md` | Consolidated four-crate, structural-form, Textual, and lowering sketches. | AGENT-PROPOSAL | Valuable design evidence, not acceptance. |
| 2026-07-15, task steering from parent, source: explicit psyche ruling | Right-associative dot and expected-type float reconstruction are blessed. The blanket requirement that every period-bearing string uses `(| |)` is rejected. With expected String, including transparent/newtype wrappers whose ultimate inner type is String, dotted raw application reconstructs string text as it does for Float. | EXPLICIT-PSYCHE; SUPERSEDES period-string proposal | Next-gen merge gate for the three readings is partly cleared: dot and float are blessed; string behavior must be corrected and re-tested before merge acceptance. |

### Claude-worker and report trace

The evidence ledger's worker trace remains the controlling historical inventory:

- `827eb2c3`, 2026-07-14 22:32: syntax and Core-first audits, agent artifacts.
- `28601d88e` and `791a0c13`, 2026-07-14 23:40: shared-codec and Logos→Rust
  lowering proposals, later accepted only in direction and gated.
- `e74f51de`, 2026-07-15 11:47: Spirit principle/slate-process doctrine,
  implementation of an explicit process ruling.
- `7f2782ac3`, 2026-07-15 11:51: up-close reconciliation, unreviewed agent
  design.
- `0468f609`, 2026-07-15 12:42 in the ledger trace: vision evidence ledger,
  agent reconstruction rather than a new ruling.

Several scouts were marked failed only because their harness rejected a
read-only report for lacking changed-file evidence. Their findings are considered
only where separately reproduced or cited as agent evidence; a failure label is
not treated as negative technical evidence.

## 3. Latest defensible vision

### Settled kernel

The following is the architecture this PoC must honor.

1. **Sema/Core is substance; Textual is a bridge.** State, edit history,
   snapshots, identity, and predictable upgrades ultimately operate over typed
   binary Core, not text.
2. **Every Core is stringless and NameTable-backed.** A Core value contains stable
   identifiers and typed structure, never owned display names.
3. **Core identity is independent of naming.** Canonical stringless Core rkyv bytes
   plus a language domain and typed layout version determine the Core hash. The
   NameTable does not enter that preimage, therefore a rename does not alter it.
4. **One table is associated with each complex Core type and governs both
   directions.** The expected Core type selects the structure to expand; raw input
   never self-classifies.
5. **Textual has many forms.** At least TextualLogos and TextualRust are views of
   one CoreLogos; future language forms are deliberately open.
6. **Logos is one-to-one with Rust at the Core level.** Every semantic Rust token
   that the supported Logos subset represents is data, not a decision constructed
   by Rust projection.
7. **Nomos is durable state.** It transforms typed CoreSchema plus names to typed
   CoreLogos plus an extended name allocation, outside text.
8. **The existing generated Rust corpus is the acceptance oracle.** It must not
   move merely because the input representation changes.
9. **Rewrite magnitude is not a constraint.** Beauty and evolvability outrank
   preserving today’s text-first implementation.

### Settled syntax consequences

- Right-associated raw application is blessed: `A.B.C = A.(B.C)`.
- A raw application reconstructs numeric text when the expected type is Float.
- A raw application reconstructs string text when the expected type is String,
  including through any transparent/newtype wrapper that ultimately expects String.
- This is an expected-type rule, not lexer classification. The raw tree remains
  the same application tree in every case.
- No claim is made here about spaces, pipes, other delimiters, arbitrary opaque
  literals, or additional escaping. Those need independent rules; this report
  deliberately does not infer them.

### Valuable but unaccepted or gated design

The following should be treated as hypotheses exercised by the PoC, not silently
implemented as settled fact:

- the precise four crate names and repository boundaries;
- sidecar storage mechanics and revision identity for structural tables;
- declarative forms with an evaluator plus generated codecs;
- whether that evaluator ships in normal runtime or is initially a conformance
  reference implementation;
- raw profile revisions and the `$` Nomos extension;
- StructuralMacroNode's dotted conversion and removal of a headed compatibility
  form;
- the concrete TextualForm trait (over its EncodedForm — the settled pair; reseated
  over the nametree + structuretree in `textual-form-vision-design-v1.md`) and the
  exact `syn` two-way subset;
- Nomos meta-types, macro terminology, and detailed lowering slate;
- schema unit/split/merge identity, the lost bootstrap question, and sema-engine's
  successor stored-record identity;
- Spirit deployment scope for this PoC.

The correct status is not “rejected.” It is “do not convert a useful agent design
into psyche intent before it has been reviewed at the point where working evidence
exists.”

## 4. Measured source truth and compatibility resolution

### Exact revisions inspected

| Component | Current inspected source | Role in PoC |
| --- | --- | --- |
| NOTA next-gen | clean reconstructed snapshot of `08ce05ca4eb2` (nota 0.8.0, nota-derive 0.4.0) | candidate raw-discovery producer; unmerged |
| `repos/nota` | detached `fb60c697f559`, main-era checkout | not next-gen ground truth |
| schema | detached `eadfb7a6ccb6` | older string-bearing implementation |
| schema-language | detached `f1cc35f96ac5`; Cargo source pin `59d59aca5767523a929e5bd6fcd011a4a4e8ff23` | existing Core-shaped source to stringless-ify |
| schema-rust | detached `41f9dd611bb7` | golden oracle and eventual TextualRust harvest source |
| sema-engine | detached `0568321f6a87` | durable-log and upgrade mechanism source |
| signal-schema | detached `5248dc77a2c5` | current text-bearing contract to supersede later |
| signal-frame | detached `644f404e5d5c` | retained shared framing component |

The detached checkout identities above are observations at this audit time. Cargo
lock source revisions differ because each repository carries its own lock.

### Isolated exact-next-gen procedure

No shared checkout, lock, or branch was modified.

1. A fresh temporary directory was created:
   `/tmp/language-family-poc-nextgen-compat-1784112609`.
2. Every tracked file was reconstructed from NOTA commit `08ce05ca4eb2` using
   `jj file list -r` plus `jj file show -r`; this avoided using the active
   next-gen worktree, which has uncommitted modifications.
3. `schema`, `schema-language`, and `schema-rust` were copied into that temporary
   directory and had their `.jj` and `.git` metadata removed.
4. Each copied `Cargo.toml` received only this temporary patch:

   ```toml
   [patch."https://github.com/LiGoldragon/nota.git"]
   nota = { path = "/tmp/language-family-poc-nextgen-compat-1784112609/nota" }
   ```

5. The copied lockfiles were removed before the exact test, so Cargo could resolve
   the patched `nota` 0.8.0 rather than retain the old git-locked 0.5/0.6 versions.
6. Each crate was checked with an isolated `CARGO_TARGET_DIR`.

The first attempt retained the original lockfiles; Cargo warned that the patch
was unused and compiled the old git-resolved NOTA. That run is deliberately not
counted as compatibility evidence. The lock-regenerated run resolved `nota 0.8.0`
and `nota-derive 0.4.0` from the reconstructed exact snapshot.

### Results

| Test target | Result | Meaning |
| --- | --- | --- |
| schema-language against exact next-gen | failed: 13 compiler errors | decisive integration blocker |
| schema-rust against exact next-gen | failed through its pinned schema-language revision | transitively blocked; not an independent schema-rust API verdict |
| schema against exact next-gen | failed: 57 compiler errors | older API contract has additional delimited/pipe API divergence; separate migration surface |
| base checkouts without override | compile clean, as recorded in ledger/scout | only proves old lock closure, not next-gen compatibility |

The 13 schema-language errors are exactly three absent
`Atom::split_at_first_dot` call sites plus ten non-exhaustive matches lacking
`Block::Application`. Their locations are `src/raw.rs`, `src/source.rs`,
`src/declarative.rs`, `src/expansion.rs`, and `src/schema.rs`. This reproduces the
original foundation-audit claim under the condition it actually asserted: an
explicit override to next-gen. It also explains why a main-based `cargo check`
reported green.

The 57 errors in `schema` include no-longer-present `AtomClassification`, removed
`PipeParenthesis`/`PipeBrace` delimiter variants and helpers, and non-exhaustive
Application matches. Do not collapse this into the 13-error migration: the two
repositories are different codebases at different raw API eras.

### Timestamped Nix evidence

At 2026-07-15T10:51:54Z:

```sh
nix flake check path:/tmp/language-family-poc-nextgen-compat-1784112609/nota --print-build-logs
```

passed. Nix evaluated the nota 0.8.0 package and checks `build`, `test`,
`design-examples`, `no-escaped-newline-nota-fixtures`,
`no-production-free-functions`, `operator-271-closed-claims`,
`derive-crate-no-zst-method-holders`, `doc`, `fmt`, and `clippy`. The log observed
remote builds and copies via `ssh-ng://nix-ssh@prometheus.goldragon.criome`.

This corrects stale blanket statements that the substituter is down. It does not
prove reproducibility of a schema or Spirit integration closure, because none has
yet been defined and pinned.

## 5. PoC architecture

### The dependency rule

Core types depend downward on portable identity and names. Textual machinery
depends on raw structure and names. No Core type depends upward on parser,
Textual, `syn`, or a formatter.

```text
content-identity        raw-discovery
        ↑                    ↑
   name-table              │
        ↑                   │
     CoreSchema ──→ CoreLogos
        ↑                   ↑
        └──── structural-codec / Textual forms ────┘
                              └── TextualRust (syn + prettyplease)
```

The arrows describe allowed source dependencies, not transformation direction.
`TextualSchema`, `TextualLogos`, and `TextualRust` read Core values through the
structural-codec boundary; Core values never import those view crates.

### Proposed substrate split

This is an AGENT-PROPOSAL that respects the accepted direction and keeps each noun
independently testable.

| Proposed component | Owns | Does not own | PoC implementation |
| --- | --- | --- | --- |
| `content-identity` | portable rkyv bound, typed domain/layout tag, canonical archive bytes, `ContentHash<Domain>` | names, raw text, storage engine policy | yes |
| `name-table` | `Identifier`, append-only/interner semantics, name derivation helpers, table identity | Core ASTs, raw blocks, text parsing | yes |
| `raw-discovery` | raw node tree, delimiter recognition, application association, source spans/profile identifier | floats, strings, paths, Schema meaning | yes, narrow lift/adaptor |
| `structural-codec` | declarative structural forms, table lookup by CoreTypeId, evaluator, canonical text-side encode rules, evaluator/generated conformance harness | domain AST ownership, sema log policy, arbitrary macro execution | yes, only PoC forms |

The sidecar association is proposed as:

```text
(CoreTypeId, StructuralRevision) → StructuralForm
```

The table has its own identity and is co-versioned with the language/dialect
package. It is excluded from a Core value's content hash. This is the only shape
consistent with rename-stable Core identity and text-as-bridge: a textual format
upgrade can decode historical text with an old structural revision and encode
canonical text with a new revision while arriving at the same Core value.

That sidecar conclusion is a strong derivation, but its storage mechanics are
still a proposal rather than a separately accepted psyche ruling.

### Raw discovery and the bidirectional table

The raw layer recognizes only facts such as:

```text
Atom("two")
Delimited(Brace, children)
Application(head, payload)
PipeText(text)
```

It does not recognize a string, float, path, map entry, field, macro, visibility,
or declaration. `A.B.C` remains a right-associated raw tree.

A structural table entry is selected by an already-known `CoreTypeId` at each
boundary. It specifies the exact structural form to consume or emit: delimiter,
positional children, application head/payload, cardinality, structurally disjoint
alternatives, leaf codecs, and recursive Core-type references. It cannot hold an
arbitrary user callback; arbitrary code would make format evolution and equivalent
encode/decode impossible to inspect or prove.

```text
RawBlock + expected CoreTypeId + StructuralTable + NameTable
  → decoded Core-shaped value

Core-shaped value + expected CoreTypeId + same StructuralTable + NameTable
  → canonical RawBlock
```

The PoC must support only disjoint alternatives. Ambiguous “first matching form
wins” is forbidden: a table is rejected when two alternatives can accept the same
raw structure for one expected type.

### New blessed string behavior in the table

The structural leaf vocabulary has an expected-type reader, not a lexer rule:

```text
FloatText:  Application spine → joined dotted text → Float parser
StringText: Application spine → joined dotted text → String value
```

`StringText` is selected not only for an immediate String but through a transparent
or newtype wrapper whose terminal inner type is String. The wrapper must explicitly
publish that transparent terminal expectation; the evaluator must not infer
transparency from a name or from arbitrary representation shape.

Canonical encode for this accepted dotted-string case emits a dotted raw spelling
that re-enters as the same string under String expectation. The conformance
fixtures must include direct, one-wrapper, and multi-wrapper examples, along with
Float fixtures that share the raw application tree. This report makes no assertion
about canonical formatting or escapes for non-dotted strings, whitespace, pipe
content, delimiters, URLs beyond their dotted structure, or arbitrary opaque
foreign text.

### CoreSchema slice

The PoC begins with the existing `schema-language` Core-shaped algebra rather than
inventing another schema AST. It makes a deliberately small stringless slice:

```text
CoreSchemaDeclaration ::= Newtype | Struct
CoreSchemaNewtype     ::= { name: Identifier, wrapped: CoreTypeReference }
CoreSchemaStruct      ::= { name: Identifier, fields: Vec<CoreSchemaField> }
CoreSchemaField       ::= { name: Identifier, reference: CoreTypeReference }
CoreTypeReference     ::= Path(Vec<Identifier>)
```

The two witnesses are:

```text
CommitSequence.{ Integer }
DatabaseMarker.{ CommitSequence StateDigest }
```

The PoC has one explicit derived-name test only where data requires it:
`commit_sequence` and `state_digest` live as actual identifiers in CoreLogos. A
TextualLogos form may elide a field name only when the stored identifier equals
that independently established derived spelling. Rust projection resolves the
stored identifier; it never invents a field name.

The `schema-language` existing `CoreType` / kind-based `CoreReference` work is
reused as evidence and a migration source. The current string-bearing `schema`
repository is not made a parallel PoC implementation.

### Textual many-form slice

A `TextualForm` is proposed as a codec family object — one of many textual mouths of
an `EncodedForm` (the settled Core-side counterpart) — with three owned pieces:

1. a raw boundary (NOTA raw discovery or a foreign parser);
2. an expectation table for the relevant Core type family;
3. typed leaves needed at that boundary.

```text
TextualSchema: raw-discovery + Schema structural table → CoreSchema
TextualLogos:  raw-discovery + Logos structural table  → CoreLogos
TextualRust:   syn AST boundary + Rust structural map  → CoreLogos
```

The PoC implements TextualLogos and TextualRust for newtype and named-field struct
only. TextualSchema is the smallest importer required to demonstrate the
Core-type-associated bidirectional table. It does not implement every historical
Schema syntax.

### CoreLogos and Rust boundary

The PoC CoreLogos algebra represents all meaning necessary for the chosen Rust
items:

```text
CoreLogosItem ::= Newtype | Struct
Visibility    ::= Public | Private
Attribute     ::= ToolPath | CfgAttribute | DeriveGroup
Path          ::= Vec<Identifier>
Field         ::= { visibility, name, type_reference }
```

It must retain visibility, path segments, attribute ordering, derives, field names,
and declaration category as data. `TextualRust` may synthesize only the textual
surface required to transcribe such data: dotted Logos paths become Rust `::`,
Core identifiers resolve through NameTable, Rust delimiters appear for the stored
node kind, and `prettyplease` owns whitespace/layout. It cannot calculate derives
or visibility from Schema facts.

The decode direction uses `syn` for the selected Rust subset and rejects any
unsupported item/body explicitly. It does not implement Rust grammar. The PoC
subset is tuple newtypes and named-field structs with the selected attribute
shapes; arbitrary methods, statements, `macro_rules!`, and opaque Rust expressions
are outside the proof.

`prettyplease` remains the sole formatting authority. Byte-exact tests use only
existing prettyplease-canonical generated fixtures, never arbitrary hand-formatted
Rust. The selected golden text is both the output oracle and a Rust-decode fixture.

### Trusted evaluator and generated codec

A single structural form is authority. The evaluator is a small, closed reference
implementation that walks `StructuralForm` and `RawBlock`/structural mirror. A
one-type generated codec may be produced from the same form only after the
interpreter has a fixture suite.

The PoC must prove:

```text
raw → evaluator → StructuralValue
raw → generated codec → concrete Core
concrete Core → StructuralValue

all StructuralValue results equal

concrete Core → generated canonical encode → raw
concrete Core → evaluator canonical encode → raw

both raw trees equal
```

Whether the evaluator is a runtime dialect loader or a conformance-only reference
is not settled. The PoC compiles and runs it in tests and exposes no production
runtime dependency decision beyond that. This allows the evidence to inform the
future ruling instead of deciding it accidentally.

### sema-engine, signals, Nomos, Logos, and Spirit

- **sema-engine:** reuse its mechanisms as the durability model. The PoC may run a
  minimal in-memory/log-backed fixture to prove an atomic record containing
  `CoreSchema`, `NameTable`, and their independent identities, including rename
  receipt/replay. It does not change sema-engine's existing hash-chain domains or
  resolve its open stored-record identity policy.
- **signal-frame:** reuse the existing binary frame abstraction unchanged. Add a
  local PoC frame round-trip type if needed; do not regenerate all signal crates.
- **signal-schema:** do not alter it in this PoC. Define a small versioned
  prospective contract fixture showing `CoreSchemaEnvelope + NameTableEnvelope`
  rather than `SchemaText`. Slot listing/hash fetch are interface stubs with
  round-trip tests, not a deployed compatibility change.
- **Nomos:** no textual Nomos parser, `$` implementation, macro evaluator, or
  daemon is necessary. Define the typed input/output seam:
  `CoreSchema + SchemaNameTable → CoreLogos + extended LogosNameTable`, and use one
  fixed test lowering to create the PoC CoreLogos witnesses. This fixed lowering is
  explicitly a stub, not an implementation of accepted Nomos behavior.
- **Logos daemon:** no daemon is necessary. TextualLogos and TextualRust library
  paths establish the eventual Logos payload and generator contract.
- **Spirit:** out of scope. The PoC must not use a live Spirit service, mutate a
  store, alter a deployment pin, or claim deployment readiness. A future Spirit
  integration branch depends on a fully pinned, portable language release train
  plus isolated copied-store testing and rollback evidence.

## 6. Proposed epic and branch graph

This is an AGENT-PROPOSAL. Do not create any branch until the psyche accepts the
PoC scope and its required gated design decisions.

### Epic

Create one parent epic, `Language family Core/Textual proof of concept`, with
subtasks below. Each implementation subtask uses a fresh dedicated worktree from
clean `main`, an explicit disposition bead, and a pushed producer revision before
any consumer branch consumes it.

```text
P0 evidence-and-contract-freeze
 │
 ├─ P1 content-identity
 │    └─ P2 name-table
 │         ├─ P3 raw-discovery
 │         │    └─ P4 structural-codec
 │         │         └─ P5 CoreSchema/TextualSchema slice
 │         │              └─ P6 CoreLogos/TextualLogos/TextualRust slice
 │         │                   └─ P7 integration harness and prospective wire fixture
 │         └─ P8 sema-engine fixture adapter (may start after P1/P2)
 │
 └─ P9 release-train/Spirit design stub (documentation + contract pin inventory only)
```

### Branch and repository graph

| Branch/worktree proposal | Depends on | Produces | Landing disposition |
| --- | --- | --- | --- |
| `content-identity-poc` | sema-engine source evidence | portable archive bound, typed hash/domain/layout types, locked-byte compatibility tests | merge only after P1 review; existing sema-engine storage bytes must remain unchanged |
| `name-table-poc` | P1 | identifiers, table, name transforms, table identity and rename tests | merge after P2 review |
| `raw-discovery-poc` | nota `08ce05ca4eb2`, but not its merge | raw tree adaptor/lift and profile identity, application spine tests | independent; no NOTA merge implied |
| `structural-codec-poc` | P2 + P3 | forms/table/evaluator and generated-codec conformance slice | merge after form review |
| `schema-language-core-slice-poc` | P2 + P4 | stringless two-declaration CoreSchema slice and TextualSchema forms | integration-only until exact-next-gen migration direction accepted |
| `logos-textual-slice-poc` | P2 + P4 + P5 | CoreLogos slice, TextualLogos, `syn`/prettyplease TextualRust subset | integration-only until golden gate passes |
| `language-family-poc-integration` | all producers pushed | pinned manifest/flake/Cargo integration harness and prospective signal fixture | disposable unless full PoC accepted |
| `spirit-language-poc-plan` | integration only | pin/rollback/isolated-store plan, no deployment change | documentation-only; not a Spirit code branch |

The exact physical repository placement of the first four components remains
unaccepted. The branch graph is intentionally logical: if the psyche selects
standalone repositories, their worktrees are created under that policy; if the
up-close review collapses some into one repository with hard module boundaries,
the dependency graph and tests remain the same.

### Landing order

1. Freeze selected inputs and records: NOTA commit, schema-language source pin,
   schema-rust golden files, sema-engine test vectors, and the accepted syntax
   rules. This is not an implementation branch.
2. Land P1 only if its sema-engine compatibility evidence proves no existing
   storage-hash change. New Core domains are additive; existing sema domains stay
   byte-identical.
3. Land P2 and P3 independently after their narrow tests.
4. Land P4 after bidirectional/equivalence tests prove the table is a real common
   authority rather than another adapter.
5. Integrate P5/P6 only on a pinned integration branch. Do not merge a partial
   `schema-language` migration into main while next-gen NOTA compatibility remains
   broken.
6. Run P7 only after every producer is pushed and dependencies resolve without
   local paths. It creates no production deployment pin.
7. Decide whether any reusable result graduates from PoC. Otherwise discard the
   integration worktree/branches as the disposition beads require.

## 7. Versioning, migration, and rollback posture

### Versioning

- New substrate packages begin at `0.x` with explicit rkyv layout versions in
  their Core identity domains. A changed archive layout is a compatibility event,
  never a hidden refactor.
- Structural table revision and raw-profile revision are distinct. A table may
  evolve while preserving Core identity; a new glyph/profile must have an explicit
  profile revision and old decoder coverage if historical text is retained.
- NameTable has its own identity and versioned representation. A rename changes
  NameTable state/receipt, not Core content identity.
- Existing `nota` next-gen is a breaking public raw API. It remains a release-train
  candidate and must not merge until downstream adaptation, tests, and the revised
  String behavior land together.
- `signal-schema` remains unchanged during the PoC. A future Core-bearing contract
  uses a new operation/reply family or a compatibility-aware version change; it
  cannot silently reinterpret `SchemaText` fields.

### Storage and migration

The PoC tests a small co-versioned record fixture, not production state migration:

```text
CoreEnvelope { domain, layout_version, core_bytes, core_hash }
NameTableEnvelope { layout_version, table_bytes, table_hash }
Receipt { prior_core_hash, next_core_hash, prior_table_hash, next_table_hash, operation }
```

A rename witness must show equal Core hashes and changed NameTable identity. A
structural edit witness must show changed Core hash. A deliberately mismatched
layout version must fail loudly or select a specified upgrader; it must not decode
as if it were current.

No existing sema-engine records, Spirit stores, user state, or signals are
migrated in the PoC. Full upgrades later reuse sema-engine's deterministic
fold/checkpoint verification pattern after the open schema-unit and record-identity
rulings are supplied.

### Rollback/disposal

- Every producer branch is pushed before consumption, but no production pin is
  advanced.
- The integration branch uses only immutable commit pins; it has no local path
  dependencies at its final acceptance gate.
- A failed PoC discards its integration worktree and its designated feature
  branches. It requires no database or deployment rollback because it did not
  mutate one.
- A later Spirit rollout must use an isolated copied store and distinct socket,
  record a backup/restore rehearsal, and prove restoration of pre-upgrade state.
  That is future deployment work, not evidence supplied by this PoC.

## 8. Acceptance gates and test matrix

| Gate | Proof | PoC required? |
| --- | --- | --- |
| Core archive identity | archive/decode validates; hash has typed domain/layout; same Core bytes produce fixed digest vector | yes |
| Rename stability | name change changes NameTable receipt but preserves Core bytes/hash | yes |
| Structural disjointness | table construction rejects overlapping alternatives | yes |
| Raw non-classification | same Application raw tree drives Float and String expected-type fixtures | yes |
| Blessed dotted strings | direct String, one transparent wrapper, and nested transparent wrapper reconstruct dotted raw application; Float still does too | yes |
| Bidirectionality | evaluator decode/encode and generated decode/encode agree on all fixtures | yes |
| Canonical Textual round trip | Core → canonical raw/text → Core preserves Core and NameTable allocations under controlled fixture initialization | yes |
| TextualLogos | CoreLogos text includes stored visibility, paths, attributes, and field identifiers; only sanctioned name elision occurs | yes |
| Rust subset | `syn` decodes selected generated Rust; TextualRust re-encodes exact golden bytes through prettyplease | yes |
| Golden preservation | selected existing schema-rust golden excerpts are unchanged and compile in their existing test harness | yes |
| sema durability model | restart/refold fixture preserves paired Core/NameTable records and rejects tampering | yes, bounded fixture |
| prospective signal | rkyv frame round-trip for Core/NameTable fetch and slot-list reply types | yes, fixture only |
| next-gen compatibility | schema-language branch against exact pinned NOTA compiles and tests | no for foundation PoC; mandatory before NOTA merge/integration release |
| Nomos | durable package store, recursive macros, `$`, structural fallback | no; typed seam/stub only |
| Logos daemon | slot store/list/fetch daemon | no; library slice only |
| Spirit deployment | isolated copied-store launch, rollback rehearsal, production pins | no |

The PoC should run narrow Cargo tests first and expose them through a pinned Nix
check before acceptance. The next-gen NOTA Nix check passing is evidence only for
its own committed closure. The PoC's eventual Nix result must evaluate a portable
integration closure without `/tmp` or sibling path dependency inputs.

## 9. Explicit non-goals

- no merge of `nota/next-gen`;
- no general Schema migration or repair of all 13/57 next-gen errors;
- no full CoreSchema stringless conversion;
- no full Nomos language, `$` syntax, recursive macro evaluator, or macro package
  persistence implementation;
- no full CoreLogos coverage, Rust body model, or general Rust decompiler;
- no new signal contract rollout or generated consumer regeneration;
- no signal-frame consolidation campaign;
- no Spirit code, service manipulation, store migration, activation, deployment
  pin, or production rollback;
- no resolution of schema unit/split/merge semantics, the lost bootstrap question,
  or sema-engine successor record identity;
- no assertion that a structural evaluator belongs in production runtime.

## 10. Psyche-only ruling slate

These are decisions, not implicit approvals. Recommendations are only agent
recommendations.

1. **Authorize the bounded PoC scope and the design-only branch graph?**
   Recommendation: yes; it proves Core/Textual architecture without a deployment
   or whole-stack rewrite.
2. **Confirm the proposed first implementation order: content identity → NameTable
   → raw discovery → structural codec → CoreSchema slice → Logos/Rust slice?**
   Recommendation: yes; it makes the identity and text boundary testable before
   downstream migrations.
3. **Approve one declarative structural form as authority, with evaluator and
   generated-codec equivalence mandatory in the PoC?**
   Recommendation: yes. The later runtime-evaluator decision remains open.
4. **Approve structural tables as independently versioned, CoreTypeId-keyed text
   sidecars excluded from Core hash?**
   Recommendation: yes; this is the clean mechanism consistent with accepted
   rename-stable identity, but it remains a mechanism needing your word.
5. **Confirm the newly explicit string rule as the next-gen merge requirement:**
   dotted application reconstructs String under direct or transparent/newtype
   String expectation, while raw parsing remains structural. Recommendation: yes;
   it records the current ruling faithfully. No other escaping behavior is implied.
6. **For the PoC only, keep Nomos/Logos daemons and Spirit out of runtime scope,
   using typed seams and fixtures instead?**
   Recommendation: yes.
7. **When ready, choose the unresolved semantic boundaries:** schema unit and
   split/merge identity; restatement of bootstrap question 2; terminology for
   structural form versus macro; and the Core-side name. No recommendation is
   needed for the first two because they require your intent.

## 11. Sources

Primary evidence: `reports/logos/vision-evidence-ledger-v1.md` (especially §§1–7),
`reports/logos/up-close-design-v1.md`, `shared-codec-library-v1.md`,
`logos-rust-lowering-v1.md`, `core-first-architecture-v1.md`,
`syntax-recrystallization-audit-v1.md`, `design-v0.md`,
`nomos-macro-model-v1.md`, and the temporal scout result supplied in the task
context.

Source and command evidence is recorded in §4. The isolated temporary directory
is intentionally outside the repository and is not a portability input. It can be
deleted after independent review.
