# 147 — Live lojix deploy-into-VM test: grounding, the three answers, and the implementation plan

*The psyche authorized me to implement the live (non-hermetic) lojix deploy-into-VM
test myself — after first checking whether the KVM infra + test node are already in
place. This grounds the three questions against the live code and hosts, maps what's
already built (so I don't redo the cloud-operator Test-op arc), pins the exact code
gap, confirms no lane collision, and lays out a two-track plan. Lead facts:
prometheus's service vector is exactly `[(TailnetClient) (NixBuilder (Some 6))
(NixCache)]` — no VmHost; no lojix worktree exists under `~/wt` yet; `/dev/kvm` is
live on prometheus right now. Source: four grounded readers + synthesis. Spirit gate
on the authorizing prompt: task order executing `se72`/`7let` — no new capture owed.*

## Direct answers to the three questions

**(1) Is the KVM infra available on prometheus? — YES, live right now.** Probed the
host directly over `ssh prometheus.goldragon.criome`: `/dev/kvm` is present and
world-writable (`crw-rw-rw- 1 root kvm 10, 232`, mode 0666), the AMD-V `svm` CPU flag
is set, `nproc` reports 32 (the GMKtec EVO-X2 is a Strix Halo Ryzen AI Max+ 395, 16
cores / 32 threads; ~118 GiB RAM free). KVM is live via kernel auto-probe on the
`svm` CPU — `kvm_amd` loads itself even though prometheus's `/etc/modules-load.d/`
does not list it. So any transient `nix run` QEMU guest opening `/dev/kvm` with
`-enable-kvm -cpu host` accelerates immediately with **zero host changes**. Honours
Spirit `5hir5bnz`/`7let` (host-untouched transient-VM intent): no `nixos-rebuild`, no
networking change, no libvirtd.

**(2) Has the KVM node-service been added to the cluster + code written? — PARTIAL /
mostly NO.** The schema *capability* exists: `horizon-rs/lib/src/proposal.rs:128`
defines `NodeService::VmHost { guest_subnet, kvm: KvmAvailability, maximum_guests }`,
where `KvmAvailability::Available` means "/dev/kvm present; guests boot under hardware
acceleration." But **prometheus does not declare it** — its production service vector
(`goldragon/datom.nota:97`) is `[(TailnetClient) (NixBuilder (Some 6)) (NixCache)]`,
no VmHost. Two competing, unreconciled CriomOS modules exist: `test-vm-host.nix`
(keys off the real `VmHost` service, on main) and `vm-testing/default.nix` (keys off
a `VmTesting` node-service that **does not exist in the schema** — `grep VmTesting`
across horizon-rs is empty, so its gate can never fire for a real node; tip of CriomOS
`next`, commit `92490b6`). On the lojix side the live-test driver is scaffolded but
gated + unimplemented (below). So: the capability type exists, no node carries it, the
driver does not execute.

**(3) Is the test node defined in cluster data? — NO in production; YES only in the
synthetic fixture.** `goldragon/datom.nota` defines exactly five nodes — balboa,
ouranos, prometheus, tiger, zeus — none a test/microVM node. A test node exists only
in the synthetic CI fixture `CriomOS-test-cluster/clusters/fieldlab.nota`: `mercury
(TestVm ... 10.77.0.7/24 ... [(TailnetClient)])` and `base-home (TestVm ...
10.77.0.9/24 ...)`, with the fixture super-node declaring `(VmHost 169.254.100.0/22
Available (Some 4))`. None of that touches production cluster data.

## What's already built (don't redo)

The cloud-designer/cloud-operator Test-op arc (designer report 54, "lojix Test op")
was proposed, psyche-confirmed, and the **hermetic half landed end-to-end on the
triad mains**:

- **Unit 1 — horizon multi-host** (additive `super_nodes` + scoped
  `image_exchange_pub_keys`): horizon-rs main, commit `087a3b6d` (the multi-host
  node-model change), 135/135 tests green, single-host output byte-identical.
- **Unit 2 — the lojix Test op, hermetic path, REAL**: across the triad mains (lojix
  `538fdebf`, "REAL hermetic Test-op dispatch proven end-to-end"; meta-signal-lojix
  `1dbecc08`; signal-lojix `cc8bbf32`). `(Check mercury)` actually runs `nix build
  <flake>#checks.<system>.vm-<node>` via a decoupled `TestJobs` actor that survives
  client disconnect, recording a durable `TestRunRecord` with the real out-path.
  `run_hermetic_check` confirmed genuine (`schema_runtime.rs:2870-2884`), not faked.
