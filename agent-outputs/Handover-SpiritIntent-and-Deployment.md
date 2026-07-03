# Handover — Spirit intent doctrine (settled) + open deployment tails

## Original direction — settled and live
The session's goal was to sharpen what "intent" means so agents stop capturing
matter (mechanical/architectural defaults) as intent. It is complete.

Settled definition (canonical home: the `intent-log` skill):
- Intent is the rare, orienting will of the psyche — an aim, value, or belief he
  holds against his own convenience and that bends a whole class of downstream
  choices, like a North Star. It is not a decision, default, wish, or rule;
  those are matter. Capture is the exception; when unsure, it is not intent —
  ask.
- Five-gate test (capture only if all hold): (1) aim/value/belief, not a
  how/default/rule; (2) unbending, held against cost — "for the spirit, not for
  profit"; (3) orienting — bends a class of decisions, not one case; (4) its
  "why" is a value, not an engineering/efficiency tradeoff; (5) from the psyche,
  felt — not agent-synthesized.
- Halos (read as intent, are matter): rule-grammar (must/never), an
  engineering-justification "why", vivid phrasing, a sensible one-off default,
  agent/Spirit-operation procedure.
- Worked example: "new repos default to public" → matter.

Live on: `intent-log` (canonical), `intent-clarification`, `intent-manifestation`,
the AGENTS.md Intent section, and the spirit repo `manual.md` §2 (with a
Castaneda grounding subsection). The old weak definition record `qjrf` is
retired. The Spirit **guardian prompt** now judges captures against this
definition and is running live on ouranos (spirit rev `7b0770642ab1`).

Naming: the word "intent" stays. ("lodestar" was the only alternative left as a
possible future gloss; not pursued.) Definition-of-intent lives in the
skill/guardian, not as a Spirit record (it is Spirit-operation doctrine = matter).

## Doctrine added (matter, in skills)
- Orchestration skill: dispatch a fresh subagent on a topic change; reuse only on
  direct continuation with the agent's context under ~100–150k tokens.
- `micro-components` skill, `## Deployment independence`: component logic is
  deployment/environment-agnostic; deployment/cluster/environment/host data
  enters as configuration injected at the edge, never baked into logic; test
  clusters live only in test code.

## Settled psyche decisions carried
- CriomOS is to be deployment-agnostic; no cluster-/deployment-specific data
  baked into component logic (recorded in CriomOS ARCHITECTURE + the
  `micro-components` skill).
- A lojix production daemon carries NO baked test-op default; test fixtures live
  only in test code.

## Completed changes (landed, not deployed)
- Intent doctrine + guardian prompt (above) — live.
- Deploy activation bug fixed: adopted the hand-placed `~/.ssh/config` into
  home-manager and migrated orchestrate-daemon to a systemd `--user` unit. lojix's
  Activate-failure mislabel fixed (`ActivationFailed` now distinct from
  `BuilderUnreachable`).
- "No baked test default" landed forward as **lojix 0.4.1** (`main` @ `9f42435`)
  + CriomOS consumer (`main` @ `92c45b58`; `lojix.nix` field 7 = `NoTestDefaults`;
  lojix pin bumped to 0.4.1). Verified green. Not deployed.

## Open (tracked)
- **`primary-h945` (P1):** the live System deploy to ouranos is blocked by a
  separate system-deploy `NOPERMISSION` issue. Until a matching system generation
  lands, the guardian prompt is live but **not reboot-persistent** (reverts to the
  prior prompt on reboot), and the lojix 0.4.x daemon is not yet running live.
- **`primary-dq1r` (P2):** suggested CriomOS build-time round-trip flake check —
  CriomOS hand-authors the daemon config NOTA with no build-time guard against the
  pinned lojix writer schema (drift would fail only at daemon startup).
- criomos-home's own transitive `lojix` flake input is still at 0.3.10 — separate
  input, bump when criomos-home next moves.
- Cross-component deployment-agnostic **sweep** (map where environment-specific
  data is baked into logic across all components) — offered, never scoped.

## Artifact pointers
- `agent-outputs/LojixDeployAuthMap/Scout-SituationalMap.md` — deploy/auth map.
- `agent-outputs/LojixDeployAuthMap/Scout-DeploymentAgnosticProposal.md` — the
  deployment-agnostic redesign proposal and its decision points.
- `agent-outputs/LojixDeployAuthMap/OperatingSystemImplementer-LandingEvidence.md`
  — guardian-prompt-live + activate-fix evidence.
- Repos at handover: skills `main` (intent-log sharpening, orchestration
  fresh-vs-reuse, micro-components deployment-independence), spirit `main`
  (manual §2 + guardian prompt, rev `7b0770642ab1`), lojix `main` @ `9f42435`
  (0.4.1), CriomOS `main` @ `92c45b58`.
