# 76 — CloudNode image: live DigitalOcean confirmation (`criomos-confirmed`)

cloud-designer, 2026-06-20. The closing witness for the CriomOS CloudNode
image arc (reports 72→75). The boot-fixed, content-sized image was deployed to
real DigitalOcean and confirmed reachable, then swept. This report also serves
as the live-deploy record the self-audit (75, finding #11/#39) flagged missing.

## The witness

```
DEPLOY WITNESS droplet_id=579047618 ipv4=209.97.148.182 region=nyc3 \
  image=233619676 deploy=criomos-confirmed result=OK
```

`deploy=criomos-confirmed` is the strongest of the harness's deploy levels: the
droplet reached `Running`, sshd accepted a connection, and ssh read the CriomOS
identity marker (`/etc/os-release` `ID=nixos`) off the live node. The full cycle:

```
image 233619676 → available (min_disk=7)
droplet 579047618 → Running, ipv4 209.97.148.182
ssh :22 → timed out → refused → connected   (the boot window; harness retries)
criomos-confirm marker matched: ID=nixos
deploy=criomos-confirmed
release deleted · DO image deleted (HTTP 204) · leftover droplets: 0
```

Post-run the account is clean: 0 droplets, 0 private images, image
`233619676` returns HTTP 404, the gh release `cloud-node-2026-06-20-v2` is gone.
The harness destroys on every exit path (Rust `Drop` guard + flake EXIT trap).

## What it confirms — the root-device fix

The prior cycles reported `deploy=running-only`: the droplet reached `Running`
but ssh :22 never opened. I first mis-diagnosed this as a networking gap and
band-aided DHCP-over-networkd into the module — it didn't help. Booting the
image in **local QEMU** showed the real cause: an initrd kernel panic,
**"Failed to mount /sysroot"** at ~2.5 s. The node never reached userspace, so
there was never a network or an sshd to reach.

Root cause: `make-disk-image` labels the root partition `nixos` and the upstream
`digital-ocean-config` mounts `/` from `/dev/disk/by-label/nixos` at `mkDefault`
priority — but CriomOS's `preinstalled.nix` derives `fileSystems."/".device`
from the node's `io.disks` at **normal** priority, so doris's `/dev/vda` won
the override and pointed the initrd at a bare disk with no filesystem.

Fix (goldragon `48060b0`): doris `io.disks` root device `/dev/vda` →
`/dev/disk/by-label/nixos`. After the fix the QEMU boot is clean — `/sysroot`
mounts, "Reached target Basic System", network online, "OpenSSH Server Socket
listening" — and now, live on DigitalOcean, `criomos-confirmed`.

The lesson, recorded against my own process: a local QEMU boot is a 2-minute
diagnosis and should have come **before** the blind ~20-minute DO cycles, not
after several of them.

## Provenance

| Repo | Branch | Commit | What |
|---|---|---|---|
| horizon-rs | `cloud-designer-cloud-node-species` | `a94e2b9` | `NodeSpecies::CloudNode` + facet derivation |
| CriomOS | `cloud-designer-cloud-node-image` | `d25ae5f` | `disks/cloud-node.nix` image module |
| goldragon | `cloud-designer-cloud-node-data` | `48060b0` | doris node + the root-device boot fix |
| cloud | `cloud-designer-do-deploy-test` | `9b41512` | reusable live-deploy harness |

Image: `nixos-image-digital-ocean-26.05…-x86_64-linux.qcow2.bz2`, **1.1 GB
compressed**, DO `min_disk = 7 GB` (content-sized; growpart fills the droplet
disk at first boot). Declarative `nixpkgs digitalOceanImage` build — the
content-sized answer to the rejected 60 GB snapshot.

## Still open (carried from the 75 audit, awaiting psyche decisions)

The arc works end to end, but the audit's structural findings stand and several
are gated on design calls only the psyche can make:

- **`Substrate { Metal | Pod }` enum vs. `cloud_node` bool-accretion.** The
  CloudNode role currently rides a `bool` facet with zero consumers in
  horizon-rs (dead state) plus a redundant `TypeIs` one-hot. The audit's
  recommended shape replaces both with a typed substrate axis.
- **doris's home.** A `CloudNode`/`Metal` node now sits in *production* cluster
  data at trust `Max` with a placeholder host key (audit HIGH). Throwaway test
  node, or real cluster member? The answer decides whether it moves to a test
  cluster and how the host key is handled.
- **Fix-now remediation** (mechanical, bundled to follow the two decisions
  above so they aren't redone): `until_running` returning a non-running host on
  timeout; the covert placeholder key gaining a self-identifying marker; a
  lying "generalizes"/fixture comment; the "~55×" report over-claim caveated;
  the typed `ipv6`/`monitoring` server-spec fields replacing the hardcoded
  `false` band-aid.
