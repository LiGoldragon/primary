# Flow tool

## Break the orphaned locks; nobody owns the Flow source; anybody may call Flow, and the CLI checks the calling process so flows can refresh themselves safely

> Yeah of course. What do you mean by "locks" anyway? Yeah of course, break the locks. Nobody in particular owns Flow Source. I don't know what you mean. Anybody should be able to call Flow, especially for self-refresh, so the Flow CLI will check the process that called it. We can allow flows to refresh themselves safely.

-- living, comment on "What Waits for the Living", 2026-09-24 14:30Z, on question 4 (Flow source ownership and the five orphaned locks).

## A meta socket binds already-running processes: the Herdr session first, then a vector of its flows in one call; a tool gathers a flow's anatomy and writes its datom

> Let's create, in terms of adding the current flows into the database, a meta socket for debugging for adding already existing processes. Add an already existing Herdr first because the Herdr is going to bind with the pool, or whatever the meta flow is, and then the thinking machine flows that are running inside that meta thinking machine flow are going to be bound.
>
> They can either be bound in a single call with a vector. Just let it take a vector of the structs that we need to bind, the struct with all the data. Create the anatomy of what a flow looks like and then let's create maybe some tool that can get all that information and create the datom for it.

-- living, input mode not established, 2026-09-24, to Psyche Medium d8df70, answering how the current flows get into Flow's database. Transcription corrected: "herder" → "Herdr" (twice).
