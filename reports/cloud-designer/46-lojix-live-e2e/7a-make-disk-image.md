# 46 · 7a — deploy-target VM via `make-disk-image` (genuine writable qcow2)

**Verdict: PASS.** A real NixOS qcow2 disk image — built with nixpkgs'
`nixos/lib/make-disk-image.nix`, booted under qemu/KVM + OVMF UEFI on
Prometheus — boots via systemd-boot, runs sshd with the runner key, and
presents a **genuinely read-write `/nix/store` on a 20 GiB virtual disk with
17 GiB free**. This replaces the broken `qemu-vm.nix` attempt (file 6), whose
`vmWithBootLoader` baked a read-only 2.4 GB store.

All work is user-level under `/tmp/lojix-e2e/diskA` on Prometheus; the host's
own config/networking was never touched. The pre-existing VM on host port 2222
(pid 1862127) stayed up the whole time; this candidate used a distinct name
(`diskA`) and port (2223).

## Why `make-disk-image` instead of `qemu-vm.nix`

`qemu-vm.nix` / `vmWithBootLoader` synthesizes the disk at boot from a fixed,
read-only store image and ignores `virtualisation.diskSize` /
`writableStore` for the store — so a deploy `nix copy` cannot write paths.
`make-disk-image.nix` instead **partitions and populates a real qcow2 ahead of
time**: a GPT disk with an ESP (vfat) and an ext4 root the store lives on. The
root is an ordinary read-write partition; the only extra knob a deploy target
needs is `boot.readOnlyNixStore = false` (see "Decisive fix" below).

## The flake

`/tmp/lojix-e2e/diskA/flake.nix` — pinned `nixpkgs nixos-25.05`
(rev `ac62194c…`, reusing the existing `vm-target/flake.lock`). Shape:

- `nixosConfigurations.target` — minimal NixOS importing
  `profiles/qemu-guest.nix`; `boot.loader.systemd-boot.enable = true`;
  `fileSystems."/"` = `/dev/disk/by-label/nixos-root` ext4 `autoResize`,
  `fileSystems."/boot"` = `/dev/disk/by-label/ESP` vfat; `boot.growPartition`;
  **`boot.readOnlyNixStore = false`**; openssh + root authorized key (the
  `/tmp/lojix-e2e/runner_key.pub` ed25519, read off Prometheus and baked in);
  `networking.useDHCP`; firewall off; `console=ttyS0` for host-visible boot.
- `packages.x86_64-linux.diskImage` — `import
  (nixpkgs + "/nixos/lib/make-disk-image.nix")` with `format = "qcow2"`,
  `partitionTableType = "efi"`, `diskSize = 20480`, `installBootLoader = true`,
  `touchEFIVars = false`, `label = "nixos-root"`.

## Build (on Prometheus)

```
cd /tmp/lojix-e2e/diskA
nix --extra-experimental-features "nix-command flakes" \
  build ".#packages.x86_64-linux.diskImage" \
  --print-out-paths -o /tmp/lojix-e2e/diskA/result-img
```

Output: `/nix/store/79zmy1pwx9c08il6da2vml33gdalz5w6-nixos-disk-image/nixos.qcow2`
— a qcow2 with **virtual size 20 GiB**, ~2 GiB allocated, store-read-only.
(Note: keep the flake dir clean of stray files — a leftover unix
`serial.sock` made one path-flake eval fail with "unsupported type".)

## Writable-disk preparation

The store-built qcow2 is read-only and immutable. Make a writable boot disk by
copying it out of the store and clearing the read-only bit; also stage a
writable OVMF VARS so UEFI can persist boot vars:

```
SRC=/nix/store/79zmy1pwx9c08il6da2vml33gdalz5w6-nixos-disk-image/nixos.qcow2
cp "$SRC" /tmp/lojix-e2e/diskA/disk.qcow2 && chmod +w /tmp/lojix-e2e/diskA/disk.qcow2
OVMF=$(nix … eval --raw nixpkgs#OVMF.fd.outPath)   # …ffhsz0zg…-OVMF-202602-fd
cp "$OVMF/FV/OVMF_VARS.fd" /tmp/lojix-e2e/diskA/OVMF_VARS.diskA.fd
chmod +w /tmp/lojix-e2e/diskA/OVMF_VARS.diskA.fd
```

