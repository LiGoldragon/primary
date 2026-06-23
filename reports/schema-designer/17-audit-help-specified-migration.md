# 17 — Audit: Help-on-SpecifiedSchema migration (operator's work)

*schema-designer · report 17 · adversarial audit of operator's landed
Help-on-`SpecifiedSchema` migration (signal-spirit `3e84885259e8`, schema-next
`6e6d629d6386`; operator report 15), per the psyche's "audit what operator did."
The double-implementation loop closing the other way: operator landed; designer
audits. A preview of the coming auditor role.*

## Spirit gate

No capture — a task-only audit order. The Q3/`shape` rule the audit checks against
is already `6grf` (which operator clarified); this report verifies the code honours
it, and finds one place it does not yet.

## Method

Six dimensional finders (correctness/tests, the Q3 hash gap, design/cognitive-load,
compaction-correctness, intent-conformance, regression/dead-code) each verified
against the landed code and **independently re-ran both test suites** — not trusting
operator's report. Then an adversarial synthesis. 37 findings: **3 major, 15 minor,
1 nit, 17 praise**. Every suite was reproduced green twice (schema-next ~218 tests;
signal-spirit 19 text-feature tests + the default NOTA-free build), warning-clean,
with the `nota-text` boundary machine-confirmed via `cargo tree --no-default-features`.

The headline: this is a **good migration** — the parallel Help AST is gone, the spine
is codec-driven (no `format!` printer), the hard `6grf` role/shape distinction is
already modelled and pinned, and the naming is honest. It falls short of the psyche's
"beautiful / minimizes cognitive load" bar on the signal-spirit Help type stack
(twelve types where four would do; a schema-next source noun leaked onto the public
client API), and short of "maximizes correctness" on exactly one *forward-looking*
axis — the `shape` field that operator already flagged. M1 is a dated obligation, not
a hidden defect.

## Designer's Audit Verdict — Help-on-SpecifiedSchema Migration (signal-spirit `3e84885259e8`, schema-next `6e6d629d6386`)

### 1. Verdict

The migration is **correct, green, and substantially 6grf-conformant — it lands the design's hard core but ships one latent identity-correctness gap and a layer of avoidable cognitive load.** The central intent claim holds in the code, not just the report: `HelpModel` genuinely stores `Vec<SpecifiedSchema>` (help.rs:211-213), `render` walks that IR exclusively and rebuilds a transient catalog per call, the source-walk artifact is fully deleted (no `SourceField`/`SourceNamespace`/`HelpModelBuilder` survives grep), and the previously-misleading "the SAME resolved IR" header is now accurate. The hardest 6grf distinction — preserve the *immediate* named role boundary (`Certainty`/`Importance`/`Privacy` stay distinct over `Magnitude`) while the *fully-followed* terminal shape is a derived projection — is already modeled correctly in `immediate_body` and pinned by tests. The self-tagged `(Health)` compaction is a true codec round-trip (structural `#[shape(pascal_head, arity=1)]`, not a `format!` special-case) that provably decodes back to a payload-bearing variant. All ~218 schema-next and 19 signal-spirit text-feature tests are independently green across two runs, warning-clean, with the NOTA boundary machine-enforced. Against the psyche's bar it is strong on correctness and honest in naming, but falls short of "beautiful / minimizes cognitive load" on the signal-spirit side (twelve Help types where four would do, a leaked schema-next source noun on the public client API), and short of "maximizes correctness" on exactly one forward-looking axis: `SpecifiedPayload.shape` is a plain hashed field that will silently pollute identity the moment the authorized rebase onto `SpecifiedSchema` lands. None of these are merge-blockers for *today's* behavior; the `shape` gap is a hard deadline against a known-coming change, and the rest is shed-able load the operator can land in the same wave since there is no production to protect.

### 2. Must-fix (severity-ranked)

