# 277 - Operator b6ad09ac migration audit (2026-05-22)

*Designer audit. Operator pushed `sema-upgrade@b6ad09ac` (09:48),
turning the no-op stub into a real `persona-spirit 0.1.0 -> 0.1.1`
migration with a one-argument temporary CLI and ran it against the
deployed Spirit database backup (103 records converted). Migration
logic is clean: two private submodules (`historical`,
`current_shape`) carry source and target rkyv shapes; the redb-walk
reads with the historical descriptor, maps
`Certainty::{Maximum,Medium,Minimum}` into the same-named Magnitude
rungs, asserts into a fresh target. The temp CLI takes exactly one
NOTA argument or one NOTA-file path and emits NOTA via the codec.
Live artifacts exist; deployed daemon still serves (114 records,
post-backup). One workflow violation: `signal-persona-spirit` is
still pinned at `branch = "operator/spirit-response-protocol"`
(commit `d7b22bfb`), not main. Spirit record 109 (08:00, before
b6ad09ac) explicitly names this as the case that "should not have
been a branch - just merged to main". Magnitude branches must merge
to main before cutover proceeds.*

## 1. Audit summary

b6ad09ac is a faithful execution of /276 §11 slices 1-3 (migration
body + temp CLI + live run). Migration logic correctly scoped to
sema-upgrade (no leakage into persona-spirit); single-argument NOTA
rule honored; live witness validates /275 Point 6. Remaining gap is
/276 §11 Slice 4: `operator/spirit-response-protocol` is still a
branch. Record 109 makes this a discipline violation, not a designer
judgment. Cutover bead `primary-x3ci` correctly defers the swap to
post-deploy. **Pattern counts: 8 good, 4 ugly.**

## 2. Migration logic audit

**File.** `/git/github.com/LiGoldragon/sema-upgrade/src/migrations/persona_spirit/version_0_1_0_to_0_1_1.rs`
(b6ad09ac, 449 lines).

**Submodule shape.** `mod historical` (lines 102-236): private rkyv
definitions for the v0.1.0 shape - `Certainty {Maximum, Medium,
Minimum}` three-variant; full reproduction of Topic, Summary, Quote,
Context, Date, Time, Kind, Entry, StampedEntry, StoredRecord. `mod
current_shape` (lines 238-318): same-name types binding
`Entry::certainty: Magnitude` (from `signal_sema::Magnitude`) and
importing unchanged leaves from the current `signal_persona_spirit`
crate. `From` impls cascade: StoredRecord -> StampedEntry -> Entry,
plus enum-to-enum maps for Kind and Certainty -> Magnitude.

**Certainty -> Magnitude mapping** (lines 303-311):

```rust
historical::Certainty::Maximum => Self::Maximum,
historical::Certainty::Medium  => Self::Medium,
historical::Certainty::Minimum => Self::Minimum,
```

Three legacy variants map to three same-named Magnitude rungs; the
four intermediate Magnitude rungs are unreachable from historical
data (correct - no historical record carried any other value).
Stored discriminator bytes (0/1/2) are read through historical rkyv,
mapped to Magnitude bytes (0/3/6 in the seven-variant ordering) by
typed `From`. Structural-class migration per /263; the
implementation correctly does NOT attempt zero-cost byte
reinterpretation.

**Read/write loop.** `migrate_paths` (lines 34-51) preflight refuses
missing source / existing target / same-path. `read_historical_records`
(lines 64-79) opens engine with `SPIRIT_SCHEMA_VERSION = 1`,
registers historical descriptor against `TableName::new("records")`,
runs `QueryPlan::all`, sorts by `identifier.value()`. `write_current_records`
(lines 81-100) opens fresh engine on target, registers current_shape
descriptor, iterates and asserts via `From::from`.

**Tests** (lines 320-449): three tests cover happy path (three
records, all Certainty variants, identifier/topic/date/time
preservation, Magnitude correctness), target-exists rejection,
source-missing rejection.

**Persona-spirit is not touched.** Historical types are private to
sema-upgrade; current types borrow unchanged leaves. /270 §4a
("persona-spirit MUST NOT contain import logic") satisfied.

## 3. Temp CLI audit

**File.** `src/bin/sema_upgrade_temporary.rs` (109 lines).

**Single-argument rule.** `read_single_argument` (lines 37-50):
exactly one `args().skip(1).next()`; second positional argument
rejected; if trimmed input starts with `(`, treated as inline NOTA;
otherwise as a path read via `fs::read_to_string`. No `--verbose`,
no `--format`, no env vars. Rule honored.

**NOTA shape.**

```text
(Attempt (<source-path> <target-path> (<component> (M m p) (M m p))))
```

