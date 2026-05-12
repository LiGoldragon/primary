# CriomOS State And Sandbox Audit

Role: system-specialist
Date: 2026-05-12

## Summary

CriomOS moved materially closer to the intended architecture this week:
service decisions are now mostly role/capability data from Horizon rather
than node-name predicates, router DNS moved from Unbound to dnsmasq, edge
resolvers moved to systemd-resolved, ClaviFaber stopped pretending to own
the SSH host key, and a new independent `CriomOS-test-cluster` repository
now exercises synthetic Horizon fixtures against real CriomOS modules.

The biggest remaining architectural violation is still Wi-Fi. The router
module contains a production SSID, regulatory country, WPA3-SAE mode, and
literal SAE password. The client EAP module points at stale key material
that ClaviFaber no longer creates. The router PKI module prepares a
directory and prints imperative hints, but hostapd is still not wired for
EAP-TLS. That means the Wi-Fi PKI work is designed in outline but not yet
deployable.

The strongest new testing shape is the synthetic cluster. It proves
Horizon projection, tailnet role validation, aggregate CriomOS module
evaluation, source constraints, and one synthetic Pod toplevel build. It
also runs on Prometheus in a transient systemd user sandbox. The weak
side is that it is still not a booted network environment: it cannot prove
hostapd, NetworkManager, Wi-Fi EAP-TLS, dnsmasq service behavior, Tailscale
enrollment, or link-loss recovery.

## Evidence Read

Repositories and paths surveyed:

- `CriomOS`: `/git/github.com/LiGoldragon/CriomOS`
- `CriomOS-test-cluster`: `/git/github.com/LiGoldragon/CriomOS-test-cluster`
- `horizon-rs`: `/git/github.com/LiGoldragon/horizon-rs`
- `clavifaber`: `/git/github.com/LiGoldragon/clavifaber`
- Persona sandbox runner: `/git/github.com/LiGoldragon/persona/scripts/persona-engine-sandbox`
- Prior reports:
  - `reports/system-specialist/117-system-data-purity-and-wifi-pki.md`
  - `reports/designer/139-cluster-trust-runtime-is-persona.md`
  - `reports/designer-assistant/29-review-of-designer-139-wifi-pki.md`

Fresh checks run:

- `CriomOS-test-cluster`: `nix flake check --print-build-logs --show-trace` passed.
- `horizon-rs`: `nix flake check --print-build-logs --show-trace` passed.
- `clavifaber`: `nix flake check --print-build-logs --show-trace` passed.
- `CriomOS`: direct `nix flake check --print-build-logs --show-trace` fails because the root flake's default `system` input intentionally throws unless lojix or a fixture flake provides projected inputs.

Recent pushed commits that matter:

- `CriomOS` `bcd1e9f3`: tailnet DNS domain now derives from `node.criomeDomainName`.
- `CriomOS` `2aa6dd10`: module split by concern.
- `CriomOS` `9c179ff6`: tailnet roles read from `NodeServices`.
- `CriomOS` `4d6bb24d`: Horizon roles replace node-name gates.
- `CriomOS-test-cluster` `366a4d3f`: alternate-domain tailnet DNS contract.
- `CriomOS-test-cluster` `310e7e72`: synthetic Pod toplevel build.
- `horizon-rs` `424f5257`: containment validation rules.
- `horizon-rs` `53503486`: placement on `NodeProposal` and sum-with-data wire derives.
- `horizon-rs` `e4f165e3`: derive `Node.placement` in projection.
- `horizon-rs` `83a8338`: typed placement, capability, and `SecretReference` modules.
- `clavifaber` `adf65938`: drops SSH host-key ownership; sshd owns host keys.
- `clavifaber` `013cee21`: rootless deployment sandbox replaces nspawn.

## What Landed Well

### Horizon role data is replacing node-name control flow

The old shape was "if node name is ouranos/prometheus, enable this
service." That pattern violated the CriomOS rule that node names are
identifiers, not predicates.

Current state:

- `modules/nixos/network/tailscale.nix` enables Tailscale from
  `node.services.tailnet == "Client"`.
