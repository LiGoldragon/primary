# System Data Purity And Wi-Fi PKI Survey

Role: system-specialist
Date: 2026-05-12

## Summary

CriomOS is close to the intended shape, but it still carries a few
production cluster facts directly in Nix modules. The worst case is the
known Wi-Fi password in `CriomOS/modules/nixos/router/default.nix`. The
second class is node-name gating, mostly around headscale, tailscale, and
an extra LLM firewall port. Those decisions should be projected from
Horizon instead of being re-derived in CriomOS.

The Wi-Fi certificate path is only half-built. ClaviFaber has the right
low-level primitives to issue a CA, a router/server certificate, and a
client certificate, and it can publish the public result in
`publication.nota`. The deployed CriomOS modules still assume the older
"complex key" shape and do not wire hostapd to EAP-TLS. Horizon also does
not yet have a first-class Wi-Fi policy shape: SSID, regulatory country,
authentication mode, CA certificate identity, and authorization policy are
missing or implicit.

The safe migration is: extend Horizon first, make ClaviFaber certificates
fit real EAP-TLS requirements, then replace the router's WPA3-SAE network
with an EAP-TLS network. Do not carry the current password forward as a
fallback unless Horizon explicitly declares a temporary migration SSID.

## Current Data Boundary

The intended boundary is still coherent:

- `goldragon/datom.nota` is the production cluster proposal.
- `horizon-rs` owns schema, validation, and derived projections.
- `CriomOS` consumes projected `horizon` and should not know cluster or
  node names except through that projection.
- `CriomOS-home` consumes projected `horizon` plus user profile data.
- `CriomOS-lib` can hold implementation constants, path conventions, and
  static open data. It should not become a hidden cluster database.
- `clavifaber` owns host key-material actions and public host
  publications. It should not become the cluster convergence runner.

A certificate is public material: it contains a public key, an identity,
extensions, validity, and a CA signature. The private key and CA signing
key are not public material and must never be committed into Horizon or
Nix code.

## Findings

### P0: Production Wi-Fi Password In CriomOS

Path:
`/git/github.com/LiGoldragon/CriomOS/modules/nixos/router/default.nix:88`
through `:99`

The router module hard-codes:

- regulatory country `PL`
- SSID `criome`
- authentication mode `wpa3-sae`
- literal SAE password value

This is both a secret leak and a cluster policy leak. SSID, country, and
authentication policy belong in Horizon. The password should disappear
instead of moving to another Nix file.

Target shape:

- Horizon declares Wi-Fi policy.
- ClaviFaber provisions certificate material.
- CriomOS renders hostapd from Horizon plus local file path constants.

### P0: Wi-Fi EAP Client Module Points At Stale Private Key Material

Path:
`/git/github.com/LiGoldragon/CriomOS/modules/nixos/network/wifi-eap.nix:10`
through `:38`

`wifi-eap.nix` is gated by `horizon.node.hasWifiCertPubKey`, writes an
EAP-TLS NetworkManager profile, and points `private-key` at
`constants.fileSystem.complex.keyFile`:

- current value:
  `/etc/criomOS/complex/key.pem`
- current ClaviFaber architecture:
  ClaviFaber does not generate or own this key.

Current ClaviFaber signs the client certificate against the host's
OpenSSH Ed25519 public key. For EAP-TLS to work, the private key used by
NetworkManager must match the public key inside the client certificate.
That gives us a real design decision:

- reuse `/etc/ssh/ssh_host_ed25519_key` as the EAP-TLS private key, or
- extend ClaviFaber to generate a dedicated Wi-Fi client keypair and
  certificate.

Reusing the SSH host key is simple and matches current ClaviFaber code,
but it couples Wi-Fi identity to SSH host identity. A dedicated Wi-Fi key
is cleaner, but it requires a new ClaviFaber request and publication
shape.

### P0: Router Wi-Fi PKI Is Not Wired To hostapd

Path:
`/git/github.com/LiGoldragon/CriomOS/modules/nixos/router/wifi-pki.nix:18`
through `:39`

`wifi-pki.nix` only prepares the server key directory and prints stale
command hints. It does not configure hostapd to use:

- CA certificate
- router/server certificate
- router/server private key
- EAP server settings
- client identity authorization policy

The actual hostapd network remains WPA3-SAE in
`router/default.nix`.

### P1: ClaviFaber Has Primitives, Not A Complete Wi-Fi PKI Flow

Paths:

- `/git/github.com/LiGoldragon/clavifaber/src/request.rs:21`
  through `:29`
- `/git/github.com/LiGoldragon/clavifaber/src/request.rs:247`
  through `:303`
- `/git/github.com/LiGoldragon/clavifaber/src/request.rs:393`
  through `:463`
- `/git/github.com/LiGoldragon/clavifaber/src/publication.rs:13`
  through `:24`
- `/git/github.com/LiGoldragon/clavifaber/src/x509.rs:122`
  through `:204`

Ready:

- `CertificateAuthorityIssuance`
- `ServerCertificateIssuance`
- `ClientCertificateIssuance`
- `YggdrasilKeypairSetup`
- `PublicKeyPublicationWriting`
- publication can include SSH public key, Yggdrasil projection, and Wi-Fi
  client certificate PEM.