**M1 — `SpecifiedPayload.shape` is a fully-followed derived projection stored as a plain canonical field; it will enter content AND family hashes the instant identity rebases onto `SpecifiedSchema`.** `major`, intent-violation.
`specified.rs:459-462` — `shape: SpecifiedPayloadShape` has no `#[rkyv(skip)]` and no hash exclusion (confirmed: zero `#[rkyv(skip)]` in the file). It is fully derivable via `payload_shape_for_reference` (specified.rs:886-936), which recurses through transparent newtypes to the terminal leaf — the exact value 6grf names as a derived cache that must be **excluded** from content/family hashes. It is harmless *today* only because identity hashes the resolved `Schema`, not `SpecifiedSchema` (identity.rs:162-164; there is no `SpecifiedSchema::content_hash` anywhere). But `SpecifiedSchema::to_binary_bytes` (specified.rs:88-92) serializes every field, so the moment a `SpecifiedSchema` hash is added, two schemas with identical immediate role boundaries but a newtype that resolves differently would change address — and a transparent-newtype refactor that 6grf says must be hash-invisible would move the address. Sharpest because `immediate_body` sits right beside it and *correctly* preserves the identity-bearing boundary.
**Fix (land BEFORE the rebase — this is the deadline):** preferred is option 2 — remove `shape` from `SpecifiedPayload` and expose it as a derived side-value (`SpecifiedPayload::shape(&self, schema) -> SpecifiedPayloadShape` re-running `payload_shape_for_reference`), since `shape` is consumed in exactly one place inside the IR (`to_help_source_declaration_value`, specified.rs:490-512, reached only from help.rs:321) and is purely a Help-projection cache. Acceptable fallback: keep it as an ergonomic accessor but `#[rkyv(skip)]` it so it never reaches `to_binary_bytes`. Either way add a regression test: two `SpecifiedSchema`s differing only in a transparent-newtype indirection must hash equal. (Operator's own report Q4 flags this as unenforced — it is a *known, already-flagged* follow-up, not a hidden defect, but it must not be allowed to ride the rebase.)

**M2 — schema-next SOURCE noun `SourceDeclarationValue` leaks onto signal-spirit's public Help client API.** `major`, leakage.
`HelpEntry.body: Option<SourceDeclarationValue>` is a public field (help.rs:493) with a public accessor (help.rs:521), reachable from the crate-root-re-exported `HelpResponse` (lib.rs:17) through `entries()`. The canary is real: `help_instance_schema_convergence.rs:14` must `use schema_next::{SourceDeclarationValue, SourceReference}` and pattern-match `SourceDeclarationValue::Reference(...)` to consume signal-spirit's *own* public response. Per 6grf Help is a projection of `SpecifiedSchema`; re-exposing a schema-next `Source*` authored-source noun by name on the client boundary re-couples Help to authored-source vocabulary.
**Fix:** own the client-facing body type in signal-spirit (a neutral `HelpBody`), keeping `SourceDeclarationValue` strictly internal to the projection step. The leak is closed when the convergence test can drop its `schema_next::Source*` import.

**M3 — three parallel `name + Option<SourceDeclarationValue>` bodies (`HelpRoot` / `HelpNode` / `HelpEntry`) where one suffices.** `major`, complexity.
help.rs:369 / :433 / :490 carry the same payload; the catalog builds `HelpRoot`/`HelpNode` then immediately re-packs the identical `(name, body)` pair into `HelpEntry` (help.rs:501-507), discarding `plane`. A reader must hold six types (`HelpRoot`, `HelpNode`, `HelpEntry`, `HelpRoots`, `HelpNodes`, `HelpEntries`) to follow a flow whose content is `Vec<(Name, Option<body>)>` split into roots vs nodes.
**Fix:** collapse `HelpRoot`/`HelpNode` into `HelpEntry`; let `HelpCatalog` hold `roots: Vec<HelpEntry>` and `nodes: Vec<HelpEntry>`, deleting four types and their from_*/find/push/insert methods and rkyv plumbing. `render` keeps root-then-node precedence by searching `roots` first. This subsumes P1, P3, and P4 below.

The integration target (a concrete bar for M2+M3): `HelpModel { schemas: Vec<SpecifiedSchema> }` (drop `HelpSchemas`); transient `HelpCatalog { roots: Vec<HelpEntry>, nodes: Vec<HelpEntry> }` (no rkyv); `HelpResponse { entries: Vec<HelpEntry> }`; `HelpEntry { name: Name, body: HelpBody }` — roughly four-to-five load-bearing types versus twelve, projection boundary owned by signal-spirit.

### 3. Polish (minor / nit)

**P1 — Compaction guard duplicated verbatim at two projection sites.** `specified.rs:416-444` (`SpecifiedVariant`) and `:620-646` (`SpecifiedVariantSummary`) carry a byte-identical self-tag guard *and* identical four-arm `match (payload, stream_relation)` tail; only the payload-derivation closure differs. A programmatic diff confirmed the strings match. No test pins that the two sites agree, so a future edit to one diverges silently while the suite stays green — both sites are live (help.rs:304 and :321). **Fix:** extract one owning associated fn, e.g. `SourceVariantSignature::from_projected(name, Option<SourceVariantPayload>, Option<&StreamRelation>) -> Self`; both call sites build the payload then delegate. Satisfies the method-ownership rule cleanly since `SourceVariantSignature` is the owning noun. (Flagged independently by four sub-audits — high-confidence.)

**P2 — Dead `HelpPlane` / `plane` state.** help.rs:351-355 enum, :370 field, :381-383 pub getter — written at :282-283/:316-324, never read (`from_root` projects only `name`+`body`; no `.plane()` call site in src/ or tests/; `HelpRoot` not re-exported). Pure carrying cost that taxes the cognitive-load bar (a reader must verify Input/Output is *not* rendered). **Fix:** delete enum, field, parameter, getter. Subsumed by M3.

**P3 — `HelpSchemas` is a behaviorless one-field `Vec` wrapper.** help.rs:211-214 wraps `Vec<SpecifiedSchema>` with only `new`/`schemas()` and forces an explicit rkyv `omit_bounds`+bound block that `Vec<SpecifiedSchema>` would carry inline anyway. The chain `HelpModel -> HelpSchemas -> Vec` is two single-field pass-throughs. **Fix:** store `schemas: Vec<SpecifiedSchema>` directly on `HelpModel`, lift the bound block, delete `HelpSchemas` and its re-export.

**P4 — Vestigial rkyv derives on transient-only catalog types.** `HelpRoots`/`HelpNodes`/`HelpRoot`/`HelpNode`/`HelpPlane` derive `Archive`/`Serialize`/`Deserialize` (with full bytecheck/bound blocks on `HelpRoot`/`HelpNode`) yet are reachable only through the deliberately non-rkyv `HelpCatalog`. Nothing serializes them; the machinery misleads a reader into inferring persistence that no longer exists, and the `pub` is orphaned (not re-exported). **Fix:** strip rkyv derives and bound blocks, demote to non-`pub`, keep only `Clone, Debug, Eq, PartialEq`. Dissolves entirely under M3.

**P5 — `HelpName` duplicates `schema_next::Name`.** help.rs:547 `HelpName { value: String }` is structurally identical to schema.rs:15 `Name(String)`, and the code converts between them constantly (`From<&Name>` in, `Name::new(...)` out). This is a *judgment call* against the "names don't carry full ancestry" override — defensible if there's a deliberate API-stability boundary. **Action:** confirm intent; absent a stated reason, use `schema_next::Name` directly and delete `HelpName`. Lower priority than M2/M3.

**P6 — No projection-direction round-trip test for self-tag compaction.** The decode direction is well-pinned (`lowering.rs:117`, `(Entry)==(Entry Entry)`), but no test asserts the *projection* direction (Specified value -> `to_source_variant_signature` -> `(Name)` text, then re-lower asserting `payload.is_some()`) on a same-name enum variant — the actual Help behavior. No golden snapshot captured the old `(X X)` spelling, so nothing broke, but the regression guard for *this feature* is missing. **Fix:** add one test in `specified_schema.rs`/`design_examples.rs` driving the full projection round-trip; this also catches a P1 divergence.

### 4. Praise (genuinely excellent — be specific)

- **The parallel AST is gone and the spine is codec-driven, not hand-printed.** The old persistent source-walk model is fully deleted (grep-confirmed: no `SourceField`/`HelpModelBuilder`/`is_type_name` survivors), `HelpModel` stores only `SpecifiedSchema`, `render` rebuilds a transient catalog per call, and the text codec is the *single* schema-declaration codec end to end (`HelpResponse::from_schema_text` delegates to `SourceDeclarations::from_schema_text`; `to_schema_text` round-trips through it — no `format!`, no parallel decoder). This is the projection-at-the-boundary discipline at the right altitude. (intent-conformance#1, design-cognitive-load#7, regression-deadcode#1)
- **Self-tag compaction is correct by construction.** `SelfTagged(SourceVariantName)` with `#[shape(pascal_head, arity=1)]` (source.rs:2754-2755) is structurally mutually-exclusive from `Unit`'s `pascal_atom` by parenthesis-ness, so `(Health)` can never mis-decode as a unit; `to_enum_variant` resolves the payload unconditionally from the variant's own name (source.rs:2823), so the form is always payload-bearing and reversible. The guard is *precise and complete*: differently-named (`(Other Certainty)`), composite (`(Hardware (Optional HardwareLeaf))`), and streaming payloads correctly do **not** compact; the guard reads the *immediate* reference so `(ExactCertainty)` over a newtype chain keeps its `ExactCertainty` boundary rather than collapsing to `Magnitude`. (compaction-correctness#1, #2)
- **The hard 6grf distinction is already modeled and pinned.** `immediate_body` preserves the named role boundary (`Newtype(RecordIdentifier)` stays one-level) while `shape` follows through to `Scalar(String)` — captured crisply on a single payload at specified_schema.rs:120-130. `(Entry { ... Certainty Importance Privacy ... })` renders the three Magnitude-wrappers as distinct names, test-pinned at generated_contract.rs:340. The fix for M1 is surgical *precisely because* the immediate/followed split is already correct — `immediate_body` is the asset.
- **All suites independently green, twice, warning-clean, with the NOTA boundary machine-enforced.** ~218 schema-next + 19 signal-spirit text tests pass with zero `#[ignore]`; the default (non-`nota-text`) build links zero NOTA/schema-next code, verified both via `cargo tree --no-default-features` and the in-repo `dependency_boundary.rs` invariants. The `-121` net diff dropped zero tests — assertions were retargeted (`(VerbatimQuote { QuoteText OptionalAntecedent })`, `(Domain [(Health) (Food) ...])`) to the intended one-level-projection semantics, not lost coverage. INTENT.md was correctly updated to the SpecifiedSchema basis with no stale "source-walk" language.
- **Naming is honest, not the dishonesty the brief hypothesized.** `HelpModel` genuinely stores `SpecifiedSchema`; `HelpEntry` is explicitly documented as "a re-headed schema declaration projected from SpecifiedSchema." The IR and the response projection being different types is *correct* per 6grf — the real issue (M2) is the projection type chosen, a coupling problem, not a truthfulness one. Worth not over-charging.

### 5. Severity-ranked table

| # | Severity | Kind | Finding | Location | Fix |
|---|---|---|---|---|---|
| M1 | major | intent-violation | `shape` derived field will pollute content/family hashes on identity rebase | specified.rs:459-462 (derive at :886-936) | Remove from IR as derived side-value, or `#[rkyv(skip)]`; pin a hash-invariance test — **before** the rebase |
| M2 | major | leakage | `SourceDeclarationValue` (schema-next source noun) on public Help client API | help.rs:493, :521, lib.rs:17; canary test:14 | Own a neutral `HelpBody` in signal-spirit |
| M3 | major | complexity | Three parallel `name+body` types (HelpRoot/HelpNode/HelpEntry) | help.rs:369, :433, :490 | Collapse into `HelpEntry`; catalog holds `Vec<HelpEntry>` |
| P1 | minor | repetition | Compaction guard + match tail duplicated verbatim, untested for agreement | specified.rs:416-444, :620-646 | `SourceVariantSignature::from_projected(...)`; both sites delegate |
| P2 | minor | dead-code | `HelpPlane`/`plane` written, never read | help.rs:351, :370, :381 | Delete (subsumed by M3) |
| P3 | minor | complexity | `HelpSchemas` behaviorless one-field wrapper | help.rs:211, :152 | Store `Vec<SpecifiedSchema>` on `HelpModel` directly |
| P4 | minor | dead-code | Vestigial rkyv derives/`pub` on transient catalog types | help.rs:328, :357, :394, :421 | Strip rkyv + `pub` (subsumed by M3) |
| P5 | minor | repetition | `HelpName` duplicates `schema_next::Name` | help.rs:547; schema.rs:15 | Use `Name` directly — confirm intent first |
| P6 | minor | correctness | No projection-direction round-trip test for self-tag | specified_schema.rs, lowering.rs:117 | Add Specified->text->re-lower test asserting `payload.is_some()` |

Bottom line: **merge stands for today's behavior; M1 is a dated obligation against the authorized identity rebase and must be cleared before it lands; M2+M3 are the same-wave cleanup that moves this from "correct" to "beautiful."** M1 leads exactly as expected.
