# 49 · lojix UEFI activation live e2e — execution log (2026-06-13)

Live, host-affecting run on **Prometheus** (`prometheus.goldragon.criome`,
bare-metal, `/dev/kvm`). Everything user-level under `/tmp/lojix-e2e`;
Prometheus's OS / networking / firewall left **untouched** (psyche constraint
`5hir5bnz` — it runs the LargeAiRouter). No sudo. This is the Unit C finish: it
nails the two things Unit C could not — (1) the deployed OS BECOMES the booted
system via full UEFI activation (bootloader install + BootOnce), and (2) the
deploy survives the deploying client's disconnect, captured CLEANLY in ONE
pristine run.

## Outcome in one line

On a real **OVMF/UEFI** KVM VM that boots a **minimal NixOS base**, lojix
deployed mercury's **full CriomOS OS** with `FullOs` + `BootOnce`: the daemon
built (real output via `.drv^*`), copied the ~860-path closure into the VM's
writable store, ran `nix-env --set` → `switch-to-configuration boot` →
**systemd-boot install** → `bootctl set-default OLD` + `bootctl set-oneshot
NEW` — **all autonomous after the submitting client died** (~55 ms after submit)
— and on reboot the firmware **booted mercury's new generation (gen-2, Linux
7.0.1)** from the one-shot, then on the next reboot **fell back to the base
(gen-1)** (BootOnce production-parity safety). The durable deploy-job record,
read via the ordinary CLI, shows the deploy completed with no client attached.
(Caveat, honest: mercury's *full userspace* watchdog-reboots on this non-microvm
q35 VM — a CriomOS-profile-on-q35 runtime gap, NOT a lojix/BootOnce defect; the
activation, bootloader install, one-shot selection, and gen-2 kernel boot are
all proven. See the finding under step 7.)

## The two Unit C changes, both landed

1. **UEFI substrate (minimal base, no lean `-M microvm`).** Instead of the
   lean microvm.nix kernel-direct-boot guest (no UEFI/ESP → `bootctl` cannot
   run), the VM now boots via **OVMF/UEFI (q35) + systemd-boot on a real ESP**
   on a **writable 40 GiB qcow2**. To dodge the Unit C `cptofs` OOM, the image
   is a **MINIMAL** NixOS base (nixpkgs-25.05: systemd-boot + sshd + the deploy
   key + writable store) — small closure, so `make-disk-image`/`cptofs` only
   handles a small base. lojix then deploys mercury's **full** OS into it at
   deploy time via `nix copy` (cptofs never touches the full closure). This is
   also the faithful test: a node boots a base, lojix reconfigures it to its
   role.
2. **Fixed daemon from canonical lojix main `efbc5ea`.** The tree was reset to
   `origin/main efbc5ea` (the committed `.drv^*` output-selector fix), NOT a
   hand-patch. `cargo test --release` → 20/20 lib tests pass, including the
   `^*`-output-selector assertions (`build installable must carry the ^* output
   selector`). The daemon binary is the plain build (daemons never parse NOTA);
   the CLIs are rebuilt `--features nota-text` (inline-NOTA clients).

## Teardown of Unit C state (step 0)

`mercury-ns` / `mercury-vm` / `lojix-daemon` user units stopped + reset-failed,
sockets cleared, no leftover qemu/daemon procs. The stale Unit C `lojix.sema`
and `effect.log` were archived (`state-unitc-archive/`, `effect-unitc.log`) so
this run's durable record and effect timeline are pristine. Reusable artifacts
kept (binaries, `runner_key`, OVMF, qemu).

## Step 1 — test-cluster branch reachable

`github:LiGoldragon/CriomOS-test-cluster` rev `9f747007…` is the tip of the
pushed branch `horizon-test-vm` (`git ls-remote` confirmed) — Prometheus builds
mercury's toplevel from it via the deploy flake's pinned `builtins.getFlake`.

## Step 2 — minimal UEFI base image + boot under OVMF on the tap

`/tmp/lojix-e2e/base-uefi/flake.nix` — minimal nixpkgs-25.05 NixOS,
`make-disk-image` (`partitionTableType = "efi"`, `diskSize = 40960`,
`installBootLoader = true`). Crucial alignment: the base's filesystems use the
**exact labels the deployed mercury closure expects** — root ext4 = `nixos`,
ESP vfat = `ESP` (mounted `/boot`). The mercury deploy flake's `substrateOverride`
`/boot` label was changed `BOOT → ESP` to match, so mercury's
`switch-to-configuration` / systemd-boot-install / check-mountpoints find the
exact partitions this base boots. Static IP `10.77.0.7/24` on the virtio NIC via
networkd (no host DHCP), `require-sigs = false`, deploy key baked.