`TemporaryAttempt` (lines 7-12) is a `NotaRecord` with three
positional fields: `source: Path`, `target: Path`, `attempt:
Attempt`. The single top-level enum `TemporaryCommand` has one
variant `Attempt(TemporaryAttempt)`. Reuses
`signal_sema_upgrade::Attempt` as the third field, so the wire
identifier matches what the eventual daemon's
`signal-sema-upgrade::AttemptUpgrade` accepts. Positional
throughout.

**Reply.** `print_reply` (lines 99-106) encodes `Reply` via
`nota_codec::Encoder` and prints with trailing newline.
`UpgradeRejected` becomes process exit 1; `UpgradeCompleted` is
exit 0. NOTA on stdout, error message on stderr.

**Dispatch.** `execute` (lines 61-75) builds `DatabaseMigration`
and calls `MigrationIndex::prototype().migrate_database(&migration)`.
No second dispatch table; the temp CLI reuses the runtime index.

**Rejection mapping** (lines 77-97) collapses
`SourceMissing/TargetAlreadyExists/SameSourceAndTarget/Failed` to
`RejectionReason::MigrationFailed` - over-broad but acceptable for
the temp CLI; the daemon should add finer reasons.

## 4. Live migration artifacts

```
persona-spirit.redb                                  286720 May 22 10:01  (live, restored old)
persona-spirit.redb.v0.1.0.backup-20260522075112     208896 May 22 09:51  (backup)
persona-spirit.redb.v0.1.1.migrated-20260522075112   380928 May 22 09:51  (migrated target)
```

Both backup and migrated files exist as operator reported. Sizes
plausible. `bd show primary-x3ci` returns the cutover bead (P1, OPEN,
labels `deployment, operator, persona-spirit, sema-upgrade`), with
description correctly gating the swap on "deploying the current
Spirit daemon/CLI first".

Deployed daemon serves: `spirit '(Observe (Records (None None
SummaryOnly)))'` returns 114 records - more than the 103 in the
migrated DB because new audit/dispatcher records were logged after
the backup was taken. Deployed binary is
`/nix/store/4y7sgkqsiqvqngs7kidh0f5spi9xrw2s-spirit/bin/spirit`
(pre-Magnitude). Operator's restore-the-old-DB choice is correct -
the running binary expects Certainty bytes.

## 5. Dependency state - workflow violation

`sema-upgrade@b6ad09ac` Cargo.toml pins
`signal-persona-spirit = { ..., branch = "operator/spirit-response-protocol" }`,
resolved in Cargo.lock to `d7b22bfb77b91cb2693b9fdb04f2115825ebee2f`.
`git branch -a --contains d7b22bfb` returns ONLY the
operator/spirit-response-protocol branch and its remote - NOT main.
Both Magnitude-bearing commits (`d7b22bf` on signal-persona-spirit,
`d1c76108` on persona-spirit) are still branch-only.

**Spirit record 109** (workspace, Decision, Maximum, 2026-05-22
08:00, logged 1h40min BEFORE b6ad09ac):

> "The workspace does not use feature branches by default. Merges go
> directly to main. Version tracking happens via semver tags ...
> The Spirit-Magnitude branch (operator/spirit-response-protocol)
> should not have been a branch - just merged to main."

The branch-pin in b6ad09ac is the exact case named in record 109.
**Workflow violation, flagged.** The fix: merge the two
Magnitude-bearing commits to main, tag 0.1.1, repoint sema-upgrade's
Cargo.toml at `branch = "main"`, regenerate Cargo.lock, push. The
dependency pin must move before the cutover bead `primary-x3ci` can
proceed.

Other pins in Cargo.toml are `branch = "main"`: nota-codec,
owner-signal-sema-upgrade, sema-engine, signal-executor,
signal-frame, signal-sema, signal-sema-upgrade. Magnitude pair is
the only branch-pin.

## 6. Match against /270, /263, /276

**Against /270.** §4c (Certainty -> Magnitude as the mapping step):
implemented exactly. §4d (future redb-walking migrations reuse this
pattern): the historical / current_shape split is the reusable
pattern. §4a (persona-spirit MUST NOT contain import logic):
satisfied.

**Against /263.** Schema-address vs semver: still semver. `Version
(major minor patch)` continues to be the identity surface. /276
§10a's intent-clarity-critical question is unchanged - psyche has
not decided between schema-address (a) / semver-only (b) / layered
(c). b6ad09ac neither chose nor closed this.

**Against /276.** §11 Slice 1 (migration body): done. Slice 2 (temp
CLI): done. Slice 3 (live run on a copy): done; /276 §10f variant
(c) was answered in-flight - copy-migrate-verify-but-cutover-later;
migrated DB at `.v0.1.1.migrated-*`, original at `.v0.1.0.backup-*`,
live is the restored old DB. Slice 4 (merge to main): NOT done; §5
above is its consequence. Slice 5 (daemon): not attempted,
correctly. /275 Point 6 live witness is closed for the read-write
half; the read-back-with-v0.1.1-binary half is gated on Slice 4.

