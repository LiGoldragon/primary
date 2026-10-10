# Unified home WiFi roaming — source-grounded research

Flow b80e55, 2026-09-22. Research only — no implementation, no secrets.

## What already exists in CriomOS

The infrastructure is further along than a greenfield design:

- **`clavifaber`** (flake input `LiGoldragon/clavifaber`): issues a self-signed
  CA certificate from a GPG Ed25519 key, then issues server and node
  certificates for WiFi EAP-TLS. Commands accept one `ClaviFaberRequest` datom
  and print one `ClaviFaberResponse` datom. Pure tests plus an impure GPG
  lifecycle test exist.
- **`wifi-pki.nix`** (router module): provisions server key directory before
  hostapd starts. Prints enrollment instructions when the key is missing.
- **`wifi-eap.nix`** (client module): deploys an NM connection with
  `key-mgmt=wpa-eap`, `eap=tls`, using `node.name` as identity, CA cert at
  `/etc/criomOS/wifi-pki/ca.pem`, node cert at
  `/etc/criomOS/wifi-pki/<node>.pem`, and the complex's private key. Gated on
  `wifiCertificate` in `horizon.node.capabilities`.
- **Router hostapd**: WPA3-SAE on the primary SSID (`${cluster}.criome`),
  password from sops. Comment in source: "EAP-TLS will replace this once PKI
  is deployed." The backup wireless runs WPA2-PSK-SHA256.
- **Constants**: CA cert, certs dir, server dir, server cert, server key — all
  defined paths in `CriomOS-lib/lib/default.nix`.
- **Hostapd 2.11** in nixpkgs, NixOS module has freeform `settings` for any
  hostapd directive including 802.11r/k/v parameters.

## 1. WPA2/WPA3 Personal vs Enterprise EAP-TLS

