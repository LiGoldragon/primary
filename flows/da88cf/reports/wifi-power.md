# Prometheus Wi-Fi: the 3 dBm reading, the country, the backup radio

Subflow of da88cf, read-only. Observed 2026-09-25 21:23–21:40 CST from ouranos and over `ssh -o BatchMode=yes prometheus.goldragon.criome`. Prometheus had been up for about 8 minutes (boot 21:15:44). Nothing was changed on any host or repository. The only file written is this one.

Grades: **[O]** observed in this run; **[S]** read from upstream kernel or regdb source fetched in this run; **[I]** inference; **[U]** unknown.

## 1. Why `iw` shows 3 dBm

**Short answer.** The 3.00 dBm is a driver reporting artifact of `mt7925e` on kernel 7.1.x. It is not the transmit power. The PL regulatory domain does not cause it, and changing to MX would not change it.

**Observations [O]:**

- `iw dev wlp195s0 info`: `type AP`, `ssid goldragon.criome`, `channel 6 (2437 MHz), width: 20 MHz`, `txpower 3.00 dBm`.
- `lspci -k`: `c3:00.0 MEDIATEK Corp. MT7925 (RZ717) Wi-Fi 7`, driver `mt7925e`. The kernel is 7.1.8.
- `iw reg get`: `global country PL: DFS-ETSI`, which allows `(2400 - 2483 @ 40), (N/A, 20)`. There is no per-phy self-managed domain on Prometheus.
- `iw phy phy0 channels`: channels 1 to 13 all show `Maximum TX power: 20.0 dBm`. The phy has `Available/Configured Antennas: TX 0x3 RX 0x3`, i.e. two chains, and `supports per-vif TX power setting`.
- hostapd config, from the Nix store files that the `make-hostapd-wlp195s0-files` pre-start script names; the runtime file in `/run/hostapd` is root-only:
  - `country_code=PL`, `ieee80211d=1`, `ieee80211h=1`, `hw_mode=g`, `channel=6`.
  - No `tx_power` or equivalent setting.
  - Also present, and incidental: `ieee80211ac=1` on a 2.4 GHz radio.
- Kernel log since boot: firmware loaded (`WM Firmware Version ... Build Time: 20260605184805`). There are no regulatory or power warnings.

**Source reading [S]:**

- In stable v7.1.8, `drivers/net/wireless/mediatek/mt76/mt7925/main.c` has `.get_txpower = mt76_get_txpower` (fetched from `gregkh/linux` tag v7.1.8, line 2445).
- `mt76_get_txpower` computes `*dbm = DIV_ROUND_UP(phy->txpower_cur + delta, 2)`, where `delta = mt76_tx_power_path_delta(n_chains)`. For two chains that delta is 6.
- At v7.1, none of `mt7925/{main,mcu,init}.c`, `mt792x_core.c` or `mt76_connac_mcu.c` ever assigns `txpower_cur`. Transmit power is programmed into firmware as per-rate limit tables (`mt7925_mcu_set_rate_txpower`).
- So the reported value is `ceil((0 + 6) / 2) = 3` for any regdom and any real power.
- Upstream fixed the reporting in v7.2 with the commit "wifi: mt76: mt792x: report txpower for the requested vif link". That commit adds `mt792x_get_txpower`, which returns the rate power limit for the vif's channel.

**Conclusion.** The 3 dBm is a misread. [I, strong: source-derived and consistent with every observation.]

- The effective limit under PL on channel 6 is 20 dBm EIRP (`iw phy`). The firmware programs that limit through the rate-power tables.
- wireless-regdb (`db.txt`, fetched) gives `country MX: DFS-FCC (2402 - 2482 @ 40), (20)` and `country PL: (2400 - 2483.5 @ 40), (100 mW)`. **At 2.4 GHz both are 20 dBm.** Moving PL to MX changes nothing on channel 6. It changes 5 GHz and 6 GHz rules, DFS-ETSI versus DFS-FCC, and legality.

