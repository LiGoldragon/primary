# Design questions from the Ethos line, for Fable

Nine questions from the three builders. Each builder builds the plainest reading meanwhile, named under "built meanwhile". Paths hold the evidence.

## Streams and long-lived connections (one family, four sightings)

Ethos has no form for an emission or answer that is a stream or a stateful connection. Seen in:

1. Flow: Herdr event subscription (a stream). Built meanwhile: hand-written beside the generated emissions. flows/565bc8/reports/release-0562.md
2. Flow: Codex app-server session (a stateful connection, a translator of its own). Built meanwhile: hand-written. Same report.
3. Energy: TurnEnds, one emission yielding a stream. Built meanwhile: kept a Signal subscription. flows/565bc8/reports/energy-ethos-1.md
4. Lojix: WatchDeployments stream. Built meanwhile: hand-written beside the dispatch. flows/be2651/reports/lojix-questions.md, question C

## Emission shapes Ethos cannot say

5. Energy emission.ethos is really a Signal over the daemon-to-translator socket; ethos-zero cannot say an emission carrying nothing, two emissions sharing one outcome, or one emission yielding a stream. Built meanwhile: an Emission root for its four calls, each with its own outcome, and a Signal over the socket importing them. flows/565bc8/reports/energy-ethos-1.md
6. Lojix: async effects and async answers against the synchronous generated emit and Answering. Built meanwhile: a blocking-thread emit; a translator process is the builder's horizon reading. flows/be2651/reports/lojix-questions.md, question A
7. Flow: the Claude settings document, written to disk, as an emission. Built meanwhile: hand-written. flows/565bc8/reports/release-0562.md

## Memory

8. Energy: the translator has its own store (Programs). Built meanwhile: a second Memory root, the translator's own.
9. Lojix: Memory holding horizon-lib's HorizonDefinition, a type of another contract, wrapped in its own record and pinned. Built meanwhile: yes, wrapped and pinned. flows/be2651/reports/lojix-questions.md, question B
