# 674 — criome internal engine / identity policy language: frame and method

## The brief

The psyche asked to develop **criome's internal language** — captured (after
the Spirit gate superseded `niuj`) as Spirit `vhs2` (Decision, Medium):

> [Crayome's internal language is a limited typed policy language over
> public-key identity atoms - NOT a general-purpose virtual machine - drawing
> its limited-operation discipline from the constrained VMs of Ethereum, Tezos,
> and Solana. Public keys are the atomic unit of identity; above them it
> composes complex identity contracts from signature and time-lock mechanics:
> signature quorums of k-of-n form and thresholds that increase or decrease
> over elapsed time. It carries explicit divergence-reconciliation objects for
> when two networks split, where conflict resolution may be mediated by an
> LLM-oracle call to a provider which itself resolves through one of those
> identity contracts - for example a paid expert panel adjudicating the fairest
> resolution model.] (Spirit vhs2)

The deliverable the psyche named: research the objects and verbs needed, define
them in schema, and present a full psyche meta-report with visuals, schema code,
Rust code, and a proof-of-concept implementation.

## What this is NOT (the load-bearing constraints)

- **Not a general-purpose VM.** `vhs2` (and the superseded `niuj`) draw the line
  explicitly: a *limited typed policy language*, taking only the limited-operation
  *discipline* of the Ethereum/Tezos/Solana VMs, not their generality.
- **criome stays auth-only.** Per Spirit `wckt` [criome stays auth-only - signs
  and verifies, never transports]. A richer identity engine does not make criome
  transport; the router transports, the mirror version-controls.
- **Build on content-addressed composable authorization objects.** Per Spirit
  `z9d6` [Criome authorization contracts should be content-addressed composable
  objects: each component can decide acceptance based on another accepted object
  or contract ... Threshold, majority, or time-window acceptance policies are
  criome contract logic layered on those composable authorization objects]. This
  is the substrate the object/verb vocabulary must extend, not replace.
- **Triad-consistent.** Every component already has Signal/Nexus/SEMA engines
  (Spirit `a71r`/`3d5z`). This work specifies *what criome's Nexus engine computes
  over* — its identity object and verb vocabulary — not a fourth parallel engine.
- **Already partly built.** criome has BLS attestation, `RegistrationStatement`,
  `MasterKey`, cluster-root admission, an `Identity`/`Host` model (Spirit `2st7`,
  reports 112/114/118). The vocabulary extends the deployed model.

## Method — 9 agents across 4 phases

This lands as this meta-report directory. Numbered files:

| File | Agent | Output |
|---|---|---|
| `0-frame-and-method.md` | orchestrator | this frame |
| `1-ground-criome-vocabulary.md` | ground-criome | inventory of criome/signal-criome/meta-signal-criome existing objects, verbs, SEMA families, Identity model; domain-criome resolution surface |
| `2-ground-intent-constraints.md` | ground-intent | the binding Spirit records (vhs2, z9d6, 2st7, w2g3, wckt, d6he) + reports 112/114/118/123 distilled to design constraints |
| `3-research-chain-identity-models.md` | research-chains | Ethereum/Tezos/Solana identity + limited-operation models, what transfers to a limited identity policy language |
| `4-research-primitives-reconciliation.md` | research-primitives | threshold-sig/multisig/timelock/social-recovery primitives; fork-reconciliation, oracle, and decentralized-arbitration patterns for the divergence mechanism |
| `5-object-verb-design.md` | design-vocabulary | the criome Nexus object + verb vocabulary (limited policy language), grounded in z9d6 composable objects |
| `6-schema-code.md` | schema-author | NOTA schema for the objects/verbs, per structural-forms + nota-design |
| `7-rust-poc.md` | rust-poc | a self-contained, actually-compiled-and-run Rust PoC: identity atoms, quorum/timelock/time-varying composition, authorization evaluation, divergence-reconciliation interface with a stub LLM-oracle |
| `8-synthesis-psyche-report.md` | synthesis (+ design-critic findings) | the psyche-facing meta-report: vision, object/verb model with mermaid, schema, Rust + real PoC output, reconciliation design, open questions |

Phase 1 (ground+research) is a barrier before design. Phase 2 is the single design
synthesis. Phase 3 runs schema-author, rust-poc, and an adversarial design-critic
in parallel. Phase 4 is the synthesis that reads everything and writes the
psyche report. The PoC is honest: a standalone runnable demonstration of the
mechanics, not yet integrated into criome proper (integration is the next step).
