# vm-testing module on CriomOS `next` — recon

READ-ONLY recon. No live host mutated. All claims grounded in `jj file show -r <rev>`
reads of CriomOS / CriomOS-test-cluster under `/git/github.com/LiGoldragon`.

## Branch / rev

- CriomOS `next` bookmark = `qnqvptll c1931279` — "vm-testing: add VM-testing node
  feature (VmTesting variant, microvm.nix, Prometheus gpuPassthrough=false)"
  (`jj -R /git/github.com/LiGoldragon/CriomOS bookmark list`).
- CriomOS `main` = `wwpyzmtw f6755b56`; the feature is **only on `next`**, not main.
- CriomOS-test-cluster has **no `next` bookmark** — only `main`
  (`xqsqupno 4621bdd3`). No VmTesting wiring in its fixtures yet (see Fixture gap).

## How the module works

`modules/nixos/vm-testing/default.nix` (CriomOS `next`):

- It is a Horizon node-service feature. Enablement is **data-driven**, not a host
  option you set by hand: `enabled = nodeServices.has (node.services) "VmTesting"`
  and `payload = nodeServices.payload (node.services) "VmTesting"`
  (vm-testing/default.nix lines ~58-60; resolver `modules/nixos/node-services.nix`,
  `has`/`payload` over the `services` vector of single-key variant attrsets).
- Payload fields with defaults: `gpuPassthrough` (bool, default **false** — VFIO is
  armed ONLY when true), `display` (default `"Spice"`), `gpu` (PCI id string or null
  = virtio-gpu mode).
- Whole `config` is `mkIf enabled (mkMerge [...])`. Base branch:
  - `virtualisation.libvirtd.enable = mkDefault true`, spice USB redirection when
    display is spice; installs `qemu_kvm`, `OVMF.fd`, and `spice`/`spice-gtk`.
  - Projects `criomos.vmTesting.*` (enable, display, gpuPassthrough, gpu,
    criomeDomain, address, `vfioArmed = gpuPassthrough`) for checks + the
    domain-criome registration path to consume.
  - Declares the persistent microVM (below).
- VFIO branch `(mkIf gpuPassthrough { ... })` adds `intel_iommu=on amd_iommu=on
  iommu=pt` (+ `vfio-pci.ids=<gpu>` when gpu != null) and the vfio kernel/initrd
  modules. Inert on Prometheus because its payload carries `gpuPassthrough = false`.

## Host option that enables it

There is **no manual host toggle**. `options.criomos.vmTesting.enable` exists but is
*set by the module* (an output/projection), gated by the Horizon node carrying a
`VmTesting` service variant in `node.services`. To turn it on for a host: add a
`{ VmTesting = { gpuPassthrough = ...; display = ...; gpu = ...; }; }` entry to that
node's `services` vector in its Horizon fixture. The host-side module wiring (the
import) is already unconditional in `modules/nixos/criomos.nix`:
`./vm-testing/default.nix` is imported, and `inputs.microvm.nixosModules.host` is
imported when `inputs ? microvm` (criomos.nix lines ~36-46).

## Guest closure attribute

The guest is declared via microvm.nix as `microvm.vms.vm-testing` (vm-testing/default.nix
~line 165, under `microvm = lib.mkIf haveMicrovm { vms.vm-testing = { config = {...}; }; }`
where `haveMicrovm = inputs ? microvm`). Guest config:
`microvm.hypervisor = "qemu"`, `vcpu = 2`, `mem = 2048`, `graphics.enable = true`,
one interface `{ type = "tap"; id = "vm-testing"; mac = "02:00:00:00:00:01"; }`,
`networking.hostName = "vm-testing"`, `system.stateVersion = lib.trivial.release`.
The microvm.nix host module surfaces the guest runner/toplevel as
`config.microvm.vms.vm-testing.*` (the astro/microvm.nix `vms` option set); the module
itself does not name a bespoke toplevel/closure attribute beyond that.

## Networking shape (tap / bridge / IP / domain)

- Guest NIC: a **tap** interface id `vm-testing`, mac `02:00:00:00:00:01` (in-guest).
- **Host-side tap/bridge is NOT declared by this module.** The only `tap` reference is
  the guest interface; there is no `systemd.network`/netdev/bridge provisioning for the
  host tap. microvm.nix's host module would need the tap created/attached — this is the
  routing gap the standup plan must fill (the "routed" half).
