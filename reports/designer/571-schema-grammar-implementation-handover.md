# 571 — schema-next grammar spec: implementation handover

designer, 2026-06-09. **Read this first if you are implementing the schema-grammar
spec with no prior conversation context.** It is self-contained: this file + the
review (`570`) + the four Spirit records + the cited code is everything you need.
The psyche has greenlit implementation ("implement it"). Work the steps in order;
they are sequenced by blast radius.

## What this is

Four schema-grammar improvements for **`schema-next`** (the NOTA grammar/AST
crate, `/git/github.com/LiGoldragon/schema-next`) and its Rust emitter
**`schema-rust-next`** (`/git/github.com/LiGoldragon/schema-rust-next`). Captured
as Spirit records — verify each with `spirit "(Observe (RecordIdentifiers ((Exact [52ro]) SummaryOnly)))"` (and `yp29`/`qz6j`/`lm84`); query syntax in `skills/spirit-cli.md`:

- **`52ro`** — the enum-variant grammar gains three compact forms that kill
  tag==type repetition: `(X)` ≡ `(X X)`; `(X { field Type … })` declares the
  variant **and** registers struct `X` in the namespace; `(X [ … ])` declares the
  variant **and** registers enum `X` in the namespace.
- **`yp29`** — add a `Bytes` primitive (+ ideally fixed-size). Binary values
  (keys/sigs/digests/fingerprints/nonces) are bytes, not `String`. Current
  primitives: `String`/`Integer`/`Boolean`/`Path`.
- **`qz6j`** — the bare form `Name Type` declares a distinct **newtype**, not the
  non-distinct alias it produces today. Aliases drop, or survive only as an
  explicit rare marked form.
