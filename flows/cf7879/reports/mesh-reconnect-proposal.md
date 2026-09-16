# Mesh reconnect record — item 51 proposal

This is a design and bounded read-only witness. No wire type, service, peer configuration, login or mesh is installed. No Nix check is claimed for this document.

## Source and order

The living's source is preserved in primary predecessor 840e42's `vision/tailnet.md` and `vision/cloud.md`, read directly in its actual lane. The full relayed turn in this conversation has SHA256 `ad9987aa50a89ea94d3f81ad43621370240cce89859aefdf20bd2b023e1558ce`. It asks for last-seen LAN, last-seen public and previous public addresses so hosts can reconnect. Cloudflare messaging comes first, Git next, then the mesh. Whether “Tailnet” means restored Tailscale or our own Yggdrasil mesh remains a fork for the living.

## Proposed owner and fields

Keep this small observation record with Lojix's host record. Cloud owns provider operations and can contribute an observation; it should not own a second live host registry. A separate network Nexus is unnecessary for this proof. This ownership is proposed, not adopted.

| Field | Proposed type and meaning |
|---|---|
| Host | Existing typed host identity; never inferred from a newly seen address |
| LastLan | Optional AddressObservation |
| LastPublic | Optional AddressObservation |
| PreviousPublic | Optional AddressObservation, displaced only by a distinct newer public address |
| Revision | Monotonic integer for accepting updates |
| AddressObservation | Address, observed timestamp, reporter host identity and provenance enum |
| Address | IPv4 with four bounded integer octets, or IPv6 with sixteen bounded integer octets |
| Provenance | AuthenticatedHeartbeat, LocalInterface, ProviderObservation or PeerEvent |
| Reachability | Unknown, Candidate, Verified or Failed, with last attempt timestamp |

Use typed absence rather than empty strings. The schema needs an Ethos/Signal proposal and generated-code check before it is a contract. Store numeric address bytes and timestamps; format strings only at human/tool boundaries. Keep detailed logs separately by existing source reference. An address is an attempted endpoint, not proof of a host's identity or permission to send credentials.

## Writers and readers

A heartbeat authenticated as the existing host can report local interface addresses and provider-observed public addresses. A peer event can report a candidate endpoint but must retain its source class. A deployment can seed a candidate with explicit provenance; it must not label deployment-time configuration as a successful connection. Accept only newer observations, deduplicate an unchanged address, and retain the immediately previous distinct public address. Clock uncertainty or conflicting observations becomes Unknown; a timestamp alone is not an authenticity check.

A bounded reconnect worker asks Lojix for candidates: eligible same-network LAN address, current public address, then previous public address. It checks host identity through the existing authenticated transport before treating a connection as verified. Failed attempts use backoff and do not create a new host. Expiration limits candidate attempts; it does not delete the historical observation without a retention policy. Provider changes, firewall changes and host-key replacement are separate operations.

## Read-only observations on 2026-09-16 around 09:09–09:11 UTC

- Ouranos: `tailscale status --json` exited 0; Version `1.102.2`, BackendState `NoState`, Self.Online false. This does not establish an authenticated working tailnet, nor does it justify changing the state label to “logged out.”
- Prometheus: both the configured hostname attempt (15-second bound) and an explicit Yggdrasil roster-address attempt (12-second bound) timed out. Its current Tailscale state is unverified here.
- Zeus: short hostname did not resolve; the explicit Yggdrasil roster address reached an SSH host-key verification failure. No trust setting or known-host entry was changed. Its current Tailscale state is unverified here.
- The secondary's earlier “logged out everywhere” remains an attributed earlier report, not a current three-host witness.

The address source was the existing core roster `/nix/store/8xgi8bjmavs2q4cfnp9jyrcly477i5ak-core-checkup-roster.json`. Only Tailscale status fields above were printed; no auth URLs or credentials were retained.

## Yggdrasil source inspection

Read `modules/nixos/network/yggdrasil.nix` in CriomOS proposal revision `e27a61b026a8bdbdad564cbc89190e7bceaa5b7f`. Its generated public fragment sets `IfName = yggTun`, NodeInfoPrivacy true and multicast beacon/listen on all matching interfaces, using the configured link-local TCP port. It opens the multicast UDP and link-local TCP ports and trusts the named interface. No explicit Peers or InterfacePeers list appears in this module.

Startup merges a separate pre-created configuration with that fragment. That pre-created input may carry other settings; the runtime merged file was not read because it includes private key material. Therefore “no peers anywhere” is not established. This module alone has no last-LAN/current-public/previous-public reconnect record. Source inspection is not a witness of the currently activated host generation.

## Decision and next proof

The living's fork remains: restore the existing Tailscale tailnet, or build an own mesh over Yggdrasil using the record above. Keep the address record independent of that choice. Before either activation, the secondary should provide bounded current status from each host through its trusted route. Next source proof would generate the record type and test update ordering, duplicate observations, previous-address rotation, stale/conflicting input and bounded candidate selection. No live reconnect job or provider action is authorized by this document itself.
