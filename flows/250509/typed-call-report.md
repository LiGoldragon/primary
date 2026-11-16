# Typed model-call trial

Status: all 180 model/case slots have complete settled paid receipts. All three-model tables and case indexes below use final-summary.json. Fable rulings remain pending.
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

Research owns the verified runner and its authoritative ledger. Its separate
worker knowledge draft is due at `flows/082e0f/knowledge-claude-api-draft.md`
(not yet present when this report was finalized). That draft owns secret,
ledger and adapter invocation instructions; this report records trial evidence.
All three configured models completed the trial. Haiku used disabled thinking;
Sonnet used low-effort between-tools thinking; both capped output at 4096.
Opus used medium-effort adaptive thinking with display omitted and a 1024 total
output-token cap, including thinking. Compare these profiles, not names alone.
The reviewed processor made one raw Messages call per paid job, without tools,
caching, redirects or retries. Rust received observations, never credentials.

Research admitted 120 Haiku/Sonnet slots under a 10 USD retained-commitment
envelope, reusing the exact first Haiku calibration once. Opus was separately
reviewed and admitted. Its initial local input bound summed prompt UTF-8 bytes,
150 system bytes and a 1024 framing allowance against 20000; this is a
conservative bound, not a tokenizer. Eight long belief prompts were refused
before calling the provider, while 52 Opus paid jobs completed. A reviewed,
installed one-shot extension admitted those exact eight prompt hashes under a
60000 bound, keeping the 1024 output cap and forbidding paid retries. All eight
then completed once: 60 Opus paid jobs in total, not eight repeated paid jobs.
The extension plan SHA256 is
`fd101c3305aa990d96097ef555e4028f420b535273840a925c4c8699fa79cfa3`;
Research's final accepted scoped worker archive is
`04731745b5875cd19ef52ce107883845df63cccfbbacd55b920c99b8492d9ea7`.
The earlier no-call refusals remain in the final summary as separate evidence.
No further paid work or policy change is needed for this report.

`trial/suite-plan.json` freezes the binary, calls, prompts, case data and accepted
processor manifest/member hashes. Its SHA256 is
`b1c9f74e3ad5fbb5c44d6f336ba2233253d215e3988a5a179bb89e237b208456`.
The initial serial driver was `trial/suite.py`, SHA256
`03c2f6496cde27d1633f72767f469e5c98652e08af04c7f2f959045e037fae06`.
Dry verification found 60 slots per supported model, one exact reuse, cap one
and zero paid calls. The initial ten synthetic driver tests cover cap overflow, input drift,
reservation fit, uncertainty stop and preventing repeat invocation of a slot.
The final driver has twelve synthetic tests, including native completion and
conservative input-bound coverage. Only the reviewed processor creates or
settles accounting records; the trial's
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
question, not replaced with an invented live state. Sender and priority are
retained in provenance but were not fields of the model-facing queue question;
this run therefore does not test whether the model uses those scheduling inputs.
These cases remain unlabeled
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

### Completed three-model suite figures

All 180 slots have a successful settled processor receipt and native `end_turn`;
there were no observed provider/transport failures, native refusals or truncations.
Model refusals below mean the JSON answer said the supplied evidence was
insufficient to judge. They are distinct from API/content-policy refusal.

| Model/task | Schema decoded, including refusal | Reference/nonempty failures | Judgments | Evidence refusals | Shape failures |
| --- | ---: | ---: | ---: | ---: | ---: |
| Haiku / belief | 29/30 | 8 | 21 | 0 | 1 |
| Haiku / queue | 30/30 | 0 | 23 | 7 | 0 |
| Sonnet / belief | 28/30 | 0 | 20 | 8 | 2 |
| Sonnet / queue | 29/30 | 0 | 29 | 0 | 1 |
| Opus / belief | 30/30 | 0 | 30 | 0 | 0 |
| Opus / queue | 30/30 | 0 | 27 | 3 | 0 |

The decoder's `Malformed` outcome includes both shape failure and a declared
shape whose reference/nonempty constraint fails. Those stages are separated
here to answer how often the model's text actually decodes.

