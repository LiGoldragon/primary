# 5 — Situate and implications: the improved NOTA/schema mechanism vs our Spirit-record thread

System-designer situate synthesis. Reconciles the improved NOTA/schema
mechanism (gather files 1-4 in this directory) with our in-flight Spirit
intent-record redesign (reports 71/72) and the lojix/horizon adoption
threads. Reads the mechanism off DEPLOYED Spirit intent (`vez8`, `xai7`,
…) and off actual source under `/git/github.com/LiGoldragon/`, separating
landed from proposed. Three parts: (A) what the mechanism IS, (B) how it
situates against our prior work, (C) the exhaustive touch-list plus the
numbered psyche clarifications our thread needs.

The single most load-bearing finding: **report 72's record-shape design
and its migration mechanism are both partly superseded — the record shape
by the flat-Entry / `m27p` direction, and the migration mechanism by the
Asschema-removal direction (`vez8`) plus the fact that spirit's build
already does NOT materialize `.asschema`.** Neither invalidates the
substance (flat Entry + Relations + Weight + hash identity + clean break);
both require a re-grounding pass. Details in part B.

## Part A — What the improved mechanism IS (source-grounded, landed vs proposed)

### A.1 The shape, in three stages

Authored schema is FULL NOTA — schema is a specialized NOTA dialect built
on structural macro nodes, not a separate language that lowers into NOTA
(`vez8`, Decision, Maximum; `lcwu` consolidated in). The canonical
pipeline is two arrows, no intermediate assembled IR:

```
schema (.schema, NOTA)  ──deserialize──▶  schema-in-rust  ──lower──▶  rust-interface-code
        (structural-macro            (typed, rkyv-serializable,        (the emitter:
         codec, bidirectional)        canonical-round-trip image)       Rust projection only)
```

- **Arrow 1 (deserialize).** Authored `.schema` deserializes, through the
  structural-macro-node codec, directly into typed Rust that FULLY defines
  the schema (schema-in-rust). Faithful canonical round-trip, NOT
  byte-identical source preservation (`fz9n`, High; `vez8`). rkyv-
  serializable on the clean value (spans are decode-time error-reporting
  on the `Block`, not carried into the value).
- **Arrow 2 (lower).** The emitter (`schema-rust-next`) lowers
  schema-in-rust into Rust interface code. This is Rust PROJECTION only,
  not schema semantics. The resolution work the old Asschema performed
  (inline-declaration hoisting, visibility, ordering, symbol paths) now
  lives as METHODS on schema-in-rust types, invoked during lower. The
  emitter calls HIGH-LEVEL semantic methods, not primitive getters, so it
  stays a Rust projector and not a second schema engine (`fz9n`; operator
  314/316).

There is NO public `SchemaResolution` IR (`fz9n`). The psyche's "isn't
that what the datatypes are for?" pushback (designer 523) settled this:
of Asschema's 9 resolution jobs, ~5 are inherent in well-designed
datatypes, 1 a trivial method (Pascal→snake), 2 cross-reference read-
methods, 2 Rust-projection, 1 disappears (designer 523/524).

### A.2 The structural macro node — the codec primitive

`xai7` (Principle, VeryHigh; `ejvc`+`i0e6` consolidated), refined by
`z544` (Clarification, High). A structural macro node is **a NOTA enum
decoded by SHAPE, not by a data tag**. The enum TYPE is the whole
specification; decode is TYPE-DIRECTED: the codec structurally matches
each variant in DECLARATION ORDER, first structural match wins, then
decodes that variant's data RECURSIVELY (a variant may itself hold further
structural macro nodes). Encode emits a NOTA block matching the chosen
variant's shape — BIDIRECTIONAL. Explicitly NOT a runtime registry, NOT a
capture-map, NOT string variant-name dispatch. Realized as a derive,
`#[derive(StructuralMacroNode, attributes(shape))]`. The psyche frames it
as "the part of NOTA original design that was never implemented."

### A.3 Adjacent decided pieces (situate-relevant)

- **One lowering engine** (`58bv` High; `mxo5` Zero/probing). Schema-next
  keeps exactly one lowering, the MOST-correct not the smallest. Schema
  acts as its own codec — the shorthand source form round-trips through
  the schema codec (`xsp1` High).
