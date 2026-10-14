<!-- to-the-living:start -->
Presentation.{ «Nexus, ethos and design» }

# Nexus, ethos and design

## Crystallization

### Proposal 1: an existing harness for now; a custom one later, typed through

2026-08-21, `flows/15b67974/vision/flowDaemon.md`, typed: «yes for now.
we will create our own custom harness in the future, which will be 100%
typed datom messages going in and being expected out.»

2026-09-16, `flows/b49251/vision/flowLaunching.md`, typed: «We won't
always necessarily run just these kinds of flows in the cluster. Each
main flow can run subflows in other harnesses too if it wants, or start
a specialized main flow, which we'll start to implement now, like
implement this Nexus concept.»

Sources: `flows/15b67974/vision/flowDaemon.md`, 2026-08-21;
`flows/b49251/vision/flowLaunching.md`, 2026-09-16;
`flows/8475a9/vision/flow.md`, 2026-10-06 (spawning automated, Field now
and not forever: «book 05» Proposal 4, pending).

File: `psyche-context/skills/vision-flow.md` («Starting flows», after
its first paragraph; «for now» and «in the future» are his marks)

```text
  A Nexus component decides the system prompt and everything about a
  launch, replacing the harness's subagents with specialized harnesses
  launched with specialized system prompts.
+
+ Flow launches an existing harness for now; the custom harness to come in the future takes in, and gives out, 100% typed datom messages. A main flow may run subflows in other harnesses too, or start a specialized main flow.
```

Ruling, one number from each group:

The paragraph:
1. Land.
2. Land with changes the living names.
3. Drop.

The marks; his words carry «for now» and «in the future»:
4. One paragraph, as shown: the short-term and the long-term sentence
   side by side, each marked by his word.
5. Two lines, machine choice: the short-term sentence stands alone,
   marked, and is removed when the custom harness stands; the
   long-term sentence stands unmarked:

File: `psyche-context/skills/vision-flow.md` (under choice 5, in place
of the paragraph above)

```text
+ For now, Flow launches an existing harness.
+
+ The custom harness takes in, and gives out, 100% typed datom messages. A main flow may run subflows in other harnesses too, or start a specialized main flow.
```

### Proposal 2: typed subflows, written in datom for Flow

2026-09-15, `flows/fd0f97/vision/flowTypes.md`, typed: «You should have
a simple command to start a Codex subflow that will answer back to you
and not have to. It should be lighter for you to write one subflow
through the Datom language for Flow, because you have different types,
and they're all preprogrammed to know everything they need to know. You
don't have to tell them how to behave. You just give them the job for
their specialty, and they're off and going.»; «Launching a Codex of a
certain type, like an audit or whatever, a particular kind of audit,
even, or a special kind of Flow for transferring contexts or for editing
content context of a session script or whatever, then you can just give
it which vision files you want injected in the prompt.»

Sources: `flows/fd0f97/vision/flowTypes.md`, 2026-09-15;
`flows/b49251/vision/flowLaunching.md`, 2026-09-16 (Proposal 1);
vision-flow L30 (a launch names the metaflow, the context modules and a
brief: landed) and L62–67 (a subflow runs under its own system prompt:
landed). The `Specialty` type of a role is «book 08» Proposal 2's,
pending, in `flow/crates/flow-ethos/ethos/library.ethos`; no code line
is added here.

File: `psyche-context/skills/vision-flow.md` («Subflows replace the
harness subagent facility», after its paragraph; the figure under it)

```text
  prompt, which can reply to the successor of whoever it was meant to
  answer; that makes the system asynchronous. Subflows run under their
  own system prompts because they need different prompts.
+
+ A subflow has a type, written in datom for Flow, preprogrammed to know everything its specialty needs, so that nothing of how to behave is told to it: the launch gives it the job, its type and the vision files injected into its prompt, one simple command starts it, and it answers back to the flow that launched it.
+
+ +----------------------+
+ | the main flow        |
+ +----------------------+
+    | gives: the job, the type, the files
+    v
+ +----------------------+
+ | Flow                 |
+ +----------------------+
+    | starts, preprogrammed for its specialty
+    v
+ +----------------------+
+ | the typed subflow    |
+ +----------------------+
+    | answers back
+    v
+ +----------------------+
+ | the main flow        |
+ +----------------------+
```

Ruling, one number from each group:

The paragraph and the figure:
1. Land.
2. Land with changes the living names.
3. Drop.

«the vision files»; his 2026-09-15 words say vision files, and
vision-flow L30, landed later, says context modules:
4. «the vision files», as shown, his words.
5. «the context modules», machine reading: the vision files a launch
   injects are the context modules of L30, which the launch names.

The harness of the subflow; his words say «a Codex subflow», and
Proposal 1's words say subflows run in other harnesses too:
6. No harness named, as shown, machine reading of the two records
   together.
7. «a Codex subflow», his 2026-09-15 words.

### Proposal 3: expression at three levels

2026-09-16, `flows/b49251/vision/flowLaunching.md`, typed: «Let's make
this another kind of flow. It's like the expression flow, and they
express an idea. He could get one started, and they have both the opus
and Sol variant.»; «I guess you can even have a cheap idea expression
for proof of concept. If it's a new thing and it's just an agent coming
up with an idea, then we can do a medium expression. That would be a
medium expression. You could have a high-powered expression, I guess you
would call it, or high expression. I don't know which one is better. The
same models, and you could have a low expression to get a quick concept
out. These are sort of assigned by the concept they're representing, so
they could be reused, maybe, to bring changes afterwards, but they're
mostly just a single flow to a single concept otherwise.»

2026-09-16, `flows/b49251/vision/psycheFlows.md`, typed: «There
are going to be three levels of psyche flows: low, medium, and high
effort.»; «there should be a subflow that checks for intricate answers
from you and turns them into a visualization with an expression flow. If
it wasn't asked explicitly, it just uses a low-effort flow for that.»

