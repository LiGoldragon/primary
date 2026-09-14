# Vision Map — the living psyche's standing statements, as of 2026-09-14

Sources: Vision/*.md (distilled), flows/*/vision/*.md (raw), flows/*/notion/*.md (brainstorm, binds nothing), vision-raw/*.md (legacy raw), Intent/*.md (declared goals). Rule: later entry supersedes earlier on the same subject; notion rules nothing; distilled outranks raw only when not older than the raw statement. Quotes are verbatim, 1-3 sentences. bcd02a's live_claude_ingress output was not opened.

## Intent

No `Intent/*.md` file (anatomy, context, conversion, data, mandatoryTraits, protosParsing) addresses any topic below by name; they state cross-cutting goals only, not covered by the per-topic rule and not reproduced here.

# Architecture

## Nexus

**Current** — `flows/024bc7/vision/nexus.md`, "2026-09-13 — The nexus layer describes processes that are ongoing; they are actors":
> The nexus layer describes processes that are ongoing, like the operating system update operation or assistant call, basically something that has to lock. It's an actor. When you need something that locks, you get an actor because it has to be synchronous, so it's a process actor.

Same file, same date — "The signal layer, the nexus layer, and the sema layer are described in ethos; the database stores that namespace":
> You have the signal layer, the nexus layer, and the sema layer, and these are described in ethos. That's what that database is: it stores that namespace.

This 2026-09-13 raw material postdates and supersedes distilled `Vision/nexus.md` (approved 2026-09-11).

Superseded/older:
- [09-13] flows/6cc91b/vision/nexus.md — should a nexus have handled the pty injector; no Python
- [09-11] flows/fe34eb/vision/nexus.md — approval of Vision/nexus.md text ("Nexus is its name; daemon is not")
- [09-10] flows/fe34eb/vision/nexus.md — "no nexus core/kernel as a named part"; "a nexus is a daemon amongst other things"
- [09-09] flows/6cc91b, flows/564f55/vision/archive-nexus.md — "nexus core/kernel" (now superseded)
- [09-05] flows/1a6ca4/vision/archive-nexus.md — Flow Nexus starts flows via specialized-harness launches
- [08-23→08-31] flows/01a02fd5, flows/01a05487/vision/archive-nexus*.md — "all nexuses have a meta socket"; "nexus is a kind of thing"
- [08-27→08-29] flows/acbb6006, flows/db97561c/vision/archive-nexus.md — default clients per socket, "polling is forbidden"; Nexus as universal library, ethos-zero as daemon
- [08-26] flows/01a03d6e/vision/archive-nexus.md — no bootstrap binary; "the daemons are called Nexus"
- [08-19] flows/e06e4c07/vision/archive-nexus.md — Nexus as execution engine inside the whole (reversed 09-10)
- [08-11] flows/012fbf07/vision/archive-threeStacks.md — router-as-signal-sorter origin

Notions:
- notion: flows/bcd02a/notion/nexus.md — "a layer for storage... that's what the nexus objects are"

Contradictions:
- CONTRADICTION: archive-nexus.md (08-19, "Nexus part is the execution engine inside the whole") vs fe34eb/nexus.md (09-10, "no nexus core or kernel as a named part") — reversal, not mere refinement.
- CONTRADICTION: db97561c/archive-nexus.md (08-29, Nexus = universal library, ethos-zero = daemon) vs the prevailing framing before and after ("a Nexus is the whole long-running component itself").

## Signal

**Current** — `flows/024bc7/vision/signal.md`, "2026-09-13 — It's a request, not a configuration request; the root type of each definition is an enum":
> When you describe a signal ethos file, you're describing the requests and the responses... The root type of each definition is an enum. The structs represent an enum, and each thing can come in as an object.

Postdates and supersedes distilled `Vision/signal.md` (09-10 basis).

Superseded/older:
- [09-13] flows/bcd02a/vision/signal.md — parallel capture, same session
- [09-10] flows/6cc91b/vision/signal.md — "signal: portable rkyv + TBD protocol"; merge signal-standard/signal-frame into `signal`
- [08-14] vision-raw/signalIsOurMessagingLayer.md (+ flow copies) — ethos-file syntax anatomy, "signal is fully typed"
- [08-13] flows/6863ef19/vision/archive-signalIsOurMessagingLayer.md — CapnProto as "universal signal" (naming later abandoned, no explicit reversal found)
- [08-09] flows/98fbfa47/vision/archive-metaSignalNotOptional.md — "the metasignal is not optional" (still current in substance, folded into Vision/signal.md)

Notions: none found.

Contradictions:
- CONTRADICTION (soft): 08-13 "CapnProto = universal signal" vs 09-10 "signal = portable rkyv, no capnp" — no explicit reversal on record, the framing just disappears.

## Sema

**Current** — `flows/564f55/vision/archive-sema.md`, "2026-09-09 — sema is the database engine; its Ethos root type defines database record types" (matches `Vision/sema.md`, not superseded on this narrow point):
> Yes, SEMA is the database. When we create the SEMA Ethos type for the root type, like we have library and signal, then we're going to be defining database record types. Yes, SEMA is the database engine.

Superseded/older:
- [08-26] flows/01a03d6e/vision/archive-nexus.md — default Sema database location, init with defaults
- [08-14] flows/6329f1/vision/archive-ethos.md — sema ethos type has a storage/record type with associated kinds

Notions: none found.

Contradictions:
- CONTRADICTION (mild): 09-09 "sema = the database engine" vs the 09-13 tripartite framing in flows/024bc7/vision/nexus.md and flows/bcd02a/vision/runtime.md, which calls Sema "the storage part" of the runtime (Nexus=process, Sema=storage, Signal=requests/replies) — near-synonymous but a real ontology shift, not explicitly ruled as a correction.

## Router

**Current** — `flows/024bc7/vision/router.md`, "2026-09-13 — The router becomes the manifest; the enum is the router signal":
> The router has the orchestrate part, so the router becomes the manifest... The messenger can mean taking care of delivery of messages, whereas the router is deciding where this needs to go... That's the enum. That's where you get the enum from: the router signal.

Superseded/older:
- [08-13] flows/6863ef19/vision/archive-signalIsOurMessagingLayer.md — "routable signal" naming resolution
- [08-11] flows/012fbf07/vision/archive-threeStacks.md — router sorts signals via an enum in a shared signal repo (folded into Vision/nexus.md "Routing")

Notions:
- notion: flows/bcd02a/notion/router.md — identical 09-13 "router becomes the manifest" content, but filed as notion in this flow — the same utterance is classified as both standing vision and notion across two flows; flagged, not resolved.

Contradictions: none beyond the dual-classification flagged above.

## Storage

**Current** — `flows/024bc7/vision/storage.md`, "2026-09-13 — Every concept goes all the way through a process and somewhere where it is recorded in storage":
> Every concept is going to go all the way through a process and somewhere where it's recorded in storage, where some things can be maybe made more efficient in storage. That's what the nexus objects are.

Superseded/older: none — first appearance of this concept.

Notions:
- notion: flows/bcd02a/notion/nexus.md — identical content, filed as notion ("exploratory correspondence between process objects and storage; unfinished phrase")

Contradictions: none.

## Datom, Protos, Ethos

### Datom

**Current** — `Vision/datom.md` (distilled, landed 09-11, not superseded on Datom's general nature):
> Datom is the psyche's own coinage for the new data notation, the successor to NOTA and to the rejected name Dotos... data, strictly typed, super dense, no field names.

Narrower, later (09-12) — `flows/fe34eb/vision/datom.md`, "'logics' was Lojix: everything moves to the new datom, the stack, Horizon, Lojix, everything": "yes it was lojix."

Superseded/older:
- [09-09] flows/564f55/vision/datom.md — "another layer" (value/JSON-Value abstraction), explicitly retracted same file as not-vision
- [08-11] vision-raw/archive-datomSyntax.md — Datom carries data only, no generics; distilled into Vision/datom.md

Notions:
- notion: flows/564f55/notion/datom.md — "value layer"/"composable" naming brainstorm, explicitly ruled notion not vision

### Protos

**Current** — `Vision/protos.md` (distilled, landed 09-09, no later raw entry found):
> Protos is the name for the style all the dialects share... Protos is only about structure... A head in protos is just a head — anatomy, not interpretation.

Superseded/older: none beyond what the distillation already absorbs. Notions: none found.

### Ethos

**Current** — `flows/8325c1/vision/ethos.md`, "2026-09-13 — Understand the anatomy and the ontology of the system using ethos syntax" (postdates Vision/ethos.md's 09-11 landing):
> I really see a huge value in ethos in describing all of the types and all of the kinds... used in the implementation. Essentially, an implementation would be mostly a bunch of implementation blocks, whereas the traits would be generated by ethos kinds, and all of the types used would be specified in ethos as well.

Same file, same date, additive: "the action of copying the closure is an implementation on the type of the Nix closure... we should introduce the use of the ethos library in the Nexus" (trails off unfinished).

Foundational, still standing: `Vision/ethos.md` (landed 09-11) — "Ethos is the schema language... Ethos specifies the types and Datom fills them with data."

Superseded/older:
- [09-10] flows/fe34eb/vision/ethos.md — Ethos Zero is not a daemon; Ethos Monolith and Ethos Zero are the same thing
- [09-08] flows/564f55/vision/ethos.md — "ethos isn't about strings yet," explicitly retracted same file as not-vision
- [08-02] vision-raw/archive-ethosDotosDivisionAndHelp.md — Ethos/Dotos division, distilled into Vision/ethos.md
- [08-01] vision-raw/archive-ethosNonRepetitionLaw.md — "ethos will be the most terse non-repetitive syntax ever made"
- [08-23, distilled 09-10] Vision/archive-ethosMonolith.md — full monolith design, retired on landing

Notions: none beyond Ethos Delta (below).

Contradictions:
- CONTRADICTION: 09-08 "ethos isn't about strings" (ruled bad vision) vs 09-13 push toward Ethos describing "all of the types and all of the kinds... used in the implementation" — tension over descriptive scope, not resolved.

## Ethos delta

No standing (non-notion) material found.

Notions:
- notion: flows/024bc7/notion/ethosDelta.md — "we're going to submit the new Ethos Delta... the difference between the spec and the spec, so it's like a structured data diff, basically fully typed... I don't even know if we have the concept already" (09-13, framed by the flow as still-arriving)
- notion: flows/bcd02a/notion/ethos.md — duplicate of the above, plus the signal/nexus/sema-in-ethos quote (see Nexus)

Contradictions: none — consistent duplicates.

## Lojix

**Current** — `flows/024bc7/vision/criome.md`, "2026-09-13 — Criome takes over the authentication layer of Lojix":
> Criome should essentially take over the authentication layer of Lojix to deploy to have a root call on the host that needs to activate the operating system.

Companion, same date — flows/024bc7/vision/bootstrap.md: "You guys are in charge of bootstrapping this without breaking the system, so you make a clean Lojix nexus that, for now, uses SSH on Ouranos."

Superseded/older:
- [08-13/14] vision-raw/lojixOwnership.md — "it should only be in OS"; redeploy with only the newer Lojix daemon
- [08-10] vision-raw/mainForEverything.md — "use main for everything" (during Lojix recovery)
- [08-14–19] vision-raw/setupIndependentInterfaces.md — "the interface is lojix and meta-lojix CLI only," no flags
- [08-19→08-20] flows/01a01bac/vision/skillDesigning.md — "won't use a skill called lojix" reversed next day
- [08-23] flows/01a02b4b/vision/homeEquivalence.md — shared logic from Lojix-emitted Horizon output only

Notions: none found. Contradictions: none beyond the already-resolved 08-19/08-20 internal reversal.

## Criome

**Current** — `flows/024bc7/vision/criome.md`, "2026-09-13 — Criome takes over the authentication layer of Lojix":
> How the Criome eventually becomes the authentication for the update of the cluster using Lojix... to have a root call on the host that needs to activate the operating system.

Superseded/older: none — newly introduced 09-13.

Notions:
- notion: flows/6cc91b/notion/persona.md — "the persona is basically the root orchestrator... embedding Linux and having the bare minimum criome OS with its whole network stack, security, and sandboxing"

Contradictions:
- CONTRADICTION: naming instability — 024bc7/criome.md gives the corrected spelling "Criome" (from STT "CreoME"/"Crioome"); flows/6cc91b/vision/migration.md (same date) names the same referent "Creole" ("the meta cluster of Creole.NET... claiming the Creole TLD"); flows/6cc91b/notion/harnessPurity.md (same date) uses "Creo." Whether all three name one thing is unresolved.

## Network

**Current** — two same-date (09-13), complementary statements:

flows/024bc7/vision/network.md (also flows/bcd02a/vision/network.md, verbatim), "All the hosts connected through USB Ethernet, everybody wired together":
> I'm going to hook up Zeus to Prometheus through a USB Ethernet cable or something like that... I'll let you know when all the hosts are connected through a USB Ethernet and create a network where everybody is wired together.

flows/6cc91b/vision/network.md, "Tailnet identity-based network, IPv6 internal, any capable machine a gateway":
> We're going to have this tailnet identity-based network, super efficient, IPv6 internal, with intelligent subnet/subnetworks with IP4 to IP6 on the gateway server. Anybody can be a gateway that has enough features.

Superseded/older: none found. Notions: none found.

Contradictions: none in content; flagged only for being split/duplicated across three flow dirs (024bc7, bcd02a, 6cc91b) with no cross-reference.

## Sandbox

**Current** — two same-date (09-13) statements, both filed as vision:

flows/6cc91b/vision/sandbox.md, "A sandbox is a reserved branch of a tree, named by the short sentence that describes what this is about":
> When you create a sandbox, you create a reserved branch of a tree... This flow is a composition, which we call a harness today in the thinking machine world, and we already have a reality with our flow-based memory system, which is basically what this is.

flows/024bc7/vision/sandbox.md, "A harness component described anatomically; a full sandbox on Prometheus with virtual machines; the token in an encrypted volatile throwaway key":
> Just start a full sandbox. You can use Prometheus... I lock the keys into an encrypted, volatile, throwaway key, right, with only the process that needs the token having it.

Notions:
- notion: flows/bcd02a/notion/sandbox.md — identical Prometheus/VM/token content, but filed as notion here, flagged by that flow itself as "design questions... not evidence of a supported cross-host login mechanism"

Contradictions:
- CONTRADICTION: the identical Prometheus/VM/token quote is standing vision in 024bc7 and non-binding notion in bcd02a — authority disputed between the two flows' own classification, unresolved.

## Bootstrap

**Current** — `flows/024bc7/vision/bootstrap.md`, "2026-09-13 — A clean Lojix nexus that, for now, uses SSH on Ouranos":
> You guys are in charge of bootstrapping this without breaking the system, so you make a clean Lojix nexus that, for now, uses SSH on Ouranos. You could even change Ouranos's name to be more Latin... can you put that in your dictionary?

Superseded/older: none found. Notions: none found. Contradictions: none.

## Harness purity

**Current** — `flows/6cc91b/vision/agentAuthentication.md`, "2026-09-13 — Messaging and spawning authenticated at multiple layers, controlled by more highly permissioned nexuses":
> Every harness runs in its own sandbox, which is why I was referring back to this purity... We can enforce that even at the system operating system layer, where the whole messaging layer and spawning new harnesses layer would be authenticated at multiple layers, sandboxed, and controlled by more highly permissioned nexuses.

Superseded/older: none found.

Notions:
- notion: flows/6cc91b/notion/harnessPurity.md — "with the Nix, we're going to go pure... make the harness basically pure through the Creo. Everything is going to authenticate through the Creo multi-key system, and it's going to create these personal clusters" (source of the term "purity" referred back to above)

Contradictions: none beyond the Criome/Creo/Creole naming instability flagged above.

## Migration

**Current** — `flows/6cc91b/vision/migration.md`, "2026-09-13 — A migration system; the meta cluster of Creole.NET; claiming the Creole TLD":
> We should have a migration system also. Start setting up a migration system, like the meta cluster of Creole.NET, which is what I own, right? I'm claiming the Creole TLD.

Superseded/older: none found. Notions: none found.

Contradictions:
- CONTRADICTION: this entry's "Creole" vs criome.md's corrected "Criome" — same day, unresolved whether same referent (see Criome).

# Agents

## Paired flows

**Current** — `flows/6cc91b/vision/pairedFlows.md`, "2026-09-14 — Send him direct prompts, not intercom messages":
> You should be sending him prompts, like direct prompts. Why are you using these agent intercoms? What is this agent intercom doing?

Same file, same date: "Codex does the scripting": "You should get Codex to do all that stuff. The scripting and stuff, he's better at it."

Foundational, still standing — flows/024bc7/vision/parallelSessions.md, "A paired flow between Claude and Codex; a third, the most doubtful open-source model":
> We're going to have to add this flow concept of a pair session, a paired session, a paired flow between Claude and Codex. Maybe we're probably going to introduce a third one, the most doubtful open-source model.

Superseded/older (context):
- [09-13] flows/6cc91b/vision/pairedFlows.md — pass what psyche says to Codex via a note at every main message (narrowed by 09-14's "direct prompts")
- [09-13] flows/024bc7/vision/parallelSessions.md — send same prompt to the pair marked by harness; a waking system; re-bootstrap from a remember-first prompt
- [09-13] flows/bcd02a/vision/paired-flows.md — Codex-side parallel witness of the same session

Notions: none. Contradictions: none — bcd02a and 024bc7 are consistent parallel witnesses.

## Council

**Current** — flows/024bc7/vision/parallelSessions.md, "The council: three agree to push to production, two to implement the proof of concept":
> The three have to agree to push something into production, but only two have to agree to implement the proof of concept.

Superseded/older: [09-13] flows/bcd02a/vision/council.md — same ruling, parallel witness. Notions: none. Contradictions: none.

## Effort

**Current** — flows/024bc7/vision/effort.md, "High effort is a waste; right now we are in medium mode":
> From now on, high effort is kind of a waste... I will say we'll have a protocol go into high effort mode... but we're going to try to avoid that. If my quotas are running out... then we can go into high effort. Right now, we're in medium mode.

Same file, same date: "keep track of quotas; a thread rolling on Prometheus with the most doubtful model."

Superseded/older (context):
- [09-08] flows/5851f4/vision/subagents.md — three roles both sides, all medium effort (Haiku/Sonnet/Opus and Luna/Terra/Sol — STT wrote "Soul," corrected to "Sol")

Notions: none. Contradictions: none — 09-13 policy and 09-08 role list are consistent.

## Messenger

**Current** — flows/6cc91b/vision/messenger.md, "Whatever message is called, Messenger or the noun, use that for the messaging":
> The message was also slated to be called Messenger... orchestrate was to become orchestrator, but it looks like we've been leaning more towards the noun lately... Whatever it is called, we should use that for the messaging.

Same file, same date, additive: "a hook that sends my prompt to the other harnesses"; "a small model runs the open-source harness with a really simple job: the messaging"; "talk through Claude; the messenger tells the other half" ("you should work with Codex now and implement this messenger open-source specialized job that gets triggered").

Superseded/older (context):
- [08-09] flows/019fe728/vision/agentIntercom.md — "two stacks: Agent Intercom (third-party, use now)" vs "Messenger and Orchestrator (mine, not ready)" — superseded on "use intercom for now" by pairedFlows.md 09-14

Notions: notion: flows/bcd02a/notion/router.md — router vs. messenger distinction. Contradictions: none — naming ambiguity is the psyche's own open question, not a source conflict.

## Typed prompts

**Current** — flows/6cc91b/vision/typedPrompts.md, "Typed prompt detection: variant, separator, payload, specified in Ethos as Datom":
> You're going to have an enum, and the first thing in every message is going to be the variant. If it's typed, you're just going to see the variant, and then a separator, and then the payload... We're using Datom, so you specify it in Ethos.

Superseded/older: none on this subject. Notions: none. Contradictions: none. [context]

## Relay

**Current** — flows/6cc91b/vision/relay.md, "2026-09-14 — Six characters each end is enough; the tool lives outside the flow directory":
> You don't need so many words... I said 6, and you used like 60 or something, so 12 will be enough because the script should only search user prompt input... you should put that tool somewhere other than in the Flow ID directory.

Superseded/older: [09-13] flows/6cc91b/vision/relay.md — original: relay by matching a few characters in the transcript, not by re-emitting it. Notions: none. Contradictions: none. [context]

## Transcript extraction

**Current** — flows/6cc91b/vision/transcriptExtraction.md, three same-date facets, none superseding:
> If there was a specialized call with a Luna extractor that could intelligently decide what's relevant... a little bit of narration in between raw things that either the thinking machine said, or the psyche said, or that one of the subflows said.
> The extractor would also maintain objectivity to report everything and not hide any details that could be important... except if it's basically a user input error, like a mistake.
> I think even the extraction there could fix typos that speech detects, that even the agent might have acknowledged... or that are highly likely to have just been missed or to have been understood by the flow but not even mentioned.

Superseded/older: none. Notions: none. Contradictions: none. [context]

## Agent authentication

**Current** — flows/6cc91b/vision/agentAuthentication.md, two same-date complementary facets:
> It was supposed to check which process was actually using the tool. Essentially, we could authenticate or secure the layer between agents to a pretty high degree, even on the computer itself.
> We can enforce that even at the system operating system layer, where the whole messaging layer and spawning new harnesses layer would be authenticated at multiple layers, sandboxed, and controlled by more highly permissioned nexuses.

Superseded/older: none on this narrow subject (related: criome.md's OS-deploy auth, see Criome). Notions: notion: flows/6cc91b/notion/harnessPurity.md — Creo multi-key auth, personal clusters; notion: flows/bcd02a/notion/sandbox.md — copying subscription tokens into a sandboxed VM under an encrypted throwaway key. Contradictions: none.

## Session archiving

**Current** — flows/6cc91b/vision/sessionArchiving.md, "Garbage collect sessions, keep the important parts of the exchanges":
> Let's talk also about garbage collecting sessions and sort of archiving them, and just keeping the important parts of the exchanges, like the main responses and the most important parts of the prompts and the final responses of the agent flows.

Superseded/older: none. Notions: none. Contradictions: none. [context]

## Orchestrator

**Current (naming)** — flows/6cc91b/vision/messenger.md, same quote as under Messenger: "orchestrate was to become orchestrator, but it looks like we've been leaning more towards the noun lately."

**Current (stack identity)** — flows/019fe728/vision/agentIntercom.md, 08-09: "There's two stacks here... one is the Agent Intercom, which is not from me... and then there's the other stack, which is Messenger and Orchestrator, which are not ready to be used yet, which is from me."

Distilled `Vision/orchestrate.md` (undated) covers only the deployed "Orchestrate" skill/meta-binary, a different narrow subject, not date-comparable.

Notions: notion: flows/6cc91b/notion/orchestrator.md — maybe the orchestrator manages flows, unspecified ("you just made it up"); notion: flows/6cc91b/notion/persona.md — persona as "root orchestrator, system D"; notion: flows/bcd02a/notion/router.md — router/orchestrate/messenger correspondence.

Contradictions: none flagged; the naming question (orchestrate/orchestrator/"the noun") is left open by the psyche itself.

## Persona

**Current** — flows/1a6ca4/vision/personaMetaHarness.md, "2026-09-05 — the wild west phase of thinking machines; the persona meta-harness brings the dawn of complete thinking machine systems":
> That phase is like the wild west phase of thinking machines, and the persona meta-harness is going to bring in the dawn of the more complete thinking machine systems, which will be a complex infrastructure of a kind of thinking machine legal system interworking apparatus.

Also standing (different facet) — flows/15b67974/vision/persona.md, 08-21 (typed): "That repo hasn't been touched in a long time, even though it's slated to orchestrate the entire meta harness (called persona)."

Related: see Soul — "it's like the private part of the persona."

Superseded/older:
- [08-10/11] vision-raw/gradientsOfAuthority.md — pre-persona-meta-harness framing ("until we design the meta-harness (persona) properly")
- [08-17] flows/358f143a/vision/workspace20.md — role skills hold the awareness seat "for now"
- [legacy, undated] vision-raw/persona.md, vision-raw/spiritComponentAndFile.md — superseded by dated flow entries above

Notions: notion: flows/6cc91b/notion/persona.md — root orchestrator/"system D," embedded-Linux "criome OS" (hedged: "maybe I went off the hook there"); notion: flows/bcd02a/notion/persona.md — duplicate of the Soul entries below, filed under Persona.

Contradictions: none flagged.

## Soul

**Current** — flows/024bc7/vision/soul.md, "The private layer, the soul, the private part of the persona":
> People have their own cluster, their own thinking machine system, personalized to them. We're going to create this private layer, the soul, basically... It's like the private part of the persona.

Same file, same date: "The Soul runs on everything, ruled by a kernel process on a dedicated machine": "It's going to be ruled by a kernel process that runs... you can pick a private provider, even in the cloud."

Superseded/older: none. Notions: notion: flows/bcd02a/notion/persona.md — near-verbatim duplicate, same date. Contradictions: none. (Excluded as homophones: "Sol" the model role; "Book of Soul.")

## Third model

**Current** — flows/024bc7/vision/thirdModel.md, "Bootstrap the big open-source model; pick it and its provider on goodwill in privacy and security":
> We're going to have to figure out which model we want to pick and where we're getting provider-provided API access for this open source model... which one has good goodwill in terms of privacy and security.

Same date, companion — flows/024bc7/vision/parallelSessions.md: "Maybe we're probably going to introduce a third one, the most doubtful open-source model. Let's find it and pair it... it's going to be our third model backend."

Superseded/older: none (facets, not supersession). Notions: notion: flows/bcd02a/notion/models.md — duplicate of the "third model backend" line. Contradictions: none.

## Open-source harness

**Current** — flows/6cc91b/vision/openSourceHarness.md, "Different models for different things; the most doubtful model; the right harness makes any model":
> Maybe we run different models for different things... they've shown already... if you do the harness right and you give the right ontology and guidance, you can make any model in the right harness, essentially, by going through a process which we've started to do.

Same file: "the best open-source stack with remote control": "what is the best open-source stack with remote control, essentially the open-source Claude and Codex with a remote control solution?"

Superseded/older: none. Notions: notion: flows/bcd02a/notion/models.md — overlaps. Contradictions: none.

## Speech-to-text

**Current** — flows/024bc7/vision/speechToText.md, "Host our own speech-to-text, personalized, post-trained on my voice":
> We need to host our own speech-to-text. Wispr is a bit dumb. We need to integrate the speech-to-text into our own system to improve the voice model to recognize my voice because it's going to be personalized. We're going to post-train our own model and run them locally or in the cloud.

Related, same date — flows/024bc7/vision/soul.md: "we're also going to run these speech-to-text models on Prometheus that we're eventually going to train on our own speaking and data, personally me and Bird."

Superseded/older:
- [09-02] flows/b2da01/vision/wisprFlowService.md — rely on paid Wispr Flow rather than build a replacement (superseded on this point by 09-13 "host our own")
- [08-08] flows/019fe121/vision/dictationVocabulary.md — vocabulary tuning for STT
- [undated] flows/01a04e75/vision/listenerWisprFlow.md — provider fallback abstraction, eventual "our own Wispr server" [context]

Notions: notion: flows/bcd02a/notion/speech.md — duplicate + add Ouranos/Uranus to dictation vocabulary; notion: flows/753090/notion/speech-to-text.md — "our first big selling feature for a service that I'm going to start."

Contradictions: none direct — 09-02 "use paid Wispr" superseded by 09-13 "host our own" by date.

## Web chat transcripts

**Current** — flows/024bc7/vision/webChatTranscripts.md, "Check my web chat transcripts periodically through the browser, on Ouranos":
> I want you guys also to figure out a way to start checking my web chat data transcripts... by accessing the web app in the browser, to check my new data once periodically... on my laptop, Ouranos.

Related, same date — flows/024bc7/vision/thirdModel.md: "I've been talking about stuff like that in my actual ChatGPT online, like web access, like the chat area."

Superseded/older: none. Notions: notion: flows/bcd02a/notion/web-conversations.md — same-date near-duplicate, spells the host "Uranus." Contradictions: none — only the host-name spelling differs, flagged in both files.
