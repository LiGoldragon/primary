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
| `lojix` | 3.0.0 | (see §Landing) |

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

See §W9 outcome below.

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
- **15 production `unreachable!()` sites** named by the history report are
  untouched; they are not in W3, W8, W9 or W10.

---

## Gates

Every gate below was run locally and seen green before the commit it covers.

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