Sources: `flows/b49251/vision/flowLaunching.md`, 2026-09-16;
`flows/b49251/vision/psycheFlows.md`, 2026-09-16. No line on the
expression flow stands in vision-flow or vision-model-roles.

File: `psyche-context/skills/vision-model-roles.md` (another topic's
skill: vision-model-roles; after L17)

```text
  Every seat runs at medium effort, except the OpenAI Quaternary.
+
+ An expression flow expresses an idea, on the same models, at a level matched to it: a low expression gets a quick concept out, a cheap one serves a proof of concept; a medium expression is for a new thing, an agent coming up with an idea; a high-powered, or high, expression is the third. A high-powered psyche flow has its intricate answers turned into a visualization by an expression flow, low-effort unless asked explicitly. An expression flow is assigned to the concept it represents, mostly a single flow to a single concept, reused at most to bring changes afterwards.
```

Ruling, one number from each group:

The paragraph:
1. Land.
2. Land with changes the living names.
3. Drop.

The third level's name; his words leave it open («I don't know which
one is better»):
4. «high-powered, or high», both, as shown.
5. «high expression».
6. «high-powered expression».

The levels against L17 «Every seat runs at medium effort, except the
OpenAI Quaternary.» and intent-models L8–12 «Capability comes from
choosing a better model, not from raising a model's effort setting. … it
is never raised to buy quality.», both landed; his 2026-09-16 words say
«low, medium, and high effort» and «a low-effort flow». The three
choices are the machine's:
7. An expression level is a kind of flow, not an effort setting: L17
   and intent-models stand, the paragraph as shown; intent-models
   L16–18 already holds the two scales apart.
8. The effort setting differs by expression level; L17 changed:

File: `psyche-context/skills/vision-model-roles.md` (L17, under
choice 8)

```text
- Every seat runs at medium effort, except the OpenAI Quaternary.
+ Every seat runs at medium effort, except the OpenAI Quaternary and an expression flow, whose effort is its level.
```

9. No line on levels: the paragraph keeps its first and last sentence
   only.

### Proposal 4: a response turned into a presentation; the session tool

2026-09-16, `flows/b49251/vision/flowLaunching.md` (the record says
typed and carries the transcription brackets as the record has them: a
machine fact): «There's this tool that can be sent to a session. It's
going to be a machine thinking machine call, but it's going to have a
certain kind of instruction of what to look for. Maybe it knows exactly
the time when the thinking machine printed that response, or maybe it
has a few keywords or something, but some kind of indication to find it
and then turn that into a visualization report, as we've been doing
them, which can be put together by any Claude [transcribed "cloud"]
agent. Even a Sonnet can do it, right? As long as we can have a
low-effort mode, that's what I'm saying.»

«For that, for presenting ideas quickly, that flows like the
high-powered psychic agent should automatically have that service done
for them. For any agent that I ask, like, "Oh, here's an interesting
response. Put that together into a presentation," then I can comment on
it. Ideally, this signal goes back to the right Herder [transcribed
"Hardbey"] agent that can then start a flow or contact an already
existing flow.»

«For what I've said, it's probably going to involve a Psyche flow
because if I've said something, then the Psyche is involved.»

The Herder: the name he once gave the component that launches flows, now
Flow; the reading is the machine's.

Sources: `flows/b49251/vision/flowLaunching.md`, 2026-09-16;
`flows/b49251/vision/psycheFlows.md`, 2026-09-16 (Proposal 3);
vision-flow L56 (a marked block in a transcript becomes an action, a
book among them: landed).

File: `psyche-context/skills/vision-flow.md` (after L56; the figure
under it; the order of its boxes is the machine's reading of the
three quotes)

```text
  Every harness event reaches Flow through the harness's hooks calling the Flow CLI, so Flow knows each flow's state without polling; a marked block landing in a transcript becomes an action, a book among them, with no tool call by the flow; a flow nearing its context limit is told, writes its handover, and is refreshed as it goes idle. Polling is forbidden; a poller that must exist is registered and reported.
+
+ A tool is sent to a session: a thinking-machine call with an instruction of what to look for, the time the response was printed or a few keywords, which finds the response and turns it into a visualization report, by any Claude agent in a low-effort mode. A high-powered psyche flow has that service done automatically; any flow the living asks to put a response into a presentation gets it, and the living comments on it; the signal goes back to Flow, which starts a flow or reaches one already running. What the living has said involves a Psyche flow.
+
+ +----------------------+
+ | the living           |
+ +----------------------+
+    | asks: put that response in a presentation
+    v
+ +----------------------+
+ | Flow, the Herder     |
+ +----------------------+
+    | starts a flow, or reaches one running
+    v
+ +----------------------+
+ | a Psyche flow        |
+ +----------------------+
+    | sends the tool to the session
+    v
+ +----------------------+
+ | the session tool, a  |
+ | thinking-machine call|
+ +----------------------+
+    | finds the response: a time, keywords
+    | turns it into a visualization report
+    v
+ +----------------------+
+ | the living, who      |
+ | comments             |
+ +----------------------+
```

Ruling, one number from each group:

The paragraph and the figure:
1. Land.
2. Land with changes the living names.
3. Drop.

`[transcribed "cloud"]`:
4. Claude, as shown: «any Claude agent».
5. Another reading the living names.

`[transcribed "Hardbey"]`:
6. Herder, read as Flow, as shown: «the signal goes back to Flow»,
   machine reading.
7. Herder kept as a name of its own in the line.
8. Another reading the living names.

### Proposal 5: no sandboxing in Flow for now

2026-10-03 18:10, `flows/edf227/vision/flow.md`, typed, book comment:
«No, Flow doesn't do any sandboxing for now so that's just something
that we set up for testing outside of Flow. Has nothing to do with Flow
right now»

