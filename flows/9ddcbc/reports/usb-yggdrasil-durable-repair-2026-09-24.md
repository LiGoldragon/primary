# Ouranos–Prometheus USB Yggdrasil repair

Owner: Field Medium `9ddcbc`. Observation and source work: 2026-09-24 UTC.

## Causal conclusion

The original Ouranos-side blocker was the active USB profile's disabled IPv6. Field Low `df09b6` changed only that profile to IPv6 auto with no default route and no DNS, producing a link-local address while preserving the IPv4 share and Ouranos's wired default route. After that repair, both hosts had USB link-local addresses and Yggdrasil TCP/10001 listeners, but Neighbor Discovery still failed bilaterally and neither Yggdrasil daemon had a USB session.

The remaining observed blocker is Prometheus's effective nftables WAN policy. `eno1` has a default drop after narrow link-local Yggdrasil UDP/9001 and TCP/10001 accepts, but no ICMPv6 Neighbor Solicitation or Advertisement admission. Prometheus therefore cannot resolve the Ouranos link-local neighbor before reaching either allowed Yggdrasil port. Ouranos accepts IPv6 ICMP under its current effective policy. This supports NDP loss as the immediate remaining cause with high confidence.

Safe combined-config reads confirmed empty `Peers`, empty `InterfacePeers`, and multicast discovery enabled on both Yggdrasil daemons. This disconfirms a current static-peer explanation. The earlier Psyche observation that Ouranos USB IPv6 was disabled was correct before Field Low's repair and stale afterward. Prometheus's intended and live WAN remains `eno1`; DHCP, its default route through `10.44.0.1`, authenticated SSH over `10.44.0.148`, and Prometheus Internet access were separately observed, so upstream reassignment is not the immediate Yggdrasil failure.

## Landed source

CriomOS main revision `a50e20c40c9568e37d106bf554069b91729f6bd6` merged the repair:

- `modules/nixos/router/default.nix` admits only link-local Neighbor Solicitation and Advertisement on the declared WAN before retaining the default drop.
- `modules/nixos/network/usb-ipv4-gateway.nix` keeps IPv6 link-local, disables IPv6 default routing, and ignores IPv6 DNS on the shared USB profile.
- Focused checks cover both policies and are registered in the flake.

CriomOS main revision `59b3229436d0f101e779c14b7ed4ee0f71507540` advances the required CriomOS-home pin from `a2358e…` to current remote main `09cace84f11d56e1d4299e4921942c5fbfb0211e`, which includes the authored Codex remote-control file-limit persistence. Both commits were pushed and read back as `origin/main` at publication time.

The two focused derivations passed again from immutable `59b3229…` using the Prometheus remote builder over the proven USB IPv4 route, with local jobs disabled and fallback false:

- `usb-ipv4-gateway-policy`
- `router-yggdrasil-ndp-check`

This is remote build evidence for the policies, not deployment evidence.

## Deployment boundary

The exact Prometheus full-system build from immutable `59b3229…` and its four current Lojix materialized inputs failed during evaluation before a derivation or activation. The materialized JSON still places router data at `node.routerInterfaces`; current CriomOS requires `node.network.routerInterfaces`. The generated input dates from July and cannot be rewritten by Field as an ad hoc compatibility shim. Current Horizon/Lojix producer integration is separately owned under existing Orchestrate reservations.

Ouranos's current materialized Horizon has no `UsbIpv4Gateway` service, so the landed USB profile module is likewise inactive there until a current typed projection is materialized. Field Low's live profile repair remains the current effective Ouranos state.

No NixOS activation, service restart, firewall mutation, route change, DNS change, credential change, or host reboot occurred in this source/build sequence. The supported next gate is a current Lojix materialization carrying the nested network shape and Ouranos gateway capability, followed by the same immutable remote-only full builds, a bounded generation switch, and post-switch NDP/Yggdrasil/default-route/DNS/auth witnesses.

## Ownership and reservations

- Orchestrate `4912`: Field `9ddcbc`, six CriomOS network source/check/registration paths.
- Orchestrate `4913`: Field `9ddcbc`, CriomOS `flake.lock` for the current Home pin.
- Controller `4639` and the independent Horizon/Lojix integration reservations remain untouched.

