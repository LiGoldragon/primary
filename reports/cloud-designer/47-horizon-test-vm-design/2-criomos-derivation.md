# CriomOS derivation + the existing vm-testing module — how a role becomes a VM

Read-only grounding for cloud-designer. Repo `/git/github.com/LiGoldragon/CriomOS`;
`main` = `8762286b`, `next` = `c1931279` (vm-testing lives on `next`). All citations
are jj-shown file content from those revisions.

## 1. How a node's horizon becomes its NixOS config (the derivation chain)

CriomOS is a single `nixosSystem` whose every module receives the projected
`horizon` (cluster, node) view as a `specialArg`. There is no per-node config
file; the config is a pure function of horizon data.

- The whole system is one `nixpkgs.lib.nixosSystem` with
  `specialArgs = { horizon; system; deployment; inputs; constants; criomos-lib; }`
  and a single module `inputs.self.nixosModules.criomos`
  (`flake.nix:121-145`). `horizon = inputs.horizon.horizon` — a flake input
  lojix overrides per deploy with a content-addressed horizon flake
  (`flake.nix:85`, stub contract `stubs/no-horizon/flake.nix:4-23`).
- The top aggregate `modules/nixos/criomos.nix` is just an `imports` list:
  `normalize.nix`, `users.nix`, `network`, `edge/default.nix`,
  `metal/default.nix`, `router/default.nix`, and (on `next`)
  `vm-testing/default.nix` plus the microvm host module
  (`criomos.nix:16-47`). No branching here.

There are **two distinct gating mechanisms** the module tree branches on:

### (a) `behavesAs.*` / `size.*` — derived boolean facets of the node
These come pre-derived in the horizon JSON (projected by horizon-rs; CriomOS
only consumes them — they are `inherit (horizon.node) size behavesAs ...`,
`normalize.nix:22-28`). They are booleans, not a single enum role:

- `behavesAs.{bareMetal, edge, center, iso}` and `size.{min, medium, large, max}`.
- Modules gate whole config blocks on them. The densest example, `metal/default.nix`,
  is entirely wrapped in `mkIf behavesAs.bareMetal { ... }`
  (`metal/default.nix:295`), and inside branches further:
  `ledger.enable = behavesAs.edge` (`:311`),
  `libvirtd.enable = size.max && behavesAs.edge` (`:625`),
  `waydroid.enable = size.max && behavesAs.edge` (`:626`),
  `optional (size.min && behavesAs.edge) "uinput"` (`:337`).
- `normalize.nix` likewise: `documentation.enable = ... && !behavesAs.iso`
  (`:99-100`), iso-vs-edge package split (`:122-148`),
  `strongswan.enable = !behavesAs.iso` (`:191`),
  `pipewire = mkIf hasAudioOutput` (`:178`).

So "role" in CriomOS today = a vector of derived boolean facets, NOT a single
species enum the Nix layer reads. A new **test-VM species** would surface to Nix
as either (i) a new `behavesAs.*` facet (e.g. `behavesAs.testVm` for the GUEST's
own config) and/or (ii) a node-service variant on the HOST (next item).

### (b) Node-services — vector of variant payloads, resolved by `nodeServices`
`modules/nixos/node-services.nix` is a tiny resolver (`{ lib }` -> rec set):

- `has services name` — `builtins.any (s: serviceName s == name) ...`
  (`node-services.nix:38`).
- `payload services name` — returns the matching variant's attrs (`:40-45`).
- A service is either a bare string or a single-key attrset
  `{ VariantName = { ...payload... }; }` (`serviceName`/`servicePayload`,
  `:13-26`).

This is exactly how the vm-testing feature is gated (next item). `VmTesting` is
"resolved by node-services.nix exactly like `TailnetClient`"
(`vm-testing/default.nix:23-24`).

## 2. The existing vm-testing microVM module (on `next`)

`modules/nixos/vm-testing/default.nix` (211 lines). Intent: Spirit 2630/2631/2632
— a QEMU/KVM node to test CriomOS visually (GPU/gamma), reachable via a Criome
domain, with per-node VFIO opt-in (`:10-33`).

### Gate
- `nodeServices = import ../node-services.nix { inherit lib; }`
  (`:46`).
- `enabled = nodeServices.has (node.services or []) "VmTesting"` (`:48`);
  `payload = nodeServices.payload ... "VmTesting"` (`:49`).
- Whole `config` is `mkIf enabled (mkMerge [ ... ])` (`:113`).
- Payload fields with defaults: `gpuPassthrough` (default false),
  `display` (default "Spice"), `gpu` (default null) (`:55-57`).

### What it emits on the HOST (the node carrying the VmTesting service)
1. QEMU/KVM substrate on the host: `virtualisation.libvirtd.enable = mkDefault true`,
   `spiceUSBRedirection` when display=spice, packages `qemu_kvm`, `OVMF.fd`,
   spice tools (`:115-130`).
2. Criome-domain projection: `criomeDomain = "vm-testing.${clusterName}.criome"`
   (`:64`), resolving to the HOST's own node IP, CIDR stripped
   (`nodeAddress`, `:70-71`). Emitted as a host file entry
   `networking.hosts.${nodeAddress} = [ criomeDomain ]` (`:140-142`).
   Structured projection re-surfaced under `config.criomos.vmTesting.*`
   (`:144-154`) for domain-criome registration and checks.
