;; Lane B — the cluster-data node declaration for a DigitalOcean cloud node.
;; Spirit 2u57. Report cloud-designer/74, file 2.

# Lane B — DigitalOcean cloud node: the cluster-data declaration

## What this delivers

The EXACT positional NOTA node entry to add to
`/git/github.com/LiGoldragon/goldragon/datom.nota`, declaring a
DigitalOcean cloud node, every field mapped against
`horizon-rs/lib/src/proposal.rs` `NodeProposal` (`:45`). Plus one
load-bearing schema finding that changes the obvious answer:
**a cloud node must be `MachineSpecies::Metal`, NOT `Pod`** — the Pod
path fails projection for a host-less provider VM.

## The schema, confirmed field-by-field

### `NodeProposal` positional order (`proposal.rs:45-101`)

The decoder reads these positions in declared order. The serde
`#[serde(default)]` tail (`size`, `trust`, then everything from
`link_local_ips` down) may be omitted only from the END; every node in
`datom.nota` writes them all out explicitly, so this entry does too.

| # | Field | Type | `proposal.rs` |
|---|---|---|---|
| 0 | `species` | `NodeSpecies` | `:46` |
| 1 | `size` | `Magnitude` (dflt `Zero`) | `:47-48` |
| 2 | `trust` | `Magnitude` (dflt `Min`) | `:49-50` |
| 3 | `machine` | `Machine` | `:51` |
| 4 | `io` | `Io` | `:52` |
| 5 | `pub_keys` | `NodePubKeys` | `:53` |
| 6 | `link_local_ips` | `Vec<LinkLocalIp>` | `:54-55` |
| 7 | `node_ip` | `Option<NodeIp>` | `:56-57` |
| 8 | `wireguard_pub_key` | `Option<WireguardPubKey>` | `:58-59` |
| 9 | `nordvpn` | `bool` | `:60-61` |
| 10 | `wifi_cert` | `bool` | `:62-63` |
| 11 | `wireguard_untrusted_proxies` | `Vec<WireguardProxy>` | `:64-65` |
| 12 | `wants_printing` | `bool` | `:69-70` |
| 13 | `wants_hw_video_accel` | `bool` | `:76-77` |
| 14 | `router_interfaces` | `Option<RouterInterfaces>` | `:82-83` |
| 15 | `online` | `Option<bool>` | `:92-93` |
| 16 | `services` | `Vec<NodeService>` | `:99-100` |

### `Machine` positional order (`machine.rs:14-67`)

`species, arch, cores, model, mother_board, super_node, super_user,
chip_gen, ram_gb, disk_gb, location, super_nodes` — 12 fields. Confirmed
against the live `vm-testing` Pod entry (`datom.nota:159`, 12 elements).

### `Io` positional order (`io.rs:98-107`)

`keyboard, bootloader, disks, swap_devices, compressed_swap` — 5 fields;
`compressed_swap` is droppable from the tail (`io.rs:113` accepts 4..=5).
`disks` is a curly map `MountPath -> Disk`; each `Disk` is
`(device fs_type [options])` (`io.rs:72-79`, `:74` device, `:76` fs_type,
`:78` options).

### `NodePubKeys` positional order (`proposal.rs:510-518`)

`ssh, nix, yggdrasil` — ssh required; `nix` and `yggdrasil` are
`Option`, written `None` here. `SshPubKey` validation (`pub_key.rs:59-69`)
is the only gate that matters for the placeholder: it rejects empty and
requires every char be `[A-Za-z0-9+/=]` (`pub_key.rs:31-38`) — NO length
check (unlike `NixPubKey`/`WireguardPubKey`). So the placeholder must be a
bare base64-charset token: no spaces, no `-`, no `_`. `.line()` prepends
`ssh-ed25519 ` at projection (`pub_key.rs:71-73`), so the stored value is
the raw blob exactly like every existing node (`AAAAC3Nza...`).

### `Bootloader::Mbr` exists (`species.rs:98-102`)

`enum Bootloader { Uefi, Mbr, Uboot }`. `Mbr` is `:100`. balboa uses
`Uboot` (`datom.nota:11`), every x86 metal node uses `Uefi`; this cloud
node is the FIRST `Mbr` in the cluster — matching report 73's finding
that DigitalOcean is BIOS/GRUB-only and CriomOS gates
`boot.loader.grub.enable` on `bootloader == Mbr`
(`73-criomos-do-deploy/3-deploy-minimal.md:90`).

