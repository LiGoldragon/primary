# Prometheus connectivity from Ouranos — 2026-09-21

## Result

Ouranos has a temporary, in-memory NetworkManager shared connection on its USB Ethernet adapter. It offers `10.44.0.1/24`, DHCP leases from `10.44.0.10` through `10.44.0.254`, and DNS on `10.44.0.1`. The normal upstream route remains `192.168.1.1` through `enp0s31f6`; `https://cache.nixos.org` returned HTTP 200 from Ouranos after the change.

Prometheus has **not** been observed on this link. The USB adapter reports carrier, but its RX counter remained **0 bytes / 0 packets** before and after sharing was enabled. No DHCP lease was issued. ARP for `10.44.0.2` failed. Prometheus's Yggdrasil address `200:ca41:6b12:fba:d7bc:cfc6:4aaa:165f` did not answer ICMPv6 or SSH port 22; SSH timed out. This is not evidence that Prometheus has Internet, nor that remote builds work. The peer NIC state, cable endpoint, and Prometheus routing cannot be inspected from the present reachable host. A working carrier by itself does not identify the peer.

## Observed topology and change

Before the change, `enp0s31f6` was `192.168.1.5/24`, default route `192.168.1.1`, and `enp0s20f0u1c2` was carrier-up but had no IPv4 address. NetworkManager had selected `Wired connection 2` (UUID `662995a5-4bbe-3598-bc1a-15e9535a25f1`), an automatic DHCP profile stuck obtaining an address. Wi-Fi `wlp0s20f3` was down and NetworkManager logged an association timeout for `goldragon.criome`. IPv4 `conf/all/forwarding` was `0` before the change.

I added NetworkManager profile `prometheus-share-temporary`, UUID `92eb01d2-2087-44c9-a6ff-b2420df89d33`, with `save no`, `autoconnect no`, `ipv4.method shared`, explicit address `10.44.0.1/24`, `ipv4.never-default yes`, and IPv6 disabled, then activated it on **only** `enp0s20f0u1c2`. `10.44.0.0/24` was absent from Ouranos's IPv4 routes before activation. NetworkManager started dnsmasq with DHCP on this subnet and a listener on `10.44.0.1:53`; kernel `conf/enp0s20f0u1c2/forwarding` and `conf/enp0s31f6/forwarding` read `1` afterwards, while `conf/all/forwarding` read `0`. The firewall/NAT rules require root to inspect and remain **unverified**. A peer traffic test is required to prove forwarding.

The in-memory profile remains active so the intended peer can request an address. It is not an authored OS configuration and is not expected to survive a NetworkManager restart. No reboot, system activation, broad Nix realization, local fallback build, or Codex app-server change was performed.

## Rollback

The exact temporary profile can be removed with:

```sh
nmcli connection down uuid 92eb01d2-2087-44c9-a6ff-b2420df89d33
nmcli connection delete uuid 92eb01d2-2087-44c9-a6ff-b2420df89d33
nmcli connection up uuid 662995a5-4bbe-3598-bc1a-15e9535a25f1 ifname enp0s20f0u1c2
```

The last command restores the earlier DHCP attempt on the USB adapter; it may wait for an absent DHCP server, as it did before this work. The upstream profile `Wired connection 1` was not edited.

## Next witness and durable boundary

At Prometheus, verify that the attached Ethernet NIC is enabled and connected to the intended cable, then request DHCP on that NIC. The decisive Ouranos-side witness is a nonzero USB RX counter plus a lease in `/var/lib/NetworkManager/dnsmasq-enp0s20f0u1c2.leases`. Then test DNS and `https://cache.nixos.org` **from Prometheus**, verify its default route through `10.44.0.1`, Yggdrasil peer reachability, and an SSH-based remote-builder handshake. Ouranos currently advertises `ssh-ng://nix-ssh@prometheus.goldragon.criome` in `/etc/nix/machines`; `nix config show` confirms that file as its builder source and `builders-use-substitutes = true`. No build was attempted because SSH could not reach Prometheus and the scope excludes local fallback builds.

The peer-side failure is not yet known. A durable declarative share should be selected after a live peer/DHCP and forwarding test; deploying one now would encode an unproven interface path. A durable OS change would require the appropriate CriomOS source edit and later controlled deployment outside this bounded diagnosis.

## Sources

- Live Ouranos commands: `hostname`, `ip -br link`, `ip -br addr`, `ip route`, `ip -s link`, `ip neigh`, `nmcli device show`, `nmcli connection show`, `nmcli general permissions`, `systemctl status NetworkManager`, `journalctl -u NetworkManager`, `ss -lunp`, `/proc/sys/net/ipv4/conf/*/forwarding`, `getent hosts`, `ping`, `ssh`, `curl`, `/etc/nix/machines`, and `nix config show`, observed 2026-09-21. `sudo -n`, `run0 --no-ask-password`, `tcpdump`, and `iptables -t nat -S` could not obtain needed privilege.
- Psyche context: `flows/024bc7/vision/network.md` describes the intended wired cluster; `flows/f55ec8/vision/networking.md` describes local peer discovery through the foreign router. Neither replaces live topology evidence.
- Builder declaration: `/git/github.com/LiGoldragon/CriomOS/modules/nixos/nix/builder.nix`.
