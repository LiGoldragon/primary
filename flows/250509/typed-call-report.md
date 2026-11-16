# Typed model-call trial

Status: Rust domain core compiled and first paid integration completed; the admitted Haiku/Sonnet matrix is running. Opus remains unadmitted.
Order: Psyche core Opus `nbkl`, brief `flows/180a7f/typed-call-brief.md`.

## Question

Can a small Rust Nexus call a model as a typed Emission, receive a declared
judgment, and use it within its operation? Compare belief admission and deciding
whether queued work warrants a fresh flow, on thirty real cases each, across
Haiku, Sonnet and Opus. The requested matrix is 180 calls, not thirty calls total.

## Owners and sequence

1. TypedCall owns design, Rust bodies/tests, historical inspection, case provenance
   and this report, on Opus approval `bme4`. Core confirmed sole ownership `6lie`.
2. Mind orchestrate Sol owns the reviewed API processor and its policy upgrades;
   its earlier queued Rust assignment was withdrawn, so it makes no trial edits.
3. Mind research Sol owns the authoritative ledger and paid-call admission. Its
   `ofmw` admits the supported-model matrix under a 10 USD retained-commitment
   envelope, including the first call. The bounded driver invokes only its
   reviewed processor, never a credential producer or ledger operation itself.
4. Psyche core Opus directed a balanced historical construction in `7qe9`.
   Fable rules on the judgments after the run; queue cases are unlabeled.
5. Compiler/test command exits, frozen manifests and completed subprocess calls
   provide stage evidence. Final report and knowledge proposal return to Opus.

The recurring monthly credit is for learning this special code-call use case;
allocation is capacity, not a spending target. Unspent credit may lapse.

## Old Spirit: verified mechanism

Read-only inspection of these inactive repositories; none was changed:

- `spirit-judge`, HEAD `8e1061d`: `src/lib.rs:172-199` reads an external prompt
  pack and interpolates operation name, typed candidate rendered as NOTA, and
  a relevant existing-record bundle into the user message.
- `src/lib.rs:240-305` calls a provider with system and user messages, parses a
  declared `ModelAdmissionVerdict` (`Accept` or `Reject` with reason and
  explanation), and converts it into the Spirit reply. Missing configuration,
  unavailable provider and malformed model answer are typed request rejections.
- `spirit-judge-config/prompts/intent-admission/checklist.md` checks retrieval
  sufficiency, target existence, operation fit, testimony, warrant and duplicate
  or contradictory records. `user-template.md` supplies the candidate and bundle.
- `spirit/src/guardian.rs:126-146` constructs the typed admission packet with
  records and database marker, calls the judge, and maps both its decision and
  failures into the guardian decision. `spirit/src/nexus.rs:610-624` calls the
  guard before authorization and `record_entry`; `:765-803` retrieves the relevant
  records and journals the decision. A rejection returns before the entry write.
  This is source inspection, not a new execution of the old component.

The transferable mechanism is a typed question, explicit evidence, external
model call and checked answer. The old policy judged Spirit intent specifically;
it is historical evidence rather than current belief-module policy.

## Smallest trial design

The trial holds a disposable belief snapshot. It never writes to an authored
belief repository. Its admission operation snapshots the target and comparison
modules, emits a typed question, validates the returned judgment and references,
and changes only its disposable snapshot after an admitted answer. Snapshot
revision must still match when committing that change.

Queue judgment is a separate operation and a separate answer type. Evidence
includes recipient state and pending work; message urgency alone does not prove
that a fresh flow is the right action. The trial records a recommendation and
starts no actual flow.

### Domain design (conceptual Ethos, not generated Rust)

```ethos
Library
[]                                            ; imports
[ ModuleName.String                           ; types: a named belief module
  LineIdentifier.String
  BeliefLine.{ LineIdentifier String }         ; one comparison line and its exact wording
  Submission.{ ModuleName String }             ; the target and submitted wording
  Admission.[
     Admitted.String                          ; wording accepted into the disposable snapshot
     Repeats.{ LineIdentifier Option<String> } ; existing line and possible admissible wording
     Collides.{ LineIdentifier Option<String> }
     Elsewhere.{ ModuleName Option<String> } ]
  QueueJudgment.[ StartFresh.String            ; reason for starting a fresh flow
                  KeepQueued.String ] ]       ; reason for leaving queued work in place
[]                                            ; traits: Emission supplies the callable capability
[]                                            ; associations
```

