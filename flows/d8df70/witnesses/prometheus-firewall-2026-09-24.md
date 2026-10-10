# Witness — Prometheus firewall, 2026-09-24

Flow d8df70. Read-only diagnosis. Nothing on Prometheus was changed: no
`nft` write, no `ip`/`sysctl` write, no service restart, no rebuild, no
config edit, no commit.

## Method

- From ouranos: `ip -br addr`, `ping -c2 10.44.0.148`, `nc -vz 10.44.0.148 80`,
  `nc -vz 10.44.0.148 22`, `ip neigh show dev enp0s20f0u1c2`.
- On Prometheus over `ssh prometheus` / `ssh root@prometheus`, read verbs only:
  `ip -br addr`, `ip route`, `ip -6 route`, `ip -6 neigh`, `nft list ruleset`,
  `nft -a list chain inet filter input`, `ss -tlnp`, `systemctl --failed`,
  `systemctl cat`, `uptime`, `df -h`, `curl` to its own loopback and own
  eno1 address, `yggdrasilctl getPeers`.
- In `/git/github.com/LiGoldragon/CriomOS`: `git log`, `git show`, `grep`.
  No writes.

## 1. Interface identity — the "USB link" terminates on eno1, the declared WAN

Prometheus, `ip -br addr` and `ip route`:

```
eno1             UP             10.44.0.148/24 metric 1024 fe80::8647:9ff:fe75:8868/64
br-lan           UP             10.18.0.1/24 fe80::4435:5dff:fecb:10a2/64
yggTun           UNKNOWN        200:ca41:6b12:fba:d7bc:cfc6:4aaa:165f/7 ...
enp199s0f0u1     DOWN
default via 10.44.0.1 dev eno1 proto dhcp src 10.44.0.148 metric 1024
```

The 10.44.0.0/24 link that ouranos reaches over its USB NIC
(`enp0s20f0u1c2`, 10.44.0.1) lands on Prometheus's **integrated** NIC
`eno1`, which is also Prometheus's default route. `eno1` is Prometheus's
declared router WAN (`routerInterfaces.wan`), so the WAN policy applies
to it correctly and by design. Prometheus's own USB NIC
(`enp199s0f0u1`) is DOWN and unrelated.

## 2. Live nftables ruleset — the relevant rules, exact

`ssh root@prometheus 'nft list ruleset'`, `table inet filter`, `chain input`:

```
chain input {
	type filter hook input priority filter; policy drop;
	ip6 saddr fe80::/64 ip6 daddr fe80::/64 udp dport 9001 accept
	ip6 saddr fe80::/64 ip6 daddr fe80::/64 tcp dport 10001 accept
	tcp dport 22 accept
	iifname "vmt*" meta l4proto ipv6-icmp accept comment "Allow NDP/ICMPv6 from test-VM guests"
	iifname "vmt*" ct state { established, related } accept comment "Allow return traffic for host-initiated guest connections"
	iifname { "br-lan", "yggTun", "wlp195s0", "wlp199s0f0u4" } accept comment "Allow local network to access the router"
	iifname "eno1" ct state { established, related } accept comment "Allow established traffic"
	iifname "eno1" icmp type { destination-unreachable, echo-request, time-exceeded } counter packets 4 bytes 336 accept comment "Allow select ICMP"
	iifname "eno1" counter packets 57282 bytes 4814398 drop comment "Drop all other unsolicited traffic from eno1"
	iifname "lo" accept comment "Accept everything from loopback interface"
}
```

Consequences for inbound traffic arriving on eno1:

- **IPv4 tcp/22** — accepted by the unscoped `tcp dport 22 accept`, which
  precedes the eno1 drop. This is why ssh over the USB link works.
- **IPv4 tcp/80** — matches no accept rule; falls to
  `iifname "eno1" counter ... drop`.
- **IPv4 ICMP echo** — accepted by the select-ICMP rule. Ping works.
- **IPv6 ICMPv6 / NDP** — the select-ICMP rule is `icmp` (IPv4 only), so
  ICMPv6 is not matched by it. There is **no** NDP admit rule for eno1 in
  the live ruleset. Neighbor solicitation and advertisement arriving on
  eno1 fall to the same drop.

There is also a separate `table ip6 yggdrasil-local` with
`type filter hook input priority -100; policy accept;` carrying the same
two fe80 port rules; its accept policy does not exempt anything from the
`inet filter` chain at priority 0.

## 3. Port 80 — listener is fine; the timeout is a firewall drop

`ss -tlnp` on Prometheus:

```
LISTEN 0      1024                                      *:80               *:*    users:(("starman worker ",pid=1750,...),("starman master ",pid=1665,fd=4))
```