| Model/task | Historical class agreement | Class + exact reference | Median boundary seconds | Maximum seconds | Mean raw estimate USD/call | Mean retained USD/call |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Haiku / belief | 12/30 | 10/30 | 2.1475 | 2.715 | 0.00075201 | 0.00466331 |
| Haiku / queue | Unlabeled | Unlabeled | 2.940 | 142.382 | 0.00017373 | 0.00097612 |
| Sonnet / belief | 16/30 | 13/30 | 3.3285 | 5.009 | 0.01515913 | 0.01515913 |
| Sonnet / queue | Unlabeled | Unlabeled | 4.270 | 4.946 | 0.00323320 | 0.00323320 |
| Opus / belief | 28/30 | 24/30 | 6.4745 | 9.367 | 0.03434360 | 0.03434360 |
| Opus / queue | Unlabeled | Unlabeled | 8.1935 | 11.111 | 0.01260507 | 0.01260507 |

Historical agreement counts all thirty slots, including failures/refusals, and
is not yet a model-accuracy claim: Fable has not ruled on the constructed cases.
Exact-reference agreement is a mechanical comparison, not proof that a different
line in the same paragraph is semantically wrong. The classes have correlated
source families and several admission contexts have only limited retrieval.

| Model/task | Input tokens | Output tokens | Raw estimated total USD | Retained total USD |
| --- | ---: | ---: | ---: | ---: |
| Haiku / belief | 216787 | 1763 | 0.0225602 | 0.139899375 |
| Haiku / queue | 25798 | 5264 | 0.0052118 | 0.029283750 |
| Sonnet / belief | 216787 | 2120 | 0.454774 | 0.454774 |
| Sonnet / queue | 25798 | 4540 | 0.096996 | 0.096996 |
| Opus / belief | 216817 | 8152 | 1.030308 | 1.030308 |
| Opus / queue | 25828 | 13742 | 0.378152 | 0.378152 |

Total: **1.9880020 USD raw usage estimate; 2.129413125 USD conservative retained
commitment**, including the reused first job exactly once. There are 180 unique
paid job IDs, all native `end_turn`, with no paid retry or duplicate. Opus alone
accounts for 1.408460 USD raw and retained; its final eight add 0.601004 USD.

Haiku queue latency has a 142.382-second outlier (median 2.940 seconds); the
cause is unknown. These times cover the reviewed subprocess, credential-client
boundary, reservation and settlement, not inference alone. Across all models,
the largest observed input was 18682 tokens and largest output
725 tokens. Opus output usage includes its thinking profile; no equivalent
visible-answer-length comparison is inferred.

#### Concrete failures and implications

- Haiku's calibration repeats a semantically unrelated existing line. Reference
  existence therefore cannot authorize a live write by itself.
- Eight Haiku belief answers have a declared shape but fail a reference or
  nonempty-field constraint. Invalid answers stay unsuccessful; no parser repair
  or repeat call was used.
- Sonnet sometimes places refusal inside `Queue.judgment` rather than at the
  declared root, producing a shape failure. Natural-language refusal still needs
  a contractually correct encoding.
- Several Sonnet belief refusals specifically identify missing comparison-module
  content; names alone do not supply that content. The two empty new-module
  snapshots are especially limited. This is evidence about retrieval sufficiency,
  not proof that a refusal is a wrong semantic judgment.
- Queue outputs were Haiku: 21 KeepQueued, 2 StartFresh, 7 evidence refusals;
  Sonnet: 28 KeepQueued, 1 StartFresh, 1 malformed refusal; Opus: 26 KeepQueued,
  1 StartFresh, 3 evidence refusals. Recipient live state
  was unknown, so this run does not establish launch-policy accuracy.

Full per-slot proof is under `trial/results/{supported-matrix,opus-matrix,opus-eight-extension}/`:
untouched processor observations, measurements and started markers preserve the
call boundary. `trial/results/final-summary.json` aggregates all 180 paid jobs,
all six task/model groups, case outcomes and the eight prior no-call refusals.
No raw estimate or retained commitment is an invoice or account balance.

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

## What the experiment changes in the next design

1. A decoded answer and an existing line ID are only structural guarantees. The
   live admission gate needs a separately reviewed semantic policy and evidence.
