# Lojix — the anatomy behind the no-inherent-methods law

Carried account of the one item `reports/lojix-work.md` §W9 left open: the
`no-inherent-methods` law was written as a script but neither passed nor
enforced, because two God-objects — `impl Store` and
`impl SchemaRuntime` — could not be made to pass it honestly. Counted here,
those two blocks held **75** and **101** methods; §W9 reported 77 and 97. The
discrepancy was not chased: both counts agree that each block is far past the
size at which a single trait would be a namespace wearing a trait's clothes.
Done 2026-09-12 by subflow thread `f6db8d14-1dfe-472d-914e-9c441f852834` of
flow f6db8d, under the living's standing order for autonomous work with no
questions, holding Orchestrate lock **1226** `LojixAnatomy`.

Throughout: **witnessed** = this subflow ran the command or opened the file and
the result is quoted or summarised below; **relayed** = another flow's report
says so and is named. Nothing was deployed. The running Lojix service, its
sockets and its store were not touched. CriomOS and CriomOS-home were not
touched. All work was done in a clean clone of `main` at
`/home/li/wt/github.com/LiGoldragon/lojix/lojix-anatomy-f6db8d`, not in the
shared checkout under the Repository root.

---

## 1. Released revision

| Repository | Version | Revision |
|---|---|---|
| `lojix` | 6.0.0 | `c4bba4fa12408c39ff745b0773468cd32a74403f` |

Predecessor: `lojix` 5.0.0 `b5cddd2e16ad49d1060cf4109f44c27359195441`
(`reports/lojix-honesty.md`).

**No producer moved.** `signal-lojix` 5.0.0 `4271b5ce…` and
`meta-signal-lojix` 6.0.0 `35deec4e…` are the same pins as 5.0.0; lojix built
against them without change, so nothing was repinned. A sibling flow
reintroducing arity in `datom-codec` is not touched here. The store schema is
still v4 and no request or reply gained or lost a word: this release is
breaking in the Rust API and in nothing else.

---

## 2. What the law is, and why grep-satisfaction would have broken it

The `nexus` skill's law: *"Every method call lives in a trait. An inherent
method is a trait not yet extracted — a concept hiding in a name."* And, in the
same skill: *"One type implementing many single-function traits is one trait not
yet seen."* The two pull against each other, and the pull is the whole design
problem. A hundred-method trait passes the script and violates the
law; a hundred one-method traits pass both scripts and violate the second
sentence.

`reports/lojix-work.md` §W9 proposed nine traits for `Store` and ten for
`SchemaRuntime`, derived by grouping method *names*. That decomposition was not
used. It answers "which of these method names look alike", and the question the
law asks is "what is this type, what is it asked for, and why". Asking the
second question moved a third of `SchemaRuntime`'s methods off `SchemaRuntime`
altogether and deleted thirteen of `Store`'s.

### The three findings that shaped it

**A family is a parameter, not a method.** `Store` had eleven readers —
`live_generations`, `gc_root_records`, `event_log_entries`,
`container_lifecycle_records`, `deployment_records_unchecked`,
`identifier_allocations`, `deployment_outbox_records`,
`pending_transition_intents`, `nexus_configuration_records`, `test_runs`,
`deploy_jobs` — with byte-identical bodies apart from one field name. Beside
them sat eleven twelve-line `register_table` blocks, eleven startup validators,
thirty-three module constants spelling table name, family name and schema hash
in three parallel lists, a second struct (`LojixDirectory`) repeating all eleven
table references, a third copy of those eleven inside `resume_compaction`, and —
in a different module — eight more constants naming the same tables again for
the read-only inspector. Six copies of one list.

The kind hiding there is **the record kind itself**. `LojixRecord` now carries
`TABLE`, `FAMILY`, `SCHEMA_HASH` and `ROLE` per record type and says where its
rows live in an open store; `DurableStore::records::<R>()` is the one reader;
`LojixDirectory::register` is the one registration. The eight inspection
constants and the whole `TableInspectionTarget<RecordValue>` type are gone, and
`reconstruction.rs`'s two catalog layouts are eleven calls to
`LojixRecord::family_identity` instead of eleven hand-typed triples.

