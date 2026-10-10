# Distillation proposal: Vision/nexus.md (new), Vision/orchestrate.md (new), Vision/flowNexus.md (new)

Composed in flow acbb6006 from reports/distillCandidatesNexus.md
(records cited by their letter-number there). Each `##` is one
statement heading in the destination file. A statement lands only on
the living's explicit approval. Statements already carried by the
b675f3d9 proposals (ethos interfaces, anatomy, ethos-monolith) are
referenced, not repeated.

---

# Vision/nexus.md (proposed, new)

# Nexus

## A Nexus is the whole
Destination: Vision/nexus.md. From A2, A3, A7.

A Nexus is the whole long-running component: the process, its
sockets, the default CLI clients that speak to them, and the signal
contracts it is compiled with. Nexus is the word for it in every
name — Orchestrate Nexus, Ethos Nexus — and daemon is retired as the
name of the thing. The decision-making engine inside it is Nexus
Core, named as a heart is named within a body: speaking of the core
never excludes the rest.

## Sockets
Destination: Vision/nexus.md. From A2, A4, B1, B3, B4.

A Nexus opens at least two sockets. The ordinary socket serves
ordinary peers. The meta socket is privileged — the root user of the
Nexus — and configuration and privileged operations pass through it;
every Nexus has one, since without it nothing could configure the
Nexus. A Nexus that needs more levels of access opens more sockets.

## Default CLI clients
Destination: Vision/nexus.md. From A4, B2, A1.

Each socket has a default CLI client, written with the Nexus. The
CLI serves bootstrap first, then debugging and testing, long after
production has stopped using it. The meta CLI is named
component-meta.

## Signal only
Destination: Vision/nexus.md. From A2, F1.

Every client speaks to a Nexus in pure signal, fully binary. A Nexus
speaks only the signal contracts it is compiled with; two of these
are its own, one per socket. A Nexus thinks in typed values — enums,
structs, scalars — and the string fields it still carries are
records on the way to a fully typed form.

## The graph
Destination: Vision/nexus.md. From A5, A6.

A Nexus is a vertex in the graph of nexuses. An edge joins two
vertices and carries one contract. Every connected pair has an
ordinary edge; only some pairs have a meta edge. A Nexus is compiled
with the contracts of its own sockets and of every edge it has.

## Routing
Destination: Vision/nexus.md. From F2.

Signals cross the network through a router. The router tells signal
types apart by an enum, held in a universal signal repository every
component depends on, which wraps the objects. That repository also
holds what every signal needs in common — the handshake payload
among it.

## Configuration
Destination: Vision/nexus.md. From B5, B6.

A Nexus starts with no arguments and there is no bootstrap binary.
Its executable holds a default configuration as a constant. On start
it looks for its Sema database at the default location: a database
that exists holds the configuration; a database created new is
seeded with the defaults. The meta socket carries a Configure
interface, and changed values are accepted through it.

## Repositories
Destination: Vision/nexus.md. From H1, H2.

A component has three repositories: its main repository, holding all
its code, and two signal repositories — one for the ordinary
socket's contract, one for the meta socket's. Shared kinds go into
reusable libraries, which are encouraged.

## Everything is a Nexus
Destination: Vision/nexus.md. From C2, C4, C6.

Everything built from now on is a Nexus, and what was built in
another shape is rewritten as one. The consistency creates
reliability and raises quality and clarity.

## Actors
Destination: Vision/nexus.md. From E1, E3, E5.

The engine inside a Nexus is driven by Kameo actors. The standards
of their use are still to be designed. Arc-Mutex is permitted.

---

# Vision/orchestrate.md (proposed, new)

# Orchestrate

## The first Nexus
Destination: Vision/orchestrate.md. From D1, D4.

Orchestrate is the first Nexus: a simple component with an ordinary
and a meta socket that reserves paths, so that edit coordination has
dead-simple datom-syntax path reservation. The earlier Orchestrate
is discarded; nothing of it is sacred.

## Deployment
Destination: Vision/orchestrate.md. From D2, D3, D4.

Orchestrate is deployed unconditionally, in the home, for every
user. Its meta binary is part of it; a deployment without
meta-orchestrate is wrong.

## The skill
Destination: Vision/orchestrate.md. From D6.

The orchestrate skill covers ordinary operations only; meta
operations are outside it.

---

