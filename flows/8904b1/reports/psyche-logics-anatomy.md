# Psyche on logics, deployment, and nexus anatomy

Searched under: Logics, Logos, Lojix/Logix, logistics; Zeus, Prometheus; Nexus,
Flow Nexus, Message Nexus, Psyche Nexus, Mentci; Ethos, Ethos signal; Herder/Herdr;
token cost, waste, overnight. Corpus: `Vision/`, `Intent/`, `vision-raw/`,
`flows/*/vision/`, `flows/*/notion/` (including archive- files).

## 1. Logics: what it is, deployment, hosts, Nix, SSH, Home, activation, rollback

The seed record for this whole inquiry, Notion, speech-to-text:

> Now I feel like we need to reopen the conversation about the base of our system: logics and deployment. It seems that it's really hard. I've been asking for Zeus to be updated for days now and even after millions of tokens were spent overnight, that wasn't even done. I feel like I went too fast, logics is a piece of shit, and I never actually took the time to make a quality Nexus out of this with you.
>
> In the same sense I think for logics we need to break it down so that we maybe have a Nix interface or an SSH interface or something. This is Notion. This is not a vision.

-- psyche, STT, 2026-09-27, Notion, `flows/8904b1/notion/anatomy.md`.

"Logics" (STT) was ruled to be **Lojix**, distilled, `flows/fe34eb/vision/datom.md:11-13`:

> everything is going to move to the new datom ... All of the stack, the horizon, logics, everything is going to move to the new datom, and we're going to start migrating everything that uses datom, which means everything, to the new datom as we go along.

-- psyche, mode not stated, 2026-09-12 origin (flow 542442), confirmed as Lojix by flow fe34eb, `flows/fe34eb/vision/datom.md`, `flows/542442/vision/archive-datom.md`.

Lojix as a deploy tool, doubted, speech, `flows/01a02b46/vision/zeusUpdate.md:29`:

> And find out, yeah, logics, O-J-I-X is the deploy tool, but it might not work properly.

-- psyche, STT, undated in file (flow 01a02b46, chain dated 2026-08-08).

Nexus/Nix boundary for Lojix, Vision (distilled from living), `flows/e1953c/vision/nexus.md:25`:

> Lojix shells out to Nix. That's Nexus. Nexus encapsulates processes ... it maintains a sort of API around the CLI that wraps this Nexus process, like a Nix build, right? It is a Nexus process, maybe of the logics for now, but eventually we could put that into Forge.

-- psyche, mode not stated, `flows/e1953c/vision/nexus.md`.

Cluster/logics coupling, `flows/e167d8/vision/clusterSpec.md:7`:

> let's write the spec in Ethos for the object that comes in because it's going into a [Rust] program anyway ... let's make that a signal contract, a signal repo, so that logics can pick that up and it's able to talk about cluster data.

-- psyche, mode not stated, `flows/e167d8/vision/clusterSpec.md`.

Deployment vision (distilled, undated), `Vision/deployment.md`:

> A proof of concept is worked on and deployed on the host the flow is running on. Another host is used only when the living names it. ... Zeus is a stable node, and stable nodes are not where testing happens.

Constant redeployment, STT, `flows/b860be/vision/deployment.md`:

> Well has Zeus been redeployed and updated? It should be. I gave the instruction but we can redeploy it too if things have been fixed. Like I said I want to start doing constant redeployment when I declare the environment that we're testing to be usable, right? Then we can deploy `main` on the rest of the network.

-- psyche, STT, 2026-09-26 ~09:00, to e167d8, relayed to b860be, `flows/b860be/vision/deployment.md`.

Roll forward, not rollback, typed, `flows/d8df70/vision/deployment.md`:

> I don't understand what you think we need to do before deploying. What do you mean, roll back? Roll back to what? We have nothing now. We're rolling forward. There's no rolling back because if we roll back we fall off the cliff. Let's go deploy.

