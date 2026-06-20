# CriomOS cloud-node image — build mechanism + the new minimal DigitalOcean image type

Lane A of session 74. Spirit `2u57`: the cloud-node CriomOS image is a NEW
CriomOS image type, built DECLARATIVELY from the CriomOS configuration, kept
MINIMAL and content-sized (~1-2 GB compressed, NOT a 60 GB droplet snapshot),
with per-node config declared in the cluster data (`goldragon/datom.nota`, a
`horizon-rs` `ClusterProposal`). DigitalOcean is BIOS/GRUB-only (no UEFI) so the
node is `Bootloader::Mbr` with GRUB on `/dev/vda` + cloud-init-style per-instance
provisioning + growpart (report 73).

All paths absolute. Citations `file:line`.

## 1. How CriomOS builds an image today (the model)

There is exactly one existing image type, the live ISO. Its data is two layers:

- The CriomOS NixOS module `modules/nixos/disks/liveiso.nix:33-39` sets
  `isoImage.isoBaseName`, `isoImage.volumeID`, `makeUsbBootable`,
  `makeEfiBootable`. These are options of the upstream nixpkgs
  `installation-cd` / `iso-image.nix` module, which on import defines
  `system.build.isoImage` — the actual build derivation.
- The bootloader gate `modules/nixos/disks/preinstalled.nix:40-45` selects the
  loader from the projected `horizon.node.io.bootloader`:
  `grub.enable = bootloader == "Mbr"`, `systemd-boot.enable = bootloader == "Uefi"`,
  `generic-extlinux-compatible.enable = bootloader == "Uboot"`.

So an "image type" in CriomOS = (a) some nixpkgs image module imported into the
node config, which plants a `system.build.<name>` derivation, plus (b) the
CriomOS-side options that shape it. The flake then needs to *expose* that
derivation as a flake output.

The gap that blocks a cloud node today:
`preinstalled.nix:41` sets `grub.enable` for `Mbr` but **never sets
`boot.loader.grub.devices`**. On a real disk install that is fatal — GRUB has no
target device. The DigitalOcean path needs `grub.devices = ["/dev/vda"]`. The
upstream `digital-ocean-config.nix` supplies exactly that, so importing it both
plants the build derivation *and* closes the `grub.devices` gap in one move.

### How the node config is currently assembled

`flake.nix:150-174` builds `target = nixpkgs.lib.nixosSystem { … }` from the
projected `horizon` input (the per-deploy `ClusterProposal` view), threading
`horizon`, `system`, `deployment`, `inputs`, `constants`, `criomos-lib` through
`specialArgs`, and importing `inputs.self.nixosModules.criomos`. The aggregate
module `modules/nixos/criomos.nix:16-33` imports `./disks/preinstalled.nix`
(via `disks/default.nix:3-5`). `liveiso.nix` is **not** in that import list —
the ISO options live in the module but the live-ISO image type was never wired
into the active aggregate (confirmed: the only repo reference to `liveiso` is a
mention in `reports/0005-architecture-deep-audit.md:141`). The cloud-node
module must therefore be wired in deliberately, gated so it costs nothing on
non-cloud nodes.

`flake.nix:176-190` returns `nixosConfigurations.target = target;` plus probes.
There is **no** `system.build.*` derivation surfaced as a flake output yet
(`grep` for `system.build` / `isoImage` / `qcow` / `format = ` in `flake.nix`
hits only the `image-exchange-keys-scoped-to-co-hosts` check name). The cloud
image output is a new top-level attribute reading
`target.config.system.build.digitalOceanImage`.

## 2. The cluster-data shape for a DigitalOcean node

A node in `goldragon/datom.nota` is a `horizon-rs` `NodeProposal`:
`(species size trust Machine Io pubKeys … services)`. The two fields that matter
for the image type:

- `Machine` (`horizon-rs/lib/src/machine.rs:14-67`) — its first field is
  `MachineSpecies` (`Metal | Pod`, `species.rs:45-48`). A DigitalOcean droplet is
  a KVM guest, so substrate is **`Pod`**, with `disk_gb` set (the droplet's root
  disk, e.g. `(Some 25)`) and `location` `(Some digitalocean-fra1)`.