- **`lm84`** — a hash-identifier type: bytes domain value with a canonical
  string-encoding NOTA projection (generalizes Spirit's `RecordIdentifier`).

## Current state (already done — do not redo)

- **The dead `syntax.rs` path is removed** (the `SyntaxSchema`/`SyntaxDeclaration`
  layer — it was NOT on the live lowering path; only a test + re-export used it).
  Deleted: `src/syntax.rs`, the `mod syntax;` + `pub use syntax::{…}` in `lib.rs`,
  `tests/syntax_layer.rs`, `tests/fixtures/syntax-layer/`. schema-next builds +
  all tests pass.
- **Committed on jj branch `schema-grammar-spec`** (bookmark at `f301636a`, based
  on schema-next `main` = `xkvtpkzk`/`77e71a41`). Keep working on this branch.
- **Do NOT touch** the live `ExpectedSyntax*` variants of `SchemaError`
  (`engine.rs` ~139-145) — same substring, different thing; they are live.

## The single most important grounding fact

**There are two parse paths; the live one is `SchemaSource`, not `syntax.rs`.**
The earlier spec drafts cited `syntax.rs` lines — that module is now deleted as
dead. All real edits target the live triad:
- `engine.rs` — `lower_schema_source` (~323); **`lower_newtype` (~652) — which,
  despite its name, returns `TypeDeclaration::Alias` today** (this is the qz6j
  site).
- `source.rs` — `to_schema`; `SourceDeclarationValue::to_declaration_group`
  (~502-505, the Alias construction → qz6j); the struct/enum/reference
  delimiter split (~455-472); `SourceVariantSignature` (~1002, the `#[shape]`
  variant derive → 52ro); `TypeReference::from_name` (~1364) + reserved
  parenthesis heads `Vec`/`Optional`/`Map` (~1317, where `Bytes`/`(Bytes N)`
  attach → yp29).
- `declarative.rs` — `MacroExpansionVariant` (~1848-1898) and
  `MacroExpansionField::inline_declaration` (~1745-1764, the working precedent:
  it already dispatches `Brace`→struct / `SquareBracket`→enum / else→newtype at
  *field* position; 52ro applies the same at *variant* position).
- `macros.rs` — `enum_variants()` (~432-509), the declarative `MacroNodeDefinition`
  the nota-next dispatcher consumes.
- Emitter (`schema-rust-next/src/lib.rs`) — `RustNewtype` / `NewtypeInherentImplTokens`
  (~830/1685/3071); the newtype struct emission at **~3113** (the pub-field bug,
  Issue B below); primitive recognition (~8 sites for `Bytes`).

## Implementation steps (in order)

### Step 1 — `52ro` compact variant forms  [additive · zero forced regen · do first]

`SourceVariantSignature` (`source.rs:1002`) is a `#[shape]`-derived structural
macro:
```
#[shape(pascal_atom)]           Unit(SourceVariantName)                       // X
#[shape(pascal_head, arity=2)]  Data(SourceVariantName, SourceVariantPayload) // (X Type)
#[shape(pascal_head, arity=4)]  Streaming(name, payload, keyword, name)       // (X Type opens S)
```
- **`(X)` self-tag:** add an `arity = 1` `pascal_head` case (e.g. `SelfTagged(SourceVariantName)`)
  that lowers to a variant whose payload is a reference to the same-named type.
  No existing case uses arity-1 in variant position, so it slots in. **VERIFY
  FIRST** that the `StructuralMacroNode` derive (in `nota-next-derive`) supports
  `arity = 1` — the review inferred this from the existing attributes but did not
  confirm it against the derive's parser. If it does not, that derive needs the
  arity-1 shape added.
- **`(X {…})` / `(X […])` inline body:** these are `arity=2` like `Data`, so they
  collide in arity and must disambiguate on the **second element's delimiter**.
  Note `SourceVariantPayload` already has a `Declaration` arm (not just
  `Reference`) — check whether it already *parses* an inline brace/bracket body;
  the gap is likely the **lowering that hoists** the inline struct/enum into the
  namespace as a top-level declaration named `X` (find where `to_schema` collects
  `SourceNamespace` declarations and add the hoisted one). Mirror
  `MacroExpansionField::inline_declaration` (declarative.rs:1745).
- **Hazard:** the existing `Data` case captures its payload with `PatternElement::any`,
  which will swallow `(X {…})` before a new case is tried unless you order the
  brace/bracket cases first or tighten `Data`'s payload shape. The conflict guard
  `silently_shadows` (nota-next `macros.rs` ~879-921) only catches
  Pascal-head-shadows-Literal-head — it will NOT catch this same-arity overlap, so
  **add an explicit ordering test**, and ideally extend `silently_shadows` to flag
  same-arity payload-delimiter overlap.
- **Verify:** `cargo build && cargo test` in schema-next; add a round-trip test
  using the new forms; confirm an unchanged schema still lowers byte-identically.
- **Payoff:** collapses criome's ~15 `(Authorization… Authorization…)` self-tags
  to `(Authorization…)`; lets new authors use the compact forms.

### Step 2 — newtype pub-field fix  [`schema-rust-next` emitter · forces regen of ~15 · do its own sweep]

`schema-rust-next/src/lib.rs:3113` emits `#visibility struct #name(#visibility #reference);`
— the inner field inherits the type's visibility, so every public newtype gets a
public `.0`, violating wrapped-field-is-private (`skills/rust/methods.md`). Change
to a **private** wrapped field; the already-emitted `new`/`payload`/`into_payload`
accessors are the access path. This regenerates every contract's newtypes (`.0` →
`payload()`), so land it as its own clean sweep **before** qz6j multiplies
newtypes — do not tangle it with the qz6j semantic flip. (~15 building contracts;
see list below.)

### Step 3 — `yp29` `Bytes` primitive + canonical hex codec  [additive]

- Add `Bytes` as a fifth scalar leaf. ~8 coordinated sites: in `schema-next`
  `schema.rs` — `TypeReference` variant (~832), `from_name`, `scalar_name`,
  `is_reserved_scalar_name`, both NOTA arms; in `schema-rust-next` — `to_tokens`,
  `references_private_type`, `collect_map_keys`, `rust_type`, `default_aliases`.
