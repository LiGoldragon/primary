# Sub-agent 4 — Data and storage compatibility — 2026-06-02

Role: system-designer (sub-agent of orchestrator's session 53).
Frame: `0-frame-and-method.md` in this directory.
Dimension: production stores 1400+ records in its v0.3.0 redb;
what is the path forward for spirit-next deployment?

## Frame

Two storage stacks are in play. **Production** is
`persona-spirit v0.3.0` — the hand-written, sema-engine-backed daemon
shipped to the user profile under both `~/.nix-profile/bin/spirit` and
(critically) `~/.nix-profile/bin/spirit-next`. **The pilot** is the
schema-derived `/git/github.com/LiGoldragon/spirit-next` repo —
runnable, but NOT deployed today. The orchestrator's framing question
("what's the path for spirit-next") splits across these two senses,
and the first finding is that the deployed `spirit-next` is **not the
schema-derived pilot at all**.

The audit compared the two storage stacks variant-by-variant against
Spirit 1249 (discriminant-stability rule, now in
`skills/rust/storage-and-wire.md:280`) and looked for migration
tooling in both directions.

## What "spirit-next" means in this audit

The naming overload caused the first hour of confusion and is the
substantive finding worth surfacing first:

- `~/.nix-profile/bin/spirit-next` is a shell wrapper at
  `/nix/store/y43j833yc5jpr5r5kwkjavkj5mb5raap-spirit-next/bin/spirit-next`
  that sets `PERSONA_SPIRIT_NEXT_SOCKET=~/.local/state/persona-spirit/next/spirit.sock`
  and execs `/nix/store/77b3y13mj5awfxnqxnjb19215gkqdy2z-spirit-next/bin/spirit-next`,
  which is a symlink into `/nix/store/rrc4j5y5cxsav1w9rzw4w8scklagavrf-persona-spirit-0.3.0/bin/spirit-next`.
- Inside `persona-spirit`, `src/bin/spirit-next.rs` is **the same CLI
  binary as `spirit`** — it just talks to a different socket via the
  `PERSONA_SPIRIT_NEXT_SOCKET` env var. Both go through
  `signal_frame::signal_cli!(spirit_next, signal_persona_spirit)`. Same
  wire shape, same storage shape.
- CriomOS-home wires this together via `persona-spirit-next.url =
  "github:LiGoldragon/persona-spirit?ref=main"` in `flake.nix:144` and
  passes its `spirit-next` package in `modules/home/profiles/min/spirit.nix:36-60`.
- The schema-derived `/git/github.com/LiGoldragon/spirit-next` pilot
  is NOT a CriomOS-home input. It is buildable from its own flake
  (`/git/.../spirit-next/flake.nix`) but has no user-profile presence.

So **production has two persona-spirit-v0.3.0 daemons running
side-by-side**: one at `~/.local/state/persona-spirit/v0.3.0/`
(production binding) and one at `~/.local/state/persona-spirit/next/`
(secondary slot). The `next/` redb contains v0.3.0 records under the
v0.3.0 schema. The schema-derived pilot's storage is not yet a live
durable surface.

For the rest of this report:

- **"production"** = persona-spirit v0.3.0, hand-written, sema-engine-backed.
- **"the pilot"** = `/git/.../spirit-next` schema-derived runnable.

The orchestrator's question "can spirit-next read production's records"
is sharp only for the pilot; the deployed-`spirit-next`-wrapper case
is just two same-shape databases.

## Production storage layout

Production daemon `persona-spirit-daemon-v0.3.0` runs as a systemd
user service; the live state directory is
`~/.local/state/persona-spirit/v0.3.0/`:

```
owner.sock      Unix domain socket (owner channel)
spirit.sock     Unix domain socket (ordinary channel)
upgrade.sock    Unix domain socket (upgrade channel)
persona-spirit.redb   redb file, ~1.27 MB on disk as of audit time
```

Plus retained snapshots / cutover-backups beside that directory
(`...redb.v0.2.0.production-cutover-20260525235707` etc.) which are
not in the live path.

The redb file is opened through `sema::Sema::open_with_schema`
(`/git/github.com/LiGoldragon/sema/src/lib.rs:475-510`), so two
implicit "infrastructure" tables exist beside the domain tables:

- `__sema_meta` — key/value table, holds `schema_version=u64`. Hard-
  fails on mismatch with declared schema at open time.
- `__sema_headers` — key/value table, holds the database-header
  rkyv-archived record.

The domain table is `records`, registered in `persona-spirit/src/store.rs:26`:

```rust
const RECORDS: TableName = TableName::new("records");
```

It is a `TableDescriptor` consumed by sema-engine, which behind the
scenes opens `TableDefinition<&str, &[u8]>` (sema/src/lib.rs:257) —
the key is the record's identifier as a **decimal string** (see
`StoredRecord::key` at `persona-spirit/src/store.rs:417`:
`RecordKey::new(identifier.value().to_string())`). The value is the
rkyv archive of `StoredRecord`.

