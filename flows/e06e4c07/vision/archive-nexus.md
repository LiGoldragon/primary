# Nexus — archived

## 2026-08-19 — edge, not vertex, was meant; not every two vertices have a meta edge; edge could replace contract

Design session `e06e4c07`, typed (captured 2026-08-19T14:56+02:00),
after the Designer read "some vertices will not have the meta access"
as a property of the edge:

> re vertices: then I was trying to say edge. not all edges will have
> meta access (if we think of both socket as a single edge. said
> otherwise, not every two vertices will have a meta edge). We could
> use the word edge instead of contract.

## 2026-08-19 — edge and contract both kept; the edge line approved

Design session `e06e4c07`, typed (captured 2026-08-19T16:47+02:00),
on the proposed line "A Nexus is a vertex in the graph of nexuses. An
edge joins two vertices and carries one contract: every connected
pair has an ordinary edge; only some pairs have a meta edge. A Nexus
is compiled with the contracts of its own sockets and of every edge
it has." — contract kept for the compiled vocabulary, edge for the
link between two vertices:

> the nexus line is good.

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
