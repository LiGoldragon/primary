# signal refresh 144 system impact

## Scope

This report incorporates:

- `reports/operator/144-signal-sema-executor-refresh-2026-05-20.md`
- `reports/designer/254-signal-executor-sema-refresh-audit.md`

It updates:

- `reports/system-specialist/152-signal-convergence-pilot-and-intent-gap-impact.md`

## Current conclusion

`reports/operator/144-signal-sema-executor-refresh-2026-05-20.md`
changes the system-specialist sequencing recommendation, not the lower
architecture.

The three-layer model is now landed in the lower slice:

```text
Contract Operation
Component Command
Sema Classification
```

Sema is payloadless classification and observation vocabulary. It is
not the executable database language. Components execute their own
typed commands, then project command/effect pairs into
`SemaObservation`.

The important correction to my previous report is pilot order:

```text
foundation convergence
-> persona-spirit pilot
-> repository-ledger later
-> downstream Persona and lojix migrations after the pattern is proven
```

`repository-ledger` was the cleaner technical proving ground, but
psyche intent now explicitly prioritizes `persona-spirit` because the
workspace wants to replace the flat-file intent log with a usable
spirit CLI. That supersedes the repository-ledger-first recommendation
in `reports/system-specialist/152-signal-convergence-pilot-and-intent-gap-impact.md`.

## What is now settled

The repo split still holds:

| Repo / layer | Role |
|---|---|
| `signal-frame` | frame envelope, reply shape, batch failure classification, observable macro surface |
| `signal-executor` | lowering orchestration, command plans, atomic batch execution shape, observer projection bridge |
| `signal-sema` | payloadless `SemaOperation`, `SemaOutcome`, `SemaObservation` |
| `signal-*` contracts | contract-local public operations, replies, filters, observable event vocabulary |
| daemons | policy, command vocabulary, execution, durable state, socket delivery |

The lower implementation has landed and passed checks per `/144`:

- `BatchErrorClassification` lives in `signal-frame`.
- `signal-executor` depends on that trait instead of hardcoding every
  engine failure as unknown/not-committed.
- `CommitStatus::Partial` is gone until a real partial-commit
  surface exists.
- Persona observable event pair is `OperationReceived` /
  `EffectEmitted`.
- Explicit no-change commands are valid commands; accepted operations
  do not disappear just because their outcome is `NoChange`.

## System-specialist consequences

Do not start `lojix` migration from the old report order. `lojix` is
deployment infrastructure; it should consume the proven shape after the
persona-spirit pilot proves the real daemon path. `signal-lojix` stays
Layer 1 public vocabulary. Deployment commands/effects stay in
`lojix-daemon` when that work resumes.

Do not duplicate the downstream stale-vocabulary cleanup. At the time
of this report, `operator-assistant` holds locks on:

- `/git/github.com/LiGoldragon/signal-persona-orchestrate`
- `/git/github.com/LiGoldragon/signal-persona-introspect`

That lane is already migrating the `SemaEffect` / `SemaEffectEmitted`
drift named in `/144`.

Keep current intent logging on the file substrate until the spirit
pilot ships a real daemon/CLI and the workspace cuts over. The future
target is spirit CLI, but the current system still depends on
`intent/*.nota` as the live substrate.

## Open questions

1. Does the first usable `persona-spirit` pilot need working `Tap` /
   `Untap` subscriptions before agents start using it for intent
   submission, or is it enough that accepted observer operations have
   explicit `NoChange` command witnesses until subscription delivery
   lands?

2. Is `EffectEmitted` mandatory for every generated Persona observable
   contract, or is it the default macro vocabulary that a contract can
   replace only when it has a stronger domain-specific event noun?

## Current posture

No system code changes from this report. The right action for this lane
is to stop treating `repository-ledger` as the next pilot prerequisite
for `lojix`, and to let operator lanes finish the lower cleanup plus
the persona-spirit pilot before system-specialist resumes the deploy
daemon migration.

