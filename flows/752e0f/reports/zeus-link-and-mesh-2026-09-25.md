# The Prometheus↔Zeus link and the mesh/network-stack question (Psyche High 752e0f)

Read-only search. Nothing on any host was probed or changed by this subflow.

## 1. The living's own words on mesh, network stacks, and the transitive chain

The living's exact phrase quoted in the brief — "I've asked about looking
into more possibilities and maybe entire network stack mesh-type systems
that we could maybe use" — is typed verbatim by the living in
`flows/e71dab/log.md:15`, dated by the flow as "Asked 2026-09-25" (today's
session; the flow's own machine clock reads 09-25 while the calendar date
given to this subflow is 2026-09-24 — both point at the same live message).
That is the source record, not a paraphrase. No earlier occurrence of this
exact sentence exists anywhere searched (`Vision/`, `vision-raw/`,
`flows/*/vision/`, `flows/*/notion/`, or any Claude/Codex transcript under
`/home/li/.claude/projects`, grepped for "mesh", "network stack", "entire
network").

What the living *has* said before, on adjacent but not identical topics:

- **The transitive topology itself** — `flows/753e69/vision/transitiveNetworkTopologyAndCertificateWifi.md:12`, living, direct message to Field Medium Sol `753e69`, 2026-09-22: "Prometheus has a USB Ethernet that goes to Zeus, which should be getting internet from him through the network cable that Zeus's built-in port has. Let's make that the transitive topology, so it's a testing skill... The built-in port is for upstream, and the USB is for downstream. We just reuse that pattern... kind of statelessly." This is the integrated-NIC-uplink / USB-NIC-downlink pattern named in the brief. It was turned into the `testing-transitive-network-topology` skill.
- **"Mesh" as a name for a different thing** — `flows/e1953c/vision/mesh.md:15`, living, 2026-09-18-ish: "I think you're pretty much on the money with the mesh. It creates the identity using the criome, and it just takes care of hooking up the connections and making sure the routing rules are correct." This is a crypto-plus-tailnet-based *messaging/identity* component the living named "Mesh," not an Internet-sharing network stack.
- **"Tailnet mesh" for the Unity app** — `flows/b05237/vision/operational-unityTailnetApp.md:3,16`, living, 2026-09-18: "We don't even need to set up XMPP. Let's just use Unity with a Tailnet mesh network and a server for connecting nodes, like a closed network." Also messaging, not Prometheus/Zeus Internet sharing.
- **"Mesh protocol" for LAN discovery** — `flows/f55ec8/vision/networking.md:7`, living: "all the internal networking of our own devices and Android devices is on our own Wi-Fi in the house or through the LAN... to connect the nodes that are connected to that router to find each other on that LAN. That's the mesh protocol." Discovery on a foreign router, not the Prometheus→Zeus uplink chain.
- **Yggdrasil as the existing overlay** — `flows/01a030b7/vision/zeusUpdate.md:7`, living, typed: "use its ethernet LAN ip address 192.168.18.95 if you need to move nix paths to it (yggdrassil is over wifi and will be very slow and heavy, but it's fine for activation and other non-heavy transfers usage)." This is the one place the living compares Yggdrasil's performance directly against a wired address for Zeus.

None of these is the living asking to survey mesh-routing *alternatives*
(batman-adv, Babel, WireGuard-mesh, Nebula, Tailscale, NetBird) for the
Prometheus→Zeus leg. No Flow report anywhere under `flows/*/reports` or
`field/` mentions batman, babel, nebula, netbird, or "wireguard mesh."
Tailscale and Yggdrasil are both in active use (Tailscale as
`TailnetClient`/`TailnetController` capability on Ouranos and Prometheus;
Yggdrasil as the cluster overlay), but as deployed tools, not as a surveyed
menu of possibilities. **No Flow was ever tasked with, or answered, a
"look into mesh-type network-stack alternatives" request.** The nearest
delegated, answered work is the transitive-topology testing skill (a
specific uplink/downlink pattern, not a mesh survey) and Mind Astra
`4b0f60`'s "Network Nexus" hierarchy design (`flows/4b0f60/reports/network-nexus-design.md`), which is a typed-topology *planner*, also not a mesh-alternatives survey.

## 2. Current state of the Prometheus→Zeus link

Evidence is dense for **Ouranos→Prometheus** (the first hop) and thin to
absent for **Prometheus→Zeus** (the second hop, the one the living asked
about by name).

**First hop (Ouranos→Prometheus), as of the newest witness,
`flows/d8df70/witnesses/prometheus-firewall-2026-09-24.md`:**

- Wrong, found: Prometheus's WAN nftables policy dropped IPv6 Neighbor
  Discovery on `eno1` (the USB-facing integrated NIC), which prevented
  direct USB-link Yggdrasil peering; and it drops TCP/80, so the Nix
  binary cache times out over the USB link even though it listens and
  answers locally.
- Fixed in source, not yet deployed: Terra `df09b6`'s commit `73ba25c`
  ("Preserve USB Yggdrasil neighbour discovery") landed on CriomOS `main`
  (merge `a50e20c`), adding a scoped NDP-accept rule and a source check.
  Prometheus's *running* generation (built 2026-09-23 11:50, predates the
  fix) does not have it — confirmed live by reading `nft list ruleset` and
  seeing the FAILED neighbor entry and the drop counter increment on a
  live `nc -vz` probe.
