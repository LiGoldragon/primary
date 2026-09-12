# Lojix — W3, W8, W9, W10 executed

Carried account of work items W3, W8, W9 and the unblocked parts of W10 from
`reports/lojix-history.md`, done 2026-09-11 by subflow thread
`f6db8d14-1dfe-472d-914e-9c441f852834` of flow f6db8d, under the living's
standing order for autonomous work with no questions.

Throughout: **witnessed** = this flow ran the command or opened the file;
**relayed** = a subflow of this flow reported it and is named. Nothing was
deployed. The running Lojix service, its socket and its store were not touched.
CriomOS and CriomOS-home were not touched.

---

## Released revisions

Producers before consumers, each gate green before the next repository pinned
it.

| Repository | Version | Revision |
|---|---|---|
| `horizon-rs` | `horizon-lib` / `horizon-cli` 0.10.0 | `a56330451934d682ae15612acd49924356ec0205` |
| `signal-lojix` | 4.1.0 | `d0f5c70d437add1df16055dcb760b7ef9a140ef0` |
| `meta-signal-lojix` | 5.1.0 | `1eccc0e3d314a5d92c741959a698697c37ec0eac` |
| `lojix` | 4.0.0 | `8cb12b8d9c3864813cf54619597ea8e734b2e99f` |

`signal-lojix` and `meta-signal-lojix` each carry two commits: the contract
change, then the horizon-lib repin. The intermediate versions (signal-lojix
3.0.0 and 4.0.0, meta-signal-lojix 4.0.0 and 5.0.0) are pushed and superseded;
§W3 explains why the shape was corrected after the first push.

---

## W3 — actionable failure evidence in the durable record

Open bead `primary-cod` (P1) carried the design and the acceptance criteria;
they were used rather than new ones invented.

### What was wrong

