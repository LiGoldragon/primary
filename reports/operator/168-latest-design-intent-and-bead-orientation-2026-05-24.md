# 168 — Latest design, intent, and bead orientation

*Kind: Orientation · Topic: latest designer reports, Spirit intent, and operator-ready beads · Date: 2026-05-24 · Lane: operator*

## Prompt classification

The psyche asked the operator to refresh on the latest designer reports
and intent, orient on beads available for operator work, and report back.
The durable principle captured through Spirit is record 373:
operator work starts from current intent, designer reports, and
actionable beads.

## Sources refreshed

Latest Spirit records reviewed through 373. The most operator-relevant
new records are:

- 359: `signal_channel!` deepens into the contract compiler surface:
  Tier 1 micro header, two-enum namespace, small-object derive,
  recursive `Help`, and command documentation hooks.
- 363-365: `Help` is a noun at the end of the NOTA path, and CLI
  help still obeys the single-NOTA-argument rule.
- 366-367: next-version-as-Cargo-dependency and macro convergence
  belong in the same `signal-frame-macros` extension surface.
- 369: `sema-upgrade` and version-handover merge into the `upgrade`
  triad; `version-projection` remains a library.
- 370: deleted reports live in version-control history, not the
  working tree.
- 371: drop `persona-` prefixes from supervised component crates
  except agent-harness components; `persona` itself keeps the name.
- 373: this orientation discipline.

Reports refreshed:

- `reports/designer/317-sema-upgrade-and-macro-convergence-audit/4-overview.md`
- `reports/designer/317-sema-upgrade-and-macro-convergence-audit/1-sema-upgrade-path-audit.md`
- `reports/designer/317-sema-upgrade-and-macro-convergence-audit/2-macro-current-state-audit.md`
- `reports/designer/317-sema-upgrade-and-macro-convergence-audit/3-next-as-dependency-design.md`
- `reports/designer/318-upgrade-merger-and-persona-prefix-rename/4-overview-and-bead-list.md`
- `reports/designer/314-aggressive-consolidation-sweep-2026-05-24.md`
- `reports/designer/315-design-sema-upgrade-and-handover-current-state.md`
- `reports/operator/166-sema-upgrade-and-schema-macro-current-state-2026-05-24.md`
- `reports/operator/167-recent-reports-and-intent-refresh-2026-05-24.md`
- `reports/second-designer/163-signal-sema-interaction-and-spirit-architecture-2026-05-24.md`
- `reports/third-designer/25-most-important-questions-2026-05-24/4-overview.md`
- `reports/second-designer/160-persona-prefix-removal-coordinated-rename-2026-05-23.md`
- `reports/second-designer/162-contract-repo-lens-and-consolidation/4b-consolidated-current-status.md`
- `reports/system-designer/34-mvp-and-sandbox-audit/5-overview.md`

## Current orientation

The latest design surface has three main operator tracks.

First, the macro track is now the highest-leverage foundation track.
`reports/designer/317-sema-upgrade-and-macro-convergence-audit/4-overview.md`
and Spirit record 367 say the old separate macro beads should be
handled as one coordinated implementation on `signal-frame` and
`signal-frame-macros`: section grammar, `LogVariant`, frame micro,
recursive Help, `signal_cli!`, and next-schema projection. This is
tracked by bead `primary-ezqx` (consolidated signal_channel +
signal_cli macro epic).

Second, the Spirit cutover path remains real but gated. The code
foundation exists: `version-projection`, `signal-version-handover`,
`owner-signal-version-handover`, `sema-engine` commit sequences,
`sema-upgrade` migration witness, `persona-spirit` private upgrade
socket, and `persona` handover code. The production cutover is still
blocked by Persona deploy, v0.1.0 retrofit, and the production
pre-migration step that aligns next-daemon commit-sequence markers.

