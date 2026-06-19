---
title: 430 — VM testing / Prometheus / durable cluster node confusion
role: operator
variant: Audit
topics: [vm-testing, prometheus, lojix, criomos, horizon]
description: |
  Grounded audit of the live conversation with system-designer: what has
  actually landed, what has only been proven in hermetic NixOS VM tests, and
  what is still missing before the psyche's intended durable cluster VM node
  exists.
---

# 430 — VM testing / Prometheus / durable cluster node confusion

## Bottom line

The psyche's intended object — a durable, installed, cluster-integrated VM node
hosted on Prometheus and usable as a normal named node for deployment/logics
testing — does **not** exist in production today.

Several adjacent things are real:

- Prometheus has working `/dev/kvm` according to system-designer report 147.
- Horizon has typed support for a VM host (`NodeService::VmHost`) and a test VM
  guest (`NodeSpecies::TestVm`).
- CriomOS has a typed `test-vm-host.nix` module that can render non-autostart
  microVM guests from Horizon projection data.
- CriomOS-test-cluster has synthetic `fieldlab` fixtures and NixOS VM tests
  using an `atlas` VM host and `mercury`/`base-home` guests.
- Lojix has a system-designer feature branch
  `/home/li/wt/github.com/LiGoldragon/lojix/live-deploy-test-chain` with a
  `runNixOSTest` proof commit described as green under KVM.

Those are useful pieces, but none is the deployed durable Prometheus-hosted
cluster node the psyche was asking about.

## The conflation

Two meanings of "VM testing" are being mixed.

### Hermetic NixOS VM test

This is a Nix flake check or named Nix test that boots QEMU guests inside a Nix
builder using `pkgs.testers.runNixOSTest`.

It is valid even though Nix is pure: the build derivation is allowed to run a
process tree in an isolated sandbox, including QEMU, as long as the declared
inputs produce reproducible outputs. It is not "pure evaluation"; it is an
impure-looking runtime contained inside a pure build boundary.

What it proves:

- generated OS images boot;
- daemon wiring works inside controlled guests;
- deploy machinery can copy/activate/assert inside the sandbox;
- no production host or cluster network is touched.

What it does **not** prove:

- a node exists in the real `goldragon` cluster;
- Prometheus is configured as a `VmHost` in production data;
- the VM has a stable cluster identity/domain on the live Yggdrasil/cluster
  fabric;
- live deployment to that node works.

### Durable cluster VM node

This is what the psyche described in the conversation: a VM that exists as an
installed cluster node, has a name, can be started and stopped, is not production
critical, and can receive real deployments/logics tests while up.

What it requires:

- `goldragon/datom.nota` declares Prometheus with a `VmHost` service;
- `goldragon/datom.nota` declares a `TestVm`/Pod node whose `super_node` is
  Prometheus;
- the Horizon projection consumes that model;
- CriomOS renders the host/guest pieces from that projection;
- cluster-operator/system-operator performs the gated production deploy path
  safely, likely BootOnce rather than live switch on the router;
- lojix live test/deploy paths can target it.

This path has not happened.

## Grounded facts checked

Production cluster data:

- `/git/github.com/LiGoldragon/goldragon/datom.nota:59-97` declares
  `prometheus (LargeAiRouter ...)`.
- Its service vector at line 97 is exactly:
  `[(TailnetClient) (NixBuilder (Some 6)) (NixCache)]`.
- There is no `VmHost` service there.
- There is no production `TestVm` node in `goldragon/datom.nota`.

Report state:

- `reports/cloud-operator/388-Handover-vm-testing-closeout.md` says the safe
  hermetic surface landed and explicitly says no live Prometheus operation,
  deploy, activation, router switch, or remediation was run.
- `reports/system-designer/147-live-lojix-deploy-into-vm-test-grounding-and-plan-2026-06-19.md`
  says Prometheus has KVM but does not declare `VmHost`, production cluster data
  has no test node, and the first live run plus `goldragon/datom.nota` edit are
  gated.
