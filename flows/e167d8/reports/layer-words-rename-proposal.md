# Layer words: the rename proposal

Prepared by a subflow of Psyche Opus e167d8, 2026-09-26. Nothing here is
applied. Every skill line needs the living's approval of its exact text; every
`Vision/` and `Intent/` line changes only on his word; every code and type line
is a versioned change.

## The ruling this proposal serves

The living, 2026-09-26: the seat layers are named **primary, secondary,
tertiary, quaternary** — "That's the vocabulary I was actually looking for" —
replacing high / medium / low / ultra-low power, which collided with model
effort (light / medium / high).

    High      -> Primary
    Medium    -> Secondary
    Low       -> Tertiary
    Ultra Low -> Quaternary

Effort words stay where they mean effort.

## The mapping is confirmed by two independent records

**His 09-16 anatomy**, `flows/f55ec8/vision/layers.md`, already uses all four
words for these four positions:

- primary — "the flow of broad consideration, the broad thinking, and it needs
  to be bothered as little as possible"; "the master consideration model, which
  is the primary Fable"
- secondary — "The second has to filter it first... It has to pass an audit by
  the second layer before he can bother the layer above him"
- tertiary — "where you would have the actual real-time communication...
  maintaining liveness, remaining alert and attentive, speech-to-text
  treatment, and quick thinking"
- quaternary — "like the filter. This is where we filter out the noise";
  "pre-reflex, gut reflex, instinctive reflex, ignoring something completely"

Ordering is fixed by the same file: "the tertiary and the quaternary are on
[lower-cost models]... They sort of reflect, at a lower level, more instinctive,
less ambiguous."

**His 09-14 Vedic naming**, `flows/6cc91b/vision/pairHierarchy.md`, is the
origin of the words and agrees on every position:

> There are going to be four layers based on the Vedas, the old Sanskrit terms
> of the four layers of authority and humanity... The middle layer will be more
> like a large knowledge memory system that's consistently aware of a lot of
> things... The primary is where ideas go, basically. The third layer can
> interact with the user. It's like this fast layer, the mercurial layer... The
> fourth layer is like the public space, the more earthy down, also garbage
> collection... Basically, janitors... It all corresponds with the roles of the
> castes: primary, secondary, tertiary, and core.

So the words are not new vocabulary being introduced on 09-26. They are the
living's own 09-14 naming being **restored** over the high/medium/low/ultra-low
words that displaced it. That is the strongest possible ground for the rename,
and it also means several files already use the words correctly.

The chartered private part (`CLAUDE.md:35`,
`flows/6cc91b/vision/privateLayer.md:7`) — "The primary private talks to the
secondary private" — uses them the same way. No change; further corroboration.

---

# The mapping conflicts

Five. Two are serious.

## Conflict 1 — `roles/` maps medium to *tertiary*, not secondary

`/home/li/primary/roles/` already assigns layer words to seats, and its mapping
is not the brief's:

`roles/codex-primary.md:1`

    You are the primary Codex of the mind cluster (high-power seat, Astra).

`roles/codex-medium.md:11`

    Your job is quick, instinctive real-time work — the tertiary layer's mind counterpart.

`roles/codex-low.md:11`

    Your job is pre-reflex filtering — the quaternary layer's mind counterpart.

That is high→primary, **medium→tertiary**, low→quaternary, with secondary
unassigned. The brief's mapping is high→primary, medium→secondary,
tertiary→low, ultra-low→quaternary.

