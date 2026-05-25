*Kind: Audit · Topic: second-operator/187 NOTA shape-logic + schema upgrade macro state · Date: 2026-05-25 · Lane: second-designer (counter-ego)*

# 185 — Audit: second-operator /187 NOTA shape-logic + schema upgrade macro state

## §1 Scope

Per psyche directive 2026-05-25 (pointing at /187), apply intent 511 (audit cycle) to `reports/second-operator/187-nota-shape-logic-and-schema-upgrade-macro-2026-05-25.md`. Operator landed two commits closing /184's load-bearing missing pieces (Pieces 1+2 of the MVP sub-agent's target). This audit cross-references the landing against /184 + /181 §3 + /182 + the in-flight MVP sub-agent dispatch.

## §2 What /187 lands + verification

Two commits on main of two repos:

| Repo | Commit | Description |
|---|---|---|
| `nota-codec` | `323a3a74` | "nota-codec: add structural value shape layer" |
| `schema` | `420e13ea` | "schema: prove nota macro shape pass" (locks to nota-codec 323a3a74) |

New nota-codec public types: `NotaDocument`, `NotaValue`, `NotaMapEntry`, `NotaAtom`, `NotaString`, `NotaStringKind`. Plus `NotaDocument::parse` and `NotaValue::parse` APIs.

Shape API methods on NotaValue: `is_record`, `is_sequence`, `is_map`, `is_block_string`, `is_pascal_identifier`, `identifier_text`, `as_record`, `as_sequence`, `as_map`, `record_head`, `has_record_head`, `record_item_count`, `data_field_count`, `has_data_shape`.

Tests in `nota-codec/tests/value_shape.rs` cover: multi-value NOTA documents; macro-candidate map shapes; data-carrying record shapes; distinguishing `[...]` sequences from `[|...|]` block strings; PascalCase identifier detection.

Tests in `schema/tests/nota_shape.rs` against real fixture `tests/fixtures/schema-e2e/spirit-v0-1-1.schema` prove the first-pass classification of: 6-position file shape, ImportAll/Import directives with local paths, route enum/body declarations from `[...]`, single-ident record candidates `(String)`, multi-ident record candidates `(Topic Kind Summary ...)`, container candidates `(Vec RecordSummary)`, **upgrade macro shape `(Upgrade (FromVersion v0.1) (Migrate Entry))`**.

All checks green: cargo fmt, cargo test, cargo clippy `-D warnings`, nix flake check `--option max-jobs 0`.

## §3 Convergence with /184 + in-flight MVP sub-agent

/187 closes **Pieces 1+2** of my MVP sub-agent's target (NotaValue tree-parser + shape-logic methods). Both commits land on main before sub-agent A returns.

