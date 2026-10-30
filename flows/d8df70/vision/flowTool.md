# Flow tool

## Break the orphaned locks; nobody owns the Flow source; anybody may call Flow, and the CLI checks the calling process so flows can refresh themselves safely

> Yeah of course. What do you mean by "locks" anyway? Yeah of course, break the locks. Nobody in particular owns Flow Source. I don't know what you mean. Anybody should be able to call Flow, especially for self-refresh, so the Flow CLI will check the process that called it. We can allow flows to refresh themselves safely.

-- living, comment on "What Waits for the Living", 2026-09-24 14:30Z, on question 4 (Flow source ownership and the five orphaned locks).

## A meta socket binds already-running processes: the Herdr session first, then a vector of its flows in one call; a tool gathers a flow's anatomy and writes its datom

> Let's create, in terms of adding the current flows into the database, a meta socket for debugging for adding already existing processes. Add an already existing Herdr first because the Herdr is going to bind with the pool, or whatever the meta flow is, and then the thinking machine flows that are running inside that meta thinking machine flow are going to be bound.
>
> They can either be bound in a single call with a vector. Just let it take a vector of the structs that we need to bind, the struct with all the data. Create the anatomy of what a flow looks like and then let's create maybe some tool that can get all that information and create the datom for it.

-- living, input mode not established, 2026-09-24, to Psyche Medium d8df70, answering how the current flows get into Flow's database. Transcription corrected: "herder" → "Herdr" (twice).

## One Herdr session is a flow container of typed flows; bootstrap the live one by hand now, an import tool later

> We can add an already-live Herdr meta flow with all of its flows into the running flow with the meta socket. You don't have to spend too much time creating it. Although we should have a tool to import an already-running Herdr session into Flow eventually, otherwise we can just bootstrap by hand for now. One Herdr's session is one pool but I don't like the word "pool." It's a cluster. No it's a meta flow. No I don't know. It's a container. It's a flow container that has many flows in it: many typed flows. Typed flow meaning psyche, mind, and field, and then we're going to have sub-subroles, subtypes like that.

-- living, input mode not established, 2026-09-24, to Psyche Medium d8df70. Transcription corrected: "herder" → "Herdr" (twice), "harder" → "Herdr".

## There is one Herdr session

> Okay, there shouldn't be two Her sessions. Which one is Flow currently attached to? Do you mean Flow will know two containers? Let's go. I want to use Flow. Why aren't we using Flow? I don't understand. Just get it done. Just get it working.

-- living, input mode not established, 2026-09-24, to Psyche Medium d8df70, on learning that the seats are split between the Herdr sessions `messaging-build` and `default`. ("Her sessions" is read as "Herdr sessions"; inference.)
