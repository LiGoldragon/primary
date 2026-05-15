# Horizon Data Needed To Purge CriomOS Literals

Role: system-specialist
Date: 2026-05-13

## Summary

No, the hardwired data is not all out of CriomOS and CriomOS-home.
The previous node-name predicates are gone from active modules: I found
no remaining `node.name == ...` or `elem node.name ...` gates in
`CriomOS/modules` or `CriomOS-home/modules`. That part of the rule is
mostly fixed.

The remaining violations are a different shape: cluster and user policy
still live as literals in Nix modules, in `CriomOS-lib`, and in Horizon
itself. The big remaining items are Wi-Fi policy and password, LAN/DNS
policy, hardcoded domain suffixes, VPN selection/secrets, user tool secret
paths, and the local AI provider endpoint. These should not be moved to
another constants file. The fix is to add typed records to Horizon, then
make CriomOS and CriomOS-home render those records.

The permanent destination of this report's substance is:

- `horizon-rs`: schema, projection, validation, and tests.
- `goldragon/datom.nota`: production Horizon data once the schema exists.
- `CriomOS` and `CriomOS-home`: rendering modules only, with source
  constraints that reject production literals.
- `CriomOS-test-cluster`: synthetic fixtures proving alternate cluster
  names, domains, networks, DNS providers, and user secret references work.

## Boundary

CriomOS and CriomOS-home should consume these inputs:

- projected `horizon` facts;
- implementation constants such as file materialization paths;
- public package/model inputs pinned by Nix.

They should not define these facts:

- production node names as control flow;
- SSIDs, Wi-Fi countries, passwords, certificate policy;
- cluster/internal/public domain suffixes;
- LAN subnets, gateway, DHCP pools, upstream DNS policy;
- selected VPN provider regions/servers/accounts;
- user secret store paths such as `openai/api-key`;
- local service provider endpoints discovered by scanning cluster nodes.

Private key material and secret values should not be in Horizon either.
Horizon should carry secret references, certificate fingerprints, public
certificates, roles, and policy. Secret values remain in the secret
backend or runtime credential system.

## Current Horizon Gaps

Current `horizon-rs` `ClusterProposal` is still small:
`horizon-rs/lib/src/proposal.rs:24` through `:32` has nodes, users,
domains, and trust only. Current node proposal data has booleans for
`nordvpn` and `wifi_cert` at `horizon-rs/lib/src/proposal.rs:50` through
`:56`, and `RouterInterfaces` carries only one WLAN interface plus band,
channel, and standard at `horizon-rs/lib/src/proposal.rs:127` through
`:135`.

That is not enough to remove the remaining literals. The new Horizon data
should be added as typed records at the tail of the positional Nota
records, with `serde(default)` on every new proposal field.

### 1. Cluster Identity And Domains

Current hardwire:

- `horizon-rs/lib/src/name.rs:75` through `:83` derives
  `<node>.<cluster>.criome`.
- `horizon-rs/lib/src/user.rs:92` through `:93` derives email and Matrix
  IDs under `<cluster>.criome.net`.
- `goldragon/datom.nota:237` through `:238` has an empty domains map, so
  domain policy is still implicit.

Needed Horizon shape:

- `ClusterIdentity` or `ClusterDomains`
- internal node zone, for example today's `.criome` equivalent;
- public user/service zone, for example today's `.criome.net` equivalent;
- service DNS labels or aliases, such as `nix` and `wg`, if these are
  cluster conventions rather than hard protocol constants;
- optional tailnet DNS zone if not carried by the tailnet service record.

Resulting code change:

- replace `CriomeDomainName::for_node(node, cluster)` with projection from
  declared domain policy;
- eventually rename output fields away from `criomeDomainName` once the
  compatibility cost is acceptable.

### 2. LAN And DHCP Policy

Current hardwire:

- `CriomOS-lib/lib/default.nix:83` through `:87` defines
  `10.18.0.0/24`, `10.18.0.1`, and `10.18.0`.
- `CriomOS/modules/nixos/router/default.nix:113` through `:129` hardcodes
  DHCP lease timers and pool `.100 - .240`.
- `CriomOS/modules/nixos/router/default.nix:153` through `:189` uses
  bridge naming and USB Ethernet auto-bridge policy.
- `CriomOS/modules/nixos/network/networkd.nix:11` and `:36` through
  `:43` hardcode a hotplug subnet and DHCP server shape for USB Ethernet
  on center nodes.

