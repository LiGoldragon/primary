# 699 — impl-reference integration-bar fixes (STEP A + B)

The five integration-bar fixes that operator report 432 raised against the
`{| … |}` impl-reference prototype, and designer report 698 ruled on, are now
implemented on `next/impl-reference-syntax`. This report maps each fix to its
432 finding and 698 ruling, cites the landing `file:line`, names the new
tests, records the observed full-suite counts, and states that the merge bar
is cleared.

All paths below are in the worktree
`/home/li/wt/github.com/LiGoldragon/schema-next/impl-reference-syntax`.

## The five fixes

### Fix 1 — target resolution (698 Ruling 1; 432: "free-standing impl over an arbitrary name")

A body-optional `TypeName {| impls |}` (the `ImplsOnly` / standalone
`ImplBlock` case) must resolve its target to a type declared *elsewhere* in
the same schema. An unresolved target is a typed error, not an accepted
free-standing impl over an arbitrary name.

- Error variant `SchemaError::UnresolvedImplTarget { name }` — `src/engine.rs:218`.
- Enforced in `Schema::impls_verified` — `src/schema.rs:776`: every standalone
  `ImplBlock` whose `target` is absent from the schema's declared types is
  rejected. Both lowering paths call `impls_verified` after assembly.
- Fixture `tests/fixtures/impl-catalog/body-optional.schema` corrected so the
  impl target `StatementText` is declared by a separate body-bearing entry
  (proving "elsewhere-declared" was the intent).
- RED fixture `tests/fixtures/impl-catalog/unresolved-target.schema`.

Tests: `unresolved_impl_target_is_rejected` (`tests/impl_catalog.rs:544`) and
`unresolved_impl_target_is_rejected_on_both_paths`.

### Fix 2 — duplicate vs. composing blocks (698 Ruling 2; 432: "multiple blocks for one target")

Multiple impl blocks/entries for the same target *compose* — distinct entries
union. A true duplicate — the same trait marker twice, or the same method
signature twice on one target — is a typed error.

- Error variant `SchemaError::DuplicateImplEntry { target, entry }` —
  `src/engine.rs:224`.
- Composition identity `ImplReference::composition_key` —
  `src/schema.rs:1250`: a trait entry (marker or body-bearing) keys on its
  trait name; an inherent method keys on its full `MethodSignature::render`.
- Reject-identical check `Schema::impl_entries_distinct` — `src/schema.rs:791`,
  called from `impls_verified`.

Tests: `distinct_impl_blocks_for_one_target_compose`
(`tests/impl_catalog.rs:582`), `duplicate_marker_across_blocks_is_rejected`
(`tests/impl_catalog.rs:607`), `duplicate_method_signature_on_one_target_is_rejected`,
`distinct_method_signatures_same_name_compose`.

### Fix 3 — lowering-path parity (the real correctness bug; 432: "macro path drops the catalog")

The macro/document path dropped the impl catalog while the typed-source path
carried it — one schema text lowering to two different semantic schemas. The
fix attaches the lowered catalog on the macro path too.

- `SchemaSource::impl_manifest` — `src/source.rs:136`: lowers the catalog once
  via the recursive source walk (single source of truth, no divergent
  re-derivation).
- Macro path reads the manifest, attaches fused catalogs via
  `Declaration::attach_impls`, passes standalone `ImplBlock`s through
  `Schema::with_impl_blocks`, and runs the shared `impls_verified` —
  `src/engine.rs` (the `impl_manifest` consumption block in
  `lower_document_with_resolver`).

Witness test: `both_lowering_paths_produce_the_same_impls`
(`tests/impl_catalog.rs:673`) — the macro path and the source path produce the
SAME manifest AND the same standalone blocks for one schema text, and the
manifest is asserted non-empty so the witness is not vacuous. Companion:
`both_lowering_paths_carry_fused_catalogs`.

### Fix 4 — trait-name validation (432: "trait atoms not validated as type names") — STEP B