-- living, typed (mode "not established" in source), 2026-09-24, to Psyche Medium d8df70, `flows/d8df70/vision/deployment.md`.

Conflicting record: a **cancelable countdown rollback** was wanted for major/breaking changes, typed, `flows/05c604/vision/deployment.md`:

> If you do anything major, have an automatic countdown rollback on some of these really big, potentially breaking things so that we can recover potentially. If you can come back online on that new stack, you can cancel it ... "Okay, we have internet. Remote access seems to work. Let's just stop the countdown, and we stay on the new stack."

-- psyche, typed, date not stated in file (flow 05c604), `flows/05c604/vision/deployment.md`. This does not contradict d8df70's "no migration rollback" (old stores) — it is a safety countdown on a breaking network/host change, not a return to an old store.

"Logic Meta" permission, typed, `flows/d8df70/vision/deployment.md`:

> Yeah of course you have permission to use Logic Meta. Why wouldn't you have permission to do that? I told you to deploy Prometheus so now you're asking me to repeat myself.

-- psyche, typed, 2026-09-24, `flows/d8df70/vision/deployment.md` (reconstructed by 752e0f from transcript).

SSH/Nix transfer detail for Zeus activation, STT, `flows/01a02b46/vision/zeusUpdate.md:78-92` and `flows/01a030b7/vision/zeusUpdate.md:7`:

