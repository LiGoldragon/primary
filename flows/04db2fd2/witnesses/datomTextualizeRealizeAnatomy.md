# Witness: datom textualize and realize anatomy

Method: code read `/git/github.com/LiGoldragon/protos/src/{lib,form,block,walk,shape}.rs`, `/git/github.com/LiGoldragon/datom/src/{lib,datom}.rs`, `/git/github.com/LiGoldragon/datom/tests/{substrate,external_surface}.rs`, `/git/github.com/LiGoldragon/protos/tests/substrate.rs`, `/git/github.com/LiGoldragon/signal-orchestrate/src/generated/signal.rs`, `/git/github.com/LiGoldragon/orchestrate/src/bin/orchestrate.rs`, `/git/github.com/LiGoldragon/curriculum-deploy/src/runtime.rs`, `/git/github.com/LiGoldragon/ethos-monolith/src/fixture/mod.rs`

## 1. Files and modules

Two crates, `protos` (v0.8.0) and `datom` (v0.5.0). Datom depends on Protos via git rev pin.

### protos (1319 lines of library source)

| File | Lines | Role |
|---|---|---|
| `src/shape.rs` | 1-26 | `Shape` enum (11 variants), `ShapeDefined` trait |
| `src/form.rs` | 1-14 | `Realize` and `Textualize` trait definitions |
| `src/block.rs` | 1-446 | `Block`, `Head`, `SourceText`, `StringCarrier`, `BlockScanner`, first-pass lexer |
| `src/walk.rs` | 1-792 | `StructuralWalk`, `RealizeWalk`, `TextualizeWalk`, `RealizeScope`, `TextualizeScope`, all driving traits |
| `src/lib.rs` | 1-41 | Re-exports and three cross-cutting traits (`Headed`, `BlockScanning`, `StringCarrying`) |

### datom (1435 lines of single module)

| File | Lines | Role |
|---|---|---|
| `src/datom.rs` | 1-1435 | All Datom domain types (`Text`, `Entry`, `Group`, `Report`, `InterimNote`, etc.), `DatomRealizing`/`DatomTextualizing` seam traits, `DatomRoot`, `DatomHeadedUnit`, `DatomText<T>`, impls for scalars/collections/records |
| `src/lib.rs` | 1-13 | Re-exports |

## 2. Core types

### Protos layer

- **`Shape`** (enum, 11 variants): `Bare`, `DottedBare`, `CurlyQuoted`, `DottedCurlyQuoted`, `Parenthesized`, `DottedParenthesized`, `SquareBracketed`, `DottedSquareBracketed`, `Guillemeted`, `Braced`, `DottedBraced`.
- **`Head(String)`**: the dotted prefix of a block.
- **`SourceText(String)`**: text as data before dialect interpretation.
- **`Block`**: one lexical unit from the first pass -- `head`, `shape`, `body: SourceText`, `string_carrier: Option<StringCarrier>`, `body_span`, `span`.
- **`StringCarrier`** (enum): `Bare(String)`, `Parenthesized(String)`, `CurlyQuoted(String)`.
- **`StructuralWalk`**: the neutral frame discipline (stack of `WalkFrame`, transition history).
- **`RealizeWalk`**: wraps `StructuralWalk` + `source_cursor` for text-to-real.
- **`TextualizeWalk`**: wraps `StructuralWalk` + `output: SourceText` + `emission_cursor` for real-to-text.
- **`RealizeScope<'a>`** / **`TextualizeScope<'a>`**: scoped handles that prevent raw walk mutation by the dialect.
- **Trait `Realize`**: `fn realize(&self) -> Result<Self::Real, Self::Fault>` (form.rs:2-7).
- **Trait `Textualize`**: `fn textualize(&self) -> Self::Textual` (form.rs:10-13).
- **Trait `ShapeDefined`**: maps shape + head to a selection enum (shape.rs:21-26).

### Datom layer

- **Trait `DatomRealizing`**: `fn realize_block(scope: &mut RealizeScope, block: &Block) -> Result<Self, DatomFault>` -- the per-type realization seam (datom.rs:253-255).
- **Trait `DatomTextualizing`**: `fn textualize_in(&self, scope: &mut TextualizeScope) -> Result<(), DatomFault>` -- the per-type projection seam (datom.rs:258-259).
- **Trait `DatomRoot`**: marker + default methods `realize_source` and `textualize_source` that create the one walk per document (datom.rs:279-297).
- **Trait `DatomHeadedUnit`**: for payloadless head-dot-unit enums like `Observe.Locks` (datom.rs:268-272).
- **`DatomText<T>`**: generic textual carrier; `impl<T: DatomRoot> Realize for DatomText<T>` (datom.rs:301-322).
- **`DatomEvidence`**, **`Realized<T>`**, **`Projected<T>`**: evidence-carrying wrappers (datom.rs:83-100).
- **`EvidencedRealizing`** / **`EvidencedTextualizing`**: typed operations that return transition evidence alongside the value (datom.rs:122-132).

