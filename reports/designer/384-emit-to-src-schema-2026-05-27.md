# 384 - Emit schema-derived Rust to src/schema per record 909

Designer-assistant lane. Per psyche record 909 (Maximum, 2026-05-27):
schema-derived Rust emits to `src/schema/lib.rs` + `src/schema/<module>.rs`
in the crate source tree, NOT `OUT_DIR/schema/`. Record 902 (Maximum,
2026-05-27) already said this literally; 909 confirms it overrides
operator's `5ca1c964` OUT_DIR choice.

## What changed per repo

### `schema-rust-next` - branch `designer-emit-to-src-schema-2026-05-27`

Commit `2f8cef15` "designer: emit schema-derived Rust to src/schema per record 909"
(derived from operator main `5ca1c964`).

Files changed:
- `src/lib.rs` - `RustModulePath::to_file_path()` now prefixes
  `src/schema/` (single point; method on existing data-bearing type).
- `tests/emission.rs` - two path assertions updated:
  `"src/schema/lib.rs"` and `"src/schema/signal/public.rs"`.

Branch: <https://github.com/LiGoldragon/schema-rust-next/tree/designer-emit-to-src-schema-2026-05-27>

### `spirit-next` - branch `designer-emit-to-src-schema-2026-05-27`

Commit `b0dc496e` "designer: emit spirit schema to src/schema per record 909"
(derived from operator main `e004fc62`).

Files changed:
- `Cargo.toml` - `schema-rust-next` dep now tracks the designer branch
  (will revert to main once operator picks up the change).
- `build.rs` - `SchemaBuild` field set shrunk: `output_directory` field
  removed; `output_path` now `crate_root.join(&generated.path)`. Methods
  remain on the existing `SchemaBuild` impl.
- `src/lib.rs` - `include!(concat!(env!("OUT_DIR"), "/schema/lib.rs"))`
  becomes `include!("schema/lib.rs")` (path relative to `src/lib.rs`).
- `src/schema/lib.rs` - **committed** generated artifact (22976 bytes).
- `Cargo.lock` - dep ref refresh.

Branch: <https://github.com/LiGoldragon/spirit-next/tree/designer-emit-to-src-schema-2026-05-27>

## Test results

- `schema-rust-next` - `cargo test`: 6/6 pass on emission suite.
- `spirit-next` - `cargo build` clean; `cargo test`: 8/8 pass across
  `generated_signal_plane` (3), `process_boundary` (1), `runtime_triad`
  (4) suites.

## Surprises

1. **Only one live `emit_file()` consumer.** `RustEmitter` is also used
   from `schema-rust-next/examples/generate_spirit_fixture.rs`, but that
   calls `emit()` directly (prints to stdout, no path involved).
   `design-deep-spirit-*` repos appeared in grep but report 383
   documents them as superseded prototypes - not live. spirit-next's
   `build.rs` is the only real path consumer.
2. **`OUT_DIR` becomes unused.** spirit-next's `SchemaBuild` previously
   carried `output_directory: PathBuf` (sourced from `OUT_DIR`). With
   emission in `src/schema/`, the field had no remaining caller and was
   removed - keeping `SchemaBuild` tight per verb-belongs-to-noun.
3. **No `.gitignore` rule needed for `src/schema/`** because the
   default chosen is "committed". The file shows up cleanly in
   `jj status` and was included in the commit.

## Decisions surfaced for psyche

**`src/schema/` content: commit or gitignore?** Record 909 said "may be
committed or gitignored depending on workspace policy but the path is
fixed". I chose **committed** for this branch:

- Pro committed: PR diffs show the generated Rust changes (load-bearing
  visibility - the whole point of record 909). Humans and tools see the
  schema-emitted source without a build. No first-time-checkout dance
  ("how do I generate this before running tests?").
- Pro gitignored: Avoids generated content in version control. Smaller
  diffs. Forces the regeneration discipline.

If psyche wants gitignored instead, the change is small: add
`src/schema/` to spirit-next `.gitignore`, drop the committed
`src/schema/lib.rs` blob. The path stays the same per record 909.

## Pending follow-ups

- Operator should pick up `schema-rust-next` `designer-emit-to-src-schema-2026-05-27`
  into main; once landed, the spirit-next Cargo.toml branch ref reverts
  to `main`. (Operator-owned per intent record 515.)
- Hot-reload watch hook (record 902) still deferred.
- Multi-module loader for sibling `schema/<module>.schema` files still
  deferred (carried from report 383 open questions).

## File anchors

- `/home/li/wt/github.com/LiGoldragon/schema-rust-next/designer-emit-to-src-schema-2026-05-27/src/lib.rs`
- `/home/li/wt/github.com/LiGoldragon/schema-rust-next/designer-emit-to-src-schema-2026-05-27/tests/emission.rs`
- `/home/li/wt/github.com/LiGoldragon/spirit-next/designer-emit-to-src-schema-2026-05-27/build.rs`
- `/home/li/wt/github.com/LiGoldragon/spirit-next/designer-emit-to-src-schema-2026-05-27/src/lib.rs`
- `/home/li/wt/github.com/LiGoldragon/spirit-next/designer-emit-to-src-schema-2026-05-27/src/schema/lib.rs`
- `/home/li/wt/github.com/LiGoldragon/spirit-next/designer-emit-to-src-schema-2026-05-27/Cargo.toml`
