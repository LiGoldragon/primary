*Kind: Audit · Topic: mvp-scope-clarification · Date: 2026-05-24*

# 1 — MVP scope clarification — what's IN, what's POST, what's AMBIGUOUS

*Subagent A of the second-designer 167 MVP advance-and-fix
meta-session. Reads /320 + /321 + /322 + /323 + /324 in order;
extracts the per-element MVP scope matrix; resolves where the four
designer reports gave different answers about Spirit intent 396
(macro emits wire + sema operations + sema lowering); produces an
ordered list of open psyche clarification questions.*

## §1 TL;DR

**Clearly IN MVP** (consistent across /320 + /321 + /322 + /323 +
/324, ratified by intents 405-408):

- NOTA schema reader (`signal-frame-macros/src/schema_reader.rs`)
  with bracket-string path-refs, sandboxed resolution per /320 §2.7.
- Root-type validator with cycle detection + engine-annotation
  validation per /320 §3.4.
- Dual-input `signal_channel!` macro (NOTA-data arm + existing
  Rust-syntax arm) per /320 §2.8.
- `LogVariant` trait at `signal-frame/src/log_variant.rs` per
  /320 §2.12.
- **Layer 1 emission** — `Operation` / `Reply` / `Event` enums +
  composite struct collapse + leaf enums + transparent newtypes +
  NOTA codec impls + rkyv `Archive` impls + Frame aliases.
- **ShortHeader EMISSION** (`log_variant() -> u64`) per channel,
  hierarchical-positional 8-byte layout per /320 §2.10.
- **ShortHeader CONSUMPTION + dispatch trait** (`OperationDispatch`
  + per-channel `SpiritHandler`) per /323 §3.1, ratified by intent
  407 ("Short headers drive receive-side dispatch triage").
- **Schema-derived `VersionProjection` for v0.1.0 → v0.1.1** per
  /323 §3.2, ratified by intents 405 + 406. Identity for unchanged
  types; macro-walked field-by-field for changed types; ONE
  hand-written `From<v010::Certainty> for Magnitude` impl.
- **Box-form NOTA codec library** (`nota-box` under the `nota` repo)
  per /323 §3.3, ratified by intents 404 + 408. Bead `primary-l6pc`.
- Spirit pilot — `signal-persona-spirit/schema.nota` (per /322 §1)
  + `lib.rs` rewrite + `migration.rs` + witness tests.
- Sema-side `LogVariant` impl on `SemaOperation` — **byte 0 only**;
  bytes 1-7 zeroed per /320 §3.1.F.
- Hard-handover cutover discipline — offline-test step + database-
  test-passed marker + production startup gating per /323 §10. Bead
  `primary-x3ci.1`.

**Clearly POST-MVP** (consistent across all reports):

- Sub-byte short-header packing (1-bit Bool, 4-bit small enums,
  multi-byte large enums) per intent 392.
- Full sema bytes 1-7 layout — outcome + component tag + operation
  class per intent 390.
- Schema component daemon (runtime schema registry) per intents
  397-400.
- Recursive Help-on-every-enum per /312 — bead `primary-ezqx.3`.
- Mass workspace cutover from Rust-syntax to NOTA-data input —
  Spirit-only pilot in MVP.
- Owner-contract (`owner-signal-persona-spirit`) schema migration.
- Smart-handover live cutover (Mirror + Divergence + zero-downtime).
- Field-name override syntax `(certainty Magnitude)` per /322 §3.4.

**The big AMBIGUOUS items** (the load-bearing scope contradictions
this report exists to resolve):

1. **Spirit 396 Layer 2 emission** — `Command` + `Effect` enums +
   `ToSemaOperation` + `ToSemaOutcome` derived from `(engine X)`
   annotations. /320 frames it as IN; /321 names it new for MVP;
   /322 lists "engine annotations" as POST; /323 adds dispatch but
   not the `Command/Effect` derivation; /324 lists `OperationDispatch`
   autogen as IN but does NOT separately list Layer 2.
2. **Spirit 396 Layer 3 emission** — default lowering shell calling
   `engine.assert/match/retract/subscribe`. /320 implies IN, /321
   names it new for MVP, /322 names it POST, /323+/324 silent.
3. **Engine annotations in the schema** — the `(engine assert)`
   syntax itself. /320 §2.1 closes the shape decision (Shape A
   explicit); /322 §6.3 lists "engine annotations" as POST. /323
   /324 silent.
4. **Per-variant async handler trait signature** — /323 §8.3 leans
   `async fn handle_*` but flags as DESIGN-DECISION-REVIEW.
5. **Single-variant collapse field naming** (`certainty: Magnitude`
   vs `magnitude: Magnitude`) — /322 §3.4 leans type-derived-with-
   semantic-loss for MVP; not closed.
6. **`nota-box` library location** — `nota/nota-box` peer or
   dedicated schema repo. /324 §10.3 leans peer; not closed.
7. **Database-test-passed marker substrate** — engine commit-log
   entry kind vs daemon-side table. /323 §10.4 leans Option A; not
   closed.

The headline contradiction is items 1-3 — whether the macro emits
**only the wire surface + ShortHeader + dispatch + projection**
(narrow MVP) or **wire + ShortHeader + dispatch + projection + the
sema-engine-routing layer** (broad MVP). Spirit intent 396 itself
is Maximum-certainty and says all three; the question is whether
the FIRST MVP slice (the live Spirit cutover) includes Layer 2/3
or defers them.

The lean is **narrow MVP** — see §6.

## §2 Scope matrix

The matrix scores each design element across the four reports + the
final canonical reference /324. Status legend:

