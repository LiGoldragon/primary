# 383 — Next-version schema design: study and implement

Designer-assistant lane. Per psyche records 894 (Maximum), 902 (Maximum),
903 (Maximum). Task: STUDY operator's current main before implementing,
then IMPLEMENT the next-version namespace/folder convention on a designer
feature branch derived from operator's freshest main.

## 1. Study findings

### Operator's current main (read 2026-05-27)

While I studied and implemented, the operator landed converging work:

- **`schema-next` `807c5250` add schema package module entrypoint** — adds
  `SchemaPackage` + `SchemaModuleSource` in `src/module.rs`. The loader
  expects a crate root with `schema/lib.schema`; exposes
  `lib_schema_path()`, `module_schema_path()`, `load_lib()`,
  `lower_lib()`. Adds `Name::namespace_segments()` /
  `Name::local_part()` for colon-path splitting. Adds two new tests:
  `colon_qualified_names_lower_as_schema_names` and
  `package_loader_reads_schema_lib_entrypoint` (uses a fixture at
  `tests/fixtures/spirit-crate/schema/lib.schema`).
- **`nota-next` `1c11876b` allow colon-qualified nota symbols** — confirms
  `:` is a symbol character at the atom lexer (it already was).
- **`spirit-next` `e004fc62` load spirit schema from lib entrypoint** —
  renames `schema/spirit.schema` → `schema/lib.schema`, routes through
  `SchemaPackage::load_lib`, emits to `OUT_DIR/schema/lib.rs`, declares
  a `SchemaBuild` struct in `build.rs` with `from_environment` and
  `run` methods (no free helpers).
- **`schema-rust-next` `5ca1c964` emit schema module file paths** —
  `RustEmitter::emit_file` now uses `RustModulePath::to_file_path()` to
  produce `schema/<module>/<file>.rs` paths reflecting the colon-path
  structure of the identity.

### Designer prototypes worth carrying forward

The `design-deep-spirit-*` repos are superseded by the running
`spirit-next` pilot. `signal-frame/schema/signal-frame.concept.schema`
remains a 6-position DRAFT not consumed by the current stack (per
report 381 it is "not the truth source"). No carry forward from
those.

### Coordination state with the pair-style sweep

`schema-next` worktree `designer-pair-style-namespace-2026-05-27`
(commit `7b264003`) only contains an ARCHITECTURE.md prose edit. The
substantive pair-style code change (`8c821cba make schema namespaces
key-value only`) is on operator main. No active in-flight branches in
the other repos. The sweep landed; my new branch was based on the
newer operator main `807c5250` instead.

## 2. Plan (synthesized from 894/902/903)

1. **Namespace path syntax**: bare colon-paths as NOTA atoms
   (`signal-frame:Frame`, `schema-next:macros:RootImports`). NOTA's
   `is_symbol_character` already accepts `:` — no grammar extension.
   Operator main proves this with `colon_qualified_names_lower_as_schema_names`.
2. **Schema folder convention**: each crate has `schema/lib.schema`
   plus sibling `schema/<module>.schema`. Operator main proves this
   with `SchemaPackage::load_lib`.
3. **Rust emission target**: `src/schema/<module>.rs` per record 902
   wording, OR `OUT_DIR/schema/<module>.rs` per operator's chosen
   interpretation. Operator landed the OUT_DIR variant first. Both
   produce the same module shape from the consumer's view; only
   storage differs.
4. **Migration**: `schemas/` → `schema/`, `root.schema` →
   `lib.schema`. Operator did this for `spirit-next` but kept
   `schemas/` in `schema-next` itself.
5. **Hot-reload**: design only (out of scope this pass).

## 3. Implementation landed

### `schema-next` — branch `designer-schema-namespace-and-folder-2026-05-27` pushed

**Commit `b598604d6831`** "schema-next: migrate schemas/ to schema/ +
lib.schema entry point" — based on operator main `807c5250`.

Files changed:
- `schemas/root.schema` → `schema/lib.schema`
- `schemas/core.schema` → `schema/core.schema`
- `schemas/spirit-min.schema` → `schema/spirit-min.schema`
- `schemas/builtin-macros.schema` → `schema/builtin-macros.schema`
- `src/declarative.rs` — `include_str!` path updated to
  `../schema/builtin-macros.schema`.
- `tests/lowering.rs` — three `include_str!` paths updated;
  `root_schema_describes_the_schema_root_type` renamed to
  `lib_schema_describes_the_schema_root_type`; identity in that test
  tightened from generic `"schema"` to `"schema-next"`.
- `ARCHITECTURE.md` — full sections added for schema folder convention,
  fully qualified names (colon-path syntax), and forward direction
  pointing at `SchemaPackage::load_lib`. Merged operator's bullets
  about colon-qualified names and key/value-only braces.
