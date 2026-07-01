# NOTA Schema Machinery Audit — deviations from canonical NOTA

## Task and scope

Read-only audit (no edits to any code, schema, or test). Goal: find every place
the schema **machinery** (`schema-next` schema language + `schema-rust-next` code
generator) adds behavior on top of canonical strict-positional NOTA, or bypasses
the canonical codec — beyond the one already-known optional-positional bug. Output
is a classified inventory plus an isolated-vs-pattern verdict.

The `nota-next` structural derive machinery (`#[derive(nota::NotaEncode/Decode)]`,
`StructuralMacroNode`) is treated as the **reference for canonical NOTA**, not as a
defect.

## Canonical baseline (the reference "correct")

From `nota-next/src/codec.rs` and `nota-next/derive/src/lib.rs`:

- **Enum (derive), decode `nota-next/derive/src/lib.rs:401-462`, encode `:464-493`**
  - unit variant -> bare atom `Tag`
  - single-payload variant -> `(Tag <payload-nota>)` (exactly 2 body objects)
  - multi-field payload -> `(Tag (f0 f1 …))`
  - decode: a bare atom only matches **unit** variants; a payload variant name as a
    bare atom falls through to `UnknownVariant`. Payload variants are only reached
    inside the 2-object parenthesis branch.
- **`Option<T>` codec `nota-next/src/codec.rs:939-958`** (hand-written generic, not
  per-type): `None` -> bare atom `None`; `Some(x)` -> `(Some <x>)`. It **never**
  emits a bare-atom `Some`. Decode (`parse_option` `:584-608`) accepts only bare
  `None` or a 2-object `(Some x)`.
- **String `:456-521`** rejects redundant delimiters (`reject_redundant_delimiter`)
  — strict; a bracketed string that could be a bare atom is a decode error.
- Booleans are `True`/`False`; integers/floats are bare atoms.

Net baseline: an `Optional T` value has exactly one canonical NOTA form,
`None` | `(Some x)`, regardless of the position it occupies.

## Files and commands consulted

- `nota-next/src/codec.rs`, `nota-next/derive/src/lib.rs` (baseline).
- `schema-rust-next/src/lib.rs` (codegen; anchor region 4802-5196, derive-attr logic
  1930-2002, enum-shape helpers 1512-1576, scope-model 4330-4402).
- `schema-rust-next/src/daemon_emit.rs`, `build.rs`, `migration.rs`.
- `schema-next/src/declarative.rs` (reference lowering 1543-1593),
  `schema-next/src/schema.rs` (arity verification 810-859),
  `schema-next/src/instance.rs` (schema-text projection),
  `schema-next/src/upgrade.rs` (migration `SetDefault`).
- greps: `impl nota::Nota` emit sites, derive-attribute lists, `Optional` handling,
  default-injection signals (`unwrap_or*`, `default()`, `SetDefault`).

Observed structural fact (the frame for everything below): the **only** hand-rolled
`impl nota::Nota*` emitted anywhere in the generator is `RustOptionalEnumNotaTokens`
(`schema-rust-next/src/lib.rs:4946-5194`). Every other struct / newtype / enum /
scope-enum / map type is emitted with the canonical
`#[derive(nota::NotaDecode, nota::NotaDecodeTraced, nota::NotaEncode)]`
(`lib.rs:1964,1968,6087,6091,6137,6141`). `daemon_emit.rs` emits **no** NOTA at all
(daemon boundary is rkyv/typed). So the entire NOTA-deviation surface is concentrated
in one mechanism.

## Findings

### F1 — Bespoke per-enum NOTA codec replaces the canonical derive (the mechanism)
- Evidence: `schema-rust-next/src/lib.rs:4822-4826` (gate: emitted when
  `has_optional_payload_variant()` and `nota_surface.emits_nota()`),
  `:4829-5196` (`RustOptionalEnumNotaTokens`), derive suppression at `:1935` and
  `:1943` (`!enumeration.has_optional_payload_variant()` passed as `includes_nota`).
