# Handover — Orchestrate daemon offline: fix + SEMA schema-drift root cause

## Focus
Bring the Orchestrate claim-coordination daemon back online, and investigate the
root cause of its failure — a recurring SEMA/redb schema-version mismatch — so
this class of failure stops recurring across components. Everything else from the
prior session is out of scope.

## Confirmed facts — the current failure
- The Orchestrate daemon is OFFLINE on primary. No orchestrate process is
  running; the Unix socket `/home/li/primary/orchestrate/orchestrate.sock` is a
  stale leftover with nothing bound to it; a read-only
  `orchestrate "(Observe Roles)"` returns `Connection refused (os error 111)`.
- Crash-loop cause, from `/home/li/primary/orchestrate/orchestrate-daemon.log`:
  fatal `sema engine: schema version mismatch — file was written with v2, this
  build expects v3`. Also present in the log: repeated `daemon frame error:
  frame IO error: early eof`, and `wire path must be absolute and normalized:
  criome-authorization-push` on the meta channel. The last log line is a restart
  by a "service-restore agent" at 2026-07-03T00:39:07+02:00, with nothing logged
  since — nothing is supervising it back up.
- The `orchestrate-daemon.service` systemd `--user` unit is built in the Nix
  store (e.g. `/nix/store/3bq91jxzd3an8n4jispcglci841g68d4-orchestrate-daemon.service`)
  but is NOT symlinked into `~/.config/systemd/user/`. Only `agent-daemon.service`
  and `spirit-daemon.service` are active user units. So on this host the daemon
  is neither running nor supervised.
- Stale socket files under `/home/li/primary/orchestrate/`:
  `orchestrate.sock`, `orchestrate-owner.sock`, `orchestrate-upgrade.sock`.

## Confirmed facts — the pattern to root-cause
The same redb/SEMA schema-version-mismatch has bitten three components in one
night:
1. Orchestrate — SEMA v2 on-disk file vs v3 build (this failure).
2. mirror.service (mirror-0.1.2) — crash-looped on a redb `store-heads` table
   `HeadFamily` type-signature mismatch (old on-disk ledger vs newer binary).
3. lojix ByNode "Current" ledger — came up empty (`GenerationUnknown`) after an
   in-place 0.3.10 → 0.4.1 daemon upgrade on ouranos (tracked as bead
   `primary-3xwk`).

Suspicion (not yet confirmed as the true root cause): SEMA/redb-backed components
have no migration or reset-on-mismatch path, so any schema or binary version bump
can wedge the component on on-disk state a newer binary refuses to open.

## Open questions / live uncertainties
- Is the orchestrate on-disk SEMA state disposable? Claims are ephemeral runtime
  locks and are all void while the daemon is down, so a reset likely loses
  nothing that matters — but the SEMA file may hold more than claims (roles,
  subscriptions, the `criome-authorization-push` authorization state); confirm
  before wiping. A reset-over-migration approach was recommended but the psyche
  has not confirmed it.
- Why is the `--user` unit landed-in-repo but not activated on this host? Never
  home-deployed here, excluded from the current system generation, or a
  home-deploy gap? (The prior session left at least one home change land-only and
  undeployed — criomos-home bead `primary-7ile`; the unit activation may sit in
  similarly-undeployed home config.)
- What is `criome-authorization-push`, and why is an unnormalized/relative wire
  path reaching the meta channel — a distinct defect, or a symptom of the same
  schema drift?
- The durable fix shape (the root-cause deliverable) is undecided: per-component
  reset-on-mismatch, a SEMA-wide migration framework, or a build-time
  schema-version compatibility gate.
- Whether to weave the three instances (orchestrate, mirror, `primary-3xwk`)
  under one systemic epic.

## Artifact pointers
- `/home/li/primary/orchestrate/orchestrate-daemon.log` — crash-loop evidence
  (v2/v3 mismatch, frame IO errors, `criome-authorization-push`).
- `/home/li/primary/orchestrate/` — the stale sockets and the live socket path.
- Nix-store unit `…-orchestrate-daemon.service` — built, not symlinked into
  `~/.config/systemd/user/`.
- `agent-outputs/LojixDeployAuthMap/Scout-H945-NoPermissionDiagnosis.md` — mirror
  redb `HeadFamily` mismatch (sibling instance).
- `agent-outputs/LojixDeployAuthMap/Deploy-H945-LandingEvidence.md` — lojix
  ByNode empty-ledger nuance (sibling instance); bead `primary-3xwk`.
