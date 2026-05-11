# Router DNS Server Research

## Current State After The Edge Fix

`ouranos` is no longer using unbound as the desktop resolver. The live
state after the May 11, 2026 switch is:

- `systemd-resolved.service` active;
- `unbound.service` inactive;
- `/etc/resolv.conf` in resolved stub mode;
- NetworkManager passes the Wi-Fi gateway DNS into resolved;
- normal internet DNS and CriomOS static host lookup both work;
- no failed systemd units.

The regression where `Mod+V` returned to direct dictation was caused by
the full OS switch using CriomOS's pinned `CriomOS-home` input from
May 10, 2026. Updating CriomOS's `criomos-home` lock to the May 11 home
commit fixed that pin, so future full-system switches should keep
`Mod+V` as clipboard-only.

## Unbound Failure Shape

The local symptom was not "unbound process crashed." It was "resolver
looks alive but stops answering useful queries until restarted." The same
class of failure appears in field reports from pfSense/OPNsense users:
the resolver process is running, but queries fail across the network until
the DNS service is restarted. One pfSense thread has several independent
reports of exactly that running-but-dead shape.

Unbound has tools that reduce outage pain, but they do not fully erase
this failure mode:

- `serve-expired` can serve stale cached answers when upstream resolution
  fails. In Unbound 1.23 and later, the RFC-style behavior is the default
  mode when enabled, and it is intended as a fallback to availability or
  configuration errors. This helps only when the answer is already cached.
- `prefetch` keeps popular cached records warmer, at the cost of more
  upstream traffic.
- `unbound-control flush_infra all` clears the infrastructure cache, which
  includes EDNS, ping, and lameness data. That is a less destructive
  recovery action than a full restart if the problem is poisoned upstream
  health state.
- `forward-first` lets a forward-zone fall back to normal recursive
  resolution after forwarding failure. That is incompatible with strict
  "all upstream DNS must go through DoT" intent because it can send clear
  recursive traffic to root/authority servers.

For CriomOS, the important point is that unbound is still a serious DNS
resolver, not a lightweight LAN name service. Keeping it on routers is
defensible only if we explicitly want local recursive validation or
DNS-over-TLS forwarding with cache semantics. If the router just needs
LAN names plus upstream forwarding, unbound is probably heavier than the
problem.

## Current Alternatives

### systemd-resolved

Good fit for clients and desktop edge nodes. It is now our edge path.
It integrates with NetworkManager, tracks per-link DNS, uses the local
stub, and has fallback DNS. It is not the right primary LAN DNS/DHCP
server for router nodes.

### dnsmasq

Best fit for simple CriomOS router LAN DNS if we want small and boring.
The upstream project describes it as lightweight infrastructure for small
networks: DNS, DHCP, router advertisements, and network boot. It can read
static host names, import DHCP lease names into DNS, and cache common
record types.

This maps well to a router whose job is:

- hand out DHCP leases;
- answer `*.goldragon.criome` / cluster names from static horizon data;
- forward the rest upstream;
- stay small and recover with the network.

Tradeoff: dnsmasq is a forwarder/cache, not a full modern recursive
validating resolver in the Unbound sense. If we require DNSSEC validation
and encrypted upstreams at the router, pair dnsmasq with a local encrypted
DNS proxy or use a different resolver.

### CoreDNS

Good fit if we want an explicit, inspectable DNS forwarding pipeline with
health checks. The CoreDNS `forward` plugin supports UDP, TCP, and DoT,
reuses upstream sockets, and performs in-band upstream health checking.
It retries another upstream when a healthy proxy returns an exchange
error. Its `cache` plugin exposes metrics for cache entries, hits,
prefetch, stale serving, and evictions.

CoreDNS is attractive if we care about observability and failure behavior
more than integrated DHCP. It does not replace the router's DHCP service,
so it would pair with Kea or another DHCP owner.

### Knot Resolver

Good fit if we still want a real recursive validating resolver but want
to evaluate a modern alternative to Unbound. Knot Resolver stores its
cache in a file and shares it across workers, so the resolver does not
lose cache on restart or crash. That is directly relevant to the "restart
to recover" world: restarts hurt less.

Tradeoff: it is still a serious resolver stack, not a tiny router helper.
It may be better than Unbound for this role, but it is not the lightweight
answer.

### PowerDNS Recursor

Technically capable, but likely too large for our router role. It is an
operator-grade recursive resolver with extensive features, scripting,
metrics, and tuning. I would not choose it for a small CriomOS LAN unless
we expect to run DNS as a major service.

### dnscrypt-proxy / dnsproxy / Stubby

These are encrypted upstream proxies, not full LAN DNS ownership by
themselves. NixOS documents `dnscrypt-proxy` as the generally recommended
encrypted-DNS proxy because it has broad protocol/feature support and is
written in a memory-safe language. Stubby is explicitly lightweight and
DoT-only, normally combined with another resolver for caching/local
domains.

These make sense as optional upstream privacy components behind dnsmasq
or CoreDNS, not as the whole router DNS story.

## Recommendation

Keep the edge change that already landed:

- edge/NetworkManager nodes use `systemd-resolved`;
- no unbound on desktop edge nodes;
- cluster hostnames stay available through `networking.hosts`.

For router nodes, move toward one of two explicit choices:

1. **Simple router DNS:** use dnsmasq for LAN DNS/DHCP and static
   horizon-derived host records. This is the most proportional answer.
2. **Observable forwarding DNS:** use CoreDNS for DNS, with Kea or the
   current router DHCP service still owning DHCP. This is the better
   answer if we want health-check metrics and clear upstream behavior.

Keep Unbound only if we name the requirement it uniquely satisfies:
recursive validation, DNSSEC-heavy policy, or DoT forwarding with a
validating cache. If we keep it, harden it rather than relying on manual
restart:

- enable remote control on router nodes;
- add a network-recovery hook that runs `unbound-control flush_infra all`
  and then restarts only if a real lookup still fails;
- enable/confirm `serve-expired` and `prefetch` for outage tolerance;
- avoid dead split-DNS zones unless the owning overlay service is active;
- add a NixOS/router test that simulates link loss and proves lookup
  recovery without human restart.

The likely next implementation is not "tune Unbound harder." It is a
router DNS module split: `resolver.nix` for clients, `lan-dns.nix` for
routers, and then choose dnsmasq or CoreDNS inside the router noun.

## Sources

- NLnet Labs Unbound serve-stale docs:
  <https://unbound.docs.nlnetlabs.nl/en/latest/topics/core/serve-stale.html>
- NLnet Labs `unbound.conf(5)` forward-zone docs:
  <https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html>
- NLnet Labs `unbound-control(8)` docs:
  <https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html>
- dnsmasq project docs:
  <https://dnsmasq.org/doc.html>
- CoreDNS forward plugin:
  <https://coredns.io/plugins/forward/>
- CoreDNS cache plugin:
  <https://coredns.io/plugins/cache/>
- Knot Resolver cache docs:
  <https://knot.pages.nic.cz/knot-resolver/config-cache.html>
- NixOS encrypted DNS docs:
  <https://wiki.nixos.org/wiki/Encrypted_DNS>
- pfSense user reports of running-but-dead resolver behavior:
  <https://www.reddit.com/r/PFSENSE/comments/1mv5sq4/dns_resolver_breaks_until_restarted/>
