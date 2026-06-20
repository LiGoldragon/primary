# 73/2 — DigitalOcean droplet boot mode and its consequence for lojix activation

Lane B of the CriomOS DO deploy proof. Question: do DigitalOcean droplets
boot UEFI or legacy BIOS, can a custom image change that, what do
nixos-infect / nixos-anywhere produce there — and therefore can lojix's
`bootctl`-based BootOnce activation run on DO this week, or must the realistic
proof use a different mechanism?

Method: WebSearch + WebFetch against official DigitalOcean docs and corroborating
community/tooling sources (2025), cross-read against the lojix activation source
(`lojix/src/schema_runtime.rs`) and cloud-designer report 72. Each load-bearing
claim is cited; verified-vs-inferred is marked inline.

## Bottom line (recommendation)

**DigitalOcean droplets boot legacy BIOS/GRUB-MBR, not UEFI/systemd-boot, and
this cannot be changed — not by region, not by a custom uploaded image (DO
explicitly forbids UEFI custom images).** Therefore lojix's `BootOnce`
activation (`bootctl set-default`/`set-oneshot`) **cannot run as-is on DO**, and
neither can the EFI-reconcile tail of `Boot`/`Switch`. The deploy mechanism that
actually works on DO now is:

> **GRUB-BIOS NixOS on the droplet (provisioned by nixos-anywhere/disko or
> nixos-infect, GRUB on `/dev/vda`), activated over ssh with
> `nixos-rebuild`-equivalent `switch-to-configuration switch` (or `boot`) —
> i.e. lojix's `Switch`/`Boot` *core* step minus the `bootctl` EFI-reconcile
> tail.** The fully headless-rollback `BootOnce` path is **not feasible on DO
> this week** without either (i) teaching lojix a GRUB rollback path, or (ii)
> moving the live proof to a UEFI provider (Hetzner Cloud is UEFI; see §5).

If the proof must use lojix exactly as written, the only DO-compatible lojix
action is **`Test`** (`switch-to-configuration test`, non-persistent, no
bootloader touch) or pure **`Build`/`Eval`** (closure realization on target, no
activation). That proves the daemon→node deploy spine end-to-end but not a
persistent boot-generation switch.

## 1. DigitalOcean droplet boot mode: legacy BIOS, not UEFI

**Verified.** DigitalOcean droplets boot via **legacy BIOS**. Multiple
independent confirmations:

