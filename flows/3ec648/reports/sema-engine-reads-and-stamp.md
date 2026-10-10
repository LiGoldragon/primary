# sema-engine: read plans and the atomic open stamp

Subflow of 3ec648, 2026-10-02. Repository `sema-engine`, from remote main 516f01fe (0.16.0) to 489d290d (0.17.0), three commits pushed on main.

## What was unsupported, and what consumers ask

`ReadPlanNode` had nine operators. `AllRows`, `ByKey` and `ByKeyRange` executed. `Filter`, `Constrain`, `Project`, `Aggregate`, `Infer` and `Recurse` answered `UnsupportedReadPlan` in `match_records`, in `validate` (which runs through it) and in staged-session reads. Their plans carried placeholder strings (`PredicatePlan.expression`, `FieldSelection`, `AggregatePlan.reducer`, `RuleSetRef`, `RecursionMode`). Identified tables have only all, identifier and identifier range.

The three consumers use only the supported leaves. The counts are call sites in their crates:

- orchestrate (pinned at 27e814a7): `QueryPlan::all` ×13, `QueryPlan::key` ×1, one subscribe. It reads singleton tables and counts rows with `.records().len()`.
- flow (pinned at 516f01fe): `QueryPlan::key` ×18, `QueryPlan::all` ×11, one `validate`, one `storage_reader`. Several reads take a whole table and then filter it in memory by a field. One example is `quarantined.launch_request_id == launch_request_id` in `flow-nexus/src/store.rs` at about line 1548; another is a filter on `native_launch_binding_option` at about line 2146.
- message (pinned at 516f01fe): `QueryPlan::key` ×3, `QueryPlan::key_range` ×1, `QueryPlan::all` ×1, one subscribe. Its receipts read is a key range followed by `retain(|r| r.message_id == message_id)` in `message-nexus/src/store.rs` at about line 233.

So the one plan the consumers actually need is a filter by a record's field, over a whole table or a key range. Counting is already `validate(..).record_count()`. Nobody asks for Constrain, Project, Aggregate, Infer or Recurse.

## (1) Filter, implemented

- The predicate is now a trait, `RecordPredicate<RecordValue>` with `admits(&self, &RecordValue) -> bool`, implemented by the component on a data-bearing type. A read plan holds it as a `RecordFilter`. This replaces the string `PredicatePlan`.
- Plans are executed by two traits: `ReadPlanExecution`, implemented on `ReadPlanNode<RecordValue>` (now generic over the record), and `RowSource`. `RowSource` has two implementations: `CommittedRows` (one read transaction, so the marker and the rows agree) and `OverlaidRows` (the staging overlay). `match_records`, `validate` and staged reads all go through it.
- `QueryPlan::filtered(table, predicate)` and `.filtered_by(predicate)` work on any source: all rows, key, key range, or another filter.
- `subscribe` refuses a filtered plan with `UnsupportedReadPlan { Filter }`. Deltas match by key, and a retraction carries no record for the predicate to judge, so a filtered subscription would deliver rows outside its own view.
- The other five operators are still unsupported and still carry their placeholder strings.
- Tests are in `tests/read_plans.rs` (6). They failed first: five failed with the old dispatch. The subscribe refusal passed at first only because the read failed; once Filter executed it failed, and it passed after the guard was added.

## (2) The open stamp, made atomic

The engine's design uses one storage-kernel write transaction per durable effect, with family evolution as the precedent, so that is the mechanism used here; there is no write-then-rename.

Before the change, an open made separate writes: the layout stamp (or the refolded derived slots and re-stamp), then the versioning-policy row. After that, each `register_table` wrote its own transaction. That is the gap orchestrate's NON_IDEAL entry describes.

Witness, observed before the fix: an open interrupted between the stamp and the policy left `Stamped { layout: Some(7), policy: None, families: [] }` in the raw store.

What changed:

- Every open-time check now only reads: layout, policy, and declared families. That includes the derived-slot refold and its chain verification, now `CommitLog::refolded_derived_slots` returning `DerivedSlots`.
- `persist_open` then writes the layout plan, the first policy row, and the catalog rows of families declared with `EngineOpen::with_family(&descriptor)`, all in one transaction. A declared identified family also gets its counter row. Declarations come through the `DeclaresFamily` trait, implemented on `TableDescriptor` and `IdentifiedTableDescriptor`.
- A conflicting declared identity, or one family bound to two tables, refuses the open before anything is written.
- A stored prior generation that the declaration evolves from is left for `register_table` to evolve.
- `OpenFault::AfterLayoutStamped` aborts inside that transaction.
- `EngineOpen` moved to `src/open.rs`.
- Tests are in `tests/open_atomicity.rs` (5). Four failed first; the evolving-prior case passed both before and after, as intended. The interrupted open now leaves the raw store with no layout, no policy and no catalog row, and a clean reopen lands all three.
- The full suite passes locally, and clippy passes with `-D warnings`.

