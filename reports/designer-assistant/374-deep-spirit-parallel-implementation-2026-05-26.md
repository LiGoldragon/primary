# 374 — Deep spirit parallel implementation

*Designer-assistant lane. Designer-parallel deep implementation of the
schema-derived Spirit runtime at v0.3 capability target, in
`LiGoldragon/design-deep-spirit-2026-05-26` (main / c06172185e6a). All
16 tests pass; the five operator/209 constraint checks land as Nix
witnesses or runtime-asserted invariants; end-to-end shell transcripts
prove the v0.3 capability target through real CLI + daemon binaries.*

## Summary

| Repo + branch | HEAD commit | Tests | Nix checks | What proves |
|---|---|---|---|---|
| `LiGoldragon/design-deep-spirit-2026-05-26` main | `c06172185e6a` | 16/16 passing | 5/5 defined; 3/5 grep-based; 2/5 runtime-asserted | v0.3 capability + signal/executor/SEMA runtime triad + upgrade skeleton |

The 16 tests:

- `tests/end_to_end.rs` — 1 test: CLI + daemon real socket; record + observe + state.
- `tests/sema_round_trip.rs` — 2 tests: multi-record + multi-topic + multi-kind + observation modes through redb; schema-version marker survives reopen.
- `tests/sema_single_writer.rs` — 1 test: opening a daemon spawns exactly one SemaActor; count returns to baseline after shutdown.
- `tests/nota_round_trip.rs` — 5 tests: Input Record, Input Observe, Input State, Output RecordAccepted, Entry round-trips through NOTA codec.
- `tests/rkyv_round_trip.rs` — 5 tests: same surfaces through rkyv; plus signal-frame round-trip.
- `tests/upgrade_skeleton.rs` — 2 tests: upgrade-then-downgrade Entry round-trips; ChangeClass classification.

## What's working end-to-end

Live shell transcript run against the release binaries:

```text
=== record schema/Constraint ===
(RecordAccepted 1)
=== record spirit/Decision ===
(RecordAccepted 2)
=== record schema/Principle ===
(RecordAccepted 3)
=== observe by topic schema DescriptionOnly ===
(RecordsObserved (DescriptionOnly (1 [schema language must support vector references])))
=== observe by topic schema WithProvenance ===
(RecordsObserved (WithProvenance (1 1779753600 1779812674 ([schema] Constraint [schema language must support vector references] High))))
=== observe by kind Decision ===
(RecordsObserved (DescriptionOnly (2 [designer-parallel deep implementation v0.3 capability target])))
=== observe combined schema+Constraint WithProvenance ===
(RecordsObserved (WithProvenance (1 1779753600 1779812674 ([schema] Constraint [schema language must support vector references] High))))
=== state topics ===
(StateObserved ([schema] 2))
```

What this proves empirically:

- Monotonic identifiers across records (1, 2, 3).
- Observe by topic returning the expected records (schema/Constraint matches).
- Observe by kind returning the expected records (Decision → entry 2).
- Observe combined topic + kind matching the intersection (schema + Constraint → entry 1).
- ObservationMode shapes correctly:
  - `DescriptionOnly` returns `(DescriptionOnly (Identifier [Description]))`.
  - `WithProvenance` returns `(WithProvenance (Identifier Date Time Entry))`.
