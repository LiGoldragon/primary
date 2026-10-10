# Live witness — 2026-09-25, ouranos

Method: direct read-only commands from ouranos (this host) and read-only `ssh`
to prometheus.goldragon.criome and zeus.goldragon.criome. No restarts, no
deploys, no messages, no writes to any host. Times are UTC, from
`date -u +%H:%MZ` run in the same shell as each probe.

## 1. Flows — `hm-list` and `herdr agent list` [16:07Z]

```
$ date -u +%Y-%m-%dT%H:%M:%SZ; hostname; hm-list
2026-09-25T16:07:08Z
ouranos
FLOW	AGENT	SESSION	STATE
-	psyche-haiku-of-b80e55	messaging-build	idle
d8df70	psyche-opus-5	messaging-build	done
e51411	psyche-opus-of-d8df70-r2	messaging-build	working
-	psyche-opus-b87854	messaging-build	idle
38de5b	psyche-fable-refresh-5f38bc	messaging-build	working
00f95a	mind-sol-00f95a	messaging-build	working
26c50c	mind-astra-26c50c	messaging-build	done
5f38bc	field-astra-5f38bc	messaging-build	done
b7da5d	field-sol-b7da5d	messaging-build	done
e71dab	field-luna-e71dab	messaging-build	done
-	codex-2d0e71a77a40543c10ac8ac1	messaging-build	idle
634c9e	field-terra-opencode-634c9e	default	STALE
1b8ac0	flow-1b8ac0	messaging-build	STALE
752e0f	psyche-fable-of-836818	messaging-build	STALE
b80e55	flow-b80e55	messaging-build	STALE
e88ca4	psyche-opus-of-b81560-r2	default	STALE
6288d1	mind-sol-flow-psyche	messaging-build	STALE
23d977	flow-23d977	messaging-build	STALE
47764b	mind-high-47764b	messaging-build	STALE
4b0f60	flow-4b0f60	messaging-build	STALE
e798f3	flow-e798f3	messaging-build	STALE
eb7bae	field-medium-eb7bae	default	STALE
2c61af	flow-2c61af	messaging-build	STALE
effa1b	mind-sol-of-0ab019	messaging-build	STALE
6fb948	flow-6fb948	messaging-build	STALE
9ddcbc	field-medium-9ddcbc	messaging-build	STALE
2fe3f1	field-terra	messaging-build	STALE
c88918	flow-c88918	messaging-build	STALE
9a79dc	opus-review-of-af762b	messaging-build	STALE
9e7ea5	mind-astra-of-98ac2e	messaging-build	STALE
7091ea	flow-7091ea	messaging-build	STALE
0347d0	flow-0347d0	messaging-build	STALE
0625c3	flow-0625c3	messaging-build	STALE
0ab019	mind-astra-of-893603	messaging-build	STALE
98ac2e	mind-astra-of-0ab019	messaging-build	STALE
1cb440	field-astra-of-1f96fc	messaging-build	STALE
395aed	field-sol-of-8565e8-remote	messaging-build	STALE
cf3553	field-astra-of-33ba2b	messaging-build	STALE
03e825	flow-03e825	messaging-build	STALE
6db4fe	flow-6db4fe	messaging-build	STALE
df09b6	field-terra-recovery	messaging-build	STALE
21a218	field-reap-luna-21a218	default	STALE
c3e42e	field-sol-of-3b1574	messaging-build	STALE
d2dca6	field-luna-recovery	messaging-build	STALE

$ hm-list | tail -n +2 | wc -l
44
```

`herdr agent list` (raw JSON captured at 16:07Z; fields reduced here to
name / agent / agent_status / terminal title, all values verbatim from the
listing):

| name | agent | status | terminal title (stripped) |
| --- | --- | --- | --- |
| psyche-haiku-of-b80e55 | claude | idle | Psyche Ultra Low (claim pending) |
| psyche-opus-5 | claude | done | Psyche Medium d8df70 |
| psyche-opus-of-d8df70-r2 | claude | working | Psyche Opus e51411 |
| psyche-opus-b87854 | claude | idle | Psyche Opus b87854 |
| psyche-fable-refresh-5f38bc | claude | working | Psyche Fable 38de5b |
| mind-sol-00f95a | codex | working | Mind Sol 00f95a \| primary |
| mind-astra-26c50c | codex | done | Mind Astra 26c50c \| primary |
| field-astra-5f38bc | codex | done | Field Astra 5f38bc \| primary |
| field-sol-b7da5d | codex | done | Field Sol b7da5d \| primary |
| field-luna-e71dab | codex | done | Field Luna e71dab \| primary |
| codex-2d0e71a77a40543c10ac8ac1 | codex | idle | primary |

