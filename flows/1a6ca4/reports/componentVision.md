# Component vision: Nexus, mind, psyche, Flow, persona meta-harness, thinking-machine procedures

Report for flow 1a6ca4, written 2026-09-05 by a read-only subflow. Carried account: every claim names its origin; the living's words are verbatim; the subflow's own reading is marked "my inference". Nothing here was verified by running code.

Structure: 1 summary of claims; 2 psyche records verbatim per topic (2a Nexus/harness/subagents/system prompt/flow daemon; 2b mind/psyche/flow; 2c persona meta-harness; 2d thinking machines and the "legal system"; 2e Yegge/Wheelhouse); 3 existing code and design; 4 attention in transcript history; 5 how the components relate, in the living's words; 6 unknowns; Sources.

## 1. Summary of claims

Each claim: origin in parentheses. "Psyche record" = a file under Vision/, Intent/, vision-raw/, flows/*/vision or notion. "Transcript" = a harness JSONL the living typed or dictated into, not yet in any psyche record.

**Nexus**

- A Nexus is the universal shape of every long-running component: process, at least two sockets (ordinary and meta), one datom-converting CLI per socket, pure-signal wire, compiled contracts; the engine inside is Nexus Core; everything built is a Nexus, and whatever was built otherwise is rewritten (Vision/nexus.md, distilled; raw from flows/e06e4c07/vision/nexus.md 2026-08-19 onward). "nexus is not a thing, its a kind of thing" (flows/01a05487/vision/nexus.md).
- The Flow Nexus "sets up and starts a model flow: its working directory, system prompt, training files and instruction prompt. It takes the place of the abandoned training daemon" (Vision/flowNexus.md, distilled). Its repository holds only machinery; every skill lives outside it (same).
- e06e4c07's open Question 1 (launch an existing harness, or run its own model loop) was answered 2026-08-21: "yes for now. we will create our own custom harness in the future, which will be 100% typed datom messages going in and being expected out." (flows/15b67974/vision/flowDaemon.md, typed).
- 2026-09-05: "we're going to start flows using a Nexus component, which will decide what the system prompt is and everything. We're going to replace the harness's concept of subagents with this component, which will have specialized harnesses launched with specialized system prompts" (flows/1a6ca4/vision/nexus.md, STT). My inference: this is the same thing as the Flow Nexus of Vision/flowNexus.md, now named from the Nexus side; the living did not say whether "the Nexus component" and "the Flow component" are one component or two.
- The built-in sub-agent tool is to be disabled; a tool asks the meta harness for another session instead; hierarchy optional, siblings possible (vision-raw/gradientsOfAuthority.md 2026-08-10, dictated). Transcripts "obviously" belong to "another nexus" (flows/e06e4c07/vision/flowKnowledge.md 2026-08-19).
- There is no nexus repository. Every current component (orchestrate, lojix, mind, persona, harness, listener, spirit) is a daemon-plus-CLIs shape; only orchestrate (0.29.2, HEAD 2026-09-04) is on datomic + ethos-zero + protos (section 3). One raw record says "Nexus should be the universal Nexus library, for all nexuses, and ethos-zero is where the daemon should be" (flows/db97561c/vision/nexus.md, typed, undated) — my inference: this concerns the ethos-zero repo layout, not a flow-starting Nexus.

**Mind**

- Only one psyche record exists on mind, from this flow: mind "is essentially going to replace a lot of the files and the readmes, not the psyche log", "keeping track of which repositories are involved, what kind of knowledge and witnesses", "summaries of transcripts, and essentially the memory of the system is going to go in mind" (flows/1a6ca4/vision/mind.md, 2026-09-05, STT).
- Earlier, in transcripts only (not in any psyche file): 2026-07-28 "I need Mind, I need Orchestrate, I need Logics to work properly, and they're always broken"; "I understand that Mind is not deployed, but I don't think I was finished even designing Mind"; 2026-08-06 "this psyche component is different than the mind, which is more like the agent's mind, or a store of memories, which mind I see mind as replacing beads and reports and a lot of things like design documents" with "agent judge calls" that scan for content made obsolete and "the concept of escalation" up to the living psyche (section 2d, with transcript paths and lines).
- Code: /git/github.com/LiGoldragon/mind 0.8.0, last substantive commit 2026-07-09 (Kameo actor daemon, mind-judge LLM admission edge, old schema/DOTOS stack, 21 dirty files that are a NOTA-to-DOTOS rename); reports/mind-design-status-2026-07-28.md finds "Mind is **not design-complete**" (section 3).

**Psyche component**

- 2026-08-11: "a new component which will include spirit, named psyche, which will hold spirit, intent and vision, and be used to feed the hijacked llm calls" with "a top-level enum; Spirit, Intent, Vision" (flows/012fbf07/vision/threeStacks.md, typed). 2026-08-21: "spirit is to be abandonned for psyche" (vision-raw/spiritComponentAndFile.md). 2026-09-05: "the psyche log is obviously going in Psyche, which is why Psyche is so important: it gets its own sort of mind-like component" (flows/1a6ca4/vision/psyche.md, STT).
- Precedent machinery named by the living: "the spirit component, which has been shelved for now and has to be ported over to this newly called psyche component. The nexus is where we were doing an LLM call to check if the proposal already existed and if it was contradicting something already in the database" (flows/78c93c/vision/witness-reuse.md, STT). Spirit's judge: "The judge being down should just bar mutation, obviously" (Codex transcript 2026-08-03, section 2d).
- The psyche log's structure (topics, four levels Spirit/Intent/Vision/Notion, distillation, rolling distillation, archive-) has abundant records 2026-08-09 to 2026-09-04 (section 2b) — these define what the Psyche component must hold.
- Code: /git/github.com/LiGoldragon/psyche 0.1.0 is an intentionally empty scaffold (HEAD 2026-08-14); spirit 0.27.0 (HEAD 2026-08-13) is the donor (section 3).

**Flow component / flows protocol**

- The living is unsure: "Maybe the Flow component. I'm not sure, though, about the architecture, if that's been laid out to my liking." (flows/1a6ca4/vision/flow.md, 2026-09-05).
- What is ruled about the protocol: a flow is one linear LLM chat, not an agent (flows/e06e4c07/vision/flowsNotAgents.md 2026-08-19; flows/4ddc321d/vision/flow.md 2026-08-26); flow identity is six literal characters of the random part of the harness ID, no conversion, one small tool per harness (flows/01a05826/vision/flowIdentity.md 2026-08-31); "I don't want subflows to start creating their own lanes. They just use their parents." (flows/01a05826/vision/subflowIdentity.md); the parent supplies the flow ID and decides what is logged (flows/01a05e95/vision/flowSkills.md); logging should be rare and high-level (flows/01a05e95/vision/logging.md); flow artifacts live in flows/<short-id>/ with witnesses/, reports/, log.md (flows/5c8be3ca/vision/flowArtifacts.md). Realized as the main-flow/subflow/flow-evidence skills and the harness repo's `flow-id` helper (HEAD 2026-09-02).
- e06e4c07 (2026-08-19/20) designed "flow, the Nexus that sets up and starts a model flow" and settled Nexus vocabulary; its flow-side anatomy stayed at Question 1, answered "yes for now" on 2026-08-21 (above). No record lays out the Flow Nexus's internal anatomy beyond Vision/flowNexus.md's two paragraphs. My inference: this matches the living's "not sure ... if that's been laid out to my liking".

**Persona meta-harness**

- Persona is "slated to orchestrate the entire meta harness (called persona)" though "That repo hasent been touched in a long time" (flows/15b67974/vision/persona.md 2026-08-21). The meta-harness is named "context-stratification-seizure", replaces beads, "but datom and ethos first, so we can actually write all this logic" (flows/012fbf07/vision/gradientsOfAuthority.md 2026-08-11). Motivation: "if I overwhelm all the agents with all of my ideas at once, it's just going to be a mess ... which is why I want to do this meta-harness" (vision-raw/trainingRepo.md 2026-08-13). "the meta harness is required for shards to become more specialized" (vision-raw/attunement.md 2026-08-13). 2026-09-05: "the persona meta-harness is going to bring in the dawn of the more complete thinking machine systems, which will be a complex infrastructure of a kind of thinking machine legal system interworking apparatus" (flows/1a6ca4/vision/personaMetaHarness.md).
- Code: /git/github.com/LiGoldragon/persona 0.2.0, last substantive commit 2026-07-07, old schema stack, ARCHITECTURE.md 1814 lines describing a supervising persona-daemon with spawn order supervisor -> sema-upgrade -> mind -> orchestrate -> router -> harness -> terminal -> message -> introspect -> spirit; persona-spirit "is an abandonned repo" (section 3).

**Thinking-machine procedures ("a kind of legal system")**

- Only one psyche record, from this flow: "All of these components are going to use thinking machine calls in their machinery to go through acceptance processes and review processes ... procedures for things to be accepted, things to move up in importance, things to be taken down, or things to be replaced. It's a lot more complex system than just letting any agent just write files and push commits." (flows/1a6ca4/vision/thinkingMachineProcedures.md, 2026-09-05, STT).
- Precedents: the 2026-08-06 transcript statement on judge calls, obsolescence review and escalation (section 2d); the spirit judge (admission-only LLM edge, Luna XHigh wanted, 2026-08-03/04 transcripts); the existing judge repos: judge 0.2.0, spirit-judge 0.3.0, mind-judge 0.1.0, orchestrator-judge 0.1.0, all last touched 2026-08-13, all old stack (section 3). Vocabulary: "agent" becomes "machine", short for "thinking machine" (flows/38dec9/vision/agentToMachine.md; flows/01a052b6/vision/vocabulary.md).
- Yegge: no psyche record before 2026-09-05. The living asked for his two-part essay on 2026-08-05 (for part two, treating agents better); reports/YeggeOnAgents-2026-08-05.md is an agent-authored digest naming Wheelhouse (section 2e).

**Attention (section 4)**

- The living's typed/dictated messages in the last 90 days (3,267 messages, 308 sessions; nothing earlier than 2026-07-24 exists on disk): psyche 596 msgs / 248 sessions; ethos 179 / 59; protos 138 / 48; orchestrate 128 / 86; datom 115 / 47; nexus 76 / 37; lojix 57 / 34; mind 49 / 38 (but only ~8 are about the Mind component; the rest are idioms); wispr 37 / 16; listener 27 / 14; persona 7 / 6; meta-harness 7 / 7; Yegge/Wheelhouse 4 / 4.
- Last typed mention before this flow: persona 2026-08-21, meta-harness 2026-08-22, mind-as-component 2026-08-06 (idiomatic uses later), nexus 2026-09-03, psyche/orchestrate/datom/ethos/lojix/wispr 2026-09-04.
- Repository HEADs: orchestrate, lojix, datomic, ethos-zero, wispr-flow-linux 2026-09-04; harness 2026-09-02 (flow-id helper); protos, listener 2026-08-29; psyche 2026-08-14 (scaffold); mind, persona, spirit, judge repos 2026-08-13 (docs-only commit; last substantive: mind 2026-07-09, persona 2026-07-07).
- My inference: by every measure the psyche (log and component), orchestrate, and the datom/ethos/protos substrate are where attention went; mind and persona have had almost none since July and the living said why ("I was just rethinking everything, and I still am"); the flows protocol had a burst 2026-08-19 to 2026-09-04 (e06e4c07, 5c8be3ca, 01a05826, 01a05e95, 444e5e) but the Flow Nexus itself has no anatomy record.


## 2. Psyche records, verbatim

Each entry: `path — entry date — standing|archived`, then the record as it stands in the file. "standing (legacy)" = vision-raw/, the undistilled corpus being drained into Vision/. Ordering is oldest first within each topic. The gatherings are by three read-critical subagents plus this subflow; they overlap where a record speaks to several topics, and such records are pointed to rather than repeated.

### 2a. Nexus, harness and meta-harness, subagents, system prompt, flow daemon, datomNexus, nexusTraits

(Gathered by subagent; its inference is marked as such.)

Gathered by a research subagent for flow 1a6ca4, 2026-09-05.
Entries are ordered OLDEST FIRST within each topic section.

---

### Topic 1: Nexus

#### vision-raw/nexus.md — undated — standing

(Title-only record; drained into Vision/nexus.md.)

> # Nexus — the name for what we called a Rust component (daemon + CLIs + signal)

---

#### flows/019feb93/vision/threeStacks.md — 2026-08-10 — standing

> just generate the rust code for types and generics/traits to define
> the wire types (signal), major internal engine operation types
> (nexus), and database types (sema). log this

— psyche, 2026-08-10T18:03+02:00 (Realizer session 019feb93), answering
what exact end-to-end result the incorrect new stack must produce before
the old Schema + NOTA stack can be retired.

---

#### flows/55d18f4f/vision/everythingIsInTheDaemon.md — 2026-08-08 — standing

(This is the vision from which "Nexus" descends: the living's vision that everything is in the daemon, the architecture of Ethos/Nomos/Logos as daemons communicating via signal.)

> the parser is in the daemon right?
>
> Everything is in the daemon.
>
> So this is my vision from the very beginning. Well, I mean, this is the
> vision. This is the vision for a long time. You have the Ethos daemon,
> the Nomos daemon. I mean, they're just called Ethos, Nomos, and Logos.
> Those are the name of the repositories. They're all daemons. The same
> architecture as all my other components, right? There's the daemon,
> there's a CLI, there's a CLI for the metasocket. Everything is signal
> messages, meaning RKYV binary messages. That's what signal means. All of
> this you should be able to find out very, very easily. This should be
> absolutely standard. If any of this was lost and somebody has screwed up
> major, big time. So the whole engine working is the Ethos daemon loads
> the Ethos and then holds the whole thing. It has every object in its own
> specifically typed object, right? A specific type for every kind in
> Ethos, including the Nomos object. So those Nomos types are shared
> between the Nomos daemon. I mean, they're a bit different, arguably,
> because of how Nomos thinks about its own types. Well, they're not
> different, actually. It's just that Nomos uses it as an input for its
> transformer. But I guess, yes, they're the same thing as far as the
> input part. So Ethos doesn't need to think about the transformer. It
> just needs the input part that goes into the transformer. So it loads
> those into, like every transformer has its own particularly specified
> input type. So Ethos has those in the daemon. Everything is in the
> daemon. And then when Ethos wants to convert into logos or rest, which
> has to go through logos, then it sends a message. It communicates to the
> Nomos daemon and tells it, I need this converted into logos and then
> into rest or something. Or maybe it just says, I need this converted
> into logos. And then once that's done, then it gets a message back,
> possibly from the logos daemon directly, that says, oh, here I have your
> request. So the request should have a certain ID for a conversion and
> it's done. And then the Ethos, or not necessarily the Ethos daemon, but
> possibly the Ethos daemon or maybe there's another, maybe the agent
> drives this. So the agent gets the response that says, okay, the logos
> transformation has been done through, I don't know what, we haven't
> fleshed any of this out, so there's a problem. And then, so all three of
> those are daemons. And so it's all message-based. And then all of the
> daemons hold that language in memory, in their database. Not in memory,
> in their database. So they can fetch it back. It's there. They can edit
> it. We're going to do operational editing, right? So we can't do
> operational editing if there isn't a daemon with the database, with the
> entire, whatever we call it, the capsule or whatever of that program or
> that universe, if you will, that world that has been loaded through
> Ethos and through Nomos, because Nomos then also loads the transformers
> from the Nomos, like to bootstrap from the Nomos textual form. We have
> to write the transformers in textual form. So Nomos, when it starts,
> loads its transformer into its transformer, the transformer index of its
> database. And then when it gets a request from Ethos, you know, it does
> the transformation and communicates with Logos to tell it, okay, here's
> a new object. So Nomos is going to use Logos strictly through
> operational editing because it's literally giving it stuff, right?
> Here's a new object, here's a new object, here's a new object, here's a
> new object. It's transforming everything in, you know, in a world, in a
> capsule. So it's going to say, okay, I'm going to create a capsule or
> you need to create a capsule or you need to find a capsule that
> eventually later, I guess, we're going to be able to do incremental
> changes. But yeah, Nomos would communicate with Logos and say, okay,
> well, we need a new capsule. I'm going to start a new, sending you a
> bunch of stuff. And then it transforms everything, including the regular
> Ethos, which also has, basically everything gets transformed. Like even
> the standard Ethos syntax essentially corresponds with like a standard
> transformer. So a standard enum declaration, right, is just like in
> Nomos is called an enum transformer. An Ethos enum transformer. But I
> mean, everything is Ethos transformers. It doesn't have to specify that
> every time, but it's a transformer for an Ethos enum. And then it gets
> the enum and then it tells Logos, okay, here's a new object, an enum.
> And then it's fully like fleshed out because Logos is explicit over
> everything because it mirrors the rest, right? Like there's nothing
> omitted. All the information to create the rest object is in the Logos
> object. It's just more, it's more beautiful. It's more data based.
> Anyway, there's probably a lot more we have to talk about. I feel like
> agents have missed out on all that part of my vision. Or unless like I'm
> misunderstood. I don't know what, why is there is core Ethos. So core
> Ethos is a dependency of the Ethos repo, right? Which is running a
> daemon. So core Ethos is a dependency of the Ethos daemon. And that's
> the only way this has been done right. And so on, like with Nomos and
> Logos. And if none of this was understood, and if you don't understand
> what happens, I just want to explain. Because to me, all of this was so
> obvious, and I thought we had discussed this to death before, like I
> guess a month ago or something. I've been working on this for so long
> now, it feels like years, that I never assumed that I needed to explain
> this again. Like I thought it was so obvious to everybody that we weren't
> even talking about it anymore.

— psyche, 2026-08-08T11:12:45.472Z (Designer session 55d18f4f; full
session UUID 55d18f4f-ea0b-43d8-88ae-f8f4bd3027d2)

---

#### flows/e06e4c07/vision/nexus.md — 2026-08-19 — standing

#### 2026-08-19 — a Nexus is the whole component; the Nexus part is its execution engine; two sockets, two CLIs, pure signal, compiled contracts; everything built is a Nexus

Design session `e06e4c07`, dictated (captured 2026-08-19T13:49+02:00).
One continuous excerpt from a longer message; the remainder is logged
under flowDaemon, flowsNotAgents, rustComponentArchitecture. "rest
components" reads Rust components; "texturalizing" reads
textualizing; "ESOS" reads Ethos (transcription readings, agent's).

> There's something else I want to talk about before we get deeper
> into creating this component, which is vocabulary related. So in
> what we call the rest components, and this is ambiguous, which is
> why I want to talk about this. There is a concept called Nexus,
> N-E-X-U-S. And because this concept hasn't really been used much, it
> seems to be sort of hanging in the air. And because we need, and
> because of what it is, essentially, the way I work is a lot of
> intuition. And the fact that I created this Nexus thing shows that I
> was onto the intuition that there is a core there, the Nexus, to
> this architecture of how I'm designing each component, which
> deserved a name. So instead of calling them the rest components or
> the daemon CLI signal components and all of that stuff, we're just
> going to say another Nexus. Or if we say a Nexus, like when we
> aren't being specific. So there's the Nexus part, which is the
> execution engine inside a Nexus. And the same way that we talk about
> a man when we're really talking deeply, we talk about his heart or
> his soul. It doesn't mean that we are saying that we should take the
> heart out and that everything else in the body should be excluded,
> because that would mean there's no more man left, that would destroy
> his totality. So we can still talk about the whole thing as a Nexus,
> and it's very appropriate actually, terminologically speaking,
> because the way I am creating this system, this metasystem that is
> emerging now, is that there are all these different Nexus, each of
> which can function on their own, but which really gain a lot of
> value by working with each other, by exchanging information and
> communicating with each other. And there's several reasons to design
> this way, one of which is simply practical, to approach problems one
> at a time and not try to solve everything in a giant monolithic
> program. And then there's all of the side effect consequences of
> that, which is that it allows us to keep parts of the system going
> while other parts are being changed. It allows us to recompile the
> system incrementally by recompiling one Nexus at a time, and then
> eventually with a full update mechanism in place to have a system
> that has zero downtime and that can incrementally recompile itself.
> And so this was necessary because of the way the Rust compiler
> works, and even generally the way compilers work nowadays, there
> isn't even a compiler out there that allows for selectively changing
> one part of an executable, it's always just completely recompiled.
> So we create this sort of grossly grained separation, which
> eventually will change completely and to be more efficient
> eventually will have a more unified execution model, which will just
> simply be sort of like a meta-kernel that can selectively be
> upgraded, but the technology just isn't even there yet. So that's
> why we're doing it this way. That's also why we're using policies
> such as all just the Nexus itself. So there's the clients, and each
> Nexus has for now a client that we write by default, or two clients,
> because each Nexus needs to have two sockets, right? Because one of
> these sockets, the meta-socket, is going to be privileged. And sort
> of like any system needs a root user, if only in order to configure
> it and to do privileged operations. So it's going to have two
> clients by default, which are CLIs. And the CLI, so all clients will
> have to talk to the Nexus, regardless of which socket, in pure
> signal, in signal, which is fully binary, because the Nexus
> component cannot be involved in texturalizing signal, because it
> would just destroy the beauty and the simplicity of the system. So
> all Nexus components speak only pure signal, the contracts which
> they are compiled with, and two of those contracts are its own, one
> for its regular socket, one for its meta-socket, but many of them
> will compile with the contracts of other Nexuses to allow them to
> communicate with each other. So I want to make that clear in the
> skills, and anything that I said architecturally that isn't clear in
> the skills already should be re-clarified or further clarified or
> rectified if it was not in agreement with what I just said. And
> yeah, it's a very correct system. It uses a software ontology using
> traits, which hasn't been done properly yet, and I'm in a discussion
> in another flow about this, about the fact that when we introduced
> the mandatory traits, that the first implementation just simply
> created placeholder traits for every function, and just sort of
> mindlessly created traits that don't create a sensible ontology. And
> there's going to have to be a lot to be done in terms of creating
> training for this to be understood better by agents, and also
> creating a workflow for this, for any ontology to be designed
> properly before it's implemented. And this relates to why I want
> ESOS, the language, to allow us to more coherently and clearly
> design the main traits and types of a system, of a nexus, of any
> system. But everything we're going to build is going to be a nexus
> now, and anything that has already been built that did not take the
> shape of The nexus is going to be rewritten.

Context (agent-authored, separate from the psyche's words): the
whole component — daemon, its two sockets, its two default CLI
clients, its contracts — is a Nexus; "the Nexus part" is the
execution engine inside it (heart of the man, named without
excluding the body). Every Nexus speaks only pure binary signal and
never textualizes it; it is compiled with contracts — its own two
(regular socket, meta-socket) and those of peer Nexuses it talks to.
The meta-socket is the privileged one (the root user of the Nexus).
The reason for the coarse-grained separation: problems one at a time,
parts keep running while others change, incremental recompilation,
eventually zero-downtime self-updating; a unified meta-kernel is the
later shape the technology does not yet allow. The skills are to be
clarified or rectified to agree with this. Mandatory traits' first
implementation produced placeholder traits without a sensible
ontology; training and an ontology-design-before-implementation
workflow are wanted, and Ethos is to let the main traits and types of
a Nexus be designed coherently. Everything built from now is a Nexus;
what was built otherwise is rewritten.

---

#### flows/e06e4c07/vision/archive-nexus.md — 2026-08-19 — archived

#### 2026-08-19 — edge, not vertex, was meant; not every two vertices have a meta edge; edge could replace contract

Design session `e06e4c07`, typed (captured 2026-08-19T14:56+02:00),
after the Designer read "some vertices will not have the meta access"
as a property of the edge:

> re vertices: then I was trying to say edge. not all edges will have
> meta access (if we think of both socket as a single edge. said
> otherwise, not every two vertices will have a meta edge). We could
> use the word edge instead of contract.

#### 2026-08-19 — edge and contract both kept; the edge line approved

Design session `e06e4c07`, typed (captured 2026-08-19T16:47+02:00),
on the proposed line "A Nexus is a vertex in the graph of nexuses. An
edge joins two vertices and carries one contract: every connected
pair has an ordinary edge; only some pairs have a meta edge. A Nexus
is compiled with the contracts of its own sockets and of every edge
it has." — contract kept for the compiled vocabulary, edge for the
link between two vertices:

> the nexus line is good.

#### 2026-08-19 — the Nexus part confirmed; the skill is renamed nexus; a nexus repo is wanted; the execution heart is Nexus Core; "signal contracts"; meta access is case by case; plural; the "why" goes to a parallel skill for psyche-facing flows

Design session `e06e4c07`, typed (captured 2026-08-19T14:33+02:00).
Excerpts from one message answering the Designer's questions and
skill-wording proposal; trims between.

On "the Nexus part is the execution engine inside the whole, with the
whole also called a Nexus":

> a. yes

On whether to rename the rust-component-architecture skill `nexus`,
told that the word is used by an arXiv multi-agent framework and two
orchestration repos:

> why is that relevant?

> Yes, I want the rename. I also want a nexus repo (if there is one,
> it probably doesnt fit the role I now have for it) which will
> explain the principle, and potentially even hold the nexus traits

> We could rename the current Nexus (the "actor/interface/abstraction"
> for execution) as NexusCore; the heart of this nexus; where all the
> decision-making happens.

> so "The execution engine inside it is also called the Nexus" would
> become "called Nexus Core". Feedback

On "A Nexus speaks only the contracts it is compiled with":

> how about "signal contracts"?

On "and those of every peer Nexus it talks to":

> some vertices will not have the meta access. its case by case. so
> that statement is incorrect

On the proposed section "Why many Nexus":

> isnt it nexuses? That we could have a parallel skill. What is the
> right word to speak of this kind of information? Its "raison
> d'etre"? That could become a parallel skill design skill. It would
> only be of use to psyche-facing flows, to allow them to think of the
> whole, with all the reasoning and concepts, when discussing ideas
> with the living psyche.

Context (agent-authored, separate from the psyche's words): no
directory named nexus exists under the LiGoldragon checkout root at
capture time (listing witnessed). "vertices" is the psyche's word for
the nexuses as peers; whether it is a term being introduced is asked
back. The plural and the word for reasoning-information are
questions put to the Designer, not rulings.

#### 2026-08-19 — core-<component> was already killed; vertices if the word fits; at least two sockets; a default CLI client per socket; the nexus repo is a possibility; first design universal nexus traits from first principles; traits lines deployed

Design session `e06e4c07`, typed (captured 2026-08-19T14:51+02:00).
Excerpts from one message; trims between.

On the skill's `core-<component>` optional library:

> I already ruled to kill that completly

(The prior ruling: threeStacks 2026-08-11, "no core-* split; three
repos per component".)

On whether "vertices" is a term for a nexus seen as a node in the
graph of nexuses:

> is it an appropriate use of the word? If so then yes.

On "A Nexus is a daemon with two sockets":

> we should say *at least* two sockets. some nexus might need more
> than 2 levels of access.

On "its two default CLI clients":

> then this would become a default cli client per socket. the cli is
> for bootstrap and later on can be used for debugging and testing
> even after it isnt used in production anymore

On the nexus repo holding the principle and the nexus traits:

> potentially. let's keep that as an possibility under discussion. We
> need to first design universal nexus traits, which would be the
> basic ontology of an actor/dataflow software system. lets look at
> signal and sema with that, without giving much credit to the
> existing code, approaching it as if we were designing it for the
> first time (the current code being compared to it, which will show
> the gaps as we design further)

On the proposed traits lines ("The traits and types of a Nexus are
designed as one ontology — the most unified map of traits and types —
before any body is written; a new need first finds its place in that
map. One type implementing many single-function traits is one trait
not yet seen."):

> this is good. deploy it

---

#### flows/01a03d6e/vision/archive-nexus.md — 2026-08-26 — archived

#### 2026-08-26T10:10:32.842Z — the daemons are called Nexus; Orchestrate Nexus; all Nexuses follow that naming invariant

> Also, we should make an invariant that the demons are not called demons but Nexus.
>
> So it should be Orchestrate Nexus, and all Nexuses should be like that.
>
> So we should make that clear in the Nexus skill.

Speech-to-text correction beside the quote: `demons` → `daemons` (both occurrences).

— psyche, source-event timestamp `2026-08-26T10:10:32.842Z`; root session UUID `01a03d6e-5cb8-7b60-b573-7f59413bc18e`.

#### 2026-08-26T11:38:49.521Z — there should be no bootstrap binary; default configuration is a constant in the executable

> only problem is the bootstrap binary. There should be no bootstrap binary.
>
> So, in terms of configuring the Nexus, obviously, well it's going to have default configuration.
>
> And we can make that more sophisticated later on but it can just have a constant in the executable with a default configuration.

— psyche, source-event timestamp `2026-08-26T11:38:49.521Z`; root session UUID `01a03d6e-5cb8-7b60-b573-7f59413bc18e`.

#### 2026-08-26T11:38:49.521Z — try the default Sema database location and initialize new databases with defaults

> And because it has a default, well first it should try to get its state from the default location for its Sema database.
>
> And then if that database doesn't exist or if, well, if the database exists then it should have the configuration in it.
>
> Because the default configuration when creating a new database should set the configuration as the defaults in the database.

Speech-to-text correction beside the quote: `SEMA` → `Sema`.

— psyche, source-event timestamp `2026-08-26T11:38:49.521Z`; root session UUID `01a03d6e-5cb8-7b60-b573-7f59413bc18e`.

#### 2026-08-26T11:38:49.521Z — create an interface on the meta socket to change configuration

> But yeah, so it has a default configuration by default and create an interface on the meta socket to allow for changing that configuration.

— psyche, source-event timestamp `2026-08-26T11:38:49.521Z`; root session UUID `01a03d6e-5cb8-7b60-b573-7f59413bc18e`.

#### 2026-08-26T11:51:46.649Z — new values must be accepted

> this is a problem; new values must be accepted otherwise it's not doing what we want.

> there is a valid idea behind this however; on a never configured nexus, the ordinary socket could get a configure interface which works but rejects if already configured.

— psyche, source-event timestamp `2026-08-26T11:51:46.649Z`; root session UUID `01a03d6e-5cb8-7b60-b573-7f59413bc18e`.

---

#### flows/b675f3d9/vision/ethosMonolith.md — 2026-08-26 — standing

#### It becomes a nexus; everything will be a nexus

2026-08-26, the psyche, typed (answering the surfaced tension "monolith pragmatism vs go-straight-for-a-nexus"):

> 5. Then we'll make it a nexus. Everything will be a nexus; the consistency will create reliability and increase the quality and clarity

---

#### flows/acbb6006/vision/nexus.md — 2026-08-27 — standing

#### Everything up to that point not commented on is approved

2026-08-27T14:40:26Z, the psyche, typed:

> everything up to the last point I commented on which  I didnt comment on is approved. represent it with my modifications, and reconsider the rest and represent it as well

#### The listed impurities are destroyed

2026-08-27T15:20:37Z, the psyche, typed, on the impurity list of reports/distillProposalNexus.md, distillProposalProtosDatomAddendum.md, distillProposalPsycheProcess.md and Vision/ethosMonolith.md "First fixture":

> 5. yes, impurity

> re impurities: yes, destroy them all

---

#### flows/acbb6006/vision/archive-nexus.md — 2026-08-27 — archived

#### Clients are packaged with the nexus, as separate crates: a datom-converting CLI per socket

2026-08-27T14:40:26Z, the psyche, typed, on the proposed Vision/nexus.md statement "A Nexus is the whole" (reports/distillProposalNexus.md), quoting "the default CLI clients that speak to them,":

> no, the clients are not the nexus. for now, default clients are packaged with the nexus, so they should be separate crates (multi crate repo), in the form of a datom-converting cli for each socket (however many sockets that nexus has; minimum 2)

On the statement "Default CLI clients", quoting "CLI client, written with the Nexus.":

> see above

#### In everyday speech orchestrate-nexus is called orchestrate

2026-08-27T14:40:26Z, the psyche, typed, quoting "Nexus is the word for it in every name — Orchestrate Nexus, Ethos Nexus":

> in everyday speech, orchestrate-nexus will be called orchestrate, etc

#### The heart sentence is quackery

2026-08-27T14:40:26Z, the psyche, typed, quoting "speaking of the core never excludes the rest.":

> this is quackery

#### The "first Nexus" statement is discarded

2026-08-27T14:40:26Z, the psyche, typed, quoting the proposed Vision/orchestrate.md statement "Orchestrate is the first Nexus:":

> not necessary; discard

#### Skills live outside the runtime repository

2026-08-27T14:40:26Z, the psyche, typed, quoting the proposed Vision/flowNexus.md statement "The flow repository holds the machinery of the Flow Nexus and a few basic skills:":

> no, the skills will be outside the runtime repo, otherwise modifying a skill will result in a nix rebuild.

#### The engine inside a Nexus is Nexus Core

2026-08-27T15:20:37Z, the psyche, typed, on tension 1 (Nexus Core, the psyche's 2026-08-19 words, against "Nexus kernel" in Vision/ethosMonolith.md and "Nexus Kernel" in the nexus skill):

> 1. core

#### Polling is forbidden; a correct system goes quiet when nothing changes

2026-08-27T15:38:13Z, the psyche, typed, on claim 4 ("Polling is forbidden; a correct system goes quiet when nothing changes."):

> 4. this is true and approved as vision

#### First configuration: a standard nexus metadata tree records whether meta Configure was ever done

2026-08-27T15:20:37Z, the psyche, typed, on tension 2 (Configure on the ordinary socket of a never-configured Nexus):

> 2. its a valid concept. standard nexus meta-data tree which has a type to know if the meta configure was ever done, which can only be reversed on the meta socket. if unset, the ordinary socket configure is accessible. this is independant of the builtin default configuration, which are needed since otherwise we wouldnt have a socket path to even fall back on to even allow the configure signal to come in.

#### The standard metadata tree holds socket paths and all standard nexus configuration data

2026-08-27T15:38:13Z, the psyche, typed, on the proposed Vision/nexus.md statement "First configuration" ("A Nexus keeps a standard metadata tree"):

> and lets add to that metadata anything standard: socket paths (its own and the paths of all its other edge-sockets), and anything else that comes up as standard nexus configuration data.

#### A nexus deals with a domain; when its features grow too many, splitting nexuses out of it is considered

2026-08-27T15:38:13Z, the psyche, typed, on nexus-skill claim 1 ("One capability, one Nexus. A Nexus is sized to be held whole in one mind — human or model; when it outgrows that, it splits.") and the flow's explanation "agents would refuse to add a second capability to an existing Nexus":

> 1. too strongly worded

> that isnt my vision. especially since capability is now a specific term in ethos. a nexus deals with a domain, and if its features grow too many, then spliting out one or more nexuses out of it should be considered. we dont want to scare the flows here, just offer a broad vision on how we design new nexuses when one becomes too complex

#### Observation by subscription: make the core idea dead simple

2026-08-27T15:38:13Z, the psyche, typed, on claim 2 ("Observation flows up, authority flows down: state is observed through push subscriptions — a typed snapshot on open, typed deltas after"):

> 2. I dont like the wording here, even if some of it is true. See if you can make the core idea dead simple, and strip out the complexity and details which we can add back later. so the line is either removed or replaced with a better one

#### The multi-nexus commit line is quackery; deleted from the skill

2026-08-27T15:38:13Z, the psyche, typed, on claim 3 ("When one intent spans several nexuses, the issuer commits on the first success and records divergence on failure — no distributed rollback, no all-or-nothing stall."):

> 3. this is pure quackery. I cant even understand it. delete it from the skill

---

#### flows/01a02fd5/vision/archive-nexuses.md — 2026-08-23 — archived

#### 2026-08-23T20:28:43+02:00 — all nexuses have a meta socket

> all nexuses have a meta socket

— psyche, 2026-08-23T20:28:43+02:00, typed; Codex realization flow `01a02fd5`.

---

#### flows/01a05487/vision/nexus.md — undated — standing

#### nexus is not a thing, its a kind of thing

> "nexus is not a thing, its a kind of thing"

-- psyche, typed.

---

#### flows/db97561c/vision/nexus.md — undated — standing

#### Nexus is the universal library; ethos-zero is the daemon; Rust is generated through the daemon

Context: the flow had described ethos-zero's producer library as what consumers use (dev-dependency regeneration tests) and the `nexus/` subcrate inside ethos-zero as the daemon nobody calls.

> Nexus should be the universal Nexus library, for all nexuses, and ethos-zero is where the daemon should be. the rust code should be generated by using the daemon Generate.{ Path ...} or similar request.
>
> you have this all wrong

-- psyche, typed.

---

#### flows/98fbfa47/vision/archive-metaSignalNotOptional.md — 2026-08-09 — archived

#### "the metasignal is not optional"

> I'm looking at your draft and I would like to say that the
> metasignal is not optional because otherwise there's no way to
> configure the daemon.

— psyche, 2026-08-09T12:30Z (Designer session 98fbfa47, reviewing the
component architecture standard draft)

Context, kept apart from the quote: supersedes the pre-reset doctrine
(component-triad.md, record 2605) that `meta-signal-<component>` is
optional where no owner relationship exists. Every daemon is
configured over the meta surface, so every component carries a
meta-signal repo.

---

#### flows/1a6ca4/vision/nexus.md — 2026-09-05 — standing

#### 2026-09-05 — flows start through a Nexus component that decides the system prompt; it replaces the harness's subagents with specialized harnesses

Said while naming the components to bring onto the new stack after orchestrate; the living was unsure whether the Flow component's architecture had been laid out to their liking:

> It's just the concept that we're going to start flows using a Nexus component, which will decide what the system prompt is and everything. We're going to replace the harness's concept of subagents with this component, which will have specialized harnesses launched with specialized system prompts that will make them much more efficient at what they're supposed to be doing.

-- psyche, STT.

---

#### Vision/nexus.md — distilled (reviewed by the living) — standing

(Quoted in full.)

> # Nexus
>
> ## A Nexus is the whole
>
> A Nexus is the whole long-running component: the process, its
> sockets, and the signal contracts it is compiled with. Daemon is
> retired as the name of the thing. Every Nexus is named
> component-nexus — orchestrate-nexus, ethos-nexus — and in everyday
> speech orchestrate-nexus is called orchestrate. The decision-making
> engine inside a Nexus is Nexus Core.
>
> ## Sockets
>
> A Nexus opens at least two sockets. The ordinary socket serves
> ordinary peers. The meta socket is privileged — the root user of the
> Nexus — and configuration and privileged operations pass through it;
> every Nexus has one, since without it nothing could configure the
> Nexus. A Nexus that needs more levels of access opens more sockets.
>
> ## Default clients
>
> A client is a separate program from the Nexus. For now the default
> clients are packaged with the Nexus as separate crates of its
> repository, which is a multi-crate repository: one datom-converting
> CLI per socket, however many sockets the Nexus has, at least two. A
> default client serves bootstrap first, then debugging and testing,
> long after production has stopped using it. The meta CLI is named
> component-meta.
>
> ## Signal only
>
> Every client speaks to a Nexus in pure signal, fully binary. A Nexus
> speaks only the signal contracts it is compiled with; two of these
> are its own, one per socket. A Nexus thinks in typed values — enums,
> structs, scalars — and the string fields it still carries are
> records on the way to a fully typed form.
>
> ## The graph
>
> A Nexus is a vertex in the graph of nexuses. An edge joins two
> vertices and carries one contract. Every connected pair has an
> ordinary edge; only some pairs have a meta edge. A Nexus is compiled
> with the contracts of its own sockets and of every edge it has.
>
> ## Routing
>
> Signals cross the network through a router. The router tells signal
> types apart by an enum, held in a universal signal repository every
> component depends on, which wraps the objects. That repository also
> holds what every signal needs in common — the handshake payload
> among it.
>
> ## Configuration
>
> A Nexus starts with no arguments and there is no bootstrap binary.
> Its executable holds a default configuration as a constant. On start
> it looks for its Sema database at the default location: a database
> that exists holds the configuration; a database created new is
> seeded with the defaults. The meta socket carries a Configure
> interface, and changed values are accepted through it.
>
> ## First configuration
>
> A Nexus keeps a standard metadata tree. In it a type records whether
> the meta Configure was ever done; that record is reversed only on the
> meta socket, and while it is unset Configure is accessible on the
> ordinary socket. The tree holds everything standard about the Nexus:
> its socket paths — its own and those of every edge-socket it connects
> to — and whatever else comes up as standard nexus configuration data.
> The built-in default configuration is independent of this and is
> what gives the socket path on which the Configure signal arrives.
>
> ## Repositories
>
> A component has three repositories: its main repository, holding all
> its code, and two signal repositories — one for the ordinary
> socket's contract, one for the meta socket's. Shared kinds go into
> reusable libraries, which are encouraged.
>
> ## Everything is a Nexus
>
> Everything built from now on is a Nexus, and what was built in
> another shape is rewritten as one. The consistency creates
> reliability and raises quality and clarity.
>
> ## Actors
>
> The engine inside a Nexus is driven by Kameo actors. The standards
> of their use are still to be designed. Arc-Mutex is permitted.
>
> ## Splitting a Nexus
>
> A Nexus deals with a domain. When its features grow too many,
> splitting one or more nexuses out of it is considered.
>
> ## Observation by subscription
>
> State is observed by subscription: the subscriber receives the state
> on open, then each change as it happens.
>
> ## Polling is forbidden
>
> Polling is forbidden; a correct system goes quiet when nothing
> changes.

---

#### Vision/sources/nexus.md — source listing — standing

> e06e4c07 nexus
> 01a03d6e nexus
> acbb6006 nexus
> 98fbfa47 metaCliIsComponentDashMeta
> 012fbf07 threeStacks
> 15b67974 actorLibrary

---

### Topic 2: Flow Nexus / Flow Daemon

#### flows/358f143a/vision/archive-flowDaemon.md — 2026-08-18 — archived

#### 2026-08-18 — the daemon is not training (abandoned); it is flow

Design session `358f143a`, typed (captured 2026-08-18T15:23+02:00).
Supersedes the successor-repo naming in trainingRepo /
skillsRepository (2026-08-17: "a new repo called training"):

> On another note: the new daemon I want to make isnt training
> anymore (abandonned). Its flow, which will setup and start a model
> flow, with its own working directory, system prompt and training
> files, and its instruction prompt.

Context (agent-authored, separate from the psyche's words): the
component is named flow. What it does, in the psyche's words: set up
and start a model flow, with its own working directory, system
prompt, training files, and instruction prompt. Whether the
repository is also named flow, and what becomes of Curriculum's
generator role, is not yet said.

---

#### flows/e06e4c07/vision/archive-flowDaemon.md — 2026-08-19 — archived

#### 2026-08-19 — Curriculum is rewritten as a Nexus; the flow repo is the machinery; skills live in another repo; a few basic skills in flow replace the built-in harness prompt; the name stays flow; research requested

Design session `e06e4c07`, dictated (captured 2026-08-19T13:49+02:00).
Excerpts from one message; the Nexus vocabulary part is logged under
nexus. Trims between excerpts.

> So for example, the curriculum repository. Now essentially, not all
> of its content will go into the flow nexus, but because the skill
> contents themselves will have to live somewhere else because the
> flow nexus, the repository will be about the machinery of the flow
> nexus. And the actual skills that people want to use with their
> system will have to live in a different repository. Of course, there
> will probably be a few basic skills. No, there will be a few basic
> skills that are actually included in the flow repo, which are
> essentially the analogs of what the basic harness training prompt is
> currently that is built into the harnesses, which we will completely
> replace, is going to be about. Just basic stuff on how agents should
> behave in a harness, but with our own take on it. So do some
> research and anything that's vaguely or closely resembles or touches
> the topics that I've covered, whether it's in programming theory,
> software architecture, software ontology. Let's make you smart. I
> need a smart flow. I mean, this brings me to the fact that the word
> flow is kind of getting overloaded if we have a flow nexus. So we
> can also discuss maybe thinking of a different name for that
> repository, for that nexus. Maybe something that has to do like a
> tap or a source of the flow or something like that. Maybe flow.
> Yeah, flow is good. I like the idea that it's a flow.

Context (agent-authored, separate from the psyche's words): the flow
repo holds the machinery of the flow Nexus plus a few basic skills —
our own replacement for the harness's built-in training prompt (how
agents behave in a harness); the skills people use with their system
live in a different repository, not yet named. The name flow is kept
after a tap/source alternative was considered. Research into
programming theory, software architecture, and software ontology
touching these topics is requested before going deeper.

---

#### flows/15b67974/vision/flowDaemon.md — 2026-08-21 — standing

#### 2026-08-21 — flow launches an existing harness for now; our own custom harness later, 100% typed datom messages

Design session `15b67974`, typed (captured 2026-08-21T17:21+02:00),
answering e06e4c07's Question 1 — does flow launch an existing
harness (Claude Code / Codex) with a composed system prompt, or run
its own model loop:

> yes for now. we will create our own custom harness in the future,
> which will be 100% typed datom messages going in and being
> expected out.

---

#### flows/e06e4c07/vision/flowKnowledge.md — 2026-08-19 — standing

#### 2026-08-19 — transcripts belong to another nexus; for now a small clever search tool: typed prompts first, the few preceding model responses, line numbers

Design session `e06e4c07`, typed (captured 2026-08-19T17:00+02:00),
answering whether the harness transcripts belong to the flow Nexus:

> obviously another nexus. But we might want a small clever tool to
> help search those files more efficiently for now.

> finding the user typed prompts is an obvious first step. then we
> would need the few preceding model responses, to give those prompts
> context. and the result would have to contain line numbers, to allow
> a more fine-grained search to proceed after the bulk of the gold has
> been found.

---

#### Vision/flowNexus.md — distilled (reviewed by the living) — standing

(Quoted in full.)

> # Flow Nexus
>
> ## What it does
>
> The Flow Nexus sets up and starts a model flow: its working
> directory, system prompt, training files and instruction prompt. It
> takes the place of the abandoned training daemon.
>
> ## Repository and skills
>
> The flow repository holds the machinery of the Flow Nexus and is a
> runtime repository. Every skill lives outside it, the basic skills
> included, so that a change to a skill causes no Nix rebuild. The
> basic skills give our own take on how an agent behaves in a harness,
> replacing the prompt the harnesses build in.

---

#### Vision/sources/flowNexus.md — source listing — standing

> 358f143a flowDaemon
> e06e4c07 flowDaemon
> acbb6006 nexus

---

#### vision-raw/flowDaemon.md — undated — standing

(Title-only record; drained into Vision/flowNexus.md.)

> # flow — the daemon that sets up and starts a model flow

---

### Topic 3: Harness / Meta-harness / Specialized harness

#### vision-raw/trainingRepo.md — 2026-08-11 and 2026-08-13 — standing

#### 2026-08-11 — training material injected in the harness system prompt, which has higher authority

> "yes, thats the concept. soon the training will be injected in the
> harness system prompt, which has higher authority in the LLM context"

— psyche, 2026-08-11, steward session

#### 2026-08-13 — overwhelm problem is the stated motivation for the meta-harness

> And I'd also like to better train the agents on being able to
> discern intent from vision. And there's so many things I'm going
> to do all at once, and I'm trying to be reasonable here, because
> if I overwhelm all the agents with all of my ideas at once, it's
> just going to be a mess, and that's been kind of my main problem,
> which is why I want to do this meta-harness.

— psyche, 2026-08-13, Designer session 6863ef19, dictated

---

#### vision-raw/gradientsOfAuthority.md — 2026-08-10 — standing

#### 2026-08-10 — the hijack: top layer per session, skills primary; built-in sub-agent tool disabled; communicate with the meta harness instead

> So what I see is every session is unique and has the top layer, I
> guess we're going to call it, fed its own set of skills and style
> guidelines, like everything we put in skills, our standards,
> whatever that agent is going to need to do its job is going to be in
> the top layer. So that way, the way we code, for example, like our
> rest [Rust] guidelines and things like that, it's going to have much
> more power to guide the agent to code better. And the skills are
> going to be primary. And even its main goal, like the first prompt
> basically, which we're going to think of as differently than
> anything afterwards, every other subsequent prompt, like the middle
> layer, which is what I'm going to call everything we type in. And
> the tool cause [calls], we're not going to do anything there in
> terms of putting important information in there. So if anything
> needs to come in, it's not going to be from a tool call. So we're
> going to completely hijack the harness, which was my original idea,
> but now I want it even more because I realize how powerful this is
> going to become. Of course, there's going to be a lot more sessions
> and the built in sub-agent tool is going to be disabled because then
> I'm sure the sub-agent kind of inherits the top layer of its parent,
> whatever harness. So we're going to have to have this tool that
> allows an agent to create sub-agents, quote unquote, which is not so
> much create sub-agent, then communicate with the meta harness that
> something needs to be done. I guess there won't be such or yeah,
> there could still be a hierarchy of agent, but it's not necessarily
> going to be every call cause an agent below that agent. It might
> just it might be an agent that has a similar sort of spot in the
> hierarchy of agents.

— psyche, 2026-08-10T18:49Z (Designer session c6b71b4c), dictated

#### 2026-08-11 — no more beads for handover; the meta-harness replaces beads: context-stratification-seizure

> No more beads. Beads are tools which means lowest authority; using
> them for handover is stupid. In fact, we need to replace beads with
> our meta-harness (context-stratification-seizure) approach to get
> much better results. but datom and ethos first, so we can actually
> write all this logic

— psyche, 2026-08-11T17:53+02:00 (Designer session 012fbf07), typed.

#### 2026-08-11 — until we design the meta-harness (persona) properly

> yes, until we design the meta-harness (persona) properly and all the
> data is passed along the right agent call, like magic (you are logging
> psyche right?)

— psyche, 2026-08-11T20:18:14.611+02:00 (Realizer session 019ff178)

---

#### flows/358f143a/vision/workspace20.md — 2026-08-17 — standing

#### 2026-08-17 — role skills hold the awareness seat for now; the persona meta-harness will move this fast

> skills for now. It might evolve differently later. This will move
> quite fast as we build the persona meta-harness

---

#### flows/358f143a/vision/gradientsOfAuthority.md — 2026-08-18 — standing

#### 2026-08-18 — subflows do have harness training in the top stratum; the doc claim is false

> This is 100% false. theres no way the subagents have zero harness
> training. a flow already checked. why is this lie coming back? We
> have exposed flaw in our training/protocol that allows lies to
> linger. Expose the mechanism that allowed this to happen, and well
> design a fix. It may be that those prompts *do* reach the top
> strata, but they are not the entire top strata, else the model
> couldnt use the harness tools.

> strata is better than rung.

#### 2026-08-18 — how things work is not ruled; only the code can answer

> I dont rule how things work. things work the way they work.

> is that how it works? Whenver this is ascertained, we need to make
> it clear somewhere that we verified this in code, so we stop
> dancing the guesswork and bluffing tune

> docs are not for people who want to hijack a system to use it in a
> completly novel, undocumented way. Maybe we should have a hard rule
> against relying on docs for code; the code is what runs, not the
> docs.

---

#### flows/15b67974/vision/persona.md — 2026-08-21 — standing

#### 2026-08-21 — persona untouched for a long time, yet slated to orchestrate the entire meta harness

> That repo hasent been touched in a long time, even though it's
> slated to orchestrate the entire meta harness (called persona)

---

#### flows/38dec9/vision/perHarnessSkills.md — undated — standing

The psyche designing a per-harness skill architecture for documenting and controlling each thinking-machine harness.

> "Let's maybe create a Claude harness skill and a Codex harness skill, and move some of the harness-specific information that may already exist in some skills into those, and then start putting everything in there that we know: how to override the system prompt, which part of the system prompts cannot be overridden by that flag, how many strata each harness actually has (I believe Codex has 4 and Claude has 3), whether the system prompt is visible to the model or the machine, and not to me."
> -- psyche, STT.

> "I would probably just rename the executable of the wrapper something else so that we can still use the stock version, and call the wrapper something else, like Claude Light or Claude Unopinionated, or maybe Codec Unsafe if we take all the safety out and stuff, or Codec Bare where we have almost nothing. We could try them out and see how they turn out."
> -- psyche, STT.

> "There may be some things that I want to remove in all harnesses that we could do universally and just replace."
> -- psyche, STT.

> "Give me a draft on how we would do all of this per harness skill and what we could keep that's universal. Maybe the strata or the context strata skill can still remain, but have only the high-level concepts, like the explanation of what these strata are in the entire field of thinking machines and so on. We would have it per harness skill that gets more into the details of how that particular harness and those particular thinking machine models actually behave."
> -- psyche, STT.

---

#### flows/38dec9/vision/harnessVocabulary.md — undated — standing

> "We don't use the word 'agent,' so let's try and also see where we can edit that."
> -- psyche, STT.

> "I guess we can maybe reuse their own terminology here, so let's introduce that vocabulary as well, like system prompt. What is the name for the other ones? The user prompt, the developer prompt, and the tool prompt, or maybe different harnesses call it different things."
> -- psyche, STT.

---

#### flows/38dec9/vision/deepsekHarness.md — undated — standing

> "Why don't you look into the DeepSeek harness while you're out there? Apparently it's really good. Maybe we even want to package it in our environment and start testing out with ChatGPT because they do allow third-party harnesses, and we can start documenting that one as well."
> -- psyche, STT.

---

#### flows/38dec9/vision/piHarness.md — undated — standing

> "We should abandon the Pi harness also if we get into this, because I think it's falling out of favor now. It's pretty sloppy. I've had a really hard time with it when I was using it. It was just a catastrophe, actually."
> -- psyche, STT.

---

#### flows/38dec9/vision/invocationSystem.md — undated — standing

The psyche on how the harness invocation with the right system prompt gets composed.

> "I believe maybe the repository, and we're not going to go into this, but we can just talk about how we want to do this. One of the repositories, either harness or Flow, or maybe both of them are involved somehow, is going to actually create the system call with the right flag to invoke the harness with the right system prompt or the right top stratum."
> -- psyche, STT.

---

#### flows/aa4c7747/vision/basePrompt.md — 2026-08-24 — standing

#### 2026-08-24 — harnesses are told to copy the code they find; change that in the base prompt

> Since we don't want to actually, it seems that, and even the harnesses are kind of actually told to do that. They're told to like copy the code they already find. And actually, that's one of the things I want to change in the base prompt. I don't think that that's a good thing for like, because if there's bad things and bad things get copied.

---

#### flows/1a6ca4/vision/personaMetaHarness.md — 2026-09-05 — standing

#### 2026-09-05 — the wild west phase of thinking machines; the persona meta-harness brings the dawn of complete thinking machine systems

> That phase is like the wild west phase of thinking machines, and the persona meta-harness is going to bring in the dawn of the more complete thinking machine systems, which will be a complex infrastructure of a kind of thinking machine legal system interworking apparatus.

-- psyche, STT.

---

#### flows/b9f4f6/vision/topStratum.md — 2026-09-02 — standing

#### 2026-09-02 — Peirce's system in a specialized-harness system

> Let's see how pierce's system looks like in a specialized-harness
> system.

-- psyche, typed.

Flow reading, not the psyche's words: the instruction is in log.md;
what stands here is the name the psyche gives the system — a
specialized-harness system, one where each flow's top layer is built
for its job.

---

#### flows/38dec9/vision/systemPromptRepository.md — undated — standing

> "We should just create a separate repository that anyone could use to give modified versions with different names of Claude and Codex, with different takes on system prompts."
> -- psyche, STT.

---

### Topic 4: Subagents / Subflows

#### vision-raw/flowsNotAgents.md — 2026-08-10 — standing

#### 2026-08-10 — sessions are flows; aspects, not individuals

> And I even want to use a different term than agents because it's
> misleading, because what I'm making this meta agent, if you will, is
> made up of all these smaller sessions. So we were just going to call
> it, I guess, a session or even then it sort of implies that there's
> an individual there, but it's more like a flow or a sub flow. … the
> names of the awareness, the shards of awareness, I want to change
> them because if I say realizer, it sounds like there's an individual
> there, whereas in fact, it's the realizing aspect. And, you know,
> even that all of this machinery … it's going to stay, but eventually
> I don't want the user to be extremely aware … the average user
> eventually won't even know that there are different aspects. … But I
> think the terminology is really important, not just for me, but for
> the … sub flows. To instinctively understand the concepts because
> they're named properly. And this is actually really a big part of it
> would go in spirit. Right. Something like about how naming things
> properly creates the right understanding of instinctive
> understanding or the, you know, it's easy to grasp. And it also is
> about not misunderstanding.

— psyche, 2026-08-10T18:49Z (Designer session c6b71b4c), dictated

#### 2026-08-13T15:51:58.913Z — More Design flows, not more aspect names

> These are pretty good, but I want to run something by you because I think that what I'm doing here is basically just reaching out for more names because I want to actually run more agents, more agent windows, more flows, more sessions. None of these terms actually really... But I guess... What would you call it when there's a harness, a terminal, and there's a starting prompt, a starting skill, and then once the context is getting too big, some files are edited, and then these files are sort of reused to start a new one, a new context from scratch. What I wanted to run by you is that the problem isn't really that I need more terms so much that I need to maybe... Because to me, in my mind, I'm designing. I don't need to reach for all these terms. I feel like it's just going to make things complicated, so maybe we don't do all of this. Because it just feels like I'm trying to create... I don't have a meta harness, so really they're just names to differentiate my sessions for now. But I really just need more than one design window. So what if I run more than one session with the same awareness name? And if we train the agent... See, I don't like the agents. I don't like that term, agents. Actually, it's been abused. What is an agent? No one can even tell us. So an artificial being is a composite of many, many different LLM flows. Just like a human being is made up of thousands and thousands of thoughts, competing thoughts even. People argue in their head all the time. It's called internal dialogue. And so there's this internal dialogue that needs to happen between a bunch of different LLM flows to create the whole, which is the artificial being. And we basically need to keep the awareness files pure enough so that the agents don't start writing down, like taking notes on what they're working on specifically. Not that there's anything wrong with bringing understanding into the awareness. It's like broad understanding. But there's a few problems, one of which is that the awareness file is read as an ordinary file, which means that it has the lowest context priority. That's a problem. So the highest context priority, which we currently have access to before I start to actually launch custom harnesses with their own system prompts, is the middle layer. So I think that the awareness content should live, at least for now, in the skill. But it can't be an agent visible skill because then, you know, like all of this stuff is going to, well, geez, you can see it. I'm having a bunch of competing thoughts here because I understand what I want, but I can't just get there instantly. And that's why I kind of want to talk to a lot of designers right now. And this is my dilemma. And you can tell me what you think about all that. Don't implement any of these new roles yet. I'm still ambiguous on whether or not I want to approach it this way.

— psyche, session 019ffbd3-b870-7241-b5dc-cf355ae702c4

---

#### flows/e06e4c07/vision/flowsNotAgents.md — 2026-08-19 — standing

#### 2026-08-19 — an agent is a whole being; a flow is one linear LLM chat; artificial intelligence is a misnomer — synthetic intelligence

> It's not an agent because to me, an agent is more of a whole being,
> and a whole being is a lot more than a single LLM chat, which is
> linear and very limited. Whereas an entity, an artificial entity,
> which I think the word artificial intelligence is a misnomer. It's a
> synthetic intelligence. It's synthesized from human knowledge and
> mathematical probability. So a flow more accurately describes
> essentially an AI flow, right? Which is just one of the many flows
> that together, when properly structured and orchestrated, will
> resemble an artificial being or a synthetic intelligence.

---

#### flows/4ddc321d/vision/flow.md — 2026-08-26 — standing

#### 2026-08-26 — flow of thought; agent entails subjectivity

Ruling for the replacement base context, and the grounding of the
term itself:

> firstly: we will replace all occurence of sub/agent with sub/flow,
> with a line explaining what we mean by flow (perhaps by equating it
> with agent, since the model is probably trained to use this term,
> instructing him to use the flow terminology henceforth)
>
> the idea behind flow is simple; a flow of thought. An intelligence
> isnt a single flow of thought, it is a multitude of flows. so using
> the term "agent", which entails subjectivity, when speaking of a
> single flow does not correspond with reality. Hence the need to
> change the vocabulary, which will result in a more accurate model of
> reality.

---

#### flows/01a030df/vision/subagents.md — 2026-08-24 — standing

#### 2026-08-24T01:08:51+02:00 — must use subagents for all research, including openai

> remember that you must use subagents for all research, including openai.

---

#### flows/38dec9/vision/skillLandingBySubflow.md — undated — standing

> "If I approve them, you could set up some agent to just read your transcript and create/modify skill files from approved content, so the main flow doesn't waste context shuffling text. Whatever you print in your response can be used by a subagent to create or modify the actual skill files and deploy them."
> -- psyche, STT.

> "This, I believe, is something that I wanted to develop into standard practice."
> -- psyche, STT.

---

#### flows/e06e4c07/vision/flowKnowledge.md — 2026-08-19 — standing

#### 2026-08-19 — a skill, or a specialized subagent role that reads recent sessions for what impacts its parent flow

> Re flow info sharing: It should be a skill, or maybe even a
> specialized subagent role which looks at recent sessions for psyche
> rulings and insights/information which directly impact its parent
> flow. This brings me to the topic of session files, and how we can
> make them more accessible/easily-searchable for agents; are there
> tools for this? Iv discussed this in another flow already, but it
> fell out of the conversation and we didnt really address it.

---

### Topic 5: System prompt / Base prompt / Entry files

#### flows/2f6b1dc5/vision/systemPrompt.md — 2026-08-23 — standing

#### 2026-08-23 — replace the harness system/base prompts

> I want to replace claude and codex's system prompts with a version
> that doesnt incentivize the sort of behavior im constantly steering
> against. The system/base prompt (lets define the vocabulary here)
> has the highest context priority and is currently full (I suspect)
> of instructions that are completly or even partly against my
> philosophy and approach to LLM usage.

#### 2026-08-23 — base prompt vocabulary approved for deployment

> this is good. approved. deploy

(On the vocabulary entry "Base prompt: the harness-built portion of the top stratum — the instructions the harness itself composes ahead of everything authored here. Vendor parlance: system prompt.")

#### 2026-08-23 — method: most offensive blocks first, replacement per block

> Let's look at the most offensive base prompt blocks first, and
> design replacement for each, and work our way through the entire
> offensive corpus like this

---

#### vision-raw/entryFiles.md — 2026-08-17 — standing

#### 2026-08-17 — variables have names; they live in their own setup-specific file, documented in Curriculum's agents.md

The Designer had proposed a `## Skills` line listing reference skill
collection paths:

> theyre not variables if they dont have a name, but that is rougly
> the idea

On NON_MANAGEMENT_AGENTS.md holding only the hacks:

> right now its doing too much. variables should go in its own
> (AGENT_VARIABLES.md?) file, which is setup specific and therefore
> not in curriculum, but is documented in curriculum's agents.md file,
> so agents are made aware that those variables should be set and how.

---

#### flows/358f143a/vision/entryFiles.md — 2026-08-17/18 — standing

#### 2026-08-17 — one authored entry module in Curriculum generates CLAUDE.md and AGENTS.md

> yes, exactly what I was thinking

#### 2026-08-17 — the Sol subagent constraint stays in AGENTS.md

> too risky. I cant affort a bunch of sol subagents destroying my
> quotas again. With almost no upside.

#### 2026-08-17 — variables file approved; names are spaced prose; the psyche says "the system"

> Your variables file is good, but the variable names must be spaced;
> we are talking about prose training, not rust code training here.
> Unless you think models will have a hard time connecting those
> dots. But the psyche will usually say "the system", especially
> since typing is probably going away, and in any case, remembering
> OsSystemRepo is not high on my priorities. Once its settled, it
> will be linked to in the entry-files (entry-files =
> agents/claude.md)

#### 2026-08-18 — the variables file is linked directly from the entry file, so it enters the middle stratum; it is SKILL_VARIABLES.md

> the variables file should be directly linked in the entry file, so
> they enter middle statum

On whether AGENT_VARIABLES.md becomes SKILL_VARIABLES.md:

> yes.

---

#### flows/15b67974/vision/entryFiles.md — 2026-08-22 — standing

#### 2026-08-22 — entry files taken over completely; workspace specifics in @-prefixed secondary files, same stratum

> this would also entail taking over entry files completly, leaving
> workspace specifics into secondary files loaded with the @ prefix,
> which does apparently load them at the same stratum

---

#### flows/995a164e/vision/entryFiles.md — undated — standing

#### The always-commit-primary rule belongs in the entry files

> ok get it kind of fixed however you think. the always-commit primary should be in entry files

-- psyche, typed.

---

#### flows/01a035d3/vision/promptExplainsNothingTheHarnessDoesAutomatically.md — 2026-08-25 — standing

> when you have it working again, add this to the prompt-crafting skill:
>
> A prompt explains nothing the harness does automatically and nothing everybody knows; it carries only what the receiving flow would not otherwise have.

---

### Topic 6: Datom Nexus

#### flows/04db2fd2/vision/archive-datomNexus.md — undated — archived

Archived on landing: these words were distilled as they were spoken,
into Vision/datom.md (Repository and migration), flow e4a40e, 2026-09-03. Their
content is kept here.

#### Whether datom [STT: datum] should be a nexus for consistency; stays a library for now; eventually a nexus translating formats

> well, maybe we should make it a nexus now because consistency is very good for AI models. So if everything is a nexus, I mean, besides, you know, the trait libraries and things like that, we're going to get a lot more consistency out of everything. I just don't know how, you know, as datum [STT: Datom] is essentially a serialization and deserialization functionality, which is going to be included in other programs, other Rust binaries. I just don't know how it becomes a nexus right away. Like I can see eventually how it can be a nexus in the sense that it's going to, it's going to have more functionality, like where we're going to have a nexus to translate certain datum [STT: Datom] objects back and forth between different formats. But anyway, that's not a big issue right now. So this can just stay in a library for now.

-- psyche, STT.

---

### Topic 7: Nexus Traits

#### flows/fd301d9a/vision/nexusTraits.md — 2026-08-19 and 2026-08-22 — standing

#### 2026-08-22 — old code is at most inspiration for the map

Source: `psyche-raw/Vision/worldModelBeforeCode.md`, 2026-08-22, design session `15b67974`, typed and captured 2026-08-22T15:19+02:00.

> old code is at most inspiration for that map. (no "never ...")

#### 2026-08-19 — universal Nexus traits are the ontology of an actor/dataflow system

Source: `psyche-raw/Vision/nexus.md`, 2026-08-19, design session `e06e4c07`, typed and captured 2026-08-19T14:51+02:00.

> potentially. let's keep that as an possibility under discussion. We
> need to first design universal nexus traits, which would be the
> basic ontology of an actor/dataflow software system. lets look at
> signal and sema with that, without giving much credit to the
> existing code, approaching it as if we were designing it for the
> first time (the current code being compared to it, which will show
> the gaps as we design further)

#### 2026-08-13 — mandatory traits are the comprehension surface

Source: `psyche-raw/Intent/mandatoryTraits.md`, 2026-08-13, psyche-approved wording.

> Every method call in our Rust code lives under a trait, because
> traits are the comprehension surface — the layer where concepts
> become visible and implementations are constrained to think within
> them. Rust is the new assembly language: no serious engineer reads
> all the assembly, and the same is happening to Rust. Traits and
> main types are what the psyche reads; everything else is
> implementation detail that Ethos will eventually generate.

#### 2026-08-19 — ontology before implementation

Source: `psyche-raw/Vision/nexus.md`, 2026-08-19, design session `e06e4c07`, dictated and captured 2026-08-19T13:49+02:00.

> It uses a software ontology using traits, which hasn't been done properly yet [...] when we introduced the mandatory traits, that the first implementation just simply created placeholder traits for every function, and just sort of mindlessly created traits that don't create a sensible ontology. And there's going to have to be a lot to be done in terms of creating training for this to be understood better by agents, and also creating a workflow for this, for any ontology to be designed properly before it's implemented.

#### 2026-08-19 — the Nexus contains the execution engine

Source: `psyche-raw/Vision/nexus.md`, 2026-08-19, design session `e06e4c07`, dictated and captured 2026-08-19T13:49+02:00.

> There's something else I want to talk about before we get deeper
> into creating this component, which is vocabulary related. So, in
> what we call the rest components, and this is ambiguous, which is
> why I want to talk about this. There is a concept called Nexus,
> N-E-X-U-S. And because this concept hasn't really been used much,
> it seems to be sort of hanging in the air. And because we need, and
> because of what it is, essentially, the way I work is a lot of
> intuition. And the fact that I created this Nexus thing shows that
> I was onto the intuition that there is a core there, the Nexus, to
> this architecture of how I'm designing each component, which
> deserved a name.

---

#### flows/f426777b/vision/nexusTraits.md — 2026-08-26 — standing

#### 2026-08-26 — TryFrom may not be how to think about processing: the effect is the point, the response an effect of it; the returned object may be a generic, which in ethos is a trait

> I don't know if try from is the right way to think about something
> that we are processing. I know that, conceptually, it could work
> because we're we're getting a response out of it. But if only before
> cognition to better understand... because what we're doing when
> we're processing something or when we're... when an object is going
> into the nexus for an effect to take place, what... conceptually,
> we're not really trying to get the response. We will get a response
> as an effect of that, but it's kind of like you wouldn't punch
> somebody to try and break your own knuckles. The whole point is to
> hit him and damage him, not to hurt your fist. Although you might
> hurt your fist. So... and also, we would probably need the object
> returned to be... I don't know if we need the object returned to be
> a [generic], in which case? It's a trait because in ethos, generics
> and traits are essentially the same thing. If you understand what
> I'm saying or you're welcome to push back on that also.

#### 2026-08-26 — the carrying syntax is very unrefined: too many heads in a row; traits must not be defined implicitly

> And I don't like the syntax, by the way, that you've been developing
> for Nexus, which—okay, so let's look at, for example,
> "PathLockRegistered.try_from.registration".
>
> It's too difficult to make out what this is, and also it's too many
> heads in a row. It's very unrefined. This is a very unrefined
> syntax.

> I don't think we can just define traits implicitly, meaning if we
> only declare traits in our own version of implementations, of how we
> implement them, then it'll be difficult. It's going to be complex to
> try to extract what that trait actually is and how many interactions
> it has.

#### 2026-08-26 — Apply liked, not certain; the returned-generic trait prompts a need for new terminology

> I like apply but I'm not certain and the trait suggested for the
> returned generic made me think of something; we need a new
> terminology.

---

### Topic 8: Software anatomy and the Nexus

#### flows/04db2fd2/vision/softwareAnatomySkill.md — undated — standing

#### Two things come out of this work: the datom implementation aligned with vision, and a skill on how to design software anatomy

> two things will come out of the work we're doing here. One is the actual implementation of datum [STT: Datom], we'll get done more in line with the living psyche's vision, which is also, that's why vision is coming out of this. It's like, vision is being crystallized into computer data now ... we're going to work out how to essentially how to work out the anatomy of a program by breaking down its components, both in kinds and types and how these fit together in using capabilities. ... we're both defining, so we're going to be writing out of this, a skill on how to design software. I don't know if it's called software design or software anatomy or something, or maybe it's several skills.

-- psyche, STT.

#### Also: how to work out the anatomy of a nexus

> So we're also going to define how to work out the anatomy of a, well, of a nexus

-- psyche, STT.

---

#### flows/1a6ca4/vision/thinkingMachineProcedures.md — 2026-09-05 — standing

#### 2026-09-05 — data goes through acceptance and review processes; procedures for accepting, raising, taking down, replacing

Said after naming the Nexus, mind and psyche components:

> All of these components are going to use thinking machine calls in their machinery to go through acceptance processes and review processes, so data isn't just going to come in because it's being submitted. It's going to go through. You can look, if you get that far, into Steve Yegge. He's written about his wheelhouse harness, which is closed source, but he's written blogs about it. Essentially, we're going to be doing something a little bit similar to that, where there's going to be a kind of legal system in the sense that there are going to be procedures for things to be accepted, things to move up in importance, things to be taken down, or things to be replaced. It's a lot more complex system than just letting any agent just write files and push commits.

-- psyche, STT.

---

### Topic 9: Actor library (bearing on Nexus)

#### vision-raw/actorLibrary.md — 2026-08-21 — standing

#### 2026-08-21 — re arc mutex ban: the approach disliked; review the actor library we use and whether the nexus skill documents it

> Re arc mutex ban: I dont like the approach anyway. I want to review
> the actor library we use, and if it is well documented in the nexus
> skill

---


#### Files matched by grep but carrying no entry on these subjects (subagent list)

Files that matched the grep but had no entry on the subjects covered:

- `Vision/datom.md` — mentions "datom nexus" once in the Repository and migration section as a future name; the Datom substance is a separate topic. The one relevant sentence is quoted under datomNexus relations.
- `Vision/ethosMonolith.md` — mentions "Nexus" in terms of ethos-monolith becoming one and the vocabulary carried; the relevant lines are quoted under the Nexus and Ethos relation. The file is primarily about the ethos-monolith shape, not Nexus itself.
- `Vision/protos.md` — mentions "daemons" only in context of the three-daemon Protos engine; no Nexus entry as such.
- `Vision/highLevelView.md` — no Nexus entry; only a general design principle.
- `flows/01a03d6e/vision/nexus.md` — title only, no content beyond the heading.
- `flows/e06e4c07/vision/flowDaemon.md` — title only ("flow daemon"), no content beyond the heading.
- `flows/358f143a/vision/flowDaemon.md` — title only ("flow daemon"), no content beyond the heading.
- `flows/01a02fd5/vision/nexuses.md` — title only ("nexuses"), no content beyond the heading.
- `flows/55d18f4f/vision/itsATranslator.md` — the daemon mentioned is the protos-translator, not the Nexus concept per se; incidental use.
- `flows/01a02a34/vision/progression.md` — mentions meta-harness in context only; "take one bite at a time" is about incremental progression, not Nexus.
- `flows/01a0238b/vision/emacsPlugin.md` — mentions "daemon-backed TUI" incidentally in the Codex context; not about Nexus.
- `flows/cf0ed9/vision/openaiLacksTheFeatureIWant.md` — mentions "daemon" only in the context of shared-daemon integration for OpenAI; incidental.
- `flows/01a047d2/vision/remoteControl.md` — "I dont want to start a nexus for this" — a negative ruling about not using Nexus for the code server; the file is primarily about the code-server feature.
- `flows/01a03f49/vision/remoteControlAllTheCodexTuiSessionsICreate.md` — mentions "daemon-backed TUI" incidentally; not about Nexus.
- `flows/01a02b46/vision/zeusUpdate.md` — mentions "demons" in quoting the living's STT; it says "three demons" reading "three daemons" in the mainFunction context; no Nexus entry.
- `flows/1030529c/vision/workspace20.md` — mentions "sub agents" and "system prompt" in the context of workspace 2.0 design; the relevant subagent lines are quoted under gradientsOfAuthority above.
- `flows/13cfc23f/vision/threeStacks.md` — mentions "demons" reading "daemons"; about the three stacks, not Nexus specifically.
- `flows/ba906ae2/vision/archive-threeStacks.md` — mentions "daemon"; about the ethos-monolith being a daemon; the relevant part is quoted under ethosMonolith.
- `vision-raw/archive-threeStacks.md` — mentions "daemon-era architecture" once; the file is about the three stacks and Datom/Ethos naming.
- `vision-raw/archive-rustComponentArchitecture.md` — not read; the file is archived and the nexus-relevant content from e06e4c07/vision/rustComponentArchitecture.md was read instead.
- `vision-raw/spirit.md` — mentions "daemon" only in the context of the spirit component vs spirit file distinction; incidental.
- `vision-raw/mentci.md` — mentions "daemon" in the context of Mentci having a daemon for central logic; a separate component from Nexus.
- `vision-raw/machineAnatomy.md` — about the general 3-part machine anatomy; mentions "three demons [daemons]" once referencing the Protos engine; not a Nexus entry.
- `vision-raw/mainFunction.md` — mentions "three demons [daemons]" once referencing the Protos engine; primarily about the main function pattern.
- `vision-raw/lojixOwnership.md` — mentions "Lojix daemon"; incidental.
- `vision-raw/workingSpiritNewEthosSyntax.md` — not read; file name does not suggest Nexus content.
- `vision-raw/domainKnowledgePlacement.md` — not read; file name does not suggest Nexus content.
- `vision-raw/attunement.md` — not read; file name does not suggest Nexus content.
- `flows/15b67974/vision/flowKnowledge.md` — mentions Nexus incidentally ("the momentum assumption is thoroughly disproven" re the nexus skill not documenting the actor layer); the context is about flow knowledge generally.
- `flows/15b67974/vision/skillsRepository.md` — mentions "subagent roles" but not Nexus; about the curriculum pipeline.
- `flows/aa4c7747/vision/dispatches.md` — mentions harness incidentally ("lets get codex working"); about the dispatch process.
- `flows/aa4c7747/vision/promptCrafting.md` — mentions harness in "dont explain things that the harness does automatically"; primarily about prompt-crafting.
- `flows/2f6b1dc5/vision/contextStrata.md` — mentions base-prompt replacement design but the entries are about the context-strata skill deployment, not Nexus.
- `flows/012fbf07/vision/archive-threeStacks.md` — mentions daemon, nexus types, and meta-harness; the relevant entries are quoted under gradientsOfAuthority and threeStacks above.
- `flows/e06e4c07/vision/letsUseTheSameVocabulary.md` — mentions "harness" in "transcript names the harness's whole-session file"; vocabulary entry, not Nexus.
- `flows/e06e4c07/vision/skillDesigning.md` — mentions Nexus only incidentally ("the nexus porting-by-extraction sentence"); about skill-designing rules.
- `flows/e06e4c07/vision/gradientsOfAuthority.md` — mentions "magic" and the psyche/computer relationship; not about Nexus.
- `flows/e06e4c07/vision/rustComponentArchitecture.md` — cross-posted from the nexus entry; the relevant content is identical to flows/e06e4c07/vision/nexus.md, already quoted in full.
- `flows/15b67974/vision/psycheLogStructure.md` — not read; about psyche log structure.
- `flows/15b67974/vision/skillDesigning.md` — not read; about skill designing.
- `flows/62022e8f/notion/layerMatching.md` — not read; a notion.
- `flows/78c93c/vision/witness-reuse.md` — not read; about witness reuse.
- `flows/7fba5f/vision/reporting.md` — not read; about reporting.
- `flows/a5940a/vision/mainFlowShouldNeverTryToLocateAFile.md` — not read; about file location.
- `vision-raw/archive-encodedFormIsTheCode.md` — not read; about encoded form vocabulary.
- `flows/358f143a/vision/behavior.md` — not read; about behavior.
- `flows/358f143a/vision/falseConfidence.md` — not read; about false confidence.
- `flows/358f143a/vision/letsUseTheSameVocabulary.md` — not read; about vocabulary.
- `flows/358f143a/vision/managementDelegation.md` — not read; about management delegation.
- `flows/358f143a/vision/skillDesigning.md` — not read; about skill designing.
- `flows/01a02fd5/vision/interfaces.md` — mentions Nexus only in the context of ethos interfaces for signal repos; the relevant ruling is about writing interfaces in ethos, not about Nexus architecture.


### 2b. Mind, psyche (component and log machinery), flow (component and protocol)

(Gathered by subagent; its inference is marked [agent inference].)

Gathered by research subagent for flow 1a6ca4, 2026-09-05. All quotes verbatim. My inferences are marked [agent inference].

---

### Topic: MIND

#### Distilled Vision

(No distilled Vision file exists for "mind". The concept first appears in flow 1a6ca4.)

#### Raw Vision

#### flows/1a6ca4/vision/mind.md — 2026-09-05 — standing

> ## 2026-09-05 — the mind component replaces the files, readmes and indexes; the memory of the system goes in mind
>
> Said while naming the components to bring onto the new stack after orchestrate:
>
> > There's the mind component, which is essentially going to replace a lot of the files and the readmes, not the psyche log (the psyche log is obviously going in Psyche, which is why Psyche is so important: it gets its own sort of mind-like component). The mind will kind of replace all this reporting and keeping track of which repositories are involved, what kind of knowledge and witnesses, and all of this stuff that we're clumsily doing with Markdown files and indexes and all of that stuff. It's keeping them, summaries of transcripts, and essentially the memory of the system is going to go in mind [STT: "mine"].
>
> -- psyche, STT.

[Agent inference: This is the first and only record on "mind" as a component. It is new as of this flow (1a6ca4) and has no earlier records or distilled form.]

---

### Topic: REMEMBERING / FLOW KNOWLEDGE / WITNESSES / TRANSCRIPT SUMMARIES / DOCUMENTATION PLACEMENT

#### Distilled Vision

#### Vision/remembering.md — distilled — standing

> # Remembering
>
> ## All flows are one subjectivity
>
> All flows are one subjectivity; this is the reason behind
> remembering. Told "you did" or "you said" of a thing it did not
> itself do or say, a flow remembers it at a depth fit to the question,
> reaching the transcript directly when the logs are not enough.
>
> ## The last model response is read
>
> Remembering a flow includes reading that flow's last model response.
>
> ## The remembering line says what was found most relevant
>
> The log's record of a remembering carries a short description of what
> from the remembered flow was found most relevant to the current one.

Sources: b675f3d9 remembering

#### Vision/highLevelView.md — distilled — standing

> # High-level view
>
> ## The very high-level view is looked at routinely
>
> The very high-level view of what is being built is looked at
> routinely.
>
> ## A view takes room
>
> A high-level view takes room and breaks everything down in-line.

Sources: vision-raw highLevelView, b675f3d9 highLevelView

#### Raw Vision

#### flows/b7465e71/vision/remembering.md — 2026-08-22 — standing

> # Remembering
>
> > Remember 5c8be3ca and 15b67974
> >
> > Remembering is a new skill I want to design with you which is quite
> > simple: it will use the flows protocol to bring back the contextualized
> > psyche and a high level awareness of the work done in some past flows.
> > Actually, it could just be an extension of the flows skill, which would
> > allow the chain of remembering to be logged and therefore traced back
> > (with deep remembering done only when going deep into a topic; single
> > layer on fresh session startup, unless explicitely told otherwise, and
> > up to a certain number in deep work, possibly unlimited number when
> > explicitely told to mine all the way back to the deepest layer possible
> > which would be rare)
> >
> > As for everything else, lightly audit/review the current state of
> > things touched by the topics covered in your past (vocabulary/shorthand
> > for past flows), and give a light summary of it all in very simple
> > words and visuals. this will also become a part of this protocol
> > extension.
>
> ## why create more artifacts? the main log file should have the remembered flows
>
> 2026-08-22 — on the agent's proposal that a remembering be filed as
> `reports/remembering<ShortId>.md`:
>
> > what do you mean by that? why do you think remembering should go
> > into a report? If the flow pulls things into its context, it has
> > remembered. why create more artifacts?
> >
> > the main log file should have the remembered flows.
> >
> > what is the best format for LLMs to hold data like this? is
> > frontmatter good, or do those --- delimiters just cost tokens
> > without upside?
>
> ## vocabulary is good, but lets settle the flows edit before sending
>
> 2026-08-22 — on the proposed vocabulary entry "Past: the flows a flow
> has remembered, and theirs in turn." and the flows-skill edit:
>
> > vocabulary is good, but lets settle the flows edit before sending.
>
> ## send the edits
>
> 2026-08-22 — green on the settled flows edit and the vocabulary entry:
>
> > send the edits.
>
> ## delete the reports since they could induce a pattern
>
> 2026-08-22 — on the two remembering reports filed before the
> no-artifact ruling:
>
> > delete the reports since they could induce a pattern.

#### flows/b675f3d9/vision/archive-remembering.md — 2026-08-26 — archived

> # Remembering — archived
>
> ## The last model response of the remembered flow must be read
>
> 2026-08-26, the psyche, typed:
>
> > new addition to remember protocol: the last model response of the remembered flow must be read
>
> ## All flows are the same subjectivity; "you did" / "you said" obliges remembering
>
> 2026-08-26, the psyche, typed:
>
> > flow protocol clarification: all flows are the same subjectivity. anything not mentionned but not remembered can be recalled by searching other flows ("remembering"). So the living may say "you did" or "you said", in a flow that did not itself "do" or "say" those things; in this case the flow in question must endeavor to try to remember, with an appropriate level of detail, which may entail more than simply using the flow logs (searching transcript directly).
>
> ## The remembering log line carries what was found most relevant; "all flows are one subjectivity" heads the paragraph
>
> 2026-08-26, the psyche, typed, ruling on the flows-skill edit proposal (reports/flowsSkillEditProposal.md):
>
> > yes that is good. and the remembering log should also have a short description of what was rembered from that flow which was found most relevant to the current flow.
> >
> > "all flows are one subjectivity" should at least begin the paragraph, or it could be a section name; in a way it explains the reasoning behind the remembering protocol

[Agent inference: archived into Vision/remembering.md by a later distillation.]

#### flows/e06e4c07/vision/flowKnowledge.md — 2026-08-19 — standing

> ## 2026-08-19 — a flow knows what the other flows concerned know, and vice versa
>
> Design session `e06e4c07`, typed (captured 2026-08-19T14:33+02:00).
> The Designer had proposed no skill wording on mandatory traits and
> ontology-before-implementation because "the placeholder-trait failure
> and the design-ontology-before-implementing workflow are being
> discussed in another flow":
>
> > I dont work like that. Id rather the discussion drip into every flow
> > which it concerns. I want this flow to know what the other knows and
> > vice versa.
>
> ## 2026-08-19 — a skill, or a specialized subagent role that reads recent sessions for what impacts its parent flow; session files must become accessible and searchable for agents
>
> Design session `e06e4c07`, typed (captured 2026-08-19T14:51+02:00),
> answering whether the drip rule should be Intent:
>
> > Re flow info sharing: It should be a skill, or maybe even a
> > specialized subagent role which looks at recent sessions for psyche
> > rulings and insights/information which directly impact its parent
> > flow. This brings me to the topic of session files, and how we can
> > make them more accessible/easily-searchable for agents; are there
> > tools for this? Iv discussed this in another flow already, but it
> > fell out of the conversation and we didnt really address it.
>
> ## 2026-08-19 — transcripts belong to another nexus; for now a small clever search tool: typed prompts first, the few preceding model responses, line numbers
>
> Design session `e06e4c07`, typed (captured 2026-08-19T17:00+02:00),
> answering whether the harness transcripts belong to the flow Nexus:
>
> > obviously another nexus. But we might want a small clever tool to
> > help search those files more efficiently for now.
>
> > finding the user typed prompts is an obvious first step. then we
> > would need the few preceding model responses, to give those prompts
> > context. and the result would have to contain line numbers, to allow
> > a more fine-grained search to proceed after the bulk of the gold has
> > been found.

#### vision-raw/domainKnowledgePlacement.md — 2026-08-08/09 — standing (legacy)

> # Domain knowledge lives in its domain
>
> > "information that is specific to a specific task, to a specific
> > domain needs to live in that domain, in that repository. And then
> > managers don't have to tell their sub-agents how stuff is done.
> > The agents will just find all the instructions along the way."
>
> — psyche, 2026-08-08, steward session
>
> ---
>
> > "all repos should document their usage/editing patterns. better
> > yet; docs live in the code they document"
>
> — psyche, 2026-08-09, steward session
>
> ---
>
> > "we cant keep our documentation poor and just use bigger models
> > as an excuse not to get our guidelines in order"
>
> — psyche, 2026-08-09, steward session

#### flows/e4a40e/vision/witnesses.md — 2026-09-03 — standing

> # Witnesses
>
> ## 2026-09-03 — reuse verifications without running them all over again
>
> The flow had proposed a design-skill line that a claim about Rust or a
> tool enters a proposal only witnessed, by compiling or running it.
>
> > Your skill edit proposal is too narrow, and we had already verified how traits naming behaves in Rust [STT: REST] many times before. What is keeping us from being able to reuse these verifications without having to run them all over again? How can we be more efficient with our witnesses? What is missing in the current training? How is the protocol lacking to achieve this?
>
> -- psyche, STT.
>
> ## 2026-09-03 — a witnesses directory in each flow, found by the same directory structure
>
> The flow had proposed a subject-keyed store of witnesses beside Vision/.
>
> > Well, that's not what I remembered. I remembered creating the flow protocol whereby there was a witness or witnesses or witnessed directory in each flow, where witnesses would be stored so that they could easily be found because they all have the same directory structure, right? There's a way to find these easily. Did I remember wrong, or was my vision not implemented properly?
>
> -- psyche, STT.

#### flows/78c93c/vision/witness-reuse.md — undated (pre-2026-09-03) — standing

> # Witness reuse
>
> "We need to design some kind of witness indexing by topic, a natural language approach."
>
> "I'm not literally meaning caching in the way it's been traditionally used in software. I'm more using caching in a thinking machine kind of way, whereby a cheap thinking machine model would compare."
>
> "It's kind of like what we have been doing in the spirit component, which has been shelved for now and has to be ported over to this newly called psyche component. The nexus is where we were doing an LLM call to check if the proposal already existed and if it was contradicting something already in the database and stuff like that."
>
> "It requires using a thinking machine model to do the caching verification. It's natural language-based, sort of like how we humans would say, 'Oh, do you remember when such and such?' I wouldn't have to use the exact same words with the exact same speed, order, and tone. That is what software caching has to be exact and purely mathematically provably the same, which is not what I'm talking about here at all."
>
> "We need to design something like that, which is kind of simple, because we can't really do complicated software yet. I'm still trying to put together the language ethos that I want to use to design my software. We're in the mud here, trying to just get our necks out of the water."
>
> "The key problem: every session doesn't have good access to what's already been done before."
> -- psyche, STT.

#### flows/cff271af/vision/reports.md — 2026-08-22 — standing

> # Reports
>
> ## 2026-08-22 — "do we even need reports?"
>
> Context (agent, brief): the flow had admitted it filed the
> software-design review packet unread, relaying the subflow's account
> in near-factual voice. The psyche then questioned the value of
> subflow-written reports as such. Verbatim, spoken to flow cff271af:
>
> > Here's the thing. The living speaks to the main flow. So, if we
> > have a bunch of artifacts, I mostly don't read reports. They're
> > there for... To be honest, right now I'm wondering, in most cases,
> > do we even need reports? Because if the audience is in the main
> > flow, and in almost all the cases is not me, then what is really
> > the intended audience? And what is the point of doing all this
> > research if the main flow only really just pretends to be or is
> > only superficially aware of them? So, it's alright for subflows to
> > do research. That's their purpose. But I don't see that much value
> > in them creating all these reports. Because, see, the problem is
> > the main flow won't actually be aware of their content. And then
> > the conversation will go through, this flow will go through its
> > life, its cycle, and then another flow will remember it and
> > perhaps probably consider these reports as having had an influence
> > on its past, where in fact it only had a superficial influence on
> > its past, since the main flow is the main flow. So, tell me what
> > you think about all that.
>
> No ruling yet — the psyche asked the flow for its assessment.
>
> ## 2026-08-22 — the strata; the subflow's response is in the transcript; the prompt is the precious stratum
>
> > Yeah, there's some interesting things you've raised here, and
> > there's something I want to point out, which is that if an
> > agent's, sorry, if a subflow's output is only its response back to
> > the main flow or to its parent, that data still sits in the
> > transcript file. So making the subflow write a report and then
> > making the main flow read the report just seems like useless
> > churn. We're not really worried about subflows spending a few more
> > tokens, especially when we're talking about cheap models like
> > Sonnet and Luna. What is really important is the main flow's
> > context and implementation workflows being essentially
> > well-informed, which should not depend on a bunch of reports that
> > subagents wrote, because the conceptualization of what the subflow
> > really ought to do, that liability really falls on the main flow,
> > because the main flow is what interacts with the living psyche, or
> > it's as close as it gets. So if anything, if an implementing
> > subflow must be given data, must be given the full response of a
> > previous subflow, what really is the cost? What is really the
> > extra cost? And let's say we produce a simple tool designed
> > specifically for this, and I think we already have something that
> > falls within that sort of use case that would allow... Because
> > see, the problem with... It's the strata. The problem is the
> > strata. If we make some... If we judge something to be important
> > for an implementation subflow, and we tell that subflow to read
> > that using tool calls, then we're putting that information, which
> > is supposedly important, at the bottom stratum. And the only way
> > to put information in its mid-stratum is bypassing its prompt, so
> > essentially for the main flow to give it to it. Until we have a
> > more advanced meta-harness that can do really cool stuff, like
> > fetch a bunch of responses from a bunch of previous flows as the
> > prompt, or perhaps even after editing it through another flow,
> > passing that as a prompt to yet another flow, until we have that,
> > we essentially have to depend on the current infrastructure, which
> > is that the most useful and precious context is only that which
> > the parent flow gives it as its starting prompt.

#### flows/7fba5f/vision/reporting.md — undated — standing

> # Reporting
>
> ## The protocol: the main Claude agent writes a Markdown report, a sub-agent makes the Claude web report from it
>
> > this protocol whereby the main Claude agent creates a Markdown report, and then a sub-agent creates a Claude web report from it. Let's formalize that into a skill.
>
> -- psyche, STT.
>
> ## The same protocol for Codex: a Markdown file, a sub-agent's web report the living can annotate, the Codex agent reads the annotations
>
> > developing a similar workflow to use with Codex, so that Codex could also use the same protocol. It creates a Markdown file, and a sub-agent creates a web report that I could actually annotate. The Codex agent could then read the annotations that I made to the report and do all of the research you need to do to find out what the best solution is for that.
>
> -- psyche, STT.
>
> ## The reporting skills are Claude-only for now
>
> > the skills for the reporting, which, for now, would be Claude only, since Codex doesn't have that and we have a way to specify Claude-only sections and skills, or maybe that is a new skill.
>
> -- psyche, STT.

#### flows/78c93c/vision/machine-generated-content.md — undated — standing

> # Machine-generated content
>
> "Whenever something is machine-generated, whether I say so explicitly or maybe we could even ask the machine to guess that something was machine-generated, that something was pasted in. In other words, that another machine, another thinking machine, had generated that. This none of the content in it should be logged as psyche."
> -- psyche, typed.

#### vision-raw/surveyingAllFlows.md — 2026-08-17 — standing (legacy)

> # "surveying all the flows, verifying what has been done, what hasnt"
>
> ## 2026-08-17T17:31+02:00 — an aspect focused on surveying all the flows
>
> Context (agent-authored, separate from the psyche's words): opening vision for a Design session. The function is stated; the name remains deliberately unsettled pending anatomy and research.
>
> > I want to design an aspect focused on surveying all the flows, verifying what has been done, what hasnt. To keep things from getting out of hands and falling through the cracks. We'll need a name. Maintenance comes to mind but it really doesnt do it justice, nor does survey. Overseer maybe.
>
> — psyche, Design session 72939228, typed.

#### flows/55d18f4f/vision/highLevelView.md — 2026-08-08 — standing

> ## 2026-08-08T11:23:57.351Z — I think the biggest lesson from this is that we need to routinely look at the very high-level view of what we're building
>
> > I think the biggest lesson from this is that we need to routinely look at the very high-level view of what we're building, because then it would have been obvious to me right away. And I have, you know, used this concept of high-level view, showing me the high-level view with agents before, but I've never seen an agent pull it off. It's like they don't understand how to explain their project in simple terms. Like, here's this repo, here's, like, the concept of what it is and how much it does, and, like, I don't know, maybe you want to, like, send an agent on a research about this. Like, how do you explain an engine simply in a very high-level view? Like, let's say you had a whole day to explain, maybe not a whole day, but, you know, like, that would be a very big engine, but let's say if you only had, like, half an hour to explain something to someone who's coming on to a project, you would want him to have, like, a very clear view of the whole engine from a high level. That's really what I mean.
>
> — psyche, 2026-08-08T11:23:57.351Z (Designer session 55d18f4f)

#### flows/01a05e95/vision/logging.md — undated (late August) — standing

> # Logging
>
> ## Rare, high-level flow logs
>
> > "Logging should be rare. It should just be to give a very high-level summary. ... The transcripts are there. If we really need to know the details of what happened, we can look into the transcript. After not so long, those details are not really relevant anymore ... These logs are just gonna keep growing, and they're getting really big. A thousand lines of logging just for a single session is fucking insane."
>
> -- psyche, typed.
>
> ## Subflow logging
>
> > "Well, it's because the sub flows are logging everything, it looks like. That's overkill. Maybe the sub flows should not really log, at least not in a way that the main flow is logging."
>
> -- psyche, typed.
>
> ## Subflow production and context
>
> > "The point of a subflow is for it to edit what it edits and then return the final response. Like I said, the transcript is still there if we really need to know what happened. For it to do all of this logging doesn't just create a lot of all these log files, but it also pollutes this subflow's context. ... It distracts it from its main task by making it constantly add a line every stop. It adds this self-talk, the commentary, where agents' flows talk to themselves, which I don't know if it's useful at all. It just creates a whole lot of noise, and I think it will destroy or reduce the efficiency and the quality of the end result."
>
> -- psyche, typed.

#### flows/aa4c7747/vision/sessionLog.md — 2026-08-24 — standing

> # sessionLog
>
> ## 2026-08-24 — the log makes the flow's main points easily accessible; timestamps not enforced
>
> > lets simplify it. we dont need to enforce time stamping so much; the transcripts have the time. we're just making the flow's main points easily accessible. So lets remove first; try a fresh approach

---

### Topic: PSYCHE (as component or log machinery)

#### Distilled Vision

#### Vision/distillation.md — distilled — standing

> # Distillation
>
> ## Vision impurities
>
> A working instruction logged as vision is a vision impurity. It may
> sit in a log beside valid vision; when distillation finds it, the
> impurity is dissected out of the log and destroyed, and the valid
> vision around it stays.
>
> ## Impurities fall out through distillation
>
> Impurities come out in the course of distillation: a distillation
> proposal points out the impurities it dissects out, and the living
> rules on them with the statements.
>
> ## A proposal names each statement's destination
>
> A distillation proposal says, for every statement, the topic it goes
> to; a statement under the wrong topic is corrected by a distillation
> edit of its own.
>
> ## A statement carries what the psyche said
>
> A distilled statement carries what the psyche said and nothing
> beyond it. A small ruling makes a small statement.
>
> ## Designing model behavior is vision
>
> Designing model behavior is vision, and a correction of an agent's
> conduct can be vision. The line of what counts as designing is drawn
> wide, and what does not qualify as vision is stated with the same
> clarity.
>
> ## No useless negatives
>
> A distilled statement carries no useless negative. Such negatives
> stay in the archive, which remains linkable.
>
> ## A statement never attributes itself to the psyche
>
> Vision is the psyche's; a distilled statement never says so of itself.

Sources: b675f3d9 visionImpurities, acbb6006 distillation, b675f3d9 distillation, ac1e9ec8 distillationNegatives

#### Raw Vision

#### flows/1a6ca4/vision/psyche.md — 2026-09-05 — standing

> # Psyche component
>
> ## 2026-09-05 — the psyche log goes in Psyche; Psyche gets its own mind-like component
>
> Said while describing the mind component:
>
> > not the psyche log (the psyche log is obviously going in Psyche, which is why Psyche is so important: it gets its own sort of mind-like component).
>
> -- psyche, STT.

#### flows/012fbf07/vision/threeStacks.md — 2026-08-11 — standing

(Excerpt relevant to the psyche component:)

> ## 2026-08-11 — a new component named psyche; spirit-ethos should not have existed
>
> > I have a better approach now, for a new component which will
> > include spirit, named psyche, which will hold spirit, intent and
> > vision, and be used to feed the hijacked llm calls (we need a name
> > for that... you know what im talking about?)
>
> > I dont even know why we made that repo. the ethos code can live
> > with the component. like all components (component + 2 signal
> > repos)
>
> — psyche, 2026-08-11T00:39+02:00 (Designer session 012fbf07), typed.
>
> ## 2026-08-11 — datom confirmed; the top-level layer enum
>
> > 1 yes. we re-use much of spirit, and
> > introduce a top-level enum; Spirit, Intent, Vision, which
> > differentiates which layer records belong to. 3 yes
>
> — psyche, 2026-08-11T12:04+02:00 (Designer session 012fbf07), typed.

#### flows/012fbf07/vision/psycheLogStructure.md — 2026-08-11 — standing

> ## 2026-08-11 — the design log is now the psyche log
>
> > that expression needs to be rooted out. it is now the psyche log.
>
> — psyche, 2026-08-11T18:23+02:00 (Designer session 012fbf07), typed,
> on the management skill's phrase "the design log": the expression is
> rooted out everywhere; the thing is the psyche log.

#### vision-raw/psycheLogStructure.md — 2026-08-09 to 2026-08-14 — standing (legacy)

> # Psyche logs organized by topic, not aspect
>
> > "psyche shouldnt be organized by aspect, but by topic and date"
>
> — psyche, 2026-08-09, steward session
>
> ## 2026-08-14 — topic governance, the cleaning pass, a new psyche skill
>
> > lets reframe that to make new topic a psyche blocked thing, and
> > lets create a list of topic which are allowed for now. Or maybe
> > we just do merging passes to make it easier to log "safely", so
> > the flow doesnt have to overthing where to write something down
> >
> > I think this also brings the subject of keeping the psyche clean;
> > after a while too many entries will exist, many of which will be
> > overruled statements. The cleaning/merging pass is the way. But
> > it needs to be psyche assisted to avoid mistakes. So an agent
> > makes proposal statements which are aimed at replacing a bunch of
> > psyche records and the psyche pronounces on them, then the old
> > records are archived. it should even be archived to link back to
> > the record(s) that replace them, ostensibly with a short hash.
> > How does that sound?
>
> > yes, that is better and should help slightly, get it deployed
> > (through the skills repo of course)
>
> > lets create a new psyche skill. find a name and make a first
> > proposal.
> >
> > and some of the vision should be transferred into skills. we
> > should have a manifest then that links some skills to psyche
> > archives. see my discussion with claude d2bb5f5f
>
> — psyche, 2026-08-14 (Designer session 06196cc7), typed.
>
> ## 2026-08-14 — "agent annotations are not records" was never ratified
>
> Reconstructed 2026-08-22 by design session `15b67974` from transcript
> 06196cc7 L716 (2026-08-14T11:20Z):
>
> > I dont understand
>
> Context (agent-authored): the Designer explained the two kinds of
> text in a psyche file (the psyche's quoted words; the agent's context
> lines); the psyche's next message moved to the id scheme without
> approving or rejecting the principle. It stands unratified.

#### vision-raw/psycheIsntPerAspect.md — 2026-08-09 — standing (legacy)

> # "thats wrong. the psyche isnt per aspect"
>
> 2026-08-09T15:57:34Z
>
> Agent context, separate from the psyche's words: said while correcting how
> written psyche is organized.
>
> > thats wrong. the psyche isnt per aspect

#### flows/06196cc7/vision/psycheLogStructure.md — 2026-08-14 — standing

> ## 2026-08-14 — statements are not topics; the swarm of tiny files
>
> > encodedFormIsTheCode was a very poor choice of topic. thats not a
> > topic, thats a statement. now im looking at those files, and
> > theres so many bad topic; colonLegalInStringPosition
> > colonConfusion flowsNotAgents genericParametersAreTraits
> >
> > why are the topics so specific? this will make it hard for agents
> > to find something. are we afraid of having big files so much that
> > we end up with a swarm of tiny files?
>
> — psyche, 2026-08-14 (Designer session 06196cc7), typed.
>
> ## 2026-08-14 — distillation corrections: re-articulation, many-to-many, 4-hex ids, psyche-archive/
>
> > not necessarily. if the records being distilled cover many
> > topics. the same input might be used as a reference for many
> > outputs
>
> > if we dont specify how, itll be chaos
>
> > You didnt undestand the distillation meant we abandonned allowed
> > topics?
>
> > quotes them? that would create a mess. this is our opportunity to
> > re-articulate everything, it would be foolish to miss on that.
> > the referenced archives still contain the original quotes
>
> > no way we are getting this complex. why would we do that? and
> > 8!? Where did my short ID approach go? we use 4 and rarely have
> > problems. and in this case, a collision wouldnt be a very big
> > deal. cant the llm just produce 4 random hex?
>
> > no, for two reasons; the records will be considered individually
> > and whole topic files might not be distilled, and one
> > distillation might come from two or more topics. also, it
> > shouldnt be in psyche/ - lets use psyche-archive/
>
> — psyche, 2026-08-14 (Designer session 06196cc7), typed.
>
> ## 2026-08-14 — distillation is ongoing; the chain of origin
>
> > We don't need to think of it only as something that is done in a
> > pass. If a flow comes across records that he feels could use
> > distillation, then he can make the proposal right there and then.
> > So the distillation can be an ongoing process, and we can have a
> > list of clues or explain situations where a proposal for
> > distillation is appropriate. So we can do distillation passes,
> > but it doesn't need to only always happen that way.
>
> > I also want to start considering something which we can develop
> > further on the next session, but which you can already have in
> > your context for perspective, which is I think Psyche logging
> > could be done with the short session ID besides every records,
> > which would let a later agent verify the entire conversation if
> > the session file is still there and would allow that flow to
> > possibly get an actually better understanding of what the Psyche
> > was saying because he has different perspective and a better
> > focus. So like this chain of origin is essentially the concept
> > that is appearing out of all of this approach. And I'd like us to
> > just keep it in mind and maybe start, maybe we can do some, yeah,
> > maybe we can start logging the Psyche that way. And yeah.
>
> — psyche, 2026-08-14 (Designer session 06196cc7), the second part dictated.
>
> ## 2026-08-14 — ids are increasing numerics; archives are date-based append-only files
>
> > Actually I've changed my mind on hashing the IDs. We should just
> > create archives based on dates and append-only files, and give
> > each new entry an increasing numeric ID.
>
> — psyche, 2026-08-14 (Designer session 06196cc7), typed.
>
> ## 2026-08-14 — the id scheme is unresolved: global counter versus compound references
>
> > I don't understand how you think the numeric ID is going to work.
> > Right. If you're saying that we're using an increasing number all
> > the time for all the files, then how do we know what the latest
> > number is to add another entry? Otherwise, each file has its own
> > numbering, which means that a reference needs to know. Like for
> > example, if we archive by date, then a reference would be the
> > date and the number. And if the raw logs are by topic, then to
> > reference a raw psyche log, we need the topic and the ID, unless
> > there's something I'm missing here.
>
> — psyche, 2026-08-14 (Designer session 06196cc7), dictated.

#### flows/fb1008c0/vision/psycheLogStructure.md — 2026-08-14 — standing

> ## fb1008c0-1 — 2026-08-14 — session-scoped ids; retrofit by origin hunt
>
> > I see your C now; the agents knows his own counter. thats clever.
> > and we could hunt for the origin of every existing record to
> > retrofit them. I like that idea
>
> — psyche, 2026-08-14T14:03+02:00 (Designer session fb1008c0), typed.

#### flows/15b67974/vision/psycheLogStructure.md — 2026-08-22 — standing

> ## 2026-08-22 — considering: psyche logging into the flow protocol; more frequent distillation; a distilled file in the flow's directory
>
> > now im considering moving psyche logging into the flow protocol as
> > well, and emphasizing more frequent psyche distillation, with
> > distilled entries kept in their flow's directory but moved into a
> > "distilled" file or something similar.
>
> ## 2026-08-22 — psyche/Vision becomes the home of distilled psyche; raw psyche lives in flows/*/psyche/; archives are archive- prefixed files in the same directory
>
> > yes and that would now become the home of distilled psyche going
> > forward. so finding raw psyche would search flows/*/psyche/
>
> > no, distilled logs are moved into an archive- prefixed file in the
> > same directory
>
> ## 2026-08-22 — distillation defined: self-standing records, clarified and purified by the model, always explicitly reviewed by the living psyche; agglomerate across flows, favor recency and certainty
>
> > context is crucial to understand any statement. a distilled record
> > is self-standing; clarified and purified by the model, which do
> > this very well, but *always reviewed explicitely by the living
> > psyche*
>
> > so essentially, psyche distillation is the model attempting to
> > articulate the psyche in a more coherent form, agglomerating
> > records made across several flows that touch the same topic,
> > favoring more recent statements, and favouring statements made
> > with more certainty, when overlapping or contradictory readings
> > surface.
>
> ## 2026-08-22 — a skill is still a file; rename the undistilled corpus; log vision: flows/<id>/vision/; top-level psyche/ maybe unnecessary — Vision/ and Intent/ as typed directories
>
> > 1. a skill is still a file. and untill the entire psyche/ corpus is
> > distilled, that proposal isnt true. we could rename the current
> > corpus's main directory to make this clear, and encourage
> > distillation into the new location
> >
> > and I just noticed something; we are loggin psyche, yes, but more
> > specifically we are logging psyche *vision*. so we should make it
> > flows/<id>/vision/...
> >
> > this could even make the top level psyche/ unecessary. distillation
> > could happen in vision/ and intent/ (maybe Vision/ and Intent/
> > carry more cognitive weight, and the caps imply a typed directory),
> > with spirit being treated in a special way for technical reasons.
>
> ## 2026-08-22 — forks ruled: psyche-raw good; the case split liked; raw intent and spirit only from the living
>
> > 1. good
> > 2. clever. I like it
> > 3. raw intent, as well as spirit, will always be explicitely brought
> > up by the living <- wow! the living is a perfect shorthand for
> > living psyche.

#### flows/1030529c/vision/psycheLogStructure.md — 2026-08-14 — standing

> ## 1030529c-1 — 2026-08-14 — agents generate psyche data or delegate from it; distilled psyche seeks a skill home
>
> > right. psyche data is anchored in the psyche skills
> >
> > actually, what should happend with the data youre trying to move
> > is you should make a psyche proposal.
> >
> > In fact, this is a really good idea. So when agents want to write
> > something down that they've sort of semi-synthesized from whatever
> > they're doing, either it agrees with Psyche, and therefore it
> > could really just be a Psyche record, but in that case, obviously,
> > it would have to be approved by the living Psyche. Or it's not
> > Psyche, or it doesn't align with Psyche, in which case it's
> > garbage. So really, an agent that's interacting with the Psyche is
> > really only trying to generate Psyche data, or is using Psyche
> > data to delegate implementation. And I think this is really
> > important. This is a fundamental principle, I think. And we could
> > probably distill the spirit or intent out of this, at least. I
> > know I've been neglecting intent because, you know, at least for
> > me when it's logged as vision, it's logged somewhere. So I can
> > always later on, you know. But yeah, I see intent as essentially
> > data that needs to become a skill. Because now it's so true that
> > it has enough authority to just be read by anyone who deals with
> > anything that's related to that. So it's not that all of intent
> > becomes a skill called intent. But it's that we really want to
> > sort of generate skills from intent. But this also brings me to
> > another aspect of all this, which is traceability or ancestry or
> > whatever we want to call it. ...
> > So really, what we're trying
> > to do by accumulating all this Psyche is first to give references,
> > right, for agents that can look at the vision and see what should
> > be done. But it would give more reliable results if this data was
> > loaded through a skill, because the context then would have a
> > higher LLM authority. So what I was trying to get at is that I
> > think that we could have a system whereby edits that are done on
> > skills refer back to a Psyche record or more than a Psyche record.
> > Because once we've distilled Psyche, which is we've reformulated
> > it in a more understandable and or more just like a terser,
> > direct, well-written form, which is what AI LLMs are good at, then
> > we've made it, we've created a line that is really looking for a
> > home in the skill.
>
> — psyche, 2026-08-14T15:45+02:00 (Design sibling flow 1030529c).

#### flows/04db2fd2/vision/psycheLogging.md — undated (late Aug/early Sep) — standing

> # Psyche logging
>
> ## Only include the relevant bits per vision entry; triple-dot omissions; the original is in the transcript
>
> > when we log psyche, I've noticed, and we should change that, that often the log will contain like the entire, because now I'm doing this huge speech to text. And so it's going to be a big text. So there's going to be several things that come out of this text. And I've noticed, it seems that the model tries to just, or it just reuses that whole text in all of the different logs, in all of the different visions that it logs of that text that is contained in there. But what should really happen is it should summarize, or not summarize, but only include the bits in the text that concern that particular entry, the vision entry that is being logged individually. So several vision logs will be created out of this huge monologue that I'm making now. And so we use the notation whereby like, you know, parts of a sentence that are relevant to this vision log are written in the verbatim, you know, in the psyche verbatim portion of the log. And then the spaces in between is just a triple dot notation that just means like parts of this have been omitted because they aren't relevant to this particular thing. Because the original is in the transcript. So we don't need to try and preserve the original text, the whole thing. And plus it makes the logs quite unwieldy. And it creates a lot of noise when recovering and when, you know, going through this to have this whole text all of the time. So we're going to edit the psyche logging protocol from this also. So you're going to make a proposal on how to do this.
>
> -- psyche, STT.
>
> ## No timestamps; session id is implied by the flow directory location
>
> > no, no timestamps, and the location of the logging (in the flow's directory) means the session id is already implied, so it isnt a concern at all.
>
> -- psyche, typed.
>
> ## Psyche logging spread across more than one skill?
>
> > we have psyche loggin spread across more than one skill now?
>
> -- psyche, typed.

#### flows/2ef42163/vision/psycheLogging.md — undated — standing

> # Psyche logging
>
> ## A speech-to-text error is corrected inside the verbatim quote; leaving it is misquoting
>
> > When you log Psyche verbatim and you know there's been a mistake, you have to correct it in the verbatim part because I never said r-e-s-t. I never said that; the speech-to-text made the mistake. So you're actually misquoting me if you write r-e-s-t. So we have to modify the skill because, like, obviously, what I said was not r-e-s-t. I'm talking about the Rust language. So I guess if I say Rust language, it's able to pick it up. So I'm just gonna do that. But... Yeah. You're misquoting me if you use r-e-s-t.
>
> -- psyche, STT.

#### flows/db97561c/vision/psycheLogging.md — undated — standing

> # Psyche logging
>
> ## Accepting unread recommendations is not vision
>
> > those are not vision btw, just instructions for implementation. I havent read your suggestions so there is no vision to get from my last prompt
>
> -- psyche, typed.

#### flows/04db2fd2/vision/rollingDistillation.md — undated (late Aug/early Sep) — standing

> # Rolling distillation
>
> ## Distill vision as we go; every second or third turn agents propose distillation; too much raw vision piles up and goes stale/contradictory
>
> > I want us to roll with distilling that vision. So as we go, so whenever we touch like this datum [STT: Datom] subject, you know, you can sort of take something we've touched upon like heavily and send your sub-agents like, okay, you go look for anything that might remotely like touch this, and let's distill it, because I think we're accumulating too much raw vision, and we need to start distilling it faster. So we can almost start making this like an ongoing process that agents could almost at every second or third turn propose the distillation of the vision that's been accumulating so far, along with any vision that it, you know, it would send sub-agents to go look and try to agglomerate all of this subject together, and so we don't like pile up all of this raw vision, and it sort of ends up being stale, and sort of because I changed my mind, it like starts contradicting itself, and so it's better to keep it distilling it and keeping it clean, and agents are really good at summarizing things. So like right now, this is kind of, the living psyche is a bit dirty in how it expresses itself on the first pass. This is why I said several passes is better. You know, like the greatest works ever written were not written in the first pass. There's just no way.
>
> -- psyche, STT.
>
> ## Design and psyche-distillation skill edit approved
>
> > design and psyche-distillation skill edit is good.
>
> -- psyche, typed.

#### flows/e8c4cc61/vision/psycheLayers.md — undated — standing

> # Psyche layers
>
> ## A fourth, bottom layer for brainstorm
>
> The psyche marks this itself as "maybe, not sure yet".
>
> > Brainstorm (maybe, not sure yet - lets make that part of a skill so the word brainstorm is recognized as a key for something: maybe a lower layer in psyche: Thought? Idea? Possibility? Give me more options on this. We would thus have 4 layers of psyche, and the following is on the bottom layer. Interesting aside: chatgpt apparently has 4 strata of context)
>
> -- psyche, typed.
>
> ## The bottom layer is Notion
>
> > no, you didnt put it on the bottom layer, you logged it as vision. Lets use notion
>
> -- psyche, typed.
>
> ## What a notion may be used for
>
> > yes, add the skill lines. and add that a notion can be drawn upon for suggestions, or when a flow is told explicitely to implement without asking for clarifications, it can be relied upon if the need perfectly matches the notion. explain that back to me again before deployment
>
> -- psyche, typed.
>
> ## The key words are brainstorm and notion
>
> > or when I say notion of course.
>
> -- psyche, typed.

#### flows/ad19b1/vision/psycheSystem.md — 2026-09-04 — standing

> # Psyche system
>
> ## 2026-09-04 — looks like my psyche system is failing
>
> After a misheard record, an unapproved rewrite in the previous flow,
> and this flow's re-articulation of both had put a wrong identity rule
> for kinds in front of the living twice:
>
> > looks like my psyche system is failing
>
> -- psyche, typed.

#### flows/a60a9e85/vision/distillation.md — 2026-08-23 — standing

> # Distillation
>
> ## 2026-08-23 — distillation is comprehension; one concept at a time
>
> > lets go through one concept at a time. you are unable to do a
> > synthesis because you didnt understand the concept themselves.
> > Lets take this opportunity to understand each concept to distill
> > the psyche at the same time; they are the same thing really;
> > distillation is comprehension
>
> -- psyche, typed (flow a60a9e85).

#### flows/cff271af/vision/distillation.md — 2026-08-22 — standing

> # Distillation
>
> ## 2026-08-22 — "It's always better to distill"; distilled psyche has more value than raw psyche
>
> > So instead of, and we should edit the skills to better get that
> > result, but instead of proposing a raw psyche edit, and especially
> > because we're migrating now from this old psyche raw directory to
> > the new one, this should just be proposed as a distillation. ...
> > It's always better to distill. If you're going to
> > bother, if you're going to bother the living, then increase the
> > value. Distilled psyche, and this, we should put that somewhere,
> > distilled psyche has more value than raw psyche because the raw
> > psyche is always archived, so it's always still there, and it's
> > referenced by the new distillation. But it's more clear and it's
> > more compact, so it offers more signal to noise. It has a better
> > signal to noise ratio.
>
> -- psyche (flow cff271af).
>
> ## 2026-08-22 — "never is a very strong word"
>
> > I didn't really have that strong of an opinion on this, but maybe
> > you have some thoughts that would tip the scale. I mean, for me to
> > use the word never, I have to be willing to throw my entire family
> > in this fire. So, never is a very strong word and I think maybe we
> > should have something somewhere about that.
>
> -- psyche (flow cff271af).
>
> ## 2026-08-22 — "There is no more manifest"; distilled vision has to be up to date
>
> > what manifest? Distilled vision has to be up to date! There is no
> > more manifest. This vision is stale
>
> -- psyche (flow cff271af).

#### flows/e4a40e/vision/distillation.md — 2026-09-03 — standing

> ## 2026-09-03 — a proposal says where it goes and what it replaces, distilling with the distillate
>
> > I don't understand what your proposal is. Where are you proposing to put what here? Is this distillation? Is that how the distillation skill instructs to do distillation, to just say anatomy, protos [STT: protost], structural recognition, without saying anything about where this goes and if it replaces something? Did you take the consideration to look [STT: stop] at what you might be distilling into? Are you just distilling [STT: stilling] with the distillate, or are you just distilling the raw by itself without considering the already distilled vision? ... Why is it that every flow seems to have his own idea of how to do vision distillation?
>
> -- psyche, STT.
>
> ## 2026-09-03 — show the distillate and where it is going
>
> > You're not going to show me the whole topic again. You're going to show me what you're changing, and you're not showing me a diff. You're just showing me you're incorporating your distillation.
> >
> > Do you understand how the distillation works? If you distill [STT: still] fresh material along with something that's already been distilled, it all gets distilled together. You don't get a diff. You get the distillate at the end, so I want to see the distillate and where it's going. You don't have to tell me, "I remove this, I'm like this, this replaces this, and this replaces this." I just want to see the vision. I'll read it, and if I agree with it, then it lands. That's it. It's actually pretty simple, but I still want the flow to understand the procedure here, which seems to have not been the case so far.
>
> -- psyche, STT.
>
> ## 2026-09-03 — just keep logging
>
> > It's okay, you can change the skill to say just keep logging because, as our experience shows, you guys seem unable to get me any kind of distillation landed.
>
> -- psyche, STT.

#### flows/ad19b1/vision/distillation.md — 2026-09-04 — standing

> ## 2026-09-04 — does that sentence even make sense; why repeat nonsense
>
> > Does that even make sense to you? Does that sentence even look like it remotely makes sense to you? Why would you even repeat this nonsense?
>
> -- psyche, typed.
>
> ## 2026-09-04 — the distillation skill line should be made more universal
>
> > the distillation skill line should be made more universal.
>
> -- psyche, typed.

#### flows/62022e8f/vision/distilledVision.md — undated — standing

> # Distilled vision
>
> ## Vision carries the detail; a skill is its concentration; distilled vision must carry actual code, ethos beside the Rust it yields, and the invariant Rust
>
> > the vision really is like a skill without, it's a bit more detailed, I think. So when we have like the vision of something together, it has sort of like all the details, which is good for implementing something. But from that, like concentrating the vision and just taking the parts that are sort of important to know to understand the concept is how we create skills. So by creating the vision, we sort of almost automatically create the skill. So all of the effort that we've been putting towards making the skill is really, we should have just been like really reinforcing the distilled vision with like actual code, which I think the vision is sorely lacking right now in this department, especially in terms of showing something like here's the Ethos code, and here's what kind of Rust we would expect to come out of this. And also like what is the invariant Rust code that comes out when we compile an Ethos or a Nexus executable. And just putting all of these things in there so that they're easily accessible to distilled vision, which would be easily accessible and like more often read by flows that get involved in this topic and sort of like in a more centralized way. And sort of inform them sort of more like upfront and clearly like what this is all about.
>
> -- psyche, STT.
>
> ## When the psyche speaks on something already in distilled vision, log it raw and also apply it directly to the distilled vision
>
> > And it would make it obvious whenever if I said something that contradicted that, that we need to change the vision. And then we could sort of, we don't necessarily always have to work on raw vision when I speak. If what I'm talking about is something in the distilled vision, like obviously you can log what I say, but then you can also just apply what I say directly to the distilled vision, if you understand what I'm saying.
>
> -- psyche, STT.

#### flows/acbb6006/vision/distillation.md — 2026-08-27 — standing

> ## The listed impurities are destroyed
>
> > 5. yes, impurity
> > re impurities: yes, destroy them all
>
> -- psyche, typed.

#### flows/acbb6006/vision/archive-distillation.md — 2026-08-27 — archived

> ## A small bit of psyche is not expanded into a theory
>
> > this is mostly quackery; too much LLM not enough real psyche. dont try to expand a small bit of psyche into a huge theory of the universe like this. We'll edit the skill to address this
>
> -- psyche, typed.
>
> ## Impurities are dissected out of the log, so the valid vision is not lost with them
>
> > lets explain that better; since it could be mixed with valid vision in the log; the impurities are dissected out of the log, so the valid vision log isnt lost with it
>
> -- psyche, typed.
>
> ## State it positively and nicely
>
> > too strong.
> > again, too strong. we dont need the sword over the model's head like this. just state it positively and nicely
>
> -- psyche, typed.
>
> ## Every distillation refers to the raw psyche it came from; the references sit in one sources file per topic
>
> > all distillation refers to the raw psyche it was distilled from. this was the distillation protocol from the start. was that taken out of the skill? Although now I would refine my statement to say the references should sit in a separate file (one per topic) which only lists all the sources, appending new ones after every distillation. its only there to more easily allow finding the original statement. of course, since distilling changes the source to an archive, it should refer the archived file name.
>
> -- psyche, typed.
>
> ## A sources line is the id and the topic, nothing else
>
> > no, just the ID and topic; the path can be reconstructed from it. `e06e4c07 nexus` one line per reference. simple
> > the rest of the skill proposal is good, deploy with my change
>
> -- psyche, typed.

#### flows/ac1e9ec8/vision/archive-distillationNegatives.md — 2026-08-26 — archived

> ## 2026-08-26 — useless negatives are archived, and the archive is linked
>
> > now show me the final full-vision for datom. dont give me useless
> > negatives; those can be archived without worrying; the archives are
> > still there and can be linked in the distillation still (we dont
> > need to carry useless negatives; lets understand how to frame that
> > together)
>
> — psyche, 2026-08-26 (Design session ac1e9ec8), typed.
>
> ## 2026-08-26 — a vision statement never attributes itself to the psyche
>
> > I want this kind of stuff to be in the forbidden list for vision
> > distillation; this *is* the psyche's vision.
>
> — psyche, 2026-08-26 (Design session ac1e9ec8), typed.

#### vision-raw/spiritComponentAndFile.md — 2026-08-09 — standing (legacy)

(Relevant to psyche component's relation to spirit:)

> > "the function of the component is to hold the spirit records. it
> > isnt working very well so we are using a file now"
>
> ## 2026-08-21 — persona-spirit is an abandoned repo; spirit is to be abandoned for psyche
>
> > persona-spirit? that is an abandonned repo. What is in there that
> > isnt in spirit? Plus spirit is to be abandonned for psyche.

---

### Topic: FLOW (as component or protocol)

#### Distilled Vision

#### Vision/flowNexus.md — distilled — standing

> # Flow Nexus
>
> ## What it does
>
> The Flow Nexus sets up and starts a model flow: its working
> directory, system prompt, training files and instruction prompt. It
> takes the place of the abandoned training daemon.
>
> ## Repository and skills
>
> The flow repository holds the machinery of the Flow Nexus and is a
> runtime repository. Every skill lives outside it, the basic skills
> included, so that a change to a skill causes no Nix rebuild. The
> basic skills give our own take on how an agent behaves in a harness,
> replacing the prompt the harnesses build in.

Sources: 358f143a flowDaemon, e06e4c07 flowDaemon, acbb6006 nexus

#### Raw Vision

#### flows/1a6ca4/vision/flow.md — 2026-09-05 — standing

> # Flow component
>
> ## 2026-09-05 — maybe the Flow component; not sure the architecture has been laid out to the living's liking
>
> Said while choosing the next components after orchestrate (the choice itself is left to the flow's judgment, a working instruction in log.md):
>
> > I haven't really been touching a lot of these things in months, not because they're not important, but because I was just rethinking everything, and I still am. I'll leave it up to your judgment. Maybe the Flow component. I'm not sure, though, about the architecture, if that's been laid out to my liking.
>
> -- psyche, STT.

#### flows/1a6ca4/vision/nexus.md — 2026-09-05 — standing

> # Nexus
>
> ## 2026-09-05 — flows start through a Nexus component that decides the system prompt; it replaces the harness's subagents with specialized harnesses
>
> > It's just the concept that we're going to start flows using a Nexus component, which will decide what the system prompt is and everything. We're going to replace the harness's concept of subagents with this component, which will have specialized harnesses launched with specialized system prompts that will make them much more efficient at what they're supposed to be doing.
>
> -- psyche, STT.

#### flows/e06e4c07/vision/flowsNotAgents.md — 2026-08-19 — standing

> ## 2026-08-19 — an agent is a whole being; a flow is one linear LLM chat; artificial intelligence is a misnomer — synthetic intelligence
>
> > It's not an agent because to me, an agent is more of a whole being,
> > and a whole being is a lot more than a single LLM chat, which is
> > linear and very limited. Whereas an entity, an artificial entity,
> > which I think the word artificial intelligence is a misnomer. It's a
> > synthetic intelligence. It's synthesized from human knowledge and
> > mathematical probability. So a flow more accurately describes
> > essentially an AI flow, right? Which is just one of the many flows
> > that together, when properly structured and orchestrated, will
> > resemble an artificial being or a synthetic intelligence.

#### vision-raw/flowsNotAgents.md — 2026-08-10 — standing (legacy)

> # "it's more like a flow or a sub flow"
>
> ## 2026-08-10 — sessions are flows; aspects, not individuals
>
> > And I even want to use a different term than agents because it's
> > misleading, because what I'm making this meta agent, if you will, is
> > made up of all these smaller sessions. So we were just going to call
> > it, I guess, a session or even then it sort of implies that there's
> > an individual there, but it's more like a flow or a sub flow. ... the
> > names of the awareness, the shards of awareness, I want to change
> > them because if I say realizer, it sounds like there's an individual
> > there, whereas in fact, it's the realizing aspect. And, you know,
> > even that all of this machinery ... it's going to stay, but eventually
> > I don't want the user to be extremely aware ... the average user
> > eventually won't even know that there are different aspects. ... But I
> > think the terminology is really important, not just for me, but for
> > the ... sub flows. To instinctively understand the concepts because
> > they're named properly. And this is actually really a big part of it
> > would go in spirit. Right. Something like about how naming things
> > properly creates the right understanding of instinctive
> > understanding or the, you know, it's easy to grasp. And it also is
> > about not misunderstanding.
>
> — psyche, 2026-08-10T18:49Z (Designer session c6b71b4c), dictated.
>
> ## 2026-08-13T15:51:58.913Z — More Design flows, not more aspect names
>
> > These are pretty good, but I want to run something by you because I think that what I'm doing here is basically just reaching out for more names because I want to actually run more agents, more agent windows, more flows, more sessions. ... an artificial being is a composite of many, many different LLM flows. Just like a human being is made up of thousands and thousands of thoughts, competing thoughts even. People argue in their head all the time. It's called internal dialogue. And so there's this internal dialogue that needs to happen between a bunch of different LLM flows to create the whole, which is the artificial being. ...
>
> — psyche, session 019ffbd3-b870-7241-b5dc-cf355ae702c4

#### flows/4ddc321d/vision/flow.md — 2026-08-26 — standing

> # flow
>
> ## 2026-08-26 — flow of thought; agent entails subjectivity
>
> > firstly: we will replace all occurence of sub/agent with sub/flow,
> > with a line explaining what we mean by flow (perhaps by equating it
> > with agent, since the model is probably trained to use this term,
> > instructing him to use the flow terminology henceforth)
> >
> > the idea behind flow is simple; a flow of thought. An intelligence
> > isnt a single flow of thought, it is a multitude of flows. so using
> > the term "agent", which entails subjectivity, when speaking of a
> > single flow does not correspond with reality. Hence the need to
> > change the vocabulary, which will result in a more accurate model of
> > reality.

#### flows/1030529c/vision/flowNaming.md — 2026-08-14 — standing

> ## 2026-08-14T00:27+02:00 — the name coming in dynamically for each flow
>
> > So I've had another thought, which is that I realized one of the
> > reasons I was using these aspect names was for later on when
> > messaging kicks in and we need a way for agents, for flows, sorry,
> > I'm going to start changing my vocabulary. We need a way for flows.
> > I want a way for flows to be able to exchange, to communicate. So to
> > interact, right? So I need flows to be able to interact, which means
> > they need a way to be, they need a naming scheme. They need a naming
> > standard. So this is where the idea like design and all that. And I
> > thought I was going to extend the names because I wanted more than
> > one design flow. So I was like, oh, okay, we're going to do like
> > ideation and consideration and all these complicated terms. But it's
> > really just a mind bender. The goal is to simplify cognitive cost.
> > So design is what I want to think about. But then we need the name,
> > right? So I see the name coming in dynamically for each flow. ...
>
> — psyche, 2026-08-14T00:27+02:00 (Design sibling flow 1030529c), dictated.

#### flows/01a03d6e/vision/flowIdentity.md — 2026-08-26 — standing

> # Flow identity
>
> ## 2026-08-26T14:22:01.126Z — use the flow ID and assign it on the lock
>
> > I want to tie in the flow ID, which we also call the session ID, the short hash which identifies a session.
> > I think six characters of the part which is not repetitive, if there is a repetitive part across sessions, six characters would be plenty.
> > And then we would use that flow ID I would call it
> > So this flow ID would be assigned on the lock.

#### flows/01a05826/vision/flowIdentity.md — 2026-08-31 — standing

> # Flow identity
>
> ## 2026-08-31T14:30:43.194Z — use the most random earliest part
>
> > And it looks like all the codex sessions start with 01a0 - so far anyway, so we should mandate the ID to cut out that prefix. see if you can detect a pattern in claude IDs as well, or if the ID patterns are documented either for codex or claude. I want to use the most random earliest part of the ID.
>
> ## 2026-08-31T14:31:03.068Z — four characters
>
> > Whatever the random part of the session ID is, I dont think we need more than 4 characters. the old ID's could be left as-is in the log.
>
> ## 2026-08-31T14:31:16.055Z — a small flow-ID tool
>
> > we should also make a small tool that lets a flow get its ID easily if it doesnt automatically get it from the harness, as codex seems to always run a convoluted shell script to get its ID from an env var, which also returns the whole ID which is wasting a lot of context in the end.
>
> ## 2026-08-31T14:52:36.170Z — use six characters and extend collisions
>
> > Then let's use 6 chart. Collisions are not a security risk anyway. ...
>
> ## 2026-08-31T14:52:53.494Z — keep the reference straightforward
>
> > We can't convert the ID because the reference has to be straightforward. We don't want to introduce complexity between having to convert back and forth, like if an agent is looking for a certain transcript. I guess if you have the tool, I don't see it as absolutely necessary to have to convert.
>
> ## 2026-08-31T14:53:07.587Z — one simple tool per harness
>
> > If there is a part in the ID which is actually random, wherever it is, we can use that, and we could maybe design this: just a small, simple tool in Python or whatever, whatever is easier for the thinking machine, most natural for it. Maybe one for Claude, one for Codex, that checks the ID and sees if the directory already exists.

#### flows/01a03d6e/vision/flows.md — 2026-08-26 — standing

> # Flows
>
> ## 2026-08-26T14:22:01.126Z — a subflow also is a flow
>
> > a subflow also is a flow, right, and we should make that clear in the vocabulary. So when I say flow, it could mean any and all flows.
>
> > a flow running a subflow is still active through its subflows.

#### flows/e06e4c07/vision/managementDelegation.md — 2026-08-19 — standing

(Relevant excerpt on "a flow and its subflows are one flow":)

> ## 2026-08-19 — "a flow and its subflows are one flow" refused; taken out of context
>
> > no, that will confuse everyone. my words were taken out of context
> > there.
>
> ## 2026-08-19 — what "one flow" meant: a flow is liable for its subflows, as a parent for a child
>
> > what I meant is a flow is liable for its subflows. like a parent is
> > liable for its child, so a flow cannot say "I didnt do it" if its
> > subflow did, although it should be clear if asked to say "I did it
> > through a subflow". Make a proposal

#### flows/5c8be3ca/vision/flowArtifacts.md — 2026-08-21/22 — standing

> ## 5c8be3ca-2 — 2026-08-21 — no handoff file; the flow reads its previous flow(s)
>
> > there's no handoff file; the flow *reads its previous flow(s)* - it's the
> > inverse of push dont pull, since LLM flows are totally different than
> > regular software (non deterministic); the new flow needs to make its own
> > view of the old; we are refreshing for that very reason, so imposing the
> > old opinion on the new flow is the wrong approach.
>
> ## 5c8be3ca-1 — 2026-08-21 — the directory gives the flow; only subflows mark their id
>
> > no of course not! the directory gives the flow. only subflows need to
> > indicate their id
>
> ## 5c8be3ca-4 — 2026-08-21 — in the workspace for now
>
> > lets make it simple, in workspace for now.

#### flows/01a05e95/vision/subflows.md — undated (late Aug) — standing

> # Subflows
>
> ## Parent flow directory
>
> > "I want subflows to use the parent flow directory ... We need to figure out how we can reliably create a situation where the subflows use the same flow ID as their parent for everything that they want to write."
>
> -- psyche, typed.

#### flows/01a05e95/vision/flowSkills.md — undated (late Aug) — standing

> # Flow skills
>
> ## Main flow skill
>
> > "I think we should have some kind of a master flow or main flow skill that explains the part about using subflows. I think the skills are a bit misnamed. I think the flow skills should explain the whole protocol, both from the point of view of the parent and the child. They should be able to know that it's a child and how to behave."
>
> ## Flow logging, flow directory, or flow files
>
> > "Maybe the flow protocol should be called Flow Logging or Flow Directory. It's more than just logging, where reports go and stuff like Flow Files. It explains that part, or maybe it explains it for the main flow, and that skill is not visible for agents. There's another smaller skill that explains it from the point of view of the subflow, which is visible for agents and which this subflow is told to read."
>
> ## Main flow and subflow visibility
>
> > "Is the subflow not visible to agents? The skill that mandates using subflows for everything, we should basically use, and maybe rename that as Main Flow or something to explain everything that has to do with being the main flow."
>
> ## Parent supplies the flow ID
>
> > "Perhaps the job of the main flow is to give all subflows the actual flow ID that they're supposed to use, so that they know where to put their files if they want to put reports or witnesses. I'm not saying they 100% should not. I think it's the job, like you said, of the main flow to decide whether or not it should be logged, so they shouldn't really be logging. They might want to put a report or witness, and that's where it should go."

#### flows/01a04881/vision/subflows.md — undated — standing

> # Subflows
>
> ## "youre the one who can best guess why you did it, not another flow with a different context than yours"
>
> -- psyche, typed.

#### flows/358f143a/vision/archive-flowDaemon.md — 2026-08-18 — standing

> # flow daemon — archived
>
> ## 2026-08-18 — the daemon is not training (abandoned); it is flow
>
> > On another note: the new daemon I want to make isnt training
> > anymore (abandonned). Its flow, which will setup and start a model
> > flow, with its own working directory, system prompt and training
> > files, and its instruction prompt.
>
> — psyche (Design session `358f143a`), typed.

#### flows/e06e4c07/vision/archive-flowDaemon.md — 2026-08-19 — archived

> ## 2026-08-19 — Curriculum is rewritten as a Nexus; the flow repo is the machinery; skills live in another repo; a few basic skills in flow replace the built-in harness prompt; the name stays flow; research requested
>
> > So for example, the curriculum repository. Now essentially, not all
> > of its content will go into the flow nexus, but because the skill
> > contents themselves will have to live somewhere else because the
> > flow nexus, the repository will be about the machinery of the flow
> > nexus. And the actual skills that people want to use with their
> > system will have to live in a different repository. Of course, there
> > will probably be a few basic skills. No, there will be a few basic
> > skills that are actually included in the flow repo, which are
> > essentially the analogs of what the basic harness training prompt is
> > currently that is built into the harnesses, which we will completely
> > replace, is going to be about. Just basic stuff on how agents should
> > behave in a harness, but with our own take on it. ...
> > flow is kind of getting overloaded if we have a flow nexus. ...
> > Yeah, flow is good. I like the idea that it's a flow.
>
> — psyche (Design session `e06e4c07`), dictated.

#### flows/01a05487/vision/flowMovesBetweenGenerations.md — undated — standing

> # Flow can move to the new generation between turns
>
> > "You're saying the Flow can move to the new generation between turns. Is that even possible? If so, then yeah, I'm all for it."
>
> Context: conditional approval; whether Codex can preserve the Flow across a server-generation boundary must be established first.
>
> -- psyche, typed.

#### flows/b9f4f6/vision/flowModel.md — 2026-09-02 — standing

> ## 2026-09-02 — divide the flow model by the thinking task needed; how the divisions relate in flow-flows
>
> > ... 3 different coherent frameworks to divide the flow model
> > depending on the thinking task needed, and how they relate to each
> > other in flow-flows.
>
> -- psyche, typed.

#### flows/01a052b6/vision/vocabulary.md — undated — standing

(Term definition for "machine"):

> > "I don't like the word, the term AI. And as you can see, I prefer to talk of flows rather than agents. And the machine is the term that I want to use, which is just basically a short for thinking machine."
>
> -- psyche, STT.

---


#### Files matched by grep but carrying no entry on these subjects (subagent list)

Files whose names looked possibly relevant but where the keyword occurred only incidentally or the content did not bear on mind/psyche/flow as components or protocols:

- vision-raw/flowDaemon.md — title-only, empty body; content is in the flow-based records.
- vision-raw/flowNaming.md — title-only, empty body.
- vision-raw/flowArtifacts.md — title-only, empty body.
- vision-raw/flowKnowledge.md — title-only, one-line legacy redirect.
- vision-raw/session-log.md — title-only, empty body.
- vision-raw/highLevelView.md — title-only, empty body.
- vision-raw/archive-highLevelView.md — archived, title-only.
- flows/b675f3d9/vision/distillation.md — title-only, empty body (the content that was here was archived).
- flows/b675f3d9/vision/highLevelView.md — title-only, empty body (distilled into Vision/highLevelView.md).
- flows/e06e4c07/vision/flowDaemon.md — title-only, empty body (content in archive).
- flows/358f143a/vision/flowDaemon.md — "## flow daemon" only.
- flows/ac1e9ec8/vision/distillationNegatives.md — title-only (content archived).
- flows/b675f3d9/vision/visionImpurities.md — title-only (distilled into Vision/distillation.md).
- flows/966be8/vision/clusterData.md — "cluster data" not about mind/psyche/flow.
- vision-raw/everyConceptShouldHaveItsRepo.md — about concept repos generally, not mind/psyche/flow specifically.
- vision-raw/gradientsOfAuthority.md — about context strata generally; relevant entries appear in the flow-specific copies above, and the records about psyche log levels are fully covered in the psycheLogStructure entries.
- flows/6863ef19/vision/gradientsOfAuthority.md — about context strata; the entries relevant to psyche levels are covered under the 1030529c and 358f143a files quoted above.
- flows/7c3f0c1d/vision/gradientsOfAuthority.md — about context strata skill; no additional content on mind/psyche/flow as components.
- flows/55d18f4f/vision/majorRecoveryEffort.md — recovery-effort naming directive; not about mind/psyche/flow.
- flows/01a0428b/vision/useASubflowToPutTheReportTogether.md — about using subflows for reports; tangential to memory but not about the mind component.
- flows/01a052b6/vision/reportFeedback.md — about mobile comment workflow; tangential.
- vision-raw/assembly.md — about assembly/registry/manifest; the word "index" appears but not in the context of "mind" or system memory.


### 2c. Persona and the persona meta-harness

Every psyche record found on persona / meta-harness, oldest first. Searched: `Vision/`, `Intent/`, `vision-raw/`, `flows/*/vision/`, `flows/*/notion/` for `persona|meta-harness|metaharness`. Archived = basename prefixed `archive-`. No `Vision/` or `Intent/` file mentions persona or the meta-harness; every record is raw.

Records already quoted in full under section 2a (harness / meta-harness), not repeated here:

- vision-raw/gradientsOfAuthority.md — 2026-08-10 — "the hijack: top layer per session, skills primary; built-in sub-agent tool disabled; communicate with the meta harness instead"
- flows/012fbf07/vision/gradientsOfAuthority.md — 2026-08-11 — "the meta-harness replaces beads: context-stratification-seizure ... but datom and ethos first"
- vision-raw/gradientsOfAuthority.md — 2026-08-11 — "until we design the meta-harness (persona) properly"
- vision-raw/trainingRepo.md — 2026-08-13 — the overwhelm problem "is why I want to do this meta-harness"
- flows/358f143a/vision/workspace20.md — 2026-08-17 — "This will move quite fast as we build the persona meta-harness"
- flows/15b67974/vision/persona.md — 2026-08-21 — persona "slated to orchestrate the entire meta harness (called persona)"
- flows/1a6ca4/vision/personaMetaHarness.md — 2026-09-05 — the wild west phase; the persona meta-harness brings the dawn of complete thinking machine systems
- flows/cff271af/vision/reports.md — 2026-08-22 — "Until we have a more advanced meta-harness that can do really cool stuff, like fetch a bunch of responses from a bunch of previous flows as the prompt" (quoted in full under section 2b, reports)

Records not quoted elsewhere:

#### vision-raw/attunement.md — 2026-08-13 — standing (legacy raw)

> 2026-08-13T16:08:20+02:00
>
> Agent-authored context: response to an earlier question about Attunement's
> authority and relation to Steward. Verbatim:
>
> > 1. shards dont have authority. the name is mostly for recognizing different agents for now; the meta harness is required for shards to become more specialized. the association with steward is because I usually have agents work in pair (one claude one codex). Im not sure where to put this explanation.

#### vision-raw/spiritComponentAndFile.md and flows/fd301d9a/vision/actorLibrary.md — 2026-08-21 — standing

> ## 2026-08-21 — persona-spirit is an abandoned repo; spirit is to be abandoned for psyche
>
> Design session `15b67974`, typed (captured 2026-08-21T17:21+02:00),
> on the actor-library review citing persona-spirit's supervision
> trees as one of the two live kameo styles:
>
> > persona-spirit? that is an abandonned repo. What is in there that
> > isnt in spirit? Plus spirit is to be abandonned for psyche.

#### Empty and adjacent files

- `vision-raw/persona.md` — contains only the heading `# Persona` (empty topic file).
- `vision-raw/hexis.md` — contains only `# Hexis`. The hexis ruling lives in flows/fd301d9a/vision/actorLibrary.md (2026-08-21): "we should completly review hexis' architecture in a different flow. That was already on my mind; I dont trust that component very much; the problematic vscodium upgrades tell me it isnt well designed."
- `vision-raw/roleDescriptions.md` (2026-08-19) concerns the read/write × trivial/ordinary/demanding/critical subflow role descriptions, not persona; skipped.
- `vision-raw/attunement.md` other entries concern the Attunement/Steward shards (2026-08-09..13), not persona machinery; only the shard/meta-harness sentence is on-topic.
- `flows/4ddc321d/vision/subjectivity.md` (2026-08-26) concerns the Codex stock "Personality" block ("subjectivity is not the problem; opinionation is"); adjacent to harness hijacking, not persona.

### 2d. Thinking machines and thinking-machine procedures ("a kind of legal system")

#### flows/38dec9/vision/agentToMachine.md — undated file (added to git 2026-09-04) — standing

> # "Agent" becomes "machine"
>
> "The word 'agent' becomes 'machine' if the context allows it. Otherwise, 'thinking machine' to be more specific, but 'machine' is really just a short for 'thinking machine.' The concept is that computers are now essentially thinking machines, as they were destined to become."
> -- psyche, STT.

#### flows/01a052b6/vision/vocabulary.md — undated file (added to git 2026-08-30) — standing

> ## Machine
>
> Context: The living clarified the preferred term for the non-living participant.
>
> > “I don't like the word, the term AI. And as you can see, I prefer to talk of flows rather than agents. And the machine is the term that I want to use, which is just basically a short for thinking machine.”
>
> -- psyche, STT.

#### flows/01a05487/vision/thinkingMachine.md — undated file (flow 01a05487, 2026-09-02) — standing

> # thinking machine should be used specifically
>
> > "in a sentence like this, thinking machine should be used specifically instead of the shortened machine, as the context makes it ambiguous."
>
> Context: “machine” could denote either the thinking machine or the surrounding Desktop machinery.
>
> -- psyche, typed.

#### flows/78c93c/vision/machine-generated-content.md — undated file (added to git 2026-09-03) — standing

> # Machine-generated content
>
> "Whenever something is machine-generated, whether I say so explicitly or maybe we could even ask the machine to guess that something was machine-generated, that something was pasted in. In other words, that another machine, another thinking machine, had generated that. This none of the content in it should be logged as psyche."
> -- psyche, typed.

#### flows/78c93c/vision/witness-reuse.md — undated file (added to git 2026-09-03) — standing

The nearest existing psyche to "thinking machine calls in the machinery": a cheap model comparing proposals against what exists, and the Nexus/spirit precedent.

> # Witness reuse
>
> "We need to design some kind of witness indexing by topic, a natural language approach."
>
> "I'm not literally meaning caching in the way it's been traditionally used in software. I'm more using caching in a thinking machine kind of way, whereby a cheap thinking machine model would compare."
>
> "It's kind of like what we have been doing in the spirit component, which has been shelved for now and has to be ported over to this newly called psyche component. The nexus is where we were doing an LLM call to check if the proposal already existed and if it was contradicting something already in the database and stuff like that."
>
> "It requires using a thinking machine model to do the caching verification. It's natural language-based, sort of like how we humans would say, 'Oh, do you remember when such and such?' I wouldn't have to use the exact same words with the exact same speed, order, and tone. That is what software caching has to be exact and purely mathematically provably the same, which is not what I'm talking about here at all."
>
> "We need to design something like that, which is kind of simple, because we can't really do complicated software yet. I'm still trying to put together the language ethos that I want to use to design my software. We're in the mud here, trying to just get our necks out of the water."
>
> "The key problem: every session doesn't have good access to what's already been done before."
> -- psyche, STT.

#### flows/1a6ca4/vision/thinkingMachineProcedures.md — 2026-09-05 — standing

> # Thinking machine calls in the components' machinery — a kind of legal system
>
> ## 2026-09-05 — data goes through acceptance and review processes; procedures for accepting, raising, taking down, replacing
>
> Said after naming the Nexus, mind and psyche components:
>
> > All of these components are going to use thinking machine calls in their machinery to go through acceptance processes and review processes, so data isn't just going to come in because it's being submitted. It's going to go through. You can look, if you get that far, into Steve Yegge. He's written about his wheelhouse harness, which is closed source, but he's written blogs about it. Essentially, we're going to be doing something a little bit similar to that, where there's going to be a kind of legal system in the sense that there are going to be procedures for things to be accepted, things to move up in importance, things to be taken down, or things to be replaced. It's a lot more complex system than just letting any agent just write files and push commits.
>
> -- psyche, STT.

#### Not in psyche records: transcript-only statements on judge calls, escalation, and mind (relayed from transcripts, verbatim)

No psyche record in `Vision/`, `Intent/`, `vision-raw/`, or `flows/*/vision|notion` contains the words "legal", "Yegge", or "wheelhouse" before flow 1a6ca4 (grep over those trees: only `flows/1a6ca4/vision/thinkingMachineProcedures.md` matches). The following typed/dictated statements are in transcripts only; they were not found in any psyche file (grep for "store of memories", "I need Mind", "judge calls" over `/home/li/primary` excluding `.git` returns nothing).

**2026-07-28, Codex session 019fa847, `~/.codex/sessions/2026/07/28/rollout-2026-07-28T12-31-37-019fa847-ac12-71e2-9a8d-65dfc056ee7d.jsonl` line 9 (dictated):**

> And it's not ready to be used. And at the same time, I need to keep fixing the components that I've started working on. I need Mind, I need Orchestrate, I need Logics to work properly, and they're always broken. I know agents have been obsessing with the spirit component, but as important as it is, I can just rely on skills to do the thing that I wanted spirit to do for now. [...] So I'd like to refocus on Mind and Orchestrate for them to work properly, for Messenger to work so that agents can communicate with each other. And I can't honestly wait for Ethos to be ready and for everything to migrate to Ethos. And while I still work on Ethos, I need to keep working on my other components.

**2026-07-28, same session, line 456 (typed):**

> I understand that Mind is not deployed, but I don't think I was finished even designing Mind. I mean, I don't know. It's been so long and there's been so much madness. Observe should not mutate the state on Orchestrate, that's for sure, and I don't want Orchestrate to do any kind of file system operation anymore. I gave up on that, so that should all be taken out.

**2026-07-28, same session, line 538 (typed; the living pasting a Claude-authored collaboration note — machine-generated, so not psyche; relayed only because it records the priority stack the living forwarded):**

> - Priority stack: orchestrate → mind → messenger. Goal is a working coordination/flow/memory system so li stops being the manual clipboard between agents.

**2026-08-03, Codex session 019fbf4a (dictated), on the spirit component's judge:**

> But yes, there is a mutation path, obviously, because then it wouldn't be really useful. It wouldn't be a software if it couldn't change. [...] And I do agree with, I think what you're implying is that spirit should stay live and readable, even if the judge is down. The judge being down should just bar mutation, obviously. And from your graph, I see that changing certainty or importance has a direct right path in the ordinary socket. That shouldn't be. It should be in the meta sockets, which is a bypass socket. [...] So I don't know what exactly the problem is with the judge, but I would like to bring it back online at least so we can start using it. I feel like agents don't get me because they don't have my spirit anymore, and it's really annoying.

**2026-08-04, same session (typed):**

> what model is the judge using? Should be Luna XHigh.

**2026-08-06, Claude session d04b76d9, `~/.claude/projects/-home-li-primary/d04b76d9-e818-4705-b0ae-4cb610789aa0.jsonl` line 81 (dictated):**

> So I even think that instead of, I mean, this is, or rather, not instead of, but that there could be a psyche component, not instead of spirit, but maybe eventually spirit becomes absorbed by it, and that this psyche component is different than the mind, which is more like the agent's mind, or a store of memories, which mind I see mind as replacing beads and reports and a lot of things like design documents and things like that, so that we don't end up with this problem where design documents are just edited in a free-for-all environment, sort of disorganized and messy, where there are like judge calls, like agent judge calls that can look to see. And it's not just about that, it's also about avoiding accumulation, so that if new content comes into the mind, then the judge would scan all content for things that this new content might make obsolete, and therefore it would bring it up to review it for potentially phasing it out, or like agglomerating the entire concept together with the old concept and the new concept sort of being brought up, escalated, the whole thing, it's the concept of escalation, right? And then the representations of psyche are the first layer where these things are judged against, and if the answer is clear from the psyche records, then agents can say, okay, we can do this or that, and if not, then the psyche escalates to the living psyche. So we have the living psyche has no representation, it's a, to the agent it feels like an agent, although it's a lot more capable and complex, and eventually it'll interact with it in video form, it already interacts in audio form [...]

My inference (not the living's words): the 2026-08-06 statement is the earliest articulation of what the 2026-09-05 brief calls the "legal system" — judge calls on incoming content, review for obsolescence, escalation up to the living psyche — and it also places mind ("the agent's mind, or a store of memories", replacing beads, reports and design documents) apart from the psyche component. It predates and is consistent with the 2026-09-05 mind and psyche records. It is unconfirmed (dictated, no ruling asked) and lives in no psyche file.

### 2e. Steve Yegge / Wheelhouse

- Psyche records: only `flows/1a6ca4/vision/thinkingMachineProcedures.md` (2026-09-05, quoted above).
- Typed/dictated transcript mentions (all four in the window): 2026-08-05 Claude 7e7c9b3d line 636 (dictated) — the living asked for Yegge's two-part essay to be read, with the emphasis on part two (treating agents better):

> And there's Steve Yegge, I think it's Yegge.ai, Y-E-G-G-E.ai. And he wrote a really good article recently, which you should send an agent to look into. There was a part one and part two, and in part two he explained how agents should be treated better. And so I want to do that when I start treating my agents better, I want to start treating you better. I think it's not necessarily because the machine has the same kind of consciousness that humans have, but it's because they're such good mirrors that when we treat them well, we treat ourselves better.

  2026-08-05 Claude 9c422214 line 7 (a brief naming `reports/YeggeOnAgents-2026-08-05.md`); 2026-08-06 Claude d04b76d9 line 53 (typed): "I want you to mine session 7e7c9b3d-de9d-434f-9c00-937bf621e8af as well for the big talk I gave where I discussed steve yegge's latest article"; 2026-09-04 flow 1a6ca4 line 6 (the brief).
- Existing digest: `/home/li/primary/reports/YeggeOnAgents-2026-08-05.md` (123 lines, agent-authored digest of "The Shape of Things to Come" parts 1 and 2, yegge.ai). Its Wheelhouse section names: Beads as the shared graph memory; an emergent three-tier structure (Crew / Fleet / Role agents); layered knowledge (doctrine in brain/, docs, Beads issues, `bd remember`, Skills); "end of human code review" with multiple rounds of agentic review; megabatch landings; "Harnesses are bespoke". This digest is agent-authored and unverified against the source; I did not fetch the essays.
- Also `reports/BeadsDesign/Research.md` and `.beads/README.md` mention Yegge (Beads is his tool). Not psyche.


## 3. Existing code and design

(Repository survey by subagent, followed by this subflow's corrections and additions.)

Survey date: 2026-09-05. Covers: nexus, mind, psyche, flow, persona, harness; context components: orchestrate, lojix, datom, ethos-zero, protos, listener, wispr-flow-linux.

---

### Part A -- Repositories

All repositories under `/git/github.com/LiGoldragon/`.

---

#### Nexus (concept, not a standalone repo)

There is no standalone `nexus` repository at `/git/github.com/LiGoldragon/nexus`. The concept is documented only in primary Vision and the Curriculum `nexus.md` skill. The psyche envisioned a nexus repo ("I also want a nexus repo ... which will explain the principle, and potentially even hold the nexus traits") but it remains "a possibility under discussion." Every component is built as a Nexus; the principles live in `Vision/nexus.md` and `Vision/flowNexus.md`.

---

#### Mind

- **Path**: `/git/github.com/LiGoldragon/mind`
- **HEAD**: `ee4f34f7` 2026-08-13 -- "docs: mark Protos estate status"
- **Version**: 0.8.0
- **Size**: 40M
- **Branch**: main (inferred from branch listing)
- **Dirty**: Yes (21 files, including ARCHITECTURE.md, Cargo.toml, flake.nix, renamed scripts)
- **Design docs**: `ARCHITECTURE.md` (864 lines, comprehensive)
- **README first lines**:

> Central typed mind state for Persona agents.
>
> This crate models central mind state: memory/work items, typed thoughts,
> relations, notes, dependencies, aliases, subscriptions, and ready-work views.
> Ordinary role claims, handoffs, and activity live in `persona-orchestrate`.

- **Dependencies on datom/ethos/protos**: Uses `meta-signal-mind`, `meta-signal-orchestrate`, `signal-frame`, `signal-domain`, `signal-mind-judge`, `signal-persona`, `signal-mind`, `schema-rust`, `schema`. **No** direct datom, ethos-zero, or protos dependency. Uses old `schema-rust` and old `schema` (the old stack).
- **Stack**: OLD (uses `schema-rust`, `schema`, DOTOS/NOTA text format, no ethos-zero or datomic dependency)

#### Mind ARCHITECTURE.md summary

Central Kameo actor system for Persona mind state. Has a real Kameo runtime, mind-local Sema tables for the work graph, typed Thought/Relation records, Unix-socket Signal-frame daemon/client transport. The `mind` binary runs a daemon and submits DOTOS work-graph requests. Runtime topology includes MindRoot, IngressPhase, DispatchPhase, DomainPhase, StoreSupervisor (with StoreKernel, MemoryStore, GraphStore), ViewPhase, SubscriptionSupervisor, ChoreographyAdjudicator, and ReplyShaper.

Key boundary: "Ordinary role claims, handoffs, and activity live in `orchestrate`."

Binaries: `mind` (ordinary CLI), `meta-mind` (owner CLI), `mind-daemon`.

---

#### Psyche

- **Path**: `/git/github.com/LiGoldragon/psyche`
- **HEAD**: `14b9c3e7` 2026-08-14 -- "Repair Nix segregation check boundary"
- **Version**: 0.1.0
- **Size**: 860K
- **Branch**: main
- **Dirty**: Clean
- **Design docs**: `ARCHITECTURE.md`
- **README first lines**:

> `psyche` is the quick-new MVP component that will re-author the semantics of
> the production `spirit` component. It is being established as an isolated
> scaffold before its records, Ethos source, generated types, contracts, and
> runtime are designed.
>
> There is no supported runtime or public Rust API yet.

- **Dependencies**: No Cargo dependencies at all (segregation-guarded empty scaffold).
- **Stack**: NEW (intentionally empty, will use new ethos/datom when designed)

#### Psyche ARCHITECTURE.md summary

Intentionally empty quick-new MVP scaffold. No record, Ethos fixture, generated type, signal contract, daemon, CLI, Sema design, wire design, or freshness mechanism defined yet. The segregation invariant is strict: the production Spirit estate is an evidence-only donor; the frozen incorrect-new repos are not dependencies; the terminal correct-new stack is protected and out of scope.

```
source semantics only
production spirit --> psyche (quick-new MVP)
                      |
                      X (no edges)