- `flake.nix` — new check `schema-folder-convention` asserts the new
  layout. Removed `schemas/` references in
  `namespace-braces-are-key-value`.

**Tests**: all 13 tests pass on the migrated layout, including the
two operator-side tests (`package_loader_reads_schema_lib_entrypoint`,
`colon_qualified_names_lower_as_schema_names`).

Branch: <https://github.com/LiGoldragon/schema-next/tree/designer-schema-namespace-and-folder-2026-05-27>

## 4. Implementation deferred / not landed

### `spirit-next` — superseded by operator main; designer branch abandoned

I started a designer branch that wrote the emission target to
`src/schema/lib.rs` (gitignored) per record 902's literal wording, with
`pub mod schema { include!("schema/lib.rs"); }`. Operator's `e004fc62`
landed `OUT_DIR/schema/lib.rs` with `pub mod schema { pub mod lib {
include!(concat!(env!("OUT_DIR"), "/schema/lib.rs")); } }` shortly
before I would have pushed. Per record 903 (designer rebases off
newest operator main), I abandoned the divergent designer branch
rather than push a competing interpretation. The substance of my
spirit-next plan is now redundant — operator main implements it.

### `schema-rust-next` — superseded by operator main; worktree dropped

Operator's `5ca1c964 emit schema module file paths` already produces
the `schema/<module>/<file>.rs` emission paths reflecting colon-paths.
Nothing for designer to add this pass. Worktree dropped.

### `signal-frame` — out of scope this pass

`signal-frame` still uses the old `signal_channel!` macro stack and is
not yet wired to schema-next. The `schema/signal-frame.concept.schema`
DRAFT is a 6-position older shape (per report 381) and not consumed
by the schema-next pipeline. Migrating signal-frame to the new
schema-next stack is a substantially larger restructure and warrants
its own focused designer pass after operator's stack stabilises.
Worktree dropped.

### `nota-next` — already done by operator

`1c11876b allow colon-qualified nota symbols` already locked in `:`
acceptance at the atom lexer. No designer work needed.

## 5. Open questions for psyche/designer review

1. **Emission target storage — `src/schema/` vs `OUT_DIR/schema/`?**
   Record 902 literally says "another folder in the crate source
   called src/schema/ producing src/schema/lib.rs etc". Operator
   chose `OUT_DIR/schema/lib.rs` (gitignored by Cargo convention).
   Both produce the same module hierarchy from the consumer's
   `mod schema { mod lib { ... } }` declaration. Worth
   psyche confirmation: is `OUT_DIR/schema/` adequate, or should the
   mirror live in `src/schema/` (gitignored, but in-tree) so the
   schema-emitted source is browsable next to hand-written source?
2. **`signal-frame` migration to schema-next** — the concept schema
   already exists in 6-position older shape. The whole crate still
   uses the legacy `signal_channel!` macro stack. When (and how) does
   `signal-frame` move onto schema-next? This is a Maximum-magnitude
   future direction but no dated trigger.
3. **Multi-module loader** — `SchemaPackage::load_lib` only loads
   the single `lib.schema` file. Resolving `module:Type` references
   to sibling `schema/<module>.schema` files (and across crates to
   foreign crates' `schema/lib.schema`) is the next slice. Operator's
   schema-rust-next emits the module-path file structure but
   schema-next's loader doesn't yet read multiple modules. This is
   the highest-value remaining slice toward record 902's full
   intent.

## File anchors

- Branch on disk: `/home/li/wt/github.com/LiGoldragon/schema-next/designer-schema-namespace-and-folder-2026-05-27`
- Schema-next migrated files:
  - `/home/li/wt/github.com/LiGoldragon/schema-next/designer-schema-namespace-and-folder-2026-05-27/schema/lib.schema`
  - `/home/li/wt/github.com/LiGoldragon/schema-next/designer-schema-namespace-and-folder-2026-05-27/schema/core.schema`
  - `/home/li/wt/github.com/LiGoldragon/schema-next/designer-schema-namespace-and-folder-2026-05-27/schema/spirit-min.schema`
  - `/home/li/wt/github.com/LiGoldragon/schema-next/designer-schema-namespace-and-folder-2026-05-27/schema/builtin-macros.schema`
- Updated ARCHITECTURE: `/home/li/wt/github.com/LiGoldragon/schema-next/designer-schema-namespace-and-folder-2026-05-27/ARCHITECTURE.md`
- Operator main converging commits:
  - `schema-next` `807c5250c313` add schema package module entrypoint
  - `nota-next` `1c11876b` allow colon-qualified nota symbols
  - `spirit-next` `e004fc625706` load spirit schema from lib entrypoint
  - `schema-rust-next` `5ca1c964` emit schema module file paths
