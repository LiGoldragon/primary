# 3 · Lane C — the minimal provable "CriomOS deployed onto the DO node"

cloud-designer sub-agent, 2026-06-20. Source-grounded against lojix
`schema_runtime.rs`, CriomOS `flake.nix` + nixos modules, and the canonical
nixpkgs DigitalOcean module. Boot-mode fact (Lane B) re-derived from
nixpkgs source this session. Every load-bearing claim cites `file:line` or
a URL; verified vs inferred is marked.

## TL;DR — the decision

**Do NOT use `meta-lojix Deploy … BootOnce` for the first live DO node.**
A DigitalOcean droplet boots **legacy BIOS / GRUB-MBR, not UEFI** — verified
from the canonical nixpkgs module
(`boot.loader.grub.devices = [ "/dev/vda" ]`, no EFI;
[digital-ocean-config.nix][do-config]). Every lojix `Boot`/`Switch`/`BootOnce`
activation path hard-requires `bootctl` + `/boot/loader/entries/nixos-generation-N.conf`
(systemd-boot UEFI) — `SystemActivation::boot_once_script`
(`schema_runtime.rs:3616-3635`), `step_set_efi_default_invocation`
(`:3674-3689`), and the simple `nix-env --set && switch-to-configuration boot`
path (`:3587-3596`). On a GRUB droplet `bootctl` is absent, so lojix's
BootOnce **cannot activate**. This matches the AGENTS guard the prior
contract already stated: "activation assumes systemd-boot UEFI NixOS; lojix
has no install path" (72/1 §"What the target node must satisfy", row 4).

**The simplest end-to-end "CriomOS is deployed" we can PROVE live this week
is a plain `nixos-rebuild switch --target-host root@<ip> --flake <criomos>`**,
where the flake attribute is CriomOS's own `nixosConfigurations.target`
realized with the four per-deploy inputs overridden to a **GRUB/MBR DO
horizon**. `nixos-rebuild` is bootloader-agnostic: it runs
`switch-to-configuration switch`, which invokes whichever bootloader the
*config* declares (here GRUB), unlike lojix's hardcoded `bootctl`
([nix.dev provisioning][nixdev]; [nixcademy remote][nixcademy]).

This is the same `system.build.toplevel` lojix would build
(`schema_runtime.rs:887`), activated the same way (`switch-to-configuration`,
`:3589`) — just driven by the stock `nixos-rebuild` wrapper that does not
assume `bootctl`. So the closure and activation are production-faithful; only
the *driver* differs.

## The exact deploy command

```
nixos-rebuild switch \
  --flake /git/github.com/LiGoldragon/CriomOS#target \
  --target-host root@<droplet-ipv4> \
  --build-host root@<droplet-ipv4> \
  --override-input system  path:/git/github.com/LiGoldragon/CriomOS/stubs/no-system \
  --override-input horizon path:<do-node-horizon-flake> \
  --override-input deployment path:/git/github.com/LiGoldragon/CriomOS/stubs/default-deployment \
  --override-input secrets path:/git/github.com/LiGoldragon/CriomOS/stubs/no-secrets
```

- `#target` is the only NixOS surface the CriomOS flake exposes
  (`flake.nix:180`, `nixosConfigurations.target`); `.config.system.build.toplevel`
  is appended by `nixos-rebuild` itself. This is the SAME attribute lojix
  uses (`DeployAction::target_attribute → nixosConfigurations.target.config.system.build.toplevel`,
  `schema_runtime.rs:887`).
- `--build-host root@<ip>` makes this **build-on-target** — realization in the
  droplet's own store, mirroring lojix's `--store ssh-ng://…` semantics
  (`schema_runtime.rs:3991-4008`). Drop `--build-host` to build locally and
  `nix copy` to the droplet instead (needs the droplet to accept unsigned or
  signed paths). For the first proof, **omit `--build-host` and build locally**
  — a CriomOS toplevel is small (no model NARs on a CloudNode), and it avoids
  needing the droplet to be a working remote builder on the first contact.
- The four `--override-input`s replace CriomOS's per-deploy stub inputs
  (`flake.nix:79,92,96,100`; stubs confirmed present:
  `stubs/{no-system,no-horizon,default-deployment,no-secrets}`). `horizon`
  is the load-bearing one — it must project a **GRUB/MBR DO node** (below).
  `system`, `deployment`, `secrets` use the in-repo stubs as-is for a
  secret-free, home-off, x86_64 first cutover.

