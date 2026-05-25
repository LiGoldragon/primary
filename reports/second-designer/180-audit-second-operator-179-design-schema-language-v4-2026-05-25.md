*Kind: Audit (historical) · Topic: second-operator/179 4-field schema design vs adopted 6-field · Date: 2026-05-25 · Lane: second-designer (counter-ego)*

# 180 — Audit: second-operator/179 design-schema-language-v4 — historical disposition

## §1 Scope

Per psyche directive 2026-05-25 ("audit"), apply intent 511 (audit cycle) to `reports/second-operator/179-design-schema-language-v4/4-overview.md` (dated 2026-05-24 — historical, written when designer was at `/326-v4`; design has since moved through v5-v13). This audit dispositions each substantive proposal against what ACTUALLY LANDED on main between then and now.

## §2 Per-proposal disposition

| /179 proposal | What landed | Disposition |
|---|---|---|
| **4-field schema spine** (headers / imports / namespace / surfaces) | **6-field** per /326-v13 + operator/174-v5 + operator/180 (`{imports} [ordinary] [owner] [sema] {namespace} [features]`) | **REJECTED** — workspace chose explicit 3-position header triad over a single header-set vector |
| Headers as enum-shaped first-position vector with `(Working [...]) (Policy [...]) (Sema [...])` variants | Three separate top-level header positions, names `ordinary` / `owner` / `sema` | **REJECTED** — same shape rejection as above; vocabulary also differs (ordinary/owner/sema vs Working/Policy/Sema) |
| Header form `(Record Entry Assert)` with inline SemaOperation | `(Record [Entry])` per /326-v13 uniform form + `Variant.engine: Option<Engine>` per /171 + operator/180 | **REJECTED** — engine classification moved off header into Variant annotation; uniform `(Verb [SubVariant ...])` adopted (intent 494) |
| Surfaces vector with Reply/Event/Observable/Storage variants | `[features]` at position 6 with Reply/Event/Observable/Upgrade variants per /326-v13 §2 | **ABSORBED** (renamed) — concept adopted; "surfaces" → "features"; Storage deferred (TODO per /176 §13) |
| Type expressions in parens: `(Option Topic)` not `[Option Topic]` | `(Option Topic)`, `(Vec RecordSummary)` per intent 485 + /326-v10 onward | **ABSORBED** ✓ |
| Imports import namespaces selectively: `signal-sema (Select path [Names])` | `(Import path [Names])` + `(ImportAll path)` per /326-v13 + operator/174-v5 | **ABSORBED (different shape)** — selectivity adopted; per-binding name → directive map shape differs; functional equivalence |
| Declaration kinds EXPLICIT: `(Enum [...])`, `(Record [...])`, `(Newtype T)` in NOTA | Positional inference: `[...]` = enum, `(T)` = newtype, `(F1 F2 ...)` = record per /170 + operator's BuiltinSchemaMacro | **REJECTED** — shape-based dispatch chosen over explicit kind tags |
| Repetition `Entry (Entry ...)` is wrong | /326-v13 has `Entry (Topic Kind Summary Context Magnitude Quote)` — no repetition; header `State` and namespace `State` are different objects sharing a name (architectural seam per operator/174-v5) | **OBSOLETE** — the critique targeted an earlier shape that no longer exists; the seam pattern that emerged resolves the concern differently |
| Schema struct with named Rust fields | `Schema { component_name(future), imports, ordinary_header, owner_header, sema_header, namespace, features }` per operator/180 + my /172 mockup A | **ABSORBED (different shape)** — 6 named fields not 4 |
| "No comments in schema; every position defined by base schema" | Positional NOTA across the board per /326-v13; comments retired per intent 426 | **ABSORBED** ✓ |
| Schema field names preserved (implicit in `(field Type)` shape) | `SchemaField { name, schema_type }` landed per operator/180 (`e4e1581c`) | **ABSORBED** — exactly the shape /179 implied |

Score: **5 ABSORBED, 4 REJECTED (with reason), 1 OBSOLETE, 1 ABSORBED-RENAMED**. The 4-vs-6 field shape question was the load-bearing divergence; rejected in favor of 6.

## §3 Why the 4-field shape lost

The workspace settled on 6 because:

1. **Per-leg discoverability**: three explicit header positions (ordinary/owner/sema) make the triad-of-contracts pattern immediately visible at the file level. A single header-set vector buries the triad inside one position.

2. **Operator/174-v5's "header is one concern" pushback**: /179's argument was "headers are one concern; one vector". /174-v5 + /326-v13 implicitly responded: "the triad IS three concerns — ordinary, owner, sema are different authority classes". The triad isn't one concern split three ways; it's three concerns that happen to share a header shape.

3. **Schema-positional teachability**: agents reading a `.schema` file can know "position 2 is owner header" without parsing — file-position determines meaning. With a single header-set vector, agents have to read variant tags to know which header is owner. Marginal cost; small but recurring.

4. **Empty positions are cheap**: /179 critiqued "hard-codes three mostly-empty positions". /326-v13 + /180 ship Spirit with empty `[]` for owner + sema; cost is one bracket pair per empty position. Cheap.

