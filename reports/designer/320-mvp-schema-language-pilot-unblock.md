*Kind: Design · Topic: mvp-schema-language-pilot · Date: 2026-05-24*

# 320 — MVP design: unblock schema-language signal+sema macros, header generation, Spirit pilot

**Status:** operator-ready. Pilot bead spec at `§4`. Closed
decisions at `§2` carry "possibly needs review" markers per
psyche directive — operator inlines those markers into the code
they land.

## §1 Blockers identified

To get the new schema-language-based Signal+Sema into macros with
header generation in production, **13 design holes** need to close.
This report closes all 13 with reasoned decisions; alternatives
preserved in `§2` for later review.

### §1.1 The eight from `/164 §9`

1. Engine-routing annotation shape (Shape A explicit vs Shape B
   naming-convention).
2. Single-variant data-carrying enum — emit Rust struct or enum.
3. Schema file location (`<repo>/schema.nota` vs `<repo>/src/`).
4. Built-in primitive set.
5. Stream relation declaration shape.
6. Channel-section (golden-ratio split) assignment.
7. Path-ref security + sandbox.
8. Migration mode (dual-input vs new macro).

### §1.2 The three from spirit 388-392 (short-header structure)

9. Sub-byte packing — defer to post-MVP per spirit 392.
10. Root-vs-sub-enum relationship in the 8-enum 64-bit layout —
    interpretation (B) hierarchical-positional (byte 0 = root,
    bytes 1-7 = sub-enums in parallel) per `/305-v2` ratified
    framing.
