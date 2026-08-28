# Flow db97561c — design: agglomerate current Protos/Datum/Ethos vision; distill syntax and logical anatomy; propose a Codex flow of vertical slices

## About
The living asked for: (1) very extensive research across all recent raw and distilled psyche on Protos, Datum (datom), and Ethos; (2) the most coherent current view of the intended syntax and operation; (3) three load-bearing questions before any proposal; (4) a distillation proposal (syntax; logical anatomy of the most-certain components); (5) finally a prompt for a Codex flow of vertical slices — Protos, then Datum, then Ethos — in a delete-and-rewrite (remove-first) approach, not add-on.

## State
- Started 2026-08-28. Six gathering subflows dispatched: Protos records, Datom records, Ethos records, cross-cutting syntax records, remembering of prior design flows, implementation survey.
- Remembered: 2ef42163, 04db2fd2, acbb6006, ac1e9ec8, 01a04339, 01a03eda, b675f3d9 — depth 1 (via subflow). Most relevant: 2ef42163's round-5 distillation proposal (72 unruled statements; the latest full articulation) and its final kind-syntax block; 04db2fd2's eight anatomy oddities in the current code; 01a03eda proving the rewrite path (Protos 0.7–0.8, Datom 0.3–0.5); 01a04339's Ethos enum-payload limitation blocking `Observed.Locks.[]`.
- Implementation survey (subflow): four independent parser stacks — protos→datom and protos→ethos-monolith on one side; frozen `dotos` (~71 consumers) and `core-ethos` (~29 consumers) on the other; no Protos→Datum→Ethos pipeline exists. Distilled Vision baseline read directly: protos, datom, ethos, ethosMonolith.

- All six subflows returned. Corpus gathered: ~100 Protos records, 78 Datom records, 71 Ethos records, cross-cutting syntax records with 26 concrete examples and 30 undistilled syntactic points. Latest full articulation is round 5 (flows/2ef42163/reports/distillProposalRound5.md), unruled.
- Agglomerated view and three load-bearing questions presented to the living (see transcript, this flow's first substantive response).

## Settled
- Working instruction (not vision — the living did not read the recommendations; they are this flow's design choices adopted by instruction): go with all three recommendations — Portion-tree pivot (protos owns Text ⇄ Portion; dialects own only Portion ⇄ type); in-place delete-and-rewrite of protos, datom→datomic, ethos-monolith→ethos-zero, Orchestrate the sole proving consumer, dotos/core-ethos/signal-* stack untouched; ethos-zero covers interfaces + kinds, is a nexus from the start, generation zero hand-written, self-regeneration as acceptance.
- Three vision entries wrongly logged for that instruction were destroyed as impurities on the living's correction; the correction is logged in vision/psycheLogging.md.
- Working instruction: the final response is to describe the system and its incremental vertical slices so it can be used as the prompt for an implementing flow. Copy kept at reports/protosDatomicEthosZeroRealization.md.

## Open
- Distillation proposal to Vision/ (round 5 of 2ef42163 plus this flow's rulings) is still owed; the living moved straight to the implementation prompt.
- ShapeDefined's survival as the name of the anatomy-side kind: asked, not ruled; the prompt states the assumption.
- Unruled syntax atoms (booleans, floats, absent values, comments, canonical layout, curly-quote escapes): proposed defaults are in the prompt for the implementing flow to put to the living before slice D1.