- `modules/nixos/network/headscale.nix` enables Headscale from
  `node.services.tailnetController == "Server"`.
- `horizon-rs` projects `NodeServices`.
- `CriomOS-test-cluster` has a negative fixture that rejects multiple
  tailnet controller servers.

This is a good pattern: semantic role in Horizon, projection-time
validation in Horizon, Nix modules only render the projected role.

### Tailnet DNS stopped hardcoding the cluster TLD

`dnsmasq.nix` and `headscale.nix` used to build
`tailnet.${cluster.name}.criome`. They now derive the cluster domain from
the projected node domain:

- `CriomOS/modules/nixos/network/dnsmasq.nix`
- `CriomOS/modules/nixos/network/headscale.nix`

The test-cluster now mutates the synthetic domain to `.fieldlab.test`
and proves both dnsmasq and Headscale render the altered base domain.

This is not yet a full Horizon custom-TLD end-to-end test. It rewrites
projected fixture data inside the Nix check. That is still valuable as a
CriomOS module contract, but the stronger future witness is:
`ClusterProposal.tld -> horizon-cli -> CriomOS module output`.

### DNS split is now proportional

The DNS stack moved toward the shape recommended in
`reports/system-specialist/115-router-dns-server-research.md`:

- edge/NetworkManager nodes use `systemd-resolved`;
- router nodes use dnsmasq for LAN DNS and cluster records;
- Unbound is no longer the default edge resolver.

This matches the actual operational failure: Unbound was too heavy for
the laptop edge resolver and could get into a running-but-dead state
after network loss.

What is still missing: a booted service test that proves dnsmasq answers
cluster names, forwards upstream, and recovers across link changes.

### ClaviFaber is cleaner than it was

ClaviFaber is now a narrower key/publication tool:

- sshd owns `/etc/ssh/ssh_host_ed25519_key`; ClaviFaber reads the public
  half into `publication.nota`.
- `YggdrasilKey` owns per-host Yggdrasil keypair generation/projection.
- `CertificateIssuer` owns certificate issuance.
- `PublicKeyPublicationWriting` assembles SSH public key, optional
  Yggdrasil projection, and optional Wi-Fi client certificate.
- Tests cover actor topology, actor trace, idempotent issuance,
  parse-before-skip, forbidden edges, publication writing, and
  certificate validity windows.

The actor-per-concern direction is visible here and is better than the
old "converge everything" surface.

### Synthetic cluster testing exists now

`CriomOS-test-cluster` is the first independent cluster fixture repo
that does the right kind of Nix-backed testing:

- `projections-match-fieldlab`: pinned fixture projections must match
  `horizon-cli`.
- `multiple-tailnet-controllers-rejected`: bad cluster role shape must
  fail.
- `cluster-contracts`: module-level contracts for tailnet, dnsmasq,
  Wi-Fi EAP profile rendering, Nix cache/builder roles, SSH known hosts,
  and alternate-domain tailnet DNS.
- `full-module-contracts`: full aggregate CriomOS module evaluation for
  synthetic `beacon` and `cedar` with home disabled.
- `source-constraints`: source scan over CriomOS Nix modules for
  production host facts, node-name predicates, and fixed cluster-domain
  fragments.
- `dune-toplevel`: synthetic Pod node toplevel build.
- `run-on-prometheus` and `build-dune-on-prometheus`: pushed-flake
  checks/builds inside a transient systemd user sandbox on Prometheus.

This is the right testing direction: architecture constraints have named
witnesses, and stateful/remote checks are exposed through flake apps.

## Specified But Not Implemented

### Wi-Fi PKI is not implemented

The desired shape from reports 117, 139, and designer-assistant/29 is:

- Horizon carries typed Wi-Fi policy: SSID, country, auth mode,
  migration window, CA fingerprint, server identity, client
  authorization, and secret references.
- ClaviFaber owns dedicated Wi-Fi keypair/certificate generation.
- Certificate profiles explicitly include SAN, EKU, key usage,
  validity, and eventually revocation or short-lived cert policy.
- A cluster-trust runtime distributes public certificate material from
  ClaviFaber publications to the hosts that need it.
