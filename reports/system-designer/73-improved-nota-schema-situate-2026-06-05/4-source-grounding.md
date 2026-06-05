# 4 — Source grounding: landed vs proposed in actual code

Read-only grounding of the improved NOTA/schema mechanism against source under
`/git/github.com/LiGoldragon/`, as of 2026-06-05. Honest landed-vs-proposed,
per repo, with file:line / commit evidence.

## Which repos are live (don't be fooled by name collisions)

There are two generations of repos. The LIVE stack is the `-next` triple plus
the spirit pilot; the un-suffixed `nota` / `nota-codec` / `schema` /
`schema-rust` are the OLD generation and are NOT the active pipeline.

Live dependency graph (from `Cargo.toml`):
`nota-next` ← `schema-next` ← `schema-rust-next` ← `spirit`.

- `schema-next/Cargo.toml:16` → `nota-next` (git, branch main).
- `schema-rust-next/Cargo.toml:16,31` → `schema-next` + `nota-next`.
- `spirit/Cargo.toml:53` → `schema-rust-next` (git, branch main).

`nota-codec` (HEAD `24e7823`, last src commit `323a3a7` "add structural value
shape layer", May 25) is the OLD codec; its structural work was superseded by
`nota-next`. The active NOTA repo per `nota-next/INTENT.md` is explicitly
nota-next: *"The raw NOTA replacement repository is nota-next … not a
branch-only temporary surface."*

## 1. Structural macro node — IMPLEMENTED and landed in `nota-next`

The structural macro node is a real, working mechanism in `nota-next`, decoded
by SHAPE in declaration order, type-directed. It is the most-landed piece of the
new direction.

- The decode-by-shape engine: `nota-next/src/macros.rs`. `StructuralVariant`
  (line 387) carries name + `Pattern` + expected-shape diagnostic;
  `StructuralVariantSet::dispatch` (line 469) tries variants **in declaration
  order** at a `PositionPredicate` and returns the first structural match — no
  data tag, pure shape match. `validate_no_silent_conflicts` (line 492) rejects
  a variant set where an earlier general shape would shadow a later one (e.g. a
  Pascal-headed parenthesis shadowing a same-arity literal-headed variant —
  `ParenthesizedHeadShape::silently_shadows`, line 901).
- The typed enum bridge trait: `StructuralMacroNode` (line 1267).
  `from_structural_nota` (line 1276) parses source → single root → dispatch →
  typed Rust value; `to_structural_nota` (line 1274) is the reverse. This is the
  "a NOTA enum decoded by SHAPE, type-directed" intent, in code.
- The derive: `nota-next/derive/src/lib.rs:23`
  `#[proc_macro_derive(StructuralMacroNode, attributes(shape))]`. It generates
  the ordered `structural_variants()` list and the direct decode/encode from the
  enum's **declaration order** and per-variant `#[shape(...)]` attributes
  (`pascal_atom`, `head = "..." arity = N`, `pascal_head arity = N` —
  enumerated at lib.rs:895-905). Codegen builds the variant list at line 678 and
  the `from_structural_candidate` dispatch at line 715.
- Direct decode (not registry-mediated) is the CURRENT state: HEAD commit
  `fb600e3` "nota structural macro node direct decode" (Fri Jun 5 11:32),
  preceded by `f066805` "derive structural macro node enums" and `a9a34f6`
  "make structural macro nodes typed codec variants". So as of today the derive
  decodes a `MacroCandidate` directly into the typed value rather than going
  through the global `MacroRegistry`.
- Round-trip proof: `nota-next/examples/structural_macro_round_trip.rs` (the enum
  type IS the specification) and `nota-next/tests/macro_nodes.rs`.

Current-state nuance: there is BOTH a lower-level `MacroRegistry` (line 991, a
runtime registry of `MacroNodeDefinition`s) AND the typed `StructuralMacroNode`
derive. `nota-next/ARCHITECTURE.md` is explicit that the registry "is not the
conceptual home of typed macro nodes" — it is "useful for low-level exploration
and schema's existing transitional matcher." The typed enum path is the intended
home; the registry is transitional.

## 2. Asschema — NOT removed. It is a live COMPATIBILITY projection.

This is the load-bearing correction to the scout. Intent `vez8` says "ASSCHEMA
IS REMOVED." In source, asschema is **present, live, and explicitly retained as
a compatibility surface** in both schema-next and schema-rust-next. Removal is
the stated TARGET, not the landed state.

Evidence it is present:
- `schema-next/src/asschema.rs` exists (the `Asschema` type, `Name` codec, etc.).
- `schema-rust-next` commit `038fa23` (Fri Jun 5 10:05) is literally titled
  "mark asschema as **compatibility input**" — a marking pass, not a removal.
- `schema-rust-next/src/lib.rs` still exposes `RustEmitter::emit_file(&Asschema)`
  (line 52), `emit_module(&Asschema)` (line 98),
  `emit_file_from_artifact(&AsschemaArtifact)` (line 74),
  `emit_file_from_nota_path` (line 78), `emit_file_from_binary_path` (line 86).
  `RustModule::from_asschema` (line 127) is still the core mapping.

What replaced the assemble step (resolution-as-methods on schema-in-rust):
PARTIALLY landed. The new typed source value `SchemaSource` exists
(`schema-next/src/source.rs:20`) and is the authored-source boundary:
`from_schema_text` (line 28), `to_schema_text` (line 92), rkyv `to/from_binary_bytes`
(lines 102-110). But `SchemaSource::lower` (line 112) and `to_asschema`
(line 120) **still produce an `Asschema`** as an internal intermediate before
Rust emission. So resolution now runs as methods on `SchemaSource` /
`SourceTypeResolver` (line 126: `SourceTypeResolver::from_source`), but the
output of that resolution is still the `Asschema` data shape, which the emitter
then consumes. The resolution moved onto schema-in-rust types; the `Asschema`
*data endpoint* did not yet go away.

Authoritative intent statements in source confirming "compatibility, not
removed":
- `schema-rust-next/INTENT.md:263-271`: "The emitter currently starts from
  assembled schema data as a compatibility surface … The **target after Asschema
  retirement** is the schema-in-Rust pipeline."
- `schema-rust-next/INTENT.md:273-278`: artifact paths "are retained only until
  the structural schema-source handoff replaces Asschema."
- `schema-rust-next/ARCHITECTURE.md:41-46`: "`Asschema` remains a compatibility
  input and artifact surface … the shared generation driver no longer
  materializes `.asschema` files as normal generated component artifacts."
- `schema-next/ARCHITECTURE.md:106-122` (§"Compatibility Asschema Endpoint"):
  "`Asschema` is the current compatibility data endpoint … Asschema is retained
  as the current compatibility [endpoint]."

So: the DESIGN says remove asschema; the CODE keeps it as the live intermediate
and explicitly defers removal. One real removal already happened: the shared
driver no longer writes/freshness-checks `.asschema` files as component outputs
(ARCHITECTURE.md:138-140, INTENT.md:101-104) — see §3.

## 3. The current pipeline in code, RIGHT NOW

Authored `.schema` (NOTA) → `SchemaSource` (typed, rkyv) → `Asschema`
(compatibility intermediate) → `RustModule` → generated `src/schema/*.rs`.

Step by step, with entry points:

1. **Load.** `SchemaPackage::load_module(module)` reads
   `{schema_dir}/{module}.schema` — `schema-next/src/module.rs:47-48`
   (`format!("{}.schema", …)`). Note: it reads **`.schema`**, never `.asschema`.
2. **Structural decode to typed source.** `SchemaModuleSource::to_schema_source`
   → `SchemaSource::from_schema_text` → `from_document`
   (`schema-next/src/source.rs:28-74`). This walks the `nota-next::Document`
   root objects (imports? + input + output + namespace). NOTE: the *top-level*
   `SchemaSource::from_document` is **hand-written `from_block` recursion**, not
   the `StructuralMacroNode` derive. The structural-macro-node trait is used at
   ONE leaf type so far: `impl StructuralMacroNode for SourceVariantSignature`
   (`schema-next/src/source.rs:876`). So structural-macro-node decode is landed
   in nota-next and *adopted at one leaf* in schema-next; the bulk of schema
   source decode is still hand-written shape matching.
3. **Source round-trip witness.** The driver round-trips
   `SchemaSourceArtifact` (text→source→text) and fails on mismatch —
   `schema-rust-next/src/build.rs:~430` `SourceArtifactRoundTrip::validate`.
4. **Lower to Asschema (compatibility).** `RustEmitter::emit_file_from_schema_source`
   (`schema-rust-next/src/lib.rs:60`) internally lowers SchemaSource→Asschema
   via `SchemaEngine`/`SourceTypeResolver`, then `RustModule::from_asschema`.
5. **Emit Rust + freshness check.** `GeneratedModule::from_emission`
   (`schema-rust-next/src/build.rs:380-405`) produces the `rust_file`;
   `check_generated_artifacts` (line ~407) freshness-checks ONLY the generated
   Rust file (`rust_artifact`), NOT any `.asschema`. `write_or_check(ENV)`
   (lib.rs/build.rs `FreshnessCheck::from_environment`) writes when the env var
   is set, else checks.

Entry point for a component build: `schema_rust_next::build::GenerationDriver::new(plan).generate().write_or_check(ENV)`
with `GenerationPlan::{wire_contract, daemon_runtime, component_runtime_compatibility}`
(`schema-rust-next/src/build.rs:33,41,51`). Generated Rust lands in the
consumer's `src/schema/` (header `// @generated by schema-rust-next`,
e.g. `spirit/src/schema/signal.rs:1`).