- Deviation: whenever any variant payload is `(Optional T)`, the generator stops
  delegating to the canonical derive and hand-writes `NotaBodyDecode` / `NotaDecode`
  / `NotaBodyEncode` / `NotaEncode` / `NotaDecodeTraced` for the whole enum. This is
  hand-rolled per-type encode/decode logic layered on the generic codec, matching a
  specific `TypeReference::Optional` shape in the emit path.
- Classification: `needs-psyche-judgment` — the doc comment (`:4842-4848`) shows it
  is deliberate "optional-leaf" sugar, not an accident. Whether the workspace
  sanctions a bespoke codec that diverges from the derive is a design call. Its
  concrete behaviors below are defects against the canonical baseline.

### F2 — Silent omission of the payload component + atom demotion on encode
- Evidence: `schema-rust-next/src/lib.rs:5100-5108` (encode arm for
  `Some(TypeReference::Optional(_))`).
- Deviation: `Variant(None)` encodes as the **bare atom** `Variant` (the payload
  object is dropped entirely); `Variant(Some(x))` encodes as `(Variant <x>)` — the
  `(Some …)` wrapper is stripped. Canonical would emit `(Variant None)` and
  `(Variant (Some x))`. Two of the named "fuckery" classes at once: silent omission
  of a variant component (the `None` case loses its object) and atom
  coercion/demotion (the `Some` wrapper is demoted away).
- Classification: `defect` — breaks canonical round-trip compatibility; a canonical
  reader/writer of the same logical type disagrees on the bytes.

### F3 — Positional inconsistency: one `Optional` type, two NOTA encodings
- Evidence: variant-payload path `lib.rs:5077-5081` / `:5100-5108` vs the canonical
  `Option` codec used for every non-variant-payload position
  (`nota-next/src/codec.rs:948-958`, reached through the derive for struct fields,
  vector elements, map values, and the **inner** element of a nested
  `(Optional (Optional T))`).
- Deviation: the identical schema construct `(Optional T)` renders as `(Some x)` /
  `None` in a struct-field / vector / map / nested-inner position, but as `x` /
  bare-atom in a variant-payload position. In `(Optional (Optional T))` the two
  encodings appear side by side in one value: outer collapsed, inner canonical.
  The wire form of `Optional` is therefore not uniform — position changes meaning,
  which the canonical model forbids.
- Classification: `defect`.

### F4 — Lenient acceptance + rejection of the canonical form (decode asymmetry)
- Evidence: `schema-rust-next/src/lib.rs:5060-5069` (`optional_unit_arms`: bare atom
  `Variant` -> `Self::Variant(None)`), `:5077-5081` (payload arm decodes
  `children[1]` as the **leaf type**, not as `Option`); traced mirror at
  `:4873-4896` and `:4898-4942`.
- Deviation:
  - Accepts a form the canonical grammar rejects: a bare atom naming a
    payload-carrying variant (canonical derive returns `UnknownVariant` for this).
  - Rejects / misreads the canonical form: the canonical `(Variant None)` and
    `(Variant (Some x))` are decoded by trying to parse `None` / `(Some x)` as the
    **inner leaf type** (not as `Option`), so canonical-encoded data fails to decode
    or is misinterpreted. Decode accepts a form encode never produces (bare `Variant`
    is only produced by this path, never by canonical) and refuses a form canonical
    encode does produce.
- Classification: `defect`.

### F5 — Missing schema-language validation permits `Optional` at variant payloads
- Evidence: lowering accepts `(Optional T)` in any reference position with no
  positional guard — `schema-next/src/declarative.rs:1559-1562`; arity verification
  treats `Optional(inner)` as always-valid and only recurses, with no
  variant-payload restriction — `schema-next/src/schema.rs:837-857`
  (`verify_enum_arities` -> `verify_reference_arities`).
- Deviation: the schema language has no rule that forbids (or even flags)
  `(EnumVariant (Optional T))`, which is exactly the shape that triggers F1-F4 in the
  generator. This is the "missing schema-language validation that permits the above
  to be expressed" class. The generator's `has_optional_payload_variant()`
  (`schema-rust-next/src/lib.rs:1523-1527`) then silently switches codecs with no
  diagnostic.
- Classification: `defect` (validation gap) — it is what makes the whole
  non-canonical path reachable.

## Notes on things that are NOT defects (checked, cleared)