## THE BLOCKER: `Pod` is wrong for a cloud node

The intuitive choice is `MachineSpecies::Pod` (it IS a VM, and
`BehavesAs::derive` sets `virtual_machine = matches!(species, Pod)` —
`node.rs:212`). It does not work. Projection runs, for every Pod
unconditionally (`horizon.rs:57`):

```
proposal.validate_pod_super_node(name, &self.nodes)?;   // node.rs:652
```

which requires (`node.rs:660-671`) a NON-EMPTY host-set
(`{super_node} ∪ super_nodes`) whose EVERY member already exists as a
node in the cluster. A DigitalOcean droplet has no in-cluster host:

- `super_node None` → empty host-set → `Error::UnresolvableArch`
  (`node.rs:665`).
- `super_node (Some <fake>)` → `Error::MissingSuperNode` (`node.rs:669`).

There is no host-less Pod. `Pod` models a test-VM guest pinned to a
cluster VM-host (that is exactly what `vm-testing` is —
`super_node (Some prometheus)`, `datom.nota:159`). It is the wrong
substrate for a provider VM we don't host.

### Resolution: `MachineSpecies::Metal` with explicit arch

`Metal` (`species.rs:47`) skips both Pod validators (`node.rs:657`,
`:690` early-return on non-Pod) and `resolve_arch` short-circuits on the
explicit `arch` (`node.rs:623`). The DO virtio VM presents as a normal
x86_64 machine to the guest OS, so `Metal (Some X86_64) ...` is honest at
the level the projection cares about. The deploy path keys on
`io.bootloader = Mbr` for the GRUB-on-`/dev/vda` decision
(`73/3-deploy-minimal.md:90,94`), NOT on `virtual_machine`, so choosing
`Metal` over `Pod` does not break the cloud-boot wiring — it only flips
`bare_metal`/`virtual_machine` in `BehavesAs` (`node.rs:211-213`), which
the DO deploy does not read.

This is the cross-lane decision Lane A (the CriomOS image/species work)
must ratify: either (a) cloud nodes ride `Metal` (this report's working
answer, needs no schema change), or (b) horizon-rs grows a host-less
cloud substrate — a new `MachineSpecies::Cloud` or a `Pod` whose
host-set is allowed empty — gated behind a fresh `NodeSpecies::CloudNode`
(Spirit `ad53`). (b) is the cleaner long-term shape but is a schema
change; (a) ships today. I recommend (a) now, (b) tracked.

## NodeSpecies choice: `Edge`

No `CloudNode` species exists yet (`species.rs:13-31`). Among existing
variants, `Edge` (`:18`) is the closest minimal-server fit that the
deploy path tolerates, BUT note `Edge` derives `has_video_output = true`
and `edge = true` (`node.rs:207,410`), pulling desktop/edge facets a
headless cloud server does not want. The genuinely minimal choice is
`TestVm` (`:30`) — it derives ONLY `test_vm` + `virtual_machine` and NO
edge/center/router facets (`node.rs:214-231`) — but `TestVm` is
semantically a throwaway test guest AND forces the `Pod` substrate per
its doc (`species.rs:24-29`), colliding with the blocker above.

For minimality without the Pod collision I use **`Edge`** as the
provisional species and flag the species gap as the primary open
question for Lane A. A purpose-built `NodeSpecies::CloudNode` (deriving a
lean headless-server profile: no video output, no edge desktop, no
router) is the right end state and is exactly what Spirit `ad53`
anticipates.

## The entry — copy-pasteable

Node name `doris` (DigitalOcean + a real name; fresh, unused in
`datom.nota`). Add it inside the nodes map (the first `{...}`,
`datom.nota:5-180`), e.g. right after `balboa` (alphabetical-ish, and
balboa is the other non-Uefi node). Indentation matches the file's
4-space node indent.

