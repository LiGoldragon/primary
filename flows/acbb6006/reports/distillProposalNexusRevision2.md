# Nexus distillation — revision 2 (after the living's rulings of 2026-08-27T14:40Z)

Landed on approval: Vision/nexus.md (Sockets, Signal only, The graph,
Routing, Configuration, Repositories, Everything is a Nexus, Actors),
Vision/orchestrate.md (Deployment, The skill), Vision/flowNexus.md
(What it does). Discarded on ruling: orchestrate.md "The first Nexus".
Raw-record archiving is held until the whole nexus cluster is ruled
(the impurity list shares files with the replaced records), then done
in one pass.

Re-presented with the living's modifications (vision/nexus.md of this
flow):

## Vision/nexus.md — "A Nexus is the whole" (first heading)

A Nexus is the whole long-running component: the process, its
sockets, and the signal contracts it is compiled with. Daemon is
retired as the name of the thing. Every Nexus is named
component-nexus — orchestrate-nexus, ethos-nexus — and in everyday
speech orchestrate-nexus is called orchestrate. The decision-making
engine inside a Nexus is Nexus Core.

## Vision/nexus.md — "Default clients" (after "Sockets")

A client is a separate program from the Nexus. For now the default
clients are packaged with the Nexus as separate crates of its
repository, which is a multi-crate repository: one datom-converting
CLI per socket, however many sockets the Nexus has, at least two. A
default client serves bootstrap first, then debugging and testing,
long after production has stopped using it. The meta CLI is named
component-meta.

## Vision/flowNexus.md — "Repository and skills"

The flow repository holds the machinery of the Flow Nexus and is a
runtime repository. Every skill lives outside it, the basic skills
included, so that a change to a skill causes no Nix rebuild. The
basic skills give our own take on how an agent behaves in a harness,
replacing the prompt the harnesses build in.

## Sources
- flows/acbb6006/vision/nexus.md (the rulings)
- flows/acbb6006/reports/distillProposalNexus.md (revision 1)

## Added after the 2026-08-27T14:40Z+ rulings

Ruled: Nexus Core (Vision/ethosMonolith.md corrected; nexus skill edit
dispatched). Ruled impurity: ethosMonolith.md "First fixture" removed.

### Vision/nexus.md — "First configuration" (after "Configuration"; proposed)
From the living's words in vision/nexus.md of this flow.

A Nexus keeps a standard metadata tree, in which a type records
whether the meta Configure was ever done; that record is reversed
only on the meta socket. While it is unset, Configure is accessible
on the ordinary socket. The built-in default configuration is
independent of this and is what gives the socket path on which the
Configure signal arrives.

### Vision/datom.md — "Reply shape": withdrawn
Ruled quackery. The 01a04339 record ("good enough for now" on
`Observed.Locks.[]`) stays raw until the nonempty layout is ruled.