- CriomOS verifies delivered CA material against Horizon's fingerprint
  before hostapd/NetworkManager consumes it.
- hostapd is rendered for EAP-TLS.
- NetworkManager clients use domain pinning and a privacy-preserving
  outer identity.

Current state:

- `router/default.nix` still hard-codes country `PL`, SSID `criome`,
  WPA3-SAE, and a literal SAE password.
- `network/wifi-eap.nix` still writes SSID `criome`, identity
  `${node.name}`, no `anonymous-identity`, no `domain-suffix-match`, and
  points `private-key` at `constants.fileSystem.complex.keyFile`.
- `complex.nix` now only writes `publication.nota` from sshd's public
  key; it does not create the complex private key that `wifi-eap.nix`
  expects.
- `router/wifi-pki.nix` only prepares a directory and prints stale manual
  instructions.
- `clavifaber` can issue certificates, but not yet the full Wi-Fi-safe
  profile and trust publication shape.

This is the main "do not deploy yet" area.

### Cluster-trust runtime is still missing

The reports converge on this boundary: Horizon carries policy and
fingerprints, ClaviFaber emits local public material, and a separate
runtime distributes that public material across the cluster.

That runtime does not exist yet. As a result, the data path for "new host
publishes its SSH public key, Yggdrasil address, Wi-Fi cert, and those
facts reach the cluster" is still conceptual.

Related open work:

- `primary-e3c`: `ClusterRegistryActor` + `TrustDistributionActor` with
  push primitive.
- `primary-nvs8`: feed Wi-Fi EAP certificates into test-cluster fixtures.
- `primary-mm0`: ClaviFaber end-to-end sandbox and Prometheus runner.

### Wi-Fi policy and secrets are not in Horizon

`horizon-rs` has:

- `NodeServices` for tailnet roles.
- placement/capability/SecretReference types in progress.
- `wifi_cert: bool`, still too small for real Wi-Fi policy.

It does not yet have a `WifiNetwork` or equivalent policy record. It
also does not yet project the router Wi-Fi policy needed to remove the
literal SSID, country, and SAE secret from CriomOS.

### New placement/capability work is not consumed by CriomOS

The system assistant's `horizon-rs` work added the right direction:
typed placement, capabilities, `SecretReference`, `NodePlacement`, and
containment validation. Fresh Horizon tests passed, including contained
host not found and nested containment rejection.

CriomOS does not yet consume the new placement/capability model. The
test-cluster still uses legacy `Machine Pod ...` shape, with placement
derived for compatibility. That is acceptable during migration, but it
means the current contained-node design is not yet exercised as a real
CriomOS deployment surface.

### VM/nspawn service smoke is still open

The Prometheus runner proves Nix evaluation/build in a transient user
service. It does not boot a VM or nspawn container and does not start
dnsmasq, hostapd, NetworkManager, Tailscale, Headscale, or systemd
services inside an isolated OS environment.

Open work `primary-58l` is still the correct next layer: add a VM or
nspawn service smoke for DNS and tailnet roles.

## Implemented But Not Implemented Well

### Direct `CriomOS` flake check is not a useful command

Plain `nix flake check` in `CriomOS` fails because the repo's root flake
has stub `system` and `horizon` inputs. This is understandable: CriomOS
is meant to be driven by projected lojix inputs.

But the testing skill says the canonical repo test should be Nix-backed
and easy to run. Today the real check has moved outside the repo into
`CriomOS-test-cluster`. That is workable, but the ergonomics are weak:
a fresh agent can run the obvious command in the main repo and get a
failure that looks like a broken suite.

Better shape:

- keep the stubbed deploy target;
- add a repo-owned fixture check that supplies synthetic `system` and
  `horizon` inputs, or document that `CriomOS-test-cluster` is the
  canonical check surface in `CriomOS/AGENTS.md` and `CriomOS/README.md`;
- ideally expose a `checks.<system>.fixture` or app that runs the
  external fixture without needing agent memory.

### Source constraints are a tripwire, not proof

`CriomOS-test-cluster/checks/source-constraints.nix` scans
`modules/nixos` through Nix APIs, not shell grep against the Nix store.
That is good.

