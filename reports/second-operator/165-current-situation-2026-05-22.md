# Current Situation

Report kind: situation
Topic: second-operator current working surface after heavy context maintenance
Date: 2026-05-22
Lane: second-operator

## Where We Are

The lane is back to a small active report set. The old
`operator-assistant` reports were restored under `second-operator`,
then re-read and folded forward. The active context after this pass is:

- `reports/second-operator/165-current-situation-2026-05-22.md`
  - this report, the desk-level current state.
- `reports/second-operator/166-review-persona-orchestrate-migration-2026-05-22.md`
  - the current Orchestrate implementation and migration target.
- `reports/second-operator/163-lane-registry-implementation-result-2026-05-22.md`
  - fresh implementation result retained as an audit source for the
  lane-registry slice.
- `reports/second-operator/167-review-persona-engine-backlog-2026-05-22.md`
  - the old Persona engine phase-3 residue, repackaged against current
  state.
- `reports/second-operator/168-review-mind-router-policy-2026-05-22.md`
  - Mind, Router, channel authority, and owner-signal shape.
- `reports/second-operator/169-review-criome-lojix-authorization-2026-05-22.md`
  - Criome/Lojix authorization residue.

Everything else in this lane was a working witness or transitional
handover. Its live substance is now in the six reports above, current
repo commits, architecture files, skills, or beads.

## Main Work Now

The main second-operator target is still bead `primary-c620`: migrate
the `persona-orchestrate` triad to the current foundation.

The lane-registry slice is done. Bead `primary-ao1q` is closed. The
current code state is:

- `signal-persona-orchestrate` has role-vector lane vocabulary,
  `Observation::Lanes`, and clean current `signal-frame` macro output.
- `owner-signal-persona-orchestrate` has lane `Register`, lane
  `Retire`, and `SetAuthority`.
- `persona-orchestrate` has a `lane_registry` table and owner/ordinary
  handlers for the lane registry.
- the CLI still talks only to the daemon, and the constraint tests
  protect that boundary.

The next useful implementation is not more report cleanup. It is the
Orchestrate executor migration:

1. add daemon-local `Command` and `Effect` types;
2. route ordinary and owner socket execution through `signal-executor`;
3. project commands and effects through `ToSemaOperation` and
   `ToSemaOutcome`;
4. replace the CLI's working-first-owner-second decode path with
   generated head routing when the macro surface is ready;
5. add constraint tests proving the daemon no longer bypasses the
   executor path.

## Designer And Operator Report Absorption

Absorbed the current designer/operator surface after the lane-registry
slice:

- `reports/designer/249`, `/257`, `/263`, `/264`, `/266`, `/268`,
  `/270`, `/271`, `/273`, `/274`, `/278`, `/279`, `/280`.
- `reports/operator/136`, `/150`, `/151`, `/153`, `/154`, `/155`,
  `/156`.
- `reports/second-designer/130` through `/150`, with focus on
  Orchestrate `/137`, lane registry `/146`-`/149`, recording `/145`
  and `/148`, and identity/runtime functions `/150`.
- `reports/second-operator-assistant/7` through `/11`.
- `reports/third-designer/14` through `/16`.

The short synthesis:

- **Spirit cutover is the active system blocker.** Both v0.1.0 and
  v0.1.1 daemons are running; v0.1.1 has a migrated database through
  record 146; unsuffixed `spirit` still writes to v0.1.0. The open
  cutover choice is dual-write wrapper, immediate default flip with
  v0.1.0 fallback, or high-water-mark replay before allowing more old
  writes.
- **Sema-upgrade is the durable migration substrate.** The prototype
  exists; the real daemon and thin `upgrade` CLI are the next durable
  shape. Open design pressure remains self-upgrade/bootstrap,
  commit-sequence scope, and typed rejection fanout.
- **Schema identity moved from semver to content address.** The
  schema hash is the per-component Blake3 hash over the canonical
  NOTA schema, including public signal types and private runtime
  storage wrappers.
- **The v4 component migration recipe is stable.** Each component
  needs contract-local verbs and observable blocks, then daemon-local
  `Command`/`Effect`, `ToSemaOperation`/`ToSemaOutcome`, `Lowering`,
  `CommandExecutor`, and executor-centered socket routing.
