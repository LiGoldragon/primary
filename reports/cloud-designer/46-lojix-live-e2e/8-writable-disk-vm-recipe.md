# 46 · 8 — Writable-disk deploy-target VM: the winning recipe

Synthesis of candidates 7a (`make-disk-image`) and 7b (`nixos-generators`).
Both were re-booted from scratch and re-verified live on Prometheus for this
report; the winner is now running detached on host port 2222 (the
`dune.fieldlab.criome` ssh alias) ready for the daemon's copy + BootOnce
activation.

## Winner: `make-disk-image` (candidate 7a, diskA)

Both candidates EMPIRICALLY PASSED every gate — writable `/nix/store`,
>=15 GiB free, real systemd-boot UEFI, ssh-as-root with the throwaway key.
diskA wins on deploy-target merits, not on capability:

| Axis | diskA (make-disk-image) | diskB (nixos-generators) |
|---|---|---|
| Channel | **nixos-25.05 (stable)** | nixos-unstable (26.11) |
| Flake inputs | **nixpkgs only** | nixpkgs + nixos-generators |
| Store-rw mechanism | `boot.readOnlyNixStore = false` (no bind) | `boot.nixStoreMountOpts = ["rw" ...]` (rw bind) |
| Disk / free | 20 GiB / **17 GiB** | 24 GiB / 20 GiB |
| Kernel | 6.12.63 | 6.18.35 (brand-new) |
| systemd-boot | 257.10 | 260.1 |
| nix | 2.28.5 | 2.34.7 |

Decision: a deploy target wants the fewest moving parts and the most
predictable base. diskA rides the **stable** channel, has **one** flake input,
and uses the canonical minimal `make-disk-image` path. diskB rides unstable
(26.11), pulls a bleeding-edge kernel, adds a second flake input
(`nixos-generators`), and its store-rw override (`nixStoreMountOpts`) is the
fragile replacement for the `readOnlyNixStore` knob that unstable *removed* —
exactly the kind of release-churn surface a deploy target should not depend on.
Capability is identical; diskA is the lower-risk base. (If a >=24 GiB store or
a 26.11 toolchain is later required, diskB is a proven drop-in: same boot
command shape, swap the disk/OVMF/qemu paths.)

## Exact build command (on Prometheus)

Flake: `/tmp/lojix-e2e/diskA/flake.nix` — pinned `nixpkgs nixos-25.05`
(`flake.lock` rev `ac62194…`). Minimal NixOS: systemd-boot UEFI, sshd + baked
root key, ext4 root with `autoResize` + `boot.growPartition`,
`boot.readOnlyNixStore = false`. `packages.x86_64-linux.diskImage` imports
`nixpkgs/nixos/lib/make-disk-image.nix` with `format = "qcow2"`,
`partitionTableType = "efi"`, `diskSize = 20480`, `installBootLoader = true`,
`touchEFIVars = false`, `label = "nixos-root"`.

```
cd /tmp/lojix-e2e/diskA
nix --extra-experimental-features "nix-command flakes" \
  build ".#packages.x86_64-linux.diskImage" \
  --print-out-paths -o /tmp/lojix-e2e/diskA/result-img
```

Output (read-only, immutable):
`/nix/store/79zmy1pwx9c08il6da2vml33gdalz5w6-nixos-disk-image/nixos.qcow2`
— qcow2, virtual size 20 GiB, ~2.1 GiB allocated.
Keep the flake dir free of stray sockets (a leftover `serial.sock` once made a
path-flake eval fail "unsupported type").

## Writable-disk preparation

The store qcow2 is read-only; make a fresh writable working copy plus a
writable OVMF NVRAM (reflink keeps it cheap; the file grows on guest writes,
proving real on-disk writes):

```
cd /tmp/lojix-e2e/diskA
SRC=/nix/store/79zmy1pwx9c08il6da2vml33gdalz5w6-nixos-disk-image/nixos.qcow2
cp --reflink=auto "$SRC" /tmp/lojix-e2e/diskA/deploy.qcow2
chmod u+w /tmp/lojix-e2e/diskA/deploy.qcow2
cp /nix/store/ffhsz0zgnbddqi9zb1jabs1h4p82mwv2-OVMF-202602-fd/FV/OVMF_VARS.fd \
   /tmp/lojix-e2e/diskA/OVMF_VARS.deploy.fd
chmod u+w /tmp/lojix-e2e/diskA/OVMF_VARS.deploy.fd
```

## Exact qemu boot command (KVM + OVMF UEFI + hostfwd 2222)

Saved as `/tmp/lojix-e2e/diskA/boot-target-2222.sh` and launched detached.
qemu 10.2.2, OVMF-202602. `hostfwd=tcp:127.0.0.1:2222-:22` is exactly what the
`dune.fieldlab.criome` alias targets (HostName 127.0.0.1, Port 2222, User root,
IdentityFile `/tmp/lojix-e2e/runner_key`).

```
QEMU=/nix/store/7yf84vnnsnvdi7r8g2grfpafnq17mp8y-qemu-10.2.2/bin/qemu-system-x86_64
OVMF=/nix/store/ffhsz0zgnbddqi9zb1jabs1h4p82mwv2-OVMF-202602-fd
DIR=/tmp/lojix-e2e/diskA
"$QEMU" \
  -name lojix-target -machine q35,accel=kvm -cpu host -smp 4 -m 4096 -nographic \
  -drive if=pflash,format=raw,readonly=on,file="$OVMF/FV/OVMF_CODE.fd" \
  -drive if=pflash,format=raw,file="$DIR/OVMF_VARS.deploy.fd" \
  -drive file="$DIR/deploy.qcow2",if=virtio,format=qcow2 \
  -netdev user,id=net0,hostfwd=tcp:127.0.0.1:2222-:22 \
  -device virtio-net-pci,netdev=net0 \
  -serial file:"$DIR/serial.deploy.log" -monitor none
```

