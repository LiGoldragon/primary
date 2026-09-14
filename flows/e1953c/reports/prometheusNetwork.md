# Prometheus network — router module, dongle policy, center sharing, backup radio, staleness
Flow e1953c subflow, read-only. `file:line` is relative to `/git/github.com/LiGoldragon/` — `CriomOS` at `main`
36653a1, `goldragon` 2a13945, `horizon-rs` 8c11dfa, `CriomOS-lib`, `CriomOS-test-cluster`; host facts by ssh.

## The living's words (they rule §2 and §3)
> The LAN is connected to Prometheus through a USB LAN adapter that we need to support to give internet access by
> default. Somehow, we have a service that makes sure that it's distributing internet from whatever it's getting on
> its LAN port, or maybe even its Wi-Fi. […] We're going to set up that USB trick everywhere. […] We need something
> that doesn't break the networks after booting, so we can hotplug the USB.
> -- psyche, STT, 2026-09-14, `/home/li/secondary/flows/57a7aa/vision/network.md`

> Anybody can be a gateway that has enough features. Most laptops can be a gateway when they receive internet from the
> main LAN.
> -- psyche, STT, `/home/li/primary/flows/6cc91b/vision/network.md`

## 1. Country, transmit power, and the 3 dBm
Witnessed. Country: `modules/nixos/router/default.nix:37` — `wirelessCountryCode = routerInterfaces.country or
routerInterfaces.wirelessCountryCode or "PL"`, used at `:191` (hostapd `countryCode`) and `:308` (backup conf
`country_code=`). The schema has **no country field**: `horizon-rs/lib/ethos/horizon.ethos:66` — `RouterInterfaces.{
Interface Interface WlanBand Integer WlanStandard Option<SecretReference> Option<BackupWireless> }`, the same seven in
`horizon-rs/lib/src/model.rs:167-176`, so PL is always the fallback; `checks/router-wifi-horizon-policy/default.nix`
forbids the literal in the hostapd attribute but tolerates it in that fallback. **Transmit power is set nowhere** — no
`txpower` anywhere in `modules/nixos/router/`, not in the radio block (`:186-209`) nor the generated backup conf
(`:302-323`), and no field for it in the schema. On the host: `iw reg get` → `country PL: DFS-ETSI`, 2400-2483 @ 20
dBm; `iw phy phy0 info` → `2437.0 MHz [6] (20.0 dBm)`; `iw dev` → `wlp195s0 … type AP, channel 6, txpower 3.00 dBm`;
driver `mt7925e`; kernel 7.0.1; no txpower/SAR/regulatory line in `journalctl -b -k`.

