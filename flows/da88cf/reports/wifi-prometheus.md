# Wi-Fi from Prometheus: the assembled picture

Subflow of da88cf, read-only. Observed on ouranos and over read-only ssh to Prometheus, 2026-09-25 21:00–21:20 local time (CST, UTC−6). Nothing was changed on any host, repository, or NetworkManager profile.

Grades: **[O]** observed directly in this run; **[R]** read from a retained report or transcript (the author's claim, not re-witnessed here); **[I]** my inference; **[U]** unknown.

## 0. Short answer

- **The feature already exists and is enabled in cluster data** [O]. In `goldragon/cluster-definition.datom`, Prometheus carries the `Router.{}` capability and a `RouterInterfaces` record: WAN `eno1`, AP radio `wlp195s0`, 2.4 GHz, channel 6, Wi-Fi 4, WPA3-SAE password reference `routerWifiSaePasswords`, and a backup AP on the USB radio `wlp199s0f0u4` (SSID `criome-backup`, channel 11, secret `routerBackupWifiPassword`). CriomOS `modules/nixos/router/default.nix` on `main@origin` turns that into hostapd, a `br-lan` bridge at 10.18.0.1/24, Kea DHCP, NAT to the WAN, and WAN lease recovery.
- **The AP is broadcasting again right now** [O]. Prometheus was powered off from 12:55 to 21:15 today. Its previous boot's journal ends at 12:55:13, and no new pstore panic was written. At 21:19, `wlp195s0` is `type AP`, `ssid goldragon.criome`, channel 6. Ouranos's scan lists `goldragon.criome` (BSSID DC:56:7B:FB:76:1F, WPA3, signal 42).
- **The laptop's Wi-Fi to Prometheus was switched off by an agent, not by the living** [O][R]. On ouranos, the NetworkManager profile `goldragon.criome` has `autoconnect=no` and was last used 09-24 14:51 local. The kernel logged `deauthenticating from dc:56:7b:fb:76:1f by local choice` at 14:51:00. The d8df70 transcript shows who did it, at 2026-09-24T20:50Z:
  - The command was `nmcli con modify goldragon.criome connection.autoconnect no; nmcli con down goldragon.criome`. d8df70 called it "Wi-Fi A".
  - The instruction came as a relay from e51411: "the living said to stop asking and deploy everything, so take your recommendation, Wi-Fi A, and apply it now: keep ouranos off Prometheus's access point."
  - The reason was to remove the suspected trigger of Prometheus's mt7925 kernel panics: ouranos's Wi-Fi kept dropping and reassociating to the AP.
  - The profile is imperative only. It is not declared in CriomOS or CriomOS-home, so a rebuild neither restores it nor keeps it off.
- **No declared client-side feature exists.** Nothing in cluster data makes a node, such as ouranos or the living's devices, join the cluster AP. The one Wi-Fi client module, `network/wifi-eap.nix`, is gated by the `WifiCertificate` capability and targets an EAP-TLS SSID `criome`, which no AP serves. The AP serves WPA3-SAE `goldragon.criome`. No node carries `WifiCertificate`.

## 1. Prometheus in cluster data

Repository: `/git/github.com/LiGoldragon/goldragon`, head `8c4d03d`, `cluster-definition.datom`. The goldragon flake composes it with `criomos-horizon-config` through Horizon, and Lojix receives the result as `ProposalSource`.

| Field | Prometheus value [O] |
|---|---|
| Installation | UEFI, btrfs subvolumes root/home/nix/var |
| Size / trust | Max / Max |
| Machine | `Metal.{ X86_64 { 8 Some.«GMKtec EVO-X2» … 128 GB } }` |
| Keyboard | Qwerty |
| Network | link-local none; node IP `5::5/128`; `RouterInterfaces.{ eno1 wlp195s0 TwoG 6 Wifi4 Some.{routerWifiSaePasswords} Some.BackupWireless.{ wlp199s0f0u4 criome-backup TwoG 11 Wifi4 {routerBackupWifiPassword} } }` |
| Yggdrasil | `200:ca41:6b12:fba:d7bc:cfc6:4aaa:165f` (resolves as `prometheus.goldragon.criome`) |
| Online | `Some.True` |
| Capabilities | `Center LargeAi Router TailnetClient NixBuilder.Some.6 NixCache VmHost.{169.254.100.0/22 Available Some.4}` |

Schema (`horizon-rs/lib/ethos/horizon.ethos`):

- `RouterInterfaces.{ Interface(wan) Interface(wlan) WlanBand Integer(channel) WlanStandard Option<SecretReference> Option<BackupWireless> }`
- `BackupWireless.{ Interface WirelessNetworkName WlanBand Integer WlanStandard SecretReference }`

There is **no SSID or country field** on the primary AP. CriomOS falls back to SSID `"${cluster}.criome"`, which is `goldragon.criome`, and to country `"PL"`.

Ouranos in the same file carries `Edge LowPower NextGeneration Nordvpn HardwareVideo TailnetClient TailnetController NixBuilder.None OpenCodeTesting PersonaDevelopment`. It has no Router, no WifiCertificate, and no RouterInterfaces. Zeus carries `Edge LowPower HardwareVideo`.

**Role in the chain.** Prometheus is both a Wi-Fi AP and a downstream router, and a wired client of ouranos. The physical chain [O, and R for Zeus]:

```
ISP router 192.168.1.1
  └─ ouranos enp0s31f6 (integrated, 192.168.1.5, default route)
     ouranos enp0s20f0u1c2 (USB ASIX, cdc_ncm, 10.44.0.1/24, NM "prometheus-share-temporary", ipv4.method=shared, dnsmasq)
       └─ Prometheus eno1 (integrated RTL8125, 10.44.0.148 via DHCP, default via 10.44.0.1)
          Prometheus br-lan 10.18.0.1/24 (Kea DHCP, dnsmasq DNS, NAT out eno1)
            ├─ wlp195s0: AP "goldragon.criome", WPA3-SAE, ch 6   <- the living's phone / ouranos Wi-Fi join here
            └─ enp199s0f0u1 (USB AX88179): downlink to Zeus (10.18.0.103, R: 38de5b 09-25)
```

The ouranos to Prometheus hop is an imperative NetworkManager share, not a declared feature. CriomOS has a `usb-ipv4-gateway.nix` module keyed on a `usbIpv4Gateway` capability, but Horizon's `NodeCapability` enum has no such variant, so the hop cannot be declared in cluster data today [O].

## 2. The living's words

Verbatim, from `flows/*/vision` and `flows/*/notion` files. `Vision/` and `Intent/` hold nothing on this, and `vision-raw/` is empty. In the living's speech-to-text, "colddragon.criome" means `goldragon.criome` and "Uranus" means Ouranos.

1. 2026-09-21, `flows/753e69/vision/prometheusWifiReliability.md`: "Remember, see if anybody's doing anything about the Wi-Fi access point on Prometheus. Go drag and Creo my Wi-Fi access point on the Creo OS side in the cluster and my phone can't connect to it. I don't know. I guess it doesn't seem to have internet access."
2. Same file: "Whatever the problem was, we need to put a fix in that would not let that happen again because there seems to be a reliability issue there with maybe the wireless network getting public internet access (depending on when it was started, if it was started after the DHCP server got the address or I don't know what). We need to make this more reliable."
3. Same file: "I tried again to connect to colddragon.criome, my Wi-Fi access point on my phone, and failed. It went to get an IP address and maybe even got one, and then it just disconnected. … I can't get internet from my Wi-Fi access point, even though Prometheus should have internet, right? It's giving it to Zeus, so I'm assuming it has internet."
4. 2026-09-22, `flows/753e69/vision/transitiveNetworkTopologyAndCertificateWifi.md`: "Prometheus has a USB Ethernet that goes to Zeus, which should be getting internet from him through the network cable that Zeus's built-in port has. Let's make that the transitive topology, so it's a testing skill. … The built-in port is for upstream, and the USB is for downstream. We just reuse that pattern, and no matter how we plug things in, that's how I would want it to work, right? Kind of statelessly."
5. Same file: "There are some nodes, like Uranus, when it gets its internet from the Ethernet and it's put into stable mode. … it becomes a Wi-Fi access point itself. That would be a feature, like an opportunistic Wi-Fi access point or something like that, or a mode: optional Wi-Fi access point, right?"
6. Same file: "I guess we can use the same password for now, but eventually, for the certificate-based Wi-Fi client authentication, with the clients on my Android phones and/or on the other laptops, they all have their own certificates."
7. 2026-09-23, `flows/836818/vision/network.md` (STT): "It doesn't make sense that Prometheus isn't reachable if I'm getting internet from its Wi-Fi because it's getting internet from Uranus [Ouranos]."
8. Same file: "It never really worked well from making Uranus [Ouranos] the upstream supplier to Prometheus. Do you need to create a network hierarchy kind of thing or with features? I don't know."
9. 2026-09-24, `flows/752e0f/vision/wifi.md` (typed), about the Ouranos AP: "Yeah, I think turning it on and off automatically when we get detected, not just when you detect a cable, but when the cable is giving us internet access and logging with certificates. Yes, certificates are what I want"
10. 2026-09-24, `flows/e51411/vision/network.md` (artifact comment): "Well the concept of router is just a feature now so it's not a router per se. It has that feature. … Can we just make a really really simple fix that doesn't try to reimagine everything and introduce a bunch of other variables"
11. 2026-09-25, `flows/752e0f/vision/internetPropagation.md`: "This is a feature, right? Prometheus would ostensibly have the same feature so that USB Ethernet devices become downlinks, so it would propagate any internet access it has through that."
12. 2026-09-25, `flows/da88cf/vision/prometheus.md` (STT): "So I started it. Now that should help. It wasn't even running. I guess we had a power outage or something."

Two records are agent distillation, not the living's words: `flows/b80e55/vision/unifiedWifiRoamingAndCertAuth.md`, where "Immediate Ouranos AP canceled" appears, and d8df70's "Wi-Fi A". No living quote says to keep ouranos off Prometheus's AP.

## 3. Existing code

**On `main@origin`** (CriomOS `f09f3c8`; local `main` is one commit ahead at `19d5736`, a home pin):

- `modules/nixos/router/default.nix` (router feature):
  - hostapd primary AP, WPA3-SAE, `saePasswordsFile` from sops secret `routerWifiSaePasswords`.
  - Backup AP `hostapd-backup-wireless`, WPA2-PSK-SHA256, started by udev when the declared USB radio appears.
  - `br-lan` 10.18.0.1/24, Kea DHCPv4 pool .100–.240, nftables input, forward and masquerade out the WAN.
  - WAN DHCP via networkd; `router-wan-lease-recovery` timer (commit `114fcbd`, 09-21).
  - Declared TCP ports composed into nftables (`bd6a16d`, 09-24).
  - `kernel.panic=10`, `panic_on_oops=1`, `RuntimeWatchdogSec=30s` (`eebeab5`, 09-24).
  - USB ethernet bridged as LAN by driver list.
- `modules/nixos/router/wifi-pki.nix`: EAP-TLS server-key directory stub. EAP is not wired into hostapd; the comment says "uncomment when EAP-TLS is deployed".
- `modules/nixos/network/wifi-eap.nix`: EAP-TLS client profile `criome`, gated by `WifiCertificate`, used by no node.
- `modules/nixos/network/usb-ipv4-gateway.nix`: the USB share, keyed on a capability Horizon cannot express.
- Also `networkd.nix`, `dnsmasq.nix`, `headscale.nix`, `tailscale.nix`, `nordvpn.nix`, `yggdrasil.nix`, `router/yggdrasil.nix`.
- Checks: `router-wifi-horizon-policy`, `router-wifi-secret`, `router-wan-recovery`, `router-declared-tcp-ports`, `router-non-router-lazy`, `router-yggdrasil-ndp`, `usb-ipv4-gateway`.

**On branches, not in main:**

- `prometheus-usb-downlink-5f38bc` (`de5ac1b`) and `prometheus-usb-bus-property-5f38bc` (`da85c4a`, with unbookmarked `e92a336` and the "Match non-router USB Ethernet" commit). These bind USB LAN by `ID_BUS=usb`, excluding the WAN. They do not touch hostapd.
- `field-usb-ygg-ndp-9ddcbc` and `field-wifi-wan-recovery-753e69`: already merged.

"Optional AP" and "stable Ethernet mode" exist nowhere in code. A `git grep` across branch heads for `optional.?ap`, `stableEthernet` and `opportunistic` returned nothing.

**Deployed on Prometheus** [O]:

- Generation `system-55`, kernel 7.1.8, `kernel.panic = 10`.
- hostapd, Kea, dnsmasq and networkd are active. `hostapd-backup-wireless` is **inactive**.
- 09-24 witness (38de5b [R]): 55 is the only generation, "Configuration Revision Unknown", built 09-24 21:03, two minutes after the branch commit `da85c4a`. [I] It was probably built from the 5f38bc branch, not from main.
- Lojix's Prometheus record ends with failures [O, `lojix Query.ByNode`]:
  - Deployment 30 (`eebeab5`): Evaluate failed on an assertion; the text is truncated in the reply.
  - Deployment 31 (`f9343c6`): TestActivation failed with NAR download timeouts from `nix.prometheus.goldragon.criome`.
  - [R] Generation 55 was activated by Terra (5f38bc) outside a completed Lojix deployment record.

**Local hotfixes on ouranos (imperative)** [O]:

- NM `prometheus-share-temporary`: saved, MAC-pinned, shared, autoconnect priority 200.
- NM `goldragon.criome`: `autoconnect=no`, with `never-default`/`ignore-auto-dns` set by 6db4fe on 09-22 [R].
- NM `Mega_2.4G_1896`: `autoconnect=no`.
- Firewall drop-in hook `90-field-prometheus-usb.conf` [R].

**`testing-transitive-network-topology` skill**: its invariants cover this chain directly:

- integrated NIC is the uplink, USB NIC the downlink;
- one DHCP/DNS owner per downstream subnet;
- one egress NAT owner, preferably at Ouranos;
- "Optional AP stays absent unless explicitly enabled", and disabling it removes AP listeners without breaking wired transit;
- EAP-TLS acceptance needs per-device certificates ("a shared password is migration state").
- Result grades: source-published, installed-running, end-to-end-proven.

## 4. Live state, 2026-09-25 ~21:00–21:20 local

**Ouranos** [O]:

- `enp0s31f6` 192.168.1.5/24 (default via 192.168.1.1).
- `enp0s20f0u1c2` 10.44.0.1/24.
- `wlp0s20f3` managed, DOWN, disconnected.
- `yggTun` 201:6de1:…; `tailscale0` present.
- `networkctl`: all links unmanaged (NetworkManager owns them).
- `nmcli`: USB is `prometheus-share-temporary` and wired is `Wired connection 1`; Wi-Fi is disconnected.

**Tailscale** [O]: `tailscale status` gives `NoState`, logged out: `fetch control key: Get "https://127.0.0.1:8443/key?v=142": x509: certificate signed by unknown authority`. tailscaled has been active since 09-10. Headscale on ouranos logs `TLS handshake error … remote error: tls: bad certificate` every ~30 s, 8,651 x509 lines in 3 days. Headscale runs on ouranos (`TailnetController`). This is a separate defect and does not affect the Wi-Fi path.

**The outage** [O]:

- Ouranos dnsmasq ACKed `10.44.0.148 84:47:09:75:88:68 prometheus` every ~27 min through 12:32:29.
- From 12:57 to 13:06, both ouranos NICs flapped repeatedly, including the integrated uplink to the ISP router.
- The Prometheus journal for boot −1 ends at 12:55:13, and no pstore entry is newer than 09-24.
- [I] A power outage, matching the living's "I guess we had a power outage", and not an mt7925 panic.
- Until Prometheus returned, the USB link showed carrier at 100 Mb/s with zero RX packets. [I] That is consistent with a powered-off NIC's standby PHY.
- Prometheus booted at 21:15:44. At 21:15:56 dnsmasq sent DISCOVER/OFFER/ACK for 10.44.0.148.

**Reachability now** [O]:

- `ping prometheus.goldragon.criome`: 2/2, 3.3 ms.
- Neighbours 10.44.0.148 and fe80::8647:… are `REACHABLE`.
- `ssh prometheus.goldragon.criome` works. Earlier in the evening it timed out, as did nix-daemon builder ssh from 13:50 to 20:29.
- `ssh prometheus`, the bare alias, does not resolve a host of its own; it maps to the FQDN.

**Prometheus now** [O]:

- Uptime 3 min; `eno1` 10.44.0.148; default via 10.44.0.1.
- `br-lan` 10.18.0.1/24 with members `enp199s0f0u1` and `wlp195s0`.
- `wlp195s0` AP `goldragon.criome` ch 6, **txpower 3.00 dBm**.
- Regulatory domain `country PL: DFS-ETSI`, from the hard-coded `"PL"` default. The living is in Mexico: ouranos has a San Cristóbal location and its own regdom reads MX.
- The USB radio `0e8d:0717` (MediaTek "Wireless_Device") enumerated at usb 3-5, but **no netdev is bound**. `wlp199s0f0u4` does not exist, so the backup AP cannot start. [U] Whether the kernel lacks a driver for this ID or the dongle sits in a mode-switch state.
- Zero AP-STA-CONNECTED events this boot at 21:19.

## 5. Hypotheses for "get my Wi-Fi access back from Prometheus"

**H1, leading: the living's own devices should use Prometheus's AP `goldragon.criome` again, and the laptop's access should come back.**

For:
- He calls it "my Wi-Fi access point" (09-21) and was "getting internet from its Wi-Fi" (09-23).
- On 09-24 an agent turned ouranos's profile off ("Wi-Fi A") under a general "deploy everything" relay, not a word from the living about Wi-Fi. "Back" fits something taken away.
- The AP was also absent all afternoon because Prometheus was powered off.

Against:
- Ouranos has wired Internet, so the laptop does not need Wi-Fi for Internet. The phone could use the house router.
- The panic trigger (ouranos Wi-Fi churn) may return. `kernel.panic=10` now bounds the damage to about a minute of reboot, and kernel 7.1.8 is running; whether the mt7925 bug is fixed is unknown.

**H2: Wi-Fi as the management path from ouranos to Prometheus.**

Until 09-24, Yggdrasil to Prometheus ran over this Wi-Fi (6db4fe, 752e0f [R]), so "Why was it working before?" might refer to it.

For: tonight's frustration is about reaching Prometheus.

Against: the cable path now works (ping, ssh, remote builds per 88475f [R]), so Wi-Fi is not needed for reach.

**H3: the Optional AP feature.**

A declared feature that makes a node an AP when it has real wired Internet, with certificates (quotes 5, 6, 9). "Feature-based enabling … which I haven't seen … don't understand how to set it up" matches the living not knowing that `Router` plus `RouterInterfaces` is the feature. It also matches Optional AP being a concept with no code.

Against: he says "from Prometheus", and Prometheus already has the always-on router feature.

**One observation to decide.** Ask the living which device he means: the phone, the laptop, or both. Alternatively, while the AP is up now, watch Prometheus's hostapd and Kea journal while the living tries the phone on `goldragon.criome`.
- The phone connects and gets Internet: the remaining ask is the laptop (H1 laptop) or the feature's visibility (H3).
- It fails at authentication or association: the cause is the radio (3 dBm, PL regdom) or the password.

## 6. For H1: what a declared feature needs

**Already declared and deployed** (Prometheus side): the `Router` capability, `RouterInterfaces`, the router module, and the secret `goldragon/secrets/routerWifiSaePasswords.sops`. That file is age-encrypted sops; its value was not read. It reaches CriomOS as `inputs.secrets.sopsFiles.routerWifiSaePasswords` through Lojix's private secrets input (the CompleteHost secret binding). For the phone, nothing needs deploying. The living joins `goldragon.criome` (WPA3) with the password he set. [U] Whether he has the password at hand.

**Missing:**

1. **Client feature** (ouranos, and later other laptops). One option is a Horizon capability, for example a cluster-Wi-Fi client carrying a router node reference.
   - Needed: a horizon-rs ethos variant, a projection, and a version bump.
   - A CriomOS module declaring the NetworkManager profile: SSID from the router's projection, SAE, lower priority than wired, `never-default` while wired is up.
   - The goldragon enablement on ouranos.
   - The client needs the SAE password. The secret's sops recipients must include ouranos's key. [U] Current recipients were not inspected.
   - This replaces the imperative profile. It also reverses Wi-Fi A, which needs the living's word because Wi-Fi A was a panic mitigation.
   - The existing `WifiCertificate`/EAP-TLS path is the certificate end state the living asked for. It needs a CA, per-device certificates, and hostapd EAP, none of which is deployed.
2. **Radio correctness.** Add a country field to `RouterInterfaces`, or a cluster location, so hostapd stops using PL. Investigate the 3 dBm transmit power.
3. **Backup AP.** The USB radio at usb 3-5 has no driver bound, and the declared name `wlp199s0f0u4` is absent.
4. **Declare the ouranos to Prometheus hop.** Needs a `UsbIpv4Gateway` Horizon variant; this is the transitive-topology work.

**Deployment path.** `lojix-meta 'Deploy.Host.{ goldragon <node> CompleteHost <proposal> <secrets> <flake> … }'`:
- Proposal: `$(nix path-info goldragon#horizon-definition)/horizon-definition.datom`.
- Builder: Prometheus, now reachable.
- For ouranos (client) and Prometheus (radio fixes).

**Blockers:**
- (a) The living's word on H1 versus H3, and on reversing Wi-Fi A.
- (b) The phone: the living enters the password; agents never read it.
- (c) The last Lojix Prometheus deployments failed. Generation 55 runs a branch build with an unknown revision. Main does not yet carry the USB-downlink branch. Any Prometheus redeploy from main would drop the branch's USB bridge binding unless it is merged first.
- (d) The client feature needs a producer change (horizon-rs) before the consumer changes (CriomOS, goldragon).
- (e) Prometheus's uptime is minutes. Whether the AP stays up and panic-free is unproven.

The fastest reversible step, if the living wants the laptop back on the AP tonight, is imperative and not the declared feature: `nmcli connection modify goldragon.criome connection.autoconnect yes` then `nmcli connection up goldragon.criome`. The profile keeps `never-default` and `ignore-auto-dns`, so wired Internet stays primary.

## Sources

- `/git/github.com/LiGoldragon/goldragon/cluster-definition.datom`, `README.md`, `secrets/` (listing only).
- `/git/github.com/LiGoldragon/horizon-rs/lib/ethos/horizon.ethos`, `lib/src/model.rs`, `lib/src/projection/views.rs`.
- CriomOS `main@origin` `f09f3c8`: `modules/nixos/router/{default,wifi-pki}.nix`, `modules/nixos/network/{wifi-eap,usb-ipv4-gateway}.nix`. `jj log` over `files("modules/nixos/router")` and the 5f38bc branch diff.
- `/home/li/primary/.claude/skills/testing-transitive-network-topology/SKILL.md`.
- Ouranos: `ip -br link/addr`, `ip route`, `ip neigh`, `networkctl list`, `iw dev`, `nmcli device`, `nmcli connection show`, `nmcli dev wifi list`, `tailscale status`, `systemctl status tailscaled`, `journalctl` (dnsmasq-dhcp, e1000e, wpa_supplicant, headscale, nix-daemon), `/sys/class/net/enp0s20f0u1c2/{carrier,speed,statistics}`, `lojix 'Query.ByNode.{ goldragon prometheus None }'`.
- Prometheus (read-only ssh, 21:19): `uptime`, `readlink` system profile, `uname -r`, `sysctl kernel.panic*`, `systemctl is-active`, `ip -br addr/link`, `ip route`, `iw dev`, `iw reg get`, `journalctl --list-boots`, `journalctl -b -1 -n 3`, `journalctl -k -b` (usb/mt79), `journalctl -u hostapd -b`, `/var/lib/systemd/pstore` listing, `lsusb`.
- Reports: `flows/6db4fe/reports/prometheus-wifi-brief-2026-09-21.md`, `flows/d8df70/reports/prometheus-recurring-outage.md`, `flows/38de5b/receipts/live-witness-20260925.md`, `flows/752e0f/reports/zeus-link-and-mesh-2026-09-25.md`, `flows/6db4fe/reports/{prometheus-builder-recovery-2026-09-22,network-chain-attempts,prometheus-connectivity}.md`, `flows/836818/reports/prometheus-observations-2026-09-23.md`, `flows/38de5b/log.md`, `flows/da88cf/{log.md,vision/prometheus.md}`.
- Transcript: `/home/li/.claude/projects/-home-li-primary/d8df703d-d083-4c29-9597-6b32e7411b75.jsonl` (2026-09-24T20:50:10Z e51411 relay; 20:50:32Z the `nmcli` Wi-Fi A command; 21:01Z "imperative-only").
- Vision records listed in section 2.