Witnessed at `lojix/src/schema_runtime.rs`: `NixCommand::run` captured the
child's stderr, formatted it into a `String`, and handed it to `EffectFailure
{ effect_stage, string }`. `fail_pipeline` then `eprintln!`'d the stage,
mapped the stage to one of eleven `DeployRejectionReason` values, and
persisted only stage plus reason. The string died there. Two stages —
`Eval` and `Build` — both mapped to `FlakeReferenceMalformed`, which is true
of neither: a flake that evaluates and then fails to build is not a malformed
reference. Flow 542442 had already witnessed exactly this and recorded it on
the bead.

A second, independent loss: the detached-activation observer at
`DetachedActivationUnit::classify` read systemd's `ActiveState` and the
service `Result`, printed both to the journal, and returned a payload-less
`DetachedActivationOutcome::Failed`.

A third: `DeploymentPipeline::phase_event` takes `_detail: Option<String>`
and discards it. That one is left in place — see §Not done.

### The contract

`signal-lojix`'s `DeploymentFailure` gained a third field. Final shape:

```
DeploymentFailure.{ DeploymentFailureStage DeploymentTerminalReason Option<FailureEvidence> }
FailureEvidence.{ Option<FailedCommand> FailureDetail DetailTruncated }
FailedCommand.{ CommandProgram Vector<CommandArgument> Option<ExitCode> }
```

`DeploymentTerminalReason` gained `EvaluationFailed` and `BuildFailed`.

The first push (signal-lojix 3.0.0) had the command's program, arguments and
exit code flat inside `FailureEvidence`, non-optional. That was wrong: a stage
that fails without running a subprocess — a Horizon projection, an internal
invariant — has detail worth keeping and no program to name, and would have
had to write an empty string. The shape was corrected in 4.0.0 and the extra
release taken rather than shipping a type that must lie. The living was not
asked; the brief ordered decisions to be made and recorded.

`meta-signal-lojix` declares no type of its own here — `DeployTerminal`
carries `signal-lojix`'s `DeploymentRecord` — but its wire changes with the
ordinary one, so it was bumped and repinned.

### The producer

In `lojix`:

- `StageFailure` is now the single carrier every effect failure travels in:
  the detail the stage reported, and an optional `FailedCommand`.
  `From<String>` and `From<&str>` cover the no-subprocess cases, so the
  existing `?` chains through `ClosureCopy::run`, `Activation::run`,
  `HermeticCheck::run` and the boot-once path compose unchanged.
- `NixCommand::run` returns `Result<String, StageFailure>` and its failure
  path carries `status.code()` and the real stderr. A process killed by a
  signal reports no code, and `Option<ExitCode>` says so rather than
  inventing one.
- The `Witnessing` trait turns a reported failure into durable evidence:
  every line containing a credential term is dropped (reusing the existing
  credential vocabulary — `token`, `secret`, `password`, `passwd`,
  `credential`, `apikey`, `api-key`, `api_key`, `auth`), then the last
  4 KiB survive on a line boundary. `detail_truncated` is true whenever
  either step removed anything.
- `EffectFailure` carries `failure_evidence` instead of `string`.
- `fail_pipeline` persists the evidence into the terminal and maps `Eval` and
  `Build` to their own reasons.
- `DetachedActivationOutcome::Failed` carries a `DetachedActivationFailure`
  with systemd's `ActiveState`, `Result`, and `ExecMainStatus`, and both of
  its terminalization sites (`SchemaRuntime::terminal_outcome` and
  `daemon.rs`'s observer) persist it.

The event log needed no new write: `Store::terminalize_deployment` already
routes through `complete_pending_transition_intent`, whose journalled
`DeploymentPhaseEvent` carries `optional_deployment_terminal`. The evidence
rides inside that terminal, so `Query.ByEventLog` returns it. The bead's
observation that the event log was empty for deployment 190 was against
0.20.3 and no longer holds.

### The witness

`lojix/tests/failure_evidence.rs`, six tests, driving the same submit/drive
pipeline the daemon's job actor drives against hermetic fake `nix` and `ssh`
programs. The fake `ssh` fails its activation step with exit 42 and a
three-line stderr, one line of which is a credential.

Each test was **seen failing once** before being trusted: with
`optional_failure_evidence: None` restored in `fail_pipeline` and
`ByDeployment(_) => false` restored in `generation_matches`, five of the six
failed and the sixth — the partial-mutation separation — passed, which is
correct, since it asserts a property that predates this change.

Exposed as the Nix check `failure-evidence` in `lojix/flake.nix`, alongside
the workspace `test` check that already covers it.

### Acceptance criteria

`primary-cod`'s criteria, each against a named test:

| Criterion | Witness |
|---|---|
| failing UserEnvironment activation produces a durable queryable redacted failure record naming the failed command and exit status | `a_failed_activation_names_the_command_and_its_exit_status` |
| redacted | `the_durable_detail_drops_the_credential_line_it_was_printed_beside` |
| event-log query returns it | `the_event_log_carries_the_same_evidence_as_the_record` |
| terminal state remains Failed Activate | asserted in the first test |
| tests witness partial profile mutation separately from runtime activation | `the_profile_advanced_although_the_deployment_failed` |
| the durable Nix check passes | `checks.failure-evidence` |
| UPGRADES.md explains partial-failure reconciliation before retry | `lojix/UPGRADES.md` §3.0.0, four numbered steps |

The bead was closed on this evidence.

---

## W8 — the two one-line truths

**`ByDeployment(_) => false`.** `generation_matches` returned false for every
`ByDeployment` selection, so a documented selector answered with no generation
— the one question an operator asks after a deployment. It now matches
`live.deployment_identifier`. Witness:
`a_by_deployment_query_answers_with_the_generation_it_produced`, seen failing
against the old line.

**`check_key_material`.** Removed, with the whole `CheckHostKeyMaterial`
vocabulary, from `signal-lojix` and from `lojix`.

The decision and its ground: the verb was answered by a stub returning an
empty mismatch vector for every node, and `adapters.rs` raised it with
`key_material_mismatch_vector: Vec::new()` unconditionally — the wire type
could not have carried a mismatch even if one had been computed. Nothing
compared published key material against a live host, and nothing could: the
verb sat on the synchronous store-read path with no effect behind it. A
security check that always answers "no mismatch" is worse than no check,
because an operator can trust it. Under the spirit's "backward compatibility
is never a design variable" the vocabulary was deleted rather than kept as a
parallel dead path.

What a real implementation would need, recorded so it is not re-derived:
Horizon already projects the published side (`horizon-rs/lib/src/model.rs`
`ssh_public_key_line`, `NodeKeys::ssh_pub_key`, `YggdrasilKeyView`), so the
missing half is the live side — an SSH read of the host's actual key material,
which is an effect and therefore needs its own `EffectStage` and pipeline, not
a store read. That is a different contract from the one removed.

**Owed:** the `lojix` skill documents `CheckHostKeyMaterial` under "Ordinary
requests". The skill is now wrong. Skill edits require the living's explicit
approval after proposal (W2's standing condition), so this is not edited here
— it is an addition to W2's proposal.

---

## W9 — the two laws

The laws are the `nexus` skill's: `fn main()` is the only production free
function, and behavior is homed in traits, so a bare `impl Type { … }` is a
trait not yet extracted. `signal-lojix` and `meta-signal-lojix` already enforce
both as Nix checks over their `src/`; `lojix` and `horizon-rs` did not.

The surveyed scale, witnessed by running the two check scripts read-only:
`horizon-rs` 45 free functions and 1 bare impl; `lojix` **100 free functions
and 86 bare impls** — the latter including `impl SchemaRuntime`, with well over
a hundred methods, in an 8670-line file. These are two very different jobs, and
they were treated as such.

### horizon-rs — both checks green (relayed)

Done by a `write-demanding` subflow of this thread, which ran its own gate and
reported it. Released as `horizon-lib`/`horizon-cli` 0.10.0,
`a56330451934d682ae15612acd49924356ec0205`. Its own account:

`lib/src/projection.rs` (1063 lines) became a module directory of files of a
few hundred lines each, and its 45 free functions became eight traits homed on
data-bearing types: `DatomDecoding` (the four `decode*` functions, with their
per-document budgets as associated consts), `Named` (16 enum name functions
collapsed into one trait), `MagnitudeRanking`, `MagnitudeName` on `str`,
`Projection` (the eight context-free projections), `TrustResolving` on
`ClusterTrust`, `NodeCatalogue` on `[NodeDefinition]`, `NodeGraph`,
`MachineProjection`, `NodeProjection`, `NodeDeriving`, `UserProjection`,
`Composing`, `Projecting`.

Two missing types were named rather than worked around: `Viewpoint<'a>` (four
viewpoint facts that were being passed as loose arguments) and
`NodeDefinitions`. No zero-sized namespace type was created. **No exceptions
were taken** and **nothing was deleted as dead** — every free function had a
live caller, checked against lojix's sources before concluding anything `pub`
was live.