## 3. Textualize pipeline (real-to-text)

### Entry points

1. **`DatomRoot::textualize_source(&self) -> Result<SourceText, DatomFault>`** (datom.rs:292-296): creates a fresh `TextualizeWalk`, calls `textualize_source` on it with a closure that delegates to `self.textualize_in(scope)`, returns `walk.textual_source()`.
2. **`EvidencedTextualizing::textualize_evidenced`** (e.g. datom.rs:1363-1380 for `Report`): same pattern but wraps the root block in `scope.textualize_block(Shape::Braced, None, ...)` and returns `Projected<T>` with walk observation.
3. **`Textualize::textualize(&self)`** (implemented for `Report` and `InterimNote` at datom.rs:1421-1435): delegates to `textualize_evidenced`, discards evidence.

### Dispatch

The walk itself is shape-agnostic. Dispatch is type-driven: each type's `DatomTextualizing::textualize_in` calls `scope.textualize_block(shape, head, closure)` with the correct shape for that type. The closure emits children by calling `child.textualize_in(body)` recursively.

Shape selection at textualize time:
- `String` / `Text`: `Shape::Bare` if `fits_bare()` returns true, else `Shape::CurlyQuoted` (datom.rs:816-829).
- `bool`: `Shape::Bare`, emits `"true"` or `"false"` (datom.rs:391-397).
- `i64`: `Shape::Bare`, emits decimal string (datom.rs:365-371).
- `Vec<T>`: `Shape::SquareBracketed`, no head (datom.rs:449-457).
- `BTreeMap<String, T>`: `Shape::Guillemeted` (`<<...>>`), entries as `Head.[value]` (datom.rs:504-516).
- Records (e.g. `Report`, `Group`, `InterimNote`): `Shape::Braced`, positional fields emitted in order.
- Enums / variants: `Shape::DottedBraced` with head = variant name.
- `DatomHeadedUnit` (e.g. `Observe`): `Shape::DottedBare` with head = type head, body = unit name (datom.rs:428-435).
- `Entry::Note`: `Shape::Bare` (if bare-safe) or `Shape::DottedCurlyQuoted` with head `"Note"` (datom.rs:1122-1135).
- `Entry::Group`: `Shape::DottedBraced` with head `"Group"` (datom.rs:1137-1146).
- `Entry::Tags`: `Shape::DottedSquareBracketed` with head `"Tags"` (datom.rs:1148-1159).

### How nesting/recursion works

`TextualizeScope::textualize_block` (walk.rs:727-784):
1. If position != 0, emits `" "` (one space separator between siblings).
2. Emits head + `"."` if present.
3. Looks up delimiters from shape; emits opening delimiter.
4. Calls `self.driver.enter(shape, start..start)` to push a new frame onto `StructuralWalk`.
5. Calls the dialect closure, which recursively calls `textualize_in` on children (each of which calls `textualize_block` again).
6. On Ok: emits closing delimiter, finishes the frame span, calls `close()` + `resume()`.
7. On Err: finishes span, closes, and marks the walk faulted.

### How indentation/layout is decided

There is no indentation. Canonical output is flat: one space between sibling blocks (walk.rs:743-745). No newlines are emitted.

### Leaves vs. compounds

Leaves (scalars) call `scope.emit_scalar(text)` inside a `textualize_block` closure. Compounds call `child.textualize_in(body)` for each child, which opens nested blocks. The distinction is purely in the `DatomTextualizing` implementation of each type.

## 4. Realize pipeline (text-to-real)

### Entry points

1. **`DatomRoot::realize_source(source: &SourceText) -> Result<Self, DatomFault>`** (datom.rs:280-290): creates a `RealizeWalk`, calls `walk.realize_source(source, |scope, block| Self::realize_block(scope, block))`, expects exactly 1 result.
2. **`DatomText<T>::realize() -> Result<T, DatomFault>`** (datom.rs:315-321): delegates to `T::realize_source`.
3. **`EvidencedRealizing::realize_evidenced`** (e.g. datom.rs:1317-1337 for `ReportText`): same pattern, returns `Realized<T>` with walk observation.
4. **`Realize::realize()` for `SourceText`** (block.rs:111-118): returns `Vec<Block>` -- raw blocks, no Datom interpretation.

### Scanning (first pass)