**Inferred, not yet verified live:** that `nixos-rebuild`'s flake input
plumbing forwards `--override-input` into the `#target` evaluation cleanly
with CriomOS's `follows` graph (the `pkgs`/`horizon`/`system` follows at
`flake.nix:36-38,87-88` are designed for exactly this lojix override, so it
should — but the `nixos-rebuild` wrapper's `--override-input` passthrough on
this nixpkgs fork is unconfirmed). The robust fallback is to make the DO
horizon a **tiny content-addressed flake** whose `.#target` is fully pinned
(the lojix production shape), then
`nixos-rebuild switch --flake <do-deploy-flake>#target --target-host root@<ip>` —
no `--override-input` flags at all.

## The minimal CriomOS config — the DO horizon

CriomOS already renders a GRUB/MBR node; **no module edit is required for the
bootloader** — only a correct horizon projection. The gate is
`preinstalled.nix:41`:

```nix
grub.enable = bootloader == "Mbr";        # ← DO droplet path
systemd-boot.enable = bootloader == "Uefi";
```

So the DO node's horizon must set `io.bootloader = "Mbr"` (CriomOS
`Bootloader::Mbr`, the legacy-BIOS variant), NOT `Uefi`. The minimal horizon
that makes a DO droplet a deployable CriomOS node:

| Horizon field | Value | Why |
|---|---|---|
| `node.species` | `CloudNode` (or `TestVm` as a stand-in until ad53 lands) | leanness — no edge/center/router/largeAi facets (72/2 §1.1) |
| `node.io.bootloader` | **`Mbr`** | DO is BIOS/GRUB, not UEFI (`preinstalled.nix:41`; [do-config]) |
| `node.io.disks` | `/` → `/dev/vda1` ext4 (label `nixos`) | the droplet root disk (`preinstalled.nix:48-55`) |
| `node.machineSpecies` | `Pod` | a CloudNode is a provider VM → derives `virtual_machine` (72/2 §1.1) |
| `node.name` / `cluster.name` | e.g. `prometheus` / `goldragon` | identity; also the criome domain |
| root `authorizedKeys` | operator deploy pubkey | so `nixos-rebuild`/ssh reach `root@<ip>` (`users.nix:45-49`; `test-substrate.nix:151-152`) |

**Two concrete gaps the GRUB path exposes (must be closed in the horizon or a
small gate, NOT inferable):**

1. **`boot.loader.grub.devices` is unset.** `preinstalled.nix:41` enables GRUB
   but never sets the install disk; a BIOS GRUB install with no
   `grub.devices` fails activation. The DO node config must set
   `boot.loader.grub.devices = [ "/dev/vda" ]` (matching the canonical DO
   module, [do-config]) — via a horizon `io` field if one projects
   `grub.device`, else a one-line gate module
   (`modules/nixos/disks/cloud-node.nix`, the §72/2 gate) adding it under
   `mkIf (behavesAs.cloudNode or false)`. **Verify whether the current
   horizon schema projects a grub device before assuming the gate.**
2. **NSS + root shell + growpart for a headless cloud boot.** The
   `test-substrate.nix:130-141` prebakes (nscd on, passwd/group/shadow →
   `files`, absolute bash root shell) are needed or sshd rejects `root` as an
   "invalid user" on a headless node — exactly the CloudNode gate's job
   (72/2 §2). Plus `console=ttyS0` serial (`test-substrate.nix:164`) and
   growpart so the image fills the droplet disk.

For the very first proof these can be supplied as an **inline extra module**
on the `nixos-rebuild` flake (a throwaway `do-deploy` flake whose `#target`
imports `criomos` + a 15-line gate), avoiding any edit to CriomOS main until
the shape is proven. That gate is the embryo of the real
`disks/cloud-node.nix` (72/2 §1.2).

## "CriomOS deployed" vs merely "NixOS reachable"

A precise line, since the goal is to PROVE the former, not the latter:

| Claim | Evidence required | What it is NOT |
|---|---|---|
| **NixOS reachable** | `ssh root@<ip>` answers; `nixos-version` runs | could be the stock nixpkgs DO image, or any NixOS — says nothing about CriomOS |
| **CriomOS deployed** | the running `system.build.toplevel` is CriomOS's `nixosConfigurations.target` for *this node's horizon*: `readlink /run/current-system` points at the closure `nixos-rebuild` just built from `CriomOS#target`; `/run/current-system/nixos-version` / the system label carries the CriomOS revision; the CriomOS-specific module set is active (e.g. `normalize.nix` sshd-keys-only posture, the horizon-projected `networking.hostName = <node>`, `networking.domain = <cluster>.criome`) | a stock DO NixOS image with extra packages; an Ubuntu→NixOS cloud-init conversion |