**Sub-agent A status implication**: A's worktree was forked from older main (before `323a3a74`). When A returns, A's Pieces 1+2 will be REDUNDANT (operator's landing supersedes). A's Pieces 3+4+5 (multi-pass pipeline + end-to-end test + meta-circular demo) remain NEW WORK that builds ON TOP OF operator's foundation. The right outcome:

- A rebases onto current main (gets operator's nota-codec landing)
- A's Pieces 1+2 collapse — replaced by operator's `NotaDocument`/`NotaValue`/shape-API
- A's Pieces 3+4+5 remain valuable — multi-pass dispatch + spirit.schema end-to-end + meta-circular extension
- A's report at `/183` should note the convergence + adapt to operator's API

This is the parallel-implementation pattern (intent 508) producing **maximally-convergent-with-minimum-redundancy** evidence: A built the same foundation in parallel; operator landed first; A's marginal value is the upstack pieces.

## §4 The `[|...|]` block-string interpretation — clever resolution

Operator interpreted the psyche's `[... | ...]` enumeration as **block strings in the form `[|content|]`** (sequence-bracket plus pipe-delimiter). Tests confirm distinguishing `[...]` (sequence) from `[|...|]` (block string).

This is a clean resolution of the ambiguity I flagged in /184 §13 Q1. The form `[|...|]` is syntactically distinct from `[...]` so the parser dispatches unambiguously. Without the `|` delimiter pair, inline `[content]` would be ambiguous with a one-element sequence — operator's §"Important design edge" calls this out explicitly.

Note: this is DIFFERENT from the bracket-string form `[text]` mentioned in earlier intent (per /176 + bracket-string transition work). The `[|...|]` form is the BLOCK string (multi-line literal); `[text]` was the simpler bracket-string proposal that hasn't fully landed. Worth tracking that these are TWO different proposals.

**Lean on operator's Q1**: keep the current rule (`[content]` = sequence; `[|...|]` = block string). It cleanly resolves the prompt enumeration without overloading `[]` with delimiter-aware string mode. Confirm with psyche if you want different.

## §5 Real vs design-only — operator's honest status

/187 §"Current reality" is honest about what's wired vs what's still design:

**Real now**:
- Generic NOTA structural parsing in nota-codec ✓
- Schema-side tests prove the first pass works against real `.schema` files ✓
- Schema already parses `Upgrade` features and lowers into `Feature::Upgrade` ✓ (existing per /182)
- `AssembledSchema::plan_upgrade_from` already infers identity / additive enum-variant / explicit migrate / renamed / drops / untranslatable ✓ (existing per /182)

**Still design / not yet wired**:
- Fixed-point macro expansion over generic NotaValue spaces (intent 569)
- User-declared macros that expand into later schema objects
- Deriving + emitting Rust `VersionProjection` implementations from `UpgradePlan` ← **the largest remaining gap per /176 §13 + /181 §3 + /182 §6**
- Production schema parser handoff from `NotaValue` nodes instead of raw `Decoder` stream positions ← /334-v2 §5 step 2 + /184 §13 Q2

Operator's status table confirms my /184 §11 deviation→action map: Pieces 1+2 wired (now via /187); Pieces 3+4+5 remain (MVP sub-agent target); UpgradeMacro emission remains (separate slice per /181 §3 + /182 §7).

## §6 Answering operator's 3 questions

### §6.1 Q1: generic `[content]` as string vs current rule (`[content]` = sequence, `[|...|]` = block string)

**Lean: keep current rule.** Operator's resolution cleanly disambiguates without overloading `[]`. The form `[|content|]` for block strings preserves `[...]` as the unambiguous sequence syntax. The earlier bracket-string proposal `[text]` (per /176 + bracket-string migration work) is a separate concept — if it lands, it lands as a TYPED string position (decoder knows the target type), not as a generic NotaValue shape.

Send back to psyche if you want different — but operator's choice is the principled one.

### §6.2 Q2: Upgrade as feature-vector only vs also namespace-level macro

**Lean: feature-vector only.** Per /326-v13 + /176 §13: namespace position is for TYPE DECLARATIONS; feature position is for CROSS-CUTTING contract surfaces (Reply / Event / Observable / Upgrade / future Storage). Upgrade is cross-cutting (operates on the whole schema's type set). Adding it to namespace breaks position-vs-content discipline.

Counter-argument: if user-defined macros (per future /329 extensibility) want to declare type-specific upgrade rules in the namespace, that's a finer-grained pattern. But for MVP and the canonical Upgrade-feature use case, feature-vector is correct.

### §6.3 Q3: replace schema::Parser with NotaValue traversal vs keep parallel

**Lean: keep parallel for MVP; migrate later** (matches /184 §13 Q2 lean + /334-v2 §5 step 2). Specifically:
- Phase 1 (now): both paths coexist — schema::Parser stays as the production semantic path; NotaValue/NotaDocument as the macro-front classification path
- Phase 2 (after MVP sub-agent's Piece 4 proves byte-equivalence on full pipeline): collapse schema::Parser onto NotaValue traversal
- Phase 3 (after UpgradeMacro lands per /181 §3 + /182 §7): the multi-pass pipeline becomes the canonical reader; schema::Parser deletes

Keep parallel now because (a) production path must keep working through the migration; (b) byte-equivalence proof needs both paths runnable concurrently for the test.

## §7 Implications for the in-flight MVP sub-agent

Sub-agent A was dispatched per /184 to build Pieces 1-5. Operator's /187 landing means:

- **A should rebase onto current main** before continuing — gets `NotaDocument` / `NotaValue` / shape-API for free
- **A's Pieces 1+2 collapse** — replaced by operator's landing
- **A's Pieces 3+4+5 remain valuable** — multi-pass pipeline with shape-logic dispatch + end-to-end test against `spirit.schema` (byte-equivalence vs canonical `schema::Schema::parse_str`) + meta-circular extension demo
- **A's `/183` report should fold** the convergence — note operator's foundation + describe what A built on top

If A has already started writing Pieces 1+2 from scratch in the worktree, A's work becomes a parallel-implementation that demonstrates a SECOND viable shape for the same substrate. Comparison between operator's shape-API and A's shape-API could surface useful insights (per parallel-implementation pattern intent 508).

When A returns I will synthesize against /187. A is still running per the background-agent reminder; no direct intervention needed.

## §8 Deviation table updates

For /176 §13 + /184 §11:

| Row | Before /187 | After /187 |
|---|---|---|
| `NotaValue` tree-parser in nota-codec | NOT (per /334-v2 §3.2) | WIRED (`NotaDocument` + `NotaValue` + `parse_str` + `parse_sequence`) |
| `Lexer::next_token_with_span` | NOT (per /334-v2 Q4) | UNCLEAR — not explicitly named in /187; check operator's commit for span tracking |
| Shape-logic methods on NotaValue | NOT (per intent 588 + operator-prompt) | WIRED (`is_record` / `is_sequence` / `is_map` / `is_block_string` / `is_pascal_identifier` / `record_head` / `record_item_count` / `data_field_count` / `has_data_shape` + accessors) |
| `[|...|]` block string distinction | undefined | WIRED via `is_block_string` |
| Generic first-pass macro dispatch | NOT | WIRED test-side (schema/tests/nota_shape.rs); production parser still uses Decoder |
| Multi-pass with fixed-point (intent 569) | NOT | UNCHANGED — still not wired in production |
| User-declared macros | NOT | UNCHANGED — still design only |
| Schema-derived VersionProjection emission | NOT (hand-written) | UNCHANGED — still the largest remaining gap |
| Production schema parser via NotaValue | NOT (Decoder-based) | UNCHANGED — parallel path; migration deferred |

The biggest wins from /187: tree-parser + shape-logic landed; `[|...|]` distinction resolved; real-fixture test proves shape pass works end-to-end on Spirit's actual schema.

## §9 Recommendations

In priority order:

1. **Confirm the `[content]` vs `[|...|]` design choice** with psyche (operator Q1). Lean stated; one-line confirmation unblocks future schema design.

2. **MVP sub-agent's Pieces 3+4+5 still load-bearing** — when A returns, synthesize against /187: A's multi-pass pipeline + end-to-end test + meta-circular demo become the next layer on top of operator's foundation. A's Pieces 1+2 collapse.

3. **Next operator slice per /181 sequencing**: primary-602y P0 first (production unblocker per /179 §3), then UpgradeMacro per /181 §3 + /182 §7 3-step path (closes largest remaining hand-written deviation). The UpgradeMacro slice now has solid substrate to build on (`NotaValue` + shape-logic + spirit-v0-1-1.schema test fixture).

4. **Backport `[|...|]` block-string awareness** to any earlier-landed bracket-string discussion — there are now TWO different bracket-string-like proposals in the workspace (`[text]` simple form, `[|...|]` block form). Worth a brief note in skills/nota-design.md (or wherever NOTA forms are documented) clarifying the distinction.

5. **Update `/184` reference** — the §13 Q1 open question on `[... | ...]` is now ANSWERED by /187's `[|...|]` interpretation. /184 can be retroactively annotated or superseded; either way, the question is closed.

## §10 References

- `reports/second-operator/187-nota-shape-logic-and-schema-upgrade-macro-2026-05-25.md` — the implementation under audit
- `reports/second-designer/184-fully-schema-and-nota-comprehensive-understanding-2026-05-25.md` — my parallel synthesis (Q1 now answered)
- `reports/second-designer/182-schema-crate-state-and-version-projection-derivation-2026-05-25.md` — schema crate state pre-/187
- `reports/second-designer/181-counter-ego-mvp-leans-2026-05-25.md` §3 — UpgradeMacro MVP (next slice up)
- `reports/second-designer/170-schema-lowering-executor-model-2026-05-24.md` §2 — original shape-dispatch rules
- `reports/designer/334-v2-multi-pass-nota-first-schema-reader.md` — multi-pass model
- `reports/nota-designer/8-nota-schema-lowering-deviation-audit.md` — schema-stack audit
- `/git/github.com/LiGoldragon/nota-codec/` at `323a3a74` — landed code
- `/git/github.com/LiGoldragon/schema/` at `420e13ea` — landed code
- `/git/github.com/LiGoldragon/schema/tests/fixtures/schema-e2e/spirit-v0-1-1.schema` — test fixture
- `/git/github.com/LiGoldragon/schema/tests/nota_shape.rs` — landed end-to-end test
- `/git/github.com/LiGoldragon/nota-codec/tests/value_shape.rs` — landed shape-API tests
- Intent records 511 (audit cycle), 526 (lean confirmations), 549 (multi-pass NOTA-first), 569 (iterative-to-fixed-point), 588 (NOTA shape-logic layer), 589 (multi-pass passes generic NOTA), 595 (fully-schema-and-nota MVP)
