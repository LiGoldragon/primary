# Audit of workspace activity on 2026-06-20

System-operator audit, run on 2026-06-20 at about 20:33-20:40 EEST.

## Scope and evidence

I treated "today" as 2026-06-20 in the active workspace timezone. Evidence
checked:

- `tools/orchestrate status` for live claims and open beads.
- `jj log` and `jj status` across `/home/li/primary`, active `/git/...`
  repositories, and `~/wt/...` worktrees.
- Reports modified today under `reports/`.
- Live services: `lojix-daemon.service`, `spirit-daemon.service`, failed
  system/user units, and lingering component processes.
- Local deploy run records under `~/.local/state/lojix-runs`.

This is a state and integration audit, not a full line-by-line code review of
every diff produced today.

## Executive findings

| Severity | Finding | Current state |
|---|---|---|
| Critical | `lojix-run` is stale again in the active user profile. | `/home/li/.nix-profile/bin/lojix-run` resolves to `lojix-run-0.1.0` and embeds `lojix-cli-0.1.0`. Earlier `CriomOS-home` main fixed this with `3729ca21`, but a later activation of `criomos-home-spirit-bypass` at 16:28 EEST reverted the active profile to a branch based before that fix. |
| High | A test `spirit-daemon` is still running outside systemd supervision. | PID `698978`, cwd `reports/system-maintainer/705-spirit-audit/raw`, sockets under `/tmp/spirit-sb2/`. It appears isolated from production sockets, but it is unmanaged session residue. |
| High | Primary has uncommitted report work. | `reports/pi-operator/12-cloud-node-operator-side.md` is added but not committed. It documents horizon-rs main integration and a goldragon lock blocker. |
| High | The Spirit audit plan is not executed, but the bypass is deployed. | Spirit is now live at `0.15.0`, but the 1323-to-591 record trim remains pending. Report text that said production was untouched is stale after the later activation. |
| Medium | One failed user transient scope remains from an OOM. | `app-ghostty-surface-transient-7999.scope` failed at 16:41 EEST after 19.2G memory and 20.8G swap peak. System units have zero failures. |
| Medium | Several feature worktrees hold dirty state. | Notably `CriomOS-test-cluster`, `mentci-lib`, `mentci-egui`, `signal-mentci`, `signal-criome`, structural-form Spirit/schema worktrees, and VM-host branches. Many correspond to active locks, but they are live risk if the owning lane disappears. |

## Live system state

`lojix-daemon` is healthy and running `lojix-0.3.10`:

- service active since 14:55:18 EEST;
- daemon binary path contains `lojix-0.3.10`;
- successful deploy outputs at 15:23, 15:34, 16:20, 16:30, and 16:30 EEST.

The deploy history also shows real earlier failures:

- GitHub API 403 and rust stable hash mismatch near midnight;
- repeated SEMA layout mismatch restart loop around 04:12-04:14 EEST;
- 4-root vs 5-root datom/schema mismatch around 11:43 EEST;
- model `.drv` missing failures at 12:38 and 12:53 EEST;
- invalid target-store `.drv` at 14:30 EEST.

Those failures align with the system-designer self-audit and were later
resolved enough for successful deploys.

`spirit-daemon.service` is healthy and now reports `0.15.0`:

- active since 17:35:04 EEST;
- startup reported `(Current (1333 0))`;
- `spirit Version` returns `(VersionReported 0.15.0)`.

Production Spirit is not still at the 0.14.0 state described in the middle of
the system-maintainer handoff. The handoff became stale after the later
`criomos-home-spirit-bypass Activate`.

## Critical regression: `lojix-run`

The system-operator fix landed correctly on `CriomOS-home` main:

- `0392a3a1` changed the package input from `lojix-cli` to current `lojix`.
- `3729ca21` routed deploy requests through `meta-lojix` and translated the old
  flat `HomeOnly` shape to meta-signal `Deploy (Home ...)`.

That fix was verified and activated once at 16:20 EEST via:

