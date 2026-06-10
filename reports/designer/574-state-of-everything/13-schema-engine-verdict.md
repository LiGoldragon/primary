# Schema engine + grammar-overhaul verdict

## Schema Engine + Structural-Macro Grammar — Authoritative Verdict (2026-06-10)

### One-line answer
The **engine is coherent and largely beautiful** — the grammar overhaul (52ro/yp29/qz6j/lm84) is fully implemented and green on both `schema-next` (c8ebb39) and `schema-rust-next` (eca4028). But the **consumer fleet has barely begun migrating**: the terse forms exist almost entirely in test fixtures, while ~85 consumer `.schema` files still carry the OLD verbose grammar. The work that landed is the *capability*; the *fleet sweep* is almost entirely ahead.

### Engine health
`schema-next` builds clean at HEAD and passes its full suite (107+ tests across 13 binaries, all green). The grammar AST is genuinely clean:
- `TypeReference` (schema.rs:808) carries `Bytes` + `FixedBytes(u64)`; there is **no `Alias` variant** anywhere — `TypeDeclaration` is exactly `Struct | Enum | Newtype` (qz6j fully removed at the type level, not just disabled).
- The three reference-parsing paths agree: the live `SchemaSource` path (`source.rs` — `SourceVariantSignature::SelfTagged` arity-1, `SourceReference::FixedBytes` + `Bytes` head dispatch), the registry path (`TypeReference::from_parenthesis_objects`), and the `from_block` semantic-lowering path all handle the new forms identically.
- `52ro` self-tag lowers unconditionally to `from_name(name)` (source.rs:1060) — the test `self_tagged_variant_form_equals_explicit_repetition` proves `(Entry)` ≡ `(Entry Entry)`.

`schema-rust-next` builds against the no-alias schema-next and is green (66 tests). The emitter is **mostly `quote!`/`ToTokens`** (migration.rs `TypeRenderer`/`DefaultRenderer` are exemplary `impl ToTokens`; lib.rs emits `quote!{ Bytes }`, `quote!{ FixedBytes<#width> }`, hex codecs as token streams). The remaining transitional cruft is a **parallel string-based `rust_type()` renderer** (lib.rs:5623) that duplicates the `ToTokens` type path and is still wired into enum-constructor payload emission (lib.rs:4124-4131) via string→`syn::parse` round-trips.

### Grammar adoption (engine vs fleet)
| Form | Engine | Fleet |
|---|---|---|
| 52ro self-tag `(X)` | DONE, 3 paths agree, tested | ~0 real adoption; **787 occurrences of the OLD `(X X)` repetition across 85 files** |
| yp29 `Bytes` / `(Bytes N)` | DONE, scalar leaf + numeric arg + hex codec | 1 partial consumer (`signal-frame`); old `(Vec Integer)`-as-bytes still in `meta-signal-upgrade`, `signal-terminal` |
| qz6j no-aliases | DONE, `Alias` variant deleted | **~191 bare re-tag aliases** across spirit/agent/router/mind/message still rely on the now-dead transparency |
| lm84 hash-id (newtype-over-Bytes) | DONE, `Digest Bytes` round-trips | 0 consumer adoption (fixtures only) |

### Consumer schema debt
**~85 of ~102 consumer schema files** would need migration. The two big classes: (1) **787 old `(X X)` self-tag repetitions** that should collapse to `(X)`, and (2) **~191 bare `Name Synonym` re-tag aliases** (`Record Entry`, `Prompt signal-agent:lib:Prompt`) that post-qz6j are now *distinct newtypes*, not transparent — these are the correctness-breaking sites. Even the single most-migrated consumer (`agent/nexus.schema`) is only HALF-migrated: root enums use the new `(Prompt)` terse form, but its namespace still uses old `(SignalArrived SignalArrived)` + re-tag aliases.

### .concept.schema vs split-triad duality
~50 `.concept.schema` files vs ~48 split triad-port files (`nexus`/`sema`/`signal`/`meta-signal`/`daemon`/`lib`). **7 repos carry BOTH** (harness, mind, orchestrate, repository-ledger, router, system, terminal) — the split files are the live source; the `.concept.schema` is stale legacy cruft in a *different, older dialect* (parenthesized single-type newtypes like `Text (String)`, `Identifier (u64)` — note `(u64)` isn't even valid schema-next grammar). 11 repos are split-only (live). The concept-schema dialect should be retired wholesale, not migrated form-by-form.

### nota-next encoding divergence
The risk is **real but bounded and decode-safe**. The bump is the bare-atom encoding (`027e18a`, "render bare-safe strings as atoms"): `NotaString::format()` now emits plain alphanumeric strings as bare atoms instead of `[bracket]`. nota-next main is linear: `…→ae5c25c (schema-rust-next pin) →16493c8→2719624→027e18a (BUMP) →d8862b6 (HEAD)`.

- schema-rust-next deliberately pins `ae5c25c` (4 commits behind, BEFORE the bump) — isolation confirmed correct.
- **5 consumers pin the bump (d8862b6): spirit, criome, signal-criome, meta-signal-criome, agent.**
- Generated code calls `<Self as NotaEncode>::to_nota` → resolves to the *consumer's own* nota-next pin at compile time. So those 5 emit bare atoms where ae5c25c-pinned siblings emit `[brackets]`.
- The bump touched only `format()` (emit), not the parser; `parse_string` already accepts both bare atoms and brackets. So this is **emit-divergence, not a decode break** — the exposure is byte-equality / dedup / hash-stability / fixture-stability, not interop failure. Lowest-real-risk but must be unified before any byte-stable wire contract is declared.

### Bottom line for the psyche
The macro overhaul achieved exactly its goal — the engine *can* now express the terse, readable forms, and it does so beautifully and coherently. What "the state of the schema files" reveals is that the schema FILES themselves are overwhelmingly still in the old verbose dialect: the terse grammar is a capability not yet cashed in. The next body of work is mechanical-but-large: a fleet sweep (52ro collapse, qz6j re-tag→direct, yp29 bytes, concept-schema retirement) gated on each consumer's lock-bump, plus a decision to unify the nota-next pin so the d8862b6/ae5c25c fork closes.
