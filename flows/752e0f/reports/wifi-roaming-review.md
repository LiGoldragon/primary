# Review — `flows/b80e55/reports/wifi-roaming-research.md` (Psyche High 752e0f)

Read-only review. Nothing in CriomOS, clavifaber, horizon-rs, or goldragon was
changed. Method: read the report; read the named source files at their current
revisions (CriomOS at `bd6a16d`, clavifaber pinned at `d0488014` in
`flake.lock`); grepped `Vision/`, `vision-raw/`, and `flows/*/vision/` for the
living's recorded words on Wi-Fi, roaming, access points, Ouranos, Yggdrasil,
Ethernet, DNS, firewall, and credentials; read the two witnessed network
records named in the brief.

## Verdict

**Not ready as a directive for Mind. Phase 1 is separable and ready with
named fixes; Phases 2 and 3 are not.**

Three reasons, in order of weight.

1. **Phase 2's central promise is unachievable under the witnessed topology.**
   The report concludes "Two APs, seamless roaming." Ouranos is *upstream* of
   Prometheus: Prometheus's `eno1` holds `10.44.0.148/24` with
   `default via 10.44.0.1` (witnessed, `flows/d8df70/witnesses/prometheus-firewall-2026-09-24.md`),
   while Prometheus's AP is bridged into `br-lan` on `10.18.0.0/24` with its own
   Kea and dnsmasq. An Ouranos AP sits in a different L2 broadcast domain and a
   different subnet with its own DHCP. 802.11r Fast BSS Transition preserves the
   802.11 association keying, not the IP lease — a client crossing between those
   two APs re-DHCPs and every session drops. FT requires both BSSes in one
   bridged L2. The report never raises subnet or bridge continuity. This is not
   a detail to fill in; it invalidates the phase as designed.

2. **Two factual claims about existing tooling are false**, and one of them the
   report inherited from CriomOS's own stale text (claims 5 and 17 below).

3. **The EAP client profile cannot match the AP.** `wifi-eap.nix` hardcodes
   `ssid=criome`; the live AP SSID is `${cluster}.criome`. Phase 3 would deploy
   a profile that never associates. The report reproduces `wifi-eap.nix`'s
   contents without noticing.

Phase 1 is worth separating and can go to Mind once the fixes in §4 are named —
but see §2 for why the living's recorded priority puts a reliability fix ahead
of it, and note that with one AP 802.11r yields nothing at all.

## 1. Claim table — what CriomOS actually has

Verdicts are against CriomOS `bd6a16d`, clavifaber `d0488014`, horizon-rs and
goldragon at their present checkouts.

