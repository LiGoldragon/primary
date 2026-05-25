# 191.2 - Intent audit and current second-operator context

Kind: Intent audit + context maintenance overview  
Topic: second-operator active work, repo-intent gaps, constraint table  
Lane: second-operator  
Date: 2026-05-25  
Intent cut: Spirit record 655

## Current summary

This pass refreshed intent through Spirit record 655, agglomerated the
second-operator report lane into this meta-report directory, and audited the
repo intent/architecture surfaces most directly touched by recent
second-operator work.

Active second-operator report set after this pass:

| Path | Why it remains active |
|---|---|
| `reports/second-operator/184-orchestrate-short-header-ingress-implementation-2026-05-25.md` | Orchestrate ordinary/owner socket `ShortHeader` validation witness. |
| `reports/second-operator/186-orchestrate-upgrade-socket-implementation-2026-05-25.md` | Orchestrate private upgrade socket and Mirror-before-readiness handover witness. |
| `reports/second-operator/190-schema-mainline-macro-index-port-2026-05-25.md` | Schema mainline `NotaValue` parser + macro index + initial macro pipeline witness. |
| `reports/second-operator/191-intent-context-maintenance-2026-05-25/` | Current intent-cut frame, report agglomeration, and this audit. |

All other second-operator reports from `163` through `190` are now retired by
this context-maintenance pass. Their load-bearing substance is carried in
`1-report-agglomeration.md` and this overview; durable implementation truth is
in code, tests, and commits.

## Work map

```text
Spirit intent 628-655
        |
        v
second-operator report agglomeration
        |
        +--> schema engine current path
        |       nota-codec tree -> schema shape parser -> AssembledSchema
        |       -> schema-rust composer -> emit_schema!
        |
        +--> orchestrate current path
        |       ShortHeader ingress validation
        |       private upgrade socket + Mirror handover
        |
        +--> repo intent audit
                schema / nota-codec / signal-frame / orchestrate triad
```

## Latest intent table

| Records | Topic | Constraint now carried |
|---|---|---|
| 628-631 | schema | Parentheses are enum/variant syntax; square brackets are struct/field-vector syntax. This reverses earlier examples. |
| 635-636 | schema/workspace | Design corrections apply globally unless explicitly scoped. Agents must ask where the structural rule applies, not only patch the example. |
| 637-643 | schema | Schema-derived Rust emission is fresh top-down composition from `AssembledSchema`. It must not delegate to legacy `signal_channel!`. The new proc macro name is `emit_schema!`; old body macro is migration-only. |
| 644-645 | intent | Refresh Spirit before maintenance or implementation; track the absorbed intent counter and maintain hot windows by topic. |
| 646, 651 | reports | Context maintenance agglomerates old reports into current summaries and retires stale originals. Reports are working surfaces, not archives. |
| 647-648 | intent | Maintain full constraint tables and audit them against new intent. Repo `INTENT.md` files are core maintained surfaces. |
| 649-650 | architecture/code | When implementation feels awkward, reopen the library/interface design question. Code should be elegant, succinct, and self-describing. |
| 652-655 | interaction | Workspace logic should be modeled as typed interactions: one domain matched against another, typed unavailable/error outcomes, and async state queries through the actor system. |

## Constraint table

