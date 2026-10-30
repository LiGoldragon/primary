# Versioning

## 2026-10-30 — With interfaces that repopulate Memory in every way, a store upgrade need not be programmatic: a cheap flow reads the old store and infers the signals that repopulate the new one, when the upgrade looks or proves difficult
Context: the living, in the Psyche core Primary chat 0568e3, after the Primary ruled that next starts on a fresh store.

If we have interfaces that allow us to repopulate the memory in every way (whether it's to specify what a perma flow's history is: all of its flow ideas, so that we know a vector of all of its history of flow IDs and everything else), then we don't necessarily need the store upgrade to be done programmatically. We could just get a fairly cheap agent to repopulate the database by reading the old one and inferring what kind of signals would repopulate the new database. Do you follow me? That might avoid a whole bunch of messing around when it comes to upgrading, sometimes not always, but it could be a good solution for when the upgrade either looks or proves to be difficult.