- `reports/system-designer/148-durable-production-test-vm-horizon-design-2026-06-19.md`
  correctly describes the durable node as `VmHost` on Prometheus plus a
  `TestVm` guest, but also names the production cluster-data edit as still
  gated.
- `reports/cloud-designer/51-prometheus-live-vm-host/4-plan.md` proposes the
  same production-vs-test-surface choice and explicitly marks the Prometheus
  declaration location as needing psyche confirmation.

Repo state:

- `/git/github.com/LiGoldragon/horizon-rs` main contains `NodeService::VmHost`
  and `NodeSpecies::TestVm`.
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/test-vm-host.nix` consumes
  `VmHost` and hosted `TestVm` projections.
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/vm-testing/default.nix`
  still exists and gates on a string-like `VmTesting` service surface that does
  not match Horizon's current typed model. That is a cleanup gap.
- `/git/github.com/LiGoldragon/CriomOS-test-cluster` main owns synthetic
  fieldlab tests; its `INTENT.md` explicitly says it is deliberately not
  `goldragon`.
- `/git/github.com/LiGoldragon/lojix` main still rejects live test submissions
  with `LiveNotYetEnabled`.
- `/home/li/wt/github.com/LiGoldragon/lojix/live-deploy-test-chain` contains a
  system-designer branch with `DeployIntoTestVm` / `AssertTestVm` effects and a
  `live-deploy-bracket` `runNixOSTest` check. That branch is evidence for the
  hermetic live-chain proof, not production deployment.

## What I think happened

The agents built and reported valid lower layers, but the language around them
blurred the acceptance target.

The true chain is:

1. Type support exists in Horizon.
2. Nix/CriomOS support mostly exists for rendering a VM host and guest.
3. Synthetic NixOS VM tests exist and are useful.
4. Lojix live-chain branch work exists.
5. Production `goldragon` data is not edited.
6. Prometheus is not deployed as a VM host.
7. The durable cluster VM node is not up.

So the right complaint is not "all VM testing was fake." The right complaint is
"the thing I meant by VM testing was the durable cluster node, and that final
production object was not created while nearby hermetic tests kept being reported
as if they were closing the same loop."

## Who can get it done

The missing work crosses from design/code into production cluster deployment.
That is cluster-operator/system-operator territory, with operator support.

The concrete implementation path is:

1. Decide that the `VmHost` fact belongs in production `goldragon/datom.nota`
   rather than only a synthetic test proposal.
2. Edit `goldragon/datom.nota`: append `(VmHost <guest-subnet> Available (Some
   <maximum-guests>))` to Prometheus and add a durable `TestVm` Pod node hosted
   by Prometheus.
3. Regenerate/validate Horizon projection.
4. Clean up the obsolete CriomOS `vm-testing/default.nix` string-keyed module
   or at least ensure the live path uses `test-vm-host.nix`.
5. Deploy Prometheus safely through the cluster-operator path, not a casual live
   switch on the router.
6. Start the durable VM and prove it is reachable as a cluster node.
7. Retarget lojix live deploy/assert to that durable node after the current
   branch lands or is ported.

The immediate coordination problem: current locks show `system-designer` owns
the lojix triad branch, while `cluster-operator` and `system-operator` are idle.
No lane currently owns the production `goldragon` + deploy step.

## My recommendation

Treat the durable node as a production deployment task, not another design
discussion.

The next psyche-facing request should be concrete:

"Cluster-operator/system-operator: create the Prometheus-hosted durable
`TestVm` node in production cluster data and deploy it safely. Use
`NodeService::VmHost` on Prometheus and a `NodeSpecies::TestVm` Pod guest
homed on Prometheus. Do not run a live switch on the router; use the safest
BootOnce/deploy path. Report the resulting node name, domain, state, and how to
start/stop it."

That separates it from SD's current lojix branch work. SD can continue proving
the live deploy bracket, but the cluster node itself needs a production operator
lane.