**Most of Nexus Core's methods were verbs of their arguments.** Of
`SchemaRuntime`'s 101, twenty-four took a value and returned a projection of it
and never touched `self`: five `*_reason` conversions from one store rejection
into each meta verb's vocabulary, `terminal_reason`, two effect-stage
classifications, `deployment_lifecycle`, `activation_slot`, three `*_matches`
selection predicates, five deploy-request admission judgements, two marker
constructors, two configuration receipts and `reply_meta`. They are now
`RejectionVocabulary` on `RejectionReason`, `TerminalReason` on
`DeployRejectionReason`, `FailureStaging` on `EffectStage`, `PhaseLifecycle` on
`DeploymentPhase`, `ActivationSlot` on `ActivationEffect`, `TestRunSelecting` on
`TestRunLookup`, `GenerationSelecting` on `Selection`, `DeployAdmission` on
`DeployRequest`, and five `From` impls. **A deploy request now judges itself**,
which is the honest shape: nothing about the store or the pipeline participates
in deciding whether a request is admissible.

**Seven types were already one kind.** `NixCommand`, `ClosureCopy`,
`Activation`, `HostActivation`, `UserEnvironmentActivation`, `HermeticCheck` and
`HorizonMaterialization` each had `async fn run(&self, execution:
&EffectExecution) -> Result<Product, StageFailure>`. That is one trait —
`Effect`, with an associated `Product` — and writing it that way is what turned
up the one signature that did not fit: `HorizonMaterialization::run` took no
execution and reached into its own configuration for one. It now takes it like
every other effect.

---

## 3. The decomposition, as landed

### `Store` — seven ledgers over one record vocabulary

| Trait | Methods | What it is asked |
|---|---|---|
| `LojixRecord` (on the 11 record types) | 4 consts, 1 required fn, 3 defaults | Where this family lives, what it is called, how it registers |
| `DurableStore` | 5 | Where the store is, how far its write counter has run, every row of one family |
| `StoreIntegrity` (`pub(crate)`) | 4 | The write gate, the startup decode gate, resumed compaction |
| `NexusPersistable` | 7 | The Nexus's durable configuration and its two socket-scoped mutations |
| `IdentifierAllocating` | 7 | The durable high-water row |
| `TransitionJournal` | 14 | Exactly-once delivery of a durable transition |
| `EventHistory` | 5 | The bounded historical plane and its retention |
| `DeploymentLedger` | 14 | The durable life of one deployment, job row included |
| `GenerationLedger` | 6 | What is installed on a node and what keeps it alive |
| `TestRunLedger` | 1 | The durable record of a test run |

`TestRunLedger` has one method and is noted as an exception to "prefer fewer
kinds": its reads went to `records::<StoredTestRun>()` and its identifier to
`IdentifierAllocating`, leaving one verb. Folding it into `DeploymentLedger`
would say a test run is a deployment, which it is not.

Thirteen of `Store`'s 75 methods were deleted outright rather than rehomed: the
eight private family readers, the two public readers whose whole body was one
`match_records` call (`test_runs`, `pending_transition_intents`), and the three
public aliases (`gc_roots`, `deployment_records`, `deployment_outbox`) that
forwarded to the private ones. The remaining 62 are the 63 trait methods above
minus `records`, which is new.

### `SchemaRuntime` — seven questions

| Trait | Methods | What it is asked |
|---|---|---|
| `RuntimeCore` | 7 | How an engine is made, what it sits on, how an action runs to a reply |
| `SignalDeciding` (`pub(crate)`) | 17 | What to do with an arriving signal or a completed step |
| `DeployDriving` | 17 | Driving one deployment from handle to terminal record |
| `TestDriving` | 6 | Driving one test run to a verdict |
| `SemaApplying` (`pub(crate)`) | 14 | Applying one decided write |
| `SemaObserving` (`pub(crate)`) | 5 | Answering one decided read |
| `EffectRunning` (`pub(crate)`) | 11 | Running one decided effect and reporting what came back |

101 → 77 methods on the type, in seven traits, none larger than seventeen.

### The other 65 blocks

Each became one trait named for the question its type answers —
`BootstrapJournalling` (21), `NixInvoking` (17 after `run` moved to `Effect`),
`HostActivating` (16), `DeployCursor` (21), `UserEnvironmentActivating` (11),
`DetachedActivation` (11), and the rest between one and nine — except where the
honest answer was something other than a new trait:

- **`Payload`**, one trait for every newtype in the crate. The four
  `flow_newtype!`/`flow_text!`/`runtime_newtype!`/`runtime_text!` macros emitted
  four identical `impl $name { new, payload, into_payload }` blocks; `OriginRoute`
  and `EventLogRetention` had hand-written copies. One trait clears all six.
- **`Named`**, for the four types whose only question was their one text form.
- **`OfflineCommand`**, for `StoreInspectionCommand` and `StoreResetCommand` —
  two shapes of one kind (read the process's one inline Datom argument, then do
  the thing), with `from_environment` as a trait default.
- **`From`**, where the method was a conversion and nothing else:
  `JournalStage::from_effect`/`effect`, `EffectResult`'s four constructors,
  `HorizonUserName::try_new`, `SchemaRuntime::marker`/`sema_marker` (a
  `From<u64> for StateMarker` already existed beside them),
  `configuration_receipt`, `configuration_rejection`, `reply_meta`.
- **Public fields**, where the type was a report rather than an actor.
  `StoreInspection` and `TableInspection` are what a read-only inspection
  *found*. Eight accessors returned a private field and nothing else; the
  fields are public now and the accessors are gone, three of them (`catalog`,
  `tables`, `role`) having had no caller at all. Only `table_named` remained a
  verb, on `InspectedTables`.

---

## 4. What decomposition revealed as dead, and was deleted

Every removal below was checked by a repository-wide grep including `tests/`
before it was made.

- **The effect barrier, entire.** `EffectBarrier`, its semaphore,
  `RuntimeConfiguration::test_with_effect_barrier`, the `effect_barrier: Option<…>`
  field, and the `if let Some(barrier) = … { barrier.wait().await }` in front of
  the pipeline's first effect. It existed for the up9b decoupling witness — a
  test that proved the daemon replies the accepted handle while the pipeline is
  still parked. **Nothing constructs a barrier any more**: the only producer was
  `test_with_effect_barrier`, which has no caller anywhere in the workspace. The
  option was always `None` and the branch was never taken. This was invisible
  while the methods were inherent on a 9-method impl block; naming the trait
  `EffectGating` and asking who gates made it obvious.
- **`impl NexusPersistable for Store`**, five methods forwarding to five
  identically named inherent methods. The trait existed, the impl existed, and
  the impl called the inherent copy. The bodies moved into the trait impl.
- **`Nexus::root()`**, `StoreInspection::catalog()`, `StoreInspection::tables()`,
  `TableInspection::role()` — no callers.
- **`NexusWork::sema_write_completed`, `sema_read_completed`, `effect_completed`,
  `NexusAction::reply_to_signal`** — one-line functions wrapping one enum variant
  each. The variant is the constructor.
- **Ten `Store` family readers** and their three public aliases, superseded by
  `records::<R>()`. `deploy_jobs` survived because reading it validates the
  persisted closure path.
- **Thirty-three table constants**, eleven registration blocks, eleven startup
  validators, the eleven-field copy inside `resume_compaction`, the eight
  inspection-target constants and `TableInspectionTarget<RecordValue>` — all
  superseded by `LojixRecord`.

---

## 5. Line counts

Production Rust only (`src`, `nexus/src`, `clients/*/src`, `tools/src`), by
`wc -l`, witnessed at both revisions.

| File | 5.0.0 | 6.0.0 | Δ |
|---|---:|---:|---:|
| `src/schema_runtime.rs` | 8768 | 9771 | +1003 |
| `src/lib.rs` | 3493 | 3752 | +259 |
| `src/bootstrap.rs` | 2842 | 2979 | +137 |
| `src/daemon.rs` | 1304 | 1351 | +47 |
| `src/runtime_model.rs` | 990 | 1003 | +13 |
| `src/adapters.rs` | 955 | 956 | +1 |
| `src/reconstruction.rs` | 651 | 625 | −26 |
| `src/inspection.rs` | 553 | 516 | −37 |
| `src/runtime_flow.rs` | 551 | 575 | +24 |
| `clients/meta/src/lib.rs` | 300 | 300 | 0 |
| `src/inspected_text.rs` | 272 | 272 | 0 |
| `src/ingress.rs` | 225 | 225 | 0 |
| `tools/src/lojix-write-configuration.rs` | 204 | 204 | 0 |
| `clients/ordinary/src/lib.rs` | 92 | 92 | 0 |
| `tools/src/lojix-migrate-configuration.rs` | 62 | 62 | 0 |
| `src/client.rs` | 32 | 41 | +9 |
| the six binaries | 95 | 99 | +4 |
| **total** | **21388** | **22821** | **+1433** |

