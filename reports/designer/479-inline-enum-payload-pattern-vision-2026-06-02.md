; designer
[nota-design schema-idiom inline-enum-payload variant-anonymous-enum schema-vocabulary-economy sugar-extension data-variant-resolution type-table-lookup]
[Vision report for the inline-enum-payload NOTA pattern + the user's sugar extension that lets the inline header declare data-carrying variants without explicit payload syntax. Spirit search confirmed the general principle was uncaptured before 1467; the sugar extension 1468 makes the inline form fit ALL variant shapes (unit + data-carrying) by letting the codec resolve variant names against the type table. Three worked examples (operator 289 Busy + designer 478 RuntimeSituation + spirit-next Output with sugar). Skill addition proposal — Rule 4 in skills/nota-design.md. Implementation discussion: codec lookup pattern + emission shape considerations.]
2026-06-02
designer

# 479 — Inline enum payload pattern + sugar extension

## TL;DR

The psyche surfaced a NOTA design idiom across two captures today:

- **Spirit 1467 (Decision High)** — the general inline-enum-payload pattern: when a variant's payload would be a single-use enum, inline it as a bracket list (`(Busy [DatabaseOverloaded ResourceDisconnected])`) instead of declaring a named enum + wrapper.
- **Spirit 1468 (Decision High, sugar extension)** — the inline enum-body list can declare variant NAMES without distinguishing unit vs data-carrying. The codec resolves names against the type table: defined-elsewhere-as-newtype → data-carrying; undefined → unit.

Together: inline becomes the right choice for ANY single-position enum, regardless of whether its variants carry data. The header stays compact; the variants' shapes live in their own type definitions.

Spirit search confirms both captures are first-of-kind. Spirit 1209 is partial-overlap (declaration-level only). Operator 1466 is Busy-specific. The general pattern + sugar are now workspace-canonical.

Vision: extend `skills/nota-design.md` with Rule 4 covering both. Apply across new schema sketches. Workspace beauty + vocabulary economy compound (Spirit 1411 + 1387).

## Section 1 — The base pattern (Spirit 1467)

### Inline form

```nota
(VariantName [Option1 Option2 Option3 Option4])
```

The variant's payload IS the inline enum, expressed as a bracket list. Variant name + position provide context.

### Named form

```nota
(VariantName NamedEnumType)
; ... separate ...
NamedEnumType [Option1 Option2 Option3 Option4]
```

The enum has its own name + declaration.

### The choice

Inline fits when: enum is referenced ONLY at this position; payload is small (~2-6 variants); no independent semantic identity; variant name carries most meaning.

Named fits when: enum is reused at multiple positions; enum has independent identity worth naming; large (10+ variants); part of stable cross-component contract.

The HEURISTIC is per-position: when the same inline list shows up at two positions, the pressure to name surfaces naturally. Don't preempt that pressure.

## Section 2 — The sugar extension (Spirit 1468)

### The insight

The user surfaced: *"what if it's defined by being declared like this in the header? That would be nice sugar feature. and the variants can be a newtype defined elsewhere in which case it is a data-variant - but the header doesn't need to know that, hence why it fits such a small space."*

The inline header `[Option1 Option2 Option3]` is a list of variant NAMES. Whether each Option is unit or data-carrying is determined by the option's own type definition elsewhere in the schema:

```nota
; Defined elsewhere (data-carrying variants):
RecordAccepted SemaReceipt
RecordsObserved ObservedRecords
Rejected SignalRejection

; Inline enum header references them:
Output [RecordAccepted RecordsObserved Rejected Busy MaintenanceMode]
;                                                ^^^^ ^^^^^^^^^^^^^^^ unit variants
;        ^^^^^^^^^^^^^^ ^^^^^^^^^^^^^^^^ ^^^^^^^^ data-carrying (resolved from type table)
```

The header is a clean enum-tag list. The variant shapes are factored out into their own type declarations. The codec does the lookup.

### Why this is better than the explicit-paren form

Current (explicit):
```nota
Output [
  (RecordAccepted SemaReceipt)
  (RecordsObserved ObservedRecords)
  (Rejected SignalRejection)
  Busy
  MaintenanceMode
]
```

Five lines + repeated parens + payload-at-position. Reading the variant list means reading past the payload types.

With sugar:
```nota
Output [RecordAccepted RecordsObserved Rejected Busy MaintenanceMode]
```

One line. The reader sees the VARIANT VOCABULARY directly. To know payload shapes, look up each variant's type definition. The separation of concerns matches Rust's `enum Foo { Bar(T), Baz }` shape — the enum body is a list of variants; each variant's shape is its own concern.

### Where the type definitions live

```nota
; schema namespace section:
{
  RecordAccepted SemaReceipt
  RecordsObserved ObservedRecords
  Rejected SignalRejection
  Busy []                              ; unit (empty data)
  MaintenanceMode []                   ; unit
}
```

Or possibly unit variants are simply omitted from the type table — the codec defaults to unit when no entry exists for the name.

This needs codec design — see Section 7.

## Section 3 — Worked example A: operator 289 Busy reply

### Original (named form, full structure)

```nota
Output [
  (RecordAccepted SemaReceipt)
  (RecordsObserved ObservedRecordsReply)
  (RecordRemoved RemoveReceipt)
  (Busy BusyReport)
  (Rejected SignalRejection)
]

BusyReport {
  reason BusyReason
  retry RetryGuidance
}

BusyReason [DatabaseBusy NexusOverloaded MaintenanceMode]
RetryGuidance [(RetryAfter Integer) RetryLater]
```

### Compact per Spirit 1467 (inline enum payload)

```nota
Output [
  (RecordAccepted SemaReceipt)
  (RecordsObserved ObservedRecordsReply)
  (RecordRemoved RemoveReceipt)
  (Busy [DatabaseOverloaded ResourceDisconnected OtherReason] (Optional RetryGuidance))
  (Rejected SignalRejection)
]

RetryGuidance [(RetryAfter Integer) RetryLater]
```

### Maximum compact per Spirit 1467 + 1468 (sugar extension)

```nota
; Type table:
{
  RecordAccepted SemaReceipt
  RecordsObserved ObservedRecordsReply
  RecordRemoved RemoveReceipt
  Rejected SignalRejection
  ; Busy is a single-position enum: inline its body at the Busy declaration:
  Busy [DatabaseOverloaded ResourceDisconnected OtherReason]
  RetryGuidance [(RetryAfter Integer) RetryLater]
}

; Output enum header:
Output [RecordAccepted RecordsObserved RecordRemoved Busy Rejected]
```

The `Output` enum body is now five variant names, all in one line. Each variant's shape is in the type table. The schema reads cleanly: "Output is an enum of these five variants; here are their shapes."

The Busy variant is itself defined as a 3-option inline enum (per Spirit 1467). No `BusyReport` struct anymore; if RetryGuidance becomes needed at Busy, it's added as a positional field at Busy's type definition.

## Section 4 — Worked example B: designer 478 RuntimeSituation

### Original

```nota
RuntimeSituation [
  NormalOperation
  (Backpressure QueueState)
  (SustainedBackpressure (Duration QueueState))
  (EscalatedShedding SheddingPolicy)
  (BudgetExceeded ContinuationBudget)
  (Custom ComponentRuntimeSituation)
]
```

### With sugar extension

```nota
; Type table:
{
  Backpressure QueueState
  SustainedBackpressure (Duration QueueState)
  EscalatedShedding [Aggressive Moderate Light]            ; inline per 1467
  BudgetExceeded ContinuationBudget
  Custom ComponentRuntimeSituation
}

; Inline body:
RuntimeSituation [NormalOperation Backpressure SustainedBackpressure EscalatedShedding BudgetExceeded Custom]
```

The body lists six variants by name. `NormalOperation` is unit (no type-table entry needed, OR the codec accepts undefined-as-unit). The rest are data-carrying with their shapes elsewhere. The reader sees the situation vocabulary at a glance.

## Section 5 — Worked example C: spirit-next current schema with sugar

The current spirit-next schema (operator 281 §"Current Pipeline"):

```nota
{}
[(Record Entry) (Observe Query) (Remove RecordIdentifier)]
[(RecordAccepted SemaReceipt) (RecordsObserved ObservedRecords) (RecordRemoved RemoveReceipt) (Error ErrorReport) (Rejected SignalRejection)]
{
  NexusInput [(Signal Input) (SemaWrite SemaWriteOutput) (SemaRead SemaReadOutput)]
  NexusOutput [(SemaWrite SemaWriteInput) (SemaRead SemaReadInput) (Signal Output)]
  ...
  Entry { Topics * Kind * Description * Magnitude * }
}
```

With sugar:

```nota
; Type table:
{
  Record Entry
  Observe Query
  Remove RecordIdentifier
  RecordAccepted SemaReceipt
  RecordsObserved ObservedRecords
  RecordRemoved RemoveReceipt
  Error ErrorReport
  Rejected SignalRejection

  Signal Input                ; aliases for NexusInput's variants:
  SemaWrite SemaWriteOutput   ; — these wear the NexusInput payload shapes
  SemaRead SemaReadOutput     ;   when used inside NexusInput's body
  Entry { Topics * Kind * Description * Magnitude * }
}

; Inline bodies:
Input [Record Observe Remove]
Output [RecordAccepted RecordsObserved RecordRemoved Error Rejected]
NexusInput [Signal SemaWrite SemaRead]
NexusOutput [Signal SemaWrite SemaRead]   ; SAME names; different payloads in context
```

WAIT — `NexusOutput` references `Signal`, `SemaWrite`, `SemaRead` with DIFFERENT payload types than `NexusInput` uses. The type table can't have two entries for `Signal` (`Input` vs `Output`).

This is a real design issue. Solutions:
- (a) Prefix the variant names in the type table: `NexusInputSignal Input`, `NexusOutputSignal Output`. Then the inline body references them but the reader has to know the prefix.
- (b) Scope the type table per enum: each enum's body can reference variants whose names resolve in the enclosing scope (the namespace of THAT enum's body).
- (c) Mandate that across the schema, each variant name appears in only one enum-body position. `Signal` would need different names in `NexusInput` vs `NexusOutput`.

