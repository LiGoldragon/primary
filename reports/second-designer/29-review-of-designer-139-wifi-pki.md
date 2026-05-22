# Report 29 - Review of designer/139 Wi-Fi PKI migration

Date: 2026-05-12
Role: designer-assistant

## Scope

This reviews, researches, and critiques
`reports/designer/139-wifi-pki-migration-designer-response.md`.

The review treats designer/139 as a design report, not an
implementation. I did not edit designer-owned reports or system-owned
repos. Some related implementation work is currently in flight in
`horizon-rs`, `CriomOS`, and `goldragon`; I read it as current context
only.

## Bottom line

Designer/139 is directionally right. The major architectural choices
hold:

- CriomOS must stay network-neutral.
- Wi-Fi policy belongs in Horizon, not in Nix literals.
- ClaviFaber should stay a narrow key/certificate tool.
- A separate cluster-trust runtime should distribute public trust
  material.
- Reusing SSH host keys for Wi-Fi authentication is the wrong identity
  coupling.
- NetworkManager profiles need server-domain pinning and a non-leaking
  outer identity.
- The node-name gates for tailnet/headscale service roles should move
  into Horizon service-role data.

The report is not yet safe as an implementation spec for the EAP-TLS
spine. It needs an addendum before operators implement the Wi-Fi PKI
path, because several details decide whether the deployment is merely
typed or actually secure.

The most important missing decisions are:

1. what public-material record the cluster-trust runtime actually
   ingests and distributes;
2. what signature algorithm signs the Wi-Fi CA and leaf certificates;
3. how `KnownClusterNodes` is enforced beyond "the cert chains to this
   CA";
4. how certificate expiry/revocation is represented and witnessed;
5. how Horizon handles migration-window expiry without using ambient
   wall-clock time inside a pure projection.

## Research confirmations

The external standards and tool docs support the report's broad
security instincts.

RFC 5216 says EAP-TLS peer/server identities come from certificate
subject or subjectAltName, prefers dNSName for host/server identities,
and says implementations should check Extended Key Usage for serverAuth
and clientAuth. It also requires CRL support for revocation. That
supports designer/139's insistence on SAN/EKU tests, but it also means
the report should not stop there.

RFC 9190 updates EAP-TLS for TLS 1.3. It strengthens privacy and says
anonymous NAIs are required for implementations supporting TLS 1.3, and
it makes revocation checking stronger. That supports a constant outer
identity, but it also makes revocation a first-class design issue.

NetworkManager's 802.1X settings expose `domain-match`,
`domain-suffix-match`, `anonymous-identity`, `client-cert`, and
`private-key`. The keyfile plugin stores connection profiles in
`/etc/NetworkManager/system-connections/`, ignores files with unsafe
permissions, and has readable path syntax for certificate paths. This
supports designer/139's `domain-suffix-match` point and current
CriomOS's "write a keyfile and chmod 0600" surface.

hostapd's sample configuration confirms the integrated EAP server uses
`eap_server`, `eap_user_file`, `ca_cert`, `server_cert`, and
`private_key`. The hostapd example user database allows `*` as a
wildcard for EAP-TLS, but says first matching entry wins. That makes
`* TLS` a valid minimal shape, not necessarily a sufficient
authorization policy.

hostapd's sample configuration still marks `ENABLE-TLSv1.3` as
experimental and disabled by default. That makes designer/139's caution
around Ed25519 reasonable, but the report needs to go further: leaf key
algorithm and certificate signature algorithm are separate decisions.

## Current implementation context

Some of designer/139's non-Wi-Fi recommendations are already being
worked on.

In `horizon-rs`, `NodeServices` is in flight as a grouped record with:

- `tailnet: Option<TailnetMembership>`
- `tailnet_controller: Option<TailnetControllerRole>`

In `goldragon`, `datom.nota` is being changed from trailing boolean
tailnet fields to `(NodeServices Client Server)`-shaped records.

In `CriomOS`, `tailscale.nix` and `headscale.nix` are being changed to
read `node.services.*` instead of `node.tailnetClient` /
`node.tailnetController`.

That implements the spirit of designer/139's `NodeServices` move. The
remaining missing witness is cluster-level validation: "at most one
tailnet controller server" should live in Horizon, not only in Nix
checks.

The Wi-Fi pieces are still in the old state:

- `CriomOS/modules/nixos/router/default.nix` still has SSID `criome`,
  country `PL`, WPA3-SAE mode, and the literal SAE password.
- `CriomOS/modules/nixos/network/wifi-eap.nix` still writes
  `identity=${node.name}`, has no `domain-suffix-match`, and points
  `private-key` at the complex key path.
- `CriomOS/modules/nixos/router/wifi-pki.nix` still only prepares the
  server key directory and prints stale imperative hints.
- `clavifaber/src/x509.rs` still emits BasicConstraints, KeyUsage, and
  SubjectKeyIdentifier, but not SAN or EKU.
- `clavifaber/src/request.rs` still signs client certs from an OpenSSH
  Ed25519 public key, not a dedicated Wi-Fi keypair.

## Critique

### 1. The cluster-trust runtime cannot yet do what 139 assigns to it

Designer/139 says the trust runtime distributes CA material, server
certificates, and per-host client certificates. That is the right
component boundary, but the current publication contract does not carry
that material.

Current `clavifaber::PublicKeyPublication` carries:

- node name;
- OpenSSH public key;
- optional Yggdrasil projection;
- optional Wi-Fi client certificate PEM.

It does not carry a Wi-Fi CA certificate, a Wi-Fi server certificate, a
certificate purpose, an authority name, a fingerprint record, a
certificate serial, a revocation state, or a "this publication supersedes
that certificate" relation.

So designer/139 is currently relying on a runtime data path that does
not exist. Before implementation, define a real public-material contract,
probably a sibling to the current publication shape:

- `CertificateAuthorityPublication`
- `WifiServerCertificatePublication`
- `WifiClientCertificatePublication`
- `CertificateFingerprint`
- `CertificateSerial`
- `CertificatePurpose`
- `CertificateRevocationObservation` or a short-lived-cert policy

The key point: Horizon may carry only fingerprint and nominal identity,
but something typed must carry the actual public certificate material
from ClaviFaber to the trust runtime and from the trust runtime to
CriomOS.

### 2. Fingerprint-only Horizon needs a verification witness

I agree that Horizon should not embed PEM. But designer/139 should add
the activation witness:

> CriomOS verifies that the runtime-delivered CA certificate hashes to
> the Horizon-declared fingerprint before it renders or starts hostapd /
> NetworkManager.

Without that check, the fingerprint is ornamental. The trust runtime
could accidentally distribute the wrong public certificate and CriomOS
would still use it.

### 3. ECDSA-P256 leaf keys do not solve the Ed25519 chain issue

Designer/139 says the dedicated Wi-Fi keypair should default to
ECDSA-P256, with Ed25519 only after an interop test. That is good for
the leaf keypair, but incomplete.

Current ClaviFaber signs certificates with `ED25519_OID` using the GPG
Ed25519 keygrip path. That means even if the Wi-Fi client and server
leaf keys are P-256, the certificate signatures can still be Ed25519.
Many EAP-TLS interoperability problems live in exactly that layer: can
the supplicant validate this signature algorithm in this EAP/TLS path?

So the real algorithm decision has two axes:

- leaf key algorithm: P-256 is the right default;
- issuing CA signature algorithm: also needs a conservative Wi-Fi-safe
  default, or an interop witness if it remains Ed25519.

If the Wi-Fi CA remains GPG-Ed25519, designer/139's P-256 leaf default
does not remove the Ed25519 deployment risk. A safe implementation needs
either a Wi-Fi-specific ECDSA CA or a passing integration test against
the actual NixOS NetworkManager/wpa_supplicant and hostapd builds.

### 4. `KnownClusterNodes -> * TLS` is too loose as stated

Designer/139 says that for `ClientAuthorization::KnownClusterNodes`,
hostapd's `eap_user_file` can be:

```text
* TLS
```

That is valid hostapd syntax, but it is not the same as "known cluster
nodes are authorized." It means "the phase-one identity may be anything;
continue with EAP-TLS." The real authorization then depends on what
hostapd validates from the client certificate chain and what the CA is
allowed to sign.

This can be acceptable only if one of these is true:

- the Wi-Fi CA signs only currently-authorized Wi-Fi client
  certificates, and those certificates are short-lived enough that
  removal is acceptable without revocation;
- hostapd is given a CRL and configured to check it;
- generated `eap_user_file` entries enumerate the actual allowed
  identities, such as `"node@realm" TLS`, and the cert profile makes
  those identities authoritative;
