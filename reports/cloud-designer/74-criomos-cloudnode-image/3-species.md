# 74/3 — horizon-rs species/projection for the cloud-node image type (Lane C)

*cloud-designer report 74 · 2026-06-20 · Spirit 2u57 (minimal declarative
CriomOS cloud-node image). Every claim cites `file:line` in
`/git/github.com/LiGoldragon/horizon-rs` and `/git/github.com/LiGoldragon/CriomOS`.*

## Decision

**Add a new `NodeSpecies::CloudNode` variant — with `TypeIs.cloud_node`
and `BehavesAs.cloud_node`, mirroring `TestVm` exactly.** Do NOT reuse
`TestVm`. The "new image type" is BOTH a species concern (the minimal
profile is derived from the species, the same mechanism `TestVm` uses)
AND an image-format concern (Lane A) — but the format module needs a
stable derived facet to gate on, and that facet is `behaves_as.cloud_node`.
`Bootloader::Mbr` alone cannot carry it, and reusing `test_vm` actively
mis-fires.

This confirms the prior same-lane decision in report 65 §1
(`reports/cloud-designer/65-cloud-node-image-home.md:7-12`), and supplies
the exact edits.

## Why not reuse `TestVm` + `Bootloader::Mbr` + Lane-A image output

Three independent reasons, each fatal on its own.

### 1. `behaves_as.test_vm` fires the HOST microVM emitter — a cloud node must not

`test_vm` is not an inert lean-flag; CriomOS reads it on BOTH the guest
and the host. `modules/nixos/test-vm-host.nix` discovers guests by
`(node.behavesAs.testVm or false)` and emits a real KVM microVM + tap +
guest-IP hosts entry + non-autostart unit for every projected ex-node
carrying it (`test-vm-host.nix:163,167,176`). A DO droplet is not a
microVM we launch on one of our hosts; tagging it `test_vm` would make
its co-resident nodes try to host it. The guest-side gate
(`test-vm-guest.nix:45`, `mkIf (behavesAs.testVm or false)`) and the
host-side emitter are the same flag — you cannot borrow the leanness
without the host emission. (Both wired in `criomos.nix:44,48`.)

### 2. `TestVm` is a `Pod` guest with a mandatory `super_node`; a droplet has none

`TestVm`'s substrate is `MachineSpecies::Pod` by design
(`species.rs:27`), and `BehavesAs::derive` sets `virtual_machine` from
`MachineSpecies::Pod` (`node.rs:212`). A `Pod` is validated to name a
host-set whose every member exists — `validate_pod_super_node` rejects a
`Pod` with an empty host-set as `Error::UnresolvableArch`
(`node.rs:652-666`), and arch resolution itself defers a `Pod`'s arch to
its `super_node` (`node.rs:618-638`). A DO cloud node is a standalone
machine: it has no host in our cluster, resolves its own arch, and its
`machine.species` is naturally `Metal` (from CriomOS's view it is the bare
machine it boots on, not a guest of one of our hosts). So it cannot be a
`Pod`, which means it cannot be `TestVm` — `TestVm`'s whole identity is
"a Pod guest launched on `Machine::super_node`" (`species.rs:23-29`).

A `Metal` cloud node also derives `iso = !virtual_machine && io_disks_empty`
(`node.rs:213`); with disks declared in the cluster data (the cloud node
HAS a root disk, `/dev/vda`) `io_disks_empty` is false, so `iso` is
correctly false. Good — but this only works because the cloud node is its
own species with declared disks, not a disk-less marker.

### 3. The image-format output (Lane A) needs a derived facet, not an `io` field

`Bootloader::Mbr` already drives the GRUB-vs-systemd-boot choice directly
off `horizon.node.io.bootloader` in `disks/preinstalled.nix:46-50`
(`grub.enable = bootloader == "Mbr"`). That correctly handles the
BIOS/GRUB requirement (report 73/2) **for any species** — it is purely an
`io` concern and needs no species. BUT `bootloader` is a single field on
`Io` (`io.rs:14`); it cannot select a whole image-FORMAT module
(cloud-image build target + cloud-init + growpart), and it does not
distinguish a cloud node from, say, a future MBR bare-metal box.

CriomOS today has zero cloud-init / growpart / digitalOcean modules
(grep across `CriomOS/` returns nothing). Lane A will add a cloud-image
module (the fourth member of the `disks/` family alongside
`preinstalled.nix`, `pod.nix`, `liveiso.nix` — report 65 §1). That module
must be `mkIf (behavesAs.cloudNode or false)`, exactly as
`test-vm-guest.nix:45` gates on `behavesAs.testVm` and `liveiso.nix:31`
reads `behavesAs.bareMetal`. The leanness ALSO comes from the species
deriving none of the heavy `type_is` flags — identical to how `TestVm`
leaves edge/center/router/large_ai false purely by setting none of them
(`node.rs:214-220`, asserted in
`horizon-rs/lib/tests/horizon.rs:520-528`). That is the ~1-2GB content-size
mechanism: no desktop tree (`metal/default.nix:295` `mkIf behavesAs.bareMetal`
— false), no edge tree (`edge/default.nix:30` — false), no LLM/center/router
weight, plus the cloud-image module can force documentation off the way
`test-vm-guest.nix:46-52` does.

