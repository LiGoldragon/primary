# Configured Prometheus builder transport, one bounded check

Observed **2026-09-22 01:20:24 UTC** (2026-09-21 19:20:24 local) from **Ouranos**. `/etc/nix/machines` has one configured remote builder, `ssh-ng://nix-ssh@prometheus.goldragon.criome`, with the root-owned `/etc/ssh/ssh_host_ed25519_key`. The name resolved to its recorded Yggdrasil IPv6 address. One `socket.create_connection(("prometheus.goldragon.criome", 22), timeout=8)` returned `TimeoutError` after **8.008 s**. This is a fresh target TCP transport failure, not a successful SSH/Nix-store handshake. There was no build, credential substitution, route change, network restart, or repeat attempt.

The configured key is mode `0600 root:root`; `sudo -n -l` refused because a password is required. This worker therefore could not run a valid authenticated `nix store info --store ssh-ng://…` in the configured daemon-builder identity. A direct probe as `li` would use a different identity and would not test the configured builder. The local Nix daemon's ability to dispatch was not established by this check. The exact peer-side cause of the timeout is unknown. Existing [uplink evidence](prometheus-uplink-reliability-2026-09-22.md) also lacks a currently working Prometheus route; it does not prove peer power, Wi-Fi, cable, or OS state.

For the Mentci stage-2 remote check, this result is an **infrastructure transport blocker at this time**, not a compiler failure or a source verdict. It is separate from the Flow graph's previously reported Cargo.lock/Git dependency fetch mismatch and in-build DNS error. The next check belongs after a new peer-side route or console witness: verify the configured TCP endpoint, then perform the builder-identity store handshake and the exact remote check once, with no local fallback. Do not infer a working builder from Ouranos's public-cache Internet access.

## Receipt scope

- Initiator: Ouranos; target: exactly the host in `/etc/nix/machines`, TCP port 22.
- Network budget: one 8 s connect; elapsed 8.008 s; outcome timeout.
- Authentication/store/build: not attempted because configured identity was inaccessible to this worker and TCP failed first.
- VM: `microvm@vm-testing` remains stopped under its separate guest reservation; no VM observation is inferred from this transport test.