Limits:

- it catches specific literal fragments, not semantic policy;
- it does not scan `CriomOS-home`, `CriomOS-lib`, `goldragon`, or all
  generated output;
- it can miss equivalent bad logic written in a different form;
- it can produce false positives if fixture strings enter module code.

Keep it as a cheap guard. Do not treat it as the final purity proof.

### The alternate-domain test mutates projected data

The tailnet-domain regression test rewrites `criomeDomainName` inside
the Nix check, then checks module output. That proves CriomOS consumes
the projected domain, not a fixed TLD.

It does not prove the full Horizon projection path for custom cluster
TLDs. That should be added once `CriomOS-test-cluster` authors a custom
TLD in `fieldlab.nota` and regenerates fixtures from `horizon-cli`.

### Prometheus sandbox is useful but shallow

The runner copied the Persona sandbox idea: fresh sandbox dir, isolated
HOME/XDG state, transient `systemd-run --user`, logs on failure, pushed
remote flake, and no dependence on the local checkout.

It is not as complete as Persona's sandbox:

- no credential policy layer;
- no reusable sandbox abstraction;
- no automatic artifact retention;
- no booted system boundary;
- still shares the host Nix daemon/cache/network;
- does not isolate graphical applications or network services.

This is enough for pushed-flake reproducibility. It is not enough for
Wi-Fi, service lifecycle, or desktop integration tests.

### Wi-Fi EAP module has a stale private-key assumption

`wifi-eap.nix` still assumes a private key at
`constants.fileSystem.complex.keyFile`. ClaviFaber no longer creates that
file. This means the service will skip rather than produce a working EAP
profile on hosts that set `hasWifiCertPubKey`.

The module also lacks the EAP-TLS safety pieces from designer/139 and
designer-assistant/29: `domain-suffix-match`, outer identity, dedicated
Wi-Fi keypair, and certificate-profile enforcement.

### WireGuard module still has a clear bug

`modules/nixos/network/wireguard.nix` contains:

```nix
mkUntrustedProxy = untrustedProxy: {
  inherit (wireguardUntrustedProxies) publicKey endpoint;
  allowedIPs = [ "0.0.0.0/0" ];
};
```

That inherits `publicKey` and `endpoint` from the whole
`wireguardUntrustedProxies` list instead of from the `untrustedProxy`
argument. This is likely unused right now, but it is exactly the kind of
stale network module code that should be either fixed or retired.

Open work `primary-cua` asks whether WireGuard is used at all. That
audit should happen before expanding tests around it.

### Bare-metal synthetic builds expose firmware policy debt

Trying to build a synthetic bare-metal node hit unconditional
`hardware.enableAllFirmware = true` in `modules/nixos/metal/default.nix`.
The test-cluster worked around this by building a synthetic Pod node
instead.

That workaround is reasonable for the first toplevel witness, but the
underlying issue remains: firmware policy should be gated by hardware
capability or deployment policy, not unconditional bare-metal import.
Open work: `primary-un7p`.

## Patterns Emerging

### Good pattern: role data in Horizon, rendering in CriomOS

This pattern worked for tailnet roles and should be repeated:

1. Horizon owns the semantic field.
2. Horizon validates cluster-level invariants.
3. CriomOS reads the projected field directly.
4. A fixture cluster proves the behavior.

This should be the template for Wi-Fi policy, AI-provider roles,
contained-node placement, and future service capabilities.

### Good pattern: one actor per concern

ClaviFaber's current shape is noticeably healthier:

- `YggdrasilKey` owns the Yggdrasil binary boundary.
- `CertificateIssuer` owns certificate issuance.
- `GpgAgentSession` owns gpg-agent.
- `PublicKeyPublicationWriting` assembles the public output.

The tests reflect this architecture: actor topology, forbidden edges,
and actor traces. This is the right antidote to previous "converge"
mega-requests.

### Risk pattern: scaffolds that look like implemented features

Several modules are named like features but only prepare directories or
print manual instructions:

- `router/wifi-pki.nix`
- parts of `wifi-eap.nix`
- `headscale-selfsigned-cert` as phase-one TLS
- tailnet enrollment remains manual

Scaffolding is useful, but it must be labeled as scaffolding in code and
tests. Otherwise agents will assume the feature is done because a module
with the right name exists.

### Risk pattern: "fixture says it works" before a booted service exists

Nix option evaluation is powerful, but it does not start services. The
new tests are good architecture witnesses, not operational witnesses.
The next failures will likely be in systemd ordering, service
permissions, real config parsing, runtime state, and network behavior.

### Risk pattern: test surface split across repos

`CriomOS-test-cluster` is a good external witness, but it also means the
main repo's own obvious test command fails without projected inputs.
This can confuse agents and makes "what do I run?" less obvious.

The long-term shape should make the relationship explicit: CriomOS is
the platform repo; CriomOS-test-cluster is the synthetic cluster
conformance repo.

## Tests And Their Meaning

### Tests that passed and what they prove

`horizon-rs` `nix flake check`:

- Rust tests passed.
- Proves typed projection logic, name validation, tailnet roles,
  placement derivation, containment rejection, custom TLD name rendering,
  projection purity source scan, and proposal round trips.
- Does not prove any CriomOS module consumes those fields correctly.

`clavifaber` `nix flake check`:

- Build, fmt, clippy, Rust tests passed.
- Proves actor topology, Kameo mailbox paths for Yggdrasil projection,
  forbidden edge scans, idempotent certificate issuance, publication
  writing, request round trips, and certificate validity-window checks.
- Does not prove Wi-Fi EAP-TLS interoperability, SAN/EKU correctness,
  revocation behavior, dedicated Wi-Fi keypair generation, or cluster
  distribution.

`CriomOS-test-cluster` `nix flake check`:

- Synthetic Horizon projections match fixtures.
- Duplicate tailnet controller fixture is rejected.
- CriomOS module contracts render expected network/Nix/Wi-Fi fragments.
- Source constraints reject known bad module patterns.
- Synthetic `dune` toplevel evaluates.
- Does not boot a system or start services.

Prometheus `run-on-prometheus`:

- The pushed GitHub flake can be checked from another machine inside a
  transient systemd user service.
- Proves the test is not relying on local uncommitted files.

Prometheus `build-dune-on-prometheus`:

- The pushed GitHub flake can build the synthetic `dune` toplevel on a
  remote host inside the same transient sandbox pattern.

### Unexpected test behavior

- The first Prometheus sandbox attempts needed an explicit PATH because
  Nix fetchers needed `git` inside the transient unit. The runner now
  sets PATH explicitly.
- Bare-metal synthetic toplevels exposed the unconditional firmware
  import. That is now tracked as `primary-un7p`.
- `CriomOS-test-cluster` sometimes reports "running 0 flake checks"
  after evaluating derivations because the outputs are already realized.
  That is normal Nix behavior, but easy to misread.
- Building the synthetic toplevel can pull a broad desktop-ish closure
  even with home disabled. This may be expected from current CriomOS
  imports, but closure weight should be watched as Pod/contained-node
  tests become more serious.
- `CriomOS` direct flake check fails without projected inputs. This is
  expected by architecture but poor as a default developer command.

## Tests We Still Need

### Booted router DNS test

Need a VM or nspawn/NixOS test that starts the router profile and proves:

- dnsmasq starts;
- cluster host records resolve;
- tailnet base-domain routing appears only when Headscale is enabled;
- upstream fallback works;
- service recovers from network changes.

This is `primary-58l`.

### Wi-Fi EAP-TLS integration test

Pure Nix cannot prove Wi-Fi. We need a more realistic environment for:

- hostapd EAP-TLS config parsing;
- NetworkManager/wpa_supplicant client config parsing;
- certificate chain validation;
- `domain-suffix-match`;
- anonymous outer identity;
- client authorization;
- revocation or short-lived-certificate behavior;
- actual algorithm compatibility for the CA signature and leaf key.

This likely needs a VM pair, mac80211_hwsim, or a lab AP/client setup.
Until then, Wi-Fi can have source and config-rendering tests, but not a
real connectivity proof.

