# 75 — message / router / orchestrate → production on the schema/triad-engine base (frame + method)

Kind: meta-report directory (frame + skills rulebook + intent agglomeration + triad-base state + 3 component production maps + adversarial verification + orchestrator overview).
Topics: engine, message, router, orchestrate, triad-runtime, schema-rust-next, signal, nexus, sema, production, port-readiness, supervision, delivery.
Date: 2026-06-05.
Role: system-designer (orchestrator).

## Psyche directive

> "refresh skills and intent in depth and research how you would bring message,
> router and orchestrate into production state with the new schema/triad-engine base"

Two halves, both to be done seriously (not a token pass): (1) a deep refresh of the
governing **skills** and **intent**, landed as durable digests; (2) a source-grounded
research/design for taking **message**, **router**, **orchestrate** to production on the
**schema/triad-engine base** — the spirit-pilot shape, `triad-runtime` runner, and
`schema-rust-next` emission.

## The anchoring finding (verified against source, 2026-06-05)

**All three target components are PRE-triad-engine.** They are hand-written Kameo
daemons carrying the OLD schema form, not the three-plane triad:

| Component | Today (source-verified) | Schema form |
|---|---|---|
| `message` | Kameo root actor, `daemon.rs` + `actors/` + `output_validator.rs`; stateless boundary; INTENT.md says "depends on stable Persona Kameo lifecycle reference" | one `message.concept.schema` (concept form) |
| `router` | hand-written `RouterRuntime`; `channel.rs`/`delivery.rs`/`adjudication.rs`/`harness_delivery.rs`/`tables.rs`; `sema` lib for `router.redb` | one `router.concept.schema` (concept form) |
| `orchestrate` | most advanced — sema store, dynamic role registry, owner contract, ShortHeader validation, Mirror upgrade-handover; hand-written `daemon.rs`/`tables.rs`/`lowering.rs` | `.concept.schema` PLUS old versioned `orchestrate-v0-1*.schema` (pre-`schema-next`) |

The contract repos exist as concept-schema stubs only: `signal-message`, `signal-router`,
`owner-signal-router`, `signal-orchestrate`, `owner-signal-orchestrate` are each
`src/lib.rs` + one `*.concept.schema` (owner-signal-* not yet renamed to `meta-signal-*`).

## The base they port ONTO (the reference, verified)

- **`spirit`** — the canonical triad daemon: `schema/{signal,nexus,sema}.schema` →
  `src/schema/{signal,nexus,sema}.rs`, with `engine.rs` (SignalEngine impl), `nexus.rs`,
  `plane.rs`, `store.rs`. This is the worked example every port copies.
- **`triad-runtime`** — the runner (the `7ca4` lever). HEAD `28d03c3`
  "add multi-listener daemon shell" — so the **MultiListenerDaemon is now COMMITTED**
  (no longer operator's uncommitted working copy). `runner.rs`, `daemon.rs`, `role.rs`,
  `frame.rs`, `argument.rs`, `trace.rs` are the plug-in surface.
- **`schema-rust-next`** — the emitter (`RustEmissionTarget`: WireContract / ComponentRuntime
  / SignalRuntime / NexusRuntime / SemaRuntime; the `triad_main!` runner-loop emission;
  lifecycle hooks; effects; typed trace). Green (53 tests at last check).
- Asschema removal is COMPLETE in code (report 73 §7). The new pipeline is
  `schema/*.schema → src/schema/*.rs` directly via the structural-macro-node codec.

## Binding intent anchors (description-first; codes secondary, re-minted recently)

- The running-orchestrated-system target — persona supervises introspect + schema-daemon +
  the others as one running whole (`mazv`); **Orchestrate = the `orchestrate` component**
  that runs the daemon set (`tq18`).
- Extract the generic triad runner now (`7ca4`); the runner adapter is generated glue,
  authors implement the three plane engines + effect handler + budget reply (`rpr5`); SEMA
  owns DB / Nexus owns decisions / Signal owns communication (`tirp`/`t2iy`).
- The Nexus schema IS the engine's visible internal feature catalog — every internal
  feature is a declared Nexus verb+object (`z6qu`, VeryHigh).
- A component triad is ≥3 separate plane schema files; Signal wire-contract in the contract
  repos, Nexus+SEMA inside the daemon crate (`lc2r`).
- `meta-signal-*` is the canonical policy-contract prefix; `owner-signal-*` is a migration
  leftover to retire (component-triad skill §4).
- Component feedback/status/errors are typed self-descriptive NOTA enums, no string
  messages (`bexd`).
- Engine traits carry minimal `on_start`/`on_stop` lifecycle hooks — the minimum surface
  persona supervision uses (`czw0`).
- Inter-component messaging uses unique agent+message identifiers for async correlation
  (`h4mn`); no NOTA between live components (binary wire only).

## Method — the workflow

Phase 1 **Refresh** (barrier, 3 agents, each writes its report):
- `1-skills-production-rulebook.md` — distill the full governing skill set into the
  production-readiness rulebook + a checklist a component MUST satisfy to be triad-shaped.
- `2-intent-agglomeration.md` — deep Spirit sweep across every relevant topic; the binding
  decisions/principles/corrections + the OPEN questions; description-first citation.
- `3-triad-base-state.md` — how a production triad daemon is actually built TODAY against
  spirit + triad-runtime + schema-rust-next, end to end; landed-vs-proposed/blocked.

Phase 2 **Map** (3 agents, each reads reports 1-3, writes its report):
- `4-message-production.md`, `5-router-production.md`, `6-orchestrate-production.md` —
  per component: exact current architecture, the gap to the base, the concrete port plan
  (which plane schemas; the Nexus feature catalog; SEMA tables or stateless carve-out;
  the contract-repo rename to meta-signal), witness tests, build/test plan, blockers,
  and the open decisions for the psyche.

Phase 3 **Verify** (adversarial, per component, pipelined off each map): re-check the
current-state and "port path is unblocked" claims against source; default skeptical.

Phase 4 **Synthesis** (orchestrator): `7-verification.md` + `8-overview.md` — the
sequenced production roadmap, shared blockers, open decisions.

## Discipline

- Refresh/map agents are READ-ONLY on code; they write exactly ONE report file each into
  this directory; no edits/commits/mutating ops on any repo.
- Verify every file/type/record/intent citation against source. Landed-vs-proposed honesty
  is mandatory — do not claim a port path is unblocked if it depends on something not yet
  landed (sema-engine emit, `primary-vllc`, the meta-signal rename, two-listener wiring).
- Cite intent as bracket-quoted summaries, description-first, code secondary.
- NOTA discipline when quoting: bracket strings only, positional records, never `"`.
- Do not touch the `triad-runtime` working copy or any operator-owned main.