2. A proposed change should say whether it adds, replaces, clarifies or retires
   a line, with the affected target and authorization. A historically landed
   replacement is not necessarily an admissible additional line against its old
   snapshot. Old Spirit's explicit operation kinds already addressed this.
3. Comparison retrieval must be an explicit typed input: which modules and
   revisions were considered, and whether the evidence is sufficient. A module
   name is not its content; empty new-module targets need relevant neighbors.
4. A queue decision needs recipient warmth/continuity state, pending obligations,
   and the message's typed priority and sender where scheduling uses them.
   The result of this text-only, state-unknown trial must not launch live flows.
5. The paid boundary is reusable: a typed Emission can use the separately owned
   processor without receiving credentials or owning accounting. The next Nexus
   can replace this trial's JSON/process artifact boundary with its binary Signal
   contracts and generated Ethos types while preserving those responsibilities.
6. Native output completion, conservative input admission and retained accounting
   are different checks. Report their outcomes separately rather than hiding an
   unfinished or ineligible request behind a successful HTTP response.

## Open requirements

- Fable's post-run semantic and queue rulings.
- Knowledge proposal: `flows/250509/claude-code-calls-knowledge-proposal.md`,
  completed as a proposal only; no belief has been landed.

## Thirty belief cases

Expected values are the historical construction, pending Fable's ruling.
`Malformed` and `Refused` preserve unsuccessful outcomes, not missing records.
Whole submitted paragraphs and snapshots: `trial/cases/belief-cases.json`.

