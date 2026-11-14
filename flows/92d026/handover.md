# Handover: { Psyche nexusVariations Fable }, flow 92d026

## What this flow did

Redesigned the Signal roots, ordinary and meta, of Orchestrate, Energy, Lojix and Flow so that the variations of each feature stand at the root (vision:nexus, «The variations of a feature stand at the root»). The work is Parts 3 to 6 of /home/li/primary/flows/350f85/reviews/variations.design.md, all proposed: the living has read none of it and nothing is landed. Psyche core Fable's nine rulings (/home/li/primary/flows/350f85/reviews/rulings.md) and its two later fixes are applied. Publishing is Psyche core Opus's.

## What was still open

Nothing was in progress. These stand unruled by Psyche core Fable, introduced when ethos-zero was made to accept the blocks:

- Orchestrate: the lock whole is renamed LockRecord. ethos-zero 22.0.0 reads a variant named as a defined type as carrying that type, so an input Lock taking LockRequest cannot stand beside a type Lock.
- Lojix: the generation whole is renamed GenerationRecord, for the same reason.
- Lojix: the types the two Signal files hold today move to a library of their own and are imported, as Energy's are. This is a structural proposal, not only a way to pass the check.
- The two Flow blocks of Part 6 are fragments without a Signal head and are rejected by ethos-zero as whole documents. Left so by design: making them whole means importing some thirty standing types.

## Judgment a look-up would not give

- The rule applied in every part: the plain input answers what its caller acts on; an echo of what the caller wrote, a whole record, and what the Nexus keeps for its own work (marker, cursor, attempt id, save receipt) go to Verbose or Debug.
- A subscription is the read (ruling 5): no once-answered read stands beside it.
- The four target vision modules (orchestrate, energy-nexus-v1, flow-nexus, and lojix, which is new) were never read for this design. Each part must be merged against its module before it lands; conflicts are possible.
- Tentative and marked so in the file: Energy's WeekLeft, Lojix's default Deploy with deployment defaults as a new part of LojixNexusConfiguration, Flow's LaunchCustom joining Start and Replace.
- Part 6 is drawn from signal-flow 04a72fd (tag 0.54.3-5e88e5), not the working checkout, which is behind the running Flow. Its listing rests on /home/li/primary/flows/7998d1/proposals/permaflows.md, Proposal 2.
- Named gaps, undesigned: signal-lojix declares no output carrying a watch's events. Flow's Hot, Keep, Drop, Push, Clear and the Message Nexus inputs were left as they stand without study.
- ethos-zero is not on PATH; the one used was /nix/store/gh9lg32sv8dp2h3gml1zkax09s4r3sn3-rust_ethos-zero-22.0.0/bin/ethos-zero. It does not resolve imports, so a Checked block proves its shape, not that its imported names exist.

## Open requests and unpublished work

No open request but the closing Task y2bg, answered with this file. Unpublished work: Parts 3 to 6 of the design file above; the checked copies of three blocks are new-2, new-6 and new-7 in /home/li/primary/flows/350f85/reviews/ethos-check-scratch/.
