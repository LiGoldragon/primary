# Nexus — the name for what we called a Rust component (daemon + CLIs + signal)

## 2026-08-19 — a Nexus is the whole component; the Nexus part is its execution engine; two sockets, two CLIs, pure signal, compiled contracts; everything built is a Nexus

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

## 2026-08-19 — the Nexus part confirmed; the skill is renamed nexus; a nexus repo is wanted; the execution heart is Nexus Core; "signal contracts"; meta access is case by case; plural; the "why" goes to a parallel skill for psyche-facing flows

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

## 2026-08-19 — core-<component> was already killed; vertices if the word fits; at least two sockets; a default CLI client per socket; the nexus repo is a possibility; first design universal nexus traits from first principles; traits lines deployed

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

## 2026-08-19 — edge, not vertex, was meant; not every two vertices have a meta edge; edge could replace contract

Design session `e06e4c07`, typed (captured 2026-08-19T14:56+02:00),
after the Designer read "some vertices will not have the meta access"
as a property of the edge:

> re vertices: then I was trying to say edge. not all edges will have
> meta access (if we think of both socket as a single edge. said
> otherwise, not every two vertices will have a meta edge). We could
> use the word edge instead of contract.
