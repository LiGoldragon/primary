# Cross-crate schema import — prototype, feasibility verdict, mechanism

*Subagent report (system-designer lane, inherited per record 920). Dispatched
by the meta-report orchestrator's frame `0-frame-and-method.md` §"Subagent
dispatch brief" to PROVE cross-crate schema import works in Nix and land the
mechanism in schema-next + schema-rust-next + a prototype consumer.*

## Feasibility verdict: YES

Cross-crate schema import works, and it works in Nix. The mechanism is Cargo's
`links` manifest key + a build-script `cargo::metadata=schema-dir=<path>` line
+ the `DEP_SCHEMA_CORE_SCHEMA_DIR` environment variable Cargo sets for direct
dependents' build scripts — exactly as the orchestrator's research predicted.
No fallback to `cargo metadata` was needed; `DEP_*` propagation survives
crane's sandbox because Cargo (not Nix) sets it.

Three things proved it, in increasing order of authority:

1. **A throwaway two-crate Cargo workspace** confirmed `DEP_PROBE_CORE_SCHEMA_DIR`
   reaches the consumer's build script with the exact source-dir path the
   dependency's build script advertised.
2. **`cargo test`** on the real `schema-core` workspace (with the feature-branch
   schema-next/schema-rust-next patched in) compiled both crates — running both
   build scripts, so `DEP_SCHEMA_CORE_SCHEMA_DIR` propagated — resolved the
   import, compiled the emitted Rust, and passed 3 type-identity tests.
3. **`nix flake check`** on `schema-core` (the load-bearing witness) — result in
   §"The Nix witness" below.

## What was built — three repos on branch `cross-crate-schema-import`

| Repo | Branch push surface | Change |
|---|---|---|
| `schema-next` | `cross-crate-schema-import` (pushed) | Import RESOLUTION: a resolver mapping crate-name → schema-dir, used during lowering to turn collected imports into resolved external references. |
| `schema-rust-next` | `cross-crate-schema-import` (pushed) | Cross-crate emission: `pub use` alias for each imported type + a `From` bridge for each imported module's `NotaDecodeError`. |
| `schema-core` (NEW repo) | `cross-crate-schema-import` (pushed) | Two-member Cargo workspace proving the mechanism end-to-end + crane `flake.nix` with `nix flake check`. |