Bare `impl Type { … }` blocks in production Rust: **67 → 0**.
Traits in production Rust: **63 → 141**.
Diff across the whole repository: 37 files, 5249 insertions, 3595 deletions.

**The file grew, and this is the honest result, not a failure to simplify.**
A trait states each method twice — once as specification, once as body — and 67
impl blocks carrying several hundred methods therefore cost several hundred
signature lines that an inherent block does not. Against that, on the order of 600 lines
of genuine duplication and dead code were deleted (§4): thirty-three constants
and their comments, eleven twelve-line registration blocks, the eleven-field
copy inside `resume_compaction`, eleven readers, eleven validators, the eight
inspection constants and `TableInspectionTarget`, the two hand-typed catalog
layouts, the barrier, the forwarding `NexusPersistable` impl, four dead
accessors and four variant wrappers. Where the law and "less
code" pointed the same way — the eleven readers, the six copies of the table
list, the barrier — the code shrank; `src/inspection.rs` and
`src/reconstruction.rs` are the two files where that dominated, and they are the
two files that got smaller. Where the law asks for a specification the code did
not have, it grew. The brief asked for less code; what it got is less *duplicated*
code and more *stated* code, and the statement is the thing the law is for.

---

## 6. Enforcement

`flake.nix` gained:

```nix
no-inherent-methods =
  pkgs.runCommand "lojix-no-inherent-methods" { src = lawSource; }
    (builtins.readFile ./checks/no-inherent-methods.sh);
```

beside the `no-free-functions` check it already had, over the same `lawSource`
(every `.rs` and `.sh` in the tree, because crane's `source` filter excludes
shell scripts).

**Seen failing once before being trusted.** A four-line
`struct ADeliberateViolation; impl ADeliberateViolation { fn a_deliberate_inherent_method(&self) {} }`
was appended to `src/client.rs` and committed (the flake source is the tracked
tree). `nix build .#checks.x86_64-linux.no-inherent-methods` failed, exit 1,
printing:

```
> /nix/store/0vsljw0sn96pj5znn904cn3jnfy4rsgw-source/src/client.rs:45:impl ADeliberateViolation {
> production Rust must home behavior in traits
```

The witness commit was abandoned and the same build then succeeded, together
with `no-free-functions`.

No behavioural change was made that a test could witness, so no new test was
written: this is a relocation of method bodies into traits, and the existing
suite is the witness that the relocation preserved behaviour. The two changes
that are not pure relocation are covered by existing tests —
`tests/store_startup_gate.rs` asserts the startup stage string that the
`LojixRecord` collapse now formats (`"validating live-set rows"`, unchanged for
that family), and the whole suite exercises `records::<R>()` in place of the
eleven deleted readers. The one deliberate message change is recorded in
UPGRADES.md: two single-row families now say "rows" like every other family.

---

## 7. Gate

Local, on the exact released tree:

| Command | Result |
|---|---|
| `cargo build --workspace --all-targets` | clean, no warnings |
| `cargo test --workspace` | all green, 0 failures |
| `cargo clippy --workspace --all-targets -- -D warnings` | clean |
| `cargo fmt --all` | applied, idempotent |
| `cargo doc --workspace --no-deps` | no new warnings |

`nix flake check -L` ran all fourteen checks the flake declares —
`build`, `nexus-binary`, `test`, `deploy-honesty`, `failure-evidence`,
`fresh-daemon-startup`, `nexus-startup-rejects-arguments`,
`bootstrap-rejects-flags`, `fmt`, `clippy`, `no-free-functions`,
**`no-inherent-methods`**, and both NixOS VM tests
(`retained-transient-semantics` and `same-host-test-activation`, which actually
boot a guest) — and printed **all checks passed!**, on Prometheus. The five
released commits are `c566625c` (`Payload`), `19b7e9cc` (the store's record
kinds and ledgers), `1c799aec` (the schema-runtime nouns), `9170f1d3` (Nexus
Core), `d57a8861` (the readiness announcement) and `c4bba4fa` (its upgrade
note). `git ls-remote origin main` answers `c4bba4fa1240…` after the push.

