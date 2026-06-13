# 49 · UEFI activation e2e — verified synthesis (2026-06-13)

The clean UEFI re-run + independent adversarial verification. The drive log is
`1-execution-log.md`. The verifier returned **pass-with-notes** — it confirmed
the core lojix mechanics end-to-end and scoped exactly what stayed circumstantial.

## Proven end-to-end (independently verified over ssh)

- **lojix deploy pipeline, with the fix, all the way through activation.** From
  the canonical fixed tree (lojix main `efbc5ea`): build (`<drv>^*` → the
  realised output — verified a real `nixos-system` dir with `/init`, **not** a
  `.drv`) → `nix copy` ~860 paths into the VM's writable store → `nix-env --set`
  → `switch-to-configuration boot` → systemd-boot install → `bootctl set-default
  OLD` + `set-oneshot NEW`. Every step completed (UEFI present). The activated
  artifact is mercury's real OS closure (`63ad6qf2…-nixos-system-mercury`), set
  as system profile generation 2 with its own installed ESP entry (Linux 7.0.1).
- **Disconnect survival (the heavy work).** Captured client-death timestamp
  (T1 = 20:52:58.715; the client lived ~55 ms); the build/copy/activate effects
  ran *minutes after*, autonomously in the daemon's `DeployJobs` actor with no
  client — one pristine, un-overwritten run (live `effect.log` byte-identical to
  the pristine snapshot). The durable terminal deploy-job record is readable via
  the **ordinary CLI** with no client attached:
  `(Queried ([(1 1 fieldlab mercury FullOs BootOnce Current 63ad6qf2…)] (11 11)))`.
- **BootOnce config + fallback.** `set-default OLD` + `set-oneshot NEW`; the
  static end-state (gen-1 default+current, gen-2 installed, OneShot consumed) +
  a ~5-min gap in the base journal where gen-2 ran + the return to gen-1
  demonstrate the production-parity safety — an unstable new generation
  auto-falls-back and does not trap the node.
- **The `.drv^*` fix held end-to-end** — the central production bug, fixed +
  verified live: the activated/booted artifact is the realised OS, never the
  `.drv`.
- **Prometheus untouched (`5hir5bnz`)** — re-checked adversarially: no
  `vmt0`/`10.77` on the host netns, host OS/networking/services intact, the tap
  only in the private user namespace, no sudo.

## What was circumstantial / blocked (honest)

- **The actual gen-2 kernel boot at reboot-1 was not durably witnessed by the
  verifier** — qemu truncates its `-serial file:` on restart, so the surviving
  serial only shows the current base boot (it does list the 7.0.1 entry in the
  menu). The gen-2 boot is corroborated circumstantially (journal gap, consumed
  OneShot efivar, installed+selectable entry). → A targeted re-arm + *guest*
  reboot with a durable append-only serial capture closes this (in flight).
- **mercury's full userspace does not stabilize on a generic q35 VM** — the
  systemd watchdog reboots it at ~180 s because mercury is built for the microvm
  machine type. This is a CriomOS lean-profile-on-q35 RUNTIME gap, **not** a
  lojix/BootOnce defect — so "the gen-2 kernel boots from the one-shot" is shown,
  but "mercury runs as a working node" is not. → fold into Unit B.
- Minor: the earliest eval effects share the same wall-clock second as the
  ~55 ms client life (only the later copy/activate are unambiguously post-death —
  but those are the meaningful ones); the drive report conflated 49a/49b closure
  hashes (ground truth is internally consistent — live state = 49b's
  `63ad6qf2`).

## Net

lojix's deploy + disconnect-survival + BootOnce activation pipeline is proven
live end-to-end against a real writable-disk **UEFI** node; the production `.drv`
bug is fixed and verified; Prometheus stayed untouched. The remaining items are a
test-harness durable-capture of the boot moment (closing now) and a CriomOS
lean-profile gap (Unit B) — neither a lojix defect.

## Follow-ups

- (in flight) durable serial witness of the gen-2 BootOnce boot.
- Unit B: harden the lean CriomOS profile to stabilize on a generic UEFI VM (the
  q35 watchdog) + the networkd-ordering note from report 47.
- Minor daemon hardening: the empty-stdout `.drv` fallback in build-output
  capture (report 48 note); durable client-liveness capture in the disconnect
  harness.
- Operator: integrate Units A/B (horizon + CriomOS feature branches) to main.