- a future RADIUS component owns richer authorization.

Designer/139 should not phrase cert presence as authorization unless it
also defines the lifecycle of authorization removal. "Known cluster
nodes" is not only an issuance policy. It is also a revocation or expiry
policy.

### 5. Revocation is missing from the migration spine

RFC 5216 requires CRL support, and RFC 9190 strengthens revocation
requirements for EAP-TLS 1.3. hostapd also has a `check_crl` surface,
with the operational caveat that CRLs must be available locally.

Designer/139 mentions certificate profiles but not revocation. That is a
real omission. At minimum the Wi-Fi PKI design needs one of:

- short-lived Wi-Fi client certificates with an explicit maximum
  lifetime and no revocation path for phase one;
- a `WifiCertificateRevocationList` artifact distributed by the
  cluster-trust runtime and consumed by hostapd;
- an explicit decision that revocation waits for a RADIUS/auth daemon,
  with phase-one certificate lifetime shortened accordingly.

Without this, a removed or compromised node remains authorized until its
certificate expires.

### 6. `MigrationWindow { until: TimestampNanos }` must not use ambient time

Designer/139 says the migration fallback expires by a projection-time
check. That is correct as a constraint, but dangerous if implemented by
calling the current wall clock inside `horizon-rs`.

Horizon is a pure projection library. Its own design says it does not
read environment or filesystem state. If it also reads ambient time,
the same `datom.nota` can project differently on different days without
an explicit input.

The fix is simple: keep the expiry typed, but pass the evaluation
instant explicitly through the deploy path, or make `lojix-cli` perform
the expiry validation before invoking Horizon. The important rule is
that time is data, not ambient context.

### 7. The recursive authentication enum is too permissive

This proposed shape:

```rust
pub enum WifiAuthentication {
    EapTls(EapTlsConfiguration),
    Wpa3Sae(Wpa3SaeConfiguration),
    MigrationWindow {
        primary: Box<WifiAuthentication>,
        fallback: Box<WifiAuthentication>,
        until: TimestampNanos,
    },
}
```

permits nested migration windows and self-similar policy trees. The
actual domain wants a smaller closure:

```rust
pub enum WifiAuthentication {
    EapTls(EapTlsConfiguration),
    Wpa3Sae(Wpa3SaeConfiguration),
    MigrationWindow(WifiMigrationWindow),
}

pub struct WifiMigrationWindow {
    pub primary: StableWifiAuthentication,
    pub fallback: LegacyWifiAuthentication,
    pub until: TimestampNanos,
}

pub enum StableWifiAuthentication {
    EapTls(EapTlsConfiguration),
}

pub enum LegacyWifiAuthentication {
    Wpa3Sae(Wpa3SaeConfiguration),
}
```

That closes the shape around the actual migration. If another migration
appears later, add the named variant then.

### 8. `NodeProposal.wifi` plus `router_interfaces` still leaves invalid states

Designer/139 chooses `NodeProposal.wifi: Option<WifiNetwork>` and
validates it against `router_interfaces`. This is workable, but the type
still permits impossible combinations:

- router interfaces with no router configuration;
- Wi-Fi policy on a non-router;
- router with interfaces but no explicit network policy;
- a multi-AP future crammed into one optional field.

A stronger shape would be:

```rust
pub struct NodeProposal {
    pub router: Option<RouterConfiguration>,
    // ...
}

pub struct RouterConfiguration {
    pub interfaces: RouterInterfaces,
    pub wifi: Option<WifiNetwork>,
}
```

That makes router-owned Wi-Fi policy structurally adjacent to the router
interfaces. The current `RouterInterfaces` field exists already, so a
two-step migration may be reasonable; but designer/139 should name this
as a conscious debt if it keeps separate fields.

### 9. LiveISO password handling is more than a one-line hash change

Designer/139 says the root password can become `initialHashedPassword`
or be unset. The unset/setup-on-boot route is clean. A hashed password
inside Nix is still a reusable credential-like artifact: better than a
plain literal, but not automatically acceptable for a signed/distributed
installer image.

The durable decision should be:

- local disposable ISO: documented local override is acceptable;
- signed/distributed ISO: no default root password, or one-time
  enrollment on first boot.

Do not treat a hash in the store as equivalent to no credential.