`BlockScanner::scan()` (block.rs:124-298): character-by-character lexer.
- Skips whitespace.
- Collects non-whitespace, non-delimiter runs as the prefix.
- If prefix ends with `.`, it becomes a `Head`; otherwise the whole prefix is a bare atom body.
- On seeing an opening delimiter (`(`, `"`, `[`, `<<`, `{`), constructs the appropriate block with shape, body (text between delimiters), and string carrier.
- Delimiter scanning is split into three methods: `parenthesized` (depth-tracking `()`), `curly_quoted` (flat `"..."`), and `structural` (generic, handles nested balanced delimiters `{}`, `[]`, `<<>>` by pushing closers onto a stack, and delegates to `parenthesized`/`curly_quoted` when those openers appear inside).

### Walk-driven realization (second pass)

`RealizeWalk::realize_source` (walk.rs:592-621):
1. Resets history, enters a root `Shape::Bare` frame.
2. Creates a `RealizeScope` with the full source.
3. Calls `scope.realize_body(dialect)`.

`RealizeScope::realize_body` (walk.rs:624-661):
1. Scans `self.body` into blocks via `BlockScanning::blocks()`.
2. For each block: rebases spans to root source, enters a frame for the block's shape, creates a child `RealizeScope` with the block's body, calls the dialect closure.
3. On Ok: closes frame, resumes parent, advances cursor.
4. On Err: closes frame, faults the walk.

The dialect closure dispatches on shape + head via `ShapeDefined::select`, then calls the type-specific `DatomRealizing::realize_block`. Records use `RecordPosition` to track positional fields.

### Error handling

- Protos errors: `WalkFault` enum (`UnexpectedCloser`, `UnclosedBlock`, `InvalidHead`, `FaultedWalk`).
- Datom errors: `DatomFault { problem: DatomProblem }` with variants `Shape`, `Head`, `Value`, `Path`, `Position`, `ExtraPosition`, `MissingPosition`, `AmbiguousMapPair`, `Protos(WalkFault)`.
- `WalkFault` converts to `DatomFault` via `From`.
- Once faulted, a walk refuses all further operations (`FaultedWalk`).

### Symmetry with textualize

The pipelines are structurally symmetric:
- Both use the same `StructuralWalk` frame discipline (enter/close/resume).
- Both use scoped handles (`RealizeScope` / `TextualizeScope`) that prevent raw walk mutation.
- Both dispatch per-type: `DatomRealizing::realize_block` mirrors `DatomTextualizing::textualize_in`.
- `DatomRoot` provides default `realize_source` / `textualize_source` that are each other's inverse.

Asymmetry: `Textualize` (Protos trait) is infallible (`fn textualize(&self) -> Self::Textual`) while `Realize` is fallible. But at the Datom level, `DatomTextualizing::textualize_in` returns `Result<(), DatomFault>`, and the Protos-level `Textualize` impl for `Report`/`InterimNote` wraps that in `Result<ReportText, DatomFault>` (datom.rs:1421-1435). So in practice both directions are fallible at the Datom level.

## 5. Callers

| Caller | Path | Usage |
|---|---|---|
| **orchestrate CLI** | `/git/github.com/LiGoldragon/orchestrate/src/bin/orchestrate.rs` | `DatomText::<OrchestrateRequest>::from(SourceText(text)).realize()` -- parses CLI input as Datom |
| **signal-orchestrate** (generated) | `/git/github.com/LiGoldragon/signal-orchestrate/src/generated/signal.rs` (746 lines, 78 DatomRealizing/DatomTextualizing impls) | All Orchestrate wire types (locks, operations, etc.) implement `DatomRealizing`/`DatomTextualizing` via ethos-monolith code generation |
| **curriculum-deploy** | `/git/github.com/LiGoldragon/curriculum-deploy/src/runtime.rs` | `CurriculumRequest` and `Configuration` types with hand-written `DatomRealizing`/`DatomTextualizing` impls |
| **ethos-monolith** (code generator) | `/git/github.com/LiGoldragon/ethos-monolith/src/fixture/mod.rs` | Generates `DatomRealizing`/`DatomTextualizing` impls for Ethos-declared types. Emits Rust source strings containing newtype delegations, positional record realize/textualize, and enum variant dispatch. Template at lines ~1532-1921. |
| **signal-spirit** (generated) | `/git/github.com/LiGoldragon/signal-spirit/src/schema/spirit/generated.rs` | Generated Datom impls for Spirit wire types |
| **meta-signal-spirit** (generated) | `/git/github.com/LiGoldragon/meta-signal-spirit/src/schema/meta/generated.rs` | Generated Datom impls for meta-Spirit wire types |

## 6. Tests