`HomeOnly goldragon ouranos li ... github:LiGoldragon/CriomOS-home/main Activate`

However, two later runs used the `criomos-home-spirit-bypass` branch:

- 16:27 EEST `Build`
- 16:28 EEST `Activate`

That branch is based on `c3be1e96`/`51a19beb`, before the `lojix-run` fix. The
current active profile therefore reverted:

- profile current link: `profile-1893-link`, updated 16:30 EEST;
- active `lojix-run`: `lojix-run-0.1.0`;
- embedded default: `lojix-cli-0.1.0`.

So the earlier final state "active wrapper embeds `lojix-0.3.10/bin/meta-lojix`"
was true immediately after the main activation, but is false now. The fix needs
to be merged/cherry-picked onto the Spirit-bypass profile branch, or the active
profile needs to return to a branch that contains both Spirit 0.15.0 and the
`lojix-run` wrapper fix.

## System-designer deploy work

The system-designer lane did the largest production-impacting work:

- `lojix` advanced through `0.3.5` to `0.3.10`.
- `CriomOS` was repinned repeatedly to consume those releases.
- prometheus received the durable `vm-testing` TestVm node in built-but-not-
  booted form.
- deadlock-free self-Switch and build-on-target behavior were reportedly proven.
- the lane self-audited report overclaims and corrected reports 152/153.

The system-designer self-audit is unusually valuable: it caught a real false
claim about the `0.3.8` eval-store fix and traced a local-store inconsistency
from garbage collection. The later `0.3.10` commit fixed the build step's store
selection.

Remaining risks:

- the lane still holds broad locks on `CriomOS`, `goldragon`, `lojix`,
  `signal-lojix`, `meta-signal-lojix`, and `clavifaber`;
- `goldragon` is blocking cloud-node data integration;
- several VM-host worktrees are dirty.

## System-maintainer Spirit audit

The Spirit database audit produced a concrete trim plan:

- snapshot: 1323 active records;
- target: 591 active records;
- every survivor assigned kebab-case referents;
- trimmed records archived in raw artifacts;
- not executed against the live store.

The bypass code landed on `spirit` main:

- `e126e5a`: owner import auto-registers referents and enforces kebab-case for
  new referents;
- later `7fc267c`: import upserts existing IDs instead of insert-only;
- Spirit is now deployed as `0.15.0`.

Risks:

- the trim plan must be re-rendered before execution because the live store
  drifted;
- there is a lingering sandbox daemon under `/tmp/spirit-sb2`;
- durable intent from that session was intentionally deferred and should be
  revisited after the trim/deploy state settles.

## Cloud-node and website-hosting work

Cloud-designer and pi-operator moved the cloud-node arc:

- DigitalOcean custom image work was built and live-tested.
- `doris` was designed as a real low-trust cloud node.
- `horizon-rs` removed the dead `TypeIs` one-hot and derives `BehavesAs`
  directly from typed species.
- pi-operator merged the horizon branch to `horizon-rs` main as `bd1cc2c1`.

The goldragon branch is still not merged because `system-designer` holds the
`goldragon` lock for VM-host/TestVm work. The open beads reflect that:

- `primary-n98t`: land cloud-node feature branches;
- `primary-unig`: website-hosting service, blocked by `primary-n98t`.

## Criome and Mentci work

Criome work advanced in several layers:

- `criome` main landed the cluster witness, meta approval socket, authorization
  mode, client approval hardening, and witness binaries.
- designer branches advanced E1 cross-criome peer transport.
- `signal-criome` and `meta-signal-criome` gained authorization and parked
  approval surfaces.
- `CriomOS-test-cluster` built NixOS VM witnesses, but its canonical checkout is
  currently dirty with cluster and fixture updates.

Mentci work advanced but remains branch/prototype-heavy:

- `meta-signal-mentci`, `mentci`, and `mentci-egui` main received typed
  component socket endpoints earlier today.