- **Codec opt-in** (`bkcd` High; `hu8i` Maximum). rkyv is the universal
  wire base; the NOTA codec (NotaDecode/NotaEncode) is OPT-IN per consumer
  — double clients (CLI, text+binary) get the NOTA derive, binary-only
  consumers (the daemon) must NOT compile NOTA impls in. Schema and
  schema-emitted Rust sit on the SAME NOTA typed interfaces direct Rust
  code uses — no parallel mini-codec per generated schema.
- **Typed emission** (`zhjg` Zero; `kuw2` Medium; `dtwe`/`fhaj`/`6th4`
  High; `epn9`/`q13r`/`u1nr` High). Emission moves from hand-indented
  `format!` to a RustItem/RustImplBlock/RustMatch token model; generated
  Rust emits into a dedicated `src/schema/` module tree; bare namespace
  bindings lower to `TypeDeclaration::Alias`; every root enum auto-gets a
  recursive `Help` action; more runtime behavior (default trait wrappers,
  tracing) pushes into the schema-generated interface.

### A.4 Landed vs proposed (the honest line — gather file 4)

**LANDED in `nota-next`:** the structural-macro-node engine is real and
working. `StructuralVariantSet::dispatch` (`src/macros.rs:469`) tries
variants in declaration order, first structural match wins, no data tag;
`validate_no_silent_conflicts` (492) rejects exact-pattern shadowing;
the `StructuralMacroNode` trait (1267) bridges to typed Rust; the derive
(`derive/src/lib.rs:23`) generates ordered variants + decode from
declaration order + `#[shape(...)]`. HEAD `fb600e3` "direct decode" (Jun
5) decodes a `MacroCandidate` directly rather than through the global
`MacroRegistry` (which `ARCHITECTURE.md` calls transitional). Round-trip
example + tests pass.

**LANDED in `schema-next` / `schema-rust-next` (PARTIAL):** the typed
source value `SchemaSource` exists (`source.rs:20`) with `.schema`↔source
text round-trip and rkyv bytes; `SourceTypeResolver::from_source`
(`source.rs:126`) runs resolution as methods on the source. Multi-module
loading; `RustEmissionTarget::SignalRuntime` (fifth target, emits
`SignalEngine`); `NexusRunnerAdapter`. `load_module` reads `{module}.schema`
never `.asschema` (`module.rs:48`). The shared driver no longer
materializes / freshness-checks `.asschema` files.

**NOT landed (proposed):**
- **Asschema is NOT removed.** This is the load-bearing correction to the
  scout framing. `vez8` says "removed"; source keeps it as a LIVE
  compatibility intermediate, removal explicitly DEFERRED. Evidence:
  `schema-next/src/asschema.rs` exists; `schema-rust-next` commit
  `038fa23` is literally "mark asschema as **compatibility input**" (a
  marking pass, Jun 5); `RustEmitter::emit_file(&Asschema)` still exposed
  (lib.rs:52); `SchemaSource::lower`/`to_asschema` (source.rs:112,120)
  STILL produce `Asschema` as the internal intermediate before Rust
  emission. INTENT/ARCHITECTURE in both repos call Asschema "the current
  compatibility data endpoint … target after Asschema retirement is the
  schema-in-Rust pipeline." So the pipeline RIGHT NOW is:
  `.schema → SchemaSource → Asschema (compat) → RustModule → src/schema/*.rs`.
- The top-level `SchemaSource` decode is still hand-written `from_block`;
  the `StructuralMacroNode` derive is adopted at exactly ONE leaf
  (`impl StructuralMacroNode for SourceVariantSignature`, source.rs:876).
- The direct-typed-derive decode (kill the `match macro_name()` string
  re-dispatch seam — operator 315), the dead-variant SHADOWING conflict
  check, the `#[shape]` vocabulary completeness, and deserialize-time vs
  read-time for the two cross-reference lookups (designer 523) are all
  proposed/open.
- **P1 blocker — dual-lowering bare-header bug** (`primary-vllc`): the
  registry path lowers a bare PascalCase variant to payload `None`; the
  SchemaSource path resolves a same-named payload. The two routes silently
  disagree on whether a header carries data. Operator: "schema-as-codec is
  unreliable until ONE authoritative lowering exists." This is the most
  conceptually dangerous open item and it sits directly under our flat-Entry
  enum (whose `Kind`/variant headers are exactly bare-PascalCase forms).

## Part B — Situate vs our prior work (reports 71/72 + lojix/horizon)

### B.1 The Spirit record redesign (reports 71 §3 / 72) — what changes