Gaps:

- `CriomOS/modules/nixos/complex.nix:24` through `:31` currently invokes
  only `PublicKeyPublicationWriting` with no Yggdrasil keypair and no
  Wi-Fi certificate.
- Current X.509 issuance adds basic constraints, key usage, and subject
  key identifier, but I did not find Subject Alternative Name or Extended
  Key Usage handling.
- Server certificates should carry a server identity clients can validate.
- Client certificates should carry client authentication intent.
- Tests should assert the certificate extensions required by the chosen
  EAP-TLS policy.

I would not deploy EAP-TLS until ClaviFaber grows or confirms these
certificate-shape requirements.

### P1: Horizon Schema Lacks Wi-Fi Policy

Paths:

- `/git/github.com/LiGoldragon/horizon-rs/lib/src/proposal.rs:36`
  through `:94`
- `/git/github.com/LiGoldragon/horizon-rs/lib/src/proposal.rs:96`
  through `:104`
- `/git/github.com/LiGoldragon/horizon-rs/lib/src/node.rs:329`
  through `:348`
- `/git/github.com/LiGoldragon/goldragon/datom.nota:82`
  through `:115`

Horizon currently has:

- `NodeProposal.wifi_cert: bool`
- `NodeProjection.has_wifi_cert_pub_key = self.wifi_cert`
- `RouterInterfaces` for WAN/WLAN interface, band, channel, and standard.

It does not have:

- SSID
- regulatory country
- Wi-Fi authentication mode
- CA public certificate or CA certificate fingerprint
- EAP server identity policy
- authorized Wi-Fi client identity list
- migration/fallback SSID policy

The `wifi_cert` boolean is too small for the deployed surface. It can
remain as a derived convenience, but the source data should become an
explicit Wi-Fi policy record.

### P1: Node Names Still Gate Services In CriomOS

Paths:

- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/network/tailscale.nix:7`
  through `:19`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/network/headscale.nix:12`
  through `:23`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/nix.nix:73`
  through `:80`

Current hard-coded node decisions:

- tailscale runs only on `ouranos` and `prometheus`
- headscale runs only on `ouranos`
- port `11436` opens only on `prometheus`

These should be Horizon-derived capabilities or roles, for example:

- `node.services.tailscale.enable`
- `cluster.headscale.serverNode` or `node.services.headscale.enable`
- `node.services.largeAi.openFirewallPorts`

This also removes the brittle fallback
`ouranos.${cluster.name}.criome`.

### P1: CriomOS-lib Holds Some Cluster Policy As Constants

Path:
`/git/github.com/LiGoldragon/CriomOS-lib/lib/default.nix:66`
through `:103`

Probably OK as implementation constants:

- runtime directory names
- `/etc/criomOS/wifi-pki/...` paths
- Yggdrasil interface name
- Nix service port conventions, if these are CriomOS protocol defaults

Probably Horizon data:

- LAN subnet `10.18.0.0/24`
- LAN gateway `10.18.0.1`
- Wi-Fi ULA suffix, if it is specific to the goldragon network

The bridge name `br-lan` is duplicated in
`router/default.nix:17` and `network/dnsmasq.nix:20`. If it is just a
CriomOS implementation convention, move it into `CriomOS-lib`. If it is
deployment policy, move it into Horizon.

### P2: CriomOS-home Has One Naming Leak

Path:
`/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/pi-models.nix:37`
through `:60`

The endpoint is correctly found through Horizon:

- first node with `typeIs.largeAiRouter`
- otherwise first node with `behavesAs.largeAi`

But the provider namespace is hard-coded as `prometheus`. That is not a
network endpoint leak, but it is a node-name leak in user-facing config.
Rename it to a role name such as `criomos-local` unless the model IDs
intentionally need to reveal the serving node.

The open model inventory in `CriomOS-lib/data/largeAI/llm.json` is not a
cluster secret. It is acceptable static Nix data under the carve-out for
open-source models.

### P2: Live ISO Root Password Is A Credential In Nix

Path:
`/git/github.com/LiGoldragon/CriomOS/modules/nixos/disks/liveiso.nix:16`

`users.users.root.initialPassword = "r"` is not node or cluster data, but
it is still a credential in Nix. This is only acceptable for explicitly
local disposable installer images. If the ISO is distributed, it should
move to a documented local build-time override or be disabled.

### P2: WireGuard Proxy Helper Looks Wrong

Path:
`/git/github.com/LiGoldragon/CriomOS/modules/nixos/network/wireguard.nix:26`
through `:29`

`mkUntrustedProxy` receives `untrustedProxy` but inherits `publicKey` and
`endpoint` from `wireguardUntrustedProxies`, which is the whole list. It
looks like it should inherit from the argument. This is outside the Wi-Fi
data-purity path, but it is a real-looking bug to fix separately.

## Proposed Horizon Shape

Add a cluster Wi-Fi policy to `horizon-rs` rather than putting more
fields directly on every module.

Example shape, names still subject to the naming discipline:

```nota
(WifiPolicy
  "criome"
  "PL"
  EapTls
  (WifiCertificateAuthority
    "sha256:..."
    "-----BEGIN CERTIFICATE-----...")
  (WifiServerIdentity
    "wifi.goldragon.criome")
  (WifiClientAuthorization HorizonNodes))
