---
title: 73.2 — Designer-thread digest — the improved NOTA/schema mechanism
role: system-designer
date: 2026-06-05
topics: [nota, schema, structural-macro, asschema, schema-in-rust, resolution, spirit-pilot, pipeline]
description: |
  Digest of the designer thread (reports 504, 511-525) on the improved
  NOTA/schema mechanism: structural macro node = type-directed shape decode;
  schema-is-specialized-NOTA; schema-in-rust replaces Asschema; resolution-as-
  methods; the deserialize-then-lower pipeline. Tracks the evolution and
  records the converged plan plus the 512 spirit-plane-split details relevant
  to the spirit pilot.
---

# Designer-thread digest — the improved NOTA/schema mechanism

This digests the designer thread, separating what is DECIDED (psyche
intent, captured in Spirit) from what is PROPOSED (designer/operator
recommendation pending). The thread runs from the schema-stack design
history (504) through the structural-macro prototype (517) to the
converged Asschema-removal plan (522) and the pipeline framing (524),
with intent-maintenance consolidation in 525.

## (1) What the improved mechanism IS

### The structural macro node — type-directed shape decode (DECIDED)

The load-bearing primitive. Spirit records `ejvc` (mechanism) and `i0e6`
(type-directed clarification), now consolidated into `xai7` (Principle,
VeryHigh) per report 525 §"Consolidated".

NOTA needs a STRUCTURAL MACRO NODE: a special enum whose variants are
matched by STRUCTURE, not by a data tag (report 517 §"The mechanism",
525 tombstone `ejvc`). When an object sits at a structural-macro-node
position the decoder inspects it structurally first — delimiter kind,
sub-object count, sub-object shapes, is-it-a-qualified-symbol, sigil
presence — and selects the FIRST variant whose structural pattern
matches, trying variants in DECLARATION ORDER. Only after the structural
match does NOTA decode the object using that variant's data type,
RECURSIVELY. The mechanism is BIDIRECTIONAL: encoding the Rust enum value
emits a NOTA block matching the chosen variant's structure.