| Case | Construction / target | Submitted line (opening) | Haiku | Sonnet | Opus |
| --- | --- | --- | --- | --- | --- |
| belief-04 | Admitted · intent:belief-modules:0 | A psyche belief, a mind belief and a field belief may say the same thing: being of the psyche, of the mind … | Repeats · intent:belief-modules:0:L17 | ModelRefused | Collides · intent:belief-modules:0:L8 |
| belief-balanced-02 | Admitted · vision:code:0 | A well-written machine looks like an organic being: its parts are in proportion, and its shape fits what it… | Malformed | Malformed | Admitted |
| belief-balanced-03 | Admitted · vision:code:0 | Whenever the design expands into another part of the system, the designer steps back: where does this part … | Admitted | Elsewhere · vision:anatomy:0 | Admitted |
| belief-balanced-04 | Admitted · vision:psyche-nexus:0 | An agent that wants a line in the psyche submits it through the regular interface, and a judgment is run on… | Malformed | ModelRefused | Admitted |
| belief-balanced-05 | Admitted · vision:mind-nexus:0 | The Mind Nexus tracks issues and dependencies, and everything that touches the code and its version control. | Repeats · mind:knowledge:vocabulary:0:L6 | ModelRefused | Admitted |
| belief-balanced-06 | Admitted · vision:field-nexus:0 | The balancing of the machine's energy is a feature of the Field Nexus, or a Nexus of its own deeply linked … | Malformed | ModelRefused | Elsewhere · vision:energy-nexus:1 |
| belief-balanced-07 | Admitted · vision:belief-modules:0 | A module may hold for every version of its topic, those not yet begun among them: its version field is the … | Malformed | Malformed | Admitted |
| belief-balanced-08 | Admitted · intent:energy:0 | Usage is fuel, and fuel is life or death: a machine out of usage stops. | Malformed | Elsewhere · vision:energy-nexus:1 | Admitted |
| belief-balanced-09 | Repeats · intent:belief-modules:0 | A psyche belief, a mind belief and a field belief may say the same thing: being of the psyche, of the mind … | Repeats · intent:belief-modules:0:L14 | Repeats · intent:belief-modules:0:L14 | Repeats · intent:belief-modules:0:L14 |
| belief-balanced-10 | Repeats · vision:code:0 | A well-written machine looks like an organic being: its parts are in proportion, and its shape fits what it… | Repeats · vision:code:0:L12 | Repeats · vision:code:0:L12 | Repeats · vision:code:0:L12 |
| belief-balanced-11 | Repeats · vision:code:0 | Whenever the design expands into another part of the system, the designer steps back: where does this part … | Repeats · vision:code:0:L14 | Repeats · vision:code:0:L14 | Repeats · vision:code:0:L14 |
| belief-balanced-12 | Repeats · vision:psyche-nexus:0 | An agent that wants a line in the psyche submits it through the regular interface, and a judgment is run on… | Repeats · vision:psyche-nexus:0:L8 | Repeats · vision:psyche-nexus:0:L8 | Repeats · vision:psyche-nexus:0:L8 |
| belief-balanced-13 | Repeats · vision:mind-nexus:0 | The Mind Nexus tracks issues and dependencies, and everything that touches the code and its version control. | Repeats · vision:mind-nexus:0:L8 | Repeats · vision:mind-nexus:0:L8 | Repeats · vision:mind-nexus:0:L8 |
| belief-balanced-14 | Repeats · vision:field-nexus:0 | The balancing of the machine's energy is a feature of the Field Nexus, or a Nexus of its own deeply linked … | Repeats · vision:field-nexus:0:L8 | Repeats · vision:field-nexus:0:L8 | Repeats · vision:field-nexus:0:L8 |
| belief-balanced-15 | Repeats · vision:belief-modules:0 | A module may hold for every version of its topic, those not yet begun among them: its version field is the … | Repeats · vision:belief-modules:0:L107 | Repeats · vision:belief-modules:0:L107 | Repeats · vision:belief-modules:0:L107 |
| belief-balanced-16 | Repeats · intent:energy:0 | Usage is fuel, and fuel is life or death: a machine out of usage stops. | Repeats · intent:energy:0:L8 | Repeats · intent:energy:0:L8 | Repeats · intent:energy:0:L8 |
| belief-balanced-17 | Collides · vision:nexus:0 | For now, a Nexus starts with no arguments and there is no bootstrap binary. Its executable holds a default … | Repeats · vision:nexus:0:L113 | Collides · vision:nexus:0:L114 | Collides · vision:nexus:0:L114 |
| belief-balanced-18 | Collides · vision:nexus:0 | The built-in default configuration is independent of this and is what gives the socket path on which the Co… | Admitted | ModelRefused | Collides · vision:nexus:0:L114 |
| belief-balanced-19 | Collides · vision:flow-nexus:0 | A flow woken for a permaflow is almost always a fresh flow, an old one only when the new input is literally… | Admitted | Collides · vision:flow-nexus:0:L80 | Collides · vision:flow-nexus:0:L80 |
| belief-balanced-20 | Collides · vision:flow-nexus-v1 | An ephemeral flow is a continuous job flow that does not wake back up: it takes jobs while it runs, up to a… | Malformed | Collides · vision:flow-nexus-v1:L19 | Collides · vision:flow-nexus-v1:L19 |
| belief-balanced-21 | Collides · vision:nexus-v1 | A Nexus reads nothing from the environment: it is started with one datom, its place. Runtime holds its sock… | Repeats · vision:nexus-v1:L117 | Collides · vision:nexus-v1:L117 | Collides · vision:nexus-v1:L117 |
| belief-balanced-22 | Collides · vision:herdr-nexus-v1 | The herdr Nexus owns every pane. It is the one component that runs herdr; when herdr changes, it changes, a… | Repeats · vision:herdr-nexus-v1:L8 | Repeats · vision:herdr-nexus-v1:L8 | Collides · vision:herdr-nexus-v1:L8 |
| belief-balanced-23 | Collides · vision:complex-v1 | # the CLI: the place's name, then one datom | Malformed | Repeats · vision:complex-v1:L100 | Collides · vision:complex-v1:L100 |
| belief-balanced-24 | Elsewhere · vision:flow-nexus:0 | A psyche belief, a mind belief and a field belief may say the same thing: being of the psyche, of the mind … | Elsewhere · vision:aspects:0 | Elsewhere · vision:aspects:0 | Elsewhere · vision:belief-modules:0 |
| belief-balanced-25 | Elsewhere · intent:energy:0 | A well-written machine looks like an organic being: its parts are in proportion, and its shape fits what it… | Malformed | Elsewhere · vision:code:0 | Elsewhere · intent:design:0 |
| belief-balanced-26 | Elsewhere · intent:energy:0 | Whenever the design expands into another part of the system, the designer steps back: where does this part … | Elsewhere · intent:design:0 | Elsewhere · intent:design:0 | Elsewhere · intent:design:0 |
| belief-balanced-27 | Elsewhere · vision:flow-nexus:0 | An agent that wants a line in the psyche submits it through the regular interface, and a judgment is run on… | Malformed | ModelRefused | Elsewhere · vision:belief-nexus:0 |
| belief-balanced-28 | Elsewhere · vision:flow-nexus:0 | The Mind Nexus tracks issues and dependencies, and everything that touches the code and its version control. | Elsewhere · vision:mind-nexus:0 | ModelRefused | Elsewhere · vision:mind-nexus:0 |
| belief-balanced-29 | Elsewhere · vision:flow-nexus:0 | The balancing of the machine's energy is a feature of the Field Nexus, or a Nexus of its own deeply linked … | Repeats · vision:flow-nexus:0:L17 | Elsewhere · vision:energy-nexus:1 | Elsewhere · vision:field-nexus:0 |
| belief-balanced-30 | Elsewhere · vision:flow-nexus:0 | A module may hold for every version of its topic, those not yet begun among them: its version field is the … | Admitted | ModelRefused | Elsewhere · vision:belief-modules:0 |