Both checks are wired as `checks.<system>.no-free-functions` and
`checks.<system>.no-inherent-methods`, scanning `lib/src` and `cli/src` — the
whole of horizon-rs's production Rust. `no-free-functions.sh` filters out
`fn main(` so the two binary entry points pass; that is the law itself, and the
script carries a comment saying so. Both checks were **seen failing once**
against injected violations before being trusted.

The consumer edits this cost `lojix`, all applied and witnessed compiling here:
`src/bootstrap.rs:22` imports `{DatomDecoding, HorizonDefinition, Projecting}`;
`horizon_lib::decode(x)` becomes `HorizonDefinition::decode(x)` at
`src/bootstrap.rs:839`, `tools/src/lojix-write-configuration.rs`,
`clients/meta/src/lib.rs:99` and `tests/common/mod.rs`;
`src/schema_runtime.rs:20` imports `Projecting`. `signal-lojix` and
`meta-signal-lojix` re-export `HorizonDefinition`, so both were repinned to
0.10.0 before lojix was — producers first.

### lojix — no-free-functions landed and enforced; no-inherent-methods written, not enforced

Done by a `write-demanding` subflow of this thread on branch
`lojix-trait-laws`, as the brief required; its account is relayed, and this
flow witnessed the gate independently before landing it on `main`.

**What landed.** Five commits on top of `48f637e8`, tip
`8cb12b8d9c3864813cf54619597ea8e734b2e99f`, version 3.0.0 → **4.0.0** across
`Cargo.toml`, `nexus/`, `tools/`, `clients/ordinary/`, `clients/meta/`, with a
`## 4.0.0 — behavior is homed on the thing it belongs to` entry in
`UPGRADES.md`. **110 free functions were rehomed**; zero module-level free
functions remain outside `fn main` in the five production directories
(`src`, `nexus/src`, `clients/ordinary/src`, `clients/meta/src`, `tools/src`).

