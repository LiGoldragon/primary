# Weave — primary-h945 ouranos Deploy-Unblock Execution Plan

Autonomous overnight run, WEAVE phase. This is the tracker graph + dispatch plan
the orchestrator uses to drive the h945 deploy-unblock to completion without the
psyche. The weave has been PERFORMED against the primary beads DB; this document
is the readable projection. Authoritative cause:
`agent-outputs/LojixDeployAuthMap/Scout-H945-NoPermissionDiagnosis.md`. Prior
tails: `agent-outputs/Handover-SpiritIntent-and-Deployment.md`.

## Locked decisions (do NOT re-litigate)

1. The h945 "NOPERMISSION" is a triple mislabel. Real cause: `mirror.service`
   (SEMA mirror daemon mirror-0.1.2) crash-loops on a redb `HeadFamily` table
   type-signature mismatch, so `switch-to-configuration switch` exits 4.
2. `mirror.service` is disabled ALTOGETHER in CriomOS on ALL hosts, minimally and
   REVERSIBLY (mirror module/flake wiring preserved). Do NOT modify the mirror
   repo. Do NOT build a reset-on-mismatch guard. Noted against the `primary-nbmq`
   mirror epic (live enablement deferred until mirror is real).
3. The live System Switch to ouranos is driven AUTONOMOUSLY by a deploy worker
   (psyche pre-authorized; will not run it). With `mirror.service` disabled the
   switch should exit 0. The deploy also lands host lojix `0.3.10 -> 0.4.x`
   (CriomOS main already pins lojix 0.4.1) and makes the guardian prompt
   reboot-persistent.
4. Reboot-persistence is verified STRUCTURALLY (the newly-activated generation
   pins the current guardian/home + spirit input). Do NOT reboot ouranos
   gratuitously.

## Bead graph

`primary-h945` was reframed as the umbrella EPIC (P1) for the remaining deploy
tail; the landed no-baked-test-defaults history stays in its description for
provenance. Two ordered children plus two standalone beads were added; the
existing `primary-dq1r` was wired in.

| Bead | Title (short) | Pri | Repo | Suggested role | Status |
|------|---------------|-----|------|----------------|--------|
| primary-h945 | EPIC umbrella: deploy-unblock ouranos System Switch | P1 | (epic) | (container) | OPEN 0/2 |
| primary-h945.1 | Disable mirror.service (all hosts, reversible) + confirm/bump guardian spirit-home pin | P1 | CriomOS | operating-system-implementer | OPEN, READY |
| primary-dq1r | CriomOS build-time round-trip flake check guarding daemon-config NOTA vs pinned lojix writer schema | P2 | CriomOS | operating-system-implementer / nix | OPEN, READY |
| primary-h945.2 | Deploy live System Switch to ouranos + verify | P1 | CriomOS (target ouranos) | operating-system-implementer / deploy | OPEN, BLOCKED |
| primary-7ile | criomos-home transitive lojix input bump 0.3.10 -> 0.4.1 | P3 | criomos-home | operating-system-implementer | OPEN, READY (parallel) |
| primary-usqs | Audit + closeout: verify in-repo + green + live-state; close h945 + dq1r | P1 | CriomOS + live ouranos | nix/rust auditor, then repository-closeout / tracker-weaver | OPEN, BLOCKED |

## Dependency ordering (the DAG)

```
primary-h945.1  ─┐
                 ├─blocks─> primary-h945.2 ─┐
primary-dq1r    ─┘                          ├─blocks─> primary-usqs
                                            │
primary-h945.1 ─────────────blocks──────────┤
primary-dq1r   ─────────────blocks──────────┘

primary-7ile : no blockers, no blocked; runs fully in parallel (does NOT gate
               h945/dq1r closure)
```

Edges actually written to the tracker:
- `primary-h945.1 blocks primary-h945.2`
- `primary-dq1r   blocks primary-h945.2`
- `primary-h945.1 blocks primary-usqs`
- `primary-h945.2 blocks primary-usqs`
- `primary-dq1r   blocks primary-usqs`

Verified via `bd ready --explain`: h945.1, dq1r, 7ile report "no blocking
dependencies"; h945.2 and usqs report BLOCKED. The epic-parent link does NOT
block the children.

## Dispatch waves (ready set)

### Wave 1 — dispatch NOW, in parallel

- WORKER A (operating-system-implementer, ONE CriomOS worktree/claim):
  `primary-h945.1` AND `primary-dq1r` together in a SINGLE CriomOS change. They
  touch the same repo; one worker on one claim avoids CriomOS worktree/claim
  contention. Land to CriomOS main (jj commit + push), green.
- WORKER B (operating-system-implementer, criomos-home): `primary-7ile`. Fully
  parallel, different repo. Land-only bump unless a home deploy is separately
  warranted (record the decision on the bead). Low priority; may slip without
  blocking the deploy.

