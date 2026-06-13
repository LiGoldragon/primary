# 7b — Approach B: nixos-generators qcow2 deploy-target VM

Real writable NixOS qcow2 disk image built on `prometheus.goldragon.criome`,
under `/tmp/lojix-e2e/diskB`, replacing the broken qemu-vm.nix attempt
(ro store + 2.4 GiB). Every claim below is grounded in a command that was run.

## Result

PASS. Built + booted under KVM/OVMF UEFI; verified writable `/nix/store`
on the virtual disk, >=15 GiB free, systemd-boot active (`bootctl status`
works). See verification block at the end.

## Environment (Prometheus, verified)

- `/dev/kvm`: `crw-rw-rw-` (writable). `nproc` = 32. `/tmp` 1012 GiB avail.
- `nix` 2.34.6; flakes via `--extra-experimental-features "nix-command flakes"`.
- qemu/OVMF NOT in PATH — built from the locked nixpkgs:
  - `qemu` 11.0.0 → `/tmp/lojix-e2e/qemu-result/bin/qemu-system-x86_64`, `qemu-img`
  - `OVMF.fd` → `/nix/store/zp51g43pr03sisri6xs1nyba6j2ad5kc-OVMF-202602-fd/FV/`
    (`OVMF_CODE.fd` read-only firmware, `OVMF_VARS.fd` NVRAM template)
- ssh pubkey baked in: `/tmp/lojix-e2e/runner_key.pub`
  (`ssh-ed25519 AAAA...YZIm6 lojix-e2e`).

## The flake (`/tmp/lojix-e2e/diskB/flake.nix`)

Inputs: `nixpkgs` = `github:NixOS/nixpkgs/nixos-unstable` (locked to
`9ae611a`, NixOS 26.11.20260610), `nixos-generators` follows nixpkgs.

Builder: `nixos-generators.nixosGenerate { system = "x86_64-linux";
format = "qcow-efi"; modules = [ ... ]; }`. The `qcow-efi` format uses
`lib/make-disk-image.nix` (real ext4 root + real writable store on the
qcow2; NOT 9p, NOT overlay, NOT a host-shared mount) with an EFI partition
table + ESP.

Module overrides applied on top of the format:

- `virtualisation.diskSize = 24576;`  — 24 GiB virtual disk (the
  `make-disk-image` disk/root size knob).
- Bootloader switched from the format's GRUB-EFI to **systemd-boot**:
  `boot.loader.grub.enable = lib.mkForce false;`
  `boot.loader.systemd-boot.enable = true;`
  `boot.loader.efi.canTouchEfiVariables = false;`
  (Required so `bootctl` / systemd-boot is the active loader.)
- **Writable store** (KEY FIX): `boot.nixStoreMountOpts = [ "rw" "nodev" "nosuid" ];`
  NixOS 26.11 removed `boot.readOnlyNixStore`; the default
  `nixStoreMountOpts` is `[ "ro" "nodev" "nosuid" ]`, which re-bind-mounts
  `/nix/store` read-only on top of the rw root. Setting `rw` keeps the
  store mount read-write. (First build had a ro store bind precisely
  because this default was in effect.)
- openssh: `enable = true`, `PermitRootLogin = "yes"`,
  `PasswordAuthentication = false`; root authorizedKeys = baked-in pubkey.
- `networking.firewall.enable = false;`, serial console, `stateVersion = "24.11"`.

## Exact build command

```
cd /tmp/lojix-e2e/diskB
nix flake lock --extra-experimental-features "nix-command flakes"
nix build --extra-experimental-features "nix-command flakes" .#diskB \
  -o result --print-build-logs
```

Build output: `result/nixos.qcow2`, `qemu-img info` → virtual size 24 GiB
(25769803776 bytes), disk size ~2.3 GiB (sparse — grows on guest writes).

## Writable-disk prep

The build result is read-only in the store. Make a writable working copy
plus a writable OVMF NVRAM:

```
cd /tmp/lojix-e2e/diskB
cp --reflink=auto result/nixos.qcow2 disk.qcow2
chmod u+w disk.qcow2
cp /nix/store/zp51g43pr03sisri6xs1nyba6j2ad5kc-OVMF-202602-fd/FV/OVMF_VARS.fd OVMF_VARS.diskB.fd
chmod u+w OVMF_VARS.diskB.fd
```

`qemu-img info disk.qcow2` → virtual size 24 GiB, `-rw-r--r--`.

## Exact qemu boot command (KVM + OVMF UEFI + hostfwd 2224)