Registered flow id: taken from the `FLOW` column of `hm-list`; `-` means the
agent is registered with no flow id (psyche-haiku-of-b80e55,
psyche-opus-b87854, codex-2d0e71a77a40543c10ac8ac1).

Presence difference: `herdr agent list` returns 11 agents. `hm-list` returns 44
rows: the same 11, name for name, plus 33 rows marked `STALE`. Every STALE row
is present in `hm-list` and absent from `herdr agent list`. No agent appears in
`herdr agent list` that is missing from `hm-list`. `hm-list` state matches
`herdr` `agent_status` for all 11 live rows.

## 2. Flow Nexus on ouranos [16:07Z]

This host is `ouranos`, so the probe is local. The unit is a user unit; no
system-level flow unit exists.

```
$ systemctl --user list-units --type=service --all | grep -iE "flow|nexus|lojix"
  flow-nexus.service            loaded active running  Flow Nexus
  orchestrate-nexus.service     loaded active running  Orchestrate Nexus path-reservation service
  unity-local-poc-0ab019.service loaded active running [systemd-run] .../flows/0ab019/unity-local-poc/run-local.sh

$ systemctl --user status flow-nexus.service --no-pager
● flow-nexus.service - Flow Nexus
     Loaded: loaded (/home/li/.config/systemd/user/flow-nexus.service; enabled; preset: ignored)
     Active: active (running) since Thu 2026-09-24 16:43:48 CST; 17h ago
 Invocation: 9ff0fe288b47409086abbc4b7b2905e3
   Main PID: 2787342 (flow-nexus)
      Tasks: 2 (limit: 37849)
     Memory: 3.8M (peak: 5.6M)
        CPU: 55ms
     CGroup: /user.slice/user-1001.slice/user@1001.service/app.slice/flow-nexus.service
             └─2787342 /nix/store/...-flow-0.6.0/bin/flow-nexus

Sep 24 16:43:48 ouranos systemd[2067]: Started Flow Nexus.
```

Version, from the unit's ExecStart (the binary takes no `--version`; flag-style
arguments are rejected by contract): `flow-0.6.0`, ExecStart
`/nix/store/…-flow-0.6.0/bin/flow-nexus`, one argv entry, no arguments.
The `flow` CLI on PATH resolves to the same derivation, `flow-0.6.0/bin/flow`.

Sockets present:

```
$ ls -l /run/user/1001/flow/
srw------- 1 li users 0 Sep 24 16:43 flow-meta.sock
srw------- 1 li users 0 Sep 24 16:43 flow.sock
```

Socket answering a status query — partly unwitnessed. The ordinary socket
accepts a connection:

```
$ python3 -c "import socket; s=socket.socket(socket.AF_UNIX); s.settimeout(3); s.connect('/run/user/1001/flow/flow.sock'); print('connected ok'); s.close()"
connected ok
```

No query form for the Flow CLI is documented in
`/home/li/primary/.claude/skills/nexus/SKILL.md`, `SKILL_VARIABLES.md`, or
`flows/5f38bc/log.md` (grep for `flow '` across `.claude/skills/` returns
nothing). Every candidate was rejected by the client before any frame could
reach the Nexus:

```
$ flow 'List'
invalid Flow query: Error { layer: Composition, path: [], kind: Variant { expected: "Query", found: "List" } }
$ flow 'Query'
invalid Flow query: Error { layer: Composition, path: [], kind: Variant { expected: "Query", found: "Query" } }
$ flow 'Query.List'
invalid Flow query: Error { layer: Composition, path: [], kind: Variant { expected: "Query", found: "Query" } }
$ flow 'Query.ListFlows'
invalid Flow query: Error { layer: Composition, path: [], kind: Variant { expected: "Query", found: "Query" } }
$ flow 'Query.All'
invalid Flow query: Error { layer: Composition, path: [], kind: Variant { expected: "Query", found: "Query" } }
$ flow 'Query.{ None }'
invalid Flow query: Error { layer: Composition, path: [], kind: Variant { expected: "Query", found: "Query" } }
$ flow 'Resolve.38de5b'
invalid Flow query: Error { layer: Composition, path: [], kind: Variant { expected: "Query", found: "Resolve" } }
```

