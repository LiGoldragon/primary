# Routed microVM standup — host state recon (READ-ONLY)

Read-only reconnaissance to ground a safe plan for standing up a routed
microVM as the lojix e2e test target. No host was mutated; every command
below was inspection-only (ip/readlink/ls/nproc/free/systemctl-status/command-v).

## Cluster definition (source of truth)

`/git/github.com/LiGoldragon/goldragon/datom.nota` — a horizon-rs
`ClusterProposal` (positional NOTA, schema in
`/git/github.com/LiGoldragon/horizon-rs/lib/src/node.rs`). Node species and
their derived behaviour flags:

| Node | Species (datom.nota line) | Derived behaviour (node.rs) | Notes |
|---|---|---|---|
| balboa | `Center` (L6) | center, low-power | Arm64 rock64 SD-card node |
| ouranos | `EdgeTesting` (L28) | edge, next_gen, low_power | THIS workstation (ThinkPad T14 Gen5) |
| prometheus | `LargeAiRouter` (L59) | **router=true**, large_ai, center | **HIGH RISK — the cluster router** |
| tiger | `EdgeTesting` (L98) | edge, next_gen, low_power | resolves but unreachable (ssh timeout) |
| zeus | `Edge` (L126) | edge, low_power | ThinkPad T14 Gen2 |

Species → behaviour mapping: `TypeIs::from_species` (node.rs:166-179);
`BehavesAs` derivation `edge_testing => next_gen + low_power`,
`large_ai_router => router + center` (node.rs:186-196). So prometheus is the
only node carrying `router: true`.

Note: the datom labels zeus `Edge` (L126) and ouranos `EdgeTesting` (L28),
which differs from the prompt's loose grouping. Grounded in the file, zeus is
a plain `Edge`, tiger is `EdgeTesting`.

## Per-host inspection (read-only ssh over Yggdrasil 200::/7)

### prometheus.goldragon.criome — REACHABLE
- Role: **LargeAiRouter / router=true** — the live cluster router. Do NOT
  make networking changes here.
- KVM: **yes** — `crw-rw-rw- root kvm 10,232 /dev/kvm`.
- Generation: `nixos-system-prometheus-26.05.20260422.0726a0e`; NixOS
  `26.05.20260422.0726a0e (Yarara)`.
- Resources: nproc 32, mem 124Gi total / 121Gi available (huge headroom).
- system-running: `running`; no failed units.
- Networking (live routing surface — fragile):
  - `eno1` UP `192.168.18.94/24` (uplink LAN)
  - `br-lan` UP `10.18.0.1/24` — **the cluster bridge / gateway** (clients on
    10.18.0.0/24, e.g. zeus is 10.18.0.106)
  - `wlp195s0` + `wlp199s0f0u4` UP — the two router wifi radios declared in
    datom.nota L95 (`routerWifiSaePasswords` + `criome-backup`)
  - `tailscale0`, `yggTun` `200:ca41:.../7`
- Virt tooling: `qemu-system-x86_64` / `microvm` / `virsh` **NOT** on PATH;
  no `/var/lib/microvms`, no microvm units.

### zeus.goldragon.criome — REACHABLE
- Role: `Edge` (datom.nota L126) — not a router, not a center. Safe blast
  radius for experimentation.
- KVM: **yes** — `/dev/kvm` present; `kvm_intel` + `kvm` modules loaded.
- Generation: `nixos-system-zeus-26.05.20260422.0726a0e` (same Yarara build as
  prometheus).
- Resources: nproc 8, mem **15Gi total / ~9.6Gi available** (modest — a
  microVM must be sized small; 5.7Gi already in use).
- system-running: `running`; no failed units.
- Networking: `wlp0s20f3` UP `10.18.0.106/24` (DHCP client on prometheus's
  br-lan), `yggTun` `200:17f7:.../7`. Wired `enp0s31f6` DOWN. **No bridges
  present** — a microVM host bridge would need to be added.
- Virt tooling: `qemu-system-x86_64` and `virsh` **already on PATH**
  (`/run/current-system/sw/bin/`). No microvm units / `/var/lib/microvms` yet.

### tiger.goldragon.criome — UNREACHABLE
- DNS resolves (`202:3895:9c1b:16:8c36:4f28:66fe:85fc`) but
  `ssh ... port 22: Connection timed out`. Powered off or off-network. Not
  inspectable this session.

### balboa — UNREACHABLE
- No hostname resolution under `goldragon.criome` / `criome` / bare. Arm64
  SD-card node, not a candidate.

## First read on the safest microVM host
**zeus** is the safest target: it is a plain `Edge` node (zero router/center
responsibility), already has KVM + qemu + virsh present, runs the identical
26.05 generation, and is reachable. Its only weakness is RAM
(~9.6Gi free) — the microVM and its routed test network must be sized small,
and a host bridge/tap must be created (none exists today).
prometheus has vastly more capacity and KVM, but it is the live cluster
router (`br-lan` gateway, two wifi radios) — any networking change there is
high risk and should be avoided for this task.