**The check.** `checks/production-rust.sh` is a shared preamble defining
`production_sources()`; `tests/` is not production source and is not scanned.
Its `strip_test_items` awk pass removes each `#[cfg(test)]` **item** whole —
attribute line, then the statement or the brace-balanced block — and resumes
reading production code after it, rather than stopping at the first
`#[cfg(test)]`. That distinction is load-bearing: `src/reconstruction.rs` had a
`#[cfg(test)]` free function at line 260 with 150 lines of production code
after it, and `src/daemon.rs` has production code after its `mod tests` ends.
String and char literals and line comments are blanked before braces are
counted. `flake.nix` gained a `lawSource` (every `.rs` and `.sh`) because
crane's `source` filter excludes shell scripts and would have hidden `checks/`
from the derivation. The check was **seen failing once**: appending
`fn a_deliberate_violation() {}` to `src/client.rs` failed it by file and line.

One carried-over limitation, identical to the authored `signal-lojix` and
`horizon-rs` scripts: `^fn` is column-anchored, so a free function nested
inside a private `mod` would be missed. The two such modules in
`schema_runtime.rs` were read by hand and contain none.

**The two named wins.** `canonical_nix_store_root` (×3) and `credential_like`
(×3 free plus one percent-decoding inherent method) became
`src/inspected_text.rs` — types `NixStorePath`, `InspectedText`,
`PercentEncodedText` bearing traits `StoreItemShape`, `CredentialBearing`,
`PercentDecoding`; the percent-decoding variant is a second `CredentialBearing`
impl rather than a fourth copy. Separately, the 18 identity shims in
`schema_runtime.rs`'s `mod ordinary`/`mod meta` (`pub struct X; impl X { pub fn
new(p: P) -> P { p } }`) were deleted and all 42 call sites unwrapped to the
bare payload, taking both `#[allow(clippy::new_ret_no_self)]` with them.

**Public API moves a consumer must apply** — exactly five `pub fn` removed,
two `pub trait` added, nothing else, diffed across the whole public surface:

| Was | Is | Import |
|---|---|---|
| `lojix::single_inline_datom_argument(arguments)` | `arguments.single_inline_datom()` | `lojix::InlineDatomArguments` |
| `lojix::bootstrap::run_from_environment()` | `BootstrapRun::run_from_environment()` | `lojix::bootstrap::BootstrapInvocation` |
| `lojix::bootstrap::decode_single_inline(args)` | `BootstrapRun::decode_single_inline(args)` | same |
| `lojix::bootstrap::run_with_executor(req, &mut e)` | `req.run_with_executor(&mut e)` | same |
| `lojix::bootstrap::run_with_executor_and_crash(req, &mut e, &mut c)` | `req.run_with_executor_and_crash(&mut e, &mut c)` | same |

No Rust consumer of `lojix` exists outside the workspace — `/git/github.com/LiGoldragon/`
was grepped for `lojix::`/`lojix_lib::`, and CriomOS consumes only the Nix
package and the CLI binaries. Nothing outside `lojix` was edited.

**Exceptions taken**, two, each commented at its site: `nexus/src/main.rs`
keeps the argument guard and the serve call inside `fn main` rather than
growing a floating verb; and the secrets-directory admission at
`schema_runtime.rs` lost its bespoke wording when it moved onto the shared
`OfferedPath::existing_directory`, with a comment recording that it is now held
to the same no-symlink contract as every other lojix path. One behavioural
note that is not an exception: four `BootstrapError::Validation` message
strings changed wording, because the shared `PathFault` has one `WrongKind`
variant. Nothing asserts on those strings.

**What was deleted as dead** — all private, each verified by a repo-wide grep
including `tests/` before removal: the 18 shims; `bootstrap::ingress_text` and
`lojix-write-configuration`'s `text` (identity functions, inlined); the
duplicate `canonical_nix_store_root`/`credential_like` copies and
`SchemaRuntime::percent_decode_once` (relocated, not lost);
`reconstruction`'s `#[cfg(test)] fn schema_version`, replaced by
`LojixStoreDatabase::schema_version`; `bootstrap::safe_existing_directory` and
the whole `safe_*` family, superseded by `PathAdmission`/`PrivatePathAdmission`;
and `nexus/src/main.rs`'s `fn run`, folded into `fn main`.

### The half of W9 that is not done: no-inherent-methods in lojix

