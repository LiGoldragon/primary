# 6 · Built and tested — the re-usable CriomOS-on-DigitalOcean deploy harness

cloud-designer, 2026-06-20. What I made in response to *"develop and test
further. try deploying criomos to DO with a pre-made image. report on what/how
you made it. let's make this re-usable test code."* This report is the
build+live-test record; the research recipe it implements is
`5-recipe.md`, the boot-mode/token findings are `1`–`4`.

Branch `cloud-designer-do-deploy-test` @ `783e23c` (cloud, pushed). Live witness
captured against real DigitalOcean.

## TL;DR

- **Built a re-usable live deploy harness** that provisions a DigitalOcean
  droplet **from a pre-made image** through the production adapter, confirms it
  over ssh, and **always destroys** every resource — plus the flake app, the
  CI-safe check, and the image-mint recipe. All on the branch.
- **Ran it live and green** (mode 2, current token): provision → Running → ssh
  reachable → destroyed, **droplet `578965503`, ipv4 `143.244.145.64`, clean
  teardown, 36.7s**, account verified empty afterward.
- **The literal "pre-made CriomOS image" (mode 1) is blocked on one thing only
  the psyche can do:** the live DigitalOcean token lacks the **`image:create`**
  scope, so minting/snapshotting an image `403`s. Re-mint the token with
  `image:create` (or full scope) at the same gopass handle and the harness boots
  the CriomOS image with `CRIOMOS_IMAGE=<id>` — no code change.
- **Two hard constraints the research nailed:** DigitalOcean droplets boot
  **legacy BIOS/GRUB only** (UEFI unsupported by policy), so lojix's
  `bootctl`/`BootOnce` activation is **structurally impossible on DO** — the
  deploy is bootloader-agnostic `nixos-rebuild switch`; and a Mbr horizon needs
  a `boot.loader.grub.devices = [ "/dev/vda" ]` gate (`preinstalled.nix:41`
  enables GRUB but sets no device).

## What I made

| Artifact | Path (branch `cloud-designer-do-deploy-test`) | What it does |
|---|---|---|
| Deploy harness | `cloud/tests/digitalocean_deploy_live.rs` | Provision-from-image → poll Running → ssh-confirm → optional `nixos-rebuild` push → **always destroy** → one witness line. Methods on data-bearing types; typed `DeployLevel`. |
| Flake app | `cloud/flake.nix` `apps.digitalocean-deploy-live-test` | `writeShellApplication` wrapper: injects the gopass token, runs the test, and adds a **prefix-named `trap … EXIT` sweep** as a second always-destroy net (covers `kill -9` before the Rust `Drop` runs). |
| CI gate | `cloud/flake.nix` `checks.digitalocean-deploy-live-test-compiles` | Compiles + `--list`s the test but **never executes it**, so `nix flake check` catches bit-rot without spending money. |
| Image-mint recipe | `cloud/scripts/digitalocean-mint-criomos-image.sh` | The re-usable "how you make the image": provision Ubuntu → `nixos-infect`/`nixos-anywhere` → snapshot → numeric image id → destroy mint droplet. Shellcheck-clean. Blocked at the snapshot step until the token gains `image:create`. |

The harness drives the **in-process `digitalocean::HttpApi`** — the same
adapter the daemon uses in production — not `doctl` (which isn't installed). It
extends the proven Tier-1 lifecycle test, generalizing its `Drop`-guard cleanup
into `DeployCleanup` and its key-mint into a prefix-named `TemporarySshKey`
whose **private half stays local** so the deploy step can reach the node.

## The two modes (the image is what carries CriomOS)

- **Mode 1 — pre-made image (the asked-for path).** `CRIOMOS_IMAGE=<numeric
  snapshot id>`: boot a droplet from the CriomOS snapshot; "deploy" = boot +
  confirm the running system is CriomOS (ssh reads the `/etc/os-release` /
  `CRIOMOS_MARKER`). No push step — the OS arrives in the image. **Runnable the
  moment a snapshot id exists** (blocked today only on the token scope to mint
  one). `DO_REGION` must equal the image's home region (DO constraint).
- **Mode 2 — stock image (runnable today, proven).** Boot a stock slug
  (`ubuntu-24-04-x64`), confirm ssh reachability; with `DEPLOY_FLAKE` set, push
  a generation with `nixos-rebuild switch --target-host` (requires the node be
  NixOS first — i.e. a NixOS image or a `nixos-infect`'d droplet).

## What is proven vs pending — honest deploy-level matrix

| Capability | Status | Evidence |
|---|---|---|
| Provision from a parametrized image → Running → IPv4 → **always destroy** | **Proven live** | droplet `578965503`, ipv4 `143.244.145.64`, `deploy=ssh-reachable result=OK`, account empty after |
| ssh-confirm path (mint key, wait for sshd, read `/etc/os-release`) | **Proven live** | the retry loop absorbed an early "connection refused"; read Ubuntu's release (no CriomOS marker → honest `ssh-reachable`) |
| Harness compiles + clippy-clean (`-D warnings`) + CI gate never spends | **Proven** | `cargo test --no-run` green; `cargo clippy -- -D warnings` clean; `--list`-only check |
| Mode 1 boot-a-CriomOS-image + marker confirm | **Blocked on token** | needs `image:create` to mint the snapshot; harness code is ready |
| `nixos-rebuild switch` deploy-push (DEPLOY_FLAKE) | **Wired, not yet exercised live** | needs a NixOS node + a Mbr-horizon `do-node` flake with the `/dev/vda` GRUB gate |
| lojix `Deploy … BootOnce` on DO | **Out on DO** | DO is BIOS-only; `bootctl`/systemd-boot cannot run — UEFI `BootOnce` belongs on Hetzner |

## How to run it

```sh
cd /git/github.com/LiGoldragon/cloud   # (or the do-deploy-test worktree)
# mode 2 today — stock image, ssh-reachable confirm, always destroy:
nix run .#digitalocean-deploy-live-test
# mode 1 once a CriomOS snapshot exists:
CRIOMOS_IMAGE=<numeric-id> DO_REGION=<image-region> nix run .#digitalocean-deploy-live-test
# mint the image (after the token gains image:create):
DO_REGION=nyc3 ./scripts/digitalocean-mint-criomos-image.sh
```

## The one psyche action that unblocks the literal ask

**Mint a DigitalOcean Personal Access Token with `image:create` (the prior
session's lean was full scope — *"I would have chosen all them myself"*) and
store it at `gopass digitalocean.com/api-token`.** That is the single gate
between the harness as-is and a real *pre-made CriomOS image* boot. Token
minting is the human's (browser) job; nothing else in the path needs it.

## Next slice (once the token is widened)

1. Run `scripts/digitalocean-mint-criomos-image.sh` → a numeric CriomOS image id
   (the `CONVERT=anywhere FLAKE=…` variant gives full CriomOS fidelity once a
   Mbr-horizon `do-node` flake with the `/dev/vda` GRUB gate exists).
2. `CRIOMOS_IMAGE=<id> DO_REGION=<r> nix run .#digitalocean-deploy-live-test` →
   `deploy=criomos-confirmed`.
3. Promote the `do-node` GRUB gate into the real `modules/nixos/disks/cloud-node.nix`
   (the embryo of Spirit `ad53`'s CloudNode species, but Mbr/BIOS for DO).