Sources: `flows/edf227/vision/flow.md`, 2026-10-03; vision-flow L14 (the
Capsule: landed); «book 07» Proposal 5, choice 8 («Short term only; the
Capsule sandboxes long term»), pending.

File: `psyche-context/skills/vision-flow.md` (L14; his «for now» is
the mark; builds on «book 07» Proposal 5 choice 8)

```text
- The Capsule is the component that makes where a flow runs. Its first embodiment is the semi-sandbox: only the credential files are copied, everything else is recreated, with its own sockets and store, running light models. Later it encrypts the sensitive parts of the filesystem under a volatile key.
+ For now Flow does no sandboxing: a sandbox is set up for testing outside Flow. The Capsule is the component that makes where a flow runs. Its first embodiment is the semi-sandbox: only the credential files are copied, everything else is recreated, with its own sockets and store, running light models. Later it encrypts the sensitive parts of the filesystem under a volatile key.
```

Ruling, one number from each group:

The line:
1. Land.
2. Land with changes the living names.
3. Drop.

Where it stands; no word of his on this fork:
4. At the head of the Capsule paragraph, as shown, machine choice: the
   short-term sentence is read before the long-term one it suspends.
5. A paragraph of its own after L14, machine choice: the Capsule
   paragraph stays untouched when the sentence is removed.

### Proposal 6: the flow id in words

2026-10-02, `flows/01e496/vision/flowNexus.md`, typed: «Flow could have
the lock on the flows so that we can lock it and also address it by name
instead of by Flow ID. I'd also like the Flow ID to be converted into
words.» Landed in part, vision-flow L12 and L16; the words not landed.

2026-10-02, `flows/01e496/vision/flowIdentity.md`, typed: «They're just
for accounting or for the ledger, the archive side of things, and for
knowing where to search if the transcript is needed, etc.»

2026-10-07, `flows/d4ae97/vision/flow.md`, STT: «I'd rather see the
word-based one. I think it would be cool to have this word-based
translation that actually works. Let's see if we can do that with three
words, maybe even two.»; 2026-10-09, `flows/445410/vision/flow.md`, STT:
«I would like the word-based flow ID»; 2026-10-12,
`flows/d68c82/vision/messaging.md`, STT: «I've asked for the flow ID of
the sender to be replaced by the actual aspect (like how we name
metaflows: aspect, topic, and then layer). That's how I want flows to
stop referring to each other by flow IDs»; 2026-10-13,
`flows/7c89aa/vision/flow-ids.md`, STT: «I want flow IDs to almost
disappear from the chat.»

Sources: `flows/01e496/vision/flowNexus.md` and
`flows/01e496/vision/flowIdentity.md`, 2026-10-02;
`flows/d4ae97/vision/flow.md`, 2026-10-07;
`flows/445410/vision/flow.md`, 2026-10-09;
`flows/d68c82/vision/messaging.md`, 2026-10-12;
`flows/7c89aa/vision/flow-ids.md`, 2026-10-13. The word form itself is
«book 04» Proposal 2, pending (its line: «A flow id is also written as
words: the first 33 bits of the harness's session id, as words from a
published word list…»); the ids for the ledger, «book 04» Proposal 3,
pending. Machine fact: no word encoding of a flow id exists in the flow
or the protos repository.

File: `psyche-context/skills/vision-flow.md` (after L20; «book 04»
Proposal 2 adds its word-form sentence there, and the line below
follows that sentence; builds on it)

```text
  A topic's name is a camelCase identifier, uncapitalized. A flow's id is the hash of the harness's session id, so a transcript is found from the flow id. Where the harness lets Flow choose the session id, Flow chooses it before the flow starts and the flow reads it in its prompt; where the harness assigns it, Flow learns it when the flow binds. No flow declares its id: every call to Flow is identified by the calling process.
+ The words are three, maybe even two. In the chat a flow is named by its metaflow, and the flow id almost disappears; it is for the ledger and for finding the transcript.
```

Ruling, one number from each group:

The line:
1. Land.
2. Land with changes the living names.
3. Drop.

How many words; his words: «three words, maybe even two»:
4. «three, maybe even two», as shown.
5. Three: «book 04» Proposal 2's count, the machine's arithmetic (33
   bits, three words of a 2048-word list).
6. Two.

### Proposal 7: each implementation has its own metaflow

2026-10-07, `flows/d4ae97/vision/flow.md`, STT: «This is how you keep
track of your work: each implementation has its own flow or meta flow.
That's brilliant. And then each of those can have a different level:
primary, secondary, which corresponds with the model, and then we have
the actual model.»

The same words open with «This is a job for the mind, right, to document
the current environment, which is knowledge: how the tools that we have
now are working, so that the agents that are working with them can
either improve them, which is the mind. It just is a mind job not a
psyche job.»: that is «book 05» Proposal 8's line («Mind implements and
documents»), pending. Between the two: «I guess there's nothing against
using Opus sometimes for an implementation job, which is actually maybe
its own kind.»

Sources: `flows/d4ae97/vision/flow.md`, 2026-10-07; vision-flow L16 (the
metaflow: landed) and L30 (the layer decides the model: landed).

File: `psyche-context/skills/vision-flow.md` (after L16)

```text
  Flow manages metaflows. A metaflow is one address, { Aspect Topic Layer }, that continues through several flows one after another; the flow is its current run, and what is addressed is always the metaflow, never a flow. The default topic is core: the permanent topic, the thing that keeps the machine going, the last topic to stand.
+
+ Work is kept track of by its flows: each implementation has a flow or metaflow of its own, each at its own layer.
```

Ruling, one number from each group:

The line:
1. Land.
2. Land with changes the living names.
3. Drop.

