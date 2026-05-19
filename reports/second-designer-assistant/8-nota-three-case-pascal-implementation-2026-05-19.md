# 8 — NOTA three-case PascalCase rule: codec + spec implementation

**Lane:** second-designer-assistant
**Date:** 2026-05-19
**Status:** three of four beads landed; primary-hj63 README portion landed, codec portion deferred to operator
**Beads addressed:** primary-x3xj (Bool as enum), primary-y4l4 (Option Some-wrapping), primary-r8vi (PascalCase forbidden at String), primary-hj63 (README rewrite)
**Audience:** designer (language-design authority), operator (cascade through nota-derive + consumer crates)

## TL;DR

Implemented the psyche's three-case PascalCase rule in nota-codec
and aligned the spec README + per-repo INTENT.md:

1. **`Bool` is an enum** — `True` / `False` PascalCase unit variants
   (case 3). The lowercase `true` / `false` keyword tokens are gone
   from the lexer; `Token::Bool` is removed from the Token enum.
2. **`Option<T>` is a normal enum** — bare `None` for absent (case
   3), `(Some inner)` for present (case 1). The Some-less carve-out
   is gone.
3. **PascalCase is forbidden at String positions** — bare
   PascalCase tokens at `String` schema positions return
   `Error::PascalCaseAtStringPosition`. PascalCase is variant
   territory only.
4. **README documents the three-case rule** — §Identifiers,
   §Optional values, §Bare-identifier strings, §Records, §Literals
   all rewritten. §Records names the struct-vs-variant distinction
   with an explicit implementation note pointing at primary-hj63 for
   the codec follow-up that drops the head from NotaRecord-derived
   structs.

All 112 cargo tests pass; `nix flake check` green. The `Path`
inner type was also swapped from `String` to `camino::Utf8PathBuf`
in the same session — the user surfaced that a "path datatype"
should actually be a path, not a string wrapper.

## Commits

| Repo | Commit | Description |
|---|---|---|
| `LiGoldragon/nota-codec` | `7954b070` | `Path` inner type → `camino::Utf8PathBuf` |
| `LiGoldragon/nota-codec` | `503f4754` | NOTA three-case rule: Bool enum, Option Some-wrap, PascalCase forbidden at String |
| `LiGoldragon/nota` | `0b0af8bb` | spec + INTENT.md: three-case rule, Bool, Option, §Records with hj63 note |
| `LiGoldragon/nota` | `ad14c35d` | example.nota: True / False for Bool |

## What landed in nota-codec (`503f4754`)

### `src/lexer.rs`
- Removed `Token::Bool(bool)` variant — Bool is no longer a
  distinct token kind. The lexer treats `True` / `False` as
  ordinary PascalCase idents.
- Removed the `"true"` / `"false"` keyword dispatch in
  `next_token`. The two lowercase strings (if they appear) become
  ordinary camelCase `Token::Ident("true")` / `Token::Ident("false")`
  and would decode as String content at a String position.

### `src/ident.rs`
- `Ident::is_bare_string` and `Ident::is_bare_path` exclude only
  the reserved literal `None` (the Option-absent sentinel).
  `"true"` and `"false"` are no longer reserved.

### `src/encoder.rs`
- `write_bool` emits `True` / `False` via `write_pascal_identifier`,
  not the lowercase keywords.
- `write_path` docstring updated to remove `true` / `false` from
  the reserved-literal list.

### `src/decoder.rs`
- `read_bool` matches `Token::Ident("True")` / `Token::Ident("False")`
  instead of the removed `Token::Bool` variant.
- `read_string` adds a PascalCase-rejection branch returning
  `Error::PascalCaseAtStringPosition` — runs before the existing
  bare-string-vs-path-shaped check so the most specific error
  surfaces first.

### `src/traits.rs`
- `Option<T>` encode/decode rewritten. Present writes
  `(Some inner)` via `start_record("Some") + value.encode + end_record`;
  absent stays bare `None`. Decode peeks for `None` first
  (existing logic), else `expect_record_head("Some") + T::decode +
  expect_record_end`. The big comment block describing the
  "explicit None always" rule and the "no implicit-None branch"
  history was kept and updated.

### `src/error.rs`
- New variant `Error::PascalCaseAtStringPosition { content: String }`
  with help text naming both remedies (quote, or use camelCase /
  kebab-case).

### Tests

| File | Updates |
|---|---|
| `tests/horizon_rs_feedback_fixes.rs` | `true` → `True` in wire fixtures; Option-present tests use `(Some "label")` / `(Some 42)`; `string_field_accepts_bare_pascal_identifier` inverted to `string_field_rejects_bare_pascal_identifier` with PascalCaseAtStringPosition error assertion |
| `tests/nota_record_round_trip.rs` | `Node { name: "User" }` → `"userName"` (PascalCase string content rejected) |
| `tests/nota_sum_round_trip.rs` | Same — `"User"` → `"userName"` |
| `tests/option_vec_struct_variant.rs` | Option-present wire fixtures wrapped as `(Some …)`; PascalCase string content (`Switch`, `Alice`, `G`) → camelCase (`switch`, `alice`, `g`) |
| `tests/path_round_trip.rs` | `string_position_still_accepts_strict_bare_idents` drops `"Foo"` from the loop; new test `string_position_rejects_bare_pascal_case` asserts the new error variant |

Test totals: 112 tests pass (up from 111; one test added). `nix flake check` green.

## What landed in nota (`0b0af8bb` + `ad14c35d`)

### `README.md`
- Header sentence: "one reserved literal (`None`)" instead of
  "no parser keywords beyond `true` / `false` / `None`".
