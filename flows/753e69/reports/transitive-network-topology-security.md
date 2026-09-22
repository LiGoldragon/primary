# Cascaded routed cluster topology — terminology and security review

## Current answer

Prometheus is **not currently proven to have Internet through Ouranos**. A
2026-09-21 bounded witness did prove the path under temporary Ouranos DHCP,
firewall, and NAT rules: Prometheus received `10.44.0.148/24` through gateway
`10.44.0.1`, resolved `cache.nixos.org`, and received HTTP 200. The latest
independent test instead found no current Prometheus lease, ARP response, or
ICMP response. That later observation supersedes the earlier proof for current
availability. The Zeus cable was intentionally unplugged after an earlier
end-to-end proof, so the second hop is intentionally unavailable now.

## Canonical terminology

The short term for a laptop's built-in Ethernet port is **onboard NIC** or
**integrated NIC**. `NIC` means network interface controller. Describe role
separately from hardware:

| Node | Physical interface | Role term | Link term |
| --- | --- | --- | --- |
| Ouranos | integrated NIC `enp0s31f6` | **uplink**, **WAN-facing interface** | upstream link to the ISP/home gateway |
| Ouranos | USB NIC `enp0s20f0u1c2` | **downlink**, **LAN-facing interface** | transit link to Prometheus |
| Prometheus | integrated NIC `eno1` | **uplink**, **WAN-facing interface** | transit link from Ouranos |
| Prometheus | USB NIC `enp199s0f0u2c2` | **downlink**, **LAN-facing interface** | transit link to Zeus |
| Zeus | integrated NIC, exact current name unknown | **uplink**, **WAN-facing interface** | transit link from Prometheus |

Each cable between adjacent nodes is a **point-to-point transit link**. The
whole shape is a **cascaded routed gateway chain**. “Transitive topology” is a
useful project name for the reusable invariant. If every hop performs NAT, the
result is **nested NAT** or **double NAT**. The preferred durable shape is
routing on every hop with one egress NAT owner at the Internet edge, Ouranos.
Temporary NetworkManager `ipv4.method=shared` creates DHCP, forwarding DNS,
and NAT toward the current default connection, so applying it at every hop
would create nested NAT rather than pure transit routing.

```text
ISP/home gateway
  -> Ouranos integrated NIC [uplink/WAN]
  -> Ouranos USB NIC [downlink/LAN]
  -> Prometheus integrated NIC [uplink/WAN]
  -> Prometheus USB NIC [downlink/LAN]
  -> Zeus integrated NIC [uplink/WAN]
```

## Reusable interface-role policy

The living's desired invariant is clear: **integrated NIC is upstream; USB NIC
is downstream**. Call this the **integrated-uplink / USB-downlink policy**.
It can be topology independent, but it cannot be literally stateless. DHCP
leases, addresses, routes, neighbor state, firewall state, forwarding, DNS,
and certificate state necessarily exist. The implementable target is
**declarative and convergent**: after boot, hotplug, cable movement, or service
restart, the node reconciles toward the same role policy without relying on a
stale interface name or hostname.

Identify interfaces from stable hardware facts and the typed node capability;
verify the local MAC and driver class; reject ambiguous multiple integrated or
USB NICs. Never infer direction solely from the current default route because
a failed or malicious DHCP server can install the wrong route. Each downstream
link needs a distinct subnet, one DHCP owner, one DNS policy, and explicit
forwarding rules. Upstream and downstream must never be bridged accidentally.

The accepted `UsbIpv4Gateway` service already represents one node's gateway
edge with `downstream`, `downstream_mac`, `gateway`, and `uplink`. Reusing that
shape per node makes the chain recursive without making it hostname-specific.

## Stable Ethernet and optional AP mode

Use **Wired Uplink Gateway Mode** as the canonical mode name. “Stable Ethernet
mode” is a good UI label if it means the same explicit state. Its optional
wireless feature is **Managed AP on wired backhaul** or **Optional AP**.
“Opportunistic AP” should be reserved for an explicitly accepted automatic
policy; silently enabling an AP when a cable appears would be surprising and
increases attack surface.

Only an authorized network administrator capability should toggle the mode.
The transition should be transactional: preflight the wired uplink, preserve a
management path, install address/route/firewall/AP state, test health, commit,
and roll back on failure. Record the actor, requested mode, previous state,
result, and rollback. Do not place passwords, private keys, OAuth material, or
certificate enrollment secrets in command arguments or logs.

## Wi-Fi and PKI security

The transitional shared password is WPA3-SAE personal authentication. The
certificate target is **WPA3-Enterprise with 802.1X/EAP-TLS**, using a RADIUS
server and one client certificate/private key per Android phone or laptop.
NIST describes EAP methods for wireless authentication and separately uses
802.1X/EAP-TLS as a certificate-backed endpoint authentication pattern. Each
device identity should have a unique key, constrained client-auth usage,
bounded lifetime, renewal, and revocation. Never copy one device private key
to another client.

Use an offline local root CA and a restricted issuing intermediate rather than
placing the root signing key on the AP. The RADIUS server needs its own server
certificate, and clients must validate the expected CA and server identity to
prevent evil-twin credential capture. Keep an emergency recovery path and a
separate onboarding flow. A shared-password SSID can coexist temporarily, but
it should be identified as migration state and isolated from administrative
services.

For internal DNS, an invented bare `.criome` or `.CreoM` top-level domain can
collide with future or external DNS. For strictly local names, use a project
subdomain under `home.arpa.`, such as `criome.home.arpa.`, or a subdomain of a
public domain the living controls with split-horizon DNS. RFC 8375 reserves
`home.arpa.` for home networks and warns that local answers are not inherently
trusted. Private certificates still require the managed clients to trust the
private CA, and certificate SANs must exactly match the selected names.

## Firewall and routing requirements

- Default-deny new forwarding; allow established and related return traffic.
- Permit forwarding only between the declared uplink/downlink pair and only
  for intended source subnets. Apply anti-spoof checks on both sides.
- Keep DHCP/DNS listeners bound to the downstream interface. Do not expose
  them on the uplink or management interface.
- Prefer one NAT owner at Ouranos. Route Prometheus and Zeus downstream
  prefixes toward their next hop. If nested NAT is retained temporarily,
  label it explicitly and test inbound limitations and failure diagnosis.
- Treat IPv6 deliberately: either route prefixes with RA/DHCPv6 and equivalent
  firewall policy, or disable it on the temporary transit links until that
  policy exists. IPv4 NAT does not secure IPv6.
- Separate management access from client/AP traffic and preserve the known
  management path during every transition.
- Reject duplicate DHCP, duplicate NAT owners, overlapping prefixes, ambiguous
  NIC selection, link loops, and simultaneous networkd/NetworkManager ownership.

## Source basis

Local evidence: `flows/753e69/reports/network-path-plan-2026-09-21.md`,
`flows/6db4fe/reports/usb-gateway-consumer.md`, and the latest Terra independent
network result delivered to `753e69`. Standards references:

- RFC 8375, `home.arpa.`: https://www.rfc-editor.org/info/rfc8375/
- NIST SP 800-120, wireless EAP methods:
  https://www.nist.gov/publications/recommendation-eap-methods-used-wireless-network-access-authentication
- NetworkManager `ipv4.method=shared` behavior:
  https://networkmanager.dev/docs/libnm/1.30/NMSettingIP4Config.html

The existing Psyche Low Sonnet route is currently blocked in an expired-login
OAuth screen. This report is therefore Field-authored and queued for Psyche
security review; it is not represented as a fresh Sonnet review.
