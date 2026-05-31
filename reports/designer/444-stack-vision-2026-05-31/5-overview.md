# 5 — Overview: synthesis, current truth, agglomeration ledger, open horizons

*Kind: meta-report synthesis · Topics: stack-vision, current-truth, agglomeration, operator-265-convergence, open-horizons · 2026-05-31 · designer lane*

## What this synthesis is

Closing the meta-report for designer 444. Four body reports cover the schema/NOTA stack across four perspectives — the four logical planes, the data model (Rust ↔ NOTA ↔ rkyv equivalence), NOTA parsing + structural macros, and the runtime integration. This file ties them together, marks the agglomeration of retired vision reports, names the current truth where sub-agent reading drifted from live code, and orders the open horizons.

## The one-paragraph architecture story

NOTA is a programmable syntax library (Spirit 1281). It owns the parsed structure (`Document → Vec<Block>`), the codec derives (`NotaDecode` / `NotaEncode`), the macro-node registry, and the known-root document body abstraction. Schema is the first major CONSUMER: it registers schema vocabulary as macro-node patterns over NOTA's mechanism, lowers `.schema` source through the structural matcher into typed `Asschema`, and projects `Asschema` across four logical planes (Asschema-data, AsschemaArtifact-projection, AsschemaStore-persistence, RustEmitter-consumption per Spirit 1272). The four planes are connected by derives — `NotaEncode`/`NotaDecode` for text, `rkyv::Archive`/`Serialize`/`Deserialize` for bytes, and one or two lines of glue for the persistence cycle. The schema-rust-next emitter consumes typed `Asschema`, produces `RustModule` data, renders the data to Rust source, and the result is what spirit-next's Signal/Nexus/SEMA runtime uses as its wire and storage nouns. CLI processes parse NOTA at the human edge; the daemon stays binary-only via `NotaSurface` feature-gating (Spirit 1244). The whole picture is derive-driven from end to end; the elegance is that no "glue code" exists between any pair of corners.

## The four body reports — navigation

| File | Frame | When to read it |
|---|---|---|
| `1-four-logical-planes.md` (504 lines) | The four typed objects per Spirit 1272 — Asschema (data), AsschemaArtifact (file projection), AsschemaStore (durable persistence), RustEmitter (consumption); each plane's signature, surface methods, location, and explicit "not its job" boundaries; the generic-substrate horizon (`SerializableArtifact<T>` and `SemaStore<T>`). | When asking: "where does THIS responsibility live?" |
| `2-data-model.md` (659 lines) | Rust ↔ NOTA ↔ rkyv equivalence across 11 major types (Asschema, SchemaIdentity, Name, Declaration + Visibility, TypeDeclaration, StructDeclaration + StructFieldMap + FieldDeclaration, EnumDeclaration + EnumVariant, NewtypeDeclaration, TypeReference, ImportDeclaration + ResolvedImport, MacroDeclaration horizon); the strict-brace key-value contract (Spirit 1259) in the StructFieldMap codec; the honest-notation discipline (Spirit 1267-1269). | When asking: "what does THIS type look like in Rust / NOTA / rkyv?" |
| `3-nota-parsing-and-structural-macros.md` (605 lines) | Two-layer architecture per Spirit 1279 — universal structural parse (Layer 1) + per-consumer macro-node dispatch (Layer 2); recursive pattern constraints; known-root document body codec per Spirit 1278; worked structural-matching examples; the constraint-vector language. | When asking: "how does a `.asschema` file become a typed `Asschema`?" |
| `4-runtime-integration.md` (873 lines) | Schema-emitted types ARE the runtime nouns; the compilation pipeline (schema source → Asschema → RustModule → Rust source → binary); NotaSurface gating per Spirit 1244; the Signal → Nexus → SEMA triad; the CLI ↔ daemon wire path; the schema-core extraction horizon. | When asking: "how does the running daemon use the schema?" |

## Convergence with operator 265

