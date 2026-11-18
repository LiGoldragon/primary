# Proposal 2 source packet — 0.60.1 allocation

Owner: Mind flowNexus Sol, successor 01a511; inherited reservations 427
(source) and 422 (this packet). Task a8fa; Core sebp/hyhv/jooa source audit.

## Immutable source candidate

- Worktree `/git/worktrees/flow-order-lifetime-2b25fa`, branch
  `order-lifetime-2b25fa`.
- Commit `20ca7d8b77dc2618bb1ada46262c352a53da5026`, sole parent
  `8e6097139cc2348440b283245cdfe76224b929a0`; clean after commit.
- Source-only candidate: manifests, lock, Cargo.nix, hashes and flake remain
  the baseline. Psyche/Core allocate this release 0.60.1; release metadata
  and its generation have not run. Frozen reminder cda remains separate,
  allocated 0.60.2 when resumed and rebased. No reminder dependency found.
- No contract, generated type, Ethos, stored schema, upgrade engine or
  configuration change. No publication, merge, build, native launch or
  runtime mutation performed.

## Production changes

`crates/flow-nexus/src/store/logical_delivery.rs`:
`MintsRequestIds::answerable_by` now accepts only Question for Result and
continues to accept only Task for Done. `HoldsOpenRequests::open_requests`
selects only Question and Task, preserving original IDs, delivery evidence,
answer-history bindings, order and task deadlines. This is a derived
obligation: an Order ID remains useful delivery history, not a promise of
an answer. Existing delivered Orders need no migration and no invented
Answered marker. Queued/uncertain delivery state is preserved, so no Order
is silently marked read or withdrawn. Queue, normal receipt, startup,
recovery and grouped receipt paths use these same retained facts when
answering or composing successors.

`crates/flow-nexus/src/send_tool.rs`: public SendableRequest/SendableMessage
construction and the ordinary `resolve_sendable_message` replace private
Result construction with an empty logical ID. Resolution runs before
answer-route and kept-answer paths. Existing replay records stay replay
records. Declared native tool kinds remain Order/Question/Result/Notice;
Task/Done/Living testing uses the existing ordinary CLI, not a new schema.

`UPGRADES.md` explains derived closure and unchanged storage. Other source
edits, in `src/lib.rs`, `src/store.rs` and
`src/store/request_id_migration_process.rs`, are fixtures embedded in those
modules, not production-body changes.

## Named fixtures — authored, UNRUN

- `only_questions_and_tasks_owe_replies_across_delivery_states`: Order,
  Question, Task, Notice and Living across queued/uncertain/delivered;
  Result and Done kind resolution; nonmutation of queue, snapshot, binding
  and reminder. It reads the existing shape; no schema rewrite is required.
- Claude and Codex successor fixtures each deliver a real Order, refuse its
  Result and exclude its text from the successor, carrying Question and
  Task IDs in order and preserving the Task deadline. Existing duplicate
  Done and answered-Question exclusion checks remain.
- Dynamic Results: delivered Order/Task refuse, Question resolves; both
  addressed and unbound senders, kept versus routed answer, exact replay,
  duplicate new-call refusal, and unknown request refusal.
- Existing answer-ID restart/reuse, routed Result, uncertain self-answer,
  grouped Codex receipt and archival fixtures now use Question where they
  request a Result. Historical predecessor fixture bytes remain unchanged.
- Migration process fixture explicitly refuses a Result to a delivered
  migrated Order, admits/delivers a current Question for the positive socket
  Result path, and retains the old Task/Done and archival paths.

`rustfmt --edition 2024 --check` on the changed modules and `git diff
--check` passed. No compile/test success is claimed. Independent Core audit
and the final immutable whole gate remain required.

## Audit attention and evidence limits

Please judge the derived-lifecycle representation against Proposal 2,
particularly the existing Answer query: `queue_operations::answer` still
reports `AnswerRejected.Open` solely from a binding's historical Open bit,
including Order bindings, as it already does for nonanswerable kinds. Its
vocabulary has no added closed-without-answer outcome in this candidate.
This is a known read-surface gap for the audit, not proof that an Order owes
an answer: both answer admission and successor carry reject it. No new
query meaning has been silently selected. Please rule whether the bounded
release should have this read return existing `Refused.Unresolved` for a
nonanswerable request, or retain that separate query's current meaning.

The base does not expose a SendSeveral input in its ordinary dispatcher;
grouped native delivery is exercised by the existing Codex cohort fixture.
This release adds no input or group schema. No native cheap-flow proof has
run. Field 8c7m accepts isolated runtime custody but has not yet established
an approved capsule/launcher/places/credential contract. That is a live
acceptance dependency, not evidence of source correctness.

## Field source pointers for a supported capsule plan

- `crates/flow-nexus/src/main.rs`: daemon takes one place-name datom,
  finds Place in the configured configuration home, and requires its runtime
  and state directories to exist. No alternate guessed flags.
- `crates/flow-place/src/lib.rs`: CliEnvironment and ResolvesCliPlace read
  XDG_CONFIG_HOME/HOME, the client configuration and the named place file;
  CLI routing follows the Place Runtime. The unit fixture demonstrates an
  isolated configuration home naming a distinct place and runtime.
- `crates/flow/src/main.rs` and `crates/flow-meta/src/main.rs`: ordinary and
  meta clients reach that place, not a command-line socket argument.
- `flake.nix` packages.default packages workspace binaries together and
  packages.nexus-configure provides the pinned place compiler. Daemon
  resolves flow-hook beside its own executable. A concrete package path
  awaits the final gate/build; none is claimed here.
- `src/send_tool.rs`/`src/store/send_call.rs`: a daemon's native tool
  subscriber handles threads held in that daemon's own Memory and launch
  records. CLI Place separation alone is not proof of complete native
  launch/hook/Curriculum/Herdr/credential isolation; Field must establish
  those concrete bindings before any launch.

## Next chain

Core audits this exact committed source and resolves the Answer read
surface. Then reserve metadata-generation phase, finalize 0.60.1 metadata,
commit its exact descendant, obtain a fresh Core whole-gate grant, and run
one immutable remote gate. Field completes the isolated capsule plan and
obtains its native-resource clearance, then owns actual cheap-flow matrix
and successor proof. One nonwriter audits commit plus native evidence
against Proposal 2. Only Psyche acceptance permits main merge/next switch.
Task a8fa stays open until actual completion; no Done yet.