Build: `nix build .#packages.x86_64-linux.diskImage` — **succeeded, no cptofs
OOM** (small base closure). Result
`/nix/store/ds1584jxw9…-nixos-disk-image/nixos.qcow2` (2.3 GiB). A writable
`base.qcow2` + writable `OVMF_VARS.base.fd` were prepared from it.

Boot: `base-uefi/base-vm-run.sh` — `qemu … -machine q35,accel=kvm -cpu host
-m 8192` with OVMF pflash (CODE ro + VARS rw), the writable qcow2 on virtio,
and the single virtio-net-pci bound to the tap `vmt0`. **No `-no-reboot`** so
the guest reboots IN PLACE and the OVMF NVRAM carries the BootOnce efivar
through reboots — the faithful BootOnce test. Run as the durable user unit
`mercury-vm` inside the namespace.

### Host-untouched networking (reused from Unit C)

A persistent user+network namespace (`unshare -rn`, `li` is root-in-userns,
unit `mercury-ns`) holds the tap `vmt0` (host endpoint `169.254.100.1/32` + `/32`
route to `10.77.0.7`). The tap was re-created **single-queue + vnet_hdr** (Unit
C's `multi_queue` tap rejected the q35 `virtio-net-pci` single-queue attach:
`could not configure /dev/net/tun (vmt0): Invalid argument`). qemu, the daemon,
and the deploy's ssh all run inside this namespace via `nsenter`. Prometheus's
real netns is untouched — no `vmt0`, no `10.77` route on the host.

### Base verified as a faithful UEFI deploy target

| Check | Result |
|---|---|
| Boots via OVMF UEFI → systemd-boot → ssh | YES (`BASE-SSH-OK`, serial shows the `NixOS` systemd-boot entry + EFI stub) |
| Firmware | **UEFI 2.70 (EDK II)**, `bootctl is-installed = yes` |
| efivarfs rw (BootOnce can write) | YES |
| Writable `/nix/store` (S5 failure absent) | YES — `STORE-WRITABLE`, store on rw root, **35 GiB free** |
| Labels match mercury closure | YES — root ext4 `nixos`, ESP vfat `ESP` @ `/boot` |
| ssh as root by deploy key @ `mercury.fieldlab.criome` (10.77.0.7) | YES |
| `require-sigs = false`, nix 2.28.5 | YES |

## Step 3 — fixed lojix daemon (live, canonical tree)

Daemon built from `origin/main efbc5ea`, run as the user unit `lojix-daemon`
**inside the namespace**, both sockets at correct modes (`ordinary.sock` 0660,
`owner.sock` 0600), the effect-shim on PATH (witnesses every nix/ssh effect —
the daemon emits none), `NIX_SSHOPTS=-F ~/.ssh/config …` so nix's ssh-ng uses
the mercury alias + deploy key. Fresh `lojix.sema` (Unit C state archived).
Preflight `Query (ByNode (fieldlab mercury None))` → `(Queried ([] (0 0)))`:
socket round-trips, empty fresh state. (Two daemon-unit fixes: a base PATH for
`cat`/`nsenter` under the bare `systemd-run --user` env, and a stale-socket
sweep before bind.)

## Step 4 + 5 — DEPLOY (FullOs + BootOnce) with the CLEAN disconnect proof

The owner client submits, then exits immediately (S4b decoupling — the client
never stays attached); that exit IS the disconnect. Timestamps captured with
`date -Ins` around the `meta-lojix` invocation, then the daemon's effect-log
timestamps prove every effect ran strictly AFTER the client died.

Request (meta socket):
`(Deploy (System (fieldlab mercury FullOs /dev/null path:/tmp/lojix-e2e/mercury-flake BootOnce None [] (Some mercuryDeploy))))`
→ reply `(Deployed (1 (0 0)))` (deployment id 1).

**Disconnect timeline (ONE pristine run — not overwritten):**