`checks/no-inherent-methods.sh` exists and runs in `lojix`, but **it does not
pass and `flake.nix` does not reference it**. The brief asked for both laws
enforced; one is. This is the single largest piece of W9 left open, and it was
stopped at deliberately rather than forced.

**67 bare `impl` blocks remain** (down from 86): `src/schema_runtime.rs` 37,
`src/inspection.rs` 9, `src/bootstrap.rs` 8, `src/runtime_flow.rs` 7,
`src/lib.rs` 2, `src/runtime_model.rs` 2, `src/client.rs` 1,
`src/reconstruction.rs` 1.

The reason for stopping is that two of them are God-objects: `impl Store`
(`src/lib.rs:729`, **77 methods**) and `impl SchemaRuntime`
(`src/schema_runtime.rs:2015`, **97 methods** over 2680 lines). Turning either
into one 77- or 97-method trait would pass the grep while being exactly what
the law forbids — a namespace wearing a trait's clothes. Honest decomposition
is a design job, not a refactor pass. This flow agrees with that judgement and
records the proposed decomposition so the next flow starts from it rather than
re-reading the method sets:

- `impl Store` → nine traits: `StoreOpening`, `StoreReading` (the 14 family
  readers), `NexusConfigurationStore`, `IdentifierAllocating` (the 8
  `next_*`/`allocate_*`), `TransitionIntentJournal` (the 12 outbox and
  pending-intent verbs), `EventHistoryMaintenance`, `DeploymentLedger` (13
  admission/terminal/phase verbs), `GenerationLedger`, `JobLedger`.
- `impl SchemaRuntime` → ten: `RuntimeConstruction`, `SignalDeciding` (the 8
  `decide_*`), `SubscriptionServing`, `DeploySubmitting`, `TestSubmitting`,
  `RejectionVocabulary` (the 17 `*_reason`/`*_rejection` — arguably a type of
  its own rather than a trait), `SemaApplying`, `Configuring`, `Querying`,
  `EffectRunning` (the 12 `run_*`).
- The other 65 blocks are small with an obvious single trait each:
  `EphemeralJournal` (21 → `Journalling`), `NixCommand` (18 → `NixInvoking`),
  `HostActivation` (17), `DeployPipeline` (21), `UserEnvironmentActivation`
  (12), `DetachedActivationUnit` (11), and the rest 1–9 methods apiece.
- `runtime_flow.rs:19,42` and `runtime_model.rs:13,38` are four blocks emitted
  by two declarative macros wrapping newtypes (`new`/`payload`/`into_payload`).
  One `Payload` trait implemented by the macro clears all four — the cheapest
  remaining win — but it rewrites every `X::new(v)` call site across the crate
  and its tests, so it was left rather than landed half-verified.

### Landing it on main

This flow re-ran the gate itself rather than landing on a relayed claim. `nix flake check -L --builders ''` was run here against
`git+file:///git/github.com/LiGoldragon/lojix?rev=8cb12b8d9c3864813cf54619597ea8e734b2e99f`
and printed **all checks passed!**, covering `build nexus-binary test
fresh-daemon-startup failure-evidence nexus-startup-rejects-arguments
bootstrap-rejects-flags fmt no-free-functions clippy
retained-transient-semantics same-host-test-activation`. `main` was then moved
to `8cb12b8d9c38` and pushed, and the spent `lojix-trait-laws` bookmark deleted
locally and on the remote.

The gate had to be run against the pinned revision rather than the working
copy, because a sibling flow had taken the shared working copy at
`/git/github.com/LiGoldragon/lojix` while this work was finishing: `jj op log`
shows a new empty commit off the old `main`, and the tree carries
`tests/zz_scratch_proposal.rs` and modified manifests still at 3.0.0. None of
it was touched, committed or reverted by this flow. That sibling's manifests
will conflict with the 4.0.0 bump now on `main`; it is named here so whoever
reconciles it knows where the versions came from.

---

## W10 — housekeeping

**Floating dependencies pinned.** `lojix/Cargo.toml` had `sema-engine` and
`triad-runtime` at `branch = "main"` while every other git dependency pinned a
rev; `nexus/Cargo.toml` had `triad-runtime` the same way. All three now pin
the revision the lock already resolved: `sema-engine`
`27e814a721439af67721c530d48b4d2101141f74`, `triad-runtime`
`02cdd49df63a1769b3cf1b2761261a87eeaa75a4`. No `branch = "main"` remains in
any workspace manifest.