- **Unit 3 — CriomOS scoped image-exchange key emission**: CriomOS main, commit
  `6646275d` (the image-exchange-keys closeout); gate
  `image-exchange-keys-scoped-to-co-hosts` green.

**Explicitly deferred / psyche-gated** by cloud-operator report 388 (the vm-testing
closeout): "no live run, deploy, remediation, activation, router switch, or
Prometheus host op without explicit user authorization naming target + operation."
The first live run on a real host and the prometheus `VmHost` cluster-data edit are
the gated items.

## The exact gap to a running live test

### (a) lojix CODE work — the unimplemented live chain in `schema_runtime.rs`

Verified directly. The shapes exist; the execution is stubbed.

1. **Submit-time gate** (`schema_runtime.rs:1595-1600`): a `TestMode::Live` run is
   rejected with `TestRejectionReason::LiveNotYetEnabled` before a row is minted — an
   honest reject mirroring the Deploy `UnsupportedDeployAction` precedent. The single
   on/off switch.
2. **Throwaway effect runners** (`schema_runtime.rs:2894-2926`):
   `run_bring_up_test_vm` / `run_tear_down_test_vm` build a fully-formed real
   `ssh -o BatchMode=yes root@<host>.<cluster>.criome '<systemd-run --user ...
   unshare -rn ... nsenter <runner>>'` invocation, then discard it with `let
   _invocation =` and return synthetic `TestVmBroughtUp`/`TornDown`. They never
   `.run().await`.
3. **Empty runner closure + guest IP** (`schema_runtime.rs:1382-1386` and
   `:324-332`): the Live arm passes `ClosurePath::new(String::new())` and
   `bring_up_command` hardcodes `guest_ip: String::new()`. No build step produces the
   microVM runner before bring-up.
4. **Missing deploy+assert middle** (`decide_test_effect_completion`,
   `schema_runtime.rs:1755-1782`): the bring-up arm sets stage `BroughtUp` then
   immediately `Asserted` with *nothing between*, jumps to `TearDownTestVm`, and
   teardown writes terminal `Failed(FailureStage::Assert)` — never `Passed`, because
   nothing is deployed or asserted. The bracket exists; the deploy-into-VM + assert
   effect does not exist in the schema (`nexus.rs` has
   `BringUpTestVm`/`TearDownTestVm` but no `DeployIntoTestVm`/`AssertTestVm`;
   `EffectStage` lacks Deploy/Assert arms). Note: `TestRunPhase::Deploying/Asserting`
   and `FailureStage::Deploy/Assert` already exist in signal-lojix, so no phase
   additions are needed there.

Ordered code work: add the deploy+assert effect to `nexus.rs` (and matching
`EffectStage` arms) → add a runner-closure build step before bring-up (mirror
`HermeticCheck::build_check`) capturing out-path + guest IP → make the bring-up /
teardown runners actually `.run().await` → wire deploy+assert into the bracket so
teardown records `Passed`/`Failed` from a real verdict → implement the assert (deploy
via `nix copy --to ssh-ng://root@<guest_ip>` + activate, then run the flake's
assertion over the guest) → relax/flag the submit gate. Schema edits touch the triad
in lockstep: lojix `src/schema/nexus.rs`, signal-lojix, meta-signal-lojix.

### (b) cluster INFRA work

1. **prometheus KVM enablement: NOTHING required.** Already live (question 1). Do
   **not** enable libvirtd / microvm / a persistent `VmHost` service on prometheus
   just to run a transient VM — those add routed taps, routes, and a criome-domain
   hosts entry that touch host networking (`vm-testing/default.nix:140-142`),
   contrary to the transient-VM intent. libvirtd is confirmed inactive on prometheus.