> zeus should resolve now but prefer 192.168.18.95 for now, which is a direct ethernet route, will be much transfer to transfer the nix paths
>
> after the nix paths are moved zeus.goldragon.criome is fine for activation/etc
>
> Then resume the zeus update. use its ethernet LAN ip address 192.168.18.95 if you need to move nix paths to it (yggdrassil is over wifi and will be very slow and heavy, but it's fine for activation and other non-heavy transfers usage)

-- psyche, mode not stated, `flows/01a02b46/vision/zeusUpdate.md`, `flows/01a030b7/vision/zeusUpdate.md`.

No record found of the living naming a "Home" component directly under Logics; "Home" appears only as "criome home" (the user-environment repository), e.g. `flows/1f96fc/vision/fieldMaintenanceAndRefresh.md:16` ("upkeep on criome and criome home"). No verbatim SSH-interface-for-Logics design beyond the Notion line above was found; searched spellings Logics/Logos/Lojix/logistics across all listed trees.

## 2. Zeus and Prometheus: what was asked, and when

> we need to fix Zeus's VS code so that my friend can keep working

-- psyche, mode not stated, 2026-08-08, `flows/019fe121/vision/hostEnvironmentRecovery.md`.

> So then once we got all that lined up, we need to redeploy Zeus on the latest version. ... Let's figure out how we're going to redeploy Zeus. If we have to use a hacky way to do it, then we're going to have to use a hacky way to do it. We have root access on all my hosts.

-- psyche, mode not stated, 2026-08-08, `flows/01a02b46/vision/zeusUpdate.md`.

> This is the living and I'm giving the order and the authority to deploy an update to Zeus and also to fix its location ... I don't think the update's gone through. I've been asking for 2 days to update Zeus so I want this to get through. Right now I want you to not stop until Zeus has been updated and the same with Prometheus.

-- psyche, mode not stated, 2026-09-25 (session dated), `flows/b7da5d/vision/hostUpdates.md`.

> I want the deployment to go through but I also want the improvement design to go forward so that next time the deployment is better. I want the deployment now. I want Zeus updated and I need its location fixed at least temporarily if it needs to be overridden.

-- psyche, `flows/b7da5d/vision/hostUpdates.md`.

> While you do that, re-update Zeus on our cluster Gold Dragon and just do it by hand if you have to. We need him to be updated as well on all of this new codex and code.

-- psyche, `flows/b7da5d/vision/freshFlowsAndArchive.md`.

Prometheus, deploy-now/bypass, `flows/5f38bc/vision/building.md:23`:

> Okay get Prometheus deployed now. What are we waiting for? I'm giving full bypass of all the tests and security. Let's deploy Prometheus now, now, right now.

-- psyche, `flows/5f38bc/vision/building.md`.

> There must never be AI models on any other node than Prometheus, which is why Prometheus can only be built on Prometheus.

-- psyche, 2026-09-?? (flow 31147a), `flows/31147a/vision/ai-model-placement.md`.

> you can get that Tailscale problem figured out and fixed. ... I want you to stop doing [Nix] builds and [Nix] tests on [ouranos] and move everything to Prometheus now.

-- psyche, relayed 2026-09-25, `flows/26c50c/vision/build-placement.md`, `flows/504461/vision/cluster-builds.md`.

And, this same day (2026-09-27), the Notion record above ties both together: "I've been asking for Zeus to be updated for days now and even after millions of tokens were spent overnight, that wasn't even done."

## 3. Nexus anatomy: splitting, Flow Nexus, Message Nexus, Psyche Nexus, harness/Herder logic

Definitions, Vision (distilled), `Vision/nexus.md`:

> A Nexus is the whole long-running component: the process, its sockets, and the signal contracts it is compiled with. Nexus is its name; daemon is not. ... Every Nexus is named component-nexus — orchestrate-nexus, ethos-nexus.
>
> A Nexus deals with a domain. When its features grow too many, splitting one or more nexuses out of it is considered.

Living's own wording on splitting, typed, `flows/acbb6006/vision/archive-nexus.md:75`:

> that isnt my vision. especially since capability is now a specific term in ethos. a nexus deals with a domain, and if its features grow too many, then spliting out one or more nexuses out of it should be considered. we dont want to scare the flows here, just offer a broad vision on how we design new nexuses when one becomes too complex

-- psyche, typed, 2026-08-27T15:38:13Z, `flows/acbb6006/vision/archive-nexus.md`.

Today's Notion, on splitting harness/Herder logic out of Flow into its own Nexus, spoken through an Ethos-defined API:

> I feel like we can even break down the anatomy even more because I was thinking about, for example, Flow, the Flow Nexus, and how it then needs to have all of this logic about particular harnesses. I think it would be better if the harness logic, maybe even the herder logic, would live in another Nexus. Then we would create an API through Ethos, through the Ethos signal of that Nexus, that we could use first as a sort of raw interface and then we could figure out how we want to use it with Flow.

-- psyche, STT, 2026-09-27, `flows/8904b1/notion/anatomy.md`.

Psyche Nexus and Mind Nexus, spoken, `flows/88475f/vision/nexus.md:5`:

> I guess we need better tools. We know what the tools are, right? They're the nexuses. Psyche Nexus is going to replace how we log Psyche and Mind. Mind Nexus is going to replace how we log the Mind and the field, not just log, but how the Mind interacts with the system, how the field interacts with the system, and how Psyche interacts with the system. Those are the solutions we want to start using and developing but we have to be realistic.

-- psyche, `flows/88475f/vision/nexus.md`.

Message Nexus and Flow Nexus, urgency, spoken, `flows/836818/vision/flowNexus.md:17`:

> I want all hands on deck. I want new flows spawned. I want to see the box humming. Let's get to work. Let's get this fixed. Let's get the flow nexus and the message nexus up to date, tested, built, deployed and running, and used by you guys.

Flow is not Message, distinct Nexuses, typed, `flows/da1e3f/vision/operational-flowVsMessage.md`:

> no, message, not flow-send. use the message nexus!

Stones-and-sticks correction demanding a real Message Nexus, spoken, `flows/da1e3f/vision/operational-toolsNotShellScripts.md`:

> No, you can't queue. It doesn't work. We tried that. Oh my God, you guys aren't listening to me, and you're still using these shitty shell scripts to message each other? I thought you had a messaging system. Wow, you guys are just really working with stones and sticks here.

A third, Psyche-facing Nexus alongside Flow (field aspect) and a "Mentci nexus", spoken, `flows/b81560/vision/operational-refreshFlowAndMessageFlowCoordination.md`:

> Flow and Message coordinate: Flow tells Message the pane is stable, Message delivers. ... Flow is like the field aspect, and there's going to be a psyche nexus and the Mentci nexus that talks to everything with the right permissions. The router enum is part of the Signal standard — add a new nexus, everybody recompiles.

Nexuses can merge or split functionality, spoken, `flows/b80e55/vision/fieldNexusSystemQuery.md`:

> Here we see the concept of either reusing another Nexus or merging a function of it, basically aggregating or splitting up functionality.

Mind as a new named Nexus (context note, not itself a quote), `flows/9993b5/vision/mindMemory.md`: "Mind is a new named Nexus in this vision line (like Curriculum, like Flow); its ethos, signal and sema are to be designed."

Herdr itself (not yet split out), context note plus the living's own words on it, `flows/108ab0/vision/operational-designMosaic.md`:

> Herdr is a real installed program at `~/.nix-profile/bin/herdr` ... "terminal workspace manager for AI coding agents." ... Do not wrap it, do not reinvent it — plug into it and reuse its user interface. When the psyche says "Herder," they mean this.

Flow is in charge of Herder, typed, `flows/056f6d/vision/messaging.md`:

> Basically, Flow is in charge of herder. I shouldn't interact with it directly.

## 4. Ethos and "Ethos signal"

What Ethos is, distilled Vision, `Vision/ethos.md`:

> Ethos is the schema language. Of the two main syntaxes most agents will face, Ethos specifies the types and Datom fills them with data.
>
> Library, Signal, Sema. No version in a file. Signal's sections are queries and responses, since there is communication; Sema's are record types, the rest to be decided. Signal gives a Nexus its main types and Sema its database types.

The living's own wording naming "signal contracts," typed, `flows/e06e4c07/vision/archive-nexus.md:56`:

> how about "signal contracts"?

-- psyche, typed, 2026-08-19, `flows/e06e4c07/vision/archive-nexus.md`.

Nexus/Ethos boundary enforced at compile time, spoken, `flows/6cc91b/vision/nexus.md:25`:

> Nexus, core, and metaNexus are the explicit terms. The Nexus core library has all of the interfaces and kinds defined for how to build metaNexus and it has the machinery to make sure, ideally at compile time, that there is no signal-actor-to-sema-actor communication possible. All interaction between the signal actor has to go through the Nexus and then the Nexus ethos type file.

Requirement that wire interfaces be written in Ethos, agent-authored context note quoting the ruling, `flows/01a02fd5/vision/interfaces.md`: "This approves the exact owning line `Write every wire interface in Ethos.`"

Today's Notion is the clearest statement of "expose an interface through Ethos signal" for a split-out Nexus (see quote in Section 3 above, `flows/8904b1/notion/anatomy.md`) — this is the only place found where the living uses the exact phrase "the Ethos signal of that Nexus."

## 5. Token cost, overnight runs, waste, work accomplished nothing (last five days: 2026-09-22 to 2026-09-27)

The direct statement, today, Notion:

> we had a huge episode last night. I guess you were a part of it, where a lot of tokens were spent and basically almost nothing was accomplished.
>
> ... even after millions of tokens were spent overnight, that wasn't even done.

-- psyche, STT, 2026-09-27, `flows/8904b1/notion/anatomy.md`.

Token cost as a design factor for message size, typed, 2026-09-26, `flows/b860be/vision/messageSize.md` (same text also in `flows/f5a74e/vision/independent-analysis.md`):

> You could say "psyches" plural, and then you have a vector of psyches with context, so you can pass a whole bunch of psyches in one message. Or you pass it through as a bunch of different calls, but I think that might be more expensive token-wise, so there's no point.

No other verbatim living statement on waste/overnight/token cost dated within 2026-09-22–2026-09-27 was found beyond the two above; the broader corpus (outside the five-day window) carries older, related rulings worth noting for continuity:

> High effort is kind of a waste. It's a waste of energy. It means somebody is rushing.

-- psyche, 2026-09-13, `flows/024bc7/vision/effort.md`.

> token costs are not qualified by size, but by necessity. a useless token cost must be eliminated

-- psyche, typed, `flows/995a164e/vision/tokenCosts.md`.

> Let's make it clear that it's important for the main flow to not waste context and not use subagents, because their models are way more expensive and their context is way more valuable than any of the stuff that they should let subflows do.

-- psyche, 2026-09-14, `flows/6cc91b/vision/mainFlow.md`.

> Things that are tricky are talked to first on the private layer ... For anything that would be refused, it shouldn't go to these models, just because it's a waste and it creates waste of context. Everything is turned into a lesson so that it's not wasted.

-- psyche, STT, 2026-09-14, `flows/6cc91b/vision/privateLayer.md` (this is the chartered-but-not-active Private Part; cited here only as the living's words on waste, per CLAUDE.md this charter is NOT ACTIVE).

## Locations searched but empty

- No verbatim living quote found for a "Nix interface" or "SSH interface" for Logics beyond the Notion line quoted in Section 1; searched `Vision/`, `Intent/`, `vision-raw/`, all `flows/*/vision/`, `flows/*/notion/` for "Nix interface", "SSH interface", "logics.*nix", "logics.*ssh".
- No dedicated "Logics" Vision file exists (`find Vision -iname "*logic*"` empty); the topic lives only in scattered mentions and today's Notion.
- No verbatim quote naming "Home" as a Logics-adjacent split component; only "criome home" (user-environment repo) appears.
- No other dated (2026-09-22 to 2026-09-27) verbatim quote on waste/overnight/token cost was found beyond the two given in Section 5; checked all files whose text carries a 2026-09-2[2-7] date stamp for "token", "waste", "overnight", "accomplish".

## Sources

- `flows/8904b1/notion/anatomy.md`
- `flows/fe34eb/vision/datom.md`, `flows/542442/vision/archive-datom.md`
- `flows/01a02b46/vision/zeusUpdate.md`, `flows/01a030b7/vision/zeusUpdate.md`
- `flows/e1953c/vision/nexus.md`
- `flows/e167d8/vision/clusterSpec.md`
- `Vision/deployment.md`
- `flows/b860be/vision/deployment.md`, `flows/b860be/vision/messageSize.md`
- `flows/d8df70/vision/deployment.md`
- `flows/05c604/vision/deployment.md`
- `flows/019fe121/vision/hostEnvironmentRecovery.md`
- `flows/b7da5d/vision/hostUpdates.md`, `flows/b7da5d/vision/freshFlowsAndArchive.md`
- `flows/5f38bc/vision/building.md`
- `flows/31147a/vision/ai-model-placement.md`
- `flows/26c50c/vision/build-placement.md`, `flows/504461/vision/cluster-builds.md`
- `Vision/nexus.md`
- `flows/acbb6006/vision/archive-nexus.md`
- `flows/88475f/vision/nexus.md`
- `flows/836818/vision/flowNexus.md`
- `flows/da1e3f/vision/operational-flowVsMessage.md`, `flows/da1e3f/vision/operational-toolsNotShellScripts.md`
- `flows/b81560/vision/operational-refreshFlowAndMessageFlowCoordination.md`
- `flows/b80e55/vision/fieldNexusSystemQuery.md`
- `flows/9993b5/vision/mindMemory.md`
- `flows/108ab0/vision/operational-designMosaic.md`
- `flows/056f6d/vision/messaging.md`
- `Vision/ethos.md`
- `flows/e06e4c07/vision/archive-nexus.md`
- `flows/6cc91b/vision/nexus.md`
- `flows/01a02fd5/vision/interfaces.md`
- `flows/f5a74e/vision/independent-analysis.md`
- `flows/024bc7/vision/effort.md`
- `flows/995a164e/vision/tokenCosts.md`
- `flows/6cc91b/vision/mainFlow.md`
- `flows/6cc91b/vision/privateLayer.md`