**Stations [O]:**

- `iw dev wlp195s0 station dump` is empty. No clients have associated since boot.
- Ouranos's cached scan: `goldragon.criome DC:56:7B:FB:76:1F ch 6 signal 49 WPA3`.
- Historical clients show the AP served real traffic at this "3 dBm". Since 09-21, AP-STA-CONNECTED lines by OUI prefix only, not resolved:
  - `dc:90:09`: 353
  - `14:85:7f`: 32
  - `5a:47:10`: 11 (locally administered, i.e. a randomized MAC)
  - `56:83:a6`: 3 (locally administered)
- The last connect was 09-25 12:37, before the power loss.

[U] The real radiated power. That needs an RSSI-at-known-distance comparison, or v7.2's reporting. [U] Whether the MT7925's own firmware SAR or back-off lowers it. The `mt7925e` module parameters and ACPI SAR tables were not read.

## 2. Where the living is

**Evidenced:**

- [O] Both hosts' `timedatectl` gives `America/Mexico_City (CST, -0600)`, and `/etc/localtime` points to `America/Mexico_City`.
  - CriomOS enables `services.localtimed` (geoclue) on metal nodes (`modules/nixos/metal/default.nix`). It sets no fixed `time.timeZone`.
  - So the zone was detected, not declared. [U] Which geoclue source Prometheus used: it has no FixedLocation, so geoclue falls back to 0/0. It may be network-based; not checked.
- [O] Cluster data (`goldragon/cluster-definition.datom` at `8c4d03d`): **ouranos carries `FixedLocation` `Some.{ 16.736944 -92.6375 2121.0 1000.0 }`**. [I] Those are latitude and longitude near San Cristóbal de las Casas, Chiapas, Mexico. Prometheus has no FixedLocation.
- [O] Ouranos's own radio (iwlwifi) reports `phy#0 (self-managed) country MX`, while its global domain is `00`. The firmware decided that, presumably from 802.11d or its location logic.
- [O] Psyche, typed, `flows/05c604/vision/cluster.md`: "...get Zeus updated so that it has all the latest fixes we've done since moving to Mexico." The grep of `Vision/`, `vision-raw/` and `flows/*/vision/` for mexico, San Cristóbal and Chiapas finds only this record and one mention in `flows/6cc91b/vision/notifications.md` of a server "closer to Mexico".

**Assumed:** that Prometheus is physically with ouranos in Mexico. [I] This is likely, because it is wired to ouranos by a USB-Ethernet cable (the prior report, §1). No WAN geolocation was looked up.

## 3. The declared country fix

**What exists [O]:**

