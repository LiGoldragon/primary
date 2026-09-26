# Tester brief: daisy-chain post-deploy verification

Issued after UsbDownlink is deployed on ouranos and Prometheus (and, if it
happened, zeus's first Lojix deploy). Read-only. Do not proceed if any
target has not reached the stated revision.

## Bounded target

Three-node wired chain: ouranos (integrated NIC uplink to ISP) -> USB
downlink -> Prometheus (integrated NIC uplink from ouranos) -> br-lan,
including the Wi-Fi AP hop on Prometheus -> USB downlink -> zeus (integrated
NIC uplink from Prometheus). Nothing outside this chain (zeus's own Wi-Fi
`Mega_2.4G_1896`, Tailscale/Headscale) is in scope except to prove it is
*not* the path used.

## Immutable revisions

- CriomOS: `<CRIOMOS_REV>`
- goldragon: `<GOLDRAGON_REV>`

Record each node's running generation and its source revision; stop and
report UNKNOWN if a node is not running these.

## Authority limits

- Probes only, over `ssh -o BatchMode=yes`.
- No config changes, no service restarts, no `nmcli`/`networkctl` mutation.
- No reboots, no power cycling.
- No Tailscale/Headscale actions of any kind.
- **Forced-interface caveat: zeus also sits on a foreign Wi-Fi AP. Every
  IPv4 test on zeus (and any dual-homed node) must force the wired
  interface** (`curl -4 --interface <if> ...`); an unforced test proves
  nothing about the chain.

## Acceptance contract, per hop

For each hop (ouranos->Prometheus, Prometheus->zeus, Prometheus AP):
1. **Default route** on the downstream node is via the immediate upstream
   hop's address, not a stale or foreign gateway.
2. **DHCP lease** held by the downstream node on its USB NIC, issued by the
   upstream node's DHCP server (leasefile or query, not inference from a
   configured address).
3. **IPv4 fetch** of a known small URL, forced through the wired interface,
   succeeds (200) on Prometheus and on zeus: `curl -4 --interface <if> ...`.
4. **NAT/conntrack evidence** on each gateway (ouranos, Prometheus): live
   `conntrack -L` or firewall counters showing translated flows for the
   downstream subnet, not just a loaded ruleset.
5. **AP hop only:** hostapd broadcasting with `country=MX`, and hostapd log
   lines at the declared log level, both read live.

## Negative cases (must be absent)

- NM connection `prometheus-share-temporary` — absent (not just inactive).
- Firewall drop-in `/etc/systemd/system.control/firewall.service.d/90-field-prometheus-usb.conf`
  and its script `/etc/systemd/field-prometheus-usb-firewall.sh` — absent.
- No other hotfix, override, or manual unit outside the declared
  `<CRIOMOS_REV>`/`<GOLDRAGON_REV>` closure — list every file/unit checked
  and its absence, not just a summary claim.

## Independent oracle

Each claim needs a source distinct from the actor whose config produced it:
route/lease claims from the downstream node's own view AND the upstream
node's server-side lease table; NAT claims from live counters, not the
static ruleset; AP claims from hostapd's own log plus an external scan
(e.g. `iw scan` from a third device) where feasible; "absent" claims from a
direct file/unit stat, not a memory of what should have been removed.

## Evidence grades to return

Per hop and per claim: **source-published**, **installed-running**,
**end-to-end-proven**, or **UNKNOWN**. Never infer the whole chain from one
successful hop; report each hop independently.