The listener is `nix-serve` (starman), `services.nix-serve.bindAddress = ""`,
bound to the **wildcard** — every address, v4 and v6. `nix-serve.service`
is `loaded active running`.

From Prometheus itself:

```
curl http://127.0.0.1/nix-cache-info      -> 200
curl http://10.44.0.148/nix-cache-info    -> 200
```

So the service answers on the eno1 address when the packet does not
traverse the input hook.

From ouranos over the USB link:

```
ping -c2 10.44.0.148   -> 2 received, 0% loss
nc -vz 10.44.0.148 22  -> Connection to 10.44.0.148 22 port [tcp/ssh] succeeded!
nc -vz 10.44.0.148 80  -> (no output; timed out)
```

Counter proof, two `nc -vz … 80` attempts run between two reads of the
drop rule:

```
BEFORE: iifname "eno1" counter packets 57331 bytes 4818254 drop comment "Drop all other unsolicited traffic from eno1" # handle 15
AFTER : iifname "eno1" counter packets 57354 bytes 4819950 drop comment "Drop all other unsolicited traffic from eno1" # handle 15
```

**Established: the USB-side port-80 timeout is a firewall drop.** Not a
listener binding problem (wildcard, answers locally on that same
address), not a routing problem (same L2 link, IPv4 ping and tcp/22 both
work, `10.44.0.148 lladdr 84:47:09:75:88:68 REACHABLE` in ouranos's ARP
table).

## 4. The NDP drop is still live

Prometheus, `ip -6 neigh`:

```
fe80::c730:ec24:c777:db80 dev eno1 FAILED
```