### Wave 2 — after Wave-1 CriomOS change lands green

- WORKER C (operating-system-implementer / deploy): `primary-h945.2`. Drives the
  live System Switch to ouranos via `meta-lojix`. Must run in THIS primary
  environment (see precondition below).

### Wave 3 — after the deploy verifies

- WORKER D (nix/rust auditor, then repository-closeout or tracker-weaver):
  `primary-usqs`. Independent verify of all in-repo changes + green evidence +
  live-state reconciliation, then close `primary-h945` (with children) and
  `primary-dq1r` from evidence. Do NOT close if evidence is short.

## Per-bead acceptance evidence

### primary-h945.1 — disable mirror.service + guardian pin (CriomOS)
- `nix build` of the ouranos system closure is green with `mirror.service`
  disabled (unit absent / not enabled), mirror module + flake input still wired
  (reversible).
- CriomOS main's pinned spirit/home input carries guardian rev `7b0770642ab1`
  (spirit 0.21.0); if it pinned an OLDER spirit, the input was bumped here.
- Landed to CriomOS main; disabled-unit diff + spirit/home pin rev captured.

### primary-dq1r — round-trip flake check (CriomOS)
- A CriomOS flake check runs the pinned `lojix-write-configuration` binary
  against the module's emitted `startupRequest` NOTA (tempfile) and asserts it
  decodes; build FAILS on module-NOTA / pinned-writer-schema drift.
- Check present AND passing on CriomOS main; ideally in the same change as h945.1.

### primary-h945.2 — live System Switch to ouranos (deploy)
- `switch-to-configuration` exits 0 (no failed units).
- lojix on ouranos resolves to 0.4.x (not 0.3.10).
- `mirror.service` NOT running and NOT enabled.
- New system generation STRUCTURALLY pins the current guardian/home + spirit
  input (guardian rev `7b0770642ab1`) — by inspecting pinned inputs, no reboot.
- `lojix "(Query (ByNode (goldragon ouranos None)))"` shows a new `FullOs Switch
  Current` record whose store path == the newly-built toplevel.

### primary-7ile — criomos-home lojix bump (criomos-home)
- criomos-home flake.lock lojix input == `9f42435...` (0.4.1); nix eval resolves
  lojix 0.4.1; green; landed to criomos-home main. Home-deploy vs land-only
  decision recorded on the bead.

### primary-usqs — audit + closeout
- Independent auditor confirms: mirror.service disabled reversibly (wiring
  preserved), guardian spirit/home pin present, dq1r check present + passing,
  green build evidence, and live ouranos reconciliation (guardian persistent,
  lojix 0.4.x live, mirror gone). Then h945 (+ children) and dq1r closed with
  evidence recorded on the beads.

## Blocker / hiccup analysis

NO BIG HICCUP. Per locked decision 3 the psyche has PRE-AUTHORIZED the autonomous
deploy, so it is not a psyche-gated act. The mirror-disable route (locked
decision 2) deliberately avoids the one genuinely privileged, psyche-gated op the
scout flagged (clearing the root-owned `/var/lib/mirror` ledger) — with
`mirror.service` off, no host-state clearing is needed. Scout evidence shows the
existing lojix daemon path authenticated to `root@ouranos` (BatchMode key-based)
and ran the full switch as root on deploy id 25/38; only mirror.service failed.
So no interactive human credential and no operator-only host access are required.

### Watch items (NOT blockers — surface only if they materialize)

1. DEPLOY-ENV PRECONDITION (on primary-h945.2): the deploy worker must run in
   THIS primary environment, where `meta-lojix` reaches ouranos over the existing
   key-based `root@ouranos` SSH. If the worker is dispatched to an isolated
   environment lacking that access, the deploy STOPS and escalates — do not
   invent a workaround. (Access demonstrably exists here per prior attempts.)
2. GUARDIAN-PIN SCOPE CREEP (on primary-h945.1): if CriomOS main pins an OLDER
   spirit lacking the guardian and bumping the spirit/home input turns out
   non-trivial (transitive home/spirit rebuild), h945.1 grows but stays
   worker-landable. Flag if it balloons.
3. 0.3.10 -> 0.4.x SELF-UPGRADE (on primary-h945.2): the switch upgrades the
   lojix daemon in place; prior attempts show the 0.3.10 daemon drives the full
   switch, so this is expected to work — the deploy worker must still confirm the
   new 0.4.x daemon comes up active post-switch.

## Tracker verification (this weave)

- `bd show primary-h945` — epic, 2 children (h945.1, h945.2), 0/2 complete.
- `bd dep tree primary-h945.2` / `primary-usqs` — both BLOCKED with the expected
  blockers.
- `bd ready --explain` — h945.1, dq1r, 7ile READY ("no blocking dependencies");
  h945.2, usqs BLOCKED.
- Notes added: reframe note on h945; wiring note on dq1r; mirror-disable note on
  the primary-nbmq epic.
