# 48 · Unit C live e2e — synthesis + findings (2026-06-13)

Two phases: a drive agent ran the live deploy on Prometheus; an independent
adversarial verifier SSHed in and checked ground truth. The verifier corrected
two overstatements in the drive report — recorded honestly below. The drive
agent's running log is `1-execution-log.md`.

## Proven live (verifier-confirmed)

- **Real writable-disk KVM microVM.** mercury runs as a genuine KVM microVM
  (4 hardware vcpus, `cpu host`, `systemd-detect-virt=kvm`) with a writable
  40 GiB ext4 root **and** a writable `/nix/store` overlay. **The S5
  read-only-store failure mode is ABSENT** — the whole reason for a
  horizon-modeled node. The deployed OS closure (865 paths) landed valid on
  mercury's writable store.
- **Deploy pipeline build→copy→register, live + daemon-driven.** The daemon ran
  `nix eval` → `nix build` (a real `nixos-system-mercury`) → `nix copy` into
  mercury's store → `nix-env --set` (system profile generation 1 → the deployed
  closure). The effects match the daemon's own typed command construction (not a
  hand-run script).
- **Prometheus untouched (`5hir5bnz` upheld).** The tap + guest IP + route live
  ONLY in a private user network namespace (`unshare -rn`, no sudo); the host
  netns is identical pre/post (the LargeAiRouter's interfaces/routes intact), and
  the host cannot even reach the guest. The only host change was one line
  appended to li's own `~/.ssh/config`.

## NOT proven — two honest gaps (verifier)

- **Activation did not complete.** `/run/current-system` still points at
  mercury's original boot system. `switch-to-configuration` FAILED at the
  bootloader step ("Not booted with EFI"; `/boot` empty; no BootOnce). Only
  copy + profile-register happened — the running OS was not switched.
- **Live disconnect-survival timeline not freshly evidenced.** The drive
  report's strong ~55 s post-disconnect window (client exit 17:35:13, effects
  17:35:16–17:36:09) belongs to an earlier run that a 17:39–17:40 re-run
  destroyed. The surviving run shows only a ~1 s submit-to-effect gap with no
  captured client-death timestamp. The survival ARCHITECTURE is real (S4b
  daemon-lifetime `DeployJobs` actor; a durable SEMA deploy-job record exists,
  committed at deploy conclusion) and the effects are daemon-driven — but the
  "completed after the client died" claim is not independently proven on
  surviving artifacts.

## Findings (high value)

1. **Real lojix daemon bug — caught live, fixed, must land in lojix.**
   `nix build <drv> --print-out-paths` prints the **.drv**, not the realised
   output, on nix 2.4+. So the daemon copied/activated the *.drv* — **without the
   fix the daemon can never activate a deploy.** Patched to `<drv>^*` (select all
   outputs); the corrected build is what landed a real closure on mercury. This
   is the single most valuable thing the live run produced — unit tests and the
   S5 run (which stopped at *build*) never reached the activation path that
   exposes it.
2. **Substrate ↔ EFI mismatch (architectural).** A lean `microvm.nix` guest
   direct-boots the kernel and has **no UEFI/ESP**, so the EFI
   bootloader-install / BootOnce step — part of production-parity activation, and
   exactly how a real node boots — **cannot run on it**. The UEFI alternative
   (`make-disk-image` + OVMF, S5-proven) is blocked here by a `cptofs` OOM (env
   tooling, not lojix). To test full activation/BootOnce faithfully, the test VM
   must boot via **UEFI (q35 + OVMF)**, not the lean `-M microvm` machine type.
3. **CriomOS lean-guest-on-microvm gaps** surfaced (clavifaber forced build; NSS
   disabled → sshd "invalid user"; guest-IP/NIC-match) — fold into Unit B
   hardening alongside the networkd-ordering note from report 47.

## Follow-ups

- **Land the daemon `<drv>^*` fix in lojix** (in flight; commit→review→push main).
- **Decide the EFI substrate** for the full-activation + faithful-deploy test
  (a UEFI VM), then do **one clean instrumented run** that captures the
  client-death timestamp + the decoded durable job terminal state — nailing both
  activation and disconnect survival in a single inspectable run.
- Resolve the `cptofs` OOM (UEFI image build) for that substrate.
- Fold the CriomOS lean-guest gaps + the networkd-ordering note into Unit B.

## Bottom line

The substrate goal is met (a real, writable-disk, horizon-modeled microVM — S5's
blocker gone), the deploy pipeline is proven live through generation-register,
Prometheus is untouched, and the live run paid for itself by catching a
deploy-blocking daemon bug. The EFI activation and a clean disconnect-survival
timeline remain to be nailed on a UEFI substrate.