Needed Horizon shape:

- `LanNetwork { cidr, gateway, bridgeInterface, dhcpPool, leasePolicy }`
- `AccessPortPolicy` or `RouterLanPort` for USB Ethernet bridge behavior;
- optional `HotplugNetwork` for center-node USB DHCP behavior.

Open question:

If `br-lan` is a CriomOS implementation convention, it can stay as a
constant. If another cluster should be able to choose it, it belongs in
Horizon with the LAN record.

### 3. Resolver And DNS Policy

Current hardwire:

- `CriomOS/modules/nixos/network/default.nix:75` through `:80` sets
  resolver fallbacks to loopback, Cloudflare, and Quad9.
- `CriomOS/modules/nixos/network/resolver.nix:23` through `:24` has the
  same Cloudflare/Quad9 defaults for systemd-resolved.
- `CriomOS/modules/nixos/network/dnsmasq.nix:34` through `:43` hardcodes
  Cloudflare and Quad9 IPv4/IPv6 upstreams.
- `CriomOS/modules/nixos/network/dnsmasq.nix:119` through `:123`
  hardcodes Tailscale's `100.100.100.100` MagicDNS server address.
- `CriomOS/modules/nixos/network/networkd.nix:52` through `:58` repeats
  Cloudflare/Quad9 fallbacks.

Needed Horizon shape:

- `ResolverPolicy { upstreamServers, fallbackServers, localListenAddresses }`
- `TailnetDnsPolicy { baseDomain, dnsServerAddress }` or add
  `dnsServerAddress` to `TailnetControllerRole::Server`.

Resulting code change:

- dnsmasq, resolved, and networkd render resolvers from Horizon;
- no resolver module should know Cloudflare, Quad9, or the MagicDNS
  service address unless Horizon declares them.

### 4. Wi-Fi Policy And PKI

Current hardwire:

- `CriomOS/modules/nixos/router/default.nix:88` through `:99` hardcodes
  regulatory country, SSID, WPA3-SAE mode, and a literal SAE password.
- `CriomOS/modules/nixos/network/wifi-eap.nix:20`, `:26`, and `:75`
  hardcode the `criome` NetworkManager connection ID, SSID, and file
  name.
- `CriomOS/modules/nixos/router/wifi-pki.nix:18` through `:39` only
  prepares a directory and prints imperative ClaviFaber hints; hostapd is
  not wired for EAP-TLS.

Needed Horizon shape:

- `WifiNetwork { id, ssid, country, authentication }`
- `WifiAuthentication` sum:
  - `Wpa3Sae { password: SecretReference }`
  - `EapTls { ca, serverIdentity, clientProfile, authorization }`
- `RouterRadio { interface, band, channel, standard, network, bridge }`
  as a list, not a single `wlan`.
- `WifiClientProfile { network, identity, outerIdentity, caFingerprint,
  domainSuffixMatch, clientCertificate }`
- `CertificateAuthority` and `CertificateProfile` records for the public
  CA certificate/fingerprint, SAN/EKU/key-usage policy, validity, and
  revocation or replacement strategy.

Migration note:

The existing password-based Wi-Fi can stay only as explicitly marked
transition debt during the dual-radio migration: old WPA3-SAE network on
one radio, new EAP-TLS network on the USB radio, clients migrate, then the
old network is deleted. Do not move the literal password into Horizon as a
value; use a `SecretReference` if the old network must be represented
during the transition.

### 5. Tailnet Controller Trust

Current state:

- Tailnet role data is now mostly in Horizon:
  `horizon-rs/lib/src/proposal.rs:101` through `:124`.
- `goldragon/datom.nota:83` declares `(NodeServices Client (Server 8443
  "tailnet.goldragon.criome"))`.

Remaining hardwire/scaffold:

- `CriomOS/modules/nixos/network/headscale.nix:22` through `:24` chooses
  TLS materialization paths.
- `CriomOS/modules/nixos/network/headscale.nix:26` through `:63` creates
  a first-boot self-signed certificate.

Needed Horizon shape:

- add `dnsServerAddress` and TLS/certificate policy to
  `TailnetControllerRole::Server`, or reference a shared
  `ServiceCertificate` record;
- Horizon should carry trusted CA fingerprint/public certificate data,
  not the private key;
- ClaviFaber or the cluster-trust runtime should publish/distribute the
  service certificate material.

### 6. VPN Profiles

