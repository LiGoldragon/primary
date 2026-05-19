# 136 — persona-spirit current system and remaining gaps

*Operator update after the first useful raw Spirit slice landed.*

## 0 · Short Read

`persona-spirit` is now a usable raw intent component for typed
entry logging and querying. It is not yet a daemon actor tree.

Current path:

```text
agent
  -> persona-spirit CLI
  -> decode one signal-persona-spirit request
  -> SpiritRuntime
  -> SpiritStore
  -> sema-engine table records
  -> typed SpiritReply as NOTA
```

Example write:

```sh
persona-spirit '(Entry (naming Correction "drop ancestor prefixes" "naming context" Maximum "2026-05-19T15:46:23Z" "names do not carry their full ancestry"))'
```

Reply:

```nota
(RecordAccepted ((1 naming Correction "drop ancestor prefixes" Maximum)))
```

Example query:

```sh
persona-spirit '(RecordObservation ((None SummaryOnly)))'
```

Reply:

```nota
(RecordsObserved ([(1 naming Correction "drop ancestor prefixes" Maximum)]))
```

## 1 · What Changed

### `signal-persona-spirit`

Path: `/git/github.com/LiGoldragon/signal-persona-spirit`

The contract no longer repeats the intent namespace in every type.
The main records are:

```rust
pub struct Entry {
    pub topic: Topic,
    pub kind: Kind,
    pub summary: Summary,
    pub context: Context,
    pub certainty: Certainty,
    pub timestamp: Timestamp,
    pub quote: Quote,
}

pub struct RecordAccepted {
    pub captured: RecordSummary,
}
```

`Entry` is one top-level assertion record. Restatements are repeated
records, not a vector inside one record. `RecordIdentifier` is
spirit output, not agent input.

### `owner-signal-persona-spirit`

Path: `/git/github.com/LiGoldragon/owner-signal-persona-spirit`

The owner contract also dropped redundant prefixes:

```rust
pub struct StartOrder {
    pub generation: Generation,
}

pub struct RegisterIdentity {
    pub name: IdentityName,
}
```

The generated channel types still carry the channel root
(`OwnerSpiritRequest`, `OwnerSpiritReply`). That is macro output, not
payload naming noise.

### `persona-spirit`

Path: `/git/github.com/LiGoldragon/persona-spirit`

The runtime now has a store object over `sema-engine`:

```rust
pub struct SpiritStore {
    engine: Engine,
    records: TableReference<StoredRecord>,
}
```

Implemented request handling:

```rust
match request {
    SpiritRequest::Entry(entry) => RecordAccepted(...),
    SpiritRequest::RecordObservation(observation) => RecordsObserved(...) | RecordProvenancesObserved(...),
    other => RequestUnimplemented(...),
}
```

The CLI can persist `Entry` records and query them later from the
same database path. Tests pass an explicit `StoreLocation`; normal
CLI use falls back to `PERSONA_SPIRIT_STORE`,
`PERSONA_STATE_PATH`, then `/tmp/persona-spirit.redb`.

## 2 · Constraint Tests

The runtime tests are named after the behavior they enforce:

```text
persona_spirit_client_asserts_entry_and_mints_record_identifier
persona_spirit_client_persists_entries_for_later_summary_observation
persona_spirit_client_filters_record_observation_by_topic
persona_spirit_client_returns_provenance_only_when_requested
persona_spirit_client_repeated_entries_remain_distinct_records
```

These tests prove the current intent decisions:

```text
agents do not send identifiers
spirit mints identifiers
summary queries stay summary-only
provenance is explicit
restatement is repetition
```

## 3 · Remaining Gaps

The largest missing piece is the daemon. The component still runs the
store in-process through the CLI; it does not yet expose a Kameo actor
tree or socket boundary.

Not implemented:

```text
persona-spirit-daemon socket listener
Kameo SpiritRoot / Store actor topology
owner-signal lifecycle handling
subscriptions
classifier / guardian
spirit-to-mind owner calls
filesystem projection from database back to intent/*.nota
```

I do not see a need for new psyche clarification before the next
implementation step. The next clear slice is daemonizing this exact
store/query behavior behind the component socket without changing the
contract shape again.

## 4 · Verification

Passing locally:

```text
signal-persona-spirit: cargo test --locked
signal-persona-spirit: cargo clippy --all-targets --locked -- -D warnings
owner-signal-persona-spirit: cargo test --locked
owner-signal-persona-spirit: cargo clippy --all-targets --locked -- -D warnings
persona-spirit: cargo test --locked
persona-spirit: cargo clippy --all-targets --locked -- -D warnings
```

Passing through Nix with remote builder:

```text
signal-persona-spirit: nix flake check -L --max-jobs 0
owner-signal-persona-spirit: nix flake check -L --max-jobs 0
persona-spirit: nix flake check -L --max-jobs 0
```
