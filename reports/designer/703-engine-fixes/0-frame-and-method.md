# 703 — engine fixes: decisions, research, and implementation (frame)

The psyche, after report 702 (the deep engine analysis): *"fix everything
with your leans. research if needed."* This session turns the 702 findings
into fixes. The 702 beads split across three lanes; this frame records who
does what and why, so "fix everything" honors the hard lane override
(operators own code-repo `main` + integration; designers ship `next`
branches in `~/wt`; system-operator owns deploy/fleet).

## The split

**Designer-lane — I implement directly (with my leans):**
- The schema-language code fixes, shipped as `~/wt` feature branches proven
  green (the established pattern — impl-reference shipped this way, operator
  merged): (a) collapse schema-next to one lowering engine so the `schema-1`
  nested-namespace divergence cannot recur; (b) wire schema-rust-next to
  consume the `{| |}` impl catalog (or rule it deferred — research first).
- Primary docs/truth-pins (active-repositories) — directly on main.
- The design rulings that *apply existing intent* (no new Spirit): the
  `m0p2` matcher classification; the `{| |}` catalog consumer decision.
- The two completeness audits the 702 lanes missed (upgrade daemon;
  mentci-lib).

**Operator-lane — firm leaned constraints (operator owns main + is actively
mid-flight on the loop; report 4c2c5b8f landed during the 702 run):** the
propagation-loop integration, sharpened by the 702 fracture finding —
rebase `criome-gated-propagation-loop` onto spirit `aa7e9b0`, call the
*production* restore method, add a daemon caller + criome socket gate, mirror
E5, router m0p2 wire; plus schema-rust-next panic→typed-error, criome BLS
aggregate, criome free-fn→method, mentci durable SEMA + egress.

**System-operator-lane — firm leaned constraint + research:** resolve the
kameo fork split-brain (the #1 cross-stack risk) — one runtime for the
whole fleet + triad-runtime pin bump + a nix flake-check witness; this is
also the precondition for the multi-machine cluster (can't cluster a fleet
running two actor runtimes).

## Decisions I am taking with my leans (no longer open questions)

The psyche delegated these ("with your leans"); research makes each
concrete. Documented here as design decisions (ratifiable), not captured as
Spirit (they apply existing intent / are my calls, not psyche intent):

1. **`m0p2` classification** — lean: criome's surviving snapshot filter is
   observation/audit (keep); the time-pulse matcher needs the research
   verdict (file `2`).
2. **`{| |}` catalog consumer** — lean: wire schema-rust-next to consume it
   (file `3` confirms or overturns vs the parallel `scalar_like` path).
3. **Fleet runtime** — lean: everyone onto the LiGoldragon kameo fork (it
   exists because router's lifecycle needs drove it); file `1` verifies the
   fork contents + the spirit/mirror migration cost + upstreaming option.
4. **First cluster hosts** — lean: proceed with a concrete three from the
   host inventory unless redirected (file `4`); a 2-of-3 needs three.

## Method

Phase 1 — a parallel research-and-decide workflow: five deep agents, each
resolves one decision/audit against real code and returns a firm
recommendation, writing its numbered file. Phase 2 — a brief-synthesis agent
folds the leaned decisions into the operator brief (`6`) and system-operator
brief (`7`). Phase 3 (after research, in the main thread) — I implement the
designer-lane code fixes on feature branches proven green, fix the primary
docs, and finalize the decisions summary. Report layout:

| File | Content | Lane |
|---|---|---|
| `1-kameo-fleet-runtime.md` | fork analysis + firm fleet-runtime decision + pin/nix plan | research → system-operator |
| `2-m0p2-matcher-classification.md` | classify criome's surviving matchers; the ruling | research → designer ruling |
| `3-impl-catalog-consumer.md` | catalog vs scalar_like; the consumer design | research → designer impl |
| `4-first-cluster-hosts.md` | host inventory + the concrete first three | research → deploy |
| `5-upgrade-and-mentci-lib-audit.md` | the two completeness-gap audits | research → designer |
| `6-operator-brief.md` | the sharpened propagation-loop + code-fix brief | synthesis → operator |
| `7-system-operator-brief.md` | the kameo-fleet + nix-witness brief | synthesis → system-operator |
| `8-decisions-and-implementation.md` | the firmed decisions + the shipped designer branches | designer (me) |