**UNAFFECTED (the substance survives intact):**
- The flat `Entry { Topics, Kind, Description, Certainty, Weight,
  Privacy(Optional), Relations(Vec<hash>) }` record shape, as collapsed by
  the `m27p` NOTA correction. The improved mechanism is about HOW schema
  becomes Rust; it does not touch WHICH fields a record carries.
- 96-bit random hash identity, stable across removals; relations stores
  canonical hashes; CLI cites shortest-unique base36-lowercase prefix,
  min FOUR chars (`tw81`). Hash identity lives inside `a3l4` ("short
  record-identifier hashes sized for non-collision"); no schema-mechanism
  record touches it.
- Relations-field-as-only-code-change (`50qy`/`a3l4`); no composite type
  (`22t6`/`y0vr`); refresh/agglomeration as agent BEHAVIOR in a skill
  (`66bd`); auditor auto-proposes, psyche confirms retire (`1gwe`); weight
  as second Magnitude axis (`515t`/`vbx6`/`g8ln`/`9bxr`); clean break in
  the pilot, production migration is operator work at cutover (`o7lx`).
  None of these are touched by the schema-mechanism change.

**SUPERSEDED — report 72's RECORD SHAPE itself.** Report 72 is the
per-kind ENUM design: a five-variant `Entry` with `*Fields` structs, where
privacy is a per-kind field carried ONLY by `Constraint` and dropped
entirely from public variants (72:284-298, 353-373). That whole per-kind-
variant shape is superseded by the `m27p` correction that COLLAPSED the
per-kind enum to a FLAT record with privacy as an Optional field (NOTA
None = public, `(Some Magnitude)` = elevated, available to ANY kind). Our
prior-work frame already records this collapse; report 72's text was
written one step before it. The implication chains:
- Report 72's whole "Migration table" mapping old flat → per-kind variants
  (72:343-375) is moot — there is no per-kind variant to map onto. The
  flat shape is a SUPERSET- shaped rename (`magnitude`→`certainty`, add
  `weight`, add `relations`, make `privacy` Optional), not a variant
  partition.
- Report 72's "privacy-bearing-kinds" migration risk (72:367-373) — the
  worry that elevated-privacy records that aren't `Constraint` have
  nowhere for their privacy to land — DISSOLVES under `m27p`: privacy is
  available to any kind as an Optional, so no kind loses a privacy slot.

**WRONG / OUTDATED — report 72's migration MECHANISM.** Report 72:382-385
and 484-486 say the version handover works by *"Bump the asschema version
literal in build.rs:31 … this propagates into all three `*.asschema`
headers. Regenerate with SPIRIT_UPDATE_SCHEMA_ARTIFACTS set"* and
*"regenerate so `src/schema/{signal,sema,nexus}.rs` and `schema/*.asschema`
rewrite."* Source grounding (gather 4 §4) shows this is no longer how
spirit builds:
- spirit's `build.rs` builds from `signal.schema`/`nexus.schema`/`sema.schema`
  via `GenerationDriver` and freshness-checks ONLY `src/schema/*.rs`. The
  driver does NOT materialize `.asschema`.
- There is NO `build.rs` version literal that propagates into `.asschema`.
  The `"0.1.0"` at build.rs:31 is the package-version arg to
  `GenerationPlan::new`, not stamped into any `.asschema` header.
- `SPIRIT_UPDATE_SCHEMA_ARTIFACTS` still exists (build.rs:38) but now gates
  the GENERATED RUST, not `.asschema`.
- The committed `.asschema` files in spirit are RESIDUE: stale
  `rerun-if-changed` watch lines (build.rs:22,25,28) + test fixtures
  (`tests/operator_271_closed_claims.rs:24-26`), not build inputs.

So the correct version-handover surface is: **edit `schema/signal.schema`,
regenerate `src/schema/signal.rs` via `SPIRIT_UPDATE_SCHEMA_ARTIFACTS`** —
there is no `.asschema` step. And under the clean-break decision (`o7lx`,
already landed in report 72:570-588 by its own adversarial verifier) the
pilot writes NO `UpgradeFrom` at all — fresh DB. So report 72's entire
"Mechanism (the pilot's actual version-handover path)" subsection
(72:377-407) is doubly mooted: the asschema regen path is wrong, AND
clean-break means no version handover runs in the pilot anyway. The
`SchemaVersion` bump becomes a hard reject (fresh DB), confirmed by 72's
own §"Blockers 2 & 3" revision.

**BETTER / SIMPLER now:**
- The flat Entry authors and decodes more cleanly under schema-is-NOTA than
  the per-kind enum would have. A flat positional record is ordinary
  positional NOTA at a `Record` position; it does NOT need the structural-
  macro-node decode-by-shape machinery at all (decode-by-shape is for
  positions where DIFFERENT object SHAPES select different variants — the
  flat record is one fixed shape). So the schema-mechanism complexity does
  not propagate into our record at all. This is simpler than the per-kind
  enum, which WOULD have been a structural-macro-node position (variant
  selected by `Kind` tag — but note: that is a DATA-TAG enum, NOT a
  structural-shape enum, so even the enum design would have used ordinary
  positional decode, not `StructuralMacroNode`).
- `Privacy` as NOTA `Optional` (`m27p`) is exactly the codec's `Option`
  handling: `None` token vs `(Some Magnitude)`. No new mechanism; it rides
  the existing NOTA optional decode. Under codec-opt-in (`bkcd`), the
  daemon carries the rkyv shape and the CLI carries the NOTA derive — the
  flat Entry's optional/vector fields decode identically on the text edge.
- `Relations(Vec<hash>)` is an ordinary positional vector field — no
  mechanism interaction.

### B.2 Does the structural-macro-node decode-by-shape change our record shape?

No. The flat Entry is a single fixed positional shape. Decode-by-shape
selects among VARIANTS WITH DIFFERENT STRUCTURES at one position; the flat
record has no such variation. The `Kind` field is a data-tag enum
(`Decision`/`Principle`/`Correction`/`Clarification`/`Constraint`), decoded
by tag, not by shape. So `xai7`/`StructuralMacroNode` is orthogonal to our
record. The ONE place it could touch us is the P1 bare-header bug
(`primary-vllc`): the `Kind` unit-enum variants ARE bare-PascalCase headers,
and the two lowering routes currently disagree on whether a bare header
carries a payload. Our `Kind` variants are payload-less, so we want the
SchemaSource resolution to lower them to payload `None` — which is exactly
the disagreement. We should NOT regenerate our schema until `primary-vllc`
is fixed toward one authoritative lowering, or verify our `Kind` enum
lowers identically on both routes.

### B.3 lojix / horizon adoption

- **lojix should adopt triad + schema (`4sff`).** This is downstream of
  the mechanism, not blocked by it: lojix would author `.schema` files and
  generate via the same `schema-rust-next` driver. The Asschema-removal
  state matters only in that lojix should target the `.schema`→Rust surface
  directly (as spirit already does) and NOT wire any `.asschema`
  materialization — i.e. copy spirit's CURRENT build.rs, not report 72's
  description of it. lojix adoption should wait until the one-authoritative-
  lowering P1 is fixed, since a fresh adopter shouldn't inherit the dual-
  lowering ambiguity.
- **horizon-rs is a library hack (`4v45`).** Unaffected by the schema
  mechanism — it is not a triad component and authors no schema.

### B.4 The spirit-plane-split (designer 512) — situate note

Report 512's intra-crate three-file split (`signal`/`nexus`/`sema.schema`,
self-package imports `spirit:signal:Entry`) is ALREADY LANDED
(`8d0e32cf`). The one correction that carries into our thread: 512 used
`WireContract` for spirit's OWN signal schema — that is the bug 514
diagnosed and 515 fixed. The daemon's own signal schema emits to
`SignalRuntime` (emits `SignalEngine`), NOT `WireContract`. spirit's
build.rs already calls `signal_runtime_module("signal")`. The designer's
old `spirit-plane-split` branch should be ABANDONED, not integrated. Our
flat-Entry edit lands in the already-split `schema/signal.schema`; nothing
to redo there.