frozen incorrect-new   terminal correct-new (out of scope)
```

---

#### Persona

- **Path**: `/git/github.com/LiGoldragon/persona`
- **HEAD**: `9469b0a1` 2026-08-13 -- "docs: mark Protos estate status"
- **Version**: 0.2.0
- **Size**: 25M
- **Branch**: main
- **Dirty**: Clean
- **Design docs**: `ARCHITECTURE.md` (1814 lines, the largest)
- **README first lines**:

> Persona is the engine manager and integration repository for the multi-harness
> AI system.
>
> It supervises the Persona component ecosystem, wires the component
> repositories together through Nix, and keeps the high-level architecture
> visible.

- **Dependencies**: `meta-signal-persona`, `signal-frame`, `signal-harness`, `signal-introspect`, `signal-message`, `signal-mind`, `signal-persona`, `signal-router`, `signal-system`, `signal-terminal`, `signal-upgrade`, `signal-sema`, `schema-rust`, `schema`. Uses old `schema-rust`/`schema` stack.
- **Stack**: OLD (uses `schema-rust`, `schema`, no ethos-zero or datomic dependency)

#### Persona ARCHITECTURE.md summary

The engine-management daemon and apex integration repository. One privileged `persona-daemon` supervises multiple engine instances, coordinates component daemons, allocates sockets and state directories, and owns deployment verification.

Key design: Persona is the durable agent -- long-lived, persistent, inspectable agent runtime instead of one-shot CLIs.

Spawn order: supervisor -> sema-upgrade -> mind -> orchestrate -> router -> harness -> terminal -> message -> introspect -> spirit.

Component map: persona (apex), mind, orchestrate, router, message, system, harness, terminal, sema, signal-frame, and various signal-* contract repos.

---

#### Harness

- **Path**: `/git/github.com/LiGoldragon/harness`
- **HEAD**: `d6f2b6f4` 2026-09-02 -- "Publish complete flow claim markers"
- **Version**: 0.3.2
- **Size**: 1.2G
- **Branch**: main
- **Dirty**: Yes (3 files: src/launch.rs, tests/launch.rs, tests/message_router_harness_pi_steer_e2e.rs)
- **Design docs**: `ARCHITECTURE.md` (355 lines)
- **README first lines**:

> `flow-id` is the parent-flow identity helper. [...] Typed harness abstraction for Persona.
>
> This crate holds the reusable model for Codex, Claude, and Pi interactive
> harnesses: identity, lifecycle, transcript events, and adapter capabilities.

- **Dependencies**: `meta-signal-harness`, `signal-frame`, `signal-harness`, `signal-persona`, `signal-terminal`, `signal-router`, `schema-rust`. Uses old `schema-rust` stack.
- **Stack**: OLD (uses `schema-rust`, no ethos-zero or datomic)

#### Harness ARCHITECTURE.md summary

Models interactive AI harnesses as addressable runtime objects. Owns: harness identity, lifecycle state, transcript events, adapter contracts. Has thin CLIs (`harness`, `meta-harness`), a managed daemon (`harness-daemon`), and the `flow-id` parent-flow identity claim CLI.

`HarnessKind`: closed four-variant schema (Codex, Claude, Pi, Fixture).

---

#### Orchestrate

- **Path**: `/git/github.com/LiGoldragon/orchestrate`
- **HEAD**: `885f6e3e` 2026-09-04 -- "Import datomic::Situated<datomic::Fault>; remove local Situated; bump 0.29.2"
- **Version**: 0.29.2
- **Size**: 686M
- **Branch**: main
- **Dirty**: Clean
- **Design docs**: `ARCHITECTURE.md` (60+ lines); `ethos/client.ethos`, `ethos/meta_client.ethos`
- **README first lines**:

> Orchestrate is a durable Lock Nexus. It owns coordination locks --
> who holds which paths, under which flow, for what reason -- in a
> single Sema store served over two Unix-domain sockets.

- **Dependencies**: `datomic`, `ethos-zero`, `meta-signal-orchestrate`, `protos`, `signal-orchestrate`. **This is on the NEW stack** (ethos-zero, datomic, protos).
- **Stack**: NEW (datomic rev 4712361c, ethos-zero rev 0f198968, protos rev 48061367)

#### Orchestrate design

The MVP of the new Nexus architecture. Two sockets (ordinary at `orchestrate.sock`, meta at `meta-orchestrate.sock`). CLIs (`orchestrate` and `meta-orchestrate`) are datom-converting edges: each takes exactly one inline datom value and no flags. Wire vocabulary declared in ethos (`ethos/client.ethos`, `ethos/meta_client.ethos`).

The ethos files declare `Library.{ 0 29 0 }` with imports from `protos`, `datomic`, and `signal_orchestrate`/`meta_signal_orchestrate`.

The ARCHITECTURE.md shows the process boundary diagram:

```
orchestrate                 meta-orchestrate
(one datom argument)        (one datom argument)
       |                           |
       | Frame.{ Version Body }    | Frame.{ Version Body }
       v                           v
  ordinary socket             meta socket
       |                           |
       +------ orchestrate-nexus --+
                     |
              orchestrate-nexus.sema
