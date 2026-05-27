# 370 — Implementation gap audit (designer-side)

*Designer-side audit complementing operator's `reports/operator/206-schema-spirit-running-concept-audit-2026-05-26.md`. Operator's audit covers what's missing for spirit-next to become real production Spirit. This report adds the gaps /206 doesn't cover — the broader architecture (Layer 6 upgrade; schema-schema in NOTA; daemon-as-process; async mail), the shape-questions that remain unresolved from `reports/designer/361-latest-vision-schema-derived-nota-stack-2026-05-26.md` §11 (15 consolidated), and the discipline/workflow gaps surfacing from records 852-855.*

## §1 Frame — designer-side audit layered on /206

`reports/operator/206-schema-spirit-running-concept-audit-2026-05-26.md` is thorough at the implementation layer:
- Verification (all three running concepts pass `nix flake check`)
- 9 prioritized gaps (3 P0 + 4 P1 + 2 P2)
- 5 architectural patterns to preserve
- Recommended next slice (emit route/header layer)

This report doesn't restate /206's gaps; it ADDS the gaps /206 doesn't cover. They fall into four categories:

1. **Architecture-layer gaps** — Layer 6 schema diff + upgrade; schema daemon; nota.schema actually self-hosting
2. **Shape-question gaps** — items from `/361 §11` consolidated open questions still unresolved
3. **Discipline / workflow gaps** — records 852-855 not yet manifested into skills + tooling
4. **Aspirational claims** — truth-verification table claims 7-8 still untested

## §2 Architecture-layer gaps /206 doesn't cover

### §2.1 Layer 6 — schema diff + upgrade traits (Maximum priority for production)

Per `reports/designer/361-latest-vision-schema-derived-nota-stack-2026-05-26.md` §9 + `reports/operator/199-nota-core-schema-stack-implementation-target-2026-05-26.md` Layer 6:

```rust
pub trait UpgradeFrom<Previous> { ... }
pub trait DowngradeTo<Previous> { ... }
```

Plus change-class taxonomy (zero-cost / append-only / projection / destructive / incompatible).

**Current state**: `schema-rust-next` emits types + short-header constants + (per `reports/operator/205-spirit-next-schema-pilot-implementation-2026-05-26.md`) NOTA codec boundary. **It does NOT emit upgrade traits.** /206's P0 #3 names "no migration path" as part of the durable-state gap; the schema-diff engine that would drive migration is unmentioned.

**Why this matters**: spirit v0.3 → v0.4 cutover (or any future schema evolution) requires the upgrade machinery. Per `reports/designer/346-actor-schemas-and-upgrade-mechanism-2026-05-25.md` §4 + the `mod previous` / `mod next` bridge pattern, this is load-bearing for the side-by-side deployment discipline (`reports/operator/187-spirit-v0-2-0-side-by-side-deployment-2026-05-25.md`). Without it, every schema change is a manual write-bridge slice.

**Acceptance shape**: schema-rust-next emits Diff(Asschema_main, Asschema_next) → typed change report + UpgradeFrom/DowngradeTo trait impls for each affected type. Spirit-next gets a test that runs a tiny schema migration end-to-end.

### §2.2 Schema-schema self-hosting (record 807 + /363 hybrid finding)