## Part C — Everything it touches + numbered clarifications

Severity key: **[BLOCKS]** = blocks our flat-Entry build/regeneration;
**[UPDATE]** = a report/skill/file that must be corrected to match landed
reality; **[NICE]** = good-to-know, non-blocking.

### C.1 Reports to update

1. **[UPDATE] Report 72** — the central correction target. Three
   subsections need re-grounding: (a) the record-shape section (72:279-313)
   is per-kind enum, superseded by flat Entry / `m27p`; (b) the migration
   table (72:343-375), moot under flat shape; (c) the "Mechanism (pilot's
   version-handover path)" (72:377-407) AND the implementation-steps
   asschema-regen lines (72:484-486), both WRONG (no `.asschema`
   materialization; clean-break means no handover runs). Report 72's own
   adversarial §"Blockers 2 & 3" (72:570-588) already pivoted to clean
   break; the fix is to make the body consistent with that pivot and with
   the landed `.schema`→`src/schema/*.rs` build. (Note: 72 is a single
   `.md`; an addendum or a superseding report 74 is cleaner than editing in
   place, given the cross-references.)
2. **[UPDATE] Report 71 §3** (the spirit-record-architecture-redesign
   sub-file) — same record-shape supersession (per-kind → flat) and the
   same migration-mechanism correction if it repeats the asschema path.
   Verify and annotate.