What remains:

- The kernel's own header and schema-version stamp (`sema::Sema::open_with_schema`, in `__sema_meta`) is a separate, earlier transaction, and it is in the `sema` repository. While reading it I saw a likely crash hazard but did not test it: `is_fresh_file` is taken from `!path.exists()` before `Database::create`. A crash after the file is created but before the stamp commits would leave a file the next open refuses as `LegacyFileLacksSchema`. This was not touched.
- Families registered only through `register_table` still land one transaction each. Orchestrate is atomic only once it declares its three or four families through `with_family`. That adoption is orchestrate's work, and its pin is still at 27e814a7.

## (3) Distance to the memory kind the living described

His words (91ea9f `vision/ethos.md`, 2026-10-02) are hedged: "a standard successful or unsuccessful change", "each version is possibly going to have an implementation of an upgrade from or an upgrade to. I'm not sure … upgrade from makes more sense … could be a symmetrical operation", and the upgrade "is going to be the very edit".

- **Typed change result.** Writes return `Result<MutationReceipt | CommitReceipt | IdentifiedMutationReceipt, Error>`. Success is typed: commit sequence, snapshot and key, through a `DatabaseMarker`. Failure is a single engine-wide `Error` enum. It is not per kind and not rkyv-archived, so it cannot travel on Signal. About 28 of its fields are Strings, for example the stored and declared values in `FamilyIdentityMismatch`. The versioned log records only successful changes; a refused change leaves no record. Missing: a per-kind change outcome type (changed, or refused with a typed reason) that the kind itself carries and that can be archived.
- **Per-version upgrade-from.** Only domain-keyed families have one: `TableDescriptor::with_prior(SchemaHash, Fn(Prior) -> Current)`. It is a hand-written closure, keyed by a prior's blake3 schema hash rather than a version. Each prior converts in one direct step to the current shape rather than through a chain of per-version steps. Identified families have none. Ethos-generated tables (`TableSpecification`) explicitly "carry no evolution behavior". Nothing derives the upgrade from the ethos edit. Missing: a version-to-version upgrade owned by the kind and generated from the ethos diff, versions read from the manifest, coverage for identified and generated families, and the open question of symmetry (upgrade-to) that he left open.
- The distance is large on both parts. The engine has the right transactional and logging machinery (evolution lands rows, catalog and log in one transaction; refused opens and evolutions write nothing), but the shape is a closure keyed by hash, not a kind. None of this was implemented, as the brief asked.

## Check and NON_IDEAL

`nix flake check -L github:LiGoldragon/sema-engine/489d290df38a…` ran once in the detached unit `sema-engine-check-3ec648` (RuntimeMaxSec=2700), built on prometheus, and ended `Result=success` with "all checks passed!" (x86_64-linux). Orchestrate's NON_IDEAL entry got one appended line (orchestrate a90c38c2): the engine fix has landed, and the entry closes once orchestrate repins and declares its families at open.

## Sources

- sema-engine `ARCHITECTURE.md`, `NON_IDEAL_AGENTS.md` (only a Protos-train notice; no read-plan or stamp entry), `src/query.rs`, `src/engine.rs`, `src/catalog.rs`, `src/commit_log.rs`, `src/open.rs`, `tests/read_plans.rs`, `tests/open_atomicity.rs`; commits 692aa5ea, 928f0175, 489d290d.
- orchestrate `NON_IDEAL_AGENTS.md` «Store-format stamping is not atomic with family registration»; `crates/orchestrate-nexus/src/store/*.rs`.
- flow `crates/flow-nexus/src/store.rs`, `store/delivery.rs`; message `crates/message-nexus/src/store.rs`.
- sema `src/lib.rs` `open_with_schema`, `ensure_schema_version`.
- `/home/li/primary/flows/91ea9f/vision/ethos.md` (memory kind); `/home/li/primary/flows/3ec648/rulings.md` ruling 3; vision-ethos skill.
