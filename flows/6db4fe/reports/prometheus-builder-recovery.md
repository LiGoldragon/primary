# Prometheus builder recovery check — 2026-09-21

## Result

Prometheus remains unreachable from Ouranos. **No remote Nix gate ran.** There was no local fallback, reboot, garbage collection, service restart, or network mutation in this recovery check. The peer-side NIC, power/cable endpoint, or routing must be inspected from Prometheus or another already-working management route before a change on Ouranos can be justified.

The earlier temporary NetworkManager share is still active on Ouranos USB Ethernet `enp0s20f0u1c2` at `10.44.0.1/24`; the original upstream default route still uses `enp0s31f6` via `192.168.1.1`. The USB interface has carrier but **0 RX bytes and 0 RX packets**, a zero-byte DHCP lease file, and failed ARP for `10.44.0.2`. Its TX counter rose to 537 packets without a peer response. The share was not recreated or modified here. Its exact rollback remains in `flows/6db4fe/reports/prometheus-connectivity.md`; it is an in-memory NetworkManager profile, not durable OS configuration.

The configured builder is still `ssh-ng://nix-ssh@prometheus.goldragon.criome` in `/etc/nix/machines`; `nix config show` points `builders` at that file and has `builders-use-substitutes = true`. The hostname resolves from `/etc/hosts` to Prometheus's Yggdrasil address. The route selects `yggTun`, but bounded TCP/22 and a single batch-mode SSH attempt timed out. This proves neither a working builder connection nor Prometheus Internet access. The Yggdrasil admin socket could not be opened by this user, so peer table state was not claimed.

An earlier live record in `flows/f55ec8/log.md` identified Prometheus as `192.168.1.16` on the same foreign LAN. Ouranos routes that address directly through `enp0s31f6`, but a single ping got no reply, ARP remained `INCOMPLETE`, and batch SSH returned `No route to host`. This historic address may have changed; the result only rules out this recorded route at observation time. The `/etc/hosts` WireGuard address `5::5` has no route on Ouranos, and Tailscale reported backend `NoState`; neither is a supported fallback witness.

One useful typed coordination request was submitted over the existing exact HM route to Field consumer owner **9ddcbc**. It asked for peer-side NIC/DHCP/route evidence and avoidance of competing Ouranos network changes under its consumer ownership. HM returned submission only; a substantive target read or result had not been observed when this report was written. The declarative consumer files under its lock were not touched. Field Sol's packaging gate remains blocked before test execution; this report does not downgrade or reclassify it as passed.

## Next gate and ownership

The next owner with Prometheus-side access should inspect the peer NIC, cable endpoint, DHCP lease/default route, and Yggdrasil service locally. The decisive Ouranos-side signals are nonzero USB RX and a DHCP lease on the shared link, or a new exact reachable peer address with an SSH host-key/builder handshake. Only then test DNS and `https://cache.nixos.org` **from Prometheus**, then the configured SSH builder and the original bounded Nix gate. A durable USB share belongs in the OS source only after the physical/peer route and forwarding path are proven. Until then the in-memory share may be removed using the rollback in the earlier report, but doing so would merely restore the former inactive DHCP attempt and would not repair Prometheus.

## Evidence boundary

Read-only checks: `hostname`, `ip -br link/addr`, `ip route`, `ip -6 route get`, USB `ip -s link`, `ip neigh`, NetworkManager active connection/device state, DHCP lease size, `getent ahosts`, one bounded TCP/SSH attempt to the configured Ygg hostname, one ping and SSH attempt to historic LAN address, Tailscale status, Yggdrasil admin socket attempt, `/etc/hosts`, `/etc/nix/machines`, and `nix config show`. Sources: earlier `flows/6db4fe/reports/prometheus-connectivity.md`, historic address in `flows/f55ec8/log.md`, and intended cluster networking in `flows/024bc7/vision/network.md` and `flows/f55ec8/vision/networking.md`. The temporary USB topology is not proof that Prometheus is at the other end of that carrier.

