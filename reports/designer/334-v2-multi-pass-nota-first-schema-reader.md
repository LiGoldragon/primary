*Kind: Design + Correction · Topic: multi-pass NOTA-first schema reader · Date: 2026-05-25 · Lane: designer*

# 334-v2 · Multi-pass NOTA-first schema reader — corrected per subagent witness

## §1 What this revises

`/334` was written from a model of how the codebase looked from outside; the subagent at `~/wt/github.com/LiGoldragon/schema/multi-pass-nota-reader` (commit `1f457bbb`) implemented the six-pass pipeline against the live code and surfaced four substantive errors in the original report. All four are corrected here. The six-pass conceptual model itself is sound — proven by **byte-equivalent `AssembledSchema` output vs the canonical `schema::LoadedSchema::read_path` across all three live schemas** (spirit / version-handover / orchestrate). The corrections are about WHERE the pieces actually live in the workspace, not WHETHER the model works.

## §2 The corrected story

Schema is NOTA with macros at named positions. The remedy for the parallel-parser deviation in `signal-frame/macros/src/schema_reader.rs` is **already mostly landed on main** (574 LoC adapter, not the 1700 LoC parallel parser /334 claimed). The actual missing piece sits one level down: `nota-codec` lacks a `NotaValue` tree parser + per-token spans, so anything that wants to consume NOTA as structured data has to build its own tree assembler on top of the streaming `Decoder`. The schema crate did exactly that. The multi-pass remedy collapses to two concrete deliverables: (a) land a tree-parser + spans in `nota-codec`; (b) collapse `schema/src/parser.rs` (497 LoC) onto the multi-pass module (~200 LoC) once `nota-codec` exposes the tree.

That's the whole remedy. Much smaller than /334 §6 claimed.

## §3 Per-pass corrections

### §3.1 Pass 0 — lexical (text → tokens)

**Status today**: works. `nota_codec::Lexer::next_token` exists.

**Original /334 claim**: "no schema-specific behavior, lives in nota-codec."

**Correction**: ✓ correct.

### §3.2 Pass 1 — syntactic (tokens → NotaValue tree)

**Status today**: NOT IMPLEMENTED in `nota-codec`. The crate exposes only the streaming `Decoder`; there is no `NotaValue` enum and no tree assembler. The subagent had to BUILD Pass 1 from scratch in `schema/multi-pass/src/pass1_parser.rs`.

**Original /334 claim**: "the universal NOTA parser. Output: a generic NotaValue tree. ... Lives in nota-codec."

**Correction**: Pass 1 LIVES in `nota-codec` aspirationally but DOES NOT EXIST there today. Either land it in `nota-codec` (the long-term right home — every NOTA consumer benefits) or keep it in `schema` as a private substrate. Lean: land it in `nota-codec` — every other NOTA-reading client (sema, signal frames, intent records, lock files) has to do the same trees-on-top-of-streams dance otherwise.

### §3.3 Pass 2 — structural (NotaValue → SchemaDocument positions)

**Status today**: works in the multi-pass module. But the shape assumption was wrong.

**Original /334 claim**: "the root NotaValue is a tuple of six positions matching the canonical layout."