**A note on the remote builder, because it cost this flow half an hour.**
Prometheus is already the system's configured builder — `/etc/nix/machines`
holds `ssh-ng://nix-ssh@prometheus.goldragon.criome x86_64-linux … big-parallel,kvm,nixos-test`
— so plain `nix flake check -L` routes there by itself, and `max-jobs = 1`
locally means it mostly must. Passing
`--builders 'ssh://prometheus x86_64-linux'` **overrides** that machines file
with a worse route: `prometheus` is an alias in the user's `~/.ssh/config`, and
the Nix daemon runs as root and does not read it, so the build printed
`cannot build on 'ssh://prometheus': … Could not resolve hostname prometheus`
and silently fell back to building everything locally. The lesson, confirmed by
the main flow: do not pass `--builders` at all; if an override is unavoidable
it must be `ssh-ng://nix-ssh@prometheus.goldragon.criome`, and `--max-jobs 0`
forces the remote. The earlier `--builders ''` in `reports/lojix-work.md` was
forcing every VM test onto this machine for the same reason.

---

## 8. What remains

- **`DeploymentPipeline::phase_event`'s `_detail: Option<String>`** is still
  discarded, as `reports/lojix-work.md` recorded. Untouched here.
- **`CopyClosure` still maps to `BuilderUnreachable`**, as recorded there.
  Untouched here.
- **The `lojix` skill's `CheckHostKeyMaterial` row** is still wrong, and the
  skill does not yet name the traits a Rust consumer must import. Skill edits
  need the living's explicit approval after proposal (W2's standing condition),
  so this is an addition to W2's proposal, not an edit.
- **Three `#[allow(async_fn_in_trait)]`** on `RuntimeCore`, `DeployDriving` and
  `TestDriving`, each with a comment at the site saying why: the trait is
  implemented by exactly one type, is never used behind `dyn`, and its futures
  are awaited on the task that created the engine, so there is no `Send` bound
  for a caller to name. The alternative — hand-written
  `-> impl Future<Output = T> + Send` with `async move` bodies — would be
  thirty lines of ceremony for a bound nobody needs. If a second implementor
  ever appears, this is the first thing to revisit.
- **`checks/no-free-functions.sh` and `checks/no-inherent-methods.sh` are
  column-anchored**, so a free function or an inherent impl nested inside a
  private `mod` is not seen. This limitation is inherited from the authored
  `signal-lojix` and `horizon-rs` scripts and is unchanged. The two such modules
  in `schema_runtime.rs` (`mod ordinary`, `mod meta`) contain only `pub use` and
  `pub type` and were read by hand.
- **The shared checkout at `/git/github.com/LiGoldragon/lojix` is at 4.0.1**
  (`0bb3d66c`, a stale `main` with an empty commit on top), two releases behind
  the remote. It was not touched. Whoever next works there must fetch first.

## Sources

- `flows/f6db8d/reports/lojix-work.md` §W9 — the open item, the 67-block
  survey, and the nine/ten-trait proposal this flow read and did not use, with
  the reason recorded in §2 above.
- `flows/f6db8d/reports/lojix-honesty.md` §1 — the 5.0.0 baseline revision and
  the producer pins that did not move.
- The `nexus` skill — "Traits first", "No free functions", "One type
  implementing many single-function traits is one trait not yet seen", and the
  instruction that each exception is noted at its site.
- `Vision/nexus.md` — "Universal traits first"; "Processing is for the effect …
  the name is open, Apply liked", which named `SemaApplying`.
- The `spirit` skill — "Backward compatibility is never a design variable",
  which grounds the deletions in §4; "Name what a thing is, what is wanted from
  it, and why", which is the question each trait doc answers.
- The `testing` skill — "A new test is seen failing once before it is trusted",
  applied in §6 to the check itself.
- Witnessed directly in this subflow: the `lojix` working tree at
  `b5cddd2e` and at every commit since; `cargo build`, `cargo test`,
  `cargo clippy -- -D warnings`, `cargo fmt`, `cargo doc`, `nix build` and
  `nix flake check` output as cited.