«an implementation job, which is actually maybe its own kind»; a
notion, not ruled; the choices are the machine's:
4. No line, as shown.
5. A sentence added: «An implementation job is a kind of its own.»

### Proposal 8: where Flow's memory lives

2026-09-17, `flows/9993b5/vision/flowAnatomy.md`, typed: «We can map a
pretty sensible flow anatomy for the flow CLI. It's not going to be
where the memory lives, so the mind is going to use it.»; the same
message, `flows/9993b5/vision/mindMemory.md`: «But the Flow's memory
will live in mind, and so mind will become our most bloated component in
terms of the database quickly.»

2026-10-03 18:13, `flows/edf227/vision/flow.md`, typed, book comment
(«Transcription uncertain: "in every story"» in the record): «No the
configuration flow does not live in a Markdown file in every story. It
lives in its own database and its memory. That's where the configuration
goes ...»

Landed: vision-nexus L66 «Its Memory is its own typed store, reached
only through the memory engine; there is no central store; policy state
and working state live in that one store, and policy changes only over
the meta socket.»; vision-nexus L87–94 (configuration in the Nexus's own
database). The two dated records point two ways and no later word of his
joins them; the choices are the machine's.

Sources: `flows/9993b5/vision/flowAnatomy.md` and
`flows/9993b5/vision/mindMemory.md`, 2026-09-17;
`flows/edf227/vision/flow.md`, 2026-10-03.

Ruling, one number:

1. The 2026-10-03 words and L66 stand; no line.
2. Flow's memory stays Flow's, and Mind uses the flow data, machine
   reading of the two records together:

File: `psyche-context/skills/vision-flow.md` (after L16, under
choice 2)

```text
+ Flow's memory is Flow's own; the flow data Flow records is what Mind uses for its memory, the biggest database of the system, whose size is kept, distributed or archived.
```

3. Flow's memory lives in Mind, his 2026-09-17 words; L66 changed:

File: `psyche-context/skills/vision-nexus.md` (L66, under choice 3)

```text
- The running Nexus holds its whole domain as typed values, a specific type for every kind; no text arrives on its wire and none leaves it. Its Memory is its own typed store, reached only through the memory engine; there is no central store; policy state and working state live in that one store, and policy changes only over the meta socket.
+ The running Nexus holds its whole domain as typed values, a specific type for every kind; no text arrives on its wire and none leaves it. Its Memory is its own typed store, reached only through the memory engine; there is no central store; policy state and working state live in that one store, and policy changes only over the meta socket. Flow's memory lives in Mind.
```

### Proposal 9: Nexus objects describe processes