**The minimal proof-of-CriomOS assertion set (run after the switch):**

```
ssh root@<ip> 'readlink /run/current-system'            # == the closure nixos-rebuild printed
ssh root@<ip> 'hostname -f'                              # == <node>.<cluster>.criome  (horizon-projected)
ssh root@<ip> 'cat /run/current-system/nixos-version'   # carries the CriomOS toplevel label
ssh root@<ip> 'systemctl is-active sshd && grep -c PasswordAuthentication\ no /etc/ssh/sshd_config'
```

"CriomOS deployed" = the third and fourth lines: the activated closure is the
CriomOS-evaluated toplevel for this node's horizon (not stock NixOS), and the
CriomOS posture (`normalize.nix` keys-only sshd, projected criome domain) is
live. Merely SSH-ing in proves only "NixOS reachable."

## Why this is the right minimal choice (vs the three options offered)

1. **Full `meta-lojix Deploy … BootOnce` — REJECTED for week-one.** Blocked on
   the boot mode (GRUB ≠ systemd-boot, so `bootctl` activation fails,
   `schema_runtime.rs:3616-3689`) AND on `nixosConfigurations.target`'s node
   identity still being "the deferred M3 materialization work"
   (`schema_runtime.rs:882` comment) — lojix's horizon `--override-input`
   injection of node identity is not confirmed wired. Two unbuilt
   dependencies; not provable this week. (It becomes the right path once the
   DO node is UEFI-capable — see below — and M3 lands.)
2. **`nixos-rebuild switch --target-host` — CHOSEN.** Bootloader-agnostic,
   no `bootctl` assumption, builds the identical `CriomOS#target` toplevel,
   activates via the identical `switch-to-configuration switch`. Provable on a
   stock GRUB DO droplet this week. The one driver that does not inherit
   lojix's UEFI assumption.
3. **Bare build-on-target realization of the closure — INSUFFICIENT alone.**
   `nix build … --store ssh-ng://root@<ip> CriomOS#target.config.system.build.toplevel`
   proves the closure *realizes on the node* but does NOT activate it — the
   node still runs its old generation. That is "closure present," weaker than
   "CriomOS deployed." `nixos-rebuild switch --build-host` does both
   (build-on-target THEN switch) in one command, so it strictly dominates.

## The clean upgrade to the full lojix path (next, not this week)

To later deploy via real `meta-lojix Deploy … BootOnce`, the DO node must
become **UEFI/systemd-boot**. DigitalOcean's *default* droplet firmware is
BIOS, but a **custom UEFI CriomOS image** (the ad53 CloudNode image, 72/2 §3)
booted with an EFI System Partition makes `bootctl` present and the lojix
BootOnce path live. So the progression is:

```
week 1 (this report):  stock GRUB DO droplet  +  nixos-rebuild switch CriomOS#target(Mbr horizon)   → CriomOS deployed, GRUB
later (ad53 + M3):     baked UEFI CloudNode image  +  meta-lojix "(Deploy (System (… FullOs … BootOnce …)))"  → CriomOS deployed, lojix-managed, headless-safe rollback
```

The week-1 path is the honest minimal proof; it does not pretend lojix's
production deploy works on a node it structurally cannot activate.

**UNVERIFIED — confirm live before running:**
- DO droplet is BIOS/GRUB by default (canonical nixpkgs module says so via
  `grub.devices=/dev/vda` + GRUB timeout, [do-config]; but confirm the
  *specific* droplet plan/region you provision exposes no UEFI option).
- `nixos-rebuild --override-input` passthrough on `github:LiGoldragon/nixpkgs`
  fork forwards into `#target`'s follows graph (fallback: a pinned
  `do-deploy#target` flake, no flags).
- Whether CriomOS's horizon schema projects `grub.device` / `boot.loader.grub.devices`;
  if not, the one-line `devices=[/dev/vda]` gate is mandatory.
- Operator deploy pubkey is in the droplet's `root` `authorized_keys` at
  first contact (the same precondition flagged 72/1 §"Open question").

[do-config]: https://github.com/NixOS/nixpkgs/blob/master/nixos/modules/virtualisation/digital-ocean-config.nix
[nixdev]: https://nix.dev/tutorials/nixos/provisioning-remote-machines.html
[nixcademy]: https://nixcademy.com/posts/nixos-rebuild-remote-deployment/
