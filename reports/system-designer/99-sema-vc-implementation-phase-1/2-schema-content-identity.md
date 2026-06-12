# 99/2 — schema-next blake3 content identity (whole-schema + family closures)

*Implementation sub-agent chapter (workflow run `wf_8724d72d-bd4`, 2026-06-12, system-designer lane). The adversarial review — which independently re-ran every test suite — is appended.*

# schema-next: content identity (branch `schema-content-identity`)

## What landed

Schema now owns its content identity, realizing Spirit x0ja (one blake3 basis for all content addressing) and wrjl (the schema's hash is its identity/version). Everything is computed on the **semantic schema-in-Rust value** (`Schema`), never on `.schema` text, so formatting-only source edits do not move any address. Head commit `4f1bd2a1cbeb` ("content identity: blake3 ContentHash + FamilyClosure on Schema"), pushed to `origin/schema-content-identity`.

## The nouns

- **`ContentHash`** — `src/identity.rs:57` — a 32-byte newtype over blake3 output; private field, derives rkyv `Archive/Serialize/Deserialize` + `Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd`; hand-written `Display`/`Debug` render lowercase hex; accessors `as_bytes()`/`to_hex()`. Construction is closed: only `ContentHash::derive(HashDomain, bytes)` (`src/identity.rs:60`), private to the identity module.
- **`HashDomain`** — `src/identity.rs:26` — a private two-variant enum (`Schema`, `FamilyClosure`) whose `context()` returns the blake3 `derive_key` context string per kind (`"schema-next 2026-06-12 whole-schema content identity"` / `"schema-next 2026-06-12 family-closure content identity"`). Domain separation is structural: the two hash kinds cannot collide because they are keyed hashes under distinct contexts.
- **`FamilyClosure`** — `src/identity.rs:98` — the per-family identity noun: root `Name` + reachable `Vec<Declaration>` + reachable `Vec<ImportDeclaration>` + reachable `Vec<StreamDeclaration>`, every group sorted canonically by name so closure bytes are independent of walk order. `FamilyClosure::content_hash()` (`src/identity.rs:124`) hashes the closure's own rkyv bytes under the family domain — the closure type owns the walk result and the hash.
- **`ClosureWalk`** — `src/identity.rs:153` — the private state-bearing walker (schema ref, family name for error context, three `BTreeMap`s doubling as visited-sets and canonical sorters). All verbs are methods on it: `family_root` (`:191`), `visit_declaration`, `visit_enum`, `visit_stream` (`:243`), `visit_reference` (`:265`), `visit_name` (`:284`). No free functions anywhere.

## The Schema surface

- `Schema::content_hash()` — `src/identity.rs:135` — blake3 over `Schema::to_binary_bytes()` (the existing canonical rkyv archive at `src/schema.rs:390`), under the whole-schema domain.
- `Schema::family_closure(name)` — `src/identity.rs:144` — the closure for a namespace declaration **or** an input/output root enum (a root enters the closure as a public enum `Declaration`; its input/output position is the version-control layer's concern). These inherent impls live in `src/identity.rs` (schema.rs is already ~1600 lines; identity is one coherent concern file).

## Closure reachability semantics

From the root declaration the walk follows: struct field references, enum variant payloads, newtype/alias references, `Vector`/`Optional`/`ScopeOf` inner references, both `Map` positions, and — beyond the brief's minimum — stream relations (`opens`/`belongs`) into `StreamDeclaration`s and their `token`/`opened`/`event`/`close` references, since those shape the family's wire surface. Scalar leaves (`String, Integer, Boolean, Path, Bytes, FixedBytes`) terminate. Cycles terminate via the name-keyed maps.

**Imports — honest limitation:** in this crate `ResolvedImport` (`src/resolution.rs:102`) carries only `local_name` + parsed `crate:module:Type`; resolution loads the dependency module schema transiently to confirm the name and then drops it — the imported declaration's own closure is *not* available. So a reachable import contributes its **stable identity only**: the `ImportDeclaration` (local alias + `crate:module:Type` source), which exists identically whether or not a resolver ran, keeping the family hash independent of resolution mode. Consequence the version-control layer must own: an edit *inside* the imported type in the dependency does **not** move the importing family's hash; cross-crate change detection composes this hash with the dependency schema's own hashes. (`ResolvedImport`'s Rust-path data is fully derived from the same `crate:module:Type` name, so including it would add no identity.)

Unknown names produce typed errors: `SchemaError::FamilyRootNotFound` / `FamilyReferenceNotFound { family, name }` (`src/engine.rs:181-187`), in the crate's existing hand-written error idiom (this crate's `SchemaError` predates and does not use thiserror; new variants match the file's established style).

## Determinism

rkyv 0.8 with this crate's `little_endian, pointer_width_32, unaligned` feature set produces packed, padding-free archived layouts, so equal `Schema`/`FamilyClosure` values serialize to equal bytes; the closure's canonical sort removes walk-order sensitivity. Witnessed by parsing the same fixture twice and by the formatting-variant tests.

## Witnesses (tests/identity.rs, 8 tests, all passing)

- `identical_schema_produces_identical_hashes` — same fixture lowered twice: equal whole-schema, `Entry`-family, and `Input`-family hashes.
- `deep_field_type_change_changes_the_family_hash` — `Magnitude` (two reference hops below `Entry`: `Entry -> Detail -> Magnitude`) changed `Integer`→`String` moves the `Entry` family hash and the whole-schema hash.
- `unrelated_declaration_change_leaves_the_family_hash_unchanged` — editing `Unrelated` leaves the `Entry` family hash fixed while the whole-schema hash moves.
- `formatting_differences_do_not_change_any_hash` — a re-spelled source with `;;` comments and whitespace churn yields identical whole-schema and family hashes (hash is over the semantic value, not text).
- `family_closure_collects_only_reachable_declarations_sorted_by_name`, `root_enum_family_closes_over_its_variant_payloads`, `unknown_family_root_is_a_typed_error`, `family_reaching_an_import_includes_its_stable_identity` (uses the existing `marker-core`/`import-consumer` fixtures; also proves the import-bearing family hash is stable across two resolved lowers).

## Files touched

- `src/identity.rs` (new, 311 lines), `tests/identity.rs` (new, 256 lines)
- `src/engine.rs:181-187` (two error variants), `src/lib.rs:3,18` (module + `pub use identity::{ContentHash, FamilyClosure}`)
- `Cargo.toml:16` (`blake3 = "1"`) + `Cargo.lock`
- `INTENT.md` (two new constraint paragraphs bracket-quoting Spirit wrjl and x0ja as realized), `ARCHITECTURE.md` (content-identity paragraph in the Semantic Schema section)

`SchemaIdentity`'s hand-authored version string (`src/engine.rs:27-47`) is untouched; content identity lands beside it. Full suite: 123 tests green, zero warnings, `cargo fmt` clean.

## branches
- schema-next @ schema-content-identity head 4f1bd2a1cbeba379e490a1f3022a97a7ae635cdb (/home/li/wt/github.com/LiGoldragon/schema-next/schema-content-identity)

## testResults
schema-next (worktree /home/li/wt/github.com/LiGoldragon/schema-next/schema-content-identity), cargo test, all suites:

     Running tests/big_examples.rs        — test result: ok. 3 passed; 0 failed
     Running tests/collections.rs         — test result: ok. 13 passed; 0 failed
     Running tests/design_examples.rs     — test result: ok. 13 passed; 0 failed
     Running tests/identity.rs            — test result: ok. 8 passed; 0 failed
     Running tests/lowering.rs            — test result: ok. 25 passed; 0 failed
     Running tests/macro_exploration.rs   — test result: ok. 14 passed; 0 failed
     Running tests/operator_271_closed_claims.rs — test result: ok. 7 passed; 0 failed
     Running tests/raw_core_schema.rs     — test result: ok. 6 passed; 0 failed
     Running tests/resolution.rs          — test result: ok. 7 passed; 0 failed
     Running tests/source_codec.rs        — test result: ok. 17 passed; 0 failed
     Running tests/symbol_path.rs         — test result: ok. 5 passed; 0 failed
     Running tests/upgrade_pilot.rs       — test result: ok. 5 passed; 0 failed
   Doc-tests schema_next                  — test result: ok. 0 passed; 0 failed

New identity suite tail (cargo test --test identity):
running 8 tests
test unknown_family_root_is_a_typed_error ... ok
test family_closure_collects_only_reachable_declarations_sorted_by_name ... ok
test root_enum_family_closes_over_its_variant_payloads ... ok
test family_reaching_an_import_includes_its_stable_identity ... ok
test unrelated_declaration_change_leaves_the_family_hash_unchanged ... ok
test deep_field_type_change_changes_the_family_hash ... ok
test formatting_differences_do_not_change_any_hash ... ok
test identical_schema_produces_identical_hashes ... ok
test result: ok. 8 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

Total: 123 passed, 0 failed, 0 compiler warnings.

## blockers
- None blocking. One design fact the orchestrator should carry forward: ResolvedImport in schema-next holds only the import's stable identity (local alias + crate:module:Type) — the dependency's declaration closure is not retained after resolution, so an importing family's hash does not move when the imported type changes inside the dependency; the version-control layer must compose family hashes with the dependency schema's own content hashes for cross-crate change detection.


## Adversarial review

VERDICT: approve

## mustFix

## advisory
- Family closures exclude RelationDeclaration: equivalence relations over variant paths (Schema.relations, src/schema.rs:408-443) are semantic Schema data that never move any family address — only the whole-schema hash sees them. The ClosureWalk (src/identity.rs:153-311) is documented as reachability-from-the-declaration and relations point AT declarations rather than being reachable from them, so the implementation is internally consistent, but the version-control layer consuming family hashes will treat hash-stable as semantically-unchanged. Before family addresses land in storage, either extend the walk to attribute relations whose paths resolve inside the closure, or state the exclusion explicitly in the identity.rs module doc and the new ARCHITECTURE.md paragraph (currently both enumerate inclusions only, inviting a false completeness assumption).
- Whole-schema/family hash asymmetry: Schema::content_hash covers the full Schema value including SchemaIdentity (component name + hand-authored version string) and resolved_imports (src/schema.rs:207-216 via to_binary_bytes at schema.rs:390), so a version-string-only bump moves the whole-schema content address with zero structural change, while FamilyClosure (src/identity.rs:98-103) carries neither. Defensible under wrjl's 'any edit changes the address', but worth one explicit sentence in ARCHITECTURE.md so consumers know the whole-schema address is not pure structure.
- family_reaching_an_import_includes_its_stable_identity (tests/identity.rs:216-256) is a same-process witness: it lowers the same source twice with the same resolver, so it would still pass if resolved filesystem paths leaked into the closure. I verified machine-independence by type inspection instead (ImportDeclaration/ImportSource are symbolic-only). A stronger witness lowers from a relocated copy of the fixture directory and asserts hash equality.
- No cross-process golden-hash witness exists; identical_schema_produces_identical_hashes proves only in-process determinism. Deliberately reasonable while the Schema struct churns pre-production (a golden hash would break on every schema-shape change), but the version-control layer needs one pinned-hash test the moment addresses are persisted, since rkyv byte stability then becomes a load-bearing wire contract.
- ContentHash::to_hex (src/identity.rs:70-72) allocates a String per byte via format!; a fmt-based hex write (or blake3's own to_hex on the raw bytes) is cleaner. Trivial.

## disciplineFindings
- No free functions anywhere in the diff: all logic lives on ContentHash, FamilyClosure, impl Schema, ClosureWalk, and HashDomain. HashDomain (src/identity.rs:26-38) is a two-variant fieldless domain enum selecting derive_key contexts via match — a real noun, not a ZST namespace.
- Full-English identifiers throughout (formatter, declaration, reference, hasher); no ancestry-repeating names — ContentHash and FamilyClosure, not SchemaContentHash (C-CRATE-PREFIX respected); private walk state named ClosureWalk with consuming into_closure, direction-encoded.
- Errors follow the crate's existing hand-written-enum idiom: two new structured variants FamilyRootNotFound and FamilyReferenceNotFound on SchemaError (src/engine.rs:181-187), Display-via-Debug matching engine.rs:296-300; the typed error is asserted by value in tests/identity.rs:200-213. No anyhow, no string errors.
- No hand-rolled parsing (hashes computed over the existing lowering pipeline's semantic value), no stringly dispatch, no bool flags, no backward-compatibility shim — the change is purely additive and the beside-not-replacing relationship to SchemaIdentity is the quoted Spirit decision, not a compat virtue claim.
- Tests in a separate tests/identity.rs file matching the repo's tests/ layout; fixture state owned by a data-bearing IdentityFixture struct; exact sorted closure membership asserted (tests/identity.rs:180: [Detail, Entry, Magnitude, Topic]).
- family_closure takes &str matching the pre-existing Schema::root_named(&str) idiom (src/schema.rs:269); family_root dissolving the namespace-declaration-vs-root-enum special case by wrapping roots as Declaration::public (src/identity.rs:191-201) is the beautiful move in this diff.
- INTENT.md update quotes exactly two bracket-quoted Spirit records with identifiers (wrjl Decision, x0ja Constraint) matching the brief's named constraints; ARCHITECTURE.md paragraph (lines 148-165) accurately describes the implementation; nothing outside the brief's repo was touched and Cargo.lock growth is blake3's dependency tree only.

## testHonesty
Yes — I re-ran the full suite myself in /home/li/wt/github.com/LiGoldragon/schema-next/schema-content-identity (a clean jj workspace whose head 4f1bd2a1 exactly matches the claimed commit and origin/schema-content-identity): all 13 suites green, 123 passed / 0 failed, byte-for-byte matching the claimed per-suite counts; tests/identity.rs re-run after touching src/identity.rs gives 8/8 with a warning-free rebuild. The 0-warnings claim holds for rustc (cargo clippy shows 3 warnings, all pre-existing on main in files this branch does not touch). The witnesses are real, not flattering: deep two-hop field-type change moves both hashes, unrelated-declaration change moves the whole-schema hash but not the family hash, formatting/comment-only re-spelling moves neither, closure membership is asserted as an exact sorted list, and the unknown-root error is matched by typed value. Two witnesses are weaker than their names suggest (identical-hash and import-stability prove only same-process determinism), so I verified the cross-machine determinism claim independently: Schema holds only Vecs, import types are symbolic-only with no PathBuf or version, the closure sorts via BTreeMap, and rkyv 0.8.16's resolve_aligned zeroes the archived buffer before field writes while pad() writes explicit zeros, with little_endian/pointer_width_32/unaligned pinned in Cargo.toml — so the hashed bytes are genuinely canonical.