| | WPA3-SAE (current) | WPA2/3-Enterprise EAP-TLS |
|---|---|---|
| **Infrastructure** | One sops-managed password per SSID | CA + per-node certs (clavifaber exists), RADIUS (hostapd's integrated or FreeRADIUS) |
| **Per-device identity** | No — shared credential | Yes — each node has `<name>.pem`, revocation per-device |
| **Client compat** | All modern devices | Android 10+, iOS 13+, macOS 10.15+, NixOS/Linux (NM + wpa_supplicant) — older IoT may not support |
| **Credential rotation** | Change one password everywhere | Reissue one node's cert; others unaffected |
| **Roaming** | Works with 802.11r FT-SAE | Works with 802.11r FT-EAP |
| **CriomOS readiness** | Deployed today | Modules exist but EAP-TLS path is commented out; clavifaber issues certs |

**Tradeoff**: WPA3-SAE is live and working now. EAP-TLS gives per-device
identity and revocation but needs: (a) CA bootstrapped with clavifaber,
(b) server certs deployed to each AP, (c) node certs deployed to each client,
(d) hostapd switched from `wpa3-sae` to `wpa-eap` or a mixed mode.

## 2. Certificate lifecycle

The tooling exists. The lifecycle:

1. **CA creation**: `clavifaber` derives from a GPG Ed25519 key (operator's
   YubiKey or gpg-agent). CA cert → `/etc/criomOS/wifi-pki/ca.pem` on all
   nodes (distribute via sops or CriomOS activation).
2. **Server cert**: `clavifaber server-cert --ca-keygrip <kg> --ca-cert ca.pem
   --cn <host>.criome --out-cert server.pem --out-key server.key`. Deploy
   `server.key` to `/etc/criomOS/wifi-server/server.key` via sops.
3. **Node cert**: `clavifaber node-cert --ca-keygrip <kg> --ca-cert ca.pem
   --ssh-pubkey "$(cat /etc/criomOS/complex/ssh.pub)" --cn <name>
   --out <name>.pem`. Deploy to `/etc/criomOS/wifi-pki/<name>.pem`.
4. **Revocation**: reissue CA or maintain a CRL. Not yet implemented in
   clavifaber — a CRL or OCSP service would be a new component.
5. **Renewal**: set cert validity (default from clavifaber unknown — check
   `certificate_validity_window.rs` test). A cron/timer on Prometheus with
   CA access could auto-renew.
6. **Phone enrollment**: phones can't use the complex key path. Options:
   (a) PKCS#12 bundle transferred via USB/AirDrop/QR, (b) a SCEP/EST
   enrollment web endpoint on Prometheus, (c) WPA3-SAE as the phone SSID
   with EAP-TLS for cluster nodes only.

**Storage**: CA private key in sops (age-encrypted, Goldragon 8c4d03de
recipient). Server keys in sops per-node. Node certs are public and can be
in the repo or generated at activation.

## 3. 802.11k/v/r fast roaming

| Standard | What it does | hostapd directive | Client support |
|---|---|---|---|
| **802.11k** (RRM) | AP sends neighbor reports so clients know which AP to roam to | `rrm_neighbor_report=1` | iOS, Android 8+, most laptops |
| **802.11v** (BSS transition) | AP can suggest a client move to a better AP | `bss_transition=1` | iOS, Android 9+, macOS |
| **802.11r** (FT) | Fast BSS transition — pre-authenticates with the target AP during roam, <50ms handoff | `ieee80211r=1`, `mobility_domain=<hex>`, `ft_over_ds=1`, `ft_psk_generate_local=1` (for SAE) or FT-EAP keys | iOS, Android 10+, most laptops. Some older IoT devices disconnect |

**Requirements for roaming**:
- All APs share the same SSID, same security mode, same mobility domain ID
- `nas_identifier` set per AP (unique, e.g. MAC-derived)
- For FT-SAE: `ft_psk_generate_local=1` avoids needing a shared key table
- For FT-EAP: PMK-R0 and PMK-R1 key holders must be configured (each AP
  needs to know the others)

**NixOS hostapd module**: the freeform `settings` attribute on both radio
and network levels accepts all these directives. CriomOS already uses
`settings.bridge` — adding roaming is the same mechanism:

```nix
settings = {
  bridge = lanBridgeInterface;
  ieee80211r = 1;
  mobility_domain = "c710";   # same on all APs
  ft_over_ds = 1;
  ft_psk_generate_local = 1;  # SAE mode
  rrm_neighbor_report = 1;    # 802.11k
  bss_transition = 1;         # 802.11v
  nas_identifier = "...";     # unique per AP
};
```

## 4. Ouranos AP — only when wired Internet exists

Immediate Ouranos API setup is canceled. Source-backed proposal:

A CriomOS module that starts hostapd on Ouranos's WiFi NIC conditionally:

```nix
# Proposed shape — not a deployment
systemd.services.hostapd = {
  after = [ "systemd-networkd-wait-online@enp0s31f6.service" ];
  bindsTo = [ "sys-subsystem-net-devices-wlp0s20f3.device" ];
  # Only start when wired has carrier + DHCP lease
};
```

Implementation options:
- **networkd `RequiredForOnline`**: `enp0s31f6.network` with
  `[Link] RequiredForOnline=routable` — hostapd starts only after wired is
  routable
- **systemd path unit**: watch for `/run/systemd/netif/links/*/carrier`
- **Condition in service**: `ExecCondition` checking `ip route get 1.1.1.1`
  selects `enp0s31f6`

This needs the USB sharing capability in Horizon (same question as the
USB Internet sharing) to gate which nodes run an AP.

## 5. Prometheus AP

Already runs hostapd with WPA3-SAE on `wlp195s0` in `br-lan`. For unified
roaming:

- Same SSID (already `${cluster}.criome`)
- Same security mode (both SAE or both EAP-TLS)
- Same `mobility_domain` in `settings`
- Prometheus could also host the RADIUS server (hostapd's integrated RADIUS
  or FreeRADIUS) for EAP-TLS — it's the always-on router node

For integrated RADIUS in hostapd:
```
# In hostapd settings
ieee8021x=1
eap_server=1
eap_user_file=/etc/hostapd/eap_user
ca_cert=/etc/criomOS/wifi-pki/ca.pem
server_cert=/etc/criomOS/wifi-server/server.pem
private_key=/etc/criomOS/wifi-server/server.key
```

## 6. Design for existing cluster mechanisms

- **Secret storage**: sops-nix with age. CA private key → sops binary secret.
  Server key → sops binary secret per router node. Node certs → public,
  derivable from the complex SSH pubkey.
- **Horizon capability**: `wifiCertificate` already exists and gates
  `wifi-eap.nix`. A `WifiAccessPoint` capability could gate the AP module.
  `UsbInternetSharing` (the earlier question) is the same pattern.
- **Credential ownership**: the GPG keygrip for the CA stays with the
  operator (the living). clavifaber reads it via gpg-agent. No agent ever
  holds the CA private key.

## 7. Recommendation

**Phase 1 (immediate value, low risk):**
Add 802.11r/k/v settings to the existing WPA3-SAE hostapd config on
Prometheus. Six lines in `settings`. Clients that support FT-SAE roam
seamlessly; others still connect normally. No new infrastructure.

**Phase 2 (when Ouranos AP is ready):**
Add Ouranos as a second AP with the same SSID, same SAE password (from
sops), same `mobility_domain`. Gate on wired Internet presence. Two APs,
seamless roaming.

**Phase 3 (when PKI is bootstrapped):**
Switch from SAE to EAP-TLS. clavifaber bootstraps the CA, issues server
and node certs. hostapd's integrated RADIUS on Prometheus. wifi-eap.nix
activates on clients. Phones stay on a SAE SSID or get PKCS#12 bundles.
Per-device identity and revocation.

**The RADIUS/CA service is a natural nexus component** — Mind designs the
signal contract, Field deploys it on Prometheus, clavifaber provides the
cert operations.

## Sources

- `modules/nixos/router/default.nix:186–211` — current hostapd config
- `modules/nixos/router/wifi-pki.nix` — server key provisioning
- `modules/nixos/network/wifi-eap.nix` — EAP-TLS client module
- `CriomOS-lib/lib/default.nix:55–61` — wifiPki constants
- `clavifaber/README.md` — CLI surface, test coverage
- `flake.nix:110–116` — clavifaber input
- hostapd 2.11 documentation — 802.11r/k/v directives