The persisted Rust type is:

```rust
// persona-spirit/src/store.rs:45-49
struct StoredRecord {
    identifier: RecordIdentifier,
    entry: StampedEntry,
}

// persona-spirit/src/store.rs:56-61
struct StampedEntry {
    entry: Entry,            // signal-persona-spirit::Entry
    date: Date,              // u16 year, u8 month, u8 day
    time: Time,              // u8 hour, u8 minute, u8 second
}

// signal-persona-spirit/src/lib.rs:362-368
struct Entry {
    topics: Topics,          // Vec<Topic>, Topic = String newtype
    kind: Kind,              // 5-variant enum
    description: Description,// String newtype
    certainty: Certainty,    // type alias for signal_sema::Magnitude
}
```

Declared schema version: `SchemaVersion::new(3)`
(`persona-spirit/src/store.rs:22`). The "v0.3.0" name and the
schema version number happen to align right now; this is by
convention, not enforced.

Record count probe via the deployed CLI confirms records go from 1
through at least 1400 (latest seen during this audit), consistent
with the orchestrator's "1375+" estimate. Topic vocabulary is broad —
hundreds of topic strings active.

## Pilot storage layout

The schema-derived pilot is at
`/git/github.com/LiGoldragon/spirit-next`. Storage code lives in
`src/store.rs`. The redb structure is **manual**, not sema-engine-
backed:

```rust
// spirit-next/src/store.rs:16-22
const RECORDS: TableDefinition<u64, &[u8]> = TableDefinition::new("records");
const LEDGER:  TableDefinition<&str, u64>  = TableDefinition::new("ledger");
const NEXT_IDENTIFIER_KEY: &str = "next-identifier";
const COMMIT_SEQUENCE_KEY: &str = "commit-sequence";
```

Two domain tables:

- `records` — key is `u64` (the identifier as a binary integer key,
  not a string). Value is rkyv archive of `Entry`.
- `ledger` — holds the next-identifier counter and the commit
  sequence as two `u64` rows under string keys.

There is **no sema-engine, no `__sema_meta`, no `__sema_headers`, no
schema-version guard.** A fresh file is created if `path.exists()` is
false, otherwise opened blindly. The pilot's `Store::open`
(`spirit-next/src/store.rs:136-154`) calls `Database::create` directly
through redb 2.6.3 (note: production sema depends on redb 4 per
`sema/Cargo.toml`). Major redb version mismatch.

The persisted Rust type is the schema-emitted `Entry`
(`spirit-next/src/schema/lib.rs:243-250`):

```rust
struct Entry {
    topics: Topics,           // Vec<Topic>, Topic = struct NewType(String)
    kind: Kind,               // 5-variant enum
    description: Description, // String newtype  
    magnitude: Magnitude,     // 7-variant enum
}
```

No date/time. No identifier inside the value (the identifier is the
table key). No `StampedEntry` wrapper.

Schema source: `spirit-next/schema/lib.schema`. Emitted by
`schema-rust-next` into `src/schema/lib.rs` (committed) and
`target/debug/build/.../out/schema/lib.rs` (verified at build time
through `build.rs`).

State directory in nix integration tests: `/tmp/...` paths. No
production deployment slot today.

## Discriminant-stability check (Spirit 1249)

The persisted enums on the two sides are `Kind` and `Magnitude` plus
the discriminants inside `Topic` and `Description` newtype wrappers
(which are not enums, so they are immune). I checked variant order on
both sides.