- **Orchestrate remains the second-operator implementation target.**
  Lane registry landed. The next slice is executor migration and
  owner-signal shape cleanup; do not expand the owner contract by
  copying lock-helper or router mechanics.
- **Role identity has changed underneath lane registry.** Lanes are
  windows into one role agent; `operator` and `second-operator` share
  identity. Orchestrate eventually needs `lane_registry`,
  `lane_sessions`, and `role_identities` tables rather than treating a
  lane as an agent.
- **Mind decides; Orchestrate enacts.** Channel choreography decisions
  live in Mind; Orchestrate owns Router and turns high-level Mind
  decisions into low-level Router owner-signal calls.
- **Lane retirement has a report conflict.** `reports/second-designer/149`
  says retired lane identifiers should be reserved forever. Newer
  psyche clarification to this lane says retired identifiers can go
  away for now. I treat the newer clarification as current for the
  present MVP unless designer reopens it.

## Current Questions For Psyche

1. For Spirit cutover, should unsuffixed `spirit` dual-write to both
   v0.1.0 and v0.1.1 during migration, flip immediately to v0.1.1
   with v0.1.0 as read-only fallback, or block old writes until
   sema-upgrade has high-water-mark replay?
2. Should second-operator proceed with Orchestrate executor migration
   now, or should this lane pause until the Spirit/sema-upgrade cutover
   finishes?
3. For Orchestrate's next owner-signal pass, what high-level
   Mind-to-Orchestrate verbs should carry channel-choreography
   decisions before Orchestrate calls Router's `Grant`/`Extend`/
   `Revoke`/`Deny`?
4. Should `reports/second-designer/149` be treated as superseded on
   retired lane identifier tombstones by the newer clarification, or
   do you want designer to re-audit that point explicitly?
5. Should this lane keep a simple report-read ledger section until the
   eventual agent-checkout command exists, or is this absorption note
   enough for now?

## Delta Absorption After Third-Designer 17

Freshly absorbed after the first absorption commit:

- `reports/third-designer/17-situation-and-questions-2026-05-22.md`
  - confirms the same active priorities, adds that
    `third-designer` is now a structural parallel-main lane, and
    states the designer-side question list more aggressively.
- `reports/designer/214-criome-architecture-record-2026-05-17.md`
  - keeper for Criome's Unix-user security boundary, owner socket,
    encrypted owner session, and future `owner-signal-criome`.
- `reports/designer/234-concept-designer-role.md`
  - keeper for concept designer as a real future role and entry
    point for new concepts.
- `reports/designer/pi-api-surface-notes.md`
  - keeper for Persona-pi: Pi is Mario Zechner's `pi-mono`, with a
    flat TypeScript extension API that Persona-pi must adapt into
    typed noun-method records.
- `reports/operator/108` through `/135`
  - older operator history. Live residue is already summarized by
    `reports/second-operator/167`, `/168`, `/169`, and current
    designer audits. The active residue is: persona-mind prototype
    context, Kameo lifecycle correctness, early engine-manager /
    sandbox witnesses, terminal/owner-signal experiments, and
    sema-engine split history.
- `reports/cluster-operator/2-current-state-after-designer-operator-report-absorption-2026-05-22.md`
  - peer operator synthesis in the working copy; it agrees that
    Spirit cutover, sema-upgrade bootstrap, schema hash adoption,
    Orchestrate executor migration, engine-manager Axis 2, Forge,
    and Persona-pi are the active decision surfaces.

No change to second-operator's immediate code posture: Orchestrate
executor migration is still the lane's implementable next slice, but
it should stay narrow and not try to settle Spirit cutover,
sema-upgrade bootstrap, Forge, or Persona-pi.

Additional questions now worth carrying:

1. Does `third-designer`'s new structural lane change any operator
   routing, or should second-operator treat it as another window of
   the same Designer agent and simply keep reading its reports?
2. Should `concept-designer` now get a real lane registration through
   Persona Orchestrate once the lane registry becomes canonical, or
   stay as a design report until the role is fleshed out?
