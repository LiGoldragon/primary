<!-- to-the-living:start -->
Presentation.{ «Flow: Nexus, ethos and design, 2nd edition» }

# Flow: Nexus, ethos and design

This book is about Flow and the Nexus: which harness Flow starts, typed subflows, expression flows, a response turned into a presentation, and how a Nexus is configured and built. Where the first edition offered choices, each proposal takes one reading for you to land, amend or reject. The line on books showing code is left out, since books now carry no code.

## Proposal 1: psyche-context › skills/vision-flow.md

+ For now, Flow launches an existing harness.
+ The custom harness to come takes in, and gives out, 100% typed datom messages.
+ A main flow may run subflows in other harnesses too, or start a specialized main flow.

Ruling: land, amend, or reject.

## Proposal 2: psyche-context › skills/vision-flow.md

+ A subflow has a type, written in datom for Flow, preprogrammed to know everything its specialty needs, so that nothing of how to behave is told to it.
+ The launch gives it the job, its type and the context modules injected into its prompt; one simple command starts it, and it answers back to the flow that launched it.

Ruling: land, amend, or reject.

## Proposal 3: psyche-context › skills/vision-model-roles.md

+ An expression flow expresses an idea, on the same models, at a level matched to it.
+ A low expression gets a quick concept out, and a cheap one serves a proof of concept.
+ A medium expression is for a new thing, an agent coming up with an idea.
+ A high-powered, or high, expression is the third.
+ An expression level is a kind of flow, not an effort setting.
+ An expression flow is assigned to the concept it represents, mostly a single flow to a single concept, reused at most to bring changes afterwards.

Ruling: land, amend, or reject.

## Proposal 4: psyche-context › skills/vision-flow.md

+ A tool is sent to a session: a thinking-machine call told what to look for, the time the response was printed or a few keywords, which finds the response and turns it into a visualization report.
+ Any Claude agent can make it, on a low layer.
+ A high-powered psyche flow has that service done automatically, its intricate answers turned into a visualization by a low expression unless asked explicitly.
+ Any flow the living asks to put a response into a presentation gets it, and the living comments on it.
+ The signal goes back to Flow, which starts a flow or reaches one already running.
+ What the living has said involves a Psyche flow.

Ruling: land, amend, or reject.

## Proposal 5: psyche-context › skills/vision-flow.md

+ For now Flow does no sandboxing: a sandbox is set up for testing outside Flow.

Ruling: land, amend, or reject.

## Proposal 6: psyche-context › skills/vision-flow.md

+ A flow id is also written in words: three, maybe even two.
+ In the chat a flow is named by its metaflow, and the flow id almost disappears; it is for the ledger and for finding the transcript.

Ruling: land, amend, or reject.

## Proposal 7: psyche-context › skills/vision-flow.md

+ Work is kept track of by its flows: each implementation has a flow or metaflow of its own, each at its own layer.

Ruling: land, amend, or reject.

## Proposal 8: psyche-context › skills/vision-flow.md

+ Flow's memory is Flow's own; Mind uses the flow data Flow records for its memory, and so becomes the most bloated component in terms of the database.

Ruling: land, amend, or reject.

## Proposal 9: psyche-context › skills/vision-nexus.md

+ A Nexus's objects describe its processes; «process» is not said each time, since being a Nexus object implies it.
+ A Nexus object runs only inside a Nexus meta-actor, as a flow is the actor inside the runtime.
+ A sub-process is defined as more objects, among them a Nexus object that is an actor.
+ An effect is a Nexus process: an internal algorithm over data, or a wrapped command line such as Nix.

Ruling: land, amend, or reject.

## Proposal 10: psyche-context › skills/vision-nexus.md

+ For now, a hack to get a Nexus started: its configuration is loaded atomically from files, datom payloads for configuring that Nexus, kept in separate files in different repositories and at different layers.
+ The meta CLI is given them in succession on the meta socket, to start the Nexus with the right payload, so that datom path expansion need not be solved yet.
+ A registry is populated the same way, from datom files in the repositories, each updated by whoever updates its repository, loaded together into one registry.

Ruling: land, amend, or reject.

## Proposal 11: psyche-context › skills/vision-nexus.md

+ One shared library, used by many nexuses, identifies the calling process of a CLI, so that the code is not rewritten for every CLI and reads at a glance.
+ It runs in the background whenever a CLI is used, neither user-facing nor configurable, and may be on all CLIs.

Ruling: land, amend, or reject.

## Proposal 12: psyche-context › skills/vision-protos.md

+ ## The identifier made of words
+ An identifier names what agents or humans must identify: anything user-facing that is named through judgment, a topic among them.
+ It is more than one word, camelCase and uncapitalized, which tells it apart from a variant.
+ It is a variant created on demand, more descriptive, with nothing recompiled to add one.
+ It lives in a shared library, used in more than one dialect, and is checked when created.

Ruling: land, amend, or reject.

## Proposal 13: psyche-context › skills/vision-nexus.md

+ The three parts, and how each is divided, are the bulk of the machine's anatomy: the pieces to define in the system.
+ One good Nexus comes first, with all its types and all its traits well defined; Flow is the most needed.

Ruling: land, amend, or reject.

## Proposal 14: psyche-context › skills/vision-book.md

+ A book's code is implemented before the living comments, and modified when the comment comes; its psyche-module lines land on the comment.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
