# sema-engine: the first Memorable slice

Subflow of 3ec648, 2026-10-02. Repository `sema-engine`, from main 489d290d (0.17.0) to 9884905f (0.18.0), three commits, pushed on main. Design: Mind Astra dea0ba's sketch (`reports/memorable-sketch.md`), smallest target. Authority: the living's typed words of 2026-10-02 on the memory kind (in the brief).

## What landed

Commits: c94f31ce (typed change), 65bf9de3 (typed upgrade replaces `with_prior`), 9884905f (0.18.0, ARCHITECTURE, new UPGRADES.md). Code is in `src/memory/` (`mod.rs`, `change.rs`, `upgrade.rs`). The surface is traits first:

- `Memorable` on a stored record type: `type Change`, `type Refusal`, `change(Option<&Self>, &Change) -> Decision<Self, Refusal>` (`Ready` or `Refused`). It is pure; nothing is durable until the engine commits.
- `MemoryChanges` on `Engine`: `change(MemoryChange) -> ChangeOutcome<Refusal>` with three branches:
  - `Changed(ChangeReceipt)`: the caller-chosen `ChangeIdentifier`, the effect (Created or Replaced), the key, the commit sequence and the snapshot.
  - `Refused(Record::Refusal)`: the record's own typed reason. The engine `Error` enum never carries it.
  - `Failed(StorageFailure)`: a `StoragePhase` plus the engine error that caused it. Admission, Read and Commit mean the store is confirmed unchanged. AfterCommit means the change is durable and its receipt resolves by its id.
  - The receipt lands in `__sema_engine_change_receipts` in the same transaction as the row, the logs and the counters. `change_receipt(id)` resolves an uncertain outcome. A change resent under an id that already committed answers its recorded receipt and is not applied again.
- `MemoryDefinition` gives a record definition its manifest version and its schema hash. `UpgradeFrom<Predecessor>` is the authored conversion, returning `Decision<Self, typed Refusal>`. `TableDescriptor::with_predecessor::<P>()` records a `ManifestEdge`: the declared version and the predecessor it names, mapped to the old and new schema hashes. Only a forward edge that names the descriptor's own hash is admitted.
- `MemoryUpgrades::upgrade_table::<P, C>(descriptor)` returns `Upgraded(receipt)`, `AlreadyCurrent(table)`, `Refused { key, reason }` or `Failed(StorageFailure)`. Every row converts before any is written. The converted rows, the catalog registration (the format marker) and the log entries land in one transaction. `UpgradeFault::AfterRowsWritten` interrupts that transaction for the crash witness.
- `with_prior(SchemaHash, Fn(Prior)->Current)` and `EvolutionStep` were removed, not kept alongside. `register_table` no longer migrates. When the store still holds a declared predecessor it refuses with `Error::UpgradePending`; an undeclared identity still gets `FamilyIdentityMismatch`. The consumers inside the repository were moved to the typed form: `tests/family_evolution.rs` (9 tests) and `tests/open_atomicity.rs`. No other repository under `/git` used `with_prior`.

## What is proven

Witness family (`tests/note_family/mod.rs`): note v1 holds `text`; v2 holds `title` and `body`. The split rule: the title is the first line, trimmed; the body is everything after the first line break, verbatim, or empty when there is none. An empty text, or one whose first line is blank, refuses with `InvalidLegacyTitle { note }`. The change refusals are `EmptyTitle` and `Missing`.

- `tests/memorable_change.rs` (4 tests):
  - A ready change commits. Its receipt survives a reopen.
  - A repeated change id answers its recorded receipt without a new commit.
  - A refused change answers `EmptyTitle` or `Missing`. The `.sema` file bytes are identical, the commit sequence does not move and no receipt is written.
  - An unregistered table yields `Failed` at the Admission phase.
