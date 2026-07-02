# Operating-System Implementer — VM-Field Prep Evidence (2026-07-03)

Host/OS work preparing the whole-engine VM-cluster testing field on `prometheus`
(sole permanent builder) from the dev host `ouranos`. Scope: kink-ledger open
decisions (a),(c),(d),(e) + the local ssh `HostName` fold-in. Source framing:
`reports/field-readiness/02-kink-ledger.md`, `reports/field-readiness/HANDOVER.md`.

Acting model: Claude Opus 4.8 (1M context), high reasoning. Ran on `ouranos`.

## Summary of dispositions

| Item | State | Live-activated? |
|------|-------|-----------------|
| (a) nixos-test on builder line | declarative change LANDED+PUSHED+PROVEN | No — ouranos System Switch deferred to operator |
| (c) Jun30–Jul1 demo cleanup | demo runtime REMOVED; 13G worktrees DEFERRED | Yes (removal done) |
| (d) GitHub-free nix-copy inner loop | VERIFIED working + SANCTIONED in docs | Yes (verified live) |
| (e) retire persistent VM guest | REPORTED, not retired (concrete blockers) | No — no edit/deploy |
| ssh HostName fold-in | declarative change LANDED+PUSHED | No — Home Activate deferred |

All three system/home *activations* were deferred for concrete host-safety /
coordination reasons (below). Live actions actually performed: (c) removal and
(d) live verification build on prometheus.

## (a) nixos-test builder feature — CriomOS main `f8eb6ff7` (pushed)

Observed facts:
- The prometheus builder line is emitted by **ouranos's own** system build
  (`nix.buildMachines`), from `horizon.node.builderConfigs[].supportedFeatures`.
- The live projection source is `horizon-rs/lib/src/node.rs:330-337`
  (`BuilderConfig::from_node`): non-edge builders get `["big-parallel","kvm"]`,
  **no `nixos-test`**. That projection is compiled into the deployed `lojix`
  daemon (Cargo dep, `lojix/Cargo.lock:280`), which projects horizon in-process
  at deploy time and overrides only `horizon/system/deployment/secrets`.
- CriomOS `modules/nixos/nix/builder.nix` (the consumer) is re-read **fresh**
  from source on every deploy, so a change there lands with one ordinary deploy.
- The existing `checks/nix-role-policy` example builderConfig already listed
  `nixos-test` in its *input* — inconsistent with the real projection.

Changed files (committed `f8eb6ff7`, pushed to origin main):
- `modules/nixos/nix/builder.nix`: `buildMachineFor` now computes
  `supportedFeatures = if elem "kvm" builder.supportedFeatures then unique (…++["nixos-test"]) else …`.
  Rule made explicit: a kvm-capable builder is also nixos-test-capable; the two
  are bound together at the emission point so no consumer must remember it.
- `checks/nix-role-policy/default.nix`: input builderConfig changed to the real
  projection `["big-parallel","kvm"]`; added an assertion that the output
  buildMachines line becomes `["big-parallel","kvm","nixos-test"]`.

Locus decision: change lives in `builder.nix` (CriomOS), **not** horizon-rs.
horizon-rs is the canonical single home, but changing it needs the full
lojix-daemon-redeploy chain (compiled-in projector) + test-cluster fixture
regen. builder.nix is fresh-evaluated per deploy → one edit, one ordinary
deploy, functionally identical (builder.nix is the sole consumer). Recommended
follow-up: converge the feature into horizon-rs `node.rs:330-337` the next time
the lojix daemon is redeployed anyway.

Proof (non-destructive):
- Standalone eval of the real `builder.nix` fed input `["big-parallel","kvm"]`
  → `supportedFeatures = ["big-parallel","kvm","nixos-test"]`, hostName
  prometheus. (nix-role-policy full flake check additionally needs a
  lojix-materialized `horizon`; kink-20 says not to hand-write it, so the
  direct module eval is the proof.)
- Scheduling Test A: drv `requiredSystemFeatures=[kvm,nixos-test]`, current
  `/etc/nix/machines` (advertises only `[big-parallel,kvm]`) → cannot go remote
  (fell back to disabled local). Confirms the gap.