Current hardwire:

- `CriomOS/modules/nixos/network/nordvpn.nix:19` through `:24` reads a
  committed NordVPN server lock file and DNS/client values.
- `CriomOS/data/config/nordvpn/update-servers:18` through `:26` chooses
  specific countries/regions.
- `CriomOS/modules/nixos/network/nordvpn.nix:35` through `:60` renders
  NetworkManager connection names and interface names from that lock.
- `CriomOS-home/modules/home/profiles/min/default.nix:240` through
  `:267` hardcodes the NordVPN gopass path, private-key destination, and
  API endpoint in a user wrapper.
- `CriomOS/modules/nixos/network/wireguard.nix:40`, `:47`, and `:65`
  hardcode the `wg.` alias, private key path, and `51820` listen port.

Needed Horizon shape:

- `VpnProfile` sum with variants such as `Nordvpn` and `WireguardMesh`;
- selected exits/regions/server lock reference as data;
- account/token `SecretReference`;
- private key `SecretReference` or materialization profile;
- endpoint and listen port policy if not protocol constants;
- routing/exemption policy for overlays.

Open question:

The NordVPN server lock may be better as a separate public provider-data
input referenced by Horizon, not embedded directly in Horizon. The choice
of countries and account secret still belongs outside CriomOS code.

### 7. Nix Cache And Build Capabilities

Current hardwire/capability smell:

- `CriomOS/modules/nixos/nix/cache.nix:30` through `:35` treats
  `isNixCache` as a boolean but the "yes" carries endpoint, port,
  signing-key path, and retention policy.
- `CriomOS/modules/nixos/nix/builder.nix:35` through `:48` renders a
  builder config from projected booleans and derived data, with protocol
  and speed factor in the module.
- `horizon-rs/lib/src/node.rs:71` through `:84` exposes many derived
  booleans: `is_nix_cache`, `is_remote_nix_builder`, `is_dispatcher`,
  `has_nordvpn_pub_key`, `has_wifi_cert_pub_key`.

Needed Horizon shape:

- `NodeCapabilities`
- `BinaryCache { endpoint, publicKey, signingKey: SecretReference,
  retentionPolicy }`
- `BuildHost { maxJobs, coresPerJob, systems, trust }`
- `BuildDispatcher { policy }`

This is the same typed-records-over-flags problem as Wi-Fi: a boolean is
too small once the consumer needs data.

### 8. Local AI Provider

Current hardwire:

- `CriomOS/modules/nixos/llm.nix:23` through `:31` reads public model
  inventory and server port from `CriomOS-lib/data/largeAI/llm.json`.
- `CriomOS/modules/nixos/llm.nix:113` through `:123` starts llama.cpp
  from that inventory.
- `CriomOS-home/modules/home/profiles/min/pi-models.nix:19` through
  `:27` scans cluster nodes looking for `largeAiRouter` or `largeAi`.
- `CriomOS-home/modules/home/profiles/min/pi-models.nix:39` through
  `:44` hardcodes provider name and derives a base URL with fallback
  port `11434`.

Needed Horizon shape:

- `AiProvider` or `LlmService` record:
  - provider name;
  - serving node or endpoint;
  - protocol, for example OpenAI-compatible completions;
  - port/base URL;
  - optional API-key secret reference;
  - enabled model IDs or model inventory reference.

What can stay in Nix:

The public open-model catalog and fetch hashes can stay in
`CriomOS-lib`/Nix. The cluster decision that "this node serves these
models on this endpoint and Home should configure this provider" belongs
in Horizon.

### 9. User Tool Secret References

Current hardwire in CriomOS-home:

- OpenAI transcription key:
  `CriomOS-home/modules/home/profiles/min/dictation.nix:22`.
- Dictation backend/model/vocabulary:
  `CriomOS-home/modules/home/profiles/min/dictation.nix:63` through
  `:85`.
- GitHub CLI and hub token paths:
  `CriomOS-home/modules/home/profiles/med/default.nix:17` through `:34`.
- NordVPN account token:
  `CriomOS-home/modules/home/profiles/min/default.nix:240` through
  `:267`.
- Linkup API key:
  `CriomOS-home/packages/pi/default.nix:62` through `:65`.
- Anna's Archive secret key and default service URL:
  `CriomOS-home/modules/home/profiles/med/cli-tools.nix:14` through `:45`.

Needed Horizon shape:

- `SecretReference { backend, path, purpose }`, or a more abstract
  `UserSecretReference { name, purpose }` plus a user/host-local secret
  backend mapping;
- `DictationProfile { backend, model, language, vocabulary, apiKey }`;
- `ToolCredentialProfile` for GitHub, Linkup, Anna's Archive, NordVPN,
  and similar per-user services.

Open boundary question:

If the cluster Horizon should stay free of user-private tool preferences,
then add a user Horizon/profile layer rather than putting every personal
tool secret reference in the cluster proposal. Either way, these paths
should stop living in CriomOS-home modules.

## What Should Not Move Into Horizon

Do not put secret values or private keys in Horizon.

These can remain in code or implementation constants:

- Nix package versions and public source pins.
- Public open-model fetch URLs and hashes.
- File materialization paths such as `/etc/criomOS/wifi-pki/...`, if they
  are CriomOS implementation choices.
- Protocol constants that truly do not vary by cluster.
- Test fixture names, as long as architecture tests also include
  synthetic non-Goldragon names/domains.

The dangerous pattern is not "a string exists in code." The dangerous
pattern is "a production cluster or user decision exists in code."

## Constraint Tests To Add

These tests should land before or with the migration:

- `horizon-rs`: project a cluster with non-`.criome` internal and public
  domains; assert node FQDNs, Nix cache domains, email, and Matrix IDs
  use the declared domains.
- `horizon-rs`: parse and project Wi-Fi records, resolver policy, VPN
  profiles, AI provider records, and secret references from Nota.
- `CriomOS-test-cluster`: synthetic router with two Wi-Fi radios; assert
  old WPA3-SAE transitional network and new EAP-TLS network render from
  Horizon data.
- `CriomOS-test-cluster`: synthetic DNS policy with non-Cloudflare
  upstreams; assert dnsmasq, resolved, and networkd render those values.
- `CriomOS-test-cluster`: synthetic local AI provider endpoint; assert
  CriomOS-home config uses the provider record, not a cluster-node scan.
- Source constraints over `CriomOS/modules` and `CriomOS-home/modules`
  forbidding production literals such as Goldragon node names, production
  SSIDs, production secret-store paths, `.criome` derivations, and fixed
  public DNS providers outside tests/docs.

The source scan must run over repository paths, never over `/nix/store`.

## Recommended Order

1. Add `ClusterIdentity`/domain policy to Horizon and make projection stop
   deriving `.criome` and `.criome.net`.
2. Add `SecretReference` and decide whether user secret references live in
   cluster Horizon or a user-profile Horizon layer.
3. Add resolver and LAN policy records; render dnsmasq, resolved,
   networkd, DHCP, and bridge policy from them.
4. Add Wi-Fi policy records with dual-radio support; represent the
   temporary WPA3-SAE network as transition debt and the new EAP-TLS
   network as the target.
5. Add AI provider records so CriomOS-home does not discover providers by
   scanning node roles.
6. Add VPN profile records or a Horizon reference to external provider
   data.
7. Replace remaining capability booleans with typed records where the
   "true" case carries data.
8. Add source-constraint tests and remove the old literals from
   CriomOS/CriomOS-home.

## Current Answer

The hardcoded node-name gates are gone from the active system modules I
checked. The hardwired cluster and user policy is not gone. To remove it
properly, Horizon needs typed records for domains, networks, Wi-Fi,
resolver policy, service trust, VPN, AI providers, and secret references.
Once those records exist and are projected, CriomOS and CriomOS-home can
be reduced to pure renderers, and the source constraints can make the old
pattern hard to reintroduce.

## Refactor Status, 2026-05-15

Schema work landed on the `horizon-re-engineering` branch in each
relevant repo (horizon-rs, goldragon, CriomOS, CriomOS-lib,
CriomOS-home, CriomOS-test-cluster). End-to-end verification for
each step is `nix flake check` on CriomOS-test-cluster against the
fieldlab fixture (cluster-contracts, full-module-contracts,
projections-match-fieldlab, multiple-tailnet-controllers-rejected,
source-constraints — all green at the latest tip).

Done on the refactor branch:

- Step 1 — `proposal::*` / `view::*` namespace split.
- Step 4 — `cluster.lan` (LanNetwork: cidr/gateway/dhcpPool/leasePolicy)
  + `cluster.resolver` (ResolverPolicy: upstreams/fallbacks/listens).
  CriomOS network/default.nix, dnsmasq.nix, resolver.nix consume.