## 7. Patterns observed

**Good (8).**

1. **Two-submodule shape: `historical` + `current_shape`.** Future
   migrations reuse this. Source bytes get a private reproduction of
   deployed types; target bytes borrow current crate leaves and
   override only what changed. Eight leaves duplicated verbatim, one
   replaced (Certainty), three branch-types reshape. Narrow,
   reviewable diff.
2. **`From`-chained translation.** Whole conversion is one
   direction of typed flow; no per-field handwiring at the call
   site.
3. **Field name preserved: `entry.certainty`.** Even though the
   type is now Magnitude, the field name stays `certainty`. Per
   AGENTS.md / field-name-carries-dimension: dimension lives in the
   field name; variant set is the universal rung vocabulary.
4. **Preflight refuses unsafe states.** Source-missing,
   target-exists, same-path caught before any redb work starts.
5. **Sort by identifier before write.** Two runs of the migration
   on the same source produce identical target bytes - matters for
   any future content-addressing.
6. **Temp CLI reuses runtime index.** No second compile-time
   dispatch table.
7. **Single-NOTA-argument rule honored.** Inline string or path,
   not both; second argument rejected; no flags.
8. **Reply is NOTA on stdout.** The temp CLI behaves like a
   degenerate-shape Signal client.

**Ugly (4).**

1. **Branch-pin on `signal-persona-spirit`.** §5 above. Direct
   violation of record 109. Must be cleared before cutover.
2. **`RejectionReason::MigrationFailed` is over-broad.** Five
   error conditions collapse to one. Acceptable for the temp CLI;
   the daemon's `RejectionReason` should fan out.
3. **Schema-address still semver.** Per /276 §10a; load-bearing
   fork still open.
4. **Sort by `identifier.value()` only.** Not a bug today; flagging
   the implicit assumption for any future identifier-semantics
   change.

## 8. Open items for follow-up

**8a. Cutover gating** (blocks `primary-x3ci`): (1) merge
operator/spirit-response-protocol to main on signal-persona-spirit
AND persona-spirit; tag 0.1.1; (2) repin sema-upgrade Cargo.toml
to `branch = "main"`, regenerate Cargo.lock, push; (3) rebuild
CriomOS-home, deploy, swap `.v0.1.1.migrated-*` into live path,
restart spirit, verify with a fresh Magnitude-rung Record.

**8b. Version-suffixed multi-daemon for verification.** /276 §10f
variant (c) is open: side-by-side verification by running a v0.1.1
daemon against the migrated DB before cutover. Operator's current
path treats merge-and-deploy as verification. Decision opens a
question about parallel `persona-spirit-v0-1-1` daemon on separate
socket if multi-daemon-per-component becomes the cutover pattern.

**8c. Schema-address fork.** /276 §10a unchanged. The next
sema-upgrade slice that touches the wire identifier is the natural
decision point.

**8d. Daemon (Slice 5).** Bead `primary-l3h5` open. Awaits answers
on /276 §10c (boot order), §10d (self-upgrade), §10f (success
criterion). Record 109's no-branches rule applies - no
`operator/sema-upgrade-daemon` branch.

**8e. `RejectionReason` fanout.** Before the daemon ships, the
ordinary `signal-sema-upgrade` `RejectionReason` enum should gain
finer variants (source-missing, target-exists, component-mismatch,
version-mismatch, engine-error) so the daemon's response surface is
honest about which class of failure happened.

## 9. References

- **Operator commit.** `sema-upgrade@b6ad09ac` (2026-05-22 09:48).
- **Designer reports.** `/263` schema-spec language; `/270`
  sema-upgrade design; `/275` operator audit (Point 6 live witness);
  `/276` sibling sema-upgrade prototype audit (earlier today).
- **Intent.** Spirit record 109 (workspace, Decision, Maximum,
  2026-05-22 08:00) - no-branches-by-default. This audit's load-
  bearing intent reference.
- **Beads.** `primary-x3ci` (cutover, P1, open); `primary-l3h5`
  (daemon, open).
- **Live artifacts.** `/home/li/.local/state/persona-spirit/persona-spirit.redb.v0.1.0.backup-20260522075112`,
  `/home/li/.local/state/persona-spirit/persona-spirit.redb.v0.1.1.migrated-20260522075112`,
  `/home/li/.local/state/persona-spirit/persona-spirit.redb` (live,
  restored). Deployed binary
  `/nix/store/4y7sgkqsiqvqngs7kidh0f5spi9xrw2s-spirit/bin/spirit`.
- **Branch state.** `signal-persona-spirit@d7b22bfb` and
  `persona-spirit@d1c76108` on `operator/spirit-response-protocol`,
  not on main.
