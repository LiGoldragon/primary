# Lojix onto its Ethos: steps 6 and 7

Both steps are on branch `ethos28-be2651` of lojix. Each is one commit, pushed and gated green on prometheus. Nothing is merged, released or deployed.

Each claim is marked **Observed** (seen in a run or in source) or **Inference**. `$S` is `/tmp/claude-1001/-home-li-primary/be26511c-e6c3-597a-9e57-a86a1ac3a1e0/scratchpad`.

## Heads

| step | commit | version | gate |
|---|---|---|---|
| base | 26caf36 | 0.10.7 | — |
| 6 | **bde7b0e70df6ba9f39574004a9091ed165f01eb1** | 0.10.7 | 18 of 18 green, `$S/s67/gate-lojix-bde7b0e.log` |
| 7 | **7f218c152db68d27b6c38f3c1cd83ae0323eaa7c** | 0.11.0 | 18 of 18 green, `$S/s67/gate-lojix-7f218c1.log` |

Each gate covered build, clippy, fmt, test, both trait-law checks, the four NixOS VM checks and the rest of the flake's checks. The `test` check ran the new representation and fixture tests: 10 and 3 passed at step 6, 12 and 4 at step 7 (Observed in the logs).

`cargo test --workspace` on the builder:
- step 6: 232 passed, 3 ignored;
- step 7: 235 passed, 3 ignored.

Both runs fail the same two tests in `tools/tests/nexus_configuration.rs`, with `LegacyFileLacksSchema`. They fail identically at 26caf36, and the gate does not run them (Observed; logs `$S/s67/t4.log` and `$S/s67/t6.log`).

## Step 6 (bde7b0e): the leaf twins go

**What changed (Observed).**
- **runtime_model.rs.** 106 hand declarations are gone. They are now `pub use` of the generated signal-lojix and meta-signal-lojix types:
  - every scalar and integer newtype;
  - the four markers, and `StateMarker`, which is now `DatabaseMarker`;
  - all 26 unit enumerations, with `DeploymentLifecycle` and the hand `DeploymentPhase` now the contract's one `DeploymentPhase`;
  - every record whose shape agrees with the contract's: requests, rejections, receipts, `DeploymentRecord`, `DeploymentPhaseEvent`, `EventLogPage` and the rest.
- **What remains.** 150 declarations become 45:
  - 8 twins whose shape differs: Selection, Generation, GenerationListing, TestRunRecord, TestRunListing, HostDeployment, UserEnvironmentDeployment, DeploySubmission;
  - Lojix's own records and the decision plane.
- **Bridge (Inference: temporary).** A `carried!` macro implements Lojix's `Payload` trait on the generated newtypes, so existing `::new` and `.payload()` call sites keep working. Step 8 can drop it.
- **adapters.rs.** It goes from 1014 lines to 341, and from 139 conversion impls and macro invocations to 11 impls. What is left:
  - the ingress lowering and egress raising;
  - Selection;
  - the deploy submission, with its Horizon definition inside;
  - the canonical-path projections of Generation and test runs.
- **Integers are the contract's `i64` throughout.** The identifier allocator refuses past `i64::MAX`. The engine's `u64` commit sequence is refused past `i64` rather than wrapped (`ContractCommitSequence`).
  - **Behaviour change.** A negative identifier on the wire now reaches the engine and is answered as unknown, where the seam used to refuse the frame. The adapter test says so.
- **A record of Lojix's own (Observed, forced).** `impl EngineRecord for DeploymentRecord` is now an orphan, because both the trait and the type are foreign. So the store keeps `StoredDeploymentRecord { DeploymentRecord }`, a record of Lojix's own, already in step 6.
- **Field names follow the generated ones** across the code: `x_option`, `database_marker` and the rest.
- UPGRADES and ARCHITECTURE are updated.

**Byte proof (Observed).**
- **0.10.6 records frozen.** `tests/frozen/v0_10_6.rs` copies the stored closure of da0ad8a's `runtime_model.rs` verbatim.
- **Representation tests.** `tests/memory_representation.rs` checks every family, both ways. Bytes are equal, 0.10.6 bytes read as the current value, and current bytes read as the 0.10.6 value. Values have every option set:
  - live generation and GC root;
  - all three logged events;
  - container record;
  - two deploy jobs, Host with a hosted-pair Horizon definition, and UserEnvironment;
  - test run, `StoredDeploymentRecord` against the 0.10.6 `DeploymentRecord`, identifier allocation, outbox row and transition intent.
- **Enumerations.** All 22 stored enumerations are checked variant by variant, including `DeploymentPhase` against both 0.10.6 `DeploymentPhase` and `DeploymentLifecycle`, and every data-carrying variant.
- **Fixtures.** `tests/store_fixture_rows.rs` reads every row of every family raw, decodes it, re-archives it and requires its own bytes back.
  - It printed the same rows and per-family digests under 26caf36 and under step 6, for all three fixtures (`$S/s67/fixture-rows-26caf36.log` and `$S/s67/fixture-rows-step6.log`).
  - The only difference is the quarantined row's digest. That row's `decode_error` text holds heap addresses that vary from run to run; its archive sha is identical (`a869026f…`).