```nota
    doris (Edge
      Min
      Max
      (Metal (Some X86_64) 1 (Some [DigitalOcean Droplet]) None None None None (Some 2) (Some 25) (Some digitalocean-nyc1) [])
      (Qwerty
        Mbr
        {
          / (/dev/vda Ext4 [])
        }
        [])
      (AAAAC3NzaC1lZDI1NTE5AAAAIArEPLACEHOLDERdorisCloudNodeSshKeyReplaceMe00000000 None None)
      []
      None
      None
      False
      False
      []
      False
      False
      None
      None
      [(TailnetClient)])
```

## Each field explained against `proposal.rs`

- **`doris`** — the `NodeName` map key (`proposal.rs:29`,
  `BTreeMap<NodeName, NodeProposal>`). Fresh; collides with nothing in
  `datom.nota:5-180`.

- **position 0 `Edge`** — `species: NodeSpecies` (`:46`). Provisional;
  see "NodeSpecies choice" — wants a real `CloudNode` variant.

- **position 1 `Min`** — `size: Magnitude` (`:47`). A 1-vCPU
  small droplet. `Min` (not `Zero`) keeps `enable_network_manager`'s
  `sized_at_least.min` gate live (`node.rs:408-409`) and lets the node be
  a dispatcher target if ever trusted; `Zero` would be the bottom rung.
  `Min` is the honest small-cloud size.

- **position 2 `Max`** — `trust: Magnitude` (`:49`). The cluster owns
  this droplet, so it is fully trusted, matching every other goldragon
  node (`datom.nota:99,127`, etc.). Trust `Zero` would DROP the node from
  the horizon entirely (`horizon.rs:48-51`); `Max` keeps it projected and
  admin-reachable.

- **position 3 `(Metal (Some X86_64) 1 (Some [DigitalOcean Droplet]) None None None None (Some 2) (Some 25) (Some digitalocean-nyc1) [])`**
  — `machine: Machine` (`:51`), 12 positional fields (`machine.rs:14-67`):
  - `Metal` — `species: MachineSpecies` (`machine.rs:15`). NOT `Pod`; see
    the blocker. Skips the host-set validators.
  - `(Some X86_64)` — `arch: Option<Arch>` (`machine.rs:16`). Explicit so
    `resolve_arch` short-circuits (`node.rs:623`) with no super-node to
    inherit from. DO standard droplets are x86_64.
  - `1` — `cores: u32` (`machine.rs:17`). A 1-vCPU droplet; bump to match
    the chosen plan.
  - `(Some [DigitalOcean Droplet])` — `model: Option<ModelName>`
    (`machine.rs:18`). Free string, bracket-delimited because it contains
    a space (NOTA bare-atom rule). Not a `KnownModel` (`species.rs:150`),
    so it drives no `ComputerIs`/`model_is_thinkpad` branch
    (`node.rs:432-437`) — correct; a cloud VM needs no model-specific
    config.
  - `None` — `mother_board: Option<MotherBoard>` (`machine.rs:19`). The
    only variant is `Ondyfaind` (`species.rs:138`); a droplet has none.
  - `None` — `super_node: Option<NodeName>` (`machine.rs:21`). Pod-only;
    `Metal` ignores it. None.
  - `None` — `super_user: Option<UserName>` (`machine.rs:23`). Pod-only.
    None.
  - `None` — `chip_gen: Option<u32>` (`machine.rs:32`). Intel iGPU media
    generation; a headless cloud VM has no iGPU and wants no media stack.
  - `(Some 2)` — `ram_gb: Option<u32>` (`machine.rs:38`). 2 GiB, a
    typical small droplet. Adjust to plan.
  - `(Some 25)` — `disk_gb: Option<u32>` (`machine.rs:46`). 25 GiB, the
    DO small-droplet root disk. Cluster-authored; not derivable. (For a
    `Metal` node this is informational — the disk layout comes from `Io`;
    growpart resizes the live root to the real provisioned size at boot,
    report 73.)
  - `(Some digitalocean-nyc1)` — `location: Option<Location>`
    (`machine.rs:54`). A free site label (`machine.rs:88-95`, transparent
    String). Bare atom: no whitespace, `-` stays bare. Set to the real
    DO region/datacenter.
  - `[]` — `super_nodes: Vec<NodeName>` (`machine.rs:66`). Pod-only image
    co-hosts; empty for a `Metal` node.

