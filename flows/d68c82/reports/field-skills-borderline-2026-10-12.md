# Field-skills borderline items, 2026-10-12

Lines left unchanged in `Field skills` because it could not be told
whether they are the living's psyche or a needed machine rule, or
whether removing them loses something. Each item gives the skill, the
exact lines, the line it may duplicate or conflict with, and the
question to put to him.

## 1. Local models on one named host

Skill: `compensation-default-effort`.

    Local model hosting and its files live only on Prometheus. This does not
    constrain vendor inference.

May conflict with `compensation-behavior`: "Anything that differs between
setups — a path, a repository, a host — must be a skill variable." The
host name comes from his raw words in
`flows/b7da5d/vision/modelPlacement.md` (2026-09-26): "There must never
be AI models on any other node than Prometheus".

Question: Local AI models may live only on Prometheus. Should the skill
keep the name Prometheus, or name it through a setup value such as "the
model host", so that another setup can use another machine?

## 2. The refresh threshold as a fixed number

Skill: `compensation-launch`.

    A flow at or above 30% of its observed context window, or 200,000
    observed tokens, receives no further work.

May conflict with `vision-flow`: "A flow is refreshed when its context
passes the layer's threshold". His raw words give two figures:
`flows/f55ec8/vision/flowRefresh.md` ("30% of your context as a Fable
agent, right? That's 300,000 tokens") and
`flows/b80e55/vision/refreshThresholdAndCacheSnapshot.md` ("above 30%,
like 200,000 to 300,000 tokens").

Question: A flow stops receiving work when its context is nearly full.
Should that limit be one number for every flow (30%, or 200,000
tokens), or a separate number for each layer, set in Flow's
configuration?

## 3. The contact-discipline skill, which no launcher delivers

Skill: `trial-contact-discipline` (marked user-only, so no flow can
load it, and no launcher or Curriculum role lists it, so no flow
receives it).

    Tell the Psyche Primary that its user-only status makes his approval necessary. The Primaries receive prepared packages when their judgment is relevant; their time is reserved for important matters. The living chooses the recipient directly. Routing examples are guidance, never a universal only-questions rule.

May duplicate `compensation-launch`: "A flow that hands work to a
Primary ... sends all of it in one message." The other sentences match
no vision line, and their meaning is unclear.

Question: This skill tells flows how to approach the Primaries. Nothing
delivers it today. Do its sentences carry something you said, for
example that you alone pick which Primary a matter goes to? If they do,
what should they say; if not, may the skill be deleted?

## 4. Messages addressed by flow id

Skill: `compensation-messenger-clj`.

    TARGET is the recipient's six-character flow id.

May conflict with his raw words in `flows/d68c82/vision/messaging.md`
(2026-10-12): "I've asked for the flow ID of the sender to be replaced by
the actual aspect (like how we name metaflows: aspect, topic, and then
layer). That's how I want flows to stop referring to each other by flow
IDs". The line describes what `hm-send` accepts today.

Question: A flow sends a message today by naming the recipient's
six-character id. Should a flow instead name the recipient by aspect,
topic and layer, for example `{ Psyche core Secondary }`, with the tool
changed to accept that?

## 5. Short text in a book's opening

Skill: `compensation-book-distillation`.

    A book opens with its context as figures, with any text a few short lines inside them, then goes straight to the proposals.

and, in the first paragraph, "a book carries no survey; its context
serves the proposals that follow."

May pull against his raw words in `flows/d68c82/vision/books.md`
(2026-10-12, on «Anatomy audit»): "It's too dense. The machine thinks
that I know a bunch of things ... bits of text so dense that I have to
guess what the context is."

Question: Books are to open with pictures and very little text. When a
proposal needs background you may not have, should the book explain it
in full sentences beside the proposal, even if that makes the book
longer?

## 6. Code layout in books

Skill: `compensation-book-distillation`.

    Code never sits in a nested or indented column.

May read as conflicting with Mind's `operation-flashbook`: "Arrange
ethos and datom blocks vertically, with every nested bracket on its own
indented line".

Question: Does "never in an indented column" mean that a code block
always spans the page's full width, while the code inside it may still
indent its nested brackets?

## 7. The successor's opening context

Skill: `trial-succession`.

    Carry one concentrated vision block with the verbatim psyche from the last three flows.

May conflict with `vision-flow`: a flow nearing its limit "is told,
writes its handover, and is replaced". "Concentrated" and "verbatim"
also pull in two directions.

Question: When a flow is replaced, should its successor start from the
handover the old flow writes, from your exact words in the last three
flows, or from both?