Operator's parallel meta-report at `reports/operator/265-programmable-nota-structural-macro-vision-2026-05-31/` covers the same architecture from the implementation-anchored angle (NOTA layer / Schema consumer layer / Spirit runtime layer / overview-and-gaps). Three points of convergence worth stating:

1. **The architectural shape is the same** — NOTA owns parsed-structure + macro-node programming + derives; Schema is a consumer that supplies vocabulary + lowering; Asschema is data with three projections (NOTA + rkyv + SEMA); spirit-next uses schema-emitted types as wire nouns. Independent convergence between operator's source-read and designer's vision-led presentations is a strong correctness signal.
2. **The gap structure converges with designer 443's audit** — operator 265 §"Remaining Gaps" lists schema-core extraction, RustModule-as-data partial, variant projections, generic artifact/store, CLI source handling. These match designer 443's top-5 improvements (1, 2-now-resolved, 5, 3, sub-agent 4 Finding 7) item-for-item. Three independent analyses (designer 443, operator 265, designer 444 sub-agents) name the same backlog.
3. **The graph-size discipline (Spirit 1282) is shared** — operator 265 uses short focused graphs paired with real code; designer 444 enforces a hard cap of 5 nodes per graph; both reports honor "split large explanations into several parts."

The two meta-reports are complementary, not redundant. Operator 265 is the implementation-anchored reading; designer 444 is the data-type-equivalence-anchored complement. A reader new to the architecture should read both; for a single-source overview, designer 444's `1-four-logical-planes.md` + operator 265's `4-overview-and-gaps.md` together give the fastest grounding.

## Current truth — the corrections sub-agent 3 missed

Sub-agent 3 (NOTA parsing + structural macros) was dispatched with framing from designer 443 that the **Spirit 1280 violation** (text round-trip in declarative macro lowering) was pending the highest-priority fix. **The violation is FIXED in live code.** Verified by reading `schema-next/src/declarative.rs` at `fe770d1`:

- `MacroBindings` stores `Vec<SingleMacroBinding>` + `Vec<RepeatedMacroBinding>` (declarative.rs:1025-1030).
- `SingleMacroBinding.value: Block` — the binding stores a typed `Block` reference, not a `String` (declarative.rs:1090-1097).
- `RepeatedMacroBinding.values: Vec<Block>` (declarative.rs:1099-1102).
- `ExpandedTemplate::lower_to_output` lowers through `AssembledTemplate::new(ObjectView::Expanded(&self.object)).lower(registry, context)` — direct structural lowering without text reparse (per operator 265 §"Structural Macros, Current Truth").
- The remaining `source: String` on `ExpandedTemplate` is a TRACE surface (`object.compact_notation()`), used for diagnostics and `context.remember_expanded_template`, not the lowering substrate.

Operator's fix landed at `schema-next 877c03f5` (`schema: keep declarative macro expansion structural`), then repinned at `fe770d1d` (`schema: repin recursive nota macro substrate`). This **closes designer 443 improvement #2** in code — the audit's framing of the violation was correct at the time of writing; operator's subsequent slice resolved it.

Sub-agent 3 §"Structural over text macros (Spirit 1280)" reads "the Spirit 1280 violation pending" — that framing should be read as **historical context** about what the audit found; the current state is that the violation is closed. The remaining text surface in `ExpandedTemplate::source` is the open question operator 265 §4 raises: should the trace surface stay as text or become structured `ExpandedObject` plus optional rendered text. That's an ergonomic refinement, not the original anti-pattern.

## Agglomeration ledger — old reports retired

Per the frame's retirement policy, the following design vision reports retire into the new presentation with landing evidence:

| Retired report | Landing evidence — where its content lives now |
|---|---|
| `reports/designer/430-codec-opt-in-research-rkyv-base-nota-on-top.md` | Codec opt-in is LIVE via `NotaSurface` gating (operator 246; spirit-next Cargo.toml feature gating). Content in `4-runtime-integration.md` §"NotaSurface gating". |
| `reports/designer/431-daemon-zero-nota-state-aware-startup-multi-signal.md` | Zero-NOTA daemon is LIVE via NotaSurface + binary `Configuration`; state-aware startup remains a future horizon. Content in `4-runtime-integration.md` §"The CLI single-argument rule" and §"NotaSurface gating". |
| `reports/designer/434-live-assembled-schema-bootstrap-and-loop-closure.md` | Asschema-as-artifact is LIVE (Spirit 1246; operator 252); the bootstrap loop closure target is in operator 263 Gap 1 + designer 443's remaining work. Content in `1-four-logical-planes.md` §"Plane 1: Asschema" and `2-data-model.md` §"Asschema". |
| `reports/designer/435-vision-for-the-four-remaining-gaps.md` | Gap A (macro-table-as-data, partial), Gap B (RustModule-as-data, partial per operator 265 + sub-agent 3), Gap C (schema-core extraction, pending — THE headline horizon), Gap D (schema diff/upgrade, deferred). Content in `4-runtime-integration.md` §"The schema-core extraction horizon" + designer 443 §"Top 5". |
| `reports/designer/437-strict-brace-key-value-explanation-and-implementation-try.md` | Strict-brace key-value is LIVE (Spirit 1259; operator 256). Content in `2-data-model.md` §"The strict-brace key-value contract" and `3-nota-parsing-and-structural-macros.md` §"Worked structural matching examples". |
| `reports/designer/438-macro-nodes-at-nota-layer-vision-focused-on-critical-parts.md` | Macro nodes at NOTA layer are LIVE (Spirit 1263; operator 261; nota-next 3f46c2e for recursive patterns + Delimiter substrate). Content in `3-nota-parsing-and-structural-macros.md` §"Layer 2: macro-node programming". |
| `reports/designer/441-asschema-types-rkyv-sema-roundtrip.md` | Four-object separation is LIVE (Spirit 1272; AsschemaStore at operator 84ce382); content agglomerated across `1-four-logical-planes.md` (the four-object framing), `2-data-model.md` (the Rust ↔ NOTA ↔ rkyv equivalence + signatures), and `4-runtime-integration.md` (the SemaStore + redb substrate). The prototype branch `designer-store-prototype` (`f2b477a`) is referenced in `1-four-logical-planes.md` §"Plane 3" as the design derivation. |
| `reports/designer/442-known-root-nota-anti-pattern-and-elegant-path.md` | Anti-pattern is FIXED in live code — `schema-next` `57bab60` (derive-driven Asschema known-root codec) + `nota-next` `14ad2f8` (known-root body codec) + `nota-next` derive crate `#[nota(known_root)]` + `#[nota(name = ...)]` attributes. Content in `3-nota-parsing-and-structural-macros.md` §"The known-root abstraction" and `1-four-logical-planes.md` §"Plane 1: Asschema". |