### Kind — IDENTICAL

Both sides declare:

```rust
// signal-persona-spirit/src/lib.rs:309-315  AND
// spirit-next/src/schema/lib.rs:265-271
enum Kind {
    Decision,       // 0
    Principle,      // 1
    Correction,     // 2
    Clarification,  // 3
    Constraint,     // 4
}
```

Five variants, same names, same order, both without `#[repr(u8)]`
(rkyv assigns sequential discriminants in declaration order). Spirit
1249's "append new variants at the end" rule has been honored, but
trivially so — neither side has added a new `Kind`.

**Verdict: compatible.** A `Kind` byte from production's redb decodes
to the same `Kind` byte in spirit-next's emitted type.

### Magnitude — INCOMPATIBLE TODAY (the load-bearing finding)

Production uses `signal_sema::Magnitude`, with `Zero` appended last
and `#[repr(u8)]` explicit
(`/git/github.com/LiGoldragon/signal-sema/src/magnitude.rs:13-25`):

```rust
#[repr(u8)]
enum Magnitude {
    Minimum  = 0,
    VeryLow  = 1,
    Low      = 2,
    Medium   = 3,
    High     = 4,
    VeryHigh = 5,
    Maximum  = 6,
    Zero     = 7,   // appended last per Spirit 1249
}
```

The pilot's schema-emitted Magnitude
(`spirit-next/src/schema/lib.rs:275-283`, lowered from
`spirit-next/schema/lib.schema:46`) is:

```rust
enum Magnitude {
    Minimum,    // 0
    VeryLow,    // 1
    Low,        // 2
    Medium,     // 3
    High,       // 4
    VeryHigh,   // 5
    Maximum,    // 6
    // Zero missing
}
```

**Variant set differs.** The pilot's schema source omits `Zero`
entirely. Two consequences:

1. **Existing-record decode** — for the 7 originally-named variants,
   the discriminant bytes happen to line up (both 0..6 in the same
   order). Production records whose certainty is `Minimum` through
   `Maximum` will decode bytewise correctly into pilot's `Magnitude`,
   so that direction "works by accident".
2. **`Zero` records cannot decode** — any production record with
   `certainty = Zero` (discriminant 7) is unrepresentable in the
   pilot's emitted enum and rkyv decode would fail with a bytecheck
   error. The audit did not enumerate which production records carry
   `Zero` certainty; `CertaintySelection::removal_candidates()`
   (`signal-persona-spirit/src/lib.rs:488`) selects `Exact(Zero)` and
   is used in workflow for removal-candidate review — meaning
   production *does* mint `Zero` records. They would be skipped on
   pilot import.

