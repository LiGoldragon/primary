# 74 — Engine-forward exploration (frame + method)

Kind: meta-report directory (frame + 6 area mappers + prioritized backlog + completeness/foundation critique + orchestrator overview).
Topics: engine, cloud, persona, supervisor, introspect, schema-daemon, triad-runtime, runner, lojix, spirit, port-readiness, prioritization.
Date: 2026-06-05.
Role: system-designer (orchestrator).

## Psyche directive

"Acquire fresh intent and then do a multi-agent search exploration on where you
could put your effort to move the engine forward, especially the parts we've been
working on the most — the cloud. I would like also to have Orchestrate running
persona, the manager of the whole thing, the introspector, the schema daemon, all
of these things. Do a full audit research exploration on how you could actually
move things forward — even though we're still shifting the foundation a bit — but
at least start porting the code and make it ready. We have a huge amount of tokens
to spend till tomorrow, so let's get ahead of the work we'll have to do when the
foundation stabilizes more. It's pretty good already. There should be a good
direction to how I want things to be, so there should be lots to do."

So: an exhaustive, source-grounded exploration of WHERE to put effort to move the
engine toward a **running orchestrated system**, with a prioritized, actionable
backlog that distinguishes **safe-to-port-now** (foundation-stable) from
**prep / wait-on-foundation** (rework risk). The token budget is large; be
thorough. Get ahead of the work.

## The target state (captured this session)

`(Spirit Decision mazv)` [The engine target running state is a live orchestrated
system: persona — the manager and supervisor of the whole thing — runs and
supervises the introspector (persona-introspect), the schema daemon, and the other
triad components together as one running orchestrated whole, not just proven
in-tree.]

## Fresh intent anchors

- `(Spirit Decision 7ca4)` [Extract the generic triad runtime runner now: every
  schema-derived daemon plugs component logic into shared Signal/Nexus/SEMA runner
  objects instead of hand-writing daemon boilerplate.] — THE lever.
- `(Spirit Decision rpr5)` [the bundled triad runner adapter is generated glue;
  component authors implement the three plane engines + effect handler + budget
  reply, not a fourth engine surface.]
- `(Spirit Principle tirp)` [SEMA owns DB, Nexus owns decisions, Signal owns
  communication; daemon code minimal beyond startup + runner wiring.]
- `(Spirit Decision bp8k, Maximum)` [for the cloud component, ignore the earlier
  prototype as authority; write fresh from the current desired shape.]
- `(Spirit Decision vnnx)` [the cloud port uses TWO schemas — signal-cloud (working,
  peer, read-only Observe+Validate) + meta-signal-cloud (policy, owner-only, the
  eight account/plan mutations) — each emitting Signal/Nexus/SEMA, sharing record
  types; runtime imports both, runs two listeners.]
- `(Spirit Clarification 545o / Correction 4tas, both Maximum)` [a cloud schema
  triad is not complete merely because runtime plane schema files exist; if no
  generator blocker remains, IMPLEMENT the engine; name blockers explicitly rather
  than leaving concept placeholders.]
- `(Spirit Principle z6qu, VeryHigh)` [the Nexus schema is the engine's visible
  internal feature catalog: every engine feature is a declared Nexus verb+object.]
- `(Spirit Correction lc2r)` [a component triad is ≥3 separate plane schema files;
  Signal wire contract in the contract repos (wire-only); Nexus + SEMA plane
  schemas are separate files inside the component daemon crate.]
- `(Spirit Decision 7x50)` [bootstrap policy authored as NOTA source, consumed as a
  pre-encoded typed binary artifact at first start; later changes via meta-signal.]
- Asschema removal is COMPLETE in code (report 73 §7); structural macro node landed.

## The six exploration areas (component → repos)

| File | Area | Repos |
|---|---|---|
| `1-cloud.md` | Cloud two-contract triad port (psyche's #1 emphasis) | `cloud`, `signal-cloud`, `meta-signal-cloud` |
| `2-persona-supervisor.md` | Persona = manager/supervisor + the orchestrated running system | `persona`, `owner-signal-persona`, `signal-engine-management`, `orchestrate`, `mind` |
| `3-introspect.md` | The introspector | `introspect`, `signal-introspect`, `signal-router` |
| `4-schema-daemon.md` | The schema stack as a running daemon | `schema`, `schema-next`, `schema-rust-next`, `nota-next` |
| `5-triad-runner.md` | The shared triad runtime runner (the lever, `7ca4`) | `triad-runtime`, the spirit pilot as reference |
| `6-deploy-and-pilot.md` | Deploy stack adoption + pilot readiness | `lojix`, `signal-lojix`, `spirit` |

Each mapper: current state (source-grounded, **landed vs proposed**), the concrete
move-forward / port / make-ready work items, and a per-item **foundation-stability
verdict** — safe-to-port-now vs prep vs wait-on-foundation (and WHY).

Then: `7-prioritized-backlog.md` (synthesis — ranked where-to-put-effort with the
critical path) and `8-overview.md` (orchestrator psyche-facing synthesis,
incorporating the completeness + foundation-stability critiques).

## Discipline

- Mappers are READ-ONLY; write ONE numbered report; no edits/commits/mutating ops.
  Verify every file/type/record citation against source. Landed-vs-proposed honesty.
- The foundation IS still shifting — every "safe-to-port-now" claim must justify why
  it won't be rework (cite what's stable: e.g. the wire contracts, the runner shape,
  asschema-removal-done). Do NOT recommend porting onto sand.
- Cite intent as bracket-quoted summaries with the current short code (note: codes
  re-minted recently — prefer description-first).
- NOTA discipline if quoting: bracket strings only, positional, no quotes.
