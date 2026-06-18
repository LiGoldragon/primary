# 140 — Handoff to system-operator: deploy the cross-host router transport (L1 → L2 → L3)

*The psyche asked what I can hand to system-operator. This session got the router
cross-host transport to **L1 (proven across two real kernels under KVM)**; the
ladder from here to a real two-host deployment is platform/deploy work — your
lane, not mine. This packages it. Each item names its locators and is honest about
what's ready now vs. gated on operator merging my feature branches to code-repo
main.*

## The realness ladder (report 136), where we are and who owns each rung

| Rung | What | State | Owner |
|---|---|---|---|
| L0 | in-process loopback forward | done | (done) |
| L1 | two real kernels, real VM network, delivery witnessed | **done, GREEN under KVM** (138/6) | (done) |
| L2 | routed over **Yggdrasil** peers, not a virtual bridge | not built | **system-operator** |
| L3 | two real hosts (ouranos ↔ prometheus) over the mesh | not built | **system-operator / cloud-operator** |

## Ready now (NOT gated on a code-repo merge)

1. **Stand up the L1 nixosTest as a standing check on a KVM host.** The test
   `router-two-kernel-cross-host-transport` lives on the `router` branch
   `transport-two-kernel-e2e-138` (the two-kernel transport e2e). It built and ran
   to exit 0 under `/dev/kvm`, but only with `dangerouslyDisableSandbox` inside an
   agent sandbox. Making it a standing CI check on a KVM-capable host gives the
   transport a permanent regression net. Pure platform readiness — no code change.

2. **Enable Yggdrasil for the L2 rung.** Yggdrasil is configured in CriomOS
   (`CriomOS/modules/nixos/network/yggdrasil.nix`) but **disabled in the test
   cluster** (`CriomOS-test-cluster/flake.nix`, `lib.mkForce false`). Turning it on
   and verifying mesh connectivity between two nodes is platform work independent
   of the router code — it's the substrate L2/L3 need. The m3 deploy plan
   (`reports/designer/669-first-e2e-offline-build/4-router-m3-deploy-plan.md`)
   already picks the Yggdrasil fabric and names node addresses in `datom.nota`.

## Queued behind operator merging the transport branches to `router` main

3. **Harden `message-router.nix` from test-fixture into a real deployed service
   module.** I created a *minimal* module at `nix/modules/message-router.nix` (on
   `transport-two-kernel-e2e-138`): it encodes typed NOTA → rkyv in `ExecStartPre`
   (two one-arg encoders `router-encode-configuration` / `router-encode-bootstrap`)
   then runs `router-daemon <config.rkyv>` with one argument, no flags — the daemon
   discipline is already honored. It's the seed, not production: you own the state
   dir, key paths, restart/SEMA-resume, and the `criome_socket_path` wiring (note:
   the daemon now *refuses to start* with a criome socket set until the milestone-3
   criome client lands — `Error::CriomeVerifierUnavailable`, by design). This is the
   `message-router.nix` half of report 137 §5 / 669/4. The `criome.nix` module is
   the sibling that doesn't exist yet.

4. **The L3 rung: deploy `router-daemon` on ouranos ↔ prometheus over the mesh.**
   Register each as a remote router (`RegisterRemoteRouter` at its Yggdrasil/tailnet
   address) and run a real cross-host forward. The transport is on branches
   `transport-p1-fixes-138` (the P1 fixes + production verifier fence) and
   `transport-two-kernel-e2e-138` (the test + module + `router-forward-probe`
   client) — operator merges those to `router` main first.

## Further out (named so it's not lost)

- **Provision per-machine criome node identities** with the offline cluster-root
  admission ceremony — branch `cluster-root-admission-ceremony` on `criome` (the
  one-shot minting tool that produces a cluster-root-signed `RegistrationStatement`
  the on-main `ClusterRoot::admits` gate accepts). This is the key-custody/`q1le`
  deploy step for real multi-host criome; gated on the ceremony merging + the
  criome client existing.

## What is NOT for system-operator (so the lanes stay clean)

Operator, not system-operator, owns: merging all four feature branches to
code-repo main; creating the `signal-standard` GitHub remote; and the
`signal-criome` positional migration (designer's Woe-4) that unblocks regenerating
the criome contracts. Those are code-integration, not OS/platform/deploy.

## Note

This handoff is the transport-deploy path only; it does not depend on the
in-flight `attendance-fanout-139` / `attested-moment-majority-guard-139` build
(workflow `wgpa80oej`). If you'd rather track these as beads than a report, say so
and I'll mint them.