The rejection for the literal root `Query` reports `expected "Query", found
"Query"`, so the client refuses even the root it names. Therefore: the unit is
running and its socket accepts connections, but **no reply from the Nexus was
witnessed**; whether it answers a status query is unwitnessed, for want of an
accepted query form on the 0.6.0 client.

## 3. Prometheus [16:07Z–16:08Z]

```
$ ping -c1 -W2 prometheus.goldragon.criome
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 15.826/15.826/15.826/0.000 ms

$ ssh prometheus.goldragon.criome 'date -u +%H:%MZ; hostname; uptime; readlink /nix/var/nix/profiles/system; ip -br link; ip -br addr; ip route; ping -c1 -W2 1.1.1.1'
16:07Z
prometheus
 10:07:53  up  19:05,  0 users,  load average: 0.00, 0.02, 0.00
system-55-link
lo               UNKNOWN        00:00:00:00:00:00 <LOOPBACK,UP,LOWER_UP>
eno1             UP             84:47:09:75:88:68 <BROADCAST,MULTICAST,UP,LOWER_UP>
enp199s0f0u1     UP             00:0e:c6:ad:21:5d <BROADCAST,MULTICAST,UP,LOWER_UP>
wlp195s0         UP             dc:56:7b:fb:76:1f <BROADCAST,MULTICAST,UP,LOWER_UP>
br-lan           UP             46:35:5d:cb:10:a2 <BROADCAST,MULTICAST,UP,LOWER_UP>
yggTun           UNKNOWN        <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP>
tailscale0       UNKNOWN        <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP>
lo               UNKNOWN        127.0.0.1/8 ::1/128
eno1             UP             10.44.0.148/24 metric 1024 fe80::8647:9ff:fe75:8868/64
enp199s0f0u1     UP
wlp195s0         UP             fe80::de56:7bff:fefb:761f/64
br-lan           UP             10.18.0.1/24 fe80::4435:5dff:fecb:10a2/64
yggTun           UNKNOWN        200:ca41:6b12:fba:d7bc:cfc6:4aaa:165f/7 fe80::9128:eac0:6b24:9567/64
tailscale0       UNKNOWN        fe80::6406:4001:3ef0:f224/64
default via 10.44.0.1 dev eno1 proto dhcp src 10.44.0.148 metric 1024
10.18.0.0/24 dev br-lan proto kernel scope link src 10.18.0.1
10.44.0.0/24 dev eno1 proto kernel scope link src 10.44.0.148 metric 1024
10.44.0.1 dev eno1 proto dhcp scope link src 10.44.0.148 metric 1024
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 65.521/65.521/65.521/0.000 ms

$ ssh prometheus.goldragon.criome 'ip -br link show master br-lan; ethtool enp199s0f0u1; ethtool eno1; nixos-rebuild list-generations; ip neigh show dev br-lan'
enp199s0f0u1     UP             00:0e:c6:ad:21:5d <BROADCAST,MULTICAST,UP,LOWER_UP>
wlp195s0         UP             dc:56:7b:fb:76:1f <BROADCAST,MULTICAST,UP,LOWER_UP>
(ethtool produced no output on either interface — ethtool is not on PATH there;
 `command -v ethtool` exited 1)
Generation  Build-date           NixOS version           Kernel  Configuration Revision  Specialisation  Current
55          2026-09-24 21:03:26  26.11.20260813.0e251e2  7.1.8   Unknown                 []              True
10.18.0.103 lladdr 90:2e:16:47:ea:e3 REACHABLE
10.18.0.2 FAILED
fe80::9ca9:3db7:4354:3cd1 lladdr 90:2e:16:47:ea:e3 STALE
```

Reading: reachable by ICMP, 15.8 ms. Generation 55 (`system-55-link`, built
2026-09-24 21:03:26, NixOS 26.11.20260813.0e251e2, kernel 7.1.8), the only
generation `list-generations` reports and marked Current. Uptime 19:05.
Bridge `br-lan` is UP with 10.18.0.1/24 and has two members: the USB NIC
`enp199s0f0u1` and the Wi-Fi `wlp195s0`. Both members are UP with
LOWER_UP; the USB NIC carries no address of its own, as a bridge port
should not. Uplink is the integrated NIC `eno1`, 10.44.0.148/24. Default
route exists, `via 10.44.0.1 dev eno1`, and an external address answers:
one ping to 1.1.1.1, 1/1 received, 65.5 ms.

## 4. Zeus link [16:08Z]

Zeus sits on Prometheus's downlink subnet 10.18.0.0/24 as 10.18.0.103, which
is the `REACHABLE` neighbour on `br-lan` above, MAC 90:2e:16:47:ea:e3.

