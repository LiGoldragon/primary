# Flow whole design

Flow makes a requested run appear, gives it a durable address, receives its
lifecycle evidence, and ends or refreshes it without leaving a dead route. A
Flow is one harness session and context. Replacing the complete context makes a
new Flow.

## Four roots, twelve voices, and titles

Flow uses four ethos roots. Library contains shared kinds. Signal is the public
request and response surface. Operation describes durable work. Memory holds
admissions, caller-scoped occurrences, attempts, policy, raw reports, and
receipts. Memory data is not public wire state.

```ethos
Library
[]
[ Voice.{ Aspect.[ Psyche Mind Field ]
         Layer.[ Primary Secondary Tertiary Quaternary ] }
  FlowId.String
  Title.{ Voice FlowId }
  RequestId.String
  CapsuleId.String
  Body.String
  State.[ Running Idle Ended ]
  Event.[ Started ToolUsed.String Stopped ] ]
[]
[]
```

`Voice` is the struct `Voice.{ Aspect Layer }`: `Aspect` has Psyche, Mind, and
Field values, and `Layer` has Primary through Quaternary. Layer names topology,
never a model. `Psyche.Primary` is only a Signal display projection of that
struct; it does not encode variants or change identity.
Flow's own Memory/database and meta configuration select harness, model, and
effort for each Voice. That configuration is not a Markdown knowledge skill.
An unconfigured Voice refuses launch rather than inferring a model.

A title is `Title.{ Voice FlowId }`: for example,
`Psyche.Secondary <harness-identity>`. Layer replaces the former model field.
For the MVP, `FlowId` remains the existing typed harness-hash identity: it is
not an Integer and is not rendered into words at launch. Voice is the enduring
route. The native harness session ID is correlation data, never the public
address.

The following is an illustrative, uncompiled combined target. It records the
intended four-root boundary; it is not a claim that the generator currently
accepts or emits the complete layout.

```ethos
Signal
[ flow:[ Voice FlowId Title Body ] ]
[ Start.{ Voice Body }
  ResolveVoice.Voice
  ResolveFlow.FlowId
  Send.{ FlowId Body } ]
[ Started.{ Voice FlowId }
  VoiceResolved.FlowId
  FlowResolved.{ Voice Title }
  Sent ]
[]

Operation
[ flow:[ Voice FlowId CapsuleId Event Body ] ]
[ Start.{ Voice CapsuleId Body }
  Refresh.{ Voice CapsuleId }
  Record.{ FlowId Event } ]
[ Started.FlowId
  Refreshed.FlowId
  Recorded ]
[]

Memory
[ flow:[ Voice FlowId CapsuleId Title ] ]
[ Current.{ Voice FlowId }
  Registry.{ FlowId NativeSession.String CapsuleId Title } ]
```

Signal imports the Library names `Voice`, `FlowId`, `Title`, and `Body`; it
does not restate their shapes. Memory imports `Title` with its other names and
has exactly its two data sections, `Current` and `Registry`. Operation carries
the direct `CapsuleId`, rather than a `Capsule` wrapper, and shows the verb and
past-tense response for each lifecycle operation.

Signal renders a Voice as `Psyche.Primary` only for the common readable
projection. The underlying `Voice.{ Aspect Layer }` remains the same data. A
query and response can therefore display:
`ResolveVoice.Psyche.Primary => VoiceResolved.<harness-identity>`; then
`ResolveFlow.<harness-identity> => FlowResolved.{ Psyche.Primary
Title.{ Psyche.Primary <harness-identity> } }`.

## Deferred Wordable rendering and collision handling

Wordable remains a technically generated Ethos kind for reversible canonical
word renderings at supported widths. It is not part of the Flow MVP wire,
launch gate, or title. The MVP `FlowId` is the existing typed harness-hash
identity; the underlying raw hash remains machine-internal, while model-facing
receipts use readable artifact names, paths, and match or mismatch status.

