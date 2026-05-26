# 197 — NOTA core design refresh and gap audit

Operator audit after refreshing current Spirit intent, recent reports, and the
schema/NOTA implementation branches on 2026-05-26.

## Scope

I treated this as an audit of the current NOTA-core / schema-derived design
arc, not a new implementation slice.

Read:

- `ESSENCE.md`, `INTENT.md`, `skills/reporting.md`,
  `skills/report-naming.md`, `skills/operator.md`,
  `skills/human-interaction.md`, `skills/nota-design.md`
- Spirit intent for `schema`, `nota`, `macro`, `assembled`, `header`,
  `component-shape`, `core`, and `naming`
- `reports/designer/350-schema-feature-drift-retraction-2026-05-26.md`
- `reports/designer/353-schema-derived-nota-design-2026-05-26.md`
- `reports/designer-assistant/354-schema-derived-nota-prototype-2026-05-26.md`
- `reports/designer/355-critique-of-operator-195-schema-driven-nota-reader-2026-05-26.md`
- `reports/operator/193-schema-object-pass-and-spirit-v0-3-skill-correction-2026-05-26.md`
- `reports/operator/194-nota-schema-restack-operator-reading-2026-05-26.md`
- `reports/operator/195-schema-driven-nota-reader-prototype-2026-05-26.md`
- `reports/operator/196-schema-object-block-pass-prototype-2026-05-26.md`
- repo intent files for `nota`, `nota-codec`, and `schema`

Branches inspected:

- `/home/li/wt/github.com/LiGoldragon/schema/operator-schema-driven-nota-parser-prototype-2026-05-26`
- `/home/li/wt/github.com/LiGoldragon/schema/designer-schema-derived-nota-2026-05-26`
- `/home/li/wt/github.com/LiGoldragon/nota/designer-schema-derived-nota-2026-05-26`
- `/home/li/primary/repos/nota-codec`

Verification I ran:

- `cargo test --test schema_driven_nota_reader` in the operator schema branch:
  5 passed.
- `cargo test -p schema-derived-nota-prototype` in the designer schema
  branch: 29 passed.
- `cargo test --workspace` in the designer schema branch: passed.
- `cargo test --workspace` in the operator schema branch: passed.

I did not independently rerun `nix flake check` during this audit. Reports
195, 196, and 354 each claim their relevant Nix checks passed.

## Current Intent Reading

The current load-bearing records are 730-778:

- 730-732 retract authored schema Features:
  `EffectTable`, `FanOutTargets`, `StorageDescriptor`.
- 746 says NOTA itself is schema-derived.
- 747-751 define schema as the interpretation layer for delimiter-shaped
  NOTA, with a precompiled core library, schema daemon, and three-part
  Specifying / Input / Output structure.
- 753 says macros bring their own shape-reading logic.
- 754-756 constrain the prototype: delimiter-first object parsing,
  separate schema interpretation, Rust reader code emitted from assembled
  schema.
- 758 corrects operator report 195: a delimiter shape means struct/newtype
  only in the macro position whose lowerer gives it that meaning.
- 759 and 769 identify the macro-free endpoint as `AssembledSchema` /
  `Asschema`: pure NOTA-representable assembled schema with fully resolved
  enum and struct definitions.
- 761 and 770-776 sharpen the parser layer: break input into delimiter-
  bounded object blocks with source spans and recursive shape predicates,
  then reassemble resolved blocks after macro expansion.
- 765-768 move Spirit-facing naming toward `spirit`, `signal-spirit`, and
  `core-signal-spirit` rather than old `persona-*` / `owner-*` ancestry.
- 778 allows considering new clean repositories if branch and old-repo
  ancestry become too confusing. This is not an immediate rename order.

## What Others Built

### Operator path

Reports 193-196 form one line:

1. `SchemaObjectPass`: delimiter-first `NotaValue` tree over schema text,
   with ordered namespace maps and path/object metadata.
2. `AssembledNotaSchema` + `NotaReaderRustEmitter`: schema namespace text
   lowers to ordered assembled declarations, then emits explicit
   `NotaDecode` impls.
3. Compiled fixture testing: generated Rust is string-compared to a fixture,
   compiled, and used to decode real NOTA.
4. `SchemaBlockPass`: source-oriented block scanner with byte/line/column
   spans and recursive shape predicates over delimiter-bounded blocks.

The current operator schema worktree has the object-block work committed as
`27254fc5` (`schema: add source block pass for macro shape predicates`) on
top of the reader-emission commit `f9b5fdd4` (`schema: prototype
schema-driven nota reader emission`). Report 196 is likewise present in the
primary workspace history as `ba8749c8` (`report operator/196: schema object
block pass prototype`).

