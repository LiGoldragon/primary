# Start shorthands — a proposal for the living's review (Flow gap G7)

Composed by an Opus subflow of Psyche High 38de5b, 2026-09-25. A document, no code. Nothing here is built or lands in Vision until the living accepts it.

Marking. Every name this document introduces that the living never said is marked *(agent coinage)* where it first appears. The living's own words are quoted verbatim, in `>` blocks, with their flow id and topic.

## What this rests on

> It should have a complex Flow start call and then it should have shorthands for partly preconfigured minimal calls that don't require so many arguments passed. We like this idea of having these shorthands, I call them. I don't know if there's a canonical way to name them in the industry.
>
> Let's look at the anatomy, design it better, and make this complex central call, which, for any main function or any main feature, is what we would do. Let's get the pattern out of this into a vision that I'll review […]

-- living, 2026-09-25, e51411 launch.

> Actually, we should always have a simple command for everything.

-- living, fd0f97 launch.

> You should have a simple command to start a Codex subflow that will answer back to you and not have to.

-- living, typed, fd0f97 flowTypes.

> The refresh has to just be a simple command, and then the subflow will put together the refresh and have the system prompt in place.

-- living, f55ec8 flowRefresh.

The pattern, in one line: **one complex central call that the Nexus understands, and a family of shorthands that only the client understands, each of which the client expands into exactly that central call before anything is sent.** The Nexus never learns that a shorthand existed.

On the name. "Shorthand" is the living's word and this proposal keeps it. For the living's question about the industry: git calls the split *porcelain* (friendly commands) over *plumbing* (the full primitive); shells and git also say *alias*; configuration tools say *preset* or *profile*; library code says *convenience constructor*. None of them fits better than "shorthand", and "profile" is already taken here by LaunchProfile.

## 1. The central Start, whole

### Its ethos type

From signal-flow `ethos/signal.ethos` at main (f881ab3), the Start query and every type it reaches, in the order the Signal declares them (other queries and types omitted):

```
Signal
[]
[ Start.StartRequest  … ]                                  ; queries
[ Started.Started  LaunchPending.LaunchAttempt  StartAmbiguous.PromptDeliveryIntent  StartRejected.StartRejection  … ]
[ FlowId.String  SessionId.String  TurnId.String
  LaunchRequestId.String  SourcePath.String  SourceSha256.String  SkillName.String
  ModelName.String  Effort.String  RememberingDepth.Integer
  HerdrSessionName.String  SystemPromptBundleFile.String  InstructionPrompt.String
  FlowAspect.[ Psyche Mind Field ]
  PowerLevel.[ High Medium Low UltraLow ]
  HarnessKind.[ Codex Claude ]
  LaunchSource.{ SourcePath SourceSha256 }
  RememberedFlow.{ FlowId RememberingDepth }
  LaunchProfile.{ LaunchRequestId Vector<LaunchSource> Vector<SkillName> FlowAspect PowerLevel HarnessKind ModelName Effort Option<FlowId> Vector<RememberedFlow> HerdrSessionName SystemPromptBundleFile InstructionPrompt }
  OriginClue.{ FlowId SessionId TurnId }
  StartRequest.{ LaunchProfile OriginClue } ]
```

The thirteen positions of LaunchProfile, numbered for the expansion tables below:

| # | Type | What it is |
|---|---|---|
| 1 | LaunchRequestId | the caller's id for this launch attempt |
| 2 | Vector<LaunchSource> | files injected into the first prompt, each path relative to the source root plus its SHA-256 |
| 3 | Vector<SkillName> | skills the new flow loads natively, in order |
| 4 | FlowAspect | Psyche, Mind or Field |
| 5 | PowerLevel | High, Medium, Low, UltraLow |
| 6 | HarnessKind | Claude or Codex |
| 7 | ModelName | the native model string |
| 8 | Effort | the native effort string |
| 9 | Option<FlowId> | predecessor |
| 10 | Vector<RememberedFlow> | flows it remembers, each with a depth |
| 11 | HerdrSessionName | the Herdr session it opens in |
| 12 | SystemPromptBundleFile | absolute path of the system-prompt bundle |
| 13 | InstructionPrompt | the job, as text |