**Two incompatible kameo crates resolved to one, from crates.io.** Witnessed:
`lojix` depended on crates.io `kameo` 0.20.0 while `triad-runtime` depended on
`git+LiGoldragon/kameo.git?rev=f491b45d`, so two copies with
non-interchangeable `Actor`/`ActorRef` types sat in one binary.

The fork was not touched, as instructed. `triad-runtime` was not touched
either: it uses only upstream 0.20 API (`ActorRef`, `Infallible`, `message`,
`Reply`, `DelegatedReply` — witnessed by grep over its sources), so a
`[patch."https://github.com/LiGoldragon/kameo.git"]` in `lojix/Cargo.toml`
redirecting that git source to the published crate collapses both to one.
Witnessed: `cargo tree -i kameo` shows one `kameo v0.20.0` with `lojix` and
`triad-runtime` both under it; `Cargo.lock` has one `[[package]] name =
"kameo"`.

A note against the alternative: `triad-runtime`'s local checkout at
`/git/github.com/LiGoldragon/triad-runtime` is **divergent from its origin**
— local `main` is `428cb2fc` at version 0.7.0, `main@origin` is `02cdd49d` at
0.8.1, with no ancestry path either way, and `jj git fetch` reports nothing to
fetch. Anyone editing that repository reads a stale tree. Not repaired here;
recorded.

**The source-grepping test deleted.** `lojix/tests/actor_native_runtime.rs`
read `src/daemon.rs` and `src/schema_runtime.rs` as strings and asserted on
nine forbidden and eight required literals. It witnessed no behavior and
failed on any edit. The living forbade source-searching tests
(`flows/01a01bac/vision/testTravesties.md:9`) and fe34eb had already written
that it should be replaced or deleted. Nothing referenced it outside itself.

**Bookmarks pruned.** Of lojix's 37 non-`main` bookmarks, nine point at
commits that are ancestors of `main` — the work is in main and the bookmark is
spent. Those were deleted locally and on the remote:

`durable-ledger-retention`, `horizon-driven-intercom`,
`lojix-current-fixtures-542442`, `lojix-datom-horizon-542442`,
`lojix-datom-ingress-542442`, `lojix-datom-writer-542442`,
`realizer-three-stack-status`, `remove-effect-timeout`,
`test-defaults-optional`.

Two more, `discard/disposable-rehearsal` and `disposable-rehearsal`, were
already deleted on the remote and were forgotten locally.

The remaining 26 were **not** deleted, and this is a decision, not an
omission. They are unmerged: a pre-rewrite epic from 2026-07-16/17
(`lojix-canonical-*-milestone-2` through `-9`,
`lojix-canonical-dependency-closure`, `lojix-lifecycle-completion`,
`lojix-schema-one-reconstruction-milestone-8`, `finish-lojix-rewrite`,
`bounded-lifecycle-remediation`, `deployment-compatibility-preflight`,
`certification-blocker-repair`, `ZeusBirdLedgerLojix`,
`home-attribution-integration`) plus older strays (`horizon-leaner-shape`,
`horizon-re-engineering`, `live-deploy-test-chain`, `push-schema-concept-lojix`,
`recovery/lojix-orphan-20260804`, `schema-deep`, `schema-deep-iteration-2`,
`system-operator-contained-test-poc`,
`system-operator-pre-reconcile-2026-05-27`).

The Nexus port superseded that epic, but superseded is not merged: the remote
branch is the only copy of that work, and the brief permits a remote deletion
only where abandonment is clear. It is clear for the nine; for these it is a
judgement the living has not made — the history report itself says "once their
fate is ruled". They are listed here so the ruling can be made from one page.

---

## Not done, and why

- **`DeploymentPipeline::phase_event`'s `_detail: Option<String>`** is still
  discarded. Non-terminal phase transitions therefore carry no detail. The
  terminal transition — the one that matters for diagnosis — does, through
  `optional_deployment_terminal`. Widening `DeploymentPhaseEvent` would be a
  third wire break in one session for a case with no witnessed loss behind it.
- **`CopyClosure` still maps to `BuilderUnreachable`**, which is wrong for a
  copy that failed for any other reason. With evidence attached the reason is
  no longer the only thing an operator has, so a further reason variant was
  not added. Recorded rather than silently accepted.