- **Everything else uses the canonical derive.** The only bespoke `impl nota::Nota*`
  is F1. Structs, newtypes, map keys, scope enums, and unit/plain-payload enums all
  route through `#[derive(...)]` (`lib.rs:1964/1968/6087/6091/6137/6141`,
  `scope_enum_type_attributes` -> `derive_attributes(..., includes_nota=true)`).
  No reordering, no positional-vs-named confusion, no default injection found in the
  struct/newtype emit paths. `intended-machinery`.
- **`schema-next/src/instance.rs`** projects the decode trace to *schema text*
  (a human/diagnostic projection built from the codec's own captured
  `InstanceSchema`), not a value codec. No value-level deviation. `intended-machinery`.
- **Migration `SetDefault` (`schema-next/src/upgrade.rs:89,155-161,212-217`)** injects
  a field default, but only through the versioned `AddField` schema-edit / upgrade
  path (`apply_add_field`), i.e. a controlled, versioned migration consistent with
  `rust-storage-and-wire`. It is not a silent decode-time default. `intended-machinery`
  (contrast it deliberately with F2, which drops/injects with no version guard).
- **Scope `terminal_payload` / `is_optional_payload`
  (`schema-rust-next/src/lib.rs:4347,4384-4392`)** is scope-taxonomy generation, not a
  NOTA value codec; it does not itself emit a non-canonical value form.
  `intended-machinery` (but see residual risk).
- **`daemon_emit.rs`** emits no NOTA. `intended-machinery`.

## Verdict — isolated case or symptom of a pattern

**Structurally isolated, behaviorally a full pattern.** There is exactly one place in
the entire generator where "add logic on top of NOTA" happens: the
`RustOptionalEnumNotaTokens` mechanism (F1). The rest of the generator is disciplined
— it delegates to the canonical derive and does not hand-roll codecs, inject defaults,
reorder, or parse leniently. So this is **not** an epidemic of many independent
bespoke codecs.

However, that single mechanism is not a one-line typo either: it deliberately embodies
essentially the whole menu of NOTA-deviation symptoms at once — silent component
omission (F2), atom demotion of the `Some` wrapper (F2), position-dependent encoding of
one type (F3), lenient acceptance plus canonical-form rejection (F4) — and it is
reachable only because the schema language has no validation forbidding `Optional` at a
variant-payload position (F5). It is best read as a single intentional "optional-leaf
sugar" design decision that trades canonical uniformity for a shorter surface syntax,
guarded by nothing at the schema layer. The optional-positional bug is therefore one
mechanism with several distinct defect faces, not several unrelated bugs, and the
correct fix is a decision about that one mechanism plus a schema-language guard — not a
generator-wide sweep.

## Residual risks and unknowns

- **Cross-component wire drift (not exercised here).** If any consumer or stored value
  was produced by the canonical `Option` representation `(Variant (Some x))` /
  `(Variant None)` for a type that now hits F1, those bytes will not round-trip. I did
  not enumerate downstream persisted corpora; a storage/wire compatibility check on any
  enum with an optional payload variant is warranted before treating F2/F4 as
  cosmetic.
- **Scope enums with optional payloads.** `scope_enum_type_attributes` always requests
  the nota derive (it does not gate on `has_optional_payload_variant`), while `RustEnum`
  gates and swaps to the bespoke path. I did not confirm whether a generated *scope*
  enum can itself carry an `Optional` variant payload; if it can, the scope enum would
  get the *canonical* `(Some x)`/`None` form while the corresponding source enum gets
  the collapsed form — a second positional inconsistency. Flagged as an unknown to
  verify, not asserted.
- I did not run `cargo test`/`cargo build` (read-only audit; no check was named by an
  implementer). All findings are by source inspection with file:line evidence above;
  the round-trip claims follow from the canonical codec contract in
  `nota-next/src/codec.rs` versus the emitted arms cited.

## Provisional status

These are audit findings, provisional until psyche/psyche-owned guidance accepts them.
F1's classification in particular (`needs-psyche-judgment`) turns on whether the
optional-leaf sugar is a sanctioned design; F2-F5 are defects against the stated
canonical baseline regardless.