- Scheduling Test B: same drv, `--builders` line carrying `nixos-test` →
  dispatched to `ssh-ng://nix-ssh@prometheus.goldragon.criome`, built there,
  copied `scheduled-ok` back. Confirms the fix's effect.
- Note: ouranos LOCAL `system-features` already includes `kvm nixos-test`, so
  naive VM checks would otherwise run on the dev host itself — scheduling to
  prometheus is exactly what the builder-line feature enables.

Deferred (operator, host-safety): live activation is a **System Switch of
ouranos** (the dispatcher owns the builder line). The running ouranos system
store path (`c4kfjxxv…`) is NOT in lojix's tracked FullOs generations
(latest tracked: gen 19/20 `kwrk0w4j`/`dfp8lbaf`, gen 33 BootOnce `5wv10nsk`),
so the Switch delta from CriomOS main is unmeasured, and it is a self-Switch of
the live dev host mid-session (lojix even special-cases ouranos-from-ouranos,
`schema_runtime.rs:707`). Watched operator command:
```
meta-lojix '(Deploy (System (goldragon ouranos FullOs /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS?rev=f8eb6ff759fc Switch None [] None)))'
```
Verify after: `readlink -f /etc/nix/machines` line shows
`big-parallel,kvm,nixos-test` for prometheus; `nix build <local-checkout>#checks.x86_64-linux.vm-mercury`
schedules to prometheus without `--builders`. vcqx updated + `blocked-on-psyche`
label dropped (decision resolved).

## (c) Jun30–Jul1 demo cleanup

Observed:
- No demo tmux sessions remain. No demo daemon processes running (only geoclue's
  built-in demo agent and the live deployed `spirit-daemon` — both legitimate,
  left alone).
- Demo runtime dir `/tmp/criome-mentci-spirit-demo-20260701-150210` (220K): all
  5 pid files dead, all sockets dead, held a stale demo `criome.masterkey`
  secret + `criome.sema`. **REMOVED** (verified no live socket/pid holder first).
- Demo dir `/tmp/criome-mentci-spirit-demo-20260701-142204` (13G): its
  `worktrees/` are **9 registered `jj workspace add` workspaces** in the
  component repos (criome, spirit, mentci, mentci-egui, mentci-lib, router,
  signal-criome, signal-mentci, meta-signal-criome), several with uncommitted
  demo changes on a "demo workspace for criome authorization push" commit.

Deferred (boundary): the 13G `-142204` worktrees are NOT removed. They are
registered workspaces inside fenced `signal-*` and criome/spirit component repos
(out of my boundary), carry uncommitted changes intersecting the
criome-authorization work (open decision b, owned by another worker), and clean
removal would need `jj workspace forget` inside those repos. Recommend the
component-repo/authorization owner deregister (`jj workspace forget
demo-<repo>-20260701-142204` in each) then remove the tree. The older `/tmp`
cruft (mentci-criome-*, router-*, browser_use_agent_* etc., dated May–Jun 29)
is out of the Jun30–Jul1 scope and possibly other workers' active sandboxes —
left untouched.

## (d) GitHub-free inner-loop derivation shipping — VERIFIED + sanctioned

Observed / verified:
- User-level `nix copy`/`ssh` to `nix-ssh@prometheus` is **publickey-denied**
  for li (and li's `criome_test` key) — only ouranos's root SSH host key is
  authorized in prometheus's `nix.sshServe.keys`.
- But the trusted derivation-shipping path already **exists and works** at the
  nix-daemon (root) level: a forced-remote `nix-build --max-jobs 0` of a fresh
  derivation dispatched to prometheus over the host-key builder connection,
  built there, and copied the output back — **no GitHub, no user credential**.

Sanction (CriomOS-test-cluster main `e57cc8d2`, pushed): added a
"Inner loop without GitHub" subsection to `README.md` documenting that building
a **local checkout** dispatches the closure to prometheus over the daemon's
builder connection (git push stays the durable publish); explicit `nix copy`
must use the trusted host-key identity (root), since user keys aren't authorized
on the restricted `nix-ssh` account. No new trust / deploy required — the path
is enabled by the existing builder relationship.

## (e) Persistent VM guest — REPORTED, not retired

Concrete reasons it is NOT safe/in-scope to retire now (dw95 updated):
1. The surface is being actively **extended**: goldragon main HEAD `824ffe64`
   is "author two persistent TestVm guests on prometheus (mirror-alpha,
   mirror-beta)". `goldragon/datom.nota` now declares THREE TestVm nodes on the
   single prometheus VmHost (`datom.nota:97`, `169.254.100.0/22 Available
   (Some 4)`): `vm-testing` (dw95), `mirror-alpha`, `mirror-beta`
   (primary-1e6b.1). All share the one VmHost; removing it breaks mirror-*.