**Verdict: ALIGNED FOR 0..6, BROKEN FOR 7.** This is exactly the
class of silent-corruption Spirit 1249 warns about, and it is live
in the pilot today: the schema source needs `Zero` appended as the
8th variant (matching production's `repr(u8)` declared layout) before
any bridge between the two stores can be byte-safe.

Recommendation upstream of the pilot: extend `spirit-next/schema/lib.schema:46`
to `Magnitude [Minimum VeryLow Low Medium High VeryHigh Maximum Zero]`
matching the declared physical order, and propagate to all asschema
files. Schema-rust-next will then emit variants in the matching
order. This is the minimum byte-compatibility fix.

## rkyv archive compatibility

Both sides use rkyv 0.8 with the identical feature set:

```
features = ["std", "bytecheck", "little_endian", "pointer_width_32", "unaligned"]
```

Confirmed for production (`persona-spirit/Cargo.toml:39`,
`signal-persona-spirit/Cargo.toml:20`, `signal-sema/Cargo.toml`,
`sema/Cargo.toml`) and pilot (`spirit-next/Cargo.toml:46`). The
feature pin matches lore's `rust/rkyv.md` canonical set — there is
no silent feature-flag drift between the two stacks.

However, archive compatibility requires not just the same rkyv
features but the same **type layout**. The Entry shapes diverge:

- Production: `StampedEntry { entry: Entry, date: Date, time: Time }`,
  archived under key `<identifier>.to_string()`.
- Pilot: `Entry { topics, kind, description, magnitude }`,
  archived under key `<identifier> as u64 big-endian`.

These are different rkyv archive layouts AND different redb key
types. The pilot cannot zero-copy access production's archived bytes.

Two distinct gaps stack on top of each other:

1. The pilot has **no date/time** in its Entry. Production's
   `StampedEntry::date`/`time` would be lost in any naive port.
2. The pilot's redb key is `u64` (binary, big-endian per redb), not
   the decimal-string key production uses. The redb table itself
   would refuse cross-read because the key type encoding differs.

**Verdict: pilot cannot read production's redb file as-is.** Even
beyond the schema-version guard (which would already block sema-
engine open against a non-sema file or vice versa), the table key
type and value type mismatch independently.

## Migration tooling state

Production-side: `persona-spirit/src/migration.rs` carries a
two-version migration ladder using the `mod historical / mod
current_shape` pattern documented in `skills/spirit-cli.md`
§"Substrate migration discipline". There are projection witnesses
for v0.1.0 -> v0.1.1 and v0.2.0 -> v0.3.0
(`V010ToV011`, `V020ToV030`). The binary
`spirit-migrate-0-2-to-next` (`src/bin/spirit-migrate-0-2-to-next.rs`)
delegates to `MigrationConfiguration::migrate_v020_to_next`
(`src/migration.rs:92-94`).

**Important — naming overload.** This `migrate_v020_to_next` refers
to "migration to the next production schema version" (which became
v0.3.0). It is NOT a migration to the schema-derived pilot. There is
**no migration code anywhere targeting the pilot's storage shape**.
The `production -> v0.3.0` migrator is just the predecessor cutover.

Pilot-side: zero migration tooling. No `import`/`export`/`Migrate`
verb in the schema. The `Input` enum in
`spirit-next/src/schema/lib.rs:287-293` has `Record / Observe /
Lookup / Count / Remove` — no import. The pilot is purely a
fresh-database engine.

Per designer 447 (record visible at production identifiers around
the upgrade-as-SEMA design), upgrades are intended to be SEMA
operations on Asschema — Maximum certainty, but **not yet
implemented**. Confirmed: nothing in either repo provides such a
mechanism today.

**Verdict: there is no tooling today to bring production records
into the pilot.** Building one is plausible but pre-requisite work.

## Side-by-side starting state

If the pilot were deployed today into its own state directory at
`~/.local/state/persona-spirit/spirit-next/` (analogous to
`v0.3.0/`), it would:

- Start with an empty redb (no schema-version guard, no record).
- Daily intent capture during incubation would continue to go to
  production's `~/.nix-profile/bin/spirit` (and the secondary
  `next/` slot that today shares the v0.3.0 wire shape).
- The pilot's database would slowly accumulate any test records
  written against it — none of them shared with production.

This is fine for a long incubation period. The pilot has the
schema-derived emission story to validate (build.rs witness checks,
generated enum surface, plane envelopes) independent of importing
existing data. The substrate-migration discipline
(`skills/spirit-cli.md` §"Substrate migration discipline") encourages
this — strict substrates take their own ground truth; cutover is
the moment of vocabulary normalisation, not a continuous bridge.

## Cutover options — feasibility verdicts for each

### Option A — Export/import via observation + Record commands

Workflow: drive `spirit "(Observe (Records ((Any []) None Any
VeryDeep WithProvenance)))"` against production, parse the NOTA
reply, re-`Record` each entry against pilot's CLI.

Blockers today:

- Pilot's CLI accepts a `Record` operation with payload `Entry`
  (`{ topics, kind, description, magnitude }`) — there is no slot
  for date/time. Provenance would be silently lost; record numbers
  (identifiers) would be re-minted by the pilot's ledger rather
  than preserved. That's a meaningful information loss.
- Pilot's `Magnitude` is missing `Zero` (variant set mismatch).
  Records with `certainty = Zero` would either be rejected or
  silently dropped, depending on the migration script's error
  handling.
- Pilot's `Input` enum has no notion of "import this with this
  identifier" — only fresh `Record`. The identifier-preservation
  pattern used in `persona-spirit/src/migration.rs:128`
  (`import_migrated_record`) is missing from the pilot's surface
  entirely. Identifiers re-mint from 1.
