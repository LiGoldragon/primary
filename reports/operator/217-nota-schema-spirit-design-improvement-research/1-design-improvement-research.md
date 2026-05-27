# Design improvement research: NOTA + schema-next + schema-rust-next + spirit-next

Subagent research report. Inputs read: recent Spirit intent, the requested designer/operator reports as available, and current checkouts for `nota-next`, `schema-next`, `schema-rust-next`, and `spirit-next`.

## Strongest ideas to preserve

1. Keep `nota-next` as the honest structural floor. It should parse balanced delimiters, spans, pipe text, atoms, root-object order, and candidate symbol shapes only. The `Block::is_*` versus `Block::qualifies_as_*` split in `/git/github.com/LiGoldragon/nota-next/src/parser.rs` is the right boundary.

2. Keep schema as positional recursive structure, not labeled records. The current four-root shape in `schema-next/src/engine.rs` matches the fresh intent: imports, input, output, namespace. Record 940 sharpens this: schema is one recursive shape from root struct through macro-expanded fields down to scalar leaves.

3. Preserve pair-style brace namespaces. Spirit records 891, 894, 901, and current tests all converge: braces are key/value maps structurally; namespace is dynamic-enum-like conceptually; append-only order is future upgrade headroom.

4. Preserve real declarative macro definitions with visible captures. `schema-next/schemas/builtin-macros.schema` plus `$Name` and `$*Fields` is the first real macro substrate. Do not regress to Rust-only lowering that merely calls itself a macro system.

5. Preserve source-visible generated Rust. Spirit records 909 and 910 correct the `OUT_DIR` detour: generated schema code lives under `src/schema/`. `spirit-next/src/schema/lib.rs` plus `build.rs` freshness checking is the right reviewable loop.

6. Preserve generated signal-plane ownership. `schema-rust-next` now emits route enums, short headers, rkyv frame methods, and `SignalFrameError`; `spirit-next/src/transport.rs` only owns Unix-stream length-prefix I/O. This is the best recent improvement over report 208's gap.

7. Preserve the runtime triad as visible Rust shape: signal `Input` lowers to generated `SemaCommand`, store applies one command path, `SemaResponse` maps to `Output`. `spirit-next/src/engine.rs` and `src/store.rs` are still MVP, but the nouns/verbs split is correct.

## Gaps and wrong turns to correct

1. `schema-next` itself still uses `schemas/` in the current checkout (`schemas/root.schema`, `schemas/core.schema`, `schemas/builtin-macros.schema`, `schemas/spirit-min.schema`). That conflicts with the crate-standard `schema/lib.schema` direction already used by `spirit-next`. Migrate the schema crate's own self-description to the same convention.

2. `SchemaPackage` loads `schema/lib.schema` and can compute sibling paths, but imports are not real. `schema-next/src/module.rs` has path helpers; `schema-next/src/engine.rs` still lowers imports as local declarations without transitive load, collision checks, selective import, import-all, or cross-crate crate-name resolution.

3. Macro dispatch is still first-match, not most-specific match. Fresh record 932 says macro matching uses delimiter, internal shape, object count, qualified-symbol predicates, and combinations, with most-specific dispatch. `schema-next/src/macros.rs::MacroRegistry::lower` currently returns the first match.

4. The root schema/bootstrap story is still Rust-owned. `schema-next/src/engine.rs` hard-codes the four root positions and default registry. Record 886 requires a tested schema-authored self-description even while bootstrap Rust remains; record 940 wants recursive macro expansion from root-layer struct to scalar leaves.

5. `RecordSet [Entry]` in `spirit-next/schema/lib.schema` is a newtype around one entry, not a vector result set. Spirit v0.3 records use multi-topic entries and observation returns multiple records. `spirit-next` is still a concept, not feature parity.

6. Spirit SEMA is still in-memory. `spirit-next/src/store.rs` has `Vec<StoredRecord>` behind a `Mutex` via `Engine`. It needs redb persistence, daemon-stamped timestamps, schema-version markers, read-side migration, and query/topic catalog parity.

7. Schema diff and upgrade derivation are absent. `schema-next/src/asschema.rs` is an ordered assembled model, but there is no canonical `.asschema` serialization, schema hash, diff classification, generated `UpgradeFrom`/`DowngradeTo`, default/discard annotations, or incompatible-change failure.

8. `schema-rust-next` still emits scalar aliases (`pub type Text = String`, `pub type Integer = u64`) and generated NOTA helper objects inside every output. The helper-object move fixed free functions, but scalar identity and reusable codec support still want real typed schema/runtime homes.

9. `signal-frame` remains outside the new stack. Intent records 860 and 863 decide that signal-frame protocol belongs in the existing `signal-frame` repository as schema-derived substrate. The current stack emits frame support locally; it does not yet import a canonical `signal-frame.schema`.

## Next refactor targets

