---
description: Ouranos access and declarative host source pointers.
dependencies: []
---

# Ouranos

The hostname is `ouranos`. Root access from this host was verified with `ssh -o BatchMode=yes root@localhost`, returning UID 0 without a password prompt.

The host declaration is `/git/github.com/LiGoldragon/goldragon/cluster-definition.datom`, node `ouranos`, hardware `Metal.X86_64` with model `ThinkPadT14Gen5Intel`. Verified at clean commit `dc57e801671ee7da776664f693d0fbd77f2aedb6`.

That repository's `flake.nix:31–37` combines the cluster with `horizon-config/horizon-configuration.datom`. The inspected local `criomos-horizon-config` checkout at `e222d3a7128484d8163a1a5bf90fbf1a4a15b6ef` lacks that file; the actual selected configuration input remains unverified.

CriomOS assembles generic `boot.kernelParams` in `/git/github.com/LiGoldragon/CriomOS/modules/nixos/metal/default.nix:509–544`. This was read in the dirty checkout at `adc2e8d5f572a833baa492c3c3e9615cb1bf1019`; it is a source pointer, not deployed-source equivalence or edit custody. An Ouranos-specific kernel-parameter extension has not been established. Verify that destination before a host-specific change.
