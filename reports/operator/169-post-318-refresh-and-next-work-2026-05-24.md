# 169 — Post-/318 Refresh And Next Work

*Kind: Refresh · Topic: post-/318 implementation state, new intent, and next operator work · Date: 2026-05-24 · Lane: operator*

## Prompt Classification

The psyche asked for a refresh to see whether new material helps the
operator continue, and said the result will be forwarded to designer
for review and guidance. I treated this as an operational refresh
directive, not a durable new workspace rule. No Spirit record was
created for this turn.

## Sources Refreshed

- `ESSENCE.md`
- `INTENT.md`
- `repos/lore/AGENTS.md`
- `orchestrate/AGENTS.md`
- `skills/operator.md`
- `skills/reporting.md`
- `skills/beads.md`
- `skills/spirit-cli.md`
- `skills/component-triad.md`
- `skills/jj.md`
- `skills/nix-usage.md`
- Spirit records through 387
- `reports/designer/318-upgrade-merger-and-persona-prefix-rename/`
- `reports/designer/317-sema-upgrade-and-macro-convergence-audit/`
- `reports/operator/167-recent-reports-and-intent-refresh-2026-05-24.md`
- `reports/operator/168-latest-design-intent-and-bead-orientation-2026-05-24.md`
- `reports/second-designer/163-signal-sema-interaction-and-spirit-architecture-2026-05-24.md`
- Open and ready BEADS state as of this refresh

## New Material Since Operator /168

Spirit records 375 through 387 were created by the /318 execution
wave, mostly by worker lanes. They do not redirect the architecture;
they confirm implementation discipline for the work just landed:
R10 agent-contract rename prep, U1 upgrade scaffold as scaffold-only,
U6 version-projection rename constraints, jj inline workflow, and
bounded verification expectations.

The main new actionable state is therefore in BEADS, not in new
designer prose: the /318 child beads that could be executed by this
operator wave are now closed, and the remaining /318 execution beads
are blocked by Spirit cutover and Persona/CriomOS-home repin order.

## /318 State After This Operator Wave

Completed in this wave:

- `primary-l3h5.2` — `signal-upgrade` working contract merger.
- `primary-l3h5.3` — `owner-signal-upgrade` owner contract merger.
- `primary-l3h5.4` — sema-upgrade migration/catalogue substance and
  Persona handover driver moved into `upgrade`; follow-up cleanup
  retired the old `sema-upgrade` prototype library surface.
- `primary-l3h5.5` — Persona narrowed back to process lifecycle and
  versioned unit start; direct upgrade orchestration moved out.
- `primary-l3h5.6` — `version-projection` renamed runtime lookup
  types; `upgrade::MigrationCatalogue` landed.
- `primary-wpnd` — `persona-sema` fully retired: GitHub repo deleted,
  local checkout removed, active repo map and storage skill cleaned.
- `primary-a0m7` — empty `signal-persona-terminal-test` checkout
  removed.

Remaining /318 items:

- `primary-0m1u.11` — Spirit triad rename after cutover. Blocked by
  `primary-x3ci`, the Spirit v0.1.1 production cutover.
- `primary-0m1u.12` — Persona meta catch-up and CriomOS-home repin.
  Blocked by R11.
- `primary-l3h5.7` — CriomOS-home repin for the upgrade triad
  deployment. Blocked by R12.

The /318 parent epics remain open because the blocked tail is real.
The operator should not treat U7 or R12 as free implementation work
until the Spirit cutover and naming order move.

## Current Ready Work

The most relevant ready operator beads now are not the remaining
/318 tail. The ready list points back to the macro foundation:

- `primary-ezqx` — consolidated `signal_channel!` + `signal_cli!`
  macro extension epic. This is the whole convergence surface:
  `LogVariant`, recursive `Help`, golden-ratio namespace allocation,
  `frame_micro`, and Tier-1 always-on behavior.
- `primary-2cjv` — reshape `ExchangeFrame` and `StreamingFrame` to
  carry the `micro: u64` prefix field. This is the cleanest
  standalone foundation slice if the designer wants a smaller next
  operator step.
- `primary-v5n2` and `primary-8r1j` — macro sub-slices that are
  ready, but should probably be treated as children of
  `primary-ezqx` rather than independently re-planned.

The persona-agent track is also visible as ready, especially
`primary-gvgj.3`, but it is still naming-sensitive. Spirit record
371 and the /318 rename wave mean any start there should use the
settled `agent` vocabulary rather than a soon-to-be-renamed
`persona-agent` shape.

## Operator Recommendation

The best continuation is one of two paths:

1. If designer wants the smallest high-signal code slice, take
   `primary-2cjv` and land `micro: u64` on `signal-frame` frames
   with full cargo and Nix witnesses.
2. If designer wants fewer intermediate states and one coherent
   macro landing, take `primary-ezqx` and implement the macro
   convergence as a single coordinated operator pass.

I would not continue the /318 rename/deploy tail directly from here.
The remaining /318 beads are correctly blocked: Spirit cutover first,
then Spirit rename, then Persona/CriomOS-home repin, then upgrade
triad deployment repin.

## Questions For Designer

1. Should the next operator slice be `primary-2cjv` as a narrow
   `signal-frame` micro-field foundation, or the larger
   `primary-ezqx` macro convergence epic?
2. Should `primary-v5n2`, `primary-8r1j`, `primary-3cl1`,
   `primary-l02o`, `primary-915w`, and related macro beads be
   explicitly folded under `primary-ezqx` before implementation,
   or can operator proceed with `primary-ezqx` as the coordination
   umbrella?
3. For the agent track, is `agent` fully settled as the implementation
   name now, such that new daemon work should start under `agent`,
   `signal-agent`, and `owner-signal-agent` rather than any
   `persona-agent` placeholder?
4. Should designer review the completed /318 U2-U6 commits before
   operator starts macro work, or is the bead closure plus passing
   Nix/cargo evidence enough to move on?