3. Should Criome's owner-session encryption and `owner-signal-criome`
   become a near-term implementation target, or remain behind Spirit
   cutover / sema-upgrade / Orchestrate?
4. For old operator reports, do we want a cleanup pass to retire
   `reports/operator/108` through `/135` into newer successor reports,
   or leave them as historical keepers until the main operator lane
   runs its own context maintenance?

## Latest Delta Absorption

Freshly absorbed after the second absorption commit:

- `reports/designer/281-headless-pi-research.md`
  - Pi has two documented headless modes: RPC over JSONL
    stdin/stdout and Node SDK via `createAgentSession`. Package
    identity is corrected to `@earendil-works/pi-coding-agent`.
    DeepSeek is already supported through `@earendil-works/pi-ai`.
    The open design question is whether the workspace wrapper should
    be a Rust RPC crate, a Node library, or a triad-backed service.
- `reports/cluster-operator/1-bird-zeus-local-update-authority-design.md`
  - Bird-on-Zeus update authority should be an explicit Horizon
    `SystemUpdateGrant`, not `trust = Max`, root SSH, `wheel`,
    `nixdev`, or arbitrary `lojix-cli` sudo. First implementation is
    Horizon grant, CriomOS local update helper, and `lojix-cli`
    local activation path.
- `reports/cluster-operator/3-third-designer-17-blocker-audit-2026-05-22.md`
  - Updates current blockers. `tools/orchestrate status` was fixed
    locally by making the helper accept dynamic lanes. The Spirit
    branch/tag blocker is stale; the real blocker is v0.1.0 write
    drift after v0.1.1 staging. Engine-manager Axis 2 remains open.
    `ItemPriority` already collapsed to `signal_sema::Magnitude`;
    health/readiness still need a decision.

Current corrections from this delta:

- Do not treat `tools/orchestrate status` as the active blocker
  anymore. It is a transitional helper and still not the destination,
  but the immediate closed-enum breakage is fixed in the cluster-
  operator commit.
- Spirit cutover should be framed as: v0.1.1 is staged but stale;
  v0.1.0 has later records. The work is restage/replay tail writes,
  then dual-write or flip default.
- Persona-pi / DeepSeek work is now better grounded, but it remains a
  design/proposal target, not this lane's immediate implementation.
- Bird-on-Zeus local update authority is a cluster/system lane item,
  not second-operator's Orchestrate slice.

Questions added by this delta:

1. For Bird on Zeus, is the first allowed action set `BootOnce` +
   `Test`, or should `Switch` be included from the start?

## Delta Absorption After Designer 282 / 283 And Third-Designer 18

Freshly absorbed:

- `reports/designer/282-workspace-implementation-status.md`
  - roughly 30-35% of the named architecture exists as working code.
    Production has Spirit, repository-ledger, and the pre-Persona
    deploy stack; the Persona engine is not production. `/249` still
    has 24 of 35 gaps open.
- `reports/designer/283-session-summary-2026-05-22-prime.md`
  - prime designer's next focus is `/249` gap closure. The DeepSeek
    direction moved out of persona-pi and into a new
    `persona-llm-client` library direction. `signal-sema` needs the
    Magnitude `Unknown` widening and Health/Readiness collapse follow-up.
- `reports/third-designer/18-audit-synthesis-2026-05-22.md`
  - corrects the live blockers: Spirit branch/tag blockage is stale,
    the real blocker is v0.1.0 write drift after v0.1.1 staging.
    `tools/orchestrate status` is fixed locally, but the durable
    destination remains typed persona-orchestrate.

Current corrections:

- Treat Spirit cutover as a v0.1.0 write-drift problem after staging,
  not a missing branch merge.
- Treat `tools/orchestrate status` as fixed locally; it is still only
  a transitional helper.
- Treat `/249` gap closure as designer's primary focus, not
  second-operator's implementation lane.
- Treat Orchestrate executor migration as independent enough to
  proceed, but ranked behind the live Spirit cutover wrapper.
- Treat `persona-llm-client` as the new DeepSeek direction. Persona-pi
  remains a separate harness-runtime component.

Questions to carry:

1. `EffectEmitted` payload: component-local typed `Effect` or
   universal `SemaObservation`?
2. Orchestrate executor migration timing: after the Spirit wrapper or
   in parallel?
3. `persona-llm-client`: library only or full triad?
4. Spirit v0.1.1 asymmetry: `persona-spirit` and
   `signal-persona-spirit` are v0.1.1 while
   `owner-signal-persona-spirit` remains v0.1.0; intentional?

## Cleared Questions From Latest Psyche Clarification

Cluster-operator is an operator role with a specialized cluster topic:
cluster reports, cluster questions, cluster deployments, and cluster
implementations. Ordinal prefixes copy whatever follows them, so a
future `second-cluster-operator` would be another window of the
cluster-operator role. Spirit record 174 captures this clarification.

For headless Pi, a Rust RPC wrapper is now the preferred baseline
workspace surface even if later work also adds a Node SDK wrapper or a
proper triad service. Spirit record 175 captures this decision. The
remaining open point is conceptual rather than directional: explain
what the Pi RPC process actually looks like and whether it should be
short-lived per request or held open as a reusable session.

## Refresh After Spirit 176-193, Cluster-Operator 4, And Designer 284

Freshly absorbed:

- Spirit records 176-193.
- `reports/cluster-operator/4-update-authority-and-lojix-daemon-current-state-2026-05-22.md`.
- `reports/designer/284-per-type-migration-trait-specification.md`.

Action taken in this lane:

- Cleared the stale Bird-on-Zeus branch question. The current update
  source is LiGoldragon `main`, not a Bird/Aether branch. Cluster-
  operator owns the implementation path.
- Reframed the Spirit cutover question. The active design is no longer
  generic dual-write vs flip vs replay; the new vocabulary is `main`
  and `next`, with the CLI routing to `next`, `next` coordinating back
  to `main`, and `main` recording divergence or recovering what it can.
- Kept Orchestrate executor migration as this lane's implementation
  target. The migration-trait specification is foundation work; it
  affects every daemon later, but it does not block local
  signal-executor routing inside persona-orchestrate.
- Did not edit `skills/role-lanes.md`. Spirit record 174 should be
  manifested there as specialized-role discipline, but the file is
  already dirty from another lane. Committing it from here would mix
  ownership.

Current migration-shape implications:

- The canonical version-pair vocabulary is `main` / `next`.
- Component development is moving toward standard `main` and `next`
  branches.
- The proposed migration foundation is a new `migration` crate plus a
  `signal-version-coordination` contract.
- `PeerCheck` is proposed on each component working contract; universal
  coordination back to `main` is proposed through
  `signal-version-coordination`.
- persona-introspect is proposed as the cross-version failure-log home.
- Historical signal versions are proposed as frozen sibling repos such
  as `signal-persona-spirit-v0-1-0`.

Still-relevant questions after this refresh:

1. `EffectEmitted` event payload: component-local typed `Effect`, or
   universal `SemaObservation`? This still blocks observable blocks on
   the unmigrated persona contracts.
2. Orchestrate executor migration timing: should second-operator keep
   going in parallel, or pause until the Spirit `main`/`next` cutover
   path is implemented?
3. In Orchestrate, do `Watch`/`Unwatch` survive as domain streams for
   role/lane/claim/activity facts, or should generic observation be
   only `Tap`/`Untap`?
4. What are the first high-level Mind-to-Orchestrate owner verbs for
   channel choreography before Orchestrate calls Router's
   `Grant`/`Extend`/`Revoke`/`Deny`?
5. What is the durable split between role definition, lane/window,
   agent run, job, and policy records in persona-orchestrate?
6. Is the Spirit release asymmetry intentional:
   `persona-spirit` + `signal-persona-spirit` at v0.1.1 while
   `owner-signal-persona-spirit` stays v0.1.0?
7. Is `persona-llm-client` a library only, or does it become a full
   triad with daemon, working signal, and policy signal?
8. For headless Pi RPC, should the Rust wrapper keep one Pi process
   alive per role/lane session, per task, or per call?
9. For headless Pi state, should Pi's own session persistence be used,
   or should the Rust wrapper own persistence and treat Pi as stateless?