| # | Report's claim | Verdict | Evidence |
|---|---|---|---|
| 1 | `clavifaber` is a flake input (`LiGoldragon/clavifaber`) | **True** | `CriomOS/flake.nix:110-116`; pinned rev `d0488014bf931a4690cc2f64a0b41c1df3435cab` at `CriomOS/flake.lock:526-548` |
| 2 | clavifaber issues a self-signed CA from a GPG Ed25519 key, then server and node certs for Wi-Fi EAP-TLS | **True** | `clavifaber/README.md:3-8`; `clavifaber/src/request.rs` — `CertificateAuthorityIssuance` (:59), `ServerCertificateIssuance` (:109), `ClientCertificateIssuance` (:173) |
| 3 | Commands accept one `ClaviFaberRequest` datom and print one `ClaviFaberResponse` datom | **True** | `clavifaber/src/main.rs:13-18`; `clavifaber/src/generated/clavifaber.rs:4-22` |
| 4 | Pure tests plus an impure GPG lifecycle test exist | **True** | `clavifaber/README.md:27-40`; `clavifaber/tests/` holds 7 files incl. `certificate_validity_window.rs` |
| 5 | Issuance runs as `clavifaber server-cert --ca-keygrip … --out-cert … --out-key …` and `clavifaber node-cert --ca-keygrip … --ssh-pubkey … --cn … --out …` (report §2 steps 2–3) | **False** | clavifaber has no `clap` dependency and no flag parser anywhere in `src/`. `main.rs:14` parses one datom text argument. The real forms are positional: `ServerCertificateIssuance.{ keygrip ca-cert cn out-cert out-key }` (`request.rs:109-168`) and `ClientCertificateIssuance.{ keygrip ca-cert ssh-pubkey cn out }` (`request.rs:173-219`). **The report copied these strings verbatim from CriomOS's own operator messages at `modules/nixos/router/wifi-pki.nix:34` and `modules/nixos/network/wifi-eap.nix:73`, which are themselves stale.** Both belong on Mind's fix list. |
| 6 | `wifi-pki.nix` provisions the server key directory before hostapd starts and prints enrollment instructions when the key is missing | **True** | `CriomOS/modules/nixos/router/wifi-pki.nix:18-39`; imported at `router/default.nix:90` |
| 7 | `wifi-eap.nix` deploys an NM connection with `key-mgmt=wpa-eap`, `eap=tls`, `node.name` as identity, CA at `/etc/criomOS/wifi-pki/ca.pem`, node cert at `<certsDir>/<node>.pem`, complex private key | **True** | `CriomOS/modules/nixos/network/wifi-eap.nix:20-47`; imported at `network/default.nix:74` |
| 8 | It is gated on `wifiCertificate` in `horizon.node.capabilities` | **True as code, dead in practice** | Gate at `wifi-eap.nix:14`; capability exists as `WifiCertificate.NoSettings` in `horizon-rs/lib/ethos/horizon.ethos:71`, `model.rs:224`, `projection/views.rs:139`. **But no node declares it** — every node's capability vector in `/git/github.com/LiGoldragon/goldragon/cluster-definition.datom` lacks it, so `wifi-eap.nix` takes its `!hasWifiCertPubKey` branch on every host today. The report presents the gate as if it were merely waiting on certs. |
| 9 | Router hostapd runs WPA3-SAE on the primary SSID `${cluster}.criome`, password from sops | **True**; cited lines wrong | `router/default.nix:203-231` (`mode = "wpa3-sae"`, `saePasswordsFile = config.sops.secrets.…path`), SSID default at `:37-39`. Report's Sources say `186–211`. |
| 10 | Source comment: "EAP-TLS will replace this once PKI is deployed" | **True**, verbatim | `router/default.nix:215` |
| 11 | The backup wireless runs WPA2-PSK-SHA256 | **True** | `router/default.nix` preStart heredoc: `wpa=2`, `wpa_key_mgmt=WPA-PSK-SHA256`, `wpa_pairwise=CCMP`, `ieee80211w=1` |
| 12 | CA cert, certs dir, server dir, server cert, server key are defined in `CriomOS-lib/lib/default.nix:55–61` | **True, but in a different repository** | `/git/github.com/LiGoldragon/CriomOS-lib/lib/default.nix:55-61`. The report's Sources list reads as a path inside CriomOS. Mind would look in the wrong tree. |
| 13 | Hostapd 2.11 in nixpkgs; the NixOS module has freeform `settings` accepting any directive | **Partly unverifiable** | The freeform-`settings` half is true in use: `router/default.nix:224` already passes `settings = { bridge = …; }`. The *version* 2.11 was not evaluated here and is unverified. |
| 14 | Prometheus already runs hostapd with WPA3-SAE on `wlp195s0` in `br-lan` | **True** | Declared: `goldragon/cluster-definition.datom`, prometheus `routerInterfaces` = `{ eno1 wlp195s0 TwoG 6 Wifi4 Some.{ routerWifiSaePasswords } Some.{ wlp199s0f0u4 criome-backup TwoG 11 Wifi4 { routerBackupWifiPassword } } }`. Witnessed live: `flows/d8df70/witnesses/prometheus-firewall-2026-09-24.md` nft ruleset names `wlp195s0` and `wlp199s0f0u4`. |
| 15 | Revocation is not yet implemented in clavifaber; a CRL/OCSP service would be new | **True** | No `crl`, `revok`, or `ocsp` anywhere in `clavifaber/src/` |
| 16 | Certificate validity default "unknown — check `certificate_validity_window.rs`" | **Resolvable, and now resolved** | `clavifaber/src/x509.rs:106` CA = 10 years; `:146` server = 2 years; `:187` node = 2 years. Mind does not need to guess. |
| 17 | Ouranos's Wi-Fi NIC is `wlp0s20f3` and its wired uplink is `enp0s31f6` (report §4 code block) | **Unverifiable / not in any source** | `wlp0s20f3` appears nowhere in CriomOS, horizon-rs, or `cluster-definition.datom`. `enp0s31f6` appears only as a check *fixture* at `CriomOS/checks/usb-ipv4-gateway/default.nix:9`, not as Ouranos's declared interface. Ouranos's declared `routerInterfaces` field is **`None`** (`cluster-definition.datom`, ouranos entry). The report presents both names inside proposed Nix as though they were established. |
| 18 | Secrets are sops-nix with age, "Goldragon 8c4d03de recipient" | **Unverifiable here** | The secrets repository was not read in this review. sops usage itself is true (`router/default.nix:111,119`); the recipient fingerprint is unchecked. |
| 19 | A `WifiAccessPoint` capability could gate the AP module; `UsbInternetSharing` is the same pattern | **Report's inference — neither exists** | The capability enum at `horizon-rs/lib/ethos/horizon.ethos:71` contains neither name. The report hedges with "could", which is honest; Mind must read it as design, not inventory. |