- A DigitalOcean community answer ("Is Ubuntu instances boot with EFI or BIOS?")
  states there is **no `/sys/firmware/efi`** directory on a droplet and
  `efibootmgr` returns *"EFI variables are not supported on this system"* — the
  definitive Linux-side test for BIOS vs UEFI. The absence of `/sys/firmware/efi`
  is exactly the precondition systemd-boot / `bootctl` require, and it is absent.
  [DO community: Is Ubuntu instances boot with EFI or BIOS?](https://www.digitalocean.com/community/questions/is-ubuntu-instances-boot-with-efi-or-bios)

- A July 15 2025 DigitalOcean ideas-portal feature request — *"Migration from
  Legacy BIOS to UEFI"* — exists precisely because droplets are still Legacy
  BIOS in mid-2025. The request asks DO to *consider migrating its VM
  infrastructure from Legacy BIOS to UEFI*; it is an open user suggestion with
  **no DO commitment and no ship date**, so BIOS is the standing reality as of
  the most recent (2025) source.
  [DO ideas: Legacy BIOS → UEFI migration request (2025-07-15)](https://ideas.digitalocean.com/core-compute-platform/p/migration-from-legacy-bios-to-uefi-for-enhanced-performance-and-security)

**Region / image dependence — inferred-strong:** I found **no source** indicating
the boot mode varies by region or by stock image (Ubuntu / Debian / Fedora /
etc.). The firmware is a property of the DO hypervisor/VM platform, not the guest
image, and the custom-image rule in §2 (UEFI categorically unsupported, no
region carve-out) is consistent with a uniform BIOS platform. Treat "DO is BIOS
everywhere" as the safe operating assumption; it is not contradicted by any
source found.

## 2. Custom uploaded image cannot be UEFI/systemd-boot

**Verified — this is the decisive constraint.** DigitalOcean's official Custom
Images documentation states, verbatim:

> **"UEFI boot is not supported. Custom images must boot using BIOS."**

[DO docs: Custom Images — Limits](https://docs.digitalocean.com/products/custom-images/details/limits/)

So the escape hatch of "upload a UEFI systemd-boot NixOS image" is **closed by
policy**, not merely unsupported by tooling. A custom image that boots only via
UEFI/systemd-boot will not boot as a droplet. (The features page additionally
notes raw images may carry an MBR *or* GPT partition table, but that is partition
layout, not firmware — GPT-on-BIOS still requires a BIOS-boot partition for GRUB
embedding, see §3.)
[DO docs: Custom Images — Features](https://docs.digitalocean.com/products/custom-images/details/features/)

This means a CriomOS cloud-node image destined for DO **must** be GRUB-BIOS. The
home-built `cloud-node` image work (report 65) and any image-upload path must
target `boot.loader.grub` with a BIOS device, not `boot.loader.systemd-boot`.

## 3. What nixos-infect / nixos-anywhere produce on DO: GRUB-BIOS

**Verified.** Both standard NixOS-on-DO provisioners land **GRUB in BIOS/MBR
mode**, because that is the only thing that boots there:

- **nixos-infect** on DO is historically defined by the GRUB-BIOS failure mode:
  the canonical issue ("Digital ocean grub issue", elitak/nixos-infect#2) is GRUB
  refusing to embed because *"this GPT partition label contains no BIOS Boot
  Partition; embedding won't be possible … but this is required for cross-disk
  install."* The fix is to give GRUB a BIOS-boot partition / install GRUB to the
  MBR device — i.e. the resolution is *more* BIOS-GRUB, never a switch to
  systemd-boot. nixos-infect's DO output is `boot.loader.grub` on the disk
  device.
  [elitak/nixos-infect#2 — Digital ocean grub issue](https://github.com/elitak/nixos-infect/issues/2)

- **nixos-anywhere + disko** on a DO droplet sets `boot.loader.grub.device` to
  the disk (DO virtio disk is **`/dev/vda`**); disko's `nixosModule` wires the
  GRUB device for BIOS automatically. There is no UEFI ESP because there is no
  EFI firmware to read it.
  [disko #981 — boot.loader.grub.devices / EFI](https://github.com/nix-community/disko/issues/981);
  [NixOS Wiki — Bootloader (GRUB BIOS requires boot.loader.grub.device)](https://wiki.nixos.org/wiki/Bootloader)

**Inferred (consistent, not separately cited):** a stock DO Ubuntu/Debian droplet
already boots GRUB-BIOS, so an in-place infect inherits BIOS; nixos-anywhere via
kexec installs onto the same BIOS disk. Either way the resulting NixOS uses
**GRUB, no `/boot/loader/entries`, no `bootctl`.**

## 4. Consequence for lojix activation

lojix has two structurally different activation paths
(`lojix/src/schema_runtime.rs`, `SystemActivation`):

| lojix action | What runs on target | EFI / `bootctl` dependency | DO-feasible? |
|---|---|---|---|
| `Test` | `switch-to-configuration test` (`schema_runtime.rs:3584-3585`) | **none** — non-persistent, no bootloader touch | **Yes** |
| `Build` / `Eval` | closure realize on target; `ssh_invocation` returns `None`, no activation (`:3579-3581`) | none | **Yes** |
| `Switch` / `Boot` | `nix-env --set` + `switch-to-configuration {switch,boot}` (`:3587-3590`), **then** `reconcile_efi()` → `bootctl set-default` + `set-oneshot ''` (`:3705-3717, 3674-3689`) | **EFI tail** (`requires_efi_reconcile()` true for Boot/Switch, `:3659-3664`) | **core step yes; `bootctl` tail fails** |
| `BootOnce` | `systemd-run` transient unit running `boot_once_script`: `bootctl status` → `bootctl set-default OLD` → `bootctl set-oneshot NEW`, asserting `/boot/loader/entries/$NEW` exists (`:3616-3635`) | **fully `bootctl`/systemd-boot/ESP** | **No** |

On a DO BIOS/GRUB droplet:

- `bootctl` exits non-zero (no EFI variables, no `/sys/firmware/efi`), so
  `bootctl status` in `boot_once_script` fails immediately, `OLD` is empty, the
  `[ -n "$OLD" ]` guard trips, and the `[ -f "/boot/loader/entries/$NEW" ]`
  assertion fails because GRUB has no loader-entry directory. **`BootOnce` cannot
  run as-is.** This matches report 72 §1.5 / report 71-4 (a): lojix activation
  "assumes systemd-boot UEFI NixOS" and has no install path
  (`72/1-lojix-deploy-contract.md:206, 341`).

- `Switch`/`Boot`'s *core* `switch-to-configuration switch|boot` is
  bootloader-agnostic and works fine on GRUB — but the trailing
  `reconcile_efi()` (`bootctl set-default`) will fail on DO. So `Switch`/`Boot`
  are feasible **only if the EFI-reconcile tail is skipped/conditioned** on the
  target actually being EFI. (`switch-to-configuration switch` itself already
  runs the GRUB generation install via NixOS's own bootloader builder, so the
  `bootctl` step is redundant on GRUB, not just broken.)

### Is full lojix activation feasible on DO this week?

**No, not the headless-rollback `BootOnce` flow** — it is hard-wired to
systemd-boot + UEFI + mutable ESP, none of which DO provides, and DO forbids
supplying them via custom image. Making `BootOnce` work on DO is a code change
(a GRUB rollback path, e.g. `grub-reboot`/`grub-set-default` oneshot semantics),
not a config tweak — out of scope for a this-week live proof.

## 5. The realistic DO deploy proof — recommendation

Order of preference for proving a LIVE DO deploy path this week:

1. **(Recommended) GRUB-BIOS NixOS + `switch-to-configuration switch` over ssh.**
   Provision the droplet to NixOS with nixos-anywhere/disko (GRUB on `/dev/vda`,
   no ESP) or nixos-infect. Drive activation with lojix's `Switch` (or `Boot`)
   **core step** — `nix-env -p /nix/var/nix/profiles/system --set <closure> &&
   <closure>/bin/switch-to-configuration switch` — which is exactly
   `nixos-rebuild switch`'s activation and is bootloader-agnostic. This proves a
   *persistent* generation switch on a real DO droplet. **Caveat:** lojix as
   written appends `reconcile_efi()` for `Switch`/`Boot`; on DO that tail fails,
   so either (a) run the `switch-to-configuration switch` step directly over ssh
   for the proof (bypassing lojix's EFI tail), or (b) gate `requires_efi_reconcile()`
   on EFI presence (`test -d /sys/firmware/efi`) so lojix's `Switch` becomes
   DO-clean. Option (b) is the right durable fix and small.

2. **(Cleanest lojix-as-is) `Test` activation** — `switch-to-configuration test`.
   Runs unmodified lojix, touches no bootloader, works on DO today. Proves the
   full daemon→socket→node deploy spine and live config activation, but the
   switch is non-persistent (lost on reboot). Good as the *first* green light if
   modifying lojix is undesirable this week.

3. **(Narrowest) Build-on-target closure realization only** —
   `nix build --store ssh-ng://root@<ip> <drv>^*` or `nix copy --to
   ssh-ng://root@<ip>`, no activation at all. Proves store/transport reachability
   to a DO droplet but not activation. Weakest claim; use only if even `Test`
   is blocked.

4. **(If UEFI/`BootOnce` must be exercised live) move that leg to Hetzner Cloud.**
   Hetzner Cloud VMs boot UEFI (per the report 56 Hetzner on-ramp work), so the
   full systemd-boot `BootOnce` headless-rollback path can be proven there while
   DO covers the BIOS/GRUB matrix. This is the honest split: **DO proves
   GRUB-BIOS `Switch`; Hetzner proves UEFI `BootOnce`.** (Hetzner UEFI claim is
   from prior cloud-designer work, report 56 — verify live before relying on it.)

## Unverified / to confirm live

- That `efibootmgr`/`/sys/firmware/efi` absence holds on the *current* (2026) DO
  droplet image family I will actually boot — confirm on the live droplet with
  `[ -d /sys/firmware/efi ] && echo UEFI || echo BIOS` before choosing the lojix
  action. (Source evidence is 2025-era community + 2025 ideas portal.)
- Region independence of boot mode — no source explicitly rules out a UEFI
  region; assumed uniform BIOS. Confirm on the target region.
- Hetzner Cloud being UEFI (§5 option 4) — carried from report 56, not
  re-verified here.

## Sources

- [DO docs — Custom Images, Limits ("UEFI boot is not supported. Custom images must boot using BIOS.")](https://docs.digitalocean.com/products/custom-images/details/limits/)
- [DO docs — Custom Images, Features (MBR/GPT, no UEFI)](https://docs.digitalocean.com/products/custom-images/details/features/)
- [DO community — Is Ubuntu instances boot with EFI or BIOS? (no /sys/firmware/efi; efibootmgr unsupported)](https://www.digitalocean.com/community/questions/is-ubuntu-instances-boot-with-efi-or-bios)
- [DO ideas — Migration from Legacy BIOS to UEFI (2025-07-15, open request ⇒ still BIOS)](https://ideas.digitalocean.com/core-compute-platform/p/migration-from-legacy-bios-to-uefi-for-enhanced-performance-and-security)
- [elitak/nixos-infect#2 — Digital ocean grub issue (GRUB-BIOS embedding)](https://github.com/elitak/nixos-infect/issues/2)
- [nix-community/disko#981 — GRUB device vs EFI](https://github.com/nix-community/disko/issues/981)
- [NixOS Wiki — Bootloader (BIOS requires boot.loader.grub.device)](https://wiki.nixos.org/wiki/Bootloader)
- lojix activation source: `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:3551-3718` (SystemActivation, boot_once_script, reconcile_efi)
- `reports/cloud-designer/72-lojix-cloud-implementation-research/1-lojix-deploy-contract.md:206,341`