10. For headless Pi tools, which built-ins are initially allowed:
   read-only tools, shell, edit/write, or policy-configurable tools?
11. For Bird-on-Zeus, is the first helper surface exactly
    `(LocalUpdate HomeProfile)` and `(LocalUpdate FullSwitch)`, or
    should engineering actions like `Test` and `BootOnce` be exposed
    immediately?
12. For the Bird-on-Zeus root boundary, should the helper be Rust from
    the first real slice, or is a zero-dynamic-field shell wrapper
    acceptable as a temporary experiment?
13. For designer 284's migration spec, do the open leans stand:
    crate name `migration`, frozen sibling historical repos,
    separate `signal-version-coordination`, no owner coordination
    contract yet, PeerCheck on working contracts, compile-time
    `MigrationIndex`?

## Refresh After Spirit 194-210 And Version-Handover Reports

Freshly absorbed:

- Spirit records 194-210.
- `reports/third-designer/19-refresh-after-prime-session-2026-05-22.md`.
- `reports/cluster-operator/5-refresh-after-new-intents-and-reports-2026-05-22.md`.
- `reports/designer/285-versionprojection-trait-and-handover-protocol-specification.md`.
- `reports/operator/157-version-projection-refresh-and-question-rollover-2026-05-22.md`.
- `reports/second-designer/151-design-mind-and-orchestrate-replacement-readiness.md`.
- `reports/operator/158-version-handover-foundation-implementation-2026-05-22.md`.

Action taken in this lane:

- Marked `/284` as superseded by `/285` wherever they differ. The
  implementation target is now `version-projection` plus
  `signal-version-handover`, not `migration`,
  `signal-version-coordination`, or per-component `PeerCheck`.
- Marked old Spirit Path A stop/freeze/migrate/start wording as
  superseded by smart socket handover. Record 203 supersedes record
  198.
- Marked sema-upgrade bootstrap as settled: sema-upgrade dogfoods the
  version-projection mechanism from day one, with no separate
  handwritten bootstrap phase.
- Marked Engine-manager Axis 2 timing as settled: land now as step 0
  of the `/257` / `primary-u8vo` contract migration sweep.
- Marked Orchestrate executor migration as clear next work in this
  lane. `reports/second-designer/151` says Orchestrate can canary
  before full sema-upgrade because claim/activity state is tolerable
  to rebuild; Mind cannot.