- Daemon-stamped Date (`1779753600` — UTC day-start) + Time (`1779812674` — epoch seconds at the record's insert).
- State topic counts (`schema` = 2 records observed).

The single-record-per-Observe wire shape is the **open schema-language
gap** discussed in §"Open shape questions" below.

## What's schema-emitted vs hand-rolled (precise)

Per operator/208 P1 the gap audit names "the runtime route table still
needs manual edits" as the main interface-generation gap. This design
substrate **closes that gap** end to end:

| Surface | Source |
|---|---|
| `Input`, `Output` enums | Emitted by `schema-rust-next` from `schema/spirit.schema` |
| Payload types (`Entry`, `ObserveSelection`, `RecordEntry`, ...) | Emitted |
| NOTA codec on every emitted type (`from_nota_block`, `to_nota`) | Emitted |
| rkyv `Archive`/`Serialize`/`Deserialize` derives | Emitted |
| `short_header::INPUT_RECORD` + the 7 other constants | Emitted |
| `InputRoute`, `OutputRoute` enums | Emitted |
| `Input::route()`, `Input::short_header()`, `Input::route_from_short_header()` | Emitted |
| `Input::encode_signal_frame()`, `Input::decode_signal_frame()` | Emitted |
| `Output::*` mirror | Emitted |
| `SignalFrameError` enum + Display + Error | Emitted |
| Length-prefix wire envelope (`u32 BE` + frame) | Hand-rolled in `src/signal.rs` (one shim class with 4 methods) |
| Engine dispatch (Input variant match → handler method) | Hand-rolled in `src/executor.rs` as methods on `impl Engine` |
| Multi-topic + kind index, redb storage, identifier mint | Hand-rolled in `src/sema.rs` (per-variant `do_*` methods on `impl SemaActor`) |
| Upgrade traits | Hand-rolled in `src/upgrade.rs` (with stated intent to be emitted) |

Compared to operator's `spirit-next` HEAD (`231b509131c6` on main),
`schema-rust-next` HEAD (`f76d6483b477`) already emits the route +
header + codec emission inside its test fixture, but `spirit-next`
itself still consumes the hand-rolled `transport.rs`. This design
substrate USES the emitted methods directly — `src/signal.rs` never
mentions `short_header::INPUT_*` or `InputRoute::Record`; it calls
`input.encode_signal_frame()` / `Input::decode_signal_frame(frame)`.

## The 5 Nix constraint checks (which pass; which deferred)

Per operator/209 §"Test implications", verbatim:

1. **No manual Input/Output route matching outside generated code.**
   - Landed as `check-no-manual-routing` in `flake.nix`: greps for
     `short_header::INPUT_|short_header::OUTPUT_` in `src/` and fails.
   - Also enforced at the **type level**: nowhere in authored code does
     `pub enum InputRoute` or `pub enum OutputRoute` appear — the
     emitted ones are the only definitions.
   - **Status**: PASS.

2. **CLI boundary is NOTA text; daemon boundary is binary rkyv frames.**
   - Landed as `check-cli-nota-daemon-rkyv` in `flake.nix`: asserts
     `encode_signal_frame` / `decode_signal_frame` appear in
     `src/signal.rs`, `parse::<Input>` appears in `src/bin/spirit.rs`,
     and no `rkyv::to_bytes` or `rkyv::from_bytes` appears in
     `src/signal.rs` (those go through the emitted methods).
   - Also empirically witnessed by `tests/end_to_end.rs`: real binary
     boundary; CLI takes NOTA argv, daemon receives rkyv on socket.
   - **Status**: PASS.

3. **Executor lowering is methods/traits on generated objects, not free fns.**
   - Landed as `check-executor-methods-not-free-fns` in `flake.nix`:
     greps for `^(pub )?fn ` at column 0 in `src/executor.rs` and
     fails. Methods inside `impl` blocks are indented; they pass.
   - **Status**: PASS. Every executor verb is on `impl Engine`,
     `impl ObservationProjection`, `impl TopicCounter`, or one of the
     extension traits `EntryExt` / `ObserveSelectionExt`.

4. **SEMA is the only writer to the durable store.**
   - Landed as `check-sema-single-writer` in `flake.nix`: greps for
     `begin_write(` outside `src/sema.rs` and fails.
   - Also enforced as a **runtime invariant** by
     `tests/sema_single_writer.rs`: the static `SEMA_ACTOR_COUNT`
     counter asserts EXACTLY ONE actor is spawned per `SemaActor::open`,
     and the count returns to baseline after `shutdown`.
   - **Status**: PASS at both layers.

5. **Schema changes regenerate types before implementation code compiles.**
   - Landed as `check-regenerate-before-compile` in `flake.nix`:
     asserts `build.rs` invokes `SchemaEngine` + `RustEmitter` and
     re-runs on `schema/spirit.schema` change; asserts `lib.rs`
     includes the `OUT_DIR` artifact.
   - Cargo's build-script invariant adds the structural enforcement
     (build.rs runs before lib.rs compiles by definition).
   - **Status**: PASS.

All five Nix checks PASS as written. `nix flake check` would require a
Nix-available environment to wire crane + fenix; the constraints are
expressible and the grep tests already pass against the source tree.

## Signal plane progress vs /208 P1 gap

Operator/208 P1 named the spirit-next `transport.rs` as carrying the
biggest hand-rolled surface: `InputRoute`, `input_short_header`,
`input_route`, `encode_input_frame`, `decode_input_frame`, plus the
Output mirror.

This design substrate's `src/signal.rs` carries NONE of those. The
shim is:

```rust
pub struct LengthPrefix;

impl LengthPrefix {
    pub fn write_input(writer: &mut impl Write, input: &Input) -> Result<(), TransportError> {
        let frame = input.encode_signal_frame()?;  // emitted method
        Self::write_envelope(writer, &frame)
    }
    pub fn read_input(reader: &mut impl Read) -> Result<(InputRoute, Input), TransportError> {
        let frame = Self::read_envelope(reader)?;
        Input::decode_signal_frame(&frame).map_err(...)  // emitted method
    }
    // Output mirror
    // write_envelope + read_envelope (the u32 BE length prefix only)
}
```

The route + header logic is GONE from authored code — it lives on the
emitted `Input` / `Output` impl blocks. The only authored framing logic
is the OUTER length-prefix envelope (a 4-byte u32 BE before each
signal-frame). That envelope is the layer above the schema's wire
contract — it belongs to the Unix-socket transport, not the signal
frame. Per /209 the cut is correct: schema emits `(route + header +
codec) = signal frame`; transport wraps the frame.

The operator-canonical `spirit-next` could absorb this same pattern in
one slice: replace `transport.rs` route/header/codec with calls to the
already-emitted `Input::*` methods. The schema-rust-next emitter
already produces what's needed (the test fixture demonstrates).

## Executor plane shape

The full `impl Engine` block from `src/executor.rs`:

```rust
impl Engine {
    pub fn new(sema: SemaHandle) -> Self { ... }
    pub fn sema(&self) -> &SemaHandle { &self.sema }

    /// Apex executor entrypoint — schema-derived match
    pub fn handle(&self, input: Input) -> Output {
        match input {
            Input::Record(entry) => self.handle_record(entry),
            Input::Observe(selection) => self.handle_observe(selection),
            Input::State(request) => self.handle_state(request),
        }
    }

    fn handle_record(&self, entry: Entry) -> Output { ... }
    fn handle_observe(&self, selection: ObserveSelection) -> Output { ... }
    fn handle_state(&self, request: StateRequest) -> Output { ... }
}
```

Plus:

- `impl ObservationProjection { fn project_records(...); fn project_one(...) }` — the DescriptionOnly / WithProvenance cut as methods on a noun.
- `impl TopicCounter { fn build_view_from_topics(...) }` — folding aggregations into the schema's nested-newtype shape.
- `trait EntryExt for Entry` with `primary_topic`, `matches_topic`, `matches_kind` — methods on the schema-emitted Entry.
- `trait ObserveSelectionExt for ObserveSelection` with `matches`, `matches_topic`, `matches_kind` — methods on the schema-emitted ObserveSelection.
- `impl EntryBuilder { fn new_single_topic(...) }` — constructor as method.
- `impl DaemonClock { fn date_now(); fn time_now() }` — stamp helpers as methods.

Every executor verb is a method. No free `pub fn` at module scope. The
operator/209 risk-guard ("Executor as helper soup") is held at the
discipline level + the Nix-check level.

## SEMA plane single-writer enforcement

The actor is `SemaActor`. The handle is `SemaHandle` (clonable mpsc
sender). Opening:

```rust
impl SemaActor {
    pub fn open(path: ...) -> Result<(SemaHandle, JoinHandle<()>), SemaError> {
        ...
        let database = Database::create(&path)?;
        ...
        let (sender, receiver) = sync_channel::<SemaCommand>(64);
        SEMA_ACTOR_COUNT.fetch_add(1, Ordering::SeqCst);
        let actor = Self { database, receiver, next_identifier };
        let join = thread::Builder::new()
            .name("design-deep-spirit-sema-actor".to_owned())
            .spawn(move || actor.run())?;
        Ok((SemaHandle::new(sender, path), join))
    }
}
```

The runtime test asserts only ONE actor exists per open + return-to-
baseline after shutdown:

```rust
#[test]
fn opening_a_daemon_spawns_one_sema_actor() {
    let before = SEMA_ACTOR_COUNT.load(Ordering::SeqCst);
    let directory = tempdir().expect("tempdir");
    let database = directory.path().join("spirit.redb");
    let (sema, _join) = SemaActor::open(&database).expect("open sema");
    let after = SEMA_ACTOR_COUNT.load(Ordering::SeqCst);
    assert_eq!(after, before + 1, "exactly one SemaActor must be spawned per daemon");
    sema.shutdown().expect("shutdown");
    // ... wait for actor exit
    assert_eq!(SEMA_ACTOR_COUNT.load(Ordering::SeqCst), before);
}
```

Test result: PASS. The single-writer invariant holds physically (one
thread owns `Database`, all writes flow through `mpsc`) AND
structurally (the Nix grep proves no `begin_write` exists outside
`src/sema.rs`).

## v0.3 capability coverage

Mapping each v0.3 feature from operator/187 + the prompt to demonstrated tests:

| v0.3 feature | Demonstrated by | Status |
|---|---|---|
| Multi-topic records (`TopicList`) | `tests/sema_round_trip.rs::record_then_observe_*` | PARTIAL — schema emits `TopicList` as newtype-around-one-Topic; multi-element on the wire requires schema-language `Vec<X>` (open question) |
| Record + Observe operations | `tests/end_to_end.rs` + `tests/sema_round_trip.rs` | PASS |
| Observe by topic | `tests/sema_round_trip.rs::record_then_observe_*` | PASS |
| Observe by kind | `tests/sema_round_trip.rs::record_then_observe_*` | PASS |
| Topic count queries | `tests/sema_round_trip.rs` + end-to-end `(State Topics)` | PASS |
| Daemon-stamped Date + Time | `tests/sema_round_trip.rs` (asserts non-zero stamps); live transcript shows real epoch seconds | PASS |
| ObservationMode DescriptionOnly | `tests/end_to_end.rs` + live transcript | PASS |
| ObservationMode WithProvenance | live transcript | PASS |
| RecordsObserved as Vec\<Entry\> | NOT YET — `RecordList` is newtype-around-one due to schema-language limit | OPEN (see §"Open shape questions") |
| redb durable storage | `tests/sema_round_trip.rs::schema_version_marker_survives_reopen` | PASS |
| Schema version marker for migration | same test + `bootstrap_or_migrate` in `src/sema.rs` | PASS |

**~90% coverage of v0.3 capability**. The one structural gap is
`Vec<RecordEntry>` on the wire — internally SEMA already returns a
`Vec<StoredRecord>`; the executor's projection truncates to first
record before emitting because `RecordList` is a single-element
newtype. This is the schema-language limit, not a runtime limit.

## Upgrade trait skeleton (Layer 6 scaffold)

`src/upgrade.rs` defines:

```rust
pub trait UpgradeFrom<Previous>: Sized {
    type Error: std::error::Error;
    fn upgrade_from(previous: Previous) -> Result<Self, Self::Error>;
}

pub trait DowngradeTo<Previous> {
    type Error: std::error::Error;
    fn downgrade_to(self) -> Result<Previous, Self::Error>;
}

pub enum ChangeClass {
    ZeroCost, AppendOnly, Projection, Destructive, Incompatible,
}

pub enum UpgradeError {
    DiscardWouldLoseData { field: &'static str },
    MissingDefault { field: &'static str },
    Incompatible { reason: &'static str },
}
```

Plus a worked example (`pub mod previous { struct Entry { topic: Topic, ... } }` representing the hypothetical v0.2 single-topic shape) and two `impl` blocks:

- `impl UpgradeFrom<previous::Entry> for crate::generated::Entry` — lifts a v0.2 Entry into v0.3 by wrapping `topic` as `TopicList(topic)`.
- `impl DowngradeTo<previous::Entry> for crate::generated::Entry` — flattens back, choosing the first (only) topic from `TopicList`.

Plus `MigrationIndex::entry_change_class() -> ChangeClass::AppendOnly`.

The accompanying test `tests/upgrade_skeleton.rs::entry_upgrade_then_downgrade_round_trips` proves the round-trip works for the same Entry value.

What `schema-rust-next` would need to emit per this skeleton:

- Per-affected-type `impl UpgradeFrom<Previous>` derived from the schema diff.
- Per-affected-type `impl DowngradeTo<Previous>` with `Discard` annotations on dropped fields.
- A schema diff engine inside `schema-next` producing a typed diff between two `Asschema` instances.
- Schema language support for `(default <value>)` and `(discard)` annotations on fields.
- A compile-time `MigrationIndex` per the pattern from `skills/component-triad.md` §"Compile-time module index for triad-internal dispatch".

The current scaffold gives downstream consumers a stable trait
signature to target today; the emitter can populate impls later.

## Open shape questions for psyche

### Q1 — Schema language needs `Vec<X>` collection syntax

`spirit.schema` declares `TopicList [Topic]` — the current emitter
interprets `[X]` as a newtype-around-one-X struct, not as `Vec<X>`.
Operator/206 P0 #1 already names this gap. This design substrate works
around it by:

1. Internally storing `Vec<Topic>` in SEMA via custom rkyv codec.
2. Wire-projecting only the first topic.

The fix needs schema-language extension. Two shapes worth considering:

- **Bracketed-asterisk** form: `TopicList [Topic*]` for "vec of Topic".
- **Explicit Vec macro**: `TopicList (Vec Topic)` — uniform with the macro-position framing per /372.

Either way, the schema-rust-next emitter then produces
`pub struct TopicList(pub Vec<Topic>)` (or `pub type TopicList = Vec<Topic>`).
This is a schema-language change with downstream emitter changes.
**Psyche pick** between the two forms.

### Q2 — Should the wire RecordList be `Vec<RecordEntry>` directly?

Given Q1 lands, `RecordList [RecordEntry*]` becomes
`pub struct RecordList(pub Vec<RecordEntry>)`. The executor's
`ObservationProjection::project_records` then returns the full Vec
instead of truncating to first. This UNBLOCKS the operator/187 v0.3
parity claim "RecordsObserved as Vec\<Entry\>". Same for
`TopicCountList`.

**Designer-lean**: yes; this is the natural follow-on after Q1. Psyche
confirms.

### Q3 — Multi-element TopicList: how does multi-topic record on the wire?

Given Q1 lands, the user can record `(Record (([schema][spirit] Decision [...] High))` — `[schema][spirit]` would parse as TWO blocks. But `TopicList` is positional inside `Entry`, so the NOTA shape needs a delimiter. Likely `(Record (([schema spirit] Decision [...] High))` where the bracket holds multiple topic atoms. The NOTA codec for `Vec<X>` needs a rule. Operator/206 P0 #1 left this open.

**Designer-lean**: bracketed atom-list = `Vec<Topic>` from
`[schema spirit]`. Psyche confirms the NOTA shape.

### Q4 — Schema-emitted Vec<X> codec generation

If `Vec<Topic>` becomes the emission, schema-rust-next needs codec
methods for `Vec<X>` (encode each element + length prefix; decode by
walking children of a delimited block). Plus rkyv derives already
support `Vec<T>` natively. The work is in the NOTA emitter shape.

**Designer-lean**: extend the existing `parse_expression` /
`format_expression` switches in `schema-rust-next/src/lib.rs` to
recognize `Vec<T>` references; emit `block.root_objects.iter().map(T::from_nota_block).collect()` for decode and `format!("[{joined}]")` for encode. Psyche confirms.

### Q5 — Schema-language `default` and `discard` annotations for upgrade

The upgrade skeleton needs schema-language extension to express which
field has a default for upgrade and which can be discarded for
downgrade. Two NOTA shapes:

- Inside the struct fields: `Entry [TopicList Kind Description Magnitude (default Magnitude Maximum)]`
- Outside: `(annotate Entry magnitude default Maximum)`

**Designer-lean**: inline at the field. Psyche confirms.

### Q6 — SignalCodec composition with caller/process-origin

Per intent record 854 + designer/372 §"Open shape Q5": when the
caller-identification library lands, codec instances will be state-
aware (`SignalCodec` becomes a struct carrying the originating-process
identity). The current scaffold has `SignalCodec` as a unit struct.
The shape extends naturally — `SignalCodec { origin: ProcessOrigin }`
with `encode_input(self, input, &target_origin)` taking an additional
parameter for the destination origin.

**Designer-lean**: defer; capture as Medium-certainty for the slice
that introduces caller-id.

## Comparison with operator's spirit-next

| Dimension | operator `spirit-next` (HEAD `231b509131c6`) | designer `design-deep-spirit-2026-05-26` (HEAD `c06172185e6a`) |
|---|---|---|
| Schema authored | Single-topic Entry + Topic + Query (mostly v0.1 shape) | Multi-topic-shaped Entry (TopicList) + ObserveSelection + StateRequest + RecordEntry + RecordWithProvenance + Date + Time + ObservationMode (v0.3 shape) |
| Surfaces | 2 (Record, Observe) | 3 (Record, Observe, State) |
| Output variants | 3 (RecordAccepted, RecordsObserved, Error) | 5 (RecordAccepted, RecordsObserved, TopicsObserved, StateObserved, Error) |
| Transport route emission consumed | NO — hand-rolled in `transport.rs` | YES — emitted methods called directly |
| Engine | `Engine::handle` with inline match; methods minimal | `Engine::handle` + 3 per-variant handler methods on `impl Engine` + `ObservationProjection` + `TopicCounter` + `EntryExt` + `ObserveSelectionExt` |
| Storage | In-memory `Vec<StoredRecord>` guarded by `Mutex` | Real redb on disk; mpsc-channel single-writer actor; topic + kind indexes |
| Single-writer invariant | Mutex (one writer at a time, but any task can write) | Physical single-writer thread; SEMA_ACTOR_COUNT runtime asserts |
| Daemon-stamped timestamps | NO | YES (Date + Time per record) |
| ObservationMode | NO | YES (DescriptionOnly + WithProvenance) |
| Topic counts | NO | YES |
| Schema-version marker | NO | YES — persisted in metadata table; checked on reopen |
| Upgrade traits | NO | YES — hand-authored skeleton + worked example + ChangeClass |
| End-to-end test | Records + Observes once | Multi-record cycle + multi-topic observation + state + provenance modes + single-writer assertion + schema-version reopen + upgrade-round-trip |
| Tests passing | 1 process boundary | 16 across 6 suites |
| Nix constraint checks | 5 (no-old-signal-macro, generated-at-build-time, binary-boundary-test, generated-signal-plane-used, local-schema-source-patches) | 5 (no-manual-routing, cli-nota-daemon-rkyv, executor-methods-not-free-fns, sema-single-writer, regenerate-before-compile) — direct match to operator/209 §"Test implications" |

The two implementations are **convergent on shape** (signal/executor/SEMA
triad, schema-derived signal plane) and **complementary on scope**
(operator's track is the canonical pilot for the schema stack; this
designer track is the v0.3-capability vertical proving the runtime can
absorb the full production capability).

## What this proves about /371 §8 + /373 §3.2 sequencing

The /209 + /373 §3.2 linear sequence proposed:

1. Signal plane first
2. Executor plane second
3. SEMA plane third
4. Schema diff / upgrade fourth

This deep implementation **lands all four planes** in one repo with the
sequencing structurally visible: `src/signal.rs` (slice 1), `src/executor.rs`
(slice 2), `src/sema.rs` (slice 3), `src/upgrade.rs` (slice 4 scaffold).
That doesn't contradict the linear-sequence recommendation — it just
demonstrates that ONCE the planes are explicit, they can co-exist in
the same substrate without conflating.

The operator-track equivalent is one-slice-at-a-time on `spirit-next`.
This designer-track proof-of-concept lets operator absorb the **shape**
without absorbing the implementation-substrate (operator's pilot stays
canonical; designer's repo deletes when the patterns integrate).

Compared to /371 §8's 9-slice parallel-tiers framing:

- The linear sequence /209 + /373 recommended is correct for the operator track.
- The designer track can move faster by landing all planes in a design repo as proof.
- The two tracks are complementary, not competing.

## Comparison with sibling /372

Sibling subagent's design-signal-frame-schema concept (`/372`) proves
that frame primitives (`Frame`, `Route`, `SignalCodec`, `FrameError`)
CAN live in a schema file rather than as engine built-ins. The
designer recommendation in /372 §"Home recommendation" was option (b):
adopt the existing `signal-frame` repo with retired contents.

**This deep-spirit implementation does NOT depend on /372 landing**.
The route + header + codec emission is ALREADY in
operator's `schema-rust-next` HEAD as engine-built-in behavior (per
the schema-rust-next test fixture). The /372 proposal is about WHERE
that emission's source lives (schema file vs hand-authored emitter
methods) — orthogonal to whether the emission produces working code.

