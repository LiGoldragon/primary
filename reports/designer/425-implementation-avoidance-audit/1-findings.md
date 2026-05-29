# 425 — Implementation-avoidance audit: findings

*Authored by the dispatcher (designer lane). The dispatched sub-agent was
blocked by repeated 529 server-overload errors (two attempts, 0 tool-uses each),
so the audit was performed directly. Checked the live code against
[[424-schema-nota-extension-full-correctness-design-intent]] §5. Verdict:
**honest bootstrap — no design-implementation avoidance found.***

## Per-pattern verdicts

**1 · Circular golden tests — GENUINE (no circular tests).** `big_examples.rs`
and `big_emission.rs` assert on the *structure* of the lowered `Asschema` —
`assert_has_type(namespace, "Entry")`, `assert_has_variant(input, "Record")`,
non-empty input/output variants, `macros_applied` contains `Struct`/`Enum`,
`positions_seen` contains `RootNamespace` (`big_examples.rs:56-95`). They do NOT
compare against a dumped golden. The `.witness.txt` files are **orphaned** — the
only `witness` left in tests is a comment (`design_examples.rs:247`); no test
loads them. So this is *not* circular testing — but the dead `.witness.txt`
files still violate record 1112 and must be deleted (see Actions).

**2 · Stubs dressed as done — GENUINE.** No `todo!` / `unimplemented!` /
`panic!` in `src` across the three repos; only two legitimate
`unreachable!("atoms are handled by demote_to_string")` (`declarative.rs:194,405`).

**3 · Shared codec — PARTIAL, honestly in-progress (not avoidance).** `nota-next`
does not yet own `NotaEncode`/`NotaDecode`; `schema-rust-next` still emits a
per-file reader over `nota_next::Block`. The operator **openly flagged this** as
the next slice (operator report 237 §Remaining Gaps). Honest in-progress, not
disguised completeness.

**4 · Macros-as-data (record 1109) — GENUINE.** `MacroRegistry::lower(MacroObject)
-> MacroOutput` (`macros.rs:224`), and `MacroOutput` is all assembled-schema
*data* variants — `Asschema` / `Types(Vec<TypeDeclaration>)` / `Reference` /
`Fields` / `Variants` (`macros.rs:171-181`). No `Document::parse` / re-parse in
`macros.rs`. The old text-round-trip "deepest debt" (build-a-string-and-reparse)
is **fixed** — macros are data-in/data-out. (`expanded_templates: Vec<String>`
is a diagnostic trace only, `macros.rs:157`.)

**5 · Claimed-but-absent features — two real, openly-untracked gaps:**
- **Roots model (record 1155) — ABSENT.** `Asschema` still has `input`/`output`
  + `namespace` (`asschema.rs:59-66`); no `roots` / `RootDeclaration`. Genuine
  gap (step 5 not built); not disguised-as-done — but also not flagged by the
  operator.
- **Scalar `Path` (record 1152) — ABSENT.** `TypeReference` has
  `String`/`Integer`/`Boolean`, no `Path` (`asschema.rs:184-192`). Minor.
- **Inline-declare-reuse (record 1178) — GENUINE/present.** Inline pipe
  declarations lower into an ordered namespace with declare-before-use
  (operator report 237; `lowering.rs` test).

**6 · Emitted runtime — GENUINE (caveat).** Lowering tests are structural
(genuine), and there is a compiled-generated-Rust test that parses frames and
dispatches mail (operator report 237). I did not deep-read the dispatch test
body, but the structure indicates real emission, not a stubbed skeleton.

## Overall verdict

**Honest bootstrap. No design-implementation avoidance.** Tests assert on real
lowered structure (not circular goldens); no stubs-as-done; the macro engine is
genuinely data-based (1109 satisfied — the deepest concern, fixed); the codec
slice is openly flagged in-progress. The open gaps (codec-in-nota-next, roots
model, `Path`) are *real but honestly tracked or simply not-yet-built* — not
faked.

## Actions (operator)

1. **Delete the orphaned `.witness.txt` files** (6 files, schema-next +
   schema-rust-next) — record 1112; they are dead (unconsumed) but still
   present.
2. **Complete the open mandatory steps** (424 §3): the shared codec (in
   progress), the roots model (1155, not started), and the `Path` scalar (1152).
3. The roots model is the one absent piece the operator did **not** flag — surface
   it explicitly in the remaining slices, since the reactive engines depend on it.