### 10. The report should separate implementation product names from roles

Designer/139 is good on the main rule: Horizon should name roles, not
products. The current in-flight `TailnetMembership` /
`TailnetControllerRole` move follows that better than fields named
`tailscale` and `headscale`.

The remaining check is to make sure CriomOS keeps product names local to
rendering modules. Horizon should say tailnet member/controller; CriomOS
currently renders that with Tailscale/Headscale.

## Best path forward

1. Keep designer/139 as the guiding report, but write an addendum before
   implementing the Wi-Fi spine. The addendum should cover public trust
   records, CA/leaf algorithms, revocation/expiry, and the exact
   authorization meaning of `KnownClusterNodes`.

2. Land the current `NodeServices` migration separately. It is good and
   low-risk. Add Horizon validation for at most one tailnet controller
   server before calling that piece complete.

3. Do not implement EAP-TLS hostapd wiring until the ClaviFaber
   certificate profile is fixed and witnessed. Required tests:
   server SAN dNSName, serverAuth EKU, client identity SAN, clientAuth
   EKU, CA key usage, certificate signature algorithm, and validity
   lifetime.

4. Decide whether the Wi-Fi CA may remain Ed25519-signed. If yes, the
   acceptance test must launch the actual NixOS hostapd plus
   NetworkManager/wpa_supplicant path and authenticate with the emitted
   certificates. If no, add a Wi-Fi-specific ECDSA CA path.

5. Define the cluster-trust publication contract before distributing
   PEMs. Horizon carries the fingerprint; the trust runtime carries the
   public certificate material; CriomOS verifies the fingerprint before
   using the delivered file.

6. Replace the recursive `MigrationWindow` with a non-recursive typed
   migration record, and make expiry validation consume an explicit time
   input from the deploy path.

7. When CriomOS renders NetworkManager, require a constant outer
   identity and server-domain pinning. When CriomOS renders hostapd,
   generate `eap_user_file` from the typed authorization policy and
   define the revocation or short-lifetime strategy at the same time.

## External sources used

- RFC 5216, EAP-TLS identities, certificate validation, EKU, and
  revocation:
  https://www.rfc-editor.org/rfc/rfc5216.html
- RFC 9190, EAP-TLS 1.3 privacy, anonymous NAI, and revocation updates:
  https://www.rfc-editor.org/rfc/rfc9190
- NetworkManager 802.1X settings:
  https://networkmanager.pages.freedesktop.org/NetworkManager/NetworkManager/settings-802-1x.html
- NetworkManager keyfile settings:
  https://networkmanager.pages.freedesktop.org/NetworkManager/NetworkManager/nm-settings-keyfile.html
- hostapd sample configuration:
  https://sources.debian.org/src/wpa/2%3A2.10-25/hostapd/hostapd.conf
- hostapd EAP user database example:
  https://chromium.googlesource.com/external/w1.fi/cgit/hostap/+/refs/tags/hostap_2_1/hostapd/hostapd.eap_user

## Local files read

- `reports/designer/139-wifi-pki-migration-designer-response.md`
- `reports/system-specialist/117-system-data-purity-and-wifi-pki.md`
- `reports/designer/110-cluster-trust-runtime-placement.md`
- `CriomOS/AGENTS.md`, `CriomOS/ARCHITECTURE.md`, `CriomOS/skills.md`
- `horizon-rs/AGENTS.md`, `horizon-rs/ARCHITECTURE.md`,
  `horizon-rs/skills.md`, `horizon-rs/docs/DESIGN.md`
- `clavifaber/ARCHITECTURE.md`, `clavifaber/skills.md`
- `CriomOS/modules/nixos/router/default.nix`
- `CriomOS/modules/nixos/router/wifi-pki.nix`
- `CriomOS/modules/nixos/network/wifi-eap.nix`
- `CriomOS/modules/nixos/network/tailscale.nix`
- `CriomOS/modules/nixos/network/headscale.nix`
- `CriomOS/modules/nixos/network/wireguard.nix`
- `CriomOS/modules/nixos/disks/liveiso.nix`
- `horizon-rs/lib/src/proposal.rs`
- `horizon-rs/lib/src/node.rs`
- `goldragon/datom.nota`
- `clavifaber/src/publication.rs`
- `clavifaber/src/request.rs`
- `clavifaber/src/x509.rs`