3. The guest itself, declared through microvm.nix, guarded by
   `haveMicrovm = inputs ? microvm` (`:76`):
   ```
   microvm = lib.mkIf haveMicrovm {
     vms.vm-testing = { config = {
       microvm = { hypervisor = "qemu"; vcpu = 2; mem = 2048;
                    graphics.enable = true;
                    interfaces = [ { type="tap"; id="vm-testing";
                                     mac="02:00:00:00:00:01"; } ]; };
       networking.hostName = "vm-testing";
       system.stateVersion = lib.trivial.release; };
     };
   };   (:162-182)
   ```
4. VFIO branch — `mkIf gpuPassthrough { ... }` (`:190-209`): IOMMU kernel params,
   `vfio-pci.ids=${gpu}`, vfio kernel/initrd modules. Inert when false.

### What it does NOT do (the gaps for a deployable on-demand test VM)
- The guest `config` is **minimal and inline** — only hypervisor/cpu/mem/gpu/
  one tap iface/hostname/stateVersion. It is NOT a CriomOS image: no
  `services.openssh`, no `users` / authorized keys, no operator key, no IP/route.
  It is a viewable Spice endpoint, explicitly "the desktop/component test surface
  is exercised by the ephemeral runNixOSTest checks; this persistent VM is the
  long-lived, human-viewable endpoint" (`:156-161`). It is **not a deploy target**.
- The tap interface has an `id` and `mac` but **no host-side tap setup, no guest
  IP, no `networking.hosts` for the guest** — the criome domain resolves to the
  HOST's IP, not the guest's. So lojix could not SSH-deploy to the guest as a node.

### Always-on vs on-demand
**Always-on as written.** microvm.nix's `microvm.vms.<name>` host declaration
creates a `microvm@<name>.service` that the host module enables and (by default)
auto-starts at boot — a "persistent routed test microVM" / "long-lived" endpoint
(`:31-33`, `:156-161`). Nothing in the module sets it to manual-start or socket-
activated. On-demand is achievable (microvm.nix supports `autostart`/manual
`microvm -r`/systemd `Restart`+manual start), but the current module does not
express it; making the test VM **on-demand** requires emitting a non-autostart
guest unit (or a `microvm-vms` declaration the host can `start`/`stop`).

## 3. How a HOST runs a guest today + what a TestVm role must emit

### Host mechanism
microvm.nix host module (`inputs.microvm.nixosModules.host`) imported in
`criomos.nix:45-47` only when `inputs ? microvm`. It turns each
`microvm.vms.<name>` into a per-guest systemd service running QEMU. That is the
only guest substrate wired today (`libvirtd` is enabled but unused for the
declared VM). So a TestVm host emits a `microvm.vms.<name>` declaration; the host
module does the rest.

### The deploy-target / SSH model (how lojix reaches any node)
- Every node runs sshd, keys-only, no passwords:
  `services.openssh.enable = true; settings.PasswordAuthentication = false; ports=[22]`
  (`normalize.nix:171-176`).
- Operator/admin access is the **root** authorized keys:
  `users.users.root.openssh.authorizedKeys.keys = adminSshPubKeys`
  where `adminSshPubKeys = horizon.node.adminSshPubKeys`
  (`users.nix:16-17, 45-49`). Per-user keys come from `horizon.users`
  (`users.nix:22, 30`).
- Reachability is `networking.hosts` built from each node's `nodeIp`/
  `criomeDomainName`/`yggAddress` by `mkCriomeHostEntries`
  (`network/default.nix:26-66, 90`), plus the ssh_known_hosts file from
  `exNodes` `criomeDomainName` + `sshPubKeyLine` (`normalize.nix:36-43`).

### What a first-class on-demand TestVm role must emit
On the **HOST node** (carries the `TestVm` service / is the named physical host):
- `microvm.vms.<guestName>` with hypervisor/vcpu/mem from declared resources,
  and a **fully set-up tap**: host tap device + guest IP/route so the guest is
  reachable (today only an unconfigured tap `id`/`mac` exists,
  `vm-testing/default.nix:170-176`).
- A **non-autostart / manually start-stoppable** guest unit so it is launched to
  test and stopped after (the current always-on declaration must become on-demand).
- A `networking.hosts` entry resolving the GUEST's criome domain to the GUEST's
  IP (today it points at the host IP, `:140-142`) so lojix and ssh_known_hosts
  resolve the guest as its own node.

On the **GUEST** (an initial bootable, deployable CriomOS image):
- A real CriomOS guest config, not the 7-line inline stub: it must carry
  `services.openssh` + `users.users.root.openssh.authorizedKeys.keys =
  adminSshPubKeys` (the operator key) so lojix can SSH-deploy into it exactly
  like any node (mirrors `users.nix:45-49` / `normalize.nix:171-176`).
- Its own horizon facets so the rest of the module tree derives a sane minimal
  config — i.e. the new **test-VM species** surfaces as a `behavesAs.*` facet (or
  a `size.min`-like profile) on the guest's own horizon, and the guest is a
  declared cluster node in the proposal whose `nodeIp`/`criomeDomainName` feed
  `mkCriomeHostEntries` and `ssh_known_hosts`.
- A bootable disk/state so it can come up unattended, then accept the deploy.

### Net shape for the design
Two horizon-projected facts, not one: (a) the **HOST** node gains a service/
field naming the guest, its resources, location, and on-demand flag, and emits
the `microvm.vms.<name>` + tap + guest-IP host entry; (b) the **GUEST** is itself
a declared cluster node with a test-VM species facet, an initial bootable
CriomOS config carrying sshd + operator key, so lojix treats it as an ordinary
deploy target and CriomOS checks validate it like any node. The existing
vm-testing module is the host-side scaffold to extend; it is currently a viewable
always-on Spice endpoint, not a deployable on-demand node.
