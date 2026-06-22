# Schema IR — one representation, three projections

*schema-designer · report 10 · answers the psyche's research question
(is the lowering IR the same as the help/instance data?) with a
code-grounded synthesis. Converges with operator's
`reports/schema-operator/6-help-as-schema-ir-view.md` — the fifth
independent convergence (help, schema-codec, instance-schema design,
instance-schema impl, now the IR unification).*

## The answer

**Yes at the core, no at the surface: there is ONE shared canonical
"what a type is" object, and the three uses are thin projections of it —
not three byte-identical types.** The shared core is **schema-next's
resolved IR: `schema::TypeReference` nested in `Schema` / `Declaration` /
`TypeDeclaration` / `EnumVariant`** (`schema-next/src/schema.rs:2124`).
The raw `Source*` AST is a **transient parse stage** that resolves into
the IR (`to_type_reference` `source.rs:2912`, `resolve_reference`
`source.rs:2946`), not a consumer-facing form.

## Today: three reference enums, and why only Help diverges

| representation | who walks it | container axis |
|---|---|---|
| resolved `schema::TypeReference` (`schema.rs:2124`) — canonical IR (scalar leaves, qualified names, `Vector`/`Map`/`Optional`/`ScopeOf`, `Application`) | **Rust-lowering** (`schema-rust-next` `RustTypeReferenceTokens` `lib.rs:1886`, `Vector→Vec<T>`) | `Vector` |
| raw `SourceReference` (`source.rs:2745`) — pre-resolution parse tree | **Help** (`help.rs` imports `SourceReference`, **no** `TypeReference`; builds from `from_schema_text`, never lowering) | `Vector`, but `(Vec …)` falls to `Application{head:"Vec"}` (`source.rs:2828`) |
| nota-next-local `TypeReference` (`instance_schema.rs:27`) — decoder-captured | **instance-schema** (`expected` field, `instance_schema.rs:82`) | `Vector` |

The three are **near-isomorphic on the container axis** (all carry
`Vector`/`Optional`/`Map`); the resolved IR is strictly richest. The
non-canonical forms each lift *into* it. **Instance-schema and
Rust-lowering already agree** on the canonical reading (`Vector` / `Vec<T>`)
— instance-schema because its references come from real typed Rust
positions, lowering because it walks the resolved IR (it tolerates the
stray `Application{Vec}` only by the coincidence that `Vec` is valid
Rust). **Only Help diverges, and only because it consumes the raw
pre-resolution `SourceReference`** — exactly "typed only in the weak
sense of a typed AST node, not the intended built-in vector."

## The unification

One reference vocabulary (the resolved IR), three projections:

- **Rust-lowering** = the **emitted view** (already correct): `TypeReference` → Rust/rkyv.
- **Help** = the **declared-type view** — move it onto the resolved IR: build from `engine.lower_schema_source` over the embedded `*_SCHEMA_SOURCE` (the same path lowering uses) instead of `from_schema_text`; match `schema::TypeReference` instead of `SourceReference`; the `HelpBody`/`HelpTypeExpression` duplication of `SourceDeclarationValue`/`SourceReference` collapses away.
- **instance-schema** = the **realized-value view** — already canonical; its `expected` spine should be (or losslessly lift to) `schema::TypeReference`, with the per-value body as the overlay.

**The `Vec`/`Vector` bug dissolves by construction:** once Help reads the
resolved IR it can no longer pick the raw `Application` branch (it never
touches `SourceReference`); combined with the canonicalization fix it
renders `(Vector Domain)` like everyone else.

## Adversarial: one core, not one monolith

Each use genuinely needs something the others discard — so it is **one
shared core IR + three thin per-use layers**, not a single struct:

- **Help** needs source-level **docs/comments, declaration order,
  presentation** that lowering drops (the `HelpModel` tree is
  presentation, not type IR). Comments live only in source text → the IR
  carries doc metadata *or* Help keeps a doc-decoration pass over the
  source alongside the resolved structure.
- **Rust-lowering** needs **Rust-target details** (derive sets, rkyv
  `omit_bounds`/bytecheck, scalar→concrete Rust type, identifier
  sanitization) — the emitted-view layer, downstream of the IR.
- **instance-schema** needs **per-value realized structure** (which
  variant, vector element count, optional presence, per-element children)
  — a value-trace overlay pairing each realized node with its expected IR
  reference.

So: the "pure information on what a thing is" **is** shared and single
(the resolved reference IR); the per-use layers are presentation,
target-codegen, and realized overlay — none of which belong in the core.

## Migration

1. **Point Help at the resolved IR.** In `help.rs`: replace
   `HelpModel::from_signal_schema_source`'s `from_schema_text` build with
   `engine.lower_schema_source(*_SCHEMA_SOURCE)` → `schema::Schema`;
   change imports from `Source*` to `Schema`/`Declaration`/`TypeReference`;
   rewrite `HelpTypeExpression::from_reference` to match
   `schema::TypeReference` (scalar leaves arrive as dedicated variants,
   not `Plain`); add a doc-decoration pass only if Help must surface
   source comments. Delete the `HelpBody`/`HelpTypeExpression`
   source-coupling duplicate.
2. **Fix `Vec`→`Vector` canonicalization** at the decode/resolve
   boundary (accept `(Vec T)` as canonical `Vector`, or migrate the
   contract `.schema` sources to `(Vector T)`; `Vector` is canonical).
3. **Lift instance-schema's `expected`** to `schema::TypeReference` so
   all three share one reference type.
4. Mirror in both Help copies; update Help goldens `Vec`→`Vector`.

## Status

The **vision is being built on the `schema-ir` designer branch** (Help
collapsed onto the resolved IR, the duplicate deleted, `Vec`→`Vector`
fixed, a test proving Help and instance-schema render the same type
identically). When it lands this report gets the before/after and the
branch tips. Recommendation (with operator): **collapse Help onto the
schema IR before broadening beyond Spirit**, so mentci and every future
contract inherit the unified object.
