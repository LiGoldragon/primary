# persona-orchestrate context sweep

## What moved

- Recorded fresh intent: `persona-orchestrate` should move forward now
  so the workspace can leave the old shell-script orchestration helper.
- Created `/git/github.com/LiGoldragon/persona-orchestrate/INTENT.md`
  from `intent/persona.nota` and `intent/component-shape.nota`.
- Rewrote `/git/github.com/LiGoldragon/persona-orchestrate/ARCHITECTURE.md`
  to carry the current implementation slice and the full triad
  destination in one permanent doc.
- Added missing workspace index symlinks:
  `/home/li/primary/repos/persona-orchestrate` and
  `/home/li/primary/repos/signal-persona-orchestrate`.

## Report sweep

The operator-assistant lane has one load-bearing persona-orchestrate
report:

- `/home/li/primary/reports/operator-assistant/154-primary-hrhz-architecture-audit-2026-05-18.md`

Its useful findings are now represented in the repo architecture:
triad incomplete, owner-signal absent, lane registry not implemented,
subscribe variants missing, lock-file projection inverted, exact-scope
handoff required, and activity slot exposure needed.

The newer canonical design layer is:

- `/home/li/primary/reports/designer/233-persona-orchestrate-operator-handoff.md`

That report absorbs the prior designer reports and answers the
operator-assistant audit questions. I treated it as current design
truth while migrating permanent shape into the repo docs.

The rest of `reports/operator-assistant/` is older implementation
work or unrelated component audits. No other operator-assistant report
had current persona-orchestrate substance to migrate.

## What is clear enough to implement

- Build the real `persona-orchestrate` triad: long-lived daemon, thin
  CLI, ordinary socket, owner socket, sema-engine state, and
  component-triad witness tests.
- Add ordinary `Subscribe` families for activity, claims, and lane
  registry.
- Add activity slot to queried `Activity` records.
- Add exact-scope handoff rejection.
- Create `owner-signal-persona-orchestrate`.
- Add the `lane_registry` policy table and bootstrap it from the
  current lane seed on first start.
- Make lock files a daemon projection, not the source of truth.

## Clarification Needed

Only one item looks like real psyche intent is still missing:

**What exact identity shape should `LaneIdentifier` use?**

The intent is clear that lane registry is data, not enum variants.
The architecture still needs the identifier shape. The viable choices
are a human-readable string newtype, a content hash, or a sema-engine
slot minted by the registry. My lean is the sema-engine slot because
the registry is the infrastructure that mints lane identity, while the
CLI can render slots as human names.
