# What Opus of Psyche core is still trying to do

Get Flow Nexus 0.48 running beside 0.44 and move the seats to it.

- Mind core is finishing delivery on flow main: awake flows get every message at once, only HardAbrupt interrupts, and a queue exists only for a flow that is asleep. When it is green it pushes to GitHub and sends the commit.
- The unit is mine, on CriomOS-home branch flow-048-unit: its own store and sockets, no environment variable, its settings declared and applied over meta, every metaflow OnDemand. When the commit arrives: lock the flow input to it, set the typed presentation prompt to None, rebuild, send Field core Primary the diff and the checks, then deploy. The branches flow-048-unit and search-binding fold into CriomOS-home main in that same deploy commit.
- After deploy: send a message into a working seat and test a refresh. Then move the seats one at a time by rewriting the Metaflows family on both Nexuses, until Mind adds Maintain and Release. Remove 0.44 from the declaration once it is empty, and keep its store.
- At the end: one plain-English book, "What changed without your review", with one paragraph per change made today without his review, including Mind beliefNexus's one sentence on its crash fix. Fable tells him once it is up.

Fable writes the proposals; I publish and land them. Version 1 work reaches the living only once version 0 runs.
