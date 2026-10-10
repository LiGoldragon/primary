# Zeus probe — passive, read-only (b860be, 2026-09-26)

Brief: the living, relayed by e167d8 — "Make sure Zeus is updated." Determine
whether the host Zeus can be brought to tonight's integrated state through
Lojix. Nothing changed, nothing sent.

## 1. Cluster data

Goldragon checkout: `/home/li/wt/github.com/LiGoldragon/goldragon-b860be-check`,
a `jj` working copy whose `cluster-definition.datom` is byte-identical
(`diff` clean) to `jj file show -r main cluster-definition.datom`, and
`main` there resolves to `ddf27e0c28bfdd98bf36dcb580ab51abc2c6c40b` — the
exact commit named in the brief.

Zeus's exact node entry, verbatim from `cluster-definition.datom`:

```
{ zeus
  Installation.{ Uefi
    [ { /dev/disk/by-uuid/4bd0cbe7-082d-4f06-9283-978b834a85db / Ext4 [] }
      { /dev/disk/by-uuid/1491-B84C /boot Vfat [ fmask=0022 dmask=0022 ] } ]
    [] }
  Max Max
  Metal.{ X86_64 { 4 Some.ThinkPadT14Gen2Intel None Some.12 None None } }
  { Colemak None }
  { [] None None [] None }
  { AAAAC3NzaC1lZDI1NTE5AAAAIMAZxp1YpShbxSy1/Khu4wc57o+yWyuMh/80+dKHg6TW
    Some.35/dVZHU8IKAHRMLgmYKW8ZulqATh4sSueMkthLVM2g=
    Some.{ f40458290d7a2d79efdbef4b5f046fb7f825626eda9d118e4f2b869c105f6ec4
           200:17f7:4fad:e50b:a50c:2048:2169:41f7
           300:17f7:4fad:e50b } }
  None
  [ Edge.{} LowPower.{} HardwareVideo.{} ]
  None
}
```

Read plainly:

- **name**: `zeus`.
- **machine**: `Metal.{ X86_64 { 4 Some.ThinkPadT14Gen2Intel None Some.12 None None } }`
  — bare metal x86_64, 4 cores, ThinkPad T14 Gen2 Intel, 12 (RAM, unit
  unstated in the raw datom).
- **the two tier fields before `Metal`** (`Max Max`): same values as
  Prometheus's and Tiger's entries. The schema name for these two fields
  was not found in a read source in this pass (searched CriomOS,
  horizon-rs, schema-rust, protos, core-schema for a `Trust` enum
  definition without a hit); reported as raw positions, not renamed.
- **network placement**: the `{ [] None None [] None }` field is empty —
  no static/router-declared address for zeus, unlike Prometheus's LAN
  block. The identity block that follows (`{ AAAAC3… Some.35/dV… Some.{
  f4045829… 200:17f7:4fad:e50b:… 300:17f7:4fad:e50b } }`) carries an SSH
  host key plus a Yggdrasil-shaped identity/address pair
  (`200:…` / `300:…`), the same shape ouranos and prometheus carry.
- **roles**: `[ Edge.{} LowPower.{} HardwareVideo.{} ]` only. No
  `TailnetClient`, no `TailnetController`, no `NixBuilder` entry at all
  (contrast Tiger, which explicitly carries `NixBuilder.None`), and no
  `UsbDownlink`.