Third, the rename and upgrade-merger wave is feasible but must be
sequenced. `reports/designer/318-upgrade-merger-and-persona-prefix-rename/4-overview-and-bead-list.md`
defines phase-1 supervised-component prefix drops, post-pilot Spirit
rename, and a later `upgrade` triad merger. This is not just a search
and replace; each triad rename must include dependent Cargo, source,
Nix, and active repository map changes in lockstep.

## Ready beads seen

One successful `bd ready --json` returned these operator-ready P1
items before the BEADS embedded backend locked under another process:

- `primary-ezqx`: consolidated macro epic. This is the most
  foundation-heavy task. It touches `signal-frame`, `signal-frame-macros`,
  and later `signal-cli`/consumer adoption.
- `primary-v5n2`: add `contract_section` grammar and auto-allocation
  to `signal-frame-macros`. This is a macro-epic slice, not a good
  isolated landing unless the epic explicitly splits.
- `primary-2cjv`: reshape `ExchangeFrame` and `StreamingFrame` to carry
  `micro: u64`. This is a concrete foundation change and probably the
  cleanest standalone code bead if not taking the whole epic.
- `primary-gvgj.3`: persona-agent daemon skeleton. Ready, but affected
  by the fresh naming decision that `persona-agent` likely becomes
  `agent`; start only after that naming is settled or build the new
  name directly.
- `primary-07ot`: persona-router delivery durability. Ready, but sits
  downstream of the agent abstraction direction and may be cleaner
  after the agent socket skeleton exists.
- `primary-gvgj`: persona-agent component triad epic. Ready as an epic,
  but too broad to start before the naming decision and skeleton slice.
- `primary-srmq`: lojix-daemon authenticated Nix flake resolution.
  Ready but belongs more to the system/deploy track.

Other ready items were system-specialist/system-designer surface
(`primary-kbmi.*`, `primary-54ti`) and should not be my first pickup
unless the psyche redirects the operator to that track.

## BEADS reliability note

The `bd ready` call succeeded once. Several later `bd list` / `bd show`
calls failed with:

`embeddeddolt: another process holds the exclusive lock on /home/li/primary/.beads/embeddeddolt`

This reinforces the note in `reports/designer/313-great-summary-and-handover-2026-05-24.md`
that BEADS needs a server-backed or otherwise concurrent-safe mode if
multiple agents are going to orient at the same time.

## Recommended operator pickup

The best first pickup is `primary-2cjv` (signal-frame frame reshape).
It is concrete, foundation-level, and feeds the macro convergence epic
without forcing the entire macro redesign into one first step. It should
be claimed with a task lock plus `/git/github.com/LiGoldragon/signal-frame`
and tested with cargo plus Nix using `--option max-jobs 0`.

If the psyche wants the broader macro push immediately, claim
`primary-ezqx` instead and implement it as the report describes:
one coordinated PR-shaped landing across `signal-frame` and
`signal-frame-macros`, not isolated partial beads.

I would avoid starting `primary-gvgj.3` until the `agent` naming
confirmation is absorbed into the bead body or the repo names are
settled. Starting it under `persona-agent` now risks immediate churn.

I would avoid the /318 rename wave until the designer's proposed R/U/C
beads actually exist in BEADS or the psyche directly tells operator to
file and execute them. The report is implementation-ready in shape, but
the tracking substrate is not yet aligned.

## Still-relevant questions

1. For the macro track: should I take `primary-2cjv` as the first
   standalone foundation slice, or claim `primary-ezqx` and land the
   full macro convergence as one larger pass?
2. For naming: is the `agent` triad name now settled enough that
   operators should implement the daemon skeleton under `agent`,
   `signal-agent`, and `owner-signal-agent` rather than
   `persona-agent`?
3. For /318 execution: should operator file the R1-R12, U1-U7, and
   C1-C3 beads from the report now, or wait for designer to finish the
   bead filing pass?
4. For BEADS infrastructure: should system-specialist take a task to
   remove the embedded single-writer bottleneck before more parallel
   operator waves rely on `bd ready`?