- **position 4 `(Qwerty Mbr { / (/dev/vda Ext4 []) } [])`** —
  `io: Io` (`:52`), 5 positional fields (`io.rs:98-107`):
  - `Qwerty` — `keyboard: Keyboard` (`io.rs:13`). A headless server has
    no human at a keyboard; `Qwerty` is the neutral default (only
    `use_colemak` reads it — `node.rs:524` — irrelevant headless).
  - `Mbr` — `bootloader: Bootloader` (`io.rs:14`, variant
    `species.rs:100`). THE load-bearing field: DigitalOcean is
    BIOS/GRUB-only, CriomOS gates `boot.loader.grub.enable` on
    `bootloader == Mbr` (report 73 `3-deploy-minimal.md:90`). First `Mbr`
    in the cluster.
  - `{ / (/dev/vda Ext4 []) }` — `disks: BTreeMap<MountPath, Disk>`
    (`io.rs:15`). A SINGLE mount: `/` only. NO separate `/boot` — BIOS/
    GRUB embeds its core image in the MBR gap and reads `/boot/grub` from
    the root filesystem, so no ESP/`/boot` partition is needed (contrast
    every Uefi node, which carries a `Vfat` `/boot` — `datom.nota:36,69`).
    The `Disk` is `(/dev/vda Ext4 [])` (`io.rs:72-79`): device
    `/dev/vda` (the DO virtio root disk), `fs_type` `Ext4`
    (`io.rs:177`), empty `options`. Bare atoms throughout — `/` and
    `/dev/vda` carry only `/`, which stays bare (NOTA rule).
  - `[]` — `swap_devices: Vec<SwapDevice>` (`io.rs:16`). None; the
    droplet runs swapless or via zram if `compressed_swap` is later set.
  - `[]` — `compressed_swap` is the droppable 5th field; written as the
    absent-tail. NOTE: an empty list `[]` at position 4 decodes via
    `Option::<CompressedSwap>::from_nota_block` — to be unambiguous this
    is the standard "no compressed swap" form. (Matches the
    droppable-tail handling at `io.rs:124-127`.) If a tool round-trips
    this, confirm the encoder emits `None` vs `[]` here; balboa writes
    its Io with no 5th element at all (`datom.nota:13-15` closes after
    the swap-devices `[]`), which is the safest form — see open question.

- **position 5 `(AAAAC3Nza...PLACEHOLDER... None None)`** —
  `pub_keys: NodePubKeys` (`:53`), 3 fields (`proposal.rs:510-518`):
  - the long base64 token — `ssh: SshPubKey` (`:513`). PLACEHOLDER. Must
    be base64-charset-only and non-empty (`pub_key.rs:59-69`,
    `:31-38`); replace with the droplet's real ed25519 host pubkey blob
    (the `AAAAC3NzaC1lZDI1NTE5AAAA...` form, NO `ssh-ed25519 ` prefix —
    `.line()` adds it, `pub_key.rs:71-73`). The placeholder shown is
    pure `[A-Za-z0-9]`, so it PARSES (lets the cluster project for
    testing) but is obviously not a real key.
  - `None` — `nix: Option<NixPubKey>` (`:515`). No Nix signing key; the
    cloud node is not a binary-cache/builder. (If it ever serves a cache,
    add the 44-char key here.)
  - `None` — `yggdrasil: Option<YggPubKeyEntry>` (`:517`). Not on the
    Yggdrasil mesh.

- **position 6 `[]`** — `link_local_ips: Vec<LinkLocalIp>` (`:54`). None;
  cloud-init injects the real per-instance network at boot (report 73), so
  no static link-local addressing is declared.

- **position 7 `None`** — `node_ip: Option<NodeIp>` (`:56`). None — the
  droplet's public IP is assigned by DigitalOcean per-instance and
  injected by cloud-init, not cluster-declared. (Most goldragon nodes set
  a `5::N/128` here — `datom.nota:49,88` — that is the internal mesh
  address; a cloud node joins via Tailnet instead, position 16.)

- **position 8 `None`** — `wireguard_pub_key: Option<WireguardPubKey>`
  (`:58`). No WireGuard; the node joins the cluster over Tailnet.

- **position 9 `False`** — `nordvpn: bool` (`:60`). No NordVPN proxy.

- **position 10 `False`** — `wifi_cert: bool` (`:62`). No WiFi; a cloud
  VM is wired-only.