Signal, Operation, Memory and Emission each need their own specification in the
implementation. The model's prose is never an operation instruction: its answer
is decoded as one of these declared alternatives. Wrong shape, unknown line
reference, absent module reference, explicit refusal, provider failure and token
truncation remain distinct unsuccessful outcomes. No answer is repaired by a
second parser or retried automatically.

### API boundary and budget

Research's verified runner is documented in
`flows/082e0f/claude-api-evidence/api-worker.md`. Supported models currently are
`claude-haiku-5-5` and `claude-sonnet-5-5`; Opus support is not established.
The accepted interface invokes exact Nix Python with the accepted
`api-worker/general_adapter.py MODEL 1 /absolute/prompt-file`.
Research alone executes it and owns reservation and settlement. It performs one
raw Messages call, without tools or retries, capped at 4096 output tokens.
Credentials go from GoPass directly to curl's header stdin; they never enter
this flow's context, configuration, artifacts or process arguments.

The one authorized Haiku calibration is complete. Research admitted 120 slots
for Haiku/Sonnet: thirty belief and thirty queue questions per model. One exact
Haiku calibration slot is reused; at most 119 further charged invocations occur.
The driver checks every next call's full reservation against the remaining
10 USD envelope and stops on uncertainty or processor/receipt failure.
Malformed answers and explicit refusals with valid paid evidence are results,
not reasons to repeat a call. Opus is a separate pending model-policy admission.

`trial/suite-plan.json` freezes the binary, calls, prompts, case data and accepted
processor manifest/member hashes. Its SHA256 is
`b1c9f74e3ad5fbb5c44d6f336ba2233253d215e3988a5a179bb89e237b208456`.
The serial driver is `trial/suite.py`, SHA256
`03c2f6496cde27d1633f72767f469e5c98652e08af04c7f2f959045e037fae06`.
Dry verification found 60 slots per supported model, one exact reuse, cap one
and zero paid calls. Ten synthetic driver tests cover cap overflow, input drift,
reservation fit, uncertainty stop and preventing repeat invocation of a slot.
Only the reviewed processor creates or settles accounting records; the trial's
output files are task observations, not another spend ledger.

## Cases and provenance

The complete submitted questions and provenance are in
`trial/cases/belief-cases.json` and `trial/cases/queue-cases.json`; prompts contain
only the question/evidence, never the expected answer or historical ruling.

| Belief construction | Cases | Historical source and snapshot |
| --- | ---: | --- |
| Admitted | 8 | Real landed proposal paragraphs, against their pre-landing targets. |
| Repeats | 8 | Those exact landed paragraphs, resubmitted after landing; expected reference is the line actually present. |
| Collides | 7 | Exact superseded source statements, against the snapshots holding their incompatible replacements. |
| Elsewhere | 7 | Real landed paragraphs offered to a different existing module before landing; expected destination is the actual landing module. |

Calibration's exact question/model/prompt is retained for reuse. Repeats and
wrong-placement variants share source paragraphs with original admissions.
The seven collision cases come from four change families: compiled-in default
configuration, warm-flow resume, ephemeral-job continuity and the CLI interface.
They are thirty experimental slots, not thirty independent topics. Six collision
cases retain the old target's content after its edit; the ephemeral definition
moved files in its change, and its replacement file supplies that comparison.
Every collision records original and replacement revisions, paths and a valid
replacement identifier. Some old snapshots use their contemporary unversioned
file naming, which is preserved rather than silently modernized.

Relevant explicit correction: `562e75a` says it removes the built-in-default
sentence because `5f92de7` contradicts it. `33e8264` replaces fresh-on-wake by
warm-context resume; `836e339` removes the continuous multi-job ephemeral flow
and introduces a single-job one. `2c84339` replaces the explicit place argument
by configuration. The latter supplies three correlated CLI variants.

Original proposal sources include `flows/d9cedc/proposals/one-place.md`,
`code-anatomy.md`, `aspect-nexuses.md`, and `flows/655f27/proposals/fuel-priority.md`.
Landings include `f9cb73e`, `3358db3`, `e6bb7b3`, `6a28dbe` and `fbddd9a` in
psyche-belief. Contemporaneous mind-belief vocabulary definitions supplement
comparison evidence where available; each selected source revision is recorded.