The OriginClue after the profile names who is asking: flow id, session id, turn id.

### A full Start, as datom

A fresh Psyche High Fable flow, as the `flow` CLI takes it today (the values after position 8 are illustrative, not rulings):

```
Start.{ { fresh-38de5b-7 [ { Vision/flowNexus.md eb7fac0ae5ca309f72cb2274b1ce24c8904e34f08e65c6be9496531d8d0d84f2 } ] [ spirit main-flow psyche psyche-interraction ] Psyche High Claude claude-fable-5-1 medium None [] messaging-build /home/li/.local/share/flow/bundle/psyche.md «Begin as Psyche.» } { 38de5b 3c1e9f0a-session turn-12 } }
```

Every one of those positions must be written by hand today. That is the gap G7 names.

## 2. The shorthands

### Where they live, and how the CLI tells them apart

The shorthand type is client-only *(agent coinage: Shorthand as a type name)*. It lives in the flow repository beside the CLI, as a Library (for example `crates/flow/ethos/shorthand.ethos`), not in signal-flow, because the Nexus never receives it.

```
Library
[ signal_flow:[ FlowId FlowAspect HarnessKind InstructionPrompt ModelFamily ]
  specialty:Specialty ]                                      ; Specialty waits on the specialty ruling
[ Shorthand.[ Fresh.FreshStart
              Refresh.FlowId
              Subflow.SubflowStart
              Trial.TrialStart
              Specialized.SpecializedStart ]
  FreshStart.{ FlowAspect ModelFamily }
  SubflowStart.{ ModelFamily InstructionPrompt }
  TrialStart.{ HarnessKind InstructionPrompt }
  SpecializedStart.{ FlowAspect ModelFamily Specialty InstructionPrompt } ]
[]
[]
```

Fresh, Refresh, Subflow, Trial, Specialized as call heads are all *(agent coinage)*. "Refresh" and "subflow" are the living's words for the acts; their use as datom heads is ours.

The CLI still takes exactly one inline datom. It reads the head: if the head names a Query variant (Start, Restart, List, …) the value is read as a Query exactly as today; otherwise it is read as a Shorthand. The two head sets are disjoint, so the long form is untouched: `Start.{ … }` parses and sends byte-for-byte as it does now. Why the shorthands are sibling heads rather than `Start.Seat.{ … }` is open question 1.

The brief's example head was `Start.Seat.{ Psyche Fable }`. This proposal writes `Fresh.{ Psyche Fable }` instead, because the living has twice pushed back on "seat": "I don't understand why you can't call them Flows" (752e0f vocabulary); "do you mean something else by 'seat'?" (d8df70 flowLifecycle). See open question 2.

### What expansion reads from

Each of the 13 positions is filled from these, alone or in the pairs the tables name:

- **S — the shorthand itself**: what the caller wrote.
- **D — defaults held in the Nexus configuration**, read by the client through a new ordinary query (below).
- **R — the registry**: what the Nexus has recorded about an existing flow, including the StartRequest it was launched with.
- **C — the caller's own identity**: `FLOW_ID` and the harness session from the caller's environment, and the caller's own row in R.
- **G — generated by the client**: the launch request id.
- **H — hashed by the client at expansion**: each source path in D is read under the source root and its SHA-256 computed then, so a refreshed vision file is picked up without anyone editing a hash.
- **K — a constant of the expansion rule**, written in the client's code.

### The defaults the Nexus holds