- Unfixed even in source: TCP/80 (the cache) has no proposed-and-landed
  fix, only a proposal in the same witness document.
- Masking the symptom: Yggdrasil currently reaches Prometheus over
  `br-lan` (Wi-Fi-side), not over the USB link, so the overlay works today
  despite the NDP drop — at ~92ms RTT instead of the ~1.8ms the direct USB
  link would give.
- Separately, `flows/9ddcbc/reports/usb-yggdrasil-durable-repair-2026-09-24.md` records that even the landed source can't yet be deployed: a full-system Prometheus rebuild against current `main` fails at evaluation because the materialized Lojix input still places router data at `node.routerInterfaces` while current CriomOS expects `node.network.routerInterfaces` — a producer/consumer schema mismatch outside Field's authority to patch.

**Second hop (Prometheus→Zeus): no witness dated today (2026-09-24) exists
in any report, witness, or field/ receipt searched.** `flows/d8df70/`'s own
reports and log contain zero mentions of Zeus. The most recent Zeus-side
evidence found anywhere is `flows/836818/reports/prometheus-observations-2026-09-23.md` (2026-09-23, one day earlier): Zeus was seen only as a
downstream AP client of Prometheus's `br-lan` (`10.18.0.103–108/24`,
gateway `10.18.0.1`), reaching HTTPS successfully through that chain on
2026-09-21, and as Prometheus's *only* live Yggdrasil peer
(`200:17f7:4fad:…`) as of 2026-09-23 22:42 — identity not confirmed as
Zeus by any observer, only inferred from the cluster definition. Whether
Zeus is currently getting Internet through Prometheus at all today is
**unverified** — the living's opening question in this same conversation
("Did anybody figure out what was wrong with the cable connection between
Prometheus and Zeus?", `flows/e71dab/log.md:13`) has not yet been answered
by any dated 2026-09-24 Zeus-side probe.

## Sources

- `flows/e71dab/log.md` (lines 13, 15)
- `flows/753e69/vision/transitiveNetworkTopologyAndCertificateWifi.md`
- `flows/e1953c/vision/mesh.md`
- `flows/b05237/vision/operational-unityTailnetApp.md`
- `flows/f55ec8/vision/networking.md`
- `flows/01a030b7/vision/zeusUpdate.md`
- `flows/836818/vision/network.md`
- `flows/836818/reports/prometheus-topology-2026-09-23.md`
- `flows/836818/reports/prometheus-observations-2026-09-23.md`
- `flows/d8df70/witnesses/prometheus-firewall-2026-09-24.md`
- `flows/9ddcbc/reports/usb-yggdrasil-durable-repair-2026-09-24.md`
- `flows/4b0f60/reports/network-nexus-design.md`
- `.claude/skills/testing-transitive-network-topology/SKILL.md`