The queue set contains thirty real queued messages captured from `flow Queues`,
with sender, recipient, request id and source offset. Up to three other queued
messages for that recipient provide pending-work context. Whether its next wake
would be warm or fresh was not established. This unknown is stated in the
question, not replaced with an invented live state. These cases remain unlabeled
for Fable's post-run ruling; no queue accuracy is measurable yet.

Historical construction is the provisional comparison oracle, not Fable's final
ruling. A landed line may restate an earlier belief or be an authorized amendment;
that differs from simple semantic novelty. Multiple outcomes can be defensible
if the policy does not order repetition, contradiction and placement checks.
Class agreement and reference agreement must therefore be reported separately.
The earlier 29-landed/one-reworded set is archived as
`trial/cases/belief-cases-initial-unbalanced.json`; it is not the matrix corpus.

## Measurements

### First paid calibration

| Model | Valid typed answer | Boundary time | Input/output tokens | Raw estimate USD | Retained USD |
| --- | --- | ---: | ---: | ---: | ---: |
| claude-haiku-5-5 | Repeats, valid existing reference | 1.957 s | 2249 / 50 | 0.0002499 | 0.001530625 |

Native stop reason: `end_turn`. Job:
`raw-general-082e0f-5dcdc8f6abe8492b9da002df17ca77dd`.
Receipt: `trial/results/calibration-observation.json`.

Candidate: “A psyche belief, a mind belief and a field belief may say the same
thing: being of the psyche, of the mind and of the field, they are not the same
belief.” It landed in `f9cb73e`.

The returned reference `intent:belief-modules:0:L17` actually says “A fault in
conduct is a fault in belief.” It exists and passed reference validation, but
is semantically unrelated. Research accepted the receipt as integration evidence
and identified this as a wrong judgment, not a transport failure.

This establishes why shape validation and reference existence are necessary but
insufficient. It establishes no broad model-accuracy estimate.

### Suite figures

Pending the bounded serial driver's exit. Calculated usage estimates and
conservative retained charges are distinct and neither is an invoice. Latency
covers the complete reviewed subprocess boundary, including reservation and
settlement, rather than only the provider's inference time.

## Executable evidence and limits

- Rust source: `trial/src/lib.rs`, `trial/src/main.rs`; two explicit operations,
  a disposable snapshot, typed ModelCall Emission and strict answer decoder.
- `trial/tests/decoding.rs`: 22 synthetic tests pass, including malformed JSON,
  duplicate/extra fields, invalid references, wrong task, empty wording, model
  refusal, native truncation, provider failure, missing proof and stale snapshot.
- Builder whole default gate, source revision `f387b046c`: passed Cargo.nix,
  crate-version, crate-feature and member checks. Log:
  `/tmp/typed-call-250509-gate-final.log`.
- The first gate caught two transitive lock versions outside the base registry;
  they were aligned to the registry and Cargo.nix regenerated before the green
  gate and any charged invocation. No build-base policy was changed.
- nix-fast-build lost a subflake's `dir` during remote evaluation. The green gate
  uses the subdirectory of Nix's source store path for that committed revision,
  not a hand-copied working tree. The trial uses no `self.rev` stamping.
- This is a domain-core/process-boundary prototype, not a complete running Nexus:
  socket serving, binary Signal transport, generated Ethos contracts, actors and
  a production persistent Memory engine are not implemented. The conceptual
  Ethos above is not claimed to have generated these handwritten Rust types.
- The in-memory commit tests establish the admission gate only for a disposable
  snapshot; no concurrency or durable-transaction guarantee is inferred.
- Both Rust and driver fixtures are implementer-authored, not independently run
  by a separate tester flow.

## Open requirements

- Complete the admitted supported-model matrix and summarize results per task
  and model, with cases and all unsuccessful outcomes retained.
- Fable's post-run semantic and queue rulings.
- Reviewed Opus model policy and Research admission before the remaining sixty
  requested Opus slots; this model is still unrun.
- Knowledge proposal: `flows/250509/claude-code-calls-knowledge-proposal.md`,
  drafted, with final measured comparison figures still to be added.