## 4. The spirit pilot — already on the NEW pipeline; `.asschema` is residue

Decisive for whether report-72's implementation approach holds.

**spirit's build already consumes `.schema`, not `.asschema`.** `spirit/build.rs`
calls `GenerationDriver::new(plan).generate().write_or_check("SPIRIT_UPDATE_SCHEMA_ARTIFACTS")`
(lines 35-39) over `ModuleEmission::{signal_runtime_module("signal"),
nexus_runtime(), sema_runtime()}` (lines 32-34). The driver's `load_module`
reads `signal.schema` / `nexus.schema` / `sema.schema` (the `.schema` path,
module.rs:48), lowers through `SchemaSource`, and freshness-checks ONLY the
generated `src/schema/*.rs`. So spirit is on the SchemaSource pipeline today.
The authored `schema/signal.schema` is real authored NOTA (positional, name-first
`@`-less roots, e.g. `[Record Observe Lookup …]` enum lists, namespace brace).

**The `.asschema` files in spirit are residue, not build inputs.** They are:
- Still committed (`git ls-files schema/`: signal/nexus/sema `.asschema` all
  present alongside `.schema`).
- Listed as `cargo:rerun-if-changed=schema/{signal,nexus,sema}.asschema`
  (build.rs:22,25,28) — stale watch targets, not consumed by the driver.
