# Triad-engine refresh + lojix port to the new model

Cloud-designer lane. 2026-06-05. **Meta-report directory.** The psyche flagged
that the basic triad-engine components are in flux — there is a newer version
and new composition instructions — and asked me to (1) refresh on the latest,
(2) port the lojix work onto it, (3) drive end-to-end testing (build, maybe
deploy) as far as I can, and (4) resolve-or-explain the streaming problem they
don't understand.

## What changed in the last ~24h (orientation already done)

- **asschema removed.** schema-next dropped the Asschema compatibility surface;
  schema-rust-next removed the asschema emitter API, is at **0.1.13**, and now
  lowers "rust through schema object traits" + "source driver emission" with a
  "schema source binary archive".
- **triad-runtime is the shared runtime.** It owns the recursive **Runner**
  (the Nexus action loop + typed continuation budget), the **single-listener
  daemon runner**, `ComponentCommand`/`ComponentArgument` (single-arg rule),
  `LengthPrefixedCodec`, and trace transport. Components implement the three
  plane engines + effect handler + budget-exhausted reply; the `RunnerEngines`
  adapter is generated (record `7ca4`).
- **The Nexus schema is the engine's FEATURE CATALOG** (record `z6qu`): every
  internal feature — computation, filter, conditional write — is a declared
  Nexus verb+object, never inline hidden logic.
- **Concrete cloud template:** `cloud/schema/nexus.schema` (`[NexusWork]` /
  `[NexusAction]` roots; `SignalInput`/`SignalOutput` unions of ordinary+meta;
  `EffectCommand` catalog; the `SignalArrived → Command* → Continue` re-entry
  model) + `cloud/schema/sema.schema` (`SemaReadInput`/`SemaWriteInput` roots +
  table records + `StateMarker`). Generated Rust is checked in at
  `cloud/src/schema/{nexus,sema}.rs` via `build.rs`
  `GenerationDriver::new(plan).generate().write_or_check(...)`, with each
  contract schema dir read through `DependencySchema::from_cargo_metadata`.
- **Caveat:** the cloud `Store` still handles requests directly inline (the
  Cloudflare call is in `Store`, not yet a Nexus `CommandEffect`), so even the
  template is mid-migration to the full runner model.
- **Streaming is still absent** in the new schema-next — no event/stream root,
  no opens/belongs (word-boundary grep empty). The upgrade did NOT solve the
  Phase-1 streaming gap.

## Method

- **Empirical anchor (running):** `cargo build` of the cloud component
  (background) — does the new pipeline build end-to-end? This decides whether
  the model is solid enough to port lojix onto now.
- **Refresh workflow (background):**
  - A1 — the authoritative "how to compose a triad component now" guide (the
    new instructions), distilled from the cloud template + triad-runtime +
    schema-rust-next + component-triad.md → file `1`.
  - A2 — streaming analysis across the three layers (schema-next grammar,
    schema-rust-next emitter, triad-runtime runtime): a clear minimal fix with
    concrete diffs, OR a precise explanation + options + what's uncertain →
    file `2`. This is what the psyche specifically asked to resolve-or-explain.
  - B1 — the lojix port plan mapped piece-by-piece to the cloud template, plus
    drafting the two genuinely-new daemon schemas `lojix.nexus.schema` (the
    deploy-pipeline `EffectCommand` catalog) and `lojix.sema.schema` (the four
    tables) → file `3` + `drafts/`.
- **Synthesis (orchestrator):** combine the build result + the three files into
  a report on what's done, what builds, the streaming answer, and what to move
  forward with.

Phase-1 GREEN contracts (report 24) carry forward unchanged in shape — the
`lib.schema` naming already matches cloud; the port adds the crate scaffolding
(Cargo + build.rs + src) and the daemon plane schemas + runner wiring.
