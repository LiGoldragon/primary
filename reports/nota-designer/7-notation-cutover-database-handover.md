# NOTA Notation Cutover And Spirit Database Handover

## Claim

Changing canonical NOTA string notation from quote-delimited strings to
bracket strings should not, by itself, break the Spirit database, because the
database boundary is typed storage, not raw NOTA text storage.

In the current `persona-spirit` source, `src/store.rs` opens a sema-engine
`persona-spirit.redb`, registers a `records` table, and persists
`StoredRecord { identifier, entry: StampedEntry }` as rkyv-archived typed
records. `StampedEntry` contains the typed `signal-persona-spirit::Entry`
plus daemon-stamped date/time. The NOTA parser is on the CLI/request boundary:
the `spirit` CLI decodes one NOTA argument into a typed Signal operation, sends
length-prefixed rkyv Signal frames to the daemon, and renders typed replies
back to NOTA.

So the notation change is mainly a runtime/parser/client cutover. It becomes
an on-disk migration only if the archived Rust types or sema table shape
change.

## Current Upgrade Shape

The current Spirit upgrade surface already has most of the handover vocabulary:

- `AskHandoverMarker` reads component name, contract version, commit sequence,
  write counter, last record identifier, and timestamp.
- `ReadyToHandover` accepts only when the source marker still matches the
  daemon store.
- Accepted readiness freezes public writes while ordinary reads remain
  available.
- `HandoverCompleted` finalizes only after accepted readiness and unchanged
  marker, then removes ordinary and owner socket paths.
- `RecoverFromFailure` reopens public writes after a failed readiness window.
- `Mirror` can apply component-private `StampedEntry` rkyv payloads after
  completion when the target contract version matches.

The tests named in `persona-spirit/ARCHITECTURE.md` witness these properties,
including marker drift rejection, write freeze, recovery, mirror application,
wrong-target rejection, and Persona selector flip from `v0.1.0` to `v0.1.1`.

## Hard Handover Interpretation

For the psyche's proposed `0.1` hard handover, the clean shape is:

1. Stop treating zero-downtime as the immediate requirement.
2. Use manual downtime at the psyche's chosen moment, only after an explicit
   agent order.
3. Keep the old database as the immutable backup source during preflight.
4. Start the new runtime against a copied or projected target database.
5. Run an offline responsiveness/readability test against the backup without
   durable writes to that backup.
6. Write the successful upgrade-test witness only into the new database.
7. Flip the active runtime selector only after the witness exists and the new
   engine can read the migrated/copied records.

That gives the workspace a real runtime engine switch without forcing the
parser change to masquerade as a live database migration.

## Database-Test Witness

The proposed "database-test passed" entry should be a typed system/upgrade
record, not an ad-hoc human intent entry. It should say, in component-native
terms:

- which component and source version were tested;
- which target version and contract hash accepted the database;
- which source marker was read from the backup;
- which target marker was observed after the test;
- which checks passed: open, read, topic/record query, last identifier,
  optional sampled provenance decode, and write/read of the witness in the
  target database;
- when the test ran.

The important invariant is asymmetric mutability: the backup database is read
only during preflight, while the target database records the fact that the new
engine successfully opened, read, and wrote through its own current type
system.

## Answer To The Immediate Question

Yes, with that boundary: a NOTA notation hard cutover can avoid breaking the
database if the stored typed records do not change. The unsafe path would be
mixing old and new parsers against one live CLI/daemon surface without an
explicit runtime switch. The safe path is a `0.1` hard handover with downtime,
backup-read preflight, target-db upgrade witness, and then selector flip.

The remaining design work is to promote the database-test witness into a
proper typed contract. It belongs near the version-handover / engine-management
surface, not as a free-form text convention inside ordinary Spirit intent.