The copy is a real read-write qcow2 (`qemu-img info` → file format qcow2,
virtual size 20 GiB); it grows on use, confirming live writes land on disk.

## Exact qemu boot command

`/tmp/lojix-e2e/diskA/boot-diskA.sh` (qemu 10.2.2, OVMF-202602):

```
$QEMU/bin/qemu-system-x86_64 \
  -name diskA -machine q35,accel=kvm -cpu host -smp 4 -m 4096 -nographic \
  -drive if=pflash,format=raw,readonly=on,file=$OVMF/FV/OVMF_CODE.fd \
  -drive if=pflash,format=raw,file=/tmp/lojix-e2e/diskA/OVMF_VARS.diskA.fd \
  -drive file=/tmp/lojix-e2e/diskA/disk.qcow2,if=virtio,format=qcow2 \
  -netdev user,id=net0,hostfwd=tcp:127.0.0.1:2223-:22 \
  -device virtio-net-pci,netdev=net0 \
  -serial file:/tmp/lojix-e2e/diskA/serial.log -monitor none
```

Boot proceeds: OVMF UEFI → systemd-boot menu (`NixOS` entry) → kernel 6.12.63
→ `Welcome to NixOS 25.05 … ttyS0` → sshd up on the qemu user-net lease
`10.0.2.15/24` (`enp0s2`). Reach it from Prometheus loopback:

```
ssh -i /tmp/lojix-e2e/runner_key -p 2223 \
  -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@127.0.0.1
```

## Verification (all PASS, captured live)

| Check | Result |
|---|---|
| SSH login (runner key, root) | OK — `uname` `Linux nixos 6.12.63 … x86_64` |
| `mount \| grep /nix/store` | **no separate store mount** (count 0); store lives on the rw root `/dev/vda2 … (rw,relatime)` — **not ro** |
| `touch /nix/store/.rwtest && rm …` | `STORE-RW-OK` |
| 50 MB write into `/nix/store` | `WROTE-50MB` then `CLEANED` — multi-GB `nix copy` will fit + write |
| `df -h /nix/store` | 20G size, **17G avail** (11% used) — ≥15 GiB headroom met |
| `lsblk` | real disk: `vda` 20G → `vda1` 249M vfat `/boot` + `vda2` 19.7G ext4 `/` (no 9p, no overlay) |
| `bootctl status` | systemd-boot 257.10 under UEFI 2.70 (EDK II); ESP entry `nixos-generation-1.conf` |
| `readlink /run/current-system` | `/nix/store/m8kbkgs5assasgv7fysrl48zvgs1xlk0-nixos-system-nixos-25.05.20260102.ac62194` |

## Decisive fix vs first boot attempts

1. First two builds left the store read-only: `make-disk-image` gives a
   writable ext4 root, but NixOS's default `boot.readOnlyNixStore = true`
   bind-mounts `/nix/store` **ro** over that rw partition. Symptom:
   `/dev/vda2 on /nix/store … (ro,relatime)` and `STORE-RW-FAIL`. Setting
   **`boot.readOnlyNixStore = false`** removes the bind mount; the store is
   then simply the rw root. This is the one config change a deploy target
   needs beyond a plain make-disk-image NixOS.
2. The early "sshd unreachable" scare was a host-side false negative: a
   serial-console login proved sshd was `active` and listening on
   `0.0.0.0:22` inside the guest with the network up; a direct
   `qemu-img`/`ss` check showed qemu listening on `127.0.0.1:2223` and a real
   TCP connect succeeded. The `(echo > /dev/tcp/…)` probe under the remote
   shell raced; an actual `ssh` handshake is the reliable readiness gate.

## Teardown

Test VM stopped (`kill` the `diskA` qemu pid); host port 2223 closed
afterward; the unrelated VM on 2222 untouched. Reusable artifacts left in
`/tmp/lojix-e2e/diskA/`: `flake.nix`, `flake.lock`, `boot-diskA.sh`,
`disk.qcow2`, `OVMF_VARS.diskA.fd`, build/serial logs.

## Use as the S5 deploy target

Boot `boot-diskA.sh` (or its 2222-free port of choice), wait for the ssh
handshake, point the lojix daemon's `ssh-ng://root@127.0.0.1:2223` target at
it. The store is writable with 17 GiB free, so the `nix copy` half that
stalled in file 6 will land; `bootctl` + a real ESP make `BootOnce` /
switch-to-configuration meaningful.