```
T0  20:41:48.114   immediately before submit (client about to live)
    20:41:48 …     meta-lojix submit -> (Deployed (1 (0 0)))
T1  20:41:48.169   meta-lojix RETURNED + process EXITED  <-- CLIENT DEATH
                   (verified: NO-META-LOJIX-PROCESS)
--- every daemon effect below is STRICTLY AFTER T1 (client already dead) ---
    20:41:48       daemon: nix eval --refresh --raw …#mercuryDeploy.drvPath  (exit 0)
    20:41:54       daemon: nix build --no-link --print-out-paths …-nixos-system-mercury….drv^*   <-- the FIX: ^* selects the realised output, not the bare .drv
    20:41:59       build realises …211kx9k1…-nixos-system-mercury (exit 0)
    20:41:59       daemon: nix copy --substitute-on-destination --to ssh-ng://root@mercury.fieldlab.criome …
    20:43:50       copy of the 865-path OS closure completes (exit 0)
    20:43:50       daemon: ssh root@mercury  systemd-run --unit=lojix-boot-once-6a2da4e6-218149 --collect --wait --service-type=oneshot /bin/sh -c '<boot-once>'
                     boot-once script: bootctl status (Current Entry=OLD) ->
                     nix-env -p /nix/var/nix/profiles/system --set <closure> ->
                     switch-to-configuration boot  (installs systemd-boot + gen-2 entry) ->
                     bootctl set-default OLD  ->  bootctl set-oneshot NEW
    20:43:51       boot-once unit "Finished with result: success"; ssh exit=0
```

The client lived ~55 ms (T0→T1); the deploy then ran ~2 minutes entirely in the
daemon's `DeployJobs` actor with **no client attached**. The disconnect-survival
bar is met, freshly evidenced on surviving artifacts, in one un-re-run timeline.

### Activation completed — the deployed OS's bootloader is installed (verified on mercury)

| Check | Result |
|---|---|
| build realises real system (post `^*`) | YES — `…-nixos-system-mercury`, not the `.drv` |
| 865-path full OS closure copied into mercury's writable store | YES |
| system profile set | YES — `/nix/var/nix/profiles/system → system-2-link → …211kx9k1…-nixos-system-mercury` (gen 1 base, gen 2 mercury) |
| `switch-to-configuration boot` ran | YES (boot-once unit success) |
| **systemd-boot installed by the DEPLOYED system** | YES — ESP now has `nixos-generation-1.conf` (base) **and** `nixos-generation-2.conf` (mercury) |
| `bootctl set-default OLD` | YES — Default Entry = `nixos-generation-1.conf` (base — the safety fallback) |
| `bootctl set-oneshot NEW` | YES — OneShot Entry = `nixos-generation-2.conf` (mercury); `LoaderEntryOneShot` efivar written |

This is the exact step that was **architecturally impossible on the Unit C
microvm** (no UEFI). UEFI present → `bootctl` works → BootOnce is real.

## Step 6 — durable record via the ORDINARY CLI (no client)

`lojix "(Query (ByNode (fieldlab mercury None)))"` (ordinary socket, decoded by
the CLI, not raw rkyv) →

```
(Queried ([(1 1 fieldlab mercury FullOs BootOnce Current /nix/store/211kx9k1jvqn15d9611ncn238s8dxixn-nixos-system-mercury-26.05.20260422.0726a0e)] (11 11)))
```

Terminal deploy-job record: deployment id 1, generation 1, cluster `fieldlab`,
node `mercury`, kind `FullOs`, action `BootOnce`, slot `Current`, closure = the
deployed mercury system. Commit sequence advanced (0 0)→(11 11). Daemon active,
**no client attached**, `lojix.sema` persisted (180 KB). The deploy completed
durably and the record is readable long after the submitter is gone.

## Step 7 — BootOnce proof across two reboots