The defaults record *(agent coinage: every type name in this block)* is Signal, set through meta Configure (meta-signal-flow's Configuration grows to carry it; G10 already moves launch configuration into the Sema store) and read on the ordinary socket:

```
; signal-flow additions
[ … Defaults.DefaultsRequest  Profile.FlowId … ]                           ; queries
[ … DefaultsListed.LaunchDefaults  Profiled.StartRequest  ProfileRejected.ProfileRejection … ]
[ …
  DefaultsRequest.{}
  ModelFamily.[ Fable Opus Sonnet Haiku Astra Sol Luna ]
  ModelBinding.{ ModelFamily HarnessKind ModelName Effort }
  PowerBinding.{ FlowAspect ModelFamily PowerLevel }
  AspectDefaults.{ FlowAspect Vector<SourcePath> Vector<SkillName> SystemPromptBundleFile InstructionPrompt }
  SubflowDefaults.{ FlowAspect Vector<SkillName> SystemPromptBundleFile }
  TrialBinding.{ HarnessKind ModelFamily }
  RefreshInstruction.String
  LaunchDefaults.{ HerdrSessionName Vector<ModelBinding> Vector<PowerBinding> Vector<AspectDefaults> Vector<SubflowDefaults> Vector<TrialBinding> RefreshInstruction }
  ProfileRejection.[ UnknownFlow NoRecordedStart ] ]
```

A snapshot of it, as datom (the rows are this subflow's reading of the flows running today — see open question 6):

```
DefaultsListed.{ messaging-build
  [ { Fable Claude claude-fable-5-1 medium } { Opus Claude claude-opus-5 medium } { Haiku Claude claude-haiku-4-5 low }
    { Astra Codex gpt-6-astra medium } { Sol Codex gpt-6-sol medium } { Luna Codex gpt-6-luna low } ]
  [ { Psyche Fable High } { Psyche Opus Medium } { Mind Sol Medium } { Field Astra Medium } { Field Sol Medium } { Field Luna Low } { Field Haiku UltraLow } ]
  [ { Psyche [ Vision/flowNexus.md ] [ spirit main-flow psyche psyche-interraction ] /home/li/.local/share/flow/bundle/psyche.md «Begin as Psyche.» }
    { Field [] [ spirit main-flow ] /home/li/.local/share/flow/bundle/field.md «Begin as Field.» } ]
  [ { Psyche [ spirit subflow psyche ] /home/li/.local/share/flow/bundle/psyche.md } ]
  [ { Claude Haiku } { Codex Luna } ]
  «Continue the work of your predecessor.» }
```

`Profile.FlowId` *(agent coinage)* answers the StartRequest a flow was launched with. No ordinary query returns a LaunchProfile today; Refresh and Subflow need one.

### Shorthand 1 — Fresh: a new flow by aspect and model

```
Fresh.{ Psyche Fable }
```

One line: a new main flow of that aspect on that model, everything else from the aspect's defaults.

| # | Source | Rule |
|---|---|---|
| 1 | G | a fresh launch request id |
| 2 | D, H | AspectDefaults[Psyche] source paths, each hashed now |
| 3 | D | AspectDefaults[Psyche] skills |
| 4 | S | Psyche |
| 5 | D | PowerBinding[Psyche, Fable]; no row → the client refuses and sends nothing |
| 6, 7, 8 | D | ModelBinding[Fable]: harness, model, effort |
| 9 | K | None |
| 10 | K | [] |
| 11 | D | HerdrSessionName |
| 12 | D | AspectDefaults[Psyche] bundle |
| 13 | D | AspectDefaults[Psyche] instruction |
| origin | C | the caller's flow id, session, turn |

With the snapshot above and request id `fresh-38de5b-7`, `Fresh.{ Psyche Fable }` expands to exactly the full Start printed in section 1.

EDN, for flow-clj: `#fresh [:psyche :fable]`.

Resting on: "shorthands for partly preconfigured minimal calls that don't require so many arguments passed" (e51411 launch).

### Shorthand 2 — Refresh: a successor for a named flow

```
Refresh.e51411
```

One line: start the successor of flow e51411 from the profile it was launched with, sources re-read, predecessor set.

| # | Source | Rule |
|---|---|---|
| 1 | G | a fresh launch request id |
| 2 | R, H | the same source paths as R's profile, re-hashed now |
| 3–8 | R | skills, aspect, power, harness, model, effort as R recorded them |
| 9 | S | Some.e51411 |
| 10 | R | R's remembered flows |
| 11, 12 | R | Herdr session and bundle as recorded |
| 13 | D | RefreshInstruction |
| origin | C | the caller |

The client first sends `Profile.e51411`; `ProfileRejected.UnknownFlow` stops it with nothing started.

EDN: `#refresh "e51411"`.

Resting on: "The refresh has to just be a simple command" (f55ec8 flowRefresh); and, in distilled Vision/flowNexus.md, "Reaping belongs to the refresh event, not to a later sweep." That second statement is why this shorthand is not finished by Start alone — see open question 4.

### Shorthand 3 — Subflow: a subflow that answers back to its caller

```
Subflow.{ Opus «Write the Start-shorthands proposal.» }
```

One line: a subflow of the caller's own aspect on the named model, carrying only the job.

| # | Source | Rule |
|---|---|---|
| 1 | G | a fresh launch request id |
| 2 | K | [] |
| 3 | D | SubflowDefaults[caller's aspect] skills |
| 4 | C, R | the caller's own aspect, from the caller's row in R |
| 5 | D | PowerBinding[caller's aspect, Opus] |
| 6, 7, 8 | D | ModelBinding[Opus] |
| 9 | K | None |
| 10 | K | [] |
| 11 | D | HerdrSessionName |
| 12 | D | SubflowDefaults[caller's aspect] bundle |
| 13 | S | the job |
| origin | C | the caller — this is what the subflow answers back to |

EDN: `#subflow [:opus "Write the Start-shorthands proposal."]`.

Resting on: "a simple command to start a Codex subflow that will answer back to you" (fd0f97 flowTypes); and Vision/flowNexus.md: "A subflow is instead an independent flow with its own system prompt, which can reply to the successor of whoever it was meant to answer."

### Shorthand 4 — Trial: a throwaway test flow on a cheap model

```
Trial.{ Claude «Reply exactly TRIAL_OK.» }
```

One line: a bare Field flow at the lowest power, on the cheapest model of the named harness, to test something about the harness itself.

| # | Source | Rule |
|---|---|---|
| 1 | G | a fresh launch request id |
| 2 | K | [] |
| 3 | K | [] |
| 4 | K | Field |
| 5 | D | PowerBinding[Field, TrialBinding[Claude]] — UltraLow in the snapshot |
| 6, 7, 8 | D | ModelBinding[TrialBinding[Claude]] — Haiku in the snapshot |
| 9 | K | None |
| 10 | K | [] |
| 11 | D | HerdrSessionName |
| 12 | D | AspectDefaults[Field] bundle |
| 13 | S | the test prompt |
| origin | C | the caller |

EDN: `#trial [:claude "Reply exactly TRIAL_OK."]`.

Resting on: "Do you want to test this with a haiku model or something?" (e51411 launch, 2026-09-24). Field for testing is the flow-aspect skill's reading ("Testing is field-type work"), not a living quote.

### Shorthand 5 — Specialized: a flow started for its specialty

**Waits on the specialty ruling** (specialties-distillation.md, open before the living). Shown so the family is seen whole; not to be built until the living rules whether a specialty is a sibling query or an option on Start.

```
Specialized.{ Psyche Fable VisionDistillation.{ specialties [ { e51411 flowAspect } { e51411 stack } ] } «Distill the specialty vision.» }
```

One line: Fresh's expansion with the job given, wrapped in the specialized start with its Specialty.

Expands to `StartSpecialized.{ <profile> <Specialty> <origin> }` (proposed in specialties-distillation.md), where the profile is Fresh's expansion for Psyche Fable except position 13, which is S. If the living instead rules Start carries Option<Specialty>, it expands into Start.

EDN: `#specialized [:psyche :fable #vision-distillation ["specialties" [["e51411" "flowAspect"] ["e51411" "stack"]]] "Distill the specialty vision."]`.

Resting on: "You just give them the job for their specialty, and they're off and going." (fd0f97 flowTypes).

### Byte-identity, stated as the test G7 asks for

Expansion is a pure function of five inputs: the shorthand, a LaunchDefaults snapshot, the R record when one is read, the caller identity, and the generated request id (plus the bytes of each source file for H). With those fixed in a fixture, the unit test asserts that the expanded Query and the Query read from the written-out long form produce the same rkyv bytes, and that the expanded Query textualizes to the same datom text. The existing `start_accepts_one_inline_typed_launch_profile` test is unchanged.

### The EDN mirror, for flow-clj

The rule is the one specialties-distillation.md set: a tag is a variant carrying data, a keyword is a variant carrying nothing, a vector is a struct or a vector by position. flow-clj does not exist yet; this is the shape it would take.

| Datom | EDN |
|---|---|
| `Start.{ { … 13 … } { 38de5b s t } }` | `#start [[…13…] ["38de5b" "s" "t"]]` |
| `Fresh.{ Psyche Fable }` | `#fresh [:psyche :fable]` |
| `Refresh.e51411` | `#refresh "e51411"` |
| `Subflow.{ Opus «…» }` | `#subflow [:opus "…"]` |
| `Trial.{ Claude «…» }` | `#trial [:claude "…"]` |
| `Specialized.{ Psyche Fable VisionDistillation.{ … } «…» }` | `#specialized [:psyche :fable #vision-distillation […] "…"]` |

The brief sketched `#start #seat [:psyche :fable]`; that is the EDN of the nested-head form of open question 1. One small correction to the earlier EDN example in specialties-distillation.md: Effort is a String in the Signal, so it mirrors as `"medium"`, not `:medium`.

## 3. What the Nexus receives, and what the client owns

**The Nexus receives only Signal:** the full Start (or StartSpecialized, once ruled) with all 13 positions filled; the two read queries Defaults and Profile; and, on the meta socket, Configure carrying LaunchDefaults. It composes and validates exactly as today. It never sees a Shorthand and has no code path for one.

**The client owns:** the Shorthand type; the head dispatch; the expansion rules; request id generation; reading the caller's identity from its environment; hashing source files under the source root; and refusing a shorthand whose defaults have no row (for example `Fresh.{ Psyche Luna }` with no PowerBinding for it), in which case nothing is sent. Because a CLI's output is always an enum, that refusal is itself a datom, for example `ExpansionRefused.NoPowerBinding.{ Psyche Luna }` *(agent coinage)*.

**The defaults are the Nexus's; the rules are the client's.** Changing what a fresh Psyche flow loads is one meta Configure, with no rebuild. Changing what Fresh means is a client change.

## 4. Open questions for the living

1. **One head or sibling heads.** Should the short form be written `Start.Fresh.{ Psyche Fable }` (the Start head shared), or `Fresh.{ Psyche Fable }` beside it? A datom position has one type, so a shared head means the long form must also change, to `Start.Full.{ { … } { … } }` — and G7's acceptance says the long form stays unchanged. A third way is your multi-form concept: "It would just be the same concept, but some of the fields can be omitted depending on which arity is being used. That way, we have a simple form and a complex form without having to always write out all the fields" (62022e8f multiFormConcepts). But `Start.{ Psyche Fable }` and today's `Start.{ { … } { … } }` both have two positions, so arity alone cannot tell them apart, and datom has no omittable fields yet. This proposal takes sibling heads.

2. **The name of the fresh-flow shorthand.** The brief wrote `Start.Seat.{ Psyche Fable }`; you have asked twice why flows are called seats. `Fresh.{ Psyche Fable }` is proposed. Would you rather `New`, `Flow`, or another word?

3. **Where the defaults live.** Proposed: in the Nexus's configuration, read through `Defaults.{}`. The other way is a constant in the flow client. Example: to add `ethos` to every fresh Psyche flow's skills, the first is one meta Configure; the second is a rebuild and redeploy of `flow`. Which do you want?

4. **Does Refresh start, or replace?** `Refresh.e51411` expanded into Start launches the successor with predecessor e51411, but leaves e51411 routable — against "Reaping belongs to the refresh event". G8 proposes a Replace query that starts and reaps in one event. Should Refresh expand into Replace once it exists, and be withheld until then?

5. **Who assigns the request id.** Today the caller writes position 1. Vision/flowNexus.md says of the requester: "It is assigned a request ID, by which it asks later for status". Example: typing `Fresh.{ Psyche Fable }` twice by mistake — with a client-generated id that is two launches; with an id derived from the caller's turn it is one launch refused as a duplicate. Should the Nexus assign the id, which would remove it from the LaunchProfile?

6. **The power and model table.** The snapshot's rows are read from the flows running today, not from your words: Psyche Fable High, Psyche Opus Medium, Mind Sol Medium, Field Astra Medium, Field Sol Medium, Field Luna Low, Field Haiku UltraLow. Are these right? And should `Fresh.{ Psyche Luna }` be refused, or allowed for the proposed Voice role?

7. **What a trial loads.** `Trial.{ Claude «…» }` loads no skills. But the trial you proposed on 2026-09-24 — whether several `/skill` commands work in one Claude first prompt — needed skills in it. Should Trial take a skill list, `Trial.{ Claude [ spirit main-flow ] «…» }`, or keep one form without skills and one with?

8. **The subflow's aspect.** `Subflow.{ Opus «…» }` takes the caller's aspect, so a Psyche flow's subflow is Psyche, as this subflow is. Is that right, or should a subflow name its aspect, `Subflow.{ Field Sol «…» }`, so Psyche can hand a job straight to Field?

9. **Beyond Start.** You said the central call plus shorthands is "for any main function or any main feature". Should the same be proposed next for Send, for example `Say.{ e51411 «…» }` expanding into the full Send, and for the messenger's commands?

## 5. Sources

Living's words, by flow id and topic:
- e51411 launch — the complex central Flow start call plus shorthands, for every main feature (2026-09-25); one prompt at launch, /main-flow inside it; "test this with a haiku model" (2026-09-24).
- fd0f97 launch — "we should always have a simple command for everything".
- fd0f97 flowTypes — a simple command to start a Codex subflow that answers back; preprogrammed types given only the job.
- f55ec8 flowRefresh — the refresh a simple command.
- 62022e8f multiFormConcepts — a simple form and a complex form of one concept, fields omitted by arity.
- 752e0f vocabulary; d8df70 flowLifecycle — flows, not seats.
- Vision/flowNexus.md (distilled) — refresh reaps; subflows replace harness subagents and answer back; the requester is assigned a request ID.
- Vision/nexus.md (distilled) — Configuration; Default clients; Signal only.

Reports in 38de5b: audit-flow.md G7 (also G8 Replace, G9 status by request id, G10 configuration); specialties-distillation.md (Start example in datom and EDN, StartSpecialized, Specialty); vocabulary-acquisition.md ("Start" as a call name and "seat" are agent terms; "shorthand" and "complex central call" are the living's).

Code at main: signal-flow `ethos/signal.ethos` (f881ab3), LaunchProfile and StartRequest; meta-signal-flow `ethos/signal.ethos` (a1316a0), Configuration; flow `crates/flow/src/main.rs` (972d8d2), the one-datom CLI and its Start test; flow `crates/flow-nexus/src/composition.rs`, profile validation and source hashing.