1. `/git/github.com/LiGoldragon/schema-next`
   - Rename `schemas/` to `schema/`.
   - Make `schema/lib.schema` the schema crate entrypoint.
   - Move `builtin-macros.schema` under the new convention and update `DeclarativeMacroLibrary::builtin`.
   - Add a self-description fixture that lowers through the current engine and names the root `Schema` fields and nested declaration types.

2. `/git/github.com/LiGoldragon/schema-next/src/module.rs`
   - Add import declarations that `schema/lib.schema` can use to load sibling modules.
   - Return a package-level assembled result, not only one `SchemaModuleSource`.
   - Preserve fully qualified names through all imported modules.
   - Reject duplicate local names and conflicting imported names.

3. `/git/github.com/LiGoldragon/schema-next/src/macros.rs` and `src/declarative.rs`
   - Replace first-match dispatch with explicit match objects carrying specificity.
   - Represent pattern criteria beyond literal captures: delimiter, root-object count, atom qualification, pair/map position, and rest capture.
   - Add ambiguity errors when two macros match with equal specificity.

4. `/git/github.com/LiGoldragon/schema-rust-next/src/lib.rs`
   - Emit from a package/multi-module `Asschema` collection to multiple `src/schema/**/*.rs` files.
   - Keep generated signal-frame methods on generated root enums, but prepare them to come from imported `signal-frame.schema`.
   - Replace raw scalar aliases with schema-declared scalar/newtype strategy when the schema core is ready.

5. `/git/github.com/LiGoldragon/spirit-next/schema/lib.schema`
   - Update toward Spirit v0.3 parity: `Entry` has topic vector semantics, daemon-stamped timestamp type, and observation outputs a vector-backed record set.
   - Split ordinary and core/owner contracts when the signal-triad split is implemented.
   - Keep `SemaCommand`/`SemaResponse` visible as generated nouns.

6. `/git/github.com/LiGoldragon/spirit-next/src/store.rs`
   - Replace `Vec<StoredRecord>` with redb-backed single-writer SEMA.
   - Store schema-version per record or table entry.
   - Add topic catalog and observation query support.
   - Make migrations read-side and daemon-owned.

7. `/git/github.com/LiGoldragon/signal-frame`
   - Treat the old `signal_channel!` infrastructure as legacy.
   - Introduce `schema/lib.schema` or `schema/signal-frame.schema` as decided by the migration pass.
   - Make component schemas import frame primitives instead of each generated crate owning its own private frame support.

## Highest-value Nix tests and witnesses

1. `schema-next-schema-folder-convention`: fail if `schemas/` remains, require `schema/lib.schema`, require `DeclarativeMacroLibrary::builtin` to load through the new path.

2. `schema-next-self-description-lowers`: lower the schema self-description through `SchemaEngine`, assert root field names/types, assert namespace pair-style, and assert macro traces include declarative macro expansion.

3. `schema-next-imports-load-sibling-modules`: fixture crate with `schema/lib.schema` importing `schema/signal.schema`; prove both lower into one qualified assembled package.

4. `schema-next-import-collision-rejected`: two imported modules export the same local name; check the engine returns a typed collision error.

5. `schema-next-macro-specificity`: two macros match one object, the more specific one wins; equal specificity fails with an ambiguity error.

6. `schema-rust-next-emits-multi-file-module-tree`: one package identity emits `schema/lib.rs` plus at least one nested module file; compare exact generated fixtures, compile them, and run NOTA/rkyv round trips.

7. `spirit-next-generated-source-freshness`: keep the existing build-script stale-source failure, but add a central regeneration command witness so agents do not rely on an ad hoc example invocation.

8. `spirit-next-recordset-is-vector-backed`: record two matching entries, observe by topic/kind, and prove the generated `RecordSet` carries both over the process boundary.

9. `spirit-next-redb-restart-persists-records`: daemon writes through CLI, shuts down, restarts with the same state dir, and observation returns the prior record.

10. `spirit-next-schema-version-read-migration`: seed a previous-version fixture database, start current daemon, read a record, and prove the migrated current form plus schema-version marker.

11. `signal-frame-schema-imported-by-spirit`: generated Spirit frame methods must come from an imported signal-frame schema path; grep should reject local duplicate frame primitive declarations once the import exists.

## Open intent questions that block implementation

1. None block the next `schema-next` import/package slice. The crate folder, `schema/lib.schema`, single-colon names, pair-style namespaces, and source-visible `src/schema/` emission are already decided strongly enough.

2. The exact committed-versus-gitignored policy for `src/schema/*.rs` is not settled in the inputs, but it does not block implementation. Spirit record 909 fixes the path and visibility; the repo can choose whether generated files are committed once the regeneration command exists.

3. The signal-frame import shape does not block the immediate package-loader work, but it blocks the full "generated frame behavior comes from one canonical frame schema" milestone. Intent decides the home (`signal-frame` repo), not the exact schema vocabulary.

4. Spirit production replacement is blocked by implementation, not by intent: v0.3 parity, redb durability, migration, and multi-topic observation still have to land before cutover can be considered.
