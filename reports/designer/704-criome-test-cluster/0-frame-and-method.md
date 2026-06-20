# 704 — Reusable networked criome test cluster: frame and method

## The ask (psyche, 2026-06-20)

> we need a fully tested criome cluster, which means actually networked
> sandboxes, with spirit gate authentication. we should have a nice interface
> for testing networked things like this. do research/implementation of this.
> prometheus is a very powerful host which could easily host a vm cluster. look
> into it from the "easily re-usable" test cluster angle. let's fix this. take
> your time.

> we also have the cloud digital-ocean on-demand VMs - you can use that for
> testing the cluster too.

Six explicit requirements drive everything downstream: (1) *fully tested*
criome cluster, (2) *actually networked* sandboxes (not in-process mocks), (3)
*spirit gate authentication* exercised end-to-end, (4) a *nice, easily-reusable
interface* for testing networked things, (5) *prometheus* as a VM-cluster host,
(6) *DigitalOcean on-demand VMs* as a second substrate.

## Spirit gate outcome — Record (pending, blocked on outage)

The prompt carries durable testing intent beyond this one task: the criome
cluster's validation path *requires* actually-networked multi-node sandboxes
with the spirit gate authenticated, reached through one reusable test-cluster
interface that can target local/prometheus VMs and DigitalOcean on-demand VMs.
That still guides after this task is erased → it is a `Decision`
(testing-discipline domain), not task state.

**It cannot be captured yet: the production Spirit daemon is down** (see below).
The capture is parked here so it is not lost (no harness-dependent memory). On
Spirit recovery, record under domain `(Technology (Software (Quality Testing)))`
with referents `[criome spirit prometheus cloud]`, certainty `High`
(firm, repeated, "let's fix this"), testimony quoting both messages verbatim.
A second weaker arrow ("you can use that for testing too" re DO) is `Medium` and
folds into the same record as a substrate clause, not a sibling.

## Discovered blocker — production Spirit is down (system-maintainer)

`spirit-daemon.service` on ouranos is `failed` (start-limit-hit). Root cause from
the journal: the generation activated at 03:14 today runs a
`spirit-migrate-store` whose `production_migration.rs` rejects the live store
with `unrecognized spirit store schema version: 10`. The previous (newer) daemon
ran fine until 03:14 and had already written the store at schema v10.

This is a **rollback-in-effect**, not data loss — the `.sema` store files in
`~/.local/state/spirit/` are intact. spirit `main` HEAD (`9ac01ae`) contains
commit `f1bc797 "recognize live v10 store family migration"`; the deployed
generation predates it. **Fix: rebuild/redeploy spirit (+ its home-manager
service) from current main, which recognizes the v10 store.** This is a
system-maintainer/system-operator deploy touching the live intent store, so the
designer lane surfaces it and hands it off rather than executing it.

Consequence: intent capture is blocked workspace-wide until Spirit is back.

## Not greenfield — existing infrastructure inventory (pre-survey scout)

| Asset | Path | Relevance |
|---|---|---|
| `CriomOS-test-cluster` | `/git/.../CriomOS-test-cluster` | microvm-based cluster test flake — candidate reusable harness |
| vm-testing-prometheus-policy | `CriomOS/checks/vm-testing-prometheus-policy/` | prometheus already designated VM-test host |
| test-substrate module | `CriomOS/modules/nixos/test-substrate.nix` | NixOS test substrate |
| `cloud` + `digitalocean.rs` | `/git/.../cloud/src/digitalocean.rs`, `tests/digitalocean_live.rs` | DO on-demand VM provisioning (the psyche's second substrate) |
| `cloud` triad | `signal-cloud`, `meta-signal-cloud` | cloud component contract |
| `horizon-rs` | `/git/.../horizon-rs` | node/machine/cluster lib using nixosTest — candidate interface backbone |
| `lojix` / `lojix-cli` | `/git/.../lojix*` | Nix substituter + host key material — multi-node deploy trust |
| spirit 1-of-1 gate | spirit main `90875f2` `src/criome_gate.rs` | the gate the cluster must exercise |

The task is therefore **map → find the gap to fully-tested-networked → design the
reusable interface → implement/brief**, not build from zero.

## Method — Workflow `criome-test-cluster-research` (`wf_fbc72a4d-ab4`)

Three phases:
- **Survey** — 6 parallel deep readers: (1) criome propagation + spirit gate,
  (2) CriomOS-test-cluster, (3) prometheus VM-host infra, (4) cloud/DigitalOcean,
  (5) horizon-rs + lojix, (6) testing discipline + interface design space. Each
  returns a structured dossier (current state, findings with file:line, gaps,
  reusable-interface notes).
- **Design** — one synthesis agent: inventory, the reusable interface, the
  three-substrate strategy (nixosTest / microvm / DO), the end-to-end spirit-gate
  test, the lane-owned implementation plan, open questions.
- **Critique** — completeness critic scoring the design against the six explicit
  requirements, adversarially listing missing/weak items.

Synthesis lands in the highest-numbered file here; the design + critique are
finalized by the designer into the psyche-facing report and lane briefs. Host
provisioning (prometheus VM host, DO droplets) and the spirit redeploy are
system-operator/system-maintainer; code lands via operator on code-repo main;
designer prototypes the harness on a branch.

## Execution status (live)

- **Spirit outage RESOLVED.** Root cause was narrower than first stated: not a
  bad rebuild but a **stale-systemd-symlink drift** — home-manager generation
  801 (current, Jun 19 23:21) already pins the good spirit (daemon
  `w09z999am`, startup-state `gxa9f8i9` which recognizes the v10 store), but the
  live `~/.config/systemd/user/spirit-daemon.service` had drifted to a broken
  standalone unit (`mj2w349b` startup-state) from a partial/rolled-back 03:14
  activation. Fix: **re-activated generation 801** (`$gen/activate`), which
  rewrote the systemd units to the good spirit; `daemon` started clean,
  `(Current (1322 0))`, `spirit Version → (VersionReported 0.14.0)`,
  `Marker → (1416 …)`. No rebuild, no lock change, live store never at risk
  (backed up to `~/.local/state/spirit/spirit.sema.pre-redeploy-backup`
  regardless). The psyche authorized me (designer) to do this directly.
- **Intent captured — Spirit `cpip`** (Decision, Medium certainty, domains
  testing+deployment, referents `[criome spirit prometheus cloud]`). First
  submission was `Overstated` (claimed High; the prompt's HOW carries
  exploratory wording — "could easily host", "look into it", "take your time"),
  downgraded to the honest Medium. `7let`/`77ic` were **not** edited — they
  already reconcile each other (77ic permits the KVM-host capability touch while
  keeping everything else untouched); the psyche's "hermetic-only default"
  choice affirms 7let as the test-cluster default and leaves 77ic as the opt-in
  durable tier, folded into `cpip`.
- **Psyche decisions (AskUserQuestion):** redeploy spirit now (done);
  hermetic-only default (7let); start Phase 1 hermetic now.
- **Phase 1 underway** on branch `criome-cluster-test` (jj workspace
  `~/wt/github.com/LiGoldragon/CriomOS-test-cluster/criome-cluster-test`,
  off main `twunuxus`). Done: **added** flake inputs `spirit` (gate, main),
  `criome` (6c75804), `signal-criome` (9194c79) — kept `persona-spirit` for the
  upgrade test; `nix flake lock` resolved clean. Next: `mkCriomeClusterTest.nix`
  generator + criome/spirit NixOS service modules + the Stage A 1-of-1
  cross-kernel test + `fieldlab.nota` member nodes.