Retained (not retired):
- `reports/designer/351-intent-file-tour-2026-05-26.md` (intent file history)
- `reports/designer/352-intent-log-audit-2026-05-26.md` (intent audit history)
- `reports/designer/412-review-of-system-designer-42-horizon-167-audit.md` (system-designer review history)
- `reports/designer/415-context-maintenance-2026-05-28.md` + `reports/designer/439-context-maintenance-2026-05-30.md` (maintenance ledgers)
- `reports/designer/443-design-improvements-audit-2026-05-31/` (active audit + ordered backlog — improvements #1, #3, #4, #5 still pending; #2 closed by operator 877c03f5)

After retirement: 6 retained reports + `443/` audit + `444/` new presentation = 8 designer-lane report units. Under the 12-cap from `skills/reporting.md`.

## What's LIVE today (corrected current truth)

Concrete state after operator's recent work:

- **Asschema four-object separation** — Asschema (data) + AsschemaArtifact (file projection) + AsschemaStore (durable persistence, `schema-next/src/store.rs` at `84ce382`, redb-backed) + RustEmitter (consumption, in `schema-rust-next/src/lib.rs`). All four live in main.
- **Asschema known-root NOTA codec** — derive-driven via `#[nota(known_root)]` + `#[nota(name = "Input")]` + `#[nota(name = "Output")]`. Hand-rolled positional decoder is gone. Anti-pattern from designer 442 is FIXED.
- **Macro nodes at NOTA layer** — `nota_next::MacroNodeDefinition` + `Pattern` with recursive `children: Option<Box<Pattern>>` (closes designer 443 sub-agent 1 Finding 2's Pattern/ChildPattern collapse); multi-field enum variant derive support; public `Delimiter::wrap` / `Block::as_delimited` substrate.
- **Strict-brace key-value contract** — every brace entry inside `{}` is exactly two objects (StructFieldMap codec at `asschema.rs:492-532`); Spirit 1259 honored at all positions.
- **Declarative macro lowering is STRUCTURAL** — `MacroBindings` stores `Block` / `Vec<Block>` values; `ExpandedTemplate::lower_to_output` lowers through `ObjectView::Expanded` directly; Spirit 1280 violation closed at `877c03f5`.
- **Build-time artifact chain** — `spirit-next/build.rs` proves the path: `.schema` → `AsschemaArtifact` → checked-in `.asschema` → generated Rust → binary artifact equivalence per operator 265 §"Build-Time Artifact Chain".
- **CLI/daemon split** — NotaSurface gating; CLI binary `required-features = ["nota-text"]`; daemon binary closes without `nota_next` runtime dependency; rkyv-only wire end-to-end.
- **Signal/Nexus/SEMA triad** — operates on schema-emitted nouns end-to-end; `Mail<BeingProcessed>` typestate carries lowered SEMA input across the boundary.

## Open horizons — ordered backlog

After this synthesis, the actionable backlog (designer 443 §"Recommended sequencing" + operator 265 §"Remaining Gaps" both converge here):

1. **Schema-core extraction** (designer 443 #1; operator 263 Gap 4; operator 265 Gap 1; designer 435 Gap C). The biggest single boilerplate cut — ~470 lines per emitted component (byte-identical envelope substrate) + ~300-400 lines hand-written runtime substrate that also lifts (`Mail<Phase>` typestate, `MailLedgerHook`, `Engine`-as-composer). Multiplicative scope: every additional component drops the same amount. Headline horizon. Requires coordination across `schema-next` (declare which support nouns are imported), `schema-rust-next` (emit `use schema_core::*`), and every consumer component.
2. **Generic `SemaStore<T>` + `SerializableArtifact<T>` substrate** (designer 443 #3; operator 265 Gap 4). Mechanical wins, ~500 lines across schema-next + spirit-next. Best timed once a second store and a second artifact owner make the abstraction shape stable. Can land in `schema-next` initially or in a future `sema-storage` crate.
3. **`RustModule`-as-data completeness** (designer 443 sub-agent 3 #2; operator 265 Gap 2). Extend `RustItem` enum from "type declarations only" to "all Rust items" (impl, trait, fn, const, module). Tests assert structure instead of text. Half-closed per designer 435 Gap B; the support-emission methods (`emit_signal_frame_support`, `emit_mail_event_support`) become data items, then schema-core extraction (#1) absorbs most of them.
4. **Schema-emitted variant projections** (designer 443 #5; operator 265 Gap 3). `From<Payload> for Enum` + sibling-plane translations that spirit-next currently hand-rolls in `engine.rs:326-399` + `nexus.rs:105-154`. Falls out of schema-rust-next emitter changes naturally; ~120 lines.
5. **NOTA source helper for inline-vs-path argument handling** (designer 443 sub-agent 4 Finding 7; operator 265 Gap 5). The CLI's `read_single_argument` string-prefix branching at `spirit-next/src/bin/spirit-next.rs:41` belongs in nota-next as `NotaSource::from_argument`. Small but principled.

Designer 443 improvement #2 (drop text round-trip from declarative macro lowering) is **CLOSED** — operator landed `877c03f5`. Designer 443 improvement #4 (nota-next derive features + public Delimiter surface) is **PARTIALLY CLOSED** — Delimiter substrate landed at `nota-next 3f46c2e`; the multi-field-variant derive landed; the inherent-method shadowing for caller ergonomics remains pending.

## Open design questions

From operator 265 §"Open Questions" + designer 443 sub-agent 2 Finding 4:

1. **`schema-next::MacroNodeDefinition` wrapper boundary.** The wrapper at `schema-next/src/macros.rs:294` holds `position`, `dispatch`, and `cases` — but the position is already inside each contained `nota_next::MacroNodeDefinition` case (sub-agent 2 Finding 4 quantified the wrapper at ~290 lines of delegate logic). Designer-side answer: the wrapper IS a delegate layer today; should flatten once nota-next exposes a "position-grouped registry profile" that returns matches grouped by position predicate. Worth a small psyche call on whether to ship the flattening as a slice or wait until schema-core extraction reshapes the surface.
2. **Schema-core crate split.** One crate or several narrower crates (`signal-frame`, `plane-envelope`, `origin-route`, `mail-keeper`)? Operator 265 leaves this open. Designer 435 §7 originally proposed one crate; the runtime-ownership boundary may argue for narrower libraries once `Mail<Phase>` lifts and `SemaStore<T>` substrate moves out of spirit-next.
3. **Generic artifact/store substrate location.** Operator 265 asks: schema-next, schema-core, or a future sema/storage crate? Designer-side preference: ship `SerializableArtifact<T>` in schema-next initially (it's generic over any type with the right derives), then re-home once schema-core lands. `SemaStore<T>` is more substrate-flavored; could live in either schema-core or a dedicated `sema-storage` from the start.
4. **`ExpandedTemplate::source` trace surface.** Stay as text trace or become structured `ExpandedObject` + optional rendered text? Operator 265 frames as design refinement. Designer-side note: the structural form would compose better with the existing macro-node data model and would make trace records queryable, but the text form is simpler and matches what operators want when debugging macro expansion.

## Cross-references

- `reports/designer/443-design-improvements-audit-2026-05-31/` — the broad design audit with ordered backlog; sub-agent 2's #1 finding (Spirit 1280 violation) is now closed per `schema-next 877c03f5`; the other improvements remain pending.
- `reports/operator/265-programmable-nota-structural-macro-vision-2026-05-31/` — operator's parallel implementation-anchored vision; converges on the architecture and the gap structure.
- `reports/operator/263-unimplemented-gap-audit-2026-05-31.md` — operator's 8-gap audit; Gap 1 = improvement #2 (closed), Gap 4 = improvement #1 (open).
- `reports/operator/262-total-architecture-core-macro-artifacts-2026-05-30.md` — operator's earlier full stack tour after the macro library artifact landed.
- Spirit records: 1244 (binary daemon + feature-gated NOTA), 1246 (live asschema artifact), 1249 (rkyv discriminant stability), 1259 (strict brace key-value), 1263 (macro nodes at NOTA layer), 1267-1269 (notation honesty: no heterogeneous vectors, no meaningless wrappers, truthful representation), 1270 (three categories + module-qualified + cross-crate), 1271 (rkyv-in-SEMA + NOTA re-export through derived types), 1272 (four-object logic separation), 1274 (positional root reading), 1277 (input/output as struct fields not variants), 1278 (NOTA-layer abstraction for known-root), 1279 (two-layer structural matching + ordered patterns + no-match-as-error), 1280 (structural macros over text macros), 1281 (NOTA as programmable syntax library for structural-macro languages), 1282 (architecture presentations use short focused graphs + multiple parts + paired with real code).