| Area | Current constraint | Evidence | Status |
|---|---|---|---|
| Intent-first work | Every maintenance or implementation turn starts by refreshing current Spirit intent. | Spirit 644; AGENTS intent-first rule. | Applied here. This report declares cut 655. |
| Intent windows | Agents should track the highest absorbed intent record and keep hot topic windows for active work. | Spirit 645. | Implemented manually in this report. Needs a shared substrate later. |
| Report maintenance | Old reports get forwarded, migrated, kept rarely, or dropped. Agglomeration should reduce the active desk. | `skills/context-maintenance.md`; Spirit 646, 651. | Applied here; active set reduced to four report entries. |
| Repo intent | Per-repo `INTENT.md` is a core surface, not decoration. | Spirit 648; `skills/repo-intent.md`. | Gaps found below; needs follow-up edits. |
| Global corrections | Psyche design corrections apply to the whole design unless explicitly scoped. | Spirit 636. | Delimiter swap and `emit_schema!` split must be audited everywhere. |
| Schema delimiters | `()` carries enum/variant forms; `[]` carries struct/field vectors. | Spirit 628-631, 635. | Implemented in schema main; older reports and some external prose are stale. |
| Field naming | Struct field names are inferred from type names; the `(Type)` form means an existing type in field position. | Spirit 610-611, 617, 626-627. | Implemented in current schema parsing direction; examples need continued audit. |
| Schema file shape | Current working code reads six top-level values with no outer wrapper: imports, ordinary header, owner header, sema header, namespace, features. | Reports 180, 181, 190; schema code. | Active implementation shape unless psyche reopens arity. |
| Schema parser substrate | Parse universal NOTA into `NotaValue`; schema owns shape recognition and macro passes. | Spirit 588-590, 600, 607-609; report 190. | Mainline schema now uses the shape path; fixed-point user macros remain open. |
| Rust emission | `emit_schema!` consumes structured schema data and emits Rust directly; it must not route through `signal_channel!` or `ChannelSpec`. | Spirit 637-643; designer 340; operator 184. | Partially implemented in `signal-frame` split. Repo prose still stale. |
| Old macro path | Legacy hand-written signal macro can survive only as explicitly legacy migration surface. | Spirit 641, 643. | Should be named/fenced as `legacy_signal_channel!` until deleted. |
| Interact pattern | Most logic is a match between typed domains producing typed outcomes. | Spirit 652-654; second-designer 195. | New design constraint. Schema shape recognition, upgrade planning, daemon dispatch, handover, and orchestrate claims should converge on it. |
| Async state | Interactions that need engine state or outbound checks become async; actor system owns the wait. | Spirit 655. | Needs implementation design before large refactors. Current lean: use existing actor substrate rather than parallel runtime. |
| Orchestrate ingress | Ordinary, owner, and private upgrade sockets must reject wrong-header frames before service dispatch. | Reports 184, 186; orchestrate architecture. | Implemented in recent orchestrate work; remains an active witness. |
| Orchestrate handover | Mirror critical state before readiness and keep upgrade socket private. | Report 186; orchestrate architecture. | Implemented slice; open recovery/divergence boundary remains. |
| Test claims | Test claims need concrete test path, invocation, and witness. | Spirit 577. | Applies to follow-up repo-intent and schema/orchestrate work. |
| Nix usage | Nix calls in this workspace use the remote builder via `--option max-jobs 0`. | User directive. | Applies to future verification; this report pass did not need a Nix build. |
| Elegance rule | If a change produces awkward code, consider changing the supporting library/interface. | Spirit 649-650. | Relevant to replacing macro compatibility layers with fresh schema interfaces. |

## Repository intent and architecture audit

