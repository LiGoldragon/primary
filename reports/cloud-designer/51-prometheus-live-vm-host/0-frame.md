# 51 — Prometheus as the LIVE on-demand VM-testing host: frame and method

## The goal (psyche intent, report-47 integrated vision)

Make **Prometheus** the live on-demand VM-testing host: literally hosting
on-demand test VMs via the cluster-data-generated C1-C5 emission, with
lojix deploying the test configuration into each VM, additive and
host-untouched. Today the `VmHost` role is declared on **ATLAS** — a
synthetic `fieldlab` fixture node that cannot even build its full
toplevel here — not on Prometheus. That is the gap. This session
produces a plan for psyche confirmation **before anything touches
Prometheus**.

## The gap, stated precisely

The on-demand mechanism is fully built and green (C1-C6, all on
`horizon-test-vm` branches), but it is **driven from ATLAS's
projection**:

- The role datum is declared on ATLAS:
  `CriomOS-test-cluster/clusters/fieldlab.nota:29` (branch
  `origin/horizon-test-vm`):
  `[(TailnetClient) (TailnetController) (NixBuilder (Some 8)) (NixCache) (VmHost [169.254.100.0/22] Available (Some 4))]`.
- ATLAS hosts three `TestVm` Pod guests — `mercury` (`:105`),
  `base-home` (`:155`) and the `Edge` Pod `edge-desktop` (`:130`) —
  each a `Pod (… (Some atlas) (Some aria) …)`, `super_node = atlas`.
- The C4/C5/C6 generators hardcode `hostNode = "atlas"`
  (`flake.nix:131,161,207,215`) and the whole suite projects
  `--cluster fieldlab` (`flake.nix:56-66`).
- **Prometheus is declared in a different cluster repo**,
  `goldragon/datom.nota:59-97` — a production `LargeAiRouter`, `Metal`
  GMKtec EVO-X2 (8 cores / 128 GiB), services
  `[(TailnetClient) (NixBuilder (Some 6)) (NixCache)]` — **no `VmHost`**.

So closing the gap is a **modeling + harness-retarget** problem, not a
mechanism problem: declare `VmHost` on Prometheus's own projection (or
on a Prometheus host node the generators can project), retarget the
generators' `hostNode` to Prometheus, and materialize the same generated
emission output on Prometheus — choosing the run modality that respects
`5hir5bnz`.

## The binding constraint: `5hir5bnz` (router safety)

Prometheus is the live `LargeAiRouter`. `5hir5bnz` (governing decision
`se72`; live constraints `kx32`/`xv9v`/`1lex`, reconstructed in
`reports/cloud-designer/43-routed-microvm-standup/5-risk-history.md:21-45`)
forbids, concretely: a live `switch` that bounces
`hostapd`/`networkd`/`kea`/`dnsmasq` (the exact mechanism that broke
Prometheus during the gemma deploy); any activation whose connectivity is
unproven while **no out-of-band/console access exists** ("there is none
today"); leaving an unverified generation as the default boot target; and
running the risky step in the foreground SSH session. Every design choice
in the plan is checked against this.

## Two real access modalities to Prometheus (grounded)

1. **System-config root deploy.** Prometheus is a managed CriomOS UEFI
   node, root-reachable: `users.nix:45-49` sets
   `root.openssh.authorizedKeys.keys = adminSshPubKeys` on every node,
   and `adminSshPubKeys` is the horizon projection of every Max-trust
   user's keys (`horizon-rs/lib/src/node.rs:519-544`); `li` is
   `Unlimited`/`Max` with SSH keys (`datom.nota:172-187`), so li's keys
   are the root admin keys. The exercised path is
   `lojix-cli '(Deploy (Cluster goldragon) (Node prometheus) (Action switch))'`
   → `switch-to-configuration` over `ssh root@prometheus.goldragon.criome`
   (`CriomOS/README.md:25-29`; prior field deploy:
   `CriomOS/reports/0034-self-review-prom-deploy-session.md`).
   **Feasible — but on the router it re-arms the `5hir5bnz` mechanism.**
2. **User-level host-untouched (no sudo).** Login user `li` (uid 1001)
   has **no general sudo**; `/dev/kvm` is world-writable (mode 666); the
   microVM + additive tap run in a private user+network namespace
   (`unshare -rn`, li root-in-userns), qemu/lojix/ssh via `nsenter`. This
   is the **proven reports-48/49 modality**: Prometheus's real
   netns/OS/firewall verified byte-identical before/after, the
   LargeAiRouter stack intact. Leaves Prometheus's generation untouched.

These are orthogonal, both real. The plan recommends modality (2) for the
live run and modality (1) **off the table** until out-of-band access
exists.

## Method

Three grounding sub-reports were commissioned and are synthesized here:

- **prometheus-node** — where Prometheus is declared, its current role,
  and its reconfigurability (both access modalities, definitively).
- **on-demand-hosting** — what the VmHost role generates (C1-C3 output:
  the microvm `declaredRunner` + additive tap), the generated-vs-invoked
  boundary, and the cross-cluster placement blocker.
- **safety** — the `5hir5bnz` binding text, what a system-deploy of the
  VmHost emission would actually touch on the live router, and the
  host-untouched namespace alternative; recommends host-untouched.

The plan (`4-plan.md`) integrates these into a concrete, ordered,
confirmation-gated sequence: which steps are cluster-data edits, which
are builds (no host effect), and exactly which steps touch Prometheus and
how.

## Key files

- `goldragon/datom.nota:59-97` — Prometheus = production `LargeAiRouter`,
  no `VmHost` (the model edit point).
- `CriomOS-test-cluster/clusters/fieldlab.nota:29,105-180`
  (`origin/horizon-test-vm`) — ATLAS `VmHost` + the three Pod guests (the
  template).
- `horizon-rs/lib/src/proposal.rs:33-160` (`origin/horizon-test-vm`,
  `fe7182f`) — C1 `NodeService::VmHost { guest_subnet, kvm,
  maximum_guests }`, `KvmAvailability`, `MaximumGuests`,
  `VmHostCapability`, `Node::vm_host()`.
- `CriomOS/modules/nixos/test-vm-host.nix` (`origin/horizon-test-vm`) —
  C2 emission, `mkIf (hasGuests && kvmAvailable)` at `:269`, tap sliced
  from `guest_subnet`.
- `CriomOS/modules/nixos/test-substrate.nix` — C3 substrate prebakes.
- `CriomOS-test-cluster/lib/mkVmTest.nix`, `lib/mkDeployTest.nix`,
  `flake.nix:56-66,114-270` (`origin/horizon-test-vm`) — C4/C5/C6
  generators, `hostNode = "atlas"`, fixture projection from
  `--cluster fieldlab`.
- `CriomOS-test-cluster/scripts/{run,nspawn-dune}-on-prometheus` — the
  host-runner precedent (`ssh prometheus.goldragon.criome`,
  `systemd-run --user`).
- `reports/cloud-designer/43-routed-microvm-standup/5-risk-history.md:21-95`
  — `5hir5bnz`/`kx32`/`xv9v`/`1lex` binding text.
- `reports/cloud-designer/{47,48,49,50}-*` — v1 lifecycle, the proven
  host-untouched namespace run, and the C1-C6 interface.
