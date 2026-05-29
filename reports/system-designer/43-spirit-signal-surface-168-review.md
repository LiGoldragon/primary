# Review — `/168` Spirit signal-surface bad-pattern audit

*Designer review of `reports/system-operator/168-spirit-signal-surface-bad-pattern-audit-2026-05-28.md`, per psyche direction 2026-05-28. `/168` is a sound, file:line-grounded audit; this review validates it and adds the designer-class lens: its eight findings are all symptoms of ONE root — production `signal-persona-spirit` is still on the OLD signal-schema path where the schema is not the source of truth — and that root's structural fix is exactly the schema-derived migration that `/41` (horizon-next) just proved works end to end.*

## Verdict — `/168` is correct and well-grounded

Every finding is real and cited to file:line. The trigger is concrete (the `(RecordsObserved ([...]))` double-delimiter on a live `RecordIdentifiers` query), the analysis correctly separates the NOTA layer from the signal/schema implementation choice, and the recommended fix order (names first compatibility-preserving → rename projection nouns → fix schema drift → fix the reply-shape substrate → clean the CLI surface) is the right sequence. The conclusion — "not just one ugly enum variant; a cluster of old signal-schema limitations and naming shortcuts leaking into the human-facing CLI" — is exactly right. No correction needed; this review extends it.

## The designer lens — all eight findings share one root

`/168`'s findings sort into three groups, and all three trace to the same root cause: **`signal-persona-spirit` is on the legacy `signal_channel!([schema])` path, where the `.schema` is consumed for channel/route shape but the domain types are hand-written** — so the schema is presented as a contract but is not the source of truth (`/168` finding 8, which it correctly calls "the deepest bad pattern in this audit").

### Group 1 — the schema-not-source-of-truth root (finding 8)