Detached launch (re-invokable; survives the launching shell):

```
setsid /tmp/lojix-e2e/diskA/boot-target-2222.sh </dev/null \
  >/tmp/lojix-e2e/diskA/qemu.deploy.out 2>&1 &
```

Boot path: OVMF UEFI → systemd-boot menu (`NixOS` entry, 1 s timeout) →
kernel 6.12.63 → sshd on the qemu user-net lease. ssh handshake (not a
`/dev/tcp` probe) is the reliable readiness gate; it comes up ~12 s after
launch.

## Verification — re-run live for this report (all PASS)

Booted fresh on port 2222 and probed via the `dune.fieldlab.criome` alias:

| Check | Result |
|---|---|
| ssh root via alias (runner key) | `ALIAS-OK Linux 6.12.63` |
| store mount | NO separate `/nix/store` mount; store on rw root `/dev/disk/by-label/nixos-root / ext4 rw,relatime` — **not ro** |
| `touch /nix/store/.rwtest` | **STORE-RW-OK** |
| 1 GiB `dd` into `/nix/store` | **WROTE-1GiB** then CLEANED (host `deploy.qcow2` grows = real disk writes) |
| `df -h /nix/store` | 20G size, **17G avail** (11% used) — >=15 GiB met |
| `lsblk` | real disk: `vda` 20G → `vda1` 249M vfat `/boot` + `vda2` 19.7G ext4 `/` (no 9p, no overlay) |
| `bootctl is-installed` | `yes` (rc 0) |
| `bootctl status` | systemd-boot 257.10, UEFI 2.70 (EDK II), Boot counting feature present |
| `bootctl set-oneshot <entry>` | **rc 0**; `LoaderEntryOneShot-4a67b082-…` efivar written (52 bytes UTF-16); `set-oneshot ""` clears it rc 0 |
| efivarfs | `efivarfs on /sys/firmware/efi/efivars (rw,…)` — runtime-writable despite build-time `canTouchEfiVariables = false` |
| `readlink /run/current-system` | `/nix/store/m8kbkgs5…-nixos-system-nixos-25.05.20260102.ac62194` |
| `nix-store --version` | 2.28.5 (writable store for `nix copy`) |

diskB was independently re-verified on port 2224 with identical PASS results
(store rw bind on `/dev/vda2`, 20 GiB free, bootctl 260.1, ssh OK) before being
stopped — it is a proven fallback.

## Current live state on Prometheus

- The broken `qemu-vm.nix` squatter that previously held port 2222
  (pid 1862127, the 9p-virtfs VM over a 6 MB `target.qcow2`) was **stopped**.
- The diskA winner is **running now** on `127.0.0.1:2222` (the
  `dune.fieldlab.criome` alias), writable store with 17 GiB free, sshd live.
- Reusable artifacts in `/tmp/lojix-e2e/diskA/`: `flake.nix`, `flake.lock`,
  `boot-target-2222.sh`, `deploy.qcow2` (writable, in use),
  `OVMF_VARS.deploy.fd`, `serial.deploy.log`. The original `boot-diskA.sh`
  (port 2223) is kept for side-by-side testing.

## Caveats for the real deploy

- **deploy.qcow2 is single-use state.** Each `nix copy` + BootOnce run mutates
  it. To re-run from a clean slate, kill the VM and re-`cp --reflink=auto` from
  the read-only store image (the prep step), then re-launch.
- **One VM per port.** Only one qemu may bind 2222. If a deploy run leaves a VM
  up, `pgrep -af 'name lojix-target'` and `kill` before relaunching, or the new
  boot silently fails to bind hostfwd.
- **BootOnce reconcile is real.** `bootctl set-oneshot` writes the
  `LoaderEntryOneShot` efivar at runtime even though the image was built with
  `canTouchEfiVariables = false` (that flag only governs image-build-time efivar
  touching; efivarfs is mounted rw at runtime). The daemon's BootOnce path will
  work.
- **Stable channel = stable nix.** Guest nix is 2.28.5; if the daemon pushes
  paths built by a newer nix with a store-format or signature expectation,
  confirm wire compatibility. `nix copy` over `ssh-ng://` is fine here.
- **`touchEFIVars = false` + `installBootLoader = true`** is the right combo:
  systemd-boot is baked into the ESP at build time (so `bootctl is-installed`
  is `yes` on first boot) without needing host efivars during the image build.
- **Serial log is the boot oracle.** If ssh doesn't come up, read
  `/tmp/lojix-e2e/diskA/serial.deploy.log` — it carries kernel + systemd console
  (`console=ttyS0,115200`).

## Readiness

Ready. The winner is already booted on the `dune.fieldlab.criome` alias
(127.0.0.1:2222) with a writable 17 GiB-free store, working systemd-boot, and
proven BootOnce — point the lojix daemon's `ssh-ng://root@127.0.0.1:2222`
(or `root@dune.fieldlab.criome`) target at it and run the copy + activation.