## Step 7 (7f218c1): Lojix's own memory.ethos

**What changed (Observed).**
- **The Memory.** `ethos/memory.ethos` (59 lines) generates `src/memory.rs`, with 34 types, using ethos-zero 29 f23eacf. `build.rs` now checks both generated files fresh: "src/memory.rs is stale; regenerate it from ethos/memory.ethos".
- **Contract types held whole** inside records of Lojix's own:
  - `StoredDeploymentRecord.{ DeploymentRecord }`;
  - `StoredTestRun.{ TestRunRecord }`, which also retires the hand TestRunRecord and TestRunListing twins, with the canonical-path filter moved to the ordinary egress;
  - `DeployJob`'s `Option<ActualizedDeploySubmission>`, with the Horizon definition, pinned horizon-lib, beside the deployment.
- **In-place heads** name the positions that had no type of their own: RequestedReference, ResolvedReference, ResolvedRevision, BootOnceUnit, FlakeInputName, FlakeInputUrl, NixArchiveHash, and the three `Next…` allocator integers.
- **Still hand-written:** LojixRecord and EngineRecord, keys, family names, schema hashes, and the schema version, which stays 5.
- **runtime_model.rs** goes from 45 declarations to 20:
  - 6 twins: Selection, Generation, GenerationListing, HostDeployment, UserEnvironmentDeployment, DeploySubmission;
  - 14 decision-plane types.
- **adapters.rs** keeps 11 impls. The submission conversions are now `From` both ways, because a deploy job stores the contract's form.
- **The deploy-job upgrade.** The family's schema hash moves from `[5; 32]` to `[14; 32]`. memory-engine's `upgrade_table` converts every row, in one write, from the 0.10.6 layout frozen in `src/upgrade.rs` (`EarlierDeployJob`, with `UpgradeFrom`). Startup logs `FamilyUpgraded.{ deploy-job <rows> }`.
- **The quarantine retires.**
  - A row no record reads refuses the store, naming its table and key (`Error::UndecodableRow`). The startup probe leaves the file untouched.
  - The open drops 0.10.6's `quarantined-row` rows in one commit and logs `QuarantinedRowDropped.{ <table> <key> «<error>» }` for each. The family keeps its 0.10.6 identity.
  - The quarantine-only configuration rebuild is gone.
- **The inspector** reports a deploy-job family still in the 0.10.6 layout as `upgrades-on-open`.
- **The reset catalog** accepts the deploy-job family under either hash.
- **Version** 0.11.0 on every crate, because the store format changed. UPGRADES has a `0.10.6 to 0.11.0` entry that folds in the unreleased 0.10.7. ARCHITECTURE is updated.

**Byte and upgrade proof (Observed).**
- **Every family except the deploy job** still archives as 0.10.6 wrote it, both ways, and that now includes the configuration record.
- **The deploy job, three ways:**
  - `EarlierDeployJob` is byte-equal both ways to 0.10.6's `DeployJob`;
  - a 0.10.6 deploy job, read and upgraded, equals a hand-built current job, Horizon definition beside, and round-trips;
  - 0.10.6 bytes do not read as the current job without the upgrade.
- **The new fixture.** `tests/fixtures/lojix-0.10.6-deploy-jobs.memory` (548 KiB) was written by 0.10.6 itself: da0ad8a on the builder, through `SchemaRuntime::submit_deploy`. It holds a Horizon-mode Host deploy with a hosted pair and a builder, and a Direct user-environment deploy. Generator: `$S/s67/fixturegen/`.
  - On open: `upgraded_deploy_jobs = Some(2)`. The Host job carries its Horizon definition beside it; the user job carries none.
  - Every other family's row digests are unchanged.
  - A reopen upgrades nothing.

**The three original fixtures (Observed).**

| fixture | step 6 | step 7 |
|---|---|---|
| pre-Nexus v5 | every row reads to its own bytes | the same |
| Horizon 0.12 deploy job | opens, `deploy-job 1` set aside | refused: `UndecodableRow deploy-job 1`; the file is byte-equal after |
| 8.1.0 sema | converts, its deploy job set aside | conversion refused at `VerifyingConvertedCopy`; `lojix.sema` untouched, no `lojix.memory` |

## A/B over a fresh copy of the live store

**The copy (Observed).**
- I copied `/var/lib/lojix/lojix.memory` as root through `ssh root@localhost`. The source before, the copy and the source after all hash `ead29c24…`.
- `lojix.service`, pid 1637 since 11-11, was not touched. Proof: `$S/s67/ab/copy-proof.txt`.
- I repaired the copy once with the redb probe, giving R, `879733a4…`. R holds 199 live generations, 2026 events, 580 deployment records, an empty deploy-job family and 4 quarantined rows.