Designer lean: **(b) scoped type table**. The codec lookup respects enum-namespace boundaries. Inside `NexusInput`'s body, `Signal` resolves to `Signal Input`; inside `NexusOutput`'s body, `Signal` resolves to `Signal Output`. Scoping by enclosing scope is the natural Rust analog.

This is a codec design question for schema-next. Spirit 1468 captures the direction; the resolution mechanism is implementation-pending.

## Section 6 — Skill addition proposal — Rule 4 in `skills/nota-design.md`

```markdown
## Rule 4 — Inline single-use enum payloads; named enums when reused

When a variant's payload would be an enum, choose between inline and named:

### Inline form

A variant's payload can be expressed as an anonymous enum list directly:
`(VariantName [Option1 Option2 Option3])`. The variant name + position carry
the context.

For enum bodies, the sugar extension (per Spirit 1468) lets the body list
just variant names; the codec resolves each name's payload shape from the
schema's type table:

```nota
; Type table declares shapes:
{
  RecordAccepted SemaReceipt
  Busy [DatabaseOverloaded ResourceDisconnected]
  MaintenanceMode []
}

; Body lists variant names:
Output [RecordAccepted Busy MaintenanceMode]
```

This factors variant shapes out of the body and keeps the enum header clean.

### Named form

A named enum type is declared separately and referenced by name:
`(VariantName NamedEnumType)` + `NamedEnumType [Option1 Option2 ...]`.

### Choose inline when

- The enum is referenced ONLY at this position.
- The payload is small (~2-6 variants).
- The enum has no independent semantic identity worth naming.
- The variant's name carries most of the meaning.

### Choose named when

- The enum is reused at multiple positions.
- The enum has independent semantic identity worth naming.
- The enum is large (10+ variants).
- The enum is part of a stable cross-component contract.

The pressure of seeing the same inline list at two positions is the right
signal to surface the shared concept and name the enum. Don't preempt that
pressure.

### Example — Spirit `Magnitude`

`Magnitude [Zero Minimum VeryLow Low Medium High VeryHigh Maximum]` is
rightly NAMED: 8 variants, used across Entry payloads + query filters +
policy declarations. Inlining would force duplication.

### Example — hypothetical Busy reply

`Busy [DatabaseOverloaded ResourceDisconnected MaintenanceMode]` is rightly
INLINE: 3 variants, used only at this position, no independent identity.

### Codec resolution scope

Inline body references resolve against the type table in the schema's
enclosing scope. Different enums can have variant names that resolve to
different payload shapes — scoping handles the asymmetry (e.g.,
`NexusInput`'s `Signal` resolves differently from `NexusOutput`'s `Signal`).
```