### Cluster-trust runtime end-to-end

Need a test that runs:

1. ClaviFaber emits public material for host A.
2. The cluster-trust runtime ingests it.
3. The cluster database/Horizon-side public facts update.
4. A synthetic host B receives the public material.
5. CriomOS verifies fingerprints before writing local files.

Without this, public-key/certificate distribution remains a design
story rather than an implemented path.

### Projected CriomOS root check

Need an easy command that answers: "does CriomOS pass with a valid
synthetic horizon/system input?" It can live in CriomOS or be delegated
explicitly to `CriomOS-test-cluster`, but the path must be documented
and discoverable.

### Full deploy-path check through lojix

The synthetic cluster bypasses lojix. That is appropriate for module
contracts, but it does not prove the operator path:

- NOTA request;
- horizon projection;
- system/deployment flake generation;
- build;
- switch/copy behavior;
- Nix signing/cache path.

This belongs after the fixture module tests are stable.

## Current BEADS State

Closed:

- `primary-0tp`: synthetic node toplevel build in sandbox.

Open and still meaningful:

- `primary-a61`: move router Wi-Fi policy and SAE secret out of Nix modules.
- `primary-nvs8`: feed ClaviFaber Wi-Fi EAP certificates into test-cluster fixtures.
- `primary-58l`: VM or nspawn service smoke for DNS and tailnet roles.
- `primary-1ha`: more negative Horizon role fixtures.
- `primary-7ay8`: keep Prometheus sandbox artifacts and run metadata.
- `primary-un7p`: gate all-firmware policy by deployment or hardware capability.
- `primary-8b3`: ClaviFaber owns per-host Yggdrasil keypair; consolidate with network/yggdrasil.nix.
- `primary-tpd`: review Headscale and Yggdrasil roles in CriomOS.
- `primary-cua`: audit whether WireGuard is still used.

BEADS itself showed intermittent embedded-dolt writer contention during
this survey. That is backend contention, not coordination ownership.

## Recommended Next Order

1. **Make the test surface explicit.**
   Document `CriomOS-test-cluster` as the current conformance surface or
   add a synthetic projected check inside CriomOS. This prevents agents
   from treating direct `nix flake check` failure as an ordinary broken
   suite.

2. **Add booted DNS/tailnet smoke.**
   Extend `CriomOS-test-cluster` with a VM or nspawn test for dnsmasq and
   Headscale/Tailscale role rendering. This is the next realistic layer
   after pure module evaluation.

3. **Finish Horizon Wi-Fi policy shape before editing router Wi-Fi.**
   Add `WifiNetwork` or equivalent typed policy, secret references, and
   validation. Do not move the SAE password into another Nix file.

4. **Fix ClaviFaber Wi-Fi certificate profile.**
   Add dedicated Wi-Fi keypair generation, SAN/EKU/key-usage tests,
   explicit CA signature algorithm decision, and revocation/short-lived
   certificate policy.

5. **Create or skeleton the cluster-trust runtime.**
   The public-material distribution path is the missing center of the
   key-management story.

6. **Replace router/client Wi-Fi modules from policy.**
   Once Horizon and ClaviFaber have the correct data, render hostapd and
   NetworkManager from projected policy plus runtime-delivered public
   material.

7. **Decide WireGuard.**
   Fix `wireguard.nix` if it is alive; delete or quarantine it if it is
   not. The current stale bug should not linger inside the active module
   graph.

8. **Gate firmware policy.**
   Let synthetic bare-metal builds run without unfree firmware unless
   the fixture asks for it.

## Bottom Line

The direction is now right: more typed Horizon facts, less cluster data
inside Nix modules, more Nix-backed architecture witnesses, and remote
sandbox checks from pushed commits. The implementation is still in the
middle of the migration. DNS and tailnet roles are in decent shape.
Placement is landing in Horizon but not yet fully consumed by CriomOS.
ClaviFaber is structurally much better, but Wi-Fi PKI remains a design
and integration project, not a live feature.

The next quality jump is not another source scan. It is a booted
service sandbox plus a first real cluster-trust runtime path.
