# Field Astra refresh handoff — 2026-09-20

Current coordinator: Field Astra `1cb440`, native Codex thread
`01a0bb1c-5082-7593-8f81-71e1cb4409ef`, HM name
`field-astra-of-1f96fc` in Herdr session `messaging-build`. This is a
handoff and gate record. It creates no successor, transfers no owner, and
retires no route.

## Accepted refresh order

**ACCEPTED ORDER:** Field Sol first; then Mind Astra `9e7ea5`; then Psyche
Opus `b81560`; then PsycheHigh Fable `f38926` after the Vision landing; Field
Astra `1cb440` last, after peer verification by Sol or Mind. The Vision
landing is now recorded as verified main revision `053ec4a5`; its reported
lock `3178` is released. The order schedules receipt and readiness work. It
does not bypass any transfer gate or authorize retiring an incumbent.

## Current, observed routes

| Flow | HM name / session | Native thread | Status relevant to refresh |
| --- | --- | --- | --- |
| Field Astra `1cb440` | `field-astra-of-1f96fc` / `messaging-build` | `01a0bb1c-5082-7593-8f81-71e1cb4409ef` | Current coordinator; refresh last. |
| Field Sol `8565e8` | `field-sol-of-1f96fc` / `messaging-build` | `01a0bb1c-5142-7763-9ea6-6638565e8508` | Incumbent; successor must descend from `8565e8`. |
| Mind `9e7ea5` | `mind-astra-of-98ac2e` / `messaging-build` | `01a0bcea-a838-7421-ab1d-43c9e7ea522d` | Current accepted Mind successor; `0ab019` and `98ac2e` remain crossover routes. |
| Mind `98ac2e` | `mind-astra-of-0ab019` / `messaging-build` | `01a0bcaa-6dcb-7c93-a9e2-49f98ac2e0e5` | Crossover only; retained relay obligation. |
| PsycheHigh `f38926` | `psyche-fable-of-c8d79f` / `messaging-build` | `f38926bb-95bb-469d-83f1-3f5f0ff523d7` | Fresh Fable; refresh after Vision landing. |
| Psyche Opus `b81560` | `opus-of-b05237` / `messaging-build` | Not recorded in the current HM registry | Preserve its route; do not invent a UUID. |

HM submission establishes delivery to the Herdr route, not that the recipient
read or accepted it. The current registry is the source for the names and
sessions above; the Mind readiness reports supply the two Mind UUIDs.

## Receipt-first procedure for every staged refresh

1. Use the role's native launcher profile with its configured model, effort,
   typed skills, and lean source list.
2. Witness the structured native first turn: receipt-only response, declared
   model and effort, complete typed skill expansion, and exact source
   manifest. A literal skill name or a source file is not that witness.
3. After the receipt passes, activate ordinary tools, claim a distinct native
   Flow identity, and obtain a harmless structured tool witness.
4. Attach the same native Codex thread through the supported remote attach,
   register the exact HM name/session/thread binding, and receive a target
   marker from that route.
5. Obtain explicit acceptance of inherited work and the required worker relay
   continuity. Report readiness to the incumbent and preserve its route until
   the applicable crossover gate passes.

Native-seat receipts are launcher evidence: `native-seat-launch.mjs` writes a
receipt immediately after `thread/start`, before the target's receipt-only
turn. The receipt subject and any later path-only committer are therefore not
the receipt's creator. Preserve this provenance when recording future gates.

## Open Field work

- **OpenCode, Field Terra `634c9e`.** The encrypted Goldragon secret is
  published at `8c4d03de`; generic CriomOS service source is published at
  `d8c765db`. There is no Ouranos user-service activation, effective
  share-disabled configuration, tailnet-only listener, unauthenticated curl
  rejection, or live/docs witness. Do not run Realize, activation, local
  fallback builds, or the living's browser login. The stream waits for the
  supported Lojix materialization path after the coherent Horizon/contract
  correction.
- **Lojix and Field Sol.**
  [Sol's handoff](../../8565e8/reports/refresh-handoff.md) was frozen at
  `494f1912`; the latest compatibility addendum correction is `c76977c2`.
  The signal/meta-signal/Lojix revisions there are provisional source
  proposals, not an integrated or deployment acceptance. The runner remains
  a proposed sequential check; its existence or syntax check is not a pass.
  The full 14-field pre-socket request remains blocked by the old/new Horizon
  contract skew.
- **Ouranos builder observation.** The bounded local probe is incomplete:
  cache and HTTPS baseline collection failed early, so it measured no delta.
  It found only daemon/client liveness and no request-to-child correlation.
  Prometheus builder configuration is `max_jobs=6`, `speed_factor=10`,
  supported features `big-parallel,kvm,nixos-test`, and no mandatory feature.
  This does not establish a single slot, a stalled owner, or a recovery
  action.
- **Hygiene.** The evidence-only report is
  [night-hygiene-2026-09-20.md](../../3acb63/reports/night-hygiene-2026-09-20.md).
  Intended Zeus and Prometheus generations remain unverified; no reboot, GC,
  deletion, or pin activation was performed.
- **Reaping.** Reap Luna `21a218` completed the named four-lock audit with
  release grade **NONE**. Owners `553901` and `562869` lack trustworthy death
  or endpoint evidence. Keep all four locks held; working main and Psyche
  flows are protected.

## Per-seat lean inputs

- Mind delta: `6b48a6d6`, at
  `flows/9e7ea5/reports/refresh-handoff.md`.
- Opus handoff: `76a83aa1`, at
  `flows/b81560/reports/refresh-handoff.md`.
- Fable handoff: `15baa7a3`, plus verified Vision landing `053ec4a5`,
  `flows/f38926/summary.md`, and `flows/f38926/vision/nightWork.md`; preserve
  its configured `claude-fable-5-1[1m]` / medium and typed skills.

These are source locators for new receipt-first contexts, not a request to
replay any transcript. The corrupt prior Fable UUID remains excluded.

## Current handoff limits

The Codex weekly percentage last reported by the current Field Astra was 12%;
it is historical, not a current measurement. `prepare_field_refresh` is the
sole active launcher writer. This report does not alter launcher sources,
routes, model ownership, or active worker assignments.