Per record 807 + the /363 verdict: the schema-schema is hand-authored Rust today (operator's `SchemaMacro` trait + `MacroContext` + `SchemaSchema::default()` with built-in macros). Eventually `schemas/schema.schema` (queued per `reports/operator/199-nota-core-schema-stack-implementation-target-2026-05-26.md` Phase 0) describes the schema language IN NOTA.

**Current state**: no `schema.schema` exists. The schema-schema lives entirely in Rust source.

**Why this matters less than §2.1**: per /363's hybrid finding, byte-level recognition CANNOT emit declaratively — must stay hand-authored. Schema-schema may have a similar bootstrap floor; the schema for the schema-language might be partially declarative + partially hand-authored. Worth scoping but not blocking.

**Acceptance shape**: a `schema.schema` file describing what can be described declaratively (probably namespace shape; possibly macro signatures); a corresponding test that the schema-schema Rust code matches what its own schema would emit.

### §2.3 Schema daemon as a process (deferred per /199 §"Open question 5"; record 750)

The schema daemon — a long-lived process resolving + caching schemas across compilations — is named in `/361 §7` (records 749, 750) but explicitly deferred per `reports/operator/199-...` §"Open §5".

**Current state**: `schema-next::SchemaEngine` is in-process. Build-time emission via `build.rs` works without a daemon (operator's `generated-at-build-time` Nix witness enforces this).

**Why this matters**: when schemas grow (many `.schema` files across many repos importing each other), in-process resolution per-build becomes slow + opaque. A daemon-shaped cache + cross-build-incremental resolution becomes load-bearing.

**Acceptance shape (when ready)**: `schema-next` ships an optional daemon binary; the daemon answers schema-resolution queries; build.rs queries the daemon when available, falls back to in-process when not. Not blocking for spirit-next pilot.

### §2.4 nota.schema living truly self-hosted

`/363` proved the narrower recursion-floor cut is PARTIALLY feasible — type declarations emit cleanly from `nota.schema` but byte-level recognition can't. **The hybrid recommendation** in `/361 §4` + `/363`: operator's wider cut stays for byte recognition; schema-driven emission applies to type declarations above the byte floor.

**Current state**: operator's `nota-next` is hand-authored. The `schemas/nota.schema` in `design-nota-from-schema` (designer parallel) exists as evidence but isn't consumed by operator's `nota-next`.

**Why this matters**: even per the hybrid finding, **some of nota-next's TYPES** could come from `nota.schema`. The Block / Atom / SourceSpan / SourcePosition definitions are TYPE declarations — they could emit from `nota.schema` even though the lexer + parser stay hand-authored. Closing this would land record 746's all-the-way-back claim for the types-layer.

**Acceptance shape**: `nota-next` adopts a `nota.schema` that declares its TYPES; `nota-next/build.rs` emits those types via schema-rust-next; lexer + parser remain hand-authored against the emitted types.

## §3 Shape-question gaps from /361 §11 still unresolved

`reports/designer/361-latest-vision-schema-derived-nota-stack-2026-05-26.md` §11 lists 17 consolidated open shape questions. Some have resolved through implementation; some remain.

| # | Question | Status |
|---|---|---|
| Q1 | Root field ordering (imports-first vs input/output-first) | ✅ RESOLVED — both /205 + /368 default to imports-first |
| Q2 | Recursion floor cut | ✅ RESOLVED — `/363` hybrid finding |
| Q3 | Build-time vs committed emission | ✅ RESOLVED — `/369` both chose build-time |
| Q4 | Kernel bracket-disambiguation (`[text]` as raw-string at nota-core OR raised to schema context) | ⚪ OPEN — /206 doesn't address; current `nota-next` has `is_pipe_text` for `[\|...\|]` and raw bracket otherwise |
| Q5 | Schema daemon triad shape (when it lands) | ⚪ OPEN (DEFERRED per §2.3 above) |
| Q6 | `Asschema` vs `AssembledSchema` naming | ✅ RESOLVED — operator's `Asschema` adopted in /205 |
| Q7 | Block leaf classification cut (exact leaf candidate kinds + tiebreakers) | ⚪ OPEN — operator's `AtomClassification` enum landed but the exact classification rules aren't documented |
| Q8 | Reassembly separator policy (newline/space/none when re-emitting concatenated blocks) | ⚪ OPEN — `nota-next::Block::reemit` exists but separator behavior at concat boundaries isn't pinned |
| Q9 | Bare-identifier eligibility (exact alphabet + edge cases) | ⚪ OPEN — current `qualifies_as_*` helpers presumably pin specific alphabets but the rules aren't surfaced in design docs |
| Q10 | Variant-payload representation | ✅ RESOLVED — operator's MVP shows `(Variant Payload)` always (uniform tagged-enum shape) |
| Q11 | Predicate naming convention | ✅ RESOLVED — `is_*` factual / `qualifies_as_*` structural per record 800 |
| Q12 | InputOutputStructMacro role-awareness | ✅ RESOLVED — `lower(object, position, ctx)` per /200 + /205 |
| Q13 | Macro::lower return shape | ✅ RESOLVED — operator's `MacroOutput` enum chosen |
| Q14 | Schema-schema's own self-hosting | ⚪ PARTIAL — `/363` hybrid finding; some types emittable, kernel stays hand-authored |
| Q15 | User-authored macro registration story | ⚪ OPEN — `SchemaMacro` trait is public but registration mechanism not exercised |
| Q16 | Macro trait shape (typed associated I/O vs single MacroOutput enum) | ✅ RESOLVED — operator chose single MacroOutput enum |
| Q17 | Schema daemon naming (triad shape) | ⚪ OPEN (DEFERRED) |

**6 OPEN shape questions remain**: Q4, Q5, Q7, Q8, Q9, Q15, Q17 (and Q14 partial). Of these, **Q15 (user-macro registration) is the most-impactful** for the next implementation tier — without it, the schema language is closed to extension.

## §4 Discipline + workflow gaps (records 852-855 manifestation)

Four recent intent records await manifestation into workspace skills + tooling:

### §4.1 Record 852 — central integration tests via Nix input override

The directive: *"central tests that can just rebuild, regenerate all the Rust code for everything and test it all together... using these Nix override, input override from a central repository."*

**Current state**: each repo has its own `nix flake check`. There's no `goldragon-schema-stack-tests` (or similar) repo that pins local checkouts of nota-next + schema-next + schema-rust-next + spirit-next via flake input overrides and runs cross-repo tests.

**Why this matters**: changes to schema-rust-next today are validated by its own flake check. A breaking change that affects spirit-next downstream isn't caught until you separately rebuild spirit-next. A central test pinning local checkouts catches cross-cutting regressions.

**Acceptance shape**: either a new `schema-stack-tests` repo (per `skills/major-break-via-new-repo.md` discipline) OR a section in spirit-next's flake.nix that supports `--override-input` for the substrate repos. Operator's recommended next slice (route/header emission) would benefit from this for round-tripping.

### §4.2 Record 853 — methods on schema-generated objects

The directive: *"agents implement behavior as methods on the real objects specified by schema-generated Rust types; schema objects are the nouns, and implementation code attaches verbs to those nouns rather than adding free-function logic around them."*

**Current state**: AGENTS.md hard override (records 712/729) says no free functions outside `#[cfg(test)]` + `fn main()`. Record 853 SHARPENS this — the framing is now positive (verbs-attach-to-nouns) and explicitly tied to schema-emitted types. **No skill yet captures the sharpened framing.**

**Why this matters**: agents writing spirit-next's `Engine::handle` or future actor code should know that methods attach to schema-emitted types, not float as standalone functions. The framing is load-bearing for keeping the runtime code disciplined as it grows.

**Acceptance shape**: either update `skills/rust-discipline.md` (or `skills/abstractions.md` — *"Verb belongs to noun. Methods on types; no free helpers when a method would do."* per the existing entry) with record 853's framing, OR create `skills/methods-on-schema-objects.md` as a new topic skill. Also a Nix check candidate per /206 §"Pattern 4" — *"no hand-written generated-type mirrors."*

### §4.3 Record 854 — root object carries signal-frame protocol

The directive: *"The root schema-generated signal object should carry the signal-frame protocol behavior needed for rkyv serialization and process-to-process dispatch, with caller/process-origin support integrated when that library is ready."*

**Current state**: spirit-next's `transport.rs` hand-writes the frame encoding (`length + header + rkyv`). The schema-generated `Input` enum doesn't carry framing methods directly; the transport module wraps it externally.

**Why this matters**: per `/367` the root object IS the specification's apex. Framing should be a method on Input (or its archived form) rather than a separate transport module. /206 P0 #2 names the route/header gap; this is the same gap from a different angle.

**Acceptance shape**: schema-rust-next emits framing methods on root surfaces; spirit-next's `transport.rs` becomes a thin wrapper around emitted methods. Operator's recommended next slice (route/header emission) is the direct path to this.

**Caller/process-origin sub-claim**: a library to identify which process a message came from. Per the psyche: *"I think it was written down somewhere"* — a recall pointer to existing workspace knowledge. **Search task** — not new intent; deferred until needed.

### §4.4 Record 855 — change-loop discipline

The directive: *"changing a data type in the schema-derived stack means editing the schema, regenerating the Rust types and traits, then writing implementation methods against the regenerated objects; agents should not hand-edit generated data type mirrors."*

**Current state**: spirit-next's `build.rs` enforces regeneration; the discipline is structurally enforced for spirit-next. **The skill that codifies this for future agents doesn't exist yet.**

**Why this matters**: when a new agent picks up spirit-next or a sibling component, they need to know "edit schema, not generated code." Without the skill, the structural enforcement (build.rs always regenerating) is the only signal — agents could miss why the indirection exists.

**Acceptance shape**: either update `skills/feature-development.md` with a §"Schema-derived data type change-loop" section OR create a new `skills/schema-change-loop.md`. Cross-reference from `skills/rust-discipline.md` and `skills/architecture-editor.md`.

## §5 Aspirational claims still untested

From `reports/designer/366-component-view-and-truth-verification-2026-05-26.md` §9 (updated to 9/12 verified):

| Claim | Status | Why unblocked depends on |
|---|---|---|
| 7. Async unique-ID mail delivery | 🔵 ASPIRATIONAL | Needs message_id substrate + actor mailbox + concurrent-test harness |
| 8. Synchronous fast-response option (dual-Reply shape) | 🔵 ASPIRATIONAL | Needs the dual-shape Reply (immediate vs pending-with-handle); requires §4.3 framing first |

Plus an implicit 13th claim worth tracking:
- **13. Schema-derived upgrade traits** (UpgradeFrom + DowngradeTo from §2.1) | 🔵 ASPIRATIONAL — entire Layer 6 not yet built

## §6 What's surfaced now that NEEDS clarification

Three open questions for psyche review window:

### Q-NEW-1: Central test substrate (record 852) — new repo or in-repo flake?

Per `skills/major-break-via-new-repo.md` discipline + record 852: should the central-tests live in a new repo (e.g. `schema-stack-tests` or `goldragon-integration-tests`) OR in spirit-next's flake.nix as a multi-input override target?

**Designer lean**: new repo (`schema-stack-tests`). Reasons: clean separation; multiple downstream consumers (not just spirit-next) eventually need integration testing; the repo can hold cross-cutting fixtures that don't fit naturally in any single component repo.

### Q-NEW-2: methods-on-schema-objects — new skill or extend existing?

Per record 853: where does the sharpened verb-attaches-to-noun framing land? Options:
- (a) Extend `skills/rust-discipline.md` with a §"Methods on schema-emitted types"
- (b) Extend `skills/abstractions.md` (which already has *"Verb belongs to noun"*)
- (c) Create `skills/methods-on-schema-objects.md` as a new topic skill

**Designer lean**: (b) — `skills/abstractions.md` already has the verb-belongs-to-noun framing; record 853 SHARPENS it with schema-emitted-types specificity. Extending the existing skill keeps the skill index tight per `skills/skill-editor.md`.

### Q-NEW-3: caller/process-origin library — find or build?

Per record 854 + the psyche's recall *"I think it was written down somewhere"*: search workspace for the prior caller-identification library OR scope a new one?

**Designer lean**: search first (low-cost; recall might surface). If nothing found, scope as a discrete library design report. Don't block the route/header slice on this; it's adjacent.

## §7 Priority synthesis — what to attack next

Operator's /206 §"Recommended Next Slice" names route/header emission (P0 #2 closure). That's the right immediate slice. Layered on top:

| Tier | Slice | Closes |
|---|---|---|
| **Immediate** | Route/header emission (operator's recommendation) | /206 P0 #2; partial record 854 |
| **Immediate** | Apply record 853 to /206 P1 #7 (granular unit tests) — name designer's tests as the unit baseline | /206 P1 #7 |
| **Next** | Vector + Option type references in schema language | /206 P0 #1 (partial — covers vector + option) |
| **Next** | Central test substrate per record 852 (new repo OR in-repo) | record 852 |
| **Mid-term** | redb durable state with rkyv-at-rest | /206 P0 #3 |
| **Mid-term** | User-authored macro registration (Q15) | /361 §11 Q15 + /206 P1 #5 partial |
| **Mid-term** | Triad split (spirit + signal-spirit + core-signal-spirit) | /206 P1 #4 |
| **Mid-term** | Schema-rust-next emits NOTA codec impls on emitted types (mostly done; verify) | /206 P0 #1 (partial) |
| **Later** | Layer 6 schema diff + UpgradeFrom/DowngradeTo trait emission | §2.1 above; new gap |
| **Later** | nota-next adopts nota.schema for its TYPES (per /363 hybrid) | §2.4 above |
| **Later** | Schema daemon as process | §2.3 above; deferred per /199 |
| **Later** | Async unique-ID mail delivery + dual-Reply shape | claims 7-8 |

**12 named slices**. Operator's /206 covers the immediate tier well; this audit adds the mid-term + later tiers.

## §8 What can be safely deferred

Three items remain DEFERRED without urgency:

- **Schema daemon as process** (§2.3) — current build.rs in-process emission is fine for the pilot + the next several slices
- **nota.schema self-hosting at nota-next** (§2.4) — type-emission would land record 746's claim incrementally; not blocking anything else
- **Schema daemon triad naming (Q17)** — operator's open question 5; depends on §2.3 happening first

These are real gaps that should NOT drift into the "we forgot" category — but they don't block production-direction work.

## §9 What stays true and unchanged

The architectural pattern from operator's /206 §"Patterns to Preserve" remains right:
- Authored schema is small; generated Rust is full
- Runtime logic matches typed trees (Input → state op → state response → Output)
- NOTA at edges; rkyv between components
- Constraint tests name architecture, not just behavior
- Designer branches are evidence, not mainline

Nothing in this audit contradicts those patterns. The gaps are about extending the patterns further, not changing them.

## §10 References

- `reports/operator/206-schema-spirit-running-concept-audit-2026-05-26.md` — the operator audit this report layers on
- `reports/operator/205-spirit-next-schema-pilot-implementation-2026-05-26.md` — the empirical baseline
- `reports/designer/361-latest-vision-schema-derived-nota-stack-2026-05-26.md` §11 — the 17 consolidated open shape questions
- `reports/designer/363-design-nota-from-schema-comparison-2026-05-26.md` — the recursion-floor hybrid verdict
- `reports/designer/366-component-view-and-truth-verification-2026-05-26.md` §9 — the truth-verification table (9/12 verified)
- `reports/designer/367-nota-as-specification-superset-of-capnproto-2026-05-26.md` — the latest framing
- `reports/designer-assistant/368-running-spirit-concept-on-new-architecture-2026-05-26.md` — designer parallel concept
- `reports/operator/187-spirit-v0-2-0-side-by-side-deployment-2026-05-25.md` — the deployment discipline upgrade traits would serve
- `skills/double-implementation-strategy.md` + `skills/major-break-via-new-repo.md` — the new-repo workflow
- `skills/abstractions.md` — the existing methods-on-types skill record 853 sharpens
- `/369` comparison + branch-retirement decision retired in sweep /377; the convergence/retirement substance is absorbed into /371 §8 sequencing.
- `/346` actor-schemas + upgrade mechanism retired in sweep /349; substance is in `repos/persona-spirit/INTENT.md` + `repos/persona-spirit/ARCHITECTURE.md`. Layer 6 upgrade traits implement it.
- Spirit records: 712 / 729 (methods on impl blocks; sharpened by 853); 746 (NOTA itself schema-derived; partial per /363); 749-750 (precompiled library + daemon); 807 (schema-schema core Rust); 819 (emission separate from macros); 822 (forge content-addressing); 844 (single emit_all_schemas!); 852 (central integration tests via Nix input override); 853 (methods on schema-emitted objects); 854 (root signal object carries signal-frame protocol + caller/process-origin); 855 (change-loop discipline)
- Operator repos: `nota-next`, `schema-next`, `schema-rust-next`, `spirit-next`