- Step 6 — `cluster.aiProviders` (typed AiProvider with models, sources
  as a NotaSum of AiModelFetchurl/AiModelMultiShard, per-model serving,
  per-provider serving config). `CriomOS-lib/data/largeAI/llm.json`
  deleted. CriomOS llm.nix + CriomOS-home pi-models.nix consume.
- Step 6b — per-node operating envelope on AiServingConfig
  (gpu_override, memory_max_gb, memory_high_gb). RDNA3
  HSA_OVERRIDE_GFX_VERSION + memory caps gone from llm.nix.
- Step 7a — collapse `is_nix_cache + nix_cache_domain + nix_url` into
  `Option<NixCache>` on view::Node. Same yggdrasil-style sub-record
  collapse as step 14.
- Step 7b — drop six shadow `has_*_pub_key` fields (has_nix, has_ygg,
  has_wireguard, has_nordvpn, has_wifi_cert, has_base). Consumers
  derive locally from the underlying typed field.
- Step 8 — `cluster.vpnProfiles` (VpnProfile NotaSum with NordvpnProfile
  variant carrying VpnDns / VpnClient / NordvpnServer list /
  credentials SecretReference). `CriomOS/data/config/nordvpn/*` deleted.
  CriomOS nordvpn.nix consumes.
- Step 11 — `cluster.tailnet` (TailnetConfig: baseDomain + optional
  TlsTrustPolicy). TailnetControllerRole::Server collapsed to
  port-only.
- Step 14 — yggdrasil sibling fields (`ygg_pub_key`, `ygg_address`,
  `ygg_subnet`) collapsed into `Option<YggPubKeyEntry>`. SSH-pubkey
  always-true field deleted.

Open on the refactor branch:

- Step 3 — `criomeDomainName` rename / cluster-domain policy.
- Step 5 — Wi-Fi typed records (WifiNetwork with WifiAuthentication
  sum: Wpa3Sae / EapTls). The CriomOS literal SAE password is now
  out of source via the production sops integration (see report 121),
  but it's not yet behind a typed Horizon record on the refactor
  side. Migration here is one of two paths: (a) add WifiNetwork to
  Cluster + author SecretReference for the password; (b) keep the
  password as a SecretReference on `RouterInterfaces` (already
  shaped that way in production main, see report 121) and add SSID
  / country / regulatory policy as additional Cluster fields.
- Step 9 — NodePlacement (typed location per node).
- Step 10 — Machine data-bearing variants (no ZST machine variants).
- Step 12 — ProjectedNodeView typed shape.
- Step 13 — Ghost-as-Publication.
- Step 15 — source-constraint tests for the refactor's invariants.

Two consumer modules in the refactor branch carry loud-fail throws
where SecretReference resolution is needed:

- `horizon-re-engineering` CriomOS llm.nix — when `AiProvider.api_key`
  is `Some(ref)`. Today's local providers have `api_key = None` so
  the throw doesn't fire on goldragon.
- `horizon-re-engineering` CriomOS nordvpn.nix — when a node opts
  into nordvpn (`node.nordvpn = true`) and the cluster has a
  `NordvpnProfile`. Today's fieldlab fixture has empty `vpn_profiles`
  so the throw doesn't fire on the fieldlab test path.

Both throws were a stub against the unproven secret backend. **The
backend is now proven on production main** (report 121, phase 2).
The refactor's consumer modules can adopt the same pattern that
production router/default.nix uses today: pull
`inputs.secrets.sopsFiles.<name>` into the consumer module, declare
`sops.secrets.<name> = { sopsFile = ...; mode = "0400"; restartUnits
= [ ... ]; }`, and pass `config.sops.secrets.<name>.path` to the
service that consumes it. The lojix-cli artifact-staging code already
generalises: `src/artifact.rs:21` synthesises `sopsFiles = { ... }`
from any sops files present in `<cluster-repo>/secrets/`. Adding new
named secrets needs no infrastructure changes — author the encrypted
file beside `router-wifi-sae-passwords.sops`, declare the
SecretReference in datom, and consume it in the relevant CriomOS
module.

Pre-existing kea-dhcp4-server stale-socket bug (also discovered
during this arc) — see report 121 §"Side Note: Pre-existing kea
Bug Found". Independent of the schema work; worth folding into the
step-7 / NodeCapabilities work or treating as standalone follow-up.
