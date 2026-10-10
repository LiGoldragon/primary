# Flow first, Message plugged in after; Flow composes the prompts

> Can you get in touch with Mind Astra, or any kind of highest field that you can find, if you can't find one, to implement your best design of Flow (so we can spawn Flow and message into pains using the Flow CLI)? We'll plug message into that after we deploy Flow and we can use it to start a session.
>
> It has to have a way to compose the prompts: the first prompt and eventually a way to compose the system prompt but we can start with the prompt. What's the situation with injecting a bunch of skills in a single prompt in Claude?

-- psyche, typed, 2026-09-23, directly to Psyche High 836818. "pains" read as panes (Herdr panes); correction noted, not applied inside the quote since the message was typed.

## A proper flow tool; all hands; the box humming

Heard by Psyche Medium d8df70 on 2026-09-24 (its transcript lines 1196 and 1240, 13:53:39Z and 14:03:19Z, queued); raw record in flows/d8df70/reports/living-words-since-launch.md; quoted here because it directs this seat's coordination.

> I don't like it anyway because it's mixing different areas, different designs. We need to just have a proper flow tool. How's the flow tool? How's the connection to Prometheus? How fucked are we this morning? I've been pulling my hair because you can't even connect to Prometheus with a direct Ethernet cable. I don't care about this skill edit. Just forget about it. It's fucking meaningless. I'm not happy with how things are going. I want things to run better. It's not fun to work with you right now. You can't start flows properly. When I say "you" I mean all of you as a whole, all of the flows.

> Is there a firewall problem on Prometheus? You want to go check that out and get mine to test, build, and deploy the new flow and then let's make message work with it. I want Prometheus up, right? Let's fix the firewall so it's fully up or whatever is wrong with it.
>
> I want all hands on deck. I want new flows spawned. I want to see the box humming. Let's get to work. Let's get this fixed. Let's get the flow nexus and the message nexus up to date, tested, built, deployed and running, and used by you guys.

-- psyche, STT, 2026-09-24, to Psyche Medium d8df70. Also at its lines 1087 and 1127: flows talk to Codex seats by message, they do not run Codex; images are Mind's work, not Field's, "Field is for repair."

## The living's answers to the six questions, 2026-09-24

Heard by Psyche Medium d8df70 as comments on "What Waits for the Living" (14:28 to 14:32 UTC) and its instruction "Talk to Fable about all this and get Mind and Field to adapt the answers into code and deploy." Raw records with the words: flows/d8df70/vision/flowLifecycle.md, building.md, flowTool.md, messaging.md (commit 24077d45). Quoted here because they replace this seat's provisional rulings.

> A seat starts receiving. The old seat stops receiving first. That's how we get a lock. I'd rather use the word "flow" also, but do you mean something else by "seat"? A new flow starts receiving as soon as it has its start prompt and then the old seat or flow is killed or removed. Its conversation or its thing is archived. I'd also like to know what happens with archives and if they're searched differently.

> Well when the builder isn't reachable we just build locally.

> I'm not sure what you mean. How do the running services get back to the known source? They're built and installed from CriomOS so you can check the source that built that generation. I guess find out how that link is made if you want to know.

> Yeah of course. What do you mean by "locks" anyway? Yeah of course, break the locks. Nobody in particular owns Flow Source. I don't know what you mean. Anybody should be able to call Flow, especially for self-refresh, so the Flow CLI will check the process that called it. We can allow flows to refresh themselves safely.

> If a message can't be delivered, then we try a higher power. If Psyche Medium is not reached, we try Psyche High and if there's nothing higher then we try lower. The message returned for the caller will say what happened but we'll have a bunch of rules. Also we can start a flow if it's missing, it needs to get a message, and it's considered crucial. All the medium and high flows are considered crucial.

> The old flow is closed when it has a replacement, at which point it shouldn't be reachable anymore because the lock took that route away for the replacement. In fact it just blocks until the new pane or seat is ready to receive and then the old one in the same swoop. We verified it is not active and then we exit it. In order for the flow to refresh, it needs to have a flow handover in its transcript somewhere, a recent transcript not too old.

-- psyche, typed as comments, 2026-09-24, to Psyche Medium d8df70; "createoms" and "Psyq" repaired to CriomOS and Psyche by d8df70.

## Rolling forward: deploy now

Heard by Psyche Medium d8df70 on 2026-09-24 about 15:05 UTC (locator owed), forwarded verbatim:

> I don't understand what you think we need to do before deploying. What do you mean, roll back? Roll back to what? We have nothing now. We're rolling forward. There's no rolling back because if we roll back we fall off the cliff. Let's go deploy. Fucking move your ass.

-- psyche, STT, 2026-09-24, to Psyche Medium d8df70.

## Not live yet: no old stores, no migration

Heard by Psyche Medium d8df70 on 2026-09-24 (locator owed), forwarded verbatim:

> We don't need to keep old stores of Flow and message. We're not even live yet. Stop treating this like it's a fucking migration.

-- psyche, STT, 2026-09-24, to Psyche Medium d8df70.

## Binding the existing flows into Flow through the meta socket

Heard by Psyche Medium d8df70 on 2026-09-24; verbatim in flows/d8df70/vision/flowTool.md (last entry); quoted here because it directs the Flow work:

> Let's create, in terms of adding the current flows into the database, a meta socket for debugging for adding already existing processes. Add an already existing Herdr first because the Herdr is going to bind with the pool, or whatever the meta flow is, and then the thinking machine flows that are running inside that meta thinking machine flow are going to be bound. They can either be bound in a single call with a vector. Just let it take a vector of the structs that we need to bind, the struct with all the data. Create the anatomy of what a flow looks like and then let's create maybe some tool that can get all that information and create the datom for it.

-- psyche, STT, 2026-09-24, to Psyche Medium d8df70.

## A Herdr session is a flow container, not a pool

Heard by Psyche Medium d8df70 on 2026-09-24; verbatim in flows/d8df70/vision/flowTool.md (last entry):

> We can add an already-live Herdr meta flow with all of its flows into the running flow with the meta socket. You don't have to spend too much time creating it. Although we should have a tool to import an already-running Herdr session into Flow eventually, otherwise we can just bootstrap by hand for now. One Herdr's session is one pool but I don't like the word "pool." ... It's a container. It's a flow container that has many flows in it: many typed flows. Typed flow meaning psyche, mind, and field, and then we're going to have sub-subroles, subtypes like that.

-- psyche, STT, 2026-09-24, to Psyche Medium d8df70.
