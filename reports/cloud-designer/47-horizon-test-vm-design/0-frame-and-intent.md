# 47 · Horizon test-VM infrastructure — design frame + captured intent

## Captured psyche intent (2026-06-13)

> *"I want it integrated, but not always running. with a proper role created in
> horizon, and a way to define a cluster node as the test vm (and its
> location/host/etc)."*

(Spirit capture is pending — the deployed Spirit Justification/verbatim-quote
wire shape has drifted from the recalled form and `spirit-daemon` is flaky;
this report is the durable record until the formal Spirit `Decision` is
written. **To capture when Spirit is healthy.**)

**Clarified decision.** Test VMs are **durable, on-demand, horizon-integrated**
infrastructure — not ad-hoc throwaways (this evolves the throwaway framing of
`se72`/`7let` per explicit psyche direction). Specifically:

1. **A proper test-VM role/species in horizon** — a node *kind* the cluster
   model understands, alongside the existing roles (Center, Edge, EdgeTesting,
   LargeAiRouter, …).
2. **A cluster node declared AS a test VM** in the proposal (`datom.nota`),
   naming its **host** (the physical node the VM runs on), its **location**,
   and its resources (cpu/mem/disk).
3. **On-demand lifecycle** — the VM is launched to run a test and stopped
   after; it is *not* always running (so it isn't the always-on `vm-testing`
   microVM module as-is).
4. **Integrated** — lojix deploys to it like any node (it has a real identity /
   Criome domain), and CriomOS configs validate against it; the daemon's
   copy + activate target it via the normal horizon-derived address.

This is the right durable replacement for the `/tmp` throwaway. The S5 live run
already proved the pieces work: the lojix daemon builds a real OS, and a real
writable-disk qcow2 (`make-disk-image`) is a genuine bootable, ssh-reachable,
RW-store node — the e2e only stalled on a stale fixture hash, which a
horizon-modeled test node sidesteps.

## Psyche decisions on the proposal (2026-06-13)

- **Substrate: real KVM microVM** (own kernel + a real virtual disk) — NOT an
  nspawn container. The grounding leaned nspawn for simplicity; the psyche
  chose the faithful VM (consistent with `se72`/`7let`/the KVM+virtual-disk
  direction). So CriomOS emits a `microvm.nix` guest (with the non-autostart +
  tap + guest-IP wiring the proposal named), not `criomos-nspawn`.
- **Lifecycle: v1 host-triggered now.** A host-side runner does
  create+start → lojix `Deploy` → stop; **lojix is unchanged** (it just
  deploys to the node's `<node>.<cluster>.criome` address). The lojix-driven
  `StartNode`/`StopNode` meta op (v2) is a deferred follow-on.
- (These refine the report's captured intent; Spirit capture of both still
  pending the daemon/wire-shape fix.)

## Implementation order (psyche-approved)

A (horizon foundation): horizon-rs model — `NodeSpecies::TestVm`, `Machine`
`disk_gb` + `location` (+ `Location` newtype), `node.rs` `test_vm` facet — +
golden projection test + declare a test-VM node (real disk, not tmpfs) in
`CriomOS-test-cluster/clusters/fieldlab.nota`. B (CriomOS): gate the lean guest
on `behavesAs.testVm`; emit the microVM guest + tap + guest-IP `networking.hosts`
+ non-autostart unit on the host. C (trigger + live e2e): the host-side runner,
then bring the real microVM up and have lojix deploy into it. Code repos
(horizon-rs/CriomOS/CriomOS-test-cluster) use designer feature branches in
`~/wt`; operator integrates main.

## What to design (this meta-report)

Ground the actual horizon model + CriomOS derivation, then design:
- the test-VM **role/species** in horizon-rs (the model + projection);
- the **node-as-test-VM** proposal declaration: host (the physical node),
  location, resources — i.e. modeling "node X is a VM hosted on node Y";
- the **on-demand lifecycle** (who launches/stops it, how);
- the **CriomOS derivation** (role → the VM definition on the host; the guest's
  initial config so it's a deployable target);
- **lojix integration** (deploy-to-test-node via the horizon-derived address).

Output is a design proposal for psyche review before implementing (it changes
the horizon model — an architecture change).

## Method

Read-only grounding fan-out (horizon model; CriomOS derivation + the existing
vm-testing module; the host/location + on-demand lifecycle modeling), then a
design synthesis. No live changes.
