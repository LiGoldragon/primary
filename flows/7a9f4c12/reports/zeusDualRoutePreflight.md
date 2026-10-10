# Zeus dual-route preflight

## Result

Both the direct-IP transfer route and the DNS activation route are currently
usable under strict host-key checking. Strict SSH and `ssh-ng` Nix-store probes
reach Zeus through `192.168.18.95` and `zeus.goldragon.criome`; both endpoints
return `hostname=zeus` and the same Ed25519 fingerprint
`SHA256:5w4Jj0zqvfZdiGmJLCTKOG6JdXSdMCf3OaBd4EY65Mk`. This strongly identifies
one target at probe time, with the usual caveat that matching host keys do not
prove the absence of address translation or cloning.

## Observations

Zeus is NixOS `26.05.20260422.0726a0e (Yarara)` on x86_64/Linux 7.0.1. The
current and booted system profile is generation 63, with generations 60–62
available; systemd-boot's current and default entry are both generation 63.
Generation 62 is the immediate observed rollback candidate.

`/nix` has 81 GB free of 468 GB (82% used; 10% inode use). `/boot` has 392 MB
free. systemd reports `running` with no currently failed units. The boot
journal records successful NixOS activation and successful enabled Home Manager
services for both users, but also records duplicate D-Bus-name warnings and an
`mpd.service` start failure. Independent Home Manager profiles are current at
bird generation 30 (2026-07-29) and li generation 28 (2026-01-17). Their
NixOS-managed service/gcroots outputs are separate links and do not have a
generation number established by this probe.

Ouranos's ordinary Lojix query remains empty for Zeus:
`Queried.([] [] (625 625))`. No proposal or deployment was submitted.

## Inference

The transport preconditions for a two-route deployment are now witnessed: use
`ssh-ng://root@192.168.18.95` for closure transfer and
`root@zeus.goldragon.criome` for activation, each with strict known-host
checking. The target has a current profile, a prior rollback generation, and
substantial free space, but the activation journal is not clean and profile
versus managed-service Home Manager state is not proven synchronized.

## Safe and unsafe next boundaries

Safe to construct a typed request's transport fields and to perform separately
authorized read-only evaluation/preflight using the witnessed endpoints.

Still unsafe or unresolved for an actual deployment: the immutable source
revision, output selector, builder/substituter choices, Home Manager
synchronization intent, closure size, and activation action are not established
by this preflight. Live activation, boot-profile changes, copy, proposal
submission, and reboot were not authorized here and were not attempted.

## Sources

- [reachability witness](../witnesses/reachability.md)
- [target-state witness](../witnesses/targetState.md)
- [Ouranos Lojix witness](../witnesses/lojixState.md)
- [prior Zeus psyche and transport record](../../01a02b46/vision/zeusUpdate.md)
