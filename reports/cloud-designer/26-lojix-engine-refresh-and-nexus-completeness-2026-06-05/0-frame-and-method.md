# 26 — lojix engine refresh + Nexus-for-lojix completeness — frame & method

2026-06-05. cloud-designer lane. Meta-report directory: orchestrator
frame here, sub-agent findings numbered 1–5, adversarial review `6`,
synthesis `7-overview.md` (highest-numbered = the session synthesis).

## What the psyche asked (this turn)

> "Refresh, get some fresh intent, and get a fresh look at the work on
> the new logics again, especially with the whole engine rewrite thing
> and defining Nexus for logics so that all of its internal operations
> are defined by the schema interface. And properly identifying all of
> the functionality and what kind of database runtime state it needs to
> have. And you can see the decisions I've made on how to handle the
> more advanced horizon variables by splitting horizons into two logical
> parts so that we keep the first raw horizon evaluation more clean and
> maintainable and possibly this keeps the door open for better
> integration into a larger component system later on."

Reference handed in: `reports/designer/534-horizon-raw-pretty-split.md`.

## Three concrete deliverables inside the ask

1. **Fresh situation** — where the lojix engine-rewrite stands *now*
   (the triad-port lib+bins compile GREEN as of this turn; daemon
   two-socket loop being finalized in parallel by workflow `w8tlwkbx4`).
2. **Nexus-for-lojix completeness** — is *every* internal operation of
   the lojix daemon a declared Nexus verb+object in `nexus.schema`
   (record `z6qu`: nexus = engine feature catalog)? Audit the catalog
   against the full functionality inventory; list gaps + redundancies.
3. **Runtime-state model** — properly identify *all* the functionality
   and *all* the durable database state lojix needs (the SEMA plane:
   live set, GC roots, event log, container lifecycle). Verify
   completeness and type-reuse minimalism (`a2t4`).

Plus the **raw/pretty horizon boundary** reflection: how the
`9p8v`/`avvh` split shapes what lojix consumes from horizon.

## Intent already captured this turn

- `9p8v` (designer, High) — the raw/pretty split decision (in 534).
- `avvh` (this lane, High, gap-fill) — the split is *also* a
  forward-integration seam: raw horizon stays a clean typed model that
  can later be promoted to a real component; links `x8iv`/`tvbn`.

## Anchor intent records (finders read these via the Spirit CLI)

`z6qu` nexus=feature-catalog · `a2t4` minimal-horizon + type-reuse ·
`tvbn` rewrite charter (horizon=hack, lojix=full triad) · `fe2j`
port-first sequencing · `qkvx` typed-source-first · `vu2k`
horizon types-only-module schema shape · `9p8v`+`avvh` raw/pretty ·
`242o` ouranos swap/zram via cluster-data.

## Method — five parallel finders, then verify, then synthesize

1. **Fresh intent sweep** — full Spirit sweep on lojix/horizon/nexus/
   sema/engine-rewrite; agglomerate the current picture + flag stale
   records.
2. **Functionality inventory** — enumerate every operation the deploy
   stack performs, sourced from legacy Stack A (`lojix-cli/src/*.rs`)
   + lojix ARCHITECTURE.md + the contracts.
3. **Nexus completeness audit** — map every `nexus.schema` verb against
   the inventory; gaps + redundancies.
4. **Runtime-state model** — the SEMA plane: do the four tables capture
   all durable state? type-reuse minimalism check.
5. **Raw/pretty horizon boundary** — how the split reflects into the
   lojix↔horizon consumption boundary and the later-promotion seam.

Then `6` adversarial review of the completeness claims, then `7`
synthesis with a prioritized actionable list toward cutover.

Constraint given to every finder: **read-only analysis + write your own
report file only — no `cargo`/`jj`** (a parallel workflow is editing the
daemon source; avoid build/lock contention).
