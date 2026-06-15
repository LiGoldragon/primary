# Frame: a general, cluster-data-generated VM-testing interface + readable OS/home-profile suite

## The psyche's directive (verbatim)

> create better interfaces in our stack for using a general vm testing, but
> using cluster-data-generated code, not cluster specific to me (node hosting
> it needs a role, interface must be predictable and/or use a generated config
> (generated in nix ostensibly with cluster data from the vm host and the
> vm-node config)), and use it to create a suite of easy-to-read tests for a
> bunch of complex os and home-profile testing

This is an **architecture proposal** for psyche review. It does not implement.
The sibling `4-design-proposal.md` is the full proposal; this file is the frame
and method.

## What the directive decomposes into

1. **General, not cluster-specific.** The interface must be derived from the
   cluster model — a function of projected horizon data — not the hand-built
   `/tmp/lojix-e2e` apparatus reports 48/49 ran on Prometheus. "Node hosting it
   needs a role" → the host is identified by cluster data, not by name.

2. **Predictable / generated config.** "Generated in nix with cluster data from
   the vm host and the vm-node config" → a Nix generator whose two inputs are
   exactly (a) the **VM host's** projected horizon and (b) the **VM-node's**
   projected config, both products of `horizon-cli`. No per-node hand-authoring
   of runners, taps, keys, or override sets.

3. **A suite of easy-to-read tests** over **complex OS configs and
   home-profiles** — the readable test layer that the existing static
   policy-eval checks cannot provide (they never boot).

## Method

Five read-only grounding sub-agents were dispatched, each citing files under
`/git/github.com/LiGoldragon` (branch `horizon-test-vm`, the live mains, and the
test-cluster) plus reports 47-49:

- **host-role** — should the VM-host be a `NodeSpecies`, a `behavesAs` facet, or
  a derived capability? What host-side data must projection expose?
- **generalize** — what is already cluster-data-generated (Unit B) vs what was
  bespoke in the live runs (reports 48/49); the generalization gap.
- **nix-generator** — what NixOS test frameworks fit the microvm constraint; the
  generator signature; how guest config + host data combine into one check.
- **profiles** — the concrete catalog of complex OS modules and home-profiles
  worth testing, each with ground-truth assertions.
- **test-loop** — the driving model (pure-nix VM tests vs lojix-deploy); the
  non-negotiable substrate constraints; the readable declarative-spec shape.

The synthesizer verified every load-bearing claim against the actual code:
`NodeService` enum shape (`proposal.rs:96-138`), `BehavesAs.test_vm` /
`virtual_machine` (`node.rs:140-217` on branch), the host fold
(`test-vm-host.nix:60-71,175`), and the `fixtureSystem` / `configurationFor`
generator pipeline (`CriomOS-test-cluster/flake.nix:114-133`,
`checks/cluster-contracts.nix:43-58`).

## What already exists (the foundation, do not rebuild)

- **Unit A** (`horizon-test-vm`): `NodeSpecies::TestVm` → `behavesAs.testVm` (the
  guest's role), `Machine.super_node` host edge, `disk_gb`/`location`.
- **Unit B** (`horizon-test-vm`): `test-vm-host.nix` folds `exNodes` on
  `superNode == thisNode && behavesAs.testVm` and emits per-guest microvm
  declaration + additive tap + guest-IP hosts entry — all from cluster data,
  zero hand-wired node names. `test-vm-guest.nix` gates leanness on
  `behavesAs.testVm`.
- **The generation pipeline**: `clusters/<c>.nota` → `horizon-cli --cluster c
  --node n` → projected `Horizon` JSON → `lib.nixosSystem { specialArgs.horizon
  = <JSON>; modules = [criomos]; }`. The `configurationFor` / `fixtureSystem`
  builders already do this for static-attribute checks.
- **The lojix deploy path** (reports 46-49): build → copy → activate → BootOnce →
  survive-disconnect, the `.drv^*` fix on lojix main, the
  `meta-lojix Deploy … build_attribute=…` one-NOTA-arg CLI.

## What is missing (what this proposal adds)

- A **host-side capability datum** (tap subnet, KVM, capacity) so the generator
  reads it from projection instead of inventing `169.254.100+i.1` in Nix.
- A **generator** `mkVmTest { hostNode; vmNode; testScript; }` producing a
  runnable flake check from cluster data alone — the first `runNixOSTest` in the
  stack, forced onto the microvm machine type.
- A **named test-substrate override profile** (writable store, require-sigs off,
  NSS/root-shell fixes, serial, label alignment) — currently re-derived ad hoc
  in `/tmp` per live run.
- The **readable suite** itself: ~12 candidate (role, size, profile) tests over
  the complex OS modules and home-profiles, each a declarative spec.

## The hard constraints any design must respect (from reports 48/49)

Non-negotiable, learned live:

1. **microvm machine type** for booting the lean profile — a generic q35 hangs
   userspace after kernel boot.
2. **Writable disk + writable `/nix/store`** (the S5 read-only failure is the
   whole reason for a modeled node).
3. **Additive tap, host untouched** (`5hir5bnz`) — user network namespace, no
   sudo, no reorder of the host's interfaces/routes/firewall.
4. **Horizon-derived address** `root@<node>.<cluster>.criome` resolving to the
   guest's own `nodeIp` — lojix targets it with zero VM special-casing.
5. **Lean-guest NSS / root-shell / require-sigs / label** pre-bakes, or the
   guest is not even SSH-reachable.

## The one tension the proposal surfaces rather than hides

The lean CriomOS profile **boots userspace on `-M microvm` but cannot do UEFI
BootOnce** (no ESP); it **does UEFI BootOnce on q35+OVMF but hangs userspace**.
So the hermetic OS/home suite uses microvm; the full-fidelity lojix smoke test's
substrate is gated on the open Unit-B q35-userspace hardening, or scoped to
assert through generation-activation (proven on microvm).