2026-09-14, `flows/e1953c/vision/nexus.md`, STT: «In the Nexus objects,
you're going to describe all the processes. I don't think you need to
say "process" all the time, but it's kind of included or implied by
being a Nexus object, which means it can only be used with a Nexus
meta-actor, meta-process, or meta-flow, basically. It's like the same
concept as the flow is the actor inside the runtime.»; the same day,
later: «What I meant was that there's a meta actor also: the Nexus meta
actor, the Sema, and the Signal. We talked about this, but we never
actually reviewed it together: how the trait enforces that it can only
be used inside of a particular meta actor, like either the Signal actor,
the main Signal actor, or the Nexus actor. The Nexus actor, the Sema
actor, and the Signal actor have their sub-actors, or possibly their
implementations, that need to run inside these actors.»; «We separate
the logics in the code, and we enforce it on the compiler. Is that
possible?»; the same day, on effects (the record notes «Speech-to-text
corrected in the quote: "Logic shells out to Nex" for "Lojix shells out
to Nix"»): «Oh, I'm glad you asked that. What about effects? Lojix
shells out to Nix. That's Nexus. Nexus encapsulates processes, whether
they're internal algorithms running over data that got somehow by
reading some signal archive or Sema database, or whether it's using a
special command line like Nix. There could be many other things, and it
maintains a sort of API around the CLI that wraps this Nexus process,
like a Nix build, right?»; and last: «You have sub-processes, so you define those
as more objects, and you're going to have a certain kind of object, a
nexus object that is an actor, basically. Maybe we even have to find a
better term for that.»

Sources: `flows/e1953c/vision/nexus.md`, 2026-09-14 (the date is
`flows/e1953c/log.md`'s, lines 41–47; the record file is undated);
vision-nexus L124–127 («Actors»: landed) and L146–148 («Three parts and
one path»: landed; Proposal 13 builds on it).

File: `psyche-context/skills/vision-nexus.md` («Actors», after L127)

```text
  The engine inside a Nexus is driven by Kameo actors. The standards
  of their use are still to be designed. Arc-Mutex is permitted.
+
+ A Nexus's objects describe its processes; «process» is not said each time, it is implied by being a Nexus object, which runs only inside a Nexus meta-actor, as a flow is the actor inside the runtime. A sub-process is defined as more objects, among them a Nexus object that is an actor. An effect is a Nexus process: an internal algorithm over data, or a wrapped command line such as Nix.
```

Ruling, one number from each group:

The paragraph:
1. Land.
2. Land with changes the living names.
3. Drop.

The three meta-actors against the three parts. His 2026-09-14 words:
«the Nexus meta actor, the Sema, and the Signal»; his 2026-10-12 words,
`flows/d68c82/vision/design.md`, STT: «the three different parts: the
operation, the signal, and the memory»; the landed line, L148: «Signal
is what it says, Operation is what it does, Memory is what it
remembers». The compiler's enforcement ends in his question «Is that
possible?». The choices are the machine's:
4. The meta-actors are the three parts under their later names, Nexus
   read as Operation and Sema as Memory, machine reading of the later
   words; a sentence added:

File: `psyche-context/skills/vision-nexus.md` (after L148, under
choice 4)

```text
  A Nexus has three parts, each its own ethos specification: Signal is what it says, Operation is what it does, Memory is what it remembers. Nexus always names the whole; the part that does is Operation. Every effect has a matching operation type. A signal reaches memory only through operation; memory answers operation that the change succeeded or failed; the answer returns through operation and leaves as a signal. Reading a Nexus's ethos alone shows every object and process on that path.
+
+ Each part is a meta-actor: its sub-actors run only inside it, the logic of each part separated in the code, and the separation enforced by the compiler.
```

5. The 2026-09-14 meta-actors stay in the record; L148 stands alone.

The word «actor»; his words: «Maybe we even have to find a better
term for that.»:
6. «actor» stands, L126 unchanged.
7. Another term the living names, written in place of «actor» at L126
   and in the paragraph above.

### Proposal 10: configuration loaded from files, in succession, on the meta socket

2026-10-09, `flows/445410/vision/nexus.md`, STT («Transcription
corrected: "mine" → "Mind"» in the record): «We need to allow the Nexus
to have its configuration loaded atomically so that it can live in
separate files in different repositories. That way, we don't have to
solve the whole Datom path expansion for now, and we can just load all
the configuration, even at different layers, using config files
(basically Datom payloads for configuring that particular Nexus that the
CLI can use in succession to start up that Nexus with the right payload
on the meta socket). It's like a hack to get the Nexus started.»

2026-10-10, `flows/081064/vision/ethos.md`, STT, relayed: «now we need
to define the anatomy of that registry and use the same atomically
updatable approach. The registry can be populated from multiple sources
using the datom files that can be in the repositories that essentially
wrap all of the data in that particular repository and can be updated by
whoever updates that repo. It can then be loaded along with other
repositories to create a full registry.»

Landed: vision-nexus L87–94 («Configuration»: no arguments, no bootstrap
binary, defaults as a constant, the meta socket carries a Configure
interface); `flows/edf227/vision/flow.md`, 2026-10-03 (configuration in
Flow's own database and memory, Proposal 8).

Machine facts. flow origin/main d190e10 (2026-10-13):
`crates/flow-nexus/src/main.rs` opens a configuration-only listener
(`open_configuration_listener`, L604) that serves one rkyv
`MetaQuery::Configure(change)` (`serve_one_configuration`, L566, L583).
meta-signal-flow origin/main 88f3759 (2026-10-09), `ethos/signal.ethos`
L176–180, declares `ConfigurationFragment`, `ConfigurationFilePath`,
`ConfigurationFilePathVector`, `ConfigureFiles` and `ConfigurationFile`;
flow `docs/branch-consolidation-20261013.md` L67 records «Remove
obsolete ConfigureFiles frontend whose producer types no longer exist.»
knowledge-datom, a machine skill, says a datom «passes inline at a CLI
boundary, never as a datom file».

Sources: `flows/445410/vision/nexus.md`, 2026-10-09;
`flows/081064/vision/ethos.md`, 2026-10-10;
`flows/edf227/vision/flow.md`, 2026-10-03.

File: `psyche-context/skills/vision-nexus.md` («Configuration», after
L94; his «for now» and «a hack» are the mark; the figure under it)

```text
  A Nexus starts with no arguments and there is no bootstrap binary.
  Its executable holds a default configuration as a constant. On start
  it looks for its Sema database at the default location: a database
  that exists holds the configuration; a database created new is
  seeded with the defaults. The meta socket carries a Configure
  interface, and changed values are accepted through it.
+
+ For now, a hack to get a Nexus started: its configuration is loaded atomically from files, datom payloads for configuring that Nexus, kept in separate files in different repositories and at different layers; the CLI uses them in succession on the meta socket to start the Nexus with the right payload, so that datom path expansion need not be solved yet. A registry is populated the same way, from datom files in the repositories, each updated by whoever updates its repository, loaded together into one registry.
+
+ +----------------------+
+ | datom files, in their|
+ | repositories, layers |
+ +----------------------+
+    | read, one after another
+    v
+ +----------------------+
+ | the meta CLI         |
+ +----------------------+
+    | Configure, one payload at a time
+    v
+ +----------------------+
+ | the meta socket      |
+ +----------------------+
+    | accepts, atomically
+    v
+ +----------------------+
+ | Memory: the Nexus    |
+ | configured           |
+ +----------------------+
```

Ruling, one number from each group:

The paragraph and the figure:
1. Land.
2. Land with changes the living names.
3. Drop.

The file against L56 «A CLI turns text into Signal and nothing more: it
takes one inline datom, no flags, no subcommands;» (landed); his
2026-10-09 words: «config files (basically Datom payloads … that the CLI
can use in succession». The choices are the machine's:
4. A shell step passes each file's content inline, one call per file;
   the CLI unchanged, L56 stands.
5. The meta CLI takes a file path; L56 changed:

File: `psyche-context/skills/vision-nexus.md` (L56, under choice 5)

```text
- A CLI turns text into Signal and nothing more: it takes one inline datom, no flags, no subcommands; it identifies the process that called it and carries that identity in the message, so a Nexus knows its caller by the process, never by a claim. A CLI speaks to one Nexus, opens no store, stays thin; datom and all text handling are compiled out of the Nexus, which decodes only known types in their rkyv form and so stays small, since it keeps running and there may be many.
+ A CLI turns text into Signal and nothing more: it takes one inline datom, or for now the path of a file holding one, no flags, no subcommands; it identifies the process that called it and carries that identity in the message, so a Nexus knows its caller by the process, never by a claim. A CLI speaks to one Nexus, opens no store, stays thin; datom and all text handling are compiled out of the Nexus, which decodes only known types in their rkyv form and so stays small, since it keeps running and there may be many.
```

### Proposal 11: one shared library identifies the calling process

2026-10-12 16:21, `flows/875960/vision/flow.md`, STT, relayed: «I see
that you have the process object defined in the library for Flow but we
should have a shared library that many components, that many nexuses,
are going to use. This is because identifying the calling process of a
CLI is something I would like to minimize the amount of code that needs
to be rewritten for every CLI and increase the ease of cognition when
reading the code as to what this is doing. Obviously this is done in the
background whenever the CLI is used so none of it is actually
user-facing in a sense or configurable. It's just something that happens
and it may be on all CLIs.»; and, the same comment: «Flow isn't even on
in production so I'm not even worried about merging more into main.»

Landed: vision-flow L20 «No flow declares its id: every call to Flow is
identified by the calling process.»; vision-nexus L56 «it identifies the
process that called it and carries that identity in the message, so a
Nexus knows its caller by the process, never by a claim».

Machine facts. flow origin/main d190e10 (2026-10-13): the Nexus reads
its peer through the kernel, `crates/flow-nexus/src/caller.rs` L44
`rustix::net::sockopt::socket_peercred(self)`; the CLI crates
`crates/flow` and `crates/flow-meta` carry no process identity in the
message; `crates/flow-ethos/ethos/library.ethos` L37 declares `Process.{
Pid.Integer Started.Integer }` in Flow's own Library. The shared library
exists only untracked: nexus at ec097e3 (2026-10-04), `ethos/`
untracked, 30 lines. The caller's witness,
`flows/875960/books/8-caller-witnessed.md` Proposals 1 and 2, is
unruled. In production, the user unit `flow-nexus.service` is inactive
(dead) since 2026-10-13 12:34:25 CST, after 5 days 1 hour running.

Sources: `flows/875960/vision/flow.md`, 2026-10-12;
`flows/875960/vision/flow.md`, 2026-10-11 («no claimed [ID]», landed
L20).

File: `psyche-context/skills/vision-nexus.md` («Default clients», after
L56; the figure under it)

```text
  A CLI turns text into Signal and nothing more: it takes one inline datom, no flags, no subcommands; it identifies the process that called it and carries that identity in the message, so a Nexus knows its caller by the process, never by a claim. A CLI speaks to one Nexus, opens no store, stays thin; datom and all text handling are compiled out of the Nexus, which decodes only known types in their rkyv form and so stays small, since it keeps running and there may be many.
+
+ One shared library, used by many nexuses, identifies the calling process of a CLI, so that the code is not rewritten for every CLI and reads at a glance; it runs in the background whenever a CLI is used, neither user-facing nor configurable, and may be on all CLIs.
+
+ +----------------------+
+ | a CLI                |
+ +----------------------+
+    | calls, in the background
+    v
+ +----------------------+
+ | the shared library   |
+ +----------------------+
+    | reads the ancestry; puts it in
+    v
+ +----------------------+
+ | the message          |
+ +----------------------+
+    | reaches
+    v
+ +----------------------+
+ | the Nexus            |
+ +----------------------+
+    | anchors to the socket's peer; re-reads
+    v
+ +----------------------+
+ | the caller, witnessed|
+ | or Unidentified      |
+ +----------------------+
```

File: `nexus/ethos/library.ethos` (uncommitted; the whole is
`flows/875960/books/8-caller-witnessed.md` Proposal 1, unruled; its
lines that stand within the column shown as context, its long
comments wrapped to the column)
Ethos, the Ethos metaflow's. Apart.

```ethos
- Library ; Shared process data, observation capability and its bearer.
+ Library                   ; shared process data,
+                           ; observation and bearer
- [] ; Imports: the contract uses intrinsic types only.
+ []              ; imports: intrinsic only
- [ ; Types: a process identity, its ordered ancestry and observation refusals.
+ [                         ; types
     Pid.Integer
     Started.Integer
-    Process.{ Pid Started } ; A process identifier and its kernel start ticks.
+    Process.{ Pid Started } ; pid, start ticks
-    Ancestry.Vector<Process> ; Sending CLI first, its parents next, namespace init last.
+    Ancestry.Vector<Process> ; CLI first, init last
-    Unidentified.[ ; Why a claimed process chain cannot be trusted.
+    Unidentified.[   ; why a chain is refused
        PeerMismatch
        Vanished
        Reused
        Malformed ] ]
- [ ; Traits: observation of an existing process identity.
+ [                         ; traits
-    Identifiable.[ ; Re-observe this process and its complete parent chain.
+    Identifiable.[   ; re-observe the chain
-       identify.[ Result<Ancestry Unidentified> ] ] ] ; Yield the witnessed chain or a refusal.
+       identify.[
+          Result<Ancestry Unidentified> ] ] ]
- [ ; Associations: Process bears the observation capability.
+ [                         ; associations
-    Process.[ Identifiable ] ] ; The implementation belongs to Process.
+    Process.[ Identifiable ] ]
```

File: `flow/crates/flow-ethos/ethos/library.ethos` (origin/main
d190e10, L37; Flow's own declaration, which the shared library
replaces under «book 8» Proposal 1 choice (a); shown as context)
Ethos, the Ethos metaflow's. Apart.

```ethos
    Lock.{ Sender Address Until.Integer }
    Process.{ Pid.Integer Started.Integer }
    Sender.Address
```

Ruling, one number from each group:

The paragraph and the figure:
1. Land.
2. Land with changes the living names.
3. Drop.

The ethos file's comments; no word of his on this fork:
4. Wrapped to the column, as shown, machine choice: the file is read
   on a phone as every book is.
5. As the file stands, machine choice: the comment runs to the end of
   its line, and the column is a book's rule, not an ethos file's.

«it may be on all CLIs»; his words: «I'm not sure now»:
6. «may be on all CLIs», as shown, his words.
7. «is on every CLI», machine reading of L56's «it identifies the
   process that called it».

### Proposal 12: the identifier made of words

2026-10-12 16:12, `flows/875960/vision/flow.md`, STT, relayed (the
bracket [protos] is the relay's;
`flows/9519a1/reports/flow-book-3-comments.md` line 33 gives the comment
as «maybe the proto library», a report's claim): «Well if we create a
special thing and we call it a name or we call it a word, you're never
going to know when I'm talking about it. Those are silly suggestions.»
«This is going to be used a lot here so whenever it's like an
identifier, a word identifier, or an expression, it will be more than
one word. Wherever we have something like a topic, a particular object
that needs to be identified by agents or humans, which is anything
that's user-facing that needs to be named through judgment and has to be
given a name. Obviously variants are great but we have to recompile
everything to add one. It's essentially a variant that is created on
demand and is a bit more descriptive. The fact that it doesn't start
with a capital is how we differentiate it from variants.» «It would go
in some kind of shared library, maybe the [protos] library, because I
think it could be used in more than one place, in more than one dialect.
It would also do a check, which is interesting.» «Oh my God this is a
perfect spot for a system1 AI call to use a cheap judgment on: Is this
composed mostly? Is this made up of words? Is this a camel-case string
made up of words, whether they're proper nouns or not? It's not a
problem and then we would have, I guess, a certainty threshold.
Brilliant.» «But then again maybe there's a cheap library that can do a
quick check with a fallback on AI. That's also an interesting
possibility: if there's something that's cheap, lightweight (in terms of
runtime cost) and can, in many cases, give us an answer on whether or
not these components are actual words programmatically, and then fall
back to the AI in case of a negative.»

Earlier on the same subject. 2026-10-08, `flows/d4ae97/vision/flow.md`,
STT: «It's basically PascalCase of a certain number of words and we can
have some kind of checker on that probably.»; 2026-10-09,
`flows/445410/vision/flow.md`, STT: «but technically it should be
uncapitalized core and ethos since theyre the core:Name type which is
"camelCaseExpression" type with runtime checks when creating a new one»
(landed, vision-flow L32); 2026-10-10, `flows/081064/vision/ethos.md`,
STT, relayed: «This is the Prototypic name or whatever, the prototype
name, which is an uncapitalized identifier. It's going to have to be
composed of words so we need to put together some kind of fancy check.
Well not that fancy, I guess.»; 2026-10-11,
`flows/875960/vision/flow.md`, STT, relayed: «the topic should always
start with a small letter. It's uncapitalized. In other words we need a
name for that. It's like a datomic name or something: a camelCase
identifier.» (landed, vision-flow L20). The 2026-10-08 words say
PascalCase; every later record says uncapitalized.

Sources: `flows/875960/vision/flow.md`, 2026-10-11 and 2026-10-12;
`flows/d4ae97/vision/flow.md`, 2026-10-08;
`flows/445410/vision/flow.md`, 2026-10-09;
`flows/081064/vision/ethos.md`, 2026-10-10. The name of the type is
`flows/875960/books/7-flow-whole-ethos-4.md` Ruling 3 (Coinage, Moniker,
Epithet, Cognomen, or his), unruled; `<identifier>` below stands for
whichever he names. Machine fact: no camelCase-of-words check exists in
the protos repository; flow `crates/flow-ethos/ethos/library.ethos` L8–9
reads «; ethos-zero 16 cannot express Topic:Name yet; check camelCase at
input.» over `Topic.String`.

File: `psyche-context/skills/vision-protos.md` (another topic's skill:
vision-protos; a new section after «Canonical print», L153)

```text
  the delimiters and the inner content.
+
+ ## The identifier made of words
+
+ An identifier names what agents or humans must identify, anything user-facing that is named through judgment, a topic among them. It is more than one word, camelCase and uncapitalized, which tells it apart from a variant; it is a variant created on demand, more descriptive, with nothing recompiled to add one. It lives in a shared library, used in more than one dialect, and is checked when created.
```

File: `psyche-context/skills/vision-flow.md` (L32; his 2026-10-12
words refuse «a name or … a word» as the type's name)

```text
- Every flow has a topic; a flow with no special topic has the topic core, the heart of its aspect. A topic is a core:Name, a camelCaseExpression checked when created. A flow's title names its aspect, topic, layer and flow id: { Psyche core Secondary <id> }.
+ Every flow has a topic; a flow with no special topic has the topic core, the heart of its aspect. A topic is a core:<identifier>: an identifier made of words, checked when created. A flow's title names its aspect, topic, layer and flow id: { Psyche core Secondary <id> }.
```

Ruling, one number from each group:

The section and the line:
1. Land.
2. Land with changes the living names.
3. Drop.

The shared library; his words: «maybe the [protos] library»:
4. The protos library: «It lives in the protos library, used in more
   than one dialect.»
5. «a shared library», as shown, unnamed until the library stands.

The check; his words frame the method as exploration («Maybe this
deserves its own full research»; «That's also an interesting
possibility»): a notion, not ruled; the choices are the machine's:
6. «checked when created», as shown; the method waits for the
   research.
7. A cheap word library first, a System 1 call on what it cannot pass,
   with a certainty threshold, his last sentence; added to the
   section: «The check is a cheap, lightweight library of words first,
   and a System 1 call with a certainty threshold where it says no.»
8. A System 1 call alone, with a certainty threshold.

### Proposal 13: the three parts are the machine's anatomy; one good Nexus first

2026-10-12, `flows/d68c82/vision/design.md`, STT: «I think that what I'm
making with the Nexus system (the three different parts: the operation,
the signal, and the memory, and then how each of these is divided) is
essentially the bulk of the machine anatomy: what are the pieces that we
need to define in the system? It was something that was instinctively
going towards already. As such we could sort of flesh that out more.» «I
think what we really need to do is create one good nexus that has all of
its types and all of its traits well defined and then the flow nexus is
the most needed essentially.» Landed in part, vision-nexus L148 (the
three parts and the one path); the anatomy and the one good Nexus not
landed.

The same day, the same record, on the golden system: «When you design a
system you need to have, I guess, a role model or a golden system that
you can compare against to see if you're currently in possession of
enough data to put together all of the anatomy of the system and
design.»

2026-10-11, `flows/875960/vision/flow.md`, STT, relayed: «we need to
define all of the traits and all of the types in Ethos.» (landed,
`psyche-context/vision/ethos.md` L43–45).

Sources: `flows/d68c82/vision/design.md`, 2026-10-12 (the raw record;
`flows/875960/vision/nexus.md`, 2026-10-12, relays it);
`flows/875960/vision/flow.md`, 2026-10-11; vision-design L6–8 (landed).

File: `psyche-context/skills/vision-nexus.md` («Three parts and one
path», after L148)

```text
  A Nexus has three parts, each its own ethos specification: Signal is what it says, Operation is what it does, Memory is what it remembers. Nexus always names the whole; the part that does is Operation. Every effect has a matching operation type. A signal reaches memory only through operation; memory answers operation that the change succeeded or failed; the answer returns through operation and leaves as a signal. Reading a Nexus's ethos alone shows every object and process on that path.
+
+ The three parts, and how each is divided, are the bulk of the machine's anatomy: the pieces to define in the system. One good Nexus comes first, with all its types and all its traits well defined; Flow is the most needed.
```

Ruling, one number from each group:

The paragraph:
1. Land.
2. Land with changes the living names.
3. Drop.

Where it lands; no word of his on this fork:
4. vision-nexus, as shown, machine choice: the words describe the
   Nexus.
5. vision-design, machine choice: the words answer what the golden
   system is, and the record's home is `design.md`:

File: `psyche-context/skills/vision-design.md` (after L8, under
choice 5, in place of the paragraph above)

```text
  No one can know ahead of time that the pieces are enough to yield the best version that could be come up with at the moment. Everybody contributes to the judgment, without limit. Judging that an idea is complete is the hardest part of a thinking machine to get.
+
+ ## The golden system
+
+ A system is designed against a golden system, a role model compared against to see whether enough is in hand to put together all of the anatomy. The Nexus's three parts, and how each is divided, are the bulk of the machine's anatomy: the pieces to define in the system. One good Nexus comes first, with all its types and all its traits well defined; Flow is the most needed.
```

### Proposal 14: books show code

2026-10-06 14:58, `flows/8475a9/vision/flow.md`, typed, book comment,
relayed: «that would be cool if we could have syntax highlighting. Also
I feel like it's not enough. I don't see what `self` is although I can
imagine. I guess seeing code is making me curious about the code. We
could have code presentation blocks and try to present more code. I like
that.»; 2026-10-05, the same record, typed: «I want to see code. I want
to see visuals and not too much text.»

2026-10-06, `flows/8475a9/vision/livingMessenger.md`, STT, relayed: «if
there was something universal (other than Claude artifacts) that would
let me comment and that I could use with any models, not just Claude.
That would also have syntax highlighting and things like that and we
could style it differently.»

Machine fact: `primary/tools/book-code.html` (committed 21b5410a6,
2026-10-11) highlights ethos and datom through a hand tokenizer and
rust, clojure and bash through highlight.js 11.9.0. vision-book L6–14
carries no line on code.

Sources: `flows/8475a9/vision/flow.md`, 2026-10-05 and 2026-10-06;
`flows/8475a9/vision/livingMessenger.md`, 2026-10-06.

File: `psyche-context/skills/vision-book.md` (another topic's skill:
vision-book; after L14)

```text
+ A book shows code, in code presentation blocks with syntax highlighting, and enough of it that what a line names, `self` among them, is seen; code and visuals, not too much text.
```

Ruling, one number from each group:

The line:
1. Land.
2. Land with changes the living names.
3. Drop.

The commenting surface; his 2026-10-06 words: «something universal
(other than Claude artifacts) … with any models … style it
differently»:
4. Not in the line, as shown: the surface is the living messenger's
   subject, machine reading.
5. A sentence added: «The surface the living comments on is universal,
   usable with any model, styled our own.»

### Proposal 15: implemented before the comment

2026-10-09, `flows/445410/vision/flow.md`, STT: «the psyches are getting
me, so the books are getting pretty good. Let's start just implementing
them even before I comment, or modifying when I comment, etc.»

Machine lines on the same subject. intent-psyche L12 «The long-term
vision is the goalpost, never a blocker; the short-term vision is what
the system is to be for now. Either may be implemented or not.»
(landed). mind-context `knowledge-psyche` L53: a vision skill holds
«statements, each reviewed by the living before it stands»;
field-context `compensation-psyche-interraction`: «A statement enters a
vision- skill only as a crystallization the living has explicitly
approved.» Both are the machines' own modules, changed by their owners.

Sources: `flows/445410/vision/flow.md`, 2026-10-09.

File: `psyche-context/skills/vision-book.md` (another topic's skill:
vision-book; after L14, after Proposal 14's line)

```text
+ A book's proposals are implemented before the living comments, and modified when the comment comes.
```

Ruling, one number from each group:

The line:
1. Land.
2. Land with changes the living names.
3. Drop.

What goes ahead before the comment; no later word of his draws the
line, and the choices are the machine's:
4. The code: a proposal's code lands before the comment, and the
   psyche-module lines wait for it; the two machine lines stand, and
   the line reads:

File: `psyche-context/skills/vision-book.md` (under choice 4, in place
of the line above)

```text
+ A book's code is implemented before the living comments, and modified when the comment comes; its psyche-module lines land on the comment.
```

5. Both: the psyche-module lines land before the comment and are
   modified on it, as shown; the two machine lines are changed by
   their owners.
6. No line.
<!-- to-the-living:end -->