### Designer-assistant path

Report 354 built a broader prototype on branch
`designer-schema-derived-nota-2026-05-26`:

- `nota/schema/nota.schema`
- `schema/prototype` bootstrap kernel
- three-part schema reader
- runtime `EmittedCodec` rule surface
- `MacroEngine` shape classifier
- in-process `Library` with core fallthrough
- `coordinate.schema` demo with non-empty Input and Output

This proves more of report 353's vision than operator 195, but it is
quarantined in a separate prototype crate and does not replace production
`nota-codec` or production `schema`.

### Designer critique

Report 355 correctly identified that operator 195 did not prove the
all-the-way-back claim, did not implement the three-part structure, did not
have macro shape-interpretation, and did not remove retracted Feature code.
Report 196 partially supersedes that critique by adding the source-span
object-block pass, but the rest of the critique still stands.

## Biggest Gaps

### 1. Repo-local intent is stale in exactly the place agents will read first

`repos/schema/INTENT.md` still says the top-level `.schema` file has six fixed
positional fields:

1. imports
2. ordinary header
3. owner header
4. sema header
5. namespace
6. features

That conflicts with records 730-732 and 747-751. It also conflicts with
designer report 353 and designer-assistant report 354. The same stale shape is
still visible in `schema/ARCHITECTURE.md` on current branches, even where the
operator branch softens "features vector" into "compatibility metadata
vector."

This is the highest-risk documentation gap because agents are explicitly told
to read repo `INTENT.md` and `ARCHITECTURE.md` when editing inside a repo.
Reports can be correct and still lose if repo-local guidance points agents
back into the old six-position / feature-slot model.

### 2. The retracted Feature surface is still executable and test-locked

The operator branch still exports and tests:

- `Feature::EffectTable`
- `Feature::FanOutTargets`
- `Feature::StorageDescriptor`

The full operator branch `cargo test --workspace` passed, but it passed while
running tests such as `effect_side_features.rs` that assert the retracted
surface still parses. That means the current green suite includes tests that
lock old behavior. Reports 350, 193, 195, and 196 all acknowledge this gap,
but it has not been removed.

The immediate correction is not only deleting code. The test suite needs to
flip: authored Feature forms should be rejected, while any useful hidden
composer/runtime machinery must be reachable only from assembled or inferred
data, not from authored `.schema` text.

### 3. Three schema shapes coexist without a migration boundary

The repo currently has at least three shapes:

- old production six-position schema with compatibility metadata/features;
- operator reader prototype that accepts one namespace map only;
- designer-assistant five-block schema: Specifying, Input header, Input
  extras, Namespace, Output.

Intent record 751 says "three-part structure" with optional second and third
parts; it does not yet canonically settle whether the five physical blocks are
mandatory, optional, or only one concrete serialization of the three parts.
Report 354 names this as an open psyche question; implementation has already
encoded the five-block choice in `ThreePartSchema::read`.

This needs a concrete migration boundary:

- what authored `.schema` files look like now;
- what `Asschema` looks like after macro lowering;
- how compatibility six-position files are accepted, fenced, or rejected.

### 4. The all-the-way-back claim is still prototype-only

Designer-assistant built `nota.schema` and a bootstrap kernel prototype, but
production `nota-codec` still owns real NOTA parsing and encoding. Operator
195 emits readers that depend on `nota_codec::Decoder`; it does not generate
`nota-codec` itself.

This is not a failure of the first slice. It is the next major gap: the
workspace has not yet moved from "prototype proves possible" to "production
NOTA is schema-derived."

The missing production chain is:

```text
nota.schema
  -> bootstrap kernel
  -> Asschema / assembled NOTA grammar
  -> emit_schema! composer
  -> generated nota-codec reader/writer surface
```

### 5. Bracket string versus vector interpretation is not cleanly unified

The designer prototype kernel makes a heuristic distinction:

- `[|...|]` is a block string.
- `[...]` with punctuation such as apostrophe, quote, colon, etc. becomes an
  inline string.
- `[...]` with token-like content becomes a vector and may later be
  reinterpreted by schema position.

The operator `SchemaBlockPass` takes a cleaner lower-level stance for the new
object-block layer: `[|...|]` is opaque, while ordinary `[...]` is a square
bracket block containing objects. But that layer does not yet implement the
full string-position interpretation either.

This needs one canonical rule set and tests that cover the hard cases:

- `[hello world]`
- `[we're ready]`
- `[User]`
- `[host localhost port 8080]`
- nested `[` / `]`
- `[|...|]` containing NOTA-like text
- string newtypes and map keys

Until this is settled, the square-bracket string design is still partly
implemented by heuristics rather than by schema-derived interpretation.