A later Flow specialization may render a 33-bit slice as three camelCase BIP-39
words. Its harness-specific source is already constrained: Claude uses the
first 33 RFC-network UUIDv4 bits, with the version nibble outside that slice;
Codex uses UUIDv7 random-tail bits 92 through 124, not timestamp bits. That
future representation must be implemented and tested in deterministic code,
not judged by a model.

If a future 33-bit rendering maps to more than one Flow, resolution returns all
matches and reports Psyche. It never silently selects, routes, reallocates, or
suffixes one candidate. Legacy aliases and a later word rendering remain
separate representations.

## Lifecycle, Capsule, and hooks

`Started`, `ToolUsed`, and `Stopped` are raw observations. Flow maps them to
`Running`, `Idle`, and `Ended` only after matching the relevant turn and
session. A stop can arrive early or repeat; it does not itself mean Ended.
Idle means a settled turn and an available session, not merely quiet terminal
output.

Capsule provides the runtime home, process boundary, app-server socket, and
store. It is not a sandbox. Test isolation is an external testing setup and is
outside Flow. Herdr provides panes and TUI beneath Capsule. Every harness hook invokes
the Flow CLI. The CLI authenticates its caller through peer process, ancestry,
and Capsule association; a supplied Flow ID is checked, never trusted as
authority. A shared Codex app-server process does not identify a thread by
itself, so a Capsule-owned association is required or the run is blocked.

Only credentials carry over into a replacement Capsule. It recreates runtime
configuration and all ordinary state. Encryption of carried credentials and
stored material remains future work; it is not asserted by this design.

Codex has one paired client and app-server socket. The proxy is a client bridge,
not another server; the TUI resumes the persisted thread through that same
socket. A Codex native ID is returned by `thread/start` and bound before the
first turn. The MVP keeps the typed harness identity; any later word rendering
is outside launch. First-turn delivery is one durable attempt. Attach readiness requires a real-turn witness. Schema
acceptance, a returned UUID, and persistence flags do not prove attachment,
hook installation, or shell-environment application.

Per-voice Flow locks protect session lifecycle. Refresh creates and validates a
successor before reaping a predecessor, then makes one observed current-binding
change. Recovery resumes only the same authorized attempt.

Side work is an independent Capsule Flow, not a native harness subagent. When
an ending side flow leaves questions or requests, an ultra-low Field router
examines them under the captured authority. It may create authorized follow-up
work; it cannot escalate that authority. The result returns to the requester’s
successor by provenance, with an ended-job notice when no route remains.

## Speech, prompt modules, and compiled roles

Speech normally climbs one Layer at a time and Primary is spoken to least.
Field normally reaches Psyche through Mind. Rare direct exceptions require a
reasoned relevance judgment. This is routing guidance, not a wire-level ban.

The main Flow receives the complete composed system prompt. A current Claude
witness establishes that its main system and append modules are main-only,
while CLAUDE.md behavior differs by launch form. It does not settle native fork
or output-style inheritance; Field still needs those cases. Codex
native-subagent prompt inheritance likewise needs version-pinned evidence.
Flow therefore gives native subagents their own bounded role prompt and never
assumes a withheld or inherited module.

Curriculum compiles standing role procedure, repositories, commands, locks,
capability ceiling, and result shape into the role prompt. Invocation stays
short. Messenger, Publisher, Book, Witness, and LockWatch fail closed when a
required skill, authority, or event subscription is absent. Static tokenizer
estimates compare the complete standing prompt, inherited base, and brief;
they are not provider usage or cost. Actual cheap-role cost requires an
isolated compiled-role trial with recorded usage and delivery, which is not yet
available.

## Remaining work

No further living choice is required for this design. Remaining checks are
implementation work: compile the combined target, preserve the typed
harness-identity boundary, implement and test any later Wordable projection and
ambiguity reporting, create Capsule process attribution and replacement
behavior, and obtain the stated harness witnesses.