- **CRITICAL:** `Bytes` must **not** emit as `type Bytes = Vec<u8>`. The blanket
  `Vec<Element>` NOTA codec (nota-next `codec.rs` ~697-713) renders `Vec<u8>` as
  `[1 2 3 …]` — the exact wart this kills — and the orphan rule blocks a custom
  `NotaEncode` on an alias. Emit it as a **newtype-scalar carrying its own
  `NotaEncode`/`NotaDecode`** that projects to a single lowercase-hex bracket
  string (NOTA has no quoted strings, so the projection is mandatory or
  `expect_fresh` breaks the instant a field is retyped). Hex is exact-roundtrip,
  case/width fixed → dedup/equality stays on the bytes.
- Then migrate the **4 live `(Vec Integer)`-as-bytes sites** (`meta-signal-upgrade/lib.schema:22`,
  `signal-terminal/lib.schema:50-53`) and criome's ~5 `{ value String }` binary
  fields, each a scoped single-contract wire change with a known consumer.
- **Defer `(Bytes N)` fixed-size** unless a pilot needs it now; when needed,
  special-case a `(Bytes N)` reserved head (the grammar's first numeric type-arg —
  mirror how `Map` is special-cased; do NOT add general const-generics).

### Step 4 — `lm84` hash-identifier  [additive · downstream of qz6j + Bytes]