2. **The vm-testing node-service name mismatch** must be resolved before any
   declarative path works: the `vm-testing` module gates on `VmTesting`, not in the
   schema. Either point the predicate at the real `VmHost` (reading `KvmAvailability`
   off its payload) or add a typed `VmTesting` variant to horizon-rs. This is the
   substance of open bead `primary-wvey` (P2, "redo VmTesting as a typed horizon-rs
   node-service") — build on that typed shape, not the string-keyed hack on `next`.
3. **The test-node cluster-data definition** in production `goldragon/datom.nota` (a
   test node + prometheus carrying the chosen VM-host service) is a
   **production-cluster edit, psyche-gated**.

The transient-VM live test does **not** strictly require items 2 and 3 — those are
for the *declarative/deployed* routed-microVM path. The host-untouched cycle lojix
already addresses (`ssh root@<host>.<cluster>.criome` + `systemd-run --user` +
`unshare -rn` + `nsenter`) runs the transient guest without touching `datom.nota`.

## Collision / coordination

**Verdict: SAFE TO PROCEED SOLO on the lojix code work — no lane is mid-flight on
this arc.** Dumped every `orchestrate/*.lock`: only `operator.lock` is non-empty, and
it claims a *different* arc:

```
/git/github.com/LiGoldragon/router # cluster propagation Head kind classifier integration
/git/github.com/LiGoldragon/signal-standard # cluster propagation Head kind classifier integration
```

No file overlap with lojix. Every other lock — cloud-operator, cluster-operator,
cloud-designer, system-designer, system-operator — is empty. The lojix working copy
is clean; no bead is in-flight on the live-test driver.

Two soft coordination notes, neither a collision: (1) bead `primary-wvey` (the
typed-VmTesting node-service redo) — align the live-test host-set validation onto that
typed variant rather than forking the string-keyed hack on CriomOS `next`. (2)
system-designer reports 143-146 cover the lojix-daemon *cutover* and router↔criome
transport / credentials (the runtime-deploy side, distinct from the Test-op live
path) — watch for shared edits to lojix daemon plumbing if that work resumes.

**Boundaries NOT mine to cross solo:** (a) the prometheus production cluster-data
edit in `goldragon/datom.nota`, and (b) the first live run *deployed* onto prometheus
— both psyche-gated per report 388, and prometheus deploy / `nixos-rebuild` authority
belongs to cluster-operator / system-operator, not designer. (c) integrating any
branch into its repo's main is operator's job.

## Implementation plan

Claim the system-designer lock (the lojix triad). Then two tracks; the first is fully
self-contained and needs no prometheus authority.

**Track A — implement + verify the live chain hermetically, under KVM, host
untouched (solo, end-to-end).** The honest way to "test it myself" without the gated
prometheus deploy.

1. Create the lojix worktree (none exists): `~/wt/github.com/LiGoldragon/lojix/` on a
   feature branch off current lojix main, with sibling signal-lojix / meta-signal-lojix
   worktrees for the lockstep schema edit.
2. Implement the four code holes (section a) on that branch: the schema deploy+assert
   effect across the triad, the runner build step, real `.run().await` in the two
   runners, the bracket wiring, and the assert.
3. **Verify under a sandboxed `runNixOSTest` VM (KVM-accelerated)** — the harness
   owns its own throwaway guest, so the full bring-up→deploy→assert→teardown bracket
   runs against a nix-launched guest with no real host, no SSH to prometheus, no
   networking change. Add an ignored live-proof test (like the hermetic ones) driving
   the bracket to a recorded `Passed`, then mutation-prove it (break the deploy →
   the assert must record `Failed`). Honours `5hir5bnz`/`7let`.
4. Optionally run the same transient guest on prometheus's hardware via `nix run`
   (QEMU `-enable-kvm -cpu host`) since `/dev/kvm` is already world-writable —
   exercises real AMD-V acceleration with no deploy or config change (read/transient,
   still host-untouched).

**Track B — gated, needs an operator + explicit psyche authorization (NOT solo).** A
*deployed* live run targeting prometheus requires: the prometheus `datom.nota` VmHost
edit (psyche-gated production change), the typed-VmTesting resolution (bead
`primary-wvey`), reconciling the two CriomOS VM-host modules, and a closure deployed
to prometheus — all operator / cluster-operator territory. Critically, prometheus is
itself a live `LargeAiRouter`, so any live run there must use only the host-untouched
user-namespace path and must **never** `switch-to-configuration` on the router.

**Honest uncertainties.** (i) The deploy+assert effect shape is my design call —
single combined effect vs two — and the assertion spec (where the flake declares the
guest-side check) is not yet defined; I'll decide it as designer. (ii) Whether the
live test ultimately runs against a deployed routed microVM (Track B, the
`datom.nota` path) or stays a host-untouched transient guest is a genuine open intent
question — the two CriomOS modules disagree on which is canonical. Track A proves the
lojix code regardless; Track B's exact target should be confirmed before landing.