- `IN` — present in MVP scope explicitly.
- `POST` — explicitly out of MVP scope.
- `~IN` — implied IN by surrounding shape but not named.
- `~POST` — implied POST by absence from MVP enumeration.
- `—` — not addressed in that report.
- `AMBIG` — the report's framing is internally ambiguous.

### §2.1 Schema-language substrate

| Element | /320 | /321 | /322 | /323 | /324 | Bead | MVP verdict |
|---|---|---|---|---|---|---|---|
| NOTA schema reader (sandboxed path-refs) | IN §3.1.A | IN §1 | ~IN §3.3 | IN §2 | IN §5 | `ezqx.1` step 2 | **IN** |
| Root-type validator + cycle detection | IN §3.4 | IN §1 | ~IN §3 | ~IN §2 | IN §5 | `ezqx.1` step 4 | **IN** |
| Dual-input macro arm (`[` → NOTA, else Rust) | IN §2.8 | IN §3.2 | — | IN §2 | IN §3 | `ezqx.1` step 3 | **IN** |
| Built-in primitive set (minimal: u8-u64, bool, String, Date, Time, Bytes, Vec, Option) | IN §2.4 | ~IN §3.1 | IN §1 | — | — | `ezqx.1` | **IN** |
| Bracket-string form `[text]` for strings/paths | IN §2.4 | IN §11 | IN §2 | IN §1 | IN §2 | `36iq.7.1` parallel | **IN** (intent 401 hard) |
| Path-ref sandboxing (sibling files + Cargo deps only) | IN §2.7 | ~IN §1 | IN §3.3 | — | IN §5 | `ezqx.1` step 2 | **IN** |
| Single-variant collapse → struct | IN §2.2 | — | IN §4.2 | — | — | `ezqx.1` step 9 | **IN** |
| Schema file location (`<repo>/schema.nota` at root) | IN §2.3 | — | ~IN §8 | — | IN §5 | `ezqx.1` step 8 | **IN** |
| Stream `belongs <StreamName>` annotation | IN §2.5 | — | IN §1 | — | — | `ezqx.1` step 8 | **IN** |
| Channel-section implicit by crate prefix | IN §2.6 | — | — | — | — | `ezqx.1` step 8 | **IN** |
| Field-name override syntax `(field-name Type)` | — | — | POST §3.4 (Option B) | — | POST §10.1 | future | **POST** |

### §2.2 Wire surface — Layer 1

