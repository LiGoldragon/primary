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

A title is `Title.{ Voice FlowId }`. The current minimum-product FlowId is
the typed native harness identity, held machine-internally; Voice is the
durable route and the native session is correlation data. The living explicitly
allows word IDs to arrive in a later version. A readable word title remains a
future design, not a launch requirement.

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
`ResolveVoice.Psyche.Primary => VoiceResolved.abandonAbilityAble`; then
`ResolveFlow.abandonAbilityAble => FlowResolved.{ Psyche.Primary
Title.{ Psyche.Primary abandonAbilityAble } }`.

## Superseded Wordable/33-bit design sketch

The following 33-bit allocation prose is retained as a design record, not as
current Flow behavior. It predates the living's minimum-product direction in
[identifier vision](../vision/identifiers.md): FlowId is a hash, a collision is
reported rather than silently selected, and the word ID may be deferred. No
launcher, title, registry, or runtime configuration may claim this sketch is
implemented or settled.

Wordable is a technically generated Ethos kind, not a Flow-specific 33-bit
projection. Its four sections are superkinds, associated kinds, constants, and
capabilities:

```ethos
Library
[]
[ DictionaryVersion.{ DictionaryName.String Revision.Integer }
  WordParseError.[ Empty
                   NonCanonicalText
                   UnknownWord.String
                   WrongWordCount.{ Integer Integer }
                   InvalidIndex.Integer
                   DictionaryMismatch.{ DictionaryVersion DictionaryVersion }
                   NonCanonicalPadding ] ]
[ Wordable.{ []
             [ Dictionary
               Words ]
             [ WIDTH_BITS.Integer ]
             [ as_words.[ Words ]
               parse_words:{ [ Words ]
                             [ Result<Self WordParseError> ] } ] } ]
[]
```

It makes a kind reversible through canonical words for any supported width.
`Dictionary` and `Words` are associated kinds; their constraints belong to
kinds rather than a concrete Flow type. `WordParseError` is parse-only; width
configuration errors are separate. A prior proposal specialized FlowId to 33 bits and camelCase three BIP-39
words, with a Claude UUIDv4 slice and a Codex UUIDv7 random-tail slice. That
allocation is obsolete design prose pending a new accepted identifier contract;
it is not an input to current launch, title, or routing behavior.

A FlowId lookup yielding more than one native session is an explicit
`Ambiguous` refusal. Flow never guesses, silently routes to one candidate, or
adds an automatic suffix. Legacy 24-bit aliases and the 33-bit three-word
rendering are distinct representations. Source offsets and collision behavior
belong in deterministic code tests, not in model judgment.

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
socket. A Codex native ID is returned by `thread/start`, bound before the first
turn, then the final word Flow ID is derived and injected. First-turn delivery
is one durable attempt. Attach readiness requires a real-turn witness. Schema
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

The identifier representation remains a living/design choice: retain the
minimum typed native identity now, or later accept a specific Wordable mapping.
Remaining checks are implementation work: compile the combined target, preserve
ambiguity refusal, create Capsule process attribution and replacement behavior,
and obtain the stated harness witnesses.