A fixed-width parameterization of the Step-3 codec. Reviewers converged on
**marker-on-a-bytes-newtype**, not a new primitive (a primitive is a closed
parameterless scalar; it can't carry width + codec) — confirm with psyche.
Template: `RecordIdentifier` (`signal-spirit/src/lib.rs:210-258`) = `struct([u8;12])`
+ a separate base36 code + a NotaString projection. **Correction:** base36
shortest-unique-prefix is *display truncation*, not roundtrippable — use the
canonical hex codec from Step 3, not base36, for storage. Pilot in ONE contract
(criome `ObjectDigest`/`PublicKeyFingerprint`) before fleet adoption. (Migrating
Spirit's hand-written `RecordIdentifier` onto this is its own later contract
migration — not a freebie.)

### Step 5 — `qz6j` bare-form → newtype, SCOPED  [fleet regen · LAST · psyche-gate the sweep]

Sites: `engine.rs:652` (`lower_newtype`) + `source.rs:503`
(`SourceDeclarationValue::to_declaration_group`). **NOT a blunt flip.** A blunt
flip reinterprets ~1068 bare aliases, of which only ~306 are alias-over-primitive
(the intended wins) and **~762 are alias-over-declared-type re-exports**
(`State Statement`, `RecordAccepted SemaReceipt`) that MUST stay transparent —
wrapping them breaks every `Statement`-where-`State`-expected site across the
fleet.
- **Rule:** convert to `NewtypeDeclaration` only when the reference resolves to a
  **reserved scalar** (`String`/`Integer`/`Boolean`/`Path`/`Bytes`); leave
  alias-over-declared-type transparent (`AliasDeclaration`).
- Decide the **fate of aliases** that remain (the declared-type re-tags): keep the
  `Alias` declaration for them, or require an explicit `(Alias X)` reserved head
  (composes cleanly as a fourth reserved parenthesis head). The 762 mean
  alias-over-declared-type is *common*, so do not drop it globally.
- Update the pinning test `tests/lowering.rs:73`
  (`bare_reference_declarations_lower_to_aliases`).
- Then regen the ~15 building contracts + patch value-flow in **one coordinated
  sweep** — checked-in `src/schema/*.rs` + the `write_or_check` build gate means a
  half-landed qz6j red-lights every gated build at once. This is the one
  fleet-forcing change; confirm with the psyche before the sweep.

## The ~15 schema-rust-next-building contracts (regen scope for Steps 2 & 5)

`meta-signal-cloud`, `signal-cloud`, `upgrade`, `signal-domain-criome`,
`meta-signal-orchestrate`, `meta-signal-upgrade`, `meta-signal-router`,
`signal-criome`, `signal-upgrade`, `signal-orchestrate`, `signal-terminal`,
`signal-router`, `meta-signal-domain-criome`, `signal-message`, `agent`. (Count is
a `*/build.rs` glob estimate — verify before the sweep.)

## Debunked non-issues (do not chase these)

- "~29 repos regenerate" — it's **~15** (the list above).
- "the agent triad needs a rewrite" — **no**: `signal-agent`/`meta-signal-agent`
  are hand-written `signal_channel!` with no `schema-rust-next` dep. Their
  `(RequestUnimplemented RequestUnimplemented)` is a **manual one-line edit** to
  `(RequestUnimplemented)` *after* 52ro ships the form — not a regen. (Only the
  `agent` daemon repo builds from schema.) Migrating the agent triad onto
  schema-next is a separate, out-of-scope decision.
- "criome uses `Vec<Integer>` for bytes" — **false**; criome's binary fields are
  `{ value String }` newtypes (fixed by Step 3's String→Bytes retype). Only 4
  live `(Vec Integer)`-as-bytes sites exist (named in Step 3).
- "`(X)` collides with the unit schema-node meaning" — position-scoped (variant
  vs type-reference position); a conscious decision, not a blocker.

## Open decisions for the psyche (confirm before/while building)

1. Canonical byte→text codec = lowercase hex (recommended). base36-shortest-prefix
   stays Spirit's *display* nicety only.
2. Fixed-size bytes via a `(Bytes N)` reserved head (recommended) vs un-enforced
   newtype convention.
3. Hash-id = marker-on-bytes-newtype (recommended) vs new primitive.
4. Alias fate = scalar→newtype, declared-type→stays-transparent (or `(Alias X)`
   marker). Not a global drop.
5. Confirm the newtype pub-field fix (Step 2) lands — it changes `.0` → `payload()`
   for all generated newtypes.

## Consumer follow-ups (after the grammar lands)

- **signal-criome:** `DaemonPath`→`Path`; `BlsPublicKey`/`BlsSignature`→`Bytes`
  (or hash-id); `PublicKeyFingerprint`/`ObjectDigest`→hash-id; `ReplayNonce`→
  `Integer` (if a counter) or `Bytes` (if random — check criome's generation
  before deciding); the `(Authorization… Authorization…)` variants → `(Authorization…)`.
- **agent** (`signal-agent`): `(RequestUnimplemented RequestUnimplemented)` →
  `(RequestUnimplemented)` (manual edit; hand-written contract).

## Discipline & verify loop

- Before authoring Rust, read `skills/rust-discipline.md` + its sub-files +
  `skills/abstractions.md` (the PreToolUse hook enforces this).
- Verify: `cd /git/github.com/LiGoldragon/schema-next && cargo build && cargo test`.
  For emitter changes, regenerate a sample contract with its
  `<NAME>_UPDATE_SCHEMA_ARTIFACTS=1 cargo build` then `cargo test`.
- VCS: jj, on branch `schema-grammar-spec`; inline `-m` commits only (never an
  editor); do not push `main` of a code repo (operator integrates) unless the
  psyche says to land it. Keep each step its own commit.

## Coordination — another lane is in this emitter NOW

As of this handover, the **system-designer** lane is actively working
`schema-rust-next` newtype emission — primary `main` carries `system-designer 85:
schema-rust-next emits new(impl Into<String>) for string newtypes`. Step 2 (the
newtype pub-field fix at `schema-rust-next/src/lib.rs:3113`) and Step 5 (`qz6j`,
which mass-produces newtypes) touch the **same emitter surface**. Before editing
newtype emission, read `reports/system-designer/` + recent `schema-rust-next`
history and coordinate through the lane locks (`orchestrate/`) — do not collide on
`lib.rs` newtype token emission. (Their `new(impl Into<String>)` work may already
overlap the accessor side of the pub-field fix.)

## Pointers

- **Review (read it):** `reports/designer/570-schema-grammar-spec-review.md` — the
  grounded per-decision verdict, the four load-bearing issues, the full ordering
  rationale.
- Agent component (the motivating consumer, on main): `reports/designer/569`.
- Spirit query/record: `skills/spirit-cli.md`. The four records: `52ro` `yp29`
  `qz6j` `lm84`.
- Residual uncertainty (from the review): the `#[shape] arity=1` support is
  inferred not verified; the `~15` count is a glob estimate; the test suites were
  not run end-to-end. Verify these early.