| Repo surface | Finding | Needed action |
|---|---|---|
| `/git/github.com/LiGoldragon/schema/INTENT.md` | Exists, but is stale against records 628-643 and 652-655. It still reflects the v13/Spirit MVP phase and does not carry the bracket swap, `emit_schema!`, no-legacy-emitter constraint, or Interact/match-as-logic direction. | Update as the first repo-intent manifestation pass for schema. |
| `/git/github.com/LiGoldragon/schema/ARCHITECTURE.md` | Mostly current for the bracket swap and schema crate shape, but line 152 says `signal_channel!` emission stays in the macro crate. That boundary is stale after 637-643. | Rephrase boundary: schema owns parsing/assembly; schema-rust/`emit_schema!` owns fresh Rust composition; legacy `signal_channel!` is migration-only. |
| `/git/github.com/LiGoldragon/nota-codec/ARCHITECTURE.md` | The "Macro-pattern integration" section says nota-codec gains the `.schema` reader and `signal-frame-macros` consumes the tree. This conflicts with current architecture. | Narrow nota-codec to NOTA tree/codec and shape predicates only; schema owns `.schema`; schema-rust/`emit_schema!` owns code emission. |
| `/git/github.com/LiGoldragon/signal-frame/ARCHITECTURE.md` | Multiple sections still present `signal_channel!` as the standard future integration path and say `signal-frame/macros` gains schema reader + `AssembledSchema` lowering. | Update to runtime-kernel + legacy macro migration shape. New schema-derived emission goes through `schema-rust` and `emit_schema!`, not the old body macro path. |
| `/git/github.com/LiGoldragon/orchestrate/INTENT.md` | Exists and records dynamic roles plus schema migration, but its pending schema section still says a brilliant macro library reads schema and emits wire types. It does not mention the `emit_schema!` split or Interact direction. | Refresh after schema/signal-frame intent surfaces are corrected, so orchestrate inherits the right migration target. |
| `/git/github.com/LiGoldragon/orchestrate/ARCHITECTURE.md` | Current for short-header ingress and upgrade socket work, but the pending schema-engine section still references hand-written `signal_channel!` conversion and older design reports. | Update pending migration section to point at `emit_schema!`, schema-rust, bracket swap, and Interact-shaped lowering. |
| `/git/github.com/LiGoldragon/signal-orchestrate/ARCHITECTURE.md` | No `INTENT.md`; architecture has stale pending schema text around `signal_channel!` conversion. | Add or synthesize repo intent when project-specific intent is manifested; refresh architecture during orchestrate contract migration. |
| `/git/github.com/LiGoldragon/owner-signal-orchestrate/ARCHITECTURE.md` | No `INTENT.md`; architecture still references the current owner `signal_channel!` invocation. | Same as signal-orchestrate: refresh with owner-policy schema intent before migration. |

## Current implementation picture

Schema is the hottest second-operator context. The current real path is:

```text
.schema files
  -> nota-codec parse_sequence
  -> schema ShapeParser / node shape recognizers
  -> MacroIndex / MacroPipeline
  -> AssembledSchema
  -> schema-rust RustComposer
  -> emit_schema!
```

The first half is real on main. The second half is only partially real:
`emit_schema!` and the legacy split exist, but the composer does not yet emit
the full contract/runtime surface required by the design.

Orchestrate is the second active context. The recent implementation made
ordinary/owner ingress validation and private upgrade-socket handover real.
The next design-improvement pass should port those mechanics toward
schema-derived contract generation and the Interact/match-as-logic surface
rather than adding more ad-hoc dispatch code.

## Gaps needing clarification

1. **Repo-intent manifestation authority.** I can update the stale repo
   `INTENT.md` and architecture surfaces directly, but this crosses from
   operator implementation into workspace intent manifestation. My lean:
   second-operator should patch the implementation-adjacent repo files
   (`schema`, `signal-frame`, `orchestrate`) because the gaps now block correct
   code migration.

2. **Interact trait substrate.** The intent says every object interacts and
   async state queries go through the actor system. The open design point is
   whether the first implementation should use the current actor substrate
   directly or introduce a small shared interaction crate. My lean: start in
   `schema` with a local trait for shape recognition, then promote only after
   two components need the same surface.

3. **Orchestrate handover boundary.** Mirror currently covers claims and
   lanes. Dynamic roles, repository index state, and divergence/recovery
   ledger semantics are not fully settled. My lean: extend Mirror only for
   daemon-owned state that would corrupt active locks if lost; keep derived
   projections refreshable.

4. **Deleting the old streaming schema parser.** The shape parser is the
   current path. The streaming parser is now a diagnostic comparator. My lean:
   delete it after Spirit and Orchestrate both parse through the shape path and
   the equivalence tests stop finding useful defects.

## Next best work

1. Patch repo intent/architecture surfaces for `schema`, `nota-codec`,
   `signal-frame`, and `orchestrate` to reflect records 628-655.
2. Continue schema production work at the `emit_schema!` composer boundary,
   with tests proving schema-derived output does not call legacy
   `signal_channel!`.
3. Start the smallest Interact-shaped refactor where it is already true:
   schema node recognition or orchestrate claim resolution.
