# Nexus

## Clients are packaged with the nexus, as separate crates: a datom-converting CLI per socket

2026-08-27T14:40:26Z, the psyche, typed, on the proposed Vision/nexus.md statement "A Nexus is the whole" (reports/distillProposalNexus.md), quoting "the default CLI clients that speak to them,":

> no, the clients are not the nexus. for now, default clients are packaged with the nexus, so they should be separate crates (multi crate repo), in the form of a datom-converting cli for each socket (however many sockets that nexus has; minimum 2)

On the statement "Default CLI clients", quoting "CLI client, written with the Nexus.":

> see above

## In everyday speech orchestrate-nexus is called orchestrate

2026-08-27T14:40:26Z, the psyche, typed, quoting "Nexus is the word for it in every name — Orchestrate Nexus, Ethos Nexus":

> in everyday speech, orchestrate-nexus will be called orchestrate, etc

## The heart sentence is quackery

2026-08-27T14:40:26Z, the psyche, typed, quoting "speaking of the core never excludes the rest.":

> this is quackery

## The "first Nexus" statement is discarded

2026-08-27T14:40:26Z, the psyche, typed, quoting the proposed Vision/orchestrate.md statement "Orchestrate is the first Nexus:":

> not necessary; discard

## Skills live outside the runtime repository

2026-08-27T14:40:26Z, the psyche, typed, quoting the proposed Vision/flowNexus.md statement "The flow repository holds the machinery of the Flow Nexus and a few basic skills:":

> no, the skills will be outside the runtime repo, otherwise modifying a skill will result in a nix rebuild.

## Everything up to that point not commented on is approved

2026-08-27T14:40:26Z, the psyche, typed:

> everything up to the last point I commented on which  I didnt comment on is approved. represent it with my modifications, and reconsider the rest and represent it as well

## The engine inside a Nexus is Nexus Core

2026-08-27T15:20:37Z, the psyche, typed, on tension 1 (Nexus Core, the psyche's 2026-08-19 words, against "Nexus kernel" in Vision/ethosMonolith.md and "Nexus Kernel" in the nexus skill):

> 1. core

## First configuration: a standard nexus metadata tree records whether meta Configure was ever done

2026-08-27T15:20:37Z, the psyche, typed, on tension 2 (Configure on the ordinary socket of a never-configured Nexus):

> 2. its a valid concept. standard nexus meta-data tree which has a type to know if the meta configure was ever done, which can only be reversed on the meta socket. if unset, the ordinary socket configure is accessible. this is independant of the builtin default configuration, which are needed since otherwise we wouldnt have a socket path to even fall back on to even allow the configure signal to come in.
