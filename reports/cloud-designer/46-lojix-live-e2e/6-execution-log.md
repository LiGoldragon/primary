# 46 · S5 live e2e — execution log (2026-06-13)

Executing the runbook (file 5) on Prometheus. Everything user-level under
`/tmp/lojix-e2e`; Prometheus's own config/networking untouched throughout.

## What landed (proven live)

- **Preflight + harness:** Prometheus ready (KVM writable, 681 GiB free, system
  running); throwaway deploy key; ssh alias `root@dune.fieldlab.criome` →
  qemu hostfwd `127.0.0.1:2222`.
- **VM up:** a throwaway NixOS 25.05 qemu guest with a real systemd-boot ESP,
  ssh-reachable, distinct from the host (baseline generation captured).
- **lojix built + ran live on Prometheus:** release binaries (rustc 1.95);
  `lojix-write-configuration` wrote the rkyv startup; `lojix-daemon` ran as a
  user unit with both authority-tiered sockets at correct modes (0660/0600).
- **Deploy pipeline's BUILD half proven on the daemon:** a `Build` deploy made
  the daemon run a **real ~6-minute `nix` build (885 MB peak)** and produce the
  full dune OS closure (`/nix/store/…-nixos-system-dune-26.05`). Resolve→eval→
  build works end to end on the actual daemon against a real flake, with the
  two-CLI + job-actor + durable-store machinery all live. The `AcceptedDeploy`
  handle returned immediately (S4b decoupling visible) and the commit sequence
  advanced as phases were written durably.

## What is NOT proven live — and why (a test-harness blocker, not a daemon bug)

The activating `FullOs`+`BootOnce` deploy advanced to ~Copying then stalled;
nothing landed on the VM. Root cause: the **qemu VM is not a writable,
adequately-sized deploy target** — its `/nix/store` mounts **read-only**
(`/dev/vda2 … ro`) on a **2.4 GB** disk (795 MB free), far too small for a
~2 GB OS closure, so `nix copy --to ssh-ng://…` cannot write the paths.
`vmWithBootLoader` bakes a fixed-size ro store and ignores
`virtualisation.writableStore` / `diskSize`. The daemon does the right thing;
the throwaway target's storage config is the blocker. A clean writable target
(a proper NixOS qcow2 disk-image via nixos-generators, or a non-bootloader
writable-store VM flavor) would unblock it — but it is 1–2 more harness cycles.

## Production-readiness finding (real, tracked)

**The daemon emits no effect/pipeline logs.** `RUST_LOG` is a no-op, there is
no wire event-log read op, and `WatchDeployments` does not stream (day-one
`2tfa`). A failing deploy is therefore **silent** — an operator cannot see why.
For S5 I worked around it with a `nix`/`ssh` logging shim on the daemon's PATH,
but the daemon itself should surface effect progress/errors. This is a genuine
gap to close before production (a follow-on): a structured effect log and/or a
wire-queryable per-deploy phase/error.

## Decision pending (psyche)

Push the VM harness to land the full live copy+activate+disconnect proof, or
bank the strong partial — the daemon is validated through *build* live and
S1–S4b are all adversarially reviewed; the copy/activate command construction
is a byte-for-byte unit/argv-tested port of production `lojix-cli` (S4a) and the
disconnect-survival is unit-witnessed (S4b). Tracked follow-ons either way:
the live copy/activate proof, the daemon-observability gap, and a writable VM
harness.