### Conclusion on the framing question

The "new image type" is **not purely an image-format concern**. The
minimal profile (which packages, which module trees) is selected by the
species through `type_is`/`behaves_as` — the same lever `TestVm` pulls.
The format (qcow2/raw, cloud-init, growpart) is selected by a CriomOS
module gated on the species-derived `behaves_as.cloud_node` facet. Both
sit on the species. `Bootloader::Mbr` covers only the bootloader choice,
not the profile and not the format gate. Hence: **new species.**

## The minimal-surface recommendation

The new variant is itself the minimal surface: it is FOUR small,
mechanical edits in horizon-rs (mirroring `TestVm`), then ONE `mkIf`
gate + the cloud-image module in CriomOS (Lane A), then ONE node block
in `goldragon/datom.nota` (the per-node config the directive mandates
lives in cluster data). No daemon/wire change — the create path already
takes `ImageName` (report 73/1 §"Why Lane 2/3 need no daemon schema
change"). The variant derives NO heavy facets, so it touches no existing
node's projection (byte-identical for every current node — adding an enum
variant changes nothing for nodes that don't name it).

`behaves_as.cloud_node` and `behaves_as.test_vm` are siblings: both are
lean-profile gates orthogonal to the role facets, exactly as the doc-comment
on `test_vm` describes (`node.rs:164-168`). `cloud_node` does NOT imply
`virtual_machine` (the cloud node is `Metal` from CriomOS's view), which
is the clean separation from `test_vm`.

## EXACT horizon-rs edits

Four edits, all in `/git/github.com/LiGoldragon/horizon-rs/lib/src/`.
Copy-pasteable; each mirrors the existing `TestVm` line.

### Edit 1 — `species.rs`: add the variant after `TestVm` (`species.rs:30`)

Replace the tail of the `NodeSpecies` enum:

```rust
    /// On-demand test virtual machine — a first-class cluster role,
    /// distinct from `EdgeTesting` (a next-gen edge desktop). A
    /// `TestVm` node derives a deliberately minimal profile: it is a
    /// virtual machine (its substrate is `MachineSpecies::Pod`) but is
    /// NOT an edge, center, or router node. The host the VM runs on is
    /// `Machine::super_node`; the guest is launched to run a test and
    /// stopped after.
    TestVm,
}
```

with:

```rust
    /// On-demand test virtual machine — a first-class cluster role,
    /// distinct from `EdgeTesting` (a next-gen edge desktop). A
    /// `TestVm` node derives a deliberately minimal profile: it is a
    /// virtual machine (its substrate is `MachineSpecies::Pod`) but is
    /// NOT an edge, center, or router node. The host the VM runs on is
    /// `Machine::super_node`; the guest is launched to run a test and
    /// stopped after.
    TestVm,
    /// A cloud provider node (DigitalOcean, etc.) — a first-class
    /// cluster role whose CriomOS config is rendered into a NEW minimal,
    /// content-sized cloud image built declaratively from the projection
    /// (NOT a snapshot of a converted droplet). Like `TestVm` it derives
    /// a deliberately lean profile — it sets `cloud_node` and NONE of the
    /// heavy `type_is` role flags, so edge/center/router/large_ai all stay
    /// false and the desktop/server/LLM module trees never derive onto it.
    /// Unlike `TestVm` it is NOT a `Pod` guest: it is the bare machine it
    /// boots on (`MachineSpecies::Metal`), has no `super_node`, resolves
    /// its own arch, and so derives `virtual_machine` false. The cloud
    /// image's bootloader follows `io.bootloader` (`Bootloader::Mbr` for
    /// DigitalOcean BIOS/GRUB); cloud-init network/ssh injection and
    /// growpart are emitted by the CriomOS cloud-image module gated on
    /// `behaves_as.cloud_node`.
    CloudNode,
}
```

### Edit 2 — `node.rs`: add `cloud_node` to `TypeIs` (`node.rs:183`)

Replace:

```rust
    pub router_testing: bool,
    pub test_vm: bool,
}
```

with:

```rust
    pub router_testing: bool,
    pub test_vm: bool,
    pub cloud_node: bool,
}
```

### Edit 3 — `node.rs`: map the variant in `TypeIs::from_species` (`node.rs:198`)

Replace:

```rust
            router_testing: matches!(s, NodeSpecies::RouterTesting),
            test_vm: matches!(s, NodeSpecies::TestVm),
        }
```

with:

```rust
            router_testing: matches!(s, NodeSpecies::RouterTesting),
            test_vm: matches!(s, NodeSpecies::TestVm),
            cloud_node: matches!(s, NodeSpecies::CloudNode),
        }
```

### Edit 4 — `node.rs`: add `cloud_node` to `BehavesAs` and derive it

4a. Add the field to the `BehavesAs` struct, after `test_vm`
(`node.rs:168`). Replace:

```rust
    /// The guest's own lean test-VM profile gate. True only for a
    /// `NodeSpecies::TestVm` node. CriomOS gates the guest's minimal
    /// config on this facet; it is orthogonal to `virtual_machine`
    /// (which flags "runs on a host" for the host's substrate wiring).
    pub test_vm: bool,
}
```

with:

```rust
    /// The guest's own lean test-VM profile gate. True only for a
    /// `NodeSpecies::TestVm` node. CriomOS gates the guest's minimal
    /// config on this facet; it is orthogonal to `virtual_machine`
    /// (which flags "runs on a host" for the host's substrate wiring).
    pub test_vm: bool,
    /// The cloud-node lean image-profile gate. True only for a
    /// `NodeSpecies::CloudNode` node. CriomOS gates the minimal
    /// cloud-image module (cloud-init + growpart + image-format build)
    /// on this facet. A sibling of `test_vm`: both are lean-profile
    /// gates orthogonal to the role facets. Unlike `test_vm` it does NOT
    /// imply `virtual_machine` — a cloud node is `Metal` from CriomOS's
    /// view, not a Pod guest of one of our hosts.
    pub cloud_node: bool,
}
```

4b. Derive it in `BehavesAs::derive`, after the `test_vm` binding
(`node.rs:220`) and in the struct literal (`node.rs:231`). Replace:

```rust
        let test_vm = type_is.test_vm;
        BehavesAs {
            center,
            router,
            edge,
            next_gen,
            low_power,
            bare_metal,
            virtual_machine,
            iso,
            large_ai,
            test_vm,
        }
```

with:

```rust
        let test_vm = type_is.test_vm;
        // A CloudNode derives the same lean shape as TestVm — it carries
        // `cloud_node` and nothing else, leaving edge/center/router/large_ai
        // false because `NodeSpecies::CloudNode` sets none of their
        // `type_is` flags. It is NOT a Pod, so `virtual_machine` is false
        // and (with declared disks) `iso` is false: it is the bare machine
        // it boots on.
        let cloud_node = type_is.cloud_node;
        BehavesAs {
            center,
            router,
            edge,
            next_gen,
            low_power,
            bare_metal,
            virtual_machine,
            iso,
            large_ai,
            test_vm,
            cloud_node,
        }
```

## Tests to extend (same file, mirror the `TestVm` test)

`horizon-rs/lib/tests/horizon.rs` has the `TestVm` projection test
(`:506-528`). Add a sibling `project_cloud_node_metal_derives_lean_profile`
test: a `Metal` node, `Bootloader::Mbr`, one `/dev/vda` disk, no
`super_node`, asserting `behaves_as.cloud_node`,
`!behaves_as.virtual_machine`, `!behaves_as.iso`, and all role facets
false. This is a new test, not an edit to an existing one — no existing
test asserts exhaustive `NodeSpecies` coverage, so the four edits above
compile and leave every current test green (the new `cloud_node: false`
field appears on every projected `BehavesAs`, but no existing test
constructs `BehavesAs` literals — they read fields off projections).

## What this leaves to the other lanes

- **Lane A (image format):** the CriomOS cloud-image module under
  `modules/nixos/disks/` gated `mkIf (behavesAs.cloudNode or false)` —
  cloud-init (per-instance network + ssh-key injection), growpart, and
  the declarative image-build output. It reads `io.bootloader == "Mbr"`
  through the existing `preinstalled.nix:46-50` GRUB path; the cloud
  module adds the GRUB `/dev/vda` device + cloud-init + growpart that
  `preinstalled.nix` does not set. Import it in `criomos.nix` next to
  `test-vm-guest.nix` (`criomos.nix:44`).
- **Lane B / cluster data:** the per-node DO config is one `CloudNode`
  block in `goldragon/datom.nota`, mirroring the `vm-testing (TestVm …)`
  block at `datom.nota:156-175` but with `Metal` substrate,
  `Bootloader::Mbr`, `(/dev/vda Ext4 [])` disk, and no `super_node`.

## Unverified / to confirm

- That `nota_next`'s derived `NotaDecode`/`NotaEncode` on `NodeSpecies`
  picks up the new variant automatically — it is `#[derive(NotaDecode,
  NotaEncode)]` (`species.rs:10-12`) on a plain unit-variant enum, so the
  macro should handle it as it does `TestVm`; confirm with a round-trip
  build (`cargo test -p horizon`).
- The exact CriomOS module name/shape for the cloud-image output is
  Lane A's call; this report only fixes the GATE (`behaves_as.cloud_node`)
  it must key on.
- `cloud_node` not implying `virtual_machine` assumes CriomOS models the
  droplet as `Metal`. If a later design prefers to model a droplet as a
  `Pod` of the cloud provider (it is not — we don't host it), that would
  change `virtual_machine`; current recommendation is `Metal`, matching
  "the bare machine it boots on."