`fe80::c730:ec24:c777:db80` is ouranos's link-local on `enp0s20f0u1c2`
(confirmed from ouranos's `ip -br addr`). Prometheus cannot resolve it:
its solicitations leave, and ouranos's advertisements come back in on
eno1 as ICMPv6 and hit the eno1 drop. Ouranos's side holds
`fe80::8647:9ff:fe75:8868 lladdr 84:47:09:75:88:68 PROBE` — it learned
Prometheus's address from Prometheus's own outbound solicitations, and is
now failing to re-confirm it.

So field 9ddcbc's claim is confirmed: **the WAN policy still drops
Neighbor Discovery on the USB link, and Terra df09b6's repair is not
deployed.** The rule that would admit it exists in CriomOS `main`
(section 6) but not in Prometheus's running ruleset.

**Does it matter now?** Yggdrasil currently reaches Prometheus over a
different path, not over the USB link. `yggdrasilctl getPeers`:

```
tls://[fe80::923c:76aa:6a1a:a016%25br-lan]:10001  Up  Out  201:6de1:5500:7cac:2db9:759e:42d2:fb1d  27m43s  92.47ms
tls://[fe80::923c:76aa:6a1a:a016%25br-lan]:33505  Up  In   201:6de1:5500:7cac:2db9:759e:42d2:fb1d  26m23s  92.49ms
```

`201:6de1:5500:7cac:2db9:759e:42d2:fb1d` is ouranos's yggTun address. The
session runs over Prometheus's `br-lan`, which is inside the
`iifname { "br-lan", "yggTun", … } accept` set, so it is unaffected by
the WAN policy. RTT 92ms on a same-room pair indicates an indirect
wireless path rather than the 1.8ms USB link.

Therefore: the NDP drop does not break anything today, because
Yggdrasil found another way around. What it costs is the direct,
low-latency USB peering — Prometheus's `[fe80::8647:9ff:fe75:8868]%eno1:10001`
Yggdrasil listener can never be reached over that link while NDP is
dropped. It is a live defect with a currently-masked symptom, not a dead
finding.

## 5. Everything else on Prometheus is healthy

```
systemctl --failed   -> 0 loaded units listed
uptime               -> 08:04:25 up 20:13, 1 user, load average 0.00, 0.00, 0.00
df -h / /nix         -> /dev/nvme0n1p2 1.9T 1.4T 426G 78% (/ and /nix, same fs)
nix-serve.service    -> loaded active running
kea-dhcp4-server     -> loaded active running
readlink -f /run/current-system
  -> /nix/store/j1362haqmyh5ha7bg9ds780yzpsjchav-nixos-system-prometheus-26.05.20260422.0726a0e
  built 2026-09-23 11:50:46 -0600
```

No failed units, idle load, 426G free. The running generation predates
Terra's repair commit (2026-09-23 18:22), which is consistent with the
repair being absent from the live ruleset.

## 6. Source: what has landed, and what has not

Repository `/git/github.com/LiGoldragon/CriomOS`, HEAD `59b3229`
("Pin current CriomOS home configuration"), branch `main`.

Terra df09b6's repair is commit `73ba25c` "Preserve USB Yggdrasil
neighbour discovery" (2026-09-23 18:22), merged to `main` by `a50e20c`.
`git branch --contains 73ba25c` lists `main` and `origin/main`. In
`modules/nixos/router/default.nix` it adds, ahead of `tcp dport ssh accept`:

```nix
iifname "${routerInterfaces.wan}" ip6 saddr fe80::/64 ip6 daddr { fe80::/64, ff02::/16 } icmpv6 type { nd-neighbor-solicit, nd-neighbor-advert } accept comment "Allow link-local NDP for Yggdrasil discovery"
```

guarded by a new source check `checks/router-yggdrasil-ndp/default.nix`
which asserts the scoped NDP rule is present, that a broad
`iifname "eno1" meta l4proto ipv6-icmp accept` is *not*, and that
`iifname "eno1" counter drop` survives. It also flips the USB gateway
profile from `ipv6.method = "disabled"` to `link-local` with
`never-default` and `ignore-auto-dns`.

**This covers item 3 (NDP) completely, and item 2 (port 80) not at all.**
There is no rule admitting tcp/80 on the WAN anywhere in the router
ruleset.

### Why port 80 is not covered — the structural cause

`modules/nixos/nix/cache.nix` declares:

```nix
networking.firewall.allowedTCPPorts = optionals isNixCache [
  80
];
services.nix-serve = {
  enable = isNixCache;
  bindAddress = "";
  port = 80;
};
```

But `modules/nixos/router/default.nix` sets:

```nix
networking = {
  nat.enable = false;
  firewall.enable = !useNftables;
  nftables = {
    enable = useNftables;
    ruleset = ''…'';
  };
};
```

On a router node the NixOS firewall module is **disabled** and the whole
ruleset is hand-written. `networking.firewall.allowedTCPPorts` is
therefore inert: nothing translates it into an nftables accept. That is
why the ruleset's only unscoped TCP accept is the literal
`tcp dport ssh accept` written into the router module by hand, and why
port 11434 (`modules/nixos/llm.nix`, also `allowedTCPPorts`, also
listening per `ss`) is likewise unreachable from the WAN.

So Prometheus is a node that is both `behavesAs.router` and
`isNixCache`, and the two modules do not compose: the cache's port
declaration is silently discarded by the router's ruleset.

## 7. Proposed fix — proposal only, nothing applied

Two separate items.

**(a) NDP.** No source change needed. Terra df09b6's `73ba25c` is on
`main` and is correct as written. The fix is deployment: rebuild
Prometheus against current `main`. This is a change to a live router's
firewall and is outside this flow's read-only authority — it needs the
main flow's decision on who deploys and when.

**(b) Port 80.** Needs a source change that does not yet exist.

Smallest correct form, in `modules/nixos/router/default.nix`, in the
`inet filter` `input` chain, placed beside `tcp dport ssh accept`:

```nix
iifname "${routerInterfaces.wan}" ip saddr 10.44.0.0/24 tcp dport 80 accept comment "Allow the upstream USB link to fetch from this node's binary cache"
```

scoped so it emits only when the node is a cache — i.e. built from
`horizon.node.isNixCache`, not unconditionally — and with the subnet
taken from the USB gateway module's declared range rather than written as
a literal.

A better-shaped alternative, worth the main flow's judgement: rather than
teaching the router module about the cache, have the router module
consume the node's declared open ports so `cache.nix`'s
`allowedTCPPorts = [ 80 ]` and `llm.nix`'s `[ 11434 ]` stop being
silently inert on router nodes. That fixes a class of defect instead of
one instance, and matches "when more correctness is introduced into an
engine, the gain more than makes up for the added machinery." It is the
larger change, and it is a design decision, not a repair.

Either way the change should carry a source check in `checks/`, in the
shape Terra established with `checks/router-yggdrasil-ndp/default.nix`:
assert the cache port is admitted on a cache+router fixture, assert it is
**not** admitted on a router that is not a cache, and assert
`iifname "…" counter drop` still terminates the chain.

### A question this flow cannot settle

Admitting tcp/80 on `routerInterfaces.wan` opens the binary cache to
whatever is upstream. In this topology upstream is ouranos, the intended
consumer, which is why the exposure looks acceptable here. But the rule
lives in the generic router module and eno1 is the interface facing the
wider network on other nodes. Whether an unauthenticated nix-serve should
be reachable from the WAN at all — as against routing the cache over
Yggdrasil only, which already works — is a policy call for the psyche or
the main flow. Note that the Yggdrasil path to port 80 works today, so
there may be no need to open the WAN at all.