- CriomOS `origin/main` (`d193baf`), `modules/nixos/router/default.nix:37`:
  `wirelessCountryCode = routerInterfaces.country or routerInterfaces.wirelessCountryCode or "PL";`
  - It is used at line 216 (`services.hostapd.radios.<wlan>.countryCode`) and at lines 351–352 (the backup AP's `country_code=`/`ieee80211d=1`).
  - **The consumer already reads an optional `country`.** Only the producer and the data lack it.
  - The NixOS hostapd module already writes `country_code` plus `ieee80211d=1` from `countryCode` (observed in the generated config). Nothing else in CriomOS sets a regdom: `git grep regulatory|cfg80211|ieee80211_regdom` is empty, and `/etc/modprobe.d` has no `ieee80211_regdom`.
- horizon-rs:
  - No country field anywhere. `git grep -i country` finds only `skills.md:116`, whose bucket table already names "regulatory country" as a **Cluster fact** (proposal surface).
  - The goldragon flake pins horizon-rs `ee8d6f8`, which is the ethos line: `lib/ethos/horizon.ethos:66` has `RouterInterfaces.{ Interface Interface WlanBand Integer WlanStandard Option<SecretReference> Option<BackupWireless> }`, and it is projected in `lib/src/projection/views.rs` into `RouterInterfacesView` (`lib/src/model.rs:167`).
  - `origin/main` (`b45d6ad`, 4 commits ahead) has "Restore[d] Datomic ClusterProposal primary API". There `RouterInterfaces` is a hand-written struct in `lib/src/proposal.rs:594`, with `impl Datomic` at line 909 and a 7-part arity.
  - [I] Side hazard: on `origin/main`, the node view carries the proposal struct directly under serde camelCase (`wpa3SaePassword`, `backupWireless.password`). CriomOS reads `wpa3SaePasswordReference` and `passwordReference`. A goldragon repin to `origin/main` would hit the router module's `throw`. This was not built; flag it to whoever repins.
- goldragon data, Prometheus record: `Some.{ eno1 wlp195s0 TwoG 6 Wifi4 Some.{ routerWifiSaePasswords } Some.{ wlp199s0f0u4 criome-backup TwoG 11 Wifi4 { routerBackupWifiPassword } } }`. The record is positional.

**Minimal producer-first sketch (not applied).** It is written against the pinned ethos line `ee8d6f8`. The `origin/main` variant is noted where it differs.

(a) horizon-rs, the producer:

```diff
--- lib/ethos/horizon.ethos
+  CountryCode.String
   ...
-  RouterInterfaces.{ Interface Interface WlanBand Integer WlanStandard Option<SecretReference> Option<BackupWireless> }
+  RouterInterfaces.{ Interface Interface WlanBand Integer WlanStandard Option<SecretReference> Option<BackupWireless> Option<CountryCode> }
--- lib/src/model.rs   (RouterInterfacesView)
     pub backup_wireless: Option<BackupWirelessView>,
+    pub country: Option<String>,
--- lib/src/projection/views.rs   (impl Projection for RouterInterfaces)
             backup_wireless: ...,
+            country: self.country_code_option.clone(),   // generated field name per ethos codegen
```

- Regenerate `lib/src/generated/horizon.rs`, add a test (the existing `lib/tests/horizon.rs:475` fixture), and apply a **version bump**: positional arity changes, so all existing data breaks.
- The `origin/main` variant: add `#[serde(default)] pub country: Option<CountryCode>` to `struct RouterInterfaces`, and add an 8th element to the `embody` and `portion` arity in `impl Datomic for RouterInterfaces`.
- Validate the value as an ISO-3166 alpha-2 uppercase code (a newtype with a check, as `WirelessNetworkName` has), or leave validation to hostapd. That is a design choice.
- The alternative placement, open and with no verdict: a cluster-level or node-level country beside `FixedLocation`, derived into the router view. The bucket table places "regulatory country" on the proposal surface either way.

(b) goldragon, the data (after repinning horizon-rs):

```diff
--- cluster-definition.datom   (Prometheus NodeNetwork)
-Some.{ eno1 wlp195s0 TwoG 6 Wifi4 Some.{ routerWifiSaePasswords } Some.{ wlp199s0f0u4 criome-backup TwoG 11 Wifi4 { routerBackupWifiPassword } } }
+Some.{ eno1 wlp195s0 TwoG 6 Wifi4 Some.{ routerWifiSaePasswords } Some.{ wlp199s0f0u4 criome-backup TwoG 11 Wifi4 { routerBackupWifiPassword } } Some.MX }
```

The exact atom spelling of `Option<CountryCode>` follows the datom codec: `Some.MX` or `Some.«MX»`.

(c) CriomOS, the consumer. It needs almost nothing:

```diff
--- modules/nixos/router/default.nix
-  wirelessCountryCode = routerInterfaces.country or routerInterfaces.wirelessCountryCode or "PL";
+  wirelessCountryCode =
+    routerInterfaces.country
+      or (throw "router: horizon.node.network.routerInterfaces.country is required (regulatory domain)");
+  # optional: also pin the kernel's global regdom so it does not depend on hostapd having started
+  boot.extraModprobeConfig = "options cfg80211 ieee80211_regdom=${wirelessCountryCode}";   # inside config = mkIf ...
```

- The fork within (c), with no verdict:
  - keep a fallback, now `"00"` world rather than `"PL"`, if a missing country should not fail evaluation; or
  - `throw`, so a router cannot deploy without declaring its regdom.
- hostapd's `country_code` plus `ieee80211d=1` is already generated from `countryCode`, so no hostapd change is needed.
- A `router-wifi-horizon-policy` check update: assert that `country_code` equals the declared value.

**Transmit-power fork (presented, no verdict):**

- **Left to the regdom** (current behaviour): the firmware uses the regdom or rate limit (20 dBm at 2.4 GHz for both PL and MX). There is nothing to declare. With a v7.1 kernel, `iw` keeps showing 3 dBm regardless, so a check cannot read the power back.
- **Declared**: an optional `Option<Integer>` transmit power on `RouterInterfaces`, which CriomOS applies with `iw dev <wlan> set txpower fixed <mBm>` after hostapd starts. It would allow deliberately lowering power, and so less interference. Raising power above the regdom is impossible anyway. Verification stays blind until the kernel carries the v7.2 `mt792x_get_txpower` fix.

## 4. The backup USB radio

The earlier reading was wrong in its premise. **The `0e8d:0717` device is not the backup radio.** [O]

- `usb 3-5`, `0e8d:0717 MediaTek Inc. Wireless_Device`, has `removable = fixed`. Its three interfaces are all class `e0/01/01` (Bluetooth). Interfaces 0 and 1 are bound to `btusb` (`hci0`). Its HW/SW build time `20260605184935` matches the MT7925 Wi-Fi firmware's build of `20260605`.
- [I, strong] It is the MT7925 combo card's own Bluetooth function on an internal USB port. Interface 2 unbound is normal for a btusb ISO or alternate interface.
- The declared backup radio `wlp199s0f0u4` (PCI `c7:00.0`, USB port 4) was an **ASUS `0b05:17ba` "802.11n WLAN Adapter", driver `rtl8192cu`**, at `usb 3-4`.
  - The journal holds it on boots from 06-08 to 06-26, with `rtl8192cu 3-4:1.0 wlp199s0f0u4: renamed from wlan0` and hostapd bringing it up.
  - `usb 3-4: USB disconnect` came on **2026-06-26 12:24**.
  - Since 09-21, `usb 3-4` has been a **SanDisk Cruzer Blade `0781:5567`** (a USB stick), on every boot including this one.
  - The name `wlp199s0f0u4` never appears after June.
- Driver and firmware are present in the running generation: `modinfo -n rtl8192cu` resolves in `/run/booted-system/kernel-modules/...` and `/run/current-system/firmware/rtlwifi/rtl8192cufw*.bin.zst` exist.
- The CriomOS declaration exists: `backupWireless` produces `hostapd-backup-wireless`, bound by udev and systemd to `sys-subsystem-net-devices-wlp199s0f0u4.device`. It is inactive because the device is absent. That is correct behaviour.

**The declared fix** is physical, not code: plug the ASUS dongle back into the same port, replacing the stick, and the declared service starts.

- If the port must stay with the stick, the fix is data only: change `BackupWireless.interface` in goldragon to the new predictable name.
- [I] Naming by port path is fragile, because moving the dongle changes the name. A MAC-matched `.link` rename is a possible CriomOS improvement, not needed now.

## 5. Failed associations as seen by hostapd

- **Since this boot [O]:** `journalctl -u hostapd -b` has 5 lines: start, `COUNTRY_UPDATE`, `ENABLED`, `AP-ENABLED`. There are **zero** authentication, association, SAE, mismatch or failure events. No device has tried to join in the ~8 minutes up.
- **Logging reach [O]:** `logger_syslog_level=2` and `logger_stdout_level=2` (informational). Association, disassociation and "did not acknowledge" events are logged. SAE commit and confirm failures and PSK mismatches are debug-level in hostapd, so a wrong password would likely **not** appear. [I] Absence of SAE errors is weak evidence.
- **Since 09-21, for context [O]:**
  - Raw journal line counts. They are possibly doubled, since both stdout and syslog loggers are on.
  - The grep for `sae|mismatch|fail|reject|denied` returns **nothing**.
  - Radio-level trouble:
    - `did not acknowledge authentication response`: 4 lines on 09-21 (`5a:47:10`), 4 on 09-22 (`dc:90:09`).
    - `disassociated/deauthenticated due to inactivity`: `5a:47:10` 26 lines on 09-21, 4 on 09-22, 12 on 09-24; `56:83:a6` 4 lines each on 09-21 and 09-23.
  - [I] The 09-21 cluster for a randomized-MAC client coincides with the living's 09-21 report ("went to get an IP address ... and then it just disconnected"). Inactivity drops point to a link or upstream problem, not authentication. The client was not resolved to a device or person.
- [U] Whether `dc:90:09` is ouranos. Ouranos's current Wi-Fi MAC is `c6:af:14:…`, randomized, so it does not match.

## Unknowns

- True radiated power of `wlp195s0`; MT7925 SAR or ACPI back-off.
- Prometheus's physical location beyond "wired to ouranos"; the source of its detected time zone.
- Whether SAE failures occurred at debug level; any attempt since this boot would need a live watch while the living tries.
- Datom atom spelling for `Option<CountryCode>`; whether the producer change lands on the `ee8d6f8` ethos line or on `origin/main`'s Datomic line. They have diverged, and `origin/main`'s view field names do not match CriomOS.
- Whether the ASUS dongle still exists and where it is.

## Sources

- Prometheus, live: `iw dev`, `iw reg get`, `iw phy phy0 channels/info`, `lspci -k`, `lsusb`, `/sys/bus/usb/devices/3-5*` (ids, removable, interface classes, drivers), `journalctl -k -b`, `journalctl _TRANSPORT=kernel` (all 34 boots), `journalctl -u hostapd` (this boot and since 09-21), `systemctl cat hostapd`, Nix-store hostapd config files, `modinfo -n rtl8192cu`, `/run/current-system/firmware`, `timedatectl`, `/etc/localtime`.
- Ouranos, live: `timedatectl`, `iw reg get`, `nmcli dev wifi list --rescan no`, `/sys/class/net/wlp0s20f3/address`.
- `/git/github.com/LiGoldragon/CriomOS` `origin/main` `d193baf`: `modules/nixos/router/default.nix` lines 37, 216, 330–370; `modules/nixos/metal/default.nix` lines 20–35, 676.
- `/git/github.com/LiGoldragon/horizon-rs` `ee8d6f8` (goldragon pin): `lib/ethos/horizon.ethos:51,57,66`, `lib/src/model.rs:167`, `lib/src/projection/views.rs:70`; `origin/main` `b45d6ad`: `lib/src/proposal.rs:594,909`, `skills.md:116`.
- `/git/github.com/LiGoldragon/goldragon` `8c4d03d`: `cluster-definition.datom`, `flake.lock` (horizon rev `ee8d6f8`).
- Linux source, fetched: torvalds `master` and `v7.1` and `v7.2`, and gregkh `v7.1.8`, `drivers/net/wireless/mediatek/mt76/{mac80211.c,mt76.h,mt792x_core.c,mt7925/main.c,mt7925/mcu.c}`; GitHub commit log for `mt792x_core.c`.
- wireless-regdb `db.txt` (git.kernel.org, wens/wireless-regdb), entries MX and PL.
- Psyche: `flows/05c604/vision/cluster.md` line 16; `flows/6cc91b/vision/notifications.md`.
- Prior report: `flows/da88cf/reports/wifi-prometheus.md` §§1–4.