- `tests/memorable_upgrade.rs` (4 tests):
  - A ready upgrade splits the text as the rule says. The marker and rows are v2 in the raw store.
  - A refused conversion (the empty text) names the row and its typed reason. The file bytes are unchanged, the raw marker is v1 and the rows decode as v1 and equal the seed. `register_table(v2)` answers `UpgradePending`.
  - An interrupted commit yields `Failed` at the Commit phase. After reopening, the raw catalog names v1, every row decodes as v1 (validated), and no log entry survived. A retry lands the whole upgrade.
  - A fresh store registers v2 directly.
- Seen failing first:
  - All 8 tests failed against stub bodies. That evidence is weak: it was a panic from the stubs, not a failed assertion.
  - The interrupted-upgrade test also failed by assertion against the real upgrade before the fault hook was wired: it got `Upgraded` where `Failed` was expected.
  - The refused-upgrade bytes check first failed because the file bytes were sampled before the engine opened (an open writes). It now compares bytes while the engine is open.
- Local runs:
  - `cargo test`: the full suite is green.
  - `cargo clippy --all-targets -D warnings`: clean.
  - `cargo doc` with `-D warnings`: clean.
  - `cargo fmt`: applied.
- `nix flake check`: see the Check section.

## What remains

- **Eager versus lazy.** The engine now guarantees one thing: an eager, whole-family upgrade at registration time. It commits all rows plus the marker, or nothing. It offers no lazy conversion per record, and nothing schedules migrations. Astra's note that "the atomic open stamp alone proves neither" still holds for every other path. The edges are direct, not chained hops: a store two versions back needs its own declared edge.
- **Identified families.** `IdentifiedTableDescriptor` has no `with_predecessor` and no upgrade. `Memorable::change` is wired only for domain-keyed tables.
- **Receipts and the log.** The receipts table is engine metadata. It is not folded from the versioned log, so a rebuild or a checkpoint import loses it. A typed change also refuses inside an engaged staged group (`StagedChangeUnsupported`).
- **Change and upgrade surfaces not built.**
  - A change can create or replace a record but cannot retract one.
  - There is no Signal-side archive of `ChangeOutcome`. `StorageFailure` wraps the engine `Error`, which is not rkyv and still carries strings.
  - Nothing checks that the key stored under is the record's own key.
- **The Memory root in ethos-zero.** It does not exist. ethos-zero reads Library, Signal and Sema (knowledge-ethos). The manifest edge here is a hand-written `MemoryDefinition` impl, not something generated from a manifest. No generator emits `Memorable`, `UpgradeFrom` or descriptors from an ethos edit. Astra's point 3 is untouched: generating a rename or a defaulted field from the edit, and reporting an unresolved conversion.
- **Consumers.** orchestrate, flow and message pin older sema-engine revisions. None of them used `with_prior`, so repinning to 0.18.0 needs no code change from this slice. Adopting `Memorable` is their own work.

## Check

The run was `nix flake check -L github:LiGoldragon/sema-engine/9884905ff9c6…` in the detached unit `sema-engine-check-memorable-3ec648` (RuntimeMaxSec=7200). RESULT_PENDING

## Sources

- `/home/li/primary/flows/3ec648/reports/memorable-sketch.md` (Astra dea0ba, verbatim)
- `/home/li/primary/flows/3ec648/reports/sema-engine-reads-and-stamp.md`
- sema-engine `src/memory/{mod,change,upgrade}.rs`, `src/table.rs`, `src/engine.rs`, `src/open.rs`, `src/error.rs`, `tests/memorable_change.rs`, `tests/memorable_upgrade.rs`, `tests/note_family/mod.rs`, `tests/family_evolution.rs`, `tests/open_atomicity.rs`, `ARCHITECTURE.md` (Memorable section), `UPGRADES.md`; commits c94f31ce, 65bf9de3, 9884905f
- Skills vision-ethos, knowledge-ethos, vision-nexus, versioning, breaking-upgrades, testing