## 2. Each phase against the living's recorded words

### Phase 1 — 802.11r/k/v on the existing Prometheus SAE AP

**Authority is thin and is not a ruling.** The only record asking for
802.11k/v/r research is the brief itself,
`flows/b80e55/vision/unifiedWifiRoamingAndCertAuth.md` (living's direction
relayed through 03e825, 2026-09-22, "Input mode not established"). That record
is a research instruction — "Research WPA2/WPA3 Personal vs Enterprise EAP-TLS
… 802.11k/v/r … source-backed proposal only" — and it explicitly says the work
"must not block the live network fix." A deployment recommendation is a step
past what that record authorizes.

**It sits against the living's stated priority.** From
`flows/753e69/vision/prometheusWifiReliability.md`, living, 2026-09-21:

> "I tried again to connect to colddragon.criome, my Wi-Fi access point on my
> phone, and failed. It went to get an IP address and maybe even got one, and
> then it just disconnected."

and:

> "Whatever the problem was, we need to put a fix in that would not let that
> happen again because there seems to be a reliability issue there."

That defect — a phone associating, getting a lease, then dropping — is open.
802.11v BSS-transition management and FT are exactly the mechanisms that can
produce that symptom on clients that handle them poorly; the report itself
notes "Some older IoT devices disconnect." Adding them now confounds the
diagnosis of the very failure the living asked to be fixed first. The living's
words do not forbid Phase 1; they order the reliability fix ahead of it.

**And with one AP it buys nothing.** FT is a *transition* between BSSes. The
report calls Phase 1 "immediate value" — that is the report's inference, and it
is wrong as stated. The one place FT could act today is between `wlp195s0` and
the backup radio `wlp199s0f0u4`, which *are* both bridged into `br-lan`. The
report never notices that the backup AP is a real second BSS on the same L2,
and its Phase 1 leaves the backup AP out.

### Phase 2 — Ouranos AP gated on wired Internet

**The mode is the living's; the trigger is not.** From
`flows/753e69/vision/transitiveNetworkTopologyAndCertificateWifi.md`, living
direct to Field Medium `753e69`, 2026-09-22:

> "There are some nodes, like Uranus, when it gets its internet from the
> Ethernet and it's put into stable mode. For now, it's just a concept, but I
> would say maybe it's a script that goes into stable Ethernet mode, and it
> becomes a Wi-Fi access point itself. That would be a feature, like an
> opportunistic Wi-Fi access point or something like that, or a mode: optional
> Wi-Fi access point, right?"

and, in the same breath:

> "If somebody is in the right admin mode, like one of the right users, like
> network users or whatever, they can toggle the stable Ethernet mode."