- Used only as TEST FIXTURES:
  `spirit/tests/operator_271_closed_claims.rs:24-26` `include_str!` the three
  `.asschema` files for a "lifted artifacts carry typed records" claim
  (test at line 150).

**`SPIRIT_UPDATE_SCHEMA_ARTIFACTS` still exists** (build.rs:38) but its meaning
changed: it now gates regeneration/freshness of the **generated Rust files**,
NOT `.asschema` materialization. There is **no `build.rs` version literal that
propagates into `.asschema`** — the version string is `"0.1.0"` passed to
`GenerationPlan::new(&crate_root, "spirit", "0.1.0")` (build.rs:31), used as the
schema package version for generation/identity, not stamped into `.asschema`
headers by the driver (driver no longer materializes `.asschema`).

**spirit's INTENT.md is STALE relative to its own build.rs.** `spirit/INTENT.md:24-32`
and :60 still describe the old behavior — "Build code compares those
[`.asschema`] … materialized as `.asschema` text … compares the generated
`.asschema` and Rust artifacts with the checked-in files." That contradicts the
actual driver, which freshness-checks only the Rust file and explicitly does NOT
materialize `.asschema` (schema-rust-next ARCHITECTURE.md:138-140). spirit's
INTENT.md needs a manifestation pass to match the landed pipeline. (Flagged for
the situate/overview sub-agents.)

## Bottom line for report-72's approach

The scout's framing ("asschema is removed") over-states the landed state, and
report-72's migration mechanism leaned on it the wrong way:

- The structural-macro-node decoder is REAL and landed in nota-next, adopted at
  one schema-next leaf. Type-directed shape decode works.
- asschema is NOT removed; it is the live compatibility intermediate, with
  removal explicitly deferred ("target after Asschema retirement").
- The spirit pilot is ALREADY on the new SchemaSource pipeline: it builds from
  `.schema`, freshness-checks generated Rust, and treats `.asschema` as residue
  (committed test fixtures + stale rerun-watch). So report-72's implementation
  surface is the authored `schema/*.schema` files + `src/schema/*.rs`
  regeneration via `SPIRIT_UPDATE_SCHEMA_ARTIFACTS`, NOT `.asschema` headers /
  a `.asschema`-materializing build. The parts of report-72 that referenced a
  `build.rs` version literal propagating into `*.asschema` and
  `.asschema` regeneration are outdated and must be re-grounded: the record-shape
  change lands by editing `schema/signal.schema` and regenerating
  `src/schema/signal.rs`. The flat-Entry change itself is unaffected.
- Cleanup the pilot still owes: delete the residual `.asschema` files (or demote
  to fixtures only), drop the `.asschema` rerun-watch lines, and fix spirit's
  INTENT.md to describe the `.schema`→SchemaSource→Rust pipeline. None of this
  blocks the report-72 record-shape work; it does mean report-72's mechanism
  section needs the correction above.