11. ShortHeader projection method name (`short_header() -> u64`
    confirmed by operator's 2cjv landing in `signal-frame/src/
    frame.rs:110`).

### §1.3 The two from the 2cjv-to-macro gap

12. Where does the `LogVariant` trait declaration live (signal-
    frame crate root vs separate `signal-log-variant` crate).
13. Sema-side `LogVariant` trait shape — same trait reused, or a
    parallel `SemaLogVariant` trait.

## §2 Closed decisions — operator code-comment template

Each operator commit MUST inline the corresponding marker as a
code comment near the impacted code:

```rust
// DESIGN-DECISION-REVIEW (designer/320 §2.N): <one-line rationale>.
//   Alternative: <briefly>. Revisit if <trigger>.
```

The marker makes the decision findable + revisitable. Format
matches the existing workspace pattern for `// XXX:` /
`// TODO:` annotations.

### §2.1 Engine-routing annotation — Shape A (explicit)

**Decision:** Use `(engine <kind>)` annotation in NOTA schema per
`/164 §5.2` Shape A. Variant payload position carries the engine
routing as part of the schema:

```nota
(Record (Entry (engine assert)))
```

**Marker:** `// DESIGN-DECISION-REVIEW (designer/320 §2.1):
explicit (engine X) annotation. Alternative: Shape B
naming-convention. Revisit if schemas grow many operations with
predictable routing.`

**Rationale:** Schema as source-of-truth benefits from explicit
decisions; naming conventions hide information in vocabulary
choice + renaming a verb would change its lowering.

### §2.2 Single-variant data-carrying enum — emit Rust struct

**Decision:** When the schema declares `(Entry (Entry topic
Topic kind Kind …))` — a single-variant data-carrying enum —
the macro emits a Rust `struct Entry { topic: Topic, kind: Kind,
… }` rather than `enum Entry { Entry { … } }`.

**Marker:** `// DESIGN-DECISION-REVIEW (designer/320 §2.2):
single-variant collapse to Rust struct. Alternative: emit enum
with one variant. Revisit if struct/enum ambiguity affects
codegen downstream.`

**Rationale:** Same NOTA wire shape; `entry.topic` reads more
naturally than match destructuring; matches existing
hand-written daemon code shape.

### §2.3 Schema file location — `<repo>/schema.nota`

**Decision:** Schema file lives at the repo root,
`<repo>/schema.nota`. One file per contract crate. Build script
(or macro invocation) reads from `CARGO_MANIFEST_DIR/schema.nota`.

**Marker:** `// DESIGN-DECISION-REVIEW (designer/320 §2.3):
schema.nota at repo root, not src/. Alternative: src/schema.nota.
Revisit if Cargo.toml manifest discovery becomes complicated.`

**Rationale:** Schemas are workspace-shared artifacts; living at
repo root makes them findable + matches the rhythm of README.md
+ Cargo.toml + ARCHITECTURE.md at repo root.

### §2.4 Built-in primitive set — minimal

**Decision:** Built-in primitives the schema can reference but
not declare:

| Primitive | NOTA | Rust |
|---|---|---|
| `String` | `[text]` bracket string or bare camelCase/kebab-case ident | `String` |
| `u8`, `u16`, `u32`, `u64` | decimal | fixed-width unsigned |
| `bool` | `True` / `False` | `bool` |
| `Date` | `YYYY-MM-DD` | three-field |
| `Time` | `HH:MM:SS` | three-field |
| `Bytes` | `#hex…` | `Vec<u8>` |

Multi-line text uses block-string form `[|...text...|]` per
`nota/example.nota`. Path-refs in the schema (per §2.7) are
bracket strings: `(Magnitude [../signal-sema/magnitude.schema.nota])`.
The legacy `"..."` quote form is being retired per
`primary-36iq` and should not appear in new NOTA authoring.

Plus two containers: `[Vec T]`, `[Option T]`.

**NOT included for MVP:** `i8-i64`, `f32`, `f64`, `char`,
`HashMap`, custom container types.

**Marker:** `// DESIGN-DECISION-REVIEW (designer/320 §2.4):
minimal primitive set. Alternative: include signed ints + floats
+ char. Revisit if a concrete consumer needs them.`

**Rationale:** Workspace usage today is unsigned-only + bool +
String + Date + Time + Bytes + Vec + Option. Add others when a
concrete consumer arrives.

### §2.5 Stream relation — `belongs <StreamName>` annotation

**Decision:** Event variants annotate their stream membership
inline:

```nota
(Event
  (StateChanged (StateChanged belongs DomainStream))
  (RecordCaptured (RecordCaptured belongs DomainStream)))
```

The macro walks the Event enum, collects `belongs` annotations,
and synthesizes the stream relation. No separate root-vector
entry for `stream`.

**Marker:** `// DESIGN-DECISION-REVIEW (designer/320 §2.5):
belongs annotation on event variants. Alternative: separate
stream block in root vector. Revisit if stream relations grow
multi-event complexity not expressible inline.`

### §2.6 Channel-section assignment — implicit by crate identity

**Decision:** `signal-X` crates are always big-section
(`NamespaceSection::Big`); `owner-signal-X` crates are always
small-section (`NamespaceSection::Small`). No per-schema
declaration needed; macro reads `CARGO_PKG_NAME` to infer (per
`/307 §3.1` already-landed default).

**Marker:** `// DESIGN-DECISION-REVIEW (designer/320 §2.6):
implicit section by crate prefix. Alternative: explicit
(section X) declaration in schema. Revisit if a contract needs
non-default section assignment.`

### §2.7 Path-ref security — restricted resolution

**Decision:** Path-refs in NOTA schema resolve only to:
- (a) Sibling files in the same crate's schema directory
  (rooted at `CARGO_MANIFEST_DIR/`).
- (b) Cargo-dep crates via symbolic-ref form
  (`signal-sema:Magnitude`) resolved through Cargo dep graph.

**Rejected paths:** absolute paths, `../` traversal beyond the
crate root, `~/`, `/`. Reader rejects with explicit error.

**Marker:** `// DESIGN-DECISION-REVIEW (designer/320 §2.7):
sandboxed path-ref resolution. Alternative: arbitrary file
system traversal. Revisit if cross-crate symbolic refs prove
too restrictive for a legitimate use case.`

### §2.8 Migration mode — dual input

**Decision:** Macro `signal_channel!` accepts BOTH inputs:
- Today: Rust-syntax with keywords (`channel`, `operation`,
  `reply`, etc.)
- New: NOTA-data input starting with `[`

Macro detects: if the first token is `[`, parse as NOTA-data;
otherwise parse as Rust-syntax. Both produce the same Rust
output.

**Marker:** `// DESIGN-DECISION-REVIEW (designer/320 §2.8):
dual input mode. Alternative: separate macro nota_signal_channel!.
Revisit if dual parsing complicates macro internals.`

### §2.9 Sub-byte packing — defer post-MVP per spirit 392

**Decision:** MVP short-header structure is 1 root enum + 7
sub-enums × 8 bits each = 64 bits. No sub-byte packing. Spirit
389's bool-1bit / 16-variant-4bit / multi-byte options DEFER to
post-MVP work.

**Marker:** `// DESIGN-DECISION-REVIEW (designer/320 §2.9):
even-byte sub-enum split for MVP per spirit 392. Sub-byte packing
deferred. Revisit when concrete need for packing surfaces and
upgrade mechanism can carry the cutover.`

### §2.10 Root-vs-sub-enum relationship — hierarchical-positional

**Decision:** Per ratified `/305-v2` framing: byte 0 = root enum
variant discriminator; bytes 1-7 = sub-enum slot discriminators
in PARALLEL. All 8 enums populate simultaneously per message.
NOT tagged-union; NOT per-root-variant-layout.

**Marker:** `// DESIGN-DECISION-REVIEW (designer/320 §2.10):
hierarchical-positional 8-enum layout. Alternative: tagged-union
or per-root-variant-layout. Revisit if a channel's natural shape
fights the parallel-slot model.`

### §2.11 ShortHeader projection method — `short_header() -> u64` (already landed)

**Decision:** Operator's 2cjv landing chose `short_header()`
returning `ShortHeader(u64)` newtype per `signal-frame/src/
frame.rs:110`. Confirmed canonical.

**Marker:** N/A — already landed; comment in 2cjv code.

### §2.12 `LogVariant` trait location — `signal-frame` crate root

**Decision:** `LogVariant` trait declared in `signal-frame/src/
log_variant.rs`, re-exported from crate root. Single source of
truth.

**Marker:** `// DESIGN-DECISION-REVIEW (designer/320 §2.12):
LogVariant trait in signal-frame crate root. Alternative:
separate signal-log-variant crate. Revisit if the trait grows
many impls that don't naturally live with signal-frame.`

**Trait shape:**

```rust
pub trait LogVariant {
    /// Pack this value's discriminator state into the 64-bit
    /// short-header layout. Byte 0 = root verb; bytes 1-7 = sub-
    /// enum slot discriminators in parallel.
    fn log_variant(&self) -> u64;
}
```

### §2.13 Sema-side trait — reuse `LogVariant`, distinguish by callsite

**Decision:** Sema-side does NOT need a separate `SemaLogVariant`
trait. Same `LogVariant` trait works; the sema-side enum
(`SemaOperation`) implements it; the macro emits the impl from
the schema's `(engine X)` annotations.

The two headers (signal-side + sema-side) are distinguished by
WHICH enum's `log_variant()` is called, not by the trait. The
caller knows the context.

**Marker:** `// DESIGN-DECISION-REVIEW (designer/320 §2.13):
reuse LogVariant for sema-side. Alternative: parallel
SemaLogVariant trait. Revisit if signal-side and sema-side
header layouts diverge meaningfully.`

## §3 MVP scope — end-to-end Spirit pilot

The pilot delivers the schema-language-based macro emission for
Spirit, end-to-end: schema file → macro emission → Frame's
ShortHeader populated → tap observer sees correct headers.

### §3.1 What lands

**(A) NOTA schema reader** (~200 LoC in
`signal-frame-macros/src/schema_reader.rs`):
- Parses NOTA-data input into structured `ChannelSpec` model.
- Resolves path-refs per §2.7 (sandboxed).
- Validates root-type per §3.4.

**(B) NOTA-data input arm in `signal_channel!`** (~100 LoC in
`signal-frame-macros/src/lib.rs` + `parse.rs`):
- Detects NOTA-data input by first-token check (`[`).
- Falls through to existing Rust-syntax parser otherwise.
- Both paths produce the same `ChannelSpec` for the existing
  `emit::emit(&spec)`.

**(C) `LogVariant` trait declaration** (~10 LoC in
`signal-frame/src/log_variant.rs`):
- Per §2.12.
- Re-exported from `signal-frame/src/lib.rs`.

**(D) Per-channel `LogVariant` autogen emission** (~150 LoC in
`signal-frame-macros/src/emit.rs`):
- Walks the request enum + sub-enums per §2.10.
- Emits `impl LogVariant for <Operation>` that packs byte 0 =
  variant discriminator + bytes 1-7 = sub-enum slot discriminators.
- For MVP per §2.9: each sub-enum gets one byte; no bit-packing.

**(E) Frame `short_header` populator** (~50 LoC in
`signal-frame-macros/src/emit.rs`):
- Emit `into_frame()` constructor that calls
  `LogVariant::log_variant()` on the payload and passes the result
  to `Frame::with_short_header()` (already landed per 2cjv).

**(F) Sema-side `LogVariant` impl** (~100 LoC in
`signal-sema/src/operation.rs`):
- Manual impl on `SemaOperation` packing the 6-variant discriminator
  at byte 0; bytes 1-7 reserved zero for MVP.
- Future: extend to outcome + component-tag + per spirit 390.

**(G) Spirit schema file** (~70 LoC at
`signal-persona-spirit/schema.nota`):
- Full Spirit channel per `/164 §6.1`.
- Includes engine annotations per §2.1.

**(H) Witness tests** (~200 LoC in
`signal-persona-spirit/tests/short_header.rs`):
- Round-trip: build a `Record` operation, encode to frame,
  decode, verify `short_header()` returns the expected u64.
- Tap-anywhere: subscribe a test observer to spirit's
  short-header stream, fire a `Record` op, verify the observer
  receives the expected header.

### §3.2 What does NOT land in MVP

**Deferred to post-MVP per spirit 392 + this report:**
- Sub-byte packing optimization (spirit 389 → defer per 392).
- Schema component daemon (spirit 397 → defer; library suffices).
- Full sema-side bytes-1-7 layout (MVP zeroes them).
- Recursive Help emission (per `/312`; tracked as `primary-8r1j`
  under `primary-ezqx`).
- Next-as-dep `VersionProjection` emission (per spirit 366;
  tracked as `primary-ezqx` Slot 6).
- Mass workspace cutover from Rust-syntax to NOTA-data input
  (Spirit pilot only; other components migrate per their own
  schedule).

**Out of scope per `/164 §10`:**
- Daemon runtime details (actor topology, socket binding).
- Authorization policy.
- Performance tuning.
- NOTA-projection policy.

### §3.3 Backwards compatibility

Per §2.8 dual-input mode: existing Rust-syntax `signal_channel!`
invocations across the workspace KEEP WORKING during the
transition. Only Spirit's `signal-persona-spirit/src/lib.rs`
switches to the NOTA-data input form for the pilot.

The MVP does NOT migrate other components' contracts. Mind,
router, message, etc. stay on Rust-syntax until their own
cutover beads land.

### §3.4 Root-type validation

Per psyche: "with a check on the data type of the root."

The validator (in `signal-frame-macros/src/validate.rs` extension
arm for NOTA-data input) enforces:

- Root vector contains exactly the channel's required enums
  (`Operation`, `Reply`, optional `Event` if the channel is
  streaming).
- Each root enum's variants either reference declared enums or
  built-in primitives (per §2.4).
- Every variant payload type resolves (declared in the same
  schema OR reachable via path-ref per §2.7).
- Engine annotations (per §2.1) are valid (one of: `assert`,
  `mutate`, `retract`, `match`, `subscribe`, `validate`).
- No cycles in the path-ref graph.
- No duplicate enum names.
- Stream `belongs` annotations reference declared streams.

Validation failures produce span-pointed compile errors so the
operator sees the line + column in the schema file.

## §4 Operator bead spec — pilot test

**Bead title:** `MVP schema-language pilot — Spirit through
NOTA-data macro input + ShortHeader emission + tap test`

**Bead body:**

```text
Land the MVP for the NOTA schema-language-based signal_channel!
macro, piloted on Spirit. End-to-end: schema file → macro emits
Layer 1 + ShortHeader projection → Frame populates short_header
on every wire message → tap observer receives the headers.

Acceptance: one Spirit Record operation goes through the full
path and produces the expected short_header u64 visible at a
tap-attached observer.

Reference: reports/designer/320-mvp-schema-language-pilot-unblock.md
for the full design + closed decisions (with code-comment markers
to inline at each landing site).

Sub-tasks (sequence):

1. Add LogVariant trait at signal-frame/src/log_variant.rs
   (per §2.12 + §3.1.C). Re-export from crate root. Inline
   the §2.12 marker.

2. Add NOTA schema reader at signal-frame-macros/src/schema_reader.rs
   (per §3.1.A). Path-ref sandboxing per §2.7 (inline marker).

3. Extend signal-frame-macros/src/parse.rs with NOTA-data input
   detection (per §2.8 + §3.1.B). Inline §2.8 marker.

4. Extend signal-frame-macros/src/validate.rs with root-type
   validation (per §3.4).

5. Add LogVariant autogen emission to signal-frame-macros/src/emit.rs
   (per §3.1.D). Per-channel emit walks the request enum + sub-enums
   per §2.10 (inline marker). MVP even-byte split per §2.9 (inline
   marker).

6. Add Frame short_header populator to emit.rs (per §3.1.E).
   Constructor calls LogVariant::log_variant() and passes to
   Frame::with_short_header() (already landed per 2cjv).

7. Add manual LogVariant impl on SemaOperation in
   signal-sema/src/operation.rs (per §3.1.F + §2.13 — inline
   marker). MVP: byte 0 = discriminator; bytes 1-7 = 0.

8. Add Spirit schema file at signal-persona-spirit/schema.nota
   (per §3.1.G; full schema in /164 §6.1).

9. Migrate signal-persona-spirit/src/lib.rs to use NOTA-data
   input form (replace the existing Rust-syntax signal_channel!
   invocation with the NOTA-data form that points at schema.nota).
   Single-variant collapse per §2.2 (inline marker).

10. Add witness tests at signal-persona-spirit/tests/short_header.rs
    (per §3.1.H):
    (a) Round-trip: encode Record(Entry{...}) → frame bytes →
        decode → assert short_header() == expected.
    (b) Tap-anywhere: subscribe test observer to spirit's
        short-header tap stream; fire Record op; assert observer
        receives the expected header.

Verification: cargo fmt + CARGO_BUILD_JOBS=2 cargo test + nix
flake check --option max-jobs 0 — all passing across signal-frame,
signal-frame-macros, signal-sema, signal-persona-spirit.

Constraint: every closed decision marker per /320 §2 MUST be
inlined in the corresponding code as a // DESIGN-DECISION-REVIEW
comment. Operator does NOT relitigate the decisions; they land
per /320 + flag the marker for future review.

Dependencies: primary-2cjv CLOSED (Frame.short_header field
exists per signal-frame/src/frame.rs:87-94).

Parent epic: primary-ezqx (macro convergence). This bead is the
MVP foundation that primary-ezqx Slots 1-6 build on once the
NOTA-data input arm is in place.
```

## §5 Pilot test plan — what designer reviews

When operator delivers, designer reviews:

| Check | Acceptance |
|---|---|
| LogVariant trait shape | Matches §2.12 signature; re-exported from `signal-frame` |
| NOTA schema reader | Resolves path-refs sandboxed per §2.7; rejects out-of-sandbox refs with clear error |
| Validate pass | Root-type check per §3.4; engine annotations validated; cycle detection works |
| Macro NOTA-data arm | Detects `[` first token; falls through cleanly to Rust-syntax otherwise |
| `LogVariant` autogen | Emits byte 0 = root variant discriminator; bytes 1-7 = sub-enum slot discriminators in parallel per §2.10 |
| Sema-side impl | `SemaOperation::log_variant()` packs byte 0 correctly; bytes 1-7 zero (MVP) |
| Schema file | Spirit schema matches `/164 §6.1`; engine annotations Shape A per §2.1 |
| Spirit `lib.rs` migration | NOTA-data form replaces Rust-syntax; existing tests still pass |
| Round-trip test | Asserts the expected u64 layout |
| Tap test | Observer receives the header for a fired Record op |
| **Markers inlined** | Every §2 marker present in the corresponding code site |

Designer review = read the diff against `/320 §2-§4` checklist;
flag any unmarked decisions or deviation from the closed shapes;
sign off if clean.

If operator hits a blocker — a closed decision proves wrong, the
NOTA reader hits a corner I didn't anticipate, the Frame
short_header populator conflicts with 2cjv's shape — operator
flags via bd comment. Designer responds with revised decision +
updated marker. The revision lands as `/320 §2.N (revised)` so
the trail is visible.

## §6 What this design does NOT cover

- **Schema-language v3 grammar finalization** — `/164` is the
  forward grammar; this report consumes its v3 form. Grammar
  changes go through `/164`.
- **Schema component daemon** — spirit 397-400 named the runtime
  registry; MVP uses the library face only. Daemon is a separate
  bead post-MVP.
- **Sema-side header bytes 1-7** — MVP zeroes them. Full sema-
  side layout depends on which sema sub-classifications matter;
  defer until concrete need.
- **Mass workspace cutover** — Spirit pilot only; other components
  migrate per their own beads.
- **`primary-ezqx` slot work** — slots 1-6 land in parallel; this
  MVP unblocks them by providing the NOTA-data input substrate
  they consume.

## §7 See also

- `reports/second-designer/164-nota-schema-language-vector-of-root-verb-enums-2026-05-24.md`
  — schema-language v3 grammar (psyche-ratified, `§9` open
  questions all closed in this report's §2)
- `reports/designer/305-v2-design-64bit-signal-per-component-namespacing.md`
  — per-component namespacing model the §2.10 decision follows
  (STATUS-BANNERed per `/319` sweep)
- `reports/designer/307-design-golden-ratio-namespace-split.md`
  — golden-ratio section model the §2.6 decision applies
- `reports/designer/308-design-pretyped-envelope-and-tap-anywhere.md`
  — envelope reshape + tap discipline (the 2cjv landing
  implements this)
- `reports/designer/312-design-recursive-help-on-every-enum.md`
  — Help-on-every-enum (out of MVP scope; tracked separately)
- `reports/designer/317-sema-upgrade-and-macro-convergence-audit/4-overview.md`
  — macro convergence epic context
- `reports/designer/319-schema-stack-context-maintenance-sweep/4-overview-and-retirement-list.md`
  — designer-lane current state
- `signal-frame/src/frame.rs:20-200` — 2cjv landed code
  (ShortHeader newtype + Frame fields + peek helpers)
- `signal-frame/src/log_variant.rs` (NEW per this MVP) —
  trait declaration target
- `signal-frame-macros/src/schema_reader.rs` (NEW per this MVP)
  — NOTA schema reader target
- `signal-persona-spirit/schema.nota` (NEW per this MVP) — pilot
  schema file
- Spirit records 388 (short header canonical name), 390 (sema
  symmetric header), 391 (NOTA schema language), 392 (MVP
  even-byte scope), 393-396 (vector of root-verb enums + path-refs
  + macro emits all three layers), 397-400 (schema component
  Principle/Clarifications, post-MVP)
