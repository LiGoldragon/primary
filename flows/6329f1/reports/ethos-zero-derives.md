# ethos-zero derives, Meaning fix, and recursive-type Box emission

Flow 6329f1, subflow ethos-zero-derives.

## Changes landed

### 1. Library types now emit Clone, Debug, PartialEq, Eq derives

`type_declaration_tokens` and `emit_variant_tokens` both computed a `derive`
token stream conditioned on `signal: bool`. When `signal = false` (Library
root), the derive was an empty token stream — no derives were emitted for
Library structs, enums, or inline variant types.

Fixed: the Library branch now emits `#[derive(Clone, Debug, PartialEq, Eq)]`.
The Signal branch is unchanged (`Archive, RkyvSerialize, RkyvDeserialize,
Clone, Debug, PartialEq, Eq`). No `PartialOrd`/`Ord` are added; Signal
does not add them automatically.

### 2. Meaning intrinsic maps to datomic::Meaning (was datomic::MeaningValue)

`type_expression_tokens` had `"Meaning" => quote! { datomic::MeaningValue }`.
The type was renamed to `datomic::Meaning` in datomic commit `768426ea`.
Fixed to `datomic::Meaning`.

### 3. Recursive types emit Box and impl_datomic_box!

A type declaration (enum) whose variants include a position that directly names
the enclosing type (a bare `Named(name)` field, not wrapped in `Vector`, `Option`,
etc.) is recursive. In Rust, such a type has infinite size without pointer
indirection.

The emitter now:
- Detects direct recursive references in enum variants via `variants_have_recursive_ref`.
- Wraps those field positions in `Box<Type>` in the emitted struct/enum declaration.
- Emits `datomic::impl_datomic_box!(TypeName);` beside the enum, so `Box<Type>`
  gains `Corporal<Datom>` and `Datomic` impls (the datom is transparent).
- Threads the boxing context through inline struct/enum emissions and through
  `datomic_impl_tokens_with_boxing` so that `Corporal::incorporate` also uses
  `Box::new(T::incorporate(body)?)` for the recursive field.

The ethos file declares recursion plainly — no `Box` syntax required:
```
Query.[ Latest All Session.Text File.Text Grep.{ Query Text } ]
```
emits:
```rust
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct QueryGrep(pub Box<Query>, pub protos::Text);
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Query { Latest, All, Session(protos::Text), File(protos::Text), Grep(QueryGrep), }
datomic::impl_datomic_box!(Query);
```

### 4. datomic pinned to 0.9.0 (e4430bfe)

The datomic dependency is updated from 0.8.0 (`a27f9b8e`) to 0.9.0 (`e4430bfe`),
which provides `impl_datomic_box!` and `impl Datomic for Situated<F>`.

### 5. Generated self-bootstrap module regenerated

`src/generated.rs` is the output of emitting `ethos-zero.ethos`. The self-
description has no bare recursive refs (all recursive refs are inside `Vector<T>`,
which does not require `Box`), so the generated output does not change from the
derives fix. The bootstrap test passes.

### 6. Version bump: 1.1.0 → 1.2.0

Library type emission gained derived traits and recursive-type auto-boxing
(public behavior changes).

## Tests added

- `library_struct_emits_clone_debug_partialeq_eq_derives`: Library struct
  emits derive attributes without rkyv Archive.
- `library_enum_emits_clone_debug_partialeq_eq_derives`: Library enum same.
- `meaning_intrinsic_emits_datomic_meaning`: Meaning type maps to
  `datomic::Meaning` in emitted Rust.
- `recursive_enum_emits_box_and_impl_datomic_box`: Recursive enum emits
  `Box<Type>` and `impl_datomic_box!`.
- `fixture_library_meaning_round_trips_in_e2e`: e2e compile test with
  `(a meaning)` → `Meaning::Plain` → back; `Note(author, meaning)` round-trip.
  Also tests `Query` recursive round-trips: `Latest`, `All`, `Session.x`,
  `File.x`, `Grep.{ Latest foo }`, and double-nested `Grep.{ Grep.{ All inner } outer }`.

## Derive line for a Library struct

From a Library root, a struct emits:

```
# [derive (Clone , Debug , PartialEq , Eq)] pub struct Name ( ... ) ;
```

## Witness

- `nix flake check --builders 'ssh://prometheus'` run on worktree at
  `/home/li/wt/github.com/LiGoldragon/ethos-zero/ethos-zero-derives-6329f1`.
  Remote builder unreachable; fell back to local build. All 7 checks passed:
  `build`, `test`, `fmt`, `clippy`, `doc`, `deps`, `source`.
- 46 non-network tests pass in `cargo test --test file_contract`.
- origin/main advanced to `8bcb0b9402fb`.

## Sources

- `/home/li/primary/flows/6329f1/reports/api-deviations.md` — port findings
  identifying the Library-derives and MeaningValue gaps.
- `/home/li/wt/github.com/LiGoldragon/ethos-zero/ethos-zero-derives-6329f1/src/lib.rs`
  — emitter source.
- `/git/github.com/LiGoldragon/datomic` rev `e4430bfe` — `impl_datomic_box!`
  macro and `datomic::Meaning` type.
- `/git/github.com/LiGoldragon/claude-answers` rev `d6ae3ef` — `Query` ethos
  as the real consumer case for recursive type detection.