- **position 11 `[]`** — `wireguard_untrusted_proxies:
  Vec<WireguardProxy>` (`:64`). None.

- **position 12 `False`** — `wants_printing: bool` (`:69`). Headless; no
  printer bundle.

- **position 13 `False`** — `wants_hw_video_accel: bool` (`:76`).
  Headless; no GPU video decode.

- **position 14 `None`** — `router_interfaces: Option<RouterInterfaces>`
  (`:82`). Not a router.

- **position 15 `None`** — `online: Option<bool>` (`:92`). `None` =
  default-online (`node.rs:397`), so the node participates normally.
  (Set `(Some False)` only to administratively park it.)

- **position 16 `[(TailnetClient)]`** — `services: Vec<NodeService>`
  (`:99`). One service: `TailnetClient` (`proposal.rs:108`,
  encodes `(TailnetClient)` — `:281-283`). This is how a cloud node with
  no static mesh IP joins the cluster: it dials the Tailnet controller
  (ouranos holds `TailnetController` — `datom.nota:58`). The minimal,
  correct service set for a reachable cloud node. Leave `[]` if the node
  should join NOTHING (truly isolated), but then it is unreachable on the
  cluster overlay.

## Minimality scorecard

Every "more" field is off: `Zero`-equivalent video/print/router/wifi/
wireguard/nordvpn flags all `False`/`None`, no Nix/Ygg keys, no swap, a
single `/` partition, no `/boot`, one `TailnetClient` service. The only
non-trivial machine facts are the honest cloud sizing (`1` core,
`Some 2` GiB RAM, `Some 25` GiB disk, the DO location). This is the
leanest node entry in `datom.nota` after balboa.

## Open questions for Lane A / the psyche

1. **`Metal` vs a real cloud substrate.** This entry uses `Metal` because
   `Pod` fails `validate_pod_super_node` (`node.rs:652`) for a host-less
   provider VM. Does Lane A want (a) cloud nodes on `Metal` (ships now,
   no schema change), or (b) a new host-less substrate — `MachineSpecies
   ::Cloud` or empty-host-set `Pod` — plus a `NodeSpecies::CloudNode`
   (Spirit `ad53`)? I recommend (a) now, (b) tracked.

2. **NodeSpecies gap.** No `CloudNode` exists (`species.rs:13-31`). I used
   `Edge` provisionally, which over-derives `has_video_output`/`edge`
   facets (`node.rs:207,410`) a headless server doesn't want. `TestVm` is
   leaner but forces `Pod` and means "throwaway." A purpose-built
   `CloudNode` deriving a lean headless-server profile is the right end
   state — Lane A's call.

3. **`/dev/vda` whole-disk vs `/dev/vda1` partition.** The prompt says
   "single disk on /dev/vda"; report 73 (`3-deploy-minimal.md:102`) says
   `/dev/vda1`. GRUB-BIOS installs to the whole disk `/dev/vda`
   (`boot.loader.grub.devices`), but the root FILESYSTEM mount is
   normally the partition `/dev/vda1`. The entry above uses `/dev/vda`
   per the prompt; if the disko/growpart layout partitions the disk, this
   should be `/dev/vda1` for the `/` mount (with GRUB still targeting
   `/dev/vda`). Confirm against the final image's partition table.

4. **`Io` 5th-field form.** balboa closes its `Io` with no
   `compressed_swap` element at all (`datom.nota:13-15`), relying on the
   4-field decode (`io.rs:113`). The entry above mirrors that — it ends
   after the swap-devices `[]`, no 5th element. (The draft prose above
   mentions `[]` at position 4; the actual entry omits it, matching
   balboa — the safest round-trip form. Verify the encoder agrees.)

## Verification done

- `Bootloader::Mbr` exists: `species.rs:100`.
- `MachineSpecies` has only `Metal`, `Pod`: `species.rs:45-48`.
- Pod projection requires an existing in-cluster host-set:
  `horizon.rs:57` → `node.rs:652-673`.
- `SshPubKey` accepts any non-empty `[A-Za-z0-9+/=]`: `pub_key.rs:59-69`,
  `:31-38`.
- Field orders cross-checked against the live `vm-testing` Pod
  (`datom.nota:156-179`) and balboa (`:6-27`).
