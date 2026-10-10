<!-- to-the-living:start -->
Presentation.{ «How Message's meta socket knows its owner» }

## The case

Message has an ordinary socket and a meta socket. Message's buildable design admits to the meta socket only a process that runs in no flow, which it calls the owner, and drops the list of aspects that the current Message source admits beside the owner, seeded with Psyche (astra-runtime.md:20, citing message-design.md:124-127 and 687-688). The design marks that choice as its own inference, not a ruling. It names no mechanism by which Message knows the owner. "Runs in no flow" can only be read as Flow answering that it cannot identify the caller, the same answer Flow gives a side job or the living's terminal; that is the absence of a match, not an identity (astra-runtime.md:21). The only positive bound is the kernel's: both sockets are open to one Unix user alone. The design also leaves unsaid whether a meta configuration is admitted while Flow cannot be reached, which the current Message source allows so a wrong Flow path can be repaired (astra-runtime.md:22). Flow's own design keeps its list of admitted aspects, so the two designs differ (astra-runtime.md:23). These are the readings of the flow that wrote astra-runtime.md, not observed here. Message and Flow as designed are in development, none of it in production. The living's records call the meta socket the root user of a Nexus and want a caller known by its process, never by a claim; none of them says how the root user is recognised. One record finds the sender called "owner" absurd. This proposal states it for every Nexus, since the meta socket is defined there and the two designs would then agree; that widening is this flow's inference.

## Distillation

### D1. How a Nexus knows the owner of its meta socket, in vision-nexus

Target: `psyche-skills/skills/vision-nexus.md`, a new section after «Sockets» (line 38-44) and before «Default clients» (line 46). The section before it stands as: A Nexus opens at least two sockets. The ordinary socket serves ordinary peers. The meta socket is privileged — the root user of the Nexus — and configuration and privileged operations pass through it; every Nexus has one, since without it nothing could configure the Nexus. A Nexus that needs more levels of access opens more sockets. The section after it begins: A client is a separate program from the Nexus. Nothing is removed; one section is added, and its source lines are appended under «Sources».

**Option (a), the Unix user and the socket mode alone.**

Added, under the heading «The meta socket's owner is its Unix user»: The meta socket is open to the Unix user that runs the Nexus and to no other. Any process of that user is the root user of the Nexus; the Nexus asks no other Nexus who the caller is, and is configurable while every other Nexus is down.

Sources added: 1b8ac0 messaging.

Rests on: psyche-skills/skills/vision-nexus.md:40-44 (distilled), the meta socket as the root user of the Nexus; flows/1b8ac0/vision/messaging.md:7 (2026-09-21, raw, heard by 1b8ac0), on exposing the meta socket to everybody for now as the unsafe interface, with :18 (same day) narrowing everybody to local only. The same file at :27 (same day) says raw is on meta, so it's not usually accessible, which sits against "everybody"; whether "for now" still holds is unknown. Reading the Unix user as the whole bound is this flow's inference. flows/e06e4c07/vision/gradientsOfAuthority.md:9-14 (2026-08-19, raw) says there is no magic way for a computer to know its input is from a psyche; at :23-27 (same day) the living rejected a behavior line drawn from it as taking the example too literally, so it is not cited as support. That the current Message source bounds its sockets this way is the claim of astra-runtime.md:21, not observed here.

**Option (b), the living's terminal registered as a known identity in Flow.**

Added, under the heading «Flow knows the living's terminal»: The living's terminal is registered in Flow as an identity of its own. A Nexus learns the caller of its meta socket from the calling process, as it learns any caller, and asks Flow; Flow answers with the living's identity, and only that identity is the root user.

Sources added: efa157 callerIdentity; 93ba9f callerIdentity; 93ba9f messagingInterface.

Rests on: psyche-skills/skills/vision-nexus.md:56 (distilled), a Nexus knows its caller by the process, never by a claim; flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/callerIdentity.md:7 (2026-09-16, raw, heard by efa157; no copy found at flows/efa157), on the Nexus checking the socket's process and Flow knowing which process belongs to which flow; flows/93ba9f/vision/callerIdentity.md:5 (2026-09-26, raw; relayed copy at flows/b7ba00/vision/callerIdentity.md:7), on the CLI giving the calling process so the Nexus asks Flow and knows its origin without anyone saying who they are; flows/93ba9f/vision/messagingInterface.md:23 (2026-09-26, raw), on the sender being called "owner" being ridiculous and Message figuring out the sender from the calling process. No record names the living's terminal as an identity in Flow; that extension is this flow's inference. Under this option a meta configuration needs Flow to answer, which leaves the repair of a wrong Flow path open; that consequence is this flow's reading.

**Option (c), a credential the meta CLI holds.**

Added, under the heading «The meta CLI carries a credential»: The meta CLI holds a credential that no flow can read, and carries it in every meta request. The meta socket admits a request that carries it and refuses one that does not; Flow is not asked.

Sources added: 9993b5 callerIdentity; e1953c secrets.

Rests on: flows/9993b5/vision/callerIdentity.md:7 (2026-09-17, raw), on making sure it was that exact executable that ran and being thorough with security; psyche-skills/skills/vision-nexus.md:53-54 (distilled), the meta CLI named component-meta; flows/e1953c/vision/secrets.md:7 (logged 2026-09-14, heard date not read, raw), on the public part not being trusted with tokens. flows/bcd02a/notion/sandbox.md:15 (2026-09-13) is a notion: only the process that needs a token holds it, said of subscription tokens in a sandbox. Whether a carried credential counts as a claim, which vision-nexus.md:56 excludes, is unknown. That the 2026-09-17 words reach a credential rather than a check of the executable is this flow's reading, and keeping it from the flows that run as the same Unix user is a mechanism no record names.

**Option (d), Psyche aspect flows admitted as before.**

Added, under the heading «The psyche cluster holds the meta socket»: The meta socket admits a process that runs in no flow and the flows of the aspects its configuration lists, Psyche by default. A Nexus learns the caller's aspect from Flow.

Sources added: da1e3f operational-psycheAndMind; 88475f message.

Rests on: flows/da1e3f/vision/operational-psycheAndMind.md:17 (2026-09-17, raw, logged as operational), on only the psyche cluster using the meta socket, not enforced for now but the only cluster instructed to; flows/88475f/vision/message.md:63-65 (2026-09-25, raw), on Message's features on the meta socket and exposing interfaces at whatever authority level they need. The 2026-09-17 words speak of the meta psyche socket and then the meta socket; whether they cover every Nexus is unknown. That they ask for enforcement now is not said, and reading them as an admission rule is this flow's inference. Message's design drops this list (message-design.md:124-127), as its own inference.

**Ruling D1.** (a) The Unix user alone. (b) The living's terminal known to Flow. (c) A credential the meta CLI holds. (d) Psyche flows admitted as before. (e) Amend, by line, including a move to vision-messaging if it is Message's alone.

## Voice

One choice. Message's meta socket lets in only "the owner", but nothing says how it recognises you. A says your Unix user is enough. B has Flow know your terminal, so Message asks Flow who called, the way you want every caller known by its process. C gives the meta CLI a secret flows cannot read. D lets Psyche flows in beside you, as the current Message code does. Which one? This flow's reading: no record of yours says how the root user is recognised, B and D stop working when Flow is down, and you called the word "owner" ridiculous for a sender.
<!-- to-the-living:end -->