Claim (delegated web research, sources dated 2026): the 3.00 dBm is a **known reporting artifact**, not the
configured value — `mt7925_mcu_set_rate_txpower()` programs the SKU tables but never assigns
`phy->txpower_cur`, so `mt76_get_txpower()` returns a stale constant (linux-wireless and linux-mediatek
threads, May 2026, maintainers Sean Wang and Javier Tia; openwrt/mt76 #1076; morrownr/USB-WiFi #576). `iw set
txpower` exiting 0 with no effect is a separate, still-open gap, called orthogonal by Javier Tia in the same
thread. No source measured actual AP-mode EIRP, so that rests on maintainer assertion. A genuine depressor
does exist — the CLC-before-SAR ordering bug fixed 2026-06-17 (Fixes: 9557b6fe0c8b), postdating the kernel
prometheus runs. Flow's inference: the 50-220 ms jitter is not explained by the reported number; documented
mt7925e AP-mode bugs (use-after-free in `mt76_wcid_add_poll()`, openwrt/mt76 #1096, open) fit better.
## 2. Dongle policy — the hazard is real and unguarded; the shape is bridge, not share
`modules/nixos/router/default.nix:386-399`: `"30-usb-eth"` matches `Type = "ether"` + `Driver =
"cdc_ether cdc_ncm r8152 ax88179_178a asix"` and sets `Bridge = br-lan`. Every USB NIC with those
drivers joins `br-lan` **by driver, never by which side it faces**. WAN is the single fixed
`routerInterfaces.wan` (`:375`); for prometheus that is `eno1` (proposal.datom:1: `Some.{eno1
wlp195s0 TwoG 6 Wifi4 Some.{routerWifiSaePasswords} Some.{wlp199s0f0u4 criome-backup TwoG 11 Wifi4
{routerBackupWifiPassword}}}`). Live: `eno1` UP `192.168.1.16/24`, default via `192.168.1.1` — **the
uplink is the built-in wired port today, not the dongle**. `enp199s0f0u2c2` is `NO-CARRIER`, `master
br-lan`. `br-lan` holds `10.18.0.1/24` (`CriomOS-lib/lib/default.nix:89-91`) with kea serving
`.100-.240` (`:228-243`), `wlp195s0` bridged in (`:203-205`).

So plugging the upstream LAN into the dongle does **not** loop through prometheus (eno1 is not a bridge port) but
**merges** the upstream L2 segment into `br-lan`: two DHCP servers on one segment, LAN clients getting 192.168.1.x,
upstream hosts reaching `10.18.0.1`, and the nftables input chain admitting all of `br-lan` unfiltered (`:153`).
`40-br-lan` sets `bridgeConfig = { }` (`:403`) — STP off, no loop guard. The design guards against none of it; it has
no notion of an uplink port, and its only USB shape is **bridge** — the opposite of "distributing internet from
whatever it's getting". Hotplug itself is already safe (`ConfigureWithoutCarrier = true`, `RequiredForOnline = "no"`,
`systemd-networkd.restartIfChanged = false` at `:260`): a dongle plugged after boot does not break the network. The
gap is direction, not hotplug.

## 3. Center sharing is unreachable for this cluster
`modules/nixos/network/networkd.nix:15` — `mkIf (behavesAs.center && !behavesAs.router)`, comment at `:14` "Router
nodes provide their own networkd config with bridge/hostapd". It shares `10.47.0.1/24` with `DHCPServer` +
`IPMasquerade` on USB dongles (`:30-48`) — the *share* shape the living wants. But prometheus is `LargeAiRouter`,
which per `CriomOS-test-cluster/fixtures/horizon/atlas.json` projects `router=true center=true` → excluded; ouranos is
`EdgeTesting` and zeus is `Edge` → `center=false` (cedar/dune fixtures) → excluded. **No goldragon node satisfies
it**, matching the witness that 10.47.0.1/24 is active nowhere. Nothing in the source says it was meant for ouranos or
zeus; it was written for a center-but-not-router node the cluster does not have.

## 4. Backup radio, and 5 GHz
The module emits a udev rule (`:250-252`) and a `BindsTo`/`WantedBy` device unit (`:281-295`), so `criome-backup`
starts **only when `wlp199s0f0u4` appears**. Witnessed: `iw dev` shows only `phy#0` — the device does not exist;
`hostapd-backup-wireless` is `inactive`. So it is configured to be up and simply has no radio plugged in; `:282` and
`:256-258` give its purpose — emergency AP, router access being the recovery path during upgrades. **No 5 GHz AP is intended**: prometheus declares `TwoG` ch 6 and the module emits one radio per
`routerInterfaces.wlan` (`:187-209`); `FiveG` exists (horizon.ethos:46) but is unused, though the hardware supports it
(phy0 lists 5180-5300 MHz).

## 5. Staleness, and what a Lojix deploy would change
Generation 51, `2026-07-03 06:40`, `/nix/store/j1362haqmyh5ha7bg9ds780yzpsjchav-nixos-system-prometheus-26.05.20260422.0726a0e`;
`/run/current-system/configuration-revision` does not exist. Claim (inference): the deployed revision is at or just
before CriomOS `3aa4780` (2026-07-03) — its `flake.lock` pins `pkgs` at 281bc63c (2026-05-03), the wrapper yielding
nixpkgs 20260422, and that pin holds unchanged from May to 2026-07-10. Diffs `3aa4780..main` over
`modules/nixos/router modules/nixos/network` (93+/91-, 9 files):
- **Schema rename only, no behavior change**: `horizon.node.routerInterfaces` → `horizon.node.network.routerInterfaces`;
  `wpa3SaePassword.name` → `wpa3SaePasswordReference` (bare string); `backupWireless.password.name` →
  `passwordReference`; `cluster.name` → `horizon.cluster`; `mkIf` → `optionalAttrs`; the same rename wave in
  dnsmasq/headscale/network-default. `nordvpn.nix` rewritten (101 lines); the rest touched by renames only.
- **No change to hostapd country, channel, power, the `30-usb-eth` match, the nftables ruleset, or `networkd.nix` — a
  deploy would not fix the Wi-Fi.**
- `pkgs` moves 2026-05-03 → 2026-08-13 (c64ea0e). Claim: that carries a kernel newer than the running 7.0.1 and would
  pick up the 2026-06-17 mt7925 CLC fix — the only radio-relevant part of a deploy.
- Risk, claim, unverified: main pins horizon 40d04d2 whose `NodeCapability` carries `Router`/`Center`
  (horizon.ethos:71), while prometheus's capability vector in the checked-out proposal.datom is `[TailnetClient
  NixBuilder.Some.6 NixCache VmHost.{…}]` — neither. If `behavesAs.router` no longer projects true, a deploy silently
  turns the router module off. **Evaluate before deploying.**

## Recommended runtime fix (non-persistent, reversible)
None for transmit power: nothing to set, `iw set txpower` is a known no-op here, the 3 dBm is cosmetic. Instead, in
order: (1) `iw dev wlp195s0 station dump` for real per-client `signal` and `iw dev wlp195s0 survey dump` for channel
busy time — that separates weak radio from congested channel 6; (2) if busy, `hostapd_cli -i wlp195s0 chan_switch 5
2462` (ch 11), a live CSA reverted by switching back or restarting hostapd; (3) **do not** plug the upstream LAN into
`enp199s0f0u2c2` while `30-usb-eth` stands — keep the uplink on `eno1`. Tailscale is `active` but `Logged out`;
reauthenticating is an act on the host, outside this flow, and is not a configuration defect.

## The configuration change that would make it durable
1. Give `RouterInterfaces` an uplink *set* instead of one `Interface` and elect WAN at runtime (carrier plus a DHCP
  offer or default route on the port). Until then, split `30-usb-eth` into an explicit bridge match and an explicit
  uplink match keyed on name or MAC from horizon.
2. Widen `networkd.nix:15` from `center && !router` to whatever "can be a gateway" means for ouranos and zeus — the
  share shape the living asked for is unreachable code today.
3. Add `country` to `RouterInterfaces` so PL stops being a hard-coded fallback, and enable STP in `40-br-lan`'s
  `bridgeConfig` as a cheap guard against the merge in §2.

## Questions for the living
1. Internet reaches prometheus today on the built-in wired `eno1` (192.168.1.16, gateway 192.168.1.1), and the USB
  adapter `enp199s0f0u2c2` is plugged in with no cable. Should that adapter *become* the uplink — you move the house
  cable onto it — or stay a downstream port with the uplink on `eno1`?
2. "Set up that USB trick everywhere": on ouranos and zeus, is the case "plug a USB-Ethernet adapter into the laptop,
  cable it to a machine, and that machine gets internet from the laptop's Wi-Fi", or "the laptop gets its internet
  *from* the USB adapter"?
3. `criome-backup` (ch 11) is configured and starts by itself the moment `wlp199s0f0u4` is plugged in — it is simply
  absent. Is that dongle meant to live in prometheus permanently, or be plugged in only when the main AP is down?
4. Prometheus's AP is 2.4 GHz only though the hardware does 5 GHz. For the zeus transfer, do you want a 5 GHz AP added
  (faster, shorter range), or should it go over a cable as you said?