Worktrees for schema-next / schema-rust-next under
`~/wt/github.com/LiGoldragon/<repo>/cross-crate-schema-import/`. The new
`schema-core` repo was scaffolded in its canonical ghq checkout and committed
straight onto the feature branch (no `main` exists yet — operators create
`main` when integrating, per the designers-don't-push-to-main rule).

## The mechanism as implemented

### Shape A — minimal two-crate workspace (chosen)

The brief offered Shape A (minimal prototype) vs Shape B (entangle spirit-next).
I chose **Shape A** and realised it as a single new repo `schema-core` holding a
two-member Cargo workspace:

```text
schema-core/
├── core/      package schema-core  — the shared-types crate (declares DatabaseMarker)
└── consumer/  package consumer     — imports schema-core:mail:DatabaseMarker
```

A Cargo workspace was the right call over two separate git-dep repos because
crane builds all workspace members in one derivation, and the `links`/`DEP_*`
mechanism behaves identically for a workspace-member dependency and a `git=`
dependency (Cargo sets `DEP_*` for any direct dependent regardless). One repo,
one flake, one `nix flake check` — the smallest possible Nix witness.

### The flow

1. **`core` advertises its schema dir.** `core/Cargo.toml` declares
   `links = "schema-core"`. `core/build.rs` lowers `schema/mail.schema` to the
   checked-in `src/schema/mail.rs` (the `DatabaseMarker` definition) AND emits
   `cargo::metadata=schema-dir=<core-root>/schema`.
2. **Cargo turns that into `DEP_SCHEMA_CORE_SCHEMA_DIR`** for the consumer's
   build script — `schema-core` → `SCHEMA_CORE` is Cargo's
   uppercase-hyphens-to-underscores normalisation.
3. **`consumer/build.rs` reads it**, registers it on a
   `schema_next::ImportResolver` keyed by crate name, and lowers
   `schema/lib.schema` through the new `lower_source_with_resolver`.
4. **The resolver resolves the import** — it loads `core`'s `mail.schema`,
   confirms `DatabaseMarker` is declared there, and records a `ResolvedImport`.
5. **The emitter references, never re-declares** — `consumer/src/schema/lib.rs`
   gets `pub use schema_core::schema::mail::DatabaseMarker as DatabaseMarker;`
   plus the error bridge, and its local `Output::Marked(DatabaseMarker)` variant
   carries the dependency crate's type.

### Source-dir vs OUT_DIR-staged path

I used the **source-dir path** (`CARGO_MANIFEST_DIR/schema`), not the
OUT_DIR-staged copy. It is simpler, and it works in Nix because the flake's
`schemaFilter` admits the `.schema` files into the build source — the
dependency's schema dir is inside the same workspace source tree, so the path
the metadata advertises exists when the consumer's build script runs. The
OUT_DIR-staged path remains the more robust option if a future consumer's
dependency schema lives outside the build source.

## schema-next changes — import RESOLUTION (the gap closed)

`engine.rs:184 lower_imports` collected `ImportDeclaration`s but never resolved
them. That is the gap. New `src/resolution.rs` adds three data-bearing types
(no free functions, per the Rust discipline):

- **`ImportSource`** — `TryFrom<&Name>` splits a single-colon target
  `crate:module:Type` into its three positions and computes the Rust path
  `crate_identifier::schema::module::Type`.
- **`ResolvedImport`** — carries the local alias + parsed source; `use_item()`
  emits the `pub use … as …;`, `module_path()` gives the dependency module path
  for error bridging.
- **`ImportResolver`** — `with_dependency(crate, schema_dir, version)` registers
  a `SchemaPackage` rooted at the dir's parent; `resolve` loads the dependency
  module schema and confirms the type is declared, erroring otherwise.

`SchemaEngine` gained `lower_source_with_resolver` / `lower_document_with_resolver`.
The existing `lower_document_with_context` now delegates with an empty resolver,
so the legacy collect-only path (and all 39 existing schema-next tests) is
preserved byte-for-byte. `Asschema` carries `resolved_imports: Vec<ResolvedImport>`.
Three new `SchemaError` variants: `MalformedImportSource`, `UnresolvedImportCrate`,
`ImportedTypeNotFound`. 5 new tests in `tests/resolution.rs`.

## schema-rust-next changes — cross-crate emission

Two new `RustEmitter` methods (`emit_imports`, `emit_imported_error_bridges`),
both early-returning on empty imports so existing emission is byte-identical
(the checked-in `spirit_generated.rs` golden test still passes). 2 new tests in
`tests/cross_crate_import.rs`.

The emitted cross-crate reference — the proof, from
`schema-core/consumer/src/schema/lib.rs`:

```rust
// @generated by schema-rust-next

pub type Text = String;
pub type Integer = u64;

pub use schema_core::schema::mail::DatabaseMarker as DatabaseMarker;
// ...
impl From<schema_core::schema::mail::NotaDecodeError> for NotaDecodeError {
    fn from(error: schema_core::schema::mail::NotaDecodeError) -> Self {
        Self::Parse(error.to_string())
    }
}
// ...
pub enum Output {
    Marked(DatabaseMarker),
}
```

No `pub struct DatabaseMarker` anywhere in the consumer — the type's definition
and its rkyv/NOTA impls live in `core/src/schema/mail.rs`; the consumer reaches
them through the alias. The `Marked` variant's NOTA codec calls
`DatabaseMarker::from_nota_block` / `payload.to_nota()` across the crate
boundary, which is what forced the error bridge (see §"Findings worth the
psyche's attention").

## The Nix witness

`schema-core/flake.nix` is modeled on spirit-next's crane setup: vendors
nota-next / schema-next / schema-rust-next as `flake = false` source inputs,
patches the workspace `Cargo.toml` to point at the vendored paths, strips the
git source lines from `Cargo.lock`, admits `.schema` files through a
`schemaFilter`, `strictDeps = true`. The committed inputs point at the
`cross-crate-schema-import` branches of schema-next/schema-rust-next; the
local-override runner (per `skills/testing.md`) points at the worktrees.

Checks: `build`, `test`, `fmt`, `clippy`, plus three witness checks —
`cross-crate-import-mechanism-intact` (anchors the `links` declaration, the
`schema-dir` metadata emission, the `DEP_SCHEMA_CORE_SCHEMA_DIR` read, the
`pub use` alias, and the absence of a local re-declaration),
`no-production-free-functions`, and `local-schema-source-patches`.

`nix flake check` result excerpt (run with the worktree overrides per
`skills/testing.md`; remote builder `prometheus.goldragon.criome`):

```text
cargo-package-deps> Compiling schema-next v0.1.0 (.../vendor-sources/schema-next)
cargo-package-deps> Compiling schema-rust-next v0.1.0 (.../vendor-sources/schema-rust-next)
cargo-package-deps> Compiling schema-core v0.1.0 (.../core)
cargo-package-deps> Compiling consumer v0.1.0 (.../consumer)
...
cargo-package-test>      Running tests/cross_crate_type_identity.rs ...
cargo-package-test> running 3 tests
cargo-package-test> test marker_built_in_schema_core_flows_into_a_local_output_variant ... ok
cargo-package-test> test cross_crate_marker_round_trips_through_the_consumer_nota_codec ... ok
cargo-package-test> test the_local_alias_and_the_dependency_path_name_the_same_type ... ok
cargo-package-test> test result: ok. 3 passed; 0 failed; ...
...
all checks passed!
```

The 9 checks (build, test, fmt, clippy, doc-by-omission, plus the three
witness checks and `cargo-package-deps`) all passed. The consumer crate
compiled means its `build.rs` ran inside crane's sandbox, received
`DEP_SCHEMA_CORE_SCHEMA_DIR` from Cargo, resolved the import, and the emitted
Rust referencing `schema_core::schema::mail::DatabaseMarker` compiled — the
end-to-end Nix proof.

schema-next's OWN flake check (`~/wt/.../schema-next/...`) also passed all
checks (39 schema-next tests including the 5 new resolution tests + fmt +
clippy). schema-rust-next's own flake check cannot run against the
feature-branch schema-next (its flake has no overridable schema-next source
input — it pulls schema-next from `main`, which lacks `ResolvedImport`); its
changes are validated through the schema-core flake, which patches both crates
to their feature branches. Closing that gap (adding a `schema-next-source`
input to schema-rust-next's flake) is a small follow-up.

## Relationship to the existing `Import`/`Export` schema records

**Orthogonal concerns.** Investigated and confirmed:

- The **`{ }` Imports brace** (position 0 of the four-position document) is the
  cross-CRATE import this work resolves. Its entries are
  `{ LocalName crate:module:Type }` pairs → `ImportDeclaration`, now resolved
  against a dependency crate's schema dir.
- The **`Import [SourcePath LocalPath]` / `Export [LocalPath PublicPath]`**
  records in spirit-next's namespace (lines 8-9 of its `schema/lib.schema`) are
  ordinary schema-declared DATA types. `SourcePath`/`LocalPath`/`PublicPath` are
  `[Text]` newtypes. spirit-next's `runtime_triad.rs` test
  `import_export_paths_use_single_colon_namespaces` constructs them with string
  values like `signal:sema:Magnitude` and asserts only their NOTA round-trip —
  there is NO resolution behavior. They are a path-mapping vocabulary (a planned
  intra-schema signal/nexus/sema reuse-namespace feature), and they do nothing
  today but round-trip.

They share the single-colon namespace SHAPE (`a:b:C`) but nothing else. The
cross-crate import resolves to another crate's emitted Rust; the Import/Export
records map namespace strings within one schema's planes. This prototype neither
uses nor depends on the Import/Export records.

## Findings worth the psyche's attention

1. **Cross-crate NOTA codec needs an error bridge.** Each emitted module
   declares its own `NotaDecodeError`. When the consumer's codec calls an
   imported type's `from_nota_block`, the `?` operator needs
   `From<dependency::NotaDecodeError>`. The emitter now writes one `From` impl
   per distinct imported module. This was a real compile failure caught only
   because the imported type was load-bearing in the consumer's codec — a
   shallower proof would have missed it.

2. **The shared-types crate carries a trivial signal plane it doesn't want.**
   The four-position document + the emitter REQUIRE non-empty `Input`/`Output`
   root enums (empty enums produce zero-variant `#[repr]` errors and
   non-exhaustive matches). So `core/schema/mail.schema` has a token
   `(Mark DatabaseMarker)` / `(Marked DatabaseMarker)` plane purely to compile.
   A pure shared-types crate ought to be a types-only module with no signal
   plane. **This is the cleanest next design question** (see open questions).

3. **Generated files need `#[rustfmt::skip]`.** The emitter output is not
   rustfmt-clean for all schemas, and the build.rs freshness check compares
   against raw emitter output — so rustfmt'ing the checked-in file would break
   freshness. spirit-next already solves this with `#[rustfmt::skip]` on the
   `pub mod lib;` declaration; schema-core does the same. Worth noting as a
   standing pattern for every schema-derived crate.

## What's still iteration-N

- **Types-only module shape** for the shared crate (finding 2) — let a schema
  module declare namespace types without forcing a signal plane.
- **Version resolution** — the resolver trusts whatever Cargo resolved (the
  `DEP_*` path points at the resolved version's schema). Single-version
  happy-path only; diamond / transitive version conflicts unaddressed.
- **Transitive imports** — a crate importing a type that itself imports from a
  third crate is untested.
- **Richer cross-crate error typing** — the bridge collapses dependency parse
  failures into the local `Parse(String)` variant.
- **Committed-flake inputs** point at the feature branches; they move to `main`
  when operators integrate schema-next/schema-rust-next.

## What this unblocks

Decision A from `/37/3` — the shared schema home. With cross-crate import
proven, `DatabaseMarker` / `MailLedgerEvent` / mail-marker nouns can live in one
shared crate (`schema-core`, or a `persona-mail`) that both lojix and
spirit-next import, instead of each re-declaring them. The prototype's
`core` crate is the seed of that shared home.

## New Spirit captures

Record 1009 (the directive) was already captured by the orchestrator — not
re-captured. No NEW psyche intent statements arrived during this subagent's
work (the work was execution of an already-captured directive), so no new
Spirit records were created. The findings above (error bridge, types-only
module shape, rustfmt::skip pattern) are agent-discovered design facts, not
psyche intent — they belong in this report and the per-repo INTENT/ARCHITECTURE
files (which were written for schema-core), not in the intent log.
