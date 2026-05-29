# 10 · Operator checklist — finish the single-try boot + build the USB backup network (2026-05-28)

Things cloud-operator should make sure of, for two threads now in play
on prometheus:

1. **Finish the in-progress single-try-boot Gemma/auth deploy** — it is
   NOT done yet (psyche 2026-05-28). This is the prerequisite.
2. **Then build the USB backup admin network** the psyche asked for —
   sturdy, independent, survives an OS switchover (records 1144 + 1145).

Lane split (psyche 2026-05-28): cloud-designer designs, cloud-operator
implements. Sequencing the psyche set: single-try boot first, then add
the routing interfaces and rebuild that version for a fresh prometheus
deploy.

## Don't rebuild from scratch — the backup network is already half-declared

The most important thing to know before you start: **the backup wifi is
already in the datom and already supported by the router module.** Do
not re-invent it; extend it.

The goldragon datom (`goldragon/datom.nota:94`) already gives prometheus
a full `routerInterfaces` record, backup leg included:

```
(Some (eno1 wlp195s0 TwoG 6 Wifi4
       (Some (routerWifiSaePasswords))
       (Some (wlp199s0f0u4 [CRIOM Backup] TwoG 11 Wifi4 (routerBackupWifiPassword)))))
```

Decoded (positional `RouterInterfaces`, source-decl order):

| Pos | Value | Meaning |
|---|---|---|
| 1 | `eno1` | WAN uplink interface |
| 2 | `wlp195s0` | main WLAN / AP interface |
| 3 | `TwoG` | main band (2.4 GHz) |
| 4 | `6` | main channel |
| 5 | `Wifi4` | main wifi generation |
| 6 | `(Some (routerWifiSaePasswords))` | main WPA3-SAE password → sops secret `routerWifiSaePasswords` |
| 7 | `(Some (…backup…))` | backup wireless leg (below) |

Backup leg (`wlp199s0f0u4 [CRIOM Backup] TwoG 11 Wifi4 (routerBackupWifiPassword)`):

| Pos | Value | Meaning |
|---|---|---|
| 1 | `wlp199s0f0u4` | backup AP interface — **this is the USB wifi dongle** (`…f0u4` = USB path) |
| 2 | `[CRIOM Backup]` | backup SSID |
| 3 | `TwoG` | band (2.4 GHz) |
| 4 | `11` | channel |
| 5 | `Wifi4` | wifi generation |
| 6 | `(routerBackupWifiPassword)` | backup WPA3-SAE password → sops secret `routerBackupWifiPassword` |