A trait atom inside `{| … |}` must be a PascalCase type-name, like every other
type reference. A lowercase / non-type-name trait atom is a typed error.

- Error variant `SchemaError::NonTypeNameTrait { found }` — `src/engine.rs:230`.
- Enforced at the single decode point `SourceImplCatalog::from_block` —
  `src/source.rs:1069`: the trait atom is read, then gated through
  `Name::qualifies_as_pascal_case` (the same gate the generic-application head
  uses). Because both lowering paths decode the catalog through this method
  (the source path directly, the macro path via `impl_manifest`), the gate is
  shared — no second validator to drift.

Tests: `lowercase_trait_name_is_rejected` (`tests/impl_catalog.rs:747`, bare
marker) and `lowercase_trait_name_with_methods_is_rejected`
(`tests/impl_catalog.rs:762`, body-bearing trait impl — proving the gate is not
limited to markers).

### Fix 5 — full signature in the unverified-reference error (432: "error reports only the method name") — STEP B

`UnverifiedImplReference` compared the full `MethodSignature` internally but
reported only the method NAME, so a signature *mismatch* (right name, wrong
params/return) read as a missing-name. The error now carries the full
signature.

- `RustSurface::verify_method` — `src/schema.rs:1534`: on a missing match it
  now reports `signature.render()` (`src/schema.rs:1553`) — the canonical
  full rendering (name + parameters + return), the same rendering the
  duplicate-entry composition key keys on (`MethodSignature::render`,
  `src/schema.rs:1334`).

Test: `signature_mismatch_reports_the_full_signature`
(`tests/impl_catalog.rs:783`) — the surface provides `matches(candidate.Node)
-> Node`, the catalog references the `Boolean`-returning `matches`; same name,
wrong return type, so verification fails with the full signature (name +
`candidate` + `Node` + `Boolean`) in the error, and explicitly NOT the bare
`matches`. The existing `absent_method_signature_fails_verification`
(`tests/impl_catalog.rs:444`) was updated to assert the full signature too.

## Observed results

Run in the worktree with cargo:

- `cargo test` — **200 passed, 0 failed, 0 ignored** (baseline at branch tip
  `b9689f4f` was 189; STEP A added 8, STEP B added 3 net = 200). The
  `tests/impl_catalog.rs` bucket: **24 passed** (13 at branch tip → 21 after
  STEP A → 24 after STEP B's three new tests).
- `cargo clippy --all-targets -- -D warnings` — exit 0, **zero warnings, zero
  errors**.
- `cargo fmt --check` — exit 0, **clean**.

No stub-to-pass: every fix is enforced at lowering/verification, and each RED
test fails on the typed error path before the fix and passes after.

## Merge bar

The two bar-clearing requirements are met and proven by load-bearing tests:

- **Target resolution** (Fix 1): a standalone impl block over an undeclared
  type is a typed `UnresolvedImplTarget`, on both lowering paths.
- **Lowering-path parity** (Fix 3): one schema text lowers to the SAME impls
  (fused catalogs + standalone blocks) on the macro/document path and the
  typed-source path — the `both_lowering_paths_produce_the_same_impls` witness
  compares a non-empty manifest.

Fixes 2, 4, and 5 harden the surface (compose-distinct / reject-identical,
PascalCase trait gate, full-signature errors). The cursor-walk, the
typed/rkyv catalog, the `impl_manifest` single-source-of-truth, and the
out-of-band `RustSurface::verify_catalog` seam are preserved unchanged.

**The merge bar (target resolution + lowering-path parity) is cleared.**

## Carried-forward observation (not a blocker)

The macro-path parity attach matches fused catalogs to declarations by
qualified name (`namespace.iter_mut().find` in `lower_document_with_resolver`).
For the literal `{| … |}` syntax this is exact; if a macro *expansion* renamed
a declaration, the fused catalog would silently fail to attach. No current
test exercises macro-renamed types carrying impls — flag for integration if
that case is expected.