Carrier on Prometheus's downlink port (ethtool absent; read from sysfs, which
is the same carrier bit `ethtool`'s "Link detected" reports):

```
$ ssh prometheus.goldragon.criome 'cat /sys/class/net/enp199s0f0u1/carrier /sys/class/net/enp199s0f0u1/speed'
1
1000
```

Zeus's own view:

```
$ ssh zeus.goldragon.criome 'date -u +%H:%MZ; hostname; ip -br link; ip -br addr; ip route; ping -c1 -W2 1.1.1.1'
16:08Z
zeus
lo               UNKNOWN        00:00:00:00:00:00 <LOOPBACK,UP,LOWER_UP>
enp0s31f6        UP             90:2e:16:47:ea:e3 <BROADCAST,MULTICAST,UP,LOWER_UP>
wlp0s20f3        UP             14:85:7f:6b:99:e1 <BROADCAST,MULTICAST,UP,LOWER_UP>
yggTun           UNKNOWN        <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP>
lo               UNKNOWN        127.0.0.1/8 ::1/128
enp0s31f6        UP             10.18.0.103/24 fe80::9ca9:3db7:4354:3cd1/64
wlp0s20f3        UP             192.168.1.5/24 2806:262:b480:1076:46d6:3339:aa53:19f1/64 …
yggTun           UNKNOWN        200:17f7:4fad:e50b:a50c:2048:2169:41f7/7 fe80::5e7f:47ac:bdd2:d33f/64
default via 10.18.0.1 dev enp0s31f6 proto dhcp src 10.18.0.103 metric 100
default via 192.168.1.1 dev wlp0s20f3 proto dhcp src 192.168.1.5 metric 600
10.18.0.0/24 dev enp0s31f6 proto kernel scope link src 10.18.0.103 metric 100
192.168.1.0/24 dev wlp0s20f3 proto kernel scope link src 192.168.1.5 metric 600
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 66.390/66.390/66.390/0.000 ms

$ ssh zeus.goldragon.criome 'cat /sys/class/net/enp0s31f6/carrier /sys/class/net/enp0s31f6/speed; readlink /nix/var/nix/profiles/system; uptime'
1
1000
system-72-link
 10:08:35  up 7 days 23:08,  0 users,  load average: 0.20, 0.27, 0.22
```

Reading: carrier is up at 1000 Mb/s on both ends of the Prometheus–Zeus wire.
Zeus holds a DHCP lease from Prometheus (10.18.0.103) and prefers Prometheus's
default route (metric 100) over its own Wi-Fi (metric 600). Zeus has internet:
one ping to 1.1.1.1, 1/1 received, 66.4 ms. Zeus system profile is
`system-72-link`; uptime 7 days 23:08.

Note: neighbour 10.18.0.2 on `br-lan` is `FAILED`. Not investigated, out of
scope for this witness.

## 5. Lojix on ouranos [16:07Z]

```
$ systemctl status lojix.service --no-pager
● lojix.service - Lojix Nexus
     Loaded: loaded (/etc/systemd/system/lojix.service; enabled; preset: ignored)
     Active: active (running) since Thu 2026-09-24 16:14:33 CST; 17h ago
   Main PID: 2674994 (lojix-nexus)
     CGroup: /system.slice/lojix.service
             └─2674994 /nix/store/…-lojix-7.0.0/bin/lojix-nexus
Sep 24 16:14:33 ouranos systemd[1]: Started Lojix Nexus.
Sep 24 16:14:33 ouranos …-lojix-nexus-service-user-gpg-agent[2674994]: (LojixNexusReady /run/lojix/ordinary.sock /run/lojix/meta.sock)

$ lojix --version
(CliRejected [flag-style arguments are not part of component binaries: --version])

$ readlink -f /run/current-system/sw/bin/lojix
/nix/store/…-lojix-7.0.0/bin/lojix
```

No one-line version query exists: the lojix skill documents only datom
requests, and the CLI rejects flags by contract. Versions taken from the
derivation names instead: daemon `lojix-7.0.0` (from the running unit's
ExecStart path), client `lojix-7.0.0` (from the resolved CLI path). Client and
daemon are the same version but are two distinct store paths, i.e. two
different builds of the same version, so this is a version match, not a
same-build match. The unit's own startup line announces
`/run/lojix/ordinary.sock` and `/run/lojix/meta.sock`, while the environment
sets `LOJIX_OWNER_SOCKET=/run/lojix/owner.sock` — a name mismatch worth a
separate look, not witnessed further here.