3. **[NICE] A consolidating situate/overview** that states the
   flat-Entry-on-the-`.schema`-pipeline shape as the single live design,
   citing `m27p` + `vez8` + `o7lx`, so future agents don't re-derive from
   the superseded per-kind text.

### C.2 Skills to update

4. **[UPDATE] `skills/spirit-cli.md`** — must describe the FLAT positional
   record `(Record ([topics] Kind [desc] Certainty Weight Privacy Relations))`
   with privacy as NOTA Optional (`None`/`(Some Magnitude)`) and the short-
   code citation rule (base36 lowercase, min 4 chars, shortest-unique —
   `tw81`). It currently predates weight/relations/optional-privacy.
5. **[UPDATE] `skills/intent-log.md`** — record shape, the
   certainty-vs-weight distinction, and that relations carries provenance.
6. **[UPDATE] `skills/intent-maintenance.md`** — this is where the
   refresh/agglomeration BEHAVIOR lives (`66bd`): choosing what to merge,
   writing refreshed records with `relations` pointing at sources and a
   compounded `weight`, the reading convention (Correction relations =
   supersedes; non-Correction relations = refreshed-from), and the
   auditor-proposes / psyche-confirms loop (`1gwe`). New substance.
7. **[UPDATE] `skills/nota-design.md`** — must gain the structural-macro-
   node concept (decode-by-shape, declaration-order, type-directed,
   bidirectional, `#[derive(StructuralMacroNode)]`) as the realized "part
   of NOTA never implemented" (`xai7`/`z544`), and the codec-opt-in rule
   (rkyv universal, NOTA derive per double-client — `bkcd`/`hu8i`).
8. **[UPDATE] schema-related skills** — there is no canonical
   `skills/schema-*.md` yet for the improved pipeline. The two-arrow
   pipeline (schema-is-NOTA → schema-in-rust → lower), Asschema-removal-as-
   target, resolution-as-methods, one-lowering-engine, typed emission token
   model, and the `this-code-creates-this-code` reporting discipline
   (`u8od`/`js59`) belong in a schema skill (or `skills/schema-design.md` /
   the component-triad surface). Query `skills/skills.nota` first; this is
   the growing focus of the workspace (`u8od`) and currently under-skilled.
9. **[NICE] `skills/component-triad.md`** — note the `SignalRuntime` vs
   `WireContract` distinction (daemon-local runtime schema emits the engine;
   public contract emits zero engines — 515) so future triad ports don't
   repeat the 512/514 bug.

### C.3 Implementation surface (the spirit pilot)

10. **[BLOCKS] The flat-Entry edit lands in `schema/signal.schema`**, then
    `src/schema/signal.rs` regenerates via `SPIRIT_UPDATE_SCHEMA_ARTIFACTS`
    — NOT via any `.asschema` path and NOT via a `build.rs` version literal.
    This is the corrected mechanism. Store/validation accessors
    (`src/store.rs:313-343`, `src/engine.rs:362-375`) update to read the
    new fields. Clean break — fresh `.sema`, no `UpgradeFrom`.
11. **[BLOCKS] `primary-vllc` (dual-lowering bare-header bug)** sits under
    our `Kind` unit-enum headers. Either it is fixed toward one
    authoritative lowering before we regenerate, OR we verify our payload-
    less `Kind` variants lower identically on both routes. Do not
    regenerate blind.
12. **[NICE] Pilot cleanup** owed (not blocking our edit): delete/demote the
    residual `schema/*.asschema` files, drop their `rerun-if-changed` watch
    lines (build.rs:22,25,28), and fix `spirit/INTENT.md:24-32,60` which is
    STALE — it still claims the build materializes/compares `.asschema`,
    contradicting its own build.rs and the driver. spirit's INTENT.md needs
    a manifestation pass to the `.schema`→SchemaSource→Rust pipeline.
13. **[NICE] lojix adoption (`4sff`)** copies spirit's CURRENT build (no
    `.asschema` wiring); wait for `primary-vllc` so a fresh adopter doesn't
    inherit the dual-lowering ambiguity. **horizon-rs (`4v45`)** untouched.
