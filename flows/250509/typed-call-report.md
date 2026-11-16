# Typed model-call trial

Status: design and historical inspection; no trial API calls made yet.
Order: Psyche core Opus `nbkl`, brief `flows/180a7f/typed-call-brief.md`.

## Question

Can a small Rust Nexus call a model as a typed Emission, receive a declared
judgment, and use it within its operation? Compare belief admission and deciding
whether queued work warrants a fresh flow, on thirty real cases each, across
Haiku, Sonnet and Opus. The requested matrix is 180 calls, not thirty calls total.

## Owners and sequence

1. TypedCall owns design, historical inspection, case provenance and this report.
2. Mind orchestrate Sol owns the accepted API processor implementation. Asked
   whether it can implement the Rust trial boundary or identify its implementer.
3. Mind research Sol owns paid execution and the single authoritative ledger.
   It reserves 10 USD for this trial; this is allocation, not authorization to run
   independently. Exact prompt paths and bounds must be admitted before calls.
4. Psyche core Opus / Fable provide or rule on case labels. Asked for historical
   rejection/move decisions and fresh-flow judgments; commits alone establish
   landings, not the semantic ground truth of the other classes.
5. Each stage returns its artifact and command-exit evidence. Research executes
   admitted paid work serially. Final results return to Psyche core Opus.

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
  failures into the guardian decision. This confirms how the answer reaches
  the guardian; the final storage mutation path has not yet been traced.

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

### Proposed domain types (Ethos)

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

Proposed first paid batch: two real questions (one per task) on both supported
models, four calls. The full matrix follows only after executable fixture tests,
case labels, capacity and explicit Research admission. The 10 USD allocation
does not establish that the complete matrix is affordable under worst-case
reservations. Retained reservation and actual calculated usage cost are reported
separately; calculated cost is not invoice evidence.

## Case provenance gathered

Real reviewed proposal sources exist in `flows/d9cedc/proposals/`:

| Proposal | Landing evidence | What this proves |
| --- | --- | --- |
| `aspect-nexuses.md`, proposal 6 | psyche-belief `6a28dbee6c9f2eb99beebe6580f1b4f8d81f8810` | Ephemeral-flow line landed in vision/flow-nexus/1.md. |
| `aspect-nexuses.md`, proposal 5b | same commit | Every-version module field landed in vision/belief-modules/0.md. |
| `code-anatomy.md` | psyche-belief `3358db3`, followed by correction `cfa0ca0` | Anatomy prose landed; later emission example was mended. |
| `one-place.md` | psyche-belief `f9cb73e` | One-module belief text landed. |
| `send-several.md` | psyche-belief `4fc8fb6` | SendSeveral landed. |

The candidate's evaluation context must come from before its landing; placing
the landed text in the comparison store would turn an admission case into a
duplicate case. A correction commit is evidence of correction, not by itself a
label that the earlier candidate collides. Thirty independent cases per task
have not yet been assembled.

## Measurements

No paid trial measurements yet. Decode rate, judgment agreement, call latency
and per-call usage cost are unmeasured. No accuracy or completion claim follows
from finding the old implementation or reserving budget.

## Open requirements

- Named Rust implementation owner and source boundary; compiled dry-fixture
  evidence, including refusal, malformed, truncation and reference cases.
- Thirty provenance-backed cases per task, historical snapshots and explicit
  oracle status; Fable's eventual rulings kept separate from inferred labels.
- Research-admitted exact prompts and execution, under its existing ledger.
- Supported Opus policy before any Opus call; otherwise that column stays unrun.
- The completed matrix and figures, or an explicit partial report identifying
  exactly which requirements remain.