- Domain: `criomeDomain = "vm-testing.${clusterName}.criome"`, `clusterName =
  cluster.name or node.name`. On the criome cluster Prometheus this renders
  `vm-testing.criome.criome` (asserted by the check).
- Address: `nodeAddress = head (split "/" node.nodeIp)` — the host's own node IP with
  the CIDR suffix stripped (e.g. `10.0.0.2`). The `.criome` authority delegates the
  name to this host; the VM is reached via the host.
- Projection: `networking.hosts = { "${nodeAddress}" = [ criomeDomain ]; }` (only when
  nodeAddress != null), matching `network/default.nix`'s `mkCriomeHostEntries` grain.

## CI check

`checks/vm-testing-prometheus-policy/default.nix`, registered in `flake.nix` as
`checks.${system}.vm-testing-prometheus-policy = pkgs.callPackage
./checks/vm-testing-prometheus-policy { inherit inputs; }` (flake.nix ~line 112).

- It is a **pure isolated eval** (same grain as `desktop-audio-policy`): `lib.evalModules`
  loads the vm-testing module against a **synthetic horizon** plus minimal option stubs,
  with `specialArgs.inputs = { }` (microvm deliberately omitted, so `haveMicrovm = false`
  and the guest block is skipped). It does **not** boot a VM or need a real cluster horizon.
- Asserts the Prometheus path: `criomos.vmTesting.enable == true`, `gpuPassthrough ==
  false`, `vfioArmed == false`, NO iommu kernel param, NO `vfio_pci` module,
  `criomeDomain == "vm-testing.criome.criome"`, and
  `networking.hosts."10.0.0.2" == [ "vm-testing.criome.criome" ]`.
- Asserts the opt-in path on a contrasting `gpu-lab` node (`gpuPassthrough = true`,
  `gpu = "10de:1234"`): `vfioArmed`, an iommu param, `vfio_pci` bound, and
  `vfio-pci.ids=10de:1234` present.
- Produces `runCommand "vm-testing-prometheus-policy-check"`. So CI validates the policy
  logic, **not** an actual booted/routed microVM — there is no `runNixOSTest`/boot check
  for the persistent VM here.

## Fixture gap (CriomOS-test-cluster)

- CriomOS-test-cluster `main` has `clusters/fieldlab*.nota` and
  `fixtures/horizon/{atlas,beacon,cedar,dune}.json`; node `services` use shapes like
  `{ "TailnetClient": {} }` (dune.json), `nodeIp` like `10.77.0.4/24`, `criomeDomainName`
  like `dune.fieldlab.criome`. **No node carries a `VmTesting` variant** (grep of every
  cluster/horizon fixture on main found zero hits). So the test-cluster does not yet
  instantiate the routed microVM — adding a `VmTesting` service entry to a fieldlab node
  fixture is the wiring step to exercise it end-to-end.

## What must be true on a host to actually run it (for the standup plan)

1. The host's Horizon node must carry a `VmTesting` service variant in `node.services`
   (and a `node.nodeIp`, else the hosts projection is skipped).
2. The CriomOS flake's `microvm` input must be present (`inputs ? microvm`) so
   `inputs.microvm.nixosModules.host` is imported and `microvm.vms.vm-testing` resolves.
   It is wired on the CriomOS flake (`microvm.url = github:astro/microvm.nix`,
   `microvm.inputs.nixpkgs.follows = nixpkgs`, flake.nix ~line 41).
3. KVM/hardware virt available (`/dev/kvm`), since `hypervisor = "qemu"` with
   `libvirtd` + `qemu_kvm`; `graphics.enable = true` wants a Spice path.
4. **Host-side routing not provided by the module**: a host tap (`vm-testing`) must be
   created and routed/bridged so the guest tap NIC is reachable and the
   `vm-testing.<cluster>.criome` → host-IP hosts entry actually resolves to a live VM.
   This is the main thing the standup must add on top of the module.
5. For Prometheus specifically: keep `gpuPassthrough = false` (AI node; GPU must not be
   bound to vfio-pci) — this is an intent constraint (Spirit 2632), enforced by the CI check.
