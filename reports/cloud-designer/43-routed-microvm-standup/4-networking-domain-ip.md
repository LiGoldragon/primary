# 43 · Routed microVM standup — networking, domain, IP

Read-only reconnaissance (agent 4). HARD SAFETY: nothing below mutated any
host. ssh/ping/getent/`ip` calls were inspection only. This grounds *how the
microVM gets a Criome domain + reachable IP and becomes viewable from
ouranos* — the live workstation IS ouranos (`hostname` = `ouranos`).

## The chain at a glance

```
goldragon/datom.nota  (horizon proposal: per-node nodeIp + yggAddress)
      │  horizon-rs projects Node.criome_domain_name = <node>.<cluster>.criome
      ▼
CriomOS network/default.nix  mkCriomeHostEntries  →  networking.hosts
      │  (criomeDomainName → yggAddress ; wg.<domain> → nodeIp)
      ▼
vm-testing/default.nix  reuses that grain  →  vm-testing.<cluster>.criome
      │  resolves to the HOST's node IP (NOT a separate guest IP)
      ▼
human on ouranos opens the host's remote-display (SPICE/VNC/QMP) over Yggdrasil
```

## How the guest gets an address (tap, no host bridge yet)

`modules/nixos/vm-testing/default.nix` (next branch, `jj file show -r next`)
declares the persistent microVM via microvm.nix with **one tap interface**:

```
interfaces = [ { type = "tap"; id = "vm-testing"; mac = "02:00:00:00:00:01"; } ];
```

That is the *only* networking the module gives the guest. There is **no
host-side bridge, no tap IP/route, no forwarding, no DHCP** for the guest in
this module (confirm: the module touches `networking.hosts` only; the router
bridge `br-lan` and `kea` DHCP in `router/default.nix` are router-LAN, not the
tap). So the guest does **not** join Yggdrasil and does **not** get its own
routed cluster IP today. The guest is reached **through the host** via the
remote-display protocol, not by its own L3 address.

## How vm-testing.<cluster>.criome resolves to an IP

The module computes (vm-testing/default.nix):
- `criomeDomain = "vm-testing.${clusterName}.criome"` (clusterName from
  Horizon `cluster.name`, else node name).
- `nodeAddress = head(split "/" node.nodeIp)` — the **host's own node IP**,
  CIDR stripped.
- emits `networking.hosts = { "${nodeAddress}" = [ criomeDomain ]; }`.

This deliberately matches `network/default.nix`'s `mkCriomeHostEntries` grain
(default.nix:26-61): a node's `criomeDomainName` maps to its `yggAddress`
(primary alias) and `wg.<domain>` maps to its `nodeIp`. The CI check
`checks/vm-testing-prometheus-policy/default.nix` pins it: with `nodeIp =
10.0.0.2/24`, `networking.hosts."10.0.0.2" == ["vm-testing.criome.criome"]`.
**The domain resolves to the host, and the host's display surface fronts the
guest.** domain-criome owns registration/resolution; CriomOS only emits the
host-side hosts entry (provider-neutral projection, per the module comment).

## Where the domain + IP come from (horizon-rs projection)

- `horizon-rs/lib/src/node.rs:339` —
  `criome_domain_name = CriomeDomainName::for_node(name, cluster)`.
- `horizon-rs/lib/src/name.rs:107-108` — `for_node` ⇒
  `format!("{node}.{cluster}.criome")`. Domains are **derived from node name +
  cluster**, never auto-allocated.
- `node_ip` (`lib/src/node.rs:416`) and `ygg_address` (`:433`) are
  **pass-through from the proposal** — operator-assigned in
  `goldragon/datom.nota`, not auto-allocated. `NodeIp` is a CIDR
  (`address.rs:90`); `YggAddress` is validated inside `200::/7`
  (`address.rs:12-15`).

## Live path ouranos → prometheus (the traffic route the VM inherits)

`goldragon/datom.nota`: ouranos `nodeIp 5::3/128`, ygg
`201:6de1:5500:7cac:2db9:759e:42d2:fb1d`; prometheus `nodeIp 5::5/128`, ygg
`200:ca41:6b12:fba:d7bc:cfc6:4aaa:165f`. Cluster = **goldragon** (datom:1),
not the CI stub's `criome`.