- **daisy-chain / USB-downlink question**: in the schema itself, the
  `UsbDownlink` capability belongs to **Ouranos** (`UsbDownlink.{
  10.44.0.0/24 }`), not Prometheus — confirmed both in
  `cluster-definition.datom`'s ouranos entry and in
  `/git/github.com/LiGoldragon/goldragon/UPGRADES.md:19-20`: "Ouranos
  declares `UsbDownlink.{ 10.44.0.0/24 }`. Prometheus declares none: its
  Router LAN already is `10.18.0.0/24`." Zeus is not that role's leaf.
  Separately, the living's own design (`flows/753e69/vision/
  transitiveNetworkTopologyAndCertificateWifi.md:12`, quoted in
  `flows/752e0f/reports/zeus-link-and-mesh-2026-09-25.md`) describes an
  *unmodeled physical* cable: "Prometheus has a USB Ethernet that goes to
  Zeus... The built-in port is for upstream, and the USB is for
  downstream." That physical Prometheus→Zeus leg is real by the living's
  own account but is not represented by a `UsbDownlink` role in
  cluster-definition — Zeus instead showed up (2026-09-23 evidence) as an
  ordinary client of Prometheus's `br-lan` (`10.18.0.0/24`), the Router
  role's own LAN, not a declared USB-downlink subnet.
- **NixBuilder**: none on zeus. The cluster's NixBuilder is
  `prometheus.goldragon.criome` (skill variable), matching Prometheus's
  own `NixBuilder.Some.8` role entry.

## 2. Reachability

Canonical hostname: `zeus.goldragon.criome` (`<node>.<cluster>.<internal
suffix>`; suffix `criome` from the TailnetController certificate SAN on
Ouranos's own cluster-data entry, and matching every prior witness).

Probed from `ouranos` (this session's own host, confirmed by `hostname`),
2026-09-26 01:40–01:41 CST:

- `ping -c1 -W2 zeus.goldragon.criome` — **succeeded**, 1/1 received,
  17.6 ms, resolved to `200:17f7:4fad:e50b:a50c:2048:2169:41f7`.
- `ip route get 200:17f7:4fad:e50b:a50c:2048:2169:41f7` — routed `dev
  yggTun` (the Yggdrasil overlay tunnel), src
  `201:6de1:5500:7cac:2db9:759e:42d2:fb1d`. The route is the Yggdrasil
  overlay, not a raw hop through Prometheus's physical USB link — the
  overlay abstracts whatever physical path (USB-Ethernet or Wi-Fi
  `br-lan`) currently carries it, and this probe cannot see which one
  underlies it.
- `ssh -o BatchMode=yes -o ConnectTimeout=5 -o StrictHostKeyChecking=yes
  root@zeus.goldragon.criome true` — **succeeded** (exit 0).
- `ssh -o BatchMode=yes -o ConnectTimeout=5 -o StrictHostKeyChecking=yes
  li@zeus.goldragon.criome true` — **succeeded** (exit 0).

This reverses the prior witness in `flows/3cb84d07/witnesses/
zeusConnectivity.md`, where the same route (`yggTun`) gave no ICMP reply
and both TCP/22 and SSH timed out. Zeus is live and answering now.

## 3. Lojix state

```
$ lojix 'Query.ByNode.{ goldragon zeus None }'
Queried.{ [] [] { 824 824 } }
```

Both the host-generation vector and the user-environment-generation
vector are **empty**. Zeus has **no recorded Lojix generations and no
recorded deployments at all** — sanity-checked against the same query for
ouranos (`Query.ByNode.{ goldragon ouranos None }`), which returns a
populated generation list and deployment history with real commits
(e.g. its `CompleteHost`/`Current` generation at commit
`36653a125de8f14518af2dddf89333610891d140`), so the query form is correct
and zeus's empty result is a real absence, not a malformed request.

There is therefore no "Current CriomOS commit" for zeus to compare
against tonight's main (`e6a83edc`, confirmed as CriomOS `main`'s current
tip: `e6a83ed Pin lojix 8.0.0 (horizon 0.13.0 repin train)`) or the coming
step-2 revision. Zeus is not "N commits behind" — Lojix has never deployed
to it. A `CompleteHost` deploy tonight would be zeus's **first** Lojix
deployment, not a catch-up.

## 4. On Zeus (read-only, via SSH as `li`)

```
$ df -h /nix/store
/dev/nvme0n1p2  468G  257G  188G  58% /nix/store

$ nixos-version
26.11.20260813.0e251e2 (Zokor)

$ uptime
 01:41:00  up 8 days 14:40,  0 users,  load average: 0.29, 0.25, 0.21

$ readlink /run/current-system
/nix/store/kgg7yk3b22w0dakn9sz3l6nz23rcw5ly-nixos-system-zeus-26.11.20260813.0e251e2

$ readlink /run/booted-system
/nix/store/kgg7yk3b22w0dakn9sz3l6nz23rcw5ly-nixos-system-zeus-26.11.20260813.0e251e2
```

`/run/current-system` and `/run/booted-system` match each other (no
pending unapplied activation). Neither matches any Lojix "Current" record,
because Lojix holds no record for zeus at all — the live system on zeus
predates any Lojix-tracked deployment for this node.

## 5. Clock

```
$ date
Sat Sep 26 01:40:49 AM CST 2026
```

## Semantic outcome

- **In cluster data**: yes — `zeus` is a defined node (`Metal.{ X86_64 …
  }`, roles `Edge{} LowPower{} HardwareVideo{}`). No `TailnetClient`,
  `TailnetController`, `NixBuilder`, or `UsbDownlink` role. It is not the
  formal `UsbDownlink`-role daisy-chain leaf (that role is Ouranos's); it
  is, by the living's own description and by the one dated observation
  found, an ordinary client of Prometheus's Router LAN, reached today over
  the Yggdrasil overlay (`yggTun`), not confirmed against the physical USB
  cable specifically.
- **Reachable**: yes, right now — ping, `ssh root@…`, and `ssh li@…` all
  succeeded via `zeus.goldragon.criome` routed over `yggTun`. This is a
  reversal of the most recent prior witness (unreachable, same route).
- **Lojix Current vs main**: no comparison possible — Lojix holds zero
  generations and zero deployments for zeus. Tonight's main is `e6a83edc`
  (current CriomOS `main` tip). Zeus is not behind by a distance; it has
  never been deployed through Lojix.
- **Disk headroom**: 188G free of 468G on `/nix/store` (58% used) —
  ample for a `CompleteHost` deploy.
- **Blocker for a `CompleteHost` deploy tonight**: none found in
  reachability or disk space. The one open fact worth flagging to the
  main flow: this would be zeus's first-ever Lojix-tracked deployment, so
  there is no established `Current` baseline to diff against or roll back
  to on this node, and the deploy proposal/transport for zeus (Nix store
  URI + SSH destination pair for `CompleteHost`) has not itself been
  constructed or verified in this pass — only reachability, cluster data,
  and live host state were probed, per the passive-only brief.