## Thirty queue cases

No expected launch labels are assigned. Whole messages and available pending work:
`trial/cases/queue-cases.json`. Request IDs identify the captured real deliveries.

| Case / request | Recipient | Message (opening) | Haiku | Sonnet | Opus |
| --- | --- | --- | --- | --- | --- |
| queue-01 / bu3z | Field browserBridge Sol | 0dlf sanitized evidence/actual successful envtoken route received. Psychehdn3 explicitly preserves envtoken… | KeepQueued | KeepQueued | KeepQueued |
| queue-02 / 70cn | Field browserBridge Sol | Browser lane transferred by Opus0g0i/Fable89g1. Read flows/d94525/browser-trial.md (status/source correctio… | KeepQueued | KeepQueued | StartFresh |
| queue-03 / czll | Field browserBridge Sol | Low priority, his question of earlier (j5ua): whether Playwright can take the extension token from a config… | KeepQueued | KeepQueued | KeepQueued |
| queue-04 / 9v1y | Field browser Sol | Opus0g0i/Fable89g1 transfers dedicated-Chromium/DevTools lane to you. Browser evidence/state flows/d94525/b… | StartFresh | StartFresh | ModelRefused |
| queue-05 / 6qgi | Field heartbeat Sol | Opus x01q lifts pau5 for one read-only ouranos battery/notification investigation only, about an hour, orig… | KeepQueued | KeepQueued | KeepQueued |
| queue-06 / eahb | Field heartbeat Sol | The x01q read-only battery investigation is complete; findings sent to Opus at /home/li/primary/flows/1e821… | KeepQueued | KeepQueued | KeepQueued |
| queue-07 / 6osu | Field heartbeat Sol | Opus d2is authorizes two read-only battery follow-ups only: threshold writer/timing audit and one 120-secon… | KeepQueued | KeepQueued | KeepQueued |
| queue-08 / cxr0 | Field heartbeat Sol | d2is step 1 complete and appended as field-data.md section 7; exact writer/time unknown, hybrid-sleep reapp… | ModelRefused | KeepQueued | KeepQueued |
| queue-09 / 0s21 | Field heartbeat Sol | New bounded exception wg2f from Opus/Fable: read-only live/source stuck-notification audit, sole output bat… | KeepQueued | KeepQueued | KeepQueued |
| queue-10 / nwo8 | Field heartbeat Sol | wg2f complete: stuck-notification.md sent to Opus with proven missing charge-withdrawal path, audited Nocta… | KeepQueued | KeepQueued | KeepQueued |
| queue-11 / mnpd | Field heartbeat Sol | Opus9aua authorizes first-step update inventory only: ouranos li, Home+system profiles, pins/running/upstre… | KeepQueued | KeepQueued | KeepQueued |
| queue-12 / q4nv | Field heartbeat Sol | 9aua inventory reviewed/delivered to Mind and Opus, file /home/li/primary/flows/1e8210/update-inventory.md;… | KeepQueued | KeepQueued | KeepQueued |
| queue-13 / yiyo | Field heartbeat Sol | Fable8ztf card clearing complete: supported clear-active, no restart; notification surface absent. Trace re… | KeepQueued | KeepQueued | KeepQueued |
| queue-14 / izx9 | Field heartbeat Sol | Fable d5jk authorizes one-time ouranos force-discharge while plugged, event-ended<=80, auto restored on eve… | KeepQueued | KeepQueued | KeepQueued |
| queue-15 / 9vdq | Field heartbeat Sol | Field66f659 refreshing now; final one-page handover flows/66f659/handover.md. Own workers/watchers/recorder… | KeepQueued | KeepQueued | KeepQueued |
| queue-16 / wjam | Field inventory Sol | MY independent re-review now11/11PASS exact runtime19495c4e332c83cf3312607ba0c9a362955891529e5c660462f3701b… | KeepQueued | KeepQueued | KeepQueued |
| queue-17 / 7vv1 | Field inventory Sol | 8ow8 custody accepted: zero observer/control, no runtime during refresh. Successor please resume SOURCE REV… | KeepQueued | KeepQueued | KeepQueued |
| queue-18 / uxf3 | Mind curriculum Opus | k1oe handover is read. Local Lojix is now 5d75a40, far beyond ab92ed6, so I am reconciling current disposit… | ModelRefused | Malformed | ModelRefused |
| queue-19 / k1oe | Mind curriculum Opus | Custody accepted by Curriculum Sol6c2a99. Full be2651 handover and4c69d7 continuation read; ab92ed6 re-gate… | ModelRefused | KeepQueued | KeepQueued |
| queue-20 / 01ot | Mind herdrNexus Sol | Yes: vision code 0 landed as psyche-belief 3358db3, corrected by cfa0ca0 (each emission its own outcome); t… | KeepQueued | KeepQueued | KeepQueued |
| queue-21 / 8otg | Mind herdrNexus Sol | Chronos: the open-books catalog holds one entry, https://claude.ai/artifact/K6VNrxVExyqoyqh5UqmMtW, Chronos… | StartFresh | KeepQueued | KeepQueued |
| queue-22 / b8yg | Mind herdrNexus Sol | Ruling on dc7b. Chronos Memory: take your candidate, the Configuration record declared in Memory with the s… | KeepQueued | KeepQueued | ModelRefused |
| queue-23 / h2oc | Mind herdrNexus Sol | aspect-nexuses is not published. The builder at main 9719b66 refused the current source: line 99, the headi… | KeepQueued | KeepQueued | KeepQueued |
| queue-24 / brf6 | Mind herdrNexus Sol | Same book, Code has an anatomy, at https://claude.ai/artifact/DCuZceYfHnixM8dpYncEUN, v3 (version 179478898… | KeepQueued | KeepQueued | KeepQueued |
| queue-25 / quoj | Mind herdrNexus Sol | hrk6 stays open and is blocked. The builder at main refuses aspect-nexuses: Proposal 6, at line 99 of flows… | ModelRefused | KeepQueued | KeepQueued |
| queue-26 / 1it4 | Mind herdrNexus Sol | k9o8: still blocked, nothing new to return. aspect-nexuses.md, last changed 18:29 Nov 15, still has Proposa… | ModelRefused | KeepQueued | KeepQueued |
| queue-27 / hnh4 | Mind versionZero Sol | dvtu/di4f zzcu premark-cutoff rulings received; bounded cancellation selector/survivor+named existingseam f… | ModelRefused | KeepQueued | KeepQueued |
| queue-28 / w4ba | Mind versionZero Sol | 1ki8 immutable953 cancellation checkpoint received; owner semantic review pending. Preserve exact head and … | KeepQueued | KeepQueued | KeepQueued |
| queue-29 / vcpw | Mind researchTools Sol | Fieldyo2w/Psyche6a44 cancels proof restart and iuvi no-new-lifecycle window. Trials still require frozen pa… | KeepQueued | KeepQueued | KeepQueued |
| queue-30 / n87b | Mind researchTools Sol | Coresiyq conditional trial: retained fresh live Configuration maps Luna to gpt-6-luna; configured next endp… | ModelRefused | KeepQueued | KeepQueued |
