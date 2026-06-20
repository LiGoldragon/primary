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
- **Stage A LANDED GREEN — `criome-cluster-1of1` passes in a real NixOS VM.**
  Cross-lane convergence (clean): **operator already landed the witness on
  criome `main`** (`1eaa783`, Jun 19) — the `cluster-witness` package with
  `criome-cluster-witness-test` + `criome-write-configuration`. My local jj
  `main` was stale (6c75804), so I unknowingly re-implemented it on a branch;
  on discovery I **deleted my duplicate `criome-cluster-witness` branch** and
  repointed at criome `main`. The division: **operator owns the witness on
  criome main; designer owns the nixosTest harness.**
  - Designer contribution — `CriomOS-test-cluster` branch `criome-cluster-test`
    (`3cfb16fa`): `lib/mkCriomeClusterTest.nix` (the reusable `{cluster,
    members}` generator) + the `criome-cluster-1of1` check, consuming criome
    `main`'s `cluster-witness` package. A minimal NixOS guest runs
    `criome-daemon` as a systemd service (`ExecStartPre` encodes the rkyv
    config — `mirror.nix` shape, `ExecStart` runs the daemon on one rkyv arg);
    the witness runs against the socket. **Standalone
    `nix build .#checks.x86_64-linux.criome-cluster-1of1` is green** — VM log:
    `PROOF (a) authorized head -> Authorized`, `PROOF (b) threshold-short ->
    Rejected(QuorumShort{required:1, satisfied:0})`, `test script finished in
    7.55s`.
  This is the criome half of the spirit gate proven in a real sandbox with real
  crypto over a real socket — the reusable harness foundation.
- **Authorization model direction captured — Spirit `t00s`** (psyche, this
  session): criome's verdict can come from a connected meta-socket approver
  (mentci responds with an approval — the vote-on-existing-object adjudication)
  or a configured auto-approve acceptance policy, within criome's
  verify-and-record model; gathered-signature quorum stays the production path.
  Note: signal-criome's schema already carries
  `AuthorizationPolicyClass [SimpleSelfSigned ComplexQuorum]` but criome's
  runtime does not yet branch on it — wiring `SimpleSelfSigned`/auto-approve
  into the decision path is the next build, then the mentci meta-socket
  authorizer. (Correction below: criome main already has a bound+served meta
  socket and the approval protocol; see the reconciliation section.)

## "Fix it all" build — accurate scope after a full origin reconciliation

Psyche: *"fix it all. no meta socket is a bug."* **Correction: the criome meta
socket is NOT missing — criome `main` already binds AND serves it.** My earlier
"criome has no meta socket" came from a STALE local checkout (`6c75804`); origin
reconciliation revealed three stale-checkout errors this session (the witness,
signal-criome's meta path, and this). I misinformed the psyche, who reasonably
called the (false) absence a bug. Verified origin state:

- **criome `main` (`1eaa783`) — meta socket fully built**: `daemon.rs::bind`
  binds both working + meta sockets; `serve_forever` serves both (non-blocking
  dual-accept loop); `handle_meta_connection` dispatches `SubmitMetaRequest` to
  `CriomeRoot::submit_meta`; `CriomeMetaConnection` + `CriomeMetaFrameCodec` +
  `CriomeMetaClient` (transport.rs:207) all exist. `meta_socket_path` from config
  or defaults to `<socket>.meta`.
- **meta-signal-criome `main` (`f14c032`) — approval protocol complete**: inputs
  `Configure(CriomeDaemonConfiguration)` + `SubmitAuthorizationApproval(
  AuthorizationApproval{evaluation, decision})`; outputs `Configured` +
  `AuthorizationApprovalRecorded`; decisions `[Approve Reject Defer]`. criome's
  `record_authorization_approval` publishes the authorized object on `Approve`.
- **signal-criome `main` (`caa02a9`)** already carries
  `(MetaSocketPath (Optional DaemonPath))` (`f31d75a`). My stale branch
  `criome-meta-authz` re-added it divergently — **deleted** (origin + local).
- **mentci `main` (`577d64b`)** declares itself "the human approval organ for the
  local per-Unix-user criome" with a daemon + `home_criome_socket_path`, but its
  live criome-meta client is a placeholder (`/tmp/criome-test.socket`).

**Genuinely-remaining work (the real "fix it all"):**
1. **auto-approve** — `AuthorizationMode [Quorum AutoApprove]` is missing from
   signal-criome (add fresh off `caa02a9`); criome `EvaluateAuthorization`
   short-circuits to `Authorized` when AutoApprove; thread via
   from_configuration/encoder. Simplest verdict source; lets spirit→criome→mirror
   run without quorum or a live approver.
2. **Configure** — currently `RequestUnimplemented(NotBuiltYet)`; implement so the
   meta socket sets the mode at runtime.
3. **mentci live approval** — wire mentci's real `CriomeMetaClient` to submit
   `SubmitAuthorizationApproval`, plus the missing criome→mentci pending-
   authorization surfacing (so mentci knows what to approve) and
   `EvaluateAuthorization` returning Pending when an external approver is armed.
4. **prove the meta socket green** — extend the cluster test with a meta-socket
   round-trip (`SubmitAuthorizationApproval`/`Configure`), turning the false
   "no meta socket" into a passing test.

**Hard lesson: `git fetch` + check `origin/main` before branching every repo** —
three duplications this session all traced to a stale local jj `main`.
- **Next (Stage B):** build spirit's gate-config arming (signer key in config →
  per-head evidence — the `criome_gate.rs` documented remaining step), then add
  the spirit+mirror legs so the spirit-daemon drives the gate and the authorized
  head fans out to a mirror on a second guest over the network (genuine
  cross-machine). The flake inputs `spirit`/`signal-criome` are already added
  and locked for that work.