The same collision appears in `tools/compose-seat-prompt.py:58` ("medium Codex
... the tertiary layer's mind counterpart") and `:70` ("low Codex ... the
quaternary layer").

Both mappings can be read from the living's records, because he described the
layers by *function* and the power words by *cost*, and the two axes were never
aligned by him in one sentence. `roles/` matched by function: the medium Codex
does fast real-time work, which is the tertiary's function. The brief matches by
position: medium is the second rung of four.

**This needs his ruling and this proposal does not choose.** It matters
concretely: it decides whether `Mind Sol` becomes `Mind Secondary` or
`Mind Tertiary`, and therefore what `tools/native-seat-launch.mjs:105-108`
should say. Everything in section C below is written to the brief's mapping and
must be re-derived if he rules the other way.

## Conflict 2 — `Curriculum/skills/field.md:27` says the primary is the *fast* one

`/git/github.com/LiGoldragon/Curriculum/skills/field.md:27`

    Primary Field is the fast conversational front end to Psyche and Mind. It uses light reasoning effort when the runtime supports that named setting. Ask Mind for current evidenced truth and tested state. Ask Psyche for desired shape, undecided matters, and questions for the living. Present their separate reports concisely; Primary Field does not replace either role.

Under the ruled anatomy the primary is bothered least and considers broadly;
the *tertiary* is the fast conversational front end. So this line, in authored
source, will say the opposite of the vocabulary as soon as the vocabulary
lands. It is using "primary" in the older sense of "the main one".

Proposed replacement, on the brief's mapping:

    Tertiary Field is the fast conversational front end to Psyche and Mind. It uses light reasoning effort when the runtime supports that named setting. Ask Mind for current evidenced truth and tested state. Ask Psyche for desired shape, undecided matters, and questions for the living. Present their separate reports concisely; Tertiary Field does not replace either role.

Note this is the one place where the two conflicts touch: under `roles/`'s
mapping the fast Field front end sits at the same layer either way, which is
weak evidence that `roles/`'s function-first mapping is the one he meant.
Flagged for his ruling, not resolved.

## Conflict 3 — there is a fifth layer above the primary: **core**, layer 0

`flows/6cc91b/vision/pairHierarchy.md`:

> Start layer 0, which I'll be able to access, and then we're going to name the
> threads after this: core, primary, secondary, tertiary, and quaternary.

and

> Primary is what I'm going to talk to the most, and sometimes I'm going to talk
> to zero. I can talk to zero through primary, but if I want to go private, I'll
> go to the zero layer.

and, 09-14 typed artifact comment:

> if you look at it as a five-layer, the secondary layer is in the middle

So the scheme he named is **five** deep, with `core` / layer 0 above the primary,
and the primary is what he talks to most — not the top. That fits the private
part exactly: layer 0 is the private seat, reached directly "if I want to go
private", and the private part is chartered and not active because its
open-source seat does not run.

Consequence: renaming the four power levels to primary..quaternary is
consistent, but it does **not** make primary the top of the system. `Layer`
should either carry a fifth `Core` variant now or be documented as the four
active layers of a five-layer scheme whose top is not yet running. The proposal
below keeps the type four-wide, because only four seats exist, and flags this.

## Conflict 4 — a standing quaternary may not exist

`flows/b860be/vision/mainRoles.md` and `flows/e167d8/vision/roles.md`, typed the
same day as the naming ruling and earlier in it:

> ... 3 power levels for each of the 3 aspects: high, medium, low. That's all I
> need. If we need ultra-low roles, they're usually temporary in there or
> they're given a special function.

The *word* quaternary is ruled; a *standing* quaternary seat is not. The type
stays four-wide. The twelve-cell roster and the checkup grid may have to become
nine standing cells with quaternary temporary. This proposal flags every roster
and grid site and shrinks nothing.

## Conflict 5 — the existing layer words carry a *function* axis, not a cost axis

`flows/b49251/handoff/psyche-medium-v1/claude-base.md:5344` records:

> The primary layer is the development, design and thinking space, prototypes
> and proofs of concept; the secondary layer is deployment; deploy the clear,
> simple, well-understood things...

and `flows/05c604/vision/deployment.md:3`: "the secondary layer searches
production for bugs and fixes the deploy without breaking anything".

`design/Flows/flowCliPoc.md:49` uses the words as a third thing again — a
**placement** field with only three values, and it explicitly separates them
from effort:

    **Placement layer** records where work is placed
    (`primary`, `secondary`, or `tertiary`).  It is also distinct from a
    Curriculum **effort** selection such as `medium`.

Adopting the words for the cost/judgment axis silently asserts that
design-vs-deployment, placement, and cost are one axis. They may well be — the
primary designs because it is bothered least, the secondary deploys because it
audits — but he has not said so. Worth one question rather than an assumption.

Smaller, related: `flows/9993b5/vision/powerLevels.md` records him grounding the
old words in physical cost — "It's a power level, right? High because it's
literally how much energy we're spending." Nothing in the new words carries
that. If he wants it kept it belongs in one `Vision/modelRoles.md` sentence, not
in a layer name.

---

# Conventions used throughout

    Power / PowerLevel / power_level (the property)   -> Layer
    "power level", "power tier", "behavioral power"   -> "layer"
    "tier" / "rung" (meaning a seat position)         -> "layer"
    "high power" / "low power" (addressing a seat)    -> "primary" / "tertiary"
    roster keys high|medium|low|ultra_low             -> primary|secondary|tertiary|quaternary
    role strings "<Aspect> High"                      -> "<Aspect> Primary"
    "primary X" meaning *the main* X                  -> "the main X", never "primary"

The last line is the one that does real work. After the rename, "primary" means
the layer and nothing else; main-ness is said with "main".

One encouraging fact from the sweep: `/git/github.com/LiGoldragon/Curriculum`
contains only **three** occurrences of primary/secondary/tertiary/quaternary in
total, and `tertiary` and `quaternary` are nearly free of foreign senses
everywhere. The authored skill corpus can take the new words at low cost. The
expense is concentrated in `/home/li/primary`'s own entry files, `roles/`,
`tools/compose-seat-prompt.py`, and `design/Flows/flowCliPoc.md`.
# A. Authored skills (Curriculum) — need the living's approval of exact text

Source root: `/git/github.com/LiGoldragon/Curriculum/skills`. These are the
authored sources; `.agents/`, `.claude/`, `.codex/`, `.pi/` in Primary are
generated from them and are regenerated, never edited.

## A1. `metaflow.md` — the whole skill is about the axis

`metaflow.md:2` (description)

current

    description: A Field flow must place, coordinate, or transfer work across the Field power tiers.

proposed

    description: A Field flow must place, coordinate, or transfer work across the Field seat layers.

`metaflow.md:5`

current

    Field has four power tiers: high, medium, low, and ultra-low.

proposed

    Field has four seat layers: primary, secondary, tertiary, and quaternary.

`metaflow.md:7`

current

    Every Field tier works in the same shared operational scope: keeping the system observed, healthy, fixed, and running. A tier changes the amount of judgment applied to a job. It does not create a separate Field domain, separate authority, or separate destination for the work.

proposed

    Every Field layer works in the same shared operational scope: keeping the system observed, healthy, fixed, and running. A layer changes the amount of judgment applied to a job. It does not create a separate Field domain, separate authority, or separate destination for the work.

`metaflow.md:9`

current

    High Field handles work that needs broad diagnosis, design judgment, or coordination across active work.

proposed

    Primary Field handles work that needs broad diagnosis, design judgment, or coordination across active work.

`metaflow.md:11`

current

    Medium Field maintains the operational picture, makes ordinary judgment calls, and coordinates ongoing work.

proposed

    Secondary Field maintains the operational picture, makes ordinary judgment calls, and coordinates ongoing work.

`metaflow.md:13`

current

    Low Field carries bounded investigations, repairs, and escalations with the context and authority supplied by the sender.

proposed

    Tertiary Field carries bounded investigations, repairs, and escalations with the context and authority supplied by the sender.

`metaflow.md:15`

current

    Ultra-low Field performs narrow, repeatable observation, checking, routing, and maintenance work with bounded inputs and an explicit outcome.

proposed

    Quaternary Field performs narrow, repeatable observation, checking, routing, and maintenance work with bounded inputs and an explicit outcome.

`metaflow.md:17`

current

    Field seats communicate and transfer work both up and down the tiers. Send a job down when its judgment can be bounded. Send it up when its evidence, uncertainty, impact, or authority boundary requires more judgment.

proposed

    Field seats communicate and transfer work both up and down the layers. Send a job down when its judgment can be bounded. Send it up when its evidence, uncertainty, impact, or authority boundary requires more judgment.

`metaflow.md:19`

current

    When a suitable tier is busy, transfer the work to an available Field tier in either direction. The receiving seat accepts the transfer and receives the task, current evidence, authority boundary, open questions, and required outcome. Keep the original owner responsible until that acceptance is recorded.

proposed

    When a suitable layer is busy, transfer the work to an available Field layer in either direction. The receiving seat accepts the transfer and receives the task, current evidence, authority boundary, open questions, and required outcome. Keep the original owner responsible until that acceptance is recorded.

`metaflow.md:21`

current

    Do not strand work at a tier because its usual seat is busy. Do not widen a transferred job beyond its recorded authority.

proposed

    Do not strand work at a layer because its usual seat is busy. Do not widen a transferred job beyond its recorded authority.

## A2. `operational-status-presentation.md` — the status datom type

`operational-status-presentation.md:9`

current

        StatusPresentation.{ FlowId Aspect Power Where Vector<Facing> Vector<PsycheRecord> Vector<Question> }

proposed

        StatusPresentation.{ FlowId Aspect Layer Where Vector<Facing> Vector<PsycheRecord> Vector<Question> }

`operational-status-presentation.md:10`

current

        [ FlowId.String  Aspect.[ Psyche Mind Field ]  Power.[ High Medium Low UltraLow ]  Where.Markdown  Facing.Markdown  PsycheRecord.{ Topic Source Grade }  Topic.String  Source.String  Grade.[ Distilled Raw Notion Reconstructed ]  Question.Markdown  Markdown.String ]

proposed

        [ FlowId.String  Aspect.[ Psyche Mind Field ]  Layer.[ Primary Secondary Tertiary Quaternary ]  Where.Markdown  Facing.Markdown  PsycheRecord.{ Topic Source Grade }  Topic.String  Source.String  Grade.[ Distilled Raw Notion Reconstructed ]  Question.Markdown  Markdown.String ]

`operational-status-presentation.md:18`

current

    The living's words are quoted verbatim. No digest, revision, or id appears except a short flow id. The whole datom stays under 8 KB and is passed directly as the body of one message: `FLOW_ID=<self> hm-send <Psyche High> '<datom>'`.

proposed

    The living's words are quoted verbatim. No digest, revision, or id appears except a short flow id. The whole datom stays under 8 KB and is passed directly as the body of one message: `FLOW_ID=<self> hm-send <Psyche Primary> '<datom>'`.

`operational-status-presentation.md:22` (example datom)

current

        { 6288d1 Mind High

proposed

        { 6288d1 Mind Primary

`operational-status-presentation.md:37` (second example)

current

        { 3c91a7 Field Medium

proposed

        { 3c91a7 Field Secondary

`operational-status-presentation.md:48` — a psyche-record citation whose topic
string is the old name

current

            { «field power tiers» «6cc91b metaflow» Distilled } ]

proposed

            { «field seat layers» «6cc91b metaflow» Distilled } ]

## A3. `flow-communication.md` — routing contract

`flow-communication.md:6`

current

    A flow communicates horizontally with counterparts at the same behavioral power: Psyche Medium with Mind Medium and Field Medium as peers, for example. Power is High, Medium, Low, or Ultra Low even though a native seat is addressed and titled by its model name. For authorization, flows go up. For delegation, flows send down vertically.

proposed

    A flow communicates horizontally with counterparts at the same layer: Psyche Secondary with Mind Secondary and Field Secondary as peers, for example. The layer is Primary, Secondary, Tertiary, or Quaternary even though a native seat is addressed and titled by its model name. For authorization, flows go up. For delegation, flows send down vertically.

`flow-communication.md:10`

current

    Missing and unavailable are witnessed states. Busy or working remains eligible. Resolve the exact binding immediately before every attempt. For a horizontal message, select the unique eligible cell in the named target aspect at the sender's behavioral power. For a vertical message, select the nearest eligible rung in the requested direction within the same aspect. Multiple bindings for one cell are a conflict, never fanout or an arbitrary choice. If no eligible cell exists, return an explicit undeliverable result. A fallback succeeds only when that exact recipient accepts the attempt. An ambiguous attempt stays bound to its original recipient and is reconciled; it is never resent to another rung.

proposed

    Missing and unavailable are witnessed states. Busy or working remains eligible. Resolve the exact binding immediately before every attempt. For a horizontal message, select the unique eligible cell in the named target aspect at the sender's layer. For a vertical message, select the nearest eligible layer in the requested direction within the same aspect. Multiple bindings for one cell are a conflict, never fanout or an arbitrary choice. If no eligible cell exists, return an explicit undeliverable result. A fallback succeeds only when that exact recipient accepts the attempt. An ambiguous attempt stays bound to its original recipient and is reconciled; it is never resent to another layer.

Note: this also retires "rung" as a seat word, which was a third synonym for
the same axis. If the living prefers to keep "rung" for the vertical step,
substitute only the layer names and leave "rung" in place.

`flow-communication.md:14`

current

    Flows are users of the messaging system. Native seat names use aspect and model, such as Mind Sol or Psyche Opus 5.5. The declared power equivalence remains the routing and behavior contract.

proposed

    Flows are users of the messaging system. Native seat names use aspect and model, such as Mind Sol or Psyche Opus 5.5. The declared layer equivalence remains the routing and behavior contract.

`flow-communication.md:16`

current

    Keep aspect, exact native model identifier, model display, behavioral power, Flow ID, and native binding as separate typed facts. A title grants no identity, authority, availability, or route.

proposed

    Keep aspect, exact native model identifier, model display, layer, Flow ID, and native binding as separate typed facts. A title grants no identity, authority, availability, or route.

`flow-communication.md:18`

current

    When the living names a native model or power — Terra, Luna, or low power — normally address the corresponding other native main seat in the same aspect. That is not a request for an internal collaboration child; internal delegated work is named as delegation.

proposed

    When the living names a native model or layer — Terra, Luna, or the tertiary — normally address the corresponding other native main seat in the same aspect. That is not a request for an internal collaboration child; internal delegated work is named as delegation.

## A4. `main-flow.md`

`main-flow.md:28` (first sentence only)

current

    When the living names a native model or power — Terra, Luna, or low power — normally address the corresponding other native main seat in the same aspect, not an internal collaboration child.

proposed

    When the living names a native model or layer — Terra, Luna, or the tertiary — normally address the corresponding other native main seat in the same aspect, not an internal collaboration child.

`main-flow.md:37`

current

    A main flow's remote native title is a Datom struct, `<Aspect>V2.{ <Model> <FLOW_ID> }`. Derive the model display from its exact observed model identifier through the authoritative model-display map; refuse an unmapped identifier. For example, the Medium Mind seat on `gpt-5.6-sol` is `MindV2.{ Sol <FLOW_ID> }`. Its separate typed power remains High, Medium, Low, or Ultra Low and controls behavior, delegation, and routing. Read the model, title, and power declaration back through the supported harness adapter before reporting the seat ready.

proposed

    A main flow's remote native title is a Datom struct, `<Aspect>V2.{ <Model> <FLOW_ID> }`. Derive the model display from its exact observed model identifier through the authoritative model-display map; refuse an unmapped identifier. For example, the secondary Mind seat on `gpt-5.6-sol` is `MindV2.{ Sol <FLOW_ID> }`. Its separate typed layer remains Primary, Secondary, Tertiary, or Quaternary and controls behavior, delegation, and routing. Read the model, title, and layer declaration back through the supported harness adapter before reporting the seat ready.

`main-flow.md:14` — **no change**. "at medium effort" means effort.

## A5. `operational-layer-communication.md`

The skill's own name already says layer, which this rename makes exactly right.

`operational-layer-communication.md:10`

current

    When the living says Terra, Luna, or low power, it normally addresses the corresponding other native main seat in that aspect, not an internal collaboration child. A flow delegates an internal child explicitly.

proposed

    When the living says Terra, Luna, or the tertiary, it normally addresses the corresponding other native main seat in that aspect, not an internal collaboration child. A flow delegates an internal child explicitly.

`operational-layer-communication.md:14`

current

    Field power: reaping, sessions, and the state of the machine go to a field Terra; storage, repositories, and the home directory go to a field Sol.

proposed

    Field layers: reaping, sessions, and the state of the machine go to a field Terra; storage, repositories, and the home directory go to a field Sol.

## A6. `testing-flow-titles.md`

`testing-flow-titles.md:6` — the third and fourth sentences only

current

    High, Medium, Low, and Ultra Low remain typed behavioral powers and do not appear in the native title.

proposed

    Primary, Secondary, Tertiary, and Quaternary remain the typed layer and do not appear in the native title.

current (later in the same line)

    Cover wrong aspect, model, power declaration, or ID; unknown role or model; write/readback failures; and rollback after partial mutation.

proposed

    Cover wrong aspect, model, layer declaration, or ID; unknown role or model; write/readback failures; and rollback after partial mutation.

## A7. `correction.md`

`correction.md:14`

current

    For a correction to a flow's remote title, identify and edit the owning spawn or rename source before repairing the live title; require the corrected format <Aspect> <Power> <FLOW_ID>, with the seat's own canonical ID and explicit role metadata for aspect and power.

proposed

    For a correction to a flow's remote title, identify and edit the owning spawn or rename source before repairing the live title; require the corrected format <Aspect> <Layer> <FLOW_ID>, with the seat's own canonical ID and explicit role metadata for aspect and layer.

## A8. `refresh.md`

`refresh.md:15`

current

    Each launch profile declares an audited list of the newest applicable Vision sources. After the native `FLOW_ID` is assigned, derive its remote title as `<Aspect> <Power> <FLOW_ID>` and accept the launch only after the selected source hashes still match and the native harness reads back that exact title.

proposed

    Each launch profile declares an audited list of the newest applicable Vision sources. After the native `FLOW_ID` is assigned, derive its remote title as `<Aspect> <Layer> <FLOW_ID>` and accept the launch only after the selected source hashes still match and the native harness reads back that exact title.

Note: `refresh.md:15` and `main-flow.md:37` / `testing-flow-titles.md:6`
already disagree about whether the title carries the layer or the model. That
disagreement is pre-existing and this rename does not settle it. Flagged, not
fixed.

## A9. `psyche-interraction.md`

`psyche-interraction.md:44`

current

    A tier word beside a model, such as "Sonnet low", names the flow's power tier, which that model carries; it never names effort.

proposed

    A layer word beside a model, such as "Sonnet tertiary", names the flow's layer, which that model carries; it never names effort.

This is the single most important line in the set: it is the line that exists
only because the old words collided with effort. After the rename it can
arguably be cut, since primary/secondary/tertiary/quaternary cannot be read as
effort at all. Recommendation: keep it for one refresh cycle while old
transcripts still say "Sonnet low", then cut it.

## A10. `field.md`

`field.md:19`

current

    Field Astra is the high-power Field companion: `gpt-6-astra` at medium effort. High-power names the Field tier, never a reasoning-effort override. Field Astra is a fresh main seat with its own native-start receipt and distinct `FLOW_ID`; it does not replace Psyche or Mind.

proposed

    Field Astra is the primary Field companion: `gpt-6-astra` at medium effort. Primary names the Field layer, never a reasoning-effort override. Field Astra is a fresh main seat with its own native-start receipt and distinct `FLOW_ID`; it does not replace Psyche or Mind.

`field.md:23`

current

    Field low is `gpt-5.6-terra`. Field ultra-low is `gpt-5.6-luna`. When the living names Field Terra, Field Luna, or Field low power, normally address the corresponding other native Field main seat, not an internal collaboration child.

proposed

    Field tertiary is `gpt-5.6-terra`. Field quaternary is `gpt-5.6-luna`. When the living names Field Terra, Field Luna, or the Field tertiary, normally address the corresponding other native Field main seat, not an internal collaboration child.

The rest of the line is unchanged.

`field.md:25`

current

    Field subflows use medium reasoning effort. Luna is the ultra-low-energy investigation tier; Terra is the low-energy escalation tier. Preserve Luna's findings and context when escalating an unresolved investigation to Terra.

proposed

    Field subflows use medium reasoning effort. Luna is the quaternary investigation layer; Terra is the tertiary escalation layer. Preserve Luna's findings and context when escalating an unresolved investigation to Terra.

"medium reasoning effort" is kept: it means effort. The word "energy" is
dropped with the rest of the old axis vocabulary; see the energy-meaning
conflict above.

Note: `field.md:23` and `flows/e167d8/vision/roles.md` now disagree — the
living took Terra out on 2026-09-26 and put Luna on both lower layers. That
model assignment is a separate ruling from this rename and is not proposed
here. Flagged.

## A11. `flow-aspect.md`

`flow-aspect.md:10`

current

    through its highest-power flow to show designs, solutions, and questions.

proposed

    through its primary flow to show designs, solutions, and questions.

## A12. `operational-final-response.md`

`operational-final-response.md:14`

current

    Topics name the subjects the flow is concerned with now. Subflows name the work the response implies, each with its topic and a brief; how many start, and at what power, is not the flow's call. Questions carry what needs authorization or a ruling from above.

proposed

    Topics name the subjects the flow is concerned with now. Subflows name the work the response implies, each with its topic and a brief; how many start, and at what layer, is not the flow's call. Questions carry what needs authorization or a ruling from above.

## A13. Skills with no change needed

`vocabulary.md` holds no layer word today. **This is the gap.** The rename's
one-home line does not exist yet, so every skill above spells the axis out.
Proposed new statement for `vocabulary.md`, to be placed after "Flow directory"
and before "Thread":

    Seat layer: one of primary, secondary, tertiary, quaternary — a flow's position in its aspect, which sets peer equivalence, delegation ceiling, and escalation. Primary considers broadly and is bothered least; secondary audits before bothering the primary; tertiary holds liveness and real-time communication; quaternary filters reflexively. Never a model-effort setting.

With that line landed, several sentences above become redundant and can be cut
rather than reworded — `psyche-interraction.md:44` and the "Power is High,
Medium, Low, or Ultra Low" clause in `flow-communication.md:6` in particular.
That is the cleaner shape and matches the one-home rule: write it once, in the
field that owns it. Recommend the living approve the `vocabulary.md` line
first, then the reworded lines as a shorter set.

`claude-harness.md:78` ("`/effort low|medium|high|xhigh`") and
`claude-harness.md:94` ("memory looks low") are effort and quantity. No change.
`herdr.md:30` ("the tier-priority") is the multiplexer's own term. No change.
`operators-notes.md:13` ("approval tier") is the skill-authority axis
(`testing-` / `operational-` / no prefix). No change, though it is the one
remaining "tier" that a reader could misread; if the living wants "tier" gone
entirely it becomes "approval level".

## A14. `field.md:27` — "Primary Field"

See Conflict 2 above for the current text and the proposed replacement. It
belongs to this section by authority but is stated with the conflict because it
cannot be applied until the mapping is ruled.
---

# B. `Vision/` and `Intent/` — change only on the living's approval

## B1. `SKILL_VARIABLES.md` — the collision in its purest form

`SKILL_VARIABLES.md:5-7`

current

    Psyche medium Claude model: claude-opus-4-6[1m]
    Psyche medium Claude effort: medium
    Psyche medium Claude model without million context: claude-opus-4-6

proposed

    Psyche secondary Claude model: claude-opus-4-6[1m]
    Psyche secondary Claude effort: medium
    Psyche secondary Claude model without million context: claude-opus-4-6

Line 6 is the whole problem in eight words: the first "medium" is the layer, the
second is the effort. After the change the line reads without ambiguity.

Separate finding: **these three variables have no consumer.** Grepping
`Psyche medium Claude` across Primary's authored trees and across
`/git/github.com/LiGoldragon/Curriculum` returns only these three definitions.
Nothing refers to them by name, so the rename is free — and it is worth asking
the living whether they should be deleted instead of renamed.

## B2. `Vision/modelRoles.md`

`Vision/modelRoles.md:59`

current

    Haiku is ultra-low power. Sonnet launches Sonnet and Haiku. Opus launches

proposed

    Haiku is quaternary. Sonnet launches Sonnet and Haiku. Opus launches

`Vision/modelRoles.md:80-82`

current

    Power remains a separate typed behavioral property. High, Medium, Low, and
    Ultra Low determine peer equivalence, delegation ceilings, and escalation;
    they are not substituted into the native title.

proposed

    The layer remains a separate typed property. Primary, Secondary, Tertiary,
    and Quaternary determine peer equivalence, delegation ceilings, and
    escalation; they are not substituted into the native title.

`Vision/modelRoles.md:84-88`

current

    Horizontal communication joins aspects at equivalent behavioral power.
    Vertical communication stays within one aspect and normally advances one rung
    at a time. If the adjacent rung is absent or unavailable, routing advances to
    the next running rung in that direction, so Low may reach High when Medium is
    not running. The missing rung is reported as a gap; it does not make the
    message disappear.

proposed

    Horizontal communication joins aspects at the equivalent layer.
    Vertical communication stays within one aspect and normally advances one
    layer at a time. If the adjacent layer is absent or unavailable, routing
    advances to the next running layer in that direction, so the tertiary may
    reach the primary when the secondary is not running. The missing layer is
    reported as a gap; it does not make the message disappear.

`Vision/modelRoles.md:91-92`

current

    Aspect, exact model identifier, model display, behavioral power, Flow ID, and
    native binding remain separate typed facts. The title grants none of the

proposed

    Aspect, exact model identifier, model display, layer, Flow ID, and
    native binding remain separate typed facts. The title grants none of the

`Vision/modelRoles.md:96-99`

current

    Horizontal routing selects the unique eligible cell in the target aspect at
    the sender's behavioral power. Vertical routing selects the nearest eligible
    rung in the requested direction within the same aspect. Busy is still
    eligible.

proposed

    Horizontal routing selects the unique eligible cell in the target aspect at
    the sender's layer. Vertical routing selects the nearest eligible
    layer in the requested direction within the same aspect. Busy is still
    eligible.

The last sentence of the section, "an ambiguous attempt remains attached to that
recipient and is reconciled instead of being resent to another rung", becomes
"...to another layer".

Also in the same section: "Thus the Medium Mind seat on `gpt-5.6-sol` is
`Mind Sol <FLOW_ID>`; it is never titled Mind Medium or Mind Soul." becomes
"Thus the secondary Mind seat on `gpt-5.6-sol` is `Mind Sol <FLOW_ID>`; it is
never titled Mind Secondary or Mind Soul."

The "### Codex side (energy tiers)" heading above line 59 becomes
"### Codex side (layers)".

## B3. `Vision/flowNexus.md`

`Vision/flowNexus.md:48`

current

    flow running on ultra-low power checks every question and every

proposed

    flow running at the quaternary layer checks every question and every

## B4. `Intent/models.md` — the section that exists because of the collision

`Intent/models.md`, section "Two scales share the words high and medium"

current

    ## Two scales share the words high and medium

    The harness's model-effort setting is one scale. The naming of a flow's
    tier is another. A flow named high is named by tier, not by effort setting;
    a flow that reads its tier as an effort setting has misread it.

proposed

    ## The layer scale and the effort scale no longer share words

    The harness's model-effort setting is light, medium, high. A flow's layer
    is primary, secondary, tertiary, quaternary. The two scales share no word,
    so a layer name can never be read as an effort setting.

This is a rewrite rather than a substitution, because the section's whole
subject — the shared words — ceases to exist. It states the new shape
positively instead of guarding against the old misreading, which is what the
rename bought.

Keep the preceding section, "Better models, not higher effort", exactly as it
is: every word in it means effort.

## B5. `Vision/sources/flowNexus.md`

`Vision/sources/flowNexus.md:11`

current

    b81560 operational-fieldUltraLowRoutesSubflowRequests

**No change.** This is a provenance pointer to a raw record filename
(`flows/b81560/vision/archive-operational-fieldUltraLowRoutesSubflowRequests.md`).
Raw records keep their original words and provenance; renaming the pointer
would break the reference. Same rule applies to every `flows/*/vision/`
filename and body containing the old words: they are the living's recorded
words at their date and are not rewritten.

## B6. Raw records — explicitly out of scope

23 files under `flows/*/vision/` carry the old words, including
`flows/9993b5/vision/powerLevels.md`, `flows/b05237/vision/operational-fieldEnergyLevels.md`,
`flows/1b8ac0/vision/roles.md`, `flows/b80e55/vision/lunaForUltraLowEverywhere.md`,
`flows/b80e55/vision/haikuForPsycheUltraLow.md`,
`flows/b81560/vision/operational-twelveFoldRolesOnly.md`,
`flows/4a2502/vision/operational-delegationTierRules.md`.
None is proposed for change. They are the record.

What is owed instead is one new distilled statement in `Vision/modelRoles.md`
carrying the 2026-09-26 ruling and its provenance, so a flow that reads only
`Vision/` learns the new words. Proposed statement:

    ## The four seat layers are primary, secondary, tertiary, quaternary

    A flow's position in its aspect is its layer: primary, secondary, tertiary,
    quaternary. The primary considers broadly and is bothered least. The
    secondary audits a request before bothering the primary. The tertiary holds
    liveness, real-time communication, and speech-to-text treatment. The
    quaternary filters reflexively, correcting speech-to-text and ignoring
    noise. These names replace high, medium, low, and ultra-low power, which
    collided with the model-effort scale.

    -- ruled 2026-09-26; anatomy from `flows/f55ec8/vision/layers.md` (typed,
    2026-09-16); prior axis naming in `flows/9993b5/vision/powerLevels.md`.

---

# C. Code and types — versioned changes

## C1. `signal-flow` ethos — the canonical type, and the root of the rename

`/git/github.com/LiGoldragon/signal-flow/ethos/signal.ethos:26`, at the pinned
rev `5ca97cee791df0a63c14ae665e9bd7ad15f1f2b0` (Primary's checkout is ahead, at
`968ae3b`; the pinned rev is what Primary builds).

current (the two relevant fragments of one long line)

    PowerLevel.[ High Medium Low UltraLow ]

    LaunchProfile.{ LaunchRequestId Vector<LaunchSource> Vector<SkillName> FlowAspect PowerLevel HarnessKind ModelName Effort Option<FlowId> Vector<RememberedFlow> HerdrSessionName SystemPromptBundleFile InstructionPrompt }

proposed

    Layer.[ Primary Secondary Tertiary Quaternary ]

    LaunchProfile.{ LaunchRequestId Vector<LaunchSource> Vector<SkillName> FlowAspect Layer HarnessKind ModelName Effort Option<FlowId> Vector<RememberedFlow> HerdrSessionName SystemPromptBundleFile InstructionPrompt }

Note `LaunchProfile` already carries `Effort` beside the layer: in the current
type the two adjacent fields are `PowerLevel` and `Effort`, exactly the pair the
living said the models confuse. After the change they are `Layer` and `Effort`.

This is a wire-breaking change to the signal contract. It needs: the ethos
edit, `src/generated` regeneration, a `signal-flow` release, the rev bump in
`/home/li/primary/flow/Cargo.toml:17`, and then C2. Per `breaking-upgrades`,
old and new cannot both be live on the wire, so Nexus and every client deploy
together. Ordering matters: nothing in Primary compiles between the rev bump
and C2.

## C2. `flow-nexus` Rust — consumers of the type

All under `/home/li/primary/flow/crates/flow-nexus/src/`. Mechanical:
`PowerLevel` → `Layer`, `power_level` → `layer`, `High`/`Medium`/`Low`/`UltraLow`
→ `Primary`/`Secondary`/`Tertiary`/`Quaternary`.

`composition.rs:132-135` — the display mapping, the only place the strings are
minted

current

                PowerLevel::High => "High",
                PowerLevel::Medium => "Medium",
                PowerLevel::Low => "Low",
                PowerLevel::UltraLow => "Ultra Low",

proposed

                Layer::Primary => "Primary",
                Layer::Secondary => "Secondary",
                Layer::Tertiary => "Tertiary",
                Layer::Quaternary => "Quaternary",

Note the two-word "Ultra Low" becomes one word, which removes the
space-in-a-role-string special case that `canonicalRole`'s regex and several
role strings carry (C3, C4).

Remaining sites, all `PowerLevel` → `Layer` with the matching variant:
`composition.rs:6`, `composition.rs:475`, `composition.rs:492`
(`PowerLevel::High` → `Layer::Primary`), `composition.rs:642`
(`profile.power_level = PowerLevel::UltraLow;` → `profile.layer = Layer::Quaternary;`);
`lib.rs:382` (`binding.power_level` → `binding.layer` in a format call),
`lib.rs:670`, `lib.rs:718` (`Medium`→`Secondary`), `lib.rs:1344`, `lib.rs:1405`
(`High`→`Primary`); `store.rs:1782`, `store.rs:1808` (`High`→`Primary`);
`codex.rs:1161` (`signal_flow::PowerLevel::Medium` → `signal_flow::Layer::Secondary`);
`herdr/launch.rs:1518`, `herdr/launch.rs:1533` (`Medium`→`Secondary`).

## C3. `tools/native-seat-launch.mjs` — canonical role parsing

`tools/native-seat-launch.mjs:101-102`

current

      const exact = /^(Psyche|Mind|Field) (High|Medium|Low|Ultra Low)$/.exec(value);
      if (exact) return { aspect: exact[1], power: exact[2] };

proposed

      const exact = /^(Psyche|Mind|Field) (Primary|Secondary|Tertiary|Quaternary)$/.exec(value);
      if (exact) return { aspect: exact[1], layer: exact[2] };

`tools/native-seat-launch.mjs:104-108` — the model-name alias table

current

        'Field Astra': { aspect: 'Field', power: 'High' },
        'Field Sol': { aspect: 'Field', power: 'Medium' },
        'Field Luna': { aspect: 'Field', power: 'Low' },
        'Mind Astra': { aspect: 'Mind', power: 'High' },
        'Mind Sol': { aspect: 'Mind', power: 'Medium' },

proposed

        'Field Astra': { aspect: 'Field', layer: 'Primary' },
        'Field Sol': { aspect: 'Field', layer: 'Secondary' },
        'Field Luna': { aspect: 'Field', layer: 'Tertiary' },
        'Mind Astra': { aspect: 'Mind', layer: 'Primary' },
        'Mind Sol': { aspect: 'Mind', layer: 'Secondary' },

Note `'Field Luna'` maps to the tertiary here, while `field.md:23` calls Luna
the quaternary and Terra the tertiary, and the 2026-09-26 ruling puts Luna on
both lower layers. That is a pre-existing disagreement between this table and
the skill. Flagged; not resolved by this proposal.

`tools/native-seat-launch.mjs:140` and `:447` and `:553` — the exported symbol

current

    function authorizedFreshFieldLowPower(seatName,profile,profileSupplied,isFresh) {

proposed

    function authorizedFreshFieldTertiary(seatName,profile,profileSupplied,isFresh) {

with the matching rename at the call site `:447`
(`const launchFreshFieldLowPower = ...` → `const launchFreshFieldTertiary = ...`),
the guard at `:452`, and the export list at `:553`.

`tools/native-seat-launch.mjs:144`

current

          (seatName==='field-luna-recovery' && profile.role==='Field Ultra Low' && profile.model==='gpt-6-luna')

proposed

          (seatName==='field-luna-recovery' && profile.role==='Field Quaternary' && profile.model==='gpt-6-luna')

`tools/native-seat-launch.mjs:176-177`

current

      const displayPower = requireModelTitle(role.model);
      return { version: 2, seat, cwd, claimRoot, provisionalTitle: canonical ? `${canonical.aspect} ${displayPower}` : null, canonicalRole: canonical, displayPower, model: role.model, ...

proposed

      const displayModel = requireModelTitle(role.model);
      return { version: 2, seat, cwd, claimRoot, provisionalTitle: canonical ? `${canonical.aspect} ${displayModel}` : null, canonicalRole: canonical, displayModel, model: role.model, ...

`displayPower` is a misnomer today — `requireModelTitle` returns the model
display name, not a layer. The rename is the moment to fix it, and it also
changes the receipt field name `displayPower`, so `tools/native-batch-refresh.mjs`
and the `.native-seat-receipts/*.json` readers move with it.

`tools/native-seat-launch.mjs:523`

current

          receipt.canonicalRole?.aspect!==canonical.aspect || receipt.canonicalRole?.power!==canonical.power ||

proposed

          receipt.canonicalRole?.aspect!==canonical.aspect || receipt.canonicalRole?.layer!==canonical.layer ||

## C4. Other tools

`tools/canonical-title-alignment.mjs:120-121`

current

          !['High', 'Medium', 'Low', 'Ultra Low'].includes(role?.power) || typeof role?.model_id !== 'string') {
        throw new Error('Explicit canonical aspect, power, exact model ID, and matching seat Flow ID required');

proposed

          !['Primary', 'Secondary', 'Tertiary', 'Quaternary'].includes(role?.layer) || typeof role?.model_id !== 'string') {
        throw new Error('Explicit canonical aspect, layer, exact model ID, and matching seat Flow ID required');

`tools/claude-native-seat-refresh.py:94`

current

        match = re.fullmatch(r"(Psyche|Mind|Field) (High|Medium|Low|Ultra Low)", role or "")

proposed

        match = re.fullmatch(r"(Psyche|Mind|Field) (Primary|Secondary|Tertiary|Quaternary)", role or "")

with the tuple unpacking at `:77`, `:112`, `:426`, `:779`, `:924`
(`aspect, power = ...` → `aspect, layer = ...`) and the `titlePlan` dict key
`"power"` → `"layer"` at `:79` and `:781`.

`tools/native-batch-refresh.mjs:113` — `profile.titlePlan?.power!==canonical.power`
→ `profile.titlePlan?.layer!==canonical.layer`.

`tools/field-structure.mjs:3`

current

    const tiers = ['high', 'medium', 'low', 'ultra_low'];

proposed

    const layers = ['primary', 'secondary', 'tertiary', 'quaternary'];

with the identifier renamed at every use in that file.

`tools/field-checkup-shadow.mjs:8` — the same line, the same change.

These two are the **roster-schema break**: the keys are persisted in
`~/.local/state/field-checkup-shadow/latest.json` and in `roster.json`. A
migration or a schema version bump is needed, not a text substitution alone.
`tools/field-checkup/README.md:24` documents the old keys and moves with it.

`tools/field-luna-heartbeat.mjs:55`

current

        const prompt=`You are Field Luna, an ultra-low operational observer. ...

proposed

        const prompt=`You are Field Luna, a quaternary operational observer. ...

`tools/main-flow-mode/system-prompt.md:1`

current

    You are a main flow: one of the twelve seats that extend the living psyche. Your aspect and your power are given in your startup prompt.

proposed

    You are a main flow: one of the twelve seats that extend the living psyche. Your aspect and your layer are given in your startup prompt.

"twelve seats" is left alone here but is in tension with the 2026-09-26 "3
power levels ... that's all I need". Flagged under the conflict above.

`tools/compose-seat-prompt.py:31`, `:80`, `:93` — note these three lines
collide in *both* directions: they use "power" for the layer **and** "primary"
for something else.

current

            "role": "primary Codex mind flow (high-power). Your tmux session is `primary-mind`. ...
            "role": "primary Psyche opus (medium-power), psyche cluster — main synthesizer, dispatches subflows",
            "role": "high Psyche (highest-power), psyche cluster — deep review, spirit, hardest questions",

proposed

            "role": "the primary Codex mind flow. Your tmux session is `primary-mind`. ...
            "role": "the secondary Psyche flow, psyche cluster — main synthesizer, dispatches subflows",
            "role": "the primary Psyche flow, psyche cluster — deep review, spirit, hardest questions",

Line 80 is the clearest case of the two meanings colliding in one string:
"primary Psyche opus (medium-power)" today means *the main* Psyche seat at the
*medium* layer. After the rename that seat is the **secondary**, and the word
"primary" must go or it says the opposite of what is meant. Line 93, the
"high Psyche", is the actual primary. **The tmux session name `primary-mind`
also needs a ruling** — see the repository section.

## C5. Test files

`tools/native-seat-launch.test.mjs:5`, `:120`, `:279-281`, `:304-308`;
`tools/native-batch-refresh.test.mjs:83`, `:88`, `:94`, `:161-167`;
`tools/field-structure.test.mjs:5`, `:98`, `:100-103`;
`tools/field-checkup-shadow.test.mjs:7`, `:35`, `:39`;
`tools/canonical-title-alignment.test.mjs:6`, `:50`, `:58`;
`tools/claude-native-seat-refresh.test.py:33`.
All mechanical and all in the same commit as the code they test. 30 sites.
`field-structure.test.mjs:101` also carries the lowercase role string
`'Psyche ultra low'`, which becomes `'Psyche quaternary'`.

## C6. `config/model-display-names.json` — no change

The map holds only model identifiers and display names. No layer word appears
in it, and none should: `Vision/modelRoles.md:80` and `main-flow.md:37` both
say the layer is a separate typed fact that is not substituted into the title.
The file is correct as it stands.

## C7. Receipts — no change

`.native-seat-receipts/*.json` record what was launched at the time, with the
words in force then. They are evidence, like transcripts and raw records. Not
rewritten.
---

# D. `roles/` and `design/` — authored source outside the skills

These are authored and in Primary, not generated. They change on the living's
word like the skills do. Both are written here to the brief's mapping and must
be re-derived if Conflict 1 resolves the other way.

## D1. `roles/codex-primary.md`

The filename itself asserts a mapping. `:1`

current

    You are the primary Codex of the mind cluster (high-power seat, Astra).

proposed

    You are the Mind primary on Codex (Astra).

"high-power seat" goes because the layer name now carries it, and "primary
Codex" is rewritten so "primary" reads as the layer rather than as "the main".

`roles/codex-primary.md:11`

current

    Await orders from the living or from primary Psyche opus (Claude flow da1e3f).

proposed

    Await orders from the living or from the Psyche secondary on Claude (flow da1e3f).

This line is the collision in miniature: `da1e3f` is the *medium* Psyche seat,
so today "primary Psyche opus" means the main Psyche at the medium layer. After
the rename, calling it primary says the wrong layer.

## D2. `roles/codex-medium.md`

`:1`

current

    You are the medium Codex of the mind cluster (Sol).

proposed

    You are the Mind secondary on Codex (Sol).

`:11` — **this is the line Conflict 1 turns on.** On the brief's mapping:

current

    Your job is quick, instinctive real-time work — the tertiary layer's mind counterpart.

proposed

    Your job is auditing and ordinary judgment before the primary is bothered — the Mind secondary.

That rewrites the *job*, not only the word, which is why it cannot be applied
without his ruling. If he rules `roles/`'s function-first mapping instead, the
line keeps its job description and the seat becomes `Mind Tertiary`, and
`tools/native-seat-launch.mjs` must map `'Mind Sol'` to `Tertiary`.

`:13` — `Await orders from the living or from primary Psyche opus.` becomes
`Await orders from the living or from the Psyche secondary.` Same in
`roles/codex-low.md:13`.

## D3. `roles/codex-low.md`

`:1`

current

    You are the low Codex of the mind cluster (Luna).

proposed

    You are the Mind quaternary on Codex (Luna).

`:11` — already correct after the rename; the only change is dropping the
redundant "layer's mind counterpart" phrasing:

current

    Your job is pre-reflex filtering — the quaternary layer's mind counterpart.

proposed

    Your job is pre-reflex filtering — the Mind quaternary.

Note `roles/codex-low.md` maps **low** to quaternary while the brief maps
ultra-low there. Under the brief, Luna at the low layer is the *tertiary*. This
is Conflict 1 again, from the other end.

## D4. `design/Flows/flowCliPoc.md:49` — the placement field

current

    **Placement layer** records where work is placed
    (`primary`, `secondary`, or `tertiary`).  It is also distinct from a
    Curriculum **effort** selection such as `medium`.

proposed

    **Placement layer** records the layer the work is placed at
    (`primary`, `secondary`, `tertiary`, or `quaternary`) — the same layer the
    seat carries, not a separate axis. It remains distinct from a Curriculum
    **effort** selection such as `medium`.

This design already had the right words and the right warning about effort. The
change adds the fourth value and states that placement and seat layer are one
axis — **which is exactly what Conflict 5 asks him to confirm.** Do not apply
without that answer; if placement is a separate axis it needs a different word,
not these four.

`design/Flows/flowCliPoc.md:11-12` ("it shares one database across primary,
secondary, and tertiary") and `PRIMARY-SKELETON.md:493` ("These checks must work
from primary, secondary, and tertiary") gain `quaternary` on the same ruling.

## D5. `tools/main-flow-mode/system-prompt.md` and the twelve-seat count

Covered in C4. Repeated here because it is authored prose, not code: "one of the
twelve seats" is in tension with Conflict 4 and with Conflict 3's fifth layer.
Three aspects times four layers is twelve; times five is fifteen; three aspects
times three standing layers is nine. The number should not be written down
again until he rules.

## D6. Typed enums elsewhere that use these words on a different axis

`flows/f55ec8/handoff/successors-v7/sources/f55ec8/reports/messagingBrief.md:149`
and `:181`, and `flows/b49251/handoff/psyche-medium-v1/claude-base.md:4367`,
`:4399`, `:4436`:

    ClusterTarget.[Primary Secondary Core]
    FlowRole.[Primary Secondary Core Successor]

Three values, pairing Primary and Secondary with `Core` — which Conflict 3 now
identifies as layer 0. These are in handoff copies of reports, not live types, so
nothing is proposed. But they are evidence that `Core` belongs in the layer
enum, and if either type is ever implemented it must use the ruled names.

Encouragingly, `flows/b49251/reports/ideaBook-flowLaunching.md:63` already
proposes exactly the type this rename needs:

    Layer.[ Primary Secondary Tertiary Quaternary ]

and `flows/b49251/handoff/psyche-medium-v1/index_read.py:17` already implements
it as `LAYER = ('Primary', 'Secondary', 'Tertiary', 'Quaternary')`. The C1
proposal matches both.
---

# E. The repository named `primary`

The living, 2026-09-26, after the rename question was raised:

> But we could just put a note in the README or something. I don't know. The
> idea was that primary was the primary's workspace and that's sort of the
> highest layer but I see now it's not that simple because we aren't there yet,
> where we can spawn a different file system for every flow. We're going to get
> there.

So: **a note, not a rename.** The inventory and candidates below are kept only
as reference should he later want the rename.

Note his "that's sort of the highest layer" sits against Conflict 3: by his own
09-14 naming the highest layer is `core`, layer 0, and the primary is the one he
talks to most. The README text below says "the primary layer" and does not claim
it is the highest, which keeps it true either way.

## E1. Primary has no README

`ls README*` in `/home/li/primary` returns nothing, so the note needs a new
file, `README.md`. The `psyche` skill already anticipates one: "Primary Next
begins from Primary's root commit and carries selected repository mounting
points plus a README and AGENTS.md explaining those relationships."

## E2. Proposed `README.md`, exact text

    # Primary

    This repository is named for the primary layer. A flow's position in its
    aspect is its layer — primary, secondary, tertiary, quaternary — and the
    primary is the flow of broad consideration, bothered least. The name records
    the intent that this tree be the primary's own workspace.

    It is not that yet. Every flow, at every layer and in every aspect, works in
    this one tree, through worktrees under `/home/li/wt/primary/<flow-id>`.
    Spawning a separate filesystem for every flow is the direction; we are not
    there.

    Until then the name of this tree names no flow's layer. A flow reads its own
    layer from its startup prompt, never from the path it is standing in.

    > The idea was that primary was the primary's workspace and that's sort of
    > the highest layer but I see now it's not that simple because we aren't
    > there yet, where we can spawn a different file system for every flow.
    > We're going to get there.
    >
    > -- the living, 2026-09-26

The third paragraph is the load-bearing one: it is the only line that stops a
flow reading `/home/li/primary` as a statement about itself. If the note must be
shorter, that paragraph is the one to keep.

The per-flow-filesystem direction is worked out in
`flows/e167d8/reports/per-flow-workspaces-design.md`; the README deliberately
does not restate it.

## E3. Rename inventory — reference only

A companion sweep measured the surface. **5,430** occurrences of the literal
`/home/li/primary` in tracked files, of which **5,285 (97.3%)** are in
historical record trees that would not be rewritten (`flows/`,
`agent-outputs/`, `reports/`, `.beads/`, `sessions/`, `.native-seat-receipts/`,
`.pi/continue/`). The operational surface is small:

| Category | Sites |
| --- | --- |
| Executables, launchers, units inside the repo | 21 lines in 11 files |
| Same, in sibling repos (CriomOS, CriomOS-home, field, flow, mind) | 11 lines in 7 files |
| Live user systemd units outside any repo | 2 |
| Harness config files (`.claude.json`, `.codex/config.toml`, `.codex-next/config.toml`) | 2 files, ~21 keys |
| Authored prose meaning the repository | 12 root-doc lines, `Vision/psyche.md:17-18`, `protocols/active-repositories.md:25` |
| Curriculum skills naming the path or URL | **0** |

The items most likely to be missed:

- **`tools/field-census.mjs:94`** keys a status-line regex on the checkout's
  basename — `/primary main@/` — because `/home/li/.claude/statusline.sh:50`
  renders `basename "$cwd"`. A rename breaks this silently, with no error.
- **The bead prefix.** `.beads/config.yaml` leaves `issue-prefix` unset, so `bd`
  auto-detects it from the directory name. Every existing ID is `primary-*`
  (197 in `.beads/export.jsonl`, and IDs cited across CriomOS, CriomOS-home and
  Curriculum). A rename silently changes the prefix for new beads unless
  `issue-prefix: "primary"` is pinned first.
- **`config/` and `skills/` are separate checkouts of `LiGoldragon/primary`
  itself** and both must be re-pointed.
- **`.git/config [core] hooksPath`** is absolute (`/home/li/primary/.git/hooks`)
  and breaks on a move; `.jj/repo/store/git_target` is relative and survives.
- **`/home/li/.claude/projects/-home-li-primary`** holds 272 transcripts, and 26
  project directories in total encode `primary` in their path; 170 other files
  under `/home/li/.claude` reference the path. `/home/li/.codex/sessions` has
  **2,977** session files recording it as `cwd`. These are records; a rename
  orphans them rather than breaking them.
- **The flake input** is `prompt-relay-source` in
  `CriomOS-home/flake.nix:20-23`, pointing at `github:LiGoldragon/primary/<rev>`
  — the attribute name does not contain "primary", so a grep for the input name
  misses it. `flake.lock` nodes carry `"repo": "primary"` in CriomOS-home and
  transitively in CriomOS.
- **`/git/github.com/LiGoldragon/primary-next`** already exists as a full
  sibling copy with its own `SKILL_VARIABLES.md` and `README.md` referencing
  `/home/li/primary`.
- **Ten derivation names** in `/home/li/primary/flake.nix` begin `primary-`
  (`:60`, `:136`–`:184`), and `:2`'s description says "primary workspace".
- `SKILL_VARIABLES.md` declares the Claude, Codex and Curriculum roots but
  **has no entry for Primary's own root** — a rename would likely need one added.
- Five live worktrees carry `primary` in their path
  (`/home/li/wt/primary/{e167d8,mind-vision-00f95a,mind-vision-main-00f95a}`,
  `/home/li/wt/github.com/LiGoldragon/primary/{messenger-plural-projection-00f95a,cf7879-report-recovery}`),
  each with its own generated `.agents/ .claude/ .codex/ .pi/` trees.

Known false positives not to touch: `openai-primary-runtime` plugin ids in both
Codex configs; `PRIMARY KEY` in `tools/flow-cli-poc/flow.py:9-13`;
`rateLimits.primary` in `tools/field-census.mjs:356,362`; `ghostty-primary-selection`
and `gtk-enable-primary-paste` in CriomOS-home; `PrimaryConnection` in the
noctalia plugins.

## E4. Three candidate names, no verdict

**`workspace`** — says what the tree is, not who owns it. Pro: collides with no
layer, aspect, model or effort word; reads correctly as `/home/li/workspace`.
Con: generic to the point of saying nothing, and `/home/li/wt` already holds
worktrees that would read as workspaces inside a workspace. Also changes the
bead prefix to `workspace-`, which is long.

**`hull`** — the living's own word, from
`flows/b05237/vision/operational-responseAnatomyAndPowerAllocation.md`: "It's
left to the judgment of the hull to decide how much thinking power we send on
the subflows." Pro: his vocabulary, short, distinctive, no collision, and a
four-character bead prefix. Con: its referent was never defined — he used it for
the thing that *allocates*, which may be Flow or Nexus rather than the
repository, so naming the repo `hull` would fix a possibly wrong meaning to the
word before he has ruled on it.

**`primary-next`** — the name already chartered for the successor tree, which
exists on disk and on GitHub. Pro: costs no new vocabulary and the migration is
already planned, so the rename rides a move already intended rather than adding
one. Con: it keeps the colliding word, adds a suffix that ages badly, and
conflates "the repository after this one" with "the repository not named for a
layer" — two different changes.

---

# F. Other meanings of primary / secondary / tertiary / quaternary

Raw whole-word counts in Primary plus the Curriculum skills: `primary` 19,503;
`secondary` 1,200; `tertiary` 215; `quaternary` 148. The misspelling
`quartenary` appears nowhere. `tertiary` and `quaternary` are nearly clean — 38
of 215 and 10 of 148 hits are already "tertiary/quaternary layer", and the only
foreign senses are one medical phrase and one commit hash.

## F1. Must change — collides with the layer meaning

**"primary Psyche / Codex / Claude / Mind / flow" meaning *the main seat*.**
~2,100 occurrences; the meaning is "the main one of this cluster", independent
of layer. The damaging cases are in authored source and are proposed above:
`roles/codex-primary.md:1,11` and `roles/codex-{medium,low}.md:13` (D1–D3),
`tools/compose-seat-prompt.py:31,80,93` (C4), `Curriculum/skills/field.md:27`
(Conflict 2). `tools/compose-seat-prompt.py:80` is the worst single line —
"primary Psyche opus (medium-power)" names the *secondary* seat and calls it
primary.

**`Curriculum/skills/field.md:27` "Primary Field"** — see Conflict 2. Authored
source; must change or the vocabulary contradicts itself on arrival. Note
`field/README.md:4,6` uses "Primary Field" for the *repository's* Field tools,
a third meaning again; that one is safe because it is clearly about tooling.

**`tools/compose-seat-prompt.py:58,70`** — "the tertiary layer's mind
counterpart" / "the quaternary layer" attached to medium and low Codex. Conflict
1; cannot be written either way until he rules.

**`design/Flows/flowCliPoc.md:49` placement layer** — Conflict 5; three values
where there are four, and an explicit claim that it is a separate axis.

After the rename, the fix for the whole class is the convention in the header:
main-ness is said with "main", never "primary".

## F2. Safe — a different domain, no flow would confuse it

**The private-part charter** (`CLAUDE.md:35`, `AGENTS.md:47`,
`flows/6cc91b/vision/privateLayer.md:7`): "The primary private talks to the
secondary private". Safe and better than safe — this is the **same** meaning,
and together with the 09-14 records it is the evidence for Conflict 3's fifth
layer. No change.

**The bead ID prefix `primary-`** (~6,175 occurrences; `primary-751`,
`primary-99n`, `primary-x8by`...). Safe: a bead ID is always a token with a
suffix, never a bare word, and `NON_MANAGEMENT_AGENTS.md:32` already teaches the
form. It does make a bare grep for the layer name impractical, so any future
audit must exclude `primary-`. No change, but see E3 on pinning the prefix.

**"Primary is always committed"** (`CLAUDE.md:20`, `AGENTS.md:20`) and
`Vision/psyche.md:17-18`, `ARCHITECTURE.md:1,14,420`, `NON_IDEAL_AGENTS.md:1,4`,
`protocols/active-repositories.md:25`, `primary.code-workspace:4`. Safe:
capital-P Primary reading as the repository is established throughout, and the
README note (E2) is precisely what makes that reading explicit rather than
assumed. No change; the note is the fix.

**"Primary working directory: /home/li/primary"** — injected by the harness into
every prompt. Safe: "primary" there is the harness's adjective for the cwd among
several, in vendor parlance. It is a triple pun with the repo name and the layer
name, and it is also unavoidable, which is a second reason the README note earns
its place.

**`PRIMARY KEY`** (SQL, 13 sites, all in `tools/flow-cli-poc/flow.py` and
quoted schemas) and **secondary index / secondary key** (4 sites in
`agent-outputs/Spirit*`). Safe: SQL and storage vocabulary.

**"secondary default" route** (`flows/6db4fe/reports/network-chain-attempts.md:9`)
and **"primary disk" / "primary interface"** (6 sites in reports). Safe:
networking and hardware. No `secondary DNS`, `secondary disk` or
`secondary storage` occurs at all.

**"secondary cluster" = a set of machines** (`flows/05c604/vision/cluster.md:3,7`,
7 sites). Safe: names hosts, not seats. Authored raw vision, unchanged.

**"secondary files" = `@`-included entry files**
(`flows/15b67974/vision/entryFiles.md:1,8`, 11 sites). Safe: "auxiliary,
included by reference", a stratum not a layer. Authored raw vision, unchanged.

**"primary/secondary source"** (research provenance, ~89 sites), **"primary
design artifact"** (`vision-raw/worldModelBeforeCode.md:24,36`), **"primary
failure mode"** (`awareness/stewardship.md:11`), **"secondary review"**
(`flows/908786/reports/fable-launch.md:38`), **"secondary projections"**
(`reports/logos/textual-form-vision-design-v2.md:309`), **"tertiary GI clinics"**
(`agent-outputs/BookOfSol-grain-research/rice-and-wheat-gaps.md:1256`). Safe:
ordinary English. Unrescuable by any rename and not worth trying.

**`openai-primary-runtime`** plugin ids in both Codex configs,
**`ghostty-primary-selection`**, **`gtk-enable-primary-paste`**,
**`PrimaryConnection`**, **`rateLimits.primary`**. Safe: third-party names.

**Effort words throughout** — `claude-harness.md:78`
(`/effort low|medium|high|xhigh`), "medium reasoning effort" (`field.md:25`),
"at medium effort" (`main-flow.md:14`, `field.md:19`), `SKILL_VARIABLES.md:6`'s
*value* `medium`, "Luna at light" (`flows/b860be/vision/mainRoles.md`). Safe and
deliberately untouched: after the rename these are the **only** users of
low/medium/high, which is the entire point.

**`herdr.md:30` "tier-priority"** — the multiplexer's own scheduling term. Safe.

**`operators-notes.md:13` "approval tier"** — the skill-authority axis
(`testing-` / `operational-` / no prefix). Safe, but it is the last "tier" left
standing; if he wants the word retired outright it becomes "approval level".

## F3. Not found

No primary/secondary DNS, disk, partition, storage, or git remote sense. The
domains that usually supply competing meanings are simply absent, which is why
F1 is as short as it is.

---

# Counts

| Category | Sites | Authority |
| --- | --- | --- |
| Curriculum authored skills | 13 files, 32 lines | the living's approval of exact text |
| `roles/` and `design/` authored source | 4 files, 11 lines | the living's word |
| `Vision/` and `Intent/` | 4 files, 14 lines + 2 new statements | the living's word |
| `SKILL_VARIABLES.md` | 3 lines (no consumer) | the living's word |
| `signal-flow` ethos type | 1 line, 2 fragments | versioned, wire-breaking |
| `flow-nexus` Rust | 5 files, 16 sites | versioned, same release as the ethos |
| `tools/` non-test | 8 files, 27 sites | versioned; 2 carry a persisted-schema break |
| `tools/` tests | 6 files, 30 sites | versioned, same commit as their code |
| New `README.md` | 1 new file | the living's approval of exact text |
| Raw records, receipts, transcripts | 23+ files, ~5,285 path lines | never changed; they are the record |
| Other-meaning sites that must change | 6 lines across 3 files | as their category |
| Other-meaning sites judged safe | 16 meanings | no change |

Blocked on a ruling: **everything in C, D1–D4 and Conflict 2** depends on
Conflict 1. The mapping must be settled before any of it is written.

# Order of work, if approved

1. He rules Conflict 1 (medium → secondary or tertiary), Conflict 3 (is `Core`
   in the enum), Conflict 4 (standing quaternary), Conflict 5 (is placement the
   same axis). Nothing below can be written coherently first.
2. `vocabulary.md` gains the layer statement (A13); `Vision/modelRoles.md` gains
   the distilled ruling (B6).
3. The remaining skill, `roles/`, `Vision/` and `Intent/` lines as one approved
   set, with redundant lines cut rather than reworded.
4. `SKILL_VARIABLES.md`, or deletion of the three orphan variables.
5. `signal-flow` ethos, regeneration, release; then the Cargo rev bump at
   `flow/Cargo.toml:17` and the `flow-nexus` rename, in one deploy. Nothing in
   Primary compiles in between.
6. `tools/` and their tests, with a schema version bump and migration for the two
   roster files.
7. `README.md`.
8. Regenerate `.agents/`, `.claude/`, `.codex/`, `.pi/` from the Curriculum
   skills. None of those trees is edited directly at any step.

# Questions for the living

1. **Does medium become the secondary or the tertiary?** `roles/` and
   `compose-seat-prompt.py` already say tertiary, by function; the brief says
   secondary, by position. This decides what `Mind Sol` is called and blocks
   every code change.
2. **Is `core` / layer 0 part of the enum?** Your 09-14 naming is five deep with
   core above primary, and the private part is chartered for it. Four variants
   now, or five?
3. **Is there a standing quaternary seat**, or is the grid nine cells with
   quaternary temporary and special-function? Twelve seats, fifteen, or nine?
4. **Is placement the same axis as the seat layer?** `flowCliPoc.md:49` treats
   them as different things using the same words.
5. Should the energy reading — "high because it's literally how much energy
   we're spending" — survive as a sentence in `Vision/modelRoles.md`, or go with
   the old words?
6. Are "rung" and "tier" retired along with "power", or kept for the vertical
   step between layers?
7. Does the native title carry the layer or the model? `refresh.md:15` and
   `correction.md:14` say `<Aspect> <Layer> <FLOW_ID>`; `main-flow.md:37` and
   `testing-flow-titles.md:6` say the layer never appears in the title. This
   contradiction predates the rename.
8. The tmux session name `primary-mind` in `tools/compose-seat-prompt.py:31`:
   keep, or change with the README note?