# Vision/flowNexus.md (proposed, new)

# Flow Nexus

## What it does
Destination: Vision/flowNexus.md. From I1.

The Flow Nexus sets up and starts a model flow: its working
directory, system prompt, training files and instruction prompt. It
takes the place of the abandoned training daemon.

## What its repository holds
Destination: Vision/flowNexus.md. From I2.

The flow repository holds the machinery of the Flow Nexus and a few
basic skills: our own take on how an agent behaves in a harness,
replacing the prompt the harnesses build in. The skills people use
with their system live in a separate repository.

---

# Carried by other proposals (not repeated here)

- F5–F8 (every wire interface in Ethos; imperative voice; observe as
  root; request redundant in the input slot) → b675f3d9
  reports/distillProposalEthos.md, Vision/ethosInterfaces.md
  "Imperative voice", "Sections confer"; and Vision/ethos.md
  "Document kinds and where they live".
- G1–G5 (ontology before implementation; universal nexus kinds;
  processing is for the effect; kinds declared explicitly; Apply
  liked, uncertain) → b675f3d9 reports/distillProposalKinds.md,
  Vision/anatomy.md and Vision/kinds.md.
- C3–C6 monolith-specific (go straight for a nexus; ethos-zero;
  trinity) → b675f3d9 reports/distillProposalEthos.md,
  Vision/ethosMonolith.md additions.

---

# Tensions surfaced — the living's ruling asked

1. **Core or kernel.** The psyche's words (A3, 2026-08-19) name the
   engine inside a Nexus "NexusCore". The reviewed Vision/
   ethosMonolith.md "Shape" says "distinct from the Nexus kernel,
   the runtime engine", and the nexus skill says "Nexus Kernel". No
   record of the living choosing "kernel" was found. This proposal
   writes Nexus Core; if kernel stands, ethosMonolith.md is right
   and this statement changes.
2. **Ordinary-socket Configure.** B6 calls it "a valid idea": a never-
   configured Nexus could offer Configure on its ordinary socket,
   refusing once configured. Not written as a statement — it was
   left as an idea. Open, or a statement?
3. **Nexus skill claims with no psyche record.** Four skill claims
   trace to no record: one capability one Nexus, sized to one mind;
   observation flows up through push subscriptions, authority flows
   down; no distributed rollback; polling forbidden. They are either
   unrecorded vision — then the living's word puts them in Vision —
   or skill invention.

# Vision impurities this distillation discards — the living's ruling asked

Working instructions found among the records this distillation
replaces. On approval they are destroyed, not archived.

- D7, flows/01a03eda/vision/orchestrateRealization.md — "looks
  good. implement and deploy": an approval utterance.
- flows/01a03d6e/vision/orchestrateDeployment.md, first record —
  the session opener asking for a situation summary and a
  deployment plan.
- D5 — the sequencing of skill and deployment changes ("wait for the
  new orchestrate to be deployed before we change the edit
  coordination skill …"): working instruction. The clause "you can
  change the Nexus skill right away" goes with it.
- D4's "just go ahead and deploy and replace the skill … plow that
  through": working instruction; the deployment decision itself
  (unconditional, in home, for all users) is kept as vision above.
- B7 — "we dont need to implement that now however": a deferral.
- E4 — "I want to dedicate a flow to the actor question … Distrust
  it all, including our fork": a working instruction with a
  judgement on existing code. The judgement is not carried; only
  the Kameo confirmation and the undesigned standards are.
- E2 — "I want to review the actor library we use, and if it is
  well documented in the nexus skill": working instruction.
- flows/01a03952/vision/orchestrateInPath.md — "propose docs/skill
  that assume this orchestrate is in PATH": a directive to future
  agents. Flagged by the gatherer; outside the records this
  distillation replaces unless the living includes it.
- flows/98fbfa47/vision/rustComponentArchitecture.md — "find the
  parts that are skill", "this is no high level explanation":
  skill-composition instructions. Same status as the previous.

# Not distilled (open)

- Actor standards of use (E5: "I just havent designed the standards
  of use").
- Universal Nexus kinds — designed, not yet spoken (G2).
- The effect verb (G5).

## Sources

- flows/acbb6006/reports/distillCandidatesNexus.md (record ids)
- Vision/ethosMonolith.md
- flows/b675f3d9/reports/distillProposal{Ethos,Kinds}.md