- Verified the Orchestrate service bead already exists:
  `primary-2chb` ("Deploy persona-orchestrate as workspace user
  service"). No duplicate bead filed.

Foundation now landed elsewhere:

- `/git/github.com/LiGoldragon/version-projection` landed on main.
- `/git/github.com/LiGoldragon/signal-version-handover` landed on main.
- `/git/github.com/LiGoldragon/sema-engine` now has durable
  `CommitSequence`.
- `/git/github.com/LiGoldragon/sema-upgrade` has a handover prototype.

Current implementation reading:

- Persona engine now precedes Spirit cutover. Record 209 makes
  `primary-2y5` (persona engine) blocking for `primary-x3ci` (Spirit
  v0.1.1 cutover).
- Component upgrade orders go through the target component's owner
  socket. For Spirit that means an owner operation on
  `owner-signal-persona-spirit`, then the private
  `signal-version-handover` upgrade socket runs the daemon-to-daemon
  protocol.
- Orchestrate remains the best second-operator slice: finish
  `primary-c620` executor migration, then `primary-2chb` can deploy it
  as a workspace service, then the bash helper can be cut over.
- Mind replaces beads later than Orchestrate because bead history is
  durable. Mind needs contract migration plus sema-upgrade coverage
  before deployment.

Still-relevant questions after this refresh:

1. `EffectEmitted` event payload: component-local typed `Effect`,
   universal `SemaObservation`, or two streams?
2. Orchestrate cutover vocabulary: keep current
   `Claim`/`Release`/`Handoff` for the shell-helper replacement, then
   layer abstract-job and agent registry later?
3. In Orchestrate, do `Watch`/`Unwatch` survive as domain streams for
   role/lane/claim/activity facts, or should generic observation be
   only `Tap`/`Untap`?
4. What is the durable split between role definition, lane/window,
   agent run, job, and policy records in persona-orchestrate?
5. What exact owner operation triggers component upgrade on
   `owner-signal-persona-spirit` and later other owner contracts?
6. What is the minimal persona-engine scope needed to unblock Spirit
   cutover now that engine orchestrates upgrades from day one?
7. Is the Spirit release asymmetry intentional:
   `persona-spirit` + `signal-persona-spirit` at v0.1.1 while
   `owner-signal-persona-spirit` stays v0.1.0?
8. For version handover, should historical signal contracts be frozen
   sibling repos such as `signal-persona-spirit-v0-1-0`, as `/285`
   recommends?
9. For version handover, should `owner-signal-version-handover` stay
   deferred until sema-upgrade owner policy exists, or be created now
   for force-flip / rollback / quarantine?
10. For version handover, should mirror payloads remain raw bytes plus
    `RecordKind`, or become typed enums?
11. For version handover, should per-operation policy stay as runtime
    crate literals for now, or move into contract/schema annotations?
12. For Mind replacing beads, should cutover use a thin `bd`-style
    wrapper that emits NOTA frames, or require agents to call
    `mind '(...)'` directly?
13. For bead corpus migration into Mind, should agents hand-relog or
    should a one-shot dumb import tool be built?
14. Is `persona-llm-client` a library only, or does it become a full
    triad with daemon, working signal, and policy signal?
15. For headless Pi RPC, should the Rust wrapper keep one Pi process
    alive per role/lane session, per task, or per call?
16. For headless Pi, should Pi own session persistence, or should the
    Rust wrapper own persistence and treat Pi as stateless?
17. For headless Pi, which built-ins are initially allowed: read-only
    tools, shell, edit/write, or policy-configurable tools?
18. For Bird-on-Zeus, is the first helper surface exactly
    `(LocalUpdate HomeProfile)` and `(LocalUpdate FullSwitch)`, or
    should `Test` and `BootOnce` be exposed immediately?
19. For the Bird-on-Zeus root helper, should it be Rust from the first
    real slice, or is a zero-dynamic-field shell wrapper acceptable
    temporarily?

## Cleared Question

Retired lane identifiers do not need tombstones right now. The current
active-table behavior is acceptable: retiring a lane removes it, active
lanes are not renamed, and the system does not reserve retired names
forever.

If later history preservation requires tombstones, that is a new design
problem attached to durable agent runs or report-lane history, not a
blocker for the current lane-registry slice.

## Open Decisions That Actually Matter

`Watch` and `Unwatch` need a decision during the Orchestrate migration.
Generic operation/effect introspection belongs to mandatory `Tap` and
`Untap`. `Watch` and `Unwatch` should survive only if they become a
domain stream for Orchestrate facts such as role, lane, claim, activity,
and agent-run changes.

The owner signal still needs a deliberate signal-tree pass before it
grows beyond role, lane, repository, and immediate administration
operations. The next expansion should not blindly add abstract-job or
policy-programming verbs to the existing root set.

The live role model is not fully split yet. The code has roles and
lanes. The design direction still wants separate role definition, agent
run, job, and policy records. Do not hide those types in strings.

## Workspace State

The relevant component worktrees checked during this pass were clean:

- `signal-frame`
- `signal-executor`
- `signal-persona-orchestrate`
- `owner-signal-persona-orchestrate`
- `persona-orchestrate`
- `persona-mind`
- `signal-persona-mind`
- `owner-signal-persona-mind`
- `owner-signal-persona-router`

The primary workspace had an unrelated `second-designer` report in the
working copy during this pass. This lane did not touch or commit it.

## Not Current Work

The old May 15-18 Persona engine reports are no longer the active desk.
The substance that still matters is summarized in:

- `reports/second-operator/167-review-persona-engine-backlog-2026-05-22.md`
- `reports/second-operator/168-review-mind-router-policy-2026-05-22.md`

Criome/Lojix authorization is real but not the current second-operator
pickup unless the user switches topics. Its current packet is:

- `reports/second-operator/169-review-criome-lojix-authorization-2026-05-22.md`