This is ~50 lines of skill text; lands as a fourth load-bearing rule.

## Section 7 — Codec + emitter implementation considerations

### Codec resolution

The schema-next codec parses an inline enum body `[Name1 Name2 Name3]` into a list of variant tags. For each tag, the codec:

1. Looks up the name in the enclosing scope's type table.
2. If found, the variant carries the looked-up type as payload (data-carrying).
3. If not found, the variant is unit.

The resolution is COMPILE-TIME (during schema-parse); the runtime variant dispatch reads from the resolved type info.

### Emitter implications

Schema-rust-next emits Rust enum types from NOTA schemas. With the sugar extension:

```nota
Output [RecordAccepted RecordsObserved Busy]
```

The emitter produces:

```rust
pub enum Output {
    RecordAccepted(SemaReceipt),
    RecordsObserved(ObservedRecords),
    Busy(BusyPayload),  // anonymous-enum payload becomes auto-named per emitter convention
}

// Possible emitter convention: anonymous-enum payload gets `<VariantName>Payload` name
pub enum BusyPayload {
    DatabaseOverloaded,
    ResourceDisconnected,
}
```

The emitter convention needs design. Candidates:
- `<VariantName>Payload` for the auto-named enum (e.g., `BusyPayload`).
- `<OuterEnum><VariantName>` (e.g., `OutputBusy`).
- Anonymous Rust enum via `impl Trait` or generics — likely too complex for emitter.