| Test file | Line count | Coverage |
|---|---|---|
| `datom/tests/substrate.rs` | 390 lines | Deep report round-trip with evidence checking, curly-quote string carriers, headed delimited strings, optional bare/delimited forms, parenthesized string rejection, map key duplicate/arity errors, unrecognized head rejection |
| `datom/tests/external_surface.rs` | 329 lines | External `Request`/`Serve` enum+struct realize and textualize round-trip, integer canonical form (+reject non-canonical), `DatomHeadedUnit` for `Observe.Locks` |
| `protos/tests/substrate.rs` | 1005 lines | Block scanning, structural walk transitions, realize/textualize block round-trips, recursive and sibling fixtures, walk evidence, ShapeDefined dispatch, cursor observations |
| `signal-orchestrate/tests/generated_contract.rs` | unknown | Generated contract tests |
| `ethos-monolith/tests/interface_fixture.rs` | unknown | Fixture tests for generated interface |

## 7. Observed oddities

### Delimiter table duplication

The delimiter mapping (shape to opening/closing character pair) appears in three places:
1. `BlockRendering for Block` (block.rs:54-65) -- used only for `Block::textualize()`.
2. `TextualizeScope::textualize_block` (walk.rs:751-758) -- used by the walk-driven textualize pipeline.
3. `BlockScanner::scan` (block.rs:136-298) -- the realize-direction scanner, which matches delimiter characters directly in `match` arms.

The first two are identical shape-to-delimiter maps. The scanner encodes the same knowledge implicitly through its character matching. If a shape's delimiters changed, all three would need updating.

### `Block::textualize()` vs. walk-driven textualize

`Block` has its own `impl Textualize for Block` (block.rs:67-86) that directly concatenates head + delimiters + body into a `SourceText`. This is separate from the walk-driven `TextualizeWalk::textualize_blocks` (walk.rs:664-683), which goes through the full scope discipline. Both produce the same output for a flat block, but the `Block::textualize()` impl does not participate in the walk's frame discipline or transition history.

### Guillemeted shape has no dotted variant

Nine of the eleven shapes come in dotted/undotted pairs. `Guillemeted` (`<<...>>`) is the exception: it has no `DottedGuillemeted`. The scanner explicitly rejects `dotted` for guillemets (block.rs:227-229, `return Err(WalkFault::InvalidHead)`). This is deliberate, but asymmetric with the other structural shapes.

### `fits_bare` re-parses text

`BareProjecting for Text` (datom.rs:533-546) checks whether a `Text` value can safely be emitted bare by round-tripping it through `SourceText::blocks()`. This is a parse-and-check rather than a character-class predicate. Effective but not the cheapest path.

### `text_key` and `group_key` also re-parse

`MapKeyChecking` (datom.rs:563-616) constructs synthetic `SourceText` strings and parses them to check that a key won't be ambiguous. Same re-parse pattern as `fits_bare`.

### No indentation in canonical output

The textualize pipeline emits flat output with single-space separation. No newlines, no indentation. The only layout rule is "one space between sibling blocks" (walk.rs:743-745). Input whitespace (including newlines and multi-space runs) is consumed and discarded on realize.

### Ethos-monolith generates Datom impls as string-concatenated Rust

The code generator in `ethos-monolith/src/fixture/mod.rs` (~lines 1532-1921) constructs `DatomRealizing` and `DatomTextualizing` impls by pushing Rust source fragments into a `String`. It is template-style generation, not macro or derive based.

### No datom-syntax skill found

No file named `*datom*` exists under `Curriculum skills/`. The syntax rules are encoded entirely in the Rust source of `protos` (scanner) and `datom` (type dispatch). The earlier witness at `flows/ac1e9ec8/witnesses/datomCurrentSyntax.md` describes the same syntax from a prior code read.

### i64 support present despite earlier witness

The witness from flow ac1e9ec8 (datomCurrentSyntax.md, line 114) states "Not implemented in datom or protos. No numeric DatomRealizing impl exists." This is now incorrect: `datom.rs:336-371` contains `CanonicalInteger`, `DatomRealizing for i64`, and `DatomTextualizing for i64`. The tests in `external_surface.rs:271-308` exercise this. This was added after that witness was written.

## Sources

- protos v0.8.0: `/git/github.com/LiGoldragon/protos/`
- datom v0.5.0: `/git/github.com/LiGoldragon/datom/`
- signal-orchestrate generated: `/git/github.com/LiGoldragon/signal-orchestrate/src/generated/signal.rs`
- orchestrate CLI: `/git/github.com/LiGoldragon/orchestrate/src/bin/orchestrate.rs`
- curriculum-deploy: `/git/github.com/LiGoldragon/curriculum-deploy/src/runtime.rs`
- ethos-monolith code generator: `/git/github.com/LiGoldragon/ethos-monolith/src/fixture/mod.rs`
- Vision record: `/home/li/primary/Vision/datom.md`
- Prior witness: `/home/li/primary/flows/ac1e9ec8/witnesses/datomCurrentSyntax.md`