| Element | /320 | /321 | /322 | /323 | /324 | Bead | MVP verdict |
|---|---|---|---|---|---|---|---|
| `Operation` / `Reply` / `Event` enum emission | ~IN §3.1.D | TODAY §1 | IN §4.1 | IN §4 (signal types) | IN §5 | `ezqx.1` step 5 | **IN** |
| NOTA codec derives (`NotaEnum`/`NotaRecord`/`NotaTransparent`) | ~IN §3.1.D | TODAY §1 | IN §4 | IN §4 (derives) | IN §5 | `ezqx.1` step 5 | **IN** |
| rkyv `Archive`/`Serialize`/`Deserialize` derives | ~IN §3.1.D | TODAY §1 | IN §4 | IN §4 (derives) | IN §5 | `ezqx.1` step 5 | **IN** |
| Frame aliases (`type Frame = StreamingFrame<Op, Reply, Event>`) | — | TODAY §1 | — | — | — | `ezqx.1` step 5 | **IN** |
| `From<Payload> for Reply` conversion impls | — | — | — | — | — | `ezqx.1` step 5 | **~IN** (consistent with today's macro) |
| Stream relation witnesses (`DomainStream` + tying events) | — | — | ~IN §6.2 | — | — | `ezqx.1` step 5 | **~IN** |
| Observability (`ObserverFilter` + `ObserverSet` + `Tap/Untap` injection) | — | — | ~IN §4.1 | — | — | `ezqx.1` step 5 | **~IN** (matches today's macro) |

### §2.3 ShortHeader — emission

| Element | /320 | /321 | /322 | /323 | /324 | Bead | MVP verdict |
|---|---|---|---|---|---|---|---|
| `ShortHeader(u64)` newtype | LANDED §2.11 | LANDED §2.1 | LANDED §5.3 | LANDED §2 | LANDED §3 | `2cjv` CLOSED | **DONE** |
| `LogVariant` trait at `signal-frame/src/log_variant.rs` | IN §2.12 | IN §3.4 | IN §4.5 | IN §2 | IN §5 | `ezqx.1` step 1 | **IN** |
| Per-channel `impl LogVariant for Operation` (macro autogen) | IN §3.1.D | IN §3.2 | IN §4.5 | IN §4 | IN §5 | `ezqx.1` step 5 | **IN** |
| Hierarchical-positional layout (byte 0 = root + bytes 1-7 = sub-enums in parallel) | IN §2.10 | IN §3.3 | IN §4.5 | IN §3.1 | IN §5 | `ezqx.1` step 5 | **IN** |
| Even-byte split (1 byte per sub-enum; no packing) | IN §2.9 | IN §3.3 | ~IN §4.5 | — | IN §6 | `ezqx.1` step 5 | **IN** (intent 392 hard) |
| Sub-byte packing (1-bit Bool, 4-bit small enums, multi-byte) | POST §2.9 | POST §3.3 | POST §5.3 | — | POST §6 | future | **POST** |
| Frame `with_short_header()` populator (macro emits `into_frame()`) | IN §3.1.E | IN §1 | IN §4.6 | — | IN §5 | `ezqx.1` step 6 | **IN** |

### §2.4 ShortHeader — consumption + dispatch

| Element | /320 | /321 | /322 | /323 | /324 | Bead | MVP verdict |
|---|---|---|---|---|---|---|---|
| `peek` helpers (`short_header_from_archive` + `short_header_from_length_prefixed`) | — | LANDED §2.1 | LANDED §5.4 | — | LANDED §3 | `2cjv` CLOSED | **DONE** |
| `OperationDispatch` trait per channel | — | — | — | IN §3.1 | IN §5/§7 | `ezqx.1` step 11 | **IN** |
| Macro-emitted dispatch impl matching `header.byte_0()` | — | — | — | IN §3.1 | IN §5 | `ezqx.1` step 11 | **IN** |
| `SpiritHandler` trait (one `handle_*` per Operation variant) | — | — | — | IN §6.1 | IN §5 | `ezqx.1` step 11 | **IN** |
| Per-variant async signature (`async fn handle_*`) | — | — | — | LEAN §8.3 | LEAN §10.2 | `ezqx.1` step 11 | **IN** (lean; needs psyche confirm) |
| Tap-anywhere test (observer receives header on fired Record op) | IN §3.1.H | IN §4.1 | ~IN §5.4 | — | IN §7 | `ezqx.1` step 10 | **IN** |

### §2.5 Sema side

| Element | /320 | /321 | /322 | /323 | /324 | Bead | MVP verdict |
|---|---|---|---|---|---|---|---|
| Reuse `LogVariant` trait for sema-side (no parallel `SemaLogVariant`) | IN §2.13 | IN §3.4 | ~IN §4 | — | IN §7 | `ezqx.1` step 7 | **IN** |
| Manual `LogVariant` impl on `SemaOperation` (byte 0 only) | IN §3.1.F | IN §3.4 | ~POST §6.3 | — | IN §5 | `ezqx.1` step 7 | **IN** (byte 0 only) |
| Sema bytes 1-7 layout (outcome + component + class) | POST §6 | POST §3.4 | POST §6.3 | — | POST §6 | future | **POST** |
| `Command` enum emission per channel | ~IN §1.2 | IN §3.2 | POST §6.3 | — | — | none | **AMBIGUOUS — lean POST** |
| `Effect` enum emission per channel | ~IN §1.2 | IN §3.2 | POST §6.3 | — | — | none | **AMBIGUOUS — lean POST** |
| `ToSemaOperation` impl emission (derived from `(engine X)` annotations) | ~IN §3.1 | IN §3.2 | POST §7.1 | — | — | none | **AMBIGUOUS — lean POST** |
| `ToSemaOutcome` impl emission (derived from `Reply`) | ~IN §3.1 | IN §3.2 | POST §7.1 | — | — | none | **AMBIGUOUS — lean POST** |
| `(engine X)` annotation **shape decision** (Shape A explicit) | IN §2.1 | — | POST §6.3 ("engine annotations") | — | — | `ezqx.1` step 4 (validator accepts) | **AMBIG on inclusion in MVP schema** |
| Default lowering shell (`engine.assert / match / retract / subscribe`) | ~IN §1.1 (closes #1 routing-annotation shape) | IN §3.2 (Layer 3) | POST §6.3 | — | — | none | **AMBIGUOUS — lean POST** |

### §2.6 Version handover

| Element | /320 | /321 | /322 | /323 | /324 | Bead | MVP verdict |
|---|---|---|---|---|---|---|---|
| Schema-derived `VersionProjection` impls (Identity for unchanged) | POST §3.2 (Slot 6) | POST §6 | POST §7 (post-MVP per ezqx.2) | IN §3.2 | IN §5 | `ezqx.1` step 12 | **IN** (intents 405+406 hard) |
| Hand-written `From<v010::Certainty> for Magnitude` impl | — | — | ~POST §7 | IN §3.2 | IN §5 | `ezqx.1` step 12 | **IN** |
| Compile-time-optional code per main/next pair | — | — | — | IN §3.2 | IN §1 | `ezqx.1` step 12 | **IN** (intent 406 hard) |
| Next-as-dep `VersionProjection` (the `next_schema` declaration) | — | — | — | IN §3.2 | IN §1 | `ezqx.1` step 12 | **IN** |

### §2.7 Wire encoding

| Element | /320 | /321 | /322 | /323 | /324 | Bead | MVP verdict |
|---|---|---|---|---|---|---|---|
| Length-prefix + 8-byte short header + rkyv body wire envelope | LANDED | LANDED §2.1 | LANDED §5.3 | — | LANDED §3 | `2cjv` CLOSED | **DONE** |
| Box-form NOTA encoding (`nota-box` library) | — | — | POST §7.3 | IN §3.3 | IN §5 | `primary-l6pc` | **IN** (intent 408 hard) |
| `nota-box` location (`nota/nota-box` peer to `nota-codec`) | — | — | — | LEAN §8.2 | LEAN §10.3 | `primary-l6pc` | **IN** (lean; not closed) |
| Macro-emitted NOTA codec uses `nota-box` for unsized fields | — | — | — | IN §5.1 | IN §5 | `ezqx.1` step 14 | **IN** |

### §2.8 Cutover discipline

| Element | /320 | /321 | /322 | /323 | /324 | Bead | MVP verdict |
|---|---|---|---|---|---|---|---|
| Hard-handover (planned downtime + manual cutover) | — | — | — | IN §10 | IN §1 | `x3ci.1` + `x3ci` | **IN** (intent 410 ratifies) |
| Offline-test mode (v0.1.1 binary against backed-up DB; no writes) | — | — | — | IN §10.1 | IN §5 | `x3ci.1` | **IN** (intent 411 ratifies) |
| Database-test-passed marker entry | — | — | — | IN §10.4 (Option A lean) | IN §5/§7 | `x3ci.1` | **IN** |
| Production startup gating (refuse if marker absent/failed) | — | — | — | IN §10.5 | IN §7 | `x3ci.1` | **IN** |
| Marker substrate: engine commit-log entry kind vs daemon redb table | — | — | — | LEAN §10.4 A | LEAN §10/§7 | `x3ci.1` | **IN** (Option A lean; not closed) |
| Smart-handover live cutover (Mirror + Divergence) | — | — | — | POST §10.2 | POST §6 | future | **POST** |

### §2.9 Spirit pilot specifics

| Element | /320 | /321 | /322 | /323 | /324 | Bead | MVP verdict |
|---|---|---|---|---|---|---|---|
| `signal-persona-spirit/schema.nota` (positional, ~50 lines) | IN §3.1.G | IN §4 | IN §1 | — | IN §5 | `ezqx.1` step 8 | **IN** |
| `signal-persona-spirit/src/lib.rs` rewrite to NOTA-data input | IN §4 step 9 | IN §4 | IN §6.1 | — | IN §5 | `ezqx.1` step 9 | **IN** |
| `signal-persona-spirit/src/migration.rs` (one `From` impl) | — | — | — | IN §3.2 | IN §5 | `ezqx.1` step 12 | **IN** |
| `signal-persona-spirit/tests/short_header.rs` (round-trip + tap) | IN §3.1.H | IN §4 | ~IN §5 | — | IN §5 | `ezqx.1` step 10 | **IN** |
| Spirit owner-contract migration (`owner-signal-persona-spirit`) | — | — | POST §6.3 | — | POST §6 | future | **POST** |
| Recursive Help emission (`spirit '(Help)'`) | POST §3.2 | POST §6 | POST §7.2 | — | POST §6 | `primary-ezqx.3` | **POST** |

## §3 Spirit 396 deep dive — is Layer 2/3 emission in MVP first slice?

The pivotal intent record, captured 2026-05-24 at Maximum certainty:

```nota
(396 signal Decision
  [The signal_channel macro generates from the NOTA schema all
   three outputs — the wire/signal surface, the sema operations
   (classification), and the sema lowering operations (how each
   operation is expressed inside the engine, what kind of decision
   the engine makes).]
  Maximum)
```

The record is **Maximum certainty about the eventual scope of the
macro** — Layers 1 + 2 + 3 all under macro emission, eventually.
The question this report exists to resolve is whether the **first
MVP slice** (the live `primary-ezqx.1` pilot for Spirit) covers
all three layers or only a subset.

### §3.1 The four designer-report positions

Walking the four reports in order:

**/320 frames MVP as closing all 13 design holes**, including:
- Hole 1 (engine-routing annotation shape) — closes at §2.1 with
  Shape A explicit annotation.
- Hole 13 (sema-side `LogVariant` trait shape) — closes at §2.13.

But /320 §3.1 enumerates the LANDS list as wire-surface +
ShortHeader + sema-side `LogVariant` on `SemaOperation` (byte 0
only). The default-lowering layer is NOT enumerated. /320 §6
explicitly excludes "Sema-side header bytes 1-7" but does not
explicitly exclude Layer 2 (`Command`/`Effect`) or Layer 3 (default
lowering shell).

**/321 §3.2 explicitly names all three layers as "NEW for MVP"**:
- Layer 1 — wire surface — "TODAY (Rust-syntax input)"
- Layer 2 — sema operations — "NEW for MVP (today hand-written)"
- Layer 3 — sema lowering — "NEW for MVP (today hand-written)"

/321 is the most expansive reading.

**/322 §6.3 puts most of Layer 2/3 in POST-MVP**:
- "Sema lowering (Command + Effect + dispatcher) — Layer 3 macro
  emission — post-MVP per /164 §5.2 Shape A annotations"
- "Engine annotations `(engine assert)` — post-MVP — MVP schema is
  wire-only"

/322 is the most narrowing reading. The Spirit schema example in
/322 §1 contains NO `(engine X)` annotations.

**/323 introduces dispatch but is silent on Layer 2/3 derivation**:
- /323 §3.1 brings ShortHeader CONSUMPTION + dispatch trait into
  MVP — the macro emits `OperationDispatch` matching `header.byte_0()`
  and `SpiritHandler` (one `handle_*` per `Operation` variant).
- /323 §4 enumerates what the "brilliant macro library" produces:
  signal types, NOTA codec, rkyv codec, `LogVariant`,
  `OperationDispatch`, `VersionProjection`. **Layer 2 (`Command`/
  `Effect`/`ToSemaOperation`/`ToSemaOutcome`) and Layer 3 (default
  lowering shell) are not enumerated.**

/323 effectively narrows /321 by not naming Layer 2/3 in the
expanded scope, while expanding past /322 by including dispatch
trait emission.

**/324 §5 file map**: lists `signal-frame-macros/src/emit.rs`
extended for "LogVariant + Frame populator + `OperationDispatch` +
`VersionProjection`". Layer 2/3 still not named. /324 §7 designer
review checklist also omits Layer 2/3 explicit checks.

### §3.2 The narrow-vs-broad MVP table

| Layer | Narrow MVP (lean) | Broad MVP |
|---|---|---|
| Layer 1 — wire surface | IN | IN |
| Layer 1 — ShortHeader EMIT | IN | IN |
| Layer 1 — ShortHeader CONSUME + dispatch trait | IN | IN |
| Layer 2 — `Command`/`Effect` enums per channel | POST | IN |
| Layer 2 — `ToSemaOperation` derived from `(engine X)` | POST | IN |
| Layer 2 — `ToSemaOutcome` derived from `Reply` | POST | IN |
| Layer 3 — default lowering shell (`engine.assert / match / ...`) | POST | IN |
| Schema carries `(engine X)` annotations | POST | IN |
| Spirit schema bracket-string form (/322 §1) carries no `(engine X)` | matches narrow | needs widening |

### §3.3 The narrow-vs-broad rationale

**For narrow** (lean):

- /322's schema example is the canonical Spirit schema and contains
  no `(engine X)` annotations. The pilot's first NOTA file is the
  wire-only shape.
- /323 (the latest scope authority) introduces dispatch but does
  NOT introduce Layer 2/3 emission. The expansion was deliberate
  but selective.
- /324 (the canonical re-spec) does not list Layer 2/3 in the file
  map or the review checklist.
- The dispatch trait (/323 §3.1) is sufficient for "receive-side
  triage by matching variant arms" (intent 407) WITHOUT Layer 2/3
  — `OperationDispatch::dispatch` routes on `header.byte_0()`
  directly to `handle_record`/`handle_state`/etc.
- The `VersionProjection` (intent 406) is per-type, not per-engine-
  operation. It doesn't need Layer 2/3.
- The hand-written daemon code for Layer 2/3 in
  `persona-spirit/src/observation.rs` + `actors/dispatch.rs` (~240
  LoC per /164 §7) is the obvious next migration but doesn't block
  v0.1.0 → v0.1.1 cutover.

**For broad** (alternative):

- Spirit intent 396 is Maximum and says all three layers.
- /321 explicitly named Layer 2 + 3 as NEW for MVP.
- The /164 schema language v3 grammar (the canonical schema grammar
  designer reference) includes the `(engine X)` annotation shape.
- Migrating Spirit ONLY to wire + ShortHeader leaves the most
  expensive hand-written code (~240 LoC) in place, partially
  defeating intent 405's "MVP Spirit should run on schema-derived
  signal code".

### §3.4 The lean: narrow MVP

**Recommendation: narrow MVP** (Layer 2/3 explicitly POST-MVP),
with the path to broad MVP as a discrete follow-up bead.

Rationale:

1. **Intent 405** says "MVP Spirit should run on schema-derived
   **signal code**" — signal, not sema. The narrow reading honors
   the literal text; "signal code" is Layer 1 + ShortHeader +
   dispatch.
2. **/323 + /324** are the latest authority and both omit Layer 2/3
   from their MVP enumeration. The drift from /321 is intentional
   narrowing.
3. **Spirit 396 is about EVENTUAL scope** — Maximum-certainty about
   what the macro should do, not Maximum-certainty about what lands
   in the first MVP slice. The intent does not say "the MVP must
   emit all three layers"; it says "the macro generates all three
   outputs".
4. **The Spirit /322 schema** has no engine annotations. The
   simplest possible reconciliation with /322 is "MVP schema is
   wire-only; annotations land later". This matches /322 §6.3
   directly.
5. **Operator sizing**: the expanded /323 MVP is already at ~5-8
   operator-hours / ~2 sessions. Pulling Layer 2/3 in adds at least
   another session — both for the macro emission AND for the daemon-
   side replacement of `observation.rs` + `actors/dispatch.rs`.
   Per /323 §8.1 the scope is already on the edge of what operator
   can pickup.

The narrow MVP DOES NOT defer the `(engine X)` annotation **shape
decision** (/320 §2.1) — that's already closed; the validator just
doesn't accept the annotations in the MVP schema, and the schema
files don't include them. The shape decision waits dormant until
the Layer 2/3 follow-up bead.

### §3.5 The narrow MVP's Layer 2/3 follow-up

The natural follow-up bead — call it `primary-ezqx.4` — would:

1. Extend `signal-frame-macros/src/validate.rs` to accept `(engine X)`
   annotations (validator already has Shape A in §2.1's closed
   decision).
2. Extend `signal-frame-macros/src/emit.rs` to emit Layer 2 +
   Layer 3.
3. Update `signal-persona-spirit/schema.nota` to add `(engine X)`
   annotations to relevant variants.
4. Retire `persona-spirit/src/observation.rs` + most of
   `actors/dispatch.rs` (the lowering match).
5. Keep ONE hand-written `Dispatcher` override for `ClassifyStatement`
   (per /164 §6.4 — the only non-default routing in Spirit).

Sized: ~1 operator session post-pilot. The decisions in /320 §2.1
+ §2.13 + /164 §5.2 + §6.3-6.4 already close most of the design.

## §4 Cross-report contradictions

A flat enumeration of the inconsistencies. Numbered for reference
by Subagent E's audit.

### §4.1 Layer 2 / Layer 3 inclusion

See §3 — the load-bearing contradiction. Surfaced first in
`reports/second-operator/176 §"Main audit finding"`. This report
extends that audit with the per-report attribution and the narrow-
vs-broad rationale.

### §4.2 `(engine X)` annotations in the MVP Spirit schema

- /320 §2.1 closes Shape A explicit annotation (`(engine assert)`).
- /322 §6.3 lists "Engine annotations `(engine assert)`" as POST-MVP.
- /322 §1 Spirit schema has NO engine annotations.
- /323 / /324 silent.

**Resolution**: under narrow MVP, the validator accepts no engine
annotations in v0.1; the schema authors don't add them. /320 §2.1's
shape decision stays dormant for the Layer 2/3 follow-up.

### §4.3 `primary-ezqx.2` retirement

- /320 §3.2 lists "Next-as-dep `VersionProjection` emission" as
  "tracked as `primary-ezqx` Slot 6" — i.e., separate bead.
- /323 §5.2 says `primary-ezqx.2` retires into `.1`.
- /324 §4 confirms `primary-ezqx.2` CLOSED.
- `reports/second-operator/176 §"Beads state"` notes `bd ready`
  snapshot still listed `.2` as open.

**Resolution**: /323 + /324 supersede /320; `primary-ezqx.2` should
be closed in bd with a breadcrumb to `.1`. **Operator action
item**: confirm `bd show primary-ezqx.2` reflects closure; if not,
close it. (This is a workspace-discipline fix.)

### §4.4 Spirit pilot scope size

- /320 §3.1 sizes pilot at ~900 LoC macro/lib + ~70 LoC schema + ~200
  LoC tests, "one focused operator session, two with verification".
- /322 §8 reiterates ~860 LoC.
- /323 §8.1 names the scope expansion taking pilot to ~5-8 hours
  across ~2 sessions.
- /324 §5 says "~1450 LoC net new across 2-3 focused operator
  sessions split across `primary-ezqx.1`, `primary-l6pc`,
  `primary-x3ci.1`".

**Resolution**: /324's number is the current best estimate.
`primary-ezqx.1` bead body in `bd show` still reflects the /320
sizing — the NOTES section captures the expansion but the
acceptance text references the older shape. **Operator action
item**: cross-check that the bead acceptance criteria match /324
§7 review checklist before pickup.

### §4.5 `nota-box` library location

- /323 §8.2 leans `nota/nota-box` as a sibling library to `nota-codec`.
- /324 §10.3 reaffirms the lean.
- Neither closed.

**Resolution**: lean confirmed by two reports; treat as **IN MVP**
with the location as `nota/nota-box`. Psyche can override if a
dedicated schema repo materialises.

### §4.6 Database-test-passed marker substrate

- /323 §10.4 leans Option A — reserved row in sema-engine commit
  log.
- /324 §7 reaffirms.
- Neither closed.

**Resolution**: lean confirmed; treat as IN MVP via the engine
commit-log entry kind extension at `sema-engine/src/log.rs` per
/324 §5 file map.

### §4.7 Async-by-default dispatch handler

- /323 §8.3 leans `async fn handle_*` signatures.
- /324 §10.2 reaffirms.
- Neither closed.

**Resolution**: lean confirmed; treat as IN MVP. The macro emits
async signatures; Spirit's Kameo-actor-based daemon plugs in
naturally.

### §4.8 Field-name semantic loss for `certainty: Magnitude`

- /322 §3.4 leans type-name-derived with semantic loss for MVP
  (`pub magnitude: Magnitude` not `pub certainty: Magnitude`).
- /322 §4.2 emitted code shows `pub certainty: Magnitude` —
  inconsistent with §3.4's own lean!
- /324 §10.1 reaffirms type-derived-with-semantic-loss for MVP.

**Resolution**: /322 §4.2's example is **wrong** — the type-derived
default would emit `pub magnitude: Magnitude`, not `pub certainty:
Magnitude`. **Designer correction needed**: either fix /322 §4.2
to emit `pub magnitude` (MVP semantic loss) OR add the per-channel
override syntax to MVP. The lean is the former — fix /322 §4.2 to
emit `magnitude`. Spirit daemon code will need to adapt or wait for
the override syntax.

### §4.9 `OperationDispatch` Layer 2 leak

- /323 §3.1's emitted `OperationDispatch::dispatch` calls
  `decode_body::<Entry>` and then `self.handle_record(entry)`.
- This means the dispatch trait emits BOTH the body decode AND the
  routing to `handle_*` — Layer 1 + (proto-)Layer 2.
- The `SpiritHandler` trait (/323 §6.1) has `handle_record(entry:
  Entry)` — Entry is Layer 1, not a `Command::AssertEntry`.

**Resolution**: this is NOT a Layer 2 leak — the dispatch handler
receives the **typed payload** (Layer 1 type, like `Entry`), not a
command. The handler is still daemon-side hand-written code that
internally chooses to construct a `Command` or skip Commands
entirely. The narrow-MVP boundary holds: macro emits dispatch +
typed payload; daemon-side Command/Effect synthesis (if any) is
hand-written.

### §4.10 Closed-decision marker discipline

- /320 §2 lists 13 closed decisions with `// DESIGN-DECISION-REVIEW
  (designer/320 §2.N)` markers.
- /323 §3.3 + §8.3 + §10.4 add three more decisions with
  `(designer/323 §3.N/§8.N/§10.N)` markers.
- /322 §3.4 adds a marker `(designer/322 §3.4)`.

**Resolution**: marker namespaces overlap cleanly (different report
numbers). Operator inlines all of them at corresponding code sites.
**Audit note**: the marker count is now ~17 across /320 + /322 +
/323; tracking that they all land is part of designer's review
checklist (/324 §7 last row).

## §5 Open psyche clarification questions (ordered by impact on MVP migration)

Numbered by impact — Q1 is the largest scope decision. Each
question states the lean, the alternative, and the trigger for
when the question becomes pressing.

### Q1 — Is Layer 2/3 sema emission in the MVP first slice?

- **Scope**: directly determines pilot size (narrow ~3 sessions vs
  broad ~4-5 sessions) and the v0.1.1 binary contents (does it
  still carry hand-written `observation.rs` + `actors/dispatch.rs`?).
- **Lean**: narrow MVP — Layer 2/3 explicitly POST-MVP, follow-up
  bead `primary-ezqx.4` post-pilot. See §3.4.
- **Alternative**: broad MVP — Spirit intent 396's "all three
  outputs" applies to the first MVP slice; pilot grows.
- **Trigger**: psyche review of this report. The longer the answer
  is delayed, the more `primary-ezqx.1` operator pickup risks
  ambiguity.

### Q2 — Do `(engine X)` annotations land in the MVP Spirit schema?

- **Scope**: determines what `signal-persona-spirit/schema.nota`
  looks like at MVP. If narrow MVP (Q1=narrow), then NO annotations
  (matches /322 §1). If broad MVP, then YES annotations on every
  variant (matches /164 §6.1 + /320 §2.1).
- **Lean**: under narrow MVP, NO — the schema is wire-only. Under
  broad MVP, YES per /320 §2.1 Shape A. Decision follows Q1.
- **Alternative**: even under narrow MVP, the validator could
  ACCEPT the annotations (treating them as comments) so that adding
  them later doesn't require a schema-grammar change. **Lean: yes,
  accept and ignore** — keep /320 §2.1 closed decision dormant in
  the validator; emitter ignores until Layer 2/3 lands.
- **Trigger**: when operator authors the Spirit schema.

### Q3 — Should `nota-box` ship as part of `primary-ezqx.1` or as a
       prerequisite that gates `primary-ezqx.1`?

- **Scope**: scheduling. /323 §5.3 says new bead; /324 §4 says
  `primary-l6pc` is a dependency. If gated, the bead order matters
  and pilot can't start until `nota-box` lands.
- **Lean**: gated dependency. Per /324 §4 — `primary-ezqx.1`
  depends on `primary-l6pc`. Two parallel agents can advance them;
  pilot must wait until `nota-box` exists.
- **Alternative**: make `nota-box` a fallback — pilot starts with
  inline encoding; box-form lands as the second iteration.
- **Trigger**: operator scheduling. If `primary-l6pc` runs slow,
  the fallback may be worth accepting to keep pilot moving.

### Q4 — Field name for `Magnitude` in `Entry`: `certainty` or
       `magnitude`?

- **Scope**: Spirit's `Entry` struct shape; Spirit daemon code that
  references `entry.certainty` vs `entry.magnitude`.
- **Lean**: emit `magnitude` (type-derived default, accept semantic
  loss for MVP). Per /322 §3.4 + /324 §10.1.
- **Alternative**: add field-name override syntax `(certainty
  Magnitude)` to MVP — small extension, preserves semantic naming.
- **Trigger**: operator landing the Spirit schema + lib.rs rewrite.
  /322 §4.2's emitted code is currently WRONG (emits `certainty`
  while §3.4 leans `magnitude`); needs designer correction
  regardless of psyche decision.

### Q5 — Async-by-default dispatch handler signatures?

- **Scope**: macro emission of `SpiritHandler` and similar handler
  traits.
- **Lean**: `async fn handle_*` per /323 §8.3.
- **Alternative**: sync `fn handle_*`; daemons that need async wrap
  manually.
- **Trigger**: macro emit code authoring. Sync handlers can be
  upgraded to async later but with a breaking-trait churn; getting
  this right at MVP avoids breakage. Spirit's daemon is already
  async (Kameo).

### Q6 — Marker substrate: engine commit-log entry kind or daemon-
       side redb table?

- **Scope**: where the "database-test passed" marker lives. Affects
  `sema-engine/src/log.rs` (engine extension) vs new daemon-side
  table.
- **Lean**: engine commit-log entry kind per /323 §10.4 Option A.
- **Alternative**: daemon-side table — keeps marker in daemon's
  database; engine doesn't grow vocabulary.
- **Trigger**: `primary-x3ci.1` operator pickup. Engine extension
  has wider impact (every sema-engine consumer sees the entry
  kind); daemon-side keeps it local.

### Q7 — When does the schema component daemon (intents 397-400)
       enter the workspace?

- **Scope**: meta-architecture. The schema component triad (a
  separate triad keeping runtime schema metadata) was named at
  Principle in 397 with Clarifications 398-400 detailing storage +
  type library + macro substrate.
- **Lean**: explicitly POST-MVP. Pilot uses the library face only
  (per /320 §6 + /322 §6.3 + /323 §9 + /324 §6). The schema
  component daemon is a future epic.
- **Alternative**: bring the type library into MVP (the macro
  substrate) so that the macro EMISSION already produces types
  consumable by the future schema component.
- **Trigger**: as `primary-ezqx.1` lands, the question of where
  the macro's per-channel metadata lives sharpens. **Lean is
  stable** — emit types where they live today; introduce the type
  library when the schema component daemon design lands.

### Q8 — Recursive Help-on-every-enum (`primary-ezqx.3`) — is it
       a follow-up to `.1` or parallel?

- **Scope**: parallelism between `primary-ezqx.1` (MVP pilot) and
  `primary-ezqx.3` (recursive Help).
- **Lean**: parallel — neither depends on the other; both can
  advance simultaneously.
- **Alternative**: `.3` follows `.1` — author Help text in the
  schema requires the schema reader to support comment blocks;
  comment blocks aren't currently a primitive in the v3 grammar.
- **Trigger**: if operator picks up `.3` before `.1`, the comment-
  block primitive needs to land first (small extension). Practical
  recommendation: land `.1` first, `.3` follows; treat the
  comment-block primitive as `.3`'s first sub-task.

### Q9 — Owner-contract migration: when does `owner-signal-persona-
       spirit` migrate?

- **Scope**: workspace migration order. Spirit pilot does the
  ordinary contract; the owner contract is a separate bead.
- **Lean**: explicitly POST-MVP per /322 §6.3 + /324 §6.
- **Alternative**: include in pilot — both contracts migrate
  together. Doubles pilot scope.
- **Trigger**: when `primary-x3ci` (production cutover) lands. The
  owner contract migration is a separate cutover.

### Q10 — Smart-handover live cutover (the post-pilot work): when?

- **Scope**: future cutovers (v0.1.1 → v0.1.2). The hard-handover
  for v0.1.0 → v0.1.1 installs the smart-handover machinery, but
  whether v0.1.2 USES it depends on whether the workspace builds
  v0.1.2 with that path live.
- **Lean**: POST-pilot — install the machinery in v0.1.1 (via
  `primary-x3ci` + `primary-wdl6`), use it from v0.1.2 onward.
- **Alternative**: keep hard-handover for v0.1.2 as well; build
  the smart-handover later.
- **Trigger**: post-MVP when v0.1.2 cutover plans are made.

## §6 Recommended leans (for psyche review)

The leans summarised, in priority order, for fastest psyche
review:

| # | Question | Lean | Confidence |
|---|---|---|---|
| Q1 | Layer 2/3 emission in MVP first slice? | **NARROW MVP** — Layer 2/3 POST-MVP, follow-up bead `primary-ezqx.4`. | High |
| Q2 | `(engine X)` annotations in MVP Spirit schema? | **NO annotations in v0.1 schema; validator accepts but ignores them.** | High (follows Q1) |
| Q3 | `nota-box` part of `.1` or gating prerequisite? | **Gating prerequisite** (`primary-l6pc` dependency per /324 §4). | High |
| Q4 | `entry.certainty` or `entry.magnitude`? | **`entry.magnitude`** — type-derived default; accept semantic loss for MVP; fix /322 §4.2's example. | Medium (psyche may prefer override syntax) |
| Q5 | Async dispatch handler? | **`async fn handle_*`** per /323 §8.3. | High |
| Q6 | Marker substrate? | **Engine commit-log entry kind** per /323 §10.4 Option A. | Medium |
| Q7 | Schema component daemon timing? | **POST-MVP**, pilot uses library face only. | High |
| Q8 | Recursive Help parallelism? | **Parallel** to `.1`; comment-block primitive as `.3`'s first sub-task. | High |
| Q9 | Owner-contract migration timing? | **POST-MVP**, separate cutover bead. | High |
| Q10 | Smart-handover for v0.1.2? | **POST-pilot**, install machinery in v0.1.1, use from v0.1.2. | High |

**Designer corrections that don't need psyche review**:

- **C1**: /322 §4.2's emitted `Entry` struct shows `pub certainty:
  Magnitude`, contradicting /322 §3.4's own lean. Fix to
  `pub magnitude: Magnitude` (unless Q4 reverses lean).
- **C2**: /321 STATUS-BANNERed already; ensure all citations in
  current operator beads point to /324 not /321.
- **C3**: `primary-ezqx.2` should be CLOSED with breadcrumb to
  `.1` per /323 §5.2 + /324 §4. Check `bd show` reflects this.
- **C4**: `primary-ezqx.1` bead acceptance text references the
  older /320 shape; the NOTES section captures the expansion but
  acceptance still describes the narrower pilot. Update acceptance
  to match /324 §7 review checklist.

**The single most decision-load-bearing answer is Q1** — Layer 2/3
in or out of MVP first slice. Every other question depends on or
is consistent with Q1's answer. The lean is NARROW based on /323 +
/324 being the latest authority and both omitting Layer 2/3 from
their MVP enumeration; second-operator 176 §"Main audit finding"
flagged this independently and reached the same conclusion.

## §7 See also

- `reports/designer/320-mvp-schema-language-pilot-unblock.md` —
  closed 13 design holes; §2 markers are the authoritative
  closed-decision register; §3-§4 scope superseded.
- `reports/designer/321-mvp-visual-state-of-play.md` — STATUS-
  BANNERed; the most expansive (Layer 2/3 included) framing.
- `reports/designer/322-spirit-mvp-positional-schema-worked-example.md`
  — Spirit worked example; canonical schema (~50 lines); §6.3 puts
  Layer 2/3 POST-MVP.
- `reports/designer/323-mvp-scope-expansion-per-operator-directive.md`
  — latest scope authority; adds dispatch + projection + box-form;
  silent on Layer 2/3 derivation.
- `reports/designer/324-migration-mvp-spirit-handover-re-specification.md`
  — canonical re-spec consolidating /320 + /322 + /323; the current
  navigable index for operator.
- `reports/second-designer/164-nota-schema-language-vector-of-root-verb-enums-2026-05-24.md`
  — schema-language v3 grammar; §6.3-6.4 details Layer 2/3
  emission shape; §9 lists open psyche questions including the
  engine-annotation shape (closed by /320 §2.1).
- `reports/second-designer/167-mvp-advance-and-fix/0-frame-and-method.md`
  — this meta-session's frame.
- `reports/second-operator/176-designer-awareness-beads-and-report-audit-2026-05-24.md`
  — independent audit surfacing the Layer 2/3 contradiction first
  (§"Main audit finding"); this report extends with per-report
  attribution + lean.
- `bd show primary-ezqx.1` — MVP pilot bead (acceptance text needs
  update per C4 above).
- `bd show primary-l6pc` — `nota-box` dependency bead (per /323
  §5.3).
- `bd show primary-x3ci.1` — pre-migration + hard-handover bead
  (per /323 §10.5).
- Spirit records 388-414 (relevant: 388 short header name; 390
  sema short header symmetric; 391 NOTA schema language; 392 MVP
  even-byte scope; 393-396 vector of root-verb enums + macro emits
  all three layers; 397-400 schema component triad direction; 401
  bracket strings; 404 box-form; 405 MVP runs on schema-derived
  signal code; 406 upgrade code compile-time-optional; 407 short
  headers drive dispatch triage; 408 box-form deserves own library;
  410 manual downtime handover acceptable for 0.1; 411 upgrade
  preflight tests + marker; 412 second-designer dispatches
  subagents during MVP; 413 cross-lane operator authority for MVP
  fixes; 414 MVP active workspace phase).
- `signal-frame/src/frame.rs:20-200` — `ShortHeader` + Frame + peek
  helpers (landed per `primary-2cjv`).
- `signal-persona-spirit/src/lib.rs` — current Spirit contract
  (Rust-syntax `signal_channel!`; ~468 LoC); MVP target rewrite.
- `nota/example.nota` — canonical bracket-string syntax.