The living described an **operator-toggled mode**, entered by an authorized
user. The report replaces that with **automatic carrier detection** —
`RequiredForOnline=routable`, a systemd path unit on
`/run/systemd/netif/links/*/carrier`, or `ExecCondition` running
`ip route get 1.1.1.1`. Wired carrier is a *precondition* the living stated;
it is not the trigger he described. Building the automatic version would
deliver a different feature from the one on record. **Conflict — name it to
the living before building.**

**The shared password is supported.** Same record, same paragraph: "I guess we
can use the same password for now." Phase 2's "same SAE password (from sops)"
is consistent.

**The topology defeats the phase.** See the Verdict. Additionally, the living
has said the current Ouranos-upstream arrangement is itself the problem —
`flows/836818/vision/network.md`, STT, 2026-09-23, direct to Psyche High
836818:

> "It lies with how we reconfigure the network. It never really worked well
> from making Uranus [Ouranos] the upstream supplier to Prometheus."

Phase 2 adds a second access point on top of the arrangement the living says
never worked well, without resolving it. The report does not cite this record
at all.

### Phase 3 — graduation to EAP-TLS

**Well grounded.** Same 753e69 record, 2026-09-22:

> "eventually, for the certificate-based Wi-Fi client authentication, with the
> clients on my Android phones and/or on the other laptops, they all have their
> own certificates. … All these certificates are just on our own, like a
> self-bootstrapped authority."

Per-device certs, own CA, no external authority — the report's Phase 3 matches
this closely, and its §6 statement that the CA keygrip "stays with the operator
(the living)" and "No agent ever holds the CA private key" is consistent with
`flows/e1953c/vision/secrets.md` (the public part is not trusted with
credentials) and with `flows/e06e4c07/vision/gradientsOfAuthority.md`.

**One conflict inside the phase.** The report offers, in §2 option (c) and
again in the Phase 3 summary, "Phones stay on a SAE SSID or get PKCS#12
bundles." The living named Android phones explicitly as certificate holders.
Leaving phones on a shared password is the outcome the living's sentence rules
out. The PKCS#12 half is fine; the SAE-for-phones half conflicts and should
not survive into Mind's brief.

**One contradiction the report makes with itself.** §2 step 5 proposes "A
cron/timer on Prometheus with CA access could auto-renew." §6 says "No agent
ever holds the CA private key." A renewal timer on Prometheus is CA authority
resident on a machine. §6 is the one that matches the living's record; §2 step
5 must not be implemented as written.

## 3. What the report assumes that no record supports (its inferences)

Marked as the report's own, not as anything the living said or any source shows:

- **Automatic wired-carrier gating** in place of the living's operator toggle (§4).
- **`WifiAccessPoint` and `UsbInternetSharing` Horizon capabilities** (§6) — neither exists in `horizon.ethos:71`.
- **hostapd's integrated RADIUS on Prometheus** as the authentication home (§5) — no record names a RADIUS host, and Prometheus is the node carrying the open reliability complaint.
- **"The RADIUS/CA service is a natural nexus component"** (§7) — `Vision/nexus.md` says nothing about RADIUS or PKI. This is the report's framing.
- **`mobility_domain = "c710"`** (§3) — an arbitrary value presented in deployable Nix.
- **That Phase 1 is "low risk" with "no new infrastructure"** — inference, and contradicted by the open disconnect defect.
- **That Android will accept the self-signed CA as configured.** Android 11+ requires explicit CA installation plus a domain/server-certificate match on the EAP profile. Neither the report nor `wifi-eap.nix` addresses server-name matching. Unaddressed for the exact clients the living named.
- **That node certs are "public and can be in the repo"** (§6) — a policy decision no record makes.

## 4. What is missing for Mind to implement without guessing

**Gap 1 — exact modules, lines, and hosts, for each phase.**
Phase 1 touches exactly one attrset: `settings` at
`/git/github.com/LiGoldragon/CriomOS/modules/nixos/router/default.nix:224`, on
the single host with `behavesAs.router` — **prometheus**, per
`/git/github.com/LiGoldragon/goldragon/cluster-definition.datom`. The report
names neither the file line nor the host. It also omits the hand-rolled
`hostapd-backup-wireless` unit (`router/default.nix:318-370`), which writes a
raw hostapd config through a `preStart` heredoc and would need the *same*
mobility domain and matching directives added by hand there — it is the only
second BSS that exists today, and the only place Phase 1 can actually be
exercised. Mind needs: which two radios form the mobility domain, the domain
value, and the `nas_identifier` derivation rule.