2. `goldragon` working copy is DIRTY (`A synchronizer.nota`) — another worker is
   actively in that repo; editing `datom.nota` would collide.
3. mirror-alpha/beta are primary-1e6b.1 (outside my authorized bead set) and tie
   to the active spirit/mirror mirror-slice front.
4. Executing retirement needs a redeploy of the **sole permanent builder**
   prometheus for an idle, network-dark, harmless guest — high blast, non-urgent.
   The ephemeral runNixOSTest path is unaffected either way.

Genuine direction conflict: open-decision-(e) wants vm-testing retired, while
primary-1e6b.1 just built mirror-alpha/beta on the same VmHost. Needs psyche
adjudication before any removal. dw95 NOT closed.

## ssh HostName fold-in — CriomOS-home main `3738e2f2` (pushed)

Observed: `~/.ssh/config` is a plain hand-patched file (not home-manager
managed): `Host prometheus.goldragon.criome prometheus` / HostName + keepalive.
criomos-home had no `programs.ssh`.

Changed (committed, rebased over a concurrent worker's Colemak push `329c93ec`,
pushed `3738e2f2`): `modules/home/profiles/min/default.nix` adds
`programs.ssh` with `matchBlocks."prometheus.goldragon.criome prometheus"`
(hostname + serverAliveInterval 20 + serverAliveCountMax 3). Parse-verified.
Submitted a lojix Home **Build** (deployment 38) — admitted
(`(Deployed (38 …))`) but produced no observable build (idle daemon, no nix
activity, DB marker unchanged); a non-activating Build creates no generation and
lojix query only supports ByNode, so the Build outcome was not confirmable.

Deferred (Home Activate): (1) activating criomos-home main now also activates
the concurrent Colemak keyd change `329c93ec` a different worker just pushed —
would deploy their change to the live host without coordination; (2)
`~/.ssh/config` clobber needs a manual backup first (no
`home-manager.backupFileExtension` set). Operator steps when ready:
`mv ~/.ssh/config ~/.ssh/config.prehm.bak` then
```
meta-lojix '(Deploy (Home (goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS-home?rev=3738e2f28a77663d525ff689fe2bf0bc80178434 Activate None [])))'
```
Verify: `readlink ~/.ssh/config` is a store symlink containing the prometheus
matchBlock. The hand-patched file was left in place (still functional) since
activation is deferred.

## Checks run
- `nix-instantiate --parse` on all edited .nix files → OK.
- Standalone `nix eval` of builder.nix logic → `[big-parallel,kvm,nixos-test]`.
- Remote scheduling Test A (fails) / Test B (dispatches to prometheus) → as designed.
- (d) forced-remote `nix-build` → built on prometheus, output returned.
- Pushes: CriomOS `f8eb6ff7`, CriomOS-home `3738e2f2`, CriomOS-test-cluster `e57cc8d2`.

## Follow-ups / open items for the psyche
- Activate (a) ouranos System Switch (watched) — command above.
- Adjudicate (e): retire vm-testing vs keep building mirror-alpha/beta on the shared VmHost.
- Component/authorization owner: deregister + remove the 13G demo workspaces (c).
- Activate ssh Home change (coordinate with the Colemak worker; back up ~/.ssh/config).
- Field-readiness observability note: lojix admitted a Home Build with no
  observable execution/outcome via journal or ByNode query — worth a diagnosis
  for the sustained deploy loop (not attempted here; touches the deploy daemon).
- Converge the nixos-test feature into horizon-rs (canonical home) on the next lojix daemon redeploy.
