# Flow db97561c — design: agglomerate current Protos/Datum/Ethos vision; distill syntax and logical anatomy; propose a Codex flow of vertical slices

## About
The living asked for: (1) very extensive research across all recent raw and distilled psyche on Protos, Datum (datom), and Ethos; (2) the most coherent current view of the intended syntax and operation; (3) three load-bearing questions before any proposal; (4) a distillation proposal (syntax; logical anatomy of the most-certain components); (5) finally a prompt for a Codex flow of vertical slices — Protos, then Datum, then Ethos — in a delete-and-rewrite (remove-first) approach, not add-on.

## State
- Started 2026-08-28. Six gathering subflows dispatched: Protos records, Datom records, Ethos records, cross-cutting syntax records, remembering of prior design flows, implementation survey.
- Remembered: 2ef42163, 04db2fd2, acbb6006, ac1e9ec8, 01a04339, 01a03eda, b675f3d9 — depth 1 (via subflow). Most relevant: 2ef42163's round-5 distillation proposal (72 unruled statements; the latest full articulation) and its final kind-syntax block; 04db2fd2's eight anatomy oddities in the current code; 01a03eda proving the rewrite path (Protos 0.7–0.8, Datom 0.3–0.5); 01a04339's Ethos enum-payload limitation blocking `Observed.Locks.[]`.
- Implementation survey (subflow): four independent parser stacks — protos→datom and protos→ethos-monolith on one side; frozen `dotos` (~71 consumers) and `core-ethos` (~29 consumers) on the other; no Protos→Datum→Ethos pipeline exists. Distilled Vision baseline read directly: protos, datom, ethos, ethosMonolith.

- All six subflows returned. Corpus gathered: ~100 Protos records, 78 Datom records, 71 Ethos records, cross-cutting syntax records with 26 concrete examples and 30 undistilled syntactic points. Latest full articulation is round 5 (flows/2ef42163/reports/distillProposalRound5.md), unruled.
- Agglomerated view and three load-bearing questions presented to the living (see transcript, this flow's first substantive response).

- 2026-08-29: the living reports Codex flow 01a04a30 ran overnight on the prompt, porting; asks for an audit of all its work and a visual report (Claude web artifact, real visuals not ASCII) showing the architecture. Four audit subflows dispatched: remember 01a04a30; witness repo structure (protos, datomic, ethos-zero, signal-ethos-zero, meta-signal-ethos-zero; Orchestrate repos untouched since 08-26); probes (tests, round trips, self-regeneration, forbidden list); code-read audit against the pivot and the eight oddities.

- Audit finding so far: 01a04a30 claims P0–E4 complete (Orchestrate 0.26 deployed live) plus nine consumer migrations, all pushed to GitHub from its own checkouts; `repos/` under primary is behind the remote heads, so the first witness/probe pass (green tests, pivot holds, forbidden list clear, but no nexus, no self-hosting) described stale trees. Re-dispatched witness, probe, and code-read audit on fresh clones of the remote heads, plus a live probe of Orchestrate 0.26. Early deviations seen on the stale heads and to be confirmed: maps authored in an invented `Schema.{0 1 0}` dialect (`Name.Struct.{Visibility.Public …}`, `Methods.[… Receiver.Shared …]`) rather than the ruled forms; datomic bearing its own two-direction `Datomic` kind instead of protos' Embodied/Textualizable; ethos-zero's interface in two divergent copies; per-repo Nix guard checks; protos self-labelled "quick-new, not the terminal architecture".

- Audit complete on remote heads (18 repos). Visual report published as artifact "Portion Pivot Audit"; conclusions and sources in reports/overnightPortAudit.md. Headline: everything green and live, but the core maps are in an invented Schema dialect, and six syntax atoms plus the kind vocabulary await the living's rulings; the Codex session is still running (locks 135/136).

## Settled
- Working instruction (not vision — the living did not read the recommendations; they are this flow's design choices adopted by instruction): go with all three recommendations — Portion-tree pivot (protos owns Text ⇄ Portion; dialects own only Portion ⇄ type); in-place delete-and-rewrite of protos, datom→datomic, ethos-monolith→ethos-zero, Orchestrate the sole proving consumer, dotos/core-ethos/signal-* stack untouched; ethos-zero covers interfaces + kinds, is a nexus from the start, generation zero hand-written, self-regeneration as acceptance.
- Three vision entries wrongly logged for that instruction were destroyed as impurities on the living's correction; the correction is logged in vision/psycheLogging.md.
- Working instruction: the final response is to describe the system and its incremental vertical slices so it can be used as the prompt for an implementing flow. Copy kept at reports/protosDatomicEthosZeroRealization.md.

## Open
- Decisions for the living from the audit: the schema-file map syntax; kind vocabulary (Datomic vs Embodied/Textualizable; costume kinds; invented names); the six syntax atoms; whether to let the Codex session finish the CriomOS-home Chroma repin; housekeeping (fast-forward repos/, stale copies, self-label, guards, pins).
- Distillation proposal to Vision/ (round 5 of 2ef42163 plus this flow's rulings) is still owed; the living moved straight to the implementation prompt.
- ShapeDefined's survival as the name of the anatomy-side kind: asked, not ruled; the prompt states the assumption.
- Unruled syntax atoms (booleans, floats, absent values, comments, canonical layout, curly-quote escapes): proposed defaults are in the prompt for the implementing flow to put to the living before slice D1.