- Pilot has no daemon-stamped time. Even if the export preserved
  recorded date/time, the pilot would not stamp them; the
  re-recorded provenance would be the import time, not the
  original capture time. The historical record dates collapse.

**Feasibility today: low.** Would require either pilot-side schema
extension (add date/time to Entry, add Zero to Magnitude, add an
import-with-identifier operation) OR accepting catastrophic data
loss (no provenance, all dates collapse to import time, no zero-
certainty records). Neither is acceptable as a cutover.

### Option B — Direct read of production redb by the pilot

Pilot opens `~/.local/state/persona-spirit/v0.3.0/persona-spirit.redb`
directly.

Blockers today:

- redb version mismatch: pilot is redb 2.6.3, production sema is
  redb 4. File format compatibility between major redb versions is
  not guaranteed and not the documented contract; this is a hard
  blocker before anything else.
- Even with matching redb versions, the sema-engine schema-version
  guard would refuse open against a pilot that does not declare the
  matching schema version through `Sema::open_with_schema`. The
  pilot's `Store::open` doesn't speak this protocol at all.
- Table key type mismatch: production keys are `&str` (decimal-
  string identifier), pilot keys are `u64` (binary). The
  `records` table cannot be opened typed-as-`u64` when it was
  written typed-as-`&str` — redb tracks key types per table.
- Value layout mismatch: production stores rkyv-archived
  `StoredRecord` (with identifier + StampedEntry); pilot expects
  rkyv-archived `Entry` (no identifier, no stamp). Even bytecheck
  passing would still mean reading the wrong fields off the wire.

**Feasibility today: zero.** Pilot cannot read production's redb
in any form. Multiple independent incompatibilities each blocking.

### Option C — Wait for upgrade-as-SEMA (designer 447)

Maximum-certainty design but not implemented anywhere. Schema-
emitted upgrade operations applied as SEMA writes against the
target store, with the source as derivation. The shape:

- Source schema as Asschema input.
- Target schema as Asschema input.
- Upgrade plan as a schema-defined record set, generated by
  comparing the two schemas.
- Migration daemon applies the plan as ordinary SEMA writes
  against the target store.

This pattern would make the production -> pilot cutover the same
shape as a normal SEMA write trace, with each record becoming an
auditable mutation. It is the right long-term shape; it doesn't
help today.

**Feasibility today: not available.** Carrying as a future
direction, not as the cutover plan.

## Recommendations

Order from most-actionable to most-ambitious. The first three are
mandatory pre-requisites for the pilot to be deployable as a useful
side-by-side; the rest are downstream.

### Mandatory pre-requisites

1. **Append `Zero` to pilot's Magnitude schema.** Edit
   `spirit-next/schema/lib.schema:46` to read
   `Magnitude [Minimum VeryLow Low Medium High VeryHigh Maximum Zero]`.
   Regenerate `src/schema/lib.rs`. Re-run `build.rs` witness checks.
   This brings the variant set into byte-alignment with production's
   `signal_sema::Magnitude` (Spirit 1249 compliance). Without this,
   the pilot cannot represent the removal-candidate marker production
   already mints — meaning the pilot is structurally incomplete for
   intent-store work.

2. **Decide on date/time provenance in pilot's Entry.** The pilot's
   Entry has no date/time. Either (a) add them to the schema and
   regenerate, or (b) explicitly accept the pilot as a less-complete
   shape during incubation. Option (a) is the right path if the
   pilot is on track to become production; option (b) is honest if
   the pilot is exploring a different model. The frame here is
   skills/spirit-cli.md's prescription — production's daemon stamps
   date and time itself, and the agent never sets them. The pilot
   needs the same shape to be a real replacement.

3. **Adopt the sema-engine schema-version guard.** The pilot
   currently opens redb directly without `__sema_meta` /
   `__sema_headers`. Adopting `sema::Sema::open_with_schema` brings
   the hard-fail-on-mismatch property that makes the whole next/main/
   previous deployment model safe — without it, accidentally pointing
   the pilot at production's redb (or vice versa) silently corrupts
   without warning.

### Deployment shape for incubation