5. **Future extensibility argument cuts both ways**: /179 said one-vector is more extensible (add a new header root variant). 6-field is also extensible (add a new top-level position). The decision came down to per-leg discoverability winning over enum-shape consistency.

The 4-field design wasn't WRONG — it was a coherent alternative path. The 6-field path won on workspace-aesthetic grounds (positional triad explicit) + on operator's day-to-day reading ergonomics.

## §4 Critiques /179 made that are STILL relevant (not yet absorbed)

These are the parts where /179 was right and the current design hasn't caught up yet:

1. **"Repeating the key inside the value as `Entry (Entry ...)` is wrong because it makes the type name pretend to be the declaration kind"** — While /326-v13's actual shape `Entry (Topic Kind ...)` doesn't repeat, the same anti-pattern still appears in some EXTERNAL schemas. The principle that "declaration kind is `Enum/Record/Newtype/Alias`, not the type name" stays relevant. The schema crate's `DeclarationBody` enum captures this — the EXTERNAL NOTA syntax doesn't tag kind explicitly (relies on shape) but the INTERNAL model is explicit. The internal-vs-external asymmetry is a real design choice; /179 wanted both internal and external to be explicit; the workspace chose external-implicit + internal-explicit.

2. **Storage as a feature variant** — /179 lists `(Storage [(Records StoredRecord)])` as one of the surfaces. /326-v13 + operator/180 + my /176 §13 row name Storage as a future feature variant (TODO per /176 §13 "Storage descriptors not yet schema-derived"). /179 anticipated this need before the workspace formalized it. Operator can pull /179's `(Storage [(LocalName TypeName)])` shape as a starting sketch when the Storage feature variant lands.

3. **Inline sema-classification in headers**: /179 proposed `(Record Entry Assert)` where the third position is the SemaOperation discriminator. The current design puts engine on `Variant.engine`. Functionally equivalent BUT the ergonomic claim /179 made ("receive-side can triage early") would require pulling engine onto Route (my /172 mockup B does this; awaiting integration). Once Route carries engine, /179's "early triage" benefit is realized — just through a different syntactic surface.

## §5 What this audit teaches about parallel-path resolution

/179 vs /326-v13 is a classic parallel-design-with-divergent-conclusions case (intent 508 model). Two designer-tier lanes (second-operator at /179, designer at /326 series) produced different schemas for the same prompt. Resolution mechanism:

- Operator/174-v5 read both, picked 6-field, named its reasons → became canonical
- /326 versions absorbed 5 of /179's substantive critiques (paren types, selective imports, surfaces concept, no comments, schema struct with named fields)
- Rejected 4 with explicit reasoning (4-vs-6 field, enum-shaped header set, inline sema in header, declaration kinds explicit in NOTA)
- 1 obsolete because target moved
- 1 absorbed-renamed (surfaces → features)

The pattern that emerged: when parallel paths diverge, the LOSING path's substantive sub-critiques often still get absorbed even when its load-bearing shape proposal loses. /179 lost the 4-vs-6 fight but won on (Option Topic) paren form, selective imports, surfaces-as-variants concept, and field-name preservation.

## §6 Recommendations

1. **No new operator work required from this audit** — /179 is historical; all live work is already on the 6-field path. The audit's value is preserving the alternative-path reasoning for future-context.

2. **When Storage feature variant lands** (currently TODO per /176 §13), reference /179 §"Proposed Spirit shape" §"Surfaces" for the initial shape: `(Storage [(LocalName StoredType)])`. Operator can iterate from there.

3. **When engine-on-Route lands** (my /172 mockup B's REBASE target per /174 §3.6), the "early triage" benefit /179 anticipated will be realized through Route.engine rather than inline header syntax. Functional equivalence holds; document the choice in the eventual landing's commit message.

4. **No bead filing from this audit** — all open work is already on the canonical 6-field path with named beads (primary-602y, primary-ezqx.1, etc.).

## §7 What this audit does NOT do

- Does NOT propose reverting to the 4-field shape — that decision is settled
- Does NOT capture new psyche intent (no new psyche directives surfaced by /179)
- Does NOT recommend operator action — /179 is historical
- Does NOT block any current work — nothing in current main contradicts /179 in a way that needs reconciliation

## §8 References

- `reports/second-operator/179-design-schema-language-v4/4-overview.md` — the report under audit (dated 2026-05-24, pre-v13)
- `reports/designer/326-v13-spirit-complete-schema-vision.md` — the design that won
- `reports/operator/174-v5-schema-import-header-design-critique-2026-05-24.md` — operator's pickup of v13 + rationale for 6-field
- `reports/second-operator/180-schema-v13-model-and-upgrade-implementation-2026-05-24.md` — second-operator's own pivot to 6-field implementation
- `reports/operator/180-schema-field-name-and-upgrade-context-2026-05-25/` — schema field name preservation landing (which /179 anticipated)
- `reports/second-designer/171-audit-second-operator-180-schema-v13-2026-05-24.md` — my prior audit of the 6-field landing
- Intent records 426 (no comments in schema), 485 (paren form for type expressions), 494 (uniform header form), 506 (data-carrying macro variants with input structs), 508 (parallel implementation through tested code), 511 (audit cycle)