- §Identifiers PascalCase rule: rewritten as the three-case rule.
  Removed the "`(Tag User)` works" example (no longer true).
- §Literals table: replaced `true` / `false → Bool` row with
  `True` / `False` (with "encoded as a two-variant enum" gloss);
  added `None` / `(Some inner) → Option<T>` row.
- §Optional values: rewritten for `(Some inner)` wrapping. Explicit
  example showing the three states. Note that omitted trailing
  optionals are a typed error, not a compatibility shape.
- §Bare-identifier strings: only camelCase / kebab-case bare. Plus
  the dedicated paragraph: "PascalCase is not bare-eligible at
  String positions" with the `PascalCaseAtStringPosition` typed
  error name.
- §Bare `Path` form excluded-content table: replaced
  `true / false / None` row with just `None`; added a row noting
  bare PascalCase content is forbidden (variant territory).
- §Records: rewritten to describe struct (no head) vs
  data-carrying enum variant (head). Added an explicit
  implementation note that the current codec emits a head for every
  NotaRecord-derived struct — tracked by primary-hj63 as the codec
  follow-up.
- §Canonical form: strings bare only when content is camelCase or
  kebab-case (not just any ident class); Options emit `(Some inner)`
  for present; tail omission removed as a compatibility shape.
- §Examples: `true` → `True` in the Sequences example and the
  every-literal sample.

### `INTENT.md`
- New top section: "The three-case PascalCase rule" naming the
  three cases canonically.
- New section: "Built-in types follow the rule" with `Bool` and
  `Option<T>` as concrete examples.
- Existing "Language shape" + "File shape" preserved.

### `example.nota`
- `(debug true) (strict false)` → `(debug True) (strict False)`.
- Header comment updated.

## What did not land — primary-hj63 codec change

The bead's full scope:
1. ✅ Investigate codec strictness — done.
2. ✅ Update README — done.
3. ❌ Relax codec — deferred.
4. (Workspace-lane) Update `skills/nota-design.md` — designer's
   lane, not touched here.

The codec change requires:
- `nota-derive` `NotaRecord` derive: emit `(` + fields + `)` instead
  of `(Name` + fields + `)`. Drop the `expect_record_head(name)` on
  decode; expect just `(` and `)`.
- `nota-derive` `NotaSum` derive: newtype variants must wrap with
  the variant name explicitly (currently rely on the inner's
  NotaRecord head to provide the name — that head won't exist
  after the relaxation). Encode: `(VariantName ` + inner.encode +
  `)`. Decode: `expect_record_head(variant_name)` + inner.decode +
  `expect_record_end`. This changes the wire form for newtype
  variants from `(Foo …)` (head = inner type name) to
  `(VariantName (…))` (head = variant name, inner is nested).
- Every consumer crate (`signal-persona`, `persona-router`,
  `persona-message`, `signal-criome`, `signal-core`, etc.) that
  uses `NotaRecord` will see its wire form change. Their tests and
  any persisted Sema/redb data need migration.

That cascade is operator-lane work, not second-designer-assistant.
The bead stays open against `role:operator` for that pass. The
spec is the contract; the codec will catch up.

## Decisions taken on judgment calls

1. **Hard-flip over deprecation period.** The beads said
   "decoder accepts both during a deprecation window (or hard-flip
   — psyche's call)". Per `ESSENCE.md` §"Backward compatibility is
   not a constraint" and §"A transitional shape compromises both
   the old and the new", hard-flip is the right default. If the
   psyche wants a deprecation window, the codec change is small
   enough to add one in a follow-up.

2. **Test fixtures rewritten in place, not duplicated.** No
   "compat" test that exercises the old wire form. The new wire
   form is the only form.

3. **Workspace fixtures swept lightly.** `repos/nota/example.nota`
   updated. The workspace `intent/*.nota` files have `true` /
   `false` only inside verbatim psyche-quote content (not as Bool
   literals), so they don't need migration. `skills/skills.nota`
   has no booleans.

4. **`Path` inner-type swap bundled with this arc.** The psyche's
   "why Buf?" question in mid-conversation drove the refactor from
   `Path(String)` to `Path(camino::Utf8PathBuf)`. Shipped as its
   own commit (`7954b070`) before the grammar changes so the test
   surface stayed stable through the alphabet rewrite.

## Open follow-ups

- `primary-hj63` codec change (operator-lane).
- `skills/nota-design.md` update to reflect the three-case rule
  (designer-lane). The skill currently says "Wrapping type names
  the most useful distinction" — that's compatible with the new
  rule; the gap is that the skill doesn't yet explain when there's
  no wrapping at all (struct case).
- `nota-derive` `NotaPath` derive — still deferred per report 7
  §10.3. The Option/Bool/PascalCase changes don't change that
  recommendation.

## See also

- `reports/second-designer-assistant/7-bare-path-type-nota-2026-05-18.md` — the prior `Path` type arc.
- `intent/nota.nota` — the 9+ psyche entries on NOTA grammar that drove this work.
- `repos/nota/README.md` (commit `0b0af8bb`) — the canonical spec.
- `repos/nota/INTENT.md` (commit `0b0af8bb`) — per-repo intent synthesis.
- `repos/nota-codec/src/{lexer,decoder,encoder,traits,ident,error}.rs` (commit `503f4754`) — the codec impl.
- `repos/nota-codec/tests/*` (commit `503f4754`) — the falsifiable test surface.
- BEADS: primary-x3xj, primary-y4l4, primary-r8vi (closed by this work); primary-hj63 (codec portion still open).
