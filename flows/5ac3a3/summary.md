# Flow: prompt composition, correct startup, and communication

Design synthesis for the living, 2026-09-27. Prepared by Mind Astra, Flow 5ac3a3. This is a proposal and evidence review, not an implementation or deployment authorization. The predecessor, 6fe957, remains preserved.

## What the living has settled

The latest direct words, recorded in this flow's `vision/flow.md`, are:

> By default, we're going to use the model name.
> The power level has actually been changed. It's not high, medium, and low now. It's primary, secondary, tertiary, and quaternary, which sort of overlaps with our workspace name, so we should eventually change the name of the workspace.
> Your Astra is your primary, but all of your [panes] should be called Mind Astra and then Flow ID using the Datom syntax.

Provenance: living, STT, 2026-09-27; “pains” corrected to “panes”. The workspace rename is eventual, not authorized work in this task. The requested final deliverable was clarified directly as “Claude Artifact visual report.”

Model, aspect, behavioral power, Flow identity, and native session binding are separate facts. Astra is this Mind flow's Primary. A model-name title does not itself establish power or identity. Existing skills still contain older power vocabulary; the living's explicit correction governs this design.

## What Flow owns

A Flow is one main-flow thread and the subflows it starts. A native main successor has its own identity and an explicit predecessor relationship. A collaboration-harness subflow is not automatically a registered Flow Nexus flow.

Flow Nexus owns logical identity, launch composition, native binding, lifecycle, and recipient resolution. Herdr provides the terminal-workspace transport. Message Nexus owns durable messaging attempts and receipts where deployed. Neither a pane nor a successful transport call establishes that a recipient read or completed a request.

The long-running Nexus holds typed state in its own Sema store. Its public and privileged contracts are written in Ethos; socket traffic is validated, framed Signal. Datom is the typed textual boundary in the CLI. The CLI remains thin and speaks to its own Nexus. State changes should be observable through subscriptions, not polling loops.

## The prompt we mean to compose

The loaded main-flow and refresh contracts require one initial submission with this content:

1. The exact expanded main-flow skill first.
2. The other startup-only skills.
3. Spirit and the applicable intent and vision.
4. Relevant raw psyche, verbatim, with context, date, and provenance.
5. Open work, authority, owners, and active dispatches.
6. Witnessed knowledge, explicitly labelled inferences, and relevant distillation.
7. The required skill manifest and the concrete launch brief.

The living's earlier startup instruction is preserved in `flows/d8df70/vision/launch.md`, 2026-09-24:

> Well the real mistake was that the /main flow should have been in there. There should be only one prompt when we start a fresh flow, not two, because then that costs more money and it's less efficient.

Proposal: represent the composition as typed parts, each with its source, content identity, intended context placement, and order. Preserve raw psyche as quotation, not machine paraphrase. The harness adapter translates those parts into native input. It does not promote a tool-read summary into an authoritative skill.

The adapter must preserve the harness's instruction hierarchy. The existing context-strata skill distinguishes standing harness instructions, conversation/skill injections, and fetched material. The exact effective placement must be witnessed for each harness.

## What failed in this session

Luna's transcript and local Codex-source inspection established a specific failure. An incoming message selected ten skills while the root was already working. The transcript recorded structured skill references, but no expanded skill bodies. The initial input of a fresh turn runs the skill contributor; pending input queued during an active turn bypassed that contributor in the inspected implementation. Later fresh-turn selections produced both references and full skill bodies. A final fresh turn expanded all 17 requested remaining skills.

The UI recognized the selections. The failure was between selection and expansion during steering. The initial main-flow explanation that the names were merely unrecognized plain text was wrong. A separate early conclusion that this session could never load skills was also wrong.

Source witness: Luna read the root transcript and `/git/github.com/openai/codex/core/src/session/turn.rs`, `core/src/session/turn_input.rs`, and `ext/skills/src/extension.rs`. These findings apply to the inspected local implementation and this session; they are not a claim about every Codex version.

Proposed correction: skill-bearing input must either receive normal expansion before model delivery or be explicitly deferred to a fresh turn. The interface must expose the difference between selected, expanded, and delivered. Silent acceptance without expansion is not sufficient.

A second failure occurred during this investigation: a subflow reconstructed quotations while assembling the context packet and changed words. Independent source comparison rejected that packet and then found one remaining omission in its first correction. The corrected candidate passed all 14 source-quote comparisons and arrived in the root's user prompt with actual newlines. It explicitly supersedes the inaccurate packet. The missing procedural requirement is an exact comparison at the source and transport boundaries. Proposed wording for the owning psyche-interraction skill, for the living's review before any skill edit: “Before claiming a psyche injection is verbatim, assemble its quotations from source spans, compare every quoted passage with its cited source, and compare the decoded target user message with the verified payload.” No skill file has been edited.

## Startup anatomy and readiness

The proposed startup has distinct typed stages:

| Stage | What must be established | Failure preserves |
|---|---|---|
| Compose | Ordered source material, valid skill selections, content identities | The requested composition and exact unresolved source |
| Create and bind | Native session, Flow identity, aspect, model, power, directory, pane and terminal agree | The partial session and its binding evidence |
| Submit | One intended initial submission is accepted by the exact empty native session | The attempt and its native acceptance evidence |
| Expand | Required bodies and launch context appear in the native transcript with correct contents and order | The specific missing, changed, duplicate, or misplaced part |
| Ready | Identity/title readback, accepted context, and required routing gates pass | Every unresolved gate; predecessor remains available |

An accepted skill reference is not an expansion receipt. A process existing is not a binding receipt. A title is not identity. A machine saying “ready” is not independent evidence for the preceding gates.

The current Flow README and Codex adapter describe ordered typed skill inputs plus composed text and an empty-thread check. That does not by itself prove that native expansion places the exact main-flow body first. This is an open contract question: distinguish the submitted text from the expanded model-facing instruction sequence, then verify the sequence that the rule actually requires. Do not silently redefine the rule or bypass the native skill interface to make a check pass.

Readiness must be tied to immutable evidence of the accepted input and native binding. A retry requires a known failed prerequisite and changed evidence; an ambiguous accepted attempt is reconciled rather than blindly resent.

## Ethos and Datom: the type before the example

The current authored public Signal Ethos inspected by the gathering subflow includes:

```text
StartRequest.{ FlowType OriginClue }
StartRejection.[ UnknownFlowType LaunchRefused OriginUnavailable ]
```

The inspected meta contract contains concrete binding and delivery vocabulary, including:

```text
FlowBindingRefusalReason.[ AmbiguousPane DeadProcess DuplicateFlowId AnatomyMismatch ]
DeliveryGrade.[ Transported Presented Uncertain ]
```

These are existing source excerpts, not a proposed complete replacement contract. The reviewed public Ethos did not express all the launch-profile, skill-expansion, and receipt concepts found in the reviewed Rust implementation. This suggests a source/contract alignment gap. Exact dependency revisions and generated projection must be checked before attributing the mismatch to a particular deployed binary.

For discussion, this minimal new Library declares the proposed title and power vocabulary before showing a Datom value:

```text
Library
[]
[ FlowId.String
  ModelDisplay.String
  Power.[ Primary Secondary Tertiary Quaternary ]
  FlowTitle.[ Psyche.{ ModelDisplay FlowId }
              Mind.{ ModelDisplay FlowId }
              Field.{ ModelDisplay FlowId } ] ]
[]
[]
```

Against the proposed `FlowTitle`, the example is:

```text
Mind.{ Astra 5ac3a3 }
```

Against the separate proposed `Power`, the value is `Primary`. The exact model identifier is observed separately and mapped to its display name; the title never silently substitutes a model. This example is a design proposal, not a live rename. The older source uses V2 in the title. A September 26 record permits removing V2 in the next version; the timing of that change belongs in the next approved contract update.

The full ontology should give each real object its behavior: a composition resolves and fingerprints its parts; a native binding validates itself; a startup attempt advances through evidenced stages; a receipt states what was observed; a route resolves its eligible recipient. Traits belong on those data-bearing types. Typed failure variants identify the failed stage and reason. No catch-all text protocol or parallel compatibility vocabulary is proposed.

## Refresh without splitting the living's conversation

The living previously described a harm from speaking to old and new sessions without either knowing what was said to the other (`flows/d8df70/vision/flowLifecycle.md`, 2026-09-24). The design therefore needs an explicit receiving owner and a deliberate routing transition.

Current authority is to preserve the predecessor. The loaded refresh contract requires readiness evidence and separate authority before retirement or withdrawal of its route. Older lifecycle quotes about automatic closure describe a different earlier direction and are not used as present retirement authority.

The handoff is a referenced block in the predecessor transcript, not an imagined reconstruction. It carries current authority, open work, dispatches, evidence, and unknowns. Pending results need a recorded destination across the transition. A refresh cannot become ready merely because another pane has appeared.

## Messaging as actually observed

The passive routing subflow reported:

| Component | Observation | What it does not establish |
|---|---|---|
| Flow | 26 durable rows; current root resolves as unknown; three Codex routes available at inspection | Universal reachability or a valid route for this root |
| Sonnet | Exact native Claude identity and ready terminal found in Herdr | Flow's Claude control route; that route was unavailable |
| Message Nexus | Live process and ordinary/owner sockets; ordinary registry query succeeded | A usable Sonnet registration; none was established |
| Agent Intercom | Broker startup failed | Failure of Herdr or Message Nexus |
| Herdr fallback | Useful context injections into this root were received | Durable messaging or recipient completion by itself |

The earlier attempt to inspect the long-running Message executable with help failed. A later ordinary Message CLI query established that the service was live. The invocation failure must not be called a service outage.

There is no witnessed “message everyone” operation. Recipients must be resolved individually with exact bindings. Busy is not the same as unavailable, and ambiguous identity is not permission to choose another recipient.

The living explicitly authorized fallback in `flows/e51411/vision/messaging.md`, 2026-09-24:

> That's okay. You're all allowed to bypass failing messages and send each other straight into your panes. I just want you guys to be able to communicate with fallback.

For the requested Sonnet artifact, the witnessed fallback is a native invocation of its visual-report skill with this Markdown source. That useful delivery is authorized; it is not a diagnostic echo. Submission, presentation, read, and artifact completion must be reported separately. A private artifact URL is the requested final output.

Machine messages use the recipient's declared type and actual Datom processing. They should not simulate a type with a decorative prose envelope. Contextual living quotations remain distinct from machine-origin instructions. Durable attempts and receipt records retain integrity details instead of bloating the recipient's message with them.

## Did committing discard psyche?

The independent audit was read-only. It inventoried 38 Vision files, 17 Intent files, 90 legacy raw-vision files, 1,252 flow-vision files, 39 notion files, and 1,325 flow logs/reports/messages. These are inventory counts, not proof that every historical living utterance was captured.

The large September 25 deletion in e51411 was real. A later restoration and log merge followed it. Comparing the pre-deletion tree with current HEAD showed no remaining deleted paths in that flow. The intentional fold of kinds into Ethos and four approved removals of superseded records remain recoverable from Git history.

Other shared-checkout incidents temporarily removed uncommitted records during Jujutsu operations and reconciliation. Records survived in operation history or source transcripts. The exact external actors were not established. A previous apparent huge deletion count came from a reversed comparison and was corrected in the predecessor's audit.

A September 24 audit counted historical logging gaps. The current audit reconciled the design-relevant startup, refresh, messaging, title/power, Ethos, and Datom passages and found no exact quote in that bounded subset still absent from today's records. One original Field transcript is unavailable, but a clearly marked relay of its refresh words survives. That is a provenance gap, not absent quote text.

No permanent loss was established in the examined material. Complete coverage of all historical messages, unavailable sessions, and words never recorded remains unknown. No restoration was performed because this bounded reconciliation identified no missing design quote requiring restoration. The 14 pre-existing dirty records were subsequently preserved in their own scoped local commit. An independent before/after comparison found all 17 existing paths—including this flow's three new files—byte-identical immediately after that commit.

The resulting design requirement is durable capture with provenance and explicit record ownership. Shared-checkout history changes must not be the only protection for newly heard psyche. Capture, commit, publication, and recovery are distinct operations whose evidence must survive independently.

## Work completed and open

The first Luna investigation distinguished selection from expansion and identified the active-turn branch. The fresh-turn followup delivered the missing skill bodies. A separate gathering subflow searched the relevant written psyche corpus and inspected current Ethos declarations. An independent audit checked loss claims and reconciled the relevant historical gaps. A routing subflow separated the live Message service, incomplete Flow registrations, and usable Herdr fallback. Their reports are claims with named sources; the root directly witnessed the complete skills arriving in its context and recorded the living's latest corrections.

The requested contextualized verbatim packet has arrived in the root's user prompt. The root can directly read its sourced quotations, including the September 26 Primary/Secondary/Tertiary/Quaternary correction, the earlier startup and refresh instructions, and their provenance. The final useful Sonnet handoff is the next step after this source's publication. No code, service configuration, live title, route ownership, or predecessor lifecycle has been changed by this design work. This flow created its own log, vision record, and this summary. Repository publication must preserve every pre-existing dirty record.

Open design decisions are the precise expanded-prompt ordering contract, the complete unified Ethos vocabulary for startup and receipts, the next-version title transition, and the durable psyche capture/recovery mechanism. The existing failures have concrete boundaries; implementation should follow an approved ontology and tests at those boundaries, not more uncoordinated local repairs.

## Source trail for the visual report

- This flow's `vision/flow.md` and `log.md`: latest direct decisions and artifact clarification.
- `flows/d8df70/vision/launch.md`: one initial prompt and native skill commands.
- `flows/e51411/vision/refresh.md` and `flows/e167d8/vision/refresh.md`: transcript handoff and refresh hooks.
- `flows/d8df70/vision/flowLifecycle.md`: receiving ownership and split conversations.
- `flows/e167d8/vision/names.md` and `vision/layerVocabulary.md`: naming and power terminology.
- `flows/e51411/vision/messaging.md`: authorized fallback, compact typed messages, contextual verbatim psyche.
- `flows/e51411/vision/nexus.md`: completing Nexus design and handling changing records.
- `Vision/ethos.md`, `Vision/datom.md`, `Vision/messaging.md`, `Intent/startupPrompt.md`: distilled design records.
- Flow README and `crates/flow-nexus/src/codex.rs`, `composition.rs`, `title.rs`: inspected implementation contracts.
- `signal-flow/ethos/signal.ethos` and `meta-signal-flow/ethos/signal.ethos`: inspected authored schema.
- `flows/6fe957/reports/deletion-audit-20260927.md`, its correction, and `recovery-failure-review-20260927.md`: predecessor reports independently checked within the audit's stated scope.
- `flows/d8df70/reports/psyche-logging-audit.md`: historical census, not a current missing-record count.