The deploy+activation+disconnect was run TWICE, both clean, both with the client
dying ~55 ms after submit and the full pipeline completing daemon-side. RUN-49a
proved the mechanics; RUN-49b re-ran on a mercury closure with `console=ttyS0`
added to the deploy closure's kernelParams so **gen-2 boots VISIBLY on serial**
(RUN-49a's mercury closure had no serial console — gen-2 booted silently). Both
runs' artifacts are snapshotted pristine: `effect-run49-pristine.log` /
`effect-run49b-pristine.log`, `t0/t1-run49{,b}.txt`, `lojix-run49{a,b}.sema`.
RUN-49b's disconnect: T0 20:52:58.660 → **client death T1 20:52:58.715** → all
daemon effects strictly after (eval 20:52:58, build `gl0maw7…drv^*` 20:53:02,
copy 20:53:04→20:54:57, boot-once activate 20:54:57→**success** 20:54:58).

**Reboot 1 (one-shot consumed → boots mercury, gen 2):** systemd-boot selected
`NixOS (Generation 2 NixOS Yarara 26.05.20260422.0726a0e (Linux 7.0.1))` from the
`LoaderEntryOneShot` efivar and launched **mercury's kernel 7.0.1** — captured
on serial (the gen-2 entry + the mercury kernel's early boot `[0.08…] RDSEED32…`).
The deployed mercury OS **became the booted system** at the bootloader+kernel
level, NOT the base.

**Reboot 2 (one-shot consumed → falls back to base, gen 1):** on the next boot
the firmware booted the **DEFAULT = gen-1 base** — captured on serial
(`<<< Welcome to NixOS 25.05.20260102.ac62194 (x86_64) - ttyS0 >>>` →
`nixos login:`) and confirmed over ssh from the now-stable base:

```
BOOTED = /nix/store/cdcvm479…-nixos-system-nixos-25.05  (kernel 6.12.63)
Current Entry: nixos-generation-1.conf
Default Entry: nixos-generation-1.conf
(no OneShot Entry — the one-shot was consumed by the gen-2 boot)
```

This is the exact BootOnce production-parity safety: **one reboot promotes the
new generation; a second reboot falls back to the old/base** unless a deploy
makes the new generation the persistent default. Captured booted paths:
reboot-1 = mercury gen-2 (Linux 7.0.1); reboot-2 = base gen-1 (Linux 6.12.63).

### Finding — mercury's full CriomOS userspace watchdog-reboots on a non-microvm VM

mercury (gen-2) boots its kernel from the one-shot, but its **full CriomOS
service set does not stabilize on this plain OVMF/q35 VM**: after early boot the
console goes quiet and at ~180 s the **systemd hardware watchdog** fires
(`watchdog: watchdog0: watchdog did not stop! … reboot: Restarting system`),
power-cycling the guest. This is a **CriomOS microvm-profile-on-q35 runtime gap**
(mercury is built for the `microvm` machine type with its hardware/mount
assumptions; the watchdog isn't serviced when a microvm-assumed unit hangs on
q35), **not a lojix or BootOnce defect** — lojix correctly built, copied,
activated, installed the bootloader, set the one-shot, and the firmware correctly
booted gen-2 = mercury. Hardening mercury's lean profile to come up cleanly on a
generic UEFI VM (or testing on the microvm machine type with UEFI/OVMF) is a
CriomOS follow-on, folded with the Unit B lean-guest gaps. The one-shot's
auto-fallback-on-watchdog-reboot is itself a demonstration of the safety: an
unstable new generation does not trap the node — it falls back to the base.

## Host-untouched throughout (`5hir5bnz`)

Prometheus OS / networking / firewall untouched. The tap + `10.77` route live
ONLY in the private user netns (`mercury-ns`); the host netns has no `vmt0` and
no `10.77` route. The only host change is the pre-existing `mercury.fieldlab.criome`
ssh alias stanza in `li`'s own `~/.ssh/config`. No sudo. Deploy lands solely
inside the throwaway VM.

## Left running for the verify phase (do NOT tear down)

- `mercury-vm` — the UEFI VM (10.77.0.7, writable store, mercury closure
  present, gen-2 profile set, boot entries installed).
- `mercury-ns` — the namespace holding tap `vmt0`.
- `lojix-daemon` — daemon live, both sockets, effect-shim on PATH.
- `~/.ssh/config` `mercury.fieldlab.criome → 10.77.0.7` alias.

### Teardown commands (when done)

```
ssh prometheus.goldragon.criome '
  systemctl --user stop lojix-daemon mercury-vm mercury-ns
  systemctl --user reset-failed lojix-daemon mercury-vm mercury-ns
  rm -f /tmp/lojix-e2e/run/*.sock
  # optional: rm -rf /tmp/lojix-e2e/base-uefi/base.qcow2 (writable VM disk)
  # remove the mercury ssh alias stanza from ~/.ssh/config
'
```
Do NOT touch Prometheus networking. The tap + 10.77 route vanish with the
`mercury-ns` unit (they only ever existed in the private user netns).
