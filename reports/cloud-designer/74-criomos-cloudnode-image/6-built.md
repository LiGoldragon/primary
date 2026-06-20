# 74/6 — Built: the minimal CriomOS DigitalOcean CloudNode image (1.1 GB)

cloud-designer, 2026-06-20. Implementation + result for Spirit `2u57` (the
cloud-node image is a NEW CriomOS image type, declaratively built, minimal and
content-sized, configured via the cluster data). Follows the plan in `5-plan.md`.

## Result — the minimality verdict

The image built green and is **1,176,051,567 bytes (1.1 GB)** —
`nixos-image-digital-ocean-26.05…-x86_64-linux.qcow2.bz2`, a bzip2-compressed
qcow2. Versus the **60 GB** converted-droplet snapshot that triggered this
rework, that is the directive met: **content-sized, ~55× smaller, declarative,
reproducible.** The disk image is sized to the closure (`diskSize = "auto"`),
not to a fixed droplet geometry; growpart expands `/` to the real droplet disk
at first boot.

**Caveat (audit 75/#38).** The "~55× smaller" figure compares the compressed
content-sized image (1.1 GB) against the 60 GB *droplet disk geometry* of the
old snapshot — content size vs. provisioned-disk size, not like-for-like, so
read it as "we ship the closure, not the disk" rather than a 55× content
reduction. And the 1.1 GB build *overshot* this report's own earlier prediction
of a ~0.5–1 GB uploadable image (74/1) with no note at the time; the closure is
simply larger than predicted.

## What landed (three repos, three designer branches, all pushed)

| Repo | Branch | Change |
|---|---|---|
| horizon-rs | `cloud-designer-cloud-node-species` | `NodeSpecies::CloudNode` + `TypeIs.cloud_node` + `BehavesAs.cloud_node` derivation + test `project_cloud_node_metal_derives_lean_profile`. Full horizon suite **24 passed**. `a94e2b9`. |
| CriomOS | `cloud-designer-cloud-node-image` | `modules/nixos/disks/cloud-node.nix` (imports upstream `digital-ocean-image` only for a cloud node, content-sized, GRUB-on-/dev/vda, trims docs/firmware/fontconfig, keeps virtio initrd) + `criomos.nix` import + guarded `flake.nix` `packages.<system>.digitalOceanImage`. `621a89a`. |
| goldragon | `cloud-designer-cloud-node-data` | `doris` — a `CloudNode`/`Metal`/`Mbr`/`/dev/vda` node in the cluster data + trust line. `b10df73`. |

## The chain, verified before the build

`horizon-cli --cluster goldragon --node doris < datom.nota` projects `doris`
with `behaves_as.cloud_node = true`, `virtual_machine = false`,
`bare_metal = true`, and every role facet (`edge`/`center`/`router`/`large_ai`)
false — the lean profile. The projected horizon flake exposes
`horizon.node.behavesAs.cloudNode = true`, so the CriomOS module gate fires and
`system.build.digitalOceanImage` exists. The build was hand-materialized (the
lojix path, by hand): `horizon` = the doris projection, `system` = `x86_64-linux`
(pkgs follows), `deployment` = headless (`includeHome = false`).

```bash
nix build CriomOS#packages.x86_64-linux.digitalOceanImage \
  --override-input horizon path:<doris-projection-flake> \
  --override-input system  path:<x86_64-linux-flake> \
  --override-input deployment path:<headless-flake>
# → result/…qcow2.bz2  (1.1 GB)
```

## Minimality — by construction, three levers

1. **`virtualisation.diskSize = "auto"`** — make-disk-image measures the closure
   and sizes the partition to it; no fixed 60 GB region. growpart fills the
   droplet disk at runtime.
2. **`includeHome = false`** (headless deployment) — drops the desktop /
   home-manager tree, the bulk of an edge image. `CloudNode` derives no role
   facet, so no desktop/edge/center/router/LLM module tree derives onto it.
3. **Module trims** — docs / firmware / fontconfig off; bzip2 over qcow2.
   Default kernel/initrd modules are KEPT — virtio_blk/virtio_net are required
   to boot a droplet (the unbootable-minimization trap, deliberately avoided).

## Next — upload + deploy (token unblocked)

`gh release` the qcow2.bz2 → `POST /v2/images {url}` (the `image:create` scope is
now present) → poll to `available` → boot via the existing harness
(`CRIOMOS_IMAGE=<id> DO_REGION=nyc3 nix run cloud#digitalocean-deploy-live-test`)
→ DO's metadata server injects a fresh ssh key per-instance (the reusability the
60 GB snapshot lacked) → confirm CriomOS → always-destroy. The image is retained
as the reusable artifact; the placeholder host key in `doris` is replaced with
the real droplet key before any non-test deploy.