**Gap 2 — Ouranos has no router role, no declared interfaces, and
NetworkManager owns its links.**
Ouranos's capability vector is `Edge / LowPower / NextGeneration / Nordvpn /
HardwareVideo / TailnetClient / TailnetController / NixBuilder.None /
OpenCodeTesting / PersonaDevelopment`, with `routerInterfaces = None`
(`cluster-definition.datom`). Because it is `Edge` and not router,
`enableNetworkManager` is true and
`CriomOS/modules/nixos/network/networkd.nix` is gated `center && !router`, so
NetworkManager owns every link. The report's sketched
`systemd.services.hostapd = { … }` would contend with NetworkManager for the
radio. Implementing Phase 2 therefore requires, at minimum:
a new capability variant in
`/git/github.com/LiGoldragon/horizon-rs/lib/ethos/horizon.ethos:71` with its
projection in `model.rs` and `projection/views.rs`; a `routerInterfaces`-like
record for Ouranos in `/git/github.com/LiGoldragon/goldragon/cluster-definition.datom`;
and a decision on whether NetworkManager or networkd owns the AP link. None of
these are named in the report. **Plus the L2/subnet question in the Verdict,
which must be answered before any of this is worth building.**

**Gap 3 — acceptance tests. The report proposes none.**
CriomOS has the convention already: `checks/router-wifi-secret/default.nix`
asserts by reading the router module's text. Mind needs at least
(a) a `checks/` assertion that `ieee80211r` and `mobility_domain` appear on
every AP definition and that the domain values match;
(b) a live test that a client moving between `wlp195s0` and `wlp199s0f0u4`
keeps its DHCP lease and an open TCP connection — that is the actual claim
"seamless roaming" makes, and it is the one the subnet problem would fail;
(c) a regression for the 753e69 symptom: associate, obtain a lease, hold
Internet reachability through `eno1` for a sustained interval. The
`testing-transitive-network-topology` skill already covers the chain the AP
depends on.

Secondary, but also missing: the SSID mismatch fix in
`network/wifi-eap.nix:23,29` (`ssid=criome` versus the live
`${cluster}.criome`); correction of the two stale clavifaber command strings
at `router/wifi-pki.nix:34` and `network/wifi-eap.nix:73`; and a decision on
where the CA certificate is distributed from — the report says "via sops or
CriomOS activation" and leaves it open.

## 5. Risks to what the living said to preserve

**Default DNS — the largest unexamined risk.** The router's dnsmasq listens on
`::1`, `127.0.0.1`, and the `br-lan` gateway, and serves the cluster's internal
names (`CriomOS/modules/nixos/network/dnsmasq.nix:26-33`,
`publicClusterDomains`); Kea hands `10.18.0.1` to clients as
`domain-name-servers` (`router/default.nix`, subnet4 option-data). The living's
record, `flows/f55ec8/vision/networking.md`:

> "Our own domain name servers that are configured locally are going to route
> us internally with our messenger and everything else, like our Git servers
> and our file access when we're at home on our own Wi-Fi, or on our own LAN,
> even through a foreign router as an intermediary."

An Ouranos AP run the obvious way — NetworkManager `ipv4.method=shared`, which
is exactly the mechanism already in use there for the Prometheus USB share —
starts NM's own dnsmasq and hands associated clients **Ouranos** as their DNS
server. Internal `.criome` resolution breaks for every device that lands on
that AP, and it breaks silently and intermittently, depending on which AP the
phone picked. **The report does not mention DNS once.** Any Phase 2 brief must
state explicitly which node serves DNS to AP clients and how that survives a
roam.

**Authentication.** Switching hostapd from `mode = "wpa3-sae"` to `wpa-eap`
removes the `saePasswordsFile` path that `checks/router-wifi-secret/default.nix`
asserts on by reading the module source — that check fails on the same commit
unless updated in lockstep. Separately, `router/default.nix:281-282` sets
`hostapd.restartIfChanged = false` and `stopIfChanged = false`, deliberately,
per the comment at `:275-279`: "Router access is the recovery path during
upgrades." So neither roaming settings nor an EAP switch take effect until an
explicit restart or reboot. Mind must plan that cutover — and must **not**
"fix" those flags as a convenience.

**Keys.** The CA private key never leaves the living's GPG agent; clavifaber
reaches it by keygrip only. The report's §2 step 5 auto-renewal timer "on
Prometheus with CA access" would move CA authority onto a machine, against its
own §6 and against `flows/e1953c/vision/secrets.md`. Do not implement it.
Note also that clavifaber has no revocation path at all (§1 claim 15), so a
compromised node cert currently has no remedy short of reissuing the CA — that
is a real constraint on Phase 3, not a footnote.

**Controller ownership.** Prometheus alone carries `Center`, `Router`, and the
LAN's Kea and dnsmasq. Ouranos carries `TailnetController`. Giving Ouranos an
AP with its own address pool and resolver makes it a second controller of
client network identity. No record asks for that; nothing in the living's words
moves LAN control off Prometheus. Phase 2 should say explicitly that Prometheus
remains the sole LAN controller, or ask.

**Firewall.** The live ruleset accepts inbound only on
`{ br-lan, yggTun, wlp195s0, wlp199s0f0u4 }`
(`flows/d8df70/witnesses/prometheus-firewall-2026-09-24.md`). Any new AP
interface must be added to that set or its clients cannot reach the router at
all. The report does not mention nftables.

## Sources

Report under review:
- `/home/li/primary/flows/b80e55/reports/wifi-roaming-research.md`

Living's words:
- `/home/li/primary/flows/753e69/vision/transitiveNetworkTopologyAndCertificateWifi.md` — living, direct to Field Medium 753e69, 2026-09-22; input mode not independently established
- `/home/li/primary/flows/753e69/vision/prometheusWifiReliability.md` — living, spoken in Field Sol native flow, 2026-09-21
- `/home/li/primary/flows/836818/vision/network.md` — living, STT, 2026-09-23; provenance established at transcript by Field High 9e735b
- `/home/li/primary/flows/b80e55/vision/unifiedWifiRoamingAndCertAuth.md` — relayed through 03e825, 2026-09-22; input mode not established
- `/home/li/primary/flows/f55ec8/vision/networking.md` — internal DNS and mesh over a foreign router
- `/home/li/primary/flows/e1953c/vision/secrets.md`; `/home/li/primary/flows/e06e4c07/vision/gradientsOfAuthority.md` — credential layering

Witnessed network state:
- `/home/li/primary/flows/d8df70/witnesses/prometheus-firewall-2026-09-24.md`
- `/home/li/primary/flows/836818/reports/prometheus-topology-2026-09-23.md`

Sources read at their current revisions:
- `/git/github.com/LiGoldragon/CriomOS` at `bd6a16d` — `flake.nix`, `flake.lock`, `modules/nixos/router/default.nix`, `modules/nixos/router/wifi-pki.nix`, `modules/nixos/network/wifi-eap.nix`, `modules/nixos/network/dnsmasq.nix`, `modules/nixos/network/resolver.nix`, `modules/nixos/network/networkd.nix`, `modules/nixos/node-services.nix`, `checks/router-wifi-secret/default.nix`, `checks/usb-ipv4-gateway/default.nix`
- `/git/github.com/LiGoldragon/clavifaber` at `d0488014` — `README.md`, `src/main.rs`, `src/request.rs`, `src/x509.rs`, `src/generated/clavifaber.rs`, `tests/`
- `/git/github.com/LiGoldragon/CriomOS-lib/lib/default.nix:55-61`
- `/git/github.com/LiGoldragon/horizon-rs/lib/ethos/horizon.ethos:71`, `lib/src/model.rs:224`, `lib/src/projection/views.rs:139`
- `/git/github.com/LiGoldragon/goldragon/cluster-definition.datom`

Not read, and so left unverified: the secrets repository (sops age recipients),
the evaluated hostapd package version.