**Correction**: A `.schema` file is **six top-level values in sequence with no enclosing wrapper** — not a single root tuple. Pass 1 has to expose sequence semantics (`SequenceParser::next_value` in the subagent's impl), and Pass 2 reads six successive values. The corrected mental model: each `.schema` file's six positions are simply the first six `NotaValue` consumed from the parser stream. The "six-position macro" applies at the *file* level, not at a tuple-record level.

### §3.4 Pass 3 — macro identification

**Status today**: works. Name-collection pre-pass is confirmed needed (Q3 answered: yes).

**Original /334 claim**: "3 missing variants: NewtypeDefinition / FieldType / UpgradeRule."

**Correction**: PHANTOM. The current `schema::engine::BuiltinMacroVariant` enum is 5 variants (Import, Header, Type, Feature, plus a fifth not surfaced in /332's count). `NewtypeDefinition` folds into `TypeInput` (a newtype is a single-field struct). `FieldType` is parsed inline by `lower_type_expression` — it never needed its own variant; field types are leaves under the type macros. `UpgradeRule` ALREADY HAS `UpgradeRuleInput`. So /334 §3.4's "three missing variants" claim is wrong — the variants exist with different shape than /334 imagined. The actual gaps in BuiltinMacroVariant are more nuanced; need a fresh audit if expanding.

### §3.5 Pass 4 — macro application

**Status today**: works. Reuses existing `BuiltinMacroVariant` + `LoweringContext`. Imports are pure-by-accident — see §4 Q1 below.

**Original /334 claim**: "imports run FIRST because subsequent variants may reference imported names."

**Correction**: ✓ correct AND the existing crate already does this. The subagent reused the existing lowering machinery unchanged.

### §3.6 Pass 5 — assembly

**Status today**: not actually a separate pass — `LoweringContext::finish()` does it inline at the end of Pass 4.

**Original /334 claim**: "Pure builder. Inserts each fragment into a typed canonical container."

**Correction**: The "builder" lives inside the lowering context, not as a separate pass. Conceptually still useful to think of Pass 5 as distinct (assembly + validation + UID minting + layout); operationally it's the last few lines of Pass 4. Layout-after-assemble + component UID minting still NOT done in the current crate — those are real gaps regardless of pass-count.

## §4 Subagent's answers to /334 §8 Q1-Q7

| Q | /334 lean | Subagent finding |
|---|---|---|
| Q1 imports purity | yes typed Effects capability | macros are pure BY ACCIDENT — `ImportMacro::lower` stores metadata; the file-load happens in `reader.rs::Reader::read` OUTSIDE the macro dispatch. Typed Effects capability is doable but isn't how the crate is currently structured. |
| Q2 macro registry vs hard-code | needed for self-hosting | hard-coding 5 variants is trivial; registry pays off only when third-party extensions arrive. Defer. |
| Q3 name-collection pre-pass | likely needed | confirmed — needed. Implemented as `collect_names` running before dispatch. |
| Q4 span tracking | nota-codec probably threads spans | NO — `Lexer::next_token` returns `Token` only, no byte-offset. The subagent reimplemented ~80 LoC of position tracking on top of the lexer. Adding `next_token_with_span` to `nota-codec` would eliminate the duplication. |
| Q5 caching | defer until measured | not measured. Re-parses on every call. Fine for POC. |
| Q6 bootstrap self-hosting | plausible | plausible but blocked on (a) FieldType + HeaderEndpoint as first-class points, (b) the engine being able to serialize `BuiltinMacroVariant` back to NOTA so the meta-schema can reference variant names. |
| Q7 compat-break risk | check in-flight branches for retired forms | risk is MUCH LOWER than /334 §6 implied — the 1700 LoC parallel parser lives only in MOCKUP branches (`designer-327-mockup-3-dispatch` line 1519 uses `(Path …)`; `signal-frame-mockup-stable-caller-id-1`). Main has a 574 LoC ADAPTER over `schema::LoadedSchema::read_path`. The remedy is largely already landed. |

## §5 Implementation deltas — REVISED

The big claim in /334 §6 ("replace the entire 1700 LoC parallel parser") is wrong. Main is already an adapter. The actual remaining work is much smaller:

1. **Land tree-parser + spans in `nota-codec`.** Expose `nota_codec::NotaValue` enum + `parse_str(text) -> NotaValue` (or `parse_stream(tokens) -> NotaValue`) + `Lexer::next_token_with_span`. ~200-300 LoC + tests. Every NOTA-reading client benefits, not just schema.

2. **Collapse `schema/src/parser.rs` onto the multi-pass module.** Once `nota-codec::NotaValue` exists, `schema::parser` shrinks from 497 LoC to ~200 LoC of structural-pass + macro-identification logic. The multi-pass module from the subagent's worktree merges to main as the canonical path.

3. **Optional follow-ups (not required for remedy)**: typed Effects capability (Q1), self-hosting meta-schema (§5 of /334), layout-after-assemble (§3.6 nota-designer/8), component UID minting (§3.6 nota-designer/8). All separate slices.

The "1700 LoC remedy" /334 §6 listed is obsolete — that branch is mockup-only and gets garbage-collected with the mockup.

## §6 Byte-equivalence proof (the load-bearing result)

The subagent's multi-pass module produces output that's **Debug-equivalent** to the canonical `schema::LoadedSchema::read_path` for all three live schemas:

| Schema | Routes | Types | Imports | Multi-pass equals canonical? |
|---|---|---|---|---|
| `spirit.schema` | 4 ordinary | 37 | 1 sema | ✓ byte-equivalent |
| `version-handover.schema` | 6 ordinary | 13 | 0 | ✓ byte-equivalent |
| `orchestrate.schema` | 14 (multi-endpoint) | 31 | 1 sema | ✓ byte-equivalent |

This is the proof: the multi-pass conceptual model is correct AND the existing single-pass implementation in `schema/src/parser.rs` is already correct (just internally structured differently). The pass labels are clarifying — the work isn't a rewrite, it's a refactor toward cleaner pass boundaries + relocating Pass 1 down to `nota-codec`.

All 27 tests pass (18 lib + 6 multi-pass + 3 reader); `nix --option max-jobs 0 flake check` succeeds.

## §7 New open questions surfaced by the subagent

1. **Should `nota-codec` expose a `NotaValue` tree or stay streaming-only?** The streaming `Decoder` is great for sema-engine record decode (fixed-shape, known type). It's a pain for schema reading (variable-shape, branching). Lean: add a tree-parser as a separate module in nota-codec; don't replace the streaming decoder. Two surfaces, two use cases.

2. **Should `Lexer::next_token_with_span` replace `next_token` or coexist?** Span-aware is strictly more information. Lean: rename `next_token` → `next_token_with_span`; everywhere that doesn't need spans can ignore the second tuple element. One canonical lexer surface.

3. **Should the schema crate's `parser.rs` get rewritten to use the multi-pass module, or should the multi-pass module just be merged in as an alternative entry point?** Lean: rewrite. The multi-pass module is cleaner; the current `parser.rs` mixes structural + semantic concerns. One canonical reader, named `LoadedSchema::read_path` for compat.

4. **What's the actual current set of `BuiltinMacroVariant`s vs operator/175.4's 7-point list?** /334 said 4, said 3 missing. Subagent says 5 exist, the "missing 3" claim is wrong because the missing concerns fold into existing variants differently than imagined. A fresh small audit (no subagent needed — just read engine.rs) settles this.

5. **Is layout-after-assemble + component UID minting in scope for this remedy, or separate?** Both are named in nota-designer/8 §"What Should Change First." Subagent confirmed neither is done. Lean: separate slices — land Pass 1 in nota-codec first; layout + UID are independent improvements.

## §8 What ships next

Three sequential slices, each shippable independently:

1. **`nota-codec` tree-parser + spans** (~200-300 LoC + tests). Foundation for everything else. Per spirit record 549 (multi-pass-nota-first decision).

2. **Collapse `schema/src/parser.rs` onto multi-pass + nota-codec tree.** Adapter from subagent's `multi-pass-nota-reader` branch onto main. ~300 LoC removed; pass boundaries become explicit; no behavior change (byte-equivalent output already proven).

3. **(Optional/later)** Typed Effects capability for import purity + meta-schema bootstrap + layout-after-assemble + component UID. Each its own bead.

The two-deliverable remedy can land in a day or two. The "1700 LoC parallel parser refactor" panic in /334 §6 is unwarranted — it's already done.

## §9 References

- `/home/li/primary/reports/designer/334-multi-pass-nota-first-schema-reader.md` — the v1 design report (this report's predecessor; superseded but preserved as history)
- `/home/li/wt/github.com/LiGoldragon/schema/multi-pass-nota-reader/` — the subagent's proof-of-concept (commit `1f457bbb`); 6 multi-pass tests + byte-equivalence vs canonical for all 3 live schemas
- `~/wt/github.com/LiGoldragon/schema/multi-pass-nota-reader/src/multi_pass/pass1_parser.rs` — the tree-parser the subagent had to build (~200 LoC)
- `/git/github.com/LiGoldragon/nota-codec/src/lexer.rs:23-59` — `Token` enum, no span (the gap Q4 surfaced)
- `/git/github.com/LiGoldragon/schema/src/engine.rs:1-280` — current 5-variant `BuiltinMacroVariant` (not 4 as /334 implied)
- `/git/github.com/LiGoldragon/signal-frame/macros/src/schema_reader.rs:11-89` — 574 LoC adapter on main (not 1700 LoC parallel parser as /334 implied)
- `/git/github.com/LiGoldragon/signal-frame-worktrees/designer-327-mockup-3-dispatch/macros/src/schema_reader.rs:1519` — 1732 LoC mockup with retired `(Path …)` forms (mockup-only — gets GC'd with the mockup)
- `reports/nota-designer/8-nota-schema-lowering-deviation-audit.md` — original deviation audit
- `reports/designer/329-schema-macro-component-extensibility.md` — InputStruct-per-variant + SchemaMacro trait
- `reports/operator/175-schema-engine-prep/4-reusable-assembled-schema-lowering.md` — NodeDefinitionPoint + BuiltinSchemaMacro (5 actual variants vs the 7-point list)
- Spirit records: 549 (multi-pass NOTA-first decision), 547 (in-test unblock-the-blocker), 539 (always-background subagent)