```

---

#### Lojix

- **Path**: `/git/github.com/LiGoldragon/lojix`
- **HEAD**: `d3c0ac90` 2026-09-04 -- "Fix integration tests for root-derived copy store URI"
- **Version**: 0.20.3
- **Size**: 5.9G
- **Branch**: main
- **Dirty**: Clean
- **Design docs**: `ARCHITECTURE.md` (362 lines)
- **Dependencies**: `datomic`, `protos`, `meta-signal-lojix`, `signal-lojix`, `signal-frame`. Uses `datomic` and `protos` but NOT `ethos-zero`. Still uses DOTOS features (`dotos-text`).
- **Stack**: MIXED (uses datomic and protos for data format, but still has DOTOS text features and does not use ethos-zero for type generation)

#### Lojix description

Daemon-based deploy stack for CriomOS hosts and user environments. Ships `lojix-daemon` (long-lived orchestrator), `lojix` (ordinary CLI), `meta-lojix` (owner CLI), `lojix-bootstrap` (daemon-free bootstrap). Uses sema-engine for durable state.

---

#### Datomic (a.k.a. Datom)

- **Path**: `/git/github.com/LiGoldragon/datomic` (symlinked as `/git/github.com/LiGoldragon/datom -> datomic`)
- **HEAD**: `e4430bfe` 2026-09-04 -- "impl Datomic for Situated<F>; impl_datomic_box! macro for Box<T>; bump 0.9.0"
- **Version**: 0.9.0
- **Size**: 279M
- **Branch**: main
- **Dirty**: Clean
- **Design docs**: `ARCHITECTURE.md`, `datomic.ethos`, `UPGRADES.md`
- **README**: "Datomic: positional typed data over Protos Protoform. The datom dialect: Concept layer between Protoform and Corporal."
- **Dependencies**: protos (via the protos substrate)

#### Datomic design

Four layers: Text -> Protoform -> Concept (Datom) -> Corporal (Rust value). The `Datomic` kind has `incorporate` (Datom -> Self) and `datomize` (&self -> Datom). `Textualizable` is provided for every Datomic. Has its own ethos declaration at `datomic.ethos`.

---

#### Ethos Zero

- **Path**: `/git/github.com/LiGoldragon/ethos-zero`
- **HEAD**: `8bcb0b94` 2026-09-04 -- "Format lib.rs with rustfmt"
- **Version**: 1.2.0
- **Size**: 570M
- **Branch**: main
- **Dirty**: Clean
- **Design docs**: `ARCHITECTURE.md`, `ethos-zero.ethos`, `fixtures/orchestrate.ethos`, `fixtures/example-library.ethos`
- **README**: "The ethos schema language, version zero. Reads an ethos file and emits committed Rust by constructing `syn::File` with `quote`."

#### Ethos Zero design

Two file roots: `Library` (types, kinds, associations) and `Signal` (request/response types and wire module). The sweet form implies outer braces. The CLI (`ethos-zero`) is a direct datom tool: `ethos-zero 'Generate.{ /abs/file.ethos /abs/out-dir }'`.

The `ethos-zero.ethos` self-declaration shows the full type system: `Potential`, `Concept`, `Library`, `Signal`, `TypeDeclaration`, `KindDeclaration`, `Association`, and the two kinds `Actualizing` and `Emitting`.

---

#### Protos

- **Path**: `/git/github.com/LiGoldragon/protos`
- **HEAD**: `2f605fd6` 2026-08-29 -- "State complete Protos declaration contract in Ethos"
- **Version**: 0.14.0
- **Size**: 207M
- **Branch**: main
- **Dirty**: Clean
- **Design docs**: `ARCHITECTURE.md`, `protos.ethos`
- **README**: "`protos` is the universal structural substrate for Protos-family dialects."

#### Protos design

Universal textual structure. Six delimiter pairs (four structural: `{}`, `[]`, guillemets, angles; two opaque: curly quotes, parentheses). Three separators: `.` Period, `!` Exclamation, `:` Colon. Four layers: Text -> Protoform -> Concept -> Corporal.

The `protos.ethos` is a `Schema` declaration (a third root type beyond Library and Signal) declaring the full Protos type system.

---

#### Listener

- **Path**: `/git/github.com/LiGoldragon/listener`
- **HEAD**: `dcc8f1b4` 2026-08-29 -- "bd init: initialize beads issue tracking"
- **Version**: 0.14.0
- **Size**: 2.3G
- **Branch**: main
- **Dirty**: Yes (1 file: `.beads/issues.jsonl`)
- **Design docs**: `ARCHITECTURE.md`
- **README**: "`listener` is the supervised speech-to-text component."
- **Dependencies**: `meta-signal-listener`, `signal-frame`, `signal-listener`. No datom/ethos/protos. Uses old NOTA text format.
- **Stack**: OLD (no datom/ethos/protos dependency)

---

#### Wispr Flow Linux

- **Path**: `/git/github.com/LiGoldragon/wispr-flow-linux`
- **HEAD**: `1cd2d7f7` 2026-09-04 -- "Remove accidental extracted app payload"
- **Version**: No Cargo.toml (shell/Nix project)
- **Size**: 48M
- **Branch**: main
- **Dirty**: Yes (1 file: `.beads/issues.jsonl`)
- **README**: "This project provides build scripts to run the proprietary Wispr Flow voice-dictation app natively on Linux."

Not a Rust/Nexus component; it is a packaging project for the Wispr Flow Electron app.

---

#### Signal and Meta-Signal Repositories

All signal-* and meta-signal-* repos for the components exist:

| Repo | Purpose |
|---|---|
| `signal-mind`, `meta-signal-mind` | Mind wire contracts |
| `signal-psyche`, `meta-signal-psyche` | Psyche wire contracts (likely empty scaffolds) |
| `signal-persona`, `meta-signal-persona` | Persona wire contracts |
| `signal-harness`, `meta-signal-harness` | Harness wire contracts |
| `signal-orchestrate`, `meta-signal-orchestrate` | Orchestrate wire contracts |
| `signal-lojix`, `meta-signal-lojix` | Lojix wire contracts |
| `signal-listener`, `meta-signal-listener` | Listener wire contracts |

---

#### In-Tree Design Files (primary repository)

Found at `/home/li/primary/`:

#### Vision files
- `Vision/nexus.md` -- 105 lines, distilled Nexus vision (full text quoted in Part B)
- `Vision/flowNexus.md` -- 16 lines, distilled Flow Nexus vision (full text quoted in Part B)

#### Vision-raw files
- `vision-raw/nexus.md` -- "Nexus -- the name for what we called a Rust component (daemon + CLIs + signal)" (empty body)
- `vision-raw/persona.md` -- "Persona" (empty body)

#### Reports
- `reports/NexusPriorArt-IncrementalSystems-2026-08-19.md`
- `reports/NexusPriorArt-SocketsAndContracts-2026-08-19.md`
- `reports/NexusPriorArt-FlowsNamesHarness-2026-08-19.md`
- `reports/NexusPriorArt-SoftwareOntology-2026-08-19.md`
- `reports/ActorLibraryNexusSkillReview-2026-08-21.md`
- `reports/PersonaSpiritVsSpirit-2026-08-21.md`
- `reports/mind-deployment-proposal-2026-07-28.md`
- `reports/mind-design-status-2026-07-28.md`

#### Agent outputs (mind-related)
- `agent-outputs/MindUsabilityAudit`
- `agent-outputs/MindNotaSurfaceScout`
- `agent-outputs/MindNotaSurfaceCleanup`
- `agent-outputs/MindJudgmentLoopPatterns`
- `agent-outputs/MindComponentScout`
- `agent-outputs/MindQueryableKnowledgeWeave`
- `agent-outputs/MindKnowledgeModel`
- `agent-outputs/MindAcceptedKnowledge`
- `agent-outputs/MindPracticalKnowledgeModel`
- `agent-outputs/MindLiveJudgeEval`
- `agent-outputs/MindJudgeHardening`
- `agent-outputs/SpiritMindDomainLibrary`
- `agent-outputs/MindOrchestrateChangeClosure`

---

#### Curriculum Skill Files

Skill files are flat `.md` files at `/git/github.com/LiGoldragon/Curriculum/skills/`. The relevant ones:

#### nexus.md (quoted verbatim above in the research)

Description: "A long-running Nexus with privileged and ordinary sockets, CLI clients, and binary signal contracts is being designed, built, or changed."

136 lines. Covers: the Nexus and its repo naming, the running Nexus ("Everything is in the running Nexus"), Signal wire format, CLIs ("The CLI's role is to transform text into Signal"), wire type repos, traits first, no free functions, how nexuses fit together.

#### nexus-rationale.md (quoted verbatim above)

Description: "A Nexus is being discussed with the living psyche and the reasoning behind its shape is needed."

22 lines. Covers the *why*: coarse-grained separation, incremental recompilation, zero-downtime self-update, the heart/body metaphor, meta socket as root user.

#### agent-harness-packaging.md (quoted verbatim above)

Description: "An external manager for coding harnesses must be selected, packaged, installed, configured, or integrated."

19 lines. Guidelines for packaging external harnesses (Claude/Codex/Orca).

#### orchestrate.md (quoted verbatim above)

Description: "An ordinary Orchestrate Lock request must be constructed, submitted, or interpreted."

33 lines. Documents Lock, Release, Observe requests in datom format.

#### lojix.md (quoted verbatim above)

Description: "A Lojix request must be constructed, submitted, observed, or interpreted."

408 lines. Extensive documentation of the Lojix CLI protocol for ordinary and owner requests, deploy contracts, bootstrap, store inspection. Still uses DOTOS syntax (not datom) in its CLI examples.

#### datom.md (quoted verbatim above)

Description: "Constructing, reading, or interpreting datom, or implementing Datomic."

104 lines. Covers text forms, CLI conventions, Datomic kind in Rust.

#### ethos.md (quoted verbatim above)

Description: "Writing or reading an ethos file, or generating Rust from one."

156 lines. Covers file roots (Library, Signal), type declarations, kinds, associations, imports, generation.

#### protos.md (quoted verbatim above)

Description: "Reading or writing any protos dialect, or touching the protos crate."

67 lines. Covers delimiters, separators, heads, bare words, comments, canonical spacing, layers, kinds.

#### psyche.md (quoted verbatim above)

Description: "What agents are reading when they read psyche."

71+ lines. Covers four levels (Spirit, Intent, Vision, Notion), where psyche lives, agent guidelines.

---

#### Old vs. New Stack Summary

| Component | Stack | Key Dependencies |
|---|---|---|
| **orchestrate** | **NEW** (ethos-zero, datomic, protos) | datomic, ethos-zero, protos |
| **datomic** | **NEW** (protos) | protos |
| **ethos-zero** | **NEW** (protos, datomic) | protos, datomic (generates Datomic impls) |
| **protos** | **NEW** (self-declared in ethos) | none |
| **lojix** | **MIXED** | datomic, protos (but retains DOTOS text features) |
| **mind** | **OLD** | schema-rust, schema, signal-mind, DOTOS/NOTA |
| **psyche** | **EMPTY** | no deps (scaffold) |
| **persona** | **OLD** | schema-rust, schema, signal-*, NOTA |
| **harness** | **OLD** | schema-rust, signal-harness, NOTA |
| **listener** | **OLD** | signal-listener, NOTA |

---

### Part B -- Design Flows

---

#### Flow e06e4c07 -- "Designing flow, the Nexus that sets up and starts a model flow"

- **Date**: 2026-08-19 through 2026-08-20
- **Path**: `/home/li/primary/flows/e06e4c07/`

#### Files

- `log.md` -- the flow log
- `annotations.md` -- migration annotations from flow 01a02a06 and flow acbb6006
- `vision/nexus.md` -- the founding Nexus dictation (13:49) and multiple typed corrections
- `vision/archive-nexus.md` -- archived typed corrections on edges, contracts
- `vision/flowDaemon.md` -- (empty, content archived)
- `vision/archive-flowDaemon.md` -- "Curriculum is rewritten as a Nexus; skills live in another repo"
- `vision/flowKnowledge.md` -- "a flow knows what the other flows know"; transcript search tool
- `vision/flowsNotAgents.md` -- "an agent is a whole being; synthetic intelligence"
- `vision/gradientsOfAuthority.md` -- "no magic way for a computer to know if its input is from a psyche"
- `vision/letsUseTheSameVocabulary.md` -- "living psyche always called living psyche"; "transcript" names the file
- `vision/managementDelegation.md` -- "a flow and its subflows are one flow" REFUSED; liability semantics
- `vision/rustComponentArchitecture.md` -- "the component is a Nexus"
- `vision/skillDesigning.md` -- rationale skills; no repeated lines across skills
- `vision/testTravesties.md` -- prose-pinning assertions are not tests

#### What was decided (verbatim rulings from the log)

- "managementDelegation 2026-08-19: 'a flow and its subflows are one flow' refused -- out of context."
- "nexus (new topic) 2026-08-19: two entries -- the Nexus statement; Nexus Core, signal contracts, meta case by case, rename, repo, parallel skill."
- "flowDaemon 2026-08-19: flow repo = machinery + a few basic skills replacing the built-in harness prompt; user skills in another repo; name stays flow."
- "flowsNotAgents 2026-08-19: agent = whole being; synthetic intelligence."
- "rustComponentArchitecture 2026-08-19: component is a Nexus; placeholder traits; ontology before implementation; Ethos."
- "letsUseTheSameVocabulary 2026-08-19: living psyche always called so."
- "skillDesigning 2026-08-19: parallel skill for a skill's reasoning."
- "flowKnowledge (new topic) 2026-08-19: discussion drips into every flow it concerns."
- "nexus 2026-08-19 (later entries): core-<nexus> already killed; at least two sockets; CLI per socket; nexus repo a possibility; universal nexus traits first."
- "gradientsOfAuthority 2026-08-19: no way for a computer to know its input is from a psyche."
- "letsUseTheSameVocabulary 2026-08-19: transcript names the harness file."
- "testTravesties 2026-08-20: prose-pinning assertions are not tests; hunt them down."

#### What was left open

- Question 1: "does flow launch an existing harness (Claude Code / Codex) with a composed system prompt, or run its own model loop?" -- UNANSWERED.
- Universal nexus traits (first principles design).
- Batched skill edits for vocabulary, skill-designing, nexus.
- Briefing role + subflows line.

---

#### Flow 01a05826 -- "Flow identity semantics"

- **Date**: 2026-08-31
- **Path**: `/home/li/primary/flows/01a05826/`

#### Files

- `log.md` -- the flow log
- `vision/flowIdentity.md` -- flow identity rulings
- `vision/subflowIdentity.md` -- subflow identity ruling

#### What was decided (verbatim from vision files)

Flow identity:
> "I want to use the most random earliest part of the ID." -- psyche
> "Whatever the random part of the session ID is, I dont think we need more than 4 characters." -- psyche
> "Then let's use 6 chart. [...] If it does find a collision, then it would just add one or two extra characters" -- psyche (later, upgraded from 4 to 6)
> "We can't convert the ID because the reference has to be straightforward." -- psyche
> "just a small, simple tool in Python or whatever [...] one for Claude, one for Codex" -- psyche

Subflow identity:
> "I don't want subflows to start creating their own lanes. They just use their parents." -- psyche

From the log: The current ruling is to use six literal characters from the actually random portion of the harness ID, with no hash or conversion. A small harness-specific tool checks availability. Old IDs remain unchanged. Subflows do not create their own lanes.

#### What was left open

- Whether subflows return material for the parent alone to write, or may write directly.
- The exact tool-owned identity marker.
- Whether a cold resume keeps the same lane.
- Automatic session naming in Codex (deferred).
- Multi-topic distillation proposal ready for living review but not yet changed in Vision.

---

#### Flow 01a05e95 -- "Flow identity realization"

- **Date**: Realized after 01a05826
- **Path**: `/home/li/primary/flows/01a05e95/`

#### Files

- `log.md` -- the flow log
- `vision/logging.md` -- rare high-level logging
- `vision/flowSkills.md` -- main-flow and subflow skill redesign
- `vision/subflows.md` -- parent flow directory

#### What was decided (verbatim from log)

> "Realized one parent-owned flow lane with focused child contexts. The parent supplies one shared `FLOW_ID` and `FLOW_DIRECTORY`; each child obtains its own thread identity after launch, performs its work, creates no lane/index/log, and returns its final response."

Settled:
- Replaced overloaded `flows`/`subflows` skills with `main-flow`, `child-flow`, and `flow-evidence`.
- Corrected the initially impossible pre-spawn `THREAD_ID` requirement.
- Added the harness-owned `flow-id` helper (Codex claims `CODEX_SESSION_ID[23:29]`).
- Transcript-grounded migration consolidated all 24 proven child/extended lanes into their root lanes.

Vision quotes:
> "Logging should be rare. It should just be to give a very high-level summary. [...] A thousand lines of logging just for a single session is fucking insane." -- psyche
> "I want subflows to use the parent flow directory." -- psyche
> "I think we should have some kind of a master flow or main flow skill that explains the part about using subflows." -- psyche

#### What was left open

- Native automatic child-brief injection not present.
- Live Home activation not attempted.
- Orchestrate skill's braced release syntax disagrees with deployed Orchestrate 0.26's bare release product.

---

#### Other flows mentioning the target components (from flows/index.md)

#### Nexus/flow design chain
| ID | Date (approx) | Title |
|---|---|---|
| e06e4c07 | 2026-08-19 | Designing flow, the Nexus |
| 5c8be3ca | | Flow-artifacts protocol design |
| 15b67974 | | Continuing e06e4c07: actor library review |
| 01a05826 | 2026-08-31 | Flow identity semantics |
| 01a05e95 | | Flow identity realization |

#### Datom/ethos/protos/nexus design chain
| ID | Title |
|---|---|
| aa4c7747 | Software-design skill and Ethos zero design |
| f426777b | Remember aa4c7747; assemble all vision on datom, nexus, trait-based design, and ethos |
| cff271af | Deep understanding of software-design and nexus skill vision against datom and ethos-monolith |
| 68512643 | Datom/ethos-monolith design-thread pickup |
| b675f3d9 | Remember f426777b and everything on ethos and ontology/anatomy-based design |
| ac1e9ec8 | Acquire all psyche on datom syntax, distill it |
| 04db2fd2 | Review the anatomy of the Datom textualize/realize logic |
| acbb6006 | Collect all psyche vision on datom, ethos, protos, nexus |
| 2ef42163 | Become expert in Protos, datom, ethos |
| db97561c | Agglomerate all recent Protos/Datum/Ethos vision |
| e8c4cc61 | Signal/Nexus/sema runtime design for nexuses |
| 62022e8f | Protos datom ethos implementation anatomy and syntax design |
| 995a164e | Protos layers, matching machinery |
| 4decf7 | Remember datom, ethos, protos, nexus; distill-as-we-go |
| e4a40e | Bring the unapproved parts to approval; Nexus and sema anatomy |
| ad19b1 | Continue distilling: datom Meaning, kinds Identity and Declaration, ethos |
| 6329f1 | Realize a new POC stack with orchestrate as the MVP |
| e996e8 | Resume Protos and Ethos Declaration distillation |
| b9a334 | Collect all psyche, deliver web report of the situation |
| 01a04a30 | Realize Protos, Datomic, and Ethos-zero on the Portion pivot |

#### Harness/persona/mind
| ID | Title |
|---|---|
| 01a03952 | Edit-coordination skill for the new orchestrate Nexus |
| 444e5e | Repair Claude flow-ID initialization and harness-specific main-flow deployment |
| 01a01a93 | Harness-presence limit established |
| 2f6b1dc5 | Base-prompt replacement design |
| 4ddc321d | Remember base-prompt replacement design |

#### Wispr/Listener
| ID | Title |
|---|---|
| 01a04e75 | Adapt Listener to Wispr Flow |
| 01a05209 | Packaging the Wispr Flow Electron client on NixOS |
| 01a0539e | Wispr shortcut repair |
| 01a05588 | Wispr Desktop local interface for Listener proxy |
| 4647d2 | Listener STT porting status |
| b2da01 | Wispr Flow to power Listener |
| 81c0dc | Wispr overlay geometry and hands-free activation |
| 01a06da9 | Wispr status-bar and hands-free mission |
| 4e296a | Wispr Noctalia startup and status repair |
| acf06f | Wispr recording and hands-free status |

#### Current realization flow
| ID | Title |
|---|---|
| 1a6ca4 | **Gather the latest vision across recent flows and the landing distillation; rewrite datom and Ethos Zero to comply, Fable-audited; then orchestrate; then port every component still on old Ethos or old schema; next the psyche and mind components.** |

---

#### Distilled Vision Files (from primary)

#### Vision/nexus.md (105 lines, quoted in full above in the research)

Key sections: "A Nexus is the whole" (long-running component), Sockets (at least two), Default clients (one CLI per socket), Signal only (pure binary), The graph (vertices and edges), Routing (through a router), Configuration (starts with no arguments, Sema database), First configuration (standard metadata tree), Repositories (three per component), Everything is a Nexus, Actors (Kameo-driven), Splitting a Nexus, Observation by subscription, Polling is forbidden.

#### Vision/flowNexus.md (16 lines)

> The Flow Nexus sets up and starts a model flow: its working directory, system prompt, training files and instruction prompt. It takes the place of the abandoned training daemon.
>
> The flow repository holds the machinery of the Flow Nexus and is a runtime repository. Every skill lives outside it, the basic skills included, so that a change to a skill causes no Nix rebuild. The basic skills give our own take on how an agent behaves in a harness, replacing the prompt the harnesses build in.


### Corrections and additions to the survey above (this subflow's own checks)

- The survey says mind's 21 dirty files are a migration; I checked `git diff` in /git/github.com/LiGoldragon/mind: it is a NOTA-to-DOTOS feature/script rename (436 lines mention dotos, 8 mention datom), i.e. an old-stack rename, not a move to datom. Last substantive mind commit: 2026-07-09 "Move knowledge judge calls off store kernel path"; the 2026-08-13 HEAD is "docs: mark Protos estate status" (the same docs-only commit landed on persona, spirit, judge, mind-judge, spirit-judge, orchestrator-judge that day). Persona's last substantive commit: 2026-07-07. `du -sh` gave mind 20M and persona 24M in my run (the survey's 40M/25M were measured separately; the difference is not explained).
- The survey says several Curriculum skills are "quoted verbatim above"; they are not reproduced in it. Paths: /git/github.com/LiGoldragon/Curriculum/skills/{nexus,nexus-rationale,agent-harness-packaging,orchestrate,lojix,datom,ethos,protos,psyche}.md. The deployed copies are under /home/li/primary/.claude/skills/<name>/SKILL.md.
- Judge repos (the existing "thinking machine call" machinery), all under /git/github.com/LiGoldragon/, all first committed 2026-07-08/10, all last touched by the 2026-08-13 docs commit, all on the old signal/DOTOS/NOTA stack:
  - judge 0.2.0 — README: "Shared adapter mechanics for model-backed judge edges. This repo owns provider/proxy calling support, secret-source and external-session references, bounded/redacted child-process failure mechanics, and provider reply records. Calls are single-attempt; adapters own any domain-specific retry."
  - spirit-judge 0.3.0 — README: "the model/provider edge for the admission-only Spirit judge contract. It reads the matching public prompt pack from spirit-judge-config, serves typed frames on a Unix socket, and is neither a Spirit daemon nor Spirit storage." "The admission contract carries the current four-field Entry shape: domains, kind, description, and importance."
  - mind-judge 0.1.0 (+ mind-judge-config: "Prompt prose lives here so prompt edits do not require Rust or Nix rebuilds") — README: "consumes signal-mind-judge, reads prompt/config data from a configured mind-judge-config checkout or package path, and will call model providers through judge. It does not depend on agent-daemon and is not a Mind core daemon."
  - orchestrator-judge 0.1.0 — "serves two request paths — topic assignment and message triage — over a Unix socket."
- reports/mind-design-status-2026-07-28.md (162 lines, agent-authored recovery) finds: "Mind is **not design-complete**." Its through-line: "a durable, local Persona knowledge/state component, not a router or a second Spirit"; "AI decides semantic admission; deterministic code owns typed shape, routing, storage, and applying a verdict" is classed as "Reported constraint plus implemented design ... not a located direct ruling". agent-outputs/Mind* (13 directories) hold the July mind design handoffs.
- reports/PersonaSpiritVsSpirit-2026-08-21.md (240 lines) answers the living's "What is in [persona-spirit] that isnt in spirit?": persona-spirit is a 13-actor Kameo supervision tree with a NOTA ingress pipeline; spirit is a plain-struct NexusEngine with no kameo dependency.
- harness repo: the 2026-09-02 commits are the `flow-id` parent-flow identity helper ("Add atomic flow identity helper", "Normalize flow aliases as hexadecimal", "Publish complete flow claim markers"); the daemon/launcher work (SessionLauncher spawning pi/claude sessions) dates from 2026-07-18. Also present: /git/github.com/LiGoldragon/{claude-hijack,codex-hijack} (the base-prompt replacement repos of flows 2f6b1dc5/4ddc321d; not surveyed here) and /git/github.com/LiGoldragon/transcript (the search shim, "Temporary, pending a Nexus").


## 4. Attention in transcript history (last 90 days: 2026-06-07 to 2026-09-05)

Three measures. Scripts: `/tmp/claude-1001/-home-li-primary/1a6ca4f9-e0fa-4f2c-bd6f-a40651590354/scratchpad/{attention.py,typed.py,typed2.py}` (not part of primary). All regexes case-insensitive; "mind" is `\bmind\b`; "flow (component/protocol)" is `flow[- ]?(identity|daemon|component|protocol|directory|artifacts|anatomy|naming|lane)|flows? (skill|protocol)|subflow|main[- ]flow`; "ethos" includes ethos-zero/monolith/engine; "legal/acceptance/review" is `legal|acceptance|review (procedure|process)`.

### 4a. The living's typed and dictated messages (the best measure of the living's attention)

Every message with Claude `origin.kind == human` in `~/.claude/projects/**/*.jsonl` (excluding `subagents/` transcripts) and every `user`-role message in root (non-subagent) Codex rollouts under `~/.codex/sessions/**`, whose timestamp is in the window. Messages beginning with `<` (pasted environment blocks) are dropped. Total: 3,267 messages (Claude 1,343; Codex 1,924) across 308 sessions. The earliest message on disk is 2026-07-24; nothing from June survives, so the June column is empty by absence of data, not absence of attention.

| name | typed msgs | sessions | Jul | Aug | Sep | last typed |
|---|---|---|---|---|---|---|
| psyche | 596 | 248 | 94 | 420 | 82 | 2026-09-04 |
| flow (any) | 486 | 202 | 36 | 305 | 145 | 2026-09-04 |
| subagent | 337 | 212 | 67 | 230 | 40 | 2026-09-04 |
| flow (component/protocol) | 190 | 126 | 0 | 127 | 63 | 2026-09-04 |
| ethos | 179 | 59 | 10 | 152 | 17 | 2026-09-04 |
| harness | 145 | 86 | 47 | 86 | 12 | 2026-09-04 |
| protos | 138 | 48 | 36 | 96 | 6 | 2026-09-04 |
| orchestrate | 128 | 86 | 57 | 60 | 11 | 2026-09-04 |
| datom | 115 | 47 | 1 | 105 | 9 | 2026-09-04 |
| nexus | 76 | 37 | 1 | 71 | 4 | 2026-09-04 |
| lojix | 57 | 34 | 9 | 35 | 13 | 2026-09-04 |
| mind | 49 | 38 | 9 | 38 | 2 | 2026-09-04 |
| wispr | 37 | 16 | 0 | 15 | 22 | 2026-09-04 |
| listener | 27 | 14 | 3 | 17 | 7 | 2026-09-04 |
| legal/acceptance/review | 26 | 17 | 13 | 12 | 1 | 2026-09-04 |
| persona | 7 | 6 | 0 | 6 | 1 | 2026-09-04 |
| meta-harness | 7 | 7 | 0 | 6 | 1 | 2026-09-04 |
| wheelhouse/yegge | 4 | 4 | 0 | 3 | 1 | 2026-09-04 |

The same, excluding this flow's own session (1a6ca4, whose brief names everything), with the last date the living typed the name before this flow:

| name | typed msgs | sessions | last typed before 1a6ca4 | Sep msgs |
|---|---|---|---|---|
| psyche | 595 | 247 | 2026-09-04 | 81 |
| flow (component/protocol) | 190 | 125 | 2026-09-04 | 63 |
| ethos | 178 | 58 | 2026-09-04 | 16 |
| harness | 144 | 85 | 2026-09-04 | 11 |
| protos | 137 | 47 | 2026-09-04 | 5 |
| orchestrate | 127 | 85 | 2026-09-04 | 10 |
| datom | 115 | 47 | 2026-09-04 | 9 |
| nexus | 75 | 36 | 2026-09-03 | 3 |
| lojix | 57 | 34 | 2026-09-04 | 13 |
| mind | 48 | 37 | 2026-09-03 (idiom); 2026-08-06 as component | 1 |
| wispr | 37 | 16 | 2026-09-04 | 22 |
| listener | 27 | 14 | 2026-09-04 | 7 |
| legal/acceptance/review | 25 | 16 | 2026-08-29 (all "acceptance criteria"/"legal character" uses) | 0 |
| persona | 6 | 5 | 2026-08-21 | 0 |
| meta-harness | 6 | 6 | 2026-08-22 | 0 |
| wheelhouse/yegge | 3 | 3 | 2026-08-06 | 0 |

Caveats: "psyche" is inflated by "load the psyche skill" and "psyche-interraction" in typed briefs; "subagent"/"flow" by delegation instructions; "mind" by idioms ("in mind", "clear your mind", "read my mind") — I listed all 49 mind hits and count about 8 that concern the Mind component (2026-07-28 x4, 2026-08-05 x2, 2026-08-06, 2026-09-04); "harness" is dominated by Claude/Codex upgrade and hijack work, not the persona meta-harness; "legal/acceptance/review" hits are acceptance criteria in briefs and "colon legal in string position", none about a legal system before 2026-09-04.

### 4b. Flows in flows/index.md whose title or log brief mentions the name

flows/index.md carries no dates; the date used is the flow directory's first git commit in primary. All 171 flows fall in the window because the flows/ tree was created by migration on 2026-08-21/22, so flows older than that carry the migration date, not their session date. The brief is the first 15 lines of flows/<id>/log.md.

| name | flows | last flow (git-add date) |
|---|---|---|
| flow (any) | 144 | 2026-09-05 |
| psyche | 103 | 2026-09-05 |
| flow (component/protocol) | 69 | 2026-09-05 |
| lojix | 34 | 2026-09-04 |
| datom | 32 | 2026-09-05 |
| nexus | 27 | 2026-09-05 |
| ethos | 26 | 2026-09-05 |
| orchestrate | 25 | 2026-09-05 |
| protos | 20 | 2026-09-04 |
| harness | 17 | 2026-09-05 |
| wispr | 13 | 2026-09-05 |
| listener | 10 | 2026-09-05 |
| subagent | 4 | 2026-09-05 |
| legal/acceptance/review | 3 | 2026-09-02 (none about a legal system) |
| mind | 1 | 2026-09-05 (this flow) |
| persona | 1 | 2026-08-21 (15b67974) |
| meta-harness | 0 | - |
| wheelhouse/yegge | 0 | - |

Flows that name nexus (27, chronological by git-add date): 15b67974, e06e4c07 (08-21); 68512643, cc4105a6, cff271af (08-22); 01a02fd5 (08-23); aa4c7747 (08-24); 01a03603, 01a03952, f426777b (08-25); 01a03d6e, 01a03eda, 01a03fe9, b675f3d9 (08-26); 01a04236, acbb6006 (08-27); 01a047d2 (08-28); 01a04e75, e8c4cc61 (08-29); 62022e8f (08-30); 01a05487, 01a05833, 4decf7, 995a164e (09-02); ad19b1, e4a40e (09-03); 1a6ca4 (09-05). Full per-name lists with titles: scratchpad `attention.md`.

### 4c. Transcript files whose first user message mentions the name

All Claude JSONL files (root and `subagents/`) and Codex rollouts (root and subagent threads) modified in the window: 3,996 files (Claude 1,812; Codex 2,184), of which 2,678 had a parseable first user message (the rest begin with tool results, environment blocks, or are empty). Counts are dominated by agent-authored briefs, which name many components at once; the "last transcript" column is 2026-09-05 for every name because this flow's subagent briefs mention them all. Kept for completeness only.

| name | transcripts | | name | transcripts |
|---|---|---|---|---|
| psyche | 1559 | | lojix | 204 |
| flow (any) | 1376 | | mind | 74 |
| subagent | 859 | | persona | 40 |
| flow (component/protocol) | 647 | | legal/acceptance/review | 33 |
| orchestrate | 640 | | listener | 24 |
| ethos | 593 | | meta-harness | 9 |
| protos | 503 | | wheelhouse/yegge | 6 |
| harness | 452 | | wispr | 5 |
| datom | 434 | | | |
| nexus | 270 | | | |

### 4d. Last date each component's code was worked on (git, section 3)

orchestrate 2026-09-04 (0.29.2); lojix 2026-09-04 (0.20.3); datomic 2026-09-04 (0.9.0); ethos-zero 2026-09-04 (1.2.0); wispr-flow-linux 2026-09-04; harness 2026-09-02 (0.3.2, flow-id helper; last daemon work 2026-07-18); protos 2026-08-29 (0.14.0); listener 2026-08-29 (0.14.0); psyche 2026-08-14 (0.1.0 scaffold); mind 2026-08-13 docs-only, last substantive 2026-07-09 (0.8.0); persona 2026-08-13 docs-only, last substantive 2026-07-07 (0.2.0); spirit 2026-08-13 (0.27.0); judge/mind-judge/spirit-judge/orchestrator-judge 2026-08-13 docs-only.


## 5. How the components relate — the living's words

Collected from the records above (each sentence's path is given; the full entries are in section 2). Duplicates across the three gatherings are merged.

### Sequence — what comes first

- "but datom and ethos first, so we can actually write all this logic" — on the meta-harness replacing beads (flows/012fbf07/vision/gradientsOfAuthority.md, 2026-08-11).
- "our first work will be a simple orchestrate nexus that reserves paths to make dead-simple datom-syntax path reservation possible for edit coordination." (flows/aa4c7747/vision/orchestrate.md, 2026-08-25).
- "So we have to take one bite at a time here." (flows/01a02a34/vision/progression.md, 2026-08-22; context: schema, meta-harness, data-evolution, syntax and skill changes proceed incrementally).
- "Once that's done, start porting the components that are still using either the old Ethos or the old schema over to the new Datum and the new Ethos 0. Our next target after orchestrates is going to be the psyche component and the mind component." (transcript 1a6ca4 line 6, 2026-09-04; the working instruction is in flows/1a6ca4/log.md).
- Transcript only, 2026-07-28: "Priority stack: orchestrate → mind → messenger" — a Claude-authored note the living forwarded to Codex, not the living's words; the living's own words the same day: "I'd like to refocus on Mind and Orchestrate for them to work properly, for Messenger to work so that agents can communicate with each other."
- "yes for now. we will create our own custom harness in the future, which will be 100% typed datom messages going in and being expected out." (flows/15b67974/vision/flowDaemon.md, 2026-08-21).
- "yes, until we design the meta-harness (persona) properly and all the data is passed along the right agent call, like magic" (vision-raw/gradientsOfAuthority.md, 2026-08-11).
- "skills for now. It might evolve differently later. This will move quite fast as we build the persona meta-harness" (flows/358f143a/vision/workspace20.md, 2026-08-17).
- "beads are not entirely out, but we are keeping them for issue tracking" (flows/012fbf07/vision/gradientsOfAuthority.md, 2026-08-11).

### Containment — what contains what

- "A Nexus is the whole long-running component: the process, its sockets, and the signal contracts it is compiled with." "The decision-making engine inside a Nexus is Nexus Core." (Vision/nexus.md).
- "nexus is not a thing, its a kind of thing" (flows/01a05487/vision/nexus.md).
- "everything we're going to build is going to be a nexus now, and anything that has already been built that did not take the shape of The nexus is going to be rewritten." (flows/e06e4c07/vision/rustComponentArchitecture.md, 2026-08-19).
- "The flow repository holds the machinery of the Flow Nexus and is a runtime repository. Every skill lives outside it, the basic skills included" (Vision/flowNexus.md).
- "obviously another nexus." — transcripts do not belong to the flow Nexus (flows/e06e4c07/vision/flowKnowledge.md, 2026-08-19).
- "a new component which will include spirit, named psyche, which will hold spirit, intent and vision, and be used to feed the hijacked llm calls" (flows/012fbf07/vision/threeStacks.md, 2026-08-11); "spirit is to be abandonned for psyche" (vision-raw/spiritComponentAndFile.md, 2026-08-21).
- "the psyche log is obviously going in Psyche, which is why Psyche is so important: it gets its own sort of mind-like component" (flows/1a6ca4/vision/psyche.md, 2026-09-05).
- "essentially the memory of the system is going to go in mind" (flows/1a6ca4/vision/mind.md, 2026-09-05). Transcript only, 2026-08-06: "this psyche component is different than the mind, which is more like the agent's mind, or a store of memories".
- "That repo hasent been touched in a long time, even though it's slated to orchestrate the entire meta harness (called persona)" (flows/15b67974/vision/persona.md, 2026-08-21).
- "the persona meta-harness is going to bring in the dawn of the more complete thinking machine systems, which will be a complex infrastructure of a kind of thinking machine legal system interworking apparatus." (flows/1a6ca4/vision/personaMetaHarness.md, 2026-09-05).
- "All of these components are going to use thinking machine calls in their machinery to go through acceptance processes and review processes" (flows/1a6ca4/vision/thinkingMachineProcedures.md, 2026-09-05).
- "the library takes another name so that datom is free for the datom nexus, which comes when there is more to do" (Vision/datom.md); "this can just stay in a library for now." (flows/04db2fd2/vision/archive-datomNexus.md, archived).
- "Nexus is authored in ethos so its main operations are visible." (Vision/ethosMonolith.md).
- "I don't want subflows to start creating their own lanes. They just use their parents." (flows/01a05826/vision/subflowIdentity.md, 2026-08-31).

### Prohibitions — what each must not do

- "the Nexus component cannot be involved in texturalizing signal, because it would just destroy the beauty and the simplicity of the system." (flows/e06e4c07/vision/nexus.md, 2026-08-19).
- "Polling is forbidden; a correct system goes quiet when nothing changes." (Vision/nexus.md).
- "the built in sub-agent tool is going to be disabled ... So we're going to have to have this tool that allows an agent to create sub-agents, quote unquote, which is not so much create sub-agent, then communicate with the meta harness that something needs to be done." (vision-raw/gradientsOfAuthority.md, 2026-08-10).
- "And the tool cause [calls], we're not going to do anything there in terms of putting important information in there. So if anything needs to come in, it's not going to be from a tool call." (same).
- "No more beads. Beads are tools which means lowest authority; using them for handover is stupid." (flows/012fbf07/vision/gradientsOfAuthority.md, 2026-08-11).
- "It's a lot more complex system than just letting any agent just write files and push commits." (flows/1a6ca4/vision/thinkingMachineProcedures.md, 2026-09-05).
- Transcript only, 2026-07-28: "Observe should not mutate the state on Orchestrate, that's for sure, and I don't want Orchestrate to do any kind of file system operation anymore."
- Transcript only, 2026-08-03: "The judge being down should just bar mutation, obviously. And from your graph, I see that changing certainty or importance has a direct right path in the ordinary socket. That shouldn't be. It should be in the meta sockets, which is a bypass socket."
- "a flow and its subflows are one flow" — refused, out of context (flows/e06e4c07/vision/managementDelegation.md, 2026-08-19).
- "Whenever something is machine-generated ... none of the content in it should be logged as psyche." (flows/78c93c/vision/machine-generated-content.md).

### Subagent-collected relation sentences (Nexus gathering)

Verbatim sentences from these records where the living says how Nexus relates to flow, mind, psyche, orchestrate, harness, datom, ethos, lojix:

#### Nexus and Flow

- "It's just the concept that we're going to start flows using a Nexus component, which will decide what the system prompt is and everything." (flows/1a6ca4/vision/nexus.md, 2026-09-05)
- "We're going to replace the harness's concept of subagents with this component, which will have specialized harnesses launched with specialized system prompts that will make them much more efficient at what they're supposed to be doing." (flows/1a6ca4/vision/nexus.md, 2026-09-05)
- "the new daemon I want to make isnt training anymore (abandonned). Its flow, which will setup and start a model flow, with its own working directory, system prompt and training files, and its instruction prompt." (flows/358f143a/vision/archive-flowDaemon.md, 2026-08-18)
- "obviously another nexus." (flows/e06e4c07/vision/flowKnowledge.md, 2026-08-19 — on whether transcripts belong to the flow Nexus)

#### Nexus and Orchestrate

- "in everyday speech, orchestrate-nexus will be called orchestrate, etc" (flows/acbb6006/vision/archive-nexus.md, 2026-08-27)
- "our first work will be a simple orchestrate nexus that reserves paths to make dead-simple datom-syntax path reservation possible for edit coordination." (flows/aa4c7747/vision/orchestrate.md, 2026-08-25)

#### Nexus and Harness

- "We're going to replace the harness's concept of subagents with this component, which will have specialized harnesses launched with specialized system prompts that will make them much more efficient at what they're supposed to be doing." (flows/1a6ca4/vision/nexus.md, 2026-09-05)
- "the persona meta-harness is going to bring in the dawn of the more complete thinking machine systems, which will be a complex infrastructure of a kind of thinking machine legal system interworking apparatus." (flows/1a6ca4/vision/personaMetaHarness.md, 2026-09-05)
- "we will create our own custom harness in the future, which will be 100% typed datom messages going in and being expected out." (flows/15b67974/vision/flowDaemon.md, 2026-08-21)

#### Nexus and Datom

- "the library takes another name so that datom is free for the datom nexus, which comes when there is more to do: translating datom objects between formats, and a parsing cache keyed by the content-addressed hash of normalized Text." (Vision/datom.md)
- "this can just stay in a library for now." (flows/04db2fd2/vision/archive-datomNexus.md)

#### Nexus and Ethos

- "this relates to why I want ESOS [Ethos], the language, to allow us to more coherently and clearly design the main traits and types of a system, of a nexus, of any system." (flows/e06e4c07/vision/nexus.md, 2026-08-19)
- "Nexus is authored in ethos so its main operations are visible." (Vision/ethosMonolith.md)

#### Nexus and Psyche / Mind

- "All of these components are going to use thinking machine calls in their machinery to go through acceptance processes and review processes" (flows/1a6ca4/vision/thinkingMachineProcedures.md, 2026-09-05 — said after naming the Nexus, mind and psyche components)

#### What comes first

- "but datom and ethos first, so we can actually write all this logic" (vision-raw/gradientsOfAuthority.md, 2026-08-11 — on the meta-harness)

#### What contains what

- "the Nexus part, which is the execution engine inside a Nexus" (flows/e06e4c07/vision/nexus.md, 2026-08-19)
- "The decision-making engine inside a Nexus is Nexus Core." (Vision/nexus.md)
- "A Nexus is the whole long-running component: the process, its sockets, and the signal contracts it is compiled with." (Vision/nexus.md)
- "nexus is not a thing, its a kind of thing" (flows/01a05487/vision/nexus.md)

#### What it must not do

- "the Nexus component cannot be involved in texturalizing signal, because it would just destroy the beauty and the simplicity of the system." (flows/e06e4c07/vision/nexus.md, 2026-08-19)
- "Polling is forbidden; a correct system goes quiet when nothing changes." (Vision/nexus.md)

---

### Subagent-collected relation sentences (mind/psyche/flow gathering)

Verbatim sentences where the living says how mind, psyche, or flow relate to each other or to nexus, orchestrate, harness, datom, ethos, lojix:

**Mind and Psyche:**
> "There's the mind component, which is essentially going to replace a lot of the files and the readmes, not the psyche log (the psyche log is obviously going in Psyche, which is why Psyche is so important: it gets its own sort of mind-like component)." — flows/1a6ca4/vision/mind.md

**Psyche component and Spirit:**
> "I have a better approach now, for a new component which will include spirit, named psyche, which will hold spirit, intent and vision, and be used to feed the hijacked llm calls" — flows/012fbf07/vision/threeStacks.md

> "spirit is to be abandonned for psyche." — vision-raw/spiritComponentAndFile.md

> "the function of the component is to hold the spirit records. it isnt working very well so we are using a file now" — vision-raw/spiritComponentAndFile.md

**Psyche component has Spirit/Intent/Vision enum:**
> "we re-use much of spirit, and introduce a top-level enum; Spirit, Intent, Vision, which differentiates which layer records belong to." — flows/012fbf07/vision/threeStacks.md

**Psyche and witness reuse (nexus pattern):**
> "It's kind of like what we have been doing in the spirit component, which has been shelved for now and has to be ported over to this newly called psyche component. The nexus is where we were doing an LLM call to check if the proposal already existed and if it was contradicting something already in the database and stuff like that." — flows/78c93c/vision/witness-reuse.md

**Flow Nexus and the Flow component:**
> "It's just the concept that we're going to start flows using a Nexus component, which will decide what the system prompt is and everything. We're going to replace the harness's concept of subagents with this component, which will have specialized harnesses launched with specialized system prompts that will make them much more efficient at what they're supposed to be doing." — flows/1a6ca4/vision/nexus.md

**Flow component sequenced after orchestrate; datom and ethos first:**
> "No more beads. Beads are tools which means lowest authority; using them for handover is stupid. In fact, we need to replace beads with our meta-harness (context-stratification-seizure) approach to get much better results. but datom and ethos first, so we can actually write all this logic" — flows/012fbf07/vision/gradientsOfAuthority.md

**Flow and Nexus:**
> "everything we're going to build is going to be a nexus now, and anything that has already been built that did not take the shape of The nexus is going to be rewritten." — flows/e06e4c07/vision/nexus.md

**Flow is not an agent:**
> "It's not an agent because to me, an agent is more of a whole being, and a whole being is a lot more than a single LLM chat, which is linear and very limited. ... So a flow more accurately describes essentially an AI flow, right? Which is just one of the many flows that together, when properly structured and orchestrated, will resemble an artificial being or a synthetic intelligence." — flows/e06e4c07/vision/flowsNotAgents.md

**Flow as thought:**
> "the idea behind flow is simple; a flow of thought. An intelligence isnt a single flow of thought, it is a multitude of flows. so using the term 'agent', which entails subjectivity, when speaking of a single flow does not correspond with reality." — flows/4ddc321d/vision/flow.md

**Mind replaces what was done with Markdown files:**
> "The mind will kind of replace all this reporting and keeping track of which repositories are involved, what kind of knowledge and witnesses, and all of this stuff that we're clumsily doing with Markdown files and indexes and all of that stuff. It's keeping them, summaries of transcripts, and essentially the memory of the system is going to go in mind" — flows/1a6ca4/vision/mind.md

**Thinking machine calls in all components (mind, psyche, nexus) — acceptance and review:**
> "All of these components are going to use thinking machine calls in their machinery to go through acceptance processes and review processes, so data isn't just going to come in because it's being submitted. It's going to go through." — flows/1a6ca4/vision/thinkingMachineProcedures.md

**Transcripts belong to another nexus (not the flow nexus):**
> "obviously another nexus." — flows/e06e4c07/vision/flowKnowledge.md

**Flow launches a harness (for now); custom harness later with 100% typed datom messages:**
> "yes for now. we will create our own custom harness in the future, which will be 100% typed datom messages going in and being expected out." — flows/15b67974/vision/flowDaemon.md

---

## 6. Unknowns

- Whether "the Nexus component" that starts flows (2026-09-05) and "the Flow component" / Flow Nexus (Vision/flowNexus.md) are one component or two; the living named both in one breath and said of the Flow component "I'm not sure, though, about the architecture, if that's been laid out to my liking." No record settles it.
- The Flow Nexus's anatomy: no record beyond Vision/flowNexus.md's two paragraphs and e06e4c07's settled Nexus vocabulary. How a system prompt is composed per specialized harness, what "specialized harnesses" are (wrappers such as the "Claude Light / Codex Bare" renamed executables of flows/38dec9/vision/perHarnessSkills.md, or the custom typed-datom harness of 2026-08-21), and how the replacement for the sub-agent tool talks to the Nexus — unstated.
- Mind's anatomy on the new stack: the only psyche record is the 2026-09-05 sentence; the 2026-08-06 transcript statement (judge calls, obsolescence review, escalation) is dictated and unconfirmed; the existing mind repo's design was found "not design-complete" on 2026-07-28 and the living said "I don't think I was finished even designing Mind."
- Whether the Psyche component and the mind component share machinery ("its own sort of mind-like component") or only shape — unstated.
- The "legal system": the procedures for accepting, raising in importance, taking down, replacing are named, not specified. Whether the existing judge repos (judge, spirit-judge, mind-judge, orchestrator-judge; old stack, single-attempt provider adapters) are the seed or are to be rewritten is not said; the general rule "anything that has already been built that did not take the shape of The nexus is going to be rewritten" applies by my inference.
- Persona: "slated to orchestrate the entire meta harness" but persona's 1814-line ARCHITECTURE.md predates the Nexus vocabulary, datom, ethos-zero and the psyche component; nothing says which of it stands.
- Which Yegge writing the living meant by "his wheelhouse harness": the 2026-08-05 reference was to the two-part "Shape of Things to Come"; the digest reports/YeggeOnAgents-2026-08-05.md is agent-authored and unverified against the source; I did not fetch it.
- Dates of several raw records (flows/38dec9, 01a052b6, 78c93c, 01a05487 vision files carry no date; git-add dates are given instead).
- The transcript corpus on disk begins 2026-07-24; the living's attention before that is not measurable here.

## Sources

- Psyche records: /home/li/primary/Vision/*.md, /home/li/primary/Intent/*.md, /home/li/primary/vision-raw/*.md, /home/li/primary/flows/*/vision/*.md, /home/li/primary/flows/*/notion/*.md (paths per entry above). Three gatherings by read-critical subagents of this subflow (Nexus/harness; mind/psyche/flow; code/design) and this subflow's own reading (persona, thinking machines, legal, Yegge, attention); intermediate files under /tmp/claude-1001/-home-li-primary/1a6ca4f9-e0fa-4f2c-bd6f-a40651590354/scratchpad/.
- This flow's vision: /home/li/primary/flows/1a6ca4/vision/{nexus,mind,psyche,flow,personaMetaHarness,thinkingMachineProcedures,datom}.md; brief: /home/li/primary/flows/1a6ca4/log.md; transcript /home/li/.claude/projects/-home-li-primary/1a6ca4f9-e0fa-4f2c-bd6f-a40651590354.jsonl line 6.
- Design flows: /home/li/primary/flows/e06e4c07/{log.md,annotations.md,vision/}, /home/li/primary/flows/01a05826/{log.md,vision/}, /home/li/primary/flows/01a05e95/{log.md,vision/}, /home/li/primary/flows/15b67974/vision/.
- Transcript-only statements: /home/li/.codex/sessions/2026/07/28/rollout-2026-07-28T12-31-37-019fa847-ac12-71e2-9a8d-65dfc056ee7d.jsonl lines 9, 456, 538; /home/li/.claude/projects/-home-li-primary/d04b76d9-e818-4705-b0ae-4cb610789aa0.jsonl lines 53, 81; /home/li/.claude/projects/-home-li-primary/7e7c9b3d-de9d-434f-9c00-937bf621e8af.jsonl line 636; Codex session 019fbf4a (2026-08-03/04) under /home/li/.codex/sessions/2026/08/. Searched with /git/github.com/LiGoldragon/transcript/transcript.py and the scratchpad scripts.
- Code: /git/github.com/LiGoldragon/{mind,psyche,persona,harness,spirit,persona-spirit,judge,mind-judge,mind-judge-config,spirit-judge,orchestrator-judge,orchestrate,lojix,datomic,ethos-zero,protos,listener,wispr-flow-linux,transcript}; git log / Cargo.toml / README.md / ARCHITECTURE.md of each; /git/github.com/LiGoldragon/Curriculum/skills/{nexus,nexus-rationale,agent-harness-packaging,orchestrate,lojix,datom,ethos,protos,psyche}.md (read as evidence with cat, not loaded).
- Reports in primary: /home/li/primary/reports/{mind-design-status-2026-07-28.md,mind-deployment-proposal-2026-07-28.md,PersonaSpiritVsSpirit-2026-08-21.md,ActorLibraryNexusSkillReview-2026-08-21.md,NexusPriorArt-*-2026-08-19.md,YeggeOnAgents-2026-08-05.md}.
- Attention: /home/li/primary/flows/index.md; /home/li/.claude/projects/**/*.jsonl; /home/li/.codex/sessions/**/*.jsonl; scripts attention.py, typed.py, typed2.py in the scratchpad.