And the router module (`CriomOS/modules/nixos/router/default.nix`)
already consumes that backup leg: `backupWireless = routerInterfaces.backupWireless`,
a **separate `hostapd-backup.service`** on the backup phy (the module
comment literally says *"Backup wireless (optional) — independent
hostapd on a separate phy"*), with its own sops secret whose
`restartUnits = [ "hostapd-backup.service" ]`. Main is `hostapd-main`
with `restartUnits = [ "hostapd-main.service" ]`.

So the AP definition exists. What's missing is **independence** (below)
and the **secret + USB-ethernet** wiring.

## Thread 1 — finish the single-try boot FIRST (in progress, not done)

State on prometheus (from reports 8 + 9): booted the working **old gen
40**; the new **gen 44** (Gemma 4 multimodal + sops-fed llama auth) is
built/cached on prometheus and staged as a **revertible BootOnce
one-shot** (default stays gen 40). The single-try-boot transition itself
is not finished — close it before layering the USB-routing work.

Make sure of:

- **Never `Switch` the router node live.** A live activation stops
  `hostapd` / `dnsmasq` / `kea` — the very services your ssh rides — and
  the half-finished activation is killed, leaving prometheus unreachable
  (it happened twice; records 1105, 1117). Use **`BootOnce`** (revertible)
  or `Boot`; `switch-to-configuration test` only if you need live-without-
  changing-boot-default. Record 1125.
- **Build on prometheus** (`builder = prometheus`); never realize the
  models on the local host.
- **Console / out-of-band access is still the core exposure** (bead
  `primary-lome`). The USB backup AP reduces this risk but does not
  replace real console — get both.
- **Coordinate with system-operator** on the router-wifi projection
  before activating: the recent *"derived router wifi names"* work is
  what restarted `hostapd-main` and caused the incident, and it is
  explicitly fragile. Confirm the main SSID / interface / SAE password
  projection is right for prometheus. (Note an apparent main-wifi
  mismatch worth their eyes: clients in `wifi-eap.nix` use
  WPA3-**Enterprise** EAP-TLS on SSID `criome`, but the router's
  `hostapd-main` serves WPA3-**SAE** with `wirelessNetworkName` defaulting
  to `${cluster.name}.criome`. Reconcile before relying on the main AP.)
- Detail / beads for this thread already exist: report 9 and beads
  `primary-lome` (console), `primary-b7qc` (merge lojix-cli branch),
  `primary-fq9l` (deploy via BootOnce), `primary-ytdj` (verify vision),
  `primary-ia60` (router-wifi + password with system-operator).

## Thread 2 — make the backup truly sturdy (records 1144 / 1145)

The psyche's goal: a backup connection path that **survives an OS
upgrade and a main-router-service switchover**, so admin access can never
be lost the way it was in the incident. It must be a *dumb, sturdy
router* — plain `systemd-networkd` + simple DHCP + forwarded DNS,
deliberately **independent of the main `kea` / `dnsmasq` / `hostapd`
stack** — on the just-attached USB hardware (one USB wifi = backup AP,
two USB ethernet = master wired interface).

Four gaps to close. These are the real "make sure of" items.

### Gap 1 — the backup is on a separate radio but NOT on an independent lifecycle

`hostapd-backup` is a separate service, but it lives inside the same
`config = mkIf behavesAs.router { … }` block as everything else, and
(verify in the part of the module past the hostapd config — the
secret-guard hook blocks bulk printing of that section) the backup AP
most likely bridges into the **same `br-lan`** and is served by the
**same `kea` DHCP + `dnsmasq` DNS**. If so, a switch that restarts
`networkd` / `br-lan` / `kea` / `dnsmasq` disrupts the backup too — which
defeats the point.

Make sure: the backup AP comes up on **its own subnet, its own
networkd-served DHCP, and its own forwarded DNS**, NOT bridged into
`br-lan` and NOT dependent on `kea`/`dnsmasq`. The existing
`modules/nixos/network/networkd.nix` `20-usb-eth` block is the right
shape to copy: a static `Address`, `DHCPServer = true`,
`IPMasquerade = "ipv4"`, plain `dhcpServerConfig`, with
`resolved`/static upstream for DNS.

**Acid test for independence:** with the backup AP up, restarting
`hostapd-main`, `kea`, and `dnsmasq` (i.e. simulating a main-stack
switch) must leave `CRIOM Backup` serving and routable to the internet.
If that holds, a future main-stack `Switch` becomes survivable — you
reconnect over `CRIOM Backup`.

### Gap 2 — USB ethernet is gated OFF on the router node

`modules/nixos/network/networkd.nix:15` is
`mkIf (behavesAs.center && !behavesAs.router)`. prometheus is a router,
so that whole module — including the `20-usb-eth` master-interface logic
(10.47.0.x/24, DHCPServer, masquerade) — **does nothing on prometheus
today.** The two USB ethernet dongles are dark.

Make sure: bring an equivalent USB-ethernet master interface onto the
router node (un-gate, or add a router-node variant of `20-usb-eth`), as a
sturdy wired admin path with its own subnet + DHCP + masquerade,
independent of `br-lan` / `kea`. This is the most reliable backup of all
(wired, no radio).

### Gap 3 — the `routerBackupWifiPassword` sops secret must exist AND be wired into lojix

The router module **throws** if `inputs.secrets.sopsFiles.routerBackupWifiPassword`
is missing. This is the same pattern as `localLlmApiToken`: a new secret
needs three things, all done blind (never view the value —
`skills/secrets.md`):

1. **Mint** a password into gopass — per record 1145 it must be
   **human-readable and randomly generated** (so it can be typed on a
   phone for emergency access), not a base64 blob.
2. **Bridge** it to a sops file age-encrypted to prometheus (recipient
   `age1wgft…`), in `goldragon/secrets/`.
3. **Wire** it into `lojix-cli/src/artifact.rs` — the `SECRETS_FLAKE_TEMPLATE`
   hardcodes the secret set; `routerBackupWifiPassword` must be added there
   exactly as `localLlmApiToken` was, or the generated secrets flake won't
   carry it.

Verify by whether the build throws, not by reading the file.

### Gap 4 — confirm the projection with system-operator

The datom backup leg and the secret name are designer-side; the
horizon-rs router-wifi **projection** (how `routerInterfaces` lowers into
`hostapd` config, SSIDs, interface names) is system-operator's domain and
is the fragile area that caused the incident. Confirm the backup leg
projects correctly (SSID `CRIOM Backup`, interface `wlp199s0f0u4`, SAE
from `routerBackupWifiPassword`) before deploying.

## Consolidated checklist

- [ ] Finish + verify the single-try boot of gen 44 (router intact, both
      Gemma models serving, auth rejects tokenless requests, vision
      works); commit permanent if clean, power-cycle to revert if not.
- [ ] Never `Switch` the router live; `BootOnce`/`Boot` only.
- [ ] Build on prometheus; nothing realized locally.
- [ ] Don't rebuild the backup AP — extend the existing `backupWireless`
      / `hostapd-backup` path.
- [ ] Decouple the backup AP from `br-lan` / `kea` / `dnsmasq`: own
      subnet, networkd DHCP, forwarded DNS; pass the acid test.
- [ ] Enable a USB-ethernet master interface on the router node
      (`networkd.nix` is gated off for routers today).
- [ ] Mint (human-readable, blind) → sops → lojix `artifact.rs` the
      `routerBackupWifiPassword` secret; verify by build, not by reading.
- [ ] Confirm the router-wifi projection (main + backup) with
      system-operator before activating.
- [ ] Get real console/out-of-band access (bead `primary-lome`).

## Recommended order

1. Close out thread 1 (gen 44 boot, verify, commit/revert).
2. Mint + wire `routerBackupWifiPassword` (blind).
3. Bring up the backup network independently (backup AP off `br-lan`;
    USB-ethernet master interface on) — designer to detail the module
    shape, operator implements.
4. Prove independence with the acid test on prometheus.
5. Build on prometheus, deploy via `BootOnce`, reboot, verify, commit.

## Open design questions (cloud-designer to resolve; flag to psyche)

- **New module vs restructure.** Put the backup network in a new module
  (e.g. `modules/nixos/router/backup-net.nix`) deliberately *outside* the
  coupled `mkIf behavesAs.router` lifecycle, or lift the backup leg out of
  the main module? Independence pushes toward a separate module.
- **Backup DNS shape.** Plain forwarded DNS to a static upstream
  (`1.1.1.1`) handed via DHCP, vs a tiny `resolved` forwarder — the psyche
  said "basic forwarded DNS, dumb router." Keep it `dnsmasq`-free so it
  doesn't share the main resolver's lifecycle.
- **Backup internet.** The psyche wants the backup to keep "its internet
  access that it still has" → masquerade the backup subnet to the WAN, not
  LAN-only.

## Anchors

- Datom backup leg: `goldragon/datom.nota:94`.
- Router module: `CriomOS/modules/nixos/router/default.nix`
  (`backupWireless`, `hostapd-main` / `hostapd-backup`).
- USB-ethernet shape + router gating:
  `CriomOS/modules/nixos/network/networkd.nix` (`20-usb-eth`, line 15 gate).
- Incident + deploy safety: reports 8 and 9; secret discipline:
  `skills/secrets.md`; remote-form deploys: `skills/nix-discipline.md`.
- Intent: records 1105, 1117, 1125 (deploy safety), 1144 (backup-path
  requirement), 1145 (USB backup-network design).
