# Strict quality pickup

> **Supersession notice (2026-08-06).** Later rulings supersede parts of this file; the text below is preserved unedited as the record. No longer in force:
> - Bare trait-pickup spellings (e.g. bare `Ordered` inside shape slots) — superseded in spelling by the guillemet trait-mark ruling: trait requirements are guillemet-marked at every position (`visionReacquisitionRulings-2026-08-05.md`). The strict-pickup semantics itself stands.
> The design log reads by recency; consult the named files for the current form.

Psyche ruling, conveyed through the implementation dispatch: authored bare
`Ordered` in `WireResult.Result<Vector<Ordered> Error>` is a Trait pickup, not
a concrete type reference to be renamed at every use. The strict carriers must
retain `Ordered` as the type-parameter name and record its `Ordered` quality
bound. At the Rust boundary only, the parameter renders as `Ordered: Ord`; a
use of that parameter renders as `Ordered`. Structural names such as `Vector`
continue to use the centralized Rust type-use projection (`Vec`), while
concrete authored arguments such as `Error` stay ordinary type references.

The end-to-end witness is therefore equivalent to:

```rust
pub struct WireResult<Ordered: Ord>(Result<Vec<Ordered>, Error>);
```

This ruling supersedes the prior witness interpretation that applied the
`Ordered -> Ord` mapping indiscriminately to nested type uses.