Live read-only confirmation on ouranos:
- `ip -br addr`: `yggTun  201:6de1:5500:7cac:2db9:759e:42d2:fb1d/7` (matches
  the datom).
- `ip -6 route`: `200::/7 dev yggTun` — the whole mesh routes over Yggdrasil.
- `/etc/hosts` carries the projected grain verbatim:
  `200:ca41:6b12:fba:d7bc:cfc6:4aaa:165f  prometheus.goldragon.criome
  nix.prometheus.goldragon.criome` and `5::5  wg.prometheus.goldragon.criome`.
- `ping -6` to prometheus ygg: 2/2 received, ~16ms RTT.
- TCP connect to `[prometheus-ygg]:22`: **port 22 OPEN**.

So **ouranos reaches prometheus today over the Yggdrasil mesh** at its ygg
address (primary `.criome` alias); the `wg.` alias / `5::` nodeIp is the
WireGuard path (`network/wireguard.nix`: peer endpoint
`wg.<domain>:51820`). Yggdrasil is the working production path right now.

## What a human opens to view the VM

Once deployed on prometheus, the projected domain is
**`vm-testing.goldragon.criome`** resolving (via the host-entry the module
emits) to prometheus's address — i.e. the same host ouranos already reaches.
The viewable surface is the host's **remote display**: the module enables
SPICE by default (`virtualisation.spiceUSBRedirection`, `spice`/`spice-gtk`
packages) and the guest has `graphics.enable = true`; design report 67
(§"the gamma verdict", lines 58-60, 154-156) confirms the capture/display
path is QEMU's QMP `screendump` / built-in VNC / SPICE on the host. So a human
on ouranos opens a SPICE/VNC client (or screenshot via QMP) pointed at
prometheus over the existing Yggdrasil route. No new domain authority is
needed for first reachability — the hosts entry is local projection.

## DNS / routing prerequisites and the gap to close

1. **No guest-side L3 routing exists yet.** The tap has a MAC but no host
   bridge, IP, route, or forwarding. For the *display* path this is fine (the
   host fronts the guest), but the domain points at the **host**, so the
   chosen remote-display port (SPICE/VNC/QMP) must be **listening on the
   host's reachable address and allowed through the host firewall**. The
   module does not open a display port today — this is the concrete standup
   gap for "reachable + human-viewable."
2. **Cluster name mismatch to fix before trusting the projected string.** Live
   cluster is `goldragon`, so the real domain is `vm-testing.goldragon.criome`
   (the CI stub and several comments say `<cluster>.criome` → `criome.criome`).
   The projection is data-driven from `cluster.name`, so it self-corrects on
   the goldragon horizon; just don't hardcode `criome`.
3. **Resolution is `/etc/hosts`, not live DNS.** ouranos resolves `.criome`
   from its projected `/etc/hosts` (nscd disabled, `network/default.nix:94`).
   For ouranos to resolve `vm-testing.goldragon.criome`, the **new hosts entry
   must land in ouranos's own generation too** (it is projected per-node from
   the same horizon) — OR the human targets prometheus's address/`.criome`
   name directly. domain-criome's authoritative resolution is the eventual
   path; today it is the projected hosts grain.
4. **Yggdrasil is the live transport** and already works ouranos→prometheus
   (verified). No new route is needed; the VM's traffic rides the existing
   mesh to the host, then the host bridges it to the guest's display.

## One-line answer

The microVM gets its Criome domain `vm-testing.goldragon.criome` by
projection (host name + cluster → host node IP, via the `mkCriomeHostEntries`
grain), resolving to prometheus's address that ouranos already reaches over
Yggdrasil (`200::/7 dev yggTun`, ~16ms, ssh open); a human views it with a
SPICE/VNC/QMP client on the host. Prerequisite: open/serve a remote-display
port on the host's reachable address + firewall, ensure ouranos's generation
carries the new hosts entry, and use the real cluster name `goldragon`.