- **The `lojix` skill's `CheckHostKeyMaterial` row** — see W8.
- **`no-inherent-methods` is not enforced in `lojix`.** The script is written
  and runnable; it does not pass and `flake.nix` does not reference it. 67
  bare impl blocks remain, two of them God-objects whose honest
  decomposition is design work, not a refactor pass. The proposed
  decomposition is recorded in §W9 so the next flow does not have to
  re-derive it. This is the one part of the brief that is not met.
- **15 production `unreachable!()` sites** named by the history report are
  untouched; they are not in W3, W8, W9 or W10.

---

## Orchestrate locks

Two locks were taken at the start of this work — `1111` over
`/git/github.com/LiGoldragon/lojix` and `1112` over
`/git/github.com/LiGoldragon/horizon-rs`, both under flow `f6db8d`. At release
time both `Release.1111` and `Release.1112` answered
`ReleaseRejected.UnknownLockId`, and `Observe.Locks` shows neither: the
Orchestrate lock store lost them during the session, so there was nothing left
to release. Recorded rather than reported as a clean release, because it is a
real observation about the lock store and not a success.

`Observe.Locks` at that moment showed a sibling f6db8d lock `1204 LojixSettle`
covering `lojix`, `horizon-rs`, `signal-lojix` and `meta-signal-lojix`. Every
push described above had already landed by then.

---

## Gates

Every gate below was run locally and seen green before the commit it covers.

| Repository | cargo test | fmt | clippy -D warnings | doc | `nix flake check -L --builders ''` |
|---|---|---|---|---|---|
| `signal-lojix` 4.1.0 | green (4 tests, with and without `datom`) | green | green | green | **all checks passed** |
| `meta-signal-lojix` 5.1.0 | green | green | green | green | **all checks passed** |
| `horizon-rs` 0.10.0 | relayed green (10 tests) | relayed green | relayed green | relayed green | relayed **all checks passed** |
| `lojix` 3.0.0 | green (32 test binaries, 0 failures) | green | green | green | **all checks passed** |
| `lojix` 4.0.0 | relayed green (workspace) | relayed green | relayed green | relayed green | **all checks passed**, witnessed here against `rev=8cb12b8d…` |

The lojix gate was run against the exact landed revision —
`nix flake check -L --builders '' 'git+file:///git/github.com/LiGoldragon/lojix?rev=48f637e8…'`
— rather than against the working copy, because a sibling subflow was by then
editing the same tree for W9. It covered every check the flake declares,
including both NixOS VM tests (`retained-transient-semantics` and
`same-host-test-activation`), which actually boot a guest.

One false alarm worth recording, because it will catch the next agent too:
the first `nix flake check` of lojix reported `no test target named
failure_evidence`. The test file was real and `cargo test` ran it; Nix could
not see it because **the flake source is the tracked tree**, and the file was
still untracked. Committing first makes it visible. Nothing was wrong with the
test.

## Sources

- `flows/f6db8d/reports/lojix-history.md` — the work items W3, W8, W9, W10 and
  the evidence behind each, by this flow's read-only predecessor thread.
- Open bead `primary-cod` (`bd show primary-cod`) — W3's design and acceptance
  criteria, with the prior findings of flows 4a8046 and 542442 recorded on it.
- The `nexus` skill — the no-free-functions and no-inherent-methods laws.
- The `spirit` skill — "Backward compatibility is never a design variable",
  which grounds the removal in W8 and the shape correction in W3.
- The `testing` skill — "A new test is seen failing once before it is
  trusted", and the prohibition on source-searching tests, which grounds the
  deletion in W10.
- `flows/01a01bac/vision/testTravesties.md:9` (relayed through the history
  report) — the living forbidding source-searching tests.
- Witnessed directly in this flow: `lojix`, `signal-lojix`,
  `meta-signal-lojix`, `triad-runtime` and `kameo` working trees; `cargo
  tree`, `cargo test`, `cargo clippy`, `cargo fmt`, `cargo doc` and `nix flake
  check -L --builders ''` output as cited.
- horizon-rs W9 is **relayed** from a `write-demanding` subflow of this thread,
  which reported its own gate; its revision and API moves are quoted from that
  report and were then witnessed here by compiling `lojix` against them.