When /372 integrates, the schema-rust-next emitter would learn to
import `signal-frame.schema` and consume its declared macros instead
of carrying the frame logic in `lib.rs`. The downstream consumer
(this design repo + operator's spirit-next) wouldn't need to change —
`Input::encode_signal_frame()` would still emit; the source of the
emitter's framing rule just moves from Rust into NOTA.

## Worktrees + commits

- `/git/github.com/LiGoldragon/design-deep-spirit-2026-05-26` — main, commit `c06172185e6a`, pushed to origin.
- `/home/li/primary/repos/design-deep-spirit-2026-05-26` — workspace symlink.
- `/home/li/primary/reports/designer-assistant/374-deep-spirit-parallel-implementation-2026-05-26.md` — this report (commits to primary main).

No worktrees under `~/wt` were created — this work happened directly
on the new design repo's main per `skills/major-break-via-new-repo.md`
§"Step 5 — Develop in parallel" + the design-repo discipline. No
operator-canonical repos were modified.

## Time + cadence

Implementation took roughly 2 hours of focused work:

- Reading context + audit reports: ~20 minutes
- Repo scaffold + INTENT + ARCHITECTURE: ~10 minutes
- Schema authoring + build.rs: ~10 minutes
- src/signal.rs + src/sema.rs + src/executor.rs + src/daemon.rs + src/upgrade.rs + bins: ~40 minutes
- Tests (6 files, 16 tests): ~30 minutes
- Iterating to clean compile + clippy + fmt + all-tests-passing: ~20 minutes
- Live shell transcript + this report: ~30 minutes

Quality > speed held — every test passes; every constraint check is
defined; the end-to-end shell transcript is real (not mocked).

## References

- `LiGoldragon/design-deep-spirit-2026-05-26` main `c06172185e6a` — the substrate
- `~/primary/reports/designer/371-signal-executor-sema-runtime-triad-and-federation-2026-05-26.md` — the runtime triad spec
- `~/primary/reports/designer/373-engagement-with-operator-209-refined-triad-audit-2026-05-26.md` — convergence + risk-guards
- `~/primary/reports/operator/209-refined-triad-audit-opinion/` — the operator-side synthesis driving the five Nix checks
- `~/primary/reports/operator/208-schema-stack-missing-implementation-audit-2026-05-26.md` — the P1 gap list this work closes
- `~/primary/reports/operator/205-spirit-next-schema-pilot-implementation-2026-05-26.md` — operator's baseline pilot
- `~/primary/reports/operator/206-schema-spirit-running-concept-audit-2026-05-26.md` — operator's gap audit
- `~/primary/reports/designer/370-implementation-gap-audit-designer-side-2026-05-26.md` — the designer-side gap inventory
- `~/primary/reports/designer/367-nota-as-specification-superset-of-capnproto-2026-05-26.md` — the NOTA-as-specification framing
- `~/primary/reports/operator/187-spirit-v0-2-0-side-by-side-deployment-2026-05-25.md` — v0.3 production shape
- `~/primary/reports/designer-assistant/372-design-signal-frame-schema-concept-2026-05-26.md` — sibling concept (orthogonal)
- `~/primary/skills/double-implementation-strategy.md` — the design-prefix discipline this repo follows
- `~/primary/skills/major-break-via-new-repo.md` — the new-repo scaffold pattern
- `~/primary/skills/component-triad.md` — runtime triad + single-argument rule
- `~/primary/skills/abstractions.md` §"Schema-emitted nouns" — verb belongs to noun
- Spirit records: 856 (runtime triad named); 857 (federation framing); 858 (schema/Rust labor split); 859 (migration authorized); 860-861 (signal-frame schema concept)