Designer lean: `<VariantName>Payload` convention. Predictable; readable; consistent.

### Scope resolution

When `NexusInput::Signal` and `NexusOutput::Signal` resolve to different payload types, the codec must scope by enclosing enum. Schema-next's import resolver may already support scoped lookups; verify with the 475.1 sub-agent's findings.

## Section 8 — Workspace adoption sequence

### Short term

1. Edit `skills/nota-design.md` with Rule 4 (Section 6 draft).
2. Apply to new schema sketches in design reports.
3. When operator implements Spirit 1466 Busy reply, use inline form (and sugar if codec supports it).

### Medium term

4. Implement the codec sugar extension in schema-next + schema-rust-next emitter. Scope: 1-2 designer pilots → 1 operator implementation slice.
5. Maintenance sweep across existing schemas — identify inline-candidate variants. Opportunistic.

### Long term

6. The sugar lets every component's schema source stay compact. The runner-loop macro per Spirit 1419 + the contract-repo split per Spirit 1422 + this pattern compose: each component declares its types in the type table, its enum bodies as clean variant lists.
7. Per Spirit 1411 beauty — every line of NOTA schema source carries more meaning per token after this lands.

## Section 9 — Decision asks

This report adds NO new ratifications beyond Spirit 1467 + 1468 (both captured today).

Implementation gates:
- Skill edit to `skills/nota-design.md` (Rule 4) — can land now or in next maintenance turn.
- Codec sugar extension in schema-next — designer pilot needed; can fork from current main.
- Schema-rust-next emitter convention for anonymous-enum-payload auto-naming — design slot.

## Cross-references

- `reports/operator/289-nexus-internal-control-interface-2026-06-02.md` — Busy/BusyReport sketch; psyche's correction surfaced 1467.
- `reports/designer/478-inner-nexus-engine-recursive-runtime-control-2026-06-02.md` — RuntimeSituation worked example.
- Spirit records 1209 (square-bracket enum-body declaration — partial overlap), 1387 (schema drives most behavior; terse), 1395 + 1401 (developed interfaces; enum + multi-variant), 1411 (beauty), 1466 (Busy-specific Correction), 1467 (this — general inline pattern), 1468 (this — sugar extension).
- `skills/nota-design.md` Rule 1 (no wrapper when struct) — generalizes the same vocabulary-economy principle; Rule 4 extends to variant payloads.
- `skills/skills.nota` — canonical workspace NOTA example.
- `reports/designer/475-contract-repo-pipeline-situation-and-proposal-2026-06-02/2-overview.md` — confirms schema-next has `ImportResolver` cross-schema-import support; scoped resolution likely fits.

## For the orchestrator (chat ask)

Intent search confirmed the general inline-enum-payload pattern was uncaptured. Spirit 1467 captures the base principle; Spirit 1468 captures the sugar extension (inline body lists variant names; codec resolves payload shapes from type table). Vision: skill Rule 4 (~50 lines); codec sugar implementation; emitter auto-naming convention. Worked example showed NexusInput/NexusOutput `Signal` variant ambiguity → resolution: scope by enclosing enum.
