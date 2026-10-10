# Zeus dual-route preflight

Read-only Zeus direct-IP and DNS reachability, endpoint identity, target
generation/profile, capacity, activation-journal, Home Manager, and Ouranos
Lojix preflight. No proposal, build, copy, activation, reboot, or runtime
mutation occurred.

2026-08-22 — Both strict SSH routes and both `ssh-ng` store probes succeeded.
They identify the same Zeus endpoint by hostname and matching Ed25519 host-key
fingerprint. Zeus is system generation 63 with generation 62 available for
rollback, `/nix` has 81 GB free, and Ouranos Lojix still has no Zeus records.
Target activation completed successfully but the journal contains warnings and
an `mpd.service` failure; independent Home Manager profiles are bird 30 and
li 28, while NixOS-managed service links are separate evidence.