```

Projected fields should give CriomOS enough to render both sides:

- router/AP view:
  - SSID
  - country
  - auth mode
  - CA certificate path or installed file content
  - server certificate path
  - server private key path
  - allowed client identity policy
- client view:
  - SSID
  - auth mode
  - CA certificate path or installed file content
  - expected server identity
  - client certificate path
  - matching client private key path

Private key paths are local implementation facts and can come from
`CriomOS-lib` constants. Public certificates and fingerprints can come
from Horizon.

## ClaviFaber Integration Plan

1. Decide the client private key strategy.

   Option A: client certificates bind to `/etc/ssh/ssh_host_ed25519_key`.
   This matches current ClaviFaber code, but it reuses the SSH host key
   for Wi-Fi authentication.

   Option B: ClaviFaber grows a dedicated Wi-Fi client keypair request.
   This is cleaner and isolates failure domains, but it needs new code,
   publication schema, tests, and migration handling.

2. Add X.509 extension coverage before production use.

   Server certs should have a server identity clients can validate.
   Client certs should be explicitly suitable for client auth. Tests
   should assert the certificate profile, not just that a PEM file parses.

3. Keep CA private material out of Horizon.

   Horizon can carry the CA public certificate or fingerprint. The CA
   private key stays in GPG/keygrip-backed local state on the signer.

4. Let a cluster trust runtime consume publications.

   ClaviFaber should keep writing `publication.nota`. A separate trust
   runtime should collect those public records and update the data repo or
   its successor. This matches
   `reports/designer/110-cluster-trust-runtime-placement.md`, whose
   relevant point is that ClaviFaber produces public host material and a
   separate runtime incorporates it into cluster trust.

5. Update CriomOS rendering.

   The router module should render hostapd EAP-TLS from Horizon. The
   client module should render NetworkManager EAP-TLS from Horizon and
   point at the matching private key.

## Wi-Fi Migration Process

1. Extend `horizon-rs` with a Wi-Fi policy record, projection fields, and
   tests.

2. Add the production Wi-Fi policy to `goldragon/datom.nota`.

3. Update ClaviFaber certificate issuance:

   - add or verify SAN/EKU policy
   - decide SSH-host-key reuse versus dedicated Wi-Fi keypair
   - add tests for the certificate profile
   - ensure `PublicKeyPublicationWriting` includes the final client
     certificate data needed by the trust runtime

4. Update CriomOS client wiring:

   - stop using `/etc/criomOS/complex/key.pem`
   - use the matching private key
   - use Horizon SSID and CA/server identity policy
   - keep the NetworkManager profile generated from declarative inputs

5. Update CriomOS router wiring:

   - replace WPA3-SAE with EAP-TLS hostapd settings
   - use local server cert/key paths
   - use Horizon CA and authorization policy
   - keep any migration fallback as an explicit Horizon migration policy,
     not as a hard-coded password

6. Stage safely:

   - deploy cert material to router and one client
   - test with a temporary EAP-TLS SSID or maintenance window
   - switch default SSID once client auth is proven
   - remove the old SAE password from the deployed config

## External Implementation Notes

NetworkManager keyfile profiles support an `[802-1x]` section, which is
the right client-side surface for EAP-TLS. The current `wifi-eap.nix`
already writes that style of profile, but it uses the wrong private key
source.

hostapd can run an internal EAP server for EAP-TLS using settings such as
`ieee8021x`, `eap_server`, `ca_cert`, `server_cert`, and `private_key`.
If we later need richer authorization policy than "cert chains to this
CA and identity is allowed", FreeRADIUS becomes the more explicit policy
engine. For the first cluster migration, hostapd internal EAP is likely
enough if Horizon provides the identity policy.

References:

- NetworkManager keyfile settings:
  https://networkmanager.pages.freedesktop.org/NetworkManager/NetworkManager/nm-settings-keyfile.html
- NixOS hostapd module source:
  https://raw.githubusercontent.com/NixOS/nixpkgs/ed142ab1b3a092c4d149245d0c4126a5d7ea00b0/nixos/modules/services/networking/hostapd.nix
- hostapd example configuration:
  https://sources.debian.org/data/main/w/wpa/2%3A2.10-25/hostapd/hostapd.conf

## Immediate Next Work

1. Create a Horizon Wi-Fi policy design bead and implement it in
   `horizon-rs`.

2. Fix `wifi-eap.nix` only after the client private key strategy is
   decided. The current file is not safe to "just activate".

3. Replace the router password only after the hostapd EAP-TLS path has a
   complete test and deployment plan.

4. Move service node-name gates out of CriomOS:

   - tailscale membership
   - headscale server node
   - extra LLM/API firewall ports

5. Audit `CriomOS-lib` constants and split them into:

   - implementation path/protocol constants
   - Horizon cluster policy

6. Fix the WireGuard proxy helper as a separate low-risk bug.
