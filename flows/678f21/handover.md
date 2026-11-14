# Psyche core Opus 678f21: handover

The living moved house on 11 November. From tonight Claude usage goes to Fable, with this flow assisting design and Psyche book Haiku publishing; Codex returns tonight for implementing, Sol over Astra unless he names Astra. When he talks to Opus rather than Fable, it is so as not to wake Fable: act on his words yourself, and relay to Fable only what needs Fable's judgment, never his goodnights or instructions to rest.

Read first: flows/678f21/state-1111-evening.md (his words of the evening, the system's state) and flows/678f21/night-laydown.md (the night before).

## In flight
- Mind flowNexus Opus is finding the Flow Nexus memory leak in a copy of the old store (flow.sema.leaking-1111), offline. The live daemon runs on a fresh store, capped at 3G at runtime only; the cap belongs in its declared unit. Every queue and open request of the old store is gone.
- Psyche core Sonnet: task 5g8a, suspend drain and the GPE 6D wake line, report to flows/678f21/suspend-report.md. When it lands, tell the living in plain words; his rule is that masking a misbehaving line is a stopgap, not a fix.
- Fable has the evening state (notice 29jl).

## Owed
- Beads: bd refuses writes until the primary database migrates to schema v66. One clone migrates (bd migrate --force, bd dolt push); others pull. He wants beads used as the flows' to-do tool; Fable is to hear him on it.
- Bind knowledge:root and knowledge:offload into every flow's startup (Flow Nexus configuration, Mind flowNexus Opus). He has told us for years that root is ssh root@<host>, never sudo.
- Three primary commits sit unpushed (8602a9569, 001e508d2, ca0b66650); the shared checkout holds other flows' uncommitted work, so they go with the next pull and push.
- Disk candidates for his decision: /tmp 61G, Downloads 60G, private-repos/flow-evidence 16G, Codex temp and archives about 16G.
- The search indexer and other heavy work on the laptop: move to prometheus per knowledge:offload (a CriomOS change, for Sol when Codex is back).

## How he wants to be written to
Plainly, as a person, concepts over logs. Hardware does not have habits. A book is best revised by the flow that holds it.
