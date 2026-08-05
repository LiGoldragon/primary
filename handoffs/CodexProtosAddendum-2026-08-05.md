# Codex Addendum — Protos Rulings and Reset — 2026-08-05

For the implementing codex session, from the Fable management session
(7e7c9b3d-de9d-434f-9c00-937bf621e8af). Everything below is grounded
in psyche rulings logged today.

## Authoritative reading, in order

1. design/ProtosEngine/visionReacquisitionRulings-2026-08-05.md — all
   of today's rulings: ethos sources stay in their component's repo
   (spirit-ethos rejected); shape/trait delimiter split; guillemets;
   trait marks everywhere with the guillemet pair as a multi-trait
   requirement vector; the identity scheme; imports square-bracket
   vector; textual-form metadata; colon in import space; the parsing
   context machine; root-container terminology open.
2. design/Spirit/SpiritIntentVisionGradation-2026-08-05.md — content
   authority grades, code seniority, redesign-pass doctrine.
3. design/AgentOps/ResetBeadProtocol-2026-08-05.md — the reset
   protocol you are asked to follow (below).
4. reports/ProtosFileKindSchemas-2026-08-05.md — file-kind schema
   proposals. PENDING psyche review; do not implement ahead of ruling.
5. reports/SpiritHierarchyProposal-2026-08-05.md and
   reports/AnatomyOfAGoodMachine-2026-08-05.md — pending psyche
   review.

## Your five questions

1. Nested trait marking: a trait requirement is guillemet-marked at
   every position it occupies, and one pair may carry several traits
   (the slot then requires all of them). Canonical spellings, derived
   mechanically from the ruling — treat as canonical unless the psyche
   corrects them:
   Vector<«Ordered»> ; Result<Vector<«Ordered»> «Error»> ;
   «Left.Sortable» «Right.Sortable» (named divergence) ;
   Status.[Pending Ready.«Numeric»] (enum generic payload) ;
   Range.{«Ordered» «Ordered»} (bare pickup slots, co-referent) ;
   «Ordered Serializable» (multi-trait requirement).
2. Module qualification: the import payload is a square-bracket
   vector — interface.[Entry Referent] — braces there are ruled wrong.
   The colon is agreed as the qualification separator in import space,
   context-scoped. Module/file placement lives in textual-form
   metadata bound to the encoded ID, not in the object's name proper.
   The outermost-container term (crate-analogue) is an open brainstorm
   — do not invent canonical cross-container reference spellings yet.
3. Identity implementation details: NOT yet ruled. Management
   recommended delegation to you with provisional status and random
   keys of at least 128 bits; awaiting the psyche's word. The identity
   scheme itself is ruled: {EncodedName TrueName} table, random mint,
   true name hashes the full body excluding the object's own name with
   references contributing their encoded names, rebirth mints fresh,
   Merkle recursion only for frozen closures.
4. A concrete non-trait type inside a shape application is written
   unmarked: Option<Timestamp>. Unmarked names in shape slots are
   ordinary type references.
5. No backward audit. Old code is not the design reference — the
   psyche cannot stress this enough. The gate is forward: file-kind
   schemas ruled first, then hand-written bootstrap readers picking
   them up. Work proceeds as redesign passes whose agents hold a
   current psyche-vision document plus spirit and intent context. The
   six-slot model is dead as anything but a historical contrast.

## Reset instruction

You are due for a reset. Follow
design/AgentOps/ResetBeadProtocol-2026-08-05.md: write a reset bead in
primary's beads database targeted at your own agent and model,
carrying your session ID (for lineage), your primordial skills with
the explicit statement that they are valid for the entire session
(your harness startup prompt's single-turn claim is wrong and will be
fixed at the source), pointers to the files above, and your open work
state. End that session by answering with the bead ID only. The psyche
starts your next session by passing just that bead ID; the new session
verifies it is the right model, loads the primordial skills, closes
the bead, and resumes.