```
QEMU=/tmp/lojix-e2e/qemu-result/bin/qemu-system-x86_64
OVMF=/nix/store/zp51g43pr03sisri6xs1nyba6j2ad5kc-OVMF-202602-fd
$QEMU \
  -name diskB-e2e \
  -machine q35,accel=kvm \
  -cpu host -smp 4 -m 4096 \
  -drive if=pflash,format=raw,readonly=on,file=$OVMF/FV/OVMF_CODE.fd \
  -drive if=pflash,format=raw,file=/tmp/lojix-e2e/diskB/OVMF_VARS.diskB.fd \
  -drive file=/tmp/lojix-e2e/diskB/disk.qcow2,if=virtio,format=qcow2 \
  -netdev user,id=net0,hostfwd=tcp::2224-:22 \
  -device virtio-net-pci,netdev=net0 \
  -nographic -serial file:/tmp/lojix-e2e/diskB/console.log
```

SSH in:
`ssh -i /tmp/lojix-e2e/runner_key -p 2224 -o StrictHostKeyChecking=no \
  -o UserKnownHostsFile=/dev/null root@127.0.0.1`

## Verification (booted guest, all run over ssh root@127.0.0.1:2224)

Guest: NixOS 26.11.20260610.9ae611a, kernel Linux 6.18.35 x86_64.

- **Store mount RW** (real ext4 on the virtual disk, not 9p/overlay/ro):
  `findmnt /nix/store` → `/dev/vda2[/nix/store] /nix/store ext4 rw,nosuid,nodev,relatime`
  `/proc/mounts` → `/dev/vda2 /nix/store ext4 rw,nosuid,nodev,relatime`
- **STORE-RW-OK**: `touch /nix/store/STORE-RW-TEST.$$` succeeded (file created
  `-rw-r--r-- root root`, then removed).
- **Capacity**: `df -h /nix/store` → `/dev/vda2 24G 2.1G 20G 10%` — **20 GiB avail**
  (>= 15 GiB). Headroom proven: `dd` of a 1 GiB file into the store succeeded
  (avail 20G→19G, host `disk.qcow2` grew 2.4→3.2 GiB allocated = real writes),
  then reclaimed.
- **Root**: `findmnt /` → `/dev/vda2 / ext4 rw,relatime`.
- **systemd-boot UEFI**: `bootctl status` → Firmware UEFI 2.70 (EDK II),
  Current Boot Loader = systemd-boot 260.1; `bootctl is-installed` → `yes` (rc 0).
  ESP at `/boot` (`/dev/vda1` 249M, `systemd-bootx64.efi` +
  `loader/entries/nixos-*.conf` present).
- **current-system**:
  `readlink /run/current-system` →
  `/nix/store/gjhmgkpzvm681cam4p1lnq7vxy7sp5kc-nixos-system-nixos-26.11.20260610.9ae611a`
- **nix daemon**: `nix-store --version` → 2.34.7 (store writable for nix-copy).

VM stopped after test (`kill $(pgrep -f "name diskB-e2e")`; 0 qemu procs).

## Artifacts on Prometheus

- `/tmp/lojix-e2e/diskB/flake.nix` + `flake.lock` — the recipe.
- `/tmp/lojix-e2e/diskB/result` → `/nix/store/7y3qvmal...-nixos-disk-image/nixos.qcow2`
  (read-only build output, 24 GiB virtual).
- `/tmp/lojix-e2e/diskB/disk.qcow2` — writable working copy (booted/verified).
- `/tmp/lojix-e2e/diskB/OVMF_VARS.diskB.fd` — writable NVRAM.
- `/tmp/lojix-e2e/qemu-result` (qemu 11.0.0),
  `/nix/store/zp51g43pr03sisri6xs1nyba6j2ad5kc-OVMF-202602-fd` (OVMF).

## Key learnings vs the broken qemu-vm.nix attempt

- `nixos-generators` `qcow-efi` builds a genuine writable qcow2 via
  `make-disk-image.nix` — root and store are real ext4 on the disk image,
  with `autoResize`/`growPartition` filling the 24 GiB. No ro store, no
  2.4 GiB cap, no 9p share by default.
- Two non-obvious overrides were required:
  1. Bootloader: the format ships GRUB-EFI; switch to systemd-boot with
     `boot.loader.grub.enable = lib.mkForce false` + `systemd-boot.enable`.
  2. Writable store: NixOS 26.11 **removed `boot.readOnlyNixStore`**; the
     store is re-bind-mounted ro via `boot.nixStoreMountOpts` default
     `[ "ro" "nodev" "nosuid" ]`. Set it to `[ "rw" "nodev" "nosuid" ]`.
     (The first build had a ro store for exactly this reason.)