4. **Pilot deploys to its own state directory.** Use
   `~/.local/state/persona-spirit/spirit-next/` (NOT `next/` — that
   slot is already taken by the persona-spirit-v0.3.0 secondary
   binary). The naming choice should be explicit and visible:
   maybe `persona-spirit/pilot/` to disambiguate from the existing
   "next slot of the current shape" semantics.

5. **Pilot starts empty.** This is the side-by-side model's
   strength — no bridging, no cross-stack reads, no migration
   tool needed for incubation. The pilot's job during this phase is
   to validate the schema-derived emission, the plane envelopes, the
   single-argument config, the build.rs witness checks. Production
   records stay safely in production's slot.

6. **Daily intent capture continues against production.** Until
   cutover, `spirit` and `spirit-next` (the wrapper for v0.3.0
   secondary) remain the agent-facing surface for psyche intent.
   The pilot is exercised in test scenarios.

### Cutover, when it comes

7. **Build the historical-shape reader inside the pilot.** Follow
   the discipline named in `skills/spirit-cli.md` §"Canonical
   pattern — two-submodule migration module": private `mod
   historical` reproduction of production's `StoredRecord` and
   `StampedEntry` (rkyv-decodable from production bytes, owned by
   the pilot), `mod current_shape` aliasing the pilot's emitted
   Entry, and a `From`-chain composing the conversion. This is
   the established workspace pattern for this exact problem and
   should be the implementation reference.

8. **Cutover is an export-import done once.** Once #7 is built,
   the cutover sequence is: snapshot production's redb to a
   backup, drive the historical-shape reader to project records
   into pilot's Entry shape (with date/time appended through
   designer 447's eventual upgrade-as-SEMA when it lands, or
   through the import-with-identifier operation introduced
   alongside the migration module), import into a fresh pilot
   redb, validate count + spot-check sample records, swap the
   `spirit` alias to point at the pilot's wrapper. The cutover
   is irreversible if records get re-captured against the pilot
   afterwards, so the alias swap is the last step.

9. **No bidirectional bridge.** Spirit's discipline ("no manual
   dual-writing", `skills/spirit-cli.md` §"On the substrate
   replacement") plus the substrate-migration rule (strict
   substrate is ground truth, no backward-compat) both apply:
   once cutover happens, the pilot's data is the truth and
   production's redb becomes a static historical snapshot.

## Open questions and uncertainties

- How many production records carry `certainty = Zero` today? Not
  enumerated in this audit. If zero or near-zero, the discriminant
  mismatch is theoretical for now; if there are dozens, the
  recovery path of "rename Zero back to non-Zero before pilot
  import" gets ugly. A quick `spirit "(Observe (Records ((Any [])
  None (Exact Zero) Any SummaryOnly)))"` against production would
  resolve this.

- Does designer 447's upgrade-as-SEMA design intend to be the
  cutover mechanism for pilot adoption specifically, or is it a
  general schema-evolution mechanism that the pilot's own future
  versions would use? Not specified in the records I had access to.

- The pilot's redb 2.6.3 vs production's redb 4 dependency
  difference: is the version skew intentional (pilot is on an
  older redb because that's what `sema` was on at the time the
  pilot forked) or accidental (pilot has not been bumped along
  with sema)? Updating the pilot to redb 4 would be a
  pre-requisite for any direct file sharing, even if no other
  blockers existed.

- The pilot's `Input` enum has no `ChangeCertainty` operation
  (production has it for editing certainty without other fields).
  Not flagged as a Magnitude/Kind discriminant issue but it is a
  wire-shape gap. Out of scope for this audit; surfaced for the
  wire-shape parity sub-agent's overlap.

## Summary verdict

The schema-derived pilot's storage shape is **byte-incompatible with
production today** on three independent axes (Magnitude variant set,
Entry field set, redb key/value types), and there is **no migration
tooling targeting it from either side**. Deploying the pilot
side-by-side as an empty-database incubation slot is the right next
step; cutover requires schema convergence (Magnitude + date/time +
schema-version guard) plus a `mod historical / mod current_shape`
migration module modeled on `persona-spirit/src/migration.rs`'s
existing v0.2.0->v0.3.0 ladder, which today does NOT exist for
production -> pilot.
