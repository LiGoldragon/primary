# 558 — persona engine migration to the new architecture: frame & method

designer, 2026-06-08. Meta-report on migrating **every persona engine
component** to the new architecture, in every way. The psyche's request:
a deep audit/exploration/research → meta-report covering the full migration,
across all axes, for all components.

## What the persona engine is

Per `persona/INTENT.md` and `protocols/active-repositories.md`: the persona
engine is the privileged engine-**manager** daemon `persona` plus the
supervised component daemons it manages. Each component is a triad — the daemon
plus its two contracts (`signal-<c>` ordinary working signal + `meta-signal-<c>`
meta policy signal, per Spirit `n0ss`).

The twelve components audited:

| Component | Daemon | Contracts present |
|---|---|---|
| `persona` | engine-manager (persona-daemon + persona CLI) | signal-persona, meta-signal-persona (+ signal-engine-management to fold in) |
| `mind` | central state component | signal-mind, meta-signal-mind |
| `router` | message routing/delivery | signal-router, meta-signal-router |
| `message` | engine message ingress | signal-message — **meta missing** |
| `introspect` | inspection plane | signal-introspect — **meta missing** |
| `harness` | process/session control | signal-harness — **meta missing** |
| `system` | system observation | signal-system — **meta missing** |
| `orchestrate` | orchestration runtime | signal-orchestrate, meta-signal-orchestrate |
| `terminal` | terminal owner | signal-terminal, meta-signal-terminal |
| `spirit` | schema-derived pilot (`spirit`) + production source (`persona-spirit`) | signal-spirit, meta-signal-spirit |
| `upgrade` | upgrade/version-handover runtime | signal-upgrade, meta-signal-upgrade |
| `repository-ledger` | ledger component | signal-repository-ledger, meta-signal-repository-ledger |

Four components already show a contract-shape gap (`message`, `introspect`,
`harness`, `system` lack their `meta-signal-<c>` contract — an `n0ss`
violation).

## The rubric — nine axes of "the new architecture, in every way"

1. **daemon-shell-actor** — schema-rust-next-emitted triad daemon shell on
   triad-runtime's actor substrate (not the old blocking `MultiListenerDaemon` /
   `BoundedWorkers`, not a hand-written loop).
2. **execution-nexus** — execution through the generated nexus runner
   (`NexusWork → NexusAction`), `signal-executor` removed (`555`).
3. **contracts-schema-next** — `signal-<c>`/`meta-signal-<c>` schema-next-derived,
   no `signal_channel!` (`557`).
4. **contract-shape-two** — exactly two contracts; meta present; no third (`n0ss`).
5. **naming-bare** — bare component names, no `persona-*` drift (`k1i1`).
6. **storage-sema** — `sema-engine`/redb single-writer; SEMA route types
   schema-emitted; no direct `signal-sema` projection only to feed the old
   executor (`555`).
7. **kameo-discipline** — real state actor; hazards avoided (RestartPolicy,
   no leaked spawn, redb off the async handler, ask-not-tell) (`556`).
8. **nota-binary-boundary** — daemon takes one binary rkyv config, no flags,
   never parses NOTA.
9. **intent-arch-docs** — per-repo `INTENT.md`/`ARCHITECTURE.md` true and current.

## Method

A fan-out (13 survey agents + synthesis): one deep-dive per component reading the
actual daemon and contract code against all nine axes with file:line evidence;
one foundation/blockers pass on the shared substrate (triad-runtime nexus runner,
schema-rust-next emitter completeness, `spirit` as the end-to-end exemplar); then
a synthesis producing the readiness matrix, dependency-ordered sequencing, and
the migration plan. Grounded in the session's prior reports (`553` target, `555`
signal-executor, `556` terminal audit, `557` contracts) and Spirit `n0ss`/`k1i1`/
`r310`/`wpvz`.

## File map

- `0-frame-and-method.md` — this file.
- `1-foundation-and-blockers.md` — the shared substrate that gates everything.
- `2`…`13` — one report per component.
- highest-numbered file — the synthesis: readiness matrix, sequencing, first moves.