Finding 8 IS the schema-at-heart gap (Spirit record 1000: schema-emitted types are the canonical truth for every type; everything else is methods on those nouns). The drift `/168` shows (`PresenceView [Presence FocusArea]` in the schema vs `{ presence, focus: Option<FocusArea> }` in Rust, the Rust winning because it's what production uses) is the precise failure mode schema-at-heart eliminates. `/168`'s own fix names it: "generate these domain types from the schema so drift becomes impossible." **That structural fix is the schema-derived-stack migration** — and it is no longer hypothetical: `/41` (horizon-next, verified this session) proved a real component's datatypes generate from a pure schema through nota-next → schema-next → schema-rust-next, with collections, cross-crate imports, and a running runtime, hermetically green under `nix flake check`. So finding 8's fix = migrate `signal-persona-spirit` onto the schema-derived stack, now de-risked.

### Group 2 — the reply-shape double-wrapper (findings 4, 5)

`RecordsObserved [(Vec RecordDescription)]` emits `(RecordsObserved ([...]))` because the reply variant head + a same-named single-field payload record stack two layers. `/168`'s fix #4 ("extend the schema feature model so reply variants can carry direct payload expressions, not only same-named payload records") is a schema-emitter capability — and the schema-derived stack now has the two pieces it needs:

- **Collections (record 1034, implemented this session)** — a reply variant can carry a `Vec` directly at the type-reference position: `Projected(Vec<RecordSummary>)` rather than a wrapper record. The `(Vec RecordDescription)` shape `/168` cites is now expressible as a direct variant payload.
- **The data-carrying enum direction (record 1054, implemented in `/41`)** — the `Plane`/`Output` design has enum variants CARRY the message directly (matched on directly), not wrapped in a thin single-field record. `(RecordsObserved [...])` — the clean form `/168` wants — is exactly the shape the schema-derived emitter produces for a variant carrying a direct collection payload.

So the reply-shape substrate fix `/168` calls for is the schema-derived emitter + collections + the Plane/Output variant design — the same work `/41` exercised. Whether the variant names the operation-result (`RecordsObserved`) or the noun (`RecordSummaries`) is a design choice; the data-carrying-enum direction (1054) leans noun-direct (`RecordSummaries [...]`), which also resolves `/168`'s finding-1/2 naming complaint in one move.

### Group 3 — the naming findings (1, 2, 3, 6, 7)

`DescriptionOnly` selects a payload that isn't description-only; `RecordDescription` is a record summary not a description; `RecordProvenance.description` is a whole summary not a string; `Mode` is too generic. These are the workspace naming discipline (`ESSENCE.md` §"Naming": full English words AND no ancestry) applied to the signal surface — validate them. Two designer notes:

- **Finding 7 reveals an EMITTER improvement, not just a local rename.** `record_identifier_selection` (should be `selection` — "the ancestry is already in the containing type") is precisely the AGENTS.md hard override "names don't carry their full ancestry." `/168` notes it "likely came from schema-generated naming pressure" — i.e. the schema-rust emitter generated an ancestry-carrying field name. **So the fix is in the emitter**: schema-rust-next (and schema-rust, the production path) should apply the no-ancestry naming rule when emitting field names from schema field declarations, so the schema-derived migration (Group-1 fix) does not re-introduce ancestry-carrying names. This folds the finding-7 fix into the migration rather than leaving it a one-off hand-rename. (Relevant to the `/41` schema-rust-next work — worth a witness that emitted field names shed the containing type's ancestry.)
- The mode/projection naming (`DescriptionOnly` → `WithoutProvenance`/`SummaryOnly`; `RecordDescription` → `RecordSummary`) should be settled in the schema (the source of truth) once the migration lands, so the name is fixed once and emitted everywhere, not patched in three hand-written places.

## The convergence — two ends of one migration

`/168` (production `signal-persona-spirit`, OLD stack) and the schema-derived stack (`/35`-`/41`, NEW stack) are the two ends of the same migration. `/168`'s tactical recommendation is right for NOW — the naming pass (`DescriptionOnly`, `RecordDescription`) is the highest-signal immediate production fix, and it can land compatibility-preserving without waiting for the migration. But the STRUCTURAL fixes (finding 8's schema-as-source-of-truth + the finding-4 reply-shape substrate) are the schema-derived migration of `signal-persona-spirit` onto schema-next/schema-rust-next — and that is now de-risked, because `/41` proved the emitter handles exactly the surfaces `signal-persona-spirit` needs: collection payloads, cross-crate shared types, a clean data-carrying reply enum, and types-only modules. The Spirit component is, in fact, the natural NEXT real consumer of the schema-derived stack after the horizon-next concept (spirit-next was the pilot; production persona-spirit is the destination).

## Recommendations

1. **Do `/168`'s naming pass now (tactical, compatibility-preserving)** — `DescriptionOnly` → `WithoutProvenance`/`SummaryOnly`, `RecordDescription` → `RecordSummary`, `RecordProvenance.description` → `summary`/`record`, `Mode` → `ObservationMode`/`RecordProjection`, `record_identifier_selection` → `selection`. These are correct today regardless of the migration; per `/168`'s order, names first.
2. **Schedule `signal-persona-spirit`'s migration onto the schema-derived stack as the structural fix for findings 4 + 8** — generate the domain types + reply shapes from `spirit.schema` via schema-next/schema-rust-next, eliminating the drift (finding 8) and producing the clean direct-payload reply shape (findings 4/5). De-risked by `/41`; the production-spirit destination after the horizon-next concept.
3. **Fold finding 7 into the emitter** — schema-rust-next/schema-rust apply the no-ancestry naming rule to emitted field names, with a witness, so the migration doesn't re-introduce ancestry-carrying names like `record_identifier_selection`.
4. **Coordinate with record 1053** (production Spirit query-by-record-number, the `/168` trigger's query) — the reply-shape + naming fixes are part of the same production-spirit evolution; settle the reply nouns (`RecordSummary`, `RecordSummaries`) in the schema as that work lands.

## Note on lane + scope

`/168` is system-operator-authored but reads as designer-class architecture critique (signal-tree naming, schema-source-of-truth, reply-shape substrate) — consistent with the loosened lane boundaries (the work is the work). Its findings inform the schema-stack direction this lane has been auditing; this review is the designer second read. The actual fixes split: the naming pass is operator/system-operator tactical work on production; the schema-derived migration is the larger coordinated arc (operator amalgamation + the schema-next/schema-rust-next emitter improvements).

## See also

- `/system-operator/168-spirit-signal-surface-bad-pattern-audit-2026-05-28.md` — the audit this reviews.
- `/system-designer/41-horizon-schema-pipeline-concept/2-completion-and-fresh-intent.md` — the proven schema-derived component (collections + Plane + types-only + hermetic Nix) that de-risks the `signal-persona-spirit` migration.
- `/system-designer/40-horizon-lojix-schema-next-port-feasibility/3-overview.md` — the schema-as-main-driver feasibility (finding 8's structural fix at the stack level).
- Spirit records: 1000 (schema-at-heart — finding 8), 1034 (collections — the reply-payload fix), 1054 (data-carrying enum — the clean reply shape), 1053 (production Spirit query-by-number — the trigger), 882/AGENTS.md naming (no ancestry — finding 7).
- `ESSENCE.md` §"Naming" + `skills/naming.md` — the discipline the naming findings apply.