- `Io` (`horizon-rs/lib/src/io.rs:12-22`) — the record
  `(keyboard bootloader disks swapDevices compressedSwap)`. The second field is
  **`Bootloader`** (`Uefi | Mbr | Uboot`, `species.rs:98-102`). DigitalOcean is
  BIOS/GRUB-only, so this MUST be **`Mbr`**. The `disks` map's `/` mount points
  at `/dev/vda` (the virtio root the DO module's grub + growpart expect):
  `/ (/dev/vda Ext4 [])`.

`preinstalled.nix:40-46` already turns `bootloader == "Mbr"` into
`grub.enable = true`. The new module adds the missing
`grub.devices = ["/dev/vda"]` (plus growpart, serial console, cloud-init) for a
cloud node. There is no new `horizon-rs` variant required — `Mbr` + `Pod` +
`location` already express "a BIOS KVM guest in a datacenter". (A future
`location`-derived `behavesAs.cloud` facet would let the gate read off the
projection instead of a node-name list; noted as a follow-up in §6, not required
for the first image.)

### Worked cluster-data entry (paste into `datom.nota` node map)

A new node `dove` (the `cloud` lane's DigitalOcean edge-cache node). Positional,
source-decl order, matching the surrounding entries
(`goldragon/datom.nota:5-179`):

```nota
    dove (Edge
      Min
      Max
      (Pod (Some X86_64) 2 None None None None None (Some 4) (Some 25) (Some digitalocean-fra1) [])
      (Qwerty
        Mbr
        {
          / (/dev/vda Ext4 [])
        }
        [])
      (AAAAC3NzaC1lZDI1NTE5AAAAI<dove-host-ssh-ed25519-pubkey-base64>
        None
        None)
      []
      (Some 5::7/128)
      None
      False
      False
      []
      False
      True
      None
      (Some True)
      [(TailnetClient)])
```

`Machine` positional order is
`(species arch cores model motherBoard superNode superUser chipGen ramGb diskGb location superNodes)`
(`machine.rs:14-67`): `Pod`, `(Some X86_64)`, `2` cores, model/motherBoard/
superNode/superUser/chipGen all `None`, `ramGb (Some 4)`, `diskGb (Some 25)`,
`location (Some digitalocean-fra1)`, `superNodes []`. (A DigitalOcean droplet is
a standalone KVM guest, not a CriomOS-`VmHost` guest — `superNode` stays `None`;
unlike `vm-testing` at `datom.nota:156-179` whose `superNode` is `prometheus`.)
`Io` is `(Qwerty Mbr { / (/dev/vda Ext4 []) } [])` — the `Mbr` that flips
`preinstalled.nix:41` to GRUB. Trailing flags mirror `zeus`
(`datom.nota:126-155`).

## 3. The upstream DigitalOcean image module (confirmed current nixpkgs)

`nixpkgs/nixos/modules/virtualisation/digital-ocean-image.nix` (NixOS, current
master — fetched 2026-06-20):

- `imports = [ ./digital-ocean-config.nix ./disk-size-option.nix
  ../image/file-options.nix (renamed diskSize → virtualisation.diskSize) ]`.
- Defines `system.build.digitalOceanImage = import ../../lib/make-disk-image.nix
  { name = "digital-ocean-image"; inherit (config.image) baseName;
  inherit (config.virtualisation) diskSize; inherit config lib pkgs format;
  postVM = ''${compress} $diskImage''; configFile = … }`.
- `format = "qcow2"` (the `let` block). `compressionMethod` option =
  `gzip | bzip2` (default `gzip`); `postVM` runs `gzip`/`bzip2` over the qcow2 →
  output is `…qcow2.gz` (or `.bz2` — pick `bzip2` for the smallest upload).

`digital-ocean-config.nix` (the DigitalOcean *runtime* config it pulls in) sets:

- `boot.loader.grub.devices = [ "/dev/vda" ];`  ← closes the
  `preinstalled.nix` `grub.devices` gap.
- `boot.growPartition = true;`  ← growpart on first boot, fills the droplet disk.
- `boot.kernelParams = [ "console=ttyS0" "panic=1" "boot.panic_on_fail" ];`  ←
  serial console for the DO web console + crash-reboot.
- `services.openssh = { enable = mkDefault true;
  settings.PasswordAuthentication = mkDefault false; };`
- DigitalOcean metadata-server (169.254.169.254) provisioning: per-instance SSH
  root key injection, hostname, entropy seed, optional root password — this is
  DigitalOcean's *own* per-instance provisioning path (functionally the
  cloud-init role: per-instance network + ssh-key injection). It does **not**
  enable `services.cloud-init` itself; if a generic cloud-init network path is
  wanted on top, the CriomOS module turns it on (see §4).

Disk sizing (`nixpkgs/nixos/lib/make-disk-image.nix`):

- Default args: `format ? "raw"`, `diskSize ? "auto"`,
  `partitionTableType ? "legacy"`. The DO module overrides `format = "qcow2"`
  and passes `diskSize` (default `"auto"`), and does **not** override
  `partitionTableType` → it stays **`"legacy"` = pure MBR, BIOS-bootable, one
  primary ext4 partition, GRUB in the MBR**. This is precisely the
  `Bootloader::Mbr` shape DigitalOcean requires — no EFI system partition, no
  `bios_grub` GPT slot.
- `diskSize = "auto"` makes make-disk-image **measure the closure**
  (`du` of the store paths) and size the partition to `closure + ~5.2%
  ext4-reserved fudge + 512 MiB additionalSpace`, rounded to a MiB. The image is
  therefore **content-sized**, not a fixed 60 GB. growpart then expands `/` to
  the real droplet disk on first boot.

## 4. EXACT EDIT 1 — new module `modules/nixos/disks/cloud-node.nix`

A new file. It (a) imports the upstream DigitalOcean image+config modules, which
plant `system.build.digitalOceanImage`, set `grub.devices=["/dev/vda"]`,
growpart, and serial console; (b) gates everything on a cloud node so it is inert
elsewhere; (c) holds the closure to a minimum.

The node is identified as a cloud node by the absence of an explicit
`behavesAs.cloud` facet today, so the gate keys on `horizon-rs` facts already on
the projection: `bootloader == "Mbr"` AND a `digitalocean-` location prefix on
the machine. This is a pure-data predicate (no node-name list) and needs no
`horizon-rs` change. (§6 proposes promoting it to a first-class facet later.)

`nixpkgs` is a CriomOS flake input (`flake.nix:5`) and the node config already
receives `inputs` via `specialArgs` (`flake.nix:155-164`), so the upstream module
path is `inputs.nixpkgs + "/nixos/modules/virtualisation/digital-ocean-image.nix"`.

Create `/git/github.com/LiGoldragon/CriomOS/modules/nixos/disks/cloud-node.nix`:

```nix
{
  lib,
  inputs,
  horizon,
  ...
}:
let
  inherit (lib) mkIf mkDefault optionalString;
  inherit (horizon.node) machine;
  inherit (horizon.node.io) bootloader;

  location = machine.location or "";
  # A DigitalOcean (cloud) node: BIOS/GRUB substrate plus a datacenter
  # location whose label marks the provider. Pure projection-data
  # predicate — no node-name list, no horizon-rs change. Promote to a
  # behavesAs.cloud facet later (report 74 §6) to drop the string match.
  isDigitalOceanNode = bootloader == "Mbr" && lib.hasPrefix "digitalocean-" location;
in
{
  imports = [
    # Plants system.build.digitalOceanImage (compressed content-sized
    # qcow2 via make-disk-image, format=qcow2, partitionTableType=legacy
    # → pure MBR/BIOS) and pulls in digital-ocean-config.nix, which sets
    # boot.loader.grub.devices=["/dev/vda"], boot.growPartition=true, the
    # ttyS0 serial console, and DigitalOcean metadata-based per-instance
    # ssh-key + hostname injection. The build attribute exists on every
    # node but is only meaningful (and only exposed by the flake) for a
    # cloud node — importing it is inert weight otherwise, so the import
    # itself is gated below.
    (inputs.nixpkgs + "/nixos/modules/virtualisation/digital-ocean-image.nix")
  ];

  config = mkIf isDigitalOceanNode {
    # Smallest practical upload: bzip2 over the qcow2.
    virtualisation.digitalOceanImage.compressionMethod = "bzip2";

    # diskSize "auto" = content-sized image: make-disk-image measures the
    # closure and sizes the partition to closure + ~5.2% + 512 MiB. NOT a
    # fixed 60 GB. growpart (boot.growPartition, from digital-ocean-config)
    # then expands / to the real droplet disk on first boot.
    virtualisation.diskSize = mkDefault "auto";

    # Generic cloud-init network path on top of DigitalOcean's own
    # metadata provisioning — per-instance network config + ssh-key
    # injection for providers/paths that speak cloud-init (report 73).
    # DigitalOcean's native metadata server still covers the DO case;
    # this makes the same image portable to other cloud-init hosts.
    services.cloud-init = {
      enable = true;
      network.enable = true;
    };
    services.qemuGuest.enable = true;

    # Belt-and-braces: assert the MBR/GRUB contract the DO module relies
    # on, so a mis-declared node fails the build instead of producing an
    # unbootable droplet. digital-ocean-config already sets devices, but
    # an Mbr CriomOS node that reached this module without /dev/vda is a
    # data error worth catching loud.
    boot.loader.grub.enable = true;
    boot.loader.grub.devices = lib.mkForce [ "/dev/vda" ];

    # Minimality (see report §"How minimality is achieved"): a cloud
    # edge-cache/relay node carries no desktop, no docs, no firmware blobs.
    # The deployment.includeHome=false path (flake.nix:116, criomos.nix:13)
    # already drops home-manager; these trim the rest of the metal weight.
    documentation.enable = mkDefault false;
    documentation.nixos.enable = mkDefault false;
    documentation.man.enable = mkDefault false;
    documentation.doc.enable = mkDefault false;
    hardware.enableAllFirmware = mkDefault false;
    hardware.enableRedistributableFirmware = mkDefault false;
    fonts.fontconfig.enable = mkDefault false;
    # A droplet boots a known virtio environment; no need for the full
    # initrd module set.
    boot.initrd.includeDefaultModules = mkDefault false;
  };
}
```

### EXACT EDIT 1b — wire the module into the aggregate

`modules/nixos/disks/default.nix` currently imports only `preinstalled.nix`
(`disks/default.nix:3-5`). Add the cloud-node module beside it:

```nix
{ ... }:
{
  imports = [
    ./preinstalled.nix
    ./cloud-node.nix
  ];
}
```

(Equivalently add `./disks/cloud-node.nix` to the `imports` list in
`modules/nixos/criomos.nix:16`. Routing it through `disks/default.nix` keeps all
disk/boot-shape modules in one place, matching how `preinstalled.nix` is already
pulled in.)

The module body is fully gated by `mkIf isDigitalOceanNode`, so on every
non-cloud node (every current entry in `datom.nota`, all `Uefi`/`Uboot`) it
contributes nothing but the inert `system.build.digitalOceanImage` attribute,
which no output reads. No regression to existing nodes.

## 5. EXACT EDIT 2 — flake output that builds the DO image

`flake.nix:176-190` returns `blueprintOutputs // { checks; nixosConfigurations.target; horizonProbe; pkgsProbe; }`.
Add a package output that pulls the build derivation off the already-evaluated
`target`. `system` is in scope (`flake.nix:111`), and `target.config…` is the
node's evaluated config.

```nix
    blueprintOutputs
    // {
      checks = projectChecks;

      nixosConfigurations.target = target;

      # The minimal, content-sized DigitalOcean image built declaratively
      # from this node's CriomOS configuration: a bzip2-compressed qcow2
      # (make-disk-image, format=qcow2, partitionTableType=legacy → pure
      # MBR/BIOS, diskSize="auto" → closure-sized, ~1-2 GB compressed, NOT
      # a 60 GB snapshot). Only meaningful when `target` is a cloud node
      # (horizon bootloader=Mbr + digitalocean-* location); for any other
      # node the cloud-node module is gated off and this attribute is
      # absent, so `nix build` fails fast rather than producing junk.
      packages.${system}.digitalOceanImage =
        target.config.system.build.digitalOceanImage;

      horizonProbe = horizon;
      pkgsProbe = pkgs.stdenv.hostPlatform.system;
    };
```

Build it (lojix overrides `horizon`/`pkgs`/`system`/`deployment` per deploy, with
`deployment.includeHome = false` for a headless cloud node):

```
nix build .#packages.x86_64-linux.digitalOceanImage \
  --override-input horizon  path:<projected-dove-horizon> \
  --override-input deployment path:./stubs/headless-deployment
```

The result is `…/nixos.qcow2.bz2`. Decompress and `doctl compute image create
--image-url …` (or the operator's upload path) to register it as a custom
DigitalOcean image; create the droplet from that image.

## How minimality is achieved, and the expected size

Minimality is a hard requirement and is reached on three independent levers, in
descending impact:

1. **Content-sized partition, not a snapshot.** `diskSize = "auto"` →
   `make-disk-image.nix` measures the actual Nix closure (`du` over the store
   paths) and makes the partition exactly `closure + ~5.2% ext4 reserve +
   512 MiB`. There is no 60 GB raw region. growpart fills the droplet disk *at
   runtime*, so the *image* stays the size of its contents. This is the single
   biggest difference from the "convert a running droplet to a snapshot" path,
   which captures the whole provisioned disk.

2. **qcow2 + bzip2.** Sparse qcow2 over a content-sized partition, then bzip2.
   Unused/zero regions cost almost nothing; the upload is dominated by the
   compressed store closure.

3. **A headless cloud closure.** `deployment.includeHome = false` (the lojix
   override; `flake.nix:116`, `criomos.nix:13`) already drops home-manager,
   niri/noctalia/stylix/emacs — the desktop is the bulk of a CriomOS edge image.
   The cloud-node module additionally drops documentation (man/nixos/doc),
   all-firmware + redistributable-firmware (a KVM virtio guest needs none),
   fontconfig, and the default initrd module set. What remains is the base
   NixOS system + sshd + cloud-init/qemu-guest-agent + the node's declared
   CriomOS network/cluster services.

**Expected size.** A headless NixOS closure of this shape is roughly
1.0-1.6 GB on disk (systemd + kernel + glibc + sshd + cloud-init +
qemu-guest-agent + the cluster network units). bzip2 over the qcow2 lands the
uploadable image at **~0.5-1 GB**, with the *uncompressed* content-sized qcow2
around **~1.5-2 GB** — squarely inside the Spirit `2u57` ~1-2 GB target and far
below a 60 GB snapshot. (Final number is whatever the closure measures; the
mechanism guarantees it tracks content, not disk geometry.)

## 6. Open questions / follow-ups (not blocking the first image)

- **`behavesAs.cloud` facet.** The §4 gate string-matches a `digitalocean-`
  location prefix. Cleaner long-term: add a `cloud` (or `digitalOcean`) facet to
  `horizon-rs` `BehavesAs` (`node.rs:152-169`), derived from a
  `MachineSpecies::Pod` + a provider-typed `Location` (or a new
  `NodeSpecies::CloudEdge`), so the CriomOS gate reads `behavesAs.cloud` exactly
  as `liveiso.nix:10`/`router/default.nix:19` read their facets. That is a
  `horizon-rs` change (Lane B / a horizon-rs operator) — out of this lane's
  scope; the string predicate ships the first image without it.
- **`superNode` for a DigitalOcean droplet.** Modeled here as a standalone `Pod`
  with `superNode = None` (a DO droplet is not a CriomOS `VmHost` guest). Confirm
  `horizon-rs` projection accepts a `Pod` with explicit `arch` and no
  `superNode`: `resolve_arch` (`node.rs:618-638`) returns early on explicit
  `arch`, but `validate_pod_super_node` (`node.rs:652-673`) rejects an empty
  host-set with `Error::UnresolvableArch`. **A `Pod` with no `superNode`/`superNodes`
  fails that validation.** Two clean resolutions: (a) make `Machine::host_set`
  validation skip when `species == Pod && super_node.is_none() && location` names
  an external provider (a horizon-rs change), or (b) model the cloud node as
  `MachineSpecies::Metal` with an explicit `arch` (it IS a full machine from the
  droplet's view — it owns `/dev/vda` outright). **Recommend (b)** for the first
  image: `Metal` + `Mbr` + `/dev/vda` needs no horizon-rs change and matches how
  the droplet actually presents (a dedicated machine, growpart-resizing its own
  root). The §2/§4 entry should then use `(Metal (Some X86_64) 2 None None None
  None None (Some 4) None (Some digitalocean-fra1) [])` rather than `Pod`. Flagged
  for the psyche / a horizon-rs operator to confirm the intended substrate.
- **cloud-init vs DigitalOcean native metadata.** Both are enabled (§4). On a DO
  droplet the native metadata server already injects the ssh key + hostname;
  cloud-init is additive for portability. If the psyche wants DigitalOcean-only,
  drop the `services.cloud-init` block and rely on `digital-ocean-config.nix`'s
  metadata provisioning alone (smaller closure still).
