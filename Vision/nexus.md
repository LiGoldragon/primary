# Nexus

## A Nexus is the whole

A Nexus is the whole long-running component: the process, its
sockets, and the signal contracts it is compiled with. Daemon is
retired as the name of the thing. Every Nexus is named
component-nexus — orchestrate-nexus, ethos-nexus — and in everyday
speech orchestrate-nexus is called orchestrate.

## A kind of thing

Nexus is our word for the style of component that speaks signal and
uses a similar database. A Nexus is a daemon, amongst other things;
the headings below say what else.

## Library and daemon

Every component built from now on is a Nexus. The nexus repository is
the library that defines the core of a Nexus component.

## Universal traits first

The basic ontology of an actor and dataflow system is designed before
implementation; signal and sema are designed against it as if new, the
old code at most inspiration.

## Processing is for the effect

An object enters a Nexus for the effect; the response follows as an
effect of it. Conversion is the wrong frame for it. The name is open,
Apply liked.

## Documents

The nexus and sema documents are undesigned; when they are designed
they live in the Nexus's main repository.

## Sockets

A Nexus opens at least two sockets. The ordinary socket serves
ordinary peers. The meta socket is privileged — the root user of the
Nexus — and configuration and privileged operations pass through it;
every Nexus has one, since without it nothing could configure the
Nexus. A Nexus that needs more levels of access opens more sockets.

## Default clients

A client is a separate program from the Nexus. For now the default
clients are packaged with the Nexus as separate crates of its
repository, which is a multi-crate repository: one datom-converting
CLI per socket, however many sockets the Nexus has, at least two. A
default client serves bootstrap first, then debugging and testing,
long after production has stopped using it. The meta CLI is named
component-meta.

## Signal only

Every client speaks to a Nexus in pure signal, fully binary. A Nexus
speaks only the signal contracts it is compiled with; two of these
are its own, one per socket. A Nexus thinks in typed values — enums,
structs, scalars — and the string fields it still carries are
records on the way to a fully typed form.

## The graph

A Nexus is a vertex in the graph of nexuses. An edge joins two
vertices and carries one contract. Every connected pair has an
ordinary edge; only some pairs have a meta edge. A Nexus is compiled
with the contracts of its own sockets and of every edge it has.

## Routing

Signals cross the network through a router. The router tells signal
types apart by an enum that wraps the objects, held in the signal
repository, which every component depends on. That repository also
holds what every signal needs in common — the handshake payload
among it.

## Configuration

A Nexus starts with no arguments and there is no bootstrap binary.
Its executable holds a default configuration as a constant. On start
it looks for its Sema database at the default location: a database
that exists holds the configuration; a database created new is
seeded with the defaults. The meta socket carries a Configure
interface, and changed values are accepted through it.

## First configuration

A Nexus keeps a standard metadata tree. In it a type records whether
the meta Configure was ever done; that record is reversed only on the
meta socket, and while it is unset Configure is accessible on the
ordinary socket. The tree holds everything standard about the Nexus:
its socket paths — its own and those of every edge-socket it connects
to — and whatever else comes up as standard nexus configuration data.
The built-in default configuration is independent of this and is
what gives the socket path on which the Configure signal arrives.

## Repositories

A component has three repositories: its main repository, holding all
its code, and two signal repositories — one for the ordinary
socket's contract, one for the meta socket's. Shared kinds go into
reusable libraries, which are encouraged.

## Why everything is a Nexus

Everything built from now on is a Nexus, and what was built in
another shape is rewritten as one. The consistency creates
reliability, quality, and clarity.

## Actors

The engine inside a Nexus is driven by Kameo actors. The standards
of their use are still to be designed. Arc-Mutex is permitted.

## Splitting a Nexus

A Nexus deals with a domain. When its features grow too many,
splitting one or more nexuses out of it is considered.

## Observation by subscription

State is observed by subscription: the subscriber receives the state
on open, then each change as it happens.

## Polling is forbidden

Polling is forbidden; a correct system goes quiet when nothing
changes.