14. **[NICE] Production-spirit cutover** (operator work, `o7lx`): real
    `signal-spirit`/`meta-signal-spirit` triad repos, meta policy leg,
    parity matrix, `persona-spirit.redb`→`.sema` data migration (none done),
    real schema upgrade/diff. The flat-Entry shape change is the pilot
    surface; cutover is downstream and out of our lane.

### C.4 Clarification questions for the psyche (numbered, severity-marked)

15. **[BLOCKS] The central record-shape tension: `m27p` vs `20jk`/`f0wm`.**
    `m27p` (High) says privacy is an Optional field that EVERY record carries
    (None public / Some elevated) because "every NOTA positional record
    carries every field" — implying a FLAT record. `20jk` + `f0wm` (both
    High) say fields should VARY BY KIND, public records omitting privacy
    entirely — implying PER-KIND VARIANTS. Both High, both name "better
    architecture." Our whole thread assumed `m27p` collapsed the enum to
    flat, but `20jk`/`f0wm` were NOT superseded. Which governs: flat record
    with Optional privacy on all kinds, or per-kind variants? (A possible
    reconciliation: `Kind` is the discriminant of which fields exist, with
    privacy-as-Optional only on kinds that can be private — but that is a
    THIRD shape neither record states. Do not silently resolve.) This gates
    whether report 72's flat redesign or its per-kind redesign is the
    target.
16. **[BLOCKS] Clean-break confirmation under the new mechanism.** `o7lx`
    says pilot record-shape changes are clean-break (fresh DB), production
    migration is operator work at cutover. With Asschema-removal in flight
    and spirit already not materializing `.asschema`, confirm: the
    flat-Entry change lands by editing `schema/signal.schema` + regenerating
    `src/schema/signal.rs`, with a fresh `.sema` and NO `UpgradeFrom` in the
    pilot. (We believe yes from `o7lx` + source, but the version-handover
    machinery report 72 leaned on no longer exists, so confirm the
    no-handover stance explicitly.)
17. **[SHOULD-UPDATE] Bare-header lowering for `Kind`.** Should the
    payload-less `Kind` variants lower to payload `None` via the
    SchemaSource path (the operator's preferred authoritative route, fixing
    `primary-vllc`)? Confirms our regeneration is safe.
18. **[NICE] Does Asschema-removal need to land before our edit?** Source
    shows Asschema is still the live compat intermediate but spirit already
    builds from `.schema` and freshness-checks only Rust. We believe our
    flat-Entry edit is independent of Asschema removal (it rides the
    existing `.schema`→Rust path regardless of whether Asschema is the
    internal intermediate). Confirm we need not block on the Asschema
    deletion.
19. **[NICE] Weight default + compounding convention.** `515t`/`9bxr` make
    weight a second Magnitude axis; report 72 proposed `Medium` as the
    neutral default and qualitative compounding as skill-trained behavior.
    Confirm `Medium` default and that compounding is behavior, not engine
    rule, before it lands in `skills/intent-maintenance.md`.
20. **[NICE] Relations reading-convention by kind.** Report 72 proposed:
    `Correction` relations = what it supersedes; non-`Correction` relations
    = what it refreshes-from; no `RelationType` tag in code (the kind tag
    plus emptiness carries the meaning). Confirm this convention before it
    becomes the documented reading in the intent-maintenance skill.

## Decided-vs-proposed bottom line

DECIDED (psyche intent): two-arrow schema-is-NOTA → schema-in-rust → lower
pipeline, Asschema as removal TARGET (`vez8`); structural macro node as
type-directed shape decode (`xai7`/`z544`); one lowering engine (`58bv`);
codec opt-in (`bkcd`/`hu8i`); flat Entry with Optional privacy (`m27p`),
relations (`a3l4`/`50qy`), weight (`515t`), hash identity (inside `a3l4`),
clean break (`o7lx`); refresh as behavior (`66bd`), auditor-proposes
(`1gwe`).

PROPOSED / not landed: Asschema actually removed (still the live compat
intermediate; removal deferred); direct-typed-derive decode (string
re-dispatch seam persists); dead-variant shadowing detection; `#[shape]`
vocabulary completeness; deserialize-time vs read-time cross-reference
lookups; the `primary-vllc` one-authoritative-lowering fix. And UNRESOLVED:
the `m27p` vs `20jk`/`f0wm` flat-vs-per-kind tension (Q15) — the gating
question for our thread.