The decisive clarification (record `i0e6`, report 519): **the macro node
IS a TYPE — specifically an enum — and decode is ALWAYS type-directed;
NOTA never parses anything untyped.** The codec has DIFFERENT decode logic
for a macro-node type than for ordinary positional NOTA: a structural
match on each variant in declaration order, first match wins, then
decodes that variant's data, recursively. The enum type IS the whole
specification — runtime registries, capture-maps, and string variant
names are NOT the shape; the type drives the decode. The natural
realization is therefore a DERIVE on the enum, not a runtime
`MacroRegistry` (report 519 §"What this settles relative to the
operator").

This was "the part of the original NOTA design that was never actually
implemented" (525 tombstone `ejvc`).

### Schema is specialized NOTA, not a separate language (DECIDED)

Record `lcwu`, consolidated into `vez8` (Decision, Maximum) per 525.
Schema is NOT a separate language lowered into NOTA — schema is a more
specialized/refined NOTA DIALECT built on structural macro nodes. A
schema file is still FULL NOTA: it decodes and encodes with NOTA, just
with defined structural macros. Schema's sugar syntax — different SHAPES
of object allowed at specific positions — IS structural macros (525
tombstone `lcwu`). The psyche would rather expand NOTA than maintain a
separate lowered language.

### Asschema removal (DECIDED)

Records `pv61` + `fkbz` + `lcwu`, consolidated into `vez8` (Decision,
**Maximum** — restated 3x with rising conviction, the psyche's genuine-
repetition weight-raise; 525 §"Consolidated"). Asschema (assembled
schema) is REMOVED. The structural-macro-node mechanism replaces it: the
typed schema SOURCE is the representation, decoded directly from NOTA, and
Rust emission consumes that typed source rather than a separate assembled-
schema lowering target (525 tombstone `pv61`). This supersedes the
operator's "keep Asschema for now" recommendation (operator report 312).

Report 520 §"What 'remove Asschema' precisely means" decomposes Asschema
into three bundled things: (1) a separate ASSEMBLED IR — **dies**; (2) a
separate LOWERING STEP (`to_asschema()`) — **dies as a step**; (3) the
RESOLUTION WORK + resolved-type vocabulary (inline hoisting, visibility,
ordering, symbol paths) — **survives**, relocated onto the typed source.

### Schema-in-rust + the pipeline (DECIDED)

Record `fkbz` (the pipeline), report 524. The canonical pipeline is two
arrows, NOT a separate assemble phase (524 §"What each arrow is"):

```
schema (NOTA)  ──deserialize──▶  schema-in-rust  ──lower──▶  rust-interfaces-code
            (structural macro codec,        (rkyv-serializable,      (the emitter)
             bidirectional)                  faithful typed image)
```

- **Arrow 1 — deserialize.** Authored `.schema` NOTA deserializes,
  through the structural-macro-node codec, into Rust types that DEFINE
  THE SCHEMA FULLY (schema-in-rust). Because the codec is bidirectional,
  schema-in-rust is a faithful typed image that round-trips CANONICALLY
  (semantic/canonical equality, not original-byte identity — operator
  316, conceded; 524 §"What each arrow is"). This is DESERIALIZE, not
  lower/assemble: nothing semantic is transformed away. schema-in-rust is
  rkyv-serializable.
- **Arrow 2 — lower.** The emitter (schema-rust-next) takes schema-in-rust
  and lowers it into Rust interface code. This is where the Rust-specific
  projection happens.

Contrast with the OLD pipeline (524 §"Why this is 'no Asschema'"): old
was `schema ──lower/assemble──▶ Asschema ──emit──▶ rust` (a one-way,
lossy assemble producing an IR that did not round-trip). New reaches the
same destination role (the typed representation the emitter consumes) by
a faithful codec instead of a lossy assemble.

### Resolution-as-methods, no separate IR (DECIDED, with one small open seam)

The pipeline framing (524) and the psyche's "isn't that what the
datatypes are for?" pushback (523) jointly SETTLE the
SchemaResolution-object question that 520/522 had left open. **There is no
separate resolved-view object.** schema-in-rust IS the typed
representation; resolution work lives as METHODS on schema-in-rust's
types, computed during arrow 2 (524 §"This settles the SchemaResolution
question").

Report 523's decomposition of Asschema's 9 resolution jobs against the
datatypes (523 table): ~5 are INHERENT in well-designed datatypes (newtype
collapse, reserved scalars, nested inline declarations, visibility, source
order — free the moment schema deserializes into them); 1 is a TRIVIAL
METHOD (Pascal→snake field naming); 2 are CROSS-REFERENCE READ-METHODS
(symbol-path resolution, variant-payload resolution — need the namespace
in scope); 2 are RUST PROJECTION (nested-inline → sibling structs;
emission ordering — the emitter's job); 1 DISAPPEARS (context aggregation,
a lowering-phase artifact). "None of it is a separate resolution engine,
and none of it needs a SchemaResolution IR" (523 §"The conclusion").

This preserves the operator's boundary (314): schema-in-rust owns schema
meaning (as methods); the emitter owns Rust projection. The emitter calls
HIGH-LEVEL semantic methods, not primitive getters, so it stays a Rust
projector and not a second schema engine (524 §"Adopted refinements",
operator 316 precision 3).

## (2) Evolution across the reports — how the design converged

The thread converged in seven moves:

- **504 (design history) — the OLD world.** Documents the four-logical-
  planes model (`Asschema` data / `AsschemaArtifact` file / `AsschemaStore`
  persistence / `RustEmitter`, Spirit 1272) and the two-layer parser with
  a runtime `MacroRegistry` (ordered `Vec<MacroNodeDefinition>`,
  `dispatch` first-match). This is the baseline the structural-macro work
  REPLACES: it still has Asschema as a distinct lowering target and macros
  as a runtime registry, not a type-derive.

- **517 (prototype) — the mechanism proven on one position.** A working
  `nota-next` branch demonstrates a structural macro node (a
  `TypeReference` enum) round-tripping NOTA text → Rust → NOTA by shape
  alone, declaration-order first-match, recursive. Hand-written
  `from_block` + `Display`. Names the endpoint: a `#[derive(...)]`. Honest
  scope: one position, Asschema not yet deleted.

- **518 (designer vs operator) — two implementations, one tension.** Both
  designer and operator independently built the mechanism from the same
  prompt (strong convergence evidence). Operator's is integrated into real
  schema-next and reuses the registry `Pattern`/captures; designer's is a
  direct typed `BlockShape` dispatch. 518 surfaces the decisive critique:
  the operator's path computes the structural match, throws it away, and
  recovers the variant from a `macro_name()` STRING (the string-matching-
  as-dispatch anti-pattern). Recommends synthesis toward the DIRECT typed
  dispatch, reified.

- **519 (the type-derive) — `i0e6` resolves the fork.** The psyche's
  clarification (the macro node IS a type; the type drives the decode)
  picks the direct path. Built as `#[derive(StructuralMacroNode)]` — a
  SECOND derive distinct from the existing tag-based `NotaDecode`; the enum
  + per-variant `#[shape(...)]` attributes ARE the whole spec. No runtime
  registry, no capture-map, no string dispatch.

- **520 (Asschema removal design) — grounds the removal.** `pv61`
  decision turned into a full consumer map, resolution inventory, target
  architecture (`SchemaSource` + `resolve()` projection), 5 migration
  slices, and ONE crux for the psyche: pragmatic (`resolve()` projection)
  vs strong (emitter walks source directly). Recommends pragmatic.

- **521 (operator-vs-designer derive) — the landed state + intent-dup
  flag.** Operator landed designer's `#[shape]` front-end on main with
  their own captures/string back-end plus exact-duplicate conflict
  detection. The decode fork persists; `i0e6` favors the direct path.
  First flags the `js6q`/`pv61` intent duplication.

- **522 → 523 → 524 (convergence + simplification).** 522 settles the
  crux to PRAGMATIC (operator 314's boundary argument; designer concedes)
  with an ephemeral-projection guardrail and adopts `SchemaResolution`
  naming + 7-step sequence. 523 (psyche pushback: "isn't that what the
  datatypes are for?") shows the projection is mostly unnecessary
  scaffolding. 524 (the pipeline, `fkbz`) lands the final shape:
  schema-in-rust IS the typed representation, resolution is methods on it,
  NO `SchemaResolution` type. The three positions (psyche / operator /
  designer) reconcile.

- **525 (intent maintenance) — consolidation.** The genuine psyche
  repetition collapses into two records: `xai7` (mechanism) and `vez8`
  (direction/pipeline, raised to Maximum). Seven duplicate/superseded
  records tombstoned (`ejvc`, `i0e6`, `lcwu`, `pv61`, `fkbz`, `js6q`,
  `ydvg`). Active truth is now `xai7` + `vez8`.

## (3) The converged plan and open questions

### The converged migration (522 §"The implementation-ready sequence",
refined by 524 §"What this changes in the migration")

522's 7-step sequence with 524's one simplification (no `SchemaResolution`
type to introduce):

1. Make `SchemaSource` the faithful rkyv-serializable schema-in-rust
   (finish moving the `Source*` types onto the structural-macro decode;
   derive rkyv). 520 §"The decode side is mostly already there": most
   `Source*` types ALREADY decode by structure via inherent `from_block`;
   only `SourceVariantSignature` uses the formal derive today, so the
   type-directed decode is largely in place — the real work is relocating
   resolution and rewiring emission.
2. Put the resolution work as METHODS on `SchemaSource`'s types (the body
   of `to_asschema` becomes methods the lowering reads).
3. `RustModule::from_source` lowers schema-in-rust into Rust — calling
   those methods + doing Rust projection.
4. Build driver: deserialize `.schema` → schema-in-rust → lower; no
   `.asschema`.
5. Delete `Asschema`/`AsschemaArtifact`/`AsschemaStore` once no consumer
   remains (multi-repo: spirit, cloud, domain-criome, upgrade,
   signal-cloud).

Safety net (DECIDED as method, from 522/314): two layers — (a)
per-transformation tests FIRST (hoisting order, visibility, root
bare-header payload resolution, inline root insertion, single-field
newtype collapse, derived field naming, enum-variant payload resolution,
reserved-scalar validation, import preservation, symbol-path parity); then
(b) the byte-identical Rust-emission witness (old Asschema path vs new
schema-in-rust path must diff to zero), spirit first then a multi-plane
package. Note the two distinct round-trips (524 §"What each arrow is"):
the SCHEMA round-trip is CANONICAL; the EMISSION diff is BYTE-EXACT.

### Refinements adopted (from operator 316, 524 §"Adopted refinements")

- Canonical round-trip, not byte-identical, for the schema codec.
- rkyv on the CLEAN schema value: keep the structural-macro decode
  producing span-free typed values by construction (spans are a decode-
  time error-reporting concern on the `Block`, not carried into the
  value), so schema-in-rust IS the clean rkyv value — no separate
  clean-value projection.
- The emitter calls HIGH-LEVEL semantic methods, not primitive getters.
- No PUBLIC `SchemaResolution`; a PRIVATE traversal context/cache is fine
  if implementation needs one, kept internal to schema-next. The public
  handoff is `SchemaSource`.

### Open questions the designer thread flags

- **The one genuinely-open seam (523 §"The one genuinely-open seam").**
  Do the two cross-reference lookups (variant-payload, symbol-path)
  resolve at DESERIALIZE-time (baked in while the namespace is in scope)
  or at READ-time (datatype holds the bare reference; emitter looks it up)?
  Both fine; read-time keeps the datatype a faithful image (more "just
  NOTA"). Small, local — not the "where does the resolution engine live"
  question.

- **Who drives the migration, and where (522 §"The one open item").** A
  coordination call, not a design call. schema-next/schema-rust-next
  `main` are operator-owned. Two workable splits: operator drives on main
  with the converged spec (they own both repos and wrote the sequence,
  designer reviews); OR designer prototypes the slice 1-3 spine on a `~/wt`
  feature branch, operator integrates. The DESIGN is settled either way.

- **The persistent decode fork (521 §"Recommended end-state").** Main
  carries designer's `#[shape]` front-end + operator's captures/string
  back-end. Recommended (PROPOSED, pending acceptance): swap the generated
  decode from `from_structural_match` on `macro_name()` (string) to the
  direct typed `from_structural_block` (fuse match + construction); keep
  and STRENGTHEN conflict detection from exact-pattern-equality to
  SUBSET/SHADOWING detection (a general head declared before a specific one
  it subsumes — the more dangerous footgun neither implementation catches).

- **Pattern-vocabulary completeness (517/519 honest scope).** Current
  `#[shape]` vocabulary is the minimal three (`pascal_atom`,
  `head`+`arity`, `pascal_head`+`arity`). Per-slot sub-shapes, sigil-aware
  shapes (`Name@{...}`), variable-arity bodies, literal-unit variants, and
  sequence positions (`from_blocks`) are the next additions before all of
  schema's sugar is covered.

- **Intent-capture discipline (525 §"Going forward").** PROPOSED, pending
  psyche/operator agreement: for a live design thread the psyche conducts
  with a specific lane, THAT lane owns intent capture; the other lane
  gap-checks rather than re-capturing. Root cause of the 3 duplicate pairs
  (`24ds`, `js6q`/`pv61`, `ydvg`/`fkbz`).

## (4) Report 512 — what is directly relevant to the spirit pilot

Report 512 (bead `primary-9hx0`) is the spirit-plane-schema split, and
spirit is named the "clean bootstrap-exception EXEMPLAR every future triad
port copies." Points directly load-bearing for modifying the spirit pilot:

- **spirit gets its OWN `schema/signal.schema`; it does NOT import
  signal-spirit (512 §"The signal-spirit question — resolved Reading B").**
  Four facts settle it: no Cargo dependency / no `links` key; spirit
  generates wire types from its own schema (`build.rs` loads the schema,
  daemon consumes `crate::{Input, Output, InputRoute, OutputRoute}`);
  the roots diverge (spirit has SIX operations + EIGHT replies vs
  signal-spirit's one-op MVP; even `RecordAccepted` maps to `SemaReceipt`
  in spirit but `RecordIdentifier` in signal-spirit); and signal-spirit's
  CLEAN mark is about leak-absence, not liveness. Reconciling the external
  signal-spirit MVP with spirit's real six-op surface is a SEPARATE
  follow-up that must not block the split.

- **The split is INTRA-CRATE three-file (512 §"The exemplar uses the
  intra-crate three-file shape").** All three plane files live INSIDE the
  spirit crate. `nexus.schema` and `sema.schema` import the Signal roots
  via the self-package form `spirit:signal:Input`. This matches the
  schema-next `tests/fixtures/plane-crate/` working fixture (which actually
  lowers), not the never-built cross-crate cloud/domain-criome form. The
  self-registration `ImportResolver::new().with_package(...)` lets
  intra-crate imports resolve with no external dependency.

- **Root partition — three planes (512 §"Root partition").** Signal =
  wire operation roots + reply roots + all wire payload/leaf types. Nexus
  = daemon decision language (`NexusWork`/`NexusAction` + the stash effect
  sub-language). Sema = durable read/write vocabulary. Reuse plumbing and
  the mail-ledger types are DROPPED (vestigial / unwired). Sema root
  naming: use unprefixed `WriteInput`/`ReadInput` INSIDE `sema.schema`,
  apply `Sema`-prefixed names as import aliases in `nexus.schema` (keeps
  the daemon-facing language byte-identical to today's `lib.schema`).

- **Four-block document grammar (512 §"The four-block document shape").**
  Each `.schema` file is exactly: block 1 `{}` imports brace
  (`LocalAlias crate:module:Type` pairs); block 2 `[]` Input root enum;
  block 3 `[]` Output root enum; block 4 `{}` namespace of user-defined
  types (`Name body` pairs). Import grammar `crate:module:Type` (single
  colon, three positions); `module` is the schema FILE STEM.

- **Authorable now vs blocked on the driver (512 §"Authorable now").**
  The three schema files are pure NOTA, depend only on the published import
  grammar + the schema-rust-next `RustEmissionTarget` variants — writable
  immediately. The `build.rs` migration + Rust regeneration + freshness
  assertion is the driver's job (bead `primary-qhi6`), a clean swap to a
  three-module `GenerationPlan` (`wire_contract_module("signal")` +
  `nexus_runtime()` + `sema_runtime()`).

Two adjacent corrections from the runtime thread that override 512's
emission targeting:

- **512 used `WireContract` for spirit's own signal schema; this is the
  BUG report 514 diagnosed and 515 fixed.** A daemon's own signal schema
  must emit to `SignalRuntime` (which emits `SignalEngine`), NOT
  `WireContract` (which emits zero engines). The landed answer (515) is a
  FIFTH emission target `RustEmissionTarget::SignalRuntime`
  (`signal_only()` planes). spirit's `build.rs` calls
  `signal_runtime_module("signal") + nexus_runtime() + sema_runtime()`.
  Report 514's own SUPERSEDED header and report 515 §"My spirit-plane-split
  branch is superseded" record this: the designer's earlier
  `spirit-plane-split` branch (which used `wire_contract_module`) should
  be ABANDONED, not integrated — it was the symptom.

- **"Signal schema" names TWO different files (515 §"The conceptual
  correction").** The PUBLIC signal CONTRACT (`signal-<component>`,
  separate repo, `WireContract`, zero engines) vs the DAEMON-LOCAL signal
  RUNTIME (`<component>/schema/signal.schema`, inside the daemon crate,
  `SignalRuntime`, emits the `SignalEngine` trait). For spirit: the daemon
  emits `SignalEngine` from its OWN `signal.schema`, never from the
  contract. Each of the three planes emits exactly one engine bound to one
  daemon actor: Signal→`SignalEngine`→`SignalActor`,
  Nexus→`NexusEngine`→`Nexus`, SEMA→`SemaEngine`→`Store`.

## Decided-vs-proposed summary

DECIDED (psyche intent in Spirit): the structural macro node = type-directed
shape decode (`xai7`); schema is specialized NOTA (`vez8`); Asschema removed
(`vez8`, Maximum); the deserialize-then-lower pipeline with schema-in-rust as
the typed representation and resolution as methods, no SchemaResolution IR
(`vez8`); each daemon plane is its own schema, contracts wire-only
(records 2593/2598/2604, embodied in 511/512/515).

PROPOSED / pending: the exact `#[shape]` pattern vocabulary; swapping the
landed string-dispatch decode for the direct typed decode (521); strengthening
conflict detection to shadowing (521); deserialize-time vs read-time for the
two cross-reference lookups (523); the migration drive-split (522); the
one-capturer-per-thread discipline (525). The 512 spirit-split file partition
is authorable now but its emission TARGETS must follow 515 (`SignalRuntime`,
not `WireContract`).