### 6. The new `.schema` examples violate the no-comments schema intent

Intent record 419 says schema files should not carry comments; descriptions
belong in code, not in schema source.

The new `nota.schema` and `coordinate.schema` in the designer-assistant branch
are comment-heavy, including long section banners and prose explanations.
That makes them useful teaching artifacts but not canonical schema files under
current intent.

The fix is straightforward:

- strip comments from actual `.schema` files;
- move explanations into `ARCHITECTURE.md`, README, or a report;
- add a test or lint if schema comments are meant to be rejected for authored
  schemas rather than merely discouraged.

### 7. NOTA quotation guidance is still contradictory

Current `nota-codec` source rejects `"` with `QuoteStringDelimiter`, and tests
assert that behavior. But `repos/nota-codec/INTENT.md` and
`skills/nota-design.md` still say the decoder accepts legacy quoted strings as
migration input through `read_legacy_quote_string`.

That is now stale. It directly contradicts the code and the stronger intent
cluster around records 698 and 703. Agents reading the skill can still come
away believing quoted strings are accepted.

This is a guidance-file bug, not a code bug.

### 8. The object-block pass is good, but not yet integrated enough

Report 196's own gap is right: `SchemaBlockPass` and `SchemaObjectPass` are
two separate trees. The reader validates source blocks, then separately
builds `NotaValue` objects. Macro lowerers will eventually need:

```text
source span + block shape + typed value
```

for the same object. Without a unified representation, future lowerers risk
lining up two trees by position, which is fragile.

### 9. `AssembledSchema` / `Asschema` is not yet a concrete canonical type

Intent says macro expansion ends in an `Asschema` / `AssembledSchema` file
type: pure NOTA, fully resolved, no macros. Operator 195 discovered that the
current production `AssembledSchema` stores types in a `BTreeMap` and loses
authored order. The prototype added `Vec<AssembledNotaType>`.

That is still split-brain:

- production `AssembledSchema` is lookup-friendly but not order-preserving;
- prototype `AssembledNotaSchema` is order-preserving but not canonical;
- "Asschema" is named in intent but not represented as a repo-level schema
  file or Rust type with stable serialization.

This should become the next stable center of the system.

### 10. Branch/report hygiene has improved, but integration still needs a map

During the audit, the object-block pass and report 196 were visible as active
working-copy changes; they are now described commits. That is good.

The remaining hygiene issue is integration mapping: there are multiple
branches with overlapping proofs, and no single report says which commits
operator should merge, which designer-assistant prototype pieces are only
evidence, and which old schema POC branches should be ignored because they
carry retracted Feature drift.

## Recommended Next Moves

1. Write a short integration map: operator object-pass/object-block/reader
   commits to carry forward; designer-assistant prototype artifacts to copy
   or reimplement; old drifted POC branches to ignore.
2. Patch `repos/schema/INTENT.md` and `schema/ARCHITECTURE.md` so repo-local
   truth no longer teaches six-position/features as the current design. If
   compatibility remains, call it compatibility.
3. Patch `skills/nota-design.md` and `repos/nota-codec/INTENT.md` to remove
   the stale claim that legacy quoted strings are accepted.
4. Strip comments from `nota.schema` and `coordinate.schema`, moving the prose
   into architecture/docs.
5. Convert authored Feature tests into rejection tests and move any surviving
   mechanism behind the assembled/composer layer.
6. Define `Asschema` concretely: order-preserving, pure NOTA-representable,
   fully resolved, no macros; then migrate production `AssembledSchema` toward
   it.
7. Merge the object-block and object-value passes into one representation with
   spans, delimiter shape, recursive predicates, and typed value access.
8. Decide and test the square-bracket string/vector boundary against the hard
   examples before moving it into production `nota-codec`.
9. Hook the reader emitter into `emit_schema!` and generate one real Spirit
   v0.3 reader surface from a `.schema` file, comparing it against the current
   hand-written contract behavior.

## Bottom Line

The work is better than it looks from any single report: operator has the
production-adjacent reader and object-block path; designer-assistant has the
broader self-hosting prototype; designer critique is mostly accurate but
partly superseded by operator report 196.

The biggest danger is not missing tests. The tests I ran are green. The
danger is stale guidance and parallel green prototypes preserving old shapes:
repo intent still says six fields and features; code still tests retracted
Feature parsing; `.schema` examples use comments despite no-comments intent;
and production `nota-codec` is not yet schema-derived.

The next useful slice is a cleanup-and-centering slice around `Asschema`:
make the guidance truthful, remove authored Features, unify block/value
parsing, and make one canonical assembled schema artifact the input to
`emit_schema!`.