**The runs.**
- Each daemon served its own copy of R under the step-5 bubblewrap harness, with the same 26 inputs (29 requests, counting the Unwatch each watch sends): `$S/s67/ab/inputs.txt`, `tools/session.sh`.
- Transcripts are in `$S/s67/ab/{A,B6,B7,RB6,RB7}/`.

| run | binary | replies | daemon log | final store |
|---|---|---|---|---|
| A | 26caf36, `/nix/store/627p0x0q…-lojix-0.10.7` | reference | two `DeploymentWatchEnded` | `21f9d54b…` |
| B6 | bde7b0e, `/nix/store/sglvcchak…-lojix-0.10.7` | byte-equal to A | the same | `21f9d54b…`, byte-equal to A |
| B7 | 7f218c1, `/nix/store/2fgqi02b…-lojix-0.11.0` | equal to A after the marker `{ 14030 14030 }` is read as `{ 14029 14029 }` (20 lines) | `FamilyUpgraded.{ deploy-job 0 }`, four `QuarantinedRowDropped.{ deploy-job 124/38/46/50 «…» }`, the two watch ends | `82f8b219…` |

**Why B7's marker is one higher (Inference).** B7's open made one more commit than A's: the drop of the four set-aside rows. The marker is the same at its first and last query, so nothing else wrote.

**An equal read after (Observed).**
- `store_fixture_rows`' ignored `a_store_copy_reads_row_for_row` read R and repaired copies of A, B6 and B7 with step-7 code. Every row of every family read back to its own bytes.
- The per-family digests of R, A, B6 and B7 are identical in every family except `quarantined-row`, which is 4 rows in R, A and B6 and 0 in B7.
- R lists the same rows and digests under 26caf36's types. Listings: `$S/s67/ab/listing-step7.txt` and `listing-26caf36.txt`.
- I deleted every store copy afterwards, here and on the builder. Hashes: `$S/s67/ab/hashes.txt`.

## Rollback finding (Observed)

- **0.10.6 onto a store step 6 served:** it starts and answers. The run is RB6, using `/nix/store/m8gfpy8i…-lojix-0.10.6`, the running release. Queries and Pin are answered at marker `{ 14029 14029 }`.
- **0.10.6 onto a store step 7 served:** it is refused at startup, in RB7:

  > `registering deploy-job table … table deploy-job is registered as DeployJobFamily@0e0e…, not as the declared DeployJobFamily@0505…`

  The file is byte-equal after (`82f8b219…`), because 0.10.6 refuses on its probe copy.
- **The cause.** The upgrade moves the deploy-job family's schema hash even when the family is empty, as it is on ouranos. memory-engine admits only forward edges, so no 0.10.6 open accepts the store again.
- **What rollback then needs.** One of:
  - (a) the copy of `lojix.memory` taken just before 0.11.0 first opens it. Anything written after that copy is lost on restore.
  - (b) a downgrade tool, which does not exist. It would re-register `deploy-job` at `[5; 32]` with its rows converted back. memory-engine has no downgrade, and the schema hash is stamped into the versioned log, so this means hand-editing the engine catalog. I would not build it without a ruling.

## Needs a ruling

1. **Configuration record shape.**
   - Ethos-zero's Memory derives Datom under the library's `datom` feature. Lojix's offline tools turn that feature on by default, and `nexus::ConfigurationState` has no Datom form. With `NexusConfigurationRecord.{ Configuration.ConfigurationState<LojixNexusConfiguration> }` (Orchestrate's shape) the library does not compile (Observed).
   - What I did: I declared its two positions as `{ LojixNexusConfiguration MetaConfigureOccurred }`, byte-equal to 0.10.6, with `From` both ways to `ConfigurationState`.
   - The choices are: accept this until the tools leave the library (step 11); give nexus an optional Datom form; or put the Memory in a crate of its own with no `datom` feature.
2. **What an undecodable row does once quarantine retires.**
   - My reading of "upgraded, never accommodated" is a named refusal.
   - Consequence: a store holding a Horizon 0.12 deploy job is refused, and so is a converted Lojix 8.1.0 store holding one, which is the only sema fixture. The conversion's success path therefore has no fixture left; both of its tests now assert the refusal.
   - **Inference:** no live 8.1.0 store remains, since ouranos is on 0.10.6.
   - The alternative is that the sema conversion, itself an upgrade, drops and reports deploy jobs of a layout nothing reads.
3. **Rollback** as above: restore the pre-switch copy, or build a downgrade tool.
4. **Negative identifiers** now reach the engine (step 6) and are answered as unknown.

## Notes

- **The orphan rule forced the stored-record wrapper into step 6.** Step 7 then generated it.
- **The Horizon 0.12 fixture never reaches the upgrade.** It has no `__memory_engine_catalog` table, so the deploy-job family registers as new and the named-row refusal stops it (Observed with a probe).
- **Builder copies.** The 26caf36 and da0ad8a source trees are at `/tmp/offload/lojix-26caf36` and `/tmp/offload/lojix-da0ad8a`. Logs and scripts are under `$S/s67/`.
- **This report is not committed** to primary, like the step 1–5 reports beside it.