- designer re-founded `mentci-lib` on live contracts in a feature branch.
- `signal-mentci` received additive public readers in a feature branch.
- `mentci-egui` has a proving branch consuming the shared model.

Operator report 445 correctly preserved two schema-rust-next worktrees before
any worktree cleanup. Direct merge of those schema branches is not recommended;
they are mining sources, not ready integration.

## Orchestrate work

The orchestrate state owner is the daemon triad in `/git/.../orchestrate`; the
primary `tools/orchestrate` surface is a compatibility adapter through
`orchestrate-cli`.

Today's system-operator report 231 corrected the release-safety direction:
release invariants cannot depend on `push-*` bookmark names. A semantic lane
release-state model is still open. Designer report 707 then prototyped a
worktree registry across `orchestrate`, `signal-orchestrate`, and
`meta-signal-orchestrate`, but it is not integrated and requires a live
`orchestrate.redb` schema migration.

Current locks are daemon-backed and healthy enough for status, but live
`Observe Lanes` was previously empty. Fixed-role lane population remains an
open integration question.

## Dirty and in-flight state

Current locks:

- `cloud-operator`: `CriomOS-test-cluster`
- `cloud-maintainer`: `cloud`
- `designer`: `mentci-lib/re-found-on-live-contracts`
- `system-designer`: `CriomOS`, `clavifaber`, `goldragon`, `lojix`,
  `meta-signal-lojix`, `signal-lojix`
- `system-maintainer`: `spirit`, `signal-spirit`

Dirty surfaces found:

- `/home/li/primary`: uncommitted `reports/pi-operator/12-cloud-node-operator-side.md`.
- `/git/.../CriomOS-test-cluster`: dirty AGENTS/INTENT, cluster files,
  horizon fixtures, and `flake.lock`.
- `schema-cc`: new prototype files under `next/schema-cc`.
- `CriomOS-home/spirit-bypass`: dirty `flake.lock`.
- VM-host worktrees for `CriomOS` and `goldragon`: dirty module/data changes.
- `mentci-lib`, `mentci-egui`, `signal-mentci`: dirty live-contract branch
  work.
- `signal-criome/signal-criome-peers`: dirty peer contract/generated work.
- structural-form worktrees for `spirit`, `signal-spirit`,
  `meta-signal-spirit`, and `schema-rust-next`: dirty migration work.

Some dirty state is expected under active locks. The risk is that there are
many simultaneous high-blast-radius branches; cleanup and preservation need to
stay explicit.

## Recommended next actions

1. Fix the active profile regression: put both Spirit 0.15.0 and the
   `lojix-run` `meta-lojix` wrapper fix on the same `CriomOS-home` line, then
   activate it.
2. Stop or explicitly adopt the `/tmp/spirit-sb2` sandbox daemon. If it is only
   audit residue, kill it and remove the temp directory after confirming no
   owner is using it.
3. Commit the uncommitted pi-operator report on primary, per the "commit the
   whole working copy" discipline, once the owning lane is not still editing it.
4. Have system-designer either land or narrow the `goldragon` lock so
   `primary-n98t` can complete the doris data integration.
5. Re-render the Spirit trim plan from the live 0.15.0 store before executing
   any import/nominations.
6. Preserve or push dirty feature-branch worktrees before any cleanup pass,
   especially `mentci-lib`, `signal-mentci`, `signal-criome`, and the
   structural-form schema worktrees.

## Bottom line

Today produced real progress: `lojix` is live at `0.3.10`, Spirit is live at
`0.15.0`, prometheus has the durable VM-test node, horizon's cloud-node type
model is cleaner, and the criome/mentci/orchestrate branches have concrete
prototypes.

The main problem is integration drift between lanes. The most concrete example
is the live `lojix-run` regression: one lane correctly fixed and deployed it,
then another lane activated an older Spirit-bypass `CriomOS-home` branch and
silently reverted the user-facing wrapper. The next repair should combine those
two lines before any more home activations.
