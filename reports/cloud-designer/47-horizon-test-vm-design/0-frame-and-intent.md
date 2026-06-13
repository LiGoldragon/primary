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
